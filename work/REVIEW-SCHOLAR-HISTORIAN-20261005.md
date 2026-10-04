# REVIEW-SCHOLAR-HISTORIAN (2026-10-05)

**Domain.** What the builders of persistent capability systems learned. Evidence:
`work/SCHOLAR-HISTORIAN-CAPABILITY-SYSTEMS-20261004.md` (HIST §; every quote there has a re-fetchable key).

**What I read:** the design (§A–C, G–I, §4–5); `work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`; and the code at main
`36fca3ac` (`Kernel/ObjectiveActivity.lean` from `8194e09d`, `Kernel/AnswerSlot.lean`,
`Kernel/ObjectiveResumeContract.lean` from `7494ca13`, `Host/ObjectiveActivityWorld.lean`), not the commit messages.
No builds and no commits (see the end).

## Verdict

The root's resolutions draw the right lessons: declared durable state, no MAP, REPLAY dropped, meters as
accounting, epoch change = re-genesis. The landed activity kernel's checkpoint handling is sound, in ways KeyKOS's
builders would recognise. But the code repeats three mistakes the record names:
- **(1)** the continuation carries a copy of the durable state and writes it back after a `conflict` (Electric
  Communities' "the runtime representation becomes the schema");
- **(2)** exhaustion is free;
- **(3)** finished, faulted and unfundable activities are never disposed of (Agoric's #8400 and #8955 class).

The design text has not absorbed the root's §C resolutions, and the resolved two-phase upgrade runs new code on
the old schema during the drain.

## What the design and code got right (keep these)

1. **The checkpoint is the kernel's, never the client's:** `deliver` decodes only the record cell's own bytes
   (`resume_binds_checkpoint`), the program is re-loaded and re-checked from its content-addressed cell every turn,
   and stored checkpoints are typed by theorem (`delivery_checkpoint_typed`). This is KeyKOS's rule that the kernel
   never relies on application code "Not even application code from the system TCB" (Shapiro 2005, HIST 1E), and it
   answers Shapiro's "stray pointer errors … *will* survive" (HIST 1A).
2. **Consume-once at the decide point,** with the nullifier bound to the checkpoint digest
   (`resume_consumes_once`); the yield, its Plan writes and the next await commit in one `DataIntent`. This is
   Waterken's output commit and Miller's "hangover inconsistency … don't do it" (HIST 1A), made a theorem.
3. **Measurement-free refunds from declared envelopes** (`refund_measurement_free`), as reproducible as KeyKOS's
   meters ("one of the neat tricks", Frantz 2019, HIST 1F).
4. **A fault ends the activity, not the object.** Agoric killed the vat and later had to invent suspension (#8955).
5. **Typed outcomes, checked at birth** (`kernelOutcomes`): Shapiro's "(value|exception)" unions and E's broken
   promises (HIST 1D).
6. **No MAP, epoch change = re-genesis, meters as accounting** all match the record (HIST 1C, 1F).
7. **The record keeps `input`,** which makes REBIRTH (F6) free.

## What the design and code got wrong or missed

### F1. Durable state is still neither declared, typed nor owned in the landed kernel (code; design §A, L3)

- **What the code does.**
  - `commitYield` writes the Plan's own `plan.state` over the object cell.
  - `writeState` writes untyped `request.value`, checked only against the *activity's fee payer*.
  - `birth` accepts any object cell and any pin, so activities of different packages (different schemas) can
    alternately overwrite one object.
  - The pin lives on the activity, not the object.
- **Why it matters.** Shapiro, 2008: KeyKOS/EROS "don't have anything analogous to a schema, and I have come to see
  this as a failing" (HIST 1B). Electric Communities and Smalltalk failed because whoever wrote last defined the
  schema. Hardy's space-bank check ("so that X cannot interfere with Y's logic", HIST 1E) is the ownership half.
- **Demand.** No native route may expose `birth` or `writeState` until `Kernel/ObjectRecord` exists, carrying the
  object's single pin and its declared state type and version.
  - `commitYield` types `plan.state` at the declared type;
  - `writeState` is deleted.
- **Build order.** L3 comes before the native route (OPEN 4).

### F2. A `conflict` hands the activity a count, not the current state; the activity then writes back state derived from its copy (code; design §B)

- **The sequence.** `revalidate` turns stale reads into `conflict stale`, a bare count. The activity has no way to
  read the object, so its next `plan.state` comes from the copy in its heap. The delivery guards the *current*
  roots (`guardAt snapshot guard.cellId`), so that write commits over the interleaved write.
- **The result:** a lost update, beside a theorem (`stale_reads_conflict`) proving the activity was *told*.
- **What the record says.**
  - "Never a mutable alias of object state" is not enough: an immutable *copy* held across a yield is Electric
    Communities in miniature, where "the entire runtime representation becomes the schema" (Miller, HIST 1B).
  - It is also Waterken's 2011 replayed-read bug (HIST 1D).
  - Agoric and Goblins read durable state from the store at use.
  - ACTIVITY-NATIVE's planned `Conflict(stale, outcome)` still gives no current state.

**Replacement text for §B (capture rule), to paste after "never a mutable alias of object state":**
> A continuation never carries a copy of its object's declared state across a yield. Every resume delivers, with the
> outcome, the object's current declared state at its declared type (`Resumed { outcome, state, version }`), and
> every Plan state write names the version it was computed from; the kernel refuses the write (`Conflict`, the turn
> commits nothing else) if the object's state moved since that version. `conflict` is therefore a rebase signal
> that carries what to rebase onto, and no activity can commit a state derived from a superseded version.

### F3. Exhaustion is free (code; design §G "parks")

- **The code.** `runSegment` returns `.error .exhausted` on `.suspended`, and `deliver` then refuses the whole turn.
  Nothing commits: no fee is charged to the escrow, the submitter's `extraTicks` or anyone else. A resident whose
  resume always runs out of its envelope can therefore be delivered to forever at zero cost, and the Host pays for
  every attempt.
- **The record.** KeyKOS decrements the meter as the domain runs (Hardy 1985, HIST 1F); Agoric charges the crank
  and then terminates; gas systems charge the consumed envelope. None charged nothing.
- **This is measurement-free** under the root's G1 rule. The envelope was *declared*, so charging its full declared
  price on exhaustion depends on no measured quantity.

**Replacement text for §G, replacing the sentence starting "For an activity, a refused resume commits nothing":**
> For an activity, a resume that exhausts its declared envelope commits an `exhausted` receipt: the full declared
> price of the envelope it ran under is consumed (from the escrowed fee for the path, plus any submitter-added
> envelope), and the checkpoint, the await and the record's generation are unchanged, so the activity is parked at
> its yield with a fresh escrow required for the next attempt (`AwaitsFunding`). Exhaustion is never free and never
> refunded; the charge is a function of the declared envelope only.

### F4. Parked and finished activities have no terminal disposal (code; design §B, §G)

There are three related gaps:
- **A finished or faulted record is retained forever.** `nextRecord` zeroes its escrow, but the record cell
  (`input`, `result`) stays, with no payer.
- **A parked activity has no exit.** One that no one funds keeps its checkpoint and its escrow forever; past the
  deadline, `settle` keeps offering the timeout path, but if that path also exhausts, nothing ever ends it.
- **Two retention structures have no lifecycle:** the answer slot of an aborted activity, and the escrow of an
  activity that never resumes.

The record: KeyKOS's "junk queue" needed "outside repair" (Frantz 2018, HIST 1F); a leaking safety feature held
about 60% of Agoric's store (#8400); killing bloated vats risked the chain (#8928); suspension was invented after
the fact (#8955); "All the garbage in a waterken system gets persisted too" (Stiegler, HIST 1B).

**Replacement text for §G, appended to "Every retention structure … is a cell with a payer":**
> Every activity ends in a disposal turn. A `done` or `faulted` activity's record is deleted in the turn that ends
> it (its result lives in that turn's receipt). An activity parked past its deadline plus a fixed grace height may be
> abandoned by anyone: the turn closes its open slots as `expired`, frees its checkpoint, consumes the timeout fee
> and returns the rest of its escrow to the payer, and resolves nothing further. Abort (§C) uses the same disposal.

### F5. The two-phase upgrade as resolved runs new code on the old schema (root resolution C1; design §C)

- **The problem.** The ADOPT turn "pins the new package for new activities" while "the object's declared state is
  NOT migrated while any old activity remains". So every activity born, and every call made, between ADOPT and
  MIGRATE runs the new package against the old schema. Agoric met exactly this: a lazy migration "must be prepared
  to handle arbitrary messages despite the migration not being complete" (vat-upgrade doc, HIST 1C). Their builders
  say this is the hard part, not the easy one.
- **What the record supports.**
  - KeyKOS checked for upgrades only "when the stack is (nearly) empty" (Frantz 2008).
  - Erlang's second code load purges old processes; that purge is the deadline.
- **The fix.** The object is *closing* between ADOPT and MIGRATE. New work queues or is refused with a typed
  `Upgrading`, and only after MIGRATE does the new package run.

**Replacement text for §C (Decision and Mechanism), replacing the single-turn decision:**
> Upgrade is two governed turns and a bounded interval. (1) ADOPT records the new pin, the migration and the new
> law, all checked as below, and a mandatory drain deadline height; from ADOPT on the object is `closing`: no
> activity is born on it and new calls and sends to it are refused with `Upgrading` (sends may instead wait in its
> inbox, unpaid work never runs). (2) Old activities run on their pinned package against the unmigrated state until
> their awaits end or the deadline passes; at the deadline anyone may abort the remainder (each await resolves to
> `Upgraded`, disposal as in §G). (3) MIGRATE, admissible only when no old activity remains, writes the migrated
> state, re-judges the law, installs the new pin and bumps continuity, all at once; only then does the new package
> run. Dispositions are DRAIN-with-deadline, ABORT and REBIRTH (below); there is no MAP and no REPLAY. A Core4 or
> codec epoch change is a re-genesis.

### F6. With REPLAY gone, the obligation it served has no home: add REBIRTH and make restartability checkable (design §C; OPEN 3)

- **What is lost.** Dropping REPLAY is right (it needs a log Mini does not keep; Agoric's #12138 and #12315 sit
  there), but then a bug-fix upgrade aborts every long-running resident.
- **What the builders did instead:** restart services from durable state. NLTSS processes were "restartable without
  loss of objects and their capabilities" (Donnelley 2008); Frantz ranks "new version, discard the old" (2a) first;
  Agoric: "preserve long-term state, but abandon any work that was in-progress" (HIST 1C).
- **Mini already has the parts:** a record keeps its birth `input`, and durable state is declared.

**Text to add to §C, under Dispositions:**
> REBIRTH: abort the old activity (`Upgraded`, disposal per §G) and, in MIGRATE's turn, birth a new activity on the
> new package from the old record's `input`, against the migrated state, with the old payer's remaining escrow. It
> needs no log and no replay. A resident package may declare itself `restartable`; publish then requires a test
> (run in CI, not at admission) that abort-and-rebirth from declared state alone reaches the same declared state
> under the same deliveries, so "this service survives an upgrade" is a checked claim rather than a hope.

### F7. The design text has drifted from the root's resolutions (design §C, §I, §4)

- §C still offers `replay` in `Disposition`, a REPLAY executor in its Cost, and one upgrade turn; root C1 and C2
  supersede all three. Use F5's text.
- §I still says fn carries "checkpoints at cadence" and "replay kits". Root §I says "NO checkpoints of any kind in
  fn". Strike "checkpoints at cadence".
- §4 "Upgrade dispositions" still reads "REPLAY only if it succeeds within the upgrade turn". Change it to:
  "Decision C follows HIST: DRAIN-with-deadline, ABORT and REBIRTH; no REPLAY, no MAP."

### F8. Smaller points

- **Slot lifecycle under ABORT.** Abort must decide the activity's open slot (`expired`), or a decider can later
  decide a dead slot. This is Miller's rule of severing live references across an upgrade (HIST 1C).
- **Faults go nowhere yet.** `faulted` records a string; Tribble's keeper model (HIST 1G) wants it sent to the
  object's keeper.
- **Checkpoint growth** (4359 → 4991 B over two resumes) is partly F2's carried copy of state, which collection at
  the yield cannot remove.

## Answers to the OPEN questions (my domain)

1. **Synchronous cross-principal `call`: yes.** The record supports the root's lean more strongly than the design
   says.
   - KeyKOS, EROS and Coyotos ran synchronous CALL/return between mutually suspicious domains for decades, inside
     one failure domain.
   - A domain that is busy serving a call queues further callers on its stall queue rather than re-entering (Hardy
     2018, HIST 1F). That is Mini's "re-entry refused" by another name, and it shipped.
   - What the KeyKOS family learned was about the reply authority: "The ability to transfer the authority to *reply*
     is fairly essential. This was a pretty fundamental design mistake in Mach IPC" (Shapiro 2021). EROS resume
     capabilities also "sever the session" after one reply (2005).
   - Agoric's "never synchronous across trust boundaries" is a distributed-failure rule ("Persistence stops at the
     machine boundary") and belongs on cross-domain links.
2. **Laws: generate from `.obend` now.** This is mostly outside my domain. Morningstar's 2004 point applies: put
   persistence "into the language syntax as a first-class concept" (HIST 1B). Declarations belong in `.obend`
   syntax either way.
3. **REPLAY: drop it, and add REBIRTH (F6).** The strongest evidence:
   - Agoric #12315, 2026: parking a failed replay is "wishful thinking";
   - Agoric #12138: a related durable-state bug halted the chain in 2025;
   - the replay log Mini does not keep (scribe note C2);
   - every builder's own fallback was rebuilding from durable state (NLTSS, Frantz 2a, Close, Agoric).
4. **Build order:** slots and resume contract (landed), then **L3 `ObjectRecord`** with F1–F4, then upgrade with
   REBIRTH, then `call`. Frantz: "get the upgrade path for the space bank right in the first release" (2008); Agoric
   retrofitted durable promises, zones and suspension in three layers. The activity surface is now ahead of the
   object model it writes into.

## Commits and quests

**No commits.** F2–F4 touch `deliver`, `commitYield` and fees, which ACTIVITY-NATIVE is editing now. The local data
volume is also at 98% (113 GiB free of 7.3 TiB), under the protocol's 10% stop line; I wrote only this file.

**Quest I want next: ACTIVITY-STATE-REBASE**, to start after ACTIVITY-NATIVE lands.
- **Scope:**
  - F2: `Resumed { outcome, state, version }`, plus versioned Plan state writes refused on a moved version;
  - F3: an `exhausted` receipt charging the declared envelope;
  - F4: disposal turns (delete on done/faulted; abandon after deadline plus grace; slot expiry);
  - `writeState` deleted.
- **Modules:** `Kernel/ObjectiveActivity`, `AnswerSlot`, `ObjectiveResumeContract`, `Host/ObjectiveActivityWorld`.
- **Acceptance:**
  - new theorems `no_write_from_superseded_state` (a committed Plan state write's base version equals the
    pre-state's), `exhaustion_charges_declared` and `disposal_frees_record`;
  - the demo shows the lost-update interleaving refused, a looping resident charged per attempt, and an abandoned
    activity's escrow returned;
  - full gate on hbox (`Minidregg +Host.Main:leanArts ObjectiveProofs`).
- **After that:** REBIRTH as part of the L3/upgrade lane.
