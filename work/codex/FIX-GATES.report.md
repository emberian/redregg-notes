# FIX-GATES report (nanodregg; Claude Opus 5.5 lane; worktree hbox:/tank/dregg-build/nanodregg/wt/fixgates)

Times are hbox's clock (EDT, UTC−4).

Brief: A2 (decls bodies + RESTATES-MEANING strength + census into the fast path), A22 (census misses), A23 (THE
BAR's clock, waste's exact 1/1/0), A16 (the miscompile gate on compiled bytes) + A20's gates half (tcb rows, pins
compared). Each card its own commit with a GATES-20v/w/x/y decision. Labels: READ = from the source, MEASURED = run
here, INFERRED = reasoned, not run.

## 2026-10-24

- 05:30 EDT READ: COLLATION-20261024 §A2/A16/A22/A23, READ-LEDGER-CENSUS-GATES whole, R-0069. Worktree `wt/fixgates`
  at f9657bd; .lake copied (cp -a, under slot 1's flock) from judge slot 1.
- 05:35 EDT MEASURED: the old exporter, whole tree: 13.6 s, 1.7 GB, 20,570 rows, 29 MB raw / 7.5 MB gz.
- 05:40 EDT MEASURED (friction, decls cache of main's last 80 landings): definition bodies changed per landing 0–80, and
  theorems that name them directly 0–314 (e7c2b13: 13 defs / 41 theorems; e2eecce: 56 / 120; 1f09446: 80 / 314).
  This shaped the design (a definition's line covers its theorems).
- 06:00 EDT MEASURED: `deser ∘ ser` is the identity on all 73,919 statements and values of f9657bd. The first run had 250
  mismatches, all hygienic names with numeric components; fixed by a name reader.
- 06:10–06:57 EDT MEASURED (A2 on the real landing e7c2b13 on 1eae61f, its own message):
  - First run: RED (37), 221 s at load ~20.
  - Two of the reds were my bugs. The transplant was ordered by parts, not by references (kernel `unknown constant
    GatesOld…`). `verdict` zipped the name lists of two different statements. A third bug: `addDecl` checked
    asynchronously, so its kernel error was not caught; switched to `Environment.addDeclCore`.
  - Another fault: runtime exceptions (maxRecDepth) escaped `try`; switched to `tryCatchRuntimeEx`.
  - Strength budget: 200,000 heartbeats cost 134.8 s for 19 checks; 20,000 gives identical verdicts in 17.7 s; 5,000
    in 12.1 s.
  - Final run: RED (30), 28.3 s at load ~13. 7 of 19 RESTATES-MEANING lines shown at least as strong; 12 need a
    reader; 18 theorems changed meaning through two edited definitions (offerEscrowPackageOf 14, offerPackageOf 4).
- 06:40 EDT MEASURED (census, f9657bd built): whole census.py 21.0 s at load 9 (44.1 s at load 12); imports 1.3 s,
  axiom 12.0 s, refine 11.2 s, statement 8.5 s. Reach census: leaf 10.1 s, Hosting.Proofs.Deployed 18.3 s,
  Kernel/World.lean (329 modules) 15.7 s.
- 06:45 EDT MEASURED: decls plants: `--lean` 14 cases GREEN (91–147 s by load), its control RED (1) harness-control;
  `--synthetic` GREEN, control RED. statement_plants with the reach plant GREEN (39 s), control RED.
- 07:00 EDT MEASURED (A16): vectors `"\x01b"` [27,0]/[1,98]; `"a\u0000b"` [97,11,0]/[97,0,98]; `"\x00" ++ "b"`
  [11,0]/[0,98]; 11 other classes agree. Scan of the tree's emitted C: ok, 502 modules, 3.7 s.
- 07:02 EDT MEASURED (A20 gates half): the four host sha256 pins match their files on hbox/macOS today. The AppArmor
  row's "equal to sandbox/apparmor/nd-bwrap" is FALSE: tree 15047263…, installed 4b9faabc…; the diff is the five
  comment lines added at 173993d.
- 07:05 EDT cv tasks: 01a16d97-2a72 (DELETES as a weakening door), 01a16d97-2a86 (re-pin the historical decls plants
  H1–H4).
- 07:10 EDT Card 1 (GATES-20v) launched through scripts/commit (FULL judge). First attempt refused by the size ratchet
  (Census Lean lines 1078 → 1113 needs SIZE: lines); relaunched with them.
- 07:15 EDT The landing queue holds 4 FULL landers ahead of card 1 (fixhost, fixrust, fixlang, fixproto) and all four
  slots are busy, so cards 2–4 are tested in second and third worktrees: wt/fixgates2 (37772b9 + cards 1–4),
  wt/fixgates3 (f9657bd + card 3).
- 07:25 EDT MEASURED (card 2): the first version of the new census RED'd a landed tooth,
  `Kernel.Proofs.Refusals.plant_refusals_unseparated : ¬ Trie.Separates (plantRefusalSpec E)`. That was a FALSE red
  of my walk: an equation under `∀ i < depth` between keys chosen outside it is not pigeonhole-provable.
  Rule fixed: the escape walk enters only premises; the disjunction walk crosses `∀` with the outer choices cleared
  and does not push negations. An 11th fixture holds the case. Final: the tree reads `STATEMENT-CENSUS ok: 425
  disjunctions` (282 before; 143 new rows under `∀`, all ok); the whole census takes 23.8 s. statement_plants GREEN:
  8 vacuous plant theorems RED by name, incl. `forgotten` (cv 01a1654c-543c); 5 mutants each refused by the
  fixtures; reach RED (8); control RED. The memo's six over `P.h`: all RED.
- 07:35 EDT MEASURED: THE BAR is RED ON MAIN 37772b9. Main's own bar.sh reads `friend1 nd write exit 1: refused
  stale`; on f9657bd it reads PASS. Not this lane's layer: cv 01a16db5-b18e (bisect a7bccd8 / f1839ed).
- 07:45 EDT MEASURED (card 3, on f9657bd):
  - standing bar PASS with the clock judged: p99 430.8 ms, reopen 14.0 ms, load ~9;
  - write limit set to 1 ms: `RED write-p99-ms 491.383 > 1` (the ordinary path consumes it now);
  - control RED, want 2 1 0 read from the table;
  - full N=1000 PASS: p99 269.1 ms, reopen 71.7 ms, 34.2 s, load 6.7 (every recorded full run before read
    UNJUDGED);
  - waste.py: 0/0/0 RED by name against `=1/=1/=0`, but `[]` against the old table;
  - waste.py --plants GREEN, control RED.
- 08:00 EDT MEASURED (card 4 in wt/fixgates2): tcb.py's first pin reader mis-parsed `sandbox/apparmor/nd-bwrap` as the
  absolute path `/apparmor/nd-bwrap`. Fixed: a path must start a token, and a tree-relative pin compares the tree's
  copy. Final: `tcb: ok` with the four host pins compared on hbox. tcb plants GREEN, control RED. cbytes vectors
  GREEN; the tree scan is ok (503 modules). refusals.py ok without the source pattern.
- 08:10 EDT RULING received (ROOT relaying Ember): top-level-only non-vacuity, via the spec layer (FABLE-SPEC); no
  per-theorem machinery; plants are never a landing gate. By then card 1 (GATES-20v: strength check, per-theorem
  meaning digest, plants in the fast path) was INSIDE its FULL judge, holding a slot. GATES-14 forbids stopping a
  judge by its PID, and the inner attempt would land regardless, so it is fixed forward: GATES-20v′ follows it.
- 08:25 EDT MEASURED (GATES-20v′, scoped, in wt/fixgates2/3):
  - kept: one line per edited definition that a statement names (`undeclared redefinition`), with its parts
    (matcher, where helpers);
  - deleted: the strength check, BY:, READ-BY, the read-back, the level-parameter column;
  - fast path: the reach census stays; the plants leave it;
  - Lean plants 8 cases GREEN in 30 s; synthetic 25 GREEN; both controls RED;
  - e7c2b13: RED (8), eight redefinitions with their lines, 14.7 s at load ~8.
- 09:05 EDT Card 1 (the unscoped GATES-20v) was REFUSED by its FULL judge. The only NEW RED was its own Lean
  plants: the judge's `{fresh}` path holds a `:` (`.lake/runs/script:…`), which splits lake's LEAN_PATH.
  lang-journey (`rejected stale`, LB8b/LH7b), rows and THE BAR read PRE-EXISTING red on main, the same stale-path
  change as cv 01a16db5-b18e. So nothing of the withdrawn design landed.
- 09:15 EDT The Lean plants and the cbytes vectors now build in a colon-free temporary directory, refused by name if
  it holds `:`; measured GREEN under a `script:x-1` path. Relaunched card 1 as the SCOPED GATES-20v (one decision:
  what was built, measured and withdrawn is recorded in it). PID file
  /tank/dregg-build/claude-lanes/fixgates-scratch/land-20v.pid.
- 09:20 EDT Card 3 (GATES-20x) launched concurrently from wt/fixgates3 (rebased to d741f5a; disjoint paths). The
  first attempt was refused by parent-gates: main's waste.py cannot parse `=1`. The table form changes, so the line
  is GATE-CHANGE; relaunched with it (land-20x.pid).
- 09:50 EDT PARKED (~650K tokens). Both landers (scoped card 1, card 3) are queued behind fixrust/230/231. Cards 2
  and 4 are staged, with their messages and decisions, in hbox
  /tank/dregg-build/claude-lanes/fixgates-scratch/next/. The steps are in FIX-GATES.continuation.md.

## FIX-GATES-2 (successor, from 2026-10-24 ~09:40 EDT)
- 10:09 EDT MEASURED: card 3 (GATES-20x) REFUSED by its FULL judge (log fixgates-scratch/land-20x.log, gate log
  main/.git/nanodregg-gate-3/05718798ea6d.log). Its own rows were green: bar standing PASS, bar N=1000 PASS, bar
  control RED, waste plants GREEN + control RED. Refusal: `runs: NO VERDICT waste.py ... could not convert string to
  float: '=1'` — pre-push runs MAIN's waste.py ($J) over the CANDIDATE's waste.tsv, so a new table form cannot be
  judged in the landing that introduces it (GATE-CHANGE covers only parent-gates). Also red: lang-journey LB8b/LH7b
  and rows (main's stale-order red; FIX-KERNEL).
- 10:15 EDT Fix forward: GATES-20x split. 20x-a = gates/waste.py alone (reader + plants, table unchanged), launched
  from wt/fixgates3 at 0a299c8 (PID file fixgates-scratch/land-20xa.pid, log land-20xa.log, msg msg-20x-a.txt).
  20x-b = waste.tsv/bar.sh/bar.tsv/runs.tsv/decisions, saved in fixgates-scratch/card3/, lands after 20x-a.
  MEASURED pre-launch: new waste.py over main's table `waste: ok (83 ops pinned)`; over 20x-b's table ok, plants GREEN.
- 13:49 EDT MEASURED: card 1 (scoped GATES-20v) LANDED: a306536 (PRE-PUSH GREEN tree 1319180baf4a; displaced 3 times;
  pushed to origin). Landed unchanged: the worktree's Census/Statements.lean, statement_plants.py, pre-push and
  decisions/gates.md equal a306536's.
- 13:49 EDT READ: FIX-KERNEL's journey fix a339e9d is on main (the stale-order red).
- 13:55 EDT Cards 2 and 4 launched as ONE landing (GATES-20w + GATES-20y, msg fixgates-scratch/msg-20wy.txt): both
  append to decisions/gates.md, and scripts/commit merges each path 3-way, so a second FULL lander appending at the
  same end conflicts. Applied per the continuation in wt/fixgates at a306536; every applied file equals the tested
  wt/fixgates2 copy except pre-push/statement_plants.py comment text (fixgates2 predates the scoped card 1).
  MEASURED pre-launch: py_compile all gates/*.py ok, `bash -n scripts/pre-push` ok, `tcb: ok`, `refusals: ok (0)`;
  size: Census 1113 -> 1211 (SIZE: lines added). PID file land-20wy.pid, log land-20wy.log.
- 13:54 EDT MEASURED: GATES-20x-a LANDED: 17739d3 (waste.py reads `=V`). 20x-b waits for the 20w+20y landing: both
  append to runs.tsv and decisions/gates.md (3-way conflict otherwise), and GATES-14 forbids stopping a judge.
- 14:06 EDT MEASURED: GATES-20w + GATES-20y LANDED: 294d1c5 (PRE-PUSH GREEN tree 7e7660bdd35d, FULL judge, displaced
  once; pushed). 10 files incl. SIZE.md.
- 14:10 EDT GATES-20x-b launched from wt/fixgates3 at 294d1c5: waste.tsv =1/=1/=0, bar.sh, bar.tsv copied (no drift
  since d741f5a); runs.tsv's bar row edited + waste plants row appended; the decision entry (+ a note on the split)
  appended. MEASURED pre-launch: `waste: ok (83 ops pinned)` vs main's table, plants GREEN, control RED, `bash -n`
  bar.sh ok. Message msg-20x-b.txt (no GATE-CHANGE: main's waste.py now reads `=V`). PID land-20xb.pid.
- 15:07 EDT MEASURED: GATES-20x-b LANDED: ade5f15 (PRE-PUSH GREEN tree a1791124ca0d, displaced once, re-judged; pushed).
  All four cards are on main: a306536 (20v scoped), 17739d3 (20x-a), 294d1c5 (20w+20y), ade5f15 (20x-b).
- 15:08 EDT Cleanup: `git worktree remove --force wt/fixgates2` (its uncommitted diff, the tested copies of cards 1-4
  that all landed in final form, archived first: fixgates-scratch/fixgates2-at-removal.diff + fixgates2-cbytes.py);
  `git worktree remove wt/fixgates3` (clean). Kept: wt/fixgates (clean, at 294d1c5) and fixgates-scratch/ (owed:
  remove when nothing reads it; holds the archived diff, judge caches, plant trees).
- 15:35 EDT MEASURED: ONE CONVERGENCE on hbox main ade5f15 (scripts/converge, PID file fixgates-scratch/converge.pid,
  log converge.log): `CONVERGENCE ade5f15955c9 range f9657bd682ca..ade5f15955c9 landings=24 (fast 16, full 8) =>
  GREEN reds=0 fixed=2`. STANDING gates/build/census/generated/cargo/runs/waste all ok, waste pinned 83 unpinned 0,
  flakes 0, carried 5 (cargo path_vectors, sock, hosting-sim, kernel-sim, ledger-sim: byte-identical keys). FIXED
  run:lang-journey and run:rows after 5.4 h. Wall 26 min.
  - The new rows ran (none carried): cbytes vectors ok + control red; tcb --plants ok + control red; waste --plants ok
    + control red; bar.sh standing ok (p99 288.3 ms, reopen 48.6 ms, stale 1/1/0, load1 2.3), control red; bar.sh
    --records 1000 ok (p99 403.9 ms, reopen 97.9 ms; 20 contention stales, 0 after sync). The clock was JUDGED.
- cv: 01a16db5-b18e DONE (the convergence above). Still open: 01a16d97-2a72 (DELETES as a weakening door; under the
  ruling likely the spec layer's), 01a16d97-2a86 (re-pin decls plants H1-H4).
- INFERRED (for whoever next lands a table-form change): pre-push judges the candidate's gates/waste.tsv with MAIN's
  waste.py, so a reader and a new table form must land in that order, as two landings.
