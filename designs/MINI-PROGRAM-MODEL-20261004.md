# Mini's program model (2026-10-04)

This document turns the root's decisions (`work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`) into
the design of Mini's program model. It changes no decision. Where a decision conflicts with the
evidence or with another decision, the decision stands and a **Scribe note** states the conflict for
the root and Ember to resolve. Mini facts were read at `emberian/minidregg` main `6f82b818`
(2026-10-04 04:31). Scholar reports are cited by short name and section: BREAD
(`SCHOLAR-BREAD-PROGRAM-MODEL`), META (`SCHOLAR-BREAD-METATHEORY`), LAWS (`SCHOLAR-LAWS-CONTRACTS`),
CALLS (`SCHOLAR-CALLS-CONCURRENCY`), OS (`SCHOLAR-OS-LINEAGE`), FRONTIER (`SCHOLAR-FRONTIER-AGORIC`),
HIST (`SCHOLAR-HISTORIAN-CAPABILITY-SYSTEMS`), FN (`SCHOLAR-FN-STORAGE-NODE`) and ROOT
(`ROOT-READING-NOTES-PROGRAM-MODEL`). Every primary source named here is in the cited scholar entry,
with its paperbin path.

---

## 1. The model in one page

**Objects.** An object is a cell with a stable id that is never its package hash. It holds declared
durable state (typed, first-order, versioned Core4 data, declared in mandatory `.obend` syntax), its
law, a package pin (interface type and package hash), an upgrade-policy capability fixed at creation
(frozen by default; it may only tighten), a continuity counter, and its activities. The law judges
the declared state and an upgrade transforms only the declared state.

**Activities.** An activity is a Core4 computation of type `Activity<P,R,A>` that yields a typed Plan
and waits. Mini keeps the exact whole-machine checkpoint (`Theory/ObjectiveBendCheckpoint`,
`state_roundTrip`). A checkpoint lives as long as its awaits, is pinned to the package hash that made
it, is storage-charged after collection at the yield, and is decoded and checked before the root
moves. It captures only immutable values, resources moved into it, and send-only references; it
never captures a mutable alias of object state or turn-scoped authority. A resume spends the await
id like a nullifier, bound to the checkpoint digest, and revalidates the read versions the activity
recorded. Every await carries a height deadline, escrows the fees of its resume and timeout turns,
and resolves to exactly one of `Reply | Refused | Unknown | TimedOut | Broken | Upgraded`.

**Calls.** There are three forms. `call` is synchronous and in-turn: the callee runs its pinned
package against the turn's snapshot and returns a value and a Plan fragment, depth-first, under
Daml's authority rules, and re-entry into an object already on the stack is refused. `send` is
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

**Upgrade.** An upgrade is one governed, all-or-nothing turn under a law-governed upgrade capability
visible on the object's card. It checks declared-state subtyping or a typed linear migration, re-judges
the law, decides frozen-floor entailment with a certificate, and checks interface compatibility. Every
live activity gets a disposition inside that turn (DRAIN by default, or ABORT; REPLAY only if replay
succeeds in the turn; never MAP) or the upgrade is refused.

**Metering.** Each invocation carries one signed envelope. A Lean cost theorem states that metering is
a function of pre-state and invocation and that the meter dominates machine transitions and kernel
work. Exhaustion parks the activity; it never terminates the object. Meters account; they do not
schedule. Every retention structure is a cell with a payer; unfunded objects hibernate to their
Merkle hash.

**Presentation.** Every object answers `describe`, `affordances` and `history`. An affordance is
`Hidden`, `Disabled(reason)` or `Enabled`, and its reason comes from the same law check admission
uses. Receipts carry causal edges; unhandled faults go to the object's keeper.

**fn.** fn is Mini's archive, feed and transport for exact bytes now. It moves under the hot per-turn
log only after fn's page representation and the `fn-store-1` freeze.

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
  id          : Kernel.Contracts.ObjectRef      -- stable; never derived from `pin.package`
  stateType   : Ty                              -- declared durable-state row, first-order
  stateVer    : Nat                             -- schema version, bumped by migration
  law         : Kernel.Contracts.LawRef         -- the law cell and its exact root
  pin         : PackagePin                      -- { interface : Ty, package : Digest }
  upgrade     : UpgradePolicy                   -- frozen | governed (law : LawRef) (floors : List Pred)
  continuity  : Nat                             -- bumped by every upgrade and law change
  activities  : List ActivityId                 -- each an ObjectiveActivity record (§B)
```

The declared state lives in ordinary cells of the store; the record holds its type, not its bytes.
The front end (`native/bend-source/objective-parser.ts`, `objective-elaborate.ts`) gains a `state`
declaration on `spec … for T`, and admission refuses a package that defines an object kind without
one. `UpgradePolicy` may move only from `governed` to a stricter `governed` or to `frozen`, and its
floors may only be added; the record's own law enforces that with a `writeOnce`-style clause on the
frozen flag and an entailment check on the floor list (§C). Durable state is first-order: the
`Ty.shareable` check already refuses `Ty.computation`, and the declaration additionally refuses arrows
and `Ty.custody`, so no closure, thunk or activity can enter durable state.

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

**Cost.** One record type, one front-end declaration form, and one admission check. Authors must
state what persists; Agoric's lesson that "if v1 fails to retain something, v2 cannot get access to it"
(HIST 1C) makes that a day-one obligation rather than a later migration.

**Rules out.** Objects whose identity changes with their code; durable state that contains closures;
upgrade authority held by an unnamed key; and the "heap / virtual / durable" zone taxonomy Agoric had
to retrofit (FRONTIER §1.6).

> **Scribe note A1 (identity).** `Kernel/Contracts/Identities.ObjectRef` has three fields, `native`,
> `domain` and `kind`, and documents `kind` as "the declared semantic kind (schema/kind digest)". If
> `kind` is the digest of the declared-state schema, then a migration that changes the schema changes
> the `ObjectRef`, and every reference to the object breaks at upgrade, contrary to "a stable id".
> Either `kind` must name the interface family (unchanged by migration), or `ObjectRef` must drop it
> and the record must carry the schema version.

### B. Activities and checkpoints

**Decision.** Keep the exact whole-machine Core4 checkpoint for in-flight activities. A checkpoint lives
as long as its awaits, is pinned to the package hash that made it, is storage-charged after collection
at the yield, and is decoded and type-checked before the root moves. At a yield it may capture only
immutable values, resources moved in and send-only references; never a mutable alias of object state;
turn-scoped authority (signer grants, fee meter, handlers) never enters a checkpoint or a cell. Resume
spends the await id like a nullifier, bound to the checkpoint digest, and revalidates the read versions
it recorded (stale: re-run and a typed `Conflict`). Every await resolves to `Reply | Refused | Unknown |
TimedOut | Broken | Upgraded`, carries a height deadline, and escrows the fees for its resume and
timeout turns.

**Mechanism.** The language half exists. `Theory/ObjectiveBendDemandMachine` yields with
`Control.yielded plan`; `resume response state` is defined only on a yielded state and keeps heap and
stack (`resume_keeps_heap_and_stack`); `typed_yield_quiescent` makes every yield a safe point;
`stack_activity_signature` and `typed_resume_preserved` type the response; `state_roundTrip` restores
every state. The kernel half does not exist ("No kernel delivers responses or persists an activity
yet", `docs/OBJECTIVE-BEND-EVENTS.md`; task `01a1056f-0066`). It is built as follows.

```lean
-- Kernel/ObjectiveActivity.lean (new; mine Kernel/ObjectiveActivity{Control,Input} from the
-- codex-private-lifecycle tree first, per task 01a1056f-0066)
structure ActivityRecord where
  owner       : Kernel.Contracts.ObjectRef
  pin         : Digest                       -- package hash that produced the checkpoint
  epoch       : CoreEpoch                    -- Core4 + codec epoch
  generation  : Nat                          -- consumed by each resume
  checkpoint  : Digest                       -- H(encodeState s), bytes in a payer-funded cell
  reads       : List DurableDataIntent.ReadGuard   -- versions the continuation depends on
  holds       : CList                        -- send-only refs and escrow accounts (kernel-side)
  await       : Option Await
  state       : Running | Yielded | AwaitsFunding | Done | Faulted | Aborted

