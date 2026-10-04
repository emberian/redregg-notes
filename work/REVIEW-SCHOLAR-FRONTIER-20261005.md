# REVIEW-SCHOLAR-FRONTIER (2026-10-05): Agoric's lessons and the 2022–26 frontier, against the design and main

Read: `designs/MINI-PROGRAM-MODEL-20261004.md` (all), `work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md` (with the
root's resolutions), the ledger rows for 796d7d7a and the activity kernel, and the code, from a fresh read-only
clone of main `36fca3ac`: `Kernel/ObjectiveActivity.lean` (all 1,161 lines), `Kernel/AnswerSlot.lean`,
`Kernel/ObjectiveBendNativeAdmission.lean`, `Host/ObjectiveConsent.lean`, `Compiler/ObjectiveInvocationClaim.lean`
and `world/activity/Tally.obend`. My evidence is in `work/SCHOLAR-FRONTIER-AGORIC-20261004.md`, cited below as
FRONTIER. Nothing was committed. The reason is in §4.

## 1. Verdict

The design took Agoric's lessons nearly whole, and the landed activity kernel gets the hardest ones right
(consume-once at the decide point, mandatory deadlines, a typed outcome sum, measurement-free refunds, parking on
exhaustion). One design sentence turned into a landed defect,
however. The defect is enshrined as a theorem and demonstrated by the reference resident. When an activity's reads
go stale, the kernel destroys the decided reply, and the activity has no way to learn the current state, so its
next yield silently overwrites a concurrent writer. Three of my lessons are not met by main yet, though none is yet
contradicted by a design text: law judging the activity's writes, a payer for every retention cell, and pricing of
kernel work. They must be requirements on the native-route lane that is running now, not later lanes.

## 2. What the design and the code got right (in my domain)

- **Linear resolution authority** (FRONTIER §1.2), as code. A delivery spends the await claim and CASes the record
  in one intent. A slot is decided once by its one decider. Retries are replays. This is stronger than Agoric's
  rule, because the decider is a cell that an upgrade cannot kill.
- **Pinned checkpoints living as long as their awaits.** Every turn reloads the package by `record.pin` and takes
  the checkpoint only from the record cell. DRAIN is therefore already implemented by construction.
- **Park, don't terminate** (FRONTIER §1.4). `.suspended` becomes `.exhausted`, which commits nothing, and anyone
  may top up with `extraTicks`. Agoric had to retrofit this (#8955). Refunds are measurement-free
  (`refund_measurement_free`).
- **Typed outcomes, typed by the real checker.** At birth, every activity must type all kernel outcomes, so
  `upgraded` and `conflict` never surprise a resident at run time.
- **Guards before execution, and a dry-run quote.** The native route type-checks input before any demand runs.
  `Host/ObjectiveConsent` re-derives the whole signing plan and compares it byte for byte before signing (the
  Unison blueprint idea, FRONTIER 2.A A6).
- **Kernel work partly priced.** Native `Tariff.workOf` prices typeFuel and input/output bytes, which Agoric could
  not meter at all.
- **The design text** transcribes FRONTIER's seats, scoped grants, method guards, legibility, dispositions decided
  inside the upgrade turn, and the absence of a superuser.

## 3. What is wrong or missing, with replacement text

### 3.1 DEFECT (landed): a stale read destroys the decided reply, and the resident cannot recover (design §B, T1(e))

**What the code does.** `revalidate stale decided := if stale = 0 then decided else .conflict stale`
(`ObjectiveActivity.lean:807`). The slot was already decided by its one decider, so its `decisionClaim` is spent.
The await claim is spent too. The reply is therefore gone for good. `AwaitOutcome.conflict` carries only a count.

**It fires on every multi-activity object.** The only recorded read is the activity's own last write (line 528),
and every yield replaces the whole declared state, so two activities on one object stale each other every turn.

**The reference resident shows it.** `Tally.obend` has `case conflict(_): tally(start)`: the decided `amount` is
dropped, and the next yield writes the stale `start.total` over the other writer. The kernel accepts this, because
the CAS is against the *current* root.

This is ICP's check-then-act failure (CALLS E4) one level up. Agoric never loses a resolution: a vow's
settlement is delivered whatever else changed (FRONTIER §1.12). The cause is T1(e), "receives `Conflict`, never the
bare outcome". Scribe note B2 had asked for `Conflict(stale cells, outcome)`; the root's resolution kept the
constructor and dropped the payload.

**Replacement text, §B Decision, the sentence on stale reads:**
> Resume revalidates the read versions it recorded. If any is stale, the activity is resumed with
> `Conflict { decided : Outcome, current : DeclaredState, stale : List CellId }`. It carries the outcome its await
> actually resolved to (never discarded, because the slot decision and the await claim are spent) and the current
> committed value of every stale cell the activity may read. A resident can then merge or retry. It can never
> lose a reply or overwrite a write it has not seen.

**Replacement for T1(e):**
> `stale_reads_conflict`: if a recorded `ReadGuard` differs from the current root, the activity is resumed with
> `Conflict` whose `decided` field equals the outcome the await settled to and whose `current` field equals the
> committed bytes of each stale cell. *Tooth:* a delivery after a concurrent `writeState` that drops `decided`, or
> that delivers a stale `current`, fails the test.

**Typing.** Use `decided : Option Reply` plus a tag for the non-reply outcomes, so the response type stays
non-recursive (Core4 Plans and responses "must be non-recursive data").

**Companion rule for §A/§F.** An activity's Plan writes *fields* or *deltas* of declared state, not the whole
record. Its recorded reads are the fields it read, not its own write. Otherwise "several activities per object"
(F) means "every activity conflicts with every other".

### 3.2 GAP (landed): no law judges an activity's writes; ownership is derived from payment (design §A, §E, §H)

**No law.** `ObjectiveActivity.lean` contains no law check; a yield's `statePost` writes the object cell
unjudged, and `birth` lets any subject write any object (ledger). "Code proposes, law disposes" is not yet true for
activities, and the running native-route lane lists ownership, Book fees and GC, but not laws.

**Ownership comes from payment.** `writeState` refuses with `.notOwner` unless
`request.subject = record.escrow.payer`. The owner is whoever funded the first activity. That conflates the
*meter* with *authority*, which KeyKOS separated on purpose and which Agoric keeps separate: whoever holds the meter
does not hold the object (FRONTIER §1.4; HIST 1F). A sponsor who pays for someone's resident must not become its
owner.

**Replacement text, §A Mechanism, after the `ObjectRecord` block:**
> Every write a Plan makes to an object's declared state (from a method turn, an activity yield, or a resume) is
> judged by the object's law in the same intent, exactly as a native write is. No activity turn is admitted on an
> object without an `ObjectRecord`. Authority over an object (owning it, writing it, upgrading it, terminating it)
> comes only from capabilities named in its `ObjectRecord` and checked by its law. Paying for a turn, an escrow or
> a deposit grants no authority.

### 3.3 GAP (landed): retention cells without a payer, and unpriced kernel work (design §G)

The activity kernel creates five kinds of cell that nothing ever reclaims and nobody holds a deposit for:
- record cells (a `done` or `faulted` record keeps its result forever);
- decided slot cells;
- package cells;
- fee-account cells;
- checkpoints, which grow (4,359 → 4,991 B over two resumes, per the ledger).

The escrow price is `base + perTick · ticks` only. It ignores the checkpoint bytes it encodes and decodes, and the
full re-check of the package (`loadProgram` → `checkWithin` + `check`, under `config.typeFuel`) that every
`resolve` and every `deliver` performs.

This is FRONTIER §1.4–1.5 in miniature (Agoric #8400: an unpaid retention structure held about 60% of mainnet kv).

There are also now two tariffs, `ObjectiveActivity.Tariff` (base, perTick) and `ObjectiveBendNativeAdmission.Tariff`
(nine terms including typeFuel), plus two money rails: the fee-account cells "stand in for the Book". That is two
shapes that agree today, and the repo doctrine says to delete one.

**Replacement text, §G Mechanism, appended:**
> One tariff prices every Objective turn (method, birth, resolve, deliver): the native `Tariff.workOf` terms plus
> `checkpointBytes` (encode and decode) and the package re-check's `typeFuel`. The activity kernel's own tariff and
> its fee-account cells are deleted when escrow binds to the Book.
>
> Every cell the activity kernel creates (record, answer slot, checkpoint, package) carries a storage deposit
> posted by a named payer in the turn that creates or grows it. The deposit is priced from the bytes written and
> returned in full when the cell is removed. That is a deposit, not a measured refund, so it is consistent with
> G1. A record reaches `done` or `faulted` and its result is collected by its owner, or a decided slot is consumed
> by its delivery. Either turn removes the cell and returns its deposit. No cell outlives its last reader without
> someone paying for it.

### 3.4 MISSING (design §E): seats have no invitation, no instance binding and no reallocation authority; and the `offerSafe` sketch is wrong at zero

**The zero bug.** `offerSafe` builds `.not (.le (bookSlot seat a) (n - 1))` with `n : Nat`. For `n = 0`, `0 - 1 = 0`
in `Nat`, so "want 0 of A" becomes "hold at least 1 of A". A zero-amount keyword therefore makes the refund branch
unsatisfiable after any debit. Agoric's `AmountMath.isGTE(x, 0)` is always true.

**The design never says who may debit a seat.** In Zoe only two paths move a seat's allocation:
- the contract instance, through `atomicRearrange`, under offer safety and conservation;
- the offerer, through `exit` (`zcfSeat.js:244–270`; FRONTIER §1.10).

**The design binds the seat to no contract.** It has no invitation, which is the exclusive, assayable right naming
the instance, the installation and the terms. That right is what lets an offerer know *which code* will reallocate
its escrow (Miller 2013 §6; FRONTIER §1.9–1.10).

**Replacement text, §E "Mechanism: seats":**
> ```lean
> def atLeast (slot : Slot) (n : Nat) : Pred := if n = 0 then .all [] else .not (.le slot ((n : Int) - 1))
> def offerSafe (seat : AccountId) (p : Proposal) : Pred :=
>   .any [ .all (p.want.map fun (a, n) => atLeast (bookSlot seat a) n),
>          .all (p.give.map fun (a, n) => atLeast (bookSlot seat a) n) ]
> ```
> An `invitation` is an exclusive, assayable capability `{instance : ObjectRef, package : Digest, role : Label,
> terms : Data}`, minted only by the instance's own turns. `offer invitation proposal` spends the invitation like a
> nullifier in the same turn that creates the seat, so the offerer has assayed the instance, package, role and
> terms it is playing.
>
> A seat account may be debited only (a) by a posting in a turn of the seat's instance, judged by `offerSafe` and
> Book conservation, or (b) by the kernel `exit`, which posts the whole allocation to the offerer. A reallocation
> is one Plan action over several seats of one instance (Zoe's `atomicRearrange`). Every seat it touches is judged
> by its own law, and the Book posting algebra balances the action.
>
> ABORT of an activity, and termination of an instance, `exit` every open seat of that instance. Neither may
> strand escrowed assets.

### 3.5 RISK (design §C and the root's C1): the two-phase drain re-creates "failure discovered after commit"

C1's MIGRATE turn re-judges the new law on a state old activities kept writing after ADOPT. If it fails, the
object is stuck between versions: the "wishful thinking" class of Agoric #12315 and #12138 (FRONTIER §1.11–1.12).
The refinement moves a check out of the upgrade turn.

**Replacement text for C1, appended:**
> While an object is draining, every turn that writes its declared state is admitted only if `migrate s'` type-checks
> at the new state type and satisfies the new law, where `s'` is the state the turn would commit. The kernel
> computes this in the same turn and charges it in the turn's envelope. MIGRATE is then total by construction, and
> its admission cannot fail. If the ADOPT turn's own check of `migrate s` fails, the upgrade is refused at ADOPT.

### 3.6 Smaller corrections

- **§D, pipelines and consent.** The landed consent path (Core227) makes the caller sign the exact Plan, so any
  concurrent change refuses the invocation; two of the 13 refusals were `stale-root`. Write it down: exact-plan
  signing is the default caller protection for single-turn invocations. Seats are the protection that tolerates
  movement (a price changed, a balance moved). A pipeline signer signs its segment's exact sub-Plan, or a seat.
  Without seats, every trade in a busy domain will retry forever.
- **§3, the theorems.** Add **T0, Agreement**, which the ledger names as open ("meaning not proved unique"). Admission
  needs a deterministic big-step semantics whose result is unique. That is the vWasm split (FRONTIER 2.D D1): the
  sandboxing theorem must not depend on it, and replica agreement does. Until T0 exists, the card should label
  native receipts with the regime that settled them, as the ledger's receipt label already does.
- **§H.** Show each activity's decider on the card; today nothing shows viewers who can answer an await.

## 4. Commits

None. The two code defects (§3.1, §3.3) sit in `Kernel/ObjectiveActivity.lean`, which the running "activity native
route" lane is rewriting (ownership, Book fees, GC at yield). A parallel edit would collide with it. §3.1 is also a
design-sentence change (T1(e)) that needs the root's ruling first. I am handing both to that lane as acceptance
requirements (§5) instead.

## 5. Acceptance additions for the running activity-native-route lane

1. A delivery after a concurrent write yields `Conflict { decided, current, stale }`, and `Tally.obend` merges the
   reply. The test: two writers, both contributions survive.
2. Every activity Plan write is law-judged. A violating Plan refuses the delivery and leaves the await unspent.
3. `writeState` and `birth` require an object capability, not payer identity.
4. One tariff for all Objective turns, including checkpoint bytes and re-check typeFuel.
5. Record, slot and checkpoint cells carry deposits and are removed when collected.

## 6. The four OPEN questions

**OPEN 1: synchronous cross-principal `call`. Yes, under one condition.** Agoric's "never synchronous across trust
boundaries" is a statement about *shared-stack* JavaScript. In SES "the ses shim does not in itself isolate the
stack", so getters and proxies re-enter mid-operation, and Agoric's defence is a clean stack (FRONTIER §1.7). The
design's `call` differs on both counts: the callee reads the turn's snapshot, its writes are deferred fragments,
and re-entry is refused. A callee therefore never observes a caller's half-done state, which is the property
Agoric's clean stack buys. The condition: writes stay deferred and reads stay on the snapshot. If a later change
lets a callee see the caller's in-turn writes, the answer flips to no. Put the condition in T2 as a statement:
`frame_reads_snapshot`.

**OPEN 2: generate laws now, unify later.** Agoric is a single-language system (all JavaScript), and it still built
a separate, decidable pattern language (`@endo/patterns`, the `M.*` matchers) for guards, state shapes and
proposals rather than run arbitrary JavaScript predicates (FRONTIER §1.8). Cedar did the same (LAWS D1). Two
production systems with every incentive to unify chose a small decidable sublanguage. Generate `Pred` clauses from
`.obend` declarations now. The first concrete step is the missing one in §3.2: get `Pred` judging activity writes
at all.

**OPEN 3: REPLAY. Keep it dropped.** Agoric's replay disposition is where its two most recent production failures
sit (#12138 chain halt, October 2025; #12315, January 2026). Mini already has DRAIN by construction (§2, pins
reloaded every turn). Make DRAIN's MIGRATE total with the invariant in §3.5 and REPLAY buys nothing that ABORT plus
a re-birth does not.

**OPEN 4: build order. Fix the resume contract first, then seats and scoped grants, then `call`.** Answer slots and
the resume contract came first, and that order was right (Agoric retrofitted durable promises in three layers). But
the first residents must not be built on reply-losing conflicts, unjudged writes and unpaid cells (§5), because
everything later inherits them. Next, seats with invitations (§3.4) and scoped grants. Seats do not need `call`,
they relieve the exact-plan consent path of its stale-root retries (§3.6), and `call`'s safety argument (OPEN 1)
leans on grants. `call`, then pipelines, then protocol objects; cross-domain last.
