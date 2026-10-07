# 06 — Laws as decidable predicates; offer safety and seats

Code: minidregg main `4ef4e808`, read only. Literature tags: **READ** (read at the cited place, by me or a
worker), **VIA-SCHOLAR** (from an earlier scholar report, named, not re-verified here), **INFERRED**.
Worker verification of eUTxO/Zoe/Daml primary texts: `lit/LIT-W3-calls-sends-contracts.md`.

## 1. Current design

**A law is a decidable two-state predicate, and every write of an object's declared state passes it.**
- `Pred` (`Pred/Core.lean:170-206`) is a closed first-order language over named integer slots of the old
  and new state: `eq`, `le`, `memberOf`, `writeOnce`, `monotone`, `eqSlots`, `leSlots`, `leSlotsOff`,
  `hashEq` (commit–reveal), `ran program` (re-execution as a first-party fact), `witnessed vk` (a
  third-party claim; first-party `eval` **fails closed**), negation and boolean combinators. Decidable by
  construction; satisfiability certificates (`decide_unsat_iff`, VIA-SCHOLAR REVIEW-SCHOLAR-LAWS §5).
- `ObjectRecord.admitWrite` (`Kernel/ObjectRecord.lean:212`) projects (facts, old, new) into views and
  evaluates `record.law`; `admitWrite_ok_iff` (`:221`) is the exact characterization. Facts are `subject`,
  `height`, `target`, `turn`, `caller` (`docs/OBJECTIVE-BEND-EVENTS.md` "Objects and their law").
- Every path that writes declared state goes through it: `Birth.write_judged`, `Delivery.write_judged`,
  `StateWrite.write_judged`, and in calls `invocation_writes_from_view` (`Kernel/ObjectiveCall.lean:1233`:
  every write `w` has `w.before = w.viewed ∧ admitWrite … = .ok ()`). A delivery's write is judged with the
  activity's principal as subject, never the deliverer.
- **Three different things are called "law"/"requires"** (`docs/OBJECTIVE-BEND.md:545-559`): the cell law
  (`Pred`, the admission judge); a spec `law name(args): expr` (a hidden Bool-typed knot field, status
  always `unchecked`, never evaluated — `law impossible: false` is accepted, probe W08 red); and
  `requires` (the Self bound, checked by typing). `.obend` cannot state its own object's law: the
  `invariant/guard/permit/forbid` clauses compiled to `Pred` are designed, not built (OB5).
- **The pin gap.** `Pred.objectivePin` (`Pred/Core.lean:372`) exists, but no turn installs it and the object
  law view has no `objective/artifact` slot (`docs/OBJECTIVE-BEND.md:538-543`), so an object's law cannot
  yet say "only my pinned package's code may write me". (REVIEW-SCHOLAR-LAWS D-1; DEPUTY-OB-ENG is building
  "kernel pin clause at object create" — engineering, per its 10-06 message.)

**Seats** (`Kernel/Seat.lean`; header `:1-40`).
- `offerSafe proposal = any [all (want ≥), all (give ≥)]` (`:84-86`), a `Pred`, judged on a **total** view
  of the seat account's Book balances (`view_total`), on every reallocation by the seat's own contract
  instance. Docstring: "Offer safety (Zoe `isOfferSafe`)".
- `exit` is a kernel step that never consults a contract clause: `exit_enabled` (`:1314`), `exit_after_deadline`,
  `exit_pays_allocation` (`:1343`). Invariant over reachable worlds: `seat_offer_safe_forever` (`:1287`).
  Conservation: `seat_conserves`. The contract acts only through the Plan its re-executed code returns.

- **What a seat contract sees** (`Kernel/SeatStore.lean:255-266`): `callData` = `{input, height, seats}`,
  each seat `{seat, role, terms, give, want, allocation}`. No principal identity. DEPUTY-PRODUCT's bounty
  port asked to widen it; DEPUTY-OB-ENG approved the seat's `exit` rule and `opened` order and **held for
  this round** `invoker` and per-seat `offerer`, `payee`, `holder` (its 10-06 message).

## 2. What it commits us to

1. **Code proposes, law disposes**, independent of who proposed: the law is a per-write monitor, not a
   property proved of the code. A program cannot raise its own authority. (Strength: "robust safety" —
   VIA-SCHOLAR LAWS Part II ¶1 citing Necessity, Drossopoulou et al., and Robust Safety for Move.)
2. **Laws are first-order and two-state.** No quantification over history, no reading other objects, no
   arithmetic beyond difference constraints and constants. Anything else must be (a) compiled into kernel
   history slots (designed, not built; LAWS idea 4, REVIEW-LAWS D-8 says keep it propositional), or
   (b) pushed into `witnessed`/`ran`.
3. **Two separate languages for one word.** Spec `law` (Bool Core4 code, unchecked) and cell law (`Pred`).
   The root's OPEN 2 (generate laws from `.obend` now vs unify) is still open
   (`ROOT-PROGRAM-MODEL-DECISIONS-20261004.md:117-124`); REVIEW-SCHOLAR-LAWS §5 answers "unify the syntax,
   keep `Pred` as the semantics, refuse anything outside the fragment".
