# PROOF-SHAPE CENSUS of the Mini tree at cfdaf64d

Generated 2026-10-07 by BURN-CENSUS on burst2-a (lane /srv/lanes/census-a). Script: `/srv/lanes/census-a/src/scratch/Census.lean` (copy: /Users/ember/dev/redregg/work/burn/Census.lean), run as `lake env lean scratch/Census.lean` importing Minidregg, Assurance, Host, Selvage, Verify, SimplexQualification, ObjectiveProofs, Deployed, AxiomCensus, AxiomCensusResearch, TokenCensus. Raw TSV: `/Users/ember/dev/redregg/work/burn/PROOF-SHAPE-CENSUS.tsv` (one row per theorem: name, module, top dir, bucket, reason, nData, nProp, nInst, innerQ, proof-flags, type depth).

## Answer in one paragraph

23006 theorems (user-written, `thmInfo`, module in the repo, auto-generated aux lemmas excluded). By statement shape: **18103 (78.7%) per-function**, **3842 (16.7%) closed-instance** (fixed application to literal/near-constant parameters), only **335 (1.5%) reachable-invariant** (whole-trace / reachability statements), 472 (2.1%) refinement/simulation, 212 generic library lemmas, and **42 (0.18%) temporal/liveness**, none of which is a proved liveness property over infinite executions (see list). So: statements about whole trees/traces of computation are about 1.5% (reachable) plus the refinement 2% that relate machines; most proofs are universally quantified lemmas about one function or structure, and about one in six is a check of a fixed example. Caveat: "per-function" is a wide bucket (it includes structure-field projections and lemmas whose hypotheses are themselves a proof-carrying structure, which carry the real generality); see the rules and the precision numbers.

## Classifier rules (first match wins), as implemented

Statement = the theorem's type. `forallTelescope` strips all binders; each binder is classified as instance-implicit (nInst), Prop-valued hypothesis (nProp) or data (nData: any binder whose type is not a Prop, explicit or implicit, including types, structures and states). `innerQ` counts inner `∀` over non-Prop domains and `∃` anywhere in the body. "Repo constant" = a constant declared in a repo module (not Lean/Mathlib/Batteries). `isPropFam c` = c's type ends in `Prop` (a predicate family, so enums like `Liveness` do not count). Excluded as generated: internal names, `match_`, `proof_`, `injEq`, `inj`, `sizeOf_spec`, `eq_N`, `eq_def`, `ext_iff`, `noConfusion*`, `congr_simp`.

1. **TEMPORAL** if (a) the last name component contains one of eventually, liveness, eventual, fairness, coind, terminates, `_halts`, `halts_`, productive; or (b) the statement mentions a constant named Eventually, Terminates, Terminating, Halts, Fair, Fairness, Stream, Colist, LazyList, WellFounded, Acc; or (c) it mentions a predicate family whose name contains eventually/terminates/liveness; or (d) it contains `∃ n` over Nat where the bound variable is named n/k/m/fuel/steps/ticks/t/N/budget AND the statement mentions a Step/Steps/Run/Exec/Star/Iterate/fuel/steps constant.
2. **REFINEMENT** if the last name component contains simulat, refine, refin, agrees, agree_, _agree, correspond, bisim, equivalen, differential, conform, faithful, adequa (not "agreement", which is coding theory); or the statement mentions a constant containing simulat/refines/refinement/agree/bisim/correspond (not "agreement"); or the body is an `Eq`/`Iff` whose two sides are headed by two different repo constants both named like evaluators (eval, exec, run, interp, denot, sem, check, verify, apply, decode) ("two-evaluators").
3. **REACHABLE-INVARIANT** if the statement mentions a constant named Reachable/reachab*/ReflTransGen/TransGen/StepStar, or a predicate family named exactly Step/Steps/Run/Exec/Star, or (outside Compiler/ and Selvage/) a constant containing "trace" (weak-const); or the name contains "reachable".
4. **CLOSED-INSTANCE** if nData = 0 and innerQ = 0 and the statement is not headed by a quantifier-in-disguise (Function.Injective, Surjective, Bijective, Set.InjOn, Monotone, Antitone, ...). Prop hypotheses are allowed (they are conditions on a fixed instance). Side column `proof` flags the proof term: `native` (uses `Lean.ofReduceBool`/native_decide aux), `decide`, `rfl`.
5. **OTHER** if the statement mentions no repo constant at all (generic Lean/Mathlib-style lemma proved inside the repo).
6. **PER-FUNCTION** otherwise (universal over data, about repo functions, with none of the markers above).

