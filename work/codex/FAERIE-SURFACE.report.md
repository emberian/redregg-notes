# FAERIE-SURFACE report (2026-10-27)

Landed: `0ef740b1` on nanodregg main (one commit, rebased over af3248d8; no file overlap). hbox worktree `~/nd-land/faerie-surface`.

| item | status |
|---|---|
| 1. checked hole reads back (LANG-106) | done. `hasType_wf`/`hasType_canon` (+ fields/arms) generalised to any hole signature of wf types; new `substTy_canon`; `holeCheck_printable`, `checkContextual_facts`, and the composed `readPackage_checkedContextual` (`Lang/Proofs/PrintWire.lean`): checkContextual ok + `package p = some s` gives `readPackage s = ok p`. The install check guarantees HolePrintable for every shape; nothing to file. Caveat in LANG-106: the theorem is "if it prints, it reads back"; no theorem yet says a package with holes prints within bounds. |
| 2. ob names the line of an ill-typed candidate (LANG-107) | done. `Lowered.sites` (guard and candidate offsets); `checkLowered` appends `line N` for `holeGuardType` and `holeCandidateType`. Rows RM17 (`refused holeCandidateType 0 1 line 8`) and RM18 (`refused holeGuardType 0 line 7`) in `Lang/Journey/Readme.lean`. Not covered: a body ill-typed at the hole signature (`holeBodyType`) still names no line. |
| 3. `(createOf T)` in surface (LANG-108) | done. Slot kind `(createOf T)` (and combined with `(invoke A)`), item `(createOf (pkg e) (state e))`, `callKinds`, grammar text, spec 2.9.4 line. Reader/printer needed no case (call is an inj; core text already round-trips), so no statement changed. Row GN25 (`Lang/Journey/Gen.lean`): a surface-text creator installed, created, invoked; Turn bears B's owned object then the package; same text with an `install` slot refused `callKind createOf`. README unchanged (its `spawn` rightly generates by `install`). |

Verification: `lake build Lang lang-journey ob` and `Hosting Ledger Web Bench` green; `lang-journey` GREEN default, `--contextual`, `--contextual-checks`, `--hole-omitted-blocker-pin-admits`; `--harness-control` RED (1), the control. `ob` binary builds. No sorry in PrintWire. Not run: the row runner / scripts/commit full gate (pushed by hand per rule 1).

Decisions: LANG-106, LANG-107, LANG-108 in `decisions/lang.md`. Broke: `Surface.Lowered` gained a defaulted field; nothing re-emits.
