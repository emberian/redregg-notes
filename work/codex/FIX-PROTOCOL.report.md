# FIX-PROTOCOL — readers A3, A7, A21 + memo weak statements (nanodregg)

Lane: FIX-PROTOCOL (Claude). Base: origin/main f9657bd. Worktree hbox:/tank/dregg-build/nanodregg/wt/fixproto
(editing copy ~/dev/nanodregg-wt/fixproto). Tags: READ (path:line), MEASURED (a command I ran), INFERRED.

## A3 — measurement FIRST (before any fix)

2026-10-24 MEASURED (compiled scratch exe over the real codecs, `Scratch/Measure.lean`, never committed;
log `measure2.log`):
- constants: `frameBytesMax` 262144 (Protocol/Table.lean:416), `Host.Page.budget` = frameBytesMax − 1024 =
  261120 (Host/Page.lean:78), `recordTurnsMax` 64 (Host/Bounds.lean:28), `eventBytesMax` 65536
  (Kernel/Bounds.lean:25), `argvBytesMax` 132096 (Protocol/Table.lean:422).
- a resume frame body is `1 + (4+|k|) + (4+|result|)`: 9 bytes of framing (measured `resumeBody 0 0 = 9`).
- a full log page at the old budget: 261,120 event bytes; the Host's reply (status ‖ logReplyLayout) is
  261,245 bytes (125 bytes of framing); room left for k in one frame: **890 bytes** (for every event size
  from 4,076 to 65,276; with 65,546-byte events only 3 fit and the room is 65,360).
- phase-2 continuation of `receipt CALL`: `|k| = 216 + 2·|call|` (call 100 → 416, 335 → 886, 336 → 888,
  540 → 1,296, 65,536 → 131,288). So **any call over 337 bytes cannot confirm against a full page.**
- deployed call sizes (rows at the deployed parameters): `write @shared 2 1 --via @g` = 540 B,
  `write @shared 3 9` = 444 B, enroll 501, grant 404–499, create 374, install of `permitAll` 697,
  install of the queue Bell = 36,550 B. Every ordinary write is over 337: the memo's ~690-byte argv /
  ~335-byte call arithmetic is right (exactly: argv 4+11+4+2·|call|, the room 890 − 197 acc − 1 phase).

2026-10-24 MEASURED — THE ROW at today's code (harness given the transport's whole-body bound, nothing
else changed; `rows fullPage` and `rows --deployed fullPage`, log `prefix-rows.log`). Row: welcome; the
sponsor installs the Bell; the newcomer writes (540 B); the operator installs 64 fillers of a 4,075-byte
call each (64 × (4+4,076) = 261,120, the old budget exactly); then `receipt CALL` of each one's last call:
- toy parameters: line 72 (the Bell install's receipt) `refused pastBound`; line 73 (the write's) ok
  (toy calls are smaller, so the page is short of the budget).
- deployed parameters: line 72 `refused pastBound`, line 73 `refused pastBound`.
So D1 is real: every confirm of an ordinary write after time away (a full page behind), and every install,
fails at the client's transport (`write_body` pastBound) at the deployed parameters.
2026-10-24 10:40Z NOTE FROM FIX-HOST (coordination, A8/A9): (1) FIX-HOST's land1 (HOST-74, `host!:`) changes Protocol/Attempt.lean: `(lookup, declined)` → `declined` (was `badReply`), restates `Protocol.Attempt.next_lookup_declined`, re-emits client/src/generated.rs; it does NOT touch Protocol/Command/Machine.lean. (2) FIX-HOST's land2 (HOST-75) adds a rows Mutation `forgesRefusal`, a Writer param `forgeRefusal`, a Loopback arm and a row `forgedRefusal` (appended to `rows`) in Protocol/Rows.lean, Rows/Writer.lean, Rows/Loopback.lean — if your lying-cancel row lands first, I rebase onto it. (3) Same class as A8, left for you since it is Machine.lean: the writer answers `refused pageIo` (Host/Loop.lean:295) and the follower reads it as "not now" by NAME (Machine.lean:900, :1360) — a status overridden by a payload string (law 7). The fix is `declined pageIo` from Host + Machine reading `(.declined, pageIoName)`; FIX-HOST will do the Host half in the same landing if you want it, ask in your report.

