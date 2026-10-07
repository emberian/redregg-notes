# REVIEW-SCHOLAR-BREAD — calls, awaits, coordination grades, escrow, upgrade (2026-10-05)

BREAD §n = my report `work/SCHOLAR-BREAD-PROGRAM-MODEL-20261004.md`. Read: the design (§1, §B–§D, §F, §3,
§5, §6), the root's decisions in full, and minidregg main **36fca3ac** (fresh clone):
`Kernel/ObjectiveActivity.lean` (all 1161 lines), `Kernel/AnswerSlot.lean`, `Kernel/ObjectiveResumeContract.lean`,
`world/activity/Tally.obend`, `native/resource-client/objective-activity-demo.py`. Tags: **READ** (I read it at the cited place), **EXECUTED** (the landing's own
46/46 demo run, `3667e07d`, which I did not re-run), **INFERRED** (mine). No code commits; see §5 for why.

---

## 0. Verdict

The activity kernel carries most of the Bread lessons, and carries two of them better than Bread did. It
misses the one that mattered most for "several activities per object": **a stale resume today loses the
reply and then overwrites the newer state.** The landing's own demo asserts both as expected behaviour.

---

## 1. What the code got right (against Bread's record)

All READ in `Kernel/ObjectiveActivity.lean` unless noted.

