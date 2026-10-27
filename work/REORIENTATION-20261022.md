# REORIENTATION-20261022: the dream system in the literature's terms, and the path that promotes it into nano

Scholar (Claude, read-only on nano; wrote this file and fetched papers into `~/paperbin`). Ember, today: "the point
was to PROMOTE the toy instances into actually deployed aspects of the exact nanodregg system of our dreams …
reorient ourselves around the powerful ideas from the literature … a more powerful repair-capable, contextual,
open/still-analyzable system."

Trees read:
- nano `origin/main` = **f8d04ac** (S12 of the fold), extracted with `git archive` to my scratchpad `tip/`. Paths
  below without a prefix are nano paths at f8d04ac.
- the deleted toys at **3070fac** (`git archive 3070fac Lang` → scratchpad `old/`), cited `3070fac:<path>:<line>`.
- `redregg/work/LITERATURE-CONTEXTUAL-20261020.md` (cited LIT §n), `CONSOLIDATION-MAP-20261021.md` (MAP §n),
  `REVIEW-20261021.md` (REV), `fold/IMPACT-S2.md` (IMPACT-S2), `ACTIVITIES-DESIGN-20261022.md` (ACT-D),
  `RULINGS.tsv`, cv task `01a16171-d004` (P8 WITHDRAWAL GAP).

Tags: **READ (paper pN)** = I read the passage in the `.txt` extraction; N is the PDF page (form-feed count), not
the printed page. **READ (path:line)** = I opened the Lean at that line. **READ-LIT** = taken from LIT, whose
author read it at source and which I did not re-open. **INFERRED** = my reasoning; disagree with these first.
Nothing was built. No Lean was run.

