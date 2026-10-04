# SCHOLAR-BREAD — what Bread offered on programs, cells, calls, laws, concurrency and evolution

Read-only scholar report, 2026-10-04, written against `PROGRAM-MODEL-BRIEF-20261004.md` and ROOT's
raised scope (go deep on pipelining, partial turns, eventual refs, vats, turns-as-transactions,
cross-cell messaging, joint turns, scheduling/fairness, naming, persistence, reflection; treat each as
an OS subsystem). Nothing was built, run, edited or committed. This is the only file written.

**Roots.** `B/` = `/Users/ember/dev/breadstuffs/` (Bread / dregg; Lean under `B/metatheory/Dregg2/`).
`MEM/` = `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/`. `F/` = `/Users/ember/dev/fareoo/`.
`C/` = `/Users/ember/dev/claudesplosion/`.

**Provenance tags.** **READ** — I read the code/doc at the cited place. **LANE** — one of seven
read-only sub-readers I dispatched read it at the cited `file:line` and I did not re-read it; where I
re-checked a lane claim myself it is marked **READ**. **INFERRED** — my conclusion, not checked at a line.
**Status tags** (what Bread actually had): **RUN** = on the node's executor/API path;
**TESTED** = built with tests, no live caller; **LEAN** = proved about a Lean model with no Rust
consumer; **DOC** = design text only.

**A correction to the brief's own list (READ).** "the evaluator registry, Nock programs" are not Bread.
`grep -ri nock B/metatheory/Dregg2` hits only the word "knocks" in three FRI files; no Bread symbol is
named evaluator registry. Both are Mini's (the 10-01 addendum in
`MEM/project-no-proof-system-in-mini-admission.md`: "Nock is evaluator #1 in a REGISTRY"). Bread's
nearest things are `CellProgram::Circuit{circuit_hash}`, `StateConstraint::Custom{ir_hash}` and the
custom-effect registry keyed by vk-hash (`B/cell/src/custom_effect.rs:1-40`, LANE; its v1 verifier "accepts
non-empty proof bytes").

---

## 0. The verdict

**Bread had a definite take, and it is the opposite of the proposed Mini model on the one question that
matters most: where the program runs.** In Bread a cell holds no code. A cell is a fixed-shape record
(16 field registers, a signed balance, a committed sorted-Poseidon2 heap; `B/cell/src/state.rs:178-328`,
LANE) plus a `CellProgram` that is *data* — `None | Predicate(Vec<StateConstraint>) |
Cases(Vec<TransitionCase>) | Circuit{circuit_hash}` (`B/cell/src/program/types.rs:6-102`, LANE). A call
is a signed `Action { target, method, args, authorization, preconditions, effects: Vec<Effect>, … }`
whose **effects the caller computed off-ledger** (`B/turn/src/action.rs:73-123`, READ). The `method`
field is a BLAKE3 tag that only selects which `MethodIs`-guarded constraint cases apply
(`B/cell/src/program/eval.rs:64-136`, LANE); nothing on the executor path interprets `args`. The executor
applies the declared effects and then judges every touched cell's program on (before, after)
(`B/turn/src/executor/execute_tree.rs:590-700`, LANE). This is the Mina zkApp shape — the forest of
account updates, `balance_change` summing to zero, `use_full_commitment` — and the code says so
(`B/turn/src/forest.rs`, `B/turn/src/composer.rs` headers, READ).

So Bread's slogan was "the client proposes, the law disposes", and Mini's proposal is "**code proposes**
(re-executed by admission from a pinned package), law disposes". Mini's `Plan` is Bread's
`Action.effects`, except that Mini computes it in the kernel from code the world can see. Everything
Bread could not do follows from that one choice: no method that computes, no return value, no in-turn
call from one cell's logic into another's, no continuation that carries a value, and a "program" that is
really a law. Mini's own `DEOS.md` once said "Mini's program is a law" (`C/planning/DEOS.md:447`, READ) —
that was Bread's model. The proposed model leaves it, and Bread is evidence that leaving it is needed:
ember's 06-11 critique "our caveats and predicates are lamesauce … not feasibly possible to build
useful/real/nice apps" (`MEM/project-lamesauce-predicate-critique.md`, READ) is the user-level symptom of
having only laws.

**Where Bread is genuinely interesting** is at the edges of that model, and most of the interest is in
ideas that transfer *better* to Mini than they worked in Bread:

1. **"Determination is eager, witness is lazy"** — the governing rule for every promise/hole: what a
   pending contribution will write, whose authority it spends and its exact value delta are fixed when the
   hole is made; only the value or proof arrives later. A hole in a conservation or authority position is
   made inexpressible rather than checked (`B/docs/DESIGN-partial-turn-promises.md:38-43, §6`, READ).
2. **A promise-hole is a nullifier; to react is to spend it** — one-shot resumption enforced by the same
   fresh-insert mechanism as a note spend (`B/turn/src/reactive.rs:31`, quoted in the design doc §2.2, READ), RUN.
3. **Three-layer coordination** — causal hash-chaining (free), multi-party 2PC whose commit/abort verdict
   is a Lean-exported function the node calls (expensive), and Stingray bounded counters for concurrent
   spending without coordination (`B/coord/src/lib.rs:1-60`, READ; `B/node/src/coord_gate.rs` header, READ), RUN.
4. **A coordination grade per guard** — I-confluence / CALM classification deciding which writes can merge
   without ordering (`B/metatheory/Dregg2/Confluence.lean:33-57`, `Authority/ConfluenceClassifier.lean:69-229`,
   LANE; per-kind and per-query in Rust: `B/dregg-merge/src/gate.rs:84`, `B/dregg-query/src/classify.rs:38`, LANE).
5. **Upgrade as a proof-carrying gate** — the svenvs envelope (`Admissible step safe oldp newp :=
   SoundPolicy step safe newp ∧ oldp ⊆ newp`; `self_improvement_is_safe` for any stream of proposals)
   and Polis's non-regressive amendments over frozen floors (`B/metatheory/Dregg2/Upgrade.lean:212-273`,
   READ; `B/metatheory/Polis/Polis.lean:253-306`, LANE). LEAN only.
6. **Effect handlers that carry their own obligations** — an `EffectHandler` structure whose literal is
   ill-typed until `auth_gated`/`admission_gated`/`conserves` are proved, with global conservation proved
   once over the registry (`B/metatheory/Dregg2/Exec/Handler.lean` header, `HandlerExecutor.lean` header, READ).
7. **Regime-typed display** — a `Publication` cannot render a badge stronger than the regime that
   settled it (`honest : renderedAs.strength ≤ settledIn.strength`;
   `B/metatheory/Metatheory/ResearchRegime.lean:234-298`, LANE). LEAN only.
8. **Per-viewer affordance projection** — an affordance is live iff the viewer's caps cover it and (in
   `GatedAffordance`) the live state admits it (`B/docs/deos/DEOS.md:27-38`, `HIG.md:23-40`, LANE).