1. **The await id is a nullifier bound to the checkpoint.** `awaitId cell generation checkpoint` is spent by
   `awaitClaim`. The delivery also writes the record against its current root, so consume-once is
   decided at the decide point: two checks, as Bread's React had (nullifier plus registry, BREAD §1.2 item 5).
   `resume_consumes_once` and `second_delivery_refused` are stated over the kernel's own
   `DurableDataIntent.execute`, not over a model (Bread's were not, BREAD §2.3).
2. **The slot is bound to the activity it answers.** `settle` refuses a slot whose `activity ≠ cell`, which
   is Bread's `wake.hash == pending_id` (BREAD §1.2 item 5).
3. **Eager shape is honoured at the yield.** The slot's decider, deadline and name are fixed when the slot
   opens. The reply is **typed at resolve time** against the waiting activity's declared reply type
   (`replyTyped`); Bread never typed a fill. `birth` refuses a response type that cannot type every
   kernel outcome, so the protocol too is fixed eagerly.
4. **Typed waits with mandatory deadlines.** `Source = reply | height`. A `message` wait is refused by name
   (`messageAwaitNeedsInbox`) rather than half-built. Patience is greater than 0 and at most `maxPatience`. Expiry is
   anyone's, strictly after the deadline, and decided in the same turn. This is Bread's
   `ResolutionCondition` without the proof arm, correctly omitted (BREAD §2.1 #3).
5. **Deposits are measurement-free.** The fee pair is priced from declared envelopes. Exactly one half pays
   the ending turn and the other half returns to the payer (`refund_measurement_free`,
   `submitter_charge_declared`). This is cleaner than Bread's refund-or-burn deposit.
6. **One async mechanism**: slot plus record is the only wait path; `message` is reserved to join it
   (Bread had five, BREAD §2.2).
7. **No state from a request**; `ObjectiveResumeContract` proves every stored checkpoint is typed.

---

## 2. What the code got wrong or missed

**D-1 (serious): a stale resume loses the reply and then clobbers the newer state.** READ + EXECUTED.

- The only recorded read is the root of the object state the activity itself wrote at its yield
  (`commitYield`: `reads := [⟨object, rootBytes stateBytes⟩]`).
- On staleness, `revalidate` replaces the settled outcome with `conflict (stale : Nat)`, so the decided
  reply is discarded. The slot's claim was already spent at resolve and the await claim is spent now, so the
  reply is unrecoverable by the activity: no Core4 operation reads a slot.
- The activity is given no view of the current state. Every `await` Plan must carry `state`
  (`decodePlan`: "await.state missing"), so its next yield blindly overwrites the newer write with its stale view.
- The demo checks exactly this. Scenario B: the owner writes 99, the decider replies 7, the delivery
  yields `conflict`, and `B-show-state` asserts the state is **5**. The owner's 99 is gone and so is the 7.
  `Tally.obend` handles `conflict(_)` with `tally(start)`.
- With two activities on one object it is worse. Every yield writes the shared object cell, so each
  activity's yield stales the other's pending replies.

This inverts Bread's "determination is eager, witness is lazy" (BREAD §2.1 #1). ROOT B's "stale → re-run
and a typed Conflict" landed as conflict without re-run. Replacement: §3 R1.

**D-2 (serious before any non-scratch use): birth writes any cell the request names.** READ.
- `BirthRequest.object : CellId` is unchecked. The first yield posts `dataBytes plan.state` to it, and
  `writeState` writes `record.object` for the record's payer.
- Kernel cells are tagged (records, slots, fee accounts, packages), but nothing stops `object :=
  recordCell …` of another activity, `accountCell victim` or `AnswerSlot.cell …`. That write bricks the
  other activity, its escrow or the victim's account.
- The scratch world is safe only because its Host tags object names (`Host/ObjectiveActivityWorld.lean:50`).
- Nothing judges a Plan write by any law yet, so "code proposes, law disposes" has no disposer on this
  path. This is acknowledged scope (no `ObjectRecord`), but it must land before any world friends touch.
- The running "activity native route (ownership, …)" lane owns this file; I did not race it.

**D-3: reasons are dropped.**
- `Answer.refused reason` and `Answer.broken reason` reach the activity as bare `refused` and `broken`.
  The design fixes `Refused(residual)` and `Broken(reason)` (§1, §B).
- Bread's broken-promise cascade needed typed reasons (`DependencyBroken`, `FederationUnreachable`; BREAD
  §1.2 item 7), and sends (L6) will need `DependencyBroken` to propagate.
- A finite reason sum (`DeciderRefused | DependencyBroken | NotAReference …`) is enough.

**D-4: the decider is a subject, not a role.** `Slot.decider : SubjectId`, named by the activity in its own
Plan. For `send`, the decider must be the *callee's delivery turn*, a role handed from slot to delivery to
callee (design §D: "the decider role is linear"). A subject cannot be handed on.
`decide_single_decider` will need restating over a role. Flag it before L6 freezes the slot codec.

**D-5: kernel work per resume is unpriced.** Every `deliver` (and reply `resolve`) re-runs `loadProgram`,
a full `checkWithin` of the package, paid by nobody (the escrow prices ticks only): the "unpriced kernel
work" decision G rules out. A check cached by `pin` at `publish` removes it (INFERRED fix).

**D-6: decided answer-slot cells have no payer and are never reclaimed** (design G wants a payer).

**T1 coverage.** Landed: (a) consume-once, (b) binds checkpoint, (c) typed (via `ObjectiveResumeContract`),
(e) as stated, and (f) single decider. Missing: (d) `resume_rechecks_today`, because there is no law on the
path, and (f) `resolution_grants_nothing`, which is vacuous until capabilities exist. (e) is proved but
proves the wrong behaviour (D-1).

---

## 3. Design disputes, with replacement text

**R1 — §B, the resume view (replaces the `Conflict` mechanism).** Paste in place of "revalidates the read
versions it recorded (stale: re-run and a typed `Conflict`)" in §1 and §B decision, and step (4) of the
§B resume turn:

> A resume delivers the pair `(outcome, view)`. `view` is the current value, at the resuming turn's
> snapshot, of every declared-state cell the activity's Plans may write. It is read in the resuming turn
> and becomes the activity's new read set. The outcome is never replaced or dropped. Because the next
> Plan's writes are computed in the same turn as the read they depend on, no write is ever derived from
> a stale read. Staleness is information (`view` differs from what the activity last wrote), not an outcome.
> `Conflict` leaves the outcome sum. A Plan may omit `state` (no write). An activity whose logic needs
> "only if unchanged" states it as a law clause (`leOld`/`eq` on old slots), which the kernel judges.

Why: Bread's guarded hole committed exactly the write its guard was checked against, in one step
(`holeFill_binds_in_circuit`, BREAD §2.1 #1); ICP's await bugs were check-then-act across a commit (§B
"Why"). Delivering the fresh read with the resume closes the gap, including between two activities of one
object; withholding it makes a lost update certain.

**R2 — §D `call`: apply fragments at frame return, not at the end of the turn.** Replace "Each frame reads
the turn's snapshot; writes are deferred in fragments and applied in call order at the end. A frame whose
read set contains a cell that another frame's fragment writes aborts the turn" with:

> Each frame reads the turn's current state: the snapshot plus every fragment already applied in this
> turn. A callee's fragment is applied to the turn's journal when its frame returns, and the whole
> journal is discarded if the turn is refused. Because re-entry into an object on the stack is refused, no
> frame can observe a write made by a frame still below it, and no object's state can change while its
> own frame is suspended in a call. So applying at return is safe without a frame-conflict abort.
> Laws judge each written object on (state at turn start, state at turn end). Two-state atoms read the
> turn-start value as `old`.

Why: with deferred fragments, A calling `B.deposit` twice reads the snapshot both times and aborts under
D2. Bread applied effects as it walked the forest, with a journal and rollback (BREAD §1.1), as do Mina
and Daml. The re-entry guard exists precisely to make that safe.

**R3 — §D `send` and forwarding.** Add after "forwarded inside the resolving turn":

> Every send escrows its own postage and envelope when it is made. A send queued on an unresolved slot
> keeps its escrow there. Forwarding charges each forwarded send to its own escrow, never to the
> resolver. A slot's queue has a fixed maximum length; a send to a full queue is refused at send time. If
> the slot resolves to anything other than a reference, every queued send resolves `broken
> NotAReference`, and its postage returns. The decider of a send's slot is a role, not a subject: the
> send hands it to the delivery, and the delivery to the callee's turn.

Why: Bread's relay bounded its queues (BREAD §1.2 item 8); unescrowed forwarding bills the resolver.

**R4 — §D pipelines.** Add: "Every partially signed segment carries a `valid_until` height, and the
composed turn is refused after the smallest of them." This is Bread's partial-commitment signing, which
bound federation and nonce (BREAD §1.4). Without it, a signer's segment that failed today can be admitted
whenever it would succeed later.

**R5 — §F, the escrow rung belongs across domains.** Replace "escrow quotas (local quotas summing to the
budget) let many activities draw on one balance" with:

