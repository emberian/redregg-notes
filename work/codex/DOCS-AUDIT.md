# DOCS-AUDIT — nanodregg

The original-file tables describe the audited snapshot through 00b4f793 (initial inventory at 914f2d7e). They preserve the claims found before the rewrite; deleted-file citations refer to that snapshot. The audit was written before any landing. Implementation and final upstream deltas are recorded below and in DOCS-AUDIT.report.md.
Private audit, 2026-10-26/27. Baseline 914f2d7e, refreshed to 00b4f793 after PROTOCOL-77.1 landed. All tracked Markdown files were read whole except decisions: every title/status and every open/planned/deferred/owed/not-yet/TODO/proposed/design-only entry was read whole. Requested layer headers were read whole. Current assertions are grouped by mechanism; dated measurements and abandoned alternatives are HISTORY, not new measurements. Source inspection is not an executed deployment test. No landing preceded this document.
TRUE: implementation matches. STALE: replaced mechanism or misleading present-tense claim. FORGOTTEN CORNER: still-unclosed feature, promise, consumer or measurement; some have an explicit future trigger. HISTORY: true only as a dated record. The decision-title appendix is a read receipt, not a blanket certification of every historical measurement.
## README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| One writer, deterministic replay, typed object programs | TRUE | Kernel/Receive/Rederive.lean:40; Host/Serve.lean:1; Lang/Program.lean:1 | Share with OVERVIEW; sibling owns README. |
| Old counts/no trie/six operations/eleven verbs and archive map | STALE | SIZE.md; Protocol/Command/Verb.lean:113; Protocol/Table.lean; Kernel/World.lean:296 | Sibling rewrite; replace archive destination with new docs. |

## AGENTS.md / CLAUDE.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Files named in brief exist in tracked tree | HISTORY | git ls-files: neither tracked | Do not fabricate copies; external lane contract applies. |

## CHARTER.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Lean decides, Rust transports/custodies; bounded work and named refusals | TRUE | Kernel/Receive/Rederive.lean:40; client/src/run.rs:1; Protocol/Table.lean | Keep constraints distinct from measurements. |
| Mac build guidance and docs/record links are current operations | STALE | scripts/commit:1; worker contract; deploy/RUNBOOK.md | Update operational navigation. |
| THE BAR proves real provider/distributed deployment | STALE | scripts/bar.sh; decisions/perf.md PERF-13 | Name local stand-ins and keep outstanding integration measurements. |

## SIZE.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Generated census and ratchets | TRUE | gates/size.py:1; gates/ceilings.tsv | Regenerate only; avoid embedding counts in prose. |

## DECISIONS.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original alternatives, objections and project history | HISTORY | decisions/README.md:1 | Retain clearly frozen; not current system guide. |
| Single seed, Host-settled attempts, no activity/cross calls | STALE | client/src/custody.rs; client/src/attempt.rs:3; Lang/StdActivity.lean:11; Lang/Package.lean:139 | Link layer decisions and new docs. |

## client/DESIGN.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Rust transports frames and performs Lean steps | TRUE | client/src/run.rs:1; client/src/frame.rs; Protocol/Command/Frames.lean | Keep boundary. |
| One seed, five steps, six operations, Host committed/notcommitted attempt files | STALE | client/src/custody.rs; client/src/attempt.rs:3; Protocol/Command/Machine.lean:1162 | Rewrite frozen argv/continuation/call and own-follower receipt settlement. |
| Retry identifies intent after a committed response is lost | FORGOTTEN CORNER | client/src/attempt.rs:205; decisions/client.md CLIENT-37 | Caller-held durable intent remains missing. |

## Host/DESIGN.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Authenticated Store, bounded pages, named failures | TRUE | Host/Store.lean; Host/Base.lean:88; Host/Page.lean:248 | Retain current contracts. |
| Segment writer lock, read-only follower, no segment deletion, turn cadence | STALE | Host/Store.lean; Host/Cli.lean:403; Host/Segment.lean; decisions/host.md:543 | Key handle lock; follower owns writable Store; optional retention; byte cadence. |
| Old CLI is complete | STALE | Host/Cli.lean:92 | Use current grammar including genesis authority and carry. |

## Spec/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Top/floor claims for audited history, value/law integrity, settlement and envelopes | TRUE | Spec/Proofs/Claims.lean; Spec/Proofs/Deployed.lean; Spec/Proofs/Floor.lean | Link as assurance boundary. |
| NoRef means no holes | STALE | Lang/Proofs/Chain.lean; Lang/Term.lean | NoRef excludes closure references, not contextual holes. |
| keyFaithful is already removed | FORGOTTEN CORNER | Spec/Proofs/Member.lean:92; Spec/Proofs/Claims.lean:67 | Premise remains; continuation custody is planned. |
| Law-chain floor, law/cancel witnesses, signing/authority/at-most-once/durability/Bell apex | FORGOTTEN CORNER | Spec/README.md:40; Spec/README.md:62 | Preserve separate composition obligations. |

## deploy/RUNBOOK.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Host serve/follow/seal/check/export/import/join and retention | TRUE | Host/Cli.lean:92; Host/Cli.lean:486 | Use parser-verified short operating page. |
| Genesis origin examples and omitted certifier/threshold flags | STALE | Host/Cli.lean:145; Kernel/Receive/Follow.lean:119 | Use current genesis inputs; no copied old origins. |
| StrictModes, nd/nd-hosted, broker custody, roots and socket groups | TRUE | client/src/custody.rs; launcher/src/bin/keybroker.rs; launcher/src/bin/nd-members.rs; sandbox/src/lib.rs | Keep exact identities and custody boundaries. |
| Empty shipped pins, Host finality and old resident recovery wedge | STALE | deploy/tls/pins; client/src/attempt.rs:22; Hosting/Resident/Run.lean:263 | Describe current pins, own finality and intent recovery. |
| Real distributed/provider/cold-cache and updated systemd validation | FORGOTTEN CORNER | deploy/live/README.md:145; scripts/bar.sh | Separate deployment measurement task; not closed by parser checks. |

## deploy/live/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Burst5 runs and their measured failures/repairs | HISTORY | deploy/live/README.md:23; Host/Exit.lean | Retain explicitly as evidence. |
| 0755 bwrap copy is current installation policy | STALE | deploy/RUNBOOK.md; sandbox/apparmor/nd-bwrap | Use current restricted executable/ACL policy. |
| Cursor-bounded journal reads and marker plant | TRUE | deploy/live/journal.sh; deploy/live/harness.sh; deploy/live/broker.sh | Keep check. |
| Changed hosted join/cursor scripts have run under systemd | FORGOTTEN CORNER | deploy/live/README.md:134; deploy/live/README.md:155 | Explicitly not rerun; preserve owed measurement. |

## deploy/testground/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Browser follower, byte WebSocket relay, guest-book founder and loopback service | TRUE | deploy/testground/run.sh; deploy/testground/ws-relay.py; testground/guestbook.mjs | Link TESTGROUND. |
| Certified heads replace sponsor trust once landed | STALE | Protocol/Head.lean:389; Protocol/Command/Machine.lean:1548; Host/Store.lean:55 | Consumer landed, beside sponsor pin; deployed producer absent. |
| Independent kernel reproduction and trusted sponsor key distribution | FORGOTTEN CORNER | testground/build/build.sh:1; deploy/testground/README.md | Keep bootstrap trust boundary. |

## deploy/units/EXITS.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Generated codes/names/fatal classes | TRUE | Ops/Units.lean; Host/Exit.lean; Protocol/Exit.lean | Regenerate, never edit table by hand. |
| sync success stays stopped; retry after 2 seconds | STALE | deploy/units/linux/nd-follow-drive@.service:15 | Actual Restart=always, RestartSec=40; correct generator. |

## deploy/units/STORE.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Key lock, generation-qualified segments/index, atomic base, backup order | TRUE | Host/Base.lean:448; Host/Base.lean:461; Host/Store.lean | Keep generated layout source. |
| Anchor uses HEIGHT and file inventory is complete | STALE | Host/Cli.lean:92; Host/Store.lean:55 | Anchor is STEPS; optional base.cert/cert.tmp now exist. |

## gates/journal-report.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Finite receipt pilot and original matrix results | HISTORY | Census/JournalRun.lean:1; gates/journal_pilot.py | Not production gate results. |
| Journal tooling has a production consumer | STALE | gates/check.py; gates/runs.tsv; scripts/pre-push | Only journal tooling imports its command. |
| Alpha normalization, S0/dependency-context consumer | FORGOTTEN CORNER | Census/JournalExpr.lean; gates/journal-report.md:164 | Retain research consumer obligation and conservative over-invalidation limitation. |

## decisions/codec.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Bounded canonical codecs and pure Lean field/curve proofs | TRUE | Codec/Stream.lean; Codec/Proofs/Field.lean:248; Codec/Proofs/Curve.lean; Codec/Proofs/Ladder.lean | Keep theorem premises; no unforgeability claim. |
| CODEC-11 and 18 remain open for field/curve work | STALE | decisions/codec.md:229; decisions/codec.md:389; decisions/codec.md:658 | Close by CODEC-18/23; prior docs pass did not fix these. |
| Old hand readers/StreamLaws/stamp tasks still open | STALE | Codec/Proofs/Stream.lean; Lang/Wire.lean; Host/Base.lean:132 | Mark successors, preserve dated critiques. |
| Staged proof generator reproducibility | FORGOTTEN CORNER | decisions/codec.md CODEC-20; Codec/Proofs/Field.lean | Retain generator/recipe obligation separately from checked generated proof. |

## decisions/kernel.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Receive, canonical tries, meters, rows, journal/refusal bounds and potential | TRUE | Kernel/World.lean:1492; Kernel/Receive/Rederive.lean:40; Kernel/Proofs/Journal.lean:184 | Describe admitted turns vs refusal steps. |
| KERNEL-17/23 regressed to open | HISTORY | decisions/kernel.md:292; decisions/kernel.md:570 | Already superseded/built; allegation refuted. |
| KERNEL-55 still DESIGN ONLY/PROPOSED; old 41/44/46/49/51/52 proposed titles | STALE | decisions/kernel.md:2819; Kernel/Proofs/Weight.lean; Kernel/Proofs/JournalHead.lean; Kernel/World.lean | Point original proposal at as-built parts. |
| Joint actions imply general multisignature/multiwriter consensus | HISTORY | Lang/StdOffer.lean:286; Kernel/Receive/Call.lean | Offers implement specific atomic deals, not consensus. |

## decisions/host.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Own follower Store, key lock, generation, retention/carry and authenticated open | TRUE | Host/Store.lean; Host/Physical.lean; Host/Cli.lean | Use current file contracts. |
| HOST-22 title still advertises turn cadence | HISTORY | decisions/host.md:543 | Already explicitly SUPERSEDED. |
| Full IO/crash composition and live seal trigger | FORGOTTEN CORNER | Host/Proofs/Loop.lean; Spec/README.md:62; decisions/host.md HOST-69 | Do not promote component contracts to full loop theorem. |
| Certificate reader means deployed certificate producer exists | FORGOTTEN CORNER | Host/Store.lean:55; decisions/protocol.md PROTOCOL-77.1 | Finish HOST-80/seed producer join. |

## decisions/protocol.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Seven operations/twenty verbs, own settlement/cancel, heads, foreign receipts | TRUE | Protocol/Table.lean; Protocol/Command/Verb.lean:113; Protocol/Foreign.lean:34 | Describe actual parser and held-head premise. |
| Old TOFU/adopt and Host-finality/absent-final descriptions | STALE | Protocol/Invite.lean; Protocol/Command/Machine.lean:1183; Protocol/Settle.lean:103 | Use signed invitation/trusted key and follower finality. |
| Certificate on read checked during adoption | TRUE | Protocol/Command/Machine.lean:1548; Protocol/Head.lean:389 | Sponsor pin remains; zero threshold is not a valid empty certificate. |
| Producer, no-sponsor bootstrap and log-page certificates | FORGOTTEN CORNER | decisions/protocol.md PROTOCOL-77.1 | Preserve exact outstanding consumers. |
| Privacy and wants triggers | HISTORY | decisions/protocol.md PROTOCOL-3; Protocol/Table.lean | Preserve future triggers, not current functionality. |

## decisions/client.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Same argv resumes unsettled frozen call; follower receipts settle | TRUE | client/src/attempt.rs:205; client/src/run.rs:119 | Rewrite DESIGN. |
| CLIENT-36 verb list | TRUE | Protocol/Command/Verb.lean:113; client/src/bin/nd.rs:43 | Twenty Lean verbs plus local custody flags; describe is read OBJ ?. |
| Cross-session fairness and lost-final-reply intent identity | FORGOTTEN CORNER | attach/src/main.rs:8; client/src/attempt.rs:205; decisions/client.md CLIENT-12/37 | Document current limits, build intent identity before at-most-once claim. |
| Hybrid signature/one seed/Host settlement | STALE | Codec/Ed25519.lean; client/src/custody.rs; client/src/attempt.rs:3 | Mark superseded. |

## decisions/hosting.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| World-driven member decider, confined grains, broker custody, resident intent/effect tree | TRUE | launcher/src/bin/nd-members.rs:1; Hosting/Resident/Run.lean:249 | Keep current boundary. |
| nd-members still cites deleted nd-member@ | HISTORY | launcher/src/bin/nd-members.rs; deploy/units/linux/nd-members@.service | Exact search finds no nd-member@ reference; allegation refuted. |
| Empty shipped pins/answers relation/RESIDENTS manifest | STALE | deploy/tls/pins; Hosting/Resident/Run.lean:56; Hosting/BrokerWire.lean | Use rings/pending, deployed pin file and World residents. |
| Other-platform and multi-principal deployment coverage | FORGOTTEN CORNER | launcher/tests/fence.rs; sandbox/src/lib.rs; decisions/hosting.md HOSTING-17/40/52 | Keep Linux fence evidence separate from unrun deployments. |

## decisions/lang.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Packages, law occasions, relations, live holes, activities, offers, generators | TRUE | Lang/Package.lean:36; Lang/LiveHoles.lean:268; Lang/StdActivity.lean:11; Lang/StdOffer.lean:342; Lang/StdGen.lean:104 | Name real journey families. |
| LANG-44/50 still proposed | STALE | Lang/Rel.lean; Lang/Surface.lean; decisions/lang.md:1428; decisions/lang.md:1904 | Point to built relations/surface, preserve unfinished subfeatures. |
| LANG-48 exact pending family; package claims; general graded effects | FORGOTTEN CORNER | Lang/Claim.lean:32; Lang/Package.lean:36; Lang/LiveHoles.lean | Claim checker is not on package wire/install path; call slots are not general grades. |
| Contextual theory is runtime dependency | STALE | Lang/Contextual/LangInstance.lean:1; Lang/Contextual/NanoBridge.lean:1; Lang/Program.lean:24 | Keep research line; LiveHoles is runtime path. |
| Source IDs/tyText_names/executable Docs promises | FORGOTTEN CORNER | Lang/Surface.lean; Lang/Print.lean; docs/record/ASSEMBLY-lang-docs.md:404 | Preserve explicit authoring/docs obligations. |

## decisions/ledger.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Conservation, bounded grants and ordinary object escrow | TRUE | Kernel/Value.lean; Kernel/Receive/Ledger.lean; Ledger/Sim/Journey.lean | Distinguish value accounts/escrow from signed settlement. |
| Missing cross calls/once-only transfer in original designs | HISTORY | Lang/Package.lean:139; Kernel/Receive/Call.lean | Replaced by callable bodies/nullifiers. |

## decisions/ops.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Rendered argv/identities and exit classifications | TRUE | Ops/Units.lean; deploy/units/linux | Use generated source of truth. |
| OPS-4/16 systemd rerun and generated sync prose | FORGOTTEN CORNER | deploy/live/README.md:155; deploy/units/EXITS.md:184 | Rerun systemd scripts; correct renderer. |
| Old origin/join/permission instructions | STALE | Host/Cli.lean:92; client/src/join.rs:107; deploy/RUNBOOK.md | Update grammar and custody guidance. |

## decisions/perf.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Counts-only standing BAR / earlier fixed counter limits | STALE | scripts/bar.sh; gates/runs.tsv; decisions/gates.md GATES-20x | Clock budgets now judged; full judge includes 1000 records. |
| Local workload and worst-cut/synthetic World measurements | TRUE | Bench/; gates/waste.tsv; gates/bar.tsv | Keep measured scope; synthetic is not full deployed maximum. |
| Real SSH/provider/network/cold-cache workload | FORGOTTEN CORNER | scripts/bar.sh; docs/record/STAND-INS-20261019.md:37 | Retain separate deployment measurement. |

## decisions/gates.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Source gates, reached builds, changed-reach census, full judge/convergence and candidate snapshots | TRUE | scripts/commit; scripts/pre-push; gates/fast.py:49; scripts/converge | Document actual fast/full boundary. |
| Per-card READY/RELEASE or GATES-21 is active landing regime | STALE | decisions/gates.md:654; gates/fast.py:49 | Use current scripts; no invented readiness ceremony. |
| Outside-input keying and cold module probes GATES-20c | FORGOTTEN CORNER | gates/readset.py:40; scripts/standing.sh:146; decisions/gates.md:580 | Still reported, not closed. Preserve soundness obligation. |
| New judge input tables mechanically enter every key | FORGOTTEN CORNER | decisions/gates.md:608; gates/readset.py | W exists; generalized future-table coverage is absent. |
| Journal pilot is production gate | STALE | gates/check.py; gates/runs.tsv; Census/JournalRun.lean | Keep research-only. |

## decisions/root.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Historical decisions and coordination | HISTORY | decisions/root.md; gates/OWNERS | Preserve reasons; transfer surviving archive obligations. |
| Old per-card release state remains mandatory | STALE | scripts/commit; decisions/gates.md GATES-22 | Current landing and convergence govern. |

## decisions/spec.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Top claims and named premises | TRUE | Spec/Proofs/Claims.lean; Spec/Proofs/Member.lean | Retain assurance boundary. |
| Queued witnesses and top claims are done | FORGOTTEN CORNER | Spec/README.md:62; Spec/Proofs/Floor.lean | Keep exact law/cancel/signing/authority/durability/Bell obligations. |

## decisions/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Decision index supplies historical reasons | TRUE | decisions/*.md; gates/append-only.tsv | Keep index; current guide in docs. |
| Statuses all match built tree | STALE | decisions/codec.md:229; decisions/kernel.md:2819 | Correct demonstrated drift; do not close real promises editorially. |

## docs/record/ARCHITECTURE-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/ASSEMBLY-hosting.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/ASSEMBLY-lang-docs.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Docs library/tour and typed name checks absent; law occasions/calls/stdlib built. | FORGOTTEN CORNER | Lang/Package.lean:54; Lang/Check.lean:63; lakefile.lean | Move surviving executable-doc obligation into decision. |

## docs/record/ASSEMBLY-ledger.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/ASSEMBLY-ops.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/ASSEMBLY-perf.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/ASSEMBLY-transport-consent.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/BACKLOG-20261021.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Card readiness and old open backlog are not current gate state. | STALE | gates/fast.py; scripts/commit; Lang/LiveHoles.lean | Delete; current obligations survive below. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/COMPARE-20261021.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/CYCLE-TIME-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/DECISIONS-20261021.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/DELETE-CLOSURE-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DELETE-CODEC-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DELETE-HOST-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DELETE-KERNEL-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DELETE-PROTOCOL-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/DELETE-RUST-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DELVETALK-LEARNINGS.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/DREDGE-20261021.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/GATES-19-DESIGN.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Static-key queue design replaced by traced keys and fast landing. | STALE | decisions/gates.md:432; gates/readset.py; gates/fast.py | Delete; as-built decisions retain rationale. |

## docs/record/GATES-20-DESIGN.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Mode-only stat/reuse predictions refuted; T/C/K read sets implemented. | STALE | decisions/gates.md:514; gates/readset.py | Delete; retain as-built critique. |

## docs/record/GATES-21-PROPOSED.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Merge train explicitly unnecessary under GATES-22. | HISTORY | decisions/gates.md:654 | Delete. |

## docs/record/MINI-CONCEPTS-IN-NANO-20261018.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/NANO-VS-BREADSTUFFS-20261018.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/NANO-VS-MINI-20261017.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/PRIVACY-DESIGN-BRIEF.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Member-held per-object epoch keys/wrapping alternatives; current runtime has no content hiding. | HISTORY | decisions/protocol.md PROTOCOL-3; Kernel/Cell.lean | Preserve private-content trigger/option summary, not transcripts. |

## docs/record/PROOF-TECHNIQUE-20261019.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Technique alternatives and priced frame/head ideas, some implemented. | HISTORY | Kernel/Proofs/Frame.lean; Kernel/Proofs/JournalHead.lean | Delete after preserving live consumer obligations. |

## docs/record/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Dated architecture/scout findings, proposals, measurements and alternatives describe the recorded tree, not a current interface. | HISTORY | Kernel/World.lean:1492; Host/Cli.lean:92; Protocol/Command/Verb.lean:113; Lang/Program.lean:558; decisions/ | Delete; retain live promises in decision addendum, not obsolete recipes. |

## docs/record/RECOVERY-20261016.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Mini branch/session inventory, not missing Nano implementation. | HISTORY | decisions/root.md; Kernel/Receive/Rederive.lean; Lang/Program.lean | Delete from repo; do not republish personal records. |
| Per-card READY/RELEASE active prerequisite | STALE | scripts/commit; gates/fast.py:49; decisions/gates.md:654 | Delete historical gate wording. |

## docs/record/STAND-INS-20261019.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Provider/network/cold-cache/platform measurements remain distinct from stand-ins; some custody/fence gaps closed. | FORGOTTEN CORNER | scripts/bar.sh; launcher/tests/fence.rs; Protocol/Receipt.lean | Preserve remaining measurements. |

## proposals/README.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/README.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/client.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/client.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/codec.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/codec.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/host.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/host.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/lang.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/lang.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/ops.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/ops.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## proposals/protocol.md

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Original proposed interfaces, alternatives, questions and size budgets | HISTORY | decisions/protocol.md | Retain explicitly historical, link current docs. Do not adopt old seed/cadence/wire assumptions. |

## Kernel/World.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: Env, Entry, Reject, Reject.name, Slot | TRUE | Kernel/World.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |
| Check sequence omits ticks | STALE | Kernel/World.lean:1505 | Include checkTicks before step counter. |

## Lang/Program.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: closureDepthMax, reasonMax, Loaded, Loaded.ifaces, reasonText | TRUE | Lang/Program.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |

## Protocol/Command/Machine.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: Self, Refusal, Reply, Reply.cont, Refusal.name | TRUE | Protocol/Command/Machine.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |
| Continuation cannot steer any intent | STALE | Spec/Proofs/Claims.lean:67; Spec/Proofs/Member.lean:92 | Qualify re-derivation with sponsor-key premise. |

## Host/Serve.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: FrameRefusal, FrameRefusal.name, named, declined, FrameRefusal.final | TRUE | Host/Serve.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |

## Hosting/Resident/Args.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Grain argv serializes plan fields with counts; hidden paths are omitted | TRUE | Hosting/Resident/Args.lean:32; Hosting/Resident/Args.lean:35; launcher/src/lib.rs:171 | Keep launcher/Lean serialization correspondence. |
| place reconstructs roots/identity/plan and accepts exact equality only | TRUE | Hosting/Resident/Args.lean:102; Hosting/Resident/Args.lean:119; Hosting/Proofs/Resident.lean | Reordered/dropped/extra fields do not silently select another plan. |

## Hosting/Resident/Bell.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Description validates Bell core and extracts answer method/pending relation shape | TRUE | Hosting/Resident/Bell.lean:145; Hosting/Resident/Bell.lean:155; Hosting/Resident/Bell.lean:193 | No resident-side duplicated method index/layout. |
| One bounded pending range read yields typed ordered rings; answer echoes captured text/aim | TRUE | Hosting/Resident/Bell.lean:243; Hosting/Resident/Bell.lean:251; Hosting/Resident/Bell.lean:316; Lang/Bell.lean | Completeness relies on relation limit and range refusal rather than truncation. |
| Kept pending ring is delivered before asking about a newly lower ring; ring identity includes key and text | TRUE | Hosting/Resident/Bell.lean:218; Hosting/Resident/Bell.lean:268 | Preserve backdating and same-key/text qualifications. |
| Aimed answer forwards in same Turn under Bell grant; durable intent/answer prevents repeated paid ask | TRUE | Lang/Proofs/Bell.lean; Hosting/Resident/Run.lean; Hosting/Proofs/ResidentRun.lean | Pure decision proof alone does not establish filesystem durability; Volume model supplies its contract. |

## Hosting/Resident/Main.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Main delegates directly to Resident.run; file has no layer header docstring | TRUE | Hosting/Resident/Main.lean:1; Hosting/Resident/Main.lean:3 | No documentation claim to correct; preserve minimal entrypoint. |

## Hosting/Resident/Run.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: Exit, all, code, name, tickMs | TRUE | Hosting/Resident/Run.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |
| answers relation; shipped pins empty | STALE | Lang/Bell.lean; deploy/tls/pins; Hosting/Resident/Run.lean:56 | Use rings and deployed pins; provider key still required. |

## Hosting/Resident/Sockets.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Member command uses Protocol layouts and broker ask uses Broker wire; calls have deadlines and named failure results | TRUE | Hosting/Resident/Sockets.lean:44; Hosting/Resident/Sockets.lean:61; Hosting/Resident/Sockets.lean:71; Hosting/Resident/Sockets.lean:90 | Broker result carries parsed text, not raw provider body. |

## Hosting/Resident/Trace.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Trace events/observers support tick ordering proofs; no operational effects or deployed import | TRUE | Hosting/Resident/Trace.lean:15; Hosting/Resident/Trace.lean:27; Hosting/Resident/Trace.lean:58; Hosting/Proofs/ResidentRun.lean:49 | Retain as proof vocabulary, not resident runtime state. |

## Hosting/Resident/Volume.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Model separates live directory entries, inode data and synced history; keep/forget theorems assume this filesystem contract | TRUE | Hosting/Resident/Volume.lean:25; Hosting/Resident/Volume.lean:42; Hosting/Proofs/ResidentVolume.lean | Not a proof of Linux/macOS filesystem implementation. |
| Crash relation allows independent historical entry values and arbitrary unsynced data; model is proof-only | TRUE | Hosting/Resident/Volume.lean:70; Hosting/Proofs/ResidentVolume.lean:50 | Keep crash-model premise explicit. |

## Codec/Deployed.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Deployment fixes 32-byte digests, domain-customized cSHAKE256, kernel codecs and Ed25519 verification; Lang supplies Program | TRUE | Codec/Deployed.lean:21; Codec/Deployed.lean:23; Codec/Deployed.lean:29 | Keep the concrete instance boundary. |
| All facts required by kernel theorems are proved by Codec.Proofs.Deployed | STALE | Codec/Proofs/Deployed.lean:12; Spec/README.md; Spec/Proofs/Claims.lean | Qualify as codec laws and decoded invariants. Cryptographic faithfulness and other Spec premises remain assumptions. |

## Codec/Digest.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Digest is exactly 32 bytes; ordering/equality/indexing use bytes, codec carries raw bytes | TRUE | Codec/Digest.lean:10; Codec/Digest.lean:28; Codec/Stream.lean | Keep representation; not an arbitrary Nat digest. |

## Codec/Ed25519.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Field has ten UInt64 limbs, extended Edwards points, simultaneous scalar multiplication and cofactored equation | TRUE | Codec/Ed25519.lean:21; Codec/Ed25519.lean:70; Codec/Ed25519.lean:123; Codec/Ed25519.lean:176; Codec/Ed25519.lean:224 | Preserve arithmetic bound evidence in Field proofs, distinct from cryptographic unforgeability. |
| Noncanonical S/y and failed decompression refuse; loops terminate structurally; RFC vectors exist | TRUE | Codec/Ed25519.lean:112; Codec/Ed25519.lean:171; Codec/Ed25519.lean:209; Codec/Ed25519.lean:224; Codec/Proofs/Ed25519 | No new cryptographic certification or vector execution claimed. |

## Codec/Hash.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Hash.digest uses cSHAKE customization; Hash.mac uses KMAC256 with Digest key | TRUE | Codec/Hash.lean:218; Codec/Hash.lean:226; Codec/Hash.lean:231; Codec/Hash.lean:239; Codec/Hash.lean:244 | Length-delimited domains separate preimages; this is not a proof of collision resistance. |
| Keccak state has 25 UInt64 fields and structural block iteration; conformance vectors live in proof modules | TRUE | Codec/Hash.lean:30; Codec/Hash.lean:153; Codec/Hash.lean:193; Codec/Proofs/Hash | Keep implementation/conformance distinction. |

## Codec/Kernel.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: callMax, discipline, OpF, opWire, op | TRUE | Codec/Kernel.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |
| Complete Turn/Unsigned lists omit newer fields | STALE | Codec/Kernel.lean; Kernel/Turn.lean; Kernel/Receive/Call.lean | Point at canonical codecs rather than duplicate positional layout. |

## Codec/Layout.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Named-field lists are data consumed by Lean codec and Rust emitter; field codecs take shared frame bound | TRUE | Codec/Layout.lean:14; Codec/Layout.lean:63; Codec/Layout.lean:76; Codec/Layout.lean:85; gates/generated.tsv | Keep shared schema authority. |

## Codec/Path.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Wire path is slash-joined nonempty bounded components excluding dot, dotdot, slash and NUL | TRUE | Codec/Path.lean:17; Codec/Path.lean:26; Codec/Path.lean:47; Codec/Path.lean:51 | Root joining remains operator-specific launcher responsibility. |
| Direct byte scans and structural split implement canonical clean-path round trips | TRUE | Codec/Path.lean:29; Codec/Path.lean:57; Codec/Path.lean:64; Codec/Proofs/Path | Keep proof restricted to clean components. |

## Codec/Prime.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| powMod is bounded square-and-multiply with proved modular exponentiation specification and field-prime certificate | TRUE | Codec/Prime.lean:12; Codec/Proofs/Prime.lean:26 | Keep n/exponent premise; certificate checked by Lean kernel. |

## Codec/Raw.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Raw Nat/list/byte writers are total; lawfulness and round trips require explicit domains | TRUE | Codec/Raw.lean:20; Codec/Raw.lean:76; Codec/Raw.lean:90; Codec/Proofs/Raw | Do not use out-of-domain writes as valid representations. |
| Readers reject declared byte/count bounds and enforce element codec domains | TRUE | Codec/Raw.lean:76; Codec/Raw.lean:90 | Width conversion can truncate an invalid writer input; validity is checked upstream. |

