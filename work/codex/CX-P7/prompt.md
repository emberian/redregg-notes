# CX-P7

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

# YOUR BRIEF (CX-P7)

Name: CX-P7. Layer: LANG (gates/OWNERS: Lang/*). You are one of FOUR concurrent Lang workers on THE CONTEXTUAL PROGRAM; read

YOUR CARD: CARD P7 = DECISIONS CARD 9 RULED (B) BY EMBER: contextual holes IN THE DEPLOYED LANGUAGE, a REDESIGN DAY (always approved; a re-genesis is not a cost; price premises). Add CMTT's substituted hole to Lang's terms as the 18th constructor: hole n sigma (a hole with a substitution for its context); HasType checks sigma against the hole's context; fillRefs substitutes sigma; LangHasTy DROPS the d.ctx = [] conjunct; the boundary theorem langTemplate_no_hyps (LANG-68 2b6e5e1) is DELETED and replaced by the strengthening experiment on a DEPLOYED package (a hole whose filling uses a hypothesis of its context; the five outcomes incl. strengthening reachable in Lang: prove it over the journey). Touches every Term recursion (the checker infer: keep infer_sound/infer_complete; BigStep; the printer/reader; the lang/package wire): a lang! with a CODEC review (ROOT for CODEC: list every wire byte that moves and re-emit the vectors; every package re-ids; state the flag day: what re-emits, what refuses to load). Premises: name every landed theorem that gains a hypothesis (expected: none; one new case per touched proof): the spread goes in the decision BEFORE you build (send it in the REPORT as PRICE PREMISES with the list of touched proofs). WAVE-4 amendment: context polymorphism (Murase et al.) is the principled 'typed under any ambient context'; Norell's guarded constants (thesis ch. 3; PDF in /Users/ember/paperbin) are the precedent for a blocked hole's guard in the signature: cite both in the decision. Base: the FIXED activities bundle must be on main first (the hole generator you extend): poll main for CX-READER-ACT3's lang! hash before building (full-deadline sleeps).

Land nothing yourself: when built GREEN with gates/check.py run and your per-theorem disjunct read in the REPORT, write READY with the worktree path, changed paths and the drafted message path, then DONE.

RUN 2 (real 10-21): READ FIRST your run 1 REPORT /Users/ember/dev/redregg/work/codex/CX-P7.run1.report.md whole: it holds the built-unlanded
common substitution foundation (wt/CX-P7 at de03530; logs/CX-P7-audit.md with the exact remaining joins) and, appended at its end, ROOT'S
TWO RULINGS which your run 1 paused on without reading: (1) the deployment fork = (2) LIVE contextual packages (the typed hole signature and
candidates in the ROM; selections authenticated from pinned rows; instantiation per invocation; the runtime hole environment's typing /
cost / provenance invariants as theorems with teeth; generalized statements + closed specializations so no landed theorem gains a
hypothesis; the experiments and P8's four changes re-run over DEPLOYED packages; no staged fallback); (2) CODEC paths GRANTED (Emit/
Vectors.lean + regenerated vectors + generated.rs regenerated, under CROSS-LAYER: CODEC with the table rules). THIRD GRANT, for your run-1
ask: gates/codec-vectors.tsv (GATES) regenerates in the same lang! under `CROSS-LAYER: GATES (ROOT granted the regenerated codec vectors
for the hole constructor, real 10-21)`; generated output only. Now BUILD the card: the constructor, the contextual signature/checker,
fillRefs integration, the deployed five-outcome journey, the flag-day vectors; price premises in the decision before the constructor lands
(expected none; one case per touched proof). When GREEN with gates/check.py run and your per-theorem disjunct read in the REPORT, write
READY (worktree, changed paths, message path) and DONE; ROOT sends the reader. Do not exit while unfinished; a wait is a full-deadline
sleep, not an exit.

RUN 3 (real 10-21): READ FIRST /Users/ember/dev/redregg/work/codex/CX-P7.run2.report.md (your run 2) and /Users/ember/dev/redregg/work/codex/
CX-READER-P7.report.md whole: the reader REFUSED your READY on one ground, with a kernel-checked counterexample (logs/CX-READER-P7-contract.lean):
the LANDED fillRefs_typed's closed library-changing contract is silently not preserved under the submitted fillRefs (its old premises hold,
its old conclusion fails), and the explicit closed checker/renaming wrappers are missing. ROOT's ruling on that fork is appended at the end
of the reader's report: B. DO: (1) SUPERSEDE the six old ref-model statements (fillRefs_typed / Fields / Arms and the occurrence contracts
the reader names) explicitly: new names with the live meaning, the old names DELETED (never kept with a changed meaning), each listed in
the decision and the message with its exact changed meaning (say what you broke); (2) add the byte-identical closed checker/renaming
WRAPPERS and prove the closed-to-live deployment bridge (a closed package's behaviour is unchanged under the live path: a theorem, plus
the reader's counterexample turned into a tooth that the NEW statement refuses by construction); (3) every tooth of the six is carried
to its successor or replaced by a named successor tooth, listed; (4) the premise question stays "none" for every other landed theorem
(diff); (5) rebase onto main's tip (3bd8c12; the size gate wants a `SIZE: Rust lines` line for 20757 → 20763: add it); gates/check.py GREEN.
Then write READY (paths, message) and DONE; the reader re-reads. Do not exit while unfinished.

RUN 4 (real 10-21): ROLE SWAP — you are now the SECOND READER of the proof-consumer PORTS that CX-READER-P7 is making (its REPORT
/Users/ember/dev/redregg/work/codex/CX-READER-P7.report.md: the full-landing refusal (InvokeWitness.lean / Logic/History.lean / EscrowRun.lean
RED because they unfold the old load/loadAll/judgeOne and identify Program.run/judge with the closed runMeasured/judge), ROOT's grants and
the run_of_program ruling A, and its `READY-PORTS` line listing every ported theorem old → new). Poll that report for `READY-PORTS` with
full-deadline sleeps. Then READ every ported statement with the DISJUNCT CHECK and the premise question (NO public landed theorem gains a
hypothesis: diff against 3bd8c12; the closed bridges for counter/escrow derive from the fixed empty-signature ROM; the generalized
contextual-law lemmas carry the signature); confirm the seventh superseded contract (run_of_program → the named live extraction theorem)
is listed; rebuild the reached Kernel/Ledger/Lang proof modules ONCE (6G/2; 16G whole-tree if needed, printed, never beside a bench). VERDICT
first line of your REPORT: LAND / LAND-WITH-FIXES (exact; apply if small) / REFUSE. On LAND: rebase onto main's tip, gates/check.py,
placeholder grep, LAND via scripts/commit (lang! → full judge; detached, PID file logs/CX-P7-land4.pid; full-deadline sleeps; never stop a
judge; refusals read whole and fixed forward). Report the hash; cv task done 01a158da-0192; DONE.