9. **Reversibility in three tiers** — every effect is Clean-invertible, Contextual (needs the pre-image),
   or Committed (no inverse, on purpose: Destroy, Burn, NoteSpend, nonce ratchet, revoke)
   (`B/turn/src/reversible.rs` header, READ), TESTED.
10. **The single-machine principle** — distributed bounds are parametrized by deployment topology and
    collapse to the strong single-node properties at n=1 (`MEM/project-dregg4-vision.md`, READ;
    `B/metatheory/Dregg2/Distributed/Fibration.lean:222-240`, `Revocation.lean:301`, LANE).

**Where Bread is weak, and how to read its record.** Most of its rich ideas are LEAN-about-a-model or
TESTED-with-no-caller. The running node executes turns one at a time under one lock with one global
order (`B/node/src/execution_cursor.rs`, `B/node/src/state.rs:196`, LANE); each agent's turns are a
strict chain (`previous_receipt_hash` must equal the stored head, `B/turn/src/executor/execute.rs:587-598`,
READ); the CapTP pipelining drain has no caller (`B/wire/src/server.rs:1158,1168`, LANE); the solver
competition and challenge windows never run in the node (`B/node/src/api.rs:2670-2678`, LANE); program
upgrade in Rust is a bare swap with no migration or governance (`apply_set_program`,
`B/turn/src/executor/apply.rs:1416-1445`, READ); and **no suspended computation was ever persisted** —
pending work is a whole `Turn` re-executed from its pre-state (`B/turn/src/continuation_resume.rs:13-17`,
READ). It also had **five async mechanisms that never met**: the batch pipeline, the pending registry,
the reactive Promise/React effects, CapTP pipelining, and intents. That fragmentation is itself the
biggest lesson for Mini: one await primitive.

**Ember's "or maybe it didn't":** on *programs and calls*, Bread mostly didn't — its programs were laws and
its calls were client-assembled forests. On *promises, coordination, coordination-cost of laws, and
upgrade discipline*, it did, and Mini — which actually has continuations, re-execution and a
certifying checker — can build several of them properly where Bread could only model them.

---

## 1. Bread's model on each fork

### 1.1 Programs and cells (the ground every fork stands on)

| thing | Bread's shape | status | where |
|---|---|---|---|
| cell | `Cell { id, public_key, state, permissions, verification_key, delegate, delegation, token_id, capabilities, program, mode: Hosted\|Sovereign, lifecycle, pq_identity }` — no code, no interface field | RUN | `B/cell/src/cell.rs:338-394` (LANE) |
| state | `fields: [FieldElement;16]`, `nonce`, `balance: i64`, `fields_map` overflow, `system_roots: [FE;8]`, heap = `heap_root` + `heap_map: BTreeMap<(u32,u32),FE>` | RUN | `B/cell/src/state.rs:57,178-328` (LANE) |
| program | data: `Cases(Vec<TransitionCase{guard: Always\|MethodIs\|EffectKindIs\|SlotChanged\|AnyOf\|AllOf, constraints}>)`; all matching cases ANDed; default-deny when no case matches, and also when a method-dispatching program has no matching method case | RUN | `B/cell/src/program/types.rs:6-102`, `eval.rs:64-136` (LANE) |
| law atoms | `StateConstraint`: 69 hand-named variants (`Monotonic`, `WriteOnce`, `AffineLe`, `RateLimit`, `SenderAuthorized`, `Witnessed`, `ObservedFieldEquals`, `SettleEscrow`, `Custom{ir_hash}` …) | RUN | `B/cell/src/program/types.rs:1023-2075` (LANE) |
| call | `Action { target, method: Symbol, args, authorization, preconditions, effects: Vec<Effect>, may_delegate, commitment_mode: Full\|Partial, balance_change, witness_blobs }` | RUN | `B/turn/src/action.rs:73-123` (READ) |
| turn | `Turn { agent, nonce, call_forest, fee, valid_until, previous_receipt_hash, depends_on, conservation_proof, sovereign_witnesses, … }` run as a journalled transaction | RUN | `B/turn/src/turn.rs:468-505` (READ); `B/turn/src/journal.rs` (LANE) |
| kinds | `FactoryDescriptor` (content-addressed constructor; `state_constraints` become the child's lifetime program); Hatchery `MintedKind = FactoryDescriptor + Invariant + HpresProof` | RUN (factory), TESTED (Hatchery) | `B/cell/src/factory.rs:353-391` (LANE); `B/docs/deos/HATCHERY-ABSTRACTION-MINT.md`, `B/metatheory/Dregg2/Deos/Hatchery.lean` (READ) |
| "methods" | `InterfaceDescriptor { methods: MethodSig{symbol, args_schema, auth_required, semantics: Replayable\|Serviced} }`, `invoke()` desugars a method to caller-supplied ordinary effects; "no `Effect::Invoke`" | TESTED | `B/cell/src/interface.rs:135-244`, `B/app-framework/src/invoke.rs:1-176` (LANE); `MEM/project-cells-as-service-boolean-matching.md` (READ) |
| general compute | outside cells: the client/agent; or as a proof against a registered VK (`Effect::Custom{program_vk_hash}`); "cells are law, agents are will, receipts are the nervous system" | RUN (hosted path rejects unproven Custom) | `B/turn/src/executor/apply.rs:528-542` (LANE); `MEM/project-lamesauce-predicate-critique.md` (READ) |
| author language | Rust: hand-built `CellProgram::Cases` data + action-builder functions; `dregg-dsl` proc-macros for constraint predicates; `dreggscript` is "Not yet a language; not yet code" | RUN / DOC | `B/dregg-dsl/src/lib.rs`, `B/dreggscript/README.md:1-30` (LANE) |

Lean mirrors: `Exec/Program.lean` (`RecordProgram`, the name-keyed transcription of the constraint
catalog; READ header) and `Exec/CellProgram.lean`, where a program is `admits : KernelState → Turn → Bool`
and `denote p k t := if p.admits k t then exec k t else none`, so "a program can only ever *tighten*
`exec`, never bypass it" (READ header). The Lean and Rust dispatch rules differ: Lean has no
`EffectKindIs` and lacks Rust's "dispatching program denies an unmatched method even when `Always`
matches" (`Program.lean:716-719` vs `eval.rs:118-127`, LANE).

### 1.2 Fork 1 — calls across cells

Bread had **no dynamic call between cells**. What it had, from synchronous to asynchronous:

1. **The call forest** (RUN). A turn is a forest of `CallTree{action, children}`, Mina-style, executed
   depth-first in one rollback scope (`B/turn/src/forest.rs`, READ header). A child on a *different*
   cell is refused with `DelegationDenied` unless the parent's `may_delegate` is `SnapshotRefresh`;
   `ParentsOwn`/`Inherit` are typed but return `DelegationModeUnimplemented`
   (`B/turn/src/executor/execute_tree.rs:1415-1455`, READ). So "A calls B" means the submitter wrote B's
   action as a child; no return value flows back.
2. **Exercise via capability** (RUN). `Effect::ExerciseViaCapability { cap_slot, inner_effects }` applies
   pre-written effects to whatever cell the held capability names (`B/turn/src/action.rs:1262`, LANE). It
   is cap-mediated authority, not invocation.
3. **Cross-cell reads as verified observations** (RUN, with a defect). `StateConstraint::ObservedFieldEquals`
   is documented as "a verified observation of FINALIZED state, NOT a live read"; live cross-cell reads
   were deliberately kept out of the law language (`B/cell/src/program/types.rs:1544-1581`, LANE). In the
   hosted executor, however, the "finalized" root is the peer's *current* ledger commitment
   (`execute_tree.rs:355-371`, READ: "read from the ledger's current committed view"). The Lean side has the
   right distinction: `importValid_stable_under_source_advance` versus
   `liveRead_changes_under_source_advance` (`B/metatheory/Dregg2/Authority/CrossCellImport.lean:124,168`, LANE).
   `BoundDelta` couples two cells' deltas within one action (`Equal`/`EqualAndOpposite`,
   `types.rs:376`, LANE).
