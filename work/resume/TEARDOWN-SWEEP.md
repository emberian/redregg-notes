# TEARDOWN-SWEEP (2026-10-04)

Bundles: persvati:/home/ember/workbox/claude-lanes/bundles/teardown/<box>-<lane>__<repo>.bundle (+ .mainsha = GitHub main sha excluded as prerequisite; bundle holds branches NOT ancestors of main, excluding main's history). Evidence: persvati:/home/ember/workbox/claude-lanes/teardown-evidence/<box>/<lane>/ ; box-level in _box, _journeys, _artifacts; non-git dirs (small files <5MB) in _nogit-dirs.
WIP branches: <branch>-teardown-wip in each lane repo, created for every lane with wip=y (note: includes untracked non-ignored files; may include junk). They are INSIDE the bundles.
Boxes: gate=67.213.124.13 lane1=162.43.189.7 e2e=152.236.4.24

## gate
LANE checkpoint-invariant__src cur=lane/checkpoint-invariant wip=y main_fetched=y branches=[lane/checkpoint-invariant lane/checkpoint-invariant-teardown-wip] bundle_bytes=49972
LANE checkpoint-invariant-v__src cur=lane/checkpoint-invariant-wip wip=y main_fetched=y branches=[cand5 lane/checkpoint-invariant lane/checkpoint-invariant-old lane/checkpoint-invariant-wip lane/checkpoint-invariant-wip-teardown-wip] bundle_bytes=68256
LANE deploy3b__src cur=main wip=y main_fetched=y branches=[lane/deploy3b main main-teardown-wip] bundle_bytes=16442
LANE fairy-fix__src cur=lane/fairy-fix wip=y main_fetched=y branches=[cand5 lane/fairy-fix lane/fairy-fix-teardown-wip] bundle_bytes=33471
LANE fairy-fnwire__src cur=lane/fn-wire-2 wip=y main_fetched=y branches=[cand5 lane/fn-wire lane/fn-wire-2 lane/fn-wire-2-teardown-wip lane/fn-wire-q lane/fn-wire-visit] bundle_bytes=40319
LANE fairy-ship__src cur=main wip=y main_fetched=y branches=[cand5 lane/fairy-ship main main-teardown-wip] bundle_bytes=41297
LANE fk-2__src cur=fkcand wip=y main_fetched=y branches=[cand5 fkcand fkcand-teardown-wip] bundle_bytes=131261
LANE forcing-transparent__src cur=lane/forcing-transparent wip=y main_fetched=y branches=[lane/activity-native-2 lane/forcing-transparent lane/forcing-transparent-teardown-wip] bundle_bytes=56428
LANE forcing-transparent-v__src cur=lane/forcing-transparent wip=y main_fetched=y branches=[cand5 lane/forcing-transparent lane/forcing-transparent-old lane/forcing-transparent-teardown-wip lane/forcing-transparent-wip ref-fairy-fix] bundle_bytes=86032
LANE law-bypass__src cur=lane/law-bypass wip=y main_fetched=y branches=[cand5 lane/law-bypass lane/law-bypass-teardown-wip] bundle_bytes=476224
LANE laws-pin__src cur=lane/laws-pin wip=y main_fetched=y branches=[lane/laws-pin lane/laws-pin-teardown-wip laws-pin-persvati] bundle_bytes=13696
LANE laws-receiver__src cur=lane/laws-receiver-final wip=y main_fetched=y branches=[lane/laws-receiver lane/laws-receiver-final lane/laws-receiver-final-teardown-wip lane/laws-receiver-visit lane/laws-receiver-wip] bundle_bytes=71831
LANE mk-gate-c14__src cur=main wip=y main_fetched=y branches=[cand14 cand5 main main-teardown-wip] bundle_bytes=476310
LANE OB5-FAREOO-MATURATION__src cur=lane/OB5-FAREOO-MATURATION wip=y main_fetched=y branches=[cand5 lane/OB5-FAREOO-MATURATION-teardown-wip] bundle_bytes=25637
LANE pipeline-infra__src cur=lane/pipeline-infra wip=y main_fetched=y branches=[lane/pipeline-infra lane/pipeline-infra-teardown-wip] bundle_bytes=14155
LANE retention-payers__src cur=lane/retention-payers wip=y main_fetched=y branches=[lane/retention-payers lane/retention-payers-detached-wip lane/retention-payers-teardown-wip] bundle_bytes=25927
LANE retention-payers-v__src cur=lane/retention-payers wip=y main_fetched=y branches=[cand5 lane/retention-payers lane/retention-payers-old lane/retention-payers-teardown-wip lane/retention-payers-wip] bundle_bytes=98774
LANE seats-native__src cur=lane/seats-native wip=y main_fetched=y branches=[lane/seats-native lane/seats-native-teardown-wip lane/seats-native-wip] bundle_bytes=84114
LANE seats-native-v__src cur=lane/seats-native-v2 wip=y main_fetched=y branches=[cand5 lane/seats-native lane/seats-native-old lane/seats-native-partial lane/seats-native-v lane/seats-native-v2 lane/seats-native-v2-teardown-wip lane/seats-native-wip] bundle_bytes=177371
LANE upgrade__src cur=lane/upgrade wip=y main_fetched=y branches=[lane/upgrade lane/upgrade-teardown-wip] bundle_bytes=23896
LANE upgrade-v__src cur=lane/upgrade wip=y main_fetched=y branches=[cand5 lane/upgrade-old lane/upgrade-teardown-wip] bundle_bytes=30124
LANE W06b-SERVED-LOG-CONSENT__src cur=lane/W06b-wip wip=y main_fetched=y branches=[cand5 lane/W06b-wip lane/W06b-wip-teardown-wip] bundle_bytes=38626
LANE W09-DREX-SEATS__src cur=lane/W09-DREX-SEATS wip=y main_fetched=y branches=[cand5 lane/W09-DREX-SEATS lane/W09-DREX-SEATS-teardown-wip] bundle_bytes=43270
LANE W15-TRAFFIC-V13__src cur=lane/W15-TRAFFIC-V13 wip=y main_fetched=y branches=[cand5 lane/W15-TRAFFIC-V13 lane/W15-TRAFFIC-V13-teardown-wip relay/traffic] bundle_bytes=76208
LANE w17-machine-ops__src cur=lane/ob2-finish wip=y main_fetched=y branches=[cand5 lane/ob2-finish lane/ob2-finish-teardown-wip lane/w17-machine-ops] bundle_bytes=107605
LANE W18-STEPRAW-LINEAR__src cur=lane/W18-STEPRAW-LINEAR-wip wip=y main_fetched=y branches=[cand5 lane/W18-STEPRAW-LINEAR-wip lane/W18-STEPRAW-LINEAR-wip-teardown-wip] bundle_bytes=27825
LANE W24-SDK-ROUTES__src cur=main wip=y main_fetched=y branches=[cand5 lane/W24-SDK-ROUTES main main-teardown-wip] bundle_bytes=52441
LANE W25-CORE4-SUMS-FIX__src cur=lane/W25-CORE4-SUMS-FIX wip=y main_fetched=y branches=[cand5 lane/W25-CORE4-SUMS-FIX lane/W25-CORE4-SUMS-FIX-teardown-wip] bundle_bytes=32143
LANE W26-DEEP-EVALUATES-UNIQUE__src cur=lane/W26-DEEP-EVALUATES-UNIQUE wip=y main_fetched=y branches=[cand5 lane/W26-DEEP-EVALUATES-UNIQUE lane/W26-DEEP-EVALUATES-UNIQUE-teardown-wip] bundle_bytes=32927
LANE W30-CORE4-DIGEST__src cur=lane/W30-CORE4-DIGEST wip=y main_fetched=y branches=[cand5 lane/W30-CORE4-DIGEST lane/W30-CORE4-DIGEST-teardown-wip lane/W30-pre-rebase relay/ports-a relay/w17 relay/w17b] bundle_bytes=114648
LANE W31-RETIRE-DECIDED-VIEWS__src cur=lane/W31-RETIRE-DECIDED-VIEWS wip=y main_fetched=y branches=[cand5 lane/W31-RETIRE-DECIDED-VIEWS lane/W31-RETIRE-DECIDED-VIEWS-teardown-wip relay/agreement-2c] bundle_bytes=47062
LANE W34-RECURSIVE-PLAN-DATA__src cur=lane/W34-RECURSIVE-PLAN-DATA-wip wip=y main_fetched=y branches=[cand5 lane/W34-RECURSIVE-PLAN-DATA-wip lane/W34-RECURSIVE-PLAN-DATA-wip-teardown-wip] bundle_bytes=33207
Artifacts (/srv/artifacts/*, ~446M each tree) NOT copied; only SHA256SUMS+PROVENANCE copied.

## lane1
LANE activity-route__src cur=lane/activity-route wip=y main_fetched=y branches=[base2 lane/activity-route lane/activity-route-old lane/activity-route-r lane/activity-route-teardown-wip] bundle_bytes=87869
LANE elaborator-2__src cur=lane/elaborator-2 wip=y main_fetched=y branches=[lane/elaborator-2 lane/elaborator-2-teardown-wip] bundle_bytes=54673
LANE fairy-green__src cur=lane/fairy-green wip=y main_fetched=y branches=[lane/fairy-green lane/fairy-green-teardown-wip] bundle_bytes=20655
LANE fk-v1__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=33552
LANE fn-direct__src cur=lane/fn-direct wip=y main_fetched=y branches=[lane/fn-direct lane/fn-direct-teardown-wip] bundle_bytes=55053
LANE journey-reds__src cur=lane/journey-reds wip=y main_fetched=y branches=[cand5 lane/journey-reds lane/journey-reds-teardown-wip lane/journey-reds-wip] bundle_bytes=32460
LANE native-exercise-2__d4 cur=lane/ne2-d4 wip=n main_fetched=y branches=[lane/native-exercise-2 lane/native-exercise-2-wip lane/ne2-d4 visit/ne2-pre-rebase visit/ne2-wip-pre-rebase] bundle_bytes=130097
LANE native-exercise-2__src cur=lane/native-exercise-2 wip=y main_fetched=y branches=[lane/native-exercise-2 lane/native-exercise-2-teardown-wip lane/native-exercise-2-wip lane/ne2-d4 visit/ne2-pre-rebase visit/ne2-wip-pre-rebase] bundle_bytes=130659
LANE OB1-SURFACE-SEMANTICS__src cur=lane/OB1-SURFACE-SEMANTICS wip=y main_fetched=y branches=[cand5 lane/OB1-SURFACE-SEMANTICS lane/OB1-SURFACE-SEMANTICS-teardown-wip] bundle_bytes=36805
LANE object-record__src cur=lane/object-record-r3 wip=y main_fetched=y branches=[lane/metering-disposal lane/object-record-r2 lane/object-record-r2m lane/object-record-r3 lane/object-record-r3-teardown-wip] bundle_bytes=130779
LANE ports-a__src cur=lane/ports-a wip=y main_fetched=y branches=[lane/ports-a lane/ports-a-teardown-wip lane/ports-a-wip] bundle_bytes=30781
LANE ports-b__src cur=lane/ports-b wip=y main_fetched=y branches=[lane/ports-b lane/ports-b-teardown-wip lane/ports-b-wip visit/ports-b-pre-rebase] bundle_bytes=42313
LANE retention-payers__src cur=lane/retention-payers wip=y main_fetched=y branches=[lane/retention-payers lane/retention-payers-teardown-wip lane/retention-payers-wip] bundle_bytes=36131
LANE rollup__ci-wt cur=lane/rollup-ci wip=n main_fetched=y branches=[cand5 lane/ci-wip lane/rollup lane/rollup-ci lane/rollup-pre-squash lane/rollup-sn lane/rollup-sn-old lane/rp-wip lane/sn-wip] bundle_bytes=256238
LANE rollup__sn-wt2 cur=lane/rollup-sn wip=n main_fetched=y branches=[cand5 lane/ci-wip lane/rollup lane/rollup-ci lane/rollup-pre-squash lane/rollup-sn lane/rollup-sn-old lane/rp-wip lane/sn-wip] bundle_bytes=241742
LANE rollup__src cur=lane/rollup wip=y main_fetched=y branches=[cand5 lane/ci-wip lane/rollup lane/rollup-ci lane/rollup-pre-squash lane/rollup-sn lane/rollup-sn-old lane/rollup-teardown-wip lane/rp-wip lane/sn-wip] bundle_bytes=327254
LANE rollup-base__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=33556
LANE schema-v2-2__src cur=lane/schema-v2-2 wip=y main_fetched=y branches=[lane/schema-v2-2 lane/schema-v2-2-teardown-wip lane/schema-v2-2-visit lane/schema-v2-2-wip] bundle_bytes=55818
LANE schema-v2-2-main__src cur=detached-3b709c87 wip=y main_fetched=y branches=[detached-3b709c87-teardown-wip] bundle_bytes=547
LANE schema-v2-2-q__src cur=lane/schema-v2-2 wip=y main_fetched=y branches=[cand5 lane/schema-v2-2 lane/schema-v2-2-teardown-wip] bundle_bytes=92304
LANE scholar-fn__src cur=main wip=y main_fetched=y branches=[main main-teardown-wip] bundle_bytes=13697
LANE W02-PAY-WEEK-EXACT__src cur=lane/W02-PAY-WEEK-EXACT wip=y main_fetched=y branches=[cand5 lane/W02-PAY-WEEK-EXACT lane/W02-PAY-WEEK-EXACT-teardown-wip main] bundle_bytes=38435
LANE W04-SPK-V4-LAND__src cur=lane/W04-SPK-V4-LAND wip=y main_fetched=y branches=[cand5 lane/W04-SPK-V4-LAND lane/W04-SPK-V4-LAND-teardown-wip relay/spk] bundle_bytes=146149
LANE W05-REWRITER-CODECS__src cur=main wip=y main_fetched=y branches=[cand5 lane/W05-REWRITER-CODECS main main-teardown-wip] bundle_bytes=38618
LANE W13-DOCS-CURRENT__src cur=lane/W13-DOCS-CURRENT wip=y main_fetched=y branches=[cand5 lane/W13-DOCS-CURRENT lane/W13-DOCS-CURRENT-teardown-wip] bundle_bytes=63355
LANE W14-WEBSITE-REGEN__src cur=lane/W14-WEBSITE-REGEN wip=y main_fetched=y branches=[cand5 lane/W14-WEBSITE-REGEN lane/W14-WEBSITE-REGEN-teardown-wip] bundle_bytes=76676
LANE W16-MPC-429-TIMED__src cur=lane/W16-MPC-429-TIMED wip=y main_fetched=y branches=[cand5 lane/W16-MPC-429-TIMED lane/W16-MPC-429-TIMED-teardown-wip main relay/mpc] bundle_bytes=964035
LANE W19-C-DIFF-GENERATOR__src cur=lane/W19-C-DIFF-GENERATOR wip=y main_fetched=y branches=[cand5 lane/W19-C-DIFF-GENERATOR lane/W19-C-DIFF-GENERATOR-teardown-wip] bundle_bytes=190703
LANE W20-GATE-MUTATION__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=29483
LANE W20-GATE-MUTATION-b__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=39812
LANE W20-GATE-MUTATION-c__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=26074
LANE W20-GATE-MUTATION-d__src cur=main wip=y main_fetched=y branches=[cand5 main-teardown-wip] bundle_bytes=25514
LANE W20-GATE-MUTATION-fix__src cur=lane/W20-GATE-MUTATION wip=y main_fetched=y branches=[cand5 lane/W20-GATE-MUTATION lane/W20-GATE-MUTATION-teardown-wip] bundle_bytes=46215
LANE W21-BYZ-TARGETED__src cur=lane/W21-BYZ-TARGETED-wip wip=y main_fetched=y branches=[cand5 lane/W21-BYZ-TARGETED lane/W21-BYZ-TARGETED-wip lane/W21-BYZ-TARGETED-wip-teardown-wip] bundle_bytes=37233
LANE W23-PRE-EXISTING-REDS__src cur=lane/W23-PRE-EXISTING-REDS wip=y main_fetched=y branches=[cand5 lane/W23-PRE-EXISTING-REDS lane/W23-PRE-EXISTING-REDS-teardown-wip] bundle_bytes=31389
LANE W27-HYBRID-PQ-FOLLOWUPS__src cur=lane/W27-HYBRID-PQ-FOLLOWUPS wip=y main_fetched=y branches=[cand5 lane/W27-HELD-fn-tls lane/W27-HYBRID-PQ-FOLLOWUPS lane/W27-HYBRID-PQ-FOLLOWUPS-teardown-wip lane/W27-HYBRID-PQ-FOLLOWUPS-wip lane/W27-q] bundle_bytes=77386
LANE W27-HYBRID-PQ-FOLLOWUPS__src-i2 cur=lane/W27-HYBRID-PQ-FOLLOWUPS-wip wip=n main_fetched=y branches=[cand5 lane/W27-HELD-fn-tls lane/W27-HYBRID-PQ-FOLLOWUPS lane/W27-HYBRID-PQ-FOLLOWUPS-teardown-wip lane/W27-HYBRID-PQ-FOLLOWUPS-wip lane/W27-q] bundle_bytes=77386
LANE W27-HYBRID-PQ-FOLLOWUPS__wt-held cur=lane/W27-HELD-fn-tls wip=n main_fetched=y branches=[cand5 lane/W27-HELD-fn-tls lane/W27-HYBRID-PQ-FOLLOWUPS lane/W27-HYBRID-PQ-FOLLOWUPS-teardown-wip lane/W27-HYBRID-PQ-FOLLOWUPS-wip lane/W27-q] bundle_bytes=77386
LANE W27-HYBRID-PQ-FOLLOWUPS__wt-q cur=lane/W27-q wip=n main_fetched=y branches=[cand5 lane/W27-HELD-fn-tls lane/W27-HYBRID-PQ-FOLLOWUPS lane/W27-HYBRID-PQ-FOLLOWUPS-teardown-wip lane/W27-HYBRID-PQ-FOLLOWUPS-wip lane/W27-q] bundle_bytes=77386
LANE W29-SUM-TYPED-ENTRY-ARGS__src cur=lane/W29-SUM-TYPED-ENTRY-ARGS-wip wip=y main_fetched=y branches=[cand5 lane/W29-SUM-TYPED-ENTRY-ARGS lane/W29-SUM-TYPED-ENTRY-ARGS-wip lane/W29-SUM-TYPED-ENTRY-ARGS-wip-teardown-wip] bundle_bytes=53987
LANE W33-OUTBOX-RESEND__src cur=lane/W33-OUTBOX-RESEND-wip wip=y main_fetched=y branches=[cand5 lane/W33-OUTBOX-RESEND-wip lane/W33-OUTBOX-RESEND-wip-teardown-wip] bundle_bytes=37580
LANE W35-RC-DEDUP__src cur=lane/W35-RC-DEDUP wip=y main_fetched=y branches=[cand5 lane/W35-RC-DEDUP lane/W35-RC-DEDUP-teardown-wip lane/W35-wip-all] bundle_bytes=58907
LANE W40-HOST-ALG2-HYBRID-KEYS__src cur=lane/W40-HOST-ALG2-HYBRID-KEYS-wip wip=y main_fetched=y branches=[cand5 lane/W40-HOST-ALG2-HYBRID-KEYS lane/W40-HOST-ALG2-HYBRID-KEYS-wip lane/W40-HOST-ALG2-HYBRID-KEYS-wip-teardown-wip w24] bundle_bytes=68063
LANE W43-ORPHAN-GATES__src cur=lane/W43-ORPHAN-GATES wip=y main_fetched=y branches=[cand5 lane/W43-ORPHAN-GATES lane/W43-ORPHAN-GATES-teardown-wip] bundle_bytes=777142
NOT COPIED (>5MB): SKIPPED-BIG-EVIDENCE W02-PAY-WEEK-EXACT /srv/lanes/W02-PAY-WEEK-EXACT/native-out/success-external-input-check.log
Artifacts (/srv/artifacts/*, ~446M each tree) NOT copied; only SHA256SUMS+PROVENANCE copied.

## e2e
LANE W11-JOURNEY-OBJECT-RECORD__src cur=lane/W11-JOURNEY-OBJECT-RECORD wip=n main_fetched=y branches=[lane/W11-JOURNEY-OBJECT-RECORD] bundle_bytes=13903
LANE W38-JOURNEY-ROWS-WIRING__src cur=lane/W38-JOURNEY-ROWS-WIRING wip=n main_fetched=y branches=[lane/W11-JOURNEY-OBJECT-RECORD lane/W38-JOURNEY-ROWS-WIRING w24] bundle_bytes=48177
LANE native-exercise-2__d4 cur=lane/ne2-d4 wip=n main_fetched=y branches=[lane/native-exercise-2 lane/ne2-d4] bundle_bytes=100776
LANE native-exercise-2__src cur=lane/native-exercise-2 wip=y main_fetched=y branches=[lane/native-exercise-2 lane/native-exercise-2-teardown-wip lane/ne2-d4] bundle_bytes=103539
LANE w06__edge cur=master wip=y main_fetched=y branches=[master master-teardown-wip] bundle_bytes=293533
LANE w06__src cur=lane/w06 wip=n main_fetched=y branches=[lane/w06] bundle_bytes=4509
Artifacts (/srv/artifacts/*, ~446M each tree) NOT copied; only SHA256SUMS+PROVENANCE copied.

Non-git dirs (no repo, small files copied): gate: mk-tools; lane1: mk-tools,_w04tmp; e2e: lane fn-direct, rollup, ~/activity-route, d3b, fs, jr. Files >5MB, .lake/target/build skipped.
Not verified with git bundle verify (main absent on persvati bundle dir); all bundles size>0, none FAILED.
