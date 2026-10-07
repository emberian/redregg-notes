# 00 — GPT-6's LTUO audit (2026-10-05) and what we did about it

**Source of the audit.** GPT-6's review, pasted by Ember into the root session ce776c01 on 2026-10-05
00:23 UTC (message 1743 of `cv show ce776c01 --json`). Saved verbatim:
`work/grounding/sources/gpt6-ltuo-audit-20261005.txt`. It was a source-level audit pinned at minidregg
`259a2fb`; GPT-6 states it did not rebuild or execute anything. Our row-by-row digest of it is
`work/OB-LTUO-20261005.md` (rows LT0–LT6).

**State of our code for this file.** GitHub main `4ef4e808` (2026-10-05 11:07 -0400), fresh clone, read only.
The 10-05 Faré-calculus review that followed (`work/OB-FAREOO-REVIEW-20261005.md`, fixes D1–D5) is on
`lane/ob-review` and is **not on main** (its full gate was waiting for an hbox slot, per that file's last
section). Anything below marked "lane" is not on main.

## What GPT-6 said, in seven claims

| # | GPT-6's claim (audit section) | Kind |
| --- | --- | --- |
| G1 | The kernel is right: one final self, whole super, a real knot, lazy records. "I would preserve this kernel." (§2) | Endorsement |
| G2 | `spec S for T` typed both `self` and `super` as the whole `T` (`T → T → T`): Faré's §8.2.1 "Trivial Non-Modular Types", not modular typing. A one-method spec needed a whole-`T` seed. (§3) | Defect |
| G3 | Core type variables (rigid vars, bounds, row tails) are not an authored binder; recursive records refused ("requires explicit future-row binder"). `binary_method_changes_with_future_self` is a fact about substitution, not about programs. (§3) | Defect |
| G4 | `Specification<T>` is not closed under `compose`: metadata was part of the exact type, `{name, interface, laws}` vs `{operator, inherited, wrapping}`. Predicted `def twice(e) -> Specification<Nat>: compose(e, e)` is refused. (§4) | Defect (API) |
| G5 | `prototype(spec, target)` is a raw pair with no provenance; R(Y M) vs Y(R∘M) undecided; compose is associative for behaviour but not for reflection; observers must be listed; resource observations are separate. (§5) | Under-specification |
| G6 | "Source semantics" in our theorems means Core4's reference semantics, not `.obend`; a compiler that swaps two layers would still pass every theorem. C4's `OrderedPresentationInvariant` is unproved and, even proved, "refuse everything" satisfies renaming invariance. (§6) | Proof boundary |
| G7 | `law` is retained Boolean code, not a promise (`law impossible: false` accepted); guarding resident self-calls under `perform` does not bound a turn's pure segment. (§6) | Under-specification |

## What we did (status at main 4ef4e808 unless marked)

