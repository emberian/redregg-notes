# HOLISTIC-LANG — a judgment of nanodregg's language layer against the field (2026-10-24)

The author is the whole-file reader of `~/dev/nanodregg/Lang/` minus `Lang/Proofs/`, at `f9657bd`. The defect
memo, READ-LANG.md, came first. This note judges the design; it does not repeat the defect list, except where a
defect is the architectural point. Every claim about the code is tagged READ (with a path) or INFERRED. I did
not read `Lang/Proofs/` (83 files, about 1850 `theorem` declarations by a grep count); when I say what a proof
establishes, I am relying on its name and its decision entry, and I tag that INFERRED.

---

## 1. What this layer is, in the field's terms

### 1.1 The one-line identification

Lang is a **gas-metered, first-order-data, higher-order-code object language for validated state transitions**.
A package is a typed record of methods and laws. A method returns what it intends: a new state, a fixed-arity
row of kernel calls, and a fixed-arity row of row edits. A law is a predicate on `(old, new, request)`. A guard
is a predicate on one edit. All of it runs on a small-step CEK machine that the kernel calls through one
interface, `Kernel.Receive.Program` (READ `Lang/Program.lean:562-570`).

The closest relatives are not mainstream PL. They are the ledger languages:

- **Cardano's EUTXO validators** (Chakravarty et al., "The Extended UTXO Model", 2020). Lang's laws and guards
  are validators: they never perform an effect, they judge a proposed transition and return `ok` or a named
  refusal (READ `Lang/Package.lean:68-71`, `Lang/Law.lean:27-35`). The difference is that Lang methods compute
  the proposal on the server, deterministically, so a follower re-runs it (law 2 and the charter's "admission
  is re-execution"). EUTXO has the client propose. Nano is the hybrid that Tezos and Ethereum are not: the
  proposal is computed (as in Ethereum) and then judged by per-object predicates (as in EUTXO).
- **Move** (Blackshear et al., 2019). Like Move, Lang has a module-level invariant that callers cannot bypass:
  guards and laws are kept by any layer (READ `Lang/Journey.lean:1502-1592`, the LB13 rows and their plant).
  Unlike Move, Lang has no linear types for value. Value is the kernel's, and conservation is a kernel theorem
  (`Kernel.Proofs.Value.admit_value`, cited at `Lang/StdOfferEscrow.lean:23-24`; INFERRED that it says what it
  is cited for). That is a deliberate, defensible inversion of Move's choice; see §3.
- **Calvin** (Thomson et al., SIGMOD 2012) and the Sui/Solana "declared object set" idea. A call signs its
  read set up front: pinned cells, pinned rows, signed ranges (READ `Lang/Rel.lean:253-284`; the kernel's
  `rowView` at `Kernel/Receive/Call.lean:425-436`). Lang's runtime reads only through that view
  (`receive_congr`, cited at `Lang/Program.lean:4-6`). Disjoint footprints commute, and the journey
  demonstrates it as an equality of roots (READ `Lang/Journey.lean:861-874`, LT7; `:1125-1138`, LS10). This is
  Calvin's deterministic-transaction discipline at its smallest: one sequencer.

The PL machinery underneath is classical and well chosen:

- A **definitional interpreter** in Reynolds' sense (1972), as a **CEK machine** (Felleisen and Friedman, 1986),
  with call-by-value except for suspended record fields. A field is re-evaluated at every selection, with no
  memo (READ `Lang/Eval.lean:4-8`).
- **Open recursion by an explicit knot** (`fix` over a record): the Cook (1989) and Bracha–Cook (1990) mixin
  semantics, with `mix` left to the authoring tool (READ `Lang/Term.lean:4-7`). This is the right core for
  "layers" that inherit methods but cannot override laws or guards.
- A **total, syntax-directed checker** proved equal to a declarative typing relation (READ
  `Lang/Check.lean:1-14`; the soundness and completeness proof itself is INFERRED). The type system is
  monomorphic with canonical rows; polymorphism is pushed to the authoring layer. That is the
  Elm/Michelson/Scilla trade, not the ML one.
- **Gas** with a proved per-tick work bound. A byte primitive pays one tick per 32 bytes, before it walks them
  (READ `Lang/Eval.lean:126-159`, LANG-64; the `walked_le` theorem is INFERRED). The EVM (Wood's yellow paper,
  2014) prices by opcode; Lang prices by the bytes a primitive actually touches, and states the bound as a
  theorem. That is better than the EVM, and on a par with the cost-semantics line of work on resource-aware
  languages (the RAML line of work).

### 1.2 The generators: contracts as emitted code

`Lang.Std*` is a **library of code generators**. Each Lean function emits a closed core term. Each law's
meaning is meant to be stated over a reference big-step semantics, not by evaluating the term (READ
`Lang/Std.lean:1-8`). The literature analogue is *certified program generation*: a meta-level function whose
output's meaning is a theorem of the meta level. The activity generator (cursor plus log, with guards,
`Lang/StdActivity.lean`) amounts to a **continuation table**: an asynchronous request/response protocol, made
first-order as rows, whose guard is the only arbiter of each transition. The offer generator
(`Lang/StdOffer.lean`) is Bartoletti and Zunino's contract-oriented computing (CO2, LICS 2010) at small scale.
An offer is a latent contract. "Fuse" is their fuse rule, here fired by one party. The acceptance boxes over θ
are a decidable compliance relation.

