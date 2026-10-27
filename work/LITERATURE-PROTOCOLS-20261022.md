# LITERATURE-PROTOCOLS (real 2026-10-22): the literature that makes nano's open-protocol calculus a DEPLOYED part of nano

Scholar (Claude; read-only on nano; wrote this file and fetched papers into `~/paperbin`). Ember's ruling today: KEEP
nanodregg's open-protocol calculus and negotiation theory (R1 = keep, against REORIENTATION C10's default (B)), "maybe we
need to explore more literature for it". This memo says what the calculus is, which ten sources would make it the
strongest version of itself, what each would be stated OVER in the deployed system, and the path to a real consumer.

Trees read:
- nano `origin/main` = **f8d04ac** (fetched into `/Users/ember/dev/nanodregg`, read with `git show origin/main:<path>`).
  Paths below without a prefix are nano paths at f8d04ac.
- `redregg/work/LITERATURE-CONTEXTUAL-20261020.md` (cited LIT §n), `REORIENTATION-20261022.md` (REOR), 
  `ACTIVITIES-DESIGN-20261022.md` (ACT-D), nano `decisions/lang.md` LANG-67 (lines 2848–2934).

Tags. **READ (file pN)** = I read the passage in the `pdftotext -layout` extraction in `~/paperbin`; N = PDF page (form-feed
count). **READ-SCRY (paper_key, Thm n)** = I read the theorem/definition text in Scry's `academic.papers` full text (no page
numbers there; the theorem number is the locator). **READ (path:line)** = I opened the Lean at that line at f8d04ac.
**READ-LIT / READ-REOR** = taken from the earlier memo, whose author read it at source. **INFERRED** = my reasoning or
memory, unchecked this session: disagree with these first. Nothing was built; no Lean was run.

The one-paragraph answer. Nano's calculus is a ONE-PARTY theory: a `Prot` is one participant's plan (an indexed free
program, i.e. an interaction tree / Hancock–Setzer interaction structure, with holes), the peer exists only as the
`Handler` and as the response type, a `theirs` hole is untypable by design, and "negotiation" means one party selecting
among its own candidate fillings against a world. The literature's protocol theories are all MULTI-party: a global
description (global type, choreography, contract pair, game) whose projections are the participants, with compliance /
association as the soundness link and subject reduction + session fidelity + (sometimes) progress as the theorems. The
deployed system already HAS a multi-party protocol with a kernel-side monitor: `Std.activity` (start → captured `waits`
row → resume by a designated resumer, guarded by one row guard) and its first instance the Bell (ringer → bell object →
resident → broker → resident → bell). So the strongest version of the calculus is not more single-party theory: it is
(1) a global type over an activity, (2) its projection onto the object's methods (enforced by `receive`/`World.admit`:
the receiver IS the runtime monitor of Bocchi et al.) and onto the resident's `Prog` (already a `Prot` via
`nano_interp_runs`), (3) the association/fidelity theorem between them, and (4) negotiation re-cut as CO2's `fuse` /
MIA conjunction: two cells' posted contracts admitted together in one Turn iff compliant. The smallest real consumer is
the Bell (C-1 below), and it needs no new kernel object.

---------------------------------------------------------------------------------------------------------------------

## PART A — WHAT NANO'S PROTOCOL CALCULUS IS TODAY

### A.1 The objects (READ `Lang/Contextual/Protocol.lean`, 757 lines; `Lang/Proofs/Contextual/ProtocolTyping.lean`, 132)

- `Sig Ix` = `{Op : Ix → Type, Resp : Op i → Type, next : (op) → Resp op → Ix}` (Protocol.lean:47–50). This is exactly
  Hancock–Setzer's interaction structure / Petersson–Synek tree signature (INFERRED: the literature name; the file says
  "mini's `IxSignature`, restated").
- `Spec` = per operation `consumes : Option Tok`, `requires : List Fact`, `establishes : List Ob` (:55–58).
- `Polarity := ours | theirs` (:61–63): "who chooses a hole's filling".
- `Prot S Hole A i := ret a | call op (k : (r : Resp op) → Prot (next op r)) | hole h` (:72–76). Up to the `hole`
  constructor and the index, this is Xia et al.'s `itree E R := Ret r | Tau t | Vis (e : E A) (k : A → itree)` without
  `Tau` and inductive rather than coinductive (READ xia2020-interaction-trees p4; the comparison INFERRED).
- `Iface` = `{pol, ctx : List Fact, need : List Tok, post, owes : List Ob, accepts : Prot → Prop}` (:84–96); `Ctx` (Ω)
  maps hole names to interfaces; `Subst` (σ) is a partial filling; `subst` is SINGLE-PASS (:107–112); `fill Ω σ` fills
  only `ours` holes (:115–124).
- `Handler` = a deterministic environment `handle : Op i → St i → Σ r, St (next op r)` (:182–183); `interpret` folds the
  execution algebra; a hole yields `Result.stuck` (:186–201). `record` appends each `(i, op, r)` to a trace (:210–212).
- `Hist` = answered trace + at most ONE in-flight call (:224–226); `Open` = (template, Ω, σ, Γ, Δ, Q, Φ, hist)
  (:249–257); `Open.replan` is a plain setter, its guard `Open.Replan` is a Prop in ProtocolTyping (ProtocolTyping.lean:111).
- `View`/`admitOp`/`admits`/`commit` (:274–305): admission of the NEXT concrete effect against current facts and live
  tokens, separate from typing; a hole admits nothing (:292).
- `Frag`/`repair`/`residual` (:340–366): selective re-check of fragments by declared support.
- `Conds`, `firstFit`/`coverAll` (:378–400): scalar illustrations of shared parameters and greedy-vs-complete search.
- `Coin` (:413–486) and `Negotiation` (:491–755): the two instances.

### A.2 The judgment and the theorems (READ ProtocolTyping.lean whole; theorem statements extracted from
`Lang/Proofs/Contextual/Protocol.lean` (968 lines) and `Negotiation.lean` (474))

- `HasProt sp Ω Γ Q Φ Δ P` (ProtocolTyping.lean:31–48): `call` (no token; requires ⊆ Γ; establishes ⊆ Φ; every
  continuation typed), `spend` (token t ∈ Δ; continuations typed at `Δ.erase t`), `hole` (declared, `ours`, ctx ⊆ Γ,
  need ⊑ Δ as bags, post ⇒ Q, owes ⊆ Φ), `ret` (Q holds; ANY Δ left over: affine).
- Completion: `subst_preserves_hasProt` (Protocol.lean:74), `fill_preserves_hasProt` (:106), `HasProt.weaken` (:56),
  `fill_skips_theirs` (:115), `theirs_hole_untypable` (:123).
- Interpretation of substitution: `fold_fusion` (:193), `fold_subst` (:231), `interpret_fill` (:238),
  `interpret_record` (:476: the recording run appends exactly a `Runs` path, or exactly a `Reach` prefix to the hole).
