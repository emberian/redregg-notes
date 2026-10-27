# CONVERGENCE REPORT 2026-10-27 (second)

Tip: origin/main 8fe58cbf2115115... (8fe58cbf, "launcher tests: the broker's start window is read from the decider, and a hang is a minute with no CPU"). Range d280d23f218d..8fe58cbf2115, 83 landings (22 since the first report's tip 176110a7).
Run: hbox, fresh worktree ~/nd-land/converge2, `SWARM_MEM_MAX=24G scripts/converge` (floor 18.0G), PID file ~/nd-land/converge2.pid (wrapper loop script ~/nd-land/converge2.run.sh, log ~/nd-land/converge2.log). Full per-sha log /tank/dregg-build/nanodregg/main/.git/nanodregg-standing/8fe58cbf2115.log, record converge.out in the same directory.
Wall time: 80 min (total 4816 s: gates 24, build 1408, cargo 18, census 301, generated 17, runs 3042, waste 5). First report: 192 min.

## Load at the start (read this before any timing)
I started at 16:10:32Z when the 1-minute load first read 19.67 (the loop's gate was < 20). Ember's tighter gate (< 12) arrived AFTER the run had started; I did not restart it. So the start did NOT meet the < 12 bar. The load was 32 / 24 / 22 (1/5/15 min) at 13:13 box time, mid-run (build done, rows running), and 50 at 12:32 during the build.
Lanes building during the run (ps under nd-land / dregg-build at ~13:13, one snapshot taken mid-run; I did not capture one at the instant of start): fable-ctx4 (36 processes), glm-a (16), glm-f (8 lean), fable-trust (4 clang), agent5-tar (3 lean), plus the standing tree's own rows (grain-launch x6, hosting-drive, host follow/serve, nd-supervise, `cargo test` x4) and fixrust/fixrust-scratch leftovers (3 days old, idle). Raw: scratchpad lanes-mid.txt. Read every timing and every deadline red below as a loaded measurement.

## Verdict lines
STANDING 8fe58cbf2115 gates=RED build=ok census=RED generated=ok cargo=RED(cargo clippy) runs=RED(rows --deployed: RED(ROW forgotten FAIL plant Nanodregg.Protocol.Mutation.forgottenRefused: past its 300000 ms deadline)) waste=ok(pinned 83, unpinned 0) unmeasured=0 outside=39(traced) untraced=1 flakes=0 carried=0 daily=0 => RED
CONVERGENCE 8fe58cbf2115 range d280d23f218d..8fe58cbf2115 landings=83 => RED reds=4 fixed=2
FIXED run:cargo:launcher:broker, FIXED run:cargo:launcher:isolation (3.1 h after first red).
Note the converge.out also lists `RED run:rows` as an attribution line; the row verdict is `rows` ok, `rows --deployed` RED (below).

## Reds, attributed, with my read

### 1. census RED: 24 native_decide auxiliary axioms without allow rows  -- PERSISTS (first report red 1), the landing's defect
Output (CensusRun.lean:547): `AXIOM-CENSUS red (24):` the same 24 declarations as the first report (run_lazy_escrow, receipt_run, receipt_forged_free, run_agree, run_syncBlind, run_syncShared, run_fair_escrow, their _native.native_decide.ax_1_1 axioms, and consumers floor_receiptTruth, inhabited_receiptTruth, floor_agree_pageAbsorbs, floor_integrity_escrow, inhabited_escrow, floor_headsCompared_sync, inhabited_headsCompared_sync, floor_consent_cancelOk_record, floor_consent_okCommitted_kept, ...).
Introducing landing 87a1eb1c (Spec: receipts tell the truth ...). `git log origin/main -- gates/axioms-allow.tsv`: last edit is still 80791d05; NO allow-row landing from SPEC-4 exists in this range. Not closed. Read: the landing's defect; fix forward in SPEC (allow rows with reasons, or kernel proofs).

### 2. gates RED: size_limit: testground/kernel.wasm 4574759 bytes exceeds the 1048576-byte limit (CHARTER.md: no fixtures over 1 MB)  -- NEW, gate defect / environment
Output: `size_limit: testground/kernel.wasm: 4574759 bytes exceeds the 1048576-byte limit`. Only gate line red; paths, tcb, vectors, refusals, runs, waste ok.
The file is NOT tracked (`git ls-files testground | grep wasm` empty) and is ignored by testground/.gitignore:4; it is a build output sitting in the persistent standing tree (mtime 13:16, 4.75 MB now). gates/size_limit.py (GATES-20q, 71db9644 of 10-21) walks the disk instead of the tracked files, so a generated artifact reds the gate once the testground build has run in that tree. The gate was ok in the first report, so the wasm either did not yet exist in the standing tree then or the testground build landed since. Attribution tool lists (changed gates/tcb.tsv / tcb.py, a mis-attribution: those are `named by a red gate line` guesses: 4a3f9fb4, 62f98134, 5c0c20550, d422453a, a2b89265 ...); the nearest real owner is TESTGROUND (d422453a, the page that teaches the language, which builds the wasm) with GATES owning the walker.
Read: not a committed fixture; a GATES defect (check tracked files only, or exempt gitignored paths), possibly with TESTGROUND emitting into the tree.

### 3. cargo RED (clippy): too_many_arguments in launcher/tests/agent_hole.rs:443 (`fn h4(`, 8 of 7 args)  -- NEW, the landing's defect
Output: `error: this function has too many arguments (8/7) --> launcher/tests/agent_hole.rs:443:1 ... could not compile nanodregg-launcher (test "agent_hole") due to 1 previous error`; cargo stage exit 101.
Last toucher of launcher/tests/agent_hole.rs in the range: 2630ea32 (HOSTING, "the resident runs inside the open contextual calculus"); 37bfc852 and 2efa6a57 are neighbours in the same file family. Converge's attribution list (8fe58cbf ... 202f8f46, "changed the Rust workspace") is every Rust-touching landing; I read 2630ea32 as the introducer by `git log -S"fn h4("` (it names 2630ea32).
Read: the landing's defect (HOSTING). The lander ran its test but not clippy -D warnings on the test target.

### 4. runs RED: `rows --deployed`: ROW forgotten FAIL plant forgottenRefused: past its 300000 ms deadline  -- NEW, probably ENVIRONMENT (load), unconfirmed
Output: `ROW forgotten FAIL plant Nanodregg.Protocol.Mutation.forgottenRefused: past its 300000 ms deadline` (COST forgotten frames 35441 steps 3217), `FAIL 1 of 55`. Every other deployed row passed, including `refused` (34402 frames) next to it. The plain `rows` run is ok. (The other `forgottenRefused BLIND` line in the log is the harness-control, expected.)
This row was not red in the first report (there rows --deployed was UNREAD past 600 s and then passed in 645 s alone; the runner limit is now 1200 s but this is the plant's own 300 s deadline). The forgotten plant is the heaviest per-plant run of the deployed set (35k frames) and ran at load 30+ with 3 other tenants. Attribution tool: 571117332c2e LANG, f95ed6c4 GATES, 2efa6a57 HOSTING, 4a3f9fb4 PROTOCOL (Host.Follow in the reach) ... (all landings that touched the row's reach); the nearest are PROTOCOL 4a3f9fb4 (self-head compare in Host.Follow, adds work per follow step) and GATES f95ed6c4 (runner limit).
Read: I could not separate load from a real slowdown without a quiet re-run; I did not re-run (this report fixes nothing and the box is loaded). A plant-level 300 s deadline is the third wall-clock bound (after the 600/1200 s runner limit and the launcher's in-test 60 s) that reds under load. cv task asks PROTOCOL to time the plant alone on a quiet box and, if it is over ~150 s quiet, to treat it as a real cost regression from 4a3f9fb4.

## Rows that passed (ran 41; `ok` unless listed)
rows (non-deployed) and its harness control; adversary (3 runs); lang-journey (both runs incl. --hole-omitted-blocker-pin-admits); kernel-sim --seeds 64; ledger-sim 1; host-sim; host-file-sim; hosting-sim; script:gates/interp.py (kernel-sim 1,2; ledger-sim 1; hosting-sim 1); statement_plants.py; build_peak.py; cbytes.py vectors; tcb.py --plants; waste.py --plants; scripts/bar.sh (both); testground/build/gate.sh; standing:bench-worstcut-{births,retires,rows,writes}; standing:bench-worstworld; cargo launcher:{agent_hole? see 3, broker, isolation, resident, resident_bell, fence} and the other cargo rows. Stages ok: build (862 jobs, peak 8G of 24G), generated; waste ok (83 pinned, 0 unpinned, 0 absent): bench-worstcut-rows now ran (1301 s on a borrowed slot) so the waste measurements ARE taken this time, UNREAD count is 0, flakes 0.
(The several `FAIL harness-control` / `RED` lines inside the log are the deliberate known-red controls reading red.)
Slowest rows: rows 2125 s, bench-worstcut-rows 1301, resident_bell 1084, statement_plants 879, interp 779. At most 4 rows ran at once.

## DELTA against the first report (176110a7)
- CLOSED (2): run:cargo:launcher:broker and run:cargo:launcher:isolation. AGENT-5 / ROOT's 8fe58cbf (the broker's start window read from the decider, a hang is a minute with no CPU) landed and both passed in this loaded run (isolation 247 s, load 30+). They were the load-fragile reds; they held under comparable load.
- CLOSED: UNREAD rows. The 1200 s limit (f95ed6c4) holds: rows --deployed, resident_bell and bench-worstcut-rows (control read red, rows ran 1301 s) all produced verdicts; unread = 0.
- PERSISTS (1): census, the 24 native_decide facts of 87a1eb1c; SPEC-4's allow rows have NOT landed (axioms-allow.tsv untouched since 80791d05). Red for 2 convergences, 3.1 h.
- NEW (3): gates size_limit (untracked testground/kernel.wasm in the standing tree); cargo clippy too_many_arguments in agent_hole.rs `h4`; rows --deployed forgotten plant past 300 s.
- Still PASSING: launcher:fence, lang-journey.
Net: 3 reds -> 4 reds; 2 closed, 1 persists, 3 new (one of them probably load).

## cv tasks
Opened/noted (fix forward):
1. persists: note added to the existing SPEC census task (87a1eb1c, 24 native_decide aux axioms).
2. GATES: size_limit reds on gitignored testground/kernel.wasm (walks the disk, not git ls-files) since 8fe58cbf
3. HOSTING: clippy too_many_arguments in launcher/tests/agent_hole.rs h4 since 2630ea32
4. PROTOCOL: rows --deployed forgotten plant past its 300 s deadline since 8fe58cbf
