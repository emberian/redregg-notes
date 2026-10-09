# DEPUTY-KERNEL — final state, 2026-10-09 (drain/freeze)

Full log: work/DEPUTY-KERNEL-CONTINUATION-20261008.md. Box burst3-a; shared remote /srv/git/minidregg.git.

## Train kern — candidate for main
- sha **1c7e46da8dc7c743120cb0504958649e0c3c49e1** = refs/heads/lane/train-kern. Contains main 5896a594 (merged, no conflict).
- Full gate: `run-gate-burst.sh /srv/lanes/kern-gate 5896a594 kern2` → **red=0** (logs /srv/lanes/kern-gate/logs/gate-kern2.*).
- Artifact set READY /srv/artifacts/1c7e46da… (label next). Standing run: /srv/journeys/1c7e46da…/results.tsv (see bottom).
- Ranges in it (all verified by statement reading + plants): R0 Turn.absent/Delta.burn/stateRetired (kern-r0); kern-r1 objective_refines_step + corollaries;
  kern-oom byte StreamCodec Reject (REJECT/RECORDED-FAILURE v2) — closes cv 01a11b6a-58b7; kern-charge exact charge = legBytes + framing (premise discharged);
  R2 CheckedCommit/Admissible/WStep/Reachable over World, writer consumes certificate, 4 T1.1 plants, *Core extractions;
  kern-pole totality pole 422/422 + bytesCode sentinel + generation-addressed inboxes + Verdict.writes_unretired + schema-refs v6 + NativeAcceptedFixture re-emit;
  kern-r1 gate repair (7 ratchet/pin reds).
- Flag day: StoreEpoch schema-refs v5→v6; old Stores refuse by epoch; re-genesis. NativeAcceptedFixtureData re-emitted.
- Known merge with train prod 001b9a2c+ (derived StoreEpoch): add registry entries in Compiler/PersistedCodecTags.lean for REJECT/v2,
  RECORDED-FAILURE/v2 and generation inbox ids; drop the hand v6 (resolve to digest); Kernel/ConsentAnchor.lean union conflict.

## Unlanded
- **kern-grow** (retired, Codex auth revoked mid-range): lane /srv/lanes/kern-grow/src at base 7f6caaa6, UNCOMMITTED diff
  Compiler/DurableServed.lean (+112) Kernel/WorldRootCache.lean (+27): incremental root cache in extendVerified. Preserved:
  /srv/lanes/kern-grow/kern-grow-WIP-20261009.patch, kern-grow-scripts-20261009.tgz, local work/kern-briefs/kern-grow-WIP-20261009.patch.
  Evidence: its lane umbrella/proofs green (per worker); paired j502801195 @1000 cells same base: total 44.5→36.7 s, host 21.8→15.0 s,
  client 22 s unchanged → PARTIAL. Not gated, not merged. cv task 01a11e1b-0adc.
- Owed: cv 01a11dd8-1549 (7 open-pole hyp rows need named satisfying/refuting instances).
- No other kern lanes hold unmerged work (kern-r0/r1/oom/charge/pole: all merged, retired).

## Ops notes
- Codex credential on burst3-a REVOKED 00:40Z: `codex login` on Mac, recopy auth.json to ~/.cxo/codex-home.
- cxo: `rebase NAME <short sha>` fails to resolve (full ref works); event lines print every waiver (huge); guard `admit` matches identifiers/ledger rows.
- Lane caches: cp -al hardlinked 444 .ilean; in-place writers (objective --draft) fail — break links per file.

## Pending check (for the successor / ROOT)
Standing run of 1c7e46da started ~01:35Z on burst3-a. When /srv/journeys/1c7e46da8dc7c743120cb0504958649e0c3c49e1/DONE exists:
  awk -F'\t' '$2!="PASS"' /srv/journeys/1c7e46da8dc7c743120cb0504958649e0c3c49e1/results.tsv
Expected (from 8e37e22d and main baselines): only the prod/clock reds main also has (hostupgrade-EF, welcomecontinuity/genesis,
sshe2e, m6grain, jpay 2/3/4) + UNCONFIGURED objective/m7/JPAY6/exchange; call/send/domain/objectrecord/growth PASS
(main OOMs on those four). Any OTHER non-PASS row is a kern red.
