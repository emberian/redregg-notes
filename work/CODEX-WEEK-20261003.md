<!-- Provenance: written 2026-10-03 night by an Opus scout under Fable (session 9627d694), read-only, from the Codex transcripts (cv), origin/dev at d4e53323c, the Claude coordinator files and the design docs. Engineering state only; nothing was built or run. Companion to FABLE-FN-SESSION-20261003.md (the process audit) and FN-SWARMPLAN-20261004.md (the plan). Per-era detail in codex-week-20261003/{era1,era2-core,era2-edge,generators}.md. -->

# What Codex designed and implemented in `fn`, 2026-09-29 → 2026-10-03, by subsystem

Coordinate: `origin/dev` **d4e53323c** (10-03 15:20 -0400); snapshot `scratchpad/fn-dev-d4e53323c/`.
Read-only: nothing was built, certified or run. Pre-10-02 shas are given as old→new through
`planning/commit-map-20261002.txt`. Per-family detail with every file:line sits in the four
working notes beside this file; this document is the merged account:
`era1.md` (era-1 families F01-F12 at d4e), `era2-core.md` (store/served/accounting/lifecycle),
`era2-edge.md` (BP/web/operator/tools/tests/planning), `generators.md` (generators, codex-liaison,
stage 0). Supporting data: `py/closure.py`, `clos-*.json`, `era1-image.json`, `devlog.txt`, `era2-log.txt`.

## 0. Who is "Codex" this week: three channels, and attribution corrections

| Channel | When (EDT) | Commits on dev | Diffstat | Character |
|---|---|---|---|---|
| **Era 1**: root `01a0eeec` (gpt-6 + Sol/Astra deputies, 25-28 agents) | 09-29 16:50 → 10-01 ~04:30 | 768 (`cbd530797`=7aad444ce .. `87cb67a2e`=b34835bd4) | 1,771 files, +336,536 / −59,651 | A new runtime skeleton under the served node, plus ~678 books |
| **codex-liaison**: Claude Opus lane driving `codex exec` (gpt-6.1-sol t01-t02, gpt-6-astra t03+) | 10-01 → 10-02 23:12Z (usage limit until 10-08) | tasks t01-t44 inside Claude batches BH-BM | inside the 921-commit Claude interlude (+282,936 / −18,625) | Tools/registry/docs, def-loop conversions, ~72 reviews (r01-r72), 10 design consultations (c01-c10), one whole-system answer (w01) |
| **Era 2**: root `01a0fe41` (16 Sol deputies, 1 Astra tracer, 4 Luna proof helpers, 4 "horse" auditors, 1 lieutenant) | 10-02 16:16 / 10-03 01:18 → 15:20 | 727 (`8d17b09dd`..`d4e53323c`, all pushed by `deputy_integration` as recomposed commits) | 966 files, +118,545 / −19,766 (`3564fba83..d4e53323c`) | Wiring joins onto dev under "push before verify" |

Attribution corrections that change the picture (verified by adding commit):
- **The 12 `planning/design/*-2026-10-03.md` docs, the 24 `planning/handoff-2026-10-03/*.md` and the repair
  ledger (`planning/repair/repair.py`) are Claude's**, all from one commit `b0afc2c21` (10-02 22:47,
  "Track the coordination state in the repo", Co-Authored-By Claude Opus 5.5), merged by Batch BM `d15adc1f3`.
  Codex content inside that set is only `whole-system-correctness-astra-2026-10-03.md` (liaison w01, 1,675 l.)
  and the consults the docs quote.
- **The generator family (def-loop, def-representation, def-carried(-writer), def-carried-view, def-keyset-check,
  defkeystone v2/defteeth, def-holder, def-command, def-cost, def-section) is Claude-designed and
  Claude-implemented** (Fable lanes generators, def-carried, generators-2, def-holder, def-entry, def-command,
  failure-scope, 10-01..10-02). Era 1 wrote none. Codex's generator share is via the liaison (reviews, def-loop
  conversions, fix tasks, adopted consults) and era 2 (def-cursor, def-actor, definterface `:operation`, def-cost's
  first host rows, the DC02 dispatcher switch).
- Three 09-29 designs often credited to Codex are Claude's: `design-extent-read-protocol-2026-09-29.md` (e7e6f21d5),
  `design-paged-history-2026-09-29.md` (9436e321b), `design-resilience-framework-2026-09-29.md` (b344e9fa8);
  so is `specs/resource-vector.md` (877c69598, Claude resource-ledger, 10-01; era 2 then made 40 commits to it).
- Era-2's own design text: `planning/overnight-2026-10-03.md` (524 l., 22 revisions), `NSLICESQUEUE.md`
  (852 l., 25 slices, created `321bd7246` 04:37), `planning/empirical-workloads.md` (`030f9a2c6`), `planning/now.md`
  rewrites, LANEDUMP from ~line 1012 (+5,887 lines across these files), 26-27 new repair items, spec edits
  (`resource-vector.md` 40 commits, `nntp.md` 37, `host.md` 23, `human-client.md` 17).
- Era 2 began by merging Claude WIP (`79850a877` served-live, `a2b2bc827` post-guard-off, `59b8d97af` def-section
  step 0, `8cf37a368` burndown-3), and reworked several Claude-origin books (`failure-scope`, `host-model-machine`,
  `history-columns-foundation`, `protocol-served-table`).

State tags used: `on-dev-wired` (a host/native caller on the served or operator path at d4e) · `on-dev-unwired` ·
`on-dev-twin` (shadows a proved path) · `branch-only` · `parked` (out of image / `planning/host-parked.json`, 82
host files, owner "L3") · `reverted-by-stage-0` · `deleted` · `prose-only`.

Registry at d4e (`planning/proofs.json`, 683 rows): **certified 59 · uncertified-at-current-digest 489 · planned 135.**
`planning/current-view.json`: 25 capability rows, 4 proved (operator-journal-stream, PRF-1021, bp-source-window,
bp-source-control), 0 qualified. Of era-1's PRF range 1030-1200: 6 certified (1057, 1059, 1061, 1067, 1080, 1190),
48 uncertified, 44 planned. `planning/now.md:35`: "There is no current whole-system native endpoint."

---

## 1. Store, page pool, arena & history

**Designed.**
- Era 1: `build/coordinator/allocation-epoch-design-2026-09-30.md` (190 l.). The cold read becomes a pool-charged
  admission with a pool-owned worker. Completion publishes only for the exact issued token of a still-`:issued` row.
- Era 1: `planning/dense-history-epoch-2026-09-30.md` (388), `dense-history-owner-producer-2026-10-01.md` (285),
  `history-provider-stable-addresses-2026-10-01.md` (105). History becomes an in-memory append-only epoch of 256-reference
  pages in a binomial forest, with low-bit-first stable addresses and capture custody.
- Era 1: the checkpoint-writer contracts. These are `history-page-cursor-contract.md` (319), `history-decode-contract.md` (181),
  `page-digest-cursor-contract.md` (166), `checkpoint-reference-cursor-2026-09-30.md` (156) and
  `checkpoint-payload-lifetime-contract-2026-09-30.md` (141), plus specs `extent-window-read.md` (548) and `payload-window.md` (157).
  The writer works census-then-emit with bounded steps, a resumable BLAKE3 machine and 16 KiB windows.
- Era 2: NSLICESQUEUE §"Page-backed history and node roots" (:267), §"Reclaim and physical release" (:287),
  §"Checkpoint, recovery…" (:304), §"Paged catalog in the service" (:237). LANEDUMP "Native history roots — Sol" (:1895)
  makes the design choice explicit: build on `fn-hrecs`/P3, because "connecting [era-1's backing] alone would duplicate P3".

**Implemented (state at d4e).**

