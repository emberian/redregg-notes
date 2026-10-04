# Morning map — Mini, 2026-10-04

Written by the root (Claude, session breadstuffs-89) overnight, for Ember and the root to restart from.
It is built from: every substantive root message of last night (recovered with `cv` after the
compaction), the swarmplan v2, both Fable reviews, scout A, the shared-contracts / Bend-direction /
authenticated-quote notes, two orientation readers that checked about 900 KB of design notes and
repo docs against main (`ORIENT-A-LANGUAGE-COMPUTE-20261004.md`, `ORIENT-B-WORLD-PRODUCT-20261004.md`,
both in this directory, with per-document status tables), and direct checks on main.
Tags where they matter: READ (seen in source on main), RECORD (a report or ledger says it).

## 1. Where things stand at about 04:00

- **Main** is `711cf095`: about 95 commits past the swarm's start (`c8fdd000`). Everything that
  landed overnight is listed in `SWARM-LEDGER-20261004.txt`.
- **CI on main is red, and has been since `6f2ea54d`.** Its reds are StoreHiding rewrites, a stuck
  typeclass in `Kernel/TurnOfIntent.lean:455`, the proof-hygiene gate, and (reported) `sorryAx`
  under PayCellUpgrade. The run then times out (READ, run 37183441505). These are the
  never-compiled-base reds the cut exists to clear. The rebase lane has them as its green bar.
- **The cut is green but not landed.** It is green at `0f8322e7` on old main (`17a6489c`): umbrella
  plus `Host.Main` plus the new `ObjectiveProofs` target, 9602 jobs, host closure 613 modules with
  no BendTT. It deletes Gen-1, `Command.bend` and the BendTT command path. It fixes two real defects:
  - one nonce could be spent once per distinct family-command body;
  - dry runs were judged by an accept-all gate.

  A rebase lane is rebasing it onto main and doing the one cold build that becomes THE warm base,
  at `/tank/dregg-build/claude-lanes/warm-base`, with an `mk-lane.sh`. Until it lands, Gen-1 is
  still on main (READ) and the docs say so.
- **The workbox cleanup.** No landed work and no lane source was lost. Every surviving lane's
  commits, diffs, untracked files and status files are rescued to
  `/tank/dregg-build/claude-lanes/wip-rescue-20261004` and to `~/workbox/claude-lane-wip-20261004`.
  The seven surviving mine-now codex directories are copied to
  `/tank/dregg-build/claude-lanes/codex-mine-rescue-20261004`. Three things were lost:
  - **Codex FHE over Objective:** r34 weighted BFV, r35 return-release, r36 consent. Only the design
    notes remain; task `01a105af-d204`.
  - **The live common OO world's store, sponsor directory and binary.** A store copy from 22:55 and
    the key backups survive on `/tank/claude-evidence-20261004`. The process still runs from the
    deleted inode and will fail at its next store access. Re-home or re-genesis is your call, below.
  - **Compiled build outputs.** This costs about two hours of cold build, nothing else.
- **Lanes running now:**
  - the rebase lane;
  - proof engineering (pin command, statement-snapshot gate and vacuity probes re-committed; now
    splitting Preservation into per-constructor lemmas);
  - follow-ups;
  - the fast machine (proved `@[csimp]` linear-heap machine, waiting on the base to commit);
  - four Sonnet lanes: Rust fixes, deploy config, private rooms with PQ hybrid, SDK pinned to the
    Lean codec.

  Finished and landed overnight: hygiene (62 of 74 landed tasks closed), the collective, commons
  and station ports, and the market ports. All surviving Gen-1 domain programs now exist as `.obend`.

## 2. Decisions that are yours (ranked by what they unblock)

1. **Common world:** re-genesis a fresh one from the post-cut base, or re-home it from the 22:55
   copy (losing anything written after it). Task `01a105b6-8396`. Root's lean: re-genesis; nothing
   depends on its history except Studio demo state.
2. **Executor for admission:** keep Lean `runBounded`, now that the proved fast machine exists
   (measure it first), or put the C machine behind the differential gate as the native executor
   with Lean as its specification. Task `01a10564-84ef`. Root's lean: land the fast machine,
   measure, and decide with numbers. A C executor adds a trusted 1.5k-line C file to admission.
