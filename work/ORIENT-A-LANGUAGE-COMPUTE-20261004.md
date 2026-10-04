# ORIENT-A — language and compute: the 2026-10-03 design notes against Mini main

Read-only orientation, written 2026-10-04 by a Claude reader lane (Opus 5.5). Nothing was
built, edited or committed. This is the only file the lane wrote.

**What was read.** All thirteen notes in `/Users/ember/dev/redregg/designs/`, in full.
A fresh clone of `github.com/emberian/minidregg` main at **`1ffe6bf3`** (2026-10-04 02:42 -0400).
On main: `docs/OBJECTIVE-BEND*.md`, `docs/BEND-*.md`, the repo copies of three of the notes,
`docs/objective-bend/evidence/STATUS.md` and `docs/design/*`, plus targeted greps of
`Theory/ Compiler/ Kernel/ Host/ Assurance/ native/`. Also the swarm ledger
(`redregg/work/SWARM-LEDGER-20261004.txt`), the task backlog (`TASK-BACKLOG-20261004.md`),
and a dump of `cv task list --all --tsv` (588 rows, 381 open). Over read-only ssh to hbox:
the cut's warm base, the fastmachine lane and the zk-truth lane.

**Tags.** **READ**: I read the code or doc, or saw the file exist in a listing or grep.
**INFERRED**: a conclusion from what I read that I did not check directly. A task
"exists" only if a title in the cv dump matched. Each task check below is a keyword grep
over titles, so a task buried in a body can be missed.

---

## 0. Cross-cutting facts that change how every note reads