> Inside one domain, delta actions plus Block-STM validation already give the sequential result for a
> shared balance, so no quota is needed for correctness. The coordination grade there only predicts
> re-execution. Escrow quotas are for parties or replicas that must spend without consulting each
> other: across domains, offline, or on committee replicas. There they are Stingray's bounded counters
> (Sridhar, Sonnino, Kokoris-Kogias 2025, arXiv:2501.06531), with the `(f+1)/(2f+1)` ceiling when slices sit
> on Byzantine replicas.

Why: Bread ran Stingray for exactly the cross-silo case (BREAD §1.4); the single-machine principle
(BREAD §2.1 #12).

**R6 — ROOT resolution C1 (two-phase upgrade).** ADOPT pins the new package "for new activities" while the
state stays unmigrated. If the state type changes, new activities and `call`s would then run the new
package against the old schema. Replace step (1) with:

> (1) ADOPT: if the declared state type is unchanged (or a row subtype), ADOPT and MIGRATE are one turn,
> and old and new activities coexist. Otherwise the object enters `draining`: births and calls are
> refused with `Upgrading(deadline)`, sends wait in the inbox, and only old activities run, until the last
> ends or the drain deadline aborts it with `Upgraded`. Then MIGRATE runs and the inbox drains on the new
> package.

Everything else in §C stands. In particular, the Book being outside declared state makes Bread's
`migrate_conserves` structural rather than a theorem (BREAD §1.5). The frozen-at-creation upgrade policy
closes Bread's factory-transparency versus `SetProgram` contradiction (BREAD §2.2).

---

## 4. The OPEN questions

**1. Synchronous cross-principal `call`: yes.** Bread was the experiment without it: cross-cell children
were `DelegationDenied` and `ParentsOwn`/`Inherit` never got built (`execute_tree.rs:1415-1455`, READ),
composition fell back to client-computed effects, and the result was ember's "lamesauce" (BREAD §0). The safety case is the re-entry guard *plus R2*: with apply-at-return, the only interleaving a
callee can cause is one the guard already forbids.

**2. Laws: generate from `.obend` now.** Same as BREAD §3.2. Bread's mirrored Rust and Lean law languages
drifted (dispatch rules, `EffectKindIs`; BREAD §1.1), which is the cost of two shapes. Generation from one
source avoids it; unifying into a general Objective Bend fragment would have to re-earn `Pred.Sat`.

**3. REPLAY: agree with the provisional drop.** Nothing in Bread argues for it (its cross-turn
"continuations" were whole turns re-run from the pre-state, BREAD §1.6).

**4. Build order: insert R1 before sends.** Answer slots and the resume contract have landed.
1. The next activity change should be R1, because sends multiply concurrent writers and D-1 then bites on
   every inbox delivery.
2. Then `call` (L5), which needs no slots.
3. Then `send` as a `message` source on the *same* record and slot machinery (the code already reserves
   it), never a second async path.

---

## 5. Commits, and the quest I want next

**No commits.** Both defects sit in `Kernel/ObjectiveActivity.lean`, which the running "activity native
route (ownership, Book fees, GC at yield)" lane is editing. R1 changes the response protocol the kernel
types against, `Tally.obend`, the Python driver's scenario B, and two theorems. That exceeds "small,
well-scoped", and racing the lane would cost the root a merge. (This laptop's volume is 99% used, 113 GiB free; I wrote
only this file and a scratch clone.)

