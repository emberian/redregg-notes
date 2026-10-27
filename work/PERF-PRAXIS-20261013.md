# PERF-PRAXIS — how Ember and Claude actually do performance work (2026-10-13)

Scout: PERF-PRAXIS (Claude). Sources: three repos' perf artifacts plus the root sessions that steered them.
Session ids are Claude transcripts under `~/.claude/projects/<proj>/<id>.jsonl` (line numbers = transcript
line); `01a1…` ids are Codex sessions (`cv show <id>`). Repos: `~/dev/cv` (Rust), `~/dev/fn` (ACL2/SBCL
NNTP node), `~/dev/delvetalk2` (Lean host + Bend world + Python tests).
Sampled: cv `c6df902e` (lines 5241–5441 + perf-2 lane `subagents/agent-a5dd0d95a2e1e3bad`, `-a3d96bdb052a64c6f`);
delvetalk `81183e86` (935–1281), `769be5f2` (6072–6674); fn `1db4b0cd` (1755–13501). Note: `cv search`
and `cv touched` returned nothing useful for these repos today (index stale for them); `cv ls --cwd` + rg on
transcripts worked.

## 0. The three campaigns in one line each

| repo | trigger (Ember) | result | record |
|---|---|---|---|
| cv | "why IS cv index so slow… are we parsing entire files when we only need to be skipping around?" (`c6df902e`:5241); then "we can't be blowing up to GBs of heap… hella fast" (:5438) | full recount 329 s → 61–68 s, append 23–36 s → 0.7 s, then per-store heap from GBs to KB-flat | `docs/design/PERF.md`, `PERF-HANDOFF.md`, `DATAPATHS.md`, `tools/profiling/` |
| delvetalk2 | "why is it soooo slowwww. something has gotta be concretely foolish" (`81183e86`:935); "our tests used to take <30s" (`769be5f2`:6139) | test_objects 233 s → 33 s; suite 664 s → 88 s → 54 s; later 10–15 min → 132 s → 30.2 s | `docs/PERF.md`, `docs/review/slowness-2026-10-12/` (ROUTING + 6 facets + FAST-SUITE), `tests/PROFILE.md` |
| fn | "why are we still obnoxiously inefficient…100s store open" (`1db4b0cd`:1755); "cannot accept that those proofs took over an hour" (:12888) | 20k-article open 312 → 103 s; greeting 95 s → <0.5 s; ranked user-wait ledger; throughput + proof-cost ratchets in `make check` | `planning/performance-2026-09-26.md`, `planning/scale-profile.md`, `tools/throughput_gate.py`, `tools/proof_cost.py`, `tools/hot_path_check.py` |

## 1. Workload design

- **Real data, frozen.** cv measured against Ember's real fleet (~6,750 sessions, 95–97 GB), but before/after
  on an APFS-clone (`cp -c -R`) "frozen" copy so live sessions don't move between runs; catalog copied into a
  scratch `CLUSTERVISION_HOME`, originals write-denied (`PERF.md` "After"; `PERF-HANDOFF.md` "How to measure").
  Live-fleet numbers were kept but labelled "observations, not frozen before/after claims" (`PERF.md` composed-path).
- **Largest-real-input-per-category.** cv's table is "the largest real session per harness" (gemini 299 MB,
  codex 675 MB, claude 181 MB) — the worst case each code path meets (`PERF-HANDOFF.md` table).
- **Scale pairs, not single sizes.** cv's heap work uses generated fixtures at **16 MiB and 64 MiB** (and
  20k→200k events/calls); the claim is "flat" across the pair, so a gate tests *growth*, not a point
  (`tools/check-heap-budget.py`: `SIZES=(16 MiB, 64 MiB)`, `STORE_CEILING=8 MiB`, `STORE_GROWTH=2 MiB`).
  fn: an N-grid (N=16…20,000 articles × payload × groups) via `tests/bench/generate.py` + `measure.py`
  with a seed (`planning/scale-profile.md` §Environment); delvetalk: one-row write at 16 vs 2,048 rows
  (`deploy/bench-write.py`) — the expected answer is "close", i.e. O(changed cells).
