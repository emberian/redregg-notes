# ORDER-PRODUCT (VISIT-C, 2026-10-04 ~19:30Z; main = d27d1cad; boxes die 2026-10-05T15:55Z)
Group: NATIVE-EXERCISE-2, PORTS-A, PORTS-B, FOREMAN. JOURNEY-REDS (ad4d1f532daa84904) is running on J5 and J8; nothing here touches it.
Verdicts: READY 2 (PORTS-A, PORTS-B) · NEEDS-LANE 1 (NATIVE-EXERCISE-2) · FOREMAN: workboard triaged below (dispatch list, no lane visit).

## ⚑ JROT: the root's diagnosis is backwards
JROT is red on main because NATIVE-EXERCISE-2's D4 commit is NOT on main. D4 is the fix, not the cause. None of the lane's
7 commits has landed (checked by subject on d27d1cad). Evidence: burst-e2e /srv/journeys/d69ab3f4…/rows/journey/step-JROT/jrot/:
- trot2 rc=1 `mini: NEXT and its destination must differ from the daily key`. This client pre-check
  (native/resource-client/src/key_rotation.rs:421, from bce707b7 on 10-03) refuses before the Host sees the thief.
  Main's jrot.sh still passes the stolen daily-key file itself and expects the Host's `noPossession`.
- frot2 rc=0 `"replayed": true`, epoch stays 2. The second rotation reuses attempt id `default`, so the client replays
  the first, completed rotation. Main's jrot.sh passes no `--new-attempt`. The third FAIL (epoch 3 after restart) follows from this.
D4 (now aef58dcb) changes jrot.sh to sign with a COPY of the stolen key, to expect `unauthenticated` from the generic
Receiver, and to pass `--new-attempt possession` / `--new-attempt second`. That is all three rows.
Question for the lane, not a blocker: should a completed attempt make the next `rotate-key` a new attempt automatically?
Today a user who omits `--new-attempt` silently gets their old rotation replayed with rc=0.

## Wave 1 (now)
1. NATIVE-EXERCISE-2 (NEEDS-LANE): rebased cleanly onto d27d1cad, and Host/Main is green, but Assurance.NativeAcceptedFixture
   SIGSEGVs (139, deterministic). It goes first anyway: D4 (aef58dcb) cherry-picks cleanly onto main by itself (merge-tree
   checked), so queueing it alone closes JROT on every tip. The fixture crash is its second item.
2. PORTS-B: READY. Its first item is W08, the world-cohorts gate row (small, and it turns every world's cohort into
   a gate), then cohorts for play/ and story/. No Lean build.
3. PORTS-A: READY, the dues cohort passes 49/49 on d27d1cad. It plants mutants, commits and queues, then starts the
   sealed ballot. No Lean build.
All three are on burst-lane1. Only NATIVE-EXERCISE-2 needs a build slot. The PORTS lanes run cohorts at nice 10 against the warm base.
## Wave 2
- The FOREMAN dispatches the 8 rows below (it holds no lane, so it never blocks the wave-1 lanes).
- W12 (journey pay-enrol) waits for W02's exact price. W09/W10 (DrEX, native bounty) wait for SEATS-NATIVE to queue.

