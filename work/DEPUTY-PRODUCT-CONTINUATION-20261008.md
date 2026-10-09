# DEPUTY-PRODUCT continuation (2026-10-08, fresh instance after usage wall)
Prior record: work/CXO-EXPERIMENT-3.md. Train prod GREEN e939e557.

## 15:10Z
- prod-spk: WORKING on root ruling (typed read-only `volumes-status <store-id>` helper verb + cross-store plant). Budget raised 20M->30M (was at 15.7M).
- dregg-infra: neither edge/mini-certify nor edge/mini-wip-split started (no branch, no WIP-HELD.diff; WIP still uncommitted in ~/dev/dregg-infra, 27 entries).
- Box mirror created: burst3-a:/srv/git/dregg-infra.git (main=17674a3 = origin/main). Lane clone /srv/lanes/infra-certify/src branch lane/infra-certify.
- SPAWNED infra-certify (gpt-6.1-sol, 15M, --no-push, --allow edge/mini/**), brief scratchpad prod/certify.md: mini-certify script+service+timer (clock-tick custody), install refuses without `mini checkpoint`, health headroom, genesis-params .clock v2, jcertify.sh journey (>=600 writes) + plant (no certifier -> red at 257). Final run needs a clock-v2 artifact set: publish after rebase.
- TODO: (1) spk submit -> verify, merge. (2) rebase train onto dcab86da, publish-artifacts, full gate (run-gate-burst.sh) -> ROOT. (4) growth stall / HOST-UPGRADE / exchange (ask ROOT for fn bin copy).

## 16:05Z
- Hub reinstalled twice by ROOT (1ca975b: journey/ regex false positive fixed, rebase/unprotect/allow_dirty, INTERRUPTED; then job cap 8). cxo bugs reported: restart orphans job processes (I killed my 3 jcertify pgids), no cancel verb -> ROOT queued fixes.
- infra-certify: authorized adapting mini-clock-tick to current CLI (dedicated clock subject, --capability); jcertify cut to 320 records, serial jobs, wall bound, per-write wall_s column. Contended run: 201 creates in 32 min (~9.5 s/write, rising) -> if it reproduces UNCONTENDED, send the curve to DEPUTY-KERNEL (growth item).
- prod-spk: two-world journey rerun in flight (budget 30M, ~18M used).

## 16:55Z
- Merged GitHub main dcab86da into train prod (ref lane/main-dcab86da on /srv/git/minidregg.git) -> TRAIN_GREEN 7220394b. Published artifact set /srv/artifacts/7220394bae5c72f1ae8468ed7745bdb8547c1cc9 (label next; 421 s) -> given to infra-certify.
- prod-spk SUBMIT 5d23a239 (38 files). Deputy check: two-world PASS uid 1001 (j475058235), both cross-world plants RED with mutation asserted, unit-name plant RED; sudoers rule `#uid ALL=(root) NOPASSWD: <abs helper>`, helper checks euid0 + current_exe==registry.helper + SUDO_UID==registered operator + per-store registry custody; teardown left no sudoers/registry/mount. Waivers read (del-assert replacements, one ignore-test false positive). Merged -> train 0ea31db5, umbrella pending.
- NEXT: TRAIN_GREEN -> fresh gate lane run-gate-burst.sh -> ROOT sha. Retire prod-spk.

## 17:00Z
- TRAIN_GREEN 0ea31db5 (prod-spk merged); prod-spk retired.
- FULL GATE started: fresh lane /srv/lanes/prod-gate (mk-lane.sh), HEAD 0ea31db5, `run-gate-burst.sh /srv/lanes/prod-gate dcab86da… prod1`; results /srv/lanes/prod-gate/logs/gate-prod1.{summary,out,done|aborted}.
- Uncontended create curve (1.0 s @1 → 24.3 s @250, linear per create => quadratic) sent to DEPUTY-KERNEL. cxo `cancel` not yet installed (I kill pgids by hand).

## 17:20Z
- infra-certify DONE: ~/dev/dregg-infra branch edge/mini-certify = 7c28bf7 (message amended by me: flag day + Closes-Task 01a11be4-28a6). ROOT told Ember to push. Worker retired. WIP split NOT started (Ember's call).
- Spawned (--force, ROOT: spend the window): prod-hostup (HOST-UPGRADE; told to add `run.sh upgrade --manifest N1 --state S` operator verb, plant in plant script), prod-exch (exchange row vs LOCAL fn from /srv/fnbin/6679dae0e). Sets READY: e0a8ba21, 7220394b, 0ea31db5.
- GATE prod1 (0ea31db5) still running; reds so far: build-surfaces (source drift Assurance/NativeAcceptedFixtureData.lean -> regen protocol/lean-build-surfaces.json), unit-tests (spk python tests test_spk_ingest_namespace, test_ws_continuity_fixture: prod-spk fallout), objective-proofs (17 rows unpinned: check-objective-proofs.sh proofs --pin). Plan: one mergefix worker on /srv/lanes/train-prod/src after gate done.
- Later: jcertify growth-aware rerun after kern-grow's incremental root cache lands.

## 17:28Z
- prod-exch SUBMIT 1b779ad0 (30 files, mostly evidence 132K): local fn 6679dae0e at 8192 MiB dynamic space (SBCL_USER_ARGS), runner PASS x2, wrong-owner-key plant RED. Verified, retired. MERGE PENDING (after gatefix).
- prod-hostup SUBMIT 9104331a (5 files: run.sh upgrade verb + candidate_require_stopped, jhostupgrade.sh, plant, row_hostupgrade): F->G reopen PASS; E->F FAIL (head-anchor refusal, StoreEpoch identical across clock flag day) = correct red; plant stops on "epochs identical". MERGE PENDING. Same worker now on EPOCH FIX: derive StoreEpoch schema-refs from codec content (Compiler/DurableCheckpointCodec.lean; unprotected one-shot; budget 30M; umbrella required but NOT hub-enforced on that lane -> check ticket). DEPUTY-KERNEL: file is ours; derivation must cover kern-oom's ACTIVITY/REJECT/v2 + RECORDED-FAILURE/v2 tags.
- prod-gatefix working in train lane: a122 load_exact restated (bound premises) approved IF a refusal-of-boundless theorem is named.

## 17:37Z
- gate prod1 (0ea31db5) DONE red=4: build-surfaces, unit-tests (2 spk), objective-proofs (7466 redefined/24 restated, all 93e18aac), deploy-scripts (test-lane-build stale since m7). prod-gatefix fixed all 4 (aaf89764; restated 24 reviewed verbatim in its WORKLOG, load_exact domain restriction backed by Kernel.ClockCellDomain.load refusal; waiver admit: on ledger .admit names). Kept alive (idle) for gate2 reds.
- Train: aaf89764 recheck GREEN -> merged prod-exch 1e313e23 GREEN -> merged prod-hostup(9104331a) 5896a594 GREEN.
- GATE prod2 started at 5896a594: /srv/lanes/prod-gate2/logs/gate-prod2.*; red=0 -> send ROOT the sha.
- prod-hostup on epoch registry design (low tag module + Lean census check; kern-owned exceptions listed and self-verified); DEPUTY-KERNEL informed.

## 17:58Z MILESTONE
- GATE prod2 red=0 at 5896a5945dbce07d17dbbb5b5834318b0f64656e (31 checks, umbrella PASS). Sent to ROOT for push. prod-gatefix retired.
- Live: prod-hostup (epoch registry). Next: jcertify growth-aware rerun after kern-grow cache lands (ROOT); more product items from SHIP-PLAN §B as slots free (spend window per ROOT).

## 20:05Z (after Claude usage wall 18:05-20:02)
- Train prod LANDED: GitHub main = 5896a594 (ROOT pushed).
- prod-hostup had stalled at 17:30 (no edits). Rebased its lane onto 5896a594 (cxo rebase), resumed on the epoch registry (a137). Its SUBMITTED sha 9104331a was the EARLIER range (already in main).
- Spawned prod-v4 (gpt-6-astra, 25M, umbrella default) on SPK v4 replay (P4/R7). journey-rows NOT in its allow (default-protected): unprotect when it asks.
- Waiting: kern-grow cache landing -> growth-aware jcertify rerun (dregg-infra edge/mini/journey/jcertify.sh with births, curve vs bar).

## 21:55Z
- prod-hostup epoch work: new module Compiler/PersistedCodecTagCensus.lean (Lean census), ConsentAnchor pins + Compiler.lean imports (ConsentAnchor was OUTSIDE the umbrella closure: its storeEpoch pins never built in the gate — finding), fixture re-emit authorized via generator. Snapshot of its dirty tree -> commit 6888c832 (ref lane/snap-prod-hostup-1; shared remote accepts lane/* only) -> set /srv/artifacts/6888c832... READY (publish needs a WARM_TREE at TIP for non-GitHub shas: made /srv/lanes/snap-hostup via mk-lane).
- prod-v4 (astra) working: replay already fixed in base; real blocker grain.rs start selector (approved fix); provision.sh missing clockGenesisNow (fix at source, real time).
- DEPUTY-KERNEL hand-bumps schema-refs v6 in kern-pole; second lander converts to module constants.

## 22:00Z
- prod-v4 SUBMIT a4a2af4d (7 files): theorem CompletionAtV4.replay_lists_include (#assert_axioms), jspk1 rewritten to user-broker contract, provision.sh clockGenesisNow=$(date +%s), plant event72 omission RED at R7-stop-retry; grain.rs selector suspicion withdrawn. Merged -> train prod f5a870c2 GREEN. Retired.
- Spawned prod-demo1 (astra, 30M) DEMO-APP D1 (world/commission packages + CB1/CB5/CB7 + row + plant) from f5a870c2. Expect scope asks for Lean registration location / journey-rows (unprotect).
- cxo LONG_RX still refuses reads naming objective-native-acceptance / generate.sh paths (hostup 21:03, 21:51): report to ROOT with next batch.

## 23:10Z
- prod-hostup: switched to lean design (bidirectional census equality, registry under Compiler/, Kernel literal conversions reverted; 7 files). Snapshot 2 = 0caf6892 (lane/snap-prod-hostup-2) -> set /srv/artifacts/0caf6892... READY. Waiver approved: del-thm seedEpoch_v1_refused (retained line 373 as specialization). Budget 45M. Pending: fixture generator vs set, final umbrella, E->new refuse, plants, SUBMIT.
- prod-demo1: charged lawDenied submits hang 600 s + Host restart on 0ea31db5 = Nat.pair encoding class (DEPUTY-KERNEL), fixed in train kern 8e37e22d (StoreEpoch v6). Publishing set /srv/artifacts/8e37e22d... (log ~/deputy-prod/publish-8e37e22d.log); demo1 told to continue on it (answer a314 queued behind the publish ssh). D1 depends on train kern landing.
- cv task filed 01a11d86-325c (Objective domains lack explicit exits; Guild).

## 23:25Z ROOT corrections (4) applied
1. CAUSE: product rows never ran — pipeline-journeys.service runs stale box copy /srv/pipeline/scripts/journey-runner (02:27, no product_inputs); rows load from tip. Stopgap: installed main's runner+rows, service restarted (backup ~/deputy-prod/journey-runner.installed-0227.bak). Publishing main 5896a594 set (label main). ROOT: no push of main until a tip's STANDING run shows required rows PASS.
2. Empty-detail FAILs = same stale runner (no scope capture). prod-rowfix spawned (structural runner install + plant, FAIL causes, rerun call/send/domain/objectrecord alone, ONE clock-v2 genesisNow helper at candidate level, ssh-e2e trap masking).
3. Train prod RESET to 5896a594 (lane/train-prod force-pushed); prod-v4 a4a2af4d kept as lane/prod-v4 (OB-WORLD-DESIGN-20261008.md §8 subsumes SPK v4 retry under OB upgrade turns; P4 deletes v4 modules).
4. prod-demo1 PAUSED (not retired) until rows + kern-grow (THE BAR) land.
- sshe2e "keys deleted" = trap's unconditional last line masking `run.sh init` clockGenesisNowInvalid on genesis-params.example.json (clock-v2). welcomecontinuity same.

## 00:55Z DRAIN (ROOT/Ember: freeze for architectural rethink) — state of everything
Workers: NONE live. Retired: prod-demo1, prod-hostup, prod-rowfix (Codex auth revoked 00:26Z mid-turn: hub needs `codex login` + recopy ~/.cxo/codex-home), and earlier ones.

UNLANDED BRANCHES (shared remote burst3-a:/srv/git/minidregg.git unless noted):
- lane/train-prod = 5019da6a13b7369c32c5f62c9a7e94a04a8bf131 = main 5896a594 + prod-hostup 5ceb62d3 (derived StoreEpoch: Compiler/PersistedCodecTag{Registry,s,Census}.lean, build-time #assert_persisted_codec_tags equality reachable==registry both directions, schema-refs = cSHAKE digest; ConsentAnchor pins; Compiler.lean imports; fixture re-emit; FLAG DAY: every pre-change Store refuses by epoch -> re-genesis) + db426dbc (Host `minidregg-host store-epoch` verb; row_hostupgrade tests the tip: E e0a8ba21 -> $SET refuse, $SET reopen, previous same-epoch main or 98). Evidence: j501170384 (E->new refused naming schema-refs), j501191903 (reopen), j501218849/j501250521 (plants), umbrella b503349347; TRAIN_GREEN 5019da6a. FULL GATE prod3 red=3 (pin re-emits only): host-closure (2 entered PersistedCodecTag*), token-census (TokenCensus.lean:409), objective-proofs (655 added/7612 redefined/1 restated) -> need `check-host-closure.sh --update`, token census pin, `check-objective-proofs.sh proofs --pin` after reading the 1 restated. Standing run of 5019da6a in progress since 00:54Z (/srv/journeys/5019da6a.../).
- lane/prod-v4 = a4a2af4d (SPK v4 replay theorem + jspk1 rewrite + provision.sh clockGenesisNow) DROPPED from train per OB-WORLD-DESIGN §8 (P4 deletes v4). NOTE its provision.sh clockGenesisNow=$(date +%s) fix is NOT on main and is needed (JPAY3/4 fail "missing field clockGenesisNow").
- lane/snap-prod-demo1 = 256ca79a (Commission Board D1 WIP: world/commission/*, commission-demo-journey.py, plant-commission-double-pay.sh, row; base f5a870c2 INCLUDES dropped prod-v4; native 119/119 on kern set 8e37e22d (j501065732); umbrella never built; Guild exits finding cv 01a11d86-325c). Charged refusals hang on main (Nat.pair class) -> needs train kern.
- lane/snap-prod-rowfix = 3ad3a35d (UNREVIEWED WIP: scripts/pipeline/journey-launcher + install-journey-launcher, runner FAIL-cause capture (SystemdResult/OOMKills/peak via row parent, OOMPolicy=continue), deploy/candidate/params.sh + check-params-now.sh genesisNow helper wired into continuity/welcome/onboarding/newparticipant/m7/jhostupgrade drivers, ssh-e2e trap fix; .rowfix-evidence/ bloats the snapshot — drop it). Finding: call alone at 5896a594 = scope OOM 24G (10 kills, 2052 s).
- lane/snap-prod-hostup-{1,2,3} = publication snapshots only (sets /srv/artifacts/6888c832, 0caf6892, 6bd9b4a4). Disposable.
- dregg-infra (Mac ~/dev/dregg-infra) branch edge/mini-certify = 7c28bf7 on origin/main 17674a3 (mini-certify unit/timer, clock-tick v2, genesisNow fill, install refusals, health headroom; jcertify PASS j478466079 + plant RED@257 j478981926 on set 7220394b; Closes-Task 01a11be4-28a6). ROOT told Ember to push; box mirror burst3-a:/srv/git/dregg-infra.git. edge/mini-wip-split NOT started (Ember's call).

BOX STATE: /srv/pipeline/scripts/journey-runner+journey-rows hand-installed from main 5896a594 at 23:15 (stopgap; old copy ~/deputy-prod/journey-runner.installed-0227.bak); not refreshed by base advance (structural fix = snap-prod-rowfix WIP). Lanes I made: /srv/lanes/{prod-gate,prod-gate2,prod-gate3,snap-hostup}, plus worker lanes.

STANDING RUN main 5896a594 (00:53Z, PASS=45 FAIL=14 UNCONF=4) classification:
- call/send/domain/objectrecord: scope OOM 24G (Nat.pair charged-record class) -> PASS at train kern 8e37e22d.
- hostupgrade EF: expected red at main (epoch fix is in train prod).
- welcomecontinuity, sshe2e ("keys deleted" masks run.sh init clockGenesisNowInvalid), JPAY2/3/4 (missing clockGenesisNow): clock-v2 flag-day fallout in drivers/provision -> snap-prod-rowfix helper + prod-v4 provision.sh fix.
- m6grain: grain-journey.sh requires GRAINS_ROOT (prod-spk per-store change; row not updated) — real red.
- UNCONFIGURED: objective (no lean env), m7 (M7_REFERENCE unprovisioned), JPAY6 (mini-hermes-test-provider not in set), exchange (MINI_FN_LAUNCHER/CORE not in service env; /srv/fnbin/6679dae0e exists).

## FINAL STATE (01:05Z) — session stopped by drain
MAIN 5896a594 IS NOT DEPLOYABLE: its own standing run (/srv/journeys/5896a594.../results.tsv, 00:53Z) shows jpay2-4, welcomecontinuity, sshe2e (clock flag-day genesisNow fallout), m6grain (GRAINS_ROOT after prod-spk per-store change), hostupgrade-EF (stale StoreEpoch across the clock flag day) RED, and call/send/domain/objectrecord scope-OOM (fixed only in train kern).
Unlanded, all on shared remote burst3-a:/srv/git/minidregg.git:
- lane/train-prod 5019da6a — epoch range; BLOCKED: full gate prod3 red=3 (pin re-emits: host-closure, token-census, objective-proofs), no worker under the drain. Standing run of 5019da6a was in progress at stop (/srv/journeys/5019da6a.../) — read it first next session.
- lane/snap-prod-rowfix 3ad3a35d — UNREVIEWED WIP (runner launcher/install, FAIL causes, genesisNow helper, ssh-e2e trap). Blocked: unsubmitted, Codex auth revoked; drop .rowfix-evidence/ before use.
- lane/prod-v4 a4a2af4d — DROPPED (OB-WORLD-DESIGN §8); salvage only its provision.sh clockGenesisNow line.
- lane/snap-prod-demo1 256ca79a — Commission Board D1 WIP; blocked: paused by ROOT, needs train kern (charged-refusal hang) and umbrella; base includes dropped prod-v4 (rebase needed).
- lane/prod-hostup db426dbc, lane/prod-exch 1b779ad0 — already contained in train-prod / main respectively.
- dregg-infra edge/mini-certify 7c28bf7 (Mac ~/dev/dregg-infra and burst3-a:/srv/git/dregg-infra.git) — awaiting Ember's push to the real remote.
Codex hub: credential revoked 00:26Z; `codex login` on the Mac + recopy to burst3-a ~/.cxo/codex-home before any spawn.
