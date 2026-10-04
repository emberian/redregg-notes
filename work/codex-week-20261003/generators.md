# Generators & macros, the codex-liaison channel, and Stage 0 — fork GEN, at origin/dev d4e53323c

Snapshot read: `scratchpad/fn-dev-d4e53323c/`. Authorship from `git log origin/dev -- <path>` (all commits carry
ember's author name; lane prefixes like `generators-2:` / `def-entry:` / `def-command:` / `stage-0:` are Claude lanes,
unprefixed imperative subjects after 10-03 01:18 -0400 are Codex era-2 deputies; Codex era-1 shas are pre-10-01).
"In image" = in the transitive include closure of books/image-world{,-paged,-dtn}.lisp (computed: 1,150 books).
Certification: `planning/proofs.json` marks nearly every PRF `uncertified-at-current-digest`; where a run is cited
below it is the cited run, not re-verified. No builds were run.

**Headline: the generator family is Claude-designed and Claude-implemented (Fable lanes generators, def-carried,
generators-2, def-holder, def-entry, def-command, failure-scope, 10-01..10-02). Codex's share is (a) era-1: none of
these macros; (b) codex-liaison (gpt-6.1-sol t01-t02, gpt-6-astra t03+): ~25 reviews of generator READYs, four
def-loop conversion/extension tasks, generator bug-fix tasks, and the design consultations c04/c05/c06/c07/c09 whose
rulings were ADOPTED as the design; (c) era-2 Sol deputies: def-cursor (new), def-actor (new), definterface
:operation (new), def-cost's first host instances, the DC02 dispatcher switch and most def-command rows' growth.**

## A. Generators, one entry each

### def-loop — books/def-loop.lisp (863 lines)
- Designed: Claude generators lane (Fable), store design §4 stage 1 (planning/design-store-representation-2026-10-01.md); loop twin = (mbe :logic recursion :exec loop) + equivalence from one form.
- Implemented: 4e56f2d01 (10-01 06:14, generators) .. 7216b7054 (10-01 09:41 = Codex t25 bd0a4d5da remapped, ":map :base, base-first"). Codex liaison tasks: t18-defloop-gen (library induction per shape), t17-defloop-1 (10 of 24 hand twins in 7 books, -295 lines), t21-defloop-2 (8a66941e1->146686a0b, 8 twins in 7 books, -233), t25-defloop-gen2. Consumers: 50 forms in 32 book files; 3 `; GEN: def-loop` markers. In image. State: on-dev-wired (instances are the executed :exec of in-image functions).
- Tested/proved: codex-genscan manifest certify-20261001T160420Z-3208843 (17 def-loop-converted books + 51 direct dependents, 68 roots, hbox) per 0dab252bf; t25+t21 persvati certify-20261001T140258Z-2023672 CERT 0. Current digest: UNCHECKABLE (no cert run at d4e53323c read).
- Verdict: keep (done); remaining hand twins (494 per COMPLETE-BEFORE ST1) are conversion work, L12.

### def-representation — books/def-representation.lisp (1,215) + -lib (145) + -paged (2,318) + -tree (187) + -tree-walk (640)
- Designed: Claude generators lane (abstract stobj from one declaration), store design §4 ST1/ST3; paged foundation by Claude gate-b lanes.
- Implemented: eb481f4b1 (10-01 06:17) .. 135110646 (10-02 00:28 cert-roots). Codex share: reviews r04, r17, r19, r20-r23, r27, r30, r33, r35, r37, r39, r40, r42, r47 (gate-b/paged-catalog READYs), fix tasks t10-genfix (2f02804ad->73423e079), t22-genfix2 (8e39d3776: not found in commit map nor on dev — UNCHECKABLE), t32-imageid (90342fc47->36d1d2018). Consumers: 1 book instance (`fn-crow`, books/catalog-paged.lisp:88), 16 test forms. catalog-paged is in the image closure; no host file names fn-crow (served use is via the paged catalog attachment on the image-world-paged route). State: on-dev-wired only on the paged image route; on the default image, on-dev-unwired (the paged catalog is ST3 "Paged catalog in the service", NSLICESQUEUE §"Paged catalog in the service").
- Tested: PRF-1225/1226/1227 `planned`. Reviews r20/r23/r27/r30/r33/r35/r39/r40/r42/r47 all CONFIRMED findings, fixed forward per the liaison log.
- Verdict: keep-and-wire (ST3: the catalog behind attach-stobj on the served image).

