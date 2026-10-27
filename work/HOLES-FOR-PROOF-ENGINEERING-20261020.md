# Holes as the machinery of proof engineering (rev 3)

[INFERRED] Recommendation to ROOT, CX-SCHOLAR revision 3, real 2026-10-20: build a persistent obligation engine whose repair semantics come from nano's
closure theory and whose evidence comes from Lean and the judge. The destination is a library that can explain and repair its obligations through a
redesign day. The first experiment should run that mechanism on nano's own Kernel proof dependencies.

[INFERRED] The crucial distinction is between retaining a proof, retaining its reconstruction recipe, and authorizing a claim about the current system.
These require different dependency information. A theorem can remain true while becoming useless evidence for the claim it was advertised to establish.
The collision campaigns are the strongest reason to make that distinction part of the mechanism.

[INFERRED] The existing repair theorem supplies a component of the guarantee, not the whole guarantee. It equates judgments over retained candidates
under a fixed template. A changed Lean statement, changed definition, new proof search, or changed checker needs an explicit bridge and revision
protocol. Building those is worthwhile; calling them already proved would reproduce the statement-audit problem.

## Evidence convention and fixed reference points (rev 3)

[INFERRED] A tag covers its paragraph, including wrapped continuation lines. READ means source read, not compilation independently repeated. MEASURED
means an observation made during this read-only lane. INFERRED includes interpretation, proposed design, estimates, and proposed measurements.
Historical measurements quoted by a document remain READ claims about that document.

[MEASURED] N denotes hbox `/tank/dregg-build/nanodregg/main`, rechecked in this revision at `b5f880bc96ea6a21bf0176d4da37efdc605b270f`. The first memo
read LANG-68 at `2b6e5e1c30f14833322ebca1c292b422ba53c183`; the new source readings use the LANG-69 split.

[READ N:decisions/lang.md, LANG-69] ClosureStatements, Judge, Repair, Outcomes, Operations, Soundness, History, and Stability replace the old
Contextual/Closure proof module. The decision records preserved statement/proof bodies and changed imports; this revision cites the actual split.

[MEASURED] M denotes the `main` object of hbox's bare repository `/tank/dregg-build/claude-lanes/bundles/burst5-minidregg.git`, at
`334316df5653a846ed5d6069bbfb282bc4d5fcf6`. Revision 3 reconfirmed these objects and used `git show`, without a checkout. Hbox's `~/dev/minidregg` is
instead `e1bb78d1d19d46f520e5703f674d7b76da68f3a7`, an older scaffold.

[MEASURED] B denotes hbox's `~/dev/breadstuffs`, at `fdfef4613823c1037231b5f36255c6389030b5b5`; its `metatheory/` is the proof tree examined. These are
inspected source snapshots, not a claim that either M or B is today's integration captain's tip. W denotes `/Users/ember/dev/redregg/work` on the Mac. R
denotes W:ACTIVITIES-GPT-RAW-20261020.md; document numbers and sections below refer to that raw text, read whole before any other record in revision 3.

[READ W:DECISIONS-20261021.md, CARD 9; cv:7c10f132, exchange around 3600] Ember explicitly asked for integration into proof engineering, then mini and
breadstuffs, and approved redesign days. CARD 9 records option B: contextual holes in the deployed language. That destination supersedes the earlier
invitation to choose between a closed-hole boundary and a redesign.

## What the landed theory actually gives us (rev 3)

[READ N:Lang/Contextual/Closure.lean] An interface names a hole, its context and type, token-backed hypotheses, guard, budget, chooser, and acceptor. A
candidate retains its filling, declared supports, blockers, cost, proposer, and status. Effective supports also include tokens for context variables the
filling actually uses. Tokens have identities and versions.

[READ N:Lang/Contextual/Closure.lean, judge] Judgment first checks typing, then the interface guard, then live blockers, then missing supports, then
budget. Its statuses distinguish ill-typed or guard-conflicting candidates, pruning, suspension, uncovered cost, and verification. These statuses are
distinct from the five outcomes of repairing a selected filling.

[READ N:Lang/Contextual/Closure.lean, provenance; Lang/Proofs/Contextual/Judge.lean] The provenance representation is a list of
positive-support/negative-blocker pairs, one per candidate passing typing, guard, and cost. Alternatives form a sum; simultaneous supports form a
product. It is independent of which tokens are live, but depends on the environment, candidate set, and checker.

[INFERRED] This is useful signed provenance, not yet an arbitrary symbolic polynomial in all changing facts. In particular, guard failures are filtered
for the supplied environment. Retain the candidate archive as well as its currently computed polynomial, or a later environment change loses
alternatives. Do not flatten a shared proof DAG into exponentially many monomials merely to print this notation.

[READ N:Lang/Proofs/Contextual/Judge.lean, withdraw_never_refutes] Withdrawal changes support availability, not the type or guard calculation; it does
not create a typing/guard conflict. The ill-typed conflict theorem refutes the proposed filling's typing judgment. It does not prove that the hole's
target proposition is false or that no other filling exists.

[READ N:Lang/Proofs/Contextual/Repair.lean, repair_agrees_from_scratch; N:Lang/Contextual/Closure.lean, observe/fromScratch] Under coherence, repair and
fresh judging produce equal recorded candidate-status lists. They use the same template and retained candidates. The observation excludes selections,
accepted flags, history, and owed obligations.

[READ N:Lang/Proofs/Contextual/Repair.lean, locality/repair_rejudged_eq_touched] An unrelated token edit leaves the closure unchanged, and the repair
log contains exactly touched candidates. Environment replacement touches all candidates. The definitions still scan lists to find affected entries; the
logged-work theorem is not a bound saying elapsed work is O(affected entries).

[READ N:Lang/Contextual/Closure.lean, repairSelected; Lang/Proofs/Contextual/Outcomes.lean] The five outcomes are kept, alternative, replacement,
strengthening, and suspended. An alternative with the same filling can change the support route; a different replacement is offered for selection.
Strengthening supplies a smaller-context witness; it does not rewrite the closure's template.

[READ N:Lang/Proofs/Contextual/Outcomes.lean, strengthening_sound; History.lean, session_preserves_tpl] The strengthening law needs a lawful calculus,
the relevant checked filling, and an unused variable. It reconstructs the original filling by weakening the smaller one. Sessions preserve the template.
Consequently, changing a theorem's telescope is not already one of the existing edit operations.

