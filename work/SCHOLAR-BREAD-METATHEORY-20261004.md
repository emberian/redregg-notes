# SCHOLAR-BREAD-META — the experimental record of Bread's metatheory, mapped for Mini

Read-only scholar report, 2026-10-04, written against `PROGRAM-MODEL-BRIEF-20261004.md`, after the first Bread
scholar's report (`SCHOLAR-BREAD-PROGRAM-MODEL-20261004.md`, "the first report" below) and ROOT's reading notes.
The first report mapped Bread's programs, cells, calls and promises at the node level. This one goes into
`metatheory/`: what was tried, what each attempt actually states, whether the statement has content, whether
anything ran it, and what Mini should take. Nothing was built, run, edited or committed; this is the only file written.

**Roots.** `B/` = `/Users/ember/dev/breadstuffs/` (HEAD `22fad151e`, 2026-10-01). `M/` = `B/metatheory/`
(library `Dregg2` = 2,353 files; `Metatheory` = 31; `Polis` = 70; `Market` ≈ 100). `MEM/` =
`~/.claude/projects/-Users-ember-dev-breadstuffs/memory/`. `MINI/` = `/Users/ember/dev/minidregg/`.

**Provenance tags.** **READ**: I read it at the cited line. **LANE-n**: one of eight read-only Opus sub-readers read
it at the cited `file:line` and I did not re-read it; where I re-checked a lane claim at source it says READ.
**INFERRED**: my conclusion, not checked at a line. **Status tags** (what Bread actually had): **RUN** = the node
calls it to decide something; **DIFF** = called from Rust only as a differential/shadow or test; **LEAN** = proved
in Lean, nothing outside Lean consumes it; **DOC** = prose only.

**Content tags** (what a statement is worth): **REAL** = a genuine induction/argument about the object named;
**TOY** = real proof about a model far smaller than the system it is named for; **DEF** = true by unfolding a
definition, a field projection, `Iff.rfl`, or a conjunction of the hypotheses; **HYP** = the conclusion is (nearly)
a hypothesis, or rests on an uninhabited/unused premise; **REFUTATION** = a genuine counterexample to a naive claim
(often the most valuable thing in a file).

**Mini verdicts.** PORT THE IDEA (with what to build) · PORT THE CODE (rare) · STUDY · AVOID · and, new here,
**ALREADY IN MINI** where `MINI/` already carries a redesigned port (Mini's `ATLAS.md`, 2026-08-06, was an earlier
six-lane harvest of this same corpus; §11 lists where this report confirms, corrects or extends it).

**A warning that governs every section.** Bread's corpus is axiom-clean and sorry-free, and its own audits
(`MEM/project-statement-audit-campaign.md`, `project-verified-system.md`, `project-polis-unification-correction.md`,
`historical-dregg2-false-as-stated-sorries.md`) found, repeatedly, that the *statements* were empty while the
arithmetic was immaculate: apexes over uninhabited premises, `P → P` under claiming names, identity carriers
(`fun _ _ v => v` with injectivity `fun … h => h`), "satisfiable" witnesses that inhabit a floor only at a free
inductive type. `#assert_axioms` (`M/Dregg2/Tactics.lean`) counts `axiom` declarations only; hypotheses and typeclass
fields are invisible to it. So "kernel-clean" below never means "assumption-free", and a theorem's name is never
evidence of its content. I read statements and, for the headline ones, proofs.

---

## 0. The verdict in one paragraph

Bread's metatheory is a large, honest-in-its-headers, uneven experimental record. Three things in it are genuinely strong and
were run: **the Lean executor with a triangle refinement to independently written specs** (`execFullForestG_iff_turnSpecG`,
`running_entry_sound`, `reachable_total_zero`), decided authoritatively by the node for the "covered" turns; **small Lean
decisions exported as fail-closed gates** (2PC verdict, finality order and quorum, round advance, constraint oracle, flow
refinement); and **the meta-verification tooling** built after its own vacuity scandals. Most of the rest — choreographies, the
Hatchery, effect handlers, the resource camera, Polis, upgrade, joint turns, Await, CapTP, the fibration — is proved about toy
models or proved by unfolding a definition, and nothing outside Lean consumes it. Mini has **already absorbed** the best of the
predicate/confluence/merge layer (one `Pred` AST, an executable certificate-producing satisfiability check, a computed
coordination dial, LaceMerge, hyperdocuments), often in a better form than Bread had. What Mini can still take is mostly
**ideas that Mini can make real where Bread could only model them**, because Mini re-executes deterministic Lean, has
decidable laws with satisfiability (hence entailment), and has a certifying checker: decidable governed upgrade with frozen
floors and typed migration; obligation-carrying action kinds; a choreography as a protocol object judged by its law; the
coordination ladder and justness for concurrent activities; import-versus-live-read; and an affordance algebra whose preview
and commit gates are one function.

## Inventory

Content tags: REAL / TOY / DEF / HYP / REFUTATION (see header). Consumer: RUN / DIFF / TESTED / LEAN / DOC / none.

