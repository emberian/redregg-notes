# FIX-RUST report (nanodregg client/ launcher/ devtools/ Emit/; cards A6, A19, A18, A17)

Lane: FIX-RUST under R-0069 / R-0071. Worktrees: hbox `/tank/dregg-build/nanodregg/wt/fixrust` (build + land),
local `~/dev/nanodregg-wt/fixrust` (edit). Own CARGO_TARGET_DIR `/tank/dregg-build/nanodregg/wt/fixrust-scratch/target`.
Tags: READ (path:line), MEASURED (a command I ran), INFERRED.

2026-10-24 05:32 START at origin/main f9657bd. Read COLLATION §A6/A17/A18/A19, READ-RUST whole, READ-CODEC D-2.

## Card 1 · A6 · CLIENT-37 — LANDED a7bccd8 (pushed to origin)
- 05:50 MEASURED (client/tests/real.rs, real host serve/follow): write whose submit reply + lookup are lost ends
  `uncertain`; same argv again; with the reload skipped the height moves by TWO (`left: 10, right: 9`). With the
  continuation: +1, one attempt frozen for the two runs. Scripted plants (run.rs) RED under the same mutation.
- Design: attempt dir freezes `argv` (generated Command encoding) + `cont` (follow's continuation at submit) beside
  `call` (written last). `run` starts with `Attempt::open_for`; an open attempt of these argv bytes is driven from its
  files and follow is RESUMED with its own `cont` + end (Lean's `settled` decides the end on follow's World). Lean
  `start` taking the open call was considered and refused (frame carries argv twice = A3; `out` needs the plan's Turn).
- FLAG DAY: attempt layout; an older `call` without argv/cont refuses to load; empty attempts/ after landing.
- SIZE: client library ceiling 2528 -> 2678 (gates/ceilings.tsv, cross-layer line in the commit). ASK-worthy only if
  ROOT wants ceilings ruled per card; I raised it by exactly the measured lines.
- NOT closed: settled-but-unreported retry (F23) -> cv 01a16d4c-4294.
- Fast judge GREEN (built: none; cargo check client/attach/launcher; fmt). Clippy client --all-targets clean (MEASURED).

## Card 2 · A19 · CLIENT-38 — in the FULL landing queue (gates/*.py changed)
- 06:00 MEASURED: the old runner's `subprocess.run(timeout)` leaves a grandchild alive; `run_group` kills the group.
- `nanodregg_sandbox::die_with_parent()` (PR_SET_PDEATHSIG=SIGTERM via rustix + getppid compare; macOS getppid
  watch) first in nd-supervise, nd-members, keybroker, grain-launch. Failure = named exit parentDeath (keybroker
  149, nd-members 162, grain-launch 63; Lean BrokerExit/LaunchExit, code theorems re-decided; units re-rendered).
- gates/runs.py `run_group` (own process group, killpg past DEADLINE); readset.py strace `--kill-on-exit`.
- SECOND DEFECT, found by the real-tree plant (MEASURED, fixrust-scratch/pd/epipe.py): nd-supervise with no stderr
  reader IGNORES SIGTERM in effect: its SIGTERM thread's `eprintln!` panics on EPIPE before `kill()`. Every
  supervisor under a dead nd-members has that stderr. Fixed: `nanodregg_sandbox::say`/`say_line` (one write,
  never a panic) replace eprintln! in nd-supervise, the mux, nd.
- Plants (plants2.log): devtools/tests/orphan.rs (sh parent SIGKILLed; dead-stderr SIGTERM), launcher/tests/
  members.rs a_killed_test_process_leaves_no_supervisor_behind (a SIGKILLed child test process holding World +
  nd-members + keybroker + grain-launch, 24+ processes; nothing survives 15 s). RED under: no link in
  nd-supervise / nd-members / keybroker / grain-launch (exactly that binary's subtree survives), eprintln! back.
- The 328 already-leaked processes: untouched (no PID file names them); Ember's to stop (cv 01a16b44 (a)).
- A measurement I discarded: one run read "thread-spawned children survive"; it ran a STALE planted binary
  (rsync -a restored an older mtime, cargo did not rebuild). Re-measured with a fresh binary: they die.

## Card 3 · A18 · CLIENT-39 — built and planted in wt/fixrust3; lands after card 2 (shared files)
- One `frame::Deadline` (poll per call, PIPE_BUF writes) for sockets.rs (one deadline per request+reply), the mux
  (frame deadline, reply writes), keybroker's upstream (connect to last byte), decider pipes.
- `Hosting.Broker.Bounds.answerMsMax` (120 s) named in Lean, emitted ANSWER_MS_MAX; `residents::Decider` (one
  shape for keybroker and nd-members): a late or undecodable answer = LOST for good, then deciderLost by name.
- `fsx::create_once`: `.NAME.tmp` + fsync + hard link (refuses an existing name) + dir sync; residue passed over.
- Plants: trickling Host (P3a per-read → HANG), silent/half-frame decider (P3c no deadline → HANG), SIGKILLed
  freeze x20 (P3b in-place → short calls, 3/3 runs), crash residue in custody. Regression: client sockets/
  custody/attempt/run/mux/frame, launcher broker (13) + members (12) green in wt/fixrust3; clippy clean.

## Card 4 · A17 — NOT STARTED (parked at the token budget). Design decided:
/Users/ember/dev/redregg/work/codex/FIX-RUST.continuation.md

## 07:40 Card 1 REGRESSION found and fixed (CLIENT-37 amended), commit in flight
- MEASURED in card 2's full judge on main 7332f9c: THE BAR standing RED `friend1 nd write exit 1: refused stale`
  (the judge marked it PRE-EXISTING: a7bccd8's). Cause: the continuation re-ran a `declined stale` write by
  continuing the dead call, and follow settled it refused. Fix: resume follow with the refused end first (step 4
  checks it on its own World), then on follow's `refused` plan afresh. THE BAR standing PASS with it (bar1.log,
  stale 1/1/0), RED without it (bar2.log, the judge's exact line); run.rs a_rerun_whose_open_attempt_is_dead_plans_afresh.
- Lander: hbox wt/fixrust1b, pid file fixrust-scratch/commit1b.pid, log commit1b.log (FAST). Ceiling 2678 -> 2691.

## 08:15 State at hand-off
- main 37772b9 (not mine). Card 2 lander (FULL; pid commit2.pid, log commit2.log) displaced once and re-judging,
  head of the queue. Card 1b lander running. Both land and push unattended; read their logs for the hashes.
- Card 3 lands after card 2 (FIX-RUST.continuation.md, steps 1-4); NOTE fix1b also touches client/src/run.rs,
  table.rs and client/tests/run.rs, which card 3 does not.
- Ember 10-24 (relayed): plants are vacuity checks run when cheap, never a landing gate. Nothing pending waits on one.

# FIX-RUST-2 (successor; same tags READ/MEASURED/INFERRED)

## 08:20 START at origin/main 7655145
- READ: continuation + report whole. MEASURED (hbox): card 2 lander (pid 1527528, ticket 223, head of queue) and
  card 1b lander (pid 2198972) both alive, both sleeping in nanodregg-slot-wait for a gate slot (4 slots busy).
- Card 4 developed beside them in a fresh pair: local ~/dev/nanodregg-wt/fixrust4, hbox wt/fixrust4 (both from
  7655145; sync = scratchpad/fixrust/sync4.sh, checksum/no-times), own target fixrust-scratch/target4. Local WIP
  commit only (never pushed), to be rebased onto main after cards 2/3 land.

## 09:05 Card 1b LANDED 37fda4b (CLIENT-37 amended); hbox main / origin divergence repaired
- MEASURED: 1b landed on hbox main by CAS (37fda4b, over kernel's 7c85768), but its push was REJECTED: origin
  held 7655145 (the charter test clause, pushed to GitHub directly), which hbox main lacked. So every landing
  since 7c85768 had failed to push (7c85768 too).
- Repair: a merge commit d741f5a = merge(37fda4b, origin/main 7655145). The tree came from `git merge-tree`
  without conflict (CHARTER.md only). It was moved in by `update-ref main d741f5a 37fda4b` (CAS), pushed to
  origin (fast-forward), and the primary checkout was moved to it. A merge, not a rebase, so the landed hashes
  7c85768 / 37fda4b that other reports cite stay true.

## 09:40 Card 4 built and tested, integrated over cards 2+3 (not landed: it waits for 2 and 3)
- Preview: scratchpad/wt4p = 7655145 + WIP(cards 2+3, local fixrust 1bd91a9) + WIP(card 4). Two conflicts
  (Emit/Broker.lean bounds list and doc, frame.rs module doc), resolved by scratchpad/fixrust/resolve4.py.
  Synced to hbox wt/fixrust4.
- MEASURED (hbox wt/fixrust4, own target4): `lake build` of the emitters, host, hosting-* and the touched proof
  modules (Protocol.Proofs.Frames, Ops.Proofs.Units, Hosting.Proofs.Plan) is green. Re-emits: generated.rs,
  launcher generated.rs, broker_generated.rs and units (EXITS.md is card 3's text; every other unit is
  byte-identical). codec-vectors --check: ok (288 vectors, 59 sites). Workspace clippy --all-targets -D
  warnings: clean.
- MEASURED tests (filtered): client vectors 4, frame 4, mux 9, sockets 2, custody 11, attempt 13, run 20,
  stdio 1, foreign 1; launcher broker 13, members 12 (+ the kill plant), all green. One false red is
  discarded: members' kill plant failed only because hosting-controller was not built in this tree.
- MEASURED plant: child_parts reading the conn id big-endian makes `vectors` RED (wire/child 0: re-encoded).
- MEASURED: foreign X1b's refusal is `keyTaken`. The comment's claimed check is now made: at the advanced head,
  a later receipt of the same call is `keyTaken`, not `headMismatch`. Green.
10:26 card 1b LANDED 37fda4b (on origin/main). Card 2 refused on a decisions/client.md conflict with 1b; client.md rebuilt (main + CLIENT-29 fix + CLIENT-38), relaunched FULL (commit2.pid/log). Card 3's local decisions/client.md must be rebuilt the same way (main's + CLIENT-39) before it lands.

## 10:30 Card 2 lander REFUSED by a decisions/client.md conflict (1b's amendment); re-based and relaunched
- MEASURED: commit2 try 1 (log commit2.try1.log) ended `REFUSED — merge conflict in decisions/client.md`.
  Card 1b's amended CLIENT-37 text and card 2's appended CLIENT-38 overlapped, so nothing landed.
- In hbox wt/fixrust: the card 2 files were committed locally, rebased onto main 0a299c8, the hunk resolved
  (CLIENT-38 appended after the amended CLIENT-37), then reset --soft so the worktree holds card 2 detached at
  main. The same message and file list are relaunched: pid file commit2.pid (3534935), log commit2.log.

## Card 2 LANDED 1ab410e (CLIENT-38), pushed
- Try 2 RED: decls `undeclared redefinition` for the three exit tables (12 constants; a stricter decls gate
  was now on main). The fence/workspace "failures" in that log are the nobin-RED controls. Fix: twelve
  `RESTATES-MEANING: Nanodregg.Hosting.{Keybroker,Launch,Members}Exit[.all|.cls|.code]` lines. Try 3: GREEN
  (FULL), head after 2 displacements, landed by CAS, pushed.

## Card 3 LANDED 2d5056e (CLIENT-39), pushed
- Local WIP rebased onto 1ab410e (one conflict, launcher/tests/common/mod.rs socket letters: both kept),
  applied to wt/fixrust, emit-broker/emit-units re-emitted (ANSWER_MS_MAX, EXITS.md deciderLost text).
- Refusals on the way, each cheap. Try 1: owners, because gates/ceilings.tsv is GATES' (now `ROOT for GATES`
  in --cross-layer). Try 2: the client library was 2742 > 2741, because `cargo fmt` (card 3 had not been
  formatted) added a line. Ceiling 2691 -> 2742 = MEASURED. FAST judge GREEN; landed by CAS.

## Card 4 (A17, CLIENT-40): lander running in hbox wt/fixrust (pid file commit4.pid, log commit4.log, msg4.txt)
- Rebased onto 2d5056e cleanly. Re-checked on main+3+4 (hbox wt/fixrust4): emits, codec-vectors check, clippy,
  fmt, filtered tests (see 09:40), all green.
- A source gate caught one design error before landing (MEASURED, gates/check.py): closure C10, nothing may
  import Ops. Emit.Broker imported Ops.Units for the restart policy. Fix: the policy (restartSeconds,
  startBurst, startIntervalSeconds) moves to Hosting (Hosting/BrokerExit.lean, beside the restart classes).
  Ops.Units renders Hosting's, and the units stay byte-identical (emit-units --check). Ops' own copies are
  deleted.
- Ceilings, MEASURED against main: client library 2742 -> 2811 (+69), nd-members 690 -> 701 (+11, rustfmt's
  import blocks). Every risen row has a SIZE line (checked by script).

## Card 4 LANDED 3794975 (CLIENT-40, `client!:`), pushed to origin
- Try 1 (FULL) RED on decls only (runs: ok, 81 runs of 36 exes; the listed cargo "failures" are the nobin-RED
  controls). The change named the socket names and moved the restart policy, so seven declaration lines
  were added: RESTATES-MEANING for Hosting.followSock, Ops.Units.membersUnit / writer /
  sync_loop_under_start_limit, and DELETES for Ops.Units.restartSeconds / startBurst / startIntervalSeconds.
  Try 2 FULL GREEN, landed by CAS (displaced 0 times), pushed.
- What CLIENT-40 leaves open (its Critique):
  - frame.rs and mux.rs are still hand-written. Their widths, bounds and every vector row's verdict are
    Lean's; their code is not.
  - Emit/Rust.lean's frameIo template (launcher/broker framing, literal 4 and `as u32`) is the next vector site.
  - SameRecord's `keys` file (2–3 seeds) is still a Rust-only layout.
  - resident_bell's PATIENCE is a hand copy of Lang.Bell.patience. There is no batch-write verb, so its
    2048 sequential writes stay (LANG's call).
  - Tests that state a deployed layout keep their literals on purpose.
- Flag day: ws/rotation is 80 bytes. A 72-byte one refuses `Length`.

## State at close (FIX-RUST-2)
- origin/main = 3794975. Cards 1b, 2, 3 and 4 have all landed: 37fda4b, 1ab410e, 2d5056e, 3794975 (+ the
  d741f5a merge that let pushes through).
- No lander of mine is running. Trees: hbox wt/fixrust (at main after landing), wt/fixrust4 (test tree);
  local ~/dev/nanodregg-wt/fixrust and fixrust4 hold local-only WIP commits (superseded by the landings).