4. **Batch pipeline with eventual refs** (TESTED, no node caller). `Pipeline` = turns + dependency edges,
   Kahn-sorted, optionally atomic; `EventualRef{source_turn, output_slot, federation_id}`;
   `Target::Concrete|Eventual`. The module says of itself: "This is **not** async promise pipelining in the
   E-language sense. All execution is synchronous and local. For true E-style eventual-send, use the
   intent system." (`B/turn/src/eventual.rs:1-15`, READ). `TurnOutput` values are re-derived from declared
   effects into a process-local table and are not receipt-bound (`eventual.rs:113-124`, READ).
   The Lean model `ConditionalBatch { nodes : List (List FullAction), edges }` with `Slots := Nat → Bool`
   proves atomicity, conservation and topological soundness (`B/metatheory/Dregg2/Exec/ConditionalTurn.lean:90-232,
   417-447`, READ) — **but its slots are booleans: no value moves from producer to consumer.** It proves
   ordering, not dataflow.
5. **Promises, notifications, reactions** (RUN). `Effect::Promise{cell, resolution_condition, wake:
   Box<Turn>, timeout_height}`, `Effect::Notify{from, to, wake, …}` (deposited in the recipient's
   registry), `Effect::React{pending_id: Nullifier, condition, resolution_proof, wake}`. A promise is a
   committed effect in `effects_hash`; `apply_promise` gates `cell == actor`; `apply_notify` gates
   `from == actor ∧ wake.agent == to`; `apply_react` checks `wake.hash() == pending_id`, runs
   `resolve_condition`, and spends `pending_id` once into a React-domain nullifier set, journalled
   (`B/docs/DESIGN-partial-turn-promises.md §2.2-§5`, READ, with `apply.rs` anchors there). The fill
   **releases the stored `wake` turn to run later**, not inline (LANE, `apply.rs:~2468`). The continuation
   is a pre-built turn; it cannot compute on the resolved value.
6. **Conditional turns** (RUN, HTTP `/turn/submit-conditional`, `/turn/resolve-conditional`).
   `ConditionalTurn{turn, condition, timeout_height, submitted_at, deposit_amount}`; `ProofCondition =
   HashPreimage | RemoteProof | LocalProof | TurnExecuted`; deposit refunded on resolution, burned on
   timeout; proof-hash nullifier against replay; descriptor chosen by the condition, not the prover
   (`B/turn/src/conditional.rs:55-566` via the design doc's table, READ; `B/node/src/api.rs:2714`, LANE).
7. **Pending registry** (RUN as persisted executor state). `ResolutionCondition = AwaitReceipt{turn_hash,
   federation_id} | AwaitCondition(ProofCondition) | AwaitHeight(u64)`; `BrokenReason` incl.
   `DependencyBroken`, cascading to dependents (`B/turn/src/pending.rs:1-30`, READ header; `:43-165`, via
   the design doc, READ).
8. **CapTP** (TESTED, partly wired). Sturdy refs `dregg://<fed>/<cell>/<swiss>`, `SwissTable` with
   handoff-nonce replay protection, signed three-party `HandoffCertificate`, acyclic-only distributed GC
   with leases as the escape hatch, `PipelineRegistry`, sealed store-and-forward relay (`B/captp/src/
   {uri,sturdy,handoff,gc,pipeline,store_forward}.rs`, LANE). Inbound queueing and handoff validation are
   on the wire server; the pipeline **drain** (`resolve_local_pipeline_promise`, `drain_pipeline_outbox`)
   has no caller outside tests; a live node never builds a `SwissTable` outside `*_e2e.rs` (LANE). The Lean
   `CapTPPipeline` theorems (`drainAll_preserves_caps`, `overAuthorized_send_rejected`,
   `break_freezes_state`) are over `Exec.Kernel.exec`, a kernel model whose `exec` "only rewrites `bal`,
   never `caps`" (READ header) — so no-amplification there is partly by construction of the toy.
9. **Relay + mailbox crank** (TESTED; relay not started by the deployed unit). A seals a turn intent,
   `POST /relay/send/{dest}`; B's `MailboxCrank` drains it, checks the sender against the inbox cell's
   sender set, and runs it as an ordinary turn (`B/node/src/mailbox_crank_e2e.rs:1-15`,
   `B/dregg-sdk-net/src/mailbox.rs`, LANE). The inbox is a **cell program**: a FIFO whose discipline is
   constraints (`monotonic head/tail`, `tail ≤ head`, `immutable capacity/owner`, `SenderAuthorized`)
   (`B/dregg-storage-templates/src/cap_inbox.rs:160-235`, LANE; Lean `Exec/CapInbox.lean`, READ header).
10. **Receipts as the nervous system** (RUN). `GET /api/events/stream` (SSE, cursor resume, at-least-once)
    (`B/node/src/events.rs:1-20`, LANE). Agents subscribe and act; there is no actuator concept in core.
11. **Introductions** (RUN). `Effect::Introduce` emits a `RoutingDirective` the node uses to populate its
    routing table (`B/turn/src/routing.rs`, READ header).
12. **The algebraic-effects spec** (LEAN). `Await.lean`: `Op = await p | call cap | emit eff`, a
    `Computation` tree, `OneShot` continuations with one-shotness as a static linear invariant, the turn as
    the rollback handler (`commit_resumes_once`, `rollback_discards_continuation`), four "faces"
    (zkpromise/discharge/intent/promiseGraph) that `four_faces_unify` shows are views of one `AwaitCore`
    — an extraction identity, as the header admits (`B/metatheory/Dregg2/Await.lean:1-104`, READ).
    **This is the closest Bread came to Mini's Activity, and it never had an executor.**

### 1.3 Fork 2 — laws and contracts

- **The law language as built** is the 69-atom `StateConstraint` catalog under `Cases`/`AnyOf`/`AllOf`,
  decided partly by a Lean "constraint oracle" (`constraint_in_lean_subset`, `B/cell/src/program/eval.rs:300`;
  a subset constraint Lean did not answer is refused, `:257-299`), with eleven witness/crypto classes
  decided in Rust (LANE). RUN.
- **The algebra as modelled**: `Pred` (`B/metatheory/Dregg2/Exec/PredAlgebra.lean:127`) with De Morgan and
  double negation proved, `predStateStepGuarded` as the guarded `put` (`:580-615`) (LANE). The one
  `Guard` seam unifying authorization, preconditions, program constraints and macaroon caveats, with
  `attenuate g c := all [g, c]` and `attenuate_narrows` (`Spec/Guard.lean:90-293`, LANE). The ladder
  affine half-spaces → bounded-degree polynomials → bounded quantifiers (`Authority/RelationalClosure.lean`,
  `ArithmeticClosure.lean:101-214`, `QuantifiedPredicate.lean:68-247`, LANE); only the affine rung exists in
  Rust. LEAN.
- **Satisfiability and explanations: none.** "The only decision procedure that exists is `DecidableEq` …
  no `satisfiable` / `subsumes` / `equiv` / `isVacuous` procedure exists" (`B/docs/DESIGN-predicate-usefulness-targets.md:37-43`,
  LANE). Refusals name the failing constraint (`ProgramError::ConstraintViolated{constraint, description}`,
  `B/cell/src/program/error.rs:7`, LANE). Mini is already ahead here.
