# IMPACT-P4 — the mini specs restated: M1 (the activity checkpoint) and M2 (interaction-tree divergence)

CX-P4, 2026-10-22. Read-only lane: nothing edited in nano or mini. Plan `redregg/work/PROGRAM-20261022.md:102-104` (P4),
`NANO-VS-MINI-20261022.md:373-377` (D.4). Trees: nano origin/main `1fc905f` (fetched; read with `git show origin/main:`),
mini `hbox:/tank/dregg-build/pipeline/warm-base/src` at `334316df` (read over ssh). Tags: READ (path:line read this
session), MEASURED (a command ran and its output is quoted), INFERRED (my reasoning, unchecked by any build).
Nano paths are relative to `~/dev/nanodregg`; mini paths are prefixed `M:`.

## 0. Verdicts

- **M1: the plan's expectation holds in substance, and its citation is wrong.** No deployed or planned nano row needs a
  checkpointed continuation. The response-dependent continuation is the author's `resume` term, but it is covered by
  `activity_resume_state` (`Lang/Proofs/StdActivityMethods.lean:64`) and `activity_program_safe`
  (`Lang/Proofs/StdActivityMonitor.lean:381`). `activity_history_runs` does not exist: LANG-75.9 records why it was never
  written (`decisions/lang.md:6178-6191`, READ). **No card.** M1 found one real gap, and it is not a checkpoint:
  an unanswered log row can never be removed (§1.5). That goes to the Lang worker as a separate item.
- **M2: divergence in nano is tick exhaustion, a named refusal, and the global type needs no `Tau` node.** Every run is
  bounded by `Bounds.treeTicksMax = 131072` (`Kernel/Bounds.lean:85`, `Kernel/Receive/Derive.lean:362-365`). So "never
  halts" and "halts after the cap" are the same observation, `{label}: Fault.ticks`, and the run is refused. The monitor
  theorem quantifies over runs that RETURNED (`StdActivityMonitor.lean:344, :391`). That is every admitted run, not
  every body: a body that diverges has no admitted run, so the theorem has nothing to say about it.

## 1. M1 — what a mini checkpoint carries that nano's captured row does not

### 1.1 The nano row (READ)

- Log row value: `{answered : opt (Σ plans. response), captured : Σ plans. captured}` (`Lang/StdActivity.lean:47-48`).
  Key: `{notBefore : nat, agent : digest}` (`:35`). Cursor row: `{captured}` (`:43-44`).
- `captured` is first-order data. A relation's value must satisfy `d.val.isData` (`Lang/Package.lean:455`), and
  `Ty.isData (.fn _ _) = false` (`Lang/Ty.lean:101-105`). A row can never hold a closure.
- The resumption is `p.resume : S → captured → response → Req → S` (`Lang/StdActivity.lean:228-230`, checked by
  `checkE`). The generated method applies it to `[state, captured, arg.response, req]` (`:145`), where `state` is the
  object's state at the RESUME Turn (`:160-161` binder comment). It emits exactly two edits: the log upsert and the
  cursor retract (`:146-149`).
- `activity_resume_state` (`StdActivityMethods.lean:64-88`) states that the generated method's successful path computes
  the author's `p.resume` at the retained capture and this call's response.
- The code a resume runs is fixed when the activity starts, for two reasons. The package is ROM. A programmed object's
  state cannot be written directly and its laws cannot be replaced: both arms refuse `hasMethods`
  (`Kernel/Receive/Derive.lean:148, :163`).

### 1.2 The mini record (READ)

`M:Kernel/ObjectiveActivity.lean:176-195`, `Record`:
`object, activity, pin, input, generation, checkpoint, checkpointDigest, escrow, tried, phase`. The phase is
`awaiting Await | done result | faulted reason` (`:170-174`). An `Await` is `{id, source (reply slot+decider | height),
deadline, yieldedAt}` (`:150-155`). `checkpoint` holds the bytes of `encodeState` (`:7-9`): the WHOLE demand-machine
state, made of the heap of cells (suspended, evaluating or cached closures), the control, and the frame stack with
environments (`M:Theory/ObjectiveBendCheckpoint.lean:168-193, :265-267`). A resume is `resumed {outcome, view}`: the
settled outcome plus a view of the object's declared state read IN THE SAME TURN (`:39-46`). The kernel supplies
the outcome sum: `reply | refused | unknown | timedOut | broken | upgraded` (`:1091-1098`).

### 1.3 The statement (INFERRED from 1.1–1.2; each line names its counterpart)

A mini checkpoint carries six things nano's captured row does not:

