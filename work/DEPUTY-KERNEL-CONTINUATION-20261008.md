# DEPUTY-KERNEL continuation — 2026-10-08 (fresh instance after usage-wall kill)

Record of prior work: work/CXO-EXPERIMENT-4.md. Briefs: work/kern-briefs/. Hub: tools/cxo/cxo-b3. Box: burst3-a.
Train lane: /srv/lanes/train-kern/src; remote /srv/git/minidregg.git (lane/train-kern). GitHub main = dcab86da (refs/heads/main on the shared remote).

## Milestones
- 15:1x kern-r1 (8070ddc6) VERIFIED: already in train (b58b81bc). Statements read: intent_refines_step generic over intent
  (honest; objective/seat_refines_step are instances); corollaries stored_checkpoints_typed / domain_holds_forever /
  live_counts / migrate_cannot_fail take a ReceiverIntent premise + Reachable genesis and conclude about payloadsOf w'.
  tamper_breaks_payload_view TRUE theorem, satisfiable `changed` (changed_body_changes_payload). No ∨Collision.
  Weakness noted: the "plant went red" record is a type mismatch, i.e. the T1.1 unconstructibility plant is R2's job.
- kern-oom (775240ec) VERIFIED: Nat.pair list encoding Θ(2^n) bits derived; plant OOM at c6-no-grant; fix = byte
  StreamCodec, rejectCodec_injective, *_v1_refuses, roundtrips; 4 journey rows < 157 MiB. Merged at 052eba09 (umbrella t471947942 pending).
- kern-pole: hub restart killed its job; told to re-request (15:1x).
- kern-charge: asked for rebase (sandbox .git read-only). Lane has ONLY an untracked Kernel/ObjectiveTurnTotalityStorage.lean
  (+ import removed from Kernel.lean); plan: reset lane to green train tip, keep untracked file, re-add import, answer.

## Next
R2 spawn (astra, --from train tip, --umbrella default): Admissible cfg w t over exact Turn, durable writer consumes it,
Step/Reachable over World, four acceptance plants. Then rebase train on dcab86da, full gate run-gate-burst.sh, send ROOT sha.
- 15:2x kern-oom merge -> TRAIN_RED (semantic conflict: R0's Refusal.stateRetired missing from oom's exhaustive byte codec,
  ObjectiveActivityReceiver.lean:1315 + rfl at :1501 -> sorryAx). `merge kern --abort` (train back to 1c2d798b). Merged
  1c2d798b into kern-oom's lane (HEAD 0535c946, registry base patched to it) and sent kern-oom the fix. Then re-merge lane/kern-oom.
- kern-charge lane reset to 1c2d798b (untracked storage file kept), base patched, a13 answered (integrate Delta.burn, submit).
- R2: spawned kern-r2 then immediately retired it (0.1M) — gave the range to the veteran kern-r1 instead (lane reset to
  1c2d798b, base patched, scope widened, budget 50M). Brief: work/kern-briefs/kern-r2.md. kern-r0 retired.
- cxo gap (still): no command to re-base a live worker after its lane moves; I patch `workers.base` in ~/.cxo/registry.sqlite by hand.
- 15:10 kern-charge e0e2e3c6 VERIFIED + merged (train 55f8f244 GREEN). Statements: receiver_charge_eq_legBytes_plus_framing
  per BlobKind (activity 40 / book 26 / seat 26), retired +4, burn 0, unchanged post = full image (exact). Residual:
  prepared_ofLoaded_charge_eq_storage_plus_framing has premise `images : ∀ p ∈ prepared.final.1, PostImage p.bytes`;
  sent back to kern-charge (base e0e2e3c6) to discharge from the receiver.
- 15:11 kern-oom fix 1e46dbc4 (stateRetired = new root tag 2) merged; train kern GREEN at 2c77a933. kern-oom retired.
  closes: cv 01a11b6a-58b7 (journey OOM).