| Row | Response | Evidence | Status |
| --- | --- | --- | --- |
| LT0 | GPT-6's 11 probes rebuilt as a gated cohort, now 27 rows: `tests/objective-bend-source/ltuo/probe-cohort.json`, gate row `ltuo-probes` in `scripts/check-objective-frontend.sh`. | Read the cohort: 26 of 27 rows at target. The one red is **W08-LawImpossible** (current `finished 41`, target `refused (law-refuted)`). | DONE except W08 |
| LT1 (G4) | `Specification<T>` = `specification(SpecMeta, Extension<T>)`, with `SpecMeta`/`SpecLaws` built-in first-order sums; laws, ancestry and composition change the metadata *value*, never the type. | `Compiler/ObjectiveBendSpecificationClosure.lean:44` `composeTy_closed`; `:184` `twice_accepted`; `:192` `law_spec_accepted`. Probes W01, W02, W03 at target. Design reason: `docs/objective-bend/REFLECTION.md` "Why a uniform first-order representation". | DONE |
| LT2 (G2, G3) | Authored modular typing by **templates**: `X[Self has {…}, Super has {…}]`, `Super with {…}`, `requires` as the Self bound (checked), `fix` discharges bottom-up from the seed, rigid `Self`, recursive records nominal, F-bounds. | `docs/objective-bend/MODULAR-TYPING.md` D1–D6; `Theory/ObjectiveBendTemplates.lean:88` `canonical_instantiate`, `:392` `Discharges.infer_instantiate`, `:1033` `Discharges.check_instantiate`, `:1155` `self_as_bound_row_rigid_refused`. Probes W04, W05, W06, W06b, W07, W09b, W10, S3a–d, S4a at target. | DONE for plain chains. OPEN: `instance_accepted` (instances are re-elaborated, not substituted); ancestry specs and non-plain operands keep the whole-target rule; cross-package instances. |
| LT3 (G6) | Not started. The overview says so (`docs/OBJECTIVE-BEND.md:609-614`). | `Compiler/ObjectiveBendC4.lean:150` `OrderedPresentationInvariant` is a `def … : Prop`, unproved; evidence is compiled vectors (`Compiler/ObjectiveBendC4Vectors.lean`). | OPEN |
| LT4 (G5) | The reflection contract was written: observers listed, two equivalences (≈b, ≈r), associativity fails for ≈r and the probes R01/R02 show a program telling the associations apart. | `docs/objective-bend/REFLECTION.md` (whole file). `composition_associative` is on the separate list model (`Theory/ObjectiveBendExtensions.lean:76`), not on `Term.mix`. | PARTLY: contract written; provenance constructor, R(Y M) vs Y(R∘M), resource theorems all OPEN |
| LT5 | Not started (no surface form names another package's root). | `docs/OBJECTIVE-BEND.md:101-102`. | OPEN |
| LT6 (G7) | Not started. `law` status is always `unchecked`; `TotalProof law := law` (`Theory/ObjectiveBendTyping.lean:637`) is a renaming, not a proof. No guardedness check. | `docs/OBJECTIVE-BEND.md:545-559, 603, 621`. | OPEN |

**After GPT-6 (10-05, lane only).** Our own reading of LTUO §9.2 against the elaborator found five
defects the audit did not examine, all in method combination (`OB-FAREOO-REVIEW-20261005.md` D1–D5):
`combine and` was strict (D1); `compose` erased combined contributions (D2); a combined method could read
`super` and double-count (D3); the interface label carried source spans, so moving code changed what a
program computes (D4, a violation of LTUO §7.3.5.7 shape determinism); open specs silently dropped
qualifiers (D5). Each fix has a planted fault turning exactly its probe red. **Not on main.** Main's
overview still says `combine and` and documents `&&` as strict (`docs/OBJECTIVE-BEND.md:110-111, 201`).

## Things GPT-6 got slightly wrong, or that changed under it

- GPT-6 cites the review example's seed "with identity implementations of both methods". At main the seed
  is `{}` (`docs/OBJECTIVE-BEND.md:164,172-173`): that is what LT2 delivered.
- GPT-6's argument-order remark (Faré inherited-first, OB self-first) is right and harmless; the
  10-05 review records it as deviation V1. What GPT-6 did not flag: `compose(a, b, c)` is least-specific
  first (rightmost wins) while `extends A, B` is most-specific first (A wins), and no reason is written
  down for the mismatch (OB-FAREOO-REVIEW V2; task 01a10afe-eda1).
- **Our own doc mis-cites the book.** `docs/OBJECTIVE-BEND.md:656-657` lists "ltuo" as *Rideau, Knauth and
  Amin, The Land of the Ultimate Object*. The mirror's title page reads *Lambda: The Ultimate Object —
  Object Orientation Elucidated*, a single-author draft by François-René Rideau
  (`~/dev/fareoo/raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt:1-4`; `~/dev/fareoo/sources/ltuo-book.md:1-6`).
  Rideau, Knauth and Amin are the authors of *Prototypes: Object-Orientation, Functionally* (Scheme
  Workshop 2021; `~/dev/fareoo/sources/poof-paper.md:1-12`). A one-line doc fix; flagged to the root.

## What to ask GPT-6 about its own audit

1. Its priority 2 ("expose genuine modular typing") was met by **second-class templates**. LTUO §8.4.3.1
   says first-class types cannot be deduced from second-class ones. Does GPT-6 consider LT2 met, or is a
   first-class open extension (a parameter of type "any extension over `Self has {x}`") the actual bar?
   (Topic 02, Q-A.)
2. Its §4 recommended deciding the metadata representation "not blindly". We chose uniform first-order
   data over an existential. Is there an observer we now expose that it would not have? (Topic 03.)
3. Its §6 C4 proof package: which properties, exactly, are enough to make `OrderedPresentationInvariant`
   plus them a *specification* of C4 rather than a property "refuse everything" also has? (Topic 01.)