3. **The charge law:**
   - **The three options:** clear execution charges measured ticks, private profiles charge a
     signed envelope; or everything charges a signed versioned envelope (ticks plus heap/stack),
     refused on excess and never refunded; or gas on a shared IR.
   - **Why it matters now:** today a caller sets `proofWork` and zero is free (READ R2-2). The
     zk-truth lane showed measured ticks leak the secret branch.
   - **Root's lean:** one signed envelope for all profiles, which is simplest and leak-free.
4. **BendTT remainder:** after the cut, about 258 BendTT-side modules stay as files outside the Host
   closure, plus `native/fhe-bend`'s BendTT artifacts and `bend-ir2-proof`. Delete now, or port the
   reusable parts first (generic Air/Emit, the BendNatural compiler shape, the oblivious blocks).
   Root's lean: port the named reusable pieces in one lane, delete the rest the same day.
5. **Multi-machine model:**
   - **Three answers in the notes:** a witnessed single sequencer (SURPASS and CHANNELS; recorded
     as your resolution in `01a0f711-ffd8`), the built n=4 f=1 Simplex mesh, or ARCHITECTURAL-ARGUMENT's
     scoped joint turns with a last signer.
   - **What it decides:** whether the agreement lane's fixes go live or the mesh retires.
6. **Where a program lives:** DEOS says a law plus a runner, never code in a cell. EVENTS and
   BIGDREGG make Objective Bend activities the deos scripting language. Root's lean: activities,
   with the law as the admission bound around them, since that is what got built and proved.
7. **One traffic stack and one key-exchange family:**
   - **Traffic:** CHANNELS (Lean epoch records) and the PQ cohort mix (Rust) share no code.
   - **Key exchange:** channels use X25519, traffic pure ML-KEM-768, rooms are moving to the
     hybrid.
   - **Root's lean:** hybrid everywhere, keep the cohort mix, and fold the channel epoch records
     into it.
8. **Tenancy versus go-live:** split tenancy refuses `discord.env` and `provider-service.json`, while
   the product plan turns on Discord and pooled Hermes. The key-service behind a `mini-core` socket
   is the reconciling design (step B, "by ear").
9. **Already open in your inbox:**
   - sponsor key custody (default A lands in three days);
   - GitHub drafts;
   - dregg-infra push (split tenancy and `jdeploy3` exist only on `hbox:/srv/git`);
   - Discord app;
   - friend #1;
   - the live SPK app 8502's refused attempt;
   - a clock-ticker step bound.

## 3. The pillars

Each pillar gets its current truth and next moves in dependency order. Task ids are `cv task`
prefixes.

### P1. Objective Bend, the language

**Truth.**
- Core4 is the only kernel. It has lazy fix and mix, specifications, prototypes, reflection, sums
  (`inject`/`case`/`ifBool`/`labelEqual`), activities (`perform`/`done`/`yielded`/`resume`,
  `Activity<P,R,A>`) and a checkpoint codec.
- A certifying checker sits under adequacy, preservation, completeness (`coreRepresentation`
  inhabited), `forceWith ≡ runBounded`, deep data soundness, and typed perform, done, resume and
  yield. Every proof has its axioms pinned, and there is no sorry.
- **The proofs are in no default target on main** (READ): only `ResearchWip` imports them until the
  cut lands `ObjectiveProofs`.
- **Front end:**
  - The TypeScript elaborator is the implementation; the Lean one (1,390 lines) only
    translation-validates it.
  - The surface has ancestry with C4 linearization, method combination, affine and linear,
    spec-typed packages, and a root that is a specification.

**Faré maturation:**

| Move | State |
|---|---|
| Sums | done with metatheory |
| Effects as yield | done with metatheory |
| Declared ancestry, linearization, method combination | done at elaboration; the ordered-presentation invariant is only a Prop (`01a10500-6ea2`) |
| Checked `requires` and closed-object discharge at fix | not built (`01a10500-6f6f`) |
| Extensible root | done |
| Label equality | done |
| Dynamic get and generative identity | not built |

**Gaps scout A ranked further down:**
- the consumed mark for linear values;
- a custody-introducing term;
- the reflection observability contract, which must come before any reflection constructor;
- governed evolution with migration lemmas;
- laws as checked evidence.

**Surface gaps users hit tonight:**
- no `-`, `<` or `<=` (the parser accepts them but the elaborator does not lower them);
- no `let`, and one-line expressions;
- preview shows only the label of a sum-typed result;
- recursive data;
- the typing proposal explodes to about 235 MB per item on nested records (`01a105ba-6d10`,
  `01a105a2-bc23`);
