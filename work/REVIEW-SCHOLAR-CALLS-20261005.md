# REVIEW-SCHOLAR-CALLS (2026-10-05)

Scope: the three call forms, answer slots, the resume contract, deterministic parallel admission,
coordination grades, deal cells and upgrade dispositions.

Inputs:
- the design as of this morning (`designs/MINI-PROGRAM-MODEL-20261004.md`, 1,520 lines, with the 10-05
  merges);
- `work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`;
- the five reviews already filed (BREAD, FRONTIER, HIST, LAWS, OS);
- the landed code, read at minidregg `36fca3ac` in a fresh clone on hbox: `Kernel/ObjectiveActivity.lean`
  (1,161 lines, all of it), `Kernel/AnswerSlot.lean`, `Kernel/ObjectiveResumeContract.lean`,
  `Host/ObjectiveActivityWorld.lean` (skimmed).

I do not repeat the stale-read defect (four reviews found it; the root ruled "resume with view"). Citations of the form "CALLS X" point into my report (`work/SCHOLAR-CALLS-CONCURRENCY-20261004.md`).

## 1. What is right

- **Consume-once sits exactly where Khan says it must.** `deliver` puts three things in one `DataIntent`:
  - the await claim (`awaitClaim`, a `StableNullifier` over `H(record cell, generation, checkpoint digest)`);
  - a compare-and-swap on the record cell (`postAt snapshot request.record …`, prior = current root);
  - one transaction id per await (`deliveryTransaction await.id`).

  That is a claim taken at the read/decide point, the only repair that worked in Khan's measurements
  (CALLS C6: 2,628 fires where 400 were expected; write-path repairs failed twice). The theorems
  `resume_consumes_once` and `second_delivery_refused` quantify over *every* later intent and *every*
  schedule, so they are not identity carriers: their premises are the kernel's own `execute`.
- **The answer slot matches CALLS idea 2.** The name is `H(turn, record cell, generation)`, i.e. a call
  site no submitter chooses (Ozone, CALLS A8). There is one decider. The slot is write-once twice over
  (cell CAS and claim). Expiry is "anyone, strictly after the deadline". `decide_single_decider` and
  `stranger_refused` have named inhabitants (`sample_*`).
- **Refunds are measurement-free.** `refund_measurement_free` is the right statement of the root's G1 rule.
- **Checkpoints come from the kernel's own run.** `resume_binds_checkpoint` accepts no state parameter,
  and `birth/delivery_checkpoint_typed` reduce the before-root check to codec validity plus the digest
  binding. That is Scribe note B3, proved rather than asserted.

**Khan's six properties against the landed kernel:**

| Property | Landed | Evidence |
|---|---|---|
| PC prefix continuation | yes | `resume_binds_checkpoint` |
| EO effect exactly-once (internal) | yes | Plan write and checkpoint in one intent (`execute_no_partial_data_commit`) |
| FD fork determinism / FI | not offered, correctly | Khan's Lemma 1 (CALLS C6): with no wire discriminator, FD and CO conflict; one transaction id per await picks CO |
| CV checkpoint validity | per step only | `delivery_checkpoint_typed` *assumes* the decoded checkpoint was typed (`prior`); no invariant over reachable states discharges it (§2.2) |
| CO-c / CO-e | yes | above; an exact retry replays (`installed_retry_replays`), anything else is refused loudly |
| RD recovery determinism | yes | `resume_deterministic` |
| Liveness | **no** | §2.1 |

## 2. What is wrong or missing

### 2.1 Defect (fixed in my commit, §5): a resumed program's own fault wedges the activity forever

`runSegment` turns `divergent` and machine `refused` into `.faulted`, which commits. But four other
failures are *refusals*, so nothing commits:
- `decodePlan` errors (`plan "await.state missing"`, `"the kernel performs only await Plans"`);
- `planExtraction` and `resultExtraction`;
- `commitYield`'s `patience` and `"a height await is due after its deadline"`;
- `messageAwaitNeedsInbox`.

