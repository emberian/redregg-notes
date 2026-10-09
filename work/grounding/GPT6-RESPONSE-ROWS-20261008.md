# GPT-6's response to the 10-07 report (2026-10-08) → work rows
Full text: pasted by Ember into root session ce776c01 (retrieve: `cv search "exact-intent admission certificate"` then `cv show --range`).
GPT-6 inspected source at 061fcfc1 and read the whole report; it did not rebuild. Verdict: substantial improvement. The next wave
should be a WHOLE-SYSTEM INTEGRATION milestone, not another broad expansion: connect authenticated request → exact judged effects →
committed record → reply → implementation artifact. "The recurring failure was proving the nearby thing while leaving the decisive
connection implicit."

## Three tracks (GPT-6's authorization) + the Lean upgrade now

### T1 TRUST & COMMIT BOUNDARY
- **T1.1 Exact-intent admission certificate.**
  - `CheckedCommit cfg before := {intent, admitted : Admissible cfg before intent}`, and the durable writer consumes ONLY that.
  - `Admissible` = finalized kernel turn | inert seat turn | ordinary admitted intent | replay contract.
  - Any post-admission transformation either preserves the intent exactly or re-proves admission. Seat joins, fees, refunds, domain
    guards and newborn init all happen BEFORE sealing.
  - The census then polices only the native escape routes.
  - State the ordinary/inert noninterference facts as standalone lemmas:
    OrdinaryAdmitted(s,i) ⇒ Protected(apply s i) = Protected s.
  - ACCEPTANCE: mutate the final post after authorization, keeping its cell id and pre-root. It must be impossible to submit through
    the checked API or refused before commit. Cover a business write, a newborn law source, a refund and an omitted domain guard.
- **T1.2 Remaining-budget meter.** Today exec runs an extraction under planBudget (= the per-extraction max M) and only then
  draws, so a turn can consume u+M against allowance A.
  - Fix: extractionBudget = min(M, remaining).
  - Return the remaining meter on success AND failure.
  - Distinguish allowance exhaustion from a semantic extraction failure.
  - Single-extraction reservation stays as an explicit reservation CONTRACT over the same machinery.
  - No refunds yet: that is a policy choice, not a determinism problem.
- **T1.3 Whole-request coverage matrix.** Per ingress family, one row each:
  1. before auth: bounded decode/lookup cost;
  2. before expensive compute: auth + reserved funding;
  3. during: a cumulative limit that can STOP work;
  4. on failure: exact rollback + explicit fee disposition;
  5. on contention: retry and accounting behavior.

  Every route gets a row, and the code must actually draw from the meter. Known gaps:
  - seats decide before signature verification;
  - post-work failures still free;
  - native extraction priced but unused;
  - generated core produced before its size is checked.
- **T1.4 Frontend pricing honesty.** Measured best-of-3 is not a worst-case bound.
  - Add deterministic phase limits: generated nodes and distinct instances, not only input bytes.
  - Add a per-turn checked cache keyed by exact source, frontend id, options and library closure.
  - Calibrate conservatively.
  - Fix the in-tree 4 MiB policy at the 256K-calibrated rates (cv 01a11680-f2cc).
- **T1.5 Retry disposition.**
  - (a) Choose and document the receipt-retrieval rule: an exact recorded ingress returns its receipt WITHOUT a fresh signature
    check, while re-signed retries go through verifyRetry. Decide this, including after key rotation, and prove a routing
    theorem over `receiveLoaded`, not a helper.
  - (b) Give a recorded operation a STABLE terminal disposition across retries: today an initial charged failure answers
    `.charged`, but replay answers `.confirmed .replayed`.
  - (c) Classify fields as operation key, business-intent digest or attempt parameters:
    - business intent changed under the same op key → conflict;
    - attempt params changed → return the ORIGINAL result, labelled as the original execution and payer.
  - JOURNEY: a charged failure, a lost response, then an exact retry and a fresh-signature retry. Both report the same terminal
    disposition, and nothing is re-charged.
  - Stale read versions are rejected cheaply before replay.
- **T1.6 Artifact ownership, not prose.**
  - No hard-linked writable workspaces over immutable content: use reflink/copy.
  - The published artifact store is owned by a distinct principal and read-only to workers.
  - Each build system exclusively owns its outputs.
