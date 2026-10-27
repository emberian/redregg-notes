# FIX-KERNEL — report (A1, then the kernel memo's pure-deletion/doc DEBT)

Tags: READ (path:line), MEASURED (a command I ran; log path), INFERRED (my reasoning).
Worktrees: hbox /tank/dregg-build/nanodregg/wt/fixkernel (build), local ~/dev/nanodregg-wt/fixkernel (edit, rsync'd).
Logs: hbox wt/fixkernel/.lake/fk/.

2026-10-24 (1)     READ COLLATION-20261024 §A1 and READ-KERNEL.md whole. Base f9657bd.
2026-10-24 (2)     MEASURED first design (pins before the signature) green on all 755 jobs; REJECTED on review: a pin
                   comparison answered before the signature is an oracle on cells for a party holding no key
                   (reads need member+key+signature+follow grant: READ Protocol/Envelope.lean Envelope.check).
2026-10-24 (3)     Second design: journal -> refusedFinal -> signedBy (World, signature, key) -> checkPins -> deriveTurn ->
                   World.admit. Rebased onto origin/main 7332f9c; MEASURED full `lake build` 756 jobs green.
2026-10-24 (4)     MEASURED kernel-sim --seeds 64: ALL PASS (.lake/fk/sim5.out). Plant (submit without checkPins):
                   `probe race: the loser was refused lawDenied, not rejected stale` 64/64 seeds, `FAIL planted
                   refusals never met: [race-loser:stale, race-loser-declined:declined]` (.lake/fk/plant2-sim.out);
                   restored. (The first design's plant read the same red: .lake/fk/plant-sim.out.)
2026-10-24 10:47Z  LANDED f1839ed (KERNEL-66), pushed to origin. Fast judge: build ok (every target), decls ok —
                   330 modules exported, 14192 parent declarations in the reach, 0 map lines, 0 changes of meaning
                   (the price: no landed statement restated). WASTE re-pin admit trie-hashes-per-turn 14.087 -> 14.092
                   (MEASURED 65370/4639; the 65347 baseline is READ from the row's own source text).

## KERNEL-66 (A1) — what landed (f1839ed)
- READ the defect as stated: Submit.lean:32-44 (submit: journal -> refusedAnswer -> receive -> admit), Call.lean:422
  (`pinned` returns `w.live`, whatever the pin says). Confirmed by the plant below (MEASURED): under the old order the
  race's loser is `refused lawDenied` (recorded).
- New order: journal -> refusedFinal -> signedBy (World, signature, key) -> checkPins -> deriveTurn -> World.admit.
  `checkPins` (Kernel/World.lean) = the three disagreements `admit_stale_pin` names. `submit` calls the two halves of
  `receive` (`receive_signed` proves receive = signedBy >>= deriveTurn); `authenticatedBy` = `signedBy` passing.
- Why after the signature (design fork I decided, critique in KERNEL-66): pins-before-signature would make `stale` vs
  `badSignature` an oracle on cells for a party with no key (READ Protocol/Envelope.lean: reads need member, key,
  signature, follow grant). A member already had the oracle through admission; nothing it learns moved.
- Theorems (Kernel/Proofs/Audit.lean): stale_declined_before_receive (over submit AND judge: declined stale; no premise
  names receive), receive_not_run_on_stale (same stale verdict under ANY Program: no tick, no law),
  checkPins_error_never_admitted (the reorder renames, never changes what lands); StaleOnly.lean checkPins_ok_iff,
  checkPins_error_stale; Receive.lean receive_signed, keyRule_deriveTurn, sealTurn_rows, rowTouchesOf_pins.
- KERNEL-54's judge_stale_declined / judge_recorded_not_stale: statements and proofs unchanged (MEASURED: decls 0 map
  lines). RESTATES needed: none. submit_ok / submit_verified / verified_eq_false_iff / authenticatedBy_verified /
  admitted_facts (Settle) / admitted_elsewhere_refused (Origin): proofs re-run, statements unchanged.
- Row: kernel-sim probeRace (arms race-loser:stale, race-loser-declined:declined, race-law:lawDenied) on branch Worlds;
  random arm 7 no longer skips lawed objects (it skipped them BECAUSE of this defect: READ Gen.lean arm 7 before).
- Re-emits: nothing (no wire/cell/record/code change). INFERRED: a log recorded under the old order would no longer audit.
- Residual named in KERNEL-66: a listing grown past `most` is still `rangeTooLong`, recorded.

## Hazard met (for ROOT)
- The session scratchpad is SHARED by the FIX lanes: FIX-HOSTING's `scratchpad/sync.sh` overwrote mine, and two of my
  syncs ran its script (it synced its own worktree; no harm found in mine: hbox `git status` showed only my files).
  Mine now live under scratchpad/fixkernel/. I deleted `scratchpad/hb.sh`, a file I had created there seconds before.

## KERNEL-67 (doc debt, text only) — IN THE LANDING QUEUE at park time
- First attempt judged FAST GREEN (build ok, decls 0 map lines) on f1839ed; main moved to 37772b9 and the lander is
  re-basing, waiting for a judge slot behind FIX-GATES's full judge (hbox lander PID 1748188, log
  wt/fixkernel/.lake/fk/commit2.log). Relaunch if it gave up: `bash .lake/fk/land2.sh` in that worktree.
- Coordinator's 10-24 correction received: plants are a cheap vacuity check, not a landing gate. Nothing here was
  shaped by one; the KERNEL-66 plant was run because it was cheap (one sim build).
- Parked with redregg/work/codex/FIX-KERNEL.continuation.md (open cards 1–5).

## 2026-10-24 — main RED at lang-journey since KERNEL-66 (coordinator's ask)
- KERNEL-67 LANDED 7c85768 (its own push was rejected non-fast-forward; it reached origin through d741f5a's merge).
- MEASURED at 0a299c8 (hbox wt/fixkernel .lake/fk/lj.out): lang-journey RED (3): LB8b x2, LH7b, each `rejected stale`
  where the row expected the guard's `rung: answered` / the method's `support0 moved` (the old order). Not a wrong
  name: each call's pin moved; `stale` is the name KERNEL-66 means. P8.2 accepted either and now emits `rejected stale`.
- Rows updated (expect exactly `rejected stale`; P8.2 tightened to it); MEASURED lang-journey GREEN both modes
  (lj2.out, lj3.out). THE BAR `--records 60 --standing`: PASS (bar.out); `--harness-control`: RED harness-control
  with every comparator fired (barhc.out). No `refused stale`: FIX-PROTOCOL's BAR line (INFERRED) does not reproduce;
  bar.sh's word is `declined stale`, unchanged.
- Found (READ Protocol/Command/Machine.lean `staleBehind`): the client's BEHIND classifier still uses the OLD order
  (`receive` then admit's `stale`): a moved-pin call whose receiver also refuses on the new state reads false and its
  settlement stays `open`. Fix = `checkPins` on follow's World; staleBehind_spec / Behind.lean restate. PROTOCOL's
  file: CARD for FIX-PROTOCOL (named in the KERNEL-66 amendment).
- Landing `lang:` (Lang/Journey.lean + the KERNEL-66 amendment in decisions/kernel.md): scripts/commit running on hbox
  (PID file .lake/fk/commit3.pid, log .lake/fk/commit3.log, launcher .lake/fk/land3.sh), queued (log empty after 30
  min: waiting on the landing queue). Relaunch with `bash .lake/fk/land3.sh` if it ends REFUSED for a main move.
