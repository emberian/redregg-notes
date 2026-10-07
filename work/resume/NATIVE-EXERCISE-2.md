# NATIVE-EXERCISE-2 (a2d0ae1d713437691) -- resume note
Where it was: "Now apply the JRLANE D3/debt edits." Last reads: verify-once protocol change, escaped-constant list, hostraw call/repeat implementation. Mission: fixture build + refusal-lane debt (first native Objective acceptance).
Lane: burst-lane1 ember@162.43.189.7 /srv/lanes/native-exercise-2/src, branch lane/native-exercise-2 @8faabccc (base 5f9aa259), 7 unlanded commits (7bbb3ca2 assurance(native)! ... 8faabccc gates(native-transcripts)). 
WIP branch: lane/native-exercise-2-wip @15806e17 (native/resource-client/journey.d/jrefusal-lane.sh, journey.d/lib/hostraw.py: +72/-23 = the in-flight D3/debt edits).
Builds/gates read: logs/transcripts-green.log -> "native-transcripts: 10 triple(s), 0 failing ... PASS (verifier bf3604fb37be7ff9)"; logs/transcripts-RED-mutated.log -> "11 triple(s), 1 failing ... FAIL" = the planted mutant going red AS DESIGNED (not a defect); logs/ledger-3.log empty. build-logs/ untracked in tree (excluded from WIP).
Stale duplicates (older, 27c1b736): burst-e2e /srv/lanes/native-exercise-2 (same 2 modified files), persvati persvati ~/workbox/claude-lanes/native-exercise-2.
Main since pause: 53 landings since 5f9aa259 (lane is far behind); overlap Host/Main.lean, Kernel/DeclaredResourceController, NativeHostContext, ObjectiveBendNativeAdmission, ResourceObservationAdmission, ResourceTransaction, scripts/local-gates.sh.
Bundle: persvati:/home/ember/workbox/claude-lanes/bundles/native-exercise-2-lane1.bundle (prereq 5f9aa259; contains -wip).
Next step: finish the JRLANE D3/debt edits (checkout the wip branch state is already in the tree), then `git rebase github/main` (big, re-pin), rebuild fixtures with run-build.sh, rerun the journey; ledger said JROTL 7a8798e2 landable.

Written by FAIRY-RESUME 2026-10-04 ~18:40Z. main = github/main 66e3c5b5 (== burst-gate /srv/warm-base/src; umbrella green: /srv/warm-base/logs/green-66e3c5b5.log rc=0 18:21Z). Pause was ~18:00Z (usage wall). Boxes die 2026-10-05T15:55Z. Bundles are THIN (need prereq on main).

ROOT ADDENDUM (2026-10-05): the continuous journey runner shows JROT red on every tip back to 3b709c87: 3 of 30 checks fail.
The thief's signature is refused LOCALLY (rc=1, where the Host's noPossession is expected), and the second rotation stays at
epoch 2. This is very likely your D4 (the client blocks later rotations after one is refused at plan step) plus a client-side
pre-check that pre-empts the Host. JROT is yours; JOURNEY-REDS (Sonnet) owns J5 and J8. Evidence: work/journeys/<tip>.txt.

ROOT ADDENDUM 2: FAIRY-GREEN made JROT pass (lane/fairy-green, held) by adding `--new-attempt` for the second rotation and
expecting the possession refusal from signature-first admission. Check whether that is the RIGHT behaviour or a masked D4
(the client blocking later rotations after a refused plan step). Take what is right; the root has held that commit for you.

## VISIT (VISIT-C, 2026-10-04 ~20:05Z; main = d27d1cad)
- VERIFIED: lane1 /srv/lanes/native-exercise-2/src, lane/native-exercise-2@8faabccc (7 commits on 5f9aa259), and the
  uncommitted WIP (jrefusal-lane.sh, hostraw.py), byte-identical to lane/native-exercise-2-wip@15806e17. **None of the 7
  commits is on main** (checked by subject on d27d1cad). 62 landings since the base. Since 5f9aa259, main touched the lane's key files only in
  7dd88709 and 2a7c372b, and touched the fixture's import surface in a2454432, b663920a, 2a7c372b, bf28dd19 and 73dd077d.
- ⚑ JROT: main is red BECAUSE D4 is missing, not because of it. Main's jrot.sh passes the daily-key file itself (the
  client's NEXT≠daily pre-check, key_rotation.rs:421, refuses rc=1 before the Host). It also passes no `--new-attempt`, so the
  second rotation replays attempt `default` (rc=0, `"replayed": true`, epoch 2). Evidence: burst-e2e
  /srv/journeys/d69ab3f4…/rows/journey/step-JROT/jrot/{trot2,frot2}.*. D4's jrot.sh changes fix all three rows.
- PREPARED: rebased onto d27d1cad, **textually clean** (no conflicts). lane/native-exercise-2 = 1f34197e (D1 0eba5c66, D3
  d04fabf7, D4 aef58dcb, D5 ce04a12b, D6 5cad2e38, assurance b7c16a4e, gates 1f34197e), lane/native-exercise-2-wip = a1250c79.
  The same WIP diff is uncommitted in the tree again (verified identical). Old tips kept as `visit/ne2-pre-rebase`,
  `visit/ne2-wip-pre-rebase`.
- CHECKED (lane-check; logs ../logs/visit-lane-check{,-2,-3}.log; 24 min, 19 GB peak): 9659 of 9663 jobs build. Host/Main.lean
  elaborates green (rc=0). **RED: `Assurance.NativeAcceptedFixture` → `Lean exited with code 139` (SIGSEGV), deterministic (3 runs),
  also with `ulimit -s unlimited` and `--tstack=4000000`, so not a stack overflow.** It built pre-rebase (logs/g1, g2 rc=0).
  scripts/HypothesisLedger.lean and scripts/NativeTranscripts.lean import it, so they are unchecked.
  Likely lead (READ, not proved): a2454432 ("receiver re-runs the front end") and 73dd077d ("receivers type the replayed term")
  changed what the native admission re-executes. The fixture's captured bytes (Assurance/NativeAcceptedFixtureData, from a
  5f9aa259-era Host) now go through code that crashes the compiled evaluator under `native_decide`. That should refuse,
  not crash: find the declaration (bisect the theorems at lines 157-216), then regenerate the fixture
  (scripts/native-accepted-fixture/generate.sh) against a d27d1cad Host.
- VERDICT: **NEEDS-LANE** (the fixture SIGSEGV above). JROT does not need to wait for it.
- NEXT 1-2 h (burst-lane1; one slot at a time): (1) **queue D4 (aef58dcb) on its own first.** It touches only key_rotation.rs +
  jrot.sh and relies on the generic Receiver already on main (66967962). Build the client (sccache), run the JROT row against
  `fetch-artifacts green` + the new mini, then queue: this turns JROT green on every tip. (2) The fixture SIGSEGV: bisect,
  fix the cause, regenerate the fixture, then lane-check scripts/HypothesisLedger.lean + scripts/NativeTranscripts.lean. (3) Finish
  the JRLANE D3/debt WIP: the last two edit attempts in hostraw.py/jrefusal-lane.sh failed their asserts, so the WIP is
  partial. Then queue the rest.
- DEPENDENCIES: JOURNEY-REDS (J5/J8) shares journey.sh and the runner. Tell it D4 owns JROT so it does not "fix" jrot.sh too.
  MERGE-KEEPER: D4 standalone is a small range and can go into the next batch.