| # | area | files (under `M/Dregg2/` unless noted) | key statements | content | consumer | Mini verdict |
|---|---|---|---|---|---|---|
| 1 | MPST core | `Coordination`, `DSLChoreo` | `GlobalType`, `project`, `projection_sound`, `deadlock_freedom_by_design`, `privacy_by_projection` | DEF (head duality over global-type residuals) + REAL-small + 2 REFUTATIONS | LEAN | PORT CODE (types, notation) + PORT IDEA (protocol object) §1 |
| 2 | choreography front end | `Projection`, `Spec/Choreography`, `Verify/ChoreographyBridge` | `epp_correspondence`, blue/red, `red_projects_to_hyperedge` | DEF | LEAN | AVOID |
| 3 | hyperedge / joint turns | `Hyperedge`, `Spec/JointViaHyper`, `JointTurn`, `Exec/JointCell`, `Distributed/EntangledJoint` | `ringHyperedge`, validity≠canonicity; `atomicity_as_proof`, `binding_is_proper` | REAL-small / DEF | LEAN, DIFF | PORT IDEA (CG-2⊗CG-5 as the statement) §8.2 |
| 4 | workflows | `Protocol/Workflow*`, `Deos/WorkflowBridge` | `exec_*`, `stateGate_iff_phase` | DEF / REAL-small; attestation unbound | LEAN | PORT IDEA (step gate = `Guard.all`, bind attestation) |
| 5 | predicate algebras | `Exec/PredAlgebra`, `Spec/Guard`, `Exec/Program`, `Authority/{Relational,Arithmetic}Closure`, `QuantifiedPredicate` | pointwise `eval` laws, `attenuate_narrows` | DEF | LEAN | ALREADY IN MINI (one AST, quantifier views) §2.1-2.2 |
| 6 | symbolic decision procedures | `Crypto/Deriv/Symbolic*`, `RealGuardDecisionLift`, `PredicateLibrary` | `feasible_iff_noNegativeCycle`, emptiness/equivalence `Decidable` | REAL proof-time; never executed | LEAN | ALREADY IN MINI (better); PORT IDEA: entailment/equivalence as named decisions §2.3 |
| 7 | deployed law evaluator | `Exec/DeployedConstraint`; `B/exec-lean/src/constraint_oracle.rs` | `admitsWire_eq_violated_iff` | codec REAL; semantics `#guard` | RUN | STUDY (fail-closed decline) §2.4 |
| 8 | I-confluence / CRDTs | `Confluence`, `Authority/ConfluenceClassifier`, `Confluence/{CRDT,DriftStable,SemanticConvergence}` | `IConfluent`, `escrow_refinement`, `bounded_not_nary_safe` | DEF + REAL (CRDT) | partial (Rust per kind) | ALREADY IN MINI (dial); PORT IDEA (escrow rung) §2.5 |
| 9 | flow refinement | `Deos/FlowAlgebra`, `Deos/FlowRefine` | `decideRefines_iff` | REAL (guard-free, iteration-free) | RUN (deploy tool) | PORT IDEA (guarded protocol refinement for upgrade) §2.6 |
| 10 | temporal / causal / time | `Authority/TemporalAlgebra*`, `CausalGuard`, `Time/*` | `commit_wait_bridge`, `chainOk_sound` | REAL-small | LEAN | PORT CODE (`Deadline`) §2.7, §9.5 |
| 11 | coinductive soundness | `Boundary`, `Exec/Cell` | `stepComplete_preserves`, `livingCell_sound` | DEF over TOY | LEAN | AVOID §3.1 |
| 12 | verify/find seam | `Laws`, `ConstructiveKnowledge` | `Verifiable`, `SoundSearchable.find_sound` | REAL (interface) | — | ALREADY IN MINI §3.1 |
| 13 | triangle refinement | `Spec/WholeTurnTriangle`, `Spec/FunctionalRefinement`, `AssuranceCase.running_entry_sound` | `execFullForestG_iff_turnSpecG` | REAL over the executor the node runs | RUN (covered turns) | PORT IDEA (per-action contract) §3.2 |
| 14 | l4v-style squares | `Spec/ExecRefinement*`, `Proof/{Refine,LTS,ForestLTS,CrossCellLTS}` | `refine_*` | TOY | LEAN | AVOID |
| 15 | composed apex | `AssuranceCase.deployed_system_secure` | — | HYP (floors refuted in-tree) | — | AVOID |
| 16 | meta-verification | `Verify/{FloorRatchet,FloorCensus,FloorPole,ToothCheck,ExistsImageVacuity,KeystoneLint,FreeConclusionRatchet,LoadBearingLint}`, `Tactics` | `tooth_minus%`, `inImage_vacuous_iff_surjective`, `#assert_compiled` | REAL tooling | CI | PORT CODE (selected; fix KeystoneLint) §3.4 |
| 17 | "Deployed" pattern | `Storage/Deployed*` | `contentRootDeployed_binds_or_collides` | REAL; found a real bug | DIFF | PORT IDEA §3.3 |
| 18 | logic compiler, realizability, calculus | `Logic/*`, `Metatheory/DirectLogic*`, `Realizability/*`, `Calculus/*` | two arithmetization counterexamples | scaffolding + 2 REFUTATIONS | off-path | AVOID / STUDY §3.5 |
| 19 | Hatchery and kinds | `Deos/Hatchery`, `Verify/Contract`, `Exec/Factory`, `Verify/*FactoryProbe`, `Apps/VerificationToolkit` | `CellContract.forever`, `constructor_transparency` | DEF/TOY; probes REAL; Rust contradicts transparency | none (Rust `MintedKind` unused) | PORT IDEA (shape catalog; kind = law) §4 |
| 20 | effect handlers | `Exec/{Handler,HandlerExecutor,HandlerFloors}`, `Exec/Handlers/*` | `EffectHandler`, `turn_conserves` | DEF at registry, REAL per handler | one test | PORT IDEA (obligation fields, real dispatch) §5 |
| 21 | verb registry | `Substrate/{VerbRegistry,VerbCompression,IssuerLedger}` | `minimality`, `grant_guard_not_local` | DEF / REAL separations | Rust gate test | STUDY; PORT IDEA (issuer well) §5 |
| 22 | resource camera | `Resource`, `StepCamera`, `Substrate/FpuProbe`, `Metatheory/Dynamics/*` | `ConfinesAuthority := Fpu`, `int_auth_fpu_vacuous`, `compile_not_a_seq_hom` | DEF + REAL negatives | LEAN | STUDY; PORT IDEA ("two gates") §6.1 |
| 23 | conservation | `Exec/ReachableConservation`, `Spec/Conservation`, `Exec/TriDomain` | `reachable_total_zero`; `multi_domain_independent` | REAL / DEF | Lean executor | PORT IDEA (the Book's invariant) §6.2 |
| 24 | attenuation, caveats, discharge | `Authority/{Caveat,CaveatChain,ThirdPartyDischarge,CaveatConvergence}`, `Exec/Caps` | `attenuate_subset`, `accepts` | REAL-small; root `.unchecked` on live path | not live | PORT CODE (attenuate); fix discharge binding §6.3 |
| 25 | Biscuit / Datalog | `Authority/BiscuitGraph`; `B/token/src/{datalog_verify,biscuit_backend}.rs` | — | no Lean semantics | RUN (Rust) | AVOID §6.3 |
| 26 | import vs live read | `Authority/CrossCellImport` | `importValid_stable_under_source_advance` | REAL-small | LEAN | PORT IDEA §6.4 |
| 27 | capability graph, confinement, revocation | `Spec/Authority`, `Metatheory/Open/AuthorityClosure`, `Exec/CellConfine`, `Firmament/SeL4Kernel`, `Agent/Mandate` | `only_connectivity_begets_connectivity`, `livingCellA_confinement`, `revoke_kills_all_doomed` | REAL | LEAN | PORT IDEA + PORT CODE (revoke, add saturation) §6.5 |
| 28 | upgrade, migration | `Upgrade`, `Exec/CellUpgrade`, `Exec/StateMigration` | `upgrade_never_bricks`, `self_improvement_is_safe`, `migrate_conforms` | DEF / REAL schema (noncomputable) / HYP false | none | PORT IDEA (decidable), AVOID code §7.1 |
| 29 | Polis | `M/Polis/*`, `M/PolisGovernor.lean` | `amendment_stream_nonregression`, `governed_holds` | REAL schema / DEF | exe unexercised | PORT IDEA (frozen floors, made decidable) §7.2 |
| 30 | epistemic regimes | `M/Metatheory/{ResearchRegime,Disputation,OptimisticAdjudication}` | `Publication.honest`, `optimistic_sound` | REAL-light / DEF | none | PORT IDEA (regime-typed badges) §7.3 |
| 31 | games | `M/Metatheory/{SafetyGame,ReachGame,EnergyGame}` | viability kernel, attractor | REAL with enabledness hole | LEAN | PORT with `∃ r, legal` added §7.3 |
| 32 | roster reconfiguration | `Distributed/{ConfigBoundary,EpochReconfig}` | `churnStepOk_breaks_at_one_one_from_four` | REAL | RUN/DIFF | PORT CODE §7.1 |
| 33 | consensus gates | `Distributed/{FinalityGate,RoundAdvanceGate,AckBeforeAdmit,StrandAdmission,QuorumThreshold,FinalizationQuorum,LaceMerge,CrashRecovery}` | quorum intersection, `advance_iff` | REAL | RUN | PORT IDEA (export discipline) + CODE (quorums) §8.1 |
| 34 | 2PC | `Coord/TwoPhaseCommit`, `Exec/DistributedExports` | `evaluate_not_commit_and_abort` | REAL-small (a tally) | RUN | PORT CODE + extend §8.2 |
| 35 | fibration, revocation bound, finality tiers | `Distributed/{Fibration,Revocation}`, `Finality` | `lift_collapse`, `eventual_bounded_revocation` | DEF | LEAN | PORT IDEA (single-machine principle), rebuild §8.3 |
| 36 | concurrency, contention, justness | `Proof/{ContendedCrossCell,ContendedForest,Stingray,Fairness}`, `Coord/*` | `just_progress` | REAL-small / TOY | Stingray RUN in Rust | PORT IDEA §8.4 |
| 37 | await, CapTP, conditional turns | `Await`, `Spec/Await`, `Exec/{CapTP*,ConditionalTurn,ReactiveRegistry,Continuation}` | `commit_resumes_once`, `drainAll_preserves_caps`, `no_double_react` | HYP (uninhabited premise) / DEF / REAL-small | partly RUN (Rust) | AVOID; PORT IDEA (nullifier one-shot) §8.5 |
| 38 | vat boundary | `Exec/VatBoundary`, `Spec/VatBoundary` | `phi_drops_confinement` | DEF | LEAN | PORT IDEA (derive "crossing") §8.6 |
| 39 | affordances, projection | `Deos/{Affordance,GatedAffordance,Reactive,FireProgramAgreement,FogOfWar,Membrane,Surface}` | `fire_authorized_iff_subset`, `fireGated_iff` | REAL-small; FogOfWar headline DEF | Rust twin | PORT CODE + preview/commit types §9.1 |
| 40 | documents, transclusion, branches | `Deos/{DocMerge,DocPatch,DocMergeComposed,PatchCategory,Transclusion,AnchoredQuote,BranchStitch}`, `M/Metatheory/SettlementSoundness` | `merge_is_lub`, `deployedSettle_binds_live_authority` | REAL; PatchCategory pushout DEF | `stitch_pair` RUN | PORT CODE / IDEA §9.2 |
| 41 | reversibility, rehydration | `B/turn/src/reversible.rs`, `Deos/{Rehydration,ReplayMembrane}` | — | Rust TESTED; Lean DEF | TESTED | PORT IDEA, prove in Lean §9.3 |
| 42 | firmament, mirrors | `Firmament/*`, `B/docs/deos/FIRMAMENT-REFLEXIVE-SUBSTRATE.md` | `no_amplification`, `notifyCap_confers_no_edge` | REAL-small; mirror unbuilt | none | PORT IDEA §9.4 |
| 43 | intents | `Intent/*` | `settleRing_conserves`, `fulfilled_then_no_refund` | REAL | RUN (`verified_settle.rs`) | PORT IDEA §9.5 |
| 44 | adjunction → hyperdoctrine | `Metatheory/{Lawvere,IndexedMonoidal}` | `lawvere_triple`, `relExists_adj_relForall` | REAL-small; thesis REFUTED | `Authority/Epistemic` | STUDY §10 |

---

## 1. Choreographies and session types

**Files.** `M/Dregg2/Coordination.lean` (798 lines), `DSLChoreo.lean` (303), `Projection.lean` (133),
`Spec/Choreography.lean` (327), `Verify/ChoreographyBridge.lean` (82), `Protocol/{Workflow,WorkflowGuard,Transfer}.lean`,
`Hyperedge.lean` (481), `Spec/JointViaHyper.lean` (499), `Deos/WorkflowBridge.lean` (516), `Deos/FireProgramAgreement.lean`.
All reachable from the default `Dregg2` target; no `sorry`, no `axiom`, no `@[export]` in any of them (LANE-1, spot-checked READ).

**What it defines (READ, `Coordination.lean`).**
```lean
inductive GlobalType where                                   -- :68
  | comm (src dst : Role) (s : Payload) (cont : GlobalType)
  | choice (src dst : Role) (branches : List (Label × GlobalType))
  | mu (X : TyVar) (body : GlobalType) | var (X : TyVar) | done
-- LocalType: send | recv | select | offer | mu | var | done      -- :89
-- mergeLocal L₁ L₂ := if L₁ = L₂ then some L₁ else none         -- :193  (identity merge only)
def Dual : LocalType → LocalType → Prop                          -- :358
  | send _ s₁ _, recv _ s₂ _ => s₁ = s₂ | recv _ s₁ _, send _ s₂ _ => s₁ = s₂
  | select _ _, offer _ _ => True | offer _ _, select _ _ => True | _, _ => False
```
`Role`/`Label`/`Payload`/`TyVar` are all `Nat`. A `ProtocolCell` (:320) bundles `G`, a `TurnCoalg`, a start state
and `residual start = G`. The surface is `dregg_choreo { a ~(ℓ)~> b ; … }` (`DSLChoreo.lean:41-100`), plain macros onto
`GlobalType`, with an elaboration-time `#check_projectable` gate (:283).

**What is proved, and how (READ the two headline proofs; LANE-1 for the rest).**
| theorem | statement | proof | content |
|---|---|---|---|
| `projection_sound` :373 | for `pc.G = comm a b s k`, `a ≠ b`: `Dual (project pc.G a) (project pc.G b)` | `rw [hG]; simp only [project, if_true, if_neg hab.symm, Dual]` | one constructor unfolded; the `wf : Projectable` premise is never used; docstring admits the real EPP bisimulation is OPEN |
| `deadlock_freedom_by_design` :697 | `NoRec G → NoSelfComm G → GReach G G' → G' ≠ done → ∃ a b, a ≠ b ∧ Dual (project G' a) (project G' b)` | preservation lemmas + case split on the head | about the *global type's own reduction* `GReach`; no endpoint LTS, no queues, no asynchrony; `Dual` ignores roles and labels and holds for `choice a b []`, which is stuck |
| `deadlock_freedom_progress_step` :764 | `NoRec → Guarded → GReach G G' → G' ≠ done → ∃ G'', GStep G' G''` | head case split | true by syntax |
| `privacy_by_projection` :483 | `NoRec G → p ∉ roles G → project G p = done` | real mutual structural recursion | syntactic but genuine |
| `deadlock_initial_counterexample` :662, `privacy_var_counterexample` :465 | the naive statements are false | concrete `G` | **genuine refutations** (the old statements were false-as-stated; `historical-dregg2-false-as-stated-sorries.md` records it) |
| `epp_correspondence` (`Projection.lean:105`) | — | literally `projection_sound` | docstring: "no independent content yet" |
| `Spec/Choreography` `red_projects_to_hyperedge` :168, `blue_needs_no_hyperedge` :227, `epp_membrane_is_projection` :297 | — | field copies, `Iff.rfl`, conjunctions of facts sharing no variables | hollow |
| `ChoreographyBridge` "blue/red forever" :34-59 | — | real facts about the production trajectory `trajG` | unrelated to choreography; only the names connect them |

`GStep` has no `mu` rule, so recursive protocols are excluded by the `NoRec` premise rather than handled. `ProtocolCell` does
not tie its coalgebra to `GStep` (any coalgebra with `residual := fun _ => G` inhabits it). Nothing maps a `GlobalType`
to the blue/red colour of `Projection.lean`. **No Rust session-type or choreography implementation exists**; Rust mentions
these names only in doc comments (`starbridge-apps/agent-orchestration/src/lib.rs:45-46`). The workflow file is one
hard-coded three-party protocol whose attestation is not bound to the step (`Workflow.lean:80-86`: `stmt` is a free
parameter, and `runHappy` reuses one attestation for all three steps), with single-step facts only.

**Genuinely real in this area:** the hyperedge validity facts — `ringHyperedge` (cyclic reindexing makes the telescoping
sum vanish, `Hyperedge.lean:254`), `hyper_not_all_admissible` (:425), `hyperedge_is_validity_not_canonicity`
(`JointViaHyper.lean:226`, a sharp point: validity of a joint step does not select among histories), and
`AggTree.accepts_iff_all_leaves` (:441). But `hyperedge_sound` (:327) never uses the hyperedge's `agree`/`balanced` fields.

**Consumers.** Lean-internal only (`DSLChoreo`, `Projection`, `Spec/Choreography`, `Exec/DfaRouting`, `Claims` pins).
Nothing in the node. The memory's "we already have the MPST coordination layer"
(`project-intent-co-receipt-time-typing.md`) overstates it.

**Verdict for Mini.**
- **PORT THE CODE (small):** `GlobalType`, `LocalType`, `project`, the identity merge and the mutual `DecidableEq`
  (`Coordination.lean:68-239`), plus the `dregg_choreo` notation. Replace `MergesAt`/`NoRec`/`NoSelfComm`/`Guarded`
  with `Bool` functions and reflection lemmas so the elaboration gate is `decide`.
- **PORT THE IDEA, better than Bread could:** skip endpoint projection as the enforcement story. Mini re-executes every
  turn, so a *protocol object* can hold the residual `G` as state, and its law admits a turn exactly when it is a `GStep`
  of the residual by the role bound to the signer. Then `GStep`/`GReach` preservation and the progress lemma are the honest,
  small theorem for a **centralized choreography monitor**, and Ember's "calls across objects, very rich" gets a typed
  multi-party protocol whose conformance is a per-turn law check. Add `mu` unfolding with a guardedness check. Endpoint
  projection becomes a *client-side* artifact (what each party's resident may do next), not the safety argument.
- **Keep the two refutations** as regression theorems against restating the false versions.
- **AVOID:** citing `projection_sound`, `epp_correspondence`, or anything in `Spec/Choreography.lean` as results.

---

## 2. Verifiers and logics: the predicate/guard algebra and its decision procedures

### 2.1 About a dozen predicate algebras, never unified

(LANE-2; spot-checked READ.) `SimpleConstraint`/`StateConstraint` (`Exec/Program.lean:67,280`, ~30 scalar atoms plus
affine, reachability, clearance, `anyOf`); `Pred` (`Exec/PredAlgebra.lean:127-183`: `atom c | tt | ff | and | or | not |
allOf | anyOf` plus typed `symEq`, `symMemberOf`, `digEq`, `digFieldEq`, `fieldEqField`, `…Unchanged`, `…Changed`;
`Pred.eval : Pred → Value → Value → Bool`, a structural fold over `(old, new)`); `Spec.Guard` (`Spec/Guard.lean:90-95`:
`firstParty (p : Request → Bool) | witnessed s | all | any | gnot` — atoms are opaque Lean functions, so nothing can
analyse it); `CellProgram.Guard`; `CaveatPred` (`Authority/Caveat.lean:66-89`); `RelCaveat` (one atom,
`fieldLteOther index other delta` = `x ≤ y + c`, a difference constraint, `Exec/RelationalCaveat.lean:68`); `RelPred`,
`ArithPred`, `QuantPred`, `PrivPred`; `TemporalAtom`, `EventAtom`; `ConfluenceClassifier.Guard`; and the **deployed**
one, `DConstraint`/`DTop` (`Exec/DeployedConstraint.lean:295-368`, 58 of the 69 Rust variants over `Nat` mod 2^256).
`M/docs/RESEARCH-predicate-language.md:90` already complained of "THREE algebras". Laws proved on them are pointwise on
`eval` (`deMorgan_and/or`, `eval_not_not`, `allOf_cons`, …), each `rfl` or `simp`. **There is no Boolean-algebra or
Heyting instance on any predicate type**: `Laws.predicate_heyting` (`Laws.lean:121`) is a generic Mathlib restatement
never instantiated, while `Exec/Program.lean:14` claims the fragment "realizes" it. **DEF.**

`Spec/Guard.lean`'s one seam (authorization, preconditions, program constraints and macaroon caveats as one `Guard`),
with `attenuate g c := all [g, c]` and `attenuate_narrows` (:207) as a meet-semilattice narrowing, is the right idea
(and ember's correction "attenuation is NOT Heyting", `MEM/project-dregg2-three-projections.md`, is encoded there). Its
opaque atoms are the flaw: Mini's ATLAS law "one predicate algebra, syntactic AST end-to-end" is the fix and **is already
in Mini** (`MINI/Pred/Core.lean`).

### 2.2 The ladder affine → polynomial → quantified

`RelPred` (`Authority/RelationalClosure.lean:83`, atom `affineLe (terms) k`, absent fields read as 0 — unlike `Pred`, which
fails closed), `ArithPred` (`ArithmeticClosure.lean:101`, `polyLe`), `QuantPred` (`QuantifiedPredicate.lean:68`,
`forall_ (range : List ι) (P : ι → RelPred) | exists_ | memberOf`). The "closure theorems" are the pointwise `eval`
laws plus embeddings; `forall_eq_andFold`/`exists_eq_orFold`/`compile_sound` are list inductions (a bounded quantifier
unrolls to a fold). Hollow members: `relPred_constraints_bounded : constraintBudget p ≤ sizeBound p` compares two
identical functions; `relPred_is_record_local p rec : p.eval rec = p.eval rec := rfl`; `mulInv_non_affine_witness`
evaluates three points and does not prove non-affinity. Only the affine rung exists in Rust (`AffineLe/AffineEq/
AffineDeltaLe/FieldLteOther`, `B/cell/src/program/types.rs:1047,1344,1348,1534`); the practically useful "quantified" rung
that shipped is `DCollPred` (bounded aggregates over heap collections: `countSatGe`, `sumOfLe/Ge`, `allMembers`,
`existsMember`, `mOfNDistinct`, `DeployedConstraint.lean:208`). **DEF/TOY.** Mini: **ALREADY IN MINI** in the right shape —
`MINI/Pred/BoundedQuantifiedView.lean` makes bounded ∀/∃ *views* of the one `Pred` AST with proved-equal denotation,
exactly ATLAS's plan.

### 2.3 Satisfiability, equivalence, subsumption: there IS a decision procedure — in Lean, unused

The first report (following `B/docs/DESIGN-predicate-usefulness-targets.md:37-43`) said no satisfiable/subsumes/equiv
procedure exists. **That is wrong for Lean** (that doc predates the work; LANE-2 and READ). `M/Dregg2/Crypto/Deriv/`
(~15k lines, July 2026) holds a symbolic-derivative tower over regexes of `Pred`-labelled symbols, and
`SymbolicDifference.lean` (2,283 lines, READ) is a **verified difference-bound-matrix decision procedure**:
```lean
structure Edge (n : Nat) where src : Fin n; dst : Fin n; bound : Int   -- x(dst) - x(src) ≤ bound   :47
def NegativeCycle (G) := ∃ s es, es ≠ [] ∧ IsWalk G s es ∧ walkEnd s es = s ∧ walkWeight es < 0      :80
theorem feasible_iff_noNegativeCycle {n} (G : List (Edge n)) :
    (∃ x, Satisfies G x) ↔ ¬ NegativeCycle (withSource G)                                            :458
def predRE_emptiness_decidable_difference …   -- Decidable (∃ w, derives w R = true)              :2129
def predRE_equivalence_decidable_difference … -- Decidable (∀ w, derives w R = derives w T)       :2141
```
The extraction `predDifference?` (:540-580) maps `fieldEquals/Ge/Le`, `inRangeTwoSided`, `memberOf`, `immutable`,
`writeOnce`, `monotonic`, `strictMono`, `fieldDelta`, `deltaBounded`, `fieldLeField`, `fieldDeltaInRange`,
`fieldEqField` under `and/or/not` to cuts over `(old,new)` coordinates. Equivalence is emptiness of the symmetric
difference; subsumption is emptiness of `A ⋒ ¬B`. `RealGuardDecisionLift.lean` uses the decisions on real guards via
`@of_decide_eq_true … (by rfl)` (`history_gate_no_drift :274`, `goad_excludes_history :241`, `age18_subsumes_age1 :336`).

**Its limits, in the author's own words** (READ, end of file): "the CERTIFIED cover (`coverOfDifference`) is never
EXECUTED anywhere. `allRegions` enumerates `3^|cuts|` DBM regions … this module PROVES a decision procedure and
DEMONSTRATES the algorithm on hand-picked alphabets"; the EMPTY-direction `#guard`s are "ILLUSTRATIVE Bool evaluations,
NOT certified verdicts". Shortest paths enumerate every simple path (`simplePathsTo :147`). It decides over `Pred.eval`
on `Int`; nothing connects it to `DConstraint` (`Nat` mod 2^256), which is what the node evaluates. No `@[export]`, no
Rust consumer. **REAL (proof-time only), TOY in execution.**

**Mini is already past this.** `MINI/Pred/Satisfiable.lean` (READ header) decides the same fragment *executably*:
DNF of difference systems with presence/absence, Bellman–Ford keeping witnessing walks, a `.witness` step re-checked by
`eval`, an `.unsat` **certificate** (a clash or a constraint cycle whose bounds sum below zero) checked by
`SysCert.check_sound`, `.unknown` proved unreachable on translated laws (`SatisfiableTotal.decide_never_unknown`), with
a `dnfCap` refusing blow-up. **ALREADY IN MINI, better.** Two things in Bread's tower Mini does not yet have and should:
(a) **entailment and equivalence as named decisions** — Mini's DNF pushes negation to atoms, so `A ⊨ B` is
`unsat(A ∧ ¬B)` with a certificate, at no new cost; this is what upgrade non-regression (§7) and "the kind's floor still
holds" (§4) need; (b) **regexes over transition symbols** (multi-step law shapes: "after X, never Y"), decided by
derivatives — with Bread's stated boundary that multi-symbol words do not link `newᵢ = oldᵢ₊₁`, so they over-approximate
trace feasibility. **PORT THE IDEA (a); STUDY (b).**

### 2.4 The constraint oracle (the deployed law evaluator)

(LANE-2.) `B/exec-lean/src/constraint_oracle.rs` marshals a `StateConstraint`, old/new `CellState` and a typed context,
calls `@[export dregg_constraint_admits] def admitsFFI` (`DeployedConstraint.lean:1671`) → `admitsTop`. Lean decides 58
of 69 variants; Rust decides eleven witness/crypto arms (`PreimageGate`, `KeyRotationGate`, `ClearanceDominates`,
`SenderAuthorized`, `Renounced`, `Witnessed`, `TemporalPredicate`, `ObservedFieldEquals`, `AnyOfBound`, `CountGe`,
`Custom`). When Lean declines a subset constraint, `undecided_subset_disposition` returns
`Err(ConstraintOracleUnavailable)` — **fail-closed** (`B/cell/src/program/eval.rs:404-440`). Installed unconditionally by
the node (`B/node/src/lib.rs:1210`). **RUN.** What is proved: only the wire codec (`admitsWire_eq_violated_iff :1762`,
`admitsWire_malformed_iff :1785`, keeping malformed distinct from violated). The semantics of `admits` rest on 153
`#guard`s and a Rust differential. **DIFF-grade semantics on a RUN path.**

### 2.5 I-confluence and the coordination dial

`IConfluent I := ∀ x y, I x → I y → I (x ⊔ y)` (`Confluence.lean:33`, READ); `admits_sound` is the definition applied;
`nonpairwise_escalation` is classical De Morgan; the content is the two poles (`top_iconfluent`,
`cardLeOne_not_iconfluent`). `ConfluenceClassifier.lean`: `keeps_iff_coordinationFree … := Iff.rfl` (:125),
`monotone_keeps` (:170) needs a monotonicity hypothesis and is one `le_trans`, `bounded_breaks` takes the clash as
hypotheses. Its header says the module makes the cost "a DECIDABLE, PROVED question"; `DriftStable.lean:210` says the
opposite and is right: "'Is φ I-confluent?' is not decidable, so it is not decided. The tier is carried as a witness."
**DEF.** Genuine content: `CRDT.lean`'s `escrow_refinement` (:443, local quotas are I-confluent and `Σq = B` implies the
global bound — the Balegas/Sypytkowski bounded counter as a positive theorem), `bounded_not_nary_safe` (:506, pairwise ≠
n-ary), `locked_driftStable` (`DriftStable.lean:100`), the six-rung coordination ladder independent → monotone CRDT →
confluent after lifting → reservation (escrow) → lock → per-op equalizer (`MEM/project-drift-stability-spectrum.md`),
and `SemanticConvergence.lean` (the one computable classifier: monotone unless a negation is present). Rust classifies
per *kind* (`B/dregg-merge/src/gate.rs:84`: a static `is_iconfluent_kind()` flag) and per *query* (`B/dregg-query/src/classify.rs:64`),
never per constraint; neither is on the node path.

**Mini: ALREADY IN MINI, and better than Bread.** `MINI/Pred/CoordinationDial.lean` (READ header) computes a `Verdict`
over the one `Pred` AST for the v0 merge discipline (slot-wise max), proves `dial_sound` (every `.free` verdict is
I-confluent, by induction on the AST, against `eval` itself), and refuses loudly (`.ordering`, `.stepShaped`,
`.thirdParty`) with a necessity tooth (`demoAny_not_confluent`). Bread never had a computed per-clause grade. **PORT THE
IDEA still open:** the ladder's middle rungs — reservation/escrow (`escrow_refinement`) and "confluent after lifting" —
are where fork 3's "many activities on one object" live; Mini's dial currently says `.ordering` for them.

### 2.6 FlowAlgebra / FlowRefine (the decidable flow-refinement result)

(LANE-2, READ statements.) Syntax `Proc = done | emit ℓ | wr ℓ f v | ch P Q | seqp P R` (`FlowAlgebra.lean:121-132`) —
**no guard, no iteration**; refinement `≤ᶠ` is ordinary strong simulation at every start state. `decideRefines_iff : decideRefines A B
= true ↔ A ≤ᶠ B` (`FlowRefine.lean:372`), real strong induction (`decideFuel_sound :324`, `decideFuel_complete :339`),
with `Decidable (A ≤ᶠ B)`. **REAL**, but it is simulation checking on finite acyclic labelled systems — textbook; Pradic's
Weihrauch/Büchi machinery (arXiv:2408.14999, cited at `FlowAlgebra.lean:16`) is never exercised because the fragment has
no iteration. `flow_choice_right_skewed` (:467) is a real proof that choice half-distributes one way only; the other
"RSKA_d⊓" laws in `M/docs/FLOW-COMPOSITION-ALGEBRA.md` are not proved, and `flow_meet_semilattice` is a meet on trace
sets, not on `≤ᶠ`. Exported as `dregg_decide_refines`, called by `B/dregg-deploy/src/refine.rs:241` from
`refines_upgrade` (the `dregg-deploy refine` CLI and a desktop workflow); deploy flows are linear chains, so in practice
`new ≤ᶠ old` reduces to a prefix check. Fails closed without the archive. **RUN (deploy tool only, not admission).**

**Verdict.** **PORT THE IDEA:** decidable refinement between an object's old and new *protocol* (its method/affordance
graph) as an upgrade gate (fork 4), and between a choreography and an implementation (§1). It needs guards (Mini has
decidable laws to label edges with) and memoisation; with guards it becomes simulation over a guarded finite system,
still decidable. **AVOID** citing the Pradic/right-skew classification as proved.

### 2.7 Temporal and causal guards, guarded holes, CellProgram

- **Temporal atoms** (`Authority/TemporalAlgebra.lean:111`: `afterHeight | beforeHeight | withinWindow | cooledSince |
  rateBound | challengeWindow`) are height comparisons — difference constraints against a clock; their laws are `omega`.
  `TemporalAlgebra2` adds until/since as register flips, vesting, a sealed auction phase discipline and a concrete
  justness-liveness demo. **REAL, small.** `CausalGuard.chainOk_sound` (:80) checks a supplied chain of ack edges; no
  completeness, no search — verify-not-find. **Mini: PORT THE IDEA** — a law atom "height ≥ stored + k" is already a
  difference constraint if the clock is a slot; "causally after event E" needs a supplied, checked chain.
- **`GuardedHole`** (`Exec/GuardedHole.lean:37-67`): `holeFill_binds_in_circuit` unfolds an `if`; no circuit is involved.
  **DEF.** The design rule it names (eager shape, lazy witness) is the valuable part and is already in the first report.
- **`CellProgram`** (`Exec/CellProgram.lean:94-108`, READ): `denote p k t := if p.admits k t then exec k t else none` and
  `denote_eq_exec_on_success` is the case split. **DEF**, but it states the right principle — **a program can only tighten
  the kernel, never bypass it** — which in Mini is structural (the kernel applies the Plan; laws judge it).

---

## 3. Refinement, "Deployed", "Projections", and the meta-verification tooling

### 3.1 The three-projection architecture and the coinductive layer

The chosen dregg2 architecture (`MEM/project-dregg2-three-projections.md`) composes three "projections": **C** the
authority spine (`Authority/Positional.lean`, CDT ≡ blocklace strand log), **B** the trust law (`Laws.lean`: the TCB is
the *verifier*; soundness by verification, never by construction; VERIFY cheap, FIND undecidable), **A** the coinductive
style (`Boundary.lean`: a cell is a Moore coalgebra; "the turn is the rollback handler"; checkpoint/replay as theorems),
layered like l4v (abstract spec → executable design spec `Exec/*` → refinement `Proof/Refine.lean`).

What A actually is (READ): `def Later (Q : Prop) : Prop := Q` (`Boundary.lean:87`), so the ▶ guard is the identity;
the keystone `stepComplete_preserves` (:157) is `Execution.invariant_run` re-applied (its premise `hpres` is "Good is
preserved by every StepInv-respecting step"); `sound_refl` is reflexivity. The celebrated `livingCell_sound`
(`Exec/Cell.lean:102`, READ) is `bisim_of_oracle livingCell conservationOracle cellOracle cell_h_obs cell_h_step`, where
the oracle coalgebra has carrier `ℤ` and never changes, and `cell_h_step` is `conservation_step_realized` for the toy
`Exec.Kernel` — i.e. "the conserved total is invariant", restated as a bisimulation. **DEF over a TOY.** The checkpoint
theorems were once `id`-identities and were replaced (Cell.lean :113-115 says so) by a `Snapshot` token; the
single-machine memory calls CellRuntime's checkpoint "a `rfl` label-fiction" (`MEM/project-dregg4-vision.md`). The
dregg4 reality check itself sorted these into REAL / DECORATION / ASPIRATIONAL and put "final coalgebra FINALITY",
"comodel/handler interprets turns", "lens get/put" under DECORATION.

B is the durable part (`Laws.lean:35-56`, and `ConstructiveKnowledge.lean`): `Verifiable.Verify : P → W → Bool`,
`Discharged`, `Searchable.find` with deliberately no soundness field, `SoundSearchable.find_sound` as the plugin
contract with the tooth `evilMatcher_not_sound`. Mini's ATLAS took it verbatim (`MINI/ATLAS.md §3.1`). **ALREADY IN MINI.**

C: `Spec/Authority.lean:603` `only_connectivity_begets_connectivity` (READ) is a genuine induction over `Reachable` with
four generative constructors (introduce, amplify, mint, endow) plus a confined `origin` base case and two restrictive
ones (attenuate, revoke): every edge descends by `confers` from an initial edge or from an edge added by an authorized
generative act. **REAL, about an abstract graph** (no executor). See §6.

### 3.2 Is there a contentful refinement to the executor the node runs? Yes — the triangle.

(LANE-3; READ the statement.) `Spec/WholeTurnTriangle.lean:184`:
```lean
theorem execFullForestG_iff_turnSpecG (s s' : RecChainedState) (f : FullForestG …) :
    execFullForestG s f = some s' ↔ turnSpecG s (lowerForestG f) s'
```
`turnSpecG` is a fold `∃ s1, gateOK na s = true ∧ fullActionStep s a s1 ∧ turnSpecG s1 rest s'`; `fullActionStep`
dispatches to per-effect *relational* specs with explicit frames (e.g. `MintASpec`, `Circuit/Spec/supplycreation.lean:116`:
admission ∧ the new `bal` ∧ the new log ∧ every other field unchanged). The proof is a real induction on the action list.
`FunctionalRefinement.lean` adds per-effect biconditionals against *independently written* intent functions
(`mint_triangle :238`: `mintStep k a = some k' ↔ (mintGate k a ∧ k' = mintSpec k a)`) with `_antighost` corollaries for
~20 families. `AssuranceCase.running_entry_sound` (:811) states, for `execFullForestG s f = some s'`, per-asset
conservation, non-amplification on every forest edge, and the per-node gate invariant — with **no crypto floors**.
This is the most honest, contentful statement in the corpus about code the node actually calls (for covered turns; §5).

Caveats: the relational specs reuse executor helpers (`recTransferBal`), which is why the separate intent functions
exist; the FFI link `export_refines_endToEnd` (`Exec/FFI/Refine.lean:137`) carries `hblock : w.turn.blockHeight = 0`;
the production no-copy path `execDirect` has no theorem, only `#guard`s and a Rust differential. The older l4v-style
squares (`ExecRefinement*.lean`, `Proof/{Refine,LTS,CrossCellLTS,ForestLTS}.lean`) are over the toy
`Exec.Kernel` (`KernelState {accounts, bal : CellId → ℤ, caps}`) with `abbrev ExecRights := Unit` still present
(`ExecRefinement.lean:219`) and `discloseSupply` admitting any delta (`ExecRefinementFull.lean:106`). **TOY.**

The composed apex `AssuranceCase.deployed_system_secure` (:934) takes injectivity hypotheses (`compressInjective`,
`compressNInjective`, `cellLeafInjective`, `RestHashIffFrameFin`) that the tree itself refutes at BabyBear width
(`Verify/ApexPremiseVacuity.lean:203`, "two field elements do not fit in one"; header: "vacuous at deployed BabyBear
width, five ways"); both apexes are grandfathered in the floor-ratchet baseline. **HYP.** Logic layers over the real
trajectory exist and are genuine: CTL via `OrderHom.lfp/gfp` (`Proof/CTL.lean`), μ-calculus encodings
(`Proof/MuCalculus.lean`), just-path liveness (`Proof/CTLLiveness.lean`), a single-cell VCG `vcg_run_sound`
(`Proof/WP.lean:210`, not lifted to forests), noninterference for `setField` only with an exhibited leak
`makeSovereign_leaks` (`Proof/Noninterference.lean:544`). `Paco/` is a vendored Lean port of Coq paco
(~4k lines; header says MIT, `Paco/LICENSE` says Apache-2.0) with one consumer.

### 3.3 "Deployed" and "Projections"

- **`Projection.lean`** (READ) is the choreography front end (§1): blue/red colour = `IConfluent`, proved by `Iff.rfl`;
  `epp_correspondence` = `projection_sound`. **DEF.**
- **The "Deployed" pattern** (`Storage/{Deployed,DeployedFloorRefuted,DeployedFloorRegrounded}.lean`, LANE-3): Lean logic
  over an `@[extern]` opaque Rust primitive (`p2compress`), exported back (`dregg_storage_content_root`). Headline
  `contentRootDeployed_binds_or_collides : objs = objs' ∨ SpongeColl poseidon2Hash (…)` — **no hypothesis**: either it
  binds or a collision is constructed. Its history is the exemplar: the earlier `Poseidon2SpongeCR` floor was refuted by
  `rfl` because `Int.toNat` clamped `-1` and `0` together — **refuting the floor found a real encoder bug**; a
  `fail_if_success (… := rfl)` tooth guards the regression. Consumer: Rust tests only.

### 3.4 The meta-verification tooling — Bread's most transferable product

(LANE-3, with the vacuity classes READ in `MEM/minted-*`.) Bread built Lean-internal gates against its own recurrent
failure (true, kernel-clean, vacuous theorems):
- **Floor ratchet** (`Verify/FloorRatchet*.lean`, `FloorCensus.lean`): a "refuted floor" is *derived* from the tree's own
  `¬ F` theorems plus an injectivity-shape test (`FloorCensus.injShape :321`), consumers found by a position-independent
  elaborated-type scan (`assumesFloorContent :448`), baselines keyed by (decl, floor-set), fails closed unless ≥500k
  constants were scanned. Header: "This tool only GATES. It proves nothing." `FloorPole.HonestHypothesis` marks a
  parameterized floor honest only if four checks pass, including an inhabited-class model — the repair for the ⊥-class
  loophole (`MEM/project-statement-audit-campaign.md`, OUTCOME).
- **KeystoneLint** (`@[load_bearing_keystone satisfiable:=W teeth:=T]`, `#keystone_audit`): 86 of 110 apex pins audited
  (`M/docs/KEYSTONE-LEDGER.md`, READ). **Weakness:** it checks the companions exist and are axiom-clean, not that their
  types relate to the keystone; two `_orBreak` keystones whose conclusion was literally `True` passed it
  (`FreeConclusionRatchet` header). And its "satisfiable" witnesses for CR floors use a proven-*injective* non-hash
  `encodeSponge` (KEYSTONE-LEDGER: "`Poseidon2SpongeCR` is REALIZABLE by the proven-injective `encodeSponge`") — the
  identity-carrier class (`MEM/minted-identity-carrier-vacuity.md`).
- **FreeConclusionRatchet**: flags keystone conclusions containing a subterm the tree proves free (`Q ↔ True`).
- **ToothCheck** (`#tooth_minus T drops h`, `tooth_minus% T h`): a "dropping h breaks T" tooth must be stated about
  exactly `T` minus `h` (measured: 9 exact, 8 derived, 6 refused of 23).
- **ExistsImageVacuity**: `inImage_vacuous_iff_surjective`, `narrow_into_wide_is_nonvacuous`, the repair
  `InImageAuth f auth y := ∃ w, auth w ∧ y = f w` (the `∃`-over-an-image class, `MEM/minted-exists-image-vacuity-class.md`).
- **LoadBearingLint**: a spec must not transitively reference the executor gate it specifies; `isDefEq spec gate` must be
  false (catches `:= rfl` collapses).
- **`#assert_compiled`** (`Tactics.lean:193`): accepts only `ofReduceBool`/`ofReduceNat` or re-evaluated closed-Bool
  axioms (written after a name-pattern version accepted a forged axiom). **`scripts/check-guard-discipline.py`**: the
  `#guard` count may only fall. **`scripts/mutation-canary.sh`**: mutate burn, require AUTH-DROP to go red, daily.

**Verdict for Mini.**
- **ALREADY IN MINI (as laws):** ATLAS §6 laws 1, 2, 8, 9 encode these lessons; Mini has `Theory/AssertAxioms.lean`,
  `Theory/AssertCompiled.lean`. ATLAS planned a generated `Assurance/` (keystone audit with satisfiable + teeth + premise
  inhabitation) and notes that as of 09-30 none of it is generated.
- **PORT THE CODE (selectively, high value):** `ToothCheck`'s `tooth_minus%`, `ExistsImageVacuity`, the
  FreeConclusion fixpoint, and the floor-derivation logic are pure Lean meta-code. **Fix KeystoneLint before porting**:
  type-check that `satisfiable` instantiates the keystone's *premises* and `teeth` refutes the keystone minus one
  hypothesis, and reject identity carriers (an injective non-compressing "hash" must not inhabit a CR floor).
- **PORT THE IDEA: the triangle as Mini's per-method contract.** For every kernel action (and for every package method's
  Plan), `exec s a = some s' ↔ gate s a ∧ s' = spec s a` against an *independently written* spec with an explicit frame,
  folded to the whole turn. In Mini the executor *is* the Lean term, so this is a direct theorem, not a refinement tower.
- **PORT THE IDEA: "binds ∨ extract collision"** as the statement shape wherever Mini's commitments (the sparse Merkle
  root) are claimed to bind, and "refute your floor at the deployed instance" (it found a real bug).
- **AVOID:** l4v-style squares over a toy kernel; `Later := id` coinduction presented as productivity; composed apexes
  whose floors the tree refutes.

### 3.5 The logic compiler, direct logic, realizability, calculus

(LANE-3.) The "direct logic" program compiles typed finite Boolean/FOL predicates into the deployed `EffectVmDescriptor2`
circuit IR (two backends, a verified rewrite optimizer, a translation-validating certificate checker
`DirectLogicOptimizerCertificate`, a category of certified presentation changes, an arg-min search over presentations).
`M/docs/LOGIC-COMPILER-ASSESSMENT.md`: "a real spine, split across two backends, with the deployed backend
hand-authored"; 26 of 91 deployed descriptors compiler-authored (2026-08-05). Each compiler module says "Standalone
additive module. No integration imports are changed." Two genuine negative results: finite-field cancellation breaks
Gabbay's zero-means-true (`FOLArithmetizationCounterexamples`, `babyBear_false_and_false_accepted` via √−1), and the
published BitLogic swap relation accepts an invalid witness (`published_swap_accepts_invalid_witness :161`).
Realizability (`PCA.lean`, `Assemblies.lean`, `UFamTripos`, named `…Laws` not `Tripos` on purpose) is witnessed only by
a unit PCA; `RealizabilityLocalRewriteOracle` is a 2-row interaction-net oracle. `Calculus/DreggCalculus.dregg_calculus`
(:353) is a conjunction of existing facts with `Iff.rfl` aliases; `Calculus/Biorthogonality.lean` (677 lines) is real —
guards as biorthogonally closed behaviours tested by the live evaluator `Exec.evalConstraintCtx`.
`Metatheory/Lawvere.lean` + `IndexedMonoidal.lean` are the hyperdoctrine that replaced the refuted adjunction thesis (§11).

**Verdict.** **AVOID** the arithmetization machinery (Mini has no proof system in admission; `MEM/project-no-proof-system-in-mini-admission.md`).
**STUDY** the two counterexamples (they belong in Selvage's reading list) and the translation-validation pattern (an
untrusted optimizer emits a certificate a small checker validates — the verify/find seam applied to compilation, which is
how a Mini compiler pass from `.obend` to checked core could be trusted without being verified).

---

## 4. The Hatchery and kinds

**Files.** `M/Dregg2/Deos/Hatchery.lean`, `M/Dregg2/Verify/Contract.lean`, `M/Dregg2/Exec/Factory.lean`,
`M/Dregg2/Verify/{Escrow,Vault,Allowance,Obligation,Queue}FactoryProbe.lean`, `M/Dregg2/Apps/VerificationToolkit.lean`,
`B/HATCHERY.md`, `B/docs/deos/HATCHERY-ABSTRACTION-MINT.md`; Rust `B/sdk/src/hatchery_mint.rs`, `B/grain-commons/src/hatchery.rs`.

**The thesis (READ, `B/HATCHERY.md` §0-2).** One reusable theorem sits under every "forever" crown:
`livingCellA_carries (Good) (hpres : ∀ s cf, Good s → Good (cellNextA s cf)) … : ∀ n, Good (trajA s sched n)`.
The Hatchery's observation is that `hpres` is nearly always mechanical (a 46-way split of the executor where 45 arms
leave the field alone), so it proposes four tiers: domain tactics (`carry_forever`, `exec_frame`, `crypto_portal`),
an `aesop` rule set, a `CellContract { Inv, shape, step_ob }` bundle with `forever`, and a **shape catalog**
(`monotone_registry%`, `conservation%`, `confinement%`, `automaton_inv%`, `eventually%`) as "the smart-contract spec
language". That design is good and is the most reusable *idea* in the area.

