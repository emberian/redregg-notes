# FAERIE-HOLES report (2026-10-27)

Landed: `d13fb797` on nanodregg main (one commit, rebased over 276ba794; decisions/lang.md conflict with an unnumbered GLM-A entry resolved by keeping both). hbox worktree `~/nd-land/faerie-holes`.

| item | status |
|---|---|
| 1. package with holes prints within the wire (LANG-109) | done, with three stated premises. `holeROM_prints`, `holes_prints`, `package_prints_contextual` in `Lang/Proofs/PrintWire.lean`: checkContextual ok + wire-valid + tree fits => `(package p).isSome`. Premises the wire does not give: (a) each hole's context length + 1 <= listMax, (b) each candidate's supports length + 1 <= listMax (wire bounds those child lists only by nodeMax), (c) the body's text fits `Wire.depthMax` (not derivable from its tree: `(hole n (subst ..))` is one tree node but two text lists). `package_fitsB` now takes a tail of <= 3 sections (was 2). No existing statement changed. |
| 2. holeBodyType names its line (LANG-110) | done. `holeSite` uses `Surface.locateField l e.path` for `.bodyType`; no new site needed (`Lowered.sites` unchanged). Row RM19 in `Lang/Journey/Readme.lean`: `refused holeBodyType operands @bump.body.body.body.body.state.count line 10`. |

Follow-up (not filed in cv): premises (a) and (b) are better as a `HoleROM.check` clause refusing lists past listMax, which would discharge them; (c) needs a hole-aware `Prints` bound.

Verification: `lake build Lang lang-journey ob` green (364 jobs) after the rebase; lang-journey GREEN in default, --contextual, --contextual-checks, --hole-omitted-blocker-pin-admits. Broke: nothing re-emits.
