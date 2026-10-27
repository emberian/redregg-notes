# How we work on nanodregg (real 2026-10-27; replaces LANE-RULES-NANODREGG.md's 18 rules and every gate instruction in briefs)

Ember: development rapidity and product excellence. A lane's value is what the system can DO after it that it could not before.

1. A LANDING IS: rebase on origin/main; build what you changed (the modules your diff touches and their dependents); run the tests and journeys your change touches; push to main. That is the whole gate. Minutes, not hours.
2. The commit message says what changed and what it lets the system do. It is prose, not a form: no map lines, no SIZE lines, no CROSS-LAYER lines, no plant lines, no owners rows.
3. Validation of the WHOLE is a periodic report: `scripts/converge` (or its successor) builds the tree, runs every row and test, and TELLS what is red and which landing it came from. It never refuses a landing and never reverts; a red is a task for the lane that caused it, fixed forward.
4. There are no judge slots and no displacement. If main moved, rebase and push; if the rebase conflicts, resolve it. A push that fails because main moved again is retried, not re-judged.
5. Censuses, pins, ceilings, vector tables, the TCB table, waste ratios: if any still exists it is a REPORT a human reads at the convergence, never a gate. Delete the ones nothing reads.
6. Decisions: decisions/<layer>.md stays append-only and critiqued, because Ember asked for critiqued decisions on 10-16; one entry per real design choice, not per landing.
7. Box safety is unchanged and verbatim in every brief: never kill by pattern; PID file or nothing; never `git stash`; never an unfiltered test suite; never delete outside your own scratch; builds under swarm-build at a lane budget (6G a module, 24G a tree); every build at idle I/O (`ionice -c3 nice -n 15`); every build, development or landing, takes one of the box-wide build slots (`flock ~/nd-land/.locks/build-K.flock`, K in 1..6, the same slots scripts/commit uses) so that fifteen lanes cannot run fifteen tree builds at once; the box is shared with Mini.
8. A brief carries the goal, the material (paths, the design, the report to append to), the box-safety block, and rule 1. Nothing else about process.
9. One agent per worktree; a successor starts from the predecessor's own continuation after the predecessor is finished.
10. HOW A LANE BUILDS: reason across the whole change first, build once (two builds per landing is the norm; a build per statement is forbidden); single-file checks while iterating; no private copies of the build (the shared warm tree + `scripts/nd-check`); rebase once at the end; land small, soon; no sub-forks. The full text: METHOD-20261027.md.
11. When a process constraint appears, the first question is "do we need this at all?", never "how do we make it faster?". When a lane spends more time landing than building, the gate is the defect.