### def-carried — books/def-carried.lisp (1,404) + def-carried-writer.lisp (1,012)
- Designed: Claude def-carried lane (Fable): a carried invariant from one declaration, completeness checked against the world; derives D40's raw-dispatch rows (`:raw-with (:carried ROW)`).
- Implemented: a6ed957ed.. → a6ab51574 (10-01 06:07) .. ac5edbd9b (10-03 02:10, Codex era-2 "Classify POST raw dispatch as temporary native trust with explicit writer debt"). def-carried-writer eb351dc75 (10-02 18:34, def-entry lane) .. 87ea28674 (X06). Named escape `:incomplete (A-OWNER-INVARIANT-CARRIED (...))` by Claude lane post-guard-off (56efd6906, 10-02 23:30; D40 status 2026-10-03 in planning/decisions.md). Codex share: the liaison reviews r02 (7 raised/7 confirmed; coordinator HELD def-carried from dev on F2 "composed-term theorem bound to a raw entry"), r14, r15, r16, r24, r25, r28, r29, r60 (raw-dispatch-3, SOUNDNESS CLEAN), r63, r69; fix tasks t12-dcfix (0b8a3046f->bc2f30fd3), t14-dcfix2 (stopped), t14b-dcfix3 (04299d899->22a837287, "the one validator"). Consumers: 4 rows — fn-owner-retain-carried (books/owner-retain-carried.lisp:189, in image), fn-tcl-session-carried (books/tcpcl-session-carried.lisp:42, NOT in image), fn-owner-served-carried (host/owner-served-carried.lisp:59, ld by host/native/build.lisp:422), and the row def-holder emits (books/def-holder.lisp:1073); def-carried-writer: 2 writers in books/owner-post-carried.lisp:74,97 (Codex era-2 book, 2ae58ef8f 10-03 06:25, in image); def-carried-profile: 2.
- State: on-dev-wired — host/interfaces.lisp has 15 `:raw-with` entries; seven owner entries (fn-owner-io, -take, -control-submit, -prepare-retention/-identity/-consumer/-topic) dispatch raw under the escape; 338 writers named as owed (decisions.md D40 status 2026-10-03). 6 `:raw-guarded` routes remain (e.g. host/interfaces.lisp:34 create-fn-resource-ledger, :4406 fn-hrecs$c); stage 0 dropped Codex era-1's six bootstrap :raw-guarded routes (comment at host/interfaces.lisp:5324).
- Tested: r60 soundness clean; PRF-001/014/188 (cite owner-served-carried) `uncertified-at-current-digest`; native comparison selector FN_NATIVE_DISPATCH_COUNTERPART=1; "matching raw/counterpart POST measurements remain outstanding" (D40 status).
- Verdict: keep; the 338 owed writers are the STAGE-5B carrier work (NSLICESQUEUE §"Owner carrier and removal of whole-state revalidation").

### def-carried-view (+ def-carried-reader) — books/def-carried-view.lisp (1,038)
- Designed: Claude generators-2 (lanedumps/generators-2.md interface sketch); Codex c04 consultation answer pasted under "Astra's view", ADOPTED by the coordinator (liaison-11 log).
- Implemented: 319c1da87 (10-02 18:21) .. ef9baca4d (10-02 22:32, "WIP for the dev merge"). Consumers: fn-nnw (books/newnews-cursor.lisp:80) and fn-wix (books/withdrawal-index-carried.lisp:75, 2 readers :114,:124). Neither consumer is in the image closure; def-carried-view itself is not. State: on-dev-unwired (library + two pilots).
- Tested: ledger GEN-CARRIED-VIEW `in-progress`: fixture 55/55, nnw pilot 53/53 + tests 41/41 (REPL, hbox); PRF-1231/1232 `planned`.
- Verdict: gift-for-packet "Finish shared generators through their consumers" (NSLICESQUEUE:491); the pilots need image inclusion and a served caller.