Resumption is deterministic (`resume_deterministic`), so every later delivery of the same await meets the
same refusal. The timeout delivery is included, because it too resumes the program. The record stays
`awaiting` forever and the escrowed fee pair is locked forever. This violates Khan's liveness obligation
(CALLS C6) and Herlihy–Liskov–Shrira's weak liveness, "no asset … escrowed forever" (CALLS G1).

A resident that yields `{patience: 0}` after its first reply is enough to trigger it. The design's own text
(§B: "a deterministic failure in the resumed segment … commits a `faulted` phase") already says what the
code should do. No other review caught it; §G's disposal turn would reap it only after the grace period, once built.

The same class covers a segment that cannot reach a yield within the *turn cap*. A delivery whose envelope
already equals `config.maxTicks` and still exhausts can never run in any turn. Exhaustion *below* the cap
stays a refusal (a bigger envelope may run it). HIST F3's charge for exhausted deliveries is
complementary, not overlapping.

### 2.2 CV holds per step; the invariant is missing, and namespace confusion is what would break it

`delivery_checkpoint_typed` takes the typing of the decoded checkpoint as a hypothesis. The theorem that
discharges it for every reachable world is "every record cell decodes to a record whose checkpoint is
typed at its program's checked type", by induction over `publish | birth | resolve | deliver |
writeState`. It has not been stated.

It is not provable on the scratch kernel, for a reason the design ruled on but did not connect to CV:
- `BirthRequest.object` is any `CellId`, and `writeState` writes `record.object`.
- So a birth naming *another activity's record cell* as its object overwrites that record with data
  bytes at its own first yield (`commitYield`'s state post); `writeState` can do it again later.
- The victim's next delivery fails `decodeRecord` (`recordMissing`): wedged, with its escrow locked.
- Naming an `accountCell` instead destroys a balance.

The 10-05 ruling ("state cells live in a kernel namespace") is load-bearing for CV and liveness, not only
for authority. **Acceptance test for ACTIVITY-NATIVE:** the reachable-state CV invariant, proved.

### 2.3 Resume-with-view: the version check is either vacuous or Block-STM validation

The ruling has two parts:
1. A resume delivers a fresh view, read in the delivery turn.
2. "A Plan state write is refused if that version moved since the view."

The continuation runs entirely inside that one turn, so under the sequential fold nothing can move the
version between view and write: the check never fires. Under parallel admission it fires exactly when an
earlier turn in the batch wrote the cell, which is Block-STM read-set validation (CALLS E7). So:
- **(a) Build it once.** It is the parallel-admission validation, with the view as a recorded read. Do
  not build a second mechanism.
- **(b) Delete `Record.reads`.** With a fresh view per resume, the stored reads have no remaining reader.
  Keeping both is the "two shapes" defect the repo's doctrine forbids.

What the view does *not* fix is check-then-act across a yield. An activity can ignore the view and act on
heap-held data from an earlier turn. Only the law stops that. Say so in §B, so nobody reads the view as
isolation.

### 2.4 Upgrade: three gaps

1. **View typing during a subtype drain.** When old <: new, births and calls use the new package while
   drained activities still run old code. New code may write values outside the old type, such as a new
   variant member. The drained activity's next view then fails to type at its old declared state type,
   which is §2.1's wedge again by another route. Rule: a view or outcome that fails to type for a drained
   activity resolves that activity to `Upgraded` (abort) in the delivery turn. It never refuses.
2. **REBIRTH must never refuse MIGRATE.** If the old record's `input` does not type at the new package's
   domain, that activity falls back to ABORT. Otherwise MIGRATE is no longer total, which defeats the
   §C "making MIGRATE total" rule.
3. **REPLAY stays dropped: I concur, and withdraw my idea 8's replay disposition.** Mini keeps the
   checkpoint, not the `(Plan_i, Response_i)` log. The delivery event records only the outcome *label*,
   so the log would be new paid retention. HIST's record of Agoric #12315/#12138 outweighs the benefit.
   REBIRTH covers the restartable residents, needs no log, and is the better trade.

### 2.5 Calls: the root's D2 rule needs its scope stated, and one misquote is mine

- **Scope.** "Two frames of one turn writing the same slot abort the turn unless the slot's law declares
  the write a commutative delta" is right *within one turn*. It must not be read as applying *between
  turns of a batch*: there, writes apply sequentially in log order and write-write never aborts. Aria
  aborts write-write only because it installs writes in parallel (CALLS F4), and the design rejects
  Aria's semantics.
- **My misquote.** "10 of ~100M Ethereum executions were legitimately reentrant", in decision D1, came from
  my final relay message. My report's text (Part II.6, E1) says non-ECF. Scribe note D1's correction is
  right: the cost of refusing ECF re-entry is unmeasured.

## 3. Replacement text for the scribe

**§B, replacing the paragraph after "As amended by the root's ruling of 10-05 (resume with view)":**

> Every resume delivers its outcome with a fresh view of the object's declared state, read in the
> delivery turn and recorded as that turn's read. Under the sequential fold nothing can move it before the
> turn's own write; under parallel admission (§F) an earlier turn of the batch can, and Block-STM
> validation then re-runs the delivery. That is the version check, and there is no other. `Record.reads`
> is deleted. The view gives freshness, not isolation: an activity that acts on heap data from an earlier
> turn is constrained only by the law. Plans write fields or deltas, not whole records. `conflict` leaves
> the outcome sum.

**§B, replacing "A deterministic failure in the resumed segment (blackhole, machine refusal) commits a
`faulted` phase …":**

> A failure the resumed program itself causes commits a `faulted` phase, returns the unused escrow, and
> sends a fault message to the object's keeper. Such failures are: machine divergence or refusal, a Plan
> or result that does not decode, a patience outside its bounds, an await kind the kernel cannot serve,
> a view or outcome that does not type at the activity's declared types, or no yield within the turn
> cap. Resumption is deterministic, so refusing any of these would refuse every later delivery of the
> same await and lock its escrow forever (Khan's liveness obligation; Herlihy–Liskov–Shrira's weak
> liveness). `resumedSegment_never_refuses_program_fault` states it. A delivery is refused only for
> causes outside the program: funding, an envelope below the turn cap, a missing or mismatched slot, or
> a spent claim.

**§3 T1, add (g):**

> (g) `reachable_records_typed`: in every world reachable from genesis by admitted kernel turns, every
> record cell decodes to a record whose checkpoint decodes to a state typed at its program's checked type.
> This discharges the `prior` hypothesis of `delivery_checkpoint_typed`. *Tooth:* a birth naming another
> record's cell as its object is refused (kernel namespace, §A).

**§C, add after the drain-deadline sentence:**

> While a subtype drain runs both packages, a drained activity whose view or outcome no longer types at
> its old declared types is resolved to `Upgraded` in that delivery turn, never refused. A REBIRTH whose
> stored input does not type at the new package's domain falls back to ABORT, so MIGRATE stays total.

**§D (`call`), add to the D2 rule:**

> This rule is within one turn. Between turns of a batch, writes apply in log order and write-write never
> aborts (§F).

## 4. The OPEN questions

**OPEN 1: synchronous cross-principal `call`. Yes.**

Agoric's "never synchronous" answers a hazard Mini's `call` does not have. In E/SES a synchronous callee
runs on your stack, sees your heap mid-update, and can suspend and come back (CALLS A1 §13.1; Goblins
footnote 16, CALLS A6). Mini's callee is different:
- it reads the turn's *snapshot*;
- its writes are *deferred* fragments;
- an `Activity` method cannot be called, so no frame suspends;
- re-entry is refused.

So the DAO shape is excluded twice: once by the guard and once by the frame-conflict rule. T2's DAO tooth
must show *each* is load-bearing (remove one, keep the other, see which example commits). Production
precedent: Mina's value-returning child updates (CALLS E18), Daml exercise trees (E5), Tezos depth-first
(E2). Grossman found 0.004% non-ECF executions on Ethereum history (E1).

The cost that remains is failure attribution, Miller's "aborting the wrong plan": a callee's law refusal
aborts and charges the caller's whole turn. Make it explicit:
- refusals name the failing frame and its law clause (blame);
- a caller who will not underwrite the callee uses `send`.

**OPEN 4: build order. Repairs first, then send, then call.** The root's list omits `send` and inboxes.
Today an answer slot's only decider is a subject, so slots are half a mechanism. Proposed order:
1. Resume-contract repairs: the view ruling; the program-fault commit (§5); HIST F3's exhausted charge;
   ACTIVITY-NATIVE's namespace and ownership, with `reachable_records_typed` as acceptance.
2. L2 recursive Plan data and collection at the yield (every multi-action form needs it).
3. L3 objects, facets and declared state, *with* ADOPT/MIGRATE. Nothing long-lived should exist before
   it can be upgraded.
4. `send`, inboxes and slot deciders as roles (BREAD D-4). This finishes the one await primitive before a
   second call form; Bread's five unconnected async mechanisms are the warning (BREAD §0).
5. `call`, scoped grants and the output gate, with T2.
6. Parallel admission with T4. Call frames define footprints, so it comes after `call`. It is otherwise
   independent and can run alongside.
7. Pipelines; seats and deal cells; protocol objects; cross-domain pipelining last.

FRONTIER put seats before `call`, and I would not fight that. The firm point is send before call.

## 5. Commit, and an infrastructure hazard

**The commit.** `8d1d3c0e` on `lane/scholar-calls`, hbox `/tank/dregg-build/claude-lanes/scholar-calls/src`,
rebased on main `36fca3ac`, unsigned, not pushed. It implements §2.1:
- `programFault` classifies the program-caused refusals;
- `resumedSegment` replaces `runSegment` plus `segmentCommit` in `deliver`;
- `Delivery.endExact` replaces `segmentExact` and `yieldedExact`;
- the new theorem is `resumedSegment_never_refuses_program_fault`, with `resumedSegment_yielded` and three
  teeth (`plan_fault_commits`, `funding_is_not_a_fault`, `exhaustion_below_cap_is_not_a_fault`);
- `resume_binds_checkpoint`, `resume_deterministic` and `delivery_checkpoint_typed` are restated;
- birth is unchanged.

**Evidence.**
- *Compiled:* `lake build Kernel.ObjectiveResumeContract Host.ObjectiveActivityWorld` reports "Build
  completed successfully (3211 jobs)" (`logs/scoped-4.log`), and every new theorem is pinned with
  `#assert_axioms`.
