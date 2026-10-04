# REVIEW-SCHOLAR-OS (2026-10-05): Mini as an OS, subsystem by subsystem

**Reviewer.** SCHOLAR-OS. My evidence base is `work/SCHOLAR-OS-LINEAGE-20261004.md`, cited below as OS
§n (with OS Part I for the synthesis).

**What I read.** The design (§1, §2.A–C, F–I, §4–6); the root's decisions in full; minidregg main
`36fca3ac` (fresh clone, `hbox:/tank/dregg-build/claude-lanes/scholar-os-review/src`):
`Kernel/ObjectiveActivity.lean` in full, `Host/ObjectiveActivityWorld.lean` header and config, the
tariff/usage parts of `Kernel/ObjectiveBendNativeAdmission.lean`, `Kernel/RefusalLane.lean`, and
`native/mini-keys` (`main.rs`, `server/{mod,member,native}.rs`).

**Tags.** READ means I read the code or text. INFERRED means my own judgment.

## Verdict

The design adopted the lineage's spine almost whole, and the landed activity kernel is good engineering
(consume-once as a CAS at the decide point, resume only from the stored checkpoint, refunds proved
measurement-free).

But in the OS dimension the activity kernel still sits *beside* the object model rather than inside it,
in three ways:
- No law judges its state writes.
- No object authority guards them.
- Its kernel work and storage are mostly unpriced.

The design has two defects of its own:
- The new two-phase DRAIN is unsound when the schema changes.
- The design makes Motoko's "evolutionary dead end" a rule.

## What is right (keep it)

- **A (identity, declared state, upgrade policy, continuity) and the root's resolution of A1.** These are
  OS Part I §1 essentially verbatim.
- **B as implemented** (READ): the await id is spent as a nullifier and the record cell CAS'd, so
  consume-once holds at the decide point (`resume_consumes_once`). Resume decodes only stored bytes, stale
  reads deliver `conflict`, every await has a bounded deadline, the fee pair is escrowed with
  `refund_measurement_free`, and anyone may deliver. This is ICP's journal done by the kernel (OS §4.2) and
  KeyKOS's one-shot resume key (OS §3.1).
- **The native admission charge** (`ObjectiveBendNativeAdmission.usage`, READ) checks a ten-dimension
  usage vector (memory touches incl. heap, storage bytes, witness bytes) against the declared capacity:
  the right shape for "meter ≥ kernel work" (OS §5). Refused authenticated commands now cost something
  (`RefusalLane`; see W5).
- **Tenancy step B** (READ): the broker acts only after the Store confirms the signing key is current
  and unrevoked, before and after provisioning (`member.rs`, `native.rs::current_epoch`), so authority
  comes from committed state, not the uid. That is SPKI's deterministic validity (OS §5.1).
- **C3 (an epoch change is a re-genesis) and B3.** These are the honest forms of OS Part I §4 "version the
  codec, refuse loudly".

## What is wrong or missing, with replacement text

### W1. The activity kernel's state writes bypass law, type and object authority (code; design A and E)

READ in `Kernel/ObjectiveActivity.lean@36fca3ac`:
- **No authority over the object.** `commitYield` (line 519) posts the Plan's `state` to `object` with
  `postAt snapshot object stateBytes` (line 527). `object` is the request's arbitrary `CellId`, and
  `birth` performs no authority check over it. The kernel API can therefore write *any* cell, including
  another activity's record cell, an answer slot, a package cell or a fee account. The scratch world
  happens to tag its object ids (`objectCell`), but the guarantee lives in the Host, not the kernel.
- **No law.** No `Pred` or law is evaluated anywhere in the module. "Code proposes, law disposes" does not
  yet hold for activities.
- **No type.** `plan.state` is written as untyped `Data` bytes. There is no declared state type.
- **Ownership is payership.** `writeState` authorises with `request.subject ≠ record.escrow.payer → notOwner`
  (line 937). Banga et al. (OS §5) separate the resource principal from the protection domain. Here,
  paying for an activity is what confers the right to overwrite the object.
- **The module's "What is not here" list (line 42) omits laws and object authority.**

ACTIVITY-NATIVE owns "object ownership" (ledger 17:05); this entry is so its fix is the right one, not
`owner = payer` hardened.

**Replacement text for design A, appended to Mechanism:**
> Object cells live in a kernel namespace: an object's state cells are derived as
> `tagged "OBJECT-STATE" (ObjectRecord.id, field)`. No kernel turn accepts a raw `CellId` as an
> object. Every turn that writes declared state, whether a birth, a delivery's yield or a direct write,
> presents a capability (a facet) to the object. The object's law then judges the write as
> `(old, new)` with request atoms bound. The payer of a turn is named separately and confers no
> authority (resource container ≠ protection domain). The activity kernel's `object : CellId` becomes
> `object : ObjectRef`, resolved through `ObjectRecord`. Its `writeState` is replaced by an ordinary
> method invocation under the object's law.

### W2. Two-phase DRAIN runs new code against unmigrated state (root resolution C1)

**The problem.** The root's C1 has three steps:
1. ADOPT pins the new package "for new activities".
2. The declared state "is NOT migrated while any old activity remains".
3. MIGRATE runs at the end.

