# SCHEMA-V2-2 (a141173431eb8d455) -- resume note
Where it was: reading ("Look for committed Store fixtures"). Mission (ledger): "flat client re-check, store open at 3000, named epoch refusals"; STATUS.txt: consent anchor (Kernel/ConsentAnchor.lean, frames 228/229, Rust client_consent.rs retained anchor) + seed frame v2 carries the StoreEpoch label.
Lane: burst-lane1 ember@162.43.189.7 /srv/lanes/schema-v2-2/src, branch lane/schema-v2-2 @4e250db9 (base 5f9aa259), 4 unlanded (e4ef60ea gates SessionIndex, d3ede0a7 wip consent anchor, 7e96c66a fix forward, 4e250db9 anchors under ~/.mini/consent-anchors). Also /srv/lanes/schema-v2-2-main (detached 3b709c87, comparison baseline).
WIP branch: lane/schema-v2-2-wip @4bc9f83a (Compiler/DurableCheckpointCodec.lean +4/-2).
STILL RUNNING (not mine, left alone): /srv/lanes/schema-v2-2/growth-levels.sh mine (bin-mine/mini serve) at levels 300/1000/2000/3000; logs/levels-mine2.log was at count 1020 after 1007 writes, levels-main.log (baseline) at 120. Evidence in evidence/, w/.
Builds: no rc-bearing log among newest (levels-*.log, q1-sweep.log are measurement logs); b2.log from STATUS "IN FLIGHT" not re-verified.
Main since pause: 53 landings since 5f9aa259; overlap Compiler/CanonicalCellRegistry, DeclaredEffectCell(+Registry), DeployedCellRegistry, DurableCheckpointCodec, DurableLogTags, DurableReceiverIO -- expect real conflicts and an epoch/schema re-genesis.
Bundle: persvati:/home/ember/workbox/claude-lanes/bundles/schema-v2-2-lane1.bundle (prereq 5f9aa259; contains -wip).
Next step: let growth-levels finish (read levels-mine2.log vs levels-main.log), then rebase onto main (resolve the registry/codec overlaps), build minidregg-client-consent* + minidregg-host, run the open-at-3000 check.

Written by FAIRY-RESUME 2026-10-04 ~18:40Z. main = github/main 66e3c5b5 (== burst-gate /srv/warm-base/src; umbrella green: /srv/warm-base/logs/green-66e3c5b5.log rc=0 18:21Z). Pause was ~18:00Z (usage wall). Boxes die 2026-10-05T15:55Z. Bundles are THIN (need prereq on main).

## VISIT (VISIT-B, 2026-10-04 ~19:20Z; main d27d1cad)
VERDICT: BLOCKED-ON its own growth-levels run (then READY: rebase done, checks pending).
- Verified: 8 of 12 lane commits LANDED by patch-id (the room-schema v2 + session-index range: cbd23398..cbb14cce); e4ef60ea (pins) landed in regenerated form as 4b7a5b9f. Unlanded: d3ede0a7, 7e96c66a, 4e250db9 (consent anchor) + WIP 4bc9f83a (DurableCheckpointCodec +4/-2). Tree == WIP.
- Prepared WITHOUT touching src (the growth run uses this lane): branch lane/schema-v2-2-visit @8f18bc6b = the 3 commits + WIP rebased onto d27d1cad in a temporary worktree (removed after). Only conflict was e4ef60ea's two pin files (protocol/lean-build-surfaces.json, scripts/gates/host-closure.pin), skipped as already upstream. Files: Compiler/DurableCheckpointCodec, DurableReceiverIO, Host/ClientConsentCore, Kernel/ConsentAnchor, NativeClientConsent, NativeHostReplay, NativeHostSession, NativeSpecializedConsent, native/hyperdocument-link-sqlite-store/src/{lib,main}.rs, native/resource-client/src/client_consent.rs.
- NOT checked: lane-check needs the lane's warm src, which the growth run occupies; burst-lane1 load was 27 (>20). Textually clean is not compile-clean: main changed the registry/codec files around these.
- Growth run: logs/levels-mine2.log at count 2020 after 1991 writes (target 3000); levels-main.log (baseline) at 120 (target 300).
- Next 1-2 h (burst-lane1, one slot): when levels-mine2 reaches 3000 read it against levels-main; in src switch to lane/schema-v2-2-visit (tree == WIP, so: update HEAD to the branch, `git reset`), lane-check the 8 Lean files, build minidregg-client-consent* + minidregg-host (sccache), run the open-at-3000 check, regenerate pins, queue. Store epoch/schema change => say what re-genesises.
- Dependencies: overlaps LAWS-RECEIVER on Kernel/NativeHostReplay.lean (and CanonicalCellRegistry upstream); whichever queues second rebases on `next`.
