# HOLISTIC-LANGPROOFS — a judgment of nanodregg's Lang proof layer against the field (2026-10-24)

Reader: the same subopus that wrote `READ-LANGPROOFS.md` yesterday, at origin/main f9657bd. This is
a judgment, not a review. Claims about nano's code are tagged READ (path) or INFERRED. References
I give a year for I am confident of. Where I am not, I name the line of work instead.

Scope: `Lang/Proofs/**`, about 2,000 `theorem` declarations (MEASURED, `git grep -c "^theorem\|^private
theorem"`). These are the theorems over the Lang runtime (`Lang.program`, the machine, extraction,
the reads, the guards) and over the generators (`Std.activity`, `Std.hole`, `Std.offer`,
`Std.offerEscrow`, `Std.head`, the Bell). I also judge the verification method as it is practised
in this layer: the judge, the plants, the census, and the decision entries with their critiques.

---

## 1. What this layer is, in the field's terms

### The design it instantiates

Lang is a small, typed, strict functional object language. A *package* is a record of method terms,
guard terms and law terms over typed state and typed relations (READ `Lang/StdOffer.lean`
`offerPackageOf`; `Lang/Bell.lean`). The runtime has several parts:

* a fuel-bounded abstract machine (`run S.lib Bounds.stackMax fuel …`, READ `Lang/Program.lean:497`);
* an extraction of the machine's value into first-order data at the method's result type;
* a decode of that data into kernel `Body`s and row edits (`callsOf`, `editsOf`);
* the relation guards run over every edit (`guardEdits`, `Program.lean:506`).

The kernel sees Lang only through an abstract `Program` interface: `run`, `judge`, `checkInstall`,
`rels` (READ `Kernel/Receive/Derive.lean:110-230`).

In the field's terms the layer is three things stacked:

1. **A clocked operational semantics with an adequacy theorem to a big-step meaning.**
   `run_bigStep` and `Extract.runMeasured_means` (READ, used throughout `StdOffer.lean`) carry a
   machine run that returned to a `BigStep` derivation and a `Means` judgment. This is the
   CakeML-era "functional big-step semantics with a clock" idea (Owens, Myreen, Kumar, Tan, ESOP
   2016), used for adequacy rather than for compiler correctness. Divergence and fuel exhaustion
   collapse into one named refusal (LANG-75.13). That is exactly what a clocked semantics buys, and
   nano says it out loud.
