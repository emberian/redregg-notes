# TASK BACKLOG, 2026-10-04 (lane S5, backlog hygiene)

Source: `cv task list --all --json` at ~02:10 EDT, 585 tasks, 459 non-terminal. Landed evidence: `git -C /Users/ember/workbox/mini-unified-push-20261003` HEAD e598326e (lane tips tested with `merge-base --is-ancestor`, files with `git grep` on HEAD), the swarm ledger and the Codex lane-mining file. Nothing was closed or abandoned. Ids below are the 13-character prefix (`cv task show` accepts it).

## 1. Counts

| class | count | what was done |
|---|---|---|
| LIVE | 231 | open work, tagged with a successor lane (all of them, not only swarm-tagged) |
| LANDED-VERIFY | 74 | work is on main; tagged `landed-verify` with the commit in a note; root to close (9 of these are July cv tasks whose revision cv itself observed as landed) |
| EMBER | 12 | tagged `ember`; also carry a successor tag where the work is Claude's after the decision |
| DUPLICATE | 6 | `cv task supersede` toward the better task |
| OTHER PROJECT | 136 | not Mini/Bread: 128 DoN closure/crossplay/oracle tasks (repo `don`), cv, phoenix-strip, tokeman. Untouched except dead claims |
| total | 459 | |

STALE-CLAIM: 74 claims held by lanes that no longer exist were released with the note "claim released: owner lane ended; see SWARM-LEDGER-20261004" (56 of them LANDED, 13 still LIVE, 2 EMBER, 3 other-project). One claim was left: 01a1056c-c498 is held by `claude-followups`, opened 35 minutes before this pass, so treated as a live lane.

Swarm-20261004 tasks: 69 = 65 LIVE, 2 LANDED-VERIFY, 2 EMBER. The two swarm tasks that landed: 01a104fe-95c2 (SDK Linux control) and 01a10505-9a79 (DurableReceiverIO:1091).

Priority key: P1 = blocks the 10-13 bar, a flag day, a known hole or the next landing; P2 = needed soon; P3 = backlog. `[sw]` marks swarm-20261004 tasks. Ties are ordered by id.

## 2. LIVE by successor lane

### native (29)