structure Await where
  id        : AwaitId          -- H(owner, generation, checkpoint) : a StableNullifier
  sources   : List AwaitSource -- answerSlot s | inbox i | height h
  deadline  : Nat              -- accepted height (RevisionRef.height)
  escrow    : EscrowRef        -- Book account holding the resume/timeout fee and its envelope

inductive Outcome (R : Ty) where
  | reply (r : Data) | refused (residual : Explanation) | unknown
  | timedOut | broken (reason : BrokenReason) | upgraded (pkg : Digest)
```

A yielding turn commits, in one `Kernel/DurableDataIntent.DataIntent`, the Plan's writes, the new
checkpoint bytes, the `ActivityRecord` with `generation + 1`, the `Await`, and the escrow posting. In
`Kernel/Contracts/Cuts` terms the await is a `Reserve` (a retained `Obligation`) and the resume is an
`Install` that consumes it, so `install_rechecks_today` already states that a resume is judged under
the current law, not the law in force at the yield. A resume turn: (1) spends `await.id` as a
`StableNullifier`, the same mechanism as `Contracts.retry_cannot_reconsume_row`; (2) loads the
checkpoint bytes, checks `H(bytes) = record.checkpoint`, decodes them with `decodeState`; (3) checks
the outcome against the entry's declared `R` (`Data.conforms`); (4) compares every `ReadGuard` in
`record.reads` with the current root and, on any difference, delivers `Conflict` in place of the
outcome (Scribe note B2); (5) runs `resume` and `runBounded` (the `@[csimp]` fast machine, which
landed as `a2a8a203`) to the next yield or `done`; (6) commits. Deliveries and timeouts are not signed
by the activity's owner: they are obligation-driven turns that anyone may submit, paid from the escrow
and deduplicated by the nullifier. A deterministic failure in the resumed segment (blackhole, machine
refusal) commits a `Faulted` record and a fault message to the object's keeper; budget exhaustion
commits nothing and leaves the activity `Yielded` and marked `AwaitsFunding` (§G).

The capture rule is checked at the yield over the activity record, not the Core4 heap: `holds` may
contain only send-only references and escrow accounts the activity owns, and the turn-scoped grant
table and fee meter (§D, §G) are absent from `ActivityRecord` by type. Answer slots are kernel cells
built on `Kernel/ReactiveTerminalCell`, whose four terminal kinds (`finalized | cancelled | expired |
broken`) already race for one terminal cell with an outbox write in one `DataIntent`, with the
deadline checked against a clock read guard.

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

**Cost.** One record type, one answer-slot module over `ReactiveTerminalCell`, one resume receiver, and
the escrow postings. Each yield writes a checkpoint proportional to the live heap, which grows about 120
tokens per turn in `EventCounter.serve` until collection exists (task `01a1056f-00a4`). Because every
await has a deadline, a resident that serves forever pays one timeout turn per deadline period.

**Rules out.** Long-lived state held only in continuations; a second resume of one yield; client-supplied
checkpoints; awaits that can wait forever; and Bread's five unconnected async mechanisms (BREAD §0).

> **Scribe note B1 (capture rule versus Core4).** Core4's runtime values (`RuntimeValue`) include no
> capability, resource or mutable reference; `Ty.custody` is unused by any closed program; and the
> machine has no mutable cells other than thunk updates. A checkpoint therefore cannot hold authority,
> resources or an alias of object state at all, and the capture rule is satisfied by construction on
> the heap. What the rule actually constrains is the kernel-side activity record (`holds`), as above.
> When Core4 gains capability values, the rule must become a typing rule (a `capturable` predicate
> alongside `Ty.shareable`).

> **Scribe note B2 (`Conflict` is not in the outcome sum).** The decision delivers "a typed `Conflict`"
> when recorded reads are stale, but the outcome sum it fixes is `Reply | Refused | Unknown | TimedOut |
> Broken | Upgraded`. Either the sum gains `Conflict(stale cells, outcome)`, which keeps the resolved
> outcome deliverable, or staleness is a `Refused` reason. The first is needed if the reply must not be
> lost when the activity's earlier reads went stale.

> **Scribe note B3 ("type-checked before the root moves").** No executable checker for machine-state
> typing exists: `StateTyping` in `Theory/ObjectiveBendDemandTyping` is a `Prop`. For a checkpoint the
> kernel produced from a `Checked` program, typing holds by `typed_stepRaw_preserved` and
> `typed_resume_preserved`, so the runtime check reduces to `decodeState (encodeState s) = some s`
> against the stored bytes. An executable `checkState` is needed only for states that arrive from
> outside the kernel's own run, which decision C forbids (no MAP, no codec migration).

> **Scribe note B4 (collection at the yield does not exist).** The brief described the design as "full
> machine state, GC at yield, storage charged". The Core4 machine has no collector; its heap only grows.
> "Storage-charged after GC at the yield" depends on task `01a1056f-00a4` and on a theorem that
> collection preserves behaviour (§3, T5).

### C. Upgrade

**Decision.** One governed, all-or-nothing turn. Authority is a law-governed capability visible on the
object's card; there is no superuser. Checks: declared-state subtype, else a typed linear migration
`Old ⊸ New`; the law re-judged on migrated state; frozen floors entailed, decided as `unsat(new ∧
¬floor)` with a certificate; the new interface a supertype of every referenced facet. Activity
dispositions are decided inside the upgrade turn or the upgrade is refused: DRAIN (the default:
activities continue on their pinned old package until their awaits end), ABORT (resolves awaits to
`Upgraded`), and REPLAY only if replay succeeds within the upgrade turn. No MAP. A Core4 or codec epoch
change drains or aborts.

**Mechanism.** `Kernel/ObjectUpgrade.lean` (**new**) admits one Plan action:

```lean
structure Upgrade where
  object       : ObjectRef
  newPin       : PackagePin
  newStateType : Ty
  migration    : Option MigrationTerm     -- Core4 term : Old → New, typed linearly
  newLaw       : Pred
  dispositions : List (ActivityId × Disposition)   -- must cover record.activities exactly
