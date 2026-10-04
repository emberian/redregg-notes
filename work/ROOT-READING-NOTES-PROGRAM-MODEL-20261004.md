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

## Laws literature, read at source (~/paperbin/world-program-model)
- mackay-necessity-specs-2022 (OOPSLA): "robust modules guarantee to do ONLY what they are supposed to do
  even with untrusted malicious clients", incl. EMERGENT behaviour across many calls. Sufficient
  conditions (Hoare) vs NECESSARY conditions: "balance does not ever decrease in the future unless some
  external object now has access to the current password" — API-independent. MINI READING: Mini's
  per-write law check gives the single-step necessity for free (every write judged); the multi-step one
  needs a history/capability notion ("who can reach the authority now"), i.e. laws over capability
  reachability, which Mini's kernel-held caps could make decidable.
- drossopoulou-external-calls-2025: PROTECTION: o is protected if no external object indirectly
  accessible from the current frame has direct access to o; calling a method can only SHRINK the set of
  indirectly accessible objects; SCOPED INVARIANTS hold in every external state of the scoped future
  (until the current call returns). Effects of external calls are precluded or LIMITED (happen only as a
  direct consequence of calls from the owner). MINI READING: in-turn calls into other principals' code
  need exactly this: what a callee can do is bounded by the capabilities reachable from what it is
  handed; Mini can compute reachability in the turn's heap.
- bernauer-daml-2023, §3.6 authorization rules (verbatim shape): Create needs S ⊆ A; Fetch needs
  A ∩ (S ∪ O) ≠ ∅; Exercise needs C ⊆ A AND its consequences are checked in context S ∪ C (signatories
  pre-authorized the consequences at creation); A does NOT propagate to consequences (delegation not
  transitive, deliberately: the authority inside a choice is fixed by the template, independent of the
  calling context); a transaction is well-authorized iff all top-level actions are. MINI READING: this
  is a complete, four-rule authorization judgement for a CALL TREE — a direct candidate for how nested
  in-turn calls get authority in Mini.
- grossman-ecf-callback-free-2018: an object is ECF in a trace if an equivalent trace without callbacks
  to it exists; dynamically checkable online; all Ethereum history except the DAO-like contracts is ECF.
  MINI READING: admission re-executes and has the whole trace, so an ECF check at admission is cheap and
  kills reentrancy as a class while still allowing callbacks that commute.
- Zoe offer safety (Agoric docs): a proposal {give, want, exit}; the user gets at least `want` or a full
  refund of `give`, never worse, enforced by Zoe holding the escrow and paying out, whatever the contract
  does; payout liveness on exit. MINI READING: the caller's own terms as part of the signed invocation,
  enforced by the kernel around the callee's code — the caller-side contract Mini lacks.

## OS lineage, read at source
- morningstar-smart-people-rationalize-2006 (Chip Morningstar, Electric Communities, verbatim): built
  KeyKOS-inspired orthogonal persistence, "and it worked"; but "for most kinds of objects, the amount of
  state you actually need to save persistently is a small fraction of the full run-time state ... in an
  orthogonal scheme you save it all, indiscriminately. The problem is not so much that it's bulky ... but
  that the volume of semantic meaning that you are now committed to maintain in near-perpetuity is
  vastly increased ... The problem of schema migration as new versions of objects were developed ...
  proved effectively intractable. Ultimately we fell back on a scheme that compelled programmers to be
  much more deliberate about what state was checkpointed, and when." MINI READING: this is the strongest
  evidence in the whole corpus and it bears directly on Mini's whole-machine checkpoints. Ember is fine
  with the checkpoint/heap design; the lesson is about its ROLE: a Core4 machine checkpoint is exact and
  cheap to take, but it must not become the long-lived form of an object's state. Durable object state =
  declared, first-order, typed data (what the law judges and migration transforms); a checkpoint = an
  in-flight activity, pinned to the package that made it, drained/replayed/mapped/aborted at upgrade.
- dfinity message-execution properties: code after `await` on an inter-canister call is a SEPARATE
  message execution; in Motoko `await` always commits the current state (await* need not); requests
  between a pair are delivered in send order; reentrancy bugs arise because state committed at the await
  can change before the callback. MINI READING: Mini's yield = ICP's await-commit, so the same bug class
  (check-then-act across a yield) applies; remedies: re-validate declared reads at resume (footprint
  check), escrow anything that must not change across the gap (Bread's no-reservation rule), and make
  the response type carry Refused/Unknown/TimedOut/Upgraded so failure is handled at receive.

## Calls/concurrency scholar, spot-checked at source
- grossman-ecf 2018 lines 1181-1182: "only 10 executions out of about 100 million were legitimately
  non-ECF" — the statistic the calls scholar uses to recommend refusing re-entry outright (the ECF
  check stays an opt-in). Confirmed verbatim.
- gelashvili-block-stm-2022 Corollary 2 (line 1333): MVMemory snapshot after completion equals the
  sequential execution — the basis for "parallel admission, root = sequential fold". Confirmed present.
- Scholar conflicts to resolve in the design: footprints learned at admission (calls) vs declared (OS);
  checkpoints long-lived if code pinned + capture rule (calls) vs short-lived by policy (OS, Morningstar).
