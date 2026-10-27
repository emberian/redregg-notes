# THE CONTEXTUAL PROGRAM (real 2026-10-20) — building out what the three GPT-6 documents ask for, in nano

Ember: "we'll need to be much more ambitious to actually build all that out about nano; that's your actual assignment for the day."
Source: ACTIVITIES-GPT-RAW-20261020.md (the RAW documents; section numbers below are theirs). Landed base: LANG-66 (1e94183,
56c79a0, 6bf2585: CMTT core + the guarded contextual closure + the eight experiments), LANG-67 (8c31ace: open protocols),
LANG-68 (2b6e5e1: Lang's deployed terms as a lawful instance on the closed-hole fragment), LANG-69 (b5f880b: the closure proofs
split by responsibility). Each card is a Codex worker; each lands as its own `lang:` (or `lang!` where the Bell/wire re-ids);
every card's theorems get a second reader with the disjunct check; no landed theorem gains a premise unless the card says so.

CARD P1 · THE GUARD AS A SET OF INTERACTIONS (doc 1 §5; ludics orthogonality). Today a guard is a predicate on the hole. Build:
`Interaction`s a filling must survive (a finite list `T` per hole and world); admissible fillings `F_{h,w} = {d | admissible d ∧ d ⊥ t for
all t ∈ T}`; adding an obligation shrinks the set (`F' = F ∩ {t}^⊥`, a theorem); the TESTED/REQUIRED distinction as a theorem
(`tested ⊆ required → required^⊥ ⊆ tested^⊥`: a filling that passed every performed test may fail an untested required one, so a
`verified` status carries WHICH set it was verified against); the daimon distinction: a filling that "gives up" (the placeholder that
passes every interaction by never answering) is NOT a repair: `partial`/`gaveUp` is a distinct status, never `verified`. Connect to the
landed guard (`judge`): the predicate guard is the special case of a singleton interaction. Experiment: withdraw "the caller always
supplies a non-null value" → the filling must now survive a null interaction: tolerate, re-precondition, insert a check, or suspend.