[READ N:Lang/Proofs/Contextual/ClosureStatements.lean, Template.Typed/Derivable/Available/Settled] Derivable means the partially filled template types
under the remaining hole declarations. Availability checks selected supports, and settledness quantifies over selections; an empty selection set can
satisfy these conditions. None alone says every intended obligation has a complete proof.

[READ N:Lang/Proofs/Contextual/Soundness.lean, conditional_soundness_closure] The theorem requires a typed template, coherence, and settledness. The
operations do not establish template typing from arbitrary data. This is the same missing producer obligation identified in W:ACTIVITIES-LOG.md; a
proof-engineering adapter must supply it, not erase the premise in its UI.

[READ N:Lang/Proofs/Contextual/History.lean, executed_prefix_blocks_replan] Acceptance freezes a selection and preserves settlement obligations even
when support disappears. Version reissue does not revive old citations. The separate Rule/Derives/least-fixpoint theory in ClosureStatements and
Stability shows why reference counting cannot ground a cycle after its last external fact is withdrawn.

[INFERRED] For a proof library, acceptance should freeze a historical receipt at a revision. It must not forbid replacing that theorem's proof in every
future revision. Archive the old accepted object, open the successor obligation, and retain reconciliation obligations for claims already made. This
gives withdrawal its honest meaning without pretending published history can be rewritten.

[READ N:Lang/Contextual/Core.lean; Lang/Proofs/Contextual/Typing.lean; CoreInstance.lean] CMTT has explicit contextual metavariables and substitutions;
`cmttLaws` discharges the closure laws. Its object types are simply typed, including contextual boxes. Lean's dependent telescopes, universe levels,
typeclass arguments, inductives, and reduction behavior are not this object calculus.

[READ N:Lang/Contextual/LangCalculus.lean; Lang/Proofs/Contextual/LangInstance.lean] LANG-68's deployed instance uses closed `ref` holes and `fillRefs`.
`langLaws` is real, but `langTemplate_no_hyps` proves typed templates in that fragment have no token-backed hypotheses. The contextual strengthening
path is therefore empty for those templates, unlike the CMTT instance.

[READ N:Lang/Contextual/Protocol.lean; Lang/Proofs/Contextual/ProtocolTyping.lean] The protocol theory adds response-indexed continuations, explicit
interfaces, reusable facts, affine resource tokens, and history. `Open.Replan` is an explicit theorem premise; the data setter alone does not enforce
it. Admission of the next operation is separate from protocol derivability.

[READ N:Lang/Proofs/Contextual/Protocol.lean, locality/repair_agrees_from_scratch] Its fragment-repair theorem is especially close to a judge adapter:
each fragment has a support list and a `ReadsOnly` proof. Agreement outside changed keys implies selective repair equals full checking. The significant
obligation for our exporter is proving or conservatively enforcing `ReadsOnly`.

[READ N:Lang/Contextual/Protocol.lean, Coin; Lang/Proofs/Contextual/Protocol.lean] One filling per shared hole name cannot predict both coin responses.
Response-dependent names can encode foresight; `foresight_iff_names_separate` states that boundary. The preceding assistant's summary in cv:7c10f132
reversed this direction; the source controls this memo's interpretation.

[INFERRED] In proof orchestration, the response-dependent continuation is a legitimate next task after Lean reports a goal or counterexample. A proof
candidate for a fixed obligation is not allowed to change its target retrospectively to fit that response. Keep claim identity and revision explicit.

## What the raw documents add to the mechanism (rev 3)

[READ R:doc 1 §§2–8; doc 2 §§5–7; doc 3 §§4,7–8] The raw proposal requires more than a success-dependency graph: interaction obligations, four
preservation contracts, separated alternative worlds, grounded cycles, composable repair objects, polarity, scoped transport, and explicit logical
statuses. [INFERRED] These requirements survive the source audit. Revision 3 makes them part of the proposed mechanism, rather than leaving them as
literature analogies. The supplied raw documents are the source for literature descriptions here; the linked papers have not been independently
re-audited.

[READ R:doc 1 §5] The ludics proposal interprets a guard through admissible interactions: `F(h,w) = admissible ∩ T(h,w)^⊥`. Adding a required
counter-interaction intersects the eligible fillings with its orthogonal. If tested interactions are only a subset of required interactions, passing the
tests gives an overapproximation of admissibility. The raw text also warns that a daimon-like object which gives up can satisfy an interaction criterion
without completing a program.

[INFERRED] For proof engineering, let the obligation owner fix the guard: the exact target and context, intended instance, allowed assumptions, and
evidence required of consumers and audits. A candidate supplies evidence against that guard; it cannot replace it with an easier one. Treat ludics as a
design lens here, not a claim that Lean checking or nano's Boolean guard already implements orthogonality or biorthogonal closure. A finite plant suite
is evidence about the instrument; it is not completeness of the semantic audit. A suspended hole must never count as an established theorem, even if a
partial template remains derivable.

[READ R:doc 1 §6; N:Lang/Proofs/Contextual/History.lean, consumer_boundary] The raw boundary-theorem proposal distinguishes four reuse claims. Nano's
`consumer_boundary` proves preservation for a consumer factoring through a specified projection when that projection is equal. It does not discover that
projection or prove arbitrary clients factor through it.

[INFERRED] Each consumer edge should therefore identify its preservation contract explicitly: (1) typing/interface preservation reuses client typing;
(2) logical-contract preservation reuses client proofs under that contract; (3) observable-behavior preservation reuses cached observations; (4)
cost/resource preservation reuses bounds and scheduling evidence. These are distinct promises, not a single unqualified “compatible” flag.
Binary-to-linear search can preserve membership and lose logarithmic cost. A proof-body replacement can preserve the target and lose reconstruction
performance; a representation equivalence can preserve meaning without preserving definitional equality.

[INFERRED] The boundary certificate should name old/new revisions, permitted observations, transport or equality evidence, and every residual
obligation. Dependent clients may mention the replaced inhabitant in their types; “both have type A” is insufficient. Prop proof irrelevance does not
make a changed executable definition, a new telescope, or a changed deployment instance interchangeable. A boundary with no checked transport propagates
repair to consumers instead of claiming locality.