Known blind spots: name-pattern rules can misfire (see the sample); "ObjectiveProofs", "Verify", "Deployed", "AxiomCensus*", "TokenCensus", "SimplexQualification" have no theorems of their own (they re-export Theory/Kernel modules), so the per-directory table has no rows for them; the `#guard` facts (about 4388 occurrences in source) are NOT theorems and are not counted here at all. Proofs by `native_decide` are detected through their `_native` auxiliary lemma; the flags column is a heuristic only.

## Counts, overall

| group | total | CLOSED-INSTANCE | PER-FUNCTION | REACHABLE-INVARIANT | REFINEMENT | TEMPORAL | OTHER |
|---|---|---|---|---|---|---|---|
| ALL | 23006 | 3842 (16.7%) | 18103 (78.7%) | 335 (1.5%) | 472 (2.1%) | 42 (0.2%) | 212 (0.9%) |


## Counts per top-level directory

| group | total | CLOSED-INSTANCE | PER-FUNCTION | REACHABLE-INVARIANT | REFINEMENT | TEMPORAL | OTHER |
|---|---|---|---|---|---|---|---|
| Kernel | 8456 | 987 (11.7%) | 7135 (84.4%) | 158 (1.9%) | 132 (1.6%) | 9 (0.1%) | 35 (0.4%) |
| Theory | 4606 | 840 (18.2%) | 3356 (72.9%) | 138 (3.0%) | 162 (3.5%) | 28 (0.6%) | 82 (1.8%) |
| Compiler | 3629 | 630 (17.4%) | 2913 (80.3%) | 0 (0.0%) | 61 (1.7%) | 1 (0.0%) | 24 (0.7%) |
| Assurance | 2956 | 876 (29.6%) | 1990 (67.3%) | 39 (1.3%) | 42 (1.4%) | 4 (0.1%) | 5 (0.2%) |
| Selvage | 2949 | 420 (14.2%) | 2402 (81.5%) | 0 (0.0%) | 65 (2.2%) | 0 (0.0%) | 62 (2.1%) |
| Pred | 257 | 62 (24.1%) | 191 (74.3%) | 0 (0.0%) | 2 (0.8%) | 0 (0.0%) | 2 (0.8%) |
| Host | 136 | 26 (19.1%) | 106 (77.9%) | 0 (0.0%) | 2 (1.5%) | 0 (0.0%) | 2 (1.5%) |
| Effects | 17 | 1 (5.9%) | 10 (58.8%) | 0 (0.0%) | 6 (35.3%) | 0 (0.0%) | 0 (0.0%) |

Pseudo-directory ObjectiveProofs (modules whose name contains `ObjectiveBend` or `.Objective`, the Core4 metatheory and its Kernel wiring; ObjectiveProofs.lean itself only imports them):

| group | total | CLOSED-INSTANCE | PER-FUNCTION | REACHABLE-INVARIANT | REFINEMENT | TEMPORAL | OTHER |
|---|---|---|---|---|---|---|---|
| Objective* modules | 2732 | 145 (5.3%) | 2295 (84.0%) | 70 (2.6%) | 164 (6.0%) | 24 (0.9%) | 34 (1.2%) |

Theory/ObjectiveBendDemand* is where the trace theorems live (Reachable, preservation, adequacy, the forcing/halting development). Per top-level counts of the strongly trace-shaped buckets by directory: see columns above.

## Closed-instance theorems by proof method