| # | mini keeps | nano's counterpart | lost? |
|---|---|---|---|
| C1 | the **implicit continuation**: the frame stack, the environments and the heap at the yield, including closures and unforced thunks | the plan tag (the `Σ plans` injection) plus first-order `captured` data the author chooses | **No semantic loss; the author does the encoding.** This is defunctionalisation: the yield point becomes the plan tag, its free variables become `captured`, and `k` becomes `p.resume`'s `case response`. Bounded by `2·plans+1 ≤ methodsMax = 64` (`StdActivity.lean:220`, `Lang/Package.lean:253`), so at most 31 continuation points per activity, and by the row value bound (`Kernel/Bounds.lean:31`, `valueBytesMax = 65536`) |
| C2 | **cached cells**: work forced before the yield is not repeated (`M:Kernel/ObjectiveResumeContract.lean` header: `stored_commits_where_lazy_exhausts`, "the cache saves ticks and budget") | whatever the author did not capture is recomputed in the resume Turn, under that Turn's budget | cost only. Nano is call-by-value, and `captured` is forced data |
| C3 | **`generation`**: one record crosses many yields | a log row is one exchange. An answered row refuses every further upsert (`StdActivity.lean:91`, `"answered"`), and a second round is a NEW `start_*` at a new key | multi-round shape only; see 1.4 |
| C4 | **`pin` + `input`**: the program is re-instantiated and re-checked at each turn (`:179-184`) | ROM package; `hasMethods` refuses relaw/write (`Derive.lean:148,163`) | nothing; nano needs no pin because the code cannot change |
| C5 | **`phase = done result / faulted reason`**: the activity's return value and its fault | the result is whatever `p.resume` writes into `S`. A fault is a refused Turn (no row change) | the return value is not in the row. LANG-45 already measured this as the one observable loss (ACT-D `:79`, READ) |
| C6 | **kernel-supplied outcomes** `timedOut/refused/broken/upgraded` and a mandatory `deadline` | `response : R` is the author's sum only. No deadline. `notBefore` is only a key field | **an exit, not a continuation**: see 1.5 |

Mini's "view" is not a difference. Nano's `p.resume` receives the live state `S` and `Req`
(`Lang/Package.lean:64-66`: `agent, notBefore, occasion, principal, self, validUntil`) in the same Turn. That is mini's
`resumed {outcome, view}`, without the version compare-and-swap. Nano does not need that compare-and-swap, because the
Turn is atomic and the state is read at execution time.

**So the answer to M1's question is: no.** Under nano's resumption contract, a resumption depends on state, captured,
response and request. Mini's checkpoint, outcome and view correspond to those four, provided the author
defunctionalises (C1).

### 1.4 Does any nano row need C1, C3 or C5? (MEASURED / READ)

Census of every `ActivityPlan` on origin/main: `git grep -n "precondition :=\|resume :=\|(plan "` over `*.lean`/`*.ob`,
excluding the generator and its proofs. MEASURED: four sites.

| row | plan | captured | resume depends on | needs more? |
|---|---|---|---|---|
| Bell (`world/resident/Bell.ob:10-11`) | `ask` | `{text}` | `state` only (`(resume state)`). The hand-written `answer` (`:12-19`) writes the response into `answered` | no |
| Std.hole (`Lang/StdHole.lean:239-243`) | `fill` | `V` | `s` only. The response is `{}` | no |
| journey (`Lang/Journey/Activity.lean:12-16`) | `step` | `nat` | `case response`, `captured`, `state` | no |
| fixture (`Lang/Proofs/StdActivityTeeth.lean:8-19`) | `step`, `other` | `nat` | same as the journey | no |

Planned rows:
- **The fuse's session row** (`promo/IMPACT-PROT-6.md:117, :126, :163`, READ). It is `activityLog [settlePlan]` with
  `captured := {pair, theta}`, and "the later step (settlement) is the session activity's own resume". The offer rows
  are retracted in the fuse Turn, but θ's compliance was judged there (`jointOk`, `:149`). So the settlement needs
  `{pair, θ}`, the response and the live state, all of which it has. MEASURED: `Lang/StdOffer.lean` is not on origin/main
  (`git ls-tree` shows no `*Offer*`), so `settlePlan`'s `resume` term is unwritten. Refuter R1 covers it.