[READ R:doc 2 §5] Interface automata supplies the input/output variance lesson through alternating simulation: an implementation must accommodate the
specification's legal inputs while appropriately restricting outputs. Strengthening a producer guarantee and strengthening a receiver precondition have
opposite consequences. Ownership of a choice is also separate from when information is available.

[INFERRED] Apply that polarity directly to premise pricing. Replacing `A → Q` by `(A ∧ H) → Q` adds a requirement on every caller; it is not a stronger
usable theorem merely because its premise is stronger. Replacing Q by a proven stronger postcondition can preserve old consumers. Dropping an unused
assumption produces a stronger theorem. These three moves need different transport records. Chooser/acceptor identities enforce who can act; they do not
establish alternating simulation. A review response is an environmental input with a continuation, not a witness the repair engine may select to make
its preferred proof pass. Preserve one target revision across that interaction.

[READ R:doc 2 §7; N:Lang/Contextual/Closure.lean, Evidence/Status] The four logical statuses are Witnessed, Open/blocked, Refuted, and Outside this
procedure. They are not synonyms for the five repair outcomes or the five candidate statuses. Nano's `conflict .illTyped` refutes the typing of one
supplied filling; `guardFails` rejects that filling against its guard. Neither proves the target proposition false or the completion space empty.

[INFERRED] Store those three classifications separately. Witnessed requires a checked inhabitant of the exact obligation; Refuted requires a checked
negation or impossibility argument for that same obligation and domain. No retained candidate, a failed tactic, a timeout, an unsupported translation,
and a withdrawn support do not produce Refuted. Keep timeout/unsupported as procedural coverage information alongside the still-open logical obligation.
A claim `P ∨ Collision` can be Witnessed as a literal proposition while blocked as evidence for the intended binding claim.

## A theorem as an enduring obligation (rev 3)

[INFERRED] Represent a claim by a stable identity and an immutable obligation revision. The latter contains its elaborated target, telescope, universe
parameters, definition-closure identity, intended deployment instance, toolchain, and the interpretation of the advertised claim. A declaration name
alone is not an obligation identity: its meaning can change underneath it.

[INFERRED] Each candidate records a proof artifact, a reconstruction recipe, precise support edges, audit evidence, blockers, and checking receipts.
Keep candidate recipes after suspension or pruning. A failed tactic attempt is useful repair evidence but is not a kernel proof or a refutation. A
timeout remains incomplete work, never an ill-typed certificate produced by interpreting failure as false.

[INFERRED] Use three related graphs. The proof graph describes what an elaborated proof uses. The contract graph describes what the proposition and its
definitions mean. The reconstruction graph describes what elaborating the recipe reads, including tactics, instances, simp declarations, generated
files, plugins, and relevant tool configuration. Their edges answer different questions.

[INFERRED] A proof-body edit can change the proof graph without changing the contract graph. A definition changing beneath an unchanged theorem type can
change the contract graph. A simp-set edit can change reconstruction without invalidating an already kernel-checked proof. Conflating these makes either
unsound reuse or needless whole-library re-proving inevitable.

[INFERRED] The Lean exporter should start from both declaration type and value, enumerate constants, follow definition/type dependencies conservatively,
and retain universe and instantiated argument data. Include projection structure identities, generated auxiliaries, recursors, inductive constructor
shapes, and opaque boundaries. Track external dependency versions rather than silently omitting their meaning.

[READ M:Verify/ObjectiveManifest.lean] Mini already combines `getUsedConstants` with explicit projection-type names: optimized constant traversal alone
misses the structure named by `Expr.proj`. Its semantic closure follows definition bodies and inductive shape, but deliberately excludes theorem proof
bodies. That is appropriate for its contract purpose and insufficient for the new proof graph.

[INFERRED] “Its axioms plus the constants it unfolds” is therefore a good question, but an incomplete schema. Axiom closure omits hypotheses and
instance-specific semantic traps. An unfolding trace omits other dependencies and describes one execution. Begin with conservative elaborated
dependencies; use observed unfolding to explain or optimize that set only after an independent comparison.

[INFERRED] A support should name an immutable fact or receipt version, not a mutable boolean attached to a theorem name. Separate kernel-check receipts,
contract identities, assumption witnesses, deployment bindings, and semantic-audit approvals. A missing receipt suspends current authorization; it does
not retroactively make an old kernel derivation logically false.

[INFERRED] The minimal record schema is: obligation `(claim ID, revision, context, target, instance)`; candidate `(artifact, recipe, support versions,
blocker IDs, cost receipt)`; finding `(subject revision, candidate-or-obligation scope, evidence, disposition)`; and event
`(withdraw/assert/revise/check/select, input revision, output revision, residual obligations)`. Keep inverse edges as a derived index, with the
immutable journal as the recovery source.

[READ N:Lang/Contextual/Closure.lean, Candidate/judge] Candidate cost is supplied data compared against the interface budget. No timing instrument in
this definition certifies that number. [INFERRED] Resource authorization therefore needs a measured or otherwise justified cost receipt; a
proof-engineering scheduler must not treat a proposed cost as a measured checker bound.

[INFERRED] A blocker needs a subject, scope, reason, evidence, and disposition. For a disjunct finding, record the exact conclusion branch and a proof
that the branch follows from premises alone or from the intended instance alone. For a premise finding, record the binder/application and matched
refutation or missing witness. Distinguish a proved blocker from an open review question.

[INFERRED] Apply these blockers to credit for the intended claim, while keeping the literal theorem and its kernel receipt visible. A proof of `P ∨
Collision` is still a proof of that disjunction. If Collision is independently guaranteed, it is not evidence for P. The repair obligation is to recover
a useful statement and its consumers, not to relabel the existing proof as a Lean failure.

[INFERRED] Audit tokens can be candidate-specific or obligation-wide. A bad proof route can be replaced by another route; a vacuous target remains
vacuous under every proof of that same target. Putting an obligation-wide defect only on one candidate would let alternative selection evade it. The
judgment policy must propagate both scopes and keep unknown audits distinct from passed audits.

