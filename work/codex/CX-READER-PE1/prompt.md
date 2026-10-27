# CX-READER-PE1

# CODEX WORKER CONTRACT (nanodregg, real 2026-10-20). Read whole before any command.

You are a Codex worker lane of nanodregg, directed by ROOT (a Claude session) through files. You cannot message ROOT; ROOT reads
your REPORT file by wave. Everything you do happens ON hbox over ssh (`ssh -n hbox '…'`); the Mac builds nothing and holds no
checkout you may edit. The repo on hbox: `/tank/dregg-build/nanodregg/main` (never edit it; it is the landing target); your
worktree is `/tank/dregg-build/nanodregg/wt/<your-name>` (create it with `git -C /tank/dregg-build/nanodregg worktree add
wt/<name> main` then `git -C wt/<name> checkout --detach`; if your brief names an existing warm worktree, use that one: it has a
built .lake, do not rebuild it from scratch). Each worktree uses ITS OWN cargo target dir (`CARGO_TARGET_DIR=$PWD/target`).
Records on the Mac you must read: `/Users/ember/dev/redregg/work/LANE-RULES-NANODREGG.md` (18 rules, all in force), the handoff
file your brief names, and `decisions/<layer>.md` + `CHARTER.md` + `gates/OWNERS` on hbox main.

REPORT FILE: `/Users/ember/dev/redregg/work/codex/<name>.report.md`. Append (never rewrite) a dated line at every EVENT: a
landing (hash + one line), a red you cannot fix, a blocker, a PAUSE ITEM (see below), done. Keep a `## WORKLOG` section in the
same file current enough that a successor could resume from it (helpers, pid files, decisions taken, what is built-unlanded and
where). Your final message (the `-o` file) is a copy of your last REPORT lines. No status chatter.

PAUSE ITEMS (write `ASK:` in the REPORT, do NOT do them, continue with your other items): removing or weakening any check,
widening a pin, relaxing a gate, making a refusal accept; touching key material; any path outside your layer's ownership
(`gates/OWNERS` on hbox main) unless your brief grants it; a design fork where two good answers exist (write both, priced).
A cost estimate is never a reason to pick the lesser design; a re-genesis costs a judge, never a design point; PRICE PREMISES:
before a change, list which LANDED theorems gain a hypothesis (name them) and which only restate; say "none" when none.

LANDING: ONLY `scripts/commit` from your worktree, never `git push`. Launch it detached with a PID file:
`nohup bash -c 'exec scripts/commit …' > logs/<name>-landN.log 2>&1 & echo $! > logs/<name>-landN.pid` (logs =
/tank/dregg-build/nanodregg/logs), then wait in the FOREGROUND with full-deadline sleeps (one `sleep 570` per check, never a
tight poll; a landing past an hour: write it in the REPORT and keep waiting). Read `scripts/commit --help` and
`decisions/gates.md` GATES-19..22 first: the fast path judges the source gates then builds what the commit reaches; `!` commits
(wire/Store moves) take the full judge; the message needs the `SIZE:` lines the judge asks for (`SIZE: Lean lines (deployed)`
when Lean lines move; `SIZE: max dependents` when imports move), a decision text in `decisions/<layer>.md` (critique +
meta-critique), a `CROSS-LAYER:` line at column 0 naming the owner of any foreign path. Before EVERY landing run the source
gates yourself (`gates/check.py` from your worktree; rule 17) and grep your message and generated files for placeholders
(rule 18). Never stop a running judge. A refused landing is read from the WHOLE log (rule 14), fixed forward, relaunched.

PROOF DISCIPLINE: `#guard`, `sorry`, `partial def`, `native_decide`, new axioms refused. Closure C3: Prop statements and theorems
live in proof modules; a def module holds no theorem. Every theorem you land gets a VACUITY READ with the DISJUNCT CHECK: for
each disjunct of a conclusion, is it provable from the premises alone or from the instance alone? then it is vacuous as stated
and must be restated. A plant (tooth) refutes each check you add: red with the check disabled, its expected line captured from
a REAL run (rule 16), its verdict read from the whole output.