## A3 — the fix (PROTOCOL-70)

2026-10-24 INFERRED → decided by law 1: the page budget is a DERIVED STATIC constant, not the
continuation's actual size (that needs a per-request budget field: a second budget path the Host must
bound) and not the continuation paged out of the frame (two homes for one continuation, follow's
memory bounded by live commands). `Protocol.Bounds.pageBytesMax = frameBytesMax − 9 − 125 −
(argvBytesMax + 197) = 129,717`; `Host.Page.budget := Protocol.Bounds.pageBytesMax`. Price: a full
page holds 129,717 event bytes, not 261,120 (binds only pages of events over ~2 KB: 64 events/page).
2026-10-24 READ+fixed: follow's `Reply.bytes` now refuses a step whose fields fit but whose sum does
not (`stepTooLarge` by name); continuations deduplicated (phase 3 `[signed, ub]`, 4 `[out, cb]`, 5 `[]`,
9/10 `[]`); phase 4 settles only a verb that `submits`.
2026-10-24 MEASURED (hbox, 6G swarm-build): `Protocol.Proofs.FrameFit` green: `resume_frame_fits` (over
the real constants and every page `Host.Page.build` returns, via `Host.Page.build_within`),
`perField_budget_overflows` (the tooth in the constants), `frame_split`.
2026-10-24 MEASURED: row `fullPage` after the fix: `rows fullPage cancelLie` ALL PASS, `rows --deployed
fullPage cancelLie` ALL PASS; plant `perFieldBudget` (the per-field budget restored) caught at line 72,
`refused pastBound`, both parameter sets.
2026-10-24 READ+fixed (memo B1/B2): `Rows.Params.pageBudget` deleted, the writer pages at HOST's own
budget under both parameter sets; `toy_budget_serves`/`deployed_budget_serves` deleted.
2026-10-24 INFERRED residual, filed cv 01a16d81-d644: a `sign` step is `argvSize + 2|ub| + 163`, a
`submit` step `argvSize + 2|call| + |out| + 23`; past the frame only for an argv ≳ 2× its call. Now refused
`stepTooLarge` by name, never written.

## A7 — cancel settles on follow (PROTOCOL-71)

2026-10-24 READ+fixed: phase 10's `refused cancelled` / `ok` start a second catch-up (`cancelCatchUp`,
`tried` bits 4/8); its tip (`cancelTip` → `cancelSettled`) ends `ok` only when follow's World settles the
call `refused cancelled`, else `hostContradicted CLAIM FOLLOWSAID`.
2026-10-24 MEASURED: `cancel_ok_settled` green (whole step machine, any continuation, any result).
Row `cancelLie`: line 7 `hostContradicted cancelled open`; plant `trustCancel` caught at line 7 (`ok`);
PASS toy and deployed. `cancel`, `cancelForged` PASS both.

## A21 — atGenesis (PROTOCOL-67 amended)

2026-10-24 READ: `carryWorld` sets `steps := c.height` (Kernel/Receive/Follow.lean:180). MEASURED green:
`carryWorld_atGenesis`, `carry_genesis_atGenesis` (Protocol/Proofs/FollowHead.lean). Docstrings of
`atGenesis`, `genesisLeaf` and the FollowHead header restated; PROTOCOL-67 amendment paragraph.

## Weak statements (PROTOCOL-72)