CLOSED-INSTANCE = 3842. Proof flags: {'other-tactic/term': 1238, 'decide,rfl': 1465, 'rfl': 1004, 'native,decide': 126, 'decide': 9}. (`rfl` or `decide` alone, or both, means kernel-checked evaluation; `native` means compiled evaluation; blank/other means a tactic proof, usually `simp`/`norm_num` over literals or a proof built by applying a general lemma to specific constants.) 126 of the closed instances use native_decide.

## 30 most load-bearing CLOSED-INSTANCE theorems

Selection: CLOSED-INSTANCE theorems that are (1) cited by name in docs/OBJECTIVE-BEND.md (16 of them match, matched by full name or a unique suffix of at least 14 characters; this under-matches since the doc mostly cites families in prose), or (2) have sound/correct/safe/refus in the last name component (498 of them). Ranked: doc-cited first, then not in an Example/Fixture/Witness/Check/Demo module, then keyword count, then statement size. Only 3842 of 23006 are closed at all, and note that every "refused" theorem here is a single-input refusal: it shows the gate rejects one concrete forgery, not that the gate rejects the class.

1. `Minidregg.Theory.ObjectiveBendTyping.effect_as_argument_refused` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check  {  term :=  (Minidregg.Theory.ObjectiveBendOpenRecursion.Term.nat 0).lam.app  Minidregg.Theory.ObjectiveBendTyping.writePlan.perform,  annotations :=  Mini`
2. `Minidregg.Theory.ObjectiveBendTyping.effect_in_record_field_refused` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check  {  term :=  Minidregg.Theory.ObjectiveBendOpenRecursion.Term.record  [("next", Minidregg.Theory.ObjectiveBendTyping.writePlan.perform)],  annotations := Mi`
3. `Minidregg.Theory.ObjectiveBendTemplates.self_as_bound_row_rigid_refused` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check (Minidregg.Theory.ObjectiveBendTemplates.selfAsBoundRow [5]) [] 8).isNone =  true`
4. `Minidregg.Kernel.ObjectiveActivityGate.forged_protected_write_refused` (Kernel; doc-cited; proof: decide,rfl)
   `Minidregg.Kernel.ObjectiveActivityGate.ordinaryGate Minidregg.Kernel.ObjectiveActivityGate.forgedIntent =  Except.error  (Minidregg.Kernel.DurableDataIntent.RejectReason.protectedWrite  { value := Min`
5. `Minidregg.Theory.ObjectiveBendTyping.duplicate_affine_refused` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check Minidregg.Theory.ObjectiveBendTyping.duplicateAffine  [{ type := Minidregg.Theory.ObjectiveBendTypes.Ty.natural,  quantity := Minidregg.Theory.ObjectiveBend`
6. `Minidregg.Compiler.ObjectiveBendSpecificationClosure.law_keyword_refused` (Compiler; doc-cited; proof: native,decide)
   `Minidregg.Compiler.ObjectiveBendSpecificationClosure.acceptsSource  Minidregg.Compiler.ObjectiveBendSpecificationClosure.lawKeywordSource "asSpecification" =  false`
7. `Minidregg.Kernel.ObjectiveResumeContract.absolute_limits_refuted` (Kernel; doc-cited; proof: tactic)
   `(match  Minidregg.Theory.ObjectiveBendDemandMachine.resume Minidregg.Kernel.ObjectiveResumeContract.growResponse  Minidregg.Theory.ObjectiveBendDemandCollect.largerYield,  Minidregg.Theory.ObjectiveBe`
8. `Minidregg.Kernel.ObjectLawEnforced.capped_tally_teeth` (Kernel; doc-cited; proof: tactic)
   `Minidregg.Kernel.ObjectRecord.accepted  (Minidregg.Kernel.ObjectRecord.admitWrite  (Minidregg.Kernel.ObjectLawEnforced.cappedRecord Minidregg.Kernel.ObjectLawEnforced.cappedLaws)  Minidregg.Kernel.Obj`
9. `Minidregg.Compiler.ObjectiveBendFrontEndAdequacy.accept_inhabited` (Compiler; doc-cited; proof: native,decide)
   `(match Minidregg.Compiler.ObjectiveBendFrontEndAdequacy.example_lowering with  | Except.ok l => (Minidregg.Compiler.ObjectiveBendFrontEnd.accept l).toBool  | Except.error a => false) =  true`
10. `Minidregg.Theory.ObjectiveBendTemplates.coloured_discharges` (Theory; doc-cited; proof: decide,rfl)
   `Minidregg.Theory.ObjectiveBendTemplates.Discharges Minidregg.Theory.ObjectiveBendTemplates.colouredSelf  Minidregg.Theory.ObjectiveBendTemplates.templateAssumptions { } 1`
11. `Minidregg.Theory.ObjectiveBendTemplates.self_as_bound_row_alias_accepted` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check (Minidregg.Theory.ObjectiveBendTemplates.selfAsBoundRow []) [] 8).isSome =  true`
12. `Minidregg.Theory.ObjectiveBendTyping.heterogeneous_runtime_mix_accepted` (Theory; doc-cited; proof: decide,rfl)
   `(Minidregg.Theory.ObjectiveBendTyping.check Minidregg.Theory.ObjectiveBendTyping.heterogeneousSource [] 16).isSome =  true`
13. `Minidregg.Kernel.ObjectiveResumeContract.largerYield_resumes_exactly` (Kernel; doc-cited; proof: tactic)
   `Minidregg.Kernel.ObjectiveResumeContract.ForcingTransparent Minidregg.Kernel.ObjectiveResumeContract.largerConfig  Minidregg.Theory.ObjectiveBendDemandCollect.largerYield Minidregg.Kernel.ObjectiveRes`
14. `Minidregg.Compiler.ObjectiveBendSpecificationClosure.claim_spec_accepted` (Compiler; doc-cited; proof: native,decide)
   `Minidregg.Compiler.ObjectiveBendSpecificationClosure.acceptsSource  Minidregg.Compiler.ObjectiveBendSpecificationClosure.claimSpecSource "asSpecification" =  true`
15. `Minidregg.Compiler.ObjectiveBendSpecificationClosure.twice_accepted` (Compiler; doc-cited; proof: native,decide)
   `Minidregg.Compiler.ObjectiveBendSpecificationClosure.acceptsSource  Minidregg.Compiler.ObjectiveBendSpecificationClosure.twiceSource "twice" =  true`
16. `Minidregg.Compiler.Evaluator.resolveName_objectiveCore4` (Compiler; doc-cited; proof: rfl)
   `Minidregg.Compiler.Evaluator.resolveName "objective-core4" = some Minidregg.Compiler.Evaluator.objectiveCore4.id`
17. `Minidregg.Kernel.ObjectiveWorkAccount.meter_third_replay_refused` (Kernel; proof: decide,rfl)
   `(do  let x ←  do  let x ←  (Minidregg.Kernel.ObjectiveWorkAccount.Meter.start  (have __src := Minidregg.Kernel.ObjectiveTariff.zeroCapacity;  { typeFuel := __src.typeFuel, sourceTicks := __src.sourceT`
18. `Minidregg.Assurance.DreggNetProviderConsumer.Witness.refused_start_cancels_and_refunds` (Assurance; proof: rfl)
   `(Minidregg.Kernel.ProviderExecutionLease.terminalPlan  Minidregg.Assurance.DreggNetProviderConsumer.Witness.cancelledOutcome).kind =  Minidregg.Kernel.ReactiveTerminalCell.TerminalKind.cancelled ∧  Mi`
19. `Minidregg.Kernel.ContentResource.Audit.stale_same_length_bytes_refused` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.ContentResource.Audit.refusalOf  (Minidregg.Kernel.ContentResource.run Minidregg.Kernel.ContentResource.Audit.author  Minidregg.Kernel.ContentResource.Audit.nextOperation Minidregg.Ke`
20. `Minidregg.Kernel.ObjectiveWorkAccount.core_refuses_oversized` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.ObjectiveWorkAccount.uncovered Minidregg.Kernel.ObjectiveWorkAccount.sample  Minidregg.Kernel.ObjectiveWorkAccount.sampleArtifact  (have __src := Minidregg.Kernel.ObjectiveTariff.zero`
21. `Minidregg.Kernel.ObjectiveWorkAccount.frontEnd_refuses_oversized` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.ObjectiveWorkAccount.uncovered Minidregg.Kernel.ObjectiveWorkAccount.sample  Minidregg.Kernel.ObjectiveWorkAccount.sampleArtifact  (have __src := Minidregg.Kernel.ObjectiveTariff.zero`
22. `Minidregg.Kernel.WorldBench.bench_fold_1000_stale_refused` (Kernel; proof: native,decide)
   `(Minidregg.Kernel.World.fold Minidregg.Kernel.WorldBench.benchH Minidregg.Kernel.WorldBench.benchGenesis  ((Minidregg.Kernel.WorldBench.benchLog 1000).set 500  { txId := 501, creates := [],  legs := [`
23. `Minidregg.Kernel.ContentResource.Audit.forged_old_document_refused` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.ContentResource.Audit.refusalOf  (Minidregg.Kernel.ContentResource.run Minidregg.Kernel.ContentResource.Audit.author  Minidregg.Kernel.ContentResource.Audit.nextOperation Minidregg.Ke`
24. `Minidregg.Kernel.ContentResource.RunEditAudit.bad_insertions_refused` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.ContentResource.Audit.refusalOf  (Minidregg.Kernel.ContentResource.run Minidregg.Kernel.ContentResource.Audit.author  Minidregg.Kernel.ContentResource.Audit.nextOperation Minidregg.Ke`
25. `Minidregg.Assurance.LowRankCount.count_refusals` (Assurance; proof: decide,rfl)
   `{w |  ¬Minidregg.Assurance.LowRankAccepts Minidregg.Assurance.LowRankCount.cW  (Minidregg.Assurance.lowRankUpdate Minidregg.Assurance.LowRankCount.cW Minidregg.Assurance.LowRankCount.cA'  Minidregg.As`
26. `Minidregg.Kernel.DomainEpoch.Example.cached_foreign_domain_refused` (Kernel; proof: decide,rfl)
   `Minidregg.Kernel.DomainEpoch.admitAppend  (Minidregg.Compiler.StreamCell.headStore Minidregg.Kernel.DomainEpoch.Example.cachedHead)  Minidregg.Kernel.DomainEpoch.Example.sequencer  (Minidregg.Kernel.D`
27. `Minidregg.Theory.Renounce.bearer_renounce_refused` (Theory; proof: decide,rfl)
   `Minidregg.Theory.Renounce.gate  (some  (have __src := Minidregg.Theory.TypedAuthorization.demoCapability;  { id := __src.id, root := __src.root, parent := __src.parent, issuer := __src.issuer,  holder`
28. `Minidregg.Kernel.PayEnrolDecision.self_enrol_off_refused` (Kernel; proof: tactic)
   `Minidregg.Kernel.PayEnrolDecision.decideEnrol  (Minidregg.Theory.Store.Store.set Minidregg.Kernel.PayEnrolDecision.fixtureStore  Minidregg.Kernel.PayCell.tariffAddress  (some  (have __src := Minidregg`
29. `Minidregg.Host.Json.grainPolicy_repin_wrong_pins_refused` (Host; proof: native,decide)
   `([("expectedAddress",  Minidregg.Host.Json.decimal✝  ((Minidregg.Compiler.PolicyRecordCodec.digest Minidregg.Host.Json.grainRepinFixture✝).value + 1)),  ("expectedVersion", Json.str "4"), ("task", Jso`
30. `Minidregg.Compiler.DurableIndex.Probe.wrong_root_refused` (Compiler; proof: native,decide)
   `(match  Minidregg.Compiler.DurableIndex.setAll (Minidregg.Compiler.DurableIndex.overlay (fun x => none) [])  Minidregg.Compiler.DurableIndex.emptyDigest  [(Minidregg.Compiler.DurableIndex.Probe.probeK`

## Every TEMPORAL/LIVENESS theorem (42)

None states a liveness property of an infinite execution. They fall into: (a) bounded halting on the Objective Bend demand machine (`Halts s n` = reaches a final state in exactly n steps; `halts_*`, `forces_*`, `runBounded_*`, `node_spin_iff`); (b) completeness of fuel-bounded evaluators (`∃ n, ∀ fuel ≥ n, run fuel ... = ok`: Nock, Evaluator, derivation costs); (c) liveness conclusions projected out of an assumption structure whose fields are the unproved premises (`LivenessBoundary.*`, `ExternalCompletion.networkLiveness`, `RuntimeCompletion.eventuallyDelivered`, `ProgressRefinement.eventually*`, `LivenessRefinement.*`, `FairDelivery.eventually`): these are hypotheses re-exported, not liveness proofs.

| theorem | module | reason |
|---|---|---|
| `Minidregg.Assurance.HyperdocumentAgentRuntimeScheduler.RuntimeCompletion.eventuallyDelivered` | Assurance.HyperdocumentAgentRuntimeScheduler | name |
| `Minidregg.Assurance.HyperdocumentFinalizedDomainCrawler.ExternalCompletion.networkLiveness` | Assurance.HyperdocumentFinalizedDomainCrawler | name |
| `Minidregg.Assurance.ReactiveDurableSettlement.FinalizeSettlement.LivenessRefinement.delivers` | Assurance.ReactiveDurableSettlement | prop-const-pat |
| `Minidregg.Assurance.ReactiveDurableSettlement.FinalizeSettlement.LivenessRefinement.persists` | Assurance.ReactiveDurableSettlement | prop-const-pat |
| `Minidregg.Compiler.Evaluator.run_complete` | Compiler.Evaluator | exists-nat-steps |
| `Minidregg.Kernel.OutboxDelivery.ProgressRefinement.eventuallyAcknowledged` | Kernel.OutboxDelivery | name |
| `Minidregg.Kernel.OutboxDelivery.ProgressRefinement.eventuallyDelivered` | Kernel.OutboxDelivery | name |
| `Minidregg.Kernel.ProviderExecutionLease.LivenessRefinement.progresses` | Kernel.ProviderExecutionLease | prop-const-pat |
| `Minidregg.Kernel.QuotaGcSettlement.LivenessBoundary.acceptedCompactionEventuallyReclaims` | Kernel.QuotaGcSettlement | name |
| `Minidregg.Kernel.QuotaGcSettlement.LivenessBoundary.crawlerEventuallyRuns` | Kernel.QuotaGcSettlement | name |
| `Minidregg.Kernel.QuotaGcSettlement.LivenessBoundary.storageRemainsAvailable` | Kernel.QuotaGcSettlement | prop-const-pat |
| `Minidregg.Kernel.QuotaGcSettlement.LivenessBoundary.wallClockProgress` | Kernel.QuotaGcSettlement | prop-const-pat |
| `Minidregg.Kernel.ReactiveTerminalCell.LivenessRefinement.progresses` | Kernel.ReactiveTerminalCell | prop-const-pat |
| `Minidregg.Kernel.ReplicatedSettlementFinality.FairDelivery.eventually` | Kernel.ReplicatedSettlementFinality | name |
| `Minidregg.Theory.Nock.exhausted_says_nothing` | Theory.Nock | exists-nat-steps |
| `Minidregg.Theory.Nock.run_complete` | Theory.Nock | exists-nat-steps |
| `Minidregg.Theory.Nock.run_crash_complete` | Theory.Nock | exists-nat-steps |
| `Minidregg.Theory.Nock.step_runs` | Theory.Nock | exists-nat-steps |
| `Minidregg.Theory.ObjectiveBendDemandAdequacy.administrative_budget_halts` | Theory.ObjectiveBendDemandAdequacy | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.BackSim.back` | Theory.ObjectiveBendDemandForcingBack | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.Chain.spins` | Theory.ObjectiveBendDemandForcingConverse | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.Demand.halts` | Theory.ObjectiveBendDemandForcingNest | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.agree_halts_back` | Theory.ObjectiveBendDemandForcingBack | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.agree_transfer` | Theory.ObjectiveBendDemandForcingPend | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.failsWith_halts` | Theory.ObjectiveBendDemandForcingBackFail | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forceWith_finished` | Theory.ObjectiveBendDemandForcingSegment | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forceWith_of_halts` | Theory.ObjectiveBendDemandForcingSegment | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forces_fits` | Theory.ObjectiveBendDemandForcingExtract | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forces_halts_back` | Theory.ObjectiveBendDemandForcingBack | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forces_transfer` | Theory.ObjectiveBendDemandForcingChain | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.forces_transfer_back` | Theory.ObjectiveBendDemandForcingBack | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_drop` | Theory.ObjectiveBendDemandForcingPend | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_of_endsWith` | Theory.ObjectiveBendDemandForcingConverse | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_prepend` | Theory.ObjectiveBendDemandForcingBack | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_succ` | Theory.ObjectiveBendDemandForcingPend | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_tail` | Theory.ObjectiveBendDemandForcingPend | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.halts_unique` | Theory.ObjectiveBendDemandForcingNest | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.pend_halts_back` | Theory.ObjectiveBendDemandForcingBack | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.pend_transfer` | Theory.ObjectiveBendDemandForcingSwitch | const:Halts |
| `Minidregg.Theory.ObjectiveBendDemandForcing.runBounded_halts` | Theory.ObjectiveBendDemandForcingSegment | name |
| `Minidregg.Theory.ObjectiveBendDemandForcing.runBounded_of_halts` | Theory.ObjectiveBendDemandForcingSegment | name |
| `Minidregg.Theory.ObjectiveBendInteraction.node_spin_iff` | Theory.ObjectiveBendInteraction | const:Halts |

## Hand validation (10 per bucket, seed 4242, statements pretty-printed and read)

Rules were revised twice after two earlier samples (first: REACHABLE matched the words "execution/history/derivation/chain" and swept in 1100+ semantic-history and FRI-chain lemmas, TEMPORAL matched "Progress" and swept in ContentResource; both fixed). The sample below was drawn after the final rule change, with a fresh seed, so it was not used to tune.

| bucket | correct | notes |
|---|---|---|
| CLOSED-INSTANCE | 10/10 | all concrete instances (literals, fixtures, vectors) |
| OTHER | 10/10 | generic list/polynomial/Except/category lemmas |
| TEMPORAL | 10/10 by label | but 4 of the 10 are projections of assumed-liveness structures, and the rest are bounded halting / fuel completeness: label correct, content not liveness |
| PER-FUNCTION | 8/10 | `yieldedPlan_heapForces`, `forces_forceWith` are simulation-style (ForcesBy) lemmas that belong in REFINEMENT |
| REACHABLE-INVARIANT | 8/10 | `fill_distinguishable_at_duty_tick` and `unauthenticated_reachable` are closed instances caught by "trace"/"reachable" in a name or constant |
| REFINEMENT | 6/10 | misses: `kmac256_conforms_tagged` and `partial_terminal_agrees_but_check_bites` are closed test vectors/examples; `physicalIORefined` is a projection of an assumption bundle; `Agrees.symm` is a generic relation lemma |

Overall 52/60 = 87% precision on the sample. The weakest bucket is REFINEMENT (name patterns "conform"/"agree"/"refine" catch examples and assumption projections), so treat 472 as an upper bound; the true count of genuine two-semantics theorems is likely ~250-350. REACHABLE (335) and TEMPORAL (42) are small enough that a reader can audit them by grepping the TSV, which is worth doing before quoting the 1.5% figure. Recall was not measured (no sample of PER-FUNCTION for hidden trace statements beyond the 10 above, where none was found), but statements that quantify over traces through a locally defined `Trace`/`Network` type without any of the marker names would land in PER-FUNCTION; the Generic Simplex lemmas using `Reachable`/`Trace` were caught.
