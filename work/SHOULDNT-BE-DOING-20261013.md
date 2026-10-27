# SHOULDN'T BE DOING — the Mini hot path, reviewed at main 7dea0626 (2026-10-13)

Lane PERF-FIX (Claude). Repo main = 7dea062655060d673ccaad3a8d55493374672a95. Branch `lane/perf-fix` on
hbox:/tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git. Lane tree hbox:/tank/dregg-build/claude-lanes/perf-fix/src.
Continuation: work/PERF-FIX-LOG.md. path:line is at 7dea0626 unless marked (lane).

Method (PERF-PRAXIS): one coarse timing, then a profile, then read. Profiles: `kn2-store-bench` (Host/Kn2StoreBench.lean,
new `KN2_BENCH_CREATES=1` = each record births a cell, so N records = N cells) under `perf record --call-graph dwarf`;
the WORKLOAD script (scripts/perf/workload.sh) under `strace -f -e execve` and flat `perf record`. Comparisons are
same-pass ratios or `instructions:u`; hbox was under load (fn sbcl jobs, WORKLOAD build) throughout.

## Where the time goes (measured, before any fix)

Bench, 64 cell births, inclusive share of the whole run (open + grow + appends):
| share | what | where |
|---|---|---|
| 54% | `deployedHash` — world-root node/leaf hashes | Kernel/WorldRoot.lean:629 |
| 29% | of which `digestOfBytesLE` → `Bignum.denoteNat`: 32 GMP multiply-adds per hash turning 32 bytes into a `Digest` (a Nat) | Compiler/Sp800185Cshake256.lean:87, Theory/Bignum.lean:37 |
| 25% | of which the cSHAKE itself (Keccak + absorb + squeeze to a List) | Theory/Sp800185Cshake256Fast.lean |
| 14% | of which `encodeNat` of both child digests (base-255, GMP divrem) in `nodeInput` | Theory/AuthMap.lean:267 |
| 9.8% + 9.7% | `RootCache.ofEntries` + `RootsExact.ofEntries` — the SAME tree built twice | Compiler/DurableReceiverCore.lean:456,561 |
| 10.5% | `openSealed` re-evaluating the checkpoint root (sparse) | Compiler/DurableCheckpointCodec.lean:603 |
| 17% | `decodeRecordsFrom` — every record decoded on a full open | Compiler/DurableReceiverCore.lean (loadChained) |

Workload (main candidate, N=2 M=1 K=1, strace): **~140 execs of the 173 MB `minidregg-host`** for pure codec verbs
(46 `codec`, 33 `inspect`, 20 `signatures`, 14 `observe-assemble`, 10 `author`, 6 `assemble`), each ~0.38 G
instructions / 40 ms of process init (dynamic relocation + Lean builtin initializers: parser tokens, NameMap, simprocs,
IR). At N=6 the flat profile sampled 662 distinct Host processes; Host processes were 50% of all samples and
`minidregg-client-consent` processes 24%. The serving Host runs from a memfd (`mini serve` → `/proc/PID/fd/7 … stdio`),
which perf cannot symbolize; its own per-request profile is NOT yet taken (see "not yet").

## A. OBVIOUS-LOCAL — fixed on lane/perf-fix (each its own commit; no persisted byte, no theorem statement moved)

