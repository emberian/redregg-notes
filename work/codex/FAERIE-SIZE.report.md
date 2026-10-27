# FAERIE-SIZE report (2026-10-27)

## (1) size_limit (cv 01a17e6b-e2c4) -- LANDED 7fe2a1e8 on origin/main, GATES-31
Cause: gates/size_limit.py already used `git ls-files`, but only when `<root>/.git` exists. The convergence judges a
`materialize` export (`$common/nanodregg-standing/tree`, no .git, index at `tree.index`), so it fell back to a disk walk
and named the gitignored testground/kernel.wasm.
Fix: no .git + sibling `<root>.index` inside a git dir => `git ls-files` with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE from that
index; a checkout uses its ls-files; only a bare dir (the plants' control trees) is walked.
Plant (gates/size_limit_plants.py): in an export, an untracked 5 MB file is not named and not red; a tracked 1048577-byte
file is red by name. `python3 -I gates/size_limit_plants.py` green; the real gate reads ok on c0c5979.
Decision line: decisions/gates.md GATES-31. Pushed with plain `git push origin HEAD:main` (rule 1; Python/docs only).
Caveat: the export's index is found by convention (`DIR.index`, an ancestor named `.git`); otherwise it silently falls back to the walk (said in the Critique).

## (2) rows --deployed forgotten (cv 01a17e6b-e2f3) -- PASS, task marked done as load
Invocation: `nd-build lake exe rows --deployed forgotten` in the standing tree on hbox (nd-build from ~/nd-land/warm/scripts;
`~/nd-land/warm` is at c0125a31 with no scripts/warm, so the standing tree built 12:34 was used; no .lake copied).
Started 14:19:31Z at 1-min load 10.50 (waited ~40 min for <12, PID-filed loop). Result: `ROW forgotten PASS (plant ...forgottenRefused
caught at line 13: refused forgotten)`, ALL PASS, COST frames 35441 steps 3217. Wall 482 s including the nd-build slot wait
(all 6 slots busy at start) and lake startup; the plant itself held its 300 s deadline. Deadline unchanged. Log:
hbox ~/nd-land/faerie-size/rows.log. Note: the row prints no own time, so the plant's pure time is only bounded (<300 s).
