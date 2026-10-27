# CX-HOST2 continuation (parked 2026-10-23 near the context ceiling)

## Landed
- d23091d (origin/main) `hosting:` HOSTING-43, fast judge GREEN tree af1248d597bf, pushed. Cross-layer (ROOT for LANG/PROTOCOL/KERNEL/LEDGER lines in the message).
  - (a) FollowRun's between-frames premise = `Reach` (closure of one `Command.step` on any frame), from Host/Follow.lean's loop; Honest is NOT carried: the package fact is proved of every step (Protocol/Proofs/FollowHead.lean `step_packageAt`).
  - (b) Hosting/Proofs/Lifetime.lean `shape_provenance`, `lifetime_bounds`, `seed_ok`.
  - (c) Hosting/Proofs/SocketStrong.lean `describe_shape` (+ describe guards in Protocol/Command/Machine.lean `describe`/`describeText`, Describe.lean `methodLine`/`noBreak`; resident `Shape.read` via `splitLines`/`methodWords`).
  - (d) SocketStrong `delivered_answer_committed_strong` (encodeData answerArgTy (answerDatum r t) = some args), premise StdioLeg only; tcb `stdio-leg` row restated (one follower, `LegFrom`).
  - Fixed on the way: adopt's genesis check at the step that adopts (`atGenesis`); `Lang.readPackage` refuses a non-ROM package cell.
- Plants measured: logs /tank/dregg-build/nanodregg/logs/host2/plant-P{1,2,3}.log (+ p2.py, p3.py), control b6.log.

## Open: (e) answered_row_is_kept_answer — cv task 01a167fe-5e84 (LANG)
Not provable without a Lang change (HOSTING-43 (e) names it exactly):
1. `activity_monitor_safe` over a loaded closure (root with imports/holes; `load_top`, `runLaw_ref_admits` at a root with imports).
2. Witness: the compiled Bell's `rung` guard is `activityWaiting` with the Bell's plans/resumer.
3. Run lemma for the Bell's `answer` method's edits (upsert rings … answered = some (ask text) …; retract pending …).
Then join with `delivered_answer_committed_strong`'s args equation.
Start by reading Lang/Proofs/StdActivityMonitor.lean (header + activity_program_safe), world/resident/Bell.ob, Lang/StdActivity*.lean (how `activity` compiles), Lang/Proofs/StdActivityTeeth.lean (`activity_fixture_monitored`).

## Validation debt (R-0069: paid at convergence)
- census / rows / benches / clippy at the next convergence (fast judge only).
- launcher/tests/resident_bell.rs (deployed resident against a real member) NOT run for this change: describe's guards and the resident's new splitter are claimed to read every honest description as before (INFERRED from the definitions, not measured end to end).
- Hosting.Proofs.Reply: built inside the fast judge's `Hosting` target (it passed); not built by me (OOM note).

## Machinery (hbox)
- worktree wt/host2 (now on d23091d), plant tree wt/host2-plant (at 1103509 + the change; plants restored), scratch /tank/dregg-build/nanodregg/scratch-host2 (topo.py = bounded level-by-level build: `swarm-build python3 topo.py ROOT MODS.txt 3 LOG`; lake has no -j and a 6G cap OOMs a whole-tree build).