## FOREMAN: WORKBOARD-20261005 top 12, checked against d27d1cad
| row | verdict | what changed |
|---|---|---|
| W01 | OWNED, do not dispatch | J5/J8/rooms belong to JOURNEY-REDS. JROT is closed by landing NATIVE-EXERCISE-2's D4 (above), so no new work. |
| W02 | READY, but trim the row | The FRIENDS.md half has landed: deploy/shell/FRIENDS.md:510 "joining by yourself" (b0bcb7d0, 243fb343), so close cv 01a105c0-023c and drop that half. Still needed: deploy/pay/README.md:32-46 records nodeHourRate 297619 = 49.999992 DREGG/week. The fix is Kernel/PayTariff.lean `Tariff` (one of FIVE `structure Tariff` on main). It does not collide with RETENTION-PAYERS's Kernel/ObjectiveTariff. |
| W03 | NEEDS-SPEC, hold | The shim exists: `mini fleet-sign join/send/transfer/receipt/retry` (docs/FLEET-SURFACE.md:86, fleet-sign-journey.sh). What is left is the topic publish/poll mapping check, the one-page guide, and Pug's real transcript. That transcript's path is unknown and only the root or Ember has it. Ask before dispatching. |
| W04 | READY, but fix the source | The row names hbox, which is forbidden. Use persvati:~/workbox/claude-lanes/relay-hbox/w2-spk.bundle (ref lane-spk@a8830638, 4 commits 75671e8d 601ee402 87b6c9b5 a8830638, none on main; the bundle's prerequisites are in main's history, since it fetched into a main clone. Rebasing it onto `next` is NOT tried yet: that is the worker's first step). |
| W05 | PARTLY LANDED, re-spec | Already on main: chat in-process, `--operation-record` confinement and check-shell-paths.sh (336b7c0e), and `continuity-point`/`continuity-verify` (Host/Main.lean:5755-5760). Only the codecs mode is left (`minidregg-host CONFIG codecs`, serveCodecs, writeCodecsFrame; nothing on main). Re-apply only that part of /Users/ember/workbox/claude-lane-wip-20261004/claude-rewriter-20261004.{diff,bundle} (also on persvati relay-hbox/). |
| W06 | READY, but fix the source | jsplit-tenancy.sh is not in minidregg. It lives at persvati:~/workbox/claude-lanes/tenancy-b/dregg-infra (1a0c519 + d6b7d54). NO SECRETS on burst: copy only edge/mini/, after a key scan, never the repo. Run it inside an `lxc` container on burst-e2e (/usr/sbin/lxc is present, but nobody has checked that it works) so it cannot disturb the journey runner. The mini-keys-two-uid row is already armed (cv e2cb note), so acceptance becomes "red with the broker disabled". |
| W07 | READY after W06 | Same container, in sequence. Not in the first 8. |
| W08 | OWNED by PORTS-B | It is PORTS-B's first item (above). |
| W09 | BLOCKED-ON SEATS-NATIVE | "seats on main" is only the L7 kernel (6347dcb4). The native seat path (SeatReceiver, host ops 215-219, Kind.seat flag day) is SEATS-NATIVE's unlanded lane/seats-native@7382c36a, and a native run needs it. Dispatch from `next` once SEATS-NATIVE queues. |
| W10 | BLOCKED-ON SEATS-NATIVE | Same reason. |
| W11 | READY | Nothing owns it, and no object-record journey exists (journey.sh STEPS, journey-rows). Uses fetch-artifacts green, with no build. |
| W12 | STALE premise, re-spec | journey.d/jpay-e4.sh already does `join --solana` → fixture transfer → watcher → enrol → `--wait`, with attacker memos. It is in neither journey.sh STEPS nor journey-rows. Re-spec: wire it as JPAYE4 (STEPS + runner), then add renew, lapse and under-payment rows. Do it after W02. |

## FOREMAN: the first 8 to dispatch (load read 19:11Z from ~/load.log + ps)
Most of each box's load is the nice-19 byzburn (mini_private_backend), which yields to other work. Normal-priority use was gate 86%,
lane1 243% plus two Lean builds (both slots HELD), and e2e 283% of 8 vCPU (journey runner). Free memory: gate 88G, lane1 ~75G, e2e 29G.
1. W02 PAY-WEEK-EXACT → **burst-gate** (slot-1 was free; Lean PayTariff, then pay-watcher Rust via sccache). Trim the row as above.
2. W04 SPK-V4-LAND → **burst-gate** (Host/Main closure; queue behind W02 for the slot). Source: the persvati bundle.
3. W06 SPLIT-TENANCY-SCRATCH → **burst-e2e**, inside lxc, using only the copied edge/mini/ (no secrets).
4. W11 JOURNEY-OBJECT-RECORD → **burst-e2e** (artifacts green, no build; register the row in scripts/pipeline/journey-rows).
5. W23 PRE-EXISTING-REDS → **burst-lane1** (filtered cargo only, `-E 'test(NAME)'`, through the slot wrapper. Lane1 slots free up when VISIT's NE2 check ends).
6. W05' CODECS-REMAINDER (re-spec above) → **burst-lane1** (Host/Main; it rots fastest: a stopped patch against a moving Host/Main).
7. W19 C-DIFF-GENERATOR → **burst-gate**, nice 19, outside the slots (gate has the least normal load; the burn shares nice CPU with byzburn).
8. W13 DOCS-CURRENT → **burst-lane1** (no build; doc/path gates only).
Next in line: W07 (after W06), W12 (after W02), W17→W18 (gate, sequential), W20, W26. W22 overlaps JOURNEY-REDS's rooms
row: hand it to JOURNEY-REDS or wait for it. W03 waits for Pug's transcript path.
Before 15:55Z on 10-05, every dispatched worker mirrors its branch to persvati (bundle) and queues landable ranges in MERGE-QUEUE.md.
