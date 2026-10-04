# SCHOLAR-CALLS: calls between objects, concurrency, evolution and checkpoints (2026-10-04)

Brief: `work/PROGRAM-MODEL-BRIEF-20261004.md`. This document covers forks 1 (calls across objects), 3
(concurrency), 4 (evolution), and how 5 (checkpoints) interacts with them.

**How to read it.** Part I is the annotated bibliography, grouped by family (A–H). Part II records where
the sources disagree with each other and with the sibling scholars (BREAD, OS, LAWS). Part III is the
synthesis (≤1500 words), which ranks eight ideas.

**Method and honesty of tags.**
- I collected 80+ primary sources into `~/paperbin/world-program-model/`, with a `.txt` beside every PDF.
  Several were downloaded earlier by sibling scholars and reused.
- I ran seven reader lanes (Opus) under the brief's rules, one family each. Every lane read the papers
  itself and tagged each entry READ, SKIMMED or INFERRED. Their per-paper notes are condensed here, and
  each tag names who did the reading.
- I read the following myself: Waterken, Mina, Stingray, Cambria, Cordial Miners (skim), Herlihy–Liskov–
  Shrira deals, Herlihy swaps, Zakhary, IBC, the BREAD/OS/LAWS syntheses, and Mini's
  `designs/BEND-PERSISTENT-COMPUTATION-20261003.txt`.
- I spot-checked the load-bearing quotes behind the disagreements in Part II against the text (Tezos and
  Urbit call order; Agoric pipelining).
- Mini facts come from the brief and that design file. Nothing here was built, and no repository was
  edited.

Tag conventions: **READ** = the whole paper or the whole of the relevant sections (named). **SKIMMED** =
abstract, introduction and selected sections. **INFERRED** = from background knowledge, not from the
text. `[lane X]` = read by reader lane X. `[me]` = read by me.

---

# Part I — Annotated bibliography

## A. Object capabilities, eventual send, promise pipelining, vats and turns

**A1. Miller, *Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control*.**
PhD thesis, Johns Hopkins, 2006. https://papers.agoric.com/assets/pdf/papers/robust-composition.pdf ·
`miller-robust-composition-2006.txt` · READ for Part III, Ch. 13–19 in full, plus §2.4–2.7, §5.6, §7.1–7.5,
§23–25 [lane A1].
- **The turn.** A turn is one pending delivery processed to an empty stack (§14.1). It has exclusive
  access to everything reachable synchronously, so any multi-vat run is equivalent to an interleaving of
  turns (§14.2). It never blocks, so it cannot deadlock.
- **Not failure-atomic.** A throw breaks the result promise, but the mutations made before it remain.
- **Plan interference** (§13.1). The three hazards are aborting the wrong plan, nested subscription and
  nested publication. They are cured by `<-` to a later turn.
- **Pipelining** (§16.2). A message moves "as close to the arrowhead as possible". Broken promises are
  contagious, like NaN (§16.5).
- **E-ORDER** (§19). Ordering is fail-stop FIFO per reference, with forks at argument passing. CAUSAL
  order is "too strong" among mutually suspicious machines.
- **Argus contrast** (§24.3). Distributed 2PC blocks during a partition.

**A2. Miller, Tribble, Shapiro, "Concurrency Among Strangers: Programming in E as Plan Coordination."**
TGC 2005, LNCS 3705. https://papers.agoric.com/assets/pdf/papers/concurrency-among-strangers.pdf ·
`miller-concurrency-among-strangers-2005.txt` · READ [lane A1].
- Gives precise definitions of reliance set, authority, *defensively consistent* (incorruptible by its
  clients) and *defensively correct*.
- "If P relies on R, then P also relies on all of R's other clients unless R is defensively correct" is
  the argument against threads inside a vat.
- A Mini law makes its cell defensively consistent against its writers.

**A3. Liskov, Shrira, "Promises: Linguistic Support for Efficient Asynchronous Procedure Calls."** PLDI 1988.
doi:10.1145/53990.54016 · `liskov-promises-1988.txt` · READ [lane A1].
- **Call-streams.** Each (agent, port group) is exactly-once and ordered; different streams run in
  parallel.
- **Typed promises.** Promises carry typed exceptions and are claimed in call order.
- **coenter.** Failure of one arm terminates its siblings.
- **Correction to the folklore.** The paper does *not* pipeline calls onto unresolved results; it routes
  stream composition back through the caller (§4–5). Real pipelining comes from Joule and Udanax.
- **For Mini:** per-(sender, target) streams are a sound unit for parallel admission.

**A4. OCapN, "CapTP Specification" (draft) and "Implementation Guide."** https://github.com/ocapn/ocapn ·
`ocapn-captp-spec.md`, `ocapn-implementation-guide.md` · READ [lane A1].
- **Messages.** `op:deliver` carries a sender-chosen `answer-pos`. Messages to the answer are queued until
  it resolves. `op:get`, `op:index` and `op:untag` pipeline into the fields of a result.
- **Three-party handoff** uses doubly signed `handoff-give` and `handoff-receive` with an anti-replay
  count.
- **No embargo.** The spec has no embargo, and the implementation guide reports an ordering bug introduced
  by a latency optimisation. Ordering belongs in the semantics, not in implementer care.

**A5. Varda / Sandstorm, Cap'n Proto RPC: `rpc.capnp` (the protocol, specified in comments) and "RPC
Protocol."** https://github.com/capnproto/capnproto/blob/master/c++/src/capnp/rpc.capnp,
https://capnproto.org/rpc.html · `capnproto-rpc.capnp`, `capnproto-rpc.html` · READ [lane A1].
- **Tables and calls.** Four tables (questions, answers, imports, exports). `PromisedAnswer{questionId,
  transform}`. `sendResultsTo` supports tail calls. `Finish` gives cancellation.
- **Disembargo.** It enforces E-order when a promise resolves onto a second path. When the resolution is
  reached over the same path, "no embargo is needed".
- **The Tribble four-way race** is avoided by the rule that once P resolves to R, messages go strictly
  to R.
- **The case for pipelining.** Without it you get "sad, singleton-ish" fused interfaces.

**A6. Lemmer-Webber, Farmer, Sims, "The Heart of Spritely: Distributed Objects and Capability Security."**
Spritely Institute, draft dated 2025-05-21. https://files.spritely.institute/papers/spritely-core.pdf ·
`lemmerwebber-heart-of-spritely-2023.txt` · READ for §1, §3.1–3.2, §3.4–3.9, glossary; §3.3 SKIMMED
[lane A1].
- **Two call forms.** `$` is a synchronous call between near objects; `<-` is an eventual send.
- **The transactional turn.** It commits the actormap delta together with the outgoing sends; "unhandled
  errors result in a turn being rolled back". This gives time travel.
- **Against coroutines.** Footnote 16 calls them "splitchronous" and a re-entrancy hazard.
- **Upgrade at restore.** Serialization is a sealed self-portrait, and upgrade runs at restore.
- **For Mini:** this is the closest existing turn to Mini's.

**A7. Miller, FIG, Morningstar, "Promise.delegated / eventual send."** TC39 stage 1.
https://github.com/tc39/proposal-eventual-send · `tc39-eventual-send-README.md` · READ [lane A1].
- Design principle 2 is "Prevent reentrancy attacks": the handler runs in a later turn.
- A queued message must be forwarded at the moment its promise resolves to a delegated promise, or it
  "languish[es]" and can arrive out of order.

**A8. Plyukhin, Peressotti, Montesi, "Ozone: Fully Out-of-Order Choreographies."** ECOOP 2024,
arXiv:2401.17403 · `plyukhin-ozone-2024.txt` · SKIMMED (theorems, evaluation) [lane A1].
- Each message carries an *integrity key* derived deterministically and injectively from (line, session
  token). This removes the need for FIFO without any coordination (Thm 4).
- **For Mini:** derive answer-slot ids as H(turn id, call site), so every validator names every pending
  reply identically.

**A9. Voss, Sarkar, "An Ownership Policy and Deadlock Detector for Promises."** PPoPP 2021, arXiv:2101.01312 ·
`voss-promise-ownership-2021.pdf` · SKIMMED [lane A1].
- Every promise has exactly one owner task. A task that terminates while still owning promises is an
  error.
- Deadlock detection is precise (Thm 5.1, Thm 5.6, Cor 5.7) at 1.12× time overhead.
- **For Mini:** the kernel breaks orphaned replies and refuses awaits that would form a cycle.