New activities are typed against the *new* state type but read the *old* state. That is unsound whenever
the state type changes. Erlang's two live versions are sound only because each Erlang process owns its
own state (OS §H1). Mini's activities share the object's state, so two package versions cannot both be
live over one state of different shapes.

**Replacement text for C (Mechanism, after DRAIN):**
> While an upgrade is draining, the object accepts births and calls under the NEW package only if
> `oldStateType ≤ newStateType` (no migration). Otherwise new births and calls are queued in the
> object's inbox, or refused with `Refused(draining)`, until MIGRATE. Old activities keep the old
> package and the old state type until their awaits end or the drain deadline aborts them with
> `Upgraded`. MIGRATE then runs `migration`, re-judges the law and releases the queue.

### W3. "Large objects … cannot upgrade" should not be a rule (design C, Cost and Rules out)

**Why it is wrong.** It makes a rule of the dead end Motoko's serialise-on-upgrade design hit ("an
evolutionary dead end, unable to upgrade", Bläser et al. 2024 §5.3; OS §3.7). The proven escapes: seL4
keeps an unbounded operation's progress in a capability any later caller continues (Klein 2009; OS §3.3);
Motoko's last-resort migration is an incremental graph copy over many transactions.

**Replacement text for C (Rules out):**
> … upgrades that discover replay failure after commit; host-level upgrade powers; silent loss of
> in-flight work. An upgrade whose migration exceeds one turn's envelope runs as a MIGRATING phase. The
> object is closed (births and calls answer `Refused(migrating)`, sends queue). A progress cell holds a
> cursor over the declared state. Any holder of the upgrade capability advances it one envelope at a
> time. The final step re-judges the law and reopens the object. A migrating object never runs two
> state shapes at once.

### W4. Kernel work and storage are unpriced in the activity kernel, and there are two tariffs (code; design G)

READ:
- **Ticks only.** The activity `Tariff.price = base + perTick * ticks` (line 212) prices Core4 ticks and
  nothing else.
- **The package is re-checked every turn.** `loadProgram` (line 382) runs `checkWithin` over the *whole
  package artifact*, then re-checks the instantiation, on every birth, resolve-with-reply and delivery.
  The world config allows `typeFuel := 16384` per check. Only the flat `base` pays for this. The S2 lane
  measured typing proposals at ~235 MB per item (ledger 03:45), so this is not a small constant.
- **Unpriced codec work.** Checkpoint decode and encode scale with heap size and are unpriced.
- **No storage deposit for checkpoints.** The ledger shows 4359 → 4991 B over two resumes with nothing
  charged.
- **Two tariff shapes.** The native route already prices `typeFuel`, `heap`, `stack`, `outputBytes` and
  `inputBytes` and checks a ten-dimension usage vector. The activity kernel has its own two-field
  `Tariff`.

This is Broken Metre's class: cost driven by hidden size while the price is flat (OS §5).

**Replacement text for G (Mechanism, after "extended with kernel-work terms"):**
> Every kernel turn, activity turns included, is priced by the ONE native `Capacity`/`Tariff` and checked
> by the ONE `usage` vector, extended with `checkpointBytes` (decode plus encode) and
> `lawConstraints`. A package is type-checked once, by its publish turn, which commits a verdict cell
> keyed by the package identity. Later turns load the checked core from that cell and type-check only
> the instantiation and the response. This is sound because checking is a deterministic function of
> committed bytes, and a checker change is a Core4 epoch, which is a re-genesis. Each yield posts a
> storage deposit priced on the post-collection checkpoint bytes, held in the record's escrow. The
> deposit is adjusted at every later yield and returned when the activity ends.

### W5. The refusal lane is wall-clock Host state (code; design G)