**What was built (LANE-4, spot-checked READ).** Two different things share the names.
- `Verify/Contract.lean:84-114`: `CellContract (E : CellExecutor)` with `step_ob : ∀ s c, Inv s → Inv (E.next s c)` and
  `forever := CellCarries.carries …`, instantiated at `CellExecutor.production` over `RecChainedState` (the record kernel
  the Lean executor runs). **REAL**, but the theorem is ordinary inductive-invariant reasoning; all content is in
  `step_ob`, which quantifies over every forest step of the real Lean executor. Every app "forever" crown I read is an
  instance of a *kernel-wide* invariant, not an app property: `Apps/BountyBoardForever.lean`'s
  `bbf_plain_conserved_forever` is `asset_conserved_forever_production s0 rewardAsset sched` (READ) — the bounty board
  conserves because every cell does.
- `Deos/Hatchery.lean` (the file Ember named): a **separate toy**. `abbrev St := List ℤ`; a closed two-case
  `inductive Invariant | balanceNeverBelow (slot) (floor) | monotoneField (slot)` (:105-117); `evalStep` a two-case checker
  (:141-146); `step_preserves` (:184) is the gate's iff-lemma or `le_trans`; a *local* `CellContract.forever` (:205-221)
  takes `hadm : ∀ n, guard (traj (n+1)) (some (traj n)) = .ok` — "forever" means "any sequence of admitted steps",
  plain induction. It never imports `Verify/Contract`. **TOY.**
