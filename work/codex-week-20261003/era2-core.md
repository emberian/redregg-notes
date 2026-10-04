# Era 2 Codex (root 01a0fe41) — core subsystems: store/history, served commands, resource accounting, owner lifecycle

Coordinate: origin/dev `d4e53323c` (10-03 15:20 EDT), snapshot `scratchpad/fn-dev-d4e53323c/`. Era-2 dev window: `8d17b09dd`
(10-03 01:18 EDT "Plan Codex overnight lanes…") → `d4e53323c`; 727 commits in that window (devlog.txt), all pushed by
`deputy_integration` (sole dev writer) as recomposed "Compose/Assemble/Integrate" commits — deputy lane shas are generally
NOT dev ancestors; content was checked by blob/line compare in the reader notes (`fn-notes/*/NOTES.md`).
Subject-verb census of the 727: Record/File/Archive/Regenerate 125 · Retain/Preserve/Keep 98 · Compose/Integrate/Assemble 68 ·
Connect/Wire/Drive 26 · Prove/Certify 14.

## 0. Provenance corrections (read first)

- **The twelve `planning/design/*-2026-10-03.md` docs and all 24 `planning/handoff-2026-10-03/*.md` are NOT era-2 Codex.**
  Every one was added by Claude's `b0afc2c21` (10-02 22:47, "Track the coordination state in the repo") and each header
  names a Claude author (Opus 5.5 / Fable 5.1 lanes: arena-forget, def-command, def-holder, failure-scope, host-model,
  tcb-shrink, whole-system-correctness, repair-triage, generators-2, stage-5b, sweep-*, cost-gate, lock-check, owner-offlock,
  reclaim-retention, served-catalog-live). Two Codex-authored items inside that set: `whole-system-correctness-astra-2026-10-03.md`
  (gpt-6-astra "w01", pasted by codex-liaison-11, i.e. the liaison channel, not era-2 root) and the liaison's reviews.
- **Era-2 Codex's own design text** is: `planning/overnight-2026-10-03.md` (added 8d17b09dd, 22 revisions),
  `NSLICESQUEUE.md` (every slice = a mechanism), `planning/now.md` (25 revisions), the LANEDUMP.md entries from line ~1012
  on, 27 new `planning/repair/items/*.json` (NIGHT-*, RESOURCE-OPERATIONS, STORE-PAGES, HOST-COORDINATION,
  SYNCER-COMPLETION-ESCAPE, AWAIT-COMPLETION-LIFETIME, PROOF-SWEEP-20261003, …), and spec edits on 10-03
  (`specs/resource-vector.md` 40 commits, `specs/nntp.md` 37, `specs/host.md` 23, `specs/human-client.md` 17, `specs/storage.md` 7,
  `specs/lifecycle.md` 5).
- **Era 2 integrated Claude WIP at its start**: `79850a877` merged Claude lane `served-live` WIP (NEWNEWS -cat, cold-line
  native, r71-F7/F8) ; `a2b2bc827` merged Claude `post-guard-off`; `59b8d97af` merged Claude `d39bf9a4a` "WRAPPER step 0:
  def-section"; `8cf37a368` merged Claude `burndown-3`. Several books era 2 touched originate in Claude lanes:
  `books/failure-scope.lisp` (Claude FAILURE-SCOPE), `books/host-model-machine.lisp` (Claude HM v1 `9300e2a7d`, "salvaged
  by the coordinator"; Codex repaired it at `47476090f`), `books/history-columns-foundation.lisp` (Claude lane
  history-columns 09-27; era 2 split it at `b5bb98c92`), `books/protocol-served-table.lisp` (Claude def-command DC01; era 2
  added generated `:forms`). `def-cursor` is era-2 Codex: Claude's generators-2 handoff line 186 says "def-cursor
  (GEN-CURSOR): not started".
- **Native coordinates.** Every era-2 native pass is on one of: image `ad8da41fc` (built 05:44 EDT, 583 commits before
  d4e53323c), the synthetic candidate `1a946582c` (built by `git commit-tree` from 6e711c34b + two overlaid host files,
  not on dev), the source-loaded launcher (10:00 EDT, "do not qualify the latest whole source tree"), or an "initialized
  source cache" (S132 10 MiB). `planning/now.md:35`: "There is no current whole-system native endpoint." Nothing after
  ~06:00 EDT (DEFAULT pool install, P3 roots, LIST wiring, available-read route, output admission) has been executed in a
  native process at its own bytes.
