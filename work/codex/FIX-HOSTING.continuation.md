# FIX-HOSTING continuation (parked 2026-10-24, context past the ~400K park line)

## DONE 2026-10-24: all four cards landed (7332f9c, 37772b9, 0c9b14e, e87ac94); only the 'Not done' list below remains.
## State (UPDATE 2026-10-24: card 3 LANDED 0c9b14e; card 4 merged onto it on hbox, built green, lander
running: `.lake/scratch/land50.pid` / `land50.log` in wt/fixhosting, message `.lake/scratch/msg50.txt`. If it is
refused for decls/SIZE lines, append what it prints and rerun land.sh 50. Everything below is history.)

- LANDED: 7332f9c (HOSTING-47, A5), 37772b9 (HOSTING-48, A13 + B4 + B8 + launcher Q8).
- LANDING (detached, hbox): card 3, HOSTING-49 (A14 + Q4 + B1 + B3 + B5 + B6). The first lander (PID 2217138)
  ended REFUSED after re-basing: main's decls judge now also reads DEFINITIONS, and asked 10 more
  RESTATES-MEANING lines (TickCore, deliverP, describedShape, Exit, Exit.all, Exit.code, readP, readRings,
  textMax, tickP), now appended to .lake/scratch/msg49.txt; re-launched with land.sh (new PID in the same
  PID file). Note: hbox's working Hosting/Proofs/Socket.lean and gates/tcb.tsv and FollowAnswer.lean already
  hold card 4's edits (not in card 3's path list). Old lander PID 2217138 (PID file
  /tank/dregg-build/nanodregg/wt/fixhosting/.lake/scratch/land49.pid), log .lake/scratch/land49.log in that worktree.
  Its judge reads FAST GREEN every attempt; it keeps losing the compare-and-swap (main moved 3x, ~80 min per attempt
  on a loaded box). Do NOT kill it (scripts/commit header: never stop a judge by PID). If it gives up
  ("gave up after N displacements"), rerun from hbox wt/fixhosting:
    scripts/commit -F .lake/scratch/msg49.txt Hosting/Resident/Run.lean Hosting/Resident/Bell.lean \
      Hosting/Resident/Trace.lean Hosting/Proofs/ResidentRun.lean Hosting/Proofs/Lifetime.lean \
      Hosting/Proofs/BellConform.lean Hosting/Proofs/SocketStrong.lean decisions/hosting.md
- READY, NOT YET SYNCED/LANDED: card 4, HOSTING-50 (A20), in the LOCAL worktree ~/dev/nanodregg-wt/fixhosting
  (edit there, rsync to hbox, land on hbox). Its diff vs card 3: gates/tcb.tsv (stdio-leg row replaced by
  stdio-relay, stdio-one-follower, stdio-continuation, follow-loop; `python3 -c "import tcb; tcb.check('.')"` → []),
  NEW Hosting/Proofs/FollowAnswer.lean (answer_world, answer_reach; built green on hbox), docstring edits in
  Hosting/Proofs/Socket.lean + SocketStrong.lean (`stdio-leg` → the four rows), decisions/hosting.md HOSTING-50
  appended after HOSTING-49.
  After card 3 lands: (1) local `git fetch && git reset --mixed origin/main`, then `git checkout --` every file
  that is not one of card 4's (others' landings show as reverted); (2) rsync card-4 files to hbox wt/fixhosting
  (scratchpad sync.sh does modified+untracked; check `git status` there first: rustfmt once touched
  launcher/tests/common/mod.rs, reverted); (3) build every Hosting module but Reply; (4) scripts/commit with
  subject `hosting: the stdio-leg trust row is four trusts …` + SIZE/decls lines the judge prints. The judge will
  likely ask SIZE lines for Lean modules/lines/theorems.
- Report: /Users/ember/dev/redregg/work/codex/FIX-HOSTING.report.md (append the card 3/4 hashes).

## Not done from the memo (named)
- HOSTING-48's critique: progress-aware retry bound (read `behind HEIGHT TIP`).
- A20's other half (tcb.py pin comparison, rustix/libc rows): FIX-GATES's.
- The A5 census miss (lucky second preimage, plant logs/fixhosting/a5_plant.py on hbox): FIX-GATES's.
- `Hosting.Proofs.Reply` never built in any card (OOM at 10 GB alone; untouched closure).