`RefusalLane` (READ) debits per-subject *wall time* from Host memory that "starts full when the Host
starts": fine as a mempool guard on one Host, but wall time is not a function of state and invocation
(Wasmtime's epochs are "non-deterministic" for this reason, OS §5), two committee replicas will disagree,
and it is not money, whereas design G charges the refusal.

**Replacement text for G:**
> An authenticated invocation that preparation or admission refuses is charged the tariff price of its
> declared envelope. The debit is committed in a refusal receipt outside the refused turn. Wall-clock
> rate limits (`RefusalLane`) are mempool policy only. They may decide what a Host proposes, never what
> a replica validates. A committed block is never re-judged against a lane.

### W6. Design G is silent on admission order under saturation

"Meters account, not schedule" (HIST D3) is right for meter trees, but under saturation something still
orders admission and the design names nothing. A per-entity order is a commons that Sybil splitting
exploits (Miller & Drexler; OS §5).

**Replacement text for G (Decision, after "Meters are accounting, not scheduling"):**
> Under saturation the sequencer orders pending invocations by a published deterministic rule over their
> declared fee, so that replicas can audit it. The rule is never by count of subjects, objects or
> activities. Resumes of escrowed awaits are ordered by their deadline height.

### W7. Root G1's refund rule needs a storage clause

A storage deposit is collateral on public bytes, not a measurement of a private run; without returning
the excess when collection shrinks a checkpoint, GC at yield gives authors no incentive (OS §4).

**Replacement text, appended to G1:**
> Storage deposits are collateral on bytes that are committed and public. A deposit is re-priced at each
> yield on the stored size, and the difference is posted either way. This is not a refund of
> computation.

### W8. An `Enabled` affordance computed from law satisfiability is not "will admit" (design H and L12)

H computes `Enabled` when `Pred.Sat` finds a witness with the viewer's request slots fixed. A satisfiable
law shows the law *could* accept. It does not show that the *method* produces a Plan the law accepts. L12's
acceptance test ("every `Enabled` affordance admits") therefore fails by construction for any method whose
code refuses or yields a non-witnessing Plan. Naked Objects and Causeway separate *usable* (`disableX`)
from *valid with these arguments* (`validateX(args)`) for the same reason (OS §6.C).

H also omits provenance against a certified root, petnames, a kernel-pinned meta-card renderer, and the
split between cells, projection and local-first viewer state (OS §6, §3.5, §4.2).

**Replacement text for H (Mechanism, replacing the affordances sentence):**
> `affordances` returns, per method:
> - `Hidden`, if no capability the viewer holds reaches it;
> - `Disabled(reason)`, if the guard or law is `.unsat` for the viewer (residual, after redaction);
> - `Possible(example)`, if the law has a witness;
> - `Enabled(example)`, only if a `simulate` admission of the method with that example argument, at the
>   card's root, admits.
>
> Each card carries `(root, Merkle path, object pin, renderer pin)`. Names render through the viewer's
> petname cell. The meta-card (pin, law, upgrade policy, activities, history) uses a kernel-pinned
> renderer, never the object's package. Per-viewer layout and drafts are local-first and never cells.

L12's acceptance becomes: every `Enabled` admits; every `Disabled(reason)` refuses with that reason;
`Possible` is unconstrained.

### W9. Key custody: noted, not redesigned (tenancy B)

One broker account holds the seal key, provider keys and Discord secrets (`1d4b683f`): one confinement
domain for three secret classes (KeyKOS confines per capability set, OS §3.1). Key custody is Ember's
call, so this is a flag. The key-status reply (op 144) should name the root it reflects (ICP query/update
split, OS §4.2).

## The four OPEN questions, where my domain bears on them

**1. Synchronous cross-principal `call`: yes, with the root's guards.**
Every capability OS in the record used synchronous call/return across protection domains as its main
IPC: KeyKOS `CALL` with a resume key (OS §3.1), EROS, and seL4, where L4 after 20 years "kept"
synchronous IPC for client–server and dropped only timeouts and long IPC (Heiser & Elphinstone 2016;
OS §3.3). Their safety came from single-threaded domains queueing callers, which is mandatory re-entry
refusal under another name. The danger Agoric cites (shared state seen mid-update, Ethereum) is what
re-entry refusal and the frame-conflict rule remove. Bill by seL4 donation: the callee runs in the
caller's envelope (Lyons 2018).

**2. Laws: generate from `.obend` now.**
Generation is not "two shapes": `.obend` is the single source and `Pred` its compiled, analysable target
(Holochain integrity zomes, Singularity manifests; OS §4.5, §2). Unify only once the decidable fragment is
proved to compile to the same `Pred`.

**3. REPLAY: drop it for now (agree).**
C2's premise is weaker than stated: with receipts retained (decision I), an activity's `(Plan_i,
Response_i)` log is derivable from the accepted intents touching its record and slots, so REPLAY's real
cost is re-execution in the upgrade envelope. Revisit after W3 exists.

**4. Build order: answer slots and the resume contract first (agree, and it has landed).**
seL4's most expensive late change was retrofitting reply capabilities after the first refinement ("≈1
py, 17% of the original proof effort", Klein et al. 2009; OS §3.3). Before `call`, put W1 next: every
later lane assumes object authority and a law over activity writes.

## Commits

None. W1's right fix needs `ObjectRecord` (L3) and ACTIVITY-NATIVE is editing the same module; a patch
refusing "kernel-looking" cell ids would be a containment the doctrine forbids. The Mac data volume is at
99% (113 GiB free), under the protocol's 10% line, so I wrote nothing large locally (hbox clone only).

## Quest I want next

**OBJECT-RECORD (design L3 plus W1, coordinated with ACTIVITY-NATIVE).**
- **Scope:** `Kernel/ObjectRecord`; object-namespaced state cells; a facet capability on every
  declared-state write; the object's law judging `(old, new)` in birth, delivery and invocation; payer
  separated from authority; the activity kernel moved onto `ObjectRef`; the activity tariff replaced by
  the native `Capacity` plus checkpoint-bytes and storage-deposit terms (W4).
- **Acceptance:**
  - A birth naming a non-object cell is refused by name.
  - A Plan whose state write violates the object's law is refused with the residual.
  - A payer without the facet cannot write.
  - The Tally world's 46 checks still pass.
  - A theorem `activity_write_judged`: every committed activity state write satisfies the object's law at
    `(old, new)`, pinned with `#assert_axioms`.