- **Capability caveats** (RUN): macaroon HMAC chains, third-party caveats with discharge tickets, a
  discharge gateway service, Rust↔Lean differential tests (`B/macaroon/src/`, `Authority/CaveatChain.lean`,
  `Authority/ThirdPartyDischarge.lean`, LANE). **Datalog/Biscuit** is the token verifier
  ("the SOLE ground-truth verification semantics", `B/token/src/datalog_verify.rs:1-15`; `biscuit-auth 6.0.0`
  default feature) (LANE). RUN.
- **Coordination cost of a law** (LEAN + partial RUN): `IConfluent I := ∀ x y, I x → I y → I (x ⊔ y)`,
  `nonpairwise_escalation` (LANE). The Rust attaches grades per cell *kind* (`classify_merge` → `Free |
  Settle(NonIConfluentKind | NonMonotoneOp)`) and per query (`CoordinationClass{Monotone,
  FinalizedDependent}`), never per constraint (LANE). The claimed `guardGluing_iff_iconfluent` does not
  exist in Lean (LANE; the design doc itself calls it "not yet built", READ §9).
- **Conservation as a law**: `LinearityClass` colouring (Conservative/Monotonic/Terminal/Generative/
  Annihilative/Neutral) and a multi-domain Σ-law are LEAN; the Rust twin was deleted on 07-28 with "zero
  non-test callers" and a wrong colouring of Mint/Burn (`B/turn/src/action.rs:1016-1045`, LANE). The Iris
  camera tier (`ConservesResource := Fpu`, `ConfinesAuthority := Fpu`) is LEAN
  (`B/metatheory/Dregg2/Resource.lean:71-296`, LANE; `MEM/project-dregg2-resource-camera.md`, READ).
