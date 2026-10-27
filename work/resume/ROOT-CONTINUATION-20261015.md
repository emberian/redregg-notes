# ROOT CONTINUATION — 2026-10-15 ~05:30Z (session b3795e84 / breadstuffs), for a context restart

Pointers, not a summary; the pointed files win. Previous index: ROOT-CONTINUATION-20261009.md (still valid for everything before 10-13).

## Read in this order
1. `work/PROTOCOL-20261009.md` (gen 1.2: performance is DESIGNED (docs/HP-DESIGN.md on lane/hp-design 4329b99c); large ranges; measure at range ends; `next` integration branch; design items are work; pause only for a weakened check, key custody, an outward act, a taste fork).
2. `work/ROLES.txt` (role → agent id → one-line state; `(spawned)`/`(running)` = live). Every lane has `work/<ROLE>-LOG.md` as its own continuation; successors start from the lane's log, never from ROOT's paraphrase.
3. `work/resume/STALL-WATCH-20261007.md` (hour-by-hour; tail -60 covers 10-14/15).
4. `work/INTEGRATOR-LOG.md` "STATE AT HANDOFF" (next = a5483db3 v2 published; v3 c3b667b4 landing; merge order; landing.sh recipe).
5. docs: `docs/WASTE-MODEL.md` (lane/cost-model), `docs/HP-DESIGN.md` (lane/hp-design), `work/FOLLIES-20261014.md`, `work/SINS-LEDGER-20261009.md`, `work/RETRO-20261008.md`.