### 1.3 The contextual layer

`LiveHoles`, `HoleROM`, `StdHole`, `StdContextualHole` and `Lang/Contextual/*` implement, in their own words, contextual modal type theory
(Nanevski, Pfenning and Pientka, TOCL 2008): a hole `u :: [Ψ ⊢ A]`, closed by an explicit substitution σ (READ
`Lang/HoleDecl.lean:5-9`, `Lang/LiveHoles.lean:65-77`). The guarded holes are a truth-maintenance system. A
candidate carries its justifications as supports and hypotheses, and a withdrawn support suspends it. That is
de Kleer's ATMS (1986), which the code cites (READ `Lang/HoleROM.lean:7-10`). The executed-prefix discipline
says a hole that has been entered is not re-filled (READ `Lang/Contextual/Protocol.lean:24-26`). It echoes
Hazel's fill-and-resume (Omar et al., "Hazelnut", POPL 2017; "Live functional programming with typed holes",
ICFP 2019).

### 1.4 Where nano matches the state of the art, lags it, or has something unnamed

**It matches** on the evaluator, the checker, the gas model, the canonical type-directed data codec (READ
`Lang/Wire/Data.lean:1-17`), and the typed boundary on identifiers. A `digest` cannot be made from bytes at run
time, and every digest entering a run is checked against the World (READ `Lang/Term.lean:52-54`,
`Lang/Rel.lean:144-146`, LANG-38). That is the ocap rule "references are unforgeable" (Miller, *Robust
Composition*, 2006), enforced by typing and a boundary check rather than by a memory-safe heap. It is a clean
instance.

**It lags** in three places:

1. **Protocols.** It has the vocabulary of session types (roles, holes with "who chooses", obligations,
   affine tokens; READ `Lang/Contextual/Protocol.lean:1-39`), but no global type, no projection, and no check
   that a generated package implements its local type. The deployed offer is judged by one Lang term and by
   guards. The decisions record that nothing reads the calculus (decisions/lang.md:6444, 6481, 6491, READ).
   The field's answer for two-party contracts is multiparty session types with projection (Honda, Yoshida and
   Carbone, POPL 2008), or the generalised form (Scalas and Yoshida, POPL 2019). Nano states the shape of that
   theory beside the code and does not connect them.
2. **Specification of methods' effects.** A method's effects are data (calls and edits as fixed-arity option
   rows; READ `Lang/Package.lean:259-269`). That makes them easy to judge and hard to specify compositionally.
   The bleeding edge for "a program that emits effects which a host interprets" is Interaction Trees (Xia et
   al., POPL 2020), or algebraic effects and handlers (the Plotkin–Pretnar line of work). Interestingly, nano's
   `Contextual/Protocol.lean` builds exactly an indexed free monad with holes, and an interpreter for it (READ
   `:77-88`, `:187-215`). It uses that structure for the resident's effect program (READ
   `Lang/Contextual/NanoBridge.lean`), not for packages.
3. **Holes.** Hazel's holes are a feature of *editing*: an incomplete program still runs, with its gaps
   recorded. Nano's "live holes" are something else (§3.2).

**Unnamed in the literature, and as far as I can judge genuinely new:**

