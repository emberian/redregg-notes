# PORTS-A (ab4d720376db89000, sonnet) -- resume note
Where it was: "Now the activity-run rows of the bounty cohort, and the check-preview tool." / "Set up a runner script and a baseline with the bounty cohort." Mission: port standing dues + sealed-ballot vote as Objective worlds (briefs: work/BREAD-TRANSITION-MAP-20261005.md, WORKER-BRIEF-20261005.txt).
Lane: burst-lane1 ember@162.43.189.7 /srv/lanes/ports-a/src, on local branch `main` @440322de (no commits). Untracked: world/dues/StandingDues.obend + world/dues/preview-cohort.json (the work), world/bounty/ (copy of the board that has since landed as 35c8ccb5), testing/__pycache__.
WIP branch: lane/ports-a-wip @60e3043d (4 files, +4925; includes the bounty copy). Runner: /srv/lanes/ports-a/run-cohort.sh world/<name> (bun tests/objective-bend-source/check-preview.ts); outputs /srv/lanes/ports-a/out/dues-175637-*, dues-175708-*, dues-175950-* (Capacity, DuesActivity* dirs = it ran).
Builds: none (no lake builds; cohort runs only, result not read here; check out/dues-175950-*).
Main since pause: 17 landings since 440322de; world/bounty/BountyBoard.obend landed (35c8ccb5) -- delete the untracked copy before rebasing. Sealed-ballot not started.
Bundle: persvati:/home/ember/workbox/claude-lanes/bundles/ports-a-lane1.bundle (prereq 440322de; refs lane/ports-a-wip, main).
Next step: `git checkout -b lane/ports-a lane/ports-a-wip`-style continuation: rebase on github/main dropping world/bounty, run run-cohort.sh world/dues until the preview cohort passes (+ mutants red), then start the sealed-ballot world; commit with the gate files.

Written by FAIRY-RESUME 2026-10-04 ~18:40Z. main = github/main 66e3c5b5 (== burst-gate /srv/warm-base/src; umbrella green: /srv/warm-base/logs/green-66e3c5b5.log rc=0 18:21Z). Pause was ~18:00Z (usage wall). Boxes die 2026-10-05T15:55Z. Bundles are THIN (need prereq on main).

## VISIT (VISIT-C, 2026-10-04 ~19:20Z; main = d27d1cad)
- VERIFIED: lane1 /srv/lanes/ports-a/src was on local `main`@440322de, no commits. The work is untracked world/dues/
  (StandingDues.obend 18608 B, preview-cohort.json 49 rows), byte-identical (md5) to the agent's scratchpad copy:
  nothing unsynced. world/bounty/ was byte-identical to main's 35c8ccb5 files. Nothing of dues or sealed ballot is on
  main. The only landing since 440322de that touches this work is Compiler/ObjectiveBendElaborate.lean (the front end).
- PREPARED: removed the identical bounty copy (also kept in lane/ports-a-wip@60e3043d, unchanged); new branch
  `lane/ports-a` = d27d1cad (fast-forward); world/dues/ still untracked in the tree.
- CHECKED: dues cohort run against the WARM-BASE oleans (d27d1cad; this lane changes no Lean, so it does not build):
  **PASSED, 49/49 rows** (30 source rows, 9 value rows, 10 activity rows; refusers "capture identity", "typing budget";
  suspensions ticks/capacity). Log /srv/lanes/ports-a/logs/visit-dues-cohort.log, out
  /srv/lanes/ports-a/out/visit-dues-190758-112818 (about 4 min at nice 10).
  ⚠ The lane's own run-cohort.sh takes LEAN_PATH from the lane's .lake, which is now STALE (the elaborator changed on
  main). Use `/srv/lanes/ports-a/visit-cohort.sh /srv/lanes/ports-a/src world/<name>` (warm-base oleans).
- VERDICT: **READY**.
- NEXT 1-2 h (burst-lane1, no Lean build, no slot needed): (1) planted mutants: one refusing dues row changed to
  accept, and one wrong `expected`, each turns the cohort red (logs); (2) commit world/dues/ as one commit and queue
  it in MERGE-QUEUE.md; (3) start the sealed-ballot world (collective choice; read world/collective/CollectiveAdoption.obend
  first) with its own preview-cohort.json.
- DEPENDENCIES: none blocking. PORTS-B's world-cohorts gate row (W08) will pick up world/dues/preview-cohort.json once it
  is committed: tell PORTS-B (a4149be24e2ee7578) the row count, 49. W10 BOUNTY-NATIVE (workboard) must not touch dues.