| commit | what it removes | where |
|---|---|---|
| e61163fa | 27 of 32 bignum multiply-adds per node hash: `denoteNat` seven limbs at a time (`@[csimp] denoteNat_eq_fast`, `denoteNatFast_eq` for every base) | Theory/Bignum.lean |
| 6913c4a7 | one full Θ(cells·256·H) tree build per full root evaluation: `RootsExact.ofEntries es` rebuilt `RootCache.ofEntries es` for its injectiveCheck (no CSE across the call; profile: 9.8%/9.7%). `RootCache.build` returns cache+exactness from one build; used by loadChained, loadImage, Loaded.build, the advance fallback | Compiler/DurableReceiverCore.lean:561,584,908,1065,1264 |
| aba9f9a8 | Θ((cells+writes)²) `eraseDups` in `Image.cellIds` (`@[csimp] cellIds_eq_fast` through the existing `CellIds.addAll` exactness); `nodupFast` (hashed `List.Nodup` decision, `nodupFast_iff`) | Kernel/SessionIndex.lean |
| a16e2f1b | on a cold light open, two of three full root evaluations: `openSealedWith` hands openHead the tree it checked the sealed root against (`openSealedWith_fst`: same refusals, same body); openHead seeds `extendVerified` with it (`state_entries`), which advances it by the suffix's slots (`suffixSlots`/`replay_entries_step` = the kern-grow WIP patch, cv 01a11e1b-0adc, now also used by `Opening.extend`). Also: `receiveServed` built the full entry list + `extendIds` on every write for a collision fallback (now only on collision); `extendIds` Θ((cells+writes)²) per light write (`@[csimp] extendIds_eq_fast`); openHead's Nodup by `nodupFast` | Compiler/DurableServed.lean:683-688,763-769,894; Compiler/DurableCheckpointCodec.lean:603 |
| 579895c7 | (instrument) `KN2_BENCH_CREATES=1`: the bench only grew history on one cell; the cost axis is cells | Host/Kn2StoreBench.lean |

Before/after, kn2-store-bench, same pass, hbox tmpfs (`/dev/shm`), box under load:
| op | before | after |
|---|---|---|
| light open, 128 cells | 998 ms | 243 ms |
| light open, 256 cells | 2003 ms | 490 ms |
| full open (`load`), 128 cells | 1005 ms | 483 ms |
| full open, 256 cells | 2006 ms | 962 ms |
| light open, 256 records on 1 cell | 15 ms | 6 ms |
| whole bench run, 128 cells (open×3, light×3, grow, 2 appends) | 166.5 G instr:u | 68.2 G instr:u |

WORKLOAD before/after: §E.

## B. OBVIOUS-LOCAL — not yet done (ranked by expected effect)

1. **Pure codec verbs spawn a fresh Host per call** (~140 per tiny workload run, ~0.38 G instr each). native/resource-client/src/main.rs:1173-1191 (`process` → `client_consent::pure_host` → `local_process`), native/resource-client/src/client_consent.rs:46,303. The `codec` session (`codec_process`) exists for some; `inspect`/`signatures`/`observe-assemble`/`author`/`assemble` still exec. Fix: one codec session per client process, reused. Not done here because the socket/session path's refusal handling differs from the one-shot path (main.rs:1313-1338 vs 1200-1214); making them the same is the work, and the journeys must keep passing.
2. **Profile the serving Host per request.** It runs from a memfd (`mini serve`), so perf shows raw addresses. Run it from a file path (or teach `mini serve` an env to exec the file) and take the births-phase profile; the ROOT note (seconds per op at 20 records) says the constant term dominates, and the bench cannot see it.
3. **Full-load verbs per one-shot request**: `NativeHost.openExisting` = `DurableReceiverIO.load` decodes every record and KMACs every tag from height 1, plus three/now two full root evaluations, plus every index over all records. Host/Main.lean:962,3805,3840,4735,4859,6257,7908,7935,7990,8012,8034,8039,8084,8526,8612,8643,8801,8835,8931. `dry-run` does a full load AND a light open (Main.lean:8084-8085). Each verb ported to the light opening removes Θ(history) decode+MAC per call (the serving session already refreshes incrementally).
4. **Full open seeds nothing from the checkpoint**: `loadChained` still evaluates the checkpoint root in `openSealed` and then builds the head tree (2 evaluations). Same move as a16e2f1b, needs the resume-side twin of `replay_entries_step` for `entriesOf image snapshot`. Compiler/DurableReceiverCore.lean:1024,1065.
5. **Checkpoint state lookups are linear**: `State.snapshot.roots c = tableLookup c table` (Kernel/DurableCheckpoint.lean:76-111), so `entriesOf` over all cells is Θ(cells²) per open, and every later lookup walks the install closures down to it. A HashMap built once in `State.snapshot` keeps the statement (`coherent`, `tableLookup_rootTable` as lemmas) but every proof that unfolds `State.snapshot` must be re-done; borderline (counted local because no statement moves).
6. **`RootCache.entries ++ [(k,v)]` per written slot** and `injectiveCheck` walking every entry (Compiler/DurableReceiverCore.lean:452-466,509): Θ(len) copy per write, unbounded list. Cheap next to hashing today; removing the runtime list changes `RootsExact`'s field statement → see DESIGN 4.
7. Callers of `Image.cellIds` compiled before `Kernel.SessionIndex` is imported (Kernel/DurableReceiver.lean:183, `Image.currentCells`) still run the quadratic; move the csimp down to Kernel/DurableReceiver.lean (needs the HashSet machinery there).

