# 04 — Activities, answer slots, resume-with-view, checkpoint transparency

Code: minidregg main `4ef4e808`, read only. Literature: `lit/LIT-W2-laziness-reflection-continuations.md`
(§B effects and laziness, §C guardedness, §E continuations/durable execution) and LIT-W3 §7 (Khan).

## 1. Current design

**The construct.** `Activity<P, R, A>` yields Plans of the first-order sum `P`, is resumed with data of type
`R`, finishes with `A`. `perform` is not a value and never a reduction: a term whose next redex is a perform
has *yielded* (`yields_no_step`, `Theory/ObjectiveBendOpenRecursion.lean:497`; `yields_deterministic`,
`:552`). Matching on a perform sequences; arms are handlers; `done` lifts a pure tail.

**Effects never sit in shared cells.** An activity type is never shareable: every typing rule that
allocates a heap cell refuses it (`effect_as_argument_refused`, `Theory/ObjectiveBendTyping.lean:1391`, and
siblings for fields, payloads, specifications, Plans). The front end refuses `nullary-activity` (a
parameterless definition is a shared lazy value, so its effect would run once and be cached). On the
machine, `perform` under an update frame (while forcing a shared cell) is refused `sharedEffect`
(`perform_under_update_refused`, `Theory/ObjectiveBendDemandMachine.lean:269`), and a checked program
never reaches that refusal (`checked_reachable_no_refusal`, `Theory/ObjectiveBendDemandPreservation.lean:87`).
At a typed yield no frame forces a shared cell (`typed_yield_quiescent`,
`Theory/ObjectiveBendDemandPreservation/Cases/Activities.lean:161`).

**Kernel awaits.** A resident yields `await {write, on, patience}`; `on` is an answer slot (one decider) or
a height; the deadline is mandatory (patience ≤ `maxPatience` = 64, `Kernel/ObjectiveKernelConfig.lean:34`).
It is resumed with `resumed {outcome, view}`, the outcome exactly as settled
(`reply | refused | unknown | timedOut | broken | upgraded`; nothing produces `upgraded`) and the object's
declared state **read in the resuming turn**. Edits (`keep | set v | add n`) apply to that view:
`resume_view_current` (`Kernel/ObjectiveActivity.lean:2662`), `yield_write_from_current_read` (`:2694`),
`moved_state_refuses` (`:2725`). `add`-only writes commute (`add_writes_commute`).

**Answer slots** (`Kernel/AnswerSlot.lean`): name `H(turn, record cell, generation)` no submitter
chooses; one decider fixed at opening; one deadline; one terminal decision (`decide_single_decider`,
`:203`; `slot_decided_once`, `Kernel/ObjectiveActivity.lean:2411`).

**The resume contract.** A delivery spends the await as a nullifier `H(record cell, generation,
checkpoint digest)` and CASes the record against its current root: `resume_consumes_once` (`:2399`),
`resume_outcome_preserved`, `resume_deterministic`, `delivery_advances_generation`. A resumed segment that
diverges, refuses, yields a malformed Plan or ends unextractably commits `faulted` and returns unused
escrow, never refusing the turn (`resumedSegment_never_refuses_program_fault`, `:1270`). Abandonment after
deadline + grace (`abandon_returns_escrow`, `:3342`). Fees on declared envelopes only.

**Checkpoints.** At a yield the Plan is extracted by budgeted deep materialization, which **forces** cells
the Plan reaches; the stored checkpoint is `collect (settle forced)` of the extraction's state
(`ObjectiveBendDemandCollect.checkpoint`), encoded as tokens (`state_roundTrip`). Typed across every
reachable snapshot: `stored_checkpoints_typed` (`Kernel/ObjectiveCheckpointInvariant.lean:893`).

**Checkpoint transparency is an open premise.** `runSegment_stored_complete`
(`Kernel/ObjectiveResumeContract.lean:318`): resuming the stored checkpoint ends every segment as resuming
the machine's own yield would, *given* `ForcingTransparent` (`:309`):

```lean
def ForcingTransparent (config : Config) (yielded forced : State) (response : Term) (ticks : Nat) : Prop :=
  ∀ (s0 t0 : State) (segment : Segment), resume response yielded = some s0 → resume response forced = some t0 →
    runSegment config ticks s0 = .ok segment →
    ∃ segment', runSegment (headroom config forced) ticks t0 = .ok segment' ∧ Segment.Agrees segment segment'
```

It has a satisfying instance (`forcingTransparent_tally`) and refuting ones; **as stated it is false of a
dangling yield-stack address** (`not_forcingTransparent_dangling`, `:644`), and it does not follow from a
successful extraction (`forcingTransparent_not_of_extraction`, `:664`). The root approved strengthening it
with a premise `LexicalInvariant yielded` (MERGE-QUEUE.md line 183); DEPUTY-KERNEL item 1 is finishing it
("a stuttering simulation up to a growing address correspondence", docstring `:300-306`). Forcing can make
a checkpoint *larger* (`largerYield_checkpoint_grows`), hence the heap `headroom`. Executed evidence:
`scripts/check-objective-proofs.sh transparency` (both resumptions compared on every cohort activity).