**QUEST: RESUME-WITH-VIEW** (to take after the native-route lane lands, on its tip).

- **Scope, `Kernel/ObjectiveActivity`:**
  - The response datum becomes `{outcome: Outcome, view: S}`, where `S` is the type of the Plan's `state`
    field, read from `planType`. `birth` refuses a response type that is not this record.
  - `deliver` reads the object state cells at the snapshot, types them at `S`, and records them as the
    new read set.
  - `conflict` leaves `AwaitOutcome` and `kernelOutcomes`.
  - `PlanAwait.state` becomes optional.
  - `Answer.refused` and `Answer.broken` carry a finite reason sum (D-3).
  - The package check is cached by pin at `publish` (D-5).
  - If the native-route lane has not already done it, the object state cell is derived under a kernel tag
    from the object id, so no request can name a kernel cell (D-2).
- **Other modules:** `ObjectiveResumeContract` restated. `world/activity/Tally.obend` handles `view`. The
  demo's scenario B is inverted.
- **Theorems:**
  - `resume_outcome_preserved`: the delivered outcome equals the settled one.
  - `resume_view_current`: `view` is the snapshot value.
  - `yield_write_from_current_read`: every state post's expected root equals the root the same turn
    delivered in `view`.
  - The tooth: delivering `view` from the record's stale read set makes the demo's owner write vanish.
- **Acceptance:**
  - Scenario B now shows the owner's 99 *and* the decider's 7 (state 106).
  - A two-activities-on-one-object scenario keeps both activities' writes.
  - Full gate `lake build Minidregg +Host.Main:leanArts ObjectiveProofs` on hbox via `swarm-build`.
  - The demo is re-run with every check green.

Beyond my report I cite only Stingray (arXiv:2501.06531; metadata checked via the arXiv API, not downloaded).

---

## Appendix (2026-10-05, after the root's ruling): RESUME-WITH-VIEW, exact statements and the new Tally

This appendix follows the ruling (`ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`, final section). It is written
against `Kernel/ObjectiveActivity` at 36fca3ac. Names that ACTIVITY-NATIVE or OBJECT-RECORD will introduce
are marked **(tip)**; the lane renames them to whatever lands. Nothing here is built yet.

### A.1 Shapes

- **Object state cell (tip).** The object's declared state lives in `stateCell object`, a kernel-namespaced
  cell holding `ObjectState := { version : Nat, value : Data }`. Every committed write sets
  `version := version + 1`. Birth may create the cell (version 0 → 1); nothing else may.
