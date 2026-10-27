# GLM-B — Verdict.name collisions (cv 01a17d72, SPEC-DOCS kernel item 9)

## 2026-10-27

- Read: work/WORK-RULES-20261027.md (14 lines, whole), work/codex/SPEC-DOCS.report.md item 9,
  cv task 01a17d72 body, docs/reference/kernel.md (no occurrences of the three names —
  the reference does not list them), decisions/kernel.md entry format.
- Measured (local clone 80c622a and worktree 8fe58cbf, by grep of both name tables):
  `Verdict.name` (Kernel/Receive/Submit.lean:114) delegates to `Refusal.name`
  (Kernel/Receive/Call.lean) and `Reject.name` (Kernel/World.lean); the tables share exactly
  `missingCell`, `rangeTooLong`, `duplicateRow`. No other pair collides (checked again by
  #eval below after the rename machinery was in place).
- Inferred, not measured: a member reading a refusal record by name cannot distinguish the
  tables — this is the spec lane's finding (SPEC-DOCS item 9), taken as given from the task
  body; the code path (`codeName` answering `refused NAME`, `refusedOf` able to record a
  `.rejected` verdict, Kernel/Sim/Gen.lean:2070) corroborates it.
- Choice: renamed the REJECT side (constructor + wire name together, preserving law-7
  "name = constructor, arguments dropped"): missingCell→absentCell, rangeTooLong→rangeOverMost,
  duplicateRow→duplicateRowSlot. Refusal names untouched — they are what rows/journeys/sim
  assert (Protocol/Rows.lean:1526, Lang/Journey/Inbox.lean:178, Kernel/Sim/Gen.lean:1468/2040/2046).
- Sites updated: Kernel/World.lean (decls 3, name table 3, raise sites 1072/1076/1420/1449,
  docstrings 677/1407/1437/1461), Kernel/Receive/Submit.lean (rejectNames), Kernel/Proofs/Admit.lean:409,
  Kernel/Proofs/Rows.lean:688, Kernel/Proofs/InvokeTree.lean:989, Kernel/Turn.lean:101,
  Kernel/Sim/Gen.lean:2070, decisions/kernel.md (KERNEL-79).
- Check kept as a theorem: `Verdict.name_injective` (one wire name determines one code), in
  Kernel/Proofs/Refusals.lean next to `codeName_code`, the two-table form of the existing
  `Refusal.name_injective`/`Reject.name_injective` (constructor-carrying data makes literal
  injectivity false; the codebase's own convention is name→ctorIdx, and `Verdict.code` is the
  row index across both tables).
- (fill: #eval before/after results)
- (fill: builds, tests, emit check, hash)

ROOT (real 10-27): NEW METHOD, effective now: read /Users/ember/dev/redregg/work/METHOD-20261027.md. Reason across your whole change first; write all edits; ONE build; fix everything from its log; build again; a build per statement is forbidden. Single-file checks (`scripts/nd-build lake env lean FILE`) while iterating. Do NOT cp -a a .lake (disk at 93%): if you have no build yet, write the code and wait for scripts/nd-check (within the hour). Rebase once at the end. Land small, soon. Spawn nothing.

ROOT (real 10-27, Ember): if you are STUCK on a proof (a theorem that resists after one honest attempt per METHOD §1), do not grind: write the exact state (statement, error, the lemma you think is missing, files touched) into this report, land whatever else is green, and stop; an Opus lane takes the proof from your report.
