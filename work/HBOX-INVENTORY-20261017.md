# hbox inventory, 2026-10-17 ~22:03Z (read-only; nothing deleted, nothing committed)

Taken after the lane swarm died (~21:55Z). Worktrees are unchanged: no commit, reset, checkout, stash or clean was run. The only writes on hbox were the two patch files and a scratch script at `/tmp/inv-faerie.sh`.

## 1. Preserved WIP patches (in `/tank/dregg-build/nanodregg/logs/`)

| patch | size | files | base | what it is |
|---|---|---|---|---|
| `host11-wip-20261017.patch` | 49,705 B | 13 (523+/41-), 0 staged, 0 untracked | 71379a1 | HOST-11's in-progress HOST-41. It touches Host/{Exit,Follow,Loop,Page,Record}, Host/Proofs/{Deployed,Page}, Host/Sim/{File,Run}, Protocol/Command/Machine, Protocol/Proofs/Command, Protocol/Table, and decisions/host.md (+81). |
| `client3-wip-20261017.patch` | 41,143 B | 12 (10 modified + 2 untracked text files appended via `--no-index`), 0 staged | 1db64e8 | CLIENT-3's `nd --stdio` (CLIENT-24). It adds `client/src/stdio.rs` (5,471 B) and `client/tests/stdio.rs` (9,968 B). It modifies nd.rs, nd-supervise.rs (-60 net), custody.rs, mux.rs, sockets.rs, lib.rs, the custody and supervise tests, decisions/client.md and gates/runs.tsv (+4 rows). 258+/60- on the tracked files. |

Both patches apply with `git apply` on the stated base. Check that they reproduce the dirty tree before relying on them: the client patch has two new-file sections. The client work is complete and green, waiting only on the ceiling raise 2000 to 2150 that ROOT approved. Neither worktree has binary files.

## 2. Worktrees (`/tank/dregg-build/nanodregg/wt/`)