## Boxes
- hbox: lane builds; FIFO slots /tank/dregg-build/pipeline/slots/with-lean-slot (3 slots × THREADS=2; memory- then IO-bound tonight; ARC capped 28G; box-changes.md has every root change + undo). GitHub deploy key (write, this repo) in ~/.ssh/minidregg-deploy. Mirrors: bundles/burst3-minidregg.git (old), bundles/burst4-minidregg.git (pull-burst4-remote.timer 10 min + ExecStartPost push-mirror-lanes-to-github.sh → GitHub lane/* + next).
- burst4-a: ssh -F ~/.ssh/burst4-20261015.conf burst4-a (ember@207.188.7.163; Latitude sv_R82A0y4Rga6mM, $1.52/h since 10-15 03:27Z; README work/latitude-burst4-20261015/). Warm base next a5483db3; FIFO slots /srv/pipeline/slots/with-lean-slot 6×4; shared remote /srv/git/minidregg.git with every lane ref; landings run here now.
- persvati: prepared in --no-root mode (lane/burst-noroot-host) under ~/mini-pipeline; BLOCKED on its 15%-free disk floor (12.9% free) → Ember (cv 01a13dc4).
- Public node dregg-workhorse: still the Oct-1 candidate; DEPLOY-3 unshipped (certifier branch in dregg-infra unpushed by Ember).

## main / next
- GitHub main = 7ffd6524 (10-14). next = a5483db3 (v2; rows all PASS). v3 (c3b667b4 + fixture re-emit) was landing (INTEGRATOR-2). v4 queue: guards e22cdedc, hyp-instances 357273ab, turn-log 7877e6e7, m6grain-hbox bb993cc9, spk-ns 1c7544af, hp-design, hp-6-sim 75887614, burst-noroot-host 9066a518, consent-model 963d9818, cost-model (in v3), hp-1-bounds (pending), census-review 2287f581 (+ census commit pending), floors (pending), state-at-c2 (pending), codec-shapes (pending), perf-memo (pending).
- Landing rule: gate red=0 AND no new non-PASS vs main's baseline on the same box AND required rows PASS/declared (known-red: fleetsign cv 01a13985 (fixed on lane/fleet-race-land, in next), JPAY6 cv 01a13c42-dc55, m6grain cv 01a13d9c-8a9d).

## Rulings in force (10-14/15), each logged in STALL-WATCH with its reason
no perf verdicts on loaded boxes (raw instruction counts compare; wall doesn't) · guards come from the INTENT's asserted pre-state (HP-6 finding) · checkpoint = World v1 {cells : CellTable, system : WorldSystemCodec, head}, no rootTree, open recomputes the root · the open never trusts MAC'd node digests (no honest-sealer premise) · eventBytes derived from the archive (nothing persisted as a number) · carries pay World storage · ledger: content-addressed closure hashing, decisions only for statement-level events, (d) vacuity plant kept · instrument self-tests only when the instrument changed · publish packs from the gate lane · births row = THE BAR, pending-required-when-green, judged only when quiet · growth nightly · no relaying through the Mac (hbox/burst4 direct; deploy key on hbox) · one sandbox shape (spk resident via the profiled bwrap) · client consent bases are own-computed only.

## Ember's open items
persvati disk (free ~40 GB or remove ~/mini-pipeline) · the consent-frontier MAC key (custody; CONSENT-MODEL Part B) · the moved Host-pin check (veto or keep) · pug issue #2 licence (AGPL Lean → Apache Rust port) · issue #1 issuer-cap choice · dregg-infra edge/mini-certify push · PR3-REPLY.md / ISSUE1-REPLY.md to post when the lanes reach main.

## 2026-10-15T05:10:12Z — 14-h check-in compiled (see STALL-WATCH same stamp)
- SPK-NS r5: m6grain PASS on hbox as mini-operator (lane/spk-ns 5919eb8b; ACL-aware exec check; install-user-world grants/revokes per-app-uid ACLs). Lane DONE; queue for next v4.
- CONSENT-MODEL-2 Part A plant passes (lane/consent-model 963d9818 on next a5483db3); real finding: State.available (metering budget) is bound by neither world root nor Admissible.
- STATE-AT-3 engine wired (burst4 lane/state-at-c2 edc02035); perf enabled on burst4 for its bench.
- TURN-LOG-3 CHARGE landed 7877e6e7; the 7 retained j1 Stores refuse by charge (expected) so pole/follower rows are EMPTY until step-2 re-emits Stores. TURN-LOG-4 building b1 on burst4; guards-from-intent = Turn.pins (cell, intent digest).
- CODEC-SHAPES 58b3ae50 pushed (item 3 pending c3). CENSUS-REVIEW waiting build 3. INTEGRATOR-2 on chain9 host build (next v3). PERF-MEMO, FLOORS, HP-1 building candidates.

## PAUSE 2026-10-15 ~06:50Z — usage wall (~9 h); burst4-a DELETED; all lanes paused. RESUME FROM HERE.
main = 7ffd6524 (unchanged). next = v3.2 2c27b08b (GitHub; v3.1 03d338ee landing died at publish on a seat clash, exit 11; v3.2 gate red=0 but NO landing verdict). hbox: chain12 umbrella (lane/v4-next b5fd9ee1) may still be running unattended (/tank/dregg-build/pipeline/lanes/integrator-next/chain.pid, logs/chain-b5fd9ee1.status). hbox builds/lanes trees still exist; burst4 trees are GONE (every commit is on GitHub; hbox mirror bundles/burst4-minidregg.git final pull 06:41Z; the mirror's lane refs may lag GitHub → fetch lanes from GitHub). No warm base at next exists on hbox: the first resume step is building one (next 2c27b08b) with with-lean-slot.
Paused lanes (branch = sha on GitHub; continuation file; successor's first step):
- INTEGRATOR: lane/v4-next b5fd9ee1 (v3fix-2 + consent-model 963d9818 + census-review merged); INTEGRATOR-LOG.md "STATE AT HANDOFF (INTEGRATOR-3 …)". First: read chain12; land v3.2 2c27b08b on hbox (landings ran on burst4; hbox pipeline is the fallback; land lane must contain 195506cb+2c27b08b seat-wait); then merge hp-1-bounds e59ea490 + floors (rebase branch) tips; NOT state-at-c2 (WIP commits).
- TURN-LOG-4: lane/turn-log dbb4f0f4 on GitHub (WIP: deletes Turn.absent on top of 45aadc74 guards-from-intent; built green 7429 jobs; world-sim gate NOT run). ROOT snapshot lane/turn-log-wip-root 77ad9540 is SUPERSEDED (delete the branch). TURN-LOG-LOG.md. Rulings in force: delete Turn.absent; carries next; keep HP-1's append check + decodeEntry (merge hp-1-bounds tip); then step 2.
- HP-1b: lane/hp-1-bounds e59ea490 (1a871252 overBound wire tag + OUTCOME v6; e59ea490 cellBytesMax 8 MiB, turnBytesMax=frameBytesMax; Lean green 7587 jobs; append plant refuses on the wire code 15; Rust build, candidate, rows, frame/follower plants NOT run; objective entries not drafted). HP-1-LOG.md "CONTINUATION (HP-1b, paused 10-15 06:50)". Then HP-5 ASSERT (note: lean_set_exit_on_panic needed for assertions to crash).
- CONSENT-3: lane/consent-model 1e3ad928 on 03d338ee (5fb20bc5 JPAY6 fix: legacy scalar twin deleted, consent names+USES providerServices, Kernel/ProviderRouteConsent.lean; 1e3ad928 grain-runtime legacy branch refusal; UNBUILT). CONSENT-MODEL-LOG.md "CONTINUATION 3". Then Part B with Ember's ruling: SUBKEY derived from the client consent key. cv 01a13c42-dc55 open. Rows were writing into real ~/.mini/consent-anchors on burst4 (50 files) → fix gives each row MINI_CONSENT_ANCHOR_DIR (unverified).
- FLOORS-2: lane/floors-rebase-wip 743fc5ce on 03d338ee (kernel + row fixes + seat-count replayed; objective pin + fixture re-emit + candidate + rows TO DO; lane/floors still f580e539 on next v1). FLOORS-LOG.md continuation. Ember: issuer cap ACCEPTED; relicense (issue #2) APPROVED; both replies (PR3-REPLY.md, ISSUE1-REPLY.md) APPROVED to post (ROOT posts ISSUE1 once floors reaches main; PR3 once perf-client's commit is on main — check first).
- CODEC-SHAPES: lane/codec-shapes e317c181 (items 1–3; rows PASS at 58b3ae50 incl. exchange; e317c181 moves StoreEpoch: re-genesis; objective draft NOT done; rows at e317c181 NOT run), lane/codec-shapes-rust b90b8403 (needs rebase; TWINS.md 65 dual labels). CODEC-SHAPES-LOG.md CONTINUATION. OPEN for Ember: opcode-13 codec-child blinding-key custody.
- CENSUS-REVIEW: lane/census-review 95861a59 (review DONE: 341 L1 / 21 defect+tasks / 28 not-a-token / 1 restricted; instrument WIP unbuilt: no L2 tier, explicit-index check, SelfTest.lean, defect-only-shrinks gate). CENSUS-REVIEW-LOG.md. First: build 3 (hbox census-review/build3.log).
- STATE-AT-3: lane/state-at-c2 f7c998b6 (3 WIP commits on a5483db3; umbrella green 13086 jobs; rows PASS; growth 1253 s; bench: past reads 2–3× faster at 30k, append unchanged; ratchet, squash, force-push as lane/state-at TO DO). STATE-AT-LOG.md "PAUSED 10-15". hbox source clone claude-lanes/state-at/rb branch c2.
- PERF-MEMO: lane/perf-memo 77355fdf on a5483db3 (memo builds green; tamper test ok; ratchet reasons in WIP gates commit, --pin not run; candidate/measure/rows NOT run; MINIDREGG_HOST_HELD=0 switch is a measurement control to delete after). PERF-MEMO-LOG.md CONTINUATION. hbox mirror has stale 493bc9c7 → fetch from GitHub.
- SPK-NS DONE 5919eb8b (m6grain PASS hbox). HP-1 DONE. CONSENT-MODEL-2 Part A DONE 963d9818.
Ember rulings 10-15 ~06:30Z: 1 Part B key = subkey; 2 issuer cap ok; 3 persvati continue to a 5% floor (Ember sweeps disk); 4 relicense approved; 5 both replies approved; 6 no nightly bar box — use burst4-class box in a quiet window (now: hbox quiet window or next burst); 7 dregg-infra no rush.
Teardown done: Latitude sv_R82A0y4Rga6mM deleted 06:47Z (HTTP 204, then 404); burst4 GitHub deploy key 166499838 deleted; hbox pull-burst4-remote.timer disabled (service/script/key left, logged in hbox box-changes.md). NOT removed: persvati ~/.ssh/box_peer + Host burst4-gate block (Ember's laptop; remove when awake). Box records: latitude-burst4-20261015/teardown-20261015-box-state.txt. burst-down's bulk evidence copy was NOT taken (derived data; commits are the record).
Next burst box: needs the burst-up recipe + 195506cb/2c27b08b in its tree + MINIDREGG_LEAN_SEATS=4 + PIPELINE_LANES in box.env + perf_event_paranoid=1 + a deploy key (record, remove at teardown).

## 10-17 RESUME POINT (hbox execution node; first compaction of this project at 01:06 local / ~08:06Z)

Read `cv show b3795e84-08d4-436c-9079-91d4e05687e9 --kind prompt,answer` for the back-and-forths; the compaction summary lost detail (Ember, 10-17). This section is the index, not the record; the record is STALL-WATCH-20261007.md and the lane logs.

**Where main is.** nanodregg main LIVES ON HBOX at `/tank/dregg-build/nanodregg/main`, per-layer worktrees `/tank/dregg-build/nanodregg/wt/<layer>`, origin github.com/emberian/nanodregg (public). `~/dev/nanodregg` on the Mac is a pull-only reader (`scripts/mac-pull`). Nothing builds, simulates, benches or commits on the Mac. Commits only via `scripts/commit` from a worktree AT main (it refuses a worktree behind main: `git checkout --detach main`, re-apply the edit; I hit this twice landing the README). main at 09:30Z: **3fbbd13** (README, ROOT) on 84c7c8c (CLIENT-2: PROTOCOL-17/20/21, ceilings split per binary) on 477a682 (LEDGER-4 credit line). hbox load 0.16; the box is otherwise Ember's (GPU art, fn's acl2).

**REGIME (read first; the only process rule):** /Users/ember/dev/redregg/work/WORK-RULES-20261027.md. A landing is: rebase on origin/main, build what you changed, run what you touched, push; GitHub origin/main is the truth. The whole is a periodic report (`scripts/converge` tells, never refuses, never reverts). Briefs carry the goal, the material, box safety and the landing rule, nothing else. Verification lives in nano's top-level Spec/. Lanes are kept running by value. One agent per worktree; a successor starts from its predecessor's own continuation. hbox: builds on the NVMe at swarm-build budgets and idle I/O; /tank is the HDD mirror holding the repo. Memory: ~/.claude/…/memory/feedback-how-we-work-on-nano.md.

**STATE real 10-27 (written for a restart).** nanodregg origin/main carries: the frontier landings of 10-26 (the contextual slot and the document; fork consistency, self-heads, certified heads read and checked, the authority fixed at genesis; generators incl. parametrised; claims checked beside the type; the agent's inbox and a real model answering the Bell; the meter and the oracle time-lock); the Spec/ layer (nine claims with top theorems and floors); the testground (the kernel in the browser; the lying writer; the hosted World), PUBLIC at https://emberian.github.io/nanodregg/ and packaged as tenant nd-testground of the Mini demo box (dregg-infra branch demo-vm; wss://nano.demo.dregg.online/ws; Ember chose co-hosting; the demo-box session owns DNS and the install). Built and landing by the new rule: graded effects (TYPES), claims on the wire (PCC), Req.caller + the registry (CTX), the writer's signing seed (TRUST), the World-bound join and retirement (RETIRE), the remaining Spec claims (SPEC), the badResult fix + republish + tarball (TESTGROUND), the README and docs rewrite (two Codex workers), the replacement of scripts/commit by the one-rule landing (FIX-QUEUE). Each lane's report is codex/<LANE>.report.md and its continuation beside it; the board is codex/FRONTIER-BOARD.md; Ember's open decisions are `cv task inbox ember`. Records: promo/FRONTIER-NIGHT-20261026.md, readers/VERDICT-20261024.md, promo/TOPLEVEL-SPEC.md, promo/DESIGN-*.md.

**History (dates and hashes only; the facts live in decisions/*.md on main and the memory file 'what nanodregg is'):**
- AT ~22: 1b831da, 1ed7867, 5eb9b30, 71379a1, 9dd1e8c
- real 10-26 ~07: (no hashes)
- real 10-25 ~00: 791f8c8, a306536, ad90a47, f4e803b
- real 10-24 ~03: 231af0e, e2eecce, e7c2b13, f9657bd
- real 10-23 ~13: 00ed907, 231af0e
- real 10-23 ~05: 100ad08, 1fc905f, 28e2d88, 2d3bf14, 4916f3a, 4d4bb28, 50e8805, 51089fb, 528c9a9, 613bdca, 98bf479, b4a7f38, c066b93, d0d67f1, e2905e7, e33a9b1, e9c126f
- real 10-21 ~17: 71db964, 7e02852, a0eb75f, d7989d9, f8d04ac
- real 10-21 ~01: 06da84f, 0a8c780, 19635c9, 1b6cd0d, 2b7bc39, 3bd8c12, 3ff2657, 68e704d, 6fd29f8, 710dd08, 7473d77, 7e02852, 80419cf, 832a815, 8a1a727, 998f75a, a0eb75f, ad96bab, b72e5a8, bb77db4, c58757f, de03530, ed34b1b, f15b70f, f48965e
- real 10-20 19: 2b6e5e1
- 10-22 ~09: (no hashes)
- 10-21 ~12: 12ab757, 1e90c0b, 220f0ed, 224e9fe, 285fdc2, 50bf961, 5cfd5cf, 5fff199, 6527d9f, 6f28e4a, 7c09186, 7c94e5e, 8c2c5fd, 96c6881, 9ced635, 9d5b293, a1ca640, aa7fa1d, bd39f78, bfdff2d, c0cd535, c1166ce, c7f455e, cdc0e9a, da33440, ea52a4a
- 10-21 ~04: 1a6163b, 1e90c0b, 285fdc2, 5fff199, 6527d9f, 7c09186, 9d5b293, c0cd535, da33440
- 10-21 ~02: 1a6163b
- 10-19 LATE (~03: 0e1b027, 148ac60, 2ac395e, 2d2189e, 7de131e, 9df02da, a130087, b9ce5a7, c18e028, ce23f2e
- 10-19 EVENING (~22: 03943ee, 0e1b027, 0e8e333, 148ac60, 43ab42a, 5771c74, 5f7c58d, 748b11d, 7932cb3, 7de131e, 85cc80e, b9cd50f, bbb7e5e, c9d3b4c, cf79591, de718bf, f82a6b0
- 10-19 MORNING (~10: 174789f, 4573cce, 56f4689, 5f9edc2, 8ad3982, b040f21, b9cd50f, d377d5b
- 10-19 ~04: 10fd373, 2d4c38d, 2d76795, 2f5a201, 38d94e1, 42c261b, 53af302, 6df6a3f, 815a031, a38b84b, c80db80
- 10-19 ~00: 06876d1, 0a808e4, 0c63e85, 2db5853, 38d94e1, 42c261b, 46c826e, 6df6a3f, 70eb282, a38b84b, d1c3fbb
