# CX-READER-P11b

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

# YOUR BRIEF (CX-READER-P11b)

Name: CX-READER-P11b. ADVERSARIAL SECOND READER, then LANDER. CHARTER law 6: you are the second agent for CARD P11b (incarnation/material
for the guard with a separate completion check: the worker found at source that incarnation is closed under daimon, so materiality ≠
daimon-freedom; change-structure laws for Repair (RepairChanges identity_kept / composed_derivative); TransportKinds rechecked vs internal
distinct by construction (recheck_sound); first-class substitutions scoped to context morphisms; the intensional/extensional split for
boundaries with typed syntax-reading guards), built by CX-P11b (dead) in hbox /tank/dregg-build/nanodregg/wt/CX-P11b at b72e5a8
(uncommitted; REPORT /Users/ember/dev/redregg/work/codex/CX-P11b.report.md read whole: 54 statements with its disjunct reads, ten mutation
probes; changed paths logs/CX-P11b-changed.txt (13); message logs/CX-P11b-message.txt). Then CONTEXTUAL-PROGRAM-20261020.md CARD P11b and
LITERATURE-CONTEXTUAL-20261020.md §4 items 4, 5, 8; the cited PDFs in /Users/ember/paperbin (Fouqueré–Quatrini pp24–26 Def 5.1/5.5; Cai
et al. change structures; Kavvos; Mœbius): are the field's definitions used as stated, and does the decision text SAY the worker's
correction of the scholar (incarnation closed under daimon)? READ every statement with the DISJUNCT CHECK; premise question (diff landed
signatures against main; existing Lean files untouched per the worker: verify); teeth real (outputs whole); closure C3. Rebuild the reached
modules ONCE at 6G/2 threads (beside benches is fine; never 16G beside one). VERDICT first: LAND / LAND-WITH-FIXES (exact; apply if
small) / REFUSE. On LAND: rebase onto main's tip (append-only decision; other P-cards are landing concurrently: re-read main after the
rebase), gates/check.py, placeholder grep, LAND via scripts/commit (detached, PID file logs/CX-READER-P11b-land1.pid, log
logs/CX-READER-P11b-land1.log; full-deadline sleeps; never stop a judge; refusals read whole and fixed forward). Report the hash, DONE.
