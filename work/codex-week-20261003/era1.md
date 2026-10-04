# Era 1 (Codex root 01a0eeec, 2026-09-29 20:50 -> 10-01): state of every family at d4e53323c

Coordinates. The 10-02 history rewrite remapped every pre-10-02 sha
(`planning/commit-map-20261002.txt`): Claude's handoff 7aad444ce = **cbd530797**,
era-1 end b34835bd4 = **87cb67a2e**, 1bf2ddcaf = a6ed957ed, 35c51c706 = 25d0bf7f4,
f32c7d4db = 49d3bd846. Old shas below are given as the documents cite them; new
ones are resolvable on origin/dev. `git rev-list --count cbd530797..87cb67a2e` = 768.

Method. File trees via `git ls-tree` at cbd530797 / 87cb67a2e / d4e53323c; image
membership = transitive `include-book` closure of `books/image-world*.lisp`
(script `py/closure.py`, results `clos-*.json`, `era1-image.json`); host loading =
`host/native/build.lisp` at d4e (`build-d4e.lisp`); wiring = `git grep` of the entry
symbol in `host/` at d4e; PRF status = snapshot `planning/proofs.json`. Family
assignment of the 678 new books by name prefix (`py/fam.py`, `era1-assigned.json`),
matching the critic's F01-F12 (`build/coordinator/codex-era-architecture-review-2026-10-01.md`, "critic" below). Nothing built or run.

## 0. Aggregate numbers