## C. DESIGN (persisted shape, type, or semantics — for Ember)

1. **The world-root tree is evaluated per process and never kept** (D3/C2/D5/D6). Even with A, every cold open pays one Θ(cells·256·H). Options: persist node digests beside the MAC'd checkpoint, or a compressed sparse Merkle tree (≈log₂ n hashes per insert, root changes → re-genesis), or a long-lived process holding the Opening (the serving Host does; one-shot verbs do not).
2. **`Digest` is a `Nat`.** 43% of every node hash is converting it (`denoteNat` 29% before e61163fa, `encodeNat` 14%). A 32-byte `ByteArray` digest (or caching each node's bytes in `Tree`) removes it; that changes the `Digest` type and every statement over `Digest.value`.
3. **The executable snapshot is a closure chain** (Kernel/DurableCommitProtocol.lean:150-160; Kernel/DurableDataIntent.lean:240-244): roots/consumed/available/canonicalBytes layered as `fun c => … before.roots c`, history by snoc. Θ(k) per lookup after k installs. A map changes `Snapshot`'s field types (statements). Pair with `Reader.stateAt` + retained 64-checkpoints for `atPrefix` (Compiler/DurableReceiverCore.lean:1307-1312), which needs checkpoint retention (persisted).
4. **`RootCache` carries its proof list at runtime** (D4); state `Good` over the abstract map (an index, erased) instead.
5. **Whole post images in the log and whole-state checkpoints** (C3, D9: Compiler/DurableServed.lean:917-923 seals every cell's full bytes inside every 64th write; Kernel/DurableDataIntent.lean:71-76).
6. **`List UInt8` on the hot path** (4,659 vs 328 ByteArray): records decode bytewise (17% of a bench open in `decodeRecordsFrom`); ByteArray runtime + `@[csimp]` bridges is broad but mechanical; the codec type change is the design part.
7. **`mini serve` executes the Host from a memfd**: harmless for correctness, but makes the serving Host unprofilable by perf; a design choice (sealed exec) with a measurement cost.

## D. Code shape — per-request code that walks retained state (in the spirit of fn's hot_path_check)

Seed "grows with retained state": cells, records/history, tags, index rows, install closures. Flag traversals reachable
from a per-request entry (a CLI verb, a session op, a light receive).
| per-request entry | walk | grows with | status |
|---|---|---|---|
| light receive `receiveServed` | `Served.entriesOf … (extendIds …)` for the fallback | cells (²) | fixed (a16e2f1b) |
| light receive → `Served.advance` | `extendIds` eraseDups | cells (²) | fixed (a16e2f1b) |
| cold light open (every one-shot verb using NativeHostLight) | 3 full root evaluations | cells·256 | 1 now (a16e2f1b, 6913c4a7) |
| one-shot full-load verbs (19 sites, B3) | decode every record, KMAC every tag, 2 root evals, every index | history, cells | open |
| `at` read (`Loaded.atPrefix` below the checkpoint) | genesis replay of the prefix | history (and Θ(h²) via snoc) | DESIGN 3 |
| session first provenance request (`walkPhysical none`, Kernel/NativeHostSession.lean:200) | semantic re-admission walk from genesis | history | open (once per session) |
| every 64th write | seal every cell's full bytes + MAC over them | state bytes | DESIGN 5 |
| any open | `Image.cellIds` eraseDups | cells+writes (²) | fixed where SessionIndex is visible (aba9f9a8); B7 |
| any open on a checkpoint | `tableLookup` per cell | cells (²) | B5 |
| client CLI step | one Host exec per pure codec verb | — (constant 0.38 G) | B1 |
A static check for this class: list functions reachable from `Host/Main.lean` verb arms and `NativeHostSession` ops;
flag any that call `load`, `loadChained`, `RootCache.ofEntries`, `deployedRoot`, `Image.cellIds`, `eraseDups`,
`atPrefix`, `List.foldl` over `image.accepted`. Not written in this lane.

## E. Verification

Build: every touched module and `kn2-store-bench` green with `swarm-build lake build`; candidate built in the lane with
`deploy/candidate/lane-build.sh host|consent|rust|pack` (host binary sha256 fbcfb2e3…, consent 03b521ef…), packed at
hbox:/tank/dregg-build/claude-lanes/perf-fix/candidate. Main's candidate = WORKLOAD's warm-7dea0626/candidate.

Journey rows (driver perf-fix/run-rows.sh = journey-runner's row environment; evidence perf-fix/rows-{main,fix}/):
| row | main 7dea0626 | lane a16e2f1b |
|---|---|---|
| journey (J0–J8, JROT, JROTL, JRLANE, JGATE, JAUDIT) | PASS | PASS |
| call (63 rows) | PASS | PASS |
| send (192 rows) | PASS | PASS |
| objectrecord (39 rows) | PASS | PASS |
| growth (1000 records) | **FAIL**: write p50 2.569 s, p99 10.874 s, max 13.334 s; reopen 2.113 s (load 3.8) | **PASS**: write p50 2.051 s, p99 2.958 s, max 3.894 s; reopen 1.554 s (load 2.2) |

WORKLOAD (scripts/perf/workload.sh as present in the tree, which ran N=32 M=32 K=16 seed 20261013; same script, same
box, back to back, `PERF_UNDER_LOAD=1`; instruction counts are the comparable figure, wall is under load):
| phase | main instr:u | lane instr:u | ratio | main p50 (op) | lane p50 (op) |
|---|---|---|---|---|---|
| genesis | 40.63 G | 27.55 G | 1.47× | 2.71 s | 2.08 s |
| setup | 231.41 G | 158.27 G | 1.46× | | |
| births | 3587.52 G | 1991.13 G | 1.80× | resource 3823 / create 2519 ms | resource 2118 / create 1471 ms |
| updates | 4465.52 G | 2017.39 G | 2.21× | invoke 7966 ms (p99 22110) | invoke 3937 ms (p99 11146) |
| reads | 1554.37 G | 797.48 G | 1.95× | read-at 5155 ms | read-at 2703 ms |
| checkpoint | 71.02 G | 37.08 G | 1.92× | certify 4246 ms | 2214 ms |
| judgment | 418.76 G | 211.40 G | 1.98× | call 8905 / send 9490 ms | 4407 / 5281 ms |
| reopen | 56.20 G | 26.51 G | 2.12× | to-first-read 3046 ms | 1577 ms |
| total wall | 722.5 s | 388.9 s | | | |
Both runs: 110 records, 36 objects, `phases failed: reads` on main and lane alike (the reads phase's own check; not
introduced here). Raw: /tmp/pwM, /tmp/pwF on hbox; perf-fix/runs/wl-{main,fix}.out.

What is still wrong at this point (ROOT's merged order, work/PERF-ATTACK-ORDER-20261013.md): seconds per op at ~100
records are the constant whole-Store work inside the warm server per request — item A (`NativeHost.confirmed`
cold-opens the Store per readback, Kernel/NativeHost.lean:1245, callers :1270–2637), item C (decideTurn ×5),
E, and the rest of F. Not started in this lane; pointers in PERF-FIX-LOG.md.

### Priced after the fixes (trace run on the lane candidate, N=32 M=32 K=16)
Serving Host per-op totals from `MINIDREGG_HOST_TRACE=1` (hbox /tmp/pwT/w/public/serve.log):
| op | total | n | p50 | max |
|---|---|---|---|---|
| 212 receipt readback (`confirmed` → full cold open; item A) | 52.9 s | 73 | 843 ms | 2112 ms |
| 2 submit | 25.7 s | 36 | 480 ms | 2029 ms |
| 210 | 12.4 s | 107 | 122 ms | 458 ms |
| 1 prepare | 9.5 s | 36 | 157 ms | 812 ms |
| 214 public view | 9.3 s | 128 | 44 ms | 434 ms |
| 144 / confirm refresh / 91 / 5 | 3.8 / 3.8 / 3.7 / 3.0 s | | | |
The server accounts for ~127 s of a ~390 s run; the other ~2/3 is client-side process work (B1, ROOT's G/H/I/L).
