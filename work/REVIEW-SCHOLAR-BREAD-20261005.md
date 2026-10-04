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
6. **One async mechanism.** The answer slot plus the activity record is the only wait path, and `message`
   is reserved to join it. This avoids Bread's five unconnected mechanisms (BREAD §2.2).
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

**D-5: kernel work per resume is unpriced.** Every `deliver` (and `resolve` with a reply) re-runs
`loadProgram`: the full `checkWithin` of the package plus a re-check of the instantiation. That is paid by
nobody: the escrow prices ticks only. Anyone may submit deliveries, so this is the "unpriced kernel work"
decision G rules out. A cache keyed by `pin` (checked once at `publish`, as the
`ObjectiveBendSourceArtifact.Checked` value already proves) removes it. INFERRED fix.

**D-6: answer-slot cells have no payer and are never reclaimed.** A decided slot outlives its activity.
Design G: "every retention structure is a cell with a payer".

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

**1. Synchronous cross-principal `call`: yes.** Bread is the controlled experiment for "no in-turn
call". Its cross-cell children were `DelegationDenied` unless `SnapshotRefresh`, and `ParentsOwn`/`Inherit`
were never implemented (`execute_tree.rs:1415-1455`, READ; BREAD §1.2). Composition fell back to
client-computed effect lists (`invoke()`), and the user-level result was ember's "lamesauce … i am a toy"
(BREAD §0). The safety case is the re-entry guard *plus R2*: with apply-at-return, the only interleaving a
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
- **Est.:** one lane; touches one kernel module, one theory module, one `.obend` and one script.

Beyond my report I cite only Stingray (arXiv:2501.06531; metadata checked via the arXiv API, not downloaded).