- **Behavioural contracts**: multiparty session types — `GlobalType`, `project`, `projection_sound`,
  deadlock-freedom on the non-recursive fragment, "reified as a cell: a protocol-cell whose CellProgram is
  G" (`B/metatheory/Dregg2/Coordination.lean` header, READ) and a `dregg_choreo { a ~(l)~> b ; … }`
  surface (`DSLChoreo.lean`, READ header). No Rust consumer (LANE). LEAN. Decidable **flow refinement**
  (`decideRefines` sound and complete for step-by-step simulation of guard-free, iteration-free affordance
  flows; the algebra is right-skewed, Pradic's RSKA_d⊓) is exported and called by the deploy tool
  (`B/metatheory/Dregg2/Deos/FlowRefine.lean:360-544`, `B/dregg-deploy/src/refine.rs:58-73`, LANE). RUN for
  that tool.
- **Contracts as proof obligations on kinds**: Hatchery `MintedKind` — an author's declared invariant is
  baked into every child's program, a forge detector rejects "membership without conformance", and the Lean
  rung proves `step_preserves` + `CellContract.forever` (READ header). TESTED.
- **Contracts as obligations on verbs**: `EffectHandler` bundles `step/delta/auth/admission/trace` with
  `auth_gated/admission_gated/conserves` proofs; `turn_conserves` is proved once over `Registry := List
  PackedHandler`; `HandlerExecutor` covers all 56 `FullActionA` constructors and shows concrete attacks the
  old executor admits and the handler executor rejects (READ headers). LEAN; `TurnAdmission.lean` and
  the FFI step call `execHandlerTurn` (READ grep), but I did not establish that the node's producer runs it.
- **How strongly a guarantee may be displayed**: `ResearchRegime.lean` (`Regime = ballot | optimistic |
  witness`, `Publication.honest`), `Disputation.lean` (`byzantine_majority_cannot_uphold`),
  `OptimisticAdjudication.lean` (`optimistic_sound` needs `RefutationComplete ∧ Actuated`) (LANE). LEAN; no
  product carries the field.

### 1.4 Fork 3 — concurrency

- **Ordering and execution** (RUN): one global order (Cordial Miners `tau` over the blocklace,
  `B/blocklace/src/ordering.rs:794`), FIFO mempool drained one payload per round, finalized blocks executed
  one at a time under a single `RwLock` (LANE). No `rayon`/`par_iter` in turn/node/cell/blocklace/coord
  (LANE). Each agent's turns are serialized by `previous_receipt_hash` (READ). **Bread had no concurrency
  inside a domain.**
- **Footprints** (TESTED, unused for scheduling): `ConflictSet`, a 256-bit Bloom filter over a turn's read
  and write sets, whose doc says disjoint turns "can be safely parallelized" (`B/turn/src/conflict.rs`,
  READ header); its only consumers are encrypted-turn conflict hints (submitter-declared, unchecked) and a
  frozen-cell check during cell migration (LANE).
- **Commutation** (LEAN): disjoint debits commute, contended forests reach the same outcome, joins commute
  while revoke/exercise do not (`Proof/ContendedCrossCell.lean:176`, `Proof/ContendedForest.lean:279`,
  `Consensus/OnDemandFeasibility.lean:122,158`, LANE). Nothing schedules with them.
- **Concurrent spending without coordination** (RUN): Stingray bounded counters — per-silo slices with
  `slice_ceiling = balance·(f+1)/(2f+1)`, periodic signed rebalance, fast-unlock after a 2PC abort
  (`B/coord/src/lib.rs`, READ; `StingrayCounter` in `B/node/src/state.rs:19,564,2524`, READ grep).
- **Multi-party atomicity** — Bread's working answers, in order of what ran:
  (a) compose all parties' actions into **one turn on one executor**: `CommitmentMode::Partial` signatures
  over (action hash, position, federation, nonce) are checked by the executor (RUN); `TurnComposer`
  assembles fragments (TESTED, no node route) (`B/turn/src/composer.rs` header, READ; LANE for anchors);
  sovereign cells join by witness injection into the hosted ledger for the turn (RUN, LANE);
  (b) **2PC across nodes**: `POST /turn/atomic`, votes, and a commit/abort/pending verdict computed by the
  Lean export `dregg_coord_2pc_decide` (`coord_2pc_decide_eq` proves the export *is*
  `TwoPhaseCommit.evaluate`), with the Rust coordinator demoted to a differential (`B/node/src/api.rs:8234-8260`,
  `B/node/src/coord_gate.rs`, `B/metatheory/Dregg2/Exec/DistributedExports.lean:440-470`, READ). RUN;
  (c) a cross-cell **proof aggregate** route, which attests after the fact that N per-cell receipts agree; it
  is not what makes execution atomic (LANE).
  The Lean `JointTurn` family is LEAN and partly thin: `binding_is_proper` is a 1+1≠0 counterexample
  (`B/metatheory/Dregg2/JointTurn.lean:271-284`, READ) and `atomicity_as_proof` reduces to `and_congr` (LANE).
- **Several activities per cell**: nothing. A cell advances only by turns; long-running work is outside
  (durable-workflow over duroxide/SQLite, which does not even depend on `dregg-turn`; LANE).
- **Liveness/fairness**: van Glabbeek **justness**, not fairness, as a hypothesis on an abstract schedule
  (`B/metatheory/Dregg2/Proof/Fairness.lean:1-308`, LANE). LEAN. Nothing in Rust implements it.
- **Topology-parametrized bounds**: `Topology × FaultModel × CryptoStrength`, every bound collapsing at the
  single-machine apex (`Distributed/Fibration.lean:222,240`; `Revocation.lean:84-301`; `Finality.Tier`
  `causal < ackThreshold < bft < constitutional`) (LANE). LEAN, but the principle is ember's stated design
  requirement (`MEM/project-dregg4-vision.md`, READ).

### 1.5 Fork 4 — evolution

- **What ran**: `Effect::SetProgram{cell, program}` → `apply_set_program`: cross-cell needs the
  `SetVerificationKey` permission (an `AuthRequired` lattice Signature/Proof/Either/Impossible/Custom), then
  `c.program = program` (READ `apply.rs:1416-1445`; LANE for the rest). No migration, no version pin, no
  governance, no cooling period, and its circuit binding is "owed". The whole system evolves by
  refuse-to-load re-genesis: `CANONICAL_STATE_SCHEMA_EPOCH = 27`, a mismatched store is refused
  (`B/persist/src/lib.rs:958-1117`, LANE). The only enforced timelock is on the Ethereum settlement
  verifier (`TIMELOCK_DELAY = 2 days`, LANE).
- **What was modelled** (LEAN, none wired):
  - Mina's anti-brick rule: `UpgradeAuth = byProof v | bySignature`, stale version falls back to owner
    signature; `upgrade_never_bricks` rests on the always-true signature arm, as the file admits
    (`B/metatheory/Dregg2/Upgrade.lean:1-110, 384-450`, READ). Executable form `Exec/CellUpgrade.lean`
    (READ header).
  - The svenvs envelope: a proposal is `Admissible` iff the new policy is safety-sound and permits at least
    what the old did; `admit` installs it only then; `self_improvement_is_safe` for any finite stream of
    proposals, for any controller (`Upgrade.lean:212-273`, READ). Note: `admit` is `noncomputable` — the
    gate is a proposition, so in practice it needs a proof term.
  - Typed state migration: `Migration : Schema → Schema → (Value → Value)` with `migrate_conforms`,
    `migrate_conserves` (balance total preserved) and `migrate_anti_brick` (fail-soft to identity); field-add
    and field-rename only (`Exec/StateMigration.lean`, READ header).
  - Polis constitutions: an amendment is any `Constitution → Constitution`, applied only if
    `NonRegressive` (every subject's frozen minimum floor still holds), otherwise inert;
    `amendment_stream_nonregression` (`B/metatheory/Polis/Polis.lean:253-306`, LANE). The Rust polis app
    settles amendments by M-of-N ballot plus a `TemporalGate` cooling period and stages the successor's
    descriptor hash; it has no frozen-floor check (`B/starbridge-apps/polis/src/lib.rs:14-31`, LANE).
  - Factory constructor transparency (`Exec/Factory.lean:191-248`: "the published contract holds over the
    cell's whole life") — **contradicted** by the Rust `SetProgram`, which can rewrite any live cell's
    program; the tension was never resolved (LANE).
- **Name collision to avoid**: `B/docs/DREGG-QUIET-UPGRADE.md` is a browser extension, not program
  upgrade; `Distributed/CellMigration.lean` moves a cell between federations (LANE).

### 1.6 Fork 5 — checkpoints and heap

Bread never persisted a suspended computation. Pending work was a whole `Turn` plus a
`ResolutionCondition`, re-executed from its pre-state on resolution (`B/turn/src/continuation_resume.rs:13-17`,
READ). A true mid-turn continuation (`Continuation { captured: Vec<(UKey,UVal)>, remaining }`, "a partial
turn / promise as a PASSABLE umem") exists and is serialized only in a test
(`B/turn/src/continuation.rs`, READ header; LANE for "test only"). Lean `Exec/Continuation.lean` proves the
fold split `fold pre all = fold (fold pre prefix) rest` and states plainly that a mid-turn boundary "is not
independently committable" (READ header). The Lean checkpoint/restore theorems are `rfl`
(`Exec/CellRuntime.lean:41-174`, LANE). The heap (registers + committed sorted-Poseidon2 map) is real and
RUN. Mini's whole-machine checkpoint with `state_roundTrip` is already beyond anything Bread had.

---

## 2. What Bread got right that Mini lacks, what it got wrong, and the false friends

### 2.1 Right, and missing from Mini (mechanism + file)

1. **Eager shape, lazy witness** — `B/docs/DESIGN-partial-turn-promises.md:38-43`, `§5-§6`;
   `B/metatheory/Dregg2/Exec/GuardedHole.lean:37-67` (`holeFill_binds_in_circuit`,
   `holeFill_rejects_guard_violation`, via the doc). A hole reserves no resource; value moves only inside a
   fully determined turn; so conservation stays turn-local across a two-turn promise. **For Mini:** a
   Resident that yields holds nothing implicitly. Anything it needs across the gap must be moved into an
   explicit escrow object in the yielding turn, under that object's law.
2. **One-shot resumption as a nullifier spend** — `Effect::React` spends `pending_id` once, with
   `wake.hash == pending_id` binding the spent hole to the resumed work (doc §4). **For Mini:** a yielded
   activity's await id is spent by the resume turn; a second resume with the same id is a refusal by the
   same mechanism as a double spend, and the id binds the checkpoint digest it resumes.
3. **Typed await vocabulary with broken-promise cascade and deposits** — `ResolutionCondition`
   (`AwaitReceipt | AwaitCondition | AwaitHeight`), `BrokenReason` incl. `DependencyBroken` and
   `FederationUnreachable`, deposit refunded on resolution and burned on timeout (`B/turn/src/pending.rs`,
   `B/turn/src/conditional.rs`, READ via doc §2.3-§2.4). **For Mini:** the "what it awaits (reply, message,
   time)" of the proposed Resident should be exactly this sum, plus "a proof/condition", and a broken await
   must resume the activity with a typed `Broken(reason)` response rather than leave it parked.
4. **A coordination grade per law clause** — `Confluence.lean`, `ConfluenceClassifier.lean`
   (`monotone_keeps`, `bounded_breaks`), `dregg-merge/src/gate.rs:84`, `dregg-query/src/classify.rs:38` (LANE).
   **For Mini:** Mini's law language is decidable; it can *compute* whether a clause is monotone (preserved
   by joins of the state lattice) and attach the grade. That grade is what lets concurrency (fork 3) run
   independent writes without ordering.
5. **Concurrent spending by bounded counters** — Stingray in `B/coord/src/lib.rs` and node state (READ).
   **For Mini:** the escrow-object pattern for "many activities draw from one balance" (fork 3).
6. **Verdict functions exported from Lean at the decision point** — the 2PC decision gate
   (`B/node/src/coord_gate.rs`, `DistributedExports.lean:440-470`, READ). Mini already does this more
   thoroughly (Lean admits everything); the transferable part is the **2PC shape** for cross-domain
   atomicity with a Lean-decided verdict and a no-conflicting-decision theorem.
7. **Obligations as fields of the thing registered** — `EffectHandler` (`Exec/Handler.lean`), Hatchery
   `MintedKind` (`Deos/Hatchery.lean`), `Publication.honest` (`ResearchRegime.lean`). **For Mini:** a package
   that introduces a new Plan action kind, a new object kind or a new published claim carries its proof
   obligations as fields that the certifying checker must discharge before the package is accepted.
8. **Upgrade as an admission gate with a frozen floor** — svenvs `Admissible`/`admit`
   (`Upgrade.lean:212-273`, READ) and Polis `NonRegressive` (`Polis.lean:253-306`, LANE); typed migration
   with conservation (`Exec/StateMigration.lean`, READ). None of it ran in Bread. Mini has the pieces Bread
   lacked to run it: a certifying checker and a decidable law language with entailment.
9. **Reversibility tiers** — Clean / Contextual / Committed (`B/turn/src/reversible.rs`, READ header).
   **For Mini:** classify Plan actions the same way; undo/branch features then know which actions they may
   reverse.
10. **Per-viewer affordance projection gated on cap and state** — `project_for(held)`, `GatedAffordance`,
    `Reactive.TransitionGate{pre, post, link}` (LANE). Mini's "card = authorized view + affordances" is the
    same idea; Bread's addition is that an affordance is shown only if the law would admit it *now*, which
    Mini can decide with its satisfiability check.
11. **Verified observation vs live read** — `CrossCellImport.lean:124,168` (LANE). **For Mini:** an
    in-turn read of another object is part of the turn's footprint (live, conflicts with concurrent
    writers); an *import* is a read of a past committed root (stale but stable, conflicts with nothing).
    Both are useful; they must be different operations with different names.
12. **The single-machine principle** — `MEM/project-dregg4-vision.md` (READ). **For Mini:** one Host gets
    synchronous cross-object atomicity and immediate revocation; only committee or multi-party domains pay
    for 2PC/escrow.

### 2.2 Wrong, or never finished

- **Five async mechanisms, no common one** (pipeline, pending registry, reactive effects, CapTP pipelining,
  intents), each with its own resolution table and failure story. CapTP drain and solver/challenge flows
  never ran (LANE). Lesson: Mini needs one await primitive (the Activity) and every async feature as a use
  of it.
- **Continuations that cannot see values.** `wake: Box<Turn>` is built before the promise resolves; Lean's
  `Slots := Nat → Bool` carries no data. Pipelining "sends to a promise" were never value-dependent.
- **Laws as a catalog of 69 hand-named atoms** with Lean and Rust mirrors that drifted (dispatch rules,
  `EffectKindIs`), no satisfiability, no entailment, Rust mod-p versus Lean `Int` (LANE). Mini's
  difference-logic fragment with sat checks is the correction; do not grow it into a catalog.
- **"Finalized" observations reading current state** (`execute_tree.rs:355-371`, READ).
- **No concurrency** in execution, and per-agent serialization by receipt chaining (READ) — so one agent
  could never have two things in flight.
- **Upgrade: rich theory, bare swap in practice**, and factory transparency contradicted by `SetProgram`.
- **Lean theorems about separate models**: `CapTPPipeline` over a kernel that cannot rewrite caps,
  `atomicity_as_proof` near-tautological, checkpoint theorems `rfl`, Affordance/Reactive models not
  refined by the Rust (LANE). Polis's own adversarial review found the celebrated unification to be a shape
  identity and one summit `P → P` (`MEM/project-polis-unification-correction.md`, READ).
- **deos-js cards**: an affordance was a 5-variant `ApplyOp` (`AddToSlot | SubFromSlot | SetSlot |
  SetSlotFromArg | SetRegisterFromArgs`); JS only chose which affordance to fire and with what argument;
  the cap check ran in the host and the turn was built with `ActionBuilder::new_unchecked_for_tests`; two
  engines disagreed on the fire contract; JS state was not persisted and `Math.random`/`Date` were not
  removed (`B/deos-js-core/src/lib.rs:177-219`, `B/deos-js-runtime/src/applet.rs:218-260`, LANE).

### 2.3 False friends (look transferable, are not)

| looks like | actually is | why it misleads Mini |
|---|---|---|
| `Action.method` / `InterfaceDescriptor` / `invoke()` | a tag selecting constraint cases; `invoke()` signs caller-computed effects | Mini's method *runs*. Do not import Bread's "methods" as the model of calls. |
| `EventualRef` / `Pipeline` | synchronous local batch; outputs re-derived from declared effects, not receipt-bound | not promise pipelining; the module says so (`eventual.rs:12-15`, READ) |
| `ConditionalBatch` proofs | ordering of turns with boolean slots | no dataflow was ever proved |
| `CapTPPipeline` no-amplification | true of a kernel whose `exec` cannot change caps | the property must be re-proved against Mini's real Plan application |
| `ObservedFieldEquals` "finalized" | the peer's current commitment in the hosted executor | the live/import distinction is right in Lean, wrong in the Rust |
| `Await.four_faces_unify` | `rfl`-level extraction identity | not a semantics of async |
| "program-as-JS-in-the-cell is refuted" (`C/planning/DEOS.md:447`) | what failed was host-side unchecked authority, two engines and nondeterminism, not code-in-cells as such (Bread's JS never wrote state except through `ApplyOp`) | Mini's re-executed, deterministic, kernel-admitted code avoids each failure cause; the refutation does not transfer to Objective Bend |
| `CellProgram` = "the program" | the law | Mini's package is a new thing with no Bread analogue |
| `Effect::Custom{program_vk_hash}` as "user code" | a proof checked against a VK; the v1 verifier stub accepts non-empty bytes | Mini has no proof system in admission, by decision |
| `upgrade_never_bricks` | true because the signature arm is always admissible | it says nothing about safety of the new program |
| `polis_safety`, the Polis "unification" | generic invariant induction; a shape identity | cite the specific floors, not the frame |
| durable-workflow "durable execution" | duroxide history replay outside the kernel, no `dregg-turn` dependency | not a persisted activity |

---

## 3. Recommendation per fork, and per OS subsystem

### 3.1 Fork 1 — calls across objects (make them rich; Mini can, Bread could not)

**Port as ideas:** eager-shape/lazy-witness; await-id as a nullifier with the resumed checkpoint bound to
it; the typed await sum and broken-reason cascade; deposits on long waits; verified-import vs live-read;
the sender-authenticated inbox as an object law; introductions as the way references spread.
**Leave behind:** client-computed effect lists; `method` as a tag; batch pipelines with boolean slots;
separate async mechanisms; CapTP's swiss-number bearer refs inside one domain (capabilities are already
kernel-held in Mini).

Concretely, three call forms, all landing in one `Plan` judged by every touched object's law:
1. **In-turn synchronous call** (new relative to Bread): A's method calls B's method through a capability
   A holds; B's code runs in the same re-execution, returns a value and contributes Plan actions to the
   same atomic Plan. Footprint = union of reads/writes. Bread's `SnapshotRefresh` child is the
   degenerate, value-less version of this.
2. **Eventual send** (E-style, to a reference or to a promise): the send is a Plan action that enqueues a
   message on the target's inbox object; the sender's activity may continue or await the reply.
   **Pipelining** = a send whose target is an unresolved reply; Mini can make this value-dependent because
   resumption carries a typed value (Bread could not).
3. **Await** = the Activity's yield: `awaits ∈ {Reply(id), Message(pattern), Height(h), Condition(c)}`;
   resumption is one admitted turn that spends the await id. Broken awaits resume with
   `Broken(Timeout | Rejected | DependencyBroken | Unreachable)`.
Across a yield, nothing is reserved except by an explicit escrow object (Bread's strong-hole rule).

### 3.2 Fork 2 — laws and contracts

**Port:** method-indexed law clauses with default-deny for an unmatched method (`eval.rs:118-127`);
a computed coordination grade per clause; third-party requirements (a clause satisfied by a discharge
from another object, macaroon 3P style); obligations as fields (handlers, kinds, published claims);
display strength ≤ settlement strength for every badge Mini shows (re-executed, condition-witnessed,
optimistic, ballot); decidable refinement of affordance/workflow shapes (FlowRefine) as a deploy-time
check of a package's protocol against its predecessor.
**Leave behind:** the atom catalog; Lean/Rust mirrored law languages; conservation as a colouring of
verbs (Mini's Book owns money); camera-tier unification as a goal in itself.
**On the law-language fork:** keep the decidable predicate language as the kernel's judge of Plans, and
generate clauses from `.obend` declarations (`requires`, invariants) rather than unify the two languages.
Bread's `denote_eq_exec_on_success` principle — a program can only tighten the kernel, never bypass it — is
the property to keep: code proposes, the decidable law disposes, and package-level invariants proved by the
certifying checker are *additional* evidence, never a substitute for the per-write check.

### 3.3 Fork 3 — concurrency

**Port:** declared-and-checked footprints (Bread's `ConflictSet` idea, but computed by re-execution and
exact, not a submitter-declared Bloom filter); the coordination grade from 3.2 to let monotone clauses
merge without ordering; bounded counters / escrow objects for many activities drawing on one balance;
Lean-decided 2PC for atomicity across domains, with escrow locks in each domain; the single-machine
principle; justness (not fairness) as the liveness notion to state.
**Leave behind:** per-agent serialization by receipt chaining; one global lock; "atomicity as proof" over a
shared aggregate (Mini has no proof system in admission).
**Several activities per object** has no Bread precedent. INFERRED design consequence from Bread's record:
treat each activity's checkpoint as its own small cell-like record under the object, so two activities of
one object conflict only when their footprints on the object's state overlap.

### 3.4 Fork 4 — evolution

**Port:** the upgrade capability as a permission on the object (Bread's `SetVerificationKey` lattice;
Mina's permissions); an admission gate that requires (a) the new package's laws to preserve the object's
frozen floors (Polis `NonRegressive`; svenvs `Admissible`, decided by Mini's entailment check rather than
assumed), (b) a typed, linear migration of the object's state with conservation and conformance proved
(Bread's `migrate_conforms`/`migrate_conserves`/`migrate_anti_brick` plus fareoo's K-CARRY named drops,
`F/AUDIT.md §3`, READ), (c) a cooling period for objects whose law demands one; and make "is this object
upgradable, by whom, under what floor" part of the published package, so factory transparency and upgrade
cannot contradict each other the way they did in Bread.
**Leave behind:** the bare program swap; signature fallback as a safety argument (it is an availability
argument); upgrade-by-re-genesis for objects (keep it for the semantics digest only).

### 3.5 Fork 5 — checkpoints and heap

Nothing to port; Mini is ahead. One lesson: Bread's "a mid-turn boundary is not independently committable"
(`Exec/Continuation.lean`, READ) maps onto Mini cleanly — a checkpoint is committed only at a yield that
ends an admitted turn, never inside one.

### 3.6 Bread as an OS, subsystem by subsystem

| subsystem | Bread's answer | how far it got | right for Mini? |
|---|---|---|---|
| process model | none in the kernel; agents outside; cells are passive guarded records | RUN | no — Mini's Resident/Activity is the needed upgrade |
| turns as transactions | journalled, all-or-nothing call forest; Σδ=0 per turn | RUN | yes; keep turn = unit of admission and receipt |
| cross-object calls | client-assembled forest; `ExerciseViaCapability`; `SnapshotRefresh` children | RUN | partly — keep cap-mediation; replace client-computed effects with in-turn calls |
| eventual refs / pipelining | synchronous batch; CapTP registry with unwired drain | TESTED | the idea yes, Bread's mechanism no |
| partial turns / promises | Promise/Notify/React holes as nullifiers; ConditionalTurn with deposit | RUN | yes as rules (eager shape, one-shot spend, deposit, cascade) |
| vats | Lean `VatBoundary` (cross-vat needs a witness, Φ drops confinement); in practice a federation | LEAN | yes as a concept: a domain boundary where caps become tokens |
| messaging | relay + mailbox crank + inbox cell program; SSE receipt bus | TESTED / RUN (bus) | inbox-as-object-law yes; receipt bus yes |
| joint / multi-party | one turn on one executor with partial signatures; 2PC across nodes with Lean verdict | RUN | yes, both, with escrow per domain |
| scheduling | FIFO mempool, one payload per round, no priority, per-turn fee cap | RUN | minimal; Mini needs per-activity budgets and a stated justness assumption |
| fairness | van Glabbeek justness as a hypothesis | LEAN | the right notion to state |
| concurrency control | none (serial); Bloom footprints unused; Stingray for budgets | RUN (Stingray) | footprints + grades + escrow, not serial |
| naming | content-derived cell ids; asset = issuer cell; nameservice and governed namespace as factories; petnames SDK-local; sturdy refs not served | RUN / TESTED | ids yes; names as objects in the world (fareoo finding 6) |
| persistence | redb store, refuse-to-load epochs, overlay recovery; pending turns persisted as whole turns | RUN | Mini's checkpointed activities supersede it |
| reflection | cap-bounded frustum projection (viewer is an unchecked parameter); meta-debug stack; mirror-caps unbuilt | TESTED / DOC | reflection as a held capability, checked by the kernel, is the part worth building |
| presentation | card = per-viewer cap-projected view-tree + affordances; each fire a turn | TESTED | yes; add "law would admit now" |
| governance | M-of-N ballots + cooling; Lean non-regression | RUN / LEAN | non-regression gate yes; ballots only for what really is a vote |
| evolution | bare program swap; re-genesis | RUN | no — see 3.4 |

---

## 4. Bread-era sources the literature scholars should read

Each was cited by Bread at the file given (READ unless marked). Bibliographic details for arXiv entries
were checked against the arXiv API today; I did not download or read the papers.

1. **Plotkin & Pretnar, "Handling Algebraic Effects"**, LMCS 9(4), 2013, https://arxiv.org/abs/1312.1399 —
   cited in `Dregg2/Await.lean`. Foundation for Activity-as-effect.
2. **Miller, "Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control"**,
   PhD thesis, Johns Hopkins, 2006, http://www.erights.org/talks/thesis/ — cited in `Await.lean`. Promises,
   pipelining, `when`, introductions.
3. **Honda, Yoshida & Carbone, "Multiparty Asynchronous Session Types"**, JACM 63(1), 2016 (POPL 2008) —
   cited in `Coordination.lean`. Behavioural contracts across objects.
4. **Bailis et al., "Coordination Avoidance in Database Systems"**, PVLDB 8(3), 2014,
   https://arxiv.org/abs/1402.2237 — the origin of I-confluence; *Bread uses the concept without citing it*
   (grep "Bailis" = 0).
5. **Hellerstein & Alvaro, "Keeping CALM: When Distributed Consistency Is Easy"**, CACM 63(9), 2020,
   https://arxiv.org/abs/1901.01930 — cited in Bread docs; the per-query CALM grades.
6. **Sridhar, Sonnino & Kokoris-Kogias, "Stingray: Fast Concurrent Transactions Without Consensus"**, 2025,
   https://arxiv.org/abs/2501.06531 — implemented in `B/coord/`.
7. **Keidar, Naor, Poupko & Shapiro, "Cordial Miners: Fast and Efficient Consensus for Every Eventuality"**,
   2022 (DISC 2023), https://arxiv.org/abs/2205.09174 — Bread's ordering.
8. **Danos & Krivine, "Reversible Communicating Systems"** (CONCUR 2004) and **"Transactions in RCCS"**
   (CONCUR 2005) — cited in `docs/deos/FIRST-CLASS-REVERSIBILITY.md` and the time-travel doc. Reversible
   and committed actions.
9. **Mimram & Di Giusto, "A Categorical Theory of Patches"**, ENTCS/MFPS 2013,
   https://arxiv.org/abs/1311.3903 — cited in the document-language docs. Conflicts as objects; merge as
   pushout.
10. **van Glabbeek, "Justness: A Completeness Criterion for Capturing Liveness Properties"**, FoSSaCS 2019,
    https://arxiv.org/abs/1909.00286 — cited in `Proof/Fairness.lean`.
11. **Pradic, "The equational theory of the Weihrauch lattice with (iterated) composition"**, 2024,
    https://arxiv.org/abs/2408.14999 — cited in `Deos/FlowAlgebra.lean`. Decidable flow refinement.
12. **Bracha & Ungar, "Mirrors: Design Principles for Meta-level Facilities of Object-Oriented Programming
    Languages"**, OOPSLA 2004 — cited in `docs/deos/FIRMAMENT-REFLEXIVE-SUBSTRATE.md`. Reflection as a
    capability.
13. **Nanevski, Pfenning & Pientka, "Contextual Modal Type Theory"**, ACM TOCL 9(3), 2008 — cited in
    `metatheory/docs/GUARDED-HOLES-METATHEORY.md` (guarded hole = constrained metavariable).
14. **Mina zkApp account-update forest and `set_verification_key` permissions** (o1Labs protocol docs,
    https://docs.minaprotocol.com/zkapps) — the source of Bread's call forest, partial commitments and
    anti-brick upgrade (`turn/src/composer.rs`, `Dregg2/Upgrade.lean`).
15. **Litt, Lim, Kleppmann & van Hardenberg, "Project Cambria"** (Ink & Switch, 2020,
    https://www.inkandswitch.com/cambria/) — named in `docs/deos/HYPERDREGGMEDIA-NOTES.md:51` as the model for
    "verified migration patches", never built. Typed migration as lenses.
16. **Faré (Rideau), Houyhnhnm Computing** (`B/houyhnhnm.total.txt`) — the spec Bread mapped itself onto
    (`MEM/project-distributed-houyhnhnm-frontier.md`); already read by the fareoo scholar.
17. Named in Bread's forward vision but **never cited in code** (grep = 0): **Waterken** (Close; durable,
    resumable turn capsules) and **Spritely Goblins / OCapN** (`MEM/project-dregg4-vision.md`). Both bear
    directly on Mini's persisted activities and cross-domain references and deserve a reading.

---

## 5. What I read vs relied on

READ myself: the brief; fifteen MEM files (dregg2 architecture, three projections, resource camera,
partial-turn promises, rhizomatic, right-skew, houyhnhnm frontier, dregg4, polis hub and correction,
dreggsolve, three-faced turn, lamesauce, cells-as-service, deos UX, no-proof-system); `F/AUDIT.md §0, §3-§4,
§7.8-§8`; `C/planning/DEOS.md §0, §3`; `B/docs/OVERVIEW.md`; `B/docs/DESIGN-partial-turn-promises.md` in
full; headers of `B/turn/src/{eventual,continuation,continuation_resume,pending,reactive,conflict,
bilateral_schedule,composer,collapse,reversible,routing,script,forest}.rs`; `Action` and `Turn` structs;
`execute_tree.rs:355-371, 1415-1455`; `apply_set_program`; `execute.rs` receipt-chain check; `B/coord/src/lib.rs`
header; `B/node/src/coord_gate.rs` header and `api.rs:8234-8260`; `B/intent/src/lib.rs` header; Lean:
`Await.lean` header and decls, `Exec/ConditionalTurn.lean` §1-§4, `Exec/CapTPPipeline.lean` header,
headers of `Exec/{CellUpgrade,StateMigration,Program,CellProgram,CapInbox,Continuation,CrossCellForest,
JointCell,Handler,HandlerExecutor}.lean`, `Upgrade.lean:1-275`, `JointTurn.lean:255-290`,
`Coordination.lean` and `DSLChoreo.lean` headers, `Deos/Hatchery.lean` header,
`DistributedExports.lean:440-470`.
LANE (seven Opus Explore readers, read-only, file:line reported): the remaining citations marked LANE.
I re-checked four lane claims at source and they held (cross-cell delegation denial, "finalized" read of
current state, the bare `SetProgram` swap, per-agent receipt chaining).
ASSUMED by me: that "RUN" (on the node's code path) means deployed — the one deployment unit runs
`--federation-size 1 --consensus blocklace --prove-turns` and its image provenance is itself uncertain
(`B/deploy/README.md:146,178`, LANE).
