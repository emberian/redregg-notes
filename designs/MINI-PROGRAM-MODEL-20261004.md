# Mini's program model (2026-10-04)

This document turns the root's decisions (`work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`) into
the design of Mini's program model. It changes no decision. Where a decision conflicts with the
evidence or with another decision, the decision stands and a **Scribe note** states the conflict for
the root and Ember to resolve. The root resolved all thirteen Scribe notes on the night of 10-04
(decisions file, "Root resolutions"); each note below now carries its resolution, and the text applies
it. On 10-05 eight scholars reviewed revision 2 and the landed code; the root then ruled on their
findings (decisions file, "Root rulings on the 2026-10-05 scholar reviews"). Revision 3 applies those
rulings and merges the reviews' consistent replacement text with attribution. Where a review disputes a
decision and the root has not ruled, a **Review dispute** box in §7 quotes both sides. Revision 2
reads Mini at main `36fca3ac`; §0 records what landed since revision 1 (main `6f82b818`), and the
changelog at the end lists every change. Scholar reports are cited by short name and section: BREAD
(`SCHOLAR-BREAD-PROGRAM-MODEL`), META (`SCHOLAR-BREAD-METATHEORY`), LAWS (`SCHOLAR-LAWS-CONTRACTS`),
CALLS (`SCHOLAR-CALLS-CONCURRENCY`), OS (`SCHOLAR-OS-LINEAGE`), FRONTIER (`SCHOLAR-FRONTIER-AGORIC`),
HIST (`SCHOLAR-HISTORIAN-CAPABILITY-SYSTEMS`), FN (`SCHOLAR-FN-STORAGE-NODE`) and ROOT
(`ROOT-READING-NOTES-PROGRAM-MODEL`). Every primary source named here is in the cited scholar entry,
with its paperbin path.

---

## 0. What landed between revision 1 and revision 2 (main `6f82b818` → `36fca3ac`)

Read at source in a fresh clone of main `36fca3ac`, with the swarm ledger
(`work/SWARM-LEDGER-20261004.txt`, 12:40 onward) for the evidence each lane recorded.

- **The cut** (main `5b6d6eca`). Gen-1 Objective Bend, `Command.bend` and the BendTT command path left
  main; `ObjectiveProofs` became its own build target.
- **BendTT deleted** (main `9ccd6a2d`: `212c79af`, `b91abe35`). 241 Lean files and about 22,000 lines
  of BendTT-side code and artifacts are gone, including `Kernel/BendActivity*`. Core4's activity is now
  the only activity in the tree. Re-derive tasks were filed for the useful parts (`01a1065a-4f5d`
  ACTIVITY-CORE4 among them).
- **First native Objective accepted receipt** (main `796d7d7a`, 12 commits; module
  `Kernel/ObjectiveBendNativeAdmission`). A published `.obend` program ran through admission on a
  scratch world, charged `proofWork` equal to the tariff price of the signed, declared envelope, with the
  elaborator and lowerer pinned in the package identity, 13 named refusals that leave roots unchanged,
  and Core4 disableable by configuration. Breaking: package frame 1→2 and policy frame 2→3. Still open:
  Core4 in `Compiler/Evaluator.registry` proper, a paid invocation (the funding leg is unexercised), and
  a private-return slot.
- **Activity kernel** (main `8194e09d`, `7494ca13`, `3667e07d`). `Kernel/ObjectiveActivityWire`,
  `Kernel/AnswerSlot`, `Kernel/ObjectiveActivity` and `Kernel/ObjectiveResumeContract` (in the
  `ObjectiveProofs` target) implement lane L1's core: the activity record cell (checkpoint bytes and
  digest, pinned package identity, generation, recorded reads, escrowed fee pair, phase); five turns
  (`publish`, `birth`, `resolve`, `deliver`, `writeState`), each one `DataIntent`; awaits on an answer
  slot or a height with a mandatory deadline; and the outcome sum with `conflict`. Theorems:
  `resume_consumes_once`, `second_delivery_refused`, `slot_decided_once`, `slot_single_decider`,
  `stale_reads_conflict`, `current_reads_exact`, `resume_binds_checkpoint`, `resume_deterministic`,
  `refund_measurement_free`, `birth_checkpoint_typed`, `delivery_checkpoint_typed`. The demo
  (`Host/ObjectiveActivityWorld`, `world/activity/Tally.obend`) passed 46 of 46 checks on a durable
  scratch world: reply, retry replay, double resume refused, forged spent await refused, stale read →
  `conflict`, tampered checkpoint refused, timeout. Not yet built: the native signed route, object
  ownership (in the scratch executable any subject can birth an activity on any object), fees on the Book (fee accounts
  are kernel cells standing in for it), collection at the yield (the Tally checkpoint grew from 4,359 to
  4,991 bytes over two resumes), upgrade dispositions, sends and inboxes (a message await is refused by
  name), and a `conflict` that carries the settled outcome. The ACTIVITY-NATIVE lane is building the
  first five.
- **Receiver collapse, first family** (main `66967962`, `2c8839d2`, `47e653ed`; design
  `docs/design/RECEIVER.md`, `4b69d228`). `Theory/Receiving` and `Kernel/Receiving` define one
  receiving pipeline with its laws proved once; subject-key rotation is its first family. Every new
  turn kind in this design (birth, resolve, deliver, call, send, offer, upgrade) should be a `Receiving`
  family, not a new receiver.
- **Refusal charging** (main `6455353d`, `39c1473b`). Authenticated refusals are charged to the signer's
  refusal lane (`Kernel/RefusalLane`), which §G's refused-resume rule relies on.
- **ZK truth** (main `a006d243`). The ZK tranche covers Core4 including sums and activities, one layout
  decoder (`LayoutCodec`) binds every region, and `docs/ZK.md` states the admission bar (B1–B9; today
  admission is re-execution only). Nothing in this design changes: admission stays re-execution.
- **Tenancy step B** (main `06ddad68`). A `mini-keys` broker holds signing secrets; it is the custody
  side of every signed envelope and grant in this design and changes none of its mechanisms.
- **Running, not landed:** ACTIVITY-NATIVE (signed route, ownership, Book fees, collection at the yield
  with a resume-equivalence theorem, `conflict` carrying the outcome), ELABORATOR (the Lean parser and
  elaborator become the implementation and the TypeScript front end is deleted, which moves lane L3's
  `state` declaration into Lean), AGREEMENT, SCHEMA-V2, DEPLOY-3.

---

## 1. The model in one page

**Objects.** An object is a cell with a stable id that is never its package hash. It holds declared
durable state (typed, first-order, versioned Core4 data, declared in mandatory `.obend` syntax), its
law, a package pin (interface type and package hash), an upgrade-policy capability fixed at creation
(frozen by default; it may only tighten), a continuity counter, its creators, its keeper, and its
activities. The law judges the declared state and an upgrade transforms only the declared state. The
state cells live in a kernel namespace; every write to them needs a facet capability of the object and
is judged by its law, and paying for a turn never confers authority.

**Activities.** An activity is a Core4 computation of type `Activity<P,R,A>` that yields a typed Plan
and waits. Mini keeps the exact whole-machine checkpoint (`Theory/ObjectiveBendCheckpoint`,
`state_roundTrip`). A checkpoint lives as long as its awaits, is pinned to the package hash that made
it, is storage-charged after collection at the yield, and is decoded and checked before the root
moves. It captures only immutable values, resources moved into it, and send-only references; it
never captures a mutable alias of object state or turn-scoped authority. A resume spends the await
id like a nullifier, bound to the checkpoint digest. Every resume delivers its outcome together with
a fresh view of the object's declared state and its version, read in the same turn; a Plan writes fields
or deltas, and the write is refused if the version moved since the view (resume with view, root ruling
10-05). Every await carries a height deadline, escrows the fees of its resume and timeout turns, and
resolves to exactly one of `Reply | Refused(reason) | Unknown | TimedOut | Broken(reason) | Upgraded`.
The kernel half of this landed overnight (`Kernel/ObjectiveActivity`, §0), with a `conflict` outcome
that the ruling removes.

**Calls.** There are three forms. `call` is synchronous and in-turn: the callee runs its pinned
package against the turn's state and returns a value and a Plan fragment, which is applied when its
frame returns and billed to the caller's envelope; calls run depth-first under Daml's authority rules,
and re-entry into an object already on the stack is refused. `send` is
eventual: a Plan action that enqueues on a per-(sender, target) FIFO inbox cell, each delivery its own
paid turn, breadth-first, with answer slots named `H(turn, call site)` that have exactly one decider.
A pipeline invocation is a signed, straight-line, non-recursive program of calls on capabilities and
prior results, re-executed as one turn; partially signed pipelines from several parties compose into
one turn. Signers attach scoped, counted grants that bound what nested code may do with their
authority. Nothing externally visible leaves a domain before its turn commits.

**Laws.** The decidable law language (`Pred`) stays the judge at every write: code proposes, law
disposes. It grows two-state atoms, request atoms, necessity sugar, action-scoped clauses and
past-time temporal laws compiled to kernel-maintained history slots. Laws apply at three points:
method guards before any code runs, state laws at every write, and proposals. An offer creates a
seat, a Book account whose law is offer safety for its whole life, with a kernel exit no contract can
override. A protocol object holds the remaining global type of a choreography as its state, and its
law admits exactly a legal next step for the signer's role. Clauses are deny-by-default, indexed by
method, forbid-overrides-permit, and carry a coordination grade computed at publish.

**Concurrency.** An object may have several activities; they share state only through committed
cells. Hot state splits into sub-cells with their own laws; exclusivity across a yield exists only as
a law-governed lease. Admission runs in parallel with Block-STM semantics: footprints are learned,
the root equals the sequential fold, and the dependency DAG is published. Coordination grades decide
which turns commute and who votes; escrow quotas let many activities draw on one balance. Across
domains, exclusive rights settle in a deal cell whose decision law is offer safety; everything else
runs as a choreographed saga.

**Upgrade.** An upgrade runs under a law-governed upgrade capability visible on the object's card, in
two phases. An ADOPT turn checks the new package, migration, law, floors and interface, and assigns every
live activity a disposition (DRAIN, ABORT or REBIRTH) or the upgrade is refused. While the object drains,
it admits no new births or calls unless the old state type is a subtype of the new, and an old
activity's write is admitted only if its migration type-checks and satisfies the new law. Drained
activities end by their awaits or at a mandatory drain deadline (aborted with `Upgraded`); a MIGRATE
turn, which therefore cannot fail, migrates the state, and large objects migrate over several turns while
closed. REBIRTH re-births an aborted activity from its stored input on the migrated state. REPLAY is
dropped and MAP is never offered. A Core4 or codec epoch change is a re-genesis.

