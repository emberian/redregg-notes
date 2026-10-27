# ACTIVITIES PROPOSAL (Ember, real 2026-10-20) — three GPT documents, CONDENSED to about a third (32K of 88K chars; the header once said "verbatim" and was wrong). THE RAW TEXT: ACTIVITIES-GPT-RAW-20261020.md. Read that one.

Ember: "I'm wondering if any of this could be easier to express in nanodregg; or if nano doesn't have enough
parts and we'd need to do it with mini. Because this would be a MAJOR overhaul to core parts of our system
(finally!)" Then: "I want activities and continuations... maybe it's time to promote those things into nano.
Because we would finally have a firm theoretical, metaprogrammatic, and proof engineering basis to rest them
upon. It's about time nano captured those aspects of mini."

ROOT's read before the scholar: nano already holds the load-bearing half (versioned pins = dependency tracking
of a call on the World, `stale` = a withdrawn support, final by staleBehind_final; ObjectHistory/Std.Chain = the
interpretation theorem; the resident's Prog.interp + interp_runs + the crash-model keep/forget = a proved
continuation structure; CallFoot/submit_frame = locality; the judge (traced read-sets, carried verdicts,
attribution, fail-closed keys) = a worked ATMS). It lacks the persistent hole object (LANG-48 `Std.pending`,
approved 10-18 and never built), fill/withdraw/repair receivers, and activities themselves.

---

## DOCUMENT 1 — repair hints, guarded holes, resubstitution

Yes :) The part I'd put at the center is your "repair hints": a reasoning object that remembers both why it
currently works and where to resume reasoning if those reasons change. That gives "changing your mind" a
computational structure.

I read three connected ideas in your notes:

- Justifications remain inspectable: which assumptions support this judgment?
- Alternatives remain available: what else could support it, and why wasn't that alternative selected?
- Instantiation remains revisable: where did we commit to a particular term, representation, or proof, and can
  we reopen that commitment?

The third makes your guarded holes especially interesting. A hole could be a persistent place where a decision
is made, carrying an interface, conditions for admissible fillings, and enough retained structure to replace a
filling later.

Direct antecedents: "First-class substitutions in contextual type theory" (Cave–Pientka, LFMTP 2013); the
original ATMS paper (de Kleer 1986) discusses retaining partially attempted reasoning that might become useful
after a context change.

### 1. Dilly's distinction is useful, but the proposal introduces another operation

Removing a premise can invalidate a derivation in a monotonic logic (Γ,A ⊢ B does not give Γ ⊢ B); defeasible
reasoning adds that ADDING information can defeat a conclusion. The repair machinery operates across both and
adds: PRESERVE THE OBLIGATION, REOPEN THE CHOICE OF HOW TO SATISFY IT, AND ATTEMPT ANOTHER CHECKED CONSTRUCTION.

Example: a membership query over an immutable vector xs with contract SearchResult(xs,k) = {b : Bool | b = true
↔ k ∈ xs}. Two implementations: `binary` (requires evidence Sorted(xs)) and `linear` (requires none). With an
accepted premise s : Sorted(xs), binary is eligible and preferred. Withdraw s. A useful report distinguishes:
Sorted(xs): its recorded justification is unavailable; NotSorted(xs): no evidence supplied; the binary
candidate: its sortedness obligation is open; the linear candidate: still eligible; the membership contract:
remains established through linear; the previously established logarithmic cost bound: needs separate
reconsideration. One transition contains recovered uncertainty, a changed implementation choice, and
preservation of a higher-level judgment. If linear is only partly constructed: "membership query: suspended at
guarded hole h; remaining obligation: complete the linear-search correctness argument; retained work: input
representation, equality procedure, unaffected client derivations, previous search residual." Houyhnhnm
connection: Non-Stop Change treats code/data changes as first-class transactions, types tracking temporary
incoherence, preserving information about the intended change.

### 2. The crucial dependency is often the reason an alternative was discarded