- a canonical-shadowing shareability hole to audit (`01a10505-46cf`).

**Next moves:**
1. The cut lands; `ObjectiveProofs` and the front-end gate (landed tonight, `e512de81`) run on the
   warm base.
2. Lean elaborator becomes THE implementation, the TypeScript one is deleted, and the parser pins
   and captured packages are re-emitted (`01a10500-6e65`, `-6eef`).
3. Surface completeness: operators, `let`, recursive data, deep-forced preview, typing-proposal
   sharing.
4. Checked `requires` with final-self discharge, then laws as checked evidence. This is the next
   Faré move and the one Preoscript's futures plug into.
5. Dynamic get with generative identity, after deciding the reflection observability contract.

### P2. Engines and cost

**Truth.**
- `runBounded` is the specification.
- The C machine is `stepRaw` transcribed. It agrees on 340 of 340 differential cases with mutants
  caught, and is 900 to 2,900 times faster. Nothing proves it equal to `stepRaw`.
- The proved fast Lean machine (`stepRaw_eq_fast`, `step_eq_fast`, `runBounded_eq_fast`,
  `@[csimp]`) exists in the fast-machine lane, not on main.
- HVM, interaction nets and upstream `comp.ts` transfer nothing; parallelism comes across runs.
  This is the backends lane's verdict.

**Next moves:**
1. Land the fast machine and measure admission re-execution before and after.
2. Decision 2 (the executor).
3. Gate the C differential, then the C ≡ `stepRaw` refinement (`01a10564-8480`).
4. Decision 3 (the charge law), then implement the tariff in admission.
5. One code table and one State format for the C machine and the oblivious network (`-84c3`).

### P3. Native admission: the first Objective Accepted

**Truth.**
- The 15-hop chain from a member's Studio edit to an admitted native receipt was rebuilt in lanes:
  Claim v4, NativeAdmission with a read oracle that defaults to a named refusal,
  AuthenticatedInputs, the layout lemmas (execute once with no command, lay out the targets, gate
  once), the quote producer, Core227 consent, and Studio wire v2.
- None of it is on main. It sits on the cut's base in the native-b lane (rescue copy and successor
  brief exist).
- No receipt has ever been produced. Core4 is not in the evaluator registry, which is still
  `[nock]` (READ).

**Next moves (task `01a105bb-e2a2`, filed tonight):**
1. Native host from the warm base.
2. Genesis with the invocation policy pin.
3. Publish, signed queries, quote, op-227 signing, submit, readback.
4. The ten refusal checks.
5. Native part A: the tariff, the elaborator and lowerer pin bound into package identity, real route
   guards, a Core4 registry entry, `semanticId`/`artifactId`, a private-return slot.

This is the single most important integration milestone. Everything in P4, P6 and P11 consumes it.

### P4. Persistence and residents (the deos-js replacement)

**Truth.** The language side is complete: yield is a safe point, resume is typed, the checkpoint
round-trips, and the C machine resumes from a state Lean saved. Bread's counter applet exists as
`.obend`, and the commons runs as an Activity for 13 turns in preview. **No kernel delivers a
response to a yielded activity or stores its checkpoint.**

**Next moves:**
1. Kernel delivery: an activity record with a generation compare-and-swap, checkpoint storage and a
   typed response (`01a1056f-0066`). Read the mined codex `ObjectiveActivity` modules first.
2. The adversarial note's attacks as tests: forged checkpoint, double resume, a stale worker
   publishing after handoff, revocation with a dispatch in flight.
3. Within-turn non-divergence for residents, or a budget-is-the-contract decision (`01a1056f-0083`).
4. Heap collection at yield; the checkpoint currently grows about 120 tokens per turn (`-00a4`).

### P5. World kernel structure and efficiency

**Truth (READ unless marked):**
- There are 33 hand-written `receiveLoaded` receiver families.
- `protocol/host-operations.json` is a hand-kept twin of the Lean dispatcher.
- `HostRefinesWorld` is imported only by the umbrella, so no theorem relates the Host's dispatcher
  to the world step.
- Admission runs on `DataIntent`, not `World.step` (SURPASS T4).
- About 30 entry points prepare before verifying a signature, 17 of them with their own admission
  copy (RECORD, ship-fix receiver sweep).
- Incremental audit, D12, D15 and D16 landed; the cold audit was 1064 s at 78 records on a loaded
  box and has not been re-measured.