**A10. Agoric SwingSet documentation** (README, `delivery.md`, `kernel-promises.md`, `c-lists.md`,
`transcript.md`, `persistence.md`, `state.md`, `run-policy.md`, `metering.md`, `async.md`,
`virtual-objects.md`, `garbage-collection.md`, `dynamic-vats.md`; liveslots; vat-data), 2025.
https://github.com/Agoric/agoric-sdk/tree/master/packages/SwingSet/docs · `agoric-swingset-*-2025.md`,
`agoric-liveslots-2025.md`, `agoric-vat-data-2025.md` · READ (all) [lane A2].
- **Crank and block.** A *crank* is one delivery to one vat. Its syscalls go into a crank buffer that is
  committed or discarded. A *block* is the durable commit point, and outbound I/O is embargoed until it
  commits.
- **Resolution authority is linear.** "allocating … creates resolution authority, sending … gives it away,
  … `resolve()` consumes it". A vat that resolves a promise it does not decide is terminated.
- **Pipelining is effectively off locally.** It is enabled for no liveslots vat and is valued only
  off-host.
- **Metering terminates.** Exceeding a meter terminates the vat and cancels its messages.
- **Snapshot hazard.** A snapshot reload shifted GC timing, which threatened a metering divergence (a
  consensus fault).

**A11. Agoric upgrade and durable flows:** `vat-upgrade.md`, contract-upgrade guide, `@agoric/async-flow`
(README and states), `@agoric/vow`, 2025. https://docs.agoric.com/guides/zoe/contract-upgrade ·
`agoric-swingset-vat-upgrade-2025.md`, `agoric-contract-upgrade-doc.txt`, `agoric-async-flow-2025.md`,
`agoric-async-flow-states-2025.md`, `agoric-vow-2025.md` · READ [lanes A2, F].
- **Upgrade is one crank.** v2 must redefine every durable Kind "with the same facets and methods or a
  superset". Otherwise the vat rolls back to v1.
- **Outstanding promises are rejected** ("Upgrade is Semi-Traumatic").
- **async-flow.** It replays a closed guest function over a membrane log through the states Running,
  Sleeping, Replaying, Failed and Done. A divergence waits in Failed for a later upgrade.

**A12. Miller, Van Cutsem, Tulloh, "Distributed Electronic Rights in JavaScript."** ESOP 2013, LNCS 7792.
doi:10.1007/978-3-642-37036-6_1 · `miller-distributed-electronic-rights-js-2013.txt` · READ [lane A2].
- **Mint and purse.** All checks that can fail come before the "commit point".
- **escrowExchange** is "two phase commit enhanced with the possibility of cancellation". The prepared
  rights are *moved into* the decider's domain, so phase 2 cannot fail.
- **Contract host.** Trust is reduced to the issuers, the source text and one host.
- NodeKen checkpoints the heap and the outgoing messages per turn (design only).

**A13. Agoric Zoe, "Offer Safety" and "Zoe Overview."** docs.agoric.com · `agoric-zoe-offer-safety-docs.txt` ·
READ [lane A2].
- **The offer-safety guarantee.** "either get at least what they wanted, or get back a full refund".
- **How Zoe enforces it.** The contract proposes a reallocation as data. Zoe commits it only if it is
  offer-safe and conserves supply. This is "code proposes, law disposes" over escrowed rights.

**A14. Swasey, Garg, Dreyer, "Robust and Compositional Verification of Object Capability Patterns."**
OOPSLA 2017. doi:10.1145/3133913 · `swasey-robust-verification-ocap-patterns-2017.txt` · SKIMMED [lane A2].
- **The result.** Robust safety: a closed expression that returns only "low" values keeps every reachable
  state good under any adversarial context. It is Iris-based and mechanised in Coq.
- **The statement Mini wants.** Every Plan from untrusted code is judged, so laws are robustly safe.

**A15. Drossopoulou, Mackay, Eisenbach, Noble, "Reasoning about External Calls."** arXiv:2506.06544 (2025) ·
`drossopoulou-external-calls-2025.txt` · SKIMMED [lane A2].
- **Hoare quadruples.** These carry a *mid-condition* that must hold at every external state reached
  during a call. *Scoped invariants* hold until the active call returns (Thm 7.2).
- **For Mini:** this is the obligation Mini takes on if a cross-principal call runs inside a method's
  evaluation.

**A16. Close, Waterken Server documentation and "upgrade: Live fast, die young and leave a good-looking
corpse."** c. 2008–10. http://waterken.sourceforge.net/upgrade/ · `waterken-home.txt`,
`waterken-upgrade.txt`, `waterken-web_send.txt`, `waterken-ref_send-promise.txt` · READ (home page and
upgrade essay) [me].
- **Output commit per turn.** "At the end of every event loop turn, before any externally visible I/O is
  done, the Waterken server persists all application objects that are reachable."
- **Whole-graph migration.** `touch.jar` migrates a vat's whole object graph "as a normal vat transaction
  … commit with all objects upgraded, or abort".
- **"Implants"** separate state objects from behaviour objects, so new behaviour can be layered on the
  same state.
- **Short-lived vats** are the defence against upgrade debt.

## B. Actors, virtual actors, actor and protocol verification

**B1. Bernstein et al., "Project Orleans: Distributed Virtual Actors for Programmability and Scalability."**
Talk slides, c. 2015, companion to MSR-TR-2014-41.
https://www.microsoft.com/en-us/research/publication/orleans-distributed-virtual-actors-for-programmability-and-scalability/ ·
`bernstein-orleans-virtual-actors-2014.txt` (this is the slide deck, not the TR) · READ (deck) [lane B].
- **Virtual actors.** Actors "always exist" and are activated on demand. Activations are single-threaded
  and optionally reentrant.
- **No transactional turns.** State is saved "whenever it wants", so a request is neither atomic nor
  durable.

**B2. Microsoft, "Request scheduling" (Orleans), 2026.**
https://learn.microsoft.com/en-us/dotnet/orleans/grains/request-scheduling · `orleans-request-scheduling.txt` ·
READ [lane B].
- **Non-reentrant by default.** A grain holds a request across its awaits, so a cycle A→B→A deadlocks
  until a timeout fires.
- **Interleaving options:** `[Reentrant]`, `[AlwaysInterleave]`, `[ReadOnly]`, `MayInterleave`, and the
  scoped `AllowCallChainReentrancy`.
- "This protection against concurrency bugs has a cost, primarily liveness."

**B3. Eldeeb, Burckhardt, Bond, Cidon, Yang, Bernstein, "Cloud Actor-Oriented Database Transactions in
Orleans."** PVLDB 17(12), 2024. doi:10.14778/3685800.3685801 · `eldeeb-orleans-transactions-2024.txt` ·
READ [lane B].
- **Context union.** The transaction context is a union of read/write sets. "If the union … has seen more
  than one version of any grain, it will abort."
- **Commit.** Grain-level 2PL, with one participant acting as transaction manager. Locks are released
  early, at prepare.
- **Reconnaissance queries.** A lock-free trial run approximates the footprint, so locks can be taken in a
  global order (no deadlock aborts, Fig 8).
- **Side effects are not enforced.** They are "left to programmer discipline".

**B4. Liu, Laigner, Zhou, "Rethinking State Management in Actor Systems for Cloud-Native Applications"
(SmSa).** SoCC 2024, arXiv:2410.15831 · `zhou-rethinking-state-actors-2024.txt` · READ [lane B].
- **Declared leader/follower dependencies** are forwarded as internal transactional calls.
- **Key-level schedules** inside one actor.
- **Measured:** a PACT spends "∼80% time waiting for the turn to start execution on the first actor".
  Object granularity is the bottleneck.

**B5. Liu, Su, Shah, Zhou, Vaz Salles, "Hybrid Deterministic and Nondeterministic Execution of
Transactions in Actor Systems" (Snapper).** SIGMOD 2022. doi:10.1145/3514221.3526172 · `liu-snapper-2022.txt` ·
READ [lane E].
- **PACT** (declared actor access counts). Token-ring batches, deterministic per-actor schedules,
  three one-way commit messages. A user abort cascades to every uncommitted batch.
- **ACT** (undeclared): S2PL, wait-die and 2PC.
- **The hybrid boundary is expensive.** Throughput drops sharply going from 100% to 99% PACT.

**B6. Clebsch, Drossopoulou, Blessing, McNeil, "Deny Capabilities for Safe, Fast Actors" (Pony).** AGERE!
2015. doi:10.1145/2824815.2824816 · `clebsch-deny-capabilities-2015.txt` · READ [lane B].
- **Capabilities.** iso, trn, ref, val, box and tag are defined by which aliases they deny. Only iso, val
  and tag are sendable. A behaviour is atomic and uninterruptible.