| wt | dirty | HEAD |
|---|---|---|
| client | 12 | 1db64e8 protocol: grain row names its physical half |
| host | 13 | 71379a1 host: host export / openWith_exportFile_ok (HOST-40) |
| codec | 0 | 71379a1 |
| ledger | 0 | 71379a1 |
| protocol | 0 | 71379a1 |
| gates | 0 | d13c5b0 gates: codec vector immutable under unchanged tag (GATES-13) |
| hosting | 0 | d7c9d95 hosting: peer test CONTROL (HOST-11's red in broker) |
| kernel | 0 | 5eb9b30 kernel!: journal is a second trie instance (KERNEL-41 a') |
| lang | 0 | c302e25 lang: Std.stepTo refuses ambiguous edge (LANG-43) |
| ops | 0 | 013f35d ops: restore deploy/live/README.md |
| perf | 0 | 463200a protocol: rows' Store is HOST's genesis image |
| root | 0 | 3fbbd13 charter: README |
| transport | 0 | d5d7266 protocol: row wrongWorldRead (PROTOCOL-29) |

All clean except client and host, which are preserved above.

## 3. logs/ (total 702 MB; all files dated 2026-10-17, newest 18:03 = my patches)

Grouped by lane family. Size is `du -ch` over the family's `<prefix>[-.]*` entries. Newest times are local hbox time.

| family (prefixes) | entries | size | newest |
|---|---|---|---|
| ops3 | 69 | 218M | 14:35 (ops3-c10.out) |
| hosting (hosting, 4, 5, 6, 7) | 124+60+41+38+19 | 155M+159M+197K+247K+110K = ~314M | hosting7 16:56; hosting 09:50; hosting4 11:05 |
| host11 | 130 | 43M | 18:03 (my patch); lane's own 16:28 or earlier |
| codec4 | 15 | 61M | 09:50 |
| ops2 | 90 | 24M | 12:10 |
| host10 | 59 | 8.5M | 16:28 |
| kernel (kernel, 6, 6p, 7, 8, 9, 10, 11, 12, 31) | 56+13+8+49+64+50+41+22+26+53 | ~14M | kernel12 16:25; kernel9 11:26 |
| host (host, 6, 7, 8, 9, HOST, host2x) | 59+35+28+50+52+2+misc | ~12.5M | host7 12:54 |
| lang (lang, 5..12) | 56+12+16+19+15+18+38+20+10 | ~4.3M (lang11 3.0M) | lang12 14:56 |
| client, client3 | 53, 77 | 335K, 351K | client3 18:03 (my patch) |
| codec, codec2/3/5/6/7 | 60, 2, 27, 25, 23, 9 | 930K, 49K, 440K, 101K, 152K, 121K | codec7 15:46 |
| protocol, protocol6, protocol7 | 86, 68, 36 | 447K, 362K, 218K | protocol7 14:15 |
| ledger, ledger2/3/4/5 | 23, 38, 14, 1, 1 | ~610K | ledger3 13:33 |
| transport | 105 | 533K | 06:41 |
| gates3 | 15 | 226K | 12:45 |
| ops (original) | 14 | 187K | 00:45 |
| p32, k12, warm, standing, misc scripts and msgs (d2*, dec*, msg*, patch*, vt*, ob*, ...) | ~70 | <200K | various; k12 14:51 |
| root-standing-*.log | 1 | 4.5K | 11:24 (file is named T151833Z but dated 11:24 local; not investigated) |
| ROLES.txt | 1 | 21K | 14:26 |

Five largest entries (directories; `ls -S` sees only files, so these are by `du`):
1. `ops3-cargo-target/` 145M
2. `hosting-lane-target/` 115M
3. `hosting4-ws-target/` 107M
4. `codec4-target/` 60M
5. `hosting4-client-target/` 52M

Next: `hosting-lane-target-with-a-much-longer-name-...` 40M, `ops3-src` 34M, `ops3-bin` 34M, `host11-l41-red-tree` 31M, `ops2-cargo-target` 11M. The biggest plain files are tiny (`codec-h2.rlib` 173K, `codec-h.rlib` 169K, `codec-sample2.rlib` 153K, `kernel6-k7r6.patch` 129K, `kernel7-r5.patch` 129K).

Roughly 640 of the 702 MB is cargo target dirs and lane source copies.

Per-prefix top-5 file lists are not reproduced here. The raw output is at `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/a8357d63-efef-43bb-a4da-cdc3905383e7/scratchpad/out.txt` (lines 360-846).

## 4. Orphan judge trees

`/tank/dregg-build/nanodregg/main/.git/nanodregg-commit-main/` holds one dir, `1180086/`, 4.0M, last modified 14:58 (parent dir 17:20). It is a leftover from a commit judge that did not clean up.

## 5. Disk

`/tank` is 1.7T, 1.4T used, 349G free, 80%. Not under pressure.

## 6. Continuation sections

`/tank/dregg-build/nanodregg/logs/ROLES.txt` exists: 26,596 B, 134 lines, written 14:26. I did not read the contents.

## 7. Recommendation for a successor (nothing deleted by me)

Deletable, as files a lane created under logs/, once ROOT has confirmed no lane is resurrected from them:
- The cargo target dirs and lane source copies, about 580 MB: `ops3-cargo-target`, `hosting-lane-target`, `hosting-lane-target-with-a-much-longer-name-...`, `hosting4-ws-target`, `hosting4-client-target`, `codec4-target`, `ops2-cargo-target`, `ops3-src`, `ops3-bin`. They are regenerable build output.
- `host11-l41-red-tree` (31M), only after the host11 patch is verified. It is the HOST-41 red reproduction tree.
- `/tank/dregg-build/nanodregg/main/.git/nanodregg-commit-main/1180086` (4M, orphan judge tree). Check first that no `git worktree list` entry points at it.

Do not delete:
- `host11-wip-20261017.patch`, `client3-wip-20261017.patch` and `ROLES.txt`.
- Any `*.patch`, `*.msg`, `*.md` or commit log in logs/ until the continuations are written. Together they are under 60 MB and are the only record of rejected or WIP attempts (for example `kernel9-k38-rejected.patch`, `lang6-lang31-wip.patch`).
- Nothing under `wt/` or `main/`.

Freed space would not matter much anyway: 349G is free.
