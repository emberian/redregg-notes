# GPT-6's response to the grounding packet (2026-10-06) → work rows
Full text: pasted by Ember into root session ce776c01 (retrieve: `cv show ce776c01 --grep "active-frame view stability"`).
GPT-6 reviewed at public 84a6dac8; source-and-contract review, not a Lean rebuild. Verdict: keep the computational core; LT2 and the
forcing work earned credit; the next wave is COMPOSITIONAL CONTRACTS, not more features. Several packet claims overreached
(re-entry dispute is answerable from code; genericity is universal not existential; activity restriction is narrower; metadata
needn't block optimization). Status: proposed contracts, not checked proofs.

## Corrections to our own claims (fix docs/packet wording)
- Re-entry: W3's "deferred writes suffice" assumed a same-slot abort that doesn't exist; frameReturn applies edits to CURRENT state.
  Keep the guard; the property it buys is ACTIVE-FRAME VIEW STABILITY (descendants can't change the frame's own object state between
  entry and return), not merely a Nodup stack.
- Resume-with-view does not categorically violate Khan's PC: name it "checkpoint-prefix preservation with fresh environmental input".
- Activities: `Nat -> Activity<P,R,A>` factories are storable at core level (field rule excludes computation-HEADED types only).
  Acceptance probe first: store a factory, invoke twice, see two interactions.
- Reflection: metadata distinguishes construction trees over exposed leaves (not arbitrary code); optimizers may keep metadata m
  and replace behaviour e by an equivalent e' — no whole-program metadata non-interference needed.
- Existentials don't inherently hide provenance; Zoe "vulnerability" from a partial reading stays unconfirmed.

## Rows (by workstream, with acceptance)
A AUTHORITY & FRAMES — prove active-frame view stability (frameReturn: before = viewed); explicit DAO witness as a test; grants bind
  (target, method, interface/code id, canonical args, scope, uses) + optional caller/tree-position restriction; bounded constraints
  (recipient, cumulative cap) instead of widening; invariant "every frame receiving delegated authority has a matching unconsumed
  authorization"; keep delegation (request/subject) separate from consent (law). Relational invariants: registered, authoritative
  INVARIANT DOMAINS checked in conjunction with per-frame laws (bounded authenticated data, no discovery calls). Keep call = atomic
  co-failure; catchable failure only with specified savepoints.
B ACTIVITY SEMANTICS — machine yield ↔ reference interaction Vis(p,k): for every admissible response r, resuming s' corresponds to k(r);
  lift through call/send/await handlers; distinguish silent divergence from eventual visible progress (interaction trees).
C CHECKPOINT RESOURCES — three obligations: semantic correspondence (no invented behaviour), quantitative refinement with a budget
  VECTOR (ticks, heap, stack, materialization, sizes), deployed accounting (kernel admits/pays exactly what the refinement allows).
  The CONVERSE wanted: N(s)⇓_B o ⇒ ∃B'. s⇓_{B'} o' ∧ o≈o' ("difference is resources only"). Relate the continuation STATES, not only
  equal next Plans. Don't make forcing free; deterministic protocol representation for checkpoint bytes (digests!) separate from
  semantic heap equivalence.
D OPEN COMPONENT CONTRACTS — composition contract C_{A;B}(S,I)=C_A(S,I)∧C_B(S,F_A(S,I)), F_{A;B}=F_B(S,F_A(S,I)) as a front-end
  operation; discharge at fix; front-end commuting square (template ∘ subst = elaborate(instance)); Super genuinely abstract with
  per-operation constraints (add needs absence, override needs compatible membership, replace changes type); separately checkable
  open component artifacts linked before closed Core4 (staged modularity, say so); acceptance = three-package final-self case
  (references inside A and B see C's final definitions).
E SOURCE MEANING & ADMISSION WORK — LT3 vertical slice: independent meaning of compose order, ancestry, method contribution + lowering
  theorem; WHOLE-REQUEST work account (front end, generated core size, instances, execution, extraction, serialization, queue);
  charged execution-failure receipt after auth+funding (rollback business effects) vs cheap malformed rejection; C4: declarative
  C4Valid + soundness/determinism/completeness, fuel exhaustion ≠ inconsistency, well-formed precedence oracle; source order
  most-specific-first for compose and extends via an explicit EDITION change; digest primitive over canonical bytes with bounds.
F ASYNC EXECUTION — onward sends via bounded prepaid continuation allowance (conservation across forward/cancel/refund; bounded
  fan-out and depth); until then refuse sends from delivered methods at the interface; separate STOP-WAITING from CANCEL-IF-QUEUED;
  timeouts don't break never-expiring slots; stable operation ids for retries; deeper pipelining only with recorded dependencies
  (acyclic, single terminal decision, exactly-once escrow, bounded cascades); FIFO by entry into the RESOLVED destination queue.
G LAWS & SEATS — `law` = enforced predicate or accepted proof obligation; unchecked → `claim`/`example`; compile a specified source
  fragment to Pred; empty-want donation explicit (done-ish: marker); identity-blind contract input by default, narrow opt-in
  (offerer/payee/holder/invoker distinct); liveness claims state their actor assumptions.
H SWARM EVIDENCE — evidence key = (tree, toolchain, options, dependency closure, gate defs, fixtures, generated inputs); `green` is a
  certified product distinct from main; per-module content-addressed manifests hashing statements AND their definition closure
  (`Safe := True` must be caught); generated fixtures get an independent authority; evidence dimensions (proposition+axioms,
  execution+world, mutation+observed failure, artifact id, certified commit) recorded separately, not a ladder; distilled context is
  an index into evidence, not evidence.