- **No soundness proof in this paper.**
- **For Mini:** this is the rule for what a suspended activity may capture (val, iso, tag; never a ref to
  object state).

**B7. Hinrichsen, Bengtson, Krebbers, "Actris: Session-Type Based Reasoning in Separation Logic."**
POPL 2020. doi:10.1145/3371074 · `hinrichsen-actris-2020.txt` · READ §1–6, §8 [lane B].
- **Dependent separation protocols.** `!x⟨v⟩{P}.prot` transfers resources along with messages. Adequacy
  is Thm 5.1, mechanised in Coq.
- **Limits.** No deadlock freedom; binary protocols only.
- **For Mini:** `Activity<P,R,A>` should become dependent: R indexed by the yielded Plan.

**B8. Summers, Müller, "Actor Services: Modular Verification of Message Passing Programs."** ESOP 2016.
doi:10.1007/978-3-662-49498-1_27 · `summers-actor-services-2016.txt` · READ [lane B].
- **Response properties** of the form `T ⤳ R`, proved with obligations.
- **Actor invariants** must be self-framing and transitive to be usable across handlers.
- Soundness is only sketched.
- **For Mini:** a law that feeds cross-turn reasoning must be reflexive and transitive.

**B9. Krogh-Jespersen et al., "Aneris."** ESOP 2020 · `kroghjespersen-aneris-2020.txt` · SKIMMED [lane B].
**Timany et al., "Trillium."** POPL 2024, doi:10.1145/3632851 · `trillium-timany-2024.txt` · SKIMMED
[lane B]. **Sergey, Wilcox, Tatlock, "Disel."** POPL 2018, doi:10.1145/3158116 · `sergey-disel-2018.txt` ·
SKIMMED [lane B].
- **Aneris:** socket protocols act as laws over inbound messages.
- **Trillium:** refinement to a TLA+-style model step. It gave the first foundational proof of 2PC and
  Paxos against TLA+.
- **Disel:** send-hooks let one component constrain another's sends.
- **For Mini:** the tractable verification route is a model-first refinement, in which each admitted turn
  refines one step of a protocol model in Lean.

## C. Durable execution, workflows, exactly-once stateful serverless

**C1. Burckhardt, Gillum, Justo, Kallas, McMahon, Meiklejohn, "Durable Functions: Semantics for Stateful
Serverless."** OOPSLA 2021. doi:10.1145/3485510 · `burckhardt-durable-functions-semantics-2021.txt` ·
READ §1–8 [lane C].
- **The theorems.** Thm 5.3: the compute-storage model weakly simulates the high-level model
  ("observably exactly-once"). Thm 6.4: replay and storage of state are *bisimilar* for fixed
  deterministic code.
- **The S-Commit step** is a CAS on (consumed messages, prior state) that enqueues outputs atomically.
- **Critical sections.** Locksets are declared, acquired in a global order, cannot nest, and only locked
  entities may be called inside them.
- **What the proofs exclude.** External calls, critical sections and *versioning* are all outside the
  proofs.

**C2. Burckhardt et al., "Netherite: Efficient Execution of Serverless Workflows."** PVLDB 15(8) 2022,
arXiv:2103.00033 · `burckhardt-netherite-2022.txt` · READ (arXiv v1) [lane C].
- **Causally Consistent Commit.** Aborted work aborts everything that depends on it.
- **The atomic step.** StepCompleted atomically updates state, removes consumed messages, and adds
  produced messages and tasks.
- **Speculation.** Within a partition, speculation is free (truncate on recovery). Across partitions, a
  failure rewinds dependants.
- **Measured:** ×38 median latency on task sequences.

**C3. Zhang, Cardoza, Chen, Angel, Liu, "Fault-tolerant and Transactional Stateful Serverless Workflows"
(Beldi).** OSDI 2020, arXiv:2010.06706 · `zhang-beldi-2020.txt` · READ §1–8 [lane C].
- **Exactly-once.** Intent logs keyed by (instance id, step) give at-least-once plus at-most-once.
- **Locks and transactions.** Locks are owned by intents. Transactions use wait-die and a *collaborative*
  2PC along call edges, because under data sovereignty "there is no entity that can serve as a
  coordinator".
- **Opacity.** Isolation is opacity, because replay would re-trigger any inconsistent read.
- **Garbage collection** assumes every instance terminates within T.

**C4. Jia, Witchel, "Boki: Stateful Serverless Computing with Shared Logs."** SOSP 2021.
doi:10.1145/3477132.3483541 · `jia-boki-2021.txt` · READ §1–6 [lane C].
- **The metalog.** It orders, gives read consistency, and handles faults. "A child function inherits the
  metalog position from its parent."
- **BokiStore** decides transaction outcomes by deterministic replay, which is Mini's admission in log
  form.
- **Measured:** 4.3–4.7× lower latency than Beldi.

**C5. Qi, Liu, Jin, "Halfmoon: Log-Optimal Fault-Tolerant Stateful Serverless Computing."** SOSP 2023.
doi:10.1145/3600006.3613154 · `qi-halfmoon-2023.txt` · READ §1–7 [lane C].
- **The theorem.** Thm 4.6: a fault-tolerant protocol must log all reads or all writes that have visible
  effects.
- **Halfmoon-read** logs only writes, with deterministic version numbers. Regime switches drain in-flight
  work first.
- **For Mini:** a root chain plus signed inputs is already log-optimal. Only *external* data needs logging,
  as a signed resume.

**C6. Khan, "Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and
Resume Semantics in Workflow Persistence Layers."** arXiv:2608.03836v3 (Aug 2026) ·
`khan-resume-means-resume-2026.txt` · READ §1–9 [lane C].
- **Six properties:**
  - PC (prefix continuation);
  - EO (effect exactly-once per branch);
  - FD (fork determinism);
  - CV (checkpoint validity: a schema-invalid write is refused);
  - CO (consume-once): CO-c, one resume per interrupt; CO-e, a duplicate resume is inert;
  - RD (recovery determinism).

  Plus FI (fork intent must be expressible on the wire) and liveness.
- **Proofs.** TLC and TLAPS (196 obligations). Lemma 1: FD and CO are jointly impossible without a
  discriminator on the wire.
- **Measured failures.** LangGraph, CrewAI and pydantic-graph each violate some properties. Consume-once
  failed under concurrency: 2,628 fires where 400 were expected.