- Subject reduction (the only one): `hasProt_reach` (:317: along any prefix, consumed tokens + remaining Δ' ≤ Δ, the
  established obligations ⊆ Φ, the residual still typed), `at_most_once` (:364), `hasProt_runs` (:374: result ⊨ Q).
- History: `resubst_preserves_started` (:405), `started_obligations` (:438), `Open.resubst_wf` (:460).
- Admission and repair: `admits_local` (:512), `commit_once` (:540), `locality` (:561),
  `repair_agrees_from_scratch` (:569), `repair_residual` (:586), `repair_reuses` (:594).
- Token representation change: `hasProt_mapTok` (:654), `admitOp_mapTok` (:674).
- Scope/foresight: `no_foresight` (:758), `response_dependent_succeeds` (:776), `foresight_iff_names_separate` (:801),
  `response_indexed_names_have_foresight` (:830), `theirs_never_planned` (:841).
- The nano bridge: `nano_runs_iff` (:906), `nano_interp_agrees` (:913), `nano_interp_runs` (:947) — HOSTING-37's
  `interp_runs` (`Hosting/Proofs/ResidentRun.lean:700`) re-derived from `interpret_record` over
  `Nano.ofProg : Hosting.Resident.Prog α → Prot sig (fun _ => Empty) (fun _ => α) ()` (`Lang/Contextual/NanoBridge.lean`).
- Negotiation (Negotiation.lean): `template_hasProt` (:45), `plan_fills`/`cancel_fills` (:52, :59),
  `provider_revoked_unavailable` (:136), `revocation_repair` (:145), `representation_change_transports` (:168),
  `stale_opening_refused` (:179), `competing_commitments` (:187), `replay_refused` (:198),
  `internal_once_not_external_once` (:219), `exactly_once_needs_reply_and_dedupe` (:236), `deadline_expires` (:258),
  `cancel_path_refunds_obligation` (:266), `lost_reply_keeps_obligation` (:309), `lost_reply_blocks_replan` (:342),
  `answered_blocks_replan` (:365), `guard_stricter_than_wf` (:396), `replan_before_dispatch` (:425),
  `separate_witnesses_over_substitutions` (:461).

### A.3 What "open" means here (READ Protocol.lean:8–24; LANG-67 "Why" and item 1)

Three openings, all on ONE participant's plan: (i) an unspecified component (`hole h` with an interface in Ω), (ii) an
interaction with an environment (`call op k`, branching over EVERY response), (iii) an unfinished execution (`Hist`,
possibly with one call in flight whose reply was lost). "Open" does NOT mean an open set of participants, an unknown
peer, or an open-world adversary: the peer is a `Handler` (a deterministic function) in `interpret`, and is the
universally-quantified response in `Runs`/`Reach`. `theirs` holes are never filled (`fill_skips_theirs`) and never
typed (`theirs_hole_untypable`); LANG-67 calls these "this calculus's own rules (a `theirs` hole is a `call`), not
findings" (READ decisions/lang.md:2908–2910).

### A.4 What "negotiation" means here (READ Negotiation section of Protocol.lean:491–755; Negotiation.lean)

