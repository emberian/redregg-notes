# FLEET-RACE log (Claude, 2026-10-14) — cv task 01a13985-48ef
Lane tree: hbox:/tank/dregg-build/claude-lanes/fleet-race/src (git clone of lane/perf-fix 3f873592 from bundles/burst3-minidregg.git).

## Step 1 — diagnosis (read at source, lane tree 3f873592)
- Refusal site: Kernel/NativeClientConsent.lean:44-55 `checkObservation`. Accepts iff
  `challengeCodec.encode (NativeObservationController.challenge (observationContext config basis.opened) profile federation genesisHeight wanted intentSignature) = candidate`.
  The WHOLE challenge (Compiler/NativeObservationCodec.lean:68-90): intent, domain, semantics, federation, worldRoot, authorityRoot,
  height, clockNow, clockSlot, headers, intentSignature.
- Host side is the SAME function: Kernel/NativeHost.lean:554-575 `challengeAnswer`/`challengeLoaded` call
  `NativeObservationController.challenge (observationContext config opened) ...`; Host/Main.lean:2052-2057 op 4 uses
  `sessionOpened config state` (the serving Host's current image). challengeAt (Kernel/NativeObservationController.lean:523-533)
  takes worldRoot, authority root, `genesisHeight + context.height`, clock and headers (headerAt over worldRoot) from the context.
  So with the same pinned config, the ONLY input that can differ between Host and client is `opened` = the source state.
- Client basis: Host/ClientConsentCore.lean:504-555 `serve`: every non-thin frame first runs `verifyInitial` once, then `refresh`
  (:281, admits only the Store's appended suffix and moves to the Store's HEAD). Frame 221 (observation) is answered at the head
  admitted AT THAT FRAME, which is after the Host built its challenge (op 4).
- Rust flow: workspace::signed_view -> query_retained (native/resource-client/src/main.rs:2132, `replan::replan(.., replan::stale_root, ..)`)
  -> query_once -> authorize_observation (main.rs:1754-1800): author intent, consent 220, sign intent, host op `challenge`,
  `client_consent::observation` (frame 221) -> on frame 255 `round_trip` returns
  `local consent refused before signing: <detail>` (src/client_consent.rs:73). replan::stale_root (src/replan.rs:207) only retries the HOST's
  decoded `stale-root`; a local consent refusal is no Host decision, so it is terminal; fleet::attempt (src/fleet.rs:507-519)
  likewise only supersedes on observation_stale() (a Host decision). => terminal refusal, no replan. CONFIRMED.
- Timeline, run1 charlie-7: remote challenge height 36, challenge.bin 04:20:59.038; bravo's turn (height 37) submit.json written
  04:20:59.874; charlie's refusal stderr 04:20:59.484. Same shape for charlie-12 (h49) and charlie-21 (h77). Consistent with an interleaved
  commit landing between the Host's op 4 and the provider's frame-221 refresh (provider basis NEWER than the challenge). Not byte-proven:
  the refusal did not keep the locally derived challenge. The fix names both heights in the refusal, which makes it exact from now on.
- Semantics: docs/CLIENT-SIGNING-CONSENT.md:3-6 "custody derives the COMPLETE expected bytes from its retained request, its own
  configuration and an independently admitted source prefix"; :12-15 the core "checks exact extensions before each signing phase, and
  terminates on a rollback, prefix rewrite or invalid extension" (a valid newer extension is not terminal); src/replan.rs:4-9
  "A signed observation binds the world root, authority root and height ... any commit stales a signed read. The client re-plans."
  => The doc decides it: the signer consents to the intent AT an observation of its admitted source. A challenge at another height is
  a liveness event (re-observe on the new basis and re-consent), not a security refusal. The check stays exactly as strict.

## Plan (step 2)
- Lean: checkObservation's error becomes a typed ObservationRefusal {localPreparation | staleObservation remote local | differs};
  accept condition unchanged. stale only when the decoded candidate has intent = wanted, intentSignature = the retained one,
  same domain/semantics/federation, and a DIFFERENT height. Theorem: a stale label implies same intent+signature; acceptance unchanged.
- Rust: client_consent records the provider's named stale refusal (flag, set only from a provider frame); replan::stale_root also
  re-observes on it; bounded by --replan-max (5). Intent mismatch stays terminal, named "remote challenge differs from locally prepared intent".

## events
- Lane REBASED on main 7dea0626 (branch fleet-race), not lane/perf-fix: perf-fix's .lake was mid-build (files vanishing under cp) and
  basing on main makes before/after a clean single-variable comparison. Lean artifacts: cp -a of warm-7dea0626/src/.lake/build+config,
  cp -al of packages with every trace/hash/json/log privatised (0 shared). Sources are a git clone (no shared inodes).
- BASELINE main candidate (pipeline/artifacts/7dea0626…), fleetsign alone x3, runs/base-main/results.tsv:
  1 FAIL (1 turn, "remote challenge differs"), load 4.8->8.6; 2 FAIL (1 turn, same), load 8.6->5.0; 3 PASS, load 5.0->5.5.
  (Host stale-root signed-read replans already happen: 19/12/9 per run; the consent race is the only failure class.)
- Lean: `swarm-build lake build Kernel.NativeClientConsent Host.ClientConsentSession Host.Main` rc=0 (theorems + #assert_axioms green).
- Commit 7b8cdd38 (lane). Candidate chain runs/cand.pid -> fleet-race/cand-fix; status runs/cand-cand-fix.status.
- Candidate cand-fix @7b8cdd38 (fleet-race/cand-fix): host 1047 s, consent 69 s, rust 272 s, pack ok. mini/consent sha changed vs main.
- Unit (hbox, filtered `client_consent:: replan::`): 23 passed. New test only_a_provider_stale_observation_refusal_is_recorded_as_stale.
  RED once: mutation "any 221 refusal is stale" (drop the tag check, client_consent.rs:75) ->
  `panicked at native/resource-client/src/client_consent.rs:397:9: assertion failed: !take_stale_observation()` (the
  "remote challenge differs" case, i.e. an intent mutation would have been replanned). Reverted.
- Provider plant (plant.py, real minidregg-client-consent over stdio against a kept fix-run Store at head 121, alpha's key):
    fix:  current-h121 -> CONSENT; stale-h116 (own intent/sig/challenge) -> "stale observation: the remote challenge answers this intent
          at source height 116; the locally admitted source is at height 121"; intent-mutated (h116 intent+sig, h121 challenge of another
          intent) -> "remote challenge differs from locally prepared intent".
    main: current -> CONSENT; stale-h116 -> "remote challenge differs ..."; intent-mutated -> "remote challenge differs ...".
- Fix run 1 (kept): fleetsign PASS, load 12->13; 3 consent-stale replans taken (retired attempts with challenge, no signatures), all landed.
- Pushed lane/fleet-race = 7b8cdd38. Running: fix runs 2-3 + rows journey call send objectrecord seats (runs/fix/results.tsv).
- Not done: naming the replan's source in its stderr line (Host vs local consent). It is a compiled input, so it would need another
  host build before pack; the census reads retired attempts instead.
- AFTER, cand-fix @7b8cdd38, runs/fix/results.tsv (fleetsign alone, sequential):
    1 PASS 395 s, load 8.8->30.1, consent-stale replans 3, other signed-read replans 11, failed 0
    2 PASS 309 s, load 30.1->8.0, consent-stale replans 2, other 13, failed 0
    3 PASS 283 s, load 8.0->9.3,  consent-stale replans 2, other 11, failed 0
  (plus the kept run above: PASS, 3 consent-stale replans). 4/4 PASS; 10 consent-stale races replanned and landed, 0 "differs".
  BEFORE (main 7dea0626): 2/3 FAIL, each a single "remote challenge differs" turn.
- Rows on cand-fix: journey PASS 437 s; call PASS (63 rows); send PASS (192 rows); objectrecord PASS (39 rows); seats PASS (91/91).
- Kept for the plant: fleet-race/tmp/pr.HkSN (a fix run's fixture + fleet-home; test keys only). Delete when no longer needed.