CARD P2 · THE BOUNDARY DECLARATION (doc 1 §6). Every reusable boundary DECLARES which observations it preserves: `typingInterface`,
`logicalContract`, `observableBehavior`, `costGuarantee` (a lattice; a repair either re-establishes the declaration or propagates an
obligation beyond it). Today we have the two ends (value consumers unchanged / a syntax-reading consumer breaks) as theorems. Build:
`Boundary` as an object on the hole; `preserves : Boundary → Observation → Prop`; the theorem per level of what reuse it licenses
(client typing derivations / client proofs using the contract / cached downstream observations / bounds using the cost); the
dependent-types caveat as a theorem (replacing one inhabitant of A by another can change types mentioning it: locality needs the
abstraction/transport stated); the pruning-explanation corollary (a region discarded by a constraint reopens when the constraint is
withdrawn even if the selected answer's trace was tiny: the relevant boundary was the exclusion argument). Experiment: binary vs linear
search (doc 1 §1): membership survives the swap; the logarithmic bound gets its own status.

CARD P3 · ALTERNATIVE WORLDS AND GROUNDED CYCLES (doc 1 §7). Today the closure has one world and `lfpIter_sound`. Build: stable-model
style alternatives (`p :- not q. q :- not p.` has worlds {p} and {q}; their union is NOT a world: a theorem that the admissible-world
set is not closed under union); the four reports as distinct statuses (no applicable justification / different admissible worlds
support incompatible possibilities / one proposed world holds conflicting evidence / the analyzer has not finished); grounded cycles
already landed (`cycle_loses_grounding`, `counting_keeps_cycle`): restate over worlds. Immutable versioned premises (landed:
`reissue_never_reenables`) stay. Experiment: the two-rule program; withdraw and re-assert.

CARD P4 · FIRST-CLASS REPAIR OBJECTS AND TRANSPORT (doc 1 §8 + doc 2 §6 + doc 3 §4). Today repair is a function `repair w e cl`. Build:
`Repair` as a VALUE indexed by an edit (`e : w ⇝ w'`, `repair_e : State w → State w'`) that can be passed, abstracted over the edits it
handles, COMPOSED (`repair_{e₂} ∘ repair_{e₁} = repair_{e₂∘e₁}` on observables, or the obligation where it fails), and that exposes
intermediate obligations; a repair residual when no candidate succeeds (landed as `suspended`; make it a value with its obligations);
TRANSPORT when the proposition itself changes: a checked equivalence `A ≃ A'` carries a filling of a hole at A to A' (PUMPKIN-style),
stated as a sixth outcome `transported` with its evidence, distinct from `replacement`; the cost/intent policy as a parameter of
`select`, not of the judge. The three results stay named: conditional soundness, repair correctness (= from-scratch, landed), locality
(landed); add `compose_sound`.

CARD P5 · STATUSES AND POLARITY (doc 2 §5, §7). Build: the four logical statuses `witnessed | open (named obligations) | refuted
(a checked impossibility argument) | outsideThisProcedure (this analyzer cannot decide)` as a type the judge returns, with `refuted ≠
outside` enforced by construction (a refutation carries evidence; "no retained repair succeeded" is never `refuted`: a theorem); the
unresolved-hole-under-negation point: an open evaluator SUSPENDS a judgment whose atom is unfilled instead of reading it false (a
theorem that `not (unfilled atom)` is not `true`); alternating-simulation REFINEMENT for polarity (interface automata): a replacement
receiver may accept MORE inputs and emit FEWER outputs (`refines`), and the theorem that a replacement which narrows accepted inputs
breaks a peer that sends them (doc 2 §5's "accepts prices up to ten → up to five breaks seven"). Connect to LANG-67's polarity and
`no_foresight`.

CARD P6 · CERTIFICATES EXPLICIT ABOUT THE LOGIC (doc 3 §7, OpenTheory): a certificate = statement + theory context + definitions +
admitted assumptions + the checker it is accepted under; `accept` refuses a certificate whose context does not name every constant
the statement unfolds; a theorem that two certificates for the same statement under different contexts are DIFFERENT certificates.
This is the object the proof-engineering memo (HOLES-FOR-PROOF-ENGINEERING-20261020.md) will want for "a theorem as a hole": start
it after the memo's revision lands; the worker reads the memo first.

CARD P7 · (B) HOLES WITH A CONTEXT IN THE DEPLOYED LANGUAGE (DECISIONS CARD 9, Ember ruled (B)): `hole n σ` as an 18th Term
constructor; HasType checks σ against the hole's context; fillRefs substitutes σ; LangHasTy drops `d.ctx = []`; `langTemplate_no_hyps`
is DELETED as a boundary and replaced by the strengthening experiment on a deployed package. A `lang!` + CODEC review (every package
re-ids; not a cost). After CX-ACT's generators land (same files).

CARD P8 · THE FIRST INTEGRATION EXPERIMENT (doc 3 §8): two cells negotiate a one-use capability with alternative providers, a deadline
and a cancellation path; exercise the four changes (an unrelated state update; withdrawal of one provider's authority; a change of
representation with a checked correspondence; competing/replayed commitments) and prove the six objectives listed there, over the REAL
kernel (counted rights = the one-use capability; nd cancel = the cancellation path; stale pins = the withdrawal). After P4/P5 land.

WAVE 2 (launched real 10-20 ~20:30Z): P1+P5 (one worker: the judge's status type and the guard), P2 (boundary), P3 (worlds), P4
(repair objects + transport). P6 after the memo; P7 after the generators; P8 after P4/P5.

## WAVE 4 (real 10-20 ~22:40Z) — cards from the REAL literature (LITERATURE-CONTEXTUAL-20261020.md §4; Ember: "stop trusting GPT-6 to have digested it")

CARD P9 · PROVENANCE FOR EVERY ENV + ATMS LABEL DISCIPLINE (§4 items 1, 3; Grädel–Tannen §6 p19, Prop 15/16; de Kleer ~p145). Landed
`provenance I env cs` (Closure.lean:240) drops candidates failing the guard or the budget BEFORE forming monomials: the polynomial holds for
ONE env (the update pitfall Grädel–Tannen warn about). Build: (a) the tooth FIRST: `provenance_env_specialized` exhibits an env edit after
which a candidate becomes verified while the landed provenance has no monomial for it (the boundary becomes a tooth, not a silent limit);
(b) lift guard/budget verdicts into literals (env facts as tokens read through declared keys, or a third monomial component `envLits`);
prove `provenance_iff` for EVERY env and the update theorem (provenance after `Edit.apply` = provenance specialized, Prop 15 shape);
(c) reverse provenance = REPAIRS (Prop 16): `repairs_of_provenance : ∀ m ∈ provenance …, applyAll (edits m) w ⊨ verified` with the converse
for minimal repairs — P4's residual turned into a computed object: the minimal token edits that would verify a hole; (d) the ATMS label
discipline: `provenance_complementary_dead` (t ∈ supports ∧ t ∈ blockers → never verified; p·p̄ = 0), `provenance_minimal` (absorption,
proved to preserve provenance_iff; image PosBool[X,X̄]), NOGOODS: `nogoods : List (List Token)` on the closure + `judge_respects_nogoods`
(supports ⊇ a nogood → conflict, never suspended) = ATMS consistency, and what makes P5's `refuted` constructible from RECORDED evidence.
Docstrings: Candidate = Doyle 1979's justification (IN/OUT lists), NOT an ATMS label; AGM recovery deliberately rejected at
reissue_never_reenables.

CARD P10 · MINIMALITY + EARLY CUTOFF (§4 item 2; Mokhov–Mitchell–Peyton Jones Def 2.1, §4.2.2 — the exact analogue of our judge). Landed
`locality` is a sufficient no-op condition and its comment admits it is not minimal. Build: a per-candidate VERIFYING TRACE (the tokens
`deps I c` AND the env keys the guard read: the guard factors through a declared read-set, as `Frag.ReadsOnly` already does for protocols
at Protocol.lean:561); theorems `repair_minimal` (the re-judged log = exactly the candidates whose trace meets the edit) and `early_cutoff`
(a re-judged candidate whose status is unchanged does not dirty holes that read its selection). Rename in docstring:
repair_agrees_from_scratch = FROM-SCRATCH CONSISTENCY (Stein Thm 6.1; Adapton; Porter). Also item 12's docstrings (Davies–Pfenning at
box_ambient_free). NOTE for the bridge (CX-READER-ACT2's HIGH): the declared read-set is what lets a deployed package's observation be
complete by construction; coordinate by reading that reader's report.

CARD P11a · WORLDS AND STATUSES, NAMED BY THE FIELD (§4 items 6, 7). P3: restate cycle_loses_grounding as an UNFOUNDED-SET theorem and
counting_keeps_cycle as the GMS93 counting failure; state `admissibleWorlds = stable labellings of the candidates' IN/OUT justifications`
(Elkan 1990: JTMS computes stable models), so union-not-a-world is an instance of a known property and "analyzer not finished" is
justified by NP-completeness; choose and WRITE the cyclic-holes policy (absorptive semiring carrier per Dannert et al., or acyclic by
stratification per Stein's unrolling). P5: `refines` = de Alfaro–Henzinger Def 14 (inputs ⊇, outputs ⊆) + SUBSTITUTIVITY (Thm 4), not only
the narrowing counter-example; `outsideThisProcedure` modelled on a provenance-game DRAW (Köhler et al.), paired with P9's nogoods so
`refuted` = lost with a recorded nogood.

CARD P11b · GUARDS, REPAIRS, BOUNDARIES, NAMED BY THE FIELD (§4 items 4, 5, 8). P1: import INCARNATION (Fouqueré–Quatrini Def 5.1 p24,
5.5 p26): `material T c` = the sub-filling the interactions in T visit; `verified` carries (T, material T c); the give-up theorem = a
filling whose material part w.r.t. a required interaction ends in the daimon is `partial`, never `verified` — ludics' own distinction,
said so. P4: `Repair` obeys Cai et al.'s change-structure laws (nil = kept, ⊕, ⊖, a ⊕ (b ⊖ a) = b) so compose_sound is the standard
(f ⊕ df)(a ⊕ da) lemma; `transported` evidence in two forms distinct by construction: `rechecked` (PUMPKIN Pi's real guarantee is a
re-check; it does NOT prove the transformation) and `internal` (Lean Quot, Viola et al.); first-class substitutions (cv 01a1587d-9a98)
scoped to CONTEXT-MORPHISM edits only (strengthening/weakening/exchange: Cave–Pientka's class), never token withdrawal. P2: ValueGuard =
Kavvos's extensional region; locality for extensional consumers and breaking for intensional (syntax-reading) ones stated as the two sides
of one modal split; a syntax-reading guard TYPED by pattern matching on contextual code (Mœbius) instead of an untyped E → Tm → Bool.

AMENDMENTS to unstarted cards: P6 (landing): a certificate's logical context is emitted only by the kernel (Candle p5); unproved steps enter
as an explicit IMPORT LIST never an axiom (OpenTheory); each `verified` internalizes to a checkable term (Artemov). P7: context polymorphism
(Murase et al.) is the principled "typed under any ambient context"; Norell's guarded constants (`p : A = s when C`, thesis ch. 3) are the
precedent for a blocked hole's guard in the signature. P8: never fill-and-resume across a committed effect (Hazelnut Live Thm 4.2 needs
purity): RE-EXECUTE; cross-cell one-use consumption = LPCFS's single-transaction check; say which case nano is.

## PROOF-ENGINEERING PILOT (real 10-21 14:20Z) — Ember: "use these techniques for our verification / proof engineering; nano → minidregg → breadstuffs"

RULED (ROOT, on the memo's sequencing fork, HOLES-FOR-PROOF-ENGINEERING-20261020.md §"Price, design fork"): RECEIPT-FIRST. Build the graph adapter
with Lean as the proof checker and prove composition + revision correspondence first; the dependent-context bridge is the explicit follow-on. This is
an order of work, not a smaller destination (the memo's own words). PE1 starts now, beside P7's landing (different modules).

CARD PE1 · THE SHADOW OBLIGATION JOURNAL ON ONE KERNEL SLICE (memo §"What to build first in nano"). A journal + Lean environment exporter applied to
one real Kernel slice: chain_binds/chain_binds_sep (Kernel/Proofs/Fold.lean: the CollidesAmong escape over the explicit chainPres inputs),
inclusion_sound/exclusion_sound (Kernel/Proofs/Trie.lean: CollAmong S (readPres …)), receive_ok_with/receive_congr (Kernel/Proofs/Receive.lean),
submit_frame/call_frame (Kernel/Proofs/Logic/Triple.lean). The journal answers: what changed, which old evidence ceased to authorize which claims, what
alternatives survive, what proof work is owed. Current gates stay authoritative. Export the transitive slice (types, values, contract dependencies,
axiom sets, local premise applications); seed persistent obligations from the checked revision; evidence unavailable unless a receipt exists; landed
names/signatures UNCHANGED. The scratch-edit MATRIX (each with a real receipt, rule 16): unrelated proof edit; support proof replaced with the same
contract; definition body changed beneath an unchanged target; newly required hypothesis; unused hypothesis; GLOBAL-COLLISION ESCAPE (the
pigeonhole-vacuous shape: must be DETECTED); hidden projection/auxiliary dependency; changed instance/simp input; support withdrawal/reissue; exhausted
budget; plus withdrawal of a pruning reason, lost positive-cycle grounding, incompatible alternative worlds, lost cost evidence, partial audit coverage.
Three BASELINES per edit: A recompute closure statuses (the landed theorem's observation); B independently kernel-check retained proofs against the
new environment; C freshly elaborate the saved recipes with fixed dependencies/budgets; disagreements explained; candidate-set identity reported beside
every repair equality. The ADAPTER INVARIANT proved: a live receipt refers to the same obligation revision and inputs; every dependency outside the
changed set equal; the exported fragment reads only its declared supports; an admitted candidate has a matching successful check receipt — connected
to Protocol's fragment repair theorem and Closure's candidate model. NEVER instantiate CalculusData.check with "run Lean, false on timeout": the
adapter judges finite receipt data; Lean checks proofs. The inverted support index with the reference list as oracle; measure index maintenance, scans,
checker calls, peak memory, alternative counts separately (hash/count measures; never wall-clock as a verdict). Plants: a malformed/partial export and a
missing-import environment both report INCOMPLETE COVERAGE, never fewer obligations repaired. Owners: GATES (judge/Census integration: granted under
CROSS-LAYER), KERNEL (the sample is READ; scratch edits in a scratch copy, never the tree), LANG (the closure/journal modules: own). Then the
comparison report; mini's constructor redesign and bread's premise flow are the acceptance cases of the NEXT card.