- `MintedKind` exists only in Rust (`hatchery_mint.rs:213-226`: `{invariant, descriptor, child_program, hpres}`);
  `HpresProof::Attested { contract_hash: [u8;32] }`, and `attest_hpres` stores any 32 bytes and checks nothing (:292-295);
  Bread's own test says so (`circuit-prove/tests/hatchery_binding_deployed_tooth.rs:27`).
- Forge detection: Lean `Conforms inv program := inv.constraint ∈ program` (:329-352; `program_missing_invariant_rejected`
  is its hypothesis). Rust `attest_membership` (`hatchery_mint.rs:346-361`) accepts if the program's VK matches or every
  needed constraint appears *somewhere* in the program, ignoring case guards (so a constraint in a never-firing case counts).
- **Consumers.** The node never references `MintedKind`, `HpresProof` or `attest_membership`; the only minter is
  `grain-commons::GenesisAgent::mint_subagent`, itself unconsumed. Production "kinds" are plain `FactoryDescriptor`s with
  `state_constraints` (escrow/obligation/bridge blueprints, starbridge apps) with no `HpresProof`. **TOY + DOC.**
- **Factory transparency** (`Exec/Factory.lean:178-257`): `factory_mints_conforming`, `constructor_transparency`,
  `cellStep_preserves_program` — the last is `rfl` because the model has no program-replacing action. **Rust contradicts
  it**: `apply_set_program` (`B/turn/src/executor/apply.rs:1416-1455`) does `c.program = program.clone()` gated only by
  the `SetVerificationKey` permission, with no factory-provenance check; `SetProgram` has no Lean wire arm, so turns
  containing it always fall back to the Rust producer (`B/exec-lean/src/lean_shadow.rs:430,748`). The file did honestly
  delete its vacuous `vk_determines_*` theorems (they assumed `HashInjective` at BLAKE3 width; tombstone :259-299).
- **The five factory probes** are the interesting experiment: escrow, vault, allowance, obligation and queue as
  *factory cells over the one kernel move verb* rather than as kernel verbs. Four pass; conservation in each reduces to
  `recKExecAsset_conserves_per_asset`. **The Queue probe's honest failure** is a real design datum: per-slot caveats
  cannot say `head − tail ≤ capacity`, so it proposes a record-level `FieldLteOther` (`QueueFactoryProbe.lean:28-59,148`).
  Mini's law language already has `leSlots`/`leSlotsOff` (cross-slot difference atoms, `MINI/Pred/Satisfiable.lean` header),
  i.e. Mini starts where the probe ended.
- **The app verification toolkit** (`Apps/VerificationToolkit.lean`, guide `Apps/VERIFICATION-TOOLKIT-GUIDE.md`, READ):
  an app's logic is "folded by the author into" `admit : Int → Int → Bool` on **one scalar slot**, baked into a finite
  `admitTable` over a hand-picked grid, then `app_commit_iff_admit`, `app_violation_rejected`, `app_commit_conserves`,
  `app_commit_no_amplify` come generically; the Rust mirror is hand-ported and pinned by a copied decision vector. Real
  plumbing theorems, but the expressiveness is exactly the "lamesauce" Ember complained of (`MEM/project-lamesauce-predicate-critique.md`):
  one slot, one Bool, a finite grid. Mini's ATLAS reports 3 of 63 apps adopted it.

**Verdict for Mini.**
- **PORT THE IDEA (high value): the shape catalog as package-declared contracts.** A Mini package declares
  `invariant`s in a small set of shapes (monotone registry, conservation of a measure, confinement under a ceiling,
  relation among fields); the certifying checker discharges the one-step obligation against the method bodies and the
  law; "forever" is then the free induction. Bread's lesson is *where* the obligation must range: over the **real**
  kernel step (all methods, all callers, all schedules), not a two-case model.
- **PORT THE IDEA: a kind is its law, by construction.** In Mini a kind's laws should be part of the pinned package
  and the cell's law literally *is* (or is entailed by) them; Mini can decide entailment (§2.3), so "the new law still
  contains the kind's floor" is a decision, not a containment search that ignores guards.
- **Close the `SetProgram` hole by design**: an object kind states whether and how its law may be replaced (fork 4);
  factory transparency and upgrade must be one rule (Bread had two contradictory ones).
- **AVOID:** stored proof hashes (`HpresProof`), the `List ℤ` Hatchery, the scalar `admit` toolkit as an app model.

## 5. Effect handlers with obligations

**Files.** `M/Dregg2/Exec/{Handler,HandlerExecutor,HandlerFloors,HandlerOpenFronts}.lean`, `M/Dregg2/Exec/Handlers/*.lean`,
`M/Dregg2/Substrate/{VerbRegistry,VerbCompression,IssuerLedger,HeapKernel}.lean`, `M/Dregg2/Exec/{TurnAdmission,FFI,FFIDirect}.lean`,
`B/docs/RUST-LEAN-EXECUTOR-PARITY.md`, `M/docs/RESEARCH-handler-executor.md`.

**What it defines (LANE-4; READ for the deltas).**
```lean
structure EffectHandler (Args : Type) where                          -- Handler.lean:70-87
  step : RecordKernelState → Args → Option RecordKernelState
  delta : Args → AssetId → Int
  auth : RecordKernelState → Args → Bool
  admission : RecordKernelState → Args → Bool
  trace : Args → Turn
  auth_gated : ∀ s a s', step s a = some s' → auth s a = true
  admission_gated : ∀ s a s', step s a = some s' → admission s a = true
  conserves : ∀ s a s', step s a = some s' → ∀ b, recTotalAsset s' b = recTotalAsset s b + delta a b
abbrev Registry := List PackedHandler                                -- :105
theorem turn_conserves : ∀ es s s', execTurn es s = some s' →        -- :172
    ∀ b, recTotalAsset s' b = recTotalAsset s b + turnDelta es b
```
- `turn_conserves` is a `foldlM` induction (**REAL**, generic, ~20 lines). But **every registered handler has
  `delta := fun _ _ => 0`** (READ: `Handler.lean:251,313`, `Handlers/{Authority,Bridge,Escrow,Lifecycle}.lean`,
  `HandlerExecutor.lean:191,203,216`; `Exercise` sums inner deltas, also 0), because mint/burn are moves against an
  issuer well that carries −supply (`Handlers/StateSupply.lean:60-64`). So the "registry-wide conservation" sums zeros;
  the content is each handler's own `conserves` field, discharged from kernel lemmas. **DEF at registry level, REAL per handler.**
- **The registry is not consulted.** `ClosedEffect` carries its own handler and `execEffect e s := e.handler.step s e.args`
  (:124) never checks `tag`; `masterRegistry` appears only in `masterRegistry_length : … = 23 := rfl` (READ,
  `HandlerExecutor.lean:125`). Dispatch is `toClosedEffect`, a 56-arm `match` on `FullActionA` (:257-310). The match moved.
- `HandlerFloors.lean` (`FloorObligation St Args step := {floor, gated : ∀ s a s', step s a = some s' → floor s a}`)
  is the right structural answer to the silent-gate class (`MEM/minted-handler-floors-retire-gate-hole-class.md`), but
  the floors are separate values about separate step functions, not fields of `EffectHandler`, and `execHandlerTurn`
  never consults them.
- The header's "concrete attacks `execFullA` ADMITS but `execHandlerTurn` REJECTS" (`HandlerExecutor.lean:39-42`) is
  **stale**: the current `#guard`s (:1827-1837) show both executors rejecting R1/R6 (the live executor was fixed), and the
  R2 fixtures were deleted with escrow.
- `handler_refines_execFullA_*` (~40 theorems): handler-commits ⊆ `execFullA`-commits, one direction; no theorem relates
  `execHandlerForestG` to `execFullForestG`, the executor the node runs.
- `VerbRegistry.minimality`/`each_verb_irreplaceable` prove a hand-assigned label table is injective (**DEF**);
  `VerbCompression`'s separation theorems (`grant_guard_not_local` :466, `grant_guard_not_literal` :489,
  `freshness_not_positive` :657) are the real content of the "kernel is 3 verbs" claim, and ATLAS's "proves the kernel is
  3 verbs" is stronger than what is proved (lifecycle and revoke compress into guarded writes; minimality is a label fact).

**Did the node run it? No, but it ran its sibling.** The handler executor's export `dregg_exec_handler_turn` is called
by exactly one Rust test (`B/dregg-lean-ffi/tests/handler_cutover_probe.rs:19,40`, READ). The node calls
`produce_via_lean` → `dregg_exec_full_forest_auth[_direct]` → `execFullForestG`, the 4-leg-gated 56-arm executor
(`B/node/src/executor_setup.rs:564`, `B/exec-lean/src/lean_apply.rs:1796`, LANE-4). **For covered turns the Lean verdict is
authoritative**: a Lean commit installs Lean's post-state, a Lean reject restores the ledger even if Rust accepted
(`lean_apply.rs:1904-1936`); it is on by default (`DREGG_LEAN_PRODUCER=0` disables, `B/node/src/state.rs:93-97`) and Lean is
linked unconditionally on native (`B/node/Cargo.toml:16-18`). Uncovered turns (FNSP-v3 routes, consensus side-state,
anything not root-agreeing or not marshallable, including every `SetProgram`/`Promise`/`Notify`) fall back to Rust.
There is no theorem `TurnExecutor::execute = recKExec` (`RUST-LEAN-EXECUTOR-PARITY.md:23`), and until 2026-08-06 the
marshaller compared only the low 64 bits of the chain head, so Lean admitted forged previous-receipt hashes and its verdict
was installed (:118-164). Which binary is deployed is unverified (`MEM/project-twin-deletion-campaign.md`).

