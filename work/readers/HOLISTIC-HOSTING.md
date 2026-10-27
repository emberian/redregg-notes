# HOLISTIC-HOSTING — a judgment of nanodregg's Hosting layer against the field (2026-10-24)

Reader: the same sub-opus that wrote `READ-HOSTING.md` from a whole-file read at origin/main
f9657bd. No edits, no builds. Tags: READ (path) = I read it in the code; INFERRED = my reasoning,
not a line I saw. Literature is cited by name and year only where I am confident of both;
otherwise I say "the X line of work".

---

## 1. What this layer is, in the field's terms

Hosting is four things stacked. Each one instantiates a known design.

### 1a. A level-triggered reconciler over a decided log: desired state in the World, observed state in the box

READ `Hosting/Lifecycle.lean`, `Hosting/Controller.lean`, `Hosting/Plan.lean`.
- A grain's desired phase (`installed / running / stopped / removed`) is World state.
- What the box observes (pid, exits) is never World state ("Observed state lives only here and in
  the OS process table").
- The controller compares the two for the cell ids a batch touched and converges. It fails closed:
  a running child whose cell does not desire `running` is killed.

This is the Kubernetes controller pattern (level-triggered reconciliation against a declarative
store). The pattern goes back to Borg/Omega and is studied formally in the verified-controller
work: Anvil (OSDI 2024) proves liveness of cluster-management controllers in Verus. Nano is
**at the state of the art in shape** and **behind it in what is proved**:
- What nano proves is safety: `reconcile_names` and fail-closed decisions. `Proofs.Frame` shows
  that deciding only touched ids misses nothing, which is the batch frame property every
  incremental reconciler needs and few state.
- What it does not prove is liveness ("eventually converges"). Restart backoff is explicitly
  advisory (Controller.lean header), and the charter rules liveness "measured, never proved".

For a single-operator vat that is a defensible scope line. It is not the bleeding edge, which is
Anvil's ESR ("eventually stable reconciliation").

The grain vocabulary (grain, SPK, package, confined sandbox with a per-grain volume) is
Sandstorm's (Varda et al., the Sandstorm.io line of work). The plan is "a total function of
(store label, grain)" with `plan_not_exposed` and `plan_sockets_own`, which is a typed, Lean-decided
version of Sandstorm's confinement manifest. That is a genuine improvement on Sandstorm: there,
confinement is configuration, while here the policy is a function with theorems and the launcher
only transcribes it (READ `Plan.lean` header; INFERRED for the Rust side, which I did not read).

### 1b. The resident: an agent program as a first-order effect tree, with trace semantics and an interpreter-adequacy lemma

READ `Resident/Run.lean`, `Resident/Trace.lean`, `Proofs/ResidentRun.lean`.
- `Prog α` has `done | cmd | keep | forget | ask | say`, each continuation taking the effect's
  result.
- `Prog.interp` is a handler-parametric interpreter.
- `Runs p es a` is the set of paths over EVERY result each effect could have.
- `interp_runs` says the interpreter at a recording handler performs exactly one path.

This is a free monad over a fixed effect signature: the algebraic-effects-and-handlers tradition
(Plotkin and Pretnar's handlers, 2009; Swierstra's "Data types à la carte", 2008). It is the
first-order, inductive, finite-depth special case of Interaction Trees (Xia et al., POPL 2020).
- Nano's tree is inductive and every node is in tail position, so one tick is a FINITE tree. It
  needs no coinduction and no `eutt`, and the theorems are plain induction over paths. That is the
  right engineering choice when one tick is bounded.
- The "lifetime" across ticks is a separate inductive (`Lifetime`, and a twin, `Ticks`), which is
  where an ITree-style coinductive `iter` would have given one object instead of two.

Where nano is behind ITrees and the Iris-style program logics:
- There is no equational theory. Two trees cannot be proved equivalent, which matters as soon as
  you refactor the tick.
- Adequacy is stated only at the recording handler, not at the IO handler. ResidentRun.lean:31-33
  says so honestly.
- There is no separation logic for the volume. The volume's crash behaviour is handled by
  enumerating the POSIX op lists `keepOps`/`forgetOps` against a stated contract
  (`Proofs/ResidentVolume`, which I did not read whole; INFERRED from `Run.lean`'s docstrings). This
  is a miniature of the FSCQ crash-Hoare-logic idea (Chen et al., SOSP 2015) and of Perennial's
  crash invariants with recovery procedures (Chajed et al., SOSP 2019). `resumeOps` is literally a
  Perennial-style recovery procedure, re-run idempotently at start (HOSTING-39). Nano has the
  concept and does not have the logic: each crash theorem is proved over one op list, so a new
  durable object means a new enumeration.

### 1c. Exactly-once effects over an at-most-once channel: durable intent before spend, identity carried in the request, ambiguity resolved by re-reading state

READ `Resident/Bell.lean` header, `Run.lean` `actOn`/`deliverP`.
- The intent `(unanswered restart)` is kept durably BEFORE the ask leaves. This is write-ahead
  logging of an intent, the outbox/idempotency-key pattern of industrial exactly-once systems.
  In theory it is Gray's and Lampson's commit-uncertainty discipline: after an ambiguous outcome
  you read the state, you do not trust the error name.
- The answer carries the ring's own text, and the Bell's `rings` guard refuses unless the text and
  the unanswered status match (LANG-59). That makes the delivery a **conditional write**:
  compare-and-swap on the row. Exactly-once is enforced at the receiver, not by the sender's
  bookkeeping.
- The verified-systems analogue is how Verdi (Wilcox et al., PLDI 2015) layers a "sequence-number
  dedup" transformer over an unreliable network, and how IronFleet (Hawblitzel et al., SOSP 2015)
  states at-most-once client semantics in its RSL spec.

Nano's distinctive move is **judging a refusal by the rows, not by its name**: "after any refusal
the resident reads `pending` again" (Run.lean `deliverP` docstring). It is not novel; it is the
classical answer, but it is stated cleanly and has a theorem (`deliver_gone_continues`). Where
nano is behind is that exactly-once is proved in three slices:
- one tick (`tick_counts`);
- one process (`bell_resident_conforms` over `Ticks`);
- the crash seed (`ResidentVolume`).
They are never composed into "at most one charged ask per ring over any schedule of crashes and
restarts". That composite is the theorem a reviewer at OSDI would ask for first.

### 1d. The member-socket model: a rely relation defined by the environment's own transition function

READ `Proofs/Socket.lean`, `Proofs/SocketStrong.lean`, decisions HOSTING-42/43.
- `Moves w w'` is "one `Command.step` of the deployed follower, on ANY continuation, ANY result",
  and `Reach` is its reflexive-transitive closure.
- `FollowRun` is one command's chain of steps, with `Reach` allowed between frames.
- `step_packageAt` shows the package fact is stable under `Moves`.

This is rely-guarantee reasoning (Jones, 1983): `Reach` is the rely, `PackageAt` is a predicate
proved stable under it, and the resident's guarantee is its effect order. HOSTING-43's key decision
is to define the rely by the deployed follower's own step function, not by an `Honest` predicate
the environment is assumed to satisfy. That is exactly what the RG literature recommends, and what
IronFleet does with its host/network model: the rely is the real environment's transition relation,
so it is true by construction.

The proof found a real time-of-check bug (adopt's genesis check, HOSTING-43) because the rely was
the real step. That is the method working as the field says it should.

The trust boundary is a prose TCB row (`gates/tcb.tsv` `stdio-leg`) whose Lean shadow is
`StdioLeg`/`LegFrom`. In the field this is the "network/transport assumption" every verified
distributed system carries (Verdi's network semantics, IronFleet's UDP model). The difference is
that those are *semantic models* of the channel that the implementation is proved against. Nano's
is a *hypothesis on a trace*, satisfied by fiat. There is no model of nd's relay that the Rust is
checked against, only a sentence.

### 1e. The key broker: an authority-holding proxy with reservation metering

READ `Hosting/Broker.lean`, `Proofs/Broker.lean` statements.
- The resident never holds the provider key.
- Keybroker holds it, and Lean decides each ask. Lean prints the upstream JSON body from the ask's
  fields, so nothing the resident sent is forwarded unread (`body_tooth`: a smuggled `max_tokens`
  stays inside a string).
- Lean charges the WORST case before the call (input bytes plus `max_tokens`) and never refunds.
- A restart or a changed allowance opens the window spent to its cap (`start_window_refused`).

This is the object-capability caretaker/proxy pattern (Miller's "Robust Composition" thesis, 2006):
authority is held by a small trusted proxy that attenuates it. Pessimistic reservation metering is
the safe half of the "spending limit" designs in the capability-payment line of work (ERTP-style
purses).
- Theorems: `capped_decide` (never past cap) plus `start_window_refused` (no refund across lives).
- The provider table is Lean's (`providerOf`), so the TLS host is never the resident's word.

This part is at the state of the art for what it does, and better documented than most production
LLM gateways. The provider's JSON reader (`Hosting/Reply.lean`) is a hand-written RFC 8259 subset
parser whose correctness is established only by the round trip `reply_printed` plus closed
instances. The bleeding edge for this is generated, verified parsers: EverParse (Ramananandro et
al., USENIX Security 2019), and the Narcissus line of work for Coq. Nano is behind there.

### 1f. The Bell: the running multi-party instance, without a global type

READ `Proofs/BellConform.lean` header, `Lang/Bell.lean` `shapeOk`, `world/resident/Bell.ob`.
- The Bell is a two-role protocol, ringer and resident, plus an owner who may retire.
- It is a queue of rings, each answered at most once, guarded by a typestate on the log row
  (`activityWaiting`: the waiting/answered machine).
- In session-type terms it is a tiny multiparty protocol (Honda, Yoshida and Carbone, POPL 2008),
  and `rung` is a typestate in the Strom–Yemini sense (1986) enforced at the receiver.

BellConform's header is admirably explicit that there is NO global type and no projection ("What
this is NOT: the plan's `proj bellG resident`"). So the Bell is checked as two local machines plus a
receiver-side guard, not as the projection of a global session. For a two-role, one-round protocol
that is fine. Scalas and Yoshida's "Less is more" (POPL 2019) would say you do not need a global
type to get safety, only a property of the local types. Nano is roughly there by accident, without
the theory.

### Novel, or merely idiosyncratic?

- **The description carries the package's bytes, and the client checks the program it is about to
  serve by a shape predicate on those bytes** (`bellCore`, `shapeOk`, HOSTING-45). Remote code
  identity by hash is standard (content addressing, attestation). Checking a structural predicate
  of the decoded program instead of its identity is less common. It is closer to proof-carrying
  code's "check a property of the code you receive" (Necula, POPL 1997) than to attestation, done
  with a Boolean predicate instead of a certificate. Mildly novel, defensible: the theorems are
  about `shapeOk`, so checking `shapeOk` is the right grain (HOSTING-45's own argument).
- **"Every theorem has a plant that reds it by name, recorded in the decision."** This is
  mutation-based vacuity detection, a known idea in model checking: vacuity in temporal-logic model
  checking, from the Beer et al. (1997) and Kupferman–Vardi (late 1990s) line of work. Applying it
  to Lean statements and recording the red as part of the decision is idiosyncratic and useful;
  §2 has its limits.
- **The intent text `(unanswered restart)` as the answer a restart delivers.** It trades one wasted
  answer for zero double charges. That is a standard "prefer at-most-once on the expensive side"
  choice, made legible. Not novel.

---

## 2. The architecture judged

### The laws as a design (CHARTER.md, READ)

**Load-bearing and correct:**
- **Law 2 (Lean decides, Rust moves bytes).** This is the right TCB discipline and the one that
  makes Hosting's theorems mean anything. In my layer it is mostly real:
  - the broker's every decision is `Broker.decide`/`step`/`admit`;
  - the plan is Lean's;
  - the controller's actions are Lean's;
  - the provider JSON is read by Lean.
  It is the seL4 principle (minimise and name the unverified) applied to a polyglot system. It is
  what IronFleet and Verdi lack: their trusted shims are larger.
- **Law 7 (refusals by name; a parse failure is never a verdict; "uncertain" is real).** This is
  correct and is the formal content of the exactly-once design. It is the law I found violated in
  the deployed resident (READ-HOSTING D2: undecodable stdout → `""` → "nothing pending"). That
  violation is the architectural lesson: the law is only as strong as the reviewer's grep. A
  mechanical lint for `getD ""` / `getD default` on decoded boundary data would make it a gate.
- **Law 10 (decisions with critique and meta-critique).** Unusual, and good as an idea. It is
  architecture decision records with a built-in red team. The HOSTING-44 meta-critique ("a
  blocker named in a decision is a claim to re-measure") is the kind of epistemics most projects
  never write down.

**Aspirational (stated, not what the code does in this layer):**
- **Law 1 (one of everything).** In Hosting alone I found:
  - two line splitters (`splitLines` / `String.splitOn`);
  - two copies of the 2000-byte bound (`textMax` / `Lang.Bell.answerBounds`);
  - two inductives for one process's ticks (`Ticks` / `Lifetime`);
  - two readings of the Bell's shape (decoded package vs printed lines);
  - the tick program restated as a Prop beside itself (`TickCore`/`readRings`).
  The law is right. It is unenforced: no gate detects "two definitions of one fact", because that
  is semantic. The census of `def`s without `@[export]` (the breadstuffs lesson) is the nearest
  mechanical proxy, and nothing like it runs per layer here (INFERRED from the gates listing).
- **Law 4 (TigerStyle: an assertion for every premise where it enters).**
  - The resident ignores the `object` line of the description it trusts to be about `c.bell`
    (READ-HOSTING Q4).
  - The `lifetimeTicks = 2^48` bound makes the loop total by bookkeeping. That is legitimate fuel,
    standard in Lean practice, but it is a termination technicality, not a liveness argument.
  - D3, an invoke `declined` retried once a second for 2^48 seconds, shows a "static bound on
    everything" that bounds nothing an operator would recognise.
  TigerStyle's real content is *assertion density at boundaries*, and that is where my layer is
  thin.
- **Law 9 (every commit builds).** `Hosting.Proofs.Reply` does not build in 10 GB and was excluded
  from the control build (decisions:2337). A default-target module nobody builds is a theorem
  nobody checks. This is minor in scale and major in principle.

**Wrong-headed, or at least mis-aimed:**
- **Law 8's def/proof split by file.** It is right for rebuild latency. Combined with law 2, though,
  it produces the TickCore phenomenon: the proof module restates the program as a Prop so that the
  def module does not import proofs. The field's answer is to state specs in a third place (a spec
  module) that both import. Nano has `Trace.lean` as a half-step toward that, and it is
  underused.
- **Law 12 (size is a ratchet).** As a pressure it is right. As a law it is wrong-headed, because
  it counts lines while the costly growth in Hosting is *statements without composition*: many
  theorems, each with a "Not claimed" list, never joined. A ratchet on "theorems not consumed by
  any other theorem or by a top-level statement" would aim at the actual sprawl.

### The layer cuts

The cut that is **wrong** is between Hosting and Protocol.
- Hosting's socket proofs reason about the *internals* of `Protocol.Command.step` and `start`
  (READ `Proofs/Socket.lean`: `step_cont`, `step_invoke_ok`, `start_ne_ok`, `envelopeRefused_cont`,
  `step_describe_ok`). They do it by `repeat' split … all_goals first | …` over every arm of the
  command machine.
- These are theorems ABOUT Protocol, living in Hosting, and they will break whenever Protocol adds
  an arm.
- The missing cut is a **client contract of the follower**: a small Protocol-owned specification
  of what follow's command machine promises any client, with Hosting consuming it. Examples:
  - "an `ok` for an invoke is a settlement of a call planned from this argv";
  - "a continuation's argv is the start's";
  - "a describe's ok text is `describeText` of the live object".
- This is the classic refinement-layering mistake: the client is proved against the server's
  implementation instead of its interface. IronFleet's two-level structure (protocol layer,
  implementation layer) exists to prevent exactly this.

A second missing cut is a **spec layer for the Bell as a whole system**. Its pieces are scattered:
- the resident's local order (Hosting);
- the Bell's machine (Lang);
- the follower's journal provenance (Protocol);
- the transport (TCB row).
Nobody owns "the Bell system". `BellRow.lean`'s header says so: "The composite … is not stated".

The cuts that are **right**:
- Broker vs resident (key custody), which is the ocap cut and is clean.
- Plan as a pure function vs launcher as a transcriber.
- Volume contract as a stated trust vs the resident's logic.

### Single writer, receipts between Worlds, no agreement engine

For this system (one operator, a trusted vat, members who consent by re-execution) this is the
**right call, not a deferral**. A single sequencer with deterministic re-execution is Calvin's
insight (Thomson et al., SIGMOD 2012) without the partitioning: once an order is fixed, replicas
need only re-execute. Followers that re-derive every Turn make the follower the auditor, which is
exactly what HOSTING-43(a) leans on ("that IS the audit").
- What the charter gives up is availability under writer failure. It says so, and prices
  replication by agreement as a planned phase that keeps one decided log, which is the
  Tendermint/Raft-shaped extension.
- For Hosting specifically, the single writer is what makes the resident's exactly-once argument
  tractable: there is one row to compare-and-swap.

### The judge / gates / census / plants apparatus as a verification method

Plants are sound for what they do and hollow for what they are taken to do.
- **Sound:** a plant shows that one named theorem depends on one named fact of the code. It is
  mutation analysis applied to specifications, and it catches the breadstuffs failure mode (a
  theorem that survives any change, `P → P`). HOSTING-43's three plants, one per trigger, and
  HOSTING-45's are well-designed.
- **Hollow:** a plant shows that a statement is *not trivially true of the code*. It cannot show
  that the statement is *not trivially true outright*. READ-HOSTING D1, `journal_committed`'s
  unbounded second-preimage disjunct, would survive every code plant. The disjunct is satisfied by
  the hash function's mathematics, not by anything in the code. The vacuity check that would have
  caught it reads statements, not code ("could this disjunct be inhabited with no adversary at
  all?"). That is the 10-20 lesson, and it recurs because the apparatus is code-mutation-centric.

Compare how the reference systems establish trust:
- **seL4** (Klein et al., SOSP 2009; integrity and confidentiality by Murray et al., 2013): one
  refinement chain from C to an abstract spec, then security properties proved ONCE about the
  abstract spec. Local lemmas are subordinate to the chain.
- **CompCert** (Leroy, 2006 onwards): one semantic preservation theorem per pass, composed.
- **IronFleet** (Hawblitzel et al., 2015): implementation refines protocol, protocol refines a
  spec state machine, plus liveness.

In each, the trust is in ONE top-level statement a reader can audit in an afternoon. Nano has
~6,000 theorems and no top-level statement that the system refines a spec.

For Hosting the spec is easy to write, because it already exists in prose (Bell.lean header):
- each ring, from the moment it is pending, is answered at most once;
- its answer is a text decided by at most one charged ask (or named as unanswered);
- the answered row's text is the kept text;
- no ask is charged past the allowance's cap;
- across any crash and restart schedule.

Every ingredient is on disk: `tick_counts`, `bell_resident_conforms`, `kept_follows`,
`ResidentVolume.keep_atomic`, `resume_durable`, `delivered_answer_committed_strong`,
`answered_row_is_kept_answer`, `capped_decide`. A mechanised-metatheory practitioner would say:
**the absence of the composite is not a missing theorem, it is the missing verification.** The
pieces carry "Not claimed" lists precisely at the seams where composition would bite:
- restarts;
- lost replies;
- the World that holds the row afterwards;
- the journal entry's provenance.
Composition is where the D1 disjunct, the two tick-chain definitions and the `getD ""` gap stop
being local and become wrong answers.

Should one exist? Yes, and for Hosting it should be the *first* deliverable of any further work,
not the last.

---

## 3. The details judged

### Three choices I would defend at a top venue

**(i) The tick as a finite effect tree, with every order theorem quantified over every oracle.**
READ `Run.lean` `Prog`, `ResidentRun.lean` `Runs`, `tick_order`, `tick_counts`, `order_refuses_*`.
- The resident's control flow is data. Every node is one external effect in tail position, and the
  theorems range over all results each effect could have: every socket reply, every failed keep,
  every `AskEnd`.
- That is the right altitude for an agent that talks to untrusted services. It makes "the
  intent is kept before the ask" a statement about every execution rather than a test.
- The teeth (`order_refuses_ask_before_keep`, `order_refuses_forget_while_pending`, …) are
  negative theorems that pin the grammar from the other side.
- At a venue this is "an Interaction-Tree-style agent with a trace-set semantics, sized so that
  plain induction suffices". It is a clean, small, honest contribution.

**(ii) The rely is the deployed follower's own step function, and package stability is a theorem of every step.**
READ `Socket.lean` `Moves`/`Reach`, `SocketStrong.lean` `reach_packageAt`, HOSTING-43(a).
- Choosing `Moves := ∃ f f' kb res …, Command.step … = …` over an `Honest` predicate means the
  premise is TRUE of the deployed system rather than assumed. The deployed follow really does
  accept any resume bytes from any client (READ `Host/Follow.lean:76-80`).
- The stability proof then found a real defect: adopt could replace a populated World, a
  time-of-check bug.
- This is rely-guarantee done the way Jones intended, discovered by a lane that needed a proof to
  close. It would survive review.

**(iii) Key custody and reservation metering in the broker.**
READ `Broker.lean`, `Proofs/Broker.lean`.
- The resident never sees a key.
- Lean prints the upstream body from typed fields (no forwarding of resident bytes as structure).
- The charge is the worst case, before the call.
- A broker restart, or any change to an allowance, opens the window spent (`start_window_refused`
  over a `Fresh` invariant kept by `follow` and `decide`).
- The provider/TLS host is a Lean table, not a dial address.
- Each is a theorem about the deployed `decide`.
This is an ocap proxy with a conservation-style budget invariant. The "no refunds across lives"
invariant is the subtle one most metering systems get wrong, and here it is a two-line theorem
over an inductive invariant.

### Three choices I would be embarrassed to present

**(E1) The transport premise is a prose row whose Lean shadow is satisfied by fiat, and it bundles
four trusts, one of which is an unauthenticated continuation.**
READ `gates/tcb.tsv:54`, `Socket.lean` `FollowRun`/`LegFrom`, HOSTING-42 meta-critique.
- The theorem "an ok answer is the resident's datum committed on the member's World" is only as
  good as "nd resent THIS command's continuation byte for byte".
- `k` is a byte string follow hands out, and any client may hand any `k` back.
- In the field this is an authenticated-continuation problem with a standard answer: follow MACs
  each continuation with a per-process key and refuses an unauthenticated resume. This is the
  "encrypted/MACed state token" pattern of stateless servers, and of cookies done right.
- With that, `FollowRun`'s chain condition becomes a theorem of `Command.step` (a valid MAC
  implies a continuation this follower issued, for this argv), and the row shrinks to what it
  claims to be: three byte fields moved.
- A strong PhD student would add the MAC, add the refusal `badContinuation`, and restate `StdioLeg`
  without the chain clause. **A week**, including re-running HOSTING-43's plants.
- The more ambitious version is a Verdi-style semantic model of the relay that the Rust is proved
  against. That is **a year**, and not worth it here.

**(E2) Exactly-once is proved in three slices that are never composed, and the slices disagree
about what a run is.**
READ `Proofs/ResidentRun.lean`, `Proofs/BellConform.lean` (`Ticks`), `Proofs/Lifetime.lean`
(`Lifetime`), `Run.lean` `run`.
- The headline property of the resident, one charged ask per ring, has:
  - a per-tick theorem;
  - a per-process theorem over `Ticks`;
  - provenance and bounds theorems over a different per-process inductive, `Lifetime`;
  - a crash-seed theorem over the volume.
- The thing that makes exactly-once hard, a crash between any two effects followed by a restart
  that resumes from the volume, sits only in the seams: BellConform says "across a restart the
  kept answer is the volume's, not composed here".
- The slices are also individually soft at the boundary:
  - a parse failure frees a ring (READ-HOSTING D2);
  - a named refusal outside exit 1 retries forever (D3).
- What a strong student in the Perennial/FSCQ line would build: ONE abstract state machine for a
  ring's life (pending → asked/charged → answered | abandoned), the resident as a refinement of it
  under a crash-and-recover semantics (each crash point can resume via `resumeOps`), and a single
  theorem: for every interleaving of ticks, crashes and restarts, `charged(r) ≤ 1` and
  `answered(r) → answer ∈ kept-history(r)`.
- The pieces exist, so this is **one to two months** of careful work. Most of it is restating
  `Ticks`/`Lifetime` as one coinductive or fuel-indexed process with crash transitions, then
  rewiring the existing lemmas. Perennial itself took years because it built the logic; nano needs
  only the instance.

**(E3) Journal provenance is stated as "admitted at some World satisfying Q", which yields an
existential disjunct that is true for free.**
READ `Proofs/Committed.lean`, `Protocol/Proofs/FollowJournal.lean` `JournalFrom`, `BellRow.lean`
`answered_row_committed`.
- The spec of "this entry came from committing this call" quantifies over any `Q`-World and any
  admissible byte string. The fallback disjunct ("some other admissible call has this id") is
  therefore inhabited by the mathematics of a 32-byte hash over an unbounded domain.
- This is the textbook distinction between *existence* of a second preimage, which is guaranteed,
  and *finding* one, which is hard. Formal crypto handles it by bounding the adversary's view: the
  computational/game-based tradition, CryptoVerif, or EasyCrypt's game-hopping (Barthe et al.'s
  line of work). In a non-probabilistic setting the sound form is collision-freedom over the
  *trace actually produced*.
- A strong student would:
  - add a ghost trace of absorbed calls to `JournalFrom`, i.e. record the path instead of `Q`;
  - restate the disjunct as `CollidesAmong hash trace`;
  - then state the composite `answered_row_committed` on follow's `wf`, not on some `v'`.
- **A week or two.** Most of the cost is in Protocol's `step_journalFrom`, which is another
  layer's file. That is itself the §2 point about the Hosting/Protocol cut.

Runner-up embarrassment, briefly: the provider JSON reader's correctness rests on one round-trip
theorem and closed `decide +kernel` instances, which do not even build in 10 GB. A strong student
would write the grammar once and either generate the parser (the EverParse approach) or prove the
reader complete and unambiguous for the grammar (one induction on `value`/`members`). **Two weeks**
for the proof, and it would make the module buildable.

---

## 4. What to do

### The one structural change with the highest (what it makes true) / (cost)

**Record the path. Give follow's journal provenance a ghost trace of the calls it absorbed, and
state Hosting's composite on that trace.**
- **Change:** `JournalFrom X Q w₀ w` becomes `JournalFrom X w₀ τ w`, where τ is the list of
  `(call bytes, turn)` that follow's frames absorbed from `w₀` to `w`. Every entry of `w` is then
  `w₀`'s, or the commit of an element of τ.
- **What it makes true, in one stroke:**
  1. The second-preimage disjunct becomes `CollidesAmong hash τ`, a statement about a finite
     list, which is the sound form.
  2. `answered_row_committed` can conclude about follow's own World `wf` instead of some
     unrelated `v'`.
  3. The composite theorem ("the resident's ok-delivered answer is the row follow's World holds")
     becomes statable without a hash disjunct over a chosen target. BellRow.lean's header names
     that as the obstruction.
  4. It forces the Protocol-side client contract (§2) into existence, because τ is exactly what
     a client contract exposes.
- **Cost:** restating `step_journalFrom`/`reach_journalFrom` (a few hundred lines in
  Protocol/Proofs, mostly mechanical, since the step already knows the call it absorbed) and
  re-proving `journal_committed` and `answered_row_committed`. Days, not weeks (INFERRED from the
  shape of `JournalFrom` and `submit_journalFrom`'s statement).
- **Runner-up:** MAC the continuation (E1). Similar cost; it shrinks the TCB row to its stated
  size. Do it second.

### The one thing the layer should stop doing

**Stop growing the theorem frontier sideways. No new partial join, with its own "Not claimed"
list, until the top-level Bell spec is written down and the existing pieces are composed against
it.**
- HOSTING-42, 43, 44, 45 and 46 each added a correct, plant-checked theorem plus a careful list of
  what it does not claim. Together they are ~2,000 lines of proofs and ~170 lines of decisions
  converging on a statement nobody has written: the composite.
- Each card's "Not claimed" list is where the next defect hides: restarts, lost replies, the World
  holding the row, provenance. The pattern feels like progress, because every card is green and
  planted. It is the "method items that soothe" trap one level up: it improves the *pieces'*
  quality while the *system's* claim stays unstated.
- Write the spec first (§2's five lines), mark each existing theorem as discharging which of its
  obligations, and let the gaps be the work list.

### Grade

**B− against the bleeding edge.** The architecture's taste is A−:
- the right patterns (reconciler, effect tree, rely by the real step, ocap broker, conditional
  write);
- the right TCB discipline;
- unusually honest documentation of its own limits.

Its verification depth is C+:
- no top-level specification;
- adequacy only at a recording handler;
- a prose transport premise with an unauthenticated continuation;
- an existential provenance disjunct that is true for free;
- exactly-once proved in uncomposed slices.

The sentence: **Hosting picks the designs the literature would pick and proves many true things
about each piece, but it has not yet stated, let alone proved, the one property a reviewer of a
verified hosted-agent system would ask for first: at most one charged ask and an answer that is
the kept one, for every ring, across every crash.**