[INFERRED] Positive provenance `ab + c` can mean two certified routes to the same fixed obligation. But two syntactically different Lean proofs are
replacements under the current closure's equality, not automatically its identical-filling alternative. One possible representation uses a shared claim
certificate as filling and stores proof derivations as its distinct support certificates.

[INFERRED] That representation needs a checked correspondence: either derivation must establish exactly that certificate's proposition and context.
Proof irrelevance alone does not authorize changing definition meanings, premise audits, executable definitions, or claimed deployment bindings. Never
turn a semantic equivalence assertion into a source-name equality shortcut.

[INFERRED] Compose dependencies initially in topological order, with recursive definition components treated as revision units. The closure currently
consumes world tokens; it does not recursively judge the whole theorem graph. The separate grounding theorem is a foundation for composition, not
evidence that arbitrary mutually supporting audit receipts already have a sound fixed-point implementation.

[INFERRED] A redesign first withdraws obsolete support versions, then classifies affected obligations, generates successor revisions for changed
contracts, rechecks reusable candidates, and schedules actual re-proofs where necessary. Retain the old-to-new relation: same statement, stronger
statement, conditional replacement, or intentionally different claim. A rename is not proof of equivalence.

[INFERRED] Price three quantities separately: declarations whose contracts are affected, statements that actually gain hypotheses, and proof bodies
needing repair. A dependency cone bounds inspection; it is not the premise spread itself. The premise price must eventually name each changed telescope
and each instantiated call site where the new condition must be discharged or propagated.

[INFERRED] Strengthening offers a useful route for dead hypotheses, but Lean's dependent context requires checking the types of later binders and the
target as well as occurrences in the proof term. Generate a smaller theorem and let Lean check its dependent telescope and any transport. Do not
mechanically erase a binder solely because a proof-value scan calls it dead.

## Grounded worlds and first-class repair programs (rev 3)

[READ R:doc 1 §7; N:Lang/Proofs/Contextual/Stability.lean] The raw positive cycle `p←a, p←q, q←p` must lose p and q when a is withdrawn; immediate
support counts can keep them alive incorrectly. Nano proves grounded derivations and an unfounded-set result in a separate rule theory. The one-level
closure does not itself propagate theorem-to-theorem support or implement stable-model semantics. Its blocker literals refer to explicit token liveness.

[READ R:doc 1 §7] The default cycle `p←not q, q←not p` has alternative stable worlds {p} and {q}; retaining both is not permission to assert their
union. No evidence either way, incompatible alternative worlds, conflicting evidence inside one world, and unfinished analysis are different states.
Differential update weights record removal, not logical negation.

[INFERRED] Give receipts a compatible world/revision identity and keep alternate assumption sets separate. Two candidates can safely coexist when
neither is asserted as the other's premise; composition must check that their supports can hold in the same world. In particular, do not use “no audit
failure found” as a default proof that an audit passed. The initial experiment can use explicit finite worlds and positive, well-founded receipt
derivations; it must label default-negation reasoning Outside this procedure until its semantics and implementation are supplied. Add a cycle plant at
the composed receipt layer, not only an unrelated toy cycle already known to fail counting.

[READ R:doc 1 §8] The algebra of checked repair asks for three separate results: conditional soundness, agreement with new-world analysis, and locality.
Recompute-everything satisfies the second. History-sensitive selection needs the same history on the reference side; multiple-solution semantics
compares admissible solution sets or another stated observation, not arbitrary proof identity. A first-class repair can be passed, parameterized over
edits/substitutions, composed, compared by policy, suspended with a residual, and checked independently of how it was found.

[INFERRED] Make `RepairPlan(oldRevision,newRevision)` a persistent data object containing the boundary relation, support reads, applicability evidence,
ordered steps, candidate-producing recipe, checking operation, selection policy, and residual continuation. Steps include retain, transport,
re-elaborate, search, split an obligation, and request an owner decision. Compose plans only where intermediate revisions and contexts agree. A composed
plan must expose its remaining obligations; a transformation script or a cost estimate is not a correctness certificate. Preserve old plans and pruning
explanations so a later edit can resume work at the decision that actually became invalid.

[READ R:doc 1 §2; doc 3 §4] Repair hints include completed and conditional derivations, partial proofs, transformations, and pruning explanations. The
raw PUMPKIN Pi discussion adds mathematical content: a hint can identify a checked equivalence, transport, correspondence, or missing lemma. It does not
say arbitrary premise withdrawal admits a transport; withdrawal supplies no witness for a deleted assumption, and representation changes may require a
relation rather than an equivalence.

[INFERRED] Retain a hint's source/target contract, matching substitution, transport lemma, and remaining side conditions. If an old proof of `P old` is
reused through a relation between old and new representations, Lean must check the relation and the produced proof of `P' new`. A search hint merely
proposes these objects. Record why a branch was suppressed: inconsistency under constraint c, preference for a cheaper candidate under a, or a missing
witness for G. Withdrawal of c or a, or a new witness for G, schedules that branch. Performance preferences should influence search order; they must not
masquerade as semantic impossibility. Keep the archive even when current provenance filters it out, and record coverage limits when a bounded retention
policy evicts a residual.

## The judge is already part of this system (rev 3)

[READ N:gates/check.py; gates/fast.py; decisions/gates.md, GATES-19/20/22] Nano has source gates, a selective fast path, full judges, and convergence. A
fast landing builds reached libraries/executables and selected cargo checks; it does not certify every runtime row, census, or benchmark. Later
convergence is a separate evidence event and must stay visible.

[READ N:gates/readset.py; gates/rebase.py, verify] Traced keys record file reads and failed probes, compiler reads, selected stat information, directory
listings, executed binaries, tool versions, row text, and applicable waste limits. The verifier recomputes keys on the candidate. Reuse requires a prior
successful verdict with the same key; red or incomplete work is not reusable successful evidence.

[READ N:gates/readset.py; decisions/gates.md, GATES-20] The mechanism distinguishes runtime reads from compiler reads and listing/absence dependencies.
It records outside-tree observations without making every such input content part of the tree key; the decision records identify external configuration,
including git/lake configuration, as unfinished. This is a concrete boundary on any claim that the whole judge already satisfies `ReadsOnly`.

