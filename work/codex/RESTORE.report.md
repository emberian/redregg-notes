# RESTORE — work that d422453 reverted, put back on main (2026-10-27)

Landed on origin/main (emberian/nanodregg), by a direct push under rule 1:
- `62f98134` restore: Q5's traces and A1b's withdrawal, reverted by d422453
- `1a327535` decisions: GATES-30 says how the restore landed (a correction to one sentence)

Worktree: hbox `~/nd-land/restore`. Logs: hbox `~/nd-land/restore-scratch/`.

## Cause
d422453 (CLIENT-50, testground) was committed from a stale copy of the tree on top of a current
HEAD (9f10566). Its own diff carried six landings backwards. `gates/reverts.py` on d422453 counts
**218 hunks of 6 landings**. Three of those reverts had not been reported:

| landing | what d422453 reverted | state at 176110a (before) | now |
|---|---|---|---|
| 1e0849d (Q5, CLIENT-51) | 58/63 hunks: Emit/Traces*.lean, the 5 traces, client/tests/trace.rs, Loopback trace/attempt/ndRun, Rows rerunRow, Params.seedOf, sockets.rs pub, the 10 stand-ins back, generated.tsv and runs.tsv rows, the lakefile exe | all missing | restored |
| 0cf39ad (A1b, LANG-97) | 45/47 hunks: StdActivity `activityOwn`/withdraw, Surface `(withdraw)`, Bell.ob, proofs (StdActivity, Monitor, Teeth, Bell, BellRow, Spec Bell, StdOffer), journey LB10e-g, LB13f, LI9c, decision | code all missing; decision text already put back by ee2f790 (META-3) | restored |
| 262d5b4 (delete bwrap path in readset.py; loud kernel-sim forge tooth) | 16/16 | missing (**not reported before**) | restored |
| a03855e (law 1: 3 twins folded) | 4/5 | missing (**not reported before**) | restored |
| a2b8926 (docs: lines describing deleted mechanisms) | 36/37 | missing (**not reported before**) | restored; where a later landing had rewritten the same text (StdOffer/StdOfferEscrow headers by LANG-98, client/DESIGN.md retired by 9c170a8), the tip's text was kept |
| 9f10566 (join names its World) | 59/60 | already re-applied by 79b1ffe | unchanged |

Checked at 1a32753: applying any of the six commits' per-file patches again fails, so no file of them is still missing. Present: the five trace files, `emit-traces` in lakefile and 5 generated.tsv lines, withdraw in StdActivity/Bell/Bell.ob, the LB10e-g, LB13f and LI9c rows, `## LANG-97`.

## How the merges were resolved
- **Loopback: Q5 and Q6 merged into one run record.** Q6's adversary (9c8bc4c) landed after the revert, on a client without Q5, and both added `runs`/`runOf`. Now one `withRun` numbers every nd run, writes the trace lines, and records the judge's `Seen` when judging. `asRun` is deleted. Every call site uses Q5's `ndRun`. A continued frozen attempt calls `noteCall`, so the judge sees it. `setup` (from Q6) stays; `run` gained `tracing`.
- **Changes to fit the newer tip:** staleRefusing uses `retire @g` (KERNEL-70), and LB10g uses `.retire gw`. The rows list holds both certifiedPageRow and rerunRow. `[(withdraw)]` was added to the `Lang.Surface.grammar` string, which replaced the doc-comment grammar.
- **Renumbered:** Q5's decision was a second CLIENT-51, next to the testground review's CLIENT-51. It is now CLIENT-53, with a note.
- **Re-emitted:** world/resident/Bell (`ob (core …)`; this method reproduces the tip's Bell exactly, apart from a trailing newline), now 59082 bytes, id 325eee19…. The Bell's package id moves, so every World holding the Bell re-geneses. The 5 traces were re-emitted because the protocol and package wire changed under them (Req.caller, retire, certified heads, package wire 10).

## Runs (hbox, all builds under scripts/nd-build)
- Lean reach: `lake build Census Kernel Protocol Host Lang Codec Hosting Ledger Spec Web Emit Bench Ops` plus the exes: green (773 jobs). Rebuilt green after each of the two rebases (LANG-93; 48232e7, which overlapped StdOffer).
- lang-journey: GREEN; `--hole-omitted-blocker-pin-admits`: GREEN; `--harness-control`: RED (1). The LBw row passes: the shipped Bell core is the witness package.
- emit-traces: all 5 re-emit, and `--check` passes on the final tree.
- `cargo test -p nanodregg-client --test trace --test attempt --test run`: 2 + 10 + 14 pass. `every_trace_replays` passes: nd matches the traces byte for byte. `cargo check` of attach, client and launcher: ok.
- rows: ALL PASS; `--deployed` ALL PASS; `--harness-control` FAIL 51 of 54, as a control should. The rerun row's plant is caught in the normal run.
- adversary: `--seeds 200 --no-swap` ALL PASS; `--seeds 40 --no-swap --deployed` ALL PASS; control (trustCancel) FINDINGS 7.
- kernel-sim `--seeds 64`: ALL PASS (262d5b4's loud forge tooth).
- Final tree (after rebasing onto 48232e7): rows ALL PASS, journey GREEN, traces `--check` ok.

## The guard (GATES-30)
scripts/commit's replay offered no protection here. It replays the commit's own diff (parent to commit), and d422453's parent was current, so the reversal was in the diff itself and replayed without conflict. New: `gates/reverts.py REPO COMMIT`. A hunk of one of the last 100 landings counts as reverted when the commit's parent holds its after-image and the commit holds its before-image, tested one hunk at a time with `git apply --check`. scripts/commit runs it on every commit it replays and refuses one that reverts, with "REFUSED — … this commit reverts N hunks of M landings", naming each landing and file. `--reverts` allows a revert that is meant. Also fixed: the ignored old-judge flags shifted twice, so each one swallowed the next argument.
- Falsifier: on d422453 it reports 218 hunks / 6 landings. On 176110a, ee2f790, 37bfc85, b03731b and 6caf3fd it reports 0. On 79b1ffe, which re-applied the join, it reports 53 hunks of d422453.
- On the restore itself it reports 129 hunks of d422453 only. Through scripts/commit the restore would need `--reverts`.
- Limits: a plain `git push origin HEAD:main` bypasses it, as this restore did. A revert that also edits the restored lines is not counted. The window is 100 landings, not the lane's true base.

## Notes
- The commit message of 62f9813 says it "lands with `--reverts`". It was pushed directly instead, and 1a32753 corrects the GATES-30 text.
- `client/DESIGN.md` stays deleted (9c170a8 retired it after d422453 revived a2b8926's edit to it).
