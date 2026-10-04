# ORIENT-B: world, product, privacy, agreement. A map for restarting (2026-10-04)

A read-only orientation reader wrote this. No edits, builds or commits were made; this file is the only output.

## Baseline

- **Main.** I took a fresh clone of GitHub `emberian/minidregg` main at `1ffe6bf3` (02:42 EDT) and fast-forwarded it to `0a7295ac` (lane S8 docs) during the read. The clone is at `scratchpad/minidregg` of session c1e4d723.
- **CI on main is red.** The last completed run is 37182752860 at `6909eaf9`. In its lake-build, `Compiler/StoreHiding.lean`, `Kernel/TurnOfIntent.lean` and `Kernel/PayCellUpgrade.lean` fail: the PayCellUpgrade theorems carry `sorryAx`, and TurnOfIntent hits "typeclass instance problem is stuck". The hygiene gate also fails, on bare `#print axioms` in `Theory/Bfv*`. Runs at `f0c95118`, `1ffe6bf3` and `0a7295ac` were still in progress when I read (READ).
  - The CUT-REBASE lane is meant to deliver the green umbrella. It is not on main (READ-rec: SWARM-LEDGER 03:00).
- **Tags.**
  - **READ** — I saw it in a source file or doc on main at the commits above.
  - **READ-rec** — I read it in a record: a redregg note, scout, ledger or lane report. I did not re-verify it at source. Evidence paths on hbox may no longer exist: the ledger's 03:15 entry records a workbox wipe on hbox that removed many `/home/hbox/workbox/*` directories.
  - **INFERRED** — my reasoning.
- **Task coverage** comes from `cv task list --all --tsv`, dumped to `scratchpad/cvtasks.tsv` (588 rows, 381 open). The ids are short prefixes. "NO TASK" means no task title matched the frontier's keywords.
- **Delegation.** DEOS.md, SURPASS.md and CHANNELS.md (claudesplosion) were read in full by three sub-readers, each checking against the same clone. Their results are condensed in §B; their tags are kept.
- **Where the named docs actually live.** DEOS.md, SURPASS.md and CHANNELS.md are not in `minidregg/docs`; they are in `/Users/ember/dev/claudesplosion/planning/`. FRIENDS.md is `deploy/shell/FRIENDS.md`. The tenancy design exists only as `TENANCY-DESIGN.txt` in the shared session scratchpad. It is not in any repo: the commit `535fea1e` cites it, but no tracked file holds it (READ).

---

## A. redregg designs and work notes

### A1. designs/BIGDREGG-PRODUCT-ARCHITECTURE-20261003.txt (Codex, 10-03)

**(1) Claim.**
- Grow Mini into "bigDregg" by making community institutions, exchange mechanisms, creative tools and resident services ordinary authored Bend objects on one kernel. Starbridge is the common authoring, inspection and actuation face.
- FHEgg/DrEX mechanisms become shared source modules plus qualified execution adapters, not a trusted market universe.
- Three joined constructions:
  - (A) an allocation/exchange room;
  - (B) a world/tool studio with collective adoption;
  - (C) a resident/service commons.
- Six implementation packages follow (shared Plan receiver, authoritative allocation, private custody/intake, Starbridge projection, collective adoption, service commons).
- The addendum finds that only the canonical `resourceBook` can move balances, so settlement is one canonical `Operation.transfer` batch.

**(2) Status on main.**

| Item | Status |
| --- | --- |
| A. Allocation room | **PARTLY.** `world/market/{MarketMath,SingleSellerAllocation,UniformProRata,CanonicalBookSettlement,CanonicalUniformSettlement,SharedBookSettlement}.obend` and `market-cohort.json` landed (`187f4aac`..`f0c95118`, lane S1). They are Objective source, previewed only (READ). The refuter the doc names still stands: `native/resource-client/src/market.rs:1-25` computes the allocation in the client and refuses deposits (`depositUnavailable`) (READ). There is no native money receiver for the Objective settlement, and no native accepted receipt from any Objective source on main (README "Honest state" row; READ). |
| B. Studio and collective adoption | **PARTLY / DESIGN.** Studio edit, import, fork, history and preview exist (`native/resource-client/src/web/studio.rs`, `docs/STUDIO-SOURCE-WORKSPACE.md`) (READ). Adoption exists only as BendTT `.bend` (`world/Workshop/CollectiveAdoption.bend`), which README calls "the retiring BendTT path, kept as domain designs to port" (READ). There is no `ObjectPresentation` type anywhere (READ, grep). |
| C. Service commons | **DESIGN-ONLY** on the live path. `world/Workshop/ResidentServiceCommons.bend` is BendTT only (READ). |
| Packages 1-6 | 1 is PARTLY (W1.2 native-b holds `Host/ObjectiveInvocationQuote`, which is not on main; READ-rec, LANDING-INVENTORY "HELD"). 2 is PARTLY (as A). 3 is PARTLY (MPC private inputs `cf6a4c1d`; READ). 4 is DESIGN. 5 is DESIGN. 6 is DESIGN. |
| Addendum | Partly superseded. Its "five BendTT Books pass" is evidence on the path being deleted (Scout G blind spot 7; READ-rec). The market half was re-authored as `.obend`; the collective and commons halves were not (READ). |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Port the surviving domain sources to `.obend` | `01a104f3-e3b5` |
| Native money domain adapter / canonical settlement receiver | NO TASK |
| Sealed-market deposit | `01a0f81a-386d` |
| Starbridge ObjectPresentation | NO TASK |
| Atomic ballot / nullifier / tally receiver and guarded adoption install | NO TASK |
| Service quote / reserve / accept contract | NO TASK |
| Independent custody injection for FHE committees | NO TASK |
| Oracle Pit | NO TASK, and correctly later |

**(4) Contradicts main.**
- The addendum's "Five actual no-opaque BendTT Books pass" stands as current evidence, but README declares that path retiring (READ).
- "Grow on authored Bend objects" agrees with main's direction.

### A2. designs/CONSTRUCTION-PROOF-CONTRACTS-20261003.txt (also on main as `docs/CONSTRUCTION-PROOF-CONTRACTS-20261003.txt`)

**(1) Claim.**
- An evidence discipline: S (semantic theorem), C (crypto), R (refinement), V (validation) are kept separate.
- A six-part proof map:
  1. OO elaboration;
  2. typed Plan / atomic install;
  3. source → bounded machine → network → backend;
  4. fixed circuits and FHE;
  5. private observation, cost and MPC;
  6. agreement safety and liveness.
- Seven immediate proof joins, a persistent-computation addition, and a refuted overclaim: the Dispatch pending-root guard does not bind, and `NativeInvocationStatement` is the repair.