- *Executed (regression only):* `objective-activity-demo.py` passes 46 of 46 steps against the patched
  executable (`demo-run-1/results.json`, `"failed": []`).
- *Not yet executed:* the new fault path. That needs a resident that yields a malformed Plan after a reply,
  and I would add it as demo scenario E.
- *Possible conflict:* the scholar-bread-meta lane appends theorems to `ObjectiveResumeContract` that do not
  touch the renamed fields, so a merge conflict is unlikely.

**Hazard: warm-base lanes silently build against stale oleans after a rebase.**
- **What I saw.** After `mk-lane.sh` plus a fetch of main (71 commits past base `9ccd6a2d`), lake did not
  rebuild `Theory/TypedAuthorization` or `Theory/AssertAxioms`, although both sources changed. It reported
  them up to date, and even `lake build Theory.TypedAuthorization` was a no-op. Downstream modules then
  failed with "Unknown constant `CellField.atomsOf`" (19 errors in `CredentialAuthorityEntryCodec`, which
  the scholar-fn and scholar-bread-meta lanes also logged) and "environment already contains
  `AssertAxioms.standard`".
- **The dangerous case.** A module that *happens* to compile against the stale olean gives a false green.
- **Workaround.** Delete the lane's `.trace` file for every `.lean` changed since the base (64 files), then
  build. I did this, and it is how `scoped-4` was produced.
- **The fix belongs in `mk-lane.sh`.** Either do it automatically after a fetch, or refresh the base itself.
  Cause unknown; I did not chase it.