- P1 `01a0f87d-02f7` T4 HOST-CUTOVER (FD-1): submit = World.admit — after the stage-2 candidate; stage 0 is proved. T4 HOST-CUTOVER (FD-1): submit = World.admit
- P1 `01a1056f-0066` [sw] Kernel: deliver responses to a yielded Objective activity and store its checkpoint (the resident as a guarded fixed point across turns). kernel delivery of responses to a yielded activity + checkpoint storage
- P2 `01a0f53f-f848` PRIVATE-TRANSFER-DEAD: MCP private_transfer cannot commit (fee 0; fake Pedersen) - fix or delete. MCP private_transfer cannot commit; greenfield: delete it
- P2 `01a0f6b0-ed49` SURPASS.md: the takeover table + lanes; the start-today set. SURPASS tracker: stage 0 done, FD-1 host cutover (T4) is the next big lane
- P2 `01a0f6db-c4fb` LAW-SURFACE: delegation/revocation/install/birth project no state or clock slots; an unguarded positive state clause makes a resource's law irreplacea. LAW-SURFACE: an unguarded state clause makes a law irreplaceable
- P2 `01a0f712-3bb7` RENAME Scope.maxCost -> perRequestBytes (authority wire codec bump; batch with FD-1). rename Scope.maxCost -> perRequestBytes (greenfield codec bump)
- P2 `01a0f740-26c5` T3: capability + key epoch decided by World.admit as pinned footprint reads, not carried data. T3: capability + key epoch decided by World.admit
- P2 `01a0f856-149c` grain-runtime workspace_create has no fields: an agent-born declared cell declares none (K-FIELD-CLOSURE follow-up). grain-runtime workspace_create declares no fields
- P2 `01a0f87d-0310` FIELDS-SWEEP: every creator of declared cells passes its field list (after k-closure merges with the product branches). FIELDS-SWEEP: every cell creator passes its field list
- P2 `01a0f910-d000` PAY x K-PREROTATE: the self-enrolment memo should commit a next key (self-enrolled subjects cannot rotate today). self-enrolment memo should commit a next key
- P2 `01a0fadb-65d6` K-FIELDS-OBSERVE finish: journeys, ledger, measurement, tree vector for 1b44ecdb. K-FIELDS-OBSERVE finish (branch 1b44ecdb is not on main)
- P2 `01a104fd-9132` [sw] Add execution_source_semantics to Kernel/ObjectiveBendPreparedOutput and build that closure. execution_source_semantics into PreparedOutput; needs an hbox build
- P3 `01a0f6d0-e072` PAY kernel: self-enrollment throughput is one decision per tip (journal-floor spam can delay enrollments). self-enrollment throughput is one decision per tip
- P3 `01a0f701-0e4f` HERMES-TARIFF-2: the kernel recomputes the metered provider charge at settle (not just bounds it). HERMES-TARIFF-2: kernel recomputes the metered charge at settle
- P3 `01a0f701-0e6d` HERMES-TARIFF-3: detect Host-tariff drift against a provider purse's birth-time fees before reserve. HERMES-TARIFF-3: detect Host tariff drift before reserve
- P3 `01a0f72b-7dae` VERBNAME-PLACE: the Host renders request/verb 7 and 10 as append and place. Host renders request/verb 7 and 10 as append and place
- P3 `01a0f740-26b0` T1 follow-up: a turn that CREDITS the meter (allowance refill), conserved against a Book. a turn that credits the meter, conserved against a Book
- P3 `01a0f740-26e4` T5: define stage-F History.legBytes = canonical write bytes of a leg (charge_is_patch_bytes at the codec). T5: stage-F History.legBytes
- P3 `01a0f759-053c` HOST-SELVAGE-CUT: the last 12 Selvage modules in the deployed Host closure (digest backend types). HOST-SELVAGE-CUT: 12 Selvage modules left in the Host closure
- P3 `01a0f798-a0c5` C14 integration: tag 13, ops 130-133, refusal tag 12, STORE-CELLS/v6, GENESIS-SOURCE/v3 collision check. C14 integration: tag/op/schema collision check
- P3 `01a0f798-a0d8` C14 follow-up: prepare-stage tail-bound refusal; name tail-bound on grain birth. prepare-stage tail-bound refusal
- P3 `01a0f7f1-b6b7` NODE: the emitted game descriptors are computed at every boot (~6 s of the 7.6 s left after #86). emitted game descriptors computed at every boot (~6 s)
- P3 `01a0f81a-386d` SEALED-MARKET deposit: bid deposits as held Book accounts (generalize C3's receiver), refund at reveal, forfeit to the well. sealed-market bid deposits as held Book accounts
- P3 `01a0f890-b950` LEAN: finish moving the PoA laboratories out of 11 runtime modules (private structures block the mechanical move). PoA laboratories out of 11 runtime modules (breadstuffs)
- P3 `01a0f99e-9919` FAREOO: K-CARRY — every flag day ships a Lean-checked linear carry; re-genesis keeps by theorem, drops by name. K-CARRY: ember said teardown/rebuild; obsolete as prerequisite, root close candidate
- P3 `01a0f99e-bbea` FAREOO: K-KIND-CELL — kinds, templates and name maps as prototype cells; create --from K; no rebuild per kind. K-KIND-CELL: create --from exists; prototype cells beyond the ROM table open
- P3 `01a0fa12-caa6` POA: Galley rules_digest hashes the runtime's source FILE — every neutral edit re-signs the world. Galley rules_digest hashes the source FILE (breadstuffs)
- P3 `01a0fc34-8ba2` FAREOO: member-authored prototype and program composition with shared self/super. member-authored prototype/program composition with shared self/super
- P3 `01a10556-4a0b` [sw] MINE: ObjectiveNatural residual; Studio definition/publication (r26); Objective world acceptance probes; NativeJointSourceDiagnostics; Surface adapter. MINE: ObjectiveNatural, Studio publication, world probes, diagnostics, adapters, share-issuer v3

### agreement (4)

- P1 `01a10539-ae49` [sw] Agreement: journal decoder recurses once per entry → stack overflow on reopening a long journal; fix before any cutover. journal decoder stack overflow on a long journal; fix before cutover
- P1 `01a10539-ae89` [sw] Agreement: rebase the W1.7 commits (bde7fab2..2e74773c) onto main past the audit lane's D16 harness changes; then fix C + pure-kernel stall test + CUT. rebase W1.7 onto main past D16, then fix C and CUTOVER.md
- P2 `01a0f798-a0af` C14 follow-up: certified becomes the witness quorum's (N1) - QC replaces the operator capability in CertifyReceiver. certified becomes the witness quorum's (N1 consensus rebase)
- P2 `01a10539-aeca` [sw] Agreement: find the ~20 s per-iteration cost (p50 23 s round trip) with the committed timing logs. ~20 s per iteration, p50 23 s round trip

### spk (15)

- P1 `01a10500-f1d1` [sw] SPK: resident unit names must carry a store/deployment id (K-SPK defect) so scratch worlds can run apps beside live ones. unit names need a store/deployment id (scratch beside live)
- P1 `01a10500-f26d` [sw] SPK v4: replay must add the v4 completion to created/running lists (STOP of retried g4 / continue-START g5 currently refuse, fail-closed). v4 replay: STOP of retried g4 / continue-START g5 refuse
- P1 `01a10500-f341` [sw] Land + compile the W2.F SPK v4 commits after the cut (they touch NativeHostReplay and Host/Main). land and compile W2.F SPK v4 commits after the cut
- P1 `01a10556-492a` [sw] MINE: land the SPK failed-START recovery the live r2 world ran (runtime-spk-recovery-r2.tar + budget family); main still says receiver absent. MINE: SPK failed-START recovery the live r2 world ran; main says receiver absent
- P2 `01a0f616-5133` SPK-DISPATCH-FEE: a dispatch debits the payer account in the same turn; empty account refused. SPK dispatch must debit the payer (ember: ratelimit vigorously)
- P2 `01a0f63f-c22b` K-SPK-2: deployment8 in the unit name, export/import receipt binding, retire edge, onward sharing, restart-surviving sessions. K-SPK-2: deployment8 in unit name, export/import binding, retire edge
- P2 `01a0fb2e-f6c7` SPK-WS-REVOKE: live stream authority after session or grant revocation. SPK-WS-REVOKE: live stream authority after revocation
- P2 `01a10500-f2bc` [sw] SPK v4: resident refuses after restart instead of calling the lookup ops. resident refuses after restart instead of calling lookup ops
- P3 `01a0f52e-778d` SPK later: powerbox, WebSockets, upgrade, API tokens, export, wildcard cert. SPK later items (powerbox, upgrade, lifecycle); WebSockets already done
- P3 `01a0f84c-96fe` SPK-RESIDENT-MEM: the resident's START-time SPK re-parse is charged to the grain's class (Davros: resident 1079 MiB, app 53 MiB). resident START re-parse charged to the grain class
- P3 `01a0f84c-ec80` SPK-POWERBOX-APPS: market apps blocked on identity caps, app hooks, HackSession, powerbox HTTP (measured list). powerbox apps blocked on identity caps/hooks
- P3 `01a0fa13-a3c6` SPK-WS-CLOSE: a grain STOP closes WebSockets with a close frame, not EOF. STOP closes WebSockets with a close frame
- P3 `01a0fa13-a3e1` SPK-WS-LEAN-CLASS: WebSocket caps move into the Lean size class with K-SPK. WebSocket caps into the Lean size class
- P3 `01a0fc44-0146` SPK-MINI-DOCUMENT: delegated EtherCalc export into Mini content. SPK-MINI-DOCUMENT connector
- P3 `01a10500-f228` [sw] SPK: unprivileged broker and resident bootstrap (today both require root by code). unprivileged broker (tenancy step B territory)

### audit (16)

- P1 `01a0f6c5-687d` REFUSAL-UNIFORM: every public submit op refuses uniformly; theorem over the op table. every public submit op must refuse uniformly; theorem over the op table
- P1 `01a0f6c5-6891` LIVE-EQUALS-REPLAY: one admission function for submit and audit; the asymmetry list before the Turn cutover. live = replay: one admission function; 22-row asymmetry list
- P1 `01a0f972-8393` Durable log: truncation after the last checkpoint is undetected. durable log truncation after last checkpoint is undetected
- P1 `01a0fa73-e626` AUDIT-SUPERLINEAR: cold mini audit grows ~3.4x per 2x records (372 s at 1004, 1272 s at 2004); profile the walk. cold audit superlinear: 372 s at 1004 records, 1272 s at 2004
- P2 `01a0f674-fa46` PAY: blind the observer channel's pre-signature refusals (ops 110/119) and move P4's wait logic onto the public view. blind pre-signature refusals on ops 110/119
- P2 `01a0f7cd-a195` K-NARROW-HIDE audit: the world root commits unsalted to every unblinded cell (Book balances included). world root commits unsalted to every unblinded cell
- P2 `01a0f888-1b57` TAIL-FIELDS: stream tail ignores Scope.fields (a grant without body still tails entries). stream tail ignores Scope.fields
- P2 `01a0fa66-8ea8` EXISTENCE-ENROLLED: an enrolled key with no grant still learns whether a cell or account id exists (challenge undisclosed vs query no-grant). enrolled key with no grant still learns existence
- P2 `01a0fadb-6617` Bind the per-address view root to the signed challenge; restate root binding over the tree. bind per-address view root to the signed challenge
- P3 `01a0f63a-2348` HYGIENE: 4 bare #print axioms in Kernel/NativeHost.lean (b25e9f8b) — proof-hygiene red on final. bare #print axioms in NativeHost; now #guard_msgs form, verify check-proof-hygiene
- P3 `01a0f6d8-0101` Name the old-key refusal after rotation (today: bad-signature). name the old-key refusal after rotation
- P3 `01a0f6d8-0110` JROT: exercise exact rotation replay (op 142 replay, op 143 lookup). JROT: exercise exact rotation replay (ops 142/143)
- P3 `01a0f78f-288b` C1 follow-up: install refusal on a job cell is undisclosed (explain cannot name clause 0); revoke judged by the job law is unverified. job law install refusal undisclosed; revoke judged by the job law unverified
- P3 `01a0f7cd-e8fd` K-NARROW-HIDE audit: is a quoted atom's revision handle a confirmable commitment to the source payload?. is a quoted atom's revision a confirmable commitment
- P3 `01a0f8c4-6c88` K-LAW-LEAF for installPolicy: a re-law refused by the cell's law reads 'undisclosed'. re-law refused by the cell's law reads undisclosed
- P3 `01a0fc50-4f28` K-LAW diagnostics: authenticated ancestor attribution and closure correction. K-LAW diagnostics: authenticated ancestor attribution

### schema (9)

- P1 `01a0f63a-233a` STORE-OPEN: Store open is O(history) — full-log chain + checkpoint MAC + root-tree rebuild on every restart. Store open is O(history); W1.11 indexed session/root work is the fix
- P1 `01a0fa24-0469` A write to a 1000-entry cell takes about 400 s on the spec-Keccak Host (31x entries, about 100x time vs 32). 1000-entry cell write takes ~400 s (spec-Keccak Host)
- P1 `01a0fadb-6602` Store tree cost: full-read view size and per-write root cost (seed for full readers, cached cell tree). Store tree cost: full-read view size and per-write root cost
- P2 `01a0f612-7ab3` LinkIndex: incremental reverse map + kind-tag prefilter before decode. LinkIndex.admit recomputes invert(sources) per record
- P2 `01a0f7da-60bf` ROOM-TAIL VIEW: tail is 1+K signed reads; 200 entries / 5 streams = 12 s at load 35. room tail is 1+K signed reads; 12 s at 200 entries
- P2 `01a0f8a2-9e57` SESSION-ADOPT: the Host re-replays its own just-committed record. Host re-replays its own just-committed record
- P2 `01a0f8e3-c7c0` Host codec cost after HOST-KECCAK: ByteArray stream builder, sort-key precompute, fast nat decode. Host codec cost after HOST-KECCAK
- P2 `01a0fa51-4c0a` WORLD-ROOT-COMPRESSED: compressed sparse world root (design; the cheaper open-builds-the-cache-once step first). compressed sparse world root (design)
- P3 `01a0f60e-2dcf` doc history cost: O(rows x log) prefix replays. doc history is O(rows x log) prefix replays

### shipfix (3)

- P1 `01a10556-49cd` [sw] MINE: receipt-confirmed client consent (NativeReceiptConsent, ClientConsentCore, confirmed-receipts.patch, receipt-rust-r1). MINE: receipt-confirmed client consent
- P2 `01a0f838-d1e1` mini serve: no fairness between public clients; per-op body bounds and per-peer queues. mini serve: per-op body bounds and per-peer queues
- P2 `01a10510-6e02` [sw] grain-runtime: fix stale test paused_parent_next_generation_policy_includes_three_fixed_workers (mock expects compact view:policy; fixture lacks canon. stale paused_parent test (the one red rust-tests row)

### deploy (13)

- P1 `01a0f52e-7711` DEPLOY-3: one batched box deploy of everything landed since 5688775a. DEPLOY-3 candidate not built; W1.12 packager and gate exist, successor builds on the warm base
- P1 `01a0f5fd-648b` DEPLOY-3 first box run: check what the sandbox could not. DEPLOY-3 first-box checklist the sandbox could not run
- P1 `01a0f6d0-e063` DEPLOY-4: operator socket + tick env for self-enrollment; FRIENDS.md infra copy. operator socket + tick env for self-enrollment on the deployed box
- P1 `01a0f9c0-521b` THE BAR 10-13: two friends + hosted Hermes, joined, on the public node; 1000 records: write <= 5 s, cold reopen <= 60 s. THE BAR 2026-10-13 tracker (write<=5 s, cold reopen<=60 s at 1000 records)
- P1 `01a0f9c0-55af` M1 (intermediate): one friend's first hour on the public node, on the first merged candidate. M1 milestone: one friend's first hour on the public node
- P2 `01a0f6d0-e044` JOIN-SOLANA: the enrollment price should come from the Host (priceIn), not a client formula. JOIN-SOLANA price should come from the Host
- P2 `01a0f6d0-e055` JOIN-SOLANA x local-client: join over --remote, the friend bundle (pay-view.bin), proxy refusal text. join over --remote and the friend bundle
- P2 `01a0f6d8-00de` dregg-infra mini-reenroll/OPERATOR: copy the friend's NEXT public key beside the custody copy (K-PREROTATE flag day). copy the friend's next public key beside custody (K-PREROTATE flag day)
- P2 `01a0f830-42e7` CANDIDATE: grain-runtime is not reproducible across two candidate builds. grain-runtime not reproducible across two candidate builds
- P2 `01a0fb03-bc64` HERMES-LIVE: one useful real-provider resident through the room and durable worker paths. HERMES-LIVE: one real-provider resident through room and durable worker
- P2 `01a0fbc7-a94c` Member BYOK: authenticated remote custody, route choice and fresh Hermes provisioning. member BYOK entry; integration reopened by root
- P2 `01a0fc5d-4eba` HERMES-SUMMON-DISPATCH: authenticated member outbox to registered resident inbox service. HERMES-SUMMON-DISPATCH: member outbox to resident inbox service
- P3 `01a0fb11-e4db` HOMELAB-INFERENCE: model-aware allocation and fair scheduling across Pug heterogeneous hosts. HOMELAB-INFERENCE scheduler (a slot-free fix landed 0c148911)

### language (11)

- P1 `01a10500-6e65` [sw] Make the Lean elaborator THE implementation: preview and publication call Compiler/ObjectiveBendElaborate; delete the TS elaborator; port the parser (. make the Lean elaborator THE implementation; delete the TS elaborator
- P1 `01a10500-6eef` [sw] Re-emit every captured package and parser/elaborator pin after the parser change (PIN_PARSER in objective-source-package.ts; preview/definition toolin. re-emit captured packages and parser/elaborator pins; old captures refuse to load
- P1 `01a10500-6f2f` [sw] Put the front-end checks (elaborate-tests, c4-tests, check-parser, check-preview, TV) and Compiler.ObjectiveBendElaborate into gates. front-end checks are in no gate
- P2 `01a10500-6f6f` [sw] Objective Bend: check  at compose/fix and discharge final-self assumptions; laws as checked evidence. check at compose/fix; laws as checked evidence
- P2 `01a10505-4694` [sw] Core4 sums: open-tail default arm for case over an open variant row. open-tail default arm for case over an open variant row
- P2 `01a10556-496e` [sw] MINE: Objective laws (ObjectiveBendLaw{Interfaces,Checking}; check-law-r15 PASS) — port to sums, audit statements. MINE: Objective laws (audit statements first)
- P2 `01a10564-84a1` [sw] Sums.total refused by the type checker though the machine runs it. Sums.total refused by checker though the machine runs it
- P3 `01a104f3-e3b5` [sw] Port the surviving Bend-surface domain sources to .obend (station SharedConsequences/EngineeringStation; collective MarketMath, CollectiveAdoption, Si. port surviving Bend-surface domain sources to .obend (sums landed)
- P3 `01a10505-4708` [sw] Front end: .variant arm in the TS preview template; Sums.obend into the preview cohort. TS preview .variant arm; Sums.obend into the cohort
- P3 `01a1056f-0083` [sw] Objective activities: within-turn non-divergence check for residents; general well-typedness of decoded response data; checker-level named refusal mes. within-turn non-divergence, decoded-response typing, named refusals
- P3 `01a1056f-00a4` [sw] Objective activities: collect the heap at a yield (checkpoint grows ~120 tokens per turn in EventCounter.serve); recursive Plan/response data; before/. heap collection at yield, recursive plans, before/after

### proofs (31)

- P1 `01a10505-46cf` [sw] Audit the pre-existing canonical-shadowing shareability hole in Core4 typing. canonical-shadowing shareability hole in Core4 typing
- P2 `01a0f802-02f0` hypothesis-ledger: 70 open assumptions carry no named satisfying+refuting instance pair (TOOTHLESS ratchet). 70 open assumptions without satisfying+refuting pair
- P2 `01a0f8df-cdbc` AxiomCensus: pin the native_decide count and names (today it only reports). AxiomCensus pins the native_decide count (count now 49)
- P2 `01a0f988-ddf6` LEDGER: the tier test must be structural, never prose (a comment edit disarmed it). ledger tier test must be structural, not prose
- P2 `01a0fa5c-4a1a` VERB-TAGS: prove request-verb tags unique across kinds (the tickClock/appendObject collision class). request-verb tags unique across kinds
- P2 `01a104fd-9092` [sw] Prove DeepEvaluates deterministic (Core4 deep Data uniqueness). DeepEvaluates determinism: Data means a deep evaluation, not the unique one
- P2 `01a10503-6c57` [sw] Finish Kernel/AgreementEvidenceRegime.lean (COMMIT certificate typed as witness-for-ordering, never authorization), add the new Theory modules to the . finish AgreementEvidenceRegime (COMMIT cert as ordering witness)
- P2 `01a10503-6cb7` [sw] HypothesisLedger: mark a Prop REFUTED when refuted for ANY field, not only for every field. ledger must mark REFUTED when refuted for ANY field
- P3 `01a0f52e-773a` B9b: token verification in Lean. b9 token verification in Lean; heavy hbox lane
- P3 `01a0f611-ea87` K-TRANSCLUDE follow-up: endpoint-death replacement vs Theory DeathContext. endpoint-death replacement vs Theory.DeathContext
- P3 `01a0f627-49fd` P-AFFORDANCES follow-up: storage-irrelevance for the plan half (prepareAuthorizedLoaded). storage-irrelevance for the plan half
- P3 `01a0f627-4a0b` P-AFFORDANCES follow-up: end-to-end dry-run ⇔ submission theorem. end-to-end dry-run <=> submission theorem
- P3 `01a0f64e-c650` SheetLaw: bal/eq_raise_needs_clock and alive-constant-without-clock history theorem. SheetLaw eq_raise_needs_clock theorems
- P3 `01a0f65d-f8bb` Theory CreatePayload.rootBody: a second root shape beside the kernel's empty-container root. Theory CreatePayload.rootBody second root shape
- P3 `01a0f65d-f8c6` clearOf completeness: an acyclic splice is never refused cycle. clearOf completeness
- P3 `01a0f6ad-8d64` K-RUNS-RANGES: one mark projection for range and line anchors. one mark projection for range and line anchors
- P3 `01a0f6ae-5e6c` ZK.md: research + safe-now lanes; the admission bar for a proof carrier. ZK research tracker; ZK-TRUTH findings from the swarm feed it
- P3 `01a0f6e3-bc50` K-INSPECT: law_print_parse at the string level (a Lean lexer; retire the Rust law grammar twin). law_print_parse at the string level
- P3 `01a0f740-26d5` T9: step_conserves at the deployed Book layout (CanonicalResourceKernel), not the census Book. T9: step_conserves at the deployed Book layout
- P3 `01a0f76c-fddd` C-SAT scale: lazy DNF search + certificate trees (independent disjunctions exceed dnfCap at 11 clauses). C-SAT scale: lazy DNF + certificate trees
- P3 `01a0f796-1806` C4xC3: restate griefing_cost_bounded over the real truth-turn fee leg. C4xC3: restate griefing_cost_bounded over the real truth-turn fee leg
- P3 `01a0f796-1815` C3: bridge escrow_conserved_log's non-money edge premise from law slots to stores. C3: bridge escrow_conserved_log's edge premise to stores
- P3 `01a0f796-1823` C3: prove the money slot is receiver-private and the held account uncapturable. C3: money slot receiver-private; held account uncapturable
- P3 `01a0f7e0-b8a2` C-SAT-2 follow-up: prove the declared scalar step is Shaped scalarView; can --any beyond one field. C-SAT-2: Shaped scalarView proof; can --any beyond one field
- P3 `01a0f802-0329` hypothesis-ledger: PolishchukSpielman, HaboeckTheorem2, HaboeckErrorEnvelope are OPEN with no instance either way. Haboeck hypotheses open both ways (PolishchukSpielman part landed d16c20db)
- P3 `01a0f802-033d` hypothesis-ledger: FactoredProverHonest is a closed Prop bound as a premise, neither proved nor refuted. FactoredProverHonest closed Prop as premise
- P3 `01a0f823-fea4` PRIV-ROOMS-LAW-LINK: tie law.keys.json to Kernel/PrivateRoomKeys.keysLaw by theorem. tie law.keys.json to keysLaw by theorem
- P3 `01a0f856-14ae` Lift K-FIELD-CLOSURE from prepareCell to AcceptedInvocation (CheckedLeg-style theorem). lift K-FIELD-CLOSURE to AcceptedInvocation
- P3 `01a0f867-5725` castInjOn should cover only the law's mentioned slots (compiled law refuses beyond R where eval admits). castInjOn should cover only mentioned slots
- P3 `01a10500-6ea2` [sw] Prove OrderedPresentationInvariant in Lean (Compiler/ObjectiveBendC4.lean). OrderedPresentationInvariant is only a Prop
- P3 `01a10501-8293` [sw] Finish Theory/CertF.lean (needs Mathlib DotProduct olean on hbox) and Kernel/GenericSimplexReconfig.lean (minor simp/parse fixes). finish CertF and GenericSimplexReconfig

### backends (16)

- P1 `01a10564-845b` [sw] DemandMachine: make stepRaw linear in the heap (unique array writes; no retained previous state for the capacity check; cached stack length) with the . Lean stepRaw 20-39 s vs C 13-23 ms; admission re-execution runs the slow one
- P2 `01a0f6dd-ed7b` COMPUTE.md: schedule, price, verify, settle — the start-today lanes and the J-JOB floor. COMPUTE.md tracker (J-JOB floor landed)
- P2 `01a0f70c-db62` EVAL.md: evaluator-agnostic kernel; the second evaluator; cost in types; the start-today lanes. EVAL.md tracker (E1/C-SAT/G-NORM landed; NC and MINK remain)
- P2 `01a0f96d-f323` ABI: admit noun+max (max bounds the atom; a cell is refused by name) — ember's decision. ABI: admit noun+max (ember decided)
- P2 `01a0f96d-f34c` NOCK-FEE: runs paid per step from the runner's account with a daily free allowance — ember's decision. NOCK-FEE built on branch nock-fee c02be4a3, not on main; land it
- P2 `01a10556-498e` [sw] MINE: oblivious demand-machine backend + ObjectiveActivity (~22 modules scoped PASS beyond the cut's 11). MINE: oblivious demand backend + ObjectiveActivity
- P2 `01a10564-8480` [sw] C backend: refinement theorem C ≡ stepRaw (today shown by the 224-case differential); wire the differential harness as a gate. C refinement theorem + differential harness as a gate
- P2 `01a1056c-c498` [sw] C backend: port perform/done/yielded/sharedEffect/resume (EmitC no longer compiles after events). CLAIMED by claude-followups (35 min old); EmitC port to events
- P3 `01a0f52e-7730` NOCK carriers: attestation/bond, Avon witness consumer; three small proof items. NOCK carriers: attestation/bond/Avon witness consumer; waits on Sigilante answers
- P3 `01a0f5f8-8d9b` NOCK-MINK-JET: proven mink jet so wrapped NockApp kernels can run as doors. proven mink jet so NockApp kernels run as doors
- P3 `01a0f75a-3d5a` MUD clause 34 to ran PROGRAM; a ran clause in the shell law grammar. MUD clause 34 to ran PROGRAM
- P3 `01a0f82f-572b` K-EVAL: live evaluator disable (system-cell transition) in place of the genesis-time profile list. live evaluator disable
- P3 `01a0f8a2-9e3d` HELD-PROGRAMS: a stored Nock program is hashed and cued on every run. stored Nock program hashed and cued on every run
- P3 `01a0fad6-6713` MINK-JET-2: the +mink jet as a new evaluator (nock+mink); prove MinkJetClaim before admission. MINK-JET-2
- P3 `01a0fad6-6732` MINK-JET-3: the +keep door journey, interpreted now and under nock+mink after lane 2. MINK-JET-3
- P3 `01a10564-84c3` [sw] One code table and one State byte format shared by the C backend and the oblivious network (which lacks sums and run-time fix/mix code). one code table and State byte format for C and oblivious backends

### traffic (9)

- P1 `01a10501-830d` [sw] Traffic: Linux qualification of roster enrollment (eebcdc8e), baseline v12 on a scratch world, single-host run, two-host v13, first new effect. Linux qualification of roster enrollment, v12/v13, first new effect
- P2 `01a10510-6e60` [sw] cohort: restore a test that a stranger cannot tie up the cohort listener (deleted by d7b2f19b roster enrollment). restore the stranger-cannot-tie-up-listener test
- P3 `01a0f6e9-bba8` CHANNELS.md: constant-rate ordered broadcast domains — the simulator first, then the start-today lanes. CHANNELS tracker; CH-OMIT delivered, rest are follow-ups
- P3 `01a0f6fc-7372` channel-sim follow-ups: T5 trace test, shuffle cost, real churn trace, buddy sweep, cell packing, w-relay in T3 engine. channel-sim follow-ups; (a) closed, rest open
- P3 `01a0f7a6-6902` CH-EPOCH follow-ups: @[export] seal/opening/commit for CH-RELAY-1; admitAppend preserves ChannelStoreLaw. CH-EPOCH follow-up 2: admitAppend preserves ChannelStoreLaw (item 1 done)
- P3 `01a0f81d-695a` CH-RELAY: relay deadline misses are scheduling - RT priority or CPU reservation for mini relay, measured on the public class. relay deadline misses: RT priority/CPU reservation
- P3 `01a0f89a-d139` Channel member: bind the published epoch record to the Store payloadDigest (light export + Audit theorem). bind published epoch record to Store payloadDigest
- P3 `01a0f89a-d173` Channel member: persist the send queue and per-recipient seq across join restarts. persist channel send queue across restarts
- P3 `01a10501-83a6` [sw] Traffic: enroll registrar↔operator MAC keys (still file-provisioned); separate uids for registrar and mailbox on hbox. registrar<->operator MAC keys still file-provisioned

### mpc (1)

- P1 `01a10556-494b` [sw] MINE: private committee v4 (14 modules compiled, native-linked; v4-validate-original-r6 refused transactionConflict). MINE: private committee v4

### fhe (3)

- P1 `01a10501-82d1` [sw] FHE: check worst-case fhe.rs key-switch noise against the 2^52.39 depth-2 ceiling (BfvLifetime). worst-case key-switch noise vs the 2^52.39 depth-2 ceiling
- P2 `01a10501-825a` [sw] Import the Bfv*/BfvLifetime/Transferability modules into Theory.lean/Compiler.lean targets; guarded axiom pins; Compiler/BfvNoiseJoin; docs/BREAD-PORT. import Bfv*/Transferability into the Theory/Compiler targets
- P2 `01a10556-49ad` [sw] MINE: FHE over Objective (r34 natural/owner.rs newer than main; r35 ReturnRelease; r36 authored). MINE: FHE over Objective

### tenancy (6)

- P1 `01a104f3-e258` [sw] Tenancy step B: mini-keys key-service account, per-friend mini-s-NAME accounts, mini-proxy; per-user sshd. step B (mini-keys, per-friend accounts, mini-proxy) blocks the first friend's key on the public box
- P1 `01a10556-49ec` [sw] MINE: protected head frontier (tenant-rollback refuter PASS) → tenancy step B. MINE: protected head frontier (rollback refuter)
- P2 `01a0fb03-bc7c` DURABLE-ANCHOR: local authenticated head and client receipt continuity. DURABLE-ANCHOR: local authenticated head + client receipt continuity
- P2 `01a104f3-e285` [sw] Discord bridge and provider-service under split tenancy. bridge and provider-service cannot install under split tenancy
- P2 `01a104f3-e2a8` [sw] Run journeys J0-J8 and jroster under split tenancy on a scratch box. tenancy infra side never ran on a box; journeys under split tenancy
- P3 `01a104f3-e2cb` [sw] Arm the two-uid tenancy tests with a sudo-capable runner. two-uid row landed (NOT-ARMED); a sudo-capable runner is still missing

### rooms (39)

- P1 `01a0f99e-d668` PRIVATE ROOMS: the Discord mirror would re-publish opened text; hosted-subject rule must cover the bridge. Discord mirror would republish opened text from a private room
- P1 `01a104fd-8e73` [sw] Private rooms: end-to-end run on a real Host (found → invite → sync → seal → kick). private rooms never ran end-to-end on a real Host
- P2 `01a0f823-fe95` PRIV-ROOMS-DOC-EDIT: sealed doc edits in private rooms. sealed doc edits in private rooms (PRIVATE-DOCS lane carries it)
- P2 `01a0f96d-f360` DOCUVERSE follow-ups from ember's decisions: delete the event-log twin; all-standing-grants coverage for who/since. delete the event-log twin; all-standing-grants coverage
- P2 `01a0fadb-65ec` J-PRIV-1: per-wrap grants on the keys cell (CellField.atom) so a member reads only its own wrap. J-PRIV-1 per-wrap grants so a member reads only its own wrap
- P2 `01a0fb20-e84b` PRIVATE-DOCS: editable sealed documents on the element-tree docuverse. PRIVATE-DOCS: editable sealed documents; parts on main, rest open
- P2 `01a104f3-e2ed` [sw] Private rooms: PQ hybrid wraps (ML-KEM-768 + X25519, record v3). PQ hybrid wraps (ember prefers PQ/hybrid over MLS)
- P2 `01a104f3-e30f` [sw] Private rooms: founder-key transition (rotation of the pinned founder key). founder-key transition has no design yet
- P2 `01a104fd-9015` [sw] Arm the new private-rooms refusal tests in check-rust-tests.sh. arm the 8 new private-rooms refusal tests in rust-tests
- P3 `01a0f53e-f651` QUOTE-DISCLOSE: should a quote carry text to readers of only the quoting room? (ember) + the --disclose lane. quote --disclose lane; ember already chose reference-only for October
- P3 `01a0f5e0-5a67` DEOS.md: the docuverse/deos-in-Mini plan — floor lanes. DEOS floor-lane tracker; four floor lanes landed, residuals are separate tasks
- P3 `01a0f5ef-d692` WEB-ENTRANCE integration: remote workspace, spelled links, P-LAW refusal text. web: remote workspace still unserved; spelled links; P-LAW refusal text
- P3 `01a0f5ef-d6aa` WEB-ENTRANCE: per-page read cost and attempt-dir growth. web page read cost (backlink fold gone; attempt-dir growth remains)
- P3 `01a0f605-d8e8` K-ATOM-EDITOR: a line edit records no editor/height; stale-line refusal cannot name who. atom-editor record: K-DOC-HISTORY answers most of it; decide whether a kernel change remains
- P3 `01a0f611-ea6c` K-TRANSCLUDE follow-up: kernel run edits so appended lines are transcludable. kernel run edits so appended lines are transcludable
- P3 `01a0f611-ea93` K-TRANSCLUDE follow-up: read targets run the source law twice. read targets run the source law twice
- P3 `01a0f6ad-8d59` K-MARKS: unlink of a mark's link leaves a link mark whose link is dead. unlink of a mark's link leaves a dead link mark; decide refuse vs retire
- P3 `01a0f6e3-bc44` K-INSPECT follow-up: inspect doc-outline + doc-graph on the content line. inspect doc-outline + doc-graph
- P3 `01a0f70e-4a5f` P-DOC-RENDER follow-up: history in the one renderer (doc show --at H, doc history) at the k-doc-history merge. history in the one renderer (doc show --at, doc history)
- P3 `01a0f70e-4a83` P-DOC-RENDER follow-up: petnames for principals so an annotation author reads as a name. petnames for principals in the renderer
- P3 `01a0f72b-7d83` POLICY-EPOCH-ROTATE: expose a law's grant-generation rotation on the Host. expose a law's grant-generation rotation on the Host
- P3 `01a0f72b-7d95` ROOM-INVITE-PRIVATE: wire hosted_private_invite into room invite for --private rooms. wire hosted_private_invite into room invite
- P3 `01a0f7c7-67ab` Links and backlinks at a past height (the /at page shows none); doc-show reports its read height. links and backlinks at a past height
- P3 `01a0f7cd-a171` K-NARROW-HIDE: blind stream cells (narrowed stream reads are refused until then). K-NARROW-HIDE: blind stream cells
- P3 `01a0f7cd-a184` K-NARROW-HIDE: owner rotation of a cell's blinding (custody transfer, revocation, seed loss). K-NARROW-HIDE: owner rotation of a cell's blinding
- P3 `01a0f7cd-a1a7` K-NARROW-HIDE: client cross-check of displayed content entries against opened bytes. client cross-check of displayed entries against opened bytes
- P3 `01a0f80c-12b7` K-RESOURCE-LINK: LinkTarget.resource + view-resource names its storage. LinkTarget has no resource constructor
- P3 `01a0f814-b33e` K-RENOUNCE follow-up: Host-reported lineage of what a renounce ended. Host-reported lineage of what a renounce ended
- P3 `01a0f8c4-6ca3` K-BIRTH-LAW: the room birth gate cannot pin the law a placed cell is born with. room birth gate cannot pin the law a placed cell is born with
- P3 `01a0f8c4-6cbf` hermes/gm/grants.json names story cells P-STORY deleted. hermes/gm grants.json names deleted story cells
- P3 `01a0f99e-993f` FAREOO: K-INDEX-NAMES — ROOM/NAME resolves through the room index document; names as shared meeting points. K-INDEX-NAMES; strict JNAMES passed on a sealed binary, landing unverified
- P3 `01a0f99e-bc1a` FAREOO: K-INTERFACE — one cell, many readings: interface cells (name map + derived slots) a cell is shown through. K-INTERFACE interface cells
- P3 `01a0f9e4-0bee` K-HIDE-ROTATE follow-up: the owner needs its cell's write heights to derive ratcheted salts (delegate writes). K-HIDE-ROTATE follow-up: owner needs write heights for ratcheted salts
- P3 `01a0f9ee-5e19` mini web: serve /stream/NAME (k-stream) and remote workspaces. mini web: /stream/NAME and remote workspaces
- P3 `01a0fbd3-65db` Convert existing public documents to prospectively protected current content. convert public documents to prospectively protected content
- P3 `01a104f3-e331` [sw] Private rooms: freeze/withholding by a single server (availability limit). state the availability claim (single-server freeze/withholding)
- P3 `01a104fd-8ef8` [sw] Private rooms: first-time reader shown a consistent stale record (design §1 R2, §3(c)). named limit: first-time reader sees a consistent stale record
- P3 `01a104fd-8f66` [sw] Delete current_source.rs + current-source-helper CLI, or give it a consumer. delete current_source.rs (no consumer)
- P3 `01a104fd-8fc1` [sw] Retire the ResearchWip-only Lean RoomRelease* modules. delete the ResearchWip-only RoomRelease* modules

### sdk (13)

- P2 `01a0f52e-774e` PQ-WASM: reconcile @noble signing vs the hybrid refusal; bindings_lightclient traps. PQ-WASM: @noble signing vs the hybrid refusal; ember prefers PQ/hybrid
- P2 `01a0f6bb-c108` K-PQ-FLEET: fleet and participant keys are Ed25519-only; Bread fleets sign hybrid ML-DSA-65. fleet and participant keys are Ed25519 only; Bread fleets sign hybrid ML-DSA-65
- P2 `01a104fe-94a5` [sw] SDK: pin intent bytes to W2.A's Lean contract codec, delete the SDK's own encoder. pin SDK intent bytes to Theory/Contracts (landed 17a6489c..), delete the SDK encoder
- P2 `01a104fe-94fb` [sw] SDK: wrap consent op 227 (Objective) after W1.2 lands. wrap consent op 227 once native-b lands
- P2 `01a104fe-958e` [sw] SDK: implement the ssh:DEST operator route (today only a local Unix socket). ssh:DEST route for members off-box
- P3 `01a0f627-4a15` P-AFFORDANCES follow-up: transfer/install probes; readable control-capability records. can: transfer/install probes
- P3 `01a0f627-4a20` P-AFFORDANCES follow-up: can's delegate probe burns a local namespace id. can delegate probe burns a namespace id
- P3 `01a0f6bb-c11b` FLEET-REMOTE: fleet-sign over local-client's --remote; agents join from their own machine. fleet-sign over a remote transport
- P3 `01a0f6e3-bc5d` K-INSPECT: owner-side cap tree - issuer view of delegated children + control capability. owner-side cap tree
- P3 `01a0f6e3-bc69` K-INSPECT: why suggestions for delta/two-slot/whole-law, and inspect-of-inspect. why-suggestions for delta/two-slot laws
- P3 `01a0f7da-60ad` STALE-ROOT RE-SIGN: per-author streams still collide at the challenge (114 re-signs / 192 concurrent says). stale-root re-sign across per-author streams (retry loop landed in 349c1e58)
- P3 `01a104fe-953e` [sw] SDK: move app_document.rs onto the SDK (depends on W1.15's workspace.rs). app_document.rs onto the SDK
- P3 `01a10510-6e33` [sw] discord-entrance: durable_restart_* endpoint test race (restarted app starts while the first worker holds the custody lock); wait for delivery=confirm. discord durable_restart_* race (test, not code)

### docs (4)

- P2 `01a104f3-e35e` [sw] Review website/*.html against the rewritten README and OBJECTIVE-BEND.md. website is an Aug-10 snapshot naming a renamed proof system
- P3 `01a0f87b-93f6` BinaryTower.lean: FanPaarRecursion docs still say residual. BinaryTower docstrings still say residual
- P3 `01a104f3-e386` [sw] docs/JOURNEY.md and BEND-GENERAL-ZKVM-PATH cite paths outside the repo (claudesplosion, /Users/ember/workbox). docs cite paths outside the repo
- P3 `01a10503-6cfb` [sw] docs: how governed-evolution installs are typed by ResearchRegime. document how governed-evolution installs are typed

### infra (8)

- P2 `01a0f5fd-649b` BREAD-EDGE leftovers from the DEPLOY-3 list: Chutes key for the narrator container; stale IPs in Caddyfile/headscale/portal/poa. Chutes key placement, stale IPs in Caddyfile/headscale/portal
- P2 `01a0f823-fe87` PRIV-ROOMS-INFRA: write /etc/mini/hosted-subjects on the node. write /etc/mini/hosted-subjects on the node
- P2 `01a10501-835d` [sw] hbox/persvati WiFi power-save off (or wired) before any cross-host latency claim. WiFi power-save off or wired before any cross-host latency claim
- P3 `01a0f52e-7744` B4-SEATBELT: run the MCP-confined probe on macOS once a Lean seed exists. Seatbelt probe on the Mac once a Lean seed exists
- P3 `01a0f533-b2cc` WARM-BASES: advance both box bases after each landing; mk-clone.sh that refuses a cold base. warm-base discipline: advance bases after each landing; mk-clone that refuses a cold base
- P3 `01a0f676-2673` PERSVATI-LEFTOVERS: orphan mini-grain-controller@7001 unit; cleanup checklist for lane batches. orphan mini-grain-controller@7001 unit on persvati
- P3 `01a0f829-a072` journey G and JPAY2 go red on a loaded box: G early-stops on a 3% write rise at load 40; JPAY2 hits the 3600 s hook timeout. journey G / JPAY2 red on a loaded box
- P3 `01a0fa12-ca92` LEAN-FFI: seed member-freshness gate cannot measure a deterministic seed (same class as linked_archive_freshness). lean-seed member-freshness gate cannot measure a deterministic seed

### root-owned, no lane tag (1)

- `01a0f52e-76a0` STANDING INTEGRATOR on final: merge landed branches continuously, fix the known collisions. ROOT-OWNED standing integrator role (codex:integrate-world is gone); root is the integrator now

## 3. EMBER (most blocking first)

1. `01a1052c-6e3a` DEPLOY-3 sponsor key custody: rotatable or not. Blocks building and shipping the DEPLOY-3 candidate (public box). Ledger 07:40: Option A accept (sponsor key never rotates) or Option B pre-rotation via `run.sh init --sponsor-key`. 01a0f6d8-00f1 is superseded into this task. Setting it also fixes what 01a0f6d8-00de (copy next public key) must do.
2. `01a0f52e-7707` DEPLOY-4: Solana enrollment address and the node week rate, then the mainnet flip. Blocks self-enrollment on the public node (the 10-13 bar's two friends). Ember derives index 0 from the offline seed, enables required memos, does a 1-DREGG dry run, then publishes. Codex notes say devnet/synthetic paid entry passes; mainnet is environmental. Design assumes 5,952,380 credit/h (1000 DREGG = 168 h).
3. `01a0f52e-771c` BACKUPS-AGE: one age public key (age-keygen, send the age1... line). Blocks encrypting backups that include friends' session keys; the encrypted-backup machinery is already committed (dregg-infra 1f70524), only the recipient is missing.
4. `01a0f54c-d1dd` The consolidated EMBER list (assignee ember, 41 notes). Still-human items from it: pushes of ~/dev/dregg-infra and ~/dev/dregg-assortia (Codex notes record Ember authorising pushes); `sudo chown ember ~/.ssh/id_portable`; send the Sigilante note; Chutes key placement and /etc/mini/providers.json; create the Discord app and register commands.json; FRIENDS.md contact lines; keep-only-newest retired Store in mini-backup; the DECIDE list whose defaults stand. Codex notes claim many of these were delegated and resolved; re-confirm before relying on that.
5. `01a0f52e-7763` GITHUB: read prs/github-drafts (FINALIZE-LOG.md first), fill issue-66's three slots, post in INDEX order. Outward-facing and irreversible; contributors are waiting. Closures #55/#59/#65/#68/#69 can go any time.
6. `01a10500-f300` Live g4 app 8502: close the refused v3 attempt directory without deleting files. A cutover decision on the live r2 SPK world; v3 freshness checks refuse there until it is made. Related: the SPK recovery code the live world ran is on no branch (01a10556-492a).
7. `01a0f6db-c50a` Clock tickers: replacement route and a bound on the tick step. Replacing a ticker subject needs a re-genesis today, and a leaked clock key can push clock/now arbitrarily far forward permanently. Choose a clock-control capability on a separate cold key, plus a step bound.
8. `01a10564-84ef` Use the C machine as the native executor for Objective admission, behind the differential gate? Design fork: 900-2900x faster than Lean runBounded (which is what admission re-execution runs). Needs the gate and the tariff statement first; decision can wait on 01a10564-845b and 01a10564-8480.
9. `01a0f96b-34f4` CHANNELS 10.10: how sealed messages are keyed (your MLS question). Ember's stated preference, recorded in 01a104f3-e2ed, is PQ/hybrid over MLS, so this can be resolved on the record; Codex notes treated it as engineering analysis.
10. `01a0f52e-7777` TEARDOWN-LEFTOVERS: PoA chain data 4.8 GB, two old images 2.4 GB, TELEGRAM_* secrets, portal links, DNS records. Deletions and DNS are Ember's call; nothing was removed.
11. `01a0f6ac-3722` NOCK-PACK: send or not the local contribution pack for Chris Allen's swim-lanes. Outward-facing. Pack is built at /Users/ember/workbox/nockchain-pack-2026-10-01/, nothing sent.
12. `01a0f961-721d` tokeman: per_session_reserve has no input after drain-truth; delete or re-ground. Policy call in a separate project; low blocking.

No task exists for these; they come from the mining file: (a) archive candidates among the 256 codex lane dirs (section C of CODEX-LANE-MINING-20261004.txt; to /tank, not deletion; Ember decides); (b) the mining file's correction that SPK failed-START recovery and ten other evidenced results sit on no branch is a root/successor matter, not Ember's.

## 4. LANDED-VERIFY (root to close)

| id | title | commit |
|---|---|---|
| `019f6e94-5c35` | sim: synthetic fleet generator + replay-cost bench | c9859bca (cv review_sha of the landed revision) |
| `019f6e94-5c52` | sim: dogfood-loop scenarios — refute path, rubber-stamp, crashed worker, N-task fleet | f28b5277 (cv review_sha of the landed revision) |
| `019f6e94-5c6a` | honesty fixes: receipts overclaim wording, Done-attestation carve-out label, trust-model (solo-fleet) declarat | 66bec7b0 (cv review_sha of the landed revision) |
| `019f6e98-0e41` | G9 followup: resume argv may persist secrets — allowlisted launch manifest instead of raw argv replay (codex r | d5004d3f (cv review_sha of the landed revision) |
| `019f6eef-dc51` | provenance: freshness on the debt/landed surface (verified_at + age on every landed/suspect row; Unknown first | fd55d6d3 (cv review_sha of the landed revision) |
| `019f6ef7-0455` | excellence: TOFU per-worker credentials — close pin_identity (bind token on first use; store rejects mismatche | 34c61847 (cv review_sha of the landed revision) |
| `019f6ef7-0469` | excellence: verifiable Done — cv task done --check-cmd/--check-http/--check-file that cv RUNS and records; clo | 970d0a71 (cv review_sha of the landed revision) |
| `019f6ef7-047c` | excellence: harden saw_change past echo — require opened-changed-file / diff-in-context / ran-repo-tests; narr | 440e52b0 (cv review_sha of the landed revision) |
| `019f6f36-7715` | close sesh ls --json gaps (#15): sizeBytes, git.branch, title fallback, freshness doc | 4b3c602b (cv review_sha of the landed revision) |
| `01a0f52e-76c9` | HERMES-TARIFF: per-route tariff so own-key calls pay only the per-op fee | 97644f8f Hermes tariff by route: an own-key call pays only the per-op fee, and the purse charges by the route it recorded at reserve |
| `01a0f52e-76d3` | K-ROOM 3c: room verbs + birth gate + J7 pole for room capabilities | 3f30a38c K-ROOM 3c: j10c re-delegates the newcomer's invite to the sponsor |
| `01a0f52e-76e8` | PLACE 6/7/8: concierge+credit verbs, Hermes-in-a-room, the story verbs | 14f6dd98 P-CREDIT: a week in a room — credit, pay, tariff, topup, room status/renew/concierge, the concierge, J17; 8582425f P-HERMES-ROOM: Hermes in a room — summon/ask/d |
| `01a0f52e-76f2` | MUD lanes 7-16 (tidewrack playable) + SheetLaw regen from the fixed laws | 8280b8d7 MUD laws: refuse the referee's smite, fail closed without the clock |
| `01a0f52e-76fd` | JOIN-SOLANA: the friend-side self-enrollment client + FRIENDS.md section | 5f1f79db Integrate durable paid onboarding and exact claim recovery client |
| `01a0f52e-7783` | COLD-READ: 24 s first signed read after a Store restart | a83df5db mini: hash the selected Host image once per file identity, not once per request |
| `01a0f546-51e3` | WELL-BIRTH-GATE: gate births into rooms so strangers cannot list fake realm assets | 3f30a38c K-ROOM 3c: j10c re-delegates the newcomer's invite to the sponsor |
| `01a0f5d3-e6d9` | K-DOC-INDEX: link/backlink index as a cached fold, coverage-filtered | 28008e8a K-DOC-INDEX: links and backlinks are a cached fold of the accepted log, cut to what the reader may read |
| `01a0f5d4-b7f2` | K-TRANSCLUDE: range transclusion with disclosure at transclusion time | 6402be4b content: range transclusion with disclosure at transclusion time; a read target is a guard, not a write |
| `01a0f5d7-d167` | K-DOC-HISTORY: doc history / show --at / diff over the signed log | 76513bf9 K-DOC-HISTORY: doc history / show --at / diff over the signed log, and `at` answers only a grant that stood at that height |
| `01a0f5d8-4382` | WEB-ENTRANCE: mini web, read-only loopback hypertext over signed reads | aae807c7 mini web: a read-only loopback hypertext face over the workspace's own signed reads |
| `01a0f5e5-d817` | P-AFFORDANCES: can NAME — prepare-not-submit each held verb | d2b8d1cd Host/DryRun: submit_storage_irrelevant — the submission half names no Store writer through its config |
| `01a0f5e6-b2aa` | P-DOC-WRITE: doc pull / doc push @FILE, stale by line | 8af442e5 mini: doc pull / doc push @FILE, a stale line refused by line (DEOS #4, J12W) |
| `01a0f5ef-d69f` | WEB-ENTRANCE: stream tail, at-height and room who routes after k-stream/k-index land | b415da04 mini web on the docuverse braid: view-document pages, index backlinks, history / at / diff pages |
| `01a0f5fe-30fd` | CLOCK-SUBJECT: tick under a dedicated clock subject, not the sponsor's workspace; prune attempt dirs | 8a69da0f CLOCK-SUBJECT: a dedicated clock subject ticks under C_tick; signed reads see the clock; ticks and reads are ephemeral |
| `01a0f605-d8f2` | K-DOC-ORDER: an ordering field for document lines (push inserts by id bisection) | eb44a043 content: the element tree — document order is the tree's walk; editElement splices, moves, removes; a transclusion at line N |
| `01a0f611-ea7b` | K-TRANSCLUDE follow-up: wire doc transclude/follow/show into the shell | de327c39 shell: the docuverse verbs, one workspace action each (cv 01a0f65d-f8b0, 01a0f611-ea7b) |
| `01a0f612-7aa8` | K-DOC-INDEX merge: replace final's fold doc_backlinks with the view; add shell 'doc links' | d9ffd503 Merge k-doc-index into k-marks: the link index and unlink, on the element tree |
| `01a0f612-7abd` | LinkIndex: transclusion targets under their source document | 0c6d54b5 LinkIndex: a transclusion is a backlink of the document it reads |
| `01a0f64e-c637` | MUD-BRAID: final-mud ready for the integrator | d7f6b650 jclock: the probe law is verb-guarded like every MUD clause; a prepare-stage law refusal is read |
| `01a0f64e-c645` | Signed reads see no clock slots: an unguarded clock law locks out observation | 8a69da0f CLOCK-SUBJECT: a dedicated clock subject ticks under C_tick; signed reads see the clock; ticks and reads are ephemeral |
| `01a0f65d-f895` | K-DOC-ORDER finish: doc push places inserts by element edit (merge p-doc-write onto the element tree) | ef041cf4 Merge p-doc-write (8af442e5): doc pull / doc push over the element tree; K-DOC-ORDER closed |
| `01a0f65d-f8a3` | Host serve exits on a malformed proposal draft (availability: one bad request stops the service) | 4c5c58a3 host: a malformed request is refused by name and the session answers on; mini serve restarts a Host that stops |
| `01a0f65d-f8b0` | Shell verbs for the element tree: doc move / remove / insert --at / transclude --at | de327c39 shell: the docuverse verbs, one workspace action each (cv 01a0f65d-f8b0, 01a0f611-ea7b) |
| `01a0f674-fa35` | PAY-BRAID: final-pay ready for the integrator | ed8fcac7 hermes-keys evidence: read the purse from the view's cell (wave-c) |
| `01a0f674-fa61` | PAY: drive self-enrollment (ops 117-120) from the observer's tick | 5f1f79db Integrate durable paid onboarding and exact claim recovery client |
| `01a0f682-5a59` | HOST FAIL-STOP: a malformed JSON request kills minidregg-host for every client | 10e2cc2b journey: JSERVE, a hostile client against the live service (after J4) |
| `01a0f699-cd4f` | FLEET-COMPAT: Pug's dregg-client-sign journey against a Mini host | a88f2c6a mini fleet-sign: dregg-client-sign verbs as Mini fleet turns; a stale plan re-plans |
| `01a0f69a-f7d1` | DOCUVERSE-BRAID: one branch for the docuverse lanes + the web face on it | 52c56775 jweb: its own room names, and a board that J8 did not deny |
| `01a0f69b-d96c` | SPK-APPS: the host side on the new store + a survey of real Sandstorm apps | 24b0870a evidence: Radicale survey through its continued generation |
| `01a0f69e-4718` | K-PREROTATE: key pre-rotation — a stolen daily key cannot rotate | 8234d225 K-PREROTATE: key pre-rotation -- a stolen daily key cannot rotate; the committed next key does |
| `01a0f6ad-8d4a` | Shell verbs doc mark / doc unmark (K-MARKS client actions exist; shell not on this tree) | de327c39 shell: the docuverse verbs, one workspace action each (cv 01a0f65d-f8b0, 01a0f611-ea7b) |
| `01a0f6ad-8d6f` | K-MARKS x K-FIELDS: reviewer rows via a fields={annotations} grant at merge | 0a00cb27 journey: J-DOCUVERSE (JDV) through the shell; controls follow the one renderer; J12C stub deleted |
| `01a0f6b9-7ae7` | K-NARROW-HIDE: a narrowed view must not carry the cell root; prove independence of uncovered fields | c8bb4c15 K-NARROW-HIDE: the cell root is salted per entry and keyed by an owner-derived blinding; a narrowed read opens what it covers and sees only l |
| `01a0f6e0-92be` | C1 JOB-LAW: Kernel/Job.lean — the job lifecycle as a Pred law with both poles per edge | 0af0521b jjob1, Kernel/Job: a declared cell is born holding field 1 = 0; the order writes program from it |
| `01a0f6e3-28d0` | C3 K-JOB-MONEY: job escrow, payout and slash as conservation-checked Book turns | 759ff314 Job money: escrow, bond and payout as conservation-checked Book turns (C3 K-JOB-MONEY) |
| `01a0f6e3-3f03` | C14 TAIL-BOUND: a node cannot run more than L heights past its last certified checkpoint | 4caf8c0b C14: a between-step certify advances the journey's exact count; birth names tail-bound |
| `01a0f6f0-6a5f` | C2 K-RUN-PIN: pinned program context, noun output slot, ABI v3 | 7a7b3881 K-RUN-PIN: Abi.context live / pinned, the noun slot type, ABI v3 (COMPUTE C2) |
| `01a0f6f3-58ad` | T1 WORLD-COMPLETE: Turn/World gain spent, allowance, the parent home, the no-cell turns — every receiver expre | de5e0f55 kernel(world)!: T1 world-complete — spent, the meter, the clock pin, the footprint; every live admission is a Turn shape |
| `01a0f6f6-8ef4` | P-DOC-RENDER: doc show renders marks, transclusions, annotations, links, outline; --raw | 6ff106d6 journey(j12t): D's placeholder names the source by D's own reference, "wall" |
| `01a0f70e-4a73` | P-DOC-RENDER follow-up: mini web renders /doc through render::html (delete web.rs's own line loop) | 0a00cb27 journey: J-DOCUVERSE (JDV) through the shell; controls follow the one renderer; J12C stub deleted |
| `01a0f71e-1251` | E1 K-EVAL: Evaluator structure + Nock instance (EVAL §7 E1) | f6a77427 K-EVAL E1: the Evaluator structure, Nock as registry entry #1 |
| `01a0f726-aaab` | C-SAT-1: law satisfiability as witness-or-certificate (Pred/Satisfiable.lean) | 38073014 Pred.Satisfiable: prune subsumed systems and encode memberOf as runs, so guarded laws stay small |
| `01a0f728-e08a` | G-NORM: Patch.normalize + normalize_run/valid/footprint/idem — the diff is the cut-free normal form (EVAL 2b(a | 7305de19 theory(store): Patch.normalize -- the normal form of a valid guarded patch is its diff |
| `01a0f72e-fcb9` | CH-CELL: channel cell codec, schedule, assemble/fanout, trace theorems (Theory/Channel) | 8eedc274 theory(channel): the channel cell, schedule, assembly and trace theorems (CH-CELL, CHANNELS.md 9 row 5) |
| `01a0f751-cb79` | T3 HOST-REFINES-WORLD: Turn.ofIntent, Represents, deployed_refines_step, trace_represents_fold; the not-a-turn | 19194952 kernel(t3): the present Host refines World.step -- Turn.ofIntent as the diff, Represents, deployed_refines_step; the not-a-turn list |
| `01a0f783-65d6` | CH-EPOCH: EpochRecord + AbsentOpening codecs, ChannelLaw, omission_evident (opening holders), own_omission_evi | 415d84b8 kernel(channel)!: the domain epoch record, its absent opening, and ChannelLaw at the stream append (CH-EPOCH, CHANNELS.md 9 row 8) |
| `01a0f791-e9de` | T4 input from T3: ROM policy-source births are not turns (decide create-with-image vs appendOnly); deployed Br | adff009d kernel(t3b)!: a create carries its ROM image -- install and every initial-policy birth are turns; THE LIST is empty; the deployed Bridge; Rep |
| `01a0f796-17f4` | C1xC3: gate the job law's money columns on the job-money slot; pin Job.law | 6cc2da9c mini job: fund with --amount reads nothing; settle needs no read of the job (the reads around it are for the report) |
| `01a0f798-7cdd` | NC-2: symbolic loop summaries + declared field maxima — cost O(program), B polynomial in declared maxima | 06aba852 NC-2: Host/Json renders the optional sample-slot max as a JSON string (type the list) |
| `01a0f7c5-1c95` | CH-RELAY-1: mini relay — real ticks, exported assemble/fanout/seal, epoch appends, constant fan-out measured | d967933c channel(relay): mini relay ticks in real time on the kernel's exported assemble, fanout, tick root and seal (CH-RELAY-1, CHANNELS.md 9 row 9) |
| `01a0f7c7-6799` | DOCUVERSE onto final: TRANSACTION v5 twice, one QueryView, atCovered as RefusalReason, K-FIELDS in pageOfView | a561c4b6 web: a room page finds its children by the birth source create retains on final |
| `01a0f7e0-78de` | C-SAT-2: law-sat Host op, law check, can --any, install-time explain | c32a8414 can: a room-scoped capability covers its cell (p-affordances onto a2ac159b) |
| `01a0f814-b32e` | K-RENOUNCE follow-up: run renounce after rotation and an agent renounce live | fdd3f61d jrot: renounce after rotation (task 01a0f814-b32e): the old key is refused, the current key revokes exactly that grant |
| `01a0f88a-68b6` | K-ROOM: a non-member can birth a cell into any room (births check room presence, not membership) | 3f30a38c K-ROOM 3c: j10c re-delegates the newcomer's invite to the sponsor |
| `01a0f8c4-6cd4` | P-STORY x K-FIELD-CLOSURE: story invite must declare player_fields at birth | 176792ce P-STORY: a sealed story's table is the law on every player's cell; J15 121/121 |
| `01a0f9e1-50d3` | AUDIT: a kicked member keeps reading, writing and delegating every cell they created in the room | c2d7ba89 shell: tariff usage names the open field (help text only) |
| `01a0f9e1-50ef` | AUDIT: in a paid room, kick does not end a paid window, and a kicked or never-invited subject buys member by p | c2d7ba89 shell: tariff usage names the open field (help text only) |
| `01a0f9e1-c59a` | AUDIT: a payment at the posted price is journaled underpaid if the founder raises the price before the concier | c2d7ba89 shell: tariff usage names the open field (help text only) |
| `01a0f9e2-5fde` | AUDIT: sealing a room cell ends kick, invite and re-law while members keep writing its cells | c2d7ba89 shell: tariff usage names the open field (help text only) |
| `01a0f9f9-4e52` | Timers race friends: a tick/certify between observe and submit refuses stale-root; mini does not re-observe | 349c1e58 mini: one bounded re-observe-and-re-plan loop for every observe-then-act path (stale-root) |
| `01a0fa13-a3ac` | SPK-WS-PROXY: the loopback TLS browser proxy splices a WebSocket after 101 | b106ae15 spk: drain final upstream reply after browser half-close |
| `01a0fb7a-7a2d` | Member docuverse search and actionable navigation over authorized current collections | 46cb353b Add bounded current document search and actionable shell/web hits |
| `01a104fe-95c2` | SDK Linux control on hbox (mini-sdk + discord-entrance lib/mirror/endpoint rows) | d19bb7bf native/mini-sdk: make the scripted fake-process tests Linux-correct (dash, ETXTBSY) |
| `01a10505-9a79` | Compiler/DurableReceiverIO.lean:1091 unsolved goals on a fresh clone of c8fdd000 (Mac darwin build); diagnose; | aa929eeb Compiler/DurableReceiverIO: Loaded.judge_tail's error case unfolds the monad's bind |

Weaker than the rest: 01a0f52e-76f2 (MUD items 7-16: templates present, the referee/combat runner not separately checked) and 01a0f5ef-d69f (the /stream route is still tracked by 01a0f9ee-5e19). Evidence is lane-tip ancestry or a named file on HEAD, not a re-run of the lane's journeys.

## 5. DUPLICATES superseded

- `01a0f52e-76be` NOCK-FEE: debit Lean steps x tariff.nock.perStep from the runner's account -> `01a0f96d-f34c`. NOCK-FEE original; ember decided the rule in f34c
- `01a0f60e-2dc5` Wire or delete VersionEventRecord: Mini content history has no event-log cell -> `01a0f96d-f360`. ember decided 10-01: delete the event-log twin; f360 carries it
- `01a0f60e-2dd9` since/who reveal pre-join metadata; at does not (coverage rule split) -> `01a0f96d-f360`. f360 carries all-standing-grants coverage for who/since
- `01a0f611-ea9e` K-TRANSCLUDE: PLACE J12c carried-vs-referenced fork still open in PLACE.md -> `01a0f53e-f651`. J12c carried-vs-referenced fork = QUOTE-DISCLOSE
- `01a0f6d8-00f1` Pre-rotate the genesis sponsor key (custody decision: ember) -> `01a1052c-6e3a`. same custody decision, now posed to ember as a decision task
- `01a0f9ee-5e2c` Host cold audit takes 35-40 min on a full journey Store -> `01a0fa73-e626`. same cold-audit cost; e626 has the measured curve

## 6. Notes for the root

- Closure candidate: 01a0f99e-9919 (K-CARRY) is LIVE only on paper. Ember said upgrades are full teardown/rebuild, so a checked carry is no longer a deployment prerequisite; its notes say to preserve the WIP. Your call whether to close it.
- Landed but not closable by me because the work is split: 01a104f3-e2cb (two-uid row landed in gates, NOT-ARMED; the sudo runner remains) and 01a0f802-0329 (PolishchukSpielman part landed d16c20db, Haboeck parts open). Both kept LIVE with that said.
- Several "landed" claims in task notes name a lane tip; only those that are ancestors of main were counted. Tips not found on main (so the tasks stay LIVE): nock-fee c02be4a3 (01a0f96d-f34c), k-fields-observe 1b44ecdb (01a0fadb-65d6), mink-jet-1 822f7f97, protected head frontier, K-CARRY source.
- Tasks mentioning a task id in a commit body are usually saying "still open" (UMBRELLA-SPLIT names 053c and 3d5a that way); I counted a commit only when it says it closes or fixes the task.
- 01a0f52e-76a0 (STANDING INTEGRATOR) is released; the integrator role is now yours.
- The July cv/phoenix tasks (9) show `rev:landed` in cv itself; I tagged them landed-verify and released the claims of dead agent builders. Five other non-Mini open tasks and the 128 `don` closure tasks were left alone.