Provenance semirings: P_J = ab + c (products = joint requirements, sums = alternative derivations). Retracting a
removes one route while c keeps J; retracting c too leaves none; reintroducing evidence for a reactivates the
first route without reconstruction. "Invalidating a proof" and "invalidating its conclusion" are different
operations. Repair hints retain MORE: "candidate P was not pursued because Q was cheaper under assumption a;
candidate R was pruned because constraint c made the branch inconsistent; candidate S was suspended because
obligation G had no witness." A change can affect THE REASON FOR SUPPRESSING A BRANCH. de Kleer 1986 asks
exactly where reasoning should resume after a context change and names unrecorded control decisions as the
source of missed solutions. Sharpened: RECORD THE JUSTIFICATION FOR A COMMITMENT, INCLUDING COMMITMENTS TO STOP
SEARCHING, DISCARD A BRANCH, OR PREFER ONE CANDIDATE. Retained objects and what each enables: another completed
derivation (switch); a conditional derivation (reactivate when its assumptions return); a partial derivation
(resume at its open obligations); a proof transformation (adapt to a changed interface); a pruning explanation
(reopen alternatives when their exclusion loses support). Grädel–Tannen (provenance semantics for FOL, reverse
provenance, repairs): specializing an expression to the current situation can ERASE branches needed to explain
later updates; negation needs richer provenance than positive polynomials. The danger in premature substitution:
you can erase the place where a future change needs to act.

### 3. "Resubstitution" needs an object that survives substitution

template₁ = x + 1 with {x ↦ 2} and template₂ = 3 both evaluate to 3; revising x to 4 should give 5 for the
first and 3 for the second; the bare result cannot tell which. A revisable computation retains ⟨t, Γ, σ, v,
dependency/residual structure⟩ (the open template, its interface, the current instantiation, the result, which
work depended on which choices); the operation ⟨t,σ,…⟩ ⇝ ⟨t,σ′,…⟩ REPLACES A REMEMBERED INSTANTIATION (distinct
from composing substitutions). Cave–Pientka give substitution variables, abstraction over substitutions, passing
them as arguments. "Substitution abstraction" has two readings: parameterize a construction over a typed
substitution (a concrete foundation exists); recover a parameterized construction from an already-specialized
result (ambiguous: the 3 example). Retaining the abstraction boundary from the beginning makes the second much
less mysterious. THE OBSTRUCTION: arbitrary retraction is not a typed substitution: with Γ = (a : A), t = a,
withdrawing a leaves Δ = ∅, and a substitution from ∅ into Γ would need a closed witness of A, which withdrawal
does not supply. Guarded holes represent the point where transport becomes partial: a replacement witness
exists (fill); a conditional construction survives (retain under its remaining interface); a search remains
possible (expose the obligation and residual); a contradiction is established (report it with its evidence). A
failed repair supplies no proof that A is false. Dependent contexts (n, xs : Vec T n, i : Fin n): changing n
needs coordinated changes; a guard can express the obligation to reuse i, it cannot make an out-of-range index
valid. PUMPKIN Pi supplies checked transformations across equivalences; an arbitrary withdrawal may have none.

### 4. A guarded hole as a persistent interface to a family of constructions

hole h: local context; required type / behavioral contract; candidate fillings; applicability conditions per
candidate; currently selected filling; suspended searches and repair procedures; dependencies of selection and
pruning decisions. The stable identity belongs to the hole; its filling can change. An occurrence h[θ]
instantiates the hole's local context; a candidate u must satisfy the required type and guard after the
instantiations. Two operations easily conflated: changing the candidate assigned to h; changing the environment
in which an occurrence of h is used. Hazelnut Live: hole closures retain environments, evaluation continues
around holes, filling resumes evaluation (fill-and-resume metatheory); reopening a filled-and-consumed
dependency needs additional revision semantics. A repair procedure returns: Verified (replacement + checked
evidence) / Suspended (remaining obligations, reusable partial construction, continuation of search) / Conflict
(incompatible evidence, explanation); possibly multiple candidates or a lazy search. A heuristic hint may be
incomplete, expensive, or unsuccessful; ITS PROPOSED REPLACEMENT ACQUIRES AUTHORITY THROUGH CHECKING. PUMPKIN's
proof-repair searches changes for reusable patches (abstraction, specialization). "A Coinductive Approach to
Proof Search through Typed Lambda-Calculi" represents proof-search alternatives as formal sums and fixed points
(a finitary representation result for intuitionistic implication; not for arbitrary dependent search).

### 5. Ludics: the guard describes admissible interaction