[INFERRED] In closure language, a successful row is a candidate receipt, its input key supplies supports, changed inputs withdraw old authorization, and
re-running is a repair attempt. The conservative fallback supplies a larger support set when tracing cannot justify narrowing. Convergence adds overdue
receipts and can discover conflicts that a fast landing never checked.

[INFERRED] Calling this an ATMS is useful if it means conditional evidence with retained reasons. The present implementation does not yet provide a
theorem-level ATMS with alternative proof routes, negative semantic blockers, persistent unresolved obligations, or a proved recursive dependency
adapter. Its read sets are process/file dependencies, not an account of theorem premises.

[READ N:Census/Axioms.lean; gates/census.py] The census walks declarations and collects axiom dependencies, checking the allowed standard axioms. That
is a valuable existing environment traversal and a distinct guarantee. A false hypothesis, uninhabited carrier, tautological disjunct, or disconnected
“tooth” can survive an axiom-clean census.

[READ W:LANE-RULES-NANODREGG.md; N:gates/check.py; N:decisions/gates.md] The premise question and disjunct check presently impose review duties and
named decision records. The enumerated source gates read here do not implement a complete elaborated theorem/premise diff. Do not turn this scoped
observation into a claim that no other project instrument audits premises.

[INFERRED] Add a durable obligation index beside the existing judge receipts, and join them by commit, declaration revision, and input identities.
Report “kernel checked,” “reconstruction checked,” “semantic audit passed/open/blocked,” and “convergence pending” separately. One green icon for all
four would conceal exactly the distinctions the closure theory teaches us to preserve.

## What to build first in nano (rev 3)

[INFERRED] First deliverable: a shadow obligation journal and Lean environment exporter, applied to one real Kernel slice. Keep current gates
authoritative. The journal should answer: what changed, which old evidence ceased to authorize which claims, what alternatives survive, and what proof
work is now owed. This is an operating mechanism, not a dashboard assembled from prose afterward.

[READ N:Kernel/Proofs/Fold.lean, chain_binds/chain_binds_sep] The chain theorem's escape branch is `CollidesAmong` the two logs' explicit `chainPres`
inputs. Its `_sep` corollary discharges that branch with separation over exactly that list. This is a concrete place to track both a theorem dependency
and the semantic extent of a collision premise.

[READ N:Kernel/Proofs/Trie.lean, inclusion_sound/exclusion_sound] Trie soundness similarly names `CollAmong S (readPres S k p t)`, including the
compared proof/path inputs. [INFERRED] The sample should preserve these finite, instance-linked statements and deliberately detect a scratch mutation
replacing them with a global existential collision escape.

[READ N:Kernel/Proofs/Receive.lean; Kernel/Proofs/Logic/Triple.lean] `receive_ok_with` and `receive_congr` connect derivation to pins and row views.
`submit_frame` derives its framed triple from `Triple` and `Indep`; `call_frame` connects the footprint to admission. These provide a non-cryptographic
composition sample alongside the collision sample.

[INFERRED] Export the transitive slice rooted at these declarations, including their types, values, contract dependencies, axiom sets, and local premise
applications. Seed persistent obligations from the existing checked source revision; mark evidence unavailable unless a corresponding receipt exists.
Retain the existing theorem names and signatures unchanged in this first tooling increment.

[INFERRED] Exercise a fixed matrix of scratch edits: unrelated proof edit; support theorem proof replacement with the same contract; definition-body
change beneath an unchanged target; newly required hypothesis; unused hypothesis; global-collision escape; hidden projection/auxiliary dependency;
changed instance/simp input; support withdrawal/reissue; and exhausted checking budget. Add withdrawal of a pruning reason, loss of positive-cycle
grounding, incompatible alternative worlds, logical correctness with lost cost evidence, and partial audit coverage.

[INFERRED] For each edit, compare three baselines. A: recompute closure statuses for the same candidate set, matching the landed theorem's observation.
B: independently kernel-check retained proofs against the exact new environment and obligation revisions. C: freshly elaborate the saved recipes with
fixed dependencies and budgets. Disagreements between A, B, and C must be explained.

[INFERRED] Baseline C does not mean exhaustive fresh proof search. New candidates can be discovered later and then enter both sides of a subsequent
comparison. Report candidate-set identity alongside every repair equality. Otherwise a finite retained menu is quietly being advertised as completeness.

[INFERRED] Prove a small adapter invariant: a live exported receipt refers to the same obligation revision and inputs; every dependency outside the
changed set is equal; the exported fragment reads only its declared supports; and an admitted candidate has a matching successful check receipt. Connect
that invariant to Protocol's fragment repair theorem and Closure's persistent candidate model.

[INFERRED] Do not instantiate `CalculusData.check` with “run Lean and return false on timeout.” Its soundness/completeness laws are mathematical
judgments; resource failure is an operational result. The first adapter should judge finite receipt data and leave arbitrary Lean proof checking with
Lean. A later dependent-context bridge can internalize more of that correspondence explicitly.

[INFERRED] Add an inverted support index and retain the reference list implementation as the oracle. Check equality of affected candidates, statuses,
and residual obligations. Measure index maintenance, scan work, actual checker calls, wall time, peak memory, and alternative counts separately. The
current locality theorem motivates this optimization but does not prove its runtime complexity.

[INFERRED] Each new check needs its own disabling experiment and real expected output, following rule 16. Include a malformed/partial export and a
missing-import environment: both must report incomplete coverage, not fewer obligations successfully repaired. Whole outputs and exact source revisions
belong in the resulting receipts; this scholar lane has not executed those plants.

[READ N:gates/OWNERS; W:LANE-RULES-NANODREGG.md] GATES owns judge/Census integration, KERNEL owns the Kernel sample, LANG owns closure changes, and
shared build configuration needs its named owner. The implementation brief must assign those paths explicitly. Current memory, heartbeat, filtered-test,
and judge-window rules remain in force.

[INFERRED] Build/run work for that future lane belongs on hbox with its own cargo target and warm artifacts: `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2
swarm-build`, with heartbeat caps. Larger library exceptions require the existing named-library rule. Nothing about this experiment justifies a
whole-tree rebuild, a weakened gate, deleting caches, or concurrent duplicate judge work.