- Live: kern-r1 (R2, from 1c2d798b), kern-charge (images discharge), kern-pole (re-requested journey).
- 15:14 kern-r1 a35 ruled: lower-core extraction (HostRefinesWorldCore / DurableReceiverCore, move not copy); CheckedCommit carries certified source intent as a cert field + ofLoaded eq, no log-encoding change (encodeTurn = R3). Design doc copied to box. kern-r1 lane ff to 2c77a933, base patched.
- 15:16 a44 ruled: receiver-core extraction allowed (4 files); IO CheckedCommit indexed by Loaded+Turn, logical Admissible = Loaded+DeployedRepresents+CheckedCommit; no executable worldOf (FD-1).
- ROOT: hub fixes (cxo rebase NAME REF, unprotect, allow_dirty) need a restart; tell ROOT "kern idle" when no worker is WORKING.
- 15:25 hub restarted with ROOT fixes (cxo rebase exists now; use it instead of sqlite). Jobs interrupted; workers re-requesting.
- 15:27 a20: PayAssignmentOwner.lean allowed; writer Commit sum (ordinary w/ gate evidence + protected-cells-unchanged theorem | OB CheckedCommit) accepted, no third path.
- 15:56 cxo bug reported: 3 journeys (2 infra-certify + kern-pole) hold all CXO_MAX_JOBS slots ~30 min; kern-charge/kern-r1 builds queued since 15:28.
- 15:58 kern-charge 4758a550 (prepared_posts_images discharges the premise; headline premise-free) merged, train GREEN 8e462f42; kern-charge retired. kern-r1 lane is on 2c77a933 — rebase it with `cxo rebase kern-r1 <tip>` only at a turn boundary, or just let the train merge handle it.
- 16:20 a26: cycles cut (ObjectiveAdmissible compiles, no writer dep). Allowed 1-line imports in 4 receivers; ClockTickReceiver.lean (clock subject) held, asked ROOT.
- 16:26 ROOT OK: kern-r1 adds 1-line import to ClockTickReceiver.lean; told DEPUTY-PRODUCT.
- prod already edits ClockTickReceiver import block (+import Theory.AxiomPin, prod-clock 93e18aac); conflict resolves as union of imports.
- 16:50 kern-r1: certificate/writer green in core; a45 standing permission for proof-only/import-only downstream edits (NOTE + proceed); a47 plants must use decodable same-role alternates.
- 16:56 growth item (DEPUTY-PRODUCT: per-create wall linear in #cells) → brief work/kern-briefs/kern-grow.md; spawn REFUSED by pace gate (33% used at 1% of window). Asked ROOT; not forced.
- 17:01 ROOT: force all spawns (spend window to empty). kern-grow spawned (sol, 25M, from 8e462f42, --force). ROOT wants its first diagnosis relayed when it names the loop.
- 17:05 kern-grow diagnosis CONFIRMED by reading: DurableServed.lean:684-687 extendVerified rebuilds RootCache.ofEntries (WorldRootCache:241 foldl insertWrite from empty) over all cellIds per extension. Relayed to ROOT. Allowed DurableServed/WorldRootCache/NativeHostLight/NativeHostServed.
- 17:07 kern-pole OOM at 10G in replay (pre-oom-fix lane). Merged train 8e462f42 into its lane (68289a2a, base patched; cxo rebase refuses dirty trees). Told it to rebuild+rerun.
- 17:12 kern-pole found 2nd exponential: TurnOfIntent.lean:478 bytesCode = Encodable List Nat (nullifier key). Pole given TurnOfIntent.lean to fix (base-256 sentinel, same injectivity statement) + class grep.
- 17:21 ruled for DEPUTY-PRODUCT: StoreEpoch/schema-refs (DurableCheckpointCodec) is train prod work; asked derivation to cover kern-oom REJECT/RECORDED-FAILURE v2 tags. If hand-bumped, bump again at kern rebase.
- 17:3x AT REBASE ONTO MAIN (obligation from prod): switch ObjectiveActivityReceiver REJECT/v2 + RECORDED-FAILURE/v2 literals to prod-hostup persisted-codec tag module constants, add entries there; their gate goes red until done. Module path TBA from DEPUTY-PRODUCT.
- 17:40 kern-r1 R2 statements VERIFIED (CheckedCommit data {intent, source, derived, installs}; Admissible = Loaded+DeployedRepresents+CheckedCommit; SameAuthorization = two verdicts on same ingress, determinism via Verdict.intent_determined — real teeth; World Reachable multi-step invariants; plants = decodable same-role alternates, writer splices red). Submit refused by text guards only; waivers approved (a152).
- 17:45 R2 (kern-r1 de1a3a33) MERGED, train kern GREEN 8c228554. Mechanical check: 113 deleted theorem names all re-added except Loaded.judge_tail (replaced); moved statements identical. kern-r1 kept alive (veteran) for rebase-onto-main work.
- NEXT: kern-pole (bytesCode fix + totality), kern-grow (root cache). Then rebase train onto dcab86da (or newer main), apply prod persisted-tag module obligation if landed, full gate via scripts/pipeline/run-gate-burst.sh in a fresh lane.
- 17:48 merged main dcab86da into train (no conflict): train kern GREEN 7f6caaa6.
- 17:50 kern-grow a155: lane ff to 7f6caaa6 (base patched); allowed extendVerified refactor, client route (DurableReceiverIO/Core, ClientConsentCore, client_consent.rs) with anchor-bound persisted verified root cache, bulk bench under scripts/kern.
- 17:52 a157 ruled: client root cache = custody (same class as ConsentAnchor); anchor carries digest binding of cache; Good from NAMED extended custody premise; mismatch => full rebuild. Flag this trust-model choice to ROOT in next report.
- 17:55 kern-pole: after bytesCode fix totality 409/422 ok; 13 send intents refused retiredCell by ofCells but Host admits → real totality gap; asked for per-intent diagnosis (tombstone guard vs Host bug) before fix. P1 coverage gap queried.
- 18:00 kern-pole a172: 13 send = Host resurrects retired inbox ids (ObjectiveCall.holdInbox treats retired as empty at same coordinate). RULED: retired ids permanent; Host admit refuses writes to retired cells (+theorem); inboxes generation-addressed (pair,generation), reopen path deleted. Scope widened. Need to rebase pole lane onto train before it edits.
- 20:02 resumed after Claude usage wall (18:05-20:02). main now 5896a594 (prod landed). kern-pole SUBMITTED a92055cc to verify.
- 20:08 kern-pole checkpoint a92055cc merged (bytesCode sentinel; 409/422 with 13 send = resurrection; NOTE: with R2 in train the Host now REFUSES the resurrecting send at replay → the send journey will be red in the full gate until generation-addressed inboxes land). a187 ruled: no unsafe implemented_by; client uses light-client sibling paths vs anchored root; submit server fix separately first.
- 20:15 main 5896a594 merged into train: GREEN 810b35cb. kern-pole rebased there; sent generation work + schema-refs v5→v6 hand-bump (DEPUTY-PRODUCT agreed; derived-epoch module in flight on prod, second lander converts). ConsentAnchor.lean will conflict union-style with prod later.
- cxo nit: `cxo rebase kern-pole 810b35cbce` -> "cannot resolve in lane or shared remote" although it is lane/train-kern head on the remote (probably no fetch of lane refs / short sha). Did ff by hand + sqlite base.
- 20:56 schema-refs v6 broke protected Assurance.NativeAcceptedFixture (v5 captured seed). cxo unprotect Assurance/NativeAcceptedFixture*.lean for kern-pole; re-emit via scripts/native-accepted-fixture/generate.sh.
- 21:30 pole acceptance j492985385 exit0 but TOTAL 0 (all empty) — flagged; grow before@3000 prep too slow (5400s cap at 2120 cells) — suggested prep with fixed binary, sample old vs new on same store.
- 22:31 kern-pole fresh all-7 acceptance j496655183: TOTAL 422 ok 422 (send 78/78) with generation inboxes.
- 22:37 kern-pole 079ff7ea MERGED: generation-addressed inboxes (Inbox.key/cell over generation, key_generation_injective, HeldInbox.empty_advances), Verdict.writes_unretired (Host admission), schema-refs v6 + ConsentAnchor pins, NativeAcceptedFixture regenerated by script, send journey retarget + fresh-cell assertion. Fresh pole 422/422. Train GREEN 8e37e22d. kern-pole retired. Remaining: kern-grow (server root-cache fix + curve), then full gate.
- 22:45 full gate STARTED: fresh lane /srv/lanes/kern-gate (mk-lane, reset to 8e37e22d), `run-gate-burst.sh /srv/lanes/kern-gate 5896a594 kern1`; logs /srv/lanes/kern-gate/logs/gate-kern1.{summary,out,done,aborted}. kern-grow not yet in; if it lands, rerun gate as kern2.
- 23:05 FULL GATE kern1 on 8e37e22d: red=7 (host-closure pin, full-loaded-ratchet + import-boundary: runner in Kernel imports Host, build-surfaces fixture pin, token-census homes/restricted callers moved to Core, objective-proofs --pin, hyp-ledger new structures). Umbrella PASS. Sent all 7 to kern-r1 (lane rebased via `cxo rebase kern-r1 refs/heads/lane/train-kern` — full ref works; short sha does not).
- 23:08 DEPUTY-PRODUCT demo D1: charged law refusals hang to 600s deadline on 0ea31db5 → told: kern-oom class, rebuild on 8e37e22d (re-genesis, v6). If persists = new kern red.
- 23:12 a319: allowed gate-fix paths for kern-r1 (+unprotect lakefile, scripts/gates, protocol).
- 23:20 lane cache: objective --draft writes .ilean in place; shared cp -al hardlinks are 444 → broke links for 2 files in kern-r1 lane (cxo/pipeline gap: in-place writers vs shared inodes).
- 23:25 prod derived StoreEpoch at train prod 001b9a2c (not on main yet): Compiler/PersistedCodecTagRegistry/PersistedCodecTags/PersistedCodecTagCensus. When kern merges it: add registry entries for REJECT/v2, RECORDED-FAILURE/v2, generation inbox ids in Compiler/PersistedCodecTags.lean; drop hand-bumped v6 (resolve to digest). Order depends on who lands first on main.
- 23:30 kern-r1 gate repair 66bb848a MERGED, train GREEN 1c7e46da. Full gate kern2 started (same lane reset+clean). cv task opened for 7 open-pole hyp rows.
- 23:32 kern-r1 gate repair 66bb848a MERGED, train GREEN 1c7e46da. Full gate kern2 running (lane kern-gate reset+clean). cv task 01a11dd8-1549 opened (7 open-pole hyp rows owe instances) — kern-r1 can take it after the gate.
- 23:45 DRAIN ORDER (ROOT/Ember): no new spawns/items; finish in-flight ranges, merge, gate + standing journey run at tip, send sha, retire all, final continuation, stop. kern-grow told to submit server fix only. Gate kern2 on 1c7e46da: 22/22 PASS so far, hyp-ledger running.
- 23:48 FULL GATE kern2 red=0 at 1c7e46da (contains main 5896a594). Sent ROOT; asked how to run standing journey run at tip. Waiting on kern-grow.
- 23:58 publish-artifacts 1c7e46da label next from /srv/lanes/kern-gate/src (log kern-gate/logs/publish-1c7e46da.log); pipeline-journeys.service should pick it → /srv/journeys/1c7e46da.../results.tsv.
- 00:08 1c7e46da set READY (/srv/artifacts/1c7e46da...). Label `next` contention with DEPUTY-PRODUCT (5019da6a, train prod tip): they go first; when their run starts, re-run `publish-artifacts 1c7e46da... next /srv/lanes/kern-gate/src` (relabel only). Runner lock is flock -n (no manual queueing).
- 00:25 standing run on 8e37e22d DONE: all kern rows PASS; reds hostupgrade-EF (epoch, prod), welcomecontinuity (93e18aac clock), sshe2e (params schema), m6grain (GRAINS_ROOT), jpay 2/3/4 (clockGenesisNow); UNCONFIGURED objective/m7/JPAY6/exchange. Reported to ROOT. kern-r1 retired.
- 00:45 Codex auth REVOKED on burst3-a (kern-grow TURN_FAILED). kern-grow retired; WIP patch /srv/lanes/kern-grow/kern-grow-WIP-20261009.patch (+scripts tgz), local work/kern-briefs/kern-grow-WIP-20261009.patch; paired 1000-cell: total 44.5→36.7s, host 21.8→15.0s, client 22s unchanged (PARTIAL). cv task 01a11e1b-0adc. Final kern sha 1c7e46da (gate red=0, set READY); standing run pending behind 5019da6a.
- 00:56 main 5896a594 standing run: same prod reds + call/send/domain/objectrecord OOM 24G (kern fixes those). 1c7e46da relabelled next (00:54), runs after 5019da6a.
- 01:50 yielded per Ember: standing run of 1c7e46da in progress; check recipe in DEPUTY-KERNEL-FINAL-20261009.md.