Orthogonality: T^⊥ = {d | ∀ t ∈ T, d ⊥ t}; behaviors closed under biorthogonality. A guarded hole specifies the
interactions a filling must support under the current assumptions: F_{h,w} = {d | admissible ∧ d ∈ T_{h,w}^⊥}.
Adding an obligation t: F′ = F ∩ {t}^⊥: a revision changes the demands at an interface and some fillings cease to
meet them (withdrawing "the caller always supplies a non-null value" enlarges caller behaviors; a filling must
tolerate it, obtain a new precondition, insert a check, or suspend). Two distinctions: a finite set of TESTED
interactions gives an over-approximation of admissibility (T_tested ⊆ T_required ⇒ T_required^⊥ ⊆ T_tested^⊥: a
proof or completeness result closes the gap); an unresolved hole needs a success criterion distinct from a
completed implementation (a daimon-like placeholder as a "repaired program" validates an object that gives up).
Transcendental syntax (Eng–Seiller stellar resolution): interaction from first-order terms and unification.
Changing a substitution can change WHICH INTERACTIONS ARE POSSIBLE, including which pieces connect: some
repairs are local, others change the interaction graph itself.

### 6. Local repair needs a boundary theorem

What does a consumer rely on at this boundary, and does the replacement preserve it? Preserved: the same typing
interface (client typing derivations reuse); the same logical contract (client proofs); the same observable
behavior (cached observations); the same cost/resource guarantees (bounds, scheduling). Binary and linear search
preserve membership; a latency guarantee may not survive. With dependent types, replacing one inhabitant can
affect types mentioning it; a locality result must specify abstraction, dependency, transport. Design
discipline: EVERY REUSABLE BOUNDARY DECLARES THE OBSERVATIONS IT PRESERVES, AND A REPAIR EITHER RE-ESTABLISHES
THAT DECLARATION OR PROPAGATES AN OBLIGATION BEYOND IT. Pruning explanations matter: a solver's discarded region
reopens when its constraint is withdrawn; the boundary was the exclusion argument. Effects: distinguish
revisable descriptions and proofs; currently authorized actions; the record of actions already performed;
explicit compensation/migration. A consumed linear resource remains consumed; an alternative computation can be
retained as code without a second copy of live resources. "Not undo": changing one's mind changes future
commitments while preserving the account of what happened.

### 7. Differential dataflow maintains the machinery; the language specifies its meaning

Maintain relations: candidate establishes judgment under support; guard depends on evidence; candidate blocked
by constraint; consumer relies on interface; repair residual waits on obligation. A negative update records
removal, not evidence of negation. Semantic decisions stay explicit: what is a valid justification; when does
absence license a default; which alternative worlds are admissible; skeptical/permissive/prioritized/unresolved
selection; when is a computation complete enough to execute. Two examples: a cycle must lose support when its
grounding disappears (p :- a. p :- q. q :- p.: withdraw a; least-fixed-point gives neither; naive counting
leaves them supporting each other); alternative worlds keep their separation (p :- not q. q :- not p.: stable
models {p} and {q}; keeping both does not justify asserting their union). Keep assumption identities stable:
withdrawing a₇ : A changes its applicability; mutating a₇ to mean another proposition corrupts every stored
derivation. Immutable, versioned premises.

### 8. An algebra of checked repair

Incremental lambda-calculus: derivatives turn input changes into output changes with a correctness relation to
recomputation. A repair operation indexed by an edit e : w ⇝ w′: repair_e : State(w) → State(w′), where a state
holds checked constructions, alternatives, open obligations, and may turn a completed judgment into a suspended
one. Desired theorem: observe_{w′}(repair_e(S)) = observe_{w′}(analyzeFromScratch(w′)) (history-dependent
selection gets the history on both sides; multiple solutions compare admissible sets). Demanded Abstract
Interpretation is the precedent (incremental + demand-driven, soundness, termination, agreement with batch).
Agreement with recomputation is only one obligation (recompute-everything satisfies it). Three separate results:
CONDITIONAL SOUNDNESS (every active judgment has checked evidence under its declared assumptions and guards);
REPAIR CORRECTNESS (the specified relationship to the new-world semantics); LOCALITY (under stated boundary
conditions repair need not inspect or rebuild the rest). First-class repair objects: pass a repair procedure;
abstract over the substitutions/edits it handles; compose repairs and expose intermediate obligations; compare
alternative repairs under an explicit cost/intent policy; preserve a residual when no candidate succeeds; check
a replacement independently of how it was found.

