# FIX-GATES continuation (parked 2026-10-24 ~09:50 EDT, ~650K tokens)

Read first: FIX-GATES.report.md beside this file (the dated log), and ROOT's two corrections of 10-24 (Ember):
- top-level-only non-vacuity, via the spec layer (FABLE-SPEC); no per-theorem machinery;
- plants are never a landing gate (CHARTER test clause, 7655145).

## In flight (detached; DO NOT kill — GATES-14: never stop a judge by its PID; wait for it)
- **Card 1 = GATES-20v (scoped)**: lander PID file `/tank/dregg-build/claude-lanes/fixgates-scratch/land-20v.pid`,
  log `land-20v.log` beside it, worktree `/tank/dregg-build/nanodregg/wt/fixgates`. Paths:
  - gates/decls.py, decls_plants.py, census.py, fast.py, runs.tsv, statement_plants.py;
  - scripts/pre-push, scripts/commit;
  - Census/Axioms.lean, Census/Statements.lean;
  - decisions/gates.md.

  Message: `fixgates-scratch/msg-20v.txt`. It was queued behind 223 (fixrust), 230 and 231 in
  `main/.git/nanodregg-queue`.
- **Card 3 = GATES-20x**: lander `land-20x.pid` / `land-20x.log`, worktree `wt/fixgates3` (at d741f5a). Paths:
  gates/waste.py, gates/waste.tsv, gates/runs.tsv, gates/bar.tsv, scripts/bar.sh, decisions/gates.md. It carries
  `--cross-layer PERF` and a `GATE-CHANGE:` line (main's waste.py cannot parse `=1`).

When a lander exits, read its log's last lines.
- Refused: `grep -E "NEW RED|RED" log` and the slot log the PRE-PUSH line names. A `PRE-EXISTING` red is main's
  (lang-journey, rows and THE BAR are red on main: cv 01a16db5-b18e).
- Landed: `git log origin/main`; the commit is pushed.

## Still to land, after card 1 is on main (they depend on its census and pre-push text)
Staged on hbox in `/tank/dregg-build/claude-lanes/fixgates-scratch/next/`:
- **Card 2 = GATES-20w**:
  1. Copy `next/card2/Census/Statements.lean` and `next/card2/gates/statement_plants.py` over the worktree's. They
     are card 1 + card 2; if card 1 landed unchanged they apply as they are.
  2. Append `next/card2/gates20w.md` to decisions/gates.md.
  3. `scripts/commit -F next/card2/msg-20w.txt Census/Statements.lean gates/statement_plants.py decisions/gates.md`.
  4. It is a FULL judge (Census/ is judge code). Add `SIZE:` lines if the size ratchet asks: Census Lean lines grow
     by about 120.
  - Tested in wt/fixgates2: tree ok over 425 disjunctions; plants GREEN; control RED.
- **Card 4 = GATES-20y**:
  1. Copy `next/card4/gates/{cbytes.py,tcb.py}` (executable).
  2. `python3 next/card4/edit10.py gates/tcb.tsv` (five syscall-layer rows; corrects the AppArmor claim).
  3. `python3 next/card4/edit11.py <worktree>`: deletes refusals.py's source pattern, adds the `cbytes scan` steps
     to scripts/pre-push in both modes, appends the cbytes and tcb rows to runs.tsv. It anchors on card 1's pre-push
     text (the `census (reach` block).
  4. Append `next/card4/gates20y.md` to decisions/gates.md.
  5. `scripts/commit -F next/card4/msg-20y.txt gates/cbytes.py gates/tcb.py gates/tcb.tsv gates/refusals.py
     scripts/pre-push gates/runs.tsv decisions/gates.md`.
  - Tested in wt/fixgates2: tcb ok (four host pins compared on hbox); tcb plants GREEN; cbytes vectors GREEN; scan
    clean; refusals ok.

Each launch: `nohup bash -c 'exec env SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 scripts/commit -F MSG PATHS' > LOG 2>&1
& echo $! > PIDFILE`, from a worktree at main's tip (`git checkout --detach origin/main` after `git fetch origin`).

## Open items (cv)
- 01a16d97-2a72: DELETES as a weakening door. Under the ruling this may be the spec layer's; close it or re-scope.
- 01a16d97-2a86: re-pin GATES-20t's historical decls plants H1–H4 against GATES-20v's redefinition rule.
- 01a16db5-b18e: THE BAR and lang-journey are RED on main since f9657bd (`refused/rejected stale`).

## Cleanup owed (my own files only)
- Worktrees `/tank/dregg-build/nanodregg/wt/fixgates2` and `wt/fixgates3` (each with a ~1 GB `.lake` copy; fixgates3
  has a cargo target too), and `/tank/dregg-build/claude-lanes/fixgates-scratch/` (scratch: caches, plant trees,
  real/real3 judge caches).
- Remove fixgates2 when cards 2 and 4 have landed, and fixgates3 when card 3 has landed (`git worktree remove`).
