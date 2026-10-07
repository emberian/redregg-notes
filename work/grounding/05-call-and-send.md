# 05 — `call` (deferred writes, re-entry refusal) and `send` (inboxes, postage, forwarding)

Code: minidregg main `4ef4e808`, read only. Lane notes: `hbox:/tank/dregg-build/claude-lanes/ob8/STATUS.txt`
(OB7 and OB8 decisions with reasons). Open items 5.4 come from DEPUTY-OB-ENG's 2026-10-06 message (it is
not coding them because they change meaning). Literature: `lit/LIT-W3-calls-sends-contracts.md`.

## 1. Current design

**Call** (`Kernel/ObjectiveCall.lean`, header `:1-60`). An `invoke` turn calls one method of one object;
the method may synchronously call other objects' methods in the same turn, depth first, to `callDepth` 8.
- A method is a declaration of the object's **pinned** package, lowered by the kernel's own front end
  (`loadMethod`), of type `method(view: {version, state}, args: X) -> Activity<P, R, {result, write}>`,
  `P ⊆ {call, send}`, `R ⊆ {returned, queued}`. Every yield is answered in the same turn; a method whose
  Plan admits `await` is refused `notCallable` before running ("an Activity cannot be called").
- **Re-entry is refused, mandatorily**: `reentry_refused` (`:886`; a call whose target is on the stack
  errors `.reentry`), `invocation_reentry_free` (`:1217`; every frame stack of an admitted invocation is
  `Nodup`).
- **Writes are deferred to frame return**, applied to the frame's own object only, judged by that object's
  law on (the state the frame was shown, the new state) under that frame's facts:
  `invocation_writes_from_view` (`:1233`). The callee's view is the snapshot plus every write an earlier
  frame of this turn applied at its return. Two calls to one object compose in order.
- **Authority**: the root frame carries the signer; a nested frame carries the signer as `request/subject`
  only under a scoped grant `{object, method, uses}` of the invocation, spending one use (`grantSpent`).
  Without a grant every law atom reading the subject fails closed. `request/caller` names the calling object.
  Docstring names Daml's non-transitive delegation and Pact's scoped, counted capabilities (`:24-33`).
- **One declared envelope** for the tree (`runCounted`, proven equal to `runBounded`); exhaustion refuses
  the invocation and charges nothing.
- Reasons recorded by the lane (OB8 STATUS "DECISIONS + REASONS (OB7)"): per-frame law judgement because
  turn-end judgement "lets a granted later frame launder an ungranted earlier write"; apply-at-return +
  own-object writes + re-entry refusal ⇒ no frame-conflict abort needed; frames resume the machine's own
  yielded state, so calls need no `ForcingTransparent` premise. Evidence: journey C1–C8 51/51; a
  guard-removed mutant "commits the DAO (bank 40 / thief 60)" (MERGE-QUEUE.md line 225).

**Send** (`Kernel/ObjectiveSend.lean`, `Kernel/Inbox.lean`, `Kernel/AnswerSlot.lean`).
- A frame yields `send {to: object n | slot n, method, args}`, answered at once with `queued {slot}`; the
  message id `H(turn, index)` names its reply slot.
- The invocation declares `postage`, the envelope each message is delivered under; each send escrows its
  price into the purse of the queue holding it (`uncovered` otherwise).
- Inboxes are per-(sender, target) FIFO queues, bound `Inbox.bound = 16` (`Kernel/Inbox.lean:61`),
  `lawful_fifo` (`:146`), `reorder_unlawful` (`:172`); `queueFull`.
- `deliverMessage` (anyone) pops the head and runs the target's method as a root frame with
  `caller = sender` and **no subject**, paid from the inbox purse only
  (`MessageDelivery.debits_only_purse`, `Kernel/ObjectiveSend.lean:283`). It decides the reply slot, whose
  decider is the role `delivery m` (`decide_delivery_refused`, `Kernel/AnswerSlot.lean:251`). A failed
  delivery pops, decides `broken`, commits no write (`failed_delivery_pops`, `Kernel/ObjectiveSend.lean:333`).
- **Restricted pipelining**: a send to `slot n` (reply of an undelivered message) queues on that slot; the
  turn deciding the slot forwards it when the reply is an object reference, else refunds; a send onto the
  reply of a send that is itself only queued is refused `notPipelinable` (depth 1).
- Not built (`docs/OBJECTIVE-BEND-EVENTS.md` "Not built"): an activity yielding `call`/`send`; an activity
  awaiting a message; sends from a delivered message (refused as a failure); deeper pipelining; objects
  holding capabilities.