The one-paragraph answer. Nano already deploys more of the literature than its theory modules know: the deployed
`hole n σ` IS CMTT's `clo(u, σ)` with Thm 4.2/4.3 proved over it; `instantiateHoles` IS PUMPKIN Pi's guarantee
(re-check the transported term with the kernel's checker); `receive_congr` IS a build system's verifying-trace
theorem; `audit`/`rederive` IS from-scratch consistency checked at run time; KERNEL-54's three pin domains plus
KERNEL-60's counted rights ARE LPCFS's revocable use-once certificates. What nano lacks is the **TMS link between
them**: the deployed hole's notion of "support is live" is read from a copy the caller posted under the hole's own
object, never from the kernel object that justifies it. The P8 withdrawal gap is that missing link, measured. The
literature names the fix exactly (de Kleer §4.9: retract a justification by contradicting the assumption it was
conjoined with; Doyle: a belief's support is a justification whose antecedents are other nodes, never a copy), and
it is shape **B**, not C. Every later card in Part C is the same move: state the surviving abstract theorem over
the deployed object whose World is read from the kernel, then delete the abstract duplicate.

---------------------------------------------------------------------------------------------------------------------

## PART A — THE DREAM SYSTEM IN THE LITERATURE'S TERMS

What "repair-capable, contextual, open, still-analyzable" means, idea by idea. For each: the definition and the
paper that gives it; where the theory ON MAIN embodies it (module + theorem); where the DEPLOYED system embodies it;
and what existed only in a deleted toy.

### A.0 The four words, made precise (INFERRED, assembled from A.1–A.11)

- **Contextual**: every unfinished piece of code is a metavariable `u :: A[Ψ]` that may depend exactly on the
  parameters in Ψ, and every use of it carries a mediating substitution σ from Ψ to the ambient context
  (Nanevski–Pfenning–Pientka). A filling is checked once, at Ψ, and is valid under every σ.
- **Open**: a program with unfilled holes is still a value of the system: it can be installed, typed, run around
  its holes, and composed with other open things, with compatibility decided optimistically (there is SOME
  environment that makes them work; de Alfaro–Henzinger) rather than demanding closure first (Hazelnut Live's
  progress with indeterminate forms).
- **Repair-capable**: when the world changes, every derived belief whose justification depended on the change is
  re-labelled, and only those (Doyle's well-founded support; de Kleer's sound/complete/minimal labels; Mokhov's
  minimality), with the result equal to re-deriving from scratch (Stein Thm 6.1, Cai's derivative law). A repair
  across a changed representation is re-checked, not trusted (PUMPKIN Pi).
- **Still-analyzable**: the reasons are first-class data with an algebra: a label is a polynomial whose monomials
  are alternative environments and whose products are joint requirements (Green–Karvounarakis–Tannen); its
  absorption-normal form gives minimal repairs (Grädel–Tannen Prop 16); a refusal names what is missing
  (why-not), not only that something failed.

### A.1 Contextual modal necessity; first-class substitutions

**Literature.**
- Contextual validity: "A valid[Ψ] if A is true in every …" ; "In order to prove A valid[Ψ] we have to prove A
  using only Ψ" — READ (nanevski2008 p5–6).
- The contextual hypothesis rule: to use `u::A valid[Ψ]` "we must show that our current hypotheses in Γ are strong
  enough to establish Ψ" — READ (nanevski2008 p6).
- Theorem 4.2 (simultaneous substitution) and Theorem 4.3 (contextual substitution: `∆;Ψ ⊢ M : A` and
  `(∆, u::A[Ψ], ∆′); Γ ⊢ N : C` give `(∆, ∆′); Γ ⊢ [[Ψ.M/u]]N : C`) — READ (nanevski2008 p17–19).
- §7: "A meta-variable u::A[Ψ] can depend exactly on the parameters in Ψ. All occurrences of u in a term have the
  form clo(u, σ) … σ is a mediating substitution" — READ (nanevski2008 p35).
- Instantiation is one-way; no withdrawal in CMTT — READ-LIT §1.1.
- Cave–Pientka: substitutions as first-class values, abstraction over them, canonical form — READ-LIT §1.2.
- Murase et al.: context variables `∀γ.[γ]T1 → [γ]T2`, "multiple parts of a single context"; subject reduction,
  SN, confluence (Thms 1–3) — READ (murase2023 p2, p5, p16, p19).

**On main (theory).** `Lang/Contextual/Core.lean` (384 lines) + `Lang/Proofs/Contextual/Core.lean` (1,194): the
simply-typed CMTT core with `box`/`letbox`, `subst_lemma`/`msubst_lemma`/`subject_reduction` (READ-LIT §1.1;
MAP §2.1 R3). `CalculusLaws` (READ `Lang/Proofs/Contextual/ClosureStatements.lean:14`) abstracts the laws;
`langLaws : CalculusLaws langData LangHasTy` (READ `Lang/Proofs/Contextual/LangInstance.lean:65`) instances it by
the deployed language.

**Deployed.** This is the most deployed idea in nano:
- `Term.hole (name : Nat) (subst : List Term)` — "A contextual hole, instantiated by its explicit ordinary
  substitution" (READ `Lang/Term.lean:69–70`). That is `clo(u, σ)`.
- Typing: `.hole n σ` looks `n` up in Ω and checks σ against the declared context `d.ctx` (`inferSubst Δ Γ σ
  d.ctx`), result `d.ty` (READ `Lang/Check.lean:177–183`). That is CMTT's `mvar` rule (nanevski2008 p35).
- `HoleDecl` = `u :: [Ψ ⊢ A]` (READ `Lang/HoleDecl.lean:5–9`); `HoleROM.check` types EVERY candidate at exactly its
  declared context, "including candidates not currently selected", and "A candidate cannot introduce another
  hole" (`inferE Δ h.ctx c.body (Ω := [])`) (READ `Lang/LiveHoles.lean:61–73`). That is `∆;Ψ ⊢ M : A` with ∆ empty
  (fillings are closed in the meta-context: depth one).
- `fillHoles_typed` (READ `Lang/Proofs/Fill.lean:123`) is Theorem 4.3; `substList_typed` (READ
  `Lang/Proofs/Subst.lean:531`) is Theorem 4.2.
- `factorHole` strengthens away unused positions "from right to left so every index still names its original
  assumption" (READ `Lang/LiveHoles.lean:137–144`): a context morphism (Cave–Pientka's strengthening, partial
  inverse of weakening).

**Deleted toy.** `3070fac:Lang/Contextual/ContextMorphisms.lean` (`Morphism`, `identity`, `compose`,
`weakening`, `exchange`, `strengthen`), theorems `apply_typed`, `compose_valid`, `strengthen_sound` (READ
`3070fac:Lang/Proofs/Contextual/ContextMorphisms.lean:12–75`), all over the CMTT core's `Tm`, not `Lang.Term`.

**Absent everywhere.** Context polymorphism (Murase). First-class contextual values as a `Term` former
(`box Ψ.M`). INFERRED: nano has `box` at the ROM granularity already: a `HoleCode.body` is a closed `Ψ.M` stored
as content-addressed package bytes (READ `Lang/HoleROM.lean:15–18`), shippable between cells as ROM. That is
Ângelo et al.'s "contextual values … boxed and transmitted in messages" (READ-LIT §1.22) at package grain.

### A.2 Typed holes that run (Hazelnut Live)

**Literature.**
- "evaluation proceeds around holes, tracking the closure around each hole instance" (READ-LIT §1.6); Theorem 3.11
  (Progress): a well-typed `d` steps, or is a boxed value, or "d indet"; "The key … is to explicitly account for
  indeterminate forms, i.e. those rooted at either a hole closure or a failed cast" — READ (omar2018 p20).
- Theorem 4.1 (Filling): `∆, u::τ′[Γ′]; Γ ⊢ d : τ` and `∆; Γ′ ⊢ d′ : τ′` give `∆; Γ ⊢ ⟦d′/u⟧d : τ` — READ
  (omar2018 p22). Fill-and-resume commutes with reduction only when evaluation order does not matter;
  "Languages with non-commutative effects do not enjoy this property" — READ-LIT §1.6 (p22).

**On main (theory).** None. The closure's `Outcome` (READ `Lang/Contextual/Closure.lean:179–187`) is about
judgments, not runs.

**Deployed.**
- A blocked hole becomes `.refuse T why` that "fires only when the machine demands that hole" (READ
  `Lang/LiveHoles.lean:161–173`); `blocked_step` proves the one-step fault (READ `Lang/Proofs/LiveHoles.lean:77`).
  So a run that never demands a blocked hole completes: "evaluation proceeds around holes", in the
  fault-on-demand form, not the indeterminate-value form.
- `invoke_live_never_stuck` (READ `Lang/Proofs/LiveInvoke.lean:38`) is the progress half.
- "Selection is fresh on each invocation" (READ `Lang/LiveHoles.lean:146`): nano re-executes; it never resumes a
  saved continuation across an effect. That obeys Hazelnut's own precondition (p22): a turn has effects.

**The deliberate difference** (INFERRED): Hazelnut returns an indeterminate RESULT containing hole closures; nano
refuses by name when a hole is demanded (law 7, named refusals). Nano has no "partial result" to show a user. That
is a product question, not a defect, and Part D.3 names the measurement.

### A.3 Truth maintenance: JTMS justifications with retraction; ATMS environments, labels, nogoods

**Literature.**
- Doyle 1979 (JTMS): "The TMS revises the current set of beliefs by using the recorded justifications to compute
  non-circular arguments for nodes from premises and other special nodes … These non-circular arguments distinguish
  one justification as the well-founded supporting justification of each node representing a current belief. The
  TMS locates the set of nodes to update by finding those nodes whose well-founded arguments depend on changed
  nodes" — READ (doyle1979 p6). SL-justifications: "two lists of nodes … a valid reason for belief if and only if
  each of the nodes in the first list is believed and each of the nodes in the second list is not believed"; "by an
  assumption we mean any node whose well-founded support is a non-monotonic justification"; dependency-directed
  backtracking "makes a record of the inconsistency of this set of assumptions" — READ (doyle1979 p7).
- de Kleer 1986 (ATMS): "While a justification describes how the datum is derived from immediately preceding
  antecedents, a label environment describes how the datum ultimately depends on assumptions … The task of the ATMS
  is to guarantee that each label of each node is consistent, sound, complete and minimal with respect to the
  justifications" — READ (dekleer1986 p18).
- Nogoods: "The inconsistent environments are called nogoods … If an environment is nogood, then all of its
  superset environments are nogood as well" — READ (dekleer1986 p21–22).
- Contexts: "An ATMS context is the set formed by the assumptions of a consistent environment combined with all
  nodes derivable from those assumptions" — READ (dekleer1986 p17). "context switching is free, and most
  backtracking (and all retraction) is avoided" — READ (dekleer1986 p1).
- **Retraction, §4.9**: "To make a justification retractable, it is conjoined with an extra assumption which
  represents its defeasability. To retract the justification, the problem solver contradicts the conjoined
  assumption. This is the only reasonable way to retract a justification. Although some TMSs permit direct
  retraction, few implement it correctly (correct means that all the labels of the datum will be as if the removed
  justification never existed)" — READ (dekleer1986 p27).
- The interface: "The difficulties arise when the problem solver is permitted to make a control decision based on
  the statuses, assumptions and justifications of nodes without informing the TMS … all control decisions must be
  communicated explicitly to the TMS" — READ (dekleer1986 p4).
- Elkan 1990: "a precise characterization of the inferences performed by nonmonotonic truth maintenance systems …
  using … logic programming with the stable set semantics … and a proof that implementing a nonmonotonic TMS is an
  NP-complete problem" — READ (elkan1990 p1–2).

**On main (theory).**
- `Candidate` (`supports`, `blockers`) is a Doyle SL-justification; `judge` is the IN/OUT labelling (READ
  `Lang/Contextual/Closure.lean:152–158`, `:226–232`; the docstring cites Doyle at `:237`, `:264`).
- ATMS label discipline: `label` = `minimal ((provenance I cs).filter Monomial.consistent)` (READ
  `Closure.lean:295–296`); `label_iff`, `provenance_minimal`, `provenance_complementary_dead` (READ
  `Lang/Proofs/Contextual/Provenance.lean:43, 143, 167`). That is de Kleer p18's sound + complete + consistent +
  minimal, proved.
- `withdraw_never_refutes`, `withdraw_never_prunes`, `token_edit_conflict_iff` (READ
  `Lang/Proofs/Contextual/Judge.lean:142–160`): losing a justification never establishes its negation.
- `reissue_never_reenables` (READ `Judge.lean:17`): tokens are immutable and versioned.
- **No nogood database on main.**

**Deployed.**
- The assumption token is `HolePin = (rel, key, ver)`; `holePinHolds` is "the token is live" (READ
  `Lang/HoleROM.lean:8–12`, `Lang/LiveHoles.lean:93–96`). The derivation supports of a candidate are
  `HoleCode.supports`; a moved one refuses `derivationMoved`; a moved context hypothesis that the candidate USES
  refuses `supportMoved`; one it does not use is strengthened away (READ `LiveHoles.lean:113–124`, `:154–155`).
  That is `effSupports` (READ `Closure.lean:219–220`) executed.
- **The gap**: `holeRow` reads `rv.points self rel`, rows under the hole's own object only (READ
  `LiveHoles.lean:85–91`). Std.hole's support is `{cell, pin}` (READ `Lang/StdHole.lean:11`), and its judgment
  compares the candidate's recorded pin with the FACT ROW under self keyed by `cell` — "Keys are rows under self,
  never cell pins" (READ `Lang/StdHole.lean:63–64`). In P8 the requester posts the provider's grant id and pin as
  that fact (READ `Lang/Journey.lean:2271–2280`: `supports := providers.map fun g => (g, pinOf …)`, then `invoke r
  "post" (hole_postArg g pin)` signed by `a`). Revoking the grant retires the grant cell (READ
  `Kernel/Receive/Derive.lean:325–329`: `(g, .retire)`), and the fact row is untouched. A pin of the tombstone is a
  valid pin by design (READ `Kernel/World.lean:313–316` `domTomb`; `:344–347` `pinOf`; `:993–1001`: "absent,
  tombstone and live are three pins"). So the commit that pins the tombstone is admitted (MEASURED by the fold:
  IMPACT-S2 §0.2).
- Worse than a stale copy: the deployed `posted` guard checks only that the fact's `by` is the signing agent, on
  insert, retract and upsert (READ `Lang/StdHole.lean:183–192`). Nothing at post time compares the fact's `cell` or
  `pin` with the kernel. The extra pin the P8 commit carries for `g` (READ `Lang/Journey.lean:2287–2289`,
  `[supports[i]?…]`) is checked by the kernel against the World, but the program never sees it (methods see no
  pins: ACT-D §9 correction 1), so it constrains nothing the hole judges. INFERRED: a requester could post a "support"
  naming any digest at any pin and the hole would treat it as live.
- In TMS terms (INFERRED, but tight): the fact row is a **premise** (a node with an empty justification) standing
  for a **derived** belief ("provider g is authorised now"). Its true antecedent, the grant cell, is not recorded
  as an antecedent. No dependency-directed process can retract it, because the dependency does not exist.

**Deleted toy.** `3070fac:Lang/Contextual/Nogoods.lean`: `RecordedClosure extends Closure` with `nogoods : List
(List Token)`, `judgeRecorded` (a nogood ⊆ effective supports → `conflict .guardFails`), `selectRecorded`; theorems
`judge_respects_nogoods`, `nogood_never_suspended`, `recorded_refuted` ("∀ v : World E, (judgeRecorded cl I v
c).status ≠ .verified"), `select_respects_nogoods` (READ `3070fac:Lang/Proofs/Contextual/Nogoods.lean:31–97`).
Plus `NogoodGames`/`Games` (provenance-game draws; READ `3070fac:Lang/Proofs/Contextual/{NogoodGames,Games}.lean`).
All were over the abstract closure, with the nogood DB supplied by hand: no deployed object ever wrote a nogood.

### A.4 Provenance semirings and minimal repairs

**Literature.**
- GKT 2007: union/projection add, join multiplies; Prop 4.2, "For any valuation v : X → K there exists a unique
  homomorphism of semirings Eval_v : N[X] → K" — READ (green2007 p4). Positive fragment only (RA+, positive
  Datalog) — READ-LIT §1.4.
