
## ResearchWip (FAIRY-FIX 2026-10-04 ~19:05Z, base d69ab3f4, log burst-gate:/srv/lanes/fairy-fix/logs/researchwip.log -> researchwip4.log)
Originally 7 failing modules (+3 downstream that surfaced after the first repairs: BoundedNockNetworkChecks, RoomReleaseLineage, RoomReleaseAdmission). FIXED forward in lane/fairy-fix ea4bb15a (queued): BoundedNockChecks, BoundedNockRefinement, BoundedNockNetworkChecks, RoomKeyReleaseAuthor, RoomReleaseIntent, RoomReleaseLineage, RoomReleaseAdmission, ResourceReserveBirthFixture.
STILL RED (2), not drift but absent seams, NOT dead (imported by JointBackendParty{Wire,Receiver,Recovery}; Rust native/private-backend/src/source_endpoint.rs and docs/PORTABLE-CONTINUATION.md name them):
- Kernel.JointBackendPartyAdmission: needs `NativeHost.Config.privatePartyEndpoint` (absent) and `TypedAuthorization.Verb.invokeObject` (absent; Verb has observe/mutate/delegate Object); also type mismatches at 197, 234, 269. Its Recovery/Receiver/Wire siblings fail behind it.
- Kernel.PortableHomeCurrentGuard: needs `NativeHost.Config.portableHomeControl` (absent; surfaces row says "source seam absent").
Decision for ember/owner: add the Config fields + Verb (a design change to NativeHost.Config and the Verb enum = flag day for config codec/pins) or retire the two chains. Case for deleting: both are status AUTHORED_UNCOMPILED/WIP in lean-build-surfaces, surface authored-research, only ResearchWip imports them; case against: live Rust consumer and docs reference them.
UPDATE 19:20Z: ROOT decided to delete the two red chains; done in lane/fairy-fix 358eb030 (queued). ResearchWip rc=0 on that lane; nothing remains red from this section.
# REDS (FAIRY-GREEN, 2026-10-04 ~19:00Z)

## 1. Host write path slows with record count: journey steps G, K4, KBW (OPEN, real, not fixed)
Evidence: CI run 37205421245 (36fca3ac), gate-logs/build-logs artifacts; burst-e2e table /srv/journeys/3b709c87*/rows/journey.
 STEP G FAIL 3362s "at 10: write 9.628s, reopen 6.102s; at 100: write 58.915s, reopen 30.023s" (1000-record thresholds: write<=5s, reopen<=60s)
 STEP J7 submit 31s (3s on a fresh store); K4 PASS but 2540s; KBW FAIL 1482s.
The CI gates job did not hang; it was cancelled at 4h still on KC. Fixed only the "can't go red" half: journey wall budget (commit 4de64aa7).
Open question for the morning: why does a write cost 9.6s at 10 records on the CI runner (burst-e2e: ~4s at record 4)? cv task, owner = whoever holds the Host write path / store.
 CI journey rows also stay red until this is cured: a budget cut run is red by design.

## 2. hypothesis-ledger: 1 failure (CI 37204226062 hyp-ledger FAIL 259s)
Same as the NativeBinding row owned by NATIVE-EXERCISE-2 (task 01a107f4); not touched.

## 3. Already cured on main (no action): build-closure (218f79d9), bun/capnp installs (79de0377: objective-c, objective-frontend 7/7, rust-tests spk-volume-custody, journey cargo spk-host all traced to missing bun/capnp on the runner; cv task 01a10714 cause = capnp missing for native/spk-rpc build.rs), objective-frontend examples STALE packets (fresh on 66e3c5b5: check-objective-examples.sh PASS 4/4 in lane).

## 4. Lost coverage (follow-up row): the Host refusing a signature from a never-enrolled key
J5's uread/usubmit are now stopped by the client's local consent ("local intent subject has no current signing key") before the Host. No journey step proves the Host itself refuses an unenrolled signer; needs a raw signed frame (not via mini). Likewise JROT's kernel noPossession is behind signature-first admission and only proved in Theory/KeyPreRotation.

## Hypothesis ledger RED on clean main 259a2fb0 (ROLLUP, 2026-10-05 ~00:00Z; NOT fixed in the rollup lane)
`scripts/check-hypothesis-ledger.sh` (AxiomCensusResearch built) fails with 6 TOOTHLESS assumption-tier families, none allowlisted and none with both a satisfying and a refuting instance. Measured on a fresh mk-lane at 259a2fb0 (burst-lane1 /srv/lanes/rollup-base/logs/ledger.log) and identical on the rollup tree (set difference empty), so none comes from the rollup range. native-exercise-2's unlanded Assurance/NativeAcceptedFixture (first_binding / refused_call_unbound) already gives NativeBinding both poles (their ledger-4.log reads it GREEN).
Introducing commit (`git log -S"<decl>"`, oldest):
- Minidregg.Kernel.GenericSimplexVAInvariant.LocalFaithful (15 consumers): 2ebce376 (2026-10-03, "Publish swarm source ... including WIP")
- Minidregg.Kernel.GenericSimplexLocal.AuditExtension (2 consumers; has a satisfying instance AuditExtension.refl, no refuting one): 2ebce376
- Minidregg.Kernel.GeneralSimplexReachability.LocalCommitOutputAttestations (2): 2ebce376
- Minidregg.Kernel.GenericSimplexLocal.ViewLock (1; satisfying instance default_locked, no refuting): first 58138c40 (2026-10-03, "Publish native controller, source fixture and consumer cohort (WIP)"), again 2ebce376
- Minidregg.Kernel.GeneralSimplexReachability.AuditRefinement (1): 2ebce376
- Minidregg.Assurance.PrivateEvaluatorCustodyJoin.NativeBinding (3): 6d23bacd (2026-10-03, "Retain exact native evaluator projections and successor custody generations")
The gate that reads them RED is eb4f683d (2026-10-04, "ledger: a refutation that covers a consumer reads VACUOUS; ...") on top of the ledger d9d86446; I did not bisect which main commit first turned the gate red (the families predate it, so the likely cause is the Assurance/Kernel census growing to include them). Fix (not here): name a satisfying AND a refuting instance per family (the FLOOR-TEETH pattern, 01bc8a3b), or delete the premise; do not allowlist.