## 2. What it commits us to

1. **Synchronous calls across trust boundaries.** This is the root's OPEN 1 for Ember
   (`ROOT-PROGRAM-MODEL-DECISIONS-20261004.md:118-119`): "Synchronous cross-principal `call` at all, versus
   Agoric's 'never synchronous across trust boundaries'. Root's lean: yes, with Daml authority + scoped
   grants + mandatory re-entry refusal." Re-entry refusal is what makes this safe; its cost is unmeasured
   (root resolution D1: "the cost of refusing all re-entry is unmeasured. Keep the refusal and measure it on
   Mini's own cohorts").
2. **Refusing re-entry forbids callbacks**: observer patterns, a vault calling back a borrower (flash-loan
   shape), "A asks B, B asks A for a quote" all need either `send` or restructuring. SeRIF and ECF (below)
   are the two literatures on permitting *safe* re-entry.
3. **Views are snapshot+applied-earlier-writes, writes at return.** A caller's own pending write is
   invisible to its callees; a caller's decision computed from a callee's *returned value* can be stale by
   the time the caller's frame returns if a later sibling call changed the callee (INFERRED; the law judges
   only the caller's own object, so this is a correctness rather than a safety question).
4. **Send is asynchronous, FIFO per pair, bounded, prepaid.** Postage is fixed at send time; delivery by
   anyone; caller identity flows (`caller = sender`), subject authority does not.
5. **Answer slots unify replies and decisions**: one decider, one deadline, one terminal decision.
   Message reply slots have the role decider `delivery m`. (Delivery slots never expire today — OB-ENG item 2.)

## 3. Literature (verified by worker W3 against primary text; LIT-W3 has quotes and line numbers)

- **Miller 2006, *Robust Composition* (PhD thesis, JHU), §13.1 (plan interference), §14.1–14.2 (turns,
  vats), §16.2–16.5 (pipelining, datalock, broken-promise contagion), §19 (E-ORDER); Miller, Tribble,
  Shapiro 2005, "Concurrency Among Strangers", TGC, §7.1.** READ (LIT-W3 §1). E never banned synchronous
  calls: a turn *is* a synchronous call tree, but only among objects in one vat, for mutual exclusion without
  locks. Plan interference (nested publication, nested subscription, aborting the wrong plan) needs a callee
  running on the caller's live, mid-update heap. **Ours removes two of the three** (snapshot views + deferred
  writes; re-entry refusal) and **keeps "aborting the wrong plan"**: a callee's law refusal aborts the whole
  invocation. In code this is uncatchable by construction, since a frame's response type is
  `returned | queued` with no failure arm (`Kernel/ObjectiveCall.lean:60-63`; refusal `lawDenied`, `:461`).
  E's cure for that hazard is `send`. W3: "no paper studies exactly this point"; defensible, new.
- **E-ORDER (Miller §19.2)** is stronger than our per-(sender, target) FIFO: a reference passed in `args`
  lets the receiver send to the same target on a *different* queue and overtake the sender's earlier
  messages. READ.
- **CapTP / OCapN and Cap'n Proto RPC** (`rpc.capnp` `Disembargo` ll.688-735). READ (LIT-W3 §2). Our
  forwarding is the "same-vat" case: atomic with resolution, so the multi-path races (Tribble 4-way race)
  cannot arise, **but** the `foo()`/`bar()` ordering question survives locally: where does a forwarded
  message enter the FIFO relative to direct sends made between send and resolution? Pipelining into
  *fields* of a result (`op:get`, `op:index`) is a real loss vs ours (object-reference replies only). In a
  single kernel pipelining saves turns, not round trips.