4. **Offer safety is a state predicate, payout liveness is a kernel step.** Ours is the Zoe split
   (offer safety checked at reallocation; exit always available). It inherits Zoe's corner: with `want =
   []` the first disjunct is `all [] = true`, so **every reallocation is offer-safe and the contract may
   take all of `give`** (REVIEW-SCHOLAR-LAWS D-5). Main has no `donate` flag or empty-want refusal
   (grep of `Kernel/Seat.lean` for donat/want: none).

## 3. Literature

- **eUTxO** (Chakravarty, Chapman, MacKenzie, Melkonian, Peyton Jones, Wadler 2020, "The Extended UTXO
  Model", WTSC; paperbin `chakravarty-eutxo-2020.txt` ll.120-133, 375-420, 528-545). READ (LIT-W3 §10).
  Validator `ν(value, δ, ρ, tx) = true`: a predicate over (datum, redeemer, **the entire transaction**). Same
  shape as our law, with three differences: (a) the validator sees **all** other inputs and outputs, so
  multi-object invariants are expressible — ours sees one object's (old, new) plus request facts; (b) validators
  run only on *spend*; "There is no notion of initial state, since we would not be able to enforce it on the
  blockchain level" (CEM §4.1) — our laws judge births too (`Birth.write_judged`); (c) eUTxO's concurrency
  comes from consume-once outputs, ours from turn order. The CEM↔ledger result is a *weak* bisimulation.
- **Zoe** (Agoric; paperbin `agoric-src-offerSafety-2026.js`, `agoric-src-zcfSeat-2026.js`,
  `agoric-doc-zoe-proposal-2026.md`). READ (LIT-W3 §3). Offer safety: "the user is guaranteed to either get
  at least what they wanted, or get back a full refund of what they offered"; `isOfferSafe(proposal,
  newAllocation)` is `satisfiesGive || satisfiesWant` — ours is the same disjunction. It is safe by **induction**
  (escrowed give is safe; every committed reallocation checked). Two differences in our favour, both read:
  Zoe allows a `waived` exit ("The offering party can't cancel"); ours has only `onDemand | afterDeadline`
  (`Kernel/Seat.lean:58-62`). And Zoe's `zcfMintReallocator.reallocate` commits with **no** conservation or
  offer-safety check (`zcfSeat.js` ll.323-346; whole-Zoe status unknown), whereas our
  `seat_debit_authorized` (`Kernel/Seat.lean:1383`) enumerates the only debit paths and
  `seat_offer_safe_forever` is the reachable-state invariant.
- **Cedar** (Cutler et al. 2024, "Cedar: A New Language for Expressive, Fast, Safe, and Analyzable
  Authorization", OOPSLA; paperbin `cutler-cedar-2024.pdf`): a deliberately limited, separate policy
  language because analysability is the product; deny-by-default, forbid overrides permit, Lean-proved
  symbolic compilation. VIA-SCHOLAR LAWS D1/D3. Supports keeping `Pred` the semantics.
- **Daml** (Bernauer et al. 2023; paperbin `bernauer-daml-2023.pdf`) §3.6: signatories pre-authorize the
  consequences of their contract's choices. Mini has no signatory referent on `ObjectRecord`
  (REVIEW-SCHOLAR-LAWS D-6; `grep creators Kernel/ObjectRecord.lean`: none). See topic 05 for authority.
- **Move specs / Prover** (Dill et al. 2021, paperbin `dill-move-prover-2021.pdf`): `invariant update`
  relates old and new state; VIA-SCHOLAR LAWS idea 1 proposes `new[a] ≤ old[b] + k` atoms (still
  difference logic, so decidable).

## 4. Questions for GPT-6

- **Q6-1 (sharp).** Two meanings of "law": should the `.obend` spec `law` be *deleted* until it can be
  compiled to a `Pred` clause or discharged (doctrine: never keep a no-op the next reader trusts), or kept as
  "unchecked" metadata? If compiled, what is the right boundary between a property of the *method* (proved
  once at publish, a refinement) and a property of the *transition* (judged at every write)?
- **Q6-2.** Is a two-state, first-order, difference-logic judge expressive enough for the contracts we want
  (escrow, auction, ballot, vesting), given that temporal properties must be compiled into
  kernel-maintained history slots? Where does the literature (Cedar, Move invariants, eUTxO, past-time LTL
  monitors) say this boundary *fails*?
- **Q6-3.** Offer safety with an empty `want`: a donation by accident. Refuse unless explicit, or is there a
  principled reason Zoe left it permissive?
- **Q6-4.** Laws judge each *write*. With synchronous calls (topic 05) a single turn makes several writes
  across objects, each judged locally against its own frame's view. The OB7 lane chose per-frame over
  per-turn judgement for a stated reason: "turn-end judgment under the last writer's facts lets a granted
  later frame launder an ungranted earlier write" (`hbox:/tank/dregg-build/claude-lanes/ob8/STATUS.txt`,
  "DECISIONS + REASONS (OB7)"). Is there a cross-object invariant (A's balance + B's balance constant) that
  per-frame local judging provably cannot protect, and if so, is the answer a per-turn *conjunction* (every
  frame's law under its own facts, plus a turn-level law), rather than a choice between the two?
- **Q6-5 (from DEPUTY-OB-ENG / DEPUTY-PRODUCT).** Should seat contract code learn principal identities
  (`invoker`, `offerer`, `payee`, `holder`)? Options: (a) never; (b) opt-in per proposal (the offerer consents
  to disclosure in its terms); (c) always. Payment does not need identity (the kernel pays the payee
  regardless), but identity lets a contract discriminate by *who* and condition reallocation on it, which
  changes the information-flow story behind offer safety. Zoe's documented access model is capability-based
  (facets, invitations; `agoric-doc-zoe-contract-access-control-2026.md` "Object Access Rules"), and no Zoe
  doc I searched gives a contract the offerer's identity (READ, negative search of the Zoe docs in paperbin;
  that Zoe *deliberately* withholds it is INFERRED). Is identity-blindness part of what offer safety means, or
  orthogonal to it?