- **Captured request streams replayed.** delvetalk tee'd real host stdin into JSONL (Counter bump 6 lines;
  64-field spell parse 99; directory `receive` 16,869 lines from 1,763 archived posts) and replays them with
  `compile-profile replay LINES DIR FILTER R`, fsync off, best-of-R per class (`docs/PERF.md` "How it is measured").
- **User operations, not helpers.** fn's ledger ranks "seconds a user waits per common action" (OVER, greeting,
  POST, restart, checkpoint…) — "a fast helper is not a fast command" (`performance-2026-09-26.md` header).
  cv was *corrected into* this: Ember asked to zoom out from giant-payload heap work; DATAPATHS now ranks
  list/filter/read/refresh/export with cold/warm/one-change labels and time-to-first-useful-output
  (`DATAPATHS.md:7`, commit `29eb96ce`).
- **Size/duration:** single operations run 0.05 s–6 min; delvetalk's directory replay ~120 turns; fn phases each
  in their own `systemd-run --scope MemoryMax=24G` on `/dev/shm` (`performance-2026-09-26.md` §Measurements).

## 2. Baselines: how taken, where stored

- **First deliverable of the lane = a budget doc** with a baseline table per command and a budget column
  (cv perf-2 brief step 0, `agent-a5dd0d95…` line 0; result `PERF.md` "Baseline (0.16.1)" + "Budgets").
  Each row says *where the time goes* ("98% under `stream_counted`, 95% of that in codex").
- **Baselines are committed JSON, keyed by revision + binary hash.** fn `planning/throughput-baseline.json`:
  per metric `value`, `release`, `dev`, `floor`, `tolerance 0.25`, `core_sha256`, `quiet` flag; runs land in
  `planning/throughput/<sha>-<label>-<UTC>.json`. cv `tools/profiling/results/*.json` carries input SHA256,
  binary SHA256, compiler, image manifest. fn evidence dir has a `SHA256SUMS` (`performance-2026-09-26.md`).