inductive Disposition | drain | abort | replay
```

Admission checks, in order: the signer presents the upgrade capability and the object's upgrade law
admits the request; `record.stateType` is a row subtype of `newStateType` (no migration needed), or
`migration` checks as a linear function `Old ⊸ New` under `Theory/ObjectiveBendTyping` (linear is
enforced as at-most-once today, so the check must add exactly-once for this use); the migrated state is
judged by `newLaw` evaluated on the pair `(migrate s, migrate s)`, so state clauses must hold and
two-state clauses see no change; for each floor `f`, `Pred.Sat` decides `allL [newLaw, not f]` and must
return `.unsat` with a `SysCert` that `checkAll` accepts (`certificate_unsat`); the new interface type is
a supertype of the type of every facet referenced from another object's c-list; and `dispositions` covers
`record.activities` exactly. Then the turn writes the migrated state, the new pin, `continuity + 1`, and
one entry per activity: DRAIN leaves the activity record and its pin unchanged; ABORT resolves its await
to `Upgraded newPin` and frees its checkpoint; REPLAY re-executes the activity's retained `(Plan_i,
Response_i)` log on the new package inside this turn and refuses the whole upgrade if any yielded Plan
differs. Calls and sends to the object after the upgrade run the new package, as in Erlang's fully
qualified calls; drained activities keep the old one.

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

**Cost.** A subtype judgement on rows, a linear-migration check, an entailment call per floor, an
interface-compatibility check, and a replay executor for REPLAY. `Pred.Sat` returns `none` for laws
containing `witnessed`, `hashEq` or `ran`, and for DNFs past `dnfCap = 1024`; such floors make every
upgrade of that object refuse, so floors must stay inside the difference fragment (LAWS Part II §7).
Large objects whose migration exceeds one turn's envelope cannot upgrade.

**Rules out.** Bread's bare `SetProgram` swap (BREAD §1.5); lazy migration on first touch; upgrades that
discover replay failure after commit; host-level upgrade powers; and silent loss of in-flight work.

> **Scribe note C1 (DRAIN versus migrated state, and no drain bound).** A drained activity keeps its old
> package, and its future Plans are typed against the old Plan sum and the old declared-state schema.
> After a migration that changes the schema, those Plans name fields that no longer exist, so "sound
> because checkpoints hold no mutable state" covers the checkpoint but not the Plans the activity will
> yield. The decision also sets no bound on draining: a resident that loops (`EventCounter.serve`) never
> ends its awaits, so the old package runs forever. CALLS idea 8 and DFINITY's record ("drains can
> stall", CALLS H4) argued for a drain deadline height after which the activity is aborted with
> `Upgraded`. A resolution needs both a rule for drained Plans after a schema change (refuse them with
> `Refused(schema)`, or allow DRAIN only when the state type is unchanged) and a drain deadline.

> **Scribe note C2 (REPLAY needs a log Mini does not keep).** Mini stores the checkpoint, not the
> sequence of `(Plan_i, Response_i)` pairs. REPLAY requires each activity to retain its full interaction
> log from its start (or from its last upgrade) in a payer-funded cell, a retention structure decision G
> does not list. Its cost is the log's storage plus a replay inside one turn's envelope.

> **Scribe note C3 (frozen objects across a Core4 epoch).** A frozen object can never be re-pinned, yet
> its package runs only on the Core4 epoch it was compiled for. After a Core4 or codec epoch change, a
> frozen object can run only if the Host keeps the old evaluator forever. DRAIN across an epoch change
> likewise needs the Host to run two Core4 evaluators. The 10-04 decision that re-genesis is the default
> for every format question (SWARM-LEDGER 05:30, item 1) resolves both if a Core4 epoch change is always
> a re-genesis; the program model should say so.

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
states by typing a transaction body without `Remote`, FRONTIER 2.E E4). Each frame reads the turn's
snapshot; writes are deferred in fragments and applied in call order at the end. A frame whose read set
contains a cell that another frame's fragment writes aborts the turn (the Orleans context-union rule,
CALLS B3). Authority follows Daml (LAWS C13; ROOT): calling a method requires its controllers in the
current context; the callee's fragment is judged in the context of the callee's own signatories plus
those controllers, never the caller's ambient signers. A scoped grant is the one explicit, bounded
exception to non-transitivity: the invocation carries a grant table (`Kernel/ScopedGrant.lean`,
**new**), e.g. `Transfer(from := me, asset := A, ≤ 10)`, and any frame may spend the signer's authority
only by decrementing a matching grant, judged by an `le` atom. The grant table is turn-scoped and never
enters a cell or a checkpoint (§B).

**Mechanism: `send` and answer slots.** A `send` is a Plan action `send (target : CapIndex) (method :
Label) (args : Data) (reply : Option SlotName)`. It appends to the inbox cell keyed by (sender, target)
(`Kernel/Inbox.lean`, **new**; the inbox's FIFO discipline is its law: monotone head and tail, tail ≤
head, sender-authenticated, as Bread's `cap_inbox` had, BREAD §1.2). Its answer slot is a
`ReactiveTerminalCell` whose id is `H(InvocationId, action index)`, so every validator names it
identically (Ozone's integrity keys, CALLS A8). The decider role is linear: creating the slot gives it
to the delivery, the delivery gives it to the callee's turn, and resolving consumes it (Agoric's rule,
FRONTIER §1.2). A send whose target is an unresolved slot is queued in that slot's cell and forwarded
inside the resolving turn, so every resolution follows one path and needs no embargo (Cap'n Proto's
rule, CALLS A5). A slot whose decider faults or whose deadline passes resolves `broken` or `expired`,
and breakage propagates to queued sends. The outbox records of `Kernel/OutboxDelivery` carry everything
that leaves a domain, and nothing is released before the turn commits and, in a Simplex domain, is
final.

**Mechanism: pipelines.** A pipeline invocation is a restricted Core4 term (`Kernel/Pipeline.lean`,
**new**): a list of commands `call (cap | result i) method args` with results by index, no recursion and
no `fix`, so its cost is a function of its length. Admission re-executes it as one turn and every law
judges the composed Plan. A multi-party pipeline is a list of partially signed segments; each segment
is signed over (segment hash, position, pipeline hash), the composed turn is admitted only if every
segment's signature, grants and envelope check, and the Book's posting algebra balances the composed
Plan. That is in-domain multi-party atomicity with no two-phase commit.

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

**Cost.** A call stack with a re-entry guard and per-frame authority contexts; a grant table per turn;
inbox cells and answer slots, each paid (§G); a pipeline form; and segment signatures for multi-party
composition. A `PlanFragment` with more than one action needs recursive Plan data, which Core4 lacks
today (Plans and responses "must be non-recursive data", EVENTS; task `01a1056f-00a4`).

**Rules out.** Callbacks into an object already on the stack; callees spending a caller's authority
beyond what the caller signed; a third call order; and early delivery inside one domain.

> **Scribe note D1 (the re-entry statistic).** The decision cites "10 of ~100M Ethereum executions were
> legitimately reentrant". Grossman et al. (POPL 2018, §9, lines 1181–1182) report that "only 10
> executions out of about 100 million were legitimately non-ECF". An execution that re-enters an object
> but is equivalent to a callback-free one is ECF and is not counted. The mandatory guard refuses those
> too, and the paper (in the parts read) does not report how many executions contained callbacks at all.
> The evidence supports "non-ECF re-entry is almost never legitimate"; the cost of refusing ECF
> re-entry is unmeasured.

> **Scribe note D2 (write-write between frames).** The decision aborts a turn when a frame reads a
> version another frame wrote. It states no rule for two frames that write the same non-delta slot. The
> Orleans rule it cites aborts when the context union "has seen more than one version of any grain"
> (CALLS B3), which covers write-write if writes count as versions seen. The rule should say so.

> **Scribe note D3 (one envelope, several signers).** Decision G fixes "one signed envelope per
> invocation". A composed multi-party pipeline has several signers. The design above gives each segment
> its own envelope and charges the composed turn the sum; the decisions should confirm that a segment's
> excess refuses the whole turn and that no signer pays for another's segment.

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
-- request atoms are reserved slots, read like any slot and fail closed when absent:
--   "request/method", "request/invoker", "request/cap/<i>", "request/height"
-- (the convention already exists: Pred/Leaf's boardLaw reads "request/verb";
--  Pred/Core reads "request/target")
def necessity (A B C : Pred) : Pred := .any [.not A, .not B', C]  -- `from A to B onlyIf C`; B' is B on new
```