- **Multi-round negotiation.** P3-MEASURE counted 0 second rounds (`promo/IMPACT-P3-MEASURE.md:42-54`: "(b) = 0
  everywhere. Every deployed activity is one exchange deep") and 0 ≥2-round negotiations (`:82-98`). C3 has no consumer.

### 1.5 The gap M1 did find: an unanswered row has no exit (READ; consequence INFERRED)

The waiting guard refuses `retract` of an unanswered row: `("none", refusedT "unanswered")` (`StdActivity.lean:80-82`).
Insert requires `answered = none` (`:78-79`), and only the resumer may upsert (`:83`). Every method of the package is
under this guard (`activity_program_safe`'s premises are on the guard, not the method;
`StdActivityMonitor.lean:329-334`), so no package method can abandon a waiting row. The kernel's `retire`
(`:206-207`) passes through the same guard.

This refutes ACT-D's mapping "`abandon` = `retire` past `closes` by anyone" (`ACTIVITIES-DESIGN-20261022.md:464-466`,
READ). The generated activity has no `closes` field, and `retire` needs an answer (`activity_retire_needs_answer`,
`StdActivityTeeth.lean:96`).

INFERRED consequence: when the resumer is silent, or `p.resume` cannot finish under `treeTicksMax` (M2), the row is
waiting forever. Its slot counts against the log's `limit`; the Bell's is 1024 (`Bell.ob:7`). Mini has C6 (deadline →
`timedOut`, `faulted`) for exactly this case.

This is a liveness/garbage gap, not a checkpoint gap: adding a checkpoint would not close it. The fix is a deadline
arm in the generated guard (retract or answer-`timedOut` once `req.notBefore ≥ key.notBefore + patience`). That changes
`activityWaiting`, so it must restate `waiting_retract_iff` (`Lang/Proofs/StdActivity.lean:88`) and `WaitingStep`
(`StdActivityMonitor.lean:44`), and re-emit the Bell. It also WIDENS what the guard admits, so it falls under the
CLAUDE.md pause item 2: Ember's call.

### 1.6 Decision text for M1 (ready to paste as LANG-75.x)

