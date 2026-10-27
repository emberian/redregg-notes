# SPEC — continuation (written by SPEC-4 at parking, 2026-10-27; supersedes SPEC-3's)

Read first: METHOD-20261027.md (reason first, build once, no `.lake` copies, no sub-forks) and
WORK-RULES-20261027.md; nanodregg `Spec/README.md` (claims table + the apex table), `decisions/spec.md`
SPEC-19..24, `Spec/Proofs/Apex.lean` WHOLE (the three contracts are trusted reading), CRIT-SPEC-2.md,
this file, SPEC.report.md's SPEC-4 section.

## Where things are
- hbox worktree ~/nd-land/spec4 (detached; the stack landed from it). ~/nd-land/spec4-wire was the
  wiring fork's (finished; do not reuse). Scratch ~/nd-land/spec4-scratch (logs, pids, msg files,
  AllSpec.lean, spec-mods.txt; `.lake/gates/SpecCensus.lean` in spec4 runs the axiom census over Spec).
- Mac staging: SPEC-4 scratchpad nd4/ (a clone; stale after landing).
- Checks before any Spec landing: `lake build Spec` (or nd-check), the import-all file, the Spec axiom
  census (`lake env lean .lake/gates/SpecCensus.lean` — every native_decide fact needs an allow row AND a
  tcb.tsv row, consumers included; `python3 gates/tcb.py .`).

## SPEC-4's work: c0c59794 (the gates rows) LANDED; the rest is READY at ~/nd-land/spec4 HEAD 1ecee406
(1596d980 wiring + 1ecee406 apex) and NOT on main: land it first with `ND_RUN_DEADLINE=2400 scripts/commit`
from ~/nd-land/spec4 (its reds were rows' lang-journey 300 s deadline under load and launcher certify,
which looks like PROTOCOL-84's own red; see the report). Contents:
- SPEC-21 wiring: `Spec/Assembly.lean`; `host`/`resident` mains run `deployed storeDigest`'s fields;
  System field `start`; Host.Wiring / Hosting.Resident.Wiring.
- gates rows: the 24 native_decide census reds (4 deployed-run witnesses, 3 floor facts, consumers).
- SPEC-22 `Apex.lean`: IntentContract / TransitionContract / ViewContract over a member-process model
  (Input/MStep/Run/Issued); proved: top_transition, apex_view_start, apex_intent_signs,
  apex_intent_okNow, components; owed: IntentObligation, ViewObligation, Transition's 5 undefined clauses.
- SPEC-23 ReceiptTruth over named invariants (JournalOk, RefusalsOk, u64 height); Foreign from any base.
- SPEC-24 the independent boundary analysis.

## Owed, in order
1. Statement 3 (3b): the loop's behind comparison (`Host.Follow.behindOr`) into the System (a field, its
   deployed value the pure core over the Store's chain lookup) so `MStep`'s reply is the deployed one;
   explicit "unavailable" instead of silent acceptance when the Store cannot say.
2. Statement 1: follow binds continuations to intents (§11.2: refuse a `kb` it never issued) — makes
   (1a)/(1b) provable without `Faithful`; then (1b)'s every-later-World half from A1 + fold_journal_turn.
3. Statement 2: define the five clauses (births, exact effects, issuance, caps per step, contextual law
   meaning within a budget) from observations; replace `Dispatched` in `Authorized` (SPEC-24).
4. Statement 3 (3c): a head package that records the source World's authority; `Foreign.check` verifies
   a certificate under it; `noHeadAuthority` becomes that field.
5. SPEC-21 (c): the reopen's fold step from the record (cheap: openWith takes it); the kernel as a record
   of primitives (priced in SPEC-21); an `attempt` field emitted from the Assembly for the Rust client.
6. Older owed list (SPEC-3's): B3's ObjectHistory bound to the log over S.receive/S.admit; per-arm B1
   floors; RETIRE-2; KERNEL DecidedBy hunk; AuthKernel lemma to Kernel.

## Hazards (new)
- A contract with a ghost label the System cannot see is unsatisfiable by any System of the type:
  state intents by continuation lineage (`Issued`), not by a label follow never receives.
- A contract parameter quantified ∀ or ∃ (a relation T, a trust function) is either unmeetable or vacuous;
  fix it as a declaration (`noHeadAuthority`) or a System field.
- rows' per-ROW 300 s liveness deadline (Protocol/Rows/Run.lean rowDeadlineMs) reds landings under box
  load; ND_RUN_DEADLINE (gates/runs.py) does not reach it.