- **T1.7 Role generation / fencing tokens.**
  - Stable role addresses. Every mutating op presents the current generation, and retirement invalidates the old one.
  - Ref updates use expected-old-value (CAS).
  - Stale agents may answer questions but cannot write.
- **T1.8 Coprocess acceptance tests.** A late reply; a truncated reply followed by another request; recovery after helper failure.
  The protected property is request/response association plus clean recovery.

### T2 STORE & EXECUTION REFINEMENT
- **T2.1 Prepared-effect equivalence.** Prove π(prepare_light) = π(prepare_full), where π covers final writes, guards,
  nullifiers, fee effects and signed outcome. Today the theorems only compare outcome SHAPE (`.map fun _ => ()`) and execution
  of the same intent.
- **T2.2 Maintained-index invariant.** IndexRoot(s) = rootOf(LogicalIndex(CommittedLog s)).
  - Prove it at init and its preservation under insert/update/delete.
  - Connect authenticated answers to the logical history.
  - FAULT TO EXCLUDE: an incremental-index bug omits a consumed nullifier, and a genuine non-membership proof then verifies
    against the wrong root. No collision is needed.
- **T2.3 Whole-open refinement with an explicit fault model.**
  - Well-formed-store refinement: a relation established at init, preserved by operations, with equal observables.
  - Corruption handling: no unauthenticated answer is ever consumed; corruption is rejected at use; the audit detects what it claims.
  - Don't demand identical opens on corrupted stores.
- **T2.4 Collision extractor.** The deployed lookup theorem's disjunct "∃x≠y. H x = H y" is vacuous for a fixed-width hash.
  - Expose climb_sound's locality instead: WrongAcceptedAnswer ⇒ extractCollision(honest, opening) = some (x,y), with a cost
    bound. Or prove correctness assuming no collision among the finite relevant node inputs.
  - Apply the same discipline to key derivation and to the old injective-digest premises.
  - Don't claim "a proved security level" until this lands.
- **T2.5 Profiling.** Light-open checkIndex (~75% of its time), allocation/copy/serialization, and the Lean-vs-C gap. Profile
  now; don't switch admission to a C backend on a few matching outputs.

### T3 ONE COMPLETE PRODUCT COMPOSITION
- A real multi-module application using package laws, scoped grants, async sends, retries and an upgrade.
- Required journeys: crash/restart, charged failure, lost reply, cancellation and upgrade all preserve the same user-visible
  obligations.
- Put the action-factory and package-law acceptance cases into the standing gate.
- Lift fan-out/depth bounds from arithmetic lemmas to the app's actual message histories.
- Defer: deeper pipelining, law-language expansion, the compose-order flag day.

### L LEAN v4.34 UPGRADE NOW (bounded campaign; 4.34 has 3 soundness fixes)
- Do it in a dedicated lane with an isolated cache and fresh verification of the critical closure, before any module-system
  conversion.
- Do NOT convert kernel-checked examples to native_decide just to go green: that changes the evidence class. Prefer certificate
  lemmas for the expensive arithmetic.
- Ember accepts the new Classical.choice dependencies.
- Include the dependency-collector fix (V1).