- Grädel–Tannen 2024: dual indeterminates `N[X, X̄]` with `p·p̄ = 0` (Def 4, READ-LIT p9); keep the
  model-compatible polynomial and specialise late (§6, READ-LIT p19); **Proposition 16**: "For every monomial m of
  π⟦ψ⟧ the set R_m … is a repair … for every repair R … there is a monomial m … R_m ⊆ R. If R is a minimal repair,
  then R_m = R" — READ (gradel-tannen p23).

**On main.** `provenance` is the all-environment polynomial (one monomial per well-typed candidate, guard and
budget kept as literals) (READ `Closure.lean:269–273`); `provenance_iff` — a hole has a verified candidate at `w`
iff some monomial evaluates true at `w`, for EVERY world (READ `Lang/Proofs/Contextual/Provenance.lean:18`). S10
deleted the env-specialised twin (READ `git log` f8d04ac^^: 4f5f18b).

**Deployed.** No semiring provenance. `instantiateHoles_sources` is SOURCE provenance of syntax: the instantiated
body introduces no digest literal outside the template and the selected ROM candidates (READ
`Lang/LiveHoles.lean:215–216`; `Lang/Proofs/LiveHoles.lean:99`). Different notion (where code came from, not why a
fact holds). `HoleSelection` retains index, version, strengthened positions (READ `LiveHoles.lean:98–111`): the
selected monomial's identity, without its environment.

**Deleted toy.** `3070fac:Lang/Contextual/ProvenanceRepairs.lean`: `repairPlans` (minimal token edit sets);
theorems `repairs_of_provenance`, `changes_necessary`, `repairPlans_sound`, `repairPlans_cover`,
`repairPlans_antichain`, `repairPlans_minimal`, `repairPlans_complete` (READ
`3070fac:Lang/Proofs/Contextual/ProvenanceRepairs.lean:68–176`). That is Prop 16, proved — over the abstract world.
And `3070fac:Lang/Contextual/Acyclic.lean`: polynomials over a ranked hole graph, `adapt_correct`,
`adapt_acyclic`, `cycle_refused` (READ `3070fac:Lang/Proofs/Contextual/Acyclic.lean:134–163`).

### A.5 Proof repair across equivalences (PUMPKIN Pi; the quotient follow-up)

**Literature.**
- "The configuration is the key … Each configuration corresponds to an equivalence A ≃ B … a pair of pairs:
  ((DepConstr, DepElim), (Eta, Iota))" — READ (ringer2020 p5).
- "The implementation … produces a term that Coq type checks, and so does not add to the trusted computing base. As
  Pumpkin Pi is an engineering tool, there is no need to formally prove the transformation correct" — READ
  (ringer2020 p7). Decompile "deliberately forfeits soundness" — READ-LIT §1.7 (p11).
- Viola–Fan–Ringer: quotient equivalences, behaviour change, internal correctness in Cubical Agda — READ-LIT §1.8.

**On main.** Nothing (no transport outcome in `Closure.Outcome`).

**Deployed.** `instantiateHoles` ends: "The closed checker is the invocation boundary too; proof connects this
check to contextual substitution, rather than trusting a receipt" — `checkE Δ body p.iface (Ω := [])` on the
instantiated body (READ `Lang/LiveHoles.lean:217–221`). That is PUMPKIN Pi's guarantee exactly: whatever the
selection/strengthening/renaming did, the output is re-checked by the trusted checker. `instantiateHoles_typed`
(READ `Lang/Proofs/LiveHoles.lean:83`) then proves the re-check is redundant on success (the internal form).
Nano holds BOTH evidence forms the deleted `TransportKinds` distinguished, on its real objects.

**Deleted toy.** `3070fac:Lang/Contextual/{RepairObjects,TransportKinds}.lean`: `Correspondence`, `Registry`,
`TransportEvidence`, `Claim.rechecked | .internal`, `Observed` = `Quot`; theorems `transport_sound`,
`transport_typing`, `recheck_sound`, `internal_from_quotient`, `quotient_predicate_transport` (READ
`3070fac:Lang/Proofs/Contextual/{RepairObjects,TransportKinds}.lean`). The sixth `Outcome` (transport) was a
law-1 twin of the closure's five (MAP §1.5 F3).

### A.6 Incarnation: the part of a design interaction actually visits (ludics)

**Literature.** "Among the paths of a set of designs E, we characterize those that are really visited during the
interaction with E⊥ … designs in the incarnation of E⊥ are built from particular maximal cliques of visitable
paths" — READ (fouquere2013 p3). Def 5.1 (material, incarnation) p24; Def 5.5 (daimon closure) p26 — READ-LIT §1.10.

**On main.** Nothing.

**Deployed** (INFERRED analog, weak). A blocked hole that no run demands never faults (A.2): the verdict of a run
depends only on the holes it visits. And `Need.requiredOfLive` (READ `Lang/Sim/Need.lean:256–268`;
`requiredOfLive_spec`, READ `Lang/Proofs/LiveNeed.lean:37`) measures the steps the result needs. Neither is a
recorded "material part" of a filling.

**Deleted toy.** `3070fac:Lang/Contextual/{Material,P1}.lean`: `Filling = answer | gaveUp | fork`, `visit`,
`material`; `visited_gaveUp_never_verified`, `material_mono`, `eligible_antitone` (READ
`3070fac:Lang/Proofs/Contextual/{Material,P1}.lean`). Address trees of a private type.

### A.7 Interface automata: optimistic composition, alternating refinement

**Literature.**
- "two components are compatible if there is some environment that can make them work together … one interface
  refines another if it has weaker input assumptions, and stronger output guarantees" — READ (dealfaro2001 p1).
- "for interface automata, at every state some inputs may be illegal"; a product state where "one automaton
  generates an output that is an illegal input for the other" is an error state, and the optimistic view keeps the
  composition when a legal environment avoids it — READ (dealfaro2001 p2–3).
- Def 14 (alternating simulation), Thm 4 (substitutivity), the "cannot express which inputs must occur" limit —
  READ-LIT §1.12 (p8, p10).

**On main.** `Lang/Contextual/Protocol.lean` (757 lines): polarised holes `ours/theirs`, `fill_skips_theirs`,
`theirs_hole_untypable` (READ `Lang/Proofs/Contextual/Protocol.lean:115, 123`); `no_foresight` (READ the module
docstring `Protocol.lean:9–15`). R1 (keep or delete) is still open (MAP §7; RULINGS R-0020 stops at S12).

**Deployed** (INFERRED reading). A package's `iface` (its method types) + its laws + its row guards are an interface
automaton whose inputs are calls: a refusal (`Refusal.program …`, a law refusal, `rowUnpinned`) is an input illegal
in the current state. The kernel never "input-enables": it refuses by name. A nested `invoke` from one object to
another is the product; a nested call refused is the error state. What is not deployed: any statement comparing
two packages (refinement), or saying a caller never reaches a callee's illegal input.

**Deleted toy.** `3070fac:Lang/Contextual/{P5,Interfaces}.lean`: `Machine`, `Refines`, `AlternatingSimulation`;
`refines_iff_definition14`, `substitutivity`, `simulation_preserves_safety`, `narrowing_breaks_peer`, plus the
`priceReceiver` example (READ `3070fac:Lang/Proofs/Contextual/{P5,Interfaces}.lean`). Over a private `Machine`.

### A.8 Change structures and incremental maintenance; demanded analysis