### def-keyset-check — books/def-keyset-check.lisp (342)
- Designed/implemented: Claude generators-2, 1aca6bbfc (10-02 19:08) .. 025f282cd (10-02 22:08); the pattern itself came from Codex liaison t36 retain-disjoint (033054e60->73c628005) and t38-sf-empty (3291b99d3->2a2b55b23, the sf-success mbe), which generators-2 generalised.
- Consumers: 2 — fn-sf-success-listp (books/store-files.lisp:587), fn-retain-ks-disjointp (books/retention.lisp:24); both in image (they sit inside fn-sn-statep's guard path). State: on-dev-wired.
- Tested: GEN-KEYSET `in-progress`: tests 34/34 hbox, retention 96/96 + retention-tests 91/91, store-files 194/194 (REPL); closures "to the farm next". Measured (t38): S=n 11.9 MB at 100k; COST-GATE still finds fn-owner-io's guard fn-sn-statep 99.9% of POST cost, O(N) per POST (handoff cost-gate.md).
- Verdict: keep; the O(store) guard is the open item (planning/design/sf-statep-idiom-2026-10-03.md, held for Codex's return 10-08).

### defkeystone v2 / defteeth (the teeth library) — books/defkeystone.lisp (1,008)
- Designed: Claude G3 pilot (3b7513cba, 09-27) → generators-2 "TEETH CONTRACT v1" (lanedumps/generators-2.md:529-616); Codex c04 ADOPTED; Codex c09 delta: "DOES NOT CLOSE" (liaison-11 log).
- Implemented: last 025f282cd (10-02 22:08). Codex t23b-rlfix2 part B (e43a4144a->45d462cbb) added relation teeth. Consumers: 0 book instances; 35 defkeystone + 18 defteeth forms in tests/. Not in image. State: on-dev-unwired (test-side tool; tools/keystone_emit.py / teeth_check.py mirror it).
- Tested: GEN-TEETH `in-progress`: REPL 61/61 hbox; certify-20261002T231403Z-1883604 and -232922Z-2220863 cited; gate run pending.
- Verdict: keep; c09's open items are the next step before making a missing tooth a refusal for the 3,850 hand-teethed keystones.

### def-holder — books/def-holder.lisp (1,159) + tools/holder_check.py
- Designed: Claude def-holder lane (Fable 5.1), lanedumps/def-holder.md inventory R1..; Codex c05 consultation (headline "FALSE (exhaustive); liveness UNSAFE as stated"), pasted and fact-checked; design revised after it (d057f605c "def-holder after consultation c05").
- Implemented: fea38c4f5 (10-02 18:32) .. 09df08b63 (10-02 19:22); merged Batch BM 006d441ae (lane/def-holder-core). Consumers: fn-pio-file-holds (books/page-read-direct.lisp:334; in image; host/native/extent.lisp threads ACL2's issued/holds tables, aac4c47b0) and fn-handle-holds (books/handle-holds.lisp:96; NOT in image; ARENA-FORGET's precondition). State: on-dev-wired for the cold-read file holder; on-dev-unwired for payload handles; lane/def-holder 297e4f700 (on lane/arena-forget) branch-only.
- Tested: PRF-1239 `planned`; certify run-20261003T021008Z-02fb and natives wt-20261003T020633Z "NOT harvested" (handoff def-holder.md).
- Verdict: keep-and-wire handle-holds with ARENA-FORGET.

### def-command (the `def-nntp-command` served columns) — books/protocol-served.lisp (537) + protocol-served-table.lisp (957) + tools/protocol_emit.py
- Designed: Claude def-command lane (Fable) over planning/design/command-view-policy-2026-10-03.md; Codex c07 rulings ADOPTED in full ("by-id: pin first then completed").
- Implemented: DC01 89fd70b84 (10-02 18:52) .. 3a1cb355d (Claude); DC02 the switch — 49eea4a24 (10-03 02:45, Codex era-2 served deputy, "Switch served caller to generated command dispatcher"): books/served-catalog-chain.lisp:249-257 `fn-scr-command` now calls generated `fn-proto-archive-command-cat`; later Codex rows: LIST/NEWGROUPS 5d2626619, NEWNEWS 5d56c2e7f/8be10e440, HDR/XHDR a79eca8fe, availability split c1df2e9a4 (books/served-available-commands.lisp:273). Table: 31 served rows (CAPABILITIES..XFNCATCHUP); protocol-served.lisp:367 "The generated executable has no hand catalog-dispatch fallback". tools/view_policy_debt.json: 10 debt rows (ARTICLE/HEAD/BODY/STAT ... pinned->pin-or-completed PRF-1238).
- State: on-dev-wired (served catalog path; host reaches it through fn-served-step / fn-scr-ocfg-read-span, host/owner-host.lisp:4121).
- Tested: PRF-1236 `uncertified-at-current-digest`; PRF-1287 (LIST available boundary) `planned`. DC03-DC05 items open.
- Verdict: keep; DC04 (generate fn-nntp-archive-pinned-arms) and the PRF-1238 debt are the remainder.

### def-entry — prose + two pieces (def-carried-writer, def-cost)
- Designed: Claude def-entry lane (Fable deputy), planning/handoff-2026-10-03/def-entry.md (one declaration per host-called entry: interfaces row, preservation, writes, effects, cost, witness, bench); Codex c06 ADOPTED.
- Implemented: no `def-entry` macro on dev. Its pieces: def-carried-writer (above), def-cost (below). Liaison review of c1d69fb6a: LAND; MUST-FIX pre-existing definterface `fn-di-defined-conjuncts` dropped predefined-headed conjuncts (X06 → 87ea28674).
- State: prose-only for the umbrella macro. Verdict: gift-for-packet (DE-R2 / "Finish shared generators").

### def-cost (+ def-cost-check, def-operation-check) — books/def-cost.lisp (807), tools/cost_obligations.py
- Designed: Claude def-entry round two (68cc745fa, 10-02 22:31; "a cost is derived, never declared; an unknown callee is UNACCOUNTED, never zero"), from c04/c06 rulings.
- Implemented further by Codex era-2 Sol foundations: host/cost-host.lisp (5f8337b4f 10-03 02:36: fn-reader-chunk row with route :served, visits (+ 1 request-octets), unaccounted fn-served-step fn-reader-install-result; syncer rows), books/string-line-cursor-cost.lisp (d129d4187 10-03 07:11, cons dimension). Consumers: 11 def-cost forms in 2 files (cost-host 7, string-line-cursor-cost 4). host/cost-host.lisp ld by build.lisp:427; def-cost in image. State: on-dev-wired as a checked readout (cost rows asserted at image build); not an admission tariff (cost-host.lisp:1-4 "Partial means unknown, never an admission tariff").
- Tested: LANEDUMP:111 "both roots certified in certify-20261003T055532Z-754160"; PRF-1274 `uncertified-at-current-digest`. DE-R2 `in-progress`.
- Verdict: keep; the served operation tariff (RESOURCE-OPERATIONS) is not built.

### definterface :operation — books/definterface.lisp (804) :bad-operation check at :255
- Designed/implemented: Codex era-2 Sol foundations, 5f8337b4f (10-03 02:36). One instance: fn-ros-issue (host/interfaces.lisp:38-44: stage/funding fn-ros-install-syncer/tariff/draw/physical/outcome/retention/coverage/unaccounted).
- State: on-dev-wired for the owner syncer's worker custody only. Store design's "definterface :operation charging every entry" (D41) is otherwise unbuilt.
- Verdict: gift-for-packet ST6 (resource ledger).

### def-cursor / def-cursor/output / def-cursor/batch — books/def-cursor.lisp (153), def-cursor-batch.lisp (96)
- Designed: generator named by Claude (GEN-CURSOR: "the resumable-continuation generator ... instances fn-nnw and OVER's fn-ovw"; Astra decision: metadata NEWNEWS first); implemented by Codex era-2 served deputy.
- Implemented: 52478dfea (10-03 02:41) .. f6361a46f (10-03 11:56). Consumers: fn-nnw-meta (books/newnews-metadata-cursor.lisp:182), fn-lst (books/list-metadata-cursor.lisp:155), fn-nnw-stream /output (books/newnews-stream-cursor.lisp:191) and /batch (:535). All in image closure; books/served-plan-cursor.lisp:152 calls fn-nnw-stream-batch (fn-splan-rest-cursor-step, host-called via fnn-owner-cursor-step per PRF-1256). State: on-dev-wired for NEWNEWS; LIST via fn-proto-archive-command-available-cat with PRF-1287 `planned`.
- Tested: PRF-1256 `uncertified-at-current-digest`; batch REPL ".28 ACL2s/27,319 steps" (LANEDUMP:2581). The committed fn-cur-split mbe (books/def-cursor.lisp:17-31, `:verify-guards nil`) is recorded as "UNVERIFIED WIP" (LANEDUMP:3111).
- Verdict: keep; finish guards; OVER/HDR/XPAT instances owed (GEN-CURSOR).

### def-section — host/native/owner.lisp:2594 (macro), decisions in books/failure-scope.lisp
- Designed/implemented: Claude FAILURE-SCOPE (Fable) "WRAPPER step 0", d39bf9a4a (10-02 23:54); ACL2 refuses a bad declaration at load (fn-fs-section-declp). PRF-1251 `planned`.
- Consumers: 6 sections (owner.lisp:2602-2632 control/command/bp/connection/mux-finish; web-host.lisp:130). On-dev-wired.
- Verdict: keep.

### def-actor — host/native/owner.lisp:1748
- Designed/implemented: Codex era-2 runtime deputy, 3bda776c6 (10-03 02:07 "Retain actor custody until confirmed physical join"), on failure-scope's fn-fs-actor-step. 12 starters: owner.lisp:1755-1756, 6863-6864, 8064-8066; mux.lisp:1650; feed-service.lisp:699; pull-service.lisp:852; web-host.lisp:908-909. On-dev-wired.
- Tested: SBCL-thread fixtures "PASS (~0.25 s)" (LANEDUMP:3963, :4010); no proof (host macro).
- Verdict: keep; host-side generator — TCB-SHRINK (planning/design/tcb-shrink-2026-10-03.md) wants its decisions in ACL2.

### def-buffer
- Named in COMPLETE-BEFORE ST1 ("def-loop + def-representation (+ def-buffer)"); no book, macro or call site on dev. prose-only.

## B. The codex-liaison channel (Opus lane driving `codex exec`, 2026-10-01 → 2026-10-02 23:12Z)

Source: planning/handoff-2026-10-03/codex-liaison.md (1,372 lines; liaisons 1-11), build/coordinator/codex-protocol.md. Model: t01-t02 gpt-6.1-sol, t03 on gpt-6-astra. Shas below are as the handoff cites them; pre-10-02 shas resolved through planning/commit-map-20261002.txt (old->new). Ended by "CODEX USAGE LIMIT HIT (2026-10-02 23:12Z) ... Oct 8th" (handoff line ~1343).

Tasks (t = implementation; all on dev unless noted):
- t01 secrets redaction 9308518e4->6a4d74d28 (+afb3659d0); t02 registry beec02488->ad551334e, e927ef872->9d3121dd2; t03 cites 9d6f62ce6..069091883 (spec_cite 7/15 corrected, 7 left OPEN); t04 tools/evidence_size_check.py ed9730ac4->5ece09ef1; t05 spec_cite macro defs f4c64ae40->0cc03821a; t06 test moves 48b713d0e->ef26e2487; t07 next-id 3ac3f7757->ed82c5cde; t08 umbrella drift report (world.py --check 0 after stage 0); t10 genfix 2f02804ad->73423e079; t11 pagefix 21bfc0cfb->a5f339df5; t12 dcfix 0b8a3046f->bc2f30fd3; t13 program-gone 39d26761e->96b4bf1ea (21 stale :program names); t14 dcfix2 STOPPED; t14b dcfix3 04299d899->22a837287; t15 msgidfix 7685be9ec->227830030; t16 figure-docs 45e62e2de (D47 counts block; A-SBCL-INTERNALS moved to parked trust note); t17/t18/t21/t25 def-loop (A above); t19 reach dispositions (reach --strict 96->0); t20 reach-export b5af31929; t22 genfix2 8e39d3776 (not in commit map/dev: UNCHECKABLE); t23b rlfix2 e43a4144a->45d462cbb, 5767da6c8->35e63887c (fn-rl-install-correspondence); t24 reachfix 05082e7e7->3ee25e252; t26 tools/hint_names_check.py ed8cb2eb8->275220ed6; t27 genscan 51ac84e00->6c565f559 (ledger.generated_expansion); t28 declare (32 host-dispatch declarations; rerun as codex-declare2 520bad201, which dropped them because stage 0 declared the same 30); t29b reachseed 7c0bec092->32d2effa5; t30 danglefix BLOCKED; t31 scpfix 639f456bc->bf434f362; t32 imageid 90342fc47->36d1d2018; t33 backfill e346744e8->d516d857e; t34 testiso d660b3d39->1bba0766b; t35 bpprofile 438cd78b2->1a8ac7f21; t36 retain-disjoint 033054e60->73c628005, d874158f0->17159fe4d; t37 retain-noalloc (outcome not recorded in the handoff: UNCHECKABLE); t38 sf-empty 3291b99d3->2a2b55b23 (fn-sf-success-listp O(S+n)); t39 rewrite-dangling 92b258739 (10 commits, evidence_store EvidenceConflict); t40 log-cut coverage 80839588a (fnn-log-at validation; native_program_check "13 cuts; 7 segment cuts"); t42 DATE reads current observation 0bcd9a338 (affected-root certify 671/80 red, repaired 0bcd9a338; recert 59/20, X07b open); t43 close-fence 459a7fc4a (ambiguous extent close fences the owner); t44 ibra-timeout ef08768cb (certify 157/0); t41/t45 never run by Codex (t41 → Claude LOCK-CHECK lane; t45 brief → Claude FAILURE-SCOPE, whose books/failure-scope.lisp commits carry the "t45:" prefix, 674c20d59).
- Reviews r01..r72 (~72): READY reviews of served-certify, def-carried, recovery-refinement, msgid-linear-hash, resource-ledger, generators, page-word, figure-and-contract, paged-catalog 1-8, gate-b 1-3, raw-dispatch 1-3 (+trap), stage-0 pre-READY/deltas (r31, r41, r45, r52, r55), served-incremental 1-5, evidence-out 1-4, assurance-remainder 1-5, sf-success, cold-read (r64); standing reviews r70 (repo hygiene, 13 raised), r71 (owner.lisp + mux.lisp, 16 raised; routed to HOST-LIFECYCLE, FAILURE-SCOPE, COST-GATE, DEF-HOLDER, DEF-ENTRY, GENERATORS), r72 (io.lisp + extent.lisp, 11 raised, 9 new). The log records rejected=0 on essentially every review.
- Consultations c01 list-view (planning/design/list-view-2026-10-02.md), c02 unlanded-branch triage (build/coordinator/unlanded-triage-2026-10-02.md), c03 group-count-after-reclaim (option 2', AGREED), c04 generators-2, c05 def-holder, c06 def-entry, c07 command-view policy, c08 arena-forget (two new rows: deferred reclaim leaks interned tombstone payloads; release-extents swallows close errors), c09 teeth contract ("DOES NOT CLOSE"), c10 BP node rebind ("SAFE IF reclaim excludes live BP dependencies — NOT today"); w01 whole-system answer (planning/design/whole-system-correctness-astra-2026-10-03.md, 1,675 lines, + reconciliation round 2); o01 work offer.
- State: all landed tasks are tools/tests/registry/docs or small book fixes; none are served-path mechanisms except t40/t42/t43 (host), t38/t36 (guard :exec arms in store-files/retention).

### D43-D47 (planning/decisions.md:1695-1730)
- D43 (ratified, ember): revert Codex's acceptance-binding record field (a6ed957ed; 341 old-arity calls) to the 11-argument record; redo later as relay-v1 subject binding in typed words.
- D44 (ratified): revert Codex's CRC-0 primary-block refusal (862a06808); RFC 9171 §4.3.1 permits CRC 0 with a BIB; dtn7-rs interop.
- D45 (ratified): KEEP Codex's FN-RCL2 145-octet tombstone (books/reclaim-tombstone.lisp) as the single format.
- D46 (coordinator): revert Codex's FNCE v2/v3/v4 consumer/authority event kinds from the wire-event grammar until their producer (account adoption) exists; no certifying closure, stretched D08; Codex versions kept at 4833a5ddc, 0778994b1, 1bf2ddcaf.
- D47 (coordinator, lane figure-and-contract): park W9's obligation view fn-rov (books/retention-obligation-view.lisp), remove its install/open/rebuild maintenance and its 546,341,504-octet small-profile figure term (no served reader).

## C. Stage 0 (Claude Fable, lane/stage-0, merged 7746341fc Batch BK 10-01 21:03; regen 6eb7d166a)
What it reverted of Codex era 1, with dev shas:
- 609473ad4 + 06bf2677a: acceptance-binding record field reverted (D43).
- ef55ef010 "the served path serves again (the eight breaks, host)": (1) runtime bootstrap gate removed from fn-native-entry/xl-toplevel/image-prepare, five runtime-* host files unloaded; (2) page pool: every open enters the pool's :offline context (fn-owner-page-read-open-context / fnn-extent-pool-open-context), funded install deferred to stage 6; (3) fnn-mux-queue/-queue-plan/-flush outgoing-window gates removed; (4) fnn-owner-response-unpin restored to the 25d0bf7f4 body; (5) POST precheck → baseline fnn-octets-fill + fn-owner-existing-action-buffer, fnn-owner-pic-* runtime removed, tests/test_native_captured_attempt.py removed; (6) host/native/auth.lisp, login-bindings.lisp back to cbd530797; (7) reconfigure preflight back to fn-cca-preflight; (8) cold reads :direct per-miss thread (fnn-owner-cold-line-direct). Also: report-writer enter/leave dispatch removed from the reclaim swap; receiver-turn/index-connection host block parked in host/native/receiver-turn-parked.lisp; CRC-0 accepted again (862a06808 reverted, D44); six :raw-guarded bootstrap routes dropped.
- 9b1f44c09: captured-identity chain and index-connection close parked.
- 04ff9b99b, c95a8dbc6, 7a03074a1, 6d83edad9: FNCE consumer-authority kinds reverted; account-adoption host chain out of the image build; five account-adoption entry declarations withdrawn (D46).
- 5d430657a: "deleted runtime parked, not lost". 7d4462641 stage-0-4: live reconfiguration completes by fn-oclc-publish; S9 prose + counted-drain witnesses (retire producer fence itself not restored here; COMPLETE-BEFORE L2).
- Native: "s0p 12/13 at 610182be4, over_pins known defect" (merge subject 7746341fc).
- Follow-on (Claude cold-read-ownership, 39f3ed4eb..07c0db851, merged 0dce73ae5): the unfunded cold line pins its file generation and runs on 4 bounded workers (PRF-1234), replacing stage 0's per-miss thread.
