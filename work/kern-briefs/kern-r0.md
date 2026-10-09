# kern-r0 — `Turn.absent` + the storage answer + the OB totality pole (R0 of train `kern`)

You are a Codex worker (gpt-6-astra) on the Mini repo, lane based at 546c1c88. Deputy: DEPUTY-KERNEL (Claude).
Design (read §0, §1 rows 10-11, §3 "The fix for rows 10-11", §6.1): it is NOT in your lane; the deputy
pasted the parts you need below. Every line ref below is at 546c1c88 and was READ by the deputy unless
marked ASSUMED.

## Goal of the train
Objective Bend (OB) admission lands inside the kernel's one transition model `World.admit`. Today
`deployed_refines_step` (Kernel/HostRefinesWorld.lean ~:687-716) covers every HostStep, OB's included,
PROVIDED `Turn.ofLoaded` (HostRefinesWorld.lean:410) returns `.ok` on the OB intent. R0 makes that
proviso true and measured.

## FIRST: read the real signatures and paste them into WORKLOG.md before any edit
At least: `Turn` structure, `World.admit`, `Reject`, `Shaped`, `Turn.footprint`, `History` (World.lean:~415,
`legBytes`), `World.patchBytes` (World.lean:~497), `TurnOfIntent.Refusal` (TurnOfIntent.lean:~540-550),
`guardLeg` (:630), `storageOf`/`chargeOf` (:635-644), the guard check in `ofCells` (:684) and the storage
check (:692-693), `Turn.ofLoaded` (HostRefinesWorld.lean:410), `Represents.storage` (HostRefinesWorld.lean
~:399-400), `SnapRepresents.cells` for a `fresh` slot (DeployedBridge.lean:9-14), `cshakeHistory`
(WorldRoot.lean:695-712), `turn_negation_refused`, `every_admission_is_turn` (TurnCensus.lean:~249), and
the OB emitters of the two refused guards: `ObjectiveActivity.lean:3423,3449-3451,3473-3478` (create
without seed), `ActivitySeatEnd.lean:265-269,344-357`, `ObjectiveDomain.lean:83-89,769-772`,
`ObjectiveActivityWire.lean:224-225,246`.

## Part (a) — the storage answer. Report it with `report` THE MOMENT you have it; the deputy relays it.
Risk: every OB cell is ONE RAM address holding a whole `Payload` blob (ProtectedCell.layout:
`Namespace := Unit`, `discipline := fun _ => .ram`). The receiver charges `sum post.bytes.length`
(ObjectiveActivityReceiver.lean:~924). `ofIntent` refuses `.storageAboveCharge` when
`storageOf H creates legs > intent.exactCharge .storageBytes`. `History.legBytes` is a PARAMETER: no
deployed definition exists (the toy ones are `fun _ => 0`, HostRefinesWorld.lean:1207, WorldBench.lean:58,
World.lean:2163,2422 — a zero `legBytes` makes the storage check vacuous; do not use one).
TurnCensus.lean:145 has `legBytes := fun l => 16 * (# non-read ops)` at the census layout.
1. PIN a deployed `legBytes` (and `imageBytes`) as a named def next to the deployed bridge
   (DeployedBridge.lean or a new `Kernel/DeployedHistory.lean`): D2's rule — a leg's bytes are the
   bytes of the values it WRITES (allocate/write new value), not the old value, not reads; a free
   writes nothing (ASSUMED-BY-DEPUTY that D2 says this; check World.lean:357 docstring and say what it says).
2. PROVE or REFUTE, as named theorems: for a single-address whole-blob OB leg
   (`allocate () () payload` / `write () () (some old) (some new)` / `free () () (some old)`), the
   deployed `legBytes` equals the receiver's charge for that post (`post.bytes.length`, whatever the
   receiver sums — read it), so the OB intent does NOT trip `storageAboveCharge`. If it WOULD trip
   (e.g. the canonical encoding adds framing, or creates double-count via `imageBytes`), say exactly by
   how much and fix the CHARGE MODEL so both sides count the same written bytes — never loosen the
   check, never make OB's charge "≥ whatever". Report which.

## Part (b) — `Turn.absent`
OB pins ABSENCE in two cases and `ofIntent` refuses both with `Refusal.guardOnAbsent`:
 - row 11: `create` WITHOUT seed guards `stateCell`, which is absent (ObjectiveActivity.lean:3423,3473-3478;
   added again by `finalIntent`, ActivitySeatEnd.lean:265-269);
 - row 10: the domain judgment guards every member's `stateCell`; a stateless member is legal
   (`jointSlots` skips `none`, ObjectiveDomain.lean:83-89), so the guard names an absent cell.