- **Ratchet semantics:** fn baseline value = min(release, dev), so an improvement lowers the bar at next write;
  `proof-cost-baseline.json` "only shrinks without --allow-regression" (both files' `about`).
- **Suite timing baseline:** delvetalk `tests/run.py --baseline` rewrites checked-in `tests/timings.json`
  (slow classes, used to schedule slowest-first); a merge must hold the hbox baseline (`81183e86`:1197
  "581 tests, 54 s… the number every merge must hold to").

## 3. Profilers and measurements, and what they caught

| tool | where | caught |
|---|---|---|
| `/usr/bin/time -l`, release, best of 3; `footprint`/`vmmap` for mmap-heavy | cv `PERF.md`, `PERF-HANDOFF.md` | RSS ≠ footprint: codex 574 MB RSS was mostly file-backed mmap; gemini 1.12 GB was real |
| macOS `sample` | cv baseline | `cv index` single-threaded; 5.2 M page faults; 68% of claude parse in `serde_json::Value` |
| ratio to `std::fs::read` / `cat` of same bytes, same run | cv `perf_budget.rs`, `c6df902e`:5279 | parser was 400–750 MB/s, *not* the problem; re-reading whole files on any change + one core was |
| counting global allocator (`probe-heap`) | cv `check-heap-budget.py` | heap scaling with file size: Gemini 841 MB → 42 KB; Codex 49.7 MB → 4 KB flat |
| Cachegrind (instruction counts, Linux ARM64 container, 1 rayon thread) | cv `tools/profiling/README.md`, `cachegrind.py`, `compare.py` | 0.0051% run-to-run variation; attribution `serde_json skip_to_escape` 21.8%, dyld 9% |
| `perf stat -e instructions:u` (sum cpu_atom+cpu_core) | delvetalk `docs/PERF.md`, `FAST-SUITE.md` | load-independent A/B on shared hbox; replay 189.0 → 170.1 G |
| `perf record -F 299 --call-graph dwarf` + `stacks.py`/`under.py` | delvetalk | the machine is 7% of a turn; checkpoint encode/digest/decode around each segment is ~64%; `mi_malloc_small` 16% self |
| SBCL `sb-sprof :cpu`/`:alloc` between trigger files; `get-bytes-consed` | fn ledger | OVER 95% in one number→entry walk; BP codec 99% in bitwise CRC-32C via `floor`; 16 B/octet cons lists |
| per-stage timers / timing spans (`DELVETALK_TIMING_FILE`) | delvetalk `81183e86`:939, `769be5f2`:6165 | elaborate re-parsed type strings per lookup (290 → 15 ms); compiled defs discarded per render |
| **static scan** for "per-request function traverses retained-state collection" | fn `tools/hot_path_check.py` (+ `hot_path_dimensions.json`) | 173 whole-state sites on hot paths (`1db4b0cd`:1835) |
| **read-only LLM reading swarm** (6 codex sol facets) | delvetalk `docs/review/slowness-2026-10-12/ROUTING.md` | 100 findings with file:line, incl. the compile-discard regression (genesis 25 → 12 s, 48 → 7 s warm) |

## 4. Regression detection and gating

- **fn throughput gate** (`tools/throughput_gate.py`, `make check` line ~2868): born because "a ~20x commit
  slowdown reached dev through green merges" and half of it was tmpfs-vs-ZFS. Rules: tmpfs only, one systemd
  unit, box checked quiet (another unit >QUIET_CPU refuses with exit 3 and names it), fail above
  `max(value*(1+0.25), value+floor)`, a dev regression needs a row in `planning/throughput-causes.json`.
  Merges were held "under the throughput gate" until it passed (`1db4b0cd`:1187, :1712).
- **fn proof-cost ratchet** (`tools/proof_cost.py`, `planning/proof-cost-baseline.json`): 10 s rule, prover
  *steps* ratcheted (load-independent), seconds only from quiet ≤2-job runs.
- **fn hot-path check** `--summary --strict` in `make check` (Makefile ~3156): a static gate on the *shape*
  of the code, not its timing.
- **cv CI gates with no wall-clock threshold:** heap ceiling + growth at 16/64 MiB; "a baseline reader fails
  the same gate on source scaling, demonstrating that the gate catches the original defect" (`PERF.md`
  datapaths pass). Commit `0fd1d532` "Require active allocator counters in operation heap gates" — a gate
  must prove its instrument was live. The throughput-ratio gate is explicitly "a regression check, not
  evidence of a small improvement" (`PERF.md` Budgets).
- **cv Cachegrind compare refuses unmatched controls** (`tools/profiling/compare.py`): input SHA, seed catalog
  SHA, rayon threads, rustflags, image manifest, and native/profiled output parity must all match or it errors.
- **delvetalk:** `make smoke` as the fence ("a merge that doubles it does not go in", `81183e86`:972); hbox
  suite baseline. Its own audit later flagged wall-clock bounds in unit tests as bad tests (`tests/PROFILE.md`
  "flagged when … a wall-clock bound") after a 50 ms render bound went red under load 30 (`81183e86`:1275).

## 5. Order of operations that worked

1. **Measure the boundary once, coarsely, before theorising** — three timings (compile, turn, second turn)
   (`81183e86`:939); cat vs parse vs grep (`c6df902e`:5279). This killed the wrong hypothesis both times
   ("skipping around" would not win; parser was fine).
2. **Then read the code at the hot span** — Ember: "we'll notice right away why it's slow" (`81183e86`:981);
   the investigator found 219 knot fields elaborated when 4 were needed, by reading.
3. **Fix the foolish/asymptotic things first** (quadratics, discarded caches, whole-state re-validation,
   re-reading unchanged bytes, one core of twelve). These gave the 5–10× wins in all three repos.
4. **Only then micro-work**, A/B by instruction counts (delvetalk SHA-256 rounds 9.8 → 5.9 ms/MB; cv typed
   borrowed records).
5. **Every change: before/after in the commit + byte-identical output** (cv hashed every message of 924
   claude / 4,225 codex sessions; delvetalk journal + snapshot byte-identical; `@[csimp]` proved equal).
