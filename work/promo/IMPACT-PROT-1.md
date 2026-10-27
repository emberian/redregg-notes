# IMPACT-PROT-1 · the activity as a protocol over the kernel's history

CX-PROMO-3, 2026-10-22, nano main `51089fb`. Plan §3 P3 PROT-1; ruling R-0044 (cheap branch). Nothing built yet.
**This IMPACT carries a design FORK (§3) and an ASK for a grant (§6). Building waits for the RELEASE.**

## 1. What the plan's statement would be, and why it has no object today (READ)

Plan: `activity_history_runs` via `object_history_chain` (`Kernel/Proofs/Logic/History.lean:357`) + `machine_reached`
(`Lang/Proofs/StdChain.lean:100`) + `activity_start_state` / `activity_resume_state` (`StdActivityMethods.lean:9, :64`).

Three measured obstacles:

1. **An activity has no machine law.** `machine_reached` is over `Chain (Step lib (machineLaw S f states initial
   edges))`: a STATE law over a phase field `f`. `Std.activity` writes no phase into state ("No phase field is written
   into object state", `Lang/StdActivity.lean:91`). Its protocol is a per-KEY machine on the `log` row
   (absent → waiting (`answered = none`) → answered → retracted), enforced by the ROW GUARD `activityWaiting` (`:69`),
   with the cursor's own guard `activityQueued` (`:92`). `object_history_chain` lifts state laws only.
2. **The history trace drops the rows.** `ObjectStep.invoke` and `.nested` (`History.lean:96–122`) bind the run's
   `rows : List (RowSlot D × RowAct)`, then leave them out of the trace tuple
   `(look, pkg, laws, req, old, new, calls)`. An activity step is invisible to every theorem over `ObjectHistory`.
3. **No landed theorem says an admitted run's row edits passed their guards.** The deployed run calls
   `guardEdits` (`Lang/Program.lean:428`, called at `:461` in `runMeasuredWith`) after `editsOf`. `Lang/Proofs/Rel.lean`
   proves `guardEdits_never_stuck` and `guardEdits_unpinned`, but not "`runMeasuredWith … = .ok (…, rows, …)` ⇒ every
   edit's guard returned ok".

So the plan's composition cannot be written. The per-step facts EXIST at the guard grain: `waiting_insert_iff :208`,
`waiting_upsert_iff :320`, `waiting_retract_iff :88`, `waiting_no_replay :117`, `waiting_upsert_preserves_capture :233`
(`Lang/Proofs/StdActivity.lean`). Composing them without a history would be a rename (plan §8.2).

**NanoBridge** (`Lang/Contextual/NanoBridge.lean`) is NOT an activity embedding. It is `Hosting.Resident.Prog` (the
RESIDENT's free program) as a `Prot`, and `nano_runs_iff` (`Lang/Proofs/Contextual/Protocol.lean:906`) is the tool
PROT-3's `bell_resident_conforms` needs (from `tick_order`). Plan: "becomes the activity instance or goes". Measured
answer: neither. It STAYS, as the resident half's instance, consumed by PROT-3. PROT-1 deletes nothing there.

## 2. The theorem, as a statement (shape A, the default)

Objects: the kernel's history around one object whose package is an activity (`ObjectHistory X obj w w' tr`, with the
trace carrying each judged step's row edits), and the per-key machine of its `log` relation.

```lean
/-- the per-key phases of an activity log row, and its edges (one machine, StdChain's Reach) -/
def activityEdges : List (Label × Nat × Label) :=
  [("absent", 0, "waiting"), ("waiting", 1, "answered"), ("answered", 2, "absent")]

theorem activity_history_runs {X} (hX : X.Lawful) (hprog : X.program = Lang.program …)
    {obj : D} {p : Package} {S plans cursor log cd ld resumer}
    (hp : p = Std.activityPackage S cursor log … resumer plans …  -- or: p.rels's `log` guard field IS
          ∨ …)                                                 -- `activityWaiting S plans ld resumer`
    (hin : ∀ e ∈ tr, e.pkg = some pd ∧ readPackage e.look pd = .ok p) :
    ObjectHistory X obj w w' tr →
    ∀ k, ∀ (a b) consecutive log edits at k in tr,
      (phase a, edgeOf b, phase b) ∈ activityEdges        -- Reach activityEdges (phase at w) (phase at w')
      ∧ (b = insert → b's signer = k.agent ∧ answered = none)
      ∧ (b = upsert → resumer state req ∧ captured unchanged ∧ same plan)
      ∧ (b = retract → the row was answered)
```

Proof route: (i) **`run_edits_guarded`** (Lang, new): `runMeasuredWith … = .ok (s, calls, rows, …)` ⇒ for each
returned edit, `guardOld` found its old row and `runLaw` on the relation's guard returned `.ok (.ok ())`. This is
read off `runMeasuredWith`'s do-block, its last bind before `pure`. (ii) the `runLaw` ↔ `BigStep` bridge that the
`waiting_*_iff` statements are in (READ: `runLaw_ok_body`, `Lang/Proofs/Std.lean:846`, takes a `runLaw` ok to a `BigStep` of the body, and
`runLaw_contextual_body`, `Lang/Proofs/LawReceiver.lean:129`, does the same under a contextual library but is PRIVATE.
A guard is `runLaw` on `.get (.ref g) gl`, the same shape as a law field, so the public one applies when the guard
mentions no closure package (`NoRef`, as every generated guard is). INFERRED until built). (iii) the five guard theorems. (iv) induction on `ObjectHistory`, carrying the
per-key phase.

**Deployed mutations that make it false** (each is the plant, to be built and run first after the release):
- **P1** `runMeasuredWith` without its `guardEdits` line → an upsert of an answered row is admitted → the
  `answered → answered` step has no edge → RED by name at `activity_history_runs` (and at `run_edits_guarded`, its
  first half).
- **P2** `activityWaiting`'s upsert arm without the `answered = some → refusedT "answered"` case (`:88`): a second
  answer → no edge → RED. Distinct from P1: it falsifies only the history theorem through the guard, not
  `run_edits_guarded`.
- **P3** the plan's own tooth, "a method outside the declared machine": a package method that upserts `log` directly.
  The Bell's `answer` IS such a method (custom, not `resume_ask`). Measured: the theorem COVERS it, because the
  statement is over the guard, not over the generated methods. So P3 is not a red. It is the reason the statement is
  guard-grain: it constrains author methods too. I say this so a reader does not count it as a tooth.

**Consumers.** PROT-3's kernel half (the Bell = an activity: `ring` → start, `answer` → resume; its global type's kernel
projection is this theorem at `plans = [ask]`, resumer = `state.resident`). PROT-4: `activity_monitor_safe` is
`run_edits_guarded` + the guard theorems at the step grain, so PROT-4 shrinks to `activity_monitor_transparent`. Std.hole's
`fill` activity (`accept` → start, `resume_fill`).

## 3. The fork

- **A (default): widen the one history.** The `ObjectStep` trace element becomes a STRUCTURE (`ObjectEvent`: look, pkg,
  laws, req, old, new, calls, **rows**) in place of the 7-tuple. The current users project with `e.2.2.2.2.2.2`
  (EscrowAdmitted :389), which is the fragile shape, so this deletes it rather than adding an eighth component. Every
  theorem over `ObjectHistory` is RESTATED (the trace type changes); none gains a hypothesis.
- **B: Lang only, no history.** Land `run_edits_guarded` + `activity_step_edges` (one admitted run of an activity
  package: each log edit is an edge with its role). Price 0, no grant. But it is PROT-4's `monitor_safe` under another
  name, and the history lift ("over the kernel's history", the card's point) does not happen.
- **C: over the World's rows, not the trace.** The phase of key k is read from `w.rows` along `World.fold` of
  receive-derived Turns. That needs "every row change at obj's log came from a guarded run of obj's package", which is
  the history's job (ObjectStep's `keep`/`frame`/`other` arms already enumerate who can touch obj). C rebuilds
  `ObjectHistory` beside itself: a twin. Refused by default.

## 4. Premise price (MEASURED by grep at 51089fb; statements not yet re-elaborated)

Under A, statements whose TYPE changes (the trace's element type), 0 hypotheses gained:
- `Kernel/Proofs/Logic/History.lean`: 7 public theorems (`object_step_none/some/live`, `object_history_of_audit`,
  `object_history_chain`, `object_history_runs`, `object_history_start`) and 5 private ones. Each is a
  `RESTATES-MEANING` line under GATES-20t, because the type differs.
- `Kernel/Proofs/Logic/HistoryWitness.lean`: 3 statements (`:31, :115, :124, :136`).
- `Ledger/Proofs/EscrowAdmitted.lean` (`:345, :367, :389`) and `Ledger/Proofs/EscrowInvokes.lean` (`:73, :104`):
  `escrow_invokes_one_payout` and its admitted instances.
- `Lang/Proofs/Chain.lean:29`: docstring only.
The exact map comes from the digest after the build (GATES-20t's `decls` names every one). No wire, no fixture, no
re-genesis: proof modules only.

Under B: 0.

## 5. Gate

A: `lang:` with CROSS-LAYER: KERNEL (Kernel/Proofs/Logic/*) and CROSS-LAYER: LEDGER (Ledger/Proofs/Escrow*),
proof-only. Fast judge plus a whole-tree build (shared-module card, plan §5.6). B: `lang:` fast.

## 6. ASK

1. **The fork**: A (default), B, or C.
2. **GRANT under A**: `Kernel/Proofs/Logic/{History,HistoryWitness}.lean`, `Ledger/Proofs/{EscrowAdmitted,EscrowInvokes}.lean`,
   proof-only. R-0044 grants Lang/** + Hosting/Proofs/** + gates/tcb.tsv, which does not cover these.
3. **NanoBridge stays** (§1): confirm that PROT-1 deletes nothing there, and that PROT-3 owns it.
4. Read: Grok, per R-0044 (not a docstring).

## 7. MEASURED while the read was out (scratch; not landed; the read decides)

`run_edits_guarded`'s first half, as `runMeasuredWith_rows_guarded` (appended to `Lang/Proofs/Rel.lean`, beside its
template `runMeasuredWith_rows_under :858`). Text: `promo/PROT1/run_edits_guarded.scratch.lean`.

    runMeasuredWith … = .ok (s, calls, rows, t, n) →
      ∃ S e es, setup … = .ok S ∧ editsOf S.rels r.self e = .ok es ∧
        guardEdits bytesOf digestOf S rv pkg r es = .ok () ∧ rows = es.map (fun x => (x.slot, x.act))

- GREEN at 51089fb (`lake build Lang.Proofs.Rel`, EXIT 0).
- **Plant P1** (`promo/PROT1/plant-P1.diff`): `runMeasuredWith` computes `guardEdits` and ignores its verdict
  (`let _ := …`). Removing the line outright breaks the def's elaboration, so it is not a plant. Result: `Lang.Program`
  builds; the ONLY red is `Lang/Proofs/Rel.lean:946`, inside `runMeasuredWith_rows_guarded` (57/57,
  `promo/PROT1/plant-P1.log`). No landed theorem reds: `guardEdits_never_stuck`/`_unpinned` stay green. So today
  nothing landed says an admitted run's rows were guarded. This theorem is the first, and P1 is specific to it.
- Restored: `lake build Lang.Proofs.Rel` EXIT 0 (`promo/PROT1/restore-P1.log`). Worktree clean.