- Held, breaking (re-genesis), needs a host build: room schema v2 (a v1 room read takes 4.95 s with
  1,015 proof items) and the indexed session with per-record receipt roots.
- The `room new` exchange count is unmeasured since the rewriter's in-process chat landed.

**Next moves:**
1. Land schema v2 and the indexed session on the warm base, with before and after numbers
   (successor brief in the rescue set).
2. Re-measure the audit and `room new`.
3. **Collapse the receivers**: one `Receiver` declaration with its standard definitions and theorems
   proved once. Both Fable reviews rank this the largest reduction in lines and risk.
4. One Lean `HostOp` table, with the JSON and Rust constants emitted from it.
5. Live-equals-replay (`01a0f6c5-6891`), then T4 host cutover (submit = `World.admit`), then import
   `HostRefinesWorld` into `Host.Main` with `Turn.ofAdmission` derived from the `Accepted` object.

### P6. Graded and private execution: zk, oblivious, FHE, MPC

**Truth.**
- Mini admits nothing by proof: `witnessed` compiles to false and re-execution is the check.
- zk-truth's findings, all authored and uncompiled, in the rescue set:
  - `PackedRefinement` was trivially inhabitable;
  - the oblivious tranche's decoder does not bind the code rows, so the bits for one program decode
    as another;
  - measured ticks leak secrets;
  - padding hides nothing without hiding-PCS randomness.
- MPC runs a width-8 adder over genuinely private inputs with per-dealer entropy and a
  transcript-secrecy check (landed).
- FHE is BFV 2a+b with one owner; the Objective work was lost. The BFV noise theory is ported and
  finds depth 2 in doubt, and no smudging radius reaches 48-bit hiding on this chain.
- Graded and priced execution contracts are entirely design (GRADED-EXECUTION-ARCHITECTURE plus its
  JSON sketch).

**Next moves:**
1. Compile and land zk-truth (the corrected codec statement; bind the code, environment and field
   regions).
2. The signed tariff (decision 3) in the proof emitter as well.
3. Rebuild FHE over Objective on a Core4 producer (`01a105af`), then check worst-case key-switch
   noise against the depth-2 ceiling (`01a10501-82d1`).
4. One small `ExecutionContract` over one real `.obend` consumer answering accept, reject or
   unknown, with the sketch's prohibited fallbacks as gate rows.
5. Mine the private committee v4 (`01a10556-494b`).

### P7. Logic compilation (fixed-program circuits)

**Truth.** Every checked compiler on main binds BendTT Books. ObjectiveNatural (addition, proved
against the source relation) sits in the rescued `codex-bend-logic` directory. The generic Air/Emit
stack is reusable.

**Next moves:**
1. Decide what circuits refine: make `stepRaw` the single hub, or prove the source-relation link
   once.
2. Mine ObjectiveNatural.
3. A Core4 specializer: partially evaluate public fix and mix, and lower `case` to a mux over both
   arms.
4. Subtraction, comparison and multiplication with no-wrap proofs.

### P8. Contracts, laws and Preoscript

**Truth.** `Kernel/Contracts/*` holds the identities, the six authority cuts, the typed snapshot
classes and future-indexed certificates over Mini's accepted history (landed; research target).
Refinements into the existing per-domain types were never compiled (rescue set). Laws and
`requires` are unchecked in the language.

**Next moves:**
1. The SDK pins its intent bytes to the Lean codec (in flight, S10).
2. Compile the contract refinements and collapse the seven Observation types into them.
3. After P1.4, the first Preoscript port: a future-indexed certificate on one authored view.

### P9. Docuverse, deos and Studio

**Truth.**
- Most of DEOS's floor is built: element tree, transclusion, marks, history, `can`, templates, web
  pages that accept writes.
- None of it is reachable by members.
- Studio's prototype declarations were Gen-1 and are deleted by the cut. The r26
  definition/publication work is in the rescued `codex-docuverse-studio`.
- The event-log twin was decided "delete" and still exists.

**Next moves:**
1. Delete `HyperdocumentEventLog` and `LegacyContentCarry` (greenfield: refuse, do not carry).
2. Studio on `.obend` and mine r26.
3. One ObjectPresentation projection shared by web, Discord and Hermes.
4. A member-reachable Studio route, which needs the thin-peer consent producer named in the SDK
   design.

### P10. Privacy: rooms and traffic

**Truth.**
- Rooms were rebuilt last night with founder-pinned lineage, two-phase release, and protected-atom
  version binding. S9 is adding the ML-KEM-768 + X25519 hybrid, one invite path, founder rotation,
  per-wrap grants and an end-to-end driver.