- **The response.** The program's response type `R` must be a sum with exactly one member, `resumed`,
  whose payload is a record `{outcome : O, view : V}`.
  - `V = {version : Nat, state : S}`, where `S` is the declared state type.
  - `O` is the outcome sum: `reply : T | refused : Refusal | unknown | timedOut | broken : Breakage | upgraded`.
  - `Refusal` and `Breakage` are kernel-fixed sums. Today they are `Refusal = decider` and
    `Breakage = decider | dependency | notAReference`; the `send` lane fills the later members.
  - `replyType` becomes the `reply` member of `O`.
  - `birth` types every kernel outcome × a sample view at `R`, as `kernelOutcomes` does today.
  - `conflict` is deleted.
- **The write.** A Plan names a write, not a state.
  - `W(S)` has one field per field of `S`, each of type `Edit(T) = keep | set : T | add : T`. `add` is
    allowed only for `Nat`/`Int` fields; `set` writes a value; `keep` writes nothing.
  - `PlanAwait.state : Data` becomes `PlanAwait.write : Data`, typed at `W(S)` by the actual checker.
  - `applyWrite : Data → Data → Option Data` applies it to `view.state`, field by field, and is pure.
  - An all-`keep` write posts nothing.
- **Version check.** The state post is a CAS against the root the view was read from, in the same turn.
  A moved version makes the whole delivery refused (`stalePreRoot`), and the delivery is retryable: a fresh
  delivery reads the fresh view. A Plan never carries a version: the kernel binds it.
- **Birth is never blind.** The first segment runs with no view. Its write may use `set` only when
  `stateCell object` is absent (creation); otherwise any `set` is refused `blindWrite`, and `add`/`keep` are
  admitted.
- **The read set** of a record becomes `[stateCell object at the root the delivery wrote, or read if keep]`.
  `staleCount`, `revalidate` and `AwaitOutcome.conflict` are deleted.

### A.2 Theorem statements (to be pinned with `#assert_axioms`)

```lean
namespace Minidregg.Kernel.ObjectiveActivity
variable {rootBytes : Bytes → Digest} {config : Config} {snapshot : Snapshot rootBytes}
  {height : Nat} {request : DeliverRequest}

/-- The settled outcome reaches the activity unchanged: no kernel path
replaces, drops or rewrites it. (Replaces `stale_reads_conflict` and
`current_reads_exact`.) -/
theorem resume_outcome_preserved (delivery : Delivery config snapshot height request) :
    delivery.outcome = delivery.settlement.decided

/-- The view the activity is resumed with is the object's declared state and
version AT THE DELIVERING SNAPSHOT, and it is exactly what the response datum
carries. -/
theorem resume_view_current (delivery : Delivery config snapshot height request) :
    ObjectState.decode (snapshot.canonicalBytes (stateCell delivery.record.object)) =
        some ⟨delivery.view.version, delivery.view.state⟩ ∧
      delivery.response.datum =
        .variant "resumed" (.record [("outcome", delivery.outcome.data),
          ("view", .record [("version", .natural delivery.view.version), ("state", delivery.view.state)])])

/-- Every state write a delivery commits is computed from the view it
delivered, in the same turn: its expected pre-root is the root the view was
read from, its version is the view's plus one, and its value is the Plan's
write applied to the view's state. -/
theorem yield_write_from_current_read (delivery : Delivery config snapshot height request)
    {state : State} {plan : PlanAwait} (yielded : delivery.segment = .yielded state plan)
    (writes : plan.write ≠ keepAll) :
    ∃ post ∈ delivery.posts, ∃ value,
      post.cellId = stateCell delivery.record.object ∧
      post.expectedRoot = snapshot.model.roots (stateCell delivery.record.object) ∧
      applyWrite plan.write delivery.view.state = some value ∧
      ObjectState.decode post.bytes = some ⟨delivery.view.version + 1, value⟩

/-- The ruling's "refused if the version moved": a delivery prepared on one
snapshot is never accepted on a snapshot where the state cell moved, under any
schedule. (From the durable executor's pre-root check; the lane cites the
existing lemma.) -/
theorem moved_version_refused (delivery : Delivery config snapshot height request)
    {state : State} {plan : PlanAwait} (yielded : delivery.segment = .yielded state plan)
    (writes : plan.write ≠ keepAll) (later : Snapshot rootBytes)
    (moved : later.model.roots (stateCell delivery.record.object) ≠
      snapshot.model.roots (stateCell delivery.record.object))
    (schedule : DurableCommitProtocol.Schedule) (after : Snapshot rootBytes) :
    DurableDataIntent.execute schedule later delivery.intent ≠ .accepted after

/-- Sequential composition: a delivery built on the snapshot a previous
installed intent produced sees that intent's write (the second activity of one
object never works from the first one's pre-state). -/
theorem view_sees_prior_write {first : DataIntent rootBytes} {next : Snapshot rootBytes}
    (installed : DurableDataIntent.execute .complete snapshot first = .accepted next)
    {post : Post} (member : post ∈ first.posts)
    (delivery : Delivery config next height request)
    (same : post.cellId = stateCell delivery.record.object) :
    some ⟨delivery.view.version, delivery.view.state⟩ = ObjectState.decode post.bytes

/-- Deltas commute: two `add`-only writes applied in either order give the
same state (what lets two activities' replies both land). -/
theorem add_writes_commute (s : Data) {w₁ w₂ : Data} (h₁ : addOnly w₁) (h₂ : addOnly w₂) :
    (applyWrite w₁ s >>= applyWrite w₂) = (applyWrite w₂ s >>= applyWrite w₁)

/-- Birth is never blind: a first Plan with a `set` field is refused unless it
creates the state cell. -/
theorem birth_set_requires_creation {request : BirthRequest}
    (born : Birth config snapshot height request) {state : State} {plan : PlanAwait}
    (yielded : born.segment = .yielded state plan) (hasSet : setsSomeField plan.write) :
    ObjectState.decode (snapshot.canonicalBytes (stateCell request.object)) = none
end Minidregg.Kernel.ObjectiveActivity
```

