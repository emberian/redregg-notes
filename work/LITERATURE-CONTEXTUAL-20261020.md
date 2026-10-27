# LITERATURE-CONTEXTUAL (real 2026-10-20): what the papers actually say, against the GPT-6 digest and the landed nano closure

Scope. The three GPT-6 documents (`ACTIVITIES-GPT-RAW-20261020.md`, cited below as RAW:<line>) cite ~25 papers; nano landed a
CMTT core + guarded contextual closure from them (LANG-66 `1e94183`/`56c79a0`, LANG-67 `8c31ace`, LANG-68 `2b6e5e1`, LANG-69
`b5f880b`; files `nanodregg/Lang/Contextual/*.lean`, `Lang/Proofs/Contextual/*.lean`). This file checks each citation at the source,
then widens to what the GPT did not cite. PDFs live in `/Users/ember/paperbin/` with a `.txt` sibling from `pdftotext`.

Evidence tags: **READ (file, pdf page)** = I read the passage in the PDF (page = PDF page, not printed page unless stated);
**READ-SCRY (paper_key)** = read in Scry's `academic.papers` full text; **SCRY (query)** = metadata row in `academic.catalog` /
`openalex.works`; **INFERRED** = my own knowledge or reasoning, not checked at a source this session.
Verdict tags: CONFIRMED / OVERSTATED / WRONG / COULD NOT CHECK.

Papers fetched this session: **31** (listed in §6). Re-used from paperbin: 3. Read through Scry full text without fetching: 7.

---------------------------------------------------------------------------------------------------------------------------------

## §1 The GPT's claims, checked one by one

### 1.1 Nanevski–Pfenning–Pientka, "Contextual Modal Type Theory", ACM TOCL 9(3), 2008
DOI 10.1145/1352582.1352591 · file `nanevski2008-contextual-modal-type-theory.pdf` · RAW:625, RAW:1101
- GPT: "metavariables and substitutions become objects with a disciplined account of scope and dependency."
- Paper, abstract (READ p1): "Contextual modal type theory provides an elegant, uniform foundation for understanding meta-variables
  and explicit substitutions." §7 (READ p34–35): "A meta-variable u::A[Ψ] can depend exactly on the parameters in Ψ. All occurrences
  of u in a term have the form clo(u, σ) … σ is a mediating substitution"; and "Since dependent type theories reify proofs as objects,
  unsolved subgoals can also be represented as meta-variables."
- **CONFIRMED.** Two caveats the GPT omitted (READ p34–35): (a) the metavariable reading of §7 uses the DEPENDENT CMTT of §5, and
  question (2), "what constraints does the type theory impose on occurrences of meta-variables in the contexts or types of other
  meta-variables?", only arises there; (b) instantiation is one-way: the paper has no withdrawal, revision or un-instantiation.
- For us: `Lang/Contextual/Core.lean` is the simply-typed fragment (Thms 4.1–4.5 analogues `subst_lemma`, `msubst_lemma`,
  `subject_reduction`), so it carries no meta-context ordering, and everything about revision (`repair`, `withdraw`) is OUR addition.
  CMTT gives it no support.

### 1.2 Cave–Pientka, "First-class substitutions in contextual type theory", LFMTP 2013
DOI 10.1145/2503887.2503889 (INFERRED DOI) · file `cave2013-first-class-substitutions.pdf` · RAW:215, RAW:1101
- GPT: substitution variables; "abstract over substitutions, pass them as arguments, and return them as results"; "abstraction,
  composition, explicit substitution variables"; connects to Beluga.
- Paper (READ p1): "allowing programmers to abstract over substitutions, to pass them as arguments and return them as results"; it
  enforces "a canonical structure for substitutions, i.e. there is exactly one way to write a substitution", gives a decidable
  bidirectional system, and mechanizes "these properties restricted to the simply-typed setting in Agda". Its motivating uses are
  weakening/exchange between contexts and logical-relations environments (READ p1–2).
- **CONFIRMED.** "Composition" here means composition of substitutions (stuck composition `id_ψ[s[σ]]`, READ p5). It is not
  composition of repairs.
