# FIX-HOST continuation — card A9-remainder (HOST-78), granted by the coordinator 2026-10-24
Written by FIX-HOST at park (context ceiling ~400K). Successor: read this whole, then FIX-HOST.report.md's last 15 lines.

## The grant (coordinator's message, verbatim intent)
Do the A9 remainder yourself: delete `Kernel.Receive.audit` and its helpers, restate the consumers over
`World.fold ∧ Honest` (law 1: one re-deriver, the one the follower runs), keep every consumer's statement as
strong (RESTATES lines; name any that genuinely weaken and why), say in HOST-78 what `audit_ok` becomes
(if a restatement of absorb's soundness, delete or fold it). Subject `kernel:`; `CROSS-LAYER: KERNEL` line
naming the coordinator's grant. Land when green. FIX-KERNEL has parked: Kernel/Receive/Audit.lean and its
consumers are yours for this card. Rebase first (main at bace75a+).

## State at park (MEASURED)
- origin/main bace75a = my last landing. wt/fixhost is clean at bace75a. Own CARGO_TARGET_DIR=$PWD/target.
- Landed: 33dd692 (HOST-74), f3a00e2 (HOST-75), bace75a (HOST-76/77).
- Already on main (Host/Proofs/Refine.lean): absorbStep_turnEvent/refusalEvent/honest/sound, absorb_honest,
  absorb_sound, absorb_iff (RowsCanon for ←), honest_page_absorbed, host_run_absorbed, Deployed.host_run_kept,
  Deployed.follow_absorbed_audits (this last one CONCLUDES `audit … = .ok`: restate it to `fold ∧ Honest`
  when audit goes).

## Files naming audit/rederive/auditStep/auditTurn/auditRefusal/staleRecorded/undecodableEvent/forgedName/audit_ok (git grep on bace75a)
Kernel: Receive/Audit.lean (defs), Receive/Call.lean, Receive/Submit.lean, Turn.lean, World.lean, Sim.lean, Sim/Gen.lean,
  Proofs/{Audit,CarryRooted,Journal,LedgerNext,Logic/History,ObjectHead,Rooted,RootedDeployed,WriteNext}.lean
Ledger: Proofs/{GrantCap,GrantCapTooth}.lean, Sim/Journey.lean
Host: Base.lean, Follow.lean (docs), Proofs/Refine.lean, Proofs/SpentCheckpoint.lean
Protocol: Command/Machine.lean (docs + forgedName?), Proofs/Command.lean, Rows.lean, Table.lean
Bench: Count.lean, WorstCut.lean (runtime auditRecord). Census: Journal.lean, JournalRun.lean. Hosting/Sim/Journey.lean, Lang/Journey.lean.
(Many are prose mentions; check each hit.)

## Design notes (INFERRED, decide and say so in HOST-78)
1. `recordedBy` (Receive/Audit.lean) is NOT a re-deriver: it is the judge/cancel dispatch `Honest` uses. Keep it
   (move it to Receive/Submit.lean beside judge/cancel) and delete the rest of the file.
2. Proof consumers: almost all go through `audit_ok : audit X w l = .ok w' ↔ fold ∧ Honest`. Restate each
   `(h : audit X w l = .ok w')` premise as `(hf : World.fold X.env w l = .ok w') (hh : Honest X w l)` — the SAME
   strength (audit_ok is an iff), so `RESTATES-MEANING` per theorem with "no hypothesis gained, premise split by
   audit_ok". `audit_ok` itself then has no subject: delete it (DELETES line). Its content survives as
   Host's `absorb_iff` (the follower that runs).
3. RUNTIME auditors (Kernel/Sim/Gen, Bench/Count, Bench/WorstCut `auditRecord`) need an executable re-deriver
   at the Kernel layer and cannot import Protocol. Law-1 option to price: move the event-level core of
   `absorbStep` (given a decoded event: turn call | refusal call | cancel sig call → submit / judge-records /
   cancel-records) into Kernel/Receive as THE re-deriver, make Protocol's absorbStep = parse tag bytes + that core,
   and have kernel-sim/bench run the core on each Step's event and compare the result to the logged step. That
   moves Machine.lean (PROTOCOL; FIX-PROTOCOL's — coordinate in its report) and makes Host's absorbStep_* proofs
   unfold one more definition. The alternative (kernel-sim checks via fold only) weakens the sim — name it if taken.
4. `staleRecorded` / `undecodableEvent` / `forgedName`: constructed only by audit (check `cancelForged`'s use in
   absorbStep: it is a Refusal constructor, keep). Delete the unused refusal names (wire/name tables? grep
   Codec/Emit for `refusalNames` order: deleting a constructor shifts codes — that is a flag day: `kernel!:`,
   full judge, say what re-emits).
5. Ledger GrantCap/GrantCapTooth and Kernel Logic/History are the heaviest proof users; read them before choosing (2).

## Box safety (verbatim from the brief)
Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you
started is stopped by the PID in its PID file, and only that; no PID file, no kill. Never `git stash`. Never run an
unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch.
Launch landers with a script file (not an `&&` chain: `$L` set inside a backgrounded chain leaves the PID file
unwritten — that bit me twice): see hbox logs/fixhost-launch3.sh for the working pattern.
