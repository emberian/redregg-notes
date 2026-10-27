# FABLE-TRUST — continuation (real 2026-10-27, written by TRUST-5)

Read first: `redregg/work/codex/FABLE-TRUST.report.md` (TRUST-5 lines), `redregg/work/METHOD-20261027.md` (Ember's new method:
reason across the whole change, single-file checks while iterating, two builds per landing, rebase once at the end, land small and soon,
no sub-agents), `redregg/work/WORK-RULES-20261027.md` (rule 1), DESIGN-TRUST §4.4c and BUILT-10. Worktree:
`hbox:/tank/dregg-build/nanodregg/wt/fable-trust` (scratch in `.trust5/`; it is at origin/main `276ba794`, detached HEAD).

## State
- LANDED by TRUST-5: `276ba794` (KERNEL-79 + PROTOCOL-86 + HOSTING-61): certify-key pre-rotation inside the World, certificates carry
  signer keys (`Head.holds`), keygen/rotate-certifier, serve's inline start certification.
- `rows --deployed` row `refused` runs ~7m45s alone at load ~22, past its 300 s per-row deadline: the wall-clock class (cv 01a17c7f-abf4).

## Next, in order
1. cv 01a17e0d-0ea6: a stranger (and a far-behind follower) follows MORE than one rotation: carry the signed rotation acts beside the
   genesis input (`Certified.check` over input + rotation chain + certificate); a missing chain is named unchecked, not refused.
2. cv 01a17d16-e71d: every signed call carries its signer's head (operation-level fork*). The mechanism is not a fork; "fork or fork*"
   is Ember's (cv 01a17de0-1222). Do not build fork*.
3. cv 01a17d57-5546: a behind comparison the Store cannot answer is named (`uncheckedBehind`).
4. T3c pinless adoption still waits on `allowance` under `rootsDigest` (cv 01a17a55-5e88).

## Rules kept
Never kill by pattern; PID file or nothing. Never `git stash`. Filtered tests only. Delete nothing outside the worktree and scratch.
Every build takes a box slot. A deferral goes into `cv task` first.