- For us: the deferred card (cv task 01a1587d-9a98) is legitimate, but the paper supports only **substitution-shaped edits**
  (context morphisms: weakening, strengthening, exchange). P4's `Repair` indexed by an edit `w ⇝ w'` is first-class-substitution-like
  ONLY for the `strengthening` outcome; a token withdrawal is not a substitution, and the paper says nothing about that case.

### 1.3 de Kleer, "An Assumption-based TMS", Artificial Intelligence 28, 1986
DOI 10.1016/0004-3702(86)90080-9 · file `dekleer1986-assumption-based-tms.pdf` · RAW:144, RAW:595, RAW:1172
- GPT: de Kleer "explicitly asks where reasoning should resume after a context change, discusses failed or partially attempted rules …
  and identifies unrecorded control decisions as a source of missed solutions or redundant recomputation. His proposed interface
  makes those decisions visible."
- Paper (READ p4 = printed p130): "where should the problem solver start working? … there may have been rules which were attempted
  and failed or only partially attempted in old contexts … If we ignored these rules, then the problem solver would miss solutions. If
  we were to rerun these rules, then we would make redundant inferences." Then: "De Kleer, in [8], outlines an interface protocol …
  The difficulties arise when the problem solver is permitted to make a control decision … without informing the TMS … all control
  decisions must be communicated explicitly to the TMS."
- **CONFIRMED with an attribution slip.** The passage is real and says what the GPT says. The protocol itself is in de Kleer's earlier
  paper [8] (AAAI-84, "Choices without backtracking", INFERRED title); the 1986 paper only points to it.
- The definition the GPT did not quote is the important one (READ p19 = printed ~145): "The task of the ATMS is to guarantee that each
  label of each node is **consistent, sound, complete and minimal** with respect to the justifications."
- For us: our `provenance` (Closure.lean:240) is an ATMS-like label (a list of (supports, blockers) environments) with soundness
  (`provenance_iff`, one direction) but no **minimality** and no **nogood database**. See §4 item 3.

### 1.4 Green–Karvounarakis–Tannen, "Provenance semirings", PODS 2007
DOI 10.1145/1265530.1265535 · file `green-karvounarakis-tannen-provenance-semirings-pods2007.pdf` (pre-existing) · RAW:115
- GPT: "multiplication records joint requirements and addition records alternative derivations."
- Paper (READ p3): union/projection combine tags by "+", natural join by "·" ("for union we add multiplicities while for join we multiply
  them"). Prop 4.2 (READ p4): "For any valuation v : X → K there exists a unique homomorphism of semirings Eval_v : N[X] → K".
  Thm 4.3: "q(R) = Eval_v ∘ q(R̄)" for **RA+** queries. Datalog uses formal power series N∞[[X]] (READ p7).
- **CONFIRMED** for the positive fragment. The GPT did not say that GKT 2007 is positive-only (RA+ / positive Datalog).
- For us: our provenance carries **blockers** (negative literals), so GKT does not cover it. The right reference is Grädel–Tannen's
  dual-indeterminate N[X, X̄] (1.5).

### 1.5 Grädel–Tannen, "Provenance Analysis and Semiring Semantics for First-Order Logic", arXiv 2412.07986 (2024)
file `gradel-tannen-provenance-analysis-semiring-semantics-fol-2412.07986.pdf` (pre-existing) · RAW:162, RAW:596
- GPT: covers reverse provenance, updates, missing answers, repairs; "specializing an expression to the current situation can erase
  branches needed to explain later updates"; "negation requires richer provenance than ordinary positive polynomials."
- Paper: Def 4 (READ p9): "N[X, X̄] the quotient of the semiring of polynomials N[X ∪ X̄] by the congruence generated by the
  equalities p·p̄ = 0". §6 (READ p19), on updating a model-defining β by deleting facts: "setting p = q = 0 … would result in the
  polynomial 0. Of course this cannot be right … in β we already had the literal ¬Eab interpreted as 0"; the fix is to use the
  model-compatible π and specialize. Prop 16 (READ p23): "For every monomial m of π[[ψ]] the set R_m … is a repair … for every repair R
  … there is a monomial m … R_m ⊆ R. If R is a minimal repair, then R_m = R."
- **CONFIRMED** on all three counts. The update-erasure lesson is §6, the repair theorem is Prop 16, and negation is handled by dual
  indeterminates with p·p̄ = 0.
- For us (this matters): `provenance I env cs` is world-free in TOKENS, which is the model-compatible form and correct. But it is
  **specialized in the environment**: it filters candidates by `I.guard env c.filling` and `c.cost ≤ I.budget` before building
  monomials (Closure.lean:242). That is the §6 pitfall in exactly the shape the paper warns about. After an environment edit, a candidate
  that failed the guard has no monomial, so the polynomial cannot explain or predict it. `provenance_iff` is true, but only at a fixed
  env. See §4 item 1.

### 1.6 Omar–Voysey–Chugh–Hammer, "Live Functional Programming with Typed Holes" (Hazelnut Live), POPL 2019
arXiv 1805.00155 · file `omar2018-hazelnut-live.pdf` · RAW:307, RAW:1140
- GPT: hole closures retain environments, evaluation continues around holes, fill-and-resume with metatheory; "reopening a previously
  filled and consumed dependency would require additional revision semantics"; "does not authorize speculative external effects."
- Paper: abstract (READ p1): "evaluation proceeds around holes, tracking the closure around each hole instance … Hole closures also
  enable a fill-and-resume operation". Thm 4.2 (READ p22): "If ∆, u::τ′[Γ′]; ∅ ⊢ d1 : τ and ∆; Γ′ ⊢ d′ : τ′ and d1 ↦* d2 then
  [[d′/u]]d1 ↦* [[d′/u]]d2." Then: "filling commutes with reduction only for languages where evaluation order 'does not matter' …
  Languages with non-commutative effects do not enjoy this property."
- **CONFIRMED.** The revision point is the GPT's inference, and a fair one: fill-and-resume covers only "edits that amount to hole
  filling" (READ p3). The effects point is understated: the paper makes purity a *precondition* of the commutativity theorem.
- For us: `repair_agrees_from_scratch` is our analogue of Thm 4.2, at the level of judgment rather than reduction. Any attempt to
  "resume" a hole whose consumer is a TURN (effects on cells) falls outside Hazelnut Live's theorem by its own statement. P8's
  integration experiment must re-execute, never fill-and-resume across a committed effect.

### 1.7 Ringer et al., "Proof Repair across Type Equivalences" (PUMPKIN Pi), PLDI 2021
arXiv 2010.00774, DOI 10.1145/3453483.3454033 · file `ringer2020-pumpkin-pi-proof-repair-equivalences.pdf` · RAW:271, RAW:1132
- GPT: "supplies checked transformations across suitable equivalences"; "transforms proofs using checked equivalences … and produces
  suggested proof scripts."
- Paper (READ p7): "produces a term that Coq type checks, and so does not add to the trusted computing base. As Pumpkin Pi is an
  engineering tool, there is **no need to formally prove the transformation correct**". (READ p8): "we get the completeness result
  (proven in Coq) that every equivalence induces a configuration. We also obtain an algorithm for the soundness result that every
  configuration induces an equivalence." (READ p11): "Decompile deliberately **forfeits soundness** to suggest more useful tactics."
- **OVERSTATED.** The equivalence is checked. The transformation is not verified: it is translation-validated, because Coq re-checks
  its output. The suggested scripts are explicitly unsound.
- For us: P4's `transported` outcome must carry the *re-judged* filling at A′ as its evidence (`judge I' w (transport c) = .verified`),
  not a trusted transport function. That is what PUMPKIN Pi actually does, and it matches repo law (behavioural ≠ verified).

### 1.8 Viola–Fan–Ringer, "Proof Repair across Quotient Type Equivalences", OOPSLA 2025 (the GPT's "2025 follow-up")
arXiv 2310.06959, DOI 10.1145/3763164 · file `viola2023-proof-repair-quotient-equivalences.pdf` · RAW:1132
- GPT: "extends this direction toward representations where multiple concrete values correspond to one abstract value."
- Paper (READ p1): "We extend this proof repair algorithm so that it can express certain **changes in behavior** that were previously out
  of scope … equivalences between quotient types … since Rocq lacks quotient types entirely, our extensions use Rocq's setoid machinery
  … We also perform manual proof repair in Cubical Agda … which allows us to construct the **first ever internal proofs of correctness
  for proof repair**."
- **CONFIRMED**, and the GPT undersold it. The paper's point is behaviour change, plus internal correctness in a univalent setting.
- For us: Lean has `Quot` natively, so P2's binary-vs-linear search experiment can use a quotient equivalence (equal up to the observable
  `membership`). Transport along it is a *theorem*, not a re-check. That is stronger than 1.7 and available to us.

### 1.9 Espírito Santo–Matthes–Pinto, "A coinductive approach to proof search through typed lambda-calculi", APAL 2021
arXiv 1602.04382, DOI 10.1016/j.apal.2021.103026 · file `espiritosanto2016-coinductive-proof-search.pdf` · RAW:334
- GPT: formal sums and fixed points represent proof-search alternatives; finitary representation result for intuitionistic implication
  only.
- Paper (READ p1): "Formal sums are used in both representations to express alternatives in the search process, so that not only
  individual solutions but actually solution spaces are expressed … The main result is the existence of an equivalent finitary
  representation for any full solution space expressed coinductively"; the case study is "LJT for intuitionistic implication logic".
- **CONFIRMED**, including the restriction.
- For us: our retained candidates per hole are a finite formal sum. The paper's finitary greatest-fixed-point syntax "allows the
  detection of cycles through the type system", which is a typed route to P3's grounded cycles (see §4 item 6).

### 1.10 Ludics: Girard "Locus Solum" (MSCS 2001) via Fouqueré–Quatrini, "Incarnation in Ludics and maximal cliques of paths", LMCS 9(4:6), 2013
arXiv 1307.1028 · file `fouquere2013-incarnation-ludics.pdf` · RAW:340–402
- GPT: T^⊥ = {d | ∀t∈T, d ⊥ t}; "behaviors are closed under biorthogonality"; "successful closed interaction reaches the daimon, and
  certain replacements by daimon preserve behavior membership"; hence a daimon-like placeholder could pass as a repair.
