# Priority on return (root, 2026-10-05 fallow)
1. LIVE LAW BYPASS (cv 01a1087d-8a58): PayObservation and PayEnrol advance the clock cell WITHOUT judging its law, while
   ClockTick does judge it. Migrate both families onto Kernel.Receiving.Family (the Receiver now judges every written cell's
   law, LAWS-RECEIVER range df0cd116..90e4afbf queued), or make them judge the clock law now. Consultant: LAWS-RECEIVER
   (acc66e8ba22e15229) and SCHOLAR-LAWS (a675587c3c9fe2411).
2. Statement-snapshot gate blind to vacuous premises in Mathlib-importing modules (W42, cv 01a1089a-1168): P0.
3. ForcingTransparent: segment lift (wip 8633f2ef), then the kernel premise swap.
4. DEPLOY-3B gate on cand3 (best candidate) FAILS; ship-blocking rows and owners:
   - G growth: write median 7.7 s at 10 records, 49 s at 100 (target <=5 s at 1000) -> SCHEMA-V2-2 (client history re-check).
   - J12X (new): malformed requests through the client end "request status uncertain" instead of the Host's named refusal;
     describe with a payload gets 254 not 255 -> client transport (bc3a581b) / host grammar (4c5c58a3); unowned: assign.
   - J5/J8: client refuses before the Host -> JOURNEY-REDS (Host refusal must still be proven).
   - documents (NEW, ship-blocking): protected-doc SHARE row 16 refused by the Host: `$.purpose.draft.command.targets[0].payload.actions[2].before: invalid exact annotation guard` (client request vs Host grammar disagree); log burst-e2e:/home/ember/d3b/cand3/gate/g3/composed/state/documents-protected/protected/log/16.err. Unowned: assign.
   - residents/apps/connector: no bindings on scratch worlds (SPK/residents lanes).
   Split tenancy ran for the first time: install/ship/verify 0 FAIL; S2/S3/S8 fixed in 2aca1f8c (confirm on cand4); cand4 building.

- JOURNEY-REDS note: JROT is fixed by NATIVE-EXERCISE-2's D4 (8f987600, queued first; JROT 31/31 on burst-e2e). JOURNEY-REDS owns only J5/J8/Rooms (+ the new J12X if unassigned).

5. REVIEW A WIDENED CHECK (retention-payers WIP 63ab055a): PhysicalPostLaw now admits the registry's retired image at protected
   coordinates (ids >= 2^256). Acceptable only together with CHECKPOINT-INVARIANT's protectedWrite gate (nothing but the activity
   kernel writes protected coordinates); land them in that order, and require a theorem tying the two before RP's WIP lands.
6. ROOT DECISION (SCHEMA-V2-2 Q2, Store open at 3000 records = 2.1 s): verify old records AT USE, but only through an
   authenticated structure, so no check is weakened: every read of a history record verifies its inclusion against the
   MAC'd, anchor-bound root (Merkle/accumulator over the log), with a THEOREM that no read path returns unverified bytes;
   a tampered record is refused by name at use; `mini store audit` runs the full genesis re-check on demand and in the
   journey gate. The spent-nullifier set moves to an incremental authenticated set (not re-serialized whole into each
   checkpoint). Take the byte-level decode/hash speedups too (a constant factor, no check moves). Plain "lazy, unauthenticated"
   is rejected.

7. W04-SPK-V4-LAND BOUNCED in c14: 5 Lean logic hunks in Kernel/NativeHostReplay.lean (main now proves the final image via genesisWalk_image; W04 threads `retry` through the old runtime-compare shape). Diff: burst-lane1:/srv/lanes/W04-SPK-V4-LAND/BOUNCE-c14-NativeHostReplay.diff. Re-dispatch (opus) to restate W04 over the genesisWalk_image shape.

## Morning 10-05 update (root)
- #1 law bypass: CLOSED differently (pay families judge the clock write through ReceivingLaw.judgeWrite; teeth shown; re-genesis).
  Root decision: YES, migrate pay families onto Kernel.Receiving.Family as the next lane, starting with its two blockers
  (Family.prepare needs the checked signature for capability authorization; birthParent for account-cell creation), design in
  cv 01a109bd-8682. One judgement path, not two.
- #2 W42 blind snapshot gate: FIXED (two-env snapshot; 3 unused-premise theorems filed cv 01a109c1-2828).
- Keeper KEEPER-NIGHT (a4a30a3f184d5d010) is at ~588K: the next keeper is a fresh agent from MERGE-QUEUE LOG + its digest.
