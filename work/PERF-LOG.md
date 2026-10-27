# PERF-LOG — BUILD-PERF continuation (aa94d27502b80e789, 2026-10-17, STOPPED by ROOT at ~260K)

**Ruling in force (Ember via ROOT, 10-17):** no wall-clock benching until near the end of development,
never on the laptop (load was 120–180 all session). The lane narrows to DETERMINISTIC measures only
(instruction/tick counts, the sims' WASTE ratios, `perf stat --no-scale` on a Linux box later), never ms.
Do not build Bench/ wall-clock exes; do not run scripts/bar.sh. The lane resumes near the end, on burst5.

Brief: `~/dev/redregg/work/nanodregg-scout/ASSEMBLY-perf.md` §6. Worktree: `~/dev/nanodregg-wt/perf`
(clean, at b616a8d; made with `git worktree add --detach`, before `perf` was in scripts/worktree).
Commit: `scripts/commit -F MSG PATH...`, subject `perf:`. **Use lane-private message filenames**: the
session scratchpad is shared by several lanes and another lane overwrote my `msg1.txt` mid-commit.

## Landed
| commit | what |
|---|---|
| a53bffc (CLIENT-2 landed it) | the sandbox-hang plant `client/tests/supervise.rs::a_confined_lean_host_answers_within_the_deadline`: real nd-supervise + lake-built `host serve`, one READ frame, 3 s deadline, red by name `SILENT HANG …`. Red at 87c721e in 3.11 s; fix a1bd695 (macOS floor allows `sysctl-name "hw.ncpu"`; CLIENT-2 chose it over LEAN_NUM_THREADS). A correctness gate — keep. |
| b616a8d | `scripts/bar.sh`, `gates/bar.tsv` (limits 5000 / 60000, `run` trend rows), `decisions/perf.md` PERF-1 (both critiques). Over sockets: 2 members (nd + custody + confined `host follow` each), 1 confined writer shared by symlinked host.sock, N/2 `nd create` per member concurrently, writer stopped by PID file, reopen = new supervisor spawn → first `read` reply. RED by name for broken runs at any load; limits judged only at load1 < 2 (else UNJUDGED); plant `BAR_LIMIT_SCALE=0.0001` → RED (ran). NOT wired into standing (GATES-2 told to hold). PERF-1's status line still says "open (GATES: the standing hook)": update it to "suspended until near-end (Ember 10-17)" when the lane resumes. |

## Parked out of tree (not committed, by the ruling)
`~/dev/redregg/work/perf-bench-wip/`: `Bench/Host.lean` (+Main) — `bench-host verify N | digest N | base REPS SIZE… |
worstcut DIR BASE_N BIG_BYTES REPS`, deployed definitions only (Host.Deployed.X, Receive.submit with CODEC's
Ed25519.sign, Base.file/read, Host.genesis, fileCheckpoint, commitBatch under withinTail, openFollower with
foldStep/auditStep), IO.Ref sink, median/p99/max; `Bench/Lang.lean` (+Main) — `bench-lang WIDTH CALLS DEPTH…`,
invoke of Journey.owned behind DEPTH lib packages under the deployed Ctx (width ≤ ~100: 300 fails `encodePackage`);
`lakefile-gates.patch` — the lean_lib/lean_exe entries + TOOLING_LIBS "Bench" + size.py label (GATES-2 had agreed).
Builds green at b616a8d. If the lane resumes with DETERMINISTIC measures, the drivers (real signed births, the
worst-cut Store construction) can be reused with a tick/instruction counter in place of the clock.

## What the loaded-laptop runs showed (UNJUDGED, load 120–180, NOT numbers — leads only)
- The worst cut is bounded by `tailMax` (~35.65 MB at THE BAR's 179 KB base), but a real record is at most
  ~8.2 MB (64 turns × an eventBytesMax birth), not `recordBytesMax` 32 MiB: 5 records / 277 big births fill it.
- A follower's cold open (auditStep) re-verifies every signature: the worst cut for it is a tail of SMALL Turns
  (~90k births in 35 MB → ~90k Ed25519 verifies at ~0.4 ms ≈ 36 s+ by arithmetic, inside 60 s but the first
  BAR term that is not 1000× inside its limit). Unmeasured — the run was stopped. A deterministic proxy: count
  verifies per open (= Turns in the tail), which the code decides; no clock needed.
- lang invoke cost grows ~linearly with closure size (LANG-16 re-check per load); the deterministic version of
  P2's before/after for LANG-3 is a CEK-tick / instruction count per invoke at closure 1 and 8.

## Near-end BAR run needs
A quiet box (burst5-a in /srv/scratch, load recorded; Linux path uses bwrap — never run yet, and fsync is
fdatasync there, so the number is per device), then: `rows --times 1000 bar` (PROTOCOL's in-process row, toy
params) AND `scripts/bar.sh --records 1000 --record` (the real stack), each with `BAR load` lines; plus the
hosted resident once a hosted verb exists (bar.sh says `BAR scope … no hosted resident`). Then GATES wires
`bar=` into standing with the BAR_LIMIT_SCALE plant.

## Laws/notes for ROOT
- Shared session scratchpad between lanes is a collision hazard (my commit was judged with a `kernel:` message).
- No Lean deployed Sim params exist yet (KERNEL-4); births for any measure are signed with CODEC 279c2b8's
  Ed25519.sign — slow (~0.5 ms), so generating 100k-record Worlds costs minutes of CPU.
- Nothing of mine is running; every scratch file I made is deleted.

## PERF-1 (2026-10-18, swap 3 of STAND-INS-20261019; worktree hbox:/tank/dregg-build/nanodregg/wt/perf at 8ad3982)

### Correction to the lead above (per HOST-22)
"A follower's cold open re-verifies every signature" is STALE. HOST-22 (ROOT, 10-17) says reopen folds with
`World.step` and verifies NO signature: base and tail rest under one MAC. So verifies per reopen = 0 by design.
Verification happens at follow time: `Command.step` re-judges every paged event. Verifies per follower =
the steps it absorbs. There is no deployed counter for it (swap 10 / PERF-3), so the bar derives it from the
follower Store's STATUS steps and labels it as derived.

### bar.sh on Linux, first runs (hbox, noisy: load1 6–36 on 24 cpus)
- Linux path fixes: the sandbox needs `--exec HOST` (bwrap floor). Custody refuses keys under any g/o-writable
  ancestor (StrictModes), and all of /tank/dregg-build is 775, so the run root is `--root` (default $HOME, ext4 nvme).
  `/tmp` on hbox is tmpfs (fsync free) and is now RED by name.
- Workload: 3 actors (friend1, friend2, and the hosted-resident STAND-IN, which is `nd --init-hosted` custody
  driven by nd argv). Each creates one object and grants it `anyone mutate`. Then come round-robin writes,
  alternating own object and the next actor's object via its grant. use= is exactly 3 (PROTOCOL-43).
- `--standing` (serial, N=60): steps/cmd 1.000, records/cmd 1.000, seg-bytes/cmd 757.700 (exact across repeat runs;
  745.900 at N=30). The writer's /proc io syscall counts drifted by 1 between identical runs, so they are NOT pinned.
- Full at 300: p50 44 ms, p99 68 ms, reopen 33 ms, follow reopen 43 ms, load1 6.3 → UNJUDGED.
  Full at 1000: RED every time (5 runs), 8–12 s in.

### FINDING 1 (CLIENT, cv 01a14ed9-8c59, CLIENT-7): nd-supervise leaks ~2 fds + 1 thread per connection
The writer's supervisor gained 72/132/252 fds over 30/60/120 commands. At ~500 connections it reaches
RLIMIT_NOFILE 1024, and mux.rs accept() then silently `continue`s on try_clone failure. nd sees EPIPE/ECONNRESET.
THE BAR cannot pass at 1000 records on any box with a 1024 soft limit.

### FINDING 2 (KERNEL-19 / PROTOCOL-13): honest contention spends the refusal budget
Concurrent writers on shared objects get `refused stale`. That is correct, and it must stay recorded: the A→B→A
finality defect. But every stale refusal spends the member's refusal budget (`refusals-per-member-window` 16),
so honest re-runs reach `declined refusalBudget` (seen once at N=1000, before the fd leak hit).
Measured at N=400, full mode, 3 actors, 3 runs:
- writes meeting a stale: 3, 9, 17 of 400 (0.75–4.25 %);
- re-runs after one `nd sync`: 4, 9, 17;
- re-runs stale AGAIN after the sync: 1, 0, 0 (1 of 30). A sync before the re-run clears nearly all of them.

At N=200 (3 runs): 16, 10, 20 stale re-runs. Those runs re-ran WITHOUT a sync. bar.sh now syncs before every
re-run (PROTOCOL-44's hint names the cell; `sync` is the general catch-up) and caps re-runs at 8.
Steps/cmd in full mode rises above 1 by exactly the stale refusals (each one is a recorded step).
Note: nd does not re-read on its own after a stale; the caller must re-run.

### Progress (PERF-1, same day)
- ROOT ruled (3): PERF lands runs.py's `script:` row kind as CROSS-LAYER, with GATES-6's yes.
- GATES-6 said yes on three conditions, all done:
  (1) runs.py drops ND_BIN from a script row's environment;
  (2) Stores go under `--root {fresh}` (runs.py creates and removes it). Custody workspaces stay under $HOME
      (KB), because every /tank/dregg-build path is 775 and custody refuses keys under it;
  (3) the control's limits are 0, not x0.0001.
- Mutation-proven by hand: with each comparator disabled in turn, the control printed "a planted expectation
  stayed quiet: use / at-tip / limit" followed by `BAR verdict PASS`.
- Plants through scripts/plant:
  - `perf1-script-dash` RED: "a script row is a verdict run … never `-`".
  - `perf1-script-noexec` RED: "no executable gates/bar.tsv".
  - The inert-control plant needs `--build`, because a `--no-build` pre-push skips runs.
- scripts/plant gives every PATH=FILE plant mode 100644, so planting an executable script makes it
  "no executable". Workaround used: put the mutated file in the worktree and pass `--with`, then restore it.
  This is a GATES tool gap to report.
- CLIENT-7 landed the leak fix at cf79591 (fds bounded at 71). The fd WASTE rows must be re-pinned before
  landing.
- PROTOCOL-13 renames the in-process row's printed lines `LIVE …`, landing with PROTOCOL-48.

### LANDED de718bf (perf:, 2026-10-18)
What landed:
- scripts/bar.sh PERF-2;
- gates/runs.py `script:` row kind (CROSS-LAYER, with GATES-6's yes), and the runs.tsv row with
  --harness-control;
- 5 WASTE rows (op bar: steps/cmd 1.000, records/cmd 1.000, seg-bytes/cmd 757.700, writer and follow
  supervisor fds/cmd 0.000, after CLIENT-28 cf79591);
- bar.tsv: 3 run rows;
- perf.md: PERF-2, and PERF-3 PROPOSED.

The commit judged GREEN three times (main moved twice), then landed.

First 1000-record runs at b9cd50f (noisy hbox, load1 15–17 on 24 cpus, UNJUDGED):

| run | write p99 (ms) | writer reopen (ms) | follow reopen (ms) | use | stale re-runs |
|---|---|---|---|---|---|
| 1 | 136.6 | 110 | 111 | 3 | 15 |
| 2 | 75.2 | 105 | 107 | 3 | 0 |

cv 01a14e19-a82f is done. The stale/budget finding is cv 01a14edf-6f12 (PROTOCOL-13). PROTOCOL-13's row
prints `LIVE …` since 7932cb3.

Open after this landing:
- PERF-3: ROOT's ruling on deployed-parameter counts.
- C6: the worst-cut reopen (a Store at tailMax). It is not measured yet: at 1000 records the writer never
  sealed a base past genesis, and the reopen tail is all 1000 steps (750 KB).
- The scripts/plant 100644 gap (GATES).
- THE BAR v2 (ssh, a real resident, a cold cache) waits on HOSTING-8, OPS and a box.

### PERF-3 + C6 (after ROOT's ruling)
- bench-count (Bench/Count.lean) is built and green on hbox.
  - The toy-Store plant reads `refused shapeMismatch`.
  - The replay must reach the host's own World.
  - --harness-control flips a chain bit; it is mutation-proven in bar.sh's control.
- Verifies per step: exactly 1.000 when no refusals are recorded (serial). Pinned.
- Trie hashes per step: 15.1–16.0, varying with random keys/nonce. NOT pinned; asked ROOT about a seeded
  custody.
- C6: `host seal W` on the stopped writer at the midpoint (HOST-13 agreed, no knob). Reopen tail at 60 records:
  350.3 B/cmd (pinned). Full run at 1000: base at step 502, tail 375 KB, reopen 63 ms.
- HOST-13 correction: tailMax ≈ 18.9 MB since HOST-47 (recordBytesMax 16,779,332), ~25k records of the bar's mix.
- FINDING 3 (to KERNEL-19): a recorded refusal costs two verifies (`judge`: `submit` verifies, then
  `authenticated` verifies again). Seen as 502 verifies over 500 steps with 2 stale refusals.
- Device note: --standing on tank (ZFS) measured serial write p50 543 ms under load, against 32 ms on
  ext4/nvme in $HOME.
- Waiting on GATES-6's yes for TOOLING_LIBS "Bench". Commit message: hbox logs/perf1-msg2.txt.

### LANDED 5f7c58d (perf:, PERF-3 + PERF-4)
- What landed: bench-count (Bench lib in TOOLING_LIBS; size.py row renamed to name Bench; GATES-6 agreed), the
  midpoint `host seal`, and WASTE rows `bar reopen-tail-bytes-per-command` 350.300 and
  `bar audit-verifies-per-step` 1.000. records-per-command is now taken over the tail.
- Plant perf1-bench-c9 RED: "closure: C9 Bench.Count (deployed) imports tooling module Host.Sim.File".
- Judged GREEN on 8 attempts while main kept moving (COMMIT_RETRIES=10 on the second launch).
- Open:
  - trie hashes/step are not pinned (random keys); seeded custody is ROOT's call.
  - the tailMax worst cut (~18.9 MB) is a Bench case, unmeasured.
  - THE BAR v2.

### LESSON (ROOT-recorded, 2026-10-18): never wrap a supervised process in a tracer whose PID file dies with the run root
Two trees from my strace diagnosis of the fd leak (strace 779667 and 818024, each with nd-supervise, bwrap and
`host serve` under it) were orphaned on hbox. My scratch copy of bar.sh put `strace` in front of nd-supervise,
so the PID file named the tracer. Killing the tracer left its children, and bar.sh then removed the run root
holding the PID files. No PID file, no kill: they are on Ember's list with their PIDs, and nobody touches them.
Fix: bar.sh's PID files now live OUTSIDE the run root it removes, and a PID file is deleted only once its
process is seen gone.

### PERF-5 worst cut (bench-worstcut, built and green, not landed)
- Deterministic across 2 runs: base at step 1 (588 B World), tail 18,850,208 B = 0.999 of tailMax 18,876,520,
  452 records, 28,928 one-slot write steps.
- Reopen: 20.374 trie hashes per step, 0 verifies. Follower re-derivation: 20.374 hashes, 1.000 verify.
- 2 min 16 s and 87 MB per run.
- ROOT: a standing-only verdict row. GATES-6 is asked for the mechanism. It lands together with the bar
  trie-hashes ceiling of 19.5 (ROOT-ruled; 17 runs gave 14.37–16.96, mean 15.475, sd 0.663).
- RUNBOOK "measuring THE BAR" text drafted at hbox logs/perf1-runbook-bar.md, for OPS-5.

### LANDED c392f51 (perf:, PERF-5 + bar trie-hashes 19.5 + PID files outside the root)
- standing:bench-worstcut is in runs.tsv (GATES-17). Pre-push printed `run standing:bench-worstcut: NOT RUN(standing-only)`.
- WASTE worstcut: reopen 20.374 hashes and 0.000 verifies per step; audit 20.374 and 1.000. bar trie-hashes-per-step:
  ceiling 19.5, measured 16.963.
- Plant (c) quoted in the commit (waste.py reds the four worstcut rows when they are unmeasured).
- Kill test: bar.sh SIGKILLed mid-run left 4 PID files in ~/.nd-bar naming live supervisors. All four were
  stopped by their files.
- GATES-6 runs the first standing that includes the row. OPS-5 flips RUNBOOK §8's worst-cut paragraph to RAN on
  this hash.

## PERF-1 CONTINUATION (for PERF-2, written by PERF-1 at ~490K tokens: past the 350K line, so I stop here)

State: everything landed, at c392f51. The worktree hbox:/tank/dregg-build/nanodregg/wt/perf is clean (git checkout
--detach main before you edit). Landings: de718bf (bar in standing, script: row), 5f7c58d (bench-count, midpoint
seal), c392f51 (bench-worstcut standing row, bar trie-hashes 19.5, PID files outside the run root).

Next, in ROOT's order (ROOT 2026-10-18):
1. bench-worstcut, two more tail shapes to the same 99 % cut.
   Bench/WorstCut.lean `worstcut`: the tail loop builds `call w' m [m.id, obj] (.write obj …)`.
   - Add a mode, or one run that builds three Stores (SCRATCH/W-writes, W-births, W-retires), for a tail of
     births (`.create none [] [(stateBase, nat i)]`, pins [m.id]) and a tail of retires.
   - Retire: find the Body constructor in Kernel/Receive/Call.lean (`inductive Body`). It credits weight back
     and touches heads. To retire you need cells to retire, so make them in the base phase.
   - Pin the worst of the three per row (reopen and audit hashes/step, verifies/step). Print all three.
   - If births or retires cost more, the pinned rows move UP once, with the WASTE justification line
     "WASTE: worstcut: the first measurement of this tail" (ROOT: the one legitimate upward move).
   - Watch: a births tail grows the World, so the allowance (allowanceMax) and worldBytesMax may bind before
     tailMax. Each tail must still reach ≥ 99 % of tailMax, and the exe already fails below that.
   - A run is ~2 min 16 s per shape. Three shapes plus the control is ~9 min, which is acceptable in standing
     only. Better: make the control stop after the first shape's cut, since its expectation is about the cut.
     GATES-6 must agree that is still "the ordinary path".
2. The worst-World axis: a standing-only bench whose base is near worldBytesMax (256 MiB, Host/Bounds.lean
   Cadence.deployed), with its reopen pinned (bytes read per allowed byte, trie hashes per step folded, base
   decode). The memory and wall time of a 256 MiB World are unknown: measure once by hand under swarm-build
   before proposing the row, and ask GATES-6 whether it fits standing.
3. THE BAR v2 waits on HOSTING-9's real resident, OPS's box and a person.

How things work (learned the hard way):
- Commit: scripts/commit from wt/perf, with `COMMIT_RETRIES=10` (main moves constantly: 5 retries failed once).
  Launch it with `nohup bash -c "exec scripts/commit -F MSG PATHS" > log 2>&1 &` then `echo $! > pidfile` on its
  OWN line. A `A && B && nohup … &` puts the whole list in a background subshell, and `$!` / variables are lost.
- The judge needs SIZE lines for every row that rises. It names them ('Lean lines (Bench)',
  'Lean modules', 'max dependents …'). A gates/ change needs GATE-CHANGE, and a cross-layer path needs
  CROSS-LAYER naming GATES-6's agreement.
- An apostrophe inside `ssh hbox '…'` breaks zsh: write patch scripts locally and scp them (logs/perf1-p*.py).
- bar.sh: custody needs a $HOME chain (all of /tank is 775). `--root` is the Store device. PID files are in
  ~/.nd-bar. `--standing` is serial and its counts are exact. Only the trie-hash count is draw-dependent.
- Plants: scripts/plant [--build] --with each unlanded path; a runs check needs --build. GATES-6's 12cadcc fixed
  the executable-mode gap.
- The two orphaned strace trees (779667, 818024) are on Ember's list. Do not touch them.

Open findings owned elsewhere:
- KERNEL-20 (from KERNEL-19's handoff): a recorded refusal costs two verifies; the contention budget shape;
  cv 7380, the draw-independent hash count.
- PROTOCOL-13: cv 01a14edf-6f12 (stale and the refusal budget).
- OPS-5 b0d33d2: RUNBOOK §8 worst-cut paragraph RAN (c392f51); PID-file fact added.
- GATES-6: first standing with the worstcut row GREEN at c392f512db4b (waste pinned 56, unpinned 0); bench-worstcut control read red, run ok; WASTE worstcut 20.374 / 0.000 / 20.374 / 1.000 measured.

## PERF-2 (2026-10-18, successor of PERF-1; worktree hbox:/tank/dregg-build/nanodregg/wt/perf)

### Item 1: the worst cut in three tail shapes (PERF-6), built, measured, not landed yet
- Bench/WorstCut.lean was split into `build` (one Store per shape, built concurrently as dedicated tasks)
  and `count` (run serially, because `captured` swaps the process's stderr). The Stores are
  SCRATCH/{writes,births,retires}.
- Retires: grants (`.grant obj m.id [.mutate] none`, pins [m.id]) are born before the base. Each round
  bears grants up to the need, seals, samples one 64-revoke record frame on the World, and re-derives
  need = 64*(tailMax(base)/frame+2). It converged at 32,384 grants with a 5.76 MB base.
- LESSON: a Writer's segment lock is released only when its File is freed (there is no close API). A
  writer held in a live variable across `sealBase` gives `reopen for the seal locked`. So no writer
  stays live across a seal: sealBase and bearGrants each open their own, and it dies when they return.
- Lean: `let mut wr ← match … with | … => return …` gave "Unknown identifier wr". Bind it with a plain
  let first, then `let mut`.
- Measured (deterministic; runs 2 and 3 identical): writes 20.374, births 33.031, retires 33.959
  reopen/audit hashes per step; verifies 0/1 in all three; tailMax binds first in each shape.
  Honest run 4:39 (concurrent; 8:03 serial), 168 MB. Control 2:03, writes only.
- waste.tsv: the two hash rows go 20.374 -> 33.959. Commit message: hbox logs/perf2-msg1.txt. Waiting on
  GATES-6's yes (asked: the waste rows, and "the control builds writes alone" counting as the ordinary
  path).

### Item 2 lead: the worst World. worldBytesMax is UNREACHABLE; the allowance binds at about 1/6 of it
Draft Bench/WorstWorld.lean, with a lakefile entry `bench-worstworld` (uncommitted in wt/perf). It births
60 KB data objects until submit refuses:
- `rejected overAllowance` after 743 births;
- the base World is 44,702,268 B = 0.167 of worldBytesMax, with weight 44,646,433 (bytes/weight 1.001);
- allowance left 25,241 of 134,217,728;
- 27 s to build, reopen 775 ms (load ~11), RSS 793 MB.
Why: Turn.weight = logWeight + growth. A create's cell bytes appear in the event, in the logged creates,
AND in the growth, so the allowance (a lifetime budget for log + World) buys at most ~1/3 of itself as
World. HOST-14's "256 MiB ≈ 900 BAR stores", and Bounds' "the other half is headroom for encoding
overhead", rest on a ratio the code does not have: encoding/weight is 1.001 and the charge is ~3x.
Base decode hashes are not counted yet (decode runs under X.env inside Codec.Kernel.world). Counting them
needs a decode with `Codec.Kernel.world (countingEnv X.env) digestCodec`.
- KERNEL-20 said FINDING 3 was fixed in c18e028 (KERNEL-53). Re-measured on c18e028 with two full 1000-record bar runs:
  follower re-derivation verifies are 506 over 502 tail steps with 4 stale refusals, and 518 over 508. So it still
  reads 2 verifies per recorded refusal. Sent to KERNEL-20 and ROOT; not closed by measurement.
- Another lane is now editing wt/perf (Bench/WorstCut.lean, perf.md, a staged waste.tsv). PERF-1 touched none of
  it. The stale worstcut row text "(a recorded refusal would cost two…)" belongs to that lane, once FINDING 3 is
  really fixed.

### Landed by PERF-2
- 2d2189e PERF-6: three tail shapes. Worst per row: retires 33.959 trie hashes/step (writes 20.374, births 33.031). The control is on the LAST shape (GATES-6's condition).
- a18d6ea: a WRONG row-text "correction" (audit costs two). I wrote it from ROOT's relay of PERF-1's stale 506/502 without measuring. Superseded by ce23f2e.
- ce23f2e PERF-7: bar.sh refuses binaries that are not the tree's (lake --no-build; cargo JSON `fresh` at the exact paths; RED binaries-stale / binaries-foreign / dirty-tree on --record). It prints the build and the SHA-256s. bench-count prints `COUNT kinds turns T refusals R`. Measured 217/217 (19 refusals in the tail) and 205/205 (7): 1.000 verifies per step, refusals included.
- OPS-5 placed the bar v2 RUNBOOK text in eaa591a, PENDING. Two items unconfirmed: the resident's round (HOSTING-27) and drop_caches as root.

### Worst World (ROOT's framing: worldBytesMax is the READER's bound). Measured by hand, NOT landed
Draft: hbox wt/perf Bench/WorstWorld.lean + WorstWorldMain.lean + the lakefile entry. Copies are in
logs/perf2-wip/ and logs/perf2-lakefile.patch; this worktree is dirty with them now.
- `bench-worstworld SCRATCH synthetic N`: N tombstones (the smallest entry, 35 B each) at hashed ids, put
  in the genesis trie, written by Host.genesis (the deployed seal and MAC), opened by openFollower. The
  base decode is counted under countingEnv (bytes reach the decode through an IO.Ref).
  - At N=7,669,000: base 268,415,416 B = 1.000 of worldBytesMax. Decode trie-hashes 15,338,003, which is
    2.000 per entry exactly (also 2.000 at N=200k).
  - **Reopen 120.7 s** (hbox load ~12-15/24 cpus; not judged), against THE BAR's 60 s reopen limit.
  - Build 13.8 min; RSS 10.1 GB; 17:43 total.
- Honest (`bench-worstworld SCRATCH [STATE_BYTES]`): 16-byte births until overAllowance. 204,288 births,
  22.2 MB, reopen 2.3 s, 11 min build. 60 KB cells: 44.7 MB, reopen 0.78 s.
- A proposal for the row: the per-entry decode hash count is scale-free (2.000), so a scaled synthetic
  run (200k entries, 17 s, 246 MB) can pin it in standing, with the worldBytesMax total derived. The
  full run is too heavy for standing. The reopen at worldBytesMax exceeding 60 s is input for the
  KERNEL-20/HOST-14 worldBytesMax decision.

### ROOT ruling on worst World (2026-10-18) and PERF-8 prep
- (a) A scaled synthetic row in standing; (b) the full 256 MiB run and (c) the honest run by hand, recorded in PERF-8.
  The 120.7 s finding goes to KERNEL-21 / HOST-14 (KERNEL-55 option B, ~84-87 MB). When the bound is set:
  re-pin the derived total and name the bound in the row text.
- Built: bench-worstworld `synthetic N` / `honest [B]`. The control flips the roots (no trivial fail). The
  argument parse refuses non-numbers. Standing row `{fresh} synthetic 200000`: 17 s, 178 MB, WASTE 2.000.
- The diff is applied in wt/perf at b9ce5a7. Message: logs/perf2-msg4.txt. WAITING on GATES-6's yes.
- Asked HOSTING-10 (ac5ffc739bd9133a3) for the resident's round; OPS-5 told drop_caches = Ember's operator step.
  Evidence sent to HOST-14 (a4d3aa9099adf145c).
- OPS-5 46ae495: §8 v2 says Ember drops caches as root, then says go. Resident round still open (HOSTING-10).
- HOSTING-10: resident round = ring (friend's invoke BELL) + answer (resident's one invoke, 1 s tick, one ask per ring, never re-asked). Relayed to OPS-5 for §8. HOSTING-27 hash to come.
- HOST-14: KERNEL-55 = option B; worldBytesMax derived from worldWeightMax 75,505,125 → ~84.9–87.7 MB (ROOT Q2). Lands after KERNEL-21's 54 day + CODEC equality; HOST-14 sends the number + hash. Pin nothing to it until then. Design: hbox logs/host14-k54-k55.md.
- LANDED 35daeab PERF-8: bench-worstworld (synthetic N | honest [B]), standing:bench-worstworld {fresh} synthetic 200000, WASTE worstworld decode-trie-hashes-per-entry 2.000. GATES-6 agreed (GATES-18 next: CROSS-LAYER must name each foreign path's owner layer).
- OPS-5 d5a8996: §8 v2 carries HOSTING-10's round text, PENDING HOSTING-27's hash.
OPEN (for me or a successor): (1) KERNEL-55's bound from HOST-14: name it in the worstworld row and re-pin the derived total; (2) HOSTING-27's hash goes to OPS-5; (3) quote GATES-6's first standing line for bench-worstworld in the log; (4) the worstcut critique: a fourth tail shape (row inserts, transfers) is unmeasured.
wt/perf is clean at 35daeab. Nothing is running.
- PROTOCOL-16 (aaa9e34f332c75994) asked to make the rows bar's LIVE lines judged counts. Agreed: WASTE-shaped, gates/waste.tsv op `rowbar` (not `bar`), per-unit ratios (frames/steps per write, verifies/trie-hashes per step, reopen entries/bytes per write); ms lines stay LIVE notes, never judged; plants must assert their mutation.
- HOSTING-27 landed 0e4d57f (exe resident, pkg/resident.conf, observe,invoke:0 grant, model allowance, tick 1 s; launcher/tests/resident_bell.rs). Forwarded to OPS-5 for §8.
- OPS-5 07f31d6: §8 v2 names the resident 0e4d57f; PENDING = box, a person per friend machine, Ember drop_caches. Unrun.
- Verified at source (main): 0e4d57f is HOSTING-27; Hosting/Resident/Bell.lean:32-35 conf shape matches §8; Run.lean:82 tickMs 1000.
- ROOT asked me to hold landings ~15-20 min for CLIENT-29 (nd-members). I have no landing pending, so nothing to hold.
- LANG-18 (aab588a19107411ac): LANG-58 PROPOSED, the Bell as a queue (ring/answer are row-only turns, rings commute; resident reads pending 16 + rings per answer). At its landing: §8 'busy' text goes to OPS-5, and a rows tail joins bench-worstcut's shapes. Proposal: hbox logs/lang18-LANG-58.md.
- CLIENT-29 landed ecb02bf (ROOT's hold is over; I had none queued). HOSTING-11 (a1cf90a9c83d50c8e) confirms the queue round: ring 77 steps/116 ticks, answer 77/116; tick = read BELL pending 64. §8 (lines ~584-590) is wrong under the queue: replacement goes to OPS-5 when LANG-58+HOSTING-31 lands (not on main at f68f968).
- HOSTING-11: queue refusals relationFull (64 pending, rings 1024 until retired), keyTaken (same ringer, same view). §8 replacement drafted: scratchpad perf2/perf2-s8-queue.md; send it to OPS-5 with LANG-18's hash.
- LANG-58 + HOSTING-31 landed 96179fb (verified on main). §8 queue text sent to OPS-5. Next on my side: a rows tail for bench-worstcut (ring = 2 inserts, answer = insert+retract) is now a deployed case: measure it.

## PERF-2 CONTINUATION (written by PERF-2, ~270K tokens; a successor or a resumed PERF-2 starts here)
State: main has PERF-6 2d2189e, a18d6ea (superseded), PERF-7 ce23f2e, PERF-8 35daeab. wt/perf is clean (`git checkout --detach main` before editing). Nothing is running. Every logs/perf2-* file is mine.
§8 (OPS-5 a5d4126a74c378ee7): v2 text landed eaa591a/46ae495/d5a8996/07f31d6. The queue round text for 96179fb was sent to OPS-5 (logs/perf2-s8-queue.md). It is PENDING only on the box, the friends' machines and Ember's cache drop.
Open, in order:
1. KERNEL-55's bound (HOST-14 a4d3aa9099adf145c sends the number + hash; ~84.9–87.7 MB from worldWeightMax 75,505,125): edit the worstworld row text to name it. The bench derives its total from Cadence.deployed.worldBytesMax, so after the HOST commit the printed derived total moves by itself; quote it in a `perf:` text-only commit (CROSS-LAYER naming GATES for gates/waste.tsv, per GATES-18).
2. GATES-6's first standing line for bench-worstworld: record it here.
3. A rows tail for bench-worstcut (PERF-6 critique, now deployed by LANG-58): ring = 2 row inserts, answer = 1 insert + 1 retract. A pure ring tail meets relationFull at 64 pending, and `rings` caps at 1024 until the owner retires answered ones. So the deployed rows tail is ring/answer(/retire) cycles on an installed Bell, which needs the Bell package installed in the bench's base. Find how Lang/Journey.lean (LB4/LB5c/LB7) installs and rings it, reuse that, and add it as a fourth shape in Bench/WorstCut.lean (the build/count split takes a new Shape). If rows cost more hashes/step than retires' 33.959, that is a first-measurement move again: ask ROOT first, since the ruling said "never again" for the three tails.
4. PROTOCOL-16 (aaa9e34f332c75994) builds the rows bar's judged counts as WASTE op `rowbar` (my agreement above): review its rows when it asks.
Lessons this session: a Writer's lock lives until its File is freed, so never hold one across a seal. Never write a row text from a relayed claim: measure it (a18d6ea). bar.sh now refuses stale binaries; run it on a clean tree. GATES-18: CROSS-LAYER names each foreign path's owner layer.
- LANDED da63f5b PERF-9: the rows shape (Bell installed from world/resident/Bell.ob; ring/answer/retire cycles; second founder = the resident). rows 28.804 < retires 33.938, so no rise. Both hash ceilings fall 33.959 -> 33.938 (the kernel moved between 2d2189e and 96179fb). The control reads `FAIL rows: harness-control …`. Honest 7:08, control 9:02, 170 MB.
CONTINUATION UPDATE (PERF-2 stops here, ~310K): item 3 is DONE. Open: (1) KERNEL-55's bound from HOST-14: name it in the worstworld row and re-pin the derived total; (2) GATES-6's first standing lines for bench-worstworld and four-shape bench-worstcut; (4) review PROTOCOL-16/17's rowbar rows when staged. wt/perf is clean. Nothing is running.

## PERF-3 (2026-10-20, successor of PERF-2; worktree hbox:/tank/dregg-build/nanodregg/wt/perf; scratch logs/perf3-*)
Measured on main 359e9e8, clean tree, load1 12-18 (clocks reported only):
- worstworld 200k: 400,003 / 200,002 = 2.000; derived at worldBytesMax 91,914,346 (HOST-57): 2,626,114 entries, 5,252,215.
  By hand at the bound (synthetic 2626112, base 91,914,338 B): 5,252,227 = 2E-1 exactly (as at 200k and 2^28), reopen 56.3 s,
  5:36, 2.9 GB. synthetic 2626113 -> `FAIL Host.genesis worldTooLarge` (the bound is exact at the seal). PERF-8's 256 MiB run = past the bound.
- worstcut (7:59, 751 MB): writes 19.382, births 32.036, retires 32.938 (worst), rows 24.892. The cell shapes fall exactly 1.000/step
  (16f3b9f rootsOf); rows = LANG-59's 24.892, confirmed. LANG-19's "worst stays 33.938" predates 16f3b9f. Ceilings 33.938 -> 32.938.
- bar.sh --records 60 --standing: PASS; bench-count 27 steps, trie-hashes 402 required 402 verifies 27 -> trie-hashes-per-required 1.000
  (KERNEL-22's instrument: Required.step per step + Required.emptyRoots; FAIL required on a count below). --harness-control RED with all four fired.
- PROTOCOL-53 (rowbar): not started on the PROTOCOL side (PROTOCOL-LOG); nothing to agree yet. GATES-8's first standing lines: none received yet.
- Prepared in wt/perf (uncommitted, ROOT HOLD for GATES-19): waste.tsv worstcut/worstworld texts + ceilings, Bench/WorstWorld.lean text,
  perf.md PERF-10, RUNBOOK §8 under LANG-59 (cross-layer OPS -> ROOT). Message: scratchpad msg / hbox logs/perf3-msg1.txt.
- LANDED bfdff2d PERF-10 (after the 35-min GATES-19 hold expired; the first attempt was refused by SIZE (+1 Bench line), so the comment was kept at its line count). Rows: worstcut trie-hash ceilings 33.938 -> 32.938; worstworld text names 91,914,346 B. RUNBOOK §8 cross-layer (OPS -> ROOT). Both bench controls fire by name (re-run by hand). ROOT told.
- Open for a successor: PROTOCOL-53 rowbar rows (agree when PROTOCOL-19 stages them); GATES-8's first standing lines for bench-worstworld / four-shape worstcut (record here); THE BAR v2 PENDING (box, friends, drop_caches). At-bound reopen 56.3 s loaded vs 60 s: v2 measures the quiet margin.
wt/perf is clean at bfdff2d. Nothing is running.

## PERF-3 CONTINUATION (PERF-3 stops here, clean; a successor or a resumed PERF-3 starts here)
State: main has PERF-10 bfdff2d; GATES-19 landed 1a6163b (hold lifted). wt/perf is detached at main and clean. Nothing is running. Every logs/perf3-* file on hbox is mine (the by-hand logs: perf3-wwbound.log, perf3-wwpast.log, perf3-wc.log, perf3-bar.log, perf3-barctl.log, perf3-wwctl.log, perf3-wcctl.log).
Open, all waiting on another lane:
1. GATES-8 (a5308a6ab02a9d9a6) runs standing on 1a6163b and sends the first standing lines for bench-worstworld and the four-shape bench-worstcut: record them here. Expected: worstcut worst 32.938 (retires), worstworld 2.000 with 5,252,215 derived at 91,914,346.
2. PROTOCOL-19 (a7b300287de0afe72) builds PROTOCOL-53, the `WASTE rowbar` rows in gates/waste.tsv, after PROTOCOL-56 and the BEHIND finality. Agree them by PERF-2's terms: per unit of work, the ms lines stay unjudged LIVE notes, and each plant asserts that its mutation happened.
3. THE BAR v2 stays PENDING on Ember (the box, the friends' machines, drop_caches). When it runs, measure the cold reopen of a base AT 91,914,346 B. It took 56.3 s loaded against the 60 s limit; if it fails quiet, worldBytesMax is the knob (HOST).
Lessons: measure, never relay. LANG-19's "worst 33.938" was true at c100be5 and false at 16f3b9f. A Bench comment line counts toward SIZE: keep the line count, or add a SIZE: line.

## PERF-4 (2026-10-21, successor of PERF-3; worktree hbox:/tank/dregg-build/nanodregg/wt/perf; scratch logs/perf4-*)
Measured on main 258c273 (KERNEL-23's one-pass commit), clean tree, all under SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build.
bench-worstcut peaks at 746 MB, so 6G is enough. Runner logs/perf4-run.sh; summary + loads logs/perf4-summary.log.
- worstcut (11:14, load1 13.6 -> 29.3): writes 19.382 -> 18.661, births 32.036 -> 30.595, retires 32.938 -> 32.217 (worst),
  rows 24.892 -> 23.516. Steps, records and tail bytes are unchanged. The rows base grew 23,467 -> 23,647 B (1e90c0b/7c09186 are in range).
  Honest and control counts are identical. Ceilings 32.938 -> 32.217. Not separated at 258c273^ (attribution in PERF-11).
- worstworld 200k: 2.000 (400,003 / 200,002); derived 5,252,215 at 91,914,346, unchanged. 18.7 s, load1 5.7.
- bar.sh --records 60 --standing: PASS, 365/365 = 1.000 exact, verifies 27/27, 13.519 h/step (draw). Load1 7.7.
  The Store now sits on nvme0n1p4 ($HOME), not tank. The --harness-control run is RED with all four fired.
- Controls: worstcut `FAIL rows: harness-control …`, worstworld `FAIL harness-control: the decoded roots …`.
- PROTOCOL-53 rowbar: AGREED with PROTOCOL-20 (3 rows; per-byte not per-record; entries row dropped as unfalsifiable).
  PROTOCOL-20 lands a one-line amendment naming PERF-4. c53 was in its judge naming ROOT for PERF.
- GATES-9 first standing lines (bench-worstworld, four-shape worstcut): none received yet.
- Commit PERF-11 (waste.tsv ceilings + texts, decisions/perf.md PERF-11, RUNBOOK §8 cross-layer OPS-6): judge launched
  logs/perf4-commit1.log. NOTE: perf4-commit1.pid holds the outer `bash -c` (3850411); the scripts/commit pid is its child 3850414.
- LANDED 41e041f PERF-11 (pushed). Attempt 1 ran standing:bench-worstcut/worstworld and was GREEN against 32.217. Attempts 2-6 (GATES-20 read-sets) did NOT RUN them: `inputs unchanged`, because waste.tsv is the comparator, not a read. Displaced 5 times
  by main moving (GATES-20 145283a, PROTOCOL-53 a08a7d0 rowbar, OPS 8547e9b, HOST 35dbf99: none touches a measured runtime path).
  It landed as head by CAS.
## PERF-4 CONTINUATION (PERF-4 stops here, clean)
State: wt/perf is at main and clean. Nothing is running. Every logs/perf4-* file is mine.
Open: (1) GATES-9's first standing lines for bench-worstworld and the four-shape worstcut (expect 32.217 worst, 2.000): record them here.
(2) THE BAR v2 is PENDING (box, friends, drop_caches); measure the at-bound cold reopen (56.3 s loaded, PERF-10).
(3) PERF-11 critique: a mixed births+retires tail was not tried, and the batch may share fewer nodes there. A candidate fifth shape (ask ROOT: a rise would be a first measurement).
## PERF-6 (2026-10-21, successor of PERF-5, which wrote no section; worktree hbox:/tank/dregg-build/nanodregg/wt/perf; scratch logs/perf6-*)
- PERF-12 saved as logs/perf6-saved.patch (1123 lines, from e86f237). wt/perf reset to c8ebb06 and the patch applied with --3way: clean,
  and `git diff HEAD` is byte-identical to the saved patch. 12 paths are staged.
- Build (logs/perf6-build1.log): the four exes plus bench-worstworld, green.
- One run on c8ebb06 (logs/perf6-run.sh, perf6-both.sh; the four at once, each under SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build).
  The counts are identical to PERF-5's: writes 539816/28928 = 18.661, births 1012318/33088 = 30.595, retires 1041249/32320 = 32.217,
  rows 342925/16448 = 20.849; verifies 0 / 1.000.
  Honest walls 117/132/232/283 s (load1 11.5 -> 13-17). Control walls 142/164/273/306 s (load1 17.1 -> 12-18). Every control printed
  `FAIL <shape>: harness-control`. RSS was at most 191 MB. The rows re-derivation took 130.5 s (PERF-5: 196.7 s at a higher load).
- Plants re-run on c8ebb06 (logs/perf6-plants.py/.out): the same verdicts as PERF-5's.
- ROOT's rulings were written into decisions/perf.md PERF-12: LANG cv task 01a1558a-1644 (the package check cached per (package id, call));
  standing stays serial, GATES-10 does concurrent standing (GATES-20g). The c8ebb06 table was added, and the RUNBOOK §8 clocks line updated.
- Commit attempt 1 (logs/perf6-commit1.log, msg logs/perf6-msg.txt) was REFUSED with nothing written:
  (a) `--reverts c392f51` was refused as unneeded. Deleting the runs.tsv row does not trip stale, so the flag is dropped.
  (b) A FALSE `stale path: lakefile.lean` against 35daeab (PERF-8 added bench-worstworld right after the old bench-worstcut lines,
  which served as the hunk's context). Deleting that context makes rebase.lacks()'s merge-file re-insert the worstworld block,
  which reads as "lacking". Reproduced by logs/perf6-lacks.py, and any layout trips it. This is a GATES defect.
  I asked ROOT for a ruling: (A) --reverts 35daeab421fa with an annotated false REVERTS note, or (B) GATES-10 fixes lacks() first.
- ROOT ruled (B). GATES-10 landed a108b15 (GATES-20b′), and the stale false positive is gone.
- The main that moved under the wait carried c15487e (a retract joins the rows batch). wt/perf was rebased onto c15487e (logs/perf6-saved2.patch).
  The rebuild re-ran honest2 (load1 11.0 -> 13.1): writes/births/retires unchanged; rows 342925 -> 331960 = 20.182 (not separated;
  c15487e is the commit in range that touches row retracts). worstcut-rows trie rows re-pinned at 20.182 (waste.tsv, RUNBOOK, PERF-12).
- Attempt 2 (logs/perf6-commit2.log), REFUSED by the gates PERF-5 never ran: C3 (the Signer theorems sat in a def-module), C7 (each exe root
  declared shape defs), 5 SIZE lines, LAKE-DROP. Fixed: the theorems moved to Bench/Proofs/WorstCut.lean, and each exe root is now
  Bench/WorstCut<Shape>Main.lean (main only). closure.py ok, build green, the writes smoke 18.661 PASS, SIZE and LAKE-DROP lines in the message.
  Every run in attempt 2 was ok (63 runs of 49 exes). The cargo `test failed` lines in that log are runs' stderr, not the verdict.
- HOST-20 (a49735f6091ae518b) moves baseRecordMax 91,914,458 -> 91,914,474 (+16; frame bound = baseRecordMax + 4 + 32). No PERF number pins it.
  Prose to update AFTER its hash: gates/waste.tsv:61 (worstworld source text), decisions/perf.md:527, deploy/RUNBOOK.md:612.
- Attempt 3: logs/perf6-commit3.log (pid file perf6-commit3.pid).
- Attempt 5 was RED only on one missing `SIZE: Lean proof-modules` line; I added it. Before relaunching I ran the offline source gates
  (gates/check.py against main, logs/perf6-changed.txt). Attempts 3, 4 and 6 were each refused after 30 min with every judge slot busy
  (attempt 6 was green once, then displaced).
- LANDED 21e4470 PERF-12 (attempt 7, pushed). In the green judge (gate tree 013685ed15fa): writes 18.661, births 30.595, retires 32.217, rows 20.182,
  every control fired, waste-measured ok (79 pinned). The CAS retry reused those verdicts by traced key.
## PERF-6 CONTINUATION
State: wt/perf is at main (21e4470 or later). Nothing of mine is running. Every logs/perf6-* file is mine.
ROOT HOLD: start no scripts/commit until ROOT sends GATES-22's hash.
Open: (1) after HOST-20's hash (a49735f6091ae518b): prose 91,914,458 -> 91,914,474 in gates/waste.tsv:61 (worstworld source text),
decisions/perf.md:527, deploy/RUNBOOK.md:612 (a base past Log.frameMax of baseRecordMax 91,914,474 is refused baseTooLarge).
(2) When LANG's package-check cache (cv 01a1558a-1644) lands: re-measure the rows clocks and packages-checked-per-call, then re-pin.
(3) THE BAR v2 stays Ember's (quiet box, a friend, drop_caches). (4) PERF-4's candidate fifth shape (a mixed births+retires tail): ask ROOT.
(5) First standing lines for the four shape rows and bench-worstworld (GATES-10's concurrent standing, GATES-20g).
- HOST-64 landed as eb7028d (baseRecordMax 91,914,474). wt/perf is at eb7028d with the three prose edits staged in the working tree
  (logs/perf6-brm.py); message logs/perf6-msg2.txt. Re-measured on eb7028d: every count unchanged (logs/perf6-honest3-*, perf6-ww.out).
  Launch waits for ROOT's GATES-22 hash (the HOLD).
- GATES-22 (e568634 + fixes 2a0de84, fa8fec3) was on main and other lanes were landing again. LANDED 744d00c (the baseRecordMax 91,914,474 prose)
  by the GATES-22 fast path (source gates + build only; the next convergence judges the rest). Continuation open item (1) is DONE.
