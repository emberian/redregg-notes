# TASK-TRIAGE 2026-10-08 (cv task store, Mini)

Scope: 560 non-terminal tasks (544 open, 6 claimed, 10 rev:landed). Nothing was closed or edited. Table: `TASK-TRIAGE-20261008.tsv` (id, state, bucket, area, evidence, action, title). Evidence base: origin/main e0a8ba21 (git log/grep), the tasks' own notes (S5/S7/S8 triage notes of 10-04 carry much of it), MERGE-QUEUE.md LOG, persvati/burst3 salvage ref lists. A trailing `?` on LIVE means I found no landing evidence either way (or only a partial hit) and did not prove it open; a LANDED row always cites a main commit that names the task id or its exact subject.

## Counts per bucket

| bucket | n |
|---|---|
| LANDED | 97 |
| STALE-WIP | 10 |
| DECISION-EMBER | 14 |
| DUPLICATE | 12 |
| LIVE | 422 (of which 73 marked ?) |
| OBSOLETE | 5 |
| total | 560 |

## Counts per area x bucket

| area | LANDED | STALE-WIP | DECISION-EMBER | DUPLICATE | LIVE | OBSOLETE | total |
|---|---|---|---|---|---|---|---|
| docs | 0 | 0 | 1 | 0 | 5 | 0 | 6 |
| hermes | 0 | 1 | 0 | 0 | 7 | 0 | 8 |
| infra/swarm | 27 | 2 | 1 | 4 | 25 | 2 | 61 |
| kernel-proofs | 21 | 3 | 2 | 2 | 96 | 3 | 127 |
| objective-bend | 23 | 0 | 3 | 2 | 50 | 0 | 78 |
| other-project | 0 | 0 | 1 | 0 | 141 | 0 | 142 |
| pay | 5 | 0 | 0 | 0 | 6 | 0 | 11 |
| product/deploy | 11 | 2 | 4 | 1 | 37 | 0 | 55 |
| research/planning | 1 | 0 | 1 | 1 | 14 | 0 | 17 |
| spk | 6 | 1 | 1 | 1 | 16 | 0 | 25 |
| store | 3 | 1 | 0 | 1 | 25 | 0 | 30 |

Note: 141 of the LIVE rows are not Mini work: ~132 `closure/*`, `crossplay`, `oracle`, `schema`, `audit` tasks in repo `~/dev/don` (opened 08-11, DoN reverse-engineering) plus ~9 cv/tokeman tooling tasks. They are tagged `other-project`; suggested action is one Ember decision to park them (or `cv task abandon` in bulk), not 141 separate verdicts. Excluding them, Mini has ~419 tasks of which 97 are landed-but-open (23%).

## DECISION-EMBER (verbatim title, the default that stands if silent)

| # | id | title | default / what is asked | command |
|---|---|---|---|---|
| 1 | `01a1052c-6e3a-7a73-97c0-d27c59bee90a` | DEPLOY-3 sponsor key custody: rotatable or not | No default recorded in the task. Suggested: rotatable (controller capability on the sponsor cell at genesis), since a leaked sponsor key otherwise forces re-genesis. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 2 | `01a0f52e-7763-76c9-93f7-5b91bb844975` | GITHUB: post the finalized reviews and closures (ember reads first) | No default; outward-facing (Ember reads prs/github-drafts/FINALIZE-LOG.md, fills issue-66 slots, posts). Closures #55/#59/#65/#68/#69 can go any time. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 3 | `01a0f52e-7777-7030-83b0-b78daba07071` | TEARDOWN-LEFTOVERS: PoA data, old images, telegram secrets, portal links, DNS records | Default: keep the two old images until the next redeploy proves out, then prune; rotate or remove TELEGRAM_* (key material, Ember). Deletions are Ember's call. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 4 | `01a0f54c-d1dd-72e2-8b19-e99f146df6ff` | EMBER: pushes, chown, Sigilante note, keys (age / enrollment address / week rate), Discord app, GitHub drafts, | No default: Ember's consolidated list (pushes of dregg-infra + dregg-assortia, chown id_portable, Sigilante note, keys age/enrollment/week rate, Discord app, GitHub drafts). Note the age key and enrollment address are already in 01a0f52e-771c / -7707 notes. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 5 | `01a0f53e-f651-7338-8967-b2e33eb49d7d` | QUOTE-DISCLOSE: should a quote carry text to readers of only the quoting room? (ember) + the --disclose lane | Default stands: reference-only for October (quote is a reference; reader needs source read access); `quote --disclose` later as a source-law-permitted disclosure act. ROOT ruling 10-06. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 6 | `01a0f6ac-3722-720f-bcd8-d38ae379a002` | NOCK-PACK: local contribution pack for Chris's swim-lanes (ember sends or not) | Default (nothing was sent): do not send until Ember chooses; pack is local only. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 7 | `01a0f6db-c50a-73f0-ba60-6e2454b13f9c` | CLOCK TICKERS: replacement needs re-genesis; a leaked clock key can move now arbitrarily far forward (no step  | No default recorded. Suggested: accept re-genesis for ticker replacement (greenfield) and add a per-tick step bound so a leaked clock key cannot move now arbitrarily far. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 8 | `01a0f96b-34f4-7151-ad55-f5929567840c` | CHANNELS §10.10 (re-posed): how sealed messages are keyed — your MLS question answered | Default (S5, Ember stated preference): PQ/hybrid per-epoch room key, not MLS. Treat as unresolved: the 10-01 "one group key per room" click was an accident of the page. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 9 | `01a10500-f300-7523-8876-f03082bd4d56` | SPK: close live g4's refused v3 attempt directory without deleting files (cutover decision) | Default (in the title): close the refused v3 attempt directory WITHOUT deleting files; cutover decision on the live r2 world is Ember/ROOT. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 10 | `01a10564-84ef-70e0-b777-8ed38cc26ad9` | Decide: use the C machine as the native executor for Objective admission (behind the differential gate), with  | No default recorded. Suggested NO for now: GPT-6 T2.5 says profile first and do not switch admission to the C backend on a few matching outputs; revisit behind the differential gate + tariff from the zk-truth lane. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 11 | `01a10afe-ecd0-7501-a594-39e9025f3bb2` | OB U10: multiple dispatch (multimethods) — decide whether Objective Bend has generic functions | Default: single dispatch (LT2 F-bounded binary methods) is the answer; no multimethods; record the deviation. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 12 | `01a10afe-ecf9-7ee1-b231-63c4b038e396` | OB U11: decide class OO — prototypes for first-class type descriptors | Default: types stay static; record a deliberate deviation with its reason (no-refusal theorem). | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 13 | `01a10afe-eda1-7502-bbf7-06f14cca938c` | OB V2: decide compose argument order (least-specific-first) vs extends/precedence (most-specific-first) | Default: keep compose(a,b) = b wins; GPT-6 explicitly defers the compose-order flag day. Taste fork (Nix vs C3 order); a flip re-emits every compose site. | ask; then `cv task done` (or `abandon`) with the answer as --observed |
| 14 | `01a0f961-721d-7583-8917-8551f48a6d31` | tokeman: per_session_reserve has no input after drain-truth; delete or re-ground (policy call) | Default: delete per_session_reserve / loaded_dwell_score and its config field (drain-truth made it dead); re-ground only if a real straggler signal appears. | ask; then `cv task done` (or `abandon`) with the answer as --observed |

