# FAERIE-DEAD

Landed 262d5b4d on nanodregg main (3 files, +26 / -131 net; readset.py -125). Control: kernel-sim --seeds 64 ALL PASS (built before the rebase onto 1e0849d5; the files touched are disjoint). readset reducer smoke-tested on a real strace trace (T, L, NS=False correct).

| item | result |
|---|---|
| journal subsystem (Census/Journal*.lean, gates/journal*.py) | already gone by 6faa9848 |
| `openFollower` | already gone (HOST-77, decisions/host.md) |
| `.provenance` refusal | kept: cannot fail by the reader's argument but unreachability is not a theorem; deleting is weakening a check |
| `instanceRecheck` refusal | kept, same reason (checkE is the invocation boundary); plant uses name 10^300 which holeROMWire refuses (LANG-owned fix: use an in-memory ill-typed body or drop the plant) |
| rows parent-retirement machinery | skipped per brief (RETIRE-2) |
| World.admit journal / refused-final checks | skipped per brief (KERNEL-67) |
| kernel-sim forgery plant skipping silently | fixed: `forge = none` now `failWith`s (Kernel/Sim/Gen.lean) |
| gates/readset.py bwrap translation | deleted: host_path, bind/pivot tables, HOST_VIEW, mount/pivot_root/umount2/mount-API handling, --decode-pids=pidns, exit tracking. NS records are simply unkeyable (`keyable` = NS is False); runs.py message updated |
| other DEBT dead-code items (Page.chain decoded unread, etc.) | not touched: wire-shape decisions, not pure deletion |

No gates/runs.tsv row named a deleted exe.
