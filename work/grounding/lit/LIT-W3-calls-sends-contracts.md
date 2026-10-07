# LIT-W3: calls, sends, activities, laws, seats, admission — primary-text check (2026-10-06)

Worker: literature W3 for DEPUTY-GROUNDING. No builds, no code edits, no git.
Primary sources: `~/paperbin/world-program-model/` (called `WPM/` below). New downloads: `~/paperbin/objective-bend-grounding/`
(`stellar-soroban-authorization`, `stellar-soroban-cross-contract`, `dedaub-aptos-reentrancy`, `pact-manual-capabilities`,
`pact-capability-theory-wiki`, `eip-150`; each .html with a .txt beside; ~100 KB total). Kagi queries used: 8 of 20.
Disk: Mac data disk 99% (115 Gi free) before and after; I wrote only small text files.

Tags: **READ** = read in the primary text at the cited place. **VIA-SCHOLAR** = taken from a scholar report, not re-verified
(report named). **INFERRED** = my reasoning, not in the source. AGREE / DISAGREE / SHARPEN is about *our* design (see the brief).

Scholar reports are abbreviated: CALLS = `SCHOLAR-CALLS-CONCURRENCY-20261004.md`, FRONTIER = `SCHOLAR-FRONTIER-AGORIC-20261004.md`,
LAWS = `SCHOLAR-LAWS-CONTRACTS-20261004.md`, R-CALLS = `REVIEW-SCHOLAR-CALLS-20261005.md`.

---------------------------------------------------------------------------------------------------------------------

## 0. Headline findings (read this if nothing else)

1. **Our `call` is E's immediate call with both hazard sources removed, not a point E ever occupied.** E's plan-interference
   hazards (Miller §13.1) need a callee that runs *on the caller's live, mid-update heap* and can re-enter. We remove the live heap
   (snapshot + deferred writes) and the re-entry (refusal). No paper I read studies exactly this point (INFERRED). It is a
   defensible, probably-good point, but the literature names three things it does NOT fix: failure attribution (§1), invariants
   that span objects (§5, §10), and sibling visibility inside one frame (§Q2).
2. **Object-granularity re-entry refusal is both too strong and too weak.** SeRIF (Cecchetti et al. §4.1, Fig. 4) shows
   object re-entrancy is the wrong boundary: it over-refuses (Fig 4b) and misses application-level re-entry across *mutually
   trusting* objects (Fig 4c: A -> B -> C with A and C halves of one app; the Parity wallet shape). Aptos Move ships exactly our
   rule (module lock, direct and indirect) and its own auditors list the bypasses (§5).
3. **IC inter-canister calls are almost our `send`**: `call_perform` queues, acts only after the sender's message returns without
   trapping, pre-deducts a response reserve, guarantees *exactly one* reply-or-reject once `err_code` is 0, and gives pairwise
   FIFO of *starts* only (§6). The IC's two scars are directly ours to avoid: unbounded waits wedge the caller, and a bounded wait
   produces `SYS_UNKNOWN` (the callee ran, the caller was told otherwise).
4. **Scoped grants without argument binding are weaker than the two production precedents.** Soroban authorizes an invocation
   *with its arguments*, as a tree, with a nonce and an "exhausted" mark; Pact scopes a signature to a capability *with args*.
   Ours is {object, method, uses} (§4, Q3).
5. **Zoe's "judged on every reallocation" has a hole in the source I read**: the mint/burn path commits a reallocation with
   neither conservation nor offer-safety checked in `zcfSeat.js` (§3). Our kernel must make "every path" literal.
6. **Three scholar mis-citations / mis-corrections** (full list in the "Corrections" section), notably R-CALLS's "misquote"
   correction of the Grossman figure is itself backwards, and the OCapN "ordering bug" claim is not in either OCapN file.

---------------------------------------------------------------------------------------------------------------------

## 1. Miller 2006 "Robust Composition" and Miller/Tribble/Shapiro 2005 "Concurrency Among Strangers"

Files: `WPM/miller-robust-composition-2006.txt`, `WPM/miller-concurrency-among-strangers-2005.txt`.

### What the primary text says

- **Turn, vat, immediate call vs eventual send. READ.** Thesis §14.1 (thesis p.106): "Within a single thread of control, E has
  both a normal execution stack for immediate call-return and a queue containing all the pending deliveries. Execution proceeds by
  taking a pending-delivery from the queue, delivering its message to its object, and processing all the resulting immediate-calls
  in conventional call-return order. This is called a turn." So a turn already *contains* a synchronous call tree; E never banned
  synchronous calls, only synchronous calls **across vats**.
- **Why sync only within a vat. READ.** §14.2 (p.107): "eventual references carry only eventual-sends, not immediate-calls — an
  immediate-call on an eventual reference throws an exception." TGC p.206: "Only near references provide one object synchronous
  access to another. Therefore an object has synchronous access to state only within its own vat. Taken together, these rules
  guarantee that a running turn — a sequential call-return program — has mutually exclusive access to everything to which it has
  synchronous access." The reason is *mutual exclusion without locks*: a turn that only touches near objects needs no isolation
  mechanism. It is not a reentrancy argument.