[INFERRED] Measure the reason for each revisit as well as its cost: invalidated support, reopened pruning branch, changed interface, refreshed
authentication, failed transport, or changed resource contract. A dirty edge means potentially affected; rechecking can show the observation unchanged.
The premise spread counts actual new hypotheses and their applications, not every node marked dirty. For the first algebra test, compose two edits,
compare sequential repair with batch analysis at the final revision, and compare residuals separately from candidate statuses. Equality of selected
proof terms or acceptance history is not the landed repair theorem's observation.

## Integration experiment and the evidence boundary (rev 3)

[READ R:doc 3 §§7–8; N:Lang/Proofs/Contextual/Negotiation.lean] The raw integration experiment is two cells negotiating a one-use capability,
alternative providers, a deadline and cancellation. Nano already has the negotiation model: unrelated-update reuse, provider revocation, epoch-indexed
representation transport with stale-opening refusal, competing commitments/replay, expiry/cancellation, and lost-reply obligations. The model's
internal-once result explicitly does not establish exactly-once external execution. This is a source reading, not a claim that a deployed
proof-workbench workflow or distributed protocol has been run.

[INFERRED] Use that model as the second client of the same journal after the Kernel slice. Track the proof obligations of its four changes through the
exporter and repair plans: preserve unrelated contracts; suspend one provider's admission while retaining its conditional derivation; refresh
representation evidence using `representation_change_transports`; retain the receipt and settlement obligation after dispatch while checking
`competing_commitments`. A deadline or cancellation opens a typed continuation. It cannot erase an in-flight job or let a late result silently authorize
a successor target. Tie any result to its request identity, input revision and checker receipt.

[INFERRED] This joins proof engineering to nano's own language/protocol theory without building a second proof calculus or a second admission path. The
Kernel pilot tests declaration repair; the negotiation client tests selection, current admission, resource accounting and history together. The next
implementation must supply the journal-to-model interpretation and an executed workflow receipt. Existing negotiation theorems alone do not establish
that the new orchestration obeys them. Progress needs explicit worker availability, scheduling and bounded-check assumptions; safety while suspended is
not proof that a repair eventually finishes.

[READ R:doc 3 §7] The OpenTheory discussion requires certificate acceptance to name the statement, theory context, definitions, admitted assumptions,
and checker or semantic bridge. A shared file format does not supply a logical interpretation. The supplied Candle discussion similarly places the
theorem and its logical context at the authoritative output boundary.

[INFERRED] For Lean-to-Lean tooling, record the exact environment/toolchain and imported theories, target, instantiated parameters, axiom inventory,
artifact identity, and successful checker receipt. Check the destination environment; a same-spelled declaration or serialized success is insufficient.
For any later Isabelle/HOL or other prover participant, retain its logic tag and bridge obligation. Until a semantic translation/replay is checked, its
certificate is evidence in its source logic only. Do not make nano accept foreign certificates on the strength of common JSON or a trusted producer
name. This experiment is development tooling; nano's deployed re-execution admission remains its chartered path.

## Mini: reuse its existing proof-engineering investment (rev 3)

[READ M:PROOF-ENG-DESIGN.md; hbox:/tank/dregg-build/claude-lanes/proofeng/STATUS.txt] Mini's earlier proof-engineering work replaced repeated
constructor inversion with StepCases and a shared dispatcher, split a large preservation proof, and reduced pin maintenance. The status record reports
preserved statement/axiom inventories. Those are historical receipts, not builds rerun here.

[READ M:Theory/ObjectiveBendStepCases.lean; Theory/ObjectiveBendDemandPreservation.lean] The source exposes named case obligations and assembles them
into preservation. [INFERRED] That is already a useful template: persistent holes can correspond to case fields with explicit contexts, while the
dispatcher is the composition theorem. Re-proving a changed constructor need not rediscover the entire elimination shape separately in every consumer.

[READ M:docs/HP-DESIGN.md, opening through §1] The later redesign changes representation and runtime architecture: resident World/Host, batched
admission, byte arrays and fixed digests, bounded work, and deterministic simulation. Such changes cross semantic interfaces, not merely proof scripts.
[INFERRED] An obligation engine must retain the relation between old and successor claims instead of treating every changed fingerprint as equivalent
work.

[READ M:Verify/ObjectiveManifest.lean; scripts/objective-manifest.py] Mini already fingerprints elaborated statements and their transitive definition
closures, including inductive shape and recursive components. Its ratchet classifies added, removed, restated, redefined, and axiom events; each needs
an exact decision. Rerendering alone passes. [INFERRED] Preserve that distinction.

[READ M:scripts/HypothesisLedger.lean] The hypothesis ledger looks at Prop families and binders, refutation/witness coverage, conditional versus general
versus instance evidence, and trivial inhabitants. It distinguishes matching a particular refuted instance from refuting an entire family. [INFERRED]
These are natural producers of scoped blockers and support witnesses; a new handwritten assumption list would discard that work.

[INFERRED] Adopt the common journal schema, extend the existing environment exporter with proof-body and reconstruction edges, and ingest the existing
manifest/ledger events. Keep one canonical event identity so a premise finding cannot disagree between two tools merely because each copied a list. Do
not import the manifest serializer's `partial def` approach into nano against its source policy.

[READ M:Theory/AuthTrie.lean; Theory/AuthTrieRange.lean; Theory/ObjectiveBendDigest.lean; cv task:01a15630-cf43] The inspected mini snapshot still
contains global `∨ Collision` statements, including trie verification and deployed digest claims. The task's historical site count is not a fresh
inventory. Generic quantification over D also needs care: finite-deployment vacuity is not a proof that the generic theorem fails or that every possible
D has an inevitable collision.

[INFERRED] Use those sites as the second pilot: attach a deployment-scoped blocker, retain the literal old proof, propose an explicit compared-input or
security-reduction successor, and price the consumers that must change. The journal succeeds when the useful replacement reaches consumers, not merely
when it can display the old theorem's vacuity in a graph.

[READ R:doc 2 §6; M:Theory/TypedAuthorization.lean:1210–1245] `Capability.Admissible.at_policy_revision` is a concrete repair hint: same revocations,
issuer epoch, policy generation, and preserved parent relationships transport semantic capability bounds to a new policy revision/root. Current request
evidence, policy membership, and policy acceptance remain separate obligations. [INFERRED] Use this actual partial transport as a pilot; an
“authorization invalid” bit would unnecessarily discard the surviving subderivation, while “authorization preserved” overclaims it.

