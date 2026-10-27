# FIX-CONVERGE — cv 01a16f6d (scripts/converge false reds)

Landed: **f4e803b** on main, pushed to origin (`gates: a convergence never reads a build that did not finish as RED … (GATES-24; cv 01a16f6d)`), FULL judge PRE-PUSH GREEN tree 073d0dfbf3b7, queue head, 0 displacements.

## Diagnosis (2026-10-24)
- 22:05Z MEASURED: BOTH incidents were cgroup OOM kills at SWARM_MEM_MAX=6G. The first one was NOT caused by a lander. Journal: `run-u56831.scope` (2d5056e, 15:38:31 local / 19:38Z) and `run-u56974.scope` (743a4fb, 17:56 / 21:56Z) both say "Failed with result 'oom-kill'", 6G memory peak; the kernel shows `memory: usage 6291456kB, limit 6291456kB`; both ran LEAN_NUM_THREADS=2. Systemd then stops the whole scope, so lake writes no line at all, and the non-zero exit read `build=RED`. The three queued landers at 2d5056e happened at the same time but did not cause it.
- READ: standing.sh ran waste.py whenever any row was pinned, even when no row ran, so all 83 pinned rows read "nothing measured it" = RED. converge.py attributed every unit. With no module named in the log, it blamed every commit that changed a module.
- READ + MEASURED: **a path DOES commit reverts without ROOT.** `REVERT` lines go to `revert_landing`, which calls `scripts/commit --reverts`. At 2d5056e two runs a minute apart at the same sha counted as two sightings, so the first real sighting already had seen=2 and wrote 67 `REVERT 1ab410e…` lines. All 67 came back `REVERT-FAILED … does not revert cleanly on main` (logs/root-converge-readers.log:177+). Nothing reached main only because the revert had a merge conflict.
- READ: standing.sh also printed the previous run's runs.out counters on a tree it never built (carried=5, outside=30).

## Fix (f4e803b; scripts/converge, scripts/standing.sh, gates/converge.py, gates/waste.py)
- (a) `scoped TOOL CMD` writes the swarm-build scope's cgroup before lake or cargo starts. `converge.py build` reads three verdicts:
  - **ok**
  - **RED**: the build finished and failed. For lake: exit 1 with an `error:` line. For cargo: exit 101 or 1.
  - **ABSENT(killed: cgroup OOM, scope …, peak … of SWARM_MEM_MAX …)**, or ABSENT for a signal or for no error line.
  
  converge.py already treats ABSENT as "not judged", so nothing is attributed. The cargo stages get the same treatment. runs.out is truncated at the start of each run.
- (b) scripts/converge waits while a lander is live. A lander counts when its pid directory exists under `nanodregg-landers/` (`p<pid>` or `<seq>.<pid>`) or `nanodregg-commit-main/<pid>`, and the pid is alive with a cmdline running scripts/commit. It re-reads every 30 s for at most ND_CONVERGE_LANDER_WAIT seconds (default 3600), then exits 75 `NOT RUN` naming the pids. Revert mode is exempt.
- (c) Memory floor = 1.25 × the largest completed whole-tree build peak in 14 days, from `nanodregg-standing/build-peaks.log`, rounded up to a GiB (16G fallback if there is no record). standing.sh appends to that log. I seeded it from the journal: 44 completed standing builds since 10-10, MEASURED max 14.2G (run-u40998, 10-18) and 13.2G for readers3 at 743a4fb (threads=4). **The floor today is 18G.** A SWARM_MEM_MAX below it is REFUSED by name, exit 2. Main's own copy runs the check, in the inner run. Reply card: cv 01a16fec-e804.
- (d) waste.py `--runs-out --traces`: an unmeasured pinned row is RED only when a row that measures it (from the newest read-set's W) ran ok. Otherwise it prints `waste-absent …` and exits 3. When no row ran, standing writes `waste=ABSENT(no row ran)`. Four new `--plants` cases; WASTE PLANTS GREEN.
- One more defect found and fixed: a unit's `seen` now counts one sighting per main, never one per re-run at the same main.

## Plants (MEASURED 22:11Z; the real scripts in a scratch --shared clone, /tank/dregg-build/nanodregg/scratch-fixconverge/plant; script: …/plant.sh)
- C1, fake live lander (`exec -a scripts/commit sleep`, its PID file plus `nanodregg-landers/p<pid>`): waited 35 s, then `NOT RUN … pid 1163796 … scripts/commit`, exit 75. I stopped it by its PID file.
- C2, dead-pid directories (p999999, commit-main/999998): not treated as landers. SWARM_MEM_MAX=2G was then `REFUSED … below … floor 18.0G (… 14.2G at journal:run-u40998.scope …)`, exit 2.
- C3, SWARM_MEM_MAX=1G with a planted 0.5G record (floor 1G), state seeded with the 84 polluted units at seen 3:
  - `build=ABSENT(killed: cgroup OOM, scope run-u57029.scope, peak 1G of SWARM_MEM_MAX 1G …)`
  - `waste=ABSENT(no row ran)`
  - `CONVERGENCE … => INCOMPLETE reds=0`
  - 0 attributions, 0 REVERT lines, state byte-identical.
- The known-red control is the two incidents themselves (old code, same inputs, 84 reds each). Replaying the new classifier on their scopes gives ABSENT(killed: cgroup OOM) for both.

## Real convergence (ROOT's readers3, pid file logs/root-converge-readers3.pid; I waited on it and did not start another)
- 22:28Z READ: 743a4fb at the old code with LEAN_NUM_THREADS=4. Build ok (13.2G peak); census, generated, cargo and waste all ok (83 pinned).
  - **RED reds=2 fixed=84**, wall 28 min, no REVERT lines.
  - All 84 false units read FIXED, so converge-state.json no longer holds them.
  - The 2 reds are real: `run concurrency cargo:devtools:workspace + script:scripts/bar.sh: RED(shared scratch …)`. rustix's build probe `/tmp/rustix_test_can_compile` is a fixed /tmp path that both rows use. It was attributed to several commits at a first sighting. Filed as cv 01a17007-bdbe.
  - INFERRED: no commit caused it, but the next convergence at another main may write REVERT-PENDING for those commits until that card lands.
- I have not run a convergence on f4e803b with the new code; ROOT decides when to run one. Use SWARM_MEM_MAX ≥ 18G, or leave it unset.

## Not done / notes
- scripts/commit's own full-judge build still reads an OOM kill as RED. That refuses a landing rather than attributing one, but it is the same class of defect, not covered here.
- My scratch on hbox: /tank/dregg-build/nanodregg/scratch-fixconverge (plant clone and cwt), plus worktree wt/fixconverge.