**(2) Status on main.**
- **Mostly OBSOLETED in its machine layer.** Sections 3 and 4 are built on the BendTT closure machine. `Theory/BendClosureMachine.lean`, `Theory/BendLiveMachine.lean` and `Compiler/ObliviousNetwork.lean` are still on main, but the umbrella files (Minidregg, Theory, Kernel, Compiler, Host, ResearchWip, BendQualification) do not import them. Only `Assurance/*Checks` and BendTT compilers do (READ, grep). The cut deletes Gen-1 leftovers (READ-rec, ledger L0.1).
- The live semantic core is now Core4: `Theory/ObjectiveBend{DemandMachine,DemandAdequacy,DemandCompleteness,DemandDataSoundness,DemandPreservation,Checkpoint*}.lean`. Completeness (`machine_evaluation_complete`), forceWith ≡ runBounded and deep Data soundness are proved, but sit in ResearchWip, outside the default gate (READ, `docs/OBJECTIVE-BEND.md` at `0a7295ac`).
- **§6 agreement.** Present and compiled in `SimplexQualification.lean`: `Kernel/GenericSimplexEngineSafety.lean`, `GenericSimplexVAInvariant`, `GeneralSimplexReachability` (READ).
- **§2 joint receiver.** `Kernel/JointReceiverAdmission.lean`, `JointPromiseAuthorization`, `JointDecisionRecovery` and `JointReservation` exist (READ).
- **Activity joins.** `BendActivityProgram`, `NativeInvocationStatement` and `BendActivityRoutePermit` are on main, imported only by ResearchWip (READ).
- **Core4 activities.** `perform`/`done`/`yield`/`resume` landed in Core4 (`2ccd6290`..`e598326e`), but "No kernel delivers responses or persists an activity yet" (`docs/OBJECTIVE-BEND-EVENTS.md`; READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Kernel response delivery and checkpoint storage | `01a1056f-0066` |
| Within-turn non-divergence | `01a1056f-0083` |
| C machine refinement | `01a10564-8480` |
| PackedRefinement (zk) | NO TASK. The zktruth lane found it trivially inhabitable and a counterexample `codec_relation_not_refinement`; uncompiled and HELD (READ-rec, ledger 02:55). |
| Fixed-capacity public tariff (the Plan⟨false,false⟩ refuter) | NO TASK. W1.1 native-A was "deferred" (READ-rec). |
| ASKS frozen-share invariant over Rust | NO TASK |
| `NativeInvocationStatement` signer repair | NO TASK |
| Reachable → AuditRefinement bridge (Simplex local extraction) | NO TASK |

**(4) Contradicts main.**
- Its machine and oblivious sections name BendTT objects as the live construction (READ).
- README now says the oblivious machinery "targets the retiring BendTT core" and the zk theorems "assume an uninhabited refinement" (READ).
- The doc needs a Core4 re-statement or a historical banner.

### A3. designs/contract-graph-20261003.json

**(1) Claim.**
- A proposed semantic interface graph with three alternatives (station, desk, commons) over 18 contract nodes: definition, object, view, draft, invocation, reservation, decision, installation, activity, external_service, artifact, custody, release, recovery, history, context, ballot, evidence.
- Nine negative equivalences, for example "view != read grant", "ballot adopted != true proposition", "custody holder != audience recipient".

**(2) Status on main.**
- **PARTLY.** `Kernel/Contracts/{Identities,Cuts,Snapshot,Futures}.lean` landed (`f5c7cfac`..`17a6489c`) (READ).
  - They encode the Observe/Invoke/Reserve/Install/Release/Retire cuts, `LawRef`, `Obligation`, `InvocationId`, six `SnapshotClass`es with witness-gated conversions, and future-indexed certificates.
  - Named negative theorems include `observation_does_not_authorize_mutation`, `historical_acceptance_does_not_bypass_today`, `install_requires_reservation`, `rehearsal_to_archive_has_no_edge` and `untagged_store_collision_exists` (READ).
- **Missing nodes:** view/ObjectPresentation, activity index, external_service, ballot, evidence/regime. ResearchRegime is ported to `Theory/ResearchRegime.lean` but not joined to Contracts (READ).
- **Not integrated.** Only `ResearchWip.lean:151-154` imports Contracts. No per-domain type is refined into them; `Refinements.lean` was uncommitted (READ-rec, ledger 06:00).
- `Futures.lean` models the world as `DurableReceiver.Image`, the side SURPASS T11 would delete (READ via the SURPASS sub-reader).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Collapse the 7 Observation / ~10 Reservation definitions into Contracts | NO TASK. "Contract-type collapse" was deferred to after the cut (READ-rec). |
| SDK onto the Lean codec | `01a104fe-94a5` |
| Retire type | NO TASK |

**(4) Contradicts main.** Nothing directly; it is labelled "proposed".

### A4. designs/PRIVACY-COMPOSITION-REVIEW-20261003.txt

**(1) Claim.**
- A finite source audit across traffic, the MPC backend, the Bend machine and FHE.
- Profiles:
  - P0: PSK RPC.
  - P1: registered cohort mix with a trusted, non-colluding registrar.
  - P2: ASKS/MPC at n=3f+1, static corruption.
  - P3: clear Bend reference.
  - P4: first FHE slice.
- One real fault: the ASKS supporting-share overwrite, which leaves a completed sharing with no honest reconstruction support. It was repaired as V2.
- One construction refuter: `Plan⟨false,false⟩`, where 1 vs 2 source steps leak through any public exact fee.
- The mix set-guard holds.
- Cover must continue on refusal.
- WCET was missed (1 s pipeline) while 5 s passed.

**(2) Status on main.**

| Item | Status |
| --- | --- |
| ASKS accepted_share | BUILT. `native/private-backend/src/asks.rs` has 9 `accepted_share` references (READ). |
| Mix guard | BUILT. `native/resource-client/src/pq_mailbox.rs:414` `verify_manifest`, `:442` `verify_transition` (READ). |
| CSV enrollment gap | Closed. Roster enrollment (`d7b2f19b`, "cohort!") replaced the PSK/CSV adapter (READ, git log). |
| Cover-on-refusal | Stated in `docs/TRAFFIC-PRIVACY-PROFILE-P1.md` class 6 (READ). |
| Fixed-capacity tariff | DESIGN-ONLY (READ, grep). The zktruth lane measured the step-count leak (5 vs 8 ticks) and proposed "ticks from a signed versioned tariff, refuse on excess, never refund"; HELD (READ-rec). |
| Rollback-authority separation (anchor / ASKS WAL) | DESIGN-ONLY |
| WCET or async continuation with equal Pending cover | DESIGN-ONLY |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| One source-bound private run carried through admission, custody, install, release and restart | NO TASK. "First new private effect" was deferred (READ-rec). |
| Public meter pair | NO TASK |
| Separate rollback authority | NO TASK |
| Live cohort daemon | `01a10501-830d` (traffic Linux qualification + first new effect) |
| Registrar/operator MAC keys | `01a10501-83a6` |

**(4) Contradicts main.** P1's "CLI CSV paths do not authenticate one slot per enrolled human" is now false (READ). The rest stands.

### A5. designs/ALTERNATIVES-20261003.txt

**(1) Claim.** Three genuinely different constructions with their own falsifiers:
- (A) community-authored station: shared contested objects, institutions, missions graduating typed results;
- (B) living workdesk / research image: tools inside the medium, inspectable source, Hermes review, exact provider custody;
- (C) workshop commons of portable homes: provider replacement without host secrets, disjoint reservations.

Conditional preference: B is the shortest path, A is the necessary contrast, and C shapes custody and reservation interfaces now.

**(2) Status on main.**
- **B: PARTLY.** Documents, transclusion, history, protected fragments, web, Studio and resident context exist (README; `docs/RESIDENT-CONTEXT.md`) (READ). "Request resident work → crash → one charge" for Hermes runs only on its own Store with a scripted provider (README; READ).
- **A: DESIGN.** Story J15 exists as native Mini; shared contested entities do not (READ-rec, Scout G).
- **C: DESIGN.** No portable home or provider migration exists. SPK export, freeze and restore exist as fixtures (READ-rec, G).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Shared contested object | NO TASK |
| Mission graduation | NO TASK |
| Resident sealed handoff / old-host fencing | NO TASK |
| `RenterCheckpoint` binding to resource/genesis/generation | NO TASK |
| SharedResourceBudget oversell at f=0 | NO TASK |

**(4) Contradicts main.** It treats "Current Mini story" as the starting consumer; that holds (`templates/mud`, story). No contradiction.

### A6. designs/ARCHITECTURAL-ARGUMENT.txt

**(1) Claim.** Why the pieces are one system:
- Faré's open extensions demand lazy final-self semantics (hence Objective Bend).
- Privacy is several constructions: payload, traffic, execution, audience change, recovery.
- Agreement is scoped to actual dependencies, not a global order.
- One authored invocation must retain source, authority, resources, effects and result through execution, agreement, install, custody and release.
- The designated-last-signer joint commit is "not universally nonblocking".

**(2) Status on main.**
- **Language: BUILT** as Core4 (READ).
- **Privacy constructions: partial**, as in A4 (READ).
- **Scoped joint agreement: DESIGN.** What runs is one-domain SMR (READ-rec, Scout F).
- **One retained invocation identity: PARTLY.** `InvocationId` exists in Kernel/Contracts and the SDK (READ), but no end-to-end consumer threads it through agreement and release (INFERRED).

**(3) Frontiers and task coverage.** Cross-domain joint turns (joint reserve/YES/install): NO TASK. `protocol-joint-decision` "building" is a protocol.json row, not a cv task (READ-rec, F).

**(4) Contradicts main.** None. It is an argument, and it says so.

### A7. work/DISCORD-WORLD-ENTRANCE-20261003.txt

**(1) Claim.**
- Discord is an ordinary entrance: signed interactions → roster → the same forced shell.
- Proposed common contract: viewer + delegation + context → authorized object projection with typed intents.
- Three recovery defects to repair first: in-memory dedup, mirror cursor before custody, oldest-dropping >20.

**(2) Status on main.**
- **Defects: BUILT** (repaired).
  - Durable per-interaction custody and `/mini-status` (`deploy/discord/README.md`).
  - Mirror custody: start → POST → complete → cursor.
  - Paged backfill, with a 115-message test (READ).
  - Custody now runs through `mini-sdk` (`4b2f299d` deleted the crate's own `custody.rs`) (READ).
  - `/mini-world` presents `home --json` (READ).
- **Common projection contract: DESIGN-ONLY.**
- **Deployment: NOT DONE.** `mini-discord` is inactive on workhorse, the Discord app does not exist, and `discord.dregg.net` Caddy is absent (READ-rec, G; README step 6 is ember's).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Discord app and Caddy | inside `01a0f54c-d1dd` (EMBER bundle) |
| Discord under split tenancy | `01a104f3-e285` |
| Discord mirror re-publishing private-room text | `01a0f99e-d668` |
| Typed object projection shared with web/Hermes | NO TASK |

**(4) Contradicts main.** Its defect list is stale: all three are fixed (READ).

### A8. work/PRIVATE-ENROLLMENT-V4-DECISION-20261003.txt

**(1) Claim.**
- Root decision: separate stable source-authorized committee membership from the per-job Party context, which is derived only from genuine current funded PENDING.
- Codec, purpose and domain are bumped (v4). There is no v3 empty-field reinterpretation.
- Recovery reconstructs the original admission and never authorizes new jobs.

**(2) Status on main.**
- **NOT ON MAIN.**
- Main has the v3 shape: `Compiler/JointBackendPartyCodec.lean`, `Kernel/JointBackendParty{Admission,Receiver,Recovery}.lean`, `Host/JointBackendPartyWire.lean`. There is no `JointBackendPartySealedCodec` and no v4 (READ).
- v4 exists in a codex lane: 14 modules compiled and native-linked, but the final run refused `transactionConflict` (READ-rec, ledger 10:40 MINE item 2).

**(3) Frontiers and task coverage.** `01a10556-494b` (MINE: private committee v4). The funded 63→205 end-to-end is still open: NO separate TASK.

**(4) Contradicts main.** None. It is a decision not yet landed.

### A9. work/PRIVATE-NATIVE-RECEIVING-20261003.txt

**(1) Claim.**
- Fourteen modules pass Lean + C for private native receiving:
  - recipient encryption projection;
  - current funded append admission requiring ciphertext;
  - original-prefix recovery;
  - a recipient-205 verifier as an independent entry `Host.PrivatePartyVerifierMain`.
- Native positive receiving is UNRUN; it lacks a genuine v3 enrollment/PENDING/funded63 fixture.

**(2) Status on main.**
- **NOT ON MAIN.** `Host/PrivatePartyVerifierMain.lean` and `PrivatePartyBootstrapAuthor` are absent (READ, `git ls-files`).
- The private-backend crate on main has `native_worker.rs`, `recipient_seal.rs` and `sealed_outbox.rs` (READ).
- The packet lived at `/home/hbox/workbox/codex-scenario-private-native-20261003`. Whether it survived the workbox wipe is unknown (INFERRED).

**(3) Frontiers and task coverage.** Covered only by the MINE tasks `01a10556-494b` and `-49cd`. "Native positive receiving 63→205": NO TASK.

**(4) Contradicts main.** None.

### A10. work/SCENARIO-PRIVATE-AGREEMENT-20261003.txt

**(1) Claim.**
- The agreement carrier R3 PASS: 64 epochs, fixed width 4, P=32768. One real native op2 replay dispatch returned an exact 132-byte replayed outcome.
- Repairs E3/E7/E63 caused no second dispatch.
- Scope is explicit: it carried REPLAY and recovery of an already-installed birth, not a first new private effect, and the endpoint sees the call.

**(2) Status on main.**
- **BUILT (harness).** `testing/agreement-carrier-packet.rs`, `testing/agreement-carrier-scenario.py` and `testing/AGREEMENT-CARRIER.md` are on main (READ).
- Evidence directories are on hbox workbox, possibly wiped (INFERRED).

**(3) Frontiers and task coverage.** First new effect through the carrier: `01a10501-830d` (bundled with traffic). Separated roles and hosts: `01a10501-83a6`, `01a10501-835d`.

**(4) Contradicts main.** None.

### A11. work/FN-SWARMPLAN-20261004.md (shared-box and fn-node interface only)

**(1) Claim** (the parts that bear on Mini):
- **Mini lanes on hbox.** They are capped at ≤6 Lean lanes under `swarm-build` (96 G slice, `LEAN_NUM_THREADS=2`), plus one serialized `lake build Minidregg` every ~2 h.
- **Coexistence rules.**
  - fn jobs also run under `swarm-build`.
  - The peak hbox load target is ≤16.
  - Nothing starts or stops `/tank/fn/node`, the Mini worlds, the Studio servers or the mesh.
  - No cleanup under `/tank/fn/gates/`: `qual-bbf52159-20260925` is in use by the gitweb preview.
- **The live fn node** is pid 1477123 under `/etc/systemd/system/fn-node.service`.
- **The fn ↔ Mini interface.**
  - fn 6.6.0 offers signed exact-byte storage, idempotent resend and a local consumer cursor (poll/wait/ack on the control socket).
  - It does NOT offer a remote consumer, a cursor/ack that names a store history and view, or a non-NNTP inter-node protocol.
  - "The redis of it all" extensions are 6.6.1, with an optional zmq-pattern spike (row 6). That is ember's decision.

**(2) Status on main.**
- Mini consumes fn through `FnSelectiveRelease*`, `FnOriginOutbox` and `fn_frontier.rs`, a Host polling a pinned fn service (READ via the CHANNELS sub-reader).
- `docs/FN-*.md` (E1/E2 2026-09-24) are older experiments (READ, ls).

**(3) Frontiers and task coverage.**
- A remote-consumer interface for Mini: NO TASK in minidregg. It is a §6 decision in the fn plan.
- `fn_consumer/fn_agent/fn_client` "move to Mini?": NO TASK.

**(4) Contradicts main.** CHANNELS.md models fn as carrying portal articles (TRAVELLER/RETURN). These exist in no ref on main (READ via sub-reader).

### A12. scouts-20261003/D-deos-efficiency-semantics.txt

**(1) Claim.**
- Defect ledger D1-D18 and "idiotic" bounds B1-B8.
- Ranked hotspots:
  1. cold audit 614 s;
  2. room query ~2 s at 65 KB / 1,016-item proof;
  3. List-based Lean session;
  4. 124 s agreement doc call;
  5. a single serial Host;
  6. process spawns.
- The semantics gap: SHARED-CONTRACTS identities have no source; 7 `Observation` types, ~10 `Reservation` types, 33 version twins, 52 Receivers, 40 attempt-dir copies.
- Top-8 lanes.

**(2) Status on main.**

| Item | Status |
| --- | --- |
| D12 | **LANDED** (`91900705`) (READ) |
| D15 (queue residence → 254) | **LANDED** (`2a72f8ed`) (READ) |
| D16 (per-mutation test removed from the harness) | **LANDED** (`8283579d`) (READ) |
| Incremental audit | **LANDED** (`9c2de2f1`), "UNCOMPILED by the lane". The profile showed 1064 s on a loaded box, 745 s of it being four lifecycle records rebuilding from genesis (READ-rec, ledger 09:00). No post-fix timing is on record. |
| B1 room schema | **HELD.** Schema v2 with an open-ended field tail and the 499 cap removed; re-genesis; key codec v3→v4, schema refs v4→v5, LOG-TAG v1→v2. Before: v1 room read 4.95 s / 165 KB (READ-rec, ledger 10:05). |
| Indexed session | **HELD**, same lane (READ-rec). |
| Client batching | **PARTLY.** "chat runs workspace operations in-process" (`336b7c0e`), plus the room→index pointer hint (`1ffe6bf3`) (READ). |
| Contract types | **PARTLY** (A3). |
| Version-twin deletion, attempt-custody envelope, receiver collapse | **NOT DONE.** The SDK custody machine is the first piece (`native/mini-sdk/src/custody`), with Discord as the first consumer (READ). |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Audit superlinearity | `01a0fa73-e626` (breadstuffs repo) |
| Store open O(history) | `01a0f63a-233a` |
| Room schema v2 | NO TASK (successor brief only) |
| Twin deletion | NO TASK |
| Attempt envelope | SDK migration tasks `01a104fe-953e` and others |
| Hermes discovery fairness (B7) | NO TASK |
| Scheduler lifetime receipt ceiling (B5) | NO TASK |

**(4) Contradicts main.** It lists D12/D15/D16 as open; they have landed (READ).

### A13. scouts-20261003/E-infra-runbook.txt

**(1) Claim.**
- The live hbox inventory:
  - A1 common OO world in an ssh scope, unsupervised, tmpfs socket;
  - A2 SPK r2 world on stacked drop-ins, with the broker running as root;
  - A3 r1 demo;
  - A4 Sept-27 gitweb fixtures;
  - B1 the four-source mesh, whose broker child is dead;
  - the fn node;
  - eight Studio servers.
- The safe 00f711 lookup recipe (never `--mode submit`).
- The build runbook (swarm-build, warm trees, persvati seats).
- Fifteen hazards.

**(2) Status (READ-rec, ledger 01:15-01:50).**
- L0.3 installed 14 user units under `mini-hbox-recover.target` (inactive) and a system target for r1/r2, keys backed up at `/tank/claude-evidence-20261004`.
- Orphans: the rpc proxy and tailscale were stopped. hbox rejoined headscale as 100.64.0.2 (ledger 06:15).
- The workbox wipe after that changes the warm-tree facts:
  - the codex-unified-integration warm oleans (15 GB) are gone;
  - the cut was preserved at `/tank/dregg-build/claude-lanes/warm-base`;
  - **new lanes clone under `/tank/dregg-build/claude-lanes/`** (ledger 02:35, 03:15).

**(3) Frontiers and task coverage.** A1 adopt into units: NO TASK (a root decision). Warm bases: `01a0f533-b2cc`.

**(4) Contradicts current state.** The warm-tree paths in §3 are partly obsolete after the wipe (READ-rec).

### A14. scouts-20261003/F-privacy-agreement-guarantees.txt

**(1) Claim.** Stated vs implemented guarantees for traffic, agreement, MPC, FHE, zk and oblivious execution.

| Area | What F found |
| --- | --- |
| Traffic | Every role on 127.0.0.1; 16/16 is one replayed read-only lookup. |
| Agreement | Lean-model safety theorem; 4 replicas, 1 host, 1 process; third op stalled. |
| MPC | Public fixture inputs. |
| FHE | 2a+b with one owner. |
| ZK | `PackedRefinement` is a hypothesis with no inhabitant. |
| Oblivious | Targets the retired BendTT. |

It also gives an honest "show a friend" list and the shortest path for the two alpha requirements.

**(2) Status on main.**

| Area | Status |
| --- | --- |
| MPC | **IMPROVED.** Width-8 adder over private inputs with per-dealer OS entropy and a curious-holder transcript-secrecy check over 8,067 frames (`cf6a4c1d`). The old r31 dealing leaked each input bit and is kept as a negative control (READ git log; READ-rec ledger 04:50). |
| FHE | **Unchanged on main.** The Objective-over-FHE lane work (r34-r36) is likely LOST in the wipe (READ-rec). BFV noise theory landed (`Theory/Bfv*`) but is not imported. It found the margin ≈2^40.6 cross-term, and depth 2 survives only while relin noise is ≤2^52.39, against a possible worst case of ≈2^54 (READ-rec, ledger 04:35). |
| ZK | The zktruth lane strengthened F's finding: PackedRefinement is **trivially inhabitable**, and there is a decoder counterexample. HELD (READ-rec). |
| Agreement | Fixes A/B INSTALLED 00f711 on an evidence copy (737.6 s, identical receipts, no resubmission), but they are **not on main**. The lander resolved the rebase conflict in its own tree (READ-rec, LANDING-INVENTORY). |
| Traffic | Roster enrollment landed. No two-host run and no new effect (READ-rec). |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Agreement rebase + fix C | `01a10539-ae89` |
| Stack overflow in the journal decoder | `01a10539-ae49` |
| 20 s per iteration | `01a10539-aeca` |
| Fourth failure domain / move replicas | NO TASK |
| Traffic two-host + new effect | `01a10501-830d` |
| FHE rebuild | `01a105af-d204` |
| FHE worst-case noise | `01a10501-82d1` |
| zk PackedCodec | NO TASK |

**(4) Contradicts main.** It says MPC uses public inputs only; that is no longer true (READ).

### A15. scouts-20261003/G-product-journey-public-node.txt

**(1) Claim.**
- "Two friends + hosted Hermes in one world" has never run.
- The public node is on 5688775a (10-01). Hermes, Discord and pay are off, and only test keys are on it.
- Two journey instruments (`journey.sh`, `composed-scenario.py`) do not meet.
- No SPK app has served a browser.
- Ten blind spots and the top-8 product lanes.

**(2) Status on main.**

| Lane | Status |
| --- | --- |
| Lane 1 (DEPLOY-3) | **PARTLY.** One packager `deploy/candidate/package.py` accepts build/lane/capsule candidates and refuses mixed families (`e22f557f`). The consent role and Linux friend bundle (`8954553d`) and the composed scenario N-member spec, strict `gate` and world-restart (`09fe437e`) are on main (READ). `jdeploy3.sh` and the ship.sh glibc check are in dregg-infra `c065497` on `hbox:/srv/git` only (READ-rec). The candidate was not built, and the smoke gate is honestly RED: apps → SPK v4, residents → events, documents → forced-ssh binding (READ-rec, ledger 07:40). |
| Lane 2 (room latency) | **HELD** (schema v2). |
| Lane 3 (Hermes on main) | NOT DONE. |
| Lane 4 (browser app) | **NOT DONE.** The SPK v4 lane is HELD. Broker and resident bootstrap require root by code (READ-rec). |
| Lane 5 (Discord) | Waits on ember (A7). |
| Lane 6 (Studio for members) | NOT DONE. |
| Lane 7 (one gate) | PARTLY (`09fe437e`). |
| Lane 8 (native Objective effect) | **NOT ON MAIN** (W1.2 HELD). |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| DEPLOY-3 | `01a0f52e-7711` |
| DEPLOY-3 first box run | `01a0f5fd-648b` |
| DEPLOY-4 | `01a0f52e-7707` |
| Backups age | `01a0f52e-771c` |
| THE BAR | `01a0f9c0-521b` |
| M1 first hour | `01a0f9c0-55af` |
| Hermes live | `01a0fb03-bc64` |
| SPK→doc | `01a0fc44-0146` |
| SPK v4 | `01a10500-f341` |
| Members' Studio route | NO TASK |
| One gate at the end | NO TASK (beyond `09fe437e`) |

**(4) Contradicts main.** "Ship script cannot take hbox packaging" is now false on the Mini side (packager) (READ). The other claims stand.

### A16. scouts-20261003/R2-1-security-residuals-at-HEAD.txt (pinned at c8fdd000)

**(1) Claim.**
- Residual ledger:
  - #4 one uid for everything is CRITICAL;
  - #2 proxy signing is fixed in source but not shipped;
  - #3 private rooms are closed by being disabled;
  - #11 tickets and the install wedge.
- None of the new regression tests is in a gate. CI has never passed.
- The first-friend precondition list (a)-(h).

**(2) Status on main.**

| Item | Status |
| --- | --- |
| #4 one uid | **STEP A BUILT in code.** Operator `--peer-uid` allowlist (`transport.rs:1226-1240` `OperatorPeers`), `--socket-gid` public socket, owner-private 0600 `read_secret` with zeroize, passphrase scrubbed from children, anchor custody refusal (`535fea1e` and siblings → `86bb0b05`) (READ). **NOT DEPLOYED.** The dregg-infra split-tenancy install (`c98386d`, `866a415`) sits in a lane clone, unpushed (READ-rec). Step B (per-friend uids, mini-keys) is design. |
| #4a `--operation-record` | **FIXED** (`336b7c0e`, "confined by descriptor, with a gate") (READ). |
| #2 consent | **PARTLY.** The packager knows the consent role (`build.sh:300-303`, `package.py:58,74`), but the consent build step `b45237d1` is not on main. FRIENDS.md still does not mention `MINI_CONSENT_HOST` (READ, grep empty). Lane S7 is rebasing it (READ-rec). |
| #3 private rooms | **REBUILT** (`4564a8fa`): founder-pinned lineage, two-phase release, dead drafts, stubs deleted. See B6 (READ). |
| #3 AAD | Resolved by design: the stream address is the revision. Protected atoms now carry binding v2 (READ, `PRIVATE-ROOMS-DESIGN.txt` §3). |
| #5 refusal charging | **OPEN.** `Kernel/RefusalLane.lean` is uncommitted (READ-rec; not on main, READ). |
| #8 grain journal | **FIXED** (`6a291924`). |
| #8 torn tail | **FIXED** (`fa84160e`). |
| O3 loop-mount | **FIXED** (`6904304a`). |
| R3 rate limiter | **FIXED** (`664ee3c4`). |
| R6 hex | **FIXED** (`c158f9ba`). |
| O5 scheduler | **FIXED** (`0c148911`). |
| #11 tickets / expiry / wedge | **OPEN.** The patch is uncommitted (READ-rec). |
| Gates | 18 rust-test rows armed (L0.4) (READ-rec). CI is still red (see Baseline). |

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Tenancy step B | `01a104f3-e258` |
| Two-uid tests | `01a104f3-e2cb` |
| Split-tenancy journeys | `01a104f3-e2a8` |
| Refusal charging | NO TASK |
| Ticket expiry, tombstone and 8→2 reconciliation | NO TASK |
| Consent shipping + FRIENDS env vars | NO TASK (lane S7 only) |
| Anchor keyed vs owned | decided "owned" in TENANCY-DESIGN; no task needed |

**(4) Contradicts main.** Its HEAD-state claims for #3, #4a, #8, O3, R3, R6 and O5 are now stale (READ).

### A17. scouts-20261003/R2-3-agreement-liveness-three-hosts.txt

**(1) Claim.**
- 00f711 stalled lawfully. Replicas 0 and 1 time out before q VOTEs because Δ (15-27 s per drive iteration: one process, a subprocess per packet/MAC/sign, debug crypto, whole-journal CAS) far exceeds timeout/7.
- The engine runs only while a client request is open.
- There is a resend starvation path after reopen.
- Fixes:
  - A: standing replicas;
  - B: cut Δ;
  - C: adaptive timeout, which changes `step` and needs re-proof.
- Three hosts are not four failure domains.
- Never copy a live replica.
- An honest Oct-13 label.

**(2) Status on main.**
- **NOT ON MAIN.** No `serve-replica` (READ, grep).
- Fixes A+B proved out on an evidence copy: 00f711 installed in 737.6 s, p50 23.1 s per round trip (READ-rec).
- Fix C was written, but it is uncommitted and uncompiled, and it needs a fifth context field (re-genesis) (READ-rec).
- Three-host prep is done:
  - fresh devnet keys exist per host: replicas 0 and 3 on hbox, 1 on persvati, 2 on the Mac;
  - persvati lingers;
  - hbox is back on the headscale tailnet, so workhorse can be the fourth domain (READ-rec, ledger 05:40, 06:15).
- The live mesh is untouched and still stalled (INFERRED).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Rebase + C + stall test + CUTOVER.md | `01a10539-ae89` |
| Decoder stack overflow | `01a10539-ae49` |
| Per-iteration cost | `01a10539-aeca` |
| Move replicas, fourth box | NO TASK |
| Liveness measurements (kill -9, 30-op p50/p95) | NO TASK |
| Key custody and topology | on ember's pause list (topology and key material) |

**(4) Contradicts main.** `docs/GENERIC-SIMPLEX-NATIVE.md` still says "The first actual signed source action remains pending". Records show room birth and document birth installed (READ-rec). The doc predates both and says nothing of the stall.

---

## B. Repo and planning docs

### B1. README.md (main `0a7295ac`)

**(1) Claim.**
- Lean owns semantics and admission; Rust owns the physical boundary.
- The world comprises: the deos/docuverse, Objective Bend, SPK hosted apps, Hermes and residents, the agreement mesh, private execution as research, and Selvage.
- An "Honest state" table grades each component by evidence class: authored, compiled, executed, integrated, deployed.

**(2) Status on main.**
- The table is accurate, and S8 updated the completeness row at `0a7295ac` (READ).
- **"Payments: executed (fixtures)" is still true.** The address now exists (5N2u…, 50 DREGG/week; READ-rec, ledger 13:40). `deploy/pay/enrol.json` still holds the placeholder `EMBER_ENROL_ADDRESS` (READ). Lane S7 is wiring it in (READ-rec).
- **"Proofs not in the default gate" is true.** Theory/ObjectiveBend* is imported only by ResearchWip (READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Website vs README | `01a104f3-e35e` |
| Docs citing out-of-repo paths | `01a104f3-e386` |

**(4) Contradicts main.** None found at `0a7295ac`. At `1ffe6bf3` it still said "completeness open"; that is fixed now.

### B2. deploy/shell/FRIENDS.md

**(1) Claim.** The friend-facing guide covers:
- reset warnings and key custody, with an honest one-uid line (`86bb0b05`);
- next-key rotation; proxy mode (`--remote`);
- first 10 minutes, laws and `law check`, documents and transclusion/history/web, rooms, templates and leave;
- chat, a paid week in a room, private rooms (with the devnet/TOFU label);
- `can`, jobs, the sealed market, the Hermes librarian, exit codes.

**(2) Status on main.**
- **AHEAD OF DEPLOYMENT.** The public node runs 5688775a (10-01), which carries shell, documents and J0-J8 but not rooms or chat from the hbox line. Hermes, Discord and pay are inactive there (READ-rec, G). A friend reading this today would hit verbs the box lacks (INFERRED).
- **Proxy mode.** The steps omit `MINI_LOCAL_HOST`, `MINI_CONSENT_HOST` and `MINI_CONSENT_CONFIG`, which the client now requires to sign (READ, grep). So a HEAD-built client cannot sign in proxy mode by following this guide (INFERRED from R2-1 #2).
- **The web section** says "read-only pages", but `web.rs` accepts POST forms (READ via DEOS sub-reader).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| JOIN-SOLANA friend section | `01a0f52e-76fd` |
| FRIENDS infra copy | `01a0f6d0-e063` |
| Consent env vars | NO TASK |
| Stale lines | NO TASK |

**(4) Contradicts main.** The proxy steps omit the consent requirement main now enforces (READ). "Read-only" web is out of date (READ).

### B3. docs/SDK.md + docs/design/SDK-DESIGN.md (lane W2.H)

**(1) Claim.**
- One client library: Rust core (wasm32-clean) plus TS (`@minidregg/sdk`).
- The flow:
  - Profile → typed `Intent` over the six cuts → `explain()` of Host-presented JSON;
  - nonce-bound `Confirmation` → sign only the consent-returned headers → submit → `Receipt | Refused | Uncertain`;
  - on `Uncertain`, look up the SAME call bytes.
- Trust is CLIENT-LOCAL.
- Profiles are `blake3 derive_key("mini/<gen>")`, distinct from Bread's `dregg/0`.
- The browser extension waits on a native-messaging bridge or a thin-peer consent producer.

**(2) Status on main.**
- **BUILT.** `native/mini-sdk` (29 unit + 3 golden tests, including byte-exact lowering to a real admitted `intent.json`) and `native/mini-sdk-ts` (15/15 against a wasm oracle; 4 mutants red). Discord custody has moved onto it (READ files; READ-rec counts). Linux control passed (`0f3de3c3`, READ-rec).
- **Gaps:**
  - SDK-owned intent encoding, not the Lean codec;
  - Reserve/Install/Release/Retire do not lower;
  - op 227 Objective consent is not wrapped;
  - local Unix socket only.

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Lean codec | `01a104fe-94a5` (lane S10 running) |
| op 227 | `01a104fe-94fb` |
| `app_document.rs` onto the SDK | `01a104fe-953e` |
| `ssh:DEST` route | `01a104fe-958e` |
| Browser extension | NO TASK (correctly gated) |
| Hybrid Ed25519+ML-DSA signer | lane S10 only, NO TASK |

**(4) Contradicts main.** SDK-DESIGN says the Lean types will live in `Theory/Contracts/*`. They landed as `Kernel/Contracts/*` (READ). Minor.

### B4. docs/design/law-composition-source-codec.md (Codex, 10-02)

**(1) Claim.**
- Policy records get a typed `Component` (selector + Pred + PolicyRef list), local plus descendants.
- One canonical v5 codec.
- A historical loader walks authenticated `previous` records.
- The resolved effective conjunction is an ordinary Pred, reusing PredCompile.
- Proof obligations: resolve completeness, DFS depth, coverage, canonical order.

**(2) Status on main.**
- **BUILT in source and integrated into the kernel closure.**
  - `Pred/LawComposition.lean` is imported by `Compiler/CanonicalPolicyAdmission`.
  - `Compiler/PolicyComponentResolution.lean` is imported by `Compiler/ComposedPolicyAdmission` and `Compiler/CandidateLawResolution` (READ).
- The doc's paths (`Theory/LawComposition.lean`, a `codex/law-composition` snapshot) are stale (READ).
- Whether the listed proof obligations are discharged is not checked here.

**(3) Frontiers and task coverage.** K-LAW diagnostics: `01a0fc50-4f28`. Resolve-completeness proofs: NO TASK.

**(4) Contradicts main.** It describes itself as unswitched and uncompiled, but main imports it into admission (READ). Ember should treat the doc as stale.

### B5. docs/design/world-kind-executable-methods.md (Codex, 10-02)

**(1) Claim.**
- World-resident kinds carry one ROM method table: unique name, program ID, output→(field, key) map.
- `instance call` maps evaluator outputs to field writes through the existing Nock evaluator.
- Compute funding: 1,000,000 steps per subject per day free, then 1 credit per step, committed atomically with the effect.

**(2) Status on main.**
- **BUILT in source.** `Kernel/WorldKindMethods.lean` is imported by `Kernel/ResourceTransaction.lean`; `Kernel/RunComputeBudgetDomain.lean` is imported by four kernel modules; `Compiler/WorldExecutionContract.lean` exists (READ).
- The shell has `instance call … --fund ACCOUNT --max-compute-credits N` (`shell.rs:75,2073`) (READ).
- Nock-only. It is the precursor to Objective methods.

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| NOCK-FEE decision | `01a0f96d-f34c` |
| ABI noun+max | `01a0f96d-f323` |
| Objective methods replacing method tables | NO TASK. W1.2 is the carrier. |

**(4) Contradicts main.** "Has not yet passed Lean" is stale (READ: imported by core).

### B6. docs/PRIVATE-ROOMS-DESIGN.txt (lane W1.9b) + the older claudesplosion `planning/privacy/private-rooms.md` (10-01)

**(1) Claim.**
- Threat model:
  - the operator is honest-but-curious (primary) and active (secondary);
  - on a single-validator devnet, chain-rooted authority equals the operator's word, so authority comes from keys PINNED OUT OF BAND.
- The design:
  - a founder pin and member pins;
  - a founder-signed epoch certificate chain with client monotonicity;
  - one live release draft, with dead drafts burned;
  - two-phase release: BOUND release atoms → APPLIED readback → DISCLOSED wraps;
  - envelope address = revision; protected-atom binding v2.
- Residuals stated: R1 freeze, R2 first-sight, R3 metadata, R4 founder rotation, R5 not PQ.
- The PQ hybrid is designed and deferred.

**(2) Status on main.**
- **BUILT** (`4564a8fa`, `8c67fc66`, `d38116cd`): `roomkey.rs` has founder pin, release and epoch-head paths; `current_recipient_source.rs` was deleted (READ).
- **Not built:**
  - no ML-KEM in `roomkey.rs`/`private.rs` (READ grep; lane S9 running);
  - no end-to-end run on a real Host (task).
- The 10-01 claudesplosion version (unpinned wraps, J-PRIV-1) is OBSOLETED by this design (READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| PQ hybrid | `01a104f3-e2ed` |
| Founder-key transition | `01a104f3-e30f` |
| Freeze | `01a104f3-e331` |
| End-to-end | `01a104fd-8e73` |
| First-time reader | `01a104fd-8ef8` |
| Per-wrap grants | `01a0fadb-65ec` |
| Hosted private invite | `01a0f72b-7d95` |
| Discord mirror | `01a0f99e-d668` |
| Retire RoomRelease* | `01a104fd-8fc1` |
| Arm tests | `01a104fd-9015` |

**(4) Contradicts main.**
- §0 describes c8fdd000, now superseded by its own landing (READ).
- Its "devnet quality" label is mirrored correctly in FRIENDS.md (READ).

### B7. TENANCY-DESIGN.txt (lane W1.8; in the session scratchpad, NOT in any repo)

**(1) Claim.**
- Today one uid `mini` holds the Store, the operator socket, the seal key, the anchor, every friend's keys and the sudo rule.
- **Step A:**
  - a `mini-core` operator account;
  - tenant `mini`;
  - sessions reach only the public relay (`--socket-gid`);
  - the operator socket gets a peer-uid allowlist;
  - `session_fs` on every path verb;
  - anchor custody by ownership, not by key.
- **Step B** (ember steers): `mini-keys` and a key-service socket, per-friend `mini-s-NAME`, `mini-proxy`, per-user sshd.
- Split mode refuses `provider-service.json` and `discord.env`.
- Migration is re-provisioning, not migration.

**(2) Status on main.**
- **Step A: BUILT in Mini code** (READ; see A16).
- **Step A: NOT deployed.** The dregg-infra `install.sh tenancy=split` is unpushed (READ-rec).
- **Step B: DESIGN.**
- **The design file itself is not committed anywhere** (READ). The commit message cites it, so a reader six weeks out cannot find it (INFERRED).

**(3) Frontiers and task coverage.** `01a104f3-e258`, `-e285`, `-e2a8`, `-e2cb`; MINE "protected head frontier → tenancy step B" `01a10556-49ec`.

**(4) Contradicts main.** None in code. Its refusal of `discord.env` under split mode conflicts with the Discord go-live plan (§C).

### B8. deploy/discord/README.md

**(1) Claim.**
- An interactions endpoint, with no gateway and no bot token on the box.
- Commands: `/mini`, `/mini-help`, `/mini-world`, `/mini-status`.
- Durable interaction custody; UNKNOWN is never rerun.
- The mirror runner is an enrolled bridge member with per-direction custody and paged backfill.
- Ember's steps: the Discord app, `commands.json`, Caddy `discord.dregg.net`.

**(2) Status on main.**
- **BUILT** (code and tests) (READ).
- **NOT DEPLOYED** (READ-rec, G).

**(3) Frontiers and task coverage.** As A7, plus the native total-byte page budget for large rooms: NO TASK.

**(4) Contradicts main.** None.

### B9. deploy/pay/README.md + deploy/pay/enrol.json (payments / self-enrollment)

**(1) Claim.**
- A one-tick Solana watcher derives its config from the signed pay view, retains the whole tick, and submits `pay observe`.
- Self-enrollment records go to the operator-socket receivers (ops 117-120).
- The genesis names a `payObserver`.
- `book.json` holds the tariff.

**(2) Status on main.**
- **BUILT as fixtures.** JPAY1-6 run on their own Stores (READ-rec, G).
- **DEPLOYMENT OPEN.**
  - `enrol.json` holds the placeholder `EMBER_ENROL_ADDRESS` (READ).
  - The address (5N2u…) and the rate (50 DREGG/week) were supplied on 10-04; lane S7 is wiring them in (READ-rec).
  - Toothless hypothesis families were given instances (L0.4): `Kernel.PayEnrolClaim.Claim.valid` and `Consumption.matchesClaim` (READ-rec).
  - `Kernel/PayCellUpgrade.lean` currently fails the umbrella build with `sorryAx` (READ, CI log).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| DEPLOY-4 | `01a0f52e-7707` |
| Host-priced enrollment | `01a0f6d0-e044` |
| `--remote` join | `01a0f6d0-e055` |
| Operator socket + tick env | `01a0f6d0-e063` |
| Throughput | `01a0f6d0-e072` |
| Self-enrolled next-key | `01a0f910-d000` |
| Blind observer refusals | `01a0f674-fa46` |
| PayCellUpgrade red | NO TASK |

**(4) Contradicts main.** None. The red build of `PayCellUpgrade` contradicts any "payments compiled" reading (READ).

### B10. deploy/hermes/README.md + deploy/hermes-dispatch/README.md

**(1) Claim.**
- Hermes never holds a provider key.
- Per-call route: `user` / `pool` / `homelab`, chosen from a root-owned `providers.json`, with no fall-through between payers.
- Provider keys are sealed under `/etc/mini/credentials.key`, bound to subject + workspace key + provider.

**(2) Status on main.**
- **BUILT in code** (`hermes.rs`, `hermes_handoff.rs`).
- **Executed only with a scripted provider** on a private Store (README).
- **Off on the public node** (READ-rec).
- Split tenancy refuses `provider-service.json` until key-service moves behind a `mini-core`/`mini-keys` socket (READ, TENANCY-DESIGN §4).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| HERMES-LIVE | `01a0fb03-bc64` |
| Summon dispatch | `01a0fc5d-4eba` |
| Tariff 2/3 | `01a0f701-0e4f`, `-0e6d` |
| BYOK remote custody | `01a0fbc7-a94c` |
| Homelab scheduling | `01a0fb11-e4db` |
| `providers.json` + Chutes key | in `01a0f54c-d1dd` |

**(4) Contradicts main.** The README's custody line ("root … and the mini service user") is true today and becomes `mini-core`/`mini-keys` under tenancy (INFERRED).

### B11. deploy/spk-host/README.md (Sandstorm/SPK apps)

**(1) Claim.**
- The physical half of the long-lived app resource:
  - SPK signature, hash and manifest verification;
  - cgroup-bounded ingest;
  - a root broker with typed verbs (place/ingest/mount/install-unit/start/stop/export/backup);
  - resident unit names pinned by Mini.
- No `run` CLI until admission is connected.

**(2) Status on main.**
- **BUILT (physical layer).** The broker symlink race, setuid capability and loop-mount fixes are on main (READ: `6904304a`; R2-1 #1/#9 via record).
- **Missing from main:**
  - **Lifecycle recovery.** Main still says "reconcileFailedStart receiver is absent" (`native/spk-host/src/grain_export.rs:213`), and `jspk1.sh:277` now fails on it (READ). The SPK recovery that the live r2 world actually ran exists only in codex lane tars (READ-rec, MINE item 1).
  - **SPK v4** is HELD.
- `docs/SPK-LIFECYCLE.md` is NOT on main (READ).
- No app has served a browser (README).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Recovery mine | `01a10556-492a` |
| v4 land | `01a10500-f341` |
| Replay of v4 completion | `01a10500-f26d` |
| Restart lookup | `01a10500-f2bc` |
| Unit names carry the store | `01a10500-f1d1` |
| Unprivileged broker | `01a10500-f228` |
| SPK → Mini doc | `01a0fc44-0146` |
| Powerbox apps | `01a0f84c-ec80` |
| WebSockets | `01a0fa13-*`, `01a0fb2e-f6c7` |
| Dispatch fee | `01a0f616-5133` |

**(4) Contradicts main.** None in the README. The README's "Honest state: integrated (install, recovery)" overstates recovery, since main's recovery receiver is absent (READ).

### B12. docs/GENERIC-SIMPLEX-NATIVE.md (agreement mesh)

**(1) Claim.**
- A native Generic Simplex domain log: n=3f+1, ML-DSA-65 transferable COMMIT certificates, durable compare-and-append journal.
- The source participant: ingress → offer → certified order → fresh re-derivation → append/readback.
- An operator bridge maps only opcode 2 onto agreement.
- Limits are stated: one driver, not four failure domains; no reconfiguration or compaction.

**(2) Status on main.**
- **BUILT** (compiled): `Kernel/GenericSimplex*.lean` (~40 files), `Compiler/GenericSimplex{Codec,Controller,IO,Native,Participant,Pending,SourceAnchor,Transferability}.lean`, under `SimplexQualification.lean` (READ).
- **Liveness fixes A/B, standing replicas and the multi-host transport: NOT ON MAIN.** The lander tree holds the resolved rebase (READ-rec).
- `Kernel/GenericSimplexReconfig` and `Kernel/AgreementEvidenceRegime` are uncommitted (READ-rec; absent, READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| A17 frontiers | `01a10539-*` (see A17) |
| Reconfig/CertF | `01a10501-8293` |
| AgreementEvidenceRegime | `01a10503-6c57` |
| Bind the native consumer to the reachable-engine proof | NO TASK |
| Checkpoint/GC | NO TASK |

**(4) Contradicts main.** "First actual signed source action remains pending" is stale: two installs are on record (READ-rec). It says nothing of the stall or the fixes.

### B13. docs/TRAFFIC-PRIVACY-PROFILE-P1.md (traffic privacy)

**(1) Claim.**
- A user-facing leakage card for the W=4 PQ onion cohort.
- **Trust:** a non-colluding registrar, at least one honest relay, an honest receiver, at least two honest members, static corruption, no later key disclosure.
- **Visibility:** the endpoint sees the plaintext call.
- **Crypto:** pure ML-KEM-768 with no hybrid; Ed25519 authority means it is not PQ end to end.
- **Cost:** ≈66 GB per member per 30 days.
- **Latency:** 10-17 s.
- Six failure-leak classes.
- Enrollment is now a signed roster.

**(2) Status on main.**
- **BUILT** (`pq_mailbox.rs`, `cohort_tcp.rs`, `scheduled_transport.rs`; roster enrollment `d7b2f19b`) (READ).
- **Evidence is single-host v12 only.**
- The Linux qualification of roster enrollment is open (task).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Linux qualification, two-host v13, new effect | `01a10501-830d` |
| Wi-Fi power-save | `01a10501-835d` |
| MAC keys, separate uids | `01a10501-83a6` |
| Stranger-listener test restored | `01a10510-6e60` (claimed) |
| Observation-game proof | NO TASK |
| Forward secrecy / key lifecycle | NO TASK |

**(4) Contradicts main.**
- "Later runs (two hosts, a new effect) are recorded in the traffic lane's STATUS" points at runs that did not happen. The lane wound down before v13 (READ-rec, ledger 04:35/03:55).
- The card should say "none yet".

### B14. native/private-backend/CONSTRUCTION.txt (MPC)

**(1) Claim.**
- Reference asynchronous protocols with crash WALs: ASKS V2, IndexGather/VABA/ACS, dZK→ACSS-Id, Sh2t-Id, TripleKing Beaver triples, recipient PrivSend, a recipient-only ML-KEM seal, physical one-use custody.
- Explicit limits: variable-time GF(2^128), static f<n/3, classical ROM, no simulator/GOD/PQ.
- The clear native route would see share bodies.

**(2) Status on main.**
- **BUILT** (crate; READ).
- **Plus on main:**
  - private inputs with OS entropy and a transcript-secrecy check (`cf6a4c1d`);
  - the D12 circuit_batch postimage (`91900705`);
  - the torn final WAL record now truncates (`fa84160e`) (READ).
- The 429-stock King run passed only "by accident on the Mac", not the sanctioned hbox run (READ-rec).
- `docs/MPC-PROFILE-P2.md` is NOT on main (READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Committee v4 | `01a10556-494b` |
| Composite King crash-store + kill -9 | NO TASK |
| Sanctioned 429 rerun | NO TASK |
| Holder-private output and successor resharing | NO TASK |
| Confidential capsules in the native controller | NO TASK |

**(4) Contradicts main.** None.

### B15. deploy/candidate/INTERFACES.md (deploy)

**(1) Claim.**
- The operator procedure:
  - `build.sh` → manifest + SHA256SUMS + provenance from one `git archive`;
  - `run.sh init/start/sponsor`;
  - `journey.sh` is the definition of done.
- Toolchains and caches are pinned.

**(2) Status on main.**
- **BUILT.** `package.py` is now the single packager for build, lane and capsule candidates (`e22f557f`). The consent role and Linux friend bundle shape are on main (`8954553d`) (READ).
- The doc header is dated October 2 and does not mention capsules or `package.py` (READ, head). It is stale on shape.

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Grain-runtime reproducibility | `01a0f830-42e7` |
| Sponsor-key custody | `01a1052c-6e3a` (EMBER; default A stands in 3 days, READ-rec) |
| DEPLOY-3 | `01a0f52e-7711` |

**(4) Contradicts main.** The header predates the packager (READ).

### B16. EVENTS-DESIGN.txt + docs/OBJECTIVE-BEND-EVENTS.md (deos scripting in Core4)

**(1) Claim.**
- An Objective Bend method can be an Activity<P,R,A>: `perform` yields a typed Plan and is resumed with a typed Response.
- A resident is a guarded fixed point across turns; an event is an admitted turn that resumes it.
- Effects are a type; partiality is a judgment.
- Compared against Bread's deos-js, Objective Bend is proposed as the deos scripting language (`DeosCounter.obend`).

**(2) Status on main.**
- **BUILT in semantics, typing and proofs:**
  - `typed_yield_quiescent`, `stack_activity_signature`, `typed_resume_preserved`, `state_roundTrip`;
  - the C machine runs activities (340/340 differential, `6909eaf9`) (READ).
- **NOT INTEGRATED.** "No kernel delivers responses or persists an activity yet" (READ).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Kernel response delivery | `01a1056f-0066` |
| Non-divergence / decoded typing | `01a1056f-0083` |
| Heap collection at yield | `01a1056f-00a4` |
| C port of events | `01a1056c-c498` (claimed) |

**(4) Contradicts main.** None. It contradicts DEOS.md's stance; see §C.

### B17. docs/STUDIO-SOURCE-WORKSPACE.md + docs/RESIDENT-CONTEXT.md (docuverse faces)

**(1) Claim.**
- **Studio** composes module documents into an ordered package manifest with revision-bound composition operations, retained drafts and forks. Preview is a separate route.
- **Resident context** is selected from current-authorized signed document reads, with `mini-context-{document,summary,bundle}-v1` pins invalidated by revocation or source change.

**(2) Status on main.**
- **Studio: PARTLY.** It is on main as `native/resource-client/src/web/studio.rs` plus `workspace/studio.rs` (READ). The doc says its own prototype declarations "still carry the Gen-1 shape … feed nothing" (READ).
- The Studio binaries that were "executed on loopback" were hbox lane builds (`mini-studio-callable-r26` etc.). Studio definition/publication r26 is a MINE item, not on main (READ-rec).
- **Resident context:** Lean selector plus Rust narrow tests (READ-rec, G).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Studio definition/publication | `01a10556-4a0b` |
| Lean elaborator as the implementation | `01a10500-6e65` |
| Members' Studio route | NO TASK |
| Rewrite or delete the Gen-1 prototype declarations | NO TASK |

**(4) Contradicts main.** README's "Studio … executed" describes lane binaries, not main's code (READ-rec vs READ).

### B18. claudesplosion planning/DEOS.md (10-01; delegated read)

**(1) Claim.**
- Mini already has a Xanadu-class docuverse kernel but a fifth of the verbs and "a terminal for a face".
- Rebuild deos as arrangements of cells plus three faces: shell, a loopback web page over the friend's own signed reads, Hermes using the same verbs.
- Refused: cockpit, cards-as-code, a JS runtime, seL4, `dregg-doc`.
- "Program = a law + a runner, never code in the cell."
- 23 lanes; journeys J19-J32; the Oct-13 floor is J19-J24.

**(2) Status on main.**
- **Most of the floor is BUILT:**
  - K-DOC-INDEX (`Kernel/LinkIndex.lean`);
  - K-TRANSCLUDE (`TranscludeRequest` with `StableRange`; no bytes copied);
  - K-DOC-HISTORY;
  - K-ELEMENT-TREE (`Kernel/ContentElementTree.lean`, `tree_acyclic`);
  - K-MARKS, P-DOC-RENDER, P-DOC-WRITE, P-AFFORDANCES (`can.rs` via op 130), templates;
  - web history/diff, plus POST forms;
  - J-DOCUVERSE journey hooks;
  - K-PREROTATE.
- **PARTLY:**
  - librarian (no `mini_doc_*` tools, no quote-not-copy law);
  - runs/ranges (no `range_stable_under_insert`);
  - inspect views; media; annotation bodies (no threads).
  - K-SEARCH was replaced by a client-side Rust re-read, `doc_search.rs`, with no Lean index.
- **DESIGN-ONLY:** K-FIELDS-DOC, K-DOC-BRANCH-MERGE, P-DOC-NOTIFY.
- **K-DOC-EVENTS:** decided "delete as a twin", yet `Kernel/HyperdocumentEventLog.lean` is still on main with no Host caller.
- **DEPLOY-DOCUVERSE: not done.**
- (All READ by the sub-reader.)

**(3) Frontiers and task coverage.**
- Covered:
  - umbrella `01a0f5e0-5a67` (stale);
  - QUOTE-DISCLOSE `01a0f53e-f651`;
  - event-log twin `01a0f96d-f360`;
  - ranges `01a0f6ad-8d64`, `01a0f611-ea6c/ea87`;
  - inspect `01a0f6e3-bc44/bc69`;
  - links at height `01a0f7c7-67ab`;
  - renderer history `01a0f70e-4a5f`;
  - web remote `01a0f5ef-d692/d6aa`;
  - petnames `01a0f70e-4a83`.
- NO TASK: K-FIELDS-DOC, branch/merge, `mini_doc_*` Hermes tools, media attach, notify, annotation threads, cards-as-data, stale FRIENDS/FN-CONSUMER-E1 lines.

**(4) Contradicts main.**
- §0's five namespaces vs main's ContentResource, which also has annotate, transclude, editElement, createContainer, unlink and mark.
- "Old decoders deleted" vs `Compiler/LegacyContentCarry.lean`, a frozen migration carry, against the greenfield rule.
- K-SEARCH Lean index vs the client re-read.
- "Web read-only" vs POST forms.
- Journey scripts cite a nonexistent "DEOS §8".
- (All READ.)

### B19. claudesplosion planning/SURPASS.md (delegated read)

**(1) Claim.**
- Mini vs Bread over 25 kernel capability rows: Mini is ahead on 14, level on 4, behind on 5.
- All five behind-rows need a second machine or entrance: PQ identity, fleets, consensus, light clients, SDKs.
- The spine is the **Turn cutover**: the Host runs `DurableDataIntent.execute` over post-images, not `World.step` over patches, and the two must become one (`host_submit_is_step`).
- Multi-machine work = portals plus a witnessed single sequencer (followers re-execute, a quorum co-signs heads). Blocklace is refused.
- 40 lanes; the floor is 16, dated Oct 26.

**(2) Status on main.**
- **BUILT:** T1 world-complete (`SysSpace` parent/spent/allowance; `Kernel/TurnCensus.lean`), `Theory/StoreNormalize.lean`, T3/T3b (`Kernel/TurnOfIntent.lean`, `Kernel/HostRefinesWorld.lean`: `ofIntent_step`, `deployed_refines_step`), K-PREROTATE.
- **PARTLY:**
  - T9: `step_conserves` holds only at the census Book.
  - A1: CI exists, but there is no `gate-head.sh`.
  - L1: per-address openings, but O(n), not O(log n).
  - The SDK.
- **DESIGN-ONLY:**
  - LIVE-EQUALS-REPLAY: R1/R6/R12/R19 asymmetries remain;
  - T4: `host_submit_is_step` is only a docstring; nothing in Host calls `World.step`;
  - T5, T2, T6-T8, T10 (`agree := by intro …; rfl` still at `MultiCellHyperedge.lean:573`);
  - T11 twins: `DataIntent` has grown from 137 to 235 files;
  - N1-N7, L2-L3, F2/F4/F6/F7.
- (READ by the sub-reader.)
- `Kernel/TurnOfIntent.lean` currently FAILS the umbrella build (READ, CI log).

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| T4 | `01a0f87d-02f7` |
| LER | `01a0f6c5-6891` |
| T5 legBytes | `01a0f740-26e4` |
| T1 credit | `01a0f740-26b0` |
| T9 | `01a0f740-26d5` |
| Store open | `01a0f63a-233a` |
| N1 half | `01a0f798-a0af` |
| L1 | `01a0fadb-65d6`, `-6617` |
| SDK | `01a104fe-*` |
| PQ fleet | `01a0f6bb-c108` |
| Umbrella | `01a0f6b0-ed49` |
| T2, T6-T8, T10-T15, N2-N7, L2-L3, F2/F4/F7, A4, S3, growth to 10^4-10^5 | NO TASK |

**(4) Contradicts main.**
- 33 vs 47 admission constructors.
- The finality export was deleted.
- "No CI" is false.
- "No SDK/TS client" is false.
- "Ed25519 only / no consensus in flight" vs ML-DSA-65 Simplex.
- World docs vs the deployed `clockOf = history.length` and the `fnGateway` read.
- A3's "2 @[export]" vs 26 on main.

### B20. claudesplosion planning/CHANNELS.md (delegated read)

**(1) Claim.**
- A channel domain is a room with a slot schedule. Each lease-holder sends one fixed-size cell per tick to a relay, which appends one `EpochRecord` per epoch. That record serves as order, availability commitment, witness heartbeat and duty roster.
- The observer is everyone but the recipient. Membership and presence are public.
- Tiers T0-T5, from padded line up to DC-net. One witnessed sequencer with a witness veto.

**(2) Status on main.**
- **BUILT:**
  - CH-CELL: `Theory/Channel/{Cell,Lease,Trace,Envelope,Audit}.lean`;
  - CH-EPOCH: `Kernel/DomainEpoch*.lean`, `ChannelStoreLaw`;
  - CH-RELAY-1: `relay.rs`, `channel-lib/`, `jchan-relay.sh`, missing 3/600 deadlines;
  - CH-CLIENT-1: `channel.rs`, `mini channel`.
- **NOT ON GITHUB:** CH-OMIT (the frame codec in Lean, the DCW2 signed witness, `tick_frames_chain`); its commits are in no ref.
- **DESIGN-ONLY:** leases/slots, KEM epoch, two nodes, duties, DC-net, T2, kernel step.
- In practice the PQ cohort mix has taken T5's role, sharing no code with this stack (INFERRED).
- (READ by the sub-reader.)

**(3) Frontiers and task coverage.**

| Frontier | Task |
| --- | --- |
| Umbrella | `01a0f6e9-bba8` |
| Sim follow-ups | `01a0f6fc-7372` |
| `channelStoreLaw` preservation | `01a0f7a6-6902` |
| Digest binding | `01a0f89a-d139` |
| Queue persistence | `01a0f89a-d173` |
| Relay RT priority | `01a0f81d-695a` |
| Sealed keying (10.10) | `01a0f96b-34f4` |
| CH-OMIT merge, U1 DAG sim, U2/U3/U7/U8/U9b/U10, `domain_order_total`, sender signature in cell, IK-CCA proof, `scheduleRoot` | NO TASK |

**(4) Contradicts main.**
- `Kernel/ChannelFrame.lean` and `tick_frames_chain` "PROVED": absent.
- DCW2 signed witness and `relay-equivocation`: absent (DCW1, unsigned).
- "CH-OMIT obligations LANDED 10-02": absent.
- Schema/law versions: v2/v7 and STORE-CELLS v8 stated vs `⟨91012⟩,3` and v14 on main.
- fn TRAVELLER/RETURN portals "LANDED": absent.
- Internally, a duty no-show is called "attributable", which its own `silent_and_dropped_indistinguishable` refutes.

---

## C. Synthesis

### Pillars, in dependency order

**1. World/kernel and its efficiency.**
- **Truth.**
  - Core4 is the only language: soundness, preservation, completeness and activities proved; a C machine runs 900-2900× faster than `runBounded`.
  - Proofs sit outside the default gate; the kernel admits no Objective receipt yet.
  - Main's umbrella is RED (StoreHiding, TurnOfIntent, PayCellUpgrade with `sorryAx`).
  - Admission runs on `DataIntent`, not `World.step` (SURPASS T4).
  - D12, D15, D16 and the incremental audit landed; the audit is unmeasured since. Schema v2 and the indexed session are HELD.
- **Next moves.**
  1. Land CUT-REBASE: a green umbrella, Gen-1 deleted, ObjectiveProofs gated. Rebuild the warm base under `/tank/dregg-build/claude-lanes/`.
  2. Land W1.2 native-b: the first admitted Objective receipt.
  3. Land kernel activity delivery (`01a1056f-0066`).
  4. Land schema v2 plus the indexed session (re-genesis) and re-measure the audit.
  5. Decide the C machine as executor (`01a10564-84ef`) and LIVE-EQUALS-REPLAY → T4.

**2. Docuverse/deos.**
- **Truth.**
  - DEOS's floor is mostly built (element tree, transclusion without copying, marks, history, `can`, templates, web with POST).
  - Studio's prototype declarations are Gen-1 dead code; r26 definition/publication is unlanded.
  - Nothing is reachable by members.
  - The event-log twin was decided "delete" and still exists.
- **Next moves.**
  1. Delete `HyperdocumentEventLog` and `LegacyContentCarry`.
  2. Rewrite Studio's declarations against `.obend`, or delete them; mine r26.
  3. Make the Lean elaborator the implementation (`01a10500-6e65`).
  4. Build the ObjectPresentation projection shared by web, Discord and Hermes.
  5. Members' Studio route.

**3. Privacy and rooms.**
- **Truth.**
  - Rooms are rebuilt (founder pins, two-phase release; TOFU, not PQ, no end-to-end run).
  - Traffic P1: a single-host W=4 cohort with roster enrollment; the endpoint sees plaintext; no new effect carried.
  - MPC now runs on private inputs.
  - FHE is one owner computing 2a+b; Objective-FHE was probably lost in the wipe.
  - The zk refinement is vacuous (PackedRefinement is trivially inhabitable).
  - No fixed-capacity tariff blocks the step-count leak.
- **Next moves.**
  1. Private rooms: end-to-end run on a real Host (`01a104fd-8e73`), then the S9 hybrid wraps.
  2. Signed versioned tariff (ticks, refuse on excess, never refund). There is NO TASK.
  3. Traffic: Linux roster qualification, then the first new effect, then two hosts with Wi-Fi power-save off.
  4. Land the zktruth PackedCodec correction.
  5. FHE: rebuild, then check worst-case noise.

**4. Agreement and failure domains.**
- **Truth.**
  - Main has the compiled engine and a Lean-model safety theorem.
  - Fixes A and B installed 00f711 only on a copy (p50 23 s).
  - The live mesh is one process on one host and still stalled.
  - The journal decoder overflows the stack on long journals.
  - Three-host keys exist; workhorse can be the fourth domain.
- **Next moves.**
  1. Fix the decoder.
  2. Land the lander's resolved rebase.
  3. Find the ~20 s per iteration.
  4. Fix C plus a re-check of the safety proofs (re-genesis).
  5. Ember decides topology and custody; then move replicas (never copy) and run the R2-3 measurements. The move has NO TASK.

**5. Apps/SPK and Hermes.**
- **Truth.**
  - The SPK physical layer is hardened.
  - Main lacks the failed-START recovery the live r2 world ran; v4 is HELD.
  - Broker and resident require root.
  - No app has served a browser.
  - Hermes has run only with a scripted provider; split tenancy refuses `provider-service.json`.
- **Next moves.**
  1. Mine the SPK recovery and land v4 after the cut.
  2. Put the store id in unit names.
  3. Lawful g4 START plus Playwright EtherCalc → CSV → doc.
  4. HERMES-LIVE on a scratch world; move key-service behind a `mini-core` socket.

**6. Payments and enrollment.**
- **Truth.** Fixture rail; address and rate are decided but `enrol.json` is a placeholder; PayCellUpgrade is red.
- **Next moves.**
  1. Fix PayCellUpgrade.
  2. S7 config (address, 50 DREGG/week, age backups).
  3. Devnet rehearsal on recorded RPC.
  4. Turn on self-enrollment only after tenancy plus refusal charging (R2-1).

**7. Product and public node.**
- **Truth.**
  - The node runs 5688775a with no friends enrolled.
  - The packager and the strict composed gate are on main.
  - `jdeploy3` exists only in dregg-infra on `hbox:/srv/git`.
  - The smoke gate is red on apps, residents and protected docs.
  - "Two friends + Hermes" has never run anywhere.
- **Next moves.**
  1. Push dregg-infra (split tenancy, jdeploy3).
  2. Build DEPLOY-3 from post-cut main.
  3. Run jdeploy3 green, or ship with the red rows named.
  4. Ember names friend #1.
  5. Make FRIENDS.md match the shipped candidate.

**8. Security residuals.**
- **Truth.**
  - Tenancy step A is in code, not deployed.
  - `--operation-record`, the grain journal, torn tail, loop-mount, rate limiter and hex are fixed.
  - Open: refusal charging, ticket expiry/wedge (uncommitted, NO TASK), consent shipping, `sourceGate` defaulting to accept-all (`01a105a2-bbeb`), unsalted world root.
- **Next moves.**
  1. Consent binaries plus FRIENDS env vars.
  2. Refusal-fee lane.
  3. Tickets: notAfter, tombstone and 8→2.
  4. Split tenancy on the box.
  5. sourceGate default.

### Contradictions that need a decision

1. **Two constant-rate stacks.** CHANNELS (Lean epoch records) and the PQ cohort mix (Rust, registrar-trusting) share no code. Keep one.
2. **Three KEM suites.** Channels use X25519, traffic uses pure ML-KEM-768, and rooms are moving to an X25519+ML-KEM hybrid. Agreement signs with ML-DSA while SURPASS deferred PQ.
3. **Where a program lives.** DEOS says "law + runner, never code in the cell; cards are data". EVENTS and BIGDREGG make Objective Bend activities the deos scripting language.
4. **Multi-machine model.**
   - SURPASS and CHANNELS: a witnessed single sequencer (ember-resolved `01a0f711-ffd8`).
   - The built line: an n=3f+1 Simplex on the `DataIntent` side, which T4 would delete.
   - ARCHITECTURAL-ARGUMENT: scoped joint turns with a designated last signer.
5. **Tenancy vs go-live.** Split tenancy refuses `discord.env` and `provider-service.json`, while the product plan turns on Discord and pool Hermes. Sequence them or lift the refusal.
6. **Authority roots for rooms.** Rooms use out-of-band founder pins, while the joint/agreement path aims at chain-rooted authority. Decide whether rooms re-root once a multi-validator exists.
7. **What Oct 13 means.**
   - BIGDREGG/ALTERNATIVES: traffic privacy plus agreement as release conditions.
   - THE BAR `01a0f9c0`: two friends plus Hermes.
   - Scout F: honestly labelled demos.
8. **Greenfield vs carries.** `LegacyContentCarry` and the v3 carries in rooms and payments contradict CLAUDE.md's "refuse, don't reinterpret".
9. **Executor.** Lean `runBounded` as specification vs the C machine as admission executor.

### Where documents claim what main contradicts

- GENERIC-SIMPLEX-NATIVE: "first signed source action pending" (two are installed).
- TRAFFIC-P1: points at two-host/new-effect runs (none exist).
- FRIENDS.md: rooms/chat/private rooms/Hermes are described, but the node lacks them; proxy steps omit consent env vars; web "read-only" (it takes POST).
- README: SPK "integrated (recovery)" (main's receiver is absent); Studio "executed" (lane binaries).
- Law-composition and world-methods notes: "uncompiled/unswitched" (both are imported by the kernel).
- CONSTRUCTION-PROOF-CONTRACTS: BendTT machine as live (orphaned, slated for deletion).
- BIGDREGG addendum: BendTT Books as evidence.
- SDK-DESIGN: `Theory/Contracts` (it is `Kernel/Contracts`).
- INTERFACES.md: predates `package.py`.
- DISCORD-ENTRANCE, Scout D, R2-1, Scout G: defects now fixed on main.
- DEOS: five namespaces, deleted decoders, a Lean search index, "§8".
- SURPASS: 33 constructors, finality export, no CI, no SDK, Ed25519-only.
- CHANNELS: ChannelFrame/DCW2/CH-OMIT/fn portals "landed" (none are on main).
- TENANCY-DESIGN: cited by a commit but tracked nowhere.
