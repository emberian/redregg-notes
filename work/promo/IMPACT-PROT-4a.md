# IMPACT-PROT-4a · the receiver is the monitor, first half (`run_edits_guarded` + `activity_monitor_safe`)

CX-PROMO-4, 2026-10-22, nano main `51089fb` (hbox `wt/promo`). Plan §3 P3 PROT-4. Rulings: R-0044 (cheap branch),
R-0046 (PROT-1 = fork B: no `ObjectStep` widening, no Kernel/Ledger port; PROT-1 folds into PROT-4; land
`run_edits_guarded` as PROT-4's first half). Grant: R-0044's Lang/**. Artifacts: `promo/PROT4a/` (candidate diff,
the new module, every plant's diff and whole-tree log, `plants.out`).

**Candidate BUILT: whole tree GREEN, 726 jobs** (`lake build`, hbox logs/promo/p4a-whole.log). Nothing landed yet.

## 1. The statements (as built)

**T1, `Lang/Proofs/Rel.lean`.** The converse of the past-extraction theorems. `runMeasured_past_extraction` /
`program_run_past_extraction` (`Provenance.lean:1159, :1214`) rewrite a run past extraction to the do-block whose last
bind is `guardEdits`. That connects the run to the guard CALL. Inverting the do-block under `= .ok` gives the verdict:

```lean
theorem guardEdits_ok (h : guardEdits bytesOf digestOf S rv pkg r es = .ok ()) :
    ∀ x ∈ es, ∃ o, guardOld digestOf rv r.self x = .ok o ∧ ∀ gl, x.decl.guard = some gl →
      runLaw S.lib (.get (.ref S.g) gl) S.state (reqData bytesOf r) (guardIn x.data o) = .ok (.ok ())

theorem runMeasuredWith_ok (h : runMeasuredWith … setup … budget = .ok (s, calls, rows, t, n)) :
    ∃ S v used c e ds left es, setup … = .ok S ∧ run S.lib … (budget - S.preparation) … = .value v used ∧
      extract S.ty … v = .ok (.record [calls c, edits e, state (.record ds)], left) ∧
      editsOf S.rels r.self e = .ok es ∧ guardEdits … es = .ok () ∧ rows = es.map (·.slot, ·.act)

theorem run_edits_guarded (h : runMeasuredWith … = .ok (s, calls, rows, t, n)) :
    ∃ S es, setup … = .ok S ∧ rows = es.map (·.slot, ·.act) ∧
      ∀ x ∈ es, ∃ o, guardOld … x = .ok o ∧ ∀ gl, x.decl.guard = some gl → runLaw … = .ok (.ok ())
```

Nano object: the run `Lang.program`'s `run` makes (any setup: closed, live). Its `rows` are what
`ObjectStep.invoke`/`.nested` bind and the kernel applies. `runMeasuredWith_rows_guarded` (CX-PROMO-3's scratch) is
superseded by `runMeasuredWith_ok`.

**T2, new module `Lang/Proofs/StdActivityMonitor.lean`.** The log row's machine as data, and the guard-grain monitor:

```lean
inductive WaitingStep lib resumer req state : Data → Data → Prop
  | start  : key.agent = .digest a → req.agent = .digest a →            -- absent → waiting, by the key's own agent
      WaitingStep (insert {key, val := {answered := none, captured := c}}) old
  | answer : Resumes lib resumer req state →                            -- waiting → answered, by the resumer,
      WaitingStep (upsert {key, val := {answered := some (l x), captured := l c}})   -- same capture, own plan
                  (some {answered := none, captured := l c})
  | retire : WaitingStep (retract {key}) (some {answered := some a, captured := c})  -- answered → absent

theorem waiting_body_step (hw : (activityCaptured plans).wf) (hv : d.val = activityLogVal plans)
    (hed : Conforms ed (relEditTy d)) (hold : Conforms old (optTy d.val))
    (h : BigStep lib ((guardIn ed old).toVal :: req :: state :: cenv)
           (lawBody (activityWaiting T plans d resumer names)) (.ok (.inj "ok" w))) :
    WaitingStep lib resumer req state ed old
```

`h` is `Admits` for ANY closure environment: the shape the receiver runs a package field in (`runLaw_ref_admits`).
That is the reason this theorem is new and not a corollary of the landed `waiting_*_iff` (`Lang/Proofs/StdActivity.lean`).
Those are stated at `activityApply W [var 2, var 1, var 0]` evaluated in the inputs' own environment, so the body runs
under a doubled environment `i::q::s::i::q::s::env`. The deployed guard runs as field `gl` of the loaded record, under
closure env `[]`, i.e. body under `i::q::s::[]`. No `env` makes those equal. They are also per input shape: retract only
over `old = some {..}`, upsert only over `old = some {answered = none}` / `{answered = some}`. **MEASURED (READ + built):
the composition does not typecheck on the landed statements.** So T2 inverts the guard body directly. They stay as
they are: they are the iff (the guard also ADMITS each step), the transparency half (PROT-4b's).

**T3, same module, run grain:**

```lean
theorem activity_monitor_safe (hid : digestOf (bytesOf pkg) = some pkg) (hp : readPackage look pkg = .ok p)
    (hb : p.body = .record fs) (hrel : Row.find? ℓ p.rels = some d) (hg : d.guard = some gl)
    (hf : Row.find? gl fs = some (activityWaiting T plans d resumer names)) (hnr : NoRef resumer)
    (hv : d.val = activityLogVal plans) (hw : (activityCaptured plans).wf = true)
    (h : runMeasured … = .ok (s, calls, rows, t, n)) :
    ∃ S es, runSetup … = .ok S ∧ rows = es.map (·.slot, ·.act) ∧
      ∀ x ∈ es, x.label = ℓ → ∃ o, guardOld … x = .ok o ∧ WaitingStep S.lib resumer (reqData r) S.state x.data o

theorem activity_program_safe … (hi : p.imports = []) (hc : p.holes = [])
    (h : (Lang.program bytesOf digestOf).run … = .ok (s, calls, rows, used)) : (same conclusion)
```

Nano object: `activity_program_safe` is over the deployed `Program.run`, the run `ObjectStep.invoke` binds (via
`runMeasuredLive_leaf_closed`). The premises are on the PACKAGE the pinned cell holds, not on a method. So every method
is covered, generated or hand-written: the Bell's `answer` (an author method upserting `rings`, `Bell.ob:11`) is a
`WaitingStep.answer` or the run did not return. Proof: T1 (`runMeasuredWith_ok`, `guardEdits_ok`), conformance of edits
and old rows (`extract_conforms`, `editsOf_conforms`, `guardOld_conforms`, as in `guardEdits_never_stuck`), the loaded
closure (`load_top`), relocation the identity (`noRef_activityWaiting`, new, with `noRef_eqDataBody`/`Fields`), then
`runLaw_ref_admits` and T2.

**Premises satisfiable at a generated package.** `activity_fixture_monitored` (`StdActivityTeeth.lean`, `decide +kernel`):
the fixture's `waits` decl is guarded by `waits_waiting`, that field IS `activityWaiting actS plans d actResumer`, its value
is `activityLogVal plans`, and the capture type is well formed. To make `hv` an equation the generator itself states,
`activityLog`'s value is now the named `activityLogVal` (`Lang/StdActivity.lean`). The term is the same, so no byte moves.

**`activity_monitor_safe` vs `activity_history_runs`.** R-0046's point holds, MEASURED: the "Reach over a per-key
machine" is `WaitingStep` read per step. The step relation IS the per-key machine's edge set with its roles. Threading
it across Turns is `rowsRun_eq` (a kernel fact about every turn, Grok §3), so a history theorem adds nothing a mutation can red.

## 2. The plants (built and run; whole-tree `lake build` under each, then restored; whole logs in `promo/PROT4a/`)

| plant | mutation (deployed) | red (by name) | landed reds | verdict |
|---|---|---|---|---|
| **P1** (CX-PROMO-3's) | `runMeasuredWith`: `let _ := guardEdits …` (guards computed, verdict ignored) | `runMeasuredWith_ok` (Rel.lean:990) | **`runMeasured_past_extraction_of` (Provenance.lean:1037) and `runMeasuredLive_past_extraction_of` (:1087)**, private, under the landed public past-extraction theorems | NOT run_edits_guarded's own tooth |
| **P1b** | `guardEdits`: a guard's `.ok (.error why)` → `.ok ()` (the guard runs; its refusal is accepted) | `guardEdits_ok` (Rel.lean:967) | **none** (`guardEdits_never_stuck`, `_unpinned`, the past-extraction family all green) | **run_edits_guarded's tooth** |
| **P2** (brief's) | `activityWaiting`: the upsert of an answered row → `okT` | — (downstream not built) | `waiting_no_replay` (StdActivity.lean:117), `activity_answer_no_replay` (Teeth) | ALREADY TEETH: not duplicated |
| **P3** | `activityPackage`: the log's decl `with guard := none` (the generated log is unguarded; the `waits_waiting` field still exists) | `activity_fixture_monitored` (Teeth:45) | **none** (every other StdActivityTeeth row and the whole tree green) | the fixture witness's tooth, NOT the monitor's (R-0047: the monitor module builds under it) |

**Correction of CX-PROMO-3's measurement (IMPACT-PROT-1 §7, R-0046's text).** "P1 reds ONLY `runMeasuredWith_rows_guarded`,
and no landed theorem" was measured on `lake build Lang.Proofs.Rel` (57 jobs), whose closure does not contain
`Lang.Proofs.Provenance`. On the whole tree P1 also reds the two private past-extraction lemmas. Grok's read §4 said
this ("the equality in `program_run_past_extraction` becomes false"). The plant that only the new chain reds is P1b:
a guard that runs and is not obeyed.

**What a plant at Rel cannot show.** Lake does not build the importers of a failed module, so under P1/P1b the
importers of `Lang.Proofs.Rel` are unchecked, and under P2 those of `Lang.Proofs.StdActivity` (including the new module).
"Landed reds: none" covers every module outside those cones. Journey rows under P1b/P3 are not measured. Under P3 the
Bell's `rings` would be unguarded, which is the behaviour the monitor rules out.

## 3. Consumers

- **audit / rederive**: a follower that re-runs a method re-runs `guardEdits`, so it re-runs this monitor. Its
  admitted edit at an activity log is a `WaitingStep`. This is the fact a member's follower trusts when it reads an
  answered ring (PROT-3's `answered_row_is_kept_answer` takes it as its kernel half: the answer is a `WaitingStep.answer`
  by the resumer, capture unchanged).
- **StdActivityTeeth**: the admitting rows (`activity_start_unanswered`, `activity_answer_once`,
  `activity_retire_after_answer`) are closed instances of `start`/`answer`/`retire`, and the refusing rows are closed
  non-instances. They stay as rows. They decide the guard on the fixture's inputs, and T2 is the general statement over
  every input. Restating them as applications of T2 would delete the evidence that the fixture's guard runs. Said in
  the module doc.
- **PROT-4b** (`activity_monitor_transparent`): the iff direction, with "the row was pinned" (LANG-58) as its premise.
  It restates the `waiting_*_iff` at the deployed environment shape (§1). Its own card.

## 4. Price (MEASURED)

- Landed theorems gaining a hypothesis: **0**. Landed theorems restated: **0**. Deleted: **0**. All declarations are
  new (21 theorems: 5902 vs 5881 by `gates/size.py`), and `activityLog`'s value is the same term under a name.
  Expected `decls` map: **0 lines** (no RESTATES / RESTATES-MEANING / DELETES / DELETES-MODULE). The judge confirms it.
- `runMeasuredWith_rows_guarded` was never landed, so it has no DELETES line.
- No wire byte, no fixture, no package id moves: `activityLogVal` is the same `Ty`, and the whole tree is green with
  the journey and codec modules unchanged. Gate: **`lang:` fast** (no `lang!`).
- SIZE: modules 476 → 477; proof-modules 252 → 253; Lean lines (Lang) 38378 → 38909; deployed 28538 → 28541; max
  dependents 346 → 347; theorems 5881 → 5902.

## 5. The landing

`lang:` fast; files `Lang/Proofs/Rel.lean`, `Lang/Proofs/StdActivityMonitor.lean` (new), `Lang/StdActivity.lean`,
`Lang/Proofs/StdActivityTeeth.lean`, `decisions/lang.md` (LANG-75.9). LANG-75.9 says why PROT-1's composition had no
object (an activity has no machine law; `ObjectStep` drops rows; nothing said a run's edits passed their guards; and the
per-key "Reach" is `WaitingStep` per step plus a kernel fact), that PROT-1 folds here under R-0046, and P1's correction.

## 6. Questions (defaults in bold)

1. **Land T1+T2+T3 + the fixture witness as one landing (default)**, or T1 alone first?
2. The doubled-environment `waiting_*_iff` statements: **leave them for PROT-4b to restate at the deployed shape (default)**.
   Restating them now would be RESTATES-MEANING ×4 with no consumer in this card.
3. Journey under P1b/P3: **not run (default; the plants' verdicts are Lean reds)**. One `lang-journey` run each if asked.


## 7. Amended per R-0047 (READ-PROT-4a-grok.md)

P1 is a correction, not a tooth; P1b is `guardEdits_ok`'s; P3 is the fixture witness's, not the monitor's; the only package decided to meet the premises is the generated fixture (the Bell is the next witness; Std.hole's installed root is outside the premises); a follower re-runs `rederive` → `receive` → `program.run` → `guardEdits`. Docstrings and LANG-75.9 say exactly this.
