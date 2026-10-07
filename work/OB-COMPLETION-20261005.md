# Objective Bend completion wave (2026-10-05) — P0, ahead of every other workboard row
Ember: "some of those gaps in objective bend are unacceptable :) gotta be ambitious and address comprehensively".
Each row: Opus unless noted; consultants named; acceptance has teeth; every theorem with inhabited premises, #assert_axioms.

OB1 SURFACE SEMANTICS + ELABORATOR CORRECTNESS. Define the meaning of .obend source directly (a big-step/denotational
  semantics of the surface: specs, mix/compose with C4 linearization, records, sums, let, operators, activities), and prove
  the Lean elaborator preserves it: elaborate s = ok core -> (source s evaluates to v <-> core evaluates to the corresponding
  value), plus refusal correspondence. Today nothing states that the core means what the source says. Consultants:
  ELABORATOR (a037dc14fab57375c), ELABORATOR-2 (a8d6cf0b983a195f0), SCHOLAR-BREAD-META (aa2fbe5825f9e1048).
OB2 MACHINE PRIMITIVES. `- < <= > >= / %` (and the existing + * ==) as Core4 machine primitives costing O(1) ticks per
  operation, not prelude recursion: new Primitive arms through stepRaw, the fast machine's csimp equalities, typing,
  adequacy/preservation/completeness/data-soundness (statements unchanged, cases added), the C backend and its differential,
  the front end lowering. Delete the $prelude recursion. Cohort: sharedBurn-style tick counts drop to O(1). cv 01a1060e-5dbc.
OB3 DIGEST PRIMITIVE. A hash primitive usable from .obend (BLAKE3 or the kernel's existing digest, consistent with
  Kernel/SealedMarket), with its typing and metatheory; then make world/ballot hiding (commitment = digest(vote, salt)).
  Decide primitive vs kernel-supplied value with SCHOLAR-LAWS (a675587c3c9fe2411). Can share the Core4 change window with OB2:
  coordinate, one lane may take both.
OB4 UNIQUENESS + REGISTRY. Prove deep evaluation deterministic (W26 deepEvaluates_unique is doing the core lemma; extend it),
  drop "(not proved unique)" from the receipt label, and put Core4 in Compiler/Evaluator's registry proper (deterministic
  big-step semantics + crash relation as a property of the term), so a program record can name Core4.
OB5 FAREOO MATURATION. The three missing Faré moves plus the law syntax ruling: checked `requires` with final-self discharge
  (a spec's requirements checked at compose/fix, refused by name), dynamic selection by label, generative identity, and laws
  as clauses (invariant/guard/permit/forbid) the Lean elaborator compiles to Pred, refusing anything outside the decidable
  fragment (root ruling Q2). Consultants: SCHOLAR-LAWS, SCHOLAR-OS (ae5ec47c7b8ba51ba). Sources: /Users/ember/dev/fareoo,
  work/scouts-20261003/A-fare-houyhnhnm-vs-core4.txt.
OB6 TYPED ENTRY ARGUMENTS (Sonnet). Sum-typed (and nested) entry arguments in typed-values-v1 / the Lean front end; unary `!`.
  Cohort rows; the ballot's electorate list as the acceptance.
OB7 CALL. Synchronous cross-object `call` per the design and root rulings: the callee runs its pinned package on the turn's
  snapshot, writes deferred to frame return, re-entry refused (mandatory guard; SeRIF-style theorem), Daml authority over the
  call tree, scoped grants (Pact). Consultants: SCHOLAR-CALLS (a14796793735cdd42), SCHOLAR-FRONTIER (a7ee794e8162d4d25).
  Then OB8 SEND/INBOXES (decider as role, escrowed postage, bounded queues, forwarding at resolution).
