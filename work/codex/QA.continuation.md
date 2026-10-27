# QA — continuation: PARKED (real 2026-10-27, QA-2)

Ember (10-27): Q3 and Q4 are rechecking; stop. Q2 landed (nano `5b1c3255`). The only QA work worth a
lane is Q5 and Q6: see the first page of `redregg/work/promo/DESIGN-QA.md`. A successor starts there,
not here.

- Parked work, not to be landed as is: `hbox:qa-scratch/q3q4-parked.patch`; the uncommitted tree
  is in `wt/qa`.
- Clean landing worktree: `wt/qa-q2` (at 5b1c3255).
- The old FAST lander `qa-scratch/commit2.pid` was left alive, as instructed.

---
(previous continuation, for history)

# QA — continuation (real 2026-10-26, written by the QA lane at ~290K tokens)

Read first: `redregg/work/promo/DESIGN-QA.md` (the program Q1–Q8), then `QA.report.md` (dated log),
then `decisions/gates.md` GATES-27 and 27 (b) in nano.

## State

- **Q1 LANDED** as nano main `5527b018`, after a full judge (GREEN three times; displaced twice).
  - `gates/interp.py` compares the compiled exe with `lake env lean --run`. The two runs must be
    byte-identical, the compiled run must hold a TRACE line, and the control gives the interpreter
    the next seed.
  - `Kernel/Sim/Gen.lean` gained `traceLine`.
  - runs.tsv gained the row `script:gates/interp.py`.
- **Q2 (first half)**: ledger-sim and hosting-sim join the row, with one printer,
  `traceLine E label st marks`. The landing is in flight (fast judge): log
  `/tank/dregg-build/nanodregg/qa-scratch/commit2.log`, pid file `commit2.pid`. If it is not on
  main, read the log; the message is `qa-scratch/msg2.txt`, the lander `qa-scratch/land2.sh`.
- Worktree: `/tank/dregg-build/nanodregg/wt/qa` (hbox). Scratch:
  `/tank/dregg-build/nanodregg/qa-scratch`.
  - `bg.sh NAME CMD…` runs CMD detached with `NAME.log` and `NAME.pid`.
  - `onetree/gates/runs.tsv` is a one-row table for `gates/runs.py . --table`. `--table` reads the
    tree root from the table's grandparent directory, so the table must sit at `X/gates/runs.tsv`.
  - `mutant-bin/kernel-sim` is the seed-domain mutant used by GATES-27's plant.
  - `libndhost-mods.so` + `stub.c` is the dynlib shim that runs `host` interpreted (DESIGN-QA §2.3).

## Next, in order

1. **Q2, second half.**
   - **lang-journey**: LANG adds a TRACE line. Its sessions sit in the `Journey.register`
     registry, so the line goes where `Main` iterates them. It is 349 s interpreted, ~220 s of that
     module initialisation: measure what initialisation computes; a closed term evaluated at init
     is interpreted slowly.
   - **host-sim**: 515 s interpreted against the 600 s deadline. Give it a smaller run, e.g. one
     crash phase per run, before it joins the row.
   - **rows**: run by name, e.g. a deployed-parameter row with Ed25519.
2. **Q3, the interpreter follower** (DESIGN-QA §2.3).
   - First MEASURE an interpreted catch-up over a 1000-record writer Store. bar.sh removes its
     Stores on exit, so a measurement either adds a keep flag or drives `host serve` directly.
   - Then make the dynlib shim a lake target built from source, not hand `cc`.
   - Shape (b) first: a one-shot catch-up of `host follow`'s own `absorbStep` path. Not
     `Kernel.Receive.audit`: that is the twin of A9.
3. **Q4** belongs to CODEC: codec-vectors three ways, plus multi-block SHA-512 and RFC 8032 TEST 1024.
4. **Q6** has the biggest yield: a generated adversarial Host over `Protocol.Command`, judged by the
   member spec. It retires the 28 `Sys` booleans.

## Traps met

- `git -C main worktree add wt/qa` is relative to `main/`. Use the absolute destination.
- In ssh one-liners, `A && B && nohup X > log &` backgrounds the whole `&&` list, so a variable set
  in A is empty for a later `echo $! > $S/…`. Use `qa-scratch/bg.sh`.
- `pgrep -fl <pattern in your own ssh command>` matches itself.
- kernel-sim's own `--harness-control` changes nothing below 16 seeds. It is no control for a
  one-seed run.
