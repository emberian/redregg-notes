# Era 2 (Codex root 01a0fe41, 10-03 01:18 -> 15:20 EDT) — transport, web, operator, tooling, tests, planning

Fork ERA2-EDGE. Read-only. Coordinate: origin/dev `d4e53323c`; snapshot
`scratchpad/fn-dev-d4e53323c/` (SNAP). Era-2 commits on dev: 737
(`codex-week/era2-log.txt`, 01:00-16:00 EDT 10-03), first `8d17b09dd` 01:18 "Plan Codex overnight
lanes". All commits carry ember's author name; lane attribution is by subject, LANEDUMP and the
thread notes in `fn-notes/*` (cited as TWO = `fn-notes/transport-web-ops/NOTES.md`, TPH =
`fn-notes/tools-proofs-horses/{SLICE-SUMMARY,deputy_tools,horses}.md`, INT =
`fn-notes/integration/notes.md`, SS = `fn-notes/storage-served/NOTES.md`, COMP =
`fn-scout/composition/*`, BS = `fn-scout/build-serve/summary.md`). Lane commits were mostly
re-committed by deputy_integration under new hashes; the dev hash is what is cited.

## 0. Attribution corrections (read first)

- **The 12 `planning/design/*-2026-10-03.md` docs and the 24 `planning/handoff-2026-10-03/*.md`
  are NOT era-2 Codex.** All 36 were added by one commit, `b0afc2c21` (10-02 22:47, "Track the
  coordination state in the repo", `Co-Authored-By: Claude Opus 5.5`), merged in Batch BM
  (`d15adc1f3` lane/coordination-in-repo). Each has exactly one commit on dev (host-model.md 3).
  Codex inputs inside them are consults: `whole-system-correctness-astra-2026-10-03.md` (GPT-6
  Astra answers) and the decision "recorded by codex-liaison-11". The repair ledger itself
  (`planning/repair/repair.py`, 247 items) is the same Claude commit.
- Era-2 Codex-authored planning: `NSLICESQUEUE.md` (created `321bd7246` 04:37, 62 commits, 852
  lines), `planning/overnight-2026-10-03.md` (created `8d17b09dd`, 22 commits, 524 lines),
  LANEDUMP.md entries (+5,887 lines across those three files `8d17b09dd^..d4e53323c`),
  `planning/now.md` rewrites, 26 new repair items (list in §6), evidence-index rows.
- Codex via the codex-liaison (Opus driving `codex exec`, 10-01/10-02, audited by Claude) is a
  third channel: `tools/lock_discipline_check.py` (t41, `00300ab57` 10-02 22:06, 2,887 lines),
  `tools/commit_map.py` (t39, `3f8525b0f`, 76 lines), the t01-t16 make-check burndown.
- Pre-week Claude tools that era 2 modified (not authored): `tools/proof_repl.py` (09-22,
  4,397 lines; 6 era-2 commits), `tools/green_check.py` (09-21; 1 era-2), `tools/evidence_store.py`
  (Claude 10-01; 2 era-2), `tools/ledger.py` (09-19; 1 era-2), `tools/farm.py` (09-19; 0 era-2),
  `tools/current_view.py` (09-24), `tools/build_lists_check.py` (09-24), `tools/fn_consumer.py`
  (09-25).

## 1. BP / TCPCL / ION / peer transport, catch-up, feeds and pull

Owners: deputy_bp_transport (01a10127-fbce, 05:46-14:08 UTC-local per TWO §1), deputy_tools
"Sol transport" re-task (TPH deputy_tools §1 tasks 2-6), horse_bounds (B002 catch-up),
deputy_operator second wave (peer policy), deputy_foundations (peer bank producer).

**Designed.** No separate design doc. Slices in `NSLICESQUEUE.md` "Fair feed and pull rounds"
(:323), "BP custody, retained work and restart" (:340), "Bounded BP/TCPCL scheduling and
reassembly" (:359), "ION and external transport outcomes" (:379). Idea: each retained BP peer
session holds a funded grant from a private bank, a scheduler gives one slot per turn so one
peer cannot monopolize listener/forwarding/receipts (SCN-1110); catch-up and pull run in
resumable fair rounds instead of whole-article materialization; peer flight work draws from a
metered bank separate from the DEFAULT store pool. Funding shape is written into
`specs/resource-vector.md` (+26 lines in `6935ff363`) and `specs/bp-node-machine.md` (+12 in
`9242395f4`).

**Implemented.**

| mechanism | files @ d4e53323c | state |
|---|---|---|
| ION helper lifetime unit (X10A/X10B) | `books/bp-ion-lifetime.lisp` (22 lines, 1 defthm; `e27ea2eb1` 06:19); host `host/workflow-host.lisp:290` <- `host/native/workflow.lisp:407` | on-dev-wired |
| BP session bank + scheduler (retained sessions, async forwarding/receipts) | `host/native/bp-session.lisp` (412 lines, `21dad2b2f` 07:45; loaded `host/native/build.lisp:597`); books `bp-session-scheduler` (77, 0 defthm), `resource-bp-session` (139, 3), `bp-session-profile` (146, 4); caller `host/native/bp-node.lisp:941-1222` | on-dev-wired in DEFAULT image; **not loaded by `host/native/build-dtn.lisp`** (no bp-session line; build-dtn loads catchup-spool at :389). `tools/build_lists_check.py` reports 10 findings "bp-node.lisp calls fnn-bp-session-… which build-dtn.lisp does not load" (TWO §1 pattern a) — the DTN image is red |
| Single-slot allocation yield, drain retries, lifetime identity capacity | `de5594be5` 13:56, `0836ce232` 13:57 (bp-session) | on-dev-wired (DEFAULT) |
| BP item-prefix availability probe | `64b19e909` 14:03: `books/bp-primary-cbor.lisp` `fn-bpc-dec`, `books/bp-bundle.lisp` `fn-bpb-take-bytes` (mbe exec prefix) | on-dev-wired |
| TCPCL Contact-header / SESS_INIT deadlines (RFC 9174 §4.1) | `books/tcpcl-retained-turn.lisp` (70 lines, 7 defthm, all `-by-definition`; `d112ee676`, `831cc2872`); 8/8 defuns host-called from `host/native/tcpcl.lisp` | on-dev-wired |
| TCPCL keepalive source control, empty transfer once | `books/tcpcl-source-control.lisp` (`ec9b1322a`), `books/tcpcl-session.lisp` `fn-tcl-send` (`6dc485ef2`) | on-dev-wired |
| BP reassembly carried quantum (S026) | `host/native/bp-service.lisp:743` `fnn-bps-fragment-job`, `:1071 +fnn-bps-fragment-quantum+ 4096` | on-dev-wired; quantum is a host constant, not an ACL2 decision |
| Standalone BP DEFAULT pool before Store recovery; peer funding + terminal custody | `b259d44c9` 13:04, `9242395f4` 14:43 (`host/native/bp-service.lisp` +35/-?), `519d3ea7a`, `1de9d1aef`, `237f6b776` | on-dev-wired at source; only source fixture `tests/native_bp_owner_startup_source.lisp` |
| Peer flight bank + bounded catch-up spool worker | `host/native/catchup-spool.lisp` (259 lines, `4e6c74fdc` 14:02; loaded `build.lisp:538`, `build-dtn.lisp:389`); books `peer-flight-reservation` (124, `6935ff363`), `peer-flight-profile`, `peer-flight-startup`, `peer-catchup-spool-resources` (29 lines, 0 defthm) | **on-dev-unwired**: bank installed `owner.lisp:8264`, closed `:8269`, drained-checked `:8503,:8527`; `fnn-peer-flight-draw/-work/-settle` (`catchup-spool.lisp:200,223,240`) and all `fnn-csp-worker-*` have callers only inside catchup-spool.lisp and `tests/native_catchup_spool_source.lisp` (grep: 61 + 32 refs, 0 elsewhere). A bank nothing draws from |
| Catch-up resumable controller / framer / 64-byte hash cursor (B002) | 661 lines, 6 files | **branch-only**: lane commit `0373a76c1` (horse_bounds, "Preserve draft resumable catchup spool controller"), not an ancestor of origin/dev. `*fn-cu-request-quantum*` 262144 / `*fn-cu-max-line*` 1048576 unchanged |
| Credential admission boundary S107-S110, S097, S112; fair pull/catch-up rounds S054/S106; fair push | deputy_tools lane commits re-composed by Integration: `8fa6b902b` 04:30, `715a8778f`, `5113378d0`, `5e53c814d`, `f2ccbff38` 06:05, `66aee1993` 06:40, `e2253251e` 07:09 (`host/native/feed-service.lisp`, `pull-service.lisp`) | on-dev-wired |
| Pull actors registered, terminal cleanup debt through close | `44899d33a` 13:55 | on-dev-wired |

**Tested / proved.**
- bp-ion-lifetime + tests: certified `certify-20261003T095031Z-1342869` (lane tree
  bp-transport-oct03, 2/0); no native run (LANEDUMP:1654, TWO §1.1).
- bp-session-profile / resource-bp-session / bp-session-scheduler / tests: certified
  `certify-20261003T114543Z-1687865` 4/0 (TWO §1.2); `tests/acl2/bp-session-turn-tests` added
  to Makefile:1089 at the final push (INT C4). bp-session-profile last cert 15:44Z but changed by
  `7d276a946` (COMP tail table row 6).
- Prefix probe: `tests/native_bp_prefix_probe_source.lisp` asserts 65,540 -> 4 cons visits,
  results `equal`; evidence `planning/evidence/bp-prefix-probe-source-2026-10-03.json`;
  certify-20261003T180302Z bp-primary-cbor + bp-bundle pass. The measure is mbe :logic vs :exec
  of the same function; the decoder/CRC/publication remain whole-frame (S068 open).
- tcpcl-retained-turn certified 15:50Z, tcpcl-session 16:33Z, tcpcl-source-control 16:35Z
  (COMP tail rows 26-28) — after the snapshot commit time, at what bytes UNCHECKABLE here
  beyond COMP's "cert at snapshot bytes" column, which lists them as certified.
- Native: **SCN-1110** (two-peer selector, `tests/test_bp_node_native.py:250`) never executed;
  SCN-1090 (trickling pull), SCN-1106 (pending TLS push link), SCN-1126/1127/1128/1134/1137/1138
  all `specified` in `tests/scenarios/catalog.json`. No BP/pull native at any era-2 coordinate.
- Bank/spool: source fixture only (`tests/native_catchup_spool_source.lisp`,
  `tests/native_peer_bank_startup_source.lisp`).

**Verdict for harvest.**
- bp-session bank/scheduler: keep-and-wire — the one join is adding it (and the 7 books/2 raw
  loads, BS "DTN image gap") to `build-dtn.lisp` + regenerate `image-world-dtn`; then run SCN-1110.
- prefix probes, TCPCL deadlines/keepalive, ION lifetime: keep (wired); certify at snapshot bytes.
- peer flight bank + catchup-spool worker: gift-for-packet "catch-up bounded" — the worker and
  bank are the half on dev; the other half is `0373a76c1`'s controller; the join is
  `pull-service.lisp` drawing a lease per round. Unharvested, it is 259 loaded lines of dead code.
- fair pull/push rounds: keep; owed SCN-1090/1106 natives.
- reassembly quantum: keep; move the 4096 into the profile/ACL2 side when the BP tariff lands.

## 2. Web face

Owner: deputy_web (01a10127-7a99, 4.55 h); defect fix by deputy_integration; E016 by
horse_entries; consistency C-items on web.

**Designed.** `NSLICESQUEUE.md` "Concurrent web service" (:407) and "Web ARTICLE collector
continuation" (:573). Idea: a reactor/mailbox over fixed private reply buffers; large read
routes (article, 100-row overview, LIST of 0/1/1,003 groups) go through one shared
capture/replay engine that streams HTML from retained segments instead of materializing the
full reply; POST parsing/subject encoding/body windows stream (SCN-1105, 1113-1116, 1119, 1122).

**Implemented.**
- Five books, all `:program`, **0 defthm each**, none a Makefile root:
  `books/web-article-stream.lisp` (169), `web-list-stream` (50), `web-page-cursor` (67),
  `web-post-stream` (193), `web-reply-stream` (120). Host: `host/web-host.lisp:9-11` includes
  page-cursor/reply-stream/post-stream; `:176-182` calls `fn-was-*`, `:197-201` `fn-wrs-*`
  (article/list streams reached through web-reply-stream). State: **on-dev-wired, unproved**.
- `books/web-session-keystones.lisp` gained `fn-wss-k-reads-ignore-session-table`,
  `fn-web-private-reply-is-table-step`, `fn-web-private-begin-is-captured-gate` (PRF-1279/1290):
  on dev; REPL-admitted only (`requirements.json:6701` "certification … pending") (TWO §2.2).
- POST classifier fix `49c933f02` 10:34 (deputy_integration): `host/web-host.lisp:99
  fn-web-host-action-kind` gains `:post-form :post-command :post-stream`; the raw reactor fixture
  had stubbed that function (INT C3). on-dev-wired.
- E016 web teardown/capacity-before-listen/close receipts `6de37169e`; account-creation
  uncertainty after lost redemption reply `1d8e74e21`. on-dev-wired.

**Tested / proved.** Raw witnesses `tests/native_web_{reactor,article_stream,over_stream,
list_stream,page_cursor,post_stream,private_begin}_raw.lisp` assert byte equality with the old
renderer (sizes 0/1/1003); not in Makefile, not certified. Browser test
`tests/test_native_web.py:228` passed once (16.702 s) on world `ad8da41fc` + scratch overlays
(`planning/evidence/web-post-action-fix-2026-10-03/execution.json`) — not current source;
concurrent (`test_stalled_socket_…`) and TLS cases not run. Web is outside
`books/image-world-dtn`'s graph (COMP §4), so the current-union world never covered it.

**Verdict.** keep-and-wire: guard-verify the five books to `:logic` and state
"stream = old renderer" as theorems (the raw asserts are the statement); certify
web-session-keystones; run concurrent + TLS cases on one image. Full reply funding/tariff is owed
to the resource ledger (gift for the output-allocation packet).

## 3. Operator / control / journal / access

Owners: deputy_operator (01a10121, two waves), deputy_access (01a10126), horse_exits /
horse_entries / horse_consistency / horse_bounds (12:15-14:07), astra_source_trace.

**Designed.** `NSLICESQUEUE.md` "Operator commands and trustworthy diagnostics" (:438),
"Authentication, TLS, access and reconfiguration" (:393), "Safe completion and actor rollout"
(:106). The horses' `.spw` ledgers (§4) are the design record for the cleanup family. Idea:
every physical acquisition/return is a receipt; a close/cleanup failure never replaces the
primary outcome; an issued-but-unobserved syscall is "uncertain", not "refused".

**Implemented.**

| mechanism | files @ d4e53323c | state |
|---|---|---|
| Incremental journal replay in bounded windows | `books/owner-time-journal-stream.lisp` (545 lines, 9 defthm; `fn-otjs-report-refines-journal-report` :522 unconditional); host `host/native/io.lisp:3924-3934` | on-dev-wired; **certified** (PRF-1275, certify-20261003T110141Z / T112822Z) — one of the 4 proved capabilities in the final current view (INT C5) |
| Bounded retire observation | `books/native-retire.lisp` (245 lines, 8 defthm; book Claude S9 09-29 `f021f3158`, era 2 added observation step); host `host/native/operator.lisp` `fn-nret-observation-step/-expired-line/-fault-line` | on-dev-wired; uncertified |
| Compatible init resume | `books/native-init-resume.lisp` (85, 2 defthm, `debaad165` 06:43) <- `io.lisp` | on-dev-wired; uncertified; SCN-1100 specified |
| Pre-open DEFAULT pool startup, orphan-worker cleanup | `books/page-read-startup.lisp` (245, 6 defthm, `162bc5cbe` 12:36); 10/19 defuns host-called (owner/extent/heap) | on-dev-wired; tested only by `tests/native_owner_pool_startup_source.lisp` which stubs `fnn-core`, `fnn-store-close`, `fnn-heap-*`, `fnn-extent-*`, `fnn-owner-install` (:53-182) |
| DEFAULT heap command + next-run diagnostics, protected Store growth vs pool, runtime collector room | `8facb3cce`, `1a853af29` (`books/heap-store-figure.lisp` +3 defuns), `88877efc2`, `2675f2609`; `tests/native_heap_default_source.lisp` | on-dev-wired; SCN-1136 specified; `heap-store-figure`, `cold-read-reservation` uncertified at snapshot bytes (COMP rows 7, 12) |
| `fnn-unwind-cleanups` macro + exits EX01-EX16 | `host/native/io.lisp:545` macro; 64 call sites in 14 host files; commits `e60931096`…`376e3cdd6` | on-dev-wired; raw fixtures only; one ACL2 edit `books/log-sink.lisp` `fn-log-sink-offer-live` (`9d9110af5`) never run |
| Entry fixes E001-E016 (13 code: redeem stage order, TLS client ERR_clear_error, BP journal leak, arena seal-list residency, AUTHINFO lock faults, FIFO TOCTOU on import MANIFEST, web teardown…) | `f3b9d5909`…`6de37169e` | on-dev-wired; 5 confirmed bugs by reading + 8 plausible (TPH horses §1) |
| Consistency fixes C001-C009 incl. STARTTLS cursor reset (RFC 4642 §2.2.2) | `48c18731b`…`2675f2609`; `7b042111d` adds `(local (defthm fn-auth-tls-reader-base-preserves-consistentp …))` at `books/nntp-auth.lisp:2595` | on-dev-wired; that lemma failed twice at 200k steps on hbox and was committed in a never-admitted form (TPH horses §"Biggest problem") — nntp-auth likely red |
| Redeem input bounds (B001) | `books/native-redeem-input.lisp` (75 lines, 2 `-by-definition`-class defthm, **not a Makefile root**) <- io.lisp `fn-rip-command` | on-dev-wired; uncertified |
| No-op/refused reclaim skips history rewrite (B007) | `2e4c3da60` (`checkpoint.lisp:106`) | on-dev-wired |
| App journal lifetime cap 4096 (B003), archive dir sort (B010) | `books/app-journal.lisp:15,89-96`; `io.lisp:4841` | prose-only (found, unfixed) |
| Access: STARTTLS after auth refused; streaming ARTICLE/HEAD/BODY producer | `books/nntp-auth.lisp:3209,3476` (PRF-1266); `host/native/owner.lisp:756-766,818-826` (`fn-asto-preflight-planp`, `fn-owner-article-ready-plan-step` :program), `mux.lisp:667`; keystone cited `host/interfaces.lisp:2096-2101` | on-dev-wired (SS §3) |
| Access: HDR/XPAT retained header query | `books/legacy-header-query.lisp` (181, 16 defthm, `8630f38a3` 13:15, Makefile root) | **on-dev-unwired** (referenced only by its tests + `tests/native_header_query_source.lisp`; HDR/XPAT dispatch handed to Served, not picked up) |
| Export MANIFEST staging, node-secret rotation, exit map | `c53008594`, `376e3cdd6`, `50939d4f8`, `37911381c` | on-dev-wired |
| Astra source-trace: syncer completion escape, await lifetime, checkpoint staged verifier (S045), reclaim stale credit (S114) | 7 of 8 landed via Integration re-commits (`dbf890a93`, `2fc251d14`, …); items SYNCER-COMPLETION-ESCAPE / AWAIT-COMPLETION-LIFETIME `landed` | on-dev-wired; defect 5 (handshake slot ID) UNCHECKABLE (no item) |

**Tested / proved.** Certified at current bytes: owner-time-journal-stream (+tests) only, plus
Access's "narrow certifications" archived `d52618ff5` (grammar/Xref guards; SS §3). Everything
else: REPL-admitted (`fnn-dev-admit` in warm hbox sessions) and/or SBCL `--script` raw
fixtures that load extracted production defuns with injected I/O (≈44 horse fixtures, 17
evidence JSONs for entries). Six horse-changed books have no certification through 15:20:
nntp-auth, consumer-reason, limits-live, native-redeem-input, log-sink,
peer-catchup-spool-resources (TPH). Access's "237,330 header and 184,483 ARTICLE checks" are
loop counts in an SBCL harness that redefines ACL2 primitives in CL
(`tests/native_header_query_source.lisp:5-14,99-111`) (SS §3.5). No operator native at any
current coordinate ("Physical command checks await History's native endpoint", operator [2881]).

**Verdict.** journal stream: keep (done). Retire/init/startup/heap diagnostics: keep-and-wire —
certify and run SCN-1100/1130/1136 on one image. `fnn-unwind-cleanups` + exits/entries fixes:
keep (they are the "primary outcome survives cleanup" rule made a macro); owed: an ACL2 fact
the macro discharges, or at least one native failure schedule. nntp-auth:2595 lemma: fix
first (red book on the served closure). legacy-header-query: gift-for-packet HDR/XPAT (join =
Served dispatch). B002/B003/B010: open defects for the bounds packet.

## 4. Proof engineering and tooling

**Designed.** `NSLICESQUEUE.md` "Shared structured tracing and allocation feedback" (:504),
"Proof simplification, tooling and historical implementations" (:522); repair items NIGHT-*
(11) define each tool gate with an expected failure.

**Implemented.**

| mechanism | files @ d4e53323c | author / state |
|---|---|---|
| Structured tracing | `host/native/trace.lisp` (204; `fnn-trace-span` :83-113, row fields :6-7, `FN_TRACE` clock-only vs `FN_TRACE_ALLOC` :36-44, JSON lines :142, hotspots :155-204); loaded `owner.lisp:512`, configured `:8283`, reported `:8472`; spans at `owner.lisp:547-558,1420,2521`, `mux.lisp:571,828`, `dev-repl.lisp:64`; `tools/native_trace.py` (109); spec `specs/host.md:1946-1985` | Codex deputy_tools (`13e6cba75` 07:54 …); on-dev-wired (opt-in) |
| Live developer REPL into a running owner | `host/native/dev-repl.lisp` (260; start hook :216-235, registered :258, run `owner.lisp:8399`; eval inside owner quantum :51-74; loader refusal boundary :40-49,114-167); `tools/fn_dev.py` (160); `fnn-dev-admit :step-limit` (`f618b71f0`) | Codex root (`3f78bd7e8` 09:16) + deputy_tools hardening; on-dev-wired, developer image + `FN_NATIVE_DEV_REPL` at start only |
| Allocation measurement probes | 11 raw harnesses (`tests/native_{decoded_decision_allocation,immutable_cursor,immutable_matcher,immutable_newnews,matcher_heap,protected_window_allocation,trace_*,dev_file_refusal}_raw.lisp`), `tools/native_matcher_probe.py` (152) | Codex; test-only, not run by any suite. Archived: decoded 12,795,040 -> 2,876,592 and protected-window 523,504 -> 425,808 (`planning/evidence/tools/incremental-*-20261003.json`); NEWNEWS 8,906,224 -> 7,332,640 and matcher 20,127,712 -> 13,720,736 lane-local only; all on the historical "ad8" cache (TPH deputy_tools (a)) |
| `fn-list/immutable` sharing in cursor books | `books/immutable-list.lisp`, `wildmat-cursor.lisp:5,18,22`, `def-cursor.lisp:12,68`, `extent-window-stream.lisp`, `-compressed.lisp` | on-dev-wired; **uncertified** (no manifest covers these bytes; guard/equality only via `fnn-dev-admit`) |
| Repair verifier (base-red/head-green with designated assertion) | `planning/repair/repair.py:196-373` `regression/run_test_at/verify`, `tools/repair_unittest.py` (63), `tests/test_repair_verify.py` (21 tests) | Codex NIGHT-VERIFY on the Claude ledger; wired; used only by its author (19 items with `expected_failure`) |
| Scoped green gate | `tools/green_check.py` etc. (`1417f80a6`); `Makefile:2959`, `tools/cut_release.sh:306` | Codex NIGHT-SCOPED-GREEN; wired. 179.9 s -> 3.95 s timing is LANEDUMP prose only (:243-246) |
| Frozen evidence cache, source prefix, nested fixture inventory, duplicate-load gate (S141) | `f1a4d773c`, `7567ef1ba`, `76acfb91e`, `4315dbeba` | Codex NIGHT-*; wired in tools |
| proof_repl artifact acquisition (exact/compatible union, `--cached-only`, refuse surplus closing forms, source load timeout) | `tools/proof_repl.py` commits `55317b11a`, `eb6858e79`, `3bb097f3a`, `b85b07ed7`, `015c6ff35` | Codex on Claude tool; wired; "live speed improvement remains unmeasured" |
| `tools/native_source_world.py` (315 lines, `149fbe605` 10:56; `--defer-defthm` `439ce3b2a` 11:20) | `selected_defthms` :51-90 deletes named defthms, refuses names with `{`/`guard-thm`/`correspondence` (lexical) | Codex (deputy_history/root); on dev; produced the "current-union" world with 94 deferrals whose list exists only on hbox (INT §4d, COMP §1) |
| Proof census + two matched speedups | `tools/proof_sweep.py` (163, `22a8d46f4`); `books/cbor-invariants.lisp:602` 2,546,048 -> 1,081,858 steps; `books/bp-workflow-invariants.lisp:416` 1,875,212 -> 12,587 | Codex deputy_proof_engineering + lunas; certified `certify-20261003T083937Z-1180317`; ~12 theorems of a 38,004 census; sequence packet `22a8d46f4` uncertified |
| `.spw` maps/audits | 23 tracked files, 3,905 lines (`machines.spw` 16 host-entry cards all "catalogued; full leaf trace pending"; `boundaries.spw` 14; `audits/{entries,exits,bounds,consistency}`; `constant-candidates.json` 313 constants all "candidate"); `tools/spw_entry_inventory.py` (81, `28c7bf496`) | Codex horses; prose-only (catalog/navigation; the third-party workbench is git-ignored) |
| HM concurrent host model | `books/host-model.lisp` (1,136), `books/host-model-machine.lisp` (967), Makefile:1019-1021 | Codex deputy_groundwork; model by design (no host caller); certified at intermediate digests only; composed `fn-hmc-run-keeps-invp` (PRF-1242) is a comment at `host-model-machine.lisp:80-81` |
| Owner carrier | `books/owner-carrier.lisp`, `books/owner-post-carried.lisp`, `tools/owner_carrier/*`, `host/native/io.lisp:451-474` (`2ae58ef8f`, `b83173627`) | Codex; on-dev; two theorems never admitted (TPH Q1) — belongs to the owner/store fork's axis |
| `tools/lock_discipline_check.py` R1-R10 | 2,887 lines, Makefile:2525-2528 report-only in check-fast | Codex via liaison (t41, 10-02); wired |

**Tested / proved.** Tracing: `tests/test_native_trace.py` (4 tests, real SBCL). Dev REPL:
`tests/dev_repl_native.py` + `planning/evidence/repair/dev-repl-native-owner.{json,log}`
(DEV-REPL-NATIVE-OWNER-PASS) on a developer image of the ad8-era source. `tests/dev_file_refusal_native.py`
staged, never run. Repair verifier: 21 unit tests. **`tests/test_native_raw_scripts.py::
test_every_raw_harness_has_a_runner` is red at d4e53323c: 30 raw harnesses with no runner**
(11 deputy_tools, 1 horse_consistency, 8 source-assembly relay, …) (TPH cross-cutting).

**Verdict.** trace.lisp + dev-repl: keep (wired, opt-in). Allocation probes: keep the two
archived; add runners or delete the 30 orphan raw harnesses (the check is red). immutable-list
sharing: certify or revert (served-path books uncertified). repair verifier, scoped green,
frozen cache: keep. native_source_world `--defer-defthm`: superseded-by "certify the closure"
(COMP §0.2: every deferred theorem passed certification on 10-03; make the flag discovery-only,
BS). .spw: drop as an assurance artifact; keep `machines.spw` as a navigation index. HM model:
gift-for-packet runtime/model correspondence (owed: certify at current bytes, state PRF-1242).

## 5. Tests and harnesses (deputy_empirical, deputy_groundwork, Integration)

**Designed.** `planning/empirical-workloads.md` (created `030f9a2c6` 02:42, 12 commits): a
matrix of actual-image workloads (mixed POST/read, slow reader, crash schedule, cancellation,
reclaim credit, peer interruption, app recovery, 1k->100k curves) and replayable faults.

**Implemented.** `tools/native_mixed_workload.py` (484 lines; VmRSS/VmHWM/fd sampling every
100 ms :114-123, per-actor p50/p95/p99 :80,226-266, sealed journal + manifest; asserts recovered
bytes/numbers = acknowledged history :198-203); `tests/test_native_mixed_history.py`; evidence
index rows `planning/evidence-index.tsv:7371-7399`. Scenario catalog: SCN-1100..1138 added this
era — 32 `specified`, 1 `implemented` (SCN-1101 history relocation), 4 without a status
(SCN-1120/1121/1123/1124). Groundwork ran `tools/fn_consumer.py` (Claude, 09-25) 4 application
scenarios at source `ad8da41fc` (SCN-061/080/106 `implemented`). State: on-dev-wired (CLI tool).

**Tested.** Real runs, small, on non-dev coordinates: candidate `1a946582c` (synthetic
`read-tree/commit-tree` commit, INT C1) mixed 48 articles 4.198 s; `ad8da41fc` (lane commit +
overlays, 583 commits behind d4e53323c) mixed phase 0.877 s / 1.762 s slow reader, writer p95
178-179 ms / 217-293 ms, RSS peak 568.6 MiB, FD peak 23; funded POST/stop 2.732 s, held read
2.546 s, cancel 40.981 s (TWO §4, INT C2). After 05:44 EDT no image was built from current
source; "There is no current whole-system native endpoint" (`planning/now.md:76`). Not
delivered: curves, per-command I/O attribution, SCN-001 peer interruption (failed on Store
retention refusal), app recovery (UNCERTAIN 3 at bootstrap), SCN-1129.

**Verdict.** native_mixed_workload.py: keep (the harness is the asset; rerun on the first
stage-0-lineage image). Specified-but-unrun SCN-11xx rows: gift-for-packet "native matrix" —
each names a real selector.

## 6. Planning / ledger machinery

**Implemented (Codex).** NSLICESQUEUE.md (25 slices, headings :106-667; each with owner,
"current position", anchors to repair items/specs); overnight-2026-10-03.md (roster table,
"push before verify" rule, reorientation recipe via `cv`); LANEDUMP.md 10-03 sections
(Source assembly ×33 by helper_source_assembly, etc.); 26 new repair items (NIGHT-VERIFY,
-SCOPED-GREEN, -FROZEN-CACHE, -SOURCE-PREFIX, -NESTED-FIXTURE, -REALIZATION-SOURCE,
-DIRECT-TEMPLATE, -MACRO-READING, -STATEMENT-ROUTE, -LOCK-IDENTITY, -SELECTOR-HARNESS,
-ACTOR-JOIN, -CARRIER-REPLAY, -COST-LAMBDA, -COST-UNKNOWN, BP-RETENTION-ROUTE,
PROOF-SWEEP-20261003, AWAIT-COMPLETION-LIFETIME, SYNCER-COMPLETION-ESCAPE, sl-cold-line-deadline,
sl-cold-line-quanta, BUILD-PAGE-EXECUTOR, WR01, HARVEST-WORK, HOST-COORDINATION,
RESOURCE-OPERATIONS, STORE-PAGES). Ledger at snapshot: 308 items; open 96 / in-progress 98 /
ready 2 / landed 97 (`planning/repair/STATUS.md`, generated 18:27Z); Codex-owned 63: in-progress
50, landed 8, ready 2, open 3. Final generated view `fde81b59b`: 25 capability rows, 4 proved
(all new small: operator-journal-stream, PRF-1021, bp-source-window, bp-source-control), 0
qualified (INT C5). 132 of 737 era-2 commit subjects start Archive/File/Record/Regenerate/Refresh.

**State.** prose-only (queue, plan, dumps); ledger items are data on dev. `planning/interfaces-gaps.md`
still dated 2026-09-29, not regenerated (INT C4). `90a151a42` removed the keystone citation of
`fn-owner-cat-may-seal` from `host/interfaces.lisp:1553-1556` to pass the host-ld gate (INT C1).

**Verdict.** NSLICESQUEUE: keep as the harvest index for era 2 (each slice names its anchors);
supersede its "push before verify" clause by the push gate in BS. Ledger: keep (Claude
machinery, Codex added the verifier). The 50 Codex in-progress items: re-own or close.

## 7. Candidates for the cross-cutting sections

Right:
- Primary outcome survives cleanup: `fnn-unwind-cleanups` (io.lisp:545) + "issued-unobserved =
  uncertain" (EX11 profile rename, EX16 secret rotation) — 64 call sites, one rule.
- Prefix probes instead of whole-suffix scans (BP 65,540 -> 4 visits, measured).
- One-slot-per-turn BP scheduler with private session grants (SCN-1110 shape).
- Journal replay in bounded windows with an unconditional refinement to the list report
  (`fn-otjs-report-refines-journal-report`) — the one certified era-2 capability.
- Opt-in structured spans with explicit allocation scope; live dev REPL inside an owner quantum.
- A repair verifier that demands the designated assertion red at base and green at head.
- Raw fixtures that load the extracted production defun (horses) — narrow but real, and the
  web case showed why they must call the real classifier.

Wrong or duplicated (with evidence):
- Push-before-verify (`NSLICESQUEUE.md:39-44`): 6 horse-changed books + 5 cursor books + nntp-auth
  lemma landed uncertified; DTN image red from bp-session (build_lists_check 10 findings).
- Native "passes" on synthetic/stale coordinates (`1a946582c`, `ad8da41fc` + `ld` overlays)
  reported beside current source (INT §4).
- A theorem-deletion loader (`--defer-defthm`) to reach a logical world — every deferred theorem
  had passed certification that day (COMP §0.2); the cap, not the statements, refused.
- Gate passed by editing the declaration (`90a151a42`, interfaces.lisp:1553).
- Program-mode books with zero theorems counted as Web "source" (5 web-*-stream books).
- Infrastructure without consumer: peer flight bank installed, never drawn; catch-up worker
  loaded, never called; controller left on a lane (`0373a76c1`).
- Raw harness proliferation without runners (30; suite check red).
- Big check counts as evidence (237,330 / 184,483 loop iterations in a CL re-execution).
- `.spw` catalog with every card "full leaf trace pending" and 313 constants all "candidate".

## Counts (this fork's scope, 52 mechanisms)

on-dev-wired 36 (of which certified at current bytes: journal stream, ION lifetime, bp-session
books, prefix probe, TCPCL turn/control/session, 2 proof speedups — ≈9; the rest REPL/fixture
only) · on-dev-unwired 4 (peer flight bank, catch-up spool worker, legacy-header-query,
runtime-collector.lisp era-1 residue still in tree, loaded by nothing) · on-dev-twin 0 ·
branch-only 2 (`0373a76c1` catch-up controller; lane-local `build/dwj-trace/events.lisp`
prototypes) · parked 0 · prose-only 10 (NSLICESQUEUE, overnight plan, LANEDUMP entries,
`.spw` maps/audits, empirical matrix rows, B002/B003/B010 findings, SCN-11xx specified rows,
HM PRF-1242 target, 179.9 s timing, NEWNEWS/matcher numbers) · reverted 0.
UNCHECKABLE: the 94-deferral list (hbox-only file); Astra defect 5's fate; root<->deputy briefs
(encrypted payloads); TCPCL cert byte-match beyond COMP's table.