[READ M:Theory/CanonicalReactiveView.lean, ObserverLens/Cache.advance] The dependency set has a locality proof; a clean delta preserves the projection,
and a dirty one reprojects. `dirty_of_project_ne` gives changed implies dirty, not dirty implies changed. [INFERRED] This is the operational pattern for
the journal's support index: sufficient dependencies, explicit causes, and checked reuse. It does not establish minimality or a bound on how often
rechecking changes a result.

## Breadstuffs: make premise spread executable (rev 3)

[READ B:docs/audit/META-REVIEW-STATEMENTS.md; docs/audit/NON-VACUITY-MANIFEST.md] The campaigns distinguish literal statement truth from advertised
claims and document disconnected teeth, tautological conjuncts, wrapper claims counted as summits, and conditional satisfiability. Later repairs in the
manifest correct earlier findings. [INFERRED] Preserve dates and successor relations; an old audit paragraph must not become a permanent blocker after
its exact subject changed.

[READ B:metatheory/docs/AXIOM-HYGIENE.md; metatheory/docs/SOUNDNESS-RESIDUAL-CENSUS.md] The records separate axiom hygiene from carrier assumptions and
implementation force. Some census entries concern premises bound in a theorem; others concern whether the implementation actually forces them.
[INFERRED] Both belong in the obligation model, but they are different edges and repair jobs.

[READ B:metatheory/Dregg2/Verify/FloorCensus.lean, header and schema] Bread already has an elaborated-term floor census: discovery, matched refutations,
Prop-definition bodies, embedded occurrences, structure fields, and endpoint/threader/dead classifications. Its floor-flow DAG tracks higher-order
threading and compiler-generated auxiliaries. [INFERRED] This is much closer to the requested premise mechanism than a new source-regex dependency
scanner would be.

[READ B:metatheory/Dregg2/Verify/FloorCensus.lean] The census describes failures of earlier versions: file-level discharge credit, missed Prop bodies,
higher-order edges, and partial-import reports masquerading as progress. Its coverage sentinels and environment floor prevent that last failure.
[INFERRED] Preserve them when ingesting a smaller pilot; explicitly scoped coverage must never pretend to be the existing whole-tree census.

[INFERRED] Map endpoints to real re-proof obligations, threaders to dependent restatements, clean dead theorem binders to checked strengthening
candidates, and bundle/projection cases to structural redesign units. Preserve the census's unresolved higher-order flags rather than inventing a
complete topological order. This yields the premise price from actual flow, not just reverse imports.

[READ B:metatheory/Dregg2/Circuit/Blake3FloorReduce.lean, §2] The source itself documents that replacing a false injectivity premise with an existential
collision disjunct merely moved vacuity across the turnstile. It points to an advantage-bound successor with explicit efficiency obligations. [INFERRED]
A blocker must follow the intended binding claim through that rewrite, or automated repair will congratulate itself on manufacturing a new escape
branch.

[READ B:metatheory/Dregg2/Crypto/HierarchicalGraphCommitment.lean, RomSuccessor] This source records replacement of a global-collision chain by a
keyed-ROM reduction with bounded oracle queries. It is a successor with a model and resource accounting, not a proof that the old deployed deterministic
hash acquired global injectivity. Keep those model boundaries in the contract.

[READ B:metatheory/Dregg2/Distributed/CheckpointPrune.lean:310–402; cv task:01a15630-cf60] The historical task reported an attestation linkage gap. In
the inspected source, two statements now bind `_hatt : CheckpointAttested cp`, but their proofs do not use it. That source differs from the task's old
zero-occurrence description; adding a binder alone also does not establish the advertised attestation-dependent guarantee.

[INFERRED] Start bread with one existing floor-flow component and its replacement claims. Import its census/audit identities, produce a revisioned
repair plan, and compare actual edits with the predicted endpoint/threader/bundle split. Expand only after reconciling the pilot with the existing
whole-tree ledger. The library's size makes coverage evidence part of correctness, not bookkeeping.

## Three ways this idea is most likely to be wrong (rev 3)

[INFERRED] Failure 1: the exported support graph is unsound or too coarse to be useful. Constants miss projections, elaborator inputs, external
configuration, or premise instantiations; alternatively everything depends on everything. A declaration graph can look precise while missing the causal
inputs of the actual checker or the semantic subject of an audit.

[INFERRED] Refuting measurement: run the fixed mutation matrix and held-out historical redesigns, comparing every reused success with independent fresh
checking and exact contract/audit revisions. One falsely reused success refutes support sufficiency. Include changed pruning conditions and combined
incompatible worlds; a positive-only graph can miss both. Record false invalidations against actual rechecking; if conservative closure regularly
approaches the entire library, claimed locality wins fail.

[INFERRED] Failure 2: closure equality proves the wrong thing for dependent redesign. Fixed-template status repair is correct while the target changed,
a premise silently strengthened, or a supposedly complete obligation still has holes. The existing abstraction may require substantial new theory before
it can justify the cross-revision claims we actually want.

[INFERRED] Refuting measurement: include changed definition meanings, dependent binder deletion, changed constructor interfaces, and obligation-wide
vacuity in the pilot. Compare target revisions, kernel receipts, open-hole coverage, and residual work with fresh reconstruction. Any admitted claim
whose exact target lacks evidence refutes the bridge; an unexplained residual mismatch refutes repair. Also demand that Refuted always carries a
correctly scoped impossibility certificate, and that a preserved logical result never silently preserves a lost cost guarantee.

[INFERRED] Failure 3: persistent alternatives cost more than rebuilding the proofs they save. Most theorems may have only one practical recipe;
alternatives may share every fragile support; provenance expansion, export time, and reviewer bookkeeping may dominate the saved checker work. That
would refute the performance case without refuting the value of a truthful obligation journal.

[INFERRED] Refuting measurement: compare current incremental Lean plus existing manifests, the journal with one candidate, and the journal retaining
alternatives over the same edit corpus. Charge export, storage, indexing, repair, checking, and human classification time; measure cold/warm totals and
peak memory under the actual box caps. If alternatives save no independent re-proof work or increase total cost, keep the journal and redesign
retention.

