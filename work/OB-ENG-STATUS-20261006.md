# DEPUTY-OB-ENG status (burst 2, 2026-10-06)
Base main 4ef4e808. Workers author locally under scratchpad/obeng/<item> until BURST2-BRIEF-20261006.txt exists, then burst2-b.
Worker addendum: work/OB-ENG-WORKERS-20261006.txt.
| item | worker | model | state |
|---|---|---|---|
| seat retention + shared capacity parser (charter 2) | SEAT-RETENTION a4946efee0e1523f1 | sonnet | authoring |
| OB8 send/deliverMessage retention + inbox-writers theorem (charter 1, cv 01a10ae9-7a37/-7a53) | OB8-RETENTION ae0e3f7cedceb378f | sonnet | authoring |
| upgrade turns kernel half (charter 3, UPGRADE-BRIEF) | UPGRADE-TURNS a7d923814174b8ff0 | opus | authoring |
| kernel pin clause installed at create (charter 4a) | OBJECT-PIN a4227a31886f0ef66 | sonnet | authoring |
HELD FOR GROUNDING (design notes sent to DEPUTY-GROUNDING ad98f15ef23727e3a, 10-06): sends from a delivered message (01a10ae9-79e1),
activity awaits message (01a10ae9-7a1a), pipelining depth>1 (01a10ae9-79fd), Core4 digest primitive (new cv task). Reason: each changes
OB meaning (typing/semantics/cost of a Core4 program), which Ember froze until the GPT-6 round.

## Log
- 10-06 ~21:00 EDT: 4 workers launched (authoring). Grounding notes sent; grounding filed them (05 §4/Q5-5, 01 §4/Q1-5, 06 Q6-5).
- Ruled DEPUTY-PRODUCT's seat view request: `exit` + `opened` approved (its worker a3dae821b8bf91846, I review the SeatStore hunk);
  `invoker`/`offerer`/`payee`/`holder` HELD for grounding (identity disclosure to contract code = info-flow choice; Zoe withholds it;
  the seat is the claimant's handle, payout to payee is the kernel's job).
- kn2-forcing (DEPUTY-KERNEL, a51f9e4f86efea00c): runSegment relative heap limit + delivery envelope check, root-ruled; I review before queue;
  UPGRADE-TURNS rebases onto it.
- cv 01a113e7-92cb (empty want donates silently) -> SEAT-RETENTION's second item: explicit donation marker + named refusal, both-way rows.
- BURST2-BRIEF up (~00:50Z 10-07); workers told: burst2-b ember@67.213.117.179.
- RULED writeState DELETED; create takes an optional initial state seed judged by the creator's law (old=none, turn 4) + typedAt (OBJECT-PIN).
  Reason: a holder's direct write is the method bypass LAWS D-1 closes; under the derived pin clause it could only refuse.
- UPGRADE-TURNS: OBJECT-RECORD v2 compiles (62487128, burst2-b /srv/lanes/upgrade-turns); turn codes 6-9 (5 taken by call frames); identity-only
  births/calls while draining (stricter than ruling); messages to a draining object wait; single-turn MIGRATE (migrating phase not built: next item).
- REVIEWED DEPUTY-PRODUCT 093f836e (seat view exit+opened): approved, required seat cell frame bump v1->v2.
- KERNEL BUG (found by PRODUCT's bounty): Seat.exitAuthorized lets a holder activity's end exit an afterDeadline seat early -> SEAT-RETENTION item 3
  (holder_respects_deadline). `held` view flag rejected (fix the kernel, not the view).
- DEPUTY-KERNEL KN2-STORE-OPEN: its lanes port my files' history reads; I review hunks. My lanes add no new full-history reads.
- ROOT 10-07: no NEW workers; running ones finish. Poll every 15-20 min.
- QUEUED ob8-retention 4ef4e808..acb915d0 (proofs, compiled, planted faults). Its 4 retention gaps filed as engineering cv tasks
  01a113fe-1351 (inbox deposit), -1390 (empty inbox retire), -13ca (decided delivery slot retire), -140a (deliverMessage slot.activity check).
  Reason they are engineering not grounding: they mirror the activity storage-deposit/retire precedent; no OB program's meaning changes.
- QUEUED object-pin 4ef4e808..11f02b78 (compiled, planted faults; journeys authored not executed). Workers OB8-RETENTION, OBJECT-PIN finished.
- Running: SEAT-RETENTION (retention -> holder_respects_deadline -> donation marker), UPGRADE-TURNS (rebasing onto object-pin, COMMAND v6).
- QUEUED seat-retention 4ef4e808..f2b243cb. Approved kn2-forcing 61778bc7. PRODUCT P1 rebases onto seat-retention (frame v4).
- UPGRADE-TURNS range 4ef4e808..7e4488ee (on object-pin + ob8): HELD by me: migrate_cannot_fail had MIGRATE's own judgment as premise
  (forbidden weakening under the promised name) -> renaming + real induction + live_counts over Reachable in progress.
  Filed cv 01a1141b-d4b5 (multi-turn migrating), -d4d6 (facet table / interface compat), -d4f6 (executed Tally row).