6. **Gate what you fixed**, with a gate shown to fail on the old code.

## 6. Mistakes made and corrected

- **Bisecting a 10-minute suite.** Claude proposed "bisect first"; Ember: "no bisects please… source
  inspection, tracing, looking for derpos" and then "before-and-after number collecting on a suite that takes
  10 minutes is going to take hours" → read-only codex swarm (`769be5f2`:6153–6208). Found the regression in
  one pass.
- **Wall-clock on a shared box as evidence.** cv's PERF.md ran under load 20–180; it was retracted into
  "Measurement correction: count the work" — instructions, bytes scanned, allocations, SQLite VM steps
  (`DATAPATHS.md:55`). fn: an accidental re-run at load 8–9 vs 5 moved latencies ±20% and medians 46%;
  "a ratio taken between two points measured in the same pass is what this campaign can defend"
  (`scale-profile.md` §Replication).
- **Mixing filesystems.** fn's "20x" was half tmpfs-vs-ZFS (`throughput_gate.py` docstring). Every figure now
  names its FS.
- **Measuring a test client, not the server.** fn ARTICLE figures were mostly 4–5 ms of Python unbuffered
  `recv` per octet until the client was buffered (`throughput_gate.py` "client").
- **Fixing heap and silently regressing CPU.** cv's two-pass Zed reader bounded memory but was 2.2–2.6×
  slower; caught by clean CPU triples, replaced by decoded-spill (`PERF.md` composed-path; commits
  `0bcfa6e7`, `4e360a0d` record prune CPU regressions explicitly).
- **Over-indexing on one axis.** cv spent a day on giant-payload heap; Ember steered back to whole operations
  (`DATAPATHS.md:7`).
- **Wrong premises in the brief.** delvetalk: "canonical CBOR for packets buys nothing (JSON parse is 7 ms)"
  — the investigator refuted two brief claims (`81183e86`:1008). fn: "is that proving time or runtime?"
  answered by profile: runtime (`1db4b0cd`:1835).
- **Running perf on the laptop.** "we're absolutely hammering this laptop" → hbox; the laptop at load >100
  made an fsync-bound test red that was green on hbox (`81183e86`:1125–1197).
- **Waiting on slow things.** "the appropriate response would have been to notice no progress was being
  made, inspect the source for the slowdown" (`1db4b0cd`:12888) → fn's "no silent waiting" rule for slow books.
- **Benchmark ritual before there is something to measure (Mini itself).** Ember to a minidregg Codex
  session: "Can we please stop doing verification and benchmarking ritual before we even have something worth
  doing it about?" — rolling benchmark matrices and full-tree rebuilds after every micro-step were dropped
  for "one smoke check only when a substantial join is complete" (`019fe595-32a8`, 2026-08-09). The perf
  harness serves a named slow user operation; it is not a per-commit ceremony.
- **Tried-and-not-kept is recorded** (delvetalk `docs/PERF.md` "Tried and not kept"), which stops re-trying.

## 7. Reusable as-is for Mini

- `~/dev/fn/tools/throughput_gate.py` design: quiet-box check, one unit, tmpfs, `max(v*(1+tol), v+floor)`,
  ratchet baseline, causes file. Port the shape (828 lines; the NNTP phases are fn-specific).
- `~/dev/fn/tools/proof_cost.py` + `planning/proof-cost-baseline.json`: directly relevant to Mini's Lean
  build cost — ratchet *heartbeats/steps* rather than seconds; seconds only from quiet runs.
- `~/dev/fn/tools/hot_path_check.py` idea: seed "grows-with-retained-state" collections, flag traversals
  reachable from per-request entries. For Mini: per-turn functions that walk the whole store/world.
- `~/dev/cv/tools/profiling/cachegrind.py` + `compare.py`: native-parity check, pinned threads, refuses
  unmatched controls; works on hbox natively (Linux) with no container. `compare.py` is 47 lines, copy it.
