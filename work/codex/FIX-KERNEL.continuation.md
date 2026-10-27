# FIX-KERNEL continuation (written by FIX-KERNEL, 2026-10-24)

State:
- KERNEL-66 (A1) LANDED f1839ed on origin/main. Report: redregg/work/codex/FIX-KERNEL.report.md.
- KERNEL-67 (doc/decision debt, text only) was in scripts/commit on hbox (wt/fixkernel, log
  .lake/fk/commit2.log, lander PID 1748188, message .lake/fk/k67.msg, launcher .lake/fk/land2.sh), queued behind
  FIX-GATES's full judge. If it did not land: `cd /tank/dregg-build/nanodregg/wt/fixkernel && bash .lake/fk/land2.sh`
  (files: Kernel/Receive/Call.lean Kernel/Sim/Gen.lean Kernel/World.lean decisions/kernel.md; the edits live in that
  worktree and in ~/dev/nanodregg-wt/fixkernel).
- Edit locally in ~/dev/nanodregg-wt/fixkernel, push with scratchpad/fixkernel/sync.sh, build with hb.sh (NOT the
  scratchpad root's sync.sh: that one is FIX-HOSTING's).

Open cards (each reasoned in decisions/kernel.md KERNEL-67 "Not done here"):
1. refusedAnswer / checkJournal: one KERNEL-44 read written twice (law 1). One function `journalRead E w txId`;
   checkJournal := journalRead … t.txId; submit's first two matches use it; ~8 proofs that `unfold submit; rw [hj, hr]`
   follow (Receive.submit_replayed, Origin, Refusals.submit_refused_final, Command.lean:678, Settle.submit_facts,
   Audit.submit_verified, Settle.admitted_facts).
2. Three duplicate detectors -> one (READ-KERNEL B5): a premise fork (firstDup's lawful Ord onto row theorems vs
   dupBy's O(n^2) at touchesMax 512). Price the premise spread (decls export) before choosing.
3. rangeUnpinned for a missing relation (B8), grantWidens for a full ledger (B10): new Refusal constructors; every
   later code moves (record-code flag day; re-genesis; codec vectors of refusal names if any).
4. A signed duplicateEffect row (lang-journey: a method returning two transfers out of its own account).
5. KERNEL-66 residual: a range listing grown past `most` is `rangeTooLong`, recorded (honest contention, wrong name).