- Paper, Def 2.16 (READ p11): "R belongs to D^⊥ if [[D, R]] = Dai … E^⊥ = ∩_{D∈E} D^⊥ … E is a behaviour if E = E^⊥⊥." (READ p25):
  "One of the easiest kind of designs of a biorthogonal that may be clearly generated from already known designs concerns those
  obtained by **replacing subtrees by daimons**." Def 5.1 (READ p24): "D is material in B if D = |D|_B. The incarnation |B| of a
  behaviour B is the set of its material designs"; Def 5.5 (p26) "daimon closure".
- **CONFIRMED** on the mechanics. **OVERSTATED** on the gap: "the language needs an explicit distinction" reads as if ludics lacks one.
  Ludics has two native tools. **Incarnation/materiality** keeps only the part of a design actually visited by the orthogonal (READ p3:
  "those that are really visited during the interaction with E^⊥"). And Girard's daimon-free ("winning") designs are the proofs, as
  against paraproofs (INFERRED from Locus Solum; I did not fetch it, so COULD NOT CHECK).
- For us (P1): the "tested ⊆ required ⇒ required^⊥ ⊆ tested^⊥" theorem is antitonicity of a Galois connection, true and nearly free.
  The ludics content worth importing is **incarnation**: a filling verified against T_tested should record the *material* part, the
  sub-filling the tests actually visited. Then "verified" says what was exercised, and a daimon-padded filling is not material where it
  gave up.

### 1.11 Eng–Seiller, "Stellar Resolution: Multiplicatives", arXiv 2007.16077 (2020)
file `eng2020-stellar-resolution.pdf` · RAW:404
- GPT: interaction from first-order terms and unification, "with separate proof-like conditions in its logical correspondence."
- Paper (READ p1–2): "a new asynchronous model of computation named Stellar Resolution based on first-order unification … how it can
  represent multiplicative proof-structures, their cut-elimination and the correctness criterion of Danos-Regnier" (Thms 48, 55; MIX
  Thms 73, 75).
- **CONFIRMED**, but the scope is MLL (multiplicatives) only, which the GPT did not mention.
- For us: no landed card should cite it as more than an analogy. Nothing in P1–P8 needs it.

### 1.12 de Alfaro–Henzinger, "Interface Automata", ESEC/FSE 2001
DOI 10.1145/503209.503226 (INFERRED DOI) · file `dealfaro2001-interface-automata.pdf` · RAW:805, RAW:958
- GPT: refinement with opposing input/output variance via alternating simulation; a legal environment may supply no inputs, so
  "eventually arrives" needs extra assumptions.
- Paper, Def 14 (READ p10): "alternating simulation from Q to P if … ExtEn^I_P(v) ⊇ ExtEn^I_Q(u) and ExtEn^O_Q(u) ⊇ ExtEn^O_P(v)" (the
  refinement accepts at least the inputs and emits at most the outputs). Thm 4 (p10): refinement is substitutive under compatibility.
  (READ p8): "the one that accepts all outputs of P‖Q, and that generates no inputs … This points to a limitation of interface
  automata: while the environment assumption of an automaton can express which inputs may occur, it cannot express which inputs must
  occur."
- **CONFIRMED** on both claims.
- For us (P5): state `refines` as Def 14's inclusion pair and prove the *substitutivity* theorem (Thm 4: P ≼ Q, Q‖R compatible ⇒ P‖R
  compatible) as well as the narrowing counter-example. The counter-example alone is the weaker half. `no_foresight` (LANG-67) is the
  same limitation the paper states (READ p8).

### 1.13 Cai–Giarrusso–Rendel–Ostermann, "A Theory of Changes for Higher-Order Languages", PLDI 2014
arXiv 1312.0658 · file `cai2013-theory-of-changes.pdf` · RAW:517
- GPT: derivatives turn input changes into output changes, with correctness against recomputation.
- Paper (READ p1): "f (a ⊕ da) ≅ (f a) ⊕ (Derive(f) a da)", "≅ is denotational equality", mechanized in Agda; change structures
  (Def 2.x, p2) over simply-typed λ with primitive derivatives supplied.
- **CONFIRMED.**
- For us: P4's `compose_sound` is the change-structure law. Cai et al.'s function changes compose by ⊕ (`(f ⊕ df) (a ⊕ da)`, Lemma 2.8,
  READ p3), and "nil change" (Def 2.2) is our `kept`. Adopting the change-structure vocabulary would give P4 a known-good axiom set
  (⊕, ⊖, nil, `a ⊕ (b ⊖ a) = b`).

### 1.14 Stein–Chang–Sridharan, "Demanded Abstract Interpretation", PLDI 2021
arXiv 2104.01270, DOI 10.1145/3453483.3454044 · file `stein2021-demanded-abstract-interpretation.pdf` · RAW:546
- GPT: incremental and demand-driven analysis "with cyclic dependencies and widening, proving preservation of soundness and termination
  and agreement with its batch analysis."
- Paper, Thm 6.1 (READ p10): "(DAIG From-Scratch Consistency) … if D, M ⊢ ℓ ⇒ v; D′, M′ then v = [[ℓ]]♯*"; plus query termination.
  (READ p13): "careful handling of loops ensures the DAIG **remains acyclic**."
- **CONFIRMED with a nuance.** The *program* has cycles. The dependency *graph* is kept acyclic by unrolling with widening.
- For us: the field name for our theorem is **"from-scratch consistency"** (Acar; Hammer et al. Adapton; Stein et al.). Rename or alias
  `repair_agrees_from_scratch` so readers find the lineage. Their acyclic-by-unrolling device is one design option for P3 cycles.

### 1.15 Gelfond–Lifschitz stable models (ICLP 1988) via Lifschitz, "Thirteen Definitions of a Stable Model" (2010)
file `lifschitz2008-thirteen-definitions-stable-model.pdf` (the URL the GPT cited) · RAW:499
- GPT: `p :- not q. q :- not p.` has worlds {p} and {q}; their union is not a world.
- Paper (READ p7): "M is a stable model of Π if the minimal model of … the reduct of Π with respect to M equals M." Def D (READ p8): "M
  is a stable model … iff (i) M satisfies Π, and (ii) no non-empty subset of M is unfounded".
- **CONFIRMED** as stable-model semantics. The specific two-rule example is the GPT's (standard) and does not appear in this survey.
- For us (P3): `cycle_loses_grounding` is the **unfounded-set** condition (Def D) on a one-loop program. Restate it as "the cycle {1,2}
  is unfounded w.r.t. factsNoA" so the grounding theorem has its standard name and generalizes to loop formulas (Def E, p8).

### 1.16 Toninho–Caires–Pfenning, "Higher-Order Processes, Functions, and Sessions: A Monadic Integration", ESOP 2013
file `toninho2013-higher-order-processes-monadic.pdf` · RAW:1081
- GPT: "linear contextual monad has open process expressions as values … records the channels or services it requires and the service it
  offers"; progress belongs to that calculus.
- Paper (READ p1): "a linear contextual monad that isolates session-based concurrency. Monadic values are open process expressions and are
  first class objects … We show … type preservation, as well as a global progress theorem". It builds on "the contextual comonad
  presented in [15]" (CMTT, READ p3).
- **CONFIRMED.**
- For us: LANG-67's open protocols (polarized holes, the entered prefix) are the closest landed object. The paper's monad is *linear*.
  Our affine tokens are weaker, which is a deliberate difference that should be written down (`affine ≠ linear` costs us global
  progress).

