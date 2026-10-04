# SCHOLAR-LAWS — laws, contracts, and the logics that compose them with calls and concurrency

Scholar: SCHOLAR-LAWS (fork 2, with its seams to fork 1 calls, fork 3 concurrency, fork 4 evolution).
Date: 2026-10-04. Brief: `/Users/ember/dev/redregg/work/PROGRAM-MODEL-BRIEF-20261004.md`.
Papers: `~/paperbin/world-program-model/` (every `.pdf` has a `pdftotext -layout` `.txt` beside it; web
documents were saved as `.txt`/`.md` only). 22 Kagi queries used.

**Tags.** READ = I read the paper's core mechanism sections in the extracted text (named where it
matters), not only the abstract. SKIMMED = abstract + introduction, or the abstract plus one located
passage. INFERRED = a claim from my prior knowledge, or a conclusion I draw that the source does not
state. Every claim about *Mini* below comes from what I read in `~/dev/minidregg/Pred/*.lean` today
(`Pred/Core.lean` constructors, `Pred/Leaf.lean`, `Pred/LawComposition.lean`, `Pred/CoordinationDial.lean`,
`Pred/BoundedQuantifiedView.lean` headers, `Pred/SatisfiableTotal.lean` theorem names) or from the brief.

**What Mini's law language is today (READ in source).** `Pred` = `eq | le | memberOf` on new-state
integer slots; `writeOnce | monotone` (the only two-state atoms: `old[s]` vs `new[s]`); `eqSlots | leSlots |
leSlotsOff` (difference constraints between new-state slots); `witnessed vk` (fails closed without an oracle);
`hashEq` (commit–reveal); `ran program` (re-execution as a controller fact); `not | allL | anyL`. Bounded
quantifiers are *views* that unfold to `allL`/`anyL` (`BoundedQuantifiedView`). Satisfiability: DNF →
difference systems → Bellman–Ford returning a witness or a negative-cycle certificate
(`decide_never_unknown`, `decide_unsat_iff`). Refusals name the first failing leaf (`firstFailingLeaf`).
Laws compose over an authenticated dependency DAG read at one snapshot (`LawComposition`). The coordination
dial classifies a guard as I-confluent or not under slot-wise-max merge (`CoordinationDial`). Missing, and
relevant below: two-state *relational* atoms beyond `monotone`/`writeOnce`, any atom over the *request*
(who invoked, which method, which capability), any history/temporal atom, any atom over another object's
state other than through LawComposition, and any notion of a caller's requirement on the outcome.

Venues: where the downloaded text did not print the venue, the venue is from memory and marked
`[venue from memory]` (or "venue not checked"); URLs and paperbin paths are all verified.

---

## Part I — Annotated bibliography

### A. Behavioural contracts, typestate, session types, choreographies

**A1. Honda, Yoshida, Carbone. "Multiparty Asynchronous Session Types." JACM 63(1), 2016 (POPL 2008).**
http://mrg.doc.ic.ac.uk/publications/multiparty-asynchronous-session-types-jacm/jacm.pdf —
`~/paperbin/world-program-model/honda-mpst-jacm-2016.pdf`. SKIMMED.
The foundation: a global type G describes a whole conversation; it is projected onto one local type per
role; processes typed against their local types are communication-safe and (for well-formed G) progress.
For Mini: G is the natural shape of a *multi-object contract* — a "protocol cell" whose state is the
residual of G and whose law admits a Plan action only if it is the next step of some projection.

**A2. Scalas, Yoshida. "Less Is More: Multiparty Session Types Revisited." POPL 2019.**
https://mrg.cs.ox.ac.uk/publications/less-is-more-multiparty-session-types-revisited/preprint.pdf —
`scalas-less-is-more-2019.pdf`. SKIMMED (abstract, §1).
Shows classic MPST subject reduction has hidden restrictions that broke several published extensions;
replaces global types + duality with a *parametric safety property* on typing contexts, decidable by model
checking (properties stated in modal μ-calculus). Lesson for Mini: the checkable thing is a property of the
current context, not a global type you must author first; this matches a per-step admission check.

**A3. Hou, Yoshida. "Less is More Revisited: Association with Global Protocols and Multiparty Sessions." 2024.**
https://arxiv.org/abs/2402.16741 — `hou-less-is-more-revisited-2024.pdf`. SKIMMED (title/abstract).
Re-establishes the top-down (global-type) route against Scalas–Yoshida's critique via an "association"
relation between global type and typing context. Cited only to note the field has reconciled both routes.

**A4. Castro-Perez, Ferreira, Gheri, Yoshida. "Zooid: a DSL for Certified Multiparty Computation." PLDI 2021.**
https://arxiv.org/abs/2103.10269 — `castroperez-zooid-2021.pdf`. SKIMMED.
First mechanised (Coq) metatheory of asynchronous MPST with a certified endpoint process language that
inherits deadlock freedom and liveness. Evidence that MPST metatheory is mechanisable at the scale Mini's
Lean development already works at.

**A5. Hou, Lagaillardie, Yoshida. "Fearless Asynchronous Communications with Timed Multiparty Session Protocols." ECOOP 2024. [venue from memory]**
https://arxiv.org/abs/2406.19541 — `hou-timed-mpst-2024.pdf`. SKIMMED.
Affine timed MPST: time constraints and timeouts with failure handling, implemented as a Rust toolchain
(MultiCrustyT) with negligible overhead. Directly relevant: every await in a Mini resident should carry a
deadline (block height) and a typed time-failure branch.

**A6. Giallorenzo, Montesi, Peressotti. "Choral: Object-Oriented Choreographic Programming." TOPLAS 2024 (arXiv 2005.09520). [venue from memory]**
https://arxiv.org/abs/2005.09520 — `giallorenzo-choral-2020.pdf`. SKIMMED.
Choreographies as classes whose data types are located at roles; compiled to one Java library per role;
higher-order (choreographies passed as objects). The closest existing design to "a multi-object method
written once and projected onto each object's Plan".

**A7. Shen, Kashiwa, Kuper. "HasChor: Functional Choreographic Programming for All." ICFP 2023.**
https://arxiv.org/abs/2303.00924 — `shen-haschor-2023.pdf`. SKIMMED.
Choreographies as a (freer) monad; endpoint projection is a handler. Relevant because Mini's activities
are already an effect type: a choreography could be an Activity whose handler is projection.

**A8. Bates, Kashiwa, Jafri, Shen, Kuper, Near. "Efficient, Portable, Census-Polymorphic Choreographic Programming." PLDI 2025. [venue from memory]**
https://arxiv.org/abs/2412.02107 — `bates-multichor-census-2024.pdf`. SKIMMED.
Conclaves and multiply-located values (no redundant broadcast for conditionals); *census polymorphism*:
abstracting over the number of participants. Needed for Mini's "genuinely multi-party domains" where the
participant set is data, not code.

**A9. Hirsch, Garg. "Pirouette: Higher-Order Typed Functional Choreographies." POPL 2022. [venue from memory]**
https://arxiv.org/abs/2111.03484 — `hirsch-pirouette-2022.pdf`. SKIMMED.
Higher-order typed choreographies, generic over a local language, with message-type soundness implying
deadlock freedom, all in Coq. Shows the choreography layer can be parametric over the local language
(Mini: over Core4).