DROPPING THOSE GUARDS IS FORBIDDEN (it weakens a check: a concurrent create/seed would slip past).
Add to `Turn` a guard kind:
```lean
  absent : List CellId := []   -- must be absent AND not retired when the turn runs
```
checked in `World.admit` (before creates apply): `∀ c ∈ t.absent, w.cells c = none ∧ w.retired c = none`,
refusing with a NEW `Reject.cellPresent c` (and `.retiredIdentifier` for a retired one, if that reject
exists — read it). `Shaped` gains `t.absent.Nodup` and disjointness of `absent` from `creates` cell ids and
from `legs.map cell`. `Turn.footprint` includes `absent`. `ofIntent` maps a `ReadGuard` on an absent,
unretired cell to `absent` and NEVER returns `guardOnAbsent` — delete that constructor if nothing else
can produce it (prefer deleting to keeping a dead refusal). `turn_negation_refused` gains the pole
"the cell appeared" (a turn whose absent cell is present is refused). `step_frame`/`step_leg`/`step_wf`
should be unaffected (no write). If `Turn` is encoded/hashed anywhere (TurnRecord, WorldRoot encode),
`absent` MUST be in the encoding — a field outside the digest is a forgery surface. This is greenfield:
break shapes freely; say in the WORKLOG what shape changed and what re-emits.
Keep `every_admission_is_turn` at its count (read the count; design says 51/51) and every named World
theorem building.

## Part (c) — the totality pole (executable, RED at the base: your FIRST commit-worth of work after (b) is what makes it green)
Run `Turn.ofLoaded bridge H opened.durable verdict.intent` (with YOUR pinned deployed H) over every
recorded intent of the OB journey rows (`activity`, `objectrecord`, `call`, `send`, `seats`, `domain`,
`upgrade`; docs/OBJECTIVE-BEND.md:529-537) and assert `.ok` on each. Find where the journeys' intents are
recorded or can be reproduced (read the journey scripts under scripts/pipeline READ-ONLY — another train
owns those files; do NOT edit them; and Host replay entry points). Prefer a compiled Lean exe or `lean_exe`
target in this repo that reads recorded intents and prints one line per intent `row idx ok|refusal`, run via
`request_journey`/`request_build`. Counts must be printed (how many intents per row) so an empty run
cannot read as green. If the journeys never exercise a seedless create or a stateless domain member,
SAY SO and add a constructed instance of each as a named theorem
(`theorem ... : (Turn.ofIntent ... ).isOk = true := by decide/rfl` or `native_decide` only if unavoidable —
native_decide is guard-refused; ask first). Plant: with `absent` removed (revert ofIntent's mapping),
the pole must go RED on row 11 — run the plant, record the red output in WORKLOG, then restore.
If wiring the pole runner is a long script job, ask the deputy (`ask_deputy`) to put a sol worker on it
and give the exact entry point you want it to call.

## Rules
- Files you may edit: Kernel/World.lean, Kernel/TurnOfIntent.lean, Kernel/TurnCensus.lean,
  Kernel/HostRefinesWorld.lean, Kernel/TurnRecord.lean, Kernel/WorldBench.lean, Kernel/WorldRoot.lean,
  Kernel/DeployedBridge.lean, new Kernel/DeployedHistory.lean, new Kernel/ObjectiveTurnTotality*.lean,
  their imports in the umbrella, lakefile exe entries, and pin TSVs those regenerate. Need another? ask.
- OFF LIMITS: scripts/pipeline, native/spk-host, deploy/, journey.d (train `prod`), Theory/AuthTrie*,
  Compiler/DurableIndex*, and `Represents.spent` (do not move it toward the trie).
- No `sorry`/`admit`/`axiom`, no `#guard` for facts (name theorems; `#assert_axioms` on new headline
  theorems). No vacuous statements: no conclusion closed over the hypotheses, no `∨ Collision` over an
  infinite type, no `fun _ => 0` histories in deployed claims.
- Builds and runs ONLY via `request_build` / `request_journey` / `request_cargo`; end your turn after each
  request. Never poll.
- `submit` when (a)(b)(c) are done with the umbrella green. In the submit note list: the storage answer,
  each new/changed theorem NAME + statement, the pole counts green, the plant red output.