`leOld` needs no new decision machinery: `Pred/Satisfiable`'s `Node` already has `.old s` and `.new s`,
`monoT` already emits `⟨.old s, .new s, 0⟩`, so `leOld` is one more atom in `atomDnf`, and
`decide_never_unknown` and `certificate_unsat` extend by one case. History slots are compiled by a new
`Pred/History.lean` (**new**): a past-time formula (`since`, `once`, bounded counts over a height
window) becomes kernel-maintained slots updated by the kernel's own Plan postlude, after which the law
is an ordinary two-state `Pred` over (old history, new state); code cannot write those slots. Action
scope extends `Kernel/LawView` so that a law may read the post-state of any cell the same Plan writes,
named by its role in the Plan; the read joins the turn's footprint. Book balances enter laws through the
same view as total slots `book/<account>/<asset>`, initialised to 0 (FRONTIER §1.10 notes that `le` on
an absent slot is false, so `not le` on an absent slot is true; totality removes that trap).

**Mechanism: three points.** Every package method carries a guard, a `Pred` over arguments and request
slots, checked before the method runs; a refusal costs only the guard's evaluation. State laws run on
every write, as now. Proposals (offers, §seats) run on every reallocation of the seat. Clauses carry a
method index and a polarity (`permit | forbid`); the effective law of a write is `forbid` clauses
negated and conjoined with the disjunction of matching `permit` clauses, and no matching permit means
refusal. Refusals return `firstFailingLeaf`'s path plus the residual: the unsatisfied leaf with
request-slot values substituted, filtered by a redaction policy that names which leaves each viewer may
see (refusal text is an information channel, FRONTIER 2.B B1).

**Mechanism: seats.** `Kernel/Seat.lean` (**new**), built on `Theory/CanonicalResourceKernel` and
`Kernel/CanonicalEscrowMarket`:

```lean
structure Proposal where give want : List (AssetId × Nat); exit : onDemand | afterDeadline (h : Nat)
def offerSafe (seat : AccountId) (p : Proposal) : Pred :=
  .any [ .all (p.want.map fun (a, n) => .not (.le (bookSlot seat a) (n - 1))),
         .all (p.give.map fun (a, n) => .not (.le (bookSlot seat a) (n - 1))) ]
```

An `offer` Plan action creates the seat account, posts `give` into it from the offerer (so the initial
allocation equals `give` and satisfies the clause), and installs `offerSafe` as the seat account's law.
Every later posting that touches the seat is judged by it. `exit seat` is a kernel action whose
admissibility for the offerer is a clause the seat's law always contains and no contract clause can
forbid (forbid-overrides-permit is applied to contract clauses only); it posts the seat's whole
allocation to the offerer. Conservation is not a law: it is `Operation.apply_conserves`. Non-fungible
amounts need set-inclusion atoms; `memberOf` covers only bounded sets (FRONTIER §1.10, INFERRED there).