**Verdict for Mini.**
- **PORT THE IDEA (high value): an action kind is a record whose gates are proof fields.** When a package introduces a
  new Plan action kind, its handler is a structure with `step`, `footprint`, `authority demand`, and obligations
  `auth_gated`, `law_gated`, `conserves` (state-level measure, not a sum of zero deltas), `floor_gated` for each floor
  (Bread's `FloorObligation` as fields, not side values). Ill-typed until discharged; the certifying checker discharges.
- **PORT THE IDEA, fixing the flaw: dispatch must actually index the registry** (`tag` → handler with a proof
  `handler = registry[tag]`), or the "open registry" is a closed match in disguise.
- **PORT THE CODE (tiny):** `turn_conserves`' fold induction, if Mini wants per-action deltas.
- **PORT THE IDEA: the issuer-well model** (`Substrate/IssuerLedger.lean`: supply as −balance at the issuer, Σ=0 as an
  identity) — Mini's Book should state conservation this way so mint/burn are moves, not carve-outs.
- **AVOID the two-executor shape** (Lean covered-set + Rust fallback + differential). Mini is Lean; the chain-head
  truncation bug is the lesson about what a marshaller between two executors does to a verified decision.

---

## 6. Resource and authority logics

### 6.1 The resource camera (Iris-style)

(LANE-5; READ `Resource.lean:100-112,316-322`.) `class ResourceAlgebra R` (op, `valid`, partial `core`; no unit, no
step-index) with instances `Nat`, `Excl`, `Auth M`. `def Fpu a b := ∀ f, valid (a ⊙ f) → valid (b ⊙ f)`;
`def ConservesResource pre post := Fpu pre post`; `def ConfinesAuthority held' held := Fpu held' held` — the docstring:
"Defining it as `Fpu` — rather than proving an `↔` — is the point". So "at camera tier conservation and confinement are
one law" (`MEM/project-dregg2-resource-camera.md`, "THE PRIZE") holds **by naming**. **DEF.** `conservation_is_fpu` (:296)
passes its `hmono` premise through. In bare `Excl`, `op` is always invalid, so every `Fpu` there is vacuous.

The connection to the executor is `Substrate/FpuProbe.lean`, and its **own findings are the valuable part** (LANE-5):
`move_value_fpu` (:455), `grant_authority_fpu` (:519), `spend_evidence_fpu` (:578), `write_state_fpu` (:790) instantiate
real executor arms over each verb's footprint; but `int_auth_fpu_vacuous` (:198) — "EVERY `●`-update, including the most
violent mint, is Fpu" over ℤ; `nat_auth_coordinated_mint_fpu` (:219) — "Fpu expresses frame-consistency, NOT Σδ=0";
conservation enters only through `SAuth` (valid := measure = s₀), under which `preserve_fpu` is just `P a → P a'`; and
`camera_blind_to_caveats` (:816) with the verdict (:1032) "**PARTIAL** … The DREGG3 §2 skeleton should say 'two gates'
(Fpu + admission), not one." `StepCamera.lean` (OFE, `Later`, `Camera` with `extend`) has only the discrete instance and no
consumer. `Metatheory/Dynamics/Initiality.lean` has a real result: `interp_eq_fold`, `fold_unique`, and the negative
`compile_not_a_seq_hom` (:406) — naming the one design change that would make executor⟺circuit agreement free.

**Verdict.** **STUDY** the camera; **PORT THE IDEA** of FpuProbe's verdict: admission (law) and conservation (Book) are two
gates, not one, which is exactly Mini's split. **AVOID** StepCamera and the "one law" framing. For the Book, state
conservation directly as an invariant (`SAuth` is that, in camera clothes).

### 6.2 Conservation and linearity classes

`reachable_total_zero` (`Exec/ReachableConservation.lean:49`) — Σ over all accounts and assets is 0 at every state reachable
from a value-empty genesis by committed `execFullTurnA` steps, because mint and burn are moves against an issuer well that
carries −supply (`ledgerDeltaAsset_eq_zero`). **REAL, about the real Lean executor; the strongest value theorem in Bread.**
`LinearityClass` (Conservative/Monotonic/Terminal/Generative/Annihilative/Neutral) exists twice (`Spec/Conservation.lean:78`,
`Exec/Effect.lean:55`); `multi_domain_independent` (:363-381) unfolds a conjunction and `conservedInDomain _dom deltas :=
deltas.sum = 0` ignores its domain. **DEF.** Rust deleted its enum on 2026-07-28 ("zero non-test callers", and Mint/Burn were
coloured Generative/Annihilative while the deployed ones are well-paired, `B/turn/src/action.rs:1018-1040`); the Lean still
colours `.mint` as Generative (`Spec/Conservation.lean:166`). `GlobalValueConservation.Value_conserved_of_step` carries the
channel invariants and the untouched-disjointness as fields of `Step` (**HYP**); `ConservationMultiEdge.round_boundaryFlow_zero`
is zero by definition. `feedback-conservation-is-not-correctness.md`: per-effect Σδ=0 is a projection of the state change,
not evidence the step is right.

**Verdict.** **PORT THE IDEA:** Mini's Book should carry `reachable_total_zero` as its invariant with issuer wells (assets
are issuer cells; mint/burn are moves), proved by induction over committed turns. **AVOID** linearity colourings.

### 6.3 Attenuation, caveat chains, third-party discharge, Biscuit/Datalog

- **Attenuation** proofs are short and genuine everywhere: `Caveat.attenuate_narrows` (:162, `List.all_append`),
  `Exec/Caps.attenuate_subset` (:124) and `attenuate_confRights_le` (:156) over `Finset Auth`, `CredentialAttenuation.attenuate_le`
  (a multi-axis clearance lattice), `BiscuitGraph.biscuit_narrows`, `CDT.path_attenuates` (:158). **REAL, small.**
- **HMAC chain** (`CaveatChain.lean`): a faithful fold `T₀ = mac root nonce`, `Tᵢ = mac Tᵢ₋₁ (encode Cᵢ)` verified from the root
  key; `chain_unforgeable` (:402) routes through a `MacKernel.unforgeable` carrier, refuted by a collapse instance (:509).
- **Third-party discharge** (READ `ThirdPartyDischarge.lean:224-232`): `accepts tpc m parentTail ctx now` checks the recovered
  key, freshness (300 s), `chainValid`, `boundTo m parentTail`, and the predicate. **The discharge is bound to the parent
  macaroon's tail, not to the request or turn**, so a fresh discharge can be replayed for any request carried by the same parent
  token inside the window.
- **Is any of it live? No.** The production root authorization is `mkAuth … := { …, capMode := .unchecked (Guard.all []),
  …, chain := none, …, chainDis := fun _ => false }` (READ, `Exec/GatedForestCfg.lean:107-110`); only a demo forest carries a
  chain. Children do gate `keep ⊆ parentCap` (`mkGAuthEdge`, `FFI.lean:2332`). The exported caveat type is a tiered state caveat
  (`WCaveat`), not a macaroon. The bridges `CaveatCapBridge.chainGateG_implies_capAuthorityG` (unused `_hchain`) and
  `TokenCapBridge` (both sides unfold to `decide (granted ⊆ held)`) are **DEF**.
- **Biscuit/Datalog: no Lean semantics exists.** `BiscuitGraph.Block` is `{authority : Finset Auth, vkey, sig}` — a rights-subset
  chain, not facts/rules/checks. The real verifiers are Rust: a custom Datalog engine for macaroons
  (`B/token/src/datalog_verify.rs`, "the SOLE ground-truth verification semantics") and `biscuit-auth 6.0.0`'s authorizer for
  Biscuits (`B/token/src/biscuit_backend.rs:123-145`), with no Lean counterpart and no differential. The macaroon differentials
  hand-transcribe the Lean into Rust. (`M/docs/HARVEST-KEEPERS.md` lists "Lean model of the datalog evaluator" as unbuilt,
  "high-risk research-grade".)
- `CaveatConvergence.coreOfCaveat_view_embeds` (:177) is a genuine induction: the caveat AST is a *view* of the one `Pred`
  algebra. **REAL.**

**Verdict.** **PORT THE CODE (small):** `attenuate_subset`/`attenuate_confRights_le` over finite rights sets. **PORT THE IDEA,
fixed:** third-party requirements in laws ("this clause is satisfied by a discharge from object X") must bind the discharge to
the **invocation hash**, not just to a parent token. **PORT THE IDEA:** caveats are views over the one law AST (already Mini's
ATLAS law). **AVOID:** a second policy language (Datalog) beside the law language; the macaroon machinery unless Mini issues
bearer tokens to the outside world.

### 6.4 CrossCellImport: import versus live read

(LANE-5; the first report flagged it.) `SourceHistory := {chain : ReceiptChain, stateAt : Receipt → Value}`;
`importValid H h imp := wellLinked H h.chain ∧ imp.provenance ∈ h.chain ∧ readAt h imp.provenance imp.sourceField = imp.value`
(:87); `importValid_stable_under_source_advance` (:124) is a real three-leg argument, but immutability of the past is **built into
`advance`**, which never touches old receipts (not derived from a hash); `liveRead_changes_under_source_advance` (:168) is an
existence witness by `decide` on an empty history. Consumers: GovernedParameters, RealAppsRound2, Deos Transclusion. No executor
check, no export. **REAL-small, LEAN.**

**Verdict. PORT THE IDEA (high value for fork 1 and fork 3):** two named operations with different footprints — a *live read*
of another object (part of the turn's read set; conflicts with concurrent writers; re-executed against current state) and an
*import* (a read pinned to a committed root; stale but stable; conflicts with nothing; the receipt is part of the invocation).

### 6.5 Capability graph, CDT, revocation, confinement

- `Spec/Authority.only_connectivity_begets_connectivity` (:603, READ) — every edge descends by `confers` from an initial edge or
  from an edge added by an authorized generative act (introduce, amplify, mint, endow, or the confined `origin` self-grant).
  `Metatheory/Open/AuthorityClosure.noforge_closure` (:104) adds an amplifier-`⊗` variant (sealer/unsealer done right). **REAL,
  abstract graph.** ALREADY IN MINI's ATLAS take-list (§3.4).
- **Revocation is not transitive in the main kernel**: `Caps.revoke` works on one holder's slot; `recKRevokeTarget`
  (`AuthTurn.lean:244`) filters one holder; onward grants are independent copies; `recKRevokeDelegationFull` bumps an epoch so
  children go stale (`:392`). `CSpace.lean` promises "`revoke` walks the derivation tree" and defines no revoke. **The only
  transitive revocation is `Firmament/SeL4Kernel.revoke`** (remove a fuel-bounded `doomedSet` over `mintedFrom`, `:212-226`) with
  `revoke_kills_all_doomed` (:580); that `doomedSet` contains every transitive descendant is **not proved**.
- `SeL4Abstract.dregg_executor_cap_authority_grounded_in_seL4` (:585) assumes a bridge `SeL4DeriveNonAmpBridge` that is never
  instantiated; LANE-5 argues it is uninhabitable (it grounds attenuation in `derive_cap`, while seL4 attenuates in
  `CNode_Mint`/`mask_cap`) — INFERRED by LANE-5, not machine-checked; `project-verified-system.md` already dropped "seL4-cited"
  as a floor.
- `Exec/CellConfine.livingCellA_confinement` (:566): every held cap stays under a ceiling `U` along every trajectory of the real
  Lean executor. **REAL.** `InfoFlow/Confinement.lean` (toy `Exec.Kernel`) has two honest negative results:
  `full_noninterference_fails` (a deposit is a write-up channel) and `refusal_leaks` (refusal is a covert channel).
- `Agent/Mandate.lean`: `Mandate {grantor, holder, target, keep, budget, caveat}`, sub-delegation by `keep ∩`, `min` budget,
  conjoined caveat, with real tree invariants (`subtree_rights_le_root`, `children_no_oversubscribe`); but `materialize` passes only
  `keep` to the executor — **budget and caveat are never enforced** — and `revoke_kills_subtree` revokes per holder.

**Verdict.** **PORT THE IDEA:** the generative-authority closure as Mini's kernel invariant over held capabilities (Mini's
kernel holds caps, so it can be a theorem about the real step, not an abstract graph). **PORT THE CODE then finish it:**
SeL4Kernel's `doomedSet` revoke plus the missing saturation lemma, as Mini's single cascading revoke. **PORT THE IDEA:**
`livingCellA_confinement`'s ceiling invariant; Mandate's tree invariants with the budget enforced by the Book. **STUDY:** the
deposit and refusal channels — decide up front whether Mini accepts credit-without-capability and refusal timing as channels.

---

## 7. Governance and evolution logics

### 7.1 Upgrade (svenvs envelope), CellUpgrade, StateMigration

(LANE-6; READ `StateMigration.lean:125-142`, `Value.lean:98-103`.)
- **Mina anti-brick.** `UpgradeAuth = byProof (v : AirVersion) | bySignature` (`Upgrade.lean:64-69`);
  `setProgramAdmissible live _stored : UpgradeAuth → Prop | .byProof v => v = live | .bySignature => True` (:82-84).
  `bySignature` carries no key, message or signature — it is a constructor tag. `upgrade_never_bricks` (:384) is true
  because that arm is `True`; the file admits the genealogy induction is not load-bearing (`bumpEdge := True`, :330, :377-383).
  **DEF.** The executable `Exec/CellUpgrade.execUpgrade` (:87-92) never checks the actor and leaves `newAirVersion`
  unconstrained.