### 1.17 Hinrichsen–Bengtson–Krebbers, "Actris 2.0", LMCS 2022
file `hinrichsen2022-actris2.pdf` · RAW:1093
- GPT: messages described together with the resources they transfer.
- Paper (READ p2–3): "dependent separation protocols … allow delegation of resources, support channel sharing", with subprotocols based
  on session-type subtyping (p1).
- **CONFIRMED.** The RCLib/Aneris exclusions the GPT lists (crash recovery, reconnection, …) are from a different paper:
  COULD NOT CHECK.

### 1.18 Morgenstern–Garg–Pfenning, "A Proof-Carrying File System with Revocable and Use-Once Certificates", STM 2011
file `morgenstern2011-lpcfs.pdf` · RAW:1148–1160
- GPT: offline verifier issues a signed capability; the reference monitor checks revocation and consumes use-once certificates in the same
  database transaction.
- Paper (READ p2): "all certificates present in the justification of an access must be checked and marked consumed in a single atomic step
  … we use exclusive transactions"; "the check for certificate revocation must be made atomically with the check for use-once
  certificates"; PCFS "offlines the work of proof and certificate verification to a trusted verifier that issues a signed capability".
- **CONFIRMED.** The GPT omitted the paper's own pointer to the distributed case (READ p3): use-once certificates tracked by "a remote
  trusted party called a ratifier", with "a contract signing protocol between ratifiers" for atomic consumption, which the paper calls
  "slow in practice".
- For us (P8): KERNEL-60's counted value rights + cancel record are the in-kernel version of LPCFS's atomic check-and-consume. The
  ratifier paper (Bauer et al., INFERRED) is the precedent for the cross-cell case.

### 1.19 Abrahamsson et al., "Candle: A Verified Implementation of HOL Light", JAR 2025
DOI 10.1007/s10817-025-09743-8 (SCRY openalex W4417030735) · file `abrahamsson2025-candle-verified-hol-light.pdf` · RAW:1033
- GPT: the authoritative output channel serializes "the theorem **and its logical context**"; host OS / FFI model outside the result.
- Paper (READ p5): theorems are printed "on a special kernel-controlled FFI channel using a printer function which sits within the kernel
  … meaning that a theorem and its logical context can be recovered from the text it prints"; soundness is stated over FFI events.
- **CONFIRMED.**
- For us (P6): this is the design for certificates. Statement + context, emitted only by the kernel. It supports P6's "two certificates
  for one statement under different contexts are different certificates".

### 1.20 Sewell et al., "Cakes That Bake Cakes: Dynamic Computation in CakeML", PLDI 2023
DOI 10.1145/3591266 · file `sewell2023-cakes-that-bake-cakes.pdf` · RAW:1037
- GPT: verified runtime compilation via `Eval`; original and new code share higher-order values and call each other; open work on
  reclamation, executable memory, resource exhaustion.
- Paper (READ p1): "the original and dynamically added code can share (higher-order) values and recursively call each other … the first
  verified run-time environment capable of supporting a standard LCF-style theorem prover". Limitations (READ p3): "Code added dynamically
  is not reclaimed … Nevertheless, CakeML programs always halt with an out-of-memory error when they run out of heap, stack, or code
  memory"; x64/Linux only.
- **Mostly CONFIRMED.** Resource exhaustion is **OVERSTATED** as open: the paper says exhaustion halts with a specified OOM. Reclamation
  is the open item.

### 1.21 Hurd, "OpenTheory: Package Management for Higher Order Logic Theories", PLMMS 2009 (article.pdf)
file `hurd2011-opentheory-article.pdf` · RAW:1239
- GPT: articles expose imports/exports; destination systems replay primitive inferences under theory interpretations.
- Paper (READ p1): "Articles naturally support theory interpretations, which is the mechanism by which theories can be cleanly transferred
  from one theorem prover context to another"; an article has "an import list … an export list" (p2); on reading, an unmatched result is
  handled by "Assert the result theorem as an axiom, and add it to the import list" (READ p3).
- **CONFIRMED.**
- For us (P6): OpenTheory's import list *is* P6's "admitted assumptions". The article format says how a reader turns an unproved step into
  an import, never a silent axiom. That rule is the one to copy.

### 1.22 Ângelo–Igarashi–Murase–Vasconcelos, "Contextual Metaprogramming for Session Types", arXiv 2601.15180 (2026)
file `angelo2026-contextual-metaprogramming-session-types.pdf` · RAW:956
- GPT: contextual code with linear/unrestricted resources, transmitted and instantiated through typed communication; preservation and
  sequential progress; no general deadlock freedom.
- Paper (READ p1): "contextual values, closing arbitrary terms over a series of variables, may be boxed and transmitted in messages … We show
  type preservation, a progress result for sequential computations and absence of runtime errors for the concurrent runtime environment".
  (READ p22): "The process language does not enjoy progress due to possible occurrences of deadlocks"; deadlock freedom is set aside
  deliberately (p2).
- **CONFIRMED.**
- For us: it builds on Murase's multi-level CMTT (§2.4), the nearest published system to "a boxed hole sent to another cell" (LANG-67 +
  P8).

---------------------------------------------------------------------------------------------------------------------------------

## §2 The widened set (what the GPT did not cite)

### 2.1 Doyle, "A Truth Maintenance System", Artificial Intelligence 12, 1979 (JTMS)
DOI 10.1016/0004-3702(79)90008-0 (SCRY) · read via reprint 10.1016/b978-0-934613-03-3.50039-8 (READ-SCRY)
- "The TMS revises the current set of beliefs by using the recorded justifications to compute **non-circular arguments** … These
  non-circular arguments distinguish one justification as the **well-founded supporting justification** of each node … The TMS locates
  the set of nodes to update by finding those nodes whose well-founded arguments depend on changed nodes." Justifications have IN-lists
  and OUT-lists (nonmonotonic); contradictions trigger dependency-directed backtracking that "retracts one of the assumptions".
- For us: **our `Candidate` (supports, blockers) is a Doyle SL-justification** (IN-list = supports, OUT-list = blockers), and `judge` is
  its IN/OUT labelling. The lineage is Doyle 1979, not ATMS. The GPT cited only de Kleer.

### 2.2 Elkan, "A Rational Reconstruction of Nonmonotonic Truth Maintenance Systems", AIJ 43, 1990
DOI 10.1016/0004-3702(90)90086-f · READ-SCRY (head)
- "a precise characterization of the inferences performed by nonmonotonic truth maintenance systems … using … logic programming with the
  stable set semantics and autoepistemic logic … and a proof that implementing a nonmonotonic TMS is an NP-complete problem."
- For us (P3): this is the bridge the GPT's stable-model paragraph needed. A JTMS with OUT-lists computes stable models (Elkan). So P3's
  alternative worlds are the multiple admissible JTMS labellings of our own candidates, and the problem is NP-complete in general. P3's
  `analyzerNotFinished` status is therefore structural, not a stub.

### 2.3 Gupta–Mumick–Subrahmanian, "Maintaining Views Incrementally", SIGMOD 1993
DOI 10.1145/170035.170066 · READ-SCRY (abstract): "a counting algorithm that tracks the number of alternative derivations (counts) for each
derived tuple". (INFERRED: the paper restricts counting to non-recursive views and gives DRed for recursion.)
- For us: `counting_keeps_cycle` re-proves the known failure of counting on recursive views. Cite GMS93 in the theorem docstring and name
  the fix (DRed or well-founded re-derivation) as P3's repair procedure.