1. **`docs/EVAL.md`, `docs/COMPUTE.md`, `docs/ZK.md` and `docs/ZK-TRUTH.md` do not exist on
   main.** Git history does not have them either (READ: `git ls-files` and a log search
   for deleted files). `ZK.md` exists only as cv task `01a0f6ae` ("ZK.md: research +
   safe-now lanes"). `ZK-TRUTH.md` exists only in the zk-truth lane clone,
   `hbox:/home/hbox/workbox/claude-zktruth-20261004/src/docs/ZK-TRUTH.md` (commits
   `932ea893`, `82548487`). It is authored, not compiled and not landed. I read it in
   full (READ). It is summarized under note 6.
2. **Gen-1 is still on main.** The docs on main say it was "deleted on 2026-10-04", but
   `Compiler/ObjectiveBendLinker.lean`, `ObjectiveBendElaboration.lean`,
   `ObjectiveBendWorkshop.lean` and their siblings are in the tree (READ). The deletion
   lives in the cut: `hbox:/tank/dregg-build/claude-lanes/warm-base/src` at `0f8322e7`,
   built on the old base `17a6489c`, with a rebase in progress (READ ledger and ssh).
   After the cut, **about 258 BendTT-side `Bend*` modules remain as files** (BendLogic*,
   BendNatural*, BendOblivious*, BendWorld*, BendActivity*, BendClosure*, BendTTSource,
   BendLiveMachine). They leave the Host closure (READ: warm-base listing; ledger line
   "host closure 613 modules, no BendTT"). Whether to delete them or port them is an open
   decision (see the synthesis).
3. **`docs/OBJECTIVE-BEND.md` §"What is open" is already stale against main's code.**
   Main has:
   - `Theory/ObjectiveBendDemandCompleteness.lean`: `machine_evaluation_complete`,
     `runBounded_finite_completion`, and `coreRepresentation : Representation State
     (Scoped 0)`.
   - `Theory/ObjectiveBendDemandDataSoundness.lean`: `forceWith_unrestricted`,
     `materialize_sound` and `force_field_sound`.

   (READ grep.) The doc still says completeness, `forceWith ≡ runBounded` and deep Data
   soundness are open, and that `Representation` has no instance. Its "Known front-end
   defects" list is partly stale too. The parser now refuses `./NAME.bend` imports
   (`objective-parser.ts:147`, READ). Shared `compose` and the affine/linear surface
   landed in `31d8643e` (READ ledger 04:10). The repo copies of
   BEND-PERSISTENT-COMPUTATION and BEND-DATA-REPRESENTATION were rewritten for Core4 on
   2026-10-04, but they still say "no sums" and "no yield". Both landed since (READ).
4. **None of the Core4 proofs is in a default build target on main.**
   `Theory/ObjectiveBend*` is imported only by `ResearchWip.lean`. `BendQualification`
   imports only `Kernel.ObjectiveBendCallContext` (READ). The cut adds an
   `ObjectiveProofs` target ("umbrella + Host.Main + ObjectiveProofs 9602 jobs rc=0").
   READ in the ledger, not seen on main.
5. **The brief's Core4 inventory, checked against main:**
   - **On main.** Lazy demand machine (`stepRaw`/`runBounded`); sums (`3dc6a602`);
     activities with `perform`/`done`/`yielded`/`resume`, `Activity<P,R,A>` and a
     checkpoint codec with `state_roundTrip` (`2ccd6290`, `d3e213be`); certifying
     checker; adequacy, preservation, completeness and data soundness. All READ.
   - **Lean elaborator.** `Compiler/ObjectiveBendElaborate.lean`, 1,390 lines. It is
     translation-validated against the TS elaborator, but the TS one is still the
     implementation (task `01a10500-6e65`). Its header says "There is no adequacy
     theorem yet" (READ).
   - **C backend.** `Compiler/ObjectiveBendEmitC.lean` plus
     `native/objective-emit/runtime.c`, with activities since `6909eaf9`. Differential
     only, 340/340; no refinement theorem (READ BACKENDS doc).
   - **The proved fast Lean machine (`@[csimp]`) is NOT on main.** It is an uncommitted
     file in the fastmachine lane:
     `hbox:/tank/dregg-build/claude-lanes/fastmachine/src/Theory/ObjectiveBendDemandMachineFast.lean`,
     386 lines, with `stepRaw_eq_fast`, `step_eq_fast` and `runBounded_eq_fast` as
     `@[csimp]` (READ ssh).
   - **No native Accepted.** "On main, no Objective Bend source has produced a native
     accepted receipt" (READ OBJECTIVE-BEND.md). `Kernel/ObjectiveBendNativeAdmission`
     exists only in the warm base (READ).
   - **No cv task names the first native Objective receipt** (grep: none). The W1.2
     successor brief is in that lane's STATUS.
6. **Much evidence cited by the notes is gone.** The 02:38 hbox workbox wipe removed
   `codex-homomorphic-bend-20261003` (every physical BFV run log: run-literal-01,
   run-mux-01, run-prelude-01, and FHE over Objective r34–r36), `codex-bend-trace-20261003`
   and `codex-unified-integration-20261003` (READ: ssh existence checks).
   `codex-bend-logic-20261003` and `codex-bend-world-20261003` survive. Treat the
   physical-run claims in notes 2, 9 and 10 as **record only** from now on.
7. **Mini admits nothing by proof.** `Compiler/Evaluator.lean:431` is
   `def registry : List Evaluator := [nock]`. `Compiler/PredCompile.lean:600` lowers
   `witnessed` to constant false. `PrivateComputationKind` is
   `witnessZk | sharedMpc | encryptedRnsFhe`, an artifact discriminator only (all READ).
   Re-execution is the only admission check.

---

## 1. GRADED-EXECUTION-ARCHITECTURE-20261003.txt (Codex, graded_execution_architecture)

**(1) Central claim.** Execution should be a checked composition of contracts over one
program meaning, not a `Native|ZK|MPC|FHE|TEE` mode enum. Three objects stay separate:
*Meaning* (checked program, typed interface, exact outcome/effect relation), *Contract*
(permitted observations per observer, authority, resources, assumptions, progress) and
*Realization* (a typed plan DAG of compute/bridge/prove/verify/custody/reserve/install/
release nodes, with checked refinements and deployment evidence).

The "grade" coordinates (use, information flow, effects/authority, cost, DP, precision,
assurance, trust, progress, mobility) each have their own algebra, and many points are
incomparable. Leakage is ordered by factoring (`L1 ≤ L2` iff `L1 = f ∘ L2`). Composition
is partial and needs a whole-plan certificate (R1–R10). R9 says metering must not
disclose secrets; R10 says no downgrade fallback. The planner answers Accept,
Reject(reason) or Unknown(obligation), and Unknown never authorizes.

**(2) Status: DESIGN-ONLY for its own proposals; PARTLY for its foundations.**
- The three proposed modules do not exist on main: `Theory/ExecutionContract`,
  `Compiler/ExecutionPlan`, `Assurance/ExecutionPlanRefinement` (READ).
- The foundations it cites do exist (READ): `Theory/PrivacyProfile`,
  `PrivateComputationDeclaration`, `DisclosureDeclaration`, `TypedAuthorization`,
  `EffectDeclaration`, `ResourceCost` (25 theorems), `IndexedProgram`;
  `Compiler/Evaluator`, `SemanticManifest`, `PredCompile`, `WorldExecutionContract`;
  `Kernel/DeclaredResourceController`, `PrivateEscrowSettlement`.
- The semanticId vs plan-digest split exists only on the BendTT side
  (`Compiler/BendWorldProgramCodec`, `BendInvocation`, `Host/BendSessionDriver`,
  `Host/BendFheArtifactCheck`). No Objective module mentions `semanticId` (READ grep).
- Its "Bend pin / Quan / Q0-Q1-Q2" analysis and its owner roster (codex lanes) are
  **OBSOLETED** by the Core4 decision and the end of the codex week (READ).

**(3) Still right under Core4.** Everything structural:
- the separation of meaning, contract and realization, and no mode enum;
- leakage indexed by observer, with metadata as first-class observations;
- R3: both-arms evaluation is fine only for pure candidates, and exactly one plan is
  admitted;
- R9, now confirmed by the zk-truth lane's step-count leak (note 6);
- R10: no downgrade fallback;
- Unknown is not authorization;
- a refusal is never a zero result;
- canonical charge differs from physical cost.

**Must be restated.**
- *Meaning* is now a closed Core4 `Term` that `Typing.check` accepts, run by `runBounded`.
  On the Plan path it is run by `executeWith`, which equals `runBounded` per
  DataSoundness.
- The *use* coordinate is Core4's quantities (erased/affine/linear/unrestricted). They
  are only static: "no theorem says a value is used at most once at run time" (READ
  OBJECTIVE-BEND.md).
- The *effect* coordinate is the `Activity<P,R,A>` computation type.
- The *cost* coordinate is the vector `Limits` plus ticks that every backend shares
  (READ BACKENDS §"One tariff").
- The first consumer should be a `.obend` program, not a BendTT Bool/enum Book.

**(4) Open frontiers with no task.** Grep for graded / execution.contract / semanticid /
planid / dp / ckks returned 0 open tasks (READ). None of these is tasked:
- an execution-contract/plan-DAG module and its first real consumer;
- semanticId vs artifactId for Objective packages;
- a per-observer leakage card for Objective execution (`docs/TRAFFIC-PRIVACY-PROFILE-P1.md`
  covers traffic only);
- a DP release budget;
- precision/approximate profiles;
- a per-property trust model;
- "no downgrade fallback" as a gate row.

---

## 2. graded-execution-contract-sketch-20261003.json

**(1) Central claim.** A machine-readable twin of note 1. It contains the
semantic/requested/selected separation, twelve coordinates with their algebras, thirteen
observer-projection fields, eleven plan-node families, edge-type fields, nine `satisfies`
obligations and Accept/Reject/Unknown. It lists seven **prohibited implicit fallbacks**
(private→plaintext, shares→coordinator, crypto→hardware trust, exact→approximate,
sealed→public, same invocation→fresh paid call, exhaustion→zero/crash). It names a first
consumer with its refusal list and its receiving falsifiers.

**(2) Status: DESIGN-ONLY.** It marks itself `runtime_authorization: false`. Its
`source_snapshots` hash `/Users/ember/dev/minidregg/...`, the old local Mini, not main.
Its `bend_pin` is BendTT and **OBSOLETED** (READ).

**(3) Still right.** The prohibited-fallback list and the five receiving falsifiers can be
lifted directly into gate rows: same scalar with a different effect target, a public
secret-dependent refund, an epoch-relabelled pad, a serialized private semantic witness,
and release after audience revocation. The `ownership` block is obsolete.

**(4) Untasked.** No task exists for turning the fallback list or the falsifiers into gates
(INFERRED from the grep in note 1).

---

## 3. BEND-LOGIC-COMPILATION-20261003.txt (Codex, bend_logic_compilation)

**(1) Central claim.** One live meaning yields two compilation products. A *universal
machine trace* has a fixed transition schema and varying program/input. A *fixed-program
specialization* partially evaluates public syntax only, turns secret branches into muxes
and caps recursion publicly.

Both need three things: a source-to-machine simulation, a machine-to-constraint
**arbitrary-witness** forcing theorem, and a backend refinement. The constructive DAG is
kept beside the relational AIR, so FHE evaluates the expression rather than solving for
wires. Source charge is never the gate count. Source Nat is never aliased to a field.

Built by the note's end: BendLogicCase, Mux, PreludeCase, PreludeMux and NatAdd; the
BendNatural* reusable numeric compiler; BendArtifactBinding (planId =
cSHAKE `DREGG.BEND.CONSTRUCTIVE-PLAN/v1`). Three artifacts ran through real BFV. Its
top "current update" says Objective arithmetic `weighted(a,b)=(a+a)+b` was compiled and
physically consumed (artifact `218f020c…`, input 2,7 gave 11).

**(2) Status: built on the BendTT path, which is OBSOLETED as the Objective route; the
Objective route is not on main.**
- On main (READ):
  - `Compiler/BendLogic{Case,Mux,MuxEntry,NatAdd,PreludeCase,PreludeMux,Serialize,SignedSemantics,Specialization,Trace,BFVPlain}`;
  - `Compiler/BendNatural{Artifact,CheckedCompiler,Circuit,Compiler,Expression,Method,Refinement,Source,WorldSource}`;
  - `Compiler/BendArtifactBinding`, whose doc header says it binds BendTT Books only.
- The Objective arithmetic (`ObjectiveNatural*`, `ObjectiveNaturalResidual`) is **not on
  main** (READ: files absent). It sits in a codex lane, under MINE task `01a10556-4a0b`.
  `docs/OBJECTIVE-BEND-BACKENDS.md` classifies it as relating to the **source** relation
  (`Step`/`Evaluates`), "not to `stepRaw`" (READ).
- Its physical evidence directory is gone (§0.6).
- The generic machinery it builds on is on main and transfers without BendTT (READ
  existence): `Compiler/Air`, `AirFlatten`, `Emit`, `EmitShare`, `EmitSerialize`,
  `AirRange`, `AirBignum`.

**(3) Still right.** Every structural rule carries over:
- the two-product split;
- the constructive DAG and the relational AIR built from one Plan;
- arbitrary-witness forcing, never honest-witness only;
- public-only specialization, with secret branches as muxes;
- the cache key binds every interpretation parameter;
- integer origin before field reduction, with no −1 residue crossing moduli;
- per-limb no-wrap kept separate from the whole-value range;
- the FHE schema `dregg.bend.public-natural-expression.v1`.

**Must be restated.**
- The anchor becomes Core4 (`Evaluates`, or `stepRaw` for the trace product), not
  Eval/Walk/Book.check.
- Specialization of Core4 must partially evaluate `fix`/`mix` over public specifications.
  It must turn `case`/`ifBool` into both-arm muxes, because laziness leaks through access
  pattern (READ OBJECTIVE-BEND.md §Execution and privacy).
- "One Eval.call = one source step" accounting is replaced by ticks.

**(4) Untasked frontiers.**
- A Core4 fixed-program specializer over sums (mux lowering of `case`/`ifBool`): no task.
  `01a105af` only rebuilds the lost numeric r34–r36.
- Subtraction, comparison and multiplication circuits: MarketMath needs them, and `- <`
  are refused by the front end. No task.
- A decision on which relation (source vs `stepRaw`) circuit products refine: no task.
- A bounded-Nat fail-stop profile for backends: no task (READ grep for
  nat48/bounded/wrap; the hits are unrelated).

---

## 4. BEND-WORLD-LANGUAGE-20261003.txt (Codex, bend_world_language)

**(1) Central claim.** Objective Bend is Mini's own language. Members author partial
specifications, final-self/super, laws and governed evolution. Source packages are
immutable, with sealed imports resolved by digest. A world method is a **pure computation
that returns a typed Plan as data**. The kernel alone admits it, under current
authority, revocation, law, budget and audience.

Further rules:
- References are addresses, not rights.
- Private returns are their own slots, released only through current release admission.
- Messages belong to the atomic successor.
- Artifact identity binds source, elaborated core, toolchain, ABI, arithmetic, charge
  and bounds.
- semanticId (meaning) is separate from artifactId (plan/implementation).
- Canonical gas is defined on a shared IR, never on backend instruction counts.

It built an additive BendWorld* tranche, with BendInvocation, ReturnRelease and an opaque
receiver authored.

**(2) Status: PARTLY.**
- The language decision is **BUILT** as Core4 (READ OBJECTIVE-BEND.md).
- The note's additive tranche is on main and consumes BendTT Books, so it is
  **OBSOLETED** as the Objective path (READ): `Compiler/BendWorldSource`,
  `BendWorldProgramCodec`, `BendCoreAdmission`, `BendWorldPlan`, `BendPrivateCapacity`,
  `BendInvocation`, `BendMethodAttribution`; `Kernel/BendWorldMethod`,
  `BendSourcePublication`, `BendOpaqueResultReceiver`, `BendReturnRelease`.
- Core4's own path:
  - capture and publication as two content atoms;
  - the client `objectiveMethod` family, on main in `native/resource-client/src/workspace.rs`
    and `native/mini-sdk{,-ts}` contracts (READ grep);
  - admission in the warm base only (READ).
- The Plan is `executeWith` output lowered from deep Data. Activity Plans are
  first-order, non-recursive sums with one action per yield (READ EVENTS).
- Admission requires the Plan's effects to equal the command's effects exactly. Known
  holes (READ OBJECTIVE-BEND.md): `proofWork` is caller-chosen, the elaborator pin is
  checked for hex format only, and the route guard lists are empty.
- **No Core4 private-return slot or release exists** (INFERRED: no Objective module or
  doc names one).

**(3) Still right.**
- A pure method returns a Plan, and the kernel admits it.
- A reference is not a right.
- Artifact identity binds every interpretation input.
- Semantic and implementation identity are separate.
- Charge is not backend steps.
- Private return is independent of effects and has its own release.
- Messages are durable and atomic with the successor; no ambient reentrancy.
- Preview against the exact current view.

**Must be restated.**
- Everything about Q0/Q1/Q2, `Book.check`, safe.ts, comp.ts and Nat48.
- The "single tagged dispatcher with descending fuel" was a BendTT termination
  workaround. Core4 dispatch is lazy `fix`/`mix`.
- Cost is ticks plus `Limits`.
- The Plan ABI is Core4's `P` sum.

**(4) Untasked frontiers.**
- The first native Objective Accepted: no task (§0.5).
- A Core4 private-return slot with release: no task.
- An Objective semanticId/planId split: no task.
- Binding the lowerer pin and parser transcript. W1.1 native-A is deferred in the
  ledger. Task `01a10500-6eef` only re-emits pins.
- Messages and multi-action Plans per yield: partial. Task `01a1056f-00a4` covers
  "recursive plan/response data".
- Evaluator registration of Core4 in `Compiler/Evaluator.registry`: no task (INFERRED).

---

## 5. BEND-PERSISTENT-COMPUTATION-20261003.txt (persistent-computation construction)

**(1) Central claim.** Persist the *running activity* in Mini's own store, following FCI
and gerbil-persist. Every pure step boundary is a complete checkpoint. An effect is a
yielded Plan plus a continuation, in one Activity record with no second app journal.

The protocol:
- Durable record and readback come before any external dispatch.
- Retries reuse the same intent identity.
- Ambiguous effects stay uncertain.
- Metacontrol (inspect, export, suspend, migrate) is a set of separate capabilities.
- Advance is fenced by a generation CAS that consumes the exact predecessor.
- Migration needs a real state translation.

**(2) Status: PARTLY.**
- The note's own mechanisms are on main but sit over the strict BendTT closure machine,
  so they are **OBSOLETED** (READ): `Compiler/BendClosureContinuationCodec`,
  `Host/BendContinuationProbe`, `Kernel/BendActivity*`, `Compiler/BendActivity*`. The
  repo copy was rewritten on 2026-10-04 and says none of it transfers.
- **Core4 replacement BUILT (READ):** `Term.perform`/`done`, `Control.yielded`, `resume`,
  `Ty.computation` (`Activity<P,R,A>`), `Refusal.sharedEffect`, and the token checkpoint
  codec `Theory/ObjectiveBendCheckpoint` with `state_roundTrip` for every State. Also
  `typed_yield_quiescent` (every yield is a safe point), `stack_activity_signature` and
  `typed_resume_preserved`. The C machine resumes Lean-saved yields (340/340).
- The checkpoint deliberately carries **no** authority, generation or custody. Those
  belong to the kernel record (READ `ObjectiveBendCheckpoint.lean:6`).
- The kernel side is **not built**: "No kernel delivers responses or persists an
  activity yet" (READ EVENTS). It is tasked as `01a1056f-0066`.
- The repo copy's "WHAT DOES NOT EXIST YET" list (no codec, no yield) is stale (READ).

**(3) Still right.** The whole protocol: one activity record, the durable barrier,
same-identity retry, retained uncertainty, metacontrol capabilities, the generation CAS
fence, and migration only by translation at a safe point.

**Must be restated.** The safe point is now a typed yield (or any step boundary). The
"dependent result type rederived" step becomes checking the response against the
entry's declared `R`. `stack_activity_signature` provides `R`, but general typing of
decoded data is still per value (READ EVENTS "Not proved").

**(4) Untasked frontiers.**
- A metacontrol capability set (who may inspect or export a heap): no task.
- A native step-publication protocol (immutable published State, no effects inside
  `step`): no task.
- Post-durability external dispatch with lost-reply retry: only implicit in `0066`.

Tasked: heap collection at a yield (`01a1056f-00a4`); in-turn non-divergence and
decoded-response typing (`01a1056f-0083`).

---

## 6. BEND-PERSISTENCE-ADVERSARIAL-20261003.txt (astra_adversarial_architecture)

**(1) Central claim.** Five join obligations for the Activity abstraction:
1. Stored bytes are neither reachability nor an affine resource. Root an activity in an
   admitted initial state, carry transition evidence, and consume the predecessor in a
   native CAS.
2. Use one request-indexed continuation envelope, never two loose codecs.
3. Revocation cannot erase an already-dispatched obligation.
4. Private metacontrol is an observable protocol: sizes, timing, refusals and repair
   traffic.
5. Whole-state exactness is the right default.

Council attempts (Opus, Grok) timed out, so there is **no council opinion**.

**(2) Status.** The obligations stand. The code they targeted is obsolete.
- Under Core4, #5 is **BUILT** (`state_roundTrip`, READ).
- #1 is acknowledged as the kernel's job. EVENTS says "fencing duplicate resumes is the
  kernel's job". `Kernel/Contracts/Identities.retry_cannot_reconsume_row` exists and is
  axiom-pinned, but only in ResearchWip (READ). No kernel record consumes it yet.
- #2 is partial: `stack_activity_signature` gives per-program, not per-request,
  response typing (INFERRED).
- #3 and #4: **DESIGN-ONLY**.

**(3) Still right.** All five, restated in Core4 terms:
- the yielded State and its Plan cell replace "continuation closure plus environment";
- the per-request binding is the kernel's `InvocationId`/`AttemptId`/generation chain
  (READ EVENTS §Events).

**(4) Untasked frontiers.**
- Forged-checkpoint refusal tests (forged flag, terminal substitution, two simultaneous
  resumes, old-worker publish after handoff): no task.
- Revocation preserves dispatched obligations: no task.
- A metacontrol leakage contract: no task.

---

## 7. BEND-GENERAL-ZKVM-PATH-20261003.txt (Codex, bend_semantics_audit)

**(1) Central claim.** One live semantics should serve native, oblivious, trace-proof and
specialized backends, anchored at BendTT Eval/Walk. The lane staged:
- `BendExecutionTrace`, `BendTraceConstraints` (an AND/XOR DAG to Air) and `BendTraceIR2`
  (to Bread IR2);
- an entropy crate;
- an offline IR2 prove/verify harness.

**Findings.**
- Bread `circuit/src/stark_zk.rs` uses `SmallRng`, and cloning the hiding MMCS/FRI
  duplicates its state.
- A **one-row main trace is fully disclosed** by its extension-field opening
  (demonstrated on persvati, job05).
- Fixed height 256 is experimental only.
- Challenger v3/v4 conditioning, masking interpolation, arbitrary-witness unroll forcing
  and a Keccak-f graph followed.
- Its all-program closure requirements A–G: canonical decoder; bounded canonical arena;
  every tick stutters or makes progress; forced-wire relation; the receiver binds the
  statement; public tariff, never measured; prove/verify with tamper refusal.

**(2) Status: OBSOLETED as an Objective path.** The repo copy carries a 2026-10-04 header
saying so (READ). Its modules are on main and BendTT-anchored (READ):
`Theory/BendExecutionTrace`, `Compiler/BendTraceConstraints`, `BendTraceIR2`,
`Theory/BendMaskingInterpolation`, `Assurance/BendUnrolledSource`,
`native/bend-ir2-proof` (with `tests/short_trace_disclosure.rs`), `native/bend-proof-entropy`.

The **Core4** zk tranche is in the cut warm base only (READ):
`Compiler/ObjectiveThunkNetwork`, `ObjectiveDemand*Network`, `ObjectiveDemandPhysical`,
`Assurance/ObjectiveBendZkClaims`, `ObjectiveBendCommittedSource`. Main's
OBJECTIVE-BEND.md cites `Assurance/ObjectiveBendCommittedSource`, which is not on main.

The **zk-truth lane** (`docs/ZK-TRUTH.md`, authored and uncompiled, READ) answers the
key question: "does a verified proof imply the source result? **No, not end to end,
for any program.**"
- Link 1 (PCS verify implies the relation holds) is unproved.
- Link 5 (the verifier's result wires are read by the same decoder) is unstated.
- `PackedRefinement` is trivially inhabited by administrative stutter. The corrected
  form is `PackedCodec`.
- Refuter `codec_relation_not_refinement`: the tranche relation never binds code rows,
  so `.nat 9` bits decode as `.nat 7`.
- Step-count leak: secrets meaning 0 take 5 vs 8 ticks, and the emitter hard-codes
  `physicalTicks 9`. Fix: ticks come from a signed public envelope; refuse on excess; no
  refund.
- Padding to height 256 by repetition hides nothing.

**(3) Still right.** Requirements A–G, word for word, except that the anchor becomes
`stepRaw`. Also: the receiver binds the expected descriptor and public vector
independently; a 256-bit digest is never folded into one BabyBear element; the entropy
and short-trace findings are facts about Bread and IR2. "Proof hides from the verifier"
is different from "the prover never saw the inputs". All of this is still right.

**Must be restated.**
- The trace product refines `stepRaw`.
- The oblivious ROM lacks sums and run-time `fix`/`mix` code (READ BACKENDS); task
  `01a10564-84c3` exists for one shared code table.
- Mini has no admitted proof system, so every zk item is research until a proof carrier
  has an admission bar (task `01a0f6ae`).

**(4) Untasked frontiers.**
- Land and compile the zk-truth lane: no task. Its STATUS lists deferrals "for cv task"
  that I could not find in cv.
- Link 5 decoder binding; universal `acceptedStep` over the Builder DAG; tariff from a
  signed envelope (handed to W1.1, no cv task); transcript-ZK composition (quotient/FRI):
  no tasks.
- `SmallRng` repair in Bread `stark_zk.rs`: no task (grep smallrng/entropy: 0).

---

## 8. BEND-DATA-REPRESENTATION-20261003.txt (Codex, bend_data_representation)

**(1) Central claim.** Exact codecs for upstream-Bend Bool, Nat, List Nat, bytes and Word
as safe.ts emits them into BendTT. A codec refuses and never wraps, truncates or
saturates. Source Nat, native word, field element and BFV ring are different domains,
and each crossing names its bound. A unary source encoding can be a proof witness
without being materialized. Ten modules qualified, and the first authored-data artifact
reached a real BFV consumer (`51efc99c…`).

**(2) Status: OBSOLETED** (BendTT Book shapes). The repo copy was rewritten on
2026-10-04 and says so (READ). `Compiler/BendSource*` remain on main (READ).

The Core4 data story (READ):
- `Theory/ObjectiveBendDemandData` extracts deep first-order Data with
  `materialize_sound`.
- Sums landed (`inject`/`case`/`ifBool`/`labelEqual`). The repo doc's "no sums" is stale.
- Plans and responses "must be non-recursive data" (EVENTS), so **Core4 has no lists,
  bytes or words**.
- `Compiler/ObjectiveBendDataWire` (44 lines) decodes the preview response wire.

**(3) Still right.** The four principles in the repo copy: refuse, never wrap; name every
domain crossing; witness without materializing; source charge ≠ physical work.

**Must be restated.** The data universe is nat/bool/label/record/variant. Bytes become a
checked list of bounded Nat once recursive data exists.

**(4) Frontiers.**
- Untasked: recursive data, lists and bytes in Core4 (only partly in `01a1056f-00a4`);
  a bounded-integer profile; `-`/`<`.
- Tasked: let and preview of sums (`01a105a2`); DeepEvaluates determinism
  (`01a104fd-9092`).

---

## 9. BEND-SEMANTICS-AUDIT-20261003.txt (Codex, bend_semantics_audit)

**(1) Central claim.** Use pinned BendTT (`947db722`) Eval/Walk as the reference.

It gives an exact claim inventory: `book_check`, `confluent`, `sr`, `progress`, `halts`,
`empty`, `consistent`, with premises. Quantities: Q2 is unrestricted Data, not "two".
Rwt evidence is live. There are three evaluation layers: source WNF, the fuelled checker,
and live CBV Eval.

It lists source-compiler gaps: comp.ts erases Rwt and dead lets; Nat48 fail-stop vs
unbounded; F32 NaN canonicalization; FOLD_FUEL; FFI by continuation. It proposes one
closure machine refined to every backend (A–G) and a controlled build plan.

**(2) Status: OBSOLETED by Core4.** Objective has its own lazy semantics, and BendTT
theorems "say nothing about the demand machine" (READ OBJECTIVE-BEND.md). The repo
records that "the separate BendTT semantics audit was deleted on 2026-10-04" (READ, repo
zkvm header). `Theory/BendTTSource` stays as a vendor reference (READ). BACKENDS judges
bend2 `comp.ts` "transfers nothing" (READ).

**(3) Still right.** The method:
- one machine, refined to every backend (Core4 now has A, closed and scoped; B,
  adequacy and completeness; C partly, with `Limits` and ticks; G partly, the C
  differential);
- explicit absorbing outcomes, with exhaustion never a result;
- charge is never native instruction counts;
- FFI is never ambient;
- primitives are registered with their relation and domain;
- artifact identity binds the toolchain;
- name facts as theorems, not `#guard`.

**Must be restated.** All BendTT specifics: Rwt, Q2 Data-only reuse, structural
recursion, Type:Type. Core4 turns may diverge, ending in a blackhole or tick exhaustion.

**(4) Untasked.** A Core4 primitive/FFI registry; registering Core4 as a
`Compiler/Evaluator` entry (INFERRED: no task). The C ≡ `stepRaw` refinement theorem is
tasked (`01a10564-8480`).

---

## 10. FHE-BEND-ARCHITECTURE-20261003.txt (Codex/Astra, fhe_bend_architecture)

**(1) Central claim.** Homomorphic execution is one realization of a checked method, with
sealed persistent state and explicit release in the same world. First target: a
**public fixed program with secret finite inputs**, compiled once to a constructive
graph and run on real BFV. A secretless evaluator plus an independent ciphertext-replay
checker form the first integrity leg.

**Inventory of what Bread already has.**
- BFV Boolean `logic_schedule`, with bitness not verified.
- TFHE comparison/selection.
- Threshold BFV committee custody with verified decrypt-share certificates. Open: the
  malicious-DKG shortness seam; relinearization is honest n-of-n only.
- Same-opening proofs, uneven.
- Noise models with named holes.
- `SmallRng`.

**Three execution classes.** A: public program, secret inputs. B: public template, secret
finite choices. C: secret program on a padded universal machine.

**Contract objects.** FhePlan, KeyEpoch, InputAdmission and ReleaseAuthorization. A
durable state machine runs reserve, evaluate, check, prepare, commit, authorize release,
release. Delivery is in slices 1–4.

**(2) Status: PARTLY.**
- Slices 1–2 ran on BendTT artifacts. `native/fhe-bend` is on main (`evaluate`/`check`,
  `owner.rs`, `natural.rs`, `governed.rs`); its README header says it consumes BendTT
  artifacts only (READ).
- "FHE over Objective" (r34 weighted, r35 ReturnRelease, r36 consent) was in the deleted
  `codex-homomorphic-bend` directory (READ ssh: GONE). Tasks `01a105af` (rebuild) and
  `01a10556-49ad` (mine) exist.
- BFV noise theory is ported as `Theory/Bfv{Params,Noise,NoWrap,Fold,Mul,Ring,Smudging}`
  and `BfvLifetime`, ResearchWip only (READ). Findings (READ ledger): the depth-2 ceiling
  is relin noise ≤ 2^52.39, while worst-case key-switch noise may be about 2^54; no
  smudge radius gives 48-bit-hiding threshold release on this chain.
- Threshold custody, TFHE, the DKG fix and circuit privacy: **DESIGN-ONLY** in Mini.

**(3) Still right.**
- Classes A/B/C;
- the four contract objects;
- ciphertext replay as an integrity leg only;
- an explicit honest-owner input profile;
- no decryption oracles or "try decrypt";
- the metadata contract;
- reserve-before-secret-release, and one-time rows burned on uncertainty;
- no decrypt-reencrypt bridge;
- CKKS as a separate approximate profile.

**Must be restated.** Class A needs a Core4 specializer (note 3). Source Nat is unbounded,
so a declared bound comes first.

**(4) Frontiers.**
- Untasked: TFHE as second exact backend; threshold custody and DKG shortness; recipient
  release for Objective results; encrypted-input validity (same-opening/range);
  circuit privacy and sanitization; a CKKS profile.
- Tasked: worst-case noise `01a10501-82d1`; Bfv imports `01a10501-825a`.

---

## 11. FHE-BEND-NATIVE-BOUNDARY-20261003.txt (Codex, homomorphic_bend_construction)

**(1) Central claim.** Native boundary rules for the first physical consumer:
- use the owned `fhe0.1.1` fork directly, not Bread's GPU/PQ tower;
- canonical ciphertext parsing re-runs `Ciphertext::new` validation;
- depth-0 ct×plain arithmetic, with signed −1 by negation;
- public replay compares exact bytes and every binding;
- honest-owner input is an explicit premise;
- a governed content storage receipt is **not** a computation or release receipt;
- carry an immutable checked candidate from check through commit to release.

**(2) Status: PARTLY.** The rules are implemented in `native/fhe-bend` for BendTT
artifacts (READ README). Its run-mux-01 evidence is gone (§0.6). The governed native join
for Objective, meaning opaque candidate storage under current authority plus a release
event, is **not built** (INFERRED: no Objective module).

**(3) Still right.** Every rule. The producer must become a Core4 program.

**(4) Untasked.** Governed opaque-result storage and release for Objective FHE outputs.

---

## 12. PREOSCRIPT-OBJECTIVE-BEND-RELATION-20261003.txt (Astra, archaeology)

**(1) Central claim.** Bring Preoscript's strongest semantics into Objective Bend
selectively, and keep lean-uwueave an independent library. Three ports:
1. future-indexed result/evidence contracts on a source-authored **view**;
2. a proved query-analysis refinement from a Bool/pair/option subset of `Preo.Expr` into
   a Bend body;
3. coordination contracts on **composed** partial specs, with a strategy-sharing
   counterexample.

False friends to keep apart:
- Preoscript `Scheduling.Plan` is not Mini's `Plan`.
- A CRDT join is not ordered extension.
- Pure termination is not future stability.
- Semantic disclosure is not obliviousness.

**(2) Status: PARTLY.**
- `Kernel/Contracts/Futures.lean` on main re-states `Preo.Future` (WorldModel,
  CheckedCertificate, `futures_not_interchangeable`) and `summaryFold_iff_joinHom` /
  `no_count_merge_without_provenance` over Mini accepted history. It is in ResearchWip
  only and attached to no Objective view (READ).
- `Compiler/UwueavePreoProjectionV2` plus generated Rust is on branch
  `origin/codex/uwueave-projection-v2`, not main (READ).
- OBJECTIVE-BEND.md §"Relation to Preoscript" adopts the stance: "a contract language
  Core4 specifications should carry and check, not a projection target to emit", and
  "the obligation profile of a `mix` is not simply a sum" (READ).
- Objective laws (`ObjectiveBendLaw{Interfaces,Checking}`) are in a codex lane under
  MINE task `01a10556-496e`. `requires`/laws checking is task `01a10500-6f6f`.

**(3) Still right.** The judgment and the false friends.

**Must be restated.**
- "A closed pure invocation terminates under BendTT" becomes: a Core4 turn may diverge,
  and a resident is a guarded fixed point across turns.
- "WorldSurface" becomes `docs/OBJECTIVE-BEND-SURFACE.md`.

**(4) Untasked.** All three ports. Also the fate of the uwueave-projection-v2 branch,
which contradicts "not a projection target". Grep for preoscript/uwueave: 0 open tasks.

---

## 13. PREOSCRIPT-OBJECTIVE-BEND-COVERAGE-20261003.txt

**(1) Central claim.** A ledger of what the relation note actually read: the cv dialogue
locators (claude `36b51055` #0, #14; `0d3efcb7` #1051–1100, #1122; codex `019ff1aa` #3),
the lean-uwueave modules, and the Bread files. It records no tests or builds.

**(2) Status.** N/A. It is provenance. The "local older Mini" UwueavePreoProjectionV2 it
read is now on branch `origin/codex/uwueave-projection-v2` (READ).

**(3)** Keep it as the citation trail for note 12.

**(4)** None.

---

## SYNTHESIS (≤1200 words)

### Pillars: current truth and next moves

**P1 — The language (Core4 and its front end).** Core4 is the only kernel. On main it
has lazy fix/mix, specifications, prototypes, sums and activities, plus a certifying
checker with preservation, adequacy, completeness (`coreRepresentation`) and data
soundness. All of it sits outside every default build target. The TS
parser/elaborator is still the implementation; the Lean elaborator only
translation-validates it. Gen-1 is still in main's tree, and OBJECTIVE-BEND.md's
open list is behind the code.

Next moves:
1. Land the rebased cut: Gen-1 deleted, an `ObjectiveProofs` gate.
2. Correct OBJECTIVE-BEND.md's status sections.
3. Make the Lean elaborator the implementation, re-emit pins, and gate the front-end
   checks (`01a10500-6e65/6eef/6f2f`).
4. Add `requires`/law checking at `compose`/`fix` (`6f6f`) and audit the shareability
   hole (`01a10505-46cf`).
5. Add recursive data (lists, bytes), `-`/`<`, and `let`.

**P2 — Engines and cost.** `runBounded` is the specification. The C machine matches it
on 340/340 differential cases (900–2900× faster) but has no theorem. The `@[csimp]` fast
Lean machine exists, uncommitted, in the fastmachine lane. No tariff exists on the
Objective path, and `proofWork` is caller-chosen.

Next moves:
1. Land the fast machine. This may settle the C-executor fork `01a10564-84ef`.
2. Gate the C differential, then prove C ≡ `stepRaw` (`8480`).
3. Adopt one charge law: ticks plus `Limits`, priced from a signed versioned envelope,
   refusing on excess.
4. Use one code table and one State format for C and the oblivious network (`84c3`).

**P3 — Native admission (world).** A member invocation reaching an Accepted receipt has
been assembled in lanes. It has not happened on main, and no cv task names it. There is
no Core4 private-return slot, semanticId/planId split, lowerer pin or Evaluator registry
entry.

Next moves:
1. File and land the first native Objective Accepted, with its ten refusals.
2. Bind the lowerer pin and parser transcript in the artifact, and route guards.
3. Add semanticId/artifactId for Objective packages.
4. Add a private-return slot plus a release transition.

**P4 — Persistence and residents.** Language-side activities are complete: perform/yield,
quiescent safe points, typed resume, exact checkpoint, and the C machine resuming
Lean-saved yields. Nothing kernel-side exists.

Next moves:
1. Kernel delivery: a record with a generation CAS, checkpoint storage, typed response
   (`01a1056f-0066`).
2. The adversarial falsifiers as tests: forged checkpoint, double resume, old worker,
   revocation with an in-flight dispatch.
3. A guardedness check and heap collection at yield (`0083`, `00a4`).
4. Metacontrol capabilities and their leakage contract.

**P5 — Graded/priced execution contracts.** Entirely design. The foundations are on main
(PrivacyProfile, Disclosure, TypedAuthorization, ResourceCost), plus the BendTT-side
semanticId codec.

Next moves, after P2.3 and P3.3:
1. A small `ExecutionContract`/`ExecutionPlan` over one real `.obend` consumer, with
   Accept/Reject/Unknown.
2. The seven prohibited fallbacks and five falsifiers as gate rows.
3. A per-observer leakage card for Objective execution.

**P6 — zk and oblivious.** No end-to-end implication holds for any program. Link 1 (PCS
verification ⇒ the relation) and link 5 (the decoder is the verifier's codec) are
missing. `PackedRefinement` was vacuous. The tranche relation fails to bind code rows.
Measured ticks leak. A one-row trace is disclosed. The Core4 tranche is in the cut;
zk-truth is uncompiled in a lane.

Next moves:
1. Compile and land zk-truth, and file its deferrals.
2. Bind code/environment/field regions in the universal relation, using `PackedCodec`.
3. Put ticks from the envelope into the emitter.
4. Write the ZK.md admission bar (`01a0f6ae`).
5. Address link 1 and transcript ZK, including the `SmallRng` repair in Bread.

**P7 — FHE, MPC and private compute.** Real BFV runs happened, but only on BendTT
artifacts, and their logs are gone. FHE over Objective was lost in the wipe. The noise
theory is ported (ResearchWip); depth 2 is in doubt and threshold release at 48-bit
hiding is impossible on this chain. MPC private inputs landed separately (ledger W2.G).

Next moves:
1. Rebuild FHE over Objective on a Core4 producer (`01a105af`).
2. Check worst-case key-switch noise (`01a10501-82d1`).
3. Governed opaque-result storage plus release.
4. Encrypted-input validity.
5. TFHE and threshold custody, as their own qualifications.

**P8 — Logic compilation (fixed-program circuits).** All checked compilers on main bind
BendTT Books. The generic Air/Emit stack is reusable. ObjectiveNatural (add-only, against
the source relation) sits in a codex lane.

Next moves:
1. Decide the refinement hub (§Contradictions, item 1).
2. Mine ObjectiveNatural onto main.
3. A Core4 specializer: partial evaluation of public fix/mix, both-arm mux for
   `case`/`ifBool`.
4. Subtraction, comparison and multiplication with no-wrap proofs.

**P9 — Contracts and Preoscript.** `Kernel/Contracts/Futures` restates Preo futures over
accepted history (ResearchWip). Laws and `requires` are unchecked strings.

Next moves:
1. Laws as checked evidence (after P1.4).
2. Port 1, a future-indexed certificate on one authored view.
3. A theorem for a `mix`'s obligation profile.
4. Decide the uwueave branch.

### Contradictions someone must decide

1. **The refinement hub.** The C machine, the oblivious network and zk all refine
   `stepRaw`. ObjectiveNatural refines the *source* relation. Pick `stepRaw` as the one
   hub, or prove the link between the two relations once.
2. **The admission executor.** The choices are Lean `runBounded`, the C machine behind a
   differential gate (`84ef`), or the `@[csimp]` fast Lean machine. They are now
   competing answers to the same speed problem.
3. **Charge.** Note 4 puts gas on a shared IR. BACKENDS says ticks plus `Limits` price
   every backend directly. zk-truth says ticks come from a signed envelope, never
   measured, with no refund. Native admission has a caller-chosen `proofWork`. Decide
   whether clear execution may charge measured ticks while private profiles must charge
   the envelope.
4. **Plan ABI.** Note 4 wants a sum of typed actions with private-return slots and
   messages. Core4 activities allow one non-recursive first-order action per yield, and
   the `executeWith` route requires Plan effects to equal command effects exactly. Decide
   multi-action, recursive data, return slots, and which route is canonical.
5. **In-turn termination.** Notes 1, 4 and 12 assume pure turns terminate (BendTT). Core4
   turns may diverge and are stopped only by ticks. Decide whether a guardedness check is
   required for residents or the tick budget is the contract.
6. **What happens to BendTT.** About 258 BendTT modules, `native/fhe-bend` and
   `bend-ir2-proof` survive the cut as files. CLAUDE.md doctrine says delete the old
   shape. The alternative is to port the reusable parts first (Air/Emit stay; the
   ObjectiveNatural and zk tranches are their successors).
7. **Preoscript.** "Carry and check, not a projection target" (OBJECTIVE-BEND.md)
   conflicts with the open `uwueave-projection-v2` branch.
8. **Docs vs code.** Docs on main claim Gen-1 is deleted and that completeness and data
   soundness are open. The code says the opposite on both.
