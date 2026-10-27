# FIX-HOSTING report (nanodregg Hosting/**, gates/tcb.tsv stdio-leg row)

Worktrees: hbox `/tank/dregg-build/nanodregg/wt/fixhosting` (builds, landings via scripts/commit), local
`~/dev/nanodregg-wt/fixhosting` (edits, rsynced). Builds: `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build`,
`Hosting.Proofs.Reply` EXCLUDED everywhere (OOMs at 10 GB alone, HOSTING-43; no card here touches its closure).

- 2026-10-24 READ: COLLATION-20261024 §A5/A13/A14/A20, READ-HOSTING.md whole, RULINGS R-0069/R-0071.
  FIX-GATES.report.md ABSENT (work/codex/), so the A5 plant stays a scratch theorem.
- 2026-10-24 LANDED 7332f9c (HOSTING-47, card 1, A5). Bounded form chosen over the delete (it was two lemmas:
  `Protocol.Command.step_world`, by the case split `step_keeps` used, and `step_keeps` re-derived from it).
  `journal_committed`/`answered_row_committed` now over `ReachOn S` (frames' results) + `hfresh` (no entry at the
  base), conclusion `(callBytes c ∈ pathCalls S ∧ committed) ∨ CollidesAmong (callBytes c :: pathCalls S)`.
  CROSS-LAYER PROTOCOL: new def module Protocol/Command/Frames.lean (closure C3), `Machine.eventCall` used by
  `absorbStep`, `JournalFrom` over an explicit byte list.
  MEASURED (hbox, `python3 logs/fixhosting/a5_plant.py .lake/scratch/a5`): `#statement_census` over Hosting +
  scratch plant: both new rows `ok`; the pre-restatement statement (plant `journal_committed_unbounded`) ALSO
  reads `ok` (GATES-20s's named "lucky second preimage" miss: one side of the hash equation is the premise's
  `txIdOf X c`). Handed to FIX-GATES: a hash equation with one fixed side and the other's input under an
  unguarded `∃` is the unbounded second preimage; the plant file is `logs/fixhosting/a5_plant.py` on hbox.
  MEASURED: Protocol + Host + every Hosting module but Reply, 348/349 jobs green; fast judge green.
- 2026-10-24 LANDED 37772b9 (HOSTING-48, card 2, A13 + B4 + B8). `Mem.retries`/`retriesMax = 32`/`retry`/
  `Exit.retryExhausted` (17): every tick end that schedules a retry (describe/read/invoke failure or unsettling
  exit, refused-and-unread, ask not sent) counted, settling ends reset. Theorems `tick_retry`, `tick_lt`,
  `no_refusal_repeats_forever` (over `Ticks`), `deliverAfter_unsettled` restated. `Lifetime` deleted, consumers over
  `Ticks`. MEASURED plants (hbox logs/fixhosting/plants/A13-*.build.log): unbounded retry reds retry_retried/retry_lt;
  old behind branch reds deliver_retry/deliver_lt. MEASURED row (logs/fixhosting/q8-row.log): resident_bell Q8
  `32 retries in 33 s, then retryExhausted`, whole row ok in 371 s. INFERRED: the 32 bound is a choice (critique in
  HOSTING-48: a progress-aware bound reading `behind HEIGHT TIP` is named, not built).
- 2026-10-24 NOTED coordinator correction (Ember 10-24): plants are cheap vacuity checks, not gates; A5 decided by
  what is TRUE and useful. The landed A5 choice (7332f9c) already stands on that: the bounded form is true (proved)
  and strictly more useful than the delete (it says the entry's call is on follow's own frames); the census plant
  was recorded as a measurement of the census, not as the reason for the shape.
- 2026-10-24 card 3 (HOSTING-49) judged green on build; decls lines added; re-landing (judge slots all busy ~30 min).
- 2026-10-24 card 3 (HOSTING-49): FAST GREEN on every attempt (build ok, decls ok); lander PID 2217138 still
  re-basing after 3 displacements (main moving under ~80 min judges). MEASURED plants: undecodable-as-empty reds
  read_undecodable_stops; unchecked object line reds describeOut_ok.
- 2026-10-24 card 4 (HOSTING-50, A20) READY locally, not landed: stdio-leg → stdio-relay / stdio-one-follower /
  stdio-continuation / follow-loop; the pure half of "follow's World moves only by its frames" is now a theorem
  (Hosting/Proofs/FollowAnswer.lean answer_world/answer_reach, MEASURED green); reopen cited
  (Host.Proofs.Refine.host_reopen_folds + extern:Host.File), no row. tcb.check → [] (MEASURED, local).
- 2026-10-24 PARKED past the ~400K context line; continuation: work/codex/FIX-HOSTING.continuation.md.
- 2026-10-24 FIX-HOSTING-2 took over. READ continuation + report whole; READ land49.log whole (attempt 4 of 12
  running, fast green on attempts 1-3, each displaced by main moving: 37772b9 → 0a299c8 → 167d21b → d0e3a03).
