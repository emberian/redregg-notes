# CARRY — the re-genesis path for the World as it is now (OVERLOOKED-20261027 A1)

Worktree: hbox `~/nd-land/carry` (from origin/main 8fe58cbf). Builds: `~/nd-land/carry-logs/<name>.{log,pid}`.

## WORKLOG
- 2026-10-27 12:10 worktree made; read Carry, Follow (carry, authority), AuthorityOf, Head, RUNBOOK §6.
- Design (decision entries written in the tree, not yet landed): KERNEL-79 (carry takes a stated authority; re-authored trie; meter carried, refusal records dropped; origin = CarryStart digest, four roots + authority), CODEC-41 (carried window trie, `kernel/carried-window`), HOST-82 (`host import --certifier/--threshold/--uncertified`, `authorityUnstated`), PROTOCOL-85 (carried start = carry start; stranger checks carried certificates).
- Theorems: Kernel/Proofs/CarrySound.lean (`carry_sound`, `carry_meter`, `carry_ticksUsed`, `authorityOf_honest_fold_carry`, `deployed_carry_authority`), Host/Proofs/Carry.lean `importWorld_sound`.
- Rows: store-plants `carry-*authority*`, `carry-certified-*`; host-sim `plant-carry-authority-*`; kernel-sim `carry-authority:*`, `carry-meter:kept`.
- Docs: RUNBOOK §6 rewritten (+ §6a the testground box), docs/TRUST.md carry paragraph.
- cv task 01a17e51-e132: testground cannot follow/join a carried World (tg_found/tg_join genesis-only); §6a says the box's next flag day is a re-genesis until it lands.
- 2026-10-27 13:05 kernel build k2 queued (slots full).
- NOTE: early in the session I extracted files into an existing scratch mirror `scratchpad/nd/` (another lane's git repo) by mistake; I restored the four files it showed modified to its base with `git checkout` and moved to `scratchpad/carry-mirror/`. If that lane had uncommitted edits in Host/Cli.lean, Kernel/Receive/Follow.lean, Kernel/World.lean or docs/TRUST.md, they were lost. A `scratchpad/push.sh` may also have been overwritten (now `carry-push.sh`).
- 2026-10-27 13:40 REPLY (METHOD-20261027): next landing = the whole carry change (KERNEL-79/CODEC-41/HOST-82/PROTOCOL-85, all edits already written across ~35 files); one reach build now, fix from the full log, one more build, rebase once, land via scripts/commit — target within ~2h. No new .lake copies beyond the one made at start (~/nd-land/carry, will be removed at landing).