| | at 7aad (cbd530797) | at era-1 end (87cb67a2e) | at d4e53323c |
|---|---|---|---|
| books/*.lisp | 967 | 1,645 (+678 era 1) | 1,805 |
| era-1 books still in tree | - | 678 (115,914 lines per critic) | **675** (115,840 lines) |
| era-1 books in an image-world closure | - | 184 (26.6k lines) | **198** (28.2k lines) |
| host/*.lisp new in era 1 | - | 104 | **97** survive (7 deleted) |
| era-1 test files | - | 466 (349 tests/acl2) | 465 survive |
| era-1 tools files | - | 33 | 33 survive |

Deleted era-1 books (3): `held-record-shape`, `index-reader-render-establishment-tests`,
`reader-output-storage-tests` (moved to tests/acl2/, Makefile:185). Deleted host (7):
`host/native/{recovery-profile-read,runtime-construction-recipe,runtime-recovery-file,runtime-u64-request-source}.lisp`,
`host/{recovery-source-host,snapshot-initial-constructor-host,snapshot-initial-root-host}.lisp`.
Left the image since era 1 (10): acceptance-binding, acceptance-binding-injection,
consumer-account-binding-codec, consumer-transaction-dispatch, held-composite-fields,
held-record-shape, obligation-view-budget, retention-obligation-view, view-delta,
view-delta-concrete. Entered the image (24, all via other books, mostly era 2):
allocation-epoch-{pool,observation,collection-request}, allocation-turn-slots,
decoded-window-{begin,lease,read}, decoded-worker-controller, extent-window-compressed,
history-semantic-writer-state, nov-{byte,decimal,piece,span}-window, operation-diagnostics,
page-window-worker-storage, recovery-profile-{buffer,envelope}, recovery-prs-install,
runtime-bootstrap-turn-installation, tcpcl-{received-count,received-source,segment-source-cursor,source-continuation}.

So the critic's L3 "PARK-THE-CODEX-PILES" (move out of image, delete ~40k lines) was
**not executed**: residue is still in the tree; parking happened at the HOST layer
(`planning/host-parked.json`, 82 files, owner "L3") and by stage-0 reverts.

Per family (books / lines at d4e / in image at d4e / in image at era-1 end):

| family | books | lines | img d4e | img b34 |
|---|---|---|---|---|
| F01 post identity | 46 | 15,905 | 4 | 6 |
| F02 cold read / pool / windows | 77 | 13,244 | 36 | 30 |
| F03 index / receiver / extractions | 80 | 11,696 | 9 | 9 |
| F04 parser / NOV / subject / group number | 28 | 6,695 | 6 | 4 |
| F05 OVER / views / reports | 28 | 7,257 | 8 | 9 |
| F06 accounts / statements | 86 | 11,591 | 28 | 30 |
| F07 FNCR / 9P | 49 | 5,398 | 11 | 11 |
| F08 BP / TCPCL / substrate / peer | 80 | 11,302 | 13 | 9 |
| F09 history / digest | 63 | 15,421 | 7 | 6 |
| F10 snapshot / recovery / moved owner | 52 | 7,272 | 14 | 13 |
| F11 runtime / allocation | 21 | 2,680 | 16 | 11 |
| F12 owner glue (TLS/retire/feeds) | 16 | 3,740 | 16 | 16 |
| other (owner/catalog/consumer accessors) | 50 | 3,639 | 30 | 30 |

PRF ids in the era-1 range 1030-1200 (proofs.json at d4e): certified 6 (PRF-1057, 1059,
1061, 1067, 1080, 1190), uncertified-at-current-digest 48, planned 44. PRF-1052/1053/1054,
1108, 1126/1127 are absent from proofs.json.

Stage 0 (Claude Fable, lane/stage-0 9452565bc, merged to dev 7746341fc 10-01 21:03;
host breaks ef55ef010 10-01 06:17, follow-up 5d430657a 10-01 12:49) is the commit set
that reverted/parked era-1 served-path changes; D43-D46 ratify its format reverts,
D47 (codex-liaison t16, 45e62e2de -> 98c8e5bb3) parks the W9 view.

---

## 1. Store, page pool, arena, history

### 1.1 Page-read pool ownership (F02 half 1; KW-a)
- **Designed:** `build/coordinator/allocation-epoch-design-2026-09-30.md` (190 l.) and
  `specs/allocation-turns.md`; the cold read as pool-charged admission, a pool-owned
  worker, publication only for the exact issued token of a still-issued row.
- **Implemented:** `books/page-read-{pool-state 37, ledger 262, resources 159, ownership 172, executor 155}`,
  `page-discovery-ledger` 68, `cold-read-reservation` 93 (build.lisp:209), `cold-read-layout` 60;
  `host/page-read-host.lisp` (`fn-owner-page-read-open-context` :32, `-install-baseline` :62);
  `host/native/extent.lisp` `fnn-extent-pool-storage-start` :122, `fnn-extent-executor-start` :642,
  `fn-pio-complete` calls :995, :1141. Era 1 never called the installers (critic F02 "Decisive").
  **State: on-dev-wired** — installed at start by era 2: `host/native/owner.lisp:8247-8257`
  (`fn-owner-page-read-install-default`, then storage-start, executor-start), commits
  0ca006108 (10-03 12:14 "Install DEFAULT partial page pool before owner recovery"),
  162bc5cbe (10-03 12:36). The unfunded path was wired by a Claude lane first: 39f3ed4eb
  (10-01 21:41 cold-read-ownership, PRF-1234, `fnn-extent-issue-direct`), then def-holder aac4c47b0 (10-02 19:30).
- **Tested/proved:** PRF-1057 (issued cold reads retain identity through cancellation) and
  PRF-1080 (persistent cold executor owns one charged job) **certified**; PRF-1234 uncertified.
  Native: UNCHECKABLE here (no native ledger for d4e read).
- **Remaining defect:** the whole-extent malloc is unchanged (`extent.lisp:904`, `:1154`
  `make-array (+ elen 32)`), as the critic noted; that is ST2's.
- **Verdict:** keep-and-wire — done (the COMPLETE-BEFORE tag "KW-a SUPERSEDED by ST6" is stale against owner.lisp:8247).

### 1.2 Windows, stored-DEFLATE chunk, decoded window (F02 half 2)
- **Designed:** `specs/extent-window-read.md` (548 l., PRF-1109/SCN-1018), `specs/payload-window.md`
  (157 l., PRF-1112/SCN-1020: stored decode bound `256*C + 65,536`).
- **Implemented:** `extent-window-{plan 205, stream 169, compressed 162, buffer 47, capture 35}`,
  `page-window-{executor 172, lease 100, read 92, worker-storage 95}`, `payload-window` 328,
  `decoded-window-{descriptor,read,lease,begin}`, `decoded-worker-controller` 163, `page-file-lease` 115,
  `cold-read-window` 155, `cold-guard-bootstrap` 116 — all 36 F02 image books are in the d4e closure.
  Host: `host/page-window-{lease,executor}-host.lisp`, `host/page-decoded-window-host.lisp`
  (build.lisp:337-339), `host/native/extent-decoded.lisp` 179 l. **loaded** (build.lisp:459);
  served issue path `owner.lisp:5769-5800` (`fnn-owner-cold-issue-locked`, window discovery :5778,
  added 19ec62b71 10-03 09:41), executor `extent.lisp:320-413`. Era 1 staged them
  (3c27f8318 09-29 22:18, 7d5800297 09-30 00:17); era 2 connected them (81f449842 10-03 09:17,
  35d84d74b/6f5d538de/466659c52 10-03 12:28-13:16).
  **State: on-dev-wired (by era 2)**, against the critic's PARK/DELETE verdict for decoded-window.
- **Inconsistency found:** `planning/host-parked.json` still lists `host/native/extent-decoded.lisp`
  as parked ("F02 decoded window (L3: DELETE)") while build.lisp:459 loads it; the shrink-only
  KNOWN list should be red on that entry (not run here).
- **Tested/proved:** PRF-1109, PRF-1112 planned. The 22 `decoded-window-*` trajectory books prove
  agreement with the logical decoder `fn-pzd-decode`, not the host-called one (critic F02 Residue).
- **Verdict:** now an era-2 subject; harvest decision belongs to the era-2 account (served-composition theorem owed: PRF-1112 "served composition open").

### 1.3 Incoming buffers (F02 incoming-*)
- `incoming-copy-stobj` 229, `incoming-{buffer-carrier 88, octet-holder 95, setup-ranges 143}` in image;
  host users only `host/page-read-host.lisp` and the parked `receiver-turn-parked.lisp`.
  **State: on-dev-unwired.** Verdict: gift-for-KW-b (receiver); keep `incoming-copy-stobj` as pattern.

### 1.4 Dense all-event history epoch (F09 B)
- **Designed:** `planning/dense-history-epoch-2026-09-30.md` (388 l.), `planning/dense-history-owner-producer-2026-10-01.md`
  (285 l.), `planning/history-provider-stable-addresses-2026-10-01.md` (105 l.), `specs/history-event-directory.md`,
  `specs/history-source-custody.md`. Idea: an append-only epoch of 256-reference pages in a persistent
  binomial forest with low-bit-first stable addresses and capture custody; once-only publication with a canonical-epoch check.
- **Implemented:** `history-event-{page,directory,directory-refinement,provider 86,backing}` out of image;
  `history-capture-custody` 205, `history-capture-state` 76, `history-semantic-writer` 29 (+ `-state` 20) in image.
  Host `history-{admission-producer,operation-observation,owner-completion,owner-view}-host.lisp` parked.
  The owner seam `fn-owner-history-produce-step` does not exist anywhere at d4e.
- **State: parked (D42: P3 ratified over the dense epoch, 10-01)** for the epoch; the eight owner-host
  gates are **on-dev-wired, inert**: `host/owner-host.lisp:471, 518, 539, 610, 666 ...` call
  `fn-owner-history-bootstrap-mutationp` (`books/history-semantic-writer.lisp:25`, true while no
  publication and no APR owner) / `fn-owner-history-reset-status`; introduced 89dca11b3 (09-30 20:45),
  930b3e641, beeedbf1f (09-30 23:46). The critic and L3 say REMOVE; not removed.
- **Tested/proved:** PRF-1190 (chronological persistent forest growth, exact resumable page selection) **certified**.
- **Verdict:** superseded-by-ST5 (P3, D42) for the epoch; drop the eight gates; keep the forest-address idea as design input.

### 1.5 Checkpoint writer library (F09 A)
- **Designed:** `planning/history-page-cursor-contract.md` (319), `planning/history-decode-contract.md` (181),
  `planning/page-digest-cursor-contract.md` (166, PRF-1087), `planning/checkpoint-reference-cursor-2026-09-30.md` (156),
  `planning/checkpoint-payload-lifetime-contract-2026-09-30.md` (141), `specs/history-{record,scalar}-cursor.md`,
  `specs/history-decode-completion-source.md`, `specs/history-auth-reader.md`. Idea: census-then-emit,
  bounded-step checkpoint writing with a resumable BLAKE3 machine (57-frame bound) and size sidecars.
- **Implemented:** `history-scalar-cursor`, `history-record-cursor`, `history-decode-*`, `history-page-cursor/-reader`
  out of image; `pagestore-digest-cursor` 230, `pagestore-digest-byte-cursor` 79, `store-tree-size` 160 in image.
  No host reference to `pgs-dc-`, `fn-hrsc-`, `fn-hrcur-` at d4e. **State: on-dev-unwired** (library in tree, no caller).
- **Tested/proved:** refinements to existing codecs (critic F09: `history-scalar-cursor.lisp:209,233`,
  `history-record-cursor.lisp:712`, `pagestore-digest-cursor-progress.lisp:419`, `history-decode-refinement.lisp:787`);
  PRF-1087 planned. No composed theorem to `fn-his-snapshot`.
- **Verdict:** gift-for-ST7/P8 (online checkpoint = dirty pages): the resumable BLAKE3 cursor and record/scalar cursors are the reusable parts; the cold sub-stack (8 books, ~3.9k) and digest companions: drop.

### 1.6 Snapshot / INITIAL custody / recovery driver (F10 a-c)
- **Designed:** era-1 handoff chain "saved image -> ... -> INITIAL custody -> startup factory -> census/remap -> writer" (critic §1).
- **Implemented / state:**
  - `owner-snapshot-request` 232 + `store bless-snapshot` (`host/native/operator.lisp:701-702`): **on-dev-wired**; PRF-1050 now **planned** (critic read it certified).
  - `owner-snapshot-recovery` 1,708 l. in image: **on-dev-wired** (reaches served code through `owner-cursor-domain`); no PRF certified for it in range.
  - snapshot natives `host/native/snapshot-{startup,producer,initial-reader}.lisp`, `recovery-payload-view.lisp`, host `recovery-initial-*`, `recovery-payload-view-*`, `snapshot-initial-host`: **parked** (host-parked.json, "F10 snapshot/INITIAL").
  - `runtime-recovery-file.lisp`, `recovery-profile-read.lisp`, `recovery-source-host`, `snapshot-initial-{constructor,root}-host`: **deleted**.
  - admission census/remap (`admission-semantic-*`, 6 host files + `admission-preallocation.lisp`): **parked**; `admission-preallocation-resources` 247 in image (certifies as logic).
- **Verdict:** keep bless (done); drop the INITIAL/startup-factory natives (they call eleven undefined entries, critic F10a); census/remap: drop unless a POST-path caller is designed; `fn-asn-authority-one-is-cpr-apply-event` (admission-semantic-node.lisp:682) is a gift for config-replay work.

### 1.7 Moved owner entries and the retention carry (F10 e)
- **Implemented:** `owner-recovery-retain` 332, `owner-retain-transitions` 197, `owner-retain-state` 57,
  `owner-cursor-domain` 369, `owner-reclaim-carry` 39, `owner-obligation-state` 74 — in image, on the served start.
  **State: on-dev-wired.**
- **Tested/proved:** PRF-1067 (retention carry state boundary) **certified**; PRF-1060 (off-mutex rebuild
  constructs a valid carry) uncertified-at-current-digest; PRF-1037 (keyed catalog switch) uncertified.
- **Verdict:** keep-and-wire (certify PRF-1060/1037).

### 1.8 W9 obligation view and view-delta (F05/F10)
- `retention-obligation-view` 286, `view-delta`, `view-delta-concrete`, `obligation-view-budget`: left the image;
  no host `fn-rov-` reference. The 546,341,504-octet heap term is removed.
  **State: parked (D47, lane figure-and-contract / codex-t16 45e62e2de, merged 98c8e5bb3 10-01 21:52).**
- **Verdict:** gift-for-W9 (re-add with its reader and figure term together, per D47 Completion).

### 1.9 Acceptance-binding record field (F01)
- `books/acceptance-binding.lisp` 149 l. in tree, out of image; the 12th record field is gone from records.
  **State: reverted-by-stage-0 (D43: 341 old-arity calls broke; the binding is to be redone as the relay-v1 subject binding in typed words)** — 3327a831c, 9452565bc (10-01 20:21-20:54), merged 7746341fc.
- **Verdict:** superseded-by-KW-e (subject binding as typed words, after ST3/ST5).

### 1.10 FN-RCL2 tombstone and article subject (F04 S; KW-e)
- `article-subject` 310 l. in image; wired `host/owner-host.lisp:3076` (`fn-asj-subject` in transit decide);
  tombstone `books/reclaim-tombstone.lisp:9,30` magic NUL "FN-RCL2". **State: on-dev-wired; FN-RCL2 kept (D45).**
- Missing: the Message-ID -> original-subject conflict binding — `:subject-conflict` occurs nowhere in books/ or host/ at d4e.
- **Verdict:** keep-and-wire (KW-e open; after ST3/ST5).

### 1.11 Second paged Message-ID table / index backing (F03 index)
- **Implemented:** ~55 index books out of image except `index-query-resources` 149 and `index-writer-ticket` 14;
  9 host index files + `host/native/index-writer-turn.lisp` **parked**. `fn-owner-index-connection-start` only in
  `host/native/receiver-turn-parked.lisp:43-61`.
- **State: parked.** Branch content: `codex/*` index lanes per branch-archaeology (other scout's axis).
- **Verdict:** superseded-by-ST3/ST7 (paged catalog behind `fn-cat`; msgid-linear-hash). Seed candidates: `fn-iqr-promotion-preserves-resident-pool-total`, the `fn-ibp-node` congruent-child idea.

### 1.12 Statement recovery worker swap (F06 d; KW-i)
- `statement-recover-stream` 136 l. in image; open path `host/native/io.lisp:1780, 2970` calls `fn-ssr-rows`;
  `host/store-open-host.lisp:648` and `host/store-write-host.lisp:1114` still call `fn-srs-rows`; no theorem relates them
  (`git grep` for a defthm naming both: none). **State: on-dev-twin** (two recover workers, one theorem-less seam).
- PRF-1078 uncertified, PRF-1079 planned. **Verdict:** keep-and-wire — the ~40-line `fn-ssr-rows = fn-srs-rows` theorem, or retire one worker.

## 2. Served commands and cursors

### 2.1 OVER cursor and response pins (F05; KW-g)
- `over-window` 487 (Claude L1), `served-plan-cursor` 545 (Claude L2), `response-plan-pins` 151 (Codex, PRF-1059) — in image;
  `fn-splan-` used by mux/owner/pull-service/web-host/io. `fnn-owner-response-unpin` restored to the six-line release body
  (`host/native/owner.lisp:709-718`, stage 0 ef55ef010); the `fnn-mux-wire-source` gate removed (stage 0; zero refs at d4e).
- **State: on-dev-wired.** PRF-1059 **certified**; PRF-1020 uncertified. **Verdict:** keep (done); certify PRF-1020; L4's native pin re-run owed (UNCHECKABLE here).

### 2.2 Productive READ / transfer (F05; KW-f / W6b)
- `productive-read-chain` 1,230, `productive-transfer` 207: in tree, **out of image**, no host reference to `fn-pcr-`.
  PRF-1052/1053/1054 absent from proofs.json; inbound 1126/1127 only on lane/productive-read-transfer.
- **State: on-dev-unwired** (proof-only books over host-called `fn-mca-read-span`). **Verdict:** keep-and-wire (certify + register + specs/productive-contract.md §5; no new ACL2).

### 2.3 D25 POST-identity source cursor (F01)
- **Designed:** `specs/post-identity-source-cursor.md` (89).
- `post-identity-source-cursor*`, recipe chain, `post-identity-captured` (850), 16 `captured-*` books: out of image;
  precheck moved to `host/native/post-captured-parked.lisp` (`fnn-owner-captured-precheck-locked` :67);
  `host/post-identity-captured-host.lisp` parked. Precheck reverted by stage 0 (ef55ef010, 5d430657a).
  In image only: `poster-bytes-source` 183, `-buffer` 1,045, `post-admission-keyed` 147, `identity-hex` 16 (wired).
- **State: parked** (cursor), **reverted-by-stage-0** (precheck; ST0 break 5, not a D-row).
- PRF-1145, 1148 planned; nine books REPL-only per critic F01 (UNCHECKABLE whether any certify run has since passed).
- **Verdict:** gift-for-the-POST-cost packet (`fn-pic-run-arena` replacing `fn-rclb-same-articlep`), only after the REPL-only books certify; drop the 16 `captured-*` trace books.

### 2.4 NOV byte-budgeted formatter (F04 N)
- `nov-{byte 213, decimal 124, piece 438, span 169}-window` now inside the image closure (entered after era 1);
  no host reference to their prefixes. **State: on-dev-unwired.** **Verdict:** gift-for-OVER streaming (drain pieces into `fn-octets` inside `fn-ovw-step`).

### 2.5 Legacy parser (F04 L), group-number cursors (F04 G)
- `legacy-parser-*` (12 books) out of image, no host refs: **on-dev-unwired**. Verdict: drop, keep `fn-nlv-actual-parser-never-counter-error` (legacy-parser-validity.lisp:690) relocated.
- `group-number-trie` 62 in image (verbatim move of `fn-gnix-*`); cursors out of image. Verdict: trie keep; cursors drop.

### 2.6 Reports, reader-output (F05)
- `owner-report-capture` 117 in image (included by owner-host.lisp:28, reader-host.lisp:3); no host call of
  `fn-orc-job`/`fn-orc-register-*` at d4e (the four fence call sites are gone). **State: on-dev-unwired.**
  `reader-output-job`/`-storage` in tree, out of image: **on-dev-unwired**. `planning/report-capture-invalidation-2026-10-01.md` (140): prose-only design.
- `web-health` 60: **on-dev-wired** (web face; see §6).
- Verdict: drop reader-output (second reply buffer); report capture: gift-for-operator-status if a reader is written; prefix `fn-orc-` collides with owner-reclaim.

## 3. Resource accounting

### 3.1 Runtime bootstrap, compiled operation table (F11)
- **Designed:** `specs/runtime-operation-compiled-source.md` (9 l.), `specs/allocation-epoch.md` (13 l.).
- `runtime-bootstrap-*`, `runtime-operation-*` books: 16 F11 books in image (`runtime-operation-compiled-table` 21 l., value nil).
  Gate removed: `host/native/build.lisp:500-508` comment, `tools/extract/core-main.lisp:30-33` comment (stage 0 ef55ef010).
  Natives `host/native/runtime-{bootstrap,collector,construction-inventory,image-policy,participants,profile-envelope}.lisp` **parked**;
  `runtime-construction-recipe`, `runtime-recovery-file`, `runtime-u64-request-source` **deleted**.
  `runtime-collector.lisp` (SBCL finalizer-thread hook) not loaded.
- **State: reverted-by-stage-0** (ST0 break 1, not a D-row: "no gate before its producer", MODE 2026-10-01 rule 3).
- **Verdict:** drop (critic F11 DELETE; L3 not executed: books still in image).

### 3.2 Allocation epoch and once-only turns (F11)
- **Designed:** `build/coordinator/allocation-epoch-design-2026-09-30.md`, `specs/allocation-turns.md` (173, HST-042).
  Idea: prepay a source-derived Qgate at entry and Qbody before the body; A never decreases until a quiescent collection resets it; `f*(L0+A)+reserves <= budget`.
- `allocation-epoch` 341 (+ `-pool` 147, `-domain`, `-observation`, `-collection-request`), `allocation-turn-slots` 446 in image;
  `host/allocation-epoch-host.lisp` **parked**; `fn-aec-` has no other host user; `fn-ats-` used only by parked account/index host files.
  The control-turn wrapper `fnn-owner-serialized-with-control-turn` (`owner.lisp:2937`) refuses `:owner-control-unavailable`
  when no binding; `fnn-owner-control-binding-make` (`host/native/owner-control-turn.lisp:9`) has no caller; its one live caller
  `fnn-control-live-status-answer` (control.lisp:222-228) falls back to the legacy answer when the inspector binding is nil.
- **State: on-dev-unwired** (in image, no producer). PRF-1156/1157 **planned** (critic read them certified at 87cb67a2e; not at d4e).
- **Verdict:** superseded-by-ST6 (resource-ledger; `specs/resource-vector.md` 877c69598, Claude, 10-01). Branches `codex/allocation-epoch`, `codex/allocation-turns`, `codex/collector-core-join` are MINE-B in branch-archaeology (other scout).

### 3.3 Heap figure / W9 reserve — see 1.8 (removed, D47). `cold-read-reservation` (build.lisp:209): on-dev-wired.

## 4. Owner lifecycle

### 4.1 Retire (F12; KW-h = S9)
- `owner-retire-{settlement 113, cursor 111, counted 59}`, `native-retire` 245, `owner-retire` 171 in image.
  `host/owner-host.lisp:1831-1836`: `(fn-ort-drain-step-counted s0 s seconds (fn-owner-feed-pending state) t nil)` with comment
  "The native accepted-producer/barrier settlement observation is still OPEN". **State: on-dev-wired, defect open** (every retire ends `:deadline`; critic F12, L2).
- **Verdict:** keep-and-wire (producer fence, ~40-60 lines; restore final checkpoint).

### 4.2 Carried feed counts (F12; KW-c)
- `owner-feed-counts` 152, `feed-live-carried` 528, `owner-feed-live-carried` 145, `owner-feed-reconfigure-counted` 166,
  `peer-feed-counts` 329, `owner-outcome-counted` 338 in image; wired (`fn-ofct-/fn-oct-` in owner.lisp, extent.lisp, owner-host.lisp).
  Only per-put deltas proved (`books/owner-feed-counts.lisp:37-75`); no whole-owner invariant. **State: on-dev-wired, invariant open.**
- **Verdict:** keep-and-wire (L11, def-carried instance).

### 4.3 Owner extractions (F03)
- `owner-connection-state` 68, `owner-submission-record` 163, `owner-resource-line` 63, `connection-read-quantum` 27 in image, wired.
  `host/owner-connection-callbacks.lisp`, `owner-exposure-host`, `owner-report-writer-host`, `payload-view-host`, `query-*-host`,
  `store-checkpoint-context-host` **parked** ("F03/F10 owner extractions of the modern-owner join, unwired").
- **Verdict:** keep, certify.

### 4.4 Receiver window / turn (F03; KW-b)
- **Designed:** `specs/connection-receiver-source.md` (28).
- `receiver-provider` 166, `receiver-turn-controller` 759 in image; natives `host/native/receiver-turn-parked.lisp` and 6 receiver host files **parked**;
  production fill is still `fnn-octets-fill` (`owner.lisp:473`). `host/runtime-receiver-source-host.lisp:8` stub parked.
- **State: parked.** **Verdict:** keep-and-wire later (KW-b, after ST6), keystones at receiver-turn-controller.lisp:590/644/661 are the asset.

## 5. BP / TCPCL / peer

| item | file (lines @d4e) | state | proof | verdict |
|---|---|---|---|---|
| Listener/control machine (KW-d) | `bp-node-listener-control` 325, `bp-node-control` 162; `host/native/bp-listener-control.lisp:83`, called `bp-node.lisp:1146` | on-dev-wired | PRF-1063/1064/1075/1076 uncertified | keep-and-wire (certify) |
| Recovery profile recheck | `bp-recovery-profile` 138, `-guards` 234 (build.lisp:297-298); `fn-bprpf-` in bp-service.lisp | on-dev-wired | family-bound fix: not checked (UNCHECKABLE without reading `fn-bprpf-row-admit` history) | keep (fix bound) |
| CRC-0 primary refusal | (was bp-node.lisp:425-427) no `:block-unintelligible` in books/bp-*.lisp at d4e | reverted-by-stage-0 (D44: RFC 9171 §4.3.1 permits CRC 0 with a BIB; dtn7-rs interop) | - | done |
| TCPCL received source | `tcpcl-received-source` 122, `-count` 23, `tcpcl-segment-source-cursor` 81, `tcpcl-source-continuation` 17 (entered image); `host/native/bp-session.lisp:101-128`, `fnn-tcl-deliver-transfer` :384 | on-dev-wired (by era 2, 3f493c37b 10-03 08:42 "S068") | - | keep |
| BPSec ASB cursor, crypto | `bpsec*` books out of image; `host/native/bpsec-crypto.lisp` parked | parked | no decision registers RFC 9172 | gift-for-a-BPSec-decision; else drop |
| BP controller/digest/received/wire | 2 host files parked; books out of image | parked | received/wire zero theorems | drop received/wire; park controller |
| Substrate v2 commit codec | out of image | on-dev-unwired | `tests/acl2/substrate-commit-codec-gap-tests.lisp` (586-octet baseline defect witness) | keep the defect witness; one codec first |
| Peer adoption / invite retry | `peer-invite-retry` 244, `peer-adoption-receipt-rows` 61 in image; `host/native/peer-invite.lisp` | on-dev-wired | - | keep (done) |

## 6. Web face
- Era 1 added only `web-health` (60 l., wired via web-host; keystone, <= 23-octet body): **on-dev-wired**.
  Claude S11 web READYs (3e8824bf8, d104ea268) never merged (COMPLETE-BEFORE §0.1). Verdict: keep.

## 7. Operator / control / journal
- `store bless-snapshot` (§1.6): on-dev-wired. Offline verb `statement-sign` (`host/native/signature-command.lisp`): on-dev-wired; book certification UNCHECKABLE here.
- `planning/control-body-ticket-transport-2026-10-01.md` (173 l.; carry the ATS receipt through the live control callback): **prose-only** (its producer, the control binding, has no caller).
- Report capture (§2.6): on-dev-unwired.
- `planning/public-node-candidate-preservation-2026-10-01.md` (18 l.): read-only observation of the live node (a3553e6b at /opt/fn-a3553e6b4a23, 10-01 02:27 UTC) + a pre-deploy checklist: prose-only.

## 8. Accounts / auth (F06)
- **Designed:** `planning/typed-c-writer-lease-2026-10-01.md` (204), `specs/consumer-account-{binding-stage,config-commit}.md`,
  `planning/consumer-mature-completion-map-2026-09-30.md` (88).
- Native auth callers reverted to the legacy install (`host/native/auth.lisp` 120 l.; header :6-8 notes the parked path);
  `fnn-native-auth-adopt-config` lives in `host/native/auth-adoption-parked.lisp:17`; `host/native/account-adoption.lisp` and
  18 account host files **parked**. FNCE v2/v3/v4 grammar **reverted-by-stage-0 (D46: no certifying closure, no producer, stretches D08)**.
  Reconfigure preflight replaced by `fn-cca-preflight` (`host/owner-host.lisp:1355-1372`, stage 0).
- Logical core: 28 F06 books in image (`consumer-account-{adoption 425, carried 386, index-carry 291, relation 282, ...}`,
  `consumer-authority-codec` 413) — certify as logic, no served host line (D46 text).
- Wired keepers: `auth-credentials` 183, `control-visible-effect` 282, `native-statement-material` 54, `consumer-position-fields` 14.
- PRF-1140 planned. **Verdict:** park the core (gift-for-the account-adoption continuation named in D46 Completion); drop the stubs (`account-adoption-operation-source`, `account-preparation-admission-host`).

## 9. Consumers (FNCR) and 9P (F07)
- FNCR: 11 core books in image (build.lisp:328-332); `host/consumer-remote-host.lisp` ld (build.lisp:386); `host/native/consumer-remote.lisp`
  loaded (build.lisp:554; last touched d39bf9a4a 10-02 def-section). Its entries (`fnn-remote-receive`, `-ingress`, `-installed-entry`,
  `-receive-installed`) have **no caller** outside the file; nothing in mux/owner/tls dispatches FNCR. `consumer-remote-reader-host`, `-report-host` parked.
  **State: on-dev-unwired** (loaded, not dispatched). PKT-673 decision (2026-09-29) mandates the capability. Verdict: gift-for-Q13 (protocol design + ingress/dispatch theorems are reusable; rebuild poll/wait on the local scanner).
- 9P: books out of image/Makefile roots? (not re-checked line by line); `host/native/ninep.lisp` and 6 ninep host files **parked**. PRF-1177, 1196 planned.
  Verdict: parked; `ninep-fields` is a model bounded parser (critic F07).

## 10. Generators and macros
- Era 1 built no generator. The reusable technique the critic names is "model byte-run equals paid-step trace"
  (`fn-psc-model-byte-run`, post-identity books) — prose-level lineage only; whether def-cost/def-cursor (era 2) descend from
  `specs/runtime-operation-compiled-source.md`'s per-operation cost table is UNCHECKABLE without the era-2 transcripts.

## 11. Proof engineering and tooling
- New tools (33, all present at d4e): `tools/book_navigator.py` 384, `tools/extract/{entry_preflight 199, bound_launch 233, owner 207, bind_package 95, world_binding 57, core_launcher 46}.py`,
  `tools/extract/world-dtn.lisp` 371, `tools/operation_source_driver.py` 118, `tools/bpsec_*source_observation.py`, and `tools/resilience/` (14 files incl. adapters
  `page_io` 218, `reclaim_hold` 223, `response_holds` 159, `typed_window*`; W7 framework is Claude's b344e9fa8 design of 09-29, adapters landed in the era-1 window).
  Wiring into `make check`: not checked (UNCHECKABLE cheaply). `typed_window` scenarios target parked code (COMPLETE-BEFORE L3).
- REPL replays (pc27-pc39) stand in for certify runs on nine D25 books (critic F01).
- `planning/slice-execution-2026-09-30.md` (380 l.): Codex's process doc ("completing whole slices"): prose-only.

## 12. Tests
- 466 era-1 test files, 465 present at d4e (349 tests/acl2, 83 tests/*.py, 12 tests/native). Notable: `tests/test_native_account_adoption_transport.py:275-320`
  pinned the refusal (critic F06); `tests/test_native_over_pins.py:136,161` (status=released) — runnable again after stage 0's unpin (native verdict UNCHECKABLE here).

## 13. Era-1 designs written by Codex (verified by adding commit inside cbd530797..87cb67a2e)

| doc | lines | idea | state |
|---|---|---|---|
| planning/dense-history-epoch-2026-09-30.md | 388 | 256-ref event pages in a binomial forest, capture custody, in-memory | superseded (D42, P3) |
| planning/dense-history-owner-producer-2026-10-01.md | 285 | the missing owner seam: one semantic decision, late file completion | prose-only (no `fn-owner-history-produce-step`) |
| planning/history-provider-stable-addresses-2026-10-01.md | 105 | low-bit-first addressing must survive root growth | implemented in provider (out of image); PRF-1190 certified |
| planning/history-page-cursor-contract.md | 319 | resumable image preparation with captured store pointer + leases | library unwired |
| planning/history-decode-contract.md | 181 | bounded current-format decode, borrowed roots | library unwired |
| planning/page-digest-cursor-contract.md | 166 | resumable BLAKE3 over page words (PRF-1087) | library in image, no caller |
| planning/checkpoint-reference-cursor-2026-09-30.md | 156 | bounded schema-3 checkpoint writer preserving exact bytes | prose + unwired books |
| planning/checkpoint-payload-lifetime-contract-2026-09-30.md | 141 | payload lifetime through checkpoint | prose-only |
| planning/report-capture-invalidation-2026-10-01.md | 140 | one registered report job, sticky invalidation | book in image, no caller |
| planning/control-body-ticket-transport-2026-10-01.md | 173 | ATS receipt carried through live control callback | prose-only |
| planning/typed-c-writer-lease-2026-10-01.md | 204 | config lease on the semantic-source slot | parked with F06 |
| planning/consumer-mature-completion-map-2026-09-30.md | 88 | what a consumer user still cannot do | prose-only |
| planning/public-node-candidate-preservation-2026-10-01.md | 18 | live-node observation + deploy prerequisites | prose-only |
| planning/slice-execution-2026-09-30.md | 380 | process (whole slices) | prose-only |
| planning/review-2026-09-29-gpt6-decisions.md, review-2026-09-30-gpt6-log2.md | 224, 38 | GPT-6 review records | prose-only |
| build/coordinator/allocation-epoch-design-2026-09-30.md | 190 | prepaid allocation epoch + quiescent GC barrier | parked / superseded-by-ST6 |
| specs/allocation-turns.md, allocation-epoch.md, runtime-operation-compiled-source.md | 173, 13, 9 | turn slots; epoch; compiled table | books in image, no producer |
| specs/extent-window-read.md, payload-window.md | 548, 157 | protected windows; stored-DEFLATE window bound | wired by era 2 (PRF-1109/1112 planned) |
| specs/post-identity-source-cursor.md | 89 | 24-slot D25 inverse cursor | parked |
| specs/history-{record-cursor,scalar-cursor,event-directory,source-custody,auth-reader,decode-completion-source}.md | 326/60/96/60/84/21 | checkpoint writer + dense history | unwired / superseded |
| specs/connection-receiver-source.md | 28 | receiver turn | parked |
| specs/consumer-account-{binding-stage,config-commit}.md | 68/153 | typed C account adoption | parked (D46) |

Not Codex (added before cbd530797, Claude lanes): `planning/design-extent-read-protocol-2026-09-29.md` (e7e6f21d5, 09-29 05:02, extent-identity),
`planning/design-paged-history-2026-09-29.md` (9436e321b, 09-29 00:29, paged-history), `planning/design-resilience-framework-2026-09-29.md`
(b344e9fa8, 09-29 04:51, resilience-framework). `specs/resource-vector.md` is Claude's resource-ledger (877c69598, 10-01 06:36).
`planning/reorientation-2026-09-29.md` and `planning/handoff-2026-10-01-claude.md` (cited by the critic) are absent from d4e's tree (UNCHECKABLE location; Codex's other closeout is `build/coordinator/HANDOFF-2026-09-30-to-claude.md`, 239 l.).

## 14. State tag counts (entries in this file, one primary tag each)

on-dev-wired 19 (pool ownership; windows/decoded [era-2 wiring]; history gates [inert]; bless verb; snapshot-recovery; moved owner entries;
article-subject + FN-RCL2; OVER cursor/pins; poster-bytes/post-admission keepers; web-health; statement-sign; retire [defect];
feed counts [invariant open]; owner extractions; BP listener; BP recovery profile; TCPCL source [era-2]; peer adoption; account wired keepers) ·
on-dev-unwired 13 (incoming buffers; checkpoint writer library; productive reads; NOV windows; legacy parser; report capture/reader-output;
allocation epoch/turns; control-turn binding; substrate codec; FNCR; account logical core; dense-history design docs as code; control-body ticket) ·
on-dev-twin 1 (statement recovery `fn-ssr` vs `fn-srs`) ·
parked 10 (dense epoch D42; INITIAL/snapshot natives; admission census; W9 view D47; D25 cursor; index backing; receiver; BPSec; BP controller; 9P) ·
reverted-by-stage-0 5 (runtime bootstrap gate [ST0 break 1]; POST precheck [break 5]; acceptance-binding D43; CRC-0 D44; FNCE grammar + native auth D46) ·
deleted 1 group (7 host files + 3 books) · prose-only 7 docs · branch-only: none tagged here (branches are the harvest scout's axis; productive-read inbound PRF-1126/1127 sits on lane/productive-read-transfer).