- **Plan interference. READ.** §13.1 (p.97-100), three sequential hazards in the listener pattern: (1) **aborting the wrong
  plan** ("A listener that throws an exception prevents some other listeners from being notified … and possibly aborts the
  publisher's plan"), (2) **nested subscription**, (3) **nested publication** ("a listener may cause a publisher to publish a new
  status … After that inner invocation returns, the outer invocation of setStatus continues notifying listeners of the older,
  pre-deposit balance"). Miller's diagnosis (p.100): "The statusHolder, by running each subscriber's plan during a step of a
  publisher's plan, has provoked plan interference." TGC p.204: "all of the sequential hazards (e.g., Nested Publication) and many
  of the concurrent hazards (deadlock) occur because the statusChanged method is also invoked immediately: the publisher's plan is
  set aside to pursue the listener's plan." The cure is `<-` (eventual).
- **Pipelining. READ.** §16.2 (p.117-118): messages sent on a promise "'move' as close to the arrowhead as possible"; if the
  promise resolves locally on the target vat, "z(r2) is immediately queued on VatB's to-do list"; if it resolves on VatA the message
  is "streamed back towards VatA just behind the message informing VatA of r1's resolution"; if on a third vat it is forwarded.
  Pipelining there is onto *any* promise, not only promises of object references.
- **Datalock. READ.** §16.3 (p.118-119): a promise whose resolution requires already knowing it; "the not() message is forever
  buffered in the promise which only not()'s delivery could resolve". Miller counts "only two datalock bugs" in "perhaps 60
  programmers".
- **Broken promise contagion. READ.** §16.5: the vat catches the turn's exception and "breaks the promise by resolving the promise
  to a broken reference"; any call or send to a broken reference breaks the result.
- **E-ORDER. READ.** §19.1-19.4 (p.137-139): fail-stop FIFO per reference; reference **forks** at argument passing (Hasse
  diagram); CAUSAL order rejected because "we don't know how to enforce it among mutually defensive machines." §19.1 note:
  same-vat near calls may jump ahead of earlier eventual sends.
- **Turns never block, so cannot deadlock. READ.** TGC p.207: "computation within a turn can never block — it can only run, to
  completion or forever."
- **Defensive consistency. READ.** TGC §7.1 (p.208-209): defensive correctness = correct despite arbitrary client behaviour;
  defensively consistent = "incorruptible by its clients"; "If P relies on R, then P also relies on all of R's other clients
  unless R is defensively correct."

### Is our sync call with re-entry refusal a known-bad or known-good point?

**Neither; it is a new point whose two ingredients have precedents.** (INFERRED, from the above.)

| E hazard (§13.1) | Needs | Ours |
|---|---|---|
| nested publication | callee sees/acts on caller's mid-update state, and re-enters the publisher | removed twice: callee reads the turn snapshot and never sees a caller's pending write; re-entry refused |
| nested subscription | same, plus a mutable collection iterated during the call | removed: collections are state, writes deferred |
| aborting the wrong plan | a callee failure propagates to the caller's plan | **kept, and made worse**: a callee law refusal aborts the whole turn (R-CALLS OPEN 1 agrees) |

- **AGREE** with R-CALLS OPEN 1 that the DAO shape is excluded. **SHARPEN**: E's own cure for "aborting the wrong plan" is
  isolating failure by turn (`<-` + broken promise). Our only failure isolation is `send`. So the rule "a caller who will not
  underwrite the callee uses `send`" is not a courtesy, it is E's whole answer to hazard (1); the design should say that `call`
  failure is *never* catchable in-frame (otherwise we reintroduce a catch inside a deferred-write frame; see EIP-150 in §6 for what
  catchable callee failure did on the EVM).
- **SHARPEN (new hazard E does not have).** Because the callee runs on the snapshot and its write is judged at frame return, two
  *sequential* siblings of one caller (stack pops between them, so re-entry refusal does not fire) both read the pre-state. R-CALLS
  §2.5/D2 handles same-slot double write. It does not say whether sibling 2 sees sibling 1's *returned* write (Q2).
- **Reliance argument.** TGC's "P also relies on all of R's other clients" is the case for the law: each object must be
  defensively consistent against its own writers. That is exactly the law as the gate. AGREE (VIA-SCHOLAR CALLS A2 says the same;
  I confirm the quote above).
- **E-ORDER bears on `send`.** Fail-stop FIFO per reference plus forks is stronger than our per-(sender, target) FIFO: ours
  has no fork rule (an object reference passed in `args` can be used by the receiver to send to the same target on a *different*
  (receiver, target) queue, so receiver messages may overtake the original sender's earlier queued messages). Miller §19.2's
  Alice/Bob/Carol example is exactly this. Whether to care is a design choice (INFERRED); Miller says do, for the "Alice
  delegates querying to Bob" pattern.

---------------------------------------------------------------------------------------------------------------------

## 2. CapTP / Cap'n Proto RPC

Files: `WPM/ocapn-captp-spec.md`, `WPM/ocapn-implementation-guide.md`, `WPM/capnproto-rpc.capnp`, `WPM/capnproto-rpc.html`.

- **Pipelining. READ.** OCapN spec "Promise pipelining" (~l.188-200): a message sent with `answer-pos` creates a promise on the remote
  session that later messages reference with `desc:answer`; "When a promise is fulfilled to an object, messages sent to the promise
  will be delivered to that object." `op:get` (l.686), `op:index` (l.728), `op:untag` pipeline into *fields* of a result. Cap'n Proto:
  `PromisedAnswer{questionId, transform}` with `getPointerField` ops (rpc.capnp l.1115-1126).
- **Who names the answer. READ.** OCapN `answer-pos` "must be unique within the CapTP session" (l.590); the sender chooses it.
  **Ours differs and is better for consensus:** the message id names the reply slot (nobody submits a slot name). (INFERRED; R-CALLS
  §1 already credits Ozone for this.)
- **Embargo / E-order on resolution. READ.** `Disembargo` (rpc.capnp l.688-735): "if foo() is called on a promise, and that promise
  happens to resolve before bar() is called, then the two calls may travel different paths over the network, and thus could arrive in
  the wrong order. In this case, the call to bar() must be embargoed." "Note that in the case where Carol actually lives in … the
  same vat that the promise already pointed at, no embargo is needed, because the pipelined calls are delivered over the same path
  as the later direct calls." Also the "Tribble 4-way race".
- **Three-party handoff. READ.** OCapN spec §"Third Party Handoffs" (l.280-373): Gifter signs a `desc:handoff-give`; Receiver wraps
  it in a `desc:handoff-receive`; Exporter's `withdraw-gift` consumes the gift once ("handoffs cannot be used multiple times",
  guide l.529), with an anti-replay count; the guide (l.531) says ordering of gift deposit vs withdraw "does not matter".
- **Compare to our restricted forwarding.**
  - *Ours is the "same-vat" case only.* All our objects live in one kernel, so forwarding on resolution is a local queue move.
    CapTP's embargo/disembargo and the Tribble race arise from multiple vats and multiple paths; none arises when forwarding is
    atomic with resolution in one turn (INFERRED). **AGREE** that nested pipelining and cross-host handoff can wait.
  - *The ordering gap survives locally anyway* (SHARPEN, Q4b): a send to slot S (queued on S) followed by a direct send to the
    now-known target is the exact `foo()`/`bar()` example. If slot-queued messages are forwarded into the (sender, target) FIFO at
    the instant of resolution, a message sent *before* the resolution but forwarded *at* it can land behind direct sends made in
    between, or ahead, depending on the resolving turn's position. The design must state which; Cap'n's answer is "embargo so that
    send-order wins".
  - *Restriction to object-reference resolutions is a real loss versus CapTP's field pipelining* (`op:get`/`op:index`): a reply
    that is a record containing an object cannot be pipelined into. Acceptable for v1 (INFERRED). The Cap'n text calls
    pipelining "absolutely critical" to object interfaces over a network (capnproto-rpc.html l.206); that argument is about
    latency, which a single kernel does not have, so **our gain from pipelining is turn count, not RTT** (INFERRED; CALLS idea
    on Agoric kernel-pipelining-off VIA-SCHOLAR agrees).
  - *Datalock* (Miller §16.3) applies if a method can send to its own reply slot and then be required to resolve it from that
    send. Per-delivery run-to-completion makes it unlikely but the design should say a reply slot cannot be the target of a send
    made by the message that decides it (INFERRED).

---------------------------------------------------------------------------------------------------------------------

## 3. Agoric Zoe / ERTP: offer safety and payout liveness

Sources: `WPM/agoric-src-offerSafety-2026.js`, `agoric-src-zcfSeat-2026.js`, `agoric-src-zoeSeat-2026.js`,
`agoric-zoe-offer-safety-docs.txt` (docs "Offer Safety", "How Zoe Ensures You Won't Leave Empty-Handed" updated Jan 2020,
"Zoe v0.24.0, Aug 2022"), `agoric-doc-zoe-proposal-2026.md`, `agoric-doc-zoe-offer-enforcement-2026.md`.

- **Offer safety, definition. READ.** Doc "Offer Safety": "the user is guaranteed to either get at least what they wanted, or get back
  a full refund of what they offered — and never worse." Code `offerSafety.js` `isOfferSafe(proposal, allocation) =
  satisfiesGive(proposal, allocation) > 0 || satisfiesWant(proposal, allocation) > 0`, each `satisfiesInternal` = for every
  keyword in give/want, `AmountMath.isGTE(allocation[kw], required)`; a missing keyword in the allocation is unsatisfied (returns 0).
  FRONTIER's formula and its note on total slots are correct (VIA-SCHOLAR confirmed by READ).
  **Note the shape:** `isOfferSafe(proposal, newAllocation)`: a predicate on the new allocation and the *fixed original proposal*;
  it does not take the old allocation. Safety by induction: every committed allocation was safe, the first (the escrowed `give`)
  is safe, so the current allocation is always safe.
- **Where it is enforced. READ.** `zcfSeat.js` `atomicRearrange` (l.243-297): all seats active; `assertRightsConserved`;
  `isOfferSafe(seat.getProposal(), allocation) || Fail`; then "COMMIT POINT … The effects must succeed atomically".
- **Payout liveness. READ.** Doc "How Zoe Ensures…": "once the exit of an offer is triggered, Zoe ensures that the payout of that
  offer will be made promptly, no matter what the contract code does at that point." Triggers: contract wants out, client wants
  out, system error. Mechanism in `zoeSeat.js` `doExit` (l.71-84): `withdrawFacet.withdrawPayments(currentAllocation)` then
  `finalPayouts`. The payout is of the *current allocation held by Zoe*, not something the contract computes.
- **Exit is NOT unforbiddable in Zoe. READ.** `agoric-doc-zoe-proposal-2026.md` l.55-61: `exit` is one of `{onDemand}` (default),
  `{waived}` ("The offering party can't cancel and relies entirely on the smart contract to complete (finish or fail) their
  offer"), `{afterDeadline}`. FRONTIER l.293 lists these correctly (VIA-SCHOLAR, now READ).
- **A gap in "every reallocation". READ.** `zcfSeat.js` l.323-346, `zcfMintReallocator.reallocate`: "Unlike the zcf.atomicRearrange
  method, this one does not check conservation, and so can be used internally for reallocations that violate conservation, like
  minting and burning." It also contains no `isOfferSafe` call (the only call sites in these files are l.175-184 the seat method
  and l.269 `atomicRearrange`). I have not read `zcfMint.js`, so the caller may check elsewhere: **READ for the seat manager, UNKNOWN
  for the whole of Zoe**.

**Compare to seats ("a seat holds balances under an offer whose safety is a law judged on every reallocation, with an exit no clause
can forbid").**
- **AGREE** on the shape (R-CALLS/FRONTIER already say so): law = fixed-per-offer predicate, checked at the single commit point.
- **SHARPEN 1: "exit no clause can forbid" is strictly stronger than Zoe.** Zoe permits `waived`; our seat must not offer that
  variant, or the sentence is false. State whether a deadline-only exit is allowed (it is not "no clause can forbid"
  if the exit is only available after a deadline).
- **SHARPEN 2: the induction needs a reachable-state invariant, and a base case.** Zoe's safety of the *current* allocation holds only
  because the initial allocation equals the escrowed give and *every* write path is checked. Ours: the seat's initial balance must
  be established by a kernel action whose law is satisfied by construction, and `exit` must withdraw exactly the current balance
  (not "what the contract says"). Same pattern as R-CALLS §2.2 `reachable_records_typed` (INFERRED).
- **SHARPEN 3: "every reallocation" must include non-`atomicRearrange` paths** (mint, burn, fee debit, postage escrow, refund).
  Zoe's own seat manager has a bypass (mint path). Each kernel entry point that changes a seat balance needs the same law call
  (INFERRED from the READ gap above).
- **SHARPEN 4: Zoe's check is per-seat over proposed new allocations only for the seats named in the rearrangement** ("touched
  seats"). Seats not named are unaffected and unchecked. Our `call` tree can touch seats transitively; the rule "every seat whose
  balance changed in the turn is judged" must be stated at turn commit, not at the call site (INFERRED).
- Doc l.290-300 ("the contract never has access to your digital assets", assets are not sent to the contract, only information) is
  the property seats must keep: a seat's owner object is never handed its balance (VIA-SCHOLAR; READ in offer-enforcement doc).

---------------------------------------------------------------------------------------------------------------------

## 4. Daml (Bernauer et al. 2023, arXiv:2303.03749) authorization vs our signer/subject/scoped grant

File: `WPM/bernauer-daml-2023.txt`.

- **Model. READ.** Templates declare `signatory` (non-empty; authorize creation; notified), `observer`, and per-choice `controller`
  (§2.1-2.3, ll.150-217). A command is a tree of Create / Exercise / Fetch actions (§3.4, ll.470-500).
- **The authorization rule. READ.** §3.6 (ll.528-545), with authorization context A a set of parties:
  - Create is well-authorized iff S ⊆ A (all signatories are in A).
  - Fetch: A ∩ (S ∪ O) ≠ {} (a signatory or observer).
  - **Exercise: C ⊆ A (the choice's controllers), AND the *consequences* tx are checked in the context S ∪ C**, "the signatories
    and controllers". "This encodes that a signatory has pre-authorized the consequences of the choices when the contract instance
    was created. Delegation is not transitive, though, as the authorization context A of the Exercise action does not propagate to
    the consequences."
  - "Delegation not being transitive is a deliberate design choice … the authorization context for a choice implementation is
    determined solely by the template definition and thus independent of the calling context." "If the consequence … were instead
    checked in the augmented context A ∪ S ∪ C, then the additional parties in A could make a subaction well-authorized that in
    isolation would not be." Transitivity is opt-in by listing the needed parties as controllers of an inner exercise (Settle
    example, Fig 4).
  - A transaction is well-authorized if all top-level actions are.
- **Consuming choices. READ.** §3.3 exercise semantics (ll.472-492), step 4: the choice body is interpreted in the state where
  the exercised contract is already `Archived` if the choice is consuming; step 1 requires the contract to be Active. So re-entering a
  consuming choice of the same contract fails at step 1: re-entry protection by linearity. Non-consuming choices are re-enterable.

**Comparison with our model.**

| | Daml | Ours |
|---|---|---|
| Authority of a nested step | S ∪ C of the *callee's own template*: the callee's declared parties | the signer, as `request/subject`, only under a scoped grant {object, method, uses} |
| Source of nested authority | the callee's signatories pre-authorized it at creation | the signer's grant at invoke time; the callee declares nothing |
| Does the caller's authority flow in? | never (non-transitive, deliberate) | only through the grant; otherwise `request/caller` is an object name |
| Atomic tree | yes | yes |

- **SHARPEN (difference of kind, not degree).** Daml's nested authority is *callee-declared* (pre-authorization by the callee's
  signatories); ours is *caller-delegated* (the signer's grant). These answer different questions. Daml's rule ("who must have
  consented to this consequence") is a *consent* rule; ours ("on whose behalf may this frame act") is a *delegation* rule. Daml
  cannot express "Alice lets Bob's contract do X on her behalf this once"; that is what Soroban and Pact grants do (below). Conversely a
  grant model cannot express "this object's owners pre-consented to every consequence of this method" unless the object's law
  does. **Recommendation (INFERRED): keep both and name them**: law = callee-declared consent; grant = signer-delegated authority.
- **Daml's argument for non-transitivity is the argument for our `request/caller` + scoped subject.** AGREE: the non-transitive
  default ("the authorization safety analysis for the building blocks remains unaffected") is what `request/subject` absent-by-default
  gives us.
- **The grant is under-specified relative to production precedents (new, Q3).**
  - **Soroban (READ, `stellar-soroban-authorization.txt` ll.63-82):** the signer signs `SorobanAuthorizationEntry` carrying an
    **authorized invocation tree** (contract, function, *args*, sub-invocations), a **nonce** unique among unexpired signatures,
    and an expiry; each match marks the node **"exhausted"** so it cannot be matched twice; `require_auth_for_args` lets the callee
    constrain which args are covered. That is {object, method, **args**, tree shape, uses, expiry} against our {object, method, uses}.
  - **Pact (READ, `pact-manual-capabilities.txt` ll.94-141; `pact-capability-theory-wiki.txt` ll.55-120):** a signature is scoped to a
    capability reference *with arguments* (`TRANSFER from to amount`); `with-capability` pushes granted tokens on the call stack and
    pops them (dynamic scope = our frame scope); **managed capabilities** carry "a diminishing amount of a certain resource"
    ("watering can"), i.e. our `uses`, but as a quantity, and the manager function decides how a use decrements it.
  - So a grant that names only (object, method) lets any frame holding it call that method with arbitrary args under the signer's
    authority. **Confused-deputy exposure:** a malicious object in the middle of a tree that the signer called for another reason
    can spend the grant on its own args, as long as the (object, method) matches. Soroban and Pact both bind args.
  - Daml's "Fetch needs a signatory or observer" has no analogue of ours: reads see the turn snapshot (ambient read).
    That is a visibility choice, not a bug (INFERRED), but it is where a privacy-sensitive object would need Daml's rule.

---------------------------------------------------------------------------------------------------------------------

## 5. SeRIF (Cecchetti, Yao, Ni, Myers 2021) and ECF (Grossman et al. 2018)

Files: `WPM/cecchetti-serif-reentrant-2021.txt`, `WPM/grossman-ecf-callback-free-2018.txt` (also `grossman-ecf-2018.txt`, identical
size).

### SeRIF. What it permits and how it types it. READ.
- **Def 1 (ℓ-reentrancy, §4.1):** "If computation C1 calls computation C2, which then (possibly indirectly) calls C3, the execution
  is reentrant with respect to label ℓ if C1 and C3 are trusted at ℓ, but C2 is not." Defined by *integrity labels*, deliberately not
  by object boundaries: "We avoid object reentrancy because it relies on object boundaries — a fundamentally syntactic construct."
- **Fig 4:** (a) boundaries match; (b) a partly trusted object can create *object* reentrancy that is not ℓ-reentrancy (call into
  an untrusted part of A: harmless); (c) "mutually-trusting objects can create ℓ-reentrancy that is not object reentrancy",
  with the Parity Wallet (two famous attacks) as the example: "For an application split across A and C, if A calls B, then a call
  from B into C … is a reentrant call into the application."
- **Def 2 (§4.2):** "A program is ℓ-reentrancy-secure if every ℓ-integrity property, such as a program invariant, that holds for
  all non-ℓ-reentrant executions holds for all executions."
- **Permitted safe forms:** *tail reentrancy* (the last operation is the untrusted call; "performing all state modifications before
  calling other contracts" is the folk rule made principled), and Town Crier's `deliver`/`cancel` (§2.3: "Banning all reentrancy
  might seem appealing, but this solution would be overly restrictive"; status is updated before calling the untrusted callback).
  Enforced by an IFC type system plus run-time locks (§5, "combining a static IFC type system with a dynamic locking mechanism").
  Others they criticize: "some limit expressiveness by outlawing reentrancy entirely [14, 17]".

### ECF (Grossman et al.). READ.
- **Definition:** a run is dECF if there exists "an equivalent execution of the contract without callbacks" from the same initial
  state to the same final state; sECF if all executions are. Omitting calls is allowed when constructing the equivalent run (§2.2).
- **Decidability:** Thm 6.1: checking dECF of an execution is undecidable (it is stated for dECFofs executions); Thm 6.6:
  decidable for objects over a finite variable domain; "non-ECF executions which occur in high depth of nesting must also occur in
  depth 2" (§1). Thm 7.1: if the object is sECF_fs then states reachable in a run of the most-general client include all
  quiescent-reachable states, so the object can be verified on its own; "the analysis simply assumes ECF, and does not require
  to prove it": a runtime that enforces dECF suffices.
- **Online check:** an instrumented algorithm, a *stronger* requirement than ECF "inspired by conflict serializability" (§2.3);
  Thm 8.13: acyclic IOC relation implies ECF (a **soundness** theorem); the time bound O(nm^2) is the §8.3 analysis (ll.1103-1164),
  overhead 3.38% time / 17% memory (Fig 17).
- **Measured (Fig 14, l.1221):** Ethereum 30.VII.2015-30.III.2017: 81,097,421 executions, **128,670 "callbacks"**, 3,315 non-ECF
  (0.004%); 30.III-23.VI.2017: 15,311,650 executions, **155,662 callbacks**, 6 non-ECF (<0.001%). Text l.1182: "only 10 executions
  out of about 100 million were legitimately non-ECF". All 2,288 ETC non-ECF were DAO copies.

### Is our refusal stronger than needed, and what does it cost?
- **Stronger than ECF requires: yes, in two ways (INFERRED).** (1) ECF accepts re-entry that is equivalent to a callback-free run;
  we refuse all of it. In particular a re-entry that only *reads* the re-entered object is trivially equivalent to a callback-free
  run and costs nothing under ECF; in our model the re-entered frame reads the snapshot and its writes are deferred and
  conflict-checked, so read-only re-entry is harmless by construction. Refusing it buys nothing. (2) Our deferred writes already
  make the DAO shape impossible without the refusal: a re-entrant frame cannot see the outer frame's pending write, and a second
  write to the same slot aborts (R-CALLS D2). So the refusal is **belt over braces**, not the only mechanism. Keep it if cheap, but
  do not describe it as the mechanism that excludes re-entrancy attacks.
- **Cost of the blanket refusal, upper and lower bound (READ numbers, INFERRED reading).** Fig 14's `Callbacks` column counts
  invocations that were callbacks (re-entries into an object on the stack): 128,670 / 81.1M = **0.16%** of executions in the first
  window and 155,662 / 15.3M = **1.0%** in the second (growing: "the number of executions with callbacks increased significantly,
  indicating more complex contracts"). Blanket refusal would refuse up to that share if they were all valid; ECF refusal refuses
  <=0.004% (and ~1e-7 legitimate). The cost of OUR refusal is therefore **between ~1e-7 and ~1e-2 of executions on 2015-17 Ethereum
  and is not measured** (R-CALLS §2.5 reaches the same "unmeasured"). Only the ECF side is measured.
- **The mis-correction.** R-CALLS §2.5 ("My misquote… came from my final relay message. My report's text … says non-ECF.") and scribe
  note D1 claim the figure "10 of ~100M legitimately reentrant" is wrong and should be "non-ECF". The paper's own sentence is "only
  10 executions out of about 100 million were legitimately non-ECF" (l.1182). The original (CALLS E1) quotation is accurate; what is
  true is that "legitimately non-ECF" is a statement about ECF violations, not about re-entrancy, and that blanket refusal's cost is
  the `Callbacks` column. Use that column, not the 10.
- **The misfit that matters more (SHARPEN, Q1).** SeRIF Fig 4c/Def 2: invariants hold "for all executions" only if the notion of
  "re-entrant" tracks *trust*, not object identity. Our refusal makes Def 2 hold **for single-object invariants only**. FRONTIER
  l.731 says the guard "makes true" the theorem "every admitted re-entrant turn is equivalent to some non-re-entrant turn"; that
  holds trivially for object-level re-entry (there are none) and says nothing about A -> B -> C with A, C halves of an application.
  The law judges only the object's own (old, new, request); a cross-object invariant (A.balance + C.balance = K) is judged by no law
  that sees both. See §10.
- **Aptos Move is the production precedent for our rule, and documents its holes. READ**
  (`dedaub-aptos-reentrancy.txt`, Dedaub, 2025-09-17, "Insights from 300+ Audits"): the VM tracks `active_modules` and, when a
  module lock is active and the callee module is already active, errors "Reentrancy disallowed: reentering `{}` via function `{}` (module
  lock is active)", covering **direct and indirect** re-entry (A -> A, A -> B -> A). A second layer locks *resources* "preventing
  it from being accessed in a reentrant fashion". Documented bypasses: (1) **third-party resources are not locked** (Move 2.2
  closures): a contract whose state lives in another module's resource can be re-entered through a closure; (2) **direct
  closure-based re-entry within one module** bypasses the check ("the lock check only triggers on cross-module entries").
  These are exactly Q1 (state split across objects) and a "same object, different entry" analogue; the first says
  **a per-object lock is only as good as the guarantee that the invariant lives in one object**.

---------------------------------------------------------------------------------------------------------------------

## 6. Internet Computer, NEAR, EIP-150

Files: `WPM/dfinity-docs-message-execution-properties-2025.md`, `dfinity-docs-security-inter-canister-calls-2025.md`,
`dfinity-ic-interface-spec-2025.md`, `near-crosscontract-doc.txt`, `near-callbacks-security.txt`, `near-sigmaprime-xcc.txt`,
`objective-bend-grounding/eip-150.txt`.

### IC, compared point by point. READ.
| Question | IC (source) | Ours | Verdict |
|---|---|---|---|
| Ordering | Property 3 (docs): "if a canister A sends m1 and m2 to canister B in that order, then, if both are accepted, m1 is executed before m2"; spec "Ordering guarantees": per *pair* of canisters, "start executing in order"; **responses have no ordering guarantee** relative to each other or to calls | per-(sender, target) FIFO | **AGREE** (same unit). The IC also guarantees order only of *starts*; say so. Ours is stricter on nothing, but we must not claim reply ordering |
| Queue & backpressure | `ic0.call_perform` returns `err_code` 0 or 2; 0 means "exactly one of the reply or reject callbacks will be executed"; 2 = refused, no callbacks | queue bounded 16, answered "queued {slot}" at once | **SHARPEN**: what happens at the 17th? IC refuses at the point of the call with a defined code; ours says "answered at once with queued", so full-queue must be a defined refusal of the yielding frame (Q4d) |
| Queued only if the sender succeeds | spec: "queues the call message … but does not actually act on it until the current WebAssembly function returns without trapping"; trap discards state and queued calls (Property 5) | sends yielded by a frame; turn aborts discard them (INFERRED) | **AGREE** |
| Reentrancy at await | **Every await is a commit point** (Property 2, 5): "code after the await … is executed as a separate message execution"; Property 4: interleaving of different calls has "no reliable execution ordering"; security doc: TOCTOU and double-spend bugs, locks that never release when a callback traps | `await` is a yielded Plan; resumed in a *later turn with a fresh view* | **AGREE** and this is the IC's whole bug class; R-CALLS §2.3 already says "the view gives freshness, not isolation". The IC security doc's remedy is a *journal as lock* ("the journal acts as a lock on the critical section"), which an activity cannot get from a view |
| Cycles attached | Property 10: for unbounded-wait calls, "the sum of cycles accepted by the callee, and those refunded to the caller equals the amount that the caller attached"; `call_perform` "deducts `MAX_CYCLES_PER_RESPONSE`" set aside for response processing; `ic0.call_cycles_add` deducted immediately, moved back if the call cannot be performed | postage escrowed into the inbox purse per send | **AGREE** on escrow-at-send + refund; **SHARPEN**: the IC reserves for the *response* as well as the request (spec l.2285: "the cost for the transmission of the largest possible response, and the cost for executing the largest possible response callback … partially refunded"). Who pays for the **reply resolution and the resumption** in ours? R-CALLS mentions an escrowed fee pair; the design text should show it covers the reply leg |
| Who pays for callee execution | callee's own balance: the call is delivered only if `liquid_balance(callee) ≥ MAX_CYCLES_PER_MESSAGE`, which is *deducted* then refunded (spec l.4794-4823); sender pays call overhead and bytes | sender's postage pays the callee's execution ("paid from the inbox purse only") | **DISAGREE by design, fine**: IC is the "reverse gas" model; ours is sender-pays. Sender-pays needs the declared envelope to bound the callee (we have it) and makes spam cost the sender (good) |
| Reply/reject | Property 7: "Every inter-canister call is guaranteed to receive a single response, either from the callee, or synthetically produced by the protocol"; reject may come from callee or ICP; a reject "doesn't guarantee that the receiver's state wasn't changed" | `broken` on failed delivery; slot: one decider, one deadline, one terminal decision | **AGREE** (one terminal decision), **SHARPEN** with the next two rows |
| Unbounded wait | Property 8/9: unbounded-wait call can be delayed "arbitrarily long if it is willing to put in the required cycles"; security doc ("Make sure there are no loops in call graphs", "calling untrustworthy canisters") gives a DoS and deadlock class; a canister with a pending callback cannot be cleanly stopped/upgraded | mandatory deadline on every await/slot | **Ours is strictly better** (INFERRED) |
| Bounded wait | Property 9/11: a bounded-wait call "may generate a reject response … even if the call is successfully delivered to the callee and the callee responds"; this is `SYS_UNKNOWN`; the real response "will get dropped"; attached cycles "may get lost" | deadline expiry decides the slot `broken` | **SHARPEN, the sharpest transfer (Q4a)**: our expiry decision is a `SYS_UNKNOWN` unless the queued message is *removed and its escrow refunded in the same transition*; if it can still be delivered later, the caller is told `broken` and the effect happens |
| Call-graph cycles | security doc: "Loops in the call graph (A->B->C->A) may lead to canister deadlocks" | `send` cycles cannot deadlock a frame (no waiting); `call` cycles refused by the re-entry rule | **AGREE** (INFERRED) |

### NEAR. READ (`near-crosscontract-doc.txt` ll.4-5, 73-109; `near-callbacks-security.txt`).
- Calls are asynchronous; "The calling function and the callback execute in different blocks (typically 1-2 blocks apart)… If the
  external call fails, the calling function has already completed successfully; there's no automatic rollback."
- **Prepaid gas, declared by the caller per promise:** `with_static_gas(CALL_GAS)` for the call and a separate `CALLBACK_GAS` for
  the callback ("Always reserve gas for the callback. It executes in a separate receipt, so it can fail independently if it does not
  receive enough gas"), plus `with_unused_gas_weight` to divide leftovers proportionally (default weight 1; "If you forget that
  the default weight is 1, a callback or parallel promise can receive more of the remaining gas than you expected").
- **Compare to our `postage`:** NEAR's per-promise static gas is our "postage = the envelope each message is delivered under"; NEAR
  makes the *callback* envelope a second explicit number. Ours has one postage per invocation covering all sends. **SHARPEN:** one
  postage for all messages of an invocation cannot price a reply-resumption leg differently from a request leg; NEAR learned to
  separate them (a callback that runs out of gas is the classic failure). The weight mechanism is the cost of *not* knowing the
  envelope up front; our "priced on declared envelopes" avoids that (AGREE).
- NEAR's forged-callback and stake-twice races (VIA-SCHOLAR, CALLS E12; `near-callbacks-security.txt` is the source, not
  re-read in full) are the NEAR instance of "view gives freshness, not isolation".

### EIP-150. READ (`eip-150.txt` ll.37-58).
"Define 'all but one 64th' of N as N - floor(N / 64)" ; a call that asks for more gas than that "call[s] with all but one 64th".
The rationale for EIP-114 (l.58): "replacing the call stack depth limit with a 'softer' gas-based restriction, thereby eliminating
call stack attacks." **Bearing on us:** the 2016 *call-depth attack* needed a callee failure the caller could *observe and handle*
(the attacker burns stack so the victim's inner call fails and the victim continues in a bad branch). We have a hard depth of 8 and
one declared envelope for the whole tree, so there is no 63/64 question. But the depth limit becomes attackable exactly if a frame
can catch a callee's refusal; R-CALLS says a callee's refusal aborts the whole turn (no catch). **Keep it that way and say so**
(INFERRED; ties to §1).

---------------------------------------------------------------------------------------------------------------------

## 7. Khan 2026 "Resume Means Resume"; Burckhardt et al. 2021 durable functions

### Khan (`WPM/khan-resume-means-resume-2026.txt`, arXiv:2608.03836v3). READ.
- **Properties (abstract, §3):** six safety properties over the persistence API, "prefix continuation, effect exactly-once, fork
  determinism, checkpoint validity, consume-once, recovery determinism — plus fork-intent and liveness obligations". EO (Property 2)
  is a *safety* invariant (at-most-once); "the 'exactly' is supplied by pairing with the liveness obligation of Sec. 4".
  Liveness is `EventuallyCompletes` under **weak fairness only** (§4.1, ll.595-597, 678); its role is "closing a vacuity hole" so a
  framework with "Safety vacuous, progress dead" fails.
- **Lemma 1 (l.338) and Definition 2 (l.296-312):** FD (fork determinism) and CO (consume-once) are jointly unsatisfiable on
  identical traffic *unless* the wire carries a branch discriminator (FI, Property 7). Lemma 1 "is deliberately not an explanation of
  LangGraph's defect."
- **Measured (l.1044-1054, probe 168):** 40 cells, 400 protocol executions, "The gated effect fires 2,628 times where exactly-once
  predicts 400", saturation 1.0 in 36 of 40 cells; cross-host racers duplicate 10/10; abstract: saturation "never below 0.933".
  **The repair:** "an opt-in gate claims consumption in the shared store, serving one racer and refusing the rest before any node
  executes"; the paper states twice (l.1211-1213) "a repair placed at the persistence write path was powerless while the same repair
  placed at the durable-state read path succeeded." CALLS C6 and R-CALLS §1 are accurate on all of this (VIA-SCHOLAR, now READ).
  Caveat Khan states (l.1227): the no-latency claim is "not for every possible write-path design".
- **Fit:** R-CALLS §1's table (PC/EO/RD/CO yes, FD/FI "not offered, correctly", CV per step only, liveness no then fixed) is
  consistent with Khan's definitions. **SHARPEN:** weak-fairness liveness assumes some action eventually runs; for us that is
  "anyone may run `deliverMessage`/decide an expired slot". A chain with **no** such actor is not live; this is an economic fact
  (someone must be paid to run it), so the postage/escrow must *pay the runner of expiry and delivery*, else the liveness
  obligation is satisfied only in the model (INFERRED).

### Burckhardt et al. (`WPM/burckhardt-durable-functions-semantics-2021.txt`). READ.
- **Thm 5.3 (l.1117):** "∼ is a weak simulation relation, when hiding commit messages" (compute-storage model vs high-level model:
  observably exactly-once). **Thm 6.4 (l.1239):** replay-based and storage-of-state models are bisimilar for deterministic code.
  Footnote on why simulation vs bisimulation (l.1229-1231). CALLS C1 correct.
- **Critical sections (§3.4.1, l.559-563):** a section must name all entities up front; "while executing, it can call only entities
  that are already locked, it cannot call sub-orchestrations, and it cannot enter another critical section." Global lock order is
  *implementation* (footnote 6, l.590: "acquiring the locks in a globally consistent order, one at a time"), not a semantic rule.
- **What the proofs exclude (§5, ll.980-990, "Future Extensions"):** "The compute-storage model currently does not include external
  calls or critical sections."
- **Fit:** durable-functions *calls entities from orchestrations* with replay of recorded task results (history), which is the
  resumption story our `await` replaces with a checkpoint digest. Their rule that critical sections may call only pre-locked entities
  is the nearest published relative of "a scoped grant {object, method, uses}" **for state**, not authority (INFERRED).

---------------------------------------------------------------------------------------------------------------------

## 8. Block-STM (Gelashvili et al. 2022/23)

File: `WPM/gelashvili-block-stm-2022.txt`. READ unless marked.

- **The guarantee.** Abstract ll.21-27 ("must yield the same deterministic outcome"), ll.56-58 ("The final outcome is equivalent to
  the sequential execution of transactions in the preset order in which they appear in the block"), **Corollary 2 (l.1333):** "A call
  to MVMemory.snapshot() after a thread joins returns the exact same values at exact same paths as would be persisted at the end
  of a sequential run of all transactions"; Lemma 1 (l.1141). Mechanism: preset order + multiversion data structure + ESTIMATE
  markers; a transaction that reads an ESTIMATE of a lower transaction suspends and is re-validated; no read/write sets needed in
  advance. **Termination is Theorem 2** (l.1364): "If threads keep taking steps … and VM.execute is wait-free, then all threads
  eventually join": termination rests on the VM being wait-free, which on a chain means gas/step bounds.
- **Gas hot-spot, READ (l.918-921):** "In Blockchain systems, there is usually an associated 'gas' cost to executing transactions. A
  single location for gas updates, could make any block inherently sequential. However, this issue is typically avoided by tracking
  gas natively, burning it or having specialized types or sharded implementation." Also (l.923 area) "Diem VM currently does not
  support suspending and resuming transaction execution." Measured: up to 30% overhead when completely sequential (l.107) and
  the 17x/20x figures (l.34-35).
- **Bearing on deterministic re-execution admission.** AGREE: re-execution equals the command's effects iff the effects are a
  deterministic function of (command, state). Block-STM's equivalence is to the *preset order*, which our admission has for free
  (log order; R-CALLS §2.5). The guarantee is only as strong as `VM.execute` being a pure function of its reads (Algorithm 3: the VM
  "does not write to MVMemory", reads its own write_set first, records a read-set of (location, version)).
- **Is our deferred-write call tree friendly to it? Largely yes (INFERRED).**
  - Frames' writes are buffered and applied at frame return, never visible to a callee: this is exactly Block-STM's per-transaction
    `write_set` (a read of a location in the txn's own write_set returns the txn's value, Algorithm 3 ll.84-85). Our rule is simpler:
    callees do **not** read the caller's pending write at all. No intra-turn read-your-writes across frames means a turn's read
    set is the snapshot reads only, so validation stays per-location.
  - No suspension inside a turn: a frame never suspends while a callee runs from its own stack (all depth-first, to completion).
    The Diem VM limitation quoted above is therefore not an issue for `call`; it *is* the reason `await` must be a turn boundary
    (it already is).
  - **Two precision requirements (SHARPEN, Q6):** (a) the read set must be recorded per (object, field), not per object, or the
    "judged against exactly the state the frame was shown" check over-conflicts; the design says "turn's snapshot", Block-STM needs the
    *versions actually read*. (b) The fee sink: "Fees priced on DECLARED envelopes" removes *measured gas*, but each turn still
    debits the signer and credits something. Where the credit lands (a protocol treasury, an inbox purse) is a single location every
    turn writes: the inherently-sequential-block pattern the paper names. Make fee/escrow credits per-turn deltas judged by
    commutative laws (the R-CALLS D2 "commutative delta" escape), not read-modify-write.
- R-CALLS §2.3's "version check = Block-STM validation, build once, delete `Record.reads`" is **AGREE** (VIA-SCHOLAR, consistent with
  the algorithm above).

---------------------------------------------------------------------------------------------------------------------

## 9. CALM (Hellerstein & Alvaro, "Keeping CALM", CACM 2020)

File: `WPM/hellerstein-keeping-calm-2019.txt`. READ for the theorem; analysis of our operations is INFERRED.

- **READ:** Def 1 (l.136) monotonic; **Theorem 1 (CALM), ll.142-146:** "A program has a consistent, coordination-free distributed
  implementation if and only if it is monotonic." Distributed deadlock detection is monotone ("decisions based on incomplete
  information are stable"); distributed garbage collection is not (§1.3.1-1.3.2). Bailis et al. (`WPM/bailis-coordination-avoidance-
  2014.txt`) Claims 11-14 (ll.447-448, 1173-1204): counter increments I-confluent with `>` threshold, **not** with `<`; decrements
  the reverse. CALLS F7 correct (VIA-SCHOLAR, READ).
- **What CALM does and does not say for us (INFERRED).** CALM concerns *coordination-free distributed* implementations. We have a
  consensus order, so we always "coordinate". The use of CALM is to say **which operations could run outside the ordered path
  (cross-domain, parallel admission, light-client reads) and which must stay inside**.

| Operation | Monotone? | Why |
|---|---|---|
| `send` appended to a per-(sender, target) queue, unbounded | **yes** | grow-only sequence, one writer per queue (the sender), so no merge conflict |
| `send` with the **bound of 16** | **no** | "queue has room" is a `<`-threshold on an increment (Bailis Claim 12: not I-confluent). Two concurrent sends can both see room |
| postage escrow (`balance >= price`, decrement) | **no** | `>` threshold under decrement (Bailis Claim 13). Needs an ordered check or an escrow-split (Bailis's "escrow" amortization) |
| `deliverMessage` (pop the head) | **no** | destructive and "anyone may run it": two runners race for one head; consume-once is exactly Khan's claim-at-decide |
| answer slot: "this slot has a terminal decision" | **yes** | a write-once register; once true stays true |
| answer slot: decide *before the deadline* vs expire *after* | **no** | needs the height order: "undecided as of h" is not monotone. The one-decider rule removes the race among deciders, not between decider and expiry |
| await consumption (nullifier bound to checkpoint digest) | **add: yes; test-then-act: no** | set insertion monotone; "act only if absent" is the non-monotone read (same shape as GC) |
| view reads in a resume | **no** | freshness of a read depends on the order of prior writes |
| a law judging (old, new, request) | **depends on the law** | laws of the form "new >= old" (a le atom) are monotone and checkable without the total order; "new + old = K" are not (INFERRED from R-CALLS/LAWS use of `le`) |

- **SHARPEN.** The *only* monotone, order-free mutations are unbounded appends and write-once decisions. Everything involving the
  bound, the purse or consume-once needs the log. So parallel/cross-domain execution of sends is limited by exactly the three
  features that make them safe (bound, escrow, one-shot). That is a design fact, not a defect: say which operations a cross-domain
  `send` may use (VIA-SCHOLAR, FRONTIER's cross-domain deal cells would sit here).

---------------------------------------------------------------------------------------------------------------------

## 10. eUTxO (Chakravarty et al. 2020) and Move resources, briefly

File: `WPM/chakravarty-eutxo-2020.txt`. READ.

- **The validator signature (l.120-133):** outputs are `(ν, value, δ)`; "to check that an input with redeemer ρ that is part of the
  transaction tx is entitled to spend an output (ν, value, δ), we check that ν(value, δ, ρ, tx) = true". "we pass the entirety of
  the transaction that attempts to spend the output … to the validator invocation", so a validator can enforce *contract continuity*.
  Later formalized as `TxInfo` (ll.375-420, 488: "For all i ∈ t.inputs, ⟦i.validator⟧(i.data, i.redeemer, toData(toTxInfo(t,i,l)))
  = true").
- **CEM (§4.1, ll.528-545):** `step : S -> I -> Maybe (S × TxConstraints)`; "There is no notion of initial state, since we would not
  be able to enforce it on the blockchain level"; final states are *halting* ("a CEM final state indicates that the machine must
  halt … will not appear in the UTXO set"). **Weak bisimulation** with the ledger, mechanised in Agda (abstract l.31-33; CALLS E6
  says "bisimulation": the paper says weak).
- **Compare to laws over (old, new, request).**
  - **AGREE** on shape: validator = predicate over (old datum, redeemer, tx context incl. proposed new datum); our law = predicate over
    (old state, new state, request facts). "Code proposes, law disposes" is the CEM's off-chain `step` plus on-chain validator
    (the validator only checks the proposed next state). eUTxO's `Maybe` result (no valid transition = refusal) is our law refusal.
  - **DIFFER (a):** the eUTxO validator sees the **entire transaction**, i.e. *all* other inputs and outputs, so multi-object
    invariants are expressible and enforced by *each* input's validator. Ours sees only this object's (old, new) plus request facts.
    **A law cannot see a sibling frame's write unless `request facts` carry it.** This is the same gap as SeRIF Fig 4c and Aptos's
    third-party-resource edge (Q1). eUTxO closes it by giving the validator the whole tx; if we do the same the law is no longer
    "decidable over one object" and writes of an object become coupled to every other write in the turn.
  - **DIFFER (b):** the validator runs only on *spend* (the old output is consumed). Creation has no validator: "no notion of initial
    state". Our law "judges every write to an object's declared state", including birth? If birth is not judged, the same
    initial-state hole appears (the Zoe base case in §3 and R-CALLS §2.2).
  - **DIFFER (c):** eUTxO validators are *spend authorizations tied to the consumed UTXO*, so concurrency is by construction
    (a UTXO is consumed once; no read-write conflict). Our laws run on an object whose state persists, so the consume-once is
    replaced by the turn order (Block-STM, §8).
- **Move resources, briefly. READ** (`blackshear-move-resources-2020.txt` l.1080-1083): Move avoids dynamic dispatch by "moving the
  dynamism to the withdrawal code" (the caller supplies the logic; the callee has no callback into it): the capability answer to
  callback hijack. Relevance: the cheapest anti-re-entry design is a call model with *no callback target the callee chooses*. In
  our `call`, the callee's target is chosen by the *caller's* method; a callee that calls the caller's other objects is the
  only dispatch freedom (INFERRED).

---------------------------------------------------------------------------------------------------------------------

## Corrections to earlier scholars

1. **CALLS A4 (OCapN): "No embargo. The spec has no embargo, and the implementation guide reports an ordering bug introduced by a latency
   optimisation."** The spec indeed has no embargo (no hit). The implementation guide has **no** such report: `grep` for bug/race/optimi
   returns nothing; its only ordering remark (l.531) is that gift *deposit vs withdraw* order "does not matter". The embargo mechanism
   is in `capnproto-rpc.capnp` (`Disembargo`, ll.688-735). Mis-citation; the lesson (order belongs in the semantics) may still be right
   but is not sourced from these files.
2. **CALLS A1: broken promises "contagious, like NaN (§16.5)".** "Broken Promise Contagion" is the §16.5 title and the mechanism is
   as described; the NaN analogy does not appear in the thesis. Embellishment, harmless.
3. **CALLS E1: "Checkable online in O(nm^2) (Thm 8.13)".** Thm 8.13 is the soundness statement (no cycle in the IOC relation implies ECFc);
   the O(nm^2) bound is the §8.3 time analysis (ll.1103-1164). Also Thm 6.1 is stated for dECFofs executions.
4. **R-CALLS §2.5 and scribe note D1 "correction" of the Grossman figure is backwards.** The paper does say "only 10 executions out of
   about 100 million were legitimately non-ECF" (l.1182; also l.73-74 "just one such legitimate non-ECF contract"). What R-CALLS should
   have flagged is that this measures ECF violations, not re-entrancy; the relevant cost of blanket refusal is the `Callbacks` column
   of Fig 14 (0.16% then 1.0% of executions). See §5.
5. **R-CALLS OPEN 1, "Production precedent: … Tezos depth-first (CALLS E2)" for synchronous cross-principal `call`.** Tezos is not a
   synchronous-call precedent. `tezos-michelson-doc.txt` ll.472-473: "Internal operations are run … after the contract execution, in
   depth-first order … any contract calls emitted by a contract C are executed after contract C successfully finishes execution
   returning its result". It is `send` with depth-first delivery inside one atomic operation. The synchronous value-returning
   precedents in the list are Mina (VIA-SCHOLAR, CALLS E18, not re-read) and Daml exercise trees (READ here: but in Daml the callee sees
   live state, with the consumed contract already archived: the *opposite* of our snapshot rule).
6. **CALLS C1 (durable functions): "Locksets are declared, acquired in a global order … What the proofs exclude: external calls, critical
   sections and *versioning*".** The global order is an implementation footnote (l.590), not part of the semantics; and "versioning"
   appears nowhere in the paper (0 hits for versioning/upgrade); the excluded features are external calls and critical sections
   (§5 "Future Extensions", ll.980-990). The versioning exclusion is the scholar's inference.
7. **CALLS E6 (eUTxO): "Bisimulation with the ledger".** The paper claims a *weak* bisimulation (abstract). Minor.
8. **FRONTIER F1, l.731: "the SCHOLAR-CALLS re-entry guard makes [SeRIF's Def 2-style theorem] true by refusing re-entry".** True only for
   *object* re-entry; SeRIF's Def 2 is stated over trust-labelled ℓ-reentrancy and Fig 4c is the case an object guard misses. The Lean
   statement to prove must be about invariants of a *named* object, not "every re-entrant turn".
9. **R-CALLS §4 OPEN 1: "Grossman found 0.004% non-ECF executions on Ethereum history (E1)" as support for sync calls.** The figure is
   correct for the first window (3,315 / 81,097,421), and for the second 6 (<0.001%); but it measures an *ECF monitor's detections* (a
   stronger-than-ECF check) in a 2015-17 chain with call-depth heuristics in place ("attacking is harder as Ethereum employs … heuristics
   to limit callbacks", l.1320-1322), so it is a weak support for "refusal is cheap".
10. **Confirmed (no correction needed):** CALLS A1 turn / plan interference / E-ORDER / CAUSAL-too-strong; A2 defensively consistent;
    A5 Disembargo and Tribble race; A12/A13 Zoe; C6 Khan (all numbers); E4 IC; E7 Block-STM (Corollary 2, gas hot-spot quote); E5 Daml
    non-transitive; FRONTIER Zoe `isOfferSafe` formula and exit shapes; the SES clean-stack quote (`endo-ses-readme-2026.md` l.837-840).
11. **Not verified:** Soroban "re-entry disallowed by default" (memory, no primary text found in three Soroban pages and Kagi); Mina
    (CALLS E18) and Orleans (CALLS B2/B3) quotes; NEAR forged-callback race text (only the doc's headline read).

---------------------------------------------------------------------------------------------------------------------

## Sharpest questions

**Q1. Where does a cross-object invariant live, and who judges it?** (SeRIF Fig 4c + Def 2; Aptos third-party-resource edge; eUTxO
validator sees the whole tx.) Laws judge (old, new, request) of ONE object; re-entry refusal is per object. An application split
across objects A and C (A calls B calls C) is exactly the Parity/Uniswap shape SeRIF names, and the exact bypass Aptos's own
auditors list. Either (a) declare that an invariant must live in one object and say so in the object model, with a lint over
published packages, or (b) give laws access to the sibling frames' writes in `request facts` (eUTxO's whole-tx context) and accept
that a law is then coupled to the turn's other writes. The design currently says neither, and FRONTIER's "the guard makes the SeRIF
theorem true" is wrong for this case.

**Q2. Sibling visibility and failure inside one frame.** (E §13.1, Daml §3.3 step 4, EIP-150.) The design says a callee never
sees a caller's *pending* write and writes are judged against "exactly the state the frame was shown". Undefined: (i) after callee
B1 returns, does the caller's continuation, and a later sibling B2, see B1's write? If yes the rule is asymmetric and B2's judged
state is not the turn snapshot; if no, a caller cannot use any effect of a callee, only its result. (ii) Is the "state the frame
was shown" the turn-start snapshot or the state at call time? (iii) Can a frame catch a callee's refusal? If yes, the EVM
call-depth-attack class returns (EIP-150's reason for removing the depth limit) and "aborting the wrong plan" becomes
"continuing the wrong plan". The answers decide whether Block-STM read-set recording (§8) is per object or per frame.

**Q3. Does a scoped grant bind arguments?** (Soroban authorized invocation trees with args + nonce + "exhausted"; Pact capabilities
with args and managed quantity; Daml's callee-declared consent.) {object, method, uses} lets any frame holding the grant call that
method with arbitrary args as the signer, including a malicious object in the middle of a tree the signer called for another
purpose (confused deputy). Soroban and Pact both bind the args (Soroban also the sub-invocation shape and an expiry/nonce). What is
the grant's matching rule: args predicate, tree position, expiry height? And which of Daml's consent semantics (callee-declared)
vs delegation semantics (signer-granted) does `request/subject` mean?

**Q4. Send protocol edge cases, all with direct precedent in the IC and CapTP.**
(a) **Expiry vs delivery (IC `SYS_UNKNOWN`):** when a slot is decided `broken` by deadline, is the queued message removed and its escrow
refunded *in the same transition*? If it can still be delivered, the caller is told `broken` while the effect happens.
(b) **Forwarded-on-resolution vs direct sends (Cap'n `Disembargo`, Miller §19.2):** a message queued on a reply slot and a later direct
send to the resolved target; where does the forwarded message enter the (sender, target) FIFO, and is a reference passed in `args`
a "fork" (Miller) that lets the receiver overtake the sender's queued messages?
(c) **Datalock (Miller §16.3):** can the deciding delivery of slot S send to S, and what happens then?
(d) **Bound of 16:** the IC refuses at the call with a defined error; ours is "answered at once with queued". What does the 17th
send do (refuse the yielding frame? abort the turn? `broken` slot)? It is non-monotone (CALM §9) so it needs the log.
(e) **Who pays for the reply resolution and resumption** (IC reserves `MAX_CYCLES_PER_RESPONSE`; NEAR makes callback gas a separate
number)? One `postage` per invocation cannot price the reply leg.

**Q5. Seats: is "exit no clause can forbid" an invariant over reachable states?** Zoe's guarantee is an induction (initial
allocation = escrowed give; every path checked; exit pays the *current* allocation), it permits `waived` exit, and the seat
manager's mint path commits with no offer-safety call. For us: what kernel action establishes the first balance, which entry
points (mint, burn, fee debit, postage escrow, refund, `call`-tree transfers) call the seat law, and is `exit` defined as "pay
the current balance" so that a contract cannot choose the payout? Without the reachable-state theorem this is the same hole as
R-CALLS §2.2.

**Q6. Where do fees and purses land, and is the read set per field?** (Block-STM gas hot-spot; Bailis Claim 13.) Declared-envelope
pricing removes measured gas, but every turn still credits some sink and debits a purse. If these are read-modify-write on one
location, Block-STM's "inherently sequential" pattern is rebuilt by our own fee design, and `postage` escrow (`balance >= price`)
is a non-monotone check on every send. Should fee/escrow credits be per-turn commutative deltas judged by a `le`-style law, and must
the recorded read set be (object, field, version), not "the snapshot", for parallel admission to be correct?
