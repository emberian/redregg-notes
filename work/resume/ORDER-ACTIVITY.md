# ORDER-ACTIVITY (VISIT-A, 2026-10-04 ~19:40Z; main = green = next = 9a743f41)
Verdicts: READY 3 (FORCING-TRANSPARENT, UPGRADE, CHECKPOINT-INVARIANT*), NEEDS-LANE 2 (RETENTION-PAYERS, SEATS-NATIVE). SUPERSEDED: the old branch commits of UPGRADE (both on main) and CHECKPOINT-INVARIANT (copies + the bounced c9bb411e). *CHECKPOINT-INVARIANT's turn-wrap is BLOCKED-ON RETENTION-PAYERS.
Every lane has a fresh warm clone of main at burst-gate:/srv/lanes/<lane>-v/src. Its old tip is kept as lane/<lane>-old. Old lane dirs are untouched (retention-payers is still mid-rebase there: adopt -v, then abort the old one).
The running neighbour is ACTIVITY-ROUTE (burst-lane1, cf06c9b7, queueing in ~1-2 h). It owns the receiver Turn/Decided, Kernel/ObjectiveKernelConfig and NativeHost ops 210-214.

## Wave 1: now, all on burst-gate (2 slots; one build each at a time)
1. FORCING-TRANSPARENT: the counterexample is QUEUED (d27d1cad..11b10a52). The simulation module is a new Theory file, so it conflicts with no peer. Send it "approved: LexicalInvariant yielded".
2. RETENTION-PAYERS: fix Kernel/JobMoney.lean:193 (Batch third field) and build the dependents, then queue book!. Its ObjectiveActivity retire/deregister range is the base that UPGRADE and CHECKPOINT-INVARIANT build on, so it goes first. Rebase onto ACTIVITY-ROUTE when that lands.
3. UPGRADE, module half only: repair Kernel/ObjectStateType.lean (red from :310 typedAt_takeField; the codec half is fine). It is a new file and blocks no one. Hold the kernel-turn edits.

## Wave 2: after ACTIVITY-ROUTE lands (~1-2 h)
4. SEATS-NATIVE: rebase onto main + route. There is an add/add on Kernel/ObjectiveKernelConfig (take the route's), the NativeHost/consent/TurnCensus/Host op tables, and the one logic hunk (Instantiated on main's replayPackage loadProgram). Its E8 activity END needs the route. Run e2e on burst-e2e BEFORE its deletion 2026-10-05T15:55Z.
5. CHECKPOINT-INVARIANT: start ObjectiveActivityGate + ordinaryGate/protectedWrite on the route. The Turn/admitTurn token goes under the route's Decided, and the CheckpointTyped induction goes AFTER RETENTION-PAYERS's range (retired cells carry no payload). The ResumeContract part goes on fairy-fix.

## Wave 3
6. UPGRADE, kernel half: ObjectRecord v2 (stateType/live/phase), retain/release beside RETENTION-PAYERS's retired image, adopt/migrate/abortDrained as arms of CHECKPOINT-INVARIANT's token and the route's Decided. It lands last because it extends all three.

Shared-file hot spots: Kernel/ObjectiveActivity.lean (RP, CI, UPGRADE, route, seats), Kernel/ObjectiveResumeContract.lean (FT, CI, fairy-fix, route), Config fields (RP storageRate, seats/route configOf). Whoever lands second adds the field. Pins: take main's and regenerate.
Notes per lane: resume/<LANE>.md "## VISIT".