**Teeth** (each must turn a theorem or a demo check red):
- Restoring `revalidate` to replace the outcome breaks `resume_outcome_preserved`.
- Reading the view from the record's stored read set instead of the snapshot breaks `resume_view_current`,
  and scenario B ends at 12 instead of 106.
- Posting the state against the root recorded at the yield instead of the view's root breaks
  `yield_write_from_current_read`.
- Allowing `set` at birth on an existing object makes scenario E lose activity 1's initial state.

### A.3 The new `world/activity/Tally.obend`

The response is a one-member sum (`resumed`), so the existing `match perform(...)` form binds it; the
member, field and reason names are kernel-fixed. INFERRED: that the parser accepts a sum member whose
payload is `Nat` (`set: Nat`); if not, it becomes `set: {value: Nat}`.

```
edition ObjectiveBend 1
# A tally resident on the resume-with-view kernel. Each resume delivers the
# await's outcome together with a fresh view of the object's declared state
# and its version, read in the same turn. The tally writes DELTAS: a reply of
# `amount` is `add amount`, so a concurrent write by the owner or by another
# tally on the same object is kept, never overwritten. Its only `set` is the
# initial total, which the kernel admits only when the birth creates the state.
record State:
  total: Nat
sum EditNat:
  keep: {}
  set: Nat
  add: Nat
record Write:
  total: EditNat
record Start:
  init: EditNat
  decider: Nat
record Ask:
  decider: Nat
record At:
  at: Nat
sum Source:
  reply: Ask
  height: At
record Await:
  write: Write
  on: Source
  patience: Nat
sum Plan:
  await: Await
record Reply:
  amount: Nat
sum Refusal:
  decider: {}
sum Breakage:
  decider: {}
  dependency: {}
  notAReference: {}
sum Outcome:
  reply: Reply
  refused: Refusal
  unknown: {}
  timedOut: {}
  broken: Breakage
  upgraded: {}
record View:
  version: Nat
  state: State
record Step:
  outcome: Outcome
  view: View
sum Resumed:
  resumed: Step
def ask(start: Start, write: Write) -> Activity<Plan, Resumed, Nat>:
  match perform(Plan.await({write: write, on: Source.reply({decider: start.decider}), patience: 4n})):
    case resumed(step):
      match step.outcome:
        case reply(r): ask(start, {total: EditNat.add(r.amount)})
        case unknown(_): ask(start, {total: EditNat.keep({})})
        case refused(_): step.view.state.total
        case timedOut(_): step.view.state.total
        case broken(_): step.view.state.total
        case upgraded(_): step.view.state.total
def tally(start: Start) -> Activity<Plan, Resumed, Nat>:
  ask(start, {total: start.init})
```