ONE party (the buyer) holds the template `reserve; hole` and three candidate fillings (`plan p1`, `plan p2`,
`cancelPlan`); the "providers" are constructors of an `Op` and facts in a `World` record that the module defines
(`World := {now, deadline, auth, capSpent, other}`, :643), not cells, not members, not separate `Prot`s. The theorems
are about which candidate is ADMISSIBLE as the world changes, and about not re-planning after dispatch. The only
two-party fact is `separate_witnesses_over_substitutions` (each side's condition satisfiable, no common θ). There is no
offer, no counter-offer, no acceptance by the other side (`Iface.accepts` is `fun _ => True` in both instances; LANG-67
critique (8): "exercised by no instance yet (named gap)", READ decisions/lang.md:2930).

### A.5 Who consumes it (MEASURED: `git grep "^import <module>$" origin/main -- '*.lean'`)

- `Lang.Contextual.Protocol` ← `NanoBridge`, `ProtocolTyping` only.
- `Lang.Proofs.Contextual.Protocol` ← `Negotiation` only. `Lang.Proofs.Contextual.Negotiation` ← NOTHING.
- No journey row, no Host closure, no kernel or ledger proof imports any of the five modules. The one link to deployed
  code is in the bridge's direction (the calculus imports `Hosting.Resident.Run`; nothing deployed imports the calculus).
  REOR B.10 / C10 already said this; it is still exactly true at f8d04ac.
- Naming hazard (MEASURED, lakefile.lean:29–30): nano has a top-level `Protocol` library (the wire/command protocol,
  `Protocol/Command/*`, `Protocol/Envelope.lean`, …). `Lang.Contextual.Protocol` is unrelated. A reader grepping
  "Protocol" finds two meanings; the session-type promotion should pick a name that is not a third.

### A.6 The calculus against the literature's checklist (INFERRED from Part B's reading)

| the field's object | nano today |
|---|---|
| global description of all parties (global type / choreography / contract pair) | absent; one participant's `Prot` |
| projection / endpoint, duality, compliance between two endpoints | absent (`theirs` hole = untypable, not a dual) |
| subject reduction | `hasProt_reach` (prefix-closed typing, token + obligation accounting) |
| session fidelity (the run follows the global description) | `interpret_record` + `nano_interp_runs` for ONE party |
| progress / deadlock-freedom / liveness | absent; affine `ret` and Φ-as-upper-bound make "every obligation discharged" unstatable |
| failures (crash, omission, lost reply) | `Hist.inflight`, `lost_reply_*`, `internal_once_not_external_once` (a delivery model of the module's own) |
| refinement / subtyping (replace a component safely) | absent (deleted P5/Interfaces toys, REOR A.7) |
| runtime monitoring | absent in the calculus; PRESENT in the kernel (`receive` + row guards), unconnected |
| linear assets | affine tokens (`at_most_once`); the kernel's value is CONSERVED (`admit_value`, Kernel/Proofs/Value.lean:402) |
| negotiation / agreement | single-party candidate selection; `separate_witnesses_*` as the only two-sided statement |

---------------------------------------------------------------------------------------------------------------------

## PART B — THE TEN STRONGEST SOURCES

Each entry: the construct; the theorem the field treats as its soundness; the nano object it would be stated over; what
it defines that nano lacks or does differently. Fetched files are in `~/paperbin` with a `.txt` beside each.

### B.1 Honda–Yoshida–Carbone, "Multiparty Asynchronous Session Types", JACM 63(1) 2016 (POPL 2008)
Read through Scry full text (`academic.papers` key `10.1145/2827695`; not fetched).

- **Construct.** A global type G (Def 3.2 its LTS; Def 3.11 dependency relations; Def 3.12 linearity), projection
  `G↾p` (Def 4.1), coherence (Def 4.2, decidable: "THEOREM 4.3. Coherence of G is decidable"), typing of processes
  against the full projection `[[G]]` (Def 5.8). READ-SCRY (10.1145/2827695, Defs 3.2–5.8, Thm 4.3).
- **Soundness theorems.** "THEOREM 5.19 (SUBJECT CONGRUENCE AND REDUCTION)", "THEOREM 5.22 (COMMUNICATION SAFETY)",
  session fidelity (Cor 5.23: "The interactions of a typable process exactly follow the specification described by its
  global type"), progress (Cor 5.30, under well-linkedness Def 5.27). READ-SCRY (same key).
- **Nano object.** The GLOBAL TYPE of an activity: roles = {initiator (the `start_p` signer), object (the package), resumer
  (the `activityWaiting` guard's `resumer` term, READ `Lang/StdActivity.lean:69`)}, plus, for the Bell, the broker.
  Projection onto `object` = the package's method surface + the generated guard; projection onto `resumer` (for the Bell:
  the resident) = `tickP` read as a `Prot` (`Nano.ofProg`, already a theorem). INFERRED: the design that ACT-D §3.2's
  "IndexedProgram correspondence, exactly" table describes in prose is this projection, not yet stated.
- **What nano lacks.** The global object and projection entirely. Nano's `Prot` is a projection without a global type;
  `Coin`'s peer and `Negotiation`'s providers would become ROLES of a G rather than a `Handler`.

### B.2 Scalas–Yoshida, "Less Is More: Multiparty Session Types Revisited", POPL 2019; and Hou–Yoshida–Kuhn, "Less is More
Revisited: Association with Global Protocols and Multiparty Sessions", arXiv 2402.16741 (v6, 2026)
Scalas–Yoshida read through Scry (key `10.1145/3290343`); Hou et al. fetched: `hou2024-less-is-more-revisited-association.pdf`.

- **Construct.** Typing parametric on a SAFETY PROPERTY φ of typing contexts rather than on a global type: "Theorem 4.6
  (Subject Reduction). Assume Θ · Γ ⊢P and Γ safe. Then, P →P′ implies ∃Γ′ …"; φ "cannot be always true, because we would
  have this counterexample to type-safety" — READ-SCRY (10.1145/3290343, Thm 4.6, §4). Hou et al. restore global types
  through ASSOCIATION `∆ ⊑s G` (Def 3.7: the context splits into subtypes of projections of G plus ended entries; READ
  hou2024 p15), with "Theorem 3.1 (Soundness of Association)" and "Theorem 3.2 (Completeness of Association)" (READ p16)
  and "Theorem 3.3 (Safety, Deadlock-Freedom, and Liveness by Association)" (READ p20); fidelity Thm 4.5 (READ p24).
- **The warning that matters to nano.** Scalas–Yoshida: prior MPST extensions "overlook the consistency requirement … Hence,
  their subject reduction theorems do not hold …, or hold vacuously" — READ-SCRY (10.1145/3290343, §1/§8). This is
  nano's `minted-a-disjunct-provable-from-the-premises-is-vacuous` in the session-type field: a typing premise that no
  real context satisfies makes the theorem empty.
- **Nano object.** φ = "the activity object's admitted histories are prefixes of G's traces"; the association relation
  is between the World's rows/state for the object (the `waits` row's `answered`/`captured`, the machine phase) and a
  residual of G. Theorem 3.1/3.2's shape (each G step matched by a context step and conversely) is the shape of
  `kernel history ⇄ global type` that C-2 below states.
- **What nano lacks / does differently.** Nano's `HasProt` is already φ-style in one respect: the hole rule checks a
  declared interface, not a global type. What it lacks is ANY property of a context of several parties; and the warning
  says: state φ over the deployed contexts and prove it inhabited (a tooth that the Bell's real context satisfies φ).

### B.3 Barwell–Scalas–Yoshida–Zhou, "Generalised Multiparty Session Types with Crash-Stop Failures", CONCUR 2022 (TR
arXiv 2207.02015) — fetched `barwell2022-mpst-crash-stop-failures.pdf`

- **Construct.** Crash-stop failures with OPTIONAL RELIABILITY ASSUMPTIONS: a set R of reliable roles; a crashed endpoint
  gets type `stop` (Def 4, READ p6); crash detection is on the RECEIVING side ("Tp0 detects whether q has crashed when
  waiting for a response", READ p3); safety is `(s;R)`-safety (Def 8, READ p8).
- **Soundness theorems.** "Theorem 11 (Subject Reduction). Assume Θ · Γ ⊢ P where ∀s ∈ Γ : ∃Rs : safe(s; Rs, Γ). If
  P → P′, then ∃Γ′ such that Γ →∗ Γ′ …" (READ p11); Cor 12 type safety; Thm 15 session fidelity; Thm 20 "for all
  ϕ ∈ {deadlock-free, terminating, never-terminating, live}, if Γ is (s; R)-ϕ, then P is ϕ" (READ p13).
- **Nano object.** The resident ↔ broker and resident ↔ member-socket legs: `AskEnd` already distinguishes never-sent /
  answered / lost (READ `Hosting/Proofs/ResidentRun.lean` header: "by how the ask ended: never sent → a forget; answered
  `a` → keep …; lost → keep `(unanswered WHY)`"), which is precisely a receive-side crash-handling branch. The KERNEL is a
  reliable role (every Turn is admitted or refused by name); the broker and the provider are unreliable roles.
- **What nano lacks / does differently.** Nano models ONE lost reply as a history state (`Hist.inflight`) and proves the
  re-plan guard; it never says which roles are reliable, and it cannot state "the resident handles every crash of the
  broker" because the broker is not a role. Barwell et al. make reliability a declared parameter of the safety property.

### B.4 Graversen–Montesi–Peressotti, "A Promising Future: Omission Failures in Choreographic Programming", arXiv
1712.05465 (v4 2025) — fetched `graversen2018-omission-failures-choreographies.pdf`

- **Construct.** The communication primitive DECONSTRUCTED into independently implemented send and receive with
  frames identified so that "senders and receivers agree by construction on how each message should be identified"
  (READ p1); a static analysis, ROBUSTNESS, for delivery guarantees (READ p1).
- **Soundness theorems.** Thm 4.3 progress (READ p14); Thm 4.7 robustness preservation (READ p18); "Theorem 4.8
  (At-most-once delivery)" (READ p18); Thm 4.9 at-least-once (no omission failures assumed) (READ p18); Thm 4.10
  best-effort delivery (READ p19); Thm 5.2 EPP (projection correct, READ p22).
- **Nano object.** `Kernel/Receive/Submit.lean`: "the transaction id is the digest of the signed call, so a call already in
  the journal is `replayed` at its height whatever the World is now" (READ Submit.lean header) — that IS the frame identity
  agreed by construction; plus the resident's "a spent ask is never repeated" (`tick_counts`, ResidentRun.lean:410).
- **What nano lacks / does differently.** `internal_once_not_external_once` and `exactly_once_needs_reply_and_dedupe`
  (Negotiation.lean:219, :236) are stated over `External`, "this module's own delivery and deduplication model"
  (LANG-67, READ decisions/lang.md:2918). Graversen et al. give the general theorem (at-most-once from robustness;
  exactly-once needs no omission) over the projected programs. Over nano, the at-most-once half is a theorem about
  `submit`'s replay recognition, statable NOW with no new model.

### B.5 de Alfaro–Henzinger, "Interface Automata", FSE 2001 (have: `dealfaro2001-interface-automata`); Lüttgen–Vogler,
"Modal Interface Automata", LMCS 9(3:4) 2013 — fetched `luttgen2013-modal-interface-automata.pdf`

- **Construct.** IA: optimistic composition, alternating simulation, the limitation "cannot express which inputs must
  occur" (READ-LIT §1.12, dealfaro p8, p10). MIA adds must/may transitions ("explicit output-must-transitions while
  input-transitions are always allowed implicitly", READ luttgen p1) and, crucially, CONJUNCTION as the greatest lower
  bound: "Theorem 4.7 (∧ is And). … (i) (∃ MIA R and r ∈ R. r ⊑MIA p and r ⊑MIA q) if and only if p ∧ q is defined.
  … (ii) r ⊑MIA p and r ⊑MIA q if and only if r ⊑MIA p ∧ q" (READ p20); inconsistent states F (Def 4.4, READ p19);
  "Theorem 4.14 (Compositionality of MIA-Parallel Composition)" (READ p23).
- **Soundness.** Refinement is substitutive under compatibility (IA Thm 4 READ-LIT; MIA Thm 4.14, READ p23).
- **Nano object.** (a) refinement: a package's methods + laws + guards as an interface automaton over `invoke` calls,
  refusals as illegal inputs (REOR A.7/B.8, READ-REOR); consumer = package replacement (waits for a relaw path).
  (b) **Negotiation**: two parties' requirements are two interfaces over the SAME hole; agreement exists iff their
  conjunction is defined; Thm 4.7(i) is the general form of `separate_witnesses_over_substitutions` (Negotiation.lean:461:
  each side satisfiable, no common θ) — INFERRED correspondence.
- **What nano lacks.** A conjunction operator on `Iface` (the two parties' interfaces for one hole) and the theorem that
  it is the meet. Today the "buyer guard" and "admission" are two Props joined by `∧` over a hand-built `Conds` record.

### B.6 Benveniste et al., "Contracts for System Design", FnT EDA 12(2–3) 2018; Abadi–Lamport, "Conjoining
Specifications", TOPLAS 17(3) 1995
Benveniste read through Scry (key `10.1561/1000000053`; the Inria RR at hal-00757488 answered an HTML challenge, not
fetched); Abadi–Lamport in paperbin (`abadi-lamport-conjoining-specifications-toplas1995.pdf`; I made its `.txt` today).

- **Construct.** Assume/guarantee contracts C = (A, G), refinement ("C′ refines C … if and only if M_C′ ⊆ M_C"),
  composition ⊗, conjunction ∧, and the QUOTIENT: "Property 7 (quotient). We have C ⪯ C1/C2 ⟺ C ⊗ C2 ⪯ C1" —
  READ-SCRY (10.1561/1000000053, Properties 1–7). Abadi–Lamport: "Theorem 3 (Composition Theorem). If, for i = 1,…,n,
  (1) |= C(E) ∧ ⋀ C(Mj) ⇒ Ei …" — circular assume/guarantee made sound (READ abadi-lamport p26; Decomposition Thm 1 p22).
- **Soundness.** "Property 3 (independent implementability). Compatible contracts can be [implemented independently]";
  "Property 1 (refinement). Any implementation of C′ is an implementation of C. Any environment of C is an environment of
  C′" — READ-SCRY (same key).
- **Nano object.** THE HOLE. A hole's interface `Iface` = (ctx/need: assumptions; post/owes: guarantees) is an A/G
  contract; the template-with-a-hole is C1 (the whole protocol's contract) with C2 (the known part); the hole's
  interface SHOULD be (at least) the quotient C1/C2 — the weakest spec a filling must meet so that the completed protocol
  meets C1. INFERRED.
- **What nano lacks / does differently.** Nano DECLARES Ω by hand and proves `fill_preserves_hasProt`: a sufficient
  condition. Property 7 gives the canonical (weakest) Ω and a completeness direction nano has none of: "every filling that
  makes the whole protocol typed satisfies the declared interface". Without it, an over-strong Ω silently excludes good
  fillings and nothing goes red.

### B.7 Castagna–Gesbert–Padovani, "A Theory of Contracts for Web Services", TOPLAS 31(5) 2009; Bernardi–Hennessy,
"Mutually Testing Processes", LMCS 11(2) 2015
CGP read through Scry (key `10.1145/1538917.1538920`); Bernardi–Hennessy fetched (`bernardi2016-mutually-testing-processes.pdf`).

- **Construct.** Contracts as CCS-like behaviours, compliance ρ ⊣ σ (client always succeeds), subcontract σ ⪯ τ,
  FILTERS (a filter restricts the richer service to what the client was promised). "THEOREM 3.9. σ ⪯ τ if and only if
  there exists a filter f such that σ ≼ f(τ)"; filter soundness/completeness Thms 3.13/3.17; "THEOREM 4.5. If ⊢ P : ρ
  and ⊢ Q : σ and ρ ⊣ σ then P ⊣ Q" (contract compliance implies process compliance) — READ-SCRY (CGP Thms 3.9–4.5).
  Bernardi–Hennessy: three preorders (server, client, PEER: "a further refinement preorder based on the mutual
  satisfaction of peers", READ p1) with "p must r" / "p mustp2p r" (Def 2.1, READ p6).
- **Nano object.** `Iface.accepts` ("the acceptance contract on a filling", Protocol.lean:95–96) is the client's
  compliance requirement on a server-chosen filling: CGP's `ρ ⊣ σ`. The filter is `fill`'s restriction `Subst.ours`.
  Bernardi–Hennessy's peer preorder is the right refinement for a negotiation in which BOTH sides must be satisfied.
- **What nano lacks.** Compliance between two `Prot`s (the client's and the server's); `accepts` is a Prop nobody
  instantiates (A.4). CGP's Thm 4.5 is the theorem that would make `accepts` load-bearing: protocol-level compliance
  transfers to the running processes.

### B.8 Bartoletti–Scalas–Tuosto–Zunino, "Honesty by Typing", LMCS 12(4:7) 2016 — fetched `bartoletti2016-honesty-by-typing.pdf`

- **Construct.** CO2: processes ADVERTISE contracts (`tell ↓u C`), the system FUSES two compliant latent contracts into a
  session: "Rule [Fuse] stipulates contract: if there are two compliant contracts, a fresh session s is created; the
  latent contracts are consumed" (READ p9; the rule p10). HONESTY: a process "abides by the contracts it has stipulated in
  all possible contexts, even in presence of dishonest adversaries" (READ p1); Def 4.5 (READ p13).
- **Soundness theorems.** Honesty is undecidable (Thm 4.8, READ p14), so it is approximated by typing: "Theorem 9.9 (Type
  safety). For all closed P, if ⊢ P : f then P is honest" (READ p30); subject reduction Thm 9.6, progress Thm 9.7 (READ
  p29–30); decidable type inference Thm 8.6 (READ p28). Compliance: Def 2.7, "./1 is decidable; ./∞ is undecidable"
  (Thm 2.8, READ p7).
- **Nano object.** THE NEGOTIATION, as it should be: two CELLS each post a latent contract (a row under their own object,
  like `waits`), and ONE signed call that pins both rows performs [Fuse]: `World.admit` admits it iff the two contracts
  are compliant, consuming both rows in the same Turn (atomic by the pin check: "`World.admit`'s pin check refuses the
  Turn when the Host's cells are not what the signer saw", READ `Kernel/Receive/Call.lean` header). Honesty is the
  property of a member's program (e.g. the resident) that it keeps what it fused, against every other member.
- **What nano lacks / does differently.** Nano's negotiation is selection by one party; CO2's is agreement by fusion of two
  parties' independent advertisements, with "dishonest adversary" as the universally quantified context. INFERRED: this
  is the frame in which `separate_witnesses_over_substitutions` is the REFUSAL case of [Fuse] over real cells.

### B.9 Das–Balzer–Hoffmann–Pfenning–Santurkar, "Resource-Aware Session Types for Digital Contracts" (Nomos), CSF 2021
(TR arXiv 1902.06056) — fetched `das2019-nomos-resource-aware-session-types-digital-contracts.pdf`

- **Construct.** Contracts as processes with SHARED binary session types (acquire/accept … release/detach, mutual
  exclusion: "the acquire-release discipline ensures that clients interact with the contract in mutual exclusion", READ
  p5); EQUI-SYNCHRONIZING types: "released back to the same type at which the process was previously acquired" (READ p9);
  LINEAR assets: "the type system forbids a process to terminate while it stores any linear assets, preventing an asset
  from being discarded" (READ p5); amortized resource analysis for gas; a transactional semantics on a ledger (§9, READ p24:
  "Since the contract types are equi-synchronizing, they remain unchanged at the end of transaction execution").
- **Soundness theorems.** "Theorem 1 (Type Preservation)" and "Theorem 2 (Progress). … Either Ω is poised, or it can take
  a step … or some process in Ω is blocked along aS for some shared channel aS" (READ p18); process preservation Thm 4
  (READ p59). Re-entrancy ruled out because a second acquire before release blocks (READ p5).
- **Nano object.** A cell's method surface = a shared session type acquired by one `invoke` and released at the Turn's end;
  equi-synchronization = "the object's machine phase after a judged step is one the declared edges reach"
  (`machine_reached`, `Lang/Proofs/StdChain.lean:100`); linear assets = the kernel's conserved value (`admit_value`:
  "World.admit E w t = .ok w' → ∀ d, w'.valueSum d = w.valueSum d", READ `docs/record/ASSEMBLY-ledger.md:236`).
- **What nano does differently.** Nano's `HasProt` is AFFINE (`ret` drops Δ; `at_most_once`, LANG-67 critique (6)); Nomos is
  LINEAR for assets. For capabilities affine is right (a grant can lapse); for VALUE nano's kernel is already linear, so
  the protocol calculus under-states the deployed guarantee. The promotion should give `Tok` two kinds and prove the
  linear kind by reading `admit_value`, not by a second accounting.

### B.10 Bocchi–Chen–Demangeon–Honda–Yoshida, "Monitoring Networks through Multiparty Session Types", TCS 669 (2017);
van den Heuvel–Pérez–Dobre, "Monitoring Blackbox Implementations of Multiparty Session Protocols", RV 2023
Bocchi et al. read through Scry (key `10.1016/j.tcs.2017.02.009`); van den Heuvel fetched (`vandenheuvel2023-monitoring-blackbox-mpst.pdf`).

- **Construct.** Monitors synthesised from global types guard each principal; a network is "fully monitored".
  "Theorem 5.2 (Local safety)", "Theorem 5.4 (Global safety). If M | M is fully monitored w.r.t. Σ, then |= M | …",
  "Theorem 6.1 (Local transparency)", "Theorem 6.3 (Global transparency)", "Theorem 7.13 (Session fidelity)" —
  READ-SCRY (10.1016/j.tcs.2017.02.009). Van den Heuvel: monitors for BLACKBOXES "whose exact specification is unknown";
  soundness Thm 17 ("if each monitored blackbox in a network behaves correctly … then the entire network behaves
  correctly"), transparency Thm 23 (READ p3, p12); synthesis `gt2mon` (Def 9, READ p10).
- **Nano object.** THE RECEIVER. Members are blackboxes (any signer); `receive` + `World.admit` + the generated row guards
  are the monitor; `audit`/`rederive` is a follower re-running the monitor ("For each logged Turn it decodes the event …
  runs `receive` on its own World, and requires the very same Turn", READ `Kernel/Receive/Audit.lean` header). Local
  safety = "every admitted Turn on an activity object is an action G's projection enables now"; transparency = "a member
  following its projection is never refused".
- **What nano lacks.** The global type from which the guard would be SYNTHESISED; today `activityWaiting` is hand-written
  and its meaning theorems (`waiting_insert_iff`, `waiting_upsert_iff`, `waiting_no_replay`, READ
  `Lang/Proofs/StdActivity.lean:88–320`) are per-guard, not "the guard is the monitor of G".

### B.x Secondary sources (each would sharpen one statement; not in the ten)

- **Xia et al., "Interaction Trees", POPL 2020** (fetched `xia2020-interaction-trees.pdf`): `itree` with `Vis (e : E A)
  (k : A → itree)` (READ p4) — `Prot` is an inductive, indexed itree with holes. Its handler/`interp` laws are the
  library-grade version of `fold_subst`/`interpret_fill`; worth citing in the docstring, nothing to import (law 11).
- **Hinrichsen–Bengtson–Krebbers, "Actris 2.0", LMCS 2022** (have): dependent separation protocols
  `! x⃗:τ⃗ ⟨v⟩{P}. prot | ? … | end` (READ p17); "Theorem 9.1 (Adequacy of Actris)" (READ p47). The construct nano's
  `Spec` approximates: each message carries the RESOURCE it transfers (`{P}`), not just a token name.
- **Ghilezan–Pantović–Prokić–Scalas, "Precise Subtyping for Asynchronous Multiparty Sessions", POPL 2021** (fetched): "the
  asynchronous multiparty session subtyping ⩽ is sound" (Thm 5.2, READ p15) and "denotationally precise" (Thm 7.2, READ
  p24). The bar for package replacement if B.5(a) is ever built: precise = sound and complete for safe replacement.
- **Carbone–Montesi, "Deadlock-freedom-by-design", POPL 2013** (Scry `10.1145/2429069.2429101`): "Theorem 1
  (Deadlock-Freedom)" and "Theorem 3 (EPP)" (READ-SCRY). Choreographies make progress a property of the global program,
  not a theorem per endpoint.
- **Koutavas–Lin–Tzevelekos, "Open-World Assertion Checking for Smart Contracts via Game Semantics", arXiv 2512.22417**
  (fetched): contract vs environment as Proponent vs Opponent; "Theorem A.8 (Soundness and Completeness)" (READ p31):
  every play is a real execution, every open-world execution a play. The game-semantic meaning of "open" that nano's
  calculus does not have: the Opponent is EVERY other member.
- **Ludics** (Girard, Locus Solum, have; Terui, "Computational ludics", TCS 2011, Scry `10.1016/j.tcs.2010.12.026`): the
  daimon is giving up ("not to play the daimon, that is, not to give up", READ girard2001 p36); orthogonality = successful
  interaction; Terui "Theorem 3.6 (Monotonicity)" and "Theorem 3.9 (Separation). If T and U are standard and T ⋠ U, then
  there is a standard anti-design … such that T ⊥ … and U ⊥̸ …" (READ-SCRY, wording INFERRED from a mangled extraction).
  For nano: `Result.stuck` at a hole is a daimon-like end (the run gave up at an unfilled component); separation says
  two inequivalent fillings are distinguished by SOME counter-design, which is the completeness half `accepts` lacks.
  Kept secondary: no deployed object needs designs (LIT §1.10's verdict stands).
- **Neykova–Bocchi–Yoshida, "Timed Runtime Monitoring for Multiparty Conversations", arXiv 1408.5979** (fetched):
  deadlines as monitored clock constraints. Nano's deadlines are law refusals (REOR C8), which is the monitored reading.

---------------------------------------------------------------------------------------------------------------------

## PART C — THE PROMOTION PATH

### C.0 The consumer, named

REOR C8/C10 said the protocol theory "waits" because nothing deployed consumes it (READ-REOR). That was true of a
single-party calculus and of package refinement. It is not true of a MULTI-party calculus, because the deployed system
already runs one multi-party protocol under a monitor:

- **The Bell** (READ `Hosting/Resident/Run.lean` header; ACT-D §3.2 "The Bell as the first instance"): roles ringer,
  bell object, resident, broker. Ringer → object: `ring` (= `start_ask`, inserts the waits/rings row). Object ⇝ resident:
  the pending row, read by `read OBJ pending K`. Resident → broker: one `ask` (after the intent keep). Broker → resident:
  `AskEnd` (answered / lost / never sent). Resident → object: `answer` (= `resume_ask`), guarded by `rung` (LANG-59:
  "answered" refuses a second answer). Object → resident: taken / refused; the resident's re-read decides forget.
- **Std.activity** (READ `Lang/StdActivity.lean`): the generator of that shape for any package: `activityStartMethod`,
  `activityResumeMethod`, the `activityWaiting` guard with named refusals `notResumer | unstarted | captured`; teeth
  `activity_answer_once`, `activity_answer_authorized`, `activity_resume_requires_resumer`, … (READ
  `Lang/Proofs/StdActivityTeeth.lean:63–174`).
- **The monitor** is `receive`/`World.admit` (B.10), and the host-side participant is `tickP` (`Hosting/Resident/Run.lean:401`),
  already a `Prot` by `nano_runs_iff`.

So the SMALLEST REAL CONSUMER: **the Bell's global type, whose projection onto the bell object is what the kernel
enforces and whose projection onto the resident is what `tick_order` proves.** A theorem stated over it is consumed by
the Bell journey rows (LB*, `launcher/tests/resident_bell.rs`) and by the resident's proofs, and it has a tooth: plant a
guard that drops `old.answered = none` → the object's projection admits a second `answer` → the conformance theorem fails.

The SECOND consumer (the negotiation that "actually selects a hole candidate between two cells over the real kernel"):
**[Fuse] over two activity rows.** Two cells each hold a latent offer row; one call pins both and is admitted iff the
offers are compliant; both rows are consumed in that Turn. The deployed atomicity is the pin check plus one Turn. INFERRED:
this needs no kernel change (two pinned rows under two objects in one call is what `rowUnpinned`/`rangeUnpinned` already
police, READ `Kernel/Receive/Call.lean:201–203`); it needs a generator beside `Std.activity` (`Std.offer`?) and the
compliance check as a guard.

### C.1 The ordered cards

Every card follows REOR Part C's method (impact file, cross-family read, ledger row, one landing; consumer first). Premise
prices are mine and INFERRED until each card's impact file measures them.

**PROT-1 — the activity as a `Prot`, stated over the kernel's history (the bridge on the kernel side).**
- Lands: `activitySig plans : Sig Phase` derived from `ActivityPlan` (`Op` at a waiting phase = `resume_p`; `Resp` =
  `p.response`; `next` = the edge the `resume` arm takes) and `activity_history_runs`: for an object built by
  `Std.activity`, the judged steps of any `ObjectHistory` read as a `Reach (activityProt plans) tr _` prefix. Proof route:
  `object_history_chain` (`Kernel/Proofs/Logic/History.lean:357`) + `machine_reached` (StdChain.lean:100) +
  `activity_start_state`/`activity_resume_state` (`Lang/Proofs/StdActivityMethods.lean:9, :64`). This is ACT-D §4.4's
  `activity_history_is_path`, now landing INTO the protocol calculus instead of beside it.
- Consumer: PROT-3; the Bell rows once the Bell is re-cut as an activity (ACT-D §3.2's `lang!`).
- Premise price: the lift's (`X.Lawful`, `Lang.program`, the law in force at every judged step) — none added to landed
  theorems. Tooth: a method outside the declared machine → no `Reach` path.
- Literature: ITrees (the reading of a history as a tree path), HYC Def 3.2 (the LTS of a type).

**PROT-2 — polarity becomes ROLE.**
- Lands: replace `Polarity := ours | theirs` by a role set; a hole's interface names its chooser role; a `theirs` hole
  becomes a `call` whose RESPONDER is a role (LANG-67 already says "a `theirs` hole is a `call`"). Instance: the activity's
  `resumer` term is the responder of `resume_p`. Restate `fill_skips_theirs`/`theirs_hole_untypable` as "a filling is
  typed in its chooser role's projection only". Delete `Polarity`.
- Consumer: PROT-3. Premise price: every theorem that mentions `.ours` (fill_*, SubstOK, HasProt.hole) restated; count
  them in the impact file (INFERRED ~12). Tooth: `activity_resume_requires_resumer` (StdActivityTeeth.lean:160) is the
  deployed tooth of the role check.
- Literature: HYC (roles), Barwell et al. (roles with reliability), Carbone–Montesi.

**PROT-3 — the global type of a two-role activity, its projections, association; the Bell as the instance.**
- Lands: `Glob` (a global type over roles with `Sig`-style indexed messages), `proj : Glob → Role → Prot`, and the
  association theorem in Hou–Yoshida–Kuhn's shape (Thm 3.1/3.2, READ hou2024 p16): the object's projection matches the
  kernel history step for step (from PROT-1), and the resumer's projection is refined by its program. For the Bell:
  `bell_object_conforms` (kernel side, from PROT-1) and `bell_resident_conforms` (host side: `tick_order`'s `TickCore`
  path, ResidentRun.lean:273, is a path of `proj bellG resident`, via `nano_runs_iff`).
- Consumer: the Bell journey + `resident_bell.rs`. Tooth: plant `decideTick` asking twice → `bell_resident_conforms` red;
  plant the `rung` guard without `answered = none` → `bell_object_conforms` red.
- Premise price: none on landed theorems if stated as new conclusions from `tick_order` and PROT-1. The member-socket
  model gap (ACT-D §4.4: "a theorem joining them … would need the member-socket model, which no proof has") remains: the
  JOIN of the two projections into one run is NOT in this card; each projection is proved separately, and the join stays
  a journey row, named.
- Literature: HYC Thm 5.19/Cor 5.23; Hou et al. Thm 3.1–3.3; Scalas–Yoshida's vacuity warning (the context must be
  inhabited: the instance theorem over the real Bell IS the inhabitation).

**PROT-4 — the receiver is the monitor (local safety + transparency).**
- Lands: `activity_monitor_safe`: every Turn `World.admit` accepts on an activity object is an action enabled in the
  object's projection at the current association state (Bocchi Thm 5.2 shape); `activity_monitor_transparent`: a call that
  follows the projection and is signed by the right role is not refused by the guard (Bocchi Thm 6.1 shape; restricted to
  the guard's refusals, since price/budget refusals are outside the protocol and must be named as such).
- Consumer: `audit`/`rederive` (followers re-run the monitor) and the journey. Tooth: the existing
  `activity_*_requires_*` teeth become instances. Premise price: transparency needs "the row was pinned" as a premise
  (LANG-58: the signer pins the row) — a premise on the NEW theorem only.
- Literature: Bocchi et al. (TCS 2017), van den Heuvel et al. (blackboxes = members whose programs are unknown).

**PROT-5 — failures: in-flight, replay, at-most-once, over `submit` and the resident.**
- Lands: (a) `submit_at_most_once`: a signed call whose txId is in the journal is `replayed`, never re-admitted (over
  `Kernel/Receive/Submit.lean`'s retry recognition) — Graversen Thm 4.8's shape, with the frame identity = the call
  digest; (b) re-state `Hist.inflight` and `lost_reply_*` over the resident's `AskEnd.lost` path (the resident never asks
  twice for a kept intent: `tick_counts`), making the broker an UNRELIABLE role and the kernel a RELIABLE one (Barwell
  et al.'s R). Then DELETE `External`/`Consistent`/`internal_once_not_external_once` (the module's own delivery model):
  the deployed objects state it.
- Consumer: the resident proofs and Submit's journey rows. Tooth: drop the replay check in a plant → a replayed call
  admitted twice. Premise price: none on landed theorems (new conclusions over `submit`).
- Literature: Graversen–Montesi–Peressotti; Barwell et al.; Morgenstern et al. LPCFS (READ-LIT §1.18) for the
  check-and-consume atomicity.

**PROT-6 — negotiation as [Fuse] between two cells (the real negotiation).**
- Lands: an offer generator (two objects, each with an offer relation whose row is the cell's latent contract: an `Iface`
  value as data); a `fuse` method on a third (or on either) object that pins BOTH offer rows, checks compliance in its
  guard, and retracts both in one Turn, creating the session (an activity row). Theorems: `fuse_iff_compliant` (admitted
  iff the two offers are compliant: CGP compliance, decidable fragment as in Bartoletti Thm 2.8's `./1`),
  `fuse_atomic` (both rows consumed or neither: the pin check), and over the real World the refusal
  `fuse_refused_disjoint` = `separate_witnesses_over_substitutions` restated over two real offer rows. MIA Thm 4.7(i)
  is the meta-statement: fusion succeeds iff the conjunction of the two interfaces is defined. Then DELETE the
  `Negotiation` module's private `World` and the scalar `priceConds`/`firstFit` illustrations (Protocol.lean:401–408,
  :384–400): they become instance theorems over real rows or go.
- Consumer: a journey row "two members fuse an offer"; the activities lane's hole selection (ACT-D card E: "an `anyone`
  chooser is the open offer"). Tooth: a guard that skips the compliance check → `fuse_refused_disjoint` red.
- Premise price: none on landed theorems; new generator, new rows, re-emit the journey. A `lang!` if it touches
  `Std.activity`'s layout.
- Literature: Bartoletti et al. [Fuse] + honesty; CGP compliance; Bernardi–Hennessy peer preorder (both sides satisfied);
  Lüttgen–Vogler conjunction.

**PROT-7 — the hole's interface as a quotient (completeness of Ω).**
- Lands: for the `Prot` judgment, `iface_complete`: if `fill` with `f` yields a typed protocol, then `f` satisfies the
  WEAKEST interface computed from the template (the quotient of B.6), and the declared Ω is checked to be at least as weak.
  Without this, an over-strong Ω is unrefutable.
- Consumer: the activities lane's candidate check (ACT-D §3.3) once PROT-6 exists. Premise price: INFERRED none.
- Literature: Benveniste Property 7; Abadi–Lamport Composition Theorem for the circular case (two holes that assume each
  other).

**PROT-8 — linear value, affine capability.**
- Lands: split `Tok` into `Cap` (affine: may lapse) and `Val` (linear: `ret` only with Δ_val empty, or the leftover is
  credited back, as LANG-44 (10)'s storage credit is). State the linear half by reading `admit_value`
  (Kernel/Proofs/Value.lean:402), not by a second count.
- Consumer: PROT-6 when an offer moves value (an escrow). Premise price: `hasProt_reach`/`at_most_once` restated for the
  two kinds; count in the impact file.
- Literature: Nomos ("forbids a process to terminate while it stores any linear assets", READ das2019 p5); Toninho et al.
  (READ-LIT §1.16: "`affine ≠ linear` costs us global progress").

**PROT-9 (waits, as REOR C8 said) — refinement for package replacement.** Only when a replacement path for programmed
objects exists. Then precise subtyping (Ghilezan et al.) is the bar, not alternating simulation alone.

### C.2 Order and why

PROT-1 → PROT-2 → PROT-3 → PROT-4 → PROT-5 → PROT-6 → PROT-7 → PROT-8; PROT-9 waits. PROT-1 first because it is the only
card that makes the calculus a CONSUMER of a deployed kernel theorem (today it consumes only the host-side `interp_runs`);
every later card states its theorem over PROT-1's reading. PROT-3 is the smallest real consumer; PROT-4/5 are cheap
because the deployed objects already exist. PROT-6 is the negotiation Ember wanted, and it needs PROT-2's roles. Each card
deletes something: PROT-2 `Polarity`; PROT-5 the private delivery model; PROT-6 the private `World` and the scalar
illustrations; PROT-3 makes `Coin` a test of role-scoped holes rather than a separate game.

---------------------------------------------------------------------------------------------------------------------

## PART D — THREE WAYS THIS IS WRONG, AND THE MEASUREMENT THAT REFUTES EACH

### D.1 The activity protocol is one exchange deep, so a global type is just `Std.machine` with more words

**The claim at risk.** PROT-3's value depends on the deployed protocols having structure a typestate does not: several
roles, branching that depends on who responds, more than one round. If every deployed activity is "start, then one resume
by one resumer, then retire", the global type projects to exactly the machine the generator already declares, and
association = `machine_reached` + the guard's meaning theorems. The MPST layer would be a third vocabulary (REOR D.3's
warning, READ-REOR).
**Measurement.** Count, over every `ActivityPlan` emitted in the tree and the Bell, (a) the number of distinct roles that
sign a step on the object, (b) whether any `resume` arm inserts another `waits` row (a second round), (c) whether any
object's step depends on a different object's row. If (a) ≤ 2, (b) = 0, (c) = 0 everywhere, PROT-3 collapses to a
docstring on `machine_reached` and the Bell's four-role structure lives only host-side (where `tick_order` already states
it). Then the strongest version of the calculus is PROT-1 + PROT-5 + PROT-6, and PROT-3/4 should not land.
(INFERRED expectation: the Bell has 2 kernel-side roles (ringer, resident) and 1 round; the broker is host-side only.
That would refute PROT-3's kernel half and leave its resident half.)

### D.2 The kernel serialises everything, so the asynchronous / failure theories over-model nano

**The claim at risk.** B.3/B.4 import crash-stop and omission theory. But every kernel interaction is a Turn admitted in a
total order; nested `invoke` is synchronous within one Turn; there is no message in flight between two CELLS. The only
asynchrony is host-side (resident ↔ member socket ↔ broker). If so, the kernel half of nano needs only a SYNCHRONOUS
binary theory plus a monitor (B.10 + B.5), and the failure theories apply only to the resident, which already has
`tick_order` over every reply.
**Measurement.** Enumerate every interaction between two cells that is NOT inside one `World.admit` (grep the receivers for
any state that records "dispatched, awaiting" across Turns: today the only such is an activity's `waits` row, which is a
cell's own row, not a message). If the count is zero outside activities, PROT-5(b) is a host-side card only, and the
"reliable kernel / unreliable broker" split is the entire failure model: Barwell et al. reduce to one Boolean per role,
and the right citation is the at-most-once half of Graversen, not the theory.

### D.3 Negotiation is constraint solving over one θ, not a protocol

**The claim at risk.** PROT-6 frames negotiation as fusion of two behavioural contracts. But the one two-sided theorem nano
has (`separate_witnesses_over_substitutions`) is about a single shared parameter θ satisfying two predicates, and LANG-67's
template has ONE `call` before the hole (`reserve`). If every demanded negotiation is a one-shot agreement on θ, then
"compliance" is satisfiability of `A ∧ B` over θ, MIA conjunction and CO2's [Fuse] add nothing over a guard that checks
`A θ ∧ B θ`, and the right literature is the matcher/ATMS already in the closure (REOR B.3), not session theory.
**Measurement.** Read the activities proposal and ACT-D for any negotiation that requires ≥ 2 rounds (offer, counter-offer,
accept) or an interleaving of the two parties' steps before agreement; and check whether any planned offer contract has a
`call` after its first exchange. If none: PROT-6 lands as "two offer rows + one guard checking `A θ ∧ B θ` + atomic
consumption" (still a real consumer, still deletes the private `World`), and the session-type framing of negotiation is
dropped; keep CO2 only for its honesty statement about the member who fused.

---------------------------------------------------------------------------------------------------------------------

## Fetch list

Fetched into `/Users/ember/paperbin/` this session (PDF from arXiv, `.txt` beside it via `pdftotext -layout`):
1. `barwell2022-mpst-crash-stop-failures` (arXiv 2207.02015)
2. `hou2024-less-is-more-revisited-association` (arXiv 2402.16741)
3. `ghilezan2021-precise-async-mpst-subtyping` (arXiv 2010.13925)
4. `luttgen2013-modal-interface-automata` (arXiv 1306.3050)
5. `bartoletti2016-honesty-by-typing` (arXiv 1211.2609)
6. `bernardi2016-mutually-testing-processes` (arXiv 1502.06360)
7. `das2019-nomos-resource-aware-session-types-digital-contracts` (arXiv 1902.06056)
8. `castellan2020-game-semantics-easy-as-pi` (arXiv 2011.05248; skimmed, not used beyond B.x context)
9. `xia2020-interaction-trees` (arXiv 1906.00046)
10. `graversen2018-omission-failures-choreographies` (arXiv 1712.05465)
11. `vandenheuvel2023-monitoring-blackbox-mpst` (arXiv 2306.04204)
12. `koutavas2025-open-world-smart-contracts-game-semantics` (arXiv 2512.22417)
13. `neykova2014-timed-runtime-monitoring-mpst` (arXiv 1408.5979)
Text made for an existing PDF: `abadi-lamport-conjoining-specifications-toplas1995.txt`.
Re-used from paperbin: `dealfaro2001-interface-automata`, `hinrichsen2022-actris2`, `girard2001-locus-solum`,
`toninho2013-higher-order-processes-monadic` (via LIT), `angelo2026-contextual-metaprogramming-session-types` (via LIT).

Read through Scry `academic.papers` full text (not fetched; theorem numbers are the locators): Honda–Yoshida–Carbone JACM
2016 (`10.1145/2827695`); Scalas–Yoshida POPL 2019 (`10.1145/3290343`); Castagna–Gesbert–Padovani TOPLAS 2009
(`10.1145/1538917.1538920`); Benveniste et al. FnT 2018 (`10.1561/1000000053`); Bocchi et al. TCS 2017
(`10.1016/j.tcs.2017.02.009`); Terui TCS 2011 (`10.1016/j.tcs.2010.12.026`); Carbone–Montesi POPL 2013
(`10.1145/2429069.2429101`).

Not obtained: the Inria RR of Benveniste et al. (hal-00757488 returned an HTML challenge; the downloaded HTML was mine and
I removed it), Bocchi et al. ESOP 2010 "design-by-contract for multiparty interactions" (not located on arXiv; it is the
source for assertion-annotated global types and would sharpen PROT-4 with Spec's facts/obligations as predicates —
COULD NOT CHECK), Montesi–Yoshida "Compositional Choreographies" CONCUR 2013 (partial choreographies with open
participants; not located on arXiv — COULD NOT CHECK), Hancock–Setzer interaction structures (identity of `Sig` stated
from memory: INFERRED).