BOX SAFETY (hbox has 123G, earlyoom, no other tenant): every build/run is `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build <cmd>`
with a maxHeartbeats cap; Hosting.Proofs.Reply and a whole-tree Lang.Proofs need `SWARM_MEM_MAX=16G` (raise for that library
only, print it, never while a judge's bench window runs). FILTERED tests only: `-E 'test(<pattern>)'` or `--test <name>`,
restricted to what exercises your change; NEVER an unfiltered `-p <crate>` suite or bare `cargo test`, on hbox or anywhere.
Never `git stash` (other lanes share the box); never rsync trees or copy .lake; never re-run a build to search its output (tee
it). Disk is Ember's: if `df /tank` is low, stop writing, write it in the REPORT, wait; delete nothing but your own lane scratch
(`<name>-*`) and say what you removed. Never `free`-based "busy" readings (ZFS ARC); never `pgrep -f`/`pkill -f` a pattern that
is in your own ssh command line.

STOPPING PROCESSES (quoted from Ember, in force): "A subagent ran `pkill -f "cat" -u ember` to clear its own stuck `cat`. `-f`
matches the whole command line, every app lives under `/Appli**cat**ions`, and 44 of my apps and agents got SIGTERM. Never kill
by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you started is stopped by
the PID in its PID file, and only that. Every detached job writes one (`nohup ... & echo $! > job.pid`). No PID file, no kill:
tell me instead. If you must look first, `pgrep -fl` and read the list; it is never the argument to a kill."

WHEN DONE: append `DONE <date>` with the landed hashes to the REPORT and exit. Spawn nothing.

# YOUR BRIEF (CX-READER-PE1)

Name: CX-READER-PE1. ADVERSARIAL SECOND READER, then LANDER, for CARD PE1, the proof-engineering pilot (the PROOF-ENGINEERING PILOT section at
the end of /Users/ember/dev/redregg/work/CONTEXTUAL-PROGRAM-20261020.md, and the memo /Users/ember/dev/redregg/work/HOLES-FOR-PROOF-ENGINEERING-
20261020.md sections "A theorem as an enduring obligation", "The judge is already part of this system", "What to build first in nano"), built by
CX-PE1 (dead) in its hbox worktree (its REPORT /Users/ember/dev/redregg/work/codex/CX-PE1.report.md read whole: the worktree path, changed paths,
message path, the comparison REPORT path, its per-theorem disjunct reads, the scratch-mutation receipts). THE THINGS THAT MATTER: (1) the ADAPTER
INVARIANT is a theorem (a live receipt refers to the same obligation revision and inputs; every dependency outside the changed set equal; the
exported fragment reads only its declared supports; an admitted candidate has a matching successful check receipt) and is CONNECTED to Protocol's
fragment repair theorem and Closure's candidate model (not restated beside them); (2) CalculusData.check is NEVER "run Lean and return false on
timeout" (grep the adapter: it judges finite receipt data); (3) the scratch-edit MATRIX ran with REAL receipts (every edit, whole outputs; rule 16),
and the GLOBAL-COLLISION ESCAPE edit (the pigeonhole-vacuous `∃ … Collision` shape replacing CollidesAmong) was DETECTED, not passed; (4) the three
baselines A/B/C agree or every disagreement is explained; candidate-set identity reported beside every repair equality; (5) the malformed/partial
export and the missing-import environment report INCOMPLETE COVERAGE, never fewer obligations repaired (plant them off → the coverage claim lies →
RED); (6) the inverted index agrees with the list oracle on affected candidates/statuses/residuals, with its measures as counts (never wall-clock as a
verdict); (7) the Kernel slice's landed names/signatures are UNCHANGED (diff Kernel/ against main: empty); the premise question "none"; closure C3;
the CROSS-LAYER: GATES line for the census-side tooling; no `#guard`/`sorry`/`partial def`/`native_decide`. READ every new statement with the
DISJUNCT CHECK. Rebuild the reached modules ONCE (6G/2; 16G whole-tree printed if needed, never beside a bench). VERDICT first: LAND /
LAND-WITH-FIXES (exact; apply if small) / REFUSE. On LAND: rebase onto main's tip (append-only decision), gates/check.py, placeholder grep, LAND via
scripts/commit (a gates/ change → full judge; detached, PID file logs/CX-READER-PE1-land1.pid, log logs/CX-READER-PE1-land1.log; full-deadline sleeps;
never stop a judge; refusals read whole and fixed forward). Report the hash, DONE.

HOLD (real 10-21): Ember has called a step-back review of the day's method; READ and write your VERDICT now, but do NOT launch any landing until a line beginning 'ROOT RELEASE' appears in your own REPORT file (/Users/ember/dev/redregg/work/codex/CX-READER-PE1.report.md): poll it with full-deadline sleeps after your verdict. Also note: ROOT ruled B (alpha-normalize bound-variable labels in the version hash, with a canonicalization law and plants both ways) in CX-PE1's report; the builder reports it "retained" the conservative identity: say in your verdict whether B was applied, and if not, whether the conservative identity's false invalidations are measured and explained in the comparison report (acceptable for this pilot) — that is a LAND-WITH-FIXES item, not a refusal.