- **Daml** (Bernauer et al. 2023, arXiv:2303.03749, §3.6 authorization rules). READ (LIT-W3 §4). Exercise
  consequences are checked in the context *S ∪ C* (signatories ∪ controllers of the callee's template);
  "Delegation is not transitive … deliberate". **Difference of kind**: Daml's nested authority is
  *callee-declared consent*; ours is *caller-delegated* (the signer's scoped grant). Mini has no signatory
  referent on `ObjectRecord` (REVIEW-SCHOLAR-LAWS D-6). Also: Daml re-entry into a *consuming* choice fails
  because the contract is already archived (re-entry protection by linearity).
- **Soroban authorization** (Stellar docs, `objective-bend-grounding/stellar-soroban-authorization.txt`
  ll.63-82) and **Pact capabilities** (Kadena manual). READ. Both bind **arguments** (Soroban: an authorized
  invocation *tree* with args, nonce, expiry, each node marked "exhausted" once matched; Pact: capability
  with args, "managed" capabilities with a diminishing quantity). Ours is `{object, method, uses}`:
  **any frame holding the grant can call that method with arbitrary args as the signer** — a confused-deputy
  exposure if a malicious object sits mid-tree.
- **SeRIF** (Cecchetti, Yao, Ni, Myers 2021, "Compositional Security for Reentrant Applications", IEEE S&P,
  §4.1 Def 1, Fig 4, §4.2 Def 2). READ (LIT-W3 §5). Re-entrancy is defined by *integrity labels*, "deliberately
  not by object boundaries": object-level refusal over-refuses (Fig 4b) and **misses application-level
  re-entry across mutually trusting objects** (Fig 4c, A → B → C with A and C halves of one app — the Parity
  wallet shape). Permitted safe forms: tail re-entrancy, Town Crier's deliver/cancel. "Banning all reentrancy
  might seem appealing, but this solution would be overly restrictive" (§2.3).
- **ECF** (Grossman, Abraham, Golan-Gueta, Michalevsky, Rinetzky, Sagiv, Zohar 2018, "Online Detection of
  Effectively Callback Free Objects with Applications to Smart Contracts", POPL; Fig 14). READ. On 2015–17
  Ethereum, callbacks were **0.16% then 1.0%** of executions (Fig 14 `Callbacks` column); non-ECF 0.004% then
  <0.001%. So the cost of a blanket refusal is bounded between ~1e-7 and ~1e-2 of executions and **unmeasured**
  for us. W3: with deferred writes and snapshot views, read-only re-entry is harmless by construction, so the
  refusal is "belt over braces", not the mechanism that excludes the DAO shape. (Our journey plant
  "guard-removed mutant commits the DAO (bank 40 / thief 60)", MERGE-QUEUE.md:225, says the guard *is*
  load-bearing in at least one program: **the two claims conflict and the plant should be re-read** —
  INFERRED; see Q5-1.)
- **Aptos Move** module lock (Dedaub, "Insights from 300+ Audits", 2025-09-17; `objective-bend-grounding/
  dedaub-aptos-reentrancy.txt`). READ. Production precedent for exactly our rule (direct and indirect
  re-entry refused); its auditors list the bypasses: state held in a third party's resource, and closure
  re-entry within one module. "A per-object lock is only as good as the guarantee that the invariant lives in
  one object."
- **Internet Computer** (DFINITY interface spec and "message execution properties", paperbin). READ
  (LIT-W3 §6). Nearly our `send`: pairwise ordering of *starts* only; a call is queued only if the sender
  returns without trapping; exactly one reply-or-reject; cycles escrowed at send with a reserve for the
  **response leg**. Two IC scars: unbounded waits wedge callers (we have mandatory deadlines), and a
  bounded wait yields `SYS_UNKNOWN` (callee ran, caller told otherwise). Ours avoids `SYS_UNKNOWN` **today**
  only because delivery slots never expire (`Kernel/AnswerSlot.lean:15-22`, `expire_delivery_refused`); item
  5.4.2 (activities awaiting a message, with a deadline) would reintroduce it.
- **NEAR** (cross-contract docs; READ) makes callback gas a *second* declared number; EIP-150 (READ) shows the
  call-depth attack needs a caller that can catch a callee failure — ours cannot (above).
- **Block-STM** (Gelashvili et al., PPoPP 2023, Corollary 2) and **CALM** (Hellerstein & Alvaro, CACM 2020,
  Theorem 1; Bailis et al. 2014 Claims 11–14). READ (LIT-W3 §8–9). Deferred-write frames match Block-STM's
  per-transaction write set; the read set must be recorded per (object, field, version). The only monotone
  mutations we have are unbounded appends and write-once decisions; the inbox bound (16), postage escrow and
  consume-once are all non-monotone, so cross-domain or parallel `send` is limited by exactly the features that
  make it safe.
- **Durable Functions critical sections** (Burckhardt et al. 2021, §3.4.1): may call only pre-locked entities;
  the nearest published relative of a scoped grant, for state rather than authority (INFERRED, W3).

**Code answers to some of W3's questions** (read on main): a sibling call *does* see an earlier sibling's
write — the callee's view is "the snapshot, plus every write an earlier frame of this turn already applied
at its return" (`Kernel/ObjectiveCall.lean:21-23`), taken at frame **entry**; a full queue refuses the whole
turn by name (`queueFull`, `:66`); a frame cannot catch a callee refusal (no failure arm in `R`); seat exit
rules are only `onDemand | afterDeadline` (no Zoe `waived`, `Kernel/Seat.lean:58-62`), and
`seat_offer_safe_forever` is a reachable-state invariant from a seatless genesis (`:1287`), with
`seat_debit_authorized` (`:1383`) enumerating the only debit paths (reallocate by the seat's instance, exit,
terminate). W3's remark that "a second write to the same slot aborts (R-CALLS D2)" describes the root's design
resolution D2, **not** the code: OB7 applies writes in order at return and has no frame-conflict abort
(`Kernel/ObjectiveCall.lean:45-48`).

## 4. Open design items handed over by DEPUTY-OB-ENG (meaning changes; not coded)

**5.4.1 Sends from a delivered message** (cv 01a10ae9-79e1). Today a frame running under `deliverMessage`
that yields `send` has no paying account, so the delivery fails (pops, `broken`). Options: (a) the original
sender prepays a bounded postage *tree* declared at send; (b) the target object pays from an object-held
purse (needs objects holding accounts + authority to spend from a subjectless frame); (c) forbid by type
(a delivered method's Plan type excludes `send`). (c) is a typing rule; (a)/(b) change cost/authority
semantics. Bread's pay flows want (a) or (b).

**5.4.2 An activity awaiting a message reply** (cv 01a10ae9-7a1a). Reply slots are decided only by the
`deliverMessage` that pops that id, a subjectless turn anyone may run. Awaiting one makes the activity's
resume depend on that. Interacts with resume-with-view, timeout/abandon (delivery slots never expire), and
exhaustion. Needs: must an await on a never-expiring slot carry a timeout arm? Do `upgraded`/abort apply?

**5.4.3 Pipelining depth > 1** (cv 01a10ae9-79fd). Pipelined sends queue on the reply slot with postage in
the holding inbox's purse; a pipelined message's own slot opens only when forwarded ⇒ depth 1. E/CapTP-style
promise pipelining needs a contagion rule; OB8 explicitly refused deciding a slot from a non-matching turn.

## 5. Questions for GPT-6

- **Q5-1 (sharpest).** *Where does a cross-object invariant live?* Laws judge one object's (old, new,
  request); re-entry refusal is per object. SeRIF Fig 4c, the Aptos bypasses and eUTxO's whole-transaction
  validators all say per-object guards miss invariants split across objects (A → B → C, A and C one app).
  Options: (a) the object model *declares* that an invariant lives in one object (plus a publish-time lint);
  (b) laws see sibling frames' writes (eUTxO), coupling every write to the turn; (c) trust-labelled
  re-entrancy à la SeRIF. Which, and what Lean statement replaces "no object twice on the stack" as the
  theorem that matters? Sub-question: is the re-entry refusal load-bearing given snapshot views + deferred
  writes (W3 says no; our DAO mutant plant says yes)?
- **Q5-2.** Scoped grants `{object, method, uses}` do not bind arguments; Soroban and Pact do (and Soroban
  binds the sub-invocation tree, a nonce, an expiry). Is the confused-deputy exposure real under our model, and
  what is the right matching rule? Separately: Daml-style callee-declared consent (signatories) vs our
  caller-delegated grants — should Mini have both, named?
- **Q5-3.** Synchronous cross-principal `call` at all (root OPEN 1)? E would say: only within a vat.
  Our variant has no live heap and no re-entry, but keeps "aborting the wrong plan" (an untrusted callee's
  refusal aborts the caller's whole turn). Is "a caller who will not underwrite a callee uses `send`" an
  adequate answer, or should a frame be able to observe a callee's refusal (and if so, how do we avoid the
  EIP-150 call-depth attack class)?
- **Q5-4.** Send ordering: forwarded-on-resolution vs direct sends (Cap'n Disembargo); E-ORDER forks for
  references passed in args; datalock (can the delivery deciding slot S send to S?). Which order do we promise?
- **Q5-5 (OB-ENG 5.4.1–5.4.3).** Who pays onward sends from a delivered message — prepaid postage tree,
  object-held purse, or forbidden by type? Must an activity's await on a (never-expiring) message reply slot
  carry a timeout, and how do we avoid the IC's `SYS_UNKNOWN` when it does (remove the message and refund in
  the same transition)? What contagion rule makes pipelining depth > 1 sound? And who pays the *reply* leg
  (IC reserves for the response; NEAR declares callback gas separately; we have one `postage`)?
