# HP-DESIGN log (continuation file) — started 2026-10-14 ~19:00
Lane: HP-DESIGN (Fable architect, cap ~250K). Deliverable: docs/HP-DESIGN.md on lane hp-design (base `next`), ≤400 lines;
push mirror lane/hp-design; GitHub via ROOT. Brief: Ember 10-14 "bite the bullet, stop measuring every tiny change,
reorient the entire system into a high-performance design (tigerstyle)".

## events
- 19:00 start. READ in full: SINS-LEDGER-20261009, WASTE-MODEL.md (lane/cost-model d670d30a), perf-trace/{CREATE,JUDGE,READ},
  OB-WORLD-DESIGN §0–§4, TURN-LOG-LOG, STATE-AT-LOG, STORE-ROOT-LOG, CONSENT-MODEL-LOG, CODEC-SHAPES-LOG, PERF-MEMO-LOG,
  COST-MODEL-LOG, DELVE-SCOUT §1, TIGER_STYLE.md (fetched raw, 511 lines). Signatures read on origin/next Kernel/World.lean
  (World, Turn, History, admit/step/fold), lane/state-at Kernel/CellTable.lean, lane/turn-log Kernel/TurnLog.lean +
  DeployedTurnCompact.lean, lane/store-root Theory/AuthTrieCache.lean, lane/cost-model docs/waste-model.tsv.
- Mirror = hbox:/tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git (from lane logs). Workbox origin = GitHub.
- MEASURED on next (git grep, Kernel Compiler Host [Theory]): `List UInt8` 5065 vs `ByteArray` 372; `partial def` 56;
  `panic!`/`assert!` 0; `implemented_by` 2; `@[csimp]` 51; files mentioning Digest 509; NativeCoprocess users 3; Host/Main.lean 9164 lines.
- 19:40 docs/HP-DESIGN.md written (344 lines). Committed 4329b99c on branch hp-design = next 0125b224 + the one file
  (temporary-index commit, no worktree: the Mac data volume is at 96%). Pushed mirror lane/hp-design. GitHub: ROOT pushes
  (`git push git@github.com:emberian/minidregg.git 4329b99c:refs/heads/lane/hp-design` from the Mac workbox works if wanted).
- Five decisions: (1) one resident Host per Store = only writer/executor; log = Turns, checkpoint = World, follower = only replayer;
  (2) batched admission: ≤batchTurnsMax per store transaction, one fsync, one tag at batch end; (3) ByteArray end to end, 32-byte
  digests, one-pass canonical codecs; (4) Kernel/Bounds.lean + a runtime assertion per theorem-stated invariant; (5) seeded
  deterministic simulation (loop + follower + crash-restart) is the gate; measure only at range ends.
- First three new ranges: HP-1 BOUNDS, HP-3 LOOP, HP-6 SIM. Then HP-4 CLIENT, HP-5 ASSERT, HP-2 BYTES+DIGEST (one flag day
  after TURN-LOG 4b + CODEC-SHAPES item 1), HP-7 KECCAK.
- Reported to ROOT. Lane ends unless ROOT asks for revisions.