### 9. A small experiment

A small typed core, named contextual holes, immutable assumption tokens, a finite rule fragment, a from-scratch
reference beside the incremental one. Cases: withdraw one of two independent supports (the judgment survives
through the other); withdraw the last known support (unsupported/suspended, no negation acquired); withdraw the
reason a branch was pruned (the branch becomes available); remove the grounding of a positive cycle (the cycle
loses support); change a component of a dependent context (dependent substitutions repaired or obligations
exposed); replace a filling preserving its exported contract (client proofs stay usable); preserve correctness
but lose a cost guarantee (two statuses); reapply an earlier filling (retained structure reused where still
valid). Measure WHY work was revisited (invalidated supports, reopened branches, discharged obligations, changed
interfaces, preserved boundaries). Resource tradeoff: a compact shared representation, known alternatives,
suspended searches, with completeness limits exposed: "no retained repair succeeded" ≠ "a proof establishes the
obligation cannot be satisfied." Three papers beside the notes: First-class substitutions in CTT; An
Assumption-Based TMS; Provenance Analysis and Semiring Semantics for FOL. The most fertile question: CAN A
REASONING NODE EXPOSE A TYPED INTERFACE FOR THE WAYS ITS OWN COMMITMENT CAN BE REVISED? The piece not to erase:
the reason an alternative was set aside.

---

## DOCUMENT 2 — open protocols as typed families of continuations (read against dregg 22fad151 and mini 334316d)

The productive connection: AN OPEN PROTOCOL AS A TYPED, INSPECTABLE FAMILY OF POSSIBLE CONTINUATIONS, WITH
EXPLICIT OBLIGATIONS FOR MAKING A PARTICULAR CONTINUATION EXECUTABLE. Mini already has: checked instantiation of
open templates, response-dependent programs, selective transport of authorization evidence, dependency-based
validity, durable obligations.

### 1. Several ways a protocol can be open

An UNSPECIFIED COMPONENT (provider, price, implementation, witness, contribution): resolved by typed
substitution/instantiation. An INTERACTION WITH AN ENVIRONMENT (a peer may accept, refuse, respond differently,
stay silent): composition with a participant satisfying an interface. An UNFINISHED EXECUTION (a request
dispatched, outcome unresolved): a transition preserving history and outstanding obligations. Contextual types
[Ψ ⊢ A] (CMTT: metavariables and substitutions with a disciplined account of scope) address the first. A
judgment schematically Ω;Γ;Δ ⊢ P : Protocol_Σ(i, A) ⊣ Φ (Ω unresolved components + interfaces; Γ reusable
data/handles/evidence; Δ accounted resources; Σ available interactions, i the index; Φ obligations for
particular completions). A hole carries u :: [Γ_u; Δ_u ⊢ Protocol(I_u)] plus guards, authority, shared
transaction parameters, WHO CONTROLS THE CHOICE: an implementation we may choose and a response another
participant chooses cannot have interchangeable meanings. A hypothetical context ≠ a future runtime state:
adding a variable is structural weakening; a later epoch can revoke authority or consume a token; a contextual
modality does not transport present authorization into every future state.

### 2. Mini's two foundations

Open templates have a checked instantiation discipline (MODULAR-TYPING: declarations checked against rigid Self
and Super bounds; `Discharges.check_instantiate` in Theory/ObjectiveBendTemplates.lean:1033-1040: a checked
template remains accepted after a substitution satisfying Discharges). Responses determine the continuation's
type (Theory/IndexedProgram.lean: operations at an index, a response type per operation, the next index
determined by the response: k : Π (r : Resp(op)) Program Σ A (next(op, r)); fold_fusion/fold_rel relate
interpretations; the Activity design: yield a plan, resume on a typed response; a counter returns the increased
count after a successful write or the original after refusal). Together: a contextual package containing a
protocol continuation that can be instantiated, inspected, and run.

### 3. Guarded holes give an admission boundary; planning stays more open

