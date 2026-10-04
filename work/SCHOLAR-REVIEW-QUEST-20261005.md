# Scholar review quest (2026-10-05 morning) — you are being sent back to the front

Ember: "wanna sendmessage those halted scholars to review what actually got done and say their piece /
make substantive edits and changes (to any docs or they start impling)?" You keep the context you built;
use it. Do not redo your census; spend your attention on judgment and change.

## What happened since your report (read these)
- Design: /Users/ember/dev/redregg/designs/MINI-PROGRAM-MODEL-20261004.md (scribe-written from the root's
  decisions); /Users/ember/dev/redregg/work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md (decisions A–I, the root's
  resolutions of 13 scribe notes, 4 OPEN questions for Ember); fn: /Users/ember/dev/redregg/designs/
  MINI-FN-660-REQUIREMENTS-20261004.md + work/FN-CHECK-20261004.md + work/FN-660-RESPONSE-20261004.md.
- Landed on GitHub main (now 36fca3ac; ledger /Users/ember/dev/redregg/work/SWARM-LEDGER-20261004.txt has
  one line per landing): the cut + Gen-1 and ALL BendTT deleted; proved fast Lean machine (csimp); first
  native Objective Accepted (796d7d7a: tariff from a signed envelope, pinned elaborator, named refusals,
  Core4 disableable, 13 refusals); activity kernel (Kernel/ObjectiveActivity, AnswerSlot,
  ObjectiveActivityWire, ObjectiveResumeContract: consume-once, stale reads -> Conflict, measurement-free
  refunds; scratch-world demo); receiver collapse first family (Theory/Kernel Receiving); ZK truth
  (LayoutCodec, docs/ZK.md); proof engineering (AxiomPin, statement snapshot, vacuity probes, Preservation
  split, StepCases); tenancy step B (mini-keys broker); hybrid PQ (native/hybrid_kem.rs); SDK on the Lean
  intent codec; client dedup; SPK failed-START recovery wired; Byzantine harness; contracts refinements,
  CertF, Simplex reconfig (research). Running now: agreement, schema v2, elaborator (Lean becomes THE
  implementation), activity native route (ownership, Book fees, GC at yield), DEPLOY-3 candidate, native
  exercise (never-run paths + the TOOTHLESS ledger row).

## Your quest
1. Review, in YOUR domain, (a) the design doc and the root's decisions/resolutions, and (b) the landed code
   on main (fresh read-only clone of https://github.com/emberian/minidregg.git, or `git show` the commits).
   Read the code, not the commit messages.
2. Write /Users/ember/dev/redregg/work/REVIEW-<YOUR-NAME>-20261005.md (<= 2,500 words): what the design and
   the code got right; what they got WRONG or MISSED against your evidence (cite your report and the
   primary sources); for each design section you dispute, REPLACEMENT TEXT the design scribe can paste;
   your answers to the 4 OPEN questions where your domain bears on them, with the strongest evidence.
3. Do NOT edit designs/MINI-PROGRAM-MODEL-20261004.md yourself (the design scribe merges proposals; one
   writer per file). Exception: the fn scholar owns designs/MINI-FN-660-REQUIREMENTS-20261004.md.
4. If your review finds a defect or a small, well-scoped improvement in landed code in your domain, you may
   implement it: clone with the hbox warm base (`ssh hbox /tank/dregg-build/claude-lanes/warm-base/mk-lane.sh
   <your-lane>` creates /tank/dregg-build/claude-lanes/<your-lane>/src, base 9ccd6a2d; then
   `git fetch https://github.com/emberian/minidregg.git main` and rebase onto it), build with
   `swarm-build env LEAN_NUM_THREADS=4 lake build <targets>` (full gate: Minidregg +Host.Main:leanArts
   ObjectiveProofs), commit on lane/<your-lane> (unsigned, `-c commit.gpgsign=false -c user.name="ember
   arlynx" -c user.email="cmrx64@gmail.com"`), never push; the root lands it. Bigger changes: describe them
   as a QUEST you would take next (scope, modules, acceptance check), and the root will send you back.
   Binding rules: /Users/ember/dev/redregg/work/LANE-PROTOCOL-20261004.txt (no git stash; filtered tests;
   swarm-build on hbox; never touch live worlds, the mesh, /tank/fn; disk: stop if a disk is under 10%).
5. Final message (<= 500 words): your verdict in three sentences, the review path, any commits (ids,
   evidence class), and the quest you want next.