- **The svenvs envelope.** `SoundPolicy step safe pol := ∀ s a, safe s → pol s a → safe (step s a)` (:178);
  `Admissible step safe oldp newp := SoundPolicy step safe newp ∧ (∀ s a, oldp s a → newp s a)` (:212; the docstring
  says the inclusion runs the other way); `noncomputable def admit … := open Classical in if Admissible … then newp else oldp`
  (:217); `self_improvement_is_safe` (:263) is genuine list + reachability induction (`admit_all_keeps_sound`,
  `invariant_intro`). **REAL as a schema**, but `safe` is a free parameter, `Admissible` quantifies over all states so
  `admit` cannot run, and it is instantiated only on the vacuous genealogy. The idea ("upgrades may widen permissions but
  never leave the safety envelope; for any controller and any proposal stream") is the svenvs result
  (`MEM/project-polis-svenvs-key-insight.md`: "verify the cage, not the animal").
- **Typed state migration.** `Migration { oldSchema; newSchema; reshape : Value → Value }`; only `addField`/`renameField`;
  `migrationOK m v := conforms (m.reshape v) (.record m.newSchema) && (balOf (m.reshape v) == balOf v)`;
  `applyMigration m v := if migrationOK m v then m.reshape v else v`. `migrate_conserves` is the case split on the runtime
  gate. **`migrate_conforms` (:131) needs `hcompat : conforms v (.record m.newSchema) = true`** — that the *old* value already
  conforms to the *new* schema — and the docstring claims this holds for field-add. It does not: `conformsFields` returns
  `false` on a missing field (`Value.lean:98-103`), so `acctV1 = record [("balance",100)]` does not conform to
  `schemaV2 = [("frozen",…),("balance",…)]`. For the file's own `badMig` the gate rejects, the fallback keeps `acctV1`, and the
  cell is left **non-conforming to the new schema** — the data-brick the file says it prevents. Only `balance` is conserved;
  rename has no theorem; nothing wires it to `CellUpgrade`. **HYP (false premise).** Rust has no counterpart; the bare
  `SetProgram` swap is what ran (first report §1.5).
- **Roster reconfiguration is the strongest item here.** `Distributed/ConfigBoundary.lean`'s `classifyStep` is
  byte-transcribed by `B/blocklace/src/constitution.rs:888 config_step_allowed` with a golden test (:1437);
  `churnStepOk_breaks_at_one_one_from_four` (:150, `decide`) shows one join plus one leave at n=4 breaks quorum
  intersection. `EpochReconfig.lean` is differentialed against `federation/src/epoch_diff.rs`. **REAL, RUN/DIFF.**

### 7.2 Polis (constitutions, non-regression, the governor)

(LANE-6; correction memory READ.) The spine (`Polis/Polis.lean`, no imports): `polis_safety` (:102, real induction:
`∀ ctrl n, safe (traj step (envAct pol shield ctrl) init n)` given a sound policy, a safe shield and a safe start —
"verify the cage, not the animal"); `structure Constitution (Agent State) where activeFloor : Agent → Floor State` (:253);
`Amendment := Constitution → Constitution` (:262); `NonRegressive frozenMin am C := ∀ i, ProtectsAtLeast ((am C).activeFloor i)
(frozenMin i)` with `ProtectsAtLeast G F := ∀ s, G s → F s` (:241, :266) — semantic entailment, **not decidable** in general;
`noncomputable def guardedApply` (:273); `amendment_stream_nonregression` (:306, real induction). `frozenMin` is a parameter
outside the mutable record; nothing says who owns it or how it is set. The candidate model `dreggStep _ a := a` (:474) lets
the controller propose the whole next state. `DreggPolis.lean` §2.5 is the one weld to a real step: `execStep k t := (exec k t).getD k`,
`execPol_sound` via `exec_conserves` (:250) — over the toy `Exec.Kernel`. `PolisGovernorTheory.genGov_safe` (:76) is the general
"admit if the post-state satisfies the floor, else stay put" governor. Graded governance (`PolisGrade*`) assumes each amendment is
already non-weakening (`mono` hypothesis) — no gate. `PolisAuthDatalog` instantiates the real `Laws.Verifiable` seam with a
**propositional** 3-rule Datalog (`Atom := Nat`, no variables). The ~20 `PolisSandbox*` files are scripted agents on a
two-agent `Bool → Nat` world, episodes by `decide`.

The 2026-07-06 adversarial review (`MEM/project-polis-unification-correction.md`) holds in code: `governed_holds` is
`D.holds c h` (`Metatheory/Adversary/Schema.lean:82-84`, READ) — a struct projection; the "one adversary" framing adds zero
strength; the DECO "rung 5" is `True True True True True trivial…` (`Metatheory/Adversary/Instances.lean:701-709`) and
`Dregg2/Crypto/DecoUC.lean:3-14` now calls it hollow; `PolisStreamCarrier.polisFloorProp_forall_shape_iff_trivial` proves the
∀-shaped floor admits only `fun _ => True`.

**`polis_governor`** (`M/PolisGovernor.lean`, a `lean_exe`): its MOVE branch runs `govStep` on the two-agent toy; its `pairs`
branch runs `floorPairs`, an unproved function; the bare-list branch is an inline unproved `all`. The only caller is a JS harness
whose `lean` backend sends `pairs` (`B/harness/src/governor/governor.js:126-148`), so **the verified path is never exercised**.
The Rust polis app (`B/starbridge-apps/polis/src/lib.rs`) settles amendments by M-of-N ballot plus a cooling gate and has no
frozen-floor check (first report). **LEAN/TOY; the exe is DOC-grade evidence.**

### 7.3 Epistemic regimes: ResearchRegime, Disputation, OptimisticAdjudication, DreggSolve

- `ResearchRegime.lean`: `Regime = ballot | optimistic | witness` with strength 0/1/2; `Publication` carries
  `honest : renderedAs.strength ≤ settledIn.strength` **as a structure field** (:234-248), so an over-claiming badge cannot be
  constructed; `rendered_witness_is_true` (:255). The header: "Nothing here says any regime is sound." **REAL as a typing
  discipline, light.**
- `Disputation.byzantine_majority_cannot_uphold` (:79) contains no votes and no Byzantine agents: `Frame.verified X w₀` is
  world-constant, so `DistKnows` at `actual` collapses to `Discharged X.stmt w₀` and the theorem says "if no witness discharges X,
  w₀ does not". **DEF.**
- `OptimisticAdjudication.optimistic_sound` (:182) carries `RefutationComplete` and `Actuated := ∀ r, Refuted … r → observed r`
  as explicit hypotheses; the constructive core yields only `¬¬upheld`; `floor_is_satisfiable_and_refutable` (:363) pins both
  poles on toys. **REAL and honest**; its value is naming *actuation* (someone must actually deliver the refutation) as a
  liveness carrier distinct from soundness.
- **Arrow / List–Pettit is cited in prose (`docs/DREGGSOLVE.md:27`, `ResearchRegime.lean:63`) and formalized nowhere.**
  `research/` is empty; nothing runs.
- **Games** (`Metatheory/{SafetyGame,ReachGame,EnergyGame}.lean`, 106/209/375 lines): viability kernel as `OrderHom.gfp`,
  attractor as `lfp`, `kernelShield` ("shield the gfp, not the floor"). **Hole:** `CPre X w := ∃ m, ∀ r, legal w m r → X (step w m r)`
  has no enabledness requirement — a move with no legal response satisfies `CPre X` for every `X`, and
  `PolisDreggGame.dreggGame_cpre_unconditional` (:194-201) exploits exactly that to collapse the kernel onto the floor. Mini's
  ATLAS lists these games under "take verbatim" (§3.6); **port them only with `∃ r, legal w m r` added.**

**Verdict for Mini (fork 4, and multi-party governance).**
- **PORT THE IDEA, and make it decidable (the biggest single upgrade over Bread here):** an upgrade of an object's package is
  admitted iff (a) the new law entails every *frozen floor* the object's kind or its stakeholders declared (Polis
  `NonRegressive`, decided by Mini's entailment check, §2.3 — Bread's was `noncomputable`), (b) the new law is sound for the
  object's declared safety envelope (svenvs `Admissible`, with the certifying checker supplying the soundness certificate
  instead of `Classical`), and (c) a typed migration `V_old → V_new` is total and checked by the certifying type checker, with
  per-field conservation laws checked by entailment. **Reject** the upgrade turn on failure; never fall back to the old value
  under the new schema (Bread's data-brick).
- **PORT THE IDEA:** frozen floors live outside the amendable record and are owned by named subjects; amendments are inert
  unless non-regressive; "what the proof does not need, it does not ask to see" (`project-polis-svenvs-key-insight.md`).
- **PORT THE IDEA:** `Publication.honest` for every badge Mini renders (re-executed / condition-witnessed / optimistic / voted).
- **PORT THE CODE:** `ConfigBoundary.classifyStep` and its n=4 churn refutation, if Mini's Simplex committee can change roster
  (n=4, f=1 is exactly the case it refutes).
- **AVOID:** `upgrade_never_bricks`/`bySignature` as authorization; `StateMigration` as written; graded non-regression without a
  gate; citing `byzantine_majority_cannot_uphold`, the Arrow claim, `governed_holds`, or the `polis_governor` binary as results.

---

## 8. Distributed, consensus and async metatheory

### 8.1 What the node actually lets Lean decide (the good news)

(LANE-7.) Bread's most successful pattern: a small decision exported from Lean, a `*_eq` theorem that the export is the model
function after decoding (`unfold; rw [h]` — a marshalling identity), a fail-closed disposition in Rust, and declared, named
bypasses that `DREGG_REQUIRE_LEAN=1` revokes.

| export | node call site | role |
|---|---|---|
| `dregg_tau_order` | `node/src/blocklace_sync.rs` (`verified_tau_order`), `lib.rs:2995` | authoritative finalized order — but the executed code is `@[implemented_by tauOrderFastImpl]` (`BlocklaceFinality.lean:1373`), trusted, not kernel-checked |
| `dregg_blocklace_finalize` | `node/src/finality_gate.rs:230` | fail-closed belt check; skipped at n=1 |
| `dregg_finalization_quorum` | `node/src/finalization_votes.rs:1080` | authoritative; node refuses to start without it |
| `dregg_round_advance` | `node/src/round_advance_gate.rs:160` | authoritative; HOLD on error |
| `dregg_ack_admit` | `node/src/catchup.rs:598` | authoritative only in fork context |
| `dregg_strand_admit` | `node/src/strand_admission_gate.rs` | authoritative in form, near-identity today (seeds = constitution participants) |
| `dregg_coord_2pc_decide` | `coord/src/atomic.rs:341`, `node/src/coord_gate.rs:320` | **authoritative Commit/Abort/Pending verdict** for `/turn/atomic` |
| `dregg_coord_causal_order`, `dregg_coord_shared_budget` | coord crate | tests only / not wired to node |
| `dregg_captp_validate_handoff` | captp | authoritative, refuses without the gate |
| `dregg_captp_process_drop`, `…_pipeline_resolve` | captp | advisory; native verdict decides |

The proofs under these are mostly quorum arithmetic (`QuorumThreshold.supermajority_intersection`,
`BlsQuorumCert.two_quorums_share_member`, `FinalizationQuorum.quorum_no_conflict`) — **REAL, and they match n=4, f=1 exactly** —
plus `RoundAdvanceGate.advance_iff` (leader clause or timeout > Δ, never bypassing cordiality),
`LaceMerge.merge_comm/assoc/idem` (the replication CRDT, ALREADY IN MINI as `Theory/LaceMerge.lean`), `CrashRecovery.recover_eq_replay`,
`ConsensusTimeAck.executeFinalized_ignores_local_clock`, `ConfigBoundary` (§7.1). The finality gate is also where Bread's worst
silent failure happened: hybrid identity changed what `block.creator` means and seven consumers failed silently into a wedged
consensus at height 0 (`MEM/project-finality-gate-open-unenrolled.md`). `Consensus/TauPrefixMonotone.tau_finalized_prefix_monotone`
(:654) honestly assumes `ChainExtends` (Cordial Miners Prop 9), still owed.

### 8.2 2PC and joint turns

- **2PC** (`Coord/TwoPhaseCommit.lean`): `Tally {yes no n threshold}`; `evaluate t := if t.threshold ≤ t.yes then commit else if
  t.n - t.threshold < t.no then abort else pending` (:125); `evaluate_not_commit_and_abort` (:144, `omega`),
  `abort_no_late_commit`, `commit_stable_under_more_yes`. It counts one coordinator's tally: no messages, no crashes, no
  participant prepared/locked state; the gate does not check `wf`, so `threshold = 0` commits (Rust guards supply `wf`). What the
  commit *does* is Rust (`active.coordinator.commit(&mut s.ledger, height)`). **REAL-small, RUN.**
- **JointTurn** (`JointTurn.lean`): a joint turn is the equalizer of the participants' step maps over a shared turn id, needing
  CG-2 (`SharedTurnId`) and CG-5 (`balanced : half₁ + half₂ = 0`) as a *premise* (:105-115). Confirmed (LANE-7, and the first
  report READ): `binding_is_proper` (:271) is 1+1≠0 in ℕ over two `Unit` coalgebras; `atomicity_as_proof` (:328) is `and_congr`
  (`willSucceed` is defined as the conjunction); `joint_sound` (:186) uses the binding only to name the start state. The file still
  cites a `tensor_not_final` theorem that does not exist (:102, :122, :241), a claim `project-dregg4-vision.md` records as
  false-as-stated. `JointCharterBridge.charterBind` inhabits the "irreducible" CG-2 binding by `rfl`. `EntangledJoint.jointApplyAll`
  is an N-leg all-or-none fold over **one** kernel state (`jointApplyAll_atomic`, `_conserves :245` — real, but atomic over one
  state, which is the easy case) and is only a differential in Rust. **DEF/TOY.**
- **Hyperedge** (§1): the N-ary generalization with real ring-telescoping and validity≠canonicity content.

**Verdict for Mini.** **PORT THE CODE:** `evaluate` + `evaluate_not_commit_and_abort` with `wf` inside the gate, then extend the
model with per-participant prepared/locked state and coordinator crash, for cross-domain atomicity. **PORT THE IDEA:** the
CG-2 ⊗ CG-5 decomposition (one shared invocation id across domains + Σδ=0 across the legs) as the *statement* of a cross-domain
atomic invocation; on one Host it is the single-machine case (one state, synchronous, no 2PC — `EntangledJoint`'s easy case is
exactly right there), and on a committee boundary it is 2PC with escrow locks. **AVOID** citing `atomicity_as_proof`,
`binding_is_proper`, `joint_sound`.

### 8.3 The single-machine principle and the fibration

Ember's design requirement (`MEM/project-dregg4-vision.md`, 2026-06-01): "when running my single-machine node, I want
single-machine properties, NOT be forced into distributed-properties" — every distributed bound is parametrized by topology and
collapses to the strong property at n=1. The formalization (`Distributed/Fibration.lean`, READ :205-225): base
`B = Topology × FaultModel × CryptoStrength`; `structure Fibre P { bound : B → Time; holdsAfter; apexZero : ∀ b, IsApex b → bound b
= 0 }`; `lift_collapse` reads `apexZero` back out ("DEFINITIONAL … NOT a new theorem", the file says). LANE-7: FaultModel and
CryptoStrength never affect any bound; every fibre's bound is `b.topo.delay m n`. `Revocation.eventual_bounded_revocation` (:188)
follows because each node's view is *defined* to contain exactly the propagated events; the promised explicit `Propagates`
hypothesis does not exist. `Finality.Tier` (`causal < ackThreshold < bft < constitutional`), `commit_at_join_of_tiers` (the
commit tier is the max of the touched tiers) and `no_downgrade` (an invariant of a step relation defined as `≤`). **DEF.**
`Firmament/CapGradation.distributed_collapses_at_one` is a definitional equality.

**Verdict.** **PORT THE IDEA (it is Ember's own requirement, and Mini's architecture already embodies it):** state every
coordination bound as a function of the deployment (single Host: synchronous cross-object atomicity, immediate revocation, one
order; committee domain: BFT finality; multi-party: 2PC + escrow), and let a cross-domain commit take the max tier it touches.
**Rebuild the code** so the bound actually depends on (f, synchrony model), and revocation carries an explicit propagation
hypothesis.

### 8.4 Concurrency: commutation, contention, bounded counters, justness

- `Proof/ContendedCrossCell.lean:176`, `Proof/ContendedForest.lean:279`, `Consensus/OnDemandFeasibility.lean:122,158`: disjoint
  debits commute, contended forests reach the same outcome, joins commute while revoke/exercise do not (first report, LANE). Nothing
  schedules with them. **REAL, LEAN.**
- **Stingray** (`Proof/Stingray.lean`): `sliceCeiling b f := b*(f+1)/(2f+1)` (:103); `stingray_no_concurrent_overspend` (:309) is
  an ∃ over one concrete slice showing two orders give different verdicts; multi-silo Σ ≤ balance is not proved;
  `StingrayCertReconcile.byzantine_undetected_overspend_le_f_ceiling` (:355) is list arithmetic not tied to `rebalance`;
  `CertUnforgeable` has no instance. The Rust `StingrayCounter` is live in node state; the Lean is differential only. **TOY.**
- **Justness** (`Proof/Fairness.lean`): `SchedA := Nat → ConservingForest` applied to **one** living cell; van Glabbeek
  B-justness `Just B s sched := ∀ k cf, NonBlocking B cf → Commits … cf → ∃ n ≥ k, interferes cf (sched n)` (:219);
  `just_progress` (:349) by strong induction on a measure carried in `JustProgress`. The rationale is sound and preserved in
  `M/docs/HARVEST-KEEPERS.md`: weak/strong fairness overcommit and fair schedulers cannot be implemented in reactive languages;
  justness is feasible and survives refinement. **REAL, TOY scope.**

**Verdict.** **PORT THE IDEA (fork 3):** commutation/contention as the scheduler's classifier (independent invocations commute
and may run in parallel; coupled over-draw must be ordered), escrow/bounded counters as the pattern for many activities on one
balance (with `CRDT.escrow_refinement` as the proved local-quota law), and **justness** as the liveness property Mini states
for its activity scheduler. **STUDY** the Lean Stingray; build Mini's version over separate silo states.

### 8.5 Await, CapTP, ConditionalTurn, continuations

- **`Await.lean`** (READ :100-112, :244-290): `Op = await p | call c | emit e`; `Computation = ret a | op Reply o kont`;
  `structure OneShot (R S) where run : R → S` — `run` is a public field and Lean is not linear, so one-shotness is a convention,
  not enforced; `turnAsRollbackHandler … (resumeWith : (Reply : Type u) → Reply)` — **that type is uninhabited** (take
  `Reply := PEmpty`), so `commit_resumes_once` and `rollback_discards_continuation` can never be applied to a real handler;
  `four_faces_unify` is `⟨rfl, fun _ => rfl, rfl⟩` over three of the four faces; there is no fold semantics of handlers over
  `Computation`. **HYP/DEF.** ATLAS-era readers took the Plotkin–Pretnar vocabulary at face value; Mini's activity (perform/yield/resume
  with an exact checkpoint codec) is the executable thing this file only named.
- **`Spec/Await.lean`, the "dataflow half"**: `PromiseGraph {nodes : Finset; dep}`, `Acyclic`, `pipeline_topological` (:350, a real
  Szpilrajn/`Finset.sort` topological-order proof — generic DAG content); `broken_promise_propagates` takes as hypothesis the
  contrapositive of its conclusion; the `fulfilled` flag is unused; `resolve_monotone` keeps the clock fixed, so a resolved
  conditional becomes `Expired` later (no latch).
- **CapTP**: `pipelining_preserves_seam` is `Iff.rfl`; `CapTPPipeline.drainAll_preserves_caps` holds because `Exec.Kernel.exec`
  only rewrites balances, never caps (`Kernel.lean:69-74`).
- **ConditionalTurn**: `Slots := Nat → Bool` (:109) — no value flows; `condTurn_dependency_sound` (:417) states membership
  (`c ∈ order → order.contains p`), not precedence, although its docstring says "producer precedes consumer".