2026-10-24 MEASURED: `settle`'s plant now caught at line 6 (the lying lookup), `hostContradicted refused
open` (trustLookup trusts only the Host's refusal); `staleRange`'s plant is one change (a relay hides the
log, follow's own admission kept), caught at line 10 `declined stale`; settle/refused docstrings;
`stepsPerCommandMax` doc names the client.

## Validation

2026-10-24 MEASURED (before the rebase onto f1839ed): `rows` (toy) 47/47 ALL PASS; `rows --deployed` all
rows PASS but `fullPage`'s ops declaration (fixed, re-run PASS); after the cancelTip/settleStep refactor:
toy 47/47 ALL PASS, deployed subset (cancel cancelForged cancelLie fullPage settle rangeInvoke rangeFlag
receipt bigEvent paging rotate refused) ALL PASS. `gates/check.py`: all ok but SIZE.md (scripts/commit
writes it). A first version fed two whole-machine proofs `maxHeartbeats`; the refusals gate refused it;
fixed by naming `cancelTip`/`settleStep` (no override in the landing).
2026-10-24 MEASURED: rebased onto origin/main f1839ed cleanly; `lake build Protocol Host.Proofs.Page
Hosting.Proofs.Socket rows` green (339 jobs). Landing: scripts/commit (protocol!, full judge) running.

## Landing

2026-10-24 MEASURED: a full judge (`protocol!`) of the candidate on f1839ed: gates, build, census and
decls ok (8 map lines); red ONLY at rows/lang-journey (LB8b, LH7b "rejected stale") and THE BAR's
harness control (`friend1 nd write: refused stale`). lang-journey reds identically at clean origin/main
7655145 (hbox wt/fixproto-main, removed after): KERNEL-66 (f1839ed, pins before receivers), not this
change. ASK for ROOT/KERNEL: lang-journey LB8b/LH7b red on main since KERNEL-66.
CORRECTION (2026-10-24): my line "THE BAR's control reads refused stale, the same class" was INFERRED and is
WRONG: FIX-KERNEL could not reproduce it (THE BAR passes with its journey fix; bar.sh's word is `declined
stale`, unchanged). What the judge printed was the harness control's own red, not a main defect I measured.
2026-10-24 Relabelled `protocol:` (no persisted shape, no re-genesis; breaks stated in the body) and
landed through the fast judge per R-0069: PRE-PUSH FAST GREEN, compare-and-swap after two main moves.
**LANDED 0a299c8**, pushed to origin.
2026-10-24 Ember's correction (plants are vacuity checks run when cheap, not landing gates) noted; the
plants here were cheap and ran (all caught at their lines); nothing gated on them beyond that.
Open: cv 01a16d81-d644 (sign/submit step replies bounded as a whole). Cross-layer lines were written
"ROOT for HOST" / "ROOT for HOSTING" though FIX-HOST and FIX-HOSTING lanes are live: HOST's part is
the budget the brief ordered; HOSTING's is three tactic lines in step_cont, its statement unchanged.

## PROTOCOL-73 — staleBehind in the Host's order (card from FIX-KERNEL)

2026-10-24 READ: `Command.staleBehind` decided by `receive` then admission's `stale`; KERNEL-66's
`submit` checks `signedBy` then `checkPins` before any receiver.
2026-10-24 MEASURED before the fix: row `staleRefusing` (write through grant g raced by `revoke @g`):
line 7 (next run) `declined stale`, never settled (settlement open → resent → declined), toy and deployed
(logs stale-before.log).
2026-10-24 Fix: `staleBehind` = own call ∧ `signedBy … = ok` ∧ `checkPins` refuses (one definition with
the Host). `staleBehind_spec` RESTATES-MEANING; new `staleBehind_declined`, `checkPins_error_disagree`;
`staleBehind_final` statement unchanged, proof over the call's pins. MEASURED after: line 7 `refused
stale`, PASS toy and deployed; `refused`, `settle` PASS; toy set 47/48 (lang-journey = main's KERNEL-66
red, FIX-KERNEL's fix queued). No cheap plant: new `Plant.measured` records the before-fix measurement.
2026-10-24 **LANDED d0e3a03** (fast judge green, after three main moves), pushed. The 0a299c8 message's
BAR inference is corrected in d0e3a03's message and above.