- **The law/guard split with occasions.** A law cases on *which act* is being judged: birth, write, relaw,
  adopt, or invoke of a numbered method (READ `Lang/Package.lean:53-58`). An incoming law judges the state it is
  added over (adopt, KERNEL-27). Every relaw is judged both by the laws in force and by the incoming ones. I know
  of no ledger language with first-class, typed "law replacement" judged by both the old and the new regime.
  That is a real contribution: a typed constitutional-amendment rule. The quorum generator, whose relaw arm
  needs a quorum for exactly the incoming law list (READ `Lang/Std.lean:237-254`), shows it pays off.
- **Caller-signed read views as the only window of a pure method.** This is close to Calvin's discipline and
  to Sui's object references, with the twist that a stale pin is refused *by name with the missing
  coordinates*, so a client can derive its pins from refusals (READ `Lang/Rel.lean:343-356`). As a protocol
  for read-set discovery it is neat and, as far as I know, unnamed.

**Idiosyncratic rather than novel:**

- "Live" ROM holes whose candidates are committed in the package and selected by a row. That is guarded
  dynamic dispatch with TMS-style justifications (§3.2). The CMTT framing is decoration on it.
- The fixed-arity calls and edits rows (`c0…c7`, `e0…e7`) as the way to return a list from a language with no
  lists. It works, and its bound is honest (`callsMax = 8`). But it is a workaround for having no bounded
  sequence type. A bounded list type (`List≤n T`) with a canonical codec is standard in ABIs (the
  Ethereum ABI's arrays; Michelson's lists with gas).

---

## 2. The architecture judged (seen from Lang)

### 2.1 The twelve laws

**Load-bearing and correct:**

- **Law 2 (Lean decides, Rust moves bytes)**, with the evaluator *being* the specification. This is the most
  important choice in the layer, and it is right. It removes the extraction gap that CakeML (Kumar et al.,
  POPL 2014) or CompCert (Leroy, CACM 2009) must prove away. The trusted base is the Lean compiler on one
  total program. The cost is that the "spec" and the "implementation" are the same text, so the theorems must
  relate it to a *second*, independent semantics. Lang has one: `BigStep`, with the method-meaning and law-meaning
  theorems over it (INFERRED from `Lang/Std.lean:7-8`, `Lang/Law.lean:9`). That is the right structure: a
  definitional interpreter, plus a reference relational semantics, plus an adequacy theorem between them.
- **Law 4 (TigerStyle bounds)** in Lang means total functions, named faults, gas, a stack bound held at a
  consensus constant, and fuel-independence of outcomes (READ `Lang/Eval.lean:243-253`, `Lang/Bounds.lean`).
  That is exactly what makes re-execution consensus-safe. Without `run_agree` (fuel-independence, INFERRED
  from `Lang/Bounds.lean:40-43`), followers with different budgets could disagree. This law is doing real work.
- **Law 3 (bytes end to end) and the one data codec.** Type-directed, one tag byte per sum, big-endian
  naturals so that a key's bytes order like its values (READ `Lang/Wire/Data.lean:1-11`,
  `Lang/Rel.lean:51-67`). It is canonical by construction, and the canonicity is a theorem of the combinators
  (INFERRED). This is state of the art for consensus codecs (compare the SSZ and Borsh designs, which get
  canonicity by convention).
- **Law 6 (named theorems; one axiom census).** Sound, and better than per-theorem `#print axioms` lines.

**Aspirational, meaning stated but not what Lang's code does:**

- **Law 1 (one of everything).** It is violated structurally in Lang's most central file. `Program` keeps a
  closed twin of every loader, setup, run and judge "for its landed statements" (READ
  `Lang/Program.lean:154-161, 348-361, 454-457, 512-524`), and the twins disagree on contextual imports
  (READ-LANG F-1, measured). The law is right; the practice of keeping old shapes alive for their theorems is
  exactly what the law exists to kill. It is also the main way this repository accumulates (§4).
- **Law 7 (refusals by name).** In Lang, most refusals are `Refusal.program String` with free text (READ
  `Lang/Program.lean` throughout; `Lang/Rel.lean:150`). The journey then recovers names by substring (READ
  `Lang/Journey.lean:550-553`). Kernel refusals are constructors; Lang's are mostly strings. The law is stated
  for the system and kept by half of it.