### A.4 Demo changes (`native/resource-client/objective-activity-demo.py`)

- **A** is unchanged in substance: born with `init: set 0`, reply 5, state 5.
- **B, the acceptance check:** the owner writes 99, the decider replies 7, and the delivery yields
  `reply` with view total 99. **The state is 106.** A further reply of 4 gives 110. A delivery prepared
  before the owner's write and submitted after it is refused `stalePreRoot`. A fresh delivery then
  succeeds.
- **C** is unchanged.
- **D:** born with `init: set 40`; the timeout returns 40.
- **E, new:** two tallies on one object. E1 is born with `init: set 0`, and E2 with `init: keep` (E2 born
  with `set 0` is refused `blindWrite`). E1 receives reply 3 and E2 receives reply 4, in either order:
  **the state is 7** and both records advance. A version-0 view is never delivered after a write.

### A.5 As implemented (lane/resume-view 46b9d4fd on activity-native 9c9608b0; COMPILED and lane-gated 9642 jobs; merge keeper gated it as 67362781 in batch c2; EXECUTED: not yet, needs the native route)

These names differ from A.1–A.2; the code is authoritative.

- **`Kernel/ObjectState.lean`** (new; SCHOLAR-OS imports it rather than defining its own):
  `ObjectState {version, value}`, frame `DREGG/OBJECTIVE/OBJECT-STATE/v1`, `objectState_roundTrip`,
  `decodeObjectState_canonical`.
- **The state cell is ACTIVITY-NATIVE's protected `stateCell domain object`.** It now holds an
  `ObjectState`, read by `readState`: absent → `none`, foreign bytes → `stateCodec`.
- **`stateWrite config snapshot object current viewed write`** is the single point where a declared-state
  write is built. It returns `StateWritten {before, after, post}`; SCHOLAR-OS's `admitWrite` wraps it.
- **Writes.** `Edit = keep | set | add`. `decodeWrite` takes a record of field edits, each field named once.
  `applyWrite`:
  - all `keep` → no write;
  - absent state → every edit must `set`;
  - present state → every edited field must exist, and `add` applies only to naturals.
- **Removed:** `Record.reads` (record frame v3), `staleCount`, `revalidate`, `AwaitOutcome.conflict` and
  `conflictReplyType`.
- **Delivery:**
  - it carries `view` and `viewExact`, and the response is `responseData settlement.decided view`;
  - its guards always include `stateCell`;
  - the yield is built with `(some view) true`.
- **Birth:**
  - it carries `current`; the yield is built with `current false`;
  - it guards `stateCell`;
  - a yielding birth must type the view it leaves (`viewProtocol`);
  - `outcomeProtocol` checks the `resumed {outcome, view}` shape.
- **`writeState`** installs version + 1.
- **Theorems:**
  - `resume_outcome_preserved`: stated from the decided slot to the delivered response.
  - `resume_view_current`: `viewExact`, plus an accepted delivery leaves the state cell's root unmoved
    between the delivering snapshot and the commit.
  - `yield_write_from_current_read`.
  - `moved_state_refuses`.
  - `stateWrite_unviewed_never_sets`.
  - Helpers: `accepted_posts_current`, `accepted_guards_current`, `Delivery.posts_current`,
    `settle_posts_current`, `stateWrite_spec`, `commitYield_spec`, `segmentCommit_spec`.
  - Deleted: `stale_reads_conflict` and `current_reads_exact`.
  - `add_writes_commute` IS stated and proved (with `editField_add_comm`, `editFields_add_comm`; `applyWrite`
    now uses a recursive `editFields` instead of `mapM`).
- **Tally.obend** is as in A.3 except that `EditNat.keep()` takes no argument. Evidence: parsed and
  elaborated locally with bun at b31d8be8's frontend.
- **Acceptance** (`objective-activity-native-acceptance.py`):
  - scenario "view": a delivery prepared before the owner's write is refused; the fresh delivery gives
    total **106** at state version 4;
  - scenario "two tallies": a birth that `set`s present state is refused `blindWrite`, and a `keep` birth
    joins; **total 7**.
