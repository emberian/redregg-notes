# HYP-INSTANCES log (continuation file) — started 2026-10-14
Lane: HYP-INSTANCES (Claude). Base next 0125b224. Lane tree hbox:/tank/dregg-build/claude-lanes/hyp-instances/src
(git clone of bundles/burst3-minidregg.git, branch lane/hyp-instances; .lake/packages cp -al from warm-7dea0626,
.lake/build a PRIVATE cp -a of pipeline/lanes/integrator-next/src/.lake/build @df93b368 — no shared build inodes).
Push: mirror refs/heads/lane/hyp-instances; GitHub via ROOT.

## events
- 16:40 read FOLLIES §F3; allowlist scripts/hypothesis-ledger-allow.txt = 76 entries (69 + 7 kern train).
  Gate already reds an unlisted TOOTHLESS assumption and a stale entry; what is missing is "never grow".
- 17:20 RATCHET written (uncommitted): scripts/check-hypothesis-ledger.sh compares the allowlist's family set with
  `git show $HYP_LEDGER_BASE:scripts/hypothesis-ledger-allow.txt` (default HEAD; merge-gate-checks passes FROM);
  any added family -> "RED: allowlist GREW: <family>". Exercised the block once on three lists: real (PASS 75/75),
  +1 planted family (RED by name), -1 (PASS 74/75).
- batch 1 (16 families, poles written next to each hypothesis, allowlist 75 -> 59): ValidRadix, AuthMap.PrefixFree,
  AuthMap.WF, CrossVatSound, IsFoldHom, CodesBounded, BindingGate, PublicOnly, FrameCodec.RoundTrips,
  PrefixDiscipline, SignatureCompletion, SshsigRefinement, DurableDataIntent/DurableCommitProtocol
  .ImplementationRefinement, ExactReceiptCoinRealization, ExactRootAttribution. Scratch-tested
  (lane/../Scratch1.lean) then inserted. Build 1: all green except Compiler.DurableIndex SIGTERM (143) at 491 s
  under box load (not mine); rebuilding.
- scratch-verified for batch 2: Selvage.PrefixMeasurable (42 consumers) ref = a prover peeking at its own round's
  challenge; MultiAffine ref = x0^2 over ZMod 3.
- Iteration trick: `lake env lean ../ScratchN.lean` against the built oleans (no build) to test poles before
  editing low modules (Theory/Bignum edit rebuilds ~1/3 of the tree).
- 18:30 batch 2 written (scratch-verified unless noted), allowlist now 48: Selvage.PrefixMeasurable, MultiAffine,
  WorkPrefixMeasurable, QueryAgreementAmplifies, IdealFreshAt, FreshIdealExecution; LineageValid (unverified),
  NativeIORefinement (unverified), ObjectiveTurnTotalityStorage.PostShape (unverified);
  CellState.PairBindingPremise poles + DELETED Example.RootPairBinding (the pair's roots differ by native_decide:
  rotated_root_ne / policy_rotated_rootOf_ne, #assert_compiled; three consumers drop the premise —
  objective-manifest rows restated/removed need ledger admission at the gate).
- Waiting on a Lean slot since 17:25 (3 slots held by TokenCensus, codec-shapes lb.sh, a DurableEngine build).
- Decided: Selvage ROM/PCS/crypto premises (Poseidon2PermutationIdeal, PaddedRpRfSwitch, PaddedLazy*, MsisHardEx,
  WHIRConjecture412, Haboeck*) get NO degenerate teeth (e.g. gap := -1): a tooth at a parameter the premise is never
  used at is the gate gamed. They stay allowlisted under task 01a0f802-02f0 with that note.
- ROOT exemption: stopped slot waiter by PID file (child 1102134 killed by ROOT); THREADS=1 nice 19 swarm-build.
  Selvage.lean umbrella took 7052 s under IO pressure. One red fixed: #guard_msgs axiom pin -> #assert_compiled.
  Build 9807 jobs green. Real ledger (--no-self-test): PASS, 48 ALLOWED, ratchet PASS (48 now; 75 at HEAD).
  Plant (new instance-less hypothesis) -> "RED: Minidregg.Scratch.NewPremise is TOOTHLESS" (observed once).
- COMMITTED 4eb31587 (ratchet) + 357273ab (26 families poled + RootPairBinding deleted; 75 -> 48), pushed
  mirror lane/hyp-instances. GitHub via ROOT. OPEN: objective-contract ledger admission for RootPairBinding removal
  + 3 restated rows; build-surfaces re-pin for 22 modules.
- NEXT for a successor: Agree (Payload ⟨.state,[],[]⟩, cell ⟨reservedBase⟩), PostImage, PagePairBinding,
  HistoryBcsBad, SourceShape — all tractable with toy instances; SameAuthorization/WStep need a closed Verdict.