- **The repair** that works is a claim made at the read/decide point; write-path repairs failed twice.
- **Out of scope:** cross-version migration ("evolution requires an explicit migration step before any
  resume").

**C7. Restate, "Building a modern Durable Execution Engine from First Principles" (blog, 2025-02-20) and
"Key Concepts."** https://www.restate.dev/blog/building-a-modern-durable-execution-engine-from-first-principles ·
`restate-durable-engine-first-principles.txt`, `restate-key-concepts.txt` · READ [lane C].
- **Virtual Objects** are "single-writer per key".
- **Attempt fencing** rejects events from a stale invocation attempt; it is the operational form of
  consume-once.
- "Being persistent in the log is the point when 'the step happened'."
- Says nothing about versioning.

**C8. Temporal, "Versioning – TypeScript SDK" and "Safely deploying changes to Workflow code," 2025–26.**
https://docs.temporal.io/develop/typescript/workflows/versioning · `temporal-versioning-ts.txt`,
`temporal-safe-deployments.txt` · READ [lanes C, F].
- **Compatibility is the command sequence.** "Each await is a yield point that affects the Command sequence
  seen during Replay."
- **Patching.** `patched` markers fail replay on divergence.
- **Worker Versioning** pins an execution to a code revision, or auto-upgrades it.
- **Replay testing** runs against production histories at deploy time.

**C9. Psarakis, Christodoulou, Siachamis, Fragkoulis, Katsifodimos, "Styx: Transactional Stateful
Functions on Streaming Dataflows."** arXiv:2312.06893v4 (2025) · `psarakis-styx-2023.txt` · READ §1–7
[lane E].
- **Deterministic transactions over function-to-function calls whose call graph is discovered at run
  time.** It executes on a snapshot, then resolves conflicts by lowest transaction id.
- **ack_share** uses exact fractions to detect when an asynchronous call tree has completed.
- **Exactly-once** (Lemma 7.1) comes from replaying input against a snapshot.
- **Measured:** an order of magnitude faster than Beldi and Boki.

**C10. Spenger, Huang, Haller, Carbone, "Portals: A Showcase of Multi-Dataflow Stateful Serverless."**
PVLDB 16(12) demo, 2023. https://www.vldb.org/pvldb/vol16/p4054-spenger.pdf · `spenger-portals-2023.txt` ·
SKIMMED [lane C].
- Request/reply as a future plus a continuation over epoch-snapshotted dataflow state.

## D. Image, event-sourced and persistent systems

**D1. Yarvin, Monk, Dyudin, Pasco, "Urbit: A Solid-State Interpreter."** Whitepaper, 2016.
https://media.urbit.org/whitepaper.pdf · `yarvin-urbit-solid-state-interpreter-2016.txt` · READ §1–4, 6.4–6.5,
8, 9.6–9.9, 10.7, 11–13 [lane B].
- **Events are atomic.** "an interrupted event never happened". A crash report replaces the step.
- **End-to-end acks.** A negative ack is a committed fact.
- **A warning about promises.** Promises in state make upgrade "unnecessarily interesting".
- **Upgrade continues conversations.** An upgrade "continues all its conversations".

**D2. Urbit Docs, "Arvo" and Core Academy "Arvo I: The Main Sequence" (ca03), 2026.**
https://docs.urbit.org/urbit-os/kernel/arvo, https://docs.urbit.org/build-on-urbit/core-academy/ca03 ·
`urbit-arvo-doc.txt`, `urbit-docs-build-on-urbit-core-academy-ca03-2026.md` · READ [lane B; quote verified by me].
- **Persist, then act.** An event's effects are computed, persisted, and only then applied.
- **Urbit is moving from depth-first to breadth-first move order** (PR #6775): "breadth-first ordering
  guarantees that moves will be processed in the order they are emitted. Depth-first ordering constantly
  violates this, and in the presence of reentrancy this can cause extremely unexpected results."

**D3. Smith, Kay, Raab, Reed, "Croquet: A Collaboration System Architecture."** VPRI TR-2003-002.
https://tinlizzie.org/VPRIPapers/tr2003001_croq_collab.pdf · `smith-croquet-2003.txt` · READ; with the Croquet OS
docs `croquet-os-docs-2_*` · READ [lane B].
- **TeaTime (2003).** Pseudo-time plus a contingent two-phase commit.
- **Croquet today.** A reflector sequencer, simulation time that advances only on ticks, `future(ms)`
  sends, and snapshot plus replay of the tail.
- **The trajectory itself is evidence.** Contingent multi-party commit gave way to ordered deterministic
  replay.

**D4. Reed, "Naming and Synchronization in a Decentralized Computer System."** MIT/LCS/TR-205, 1978 · `reed-naming-synchronization-1978.pdf`
(a scan) · READ for OCR'd pp. 59–66, 73–80, 105–108 only [lane B].
- **Versions and pseudo-time.** Objects are sequences of immutable versions named by pseudo-time.
- **Possibilities.** A *possibility* is a write-once, three-state (wait/complete/abort) commit record with
  a default-abort timeout.
- **Tokens** are tentative versions, visible only under the same possibility.
- **For Mini:** a possibility is a cell whose law is difference logic.

**D5. Rideau (Faré), *Houyhnhnm Computing*, ch. 2, 5, 8, 10 (2015–16).** https://ngnghm.github.io/ ·
`houyhnhnm-ch2-save-our-souls.txt`, `houyhnhnm-ch5-non-stop-change.txt`, `houyhnhnm-ch8-ipc.txt`,
`houyhnhnm-ch10-vs-martians.txt` · READ [lanes B, F].
- **Upgrade** is a composable, atomic transaction with a typed, *linear* upgrade function and explicit
  drops (ch. 5).
- **Meta-level.** Servers and transactions belong to a meta-program (ch. 8).
- **Frozen deterministic semantics** are justified only to "replay and verify other random people's
  computations" (ch. 10). That is exactly Mini's admission.

**D6. Atkinson, Morrison, "Orthogonally Persistent Object Systems."** VLDB J. 4(3), 1995 ·
`atkinson-op-object-systems-1995.txt` · SKIMMED [lane B]. **Dearle, Kirby, Morrison, "Orthogonal
Persistence Revisited."** ICOODB 2009, arXiv:1006.3448 · `dearle-orthogonal-persistence-revisited-2010.txt` ·
SKIMMED [lane B].
- **Visibility time is the knob** (CACS): commit-time visibility gives atomic transactions; immediate
  visibility gives synchronisation.
- **Hyper-code.** Evolution works only if closures are *reachable* by migration code.

**D7. Landau, "The Checkpoint Mechanism in KeyKOS."** IWOOOS 1992 · `landau-keykos-checkpoint-1992.txt` · READ
[lane A2]. **Shapiro, Smith, Farber, "EROS: a fast capability system."** SOSP 1999, doi:10.1145/319151.319163
· `shapiro-eros-fast-1999.txt` · READ §1, 2.1, 3.4–3.5 [lane A2]. **Shapiro, Adams, "Design Evolution of the
EROS Single-Level Store."** USENIX ATC 2002 · `shapiro-eros-sls-evolution-2002.txt` · READ parts [lane A2].
- **Whole-system checkpoint.** Every page and node is checkpointed, including half-finished processes.
- **Check before commit.** A consistency check runs before commit: "Once committed, an inconsistent
  checkpoint lives forever."
- **Journaling** is allowed for data, never for capability nodes.
- **No in-kernel continuations.** A stalled kernel operation restarts from scratch.
- **The upgrade lesson** (KeyKOS §8.2): the program must be separated from its data "in advance".

**D8. Wu, Dong, Mo, Chen, "TreeSLS."** SOSP 2023. doi:10.1145/3600006.3613160 · `wu-treesls-2023.txt` · SKIMMED [lane B].
- The capability tree is the whole-system state; it is checkpointed in about 100 µs.
- **External synchrony.** Externally visible output is delayed until a checkpoint is taken.

## E. Blockchain object models and their call and concurrency semantics

**E1. Grossman et al., "Online Detection of Effectively Callback Free Objects with Applications to Smart
Contracts."** POPL 2018, arXiv:1801.04032 · `grossman-ecf-callback-free-2018.txt` · READ [lane D].
- **ECF** means a run is equivalent to some callback-free run.
- **Decidability.** Undecidable in general (Thm 6.1); decidable for finite-state objects (Thm 6.6).
  Checkable online in O(nm²) (Thm 8.13).
- **Measured on Ethereum history.** 81M executions, 3,315 non-ECF (0.004%), "only 10 executions out of
  about 100 million were legitimately non-ECF". The rest are DAO-style attacks.
- **Modular checking.** Thm 7.1: under ECF, a most-general havoc client is sound for checking an object
  on its own.

**E2. Tezos: "Michelson: the language of Smart Contracts in Tezos" (Octez docs) and Allombert, Bourgoin,
Tesson, "Introduction to the Tezos Blockchain."** HPCS 2019, arXiv:1909.08458 · `tezos-michelson-doc.txt` READ
(semantics sections), `allombert-tezos-2019.txt` SKIMMED [lane D].
- **Contracts return their operations.** A contract has type `(pair 'arg 'global) → (pair (list operation)
  'global)`: it returns the operations to emit plus its new storage. This is Mini's "method returns a
  Plan".
- **Atomicity.** The whole operation tree is atomic, depth-first, and "any contract calls emitted by a
  contract C are executed after contract C successfully finishes".

**E3. Nomadic Labs et al., "Tezos calling convention migrating from Breadth-First to Depth-First Order
(BFS to DFS)."** Tezos Agora forum, Mar–Jun 2021 · `tezos-florence-bfs-dfs-forum.txt` · READ [lane D;
quotes verified by me].
- **Why they switched to depth-first:** "the BFS convention typically provides few useful guarantees".
  Mixed conventions were rejected because "subtle bugs were frequently found".
- **Serokell's audit** found new flash-loan and oracle orderings, and a continuation-passing "view"
  callback hijack that worked through sender-based authority.

**E4. DFINITY, "The Internet Computer Interface Specification," "Properties of message executions on
ICP," "Security best practices: Inter-canister calls," 2025.**
https://internetcomputer.org/docs/references/ic-interface-spec · `dfinity-ic-interface-spec-2025.md`,
`dfinity-docs-message-execution-properties-2025.md`, `dfinity-docs-security-inter-canister-calls-2025.md` ·
READ (named sections; docs in full) [lanes D, F].
- **Every `await` is a commit point.** A trap rolls back only the current callback.
- **The consequences:** time-of-check/time-of-use bugs, double spends, leaked locks, `SYS_UNKNOWN`
  outcomes, deadlock on call cycles.
- **Upgrade.** A canister with a pending callback cannot be cleanly stopped or upgraded.
- **This is the cautionary tale for Residents.**

**E5. Bernauer et al., "Daml: A Smart Contract Language for Securely Automating Real-World Multi-Party
Business Workflows."** arXiv:2303.03749 (2023) · `bernauer-daml-2023.txt` · READ [lane D].
- **Exercise trees.** A command is one atomic tree of create, exercise and fetch actions.
- **Non-transitive authority.** An exercise's consequences are judged with authority = signatories ∪
  controllers, *not* the ambient authority. "Delegation not being transitive is a deliberate design
  choice."
- **Arguments are first-order.**

**E6. Chakravarty et al., "The Extended UTXO Model."** WTSC 2020, LNCS 12063 ·
`chakravarty-eutxo-2020.txt` · READ [lane D].
- **Validators judge the whole spending transaction.** A Constraint Emitting Machine's `step` is run off
  chain, and the validator only checks the proposed next state.
- **Bisimulation** with the ledger, mechanised in Agda.
- **A gap:** "no notion of initial state", so creation needs its own law.

**E7. Gelashvili et al., "Block-STM."** PPoPP 2023, arXiv:2203.06871 · `gelashvili-block-stm-2022.txt` ·
READ §1–6 [lane D].
- **Mechanism.** A preset order, a multiversion map and ESTIMATE markers. No read/write sets are needed in
  advance.
- **Determinism.** Corollary 2: the output equals sequential execution.
- **Measured.** 17–21× speedup on 32 threads. At most 30% overhead when the workload is fully sequential.
  "A single location for gas updates could make any block inherently sequential."

**E8. Blackshear et al., "Sui Lutris: A Blockchain Combining Broadcast and Consensus."** CCS 2024,
arXiv:2310.18042 · `blackshear-sui-lutris-2023.txt` · READ [lane D].
- **Owned objects** take a consistent-broadcast fast path. **Shared objects** take consensus, with versions
  assigned deterministically after ordering.
- **Equivocation** locks an object until the epoch ends.
- **In production** 64% of transactions use the fast path, but only 1–2% on DeFi days.

**E9. Sridhar, Sonnino, Kokoris-Kogias, "Stingray: Fast Concurrent Transactions Without Consensus."**
arXiv:2501.06531 (2025) · `sridhar-stingray-2025.txt` · SKIMMED (§1–4.2 read) [me].
- **BFT bounded counter.** Each validator gets a signing budget ηBal₀ with η = (f+1)/(2f+1). Version
  updates rebalance the budget, so the full balance takes O(log Bal₀) synchronisations.
- **FastUnlock** clears equivocation locks within consensus latency.
- **Measured:** 20,000 tps against 2 tps on a commutative workload.

**E10. Solana, "Sealevel — Parallel Processing Thousands of Smart Contracts" (2019)** · `solana-sealevel.txt` ·
READ [lane D]. **Anjana, Ravi, Herlihy, "Blockchain Transaction Conflicts: A Historical Perspective,"**
arXiv:2505.05358 · `conflicts-ethereum-solana-empirical-2025.txt` · SKIMMED [lane D].
- **Sealevel** requires read/write sets declared up front.
- **Measured conflicts.** Ethereum: 63% of transactions independent. Solana: 8% independent, with
  write-write conflicts about 76% of all conflicts.
- The comparison is not like-for-like, but coarse declared write locks clearly over-serialise.

**E11. Blackshear, Dill, Qadeer, Barrett, Mitchell, Padon, Zohar, "Resources: A Safe Language Abstraction
for Money" (Move).** arXiv:2004.05106 · `blackshear-move-resources-2020.txt` · READ §1–3, 5–8 [lane D].
- **Resource safety** is Thm 5.10.
- **No dynamic dispatch.** Move moves "the dynamism to the withdrawal code … instead of the recipient
  code", which is the capability answer to callback hijack.

**E12. NEAR docs, "Cross-Contract Calls" and "Private Callbacks"; Burnik (Sigma Prime), "NEAR Sharding &
Cross Contract Calls" (2024).** https://docs.near.org/smart-contracts/anatomy/crosscontract ·
`near-crosscontract-doc.txt`, `near-callbacks-security.txt`, `near-sigmaprime-xcc.txt` · READ [lane D].
- **No rollback.** Calls are asynchronous; the callback runs 1–2 blocks later, and "there's no automatic
  rollback".
- **Forged callbacks** are possible unless the callback is `#[private]`.
- **Racing a callback:** calling `stake()` twice before the first callback lands yields 400 tokens for
  100 NEAR.

**E13. Yanovich et al., "From Paradigm Shift to Audit Rift."** arXiv:2509.10823 (TON) · `ton-audit-rift-2025.txt` · READ §1–6 [lane D].
- **Scope:** 233 vulnerabilities across 29 asynchronous-actor projects.
- **Failure classes:** stale reads across hops, racing messages, and bounce handlers that restore a
  snapshot and so erase interleaved credits.
- **Compensations must be deltas.**

**E14. Androulaki et al., "Hyperledger Fabric."** EuroSys 2018, arXiv:1801.10228 ·
`androulaki-hyperledger-fabric-2018.txt` · READ §2.4, 3, 4.4 [lane D].
- **Execute, order, validate.** Endorsement policies are fixed and cannot be modified by untrusted
  developers. Validation is an MVCC read-set check, with phantom checks by re-execution.
- **Earlier lesson (v0.6).** Nondeterministic chaincode diverged the state.

**E15. Al-Bassam, Sonnino, Bano, Hrycyszyn, Danezis, "Chainspace."** NDSS 2018, arXiv:1708.03778 ·
`albassam-chainspace-2017.txt` · READ §I–V-A, VIII [lane D].
- **Procedures and checkers.** Procedures run on the client; *checkers* validate their traces depth-first.
- **S-BAC** is a sharded atomic commit: per-shard BFT, objects locked from prepare to accept.
- Later work reports replay attacks on cross-shard messages (INFERRED, from Sui's reference).

**E16. Dickerson, Gazzillo, Herlihy, Koskinen, "Adding Concurrency to Smart Contracts."** PODC 2017,
arXiv:1702.04467 · `dickerson-adding-concurrency-smart-contracts-2017.txt` · READ §1, 3–4 [lane D].
- **The miner** publishes a happens-before graph.
- **Validators** replay it in parallel and reject a block whose lock trace differs.
- **Undo** is through inverse logs, i.e. delta compensation.

**E17. Kniep et al., "Pilotfish."** arXiv:2401.16292 · `kniep-pilotfish-2024.txt` · READ §1–4, 6 [lane D].
**Sergey, Kumar, Hobor, "Scilla."** arXiv:1801.00687 · `sergey-scilla-2018.txt` · READ §1–2 [lane D].
- **Pilotfish** gives per-(object id, version) queues for distributed execution.
- **Scilla** transitions end in sends. A non-tail call becomes an explicit continuation that the
  environment keeps on a stack (defunctionalised CPS), which is the general form of Mini's Activity.

**E18. o1Labs, Mina documentation: "Account Updates," "Cross-Contract Calls," "Upgrading a zkApp"
(o1js 3, 2025–26).** https://docs.minaprotocol.com/zkapps/tutorials/cross-contract-calls ·
`mina-account-updates.txt`, `mina-cross-contract-calls.txt`, `mina-upgrading-zkapp.txt` · READ [me].
- **Synchronous, value-returning calls.** A call adds "a separate account update for the Incrementer
  account, with its own proof, as a child", and "the network makes sure that the value is the same one
  that the Incrementer proof returned". The tree is atomic.
- **Preconditions** are attached to each update.
- **An upgrade hazard.** State is positional ("eight field elements in a fixed order"). Reordering two
  declarations turns a balance into a counter: "Nothing fails. There is no error."

## F. Deterministic parallelism, deterministic transactions, coordination freedom

**F1. Abadi, Faleiro, "An Overview of Deterministic Database Systems."** CACM 61(9), 2018.
doi:10.1145/3181853 · `abadi-deterministic-db-overview-2018.txt` · READ [lane E].
- **No deadlocks.** A crash replays to the same state.
- **Commit protocol.** "the only thing a commit protocol must check is whether there was any node that
  executed code that could deterministically cause an abort." Votes are one-way, and only from
  participants that could abort.

**F2. Thomson et al., "Calvin."** SIGMOD 2012. doi:10.1145/2213836.2213838 · `thomson-calvin-2012.txt` · READ
[lane E].
- **Ordering inputs.** A sequencer orders inputs; deterministic locking then runs them.
- **Unknown footprints** are handled by OLLP reconnaissance.
- **Measured:** 500K TPC-C tps on 100 nodes. Paxos across continents changed latency, not throughput.

**F3. Faleiro, Abadi, "Rethinking Serializable Multiversion Concurrency Control" (Bohm).** PVLDB 8(11),
2015 · `faleiro-bohm-2015.txt` · READ §1–4 [lane E].
- **Placeholders.** Write-set placeholders are inserted before execution.
- **Reads never block writes.** Write-write conflicts never abort.
- **Aborts do not cascade.** An abort fills the placeholder with the predecessor's value.

**F4. Lu, Yu, Cao, Madden, "Aria: A Fast and Practical Deterministic OLTP Database."** PVLDB 13(11), 2020 ·
`lu-aria-2020.txt` · READ §1–7 [lane E].
- **Execution.** Every transaction in a batch reads the same snapshot. Write reservations follow, and
  losers are deferred to the next batch.
- **The cost.** The semantics depend on batch boundaries, and one 20 ms straggler costs 81%.

**F5. Hong et al., "A Hybrid Approach to Integrating Deterministic and Non-deterministic Concurrency
Control" (HDCC).** PVLDB 18(5), 2025 · `hong-hybrid-deterministic-2025.txt` · SKIMMED [lane E].
- **A warning.** A nondeterministic OCC lane forces the realised order into the log, because input logs
  no longer determine the state.

**F6. Hellerstein, Alvaro, "Keeping CALM: When Distributed Consistency Is Easy."** CACM 63(9), 2020,
arXiv:1901.01930 · `hellerstein-keeping-calm-2019.txt` · READ [lane E].
- **CALM** (Thm 1): coordination-free and consistent iff monotone.
- **Examples.** Deadlock detection is monotone; garbage collection is not.

**F7. Bailis et al., "Coordination Avoidance in Database Systems."** PVLDB 8(3), 2014, arXiv:1402.2237 ·
`bailis-coordination-avoidance-2014.txt` · READ §1–9, App. B–C [lane E].
- **I-confluence** (Thm 1) is the iff condition for coordination freedom.
- **Counters (Claims 11–14).** `x>k` under increment: yes. `x>k` under decrement: no. `x<k` under
  increment: no. `x<k` under decrement: yes.
- **Other claims.** Uniqueness of a chosen value: no. Foreign key under delete: no. Set containment: yes.
- **Escrow** is the amortised exit.

**F8. Gotsman, Yang, Ferreira, Najafzadeh, Shapiro, "'Cause I'm Strong Enough" (CISE).** POPL 2016.
doi:10.1145/2837614.2837625 · `gotsman-cise-2016.txt` · READ §1–6.4 [lane E].
- **Tokens.** Operations that acquire conflicting tokens must be ordered. The rule requires causal
  consistency.
- **Examples.** Bank withdraw takes a self-conflicting token. In the auction, close conflicts with bids,
  but bids do not conflict with each other.

**F9. Shapiro, Bieniusa, Preguiça, Balegas, Meiklejohn, "Just-Right Consistency."** arXiv:1801.06340 ·
`shapiro-just-right-consistency-2018.txt` · READ [lane E]. **Laddad et al., "Keep CALM and CRDT On"**
(PVLDB 16(4)) and **"Flo"** (POPL 2025) · `laddad-*.txt` · SKIMMED [lane E]. **Cheung et al., "New
Directions in Cloud Programming"** (CIDR 2021) · `cheung-hydro-new-directions-2021.txt` · SKIMMED [lane E].
- **Bounded counter by escrow.**
- **Threshold queries** are the only reads that are safe on a lagging replica.
- **Flo:** block only on *bounded* sources.
- **Hydro:** consistency is declared per handler.

**F10. Lohstroh, Lee, "Deterministic Actors"** (FDL 2019) · READ; **Lee, "Logical Time in Actor
Systems"** (Agha Festschrift, 2025) · READ §1–4; **Menard et al., "High-Performance Deterministic
Concurrency using Lingua Franca"** (TACO 2023, arXiv:2301.02444) · SKIMMED · `lohstroh-*`, `lee-*`,
`menard-*` [lane E].
- **Hewitt actors are nondeterministic** even over FIFO links.
- **Reactors** process messages in timestamp order; an absent input at a tag is definite.
- **The CAL theorem:** consistency at a logical time costs availability, as a function of latency.
- **For Mini:** time to await is a tag (a block height), and a timed-out await gets a typed fault branch.

## G. Multi-party atomicity across domains

**G1. Herlihy, Liskov, Shrira, "Cross-chain Deals and Adversarial Commerce."** PVLDB 13(2), 2019,
arXiv:1905.09743 · `herlihy-cross-chain-deals-2019.txt` · SKIMMED (§1–4, the timelock and CBC protocols,
the theorem statements) [me].
- **Deals are not transactions.** Safety means every compliant party ends with an acceptable payoff
  (Property 1). Weak liveness: no compliant asset escrowed forever (Property 2).
- **Escrow is the concurrency control.**
- **Two protocols.** The timelock protocol is decentralised and synchronous (Thms 1–3). The CBC protocol
  records ordered commit and abort votes on one certified ledger. The authors sketch a proof that any
  semi-synchronous deal protocol needs "a single ledger consulted by all parties".

**G2. Herlihy, "Atomic Cross-Chain Swaps."** PODC 2018, arXiv:1801.09515 ·
`herlihy-atomic-cross-chain-swaps-2018.txt` · SKIMMED (abstract, Thm 3.5) [me].
- Hashlock plus timelock swaps over a digraph. A uniform protocol is atomic iff the digraph is strongly
  connected. Time is O(diam).

**G3. Zakhary, Agrawal, El Abbadi, "Atomic Commitment Across Blockchains" (AC3WN).** arXiv preprint 2019 (venue from memory: PVLDB 13(9), 2020; not verified),
arXiv:1905.02847 · `zakhary-atomic-commitment-across-blockchains-2019.txt` · SKIMMED [me].
- **The problem with timelocks.** An expired timelock breaks all-or-nothing for a participant that merely
  crashed.
- **The fix.** The commit decision is recorded on a *witness network* (another blockchain), whose
  decision unlocks each side.

**G4. Goes, "The Interblockchain Communication Protocol: An Overview."** arXiv:2006.15918 (2020) ·
`goes-ibc-2020.txt` · SKIMMED [me].
- **Verification.** Light clients that require finality.
- **Channels.** Ordered or unordered, always exactly-once. Packets carry `timeoutHeight` and
  `timeoutTimestamp`, and the sender runs its timeout logic atomically with the timeout proof.
- **Transfers.** Cross-ledger value moves by "transitory escrow and a sequence of packets".

**G5. Keidar, Naor, Poupko, Shapiro, "Cordial Miners."** DISC 2023, arXiv:2205.09174 ·
`keidar-cordial-miners-2022.txt` · SKIMMED (abstract, introduction) [me].
- A DAG ("blocklace") Byzantine atomic broadcast. It is about ordering only and does not bear on call
  semantics.
- Bread ordered with it and still executed serially.

## H. Evolution: live upgrade with in-flight work

**H1. Hicks, Nettles, "Dynamic Software Updating."** TOPLAS 27(6), 2005. doi:10.1145/1108970.1108971 ·
`hicks-dynamic-software-updating-2005.txt` · READ [lane F].
- **The patch.** A patch is (code, state transformer, stubs). Changed types are renamed by hash. The stack
  is not transformed.
- **When to update.** Updates happen at program-chosen points. Any exception means atomic rollback.
- **Lazy migration rejected** because errors after partial use are unrecoverable.

**H2. Hayden, Saur, Smith, Hicks, Foster, "Kitsune."** TOPLAS 36(4), 2014 · `hayden-kitsune-2014.txt` · READ
§1–4, 6.2, 7–8 [lane F]. **Hayden, Magill, Hicks, Foster, Foster, "Specifying and Verifying the Correctness of
Dynamic Software Updates."** VSTTE 2012 · `hayden-dsu-correct-2012.txt` · READ [lane F].
- **Kitsune:** named update points under full quiescence; control migration to the same-named point.
- **xfgen** rejects a spec that does not cover every changed type.
- **The standing test** is a self-update (A→A).
- **Client-oriented specs** replace equivalence as the correctness notion, because equivalence forbids
  bug fixes.

**H3. Bläser, Russo, Greif, Vandersmith, Ibrahim, "Smarter Contract Upgrades with Orthogonal Persistence."**
VMIL 2024. doi:10.1145/3689490.3690401 · `dfinity-smarter-upgrades-op-2024.txt` · READ [lane F]. **Motoko docs:
stable types, enhanced multi-migration, orthogonal persistence, 2025** · `motoko-*-2025.md` · READ [lane F].
- **The compatibility check runs twice:** statically, and "dynamically, as part of the upgrade
  transaction … causes the upgrade to roll back".
- **Continuations awaiting calls are transient** and are dropped.
- **Since v0.14.6, dropping fields is forbidden.**
- **Migration chains** are typed `{in}→{out}` modules.
- **Pre-upgrade hooks are deprecated:** one that traps leaves the canister stuck.

**H4. DFINITY upgrade docs (canister management, security best practices for upgrades), 2025** ·
`dfinity-docs-canister-management-upgrade-2025.md`, `dfinity-docs-security-canister-upgrades-2025.md` ·
READ [lane F].
- **Drain or kill.** A canister must be stopped first "to wait for all outstanding callbacks", or
  uninstalled, which synthesises rejects.
- **Drains can stall.** A stalled callee makes a canister un-upgradable.
- **Timers die silently** on upgrade.

**H5. Erlang/OTP, "Compilation and Code Loading" and "Release Handling."** erlang.org/doc ·
`erlang-code-loading.txt`, `erlang-release-handling.txt` · READ §14, §11.1–11.6 [lane F].
- **Two live versions.** Fully qualified calls go to the current version, while lingering processes stay
  on the old one.
- **The new version owns `code_change`.**
- **soft vs advanced** upgrades, and **soft_purge vs brutal_purge**.
- **The mailbox hazard.** Old-format messages wait in a suspended process's mailbox.

**H6. Salehi, Clark, Mannan, "Not so immutable: Upgradeability of Smart Contracts on Ethereum."**
arXiv:2206.00716 (2022) · `salehi-not-so-immutable-2022.txt` · READ [lane F]. **Chen et al., "Proxion"**,
arXiv:2409.13563 · READ parts. **Wang et al., "The Dark Side of Upgrades"**, arXiv:2508.02145 · READ §1–6.
**Liu et al., "Demystifying the Characteristics for Smart Contract Upgrades"**, arXiv:2406.05712 · READ
§1–4 [lane F].
- **Who controls upgrades.** 48% of 8,225 upgradeable systems sit behind a single externally owned key.
- **Hidden proxies.** 19.6M proxies; 99.7% never upgraded.
- **Collisions.** 1.57M function-collision pairs and 3,022 storage-collision pairs.
- **Losses.** 37 incidents over $400M. Key theft and malicious injection account for 14 incidents and
  about $115M.
- **Broken callers.** 4,334 ABI breaking changes broke 584 real transactions.

**H7. Unison Computing, "The big idea."** https://www.unison-lang.org/docs/the-big-idea/ ·
`unison-big-idea.txt` · READ [lane F].
- **Definitions are identified by hash.** Names are metadata. Upgrade re-points names.
- **Durable values include functions.** "deserialization will always yield a value that has the same
  meaning".

**H8. Litt, van Hardenberg, Henry, "Project Cambria: Translate your data with lenses."** Ink & Switch, 2020.
https://www.inkandswitch.com/cambria/ · `cambria-inkandswitch.txt` · SKIMMED [me].
- **Mechanism.** A graph of schemas connected by bidirectional lenses. Each lens produces a translator,
  types and a JSON Schema.
- **The trade-off.** Interoperability trades off "irreconcilable design goals".
- **Scope.** Lenses translate data, not control.

**H9. Ungar, Smith, "Self" (HOPL III, 2007).** `ungar-self-hopl-2007.txt` · SKIMMED [lane F].
- Self's `define` was "inspired by, but not quite the same as, Smalltalk's 'become:'".
- The semantics of `become:` (swapping identities across the heap) are INFERRED; the text does not give
  them.

---

# Part II — Where the sources disagree, and where I differ from the sibling scholars

1. **Call order inside one atomic unit: depth-first or breadth-first?** The two deployed precedents went
   opposite ways, and both quotes are verified.
   - **Tezos** moved from breadth-first to depth-first in Florence because breadth-first "provides few
     useful guarantees" (E3).
   - **Urbit** is moving from depth-first to breadth-first because depth-first "constantly violates" the
     order in which moves were emitted "in the presence of reentrancy" (D2).
   - **Resolution: they optimise different things.** Depth-first gives *call/return* semantics. Breadth-first
     gives *message* semantics (E's queue is breadth-first). Both reported that *mixing* the two is where
     bugs live ("subtle bugs were frequently found", E3; the Urbit text records a dissent that "moves
     [can be used] essentially as function calls").
   - **So Mini should have two mechanisms, not one order.** Synchronous calls run depth-first on a call
     stack inside the turn. Eventual sends go to per-target FIFO queues and are each delivered as their
     own turn (III.1). This sharpens LAWS idea 3 and OS §2, which treat in-turn calls and sends as points on
     one scale.
2. **Is pipelining worth anything on one Host?** Agoric leaves kernel pipelining off for all local vats,
   because early delivery to the deciding vat buys nothing locally (A10). Lane A1 argues it saves the
   caller signed, paid, checkpointed resume turns.
   - **Resolution: both are right about different halves.** *Sending to an unresolved answer slot* (the
     message waits at the slot and is forwarded inside the resolving turn) is what spares the caller a turn
     per hop. Mini needs that within a domain.
   - *Early delivery to the decider* is a network-latency optimisation. Mini needs it only across domains.
   - **Against OS §2,** pipelining is not cross-domain only; the half that cuts turns matters within a
     domain too.
3. **Footprints: declared or learned?** OS §3 wants invocations to declare read/write sets. Lanes D and E
   found the opposite evidence:
   - Block-STM matches declared-set systems *without* declaration, and degrades to at most 30% overhead
     (E7).
   - Solana's coarse declared write locks leave only 8% of transactions independent (E10).
   - Mini's admission already *computes* the exact footprint by re-execution, which Orleans has to
     approximate with a reconnaissance run (B3).
   - **Resolution:** footprints are learned; declarations are only scheduling hints (III.5).
4. **Must continuation checkpoints be short-lived?** OS §1 says yes, citing Electric Communities, PJama,
   Motoko and Urbit. On my reading those failures had two causes:
   - **(a) Code identity changed under the continuation.** Unison and Mini's pinned package hash remove
     this: an old continuation of hash-pinned code stays meaningful (H7).
   - **(b) The continuation held a mutable view of state that migration then changed.**
   - **Resolution:** remove (b) with a capture rule (Pony's val/iso/tag; III.4). Checkpoints may then live
     as long as their await does, and upgrade needs a *disposition* per activity, not a time limit. OS and
     I agree on the dispositions themselves (drain, replay, map, abort).
5. **Cross-domain atomicity.**
   - The positions: Bread wants "2PC with escrow", OS wants "never an implicit 2PC; a purposeful cell",
     Lane B proposes Reed's possibility cell, and Lane D proposes S-BAC.
   - These are one design seen from four sides. Herlihy–Liskov–Shrira sketch a proof that a
     semi-synchronous deal *needs* one ledger that every party consults (G1), and AC3WN (G3) independently
     uses a witness chain.
   - Escrow moves each party's rights into that one ledger, which is Zoe and Miller's escrowExchange
     (A12, A13). Phase 2 then cannot fail, so no participant ever blocks the way Argus did (A1 §24.3).
   - **Resolution:** the "purposeful cell" *is* the deal ledger, and the escrow deposit *is* the prepare
     (III.7).
6. **Re-entry inside a turn.** LAWS idea 3 proposes a dynamic ECF check. Grossman's data (E1) supports
   something simpler as the default: refuse re-entry into any object already on the turn's call stack.
   Only 10 of roughly 100M Ethereum executions were legitimately non-ECF. Keep the full ECF check as an
   opt-in for objects whose law declares it.
7. **Checking BREAD's findings against the literature.**
   - **"Eager shape, lazy witness": supported, across domains.** It is what escrow and offers do (Zoe's
     give/want; Herlihy's escrow precondition). Within one domain it is unnecessary: Block-STM-style
     admission does not need shapes fixed in advance. Bohm's placeholders are the in-domain version, and
     they pay for it with declared write sets (F3).
   - **"Await id spent like a nullifier": strongly supported.** Khan's CO-c and the finding that only a
     read/decide-point claim works (C6); Agoric's linear decider (A10); Voss's ownership (A9); Restate's
     attempt fencing (C7).
   - **"Typed waits with cascade and deposits": supported.** E's broken-promise contagion (A1); NEAR's
     reserved callback gas (E12); IC's `SYS_UNKNOWN` as a typed outcome (E4); IBC's timeout heights (G4).
   - **"Per-law coordination grades": supported,** with an exact rule for difference logic (III.6).

---

# Part III — Synthesis: eight ideas to build into Mini, ranked

The literature does not contest Mini's spine: re-execute, apply the Plan atomically, and let every touched
law judge it. It contests four seams:
- how a turn reaches another object;
- what may happen between an activity's yield and its resume;
- how independent turns run together;
- what an upgrade does to suspended work.

Costs below are INFERRED and given in module counts.

**1. Two call forms with two orders, never one mixed mechanism (fork 1).**
- **`call`** is synchronous, inside the turn, and returns a value:
  - The callee runs its own pinned package against the turn's snapshot and returns (value, Plan
    fragment). This is Mina's child account update, with re-execution in place of a proof (E18).
  - Fragments apply depth-first in call order (Tezos, E2).
  - Each fragment is judged with Daml's non-transitive authority: the callee's law and owners plus that
    node's controllers, never the caller's ambient signers (E5).
  - The kernel refuses re-entry into any object already on the stack (E1). An ECF check can be added
    later as an opt-in.
  - If one frame wrote a different version of a cell than another frame read, the whole turn aborts
    (Orleans context union, B3).
- **`send`** is eventual. It is a Plan action that enqueues on a per-(sender, target) FIFO, and each
  delivery is its own paid turn, processed breadth-first (E's queue, A1; Urbit, D2).
- Cost: a call stack, a re-entry guard, a per-frame authority context, and an inbox cell. Two to three
  modules.

**2. Kernel promises with deterministic answer slots (forks 1, 3).**
- A send creates an answer slot whose identity is H(turn, call site) (Ozone, A8). It has exactly one
  decider (A10, A9).
- Sends to an unresolved slot queue there and are forwarded *inside the resolving turn*. Every resolution
  then takes the same path, so E-order is free and no embargo is needed (A5).
- Breakage is contagious and refunds postage (A1 §16.5).
- The kernel breaks slots whose decider is gone, and refuses awaits that would close a cycle. Awaits are
  declared, so cycles are decidable.
- Cross-domain handoff and embargo come later (A4, A5).
- Cost: one module.

**3. The resume contract as a kernel theorem (forks 1, 4, 5).**
- The checkpoint is the authority. Replay and stored state are bisimilar for fixed code (C1, Thm 6.4), and
  a root chain plus signed inputs is already log-optimal (C5). Replay only pays without a codec.
- State Khan's properties as Lean invariants: PC, EO, CO-c/CO-e, CV, RD and FI, plus liveness (C6).
- CO-c is a compare-and-swap on (activity, ordinal, checkpoint hash) at admission's read/decide point.
  That is the only place Khan's repair worked; write-path repairs failed twice.
- Awaits resolve to `Reply | Refused(explanation) | Unknown | TimedOut | Broken | Upgraded` (E4, A1).
- Outbound effects wait for commit (A16, A10, D8). External effects use deterministic outbox ids.
- Two more obligations:
  - Prove the codec is cost-transparent, as the liveslots incident shows is needed (A10).
  - Type-check every checkpoint before the root moves (EROS, D7).
- Cost: one module plus a precondition field.

**4. Activities share their object only through committed cells (fork 3).**
- At a yield, a checkpoint may capture only:
  - **val**: snapshots, packages;
  - **iso**: resources moved in;
  - **tag**: send-only references.

  It may never capture a mutable alias of object state (Pony, B6).
- A resume revalidates the read versions it recorded (Fabric MVCC, E14; Reed pseudo-time, D4). If they are
  stale, it re-runs and returns a typed `Conflict`.
- Split object state into sub-cells, each with its own law. In SmSa, 80% of the time was spent waiting for
  whole-actor turns (B4).
- Exclusivity across a yield is never the default; Orleans' default is a lock resolved only by timeout
  (B2). An object that needs exclusivity uses a law-governed lease: "only H writes until height h".
- Cost: a qualifier check at yields plus read-version records.

**5. Deterministic parallel admission with Block-STM semantics (fork 3).**
- **Parallel phase.** Compute every turn's Plan against the batch snapshot and record which cells were
  forced. Laziness keeps these read sets small.
- **Sequential phase.** In log order, re-run any turn whose reads changed earlier in the batch. Then apply
  it, with every law judging the current state (E7, F2–F4).
- **The theorem.** The root equals the sequential fold (Block-STM Corollary 2), so auditors need only a
  single-threaded interpreter. Reject Aria's batch-dependent semantics (F4).
- **Contention.** Make delta actions first-class, and never route fees through one cell: "a single
  location for gas updates could make any block inherently sequential" (E7).
- **Replication.** Publish the dependency DAG so replicas can replay in parallel (E16).
- Cost: a multiversion map, a scheduler, and one refinement theorem.

**6. Coordination grades derived from laws (forks 2, 3).**
- **The rule.** For a law atom `a·x ≤ c`, actions with a·d ≤ 0 are I-confluent. Any action with a·d > 0
  needs ordering. This generalises Bailis Claims 11–14 (F7).
- **Tokens.** Those atoms get CISE tokens (F8).
- **One computation answers three questions:**
  1. Which activity pairs on an object commute.
  2. Which turns may bypass BFT ordering (owned or monotone objects: Sui E8, CALM F6).
  3. Which participants must vote in a cross-domain commit (Abadi, F1).
- Escrow and bounded counters are the exit when ordering is needed (F9). Stingray (E9) is needed only for
  a consensus-less mesh fast path.
- Cost: a conflict relation over clauses.

**7. Multi-party atomicity by escrow into one deal domain (fork 3).**
- **Within a domain:** one turn under Daml authority.
- **Across domains:**
  - A *deal cell* lives in a domain all parties accept. It is Reed's possibility (D4) and Herlihy's CBC
    (G1): write-once, with a timeout height and default abort as its law. Herlihy sketches why a
    semi-synchronous deal needs exactly such a single ledger.
  - Parties escrow rights into it by ordinary sends. This is a prepare that cannot fail later.
  - One turn in the deal domain checks offer safety (A13) and decides. Payouts and refunds then flow back
    as sends.
  - No party ever holds a lock while waiting on a coordinator, which is what Argus (A1) and Beldi (C3) do.
  - Bind every message to its session and sequence number, to prevent replay (S-BAC, E15). Timeout
    proofs follow IBC (G4).
- **Limit:** this covers transferable, exclusive rights. Arbitrary state needs *custody transfer*, a lease
  of the cell to the deal domain.
- Cost: a deal-cell law plus light-client verification.

**8. Upgrade as one governed turn with a total disposition (fork 4).**
- **Authority.** A law over the package-hash field, frozen by default, with timelock and quorum. Salehi
  finds 48% of systems sit behind a single key, and 14 of 37 losses were injections (H6).
- **Admission checks:**
  - stable-subtype compatibility, or a typed linear migration `Old ⊸ New` (H3, D5);
  - the cell's law re-judged on the migrated state;
  - the new interface is a supertype of the old one (A11).
- **Disposition.** Every live activity must get one, or the upgrade is refused:
  - **abort**, with `Upgraded`;
  - **continue-pinned**, which is sound because code is hash-pinned (H7) and checkpoints hold no mutable
    state (idea 4); this is Erlang's two-version model (H5);
  - **map** to a new yield label (Kitsune, H2);
  - **replay** the activity's `(Plan_i, R_i)` log on the new code, entering Failed on divergence (A11,
    C8).
- **Draining** has a height deadline (H4).
- **What this rules out.** Typed, named state plus kernel-held package pointers make Mina's positional
  corruption (E18) and Ethereum's storage and selector collisions (H6) impossible.
- Cost: a subtype judgement and a migration checker.

**How they fit.** Every edge is one admitted turn, built from the ideas above:
- A signed invocation is re-executed.
- `call`s build a depth-first tree under Daml authority.
- `send`s and awaits leave typed answer slots.
- Admission runs in parallel and commits as a sequential fold.
- Grades decide what needs ordering and who votes.
- The checkpoint commits with the Plan, under the resume contract.

Deals and upgrades are ordinary turns. The codec is what makes ideas 3, 4 and 8 exact rather than
replay-approximated.