Dregg's GuardedHole fixes a field, actor, target, guard list, accepts an integer later. Mini's GuardedAdvice fixes
identity, value code, turn, pre-root, authority demand, footprint, commitments, deadline, continuation,
nullifier domain; advice dependently typed by the spec; commit checks the retained root and consumption. The
"eager shape, lazy witness" boundary needs a staging qualification: AN ADMITTED TRANSITION NEEDS A COMPLETE,
AUTHORIZED INTERPRETATION; AN UNFINISHED PLAN CAN DESCRIBE A FAMILY OF SUCH TRANSITIONS (Σ p : Provider, Σ c :
Contribution(p), Implements(p, c, I)). Two designs: elaborate an open plan into the existing admission shape; or
an admission interface over a family of contributions (a fixed interpreter + acceptance contract). Closure can be
incremental: admit one concrete action while retaining open continuations.

### 4. Intents = constrained substitution

A completion space C_w(P) = {θ | Typed(θ) ∧ Guards_w(P[θ]) ∧ Authority_w(P[θ]) ∧ Resources_w(P[θ])}: the SAME θ
must satisfy all conditions ((∃x B(x)) ∧ (∃x S(x)) ⇏ ∃x B(x) ∧ S(x): buyer ≤ 5 and seller ≥ 7 have no shared
price). Dregg's Hyperedge: all incidences bind to one shared turn identity. The matcher's greedy `can_satisfy`
scores 0.5 where an alternative assignment satisfies both wants: SEARCH STATE ≠ LOGICAL STATUS. An open intent
retains: the current partial substitution; constraints per unresolved choice; why assignments failed;
alternatives available; verified witnesses for the parts established.

### 5. Polarity and causality

A producer promising g ∧ h narrowed outputs; a receiver accepting only g ∧ h narrowed tolerated inputs; a solver
adding h narrowed candidates: different replacement consequences. Interface automata (de Alfaro–Henzinger):
alternating simulation with opposing input/output variance. Put OWNERSHIP AND POLARITY in a hole's interface:
who chooses; who must accept; is a change a refinement, a restriction on candidates, or a renegotiation. Available
information constrains substitution: ∀E ∃θ Success(P[θ], E) ≠ a CAUSAL strategy choosing from observations
actually available; an unresolved peer response stays an interaction with a response-dependent continuation,
never a freely instantiable existential (that would give the planner foresight no participant has). Division:
contextual typing = valid instantiation/dependency; the protocol interface = control, permitted interactions,
assumptions; the execution semantics = when information becomes available.

### 6. Which proofs survive? Mini's concrete answers

`Capability.Admissible.at_policy_revision` (TypedAuthorization.lean:1210-1245) transports semantic capability
admission to a new policy revision keeping other fields fixed; full authorization still has separate
obligations (request-bound evidence; current policy membership; acceptance by the current policy). A repair
result: THESE subderivations remain valid under this transport; THOSE obligations have reopened. A conditional
derivation d : [h : A ⊢ Q] survives the loss of its current instantiation: retain it and its dependency; invalidate
the binding; expose the obligation; try another binding or derivation; losing this justification does not
establish ¬Q. If the PROPOSITION changes, repair needs an explicit transport/refinement. PlanBinding.lean's
no_toctou: an admitted footprint preserves patch validity and values written; unrelated addresses keep their
values; independence conditions for order-insensitivity: A DERIVATION REMAINS REUSABLE WHEN THE OBSERVATIONS ITS
JUSTIFICATION DEPENDS ON REMAIN APPROPRIATELY EQUAL. CanonicalReactiveView: explicit dependency sets, clean/dirty
deltas, invalidation causes; sufficient dependency sets, not minimal; dirty = potentially affected.

### 7. Partiality visible in the result type

GuardedAdvice distinguishes acceptance, rejection, pending, expiry, unsupported, backend unavailable; LawSat
distinguishes unsupported fragment, unrealizable old-state observation, cap exceeded, decided. Keep statuses:
WITNESSED (a particular completion checked) / OPEN or BLOCKED (named obligations remain) / REFUTED (a checked
impossibility argument) / OUTSIDE THIS PROCEDURE. Dregg's Pred.eval makes a missing symbolic field a false atom
whose negation is true: coherent Boolean evaluation over the represented state, not a semantics where an
unknown future filling stays unknown under negation: an open evaluator suspends with its residual or uses an
explicit partial semantics.

### 8. An executed prefix leaves obligations