> **LANG-75.x M1 · the captured row loses nothing a mini checkpoint keeps that a nano row uses; no checkpointed
> continuation (2026-10-22; CX-P4; IMPACT `redregg/work/promo/IMPACT-P4.md` §1)**
> **Measured.** A mini `ObjectiveActivity.Record` (M:`Kernel/ObjectiveActivity.lean:176`) holds the whole
> demand-machine state as its checkpoint (heap, control and frame stack; M:`Theory/ObjectiveBendCheckpoint.lean:265`),
> plus generation, pin, input, escrow and phase. A nano log row holds `{answered, captured}`, with `captured`
> first-order data (`Package.lean:455`, `Ty.isData`).
> A nano resumption is `p.resume state captured response req`. The state and request are read in the resuming Turn,
> which is mini's "resume with view". The frame stack becomes the plan tag plus `captured` by defunctionalisation, at
> most 31 points per activity (`2·plans+1 ≤ methodsMax`). Pin and input are unnecessary because a programmed object's
> code and laws are fixed (`Derive.lean:148,163` refuse `hasMethods`).
> Census of the four plans on main (Bell `ask`, hole `fill`, the journey's and the fixture's `step`): each resume
> reads only the state, the capture and the response. The planned fuse session (`captured := {pair, θ}`) needs
> nothing more, and P3 measured 0 second rounds.
> **Decision.** No checkpointed continuation and no `lang!`. Two things move:
> - The plan's `activity_history_runs` was never written (LANG-75.9). The coverage is `activity_resume_state` (the
>   generated method reaches the author's continuation at the capture and the response) plus `activity_program_safe`
>   (every admitted log edit is a `WaitingStep`).
> - The response-dependent body of `p.resume` is author code. No theorem covers it beyond its typing.
> **Not a checkpoint, recorded:** an unanswered row has no exit (`activityWaiting` refuses retracting it). ACT-D's
> "abandon = retire past closes" is not what the generator does. That is a separate item (deadline arm; it widens a
> guard, so Ember's call). It is not a reason for a checkpoint.
> **Price.** 0 theorems restated. 0 bytes moved.

## 2. M2 — interaction-tree divergence

### 2.1 Mini (READ)

`M:Theory/ObjectiveBendInteraction.lean:62-71`: `Node = vis | ret | blackhole | refused | malformed | spin`. `spin` is
"silent divergence: the machine never halts" (`:13-14, :70-71`), and `node_spin_iff` makes it exactly `∀ n, ¬ Halts s n`
(`:110`). The tree is budget-FREE: an ending counts only if it is reached "above a threshold" under every larger resource
vector (`:17-19`, `EndsAbove`). `chain_spin` (`:167`), `delivery_spin` (M:`Kernel/ObjectiveReferenceLift.lean:257`) and
`History.spin` (`:503`) all say the same thing: where the reference spins, the kernel commits nothing.
`blackhole` (re-entering a thunk under evaluation) exists because the machine is lazy.

### 2.2 Nano (READ)

- `run` is the only loop. It recurses structurally on fuel; `0 => .fault .ticks` (`Lang/Eval.lean:245-253`;
  header `:18-22`: "Every way a run can end is a named `Fault` or a value"). `run_used_le` (`Lang/Proofs/Run.lean:38`)
  says no run takes more steps than its fuel. `RunOK` (`Lang/Proofs/Sound.lean:244-246`) says a typed run ends with a
  value of its type or a non-`stuck` fault.
- The fuel of every program run in a Turn is `min budget Bounds.treeTicksMax` (`Kernel/Receive/Derive.lean:362-365`;
  "nothing else runs a program"), and `treeTicksMax = 131072` (`Kernel/Bounds.lean:85`).
- Divergence is expressible: `fix` ties a record knot (`Lang/Term.lean:5-7, :48`), and "a lazy field that diverges
  exhausts the budget instead of hanging" (`Lang/Data.lean:7-8`).
- Every fault refuses, at all four places a program runs:
  - **Method.** `.fault f _ => throw (.program "{label}: {faultText f}")` (`Lang/Program.lean:453`). The converse is
    `runMeasuredWith_ok` (`Lang/Proofs/Rel.lean:990-1001`): an `.ok` run has `run … = .value v used`.
  - **Extraction.** `Lang/Program.lean:465`.
  - **Guard.** A fault is `lawDenied` (`Lang/Program.lean:438`).
  - **Law.** `fault_never_admits` (`Lang/Proofs/Receiver.lean:66-79`) and `runLaw_never_stuck`
    (`Lang/Proofs/LawRun.lean:150`).
- A refused call is final. It is recorded and answered `refusedFinal` without being re-derived (KERNEL-44;
  `Kernel/Receive/Submit.lean:23-37`). A bigger budget is a NEW signed call, still capped at 131072.
- The monitor: `activity_monitor_safe` / `activity_program_safe` hypothesise `runMeasured … = .ok (…)` /
  `(Lang.program …).run … = .ok (…)` (`StdActivityMonitor.lean:344, :391`).

### 2.3 The statement (INFERRED from 2.2; every step is a READ line)

1. Nano has no reference semantics without a budget. Its only semantics is `run` at a fuel of at most 131072, so mini's
   `spin` (∀ n, ¬Halts) has no observable image. For any body t:
   - if t never halts, then `run lib stackMax f 0 (init t) = .fault .ticks f` for every reachable f;
   - if t halts only after more than 131072 steps, the result is the same.
   Mini's `spin` and "costs more than the cap" are therefore one nano observation: the refusal
   `"{label}: Fault.ticks"`.
2. Divergence is not exactly tick exhaustion. Divergence is a STRICT subset of it. The refusal is named, it is
   final for that transaction, and it commits nothing.
3. Nano has no `blackhole`, because it is call-by-value with no update frames. It has no separate `malformed` node:
   an extraction failure or bad state bytes is also a named refusal (`Program.lean:463-465`).
4. A global type over nano's admitted Turns therefore needs **no `Tau`/`spin` node**. Every admitted step is a run that
   returned a value within at most 131072 ticks, and a non-returning body contributes no step, only a recorded
   refusal.
5. The monitor theorem is about runs that returned, which is every ADMITTED run. Reading it as "every body" is wrong
   in its wording and right in its effect. A body that diverges is not excluded by a premise. It never produces the
   `.ok` that the theorem's hypothesis `h` needs, so the theorem covers it vacuously, and it has no edits to cover.
6. Divergence across Turns is different. A peer that never answers leaves the trace with no next step. A global type
   needs no node for that either: the monitor's claim is a prefix-closed safety property. What nano cannot state is
   LIVENESS. Combined with §1.5, a silent peer or an over-cap resume term leaves a row waiting forever. Mini's
   `deadline`/`timedOut` covers that case; nano has no counterpart.

### 2.4 Decision text for M2 (ready to paste as LANG-75.x, or into PROT-3's decision)

> **LANG-75.x M2 · divergence is a refusal: the global type has no `Tau` node (2026-10-22; CX-P4; IMPACT
> `redregg/work/promo/IMPACT-P4.md` §2)**
> **Measured.** Every program run in a Turn has fuel `min budget treeTicksMax` = at most 131072
> (`Derive.lean:362-365`, `Bounds.lean:85`). `run` is structural on fuel and ends with a value or a named fault
> (`Eval.lean:245-253`, `run_used_le`). Every fault is a refusal:
> - a method fault at `Program.lean:453`, with `runMeasuredWith_ok` as its converse;
> - an extraction fault at `:465`;
> - a guard fault at `:438`;
> - a law fault by `fault_never_admits`.
> A refused call is final (KERNEL-44).
> Mini's `spin` (M:`ObjectiveBendInteraction.lean:71`, `node_spin_iff`) is a node of a budget-free reference tree. Nano
> has no budget-free semantics. A body that never halts and one that halts after 131072 ticks give the same
> refusal, `{label}: Fault.ticks`.
> **Decision.** PROT-3's global type is over admitted Turns and has no `Tau`/divergence node. `activity_program_safe`
> covers every admitted run, because admitted means returned within the cap. Divergence is a strict subset of tick
> exhaustion, which is a named, final refusal that commits nothing.
> **Boundary, stated.** The monitor is safety only. A silent resumer, or a resume term over the cap, leaves its log row
> waiting forever: nothing may retract an unanswered row (`StdActivity.lean:80-82`). Mini handles this with
> `deadline`/`timedOut`; nano has no counterpart (see M1's recorded item).
> **Price.** 0. No theorem, no byte.

## 3. Does M1 need a card?

**No `lang!` for a checkpointed continuation.** It has no consumer: four plans on main, one planned session, and 0
second rounds (§1.4). Its one capability beyond nano's (C1) is reachable by defunctionalisation, within 31 points and
64 KiB.

**The §1.5 exit gap is a separate item.** It needs a deadline arm in `activityWaiting` that retracts an unanswered row,
or answers it `timedOut`, past a declared patience. It would restate `waiting_retract_iff` and `WaitingStep` (+1
action), re-emit the Bell, and widen a guard. Recommendation: the Lang worker opens a `cv task` for it with Ember as
decider. Trigger: the first row whose resumer can be absent (the fuse session, if settlement can stall), or the Bell
reaching its 1024-row limit.

## 4. Three refuters, with measurements

**R1 — a planned row's resume needs data that is neither captured nor in live state.** Claim at risk: §1.4's "no row
needs a checkpoint".
- Measured: 4/4 plans on main read only `{state, captured, response, req}` (census in §1.4).
- The one planned row, the fuse's `settlePlan`, is UNWRITTEN: no `Lang/StdOffer.lean` on main (MEASURED).
- **Refuted if** `settlePlan.resume` (once written) must read something the fuse Turn retracted, or a peer's row. The
  offer rows' `terms` are an example. Rows are self-only (`P3-MEASURE:56-58`, `Lang/Rel.lean:179`), so a value not
  copied into `captured` at the fuse cannot be recovered.
- Check when PROT-6 lands: diff `settlePlan.resume`'s free variables against `{s, captured, response, q}`.

**R2 — some row needs more than 31 continuation points, or more than 64 KiB of captured context.** Claim at risk: C1
"defunctionalisation suffices".
- Measured: `methodsMax = 64` (`Package.lean:253`). `2·plans+1 > methodsMax` refuses `tooManyPlans`
  (`StdActivity.lean:220`), so at most 31 plans.
- Measured: `valueBytesMax = 65536` (`Kernel/Bounds.lean:31`).
- Deployed maximum: 2 plans (the fixture); the Bell has 1 and the hole has 1.
- **Refuted if** a row's protocol has more than 31 distinct suspension points in ONE object, or its pending context
  does not fit a row value.
- Mini comparison: its Record has no such bound per activity, only a byte charge. Each extra point still costs a
  `methodsMax` slot pair in nano.

**R3 — something in nano distinguishes divergence from tick exhaustion, or retries past a ticks refusal.** Claim at
risk: M2's "a final, named refusal; no `Tau`".
- Measured: `git grep -i "Fault.ticks|\"ticks\"|retry|raise.*budget"` over `Hosting Kernel/Receive client
  launcher`. It found only the journal's exact-retry recognition (`Call.lean:410-413`, `Submit.lean:4, :29-37`), which
  answers `refusedFinal` without re-deriving, plus `client/tests/run.rs:851` (a refused key, one retry, then refused).
- No path raises a budget and re-runs, and every pool is capped at 131072 (`Derive.lean:365`).
- **Refuted if** a host or resident loop re-submits a ticks-refused call with a fresh tx id and a larger budget until
  it succeeds. That loop would be a host-level `spin`: the resident's `Prog` would need a divergence branch, though the
  kernel's global type still would not.
- Also refuted if a future change lifts `treeTicksMax` or adds an unbounded pool. Then "over the cap" stops
  approximating "never halts" at any fixed size, but the refusal still names it, so the type still needs no `Tau`.