**Literature.**
- Cai et al. Def 2.1: a change structure `(V, Δ, ⊕, ⊖)` with "(e) Given u, v ∈ V, v ⊕ (u ⊖ v) equals u"; nil change
  Def 2.2; derivative `f (a ⊕ da) = f a ⊕ f′ a da`; Theorem 2.9 "Nil changes are derivatives" — READ (cai2013 p2–3).
- Mokhov–Mitchell–Peyton Jones: "Definition 2.1 (Minimality). A build system is minimal if it executes tasks at most
  once per build and only if they transitively depend on inputs that changed since the previous build" — READ
  (mokhov2018 p3). §4.2.2 Verifying Traces: "record the values/hashes of dependencies used last time, and if
  something has changed, the key is dirty and must be rebuilt" — READ (mokhov2018 p14). Def 3.1 correctness and
  early cutoff — READ (mokhov2018 p1, p5; Def 3.1 via READ-LIT §2.11).
- Stein et al. Thm 6.1 "(DAIG From-Scratch Consistency)"; the DAIG "remains acyclic" by unrolling — READ-LIT §1.14.
- Hammer et al. (Adapton): demanded computation graph; "We prove that the patching process is sound in that
  patched results will match what (re)computation from scratch would have produced" — READ (hammer2014 p2).

**On main.** `repair_agrees_from_scratch` (READ `Lang/Proofs/Contextual/Repair.lean:112`): after `repair e`, the
observable equals `fromScratch (e.apply w)` — Stein's from-scratch consistency. `repair_carries_untouched`,
`locality`, `repair_rejudged_eq_touched` (READ `Repair.lean:141, 150, 221`): a sufficient (not minimal) dirtiness
criterion, admitted in the code ("Sufficient, not minimal: an environment change touches every candidate", READ
`Closure.lean:298–299`).

**Deployed** — and here nano is AHEAD of its theory:
- `receive_congr`: "two Worlds that agree [on the pinned cells and the rows observed] derive the same Turn (or the
  same refusal) from the same call" (READ `Kernel/Proofs/Receive.lean:36–41`). That is Mokhov's verifying-trace
  soundness: a result depends only on its recorded dependencies (the pins are the trace). Every Lang read goes
  through `Pinned`/`RowView` ("A receiver's only access to state", READ `Kernel/Receive/Call.lean:275–287`), so
  the theorem covers Lang.
- `audit`/`rederive`: the follower re-runs `receive` on its own World and requires the very same Turn (READ
  `Kernel/Receive/Audit.lean:19–26`). That is from-scratch consistency checked at run time, per step.
- `Host.openWith` replays the tail from a checkpointed base (READ `Host/Open.lean:170–200`): `base ⊕ tail`.
- Hole selection keeps no cache ("fresh on each invocation", READ `LiveHoles.lean:146`), so there is nothing for a
  cache-validity theorem to be about; S11 deleted the trace cache half for that reason (MAP §2.2 D-TRACE).

**Deleted toy.** `3070fac:Lang/Contextual/RepairChanges.lean`: `ChangeData`, `replacement`, `derivative`;
`replacement_laws`, `repair_derivative`, `composed_derivative`, `repair_compose_assoc` (READ
`3070fac:Lang/Proofs/Contextual/RepairChanges.lean:12–77`). The Trace cache half (`Cached`, `refresh`,
`early_cutoff`, `refresh_consistent`; MAP §2.2 D-TRACE).

### A.9 Use-once, revocable certificates (LPCFS)

**Literature.** "the reference monitor checks that each certificate in a submitted request is absent from this
[revocation] table … the check for certificate revocation must be made atomically with the check for use-once
certificates" — READ (morgenstern2011 p2). "all certificates present in the justification of an access must be
checked and marked consumed in a single atomic step" — READ-LIT §1.18 (p2).

**On main (theory).** None (the P8 `Integration` module was deleted in S1c; its `one_use_consumption` was
`grant_moves_le_cap` at cap 1, MAP §2.2 D-WRAP).

