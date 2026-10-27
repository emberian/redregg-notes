# Common brief for CX-PROMO-8's helpers (written by CX-PROMO-8, 2026-10-23)

Repo: nanodregg. GitHub origin emberian/nanodregg is the truth. Build box: `ssh hbox`, primary checkout
/tank/dregg-build/nanodregg/main (a build box, read-only reference). Main is at c57603d or later.

METHOD (RULINGS R-0069, Ember): a card lands when YOUR build + plants are green, fast judge, no IMPACT
file, no cross-family read, no waiting for ROOT. Land with `scripts/commit -F MSGFILE PATH...` run from
your worktree (it reads current main into a private index, judges FAST for a `lang:` subject, CAS-lands
and pushes to origin). Never use a `lang!:` subject (it forces the 40-min full judge). Before landing:
`git fetch origin`; if your worktree's HEAD lags origin/main, rebase onto it.

YOUR WORKTREE: create it yourself:
  git -C /tank/dregg-build/nanodregg/main fetch origin
  git -C /tank/dregg-build/nanodregg/main worktree add --detach /tank/dregg-build/nanodregg/wt/NAME origin/main
  cp -a /tank/dregg-build/nanodregg/wt/promo/.lake /tank/dregg-build/nanodregg/wt/NAME/   # warm start (real copy, never cp -al)
Never edit wt/promo (CX-PROMO-8's) or main. Logs under /tank/dregg-build/nanodregg/logs/promo/p8/NAME/.

BUILD: `cd WT && SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build TARGETS` (whole tree: no
targets). FOREGROUND-wait every build (a backgrounded build you "wait to be notified about" strands you).
Journey: `lake build lang-journey && ./.lake/build/bin/lang-journey > FILE` (must end `lang-journey: GREEN`).
Edit files by writing them locally and `scp` (apostrophes inside ssh quoting break inline python).

WHAT THE FAST JUDGE NEEDS IN THE MESSAGE (learned by refusal; read CX-PROMO-8's landed messages with
`git log -3 --format=%B` for the shape):
- one `SIZE: <exact metric name>: <why>` line per RISEN metric of SIZE.md. Measure:
  `python3 gates/size.py . --write; git diff SIZE.md; git checkout HEAD -- SIZE.md`.
- GATES-20t map lines: every declaration the landing deletes or restates named `DELETES: <full name>` /
  `RESTATES-MEANING: <full name>` / `RENAMES: a -> b`. Get the list by running the decls judge with a
  one-line message before landing: CX-PROMO-8's script /tank/dregg-build/nanodregg/logs/promo/p5/decls.sh
  (usage: `decls.sh OUTDIR /abs/msgfile PATHS...`; it judges your uncommitted PATHS against HEAD; it
  `cd`s to wt/promo, so COPY it and change that line to your worktree).
- `PLANT: <name> -> <what went red, by name>` lines and a `MEASURED:` line; and the three flag-day
  sentences (WHAT CHANGED SHAPE / WHAT RE-EMITS / WHAT NOW REFUSES).
- the decision text appended to decisions/lang.md under your assigned `### LANG-75.N` number, with
  Decision, Price (measured), Plants, Critique and a Meta-critique naming a BIAS (read LANG-75.16-18 at
  the end of decisions/lang.md for the shape). End the commit message with
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

PLANTS: each claim gets a plant that makes a NAMED thing red (a theorem by name, or a journey row by
name), run on the whole tree, reverted byte-identical (cmp the file against a kept copy). A plant that
reds an upstream module leaves its importers unbuilt: say which cone was unchecked, or plant at a site
the upstream proofs do not unfold. A plant that changes a constructor's arity breaks proof scripts, not
statements: keep the shape (`∨ True`, a swapped field). Ask which layer refuses first (the kernel's
`sameAccount`, `belowFloor`, grant checks run before or around Lang code).

STATEMENTS: no vacuous or tautological theorems (no `P → P`, no disjunct provable from the premises, no
conclusion the premises already contain). A theorem's docstring is at the strength of its statement.
No `#guard`; use named theorems. No `sorry`, no new axioms.

BOX SAFETY (verbatim): Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no
`killall`, no `kill -u`. A process you started is stopped by the PID in its PID file, and only that; no
PID file, no kill. Never `git stash`. Never run an unfiltered `-p <crate>` test suite. Never delete
anything outside your own worktree/scratch. Disk pressure: stop writing, report, wait.

REPORT: append one line per event to /Users/ember/dev/redregg/work/codex/CX-PROMO.report.md starting
`<UTC time> CX-PROMO-8/<NAME>` (LAND <hash> ... / RED ... / BLOCKED ...). Close your cv tasks with
`cv task done <id> --note "<hash>: <one line>"` (check `cv task --help` for the exact form). Your final
message: the hashes landed, the theorem statements (names + one line each), the plants and their reds,
and anything left open (filed with `cv task open --repo /Users/ember/dev/nanodregg --issue <file> --body ... "TITLE"`).