2. **A capability-style, declared-footprint runtime.** A method's type spells every read it makes:
   its point and range slots, the `(live)` and `(receipt)` columns, the declared peer read
   (`rowsTy`, `methodReads`). The kernel pins every read cell and row (READ `Lang/Program.lean`
   `methodReads`, `PeerRead.lean`). Footprints are declared in types, as Move's `acquires`
   annotations declare resources (Blackshear et al., the Move language of the Libra/Diem line,
   2019). Reads are authenticated against signed pins, as in authenticated data structures
   (Tamassia's line of work). The receiver checks each edit with a guard term that is itself
   package code. That is Schneider's execution-monitoring enforcement (Schneider, "Enforceable
   Security Policies", TISSEC 2000), and LANG-75.9 names it correctly: "the receiver is the
   monitor".
3. **A catalogue of generator-specific run-soundness theorems.** For each generated package the
   layer proves what a returned run of each method did:
   * `take_run_sound`, `fuse_run_sound`, `escrow_*_run_sound`;
   * `answer_run` for the Bell;
   * `activity_program_safe` for activity logs;
   * `selectHole_*` for holes.

   It then lifts some of these to the admitted Turn (`fuse_atomic`, `invitation_once`,
   `escrow_fuse_admitted`, `answer_commits`) by walking the kernel's own record of the call tree
   (`Dispatched`, READ `DispatchRows.lean`).

Beside these sits `Lang/Proofs/Contextual/*`, a session-type-flavoured calculus of open protocols:
`HasProt`, `Fills`, `SubstOK`, the `Chooser`, `hasProt_reach`, `at_most_once`. It has no deployed
consumer (LANG-75.17, measured there; INFERRED still true, since nothing outside `Contextual`
imports it).

### Closest literature, and where nano sits relative to it

**Verified systems (seL4, Klein et al., SOSP 2009; CertiKOS, Gu et al., POPL 2015; CompCert, Leroy,
CACM 2009; IronFleet, Hawblitzel et al., SOSP 2015; Verdi, Wilcox et al., PLDI 2015).** These
systems put trust in ONE top-level refinement theorem: the implementation refines an abstract
specification, plus invariant proofs over that specification. Nano's Lang layer has no abstract
specification of a package. The nearest thing is the `BigStep` meaning. "The machine refines
BigStep" is proved (adequacy), but "this package's BigStep meaning satisfies this package's
specification" is replaced by one bespoke existential per method. On specification architecture
the layer is behind the state of the art. On the honesty of the base it is level with it: the
machine-to-meaning adequacy is real, no axioms (MEASURED: no `sorry` or `native_decide` in the
layer).

**Interaction Trees (Xia et al., POPL 2020).** A Lang method is a pure function from (state, args,
rows) to (state', calls, edits). Its "effects" are first-order data that the runtime interprets
later. That is a defunctionalised, one-shot ITree: one round of output events, no response
continuation within a Turn. LANG-75.12 records the continuation being defunctionalised into the
activity's `captured` column. This is the right model for a deterministic replicated object
(Calvin's determinism, Thomson et al., SIGMOD 2012, is the analogue at the database layer). It
avoids all the coinduction ITrees need, at the price of no in-Turn interaction. That price is a
good one for nano.

**Session types and contracts.** The literature splits into two lines:
* Honda 1993; Honda, Vasconcelos, Kubo, ESOP 1998; multiparty, Honda–Yoshida–Carbone, POPL 2008;
  generalised, Scalas–Yoshida, POPL 2019;
* contract compliance: Castagna, Gesbert, Padovani, "A theory of contracts for Web services", 2009;
  Bartoletti and Zunino's contract-oriented computing line.

`Std.offer` borrows Bartoletti's Fuse rule by name (READ `Lang/StdOffer.lean` header). It is much
weaker than compliance: two offers "comply" when their roles differ and a numeric θ sits inside
both boxes. Compliance in the literature is a relation between BEHAVIOURS, "whatever you do, I can
answer". The offer has no behaviour. It has one atomic swap, Herlihy's atomic cross-chain swap
(PODC 2018) reduced to one World, where atomicity is free (KERNEL-45: the call tree commits or
fails whole). The Contextual calculus does have a real `HasProt` judgment with an affine token
account and a subject-reduction theorem (`hasProt_reach`). That is a recognisable session-type
metatheory fragment, but it judges nothing the system runs. Nomos (Das, Balzer, Hoffmann,
Pfenning, et al., resource-aware session types for digital contracts, around 2019–2021) is the
closest real thing to what the offer/escrow pair is reaching for. Nomos types the contract's
protocol AND its linear assets in one discipline. Nano splits them: assets are linear in the
kernel (`admit_value`); protocol is a per-key row-guard machine. The split is defensible (law 1:
value has one owner). But the protocol half is a monitor, not a type, so no statement ever says
"the escrow's two parties follow the protocol". It says "each edit was a legal step".

**Contextual modal type theory and typed holes.** The CMTT lineage is Nanevski, Pfenning, Pientka,
TOCL 2008; typed holes are Hazel (Omar et al., POPL 2017 Hazelnut; POPL 2019, live functional
programming with typed holes). `Std.hole` and the ROM `selectHole` are a runtime CMTT. A hole has
a typed signature (`holeSignature`). A candidate filling is selected at run time against live
supports. The strengthening factor `selectHole_factor` re-types the filling in the context minus
dead hypotheses, which is the strengthening/weakening lemma of CMTT made operational. This is the
most genuinely novel thing the layer has: a CMTT meta-variable whose instantiation is chosen per
Turn from an authenticated row and gated on the liveness of kernel cells. I do not know a name in
the literature for "holes whose fillings are justified by revocable capability facts". Hazel's
holes are an editor's. Nano's are a running system's, with provenance (`selectHole_origin`) and
revocation (`revoked_support_refused`). It is closest in spirit to truth-maintenance systems (de
Kleer's ATMS, Doyle's TMS). LANG-75.3 deleted the label theory that would have made that link
precise.

**Proof-carrying authorization (Appel–Felten, CCS 1999; PCFS, Garg and Pfenning's line; Nexus,
Sirer et al., SOSP 2011).** Nano rules proof systems out of scope (CHARTER scope item 1). Admission
is re-execution. So "authorization logic" here means the kernel's grant walk plus the method's
own guard. The supports of a hole are the closest thing to PCA's credentials. They are posted
claims, checked for liveness at read time (`cellLive`). This is the macaroon/biscuit trade
(Birgisson et al., NDSS 2014) — a verifier re-checks the conditions — not PCA's "verifier checks a
proof".

**Mechanised metatheory practice (Mathlib, Iris (Jung et al., POPL 2015 and the JFP 2018 journal
version), CompCert, CakeML (Kumar et al., POPL 2014)).** At scale, practitioners build a program
logic once (Iris's weakest preconditions, CompCert's simulation diagrams, CakeML's characteristic
formulae, Guéneau, Myreen and Kumar's line) and prove clients against it. Nano's Lang layer has
no program logic. Every generator theorem inverts a `BigStep` derivation by hand, case arm by case
arm, through environment abbreviations like `fuseOkEnv` (READ `StdOfferFuse.lean:130-136`). Here
the layer is furthest behind (§3).

**Vacuity and mutation analysis.**
* Vacuity: Beer, Ben-David, Eisner, Rodeh, CAV 1997; Kupferman and Vardi, 1999 and after.
* Proof-mutation tools: mCoq, Celik et al., ASE 2019.

The plant discipline (every theorem has a deployed mutation that reds it) is exactly vacuity
detection plus mutation analysis applied to proofs. That is a genuine and under-used idea in
proof engineering, and nano practises it more systematically than most verified projects I know.
It is also not a specification-adequacy check (§2).

### Matches, lags, and unnamed things — summary

* **Matches the state of the art:**
  * clocked semantics with adequacy;
  * declared, authenticated read footprints;
  * monitor-as-guard enforcement;
  * canonical-codec data refinement used as a proof device (one θ by `decodeData_eq_ok_iff`,
    READ `StdOfferFuse.lean:699`);
  * a zero-axiom proof base.
* **Behind it:**
  * no specification layer and no program logic;
  * no completeness direction at the run grain (the decisions say so: no machine completeness at
    `stackMax`);
  * contracts without behaviours;
  * a protocol calculus with no consumer.
* **Unnamed and novel:** runtime CMTT with revocable, live-checked supports. Also, mildly, "the
  receiver is the monitor" stated as a theorem over arbitrary hand-written methods given only the
  guard (`activity_monitor_safe`'s premises are on the package's guard, not its methods). That is
  a neat local-reasoning result: the property holds for code nobody has read.
* **Unnamed and idiosyncratic:** the `*_core` lemma pattern. These lemmas take the generator's own
  field as a hypothesis so that a plant reds a named theorem (LANG-75.21 calls it "a device for
  observing plants"). This is proof structure bent to serve the observation ritual. It has no
  counterpart in the field, for good reason.

---

## 2. The architecture judged (from where this layer stands)

### The laws, as a design

**Load-bearing and right:**

* **Law 2 (Lean decides, Rust moves bytes)** is what makes this layer's theorems about the
  deployed system at all. Every theorem I read is over `Lang.program` itself, the function the
  kernel calls (READ: `take_run_sound`'s premise `h : (Lang.program …).run … = .ok …`). This is
  the CakeML/CompCert "the verified artefact IS the artefact" stance, without extraction. Lean's
  compiled code is the deployed code. The trust base is Lean's compiler, which the census records.
  This is the strongest architectural decision in the charter, and it is correct.
* **Law 3 (bytes end to end, canonical decoders)** paid off directly in this layer. LANG-77's
  one-θ result is a corollary of canonicity, not a separate protocol argument. When the codec is
  a bijection on its image, "both parties saw one value" is free.
* **Law 7 (refusals by name)** gives the theorems their shape. Every refusal arm is a constructor
  with a name, so each refusal theorem (`take_offerNotNamed` …) is a closed statement about one
  arm. It also yields the per-arm plants.
* **Law 4's fuel** (total definitions, a static bound) is what makes the clocked semantics
  possible.

**Aspirational (stated, not what the code does):**

* **Law 1 (one of everything)** is broken in the proof layer itself. Yesterday's memo lists three
  copies of `conforms_opt` and the hand restatement of the Bell in `Lang/Bell.lean` (READ). More
  importantly, there are two shapes of one fact at the architectural level: the Contextual
  calculus's `HasProt`/`Fills` notion of a protocol versus the row-guard `WaitingStep` machine.
  Both claim to be "the protocol of an activity". Only one is consumed.
* **Law 6's second half ("every theorem statement is read by a second agent before it lands")**
  is not what happens. Since R-0069 the cards say "method R-0069: no IMPACT, no read, built and
  planted, fast judge" (READ decisions/lang.md LANG-75.15 onward). The two statement defects
  yesterday's memo calls DEFECT (the unbound cell `g` in `posted_support_checked`; the escrow's
  `EscrowLegMoved` with no "receives") both passed because no adversarial statement reader was in
  the loop. The plant is a substitute for that reader. It cannot be one (below).
* **Law 10 (decisions with critique and meta-critique)** is practised with real candour: the
  critiques name their own gaps. But decision entries are append-only, and nothing marks an entry
  superseded (LANG-77's `hne`, LANG-75.21's "fuse has no row acts"). The decisions file is a
  journal, not a specification. A reader six weeks out must replay it.

**Wrong-headed in light of the field:**

* **Law 8 ("a module exports definitions OR proofs")** is a build-time optimisation promoted to a
  law (GATES-2 measured the rebuild cost). It forces specification Props such as `JointOk`,
  `NamedKey`, `WaitingStep` and `EscrowLegMoved` to live in proof modules. Those are the
  SPECIFICATIONS. They belong beside the definitions they specify, in a module a client imports
  without importing proofs. The law conflates "proof" with "statement". Every mature verified
  development (seL4's abstract spec, CompCert's `Csem`) separates spec / impl / proof, not
  def / proof. Nano has no spec tier because the law gives it nowhere to go.

### The cuts this layer touches

* **The Kernel/Lang cut (`Program` abstract to the kernel) is the right cut.** It is CertiKOS's
  layer interface in miniature: the kernel is proved once, parametrically in `Program`, and Lang
  instantiates it. The design pays for it in exactly one place, and pays too much there. Every
  Turn-grain theorem about a Lang package re-derives the kernel's call walk from the outside:
  `DispatchRows.lean` is a whole module of kernel facts proved in Lang (READ its header), and
  `fuse_tree` / `escrow_party` each walk `Dispatched` by hand. What is missing is a GENERIC lift:
  "if every dispatched run of package P satisfies run-spec S, then every admitted Turn satisfies
  Turn-spec lift(S)". It would be one theorem in the shared interface. Instead each generator
  pays roughly 100 lines to re-walk the tree.
* **A missing cut: specification.** As above. There is no tier where "what `Std.offer` is
  supposed to do" is written once, independently of its terms. That is why the escrow's statement
  could omit what a party receives and nobody's checker noticed: there was no spec to compare the
  theorem to, only the code it was derived from.
* **Single writer + receipts between Worlds + no agreement engine.** From the Lang side this is
  correct, not a deferral. A deterministic single writer makes every Lang theorem a statement
  about a pure function of the pre-state. Followers re-derive, so a theorem about `Lang.program`
  is a theorem about every replica. This is Calvin's insight. Receipts (`receipt_*_authenticated`)
  are light-client verification against a held head. The Lang half says only "what the check
  showed entered as data" (LANG-75.14 critique), which is the right modesty. The design defers
  nothing Lang needs. The one cross-World thing a contract would want, an atomic cross-World swap,
  is ruled out by charter, and Herlihy-style hashed-timelock swaps would be the honest substitute
  if it is ever wanted.

### The verification method: plants, judge, census

**"Every theorem has a plant that reds it."** As a discipline this is sound in one direction and
hollow in the other.

* **Sound:** it is vacuity detection. A theorem no deployed mutation can falsify is either a
  tautology or about the wrong object. The project has been burned by exactly that before (the
  memory index's "61 landed binding theorems bound nothing"; `P ∨ Collision` with an unbounded
  existential). Model checking learned the same lesson (Beer et al., 1997) and built tools for it.
  mCoq showed mutation analysis finds weak Coq specifications in practice. Nano does this by hand,
  per card, and writes the result down. That is better than most verified systems do.
* **Hollow:** a plant shows the theorem DEPENDS on the code. It cannot show the theorem is the
  RIGHT statement. Three observations from this layer:
  1. The escrow's run-grain theorems all red under P8d/P8e/P8f/P8g (LANG-75.21). Every plant is
     green on the property nobody stated: what a party receives. The plant set is chosen by the
     author of the statement, so it inherits the statement's blind spot. The memory index already
     names this ("every instrument blind to the next wound").
  2. Observed reds are often in private helpers, or blocked in an unbuilt cone, not refutations of
     the named statement (LANG-75.20's own meta-critique: "a downstream theorem built on a red
     lemma does not red"). The `*_core` device exists to make reds land on names. That optimises
     the observation, not the specification.
  3. Some plants mutate definitions only the theorem reads (`Peer.reliable`, READ
     `Lang/Contextual/NanoBridge.lean:83`). A tooth of a table is not a tooth of the system.

How CompCert/seL4/IronFleet establish trust instead: one specification, written to be read by
humans and small (seL4's abstract spec; IronFleet's high-level state machine; CompCert's source
semantics), and one refinement theorem whose STATEMENT is short and reviewed by people who did not
write the proofs. Trust then reduces to "is the spec right", which is a review problem the size of
the spec. In nano trust is "are these ~2,000 statements each right", a review problem the size of
the catalogue, and law 6's reader has been removed.

**Is there a top-level correctness statement?** Not in this layer. The nearest are
`activity_program_safe` (one safety property, all methods, given the guard) and the adequacy chain
`run → BigStep → Means`. `Census/Refines.lean` (READ header) is data refinement for codecs, not
system refinement. Should one exist? For Lang, yes, and it is within reach. A package spec is a
relation `Spec P : (state, args, rows) → (state', calls, edits) → Prop` per method. The top
theorem is `Lang.program` refines `Spec P` for every generated `P`, plus the generic kernel lift.
The existing run-sound theorems are already proofs of the ⊆ direction of exactly such a
refinement. They lack only the named spec they refine. A mechanised-metatheory practitioner shown
2,000 theorems with no such statement would say: you have proved a great deal of lemmas and have
not yet said what the system is.

---

## 3. The details judged

### Three choices I would defend at a top venue

**(a) Adequacy of a clocked machine to a big-step meaning, with every fault a named refusal and
divergence identified with fuel exhaustion (LANG-75.13; `run_bigStep`, `runMeasured_means`,
`runMeasuredWith_ok`, READ `Rel.lean:1172-1206`).**
This is the CakeML functional-big-step lesson applied to a replicated object language, and applied
correctly. It lets every client theorem be stated over the meaning while being about the deployed
machine. It gives law 7 its semantics: a refusal is a value of the run, not a missing derivation.
It makes the replication argument trivial: determinism of a total function. At CPP or ITP this is
a clean, citable design point, especially combined with Lean's compiled code being the deployed
code (no extraction gap, unlike Coq-extracted CompCert).

**(b) Declared, authenticated read footprints, with liveness and receipt columns derived by the
runtime, never written by the method (`cited_authenticated`, `receipt_row_authenticated`,
`peerReads_parent`, `peerReads_package`, READ `Rel.lean:364-495`, `PeerRead.lean`).**
The method's TYPE says what it reads. The runtime fills the columns from the signed pins. The
theorem says each column is the kernel's view of the cell the key names. This is an
object-capability discipline (Miller, "Robust Composition", 2006) made into a type-and-theorem
pair. It is the right way to give a contract language revocation-awareness without a proof
system. The peer read, with the "same package" check and the peer named by the argument's `pair`,
is a small and elegant answer to "how does an object read its counterparty without ambient
authority". With LANG-77's runtime encoding, it gives the one-θ property by codec canonicity, a
proof idea I would expect a reviewer to like.

**(c) "The receiver is the monitor", stated over arbitrary methods given only the guard
(`activity_monitor_safe`, `waiting_body_step`, READ `StdActivityMonitor.lean:179-405`).**
The property, that every admitted edit of an activity log is a step of the per-key machine,
quantifies over every method of the package, generated or hand-written, with premises only on the
relation's guard. That is local reasoning in the separation-logic sense. The invariant lives with
the resource (the relation), not with its clients. It is precisely Schneider's enforceability
(safety properties enforced by a monitor), proved against the deployed monitor. LANG-76's deadline
arm extends it without breaking the shape. With a liveness counterpart it would be a workshop paper
by itself.

### Three choices I would be embarrassed to present

**(1) The offer and escrow as "contracts". Read the `Lang/StdOffer.lean` and
`Lang/StdOfferEscrow.lean` headers next to the theorems that claim a fuse.**
In the field's terms an offer is a Bartoletti-style contract reduced to (role, interval box over
naturals). Compliance is "roles differ and θ is in both boxes". θ is captured and moves nothing.
In the escrow, nobody's judge reads the leg it receives (yesterday's F1). Presenting this as
"Std.offer, the fuse of two latent contracts" to a contracts or session-types audience would draw
the obvious question: where is the behaviour, and where is compliance in Castagna–Padovani's
sense? The theorems are honest about what they state. The NAMES (`jointLaw_sound`,
`invitation_once`, "the escrow instance") promise a contract theory the definitions do not have.

*What a strong PhD student would build:*
* A week: give every value-moving offer a `want` (asset, minimum amount), judged by the peer's
  take, and restate `escrow_fuse_admitted` as an exchange theorem (each party received at least
  what it wanted). That turns the escrow into a real single-World atomic swap.
* A semester: offers whose `terms` are a small behavioural contract (a finite session type over
  the activity's plans), compliance as a decidable relation proved sound against the row-guard
  machine. That is Nomos-lite and would connect the dead Contextual calculus to the live runtime.

**(2) The proof method: bespoke inversion of every generated term, with no program logic.**
`take_run_sound`, `fuse_run_sound` and `escrow_*_run_sound` are each 100–200 lines that unfold
the generator, invert the case tree arm by arm, and track de Bruijn environments by hand
(`okEnv`, `judgeEnv`, `fuseOkEnv`). They end in existential statements with 15–20 witnesses (READ
`StdOfferFuse.lean:307-326`, `StdOfferEscrow.lean:525-560`). The same tree is inverted again for
the escrow, and every LANG-77 change to the call encoding restated dozens of these (LANG-77 price:
55 RESTATES-MEANING). The decisions record the consequences. The completeness direction is "about
400 lines" and missing, the iff exists for one method body of four (READ `StdOffer.lean:579`), and
each new generator costs a new module. In Iris or CakeML practice this is what a weakest-
precondition calculus or characteristic formulae are for: prove the rules once, then a generated
term's specification follows by mostly mechanical rule application (a `wp_*` tactic, or `simp`
with the rules).

*What the student would build:* a Hoare/WP logic for Lang terms over `BigStep`. One rule per term
former, proved once against `BigStep`. Add a symbolic-evaluation tactic that discharges a generated
term's triple. Then `take`, `fuse`, the escrow and the Bell `answer` each become a stated triple
plus a tactic call, and the completeness direction becomes a total-correctness rule plus a fuel
bound lemma at `stackMax`. A simple version (no frame rule, no concurrency — the language does not
need them) is one to two months. It would cut the generator proofs by an order of magnitude and
make the iff direction routine.

**(3) A literature-dressed calculus with no reader (`Lang/Proofs/Contextual/*`, and its traces in
the runtime docstrings).**
The calculus has real content: `HasProt` with an affine token bag, `hasProt_reach` (subject
reduction), `fill_preserves_hasProt` (READ `Proofs/Contextual/Protocol.lean`). Its connection to
nano was either deleted or never built:
* PROT-2 added a `Role` index and PROT-2r removed it two landings later (LANG-75.10, 75.15);
* PROT-7 and PROT-8 landed as docstrings because nothing reads the calculus (LANG-75.17, 75.18);
* PROT-5's deployed form is `lost_reply_policy`, a Boolean defined by cases with no reader
  (READ `Contextual/Failures.lean:223`).

Presenting this as "session types for nano" would fail the first question: which running object
inhabits `HasProt`? None.

*What the student would build:* either the bridge — a theorem that the activity generator's methods
inhabit `HasProt` for the activity's declared plans, so that `hasProt_reach` becomes a statement
about logs (a month, given the WP logic of (2)) — or the deletion (a day). Both are better than
keeping it as vocabulary.

---

## 4. What to do

### The one structural change

**Introduce a specification tier for Lang packages and a single generic refinement-and-lift theorem.
Make every generator theorem an instance of it.**

Concretely:

* A `MethodSpec` is a relation from (pre-state, decoded args, rows record) to (post-state, calls
  data, edits data), written at the data grain the generators already use (`NamedKey`, `JointOk`,
  `WaitingStep` are already fragments of such specs).
* One theorem: if a package's method `m` has a term-level triple for `Spec m` (proved by BigStep,
  ideally by the WP logic of §3(2)), then every returned `Lang.program` run of `m` satisfies
  `Spec m` after `callsOf`/`editsOf` decoding. This generalises `take_run_sound` and its siblings,
  whose bodies are already this proof specialised by hand.
* One kernel lift: if every method of P meets its spec, then every admitted Turn whose dispatched
  invokes run P meets the composition of their specs over `Dispatched`. This generalises
  `fuse_tree` and `escrow_party`, and makes yesterday's missing Turn-grain composition of
  `run_edits_guarded` a corollary.
* The specs live in a `Lang/Spec/*` tier beside the generators. Law 8 is amended to
  spec / def / proof.

What this would make true: every generator's guarantee written ONCE, readable by a human in tens
of lines, separate from its proof. The kind of statement defect found yesterday becomes a spec
review instead of a catalogue audit. The escrow's missing "receives" would have been an obviously
missing spec clause, not a missing conjunct buried in a 20-witness existential. The cost is about
two months, most of it the WP logic, and the existing proofs become its first clients rather than
throwaways. No byte moves; this is a proof-tier change.

### The one thing to stop doing

**Stop treating "a plant reds a named theorem" as the evidence that a statement is right, and stop
shaping proofs (`*_core` premises, module moves "so each plant reds its own module") to produce
that evidence.**

Keep plants as what they are, vacuity detectors, and keep running them. But restore law 6's
adversarial statement reader, against a written spec (above). Count a statement as checked when a
reader who did not write it has compared it to the spec and tried to satisfy it trivially.
LANG-75.20's and 75.21's own meta-critiques show the ritual costing proof structure. Yesterday's
two DEFECTs show it missing exactly what a reader catches in minutes: a free variable and an
absent conjunct.

### Grade

**B− against the bleeding edge of mechanised verification of language-based systems.** The base is
first-rate:
* zero axioms;
* a clocked semantics with adequacy;
* the deployed function is the proved function;
* authenticated declared footprints;
* a monitor theorem with genuinely local premises;
* a novel runtime CMTT.

But the layer has no specification tier and no program logic. It establishes trust by a hand-curated
catalogue of bespoke existentials audited by plants. That is a method the field moved past with
seL4, CompCert and Iris, for reasons this layer's own decision log keeps rediscovering.