Also an Ember call but bucketed STALE-WIP: `01a105b6-8396` COMMON-WORLD (live OO world lost its store in the 10-04 workbox cleanup; re-home or retire; suggested default: retire and rebuild on the next genesis).

## Top 40 LIVE tasks by service to THE BAR (cv 01a0f9c0-521b) and the GPT-6 rows

| rank | id | serves | why | area | bucket |
|---|---|---|---|---|---|
| 1 | `01a0f9c0-521b-7400-bff7-5ca5fd59420f` | BAR | THE BAR 10-13: two friends + hosted Hermes, joined, on the public node: the bar itself; needs a measurement run | product/deploy | LIVE |
| 2 | `01a0f52e-7711-71f4-80a1-7d4a5f8a8e07` | BAR | DEPLOY-3: one batched box deploy of everything landed since 5688775a: DEPLOY-3 batched box deploy: public node must carry the new candidate | product/deploy | LIVE |
| 3 | `01a0f9c0-55af-7182-ac67-9619ce8505f4` | BAR | M1 (intermediate): one friend's first hour on the public node, on the : M1 one friend first hour | product/deploy | LIVE |
| 4 | `01a0fb03-bc64-71b3-94c3-8a6f57d1a9b8` | BAR | HERMES-LIVE: one useful real-provider resident through the room and du: HERMES-LIVE: one real-provider resident on the public node | hermes | LIVE |
| 5 | `01a0fbc7-a94c-7ee2-8c76-868f51813fc3` | BAR | Member BYOK: authenticated remote custody, route choice and fresh Herm: member BYOK + fresh Hermes provisioning | hermes | LIVE |
| 6 | `01a0fa24-0469-72b0-bf92-9ef83192740c` | BAR | A write to a 1000-entry cell takes about 400 s on the spec-Keccak Host: 1000-entry write took ~400 s: re-measure vs <=5 s write | store | LIVE? |
| 7 | `01a0fa73-e626-71a1-863a-900aa9324881` | BAR | AUDIT-SUPERLINEAR: cold mini audit grows ~3.4x per 2x records (372 s a: cold audit superlinear: re-measure vs <=60 s reopen | store | LIVE? |
| 8 | `01a11794-cab3-77a2-9bf3-c1dfba5b54ad` | BAR | KN2-TRIE sub-range B: keyed families 2-7 on the unified trie, delete P: KN2-TRIE B: keyed families on unified trie (b31 ungated on next) | store | LIVE |
| 9 | `01a114aa-6780-7703-abe5-69d1a9b38656` | BAR | KN2: authenticated keyed index for fleet head/incoming (no full-journa: authenticated keyed index, no full-journal scans | store | LIVE |
| 10 | `01a117d6-aca7-7f80-8e17-a132f1dad6f1` | BAR | KN2: since/tail views off the full loaded log (Reader.range pages): since/tail views off the full loaded log | store | LIVE |
| 11 | `01a11476-4ddb-78e1-8dea-d14930839572` | BAR | KN2 2b-3: delete the full Loaded materialization when full-loaded-call: delete the full Loaded materialization (open cost) | store | LIVE |
| 12 | `01a0fadb-6602-7b32-8f07-cfbec582aed7` | BAR | Store tree cost: full-read view size and per-write root cost (seed for: Store tree cost: full-read view size, per-write root cost | store | LIVE |
| 13 | `01a0fb03-bc7c-7992-b318-72a620920b27` | BAR | DURABLE-ANCHOR: local authenticated head and client receipt continuity: durable anchor / receipt continuity (may already be landed: verify) | store | LIVE? |
| 14 | `01a0f972-8393-7490-ac84-4030212b81ee` | BAR | Durable log: truncation after the last checkpoint is undetected: durable-log truncation undetected (may be closed by store v5: verify) | store | LIVE? |
| 15 | `01a0f7da-60bf-7667-bb99-64c757d27ba3` | BAR | ROOM-TAIL VIEW: tail is 1+K signed reads; 200 entries / 5 streams = 12: room tail view 12 s at load 35 | product/deploy | LIVE? |
| 16 | `01a0f7da-60ad-7135-a515-c45f54c87c44` | BAR | STALE-ROOT RE-SIGN: per-author streams still collide at the challenge : stale-root re-sign storms under concurrent says | product/deploy | LIVE |
| 17 | `01a0f5fd-648b-75d1-853d-454122e840f6` | BAR | DEPLOY-3 first box run: check what the sandbox could not: DEPLOY-3 first box run: items the sandbox could not check | product/deploy | LIVE |
| 18 | `01a105e1-7f98-7810-b7d8-d82af38152a6` | BAR | Hermes summon into a private room: the resident registration carries a: Hermes summon into a private room (bare key id) | hermes | LIVE |
| 19 | `01a10667-e1b3-7f60-924a-23c34e9ced8d` | BAR | Hermes controller under its own account (mini-hermes) instead of mini-: Hermes controller under its own account | hermes | LIVE |
| 20 | `01a10667-e189-76c0-83ec-e8bb8c18ca7f` | BAR | Run jsplit-tenancy.sh (split step B: S0-S8 + N1-N6) on a disposable sc: run split-tenancy journeys on a disposable VM | infra/swarm | LIVE |
| 21 | `01a0f829-a072-77d5-8d3b-99ef705a6ef0` | BAR | journey G and JPAY2 go red on a loaded box: G early-stops on a 3% writ: journeys G/JPAY2 red on a loaded box (the bar IS load) | infra/swarm | LIVE |
| 22 | `01a105d4-4a57-7853-b265-3a315bf2e9f7` | BAR | mini serve: per-peer connection-slot cap needs a per-client identity a: per-peer connection-slot cap needs socket identity | product/deploy | LIVE |
| 23 | `01a11a80-3d6c-7543-a652-928e9cf220f8` | GPT6 T2.2 | T2.2-committed-Store-refinement: relate persisted records/rows/head in: committed-Store refinement of the maintained index | kernel-proofs | LIVE |
| 24 | `01a11a80-3d42-77e1-965b-8ff1c74caf74` | GPT6 T2.2 | T2.2-set-preservation: prove set_preserves_all (discharge maintained_a: set_preserves_all | kernel-proofs | LIVE |
| 25 | `01a11aee-3d97-7c60-a1c0-334f752bf183` | GPT6 T2.4 | Collision-disjunct vacuity: '∨ Collision dig' is TRUE by pigeonhole (3: collision-disjunct vacuity in the deployed lookup theorem | kernel-proofs | LIVE |
| 26 | `01a11477-0c15-7cd1-8d9d-b00fb67f96d0` | GPT6 T2.4 | Theory Digest unbounded: injective-digest binding premises are inhabit: Theory Digest unbounded: binding premises inhabited only off the deployed hash | kernel-proofs | LIVE |
| 27 | `01a0f87d-02f7-71df-88dd-3194e2b274fe` | GPT6 T1.1 | T4 HOST-CUTOVER (FD-1): submit = World.admit — after the stage-2 candi: HOST-CUTOVER: submit = World.admit (exact-intent certificate) | kernel-proofs | LIVE |
| 28 | `01a0f6c5-6891-7547-8f98-bd6b47943b60` | GPT6 T1.1 | LIVE-EQUALS-REPLAY: one admission function for submit and audit; the a: live = replay: one admission function | kernel-proofs | LIVE |
| 29 | `01a11680-f2cc-7592-8eac-088857cc1b0d` | GPT6 T1.4 | row E: front-end rates valid only up to the measured source bound; rep: front-end rates only valid to measured bound (cv f2cc named by GPT-6) | objective-bend | LIVE |
| 30 | `01a11636-203c-7f50-bb3a-7659050e95b8` | GPT6 T1.4 | row E: front end generation not metered by the declared core; C4 fuel : front-end generation not metered by the declared core | objective-bend | LIVE |
| 31 | `01a11680-f2a6-7773-8195-bd6ed88351e3` | GPT6 T1.3 | row E: charged failure only for birth/invoke; deliveries, messages and: charged failure only birth/invoke; other turns still fail free | objective-bend | LIVE |
| 32 | `01a1180e-7140-7342-bbc9-79181ac13240` | GPT6 T1.3 | row E (b): upgrades pay their front end (adopt/migrate/rebirth in paym: upgrades pay their front end | objective-bend | LIVE |
| 33 | `01a1180e-715b-7a02-8c7c-a63d6d9d1886` | GPT6 T1.3 | row E (c): seats go signature-first with the charged failure receipt; : seats signature-first with charged failure receipt | objective-bend | LIVE |
| 34 | `01a117cd-8596-7493-8573-342a240e919c` | GPT6 T1.4 | row E: method loads re-lower the pinned entry (a kernel-installed cell: method loads re-lower: Option C per-pin cache ruled, implement | objective-bend | LIVE |
| 35 | `01a11617-4415-79a0-a5b4-b98392e825e0` | GPT6 T1.5 | ROW-F-LEFTOVERS: never-expiring slot theorem, cross-sender FIFO journe: retry leftovers: stable terminal disposition | objective-bend | LIVE |
| 36 | `01a1141b-d4b5-7802-b2cf-4763eb9575b8` | GPT6 T3 | UPGRADE: multi-turn MIGRATE (migrating phase + cursor): multi-turn MIGRATE for the upgrade journey | objective-bend | LIVE |
| 37 | `01a104f3-e3b5-78f2-9f79-ae6d58d48e02` | GPT6 T3 | Port the surviving Bend-surface domain sources to .obend (station Shar: port surviving domain sources to .obend for the composed product | objective-bend | LIVE |
| 38 | `01a105c8-187a-7a30-ab48-7b38790c1fc0` | GPT6 V3 | VACUITY: audit the 17 trivially satisfiable structures the probe found: audit 17 trivially satisfiable structures | kernel-proofs | LIVE |
| 39 | `01a10503-6cb7-77c2-bd71-88c7f674cd16` | GPT6 V2/V3 | HypothesisLedger: mark a Prop REFUTED when refuted for ANY field, not : ledger REFUTED when refuted for ANY field | kernel-proofs | LIVE |
| 40 | `01a0f6d8-00de-760d-aead-0741a6cd3134` | BAR | dregg-infra mini-reenroll/OPERATOR: copy the friend's NEXT public key : K-PREROTATE next-key copy beside custody copy (friend enrolment) | product/deploy | LIVE |

GPT-6 rows with NO live task (gaps worth opening): T1.6 artifact ownership (no hard-linked writable workspaces), T1.7 role generation / fencing tokens, T1.8 coprocess acceptance tests (late reply, truncated reply, recovery; 1930a558 landed the tagged reply protocol only), L Lean v4.34 upgrade (lean-upgrade refs exist in burst3 archive), V1 manifest dependency-collector backport/test (7609a3a1/33421c35 landed a collector fix; focused test unverified), T2.1 prepared-effect equivalence, T2.3 whole-open refinement with fault model. T1.2 (remaining-budget meter) landed: 1653897b.

## Close commands (run after review; none were run)

Verbs available: `cv task done <id> --observed <ref>`, `cv task abandon <id> --reason ...`, `cv task supersede <id> --by <id>`. (There is no `cv task close`; `resolve` answers kind=decision tasks only.) The 10 `rev:landed` cv-repo rows may need `cv task verify` first because `done` refuses while a code revision is live.

### close-done (LANDED, 97)

```
cv task done 01a107f4-1c8a-7312-ad96-4ede0d3453bb --observed "mini origin/main e0a8ba21: 9e603fa9 kernel(resume)!: forcing transparent at every valid yield; LOG b3a kn2-"
cv task done 01a10a62-36cb-73c3-aa2b-657dca83f9ba --observed "mini origin/main e0a8ba21: 36bba090 chain instance IS the checked template at sigma; instance_accepted in T"
cv task done 019f6e94-5c35-7b10-a238-f0b8cde8f118 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: c9859bca on cv main"
cv task done 019f6e94-5c49-7033-8d05-82fe27d78a4b --observed "mini origin/main e0a8ba21: rev:landed (cv revision landed state)"
cv task done 019f6e94-5c6a-70e0-9b72-ce1ef166bd10 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: 66bec7b0"
cv task done 019f6eef-dc51-73e3-88e7-7fc012afc37c --observed "mini origin/main e0a8ba21: rev:landed S5 triage: fd55d6d3"
cv task done 019f6ef7-0455-7c70-a234-3ef4107a40e2 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: 34c61847"
cv task done 019f6ef7-0469-7680-a8af-0bcf921aa706 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: 970d0a71"
cv task done 019f6ef7-047c-7b33-b8ab-1807bbaafdf2 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: 440e52b0"
cv task done 019f6f36-7715-7bb0-8ac7-bf44ddf9ce32 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: 4b3c602b"
cv task done 01a0f52e-76fd-756d-90e1-4508ea5d2084 --observed "mini origin/main e0a8ba21: DEPUTY-PRODUCT landed-verify: FRIENDS.md pay-to-enrol 243fb343,408acb23 on main"
cv task done 01a0f611-ea6c-77a4-984a-ecb64fe70e4e --observed "mini origin/main e0a8ba21: c944a8f0 content(kernel)!: insertRun (K-RUNS-RANGES); queue P5-RUN-EDITS"
cv task done 01a0f612-7ab3-7060-a0f5-95bf6ee59eb2 --observed "mini origin/main e0a8ba21: 4f6763a3 perf(linkindex) cites cv 01a0f612-7ab3"
cv task done 01a0f627-4a20-7638-9d0c-618b674b3802 --observed "mini origin/main e0a8ba21: 5df8bb07 resource-client: can delegate probe burns no namespace identity (cites "
cv task done 01a0f63a-233a-745f-b5b9-2ae27f123fd0 --observed "mini origin/main e0a8ba21: 3df668ef light open + 16633f66 checkpoint v3 + 7f5ea838 kn2-store-bench; BAR sti"
cv task done 01a0f64e-c650-73a2-af2f-b73f879bd588 --observed "mini origin/main e0a8ba21: 885fae57 SheetLaw landed in LOG b2 P2-SHEETLAW"
cv task done 01a0f6d0-e044-725d-9133-2ca54883ebef --observed "mini origin/main e0a8ba21: S7 note: already satisfied; join_solana.rs takes atomicAmount from Host quote op"
cv task done 01a0f6d0-e063-7222-accc-eeabce0e49f6 --observed "mini origin/main e0a8ba21: deploy/pay/README.md + render-enrol with pay-watcher-env on main (S7)"
cv task done 01a0f6d8-0101-70f6-8f8e-816984ea5e61 --observed "mini origin/main e0a8ba21: beeeb486 mini: name the refusal of a request signed by a non-current key (cites "
cv task done 01a0f6d8-0110-7455-af66-513753bf2f5c --observed "mini origin/main e0a8ba21: 5f9aa259 journey(JROTL): lost op-142 reply found by op-143 lookup; LOG native-ex"
cv task done 01a0f72b-7d95-761b-9dae-2e27c4f93028 --observed "mini origin/main e0a8ba21: d4e881b3 private rooms: one invite path; custody byte in invitee record"
cv task done 01a0f72b-7dae-7350-ab26-b4b7fc05f0f6 --observed "mini origin/main e0a8ba21: 35508a6f Compiler/RefusalReason renders verbs 7,10 as append/place (cites 01a0f7"
cv task done 01a0f830-42e7-7497-8950-5ca8e8ac4616 --observed "mini origin/main e0a8ba21: 5216e02f candidate: every Rust binary through one fixed path, same bytes (cites "
cv task done 01a0f838-d1e1-70e3-9ab2-2599c29546e3 --observed "mini origin/main e0a8ba21: 8ac769d7 mini serve: per-op body bounds, Host-time budgets, fair per-peer queue "
cv task done 01a0f99e-d668-72c3-8dc4-21518f4f2f36 --observed "mini origin/main e0a8ba21: 942d8ebc discord mirror: private room opened text structurally cannot reach chan"
cv task done 01a104f3-e258-74d3-b185-e0b482df20ea --observed "mini origin/main e0a8ba21: tenancy-b commits 179f6bee 73e06411 7bb016a3 on main (key broker, mini-keys); ru"
cv task done 01a104f3-e2ed-7742-97e8-17efb10696e7 --observed "mini origin/main e0a8ba21: 28c3e7fa private rooms: hybrid X25519+ML-KEM-768 wraps (record v3)"
cv task done 01a104f3-e30f-7df0-ade8-8ba2700acf5e --observed "mini origin/main e0a8ba21: 33a8fd59 private rooms: founder-key transition"
cv task done 01a104fd-8e73-7003-9931-28a2b9148acc --observed "mini origin/main e0a8ba21: a88b391b rooms(JPRIV1)!: green on a real Host; LOG PROTOCOL-NIGHT ROOMS"
cv task done 01a104fd-8f66-7fa2-9597-3e105bdd5129 --observed "mini origin/main e0a8ba21: 26429438 resource-client!: delete current_source.rs and current-source-helper"
cv task done 01a104fd-9015-7890-907c-d5423de9bb39 --observed "mini origin/main e0a8ba21: 61c37de2 gates: arm private-rooms tests in check-rust-tests.sh as named exact ro"
cv task done 01a104fe-94a5-7983-9d5f-f7c2f9f6c914 --observed "mini origin/main e0a8ba21: 940c3a79 intent bytes are Lean's (7370a7e0 lean(contracts))"
cv task done 01a104fe-958e-7d70-96e9-feb1cd13fee2 --observed "mini origin/main e0a8ba21: cf0d74f7 mini-sdk ssh:DEST route held by e2e gate"
cv task done 01a10500-6e65-7132-ba1c-88964aabb551 --observed "mini origin/main e0a8ba21: a2454432 objective(front-end)!: Lean elaborator is THE implementation"
cv task done 01a10500-6eef-77b3-9a58-d55cbb37d917 --observed "mini origin/main e0a8ba21: 4dfd96e0 re-emitted captured packages/pins with parser change"
cv task done 01a10500-6f2f-78f3-a9a8-8e3885b99e45 --observed "mini origin/main e0a8ba21: d81102e9 S8 check-objective-frontend.sh is the one gate"
cv task done 01a10500-6f6f-7e21-9f22-1c83ff726f3d --observed "mini origin/main e0a8ba21: 1f595131 composition contract one named algebra fix discharges; 0c1d6d58 final-s"
cv task done 01a10500-f1d1-7a51-bcd0-8e829d42215e --observed "mini origin/main e0a8ba21: 64d0a732 spk!: resident unit names carry the Store"
cv task done 01a10500-f26d-7e23-ab75-8571e15a8b0b --observed "mini origin/main e0a8ba21: dd97fcc6 retried g4 enters created/running chronology"
cv task done 01a10500-f2bc-7280-8c27-0ba8e3009f42 --observed "mini origin/main e0a8ba21: 304b976e resident reconciles uncertain BEGIN/CLAIM by op23/op27 lookup"
cv task done 01a10500-f341-77f2-823c-f3e1c67a2db1 --observed "mini origin/main e0a8ba21: dd97fcc6 compile the W2.F v4 retry forward (+374549d4, a183acf8 chain)"
cv task done 01a10501-8293-70b1-a8fe-541900b613cf --observed "mini origin/main e0a8ba21: 1d5ae709 bread-b: GenericSimplexReconfig compiles; CertF pinned"
cv task done 01a10501-830d-7750-a105-43a514d6c301 --observed "mini origin/main e0a8ba21: 954a5d86 traffic: Linux qualification of MCE3 roster enrollment"
cv task done 01a10503-6c57-7193-9099-d135b624c2af --observed "mini origin/main e0a8ba21: 493b2377+95bfab2d Kernel/AgreementEvidenceRegime compiles"
cv task done 01a10505-46cf-7442-8710-09fc95b7dbc6 --observed "mini origin/main e0a8ba21: ef0fe2e3 checker conversions cannot manufacture shareability; shadowing theorems"
cv task done 01a10510-6e33-72c0-b59b-edaa172dc957 --observed "mini origin/main e0a8ba21: 746bd9f5 discord-entrance: durable-restart test waits for the custody lease"
cv task done 01a10510-6e60-7d33-9855-6b891737d387 --observed "mini origin/main e0a8ba21: 232e6cf1 cohort: a stalled stranger cannot tie up the cohort listener (cites tas"
cv task done 01a10539-ae49-7262-9031-c6a840b7ea23 --observed "mini origin/main e0a8ba21: 9a2876a7 agreement: reopen long journal in constant stack, 100000-entry test"
cv task done 01a10539-ae89-7fd3-b47c-ec0235c723e4 --observed "mini origin/main e0a8ba21: LOG agreement lanes landed (3f2a7065..); W1.7 journal reopen fix"
cv task done 01a10556-492a-7b73-a1cf-9097ebec4b8b --observed "mini origin/main e0a8ba21: 374549d4 spk-host v4 retry + r2 recovery ports"
cv task done 01a10556-496e-7d33-ba63-c8ebc9ddeac9 --observed "mini origin/main e0a8ba21: 66a54085 + 6a6cbdda package laws enforced and travel in artifact"
cv task done 01a10564-84a1-7a62-993a-d1d343fab279 --observed "mini origin/main e0a8ba21: note: VERIFIED FIXED at df0cd116 (6b2616db injection rule)"
cv task done 01a1056f-0066-7012-ba29-1d1f7d80690b --observed "mini origin/main e0a8ba21: 8194e09d kernel(activity) answer slots + resume contract; 7dd88709 yield stores "
cv task done 01a1056f-00a4-7103-9916-e39a47e54daa --observed "mini origin/main e0a8ba21: 9eef9499 theory(collect): collect Core4 heap at a yield"
cv task done 01a105a2-bc23-7801-9cf9-bb57ed7d85d5 --observed "mini origin/main e0a8ba21: 6f82b818 preview: deep-force the result (cites task); let-binding in acef9f86"
cv task done 01a105ba-6d10-7292-a2c9-19cc2e62b7c4 --observed "mini origin/main e0a8ba21: acef9f86 frontend: - < <= > >= lower to package prelude; let; typed-core.v3 (cit"
cv task done 01a105bb-e2a2-7b23-bb9e-02592923b042 --observed "mini origin/main e0a8ba21: note: first native Objective Accepted on main 796d7d7a"
cv task done 01a105c0-0292-7ad0-9d75-09b5b86fb0d9 --observed "mini origin/main e0a8ba21: 408acb23 pay(tariff)!: unit is the week, 50 DREGG exactly (cites 01a105c0)"
cv task done 01a105d4-4a7c-7ff0-8125-ed124114a0b4 --observed "mini origin/main e0a8ba21: 35508a6f renders verbs 7,10 (same change as 01a0f72b-7dae)"
cv task done 01a105e7-eb36-79c1-b5ba-9d1b1dbb0029 --observed "mini origin/main e0a8ba21: 212c79af BendTT delete (244 paths) on main"
cv task done 01a105ff-1bf5-7541-9c8d-dd88ee186d3f --observed "mini origin/main e0a8ba21: 4de4ddd5 mini-sdk intent encoder checked against Lean export at runtime"
cv task done 01a105ff-1c1f-7a21-80f8-e018380e295f --observed "mini origin/main e0a8ba21: 2a4fab88 resource-client ssh client half + header signing moved onto mini_sdk (c"
cv task done 01a1060e-5dbc-70e1-b352-5aeef096278b --observed "mini origin/main e0a8ba21: 0afaf7f2 core4(objective)!: Primitive subtract/divide/less/lessEqual"
cv task done 01a1062d-3557-7223-a67d-0bb789f633c5 --observed "mini origin/main e0a8ba21: 9525b8e0 objects(pq): device keys ride shared hybrid_kem combiner"
cv task done 01a1062d-35c9-7701-aa25-c547e8f7990e --observed "mini origin/main e0a8ba21: db8abb59 spk-host(pq): TLS 1.3 X25519MLKEM768 via aws-lc-rs"
cv task done 01a1062d-35fb-7980-9618-d6bcff2746e6 --observed "mini origin/main e0a8ba21: f856f2f4 mix(pq): cohort enrollment MCE4 hybrid Ed25519+ML-DSA-65"
cv task done 01a10694-767b-7151-a581-097e8cb3f50f --observed "mini origin/main e0a8ba21: a102f980 private-backend: Gather ACK quorum pinned with constructed adversary"
cv task done 01a10694-76ce-7592-bfbf-3553d4b30821 --observed "mini origin/main e0a8ba21: a102f980 notes Lemma 4.5 cover-set mis-definition in construction"
cv task done 01a1087d-8a12-7f03-9455-425be7a255bb --observed "mini origin/main e0a8ba21: d65661cf laws(births)!: Receiver judges birth by export law"
cv task done 01a1087d-8a58-7e83-846e-3830ff00ce7c --observed "mini origin/main e0a8ba21: note: CLOCK row CLOSED on main 5d0b452d; 90e14a1d pay family"
cv task done 01a1089a-10c6-7521-9689-bc7434ac3afd --observed "mini origin/main e0a8ba21: 58ac7b83 gates: exports counts a call only in live native code"
cv task done 01a1089a-10f7-7052-b4ae-b0d7b1ea1b8e --observed "mini origin/main e0a8ba21: 58ac7b83 shell-paths derives its parser list"
cv task done 01a1089a-1131-77d1-80b1-5d4a69886e12 --observed "mini origin/main e0a8ba21: 8f88c29f local-gates drift gate sees a new untracked emitted file"
cv task done 01a1089a-11b5-7140-9fdc-2ba511b9444f --observed "mini origin/main e0a8ba21: 06c5583e gates: seven survivors now go red (W20-GATE-MUTATION)"
cv task done 01a109bd-8682-7641-941e-f5c417ccff6a --observed "mini origin/main e0a8ba21: 90e14a1d + c3b4acb4 laws(pay)!: pay families are Receiving.Family"
cv task done 01a10ae9-79e1-7802-8201-377c194d1b4a --observed "mini origin/main e0a8ba21: cf471103 kernel(send, GPT-6 row F)!: delivered method sends onward from prepaid "
cv task done 01a10ae9-7a37-7b73-956b-93b3bd07fdc0 --observed "mini origin/main e0a8ba21: 8f87fd7b proofs(objective): retention; LOG ob8-retention"
cv task done 01a10ae9-7a53-7ab0-a6ae-ee2e5d06809e --observed "mini origin/main e0a8ba21: 8f87fd7b only a sending turn writes an inbox"
cv task done 01a10b3e-af9e-74d2-9c23-852ab214bd65 --observed "mini origin/main e0a8ba21: 304b976e closes cv 01a10b3e-af9e (commit message)"
cv task done 01a113e7-92cb-7460-8e98-1e6861193195 --observed "mini origin/main e0a8ba21: 3da5a5bc seats: gift must be marked, Proposal.donate refused by name"
cv task done 01a113f0-5027-7b53-ba77-382503fd06b3 --observed "mini origin/main e0a8ba21: f25e4ebc deliver/exhaust declare checkpoint heap in extra; 928a7294"
cv task done 01a113fe-13ca-7342-8021-144297b6c821 --observed "mini origin/main e0a8ba21: ce3c4ed1 queued message deposit, emptied inbox retired, slot named"
cv task done 01a113fe-140a-7912-841d-11fbdde96112 --observed "mini origin/main e0a8ba21: c0da309a replySlot not-this-inbox refusal, MessageDelivery.activityExact (cites "
cv task done 01a11409-6df6-7a42-847e-5b1593d2a36e --observed "mini origin/main e0a8ba21: eff01705 content schemaVersion 10 drivers + fixture"
cv task done 01a11467-08ce-76e1-af06-7ddd1ab3b866 --observed "mini origin/main e0a8ba21: 92da0719 fixed-width charged record + 9e821ae9 quote once; LOG deposit-fixpoint"
cv task done 01a11476-1c59-7053-97f8-4f497c9ac0ed --observed "mini origin/main e0a8ba21: 13a2cc00 fleet-sign (cites cv 01a11476-1c59)"
cv task done 01a1147a-f80e-7b91-91df-677ad4329e08 --observed "mini origin/main e0a8ba21: 6be6564f merge gate builds every lean_exe root"
cv task done 01a1147b-103d-78a3-9619-cea9b02d5703 --observed "mini origin/main e0a8ba21: b71af30a + aaf44e0c native accepted fixture hand-written authority"
cv task done 01a11609-0512-7e20-8454-8c0a5e7db607 --observed "mini origin/main e0a8ba21: 3ff036d4 pay(probe)!: PayEnrolSignatureIO deleted (cites cv 01a11609-0512)"
cv task done 01a11617-43fd-7111-9958-916c9ed9cf93 --observed "mini origin/main e0a8ba21: 57ee7338 kernel(send, GPT-6 row F)!: nonce is operation id; retry answers origin"
cv task done 01a11620-bc75-73d1-84ef-59ba661f2245 --observed "mini origin/main e0a8ba21: 6376fed8 kernel(objective, GPT-6 row E)!: charged failure receipt"
cv task done 01a11620-bc96-7c52-b93c-f8d18eb97435 --observed "mini origin/main e0a8ba21: 4aa9ddc5 extraction ticks declared and priced; 6e569f13 ceiling; 1653897b remain"
cv task done 01a1167a-73f5-7a33-8931-d4832291e874 --observed "mini origin/main e0a8ba21: 626ef4d4 fn selective release: name why source publication is not prepared"
cv task done 01a1177f-1ba6-7171-9cb0-c6d507bd433d --observed "mini origin/main e0a8ba21: e962c4ec journey(JGATE) gateway direct call refused at gate AND receiver"
cv task done 01a117cd-857b-7792-adbc-a681eae05d88 --observed "mini origin/main e0a8ba21: 99221471 a refusal carries the meter at its failure point (cites 01a117cd-857b)"
cv task done 019f6e94-5c52-7292-95b8-c18e7645f5a0 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: f28b5277"
cv task done 019f6e98-0e41-7c53-9a73-842b29bfa451 --observed "mini origin/main e0a8ba21: rev:landed S5 triage: d5004d3f"
```

### close-stale (STALE-WIP and OBSOLETE)

```
cv task abandon 01a0f52e-774e-7596-bcad-adf5f5e7d69b --reason "obsolete: note: Mini TS SDK has no @noble/post-quantum; Ember leaning keep refusals (docs/SDK-PQ.md)"
cv task abandon 01a0f52e-76a0-7673-9409-b52f889bcef2 --reason "obsolete: S5: ROOT-OWNED role; superseded by MERGE-KEEPER + queue/ (MERGE-QUEUE.md 10-04)"
cv task abandon 01a0f52e-76f2-73a2-86fb-b87d3c6cfbe4 --reason "stale-wip: root froze; mud-area dfb55b4d cannot cherry-pick; salvage persvati lanes.git lanes/mini-datamodel-20"
cv task abandon 01a0f533-b2cc-7517-b73e-8edee780534c --reason "obsolete: superseded by pipeline!: mk-lane atomic claim, box topology (2a8f36a6, 5f2b951f) + MERGE-KEEPER"
cv task abandon 01a0f676-2673-70fe-a026-fef61d2a2ae7 --reason "stale-wip: persvati orphan unit/cleanup list; persvati torn down; no salvage ref"
cv task abandon 01a0f740-26b0-717e-8c28-b20741266d75 --reason "obsolete: BRAID-PROOF note: payRefill does not need this (PurseRefillReceiver two-leg)"
cv task abandon 01a0f96d-f34c-7b63-8d02-33750b797734 --reason "stale-wip: S5: NOCK-FEE built on branch nock-fee c02be4a3, not main; salvage persvati lanes/...nock-fee_src; em"
cv task abandon 01a0f99e-9919-79f0-a787-6ec51dca7ae2 --reason "obsolete: S5: ember said teardown/rebuild; obsolete as prerequisite (root close candidate)"
cv task abandon 01a0fadb-65d6-7bb1-b76b-5923b8709a21 --reason "stale-wip: k-fields-observe lane finish; salvage persvati lanes/...k-fields-observe_src"
cv task abandon 01a0fbd3-65db-7a23-b17a-d4b3fb6f8df5 --reason "stale-wip: codex:private-docs; PASS49 candidate 377cc32e; salvage persvati lanes/...codex-private-docs_src"
cv task abandon 01a0fc44-0146-77f3-b5ff-3c93c39e9798 --reason "stale-wip: assignee codex:spk-service; salvage persvati lanes/...codex-spk-service_src"
cv task abandon 01a0fc50-4f28-7123-96d6-e264a663f1ef --reason "stale-wip: assignee codex:law-composition; prototype 7d20df5f in persvati codex-law-origin"
cv task abandon 01a0fc5d-4eba-71d1-b6af-8572ee9098ce --reason "stale-wip: assignee codex:root-deploy; salvage persvati lanes/...codex-summon-dispatch; hermes relevance: respa"
cv task abandon 01a118de-3019-75b1-b377-b06481efb2a6 --reason "stale-wip: lane/kn2-port-b2 likely superseded by landed Ground work; salvage burst3-a archive-kn2-port-b-lane_k"
```

### close-dup (DUPLICATE)

```
cv task supersede 01a0f823-fe95-733a-b6c7-ab4b86212414 --by 01a0fb20-e84b-7511-94ef-60b8c29b8265   # PRIV-ROOMS-DOC-EDIT: sealed doc edits in private r
cv task supersede 01a105d4-4aa1-7071-b0f4-60e8268a3c52 --by 01a0f53f-f848-72f8-b83f-5ccbd92db336   # MCP private_transfer deletion: authored, uncompile
cv task supersede 01a105c0-02bb-70c0-b189-c717c1bbc9ed --by 01a0f5fd-649b-706f-b765-682873fc703c   # stale-IP residue after the 09-28 move: private net
cv task supersede 01a0f5f8-8d9b-7382-9986-63fafae5a21f --by 01a0fad6-6713-7db3-90ca-fbeba2a488d2   # NOCK-MINK-JET: proven mink jet so wrapped NockApp 
cv task supersede 01a0f60e-2dcf-777b-97ca-fe74a2d0b1e3 --by 01a1186d-687d-7273-ab6e-c4a38be7850d   # doc history cost: O(rows x log) prefix replays
cv task supersede 01a104f3-e285-7ad1-b2d4-f7d5597485c4 --by 01a10667-e1da-71b0-b24d-26b3e2759f3e   # Discord bridge and provider-service under split te
cv task supersede 01a104f3-e2a8-7d80-abd7-68cfd4cd12bf --by 01a10667-e189-76c0-83ec-e8bb8c18ca7f   # Run journeys J0-J8 and jroster under split tenancy
cv task supersede 01a104fe-953e-7871-8ae8-e8c698916660 --by 01a105ff-1c48-7860-b9dd-e2f955786618   # SDK: move app_document.rs onto the SDK (depends on
cv task supersede 01a10556-49ad-7ca2-a562-24fc1d5626d0 --by 01a1065a-4f85-73b1-b429-deecfd20e834   # MINE: FHE over Objective (r34 natural/owner.rs new
cv task supersede 01a105af-d204-7040-a060-428c79025d2b --by 01a1065a-4f85-73b1-b429-deecfd20e834   # FHE-OVER-OBJECTIVE: rebuild the deleted codex FHE 
cv task supersede 01a105e7-eb7b-7680-bdc5-9a9b14220fcd --by 01a104f3-e258-74d3-b185-e0b482df20ea   # TENANCY-B: key-service broker and per-service uids
cv task supersede 01a10644-51f7-7cc2-a93e-83db2e21f599 --by 01a10a1f-c130-7992-aeab-1d2f1d137762   # SPK: run jspk1 failstart and s2-same-app on a fres
```

### Release dead claims (6 claimed tasks, claimant claude-followups is gone)

```
cv task release 01a104f3-e35e-7531-90df-6f7ac58d4347   # Review website/*.html against the rewritten README [LIVE?]
cv task release 01a104fd-8f66-7fa2-9597-3e105bdd5129   # Delete current_source.rs + current-source-helper C [LANDED]
cv task release 01a104fd-9015-7890-907c-d5423de9bb39   # Arm the new private-rooms refusal tests in check-r [LANDED]
cv task release 01a10510-6e33-72c0-b59b-edaa172dc957   # discord-entrance: durable_restart_* endpoint test  [LANDED]
cv task release 01a10510-6e60-7d33-9855-6b891737d387   # cohort: restore a test that a stranger cannot tie  [LANDED]
cv task release 01a1056f-0083-7011-a6d6-8651c79a81f5   # Objective activities: within-turn non-divergence c [LIVE]
```

## Salvage refs for STALE-WIP rows

- Codex 10-03 wave and 10-01/02 lanes: persvati `git --git-dir=$HOME/build-salvage-20261007/lanes.git for-each-ref 'refs/heads/lanes/mini-datamodel-20260930_<lane>_src/*'` (lanes seen: mud-area, mud-braid, nock-fee, k-fields-observe, codex-private-docs, codex-spk-service, codex-law-origin, codex-summon-dispatch, c14-tail, docuverse, k-narrow-hide). Persvati has 3821 refs, burst3-a `/srv/git/minidregg.git` has 325 `lane/archive-*` refs (burst2 lanes, e.g. `lane/archive-kn2-port-b-lane_kn2-port-b2`).

- Two bulk findings: (1) the 10-01 `lane:*` follow-up tasks (most of the ~330 opened 10-01/10-04 by lane:* / orchestrator) are NOT stale-wip: their lanes finished and each filed what it could not do, so they are real residue; I kept them LIVE. (2) The only truly lane-bound rows are the codex:* assignees (326, 328, 329, 330) and the mud-area/nock-fee/k-fields-observe lane finishes; codex is dead until Oct 10, so their closing means "re-open from the salvage ref if wanted".

## Why `cv task sweep` finds nothing, and how landings should close tasks

`cv task sweep --repo ~/dev/minidregg` only lists tasks whose `--issue` path no longer exists, or whose title/body names a branch that `git branch --merged main` reports. Here neither signal exists: titles name subjects, not branches; almost no task has an `--issue`; and landing does not merge lane branches at all. The merge keeper rebases/cherry-picks each queue range onto the shared remote (burst2-a, authoritative since 10-07; GitHub is a mirror) so main gets NEW shas, the lane branch is never an ancestor of main (patch-id matches, e.g. "landed as 885fae57 (patch-id verified)"), and the local `~/dev/minidregg` clone sweep reads is stuck at 4ef4e808 while main is e0a8ba21. The LOG and `queue/*.txt` name lanes, never task ids (only 58 of the 560 open task ids appear anywhere in the queue files), and no task used `cv task propose`, so cv never observed a patch-id. Meanwhile 85 open tasks ARE already cited by id in main commit messages ("cites cv 01a0f627-4a20"), which a sweep that read `git log origin/main` would have caught for 43 of the 97 landed rows.

Concrete proposal: (1) add a `closes: <task-id>[, ...]` field to the queue/<lane>.txt format (README.txt) and make the lane brief fill it from its own task; (2) the keeper LOG line becomes `LANDED <main sha> <batch> closes=<ids>` and the keeper (or a post-land hook in the pipeline that already runs `fetch-artifacts`/`relay`) runs `cv task done <id> --observed <main sha>` only after `git merge-base --is-ancestor <tip> origin/main`; (3) adopt a `Closes-Task: <id>` commit trailer (the repo already uses `(cv 01a...)` informally) and teach `cv task sweep --repo R --remote origin/main --trailers` to list every non-terminal task whose full id or 13-char prefix appears in a commit body on the remote main, plus the queue/ LOG `closes=` lines, printing the commit; (4) point sweep at the shared remote, not a local clone, and make `cv task open --lane <name>` record the lane so a LANDED queue line for that lane lists its tasks as candidates even without a trailer; (5) for tasks that name a checkable artifact, open them with `--check-cmd 'git -C R grep -q <token> origin/main'` so `cv task done` verifies itself. Sweep stays advisory (never closes); the keeper hook is the only auto-closer and only for ids the lane declared.