- **Law 4's "assertion where a premise enters".** It is honoured at the World boundary (digests, decoded
  bytes, the request's bounds; READ `Lang/Program.lean:301-310`). Inside total Lean it degenerates into
  unreachable re-checks (READ `Lang/LiveHoles.lean:281-287`). The charter itself says this
  ("inside a total Lean definition an invariant assertion only re-checks the compiler").

**Wrong-headed, or at least the wrong default:**

- **Law 8 (the definition/proof split by file)** is a build-system workaround raised to a law. Mathlib does not
  do this; Lean's module system is meant to. As a law it costs a module per theorem file and a naming scheme.
  It is defensible as a measured local fix (GATES-2), not as architecture. I would keep it as a gate and drop
  it from the laws.
- **Law 10 (examine every decision, then critique and meta-critique it).** As practised, `decisions/lang.md`
  is 6,906 lines of landing logs (READ: its LANG-75.x and LANG-77 entries are mostly plant lists, prices and
  hash references). The original intent, a design record, is good. But the critiques are written by the lane
  that landed the change, and the file works as a journal, not a specification. The field's equivalent is the
  design rationale beside a *spec*. Nano has the rationale and no spec to sit beside (§2.4).

### 2.2 The layer cuts, seen from Lang

- **Kernel ↔ Lang, through `Receive.Program`** (`checkInstall`, `judge`, `run`, `rels`): an excellent cut.
  The kernel is parametric in a language. The kernel's admission theorems do not depend on Lang's internals,
  and a plant program can be dropped in for testing (READ `Lang/Journey.lean:408-523`: `skipJudge`,
  `eraseOccasion`, `dropCalls`, `foreignRow` are all `Program` instances). This is the same move as seL4's
  separation of an abstract specification from a capability-checked executive, at the right scale.
- **Lang ↔ Protocol, through `ReceiptCheck`**, where Lang declares the check and Protocol instantiates it (READ
  `Lang/Rel.lean:130-136`): correct dependency inversion, done honestly.
- **Lang ↔ Hosting: a wrong cut.** `Lang/Contextual/NanoBridge.lean` imports `Hosting.Resident.Trace` (READ
  `:16`), so a Lang definition module depends on the layer that should depend on it. It exists only to state
  the resident's effect program as an instance of Lang's protocol calculus. The calculus belongs to neither
  layer. It is a research artefact and should live in a research directory, depending on both.