- Traffic profile P1 is a single-host cohort of 4 with roster enrollment. The endpoint sees the
  plaintext, and no new effect has gone through it.

**Next moves:**
1. Rooms end to end on a real Host.
2. Traffic: Linux roster qualification, a first new effect through the carrier, then two hosts with
   Wi-Fi power-save off.
3. Decision 7.

### P11. Agreement

**Truth.**
- The engine and its Lean safety theorem are on main.
- Fixes A and B installed the stalled call 00f711 on a copy (737 s, identical receipts), with a 23 s
  p50 round trip. The commits are merged but uncompiled in the lander clone.
- The journal decoder overflows the stack on long journals.
- The live mesh is unchanged and still stalled; fresh devnet keys for three hosts exist.

**Next moves:**
1. Fix the decoder.
2. Compile and land the merged commits.
3. Find the 20 s per iteration.
4. Fix C plus the safety re-check (re-genesis).
5. Decision 5, then move replicas (never copy them) onto three or four failure domains.

### P12. Apps, SPK and Hermes

**Truth.**
- The physical layer is hardened.
- Main lacks the failed-START recovery the live r2 world ran; the tars are on
  `/tank/dregg-build/codex-runtime-spk-recovery-20261003`.
- v4 is held for the cut.
- Broker and resident bootstrap need root.
- No app has served a browser session.
- Hermes has only run with a scripted provider.

**Next moves:**
1. Mine the recovery and land v4.
2. Store ids in unit names.
3. A lawful g4 START, then a browser session (Playwright EtherCalc to a shared doc).
4. HERMES-LIVE on a scratch world.

### P13. Payments and enrollment, product and the public node

**Truth.**
- The public node runs `5688775a` (10-01). No friend is enrolled.
- The packager and the composed strict gate are on main; `jdeploy3` exists only in dregg-infra on
  hbox.
- The smoke gate is red on apps, residents and protected documents.
- "Two friends plus Hermes" has never run anywhere.
- The enrollment address and the 50 DREGG/week rate are decided; S7 is wiring them and the age
  backups.

**Next moves:**
1. DEPLOY-3 candidate from post-cut main.
2. `jdeploy3` green, or ship with the red rows named.
3. Consent binaries and env vars in `FRIENDS.md`, which disagrees with main in four places
   (ORIENT-B table).
4. Refusal charging and tickets.
5. Split tenancy on the box.
6. Friend #1.

### P14. Process and assurance instruments

**Truth.**
- Proof engineering has re-committed:
  - an `#assert_axioms` command (402 hand pins become 30 commands);
  - a statement-snapshot gate (1,721 statements and 1,279 axiom sets identical before and after);
  - the ledger's covered-consumer rule;
  - a trivial-inhabitant probe.

  All of this lands after the cut.
- `sourceGate` still defaults to accept-all (`01a105a2-bbeb`).

**Next moves:**
1. Land those instruments.
2. Run `scripts/local-gates.sh` from the warm base before every landing. Two reviews found that the
   gates are well designed and simply not run.
3. Remove the accept-all default.
4. Fold the retrospective's five rules into the lane protocol for every successor:
   - capability state moves only by an artifact a non-author re-ran;
   - tests land in a gate in the same commit;
   - diagnose after a second failed retry;
   - a cold-readable STATUS;
   - a named consumer.

## 4. How the morning starts

When the rebase lane reports green: land the cut. Advance main's CI to green; it has been red since
`6f2ea54d`. Announce the warm base. Then launch about ten successors from their briefs, roughly in
this order:
1. NATIVE-ACCEPTED (P3).
2. Schema v2 plus indexed session (P5.1).
3. Agreement (P11.1–2).
4. Fast machine landing and measurement (P2.1).
5. zk-truth compile (P6.1).
6. SPK recovery plus v4 (P12.1).
7. Kernel activity delivery (P4.1).
8. Receiver collapse design and first family (P5.3).
9. Lean elaborator as the implementation (P1.2).
10. DEPLOY-3 candidate (P13.1).

Ship-fix items 4 and 6, the contracts refinements, and Bread's Cert-F and reconfiguration restore
from the rescue set into whichever of these lanes owns their files.

The decisions in section 2 can be taken in any order. Decisions 2 and 3 change what NATIVE-ACCEPTED
builds, so they are best taken before or during its first hour.