### 2.4 Murase–Nishiwaki–Igarashi, "Contextual Modal Type Theory with Polymorphic Contexts", ESOP 2023
arXiv 1801.09225 · file `murase2023-cmtt-polymorphic-contexts.pdf`
- (READ p1) "a novel extension of contextual modal type theory with parametric polymorphism over contexts … multiple parts of a single
  context can be abstracted … subject reduction, strong normalization, and confluence."
- For us (P7): `hole n σ` in the deployed Term with σ checked against the hole's context. Context polymorphism is the principled way to
  write a template that works under *any* extension of its hole context (the "typed under any ambient context" toy in LANG-66).

### 2.5 Pientka et al., "Cocon: Computation in Contextual Type Theory", arXiv 1901.03378 (2019) and "A Type Theory for Defining Logics and Proofs", LICS 2019 (arXiv 1905.02617)
file `pientka2019-cocon.pdf`
- (READ p1) "We mediate between HOAS representations and computations using contextual modal types … infinite hierarchy of universes …
  Kripke-style model … normalization … subject reduction and consistency."
- For us: Cocon is the dependent, universe-polymorphic CMTT. It is where §1.1 caveat (a) gets resolved if nano's core ever goes dependent.
  Read before any card that adds dependent hole types.

### 2.6 Jang–Gélineau–Monnier–Pientka, "Mœbius: Metaprogramming using Contextual Types", POPL 2022
arXiv 2111.08099 · file `jang2021-moebius-contextual-metaprogramming.pdf`
- (READ p1) "abstractions for both generating and **pattern matching on open code** without committing to a concrete representation of
  variable binding and contexts."
- For us (P2): a guard that *inspects* a filling's syntax is pattern matching on contextual code. Mœbius types it, which our closure
  currently leaves as an untyped `guard : E → Tm → Bool`.

### 2.7 Kavvos, "Intensionality, Intensional Recursion, and the Gödel–Löb Axiom", arXiv 1703.01288 (2017)
file `kavvos2017-intensionality-godel-lob.pdf`
- (READ p1) "data in the first region, the modal one, are available as code, and their description can be examined. In contrast, data in the
  second region are only available as values up to ordinary equality. This allows us to add non-functional operations at modal types whilst
  maintaining consistency."
- For us (P2): this is the theory behind the landed `stability_class` / `valueGuard_iff` boundary (value consumers unchanged, a
  syntax-reading consumer breaks). `ValueGuard` = the extensional region, and a syntax-reading guard = an intensional operation at box
  type. Locality must quantify over extensional consumers only, and Kavvos gives the typing discipline that makes it hold by construction.

### 2.8 Davies–Pfenning, "A Modal Analysis of Staged Computation", JACM 48(3), 2001
DOI 10.1145/382780.382785 · file `davies2001-modal-analysis-staged-computation.pdf`
- (READ p2) the binding-time framing: "it is therefore desirable to declare the expected binding-time separation and obtain constructive
  feedback when the computation may not be staged as expected."
- For us: the □ of CMTT with empty context. Our `box_ambient_free` / `box_cannot_capture` teeth are the Davies–Pfenning closedness
  property. Cite it in Core.lean.

### 2.9 Norell, "Towards a practical programming language based on dependent type theory" (PhD thesis, Chalmers 2007), ch. 3
file `norell2007-towards-practical-dependently-typed-pl.pdf`
- (READ p51) "Whenever we need to verify s : B … where we cannot yet solve the constraint A = B, we replace the subterm s by a **guarded
  constant** p of type B. This constant p will compute to s only when the constraint A = B has been solved." It also notes the approach
  could "be carried over to their [CMTT's] modal type theory" (p51). Signature entries are written `p : A = s when C` (p54).
- For us: **Agda's guarded constant is our guarded closure's ancestor**: a term that cannot reduce until its guard (a constraint) is
  discharged, with the guard stored in the signature. `mvar_blocked` / `msubst_unblocks` restate it. This is the closest prior art to
  "hole with blockers" the GPT did not cite.

### 2.10 Lean 4 `MetavarContext` (source, toolchain v4.35.0: `~/.elan/toolchains/leanprover--lean4---v4.35.0/src/lean/Lean/MetavarContext.lean`)
- (READ lines 95–115) "Metavariables may be natural, synthetic or syntheticOpaque. 1. Natural metavariables may be assigned by unification
  … 3. SyntheticOpaque metavariables are never assigned by `isDefEq` … created by tactics such as `intro` … a subgoal `?n` is considered
  as solved whenever the metavariable is assigned." (lines 57–58) "we claim it is not feasible to make the whole system backtrackable … We
  claim it would be too inefficient." (209–219) depth discipline: "When `MetavarContext` is at depth N, `isDefEq` does not assign
  variables from depth < N." The CADE 2021 Lean 4 paper (`demoura2021-lean4.pdf`) does not mention metavariables (grep, READ).
- For us: Lean's three kinds correspond to our chooser/acceptor polarity. syntheticOpaque = "only the hole's owner fills it", i.e. our
  `select … notChooser` refusal. Lean deliberately keeps **no** retained alternatives (it commits to the first type-class solution). Our
  retained candidates are the opposite choice, and the depth rule is a model for nested holes (P4's intermediate obligations).

### 2.11 Mokhov–Mitchell–Peyton Jones, "Build Systems à la Carte", ICFP 2018 (PACMPL 2)
DOI 10.1145/3236774 · READ-SCRY (full text)
- Def 2.1: "A build system is **minimal** if it executes tasks at most once per build and only if they transitively depend on inputs that
  changed since the previous build." Def 3.1 (Correctness): "for all non-input keys k ∈ O, the result of recomputing the corresponding
  task matches the value stored in the result." §4.2.2 **verifying traces**: "record the values/hashes of dependencies used last time, and
  if something has changed, the key is dirty"; constructive traces add the value; "all traces except for deep traces support **early
  cutoff**."
- For us: this is the exact analogue the brief anticipated. `repair_agrees_from_scratch` = Def 3.1 correctness. `locality` is *not*
  Def 2.1 minimality; the code comment says so itself ("Sufficient, not minimal: an environment change touches every candidate",
  Closure.lean:245). Our `deps I c` plus the re-judged log is a verifying trace without the env part. See §4 item 2.

### 2.12 Hammer–Phang–Hicks–Foster, "Adapton: Composable, Demand-Driven Incremental Computation", PLDI 2014
DOI 10.1145/2594291.2594324 · READ-SCRY (abstract)
- "recomputation is oblivious to specific demands on the program output … λcdd_ic … applies a demand-driven semantics to incremental
  computation, tracking changes in a hierarchical fashion in a novel **demanded computation graph** … explicit separation between inner,
  incremental computations and outer observers." (INFERRED: its metatheorem is named from-scratch consistency.)
- For us: `observe` in `repair_agrees_from_scratch` is Adapton's "outer observer". Demand-driven repair (re-judge only holes some observer
  demands) is the next efficiency step after minimality.