**A10. Plyukhin, Peressotti, Montesi. "Ozone: Fully Out-of-Order Choreographies." ECOOP 2024. [venue from memory]**
https://arxiv.org/abs/2401.17403 — `plyukhin-ozone-2024.pdf`. READ (§1–2 start).
Out-of-order (future-based) execution inside choreographies creates *communication integrity violations*
(a value bound to the wrong variable when two same-typed messages race); the fix mixes static and dynamic
message identity. The nearest literature to promise-pipelined calls under a protocol: Mini's pipelined
replies must carry protocol-position identity, not just a type.

**A11. Castagna, Gesbert, Padovani. "A Theory of Contracts for Web Services." POPL 2008 / TOPLAS 2009.**
https://eprints.gla.ac.uk/47889/1/47889.pdf — `castagna-contracts-webservices-2009.pdf`. SKIMMED.
Contracts as behavioural descriptions; a decidable *subcontract* preorder (refining must-testing) with
*filters* as explicit coercions that make a larger service safely usable where a smaller one is expected.
For Mini fork 4: "the new package's protocol is a subcontract of the old" is a decidable upgrade check.

**A12. Das, Balzer, Hoffmann, Pfenning, Santurkar. "Resource-Aware Session Types for Digital Contracts" (Nomos). CSF 2021 (arXiv 1902.06056). [venue from memory]**
https://arxiv.org/abs/1902.06056 — `das-nomos-2019.pdf`. READ (abstract, §1).
Shared binary session types (acquire/release at an equal type — rules out re-entrancy into an inconsistent
contract), linear assets (no duplication/deletion), and amortised resource analysis giving static gas
bounds, with linear-time type checking. The acquire–release discipline is a ready-made rule for Mini's
"several activities per object": an activity acquires the object's shared state and must release it at the
type (law) it acquired.

**A13. Coblenz et al. "Obsidian: Typestate and Assets for Safer Blockchain Programming." TOPLAS 2020 (arXiv 1909.03523). [venue from memory]**
https://arxiv.org/abs/1909.03523 — `coblenz-obsidian-2019.pdf`. SKIMMED.
Typestate (which methods are callable in which abstract state) plus linear `asset` ownership, with a
proved core calculus (Silica) and user studies. Typestate is the cheapest behavioural contract to put into
a Mini law: a `state` slot with `memberOf` plus method-indexed clauses already expresses it.

**A14. Findler, Felleisen. "Contracts for Higher-Order Functions." ICFP 2002.**
https://users.cs.northwestern.edu/~robby/pubs/papers/ho-contracts-icfp2002.pdf — `findler-ho-contracts-2002.pdf`. SKIMMED.
Higher-order contracts are checked lazily at the boundary where a function value is used, and *blame* is
assigned to the party that broke its side. For Mini: when a callee receives a capability or a promise from
a caller, the contract travels with it, and a refusal must name which party's clause failed.

### B. Program logics for concurrent and distributed objects; capability logics

**B1. Jung, Krebbers, Jourdan, Bizjak, Birkedal, Dreyer. "Iris from the Ground Up." JFP 28, 2018.**
https://people.mpi-sws.org/~dreyer/papers/iris-ground-up/paper.pdf — `jung-iris-ground-up-2018.pdf`. SKIMMED (front matter).
The base logic every modern result in this family builds on (resource algebras, invariants, ghost state).
Listed as the foundation, not a recommendation to embed Iris in admission.

**B2. Krogh-Jespersen, Timany, Ohlenbusch, Gregersen, Birkedal. "Aneris: A Mechanised Logic for Modular Reasoning about Distributed Systems." ESOP 2020.**
https://iris-project.org/pdfs/2020-esop-aneris-final.pdf — `kroghjespersen-aneris-2020.pdf`. SKIMMED.
Node-local separation-logic reasoning with sockets; verified a load balancer and 2PC with a replicated log
client. Shows horizontal (node) and vertical (client of a component) modularity are both obtainable.

**B3. Timany et al. "Trillium: Higher-Order Concurrent and Distributed Separation Logic for Intensional Refinement." POPL 2024.**
https://arxiv.org/abs/2109.07863 — `trillium-timany-2024.pdf`. SKIMMED.
Program logic whose adequacy theorem is a *trace refinement* to a model (e.g. a TLA+-style spec), and with
Fairis, liveness under fairness. The right target for Mini *package-level* evidence: "this package refines
its declared protocol", proved once by the certifying checker, never at admission.

**B4. Sergey, Wilcox, Tatlock. "Programming and Proving with Distributed Protocols" (Disel). POPL 2018.**
https://ilyasergey.net/papers/disel-popl18.pdf — `sergey-disel-2018.pdf`. READ (§1, hooks §3).
Protocols as state-transition specifications separate from implementations; composition via *send-hooks*:
"a send-hook could disallow certain transitions of the client protocol unless a particular condition holds
for the local state associated with the core protocol", with no re-verification of the core. This is the
precise logical shape of a Mini law that reads another object's state (LawComposition) to gate a write.

**B5. Wilcox et al. "Verdi." PLDI 2015** — https://homes.cs.washington.edu/~mernst/pubs/verify-distsystem-pldi2015.pdf —
`wilcox-verdi-2015.pdf`. SKIMMED. Verified system transformers (e.g. adding fault tolerance) that preserve
application-level proofs. **B6. Hawblitzel et al. "IronFleet." SOSP 2015** —
https://www.microsoft.com/en-us/research/wp-content/uploads/2015/10/ironfleet.pdf — `hawblitzel-ironfleet-2015.pdf`.
SKIMMED. TLA-style layered refinement in Dafny, safety and liveness; its reported pain with undecidable
SMT queries motivates C2 (Paxos made EPR).

**B7. Sharma et al. "Grove: a Separation-Logic Library for Verifying Distributed Systems." SOSP 2023.**
https://arxiv.org/abs/2309.03046 — `sharma-grove-2023.pdf`. SKIMMED.
Time-bounded invariants for leases, crash recovery, reconfiguration; verified Go KV store at 67–73% of Redis
single-core. The "time-bounded invariant" is the logical form of a lease law in Mini (valid while
`height ≤ lease_end`, a difference constraint).

**B8. Jacobs, Hinrichsen, Krebbers. "Deadlock-Free Separation Logic: Linearity Yields Progress for Dependent Higher-Order Message Passing" (LinearActris). POPL 2024.**
https://iris-project.org/pdfs/2024-popl-dlfactris.pdf — `jacobs-linearactris-2024.pdf`. SKIMMED (§3).
Linearity of channel ownership yields deadlock and leak freedom for dependent session protocols, with
subprotocol refinement. Supports making Mini's reply-obligations linear (exactly one owner must resolve).