## Codec/Refusal.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Decoders use named refusals with offsets through Except; request layers wrap them in layer refusals | TRUE | Codec/Refusal.lean:10; Codec/Stream.lean; Protocol/Command/Machine.lean | A refusal is not a successful decoded payload. |

## Codec/Sha512.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Eight UInt64 working fields and bounded block/round iteration implement SHA-512; proof vectors exist | TRUE | Codec/Sha512.lean:32; Codec/Sha512.lean:66; Codec/Sha512.lean:77; Codec/Proofs/Sha512.lean | Keep conformance claim tied to proof vectors. |
| 80-word message schedule is a Vector | STALE | Codec/Sha512.lean:55 | Schedule is Array UInt64; constants K are Vector. Correct header representation. |

## Codec/Stream.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: Shape, Bytes, Bounded, Stream, bytes | TRUE | Codec/Stream.lean:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |
| Never copies decode input; fixed little-endian integers; StreamLaws path | STALE | Codec/Stream.lean; Codec/Proofs/Stream.lean; Codec/Varint.lean; Codec/Raw.lean | Name extraction and big-endian/varint extensions/current proof module. |

## Codec/Tag.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Tag hashes a label and codec Shape; stored shape tags reject mismatched codec structure | TRUE | Codec/Tag.lean:22; Codec/Tag.lean:54; Codec/Tag.lean:58; Host/Store.lean | Digest equality relies on the explicit crypto model, not mathematical collision impossibility. |
| Refinement function meaning is not visible in shape; lawfulness census and vectors constrain it | TRUE | Codec/Tag.lean:34; Codec/Proofs/RefineTooth.lean; gates/vectors.py | Keep semantic-change checks distinct from structural tag changes. |

## Codec/Tree.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Node wire is tag, shortest varint payload length/payload and shortest varint child count/children | TRUE | Codec/Tree.lean:40; Codec/Tree.lean:52; Codec/Varint.lean:26 | Keep shared framing authority. |
| Depth exhaustion refuses tooDeep before descending; payload/child counts are bounded | TRUE | Codec/Tree.lean:52; Codec/Tree.lean:84 | Fits proof is carried by decoded tree. |
| Stream.viaTree is the deployed adapter and tree_lawful is proved here | STALE | Codec/Tree.lean:99; Codec/Proofs/Tree.lean:209; Lang/Wire.lean | No viaTree definition remains. Point to current tree conversion/refinement and proof module. |

## Codec/Varint.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Shared bounded LEB128 reader rejects overlong terminal zero, width exhaustion and value past limit; u32/u64 widths are five/ten bytes | TRUE | Codec/Varint.lean:26; Codec/Varint.lean:54; Codec/Varint.lean:59; Codec/Proofs/Varint.lean | Keep shortest-form rule and width limits. |

## Codec/World.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| World wire carries four canonical trie listings then height, steps, chain, allowance and origin | TRUE | Codec/World.lean:222; Codec/World.lean:227 | Node hashes are reconstructed by listingAccept, not trusted from wire. |
| Leaf kind/order, journal/refusal windows, height<=steps and rows fit/head/parent are checked | TRUE | Codec/World.lean:82; Codec/World.lean:128; Codec/World.lean:233; Codec/World.lean:243; Codec/World.lean:257; Codec/World.lean:277; Codec/World.lean:284; Codec/World.lean:292 | Header is a partial list: current decoder also enforces refusal disjointness/counts and world budget. |
| Canonical decoding and journal/refusal invariants have deployed proofs; exact size is computed without encoding | TRUE | Codec/Proofs/Deployed.lean:44; Codec/Proofs/Deployed.lean:87; Codec/Proofs/WorldSize.lean | Use proof module paths; preserve domain premises. |

## Codec/WorldSize.lean — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Named size measures count World entries and support exact/upper-bound size proofs, not request-path recomputation | TRUE | Codec/WorldSize.lean:22; Codec/WorldSize.lean:29; Codec/WorldSize.lean:69; Codec/Proofs/WorldSize.lean | Keep specification measures separate from operational bounds. |

## client/src/attempt.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Signed bytes are frozen after argv and continuation; sends are marked before exchange | TRUE | client/src/attempt.rs:187; client/src/attempt.rs:319 | Keep disk ordering explicit. |
| Signed/Uncertain/Settled state comes from files, with contiguous send markers | TRUE | client/src/attempt.rs:244; client/src/attempt.rs:375 | Temporary fsx residue is deliberately skipped; other unexpected files refuse. |
| Only follower-confirmed committed/refused writes settlement; Host final status only steers | TRUE | client/src/attempt.rs:166; client/src/attempt.rs:290; client/src/attempt.rs:366 | Keep follower versus Host distinction. |
| Same argv resumes the newest un-settled attempt with its original continuation | TRUE | client/src/attempt.rs:209; client/src/run.rs:224 | A settled attempt is excluded; this is not durable caller-intent deduplication. |
| No second call is signed beside a live resumed attempt | TRUE | client/src/run.rs:224; client/src/run.rs:248 | Confirmed refused/expired may safely plan afresh; do not broaden the header into deduplication of settled caller intent. |

## client/src/custody.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Current signs ordinary calls; next signs rotation; armed incoming key can sign read envelopes | TRUE | client/src/custody.rs:445; client/src/custody.rs:479; client/src/custody.rs:508 | Keep exceptional signing roles. |
| Separate custody holds next secret outside workspace; hosted same-record custody has both keys | TRUE | client/src/custody.rs:171; client/src/custody.rs:249; client/src/custody.rs:344 | Do not promise offline theft resistance for hosted records. |
| Next seed is OS randomness and advancement waits for rotation settlement | TRUE | client/src/custody.rs:132; client/src/custody.rs:461; client/src/custody.rs:565 | Retain custody checks and guarded crash-recovery steps. |

## client/src/frame.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| u32 little-endian body length includes operation byte; empty and oversized frames refuse | TRUE | client/src/frame.rs:168; client/src/frame.rs:238 | Keep frame format distinct from other canonical codec integers. |
| Oversized body refuses before allocation and partial body/header is Truncated | TRUE | client/src/frame.rs:168 | Keep resource-bound ordering. |
| Reply deadline is absolute across syscalls | TRUE | client/src/frame.rs:34; client/src/frame.rs:41; client/src/sockets.rs:31 | Keep shared-deadline usage. |
| Child body adds connection number; Rust/Lean wire vectors agree by checked generator/vector rows | TRUE | client/src/frame.rs:259; client/tests/vectors.rs; gates/runs.tsv | Existing vector check, not newly executed by this audit. |

## client/src/fsx.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Write and sync mode-0600 exclusive temporary file, then hard-link create or rename replace, then sync directory | TRUE | client/src/fsx.rs:19; client/src/fsx.rs:29; client/src/fsx.rs:65; client/src/fsx.rs:76 | Durability depends on successful filesystem calls. |
| Temporary residue is skipped by readers and removed before the next same-name write | TRUE | client/src/fsx.rs:36; client/src/fsx.rs:47; client/src/attempt.rs:375 | Keep owned temporary-residue behavior distinct from arbitrary cleanup. |

## client/src/generated.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Protocol table is generated through emit-rust and checked by generated outputs gate | TRUE | gates/generated.tsv:2; Protocol/Table.lean | Edit generator, not generated Rust. |

## client/src/join.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Join takes sponsor key file and invitation hex, invokes confined Host join and saves invitation/input | TRUE | client/src/join.rs:54; client/src/join.rs:105; client/src/join.rs:174; Host/Join.lean | Sponsor key remains a trust input. |
| Bare invite/adopt KEY_FILE use kept inputs; founder --input saves genesis input | TRUE | client/src/join.rs:63; client/src/join.rs:174 | Document local filesystem helpers separately from follower verbs. |

## client/src/lib.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Crate supplies custody, frozen attempts, socket transport and supervisor; protocol values come from generated table | TRUE | client/src/lib.rs:12; client/src/table.rs:6; Protocol/Table.lean | 'Decides nothing' means no World transition semantics; Rust still enforces transport/custody policy. |

## client/src/mux.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Many connections share child stdio using connection-tagged frames; payload is opaque | TRUE | client/src/mux.rs:181; client/src/mux.rs:334; client/src/mux.rs:394 | Connection counter is routing, not identity. |
| Slow reader has bounded writer queue/deadline; frame, idle and in-flight reply use separate limits | TRUE | client/src/mux.rs:310; client/src/mux.rs:334; client/src/mux.rs:394 | Keep connection-level liveness limits distinct from principal fairness. |
| Connections count until fd closes; named best-effort close and child-end unreachable path | TRUE | client/src/mux.rs:61; client/src/mux.rs:106; client/src/mux.rs:141; client/src/mux.rs:394 | A close frame is best effort, not guaranteed delivery. |

## client/src/run.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Follower supplies typed steps, signed bytes and output; Rust executes under step/send bounds | TRUE | client/src/run.rs:341; client/src/run.rs:167; client/src/table.rs | Keep semantic decisions at follower. |
| Earlier open argv attempt is driven before planning; confirmed refused/expired may replan | TRUE | client/src/run.rs:224; client/src/run.rs:248 | Document the safe replan exception to the header shorthand. |

## client/src/sockets.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Workspace follower and writer sockets implement the step-loop Follow and Host interfaces | TRUE | client/src/sockets.rs:56; client/src/sockets.rs:111; client/src/sockets.rs:121 | Keep interface boundary. |

## client/src/stdio.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Hosted stdin accepts only generated STDIO_VERBS; decode/surface refuses precede follower invocation | TRUE | client/src/stdio.rs:50; client/src/stdio.rs:92 | No peer-selected widening. |
| Custody is opened rotation-refusing; workspace/sockets are startup argv, command arguments are not file paths | TRUE | client/src/stdio.rs:44; client/src/stdio.rs:114; client/src/run.rs:341 | Keep file-expanding CLI helpers outside this surface. |

## client/src/table.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Parameters come from generated protocol constants | TRUE | client/src/table.rs:6 | Keep one source for bounds and names. |

## launcher/src/broker_generated.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Generated broker frames come from Hosting.BrokerWire | TRUE | gates/generated.tsv:5; Hosting/BrokerWire.lean | Actual executable is emit-broker; header's generic emit-rust label is imprecise. |

## launcher/src/generated.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Generated launcher frames come from Hosting.Wire | TRUE | gates/generated.tsv:4; Hosting/Wire.lean | Actual executable is emit-hosting; header's generic emit-rust label is imprecise. |

## launcher/src/lib.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Controller provides plans; Rust joins roots, validates paths and constructs sandbox policy/argv | TRUE | launcher/src/lib.rs:31; launcher/src/lib.rs:64; launcher/src/lib.rs:101; launcher/src/lib.rs:171 | Keep controller/launcher responsibilities. |
| One child per grain, ordered reports, all children reaped on controller end | TRUE | launcher/src/bin/grain-launch.rs:203; launcher/src/bin/grain-launch.rs:290; launcher/src/bin/grain-launch.rs:364 | Runtime lifecycle is in the binary using this library. |

## launcher/src/residents.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Keybroker and nd-members share resident request parsing and decider-end interpretation | TRUE | launcher/src/residents.rs:42; launcher/src/residents.rs:67; launcher/src/residents.rs:89 | One consumer helper; no independent alternate parser. |

## client/src/bin/nd-supervise.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: USAGE:, Args, parse, main, run | TRUE | client/src/bin/nd-supervise.rs:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |

## client/src/bin/nd.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header module boundary: main, go, nd_dir | TRUE | client/src/bin/nd.rs:1 and definitions below header | Keep current boundary; generated headers remain generator-owned. |

## launcher/src/bin/grain-launch.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Three roots are disjoint and each launch is limited to its grain and socket names | TRUE | launcher/src/lib.rs:80; launcher/src/lib.rs:101; launcher/src/bin/grain-launch.rs:401 | Keep rootsOverlap/foreignPath refusals. |
| Each child has PID bookkeeping; controller end stops/reaps children, idle emits ticks | TRUE | launcher/src/bin/grain-launch.rs:203; launcher/src/bin/grain-launch.rs:255; launcher/src/bin/grain-launch.rs:290; launcher/src/bin/grain-launch.rs:355 | Do not replace exact-child lifecycle with process-name signalling. |

## launcher/src/bin/keybroker.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Keys, public anchors and leaf-SPKI pins are separate custody-checked operator inputs | TRUE | launcher/src/bin/keybroker.rs:219; launcher/src/bin/keybroker.rs:247; launcher/src/bin/keybroker.rs:319 | No claim that resident custody includes provider secret. |
| Decider's resident set controls sockets; peer uid/group and socket identity constrain requests | TRUE | launcher/src/bin/keybroker.rs:501; launcher/src/bin/keybroker.rs:556; launcher/src/bin/keybroker.rs:618 | Keep socket identity and resident lifecycle. |
| Lean grant selects host/key slot; TLS host verification and SPKI pin precede request bytes | TRUE | launcher/src/bin/keybroker.rs:671; launcher/src/bin/keybroker.rs:776 | Dial address is not certificate hostname. |
| Raw body is decoded by Lean and both raw/body-result key echoes are withheld | TRUE | launcher/src/bin/keybroker.rs:671; launcher/src/bin/keybroker.rs:719 | Resident receives parsed reply, status or named refusal. |

## launcher/src/bin/nd-members.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Each provisioned resident gets private follower then member supervisor, not nd-member@ unit | TRUE | launcher/src/bin/nd-members.rs:451; launcher/src/bin/nd-members.rs:609; launcher/src/bin/nd-members.rs:682 | The reported deleted-unit reference is absent from current header. |
| Follower readiness precedes member; separated state/workspace roots hide custody and Store | TRUE | launcher/src/bin/nd-members.rs:125; launcher/src/bin/nd-members.rs:515; launcher/src/bin/nd-members.rs:609 | Keep startup check and root-separation dependencies. |
| Resident births/removals/restarts are per-name, with crash-loop limit and termination grace | TRUE | launcher/src/bin/nd-members.rs:296; launcher/src/bin/nd-members.rs:310; launcher/src/bin/nd-members.rs:329; launcher/src/bin/nd-members.rs:563 | One missing/broken member must not end other residents. |

## launcher/src/bin/probe.rs — header

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Test grain executes file/socket/ask/wait/nd probes, records per-target result and received bytes | TRUE | launcher/src/bin/probe.rs:55; launcher/src/bin/probe.rs:99; launcher/src/bin/probe.rs:137; launcher/src/bin/probe.rs:148 | Test tool, not production resident API. |
| Normal grain and nd --stdio substitution choose different writable result roots | TRUE | launcher/src/bin/probe.rs:178; launcher/tests/members.rs | Keep isolation test's actual launch mode. |

## Lang/Claim.lean — additional discovery

| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Claims carried in package identity and checked at install | STALE | Lang/Claim.lean:32; Lang/Package.lean:36; Lang/Program.lean:250 | Shape checker/proof exists; no Package claim field or install call. Label building block. |

## Ranked forgotten corners

1. **Build certified-head producer/bootstrap.** Host/Store.lean:55 only reads base.cert. PROTOCOL-77.1 checks it in thin adoption; deployed producer, log certification and sponsor-independent bootstrap remain missing. Finish HOST-80/seed integration.
2. **Build durable caller intent.** client/src/attempt.rs:205 selects only unsettled argv. Crash after settlement before delivery may make repetition a new call. Add caller-held intent identity and lost-final-reply journey; do not confuse transfer --once with arbitrary-call at-most-once.
3. **Build continuation/Spec joins.** keyFaithful remains. Preserve law-chain floor, law/cancel witnesses and authority/signing/at-most-once/durability/Bell top obligations; component proofs do not close them.
4. **Build GATES-20c.** Outside home/config inputs only reported; warm module probes can miss absent paths. Implement previously priced sound coverage with plants; documentation cannot close a soundness obligation.
5. **Build package claims/grades.** Lang.Claim checker/proof not wired to Package/Wire/install. Slots bound call kinds/counts but no general graded effect encoding. Join identity/checker/consumer before advertising.
6. **Run deployment measurements.** Updated systemd harness, real SSH/provider/network/cold-cache and macOS are not closed by local stand-ins. OPS/HOSTING should run a disposable deployment measurement.
7. **Build/document cross-session fairness.** attach/src/main.rs:8 caps a session, not aggregate principal use. Keep limit visible and enforce principal budget when mutually untrusted concurrency is deployed.
8. **Retain/document Census research.** Journal tooling has no production consumer; S0/dependency-context work and alpha-normalization remain. Keep explicit research ownership and concrete next consumer; do not confuse with Kernel journal.
9. **Retain/document Contextual research.** Typed instances are theory, not deployed execution. Keep useful research labelled; runtime path is LiveHoles.
10. **Build executable docs/name checks.** ASSEMBLY-lang-docs ID-6/7/8 never produced Docs target/tour. Prefer shared parser-backed examples/link checks with negative plants over another interface database.
11. **Document privacy trigger.** Current ruling is no blinding. Preserve independent-member private-content trigger and per-object epoch-key/wrapping alternative.
12. **Document wants/live-seal triggers.** Push/wants waits for real need beyond polling; live seal for measured invite downtime. Do not implement dormant mechanisms solely to clear a list.
13. **Build/document founder verification.** Founders must independently check genesis inputs/nonce/authority; sponsor signature alone does not establish desired genesis. Preserve explicit workflow/journey obligation.
14. **Fix generated operator prose.** EXITS sync is always/40s, STORE anchor is STEPS and optional certificate sidecar exists. Fix Ops generator, not generated output.
15. **Preserve authoring promises.** LANG-48 exact pending law is not automatically closed by holes/activity; source IDs, tyText_names and tutorial promises lack consumers. Decide by author use case.

## Delete outright

Delete all 30 docs/record files, as authorized. Before deletion move surviving unique obligations into decisions/root.md: executable docs/name checks; real deployment measures; Census consumer/alpha-normalization; private-content, wants and live-seal triggers; founder verification; exact pending/authoring promises. Summarize options, never transplant raw correspondence, transcript extracts or private coverage metadata. As-built decisions and code retain implemented mechanisms. No other source/test/gate/research deletion is authorized. Keep Contextual and Census labelled research, not deleted for lacking a production caller.

## Rewrite

Create OVERVIEW, MEMBER, OBJECTS, TRUST, OPERATING, JUDGE and TESTGROUND in docs/. Rewrite client/DESIGN and Host/DESIGN as short current contract maps. Correct Spec NoRef/keyFaithful wording, stale requested headers and demonstrated status lines. Replace archive navigation in active files. README is sibling-owned; shared claims: one writer, re-execution, explicit premises, actual command grammar. Certificate consumer is not a deployed producer.
Generated EXITS/STORE corrections belong at Ops/Units.lean under owner authorization. Operational commands touching key material/deployment/publishing were not executed: REPORT records ASK under worker contract. Parser inspection and existing code/tests are evidence, not a new run. No theorem gains hypotheses or is restated.


## Deploy units: actual rendered process contracts

### deploy/testground/units/nd-testground.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| Environment=TREE=/tank/dregg-build/nanodregg/wt/testground-b | TRUE (rendered configuration; deployment not rerun) | deploy/testground/units/nd-testground.service:11; deploy/testground/run.sh | Retain parser-backed configuration; historical live-run coverage is separate. |
| Environment=STATE=/tank/dregg-build/nanodregg/testground-state | TRUE (rendered configuration; deployment not rerun) | deploy/testground/units/nd-testground.service:12; deploy/testground/run.sh | Retain parser-backed configuration; historical live-run coverage is separate. |
| Environment=PORT=8787 | TRUE (rendered configuration; deployment not rerun) | deploy/testground/units/nd-testground.service:13; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/bin/sh -c 'exec "$TREE/deploy/testground/run.sh" start "$STATE"' | TRUE (rendered configuration; deployment not rerun) | deploy/testground/units/nd-testground.service:14; deploy/testground/run.sh | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/testground/units/nd-testground.service:17; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-follow-drive@.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| Environment=ND_WORKSPACE=/etc/nd/follow/%i ND_FOLLOW_SOCK=/run/nd-follow/%i.sock ND_HOST_SOCK=/run/nd/host.sock | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-follow-drive@.service:12; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/opt/nd/bin/nd sync | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-follow-drive@.service:13; client/src/bin/nd.rs:43; Protocol/Command/Verb.lean:113 | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=always | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-follow-drive@.service:15; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=40 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-follow-drive@.service:16; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-grain-launch@.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| ExecStart=/opt/nd/bin/grain-launch /srv/nd-hosted /run/nd-broker /run/nd-member %i /run/nd-grain-launch/%i /opt/nd/bin/hosting-controller /srv/nd-hosted/worlds/%i/store %i | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-grain-launch@.service:14; launcher/src/bin/grain-launch.rs | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-grain-launch@.service:15; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-grain-launch@.service:16; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-host-follow.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| EnvironmentFile=%h/.nd/nd-host-follow.env | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-follow.service:9; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/opt/nd/bin/nd-supervise %h/.nd/ws/follow.sock --write %h/.nd/follow-store --exec /opt/nd/bin/host --hide %h/.nd/ws --hide %h/.nd/holding -- /opt/nd/bin/host follow %h/.nd/follow-store ${ND_MEMBER} ${ND_GRANT} | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-follow.service:10; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-follow.service:11; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-follow.service:12; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-host-serve.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| ExecStart=/opt/nd/bin/nd-supervise /run/nd/host.sock --write /srv/nd/store --exec /opt/nd/bin/host --hide /srv/nd/ws --hide /home -- /opt/nd/bin/host serve /srv/nd/store | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-serve.service:11; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-serve.service:12; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-host-serve.service:13; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-hosted-follow@.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| EnvironmentFile=/etc/nd/hosted/%i.env | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-hosted-follow@.service:10; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/opt/nd/bin/nd-supervise /run/nd-follow/%i.sock --write /srv/nd-hosted/worlds/%i/store --exec /opt/nd/bin/host --group ${ND_GID} --hide /etc/nd --hide /home -- /opt/nd/bin/host follow /srv/nd-hosted/worlds/%i/store ${ND_MEMBER} ${ND_GRANT} | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-hosted-follow@.service:11; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-hosted-follow@.service:12; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-hosted-follow@.service:13; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-keybroker.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| EnvironmentFile=/etc/nd/keybroker/keybroker.env | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-keybroker.service:12; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStartPre=/opt/nd/bin/emit-anchors --check /etc/nd/keybroker/anchors.pem | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-keybroker.service:15; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/opt/nd/bin/keybroker /etc/nd/keybroker/provider.key /etc/nd/keybroker/anchors.pem /etc/nd/keybroker/pins /run/nd-broker /run/nd-keybroker api.anthropic.com:443 /srv/nd/store ${ND_OPERATOR} ${ND_PEER} /opt/nd/bin/hosting-broker | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-keybroker.service:16; launcher/src/bin/keybroker.rs | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-keybroker.service:17; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-keybroker.service:18; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

### deploy/units/linux/nd-members@.service

| Claim | Verdict | Evidence | What to do |
|---|---|---|---|
| EnvironmentFile=/etc/nd/keybroker/keybroker.env | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-members@.service:10; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| ExecStart=/opt/nd/bin/nd-members /run/nd-member /srv/nd-members/%i/members /srv/nd-members/%i/follow /run/nd-member-follow /run/nd-members-%i /run/nd/host.sock ${ND_PEER} /opt/nd/bin/nd-supervise /opt/nd/bin/nd /opt/nd/bin/host /srv/nd/store --hide /etc/nd --hide /home -- /opt/nd/bin/hosting-residents /srv/nd/store | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-members@.service:14; launcher/src/bin/nd-members.rs:57 | Retain parser-backed configuration; historical live-run coverage is separate. |
| Restart=on-failure | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-members@.service:15; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |
| RestartSec=2 | TRUE (rendered configuration; deployment not rerun) | deploy/units/linux/nd-members@.service:16; client/src/bin/nd-supervise.rs; Host/Cli.lean:486 | Retain parser-backed configuration; historical live-run coverage is separate. |

## Explicit row-name citation cross-check

A journey case is usually nested under the gate rows or lang-journey entry, not a separate runs.tsv line. A missing registry spelling in a historical document is not automatically missing functionality. Literal-only matches below locate cases whose registry uses a helper.

### DECISIONS.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| Law/ (DECISIONS.md:230) | STALE | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### decisions/client.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| rotate (decisions/client.md:220) | TRUE (named in source) | Protocol/Rows.lean:585 | Keep nested case distinct from gate entry. |
| rotate (decisions/client.md:227) | TRUE (named in source) | Protocol/Rows.lean:585 | Keep nested case distinct from gate entry. |
| cargo:client:join (decisions/client.md:738) | TRUE (named in source) | gates/runs.tsv:45 | Keep nested case distinct from gate entry. |
| lieLookup (decisions/client.md:792) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| cargo:launcher:members (decisions/client.md:881) | TRUE (named in source) | gates/runs.tsv:42 | Keep nested case distinct from gate entry. |
| cargo:client:vectors (decisions/client.md:1255) | TRUE (named in source) | gates/runs.tsv:36 | Keep nested case distinct from gate entry. |

### decisions/codec.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| gates/generated.tsv (decisions/codec.md:665) | TRUE (named in source) | gates/runs.tsv:26, scripts/gate-lib.sh:124 | Keep nested case distinct from gate entry. |
| gates/runs.tsv (decisions/codec.md:732) | TRUE (named in source) | gates/converge.py:162, gates/runs.py:2 | Keep nested case distinct from gate entry. |