**No guardedness.** Nothing guarantees that a well-typed resident's pure segment terminates
(`docs/OBJECTIVE-BEND.md:374-377, 621`). Divergence is caught operationally (ticks → exhaustion, a paid turn;
at the turn cap → `faulted`).

## 2. What it commits us to

1. **One-shot, host-driven, first-order effects.** Plans and responses are first-order data; there is no
   handler in the language that can intercept a perform (the host is the only handler). This is deliberately
   weaker than algebraic effects: no multi-shot, no user handlers, no effect polymorphism.
2. **Call-by-need is only safe because effects are kept out of thunks.** The refusal of `perform` under an
   update frame plus "activity types are never shareable" is the whole argument that call-by-name (the
   reference semantics) and call-by-need (the machine) agree in the presence of effects.
3. **A checkpoint is a whole machine state** (heap + control + stack), not a replay log. Rejected
   alternative: event-sourcing replay (Temporal/Durable Functions; root resolution C2 dropped REPLAY as an
   upgrade disposition "needs a full interaction log Mini does not keep",
   `ROOT-PROGRAM-MODEL-DECISIONS-20261004.md:138`; C3 at `:140`). Consequence: the checkpoint *format* is part of the
   semantics, and upgrading the machine invalidates checkpoints (root C3: "a Core4 or codec epoch change is
   always a re-genesis").
4. **Resume-with-view** chooses freshness over isolation: the activity sees the current state, not a
   snapshot from its yield, and its write applies to that view. Any invariant the activity "remembers" in
   its continuation can be invalidated by another writer between turns; the law is the only guard.
5. **Liveness** comes from mandatory deadlines + `faulted` + `abandon`, not from any progress guarantee of
   the program.

## 3. Literature (LIT-W2 §B, §C, §E; LIT-W3 §6–§7; quotes and pages there)

- **Name vs need with effects.** Launchbury 1993 ("A Natural Semantics for Lazy Evaluation", POPL;
  correctness/adequacy as restated and machine-checked by Breitner 2017, "The Adequacy of Launchbury's
  Natural Semantics for Lazy Evaluation", JFP) and Chang & Felleisen 2012 ("The Call-by-need Lambda Calculus,
  Revisited", ESOP, Thm 4) give name = need on **effect-free** ground observations. READ. McDermott & Mycroft,
  "Call-by-need effects via coeffects" §1–2: "In call-by-need, using one variable can change the effect of
  another" — name re-runs an effect at each use, need at the first. READ. So our machine/reference agreement
  holds only because effects never reach a shared cell. Breitner also found Launchbury's own generalized
  correctness theorem **false as stated** (§2.3.3) — the failure was in which heaps/environments it
  quantified over. READ.
- **Where the line goes.** Levy 2006, "Call-By-Push-Value", HOSC 19, §3: "a value is, whereas a computation
  does"; identifiers bind only values; effects are computation-level; no memoisation of computations. READ.
  Peyton Jones 2001, "Tackling the Awkward Squad" §2.6: `unsafePerformIO` is exactly an effect run by forcing
  a shared thunk, left as an unchecked proof obligation. READ. **Our code already puts the line in types**
  (every allocation rule refuses a computation type, `effect_as_argument_refused` and siblings), so the
  runtime `sharedEffect` refusal is defence in depth, as CBPV would recommend (W2 assumed it was the
  contract; it is not — checked programs never reach it, `checked_reachable_no_refusal`). What remains of
  W2's point is a **design choice we made stricter than CBPV and Haskell**: both let a *suspended*
  computation (`U (F A)`, `IO a`) be a storable, duplicable value whose *running* is the unshareable act;
  Objective Bend forbids storing an activity at all.
- **Guardedness.** Nakano 2000 ("A Modality for Recursion", LICS §1) — its motivating example is a
  self-referential object specification with a binary method. Atkey & McBride 2013 ("Productive Coprogramming
  with Guarded Recursion", ICFP §1): `fix : (▷A → A) → A`; syntactic guardedness checks are
  non-compositional, with a higher-order counter-example — `mix` is higher-order in exactly that sense.
  Abel & Pientka (JFP, "Wellfounded Recursion with Copatterns and Sized Types" §1): with copatterns,
  productivity is termination of each projection. Xia et al. 2020 ("Interaction Trees", POPL §2):
  `perform`/resume is `Vis plan k`; a turn is `Tau* (Vis | Ret)`. READ. Upshot: cross-turn recursion under
  `perform` is productive by construction; the open obligation is termination of each within-turn segment,
  and a type-directed discipline (`self : ▷Self`) would **reject** `{good = 7, bad = self.bad}`, which our
  laziness deliberately accepts. That is a real fork: total vs partial-lazy.
- **Durable execution.** Khan 2026, "Resume Means Resume" (arXiv 2608.03836v3) §3–4: PC, EO, FD, CV,
  CO-c/CO-e, RD, FI, liveness `EventuallyCompletes`; Lemma 1 (FD and CO jointly unsatisfiable without a wire
  discriminator); measured 2,628 effect fires where 400 were expected; only a claim at the **read/decide**
  path worked. READ (W2, W3). Our await nullifier is CO-c + CO-e; `faulted` is the liveness fix.
  **Resume-with-view deliberately violates PC** ("Recovery continues from the durably recorded frontier
  state"): control and heap continue from the checkpoint, object state comes from the view. Burckhardt et al.
  2021 ("Durable Functions: Semantics for Stateful Serverless", OOPSLA, Thm 6.4, Lemma 6.5): replay and
  stored-state models are **bisimilar given a deterministic step**; DF replays because host-language state is
  not serializable, and it never shows a fresh read after replay — so neither Khan nor DF is a precedent for
  resume-with-view. READ.
- **Serialized continuations.** Termite Scheme (Germain, Feeley, Monnier 2006 §3.1, §5): closures with a
  non-serializable referent cannot be serialized (our effect rule seen from the other end); deserialization
  requires "the same compiled code". Pettyjohn et al. 2005 ("Continuations from Generalized Stack
  Inspection", ICFP §3.5) bind serialized continuations to a digest of the program text. READ. **No paper W2
  read proves a heap-serialising round trip transparent for a lazy machine with sharing**; Kali Scheme
  (Cejtin, Jagannathan, Kelsey 1995) was not obtained.
- **IC awaits** (DFINITY "message execution properties" 2, 4, 5, 8, 9; LIT-W3 §6): every await is a commit
  point; the IC's bug class is TOCTOU across awaits, remedied by a journal-as-lock. Our resume-with-view
  gives freshness, not isolation (REVIEW-SCHOLAR-CALLS §2.3 said so first).

**Code facts the literature made us check.**
- **No theorem ties a machine yield to the reference semantics' `Yields`.** `Yields` appears only in
  `Theory/ObjectiveBendOpenRecursion.lean`; a grep of `Theory/` for yield/plan theorems finds typing
  (`typed_yieldedPlanWith`, `Theory/ObjectiveBendDemandForceProofs.lean:371`), control shape and
  `perform_yields`, but no statement that the Plan the machine extracts is the Plan the reference reaches
  (READ by grep; absence INFERRED from it). The adequacy theorems cover finished runs. So for activities,
  which are the kernel's whole business, the reference semantics is currently decorative.
- **Stale values in the continuation.** The kernel applies edits to the fresh view (`resume_view_current`),
  but a `set v` whose `v` was computed before the yield and kept in the checkpoint heap is not prevented:
  `moved_state_refuses` (`Kernel/ObjectiveActivity.lean:2725`) is a compare-and-swap within the delivering
  turn, not a dataflow rule. "No write is computed from a stale read" is true of the kernel's edit
  application, not of the program's values.

## 4. Questions for GPT-6

- **Q4-1 (sharp).** *What must `ForcingTransparent` state, and against what?* W2's six conditions from
  Burckhardt, Pettyjohn, Termite, ITrees and Khan: (a) weak bisimulation on the (Plan, response) trace and
  outcome, not state equality; (b) deterministic step with no hidden inputs (heap addresses, GC timing);
  (c) "settled" (no update frame, no blackholed cell at a yield) as a stated invariant — we have it as
  `typed_yield_quiescent`; (d) serialize-after-GC is a heap isomorphism preserving sharing and cycles,
  `fix`'s self-pointing cell as the test; (e) code/machine digest in the checkpoint, refuse on mismatch;
  (f) the comparison machine must itself read the view at resume. Ours is a per-segment `Segment.Agrees`
  between two `runSegment`s, already shown false without a lexical premise. Is a per-segment agreement the
  right shape, or should the theorem be the trace bisimulation, and does (f) change what the premise is?
- **Q4-2.** The reference semantics has `Yields`; the machine has `yielded`; nothing connects them. Should
  the next adequacy theorem be "the machine's extracted Plan and continuation are the reference's `Yields`
  plan and context" (a Launchbury-style correctness for interaction trees), and is that the right place to
  hang `ForcingTransparent` instead of a machine-to-machine comparison?
- **Q4-3.** Activities are not storable values (stricter than CBPV's `U (F A)` and Haskell's `IO a`). Is that
  the right call for a persistent object language (it makes checkpoints serializable and nullifiers
  per-await), or does it block patterns we will want (a stored retry plan, a queue of pending actions)? If we
  ever allow it, each force is a new perform: what is the nullifier then?
- **Q4-4.** Guardedness: total (type-directed `▷`, rejects `bad = self.bad`) or partial-lazy (accept, fuel
  bounds each segment, out-of-fuel is a paid `exhaust` and at the turn cap `faulted`)? If partial, is
  "ticks are a protocol constant and exhaustion is a committed paid turn" a complete answer to Khan's
  liveness obligation, given that weak fairness needs *someone* paid to run `deliver`/`abandon`?
- **Q4-5.** Resume-with-view violates Khan's PC on purpose. What is the right named property in its place
  ("control continues from the checkpoint; declared state from the view") and does it need a dataflow rule
  (values read before a yield may not flow into a post-resume `set`) to deserve the name "no write from a
  stale read"?