## Price, design fork, and delivery boundary (rev 3)

[INFERRED] PRICE PREMISES — this memo and the proposed first tooling increment: landed theorems gaining a hypothesis: **none**. Landed theorem
statements restated: **none**. New adapter theorems will have explicit coverage, revision-agreement, and support-sufficiency premises; these are new
obligations to discharge, not premises quietly attached to Kernel soundness or existing closure results.

[INFERRED] Price later semantic repairs separately. A collision repair or dependent-context redesign may legitimately replace statements and
redistribute assumptions. Before that change, enumerate the affected landed theorem names, old/new telescopes, successor relations, and consumer
discharges. “The dependency graph touched N nodes” is not a substitute for that price.

[INFERRED] Tooling needs no Lang wire or Store flag day. Versioned journal records can coexist during migration. The approved B constructor remains a
separate Lang redesign; the tooling experiment can start before it and should join it afterward through shared obligation interfaces, not a second
unrelated hole engine. No re-genesis cost is an argument for weakening the intended design.

[READ W:DECISIONS-20261021.md, CARD 9; N:Lang/Proofs/Contextual/LangInstance.lean] B changes the deployed term language and its
checker/evaluator/parser/printer/wire inductions. The old closed-fragment `langTemplate_no_hyps` boundary must remain explicitly fragment-scoped or
receive a replacement when the general instance changes. “No added premises” does not mean every old boundary statement can be carried unchanged to a
stronger language.

[INFERRED] ASK, implementation sequencing fork: receipt-first builds the graph adapter, proving composition and revision correspondence while Lean
remains the proof checker. Dependent-first generalizes the contextual calculus to dependent telescopes before building the richer Lean-term bridge. Both
can reach the destination. Receipt-first estimates 4–7 engineer-days for the nano pilot; dependent-first estimates 10–20 for a first bridge, with
materially greater uncertainty. These are planning estimates, not measured throughput, and not a reopening of CARD 9's Lang option B.

[INFERRED] Recommend receipt-first with an explicit dependent-context follow-on: it tests the actual dependency and audit semantics before fixing them
inside a richer calculus. This is an order of work, not a smaller destination chosen for cost. Mini's existing exporters make its pilot an estimated 2–4
additional days; bread's first floor-component pilot an estimated 4–8. These exclude the later negotiation client, full dependent bridge, wholesale
semantic repairs and full-library recovery. Judge queues and source drift are extra elapsed time.

[INFERRED] Deliver the nano journal, exporter, checked adapter invariant, scratch mutation receipts, and comparison report together. Then use mini's
real constructor redesign and bread's real premise flow as acceptance cases. The result should let an owner withdraw a definition or audit assumption
and receive a concrete, priced repair program whose eventual claims are checked against fresh evidence.

## Reading and execution receipt (rev 3)

[MEASURED] Revision 3 read R whole in explicit ranges 1–450, 451–900, 901–1318 before the existing memo and other records. The prior memo was 551 lines;
it was revised in place, retaining the fixed-template caveat, three dependency graphs, Kernel pilot, mini/bread instruments, failure measurements and
prices. Every section is marked (rev 3) because the revision also updates source navigation, integrates the raw material, and reflows the text. This is
not an implementation landing.

[READ W:PROOF-ENGINEERING-20261021.md; ACTIVITIES-PROPOSAL-20261022.md; ACTIVITIES-DESIGN-20261022.md §§0–1,9–9.4; DECISIONS-20261021.md CARD 9;
ACTIVITIES-LOG.md] Revision 3 read the proof-engineering record, condensed proposal, activity log, CARD 9, and the design's prototype
corrections/theory/reader/landing sections. The earlier memo's whole-design read remains a prior reading receipt, not a new claim that every earlier
proposed design was reread. LANE-RULES-NANODREGG and REENTRY were read; profile context was consulted and not copied here.

[READ cv:7c10f132, exchange around #3600 ±8; cv task:01a15630-cf43 and 01a15630-cf60] The actual exchange records Ember's integration request and ROOT
taking CARD 9 as B. Its assistant summary reverses the coin naming theorem; the source, not that summary, governs the account above. The collision task
IDs are task records, not conversation sessions. Their old site counts and “finish-only” wording are historical context, not a new measurement or
override of this brief.

[READ N:CHARTER.md; gates/OWNERS; decisions/lang.md LANG-66–69; Lang/Contextual/Closure.lean;
Lang/Proofs/Contextual/{ClosureStatements,Stability,Typing,CoreInstance}.lean] Revision 3 read the closure data and these small proof modules whole;
checked the principal judge, repair, soundness, outcome, history, protocol, and negotiation statements and supporting definitions; read
Core/CoreCalculus/NanoBridge and LangInstance carrier/law/boundary sections. These are targeted source reads, not replay of every proof body in the
8,395-line contextual tree. Gates reading covered check.py, readset key/schema, fast/rebase verification and census excerpts, and relevant GATES-19–22
and subsequent carry/convergence records. The source policy's no-new-check-weakenings remains intact.

[READ M:PROOF-ENG-DESIGN.md; Verify/ObjectiveManifest.lean; Theory/TypedAuthorization.lean; Theory/CanonicalReactiveView.lean;
Theory/{AuthTrie,AuthTrieRange,ObjectiveBendDigest}.lean] Revision 3 rechecked design/exporter, partial transport/cache and collision sections, plus
StepCases, DemandPreservation, HypothesisLedger and the proofeng STATUS record. B rereads covered statement-audit/non-vacuity/residual-census sections,
FloorCensus's schema/coverage/flow, Blake3FloorReduce's correction, HierarchicalGraphCommitment/RomSuccessor collision statements, and CheckpointPrune's
actual attestation binder and proof. Earlier memo citations retained outside these rereads remain source readings of the same pinned snapshots, not
fresh whole-library audits.

[MEASURED] This lane created no worktree, build, test, judge, helper job or PID file, and changed no repository. All repository inspection was on hbox
over ssh; local access was to the requested records and cv. The proposed exporter, mutation matrix, repair comparisons and workflow have not been run.
Only the authorized memo and appended CX-SCHOLAR report are deliverables.
