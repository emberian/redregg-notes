# CX-MINI-COLL

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

# YOUR BRIEF (CX-MINI-COLL)

Name: CX-MINI-COLL. Repo: MINIDREGG (not nano): hbox /home/hbox/dev/minidregg (the production demoland; its judge/landing conventions are its own:
read its CLAUDE.md, AGENTS.md, ATLAS.md and scripts/ first; land through ITS landing path, never nano's scripts/commit; never git push to a branch
you did not create; never stash; filtered tests only). TASK = cv 01a15630-cf43: eight consumer sites in minidregg carry the pigeonhole-vacuous
`∨ Collision` shape (an unbounded `∃ a b, a ≠ b ∧ hash a = hash b` disjunct that is TRUE over a 32-byte digest, so the theorem binds nothing; nano
found 61 such sites in itself and restated them as `CollidesAmong hash S` over an EXPLICIT finite list S the theorem builds — read nano's KERNEL-56
decision in hbox /tank/dregg-build/nanodregg/main/decisions/kernel.md and two restated sites in Kernel/Proofs/Trie.lean for the shape; the memory
rule: a disjunct provable from the premises alone or the instance alone is vacuous). Read `cv task show 01a15630-cf43` and the memo
/Users/ember/dev/redregg/work/HOLES-FOR-PROOF-ENGINEERING-20261020.md section "Mini: reuse its existing proof-engineering investment" (the
AuthTrie/AuthTrieRange/ObjectiveBendDigest sites; the manifest ratchet classifies restated statements: each needs an exact decision). DO: inventory the
sites FRESH (grep `∨ Collision` and `Collision` escapes across Theory/ and Kernel/; the task's count is historical); for each, restate to
`CollidesAmong hash S` over the explicit compared inputs the proof actually hashes, retaining the literal old proof's structure, deleting the old
statement (never two shapes); the consumers that must change priced and changed; a tooth per site (a mutant that drops the explicit list → the old
vacuous shape → RED under a plant that checks the disjunct is not provable from the instance); minidregg's ObjectiveManifest ratchet records each as
RESTATED with its reason. PRICE PREMISES: name every landed mini theorem that gains a hypothesis (expected: the explicit-list premise where the old
unbounded one was free) in the decision. Build/test on hbox with `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build` (mini's library sizes may need
16G: print it); filtered tests only. Land through mini's own path as one commit per site group; report the hashes in your REPORT; `cv task done` with
the hashes. Rules: /Users/ember/dev/redregg/work/LANE-RULES-NANODREGG.md (the box-safety and kill rules apply verbatim; the nano-specific gates do not).

RUN 2 (real 10-21): READ FIRST /Users/ember/dev/redregg/work/codex/CX-MINI-COLL.run1.report.md whole (your expanded site inventory and consumer findings; your BLOCKED/ASK) and ROOT's lane ruling appended at its end. CORRECTIONS + AUTHORIZATIONS: (1) the Mini source is hbox:/tank/dregg-build/pipeline/warm-base/src at 334316df (my /home path was wrong). (2) Mini's own documented lane creator (the one that rsyncs the warm tree and copies .lake into a lane) is AUTHORIZED for ONE lane: it is Mini's designed path and the contract's rsync/.lake prohibition exists to stop duplicate rebuilds and artifact destruction on nano, which this is not; run it exactly as documented, once, into /tank/dregg-build/claude-lanes/cx-mini-coll/, never touching warm-base/src, with your own cargo target. (3) The receiving owner is ROOT-for-Mini; the keeper for main publication is Ember's standing instruction that mini lands through its private-clone integration onto main then a warm-base advance: do that if its script needs no credential you lack; otherwise STOP at built+tested patches per site group (paths + SHA256 + whole test outputs) and report; ROOT publishes or asks Ember. Then the work as briefed: restate each `∨ Collision` site to CollidesAmong over the explicit compared inputs, delete the old statement, price the consumers, a tooth per site (the disabled-list mutant RED, nonvacuity at an inhabited finite deployed-shaped instance), the ObjectiveManifest ratchet's RESTATED events. Do not exit while unfinished.
