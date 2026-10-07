# ROOT CONTINUATION (2026-10-05, before compaction) — read this first, then PRIORITY-ON-RETURN.md
Session c1e4d723 (breadstuffs-89) is the Mini swarm root. All durable state is in ~/dev/redregg/work/:
SWARM-LEDGER-20261004.txt (every event), MERGE-QUEUE.md (landings), WORKBOARD-20261005.md (foreman's board),
OB-COMPLETION-20261005.md (Objective Bend P0 wave), resume/ (per-lane notes, DISTILLED.md old->new ids, PRIORITY-ON-RETURN.md,
REDS.md, ROLLUP.md, FALLOW-DIGEST.md), resume/ROOT-PACK-20261005.md (cv distill pack of this root; ~1.2M tokens, grep it, don't read whole).
Regime (binding files): LANE-PROTOCOL, VERIFY-ONCE, PIPELINE, BURST-LANE-BRIEF (+amendments), WORKER-BRIEF, HBOX-HOLD (partial lift).
Ember 10-05 rules: <4 agents running at once, prefer Opus; Sonnet fairies ok; renew lanes via cv distill (planted subagent ids in
DISTILLED.md; SendMessage the new id); rollup per hot cluster (activity/object files have ONE owner at a time); fan out only across
non-overlapping files; landings beat throughput; no locking otherwise; decisions with reasons written down.
Git: main = green = next = 259a2fb0 at 19:50Z; ~18 ranges QUEUED. Boxes: burst-gate 67.213.124.13, burst-lane1 162.43.189.7,
burst-e2e 152.236.4.24 (Latitude, delete 2026-10-05T15:55Z; quota 2 bare metal), persvati (Ember's laptop), hbox (2 slots, fn agreed).
Running at compaction: ROLLUP (sonnet a35fb564b81d1411d: retention+checkpoint-invariant then seats), FAIRY-SHIP (sonnet
a4265d33b8613fad4: J12X + doc-share reds), MERGE-KEEPER resumed from its distilled id (see DISTILLED.md; old a02f2dd1a9d42b83f).
NEXT OPUS (in order, as slots free): (1) live law bypass PayObservation/PayEnrol (cv 01a1087d-8a58); (2) W42 snapshot gate blind in
Mathlib modules (cv 01a1089a-1168); (3) ForcingTransparent segment lift (distilled id of a60590cf65abbb0dd); (4) UPGRADE turns
(a5e2da77f3df2384b) after seats lands; (5) OB1 surface semantics / OB5 Faré / OB7 call. Then plan-scoped replay, store-open
authenticated verify-at-use (PRIORITY #6), hyp-ledger 6 red rows on main.
cv finding: distilling the ROOT barely shrinks it (notifications kept verbatim) -> cv needs a root policy (summarize notifications).