- **What is real and right**: `ReactiveRegistry.no_double_react` (:221) enforces one-shot resumption with a spent-nullifier set,
  and `Exec/Continuation.yield_resume_sound` (:82) is `List.foldl_append` (a mid-turn boundary is not independently committable).

**Verdict for Mini.** **AVOID** `Await.lean`/`OneShot` as code or as evidence. **PORT THE IDEA:** one-shot resumption enforced by
a spent set (the await id is a nullifier spent by the resuming turn and bound to the checkpoint digest — the first report's
recommendation, confirmed); **PORT THE CODE:** `pipeline_topological` if Mini needs a static order for a batch of dependent
invocations; **re-prove** CapTP-style no-amplification over Mini's real Plan application, which *can* grant.

### 8.6 Vat boundaries

`Exec/VatBoundary.vatAdmits` (:67): if `crossing` then the token must admit the request with discharges, else the cap check;
`vat_boundary_law` maps the branches onto `Integrity.cross/intra` — but `crossing : Bool` is a caller-supplied field.
`Spec/VatBoundary.phi_drops_confinement` (:205) concludes `PermissionSurvives ∧ ¬ AuthoritySurvives` from a discharging and a
non-discharging witness, with `PermissionSurvives := ∃ w, …` and `AuthoritySurvives := ∀ w, …` — it restates its hypotheses.
**DEF.** **PORT THE IDEA** (first report): a domain boundary is where kernel-held capabilities become presented tokens; Mini should
derive "crossing" from the domain of the target object, never accept it as a flag.

---

## 9. OS-level models: deos, affordances, documents, reversibility, firmament, intents, time

### 9.1 Affordances and per-viewer projection (the presentation layer)

(LANE-8; READ spot-checks.) `Deos/Affordance.lean`: `fireGate required held := required.all (held.contains ·)` (:97);
`CellAffordance {required : List Auth; effect : φ; name : Nat}` — the name is "a DISPLAY LABEL and nothing else" (:145);
`FireCtx {effectDigest; prevDigest; pre; post}` (:162); `fire` returns a receipt whose `boundRoot` is the new commitment;
`projectFor held affs := affs.filter (fireGate ·.required held)` (:385); `fire_authorized_iff_subset` (:251) rests on
`fireGateR_iff_subset` (:103). The file is candid: an earlier version proved `post = post` with the receipt discarded (flag-day
note :16-36; `Claims.lean` §39 records that the "four deos theorems ALL DISCHARGED" were definitional and one an identity
carrier). `GatedAffordance` (:102-151): `gatedOK := fireGate … && stateCond.admitsCtx ctx method old new` — capability ∧ law.
`Reactive.TransitionGate {pre; post; link}` (:104) and `ReactiveAffordance {aff; gate; openHeight; closeHeight}` (:138) —
capability ∧ (old,new) transition ∧ time window. `Viewer {held; permits}` with `membraneShows` (:359-370): authority and
disclosure as two independent axes. `FireProgramAgreement.installedProgram_gate_eq_surface_stateGate`: the surface gate and the
executor gate reduce to the same `cs.all (evalConstraint · old new)` — **but the Rust surface evaluates at `(s, s)` and the
executor at `(s, s')`** (`B/deos-leptos/src/gate.rs` `state_ok`), so preview and commit verdicts can diverge.
**REAL, small, LEAN**; the Rust (`starbridge-web-surface/src/affordance.rs`) is a hand-written twin that drifted
(`required_rights : Requirement` lattice vs `List Auth`; `AffordanceIntent` carries no receipt).

`FogOfWar.noninterference` (READ :145) is `:= hagree` because `agreeOn` is *defined* as view equality; the content is
`hidden_change_invisible`. `HIG.md` says ungranted affordances are "visibly dim, not hidden", contradicting `projectFor`.

**Verdict for Mini (presentation = a projection).** **PORT THE CODE (small):** `CellAffordance`/`fireGate`/`projectFor` and
the gated and reactive variants, with the post-flag-day receipt commitment (commit to the effect digest, never a display
name). **PORT THE IDEA, fixed:** give the *preview* judgement (law evaluated against the current state and a candidate
transition, or "would admit now" via Mini's satisfiability check) and the *commit* judgement distinct, related types so they
cannot silently diverge; and prove "the card cannot be bypassed" as equality of the projection's gate and the kernel's law (one
function, two call sites). **Decide** dim-vs-hidden as a disclosure policy per viewer (FogOfWar says hidden cells must be
structurally absent).

### 9.2 Documents, merge, transclusion, branch-and-stitch

- **DocMerge** (`Deos/DocMerge.lean`): `Status = alive | dead` with dead absorbing; componentwise `merge` (:183); `merge_is_lub`
  (:355, REAL); `ConflictAt` (:394) — two live, mutually unreachable atoms after a shared point — **conflict as first-class state**;
  `prose_iconfluent` vs `field_not_iconfluent`. DocPatch: additive ops commute; `addEdge_is_merge`. DocMergeComposed: a composed
  document merges as a product of pushouts (`boundary_no_joint_conflict`). The thin-order `IsPushout` (:651) has a genuine
  universal property. **REAL.**
- **PatchCategory** (READ :283): `IsPushoutUpToIso c a b d := c ⊑ a ∧ c ⊑ b ∧ a ⊑ d ∧ b ⊑ d ∧ IsoP (merge a b) d` — *defined*
  as iso-to-merge, so "merge realizes the pushout" is `IsoP.refl`, not a universal property over patch morphisms. Do not cite it as
  Mimram–Di Giusto. The `categoryP` instance is a genuine Mathlib category.
- **Transclusion** is a renaming of `ImportedEq` (§6.4); `AnchoredQuote` admits Transclusion's anti-forge rests on an abstract
  total `stateAt` "asserted by the model, not proven", and adds signature unforgeability and injectivity as named hypotheses.
  `TRANSCLUSION.md` lists Backlinks as proved; no declaration exists.
- **BranchStitch**: `BranchHonest := Confined M caps author`; `Stitch m b s := m ⊑ s ∧ b ⊑ s ∧ …`; `branch_cannot_drain_main` reuses
  `confined_cannot_debit_attacker`; it honestly carries `branch_may_signal_main` (integrity, not confidentiality). The doc says a
  branch is `Virtual`-typed; no such variant exists in Lean or Rust.
- **Settlement soundness** (`Metatheory/SettlementSoundness.lean:153`): `settlement_soundness := hbind … hsettled` is hypothesis
  application; the content is `deployedSettle_binds_live_authority` (:305) with the negative `branchSettle_NOT_binds` (:408):
  authority is evaluated at the settlement tip, not at branch time (revocation is the one non-monotone operation). Wired to the
  host-layer `stitch_pair` (`MEM/project-distributed-houyhnhnm-frontier.md`).

**Verdict.** **PORT THE CODE:** DocMerge/DocPatch (merge as LUB with dead-wins, conflict as state, prose-vs-field I-confluence) as
the model for mergeable text inside Mini objects. **PORT THE IDEA:** composed documents merge componentwise; a quote/transclusion
is an import pinned at a receipt; fork-a-world for residents is a confined branch whose stitch is a LUB evaluated with authority
*at the settlement tip*. **AVOID** the patch-category pushout claim and the Backlinks claim.

### 9.3 Reversibility and time travel

The three tiers live in Rust only: `B/turn/src/reversible.rs` (2,495 lines) `Inversion::{Clean, Contextual, Committed}` (:193),
`Effect::invert(&self, pre)`, `ReversibleHistory::{undo_to, replay_to, fork_at}`; `undo_to_lands_on_the_same_verified_state_as_replay_to`
passes modulo the nonce ratchet; `demo/tests/time_travel_houyhnhnm.rs` (rewind, branch, refuse across the nonce). The doc
(`B/docs/deos/FIRST-CLASS-REVERSIBILITY.md:87-96`) says "the Rust round-trip is a test, not yet a proof"; `EffectInvert.lean` does not
exist. The theory frame (`DISTRIBUTED-TIMETRAVEL-SEMANTICS.md`): a branch is a configuration of an event structure, the cap gate is
RCCS consent, settlement is a preferred maximal configuration, and the right frame is RCCS with irreversible committed actions.
`Rehydration.lean` labels a reconstruction `Live | ReplayedDeterministic | ReconstructedApproximate` from the log;
`replayedDeterministic_iff_confined` (READ :163) unfolds the `if` (**DEF**); `ReplayMembrane` restates C1 after an earlier keystone
was "literally `:= rfl` with the confinement premise unused" — replay is a function of the witnessed inputs alone.

**Verdict.** **PORT THE IDEA, then prove it in Lean:** every Plan action kind declares its reversibility tier as a total match;
Mini can prove the round-trip for Clean and Contextual actions cheaply (the inverse is a Plan, re-executed). **PORT THE IDEA:** the
rehydration label as the honest "which kind of true is this card/checkpoint" badge. Mini's exact checkpoint codec already makes
replay deterministic; ReplayMembrane's statement (replay depends only on witnessed inputs) is the property to state about it.

### 9.4 Firmament, mirrors, the reflexive substrate

`Firmament/CapGradation.lean`: one `Capability { target : Local | Distributed | Surface }`, `no_amplification`, the n=1 collapse.
`SeL4Abstract/SeL4Kernel/SeL4Composition`: an l4v-pinned transcription of endpoint/notification/mint/revoke/retype with the only
transitive revoke (§6.5) and `dregg_turn_in_pd_preserves_both`. `NotifyAuthority`/`NotifyOrgans`: a notify capability that confers
no write edge (wake ≠ write), with pubsub, inbox and event emission as one notify authority. The mirror capability
(`Target::Mirror`, Bracha–Ungar mirrors) is **unbuilt** in the firmament; the reflexive tower and Suspend are built in
`starbridge-v2`; the moldable inspector (`starbridge-v2/src/presentable.rs`) shipped. The stratified-fixpoint verdict
(`MEM/project-moldable-inspector-epoch.md`, `docs/deos/STRATIFIED-FIXPOINT.md`): the only non-monotone part of `present` is the
authority refusal, which points down the attenuation tower, so capability strata are dataflow strata **provided `present` stays pure**.

**Verdict.** **PORT THE IDEA:** reflection is a held capability over a subgraph (a mirror), checked by the kernel; keep the projection
function pure so authority strata stratify the reflexive fixpoint; a notify capability that can wake but not write. **STUDY** the
seL4 transcription (out of Mini's scope).

### 9.5 Intents, time, and the rest of the OS models

- **Intent** (`Intent/*`): four-faced `Intent` (boundary, predicate, escrow lockbox, `Deadline`); `Lifecycle` publish/fulfil/refund on
  the real ledger with `fulfilled_then_no_refund`; `Ring.settleRing` folds `recKExecAsset` atomically with `settleRing_conserves`
  and `cycle_individuallyRational`; `RingFFI.ffi_export_realises_settleRing_leg` ties to `@[export dregg_record_kernel_step]`,
  consumed by `B/intent/src/verified_settle.rs` — **one of the few genuine Lean→Rust execution paths (RUN)**. `Match` builds a real
  Mathlib coend `∫^B`. "receipt⊣intent" has no adjunction behind it.
- **Time** (`Time/{Causal,Frame,Deadline}.lean`): `CausalAfter := precedes` (frame-invariant); `FrameWithin` carries an explicit
  skew δ and a `FrameHonesty` carrier; the `Deadline` sum type forces the causal/frame distinction; `commit_wait_bridge` (waiting 2δ
  upgrades frame time to causal) and `commit_wait_needs_full_2delta`. **REAL, small.**
- **Widget**: proof-trust badges from `Lean.collectAxioms` (sees axioms, not hypotheses — a theorem over the refuted
  `Poseidon2SpongeCR` still shows green).
- **Capacities as cell programs** (`DerivedCell`, `StandingObligation`, `PrepaidLease`, `SealedEscrow`, `Vault`): good catalog
  (derived = f(sources), one-shot schedule cursor, fused meter+draw, 2-of-2 one-shot, non-diluting share price); their Lean binds
  through a 1-felt heap root whose honest strength the files state as "≈ 2^15.5 … a BREAK, not a bound".

**Verdict.** **PORT THE IDEA:** Intent Lifecycle (publish/fulfil/refund, no refund after fulfil) as the AI-to-AI contract shape;
the Ring's atomic multi-party settlement fold; the capacity catalog as *standard library laws* re-proved over Mini's state.
**PORT THE CODE:** the `Deadline` sum type and `commit_wait_bridge`. **PORT THE IDEA:** a proof badge on every card, built from a
hypothesis/carrier ledger, not from `collectAxioms` alone.

---

## 10. The adjunction thesis and its replacement; other experiments

**The thesis** (`MEM/project-adjunction-thesis-verdict.md`, READ): "agreement and adjudication are the two adjoints of ONE
(Predicate⊣Witness) adjunction" (2026-06-01). A four-lens adversarial workflow scored the load-bearing claim **BROKEN 4/4**:
`Predicate⊣Witness` (the `Seam` in `Laws.lean`) is a single-agent preorder closure; the CRDT join is a colimit and the *easy*
side, while the FLP-hard object (common knowledge C_B) is a greatest fixpoint, a limit — "polarity backwards, refuted by our own
repo"; the real axis is CALM (monotone vs non-monotone); three knowledge modalities had been conflated; and
`adjudicate := mate-of-DistKnows` is false ("adjoint-functor-theorem obligation = Arrow in disguise").

**The replacement** (LANE-8, LANE-3): a Lawvere hyperdoctrine. `Metatheory/Lawvere.lean:100-115`:
`existsAlong_adj_reindex (f) : GaloisConnection (existsAlong f) (reindex f) := Set.image_preimage`,
`reindex_adj_forallAlong`, `lawvere_triple` (thin wrappers over Mathlib on `Set`) plus Frobenius, Beck–Chevalley, and
counterexamples (`beck_chevalley_fails`, `no_galois_with_nonmonotone_reindex`); Part B (:323) `relExists_adj_relForall R` for
any relation, a real hand proof, with counterexamples (S4 fails for a reflexive-only Byzantine relation, `box_box_ne_box`).
`IndexedMonoidal.lean`: monoidal fibres over a walking-arrow base; only the lax Frobenius `⊆` holds. Adjudication is a
*separately built, regime-graded reflector* — in practice the per-regime predicates of §7.3 (`Disputation.upheld X := Holds X`;
optimistic; ballot). No general graded-reflector structure exists. **REAL as small order theory; the research value is the
verdict itself.**

**Verdict.** **STUDY**, and keep the verdict's one design consequence: Mini adjudicates by *witness* (decide only certifiable
claims; `upheld X := ∃ w, Verify X w`), never by vote, and labels anything settled otherwise with its regime (§7.3). Do not
adopt "one adjunction" language.

**Other experiments, one line each.**
- `Metatheory/Open/FinalCoalgebra.lean`: `nuF = List Adm → Obs` as a constructive final coalgebra, `no_drift_into_nuF` —
  ATLAS take-list §3.15; **STUDY** ("an object's identity is its observable behaviour").
- `Apps/` (66 files): the verification toolkit (§4), ~60 app models; ATLAS measured ~75% as five mechanical moves repeated per
  app. **AVOID** as a pattern.
- `Games/` (188 files: Automatafl, Dungeon, PathOfAngels, private-descriptor games) and `Market/` (~100: DrEX, dark AMM, FHE
  clearing): out of scope for the program model; Mini decided "Games/: skipped" (ATLAS §8.5).
- `Circuit/` (1,142 files, 714k lines), `Crypto/` (308), `Bridge/`, `Lightclient/`, `Bfv`: the proof-system arm. Out of scope
  for Mini admission (no proof system); the two arithmetization counterexamples (§3.5) and `Dynamics/Initiality.compile_not_a_seq_hom`
  are the parts Selvage should read.
- `Crypto/Deriv/` beyond §2.3: guards for a templater (`HandlebarsGuarded*`), derivative regex decision tower; **STUDY** for
  multi-step law shapes.
- `Calculus/Biorthogonality.lean`: guards as biorthogonally closed behaviours tested by the live evaluator; **STUDY**.
- `Paco/`: vendored parametrized coinduction (license header mismatch); one consumer; **STUDY**.
- `EffectAlgebraSketch.lean` (metatheory root, "UNELABORATED … has NOT been run", nothing imports it): names the trap of
  per-write versus whole-transition caveats with delta factoring and `dstep_comm`. **STUDY closely**: Mini's law judges the
  whole (old, new) of each object per turn; say so in the spec.

---

## 11. Where this report confirms, corrects or extends the first report and Mini's ATLAS

**Corrections to the first report** (`SCHOLAR-BREAD-PROGRAM-MODEL-20261004.md`):
1. "Satisfiability and explanations: none … no `satisfiable`/`subsumes`/`equiv` procedure exists" (§1.3) — **wrong for Lean**:
   `Crypto/Deriv/SymbolicDifference.lean` proves a DBM decision procedure and emptiness/equivalence decisions (§2.3). Right for
   Rust and runtime: nothing runs it. Mini's `Pred/Satisfiable.lean` is ahead regardless.
2. "`TurnAdmission.lean` and the FFI step call `execHandlerTurn`, but I did not establish that the node's producer runs it" —
   **established: it does not.** Its export is called by one Rust test; the node runs `execFullForestG` (§5).
3. "deadlock-freedom on the non-recursive fragment" for the MPST layer (§1.3) — the theorem is about the global type's own
   reduction; `Dual` ignores roles and labels; `Projectable` is never used (§1).
4. The Hatchery "Lean rung proves `step_preserves` + `CellContract.forever`" — that rung is a two-case `List ℤ` toy, a different
   `CellContract` from the one in `Verify/Contract.lean` over the real executor (§4).
5. Upgrade: add that `StateMigration.migrate_conforms` rests on a premise false for its own field-add migration, so the
   fallback leaves a non-conforming value (§7.1), and that `polis_governor`'s verified branch is never exercised (§7.2).
6. FlowRefine "decidable flow refinement … the algebra is right-skewed, Pradic's RSKA_d⊓": the decision is real but on a
   guard-free, iteration-free fragment where Pradic's machinery is unused; most right-skew laws are unproved (§2.6).
7. Confirmed at source: `four_faces_unify` is an extraction identity, `CapTPPipeline` no-amplification is by construction,
   `ConditionalTurn` slots are Booleans, `binding_is_proper` is 1+1≠0, `atomicity_as_proof` is `and_congr`. Added: `Await`'s
   handler theorems have an uninhabited premise (`resumeWith : (Reply : Type u) → Reply`) (§8.5).

**Corrections and caveats to Mini's ATLAS (`MINI/ATLAS.md`, 2026-08-06)**, which took several items "verbatim":
- §4 "MPST choreography surface (`DSLChoreo` — inherited deadlock-freedom + privacy-by-projection)": the inherited
  deadlock freedom is head duality over global-type residuals, not endpoint progress (§1). Port the types; build the monitor.
- §3.6 games "take verbatim": `CPre` lacks enabledness, and Bread's own `PolisDreggGame` exploits it (§7.3). Add `∃ r, legal w m r`.
- §3.2 `GovernedDynamics`/`governed_holds` "take verbatim": a struct projection (`D.holds c h`); keep it only as a statement
  template, with ATLAS's per-instance accept-satisfiability obligation doing all the work.
- §3.3 "four-substance product camera + `Verb = admission × footprint-Fpu`": Bread's own FpuProbe demotes it — Fpu over ℤ is
  vacuous, conservation enters only through a validity-is-invariant camera, and the honest skeleton is "two gates" (§6.1).
- §3.7 "the gate + executor core: four-leg `gateOK` (credential ∧ cap-authority-in-Lean ∧ caveats ∧ revocation)": on the live FFI
  path every root's cap-authority leg is `.unchecked (Guard.all [])` and `chain := none` (`GatedForestCfg.lean:107-110`,
  `FFI.lean:2326,2353`, READ); only delegation edges check `keep ⊆ parentCap`. Port the gate *and* make every leg load-bearing.