**Metering.** Each invocation carries one signed envelope. A Lean cost theorem states that metering is
a function of pre-state and invocation and that the meter dominates machine transitions and kernel
work. Nothing measured is ever refunded; only measurement-free amounts (undelivered postage, the unused
half of an await's fee pair) are returned. Exhaustion charges the declared envelope and parks the
activity, whose resume needs a new envelope; it never terminates the object. Finished activities are
disposed of in the turn that ends them, and parked ones may be abandoned after a grace height. Meters account; they do not
schedule. Every retention structure is a cell with a payer; unfunded objects hibernate to their
Merkle hash.

**Presentation.** Every object answers `describe`, `affordances` and `history`. An affordance is
`Hidden`, `Disabled(reason)`, `Possible` (the law is satisfiable) or `Enabled` (a simulated admission
succeeds), so the card and admission share one decision. Receipts carry causal edges; unhandled faults go to the object's keeper.

**fn.** fn is Mini's archive, feed and transport for exact bytes now: bundled blocks and receipts,
replay kits, published packages and cross-domain messages, and never checkpoints. It moves under the
hot per-turn log only after fn's page representation and the `fn-store-1` freeze. The contract is
`designs/MINI-FN-660-REQUIREMENTS-20261004.md`.

---

## 2. The decisions, area by area

Each subsection gives the decision, the mechanism, the evidence, the cost and what the decision
rules out. Lean sketches use existing Mini names where they exist and mark new modules as **new**.

### A. Objects and state

**Decision.** An object is a cell with a stable id, never its package hash. It holds declared durable
state (typed, first-order, versioned Core4 data; the declaration is mandatory `.obend` syntax from day
one), its law, a package pin (interface type plus package hash), an upgrade-policy capability set at
creation (frozen by default; it may only tighten), a continuity counter, and its activities.

**Mechanism.** The object record is a new kernel cell, `Kernel/ObjectRecord.lean` (**new**):

```lean
structure ObjectRecord where
  id          : Kernel.Contracts.ObjectRef      -- its cell id; nothing derived from schema or package
  stateType   : Ty                              -- declared durable-state row, first-order
  schema      : Digest                          -- schema digest; mutable, changed only by MIGRATE (§C)
  stateVer    : Nat                             -- schema version, bumped by migration
  law         : Kernel.Contracts.LawRef         -- the law cell and its exact root
  pin         : PackagePin                      -- { interface : Ty, package : Digest }
  upgrade     : UpgradePolicy                   -- frozen | governed (law : LawRef) (floors : List Pred)
  continuity  : Nat                             -- bumped by every upgrade and law change
  creators    : List SubjectId                  -- signers of the birth turn, fixed for life (§D)
  keeper      : Option CapRef                   -- where unhandled faults go (§H)
  activities  : List ActivityId                 -- each an ObjectiveActivity record (§B)
```

The declared state lives in ordinary store cells; the record holds its type, not its bytes. The front
end gains a `state` declaration on `spec … for T` (in `native/bend-source/objective-parser.ts` and
`objective-elaborate.ts` today; in the Lean parser and elaborator once the ELABORATOR lane lands), and admission refuses an object kind without one. `UpgradePolicy` may move only to a
stricter `governed` or to `frozen`, and floors may only be added; the record's own law enforces both
(a `writeOnce`-style clause on the frozen flag, entailment on the floor list, §C). The declaration
refuses arrows, `Ty.custody` and `Ty.computation`, so no closure, thunk or activity enters durable state.

**Authority over an object (merged from reviews: FRONTIER §3.2, OS W1, LAWS D-3 and D-6, HIST F1; ruled 10-05).**
Object state cells live in a kernel namespace: an object's state cells are derived as `tagged
"OBJECT-STATE" (ObjectRecord.id, field)`, and no kernel turn accepts a raw `CellId` as an object, so no
request can name a record, slot, package or fee-account cell as "the object". Every write a Plan makes to
an object's declared state, whether from a method turn, an activity's birth, a yield or a resume, is
judged by the object's law in the same intent, exactly as a native write is, and must type-check
against `ObjectRecord.stateType`. No activity turn is admitted on an object without an `ObjectRecord`.
Authority over an object (writing it, upgrading it, terminating it) comes only from capabilities named
in its record and checked by its law. Fee payer, invoker and object authority are three separate fields,
and none implies another: paying for a turn, an escrow or a deposit grants no authority (Banga et al.'s
resource principal is not the protection domain, OS §5; KeyKOS kept meters and authority apart, HIST
1F). There is no owner-write turn: state changes only through a method of the pinned package or through
an upgrade, so the landed kernel's `writeState` is deleted when this lands. `creators` are the signers of
the birth turn and pre-authorize the consequences of the pinned package's methods, which is Daml's
signatory rule (§D).

**Why.** Every persistent capability system kept whole-machine persistence for crash consistency and
found it unworkable as the thing that migrates. Landau (1992, §8.2) wrote that KeyKOS upgrades "must be
planned in advance"; Frantz (cap-talk, 2008-03-16) called it "a choice between easy persistence and easy
upgrade" (HIST 1C). Morningstar (2006) reported that Electric Communities' migration of "save it all"
state "proved effectively intractable" and that they "fell back on a scheme that compelled programmers to
be much more deliberate about what state was checkpointed, and when" (ROOT; OS §3.6). Agoric discards
heaps at upgrade, and Miller (cap-talk, 2026-03-05) says its orthogonal persistence exists "just to
ensure that all honest validators produce the same deterministic computation" (HIST 1A). Croquet hashed
code into session identity, so every code change made a new world (OS Part I §1). Salehi et al. (2022)
found 48% of upgradeable Ethereum systems one signing key from a rewrite (CALLS H6).

**Cost.** It needs one record type, one front-end declaration form and one admission check. Authors must
state what persists; Agoric's lesson that "if v1 fails to retain something, v2 cannot get access to it"
(HIST 1C) makes that a day-one obligation rather than a later migration.

**Rules out.** It rules out objects whose identity changes with their code; durable state that contains closures;
upgrade authority held by an unnamed key; and the "heap / virtual / durable" zone taxonomy Agoric had
to retrofit (FRONTIER §1.6).

> **Scribe note A1 (identity). Resolved by the root.** `Kernel/Contracts/Identities.ObjectRef` has
> three fields, `native`, `domain` and `kind`, and documents `kind` as "the declared semantic kind
> (schema/kind digest)" (unchanged at `36fca3ac`). If `kind` were the schema digest, a migration would
> change the `ObjectRef`. *Resolution:* an object's id is its cell id and nothing derived from its
> schema; `kind` names the semantic kind, and the schema digest is a separate, mutable field (the
> `schema` field above). Lane L3 makes that split in `Identities`.

### B. Activities and checkpoints

**Decision.** Keep the exact whole-machine Core4 checkpoint for in-flight activities. A checkpoint lives
as long as its awaits, is pinned to the package hash that made it, is storage-charged after collection
at the yield, and is decoded and type-checked before the root moves. At a yield it may capture only
immutable values, resources moved in and send-only references; never a mutable alias of object state;
turn-scoped authority (signer grants, fee meter, handlers) never enters a checkpoint or a cell. Resume
spends the await id like a nullifier, bound to the checkpoint digest, and revalidates the read versions
it recorded (stale: re-run and a typed `Conflict`). Every await resolves to `Reply | Refused | Unknown |
TimedOut | Broken | Upgraded | Conflict` (the root added `Conflict`, resolution B2), carries a height
deadline, and escrows the fees for its resume and timeout turns.

**As amended by the root's ruling of 10-05 (resume with view).** Every resume delivers its outcome
together with a fresh view of the object's declared state, with its version, read in the same turn. A
Plan state write is refused if that version moved since the view (optimistic and retryable). Plans write
fields or deltas, not whole records. `conflict` leaves the outcome sum, and refused and broken reasons
are a small fixed sum delivered to the activity. This supersedes resolution B2 and revision 2's T1(e).

**Mechanism.** The language half was already on main: `Theory/ObjectiveBendDemandMachine` yields with
`Control.yielded plan`; `resume response state` is defined only on a yielded state and keeps heap and
stack (`resume_keeps_heap_and_stack`); `typed_yield_quiescent` makes every yield a safe point;
`stack_activity_signature` and `typed_resume_preserved` type the response; `state_roundTrip` restores
every state. The kernel half landed overnight in `Kernel/ObjectiveActivity` (§0). Its record, as built:

```lean
-- Kernel/ObjectiveActivity.lean (main 8194e09d)
inductive Source | reply (slot : Digest) (decider : SubjectId) | height (due : Nat)
structure Await where id : Digest; source : Source; deadline : Nat; yieldedAt : Nat
  -- id = awaitId (record cell) generation (checkpointDigest checkpoint)
structure Escrow where payer : SubjectId; resumeTicks timeoutTicks resumeFee timeoutFee : Nat
inductive Phase | awaiting (await : Await) | done (result : Bytes) | faulted (reason : String)
structure Record where
  object : CellId; activity : Digest
  pin : Digest                  -- ObjectiveBendSourceArtifact.identity of the producing package
  input : Bytes                 -- the program is re-instantiated and re-checked every turn
  generation : Nat
  checkpoint : Bytes; checkpointDigest : Digest   -- encodeState bytes, never a summary
  reads : List ReadGuard        -- versions the continuation depends on
  escrow : Escrow; phase : Phase
inductive AwaitOutcome | reply (value : Data) | refused | unknown | timedOut | broken | upgraded
  | conflict (stale : Nat)
```

The design keeps three additions to this record for later lanes: an epoch field (unneeded while every
Core4 or codec epoch change is a re-genesis, resolution C3), the kernel-side `holds` list of send-only
references and escrow accounts that the capture rule constrains (resolution B1; needed with sends,
lane L6), and an `AwaitsFunding` mark (lane L11). The outcome sum needs two refinements: `refused` and
`broken` should carry their reasons (the redacted residual for `refused`, §E; a finite sum such as
`DeciderRefused | DependencyBroken | NotAReference` for `broken`, which sends will propagate; BREAD
review D-3; adopted by the root's ruling), and `conflict` is removed (below).

**Defect in the landed kernel: a stale resume loses the reply and then overwrites newer state.** Four
reviews found this independently (BREAD D-1, FRONTIER §3.1, HIST F2, OS verdict; read at `36fca3ac`). The
only read an activity records is the root of the state it itself wrote at its yield (`commitYield`); on a
stale read, `revalidate` replaces the decided outcome with `conflict (stale : Nat)`, although the slot's
decision claim and the await claim are both already spent, so the reply is unrecoverable; the activity
has no way to read the current state, so its next yield writes state derived from its heap copy, and the
delivery's guard is against the current root, so that write commits over the interleaved one. The demo
asserts this: in scenario B the owner writes 99, the decider replies 7, the delivery yields `conflict`,
and the state shown is 5, with both 99 and 7 gone. Because every yield writes the whole declared state,
two activities on one object stale each other on every turn. This contradicts decision B's intent
("revalidates the read versions"; "stale -> re-run"). The root ruled the fix below (BREAD R1, HIST F2;
FRONTIER §3.1 had proposed a `Conflict` carrying the decided outcome and the current state, which the
ruling did not adopt).

**Resume with view (root ruling 10-05; shapes from the BREAD review appendix, RESUME-WITH-VIEW).**
- *State cell.* An object's declared state lives in a kernel-namespaced cell holding `ObjectState :=
  { version : Nat, value : Data }`; every committed write sets `version := version + 1`. Birth may create
  the cell (version 0 → 1); nothing else may.
- *Response.* An activity's response type is a one-member sum `resumed { outcome : O, view : V }` with
  `V = { version : Nat, state : S }` and `S` the declared state type. `O = reply T | refused Refusal |
  unknown | timedOut | broken Breakage | upgraded`, where `Refusal` and `Breakage` are kernel-fixed sums
  (today `Refusal = decider`, `Breakage = decider | dependency | notAReference`; sends fill later
  members). `birth` types every kernel outcome with a sample view at the response type.
- *Writes.* A Plan names a write, not a state: `W(S)` has one field per field of `S`, each of type
  `Edit(T) = keep | set T | add T` (`add` only for `Nat` and `Int` fields). The kernel applies it to
  `view.state` field by field; an all-`keep` write posts nothing. Plans therefore write fields or deltas,
  never whole records, which is what lets several activities share one object.
- *Version check.* The state post is a compare-and-swap against the root the view was read from, in the
  same turn; a moved version refuses the whole delivery, which is retryable, and a fresh delivery reads a
  fresh view. A Plan never carries a version: the kernel binds it.
- *No blind writes.* A birth's first segment runs with no view, so its write may `set` only when it creates
  the state cell; otherwise a `set` is refused `blindWrite`, and `add` and `keep` are admitted.
- *Read set.* A record's read set is the state cell at the root the delivery wrote or read;
  `staleCount`, `revalidate` and `AwaitOutcome.conflict` are deleted. The outcome is never replaced or
  dropped. Because a Plan's write is computed in the same turn as the view it depends on, no write is
  derived from a stale read, including between two activities of one object.

Every turn is one `Kernel/DurableDataIntent.DataIntent`, so its writes commit together or not at all.
`birth` instantiates the pinned definition with typed input, runs to the first yield and commits the
record, the Plan's declared-state write, the answer slot and the escrow. `resolve` lets the slot's one
decider decide it, typed against the awaiting activity's response type, at or before the deadline.
`deliver` may be submitted by anyone: it spends the await id as a nullifier bound to the checkpoint
digest and writes the record cell against its current root, so consume-once is a compare-and-swap at
admission's decide point; as landed, it revalidates the recorded reads (stale gives `conflict`,
never the bare outcome; the ruling replaces this with the view and the version check above); past the deadline an open slot expires in the same turn and the activity receives `timedOut`;
it decodes the checkpoint from the record cell (no state is accepted from a request), resumes it with
the typed response (today the outcome alone or `conflict`; under the ruling, the outcome and a fresh
view), runs it to its next yield or end with the `@[csimp]` fast machine, and commits the
new checkpoint, the Plan's write and the next await together. In `Kernel/Contracts/Cuts` terms an await
is a `Reserve` and a delivery an `Install` that consumes it, so a delivery must also be judged under the
object's current law (`install_rechecks_today`); the scratch kernel has no object law yet, so that check
arrives with lane L3. A deterministic failure in the resumed segment (blackhole, machine
refusal) commits a `faulted` phase and a fault message to the object's keeper (`ObjectRecord.keeper`;
Tribble's keeper model, HIST 1G). Budget exhaustion commits an `exhausted` receipt that consumes the
declared envelope's price and leaves the checkpoint, the await and the generation unchanged (§G; HIST
review F3: the landed kernel charges nothing for an exhausted delivery, so a resident whose resume always
exhausts can be delivered to forever at no cost). ABORT, and the disposal turns of §G, decide the
activity's open slot as `expired`, so no decider can later decide a dead slot (HIST review F8).

Answer slots are their own module, `Kernel/AnswerSlot`, rather than an instance of
`Kernel/ReactiveTerminalCell` as revision 1 proposed. A slot is named `H(turn, call site)` from the
yielding turn's transaction and the yield's place (record cell and generation), has one decider fixed
when it opens, one deadline and one terminal decision: the decider decides `reply | refused | unknown |
broken` at or before the deadline, and anyone may expire it strictly after. A second decision is refused
twice over, by the cell compare-and-swap and by the spent claim. `upgraded` and `conflict` are outcomes
of the activity, never slot decisions. The landed slot names its decider as a `SubjectId` chosen by the
activity's own Plan; for `send` the decider must be a role handed from the slot to the delivery and on
to the callee's turn, so `decide_single_decider` must be restated over a role before lane L6 freezes
the slot codec (BREAD review D-4). The two terminal-cell modules overlap; lane L6 should either
build sends on `AnswerSlot` and delete the unused parts of `ReactiveTerminalCell`, or justify keeping
both.

**Why.** First, Mini's codec is a specified function of the Core4 machine, not an engine image; Agoric's
engine-image snapshots made every engine upgrade a restart of all vats with no rollback (FRONTIER §1.3;
issue #8955). Second, consume-once must be enforced at the read/decide point: Khan (2026) measured 2,628
fires where 400 were expected under concurrency, and only a claim at the decide point repaired it (CALLS
C6); Bread's spent-nullifier `ReactiveRegistry.no_double_react` was the one async piece that ran, while
`Dregg2/Await.lean`'s `OneShot` had a public `run` field and an uninhabited handler premise (META §8.5;
ROOT correction). Third, ICP's commit at every `await` produced time-of-check/time-of-use bugs, double
spends and leaked locks (CALLS E4; ROOT); Mini's yield commits Plan and checkpoint together, and
revalidated reads close the check-then-act gap. Fourth, a typed outcome sum makes failure arrive on
receive: E's broken promises are contagious, IC exposes `SYS_UNKNOWN`, IBC carries timeout heights, and
Marlowe proves that contracts with timeouts close (CALLS A1, E4, G4; LAWS C12). Pinning rests on
content-addressed code (CALLS H7, Part II.4); the capture rule comes from Pony's iso/val/tag (CALLS B6).

**Cost.** It needs one record type, one answer-slot module, the delivery turn and the escrow postings,
all of which now exist in the scratch kernel. Each yield writes a checkpoint proportional to the live
heap, which grows until collection exists (about 120 tokens per turn in `EventCounter.serve`; 4,359 to
4,991 bytes over two Tally resumes; task `01a1056f-00a4`). Because every
await has a deadline, a resident that serves forever pays one timeout turn per deadline period.

**Rules out.** It rules out long-lived state held only in continuations; a second resume of one yield; client-supplied
checkpoints; awaits that can wait forever; and Bread's five unconnected async mechanisms (BREAD §0).

> **Scribe note B1 (capture rule versus Core4). Resolved: accepted by the root.** Core4's runtime values (`RuntimeValue`) include no
> capability, resource or mutable reference; `Ty.custody` is unused by any closed program; and the
> machine has no mutable cells other than thunk updates. A checkpoint therefore cannot hold authority,
> resources or an alias of object state at all, and the capture rule is satisfied by construction on
> the heap. What the rule actually constrains is the kernel-side activity record (`holds`), as above.
> When Core4 gains capability values, the rule must become a typing rule (a `capturable` predicate
> alongside `Ty.shareable`). *Resolution:* the rule constrains the kernel's activity record, and Core4
> values satisfy it by construction.

> **Scribe note B2 (`Conflict` is not in the outcome sum). Resolved by the root.** The decision delivers "a typed `Conflict`"
> when recorded reads are stale, but the outcome sum it fixes is `Reply | Refused | Unknown | TimedOut |
> Broken | Upgraded`. Either the sum gains `Conflict(stale cells, outcome)`, which keeps the resolved
> outcome deliverable, or staleness is a `Refused` reason. The first is needed if the reply must not be
> lost when the activity's earlier reads went stale. *Resolution:* the sum is `Reply | Refused | Unknown |
> TimedOut | Broken | Upgraded | Conflict`. Landed as `AwaitOutcome.conflict (stale : Nat)`, which does
> not carry the outcome. *Superseded by the root's ruling of 10-05:* resume with view, `conflict` removed
> from the sum, versioned field and delta writes (§B above).

> **Scribe note B3 ("type-checked before the root moves"). Resolved by the root.** No executable checker for machine-state
> typing exists: `StateTyping` in `Theory/ObjectiveBendDemandTyping` is a `Prop`. For a checkpoint the
> kernel produced from a `Checked` program, typing holds by `typed_stepRaw_preserved` and
> `typed_resume_preserved`, so the runtime check reduces to `decodeState (encodeState s) = some s`
> against the stored bytes. An executable `checkState` is needed only for states that arrive from
> outside the kernel's own run, which decision C forbids (no MAP, no codec migration). *Resolution:*
> kernel-produced checkpoints are well-typed by theorem; the before-root check is codec validity plus
> the digest binding to the producing turn, and no foreign checkpoint is ever admitted. Landed:
> `birth_checkpoint_typed` and `delivery_checkpoint_typed` (`Kernel/ObjectiveResumeContract`) prove that
> every checkpoint the kernel stores decodes to a typed state.

> **Scribe note B4 (collection at the yield does not exist). Resolved by the root.** The brief described the design as "full
> machine state, GC at yield, storage charged". The Core4 machine has no collector; its heap only grows.
> "Storage-charged after GC at the yield" depends on task `01a1056f-00a4` and on a theorem that
> collection preserves behaviour (§3, T5). *Resolution:* collection at the yield is its own build item
> (lane L2), and storage is charged on the post-collection size once it exists.

### C. Upgrade

**Decision, as amended by the root's resolutions C1–C3.** Authority is a law-governed capability visible
on the object's card; there is no superuser. Checks: declared-state subtype, else a typed linear
migration `Old ⊸ New`; the law re-judged on migrated state; frozen floors entailed, decided as
`unsat(new ∧ ¬floor)` with a certificate; the new interface a supertype of every referenced facet. The
original decision made the upgrade one all-or-nothing turn with dispositions DRAIN (until the awaits
end), ABORT and REPLAY (only if it succeeds in the turn), and no MAP. Resolution C1 refines DRAIN into a
two-phase upgrade: (1) an ADOPT turn pins the new package for new activities, and the declared state is
not migrated while any old activity remains; (2) old activities run on their pinned package against the
unmigrated state until their awaits end or a mandatory drain deadline height, after which they are
aborted with `Upgraded`; (3) a MIGRATE turn migrates the state and re-judges the law when the last old
activity ends. Resolution C2 drops REPLAY for now (the dispositions are DRAIN with a deadline, and ABORT),
which provisionally answers OPEN 3. Resolution C3 makes every Core4 or codec epoch change a re-genesis.
The root's ruling of 10-05 refines C1 again (OS W2, HIST F5, FRONTIER §3.5): while an upgrade drains,
the object admits no new births or calls unless the old state type is a subtype of the new; an old
activity's write is admitted only if `migrate s'` type-checks and satisfies the new law, so the final
MIGRATE cannot fail; large objects migrate over several turns with the object closed, a cursor cell
holding progress, and any upgrade-capability holder advancing it (OS W3). The dispositions are DRAIN,
ABORT and REBIRTH (abort and re-birth from the record's stored input on the migrated state, with
restartability checked at publish; HIST F6). REPLAY stays dropped.

**Mechanism.** `Kernel/ObjectUpgrade.lean` (**new**) admits two Plan actions, each a `Receiving` family:

```lean
structure Adopt where
  object         : ObjectRef
  newPin         : PackagePin
  newStateType   : Ty
  migration      : Option MigrationTerm        -- Core4 term : Old → New, typed linearly
  newLaw         : Pred
  drainDeadline  : Nat                         -- accepted height; mandatory
  dispositions   : List (ActivityId × Disposition)   -- must cover record.activities exactly
inductive Disposition | drain | abort | rebirth
structure Migrate where object : ObjectRef      -- admissible only when no drained activity remains
```

ADOPT checks, in order: the signer presents the upgrade capability and the object's upgrade law admits
the request; `record.stateType` is a row subtype of `newStateType`, or `migration` checks as a linear
function `Old ⊸ New` under `Theory/ObjectiveBendTyping` (linear is enforced as at-most-once today, so the
check must add exactly-once for this use); for each floor `f`, `Pred.Sat` decides `allL [newLaw, not f]`
and must return `.unsat` with a `SysCert` that `checkAll` accepts (`certificate_unsat`); the new interface
type is a supertype of the type of every facet referenced from another object's c-list; and
`dispositions` covers `record.activities` exactly. The ADOPT turn records the pending upgrade (new pin,
migration, law, deadline) in the object record, resolves each ABORT activity's await to `Upgraded
newPin` and frees its checkpoint, and leaves each DRAIN activity on its old pin. If the old state type
is a row subtype of the new, births and calls use the new package from ADOPT on (Erlang's fully
qualified calls, CALLS H5), because both packages can read the one state. Otherwise the object is
draining: births and calls are refused with `Upgrading(deadline)`, sends wait in its inbox, and only the
old package's activities run, against the unmigrated state; no new code ever reads the old schema (OS
W2, HIST F5, BREAD R6, as ruled). Any turn at or past `drainDeadline` may abort a remaining drained
activity with `Upgraded`, so a looping resident is bounded. MIGRATE is admissible once no drained
activity remains: it applies the migration, judges the result by `newLaw` on the pair `(migrate s,
migrate s)` (state clauses must hold; two-state clauses see no change), installs the new law, sets
`schema` and `stateVer`, and bumps `continuity`. For each REBIRTH activity, the same turn births a new
activity on the new package from the old record's stored `input`, against the migrated state, funded by
the old payer's remaining escrow; it needs no log and no replay. A resident package may declare itself
`restartable`; publish then requires a test (run in CI, not at admission) that abort-and-rebirth from
declared state alone reaches the same declared state under the same deliveries, so "this service
survives an upgrade" is a checked claim (merged from HIST review F6; NLTSS restart from durable state and
Frantz's ranking 2a, HIST 1C). Queued sends then drain on the new package. Because the floors were decided at ADOPT against the
same `newLaw`, MIGRATE needs no solver call. Every Core4 or codec epoch change is a re-genesis, so no
activity or frozen object ever crosses one.

**Making MIGRATE total (merged from FRONTIER review §3.5; ruled 10-05).** As first resolved, MIGRATE re-judges the new law on
a state that old activities kept writing after ADOPT; if that fails, the object is stuck between
versions, which is the failure-after-commit class of Agoric #12315 and #12138. So while an object is
draining, every turn that writes its declared state is admitted only if `migrate s'` type-checks at the
new state type and satisfies the new law, where `s'` is the state the turn would commit; the kernel
computes this in the same turn and charges it in the turn's envelope. If ADOPT's own check of `migrate
s` fails, the upgrade is refused at ADOPT. MIGRATE then cannot fail.

**Floors (merged from LAWS review D-7; ruled 10-05).** A floor is admitted into `UpgradePolicy.floors` only if
`Pred.difference?` accepts it and `Pred.Sat` decides it satisfiable, with a witness; otherwise the turn
that adds it is refused by name. An object whose floors were accepted can therefore always be upgraded by
a law that entails them, and no floor silently turns a governed object into a frozen one.

**Large objects (merged from OS review W3; ruled 10-05).** A migration that exceeds one turn's envelope runs as a
MIGRATING phase. The object is closed (births and calls answer `Refused(migrating)`, sends queue), a
progress cell holds a cursor over the declared state, and any holder of the upgrade capability advances
it one envelope at a time; the final step re-judges the law and reopens the object. A migrating object
never runs two state shapes at once. (This replaces revision 1's "large objects cannot upgrade", which
would have made Motoko's "evolutionary dead end" a rule; Bläser et al. 2024 §5.3, OS §3.7.)

**Why.** Agoric's record decides the disposition rule. After abandoning in-flight work at upgrade, it
rebuilt durable async in three layers (vows, retry-send, asyncFlow); its open issue #12315 (January 2026)
calls parking a flow that fails replay "wishful thinking", and its rollback path halted mainnet in October
2025 (#12138) (FRONTIER §1.11–1.12). The one live KeyKOS upgrade of running state, the clock, was
"open-heart surgery … ugly beyond belief" (Frantz, cap-talk 2008-04-05; HIST 1C), which is the case
against MAP. Erlang runs old work on old code soundly because code is identified by version (CALLS H5),
and Motoko checks compatibility inside the upgrade transaction and rolls back on failure (CALLS H3).
Mina's positional state is the untyped alternative: reordering two declarations turns a balance into a
counter, and "Nothing fails. There is no error." (CALLS E18). Floor entailment is decidable because
`Pred/Satisfiable` returns a witness or a certificate and `decide_never_unknown` excludes `unknown`;
Bread's `Polis.NonRegressive` and svenvs `Admissible` were `Prop`s nothing could run (META §7.1–7.2).

**Cost.** It needs a subtype judgement on rows, a linear-migration check, an entailment call per floor,
an interface-compatibility check, a pending-upgrade field on the object record, and the drain-deadline
abort. An object with a long drain deadline runs two package versions until it. `Pred.Sat` returns `none` for laws
containing `witnessed`, `hashEq` or `ran`, and for DNFs past `dnfCap = 1024`, so such floors are refused
when installed (above; LAWS Part II §7). The draining invariant costs one migration check per state write
during a drain, and a large migration costs one turn per envelope while the object is closed.

**Rules out.** It rules out Bread's bare `SetProgram` swap (BREAD §1.5); lazy migration on first touch; upgrades that
discover replay failure after commit; host-level upgrade powers; drains with no bound; migrated state
written by old code; and silent loss of in-flight work.

> **Scribe note C1 (DRAIN versus migrated state, and no drain bound). Resolved by the root.** A drained activity keeps its old
> package, and its future Plans are typed against the old Plan sum and the old declared-state schema.
> After a migration that changes the schema, those Plans name fields that no longer exist, so "sound
> because checkpoints hold no mutable state" covers the checkpoint but not the Plans the activity will
> yield. The decision also sets no bound on draining: a resident that loops (`EventCounter.serve`) never
> ends its awaits, so the old package runs forever. CALLS idea 8 and DFINITY's record ("drains can
> stall", CALLS H4) argued for a drain deadline height after which the activity is aborted with
> `Upgraded`. A resolution needs both a rule for drained Plans after a schema change (refuse them with
> `Refused(schema)`, or allow DRAIN only when the state type is unchanged) and a drain deadline.
> *Resolution:* the two-phase ADOPT/drain/MIGRATE upgrade with a mandatory drain deadline, described in
> the amended decision and mechanism above. Old activities never see migrated state.

> **Scribe note C2 (REPLAY needs a log Mini does not keep). Resolved by the root.** Mini stores the checkpoint, not the
> sequence of `(Plan_i, Response_i)` pairs. REPLAY requires each activity to retain its full interaction
> log from its start (or from its last upgrade) in a payer-funded cell, a retention structure decision G
> does not list. Its cost is the log's storage plus a replay inside one turn's envelope. *Resolution:*
> REPLAY is dropped for now; the dispositions are DRAIN (with deadline) and ABORT. Ember may reopen it
> (OPEN 3).

> **Scribe note C3 (frozen objects across a Core4 epoch). Resolved by the root.** A frozen object can never be re-pinned, yet
> its package runs only on the Core4 epoch it was compiled for. After a Core4 or codec epoch change, a
> frozen object can run only if the Host keeps the old evaluator forever. DRAIN across an epoch change
> likewise needs the Host to run two Core4 evaluators. The 10-04 decision that re-genesis is the default
> for every format question (SWARM-LEDGER 05:30, item 1) resolves both if a Core4 epoch change is always
> a re-genesis; the program model should say so. *Resolution:* a Core4 or codec epoch change is always a
> re-genesis, so frozen objects never need to survive one.

### D. Calls across objects

**Decision.** Three forms, as stated in §1: `call` (synchronous, in-turn, depth-first, Daml authority,
mandatory re-entry refusal, abort when a frame read a version another frame wrote); `send` (eventual,
per-(sender, target) FIFO inbox, one paid turn per delivery, breadth-first, answer slots `H(turn, call
site)` with one decider, sends to an unresolved slot queued and forwarded in the resolving turn, broken
slots propagating and refunding); and pipeline invocations (signed, straight-line, non-recursive,
re-executed as one turn, composable from partially signed segments). Signers attach Pact-style scoped
grants that count down. Nothing externally visible leaves a domain before its turn commits and, in a
committee domain, is final. Early delivery to the callee's host comes only on cross-domain links, after
answer slots and their upgrade semantics exist.

**Mechanism: `call`.** `Kernel/CallFrame.lean` (**new**) runs inside one admission:

```lean
structure Frame where
  object    : ObjectRef
  method    : Label
  authority : AuthorityContext    -- callee signatories ∪ node controllers ∪ scoped grants
  reads     : List ReadGuard      -- learned from the snapshot by re-execution
  fragment  : PlanFragment        -- deferred; applied at the end of the turn

def callStep (stack : List Frame) (target : ObjectRef) … : Except CallRefusal Frame :=
  if stack.any (·.object = target) then .error .reentry else …
```

A `call` is legal only on a method typed as a pure function returning `(A × PlanFragment)`; a method of
type `Activity<P,R,A>` cannot be called, only sent to, so no frame yields inside a turn (the rule Unison
states by typing a transaction body without `Remote`, FRONTIER 2.E E4). Revision 2 deferred every
fragment to the end of the turn. The root's ruling on OPEN 1 (10-05) instead applies a callee's writes
when its frame returns: a frame's writes are deferred while it runs and applied to the turn's journal
at its return, the whole journal is discarded if the turn is refused, and the call is billed to the
caller's envelope (seL4's donation, OS review). A frame reads the turn's current state: the snapshot plus
every fragment already applied. Because re-entry is refused, no frame observes a write by a frame still
below it on the stack, and no object's state changes while its own frame is suspended in a call, so a
callee never sees its caller's half-done state (the property FRONTIER's OPEN-1 answer makes the
condition for `call`). Laws judge each written object on (state at turn start, state at turn end), and
two-state atoms read the turn-start value as `old` (BREAD review R2). Decision D1's rule that a frame
which read a version another frame wrote aborts the turn, and resolution D2's write-write abort (unless
the slot's law declares a commutative delta), are not withdrawn by the ruling; Scribe note D4 and Review
dispute 1 (§7) record the question. Authority follows Daml (LAWS C13; ROOT), with Mini referents supplied by the LAWS review
(D-6): calling a method requires its controllers in the current context; a callee frame's authority
context is the callee object's own held capabilities (its c-list), plus the method's controllers present
in the caller's context, plus matching scoped grants; `ObjectRecord.creators` are the pre-authorizing
parties, so a frame may write cells whose law requires a creator's consent only if the method's package
was pinned when those creators signed (the artifact clause of §E). That is Daml's "a signatory has
pre-authorized the consequences of the choices when the contract instance was created". The caller's
ambient signers never enter the callee's context. A scoped grant is the one explicit, bounded
exception to non-transitivity: the invocation carries a grant table (`Kernel/ScopedGrant.lean`,
**new**), e.g. `Transfer(from := me, asset := A, ≤ 10)`, and any frame may spend the signer's authority
only by decrementing a matching grant, judged by an `le` atom. The grant table is turn-scoped and never
enters a cell or a checkpoint (§B).

**Mechanism: `send` and answer slots.** A `send` is a Plan action `send (target : CapIndex) (method :
Label) (args : Data) (reply : Option SlotName)`. It appends to the inbox cell keyed by (sender, target)
(`Kernel/Inbox.lean`, **new**; the inbox's FIFO discipline is its law: monotone head and tail, tail ≤
head, sender-authenticated, as Bread's `cap_inbox` had, BREAD §1.2). Its answer slot is a
`Kernel/AnswerSlot` slot whose name is derived from the sending turn and the send's place in its Plan,
as the landed slots are, so every validator names it identically (Ozone's integrity keys, CALLS A8). The decider role is linear: creating the slot gives it
to the delivery, the delivery gives it to the callee's turn, and resolving consumes it (Agoric's rule,
FRONTIER §1.2). A send whose target is an unresolved slot is queued in that slot's cell and forwarded
inside the resolving turn, so every resolution follows one path and needs no embargo (Cap'n Proto's
rule, CALLS A5). A slot whose decider faults or whose deadline passes resolves `broken` or `expired`,
and breakage propagates to queued sends.

**Send escrow and queues (merged from BREAD review R3).** Every send escrows its own postage and envelope
when it is made. A send queued on an unresolved slot keeps its escrow there, and forwarding charges each
forwarded send to its own escrow, never to the resolver. A slot's queue has a fixed maximum length; a
send to a full queue is refused at send time. If the slot resolves to anything other than a reference,
every queued send resolves `broken NotAReference` and its postage returns (measurement-free, resolution
G1). The decider of a send's slot is a role, not a subject: the send hands it to the delivery, and the
delivery to the callee's turn (Bread's relay bounded its queues, BREAD §1.2 item 8).

**Output gate.** The outbox records of `Kernel/OutboxDelivery` carry everything that leaves a domain,
and nothing is released before the turn commits and, in a Simplex domain, is final.

**Consent (merged from FRONTIER review §3.6).** The first native route (main `796d7d7a`) has the caller
sign the exact Plan, re-derived and compared byte for byte before signing (`Host/ObjectiveConsent`), so
any concurrent change refuses the invocation (two of its 13 named refusals are `stale-root`). Exact-plan
signing is the default protection; seats (§E) are what tolerate movement, so without seats every trade
in a busy domain retries.

**Mechanism: pipelines.** A pipeline invocation is a restricted Core4 term (`Kernel/Pipeline.lean`,
**new**): a list of commands `call (cap | result i) method args` with results by index, no recursion and
no `fix`, so its cost is a function of its length. Admission re-executes it as one turn and every law
judges the composed Plan. A multi-party pipeline is a list of partially signed segments; each segment
is signed over (segment hash, position, pipeline hash) and carries its signer's own envelope, which
covers that segment only. The composed turn is admitted only if every segment's signature and grants
check, no segment exceeds its envelope (one excess refuses the whole turn, resolution D3), and the
Book's posting algebra balances the composed Plan. Every
partially signed segment carries a `valid_until` height, and the composed turn is refused after the
smallest of them, so a segment that failed today cannot be admitted whenever it would succeed later
(merged from BREAD review R4; Bread's partial commitments bound federation and nonce, BREAD §1.4). That is in-domain multi-party atomicity with no two-phase commit.

**Why.** Mina already runs synchronous, value-returning child calls whose returned value the network
checks (CALLS E18). Daml's four rules are the one complete authorization judgement for a call tree, with
non-transitive delegation "a deliberate design choice" (LAWS C13; CALLS E5). SES documents that
synchronous cross-principal calls are where re-entrancy lives (FRONTIER §1.7), so the guard is mandatory.
Pact's scoped capabilities have run on Kadena mainnet since 2019 and let signers "safely call untrusted
code" (FRONTIER 2.E E5). Tezos moved to depth-first because breadth-first "provides few useful
guarantees", Urbit is moving to breadth-first because depth-first "constantly violates" emission order
under re-entrancy, and both found that mixing orders is where bugs live (CALLS Part II.1). Sui PTBs and
Cap'n Web make the caller-composed pipeline a production pattern, and Anoma composes partial transactions
without 2PC (FRONTIER 2.E E1, E6; 2.G). Waterken persisted before any externally visible I/O, and Durable
Objects hold outgoing messages until the write completes (CALLS A16; FRONTIER 2.E E2).

**Cost.** It needs a call stack with a re-entry guard and per-frame authority contexts, a grant table per
turn, paid inbox cells and answer slots (§G), a pipeline form, and segment signatures for multi-party
composition. A `PlanFragment` with more than one action needs recursive Plan data, which Core4 lacks
today (Plans and responses "must be non-recursive data", EVENTS; task `01a1056f-00a4`).

**Rules out.** It rules out callbacks into an object already on the stack; callees spending a caller's authority
beyond what the caller signed; a third call order; and early delivery inside one domain.

> **Scribe note D1 (the re-entry statistic). Resolved by the root.** The decision cites "10 of ~100M Ethereum executions were
> legitimately reentrant". Grossman et al. (POPL 2018, §9, lines 1181–1182) report that "only 10
> executions out of about 100 million were legitimately non-ECF". An execution that re-enters an object
> but is equivalent to a callback-free one is ECF and is not counted. The mandatory guard refuses those
> too, and the paper (in the parts read) does not report how many executions contained callbacks at all.
> The evidence supports "non-ECF re-entry is almost never legitimate"; the cost of refusing ECF
> re-entry is unmeasured. *Resolution:* the figure counts legitimately non-ECF executions; keep the
> refusal (conservative) and measure its cost on Mini's own cohorts (lane L5's acceptance).

> **Scribe note D2 (write-write between frames). Resolved by the root.** The decision aborts a turn when a frame reads a
> version another frame wrote. It states no rule for two frames that write the same non-delta slot. The
> Orleans rule it cites aborts when the context union "has seen more than one version of any grain"
> (CALLS B3), which covers write-write if writes count as versions seen. The rule should say so.
> *Resolution:* two frames of one turn writing the same slot abort the turn, unless that slot's law
> declares the write a commutative delta, in which case deltas compose and the law judges the sum.

> **Scribe note D3 (one envelope, several signers). Resolved by the root.** Decision G fixes "one signed envelope per
> invocation". A composed multi-party pipeline has several signers. The design above gives each segment
> its own envelope and charges the composed turn the sum; the decisions should confirm that a segment's
> excess refuses the whole turn and that no signer pays for another's segment. *Resolution:* each
> signer's envelope covers that signer's segment, and the turn is refused if any segment exceeds its
> envelope.

> **Scribe note D4 (frame-conflict aborts under apply-at-return). Open, raised by revision 3.** Under
> deferred-to-end fragments, a frame-conflict abort was needed: a frame could read a snapshot value that
> an earlier sibling's pending fragment had already changed. Under the ruled apply-at-return, a later
> frame reads the earlier frame's applied write, so that stale read cannot occur, and two sequential
> writes to one slot compose in order instead of losing one. The ruling is silent on whether decision
> D1's frame-conflict abort and resolution D2's write-write abort still apply. Kept, they refuse turns
> such as `A` calling `B.deposit` twice (BREAD review R2); withdrawn, the commutative-delta declaration
> of D2 matters only to the coordination grade (§F).

### E. Laws and contracts

**Decision.** The decidable law language stays the judge at every write; package proofs are extra
evidence, never a substitute. It gains two-state atoms (`new[a] ≤ old[b] + k`), request atoms (method,
invoker, capability presented, height), necessity sugar `from A to B onlyIf C`, action-scoped clauses
over the cells the Plan co-touches, and past-time temporal laws compiled to kernel-maintained history
slots. Laws apply at three points (method guards, state laws, proposals). Seats and protocol objects are
as stated in §1, with payout liveness a kernel theorem for Book assets. Clauses are deny-by-default,
indexed by method and forbid-overrides-permit; each carries a coordination grade computed at publish;
publish-time checks carry certificates; admission evaluates only closed laws; refusals carry the residual
predicate under a redaction policy. OPEN: generate laws from `.obend` declarations now, or unify them
into a decidable Objective Bend fragment later.

**Mechanism: the language.** `Pred/Core.Pred` today has `eq | le | memberOf` on new slots, `writeOnce |
monotone` (the only two-state atoms), `eqSlots | leSlots | leSlotsOff`, `witnessed`, `hashEq`, `ran`, and
`not | allL | anyL`. The additions:

```lean
| leOld (a b : Slot) (k : Int)     -- new[a] ≤ old[b] + k : a Con ⟨.new a, .old b, k⟩ in Pred.Sat
-- request atoms are reserved slots, read like any slot and fail closed when absent. On main
-- (Compiler/CanonicalRuntimeProfileCore.requestSlots) these exist: request/subject (the invoker),
-- /height, /verb, /target, /nonce, /cost, /policyEpoch. To add: request/method,
-- request/package, request/cap/<i> (LAWS review §3).
def necessity (A B C : Pred) : Pred := .any [.not A, .not B, C]   -- `from A to B onlyIf C`
-- A and C read old slots and request slots, B reads new slots; this needs old-slot forms of
-- eq/le/memberOf, which Pred.Sat's `.old` nodes already represent
```

`leOld` needs no new decision machinery: `Pred/Satisfiable`'s `Node` already has `.old s` and `.new s`,
`monoT` already emits `⟨.old s, .new s, 0⟩`, so `leOld` is one more atom in `atomDnf`, and
`decide_never_unknown` and `certificate_unsat` extend by one case. History slots are compiled by a new
`Pred/History.lean` (**new**): a past-time formula (`since`, `once`, bounded counts over a height
window) becomes kernel-maintained slots updated by the kernel's own Plan postlude, after which the law
is an ordinary two-state `Pred` over (old history, new state); code cannot write those slots. History
stays propositional (merged from LAWS review D-8): `Pred/History` compiles propositional past-time
formulas only (`since`, `once`, `previously`) and bounded counts over a declared height window, over a
fixed finite set of keys named at publish; window storage is a ring of declared size charged to the
object's payer (§G); the kernel computes the new history from (old history, request, new state) before
the law is evaluated on (old history and old state, new history and new state). First-order temporal
quantification (DejaVu's, LAWS E6) is out of the fragment. Action scope is already built for joint
commands: every participant's slots are projected under `joint/target/{id}/…` and `joint/index/{i}/…`
into each target's law state (`projectWithCommon`), and Book balances enter through `moneyPolicySlots`
(LAWS review §3). It extends to Plans so that a law may read the post-state of any cell the same Plan
writes, named by its role in the Plan; the read joins the turn's footprint. Book balances enter laws through the
same view as total slots `book/<account>/<asset>`, initialised to 0 (FRONTIER §1.10 notes that `le` on
an absent slot is false, so `not le` on an absent slot is true; totality removes that trap).

**Mechanism: three points.** Every package method carries a guard, a `Pred` over arguments and request
slots, checked before the method runs; a refusal costs only the guard's evaluation. State laws run on
every write, as now. Proposals (offers, §seats) run on every reallocation of the seat. Clauses carry a
method index and a polarity (`permit | forbid`); the effective law of a write is `forbid` clauses
negated and conjoined with the disjunction of matching `permit` clauses, and no matching permit means
refusal. Refusals return `firstFailingLeaf`'s path plus the residual: the unsatisfied leaf with
request-slot values substituted, filtered by a redaction policy that names which leaves each viewer may
see (refusal text is an information channel, FRONTIER 2.B B1). The redaction policy already exists on
main: `lawRefusal fieldsOf` returns `ComposedLawDiagnostics.publicRefusal` filtered by the requester's
grant, and `lawRefusal_isSome` proves disclosure never changes the verdict (LAWS review §2).

**The package pin as a law (merged from LAWS review D-1; ruled 10-05, QUEST-LAWS-PIN running).** Today the Objective path's law state names no
method or package (`run = none` on that path), so an ordinary command whose envelope passes a cell's law
can write an object's state and bypass its methods. Every Objective invocation therefore projects into
each target's law state the slots `objective/artifact/<sourceAtom>` = 1 and
`objective/method/<methodSemanticId>` = 1, named the way `ranSlot` is so that a 256-bit identity never
enters an integer range. The slots are derived from the signed claim before execution; this is sound
because `AcceptedInvocation` is constructed only after the executed artifact is shown to be the claimed
one. Ordinary commands project neither slot, and reads fail closed. When an object is created, the
kernel installs a kernel clause on its state cells, `any [eq (artifactSlot m) 1 | m ∈ pin.methods]`,
which no package clause can remove. This makes the package pin a law, makes method-indexed clauses
expressible, and refuses ordinary-route writes to object state. An upgrade rewrites this clause in the
same turn as the pin. `request/cap/<i>` is projected the same way from the capabilities named in the
claim's `inputRefs`.

**Where laws are judged (merged from LAWS review D-2; ruled 10-05).** Laws are judged by the single Receiver, not by
families. Today `Kernel.Receiving.Family.postLaw` is a per-family Boolean, and the first migrated family
(`SubjectKeyRotation`) sets it to physical well-formedness, so judging laws is a discipline every one of
about 33 families must remember. `Family` gains `step : (p : Prepared env durable command) → (w :
DataWrite) → w ∈ writes p → LawStep`, where `LawStep` is the projected old and new `Pred.State` plus
request slots; `shape` resolves each written cell's committed law at the snapshot (`LawComposition`, one
snapshot) and requires `Pred.eval` to accept its `LawStep`. A cell is exempt only if its kind is in a
registered `KernelCellClass` (activity records, answer slots, journals, fee accounts), whose registry
carries a proof that only kernel families write that class. `postLaw` remains for physical
well-formedness only. Theorem `receive_committed_lawful` (§3) is proved once, over `Family`. This must
land before the receiver collapse moves `DeclaredResourceController` onto `Family` (its step 3).

**Surface (merged from LAWS review D-4; the root's refined OPEN 2 recommendation).** `law` and `requires` already mean other things in Objective
Bend: a spec's `law name(args): expr` is a universally quantified property of methods, elaborated to a
closure in spec metadata, and `requires` declares a member a specification needs from final self, not a
precondition. Admission rules are therefore declared with four clause kinds: `invariant` (a state law),
`guard` (a method guard over arguments and request slots), `permit`, and `forbid`. Each must elaborate to
`Pred`, and anything outside the fragment is an elaboration error. A spec's `law` remains a property of
methods: package evidence, discharged by the certifying checker where it can be and otherwise reported
unproved, never consulted at admission. `requires` keeps its meaning. (This assumes OPEN 2 is answered
as the root leans; §5.)

**Mechanism: seats.** `Kernel/Seat.lean` (**new**), built on `Theory/CanonicalResourceKernel` and
`Kernel/CanonicalEscrowMarket`:

```lean
structure Proposal where
  give want : List (AssetId × Nat); exit : onDemand | afterDeadline (h : Nat); donate : Bool
def atLeast (slot : Slot) (n : Nat) : Pred :=        -- FRONTIER review §3.4: revision 1 wrote
  if n = 0 then .all [] else .not (.le slot ((n : Int) - 1))  -- `n - 1` in Nat, so 0 meant "≥ 1"
def offerSafe (seat : AccountId) (p : Proposal) : Pred :=
  .any [ .all (p.want.map fun (a, n) => atLeast (bookSlot seat a) n),
         .all (p.give.map fun (a, n) => atLeast (bookSlot seat a) n) ]
```

An `offer` Plan action creates the seat account, posts `give` into it from the offerer (so the initial
allocation equals `give` and satisfies the clause), and installs `offerSafe` as the seat account's law.
Every later posting that touches the seat is judged by it. `exit seat` is a kernel action whose
admissibility for the offerer is a clause the seat's law always contains and no contract clause can
forbid (forbid-overrides-permit is applied to contract clauses only); it posts the seat's whole
allocation to the offerer. Conservation is not a law: it is `Operation.apply_conserves`. Non-fungible
amounts need set-inclusion atoms; `memberOf` covers only bounded sets (FRONTIER §1.10, INFERRED there).
An `offer` with an empty `want` is refused unless the proposal says `donate`, because `all []` is true and
every reallocation would then be offer-safe (merged from LAWS review D-5).

**Invitations and who may debit a seat (merged from FRONTIER review §3.4; ruled 10-05).** An `invitation` is an
exclusive, assayable capability `{instance : ObjectRef, package : Digest, role : Label, terms : Data}`,
minted only by the instance's own turns. `offer invitation proposal` spends the invitation like a
nullifier in the same turn that creates the seat, so the offerer has assayed the instance, package, role
and terms it is playing (Miller 2013 §6; FRONTIER §1.9–1.10). A seat account may be debited only (a) by a
posting in a turn of the seat's instance, judged by `offerSafe` and Book conservation, or (b) by the
kernel `exit`, which posts the whole allocation to the offerer. A reallocation is one Plan action over
several seats of one instance (Zoe's `atomicRearrange`); every seat it touches is judged by its own law,
and the Book's posting algebra balances the action. ABORT of an activity, and termination of an
instance, `exit` every open seat of that instance, so neither may strand escrowed assets.

**Mechanism: protocol objects.** `Theory/ProtocolObject.lean` (**new**) ports Bread's `GlobalType`,
`LocalType`, `project` and the `dregg_choreo` notation (`Dregg2/Coordination.lean:68-239`, the part META
§1 marks PORT THE CODE), adds `mu` unfolding with a guardedness check, and compiles a guarded global type
at publish into a finite transition table over one state slot. The object's law is the disjunction, over
table rows `(q, role, label, guard, q')`, of `all [eqOld "protocol/state" q, memberOf "request/invoker"
role, eq "request/method" label, guard, eq "protocol/state" q']`, where `eqOld` is the old-slot form of
`eq` (§E language) and `guard` is a conjunction of law atoms on the transition's payload fields. Control
states stay finite; conditions on payload values live in the guards (resolution E1).

**Mechanism: publish-time checks.** At publish, `Pred/Entailment.lean` (**new**) decides equivalence,
subsumption, dead clauses (always false) and vacuous clauses (always true) with `Pred.Sat` certificates,
and `Pred/CoordinationDial` computes each clause's grade. Admission evaluates `Pred.eval`/`evalWith` on
concrete states only and never calls the solver.

**Why.** Scilla, ConCert, EUTXO and Zoe all separate proposing a change from validating it, and robust
safety needs a check on every write whoever proposed it (LAWS Part II); cross-cell invariants proved only
at the source level fail against arbitrary invocations, hence action scope (FRONTIER 2.D D3). Move's
`invariant update` is `new ≤ old + k`, and necessity specifications reduce to single-step necessity,
which a per-write judge provides (LAWS C1, B14). Agoric converged on decidable patterns for arguments,
object state and proposals (FRONTIER §1.8). Zoe checks `isOfferSafe` on every reallocation for the seat's
whole life (`zcfSeat.js:267-270`; ROOT), but inside the contract's own vat, with payout liveness
"conditional on well-behaved issuers" (FRONTIER §1.10); Mini's Book makes both kernel facts. Cedar's
deny-by-default, forbid-overrides-permit language has sound-and-complete subsumption at 30–80 ms per
check (LAWS D1).

**Cost.** It needs about four atom families, an action-scoped `LawView`, a history-slot compiler and its monitor
theorem, method guards in the package format, a seat module, a protocol-object module, an entailment
module, and a redaction policy. None needs a proof system in admission.

**Rules out.** It rules out laws as closures (today `spec` laws are "callable closures stored in metadata; nothing
discharges them", `docs/OBJECTIVE-BEND.md`); input validation inside method bodies; caller protections
enforced by contract code; Bread's catalogue of 69 hand-named atoms (BREAD §2.2); and solver calls on the
admission path.

> **Scribe note E1 (protocol state cannot be a tree the law reads). Resolved by the root.** `Pred` evaluates difference
> constraints over `Int` slots; it cannot compute `GStep` over a global-type tree. "Its law admits
> exactly a legal next step" is realisable only by compiling the residual global type at publish into a
> finite transition table over a state slot, as above. That works for guarded recursive global types
> (they have finitely many residuals) and fails for protocols whose next step depends on payload values
> beyond finite sets. The residual global type is then the meaning of the state slot, not data the law
> reads. *Resolution (root):* protocol objects are compiled at publish into a finite transition table;
> payload-dependent conditions are law atoms on payload fields at a transition, so control states stay
> finite.

### F. Concurrency

**Decision.** Several activities per object; they share state only through committed cells; resume
revalidates reads; hot state splits into sub-cells with their own laws; exclusivity across a yield only by
a law-governed lease, never a default lock. Deterministic parallel admission with Block-STM semantics:
footprints learned during admission (declarations are hints), root = the sequential fold (single-threaded
auditors suffice), delta actions first-class, the dependency DAG published for parallel replay.
Coordination grades from laws decide which turns commute, which skip ordering and who votes. Escrow quotas
(local quotas summing to the budget) let many activities draw on one balance. Cross-domain: a deal cell in
a domain all parties accept, offer safety as its decision law, write-once with a timeout height and
default abort; everything else as choreographed sagas.

**Mechanism.** Activities of one object are separate `ActivityRecord`s; each holds a checkpoint and its
recorded `ReadGuard`s, and two activities conflict only when their footprints on the object's cells
overlap. A lease is a sub-cell whose law is `from any to write(s) onlyIf request/invoker = holder ∧
request/height ≤ leaseEnd`, a difference constraint (Grove's time-bounded invariant, LAWS B7).
`Kernel/ParallelAdmission.lean` (**new**) admits a batch in log order:

```lean
-- parallel phase: execute every invocation against a multiversion view of the batch pre-state,
--   recording each DataIntent's writes and the ReadGuards re-execution actually forced
-- validation: in log order, re-execute any invocation whose recorded read was written by an
--   earlier invocation in the batch; then judge it against the current state and install it
theorem parallel_eq_fold : ParallelAdmission.run s batch = batch.foldl admitOne s   -- T4
```

Footprints are the `DataIntent` writes and read guards produced by re-execution; laziness keeps read sets
small because only forced cells are read. Delta actions (`delta cell slot k`, and Book postings) commute
and do not count as reads of their target. Fees never route through one cell; each payer's fee is a
posting into a per-collector sub-account (Block-STM: "A single location for gas updates could make any
block inherently sequential", CALLS E7). The published DAG lists, per invocation, the earlier invocations
whose writes it read.

`Pred/CoordinationDial` grows from four verdicts to a ladder. Today `dial` returns `.free` for
merge-closed clauses under slot-wise max and `.ordering`, `.stepShaped` or `.thirdParty` otherwise. The
additions are the escrow rung (Bread's `CRDT.escrow_refinement`: local quotas are I-confluent and `Σq =
B` gives the global bound, META §2.5) and CISE conflict tokens per method pair (CALLS F8). For a law atom
`a·x ≤ c`, an action with delta `d` and `a·d ≤ 0` is free and one with `a·d > 0` needs ordering or an
escrow quota (CALLS III.6, generalising Bailis Claims 11–14). The same table answers which activity pairs
commute, which turns could skip ordering, and which participants must vote across domains.

Across domains, a deal cell is a `ReactiveTerminalCell` in the domain all parties accept. Parties move
rights into it by ordinary sends (the prepare, which cannot fail later); one turn decides by the seat law
of §E; the decision is write-once; after the timeout height the default is abort; payouts and refunds
flow back as sends bound to (session, sequence) (CALLS III.7). Workflows that do not move exclusive rights
run as sagas with typed compensating Plans (FRONTIER 2.H H1).

**Why.** Block-STM matches declared-footprint systems without declarations, costs at most 30% on fully
sequential workloads, and its output equals the sequential execution (Corollary 2) (CALLS E7; ROOT);
Solana's declared write locks leave only 8% of transactions independent (CALLS E10). A default lock costs
liveness: Orleans grains hold requests across awaits, so A→B→A deadlocks until a timeout (CALLS B2), and
SmSa measured 80% of time waiting for whole-actor turns (CALLS B4). I-confluence is necessary and
sufficient for coordination-free execution, and 10 of 12 TPC-C invariants are I-confluent (LAWS F1).
Herlihy, Liskov and Shrira sketch a proof that a semi-synchronous deal needs one ledger every party
consults, and escrow into it is a prepare that cannot fail (CALLS G1, A1).

**Cost.** It needs a multiversion map, a scheduler, a refinement theorem, delta actions, a coordination
ladder, lease templates, deal cells and saga compensations. Bread had none of this running: it executed turns
serially under one lock (BREAD §1.4).

**Rules out.** It rules out declared write locks as the scheduling unit; batch-dependent semantics (Aria, CALLS F4);
locks held across yields by default; and implicit two-phase commit across domains.

### G. Metering and storage

**Decision.** One signed envelope per invocation (decided 10-04); a Lean cost theorem: metering is a
function of pre-state and invocation, and meter ≥ machine transitions including kernel work (codec,
collection at the yield, law checks, Merkle updates). Exhaustion parks the activity and refunds the unused
remainder; it never terminates. Meters are accounting, not scheduling. Every retention structure (inbox,
await index, watcher table, recovery list) is a cell with a payer; storage is a deposit; unfunded objects
hibernate (evicted to their Merkle hash, restorable) and are never deleted; in-domain collection traces
cycles; termination is O(1) by detaching the subtree. Resolution G1 fixes the refund rule: the
never-refund rule covers measured quantities (unused envelope, ticks); exhaustion parks the activity and
its resume needs a new envelope; deterministic, measurement-free amounts may be returned, namely the
postage of sends never delivered (broken slots) and the unused half of an escrowed resume/timeout fee
pair; no refund ever depends on how much computation ran.

**Mechanism.** The envelope is the 10-04 charge law: caller-declared `{ticks, heap, stack, outputBytes}`
priced by a public tariff (SWARM-LEDGER 05:30, item 3), extended with kernel-work terms. A new
`Theory/ObjectiveBendCost.lean` (**new**) defines

```lean
def cost (s : World) (inv : Invocation) : Nat :=
  machineTicks + codecBytes(checkpoint) + collectWork + lawWork(constraints evaluated)
  + merkleWork(cells written) + storeReads(cells forced)
theorem cost_function : admit s inv = admit s' inv → … -- cost depends only on (s, inv)   -- T6
theorem meter_dominates : transitions s inv + kernelSteps s inv ≤ cost s inv            -- T6
```

Admission refuses a turn whose cost exceeds its envelope. An authenticated invocation that preparation
or admission refuses is charged the tariff price of its declared envelope, and the debit is committed in
a refusal receipt outside the refused turn (`Kernel/AdmissionPrologue`'s two stages). The wall-clock
refusal lane that landed in main `6455353d` (`Kernel/RefusalLane`, per-subject wall time in Host memory)
is mempool policy only: it may decide what a Host proposes, never what a replica validates, and a
committed block is never re-judged against a lane, because wall time is not a function of state and
invocation (merged from OS review W5; not yet ruled on by the root). For an activity, a resume that exhausts its declared envelope
commits an `exhausted` receipt: the full declared price of the envelope it ran under is consumed (from
the escrowed fee for the path, plus any submitter-added envelope), and the checkpoint, the await and the
record's generation are unchanged, so the activity is parked at its yield and its next attempt needs a
fresh envelope (`AwaitsFunding`). Exhaustion is never free and never refunded; the charge is a function of
the declared envelope only, so it is measurement-free under resolution G1 (merged from HIST review F3; ruled 10-05). Each await escrows a fee pair priced from declared
envelopes; the turn that ends the await uses one fee and the other is returned. The landed kernel does
exactly this (`Escrow.used`, `Escrow.unused`, `refund_measurement_free` in `Kernel/ObjectiveActivity`),
with a ticks-only tariff (`Tariff.price ticks = base + perTick · ticks`) and fee accounts that are kernel
cells standing in for the Book.

**One tariff (merged from FRONTIER review §3.3 and OS review W4; ruled 10-05).** There are now two tariffs: the native
route's `Tariff.workOf`, which prices `typeFuel`, heap, stack, input and output bytes and checks a
ten-dimension usage vector against the declared capacity (main `796d7d7a`), and the activity kernel's
two-field ticks tariff, which leaves the package re-check and the checkpoint codec unpriced although
every `resolve` and `deliver` re-runs `loadProgram` (a full `checkWithin` of the package, with `typeFuel`
up to 16,384 per check in the world config). Every kernel turn, activity turns included, is priced by the
one native `Capacity`/`Tariff` and checked by the one `usage` vector, extended with `checkpointBytes`
(decode plus encode) and `lawConstraints`. A package is type-checked once, by its publish turn, which
commits a verdict cell keyed by the package identity; later turns load the checked core from that cell
and type-check only the instantiation and the response. That is sound because checking is a
deterministic function of committed bytes, and a checker change is a Core4 epoch, hence a re-genesis.
The activity kernel's own tariff and its fee-account cells are deleted when escrow binds to the Book.

**Deposits and disposal (merged from FRONTIER review §3.3, OS review W4 and W7, HIST review F4; ruled 10-05, including reclaiming decided slots).**
Decision G makes storage a deposit. Every cell the activity kernel creates or grows (record, answer slot,
checkpoint, package) carries a storage deposit posted by a named payer in that turn, priced from the
bytes written. A checkpoint's deposit is re-priced at each yield on the post-collection size, and the
difference is posted either way; that is collateral on committed public bytes, not a refund of
computation, so it is consistent with G1. Every activity ends in a disposal turn: a `done` or `faulted`
record is deleted in the turn that ends it (its result lives in that turn's receipt), and its deposit
returns. A decided answer slot's cell is reclaimed by the delivery that consumes it. An activity parked
past its deadline plus a fixed grace height may be abandoned by anyone; that
turn decides its open slots `expired`, frees its checkpoint, consumes the timeout fee and returns the rest
of its escrow and deposits to the payer. ABORT (§C) uses the same disposal. No cell outlives its last
reader without someone paying for it. Storage deposits reuse `Kernel/QuotaGcSettlement`, which already
admits lease-backed insertion, quota checks and reachability-safe compaction as settlements. Every inbox,
answer slot, await escrow, history slot and checkpoint cell names its payer. Hibernation replaces an
unfunded object's subtree with its root; restoration is a turn that presents the preimage and a deposit.
Object collection traces the in-domain capability graph, which is all kernel-held, and termination
detaches an object's subtree root under a termination capability minted at creation. Bytes Mini publishes
to fn are the one storage class that is not a deposit: they are permanent by fn's theorem (PRF-088), so
they are charged a non-refundable permanent-history fee at publication, sized by octets and fn
transactions; an unfunded publication is refused before posting, never hibernated. Who receives the fee
is QE-6 in the fn contract (merged from FN review §2.4).

**Admission order under saturation (merged from OS review W6; a new rule, not yet ruled on by the root).**
Under saturation the sequencer orders pending invocations by a published deterministic rule over their
declared fee, so that replicas can audit it, and never by the count of subjects, objects or activities;
resumes of escrowed awaits are ordered by their deadline height. This orders admission; it is not
meter-tree scheduling.

**Why.** Agoric leaves deserialisation and post-crank collection unmetered on purpose, because XS
collection timing differs after snapshot reload and metering it would fork consensus; Mini's collection
runs inside the Lean semantics, so it can be metered (FRONTIER §1.4). Broken Metre found EVM gas
uncorrelated with CPU time, with programs over 100× slower per unit of gas than typical ones (OS §5).
KeyKOS "never built a scheduler using the meters", EROS found meter trees "inconsistent with … real-time",
and Coyotos was "abandoning meters entirely" (HIST 1F). Agoric's terminate-on-exhaustion forced it to
invent suspension (#8955). An unpaid safety feature, ERTP recovery sets, held about 60% of Agoric's
key-value entries (#8400), and a 310 MB cross-vat cycle was uncollectable (#8401) (FRONTIER §1.5).
Ethereum's rent stalled, Solana replaced rent with deposits, and ICP deletes frozen canisters (OS §4, §5).

**Cost.** It needs a cost semantics and its theorems, kernel-work pricing per input size, payer fields on
every retention cell, hibernation and restoration, and a tracing collector over the capability graph.

**Rules out.** It rules out terminating objects for lack of funds; meters as a scheduling instrument; unpriced kernel
work; and storage nobody pays for.

> **Scribe note G1 (refunds). Resolved by the root.** The 10-04 charge law reads "refuse on excess; never refund" (SWARM-LEDGER
> 05:30, item 3). Decision G says exhaustion "refunds the unused remainder", D says broken slots
> "propagate and refund", and B escrows the fees of both the resume turn and the timeout turn of an
> await, only one of which ever runs. These cannot all hold. Two consistent readings exist: (a) the
> charge law forbids refunds of an invocation's own envelope, while escrows (await fees, send postage) are
> deposits returned when their obligation ends without running; or (b) an await escrows one fee that
> whichever terminal turn runs consumes, and nothing is refunded. Bread's conditional turns refunded the
> deposit on resolution and burned it on timeout (BREAD §1.2), which is a third rule. Parking itself is
> consistent with "refuse on excess": a refused resume leaves the activity at its yield. *Resolution:*
> reading (a), restricted to measurement-free amounts: never refund measured quantities; return
> undelivered postage and the unused half of an await's fee pair; parked resumes need a new envelope.

### H. Presentation and debugging

**Decision.** Every object answers `describe`, `affordances` and `history`; an affordance is `Hidden`,
`Disabled(reason)` or `Enabled`, the reason computed by the same law check admission uses; projection code
is effect-free. The root's ruling of 10-05 adds `Possible` (law satisfiable) and defines `Enabled` as
"simulated admission succeeds". Causal edges on every receipt; unhandled faults route to the object's keeper.

**Mechanism.** A new `Host/ObjectProjection.lean` (**new**) computes, for a viewer with a capability set:
`describe` = the declared-state fields the viewer may observe (the `Observe` cut of
`Kernel/Contracts/Cuts`), the pin, the upgrade policy, who holds each governing capability, and the
decider of each of its activities' open awaits (merged from FRONTIER review §3.6; today nothing shows a
viewer who can answer an await); `affordances` = for each method, `Hidden` if no capability the viewer
holds can reach it; `Disabled(residual)` if the guard or law is `.unsat` for the viewer, after
redaction; `Possible(example)` if the law has a witness; `Enabled(example)` only if a `simulate`
admission of the method with that example argument, at the card's root, admits. A satisfiable law shows
only that the law could accept, not that the method produces a Plan the law accepts, so `Enabled` is
decided by simulating the method, which is the same check admission runs (merged from OS review W8; the
root's ruling of 10-05 adds `Possible` to decision H's three states). `history` = receipts touching the object with their causal edges (the invocation, the answer slot or
inbox delivery that caused it). Each card also carries `(root, Merkle path, object pin, renderer pin)`;
names render through the viewer's petname cell; the meta-card (pin, law, upgrade policy, activities,
history) uses a kernel-pinned renderer, never the object's package; per-viewer layout and drafts are
local-first and never cells (OS review W8; OS §6, §3.5, §4.2). Projection functions are typed without `Ty.computation`, so they cannot yield. Faults (§B)
are sends to the keeper capability the object names at creation.

**Why.** Bread's affordances were live only if caps covered them and the live state admitted them, and
its surface judged `(s, s)` while its executor judged `(s, s')`, which META §9.1 identifies as the reason
preview and commit types must differ (BREAD §2.1 #10). Naked Objects and Apache Causeway are the prior art
for a card as an authorized view plus behaviour (OS §6.C). Agoric's governance design goal is legibility:
"observers … are able to see who has control" (FRONTIER §1.14). Causeway's causal view was the one
debugger the E community shipped, and Tribble's keeper model routed faults to an object's keeper (HIST
1G).

**Cost.** It needs one projection module, a satisfiability call per affordance per render, and causal
fields on receipts.

**Rules out.** It rules out cards that show an affordance admission would refuse; projection code that writes; and
upgrade or termination powers invisible to the viewer.

### I. fn

**Decision, as revised by the root after FN-CHECK.** fn is Mini's archive, feed and transport for exact
bytes now: finalized blocks and receipts (bundled several blocks per article), replay kits, published
package bytes, and cross-domain deal and saga messages. No checkpoint of any kind goes to fn, because a
signed article is never reclaimable by theorem; hibernated object data and replay logs go there only if
paid for as permanent history. fn sits under the hot per-turn log later, gated on fn's page
representation and the `fn-store-1` freeze. Mini pins fn by image digest, node identity, schema digest,
format word and history-id (history-id alone survives export/import). The contract is
`designs/MINI-FN-660-REQUIREMENTS-20261004.md`, whose Scribe notes SN-1 to SN-6 the root accepted.

**Mechanism (replaced from the FN review §2.1; the contract document owns the details).** One signed
archive article carries the finalized blocks of heights `[h, h+K)` and their receipts. Its Message-ID is
Mini's digest of the bundle bytes, and K is chosen so a bundle fits fn's article bound A and one poll
page; the operator sizes fn's transaction budget T and heap H together (bundling saves T and per-record
heap, not H; contract §3.3). Every Mini post goes through fn's control socket (`hybrid-author`), never
NNTP POST, because POST answers 441 for duplicate, conflict, refused and uncertain alike. fn's exit
classes (0, 1, 3, 4, 5, 6, 7; there is no 2) map as follows: 0 → transport accepted; 1 `conflict` → Mini
keeps its own carrier as evidence, since fn stores none; 1 `busy`, `clock-unusable` or no owner reached →
retry the same bytes; 1 with any other reason → refused with that reason, a budget reason becoming
`AwaitsFunding`; 3, 4 and 6 → unknown, resolved only by an authoritative lookup or a same-bytes resend
(exit 4 can follow a durable commit); 5 → a Mini defect; 7 → nothing was sent. Mini pins (fn
running-image digest, format word, genesis node identity, schema digest, history-id, incarnation) and
keeps its SQLite hot log, the home of every checkpoint, with its head anchor (MI-01, MI-04; contract
SN-1, SN-4, SN-6).

**Transport outcomes are not answers (merged from FN review §2.2).** fn outcomes are transport facts of
an outbound post and are never written into an answer slot, because a slot is write-once
(`Kernel/AnswerSlot`) and an `unknown` written there would leave the post's later resolution nowhere to
go. The sender's outbox owns them: it retries the same persisted bytes on unknown and on transient
refusals until fn gives a definite answer, and records that answer. A slot is decided only by its
decider: for a cross-domain call, the counterpart's reply, admitted when it arrives as an fn article;
otherwise it expires at its deadline (`TimedOut`). A definite, non-transient refusal of the outbound
message (for example `author-not-enrolled` or `unknown-group`) cannot decide the counterpart's slot;
whether the sending kernel may then break its own pending slot (Bread's contagious breakage applied to
transport) is open question QF-B for the `send` lane (L6). Without it, a misaddressed message costs the
activity its full deadline.

**Why.** fn is an append-only, signed-exact-bytes log and feed with accepted, refused and uncertain kept
distinct and idempotent resend, which is what an archive and a transport need (FN §0). Its per-record heap
(about 3.6 KB), its open time (16–22 s at 40k records), and 36 posts/s on hbox's ZFS rule out one record
per turn before the D41 page representation lands (FN §3.2). fn's transaction budget is an operator
profile field: the live nodes run the 16 MiB friend rung, T = 32,768 = H/512, and a raise needs a heap
figure that fits the reservation. fn's durable-after-ack keystone is stated over a batch layer the served
commit never calls; its successor is a log-kernel theorem, 4–7 lane-days, which fn has scoped (contract
M1; FN review §2.1).

**Cost.** It needs one article profile, an archive publisher, an outcome mapping and pins. **Rules out.**
It rules out checkpoints in fn, fn as the only copy of anything Mini needs before `fn-store-1`, Mini
decisions that depend on fn's local numbering or arrival order, NNTP POST as Mini's post path, and fn
outcomes written into answer slots.

**Code defects fixed in lane `scholar-fn` (not yet landed; FN review §2.5).** Eight ack sites in
`Host/Main.lean` read fn's refusal as exit 2, a code fn has never emitted, so every real refusal became a
transport fault and each site's recovery path was dead; fixed with `Host/FnOutcome.ackStatus` and three
theorems. Four poll and status paths collapsed every nonzero exit with stderr discarded; fixed with one
`runFnLocal` helper that names fn's class and reason. `FnPortableSource.decodeGroups` was a `partial
def` with three copy-pasted encoders; replaced by a total `Kernel/Base64` with `decode_encode` and
`encode_decode`. Still open: the hand parsers of fn's text lines (waiting on fn's M5 export) and the
node-identity pin (waiting on M4).

---

## 3. The theorems Mini should state

Each theorem below names its premises, an inhabitant that makes the premises true of a built object, and
a tooth: a mutation of the implementation that must turn the theorem's test red. No theorem is admitted
whose premise is uninhabited, and none may be stated over a model the kernel does not run; the Bread
record of apexes over empty premises (META "A warning that governs every section") is the reason.

**T0. Agreement** (merged from FRONTIER review §3.6). *Statement.* `core4_bigstep_unique`: Core4 has a
deterministic big-step semantics whose result is unique, so every replica's re-execution of an admitted
invocation produces the same Plan. *Premises.* A closed, checked term. *Why it is separate.* Following
the vWasm split (FRONTIER 2.D D1), sandboxing (every transition is a signed, paid, law-accepted Plan)
must not depend on it, while replica agreement does. The first native receipt is labelled "a deep source
evaluation (not proved unique)" for exactly this gap. *Inhabitant.* `world/NativeReceipt.obend`.
*Tooth.* A deliberately nondeterministic evaluator variant fails the uniqueness check on a term with two
`case` arms that both match.

**T1. Resume contract** (`Kernel/ObjectiveActivity`, `Kernel/ObjectiveResumeContract`). **Status:
mostly landed** (main `8194e09d`, `7494ca13`). *Landed statements.* `resume_consumes_once`: once a
delivery's intent installs, no later intent that spends the same await claim is ever accepted under any
schedule, and the exact retry replays (Khan's CO-c and CO-e); `second_delivery_refused` is its
corollary for deliveries. `resume_binds_checkpoint`: the resumed machine state is decoded from the
record cell's own checkpoint bytes, whose digest the await id names, and resumed with the typed
outcome; nothing of the state comes from the request. `resume_deterministic`: two deliveries of one
record at one snapshot and height with one envelope end identically. `slot_decided_once` and
`slot_single_decider`: a slot is decided once, by its decider, on an open slot, at or before its
deadline. `stale_reads_conflict` and `current_reads_exact`: a moved recorded read yields `conflict n`
with `n > 0`; current reads yield the settled outcome itself. `refund_measurement_free`: the returned
fee is a function of the escrow and the path only. `birth_checkpoint_typed` and
`delivery_checkpoint_typed`: every stored checkpoint decodes to a well-typed state (resolution B3).
*Changed by the 10-05 ruling (resume with view).* `stale_reads_conflict` and `current_reads_exact` are
replaced by `resume_outcome_preserved` (the delivered outcome equals the settled one; no kernel path
replaces, drops or rewrites it), `resume_view_current` (the view is the object's declared state and
version at the delivering snapshot, exactly as the response carries it) and
`yield_write_from_current_read` (every committed state post's expected root equals the root the same
turn delivered in the view); exact statements are in the BREAD review appendix A.2. The tooth: delivering
a view from the record's old read set makes the demo's owner write vanish. *Still to state.* (a)
`resume_rechecks_today`: a delivery is judged under the object's current law (an instance of
`Contracts.install_rechecks_today`), once objects have laws (lane L3). (b) `resolution_grants_nothing`:
resolving a slot adds no capability to any c-list beyond the resolved value's own references, once values
can carry references (lane L6). *Premises.* The program is checked
(`Checked source []`), the yield was admitted, and installation is `DurableDataIntent.execute`, the
kernel's own relation. *Inhabitant.* `world/activity/Tally.obend` on a durable scratch world (46 of 46
checks). *Teeth.* The demo already exercises a double resume, a forged spent await and a tampered
checkpoint; under the ruling, its scenario B must show the owner's 99 and the decider's 7 both kept
(state 106) and a two-activities-on-one-object scenario must keep both activities' writes. The remaining
tooth is a mutation run (drop the nullifier spend, drop the digest check, drop the version
check), each of which must turn a named check red. Bread's `commit_resumes_once` shows what
to avoid: its handler premise `resumeWith : (Reply : Type u) → Reply` is uninhabited (ROOT correction).

**T2. Re-entry guard soundness** (`Kernel/CallFrame.lean`). *Statements.* (a) `admitted_turn_reentry_free`:
in every admitted turn, no object occurs twice on any call stack the real `callStep` builds. (b)
`frame_conflict_refused`: no admitted turn contains a frame whose read set intersects a later-applied
fragment's write set, or two fragments writing one slot whose law does not declare the write a
commutative delta (resolution D2). (c) SeRIF's semantic form (FRONTIER 2.F F1): for every per-object invariant `I`
expressed as a law, if every callback-free execution preserves `I` then every admitted execution does.
*Premises.* The statements are about the real call-stack executor and assume nothing about programs.
*Inhabitant.* An A→B→C call chain admits. *Teeth.* An A→B→A chain is refused; a DAO-shaped example (a withdraw whose callee calls back
and withdraws again with a stale balance read, every write individually law-valid) commits when the guard
is removed and is refused with it. Statement (c) alone would be close to a tautology given (a); its
content is (a) and (b) over the executor admission actually runs, and the DAO tooth shows the guard is
load-bearing. (d) `callee_sees_no_pending_caller_write`: under apply-at-return (the root's ruling on
OPEN 1), no frame reads a write of a frame still below it on the stack; this is the condition the
FRONTIER review attached to its "yes" to OPEN 1. The guard's cost is measured, not proved: lane L5 counts, on Mini's own cohorts, the
turns the guard refuses that an ECF check would admit (resolution D1).

**T3. Offer safety for seats** (`Kernel/Seat.lean`). *Statements.* (a) `seat_offer_safe_forever`: from the
`offer` that creates a seat, in every state reachable by admitted turns while the seat is open, the seat's
Book balances satisfy `offerSafe p`. (b) `exit_enabled`: in every such state, the offerer's `exit` is
admissible given its envelope, and it posts exactly the seat's allocation to the offerer. (c)
`seat_conserves`: every admitted posting touching a seat conserves per-asset totals (from
`Operation.apply_conserves`). Payout liveness is (b) plus a justness assumption on inclusion of submitted
turns (van Glabbeek; LAWS H2), stated as a hypothesis on the schedule, never on the seat. *Premises.*
The initial allocation equals `give` (the `offer` action establishes it), and seat slots are total.
*Inhabitant.* A two-party swap seat settles, and another exits. *Teeth.* A reallocation that leaves less than
`want` and less than `give` is refused; a contract clause that forbids `exit` does not stop it; making a
seat slot absent instead of 0 flips the verdict of `not le` and must be caught by a totality check; a
`want` of 0 of an asset is always met (the `atLeast` fix); an empty `want` without `donate` is refused at
`offer` (LAWS review D-5); a debit of a seat by a turn of another instance is refused (FRONTIER review
§3.4).

**T4. Parallel admission equals the sequential fold** (`Kernel/ParallelAdmission.lean`).
*Statement.* `parallel_eq_fold`: for every pre-state and batch, the parallel run's receipts, refusals and
root equal `batch.foldl admitOne s`. *Premises.* `admitOne` is deterministic (re-execution is), and the
multiversion map returns, for every read, the latest earlier write in log order. *Inhabitant.* Two
batches are built: one with disjoint footprints and one where invocation 2 reads a cell invocation 1 writes.
*Teeth.* Skipping validation produces a different root on the conflicting batch; treating a delta as a
read changes nothing in results but must show in the published DAG.

**T5. Collection at the yield preserves behaviour** (`Theory/ObjectiveBendDemandCollect.lean`, **new**,
with task `01a1056f-00a4`). *Statement.* `collect_bisim`: for a yielded state `s`, `collect s` is
yielded, `state_roundTrip` holds for it, and for every closed response `r` of type `R`, running `resume r s`
and `resume r (collect s)` produce outcomes equal up to heap-address renaming, with the same Plans.
*Premises.* The yield is typed (`typed_yield_quiescent`). *Inhabitant.* `EventCounter.serve` is collected
after ten turns.
*Teeth.* A collector that frees a cell still reachable from the stack changes the next Plan.

**T6. Cost semantics** (`Theory/ObjectiveBendCost.lean`). *Statements.* (a) `cost_function`: cost is a
function of (pre-state, invocation). (b) `meter_dominates`: machine transitions plus kernel steps (codec
tokens, collection work, law constraints evaluated, Merkle nodes rewritten, cells forced) are at most the
cost. (c) `envelope_sound`: an admitted turn's cost is at most its signed envelope, and its charge equals
the envelope. *Premises.* The tariff is a public function of the cost terms. *Inhabitant.* The
`EventCounter` turn and a seat reallocation are priced. *Teeth.* A turn with few ticks and a large checkpoint or a
large law: dropping the codec or law term from `cost` breaks (b) on it. Two further statements: (d)
`exhaustion_charges_declared`: an exhausted delivery commits a receipt charging exactly the declared
envelope's price and changes no checkpoint, await or generation (HIST review F3); (e)
`disposal_frees_record`: the turn that ends an activity deletes its record and returns its deposits (HIST
review F4).

**T7. Upgrade gate soundness** (`Kernel/ObjectUpgrade.lean`). *Statements.* (a)
`upgrade_preserves_floors`: if an upgrade is admitted, every step `(old, new)` the new law admits also
satisfies every frozen floor (from the `SysCert` and `certificate_unsat`). (b) `upgrade_state_conforms`:
the migrated state conforms to the new declared type and satisfies the new law. (c)
`upgrade_dispositions_total`: the committed upgrade assigns exactly one disposition to every live activity.
(d) `drain_never_sees_migrated_state`: no turn writes the object's state under the old package after
MIGRATE, and MIGRATE is admitted only when no drained activity remains. (e) `drain_bounded`: at any
height at or past the drain deadline, every remaining drained activity can be aborted with `Upgraded`.
(f) `upgrade_refusal_inert`: a refused ADOPT or MIGRATE changes no cell. (g) `migrate_total`: while an
object drains, every admitted state write `s'` has `migrate s'` well-typed and accepted by the new law,
so MIGRATE is admitted whenever no drained activity remains (FRONTIER review §3.5, ruled). (h)
`draining_runs_no_new_code_on_old_schema`: unless the old state type is a subtype of the new, no birth or
call under the new package is admitted between ADOPT and MIGRATE (ruled). (REPLAY is dropped, resolution
C2, so revision 1's `replay_admitted_only_if_equal` is withdrawn. REBIRTH's restartability is checked
at publish by a CI test, not by a theorem.) *Premises.* Floors lie inside the
difference fragment, and the migration term is typed. *Inhabitant.* One upgrade adds a field with a
default, and another renames a field. *Teeth.* An upgrade that weakens a floor is refused with a certificate; an
upgrade that omits an activity's disposition is refused; Bread's `migrate_conforms` false premise (field
add does not conform to the new schema, META §7.1) must reappear as a refusal, not a theorem; a drained
`EventCounter.serve` is aborted at its deadline, after which MIGRATE admits.

**T8. Choreography step soundness** (`Theory/ProtocolObject.lean`). *Statements.* (a)
`protocol_step_sound`: an admitted turn on a protocol object moves its state from `q` to `q'` only if `q'`
is the residual of a `GStep` of the global type denoted by `q`, by the role bound to the signer, on the
invoked label. (b) `protocol_progress`: for a guarded global type whose residual is not `done`, the law is
satisfiable: `Pred.Sat` returns a witness for some role's step. *Premises.* The global type is guarded and
compiled by the module's own compiler. *Inhabitant.* A three-party escrow protocol runs to `done`. *Teeth.* An
out-of-order step is refused; Bread's two refutations (`deadlock_initial_counterexample`,
`privacy_var_counterexample`) are kept as regression theorems so the false statements cannot return.

**T9. Every write is judged** (merged from LAWS review D-1 and D-2 and OS review W1; ruled 10-05).
*Statements.* (a) `receive_committed_lawful` (`Kernel/Receiving`): every write of a committed ingress
either has a committed law that accepts its step or lies in a registered kernel cell class whose writers
are proved to be kernel families only; proved once over `Family`. (b) `objective_artifact_slot_sound`: in
every `AcceptedInvocation`, the projected `objective/artifact` slot equals the executed artifact's
identity. (c) `activity_write_judged`: every committed activity state write satisfies the object's law at
`(old, new)` and was presented with a facet capability of the object. *Premises.* The real `Family`
record and the real accepted-invocation constructor. *Inhabitant.* `SubjectKeyRotation` migrated as the
first `step`-carrying family; the Tally world under `ObjectRecord`. *Teeth.* A fixture family whose write
violates its cell's law commits when the check is removed and is refused with it; an ordinary command
writing an Objective object's state cell is refused naming the pin clause; a payer without the facet
cannot write.

---

## 4. Where the scholars disagreed, and how the decisions resolve it

**Checkpoint lifetime.** OS (Part I §1) wanted continuation checkpoints short-lived by policy, citing
Electric Communities, PJama, Motoko and Urbit; CALLS (Part II.4) traced those failures to two causes,
code identity changing under a continuation and continuations holding mutable views of state, and argued
that hash pinning plus a capture rule remove both; FRONTIER (Part 3 §6) used Agoric's rebuild of durable
async as evidence that long-lived continuations are wanted anyway. Decision B takes CALLS' and FRONTIER's
side on lifetime (as long as the awaits) and OS's side on role: durable state is declared and the
checkpoint is never the thing that migrates (decision A).

**Upgrade dispositions.** OS (§8) and CALLS (idea 8) offered drain, replay, map and abort; FRONTIER
admitted MAP only for activities that are con-T-free in the Proteus sense, scanning inside thunks (2.D D5);
HIST (D2) rejected MAP as Frantz's clock surgery and allowed REPLAY only with fail-the-upgrade semantics.
Decision C followed HIST: DRAIN and ABORT, REPLAY only if it succeeds within the upgrade turn, no MAP.
The root's resolutions then dropped REPLAY (C2) and gave DRAIN a mandatory deadline and a separate
MIGRATE turn (C1), which goes further than HIST and answers CALLS' and DFINITY's drain-stall evidence.
On review, OS, HIST and BREAD showed that C1 as first written ran new code against the unmigrated state;
the root's ruling of 10-05 closes the object to new births and calls while it drains (unless the state
type only widens), makes MIGRATE total, and adds HIST's REBIRTH disposition.

**Codec epochs.** OS (§4) proposed a checked `decode_old → encode_new` for a Core4 or codec change; HIST
(D1) answered that no system migrated machine state reliably (Smalltalk "cannot be made reliable", EC
"effectively intractable", Agoric snapshots "unusable" after an engine change). Decision C follows HIST:
an epoch change drains or aborts.

**Footprints.** OS (§3) wanted invocations to declare read and write sets; CALLS (Part II.3) found
Block-STM matching declared systems without declarations and Solana's declared locks over-serialising.
Decision F follows CALLS: footprints are learned and declarations are hints.

**Pipelining.** One CALLS reading lane argued that pipelining saves the caller a signed, paid resume turn
per hop even on one Host; Agoric leaves pipelining off for every local vat, and HIST (D5) put its value in
cross-host latency and its cost high. CALLS (Part II.2) split the two halves: queueing at an unresolved
slot saves turns in-domain, early delivery saves latency only across domains. Decision D adopts the split
and sequences early delivery last.

**Call order.** Tezos moved to depth-first, Urbit is moving to breadth-first (CALLS Part II.1). Decision D
keeps both as two mechanisms with fixed orders, depth-first for `call` and breadth-first for `send`, and
never a mixed order.

**Re-entrancy.** LAWS (idea 3) proposed a dynamic ECF check at admission; CALLS (Part II.6) proposed
refusing re-entry by default with ECF as an opt-in; FRONTIER (Part 3 §2) made the guard mandatory on
Agoric's evidence. Decision D1 makes refusal mandatory. The decisions do not say whether an ECF opt-in
remains available to an object's law; Scribe note D1 records that the cost of refusing ECF re-entry is
unmeasured.

**Cross-domain atomicity.** BREAD (§3.3) proposed Lean-decided two-phase commit with escrow; OS (§3)
forbade implicit two-phase commit in favour of a purposeful cell; CALLS (idea 7) named the purposeful cell
a deal cell with escrow as the prepare; FRONTIER (Part 3 §10) restricted the deal cell to exclusive rights
and sent everything else to sagas. Decision F adopts FRONTIER's split.

**Caller protection.** LAWS (idea 2) proposed a per-invocation caller law (Zoe offers, Mina
preconditions); FRONTIER (Part 3 §1) read Zoe's source and showed offer safety is an invariant judged on
every reallocation for the seat's life, so the per-invocation law is the one-turn special case. Decision E
adopts persistent seats, and FRONTIER (Part 3 §2) supplied scoped grants for the authority half that
offers do not bound.

**Meters.** OS (§6) and FRONTIER (§1.4) adopted two-level meters with keepers; HIST (D3) agreed on per-turn
caps and payers and rejected meter trees as a scheduling instrument and any terminate-on-exhaustion rule.
Decision G follows HIST.

**Laws.** BREAD (§3.2) and LAWS (Part II, final paragraph) both recommended keeping the decidable language
and generating clauses from `.obend` declarations, citing Cedar's deliberately limited language; no
scholar argued for unification now. The decisions leave it OPEN (question 2).

**Several activities per object.** HIST and OS lane B cited KeyKOS's one-domain-at-a-time model with an
inbox, which shipped for a decade; OS lane A cited Midori's unsolved re-entrancy and argued for
footprints. Decision F allows several activities, makes them share state only through committed cells,
and replaces locks with leases.

---

## 5. Open questions for Ember

The questions are quoted verbatim from the decisions file. After the 10-05 reviews, the root recommends
treating all four as settled as summarised under each, unless Ember objects.

**1. "Synchronous cross-principal `call` (D1) at all, versus Agoric's 'never synchronous across trust
boundaries'. Root's lean: yes, with Daml authority + scoped grants + mandatory re-entry refusal."**
*For.* One Mini Host gives synchronous atomicity for free, and without `call` every cross-object
interaction costs a signed, paid turn per hop, which is the "sad, singleton-ish" interface Cap'n Proto
warns of (CALLS A5). Mina and Daml run synchronous value-returning call trees in production, and Daml's
non-transitive authority plus Pact's grants bound what a callee can do with the caller's power.
*Against.* SES documents that synchronous cross-principal interaction is where re-entrancy lives, and
Agoric chose a clean stack through promises (FRONTIER §1.7). A law-valid write derived from a stale read
passes every per-write law (the DAO shape, FRONTIER 2.F F1), so `call`'s safety rests entirely on the
guard and the frame-conflict rule being right. *Reviews and ruling (10-05):* all reviewers say yes.
OS and HIST: every capability OS ran synchronous call/return across protection domains (KeyKOS `CALL`
with a resume key, EROS, seL4, whose 20-year retrospective kept synchronous IPC), with busy domains
queueing callers, which is re-entry refusal by another name; Agoric's rule is a distributed-failure rule
for cross-domain links. FRONTIER: yes on condition that a callee never sees its caller's half-done state.
LAWS: yes, after the package-pin slots and Receiver-judged laws exist. BREAD: Bread without `call` led to
client-computed effects and "lamesauce". The root recommends to Ember: yes, with the callee reading the
turn's state, writes applied at frame return, re-entry refused and the callee billed to the caller's
envelope (Scribe note D4 asks whether the frame-conflict aborts survive).

**2. "Laws: generate from `.obend` now, unify later (root's lean), or unify now."**
*For generating now.* Cedar keeps a separate, deliberately limited language because analysability is the
point (LAWS D1), and Mini's `Pred` already has satisfiability, certificates and refusal explanations that a
general fragment of Objective Bend would have to re-earn. Refinement types show how `requires` and
invariants on signatures become clauses (LAWS E7). *For unifying now.* Two languages for one object are
two shapes that agree today and may disagree later, which the repo's doctrine names as a defect class; and
today's `spec` laws and `requires` strings already show the author's laws drifting away from the kernel's
(`docs/OBJECTIVE-BEND.md`: "nothing discharges them"). *Reviews and ruling (10-05):* BREAD, FRONTIER and
OS: generate now (Agoric and Cedar both built a small decidable sublanguage despite every incentive to
unify). LAWS refines the question: unify the syntax now (`invariant`, `guard`, `permit`, `forbid` clauses
compiled by the Lean elaborator to `Pred`, refusing anything outside the fragment), keep `Pred` as the
judge, and keep Objective Bend method `law`s as package evidence. The root recommends LAWS' refinement to
Ember (merged into §E "Surface").

**3. "REPLAY as an upgrade disposition at all, or DRAIN/ABORT only."**
*For REPLAY.* Mini's checker is exact: the Plans an activity yields are first-order data, so equality of
replayed Plans is decidable inside the upgrade turn, which is the fix Agoric's #12315 asks for (FRONTIER
§1.12). It lets a bug-fix upgrade keep long-running activities instead of aborting them. *For DRAIN/ABORT
only.* REPLAY needs every activity's full `(Plan, Response)` log retained and paid for (Scribe note C2),
and its replay must fit one turn's envelope. Agoric's replay machinery was where its 2025 chain halt and
its 2026 "wishful thinking" issue sit (HIST D2). *Root's provisional answer (resolution C2):* DRAIN
(with a deadline) and ABORT only; REPLAY is dropped for now, and Ember may reopen it. *Reviews and
ruling (10-05):* BREAD, FRONTIER, OS, HIST and LAWS agree with dropping REPLAY; HIST adds REBIRTH (abort
and re-birth from the record's stored input, with restartability checked at publish), and OS notes that
with receipts retained the interaction log is derivable from accepted intents, so REPLAY's real cost is
re-execution inside the upgrade envelope. FN adds that fn cannot be that log's home cheaply (signed
history is permanent by theorem, PRF-088), so a reopened REPLAY would need a priced Mini cell. The root
recommends to Ember: REPLAY dropped, REBIRTH added.

**4. "Order of building: answer slots and the resume contract first, then `call`, pipelines, seats,
protocol objects; cross-domain pipelining last."**
*Reviews and ruling (10-05):* every reviewer accepted slots and the resume contract first (now landed)
and asked for the object model next: OS and HIST put `ObjectRecord` and object authority before `call`,
BREAD puts resume-with-view before sends, FRONTIER puts the fixed resume contract, then seats and scoped
grants, before `call`, and LAWS puts the package-pin slots and Receiver-judged laws before the native
route and `call`; FN notes that the fn archive (L13) and the outbox fixes need nothing from answer
slots and can land before `call`, while cross-domain transport through fn needs the slots and an outbox
that owns transport outcomes. The root recommends to Ember: OBJECT-RECORD and RESUME-WITH-VIEW, then seats and scoped
grants, then `call`, then `send`. *For this order.* Every other feature needs a durable, once-only resume: sends need answer slots, seats
across a yield need parked activities, and deal cells need deadlines. Agoric added durable promises after
the fact and paid for it in three layers (FRONTIER §1.12). *For `call` first.* `call` is in-turn and needs
no answer slots, so it could land earlier and make residents useful sooner; and `call` with multi-action
fragments, like pipelines, is blocked on recursive Plan data either way (task `01a1056f-00a4`).

---

## 6. Build plan

Lanes in dependency order, each marked **done**, **partial** or **open** at main `36fca3ac`. "Warm base"
means the lane changes `Kernel/`, `Host/` or modules the default build imports and must build in a lane
cloned from the hbox warm base (`ssh hbox /tank/dregg-build/claude-lanes/warm-base/mk-lane.sh <lane>`,
then `swarm-build env LEAN_NUM_THREADS=4 lake build <targets>`; full gate `Minidregg
+Host.Main:leanArts ObjectiveProofs`); "plain lean" means its modules compile with plain `lean` into lane
oleans, as the S11 and PROOF-ENG lanes did. Since 10-04 ~10:50 EDT only the MERGE-KEEPER lane lands on
GitHub main, from requests in `work/MERGE-QUEUE.md`, after a post-merge gate on a warm copy.

**Order after the 10-05 ruling.** OBJECT-RECORD (L3, with object authority) and RESUME-WITH-VIEW (L1b)
come next, with QUEST-LAWS-PIN (running) and QUEST-LAWS-RECEIVER (L4a, before the receiver collapse's
step 3) beside them; then seats and scoped grants (L7, the grant half of L5); then `call` (L5); then
`send` (L6). No native route may expose activity `birth` or a state write before L3's object authority
and law judgement exist (HIST F1, LAWS D-3, OS W1, as ruled).

**L0. Prerequisites. Done.** The receiver collapse's first family (`Theory/Receiving`,
`Kernel/Receiving`; main `66967962`, `2c8839d2`, `47e653ed`) and the first native Objective accepted
receipt (`Kernel/ObjectiveBendNativeAdmission`; main `796d7d7a`). Every new turn kind below is a
`Receiving` family. Open inside L0: Core4 in `Compiler/Evaluator.registry` proper and a paid invocation.

**L1. Activity record, answer slots and the resume contract. Partial** (main `8194e09d`, `7494ca13`,
`3667e07d`). Landed: `Kernel/ObjectiveActivityWire`, `Kernel/AnswerSlot`, `Kernel/ObjectiveActivity`,
`Kernel/ObjectiveResumeContract`, `Host/ObjectiveActivityWorld`, `world/activity/Tally.obend` (46/46
checks), the T1 statements listed in §3. Open: the native signed route for birth, resolve and deliver;
object ownership; fees on the Book; the T1 mutation run; and `EventCounter.serve` and `TimerResident` as
native accepted residents. The ACTIVITY-NATIVE lane is running on these; per the reviews (FRONTIER §5),
its acceptance must also include: no unjudged state write, no authority from payment, one tariff with
checkpoint bytes and package-check fuel, deposits on record, slot and checkpoint cells, an `exhausted`
receipt that charges the declared envelope, and disposal turns. Its planned `Conflict(stale, outcome)`
is superseded by L1b.

**L1b. RESUME-WITH-VIEW. Open; ruled 10-05; quest written by the BREAD review (appendix A).** Modules:
`Kernel/ObjectiveActivity` (versioned `ObjectState` cell, `resumed {outcome, view}` response, `W(S)`
field/delta writes with `keep | set | add`, version compare-and-swap, `blindWrite` refusal, `conflict`,
`staleCount` and `revalidate` deleted, refused/broken reason sums, the package check cached at
publish), `Kernel/ObjectiveResumeContract` restated, `world/activity/Tally.obend` writing deltas, the demo.
Acceptance: `resume_outcome_preserved`, `resume_view_current` and `yield_write_from_current_read`
pinned; scenario B shows state 106; two activities on one object keep both writes; full gate on hbox.
Depends on L1's native route landing first (same module). Warm base.

**L1c. ACTIVITY-METERING-DISPOSAL. Open; approved by the root; quest written by the HIST review
(appendix A).** Sequence, one writer per file: ACTIVITY-NATIVE, then OBJECT-RECORD, then
RESUME-WITH-VIEW, then this lane. Scope: exhaustion as a committed turn charging the declared envelope
(admitted only when no delivery exists for the same snapshot, height and request; a zero total charge is
refused), disposal on terminal segments (record cell vacated, result only in the receipt), decided slots
reclaimed, the abandon turn after deadline plus grace, and a payer for every non-vacant cell (package
cells gain a `publisher`, a new package frame). Theorems: `exhaustion_charges_declared`,
`exhaustion_excludes_delivery`, `exhaustion_charge_measurement_free`, `disposal_frees_record`,
`birth_terminal_writes_no_record`, `decided_slot_reclaimed`, `abandon_returns_escrow`,
`abandon_delivery_exclusive`, `retention_cells_have_payer`, each with a demo falsifier. Open assumption
to check before landing: that `[]` is the store's absent-cell image. Warm base. Unblocks every later lane. Warm base.

**L2. Collection at the yield and recursive Plan data. Open (collection in progress in
ACTIVITY-NATIVE).** Modules: new `Theory/ObjectiveBendDemandCollect`; `Theory/ObjectiveBendDemandData`
and the checkpoint codec extended for recursive first-order data (task `01a1056f-00a4`); the
guardedness check (task `01a1056f-0083`). Acceptance: T5 pinned; `EventCounter.serve`'s checkpoint size
is constant across turns; a Plan carrying a list of actions round-trips. Unblocks L5 (multi-action
fragments), L6 and storage charging (resolution B4). Plain lean.

**L3. OBJECT-RECORD: objects, declared state and object authority. Open; ruled 10-05; quest written by
the OS review.** Modules: new `Kernel/ObjectRecord` (with `creators`, `keeper`, `schema`); object state
cells in a kernel namespace; a facet capability on every declared-state write; the object's law judging
`(old, new)` in birth, delivery and invocation; payer separated from authority; the activity kernel moved
from `object : CellId` to `ObjectRef` and its `writeState` deleted; the `state` declaration in the front
end (the TypeScript files today, the Lean elaborator once ELABORATOR lands); the `kind`/schema split in
`Kernel/Contracts/Identities` (resolution A1); the object law consulted by delivery (T1 (a)). Acceptance:
a package without a state declaration is refused by name; a birth naming a non-object cell is refused by
name; a Plan whose write violates the object's law is refused with the residual; a payer without the
facet cannot write; an object's id survives a re-pin and a migration; T9 (c) pinned; the Tally world's
checks still pass. Unblocks L4, L5, L7, L9, L10. Warm base.

**L4a. Laws judged structurally. QUEST-LAWS-PIN running; QUEST-LAWS-RECEIVER next (both ruled 10-05).**
LAWS-PIN: `objective/artifact` and `objective/method` slots projected in `projectCommonSlots` from the
signed claim, `artifactSlot`/`methodSlot` beside `ranSlot`, a `semanticsId` bump, and the kernel pin
clause at object birth (with L3); acceptance: an ordinary write to an Objective object's state cell is
refused naming the pin clause, the pinned method's write is accepted, T9 (b) pinned. LAWS-RECEIVER:
`Family.step`, `KernelCellClass` with its writer proof, `receive_committed_lawful` (T9 (a)),
`SubjectKeyRotation` first; acceptance: the fixture violation is refused with the check and committed
without it, rotation intents byte-identical; must land before the receiver collapse's step 3. Warm base.

**L4. Law language and publish-time checks. Open.** Modules: `Pred/Core` (`leOld`, `eqOld` and the other
old-slot forms), `Pred/Satisfiable` and `Pred/SatisfiableTotal` (the new atom cases), `Pred/Leaf`
(residuals), new `Pred/Entailment`, `Pred/History`, method guards and polarity in the package format,
`Kernel/LawView` (Plan action scope, Book slots; joint-command action scope and the redaction policy
already exist), the install-time floor check (LAWS review D-7), the propositional history compiler (D-8),
and the `invariant`/`guard`/`permit`/`forbid` surface (D-4). Acceptance: `decide_never_unknown` and
`certificate_unsat` re-proved with the new atoms; a necessity law ("balance decreases only if the
invocation presents the owner capability") is admitted and refuses a forged withdrawal; an always-false
clause is reported at publish. Unblocks L5, L7, L8, L9. `Pred` is plain lean; `LawView` needs the warm
base.

**L5. `call` and the output gate. Open.** Modules: new `Kernel/CallFrame` (apply at frame return,
callee billed to the caller's envelope, as ruled); `Kernel/OutboxDelivery` wired as the only egress;
scoped grants come from L7. Acceptance: T2 (a)–(d) pinned with the DAO tooth; a callee that tries to
spend beyond a grant is refused naming the grant; the frame-conflict and write-write rules as the answer
to Scribe note D4 settles them; the re-entry refusal count on Mini's cohorts is reported (resolution
D1). Unblocks L6. Warm base.

**L6. `send`, inboxes and pipelines. Open.** Modules: new `Kernel/Inbox`, `Kernel/Pipeline`;
answer-slot forwarding in `Kernel/AnswerSlot`; the activity record's `holds` list; the decision whether
`Kernel/ReactiveTerminalCell` stays beside `AnswerSlot`. Acceptance: a send to an unresolved slot is
forwarded in the resolving turn; a three-command pipeline admits atomically and refuses atomically; a
two-party partially signed pipeline settles a swap without escrow, and one segment over its envelope
refuses the turn (resolution D3); undelivered postage is returned (resolution G1). Unblocks L7. Warm
base.

**L7. Seats and scoped grants. Open; moved ahead of `call` by the 10-05 ruling.** Modules: new
`Kernel/Seat` over `Theory/CanonicalResourceKernel` and `Kernel/CanonicalEscrowMarket`, with invitations,
the `atLeast` offer-safety law, `donate`, and instance-only debits; `Kernel/ScopedGrant` (from L5).
Acceptance: T3 pinned with its teeth. Unblocks L11. Warm base.

**L8. Protocol objects. Open.** Modules: new `Theory/ProtocolObject` (port of Bread's `Coordination.lean`
types, `project` and `dregg_choreo`, with `mu` and guardedness), its transition-table law compiler with
payload guards (resolution E1). Acceptance: T8 pinned; a three-party escrow choreography runs natively.
Plain lean for the theory; warm base for its kernel law.

**L9. Parallel admission and the coordination ladder. Open.** Modules: new `Kernel/ParallelAdmission`;
`Pred/CoordinationDial` extended with the escrow rung and conflict tokens; delta actions. Acceptance: T4
pinned; a measured speedup on a disjoint batch; the published DAG replays to the same root on one thread.
Warm base.

**L10. Upgrade. Open.** Modules: new `Kernel/ObjectUpgrade` (ADOPT and MIGRATE families, the draining
gate on births, calls and writes, drain-deadline abort, the MIGRATING cursor for large objects, REBIRTH,
and the `restartable` publish test); exactly-once linear checking for migration terms in
`Theory/ObjectiveBendTyping`. Acceptance: T7 (a)–(h) pinned with its teeth; DRAIN, deadline abort,
ABORT and REBIRTH exercised on a live resident, then MIGRATE; a migration larger than one envelope
completes over several turns while the object refuses births. REPLAY is out of scope (resolution C2). Depends on L1, L3, L4. Warm base.

**L11. Metering and storage. Partial** (measurement-free refunds of the await fee pair landed in L1;
the native route prices a declared envelope, main `796d7d7a`). Open (ruled 10-05): one tariff and usage
vector for every Objective turn, with checkpoint bytes and package-check fuel; the package verdict cell
at publish; `exhausted` receipts; storage deposits re-priced at each yield; disposal turns; fees on the
Book instead of kernel account cells; `Theory/ObjectiveBendCost` with kernel-work terms; hibernation and
restoration over `Kernel/QuotaGcSettlement`; capability-graph collection. Not yet ruled: the refusal
charge committed in a receipt with `RefusalLane` demoted to mempool policy (OS W5), and the saturation
order (OS W6). Acceptance: T6 (a)–(e) pinned with its teeth; an unfunded object hibernates and restores
to the same root. Warm
base.

**L12. Presentation. Open.** Modules: new `Host/ObjectProjection` (four affordance states, `simulate`,
card provenance, petnames, the kernel-pinned meta-card renderer). Acceptance: for every affordance a card
shows as `Enabled`, the matching invocation admits; for every `Disabled(reason)`, it refuses with that
reason; `Possible` is unconstrained. Warm base.

**L13. fn archive and transport. Partial** (outcome-class, poll-path and base64 fixes in lane
`scholar-fn`, not yet landed). Open, as QUEST FN-DIRECT: `Kernel/FnArchive` (bundle codec, Message-ID, K
sizing against A and the 262,144-octet poll page, N1 named: equal bundle bytes give an equal
Message-ID), the Host publisher over `hybrid-author` (persisted before send, exact-bytes resend, N2
named), the acknowledged-Message-ID record under `MINIANC1`, read-back through `hybrid-verify-source`; the
hand parsers retired when fn's M5 export lands; `FnPollScopePin` extended once fn's M4 prints node
identity and schema digest. Acceptance: a bundle of K finalized blocks is posted once; an identical
resend answers `:duplicate`, exit 0, with no second record; the bundle is fetched back by Message-ID and
its authored source verified by Mini's content identity; a `430 withdrawn` answer is reported distinctly
from absence; a post during an fn restart resolves through `consumer position` or lookup, never through
a new identity; N1 and N2 `#assert_axioms`-clean; on an isolated fn developer image, never
`/tank/fn/node`. Warm base.

**L14. Cross-domain. Open.** Deal cells, sagas with compensating Plans and a weak-atomicity theorem, and
promise pipelining proper with handoff, in that order, after L1, L6 and L10. Warm base.

---

## 7. Review disputes

Scholar reviews (`work/REVIEW-SCHOLAR-*-20261005.md`) that dispute a root decision, rather than this
document's text, are recorded here with both sides quoted. Most disputes raised on 10-05 were settled by
the root's rulings the same morning: resume with view (BREAD R1, HIST F2, against FRONTIER's
`Conflict` payload), object authority, the draining upgrade with REBIRTH (BREAD R6, OS W2, HIST F5–F6),
metering and disposal, the `Possible` affordance (OS W8), seats, and the four OPEN recommendations. The
text above applies those rulings. Two disputes remain unruled.

> **Review dispute 1: frame-conflict aborts under apply-at-return (decision D1, resolution D2; BREAD
> review R2).**
> *Decision D1:* "a frame that read a version another frame wrote aborts the turn." *Resolution D2:*
> "two frames of one turn writing the same slot abort the turn, unless that slot's law declares the write
> a commutative delta (then deltas compose and the law judges the sum)."
> *BREAD review R2:* "Each frame reads the turn's current state: the snapshot plus every fragment already
> applied in this turn. A callee's fragment is applied to the turn's journal when its frame returns […]
> Because re-entry into an object on the stack is refused, no frame can observe a write made by a frame
> still below it, and no object's state can change while its own frame is suspended in a call. So
> applying at return is safe without a frame-conflict abort." Evidence: with deferred fragments, `A`
> calling `B.deposit` twice "reads the snapshot both times and aborts under D2"; Bread, Mina and Daml
> apply effects as they walk the tree with a journal and rollback.
> *FRONTIER review, OPEN 1:* yes to `call` "under one condition": "writes stay deferred and reads stay
> on the snapshot. If a later change lets a callee see the caller's in-turn writes, the answer flips to
> no." Under R2 a callee sees completed sibling calls' writes but never its caller's unreturned ones, so
> FRONTIER's stated property (no half-done caller state) still holds; its literal condition ("reads stay
> on the snapshot") does not.
> *Root's ruling on OPEN 1 (10-05):* "callee reads the turn snapshot, writes deferred/applied at frame
> return, re-entry refused, callee billed to the caller's envelope." It adopts apply-at-return and does
> not say whether D1's and D2's aborts are withdrawn (Scribe note D4).
> *For the root and Ember:* keep the aborts (conservative; refuses repeated calls into one object in a
> turn), or withdraw them as R2 argues (sequential composition; the delta declaration then matters only
> to the coordination grade).

> **Review dispute 2: where escrow quotas belong (decision F; BREAD review R5).**
> *Decision F:* "Escrow quotas (local quotas summing to the budget) let many activities draw on one
> balance."
> *BREAD review R5:* "Inside one domain, delta actions plus Block-STM validation already give the
> sequential result for a shared balance, so no quota is needed for correctness. The coordination grade
> there only predicts re-execution. Escrow quotas are for parties or replicas that must spend without
> consulting each other: across domains, offline, or on committee replicas. There they are Stingray's
> bounded counters […] with the `(f+1)/(2f+1)` ceiling when slices sit on Byzantine replicas." Evidence:
> Bread ran Stingray for exactly the cross-silo case (BREAD §1.4), and the single-machine principle (BREAD
> §2.1 #12).
> *Scribe's reading:* the two agree that quotas give coordination-free spending; they differ on whether
> an in-domain object needs them. Under decision F's own Block-STM admission with first-class deltas, an
> in-domain balance is correct without quotas, and quotas would add only to throughput when many
> activities spend concurrently. The root has not ruled.

**Review additions not yet ruled on** (consistent with the decisions, merged with attribution, and
listed so the root can confirm or strike them): OS W5 (the refusal charge committed in a receipt;
`RefusalLane` demoted to mempool policy; §G), OS W6 (the saturation admission order; §G), LAWS D-8 (history
slots propositional only; §E), BREAD R3 and R4 (send escrow and bounded queues; pipeline `valid_until`;
§D), FRONTIER §3.6 (exact-plan consent as the default protection; T0 Agreement; deciders on the card), FN
§2.1–§2.4 (the seven-class outcome mapping and six-field pin, transport outcomes kept out of answer
slots, the permanent-history fee; §I, §G) with its open question QF-B (may a sender break its own slot
on a definite transport refusal?), and OS W9, which the root has passed to Ember: the `mini-keys` broker holds three secret classes in one
account.

---

## Changelog

**Revision 2 (2026-10-05).**
- Header: revision 2 reads main `36fca3ac`; Scribe notes now carry the root's resolutions.
- New §0: what landed overnight (the cut `5b6d6eca`; BendTT deleted `9ccd6a2d`; first native Objective
  accepted `796d7d7a`; activity kernel `8194e09d`, `7494ca13`, `3667e07d`; receiver collapse first family
  `66967962`; refusal charging `6455353d`; ZK truth `a006d243`; tenancy step B `06ddad68`) and what is
  running.
- §1: outcome sum gains `Conflict`; upgrade is two-phase (ADOPT, drain with deadline, MIGRATE), REPLAY
  dropped, epoch changes are re-genesis; refund rule; fn holds no checkpoints.
- §A: resolution A1 (id = cell id; `kind` split from a mutable schema digest); the `state` declaration
  follows the front end into Lean.
- §B: mechanism rewritten to the landed `Kernel/ObjectiveActivity` record and turns; `AnswerSlot` is its
  own module, not `ReactiveTerminalCell`; resolutions B1–B4 applied.
- §C: decision restated as amended by C1–C3; mechanism rewritten for ADOPT/MIGRATE with a drain deadline;
  REPLAY removed.
- §D: resolutions D1–D3 (keep refusal and measure; write-write aborts unless a declared delta; per-signer
  envelopes in multi-party pipelines).
- §E: resolution E1 (transition table with payload guards; old-slot `eqOld` on the source state, which
  also fixes revision 1's law sketch).
- §G: resolution G1 refund rule, with the landed fee pair and ticks-only tariff.
- §I: decision revised after FN-CHECK (bundled blocks, no checkpoints, five-field pin, contract doc).
- §3: T1 marked mostly landed with the landed theorem names; T1 moved from `Theory/` to `Kernel/`; the
  reference to the deleted `BendActivity.advance_actual_run` removed; T2 gains write-write and the
  measurement; T7 rewritten for the two-phase upgrade.
- §4, §5: dispositions paragraph and OPEN 3 carry the root's provisional answer.
- §6: lane statuses with commit ids; L0 added; warm-base commands updated to the hbox `mk-lane.sh` route.
- §7: review-dispute section added.

**Revision 3 (2026-10-05).** Merged the five reviews received by 11:00 EDT (BREAD, FRONTIER, HIST, LAWS,
OS) and applied the root's rulings on them.
- FN review (11:16): §I mechanism replaced (bundles sized by A and the poll page, posts through
  `hybrid-author`, fn's seven exit classes, six-field pin); new paragraph keeping transport outcomes out of
  answer slots, with QF-B; caps and keystone sentences corrected; the `scholar-fn` code fixes recorded;
  §G permanent-history fee for fn publications; L13 replaced by QUEST FN-DIRECT; OPEN 3 and 4 notes; §7
  list of unruled additions extended.
- Header and §1: the review process; object authority; resume with view and the outcome sum without
  `conflict`; `call` writes applied at frame return and billed to the caller; upgrade with draining
  closure, total MIGRATE, multi-turn migration and REBIRTH; four affordance states.
- §A: `ObjectRecord` gains `creators` and `keeper`; new paragraph on authority over an object (state-cell
  namespace, facet capability, law on every write, payer is not authority, `writeState` deleted).
- §B: the landed lost-reply and lost-update defect recorded; the merged FRONTIER `Conflict` payload
  replaced by the ruled resume-with-view mechanism (versioned `ObjectState`, `resumed {outcome, view}`,
  `keep | set | add` writes, version CAS, `blindWrite`); reason sums for refused and broken; exhaustion
  receipt; slots expired on abort; decider as a role; Scribe note B2 marked superseded.
- §C: decision amended by the ruling; drain closes the object unless the state type widens; REBIRTH and
  the `restartable` publish test; MIGRATE made total; floors checked at install; large objects migrate
  over several turns (replacing "cannot upgrade").
- §D: `call` applies writes at frame return; Daml authority with `creators`; send escrow, bounded queues
  and role deciders; pipeline `valid_until`; exact-plan consent; new Scribe note D4.
- §E: request slots that exist on main; redaction and joint action scope already exist; package pin as a
  law (artifact and method slots); laws judged by the Receiver; surface clause kinds; propositional
  history; seats with `atLeast` (fixing revision 2's zero-amount bug), `donate`, invitations and
  instance-only debits.
- §G: refusal and exhaustion charging; one tariff with a package verdict cell; deposits re-priced at each
  yield; disposal turns; saturation order (unruled).
- §H: `Possible` and simulated `Enabled`; card provenance, petnames, meta-card renderer; deciders shown.
- §3: T0 Agreement; T1 rewritten for resume with view; T2 (d); T3, T6, T7 extended; T9 every write
  judged.
- §4, §5: dispositions paragraph and every OPEN question carry the reviews and the root's
  recommendations.
- §6: order after the ruling; L1 acceptance additions; new lanes L1b RESUME-WITH-VIEW, L1c
  ACTIVITY-METERING-DISPOSAL and L4a (QUEST-LAWS-PIN, QUEST-LAWS-RECEIVER); L3 becomes OBJECT-RECORD; L7
  moves seats and grants ahead of `call`; MERGE-KEEPER noted.
- §7: two unruled review disputes and the list of unruled review additions.

**Revision 1 (2026-10-04).** First version from the root's decisions, read at main `6f82b818`.