- **A missing cut: Lang mixes the language with its standard library and its theory.** `Lang/` holds the core
  (Term/Ty/Check/Eval/Data/Wire), the runtime adapter (Program/Rel/Call), the generators (Std*), the authoring
  surface (Surface/Read/Print), the contextual runtime (LiveHoles/HoleROM), the contextual theory
  (Contextual/*), the conformance journeys and the measurement tooling (Sim/Need) (READ, from the directory
  listing). A language with a library and an application tier usually separates `core`, `runtime` and `std`.
  The absence of that cut is why a change to a generator can sit in the same commit as a change to the
  language, and why LANG-77 needed "one `lang!` for the language, one `lang:` for its consumer"
  (decisions/lang.md:6749-6750, READ).

### 2.3 One writer, receipts between Worlds, no agreement engine

For Lang, the right call. A pure language over a caller-signed view needs no concurrency control beyond the
pins. The one writer gives a total order, and followers re-derive. This is state-machine replication
(Schneider, 1990) with the replication factor set to one and the replicas made into auditors. Receipts between
Worlds, checked against a head held in the reader's World (READ `Lang/StdHead.lean`, `Lang/Rel.lean:181-206`),
are the trust structure of IBC-style light clients, with the cryptographic proof replaced by a posted head that
a member vouches for. Nano says so, and that honesty is the right posture. The only Lang-level cost is that
`Std.head`'s law cannot distinguish an honest head from a lie (READ `Lang/StdHead.lean:11-17`): the law orders
heads and freezes on forks, and that is all it can do without proofs. The design is a deferral only if a
second writer is ever wanted. For the charter's scope it is a decision, not a deferral.

### 2.4 The verification method: plants, census, journeys

**What "every theorem has a plant that turns it red" is, in the field's terms.** It is *mutation analysis
applied to specifications* (DeMillo, Lipton and Sayward, 1978), and in particular a form of *vacuity
detection* (Beer, Ben-David, Eisner and Rodeh, CAV 1997, and the Kupferman–Vardi line of work after it). A
theorem that no plausible mutation of the code falsifies says nothing about the code. That is a real and
under-practised discipline in mechanised verification, and nano deserves credit for making it routine. The
minted lessons about vacuous disjuncts and premises provable from the hypotheses are what that discipline
finds.

**Where it is hollow.** A plant demonstrates that *one* mutation turns *one* theorem red. It does not
demonstrate that the theorems, together, pin down the behaviour. It cannot replace a statement of what the
system must do. CompCert's trust comes from one theorem, semantic preservation, whose statement anyone can
read. seL4's comes from a refinement between an abstract specification and the C. IronFleet (Hawblitzel et al.,
SOSP 2015) and Verdi (Wilcox et al., PLDI 2015) state a refinement to a distributed-system specification plus
liveness. In each, the *statement* is small and the proof is large. Nano has inverted this: the statements are
many and local (about 1850 in Lang's proofs alone by my count, INFERRED), there is no top statement, and the
plants are the evidence that each local statement is not vacuous. A mechanised-metatheory practitioner would
say:

- **Lang has most of a top statement and does not state it.** Its ingredients exist, judging from the module
  and theorem names: checker ⇔ typing, the machine's preservation and progress, run ⇔ BigStep,
  fuel-independence, law meaning, method meaning, and `callsOf`/`editsOf` read back exactly what the method
  returned (INFERRED from `Lang/Proofs/` file names and the citations in the definitions). The missing
  sentence is: *for every installed package `P` and every admitted invoke, the Turn's state, calls and edits
  are the BigStep denotation of `P.method` on the pinned view, and every law and guard of `P` denotes `ok` on
  it.* That is a one-page statement over a reference semantics that a reader can audit. It would make the
  1850 theorems lemmas of something. Today they are a field of facts whose union nobody has stated.
- **Should a system-level refinement exist?** For nano as a whole, the honest spec is a deterministic state
  machine whose transition is `World.admit ∘ receive`. Its *meaning* for users is the journey rows. The rows
  are executable acceptance tests (READ `Lang/Journey.lean:1-97`), not a specification: they demonstrate
  instances. A refinement from the kernel to an abstract "ledger of objects with laws" spec, in the style of
  Interaction Trees, is a year of work and is not what this project is for. The Lang-level adequacy theorem
  above is a week or two and *is*.
- **The journeys judge by string.** Many conformance rows match a prefix or a substring of the rendered
  verdict (READ `Lang/Journey.lean:550-553`, and the list in READ-LANG F-4). A conformance suite whose
  oracle is `splitOn` is weaker than a typed oracle. That is a direct consequence of the string-typed half of
  law 7.

---

## 3. The details judged

### 3.1 Three choices I would defend at a top venue

**(a) A metered definitional interpreter as the consensus semantics, with a proved cost model.** One total CEK
machine, one tick per transition, byte primitives charged per word *before* they walk (READ
`Lang/Eval.lean:126-159`). Outcomes are independent of extra fuel, and every way a run ends has a name (READ
`Lang/Eval.lean:75-92`). Extraction is metered under the same budget, so a lazy field that diverges exhausts the
budget instead of hanging (READ `Lang/Data.lean:1-8, 44-60`). Against the EVM's opcode table, which is priced by
convention and repriced by hard fork, this is principled. Against resource-aware type systems it is simpler
and fully dynamic. A paper: "a consensus language whose gas is a theorem". The `walked_le` statement (work per
charged tick is bounded) is the result, and it is a good one.

**(b) Laws as typed, occasion-indexed transition predicates, including law replacement, with layers that can
never override them.** A law sees `(old, new, req)` and `req.occasion` names the act; adoption makes an incoming
law judge the state it is added over (READ `Lang/Std.lean:107-125`, `Lang/Package.lean:53-58`). A layer inherits
methods by open recursion and cannot shadow a law or a guard (READ `Lang/Journey.lean:754-756`, the
`overridesLaw` refusal; LB13 at `:1563-1583`). This is EUTXO's validator discipline extended with typed
amendment and mixin inheritance. The quorum generator, with a relaw arm that needs a quorum for exactly the
incoming law ids (READ `Lang/Std.lean:251-252`), is a compelling example. I know of no published ledger
language with this combination.

**(c) The caller-signed read view, plus "refusals carry the missing coordinates".** A method sees only rows the
caller pinned and ranges the caller signed (READ `Lang/Rel.lean:256-274`). An upsert or retract of an unpinned
row is refused `rowUnpinned` *with its parent, relation and key* before any guard runs (READ
`Lang/Rel.lean:343-356`), and the kernel re-checks every pin against the World before the Turn. Determinism,
replayability and commutation of disjoint footprints follow, and the journey checks them as root equalities.
As a design for "pure contracts with discoverable read sets" it beats Ethereum's access lists (optional and
advisory) and matches Sui's object model in rigour, with less machinery.

### 3.2 Three choices I would be embarrassed to present

**(i) The contextual apparatus: CMTT vocabulary over guarded dynamic dispatch, plus a calculus no deployed code
reads.**

What the deployed live hole *is* (READ `Lang/LiveHoles.lean:206-219`, `Lang/HoleROM.lean:34-44`): a finite
list of candidate closures committed in the package, an index stored in a row, per-candidate supports (rows at
versions, or live cells), per-position hypotheses that may be strengthened away, and a guard over one pin. At
each invocation, one candidate is selected, re-justified and spliced in. In field terms that is **dynamic
dispatch through a vtable whose slot is chosen by a row, with ATMS-style justification checks**. It is a good
mechanism for "policy chosen at run time from a fixed menu". But:

- The CMTT framing (meta-variables, explicit substitutions, a weakening/strengthening factor and a re-embedding;
  READ `Lang/LiveHoles.lean:186-196`) does work that ordinary closure application would do. A candidate is
  type-checked once at its context and then *substituted into the package body* on every invocation (READ
  `:272-287`). Then the whole package is type-checked again, and again in the loader (READ-LANG F-13). In
  Hazel, typed holes buy *incremental editing*. Here nothing is edited after install; the candidates are ROM.
- The theory module (`Lang/Contextual/Protocol.lean`, 628 lines, with the toy instances Coin and Negotiation)
  has, by the decisions' own repeated admission, no deployed consumer (decisions/lang.md:6444, 6481, 6491, READ).
  The "promotion program" (LANG-75.x) has largely landed *docstrings* where theorems were planned (READ
  LANG-75.2, 75.4, 75.7, 75.8, 75.17 titles). That is honest bookkeeping, and it is also the signature of a
  theory looking for a reader.

*What a strong PhD student would build instead:* a `select` construct in the core, `select r [c₀,…,cₙ]`. The
cᵢ are closed terms of one type, checked at install; `r` is a pinned row holding an index; each cᵢ carries a
declared support set that the runtime checks against the view. That is the deployed behaviour, as one
typing rule and one machine step, with no substitution, no re-check and no hole names on the wire. It is a
**week**, including restating the selection theorems. If the project wants the CMTT story, the honest version
is Hazel's: holes as first-class *during authoring*, with the resident's editor as the client. That is a
**year**, and it is a different product.

**(ii) Refusals as strings, and a conformance oracle that greps them.** Most of Lang's refusals are
`Refusal.program s!"…"` (READ throughout `Lang/Program.lean`, `Lang/Rel.lean`, `Lang/Call.lean`). The
journey's oracle is `startsWith` and `splitOn` (READ `Lang/Journey.lean:550-553`). The code's own reasoning
shows why this matters: clients derive pins from refusals (READ `Lang/Rel.lean:345-347`), so a refusal name is
part of the protocol. The minted lesson "refusal renders as the expected verdict" recurs in Lang's hole
coverage (READ-LANG F-2). The field's answer is boring and decisive: a typed error inductive
(`LangRefusal`, with constructors carrying their coordinates), rendered by one printer, compared structurally
in tests. Kernel's `Refusal` already does this (READ `Lang/Journey.lean:568`, where it renders through
`Sim.nameOf`). *Cost:* a **week**. It touches every `throw (.program …)` site, the journey's helpers, and the
decls price.

**(iii) Generators that emit hand-indexed de Bruijn terms, with their correctness in comments.** `StdActivity`,
`StdOffer`, `StdOfferEscrow` and `StdHead` build core terms with raw `.var n`, each carrying a comment such as
"var 0 req, var 1 arg, var 2 state, var 3 rows" (READ `Lang/StdActivity.lean:104,117,197,225,229`;
`Lang/StdOffer.lean:127,198,224`). I checked every one and they are right. But "a human counted the binders" is
not a method, and the project already has the tool that removes it: `HoleSyntax`, a named-variable
construction (READ `Lang/HoleSyntax.lean:6-33`), used by `StdHole` and not by the others. In the field, emitted
object code is either intrinsically typed (well-typed by construction, the "typed tagless final" and
intrinsically-typed-syntax line of work) or built with higher-order abstract syntax. The generators do get
re-checked by `checkWith` at generation (READ `Lang/StdOffer.lean:308`), so an index error that changes the
type is caught. One that picks a wrong variable *of the same type* is not. My PT3 measurement in READ-LANG
(F-7) is exactly that class: `keys` and `theta` coincide in type at `theta = [a, b]`. *What to build:* move
every generator onto `HoleSyntax` (or a small typed HOAS front end) and make variables named. That is a
**week** for the four generators, with no byte change if the elaboration matches.

**A fourth, which is architectural rather than embarrassing: the two-party protocol has no notion of the
caller.** `Req` carries the signer, the grant's root issuer, the object and the window, but not the calling
object (READ `Kernel/Receive/Call.lean:439-440`). So `take` cannot tell its peer's nested call from anyone
holding `[invoke take]` (READ `Lang/StdOffer.lean:24-26`; LANG-77's meta-critique is about exactly this). In
object-capability terms, a nested call should arrive through a *facet* that names its sender (Miller 2006); in
session-type terms, the role should be part of the message. A `caller : opt digest` field in `Req` is a week,
and it would let `take` refuse anyone but its peer. That turns "one session row is not a fuse" into "one session
row is a fuse".

---

## 4. What to do

### 4.1 The one structural change: one loader, one setup, one install check

Make `Lang.program`'s three entry points share exactly one per-package admission function, and delete the
closed twins (`load`, `loadAll`, `admitPackage` as a separate path, `runSetup`, `runMeasured`, `runMethod`,
`judgeOne`, `judge`, `checkInstall`; READ `Lang/Program.lean`). Every package in a closure, root or import, is
admitted by one function that decides, *per package*, whether it has holes. The theorems now stated on the
closed path become statements of the live path under a "this closure has no holes" premise. That premise
already exists as `LiveClosed`'s bridge (READ, partially, `Lang/Proofs/LiveClosed.lean:120-200`).

What it would make true:

1. Install loads exactly the closure a run loads. That is the claim of the module's own header and of
   LANG-35, and it is false today for contextual imports (READ-LANG F-1).
2. THE BAR's denominator and the journey's measure become one function (READ-LANG F-6).
3. Law 1 holds in the most central file of the layer, and the `Program` file loses roughly a third of its
   definitions (INFERRED from the line ranges above).
4. Every Lang theorem speaks of the deployed path directly, not through a bridge.

Cost: the restatement the decls judge will price, perhaps a few dozen RESTATES-MEANING, by analogy with LANG-77's
55 (INFERRED), and one `lang!`. No wire byte moves. This is the highest truth-per-cost change I can see,
because it repairs a *false sentence about the system*, not a missing feature.

The runner-up, nearly as cheap, is the typed `LangRefusal` (§3.2 ii). Do it in the same quarter.

### 4.2 The one thing to stop doing: landing theory that nothing deployed reads

Stop adding to `Lang/Contextual/` and to the promotion cards whose outcome is a docstring. The pattern is a
theory module with its own types (`Prot`, `Iface`, `Hist`), toy instances, theorems, and then a card that
"promotes" it and lands as a docstring saying nothing reads it (decisions/lang.md LANG-75.2, 75.4, 75.7, 75.8,
75.17, READ titles). Each cycle costs reads, decisions and gate time, and the deployed language does not move.
Either connect the calculus to packages, where a generated package's guards are *derived from* a protocol
type and a theorem says so (that is the year-long version of §3.2's fourth point), or move it to a research
directory outside the build of the system. The project's own lesson "iterate inside the substrate" says the
same.

### 4.3 Grade

**B overall. A− for the runtime core, C for the contextual layer, B for the generators.**

The core earns its grade with a definitional, metered, total interpreter that is the consensus semantics, a
proved cost model, a canonical codec, typed unforgeable identifiers and occasion-indexed laws. Each is at or
past the state of the art for ledger languages, and the combination is original. The layer is held back by
three things. It keeps twins of its own central path, against its first law. It speaks the language of session
types and contextual modal type theory without implementing either where it runs. And it has no top-level
adequacy theorem. Its ~1850 local facts are guarded against vacuity one at a time by plants, but no single
sentence states what they add up to.