## Corrections to OUR process and rules (do before they become habits)
- **V1 Manifest dependency collector bug (CONFIRMED by GPT-6 in source).** Verify/ObjectiveManifest.lean uses
  `Expr.getUsedConstants`. In Lean 4.30 that collector skips the `Expr.proj` structure-type name (upstream PR #14728 fixes it).
  - Backport or upgrade, and add a focused test.
  - Keep two manifest scopes: logical definitional deps (opaque bodies as leaves) vs runtime implementation deps.
- **V2 The TokenCensus ban on "an L1 theorem whose proof is a bare field projection" is the WRONG RULE.** Projecting `sound` out
  of proof-carrying data is correct.
  - Replace it with checks on proposition content, constructor provenance, exact request/result indexing, and coverage of all
    minting paths.
  - Proof length or tactic (`rfl`) is not an assurance metric.
- **V3 Vacuity has several forms:**
  - an impossible precondition;
  - a tautological conclusion;
  - a circular contract;
  - an abstraction too weak for the property;
  - correct but disconnected from deployment.

  Use ABLATION tests: remove the check believed to enforce a guarantee and see whether the GUARANTEE fails, not just a script. An
  unsuccessful search = unknown. Satisfying/refuting pairs are for predicate families, not every theorem.
- **V4 Census caveat.** Shape counts are heuristics. escrow_conservation is per-operation facts, not a global history invariant;
  reclassify it.
- **V5 Root-grouped ledger approvals.**
  - A root-level change approval covers its exact affected dependent set, binding old/new root hashes + the affected claims + a
    semantic reason.
  - Important removed/restated guarantees need an implication/adapter from the replacement to the old public contract.
- **V6 Deployable ≠ green.** Deployable = RequiredStaticGates ∧ RequiredJourneys ∧ ArtifactIdentityVerified, for the SAME
  candidate artifacts and config.
  - Name the supported product surface and its required journeys.
  - An evidence key over sources doesn't establish binary provenance (cache poisoning showed why): hash outputs + record build
    provenance.
- **V7 VERIFY-ONCE + impact analysis.** A lane that changes an API checks its affected scripts, census rows and consumers itself;
  no extra full build needed.

## Answers to our questions (decisions to record)
- **5.1 Metering:** the allowance shape is right; bound execution BEFORE spend (T1.2). Refunds are a later policy choice.
- **5.2 Domains:**
  - (a) the classification is sound for modelled steps; make it structurally compulsory via T1.1;
  - (b) a validated StateInvariant fragment: REJECT transition atoms (`monotone`, …) at registration rather than evaluating them
    on identical old/new views. A separate joint TRANSITION policy is a legitimate future construct;
  - (c) a zero domainWork rate only as an explicit subsidy. Member caps don't bound predicate traversal, state size or integer
    arithmetic, so fix the source comment;
  - permanent membership must be explicit at registration and tested against required exits.
- **5.3 instance_accepted:** a DEFERRAL, not unnecessary.
  - Keep closed-program rechecking.
  - Route: PTy→Ty translation/substitution/canonicalization commutation, then Discharges.check_instantiate.
  - The three-package fixture is final-self integration, not separate compilation.
  - A stronger test adds unknown fields/components without editing old modules' target descriptions.
- **5.4 op-id:** prove the routing theorem over `receiveLoaded`. Plus T1.5.
- **5.5:** (a) and 5.12(c): refinement with a fault model (T2.3); (c) upgrade Lean now (L).
- **5.6:** reject stale read versions cheaply before replay; charge only genuinely-required pre-discovery work. Disjoint changes
  must not invalidate a plan whose full authenticated dependency set is unchanged.
- **5.7:** dropping the authority-root pin is OK IF a theorem shows two admissible pre-states give the same consent-relevant effect
  projection on success.
- **5.8:** phase limits + per-turn checked caching + conservative calibration (T1.4).
- **5.9:** root-grouped approvals (V5).
- **5.10:** the vacuity taxonomy + ablation (V3).
- **5.11:** ownership isolation (T1.6).
- **5.12:**
  - (a) prioritise liveness that bounds real obligations, with named actor/fairness/funding/chain-progress assumptions: funded
    messages reach a terminal disposition; drains finish; retries create no new obligations; cancel/refund can't strand funds;
  - (b) a small local coinductive relation closed under responses and successors, with explicit divergence. Finite traces alone
    are insufficient. Keep both obligations named: checkpointed↔uncheckpointed AND machine↔reference-language;
  - (c) maintained relation, not "equal reads".
- **Row G:** LawExpr.denote + compile_sound is the pattern for the next LT3 slice. Prioritise composition/method-contribution
  semantics over the compose-order edition change.
- **Grants:** the signer display must say `ArgsBound.capped` leaves other args unconstrained. spendFrom tries later grants (it is
  not a first-naming rule); document it.
- **Assurance case:** keep it SMALL. Top claim: "for this supported configuration and artifact set, every committed operation
  preserves the named authority, state, accounting and recovery contracts". Under it link implementing path → theorem+premises →
  deployment coverage → required execution evidence.