**Deployed.** KERNEL-60 counted rights (a grant's ledger "only grows and what is left only falls", READ
`Kernel/Receive/Call.lean:379–404`, the grant layout comment through `ledgerSpendsMax`); `grant_moves_le_cap`
(READ `Ledger/Proofs/GrantCap.lean:12`); revocation = retire = tombstone (READ `Derive.lean:325–329`); every check
of one call happens in one Turn (`touchCheck` per touch, READ `Kernel/World.lean:999–1001`). The P8 composition
spends the counted unit and selects the provider in one atomic `commit` (READ `Lang/Journey.lean:2156–2190`).
**The missing LPCFS clause**: "each certificate in the justification" — the provider grant IS in the commit's
justification (the hole's support) but the monitor does not know it, because the justification is a self-row copy
(A.3). The atomicity is there; the binding of justification to monitor is not.

### A.10 Monadic sessions; contextual values sent between parties

**Literature.** "a linear contextual monad … Monadic values are open process expressions and are first class
objects" — READ (toninho2013 p1); "each process is bundled with all channels … it uses and the one that it offers.
This is a linear counterpart to the contextual comonad" of CMTT — READ (toninho2013 p3). Ângelo et al. 2026:
boxed contextual values transmitted in messages; no deadlock freedom — READ-LIT §1.22.

**On main.** `Protocol.lean` (`Prot` with `call op k`, holes, affine tokens), `NanoBridge.lean` (embeds
`Hosting.Resident.Prog`, "trivial index … no holes (`Empty`)", READ `Lang/Contextual/NanoBridge.lean:1–9`),
`Negotiation.lean` (474 lines of example theorems). R1 open.

**Deployed.** `Hosting.Resident.Prog` (`cmd | keep | forget | ask | say`, a continuation per result; READ the
NanoBridge docstring) and `interp_runs` (READ-MAP R1: `Hosting/Proofs/ResidentRun.lean:700`); the Bell activity
(ACT-D §0 item 3). Affine, not linear (READ-LIT §1.16).

### A.11 Alternative worlds = stable labellings; acyclicity

**Literature.** Stable model: the minimal model of the reduct equals M; Def D: no non-empty subset unfounded —
READ-LIT §1.15. Elkan: JTMS with OUT-lists = stable models, NP-complete — READ (elkan1990 p1–2). GMS93 counting fails on
recursion — READ-LIT §2.3. Dannert et al.: cyclic provenance needs absorptive, fully continuous semirings —
READ-LIT §2.15. ATMS context = consistent environment + its consequences (dekleer1986 p17).

**On main.** Nothing (the Closure docstring: "supports are one level … a support cycle is not expressible here",
READ `Closure.lean:10–13`).

**Deployed.** The alternatives are `HoleROM.code : List HoleCode` (READ `HoleROM.lean:28`); the chosen world is the
selection row's index (READ `LiveHoles.lean:150–153`); the unchosen candidates are retained in ROM. No liveness in
nano is DERIVED: every support is a pin of kernel state, so every justification chain bottoms out in the World in
one step. Hence no unfounded set can exist on the live path (INFERRED; Part B row 7 makes it a theorem).

**Deleted toy.** `3070fac:Lang/Contextual/Worlds.lean` (`NormalRule`, `reduct`, `analyze`, `Report`), theorems
`check_iff_stable`, `analyze_exact`, `alternatives_sound`, `admissible_not_union_closed`, and in WorldsField
`admissibleWorlds_eq_stableLabellings`, `cycle_unfounded` (READ
`3070fac:Lang/Proofs/Contextual/{Worlds,WorldsField}.lean`). A private rule language beside nano (MAP D-RULES).

### A.12 Boundaries: what a consumer may rely on

**Literature.** The contextual hypothesis rule fixes the boundary: a consumer of `u` sees exactly `A[Ψ]` (nanevski2008
p6, p35). Kavvos: extensional (value) vs intensional (code) regions — READ-LIT §2.7.

**On main.** `Consumer`/`consumer_boundary` (READ `Lang/Contextual/Closure.lean:592–600`;
`Lang/Proofs/Contextual/History.lean:85`).

**Deployed.** Ω = `holeSignature p.holes` (READ `HoleROM.lean:39`); `Package.checkContextual` checks the body
against `p.iface` under Ω (READ `LiveHoles.lean:75–83`); the cost boundary is `Package.holeCharge` (READ
`LiveHoles.lean:195–197`) with `instantiateHoles_cost` (READ `Lang/Proofs/LiveHoles.lean:362`). So the deployed
boundary is (typing via Ω, cost via holeCharge). Behaviour is NOT a boundary: any candidate typed at the
declaration may be selected.

**Deleted toy.** `3070fac:Lang/Contextual/{Boundary,ModalBoundary}.lean`: four observations, `reuse_client_typing`,
`reuse_client_contract`, `typed_guard_judge`, `intensional_judge_breaks`; and the trivia the review named
(`dependent_inhabitants_change_types`, REV H2).

### A.13 Summary of A: what is where

| idea | literature anchor | on main (theory) | DEPLOYED | toy only (3070fac) |
|---|---|---|---|---|
| contextual holes, σ | CMTT p6, p17–19, p35 | CMTT core; `CalculusLaws`, `langLaws` | `Term.hole n σ`; `fillHoles_typed`; `substList_typed`; `factorHole` | ContextMorphisms |
| holes that run | Hazelnut p20, p22 | — | blocked → refuse on demand; `invoke_live_never_stuck`; fresh selection | — |
| JTMS/ATMS | Doyle; de Kleer p4, p17–22, p27 | `judge`, `label_iff`, `provenance_minimal`, `withdraw_never_refutes` | `HolePin`, `holePinHolds`, `derivationMoved`; **liveness from self rows only** | Nogoods, NogoodGames, Games |
| provenance, repairs | GKT p4; GT Prop 16 p23 | `provenance_iff` (all-env) | source provenance only | ProvenanceRepairs, Acyclic |
| repair across equivalences | PUMPKIN Pi p5, p7 | — | `instantiateHoles` re-check + `instantiateHoles_typed` | RepairObjects, TransportKinds |
| incarnation | Fouqueré p3, p24, p26 | — | (weak) demand-driven faults | Material, P1 |
| interface automata | de Alfaro p1–3, p10 | Protocol polarity | refusals as illegal inputs (unstated) | P5, Interfaces |
| change structures / incremental | Cai p2–3; Mokhov; Stein | `repair_agrees_from_scratch`, `locality` | `receive_congr`; `audit`; `openWith` | RepairChanges; Trace cache |
| use-once revocable certs | LPCFS p2 | — | counted rights; tombstone; one Turn | Integration (deleted S1c) |
| monadic sessions | Toninho p1, p3 | Protocol, NanoBridge (R1 open) | Resident `Prog`; Bell | — |
| worlds, acyclicity | Elkan; Lifschitz; de Kleer p17 | — | ROM `code` + selection row | Worlds, WorldsField |
| boundary | CMTT p6; Kavvos | `consumer_boundary` | Ω + `holeCharge` | Boundary, ModalBoundary |

---------------------------------------------------------------------------------------------------------------------

## PART B — THE PROMOTION TABLE

Rule for every row (from the substrate law and the fold, INFERRED): a promoted theorem is stated over a DEPLOYED
object; its World is read from the kernel (`Pinned` + `RowView`), never constructed by hand; a consumer in the Host
closure, the journey, or a kernel/ledger proof CALLS it; and it has a tooth (a plant or a decided refutation over
the real object) that turns it red when the mechanism it names is removed. "Premise price" = hypotheses the change
adds to theorems already landed (the fold's measure, `minted-price-premises-not-only-cost`).

Shared definition every row uses (sketch, INFERRED):
```
-- the closure's World, read from the kernel at one call
def kernelWorld (look : Pinned D) (rv : RowView D) (self : D) : Contextual.World Env :=
  { live := fun t => tokenHolds look rv self t, env := … the guard pin's state … }
-- a token is EITHER a row under self at a version, OR a kernel cell that must be live
inductive SupportPin | row (rel : Nat) (key : ByteArray) (ver : Nat) | cell (id : D)
```
`.cell id` holds iff `look id = .ok (some c)` (live; a tombstone or absence reads `.ok none`; an unpinned id is
`.error unpinned` — READ `Kernel/Receive/Call.lean:275–276`, `:422–423` `pinned` = `.ok (w.live E c)`, and
`Kernel/World.lean:775–778` `live` = `some cell` only for a live entry). This is the one new object; rows 1–3 and 9 need it.

### B.1 ATMS retraction (the P8 gap) — FIRST

- **Deployed object.** `HoleCode.supports : List HolePin` (READ `HoleROM.lean:15–18`) and Std.hole's `holeSupport
  = {cell, pin}` with its generated judgment (READ `StdHole.lean:11`, `:52–80`); `selectHole`, `instantiateHoles`,
  `loadLive` (which already holds `look`: READ `Lang/Program.lean:207–210`); the revoke receiver (READ
  `Derive.lean:325–329`); KERNEL-54's pin domains.
- **Theorem (sketch).**
  - `selectHole_cell_support`: `selectHole look rv self h = .ok s → ∀ p ∈ (h.code[s.index]).supports, p = .cell g →
    ∃ c, look g = .ok (some c)`.
  - `revoked_support_refused`: if a call pins `g` at its tombstone (`look g = .ok none`) then every candidate
    citing `.cell g` is `.error (.derivationMoved …)`, hence (with `resolveHole`) the hole is blocked, hence the
    commit that demands it is refused by name.
  - the journey row: "P8.2 re-pinned tombstone: refused derivationMoved" through the REAL `submit` (the probe
    `fold/S2-tombstone-probe.txt` becomes the row, as cv 01a16171 asks).
- **Premise price.** Kernel: **zero** — `receive_congr` already quantifies over `c.unsigned.pins` and every Lang read
  goes through `Pinned` (READ `Kernel/Proofs/Receive.lean:38–41`). Lang: `selectHole`, `changedHypotheses`,
  `runHoleGuard`, `resolveHole`, `instantiateHoles` gain an argument `look`; the eight `Lang/Proofs/LiveHoles.lean`
  statements (`selectHole_origin` :49, `resolveHole_refusal` :70, `instantiateHoles_typed` :83, `_sources` :99,
  `_cost` :362, …) gain a binder, no hypothesis. `selectHole_origin`'s conclusion `c.supports.all (holePinHolds rv
  self)` changes meaning (it now covers cells). Re-emit: the Std.hole bundle, the P8 package bytes, the journey
  rows (a `lang!`). Re-genesis: whatever holds package ids.
- **What the toy stated.** `judge_respects_nogoods`, `recorded_refuted`, `select_respects_nogoods`
  (`3070fac:Lang/Proofs/Contextual/Nogoods.lean:31, 79, 97`). The promotion does NOT revive a nogood database:
  KERNEL-54 makes `{g live at v, g tomb}` an inconsistent environment structurally (a pin is exactly one of three
  digests, READ `World.lean:344–347`), so the "nogood" is the pin domain itself, and the only missing thing is that
  the candidate's environment contains `g`. INFERRED: this is de Kleer §4.9 literally — the justification "provider
  authorised" is conjoined with the assumption "g live"; revocation contradicts it.
- **Consumer.** `Lang/Journey.lean` P8 rows (`p8Rows`, :2217); `Std.hole`'s generated `select`/`commit`; the live
  bridge (B.2), whose World this IS.
- **Tooth.** Plant: map `.cell g` to `true` in `tokenHolds` → the tombstone row turns admitted → journey RED. And a
  decided refutation: the same call with `look g = .ok none` must be `.error`.

### B.2 The live bridge (map §7 R2): runtime selection IS the closure's judge

- **Deployed object.** `selectHole`/`resolveHole` (READ `LiveHoles.lean:149–182`); `HoleRefusal` (one constructor
  per refusal since S9, READ `LiveHoles.lean:13–35`).
- **Theorem (sketch).** `selectHole_judge`: for `romIface h : Iface langData Env` and `romCandidate h i`,
  `(selectHole look rv self h).map (·.index) = .ok i ↔ selectionIndexRow rv self h = some i ∧ judge (romIface h)
  (kernelWorld look rv self) (romCandidate h i) = .verified`, and per refusal: `derivationMoved`/`supportMoved` ↦
  `.suspended missing` with `missing` = the moved pins; `guardBlocked` ↦ `.conflict .guardFails`. Then
  `strengthening_sound` (READ `Lang/Proofs/Contextual/Outcomes.lean:172`) applied at `langLaws` yields that
  `s.strengthened` is the strengthening outcome.
- **Premise price.** None on landed theorems (a new theorem). The STATEMENT has a cost the map did not see
  (INFERRED, Part D.2): `Closure.judge` has `pruned` (blockers) and `uncovered` (per-candidate cost vs budget);
  `HoleROM` has neither blockers nor per-candidate budget, and `HoleRefusal` has `selectionAbsent`,
  `selectionType`, `selectionIndex`, `unpinned`, `guardFault` with no `Status`. The bridge holds on the fragment
  `romCandidate h i` with `blockers = []`, `cost ≤ budget`; the remaining refusals are pre-judgment (the World could
  not be read) and map to "no judgment", not to a Status.
- **What the toy stated.** At 3070fac nothing toy; the closed-fragment bridge `hole_judgment_admission_bridge`
  with `hctx : I.ctx = []`, `hhyps : I.hyps = []` survives on main (READ
  `Lang/Proofs/Contextual/HoleBridge.lean:113–123`) and the five decide-instances `kept_context`,
  `strengthening_factor`, `alternative_same_filling`, `replacement_filling`, `used_hypothesis_suspends` (READ
  `Lang/Proofs/LiveJourney.lean:45–93`) are its pointwise shadows.
- **Consumer.** `Lang/Proofs/LiveJourney.lean` (its five instances become corollaries, kept as teeth); the journey
  rows; B.3–B.5 (each quantifies over `kernelWorld`).
- **Tooth.** If `changedHypotheses` stops checking `usesVar` (plant), `used_hypothesis_suspends` and the bridge's
  `supportMoved ↦ suspended` direction both go red.
- **Deletes.** If it lands: the CMTT core's reason to stay disappears (MAP R3); `HoleBridge`'s closed fragment
  becomes a corollary. If it cannot be stated without premises: MAP R2's other branch (take `judge`/`Status` out
  of Lang).

### B.3 Worlds as candidates; the label of a live hole

- **Deployed object.** `HoleROM.code` (the alternatives) and the selection row (the chosen context).
- **Theorem (sketch).** `live_label_iff`: `(∃ i, selectHole_at i … = .ok _) ↔ ∃ m ∈ label (romIface h) (romCands h),
  m.eval (romIface h) (kernelWorld look rv self) = true` — `label_iff` (READ `Provenance.lean:167`) at the deployed
  instance; the ATMS reading: the hole has a selectable candidate in the current context iff some minimal label
  environment is a subset of the kernel's live pins (de Kleer p19: "membership within a context can be checked by a
  direct subset test").
- **Premise price.** Zero (new statements, after B.2).
- **What the toy stated.** `alternatives_sound`, `admissible_not_union_closed`, `admissibleWorlds_eq_stableLabellings`
  (`3070fac:Lang/Proofs/Contextual/Worlds.lean:175, 241`; `WorldsField.lean:83`). The promotion drops the stable-model
  machinery on purpose: nano's supports have no OUT-lists over derived nodes, so the labelling is unique and
  polynomial (INFERRED from A.11; Elkan's NP-completeness needs OUT-lists over derived nodes).
- **Consumer.** A read-only query method on the Std.hole package (`label`) used by the resident's tick (the
  pull-driven `rejudge` ACT-D §3 names) and one journey row ("after revoke, the label of hole 0 is {provider 1}").
- **Tooth.** A label that omits a candidate whose supports are live → the row's chosen world differs from the
  label's → red.

### B.4 Provenance over live selections; reverse provenance as a planner

- **Deployed object.** `HoleSelection` (READ `LiveHoles.lean:98–111`), `HoleInstance.selections` (`:201–205`).
- **Theorem (sketch).** (a) `selection_monomial_sound`: the receipt's recorded supports are exactly
  `(monomial (romIface h) (romCandidate h s.index)).supports` and every one held in the World the Turn read — a
  receipt is a label environment, checked. (b) `repairPlans_live` = Prop 16 at the deployed instance: every
  minimal set of pins whose change would make some candidate selectable is listed.
- **Premise price.** Adding the environment to `HoleSelection` changes the receipt type: every theorem
  destructuring it gains fields (statement edits, no hypotheses).
- **What the toy stated.** `repairPlans_sound`, `repairPlans_minimal`, `repairPlans_complete`
  (`3070fac:Lang/Proofs/Contextual/ProvenanceRepairs.lean:122–167`).
- **Consumer.** (a) the audit: `rederive` already re-runs the selection; (a) is what makes the receipt worth
  logging. (b) a client/resident planner ("re-pin these to make the plan admissible") — and only if one exists.
  If none exists, (b) does not land (Part D.3).
- **Tooth.** (a): a receipt that drops a support (plant) fails `selection_monomial_sound`'s equality.

### B.5 Repair with transport over `resolveHole`

- **Deployed object.** `resolveHole`, `factorHole`, the closing `checkE` of `instantiateHoles`.
- **Theorem (sketch).** `live_repair_outcome`: given two kernel views `v, v′` that differ by an edit `e` (one pin
  moves), the pair `(resolveHole v h, resolveHole v′ h)` is exactly one of the five outcomes of
  `repairSelected` (READ `Closure.lean:505–512`) at `langData`, with `alternative_sound`, `replacement_sound`,
  `strengthening_sound`, `suspended_sound` (READ `Outcomes.lean:96–225`) instanced. "Transport" is the closing
  re-check, already deployed (A.5): `instantiateHoles_typed` is the internal form, `checkE` the rechecked form.
- **Premise price.** Zero (new; after B.2).
- **What the toy stated.** `transport_sound`, `recheck_sound`, `internal_from_quotient`, `repair_derivative`
  (3070fac, A.5, A.8). The quotient transport has **no deployed observable** to quotient by: do not build it until a
  consumer pins a value row (ACT-D card B's exported `value` row is the first candidate).
- **Consumer.** The journey's P8.3 row ("second provider selects contextual ROM candidate") becomes an instance;
  `LiveJourney`'s five decide-instances become corollaries.
- **Tooth.** A plant in `reselect` order (prefer replacement over alternative) flips `alternative_same_filling`.

### B.6 Boundary = Ω

- **Deployed object.** `holeSignature`, `Package.checkContextual`, `Package.holeCharge`.
- **Theorem (sketch).** `boundary_any_selection`: for every selection receipt `s` of every hole, the instantiated
  body has the package's interface type and cost ≤ `p.preparationCost` — which is `instantiateHoles_typed` +
  `instantiateHoles_cost` + `resolutionMax_committed` (READ `Lang/Proofs/LiveHoles.lean:83, 340, 362`). This row
  is ALREADY LANDED in substance.
- **Premise price.** Zero.
- **What the toy stated.** `reuse_client_typing`, `reuse_cost_bound` (3070fac `Boundary.lean:115, 158`; the
  latter a trivia per REV H2).
- **Action.** Name it (a docstring that says the deployed boundary is typing + cost, never behaviour) and delete the
  abstract `Consumer`/`consumer_boundary` if B.2 gives it no consumer. No new card.

### B.7 Acyclicity over the pin graph

- **Deployed object.** Support pins of candidates (rows under self, cells after B.1); the chain order of Turns.
- **Theorem (sketch).** `support_precedes`: every support pin that a Turn at height `h` checks names a row/cell
  version written by a Turn at height `< h` (a call pins the World BEFORE its own Turn applies: `touchCheck`
  compares `pinOf E cur = x.seen` against the current entry, READ `Kernel/World.lean:999–1001`). Therefore the
  "depends on" relation among selections is well-founded by height: Stein's unrolling with rank = height
  (READ-LIT §1.14), and no unfounded set can form (A.11).
- **Premise price.** Zero. It is a kernel fact about pins.
- **What the toy stated.** `adapt_acyclic`, `cycle_refused`, `unroll_equation` (`3070fac:Lang/Proofs/Contextual/
  Acyclic.lean:145–212`), `cycle_unfounded` (WorldsField:93).
- **Consumer.** B.3 (the label is computed at one World, not as a fixed point) and the decision text of any future
  card that lets a hole's support be another hole's selection row.
- **Tooth / honesty.** INFERRED risk that this is definitional (Part D.3). It earns a place only if stated as a
  property of `touchCheck` that a plant (allow pinning the post-state) breaks.

### B.8 Interface automata over the receiver

- **Deployed object.** A package's `iface` + laws + row guards; the `Std.machine` typestate the activities design
  maps activities onto (ACT-D §0 item 6: `machine_reached`, `object_history_chain`).
- **Theorem (sketch).** `refines_substitutive`: if package `p′` refines `p` in Def 14's sense over their declared
  machines (accepts at least the method calls `p` accepts in each typestate, emits at most the nested calls `p`
  emits), then every caller object compatible with an object running `p` (never reaches a refusal of the callee's
  methods along its declared machine) is compatible with `p′`. The consumer is package REPLACEMENT.
- **Premise price.** Real: a statement over `Std.machine` packages needs the machine to be the package's actual
  input language, i.e. a theorem that every non-machine call is refused by name. INFERRED: that is `machine_reached`
  read the other way; measure before pricing.
- **What the toy stated.** `refines_iff_definition14`, `substitutivity`, `simulation_preserves_safety`
  (`3070fac:Lang/Proofs/Contextual/{Interfaces,P5}.lean:66, 126; 172`).
- **Consumer.** Package replacement (an activity upgraded in place). If nano has no replacement path for programmed
  objects (`relaw` on a programmed object is refused `hasMethods`, ACT-D §9 correction 2), there is no consumer and
  the row waits.
- **Tooth.** A refining package that drops one accepted input → a caller's journey row refused.

### B.9 Use-once grants as revocable certificates

- **Deployed object.** KERNEL-60 counted rights, `spendVia`/`spendAt`, retire/tombstone, the P8 `commit`.
- **Theorem (sketch).** `commit_checks_justification_atomically`: an admitted Turn whose program selected candidate
  `i` and spent one unit via `cap` had, in the SAME World the Turn read, every `.cell g` support of candidate `i`
  live and `cap`'s ledger left ≥ 1 — LPCFS's single atomic step, stated over `receive`. After B.1 this is the
  conjunction of B.1's `selectHole_cell_support` with the landed `spendVia_ok` (READ
  `Kernel/Proofs/Ledger.lean:331`) under one `receive`.
- **Premise price.** Zero beyond B.1.
- **What the toy stated.** `one_use_consumption`, `recovery_preserves_consumption` (deleted with Integration in
  S1c; they restated landed facts, MAP D-WRAP).
- **Consumer.** P8.4 rows ("RE-EXECUTE atomic checked commitment", "competing use"), READ `Lang/Journey.lean:2346–2358`.
- **Tooth.** Split the commit into two Turns (plant) → the revoke can land between them → a row that admits.

### B.10 Monadic sessions (Protocol, R1)

- **Deployed object.** `Hosting.Resident.Prog`, `Std.activity` (READ `Lang/StdActivity.lean` exists).
- **Theorem (sketch).** If R1 = (A): `Prog` gains holes and `fill_preserves_hasProt` / `no_foresight` are stated
  over `Prog`; `nano_interp_runs` stops re-deriving `interp_runs` and becomes its generalisation. If R1 = (B):
  delete Protocol/NanoBridge/Negotiation/ProtocolTyping (2,397 lines, MAP §7).
- **Literature's lean.** Toninho's monad is the contextual comonad's LINEAR counterpart (toninho2013 p3): its point
  is that a process carries the channels it uses and offers. Nano's resident already carries its effects; what
  would be new is HOLES in a running program. INFERRED: that is not demanded by any deployed consumer today; (B)
  until the activities lane needs a hole inside a continuation.

---------------------------------------------------------------------------------------------------------------------

## PART C — THE PATH

Method per card, from the fold (MAP §5; RULINGS R-0001..R-0020): an impact file (`fold/IMPACT-<card>.md`: the
grep of every consumer, the statement-list before/after, the census digest diff), a cross-family read
(`READ-<card>-grok.md`) asked about RELEVANCE as well as vacuity, then a ledger RELEASE row, then one landing.
Consumer first: each card lands with the consumer that calls it, or does not land. The HOLD R-0001 must be released
by Ember for C1 onward (it freezes new contextual cards).

### C1 — the first real retraction: support pins on kernel cells (P8 withdrawal gap, cv 01a16171)

**Which fix shape the literature favours: B.** Reasons, each at source:
1. **de Kleer §4.9** (dekleer1986 p27): a justification is made retractable by conjoining it with an assumption that
   represents its defeasibility; retracting = contradicting that assumption; "This is the only reasonable way to
   retract a justification." Here the defeasibility assumption of "provider authorised" is "grant g is live", and
   revoke already contradicts it (it retires g: READ `Derive.lean:329`). B conjoins it. A does not (it adds a
   SECOND retraction act); C does not (it puts a constraint on pins, not on the justification).
2. **de Kleer's interface rule** (dekleer1986 p4): failures arise when "the problem solver is permitted to make a
   control decision … without informing the TMS". Shape **A** makes the withdrawal a separate act (unpost the fact)
   that the revoker must remember; forgetting it is exactly the uncommunicated control decision. The gap stays
   reachable by any client that revokes without unposting.
3. **Doyle** (doyle1979 p6): the update set is "those nodes whose well-founded arguments depend on changed nodes".
   With the antecedent recorded (B), the changed node (g) is in the argument; with a self-row copy, it is not.
4. **LPCFS** (morgenstern2011 p2): the monitor checks "each certificate in a submitted request", atomically with the
   use-once check. B puts g in the request's justification and its check in the same Turn as the spend (the kernel
   already pin-checks g atomically; B makes the program read the result). C cannot: the measured P8 commit cites g
   only as an EXTRA PIN, not as `via` (READ `Lang/Journey.lean:2177` `via := arg "grant"` and `:2285` `p8Arg asset owner cap`: `via` = `cap`, B's transfer grant). The
   kernel does not know g is authority; C needs a new "cites as authority" field on the call, which is B's
   information moved into the kernel, plus a kernel semantics change to pins that are observations (law 1:
   a second meaning of a pin).

So ROOT's recorded lean toward C (cv 01a16171 body) is, by these four sources, the containment shape: it would make
one pin pattern illegal while leaving the justification a copy. Under breadstuffs/CLAUDE.md ("a containment while
naming the real fix as later … the phases are backwards") C is the move to refuse.

**What lands.**
- `SupportPin.cell (id : D)` in `HoleCode.supports` (ROM) and the matching Std.hole support kind; `selectHole` and
  `instantiateHoles` take `look` (already in scope at `Lang/Program.lean:210`).
- the generated Std.hole judgment gains a pinned-cell read for its `cell` supports. INFERRED design point to price
  in the impact file: a method body today sees `[req, args, state, rows]` and no pins (ACT-D §9 correction 1, READ
  there); so either the Lang runtime evaluates cell supports BEFORE the body (as `selectHole` does for ROM
  supports: cleaner, no new Term former), or the method env gains a `cells` view. Default: the former, so the Term
  language does not grow.
- The semantic choice for `.cell g`: "g is live" (`look g = .ok (some c)`), optionally plus slot predicates
  (target/grantee/right) — NOT "g at version v". A grant's ledger slots move on every spend (KERNEL-60), so a
  version-exact support would be withdrawn by unrelated spends: INFERRED, and the reason Doyle's antecedent is the
  fact ("authorised"), not the snapshot.
- Journey: P8.2's deleted row returns as REAL: "re-pinned tombstone: refused derivationMoved" (plus the plant).
- Theorems B.1.

**What it deletes.** The self-row copy of a cell's liveness in P8 (`hole_postArg g pin` for authority supports).
Any `HolePin.row` used to stand for another object's state.

**Risk.** (i) The Std.hole generator re-emits; every package id holding it changes (a re-genesis; cheap).
(ii) `selectHole_origin`'s conclusion changes meaning; the S9 lesson (REV A5) is to grep foreign proof consumers
before building. (iii) Part D.1.

### C2 — the live bridge (MAP §7 R2 / S13), stated at the kernel World

**What lands.** `kernelWorld`, `romIface`, `romCandidate`, and B.2's theorem, over the C1 tokens (otherwise the
bridge would RATIFY the gap: MAP §7 R2 proposed `live t := holePinHolds rv self t`, rows under self only — the very
definition that admits the tombstone; INFERRED, and the strongest reason C1 precedes C2).

**What it deletes.** `HoleBridge`'s closed-fragment premises become unnecessary (the bridge supersedes
`hole_judgment_admission_bridge`'s `hctx`/`hhyps`; keep the Std.hole-specific half only if its consumer survives);
the CMTT core (R3 default: delete after S13, MAP §7); `LiveJourney`'s five instances stay as teeth.

**Risk.** Part D.2: the Status/HoleRefusal mismatch. If more than the pre-judgment refusals fail to map, take
`judge`/`Status`/`provenance` out of Lang (MAP R2's other branch) and keep `CalculusLaws` + `langLaws`.

### C3 — worlds as candidates: the live label

**What lands.** B.3: `live_label_iff`, a read-only `label` method on the Std.hole package, one journey row after the
revoke.

**What it deletes.** Nothing on main (Worlds died in S5). It retires the stable-model vocabulary from future cards:
the decision text says why (no OUT-lists over derived nodes; B.7).

**Risk.** Without a consumer that reads the label (the resident tick), this is breadth again. Land only with the tick.

### C4 — provenance over live selections

**What lands.** B.4(a): the receipt carries its monomial; the audit re-derives it. B.4(b) only with a planner.

**What it deletes.** `Provenance.lean`'s abstract duplicates if the instance subsumes them (it will not: the
abstract `provenance_iff` is what C3/C4 instance; keep it).

**Risk.** Receipt type churn across every proof that destructures `HoleSelection`.

### C5 — repair with transport over `resolveHole`

**What lands.** B.5's `live_repair_outcome`; the five `LiveJourney` instances become corollaries.

**What it deletes.** `Outcomes.lean`'s abstract theorems stay (they are what is instanced); delete any abstract
`Outcome` constructor that no live outcome produces (check `kept` vs `strengthening` at `langData`).

**Risk.** Two views that differ by "one edit" are not what the kernel produces between invocations (many pins
move per Turn); the theorem must quantify over a multi-edit `Change`, or it describes no real transition.

### C6 — boundary = Ω (no card; a docstring and a deletion)

B.6. If `consumer_boundary` has no consumer after C2, delete `Consumer`/`Consumer.holds` and the theorem.

### C7 — acyclicity over the pin graph

**What lands.** B.7's `support_precedes` over `touchCheck`/`receive`, consumed by C3's docstring and by the
decision text of the first card that lets a hole's support be another hole's selection row.

**Risk.** Definitional (Part D.3). Land only with its plant.

### C8 — the interface-automata reading of the receiver

**What lands.** B.8 over `Std.machine` packages, ONLY once a package-replacement path exists for programmed objects
(ACT-D §9 correction 2: `relaw` on a programmed object is refused). Until then: the decision text of the activities
lane names refusals as illegal inputs and states de Alfaro's limitation (dealfaro2001 p8 via READ-LIT §1.12:
"cannot express which inputs must occur") as the reason nano's deadlines are law refusals, not liveness.

**What it deletes.** Protocol's polarity half if R1 = (B).

**Risk.** No consumer → do not land (this was P5's failure mode: REV H1).

### C9 — use-once grants as certificates

**What lands.** B.9 with C1 (same landing or the next): the P8.4 rows already exercise it.

**Risk.** Low; it is a conjunction of C1 with `spendVia_ok` under one `receive`.

### C10 — R1 and R3 rulings, written down

Ask Ember: R1 default (B) delete Protocol; R3 default delete the CMTT core after C2, BECAUSE `HoleCode` is the
ROM-grain `box` (A.1). Both deletions are the fold's S13–S15 (RULINGS R-0020 stops at S12).

### Order and why

C1 → C9 → C2 → C5 → C3 → C4(a) → C7 → C6 → C10 → C8. C1 first because it is a measured admission of a revoked
authority and because every later card states its theorem over the World C1 defines. C9 rides with C1. C2 next
because C3–C5 quantify over its instance. C8 last because it has no consumer yet.

---------------------------------------------------------------------------------------------------------------------

## PART D — THREE WAYS THIS REORIENTATION IS MOST LIKELY WRONG

### D.1 B is the wrong owner of the withdrawal: the support should be the PROVIDER's posted fact

**The claim at risk.** C1 says the justification must read the grant cell. The activities design ruled the
opposite on purpose: "a support is a ROW UNDER THE HOLE OBJECT (an assumption token its owner posts, re-pins,
withdraws)" (ACT-D §9 correction 1, READ), because a method cannot see pins. If the right repair is that the
PROVIDER (not the requester) posts its support and the revoker's revoke and unpost are one Turn (a call with two
bodies), then shape A is atomic and B adds a Lang capability nobody needs. (Deployed today: only a fact's poster may retract or re-pin it, READ `Lang/StdHole.lean:183–192`;
in P8 the requester `a` both issues the provider grants and posts the facts, READ `Lang/Journey.lean:2262–2280`.)

**The measurement that refutes C1.** In the P8 composition, who may post and unpost a fact (Std.hole's `posted`
guard, READ `Lang/StdHole.lean:183–192`: `by` must equal the signing agent) and who may revoke the grant (the
issuer, READ `Derive.lean:328`). Build the row "revoke g and unpost g's fact in ONE call" and the row "revoke g
only". If nano can REFUSE the second by construction (a law on the grant's issuer, or a generator rule that the
fact's poster is the grant's issuer and revocation is unpost), A closes the gap with no new read and C1 is wrong.
If the second row stays admissible (the measured state today, IMPACT-S2 §0.2), A leaves the gap reachable and C1
stands.

### D.2 The live bridge cannot be stated without premises; the abstract judge is the wrong spine

**The claim at risk.** Parts B.2–B.5 and C2–C5 assume `Contextual.judge` is what `selectHole` computes.

**Evidence it may be wrong** (READ): `judge` has five outcomes including `pruned` (live blockers) and `uncovered`
(per-candidate cost over budget) (`Closure.lean:129–137`, `:226–232`); `HoleROM` has no blockers, no per-candidate
cost and no budget (READ `HoleROM.lean:15–34`); `HoleRefusal` has 21 constructors (READ `LiveHoles.lean:13–35`),
of which only `supportMoved`, `derivationMoved`, `guardBlocked` have a natural Status.

**The measurement.** Write `selectHole_judge` as a Lean statement (no proof) against f8d04ac and count (a) the
hypotheses it needs beyond "the World is `kernelWorld`", (b) the `HoleRefusal` constructors that map to no Status,
(c) the `Status` constructors no deployed run produces. If (a) > 0 on any landed theorem, or (c) ≥ 2, the abstract
closure is a second shape of the live judgment, not its spine: take `judge`/`Status`/`provenance` out of Lang (MAP
R2's other branch) and restate B.3/B.4/B.5 directly over `selectHole`.

### D.3 The promotions are renames: "the literature's terms" become a third vocabulary for deployed facts

**The claim at risk.** Several Part B rows (B.6 boundary, B.7 acyclicity, B.9 certificates, the A.8 readings of
`receive_congr` and `audit`) say "nano already has this". The review's H2 finding was that card deliverables met
in letter by definitional facts passed every reader (REV H2: 30% of 697 theorems had no binders; 37% had ≤ 2-line
proofs). A reorientation that relabels `receive_congr` as "verifying traces" and lands `support_precedes` as a
theorem is the same breadth with better citations.

**The measurement.** For each card, before building: the statement list goes to a cross-family reader with ONE
question per theorem — "name the deployed mutation that makes this false". A theorem with no such mutation (it
holds of every implementation of its types) is a docstring, not a card. If more than half of C3–C9's theorems fail
the question, this memo's Part C reduces to C1 + C2 + docstrings, and the reorientation is wrong about how much
promotion is left: the honest map would then be "nano is the system; the literature names it; two real gaps (C1,
the bridge) remain". The same measurement applies to A.2's "nano runs around holes": if no journey row or client
ever needs a PARTIAL RESULT containing holes (Hazelnut's indeterminate form), "open" in the dream means only
"installed and typed with holes", which nano already is.

---------------------------------------------------------------------------------------------------------------------

## Fetch

Fetched this session into `~/paperbin/` (each with a `.txt`; title/abstract verified in every `.txt` by the fetcher):
doyle1979-truth-maintenance-system (42 pp, AIJ 12(3) typeset) · elkan1990-rational-reconstruction-nonmonotonic-tms
(16) · mokhov2018-build-systems-a-la-carte (29) · hammer2014-adapton (11) · alchourron1985-logic-of-theory-change
(22) · artemov2008-logic-of-justification (37) · gupta1993-maintaining-views-incrementally (10) ·
girard2001-locus-solum (207) · doyle1992-reason-maintenance-belief-revision (23; the chapter cut from Gärdenfors ed.
1992) · bogetoft2009-secure-mpc-goes-live (13; ePrint 2008/068 preprint, NOT the FC 2009 published version). Also
created `qed-at-large-proof-engineering-survey-ringer-2019-2003.06458.txt` (it had none).

Not obtained: the Springer FC 2009 version of Bogetoft et al. (no copy on Anna's Archive; ePrint behind Cloudflare,
the Wayback copy was used instead). Anna's Archive notes for the next fetch: `$ANNAS_SECRET_KEY` is not a member key
(fast_download answers "Not a member"); the working domain today is annas-archive.gl; free SciDB links via headless
Playwright, libgen.li `ads.php` by md5 where DOIs with parentheses 404.

Read here at source: nanevski2008, murase2023, dekleer1986, doyle1979, elkan1990, green-karvounarakis-tannen 2007,
gradel-tannen 2412.07986, omar2018, ringer2020, fouquere2013, dealfaro2001, cai2013, mokhov2018, hammer2014,
morgenstern2011, toninho2013. Taken from LIT without re-opening (READ-LIT): Cave–Pientka, Viola et al., Stein et al.,
Lifschitz, GMS93 (the `.txt` of gupta1993 is a garbled text layer), Dannert et al., Kavvos, Ângelo et al.,
Espírito Santo et al. Fetched but not used: AGM, Artemov, Girard, Doyle 1992, Bogetoft.