**Mechanism: protocol objects.** `Theory/ProtocolObject.lean` (**new**) ports Bread's `GlobalType`,
`LocalType`, `project` and the `dregg_choreo` notation (`Dregg2/Coordination.lean:68-239`, the part META
§1 marks PORT THE CODE), adds `mu` unfolding with a guardedness check, and compiles a guarded global type
at publish into a finite transition table over one state slot. The object's law is the disjunction, over
table rows `(q, role, label, q')`, of `all [eq "protocol/state" q, memberOf "request/invoker" role, eq
"request/method" label, eq "protocol/state'" q']` (Scribe note E1).

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

**Cost.** About four atom families, an action-scoped `LawView`, a history-slot compiler and its monitor
theorem, method guards in the package format, a seat module, a protocol-object module, an entailment
module, and a redaction policy. None needs a proof system in admission.

**Rules out.** Laws as closures (today `spec` laws are "callable closures stored in metadata; nothing
discharges them", `docs/OBJECTIVE-BEND.md`); input validation inside method bodies; caller protections
enforced by contract code; Bread's catalogue of 69 hand-named atoms (BREAD §2.2); and solver calls on the
admission path.

> **Scribe note E1 (protocol state cannot be a tree the law reads).** `Pred` evaluates difference
> constraints over `Int` slots; it cannot compute `GStep` over a global-type tree. "Its law admits
> exactly a legal next step" is realisable only by compiling the residual global type at publish into a
> finite transition table over a state slot, as above. That works for guarded recursive global types
> (they have finitely many residuals) and fails for protocols whose next step depends on payload values
> beyond finite sets. The residual global type is then the meaning of the state slot, not data the law
> reads.

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

**Cost.** A multiversion map, a scheduler, a refinement theorem, delta actions, a coordination ladder,
lease templates, deal cells and saga compensations. Bread had none of this running: it executed turns
serially under one lock (BREAD §1.4).

**Rules out.** Declared write locks as the scheduling unit; batch-dependent semantics (Aria, CALLS F4);
locks held across yields by default; and implicit two-phase commit across domains.

### G. Metering and storage

**Decision.** One signed envelope per invocation (decided 10-04); a Lean cost theorem: metering is a
function of pre-state and invocation, and meter ≥ machine transitions including kernel work (codec,
collection at the yield, law checks, Merkle updates). Exhaustion parks the activity and refunds the unused
remainder; it never terminates. Meters are accounting, not scheduling. Every retention structure (inbox,
await index, watcher table, recovery list) is a cell with a payer; storage is a deposit; unfunded objects
hibernate (evicted to their Merkle hash, restorable) and are never deleted; in-domain collection traces
cycles; termination is O(1) by detaching the subtree.

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

Admission refuses a turn whose cost exceeds its envelope, and `Kernel/AdmissionPrologue` charges the
refusal before the body runs. For an activity, a refused resume commits nothing: the await is unspent,
the checkpoint unchanged, and the record shows `AwaitsFunding`; anyone may top up the await's escrow and
resubmit the delivery. That is "parks". Storage deposits reuse `Kernel/QuotaGcSettlement`, which already
admits lease-backed insertion, quota checks and reachability-safe compaction as settlements. Every inbox,
answer slot, await escrow, history slot and checkpoint cell names its payer. Hibernation replaces an
unfunded object's subtree with its root; restoration is a turn that presents the preimage and a deposit.
Object collection traces the in-domain capability graph, which is all kernel-held, and termination
detaches an object's subtree root under a termination capability minted at creation.

**Why.** Agoric leaves deserialisation and post-crank collection unmetered on purpose, because XS
collection timing differs after snapshot reload and metering it would fork consensus; Mini's collection
runs inside the Lean semantics, so it can be metered (FRONTIER §1.4). Broken Metre found EVM gas
uncorrelated with CPU time, with programs over 100× slower per unit of gas than typical ones (OS §5).
KeyKOS "never built a scheduler using the meters", EROS found meter trees "inconsistent with … real-time",
and Coyotos was "abandoning meters entirely" (HIST 1F). Agoric's terminate-on-exhaustion forced it to
invent suspension (#8955). An unpaid safety feature, ERTP recovery sets, held about 60% of Agoric's
key-value entries (#8400), and a 310 MB cross-vat cycle was uncollectable (#8401) (FRONTIER §1.5).
Ethereum's rent stalled, Solana replaced rent with deposits, and ICP deletes frozen canisters (OS §4, §5).

**Cost.** A cost semantics and two theorems; kernel-work pricing per input size; payer fields on every
retention cell; hibernation and restoration; a tracing collector over the capability graph.

**Rules out.** Terminating objects for lack of funds; meters as a scheduling instrument; unpriced kernel
work; and storage nobody pays for.

> **Scribe note G1 (refunds).** The 10-04 charge law reads "refuse on excess; never refund" (SWARM-LEDGER
> 05:30, item 3). Decision G says exhaustion "refunds the unused remainder", D says broken slots
> "propagate and refund", and B escrows the fees of both the resume turn and the timeout turn of an
> await, only one of which ever runs. These cannot all hold. Two consistent readings exist: (a) the
> charge law forbids refunds of an invocation's own envelope, while escrows (await fees, send postage) are
> deposits returned when their obligation ends without running; or (b) an await escrows one fee that
> whichever terminal turn runs consumes, and nothing is refunded. Bread's conditional turns refunded the
> deposit on resolution and burned it on timeout (BREAD §1.2), which is a third rule. Parking itself is
> consistent with "refuse on excess": a refused resume leaves the activity at its yield.

### H. Presentation and debugging

**Decision.** Every object answers `describe`, `affordances` and `history`; an affordance is `Hidden`,
`Disabled(reason)` or `Enabled`, the reason computed by the same law check admission uses; projection code
is effect-free. Causal edges on every receipt; unhandled faults route to the object's keeper.

**Mechanism.** A new `Host/ObjectProjection.lean` (**new**) computes, for a viewer with a capability set:
`describe` = the declared-state fields the viewer may observe (the `Observe` cut of
`Kernel/Contracts/Cuts`), the pin, the upgrade policy and who holds each governing capability;
`affordances` = for each method, `Hidden` if no capability the viewer holds can reach it, else the guard
and the law evaluated by `Pred.Sat` with the viewer's request slots fixed: `.witness` gives `Enabled`
with an example argument, `.unsat` gives `Disabled(residual)` after redaction; `history` = receipts
touching the object with their causal edges (the invocation, the answer slot or inbox delivery that
caused it). Projection functions are typed without `Ty.computation`, so they cannot yield. Faults (§B)
are sends to the keeper capability the object names at creation.

**Why.** Bread's affordances were live only if caps covered them and the live state admitted them, and
its surface judged `(s, s)` while its executor judged `(s, s')`, which META §9.1 identifies as the reason
preview and commit types must differ (BREAD §2.1 #10). Naked Objects and Apache Causeway are the prior art
for a card as an authorized view plus behaviour (OS §6.C). Agoric's governance design goal is legibility:
"observers … are able to see who has control" (FRONTIER §1.14). Causeway's causal view was the one
debugger the E community shipped, and Tribble's keeper model routed faults to an object's keeper (HIST
1G).

**Cost.** One projection module, a satisfiability call per affordance per render, and causal fields on
receipts.

**Rules out.** Cards that can show an affordance admission would refuse; projection code that writes; and
upgrade or termination powers invisible to the viewer.

### I. fn

**Decision.** fn is Mini's archive, feed and transport for exact bytes now (finalized blocks, receipts,
checkpoints at cadence, deal messages, replay kits); it sits under the hot per-turn log later, gated on
fn's page representation and the `fn-store-1` freeze. The contract follows the fn session's check of the
SCHOLAR-FN claims (FN-CHECK).

**Mechanism.** Mini writes one signed article per finalized block, with Message-ID `H(domain, semantics,
height, blockHash)`; its body is Mini canonical bytes, opaque to fn (FN §4.1 B1). Deal messages and
replies travel as articles between domains (B2, which E1/E2 already exercise). Mini maps fn outcomes to
the outcome sum of §B: accepted and already-stored to `Reply`, conflict and refused to `Refused`, budget
refusal to `AwaitsFunding`, uncertain and node-stopped to `Unknown`, resolved only by an authoritative
lookup (FN §4.4). Mini pins (fn image digest, store history-id, format word) and keeps its SQLite hot log
and head anchor (FN §4.5; MI-01, MI-04).

**Why.** fn is an append-only, signed-exact-bytes log and feed with accepted, refused and uncertain kept
distinct and idempotent resend, which is what an archive and a transport need (FN §0). Its per-record heap
(about 3.6 KB), its open time (16–22 s at 40k records), a live cap of 32,768 transactions and 36 posts/s on
hbox's ZFS rule out one record per turn before the D41 page representation lands (FN §3.2). Its durability
theorem for the current format is not certified at current source (FN §0).

**Cost.** One article profile, an outcome mapping, and pins. **Rules out.** fn as the only copy of
anything Mini needs before `fn-store-1`, and Mini decisions that depend on fn's local numbering or arrival
order.

---

## 3. The theorems Mini should state

Each theorem below names its premises, an inhabitant that makes the premises true of a built object, and
a tooth: a mutation of the implementation that must turn the theorem's test red. No theorem is admitted
whose premise is uninhabited, and none may be stated over a model the kernel does not run; the Bread
record of apexes over empty premises (META "A warning that governs every section") is the reason.

**T1. Resume contract** (`Theory/ObjectiveResumeContract.lean`, over `Kernel/ObjectiveActivity`).
*Statements.* (a) `resume_consumes_once`: if a delivery `d` for await `w` is installed from state `s` to
`s'`, every delivery for `w` from `s'` is refused with `alreadyResumed`, and a retry of `d`'s
`InvocationId` is an exact replay (Khan's CO-c and CO-e). (b) `resume_binds_checkpoint`: an installed
resume's machine state equals `resume r (decodeState bytes)` where `H(bytes)` is the record's checkpoint
digest; no state parameter is accepted (the shape of `BendActivity.advance_actual_run`). (c)
`resume_typed`: the delivered outcome conforms to the entry's declared `R`, so `typed_resume_preserved`
applies. (d) `resume_rechecks_today`: the resume is judged under the current law (an instance of
`Contracts.install_rechecks_today`). (e) `stale_reads_conflict`: if a recorded `ReadGuard` differs from the
current root, the activity receives `Conflict`, never the bare outcome. (f) `slot_single_decider` and
`resolution_grants_nothing`: an answer slot is resolved by at most one turn, by the holder of its decider
role, and resolving it adds no capability to any c-list beyond the resolved value's own references.
*Premises.* A checked program (`Checked source []`), an admitted yield, and the kernel's install relation.
*Inhabitant.* `EventCounter.serve` run natively for three resumes. *Teeth.* Removing the nullifier spend
makes a second delivery install; replacing the digest check with "trust the submitted bytes" lets a forged
checkpoint install; dropping read revalidation lets a stale resume deliver `Reply`. Bread's
`commit_resumes_once` shows what to avoid: its handler premise `resumeWith : (Reply : Type u) → Reply` is
uninhabited (ROOT correction).

**T2. Re-entry guard soundness** (`Kernel/CallFrame.lean`). *Statements.* (a) `admitted_turn_reentry_free`:
in every admitted turn, no object occurs twice on any call stack the real `callStep` builds. (b)
`frame_conflict_refused`: no admitted turn contains a frame whose read set intersects a later-applied
fragment's write set. (c) SeRIF's semantic form (FRONTIER 2.F F1): for every per-object invariant `I`
expressed as a law, if every callback-free execution preserves `I` then every admitted execution does.
*Premises.* The real call-stack executor; no premise about programs. *Inhabitant.* An A→B→C call chain
that admits. *Teeth.* An A→B→A chain is refused; a DAO-shaped example (a withdraw whose callee calls back
and withdraws again with a stale balance read, every write individually law-valid) commits when the guard
is removed and is refused with it. Statement (c) alone would be close to a tautology given (a); its
content is (a) and (b) over the executor admission actually runs, and the DAO tooth shows the guard is
load-bearing.

**T3. Offer safety for seats** (`Kernel/Seat.lean`). *Statements.* (a) `seat_offer_safe_forever`: from the
`offer` that creates a seat, in every state reachable by admitted turns while the seat is open, the seat's
Book balances satisfy `offerSafe p`. (b) `exit_enabled`: in every such state, the offerer's `exit` is
admissible given its envelope, and it posts exactly the seat's allocation to the offerer. (c)
`seat_conserves`: every admitted posting touching a seat conserves per-asset totals (from
`Operation.apply_conserves`). Payout liveness is (b) plus a justness assumption on inclusion of submitted
turns (van Glabbeek; LAWS H2), stated as a hypothesis on the schedule, never on the seat. *Premises.*
Initial allocation = `give` (the `offer` action establishes it); seat slots total. *Inhabitant.* A
two-party swap seat that settles, and one that exits. *Teeth.* A reallocation that leaves less than
`want` and less than `give` is refused; a contract clause that forbids `exit` does not stop it; making a
seat slot absent instead of 0 flips the verdict of `not le` and must be caught by a totality check.

**T4. Parallel admission equals the sequential fold** (`Kernel/ParallelAdmission.lean`).
*Statement.* `parallel_eq_fold`: for every pre-state and batch, the parallel run's receipts, refusals and
root equal `batch.foldl admitOne s`. *Premises.* `admitOne` is deterministic (re-execution is), and the
multiversion map returns, for every read, the latest earlier write in log order. *Inhabitant.* Two
batches: one with disjoint footprints and one where invocation 2 reads a cell invocation 1 writes.
*Teeth.* Skipping validation produces a different root on the conflicting batch; treating a delta as a
read changes nothing in results but must show in the published DAG.

**T5. Collection at the yield preserves behaviour** (`Theory/ObjectiveBendDemandCollect.lean`, **new**,
with task `01a1056f-00a4`). *Statement.* `collect_bisim`: for a yielded state `s`, `collect s` is
yielded, `state_roundTrip` holds for it, and for every closed response `r` of type `R`, running `resume r s`
and `resume r (collect s)` produce outcomes equal up to heap-address renaming, with the same Plans.
*Premises.* A typed yield (`typed_yield_quiescent`). *Inhabitant.* `EventCounter.serve` after ten turns.
*Teeth.* A collector that frees a cell still reachable from the stack changes the next Plan.

**T6. Cost semantics** (`Theory/ObjectiveBendCost.lean`). *Statements.* (a) `cost_function`: cost is a
function of (pre-state, invocation). (b) `meter_dominates`: machine transitions plus kernel steps (codec
tokens, collection work, law constraints evaluated, Merkle nodes rewritten, cells forced) are at most the
cost. (c) `envelope_sound`: an admitted turn's cost is at most its signed envelope, and its charge equals
the envelope. *Premises.* The tariff is a public function of the cost terms. *Inhabitant.* The
`EventCounter` turn and a seat reallocation. *Teeth.* A turn with few ticks and a large checkpoint or a
large law: dropping the codec or law term from `cost` breaks (b) on it.

**T7. Upgrade gate soundness** (`Kernel/ObjectUpgrade.lean`). *Statements.* (a)
`upgrade_preserves_floors`: if an upgrade is admitted, every step `(old, new)` the new law admits also
satisfies every frozen floor (from the `SysCert` and `certificate_unsat`). (b) `upgrade_state_conforms`:
the migrated state conforms to the new declared type and satisfies the new law. (c)
`upgrade_dispositions_total`: the committed upgrade assigns exactly one disposition to every live activity.
(d) `replay_admitted_only_if_equal`: a REPLAY disposition commits only if every replayed Plan equals the
logged Plan. (e) `upgrade_refusal_inert`: a refused upgrade changes no cell. *Premises.* Floors inside the
difference fragment; a typed migration term. *Inhabitant.* An upgrade that adds a field with a default
and one that renames a field. *Teeth.* An upgrade that weakens a floor is refused with a certificate; an
upgrade that omits an activity's disposition is refused; Bread's `migrate_conforms` false premise (field
add does not conform to the new schema, META §7.1) must reappear as a refusal, not a theorem.

**T8. Choreography step soundness** (`Theory/ProtocolObject.lean`). *Statements.* (a)
`protocol_step_sound`: an admitted turn on a protocol object moves its state from `q` to `q'` only if `q'`
is the residual of a `GStep` of the global type denoted by `q`, by the role bound to the signer, on the
invoked label. (b) `protocol_progress`: for a guarded global type whose residual is not `done`, the law is
satisfiable: `Pred.Sat` returns a witness for some role's step. *Premises.* A guarded global type compiled
by the module's own compiler. *Inhabitant.* A three-party escrow protocol run to `done`. *Teeth.* An
out-of-order step is refused; Bread's two refutations (`deadlock_initial_counterexample`,
`privacy_var_counterexample`) are kept as regression theorems so the false statements cannot return.

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
Decision C follows HIST: DRAIN and ABORT, REPLAY only if it succeeds within the upgrade turn, no MAP.

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

**1. "Synchronous cross-principal `call` (D1) at all, versus Agoric's 'never synchronous across trust
boundaries'. Root's lean: yes, with Daml authority + scoped grants + mandatory re-entry refusal."**
*For.* One Mini Host gives synchronous atomicity for free, and without `call` every cross-object
interaction costs a signed, paid turn per hop, which is the "sad, singleton-ish" interface Cap'n Proto
warns of (CALLS A5). Mina and Daml run synchronous value-returning call trees in production, and Daml's
non-transitive authority plus Pact's grants bound what a callee can do with the caller's power.
*Against.* SES documents that synchronous cross-principal interaction is where re-entrancy lives, and
Agoric chose a clean stack through promises (FRONTIER §1.7). A law-valid write derived from a stale read
passes every per-write law (the DAO shape, FRONTIER 2.F F1), so `call`'s safety rests entirely on the
guard and the frame-conflict rule being right.

**2. "Laws: generate from `.obend` now, unify later (root's lean), or unify now."**
*For generating now.* Cedar keeps a separate, deliberately limited language because analysability is the
point (LAWS D1), and Mini's `Pred` already has satisfiability, certificates and refusal explanations that a
general fragment of Objective Bend would have to re-earn. Refinement types show how `requires` and
invariants on signatures become clauses (LAWS E7). *For unifying now.* Two languages for one object are
two shapes that agree today and may disagree later, which the repo's doctrine names as a defect class; and
today's `spec` laws and `requires` strings already show the author's laws drifting away from the kernel's
(`docs/OBJECTIVE-BEND.md`: "nothing discharges them").

**3. "REPLAY as an upgrade disposition at all, or DRAIN/ABORT only."**
*For REPLAY.* Mini's checker is exact: the Plans an activity yields are first-order data, so equality of
replayed Plans is decidable inside the upgrade turn, which is the fix Agoric's #12315 asks for (FRONTIER
§1.12). It lets a bug-fix upgrade keep long-running activities instead of aborting them. *For DRAIN/ABORT
only.* REPLAY needs every activity's full `(Plan, Response)` log retained and paid for (Scribe note C2),
and its replay must fit one turn's envelope. Agoric's replay machinery was where its 2025 chain halt and
its 2026 "wishful thinking" issue sit (HIST D2).

**4. "Order of building: answer slots and the resume contract first, then `call`, pipelines, seats,
protocol objects; cross-domain pipelining last."**
*For this order.* Every other feature needs a durable, once-only resume: sends need answer slots, seats
across a yield need parked activities, and deal cells need deadlines. Agoric added durable promises after
the fact and paid for it in three layers (FRONTIER §1.12). *For `call` first.* `call` is in-turn and needs
no answer slots, so it could land earlier and make residents useful sooner; and `call` with multi-action
fragments, like pipelines, is blocked on recursive Plan data either way (task `01a1056f-00a4`).

---

## 6. Build plan

Lanes in dependency order. "Warm base" means the lane changes `Kernel/`, `Host/` or modules the default
build imports and must build against the warm Lean base on the build box
(`scripts/dregg-clean-build <target> --sha HEAD --host hbox`); "plain lean" means its modules compile
with plain `lean` into lane oleans, as the S11 and PROOF-ENG lanes did. Two existing lanes are
prerequisites: RECEIVER-COLLAPSE (`Theory/Receiving`, `Kernel/Receiving`, held for the warm base) and the
first native Objective accepted receipt (`Kernel/ObjectiveBendNativeAdmission`, assembled in lanes; task
NATIVE-ACCEPTED `01a105bb-e2a2`).

**L1. Activity record, answer slots and the resume contract.** Modules: mine
`Kernel/ObjectiveActivity{Control,Input}` and `Compiler/ObjectiveActivity{Computation,GuardedComputation}`
from the codex-private-lifecycle tree (task `01a1056f-0066`); new `Kernel/ObjectiveActivity`,
`Kernel/AnswerSlot` (over `Kernel/ReactiveTerminalCell`), `Theory/ObjectiveResumeContract`. Acceptance:
`EventCounter.serve` and `TimerResident` reach native accepted receipts for three resumes each; T1 pinned
with `#assert_axioms`; the three T1 teeth fail as stated. Unblocks every later lane. Warm base.

**L2. Collection at the yield and recursive Plan data.** Modules: new
`Theory/ObjectiveBendDemandCollect`; `Theory/ObjectiveBendDemandData` and the checkpoint codec extended
for recursive first-order data (task `01a1056f-00a4`); the guardedness check (task `01a1056f-0083`).
Acceptance: T5 pinned; `EventCounter.serve`'s checkpoint size is constant across turns; a Plan carrying a
list of actions round-trips. Unblocks L4 (multi-action fragments), L5 and storage charging. Plain lean.

**L3. Objects and declared state.** Modules: new `Kernel/ObjectRecord`; the `state` declaration in
`objective-parser.ts` and `objective-elaborate.ts`; the `ObjectRef.kind` change of Scribe note A1 in
`Kernel/Contracts/Identities`. Acceptance: a package without a state declaration is refused by name; an
object's id survives a re-pin. Unblocks L4, L7, L9. Warm base.

**L4. Law language and publish-time checks.** Modules: `Pred/Core` (`leOld`), `Pred/Satisfiable` and
`Pred/SatisfiableTotal` (the new atom case), `Pred/Leaf` (residuals), new `Pred/Entailment`,
`Pred/History`, method guards and polarity in the package format, `Kernel/LawView` (action scope, Book
slots), the redaction policy. Acceptance: `decide_never_unknown` and `certificate_unsat` re-proved with
`leOld`; a necessity law ("balance decreases only if the invocation presents the owner capability") is
admitted and refuses a forged withdrawal; an always-false clause is reported at publish. Unblocks L5, L7,
L8, L9. `Pred` is plain lean; `LawView` needs the warm base.

**L5. `call`, scoped grants and the output gate.** Modules: new `Kernel/CallFrame`, `Kernel/ScopedGrant`;
`Kernel/OutboxDelivery` wired as the only egress. Acceptance: T2 pinned with its DAO tooth; a callee that
tries to spend beyond a grant is refused naming the grant. Unblocks L6. Warm base.

**L6. `send`, inboxes and pipelines.** Modules: new `Kernel/Inbox`, `Kernel/Pipeline`; answer-slot
forwarding in `Kernel/AnswerSlot`. Acceptance: a send to an unresolved slot is forwarded in the
resolving turn; a three-command pipeline admits atomically and refuses atomically; a two-party
partially signed pipeline settles a swap without escrow. Unblocks L7. Warm base.

**L7. Seats.** Modules: new `Kernel/Seat` over `Theory/CanonicalResourceKernel` and
`Kernel/CanonicalEscrowMarket`. Acceptance: T3 pinned with its teeth. Unblocks L11. Warm base.

**L8. Protocol objects.** Modules: new `Theory/ProtocolObject` (port of Bread's `Coordination.lean`
types, `project` and `dregg_choreo`, with `mu` and guardedness), its law compiler. Acceptance: T8 pinned;
a three-party escrow choreography runs natively. Plain lean for the theory; warm base for its kernel law.

**L9. Parallel admission and the coordination ladder.** Modules: new `Kernel/ParallelAdmission`;
`Pred/CoordinationDial` extended with the escrow rung and conflict tokens; delta actions. Acceptance: T4
pinned; a measured speedup on a disjoint batch; the published DAG replays to the same root on one thread.
Warm base.

**L10. Upgrade.** Modules: new `Kernel/ObjectUpgrade`; exactly-once linear checking for migration terms in
`Theory/ObjectiveBendTyping`. Acceptance: T7 pinned with its teeth; DRAIN and ABORT exercised on a live
resident. REPLAY waits for Ember's answer to question 3 and for Scribe note C2. Depends on L1, L3, L4.
Warm base.

**L11. Metering and storage.** Modules: new `Theory/ObjectiveBendCost`; payer fields on every retention
cell; hibernation and restoration over `Kernel/QuotaGcSettlement`; capability-graph collection.
Acceptance: T6 pinned with its tooth; an unfunded object hibernates and restores to the same root.
Depends on Scribe note G1 being resolved. Warm base.

**L12. Presentation.** Modules: new `Host/ObjectProjection`. Acceptance: for every affordance a card shows
as `Enabled`, the matching invocation admits; for every `Disabled(reason)`, it refuses with that reason.
Warm base.

**L13. fn archive and transport.** After FN-CHECK. Modules: the article profile and outcome mapping in the
existing `Kernel/Fn*` family. Acceptance: one finalized block per article, fetched back by Message-ID and
verified by Mini. Warm base.

**L14. Cross-domain.** Deal cells, sagas with compensating Plans and a weak-atomicity theorem, and promise
pipelining proper with handoff, in that order, after L1, L6 and L10 (the upgrade semantics of answer
slots). Warm base.