### 2.13 Porter–Kirisame–Wei–Panchekha–Omar, "Incremental Bidirectional Typing via Order Maintenance", OOPSLA 2025
arXiv 2504.08946 · file `porter2025-incremental-bidirectional-typing.pdf`
- (READ p1) "a small-step dynamics that propagates updates through the marked and annotated program … We prove this system is equivalent to
  naive reanalysis in the Agda theorem prover"; Thms 5.1–5.3 Validity, Convergence, Termination (READ p11–12).
- For us: the typed-holes line (Hazel) has now done incremental *typing* with a from-scratch-equivalence proof. That is the precedent for
  making `D.check` incremental in the closure, beyond our incremental *judging*.

### 2.14 Köhler–Ludäscher–Zinn, "First-Order Provenance Games", 2013
arXiv 1309.2655 · file `kohler2013-first-order-provenance-games.pdf`
- (READ p1) "unlike semiring provenance, game provenance also provides a 'built-in' way to handle negation and thus to answer why-not
  questions: In (provenance) games, the reason why x is not won, is the same as why x is lost or drawn"; for RA+ "game provenance is
  equivalent to … N[X]" (Thm 3, p12).
- For us (P5): `suspended (missing)` is a why-not answer and `pruned (by_)` is a why answer for a negative literal. Games give *one*
  object for both, plus a **draw** status. That is a principled home for P5's `outsideThisProcedure`: a drawn position (unfounded, cyclic)
  is neither won nor lost.

### 2.15 Dannert–Grädel–Naaf–Tannen, "Generalized Absorptive Polynomials and Provenance Semantics for Fixed-Point Logic", CSL 2021
arXiv 1910.07910 · file `dannert2020-absorptive-provenance-fixed-point.pdf`
- (READ p1) "the common approach based on Kleene's Fixed-Point Theorem for ω-continuous semirings is **not sufficient** for these general
  languages … an adequate framework … semirings that are (1) fully continuous, and (2) absorptive."
- For us (P3): once holes depend on holes through cycles *with* blockers, our list-of-monomials provenance needs an absorptive semiring
  (S∞[X]) to stay well-defined. Without absorption, `provenance_iff` does not lift to the cyclic closure.

### 2.16 Ringer–Palmskog–Sergey–Gligoric–Tatlock, "QED at Large: A Survey of Engineering of Formally Verified Software", FnTPL 2019
arXiv 2003.06458 · pre-existing file `qed-at-large-proof-engineering-survey-ringer-2019-2003.06458.pdf`
- §6.4 Proof Reuse (READ p89): "Proof reuse is the proof engineering analogue to software reuse"; §7.2 Proof Evolution (p3 TOC, p206 printed).
- For us: the survey's §7.2 taxonomy (regression proof selection, proof repair, proof reuse) is the vocabulary for the
  HOLES-FOR-PROOF-ENGINEERING memo before P6. Ringer, "Adapting Proof Automation to Adapt Proofs" (CPP 2018,
  `ringer2018-adapting-proof-automation-to-adapt-proofs.pdf`, READ p1: "leverages the history of changes … to search for a patch") is the
  GPT's RAW:332 "PUMPKIN" paper, and that claim is CONFIRMED (patch specialization and abstraction, READ p3).

### 2.17 Alchourrón–Gärdenfors–Makinson, "On the Logic of Theory Change", JSL 50(2), 1985
DOI 10.2307/2274239 · READ-SCRY (p513 printed): "(−6) A ⊆ Cn((A − x) ∪ {x}) whenever A is a theory (recovery)."
- For us: AGM is a *coherence* theory over deductively closed belief sets. Our closure is a *foundations* theory: beliefs are held only
  through recorded supports, Doyle-style. `reissue_never_reenables` deliberately violates AGM recovery for re-versioned tokens, and that
  is right for immutable versioned premises. Say so in the docstring rather than leaving a reader to think AGM is being approximated.
  (INFERRED: Doyle 1992 "Reason maintenance and belief revision: foundations vs. coherence theories" makes this split; not fetched. SCRY
  found Witteveen–Brewka 1993 "Skeptical reason maintenance and belief revision", 10.1016/0004-3702(93)90090-x, on the same bridge.)

### 2.18 Artemov, "The Logic of Justification", Review of Symbolic Logic 1(4), 2008
DOI 10.1017/s1755020308090060 · READ-SCRY: "justification assertions t:F that read t is a justification for F"; LP's "Internalization property:
If ⊢ F, then there is a proof polynomial p such that ⊢ p:F" (p480 printed).
- For us: "supports as objects" already exists as a logic. Our `provenance` monomials are justification terms of a *propositional*
  justification logic (+ = Artemov's sum `s + t`, · = application). The internalization property is what P6 certificates should satisfy:
  every `verified` candidate yields a term (its monomial) that can be checked independently of the judge.

---------------------------------------------------------------------------------------------------------------------------------

## §3 What the GPT got wrong or overstated

1. **PUMPKIN Pi "checked transformations"** (RAW:271, 1132). The equivalence is checked. The transformation is explicitly *not*
   proven correct ("no need to formally prove the transformation correct", p7), its output is re-checked by Coq, and the decompiler
   "deliberately forfeits soundness" (p11). READ.
2. **The quotient follow-up undersold** (RAW:1132). Its point is behaviour change and the "first ever internal proofs of correctness for proof
   repair" (p1), not only many-to-one representations. READ.
3. **Ludics' daimon gap overstated** (RAW:402). Ludics already separates what interaction visits (incarnation, materiality, Def 5.1 p24) from
   daimon padding (daimon closure, Def 5.5 p26). The GPT presents the distinction as something "the language needs" that ludics lacks.
   READ (incarnation); the Locus Solum winning-design point is INFERRED.
4. **de Kleer attribution** (RAW:144). The resume/control-decision passage is real (printed p130), but "his proposed interface" is in de
   Kleer [8], not this paper. The GPT also omitted the ATMS's defining guarantee, labels "consistent, sound, complete and minimal" (printed
   ~p145), which is the part our design lacks. READ.
5. **The TMS lineage**. Supports+blockers are Doyle's 1979 IN/OUT-list justifications, and nonmonotonic TMS = stable models is Elkan 1990.
   The GPT cites only the ATMS (which, as a monotone system, has no OUT-lists) and cites stable models separately, so the identity
   "our judge's alternative labellings ARE stable models" never appears. READ-SCRY.
6. **GKT 2007 cited for a design with negation** (RAW:115). GKT is RA+/positive Datalog only. Our blockers need Grädel–Tannen's
   N[X, X̄], which the GPT also cites, but it presents GKT as the core interpretation without the restriction. READ.
7. **Demanded AI "with cyclic dependencies"** (RAW:546). The program's loops are cyclic; the DAIG is kept acyclic (p13). It is a nuance,
   not an error. READ.
8. **Hazelnut Live's effect restriction understated** (RAW:1140). Purity is a *precondition* of the fill-and-resume theorem ("Languages with
   non-commutative effects do not enjoy this property", p22), not a remark about "speculative external effects". READ.
9. **CakeML resource exhaustion** (RAW:1037). The paper says programs halt with OOM (specified behaviour). Only reclamation of dynamic code
   is open (p3). READ.
10. **Stellar resolution scope** (RAW:404). The result is MLL only. The GPT did not state the restriction. READ.
11. **CMTT used as if it covered revision**. RAW:625 and RAW:1101 make CMTT "the central connection", but CMTT's instantiation is
    monotone and its metavariable account (§7) relies on the *dependent* version. Withdrawal/repair have no CMTT backing. READ.