Mini's six authority cuts (Observe / Invoke / Reserve / Install / Release / Retire); yesterday's acceptance can
stay true while today's role change prevents installation. The identity contract (one semantic invocation vs its
attempts, generations, transport nonces); the portable continuation (an uncertain external call keeps its request
context and custody while its outcome is reconciled). Before dispatch, changing the provider is a candidate
substitution; after dispatch with a lost reply, the old provider may have acted: a new choice must reason about
the outstanding invocation, its outcome, compensation. Theorem target: REPLACING AN UNEXECUTED COMPONENT PRESERVES
THE ACCEPTED HISTORY AND THE OBLIGATIONS IT ESTABLISHED. Resource discipline follows the actual resource (reusable
authority, generative introduction, conserved assets, one-shot resolution rights differ); Contextual
Metaprogramming for Session Types (contextual code with linear + unrestricted resources, code transmitted and
instantiated through typed communication; preservation, sequential progress; no general deadlock freedom).
Compatibility alone cannot promise a peer resolves a hole (interface automata permit a legal environment that
supplies no inputs).

### 9. The first-class object

(P, Ω, σ, D, support, Φ, t): the retained template, its open interface, the current partial substitution, the
available derivation, its dependencies, the residual obligations, the accepted interaction history. RETAINING THE
TEMPLATE SEPARATELY FROM ITS ENVIRONMENT IS CENTRAL TO RESUBSTITUTION. Four theorem families: CONTEXTUAL
COMPLETION (a replacement satisfying the hole's typing/resource/polarity interface preserves the surrounding
contract); INTERPRETATION OF SUBSTITUTION (interpreting an instantiated protocol agrees with interpreting its
template under the environment; shared parameters and operation identities stay correlated); SELECTIVE REPAIR (a
change outside a fragment's support permits certified reuse; an affected fragment produces explicit residual
obligations; completed repair agrees with from-scratch); ADMISSION AND HISTORY PRESERVATION (concrete effects
need current admission evidence; edits to the remaining protocol preserve the executed prefix). First experiment:
a two-party quoted service (unknown provider and price, a shared request identity, a resource reservation, a
response-dependent continuation); four changes: replace the quote, revise the policy, modify an unrelated store
address, lose the reply after dispatch: each forces the theory to say which operation it is (substituting a
candidate, transporting a surviving proof, reopening an obligation, advancing a started interaction).

---

## DOCUMENT 3 — peers and precedents (the reference library)

