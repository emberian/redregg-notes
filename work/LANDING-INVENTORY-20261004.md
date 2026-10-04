# LANDING INVENTORY 2026-10-04 (lander, ~02:55 EDT)

Method: fetch each clone's main, `git cherry origin/main FETCH_HEAD` ('+' = not on main by patch-id).
Main at start: e598326e. Main now: see SWARM-LEDGER lander lines (last push 1ffe6bf3).

## LANDED by the lander
- frontend 1b2610b3: identical content already on main (empty cherry-pick), skipped.
- s4-examples 370e972d, s3-tutorial 9d49f513 b1403871 874559a0, followups 041a0207 -> 6909eaf9
- s1-market (6 commits) -> f0c95118
- rewriter f882bd01 (conflict in chat.rs::client resolved: tenancy's passphrase-to-child block dropped, no child exists) -> 336b7c0e
- rewriter uncommitted shared_names.rs (room->index hint; Rust-alone) -> 1ffe6bf3

## DUPLICATE / SKIPPED
- shipfix d83e97f5 (judge_tail): main already has the equivalent `simp [checked, bind, Except.bind]` fix.
- shipfix b45237d1, 0191cb8a: followups lane re-lands them (0191cb8a not yet seen on main).
- audit, backends, bread-a, bread-b, completeness, contracts, deploy, docs, events, gates, mpc, rooms, sdk, sums, tenancy, traffic: 0 unlanded by patch-id.
- fastmachine, s2-collective, s3/s4 (beyond above): no commits beyond main.

## HELD (per mandate)
- cut (12 commits, 7298b7f5..d3a5c5d4): root / CUT-REBASE lane.
- native-b (13, sit on cut base): 8 are the cut's commits; 2ea8cea7 1e776220 afb52964 ba824e89 d9570147 are native.
- rooms-schema (a888c312 0c6116b5 8c2f3c29 e218c57f 72b2abee): breaking, needs native host build.
- spk (75671e8d 601ee402 87b6c9b5 a8830638): uncompiled, touches Kernel/NativeHostReplay + Host/Main.
- zktruth (932ea893 82548487): uncompiled Lean (new files only).
- proofeng (fc5c7730 eb004055): lane still running; eb004055 rewrites Theory/ObjectiveBend* proofs (3.5k/-2.5k) and
  lakefile.toml/ObjectiveProofs.lean (a42afbfc is the cut's), STATUS says "lands with or without the cut" but root asked to avoid lakefile.toml pre-cut; no STATUS "ready".
- agreement (c641dad2 d72113f5 c4a6359a 7e7806e0 a5e61411 a336dfa4 = bde7fab2 af6501ee e194778d 242c5f67 eaac4a4e 2e74773c):
  CONFLICT RESOLVED in /tank/dregg-build/claude-lander-20261004/src (branch main there) between the lane's intake (renames run->runSource, restart test inside run) and audit D16 8283579d.
  Resolution: kept D16 structure (run = tipKey agreement, no restart test; runWithLostResponseCheck/runCallChecked = fixtures-only restart test)
  AND the lane's standing-replica structure (drive over Serve.iteration, restoreLog journal checks); fixture drops runCall/"run" verbs for serve-replica/await-call/lookup-all/convert-journal.
  NOT landed: Lean not compiled in lander (hbox load 27-29, no coherent packages dir; root forbade the warm-base symlink). Two aborted lake builds (logs agree-1..5 under the lander dir).
  Also open (lane STATUS): journal decoder (decodeDeltas) is non-tail-recursive -> stack overflow on reopening a long journal; must be fixed before cutover.

## UNCOMMITTED WORK AT RISK (hbox clones)
- bread-a: Kernel/AgreementEvidenceRegime.lean (never compiled)
- bread-b: Theory/CertF.lean (uncompiled), Kernel/GenericSimplexReconfig.lean (last check failed)
- contracts: Kernel/Contracts/Refinements.lean (never compiled); docs/CONTRACTS.md unwritten
- followups: EmitC/DataWire edits beyond 041a0207 (Compiler/ObjectiveBendDataWire.lean untracked, runtime.c, differential.py modified, fixtures/ untracked) -- may be dirty after 041a0207
- rewriter: 13 modified files in `uncommitted-20261004.patch` (client_consent/workspace/transport/receipt_continuity need Host/Main.lean `codecs` mode, not compiled; receipt_continuity mid-edit with 16 red tests); shared_names part LANDED.
- shipfix: 23 modified + Kernel/RefusalLane.lean (staged): items 4 (refusal charging) and 6 (tickets) await a native build
- s1-market (superseded by landed), s2-collective world/workshop/ untracked, s3-tutorial docs/tutorial untracked(landed?), s4-examples: 9 paths (landed 370e972d; verify none left)
- zktruth: 15 untracked Assurance/Compiler/Theory files (the 932ea893 commit covers part)
- deploy/gates/proofeng: build-logs and __pycache__ only
- dregg-infra: deploy clone c065497 and tenancy clone (c98386d 866a415) are on hbox:/srv/git/dregg-infra.git already (HEAD..origin empty, not ahead).