12. **Thirteen Definitions cited for the {p},{q} example** (RAW:499). The survey does not contain that example (it uses program (6)). The
    claim is correct stable-model semantics with a loose citation. READ.

Confirmed as stated (no change needed): Cave–Pientka, Grädel–Tannen (all three claims), Espírito Santo et al., interface automata (both
claims), Cai et al., Toninho et al., LPCFS, Candle, OpenTheory, Ângelo et al., Actris 2.0 core claim, PUMPKIN PATCH (CPP 2018).
COULD NOT CHECK: Aneris/RCLib exclusions, Lawyer (OOPSLA 2026), LinearActris, Velisarios, Milawa (not in scope; not fetched).

---------------------------------------------------------------------------------------------------------------------------------

## §4 What ROOT should build or restate because of the real papers

Ordered by how directly the paper refutes or strengthens something landed.

1. **The provenance is env-specialized: make it model-compatible, or state where it stops** (Grädel–Tannen §6 p19, Prop 16 p23).
   `provenance I env cs` (Closure.lean:240) drops every candidate failing `I.guard env` or `cost ≤ budget` *before* forming monomials.
   - Build: lift the guard and budget verdicts into literals. Either env facts become tokens (the guard reads `E` through declared
     keys, see item 2), or each monomial carries a third component `envLits`. Then prove `provenance_iff` for **every** env, plus the
     update theorem: `provenance` after `Edit.apply` = `provenance` specialized (Grädel–Tannen Prop 15 shape).
   - Theorem to add regardless: `provenance_env_specialized`. Exhibit an env edit after which a candidate becomes verified while
     `provenance I env cs` has no monomial for it. This makes the current boundary a tooth rather than a silent limit.
   - Then **reverse provenance / repairs** (Prop 16): `repairs_of_provenance : ∀ m ∈ provenance …, applyAll (edits m) w ⊨ verified`,
     with the converse for minimal repairs. That is P4's "repair residual" turned into a computed object: the minimal token edits that
     would verify a hole.
2. **Locality → minimality + early cutoff** (Mokhov et al. Def 2.1, §4.2.2). Today `locality` is a sufficient no-op condition and the
   comment admits it is not minimal.
   - Build: a per-candidate **verifying trace**: the tokens `deps I c` *and* the env keys the guard read (needs `guard` to factor
     through a declared read-set, cf. `Frag.ReadsOnly` in Protocol.lean:561, which already does this for protocols).
   - Theorems: `repair_minimal` (the re-judged log = exactly the candidates whose trace meets the edit) and `early_cutoff` (a re-judged
     candidate whose status is unchanged does not dirty holes that read its selection). Name `repair_agrees_from_scratch` as
     **from-scratch consistency** in its docstring (Stein Thm 6.1; Adapton; Porter).
3. **ATMS label discipline for `provenance`** (de Kleer printed ~p145; Grädel–Tannen Def 4).
   - `provenance_complementary_dead`: a candidate with `t ∈ supports ∧ t ∈ blockers` is never verified (p·p̄ = 0). One line, and the
     disjunct-check reader will want it.
   - `provenance_minimal`: absorption (drop m′ ⊇ m), proved to preserve `provenance_iff`. This gives the ATMS "minimal" property, and
     its image is PosBool[X, X̄].
   - Nogoods: a `conflict` status today carries evidence but records no nogood environment. Add `nogoods : List (List Token)` to the
     closure and `judge_respects_nogoods` (a candidate whose supports ⊇ a nogood is `conflict`, never `suspended`). This is ATMS
     consistency, and it is what makes P5's `refuted` constructible from *recorded* evidence rather than a fresh argument.
4. **P1, guard as interactions: import incarnation, not only orthogonality** (Fouqueré–Quatrini Def 5.1 p24, Def 5.5 p26).
   - Keep `tested ⊆ required → required^⊥ ⊆ tested^⊥` (cheap, true).
   - Add `material T c` = the sub-filling visited by the interactions in T, and make `verified` carry `(T, material T c)`. The
     `gaveUp`/daimon theorem becomes: a filling whose material part w.r.t. a required interaction ends in the give-up placeholder is
     `partial`, never `verified`. This is ludics' own distinction, so the card should say so rather than present it as new.
