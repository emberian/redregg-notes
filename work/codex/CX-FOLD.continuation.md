# CX-FOLD continuation — written by CX-FOLD run 1 (Claude) at its context ceiling, 2026-10-22 after LAND a27b2da

Next step: **S6** (map §2.1 "Deployed language", §4.2 row S6): `Lang/Index.lean` (upR, liftIdx, lowerIdx out of
`C/Core`), `Lang/Subst.lean` (`C/LangSubstitution` + the term half of `C/LangCalculus` + `Term.nodes` from
`Lang/HoleBudget`; namespace `Nanodregg.Lang`; DELETE `ΔOf`/`holeBound` and, in S6 or with P/LangInstance, their three
lemmas), `Lang/HoleDecl.lean` (from `C/HoleDecl`). Host closure 91 → 89 expected. Write IMPACT-S6.md first, READY-IMPACT,
poll RULINGS.tsv. S6 is a MOVE: the rename map is part of the digest diff (every surviving name equal or in the map's image).

## State on main (all fast-judged GREEN, pushed)
f665e94 S1 (13 modules) · 82ac944 S1b (audit_append → Kernel/Proofs/Audit.lean; SpentCheckpoint +
recovery_preserves_consumption → Host/Proofs/SpentCheckpoint.lean; R-0006) · 6eb92fe S1c (Integration) · a9ab514 S2
(journey p8 toy dropped; FINDING: withdrawn-provider tombstone commit is ADMITTED, cv task 01a16171-d004) · e1ccc50 S3
(11) · a747368 S4 (14 + Trace.lean:125–126 doc) · a27b2da S5 (5 + Closure exp-4 Rule/lfpIter/supportCount/countRun +
ClosureStatements ValueGuard/StableUnder/Derives, pulled forward from S10 by R-0010). decisions/lang.md: LANG-74,
LANG-74.1, .1b, .1c, .2, .3, .4, .5 (erratum for LANG-72×2/71/70 is in LANG-74). Rulings ACKed: R-0001..R-0010.
Consequence for S10: the experiment-4 deletion is DONE; S10 is now only the provenance twin (P9 replaces the
env-specialized one; P/ProvenanceTeeth goes).

## Tools (hbox, all mine, scratch only — never landed)
- Worktree `/tank/dregg-build/nanodregg/wt/cxfold` (at a27b2da, clean except untracked logs/), own `.lake`, CARGO_TARGET_DIR=wt/cxfold/target.
- `/tank/dregg-build/nanodregg/logs/cxfold/`: `mkdigest.sh WT OUT.tsv DELMODS` (imports every non-exe module of the 11
  libs, writes name/module/kind/quoted type/value hash/refs-to-declared-set; uses Census.Journal.expressionEdges);
  `diff.py BEFORE AFTER DELMODS` (prints at most 40 names — use a full listing when a reader needs exact names, as
  R-0010 did); `pp_cmd.lean` (#fold_pp: user decls of declared modules with ppExpr statements);
  `grepnames.py TAG`, `grepsuffix.py TAG`; `step.sh TAG` (the whole pure-deletion measurement, restores the tree).
  For a MOVE step, diff.py needs a rename map (extend it: map old→new names, compare digests after substituting
  names, as S1b's `S1b-eq.lean` did with Expr.replace).
- Whole-tree build: `SWARM_MEM_MAX=16G LEAN_NUM_THREADS=2 swarm-build lake build Lang Kernel Ledger Census Host Hosting
  Protocol Codec Emit Bench Ops [host lang-journey]` (~minutes warm); journey: `.lake/build/bin/lang-journey` (6 s).
- Landing: append decision to decisions/lang.md, `python3 gates/size.py --write . && python3 gates/check.py .`,
  `git checkout -- SIZE.md`, then `nohup bash -c "exec scripts/commit -F MSG PATHS..." > logs/cxfold-SNland.log 2>&1 &
  echo $! > logs/cxfold-SNland.pid` and foreground-wait on the pid.

## Lessons that cost something
- Replace every toy row with its REAL call before deciding what to keep (S2 found an admission the toy said refused).
- Read the statement list whole; a pure-deletion read misses non-restatements (S1: Integration's two deployed facts).
- Check which definitions lose their LAST theorem in a deletion step and delete them with it (S5).
- Comment-only `/- -/` edits leave oleans identical (lake rebuilds only the edited module); `/-- -/` docstrings change it.
- Cross-family reads arrive as fold/READ-Sn-grok.md + a RULINGS row within ~10–40 min.