| Mechanism | Where (d4e) | State |
|---|---|---|
| Page-read pool ownership: `page-read-{pool-state 37, ledger 262, resources 159, ownership 172, executor 155}`, `cold-read-reservation` 93, host `page-read-host.lisp:32,62`, `extent.lisp:122,642,995,1141` (era 1) | installed at start by era 2: `host/native/owner.lisp:8210-8257` (`fn-owner-page-read-install-default` → storage-start → executor-start), `0ca006108` 10-03 12:38, `162bc5cbe` | **on-dev-wired** (era 1 never called the installers; era 2 made KW-a's join; never executed natively at these bytes) |
| Protected windows, stored-DEFLATE chunk, decoded window (era 1: 36 image books incl. `decoded-window-*`, `extent-window-*`, `payload-window` 328) | era 2 connected them: `owner.lisp:5769-5800` (window discovery :5778, `19ec62b71`), `host/native/extent-decoded.lisp` 179 l. loaded `build.lisp:459` | **on-dev-wired (by era 2)**, against the critic's DELETE verdict for decoded-window; `host-parked.json` still lists `extent-decoded.lisp` as parked (inconsistent) |
| Incoming buffers `incoming-copy-stobj` 229 + 3 | only users `page-read-host.lisp` and parked `receiver-turn-parked.lisp` | on-dev-unwired |
| Dense history epoch `history-event-{page,directory,provider,backing}` | out of image; 4 host files parked; `fn-owner-history-produce-step` exists nowhere | **parked** (D42: P3 ratified over it) |
| Eight owner-host history gates (era 1, 89dca11b3 / 930b3e641 / beeedbf1f) | `host/owner-host.lisp:471,518,539,610,666…` → `history-semantic-writer.lisp:25` | on-dev-wired, inert (critic and L3 say remove; not removed) |
| Checkpoint writer library (`history-scalar-cursor`, `-record-cursor`, `-decode-*`, `pagestore-digest-cursor` 230, `store-tree-size` 160) | no host reference to `pgs-dc-`/`fn-hrsc-`/`fn-hrcur-` | on-dev-unwired |
| Snapshot/INITIAL natives, recovery driver (era 1) | `snapshot-{startup,producer,initial-reader}.lisp` parked; `runtime-recovery-file`, `recovery-profile-read`, 3 host files deleted | parked / deleted |
| `store bless-snapshot` (`owner-snapshot-request` 232; `operator.lisp:701-702`) and `owner-snapshot-recovery` 1,708 l. | in image | on-dev-wired |
| Moved owner entries `owner-recovery-retain` 332, `owner-retain-transitions` 197, `owner-cursor-domain` 369, `owner-reclaim-carry`, `owner-obligation-state` | served start | on-dev-wired |
| W9 obligation view `retention-obligation-view` 286 + view-delta + 546,341,504-octet heap term | out of image, no host `fn-rov-` | **reverted/parked** (D47, liaison t16 45e62e2de → 98c8e5bb3) |
| Statement recovery worker swap `statement-recover-stream` 136 | `io.lisp:1780,2970` call `fn-ssr-rows`; `store-open-host.lisp:648`, `store-write-host.lisp:1114` call `fn-srs-rows`; no relating theorem | **on-dev-twin** (KW-i) |
| Index backing, a second paged Message-ID table (~55 books, `index-backing-provider` 947) | out of image except 2; 9 host + `index-writer-turn.lisp` parked | parked |
| Era-2 incremental history image builder `history-image-build-rows` 92, `-row-step` 286; `host/native/history-root.lisp` 265 (build.lisp:540), `io.lisp:3696-3725` | replaces whole-suffix `fn-his-snapshot` in the three publishers | on-dev-wired |
| Era-2 P3 abstract stobj `fn-hist-paged` (`history-paged.lisp:393`, 403 l., 29 thm; `-adopt` 149; `history-pages-resident` 152) | host adopt/root-at | on-dev-wired |
| Era-2 page relocation continuation (Astra) `history-pages-relocate-step` 297, `-run` 160 | via builder | on-dev-wired |
| Era-2 root credit `history-root-credit` 121; `host/history-root-host.lisp` 227 | build.lisp:375 | on-dev-wired |
| Era-2 reclaim over P3 root (`owner.lisp:7439,7818,7875`) | still pushes every rewritten row then `fn-owner-orcp-rebuild` (`:7807-7823`) | on-dev-wired, partial (whole Store/catalog copies remain) |
| Era-2 catalog availability (`catalog-availability*` 75/56/246/70, `catalog-available-readers` 126, `served-availability` 177) | replaces `fn-sca-load-held-rows-*` in place | on-dev-wired; paired equality with the raw loader is false for unavailable rows (Integration idx 5515) |
| Era-2 arena return custody (`payload-view-lease.lisp:146`, `io.lisp:1726`, `owner.lisp:8216`) | reset/start/recover require `:closed` | on-dev-wired |
| Era-2 owner carrier `owner-carrier.lisp` 60 (not in image) + `owner-post-carried.lisp` 138 (def-carried-writer :74,:97) | `io.lisp:451-474` | carrier on-dev-unwired ("dormant", `b83173627`); POST writers on-dev-wired |

**Tested/proved.**
- Certified at current bytes:
  - PRF-1057 (issued cold reads keep identity through cancellation) and PRF-1080 (the persistent cold executor owns one charged job).
  - PRF-1067 (retention carry boundary).
  - PRF-1190 (forest growth).
  - The arena `:closed` gate (`certify-20261003T174041Z-2716643`).
  - The relocation step and run (`102524Z`, `103557Z`, at component bytes).
- Certified, but the bytes have since moved:
  - PRF-1265, the builder (`certify-20261003T101722Z-1422001`). Old-vs-new image equality is tested at `tests/acl2/history-image-builder-tests.lisp:65-70`.
- Uncertified or planned:
  - PRF-1060, PRF-1037 and PRF-1078 are uncertified.
  - PRF-1280 (P3) and PRF-1262 (availability) are planned, as are PRF-1109 and PRF-1112 (windows).
  - PRF-1050 (bless) is now planned; the critic had read it as certified.
- Native and fixture evidence:
  - No native run at d4e.
  - Pool startup is tested only by `tests/native_owner_pool_startup_source.lisp`, which stubs `fnn-core`, `fnn-extent-*` and `fnn-owner-install` (:53-182).
  - `tests/native_history_root_raw.lisp` stubs every ACL2 call (:94-141).
  - The whole-extent malloc remains at `extent.lisp:904,1154` (`make-array (+ elen 32)`; ST2's).

**Verdict for the harvest.**
- Pool install (KW-a): keep-and-wire. It is done in source; the funding theorem must be restated at the called name
  `fn-prstartup-default-plan-with-peer`, which is bridged only by definition, and then run natively. COMPLETE-BEFORE's
  "KW-a SUPERSEDED by ST6" tag is stale.
- P3 builder / `fn-hist-paged` / relocation / root credit: keep-and-wire (register PRF-1280, recertify). These are ST5's start.
- Reclaim over P3: gift-for-packet ST5/reclaim. The bounded walk is there; removing the whole copies is unstarted.
- Catalog availability: keep-and-wire after restating the refinement. It also serves as input to `group-count-after-reclaim-2026-10-03.md`.
- Windows/decoded window: now an era-2 served subject. The served-composition theorem is owed (PRF-1112); reconcile `host-parked.json`.
- Checkpoint writer library: gift-for-ST7/P8 (resumable BLAKE3 + record/scalar cursors); drop the cold sub-stack (8 books, ~3.9k l.).
- Dense epoch and the eight gates: superseded-by-ST5 (D42); drop the gates; keep the forest-address idea as design input.
- Index backing: superseded-by-ST3/ST7. The seed is `fn-iqr-promotion-preserves-resident-pool-total` plus the `fn-ibp-node` congruent-child idea.
- Statement worker twin: keep-and-wire the ~40-line `fn-ssr-rows = fn-srs-rows` theorem, or retire one worker.
- W9 view: gift-for-W9, per the D47 Completion (re-add with its reader and figure term together).
- Owner carrier: gift-for-packet ST1b/STAGE-5B (338 owed writers).

## 2. Served commands & cursors

**Designed.**
- Era 1: OVER response pins (`response-plan-pins`, PRF-1059), plus Claude's L1/L2 OVER cursor, which Codex merged.
- Era 1: productive READ keystones over the host-called `fn-mca-read-span`.
- Era 1: the D25 POST-identity source cursor (`specs/post-identity-source-cursor.md`).
- Era 1: the NOV byte-budgeted formatter and the legacy parser.
- Era 2: NSLICESQUEUE §"Complete bounded discovery and view policy" (:183), §"Finish streaming and restricted command
  families" (:197), §"Dense groups, overview and reclaim-aware navigation" (:253).
- Era 2: LANEDUMP "DC02 generated switch" (:1431), "Cursor cold reads poll on mux" (:1718), "Bounded LIST summary
  primitive" (:2987) and "Incremental LIST row/status source" (:3862, :4059).
- The view-policy table era 2 consumed (`command-view-policy-2026-10-03.md`) is Claude's; the liaison's c07 rulings were adopted in it.

**Implemented.**

| Mechanism | Where | State |
|---|---|---|
| OVER cursor + response pins (`over-window` 487 Claude, `served-plan-cursor` 545 Claude, `response-plan-pins` 151 Codex) | unpin restored `owner.lisp:709-718` by stage 0 (`ef55ef010`); mux wire-source gate removed | on-dev-wired |
| Productive READ/transfer `productive-read-chain` 1,230, `productive-transfer` 207 | out of image; PRF-1052-1054 absent from proofs.json; inbound 1126/1127 only on `lane/productive-read-transfer` | on-dev-unwired (proof-only) |
| D25 source cursor + 16 `captured-*` books; precheck `fnn-owner-captured-precheck-locked` | `host/native/post-captured-parked.lisp:67` | cursor **parked**; precheck **reverted-by-stage-0** (break 5) |
| Keepers `poster-bytes-source(-buffer)` 183/1,045, `post-admission-keyed` 147 | in image | on-dev-wired |
| NOV windows `nov-{byte,decimal,piece,span}-window` | in image closure, no host reference | on-dev-unwired |
| Legacy parser (12 books), group-number cursors | out of image | on-dev-unwired; `group-number-trie` 62 wired |
| Report capture `owner-report-capture` 117; reader-output | four fence call sites gone | on-dev-unwired |
| **Era-2 `def-cursor`** 153 + `-batch` 96 (VISITS and BYTES bounded separately; suspended op keeps custody until receipt) | consumers `newnews-metadata-cursor.lisp:182`, `list-metadata-cursor.lisp:155`, `newnews-stream-cursor.lisp:191,535`; host via `fnn-owner-cursor-step` (`owner.lisp:780`) | on-dev-wired; `fn-cur-split` mbe `:verify-guards nil` "UNVERIFIED WIP" (LANEDUMP:3111) |
| Era-2 LIST cursors `list-metadata` 209, `list-row` 151, `list-status` 132, `group-summary` 159, `served-query-plan` 92 | `owner.lisp:656-678,780`, wired `c94e83f87` | on-dev-wired |
| Era-2 NEWNEWS selectors + `wildmat-cursor` 1,133 (107 thm) + metadata/stream cursors 413/590 | via `served-plan-cursor` | on-dev-wired |
| Era-2 matcher live-peak bound `wildmat-live` 449 | test-only | on-dev-unwired |
| Era-2 string line renderer `string-line-cursor` 336, `-fill` 114, `served-plan-line-buffer` 119 | owner.lisp | on-dev-wired |
| Era-2 generated command switch: `protocol-served-table.lisp` 957 l. (Claude DC01 origin), DC02 `49eea4a24` (`served-catalog-chain.lisp:249-257`), 16 generated `:forms`; 31 rows, "no hand catalog-dispatch fallback" (`protocol-served.lisp:367`) | served catalog path | on-dev-wired; 10 view-policy debt rows (`tools/view_policy_debt.json`) |
| Era-2 selective "available" route `served-available-read.lisp` 533 l. (25/25 `:program`, generated by `tools/available_read_emit.py`) | host switched `6a5427e9e` (10-03 09:00) from `fn-mca-read-span` to `fn-av-mca-read-span` | **on-dev-twin**: PRF-380 and `fn-scar-ocfg-read-span-is-reference-under-ocl-relation` now describe an uncalled function |
| Era-2 cold read as mux poll (5-value quantum; `c922036e8`, `30bd8ab95`) | owner/mux | on-dev-wired; pull renderer ignores the 5th value (LANEDUMP:1755) |
| Era-2 response identity `response-identity` 52 | `owner.lisp:1830-1838` | on-dev-wired |
| Era-2 streaming ARTICLE `article-stream` 454, `-owner` 314 | `owner.lisp:756-826`, `mux.lisp:667` | on-dev-wired (`fn-owner-article-ready-plan-step` `:program`) |
| Era-2 HDR/XPAT `legacy-header-query` 181 (16 thm) | only tests | on-dev-unwired |
| Era-2 LIST reference/progress books | untracked in `build/lanes/codex-sol-served` | branch-only (untracked) |

**Tested/proved.**
- Certified: PRF-1059 (pins) and response-identity (`103508Z`).
- Uncertified at the current digest: PRF-1020 (OVER cursor), PRF-1236 (generated table), PRF-1256, 1257 and 1261 (NEWNEWS),
  and PRF-1274 (line renderer).
- Planned: PRF-1286 (ARTICLE stream), PRF-1287 (available route) and PRF-1304 (HDR/XPAT).
- Cert run `083937Z` lists `newnews-stream-cursor`, `served-plan-cursor` and `string-line-cursor` as FAILED ("no certificate on disk").
- `tests/acl2/served-query-plan-tests.lisp:128-133` drains at windows 1 and 256 and compares with `fn-nntp-list-command`.
  The universal cursor = reference theorem is not proved (LANEDUMP:4393-4395).
- Access's "184,483 ARTICLE checks" are loop counts in an SBCL harness that redefines ACL2 primitives
  (`tests/native_header_query_source.lisp:5-14`).
- `tests.test_cursor_cold_poll` is 1 pass with mocked ACL2/I/O.
- None of the era-2 served work has run natively at its bytes. The last image was `ad8da41fc` (05:44).

**Verdict.**
- OVER/pins: keep (done; certify PRF-1020; the L4 native pin rerun is owed).
- Productive reads: keep-and-wire (certify, register PRF-1052-1054, write `specs/productive-contract.md` §5; no new ACL2).
- D25 cursor: gift-for-the-POST-cost packet. The join is `fn-pic-run-arena` replacing `fn-rclb-same-articlep`, and only after the nine
  REPL-only books certify. Drop the 16 `captured-*` books.
- NOV windows: gift-for-OVER streaming.
- Legacy parser: drop, but relocate `fn-nlv-actual-parser-never-counter-error`.
- Reader-output: drop.
- def-cursor + LIST/NEWNEWS cursors: keep-and-wire. The packet is the universal cursor = reference theorem, the guards, and the OVER/HDR/XPAT instances.
- Generated switch: keep (DC04 + PRF-1238 debt).
- Available route: superseded-by the proved `fn-mca-read-span` chain. Revert `6a5427e9e`'s host switch, or prove the equality, before any cite.
- `legacy-header-query`: gift-for-packet HDR/XPAT (the join is Served dispatch).
- `wildmat-live`: gift for the output tariff, or drop.

## 3. Resource accounting, banks & tariffs

**Designed.**
- Era 1: `allocation-epoch-design-2026-09-30.md`, `specs/allocation-turns.md` (173) and `allocation-epoch.md` (13). An operation
  turn prepays a source-derived Qgate at entry and Qbody before its body. The prepaid total A never falls until a quiescent
  collection, and the bound is `f*(L0+A)+reserves <= budget`.
- Era 1: `specs/runtime-operation-compiled-source.md` (9 l.), a compiled per-operation cost table with a 17-field bootstrap
  capsule. The table is `nil`.
- Era 2: `specs/resource-vector.md` (Claude origin, extended in 40 era-2 commits), NSLICESQUEUE §"Output allocation and
  funding" (:122) and §"Resource accounting across operations" (:140).
- Era 2's idea: one typed ledger `fn-rl` with install/draw/settle refining the logical bank `fn-rv`. Each family draws before
  its effect and settles once. Physical return and operation outcome are separate receipts. The era-1 pool becomes the DEFAULT
  pool, installed before Store open. Peer flight work draws from its own bank.

**Implemented.**

| Mechanism | Where | State |
|---|---|---|
| Runtime bootstrap gate + compiled table (era 1; 16 F11 books still in image; `runtime-operation-compiled-table` 21 l., value nil) | gate removed `build.lisp:500-508`, `tools/extract/core-main.lisp:30-33` (stage 0 `ef55ef010`); 6 `runtime-*` natives parked, 3 deleted | **reverted-by-stage-0** (break 1, MODE rule 3) |
| `host/native/runtime-collector.lisp` 62 (SBCL finalizer-thread hook) | not loaded | on-dev-unwired residue |
| Allocation epoch `allocation-epoch` 341 (+pool 147 …) and turn slots `allocation-turn-slots` 446 | in image; `allocation-epoch-host.lisp` parked; `fnn-owner-control-binding-make` (`owner-control-turn.lisp:9`) has no caller | on-dev-unwired |
| `cold-read-reservation` 93 | build.lisp:209 | on-dev-wired |
| Era-2 typed ledger ↔ bank `resource-vector-exec.lisp:790,1676,1697` (+ liaison t23b relation teeth) | book | on-dev, certified `180036Z`, 0 digest mismatches |
| Era-2 syncer custody `resource-syncer` 230 + `definterface :operation` instance `fn-ros-issue` (`host/interfaces.lisp:38-44`) | `owner.lisp:1821,2058,2075,2078,2140` | on-dev-wired |
| Era-2 shared output pool `resource-output` 854 (74 thm, bank correspondence :727-757); chain `resource-output-chain` 395 | `owner.lisp:1867-2050` | pool on-dev-wired; chain on-dev-unwired |
| Era-2 output command admission `output-command-admission` 149 | `owner.lisp:1938-1941`; producer `host/owner-host.lisp:5514-5517` always `(:unpriced family)` | **on-dev-wired gate, producer absent**: 0/28 families priced; fail-open when `[resources] output_heap_octets` is absent |
| Era-2 output reservation in heap figure `output-reservation` 108 | heap.lisp | on-dev-wired |
| Era-2 DEFAULT pool install (§1) `page-read-startup` 245 | `owner.lisp:8210-8257` | on-dev-wired |
| Era-2 peer flight bank `peer-flight-{profile 44, reservation 129, startup 76}`, `peer-catchup-spool-resources` 29; `host/native/catchup-spool.lisp` 259 | bank installed `owner.lisp:8264`, closed `:8269`; `fnn-peer-flight-draw/-work/-settle` (`catchup-spool.lisp:200,223,240`) called only inside the file + its fixture | **on-dev-unwired** (a bank nothing draws from) |
| Era-2 resource operation reference `resource-operation` 140 | no caller, not in Makefile | on-dev-unwired |
| Era-2 def-cost host rows `host/cost-host.lisp` 36 l. (7 rows) + `string-line-cursor-cost` (4) | build.lisp:427 | on-dev-wired as a checked readout ("Partial means unknown, never an admission tariff", cost-host.lisp:1-4) |

**Tested/proved.**
- Certified: `resource-vector-exec`.
- Uncertified: PRF-1259 (output pool; cert `123849Z` has 13/296 digest mismatches), PRF-1278 (admission) and PRF-1301/1310 (DEFAULT install).
- Planned: PRF-1252 (syncer) and PRF-1156/1157 (turn slots; the critic read these certified at era-1 end).
- `planning/cost-obligations.json`: of 1,449 dispatched entries, proved 0, partial 1, derived 6 and none 1,442.
- The syncer has one native pass, `test_funded_syncer_from_mux_hold_post_and_stop`, on image `ad8da41fc`.
- "DEFAULT capacity replay timed out 30 s, not proved" (checks.json).

**Verdict.**
- Typed ledger + syncer custody: keep (the best-grounded era-2 item; the syncer's bank theorem is owed).
- Output pool: keep-and-wire (certify).
- Output admission: gift-for-packet ST6. Keep the gate off until a tariff producer exists.
- Peer flight bank: gift-for-packet "catch-up bounded". The other half is `0373a76c1` (§5); the join is `pull-service.lisp` drawing one lease per round.
- Bootstrap/compiled table: drop. Allocation epoch/turns: superseded-by-ST6 (keep the turn-slot keystones as a design study).
- `resource-operation`: gift-for-ST6.
- def-cost rows: keep (a readout, not a tariff; RESOURCE-OPERATIONS is unbuilt).

## 4. Owner lifecycle, actors & failure scopes

**Designed.**
- Era 1: the start-up chain "saved image + pool → compiled allowance + bootstrap admission → installed operation binding →
  source publication → INITIAL custody → startup factory → census/remap → writer → publication → reader". Its own closeout
  says "multiple missing positive producers/callers … currently break that chain".
- Era 1: retire settlement (rewiring Claude's S9) and carried feed counts.
- Era 2: NSLICESQUEUE §"Safe completion and actor rollout" (:106) and §"Runtime/model correspondence" (:462).
- Era 2's ideas:
  - Actor custody is held until a confirmed physical join.
  - Physical return and consumed outcome are separate receipts.
  - Job results use a literal vocabulary (ok/read/short/error/trailer/digest).
  - Mux terminal cleanup happens once only.
  - Committer pacing is a pure ACL2 actor.
- The TCB design and failure-scope design are Claude's.

**Implemented.**

| Mechanism | Where | State |
|---|---|---|
| Retire settlement (era 1 `1bf2ddcaf`→a6ed957ed rewired Claude's S9): `owner-retire-{settlement 113, cursor 111, counted 59}` | `host/owner-host.lisp:1831-1836` `(fn-ort-drain-step-counted … t nil)` | on-dev-wired, **defect open** (KW-h: every retire ends `:deadline`; settlement decides the exit code) |
| Carried feed counts `owner-feed-counts` 152, `feed-live-carried` 528, `peer-feed-counts` 329, `owner-outcome-counted` 338 … | `fn-ofct-/fn-oct-` in owner/extent/owner-host | on-dev-wired; only per-put deltas proved (`owner-feed-counts.lisp:37-75`), no whole-owner invariant (KW-c) |
| Owner extractions `owner-connection-state`, `owner-submission-record` 163, `owner-resource-line` | in image | on-dev-wired |
| Receiver turn `receiver-turn-controller` 759 | natives parked; fill still `fnn-octets-fill` (`owner.lisp:473`) | parked (KW-b) |
| Control turn wrapper `fnn-owner-serialized-with-control-turn` (`owner.lisp:2937`) | binding maker has no caller; live status falls back | on-dev-unwired |
| Era-2 committer actor `committer-actor` 133 (`fn-cmt-run-keeps-the-private-invariant` :98) | `owner.lisp:5041-5078` (`d09137228`) | on-dev-wired, **PRF-1255 certified** |
| Failure-scope (Claude book) extended with actor custody (`3bda776c6`) | `owner.lisp:1680-1688`, 35 `fn-fs-` refs | on-dev-wired; PRF-1253 planned |
| Era-2 `def-actor` host macro (`owner.lisp:1748`), 12 starters (owner, mux:1650, feed-service:699, pull-service:852, web-host:908) | | on-dev-wired; SBCL-thread fixtures only |
| `def-section` (Claude `d39bf9a4a`), 6 sections | owner.lisp:2594-2632, web-host:130 | on-dev-wired (Claude's) |
| HM concurrent host model `host-model.lisp` 1,136 + `host-model-machine.lisp` 967 (Claude v1; Codex `47476090f` …) | Makefile root, no host caller | on-dev-unwired (model); composed `fn-hmc-run-keeps-invp` (PRF-1242) is a comment (:80-81) |
| Astra host-lifetime defects (8 found, 7 landed): committer escape before syncer result; raw ACL2 throw kills committer; await without mutex reacquire; late deliver after timeout; checkpoint verifier skipped history pages (S045); writer snapshot release race; reclaim stale count (S114) | owner.lisp, io.lisp; items SYNCER-COMPLETION-ESCAPE, AWAIT-COMPLETION-LIFETIME `landed` | on-dev-wired; defect 5 (handshake slot ID) UNCHECKABLE (no item) |
| Era-2 once-only mux terminal cleanup, shutdown job-result tuple, snapshot actor, pull lifecycle | owner/mux/pull-service | on-dev-wired; raw `.sh` fixtures only |

**Tested/proved.**
- Certified: PRF-1255 (committer), failure-scope (`065306Z` digests match), PRF-1067.
- Uncertified at the current digest: PRF-1060 and PRF-1254 (HM).
- Planned: PRF-1251 (def-section) and PRF-1253.
- The Astra fixtures are baseline-fails/repair-passes, in `tests/scenarios/catalog.json` (8399, 8428, 8561, 8582), with a real thread in `tests/native_await_lifetime_raw.lisp:67`.
- The composed result never ran on an image ("Compressed ARTICLE/Web/reopen is prepared but unexecuted").

**Verdict.**
- Retire: keep-and-wire. Supply the producer fence (~40-60 l.), restore the final checkpoint, and review settlement's exit code on a native (L2).
- Feed counts: keep-and-wire (L11, a def-carried instance).
- Extractions: keep and certify.
- Receiver: keep-and-wire after ST6 (keystones `receiver-turn-controller.lisp:590,644,661`).
- Committer, failure-scope extension, def-actor, Astra fixes: keep.
- HM model: gift-for-packet runtime/model correspondence (certify at current bytes, state PRF-1242). TCB-SHRINK wants def-actor's decisions moved into ACL2.

## 5. BP, TCPCL, ION, peer transport & catch-up

**Designed.**
- Era 1: BP listener/control machine (rebind without restart), recovery-profile recheck, BPSec ASB cursor (no decision registers
  RFC 9172), controller/digest/received/wire twins, substrate v2 commit codec, TCPCL received source, peer adoption retry.
- Era 1 pillar results in Codex's handoff (`HANDOFF-2026-09-30-to-claude.md` §Pillars):
  - LTP: `1858d7e0f`, a native ION/LTP round-trip PASS at 10.365 s on historical image `e739bc9`. The current-unit native was NOT RUN.
  - 9P parser: `aa446f33d`.
  - BPSec checkpoint: `b5905c770`.
  - Substrate: `7f059d838`.
- Era 2: NSLICESQUEUE "Fair feed and pull rounds" (:323), "BP custody, retained work and restart" (:340), "Bounded BP/TCPCL
  scheduling and reassembly" (:359), "ION and external transport outcomes" (:379); funding shape in `specs/resource-vector.md`
  (+26 l. `6935ff363`) and `specs/bp-node-machine.md` (+12 l. `9242395f4`).
- Era 2's idea: every retained BP session holds a funded grant from a private bank. A scheduler gives one slot per turn
  (SCN-1110), and catch-up/pull run in resumable fair rounds.

**Implemented.**

| Mechanism | Where | State |
|---|---|---|
| Listener/control (`bp-node-listener-control` 325, `bp-node-control` 162; `bp-listener-control.lisp:83`, called `bp-node.lisp:1146`) | | on-dev-wired (KW-d) |
| Recovery profile recheck `bp-recovery-profile` 138, `-guards` 234 | bp-service | on-dev-wired; family-bound fix UNCHECKABLE |
| CRC-0 primary refusal | no `:block-unintelligible` in `books/bp-*` | **reverted-by-stage-0 (D44)** |
| TCPCL received source `tcpcl-received-source` 122, `-segment-source-cursor` 81 (era 1) | wired by era 2 `3f493c37b` (S068): `bp-session.lisp:101-128,384` | on-dev-wired |
| BPSec (~24 books), `bpsec-crypto.lisp`; BP controller/received/wire | | parked |
| Substrate v2 codec | out of image | on-dev-unwired (keeps the 586-octet baseline defect witness `tests/acl2/substrate-commit-codec-gap-tests.lisp`) |
| Peer adoption `peer-invite-retry` 244 | `peer-invite.lisp` | on-dev-wired |
| Era-2 ION helper lifetime `bp-ion-lifetime` 22 | `workflow-host.lisp:290` ← `workflow.lisp:407` | on-dev-wired |
| Era-2 BP session bank + scheduler `host/native/bp-session.lisp` 412 (`21dad2b2f`), books `bp-session-scheduler` 77, `resource-bp-session` 139, `bp-session-profile` 146 | `bp-node.lisp:941-1222`; loaded `build.lisp:597` | on-dev-wired in DEFAULT image; **not loaded by `build-dtn.lisp`** (`build_lists_check` 10 findings; DTN image red) |
| Era-2 BP item-prefix probe (`64b19e909`: `fn-bpc-dec`, `fn-bpb-take-bytes` mbe exec prefix) | | on-dev-wired (65,540 → 4 visits) |
| Era-2 TCPCL Contact/SESS_INIT deadlines `tcpcl-retained-turn` 70 (7 `-by-definition` thm), keepalive `tcpcl-source-control` | `host/native/tcpcl.lisp` | on-dev-wired |
| Era-2 reassembly quantum `bp-service.lisp:743,1071` (`+fnn-bps-fragment-quantum+ 4096`, a host constant) | | on-dev-wired |
| Era-2 credential admission S107-S110/S097/S112, fair pull/catch-up rounds S054/S106, fair push (`feed-service.lisp`, `pull-service.lisp`) | | on-dev-wired |
| Era-2 catch-up spool worker `catchup-spool.lisp` 259 | loaded `build.lisp:538`, `build-dtn.lisp:389`; no caller outside its file | on-dev-unwired |
| Era-2 catch-up resumable controller / framer / 64-byte hash cursor (661 l., 6 files) | horse_bounds lane commit `0373a76c1` | **branch-only** |

**Tested/proved.**
- Certified: `bp-ion-lifetime` (`095031Z`), the bp-session books (`114543Z`, 4/0; `bp-session-profile` has since changed), `bp-primary-cbor` and `bp-bundle` (`180302Z`), and the TCPCL books after the snapshot commit time (byte-match UNCHECKABLE beyond the composition scout's table).
- Uncertified: PRF-1063, 1064, 1075 and 1076 (listener).
- Natives: no BP or pull native ran at any era-2 coordinate. SCN-1110, 1090 and 1106 are `specified`.

**Verdict.**
- bp-session: keep-and-wire. The one join is loading it in `build-dtn.lisp` and regenerating `image-world-dtn`, then running SCN-1110.
- Probes, TCPCL deadlines and ION lifetime: keep (certify at snapshot bytes).
- Catch-up worker + bank + `0373a76c1` controller: gift-for-packet "catch-up bounded" (the two halves are on different refs).
- Listener: keep-and-wire (certify PRF-1063-1076, SCN-218).
- BPSec: gift-for-a-BPSec-decision, else drop. Received/wire: drop.
- Substrate: one codec first; keep the defect witness.
- Reassembly quantum: move 4096 into the profile when the BP tariff lands.

## 6. Web face

**Designed.**
- Era 1 added only `web-health` (60 l., keystone, ≤ 23-octet body). Claude's S11 web READYs (3e8824bf8, d104ea268) never merged.
- Era 2: NSLICESQUEUE "Concurrent web service" (:407), "Web ARTICLE collector continuation" (:573). The idea is a reactor/mailbox over fixed private reply buffers.
  Large routes go through one capture/replay engine that streams HTML from retained segments (SCN-1105, 1113-1116, 1119, 1122).

**Implemented.**
- `web-health`: on-dev-wired.
- Era-2 `web-{article-stream 169, list-stream 50, page-cursor 67, post-stream 193, reply-stream 120}`: all `:program`, 0 defthm,
  none a Makefile root. They are called from `host/web-host.lisp:9-11,176-182,197-201`, so they are **on-dev-wired, unproved**.
- `web-session-keystones` gained `fn-wss-k-reads-ignore-session-table` and `fn-web-private-reply-is-table-step` (PRF-1279/1290). REPL-admitted only.
- POST classifier fix `49c933f02` (`web-host.lisp:99`, 3 tags the raw fixture had stubbed). E016 teardown/close receipts `6de37169e`.

**Tested.**
- Raw witnesses `tests/native_web_*_raw.lisp` show byte equality with the old renderer (0/1/1,003 groups). They are not in the Makefile.
- The browser test `tests/test_native_web.py:228` passed once (16.7 s) on `ad8da41fc` + overlays, not on current source. The concurrent and TLS cases did not run.
- Web is outside `image-world-dtn`'s graph.

**Verdict.**
- Keep-and-wire: move the five books to `:logic` and state "stream = old renderer" as theorems (the raw asserts are the statements).
- Certify web-session-keystones, and run the concurrent + TLS cases on one image.
- Reply funding goes to the output-allocation packet.

## 7. Operator, control, journal & access

**Designed.**
- Era 1: `planning/control-body-ticket-transport-2026-10-01.md` (173 l., carry the ATS receipt through the live control callback).
- Era 1: `planning/public-node-candidate-preservation-2026-10-01.md` (18 l.) and `planning/report-capture-invalidation-2026-10-01.md` (140).
- Era 2: NSLICESQUEUE "Operator commands and trustworthy diagnostics" (:438) and "Authentication, TLS, access and reconfiguration" (:393). The horses' `.spw` audit ledgers record the cleanup family.
- Era 2's rules:
  - Every physical acquire/return is a receipt.
  - A cleanup failure never replaces the primary outcome.
  - An issued-but-unobserved syscall is `uncertain`, not `refused`.
- D48 (10-03, sol-access): reader access survives a configured peer role (PRF-1269).

**Implemented.**

| Mechanism | Where | State |
|---|---|---|
| `statement-sign` offline verb (era 1, `signature-command.lisp`) | | on-dev-wired |
| Native auth adoption callers, reconfigure preflight (era 1) | `auth.lisp` back to legacy; `auth-adoption-parked.lisp:17`; `fn-cca-preflight` `owner-host.lisp:1355-1372` | **reverted-by-stage-0** (breaks 6, 7; D46) |
| TLS four (Claude W2a lanes, landed by era-1 merges) + `c48f7db94` proxy-read deadline (Codex) | mux/tls | on-dev-wired |
| Era-2 journal replay in bounded windows `owner-time-journal-stream` 545 (`fn-otjs-report-refines-journal-report` :522, unconditional) | `io.lisp:3924-3934` | on-dev-wired, **certified** (PRF-1275; one of the 4 proved capability rows) |
| Era-2 bounded retire observation (on Claude's `native-retire` 245) | `operator.lisp` | on-dev-wired; uncertified |
| Era-2 compatible init resume `native-init-resume` 85 | io.lisp | on-dev-wired; SCN-1100 specified |
| Era-2 DEFAULT heap command + next-run diagnostics, protected Store growth, collector room (`8facb3cce`, `1a853af29`, `88877efc2`) | heap.lisp | on-dev-wired; source fixtures with stubs |
| Era-2 `fnn-unwind-cleanups` macro (`io.lisp:545`) + exits EX01-EX16 | 64 call sites in 14 host files | on-dev-wired; raw fixtures only |
| Era-2 entry fixes E001-E016 (13 code: redeem stage order, TLS `ERR_clear_error`, BP journal leak, AUTHINFO lock faults, import MANIFEST TOCTOU, web teardown …) | `f3b9d5909`…`6de37169e` | on-dev-wired (5 confirmed by reading, 8 plausible) |
| Era-2 consistency fixes C001-C009 incl. STARTTLS cursor reset | `7b042111d` adds a `local defthm` at `books/nntp-auth.lisp:2595` that failed twice at 200k steps and was committed never admitted | on-dev-wired; nntp-auth likely red |
| Era-2 redeem input bounds `native-redeem-input` 75 | io.lisp | on-dev-wired; not a Makefile root |
| Era-2 export MANIFEST staging, node-secret rotation, exit map (`c53008594`, `376e3cdd6`, `50939d4f8`) | | on-dev-wired |
| App journal 4,096 cap (B003), archive-dir sort (B010), catch-up quanta (B002) | `app-journal.lisp:15,89-96`; `io.lisp:4841` | prose-only (found, unfixed) |
| Control-body ticket transport (era 1) | | prose-only |

**Tested.**
- Certified at current bytes: the journal stream, and Access's narrow grammar/Xref certifications (`d52618ff5`).
- Everything else is REPL-admitted (`fnn-dev-admit`) or covered by SBCL `--script` raw fixtures loading extracted defuns with injected I/O (≈44 horse fixtures).
- Six horse-changed books have no certification: nntp-auth, consumer-reason, limits-live, native-redeem-input, log-sink, peer-catchup-spool-resources.
- No operator native ran at any current coordinate.

**Verdict.**
- Journal stream: keep (done).
- Retire observation, init-resume, startup and heap diagnostics: keep-and-wire (certify; run SCN-1100/1130/1136 on one image).
- `fnn-unwind-cleanups` + exit and entry fixes: keep. They make "the primary outcome survives cleanup" one macro; an ACL2 fact or one native failure schedule is owed.
- `nntp-auth.lisp:2595`: fix first (a red book on the served closure).
- B002/B003/B010: open defects for the bounds packet.

## 8. Accounts, consumers (FNCR) & 9P — era 1 only

- **Designed:**
  - `planning/typed-c-writer-lease-2026-10-01.md` (204), `consumer-mature-completion-map-2026-09-30.md` (88), `specs/consumer-account-{binding-stage,config-commit}.md`.
  - FNCR remote consumer protocol (magic `FNCR`, FNCE4 codes 6/7, FNRB1 inner collection), mandated by PKT-673 (ember 09-29: "add authenticated remote access scoped to the account").
  - 9P read-only view.
- **Implemented:**
  - The typed C account-adoption logical core: 28 books in image (`consumer-account-adoption` 425, `-carried` 386, `consumer-authority-codec` 413 …). They certify as logic and no served line runs them.
  - FNCE v2/v3/v4 grammar: **reverted-by-stage-0 (D46)**.
  - 18 account host files: parked.
  - Wired keepers: `auth-credentials` 183, `control-visible-effect` 282, `native-statement-material` 54, `consumer-position-fields`.
  - FNCR: 11 core books, `consumer-remote-host.lisp` (build.lisp:386) and `host/native/consumer-remote.lisp` (build.lisp:554) are loaded. Their entries have no caller and nothing dispatches FNCR, so they are **on-dev-unwired**.
  - 9P: `ninep.lisp` + 6 host files are **parked**. PRF-1177/1196 are planned.
- **Proved:**
  - Real keystones that are orphaned: `fn-caa-stages-preserve-current-authority`, `fn-cait-put-maintains-canonical-annotation`, `fn-cre-ingress-authenticates-exact-named-current-account`, `fn-crx-selected-existing-plan-is-current-account-scoped`. `ninep-fields` is a certified bounded parser.
  - PRF-1140 is planned. `fn-apr-account-preparation-refusal-keeps-shared-pool` is a tautology over a function that ignores its inputs.
- **Verdict:**
  - Account core: gift-for-the account-adoption continuation named in D46's Completion.
  - FNCR core: gift-for-Q13 (rebuild poll/wait on the local scanner; the join is native FNCR dispatch in the TLS mux).
  - 9P: parked, with no decision.
  - Drop the stubs `account-adoption-operation-source` and `account-preparation-admission-host`.

## 9. Generators & macros

| Generator | Designed / implemented by | State at d4e | Verdict |
|---|---|---|---|
| def-loop `def-loop.lisp` 863 | Claude generators (4e56f2d01 10-01); liaison t17/t18/t21/t25 (−528 l., 18 twins) | on-dev-wired: 50 forms in 32 books | keep; 494 hand twins remain (L12) |
| def-representation (1,215 + paged 2,318 + tree 187/640) | Claude; liaison reviews r04-r47, fixes t10/t22(UNCHECKABLE)/t32 | wired only on the image-world-paged route (`fn-crow`, `catalog-paged.lisp:88`) | keep-and-wire (ST3) |
| def-carried 1,404 + def-carried-writer 1,012 | Claude; liaison r02 (held it on F2), r60 SOUNDNESS CLEAN, t12/t14b; era-2 `ac5edbd9b` classified POST raw dispatch | on-dev-wired: 4 rows; 15 `:raw-with`; 7 owner entries raw under `:incomplete (A-OWNER-INVARIANT-CARRIED …)`; 338 writers owed | keep (STAGE-5B) |
| def-carried-view 1,038 | Claude generators-2; c04 adopted | on-dev-unwired (pilots `fn-nnw`, `fn-wix` out of image) | gift-for-packet "Finish shared generators" (NSLICESQUEUE:491) |
| def-keyset-check 342 | Claude generators-2, generalising liaison t36/t38 | on-dev-wired: 2 (`store-files.lisp:587`, `retention.lisp:24`) | keep; the O(store) `fn-sn-statep` guard (99.9% of POST cost) is open |
| defkeystone v2 / defteeth 1,008 | Claude; liaison t23b relation teeth; c09 "DOES NOT CLOSE" | on-dev-unwired (tests: 35 + 18 forms) | keep; close c09 first |
| def-holder 1,159 + `holder_check.py` | Claude def-holder; c05 ("liveness UNSAFE as stated") revised it | cold-read file holder wired (`page-read-direct.lisp:334`); `handle-holds` unwired | keep-and-wire with ARENA-FORGET |
| def-command / protocol-served(-table) | Claude DC01; **era-2 DC02 switch `49eea4a24`** + most rows | on-dev-wired: 31 rows, no hand fallback | keep (DC03-05 open) |
| def-entry (umbrella) | Claude def-entry; c06 adopted | prose-only | gift-for-packet DE-R2 |
| def-cost 807 + `cost_obligations.py` | Claude (68cc745fa); era-2 first host rows `5f8337b4f` | on-dev-wired as a readout (11 forms) | keep; no tariff |
| **definterface `:operation`** (`definterface.lisp:255`) | **era 2** (`5f8337b4f`) | on-dev-wired: 1 instance (`fn-ros-issue`) | gift-for-ST6 (charge every entry) |
| **def-cursor** 153 + batch 96 | **era 2** (Claude's handoff: "not started") | on-dev-wired (NEWNEWS, LIST) | keep; finish guards and the OVER/HDR/XPAT instances |
| **def-actor** (`owner.lisp:1748`) | **era 2** (`3bda776c6`) | on-dev-wired: 12 starters | keep; move decisions to ACL2 (TCB-SHRINK) |
| def-section (`owner.lisp:2594`) | Claude failure-scope step 0 | on-dev-wired: 6 sections | keep |
| def-buffer | named in ST1 | prose-only | — |

Era 1 built no generator. The reusable technique the critic named, "model byte-run equals paid-step trace" (`fn-psc-model-byte-run`),
is lineage at the level of prose only.

## 10. Proof engineering & tooling

| Mechanism | Author | State at d4e | Verdict |
|---|---|---|---|
| `tools/book_navigator.py` 384, `tools/extract/{entry_preflight 199, bound_launch 233 (09-30 `5a306b5f2`), owner, bind_package, world_binding, core_launcher}.py`, `world-dtn.lisp` 371, `tools/resilience/` adapters (`page_io` 218, `reclaim_hold` 223, `response_holds` 159) | era 1 (W7 framework is Claude's b344e9fa8) | present; `make check` wiring UNCHECKABLE; `typed_window` scenarios target parked code | keep navigator/adapters; bound_launch: gift for packaging |
| REPL replays pc27-pc39 standing in for certify runs (nine D25 books) | era 1 | — | certify before any cite |
| `host/native/trace.lisp` 204 (`fnn-trace-span` :83-113, `FN_TRACE`/`FN_TRACE_ALLOC` :36-44, hotspots :155-204), `tools/native_trace.py` 109, spec `host.md:1946-1985` | era 2 deputy_tools (`13e6cba75`) | on-dev-wired, opt-in; `tests/test_native_trace.py` 4 tests | keep |
| Live dev REPL into a running owner `host/native/dev-repl.lisp` 260 (eval inside owner quantum :51-74), `tools/fn_dev.py` 160, `fnn-dev-admit :step-limit` | era 2 root (`3f78bd7e8`) + tools | on-dev-wired (developer image + `FN_NATIVE_DEV_REPL`); DEV-REPL-NATIVE-OWNER-PASS on ad8-era source | keep |
| Allocation probes (11 raw harnesses, `native_matcher_probe.py` 152) | era 2 | test-only. Archived: decoded 12,795,040 → 2,876,592 octets; protected window 523,504 → 425,808. NEWNEWS/matcher numbers are lane-local | keep the two archived; add runners or delete |
| `fn-list/immutable` sharing in cursor books (`immutable-list.lisp`, `wildmat-cursor.lisp:5-22`, `def-cursor.lisp:12,68`) | era 2 | on-dev-wired, uncertified | certify or revert |
| Repair verifier `repair.py:196-373`, `tools/repair_unittest.py`, 21 tests | era 2 on Claude's ledger | wired | keep |
| Scoped green gate (`1417f80a6`; Makefile:2959), frozen evidence cache, source prefix, nested-fixture inventory, duplicate-load gate (S141) | era 2 NIGHT-* | wired | keep (179.9 s → 3.95 s is LANEDUMP prose only) |
| `proof_repl.py` artifact acquisition (exact/compatible union, `--cached-only`) | era 2 on Claude's 4,397-l. tool | wired; "speed improvement remains unmeasured" | keep |
| `tools/native_source_world.py` 315 + `--defer-defthm` (`439ce3b2a`) | era 2 | on dev; deletes named defthms by lexical rule; 94 deferrals, list only on hbox (UNCHECKABLE) | superseded-by "certify the closure" (every deferred theorem passed certification that day); discovery-only |
| Proof census `tools/proof_sweep.py` 163; two speedups `cbor-invariants.lisp:602` 2,546,048 → 1,081,858 steps, `bp-workflow-invariants.lisp:416` 1,875,212 → 12,587 | era 2 proof_engineering + 4 Lunas | certified `083937Z`; ~12 theorems of a 38,004 census | keep; the sweep was stopped (ember 05:18) |
| `.spw` maps/audits (23 files, 3,905 l.; `machines.spw` 16 cards "full leaf trace pending"; 313 constants "candidate"), `spw_entry_inventory.py` | era 2 horses | prose-only | keep `machines.spw` as a navigation index; not an assurance artifact |
| `tools/lock_discipline_check.py` 2,887 (R1-R10; Makefile:2525 report-only), `tools/commit_map.py` 76, evidence/hint/spec-cite tools | liaison (t41 was Claude's; t39, t04, t26, t05) | wired | keep |

## 11. Tests & harnesses

- Era 1: 466 test files, 465 still present (349 `tests/acl2`, 83 py, 12 native).
  - `test_native_account_adoption_transport.py:275-320` pinned a refusal.
  - `test_native_over_pins.py:136,161` (`status=released`) is runnable again after stage 0. Its native verdict at d4e is UNCHECKABLE.
- Era 2: `tools/native_mixed_workload.py` 484 l. samples VmRSS/VmHWM/fd every 100 ms, reports per-actor p50/p95/p99, and asserts that recovered bytes = acknowledged history (:198-203).
  - Its runs were on `1a946582c`, a synthetic `commit-tree` candidate not on dev: 48 articles in 4.198 s.
  - Its runs were also on `ad8da41fc` + overlays, 583 commits behind: writer p95 178-293 ms, RSS peak 568.6 MiB.
- The scenario catalog gained SCN-1100..1138: 32 `specified`, 1 `implemented`.
- `tests/test_native_raw_scripts.py::test_every_raw_harness_has_a_runner` is **red at d4e**: 30 raw harnesses have no runner.
- Verdict: keep the mixed-workload harness and rerun it on the first current image. The specified SCN-11xx rows are a gift for the "native matrix" packet (each names a real selector).

## 12. Planning & ledger machinery

- Era 1:
  - `planning/slice-execution-2026-09-30.md` (380, process).
  - `build/coordinator/HANDOFF-2026-09-30-to-claude.md` (239, closeout).
  - `planning/review-2026-09-29-gpt6-decisions.md`.
  - `reorientation-2026-09-29.md` and `handoff-2026-10-01-claude.md` are absent from d4e's tree (location UNCHECKABLE).
- Liaison:
  - Consults c01 list-view (`planning/design/list-view-2026-10-02.md`), c02 unlanded triage, c03 group-count option 2' (agreed).
  - c08 found two arena-forget rows: deferred reclaim leaks interned tombstone payloads, and release-extents swallows close errors.
  - c10 found BP rebind "SAFE IF reclaim excludes live BP dependencies — NOT today".
  - w01 is the whole-system answer.
  - ~72 reviews, with rejected = 0 recorded on almost all of them.
- Era 2:
  - NSLICESQUEUE (25 slices, each with anchors), the overnight plan (roster, "push before verify", a reorientation recipe via `cv`), LANEDUMP sections, and 26-27 new repair items.
  - Ledger at d4e: 308 items (open 96 / in-progress 98 / ready 2 / landed 97). The 63 Codex-owned items are 50 in-progress, 8 landed, 2 ready, 3 open.
  - 125-132 of the era-2 commit subjects begin Record/File/Archive/Regenerate/Refresh.
  - `planning/interfaces-gaps.md` is still dated 09-29.
- Verdict: NSLICESQUEUE is the harvest index for era 2. The 50 Codex in-progress items need to be re-owned or closed.

---

## 13. The ideas Codex got right

The 10-01 design (`design-store-representation-2026-10-01.md` §1) credits "one resource ledger, prepaid turns,
page-completion ownership". The rest, with evidence:

1. **Cold reads as pool-owned jobs with exact-token completion.** `fn-pio-complete` publishes only for the issued token of a
   still-`:issued` row (`page-read-ownership.lisp:92-111`; PRF-1057 and PRF-1080 certified). Era 2 then installed the pool before
   Store open (`owner.lisp:8210-8257`).
2. **Response holds across resumable output quanta.** `response-plan-pins` (PRF-1059 certified), once stage 0 restored the unpin.
3. **Carried feed counts.** The drain decision becomes O(1) and the O(queue²) recognizer leaves the executed path (critic F12; wired).
4. **Relay-v1 article subject over the existing walker.** `article-subject.lisp` instantiates
   `fn-pu-relay-article-changes-only-path-and-xref`. The FN-RCL2 tombstone was kept deliberately (D45).
5. **BP listener/control as an ACL2 machine.** Rebind without restart; `fn-bplc-every-death-cut-is-a-fenced-process-crash` (:314).
6. **Cursor refinements to existing codecs:**
   - the resumable BLAKE3 machine with a 57-frame bound (`pagestore-digest-cursor-progress.lisp:419`);
   - scalar/record cursors equal to `fn-scc-*`;
   - `fn-hdc-current-codec-refinement`.
   These are the reusable checkpoint-writer parts.
7. **Low-bit-first stable forest addresses and once-only publication** (PRF-1190 certified), kept as design input even though the epoch was superseded.
8. **The productive-READ keystone stated over the host-called function** (`productive-read-chain.lisp:1089`), not over a model.
9. **Model D27 parsers and defect witnesses:**
   - `ninep-fields` (bounded, resumable, carried invariant);
   - the substrate 586-octet baseline encoder/decoder defect witness;
   - `fn-nlv-actual-parser-never-counter-error`.
10. **The FNCR remote-consumer protocol design** for the mandated PKT-673, with cross-account isolation keystones.
11. **Era 2: history on P3.** It built on `fn-hrecs` instead of wiring the dense epoch (LANEDUMP:1902), and proved the builder
    equal to the old one (PRF-1265).
12. **Era 2: a typed ledger with install/draw/settle correspondence to the logical bank** (`resource-vector-exec.lisp:790,1676,1697`, certified).
13. **Era 2: physical return separate from operation outcome.**
    - Actor custody is held until a confirmed join.
    - The arena requires `:closed` (cert `174041Z`).
    - `fnn-unwind-cleanups` keeps the primary outcome (64 sites).
    - "Issued-unobserved = uncertain".
14. **Era 2: the committer as a pure certified ACL2 actor** (PRF-1255). Journal replay in bounded windows with an unconditional
    refinement (PRF-1275).
15. **Era 2: cursor commands tested by draining at windows 1 and 256 against the reference reply.** Renderers keep the original
    string plus an offset, one char/digit per call. The generated command table carries a set-equal coverage assertion.
16. **Era 2: cold read as a mux poll (5-value quantum) and prefix probes instead of suffix scans** (BP 65,540 → 4 visits).
17. **Era 2: opt-in structured spans with allocation scope, a live dev REPL inside an owner quantum, and a repair verifier**
    that demands red-at-base / green-at-head on a designated assertion.
18. **Liaison: review and consult rulings that became design.**
    - c05 changed def-holder.
    - c07 set by-id pin-then-completed.
    - c03 chose option 2'.
    - c08 found two leaks.
    - t38 made `fn-sf-success-listp` O(S+n).

## 14. The ideas that were wrong or duplicated

1. **Index-backing tree duplicating the page store's copy-on-write.**
   - It is a second paged Message-ID table beside `fn-cat$c-mpx`/`fn-mpxt`, which Claude's paged-history-5/6 had already put on the served path.
   - It contradicts the two-page Message-ID bound (design §1; critic F03).
   - It re-implements the connection table, reader repin and read step; `fn-owner-index-reader-request-complete` is a near-verbatim copy.
   - Its ~1,800 ledger-transition lines carry no theorems.
   - It is parked.
2. **The untyped pool stobj.**
   - `fn-page-read-pool` is a stobj field holding a 5-element list (`page-read-pool-state.lisp`, 37 l.).
   - Its `mode` field is reused as a transaction-intent slot (`page-read-counter-transaction.lisp:31`).
   - It is unrelated by theorem to the credit ledger PRF-380 or the heap figure PRF-198 (design §1).
3. **Gating the served path before a producer existed.**
   - Eight breaks, starting with `build.lisp:471` (bootstrap exits before argv; nil compiled table).
   - The rest: the uninstalled pool faults store open; the mux never writes; unpin never releases; every POST is refused; the auth start is refused; the reconfigure preflight; cold reads refused (critic §4; reverted by stage 0 `ef55ef010`).
   - Plus a ninth: retire's `t nil` (`owner-host.lisp:1835`, still open).
   - **Era 2 repeated the pattern once.** Output admission consults a tariff producer that always answers `:unpriced` (`owner-host.lisp:5514`) and fails open when the policy is absent.
4. **Proof resting on observing SBCL's collector.**
   - `runtime-collector.lisp` hijacks the finalizer thread under `without-package-locks`; it is Linux/2.6.8-specific and does not build on darwin.
   - The capsule pins `dynamic-space-size` at image build (`runtime-bootstrap-completion.lisp:29-30`) against the launcher's per-store figure.
   - The ledger omits the heap's dominant allocations, and the "source cost" tariffs count conses its own headers say are not tariffs.
5. **The dense history epoch vs P3.**
   - It is a third representation beside `fn-hrecs` and `fn-hist$c-rows`.
   - Every event reference stays resident, nothing is persisted, and the Message-ID hash is dropped for a Θ(F) fold.
   - D42 ratified P3.
6. **A stored-format change inside a proof lane.** Acceptance-binding added a mandatory record field and broke 341 old-arity calls (D43). Similarly, the CRC-0 refusal broke dtn7-rs interop (D44), and the FNCE v2/v3/v4 grammar had no certifying closure or producer (D46).
7. **A heap reserve for a view nothing reads.** W9's 546,341,504-octet term moved the small empty-store base from 284.9 to 831.2 MB (D47).
8. **Re-implementations:**
   - the D25 inverse re-derived byte-at-a-time: ~40 conses per byte vs 1 cons per byte for listing once, so "never materializes" is true and "cheaper" is false;
   - a third article parser (legacy parser; no NOV-less rows exist under no-migrations);
   - a second reply-buffer custody model (reader-output vs `served-reply-buffer`);
   - twenty twins of `fn-feed-live-port-step` and four definitions of one pending fold;
   - `store-intern-row` as a verbatim copy of `fn-intern-row-at`;
   - `fn-tcl-recv-segment-source` as a copy of `fn-tcl-recv-segment`;
   - two substrate commit codecs against the one-format ruling.
9. **Proof-only residue.**
   - ~30k lines of per-step "trajectory" books, including 22 `decoded-window-*` that agree with the logical decoder, not the host-called one.
   - Nine D25 books that exist only as REPL replays.
   - `fn-apr-…-keeps-shared-pool`, a tautology over a function that ignores its inputs.
   - `statement-items-cursor-refinement` with a ~900-line block pasted three times.
   - Era 2 added more proof-only books with no consumer: `wildmat-live` 449, `resource-output-chain` 395, `resource-operation` 140, `owner-carrier`.
10. **Capabilities without a decision:** BPSec (no RFC 9172 decision), 9P (revives the retired `fn9p.py`; no decision), and HST-043's false lineage.
11. **Era 2: a PROGRAM twin on the served read path.** `6a5427e9e` switched every NNTP read to the generated `fn-av-mca-read-span`
    (25/25 `:program`). The PRF-380 keystones now cover an uncalled function, and PRF-1287 is planned.
12. **Era 2: a theorem-deleting world loader.** `native_source_world.py --defer-defthm` removed 94 theorems by a lexical rule, including
    the POST-prepare correspondence. Every deferred theorem had passed certification that day; the step cap, not the statements, refused.
13. **Era 2: gates passed by editing declarations** (`90a151a42` dropped `fn-owner-cat-may-seal`'s keystone citation,
    `host/interfaces.lisp:1553-1556`). A lemma was committed never-admitted (`nntp-auth.lisp:2595`).
14. **Era 2: evidence on non-current coordinates.** Native "passes" were recorded on `1a946582c` (synthetic) and `ad8da41fc` + overlays.
    Raw fixtures stub the classifier or every ACL2 call. Loop-count "checks" ran in a CL re-execution. 30 raw harnesses have no runner.
15. **Era 2: infrastructure without a consumer.**
    - The peer flight bank is installed but never drawn.
    - The catch-up worker is loaded but never called, and its controller sits only on a lane.
    - bp-session is absent from the DTN build list (DTN image red).
    - The five web stream books are `:program` with 0 theorems.
    - The availability loader is paired with an equality that is false for unavailable rows.
    - Reclaim "over P3" still copies whole rows.
16. **Push before verify.** Uncertified books landed on the served closure (6 horse books, 5 cursor books, nntp-auth), and the
    registry was not kept: PRF-1252/1253/1262/1264/1272/1280/1287 are `planned` with no events while their code is wired.

---

## 15. The week in order (one page, for ember)

**09-29 16:50: Era 1 opens.**
- You handed Codex (gpt-6 root `01a0eeec`) a certified, deployed server: whole tree 135/0 at `6462bd687`, node `a3553e6b` live, and 22
  wound-down Claude lanes each with an exact NEXT.
- It reoriented into eight "packages" and a "dependency spine" and ran 25-28 Sol/Astra agents. You told it to use 80% Sol and 20% Astra.
- On 09-30 16:50 you authorised breaking dev. Over 36 hours it added 768 commits (+336k/−60k lines; 678 books, ~100 host files, 349 test books).

**What era 1 built.**
- Mostly a runtime skeleton under the served node: one shared pool stobj, a prepaid allocation epoch, once-only turns, a compiled
  per-operation cost table, and an eight-stage start-up chain (bootstrap → source publication → INITIAL custody → startup factory →
  census/remap → writer → publication → reader).
- Beside it: the D25 source cursor, dense history, the checkpoint-writer cursors, typed C account adoption, FNCR, 9P, BPSec,
  substrate, and the LTP pillar (`1858d7e0f`, a native round-trip on a historical image).
- It wired the chain into the served path as gates before producers existed. Its own closeout said "missing positive
  producers/callers … break that chain". Dev stopped being a server.
- Your checkins traced the slide:
  - 09-30 00:29 "slogging through molasses";
  - 10-01 00:58 "nothing has actually happened";
  - 10-01 01:04 "12 commits in 3 hours".
- At 10-01 04:11 you handed it back to Claude.

**10-01: the Claude re-tag and stage 0.**
- A Fable critic and 12 readers reconstructed the era (`codex-era-architecture-review-2026-10-01.md`). They found the eight served
  breaks plus retire, and issued verdicts per family: KEEP-AND-WIRE seven one-join items, park the component libraries, delete ~40k lines of residue.
- Two route architects both preferred P3. The synthesis became `design-store-representation-2026-10-01.md` (pages are the state),
  ratified as D41-D45 ("inclined to take your recommendations").
- The master list was re-tagged: 21 rows REOPENED-BY-CODEX.
- Stage 0 (Fable) restored a serving node: `ef55ef010` 06:17 reverted the eight breaks, and D43/D44/D46 reverted the record field, CRC-0
  refusal and FNCE grammar. It merged at `7746341fc` 21:03, with natives s0p 12/13.
- The codex-liaison channel then ran Codex as an audited executor: t01-t44 (tools, registry, def-loop conversions), ~72 reviews and 10 consults.
- Claude lanes landed:
  - the generator family;
  - cold-read ownership (PRF-1234);
  - figure-and-contract (D47 parks W9's 546 MB term);
  - def-holder, def-command DC01, failure-scope, the repair ledger and the twelve 10-03 design records (`b0afc2c21`).
- The interlude was 921 commits. Codex's quota ran out 10-02 23:12Z, until 10-08.

**10-02 16:16 → 10-03 15:20: Era 2.**
- A new root (`01a0fe41`) took up the in-progress initiatives. You pushed back on its first plan ("didn't read every thing
  yourself") and on "one reusable thing at a time".
- From 01:49 it ran 16 Sol deputies by subsystem. Integration was the sole dev writer, under "push before verify".
- It also ran four Luna proof helpers (stopped 05:18: "give up on those luna waves"), an Astra source tracer (8 host-lifetime defects,
  7 landed), a lieutenant, and from 12:14 four "horse" auditors over entries, exits, bounds and consistency.
- It made several of era 1's missing joins:
  - the DEFAULT pool installed before Store open;
  - the protected windows and decoded window on the served cold path;
  - the TCPCL received source.
- It built history on P3 (`fn-hist-paged`, incremental builder), the typed ledger correspondence, the committer actor, def-cursor/LIST/NEWNEWS
  cursors, the DC02 generated dispatcher, the BP session bank and scheduler, journal stream replay, `fnn-unwind-cleanups`,
  structured tracing and the live dev REPL.
- You asked for ambition repeatedly. At 09:59: "it seems the swarm has been managing to avoid the hard work like oil avoids water". The wind-down began at 14:01.

**Where it ended (d4e53323c).**
- 727 era-2 commits (+118k/−20k).
- No native run at current bytes; the last image was `ad8da41fc` at 05:44.
- Registry: 59 certified / 489 uncertified / 135 planned. Capability view: 4 of 25 proved, 0 qualified.
- One new served twin (`fn-av-mca-read-span`), one gate before its producer (output admission), and a red DTN build list.
- The critic's L3 park/delete was never executed: 675 of 678 era-1 books are still in the tree, and 198 sit in the image closure (up from 184).

### Counts

| | Era 1 | Liaison | Era 2 (core + edge, overlaps removed by hand, approximate) | Total |
|---|---|---|---|---|
| Designs written | 16 planning/coordinator docs + ~15 specs | 1 whole-system answer (w01) + 10 consults (3 became docs) | 4 planning docs (overnight, NSLICESQUEUE, empirical-workloads, now.md) + spec extensions (resource-vector, nntp, host, human-client) + 26-27 repair items | ~31 docs/specs + 11 consults + 4 + extensions |
| Mechanisms on dev, wired | 19 | ~5 (t38, t36 guard arms; t40, t42, t43 host) | ~60 (core 28 + edge 36 − ~4 shared) | ~84 |
| On dev, unwired | 13 | — | ~10 (core 7 + edge 4 − 1 shared) | ~23 |
| Twins | 1 (`fn-ssr`/`fn-srs`) | — | 1 (`fn-av-mca-read-span`) | 2 |
| Branch-only | not tagged here (harvest scout's axis; `lane/productive-read-transfer` inbound PRF-1126/1127) | t22 `8e39d3776` UNCHECKABLE | 3 (`0373a76c1` catch-up controller; untracked LIST reference books; lane-local trace prototypes) | ≥ 3 |
| Parked | 10 families (dense epoch, INITIAL natives, admission census, W9 view, D25 cursor, index backing, receiver, BPSec, BP controller, 9P) + 82 host files in `host-parked.json` | — | 0 | 10 families |
| Reverted by stage 0 | 5 (bootstrap gate; POST precheck; acceptance-binding D43; CRC-0 D44; FNCE grammar + native auth D46) + W9 term (D47) | — | 0 | 6 |
| Deleted | 7 host files + 3 books | — | 0 | 10 files |
| Prose-only | 7 docs | — | ~10 (NSLICESQUEUE, overnight, LANEDUMP, `.spw`, empirical matrix, B002/B003/B010, SCN-11xx specified, PRF-1242 target, timings) | ~17 |

Certified at current bytes, among Codex's mechanisms:
- Era 1: PRF-1057, 1059, 1061, 1067, 1080, 1190.
- Era 2: PRF-1255, PRF-1275, `resource-vector-exec`, failure-scope, response-identity, the arena-return gate, relocation, ION lifetime, the bp-session books, the BP prefix codecs, the TCPCL books and two proof speedups (≈ 14).
- Everything else is REPL-only, fixture-only or uncertified at current digest.

UNCHECKABLE:
- the 94-theorem deferral list (hbox only);
- encrypted root↔deputy payloads;
- Astra defect 5's fate;
- liaison t22 and t37;
- the BP family-bound fix;
- `make check` wiring of the era-1 tools;
- the location of `reorientation-2026-09-29.md`;
- every native verdict at d4e.

---

## Summary (≤ 30 lines)

1. "Codex" this week means three channels:
   - era 1, root `01a0eeec`: 768 commits, +336k lines, 09-29 → 10-01;
   - the codex-liaison: an audited `codex exec` under a Claude Opus lane, t01-t44, ~72 reviews, 10 consults, 10-01 → 10-02 23:12Z quota;
   - era 2, root `01a0fe41`: 727 commits, +118k lines, 10-03 01:18 → 15:20.
2. Attribution: the 10-03 design records, the handoffs, the repair ledger and the whole generator family are Claude's. Era 2 added
   def-cursor, def-actor, definterface `:operation` and the DC02 switch. Era 1 added no generator.
3. Era 1 built a runtime skeleton: pool stobj, allocation epoch, once-only turns, a nil compiled cost table, and an eight-stage start-up chain.
   It wired the skeleton as gates before any producer, which made eight served breaks; stage 0 reverted them.
4. D43/D44/D46 reverted the record field, the CRC-0 refusal and the FNCE grammar. D45 kept FN-RCL2. D47 parked W9 and its 546 MB term.
5. Era-1 components that hold up:
   - pool ownership with exact-token completion (PRF-1057/1080 certified);
   - response pins (PRF-1059);
   - carried feed counts;
   - the article subject;
   - the BP listener machine;
   - checkpoint-writer cursors that refine existing codecs (resumable BLAKE3);
   - forest addressing;
   - the FNCR design;
   - the productive-READ keystone (unregistered).
6. Era-1 ideas that were wrong or duplicated:
   - the index backing (a second Message-ID table, copying page-store COW);
   - the untyped pool;
   - the dense epoch (D42: P3);
   - proof resting on SBCL's collector;
   - a stored-format change in a proof lane;
   - a third parser;
   - a byte-at-a-time D25 re-derivation;
   - ~30k lines of trajectory residue;
   - nine REPL-only books.
7. The L3 park/delete was never executed. 675 of 678 era-1 books remain, and 198 are in the image closure. Parking happened only at the
   host layer (82 files).
8. Era 2 made era-1 joins:
   - the DEFAULT pool installed before Store open (`owner.lisp:8210-8257`), never run natively;
   - the windows/decoded window on the served cold path;
   - the TCPCL received source.
   It also put history on P3 (`fn-hist-paged`, builder PRF-1265).
9. Era-2 keepers:
   - certified: typed ledger ↔ bank, committer actor (PRF-1255), journal stream (PRF-1275), arena `:closed` gate;
   - fixture-only: `fnn-unwind-cleanups` (64 sites) and the Astra lifetime fixes;
   - not certified: def-cursor/LIST/NEWNEWS cursors, the generated dispatcher, the BP session bank/scheduler, tracing and the live dev REPL.
10. Era-2 ideas that were wrong:
    - the PROGRAM twin `fn-av-mca-read-span` on every served read (`6a5427e9e`);
    - output admission gated on an always-`:unpriced` producer (the era-1 pattern again);
    - `--defer-defthm` deleting 94 theorems;
    - a declaration edited to pass a gate (`90a151a42`);
    - a never-admitted lemma (`nntp-auth.lisp:2595`);
    - natives on synthetic or stale coordinates;
    - a peer bank nothing draws from;
    - bp-session missing from the DTN build;
    - 30 orphan raw harnesses.
11. State at d4e: 59 certified / 489 uncertified / 135 planned. Capability view 4/25 proved, 0 qualified. No native at current bytes.
12. Counts (approximate, deduplicated):
    - designs: ~31 era-1 docs/specs, 11 liaison consults/answers, 4 era-2 docs plus spec extensions;
    - mechanisms: wired ~84, unwired ~23, twins 2, branch-only ≥ 3, parked 10 families, reverted 6, deleted 10 files, prose-only ~17.
13. Top harvest joins, each one join from done:
    - restate pool funding at the called name and run natively;
    - revert or prove the available-read twin;
    - `fn-ssr = fn-srs`;
    - the retire producer fence;
    - certify and register productive reads;
    - add bp-session to `build-dtn`;
    - connect the peer bank + `0373a76c1` controller to pull rounds;
    - the `legacy-header-query` → HDR/XPAT dispatch;
    - handle-holds with arena-forget;
    - move the web stream books to `:logic`.