5. **P4, repair objects: change structures + checked transport**.
   - Adopt Cai et al.'s change-structure laws for `Repair` (nil change = `kept`, `⊕`, `⊖`, `a ⊕ (b ⊖ a) = b`). `compose_sound` is then
     the standard `(f ⊕ df)(a ⊕ da)` lemma, not a bespoke axiom.
   - `transported` evidence = the **re-judged** filling (PUMPKIN Pi's real guarantee is a re-check). Where a quotient equivalence exists
     (Lean `Quot`), prove transport internally (Viola et al.). Two evidence forms, `rechecked` and `internal`, distinct by construction.
   - First-class substitutions (cv 01a1587d-9a98): scope the card to **context-morphism edits only** (`strengthening`, weakening,
     exchange), the class Cave–Pientka covers. Do not present token withdrawal as a substitution.
6. **P3, worlds: name them stable models and cite the TMS bridge** (Lifschitz Def C/D pp7–8; Elkan 1990; GMS 1993; Dannert et al.).
   - Restate `cycle_loses_grounding` as an unfounded-set theorem and `counting_keeps_cycle` as the GMS93 counting failure. Use the
     standard names and cite them in the docstrings.
   - State `admissibleWorlds = stable labellings of the candidates' IN/OUT justifications` (Elkan). Then P3's union-not-a-world theorem is
     an instance of a known property, and the "analyzer has not finished" status is justified by NP-completeness.
   - Before holes depend on holes cyclically: switch the provenance carrier to an absorptive semiring (Dannert et al.) or keep the
     dependency graph acyclic by stratification (Stein et al.'s unrolling). Pick one and write the choice in the card.
7. **P5, statuses and polarity**.
   - `refines` as de Alfaro–Henzinger Def 14 (inputs ⊇, outputs ⊆) plus **substitutivity** (Thm 4), not only the narrowing
     counter-example.
   - Model `outsideThisProcedure` on a provenance-game **draw** (Köhler et al.): a position neither won nor lost. Pair it with item 3's
     nogoods so `refuted` = "lost, with a recorded nogood" and is constructible only from evidence.
8. **P2, boundaries: use the intensional/extensional split** (Kavvos p1; Mœbius). `ValueGuard` is Kavvos's extensional region. State the
   locality theorem for extensional consumers and the breaking theorem for intensional (syntax-reading) ones as the two sides of one
   modal split. Then a syntax-reading guard can be *typed* (Mœbius pattern matching on contextual code) instead of being an untyped
   `E → Tm → Bool`.
9. **P6, certificates** (Candle p5; OpenTheory p1–3; Artemov internalization). A certificate = statement + logical context emitted only by
   the kernel (Candle). Unproved steps enter as an explicit **import list**, never an axiom (OpenTheory). Each `verified` status
   internalizes to a checkable term (its provenance monomial + the typing derivation), per Artemov's internalization.
10. **P7, holes with context in the deployed language** (Murase et al.; Norell ch. 3). Context polymorphism is the principled form of
    "typed under any ambient context". Norell's guarded constants (`p : A = s when C`) are the precedent for storing a blocked hole's
    guard in the signature, which is what the deployed `hole n σ` + the hole rows are building.
11. **P8, integration**. Do not fill-and-resume across a committed effect (Hazelnut Live Thm 4.2 needs purity). Re-execute. Cross-cell
    one-use consumption = LPCFS's single-transaction check, and the cross-cell form is the ratifier/contract-signing case the LPCFS paper
    calls slow. Say which one nano is.
12. **Docstrings to add** (no theorem changes). Core.lean cites Davies–Pfenning for `box_ambient_free`. Closure.lean cites Doyle 1979 for
    `Candidate` (IN/OUT lists) and AGM recovery as deliberately rejected at `reissue_never_reenables`. Name `repair_agrees_from_scratch`
    "from-scratch consistency".

---------------------------------------------------------------------------------------------------------------------------------

## §5 Dark coordination (Ember's other line): MPC/FHE for auctions and industrial coordination

All rows are SCRY metadata (`academic.catalog` / `openalex.works` title queries, 2026-10-20). One-line content claims marked INFERRED are
from my own knowledge, not read this session.

1. **Bogetoft et al., "Secure Multiparty Computation Goes Live"**, FC 2009, DOI 10.1007/978-3-642-03549-4_20 (SCRY openalex W1595357546,
   545 cites). INFERRED: the 2008 Danish sugar-beet contract double auction (~1,200 farmers) run as 3-party Shamir MPC (Danisco, the
   farmers' association, the SIMAP project). The canonical "MPC replaced a trusted auctioneer" deployment. (The eprint PDF fetch returned
   HTML; not read.)
2. **Cartlidge–Smart–Talibi Alaoui, "MPC Joins the Dark Side"**, AsiaCCS 2019, DOI 10.1145/3321705.3329809 (SCRY). INFERRED: dark-pool
   order matching under SPDZ-style MPC with continuous and periodic matching.
3. **Cartlidge–Smart–Talibi Alaoui, "Multi-party computation mechanism for anonymous equity block trading: a secure implementation of
   Turquoise Plato Uncross"**, ISAF 2021, DOI 10.1002/isaf.1502 (SCRY). A real venue's uncrossing mechanism implemented in MPC.
4. **Atallah–Elmongui–Deshpande–Schwarz, "Secure supply-chain protocols"**, IEEE CEC 2003, DOI 10.1109/coec.2003.1210264 (SCRY, 82 cites).
   INFERRED: secure capacity allocation / bidding between supply-chain partners without revealing private cost data.
5. **Pibernik–Zhang–Kerschbaum–Schröpfer, "Secure collaborative supply chain planning and inverse optimization: the JELS model"**, EJOR
   2011, DOI 10.1016/j.ejor.2010.08.018 (SCRY). INFERRED: shows that the *output* of a jointly computed plan can leak inputs by inverse
   optimization, so MPC alone does not give privacy. The cautionary paper for "dark coordination".
6. **Abidin–Aly–Cleemput–Mustafa / Mustafa–Cleemput–Abidin, "A local electricity trading market: security analysis"**, ISGT-Europe 2016,
   DOI 10.1109/isgteurope.2016.7856269 (SCRY). MPC-based peer-to-peer electricity market clearing.
7. **Wu–Zhao–Zhang, "Privacy-Preserving Distributed Optimal Power Flow With Partially Homomorphic Encryption"**, IEEE TSG 2021, DOI
   10.1109/tsg.2021.3084934 (SCRY, 70 cites). FHE/PHE for grid dispatch, one of the few HE-not-MPC coordination designs with uptake.
8. **Wang–Chau–Zhou, "Privacy-Preserving Energy Storage Sharing with Blockchain and Secure Multi-Party Computation"**, arXiv 2111.02005
   (SCRY). MPC + ledger for shared-storage allocation, the closest in shape to dregg (a chain as the commitment layer, MPC for the
   private clearing).
9. **Yokoo–Suzuki, "Secure multi-agent dynamic programming based on homomorphic encryption and its application to combinatorial auctions"**,
   AAMAS 2002, DOI 10.1145/544741.544770 (SCRY, 99 cites). HE winner determination for combinatorial auctions.
10. **Wang–Ren–Wang, "Secure and practical outsourcing of linear programming in cloud computing"**, INFOCOM 2011, DOI
    10.1109/infcom.2011.5935305 (SCRY, 317 cites). LP (the core of dispatch/planning) outsourced under disguise. The "planning as a hidden
    LP" baseline.

Pattern across the set (INFERRED): deployments (1, 3) use honest-majority MPC among a few institutional parties. The lasting caution is (5):
even a perfect secure computation reveals what its output implies. For a dregg "dark coordination" cell, the output's inverse-optimization
leakage belongs in the guard/boundary story (P2), not the crypto.

---------------------------------------------------------------------------------------------------------------------------------

## §6 Inventory

Fetched this session into `/Users/ember/paperbin/` (31, each with a `.txt`):
espiritosanto2016-coinductive-proof-search · fouquere2013-incarnation-ludics · eng2020-stellar-resolution · cai2013-theory-of-changes ·
stein2021-demanded-abstract-interpretation · angelo2026-contextual-metaprogramming-session-types · omar2018-hazelnut-live ·
ringer2020-pumpkin-pi-proof-repair-equivalences · nanevski2008-contextual-modal-type-theory · cave2013-first-class-substitutions ·
dekleer1986-assumption-based-tms · dealfaro2001-interface-automata · morgenstern2011-lpcfs · sewell2023-cakes-that-bake-cakes ·
hinrichsen2022-actris2 · hurd2011-opentheory-article · lifschitz2008-thirteen-definitions-stable-model ·
toninho2013-higher-order-processes-monadic · ringer2018-adapting-proof-automation-to-adapt-proofs · viola2023-proof-repair-quotient-equivalences ·
pientka2019-cocon · jang2021-moebius-contextual-metaprogramming · kohler2013-first-order-provenance-games ·
dannert2020-absorptive-provenance-fixed-point · porter2025-incremental-bidirectional-typing · kavvos2017-intensionality-godel-lob ·
murase2023-cmtt-polymorphic-contexts · davies2001-modal-analysis-staged-computation · demoura2021-lean4 ·
abrahamsson2025-candle-verified-hol-light · norell2007-towards-practical-dependently-typed-pl

Re-used (pre-existing): green-karvounarakis-tannen-provenance-semirings-pods2007 · gradel-tannen-provenance-analysis-semiring-semantics-fol-2412.07986 ·
qed-at-large-proof-engineering-survey-ringer-2019-2003.06458.

Read through Scry full text (not fetched): Mokhov et al. 2018 (10.1145/3236774) · Hammer et al. 2014 (10.1145/2594291.2594324) · AGM 1985
(10.2307/2274239) · Artemov 2008 (10.1017/s1755020308090060) · Doyle 1979 reprint (10.1016/b978-0-934613-03-3.50039-8) · Elkan 1990
(10.1016/0004-3702(90)90086-f) · Gupta–Mumick–Subrahmanian 1993 (10.1145/170035.170066).

Not obtained: Girard "Locus Solum" (claims checked through Fouqueré–Quatrini's restatement), the Bogetoft eprint (HTML challenge), Doyle
1992 foundations-vs-coherence. Anna's Archive did not resolve (`annas-archive.org`: DNS failure), so every fetch was direct
(arXiv/author/repository).
