# PERF-CLIENT log (continuation file) — started 2026-10-14 00:30
Lane: PERF-CLIENT (Claude). Front: native/resource-client/** + scripts/perf/**. Items G, H, I, L, M(client).
Lane dir hbox:/tank/dregg-build/claude-lanes/perf-client. src = clone of bundles/burst3-minidregg.git lane/perf-fix
(a16e2f1b) + merge of lane/perf-workload (d37eee80, scripts/perf) = dbecaa17. .lake = cp -al of perf-fix's (never built:
this lane changes only Rust/Python; no lake run). Pushes -> lane/perf-client.

## method (so a successor can rerun)
- Candidates: `mkcand.sh NEW COMMIT MINI` = copy of cand-base (perf-fix's packed candidate @a16e2f1b: Host fbcfb2e3…,
  consent 03b521ef…, same .lean inputs as this lane) with bin/mini replaced, manifest paths relocated, every sha pin of
  mini + provenance rewritten (journey row checks the provenance pin). lane-build.sh pack refuses here because its
  compiled-input check counts native/*/src/** against the HOST build; the Host is not built from those.
- mini built exactly as lane-build.sh rust does (same RUSTFLAGS remap), mini only: `bmini.sh` (SRC=worktree);
  per-commit bins reproducible (mini-I == mini built from src at the same tree).
- Runs NEVER read lane src: one worktree per commit (wt-base dbecaa17, wt-G2, wt-H2, wt-I) — see "incident" below.
  `WLSRC=<wt> wl.sh CAND TAG N M K [strace]` -> /tmp/pc-TAG, runs/TAG.out (+ runs/TAG.strace with -ttt).
- Host count: `execs.py runs/TAG.strace /tmp/pc-TAG` = execve of the Host image (path or /proc/PID/fd memfd) by verb and
  per phase / ops. N=4 M=4 K=4 for strace runs (checkpoint phase red there by design: history < 64).
- Rows: run-rows.sh <worktree> <cand> <out> journey call send objectrecord.

## events
- 00:40 baseline b0-32 (cand-0 = perf-fix a16e2f1b candidate, wt dbecaa17): PASS, phases failed: NONE.
  births 2056G updates 2146G reads 898G; read-current p50 128 ms, read-at p50 2702 ms, invoke p50 3942 ms. Wall 326 s (under load).
- READS FAILURE (brief item I "confirm"): NOT the cold opens. PERF-FIX's "phases failed: reads" (/tmp/pwT, 23:55) were
  `no-grant` refusals of `at` reads at heights below the object's birth (at-b0005-15, object born at acceptedCount 21)
  from the then-uncommitted workload.py's height formula; the committed d37eee80 derives G from a probe challenge and
  passes reads (b0-32 above).
- baseline strace N=4: 216 Host execs / 61 mini processes; codec=67 (local_frame per frame) + one-shot pure verbs
  inspect 52, signatures 30, observe-assemble 22, author 16, assemble 8 (process() -> local_process, since local
  consent was not pinned) + challenge/query 5+5 (cold). Hosts/op: births 7.50, updates 5.00, reads 4.38, setup 5.67.
- G committed 20a9a091 (+ test ad17b5c9). FIRST VERSION WAS VACUOUS for the workload: activity.rs and checkpoint.rs read
  workspace.json raw, so the pin never reached them (strace showed the Host opened); fixed by pinning in both readers.
  Micro-benchmark (one `mini activity view`, P-core, cpu_core/instructions/u): pinned 0.61 M instr / 1.7 ms CPU, unpinned
  444.3 M instr / 180 ms CPU. The hash WAS essentially the whole client cost of a current read.
- G plant (plant-g.sh, real Store /tmp/pc-h-s, tampered scratch Host cand-H): pin fbcf…, file -> 6908…;
  running server keeps serving its sealed verified image -> view rc=0; `mini --verify-host` / MINI_VERIFY_HOST=1 ->
  rc=1 "differs from the workspace's pinned hostSha256"; `serve` restarted on the tampered file -> rc=1
  "socket rejected request: host image pin mismatch" (transport::request_from_envelope). Unit test ad17b5c9.
- H committed 3da880ea: strace N=4 Hosts 216 -> 61 (births 7.50 -> 1.00/op, updates 5.00 -> 2.00, reads 4.38 -> 1.88,
  setup 5.67 -> 1.00). The remaining one per mini process is its codec child.
- I committed eb3e3570: `mini query --workspace` (checked loader; socket + Host pin), workload.py uses it.
  strace N=4 with I: challenge/query cold Hosts 5+5 -> 0.
- Rows: G2 journey/call/send/objectrecord PASS. (rows on the first G/H candidates: call/send/objectrecord PASS, journey
  refused the candidate on the provenance pin -> mkcand fixed.)
- INCIDENT (mine, 01:27-01:30): I patched activity_world.py in lane src while workload runs + rows read scripts from
  lane src -> i-32, b1-32 updates red; rows-H2 call/send raised (mini-H2 got --quote-front-end). Results discarded
  (runs/old, rows-H2.contaminated); worktree-per-commit since. g2-32/h2-32 also invalid (wt HEAD's workload.py used
  `query --workspace`, unknown to G2/H2 minis) -> rerun.
- 02:00 ROOT: G/H/I/L approved; G's weakened check goes to Ember; keep as committed, no per-process hash for codec
  children. G message reworded to open with "CHECK MOVED" (per-request file hash -> serve-start pin check + explicit
  --verify-host). Rebase (message only, tree identical): G 20a9a091->764d6bb6, H 3da880ea->22166640,
  I eb3e3570->a939a35d, plant test ->142f60f3, L 21f0a31f->7cc040d6. Candidates/worktrees carry the old ids.
- N=32 under heavy box load (rows running, others' Lean): wall 641/651 s for G2/H2 vs 326 s baseline; instructions:u
  NOT comparable across these runs (multiplexed hybrid PMU + server idle work scales with wall: G2 read higher than
  base). Robust signals: read-current p50 128 -> 56 ms (G). Final client numbers come from stepbench.py
  (per-step perf stat over the client process tree only, base vs new alternated on one Store).
- Rows H2 (rerun in wt-H2): journey/call/send/objectrecord PASS. L rows running.
- 02:25 all rows PASS: G2, H2 (rerun), I (+ journey rerun in wt-I), L — journey, call 63, send 192, objectrecord 39.
- N=32 (all phases completed, all PASS; box load avg 20-30, wall/instr indicative only):
  | run | wall | resource p50 | create p50 | invoke p50 | read-cur p50 | read-at p50 | instr births/updates/reads G |
  | b0 (base, quieter) | 326 | 2148 | 1501 | 3942 | 128 | 2702 | 2056/2146/898 |
  | b1 (base, loaded)  | 511 | 4239 | 2762 | 5233 | 153 | 3001 | 2268/2235/890 |
  | i-32 (G+H+I)       | 512 | 3012 | 2470 | 5612 |  83 | 3288 | 2060/2279/407 |
  | l-32 (G+H+I+L)     | 463 | 1696 | 1421 | 5515 |  60 | 3979 | 2098/1785/406 |
  reads instructions halve with I (890 -> 407 G), updates -20% with L. read-at WALL does not drop: the session's
  `at` is itself slow (K: session base = head after rebase -> genesis replay) — a server item.
- Host processes (strace N=4 M=4 K=4): base 216 / 61 mini -> L 45 / 55 mini. Per op: births 7.50 -> 1.00,
  updates 5.00 -> 1.00 (and 2 -> 1 mini process), reads 4.38 -> 0.62, setup 5.67 -> 1.00, judgment 4.33 -> 1.00.
  The one left per mini process is its codec child.
- stepbench (client process tree only, cand-0 vs cand-L alternated on /tmp/pc-l-32, median of 3, loaded box):
  | step | base instr / CPU / wall | new instr / CPU / wall |
  | view (op 214)  | 0.444 G / 279 ms / 385 ms | 0.001 G / 2 ms / 92 ms |
  | read-at        | 110.5 G / 10.6 s / 10.9 s | 63.7 G / 4.9 s / 5.8 s |
  | invoke         | 54.5 G / 8.0 s / 11.5 s (2 procs) | 41.4 G / 3.6 s / 6.8 s |
  | birth          | 28.7 G / 6.4 s / 10.1 s | 49.6 G / 3.9 s / 7.9 s (instr UP, CPU down: unexplained; suspect consent
    suffix admission asymmetry between the two candidates' anchors) |
- NEXT CLIENT-SIDE OFFENDER (measured, perf record --sort comm): ~99% of the remaining client instructions of a
  read-at, invoke or birth are in minidregg-client-consent (the consent provider; anchors are reused within a run,
  so it is per-frame decision, not genesis admission). That is Lean (Host.ClientConsentSession) and attack-order
  DESIGN ("consent provider re-execution"): not done here.
- M client parts: none LOCAL remaining in Rust/Python. Server-side helper execs seen per run (credential-verifier 66,
  sqlite-store 43, sh 72, chmod 41 at N=4) are the Host's (withPinnedSignature, durable-read helper) = M server items.
- Pushed lane/perf-client = 7cc040d6. Commit messages of H/I/L carry the term removed but not the measured numbers
  (they are here); I did not force-push to add them.

## PERF-CLIENT-2 (2026-10-14): PR #3 (akapug) folded into H -> c1cc0a89 on lane/perf-client
- Followed CONTRIB-REVIEW-20261014.md. One commit c1cc0a89 on 7cc040d6, client_consent.rs only, co-authored
  akapug <cto@minusculeventures.com>. PR head fetched as refs/contrib/pr3 (3b7b8a70) in lane src; not cherry-picked.
- Taken: anchor_binding key (image path + inode identity + settings-bytes SHA-256), explicit drop on settings change
  mid-frame, pug's test verbatim. Fixed in H: failed/out-of-turn refusal-decode exchange drops the child (test
  codec_child_that_dies_decoding_its_refusal_is_replaced); shared test lock CODEC_TESTS + CODEC reset in all 4 codec tests.
- RED observed on H code (logs/pr3-red2.log): pug's test 2 starts != 3 at the replaced image; decode test "Broken pipe"
  on the next frame (dead child kept). GREEN after (logs/pr3-green2.log): `codec_` 6/6, x6 reruns at --test-threads=16.
  `one_shot` filter matches only agent_reserve::lost_op2_reply_keeps_one_shot_marker_and_exact_call (unrelated, ok).
- DEVIATION FROM THE REVIEW (measured): the settings PATH is NOT in the key. First version had it (pug's key):
  strace N=4 control went 45 -> 53 Host execs (setup 12->16, births 8->12). Traced with -s 300 + clone edges
  (runs/p3-d.strace): exactly the 8 `mini workspace create` processes, each starting a 2nd codec child because the
  attempt dir is renamed attempts/a-<nonce> -> attempts/create-<name> between frames (same config.json bytes).
  Host.Main loadSettings = parse of bytes; serveCodec takes config/providerRoutes once at start; path irrelevant to the
  child. Key = anchor_binding only; test codec_child_is_kept_across_a_renamed_settings_directory. (Unpushed commit
  amended 054caee2 -> c1cc0a89.)
- Control: cand-P3b (mini 11c788c6…), wt-P3 @ c1cc0a89, runs/p3b-s: HOST 45, per-phase identical to L (runs/l-s.execs2).
- Rows (rows-P3b): journey PASS (J0-J8, JROT, JROTL, JRLANE, JGATE, JAUDIT), call PASS 63, send PASS 192.
- Pushed bundles/burst3-minidregg.git lane/perf-client = c1cc0a89. GitHub push from hbox: NO KEY (publickey denied);
  ROOT to push. Reply for pug: /Users/ember/dev/redregg/work/PR3-REPLY.md (not posted).
- REGRESSION FROM H (INTEGRATOR on next) -> 859b6695 on lane/perf-client (bundle pushed; GitHub: ROOT).
  Scope measured (HEAD vs wt-G2 = 764d6bb6 tree, filters fleet:: provider_continuity:: selected_publisher::
  key_adoption:: stale): H broke 4 recovery fixtures (fleet exact_operation_lost_reply..., provider_continuity
  guarded_attempt_lookup..., selected_publisher truncated_submit... + an_old_absent_lookup...), all /bin/sh fakes
  answering one-shot `inspect` argv; since H every pure verb goes to the `codec` child. Decision: fixtures model the
  real Host (decode = Lean `inspect outcome`; Rust decoder = twin; fallback = second shape). Shared cfg(test)
  `client_consent::codec_loop_arm(snippet)`; codec_test_lock now module-level pub(crate).
  Also: replan_retries_stale_root_and_lands flaked 11/12 on BOTH trees: workspace retained_stale_observation...
  replans without replan::TEST_LOCK -> now holds it. key_adoption 2 tests (+child) red on 764d6bb6 too: NOT H's,
  untouched. Gate row rc-codec-child (9 names) in scripts/check-rust-tests.sh. 10x each: codec_ 6, stale 15,
  fleet 20, provider_continuity:: 14, selected_publisher:: 4, all ok; row names --exact 9/9.