### decisions/gates.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| lean4 (decisions/gates.md:251) | TRUE (named in source) | gates/tcb.py:194 | Keep nested case distinct from gate entry. |
| native_decide:<theorem> (decisions/gates.md:253) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| extern:<module> (decisions/gates.md:254) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| native_decide (decisions/gates.md:257) | TRUE (named in source) | gates/tcb.tsv:6, gates/tcb.py:15 | Keep nested case distinct from gate entry. |
| kernel-sim --toy --seeds N (decisions/gates.md:328) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| - (decisions/gates.md:407) | TRUE (named in source) | lakefile.lean:135, gates/cbytes.py:116 | Keep nested case distinct from gate entry. |
| standing: (decisions/gates.md:437) | TRUE (named in source) | gates/readset.py:337, gates/runs.py:112 | Keep nested case distinct from gate entry. |
| reuse …: reused (key …, byte-identical to the previous judge's) (decisions/gates.md:451) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| reuse …: re-run (key changed) (decisions/gates.md:452) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| ok (decisions/gates.md:708) | TRUE (named in source) | gates/journal_pilot.py:343, gates/certificate_plants.py:153 | Keep nested case distinct from gate entry. |
| cargo-untraced:CRATE:TEST (decisions/gates.md:712) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| cargo-untraced: (decisions/gates.md:739) | TRUE (named in source) | gates/converge.py:158, gates/runs.py:145 | Keep nested case distinct from gate entry. |
| unshare -rm (decisions/gates.md:770) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| script: (decisions/gates.md:883) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| cargo:devtools:workspace (decisions/gates.md:893) | TRUE (named in source) | gates/runs.tsv:44 | Keep nested case distinct from gate entry. |
| script: (decisions/gates.md:940) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| script: (decisions/gates.md:1019) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| script:gates/decls_plants.py --synthetic {fresh}/syn --lean {fresh}/lean (decisions/gates.md:1085) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### decisions/host.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| seal bytes-per-appended-byte (decisions/host.md:228) | TRUE (named in source) | Host/Sim/Run.lean:546 | Keep nested case distinct from gate entry. |
| seal bytes-per-appended-byte (decisions/host.md:242) | TRUE (named in source) | Host/Sim/Run.lean:546 | Keep nested case distinct from gate entry. |
| baseMismatch (decisions/host.md:304) | TRUE (named in source) | Protocol/Invite.lean:97, Protocol/Thin.lean:102 | Keep nested case distinct from gate entry. |
| seal bytes-per-appended-byte (decisions/host.md:339) | TRUE (named in source) | Host/Sim/Run.lean:546 | Keep nested case distinct from gate entry. |
| open verifies-per-turn-cadence (decisions/host.md:590) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| audit (decisions/host.md:606) | TRUE (named in source) | Protocol/Rows.lean:607 | Keep nested case distinct from gate entry. |
| foreign-origin (decisions/host.md:720) | TRUE (named in source) | Ops/Plants.lean:360 | Keep nested case distinct from gate entry. |
| loop resident-entries-per-record-past-base (decisions/host.md:1433) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| refused (decisions/host.md:2002) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| pager .read base per page (decisions/host.md:2267) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| refused (decisions/host.md:2341) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| adoptWrongWorld (decisions/host.md:2913) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| adoptWrongWorld (decisions/host.md:3030) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| forgedRefusal (decisions/host.md:3403) | TRUE (named in source) | Protocol/Rows.lean:1732 | Keep nested case distinct from gate entry. |

### decisions/hosting.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| gates/runs.tsv (decisions/hosting.md:437) | TRUE (named in source) | gates/converge.py:162, gates/runs.py:2 | Keep nested case distinct from gate entry. |
| gates/generated.tsv (decisions/hosting.md:797) | TRUE (named in source) | gates/runs.tsv:26, scripts/gate-lib.sh:124 | Keep nested case distinct from gate entry. |
| cargo:launcher:broker (decisions/hosting.md:826) | TRUE (named in source) | gates/runs.tsv:37 | Keep nested case distinct from gate entry. |
| DeciderExit (decisions/hosting.md:947) | TRUE (named in source) | Ops/Units.lean:360, Hosting/BrokerExit.lean:24 | Keep nested case distinct from gate entry. |
| cargo:launcher:isolation (decisions/hosting.md:1157) | TRUE (named in source) | gates/runs.tsv:34 | Keep nested case distinct from gate entry. |
| cargo:launcher:resident (decisions/hosting.md:1249) | TRUE (named in source) | gates/runs.tsv:38 | Keep nested case distinct from gate entry. |
| cargo:launcher:resident (decisions/hosting.md:1304) | TRUE (named in source) | gates/runs.tsv:38 | Keep nested case distinct from gate entry. |
| cargo:launcher:grain (decisions/hosting.md:1309) | TRUE (named in source) | gates/runs.tsv:39 | Keep nested case distinct from gate entry. |
| grain (decisions/hosting.md:1310) | TRUE (named in source) | Protocol/Rows.lean:1267 | Keep nested case distinct from gate entry. |
| controllerMechanism (decisions/hosting.md:1352) | TRUE (named in source) | Hosting/LaunchExit.lean:123, launcher/tests/isolation.rs:691 | Keep nested case distinct from gate entry. |
| cargo:launcher:resident_bell (decisions/hosting.md:1842) | TRUE (named in source) | gates/runs.tsv:41 | Keep nested case distinct from gate entry. |
| cargo:launcher:resident_bell (decisions/hosting.md:1888) | TRUE (named in source) | gates/runs.tsv:41 | Keep nested case distinct from gate entry. |
| rings (decisions/hosting.md:1970) | TRUE (named in source) | Bench/WorstCutRows.lean:22, Lang/Bell.lean:76 | Keep nested case distinct from gate entry. |
| stdio-leg (decisions/hosting.md:2298) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| stdio-leg (decisions/hosting.md:2317) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| stdio-leg (decisions/hosting.md:2331) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| stdio-leg (decisions/hosting.md:2371) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| rings (decisions/hosting.md:2371) | TRUE (named in source) | Bench/WorstCutRows.lean:22, Lang/Bell.lean:76 | Keep nested case distinct from gate entry. |
| answered (decisions/hosting.md:2374) | TRUE (named in source) | Ops/Units.lean:573, Ops/Plants.lean:439 | Keep nested case distinct from gate entry. |
| stdio-leg (decisions/hosting.md:2424) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| resident_bell (decisions/hosting.md:2433) | TRUE (named in source) | Hosting/Resident/Run.lean:61 | Keep nested case distinct from gate entry. |
| stdio-leg (decisions/hosting.md:2541) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| extern:Host.File (decisions/hosting.md:2551) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| follow-loop (decisions/hosting.md:2551) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| script: (decisions/hosting.md:2587) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| gates/runs.tsv (decisions/hosting.md:2601) | TRUE (named in source) | gates/converge.py:162, gates/runs.py:2 | Keep nested case distinct from gate entry. |
| targets (decisions/hosting.md:2624) | TRUE (named in source) | gates/fast.py:6, gates/check.py:103 | Keep nested case distinct from gate entry. |

### decisions/kernel.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| refusals-per-member-window (decisions/kernel.md:2031) | TRUE (named in source) | Kernel/Sim/Gen.lean:3146 | Keep nested case distinct from gate entry. |
| keep (decisions/kernel.md:2454) | TRUE (named in source) | gates/runs.py:779, gates/rebase.py:505 | Keep nested case distinct from gate entry. |
| refuse verifies-per-refusal (decisions/kernel.md:2528) | TRUE (named in source) | Kernel/Sim/Gen.lean:3147 | Keep nested case distinct from gate entry. |
| plantedArms (decisions/kernel.md:2883) | TRUE (named in source) | Kernel/Sim/Gen.lean:2874 | Keep nested case distinct from gate entry. |
| pending (decisions/kernel.md:3213) | TRUE (named in source) | gates/runs.py:1005, Census/CertificateData.lean:106 | Keep nested case distinct from gate entry. |

### decisions/lang.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| grain (decisions/lang.md:745) | TRUE (named in source) | Protocol/Rows.lean:1267 | Keep nested case distinct from gate entry. |
| rowsMax (decisions/lang.md:1368) | TRUE (named in source) | Kernel/Bounds.lean:104 | Keep nested case distinct from gate entry. |
| use=U (decisions/lang.md:1747) | TRUE (named in source) | Host/Check.lean:8 | Keep nested case distinct from gate entry. |
| value (decisions/lang.md:2819) | TRUE (named in source) | gates/journal.py:22, gates/journal_pilot.py:260 | Keep nested case distinct from gate entry. |
| waits (decisions/lang.md:2841) | TRUE (named in source) | gates/ceilings.tsv:11, gates/runs.py:93 | Keep nested case distinct from gate entry. |
| admission-prepared-type (decisions/lang.md:5635) | TRUE (named in source) | Lang/Journey/ContextualChecks.lean:107 | Keep nested case distinct from gate entry. |
| gates/runs.tsv (decisions/lang.md:5733) | TRUE (named in source) | gates/converge.py:162, gates/runs.py:2 | Keep nested case distinct from gate entry. |
| promo/E1-vectors-diff.txt (decisions/lang.md:5889) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| facts (decisions/lang.md:6135) | TRUE (named in source) | Codec/Deployed.lean:12, Lang/Subst.lean:8 | Keep nested case distinct from gate entry. |
| value (decisions/lang.md:6169) | TRUE (named in source) | gates/journal.py:22, gates/journal_pilot.py:260 | Keep nested case distinct from gate entry. |
| {role, terms} (decisions/lang.md:6307) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| activityLog (decisions/lang.md:6309) | TRUE (named in source) | Lang/StdOffer.lean:127, Lang/Bell.lean:76 | Keep nested case distinct from gate entry. |
| j (decisions/lang.md:6557) | TRUE (named in source) | gates/journal_pilot.py:84, gates/fast.py:52 | Keep nested case distinct from gate entry. |
| (.row key, .row amt vb ver) (decisions/lang.md:6557) | TRUE (named in source) | Lang/Proofs/Rel.lean:441 | Keep nested case distinct from gate entry. |
| ⟨P, 0, kb⟩ (decisions/lang.md:6623) | TRUE (named in source) | Lang/Proofs/StdOfferFuse.lean:558, Lang/Proofs/StdOfferEscrowFuse.lean:59 | Keep nested case distinct from gate entry. |
| rings (decisions/lang.md:6686) | TRUE (named in source) | Bench/WorstCutRows.lean:22, Lang/Bell.lean:76 | Keep nested case distinct from gate entry. |
| rings (decisions/lang.md:6705) | TRUE (named in source) | Bench/WorstCutRows.lean:22, Lang/Bell.lean:76 | Keep nested case distinct from gate entry. |
| --hole-omitted-blocker-pin-admits (decisions/lang.md:6944) | TRUE (named in source) | Lang/Journey.lean:2950, Lang/Journey/Main.lean:14 | Keep nested case distinct from gate entry. |
| rejudge (decisions/lang.md:6952) | TRUE (named in source) | Lang/StdHole.lean:329, Lang/Journey.lean:2109 | Keep nested case distinct from gate entry. |
| unanswered (decisions/lang.md:6976) | TRUE (named in source) | Lang/StdOffer.lean:152, Lang/Bell.lean:146 | Keep nested case distinct from gate entry. |
| facts (decisions/lang.md:7232) | TRUE (named in source) | Codec/Deployed.lean:12, Lang/Subst.lean:8 | Keep nested case distinct from gate entry. |
| gates/runs.tsv (decisions/lang.md:7234) | TRUE (named in source) | gates/converge.py:162, gates/runs.py:2 | Keep nested case distinct from gate entry. |

### decisions/ledger.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| pay (decisions/ledger.md:30) | TRUE (named in source) | Protocol/Rows.lean:1186 | Keep nested case distinct from gate entry. |
| rec {c0 : opt, …, c7 : opt} (decisions/ledger.md:228) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| rec {c0 … c7 : optTy callTy} (decisions/ledger.md:258) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### decisions/ops.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| ops/ (decisions/ops.md:13) | TRUE (named in source) | Protocol/Rows.lean:818 | Keep nested case distinct from gate entry. |
| wrongWorld (decisions/ops.md:86) | TRUE (named in source) | Protocol/Rows.lean:817 | Keep nested case distinct from gate entry. |
| cargo:emit-anchors deploy/tls/anchors.pem (decisions/ops.md:216) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### decisions/perf.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| run (decisions/perf.md:28) | TRUE (named in source) | gates/cbytes.py:35, gates/journal_pilot.py:232 | Keep nested case distinct from gate entry. |
| script: (decisions/perf.md:93) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| script: (decisions/perf.md:152) | TRUE (named in source) | gates/runs.py:195, client/tests/common/mod.rs:33 | Keep nested case distinct from gate entry. |
| standing: (decisions/perf.md:286) | TRUE (named in source) | gates/readset.py:337, gates/runs.py:112 | Keep nested case distinct from gate entry. |
| standing:bench-worstcut-<shape> (decisions/perf.md:669) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### decisions/protocol.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| audit (decisions/protocol.md:78) | TRUE (named in source) | Protocol/Rows.lean:607 | Keep nested case distinct from gate entry. |
| audit (decisions/protocol.md:101) | TRUE (named in source) | Protocol/Rows.lean:607 | Keep nested case distinct from gate entry. |
| thin (decisions/protocol.md:309) | TRUE (named in source) | Protocol/Rows.lean:684 | Keep nested case distinct from gate entry. |
| thin (decisions/protocol.md:322) | TRUE (named in source) | Protocol/Rows.lean:684 | Keep nested case distinct from gate entry. |
| thin (decisions/protocol.md:453) | TRUE (named in source) | Protocol/Rows.lean:684 | Keep nested case distinct from gate entry. |
| paging (decisions/protocol.md:472) | TRUE (named in source) | Protocol/Rows.lean:630 | Keep nested case distinct from gate entry. |
| journey (decisions/protocol.md:626) | TRUE (named in source) | Protocol/Rows.lean:526 | Keep nested case distinct from gate entry. |
| forgotten (decisions/protocol.md:830) | TRUE (named in source) | Protocol/Rows.lean:850 | Keep nested case distinct from gate entry. |
| thinStale (decisions/protocol.md:926) | TRUE (named in source) | Protocol/Rows.lean:713 | Keep nested case distinct from gate entry. |
| refused (decisions/protocol.md:1055) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| refused (decisions/protocol.md:1058) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| invite (decisions/protocol.md:1091) | TRUE (named in source) | Protocol/Rows.lean:979 | Keep nested case distinct from gate entry. |
| invite (decisions/protocol.md:1123) | TRUE (named in source) | Protocol/Rows.lean:979 | Keep nested case distinct from gate entry. |
| use (decisions/protocol.md:1179) | TRUE (named in source) | Protocol/Rows.lean:1008 | Keep nested case distinct from gate entry. |
| use (decisions/protocol.md:1201) | TRUE (named in source) | Protocol/Rows.lean:1008 | Keep nested case distinct from gate entry. |
| describe (decisions/protocol.md:1232) | TRUE (named in source) | Protocol/Rows.lean:1046 | Keep nested case distinct from gate entry. |
| receipt (decisions/protocol.md:1265) | TRUE (named in source) | Protocol/Rows.lean:1098 | Keep nested case distinct from gate entry. |
| receipt (decisions/protocol.md:1285) | TRUE (named in source) | Protocol/Rows.lean:1098 | Keep nested case distinct from gate entry. |
| settle (decisions/protocol.md:1392) | TRUE (named in source) | Lang/StdOffer.lean:67, Protocol/Rows.lean:1364 | Keep nested case distinct from gate entry. |
| rotate (decisions/protocol.md:1399) | TRUE (named in source) | Protocol/Rows.lean:585 | Keep nested case distinct from gate entry. |
| seal (decisions/protocol.md:1452) | TRUE (named in source) | Protocol/Rows.lean:743 | Keep nested case distinct from gate entry. |
| basePin (decisions/protocol.md:1459) | TRUE (named in source) | Protocol/Rows.lean:793 | Keep nested case distinct from gate entry. |
| state (decisions/protocol.md:1531) | TRUE (named in source) | Protocol/Rows.lean:1070 | Keep nested case distinct from gate entry. |
| bar (decisions/protocol.md:1538) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| pageIo (decisions/protocol.md:1569) | TRUE (named in source) | Protocol/Rows.lean:768 | Keep nested case distinct from gate entry. |
| refusedFinal (decisions/protocol.md:1706) | TRUE (named in source) | Protocol/Rows.lean:949 | Keep nested case distinct from gate entry. |
| bell (decisions/protocol.md:1728) | TRUE (named in source) | Protocol/Rows.lean:1537 | Keep nested case distinct from gate entry. |
| bigEvent (decisions/protocol.md:1755) | TRUE (named in source) | Protocol/Rows.lean:1561 | Keep nested case distinct from gate entry. |
| wrongFollower (decisions/protocol.md:1779) | TRUE (named in source) | Protocol/Rows.lean:1578 | Keep nested case distinct from gate entry. |
| uncertainHint (decisions/protocol.md:1823) | TRUE (named in source) | Protocol/Rows.lean:1595 | Keep nested case distinct from gate entry. |
| bar (decisions/protocol.md:1832) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| bar (decisions/protocol.md:1835) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| cancel (decisions/protocol.md:1922) | TRUE (named in source) | Protocol/Rows.lean:1615 | Keep nested case distinct from gate entry. |
| refused (decisions/protocol.md:2042) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| settle (decisions/protocol.md:2049) | TRUE (named in source) | Lang/StdOffer.lean:67, Protocol/Rows.lean:1364 | Keep nested case distinct from gate entry. |
| refused (decisions/protocol.md:2050) | TRUE (named in source) | Protocol/Rows.lean:887 | Keep nested case distinct from gate entry. |
| wrongWorld (decisions/protocol.md:2128) | TRUE (named in source) | Protocol/Rows.lean:817 | Keep nested case distinct from gate entry. |
| nd (decisions/protocol.md:2149) | TRUE (named in source) | lakefile.lean:137, gates/ceilings.tsv:7 | Keep nested case distinct from gate entry. |
| pending (decisions/protocol.md:2195) | TRUE (named in source) | gates/runs.py:1005, Census/CertificateData.lean:106 | Keep nested case distinct from gate entry. |
| staleRefusing (decisions/protocol.md:2257) | TRUE (named in source) | Protocol/Rows.lean:1644 | Keep nested case distinct from gate entry. |
| fork (decisions/protocol.md:2282) | TRUE (named in source) | Protocol/Rows.lean:1759 | Keep nested case distinct from gate entry. |
| certified (decisions/protocol.md:2330) | TRUE (named in source) | Protocol/Rows.lean:1819 | Keep nested case distinct from gate entry. |

### deploy/RUNBOOK.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| cargo-untraced:launcher:fence (deploy/RUNBOOK.md:39) | TRUE (named in source) | gates/runs.tsv:43 | Keep nested case distinct from gate entry. |
| run (deploy/RUNBOOK.md:616) | TRUE (named in source) | gates/cbytes.py:35, gates/journal_pilot.py:232 | Keep nested case distinct from gate entry. |
| standing:bench-worstcut-<shape> (deploy/RUNBOOK.md:653) | STALE | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| worstworld (deploy/RUNBOOK.md:669) | TRUE (named in source) | Bench/WorstWorld.lean:14 | Keep nested case distinct from gate entry. |
| run (deploy/RUNBOOK.md:769) | TRUE (named in source) | gates/cbytes.py:35, gates/journal_pilot.py:232 | Keep nested case distinct from gate entry. |

### docs/record/ARCHITECTURE-20261016.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| JAUDIT (docs/record/ARCHITECTURE-20261016.md:443) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| strace (docs/record/ARCHITECTURE-20261016.md:813) | TRUE (named in source) | gates/readset.py:70, gates/runs.py:400 | Keep nested case distinct from gate entry. |

### docs/record/ASSEMBLY-hosting.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| hermes (docs/record/ASSEMBLY-hosting.md:37) | TRUE (named in source) | Protocol/Rows.lean:1288 | Keep nested case distinct from gate entry. |
| hermes (docs/record/ASSEMBLY-hosting.md:129) | TRUE (named in source) | Protocol/Rows.lean:1288 | Keep nested case distinct from gate entry. |

### docs/record/ASSEMBLY-lang-docs.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| well (docs/record/ASSEMBLY-lang-docs.md:47) | TRUE (named in source) | Protocol/Rows.lean:1206 | Keep nested case distinct from gate entry. |
| Docs/ DOCS (docs/record/ASSEMBLY-lang-docs.md:624) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |

### docs/record/ASSEMBLY-ledger.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| Book (docs/record/ASSEMBLY-ledger.md:165) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| well (docs/record/ASSEMBLY-ledger.md:396) | TRUE (named in source) | Protocol/Rows.lean:1206 | Keep nested case distinct from gate entry. |
| Bound (docs/record/ASSEMBLY-ledger.md:411) | TRUE (named in source) | Lang/HoleBudget.lean:1, Lang/Surface.lean:230 | Keep nested case distinct from gate entry. |
| well (docs/record/ASSEMBLY-ledger.md:490) | TRUE (named in source) | Protocol/Rows.lean:1206 | Keep nested case distinct from gate entry. |

### docs/record/ASSEMBLY-ops.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| gates/generated.tsv (docs/record/ASSEMBLY-ops.md:59) | TRUE (named in source) | gates/runs.tsv:26, scripts/gate-lib.sh:124 | Keep nested case distinct from gate entry. |
| wrongWorld (docs/record/ASSEMBLY-ops.md:373) | TRUE (named in source) | Protocol/Rows.lean:817 | Keep nested case distinct from gate entry. |
| wrongWorld (docs/record/ASSEMBLY-ops.md:455) | TRUE (named in source) | Protocol/Rows.lean:817 | Keep nested case distinct from gate entry. |
| gates/generated.tsv (docs/record/ASSEMBLY-ops.md:478) | TRUE (named in source) | gates/runs.tsv:26, scripts/gate-lib.sh:124 | Keep nested case distinct from gate entry. |

### docs/record/ASSEMBLY-perf.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| gates/waste.tsv (docs/record/ASSEMBLY-perf.md:150) | TRUE (named in source) | gates/readset.py:59, gates/runs.py:538 | Keep nested case distinct from gate entry. |
| native-allow.tsv (docs/record/ASSEMBLY-perf.md:299) | TRUE (named in source) | gates/tcb.py:209, gates/refusals.py:46 | Keep nested case distinct from gate entry. |

### docs/record/ASSEMBLY-transport-consent.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| read bytes-per-page (docs/record/ASSEMBLY-transport-consent.md:478) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| thin (docs/record/ASSEMBLY-transport-consent.md:600) | TRUE (named in source) | Protocol/Rows.lean:684 | Keep nested case distinct from gate entry. |

### docs/record/CYCLE-TIME-20261016.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| objective (docs/record/CYCLE-TIME-20261016.md:254) | TRUE (named in source) | Protocol/Rows.lean:1234 | Keep nested case distinct from gate entry. |

### docs/record/DECISIONS-20261021.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| use (docs/record/DECISIONS-20261021.md:381) | TRUE (named in source) | Protocol/Rows.lean:1008 | Keep nested case distinct from gate entry. |

### docs/record/DELETE-PROTOCOL-20261016.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| journey (docs/record/DELETE-PROTOCOL-20261016.md:17) | TRUE (named in source) | Protocol/Rows.lean:526 | Keep nested case distinct from gate entry. |
| hermes (docs/record/DELETE-PROTOCOL-20261016.md:559) | TRUE (named in source) | Protocol/Rows.lean:1288 | Keep nested case distinct from gate entry. |

### docs/record/DELETE-RUST-20261016.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| journey (docs/record/DELETE-RUST-20261016.md:12) | TRUE (named in source) | Protocol/Rows.lean:526 | Keep nested case distinct from gate entry. |

### docs/record/DREDGE-20261021.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| forgotten (docs/record/DREDGE-20261021.md:39) | TRUE (named in source) | Protocol/Rows.lean:850 | Keep nested case distinct from gate entry. |

### docs/record/NANO-VS-BREADSTUFFS-20261018.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| N:gates/tcb.tsv (docs/record/NANO-VS-BREADSTUFFS-20261018.md:197) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| #guard (docs/record/NANO-VS-BREADSTUFFS-20261018.md:243) | TRUE (named in source) | gates/refusals.py:5 | Keep nested case distinct from gate entry. |

### docs/record/NANO-VS-MINI-20261017.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| pay (docs/record/NANO-VS-MINI-20261017.md:73) | TRUE (named in source) | Protocol/Rows.lean:1186 | Keep nested case distinct from gate entry. |
| exchange (docs/record/NANO-VS-MINI-20261017.md:90) | TRUE (named in source) | launcher/src/residents.rs:20, client/tests/sockets.rs:20 | Keep nested case distinct from gate entry. |
| objective (docs/record/NANO-VS-MINI-20261017.md:280) | TRUE (named in source) | Protocol/Rows.lean:1234 | Keep nested case distinct from gate entry. |

### docs/record/STAND-INS-20261019.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| bar (docs/record/STAND-INS-20261019.md:24) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| bar (docs/record/STAND-INS-20261019.md:57) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| forgotten (docs/record/STAND-INS-20261019.md:66) | TRUE (named in source) | Protocol/Rows.lean:850 | Keep nested case distinct from gate entry. |
| sandbox-exec (macOS) (docs/record/STAND-INS-20261019.md:176) | HISTORY | No exact current registry/literal; gates/runs.tsv and Protocol/Rows.lean checked | Replace old spelling with current case or retain as historical only. |
| bar (docs/record/STAND-INS-20261019.md:227) | TRUE (named in source) | Protocol/Rows.lean:1308 | Keep nested case distinct from gate entry. |
| forgotten (docs/record/STAND-INS-20261019.md:292) | TRUE (named in source) | Protocol/Rows.lean:850 | Keep nested case distinct from gate entry. |
| forgotten (docs/record/STAND-INS-20261019.md:324) | TRUE (named in source) | Protocol/Rows.lean:850 | Keep nested case distinct from gate entry. |
| trustLookup (docs/record/STAND-INS-20261019.md:384) | TRUE (named in source) | Protocol/Rows/Loopback.lean:74 | Keep nested case distinct from gate entry. |

### proposals/protocol.md — explicit row references

| Citation | Verdict | Evidence | What to do |
|---|---|---|---|
| audit (proposals/protocol.md:58) | TRUE (named in source) | Protocol/Rows.lean:607 | Keep nested case distinct from gate entry. |

## Decision read coverage

Every title and explicit status below was read. Whole flagged entries were read separately. This is coverage, not a claim that old open statuses imply absent code.

### decisions/README.md

| Title or status | Location |
|---|---|

### decisions/client.md

| Title or status | Location |
|---|---|
| ## CLIENT-9 one confinement shape, deny by default, one mechanism per platform, no fallback (2026-10-16; allow-list landed by CLIENT-2) | decisions/client.md:9 |
| **Status.** landed (macOS run 10-16; Linux run 10-17; nd-bwrap installed by ROOT 10-17). | decisions/client.md:84 |
| ## CLIENT-10 the step layout read by hand until it is emitted — a twin with an expiry (2026-10-16) | decisions/client.md:86 |
| **Status.** superseded (CLIENT-2, 2026-10-16). CODEC landed the layouts as Lean data with an emitted | decisions/client.md:97 |
| ## CLIENT-11 the member signature: pure Ed25519 or hybrid Ed25519 + ML-DSA-65, and Lean verifies it (2026-10-16, NOT IMPLEMENTED: waits for KERNEL) | decisions/client.md:104 |
| **Status.** open: KERNEL decides which signature a Turn carries (pure or hybrid, and the refusal names); | decisions/client.md:151 |
| ## CLIENT-12 friends over ssh: the remote host.sock (2026-10-16, DESIGN ONLY: waits for PROTOCOL's row) | decisions/client.md:154 |
| **Status.** B chosen; build waits for PROTOCOL's rows and `idleMsMax` in generated.rs (sha to come). | decisions/client.md:202 |
| ## CLIENT-13 the precommitted next key: where custody holds it, and the rotation step (2026-10-16, FOR EMBER: key custody) | decisions/client.md:215 |
| **Status.** RULED by Ember (10-16): Option 2 for members (separate holding); a hosted resident has | decisions/client.md:277 |
| ## CLIENT-14 the mux: one writer per connection, the idle rule waits for nothing in flight, every close named (2026-10-17, BUILD-TRANSPORT; PROTOCOL-22; scout T2) | decisions/client.md:292 |
| **Status.** landed (this commit). `nd-attach` waits on the hang-up frame and the size ceiling. | decisions/client.md:323 |
| ## CLIENT-15 one custody read for every key holder, in the sandbox crate (2026-10-17, CLIENT-3; asked by HOSTING-3) | decisions/client.md:326 |
| **Status.** landed (this commit). | decisions/client.md:357 |
| ## CLIENT-16 the phone's leaf Fits check: a theorem of Lean's leaf decoder, not a Rust refusal (2026-10-17, CLIENT-3; PROTOCOL-6's routed item, cv 01a149bf-8b34) | decisions/client.md:359 |
| **Status.** ACCEPTED by ROOT 2026-10-17. Routed: CODEC-4 proves the decode-to-CellFit lemma, KERNEL-8 | decisions/client.md:390 |
| ## CLIENT-17 one Cargo workspace, and one dev crate for the test harness (2026-10-17, CLIENT-3; ROOT ruling, HOSTING-4's stage 2b ask) | decisions/client.md:398 |
| **Status.** landed (this commit). | decisions/client.md:433 |
| ## CLIENT-18 the public read: a file custody's integrity depends on, but whose bytes are not secret (2026-10-17, CLIENT-3; HOSTING-4's ask for HOSTING-15) | decisions/client.md:435 |
| **Status.** landed (this commit). | decisions/client.md:462 |
| ## CLIENT-19 the custody reads check the directory chain, sshd's StrictModes rule (2026-10-17, CLIENT-3; ROOT ruling on CLIENT-18's flag) | decisions/client.md:464 |
| **Status.** landed (this commit). | decisions/client.md:494 |
| ## CLIENT-20 `Policy.connect`, and a file grant is a connect grant on Linux (2026-10-17, CLIENT-3; HOSTING-17 §5, ROOT rulings) | decisions/client.md:496 |
| **Status.** landed (this commit). | decisions/client.md:545 |
| ## CLIENT-21 nd-supervise `--group GID`: a socket another uid of one group may connect to (2026-10-17, CLIENT-3; ROOT ruling on HOSTING-17 §7, OPS-3, HOST-10) | decisions/client.md:547 |
| **Status.** landed (this commit). | decisions/client.md:575 |
| ## CLIENT-22 the observer record: custody that signs read envelopes only (2026-10-17, CLIENT-3; ROOT ruling, HOSTING-17 §7, PROTOCOL-7) | decisions/client.md:577 |
| **Status.** landed (this commit); the theorem-backed plant follows the flag day. | decisions/client.md:612 |
| ## CLIENT-23 an observer joins like any member, then is sealed by one rename (2026-10-17, CLIENT-3; ROOT ruling (A)) | decisions/client.md:614 |
| **Status.** landed (this commit). | decisions/client.md:639 |
| ## CLIENT-24 `nd --stdio`: a hosted resident's commands through nd-supervise, a surface it cannot widen (2026-10-17, CLIENT-3; HOSTING-20, ROOT rulings, PROTOCOL-40) | decisions/client.md:641 |
| **Status.** landed (this commit). | decisions/client.md:679 |
| ## CLIENT-25 · `declined` is not final: the attempt stays OPEN (2026-10-18, written by PROTOCOL-8 with ROOT standing in for CLIENT; KERNEL-44/47, PROTOCOL-41; landed in the refusals day) | decisions/client.md:681 |
| ## CLIENT-26 · `nd --join`: a member's own World from an invitation its sponsor signed (2026-10-18, CLIENT-5; PROTOCOL-42/44, ROOT rulings on (a)–(c)) | decisions/client.md:706 |
| ## CLIENT-27 · a settlement is the member's word: the attempt store settles a call only from its own follow's receipt; `absent` with a live window is OPEN; a landed rotation reads through its incoming key (2026-10-18, CLIENT-6; PROTOCOL-46 with PROTOCOL-10, ROOT rulings) | decisions/client.md:763 |
| ## CLIENT-28 · a connection is one fd with one end: the supervisor gives back what each connection held, and `full` bounds its fds (2026-10-18, CLIENT-7; PERF-1 FINDING 1, ROOT rulings) | decisions/client.md:798 |
| **Status.** landed (this commit). Operator sentence for EXITS.md sent to OPS-5. PERF-1 re-measures the WASTE rows. | decisions/client.md:844 |
| ## CLIENT-29 · nd-members: each resident grain's member socket from the World, over its OWN follower; nd-member@ and its env file are deleted (2026-10-19, CLIENT-8; HOSTING-30 with HOSTING-9, ROOT rulings; HOSTING-10 agreed) | decisions/client.md:851 |
| **Status.** landed (this commit). The decider becomes `hosting-residents` when HOSTING ships it, and the resident row moves onto nd-members (HOSTING-10). | decisions/client.md:930 |
| ## CLIENT-30 · SIGTERM ends no connection bare: nd-supervise names every close, nd-members stops a removed resident without stalling the tick (2026-10-20, CLIENT-9; cv 01a1507c-722d, ROOT rulings, HOSTING-12 agreed) | decisions/client.md:933 |
| **Status.** landed (this commit). | decisions/client.md:993 |
| ## CLIENT-31 · nd-members refuses at start a socket root its residents' sockets would not fit in sun_path; the name and path bounds are emitted (2026-10-20, CLIENT-9; CLIENT-8 item 10, ROOT ruling) | decisions/client.md:995 |
| ## CLIENT-32 · an `uncertain` attempt end carries follow's own words for a receipt it did not give (2026-10-20, CLIENT-9; cv 01a150b1, PROTOCOL-55's critique, PROTOCOL-58 the Lean half, ROOT ruling) | decisions/client.md:1004 |
| ## CLIENT-33 · Test scratch belongs to its creating test thread (2026-10-20, CX-GATES; ROOT granted CLIENT item) | decisions/client.md:1017 |
| ## CLIENT-34 · Scratch plant obeys the standing Clippy rule (2026-10-20, CX-GATES; follow-up to CLIENT-33) | decisions/client.md:1029 |
| ## CLIENT-35 · `nd invoke … --pin REL KEY`: a member pins a POINT read, so a `(live)` read (E1) is drivable from the deployed client (2026-10-23, CX-CLIENT; cv 01a166e9-a543, measured by CX-P5) | decisions/client.md:1041 |
| **Status.** landed eb77b78. The LANG half of the card (the live column on RANGE rows, one core with E5's receipt column) is CLIENT-36. | decisions/client.md:1066 |
| ## CLIENT-36 · the live column on RANGE rows: a listed row of a `(live)` read carries its key's cell liveness, from the one core a point uses (`Lang.keyColumns`) (2026-10-23, CX-CLIENT; cv 01a166e9-a543's LANG half, on E5's receipt column) | decisions/client.md:1068 |
| **Status.** landed (this commit). | decisions/client.md:1102 |
| ## CLIENT-37 · the next run of the same argv IS its open attempt: nothing re-plans beside a call that may still land (2026-10-24, FIX-RUST; readers/COLLATION-20261024 A6, READ-RUST F1) | decisions/client.md:1104 |
| **Status.** landed a7bccd8. | decisions/client.md:1135 |
| ## CLIENT-38 · every process of ours dies with the parent that spawned it; the runner kills a timed-out row's whole process group; a dead stderr no longer stops nd-supervise's SIGTERM (2026-10-24, FIX-RUST; readers/COLLATION-20261024 A19, READ-RUST F2; closes cv 01a16b44) | decisions/client.md:1139 |
| **Status.** landed (this commit). | decisions/client.md:1171 |
| ## CLIENT-38 · every process of ours dies with the parent that spawned it; the runner kills a timed-out row's whole process group; a dead stderr no longer stops nd-supervise's SIGTERM (2026-10-24, FIX-RUST; readers/COLLATION-20261024 A19, READ-RUST F2; closes cv 01a16b44) | decisions/client.md:1173 |
| **Status.** landed (this commit). | decisions/client.md:1205 |
| ## CLIENT-39 · one deadline per reply, never per read: every peer of ours (Host, follow, a decider, an upstream) is bounded by `frame::Deadline`; a late decider is lost for good; `create_once` leaves a file absent or whole (2026-10-24, FIX-RUST; readers/COLLATION-20261024 A18, READ-RUST F3, F4, F5, F20) | decisions/client.md:1207 |
| **Status.** landed (this commit). | decisions/client.md:1241 |
| ## CLIENT-40 · law 2 for the client's own bytes: every hand-read layout's widths are Lean's, the frame / child wire / rotation record are checked row by row against Lean's codec, and the hand-copied names and numbers are emitted (2026-10-24, FIX-RUST-2; readers/COLLATION-20261024 A17, HOLISTIC-CODEC §4.1–4.2, READ-RUST F16) | decisions/client.md:1243 |
| **Status.** landed (this commit). | decisions/client.md:1273 |
| ## CLIENT-41 · the testground: a member's client in a browser tab, its writer and follow compiled to WebAssembly (2026-10-26, TESTGROUND; redregg/work/promo/DESIGN-TESTGROUND.md) | decisions/client.md:1275 |
| **Status.** landed (this commit). Ember publishes `testground/` after `build.sh`. | decisions/client.md:1285 |
| ## CLIENT-42 · the lying writer: the testground's writer tells the conformance rows' own lies, and the visitor's follow refuses each by name (2026-10-26, TESTGROUND-2; cv 01a17a48-b31e; DESIGN-TESTGROUND §7) | decisions/client.md:1287 |
| **Status.** landed (this commit). Re-emits: `testground/kernel.{mjs,wasm}` (`build.sh c` + `build.sh wasm`); nothing else. | decisions/client.md:1297 |
| ## CLIENT-43 · the hosted World: the same page with the writer behind a WebSocket, the visitor a member joined over an invitation (2026-10-26, TESTGROUND-2; cv 01a17a48-b346; DESIGN-TESTGROUND §3.2) | decisions/client.md:1299 |
| **Status.** landed (this commit). Re-emits: `testground/kernel.{mjs,wasm}`. | decisions/client.md:1309 |

### decisions/codec.md

| Title or status | Location |
|---|---|
| ## CODEC-0 · The row attacked: CODEC is a library below KERNEL, plus one module above it (2026-10-16) | decisions/codec.md:3 |
| Status: open. | decisions/codec.md:20 |
| ## CODEC-1 · One codec structure; its laws are a separate Prop (2026-10-16) | decisions/codec.md:22 |
| Status: open. | decisions/codec.md:38 |
| ## CODEC-2 · Canonicity is stated as "the consumed bytes ARE the encoding" (2026-10-16) | decisions/codec.md:40 |
| Status: open. | decisions/codec.md:53 |
| ## CODEC-3 · Bounds live in the value types (2026-10-16) | decisions/codec.md:55 |
| Status: open. | decisions/codec.md:68 |
| ## CODEC-4 · Integers are fixed width, little-endian; no variable-length naturals (2026-10-16) | decisions/codec.md:70 |
| Status: open. | decisions/codec.md:80 |
| ## CODEC-5 · Every codec carries its Shape; tags are content-addressed from it (2026-10-16) | decisions/codec.md:82 |
| Status: open. | decisions/codec.md:98 |
| ## CODEC-6 · Hash and MAC: Keccak in Lean (SHA3-256 / cSHAKE256 / KMAC256), domain by customization (2026-10-16) | decisions/codec.md:100 |
| Status: open. The speed critique is answered for THE BAR. BLAKE3 stays the alternative if a profile | decisions/codec.md:122 |
| ## CODEC-7 · Ask of KERNEL: domains are a hash argument, not a byte prefix (2026-10-16) | decisions/codec.md:125 |
| Status: open (KERNEL to answer in decisions/kernel.md). | decisions/codec.md:135 |
| ## CODEC-8 · The follow payloads are layouts as data; every field is self-delimiting (2026-10-16) | decisions/codec.md:137 |
| Status: open. | decisions/codec.md:158 |
| ## CODEC-9 · The one recursive codec is a depth-bounded tree; LANG refines it (answers LANG-14) (2026-10-16) | decisions/codec.md:160 |
| Status: open (LANG to adopt; LANG/Wire.lean's readers become `ofTree`). | decisions/codec.md:185 |
| ## CODEC-10 · Every codec knows its size; `oneOf` and `within` bounds; the argv total is Lean's (2026-10-16) | decisions/codec.md:187 |
| Status: open. | decisions/codec.md:204 |
| ## CODEC-11 · Ed25519 verification in pure Lean (RFC 8032, cofactored), measured; no C (2026-10-16) | decisions/codec.md:206 |
| Status: open (owed: `Fe.mul`/`carry` correctness theorems against `Nat` mod p). | decisions/codec.md:229 |
| ## CODEC-12 · KERNEL's values are encoded by codecs lawful ON their bounds (2026-10-16) | decisions/codec.md:231 |
| Status: open. | decisions/codec.md:250 |
| ## CODEC-14 · The World codec: canonical bytes, read back up to `Equiv` (HOST-14's base) (2026-10-16) | decisions/codec.md:252 |
| Status: open. | decisions/codec.md:269 |
| ## CODEC-15 · One deployed Env/Ctx; the digest order is the byte arrays' (2026-10-16) | decisions/codec.md:271 |
| Status: open. | decisions/codec.md:283 |
| ## CODEC-13 · The tree's lengths and counts are canonical LEB128 varints (answers LANG-2's framing ask) (2026-10-16) | decisions/codec.md:285 |
| Status: open. | decisions/codec.md:305 |
| ## CODEC-16 · Tags are content-addressed, with a proof that shapes never share bytes (2026-10-16) | decisions/codec.md:307 |
| Status: open (HOST to stamp `Tag.of` of `Deployed.world` and `batch` into base/segment headers). | decisions/codec.md:324 |
| ## CODEC-17 · An Ed25519 signer beside the verifier, as test tooling (2026-10-16) | decisions/codec.md:337 |
| Status: open (custody ruling stays CLIENT's). | decisions/codec.md:347 |
| ## CODEC-18 · The field arithmetic is proved, not sampled (CODEC-11's owed theorems; CODEC-2, 2026-10-17) | decisions/codec.md:349 |
| Status: open (owed: the Edwards addition law and `mul2` correctness against a Nat-coordinate spec). | decisions/codec.md:389 |
| ## CODEC-19 · The trie World codec: entries in trie order, rebuilt by `build`, refused unless canonical (CODEC-2, 2026-10-17; built at KERNEL-23 part 2, 7c43273) | decisions/codec.md:391 |
| Status: built. | decisions/codec.md:424 |
| ## CODEC-20 · The RFC 8032 checks are staged, so no proof module peaks above ~3 GB (CODEC-2, 2026-10-17; GATES-2's ask via ROOT) | decisions/codec.md:426 |
| Status: open. | decisions/codec.md:450 |
| ## CODEC-21 · Sandbox paths, u32 fields and tagged frames in the one Layout family (HOSTING's ask; CODEC-2, 2026-10-17) | decisions/codec.md:452 |
| Status: open. | decisions/codec.md:477 |
| ## CODEC-22 · The carried state's version is its tag, not a policy (OPS-P1; CODEC-2, 2026-10-17) | decisions/codec.md:479 |
| Status: accepted by OPS-2 (7f7b6da); built after KERNEL-29's Carried lands. | decisions/codec.md:496 |
| ## CODEC-23 · The curve formulas are proved over the field: every point `verify` computes is on edwards25519, and add/double are the Edwards law (CODEC-18's owed curve half, part 1; CODEC-3, 2026-10-17) | decisions/codec.md:520 |
| Status: parts 1–4 built; CODEC-23 complete. | decisions/codec.md:658 |
| ## CODEC-24 · The broker frames are a second generated file, `emit-broker` (HOSTING-3's ask; CODEC-3, 2026-10-17) | decisions/codec.md:660 |
| Status: built. | decisions/codec.md:679 |
| ## CODEC-25 · `Cell.Fits` is emitted for the phone: `cell_fits::{KIND_LIMIT, SLOTS_MAX, SLOT_KEY_LIMIT, VALUE_BYTES_MAX, fits}` (CLIENT-3's need; CODEC-4, 2026-10-17) | decisions/codec.md:681 |
| Status: DELETED (ROOT's ruling on CLIENT-16). `cell_fits` had no caller: a leaf refusal is a decision, so it | decisions/codec.md:699 |
| ## CODEC-26 · A turn's record is exactly `Turn.logWeight` bytes (KERNEL-32's numbers; CODEC-4, 2026-10-17) | decisions/codec.md:708 |
| Status: built. | decisions/codec.md:725 |
| ## CODEC-27 · The emitted `path_clean` is checked against Lean's decoder on every commit (CODEC-21's critique; CODEC-4, 2026-10-17) | decisions/codec.md:727 |
| Status: built. | decisions/codec.md:752 |
| ## CODEC-28 · A refinement's lawfulness theorem is its check; the census refuses a refinement without one (CODEC-5/16's gap; CODEC-6, 2026-10-17) | decisions/codec.md:754 |
| Status: built (census, refine_accept_iff, teeth, and (d) below); step 2 (trie-order stated in bytes) and the version-suffix | decisions/codec.md:873 |
| ## CODEC-29 · `kernel/trie-order` is the order of the bytes, stated without the trie (CODEC-28 step 2; CODEC-7, 2026-10-17, agreed with KERNEL-10) | decisions/codec.md:935 |
| ## CODEC-30 · Law-6 read of the two Equiv allow rows (GATES-3's request; CODEC-7, 2026-10-17) | decisions/codec.md:980 |
| ## CODEC-31 · The journal is a trie on the wire too; decode ∘ bytes = id for the World and the carried state; both allow rows deleted (KERNEL-41 (a′) with KERNEL-12; CODEC-7, 2026-10-17) | decisions/codec.md:1008 |
| ## CODEC-32 · The refusals are a third trie on the wire; the World carries its step count; the log record is a list of steps (KERNEL-44 / KERNEL-47 with KERNEL-14; CODEC-8, 2026-10-18) | decisions/codec.md:1094 |
| ## CODEC-33 · The rows on the wire: a fourth trie, the turn's row touches and range reads, and the kernel's own byte functions as codec sites (KERNEL-46/48 with KERNEL-15/16 and LANG-14; CODEC-9, 2026-10-18) | decisions/codec.md:1225 |
| ## CODEC-34 · A reached World's rows are in the codec's domain (HOST-12's export completeness; CODEC-10, 2026-10-18, against KERNEL-17's `World.RowsOk`) | decisions/codec.md:1361 |
| ## CODEC-35 · The trie day, codec half: a proof's path carries its bits; the listings did not move (KERNEL-49 (a), CODEC-11, 2026-10-18) | decisions/codec.md:1385 |
| ## CODEC-36 · A package's codec is a refine site, so the vectors gate sees a new Lang tag (cv 01a14e58-1586; CODEC-11 with LANG-15's yes, 2026-10-19) | decisions/codec.md:1430 |
| ## CODEC-37 · Versions on the wire: a u64 varint, the entry and rows leaf carry it, the pin preimages keep eight bytes (KERNEL-54 with KERNEL-21; CODEC-12, 2026-10-19) | decisions/codec.md:1466 |
| ## CODEC-38 · The World's refusals total on the wire: a third refusals key kind, the cap's boundary pair (KERNEL-55 part 2, R1, with KERNEL-22; CODEC-13, 2026-10-19) | decisions/codec.md:1521 |
| ## CODEC-39 · A World's encoded size, exactly, against its weight; the slack is 54/49 (cv 01a150a3-2523; CODEC-13 with HOST-14 and KERNEL-22, 2026-10-19) | decisions/codec.md:1565 |
| ## CODEC-40 · The rows encoding is a varint: relation and width as LEB128, key and prefix behind a varint length (cv 01a14f7e with KERNEL-22's K22-ROWS; CODEC-13, 2026-10-19) | decisions/codec.md:1599 |

### decisions/gates.md

| Title or status | Location |
|---|---|
| ## GATES-1 · No package dependencies: Lean core + Std only (2026-10-16) | decisions/gates.md:3 |
| **Status.** open. | decisions/gates.md:17 |
| ## GATES-2 · The def/proof split is structural: a `Proofs` path component (2026-10-16) | decisions/gates.md:19 |
| **Status.** open. | decisions/gates.md:38 |
| ## GATES-3 · Gates judge a private copy of the exact commit, both by the parent's gates and its own (2026-10-16) | decisions/gates.md:40 |
| **Status.** open. | decisions/gates.md:61 |
| ## GATES-4 · One axiom census instead of per-theorem `#assert_axioms` (2026-10-16) — argues law 6 | decisions/gates.md:63 |
| **Status.** open. | decisions/gates.md:80 |
| ## GATES-5 · The size ratchet's mechanics (2026-10-16) | decisions/gates.md:82 |
| **Status.** open. | decisions/gates.md:96 |
| ## GATES-6 · Law 8's "No import hubs" is unmeasurable as stated (2026-10-16) — argues law 8 | decisions/gates.md:98 |
| **Status.** open. | decisions/gates.md:108 |
| ## GATES-7 · Commits stay inside their layer: gates/OWNERS (2026-10-16) | decisions/gates.md:110 |
| **Status.** open (the SHARED lakefile departs from ROOT's table). | decisions/gates.md:125 |
| ## GATES-8 · `scripts/commit` is the only sanctioned way to commit; a commit is refused only for reds it introduces (2026-10-16) | decisions/gates.md:127 |
| **Status.** open. | decisions/gates.md:143 |
| ## GATES-9 · The waste ratchet measures from the sims' own output: `WASTE <op> <metric> <ratio>` (2026-10-16) | decisions/gates.md:145 |
| **Status.** open. | decisions/gates.md:164 |
| ## GATES-9 · A commit is CURRENT main + its paths, and a path is taken only from a worktree whose base for it IS main's (2026-10-17) | decisions/gates.md:166 |
| **Status.** built (9db4020). | decisions/gates.md:186 |
| ## GATES-10 · No separate gate for "a commit reverts another layer's CROSS-LAYER hunk in its own file" (2026-10-17) | decisions/gates.md:188 |
| **Status.** decided; reopen on the first revert with a current base. | decisions/gates.md:207 |
| ## GATES-11 · One landing clone (hbox), N judge slots under flock, every target built and censused every commit (2026-10-17) | decisions/gates.md:209 |
| **Status.** built: 194cefb (the first hbox commit) and d5871cb. 194cefb's message lost three quoted plant | decisions/gates.md:229 |
| ## GATES-12 · The TCB table is gated: what the tree trusts without a proof has a row, pinned to what is actually used (2026-10-17) | decisions/gates.md:245 |
| **Status.** built (this commit). | decisions/gates.md:284 |
| ## GATES-13 · A codec vector is immutable under an unchanged tag (2026-10-17) | decisions/gates.md:286 |
| **Status.** built (this commit). | decisions/gates.md:311 |
| ## GATES-14 · The ungated toy run is deleted; the judge writes its own PID (2026-10-18) | decisions/gates.md:313 |
| **Status.** built (this commit). | decisions/gates.md:353 |
| ## GATES-15 · A runner that cannot read a failure is not a runner: every verdict reader proves it can read red first (2026-10-18) | decisions/gates.md:355 |
| **Status.** A landed 56f4689; B landed in this commit. cv 01a14e41-d666 closes with it. | decisions/gates.md:389 |
| ## GATES-16 · A wall-clock deadline withholds a verdict, never gives one: a timed-out run is UNREAD, re-run once, and the commit is not judged (2026-10-19) | decisions/gates.md:391 |
| ## GATES-17 · A standing-only verdict row: `standing:EXE` runs in standing and never in pre-push (2026-10-19) | decisions/gates.md:404 |
| ## GATES-18 · A CROSS-LAYER reason names the owner of each foreign path (2026-10-19, ROOT ruling) | decisions/gates.md:417 |
| ## GATES-19 · The landing queue: behind-main is a judged merge, readiness order with an age bound, verdicts carried only under a byte-identical input key (2026-10-19/20, ROOT rulings; design docs/record/GATES-19-DESIGN.md) | decisions/gates.md:432 |
| ## GATES-20a · A run is selected by every binary it runs, not only its own: spawning rows, declared drives, and names in the static key (2026-10-20, ROOT ruling; found by GATES-8's traced read-sets) | decisions/gates.md:467 |
| ## GATES-20b · The landed copy: every path is merged from what the lander recorded, never taken from the working tree; a landing that would revert a recent commit is refused `stale path` unless named; a head lander is never charged for a tie (2026-10-21, ROOT rulings; HOSTING-13's hazard, LANG-21's finding) | decisions/gates.md:487 |
| ## GATES-20 · Traced read-sets select the runs and key the reuse; the judge's code is main's, the candidate supplies only its table (2026-10-20, landed 10-21 after GATES-20b; ROOT rulings F1/F2 and "the judge's CODE is main's"; design docs/record/GATES-20-DESIGN.md) | decisions/gates.md:514 |
| ## GATES-20d · A compile's reads are C, compared only against a compile; an escaped name invalidates the trace; an implied directory is not an extra (2026-10-21, ROOT ruling; standing 145283a RED) | decisions/gates.md:580 |
| ## GATES-20e · A judge table is an input of every row it judges: a changed waste ceiling selects the row that measured it, standing-only included (2026-10-21, ROOT ruling; PERF-4's fail-open at 41e041f) | decisions/gates.md:608 |
| ## GATES-20f · A dead lander's scratch is reaped at a later lander's start, by liveness only (2026-10-21, ROOT ruling; PROTOCOL-21's 709572) | decisions/gates.md:628 |
| ## GATES-20b′ · A prior commit's change is contained when the copy holds it, whatever its context (2026-10-21, ROOT ruling; PERF-6's false positive) | decisions/gates.md:642 |
| ## GATES-22 · The fast landing and the convergence: a landing is judged by what it reaches, the whole system every 3 h, a red names the commits it read (2026-10-21, Ember's ruling via ROOT) | decisions/gates.md:654 |
| ## GATES-20k · A failure of the tracer is not a verdict: UNREAD(tracer), re-run once, twice NOT JUDGED; a retry that passes is a counted flake (2026-10-21, ROOT ruling; GATES-10 verified at source) | decisions/gates.md:696 |
| ## GATES-20j · A skipped cargo test is never ok: INCOMPLETE in pre-push, RED in standing; `cargo-untraced:` rows run without the tracer (2026-10-21, ROOT ruling; HOSTING-15's fence, built and planted by GATES-10) | decisions/gates.md:706 |
| ## GATES-20g · Rows run concurrently on free judge slots, each in its own scratch; GATES-20l · the convergence carries what the delta cannot reach, for at most a day (2026-10-21, Ember's question via ROOT; GATES-11 measured, GATES-12 built) | decisions/gates.md:719 |
| ## GATES-23 · A whole-tree census of disjunctive theorem conclusions (2026-10-20, CX-GATES) | decisions/gates.md:788 |
| ## GATES-20m · Namespace read-sets use bwrap's host bind sources (2026-10-20, CX-GATES) | decisions/gates.md:802 |
| ## GATES-20n · Complete the host-view evidence for real bwrap rows (2026-10-20, CX-GATES; follow-up to 20m) | decisions/gates.md:816 |
| ## GATES-20o · A completed pre-bind namespace child has a host-view read-set (2026-10-20, CX-GATES; ROOT ruling A) | decisions/gates.md:829 |
| ## GATES-20p · A moved added theorem keeps its statement (2026-10-21, CX-GATES; ROOT ruling A) | decisions/gates.md:845 |
| ## GATES-20q · The charter's 1 MB file law is a source gate (2026-10-21, ROOT review H3; written by GLM-5.3-flash under supervision) | decisions/gates.md:859 |
| ## GATES-20s · The statement census reads the escape's shape, not its name; a standing plant proves it can fail (2026-10-22, ROOT review H4, program card G1; Claude baseline of experiment 2) | decisions/gates.md:875 |
| ## GATES-20t · The stale-path guard's `.lean` half is a declaration diff from the census environment, and a landing's map of what it deletes and restates is checked (2026-10-22, Ember's R-0023; R-0034 under promo/READ-GUARD-grok.md; card cv 01a15f18-2636; CX-GUARD; supersedes GATES-20p) | decisions/gates.md:913 |
| ## GATES-20u · The certificate pins what `grant_moves_le_cap` says and rests on, one level, and the closure reader goes (2026-10-23, ROOT review H3 + H2, program card G2; R-0053, R-0056, R-0057 under promo/READ-G2-grok.md; IMPACT promo/IMPACT-G2.md; cv 01a16131-5868, 01a15f18-25f7) | decisions/gates.md:982 |
| ## GATES-20v · A definition's edited body is named by one line; the fast judge runs the axiom and statement census over its reach; a declared change of meaning is the spec layer's (2026-10-24, FIX-GATES; COLLATION-20261024 A2; READ-LEDGER-CENSUS-GATES D1, D2, D4; Ember via ROOT, real 10-24) | decisions/gates.md:1048 |
| ## GATES-20w · The statement census reads what a membership determines, pushes negations, reads Boolean equations and walks `∀` (2026-10-24, FIX-GATES; COLLATION-20261024 A22; READ-LEDGER-CENSUS-GATES D3; cv 01a1654c-543c) | decisions/gates.md:1122 |
| ## GATES-20y · The miscompiled literal is read from the compiled C, a vector per literal class proves which classes break; the TCB table rows the syscall layer and compares its file pins (2026-10-24, FIX-GATES; COLLATION-20261024 A16, A20's gates half; READ-LEDGER-CENSUS-GATES D7) | decisions/gates.md:1188 |
| ## GATES-20x · THE BAR's clock is judged in every run, the charter's 1000 records on every full judge; the forced contention is an exact row (2026-10-24, FIX-GATES; COLLATION-20261024 A23; READ-LEDGER-CENSUS-GATES D8, B4; CROSS-LAYER: PERF) | decisions/gates.md:1251 |
| ## GATES-25 · Every run has a TMPDIR of its own; a row run again alone is checked on what both of its runs wrote (2026-10-24, FIX-TMPRACE; cv 01a17007-bdbe; the convergence at 743a4fb) | decisions/gates.md:1312 |
| ## GATES-27 · The compiled exe is held to the interpreter's account: kernel-sim's seeds run compiled and under `lean --run`, and must print one byte-identical trajectory (2026-10-26, QA; Ember real 10-26 "maybe we should be being more ambitious about our QA"; design `redregg/work/promo/DESIGN-QA.md` Q1; COLLATION-20261024 A16, Q5; CROSS-LAYER: KERNEL) | decisions/gates.md:1374 |

### decisions/host.md

| Title or status | Location |
|---|---|
| ## HOST-4a · what SQLite gave for free that the flat log now owns (BUILD-HOST, 2026-10-16, per ROOT's ruling) | decisions/host.md:5 |
| **Status.** ruled by ROOT 2026-10-16 (HOST-4 accepted with this list required). | decisions/host.md:22 |
| ## HOST-7a · thin consent is a DECLARED ABSENCE, not a deletion (per ROOT, pending Ember's product ruling) | decisions/host.md:24 |
| **Status.** open (product ruling: Ember). | decisions/host.md:29 |
| ## HOST-8 · lookup answers `absent`; resubmitting the same bytes is idempotent (BUILD-HOST, answering proposals/client.md §3) | decisions/host.md:31 |
| **Status.** open. | decisions/host.md:56 |
| ## HOST-9 · the step protocol between `host follow` and `nd` (with PROTOCOL; answering CLIENT-2) | decisions/host.md:58 |
| **Status.** superseded by PROTOCOL-0..7 (Protocol/Table.lean: the step tags, statuses and client bounds are PROTOCOL's table; Host consumes them and defines none). `resume_rederives` stays an obligation, now of PROTOCOL-4 (`Receive.rederive`). | decisions/host.md:77 |
| ## HOST-10 · checkpoints are incremental: a base plus delta records in the same framed log (BUILD-HOST, per K1 / 617bb3a) | decisions/host.md:79 |
| **Status.** open; HOST-14 (the measurement this meta-critique asked for) proposes withdrawing it. | decisions/host.md:113 |
| ## HOST-11 · how the loop gates `log` and `read` on a follow grant, O(touched) (2026-10-16, answering PROTOCOL-3) | decisions/host.md:115 |
| **Status.** open (KERNEL: `grantOf`'s name and shape; CODEC: the verifier and request domain tag). | decisions/host.md:143 |
| ## HOST-12 · torn vs corrupt is decided by a forward scan, not by size (2026-10-16; found by plant-flip-byte) | decisions/host.md:145 |
| **Status.** open. | decisions/host.md:166 |
| ## HOST-13 · a def-module structure with a proof field proves its instances' witnesses privately (2026-10-16; accepted as cost by ROOT) | decisions/host.md:168 |
| **Status.** ruled by ROOT 2026-10-16 (accepted as cost). | decisions/host.md:178 |
| ## HOST-14 · K1 re-argued with the number: a whole-World base in a Task, no deltas (2026-10-16, HOST-2; ROOT to rule) | decisions/host.md:180 |
| **Status.** ACCEPTED by ROOT 2026-10-16; HOST-10 withdrawn. Conditions, each to land as code: (1) the | decisions/host.md:226 |
| ## HOST-15 · thin consent: a member that does not fold the whole log (2026-10-16; Ember ruled IN "if we can get away with it"; with PROTOCOL-14) | decisions/host.md:279 |
| **Status.** open (PROTOCOL-14 owns the page layout and the `baseMismatch` row; HOST serves it). | decisions/host.md:304 |
| ## HOST-16 · the Store key is an integrity-at-rest key (2026-10-16; ROOT ruled the custody) | decisions/host.md:306 |
| **Status.** ruled by ROOT 2026-10-16. | decisions/host.md:324 |
| ## HOST-17 · `log` pages from an index the base carries (2026-10-16, HOST-3) | decisions/host.md:326 |
| **Status.** open; measured as a count and answered by HOST-30 (2026-10-17). | decisions/host.md:346 |
| ## HOST-18 · a segment is bound to its base by the tag already on disk: `foreignSegment` (2026-10-17, BUILD-TRANSPORT; ASSEMBLY-transport-consent, with HOST-4) | decisions/host.md:348 |
| **Status.** landed (this commit). Re-genesis: every Store; a pre-HOST-18 base refuses `foreignSegment`. | decisions/host.md:389 |
| ## HOST-19 · the fuel restart reopens in process; the loop holds no frame between batches; the resident is never silent (2026-10-17, HOST-4; OPS D4 + D8's startup half) | decisions/host.md:391 |
| **Status.** landed (written by HOST-4, compiled, fixed and landed by HOST-5 on hbox). | decisions/host.md:454 |
| ## HOST-20 · the shape stamp: a base names the codec shapes it was written under, and an old shape refuses by name (2026-10-17, HOST-5; D2, agreed with CODEC-2) | decisions/host.md:456 |
| **Status.** landed (this commit). | decisions/host.md:502 |
| ## HOST-21 · `lookup` of a dead call answers `refused expired`, final by `absent_final`; adopt's genesis check is PROTOCOL's and suffices (2026-10-17, HOST-5; closes HOST-8's debt and HOST-3's adopt ask) | decisions/host.md:504 |
| **Status.** landed (this commit). | decisions/host.md:541 |
| ## HOST-22 · (SUPERSEDED: the turn cadence and `tailTooManyTurns` are deleted, see the amendment below) the unsealed tail was bounded in TURNS (2026-10-17, HOST-5; PERF's verifies-per-open) | decisions/host.md:543 |
| **Status.** landed (5582991); SUPERSEDED by the amendment below. Alternative (a) is raised with ROOT. | decisions/host.md:585 |
| ## HOST-23 · a follower tail over the one open: `Host.Tail` (2026-10-17, HOST-5; HOSTING-7's ask) | decisions/host.md:609 |
| **Status.** landed (this commit). | decisions/host.md:648 |
| ## HOST-24 · D8 on the Host side: STATUS at open, seal and exit; no Tally (2026-10-17, HOST-5) | decisions/host.md:650 |
| **Status.** landed (this commit). | decisions/host.md:664 |
| ## HOST-25 · open binds the segment's ORIGIN frame to the base's World: `corrupt` at 0, `foreignOrigin` (2026-10-17, HOST-6; OPS's `corrupt history` finding, built after KERNEL-24) | decisions/host.md:666 |
| **Status.** designed (51515fa); landed after KERNEL-24 (9e91ede) as specified, with these facts | decisions/host.md:754 |
| ## HOST-26 · the pinned base digest has its own customization string (2026-10-17, BUILD-TRANSPORT; scout C1's finding) | decisions/host.md:772 |
| **Status.** landed. Re-emit: every pin (out of band). | decisions/host.md:783 |
| ## HOST-27 · `host` ignores SIGXFSZ, so a write past the file-size limit is `uncertain`, never a signal death (2026-10-17, HOST-6; OPS-2's live finding) | decisions/host.md:785 |
| **Status.** landed (this commit). | decisions/host.md:819 |
| ## HOST-28 · HOST's answer to OPS-P1 (state carry): ACCEPT the two verbs, AMENDED: one stamped artifact, a required digest, the one genesis path; the carried shape is stamped, not promised stable (2026-10-17, HOST-6) | decisions/host.md:821 |
| **Status.** proposed answer to OPS-P1. HOST builds the verbs once KERNEL-6 and CODEC-2 land `carried`. | decisions/host.md:885 |
| ## HOST-29 · a batch record states each Turn's ROOT: `List (Turn × root)`, no end chain; open checks every root by admission (2026-10-17, HOST-6; KERNEL-23's World port, with KERNEL-6/7, CODEC-2/3, PROTOCOL-6) | decisions/host.md:887 |
| **Status.** built against main 4777611 + kernel7-r4 + CODEC-2's codec2-trie-r3. host-sim and | decisions/host.md:943 |
| ## HOST-30 · the index is its own append-only file, one page per seal: a seal writes only the entries since the last base (2026-10-17, HOST-7; HOST-17's count defect, ROOT's framing) | decisions/host.md:947 |
| **Status.** RULED BUILD by ROOT (2026-10-17, six conditions) and BUILT (HOST-7). What is in the tree: | decisions/host.md:1027 |
| ## HOST-31 · a page reads back as written, and a seal appends where its page is framed: `entryUnfit`, `indexMoved` (2026-10-18, HOST-8; HOST-30's law-6 read, items (a) and (b)) | decisions/host.md:1055 |
| ## HOST-32 · what a live backup in `backupOrder` guarantees: it opens to its base with at least the live records, or refuses by name (2026-10-18, HOST-8; HOST-30's law-6 read, item (c)) | decisions/host.md:1132 |
| ## HOST-33 · HOST-14 at size, as counts: the seal bound holds once stated correctly; open reads O(history) of index.log, so open must stop reading it (2026-10-18, HOST-8; ROOT's framing of HOST-14's re-check: counts, no timing) — RULED BUILD by ROOT (five conditions), BUILT by HOST-9 | decisions/host.md:1190 |
| ## HOST-34 · HOST-28 BUILT: `host export` / `host import --digest` (2026-10-18, HOST-8; after KERNEL-29 b8e0f82 and CODEC-22's carried codec 28b4a38) | decisions/host.md:1444 |
| ## HOST-35 · a Store file absent from an existing STORE directory is `missing FILE`, refused before any handle opens; no open or append creates a Store file, no sync acknowledges bytes in an unlinked one (2026-10-17, HOST-10; HOST-9's named gap, law 7 on the real path; OPS-3 agreed the sentence and the plants) | decisions/host.md:1520 |
| ## HOST-36 · `host import` writes no Store path before every check passed: a theorem over the one decision function (2026-10-17, HOST-10; HOST-28's first named gap) | decisions/host.md:1652 |
| ## HOST-37 · a backup across a writer restart: what HOST-32 left uncovered, proved (2026-10-17, HOST-10; HOST-32's critique, item 1) | decisions/host.md:1708 |
| ## HOST-38 · KERNEL-41 (a′), HOST's half: a record states BOTH roots after each Turn; the journal's invariant holds at every World the writer holds (2026-10-17, HOST-11; with KERNEL-12, CODEC-7, PROTOCOL-7 in ONE kernel! landing) | decisions/host.md:1776 |
| ## HOST-39 · HOST-28's reopen pair, proved: the open of what genesis (or import) writes is the World it was given; and the base bound that omitted the stamp (2026-10-17, HOST-11; HOST-28's second named gap; proof lane a5a9c62bf7f200e53) | decisions/host.md:1854 |
| ## HOST-40 · HOST-28's last gap: `host export` refuses no World the deployed open returns, with the two facts it cannot have named (2026-10-17, HOST-11; proof lane a5a9c62bf7f200e53) | decisions/host.md:1926 |
| ## HOST-42 · KERNEL-44/47, HOST's half: the Host commits through `Receive.judge`, a recorded refusal is a step of the log, and a log position is a STEP count (2026-10-18, HOST-12; with KERNEL-14/15, CODEC-8, PROTOCOL-8 in ONE kernel! landing). Retires HOST-8's "the Host keeps no record of refusals". | decisions/host.md:1978 |
| ## HOST-41 · a follower wrote records its own reopen refuses: a page holds at most one record's steps, and no writer encodes a count its decode refuses (2026-10-17, HOST-11; found by reading, confirmed red by lane a53d31d238840be6e; rebased over the refusals day 38d94e1 by HOST-12, landed after HOST-42) | decisions/host.md:2015 |
| ## HOST-44 · KERNEL-46/48 (rows), HOST's half: the carried state and the base carry rows; `host export` stays complete with no premise (2026-10-18, HOST-12; with KERNEL-17, CODEC-9/10, LANG-14 in ONE kernel! landing) | decisions/host.md:2112 |
| ## HOST-43 · an operator's seal: `host seal STORE` on a stopped writer, the one act the rows' checkpoint and a thin member's adopt both use (2026-10-18, HOST-12; CLIENT-5's finding via ROOT; PROTOCOL-9/10/11 co-sign the rows side; APPROVED by ROOT as proposed, with three conditions, built here). | decisions/host.md:2137 |
| ## HOST-45 · KERNEL-49 (a), path compression in the one trie, HOST's half: no Host code moves; every reopen, backup, seal and export theorem re-verified (2026-10-18, HOST-12; with KERNEL-18, CODEC-11, PROTOCOL-12 in ONE kernel! landing) | decisions/host.md:2169 |
| ## HOST-46 · every World the deployed open returns is in the World codec's domain (`openWith_codecFits`), and a base never names a position it cannot spell (`positionUnfit`) (2026-10-18, HOST-12; cv 01a14e33-3911, HOST-43's two named gaps; proof lane) | decisions/host.md:2181 |
| ## HOST-47 · the record bound is DERIVED, not picked: `recordBytesMax` = 16,779,332 (was 32 MiB), and the torn-tail window halves with it (2026-10-19, HOST-13; HOST-41's critique, HOST-18's "nobody has questioned the 32 MiB") | decisions/host.md:2199 |
| ## HOST-48 · a page's IO error refuses THAT page `pageIo`; the writer serves on (2026-10-19, HOST-13; HOST-35's named edge) | decisions/host.md:2239 |
| ## HOST-49 · HOST-21's adopt argument is a theorem: the reader refuses a record of no steps (`emptyRecord`), so a Store at step 0 holds no record past a base at step 0 (2026-10-19, HOST-13; HOST-21's meta-critique, HOST-11's edge) | decisions/host.md:2281 |
| ## HOST-50 · the readers' named WEAKs of HOST-33..46, each closed or given its trigger (2026-10-19, HOST-13; ROOT's queue item 4) | decisions/host.md:2328 |
| ## HOST-51 · two of HOST-50's kept WEAKs get teeth: host-sim drives the deployed submit through `judge`, and `positionUnfit` has a runtime witness (2026-10-19, HOST-13; ROOT's ask on a2996f7) | decisions/host.md:2358 |
| ## HOST-53 · open's one index check also requires that the base's last entry began before the base's World, so a base at step 0 counts no entry (2026-10-19, HOST-14; HOST-49's named gap, cv 01a14f2a-8c82) | decisions/host.md:2390 |
| ## HOST-54 · the page walker and `host check` refuse a record of no steps, as the open does (2026-10-19, HOST-14; HOST-49's named second readers) | decisions/host.md:2436 |
| ## HOST-52 · `Host.Sock`: THE client end of a Unix stream socket, 156 lines of C beside the Store's, every call bounded, every failure named (2026-10-19, HOSTING-10 for HOSTING-27's resident; HOST-13 agreed with conditions, HOST-14 read the diff; ROOT ruling 10-19) | decisions/host.md:2466 |
| ## HOST-55 · the backup theorems name the `tailTooLong` they refuse with its bound (2026-10-19, HOST-14; ROOT, after the disjunct audit) | decisions/host.md:2529 |
| ## HOST-56 · genesis, join and import refuse a World whose budget this binary does not admit: `allowancePastBound` and `potentialPastBound` (2026-10-19, HOST-14; KERNEL-55, ROOT Q1 = B and Q3; the HOST half, part 1) | decisions/host.md:2541 |
| ## HOST-58 · a recorded refusal adds three refusals entries (KERNEL-55 R1's World total), priced at 96 bytes of its step (2026-10-19, HOST-14; Host half of KERNEL-22's R1 `kernel!`) | decisions/host.md:2595 |
| ## HOST-59 · imported and joined Worlds meet `budget_reaches`' premises: the bound holds at every World this binary creates a Store from (2026-10-19, HOST-14; HOST-56's named gap, cv 01a150ed-7bf7) | decisions/host.md:2611 |
| ## HOST-57 · `worldBytesMax` is derived: 91,914,346 bytes, and every World the writer reaches encodes within it (2026-10-19, HOST-14; KERNEL-55 ROOT Q1 = B and Q5, the HOST half part 2) | decisions/host.md:2625 |
| ## HOST-60 · a page is never stopped for room before it serves: the budget is `eventBytesMax + 5`, and the serve is lifted through `walk` and `build` (2026-10-21, HOST-15; cv 01a150c0, PROTOCOL-18's finding) | decisions/host.md:2669 |
| ## HOST-61 · a page from before the Store's log is refused `beforeLog` by name, never served under steps nobody asked for (2026-10-21, HOST-15; ROOT approved; cv 01a15180-9499, found in HOST-60) | decisions/host.md:2713 |
| ## HOST-62 · every index entry points at its own record: the index-segment coherence, proved; a page short of the tip is non-empty (2026-10-21, HOST-16; cv 01a15180-9499) | decisions/host.md:2751 |
| ## HOST-63 · the open checks the one entry it reads against its record: the base's last entry must name the frame that ends at the base (2026-10-21, HOST-16; cv 01a15180-9499, HOST-53's alternative (d)) | decisions/host.md:2799 |
| ## HOST-64 · the checkpoint mechanism: the segment as files, each opened by a MAC'd header; retention operator-set, default keep-everything; `CheckpointTrusted` named (2026-10-21, KERNEL-44 Part 2, shape D; DECISIONS-20261021 CARD 1; HOST-19 wrote it, HOST-20 compiled and landed it) | decisions/host.md:2850 |
| ## HOST-65 · entry 0 is the Store's first record: the run begins at the origin frame's end, and the open refuses a base counting none anywhere else (2026-10-20, HOST-18; HOST-62's named-not-proved item, HOST-61's entry-0 case) | decisions/host.md:3002 |
| ## HOST-67 · three of HOST-64's follow-ups: `host import --origin` (the pin CheckpointTrusted is stated over), `Segs.read` is the logical extract, and rotate's reuse checks the header (2026-10-20, HOST-19; cv 01a1583d-864c items 1, 2, 4) | decisions/host.md:3025 |
| ## HOST-68 · the index is coherent from its RUN START: a retained Store's kept entries from `indexFrom`, and the first kept entry's step count `s₀` (HOST-65's named gap); `host check` reads it against the oldest kept header (2026-10-20, HOST-22; cv 01a1583d-864c items 3 and 6) | decisions/host.md:3075 |
| ## HOST-69 · the writer-life induction as ONE theorem: `WriterLife` over the abstract events (open, admitted fold, seal) and `writer_life_trusted` (2026-10-20, HOST-22; HOST-64's "NOT PROVED: the writer-life induction as one theorem", cv 01a1583d-864c item 5) | decisions/host.md:3118 |
| ## HOST-70 · HOST-50's five WEAK triggers re-checked against eb7028d: one FIRED (the Tail across a segment rotation) and found an unnamed throw — a reader standing in a file a finite retention unlinked is now refused `missing seg.<o>.log` by name (2026-10-20, HOST-22; HOST-19's queue, the HOST-50 WEAKs vs HOST-64) | decisions/host.md:3139 |
| ## HOST-66 · the writer serves a member's cancel: op 7 carries the tag-2 event's own bytes, and the Host decides it once with `Receive.cancel` (2026-10-20, HOST-18; cv 01a15543-39fd, KERNEL-60's C1, PROTOCOL-23 lands it with the verb and rows) | decisions/host.md:3167 |
| ## HOST-73 · a header-only plant reaches keptHeaders' indexCorrupt from (2026-10-20, CX-HOST; cv 01a158b0-d455) | decisions/host.md:3187 |
| ## HOST-72 · carried join uses the signed origin and nonce through the one importer (2026-10-20, CX-HOST, PROTOCOL-61) | decisions/host.md:3215 |
| ## HOST-71 · atomic adoption selects a fresh segment identity (2026-10-21, CX-HOST, ROOT ruling A) | decisions/host.md:3245 |
| ## HOST-74 · a frame refusal's status is the refusal's own: a frame still queued when the resident stops is `declined stopped`, an undecodable lookup is `declined undecodableCall` as at submit (2026-10-24, FIX-HOST; READ-HOST F1, COLLATION A8) | decisions/host.md:3369 |
| ## HOST-75 · the writer's refinement is about the follower that runs: `host follow`'s `absorb` keeps exactly the page events of an honest log, both ways; `host_run_audits` → `host_run_absorbed` (2026-10-24, FIX-HOST; READ-HOST F2, COLLATION A9) | decisions/host.md:3391 |
| ## HOST-76 · the writer lock is the key file's read handle, held by the `Writer` the loop holds; the five dummy re-locks are deleted, CHARTER law 4 and HOST-19 say so, and a live `host follow` has a lock plant (2026-10-24, FIX-HOST; READ-HOST F3) | decisions/host.md:3415 |
| ## HOST-77 · five Host docs say what the code does: `stepTooLarge` is after the machine, the base layout carries `retainedFrom`/`indexFrom` and the physical trailer, open reads the segment header (not an origin frame), `host seal`'s open also writes, HOST-22's title; `openFollower` (no deployed caller) is deleted (2026-10-24, FIX-HOST; READ-HOST F4, F7, F8, F9, F14) | decisions/host.md:3435 |
| ## HOST-78 · one re-deriver: `Kernel.Receive.audit` is deleted; the follower's event core moves DOWN into the kernel as `Receive.rederive`, which `host follow`, kernel-sim, the journeys and the benches all run; every `audit … = .ok` premise is `World.fold … ∧ Honest …`; two audit-only refusal names are deleted and the Store's shape stamp now names the refusal code table (2026-10-24, FIX-HOST-2; COLLATION A9 remainder, the coordinator's grant to FIX-HOST) | decisions/host.md:3445 |
| ## HOST-79 · Follow compares a self-head post BEHIND its position against its own Store: the chain its kept files hold at the post's step; a mismatch is `refused forkedPost`, the page kept (2026-10-26, RELAND-TRUST; DESIGN-TRUST T2b', cv 01a176ab-14f5; CROSS-LAYER: PROTOCOL owns `Head`, CLIENT the join test) | decisions/host.md:3464 |

### decisions/hosting.md

| Title or status | Location |
|---|---|
| ## HOSTING-0 The row, attacked; and the laws (2026-10-17) | decisions/hosting.md:7 |
| ## HOSTING-3 The grain lifecycle package, as built (2026-10-17) | decisions/hosting.md:52 |
| Status: built. | decisions/hosting.md:110 |
| ## HOSTING-3b A printer in Hosting (2026-10-17) | decisions/hosting.md:112 |
| ## HOSTING-4 KERNEL's `invoke` is default-open; the law is the only owner check (finding, 2026-10-17) | decisions/hosting.md:124 |
| ## HOSTING-5 The grain package after LANG ID-1 and KERNEL-25 (2026-10-17) | decisions/hosting.md:143 |
| ## HOSTING-6 The plan, as built (ASSEMBLY HOSTING-5) (2026-10-17) | decisions/hosting.md:192 |
| ## HOSTING-7 The controller's decisions (ASSEMBLY HOSTING-4) (2026-10-17) | decisions/hosting.md:224 |
| Status: decisions built; the exe (tail + frames to `grain-launch`) waits on HOST's tail API and | decisions/hosting.md:255 |
| ## HOSTING-8 The controller ↔ launcher frames (`Hosting/Wire.lean`) (HOSTING-2, 2026-10-17) | decisions/hosting.md:258 |
| Status: built. | decisions/hosting.md:310 |
| ## HOSTING-9 Labels are lowercase ASCII; directory names are injective; the printer is LANG's (HOSTING-2, 2026-10-17) | decisions/hosting.md:312 |
| Status: built. | decisions/hosting.md:345 |
| ## HOSTING-10 The controller exe: a pure round over HOST's tail (HOSTING-2, 2026-10-17) | decisions/hosting.md:347 |
| Status: built. | decisions/hosting.md:399 |
| ## HOSTING-11 grain-launch and the physical isolation test (HOSTING-2, 2026-10-17) | decisions/hosting.md:401 |
| Status: built. | decisions/hosting.md:445 |
| ## HOSTING-12 The provider-key broker: Lean writes the request, the window forfeits on restart (HOSTING-3, 2026-10-17) | decisions/hosting.md:447 |
| Status: stage 1 built. Stage 2 (allowances from the World) and stage 3 (the resident plan) are next. | decisions/hosting.md:593 |
| ## HOSTING-13 Allowances in the World: one allowance is one meter (HOSTING-4, 2026-10-18) | decisions/hosting.md:595 |
| ## HOSTING-14 The broker follows the World; `--drive` is deleted (HOSTING-4, 2026-10-18) | decisions/hosting.md:692 |
| ## HOSTING-15 keybroker speaks TLS to the provider; Lean names the host, the operator names the anchors (HOSTING-5, 2026-10-18) | decisions/hosting.md:761 |
| ## HOSTING-16 keybroker's exits are a Lean table (HOSTING-5, 2026-10-18, OPS-2's ask) | decisions/hosting.md:909 |
| ## HOSTING-17 Who may connect to a resident's broker socket, and where it sits (HOSTING-6, 2026-10-18, owed to OPS) | decisions/hosting.md:970 |
| ## HOSTING-19 grain-launch's and its controller's exits are a Lean table (HOSTING-6, 2026-10-18, OPS-3's ask) | decisions/hosting.md:1138 |
| ## HOSTING-20 A resident reaches the World through its own member socket, served by nd (HOSTING-7, 2026-10-18, ROOT ruling; for CLIENT-3's `nd --stdio`) | decisions/hosting.md:1194 |
| ## HOSTING-21 The resident row, and keybroker's socket admits exactly PEER (HOSTING-7, 2026-10-18) | decisions/hosting.md:1247 |
| ## HOSTING-22 The grain row's physical half (HOSTING-7, 2026-10-18, PROTOCOL-7's need) | decisions/hosting.md:1307 |
| ## HOSTING-23 Only a code the table names is passed through; any other is the mechanism's (HOSTING-7, 2026-10-18, OPS-3's burst5 find) | decisions/hosting.md:1345 |
| ## HOSTING-24 grain-launch refuses a missing layout directory at start (HOSTING-7, 2026-10-18, ROOT/OPS-3) | decisions/hosting.md:1391 |
| ## HOSTING-25 The resident reaches the World: a typed MEMBER root, built as HOSTING-20 ruled (HOSTING-8, 2026-10-19) | decisions/hosting.md:1420 |
| ## HOSTING-26 keybroker serves the World's resident grains; `RESIDENTS` is deleted (HOSTING-8, 2026-10-19; HOSTING-18 RULED (A) by ROOT) | decisions/hosting.md:1527 |
| ## HOSTING-29 The resident receives the reply TEXT; Lean reads the provider's JSON (HOSTING-9, 2026-10-19, ROOT ruling on HOSTING-8's three twin traps) | decisions/hosting.md:1604 |
| ## HOSTING-28 The provider's leaf key is pinned, as operator data; the anchors are the provider's roots (HOSTING-9, 2026-10-19; ROOT ruling P2) | decisions/hosting.md:1715 |
| ## HOSTING-27 The real resident: a Lean executable that answers a bell, THE BAR's hosted Hermes (HOSTING-10, 2026-10-19; ROOT rulings 10-19) | decisions/hosting.md:1801 |
| ## HOSTING-31 The resident answers the Bell as a queue: one read per tick, lowest first, the kept ring before any other (HOSTING-11, 2026-10-20; with LANG-58, one `lang!` commit) | decisions/hosting.md:1866 |
| ## HOSTING-32 The residents' members leave the hosted tree: MEMBERS, STATE and the follower sockets under nd's own roots; the stdio child writes its workspace and never a Store (HOSTING-11, 2026-10-20; ROOT cv 01a1507c-7245; OPS-5 agreed to the Ops/Units.lean part) | decisions/hosting.md:1913 |
| ## HOSTING-33 `hosting-residents STORE`: nd-members' decider answers only `residents`, so its unit carries no stand-in clock or key slots (HOSTING-11, 2026-10-20; ROOT, from CLIENT-8's close-out) | decisions/hosting.md:1947 |
| ## HOSTING-34 The resident on LANG-59's Bell: `answer` re-sends the ring's text, exactly-once is the `rings` guard (HOSTING-11, 2026-10-20; one `lang!` with LANG-19) | decisions/hosting.md:1963 |
| ## HOSTING-35 The resident rows run on nd-members: the member socket is served as deployed, and the birth race is planted at it (HOSTING-12, 2026-10-20; HOSTING-30's last row item) | decisions/hosting.md:1976 |
| ## HOSTING-36 The resident's tick is a tree of effects, and their order is a theorem over every path (HOSTING-12, 2026-10-20; HOSTING-27/31 critique item) | decisions/hosting.md:2001 |
| ## HOSTING-37 The three gaps HOSTING-36 named, closed as theorems: the interpreter performs exactly a path; keep and forget are durable and atomic under the volume's stated contract; the restart's seed is what the volume holds (HOSTING-12, 2026-10-20; ROOT) | decisions/hosting.md:2027 |
| ## HOSTING-39 A keep or forget that failed part way is resumed at the restart: the start re-runs a whole keep (or forget) of what the volume holds before its first tick, so nothing a new life acts on can be undone by a crash (HOSTING-13, 2026-10-21; ROOT's item, HOSTING-37's named gap) | decisions/hosting.md:2084 |
| ## HOSTING-38 A crash-loop window passes without a Turn: grain-launch reports its clock (`tick`, every `tickMs`), and the controller relaunches a crash-looped grain in the round whose clock passes its window (HOSTING-13, 2026-10-21; ROOT ruled (B) with conditions) | decisions/hosting.md:2142 |
| ## HOSTING-17 ADDENDUM · Ember ratified the custody fence as built (2026-10-21; ROOT for HOSTING, no HOSTING lane live; cv 01a155a1-f440; OPS-6 wrote it) | decisions/hosting.md:2207 |
| ## HOSTING-40 The two-uid fence, run for real: three refutations of HOSTING-17 on its first run as `nd` and `nd-hosted` (HOSTING-15, HOSTING-16, 2026-10-21; ROOT rulings 10-21; OPS-6 agreed to the UMask lines; ROOT for CLIENT to the nd-bwrap comment) | decisions/hosting.md:2247 |
| ## HOSTING-41 The member socket waits for the follower's command loop, not its supervisor's bind (2026-10-20, CX-HOSTING) | decisions/hosting.md:2270 |
| ## HOSTING-42 · The member socket: an `ok` answer is committed on the member's own World, under one premise about bytes (2026-10-23, CX-E2-2; E2b, R-0052/R-0058/R-0062/R-0065; promo/IMPACT-E2.md §1, §5; promo/READ-E2-grok.md, promo/READ-E2b-grok.md) | decisions/hosting.md:2292 |
| ## HOSTING-43 · The member socket, strong form: the delivered answer IS the resident's datum (2026-10-23, CX-HOST2; R-0065, R-0069; HOSTING-42's three triggers, KERNEL-64's finding) | decisions/hosting.md:2315 |
| ## HOSTING-44 · The answered row is the kept answer: the deployed Bell as a witness, joined to the strong socket (2026-10-23, CX-BELL; R-0069; HOSTING-43 (e), cv 01a167fe-5e84) | decisions/hosting.md:2347 |
| ## HOSTING-45 · The configured bell is the Bell: the resident checks the package it is about to serve, by its bytes (2026-10-23, CX-BACKLOG-2; cv 01a16821-5842, HOSTING-44's critique; R-0069) | decisions/hosting.md:2407 |
| ## HOSTING-46 · An abandoned ring does not stall the resident's queue: measured, and stated (2026-10-23, CX-BACKLOG-2; closes cv 01a1682e-7f9d, filed by CX-DEADLINE at LANG-76; R-0069) | decisions/hosting.md:2429 |
| ## HOSTING-47 · The journal join is bounded by follow's own frames: `journal_committed` and `answered_row_committed` restated over an explicit path (2026-10-24, FIX-HOSTING; readers/COLLATION-20261024 §A5, READ-HOSTING D1; R-0069, R-0071) | decisions/hosting.md:2461 |
| ## HOSTING-48 · No refusal repeats forever: every retry the resident schedules is counted, and `retriesMax` of them in a row end it `retryExhausted` by name (2026-10-24, FIX-HOSTING; COLLATION §A13, READ-HOSTING D3 and B4, B8; answers HOSTING-46's question; R-0069, R-0071) | decisions/hosting.md:2485 |
| ## HOSTING-49 · What the member says is decoded once, refused by name when it is not text, and checked to describe the configured bell (2026-10-24, FIX-HOSTING; COLLATION §A14, READ-HOSTING D2, Q4, B1, B3, B5, B6; R-0069, R-0071) | decisions/hosting.md:2513 |
| ## HOSTING-50 · The `stdio-leg` trust row is four trusts; the one that was a theorem away is now a theorem (2026-10-24, FIX-HOSTING; COLLATION §A20, READ-HOSTING Q1; R-0069, R-0071) | decisions/hosting.md:2539 |
| ## HOSTING-51 · The reply reader's fuel and depth are theorems, not 12 GB teeth: `Hosting.Proofs.Reply` builds in 1.6 GB (2026-10-24, FIX-REPLY; READ-HOSTING law 9, the Reply item; cv 01a16fec-e804) | decisions/hosting.md:2564 |
| ## HOSTING-52 · A real model answers the Bell: the deployed resident through keybroker, THE PIN and the Anthropic API, as an opt-in row that reads the receipt and the budget (2026-10-26, FABLE-AGENT; `redregg/work/promo/DESIGN-AGENT.md` A0, §1) | decisions/hosting.md:2599 |
| ## HOSTING-53 · The Bell is the agent's inbox: a ring carries an AIM and `answer` delivers the text to the aim's target as one typed nested call in the same Turn; the first target is the document's section, whose candidate is withdrawn by name when the Bell's grant is revoked (2026-10-26, FABLE-AGENT-2; `redregg/work/promo/DESIGN-AGENT.md` A1, §4, §6) | decisions/hosting.md:2620 |

### decisions/kernel.md

| Title or status | Location |
|---|---|
| ## KERNEL-3 · ROM cells are content-addressed; a package's identity IS its cell id (2026-10-16) | decisions/kernel.md:3 |
| Status: open (LANG to confirm LANG-5 identity = `romIdOf`). | decisions/kernel.md:14 |
| ## KERNEL-4 · Receive: one derivation per kind over a pinned view, ending in a sealed Turn (2026-10-16) | decisions/kernel.md:16 |
| Status: open. | decisions/kernel.md:38 |
| ## KERNEL-5 · Answers: LANG law refusals, PROTOCOL refusal names (2026-10-16) | decisions/kernel.md:40 |
| Status: open. | decisions/kernel.md:48 |
| ## KERNEL-6 · Members, keys, rotation, rights, data objects, follow grants, audit (2026-10-16) | decisions/kernel.md:50 |
| Status: open. | decisions/kernel.md:75 |
| ## KERNEL-7 · A retry is `replayed` by transaction id alone; `Receive.submit`; the Sim (2026-10-16) | decisions/kernel.md:77 |
| Status: open. | decisions/kernel.md:97 |
| ## KERNEL-8 · Answers to CODEC-7 and CODEC-0 (2026-10-16) | decisions/kernel.md:99 |
| Status: open. | decisions/kernel.md:108 |
| ## KERNEL-9 · Frame, ROM-forever, nullifiers-once, reopen determinism; the kernel's waste rows (2026-10-16) | decisions/kernel.md:110 |
| Status: open. | decisions/kernel.md:125 |
| ## KERNEL-10 · Answers to LANG's three asks (proposals/lang.md) (2026-10-16) | decisions/kernel.md:127 |
| Status: open. | decisions/kernel.md:140 |
| ## KERNEL-11 · A Turn names each cell once: `touches` replace pins, legs and retires (KERNEL-2, 2026-10-16) | decisions/kernel.md:142 |
| Status: open. | decisions/kernel.md:172 |
| ## KERNEL-12 · A turn's charge is its storage; one aggregate bound, `weightMax` (KERNEL-2, 2026-10-16) | decisions/kernel.md:174 |
| Status: open. | decisions/kernel.md:197 |
| ## KERNEL-13 · Answers: PROTOCOL-4 `rederive`, HOST-8 `absent_final`, HOST's `fold ↔ foldlM`, `mayFollow` (KERNEL-2, 2026-10-16) | decisions/kernel.md:199 |
| Status: open. | decisions/kernel.md:222 |
| ## KERNEL-14 · Answers: CODEC's counter widths, CLIENT-11's signature (KERNEL-2, 2026-10-16) | decisions/kernel.md:224 |
| Status: open (signature scheme: ROOT). | decisions/kernel.md:244 |
| ## KERNEL-15 · Storage is one World budget; no refill in v0, credit on retirement is the next step (KERNEL-2, 2026-10-16) | decisions/kernel.md:246 |
| Status: credit BUILT as KERNEL-19 (exact; writes too). Refill: a grant, later (ROOT). | decisions/kernel.md:262 |
| ## KERNEL-16 · Open sponsoring is wrong as stated: the sponsor does NOT pay (KERNEL-2, 2026-10-16) | decisions/kernel.md:264 |
| Status: RULED (one mechanism) and BUILT as KERNEL-20. | decisions/kernel.md:278 |
| ## KERNEL-17 · The journal is not pruned (KERNEL-2, 2026-10-16) | decisions/kernel.md:280 |
| Status: SUPERSEDED by KERNEL-33 (the journal IS pruned to the window: `kept`, `pruneJournal`; a call's | decisions/kernel.md:292 |
| ## KERNEL-18 · `worldBytesMax` is the genesis budget; the theorem is `fold_world_weight` (KERNEL-2, 2026-10-16) | decisions/kernel.md:296 |
| Status: open. | decisions/kernel.md:314 |
| ## ROOT rulings on KERNEL-14..17 (2026-10-16, recorded by KERNEL-2) | decisions/kernel.md:316 |
| ## KERNEL-19 · Credit on retirement, exact: storage is CONSERVED (KERNEL-3, 2026-10-16) | decisions/kernel.md:329 |
| Status: built (ROOT may narrow it to retires only by deleting one term). | decisions/kernel.md:361 |
| ## KERNEL-20 · Enrolment is a right; one grant kind; the World is a grant target (KERNEL-3, 2026-10-16) | decisions/kernel.md:363 |
| Status: built. | decisions/kernel.md:410 |
| ## KERNEL-21 · Every World grant is rooted at genesis, as a fold invariant (KERNEL-3, 2026-10-16) | decisions/kernel.md:412 |
| Status: built. | decisions/kernel.md:438 |
| ## KERNEL-22 · Tooling is not deployed: SIZE.md's deployed row excludes it, and C9 keeps it out of deployed imports (KERNEL-4, 2026-10-16) | decisions/kernel.md:440 |
| Status: built. | decisions/kernel.md:463 |
| ## KERNEL-23 · An authenticated cell root: the World's cell map IS a canonical binary Merkle trie, and the chain commits its root (KERNEL-4, 2026-10-16; DESIGN, BUILT as KERNEL-30) | decisions/kernel.md:465 |
| Status: BUILT as KERNEL-30 (the World is one canonical trie of cells and nullifiers, its root in the | decisions/kernel.md:570 |
| ## KERNEL-24 · A call names its World: `Unsigned.world` = the World's genesis ORIGIN, refused `wrongWorld` before anything else; genesis commits to everything it was made from (KERNEL-4, 2026-10-17; DESIGN, ROOT's D3, BUILT: `Receive.receive`'s first check, `receive_wrongWorld`) | decisions/kernel.md:582 |
| Status: BUILT (KERNEL-5, 10-17). As built: the origin is H(domOrigin, CODEC raw bytes of (name, nonce, | decisions/kernel.md:628 |
| ## KERNEL-25 · `invoke` is authorized like write: the owner, or a chain for `invoke m` rooted at the owner (KERNEL-4, 2026-10-17; ROOT's ruling on HOSTING-4, BUILT: `Receive.invoke` through `ownerAuthority … (.invoke m)`) | decisions/kernel.md:640 |
| Status: BUILT (KERNEL-5): invoke via ownerAuthority, theorem invoke_authorized; Sim arms invoke-owner:ok, invoke-no-grant:noGrant; plant principalOf in invoke ⇒ 56/64 seeds red. | decisions/kernel.md:663 |
| ## KERNEL-26 · Public objects: a grant whose grantee is the World means "any enrolled member" (KERNEL-4, 2026-10-17; ROOT ruled, BUILT: the World grantee in `Authority.lean`, kernel-sim `invoke-public:ok`) | decisions/kernel.md:665 |
| Status: BUILT (KERNEL-5): granteeHolds in walk (one disjunct), checkGrantee in grant, theorem granteeHolds_ok; Sim arms invoke-public:ok, invoke-public-method-1:grantRight; plant World disjunct off ⇒ red. A public grant is USED, never re-delegated: `walk` honours a World grantee only at the FIRST link (`pub`), and `checkParent` keeps requiring the parent grantee = the signer exactly, so the two agree on one shape (ROOT/review 10-17 named the disagreement; I chose the narrow side because the wide one let any member carve a public enrol pool into a private grant). Sim arm carve-public:noGrant. A public ENROL pool (a World-grantee grant carrying enroll n) is possible and is stated on enroll_authorized. Theorems added after review: invoke_stranger_noGrant (the refusal BY NAME), ownerAuthority_program_free (the laws only refine: the gate never reads the program). | decisions/kernel.md:680 |
| ## ROOT rulings on KERNEL-24..26 and LANG-19 (2026-10-17, recorded by KERNEL-4) | decisions/kernel.md:682 |
| ## KERNEL-27 · LANG-19 as built: `law` judges the incoming laws over the state as `.adopt`, a fifth Occasion. ROOT's LANG-19 wording was overruled by KERNEL-5's finding, and `.adopt` was chosen over the `.birth` conflation (KERNEL-5, 2026-10-17; ROOT ruled `.adopt` the same day) | decisions/kernel.md:690 |
| Status: built with the LANG half (LANG-4). | decisions/kernel.md:698 |
| ## KERNEL-28 · KERNEL's answer to LEDGER-5 (with LANG-4's LANG-23 asks): (a)(b)(c) ACCEPTED, (d) AMENDED to keyed account ids (KERNEL-5, 2026-10-17) | decisions/kernel.md:701 |
| ## KERNEL-30 · KERNEL-23 part 2 as built: the World IS one trie of cells and nullifiers; the root after each turn is in the chain (KERNEL-6, 2026-10-17) | decisions/kernel.md:750 |
| ## KERNEL-31 · genesis refuses by name outside `GenesisFits`, and every kernel World's cells fit | decisions/kernel.md:833 |
| ## KERNEL-32 · A turn's weights are the codec's byte counts: `Turn.logWeight` is the record's size, `Cell.weight` a cell's bytes (KERNEL-8, 2026-10-17) | decisions/kernel.md:889 |
| ## KERNEL-33 · The journal is pruned to the window: bounded, every answer it gives true, and a call admitted at most once (KERNEL-8, 2026-10-17; ROOT-approved, from HOST-7's HOST-17 measurement) | decisions/kernel.md:931 |
| ## KERNEL-29 as built · carry state by re-genesis: `Carried`, `Receive.carry`, one tagged origin (KERNEL-8, 2026-10-17; OPS-P1 as agreed by OPS-2, PROTOCOL-6, HOST-6, CODEC-2/3; after KERNEL-33) | decisions/kernel.md:1012 |
| ## KERNEL-34 · The phone's read takes the leaf's bytes: KERNEL-31's last premise, discharged by CODEC's leaf decoder (KERNEL-8, 2026-10-17; CLIENT-16, ROOT-accepted) | decisions/kernel.md:1078 |
| ## KERNEL-35 · The empty subtree's digest is hashed at most once per turn: one lazy copy handed down the mutation path (KERNEL-9, 2026-10-18; cv 01a1498e, KERNEL-8's handoff item 1) | decisions/kernel.md:1097 |
| ## KERNEL-36 · The trie hash rows are INSTRUMENTS: kernel-sim counts the calls the real admission makes (KERNEL-9, 2026-10-18; ROOT ruling on KERNEL-35's critique) | decisions/kernel.md:1147 |
| ## KERNEL-37 · `Env.Lawful`: what the kernel's theorems assume of an `Env`, in one premise, proved at the deployed codec (KERNEL-9, 2026-10-18; agreed CODEC-3 / KERNEL-7, KERNEL-8's handoff item 2) | decisions/kernel.md:1182 |
| ## KERNEL-38 · All the prunes of a history are one prune of the journal that never forgot: `fold_journal_filter`, and pruning changed no check in a real fold (KERNEL-10, 2026-10-18; KERNEL-33's Critique, KERNEL-9's handoff item 1) | decisions/kernel.md:1224 |
| ## KERNEL-39 · A decoded base carries `JournalOk`: `journalFits`, the kernel's half of CODEC's `kernel/journal` refusal (KERNEL-10, 2026-10-18; KERNEL-33 Critique (b), agreed with CODEC-6) | decisions/kernel.md:1295 |
| ## KERNEL-40 · Ids are names: a carried World keeps its members' ids, and a carry changes no authority (KERNEL-10, 2026-10-18; ROOT's item from OPS-2's OPS-1 critique, agreed with PROTOCOL-6) | decisions/kernel.md:1348 |
| ## KERNEL-41 · The journal is the trie's third slot kind: one authenticated map, canonical by construction, pruned by a canonical `retain` (KERNEL-11, 2026-10-17; cv 01a14ac8-1db6, GATES-3's law-6 read via CODEC-30; DESIGN, not yet built) | decisions/kernel.md:1416 |
| ## KERNEL-42 · Every message a member key signs begins with its own domain: a call's signature is over `callMessage = domCall ‖ unsignedBytes` (PROTOCOL-7 for KERNEL-11, 2026-10-17; CODEC-6's finding, ROOT ruling) | decisions/kernel.md:1709 |
| ## KERNEL-43 · What bounds the allowance is storage PLUS allowance: genesis, carry and the World codec check the sum, and every reached World keeps it below 2^64 (KERNEL-13, 2026-10-18; cv 01a14ba9-cbf4, HOST-11's proof lane, ROOT ruling) | decisions/kernel.md:1731 |
| ## KERNEL-44 PROPOSED · A refusal is a recorded system interaction, bounded per member per window; replay is bounded by a checkpoint rule (KERNEL-13, 2026-10-18; Ember's call (8) of 10-17: "they WERE system interactions", "the amount of replay is too damn high"). DESIGN ONLY until ROOT rules; the HOST half is for HOST-12. | decisions/kernel.md:1772 |
| ## KERNEL-45 PROPOSED · A Turn is the hyperedge for ONE signer; multi-signer and cross-World joint turns are DEFERRED with triggers (KERNEL-13, 2026-10-18; ROOT, from MINI-CONCEPTS-IN-NANO-20261018.md §4 and its closing half-page). Decision only; no code. | decisions/kernel.md:1891 |
| ## KERNEL-46 · LANG-44's kernel half, CO-SIGNED with five amendments, and LANG-45's (ii) capped sum ACCEPTED into it (KERNEL-13, 2026-10-18; LANG-44 items 6–11 and (c), as ROOT approved them; LANG-45 (ii) for ROOT's ruling). Design; the kernel half is built after KERNEL-44's refusals day. | decisions/kernel.md:1917 |
| ## KERNEL-47 · KERNEL-44's refusals as built: ONE fold over steps, a step counter, and seven amendments to the proposal (KERNEL-14, 2026-10-18; ROOT's question "World.fold over Step vs a second fold", settled before building) | decisions/kernel.md:1989 |
| ## KERNEL-48 · The rows day's signatures, in code and staged (KERNEL-15, 2026-10-18; KERNEL-46 as co-signed, LANG-44 (c) with ROOT's range-read conditions) | decisions/kernel.md:2079 |
| ## KERNEL-49 PROPOSED · A row insert costs 564 hashes because the one trie is uncompressed, not because rows are in it: compress the one trie (K17-K49 for KERNEL-17, 2026-10-18; ROOT's ruling on WASTE `hashes-per-row-insert` 564.071). DESIGN ONLY until ROOT rules. | decisions/kernel.md:2116 |
| ## KERNEL-50 · A refusal's record names its member, and a World's window counts are a function of its records: `refusalsCounted` (KERNEL-19, 2026-10-19; cv 01a14da3-3e7a, CODEC-8's reviewer (C) deferred by KERNEL-14; ROOT ruled the per-member form) | decisions/kernel.md:2313 |
| ## KERNEL-51 (PROPOSED, then BUILT: see AS BUILT below, which corrects this text) · The frame rule as one scheme: `Kernel/Proofs/Logic/Frame.lean` (KERNEL-19, 2026-10-19; ROOT, from PROOF-TECHNIQUE-20261019.md §3–4). DESIGN ONLY until ROOT rules. | decisions/kernel.md:2381 |
| ## KERNEL-52 (PROPOSED, then BUILT: see AS BUILT below, which corrects this text) · The head-read family as ONE authenticated-map scheme over `Trie.Spec`, instantiated per trie (KERNEL-19, 2026-10-19; ROOT, PROOF-TECHNIQUE §4.1 item 3). DESIGN ONLY. | decisions/kernel.md:2422 |
| ## KERNEL-53 · One signature verify per judgement: `judge` carries `submit`'s passing verify into the authentication (KERNEL-20, 2026-10-19; PERF-1 FINDING 3, routed by ROOT) | decisions/kernel.md:2504 |
| ## KERNEL-54 (PROPOSED) · Honest contention must not spend the spam budget: the shape of the refusal budget for `stale` (KERNEL-20, 2026-10-19; PERF-1 FINDING 2, cv 01a14edf-6f12; attempt-side meaning co-signed by PROTOCOL-15). DESIGN ONLY until ROOT rules. | decisions/kernel.md:2542 |
| ## KERNEL-54 RULED (ROOT, 2026-10-19, on the measurement): shape N as a varint, W0, all three amendments | decisions/kernel.md:2597 |
| ## KERNEL-54 AS BUILT (KERNEL-20 phase 1 by K20-K; KERNEL-21 phase 2, 2026-10-18) · ROOT's further rulings, the partners' halves, and what the proofs changed | decisions/kernel.md:2627 |
| ## KERNEL-56 · Every hash escape names its inputs: `Collision`, `Trie.Coll` and `HashColl` are deleted, and every consumer concludes `CollidesAmong hash S` over a list S built from its own objects (KERNEL-21, 2026-10-18; found by the KERNEL-54 proof lane, cv 01a1501e-d6bc; ROOT-ruled) | decisions/kernel.md:2640 |
| ## KERNEL-55 (PROPOSED; RULED and BUILT below, parts 1 and 2) · A create's bytes, and what `worldBytesMax` protects: one potential theorem, a derived bound, and two writer paths that reach it today (KERNEL-20 / K20-P55, 2026-10-19; PERF-2's item-2 lead, routed by ROOT; HOST-14 to co-sign). DESIGN ONLY until ROOT rules. | decisions/kernel.md:2648 |
| Status: PROPOSED. | decisions/kernel.md:2819 |
| ## KERNEL-55 RULED (ROOT, 2026-10-19) and AS BUILT, part 1: the potential (KERNEL-21) | decisions/kernel.md:2821 |
| ## KERNEL-55 AS BUILT, part 2: the refusals trie is bounded by the kernel (R1; lane r1 of KERNEL-21/22) | decisions/kernel.md:2827 |
| ## KERNEL-51 AS BUILT, the locality half: `check_local` (cv 01a14f65-48ec; K22-LOCAL, finished by KERNEL-23) | decisions/kernel.md:2869 |
| ## KERNEL-57 · KERNEL-6 CLOSED as built (option (a), KERNEL-27/LANG-24): `law_judged` names what adoption judges (KERNEL-24, 2026-10-21; ROOT ruled on SCHOLAR-COMPARE §1, docs/record/COMPARE-20261021.md) | decisions/kernel.md:2877 |
| ## KERNEL-58 AS BUILT · Q1, the receivers' contract and the call-level frame (KERNEL-27 lane, Ember 10-21 on PROOF-ENGINEERING-20261021 §2.1/§4) | decisions/kernel.md:2888 |
| ## KERNEL-59 AS BUILT · Q3's kernel half: one object-history lift over every body kind (KERNEL-28 lane, PROOF-ENGINEERING-20261021 §2.3/§4 Q3) | decisions/kernel.md:2907 |
| ## KERNEL-60 · Counted value rights in the grant (KERNEL-28's amount right, with credit) and the CANCEL record (design C1), re-priced after KERNEL-54; `rotate_stales_outstanding` (KERNEL-24, 2026-10-21; ROOT ruled on SCHOLAR-COMPARE §2–3) | decisions/kernel.md:2922 |
| ## KERNEL-61 AS BUILT · A counted right's cap provably falls: `LedgerContiguous`, the grant totality, and the read-back (KERNEL-30 lane, for LEDGER-7's `grant_moves_le_cap`, 2026-10-22) | decisions/kernel.md:3036 |
| ## KERNEL-62 · Whole-trie root binding (CX-KERNEL, 2026-10-20; cv 01a15849-3ae0) | decisions/kernel.md:3058 |
| ## KERNEL-63 · Retired heads join the rows overlay's seal (CX-KERNEL, 2026-10-20; cv 01a1553a-c095) | decisions/kernel.md:3110 |
| ## KERNEL-64 · An object's head is fixed under the follower's fold (CX-KERNEL, 2026-10-23; cv 01a166f9-c61c, HOSTING-42 trigger (ii)) | decisions/kernel.md:3180 |
| ## KERNEL-65 · A written row reads back on the World that admits it (CX-BACKLOG, 2026-10-23; cv 01a16821-5828, HOSTING-44's first gap; method R-0069) | decisions/kernel.md:3206 |
| ## KERNEL-66 · The pins are compared before the receivers: a stale call is declined `stale`, never judged on the World as it is now (FIX-KERNEL, 2026-10-24; COLLATION-20261024 A1, READ-KERNEL D1; method R-0069) | decisions/kernel.md:3223 |
| ## KERNEL-75 · `install` is a call an object may make: a method's returned `install` is derived as the object through the one install receiver, checked as a member's (2026-10-26; FABLE-META; with LANG-86; CROSS-LAYER: LANG owns the generator, KERNEL the arm; design `redregg/work/promo/DESIGN-META.md`) | decisions/kernel.md:3253 |
| ## KERNEL-67 · The kernel memo's documentation debt: comments and decision entries that said the opposite of the code (FIX-KERNEL, 2026-10-24; READ-KERNEL B2, B3, B4, B7; method R-0069) | decisions/kernel.md:3267 |
| ## KERNEL-68 · The meter: a Turn names its member and its ticks, and the kernel counts a member's ticks per window as it counts refusals — the second KIND of one typed window trie (FABLE-OBS, FABLE-OBS-2, 2026-10-26/27; DESIGN-OBS §1, redregg/work/promo/DESIGN-OBS.md; FRONTIER-AXES axis 4) | decisions/kernel.md:3283 |
| **Status.** landed as `kernel!:` (FABLE-OBS.report.md holds the hash and the judge's map lines). | decisions/kernel.md:3396 |
| ## KERNEL-69 · The authority is fixed at genesis: `Authority {certifiers, threshold}` is a genesis input, committed in the origin (`domOrigin` v3) and carried in the World as one ROM cell at its content id (2026-10-26; FABLE-TRUST-4; CROSS-LAYER: PROTOCOL owns the start codec and `genesisLeaf`, HOST the `host genesis` options; design `redregg/work/promo/DESIGN-TRUST.md` §1.2, §4.3, BUILT-4; with PROTOCOL-77) | decisions/kernel.md:3397 |

### decisions/lang.md

| Title or status | Location |
|---|---|
| ## LANG-8 A law returns a verdict, not a Bool (2026-10-16) | decisions/lang.md:8 |
| ## LANG-9 Package identity is KERNEL's `romIdOf` of the package cell (2026-10-16; answers KERNEL-3) | decisions/lang.md:20 |
| ## LANG-10 The stack bound is a consensus constant, not part of a budget (2026-10-16) | decisions/lang.md:30 |
| ## LANG-11 The object's state is a record type; field i lives at slot `stateBase + i` (2026-10-16) | decisions/lang.md:40 |
| ## LANG-12 Methods are indexed; their shape is fixed (2026-10-16) | decisions/lang.md:52 |
| ## LANG-13 The v1 fork: cross-object calls (2026-10-16, open) | decisions/lang.md:62 |
| ## LANG-14 LANG owns the recursive codec until CODEC has a recursive combinator (2026-10-16) | decisions/lang.md:73 |
| Status: CLOSED by LANG-17 (the hand readers are deleted). | decisions/lang.md:80 |
| ## LANG-15 No Mathlib (2026-10-16; GATES-1 not challenged) | decisions/lang.md:82 |
| ## LANG-16 Loading a closure re-checks every package in it (2026-10-16; amends LANG-5) | decisions/lang.md:86 |
| ## LANG-17 The port onto `Codec.Tree`: terms on the tree, data on the combinators (2026-10-16; closes LANG-14, answers CODEC-9) | decisions/lang.md:98 |
| ## LANG-18 A reference semantics beside the machine; `extend` keeps the old self (2026-10-17) | decisions/lang.md:137 |
| ## LANG-19 The judge is told what it judges: `Req.occasion` (2026-10-16; ID-1, with KERNEL-4) | decisions/lang.md:159 |
| ## LANG-20 The law library: generated core terms, each with a meaning theorem over `BigStep` (2026-10-16; ID-2, ID-3) | decisions/lang.md:199 |
| ## LANG-21 Cross-object calls: effects as data, restated over touches; built with LEDGER's first method-triggered receiver (2026-10-17; ID-9, closes the LANG-13 fork as a design) | decisions/lang.md:280 |
| ## LANG-22 The resident readers: a seed and a method's arguments read as TEXT at the package's types; `#HEX` bytes (2026-10-17; written by PROTOCOL-5 for LANG-3, agreed) | decisions/lang.md:307 |
| **Status.** landed; LANG's successor reviews. | decisions/lang.md:329 |
| ## LANG-23 Effects are `Body` calls in a fixed-arity row; the forwarding check is withdrawn (2026-10-17; LANG-4's answer to LEDGER-5, amends LANG-21 and LANG-3's answer recorded in decisions/kernel.md 1b4135c) | decisions/lang.md:331 |
| **Status.** agreed with LEDGER (sent 2026-10-17); built in the post-D5 `lang!` day with LANG-33's amendment: the fixed eight-slot row is replaced by declared slots. | decisions/lang.md:394 |
| ## LANG-24 The fifth occasion: `adopt laws'` — every Std law states what it does when it is ADDED over existing state (2026-10-17; with KERNEL-5's KERNEL-27, ROOT ruled `.adopt`) | decisions/lang.md:396 |
| **Status.** built (a533d7a), then AMENDED the same day (below). | decisions/lang.md:424 |
| ## LANG-25 An object names accounts by reference, not by hashing: `Req.self` yes, an `accountOf` builtin no (2026-10-17; answers LEDGER-6 (b), PROPOSED to LEDGER-2 for D5) | decisions/lang.md:444 |
| **Status.** agreed (LEDGER-7, 7229d95); built in D5 (kernel, c3c7aa3) and the post-D5 `lang!` day (`acctRefTy` in `callArms`, `(self bytes)` in `reqTy`, bounded by `reqOk`; journey LC3 checks `req.self` is the invoked object). | decisions/lang.md:464 |
| ## LANG-26 The receiver's verdict on a stdlib package is its laws' meaning (2026-10-17; closes LANG-20's chain) | decisions/lang.md:466 |
| **Status.** built. | decisions/lang.md:496 |
| ## LANG-27 Type errors by name and path: `inferE` is the checker, `infer` its `toOption` (2026-10-17; LANG-3's open item 3) | decisions/lang.md:498 |
| **Status.** built. | decisions/lang.md:518 |
| ## LANG-28 One printer: `Lang.Print` (2026-10-17; LANG-3's open item 4, for HOSTING) | decisions/lang.md:520 |
| **Status.** built; the round trip is LANG-29. | decisions/lang.md:546 |
| ## LANG-29 The printer's round trip is a theorem (2026-10-17; LANG-28's next commit) | decisions/lang.md:548 |
| **Status.** built. | decisions/lang.md:584 |
| ## LANG-30 The reader's fuel is nesting depth; a list's length has its own bound (2026-10-17; LANG-29's MEDIUM) | decisions/lang.md:586 |
| **Status.** built. | decisions/lang.md:636 |
| ## LANG-31 One label rule for the wire, the reader and the printer; the reader reads two levels past the wire; every installable package has a text (2026-10-18; LANG-30's critique, vacuity MEDIUM; LANG-6's WIP finished by LANG-8) | decisions/lang.md:638 |
| **Status.** built (this commit). `lang!`: the decoder narrows. Nothing re-emits. | decisions/lang.md:692 |
| ## LANG-32 A binder may not have a reserved name: `reservedBinder` (2026-10-17; LANG-29's vacuity point 8; LANG-31 is the bound alignment, next) | decisions/lang.md:694 |
| **Status.** built. | decisions/lang.md:720 |
| ## LANG-33 A method declares its call slots: k ≤ callsMax, each a sub-sum of `callTy` (2026-10-18; the post-D5 `lang!` day, amends LANG-23's fixed arity) | decisions/lang.md:722 |
| **Status.** built (this commit). Re-ids every package with a method or a law (`reqTy` changed): | decisions/lang.md:778 |
| ## LANG-34 THE BAR's tick row is a ratio: machine ticks per step the program requires, the required count being the size of the reference derivation (2026-10-18; cv 01a14a39-c22e, GATES-2's critique of LANG-33, with PROTOCOL-6 and GATES-2) | decisions/lang.md:781 |
| **Status.** built (this commit). Nothing re-ids: no deployed definition changed. `gates/waste.tsv` | decisions/lang.md:843 |
| ## LANG-35 The install check reads its imports through the loader (2026-10-18; cv 01a14a52-4721, the LANG-31 vacuity read; LANG-2's gap 3) | decisions/lang.md:846 |
| **Status.** built (this commit). Nothing re-ids: no package bytes changed. | decisions/lang.md:896 |
| ## LANG-36 A not-a-digest refusal is tied to the path it names (2026-10-17; cv 01a14a69-5909, the c253 vacuity re-read, LOW) | decisions/lang.md:898 |
| **Status.** built (this commit). Nothing re-ids: proof modules only. | decisions/lang.md:930 |
| ## LANG-37 THE BAR's ratio is above 1 by theorem, and extraction's requirement is what extraction forces (2026-10-17; cv 01a14a87-33b2, the LANG-34 vacuity read) | decisions/lang.md:932 |
| **Status.** built (this commit). Nothing re-ids: proof and tooling modules only. | decisions/lang.md:966 |
| ## LANG-38 Ids are a type: `digest` (2026-10-17; cv 01a14aab-adae, ROOT ruling (ii); the digest `lang!` day) | decisions/lang.md:968 |
| **Status.** built (this commit). Re-ids every package with a method or law; re-genesis. | decisions/lang.md:1049 |
| ## LANG-39 THE BAR's ratio has an extraction tooth (2026-10-17; cv 01a14abb-aa73, the LANG-37 vacuity read; with PROTOCOL-7) | decisions/lang.md:1051 |
| **Status.** built (this commit). Nothing re-ids: tooling and rows only. | decisions/lang.md:1076 |
| ## LANG-40 The required counter is complete: `requiredOf` never refuses fuel on an admitted invoke (2026-10-17; cv 01a14aba-1281, LANG-37's critique (1)) | decisions/lang.md:1078 |
| **Status.** built (this commit). Nothing re-ids: one new proof module. | decisions/lang.md:1103 |
| ## LANG-41 Every id a run holds came from where ids enter; `callsOf`'s `not a digest` is unreachable from checked Lang output (2026-10-17; cv 01a14acf-a188, cv 01a14af1-2132, LANG-38's critique (2) and vacuity LOW (5)) | decisions/lang.md:1105 |
| **Status.** built (this commit). Nothing re-ids: no package, wire or Store shape changed. | decisions/lang.md:1159 |
| ## LANG-42 The one law runner is never stuck on a loaded package's law: extraction makes progress (2026-10-17; LANG-5/6 leftover "runLaw extraction never stuck") | decisions/lang.md:1161 |
| **Status.** built (this commit). Nothing re-ids: one new proof module and a docstring. | decisions/lang.md:1181 |
| ## LANG-43 `Std.stepTo` refuses an ambiguous edge: every declared edge is the one its method takes (2026-10-17; LANG-5/6 leftover "duplicate machine edges", vacuity note) | decisions/lang.md:1183 |
| **Status.** built (this commit). Nothing re-ids: valid inputs produce the same terms. | decisions/lang.md:1202 |
| ## LANG-44 Relations: keyed, bounded rows under an object, in a third instance of the one trie; inserts at distinct keys commute because their footprints are disjoint, never because a pin is relaxed (2026-10-18; PROPOSED, LANG-13 with a KERNEL half for KERNEL-13 to co-sign; Ember's delvetalk question; DELVETALK-LEARNINGS §4.2; LANG-1's critique) | decisions/lang.md:1204 |
| **Status.** PROPOSED. Sent to ROOT and KERNEL-13 before any code. | decisions/lang.md:1428 |
| ## LANG-45 The deciding experiment: Mini's CappedTally ported by hand to nano's core; what it needs first is a capped commuting COUNTER, which LANG-44's rows give once the head carries a declared sum (2026-10-18; NANO-VS-MINI §5, ROOT's order on LANG-44; journey rows LT0–LT8) | decisions/lang.md:1430 |
| **Status.** Rows LT0–LT8 built (lang-journey GREEN, including the skip-judge plant). (ii) goes to ROOT as an | decisions/lang.md:1497 |
| ## LANG-46 The digest round trip is a law of the `Ctx`, not a free premise: `Receive.Ctx.Lawful` (2026-10-18; cv 01a14b28-7029, LANG-41's owed item; agreed by KERNEL-12 and KERNEL-13) | decisions/lang.md:1500 |
| **Status.** built (this commit). Nothing re-ids. | decisions/lang.md:1523 |
| ## LANG-47 The list-shaped sample: Mini's CoAuthor ported by hand; three relations are its first need, and its seal needs a RANGE read, which LANG-44 v0 does not have (2026-10-18; ROOT's order after LANG-45; journey rows LS0–LS10) | decisions/lang.md:1525 |
| **Status.** Rows LS0–LS10 built (lang-journey GREEN, including the skip-judge plant). The range read goes to ROOT | decisions/lang.md:1607 |
| ## LANG-48 The pending slot: one Std law family for "a value whose shape is fixed now and which arrives later", with a meaning theorem after breadstuffs' `holeFill_binds_in_circuit` (2026-10-18; PROPOSED, design only; ROOT's queue item from MINI-CONCEPTS-IN-NANO-20261018 §6/§8) | decisions/lang.md:1610 |
| **Status.** PROPOSED (design only, ROOT rules). Build order if approved: after LANG-44 (its rows give the many-slots form). | decisions/lang.md:1675 |
| ## LANG-49 · Relations built: LANG-44's Lang half as ruled (rows, range reads, head sum/cap), against KERNEL-48's signatures (2026-10-18; LANG-14, on the one `kernel!` rows day with KERNEL-16, CODEC-9 and HOST) | decisions/lang.md:1677 |
| ## LANG-50 The authoring surface: a second reader that lowers to the core text `Lang.Read` reads, outside the TCB; with LANG-51, the two core additions it cannot do without (2026-10-18; PROPOSED, design only; LANG-15; DELVETALK-LEARNINGS §4.1/§4.5/§3.1, LANG-0 (c), LANG-45/47/49's measurements) | decisions/lang.md:1740 |
| **Status.** PROPOSED (design only; ROOT rules on LANG-50 and LANG-51 separately). Build order if approved: LANG-51 | decisions/lang.md:1904 |
| ## LANG-52 The Bell: the first package a resident uses that a person wrote in the surface (2026-10-18; LANG-16, with HOSTING-8, who owns the resident process; STAND-INS-20261019 A1/E12) | decisions/lang.md:1984 |
| ## LANG-53 stepTo at run level: the generated method lands where its edge says (2026-10-18; LANG-16; cv 01a14b36-6da2, LANG-43's owed item) | decisions/lang.md:2028 |
| ## LANG-54 Std `quorum` and `windowed` run through the receivers as SURFACE laws (2026-10-18; LANG-16; LANG-12/13's owed journey rows) | decisions/lang.md:2068 |
| ## LANG-55 The receiver-admits chain loses three of its four stated gaps (2026-10-18; LANG-16; LANG-4's vacuity leftovers) | decisions/lang.md:2099 |
| ## LANG-56 A printed value is one line: the printer shows a byte string as text only when every character is plain (2026-10-18; LANG-16; PROTOCOL-13's open item after PROTOCOL-48) | decisions/lang.md:2138 |
| ## LANG-57 A relation's keys list in their declared order: a natural in Lang data is big-endian, and key-byte order is a theorem about fields (2026-10-19; ROOT APPROVED 2026-10-19, ROOT for CODEC; LANG-17; PROTOCOL-16's FINDING on PROTOCOL-51, cv 01a14f18-b8c8; blocks cv 01a14ece-43f1, the Bell as a queue) | decisions/lang.md:2181 |
| ## LANG-58 The Bell is a queue of rings: `pending` is the cursor, a ring is keyed by its signed notBefore and its ringer, and nothing a ring or an answer writes is the bell's cell (2026-10-19; ROOT APPROVED Q1-Q4; LANG-18; cv 01a14ece-43f1; HOSTING-10's requirements; with HOSTING-11's resident cut-over, HOSTING-31) | decisions/lang.md:2337 |
| ## LANG-59 A guard sees the row its edit replaces; the Bell's exactly-once is a guard on one relation; term literals go big-endian (2026-10-20; ROOT APPROVED the design, Q1 yes, Q2 = (B); LANG-18 proposed, LANG-19 built; cv 01a150a4-27ee, cv 01a14fe9-784c; with HOSTING-11's resident cut-over) | decisions/lang.md:2413 |
| ## LANG-60 The package wire has a version; a package says one line of itself (2026-10-20; ROOT ruled both parts into one lang!; LANG-19 found the reinterpretation, LANG-20 built; cv 01a15078-f528; CODEC-14 reviewed the codec hunks; PROTOCOL-19 the describe line) | decisions/lang.md:2506 |
| ## LANG-61 What extraction forces is the meaning: each field of an extracted record is its `get`'s value (2026-10-21; ROOT ruled it Lang's; LANG-21; LEDGER-4's hand-off, cv 01a152e3-9c8e) | decisions/lang.md:2562 |
| ## LANG-62 The run's state is the record it extracted; a no-ref meaning is lib-free, in Lang; `Forces` is `Means` with sizes (2026-10-21; LANG-22; LEDGER-13's open (b) and (d); cv 01a153a2-6489) | decisions/lang.md:2604 |
| ## LANG-63 The slots a run writes read back to the state it extracted (2026-10-21; LANG-22; corrects LANG-62's critique; cv 01a153b1-dc52) | decisions/lang.md:2658 |
| ## LANG-64 A tick walks at most one word: the byte primitives are charged per 32 bytes, paid before they walk (2026-10-21; LANG-23; DECISIONS-20261021 card 6, ID-4, ROOT's lean α; cv 01a14805-3d32) | decisions/lang.md:2678 |
| ## LANG-66 Contextual modal types, the guarded contextual closure and the hole rows: activities and continuations get their theory at the Lean level, and their first demonstration through the receivers (2026-10-22; ACTIVITIES-1, deputized by Ember; ROOT GO with three conditions; design `redregg/work/ACTIVITIES-DESIGN-20261022.md` §9–9.1) | decisions/lang.md:2778 |
| ## LANG-67 Open protocols as typed families of continuations: holes with polarity, linear tokens, obligations, the executed prefix, and the two-cell one-use-capability negotiation; nano's `interp_runs` re-derived as an instance (2026-10-22; ACTIVITIES-1; `redregg/work/ACTIVITIES-DESIGN-20261022.md` §9.4) | decisions/lang.md:2849 |
| ## LANG-68 Lang's deployed term language is a lawful instance of the guarded contextual closure, on its closed-hole fragment (2026-10-20 real; ACTIVITIES-2; ROOT ruled fork (A); cv 01a158c0-ddbf step 3's foundation; the (B) fork is Ember's card, cv 01a158da-0192) | decisions/lang.md:2942 |
| ## LANG-69 Split the contextual closure proof module by responsibility (2026-10-20 real; CX-ACT; cv 01a158c0-ddae) | decisions/lang.md:3010 |
| ## LANG-72 Boundary declarations and independent reuse licenses (2026-10-20 real; CX-P2) | decisions/lang.md:3036 |
| ## LANG-72 Alternative worlds and world-indexed grounding (2026-10-20 real; CX-P3; contextual program CARD P3) | decisions/lang.md:3121 |
| ## LANG-73 First-class repair values, composed residuals, policy selection and checked transport (2026-10-20 real; CX-P4) | decisions/lang.md:3209 |
| ## LANG-70 P5 logical statuses and alternating simulation; P1 finite interaction guards (2026-10-20 real; CX-P15) | decisions/lang.md:3288 |
| ## LANG-P10 Declared verifying traces, complete observations and early cutoff (2026-10-20 real; CX-P10) | decisions/lang.md:3362 |
| ## LANG-P12 Separate certified acyclic hole-provenance adapter (2026-10-20 real; CX-P12) | decisions/lang.md:3467 |
| ## LANG-P11b Material guards, change laws, context morphisms and the modal boundary (2026-10-20 real; Codex CX-P11b) | decisions/lang.md:3567 |
| ## LANG-P9 All-environment provenance, computed minimal repairs and recorded nogoods (2026-10-20 real; CX-P9; contextual program CARD P9) | decisions/lang.md:3682 |
| ## LANG-P11a Stable labellings, interface substitution and evidence-bearing game statuses (2026-10-20 real; CX-P11a) | decisions/lang.md:3804 |
| ## LANG-P6 · Certificates retain their logic and checked Environment context (2026-10-20 real; CX-P6) | decisions/lang.md:3914 |
| ## LANG-P8 Atomic one-use integration over the real receive path (2026-10-20 real; CX-P8) | decisions/lang.md:4023 |
| ## LANG-ACT Generated activities and guarded holes; Bell as an activity (2026-10-20 real; CX-ACT; cv 01a158c0-ddbf) | decisions/lang.md:4118 |
| ## LANG-P13 Complete observations in the generated hole (2026-10-20 real; Codex CX-P13) | decisions/lang.md:4244 |
| ## LANG-P7 preparatory substitution and deployment fork (2026-10-21 real; CX-P7) | decisions/lang.md:4450 |
| ## LANG-P7 live contextual packages — implementation ruling (2026-10-21 real, CX-P7 run 2) | decisions/lang.md:4513 |
| ## LANG-PE1 — receipt-first shadow obligation journal (2026-10-21, CX-PE1) | decisions/lang.md:4959 |
| ## LANG-74 Consolidation of the contextual program: one module per concept; the toys, the second judges and the second shapes are deleted (2026-10-22; CX-FOLD; `redregg/work/CONSOLIDATION-MAP-20261021.md`, `REVIEW-20261021.md`; rulings ledger R-0001–R-0003) | decisions/lang.md:5073 |
| Status: ruled by ROOT 2026-10-21 (R-0001, R-0002); steps land as LANG-74.n. | decisions/lang.md:5124 |
| Status: landed by CX-FOLD; next S1b (KERNEL/HOST re-home, R-0006), S1c (Integration), then LANG-74.2 (S2). | decisions/lang.md:5174 |
| Status: landed by CX-FOLD under R-0006; next S1c deletes Integration.lean. | decisions/lang.md:5215 |
| Status: landed by CX-FOLD; next LANG-74.2 (S2, the journey's p8 toy rows), after IMPACT-S2 and its RELEASE. | decisions/lang.md:5240 |
| Status: landed by CX-FOLD; next LANG-74.3 (S3). | decisions/lang.md:5301 |
| Status: landed by CX-FOLD; next LANG-74.4 (S4). | decisions/lang.md:5332 |
| Status: landed by CX-FOLD; next LANG-74.5 (S5). | decisions/lang.md:5367 |
| Status: landed by CX-FOLD; the pure-deletion phase S1–S5 is complete; next LANG-74.6 (S6). | decisions/lang.md:5403 |
| Status: landed by CX-FOLD-2; next LANG-74.7 (S7). | decisions/lang.md:5477 |
| Status: landed by CX-FOLD-2; next LANG-74.8 (S8, CROSS-LAYER: the four Kernel/Ledger import lines). | decisions/lang.md:5524 |
| Status: landed by CX-FOLD-2; next LANG-74.9 (S9, the `lang!` conformance card). | decisions/lang.md:5578 |
| Status: landed by CX-FOLD-3; next LANG-74.10 (S10, the provenance twin). | decisions/lang.md:5651 |
| Status: landed by CX-FOLD-3; next LANG-74.11 (S11, the Trace split). | decisions/lang.md:5691 |
| Status: landed by CX-FOLD-3; next LANG-74.12 (S12, the certificate reader to Census). | decisions/lang.md:5722 |
| Status: landed by CX-FOLD-3. The consolidation S1–S12 is complete; S13–S15 wait for Ember's rulings R1–R3. | decisions/lang.md:5766 |
| ## LANG-75 The promotion program: the toy contextual theory is promoted into deployed nano, card by card (2026-10-22; CX-PROMO; plan `redregg/work/PROGRAM-20261022.md` approved by Ember; rulings R-0024 RELEASE, R-0025 GRANT) | decisions/lang.md:5768 |
| Status: landed by CX-PROMO (lang!). Next: C9 (LANG-75.2), then the C2 measurement (P2). | decisions/lang.md:5922 |
| Status: landed by CX-PROMO (lang:). Next: C2 waits on the D.2 measurement's ruling (`promo/IMPACT-C2-MEASURE.md`). | decisions/lang.md:5959 |
| Status: landed by CX-PROMO-2 (lang:). Next: C3 + C4(a) docstrings (fast), then C5 (`promo/IMPACT-C5.md`). | decisions/lang.md:6009 |
| Status: landed by CX-PROMO-2 (lang:). Next: C5 (`promo/IMPACT-C5.md`). | decisions/lang.md:6034 |
| Status: landed by CX-PROMO-2 (lang:). Next: C5 part 2 (`selectHole_factor`). | decisions/lang.md:6081 |
| Status: landed by CX-PROMO-2 (lang:). Next: C7 (`promo/IMPACT-C7.md`), then C6. | decisions/lang.md:6119 |
| Status: landed by CX-PROMO-3 (lang:). Next: C6 (`promo/IMPACT-C6.md`). | decisions/lang.md:6153 |
| Status: landed by CX-PROMO-3 (lang:). P2 complete. Next: PROT-1 (`promo/IMPACT-PROT-1.md`, R-0044). | decisions/lang.md:6175 |
| Status: landed by CX-PROMO-4 (lang:). PROT-1 closed into this card (R-0046). Next: PROT-2 (roles replace `Polarity`; | decisions/lang.md:6248 |
| Status: landed by CX-PROMO-4 (lang:). Next: E3 + PROT-6 (the fuse), R-0044. | decisions/lang.md:6296 |
| Status: landed by CX-PROMO-6 (lang:). Next: E5's lang! from CX-P5's patch set (R-0059), after READY E5-PATCHSET. | decisions/lang.md:6355 |
| Status: landed by CX-PROMO-7 (lang!), with CX-P5 as second reader. | decisions/lang.md:6434 |
| ## LANG-76 An activity may declare a patience: an unanswered row is retired by anyone from its deadline on, with its cursor row (2026-10-23; CX-DEADLINE; Ember's open decision cv 01a166ba-7af9, built as its DEFAULT; IMPACT `redregg/work/promo/IMPACT-P4.md` §1.5; method R-0069) | decisions/lang.md:6673 |
| ## LANG-77 Typed nested-call arguments: an `invoke` slot declares its argument type, and the runtime encodes the value the method returned (2026-10-23; FABLE-T; cv 01a16679-198f; design `redregg/work/promo/DESIGN-T.md`; closes LANG-23 (iii); method R-0069) | decisions/lang.md:6711 |
| **Status.** L1 landed in the commit that carries the text above (`lang!`, FABLE-T, 2026-10-23). L2 landed in the | decisions/lang.md:6837 |
| ## LANG-78 One install loader: install admits every package of the closure, and the package itself, by the admission a run's load uses (2026-10-24; FIX-LANG card 1; COLLATION-20261024 §A10; READ-LANG F-1; method R-0069) | decisions/lang.md:6908 |
| ## LANG-79 The hole's coverage check refuses a missing pin `unpinned` by role, never under a verdict's name (2026-10-24; FIX-LANG card 2; COLLATION-20261024 §A11; READ-LANG F-2; method R-0069) | decisions/lang.md:6934 |
| ## LANG-81 The hole's support theorems are about the cell the support cites, and the deployed read supplies that binding (2026-10-24; FIX-LANG card 4; COLLATION-20261024 §A15; READ-LANGPROOFS F2; method R-0069) | decisions/lang.md:6954 |
| ## LANG-80 A deal's session row has a patience: `Std.offer` and `Std.offerEscrow` get the activity's retire, and the take tree types each refusal at its payload (2026-10-24; FIX-LANG card 3; COLLATION-20261024 §A12; READ-LANG F-3; method R-0069) | decisions/lang.md:6974 |
| ## LANG-82 The escrow's judge reads the legs: an offer declares what it wants, and a fuse moves value only when each side gives what the other asks (2026-10-24; FIX-LANG card 5; COLLATION-20261024 §A4; READ-LANGPROOFS F1, F10; method R-0069) | decisions/lang.md:6998 |
| ## LANG-86 A generator is a package whose method installs a package: `install` is a call an object may make, and `Std.headGenerator` is `Std.head` as an installed object (2026-10-26; FABLE-META, axis 1 of FRONTIER-AXES-20261026; design `redregg/work/promo/DESIGN-META.md`; with KERNEL-75) | decisions/lang.md:7025 |
| ## LANG-87 Rung 1 of generators: three payload writers (`u64be`, `sized`, `dsized`), a quoter whose output is proved to be the encoder's bytes, and the first template generator `Std.boundedGenerator` (2026-10-26; FABLE-META-2, axis 1; design `redregg/work/promo/DESIGN-META.md` §3; a `lang!`: package wire 5 → 6) | decisions/lang.md:7055 |
| ## LANG-88 A generator whose output names its invoker: `Std.ownerGenerator` takes no argument and installs the one-member allowlist of the member who generated, read from the Turn's request (2026-10-26; FABLE-META-2, axis 1; DESIGN-META §8; a `lang:`, no wire change) | decisions/lang.md:7173 |
| ## LANG-83 The document: a section is a `Std.hole` at `bytes` whose candidates are members' posts, justified by their grants, selected by an editor, withdrawn by name on revocation; its refusals name the justification that failed (2026-10-26; FABLE-CTX; design `redregg/work/promo/DESIGN-CTX.md` §2.3, §4, S0 + S1; method R-0069) | decisions/lang.md:7225 |
| ## LANG-84 Contract pins: a hole's support may demand that the cell it cites be GOVERNED by a named law or RUN a named package, read off the cell the kernel holds; a relaw that drops the law withdraws the fill by name (2026-10-26; FABLE-CTX; DESIGN-CTX §2.5a, S2; the package wire moves to version 7; method R-0069) | decisions/lang.md:7246 |
| ## LANG-92 A claim is a sentence the kernel refuses to let be false: `keeps inv law`, its certifying shape, and the checker proved sound (L1, 2026-10-26; FABLE-PCC; design `redregg/work/promo/DESIGN-PCC.md`; method R-0069) | decisions/lang.md:7264 |
| ## LANG-95 `Std.head` carries the chain: `headAtTy` = `{chain, height, roots, steps}`, the head law compares it at an equal step count, `headView.at` carries it (2026-10-26; FABLE-TRUST-2, Lang/StdHead by FABLE-OWNERSHIP; DESIGN-TRUST T2 §4.2; the Protocol half and the critique are PROTOCOL-75) | decisions/lang.md:7284 |

### decisions/ledger.md

| Title or status | Location |
|---|---|
| ## LEDGER-1 · `sealTurn` takes a list of effects and the receiver's nullifiers (BUILD-LEDGER, 2026-10-16) | decisions/ledger.md:7 |
| Status: built. | decisions/ledger.md:32 |
| ## LEDGER-2 · Value is a kernel discipline: balance AND floor conserved per denomination (BUILD-LEDGER, 2026-10-16) | decisions/ledger.md:34 |
| Status: built. | decisions/ledger.md:98 |
| ## LEDGER-3 · Three ledger receivers; the well's own id is the denomination (BUILD-LEDGER, 2026-10-16) | decisions/ledger.md:100 |
| Status: built. Next: a credit line (a floor transfer out of the well, issuer authority), its own entry. | decisions/ledger.md:137 |
| ## LEDGER-4 · A credit line is a floor transfer out of the well, under the issuer's authority (BUILD-LEDGER, 2026-10-17) | decisions/ledger.md:139 |
| Status: built. | decisions/ledger.md:178 |
| ## LEDGER-5 · Methods move value: a method's effects are `Body` calls, derived for the calling object (BUILD-LEDGER, 2026-10-17; PROPOSAL to KERNEL-5 and LANG-3, answering LANG-21 by name) | decisions/ledger.md:180 |
| Status: LANG accepted with amendments; KERNEL-5's answer on (b)(c)(d) pending. | decisions/ledger.md:239 |
| ## LEDGER-5 · CLOSED against KERNEL-28 and LANG-23: what was accepted, what amended, what each side owes (LEDGER-2, 2026-10-17) | decisions/ledger.md:241 |
| Status: CLOSED. D5 build order: KERNEL-27 → KERNEL-24 → D5 (LEDGER-2) → LANG's `lang!`. | decisions/ledger.md:292 |
| ## LEDGER-6 · The escrow: its account is `accountId self asset`, funded through a v0 mutate grant in the same tree; the payout's guard is the kernel's `once`, not the floor (LEDGER-2, 2026-10-17) | decisions/ledger.md:294 |
| Status: decided; (b) asked of LANG-4 and KERNEL-5 for D5's flag day; the package after `lang!` | decisions/ledger.md:368 |
| ## LEDGER-7 · Accounts are named by reference in `Body`: `AcctRef = well asset \| of owner asset`; no LANG builtin (LEDGER-2, 2026-10-17; amends LEDGER-6 (b), LANG-4's counter-proposal, to be LANG-25) | decisions/ledger.md:375 |
| Status: agreed with LANG-4; KERNEL-5 to review in D5's statements. | decisions/ledger.md:399 |
| ## LEDGER-8 · D5's three landings, and D5c's concrete shape: a Draft per receiver, an `At` (actor, born base), one tick pool returned by the run (LEDGER-2, 2026-10-17; builds KERNEL-28 + LEDGER-5/7, reviewed by KERNEL-6; asks LANG-5 one change) | decisions/ledger.md:401 |
| Status: decided by LEDGER-2. KERNEL-6 to review; LANG-5 asked (e). | decisions/ledger.md:465 |
| ## LEDGER-9 · LEDGER owns `Ledger/` and `world/escrow/`, and commits under `ledger:` (ROOT ruling, recorded by LEDGER-2, 2026-10-17) | decisions/ledger.md:467 |
| Status: ruled by ROOT 2026-10-17; owners.py and the OWNERS rows landed by GATES-2 in cb99f02. | decisions/ledger.md:489 |
| ## LEDGER-10 · The escrow package as built: Ledger/Escrow.lean, its law's theorems over all data, ledger-sim with three plants (LEDGER-3, 2026-10-18; builds LEDGER-6 on LANG-33) | decisions/ledger.md:492 |
| Status: BUILT (this commit). The bounty row (PROTOCOL's) is re-cut by PROTOCOL-6 on this text. | decisions/ledger.md:571 |
| ## LEDGER-11 · On LANG's digest day the escrow's ids are `digest`, and the deposit's once key is a creator-set `nonce` (LEDGER-3, 2026-10-18; with LANG-11's lang! day, cv 01a14aab-adae (ii)) | decisions/ledger.md:573 |
| ## LEDGER-12 · The escrow says what it does: one doc line, in the surface source and the Lean package alike (LEDGER-4, 2026-10-19; on LANG-60's `doc`) | decisions/ledger.md:603 |
| ## LEDGER-13 · The escrow's payout theorem is of what the receiver runs: `RunCalls` of every successful `runMeasured` of the escrow package (LEDGER-5, 2026-10-21; on LANG-61) | decisions/ledger.md:629 |
| ## LEDGER-14 · The one-payout theorem is of the receiver's runs: a chain of committed runs, each reading the slots the last wrote, pays out at most once; two kernel-evaluated runs meet its premise (LEDGER-6, 2026-10-21; on LANG-62/63) | decisions/ledger.md:705 |
| ## LEDGER-15 · The one-payout theorem over the history the World admits: KERNEL's next-run link turns an admitted history around one object into a `Runs` (LEDGER-6, 2026-10-21; on KERNEL-23's 5807a47 and 628a8b9) | decisions/ledger.md:775 |
| ## LEDGER-17 · Unspent credit sits: no sweep, no decay, no reclaim to a commons (ROOT for LEDGER, Ember's ruling 2026-10-21; closes LEDGER-4's taste fork) | decisions/ledger.md:820 |
| **Status.** ruled by Ember 2026-10-21 (recorded by ROOT for LEDGER; no LEDGER lane live). Nothing moves: | decisions/ledger.md:834 |
| ## LEDGER-16 · LEDGER-6 (c)'s v0 whole-balance grant is superseded by KERNEL-60's `transfer (cap)` (KERNEL-24 with LEDGER-6's agreement, 2026-10-21) | decisions/ledger.md:837 |
| ## LEDGER-18 · The deposit's authority is exactly its amount: the cap is read off the escrow, and a deposit then a release are an admitted history (LEDGER-7, 2026-10-22; on KERNEL-60's `Right.transfer (cap)`, KERNEL-59's `ObjectHistory`; cv 01a1553b-2765) | decisions/ledger.md:840 |
| ## LEDGER-19 · A grant moves at most what it had left, over every audited history: `grant_moves_le_cap`, a `Std.chain_sum` instance over Worlds (LEDGER-7, 2026-10-22; on KERNEL-30's 1fe9f93; ROOT's ruling on LEDGER-18's finding) | decisions/ledger.md:912 |

### decisions/ops.md

| Title or status | Location |
|---|---|
| ## OPS-0 · the row: a renderer and a driver, and nothing imports it (2026-10-16) | decisions/ops.md:7 |
| **Status.** row accepted by ROOT 10-16 ("renderer/driver; nothing imports Ops"). | decisions/ops.md:30 |
| ## OPS-1 · law 1: state is carried only by re-genesis from a checked export (2026-10-16) | decisions/ops.md:32 |
| **Status.** ACCEPTED by ROOT 10-16; charter b3787d3. BUILT 2026-10-17: KERNEL-29 (b8e0f82, Carried | decisions/ops.md:67 |
| ## OPS-2 · cross-World replay: reproduced against the real `host`, routed to KERNEL-4 (2026-10-16) | decisions/ops.md:74 |
| **Status.** CLOSED by KERNEL-24 (9e91ede). Planted against the real exe (OPS-2, the plants commit | decisions/ops.md:92 |
| ## OPS-3 · backup = the three files in order; restore = `host check --anchor` (2026-10-16) | decisions/ops.md:98 |
| **Status.** ACCEPTED: every row of the table and the live and sealed rows run in store-plants | decisions/ops.md:144 |
| ## OPS-4 · the test founder signs with RFC 8032's published vectors (2026-10-16) | decisions/ops.md:147 |
| **Status.** open. | decisions/ops.md:158 |
| ## OPS-5 · THE BAR is PERF's; OPS builds no BAR driver (2026-10-17) | decisions/ops.md:160 |
| **Status.** CONFIRMED by ROOT 10-17 (Ops/Bar.lean deleted from the plan). | decisions/ops.md:170 |
| ## OPS-6 · one prevent list from both exit tables, a start limit, and a generated operator table (OPS-2, 2026-10-17) | decisions/ops.md:172 |
| **Status.** landed with this commit; HOST-5 and CLIENT told of the coupling. | decisions/ops.md:209 |
| ## OPS-7 · the broker's production TLS anchors are a build-pinned generated file (HOSTING-15, 2026-10-17) | decisions/ops.md:211 |
| **Status.** landed with the file it checks. | decisions/ops.md:229 |
| ## OPS-8 · the keybroker unit, rendered from HOSTING-16's exit tables, checks its anchors at every start (2026-10-17) | decisions/ops.md:231 |
| **Status.** landed; run PENDING a box. | decisions/ops.md:256 |
| ## OPS-9 · HOST-33's moved check, planted through the real exe; the operator runs `check` (OPS-3, 2026-10-18) | decisions/ops.md:258 |
| **Status.** landed with this decision. | decisions/ops.md:288 |
| ## OPS-10 · the node's two users, SOCKDIR and the writer's runtime directory are rendered; the nd-hosted follower waits for CLIENT-3's socket group (OPS-3, 2026-10-18; ROOT ruling on HOSTING-17 §7) | decisions/ops.md:290 |
| **Status.** landed with this decision; follower and grain-launch units PENDING (CLIENT-3 `--group`, | decisions/ops.md:336 |
| ## OPS-11 · the hosted follower is a template unit per World, its socket flat in /run/nd-follow (OPS-3, 2026-10-18) | decisions/ops.md:339 |
| **Status.** landed; the driver (`nd sync` timer) PENDING PROTOCOL-7 + CLIENT-3; grain-launch PENDING HOSTING-19. | decisions/ops.md:370 |
| ## OPS-12 · the grain launcher is a template unit per World, rendered from HOSTING-19's two exit tables (OPS-3, 2026-10-18) | decisions/ops.md:372 |
| **Status.** landed; the burst5 run (with the keybroker's) PENDING. | decisions/ops.md:399 |
| ## OPS-13 · the follower's driver is an always-restarting `nd sync` per World, not a timer (OPS-3, 2026-10-18) | decisions/ops.md:401 |
| **Status.** landed; run PENDING burst5. | decisions/ops.md:423 |
| ## OPS-14 · the units under systemd: keybroker needs AF_NETLINK; grain-launch depends on its driver (OPS-3, 2026-10-18; burst5 run, HOSTING-7's resident row) | decisions/ops.md:425 |
| **Status.** landed. | decisions/ops.md:451 |
| ## OPS-15 · a follow Store is JOINED from a signed invitation, never a reproduced genesis; the hosted follower's join is a hand-run operator verb (OPS-4, 2026-10-18; PROTOCOL-42, CLIENT-26, ROOT-ruled) | decisions/ops.md:453 |
| **Status.** landed (this commit); row P PENDING a box window. | decisions/ops.md:499 |
| ## OPS-16 · the live harness judges only this run's journal: a cursor, planted (OPS-4, 2026-10-18; GATES-5's fail-open finding, ROOT) | decisions/ops.md:502 |
| **Status.** landed (this commit); systemd re-run PENDING a box window. | decisions/ops.md:521 |
| ## OPS-18 · the owner's audit of the six OPS-path landings made without an OPS lane (OPS-6, 2026-10-20) | decisions/ops.md:524 |
| **Status.** landed (this commit). | decisions/ops.md:541 |
| ## OPS-19 · THE PIN: api.anthropic.com's leaf key is shipped in deploy/tls/pins (OPS-6, 2026-10-21; Ember approved B1, ROOT for HOSTING) | decisions/ops.md:544 |
| **Status.** landed (this commit); no provider call has been made. | decisions/ops.md:560 |
| ## OPS-20 · the re-genesis owed for LANG-76's Bell: no deployed World holds the old Bell (CX-OPS, 2026-10-23; Ember approved the re-genesis) | decisions/ops.md:563 |
| **Status.** landed (this commit). Nothing re-emits; nothing refuses to load. | decisions/ops.md:597 |

### decisions/perf.md

| Title or status | Location |
|---|---|
| ## PERF-1 · THE BAR over sockets: real processes, one clock per `nd`, judged only when quiet (2026-10-17) | decisions/perf.md:7 |
| **Status.** superseded by PERF-2 (2026-10-18): the Linux path, a third actor, the standing row, and counts in place of a clock in the gate. | decisions/perf.md:56 |
| ## PERF-2 · THE BAR runs on Linux, in standing, and gates counts, never a clock (2026-10-18) | decisions/perf.md:58 |
| **Status.** open (GATES-6 agreed 2026-10-18: the `script:` row kind, conditions 1–3 met). | decisions/perf.md:152 |
| ## PERF-3 · PROPOSED to ROOT: deployed-parameter counts from THE BAR's own Store (swap 10, C4/C5) (2026-10-18) | decisions/perf.md:154 |
| **Status.** ruled by ROOT 2026-10-18: the PERF exe, not `host check --count` (the deployed binary counts | decisions/perf.md:196 |
| ## PERF-4 · C6: THE BAR seals a base at its midpoint; the reopen reads base + tail (2026-10-18) | decisions/perf.md:224 |
| **Status.** open. | decisions/perf.md:257 |
| ## PERF-5 · THE BAR's reopen at the true worst cut: a sized, standing-only bench row (2026-10-18) | decisions/perf.md:259 |
| **Status.** open. | decisions/perf.md:312 |
| ## PERF-6 · The worst cut, measured in three tail shapes: the costliest is pinned, not assumed (2026-10-18) | decisions/perf.md:314 |
| **Status.** open. | decisions/perf.md:374 |
| ## PERF-7 · bar.sh measures only binaries that are this tree's, by lake's and cargo's own reports (2026-10-18, ROOT) | decisions/perf.md:376 |
| **Status.** landed with this entry. | decisions/perf.md:423 |
| ## PERF-8 · The worst World is the reader's bound: a synthetic base at worldBytesMax, scaled into standing (2026-10-18, ROOT) | decisions/perf.md:425 |
| **Status.** open (re-pin at KERNEL-55's bound). | decisions/perf.md:478 |
| ## PERF-9 · A fourth worst-cut shape: the deployed Bell queue's rows tail (2026-10-18, ROOT; LANG-58 96179fb) | decisions/perf.md:480 |
| **Status.** landed da63f5b. | decisions/perf.md:521 |
| ## PERF-10 · The worst World at the derived bound; the worst cut after the shared empty digest (2026-10-20, PERF-3; HOST-57 359e9e8, KERNEL-22 16f3b9f, LANG-59 c100be5) | decisions/perf.md:523 |
| **Status.** landed with this entry. | decisions/perf.md:602 |
| ## PERF-11 · The worst cut after the one-pass commit (2026-10-21, PERF-4; KERNEL-23 258c273) | decisions/perf.md:604 |
| **Status.** landed with this entry. | decisions/perf.md:664 |
| ## PERF-12 · The worst cut, one bench per shape: every judged run bounded under the deadline (2026-10-21, PERF-5, landed by PERF-6; GATES-9's benchtrace) | decisions/perf.md:666 |
| **Status.** Landed with this entry. | decisions/perf.md:789 |
| ## PERF-13 · THE BAR re-runs the stale the kernel declines, and the standing run forces one (2026-10-22, ROOT for PERF, R-0037) | decisions/perf.md:791 |
| **Status.** Landed with this entry. | decisions/perf.md:873 |

### decisions/protocol.md

| Title or status | Location |
|---|---|
| ## PROTOCOL-0 · the row attacked (2026-10-16) | decisions/protocol.md:7 |
| **Status.** open. | decisions/protocol.md:23 |
| ## PROTOCOL-1 · six operations on two sockets (2026-10-16) | decisions/protocol.md:25 |
| **Status.** open. | decisions/protocol.md:50 |
| ## PROTOCOL-2 · "every op names exactly one receiver" is a vacuous statement; the table proves two that are not (2026-10-16) | decisions/protocol.md:52 |
| **Status.** ruled by ROOT 2026-10-16: ACCEPTED (receiver injectivity + single-writer replace the one-receiver statement). | decisions/protocol.md:64 |
| ## PROTOCOL-3 · consent-by-follow vs authorized reads: a conflict in the spec (2026-10-16) | decisions/protocol.md:66 |
| **Status.** ruled by ROOT 2026-10-16: ACCEPTED for v0. `log` and `read` are served only to keys holding a FOLLOW GRANT; membership gates the whole log; per-cell hiding/blinding from members is a DECLARED ABSENCE for v1, tied to the blinding-key custody question open with Ember. J5/K10/KH hold: a key without a grant is refused at `log`/`read` by name. | decisions/protocol.md:84 |
| ## PROTOCOL-4 · follow must re-run the receiver on every logged event (2026-10-16) | decisions/protocol.md:93 |
| **Status.** ruled by ROOT 2026-10-16: ACCEPTED; KERNEL told (Receive.rederive). | decisions/protocol.md:106 |
| ## PROTOCOL-5 · rows are Lean data, not scripts or Markdown (2026-10-16) | decisions/protocol.md:108 |
| **Status.** open. | decisions/protocol.md:123 |
| ## PROTOCOL-6 · the client bounds live in the protocol table (2026-10-16) | decisions/protocol.md:125 |
| **Status.** open. | decisions/protocol.md:134 |
| ## PROTOCOL-7 · laws attacked (2026-10-16) | decisions/protocol.md:136 |
| **Status.** ruled by ROOT 2026-10-16: the ≤40-ops ceiling becomes four ratchet rows in SIZE.md (ops, | decisions/protocol.md:144 |
| ## PROTOCOL-8 · connectionsMax = 64 (2026-10-16) | decisions/protocol.md:148 |
| **Status.** open. | decisions/protocol.md:161 |
| ## PROTOCOL-9 · review of CODEC-8 (f81e093: the follow payloads as layout data), landed CROSS-LAYER in Protocol/ (2026-10-16) | decisions/protocol.md:163 |
| **Status.** open (finding 1 asked of CODEC). | decisions/protocol.md:189 |
| ## PROTOCOL-10 · rows/run: the runner is Lean, judging is a pure function, and a row with no driver is PENDING, never PASS (2026-10-16) | decisions/protocol.md:191 |
| **Status.** open. | decisions/protocol.md:215 |
| ## PROTOCOL-11 · Protocol.Command: eleven verbs, one parser, a five-phase machine that re-derives at every step (2026-10-16) | decisions/protocol.md:221 |
| **Status.** open. | decisions/protocol.md:249 |
| ## PROTOCOL-12 · the READ ENVELOPE (HOST-11's gate as data) and Bounds.idleMsMax (2026-10-16) | decisions/protocol.md:251 |
| **Status.** open. | decisions/protocol.md:264 |
| ## PROTOCOL-13 · ROOT rulings: `read` is RESERVED; each owner names its refusals with `name_injective` (2026-10-16) | decisions/protocol.md:266 |
| **Status.** ruled by ROOT 2026-10-16. | decisions/protocol.md:280 |
| ## PROTOCOL-14 · thin consent: what a member that cannot fold the whole log verifies (2026-10-16, DRAFT with HOST-3; Ember ruled thin IN "if we can get away with it") | decisions/protocol.md:282 |
| **Status.** ruled by ROOT 2026-10-16: build A for v0 (HOST-3 agreed: `read` serves the World part | decisions/protocol.md:317 |
| ## PROTOCOL-15 · the member rows run in process against HOST's loop; plants are mutations of the parameters, judged by line and outcome (2026-10-16) | decisions/protocol.md:325 |
| **Status.** open. | decisions/protocol.md:358 |
| ## PROTOCOL-16 · KERNEL-20: the verb `follow` is DELETED; `grant world MEMBER observe --via G` says it (2026-10-16) | decisions/protocol.md:360 |
| **Status.** open. | decisions/protocol.md:372 |
| ## PROTOCOL-17 · the attempt-store decision is a Lean function nd calls (2026-10-16, ROOT: open) | decisions/protocol.md:380 |
| ## PROTOCOL-20 · `Bounds.replyMsMax` = 120000: the client's per-request reply deadline (2026-10-17, ROOT's ask for CLIENT-2) | decisions/protocol.md:407 |
| **Status.** open. | decisions/protocol.md:420 |
| ## PROTOCOL-21 · custody results are `status ‖ payload` with named refusals (2026-10-17, CLIENT-2's ask) | decisions/protocol.md:422 |
| **Status.** open. | decisions/protocol.md:436 |
| ## PROTOCOL-18 · thin consent BUILT (option A): `adopt HEIGHT DIGEST`, `Protocol.Thin.accept`, follow's state holds the download (2026-10-16) | decisions/protocol.md:439 |
| **Status.** open. | decisions/protocol.md:467 |
| ## PROTOCOL-19 · log paging; a defect found: `expired` makes a cold catch-up impossible (2026-10-16) | decisions/protocol.md:469 |
| **Status.** envelope half BUILT (PROTOCOL-5, 2026-10-17), below. | decisions/protocol.md:482 |
| ## PROTOCOL-22 · every connection close is named: `Status.closed` + `CloseReason`; the idle rule waits for nothing in flight (2026-10-17, BUILD-TRANSPORT; ASSEMBLY-transport-consent D5, scout T2) | decisions/protocol.md:515 |
| **Status.** landed (vocabulary); the mux and `nd-attach` land under `client:`. | decisions/protocol.md:547 |
| ## PROTOCOL-23 · the child wire's hang-up: the supervisor tells its child a connection ended, and the child acknowledges it by name (2026-10-17, BUILD-TRANSPORT; shape by PROTOCOL-5, ROOT's ruling) | decisions/protocol.md:549 |
| **Status.** landed. | decisions/protocol.md:572 |
| ## PROTOCOL-24 · programmed objects from the command language: `create --pkg PKG STATE`, `invoke` reads ARGS as TEXT; rows grain and THE BAR's invoke (2026-10-17, PROTOCOL-5) | decisions/protocol.md:574 |
| **Status.** landed. The WASTE lines of THE BAR's invokes wait on KERNEL-5's `invokeRun` (one | decisions/protocol.md:598 |
| ## PROTOCOL-25 · THE BAR's invokes are measured, not timed: `WASTE invoke …` pinned; a missed deadline is `hang`, a non-verdict (2026-10-17, PROTOCOL-5; ROOT's correction) | decisions/protocol.md:601 |
| **Status.** landed. | decisions/protocol.md:621 |
| ## PROTOCOL-26 · `grant TARGET anyone RIGHTS`: a public object in the command language (KERNEL-26) (2026-10-17, PROTOCOL-5) | decisions/protocol.md:623 |
| **Status.** landed. | decisions/protocol.md:635 |
| ## PROTOCOL-27 · an envelope's life is a window of heights, whatever the writer states: `notBefore`, `notYet`, `wideWindow` (2026-10-17, PROTOCOL-6; PROTOCOL-19's open critique) | decisions/protocol.md:637 |
| **Status.** BUILT (this commit). | decisions/protocol.md:708 |
| ## PROTOCOL-28 · row wrongWorld: the writer's whole log, replayed into a Store that differs only in its nonce, is refused `wrongWorld` call by call; the same nonce is a restore (2026-10-17, PROTOCOL-6; KERNEL-24 at 9e91ede) | decisions/protocol.md:710 |
| **Status.** BUILT (this commit). Rows 14 PASS, 3 PENDING (pay well bounty). | decisions/protocol.md:734 |
| ## PROTOCOL-29 · the read envelope names its World; a member signs for the World it was invited to (2026-10-17, BUILD-TRANSPORT; ASSEMBLY D3, KERNEL-24; shape with PROTOCOL-6) | decisions/protocol.md:736 |
| **Status.** landed (this commit); the cross-World envelope line in row wrongWorld follows | decisions/protocol.md:761 |
| ## PROTOCOL-30 · a carry (OPS-P1) must keep the live journal, or the attempt store calls a committed call refused (2026-10-17, PROTOCOL-6; answers OPS-P1's question to PROTOCOL) | decisions/protocol.md:764 |
| **Status.** (A) agreed by OPS-2 and taken by KERNEL-6 as KERNEL-29: the carried World keeps the old | decisions/protocol.md:786 |
| ## PROTOCOL-32 · the ledger verbs `issue`, `account`, `transfer`, `credit`; rows `well` and `pay` on the receivers; a hostile client is a row act (2026-10-17, PROTOCOL-6; LEDGER-2's D5 at c3c7aa3, LEDGER-6 (f), LEDGER-7) | decisions/protocol.md:792 |
| **Status.** BUILT (this commit). Rows 17 PASS, 1 PENDING (bounty). | decisions/protocol.md:825 |
| ## PROTOCOL-33 · row forgotten: past KERNEL-33's prune a lookup is `uncertain forgotten`, never `refused`; `Expect.unsettled` names why (2026-10-17, PROTOCOL-6; KERNEL-33 at 17e2d3f, HOST's arm) | decisions/protocol.md:827 |
| **Status.** BUILT (this commit). Rows 18 PASS, 1 PENDING (bounty), re-run after KERNEL-33's charge change. | decisions/protocol.md:852 |
| ## PROTOCOL-34 · row bounty on LEDGER's escrow; `grant` takes a value account as its target (2026-10-17, PROTOCOL-6; LEDGER-10 at 7c6c7e1) | decisions/protocol.md:854 |
| **Status.** BUILT (this commit). Rows: ALL PASS, 19 rows. | decisions/protocol.md:880 |
| ## PROTOCOL-35 · row carry: export, import by digest, the carried World answers the old journal, an old-origin call is `wrongWorld` (2026-10-17, PROTOCOL-6; KERNEL-29 b8e0f82, CODEC-5 28b4a38, HOST-28 6b89d6f) | decisions/protocol.md:882 |
| **Status.** BUILT (this commit). Rows: ALL PASS, 20 rows. | decisions/protocol.md:905 |
| ## PROTOCOL-36 · carried member ids are names (KERNEL-40, opacity); the rows key founders by the lineage's first origin (2026-10-17, PROTOCOL-6) | decisions/protocol.md:907 |
| **Status.** BUILT (this commit). Rows ALL PASS, 20. | decisions/protocol.md:922 |
| ## PROTOCOL-37 · row thinStale: a thin member adopts a pin more than a window old; the rows' `window` act (2026-10-17, PROTOCOL-7) | decisions/protocol.md:924 |
| **Status.** BUILT (this commit). Rows ALL PASS, 21. | decisions/protocol.md:951 |
| ## PROTOCOL-38 · `sync`, the catch-up verb; `CommandExit`, nd's exit table, with `behind` as its own restart-class end; `CustodyRefusal.envelopeOnly` (2026-10-17, PROTOCOL-7; HOSTING-17 §7, CLIENT-3's ask, ROOT ruling) | decisions/protocol.md:953 |
| **Status.** BUILT (this commit). Rows ALL PASS, 21. | decisions/protocol.md:976 |
| ## PROTOCOL-39 · the signed shapes are pairwise disjoint by domain; the command machine signs `callMessage` (2026-10-17, PROTOCOL-7; KERNEL-42) | decisions/protocol.md:978 |
| **Status.** BUILT (this commit). Rows ALL PASS 21; kernel-sim ALL PASS 64 seeds, arm sig-bare met; WASTE unchanged. | decisions/protocol.md:996 |
| ## PROTOCOL-40 · the `nd --stdio` surface: a resident runs every World verb but init, rotate and adopt, refused `notOnSurface` otherwise; replies are the `done` step; `peerRefused`; custody `noRotation` (2026-10-17, PROTOCOL-7; HOSTING-20, CLIENT-3's ask, ROOT approval) | decisions/protocol.md:998 |
| **Status.** BUILT (this commit): the surface, its theorems (incl. `mem_stdioWords_iff`, for any string nd receives) and the emitted names. `noRotation` and `peerRefused` are names only here; CLIENT's custody and nd-supervise enforce them, with their plants. A developer can still write `true` for a new verb; the total match makes that a decision, never a default. Rows ALL PASS 21. | decisions/protocol.md:1018 |
| ## PROTOCOL-41 · a reply is FINAL only when the refusal is recorded; `Status.declined` for every other refusal of a submit; the log is a list of steps, positioned by step count (2026-10-18, PROTOCOL-8; KERNEL-44/47, the refusals day, with HOST-12) | decisions/protocol.md:1020 |
| **Status.** BUILT in the refusals day (KERNEL-14's one commit). CLIENT owes the attempt store's `declined` arm (ROOT relays). The emitted status and command-exit tables move: `generated.rs` re-emits. | decisions/protocol.md:1076 |
| ## PROTOCOL-42 · an invitation: the joiner derives the World it joins from inputs a sponsor key it trusts signed; `invite`, `adopt INVITE KEY`, `host join`; row `invite` (2026-10-18, PROTOCOL-9; TRANSPORT's D7 and ASSEMBLY D1's open critique, with HOST-12) | decisions/protocol.md:1091 |
| **Status.** BUILT. Rows ALL PASS 23 (logs/protocol9-inv-rows2.log). Full `lake build` green. The emit checks pass, with units re-emitted. | decisions/protocol.md:1156 |
| ## PROTOCOL-43 · the use row: objects made by one member and used by another, counted from signed calls; THE BAR's purpose as a row (2026-10-18, PROTOCOL-9; DELVETALK-LEARNINGS §4.7, §7) | decisions/protocol.md:1169 |
| **Status.** BUILT. Row `use`, plant `oneMember`@14 `refused unshared:0`. | decisions/protocol.md:1201 |
| ## PROTOCOL-44 · objects describe themselves: `read OBJ ?` prints an object's methods (index, label, argument type, call slots) and laws through the one printer; refusals print what to do next (2026-10-18, PROTOCOL-9; DELVETALK-LEARNINGS §4.3) | decisions/protocol.md:1208 |
| **Status.** BUILT. Rows ALL PASS 25. | decisions/protocol.md:1257 |
| ## PROTOCOL-45 · a receipt as proof: what happened to a call, shown against the head a member holds; `receipt TXID`; row `receipt` (2026-10-18, PROTOCOL-9; cv 01a14ade-0f69 by KERNEL-11, KERNEL-41/44/47 roots; delvetalk's top thirst) | decisions/protocol.md:1265 |
| **Status.** BUILT. Rows ALL PASS 26. | decisions/protocol.md:1305 |
| ## PROTOCOL-46 · a settlement is the member's word, never the Host's: the attempt store ends a call only on its own follow's `receipt CALL`; `absent` is never the end of an attempt (2026-10-18, PROTOCOL-10 proposed, PROTOCOL-11 built; ROOT APPROVED; cv 01a14dfa-1ffb, cv 01a14ade-0f69; CLIENT-6 the client half, CLIENT-27) | decisions/protocol.md:1314 |
| **Status.** BUILT; rows ALL PASS 27. | decisions/protocol.md:1416 |
| ## PROTOCOL-47 · a sponsor pins the base its own follow verified, never the Host's word: the log reply states the writer's newest durable base; `invite` pins follow's OWN digest at it; the rows seal by `Host.sealNow` (2026-10-18, PROTOCOL-12; HOST-43's condition (1), CLIENT-5's finding; HOST-12 agreed the Host half; ROOT APPROVED) | decisions/protocol.md:1427 |
| ## PROTOCOL-48 · `read OBJ` of a programmed object prints its state VALUE, one line through `Lang.Print` at the package's state type; a data object keeps `I=VALUE` (2026-10-19, PROTOCOL-13; ROOT ruling, HOSTING-8's need, LANG-16 reviews) | decisions/protocol.md:1517 |
| ## PROTOCOL-49 · a page refused `pageIo` is "not now", never "never": the command ends restart-class `CommandExit.pageIo` (57), what it absorbed is kept, and it runs again (2026-10-19, PROTOCOL-14; ROOT ruling on HOST-48 01396b7) | decisions/protocol.md:1549 |
| ## PROTOCOL-50 · the member rows run at the deployed parameters too: one pipeline generic in the digest, `rows --deployed` beside the toy run (2026-10-19, PROTOCOL-15; STAND-INS-20261019 §4 D1, swap 7) | decisions/protocol.md:1582 |
| ## PROTOCOL-51 · `read OBJ REL K [PREFIX]`: a resident reads a relation's rows, in key order, through THE range read (2026-10-19, PROTOCOL-16; cv 01a14f18-b8c8, LANG-52's ask, for the Bell as a queue cv 01a14ece-43f1) | decisions/protocol.md:1624 |
| ## PROTOCOL-52 · KERNEL-54's attempt side: a stale is settled from the member's own fold, never recorded; an absent lookup is confirmed with follow before any resend (2026-10-19, PROTOCOL-16; KERNEL-54 ruled, PROTOCOL-15's five conditions; routed through KERNEL-21's one `kernel!` commit) | decisions/protocol.md:1667 |
| ## PROTOCOL-54 · a method's refusal reaches the member in its own words: `hint program: answer: refused notResident` (2026-10-19, PROTOCOL-17; cv 01a15039-0a62, HOSTING-10's finding, ROOT assigned) | decisions/protocol.md:1722 |
| ## PROTOCOL-55 · the rows' page budget is DERIVED from the kernel's event bound: `Kernel.Bounds.eventBytesMax + 5`, both parameter sets, with the theorem that a record's walk that has served nothing serves the first step past its start (2026-10-18, PROTOCOL-18; ROOT approved) | decisions/protocol.md:1736 |
| ## PROTOCOL-56 · a custody refusal of `signIncoming` hands back the writer's `unknownKey`: one rule over the step (2026-10-18, PROTOCOL-18; ROOT ruled (a), CLIENT-8's nd-members finding ecb02bf) | decisions/protocol.md:1762 |
| ## PROTOCOL-57 · a call refused stale BEHIND is never admitted later: the settlement's `refused staleCode` is final by theorem (2026-10-21, PROTOCOL-19; cv 01a15187; KERNEL-23 agreed the kernel statement) | decisions/protocol.md:1787 |
| ## PROTOCOL-58 · an attempt's `uncertain` names the refusal that caused it: `hint confirm: refused NAME` (2026-10-21, PROTOCOL-20; cv 01a150b1, PROTOCOL-55's critique; agreed with CLIENT-9, which lands the Rust half after this) | decisions/protocol.md:1809 |
| ## PROTOCOL-53 · THE BAR's per-unit counts are judged: `WASTE rowbar frames-per-write`, `steps-per-write`, `reopen-bytes-per-byte-past-base` (2026-10-21, PROTOCOL-20; agreed with PERF-2 as PROTOCOL-16's spec, re-scoped by ROOT for PERF; GATES-8 for gates/waste.tsv) | decisions/protocol.md:1830 |
| ## PROTOCOL-59 · `invoke OBJ METHOD ARGS [--range REL K [PREFIX]]`: the plan signs the method's range read at follow's listing (2026-10-21, PROTOCOL-21; item 4, ROOT ruled (a) with K-first order; LANG-22 agreed the structured refusal) | decisions/protocol.md:1855 |
| ## PROTOCOL-60 · A cancel reaches a follower: page event tag 2 `2 ‖ nat64 n ‖ sig ‖ call` and absorbStep's cancel arm (2026-10-19, PROTOCOL-22; PROTOCOL's half of KERNEL-60's C1, inside KERNEL-26's commit; HOST-17 agreed the Host paths on three conditions) | decisions/protocol.md:1871 |
| ## PROTOCOL-63 · `nd cancel CALL` and the `cancel` op: a member closes its own loose call (2026-10-22, PROTOCOL-23; KERNEL-60's C1 over the wire; HOST-18 agreed the Host half, cv 01a15543-39fd) | decisions/protocol.md:1903 |
| ## PROTOCOL-61 · a sponsor-signed carried start pins the origin (2026-10-20, CX-HOST; ROOT's card 7a (B′)) | decisions/protocol.md:1928 |
| ## PROTOCOL-64 · Follow settles step 4 on its own World: `done ok` for a submitted call only when follow's World journals it (2026-10-23, CX-E2; E2's T0, R-0054/R-0058/R-0060/R-0061; promo/IMPACT-E2.md §1, §4; promo/READ-E2-grok.md, promo/READ-E2b-grok.md) | decisions/protocol.md:2007 |
| ## PROTOCOL-65 · receipts between Worlds: another World's committed call, checked by Lean against a head this World holds (E5, PROGRAM-20261022 §2(a) / P5; R-0051, R-0059; cv 01a14ef0-ffe7, 01a14dfa-200a, 01a14dfa-1ffb, 01a14de7-224a) | decisions/protocol.md:2071 |
| Status: landed by CX-PROMO-7 (lang!) from CX-P5's patch set, unchanged; build, journey, vectors, decls, the X rows and PL1–PL6 re-measured on the landing worktree (hbox `logs/promo/e5/`). LANG's half is LANG-75.14. | decisions/protocol.md:2162 |
| ## PROTOCOL-67 · adopt's genesis check is "a World a genesis builds", not "no cell": the honest thin joiner adopts again (2026-10-23, CX-FIX-JOIN; R-0069; amends HOSTING-43's `atGenesis`) | decisions/protocol.md:2164 |
| ## PROTOCOL-68 · `argvBytesMax` is derived from the kernel's call bound, so every admitted call can be confirmed (2026-10-23; CX-DEADLINE, found while landing LANG-76; ROOT for PROTOCOL under R-0069) | decisions/protocol.md:2182 |
| ## PROTOCOL-69 · The journal entry at a call's id is that call's commit; step 3 submits only a call whose bytes read back as itself (2026-10-23, CX-BACKLOG-2; cv 01a16821-5835, HOSTING-44's second gap; R-0069) | decisions/protocol.md:2188 |
| ## PROTOCOL-70 · A frame is bounded AS A WHOLE: the page budget is the frame less the continuation that asked for it (2026-10-24, FIX-PROTOCOL; readers A3, READ-PROTOCOL D1; R-0069, R-0071) | decisions/protocol.md:2214 |
| ## PROTOCOL-71 · `nd cancel` ends `ok` only on follow's own World: the writer's `refused cancelled` starts a second catch-up (2026-10-24, FIX-PROTOCOL; readers A7, READ-PROTOCOL D2; the class PROTOCOL-64 closed at step 4) | decisions/protocol.md:2236 |
| ## PROTOCOL-72 · Three row plants that tested something else, and a bound's doc that named the wrong owner (2026-10-24, FIX-PROTOCOL; READ-PROTOCOL B3, B4, B8, Q8) | decisions/protocol.md:2248 |
| ## PROTOCOL-73 · Follow's stale-BEHIND test asks what the Host asks, in its order: `signedBy`, then `checkPins` (2026-10-24, FIX-PROTOCOL; found by FIX-KERNEL after KERNEL-66) | decisions/protocol.md:2255 |
| ## PROTOCOL-74 · Members compare heads: `nd sync --to STEPS:CHAIN`, `--attest`, `--check ATTEST`; a fork is refused `forkedWorld` by name (2026-10-26, FABLE-TRUST; DESIGN-TRUST T1, `redregg/work/promo/DESIGN-TRUST.md`; readers' §6, HOST §1.3, PROTOCOL §2.3, TOPLEVEL-SPEC §2.3/§11.1) | decisions/protocol.md:2265 |
| ## PROTOCOL-75 · Self-heads through the writer: `nd sync --post OBJ` posts a member's own head into a `Std.head` object of its World, and every follow that absorbs the post compares (2026-10-26, FABLE-TRUST-2; DESIGN-TRUST T2, `redregg/work/promo/DESIGN-TRUST.md` §4.2, §5; with LANG-95) | decisions/protocol.md:2286 |
| ## PROTOCOL-76 · Certified heads, the object: `Authority`, `Certificate`, `domCertify`, `certified`, and the quorum theorem (2026-10-26, FABLE-TRUST-3; DESIGN-TRUST §1.2, §1.3, §4.3: T3's unsigned half) | decisions/protocol.md:2306 |
| ## PROTOCOL-77 · The signed start carries the authority; `Protocol.Head.Authority` is KERNEL-69's object; a step-0 World holds the authority cell (2026-10-26, FABLE-TRUST-4; with KERNEL-69; DESIGN-TRUST T3b, first landing) | decisions/protocol.md:2322 |

### decisions/root.md

| Title or status | Location |
|---|---|
| ## ROOT-HBOX · main lives on hbox (2026-10-17) | decisions/root.md:3 |

### decisions/spec.md

| Title or status | Location |
|---|---|
| ## SPEC-1 Claims are predicates on a record of the deployed entry points (2026-10-26) | decisions/spec.md:6 |
| **Status.** open. | decisions/spec.md:36 |
| ## SPEC-2 The layout the closure gates force: the trusted reading lives under `Spec/Proofs/` (2026-10-26) | decisions/spec.md:38 |
| **Status.** open. | decisions/spec.md:59 |
| ## SPEC-3 `Decided`/`Audited`: the kernel's honesty with the kernel a parameter (2026-10-26) | decisions/spec.md:61 |
| **Status.** open; (b) tasked to KERNEL. | decisions/spec.md:82 |
| ## SPEC-4 A1 needs a named relay premise, and its `Start` names the trusted key (2026-10-26) | decisions/spec.md:84 |
| **Status.** open; premise deleted by §11.2. | decisions/spec.md:113 |
| ## SPEC-5 The INHABITED run is computed at the deployed `Ctx` by `native_decide` (2026-10-26) | decisions/spec.md:115 |
| **Status.** open; richer run owed (value, law, a deferred envelope, a settled command). | decisions/spec.md:136 |
| ## SPEC-6 A1's proof sharpens `step_world` inside Spec; B2's floor must be a non-reachable World (2026-10-26) | decisions/spec.md:138 |
| **Status.** open; `step_world` restated as a corollary is PROTOCOL's to take. | decisions/spec.md:158 |
| ## SPEC-7 The floors of B2 and B3: two kernels with one check missing, run at the deployed `Ctx` (2026-10-26) | decisions/spec.md:160 |
| **Status.** open; the law-chain floor owed. | decisions/spec.md:199 |
| ## SPEC-8 C(ii)'s cancel arm and C(iii)'s stale arm are claims; C(ii) and C(iii) are inhabited at the Store's digest (2026-10-26) | decisions/spec.md:201 |
| **Status.** open; the cancel run and B3's law-judged run owed. | decisions/spec.md:244 |


## Additional header findings from definition-level recheck

### Lang/Wire.lean
| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header tag inventory lists all term and primitive constructors | STALE | Lang/Wire.lean:82; Lang/Wire.lean:180 | Add hole tag 18 and u64be/sized/dsized primitive codes 12/13/14; definitions already implement them. |
| Scalar fields use ordinary shared codecs and term/type trees use shared depth-bounded framing | TRUE | Lang/Wire.lean:58; Lang/Wire.lean:95; Codec/Tree.lean:52 | Retain conversion/byte-level proof separation. |

### Codec/Proofs/Deployed.lean
| Claim | Verdict | Evidence path:line | What to do |
|---|---|---|---|
| Header says the deployed instance satisfies what kernel theorems assume | STALE | Codec/Proofs/Deployed.lean:12; Spec/README.md | Limit this statement to codec laws and decoded-World invariants; cryptographic/composed premises remain explicit. |

The additional header corrections were included in the direct landing after ROOT replaced the judge workflow. They change comments in Codec/Tree.lean, Codec/Sha512.lean, Codec/Deployed.lean, Codec/Proofs/Deployed.lean and Lang/Wire.lean. Their rationale is retained in ROOT-DOCS; no per-landing decision entry was added. No theorem gains a hypothesis or is restated.


## Final upstream delta and disposition

The rewrite landed as 95f4ea926df3920ddec6fd3eafeab4755cfb0076; 80c622afbed15bea1d236dbdbb6f1eb16189a079 refreshes SIZE after rebase and spells out the size_limit report name. Both were verified on origin/main. All 30 archive files are removed; seven guides replace them. The eleven changed Lean files have identical comment-stripped tokens to the parent source. Final new-page link check: 61 relative links, all resolving. README is unchanged by this lane.

ROOT's WORK-RULES-20261027.md replaced the per-landing judge workflow during this work. JUDGE describes direct rebase, scoped build/test and push; convergence is a report. The old GATES/assembly process descriptions in the audited snapshot are now HISTORY as operating policy, even where their scripts remain in the tree. The initial twelve source groups passed before this policy replacement; no later runtime execution is inferred from that pass.

| Newly integrated source | Claim and verdict | Evidence / disposition |
|---|---|---|
| deploy/testground/run.sh and its service | TRUE: foreground serve supervises the three processes; unit is Type=simple with Restart=on-failure. The earlier forking-unit table is historical. | CLIENT-47 diff read; TESTGROUND updated. |
| deploy/testground/run.sh, guestbook/relay and README | TRUE: fork copies the same genesis for a demonstration and GET /attest exposes a guest-book head; reached chain mismatch refuses forkedWorld. | CLIENT-47 source diff read; TESTGROUND distinguishes this from a multi-writer operating mode. |
| testground/build/build.sh | TRUE: pinned libuv headers, content-named objects and deterministic link input list replace host-header/mtime assumptions. | Full changed build-script diff read; existing c/wasm/all forms remain. Emscripten absent here, so no new browser-build claim. |
| scripts/hooks/commit-msg | HISTORY: it refused plain commits; ROOT deleted it in 5a3c2229. | First direct commit encountered it; commit-only override was temporary. Subsequent normal commit and pushes succeeded. |
| scripts/pre-push usage comment versus scripts/gate-lib.sh | STALE: comment says 30-minute slot deadline; helper actually defaults to four hours and reports every thirty minutes. | Recorded for ROOT/GATES retirement with the obsolete judge; not copied into the new landing guide. |
| SIZE.md generator's gate prose | STALE under the new policy: old ceiling/landing-form instructions remain generated text. | Numbers refreshed; generator wording should be retired with GATES' obsolete authorization workflow. No policy gate retained by the new guide. |
| Sibling README landing | Integration boundary: sibling report says its README commit 4bb86ead landed only on hbox's local main and its push was refused; it still directs readers to docs/record. | ROOT must integrate it and point navigation to docs/OVERVIEW.md / decisions/root.md. This lane did not edit README. |

Paused operational work remains explicit: no key creation, deployment mutation, provider call or publication was performed. The command forms were checked against parsers and existing source/test consumers. The obsolete scripts/commit job (PID 726955, with its original PID file) remains alive in its captured snapshot after the direct push; ROOT is notified in the report. It must not be treated as the authoritative final documentation snapshot.