Three connected problems: a verified implementation platform for dynamically extensible reasoning; a programming
environment where open proofs, programs and protocols are first-class; a distributed execution model connecting
those objects to authority, durable state, actual effects. Reference set: CertiKOS (contextual refinement across
layers); Nuprl/EventML (constructive specifications connected to executable distributed processes with a proved
correspondence); Disel (compositional protocol verification: framing, invariant strengthening); Grove/Perennial
(concurrent durable systems with crash recovery, reconfiguration, leases); IronFleet/Verdi (refinement steps for
fault tolerance); Velisarios (mechanized PBFT); Pulse/PulseCore (dependently typed concurrency with intrinsic
separation logic; PLEDGES = conditional results usable after other work completes); Ironclad Apps; Fabric and
Nexus (distributed persistent objects with information-flow policies; authorization informed by credentials and
reasoning about code). Prover platforms: Candle (an ITP whose soundness extends through its dynamically compiling
implementation to machine code; the authoritative output is a kernel-controlled channel serializing the theorem
AND its logical context: a design reference for what evidence that leaves an environment means); Cakes That Bake
Cakes (verified runtime compilation); Fast, Verified Computation for HOL ITPs (a verified evaluator; 14.5 h →
45 min); BRacK (a verified Scheme compiler via CakeML; Scheme → CakeML, a counterpart to ML → tinylisp);
Milawa/Jitawa. Protocol programming: EventML; Kalas (a verified end-to-end choreographic compiler through CakeML
to machine code with a seL4 deployment; its compiler proofs NOT connected to the seL4 proofs; assumes reliable
delivery); Toninho–Caires–Pfenning "Higher-Order Processes, Functions, and Sessions: A Monadic Integration"
(ESOP 2013): THE LINEAR CONTEXTUAL MONAD HAS OPEN PROCESS EXPRESSIONS AS VALUES recording the channels/services
required and the service offered: a precise starting point for an unfinished protocol ("here is the interaction
I implement; the endpoints and resources I require; the service I provide once supplied"); instantiation =
typed composition; Actris 2.0 (messages with the resources they transfer); Aneris/RCLib (dependent protocols
over UDP, RPC, a replicated store; exclusions: crash recovery, reconnection, progress, network security). The
sequence: open process values → resource-sensitive protocol contracts → verified transport. Contextual types:
CMTT; first-class substitutions; Beluga. Interpretation: WHEN CIRCUMSTANCES CHANGE, RETAIN THE CONDITIONAL
ARTIFACT AND RECONSIDER WHICH INSTANTIATIONS REMAIN ADMISSIBLE; distinguish substitution / withdrawal / repair /
commitment; a contextual type [Γ]A does not mean A stays available in every future distributed world
(consumption, expiry, revocation need their own semantics). Proof repair: Pumpkin Pi (checked equivalences;
quotient type equivalences 2025): a hint identifies a correspondence/transport/missing lemma, the engine proposes,
the checker decides. Hazelnut Live: evaluate around holes, retain closures, resume after a fill; no speculative
external effects. THE CLOSEST PRECEDENT FOR GUARDED FILLS: Morgenstern–Garg–Pfenning, A Proof-Carrying File
System with Revocable and Use-Once Certificates (LPCFS, STM 2011): an offline verifier checks a proof and issues
a signed capability; at access time the reference monitor checks revocation and atomically consumes the use-once
certificates in the same transaction: USING A RESOURCE ONCE INSIDE ONE PROOF DOES NOT PREVENT REPLAYING THE
ENTIRE PROOF IN ANOTHER REQUEST, so a distributed OS needs both the logical resource discipline and a durable
implementation of consumption; maps to mini's HoleSpec / Advice / VerifiedFill / commitFill. Questions a central
monitor hides: which replicated state determines availability; what identifies the consumption event; how
competing commitments resolve; what survives a crash; how the receipt binds the evidence to the transition.
Incremental reasoning: ATMS + differential dataflow (mechanism); statuses: a checked conditional artifact; a
currently justified instantiation; waiting on evidence/resources; support withdrawn; checked contrary evidence;
authority expired/consumed. CALM / invariant confluence: which updates proceed independently, per operation.
Synthesis: give an open artifact a stable identity (program/proof/protocol fragment; logical context and
interface; resource requirements and effect spec; state dependencies/read footprint; checked evidence and
unresolved obligations) that survives changes of world; revalidate the dependencies that matter (an unrelated
change; a used dependency; a changed AUTHENTICATED REPRESENTATION of an unchanged semantic dependency, e.g. a
Merkle opening refreshed because the root moved); certificate acceptance explicit about the logic (OpenTheory;
the verified checker for Isabelle's metalogic); separate derivability from current admission (an acceptance spec
binds the selected code and effect, the assumptions used, the authority exercised, the footprint, expiry and
revocation, durable consumption, the receipt's transition); state progress obligations separately (pledges;
Lawyer OOPSLA 2026 modular liveness; LinearActris deadlock freedom); expose the assumptions needed for progress.
First integration experiment: TWO CELLS NEGOTIATE A ONE-USE CAPABILITY, WITH ALTERNATIVE PROVIDERS, A DEADLINE,
AND A CANCELLATION PATH; four changes: an unrelated state update (the plan stays usable); withdrawal of one
provider's authority (that instantiation unavailable, the conditional protocol and other candidates remain); a
change of representation (a checked correspondence supports transport); competing or replayed commitments
(durable consumption permits at most one use). Proof objectives: substitution preserves the open artifact's
judgment; unchanged dependencies preserve applicability; accepted repairs produce valid artifacts; commitment
binds the checked artifact to the authorized transition; recovery preserves the consumption invariant; progress
under an explicit environment assumption; at-most-once consumption of an internal token ≠ exactly-once external
execution. Reading order: Candle / Cakes That Bake Cakes / Fast Verified Computation; BRacK / the CakeML backend;
LPCFS; CMTT / first-class substitutions / Beluga; Higher-Order Processes… / Disel; EventML / Kalas; Actris /
RCLib / Grove; Hazelnut Live / Pumpkin Pi / ATMS.
