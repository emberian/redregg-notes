# Root reading notes — program model (what I read myself, and what it changes)

Rule from Ember (10-04): read the referents, not only the syntheses.

## Bread, read at source (~/dev/breadstuffs)
- docs/DESIGN-partial-turn-promises.md (whole). "Determination is EAGER, witness is LAZY": a hole's
  field/actor/target/guard are fixed at creation, only the value arrives. Promise/Notify (Generative) and
  React (Terminal) are real effects in effects_hash; React binds wake.hash == pending_id and spends
  pending_id into the SAME nullifier set as note spends (journaled). ConditionalTurn = escrow envelope with
  deposit refunded on resolution, burned on timeout; ProofCondition {HashPreimage, RemoteProof,
  LocalProof, TurnExecuted}; descriptor chosen by the condition, not the prover. Conservation holds per
  turn only because a hole reserves NO resource; value-carrying promises were out of scope by design
  ("strong hole" inexpressible). MINI READING: Mini satisfies eager-shape per turn structurally (a yield
  ends a fully determined, conserving turn; a resume is a new one), so Mini CAN have value-carrying
  resumption without the strong hole. What Mini must copy: await id spent like a nullifier and bound to
  the checkpoint digest; deposit/timeout economics; typed broken reasons with cascade.
- turn/src/action.rs Action: target, method (a hashed Symbol), args, authorization, preconditions,
  effects: Vec<Effect> (caller-computed), may_delegate, commitment_mode Full|Partial, balance_change
  (Mina-style signed delta, sum zero per turn), witness_blobs. Confirms: Bread calls carry effects the
  client computed.
- turn/src/eventual.rs header: "This is NOT async promise pipelining in the E-language sense. All
  execution is synchronous and local." pending.rs: AwaitReceipt / AwaitCondition / AwaitHeight; broken
  propagation cascades to dependents.
- metatheory/Dregg2/Await.lean: Plotkin–Pretnar signature Op = await p | call cap | emit eff; Computation
  = free tree; OneShot continuation with resume as the sole eliminator; the turn as rollback handler
  (commit resumes once, abort discards). Never executed. MINI READING: this IS Mini's activity, which
  does execute (perform/yield/resume + checkpoint). Mini's perform plan ~ emit; call (eventual send) and
  await (on a promise) are what Mini still lacks as first-class operations.
- metatheory/Dregg2/Exec/CapTP.lean: pipelining_preserves_seam is Iff.rfl (delivery rewrites only the
  target). True by construction; NOT evidence. Mini must prove "resolving a promise conjures no
  authority" against the real Plan application.
- metatheory/Dregg2/Confluence.lean: IConfluent I := ∀ x y, I x → I y → I (x ⊔ y) over a join-
  semilattice state (BEC Thm 3.1 = Bailis); tier-1 (coordination-free) iff I-confluent;
  nonpairwise_escalation gives the clashing pair. MINI READING: Mini's decidable law language could
  DECIDE I-confluence per clause for its fragment, given a merge order on states.
- coord/src/lib.rs: three layers — causal hash-chaining; 2PC multi-party forest with threshold QC;
  Stingray bounded counters, slice_ceiling = B(f+1)/(2f+1), signed rebalance, fast-unlock after abort.
- metatheory/Dregg2/Upgrade.lean: Admissible newp = SoundPolicy newp ∧ (oldp ⊆ newp permissions) —
  upgrades may WIDEN permissions but never leave the safety envelope (safe + shield); admit is
  noncomputable (needs a proof). self_improvement_is_safe over any proposal stream. Distinct from Polis
  "frozen floors" (non-regression). Mini wants both: a safety envelope that can never be left, and
  per-subject floors that can never be lowered.
- MEM lamesauce critique (06-11): "our caveats and predicates are lamesauce"; the keystone question:
  what predicate/caveat LANGUAGE makes real apps natural — derive it from what apps could not say.
  MINI READING: the law-language fork should be decided from an app-gap list, not from elegance.