- 2026-10-24 FIX-HOSTING-2 card 4 (HOSTING-50) STRENGTHENED before landing: READ answer_world tied the step to an
  existential `kb res`, not to the frame, and answer_reach concluded `Reach` while the module doc said `ReachOn`
  of the frame's result. Restated: answer_world's step arm is `∃ v, resumeFrame.decode f.payload = .ok v ∧
  Command.step … v.1.1 v.2.1.1 = …`; answer_reach is `∃ S, (S = [] ∨ ∃ v, decode = .ok v ∧ S = [v.2.1.1]) ∧ ReachOn S`.
  HOSTING-50 record updated to say so. MEASURED: Hosting.Proofs.FollowAnswer (+ Socket docstrings) 167/167 green on
  hbox, no warnings (.lake/scratch/fa2.log in wt/fixhosting).
- 2026-10-24 13:5x FIX-HOSTING-2 card 3 (HOSTING-49): attempt 6 judged FAST RED, decls (READ land49.run1.log
  in wt/fixhosting/.lake/scratch): main's decls gate now names 10 undeclared redefinitions (TickCore, Exit,
  Exit.all, Exit.code, deliverP, describedShape, readP, readRings, textMax, tickP); each IS the point of the
  card (exit 18, the one decoder, Lang's textMax), so RESTATES-MEANING lines were added to msg49.txt. The
  worktree's SocketStrong.lean/decisions/hosting.md were set back to their card-3 text (equal to the judged tree
  b6ade0b, MEASURED by diff) for the record, then card-4 text restored after both snapshots were taken.
  ⚠ DUPLICATE LANDER: at the same minute a second agent in this same claude session (scratchpad land.sh,
  launched 13:53:09) relaunched the same card: TWO landers, 452905 (mine; its PID file was overwritten) and
  453705 (land49.pid). Identical snapshots (MEASURED: nanodregg-landers/p452905 and p453705). Neither killed
  (no PID file for mine; never stop a judge). The loser's re-base sees no diff and exits "nothing to commit"
  (scripts/commit:227, READ). msg49.txt carries the 10 lines twice (both agents appended). land49.log is
  shared by both (both truncated it); verdicts are in each pre-push's /tmp verdict file.
- 2026-10-24 ~14:05 LANDED 0c9b14e (HOSTING-49, card 3; pushed to origin). MEASURED log: fast green, decls ok
  with 23 declared changes, census over the reach ok, "landed by compare-and-swap". Lander 453705 (the other
  agent's) is the one that landed; mine (452905) is gone (READ: absent from ps; never killed by me).
- 2026-10-24 card 4 rebase: tcb.tsv conflicted with 294d1c5's five syscall-layer rows (GATES-20y, A20's
  other half, landed meanwhile): resolved = their five rows kept, stdio-leg deleted, the four HOSTING-50 rows
  after them. HOSTING-50's critique bullet saying tcb.py "compares no pin, has no rustix rows" was FALSE after
  294d1c5 and is restated to cite it. ⚠ The other agent in this session is ALSO driving card 4 in wt/fixhosting
  (it re-edited tcb.tsv/Socket.lean at 14:08 and started a build, hbuild4.log); I am NOT launching a second card-4
  lander, only watching for its land50 and checking the result.
- 2026-10-24 LANDED 0c9b14e (HOSTING-49, card 3) after 10 more RESTATES-MEANING lines main's decls judge asked for
  definitions. The worktree could not move (card 4 edits); resolved: card 4 copies 3-way merged onto 0c9b14e
  (gates/tcb.tsv conflicted with 294d1c5's new rows rustix/libc/…: kept theirs + the four new rows, stdio-leg
  deleted; tcb.check → [] MEASURED). Hosting (but Reply) 263 jobs green on 0c9b14e+card4. Card 4 lander launched.
- 2026-10-24 LANDED e87ac94 (HOSTING-50, card 4, A20). All four cards landed: 7332f9c, 37772b9, 0c9b14e, e87ac94.
- 2026-10-24 LANDED e87ac94 (HOSTING-50, card 4; pushed, origin/main = e87ac94, MEASURED by ls-remote). Lander was
  the other agent's (land50.pid in wt/fixhosting); fast green twice (build Hosting, decls ok, census over the reach
  ok), landed on attempt 2. READ the landed tree: FollowAnswer carries the frame-tied statements (decode = .ok v,
  S = [] or [v.2.1.1]), tcb.tsv has no stdio-leg row and the four rows after GATES-20y's five, the HOSTING-50
  critique cites 294d1c5. Hosting.Proofs.Reply: not built in any card (OOM at 10 GB alone; its closure untouched).
- Still open (from the continuation, unchanged): progress-aware retry bound (HOSTING-48 critique); the A5 census
  "lucky second preimage" miss (FIX-GATES's). FIX-HOSTING-2 done.
