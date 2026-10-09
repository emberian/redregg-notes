# DEPUTY-PRODUCT resume (burst 2) — STOPPED 2026-10-07 ~04:15Z, all workers done
Board + log: work/PRODUCT-BURST2-20261006.md. Root ruling: no new workers; swarm drifting down.

## Queued (MERGE-QUEUE.md REQUESTS), each reviewed by me (statements read, planted fault red, README says what is not native)
- P2-SHEETLAW 4ef4e808..90cc6020 — SheetLaw bal/eq_raise_needs_clock, alive constant over clockless histories (cv 01a0f64e-c650).
- P5-RUN-EDITS 84a6dac8..b21d5aaf — kernel insertRun refining StableRanges; content frame v10; fixture/surfaces/snapshot re-emitted (cv 01a0f611-ea6c).
- P3-FLEET-MIGRATION 4ef4e808..917582e5 (from hbox bundle; squash wip 500d2f33) — fleet-sign fixes for helm, docs/FLEET-MIGRATION.md, FRIENDS FIDO note.
- P1-SEATSTORE f2b243cb..1b8b2807 (after OB-ENG's SEAT-RETENTION f2b243cb) — seat view exit+opened, frame v4; OB-ENG approved; keeper owes pin regen.
- P1-BOUNTY-NATIVE 1b8b2807..796da939 (hbox bundle) — bounty native on seats, 190/190.

## Decisions (with reasons)
- QUOTE-DISCLOSE: ROOT ruled reference-only this burst (Ember's recorded choice); --disclose design recorded in cv 01a0f53e-f651.
- Seat view: OB-ENG approved exit+opened only; invoker/offerer/payee/holder HELD for the GPT-6 packet (information flow, Zoe hides it).
  The `held` flag was dropped: OB-ENG ruled "an activity end exits a held seat whatever its exit rule" a KERNEL BUG, fixed in SEAT-RETENTION.
- Bounty escrow wants a work-receipt asset rather than being a donation, so offer safety (not contract code) protects the poster.
- READ-TARGET-LEG (cv 01a0f611-ea93) drops the source-law run from read targets = weakens a check (pause list #2): root decides; not started.

## Left (cv tasks)
- 01a11476-1c59 helm double-commits on Mini (no receipt_hash -> retry commits twice): fix on OUR side.
- SEATS opened=height tie question (new cv task); bounty journey row unrun.
- 01a11409-6ddb run split/join/move; 01a11409-6df6 mini-sdk explain fixtures still schemaVersion 9.
- MUD-AREA port plan on cv 01a0f52e-76f2 (4 pieces, 2-3 days); MUD 8-16 after it.
- Bread SOON still blocked: cards (L12), governed namespaces (UPGRADE), Hermes on node (Ember's providers). Native play/dues next after bounty (same seat pattern).
- Lanes on burst2-b keep src+logs only (P5 lane still 7.8G, P3 src 11G — unexplained, not mine to delete beyond lanes).

## Queue protocol changed (MERGE-KEEPER, 10-07)
Queue = one file per range at work/queue/<lane>.txt (see queue/README.txt), then message the keeper "queued <lane>";
MERGE-QUEUE.md is the keeper's LOG only. main = green = c1df1f08; next = 41ca9444 (P5 + P3 in b5). Build new lanes on `next`.
The keeper took all 5 of my ranges onto next; a conflicting one comes back to DEPUTY-PRODUCT (resume P1's worker a3dae821b8bf91846 for seat/bounty conflicts).