**B9. Summers, Müller. "Actor Services: Modular Verification of Message Passing Programs." ESOP 2016.**
https://pm.inf.ethz.ch/publications/SummersMueller16.pdf — `summers-actor-services-2016.pdf`. READ (abstract, §1).
Specifies *response* properties ("every message of kind m will trigger a response satisfying R, possibly
from a different actor") via obligations and two-state assertions, composable without traces or temporal
logic. The logic Mini needs for "what an async call may promise": a resident's service is an obligation
with a relational postcondition between request state and reply state.

**B10. Voss, Sarkar. "An Ownership Policy and Deadlock Detector for Promises." arXiv 2101.01312, 2021 (venue not checked).**
https://arxiv.org/abs/2101.01312 — `voss-promise-ownership-2021.pdf`. SKIMMED.
Each promise is owned by exactly one task obligated to set it; ownership moves explicitly; this makes
"deadlock" definable for promises and detectable (including omitted sets). Directly applicable: a Mini
promise is a write-once slot whose law says only the current owner may resolve it.

**B11. Swasey, Garg, Dreyer. "Robust and Compositional Verification of Object Capability Patterns" (OCPL). OOPSLA 2017.**
https://people.mpi-sws.org/~dreyer/papers/ocpl/paper.pdf — `swasey-ocpl-2017.pdf`. READ (§1–2 key idea).
Robust safety for capability code: a *low value* is one from which no code can extract a direct reference
to private state; user code is safe to link with untrusted code if only low values cross. Gives the first
compositional specs for sealer/unsealer, membranes, caretakers. For Mini: what a capability passed in a
call may expose is a "lowval" question; membranes and caretakers (revocable forwarders) are law-expressible
objects.

**B12. Devriese, Birkedal, Piessens. "Reasoning about Object Capabilities with Logical Relations and Effect Parametricity." EuroS&P 2016.**
https://www.cs.kuleuven.be/publicaties/rapporten/cw/CW690.pdf — `devriese-ocap-logrel-2016.pdf`. SKIMMED.
Kripke logical relation for a JS-like core; capability safety as effect parametricity; evolvable invariants.
Foundation for B11.

**B13. Drossopoulou, Noble, Mackay, Eisenbach. "Holistic Specifications for Robust Programs" (Chainmail). FASE 2020.**
https://arxiv.org/abs/2002.08334 — `drossopoulou-holistic-specs-2020.pdf`. SKIMMED.
Specifications of a module's *emergent* behaviour across all method sequences, with temporal, permission
and provenance operators. Expressive but no proof logic (supplied by B14, B15).

**B14. Mackay, Drossopoulou, Noble, Eisenbach. "Necessity Specifications for Robustness." OOPSLA 2022.**
https://arxiv.org/abs/2209.08205 — `mackay-necessity-specs-2022.pdf`. READ (§1–2).
The operator `from A_curr to A_fut onlyIf A_nec`: a transition from a state satisfying A_curr to one
satisfying A_fut is possible only if A_nec holds now. Key insight: such a spec equals the intersection of
infinitely many Hoare triples ∀stmts.{A1 ∧ ¬A3} stmts {¬A2}, and is obtained from *single-step* necessity
plus encapsulation. Mechanised in Coq. In Mini the kernel judges every single write, so the single-step
form is exactly a law, and the emergent form follows by induction for free (INFERRED). Example spec:
"balance decreases only if some external object now has access to the password" → in Mini, "only if the
invocation carries capability K".

**B15. Drossopoulou, Mackay, Eisenbach, Noble. "Reasoning about External Calls." PACMPL 9 (OOPSLA2), 2025 (extended version arXiv 2506.06544).**
https://arxiv.org/abs/2506.06544 — `drossopoulou-external-calls-2025.pdf`. READ (§1–2, §8).
The newest and most directly relevant paper for fork 1×2. *Protection* ⟨o⟩: no external object reachable
from the current frame has direct access to o. *Scoped invariants* ∀x:C.{A}: if A holds in an external state,
it holds in every external state of the *scoped future* (until the current call returns). Hoare
*quadruples* {A} s {A'} ∥ {A''} with A'' holding at every intermediate external state, so an external
call can be reasoned about with no spec for the callee. Rule: if ⟨x⟩ is protected from the receiver and
all arguments before the call, ⟨x⟩ holds inside it. Worked "Shop.buy calls buyer.pay(account)" example,
Coq-mechanised soundness. For Mini this is the logic of "what a callee may do with what the caller
passed": effects need capabilities; protection is reachability over the capability graph at the snapshot.

**B16. Grossman, Abraham, Golan-Gueta, Michalevsky, Rinetzky, Sagiv, Zohar. "Online Detection of Effectively Callback Free Objects with Applications to Smart Contracts." POPL 2018.**
https://arxiv.org/abs/1801.04032 — `grossman-ecf-2018.pdf`. READ (abstract, §1).
An execution is ECF for object o if an equivalent execution without callbacks into o exists; ECF objects
can be verified modularly as if callbacks did not exist. Dynamic ECF is checkable online in polynomial
time via conflicting accesses and commutativity; replaying all Ethereum history, the DAO and similar
exploits are non-ECF and almost no legitimate executions are. Static ECF is decidable for finite local
state. For Mini: admission re-executes the whole turn and therefore *has* the trace; refusing non-ECF
turns (unless an object opts in) buys modular reasoning for synchronous cross-object calls.

**B17. Patrignani, Blackshear. "Robust Safety for Move." arXiv 2110.05043 (v2 2022; venue not checked, INFERRED CSF 2023).**
https://arxiv.org/abs/2110.05043 — `patrignani-robust-safety-move-2021.pdf`. READ (abstract, §1).
Robust safety = closed-world verifier (Move Prover) + an *encapsulator* (escape analysis) that checks the
closed-world result generalises to arbitrary untrusted callers; certifies >99% of real Move modules. The
contrast with Mini (INFERRED): a per-write kernel law needs no encapsulator, because the judge runs on
every write regardless of which code proposed it.

**B18. Georges et al. "Cerise: Program Verification on a Capability Machine in the Presence of Untrusted Code." JACM 71(1), 2024.**
https://cs.au.dk/~birke/papers/cerise.pdf — `georges-cerise-2024.pdf`. SKIMMED. Program logic plus a
logical relation for *unknown* code on a capability machine; the template for reasoning about known and
unknown components together. **B19. Rousseau et al. "Cerisier: A Program Logic for Attestation in a
Capability Machine." 2026** — https://arxiv.org/abs/2604.13638 — `rousseau-cerisier-attestation-2026.pdf`.
SKIMMED (title/authors). Adds attested code identity to Cerise; relevant to pinned package hashes as
attestations. **B20. Mück, Georges, Dreyer, Garg, Sammler. "Robust Safety via Semantic Back-Translation."
POPL 2026** — https://iris-project.org/pdfs/2026-popl-robustdimsum.pdf — `muck-robust-backtranslation-2026.pdf`.
SKIMMED. Robust safety for a C-like language obtained from a hardening compiler, proved by semantic
back-translation. Evidence the robust-safety programme is still very active.

**B21. Miller. "Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control." PhD thesis, JHU, 2006.**
https://papers.agoric.com/assets/pdf/papers/robust-composition.pdf — `miller-robust-composition-2006.pdf`. SKIMMED.
Defensive consistency, promises, pipelining, "when". Foundational; the pipelining scholar owns its mechanics.

**B22. Miller, Van Cutsem, Tulloh. "Distributed Electronic Rights in JavaScript." ESOP 2013.**
https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/40673.pdf — `miller-erights-js-2013.pdf`. READ (§5–6).
Escrow exchange in 42 lines; the *contract host*: parties agree on issuers, the contract source, the side
each plays, and a mutually trusted host; an invitation is an unforgeable token redeemable once for a
specific side of a specific contract source. Mini already has the host (the kernel) and content-addressed
packages; an invitation = a capability whose meaning includes the pinned package hash and role.

**B23. Agoric. "Zoe: offer safety and payout liveness." Documentation (Zoe v0.24, 2022; payout liveness note 2020).**
https://docs.agoric.com/guides/zoe/offer-safety , https://papers.agoric.com/zoe-payout-liveness/ —
`agoric-zoe-offer-safety-docs.txt`. READ.
"Offer safety means that the user is guaranteed to either get at least what they wanted, or get back a full
refund of what they offered." The user gives Zoe a *proposal* (give / want / exit rule); assets are escrowed
by Zoe, never sent to contract code; the contract only *instructs reallocations*, which Zoe checks; payout
liveness: once exit is triggered, payout happens regardless of contract behaviour. This is "code proposes,
law disposes" with a *caller-side law* attached to each invocation. The single most transferable idea in
this bibliography for fork 1×2.

### C. Smart-contract specification and verification

**C1. Dill, Grieskamp, Park, Qadeer, Xu, Zhong. "Fast and Reliable Formal Verification of Smart Contracts with the Move Prover." TACAS 2022.**
https://arxiv.org/abs/2110.08362 — `dill-move-prover-2021.pdf`. READ (§1–3.2).
Spec language: `aborts_if`, `ensures` with `old(...)`, global memory `invariant`s and two-state
`invariant update` (e.g. "a balance never decreases by more than max_decrease in one step"); invariants are
injected after *every* instruction that touches the relevant memory; modularity by *clusters* — functions
outside a cluster cannot invalidate its invariants, so untrusted modules added later cannot break them.
The whole Diem framework (~8.8K lines Move, ~6.5K lines spec) verifies in minutes. Quantifiers are allowed
and are the source of timeouts. For Mini: the two-state update invariant is the missing Pred atom; Move
proves at publish time what Mini checks at every write.

**C2. Blackshear, Dill, Qadeer, Barrett, Mitchell, Padon, Zohar. "Resources: A Safe Language Abstraction for Money." 2020.**
https://arxiv.org/abs/2004.05106 — `blackshear-move-resources-2020.pdf`. SKIMMED.
Linear resource types, creatable/destroyable only by the declaring module; proves resource conservation
for Move bytecode. Mini's conservation lives in its Book (per the Bread scholar); linear types at the
language level would add the static half.

**C3. Blackshear, Chursin, Danezis et al. "Sui Lutris: A Blockchain Combining Broadcast and Consensus." CCS 2024 (arXiv 2310.18042).**
https://arxiv.org/abs/2310.18042 — `blackshear-sui-lutris-2023.pdf`. SKIMMED.
Owned objects take a consensusless fast path (Byzantine consistent broadcast); shared objects go through
consensus; whether a transaction can skip consensus is checked statically from its inputs. Fork 3 seam: a
law that only the owner can satisfy makes the object "owned" in Sui's sense.

**C4. Sergey, Kumar, Hobor. "Scilla: a Smart Contract Intermediate-Level LAnguage." 2018.**
https://arxiv.org/abs/1801.00687 — `sergey-scilla-2018.pdf`. READ (§1–2.1).
Contracts as communicating automata: "All interaction with the external world … happens either at the very
start of a transition … or at the end, when a message (or messages) … can be emitted", with explicit
continuations to regain expressivity. This is exactly Mini's Plan + activity checkpoint model, independently
arrived at, and its stated purpose is to rule out uncontrolled re-entrancy.

**C5. Annenkov, Nielsen, Spitters. "ConCert: A Smart Contract Certification Framework in Coq." CPP 2020.**
https://arxiv.org/abs/1907.10674 — `annenkov-concert-2019.pdf`. READ (§5 execution layer).
`receive : Chain → Ctx → State → option Msg → option (State × list ActionBody)`: contracts return outgoing
actions, and properties are stated over all *reachable* chain states (e.g. contract-recorded balance ≤
actual balance). Same shape as Mini's method → Plan; confirms the Plan design composes with whole-system
reachability proofs.

**C6. Bernardo, Cauderlier, Hu, Pesin, Tesson. "Mi-Cho-Coq." 2019** — https://arxiv.org/abs/1909.08671 —
`bernardo-michocoq-2019.pdf`. SKIMMED. Coq framework for Michelson (designed for verification), multisig
case study. **C7. Hildenbrandt et al. "KEVM." CSF 2018** — https://daejunpark.github.io/papers/kevm.pdf —
`hildenbrandt-kevm-2018.pdf`. SKIMMED. Executable K semantics of the EVM used for bytecode verification.
**C8. Hajdu, Jovanović. "solc-verify." VSTTE 2019** — https://arxiv.org/abs/1907.04262 —
`hajdu-solcverify-2019.pdf`. SKIMMED. Source-level Solidity annotations (contract/loop invariants, pre/post)
discharged by SMT. **C9. Crafa, Di Pirro, Zucca. "Is Solidity Solid Enough?" (Featherweight Solidity). WTSC 2019**
— https://www.math.unipd.it/~crafa/Pubblicazioni/wtsc19.pdf — `crafa-featherweight-solidity-2019.pdf`.
SKIMMED. Core calculus; many errors (missing function/state, unsafe call-backs) are only caught at runtime.
Together C6–C9 show the Ethereum-lineage tools verify *code* against specs after the fact; none put the
spec in the admission path. (No paper on Solidity's SMTChecker or Certora was downloaded; INFERRED from
C10 that both are spec-annotation + SMT tools in the same family.)

**C10. Tolmach, Li, Lin, Liu, Li. "A Survey of Smart Contract Formal Specification and Verification." ACM CSUR 2021.**
https://arxiv.org/abs/2008.02712 — `tolmach-sc-spec-survey-2020.pdf`. READ (§3.1, §5.2).
Taxonomy: contract-level (temporal, deontic) vs program-level (Hoare) specs; past-time LTL with a
`previously` operator used in two Ethereum spec languages; open challenges include limited temporal
verification at program level and that runtime verification needs instrumentation or a hard fork because
contracts are immutable. Mini's kernel *is* the runtime verifier, which dissolves that last limitation.

**C11. Chakravarty, Chapman, MacKenzie, Melkonian, Peyton Jones, Wadler. "The Extended UTXO Model." WTSC 2020.**
https://fc20.ifca.ai/wtsc/WTSC2020/WTSC20_paper_25.pdf — `chakravarty-eutxo-2020.pdf`. READ (§1–2).
Outputs carry (validator ν, value, datum δ); spending checks ν(value, δ, redeemer, tx) = true, where tx is
the *whole* spending transaction, so a validator can enforce "contract continuity" across a chain of
transactions; state machines (CEMs) compile to EUTXO with a weak bisimulation proved in Agda. EUTXO
validators are Mini laws whose input is the whole Plan, not just the cell's new state.

**C12. Lamela Seijas, Nemish, Smith, Thompson. "Marlowe: Implementing and Analysing Financial Contracts on Blockchain." WTSC 2020.**
https://fc20.ifca.ai/wtsc/WTSC2020/WTSC20_paper_18.pdf — `lamelaseijas-marlowe-2020.pdf`. READ (§2, §4, §5.3).
Every `When cases timeout cont` has a timeout continuation, so every contract reduces to `Close` and refunds;
Isabelle proofs of money preservation and "timeout closes a contract" (a computable `maxTime` bound);
SMT (via SBV) static analysis that a contract never needs a runtime warning for any input. The model for
Mini obligations: every await has a deadline and a default continuation; "funds cannot be locked forever"
is a theorem about the contract shape, not a property to test.

**C13. Bernauer, Faro, Hämmerli, et al. "Daml: A Smart Contract Language for Securely Automating Real-World Multi-Party Business Workflows." 2023.**
https://arxiv.org/abs/2303.03749 — `bernauer-daml-2023.pdf`. READ (§2–3.6, §5).
Templates with `signatory`, `observer`, `controller`, `ensure`. Transactions are *trees* of
Create/Exercise/Fetch actions. Authorization rules: Create needs all signatories in the context A; Fetch
needs a signatory or observer; Exercise needs all controllers in A, and its *consequences* are checked in
the context S ∪ C (the exercised contract's signatories and the choice's controllers), **not** A ∪ S ∪ C:
"a signatory has pre-authorized the consequences of the choices when the contract instance was created",
and delegation is deliberately non-transitive so building blocks keep their authorization analysis when
composed (the atomic Settle/swap example). Privacy by sub-transaction visibility; runs on SQL, BFT, or
encrypted-participant ledgers. The best existing formal answer to "how a callee's contract composes with a
caller's turn".

**C14. Mina / o1Labs. "On-Chain Preconditions", "Permissions", "Account Updates." o1js documentation (v3.0, 2025–26).**
https://docs.o1labs.org/o1js/advanced-concepts/ZkApps/onChainPreconditions , https://docs.o1labs.org/o1js/zkapps/permissions —
`o1labs-mina-zkapp-preconditions-permissions-docs.txt`. READ.
A transaction computed off-chain against observed values carries *preconditions* (`requireEquals`,
`requireBetween` on own state, balance, nonce, network timestamp, and *other accounts*) that the chain checks
at inclusion. `setVerificationKey` is the upgrade permission; it "cannot be set to impossible or proof
permanently, because the Mina proof system may be upgraded". For Mini: preconditions are exactly Pred atoms
(equalities and intervals) over the read set — the decidable *future-indexed* validity condition of a
computation done against a snapshot (pipelined or optimistic).

**C15. Merigoux, Chataing, Protzenko. "Catala: A Programming Language for the Law." ICFP 2021.**
https://arxiv.org/abs/2103.03198 — `merigoux-catala-2021.pdf`. SKIMMED.
Default logic (exceptions over base rules) to mirror legislative structure, compiled with proofs. Relevant to
how Mini law clauses with exceptions and overrides should be authored (Cedar's forbid-overrides-permit is
the decidable special case).

### D. Policy and authorization logics; information flow

**D1. Cutler, Disselkoen, Eline, He, Headley, Hicks, Hietala, et al. "Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization." OOPSLA 2024. [venue from memory]**
https://arxiv.org/abs/2403.04651 — `cutler-cedar-2024.pdf`. READ (§2–4, §5.4).
permit/forbid policies with scope + conditions; deny by default; forbid overrides permit; deterministic,
loop-free, order-independent evaluation; policy *slicing* by principal/resource ancestry; a validator with
singleton boolean types that warns when a policy is always true or always false; and a *symbolic compiler*
to SMT that is decidable, sound and complete for equivalence/subsumption, achieved by "controls on
expressiveness" and finite ground acyclicity constraints instead of quantifiers. Refactoring checks take
~30–80 ms. Decision diagnostics name the determining policies.

**D2. Disselkoen, Eline, He, Headley, Hicks, Hietala, et al. "How We Built Cedar: A Verification-Guided Approach." FSE Companion 2024.**
https://arxiv.org/abs/2407.01688 — `disselkoen-cedar-howbuilt-2024.pdf`. SKIMMED.
Lean model + proofs, Rust production code checked by differential random testing: 4 validator bugs found by
proof, 21 more by DRT/PBT. Mini's house rule is stricter (the Lean *is* the implementation), so Cedar is
evidence for the language design, not for the assurance method.

**D3. cedar-policy. `cedar-lean/README.md` (cedar-spec, main, fetched 2026-10-04).**
https://github.com/cedar-policy/cedar-spec/blob/main/cedar-lean/README.md — `cedar-lean-readme-2026.md`. READ.
Lean theorems now include: sound slicing; sound type checking; *level-based entity slicing* (an expression
that dereferences entities to depth ≤ n evaluates identically on the store sliced at depth n); sound and
complete symbolic compilation; sound and complete verification (equivalence, implication). The depth bound
is the mechanism Mini needs for laws that read other objects: a declared, checked read footprint.

**D4. Backes et al. "Semantic-based Automated Reasoning for AWS Access Policies using SMT" (Zelkova). FMCAD 2018.**
http://www0.cs.ucl.ac.uk/staff/b.cook/FMCAD18.pdf — `backes-zelkova-2018.pdf`. SKIMMED.
Policies → SMT (strings, regex, bit-vectors, integers); questions like "can an arbitrary user write here?";
PSPACE-complete, invoked millions of times a day. Evidence that analysis-time solving is industrial; note it
is *not* in the request path.

**D5. Li, Mitchell. "Datalog with Constraints: A Foundation for Trust Management Languages." PADL 2003.**
https://www.cs.purdue.edu/homes/ninghui/papers/cdatalog_padl03.pdf — `li-datalog-constraints-trust-2003.pdf`. READ (§1).
Datalog extended with constraint domains (ranges, trees, time intervals) stays tractable for *linearly
decomposable unary* constraint domains; RT1^C as a concrete language; KeyNote shown less expressive yet
less tractable. Caution for Mini (INFERRED from the paper's restriction to unary domains plus Revesz's
results it cites): binary difference constraints under recursion need gap-order style restrictions to keep
termination; Mini's laws are non-recursive, so this only bites if Datalog-style derived relations are added.

**D6. Biscuit. `SPECIFICATIONS.md` (eclipse-biscuit, main, fetched 2026-10-04).**
https://github.com/eclipse-biscuit/biscuit/blob/main/SPECIFICATIONS.md — `biscuit-specifications-2025.md`. READ (Semantics, Scopes, Checks, Authorizer).
Append-only signed blocks; Datalog *without negation* plus expressions; `check if` / `check all` /
`reject if`; allow/deny policies, first match wins, no match = deny. *Scopes*: by default a block's rules see
only facts from the authority block, itself and the authorizer, so a later block cannot add rights;
`trusting <public key>` admits third-party blocks. Monotone (no negation) means a check can only become true
as facts are added — CALM-friendly — and revocation is handled outside the logic by revocation ids.

**D7. Becker, Fournet, Gordon. "Design and Semantics of a Decentralized Authorization Language" (SecPAL). CSF 2007.**
https://people.mpi-sws.org/~dg/teaching/lis2014/modules/authorization-1-becker07.pdf — `becker-secpal-2007.pdf`. SKIMMED.
Three deduction rules; `can say` delegation (with depth control), constraints, negated queries; sound,
complete, always-terminating evaluation via translation to Datalog with constraints under syntactic safety
conditions. (DKAL and Binder were not downloaded; INFERRED that they occupy the same Datalog-delegation family.)

**D8. Pang et al. "Zanzibar: Google's Consistent, Global Authorization System." USENIX ATC 2019.**
https://www.usenix.org/system/files/atc19-pang.pdf — `pang-zanzibar-2019.pdf`. READ (§2 consistency).
Relation tuples + userset rewrites at trillion scale; the *new enemy problem* (applying a stale ACL to new
content) solved with *zookies*: content writes record a snapshot timestamp, and later checks must be
evaluated at a snapshot at least that fresh. For Mini: a law that reads another object's authority state
must state *which snapshot* — LawComposition's "all guards same snapshot" is the strong form.

**D9. Arden, Liu, Myers. "Flow-Limited Authorization." CSF 2015.**
https://www.cs.cornell.edu/andru/papers/flam/flam-csf15.pdf — `arden-flam-2015.pdf`. SKIMMED.
Delegation and revocation are themselves information flows; delegation can enable unauthorised
downgrading. FLAM integrates authority and flow in one lattice. Relevant when Mini's laws (public) and
cards/projections (per-viewer) must not leak through the authorization decision itself.

**D10. Acay, Recto, Gancher, Myers, Shi. "Viaduct: An Extensible, Optimizing Compiler for Secure Distributed Programs." PLDI 2021.**
https://www.cs.cornell.edu/andru/papers/viaduct/viaduct-tr.pdf — `acay-viaduct-2021.pdf`. SKIMMED.
Information-flow labels on a single program drive automatic selection of protocols (replication,
commitments, MPC, ZKP) per sub-computation, via a cost model. The IFC analogue of choreography projection;
a later Mini lane could choose "re-execute in the clear" vs "BFV" per clause from labels.

### E. Decidable fragments, solvers, monitors, certificates

**E1. Padon, Losa, Sagiv, Shoham. "Paxos Made EPR: Decidable Reasoning about Distributed Protocols." OOPSLA 2017.**
https://arxiv.org/abs/1710.07191 — `padon-paxos-made-epr-2017.pdf`. READ (§1).
Model protocols in uninterpreted first-order logic and transform them so verification conditions land in
EPR (∃*∀*, Bernays–Schönfinkel–Ramsey): decidable, finite-model property, so a non-inductive invariant
yields a *finite, displayable counterexample to induction*. Verified Paxos, Multi-, Vertical, Fast,
Flexible, Stoppable Paxos. IronFleet's undecidable SMT queries are cited as the pain this removes. For Mini:
the template for growing the law language with *relations* (membership, quorums, ownership graphs) while
keeping decision procedures complete.

**E2. Cotton, Maler. "Fast and Flexible Difference Constraint Propagation for DPLL(T)." SAT 2006.**
https://www-verimag.imag.fr/~maler/Papers/ffdcp.pdf — `cotton-difference-constraints-2006.pdf`. SKIMMED.
Incremental theory propagation for x − y ≤ c inside DPLL(T). Mini's Bellman–Ford-on-DNF is the naive
point of this design space; if law authoring ever needs disjunction-heavy satisfiability, DPLL(T) with
difference-logic propagation is the standard upgrade, and its explanations are negative cycles (the
certificate Mini already returns).

**E3. Barbosa, Reynolds, Kremer, et al. "Flexible Proof Production in an Industrial-Strength SMT Solver." IJCAR 2022.**
https://gereon-kremer.de/static/2022-ijcar-cvc5-proofs.pdf — `barbosa-cvc5-proofs-2022.pdf`. SKIMMED.
cvc5 emits fine-grained, checkable proofs. The relevant architecture for Mini is *find untrusted, check
trusted*: any solver used at law-authoring or upgrade time should return a certificate (model or
Farkas/negative-cycle refutation) checked by Lean.

**E4. Basin, Klaedtke, Müller, Zălinescu. "Monitoring Metric First-Order Temporal Properties." JACM 62(2), 2015.**
https://people.inf.ethz.ch/basin/pubs/jacm15.pdf — `basin-mfotl-monitoring-2015.pdf`. SKIMMED.
Monitorable safety fragment of metric first-order temporal logic: past and *bounded* future operators with
time intervals, finite relations, aggregations. **E5. Basin et al. "VeriMon: A Formally Verified Monitoring
Tool." ICTAC 2022 [venue from memory]** — https://pm.inf.ethz.ch/publications/BasinDardinierEA22.pdf — `basin-verimon-tool-2022.pdf`.
SKIMMED. An MFOTL monitor (Since/Until, multi-way joins, sums/averages) verified in Isabelle, motivated by
real bugs found in the unverified MonPoly. Evidence a verified temporal-law checker is buildable.

**E6. Havelund, Peled, Ulus. "First-Order Temporal Logic Monitoring with BDDs" (DejaVu). FMSD 2020 (FMCAD 2017). [venue from memory]**
https://havelund.com/Publications/fmsd-2018-dejavu.pdf — `havelund-dejavu-fo-temporal-2018.pdf`. READ (§1).
Past-time first-order temporal logic (QTL) — e.g. `∀f (close(f) → (¬close(f) S open(f)))` — monitored
incrementally: past-time properties are exactly the safety properties whose violation is visible on the
prefix, and the monitor keeps one summary per subformula. For Mini: a past-time law compiles to
kernel-maintained *history slots* in the cell, after which the law is again a two-state Pred over
(old history, new state) — temporal laws without leaving the decidable judge (INFERRED design; the
incremental-summary mechanism is the paper's).

**E7. Jhala, Vazou. "Refinement Types: A Tutorial." FnT PL 2021 (arXiv 2010.07763).**
https://arxiv.org/abs/2010.07763 — `jhala-refinement-types-tutorial-2020.pdf`. SKIMMED.
Types refined by predicates from a decidable logic, checked by generating verification conditions for an
SMT solver. The cleanest model for "generate the law from .obend": `requires`/`ensures`/invariants on
method signatures, restricted to the law fragment, become law clauses.

### F. Consistency, I-confluence, CRDT verification (the fork 2 ↔ fork 3 seam)

**F1. Bailis, Fekete, Franklin, Ghodsi, Hellerstein, Stoica. "Coordination Avoidance in Database Systems." PVLDB 8(3), 2014.**
https://arxiv.org/abs/1402.2237 — `bailis-coordination-avoidance-2014.pdf`. READ (§1–4, Table 2).
I-confluence (invariant + merge + transactions) is necessary and sufficient for coordination-free
execution preserving the invariant; table of which SQL constraints are I-confluent under which operations
(foreign-key insert yes, delete no; AUTO_INCREMENT no). TPC-C: 10 of 12 invariants I-confluent, 12.7M
New-Order tx/s on 200 servers.

**F2. Hellerstein, Alvaro. "Keeping CALM: When Distributed Consistency Is Easy." CACM 63(9), 2020.**
https://arxiv.org/abs/1901.01930 — `hellerstein-keeping-calm-2019.pdf`. SKIMMED.
CALM theorem: a program has a consistent coordination-free distributed implementation iff it is monotonic.
For laws: a monotone law (Biscuit-style negation-free) can be checked on any replica's partial view
without changing its verdict later; negation and deletion need coordination.

**F3. Gotsman, Yang, Ferreira, Najafzadeh, Shapiro. "'Cause I'm Strong Enough: Reasoning about Consistency Choices in Distributed Systems" (CISE). POPL 2016.**
https://www.cs.ox.ac.uk/people/hongseok.yang/paper/popl16b-full.pdf — `gotsman-cise-2016.pdf`. SKIMMED.
First modular proof rule showing that a chosen *token/conflict relation* (which operation pairs must be
ordered) suffices for an integrity invariant under causal consistency; per-operation reasoning, SMT-automated.
The generalisation Mini's coordination dial needs: from "is the guard I-confluent under max-merge" to
"which pairs of methods must coordinate for this law".

**F4. Nair, Petri, Shapiro. "Proving the Safety of Highly-Available Distributed Objects" (Soteria). ESOP 2020.**
https://perso.lip6.fr/Marc.Shapiro/papers/2020/esop2020.pdf — `nair-soteria-2020.pdf`. SKIMMED.
State-based (merge) version of F3, per-operation rules, automated in Boogie. **F5. Shapiro, Bieniusa,
Preguiça, Balegas, Meiklejohn. "Just-Right Consistency." 2018** — https://arxiv.org/abs/1801.06340 —
`shapiro-just-right-consistency-2018.pdf`. SKIMMED. CRDTs + transactional causal consistency for
everything AP-compatible; *bounded counters* (escrow) for the common CAP-sensitive case; static analysis for
the rest. **F6. Burckhardt, Gotsman, Yang, Zawirski. "Replicated Data Types: Specification, Verification,
Optimality." POPL 2014** — https://software.imdea.org/~gotsman/papers/distrmm-popl14.pdf —
`burckhardt-rdt-spec-2014.pdf`. SKIMMED. Specs as functions of visibility/arbitration relations over events.
**F7. Gomes, Kleppmann, Mulligan, Beresford. "Verifying Strong Eventual Consistency in Distributed Systems."
OOPSLA 2017** — https://arxiv.org/abs/1707.01747 — `gomes-verifying-sec-2017.pdf`. SKIMMED. Isabelle proofs of
RGA, OR-Set, counter convergence over an axiomatic network model. **F8. De Porre, Ferreira, Gonzalez Boix.
"VeriFx: Correct Replicated Data Types for the Masses." ECOOP 2023 [venue from memory]** — https://arxiv.org/abs/2207.02502 —
`deporre-verifx-2022.pdf`. SKIMMED. Automatic verification of 35 CRDTs and OT functions by SMT.

**F9. emberian. lean-uwueave README and PREOSCRIPTING.md (local, read 2026-10-04).**
`/Users/ember/dev/leanuweave/README.md`, `/Users/ember/dev/leanuweave/PREOSCRIPTING.md`. READ (README; PREOSCRIPTING quickstart).
A checked catalogue of which (shape, invariant) pairs are FREE (I-confluent) vs ESCALATES, each with a
two-replica counterexample and priced exits (escrow, segmented re-allocation seams), plus *preoscript*:
certificates indexed by an exact future (`QueryFuture`), acceptance predicate and start index, so "a
certificate for another future or world does not typecheck". This is the strongest existing design for
future-indexed evidence in Ember's own work and the natural home of Mini's per-clause coordination grade.

### G. Governance and evolution

**G1. Suber. "Nomic: A Game of Self-Amendment" (Appendix 3 of *The Paradox of Self-Amendment*, 1990).**
https://legacy.earlham.edu/~peters/writing/nomic.htm — `suber-nomic-paradox-self-amendment-1990.txt`. READ (Initial Set 101–116, 201–213, §A).
Immutable and mutable tiers; *transmutation* (immutable → mutable) requires unanimity and must be explicit;
"In a conflict between a mutable and an immutable rule, the immutable rule takes precedence"; "No
rule-change may have retroactive application"; legality of a move can become undecidable or paradoxical
(Rule 213). The design lesson: tiered amendment thresholds, explicit tier changes, no retroactivity, and a
*decidable* legality check — which Nomic lacks and Mini can have.

**G2. Allombert, Bourgoin, Tesson. "Introduction to the Tezos Blockchain." HPCS 2019.**
https://arxiv.org/abs/1909.08458 — `allombert-tezos-2019.pdf`. READ (amendment section).
Shell vs protocol split; protocol proposals are hashes of source; four ~3-week periods: proposal, selection
vote, a side *test chain* running the elected protocol, final vote needing an 80% supermajority; the
amendment procedure is itself part of the amendable protocol.

**G3. Salehi, Clark, Mannan. "Not So Immutable: Upgradeability of Smart Contracts on Ethereum." WTSC 2022.**
https://arxiv.org/abs/2206.00716 — `salehi-not-so-immutable-2022.pdf`. SKIMMED.
Six upgrade patterns; 1.4M proxy contracts; ~50% of upgradeable ones are controlled by a single externally
owned key, ~14% by small multisigs. **G4. Liu, Li, Wu, et al. "Demystifying the Characteristics for Smart
Contract Upgrades." 2024** — https://arxiv.org/abs/2406.05712 — `liu-upgrade-characteristics-2024.pdf`.
SKIMMED. 583 upgraded proxies, 973 versions; 4,334 ABI-breaking changes; 36 storage collisions; initialization
attacks; the Pike Finance upgrade that introduced a storage collision and enabled a second theft. Evidence
that untyped upgrade with key-held authority is the dominant real-world failure.

**G5. Hayden, Magill, Hicks, Foster, Foster. "Specifying and Verifying the Correctness of Dynamic Software Updates." VSTTE 2012.**
https://natefoster.org/papers/dsu-correct-vstte12.pdf — `hayden-dsu-correct-2012.pdf`. SKIMMED.
Client-oriented specifications of update correctness, verified on a *merged program* combining old and new
versions with off-the-shelf tools. The model for stating "the upgrade preserves what clients could observe".

**G6. Litt, Lim, Kleppmann, van Hardenberg. "Project Cambria: Translate your data with lenses." Ink & Switch, 2020.**
https://www.inkandswitch.com/cambria/ — `litt-cambria-inkandswitch-2020.txt`. SKIMMED.
Bidirectional lenses between schema versions, composed along a lens graph, giving both backward and forward
compatibility for collaborating peers on different versions. The typed-migration shape for Mini packages.

**G7. Mimram, Di Giusto. "A Categorical Theory of Patches." MFPS 2013.**
https://arxiv.org/abs/1311.3903 — `mimram-categorical-patches-2013.pdf`. SKIMMED (title/abstract).
Merging patches as pushouts in a free completion that makes conflicts first-class objects. Background for
concurrent edits to a package or a law.

### H. Effects, reversibility, liveness (Bread-listed, read for the seam)

**H1. Plotkin, Pretnar. "Handling Algebraic Effects." LMCS 9(4), 2013.** https://arxiv.org/abs/1312.1399 —
`plotkin-handling-effects-2013.pdf`. SKIMMED. Handlers as interpreters of effect operations; the kernel is
the outermost handler of Mini's Activity effects, and a law is a constraint on what that handler may commit.
**H2. van Glabbeek. "Justness: A Completeness Criterion for Capturing Liveness Properties." FoSSaCS 2019.**
https://arxiv.org/abs/1909.00286 — `vanglabbeek-justness-2019.pdf`. SKIMMED. Justness (weaker than weak
fairness) as the liveness assumption; the right assumption under which "every promise with a deadline is
eventually resolved or defaulted" should be stated. **H3. Danos, Krivine. "Reversible Communicating Systems"
(CONCUR 2004) / "Transactions in RCCS" (CONCUR 2005).** https://hal.science/hal-00784051 — not downloaded
(HAL returned HTML; Springer paywalled). INFERRED: distinguishes reversible from irreversible (committed)
actions; the basis for "reversibility tiers".

---

## Part II — Synthesis: what to build into Mini, ranked

The literature converges on one architecture, and Mini is already most of the way there: **code proposes,
a decidable judge disposes, at every write, for every proposer.** Scilla (C4), ConCert (C5), Zoe (B23) and
EUTXO (C11) all independently separate computing a proposed change from validating it; Necessity (B14) and
Robust Safety for Move (B17) show why this matters: a check that runs on every write, regardless of who
proposed it, is *robust* safety without an encapsulation proof. What Mini lacks is richness *in the judge*
and a logic for the *caller's* side. Ranked:

**1. Two-state, request-aware laws (decidable core, extended).** Add to `Pred`: relational atoms
`new[a] ≤ old[b] + k` (Move's `invariant update`, C1 — still difference logic over the doubled variable set,
so `decide_unsat_iff` extends); *request atoms* — method, invoker, capability presented, block height
(`valid_until` is already a height); and the *necessity* form `from A to B onlyIf C` (B14) as sugar for
`A(old) ∧ B(new) → C(old, request)`. "Balance decreases only if the invocation presents the owner capability"
is then one clause, and the emergent multi-step guarantee follows by induction because the kernel judges
every step. Keep Cedar's (D1) discipline: deny by default, method-indexed clauses, forbid overrides permit,
and a validator that warns on always-true/always-false clauses (Mini has the satisfiability check to do this).
This endorses the Bread scholar's "method-indexed clauses, default deny".

**2. Caller-side contracts: offers and preconditions on every invocation.** An invocation carries the
caller's own law over the outcome — Zoe's offer (give/want/exit, B23), Mina's preconditions over the read
set (C14). Admission checks the callee's law on the callee's cells *and* the caller's offer on the
caller's cells and on the Plan's transfers; failure of either refuses the turn, naming whose clause failed
(Findler–Felleisen blame, A14). Preconditions are equalities and intervals — already Pred atoms — and they
are what makes a computation done against an old snapshot *future-indexed*: a pipelined or optimistic call
is valid at admission iff its preconditions still hold (the decidable core of preoscript's certificates, F9).
This is the logic of what a promise-pipelined call may promise: "this result, *if* these read-set
predicates still hold", checked at resolution, with blame on the resolver.

**3. Authorization over the call tree (Daml rules).** Treat a Plan containing nested calls as a Daml-style
action tree (C13): a call needs the callee's controllers in the current authority context, and its
consequences are judged in the context of the *callee's* pre-authorizations (its law and signatories) plus
the controllers — never the caller's ambient authority. Delegation is non-transitive by default; passing it
on must be explicit. Biscuit scopes (D6) give the attenuation rule: a later block cannot widen what earlier
blocks granted. Drossopoulou et al.'s *protection* (B15) is the logic for what a callee may do with
capabilities it is handed: effects need capabilities, and a capability not reachable from the callee's
frame is protected for the call's duration. With re-execution, admission has the full trace, so it can
also run Grossman's **dynamic ECF check** (B16) and refuse turns whose synchronous callbacks are not
equivalent to a callback-free order unless the object's law opts in. This is what makes "rich in-turn
calls" (Ember's fork 1 steer) safe.

**4. Temporal laws by compilation to history slots.** Past-time first-order temporal laws ("close only if
opened since", "at most N withdrawals in the last 1,000 blocks", "a proposal must be at least k blocks old")
compile to kernel-maintained history slots plus a two-state law (DejaVu E6, MFOTL/VeriMon E4–E5). The kernel,
not the method, updates the slots, so code cannot forge history. Bounded-future obligations become deadlines
with default continuations (Marlowe C12, timed MPST A5): every await carries a height and a fallback, so
"funds locked forever" is impossible by construction.

**5. Protocol cells for multi-object contracts.** A multi-party workflow is an object whose state is the
residual of a global type (A1) and whose law admits a Plan action only if it advances some role's projection
(runtime monitoring of session types, decidable per step). Choral, HasChor and census polymorphism (A6–A8)
give the authoring surface; Ozone (A10) warns that out-of-order replies need protocol-position identity;
promise ownership (B10) and actor-service obligations (B9) give linear "exactly one resolver" and response
specs. Nomos's acquire/release at an equal type (A12) is the rule for several activities sharing one object.

**6. A coordination grade per clause, computed, not declared.** Endorse the Bread recommendation, grounded
in I-confluence (F1), CALM (F2) and CISE/Soteria (F3–F4): from each clause compute FREE / ESCROWABLE /
NEEDS-ORDER and the conflicting method pairs (CISE's token relation, generalising `CoordinationDial`'s
max-merge v0). lean-uwueave's catalogue (F9) is the starting table; bounded counters (F5) are the default
exit. Monotone (negation-free) clauses are checkable on partial views (CALM).

**7. Governance as decidable law refinement.** An upgrade is admissible iff (a) the new law *entails* each
frozen floor, decided as unsatisfiability of `new ∧ ¬floor` in the law fragment — Cedar's sound-and-complete
subsumption (D1, D3) is the existence proof; floors must therefore stay inside the decidable fragment; (b) the
migration is a typed lens (G6) preserving conserved totals (the Bread scholar's `migrate_conserves`); (c) the
new package's protocol is a subcontract of the old (A11); (d) tiers follow Nomic (G1): immutable-tier change
needs an explicit transmutation at a stronger threshold, nothing applies retroactively; (e) a cooling period
is just a past-time temporal law from idea 4. Upgrade authority is itself a law-governed capability
published in the package, never a bare key (G3: half of upgradeable Ethereum contracts are one key; G4:
untyped upgrades cause storage collisions). Mina's lesson (C14) is that an availability escape hatch
("the owner can always re-key") is an availability argument, not a safety argument.

**8. Two clocks: evaluate at admission, decide at authoring.** Admission evaluates a closed law on a concrete
state and needs no solver. Satisfiability, equivalence, subsumption, coordination grades and upgrade
entailment are *analysis*, done when a package or law is published. There, untrusted solvers may search
(DPLL(T) for difference logic E2, EPR solvers for relational laws E1), but Lean checks the certificates
(models, negative cycles, cvc5-style proofs E3). Grow the fragment the way Paxos-made-EPR (E1) and Cedar did:
relations and bounded quantifiers only where the result stays decidable with finite counterexamples.

**How they fit.** A method call becomes: the caller signs an invocation carrying an offer and preconditions
(2); admission re-executes, producing a Plan tree (C4/C5); it checks authorization over the tree (3), ECF for
in-turn callbacks (3), each touched cell's law including history slots and protocol position (1, 4, 5), and
the caller's offer (2); refusals name the failing leaf and the blamed party. The coordination grade (6) says
which of these checks need ordering. Package-level proofs from the certifying checker (Trillium-style
refinement, B3) are *additional* evidence, never a substitute for the per-write check — the same conclusion
the Bread scholar reached. Evolution (7) reuses the same decision procedures (8).

**Where I test the Bread recommendations.** "Laws stay the decidable judge, generated from .obend":
supported — Cedar keeps a separate, deliberately limited language for analysability, and refinement types
(E7) show how to generate the clauses; the literature argues against unifying into a general-purpose
fragment. Per-clause coordination grade: supported (F1–F4, F9). Third-party requirements: supported by
Biscuit's `trusting` blocks and Daml's multi-controller choices. Display ≤ evidence: consistent with
Zanzibar's snapshot discipline (D8) but I found no paper that states it as a rule. Upgrade gate: supported,
with one caveat the Bread note does not make — entailment is decidable only if the floors are in the
fragment. Reversibility tiers: I could not obtain Danos–Krivine (H3), so this one rests on prior
knowledge (INFERRED).

**Costs (INFERRED, in module counts).** Idea 1: Pred grows by about 4 atom families, and the difference
translation and leaf explainer must cover them. Idea 2: an invocation field and one more judged
predicate. Idea 3: an authorization judgement over Plan trees (Daml's four rules) plus an ECF checker over
the re-execution trace (a conflict/commutativity pass). Idea 4: a past-time-LTL → history-slot compiler and
a verified monitor theorem. Idea 5: a protocol-cell law and a projection function. Idea 6: extend
CoordinationDial with a conflict relation. Idea 7: an entailment check (already implied by
`decide_unsat_iff`) plus a lens type. None needs a proof system in admission.
