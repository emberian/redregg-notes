# DEPUTY-PRODUCT — burst 2 board (2026-10-06). Owner: DEPUTY-PRODUCT. Workers report to DEPUTY-PRODUCT, not the root.
Charter: DEPUTIES-20261006.md (DEPUTY-PRODUCT). Box: burst2-b (BURST2-BRIEF-20261006.txt, once written). Read clone of main
4ef4e808 at the deputy's scratchpad (blobless). Owned: world/*, deos/docuverse, Bread ports, MUD, apps.

## Survey of the charter items at main 4ef4e808 (READ at source by the deputy)
- Bread NOW items N1-N5, N7: LANDED (bounty 35c8ccb5, dues+ballot 4bbccee5, play 1305ae98, story, world-cohorts gate). N6: `mini fleet-sign`
  drop-in LANDED (docs/FLEET-SURFACE.md "mini fleet-sign"); missing = migration guide + Pug-harness replay.
- SOON whose prerequisite landed: SEATS-NATIVE (2c1b5733 signed seat command, 6336af2b `mini seat` + Broker + 9-row acceptance,
  9e01c69e activity end closes held seats) and the native activity route (34d803f8) => W10 BOUNTY-NATIVE is UNBLOCKED; play/dues native next.
  DrEX as seats LANDED (e57105c5, preview + kernel; native leg = W09b). Cards need L12 (not on main). Governed namespaces need UPGRADE
  (DEPUTY-OB-ENG item 3). Hermes on the node needs Ember's providers. => not placed.
- JOIN-SOLANA (01a0f52e-76fd): client + FRIENDS.md "joining by yourself" LANDED (243fb343, 408acb23). Residue: FRIENDS.md does not say
  FIDO ssh keys are refused (client does: join_solana.rs fidoKeyRefused), and the "bare ssh user" proxy hint is absent. Folded into P3.
- QUOTE-DISCLOSE: ROOT ruled 10-06 reference-only this burst; proposal written into cv 01a0f53e-f651. Not built.
- MUD 7-16: only laws + templates on main (S8 note); items 8-16 are large; after P2's veteran.

## Items
| id | goal | worker | state |
|---|---|---|---|
| P1-BOUNTY-NATIVE | world/bounty native: escrow = a seat per bounty (give reward; want approved work or the reward back; exit at deadline), poster decision = activity answer slot, payout = seat reallocation; acceptance script on a scratch world modelled on objective-seat-native-acceptance.py | sonnet a3dae821b8bf91846 | spawned |
| P2-SHEETLAW | cv 01a0f64e-c650: bal_raise_needs_clock, eq_raise_needs_clock, alive-constant-over-clockless-history (death_needs_clock + dead_stays_dead_without_clock) in Assurance/SheetLaw.lean | sonnet acd5de24c5424a78d | spawned |
| P3-FLEET-MIGRATION | W03 finish: docs/FLEET-MIGRATION.md (one page), replay of Pug's harness calls through `mini fleet-sign` on a scratch world, unmapped verb refused loudly; FRIENDS.md FIDO + bare-ssh residue of JOIN-SOLANA | sonnet a43c146e1fb0a4c29 | spawned |
| P4-PLAY-NATIVE | world/play CommitReveal stakes in seats, forfeit by deadline exit; after P1 by P1's veteran | P1 veteran | waits P1 |
| P5-RUN-EDITS | cv 01a0f611-ea6c (K-RUNS-RANGES): kernel run edits so appended lines are range-transcludable, refining Theory/StableRanges | sonnet a86fda9422372d2cb | spawned |
| (held) READ-TARGET-LEG | cv 01a0f611-ea93: dropping the source-law run from read targets WEAKENS a check (pause list #2) -> root decides first | - | root |

## Log
- 10-06: board written; QUOTE-DISCLOSE asked + ruled; P1-P3 spawned (authoring until burst2-b exists).
- 10-06 01:05Z: P1 stopped on a kernel gap (SeatStore call view lacks invoker/offerer/payee/exit/holder/opened; verified at SeatStore.lean:255-267). Decision: full design, no weaker subset. Asked root to relay to DEPUTY-OB-ENG (owner of Seat*); P1 authors the SeatStore change as a separate commit for OB-ENG review.
- 01:12Z BURST2-BRIEF up. OB-ENG (a667f3ddb2cf279db) ruled: approve per-seat `exit` + `opened`; HOLD invoker/offerer/payee/holder for GPT-6 packet. P1 re-scoped. P2/P3 into phase 2 on burst2-b. P5 spawned (4th slot).
- 01:25Z P2 compiled 4ef4e808..6fe56b1c (lane-check 0, fault28 red; reviewed: statements + poles OK). Sent back for rebase + reword, then MUD-AREA (item 7) port plan. P1 SeatStore 093f836e (exit, opened=height) -> OB-ENG review; P1 asks per-seat `held` (activity end overrides seat exit) -> forwarded.
- 01:40Z ROOT: finish in-flight only, no new items. P2 QUEUED 90cc6020; MUD-AREA plan filed on cv 01a0f52e-76f2, not started. In flight: P1, P3, P5.
- 01:50Z OB-ENG approved 093f836e w/ seat frame v1->v2 bump; `held` dropped: OB-ENG ruled activity-end-overrides-exit a KERNEL BUG, fixed by SEAT-RETENTION (holder_respects_deadline). P1 relayed.
- 02:00Z P5 4ef4e808..7dcdf64a reviewed (statements OK, fault red) but NOT queued: umbrella red on NativeAcceptedFixture, surfaces drift, K12N unrun -> sent back to fix in lane. Follow-ups cv 01a11409-6ddb (split/join/move), 01a11409-6df6.
- 02:05Z SEAT-RETENTION queued 4ef4e808..f2b243cb (frame v3, holder_respects_deadline c4be7c92). P1 told to rebase onto it, take frame v4.
- 02:15Z P1 rebased: SeatStore 1b8b2807 (v4) -> OB-ENG review; steered escrow away from donation (no kernel guarantee) toward wanting a work-receipt asset.