- §3.9 Hyperedge "with its three negative theorems": confirmed; add that `hyperedge_sound` never uses `agree`/`balanced` (§1).
- §3.14 the deos crown: `replayedDeterministic_iff_confined` is an `if` unfolded and `FogOfWar.noninterference := hagree`
  (§9); the membrane non-amplification and DocMerge LUB are real.
- §1 "`VerbCompression` proves the kernel is 3 verbs": the minimality theorems prove a hand-assigned label table injective; the
  separation theorems are the real content (§5).
- Things ATLAS did not list that Mini should still look at: the triangle refinement (§3.2), the decidable-upgrade composition
  (§7), import vs live read (§6.4), the `doomedSet` revoke (§6.5), the coordination ladder's escrow rung (§2.5), the
  preview/commit gate divergence (§9.1), the reversibility tiers (§9.3), `escrow_refinement`, and the 2PC model's missing
  participant state (§8.2).

**Already in Mini** (redesigned ports I found by grep; not re-audited here): `Theory/Confluence.lean` (from `Confluence.lean`
and `ConfluenceClassifier.lean`, without the `Iff.rfl` synonyms), `Pred/CoordinationDial.lean` (a computed, proved dial Bread
never had), `Pred/Satisfiable*.lean` (executable, certificate-producing), `Pred/BoundedQuantifiedView.lean`,
`Theory/LaceMerge.lean`, `Theory/Finality.lean`, `Theory/{Knowledge,EpistemicConsensus}.lean`, `Theory/Hyperdocument*.lean`,
`Theory/RevocationConsensus.lean`, `Theory/AssertAxioms.lean`, `Theory/AssertCompiled.lean`.

## 12. What I read versus relied on

READ myself: the brief; the first report and ROOT's notes in full; `MINI/ATLAS.md` §0-8; MEM files (dregg2 architecture, three
projections, statement audit, verified-system retraction, adjunction verdict, dregg4 vision, Houyhnhnm frontier, rhizomatic,
three-faced turn, drift spectrum, FFI, coverage map, lean-must-be-the-implementation, proven-in-Lean-not-routable, Polis
correction, svenvs, DreggSolve, identity-carrier and exists-image classes, handler floors); `M/docs/{HARVEST-KEEPERS,KEYSTONE-LEDGER,
TEACHING-USABILITY-FRONTIER,DISCARD-CANDIDATES}.md`; `B/HATCHERY.md`; `B/docs/DESIGN-symbolic-decidability-status.md` §1;
`Apps/VERIFICATION-TOOLKIT-GUIDE.md`; at source: `Spec/Authority.lean:430-660`, `Boundary.lean:140-200`, `Exec/Cell.lean:40-130`,
`Confluence.lean` whole, `Exec/CellProgram.lean:94-108`, `Projection.lean:1-133`, `Coordination.lean:355-385,690-715`,
`Crypto/Deriv/SymbolicDifference.lean` header, declarations, `:455-475` and its closing section, `PredicateLibrary.lean` header,
`DSL.lean` header, `Exec/StateMigration.lean:125-142,270-290`, `Exec/Value.lean:95-103`, `Spec/WholeTurnTriangle.lean:184`,
`FlowAlgebra.lean:119-135`, `FlowRefine.lean:355-382`, `Await.lean:100-112,244-290`, `Fibration.lean:205-225`,
`Resource.lean:100-112,316-322`, `GatedForestCfg.lean:104-112`, `FFI.lean:2320-2360`, `ThirdPartyDischarge.lean:224-232`,
`FogOfWar.lean:136-152`, `PatchCategory.lean:283`, `Rehydration.lean:163`, `Apps/BountyBoardForever.lean`, `Metatheory/Adversary/Schema.lean:50-100`,
`Exec/EffectCommit2.lean` header; greps confirming every handler `delta := 0`, `masterRegistry` only in a length lemma, the
handler export's only Rust caller, root reachability of the main modules, and Mini's ported modules (`MINI/Pred/{Satisfiable,
CoordinationDial,LawComposition,BoundedQuantifiedView}.lean`, `MINI/Theory/Confluence.lean` headers).
LANE (eight read-only Opus Explore sub-readers; `file:line` reported): everything marked LANE-n. I re-checked at source one or
more headline claims from every lane (listed above) and all held.
ASSUMED by me: that the node binary that matters is the one built from HEAD with Lean linked (the code says Lean is
unconditional on native; `MEM/project-twin-deletion-campaign.md` says a deployed node once ran without it).

---

## 13. Synthesis

### The ten most valuable things in Bread's metatheory for Mini, in priority order

1. **Governed upgrade as a decision (fork 4).** Compose three Bread pieces that never met. Polis's frozen floors make an
   amendment inert unless every subject's frozen minimum is still entailed (`Polis.lean:241-313`). The svenvs envelope admits a
   new policy only if it is sound for the safety envelope (`Upgrade.lean:178-269`). The migration gate checks the reshaped state
   against the new schema and conservation (`StateMigration.lean`). In Bread all three were `noncomputable` or rested on a false
   premise, and none ran. Mini can decide them. It has entailment (`unsat(A ∧ ¬B)` with a certificate), and its certifying
   checker can check that `migrate : V_old → V_new` is total and typed. Upgrade is then one admitted turn: refuse on failure,
   never fall back to the old value.
2. **Obligation-carrying action and object kinds.** `EffectHandler` makes a handler ill-typed until `auth_gated`,
   `admission_gated` and `conserves` are proved (`Exec/Handler.lean:70-87`). `FloorObligation` names every other floor
   (`HandlerFloors.lean`). A package that adds a Plan action kind or an object kind should carry these as fields that the
   checker discharges. The dispatch must really index the registry; Bread's moved the 56-arm match. A kind's law must be the
   cell's law by construction, so factory transparency and upgrade are one rule, not Bread's two contradictory ones.
3. **The triangle contract for the kernel itself.** For each action, `exec s a = some s' ↔ gate s a ∧ s' = spec s a`, against
   an independently written spec with an explicit frame, folded to the turn (`execFullForestG_iff_turnSpecG`). Add
   `running_entry_sound`'s floor-free conjunction (conservation ∧ non-amplification on every edge ∧ the gate invariant) and
   `reachable_total_zero` for the Book, with issuer wells. These are the most contentful Bread theorems about the code it ran.
4. **A choreography as a protocol object (fork 1, rich calls).** Port `GlobalType`, `project` and the `dregg_choreo` notation
   as code, but do not rely on projection as the safety story. A protocol object holds the residual global type as state; its
   law admits a turn exactly when the turn is a `GStep` of the residual by the role bound to the signer. Bread's honest
   residual-preservation and progress lemmas then are the real, small theorem. Endpoint projections become what each party's
   resident may do next.
5. **The coordination ladder for concurrent activities (fork 3).** The rungs are: independent, monotone CRDT, confluent after
   lifting, reservation (escrow), lock, per-op equalizer. Mini's computed dial covers the first and refuses the rest. The
   escrow rung (`CRDT.escrow_refinement`: local quotas are I-confluent, and Σq = B gives the global bound) is how many
   activities draw on one balance without ordering. Pair it with the commutation/contention classifier
   (`ContendedCrossCell`, `ContendedForest`) for parallel independent turns, justness as the stated liveness property
   (`Proof/Fairness.lean`), and the single-machine principle.
6. **Two kinds of cross-object read.** A live read is part of the turn's footprint and conflicts with concurrent writers. An
   import is pinned to a committed receipt and conflicts with nothing (`CrossCellImport.lean:87-173`). Authority is evaluated
   at the settlement tip, not at branch time (`SettlementSoundness.deployedSettle_binds_live_authority`). These are distinct
   operations with distinct names and footprints, and calls across objects need both.
7. **Shape-catalog contracts for packages.** Bread's Hatchery design (`B/HATCHERY.md`) lets an author declare invariants in
   a few shapes: monotone registry, conserved measure, confinement under a ceiling, relation among fields. The one-step
   obligation is discharged against the real kernel step, and "forever" is a free induction. Mini can make this the package
   `invariant` surface checked by the certifying checker, ranging over all methods and callers. Bread's version ran over a
   two-case `List ℤ` toy.
8. **The capability kernel's invariants.** `only_connectivity_begets_connectivity` (generative authority from introduce,
   amplify, mint, endow and a confined self-origin) and the ceiling invariant `livingCellA_confinement` belong over the real
   step. The firmament's `doomedSet` cascading revoke is the only transitive revocation Bread had; finish its saturation lemma.
   Third-party law requirements need discharges bound to the invocation hash, not to a parent token.
9. **The presentation algebra.** `fireGate`/`projectFor` with gated (capability ∧ law) and reactive (capability ∧ transition
   ∧ window) affordances, and `Viewer` as authority × disclosure. Prove "cannot bypass the card" as one shared law function.
   Use distinct preview and commit types, since Bread's surface judged `(s, s)` while its executor judged `(s, s')`. Add DocMerge
   with conflict as state, the reversibility tiers (to be proved in Lean, which Bread never did), and the rehydration label as
   the badge for "what kind of true this card is".
10. **The honesty instruments.** Port `tooth_minus%`, `ExistsImageVacuity`, the free-conclusion and floor-derivation gates,
    and `#assert_compiled`. Fix KeystoneLint to type-check its companions and reject identity carriers. Keep the "binds ∨
    extract a collision" statement shape, the fail-closed export-gate discipline, and `Publication.honest` for every badge
    rendered. Bread found its worst wounds with these, and Mini's ATLAS already names the laws they enforce.

### The ten most dangerous false friends

1. **`Await.lean`: `OneShot`, `commit_resumes_once`, `four_faces_unify`.** This looks like the theory of Mini's Activity.
   `OneShot.run` is a public field, so one-shotness is a convention. The handler theorems need
   `resumeWith : (Reply : Type u) → Reply`, which is uninhabited. The four-face unification is `rfl` over three of the faces.
2. **`projection_sound`, `deadlock_freedom_by_design`, `epp_correspondence`.** These look like MPST deadlock freedom. They
   are head duality over global-type residuals. `Projectable` is unused, `Dual` ignores roles and labels, and there is no
   endpoint semantics.
3. **`CellContract.forever` and the app "forever" crowns.** These look like contract verification. The Hatchery's step is a
   toy, "forever" is plain induction under "every step admitted", and app crowns such as `bbf_plain_conserved_forever` are the
   kernel's own invariant renamed per app.
4. **`ConfinesAuthority := Fpu`** ("conservation and confinement are one law"). This is true by definition. Bread's FpuProbe
   shows Fpu over ℤ admits any mint and that the honest skeleton has two gates.
5. **`upgrade_never_bricks`, `UpgradeAuth.bySignature`, `migrate_conforms`.** These look like safe upgrade. The signature arm
   is the constant `True`, `admit` cannot run, and the migration theorem's premise is false for field-add.
6. **`JointTurn.atomicity_as_proof`, `binding_is_proper`, `EntangledJoint`.** These look like multi-party atomicity. They are
   `and_congr`, 1+1≠0 over `Unit`, and all-or-none over one shared state. They cite a nonexistent `tensor_not_final`.
7. **`ConfluenceClassifier` ("DECIDABLE, PROVED") and the blue/red projection split.** These look like computed coordination
   cost. They are `Iff.rfl` and Prop-only, and I-confluence of an arbitrary invariant is not decidable. Mini's
   `CoordinationDial` is the real one.
8. **`Fibration.lift_collapse`, `eventual_bounded_revocation`, `Finality.no_downgrade`.** These look like topology-parametrized
   bounds. They read a structure field back, define propagation into the view, and are monotone by definition. The fault and
   crypto axes are inert. Keep the principle, not the proofs.
9. **The Polis and epistemic summits: `governed_holds`, the `polis_governor` binary, `byzantine_majority_cannot_uphold`, the
   "Arrow" regime claim.** These are a struct projection, an executable whose verified branch nothing calls, a theorem with no
   votes or adversary in it, and an impossibility result that is cited but never formalized.
10. **CapTP, ConditionalTurn and Spec.Await dataflow.** These look like promise pipelining. `drainAll_preserves_caps` holds
    because the kernel cannot change caps. Slots are Booleans, so no value moves. "Dependency soundness" states membership, not
    precedence. `broken_promise_propagates` assumes its contrapositive.

Two further warnings span all of the above. First, `#assert_axioms`-clean, sorry-free and green mean only "no stray axiom".
Bread's composed apex `deployed_system_secure` rests on injectivity floors the tree itself refutes at BabyBear width, and it is
grandfathered in the ratchet. Second, `SymbolicDifference` "decides" satisfiability and equivalence only as a proof: its
certified cover never executed. Mini's executable `Pred/Satisfiable` is the thing to build on.