- **Registry at d4e53323c** (`planning/proofs.json`, 683 rows): certified 59 · uncertified-at-current-digest 489 · planned 135.
  `planning/current-view.json`: 25 capability rows, 4 proved (all four new small ones: operator-journal-stream, PRF-1021,
  bp-source-window, bp-source-control), 0 qualified; every core P1-P11/M4-M6/T17 `proved: no`.

## 1. Store / page / arena & history

Designed: overnight-2026-10-03.md "What the deeper reading changes" (pages + prepaid accounting foundational; "the paged
catalog already has an attachment… the next work starts there"); NSLICESQUEUE §"Page-backed history and node roots"
(:267), §"Reclaim and physical release" (:287), §"Checkpoint, recovery and bounded store utilities" (:304), §"Paged
catalog in the service" (:237); LANEDUMP "# Native history roots — Sol" (:1895) which states the design choice: build
on `fn-hrecs`/P3, "connecting [the era-1 HEP backing] alone would duplicate P3". Claude's arena-forget design
(arena-forget-2026-10-03.md, Opus) was NOT implemented by era 2 (0 era-2 subjects mention forget).

| Mechanism | Implemented (file:line, size) | State | Tested / proved | Harvest verdict |
|---|---|---|---|---|
| Incremental history image builder (append/flush/empty-suffix recycling replacing whole-suffix `fn-his-snapshot` load in the three native publishers) | `books/history-image-build-rows.lisp` 92 l (`fn-his-build-row-refines-history-append` :73), `history-image-builder.lisp` 28, `history-image-row-step.lisp` 286; host `host/native/io.lisp:3696-3725`, `host/native/history-root.lisp` 265 l (loaded build.lisp:540) | on-dev-wired | PRF-1265 certified at `certify-20261003T101722Z-1422001` (2 roots), now `uncertified-at-current-digest` (bytes moved); old-vs-new committed image equality `tests/acl2/history-image-builder-tests.lisp:65-70`; native control-flow fixture 513 events "source/session results" | keep-and-wire (recertify; image run owed) |
| P3 history abstract stobj `fn-hist-paged` (resident image immutable between adoptions, append writes the tail, MsgID buckets name ordinals) | `books/history-paged.lisp:393` defabsstobj (403 l, 29 thm), `history-paged-attach.lisp` 6, `history-paged-adopt.lisp` 149, `history-pages-resident.lisp` 152; host `history-root.lisp` | on-dev-wired (adopt/root-at host calls) | correspondence/guard/preserved thms exist; PRF-1280 `planned`, events [] | keep-and-wire (register + certify) — this is design row P3/ST5 |
| Page relocation continuation (Astra): one page per readiness/copy/zero/mark tick, 13-word header; finite runner | `books/history-pages-relocate-step.lisp` 297, `-run.lisp` 160; consumed via history-image-row-step | on-dev-wired (through builder) | certified `102524Z-1455069` and `103557Z-1487810` (component bytes); SCN-1101 stobj schedules; flat `pgs-x-grow-image` still O(image) (LANEDUMP :1866) | keep |
| Root credit (encoder length counted without materialization; page grow funded before flat resize) | `books/history-root-credit.lisp` 121; `host/history-root-host.lisp` 227 (build.lisp:375) | on-dev-wired | no PRF events found | keep-and-wire |
| Reclaim over P3 root (walk reads issued history generation, decode funding per chunk, direct P3 replacement install in swap) | `host/native/owner.lisp:7439` `fnn-owner-reclaim-walk`, `:7818`, `:7875` | on-dev-wired, partial: still `push`es every rewritten row then `fn-owner-orcp-rebuild rows` (:7807-7823) — whole Store/catalog copies, reservation unchanged | only test `tests/native_history_root_raw.lisp` stubs every ACL2 call (:94-141), not in Makefile or scenario catalog | gift-for-packet ST5/reclaim (the bounded part); the copy removal is unstarted |
| Astra S045 staged checkpoint readback (verify history pages before rename) + S114 reclaim credit from synchronized census | LANEDUMP :1469, :1510; `6c917f91b` content in `host/owner-host.lisp` (14/14 lines) | on-dev-wired | baseline-fails/repair-passes fixtures (`tests/scenarios/catalog.json`) | keep |
| Catalog availability (Option 2': "available" distinct from retained acceptance; missing facts classified once at load, tombstone fact reused) | `books/catalog-availability.lisp` 75, `-load` 56, `-owner-load.lisp` 246 (replaces `fn-sca-load-held-rows-*` in place), `-refinement` 70, `catalog-available-readers.lisp` 126, `served-availability.lisp` 177 | on-dev-wired (owner recovery loader) | PRF-1262 `planned`; Integration idx 5515: "an old theorem equates the new availability-classified loader with the raw loader. That equality is false for unavailable rows… the image remains blocked there" | keep-and-wire after the refinement is restated (gift for the group-count decision, group-count-after-reclaim-2026-10-03.md) |
| Catalog root incarnation reserved before native root binding | `books/catalog-root-incarnation.lisp` 33; owner-host.lisp | on-dev-wired | PRF-1272 `planned` | keep |
| history-columns split (logic separated so P3 attachment precedes generic introduction) | `books/history-columns-foundation.lisp` 758 (Claude 09-27 origin), `-logic.lisp` 96 | on-dev (consumed by served-catalog-join, owner-served-carried) | — | keep (refactor only) |
| Owner carrier (private structural carrier; authoritative only at an atomic caller-threading migration) + refused/aborted POST writers | `books/owner-carrier.lisp` 60 (NOT in image), `owner-post-carried.lisp` 138 (`def-carried-writer` :74, :97); `host/native/io.lisp:451-474` dispatch; `tools/owner_carrier/*.py` | owner-carrier: on-dev-unwired ("dormant… before activation", `b83173627`); owner-post-carried: on-dev-wired via def-carried-writer | no certificate covers either book's bytes (2,936-manifest scan, proof_engineering.md §4); PRF-1264 `planned` | gift-for-packet ST1b/def-carried consumers |
| Arena return custody (reset/start/recover require `:closed` return observation) | `books/payload-view-lease.lisp:146` `fn-pvl-runtime-return-step`; `host/native/io.lisp:1726`; owner.lisp:8216 guard | on-dev-wired | certify-20261003T174041Z-2716643 2/0 PASS; old-adapter counterexample archived; PRF-1308 `planned` | keep |

Not done (era-2's own words, LANEDUMP :4415-4420, :4475-4481, now.md:35-45): whole Store/catalog row copies in reclaim,
96×history credit estimate, whole-event encode, flat page-array growth, bounded checkpoint open, root/index/cold-read
correspondence, atomic carrier migration, native POST/reclaim/reopen on current bytes.

## 2. Served commands & cursors

Designed: NSLICESQUEUE §"Complete bounded discovery and view policy" (:183), §"Finish streaming and restricted command
families" (:197), §"Dense groups, overview and reclaim-aware navigation" (:253); LANEDUMP "DC02 generated switch" (:1431),
"Cursor cold reads poll on mux" (:1718), "Selective available command source" (:2642), "Actual selective owner source route"
(:2770), "Bounded LIST summary primitive" (:2987), "Incremental LIST row/status source" (:3862, :4059). The VIEW-policy
table it consumed (`command-view-policy-2026-10-03.md`) is Claude's (DEF-COMMAND, Fable).

| Mechanism | Implemented | State | Tested / proved | Verdict |
|---|---|---|---|---|
| `def-cursor` shell (consumer declares one indivisible candidate step; shell owns retained output; VISITS and BYTES bounded separately; suspended op keeps custody until receipt) + batch | `books/def-cursor.lisp` 153, `def-cursor-batch.lisp` 96 | on-dev (consumers: group-summary, list-metadata, string-line cursors) | `def-cursor.lisp` dependency digest differs from cert 113517Z (foundations notes) | keep (GEN-CURSOR realised; finish across OVER/HDR/XPAT) |
| LIST cursors: metadata / row (one byte/digit per call) / status (one char per call) / group summary; query-plan facade | `books/list-metadata-cursor.lisp` 209, `list-row-cursor.lisp` 151, `list-status-cursor.lisp` 132 (`fn-lss-one-progress` :118), `group-summary-cursor.lisp` 159, `served-query-plan.lisp` 92 (`fn-qplan-cursor-step` :83); host `owner.lisp:780` `fnn-owner-cursor-step`, render :656-678; wired by `c94e83f87` (12:36) | on-dev-wired | `tests/acl2/served-query-plan-tests.lisp:128-133` drain at w=1/256 = `fn-nntp-list-command` octets; universal cursor = reference NOT proved (LANEDUMP :4393-4395) | keep-and-wire (the universal refinement is the packet) |
| NEWNEWS: configured candidate selector, matching selector, resumable/total wildmat matcher, metadata cursor, stream cursor retaining a string renderer | `newnews-candidate-selector.lisp` 204, `newnews-matching-selector.lisp` 194, `wildmat-cursor.lisp` 1133 (107 thm), `newnews-metadata-cursor.lisp` 413, `newnews-stream-cursor.lisp` 590; consumed by `served-plan-cursor` (wired, owner.lisp/mux) | on-dev-wired | PRF-1256 (6 ev), 1257 (6), 1261 (11) all `uncertified-at-current-digest`; cert 083937Z lists `newnews-stream-cursor`, `served-plan-cursor` as FAILED ("no certificate on disk") | keep-and-wire (certify) |
| Matcher live-peak bound 38+6P+6M+11N | `books/wildmat-live.lisp` 449 | on-dev-unwired (out of image, included by nothing but its test) — proof-only twin | PRF-1261 note admits literal teeth incomplete | gift-for-packet (output tariff) or drop |
| String line renderer without coerce + fill + line buffer + logical cons cost | `string-line-cursor.lisp` 336, `string-line-fill.lisp` 114, `string-line-cursor-cost.lisp` 52, `served-plan-line-buffer.lisp` 119 (`fn-splan-line-window-preserves-residual` :91; host owner.lisp) | on-dev-wired | PRF-1274 uncertified; `string-line-cursor` FAILED in 083937Z | keep |
| Generated served command switch: 30 rows, 16 with generated `:forms` (GROUP LISTGROUP LAST NEXT ARTICLE HEAD BODY STAT OVER XOVER HDR XHDR XPAT LIST NEWGROUPS NEWNEWS); set-equal archive/form coverage assertion; unknown keywords → `fn-nntp-archive-command-pinned` directly | `books/protocol-served-table.lisp` 957 l (Claude origin; era-2 commits 48e66bb0c, 5d2626619, a79eca8fe, 5d56c2e7f, 8be10e440) | on-dev-wired (`served-catalog-chain.lisp:255`) | teeth "64/64" (LIST/NEWGROUPS), 70-event full teeth replay; PRF-1236 rewritten; no current cert | keep |
| Selective "available" command route generated by `tools/available_read_emit.py` (113 l) | `books/served-available-read.lisp` 533 l, 25/25 defuns `:program`; `served-available-commands.lisp` 331; host switched at `6a5427e9e` from `fn-mca-read-span` to `fn-av-mca-read-span` (`host/owner-host.lisp` → :4436) | **on-dev-twin**: every served NNTP read now runs a renamed PROGRAM copy of `fn-mca-read-span` (`books/owner-credits.lisp:195`); PRF-380 and `fn-scar-ocfg-read-span-is-reference-under-ocl-relation` now describe an uncalled function | PRF-1287 `planned`, events []; six-command reference tests `served-available-commands-tests.lisp:50-58` | superseded-by the proved chain: revert the host switch or prove `fn-av-mca-read-span = fn-mca-read-span` before any cite |
| Cold reads poll on mux: `fnn-owner-render-next-quantum` returns 5 values (… COLD-READ); cold = zero output + exact original plan; no await/replay loop on mux | `host/native/owner.lisp` (c922036e8+30bd8ab95), mux queue/flush | on-dev-wired | `tests.test_cursor_cold_poll` 1 pass, "mocked ACL2/I/O… source control flow, not ACL2 semantics"; retained pull renderer ignores 5th value (LANEDUMP :1755) | keep (fix pull consumer) |
| Response identity (connection/response generation words) | `books/response-identity.lisp` 52; owner.lisp:1830-1838 | on-dev-wired | certify-20261003T103508Z matches snapshot; test book not a Makefile root | keep |
| Streaming ARTICLE producer + preflight (Access) | `books/article-stream.lisp` 454, `article-stream-owner.lisp` 314; owner.lisp:756-826, mux.lisp:667 | on-dev-wired (`fn-owner-article-ready-plan-step` `:program`) | PRF-1286 `planned`; 184,483 "ARTICLE checks" = loop counts in an SBCL harness that redefines ACL2 primitives | keep-and-wire (guards) |
| HDR/XPAT header query over one immutable span | `books/legacy-header-query.lisp` 181 (out of image) | on-dev-unwired (Served never consumed it) | composition lemmas hold (LANEDUMP :4040); PRF-1304 `planned` | gift-for-packet (HDR/XPAT consumer) |

## 3. Resource accounting / banks / tariffs

Designed: `specs/resource-vector.md` (Claude resource-ledger origin 10-01 `877c69598`; 40 era-2 commits extend it),
RESOURCE-OPERATIONS.json note ("Codex 2026-10-03: … no gate before its producer"), NSLICESQUEUE §"Output allocation and
funding" (:122), §"Resource accounting across operations" (:140); LANEDUMP "optional output funding/custody producer" (:1323),
"Continuing Operator: pre-open DEFAULT partial pool startup" (:3663). The idea: one typed ledger (`fn-rl`) with
install/draw/settle refining the logical bank (`fn-rv`); each allocating family draws before effect and settles once;
physical return and operation completion are two separate receipts; the era-1 page pool becomes the "DEFAULT" pool
installed before store open.

| Mechanism | Implemented | State | Tested / proved | Verdict |
|---|---|---|---|---|
| Typed ledger ↔ logical bank correspondence (helper_resource_exec) | `books/resource-vector-exec.lisp` `fn-rl-install/draw/settle-correspondence` :790, :1676, :1697 | on-dev (book) | certify-20261003T180036Z-2785570, 0 digest mismatches vs snapshot; PRF-1211 has no events array | keep (best-grounded item) |
| Owner syncer custody (thread allowance partition; issue/physical/outcome receipts) | `books/resource-syncer.lisp` 230; owner.lisp:1821, 2058, 2075, 2078, 2140 | on-dev-wired | 6 `-keeps-representation` + 2 by-definition lemmas, NO bank correspondence; PRF-1252 `planned`; test book not a Makefile root; native `test_funded_syncer_from_mux_hold_post_and_stop` PASS on image ad8da41fc | keep-and-wire (bank theorem owed) |
| Shared output pool + generation-matched window custody | `books/resource-output.lisp` 854 (74 thm; bank correspondence :727-757); owner.lisp:1867, 1902, 1988, 1991, 2050; chain proofs `resource-output-chain.lisp` 395 (out of image) | on-dev-wired; chain on-dev-unwired (proof-only) | PRF-1259 19 events, uncertified; latest cert 123849Z has 13/296 digest mismatches incl. resource-output itself; chain only proof_repl receipt | keep-and-wire (certify) |
| Pre-factory command-family output admission + tariff preview | `books/output-command-admission.lisp` 149 (`fn-ocap-admit-preview`); owner.lisp:1938-1941; producer `host/owner-host.lisp:5514-5517` `fn-owner-output-tariff-preview` always `(:unpriced family)` | on-dev-wired gate, **producer absent**: 0 of 28 families priced; in accounted mode every command refuses; with `[resources] output_heap_octets` absent the ledger is nil and the prefix is unchecked | PRF-1278 uncertified (2 ev) | gift-for-packet ST6 (needs tariffs); keep gate off until a producer exists |
| Output reservation in heap figure | `books/output-reservation.lisp` 108; heap.lisp, owner.lisp | on-dev-wired | STATUS/HEALTH 257→273 MB fixture (LANEDUMP :4035) | keep |
| DEFAULT pool install before Store open (era-1 KW-a's join) | `books/page-read-startup.lisp` 245 (`fn-prstartup-default-plan-with-peer`), `page-read-budget-growth.lisp` 38; `host/native/owner.lisp:8210-8257` `fnn-owner-page-read-startup` → `fn-owner-page-read-install-default` → `fnn-extent-pool-storage-start` → `fnn-extent-executor-start` (added `0ca006108` 12:14, `162bc5cbe` 12:36) | on-dev-wired, never executed natively at its bytes | keystone `fn-prstartup-admitted-capacity-is-funded` is about `fn-prstartup-plan`; host calls `-default-plan-with-peer`, bridged only by-definition; checks.json "DEFAULT capacity replay timed out 30s, not proved"; PRF-1301/1310 uncertified | keep-and-wire (it closes KW-a in source; theorem at the called name + native run owed) |
| Independent peer flight bank (binary operator allowance, whole-native startup recheck, catch-up spool resources) | `books/peer-flight-profile.lisp` 44, `-reservation.lisp` 129, `-startup.lisp` 76, `peer-catchup-spool-resources.lisp` 29; heap.lisp:132-155, owner.lisp; `host/native/catchup-spool.lisp` 259 | on-dev-wired (startup); catch-up driver unwired (now.md:98-101 "remains unwired; materialized catchup is still defective") | PRF-1307 uncertified | keep; catch-up → BP/transport packet |
| Resource operation reference (principal = root slot + generation; reserve baseline/rescue before user bank) | `books/resource-operation.lisp` 140 | on-dev-unwired (out of image, no host caller, not in Makefile) | none | gift-for-packet ST6 |
| def-cost repairs (lambda reconstruction, transitive unknown-cost) + `host/cost-host.lisp` 36 l (7 rows) | NIGHT-COST-LAMBDA/UNKNOWN `ee7c686c0` | on-dev | `planning/cost-obligations.json`: proved 0 / partial 1 / derived 6 / none 1442 of 1449 dispatched entries; every row `:unaccounted` | keep (generator); no served accounting yet |

## 4. Owner lifecycle / actors / failure scopes

Designed: NSLICESQUEUE §"Safe completion and actor rollout" (:106), §"Runtime/model correspondence" (:462); overnight plan
row "Runtime coordination" (section/actor generator, lifecycle, committer, mux/cold/service, web concurrency); TCB design
and failure-scope are Claude's. Era-2's added ideas: actor custody held until confirmed physical join; physical return
and consumed outcome are separate receipts; literal JOB-RESULT vocabulary (ok/read/short/error/trailer/digest);
once-only mux terminal cleanup; committer pacing as a pure ACL2 actor.

| Mechanism | Implemented | State | Tested / proved | Verdict |
|---|---|---|---|---|
| Private committer actor (immutable values; action declarations shared with HM mapper) | `books/committer-actor.lisp` 133 (`fn-cmt-step` :41, `fn-cmt-run-keeps-the-private-invariant` :98); `host/native/owner.lisp:5041-5078` (`d09137228`) | on-dev-wired | PRF-1255 **certified** (4 ev) | keep |
| Failure-scope classification + actor exit step (Claude book; era-2 Runtime extended actor custody `3bda776c6`) | `books/failure-scope.lisp` keystones :609-650; `host/native/owner.lisp:1680-1688` (35 `fn-fs-` refs in owner.lisp) | on-dev-wired | certify-20261003T065306Z digests match snapshot; PRF-1253 `planned`, events [] | keep (register) |
| Concurrent host model HM machine (direct-read holder machine, cancellation holds, pin capture/drain invariants) | `books/host-model-machine.lisp` 967 l (Claude HM v1; Codex `47476090f`, `42e701a7a`, `2d6093677`, `f5b91fb9a`) | on-dev-unwired (out of image; Makefile root) — model only | PRF-1254 uncertified (2 ev); physical-return theorem world 168 forms/6,847,951 steps (LANEDUMP :1631) | gift-for-packet runtime/model correspondence |
| Astra host lifetime defects (8 found; 7 landed): committer escape before syncer result; raw ACL2 throw kills committer; await loop without mutex reacquire; late deliver after timed-out caller; checkpoint verifier skipped history pages; writer snapshot release race; reclaim stale cached count | `host/native/owner.lisp`, `io.lisp`; items `SYNCER-COMPLETION-ESCAPE.json`, `AWAIT-COMPLETION-LIFETIME.json` (`landed`); `tests/native_await_lifetime_raw.lisp` (real thread, `(sleep 1.1)` :67) | on-dev-wired | baseline-fails/repair-passes fixtures, in scenario catalog (8399, 8428, 8561, 8582); defect 5 (handshake slot ID) handed to Runtime: UNCHECKABLE (no tracker item) | keep |
| Once-only mux terminal cleanup; shutdown + literal job-result tuple; snapshot actor; pull lifecycle; publication/export cleanup | owner.lisp, mux.lisp, `host/native/pull-service.lisp`; raw tests `tests/native_pull_lifecycle_raw.lisp`, `native_snapshot_actor_raw.lisp`, mux_lifecycle (43 assertions) | on-dev-wired | sh-wrapped SBCL raw tests, cited in `tests/scenarios/catalog.json` (27 raw .sh entries), not Makefile targets; composed result never ran on an image ("Compressed ARTICLE/Web/reopen is prepared but unexecuted") | keep |
| Section/actor generator (`def-section`/`def-actor`) | Claude `d39bf9a4a` (step 0) merged at `59b8d97af`; PRF-1251 `planned` | prose + step-0 only; emitting macro "not started" (failure-scope.md:202) | — | Claude's packet (not era-2 output) |

## 5. Cross-cutting notes for the parent

Ideas era 2 got right (evidence):
1. Build history on P3 (`fn-hist-paged` over the existing representation) instead of wiring era-1's dense epoch / HEP
   backing — stated as the design choice at LANEDUMP :1902 ("connecting it alone would duplicate P3"); builder proved
   equal to the old one (PRF-1265 cert 101722Z).
2. Install the pool before Store recovery with the plan decided in ACL2 (owner.lisp:8210-8257) — the one join era 1 never
   made (critic §F02 "no caller in any commit").
3. Typed ledger with install/draw/settle correspondence to the logical bank (`resource-vector-exec.lisp:790,1676,1697`, cert current).
4. Physical return separated from operation outcome; actor custody kept until confirmed join (PRF-1252/1253 statements,
   `3bda776c6`, arena `:closed` gate cert 174041Z).
5. Cursor commands tested by draining at window 1 and 256 against the reference reply (`served-query-plan-tests.lisp:128-133`);
   renderers that keep the original string + offset (`string-line-cursor.lisp`), one char/digit per call.
6. Cold read as poll (5-value quantum) rather than a blocking await on the mux thread.
7. Committer control as a pure, certified ACL2 actor (PRF-1255).
8. Generated command table with a set-equal coverage assertion that refuses a missing declaration.

Ideas wrong or duplicated (evidence):
1. PROGRAM twin on the served read path: `6a5427e9e` swapped `fn-mca-read-span` for generated `fn-av-mca-read-span`
   (25/25 `:program`), leaving PRF-380's keystones about an uncalled function; PRF-1287 `planned`.
2. Gate before producer, again: output admission (`fn-ocap`) consults a tariff producer that always answers `:unpriced`
   (owner-host.lisp:5514); fail-open when the policy is absent.
3. Proof-only twins/bounds with no consumer: `wildmat-live.lisp` (449 l), `resource-output-chain.lisp` (395 l),
   `resource-operation.lisp` (140 l), `owner-carrier.lisp` (dormant).
4. Availability loader paired with an equality theorem that is false for unavailable rows (Integration idx 5515).
5. Reclaim "over P3" keeps whole-row copies; the reservation estimate is unchanged (owner.lisp:7807-7823; deputy [2430]).
6. Stubbed-ACL2 raw fixtures as evidence: `native_history_root_raw.lisp` fakes every `fnn-call` (:94-141); the web reactor
   fixture stubbed the classifier and hid a 3-tag bug (fixed 49c933f02).
7. Bring-up world with 94 deferred theorems chosen by textual transitive closure (`tools/native_source_world.py --defer-defthm`;
   list on hbox only), which removes the POST-prepare correspondence (PRF-014 keystone) from the world native runs resume from.
8. Gate passed by editing the declaration: `90a151a42` removed `fn-owner-cat-may-seal`'s keystone citation
   (`host/interfaces.lisp:1553-1556`).
9. Registry not kept: PRF-1252/1253/1262/1264/1272/1280/1287 `planned` with no events while their code is wired.

## 6. Counts (this file's 37 mechanism rows; mixed rows counted by their primary part, sub-parts listed separately)

on-dev-wired 28 (of which never executed natively at current bytes: ≥ 8 — DEFAULT pool, P3 roots/adopt, LIST wiring,
available-read route, output admission, reclaim-over-P3, catalog availability, carrier writers) · on-dev-unwired 7
(wildmat-live, resource-output-chain, resource-operation, owner-carrier, host-model-machine, legacy-header-query,
peer catch-up driver) · on-dev-twin 1 (served-available-read) · prose/step-0 only 1 (def-section/def-actor, Claude) ·
branch-only 1 (Served's `list-query-reference.lisp`/`list-row-progress.lisp`, untracked in `build/lanes/codex-sol-served`)
· parked 0 · reverted 0. Certified at current snapshot bytes among these: PRF-1255 committer; resource-vector-exec
(180036Z); failure-scope (065306Z); response-identity (103508Z); arena return (174041Z); relocation step/run (102524Z,
103557Z, component bytes). Everything else uncertified-at-current-digest or planned.