- `~/dev/cv/tools/check-heap-budget.py` pattern: two input sizes, ceiling + growth, run the *old* code once
  to show the gate goes red.
- `~/dev/delvetalk2/spec/CompileProfile.lean` `replay` pattern (Lean): capture real host requests with a
  `tee` wrapper, replay per class best-of-R with fsync off — Mini's host is Lean too.
- Table formats: cv `PERF.md` "command | real | RSS | where it goes"; fn "# | user action | waits | cause
  (function) | fix pattern | owner | expected"; delvetalk "inclusive share | what | file:line".
- delvetalk `docs/review/slowness-2026-10-12/ROUTING.md`: the reading-swarm routing table format
  (finding | file:line | cost×frequency | fix | est. saving | lane), with "estimates are guesses from reading".

---

## One-page recipe for the Mini performance effort

**Box:** hbox, `swarm-build`, `taskset -c 0-15` (P-cores), tmpfs for store I/O unless measuring durability.
Record load average + other running units with every number. Never the laptop.

| # | step | tool | artifact left |
|---|---|---|---|
| 1 | **Name the user operations** (admit a turn, open/replay a store, re-genesis, build/check, node cold start, serve a read) and pick the largest *real* input each sees today | Ember's complaint + node logs | `docs/PERF.md` §Operations: op, input, size, cold/warm/one-change label |
| 2 | **Freeze inputs**: copy a real store/journal (or capture a request stream with a `tee` wrapper), seed fixed; add a 2-size synthetic pair (e.g. N and 4N rows) | `cp`, tee wrapper, generator script | `bench/fixtures/` manifest with SHA256 of every input |
| 3 | **Coarse baseline per op**: wall, user+sys, peak RSS, best of 3, interleaved; plus a "plain read of the same bytes" control where it applies | `/usr/bin/time -v`, a per-stage timing span env var in the host | baseline table in `docs/PERF.md` with "where it goes" column; JSON under `bench/results/<sha>-<label>-<UTC>.json` with binary sha + load |
| 4 | **Profile the top 3 ops** | `perf record --call-graph dwarf` (Lean/Rust), `perf stat -e instructions:u` | inclusive-share table with file:line; raw profiles + binary copy kept on hbox (`bin-<name>`, else symbols die on rebuild) |
| 5 | **Read in parallel**: a read-only swarm (one per subsystem) hunts quadratics, discarded caches, whole-state walks per request, repeated encode/hash/decode. No bisect | codex/Opus readers | `docs/review/slowness-<date>/ROUTING.md` (finding, file:line, cost×freq, fix, est., lane) |
| 6 | **Fix asymptotic/foolish first**, one change per commit | lanes | commit body: before/after (instructions + wall + load), byte-identical output proof (journal/state root/receipts hashes; or a Lean equality theorem for a `@[csimp]` swap) |
| 7 | **Micro-work last**, A/B only by instruction counts on the frozen inputs | `perf stat` / Cachegrind + `compare.py` | `docs/PERF.md` "Before and after" + "Tried and not kept" |
| 8 | **Gate**: (a) throughput ratchet per op, quiet-box, tolerance+floor, causes file; (b) growth gate at 2 sizes (flat = O(change)); (c) static hot-path check; (d) Lean build-cost ratchet on heartbeats. Run each gate once on the *old* code to prove it goes red | ports of fn `throughput_gate.py`, `proof_cost.py`, `hot_path_check.py`; cv `check-heap-budget.py` | `bench/baseline.json`, `bench/causes.json`, `make`/`scripts/local-gates.sh` steps |
| 9 | **Handoff** whenever context runs out: the agent that measured writes the continuation (method, done, next rows ranked by last profile) | — | `FAST-SUITE.md`-style continuation file |

Rules carried over: no harness without a named slow operation (`019fe595-32a8`); measure once coarsely before theorising; never quote a single absolute from a shared box
as an improvement (ratios within one pass, or instruction counts); name the filesystem; check the client
isn't the bottleneck; a heap/latency fix must report the other axis; "a progress banner is not a result; a
failed command is not a performance success" (`DATAPATHS.md:7`).
