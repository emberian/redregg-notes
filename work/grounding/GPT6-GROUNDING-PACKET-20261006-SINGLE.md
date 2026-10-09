# Objective Bend / Mini — grounding packet for GPT-6 (single file, 2026-10-06)

**How to read this.** Code references (`File.lean:line`, theorem names, `docs/...`, `Kernel/...`, `scripts/...`) are to the PUBLIC
repository **github.com/emberian/minidregg** at commit **4ef4e808** (main as of this packet; later commits up to 28f3b84d add proofs
but no semantic change). Paths beginning `work/`, `designs/` or `resume/` refer to private planning notes; everything from them that
this packet relies on is INLINED in the appendices below. Faré's "Lambda: the Ultimate Object" (LTUO) sources are not attached; cite
by chapter/section. Tags used throughout: [read] = read in code or source; [report] = from an earlier agent report; [inferred].
`work/OB-FAREOO-REVIEW-20261005.md` is referenced in places but was never produced (the scheduled review was interrupted); ignore it.

Structure: Part I = index + ranked questions; Part II = topics 00-08; Appendix A = the Objective Bend completion/LTUO work rows;
Appendix B = literature notes (three workers); Appendix C = your (GPT-6's) earlier LTUO audit, verbatim.


# Part I — Index and ranked questions


---

## Index and executive summary

<!-- source: GPT6-GROUNDING-20261006.md -->

## GPT-6 grounding packet — Objective Bend's design commitments against the literature (2026-10-06)

**What this is.** The packet Ember takes to GPT-6 before the Mini swarm goes further on Objective Bend's
*meaning*. For each design commitment: the current design (cited to code or theorem on GitHub main), what it
commits us to, what the literature says, and the questions where we are least sure. Built by DEPUTY-GROUNDING
with three literature workers. No builds were run; nothing in the repository was changed.

**Ground truth.** minidregg GitHub main **`4ef4e808`** (2026-10-05 11:07 -0400), fresh clone, read only. Every
code claim cites `file:line` or a theorem name at that commit. The 10-05 method-combination fixes
(OB-FAREOO-REVIEW D1–D5) are on `lane/ob-review` and **not on main**; files say so where it matters.

**Evidence tags used throughout.** **READ** = read at the cited place (by me or a worker, named).
**VIA-SCHOLAR** = taken from an earlier scholar report, not re-verified. **INFERRED** = reasoning, memory, or a
conclusion from an absence (a grep that found nothing). Literature citations give author, year, title, venue
and section; quotes and page/line numbers are in the worker notes.

### Files

| File | Commitment |
| --- | --- |
| [00-GPT6-LTUO-AUDIT-AND-RESPONSE.md](00-GPT6-LTUO-AUDIT-AND-RESPONSE.md) | GPT-6's 10-05 LTUO audit (seven claims) and what we did, row by row (LT0–LT6), with status at main |
| [01-open-recursion-core4.md](01-open-recursion-core4.md) | Open recursion with lazy cells; `mix`/`fix`; C4 ancestry; method combination; Core4 primitives incl. the held `digest` |
| [02-modular-typing.md](02-modular-typing.md) | Templates + rigid `Self`; F-bounds; `requires`; `fix` discharge; no subtyping |
| [03-specification-and-reflection.md](03-specification-and-reflection.md) | `Specification<T>`, `SpecMeta`, observers, `≈b`/`≈r`, prototypes, R(Y M) vs Y(R∘M) |
| [04-activities-resume-checkpoints.md](04-activities-resume-checkpoints.md) | Activities, answer slots, resume-with-view, the resume contract, checkpoint transparency, guardedness |
| [05-call-and-send.md](05-call-and-send.md) | `call` (deferred writes, re-entry refusal, scoped grants); `send` (inboxes, postage, forwarding); OB-ENG's held items |
| [06-laws-and-seats.md](06-laws-and-seats.md) | Laws as decidable predicates; offer safety and seats; seat contracts and principal identity |
| [07-admission-by-reexecution.md](07-admission-by-reexecution.md) | Native admission by front-end replay and deterministic re-execution; fees on declared envelopes |
| `lit/LIT-W1-oo-calculus-typing.md` | Worker W1 (Sonnet): Cook, Bracha–Cook, F-bounded, Abadi–Cardelli, Wand, Rémy, Pierce–Turner, Bruce, Odersky–Zenger, MixedJava/MixML/Hirschowitz–Leroy, C3 |
| `lit/LIT-W2-laziness-reflection-continuations.md` | Worker W2 (Sonnet): Launchbury/Breitner, Chang–Felleisen, CBPV, awkward squad, McDermott–Mycroft, Nakano, Atkey–McBride, Abel–Pientka, ITrees, Wand fexprs, Felleisen, Smith, AMOP, Khan, Durable Functions, Termite, Pettyjohn |
| `lit/LIT-W3-calls-sends-contracts.md` | Worker W3 (Sonnet): Miller thesis + TGC, CapTP/Cap'n Proto, Zoe, Daml, Soroban, Pact, SeRIF, ECF, Aptos, IC, NEAR, EIP-150, Khan, Durable Functions, Block-STM, CALM, eUTxO; **11 corrections to earlier scholar reports** |
| `sources/gpt6-ltuo-audit-20261005.txt` | GPT-6's 10-05 audit, verbatim (from root session ce776c01, message 1743) |

PDFs and text extractions: `~/paperbin/objective-bend-grounding/` (new, ~80 files) and
`~/paperbin/world-program-model/` (pre-existing). Not obtained: Abadi–Cardelli *A Theory of Objects* (the book;
their 1995 paper and 1996 tutorial were read instead), Sestoft 1997, Ariola et al. 1995 (read via Chang–Felleisen
2012), Mitchell 1993, Kali Scheme 1995.

### Executive summary

1. **The kernel survives the literature.** Core4's `mix`/`fix` is Cook's wrapper semantics with the `⊕` moved
   inside the extension, so `mix` is associative on the nose (Cook & Palsberg 1989; W1 §1). Templates with a
   rigid lower-bounded `Self` are, almost word for word, Cook–Hill–Canning's POPL '90 §3.2 design ("the type
   recursion is reintroduced when the object is constructed", `Y(P[σ])`), with Bruce's MyType-matching
   soundness conditions; Objective ML made the same second-class choice. Wand's non-principality of record
   concatenation is a positive argument for instantiation over polymorphic core terms. GPT-6's 10-05 verdict
   ("preserve this kernel") stands.

2. **The weakest joints are where the calculus meets the kernel, not inside the calculus.**
   - Activities are the kernel's whole business, yet **no theorem ties a machine yield to the reference
     semantics' `Yields`**: the adequacy theorems cover finished runs only (grep of `Theory/`; topic 04).
   - `ForcingTransparent` is a machine-to-machine comparison that is false as stated, by our own
     counterexample (`not_forcingTransparent_dangling`, `Kernel/ObjectiveResumeContract.lean:644`). The
     durable-execution literature proves transparency as a trace bisimulation resting on determinism
     (Burckhardt et al. 2021, Thm 6.4). No paper read proves a heap-serializing round trip transparent for a
     lazy machine.
   - Resume-with-view deliberately violates Khan's prefix-continuation property. Nothing stops a value read
     before a yield, held in the checkpoint heap, from flowing into a post-resume `set`.

3. **Per-object guards are the literature's known blind spot.** Laws judge one object's (old, new, request),
   and re-entry is refused per object. SeRIF (Cecchetti et al. 2021, Fig 4c), Aptos Move's own auditors
   (Dedaub 2025) and eUTxO's whole-transaction validators all point at the same hole: an invariant split
   across mutually trusting objects (A → B → C) is judged by no law. W3 also argues the re-entry refusal is
   "belt over braces" given snapshot views and deferred writes. Our DAO mutant plant says the guard is
   load-bearing. **That conflict needs settling.**

4. **Authority is caller-delegated, and the grant does not bind arguments.** Daml's nested authority is
   callee-declared consent (signatories); ours is the signer's scoped grant `{object, method, uses}`. Both
   production grant systems read, Soroban and Pact, bind arguments: Soroban to an invocation tree with a
   nonce and an expiry, Pact as capability parameters with managed quantities. Ours does not, so any object
   mid-tree can spend the grant with its own arguments: a confused-deputy exposure.

5. **Typing is honest but second-class, and the front-end corollary is missing.** Faré (LTUO §8.4.3.1) says
   first-class types cannot be recovered from second-class ones; Bruce §18.1 prices dropping subtyping (hash
   types). `instance_accepted` is unstated, and `provided-mismatch` is decided at instantiation, so "checked
   once" is weaker than it reads (topic 02).

6. **The front end is trusted and partly unmetered.** Admission replays it byte-for-byte, and the replay is
   priced only through the checker's `typeFuel`. Parse, elaboration, C4 and template instantiation have no
   stated bound beyond the policy's source size (topic 07). The surface semantics (LT3) is unstarted, so
   admission guarantees the compiler's output, not the author's meaning.

7. **Reflection behaves as Wand predicts.** `composed{inherited, wrapping}` is injective on construction
   trees. Under `metadata`, equivalence of composed specs is therefore tree equality, and non-associativity
   is forced, not incidental (Wand 1998; Felleisen 1991 Thm 3.14). Programs can branch on `metadata`, which
   is intercession by the back door (topic 03).

8. **Smaller real defects found while grounding** (reported to the root; none fixed here):
   - `docs/OBJECTIVE-BEND.md:656-657` cites "ltuo" as *Rideau, Knauth and Amin, The Land of the Ultimate
     Object*. The book is *Lambda: The Ultimate Object — Object Orientation Elucidated*, a single-author draft
     by Rideau. Knauth and Amin co-wrote POOF (topic 00).
   - Seats: an empty `want` makes every reallocation offer-safe (`Kernel/Seat.lean:84-86`). REVIEW-SCHOLAR-LAWS
     D-5 is still unaddressed on main (topic 06).
   - Eleven mis-citations in the 10-04/10-05 scholar reports (LIT-W3 "Corrections"). The notable ones:
     - REVIEW-SCHOLAR-CALLS's "correction" of the Grossman figure is itself backwards. The paper says "10 of
       ~100M legitimately **non-ECF**". The cost of a blanket refusal is the `Callbacks` column, 0.16% then
       1.0% of executions.
     - The OCapN "ordering bug" is in neither OCapN file.
     - Tezos is not a synchronous-call precedent; it runs internal operations after the caller finishes.

### The sharpest questions, ranked

Ranked by (how unsure we are) × (how much is built on the answer). Each links to its topic file, which has the
full question and its citations.

1. **Where does a cross-object invariant live, and is per-object re-entry refusal the right guard?**
   ([Q5-1](05-call-and-send.md), [Q6-4](06-laws-and-seats.md))
   - Options:
     - (a) The object model declares that invariants live in one object, enforced by a publish-time lint.
     - (b) Laws see sibling frames' writes, as eUTxO validators see the whole transaction.
     - (c) Trust-labelled re-entrancy, as in SeRIF.
   - Also: is the refusal load-bearing once views are snapshots and writes are deferred? W3 says no; our
     DAO plant says yes.
   - What Lean statement replaces "no object twice on the stack" as the theorem that matters?
2. **What is the reference meaning of an activity, and what must checkpoint transparency state?**
   ([Q4-1, Q4-2](04-activities-resume-checkpoints.md))
   - Should the next adequacy theorem relate the machine's yield (Plan + continuation) to the reference's
     `Yields`, as a correctness theorem for interaction trees?
   - Should `ForcingTransparent` be a trace bisimulation under a determinism premise (Burckhardt et al.),
     rather than a per-segment agreement between two machines?
   - Which of W2's six conditions are missing? Condition (f) matters most: the comparison machine must also
     read the view at resume.
3. **Is second-class modular typing enough, and what is the substitution lemma?**
   ([Q2-1, Q2-2, Q2-3](02-modular-typing.md))
   - Every typed precedent chose second-class mixins. Faré and GPT-6's own bar point at first-class ones.
   - Without subtyping, the first-class route is an existential over a matching bound (Bruce's hash types).
     Is there a route that adds no core `∃`?
   - What front-end theorem makes "checked once" true? Must `Super` become a second rigid variable carrying
     presence/absence information?
   - What is the type of `compose` of two open layers?
4. **Do scoped grants need to bind arguments, and should Mini have both consent and delegation?**
   ([Q5-2](05-call-and-send.md))
   - Soroban and Pact bind arguments and Daml uses callee-declared signatories; ours does neither.
   - What matching rule closes the confused-deputy exposure?
   - Is `request/subject` meant as consent or as delegation?
5. **What does admission guarantee a source author, and must elaboration be metered?**
   ([Q7-1, Q7-2](07-admission-by-reexecution.md), [Q1-1](01-open-recursion-core4.md))
   - The front end is trusted (LT3 unstarted), and its replay is priced only through `typeFuel`.
   - Which surface-semantics theorem is the minimum, starting from compose order and C4 ancestry?
   - Which properties *specify* C4, given that renaming invariance alone is satisfied by "refuse everything"?
6. **Is `SpecMeta` meant to be injective on construction trees, and may behaviour read metadata?**
   ([Q3-1, Q3-2, Q3-3](03-specification-and-reflection.md))
   - Wand's triviality applies if it is injective.
   - Should we state non-interference, and in which form?
   - Introspection only (R(Y M)), or `self` as the prototype (Y(R∘M))?
7. **Resume-with-view versus stale values in the continuation.** ([Q4-5](04-activities-resume-checkpoints.md))
   - What named property replaces Khan's prefix continuation?
   - Does "no write from a stale read" need a dataflow rule?
8. **Laws.** ([Q6-1, Q6-2](06-laws-and-seats.md), [Q3-4](03-specification-and-reflection.md))
   - Delete the unchecked spec `law` until it compiles to `Pred` or is discharged?
   - Where does a two-state, first-order, difference-logic judge stop being expressive enough?
9. **Send protocol and the items DEPUTY-OB-ENG held for this round.** ([Q5-4, Q5-5](05-call-and-send.md))
   - Who pays onward sends from a delivered message?
   - Awaiting a never-expiring reply slot, and how to avoid the IC's `SYS_UNKNOWN`.
   - The contagion rule for pipelining deeper than one level.
   - Forwarding order (Cap'n Proto's Disembargo) and datalock.
   - Who pays the reply leg.
10. **Forks of taste.**
    - The `compose` order flip ([Q1-2](01-open-recursion-core4.md)).
    - Total vs partial-lazy guardedness ([Q4-4](04-activities-resume-checkpoints.md)).
    - Storable activities ([Q4-3](04-activities-resume-checkpoints.md)).
    - The `digest` primitive's pricing and type ([Q1-5](01-open-recursion-core4.md)).
    - Whether seat contracts may learn principal identities ([Q6-5](06-laws-and-seats.md)).

### How to use this with GPT-6

- Send `00` first. It is GPT-6's own audit with our response, and it asks GPT-6 to say whether LT2 meets its
  bar.
- Then send the ranked questions with their topic files. Each topic file stands alone: design, commitments,
  literature, then questions.
- The worker notes in `lit/` carry the verbatim quotes, in case GPT-6 disputes a reading.
- Every code claim is pinned to `4ef4e808`. If main moves before the round, re-check the four "not on main"
  notes in topics 00, 01 and 03.

### Also in this packet: 08-swarm-work-lifecycle.md (Ember asked: how should work items move through the swarm?)

### Addendum (root, 10-06): a new finding for the transparency topic
ForcingTransparent is now proved on the DEPLOYED kernel (segment heap limits counted from the segment's own start; growth declared
and paid at delivery, refused `heapUncovered`; StoredComplete names the run's own retained yield; the absolute-limit version is
refuted in-kernel by `absolute_limits_refuted`). But the CONVERSE is false: a stored (forced, settled, collected) checkpoint can
COMMIT where the program's own lazy run is refused, by tick exhaustion or by a result-extraction budget fault, because cached
cells save ticks and plan budget. That the difference is "resources only" is unproved (cv 01a113f0-4ff6).
QUESTION for GPT-6: is a resource-monotone, one-directional simulation the right contract for checkpointed lazy execution
(cf. Launchbury's natural semantics, Sestoft's abstract machine, cost-semantics work on call-by-need), or should admission be defined
against a cost model in which forcing is free, making both directions equal? What do durable-execution systems (Temporal, Khan)
promise about replay costs?


# Part II — Topics


---

## 00-GPT6-LTUO-AUDIT-AND-RESPONSE

<!-- source: 00-GPT6-LTUO-AUDIT-AND-RESPONSE.md -->

## 00 — GPT-6's LTUO audit (2026-10-05) and what we did about it

**Source of the audit.** GPT-6's review, pasted by Ember into the root session ce776c01 on 2026-10-05
00:23 UTC (message 1743 of `cv show ce776c01 --json`). Saved verbatim:
`work/grounding/sources/gpt6-ltuo-audit-20261005.txt`. It was a source-level audit pinned at minidregg
`259a2fb`; GPT-6 states it did not rebuild or execute anything. Our row-by-row digest of it is
`work/OB-LTUO-20261005.md` (rows LT0–LT6).

**State of our code for this file.** GitHub main `4ef4e808` (2026-10-05 11:07 -0400), fresh clone, read only.
The 10-05 Faré-calculus review that followed (`work/OB-FAREOO-REVIEW-20261005.md`, fixes D1–D5) is on
`lane/ob-review` and is **not on main** (its full gate was waiting for an hbox slot, per that file's last
section). Anything below marked "lane" is not on main.

### What GPT-6 said, in seven claims

| # | GPT-6's claim (audit section) | Kind |
| --- | --- | --- |
| G1 | The kernel is right: one final self, whole super, a real knot, lazy records. "I would preserve this kernel." (§2) | Endorsement |
| G2 | `spec S for T` typed both `self` and `super` as the whole `T` (`T → T → T`): Faré's §8.2.1 "Trivial Non-Modular Types", not modular typing. A one-method spec needed a whole-`T` seed. (§3) | Defect |
| G3 | Core type variables (rigid vars, bounds, row tails) are not an authored binder; recursive records refused ("requires explicit future-row binder"). `binary_method_changes_with_future_self` is a fact about substitution, not about programs. (§3) | Defect |
| G4 | `Specification<T>` is not closed under `compose`: metadata was part of the exact type, `{name, interface, laws}` vs `{operator, inherited, wrapping}`. Predicted `def twice(e) -> Specification<Nat>: compose(e, e)` is refused. (§4) | Defect (API) |
| G5 | `prototype(spec, target)` is a raw pair with no provenance; R(Y M) vs Y(R∘M) undecided; compose is associative for behaviour but not for reflection; observers must be listed; resource observations are separate. (§5) | Under-specification |
| G6 | "Source semantics" in our theorems means Core4's reference semantics, not `.obend`; a compiler that swaps two layers would still pass every theorem. C4's `OrderedPresentationInvariant` is unproved and, even proved, "refuse everything" satisfies renaming invariance. (§6) | Proof boundary |
| G7 | `law` is retained Boolean code, not a promise (`law impossible: false` accepted); guarding resident self-calls under `perform` does not bound a turn's pure segment. (§6) | Under-specification |

### What we did (status at main 4ef4e808 unless marked)

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

### Things GPT-6 got slightly wrong, or that changed under it

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

### What to ask GPT-6 about its own audit

1. Its priority 2 ("expose genuine modular typing") was met by **second-class templates**. LTUO §8.4.3.1
   says first-class types cannot be deduced from second-class ones. Does GPT-6 consider LT2 met, or is a
   first-class open extension (a parameter of type "any extension over `Self has {x}`") the actual bar?
   (Topic 02, Q-A.)
2. Its §4 recommended deciding the metadata representation "not blindly". We chose uniform first-order
   data over an existential. Is there an observer we now expose that it would not have? (Topic 03.)
3. Its §6 C4 proof package: which properties, exactly, are enough to make `OrderedPresentationInvariant`
   plus them a *specification* of C4 rather than a property "refuse everything" also has? (Topic 01.)


---

## 01-open-recursion-core4

<!-- source: 01-open-recursion-core4.md -->

## 01 — Open recursion with lazy cells, C4 ancestry, method combination, Core4 primitives

Code: minidregg main `4ef4e808`, read only; the method-combination fixes D1–D5 are on `lane/ob-review`,
not main (`work/OB-FAREOO-REVIEW-20261005.md`). Book: Rideau, *Lambda: The Ultimate Object — Object
Orientation Elucidated* (draft, 2026; mirror `~/dev/fareoo/raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt`),
cited "LTUO §n". Classic OO literature: `lit/LIT-W1-oo-calculus-typing.md`; laziness:
`lit/LIT-W2-laziness-reflection-continuations.md` §A–B.

### 1. Current design

**The two rules** (`Theory/ObjectiveBendOpenRecursion.lean:250-252`, reference relation `Step`):

```lean
| mix (lower upper : Term) : Step (.mix lower upper) (mixBody lower upper)   -- λself.λsuper. upper self (lower self super)  (:150)
| fix (spec inherited : Term) :
    Step (.fix spec inherited) (.app (.app spec (.fix spec inherited)) inherited)
```

- The reference semantics is weak-head **call-by-name** (file docstring `:3`). The demand machine
  (`Theory/ObjectiveBendDemandMachine.lean`) is **call-by-need**: arguments and record fields are shared
  heap cells evaluated at most once; `fix` ties one address to itself (`:115`); re-entering a cell under
  evaluation is a `blackhole` (`:62, 101`), observed as divergence (`:218`).
- Records are records of separate suspensions, first match wins; `extend` overrides; `get` takes a static
  name only (no computed-name `get`) (`docs/OBJECTIVE-BEND.md:70-78`).
- Machine ↔ reference: `runBounded_observation_sound` (`Theory/ObjectiveBendDemandAdequacy.lean:3616`),
  `runBounded_resource_independent` (`:3636`), `machine_evaluation_complete`
  (`Theory/ObjectiveBendDemandCompleteness.lean:1115`; finite, with no resource bound),
  `typed_stepRaw_preserved`, `checked_reachable_no_refusal`. Divergence, blackholes, suspension remain.
- **The package is a specification**: every global is a field of one record knot, `fix(specification({package:
  …}, λ$globals λ$seed. extend $seed {M.decl: …}), {})` (`docs/OBJECTIVE-BEND.md:96-102`), so mutual recursion
  goes through the knot. No surface form names another package's root.

**Ancestry** (`Compiler/ObjectiveBendC4.lean`). `spec S extends A, B for T` is linearized by C4 (C3 plus the
suffix property, LTUO §7.4.4) **in the elaborator**; the extension is the `mix` chain of the ancestors'
layers; no new Core4 constructor. Identity = the qualified declaration key, so a diamond's shared ancestor
counts once while `compose(E, E)` applies `E` twice. Our 10-05 review found C4 a step-for-step port of
Faré's pommette `c4-linearize` (OB-FAREOO-REVIEW "Verdict"). **Unproved**: `OrderedPresentationInvariant`
(`Compiler/ObjectiveBendC4.lean:150`) is a `def … : Prop` that nothing proves; the evidence is compiled
vectors and 4000 seeded random DAGs (`Compiler/ObjectiveBendC4Vectors.lean`).

**Two orders.** `compose(a, b, c)` is least-specific first (rightmost wins, as Nix
`composeManyExtensions`); `extends A, B` and the precedence list are most-specific first (A wins). No reason
for the mismatch is written down (OB-FAREOO-REVIEW V2; task 01a10afe-eda1, "a taste fork for Ember").

**Method combination.** Qualifiers `def`, `suffix spec`, `around`, `combine +`, `combine *`, `combine and`
(`docs/OBJECTIVE-BEND.md:110-112`); `before`/`after` parsed and refused in pure code. On main, `combine and`
is strict and `compose` of combined specs erases contributions; the lane fixes make the **combination the
protocol's** (declared on the record, `record Doc: combine + weight() -> Nat`), short-circuit `and`/`or`,
forbid `super` in a combined body, strip source spans from the interface label, refuse qualifiers in open
specs (OB-FAREOO-REVIEW D1–D5, each with a planted fault turning exactly its probe red).

**Primitives.** `binary p l r`, strict left-to-right, one machine step each, `p ∈ {add, multiply, equal,
conjunction, labelEqual, subtract, divide, less, lessEqual, modulo}` (`docs/OBJECTIVE-BEND.md:70`);
naturals unbounded. No digest primitive (below, §4).

### 2. What it commits us to

1. **Laziness is semantic, not an optimization**: `{good = 7, bad = self.bad}.good` is 7. Any strict
   backend (C, circuit, FHE) must preserve call-by-name observations; a private backend must evaluate both
   arms and leak nothing through demand (`docs/OBJECTIVE-BEND.md:642-652`).
2. **Inheritance is computation, not declaration**: `mix` and `fix` are terms; specs are values. MI
   (C4) is resolved *statically* over declaration identities, so computed specs cannot take part in
   declared ancestry (LTUO §7.4.6 "prototypes with optimal inheritance" is first-class; ours is not — U6).
3. **Unbounded naturals with O(1)-tick primitives** make the tariff's tick count a poor proxy for work on
   large numbers (the reason for the size-aware meter discussion, §4 below).
4. **The package knot is the module system.** Separate compilation and cross-package extension (LT5) must
   come through it.

### 3. Literature (LIT-W1 §1–2, §10–11; LIT-W2 §A; quotes and pages there)

- **Cook 1989** (PhD thesis, Brown, "A Denotational Semantics of Inheritance", §2.5–2.6, §4.1–4.4) and
  **Cook & Palsberg 1989** (OOPSLA, §3.2): a class is a generator, a subclass a wrapper
  `self → super → delta`, applied by `W ⊛ G = λself. W(self)(G(self)) ⊕ G(self)`. READ. Core4's extension takes
  and returns the *whole* value, so `mix` is plain function composition and associative on the nose, with no
  hypothesis on `⊕` (INFERRED, W1 §1). Cook's "generalized inheritance" `M ∘ G ∘ P` lets the self passed to
  the parent be modified (renaming); Core4 passes one self to all layers, a deliberate narrowing.
- **Bracha & Cook 1990** ("Mixin-based Inheritance", OOPSLA/ECOOP §3.1, §4): `M1 ⋆ M2` gives priority to the
  **first** argument; "If a component is composed more than once it will appear as multiple copies"; §3.1
  criticises linearization for rewriting declared parent relationships. READ. Bracha–Cook `⋆`, Flatt et al.'s
  MixedJava `compose` (POPL 1998 §4) and Faré's own POOF `(mix c p)` are all **most-specific-first**; Core4's
  `compose` is least-specific-first while its `extends` is most-specific-first. READ (W1 §2). No source has
  both directions in one language.
- **Hirschowitz & Leroy 2002** ("Mixin Modules in a Call-by-Value Setting", ESOP §1, §3): composition of
  independently checked pieces can create ill-founded recursion "a posteriori … at a time where only the
  signatures of A and B are known"; "the sum of two safe graphs is not necessarily safe". READ. In Core4 such
  a cycle is a runtime blackhole, which our safety theorem explicitly permits
  (`checked_reachable_no_refusal`: "divergence, blackholes and suspension remain possible",
  `docs/OBJECTIVE-BEND.md:581`) — a conscious choice of the partial-lazy discipline over a dependency-graph check.
- **Dreyer & Rossberg 2008** ("Mixin' Up the ML Module System", ICFP): recursive linking by backpatching
  lazy reference cells — the package-as-record-knot is the same device. READ (W1 §10).
- **Launchbury 1993** anchors `fix` (native recursive `let`, a cell pointing to itself), whereas the
  Ariola–Felleisen call-by-need calculi exclude cyclic terms (Chang & Felleisen 2012, p. 19: "does not include
  an explicit letrec"). READ (W2 §A1, A3). Breitner 2017 found Launchbury's generalized correctness theorem
  false as stated (§2.3.3): the exposure was the quantifier over initial heaps.
- **C3** (Barrett, Cassels, Haahr, Moon, Playford, Withington 1996, "A Monotonic Superclass Linearization for
  Dylan", OOPSLA): monotonicity and local precedence; the paper states no suffix property. **C4** (LTUO
  §7.4.4, `ltuo-readable.txt` around l.3791): C3 plus the suffix property **for specs declared suffix** only;
  Scala reaches suffix without monotonicity (Odersky & Zenger 2005 §2.2: "linearization in Scala is not
  monotonic"). READ (W1 §9, §11).
- **LTUO §3.1.6 "OO isn't Message Passing"**: our 10-05 review read it as agreeing with keeping `call`/`send`
  outside the calculus (OB-FAREOO-REVIEW, "OB7 call and OB8 send").

### 4. Open item handed over by DEPUTY-OB-ENG: a `digest` primitive (Core4 semantics change, held for this round)

`Theory/ObjectiveBendDigest.lean` (W30, d8f7ca48) defines `digest a b` = cSHAKE256 under
`DREGG.OBEND.DIGEST/v1` over `len(a):8 ‖ a ‖ b` (preimage `:123`, `Admissible` `:127`), with
`binds_or_collides` proved and hiding **assumed**; the C export `minidregg_obend_digest` exists, but
`Primitive.digest` (W30 3c541dd5) is **not on main**. Adding it adds a Core4 constructor, a typing rule, a
machine step and a meter row. cv 01a1088f-47a0 proposes a size-aware meter (≤ 3 Keccak-f per step at
`scalarBits` 512) against "one tick, like multiply". Motivating use: ballot hiding, commitment =
digest(vote, salt) (OB3 in `work/OB-COMPLETION-20261005.md`). Questions: one-tick vs size-aware pricing;
Nat-in/Nat-out vs a bytes type; and whether a hash belongs in the language at all versus a kernel-supplied
value or a `Pred.hashEq` law clause (which already exists, `Pred/Core.lean:190-194`).

### 5. Questions for GPT-6

- **Q1-1.** *The C4 proof package.* GPT-6 noted that renaming invariance is satisfied by "refuse everything".
  What set of theorems is a *specification* of C4 — precedence-constraint satisfaction, monotonicity, suffix
  preservation for declared suffixes, completeness (refuses only when no consistent order exists), and the
  link from the list to method-combination behaviour? Is completeness provable for C4 at all, given that C3's
  is with a fixed tie-break?
- **Q1-2.** *Order conventions.* Every source (Bracha–Cook, MixedJava, POOF) composes most-specific-first;
  our `compose` is least-specific-first and our `extends` most-specific-first. Diamonds: `extends` dedups by
  declaration key, `compose(E, E)` applies `E` twice (Bracha–Cook would too). Is there a principled reason to
  keep `compose` as Nix-style pipeline order, or should it flip (a re-emit of every compose site)?
- **Q1-3.** *Cycles created by composition.* We chose partial-lazy (cycles are blackholes, a run-time
  divergence that the tariff and `faulted` absorb). Hirschowitz–Leroy would carry a dependency graph in the
  signature. In a ledger, where divergence costs the submitter a declared envelope, is "cycles are
  divergence" acceptable, or should `fix` refuse a chain whose requirement discharge is cyclic?
- **Q1-4.** *Which cyclic call-by-need calculus is the reference-vs-machine theorem anchored in*, and does our
  Lean statement name its quantifier over initial heaps (the exact place Launchbury's theorem was wrong)?
- **Q1-5 (OB-ENG item 4).** Digest as a Core4 primitive: one tick (like `multiply`) or size-aware (≤ 3
  Keccak-f per step at 512 scalar bits)? Nat-in/Nat-out or a bytes type? Or not in the language at all,
  since `Pred.hashEq` already makes commit–reveal a law clause?


---

## 02-modular-typing

<!-- source: 02-modular-typing.md -->

## 02 — Modular typing: templates, rigid Self, F-bounds, `requires`, `fix` discharge

Code: minidregg main `4ef4e808`, read only. Design record: `docs/objective-bend/MODULAR-TYPING.md`
(D1–D6). Classic literature: `lit/LIT-W1-oo-calculus-typing.md`. Book: LTUO §8 (Rideau, *Lambda: The
Ultimate Object*, mirror `ltuo-readable.txt`).

### 1. Current design

- **Core types** (`Theory/ObjectiveBendTypes.lean`, `Theory/ObjectiveBendTyping.lean`): a proof-producing
  checker (`check` returns a derivation, `Checked`). Rows compared canonically; **no subtyping**; type
  equality exact up to one bounded head unfolding of an alias variable; bounded type variables keep row tails
  (`future_row_instantiation_accepted`, `Theory/ObjectiveBendTyping.lean:744`); `fix` typed homogeneously
  (`target → inherited → target`), heterogeneity lives in `mix` (`heterogeneous_runtime_mix_accepted`, `:712`).
- **D1 Templates, not polymorphic Core4 terms.** An open declaration
  `extension AddY[Self has {x: Nat}, Super has {x: Nat}](self: Self, super: Super) -> Super with {y: Nat}`
  is checked once with `Self` and `Super` rigid; each use at `fix` is re-elaborated at its instance
  (memoized knot field `M.E@i`); the emitted program is closed Core4, so "every machine theorem keeps its
  statement and proof". Stated cost: code grows with distinct instances; **an open template is
  second-class** (a parameter can be any closed `Extension<T>`, never "any extension over `Self has {x}`").
  (MODULAR-TYPING.md:23-30.)
- **D2 Rigid ≠ alias.** `Self` is a lower bound the instance *supports*, never equal to its bound row:
  `Assumptions.rigid`; `self_as_bound_row_alias_accepted` / `self_as_bound_row_rigid_refused`
  (`Theory/ObjectiveBendTemplates.lean:1155`).
- **D3** Closed `spec S for T` types `self : T` but `super` at the members it reads (partial seeds work).
- **D4** `requires m(…) -> R` is the Self bound, checked against `T` exactly (`requires-signature`).
- **D5 `fix` discharges** bottom-up from the seed: `I_k = canonical(provided(L_k)[σ_k])`, `fix` requires
  `I_n = T`; refusals `requires-unprovided` (naming who requires), `inherited-unprovided`, `seed-extra`.
  **Bounds are never merged symbolically**: each layer is discharged where every type is known
  (MODULAR-TYPING.md §4 "Chain"). So `compose(AddY, AddZW)` of two *open* layers has no open type of its own.
- **D6** Recursive records are nominal (bounded-variable machinery of recursive sums); F-bounds
  (`Self has {heavier(other: Self) -> Self}`) range over every future type with such a method.
- **Proved** (`Theory/ObjectiveBendTemplates.lean`): `canonical_instantiate` (`:88`),
  `Discharges.infer_instantiate` (`:392`), `Discharges.check_instantiate` (`:1033`): if the checker accepts
  a template under rigid bounds and a substitution discharges them, it accepts the instance at the
  instantiated type with the same uses, given `extra` fuel. Inhabited by `coloured_instance_accepted`.
- **Open**: `instance_accepted` — instances are re-elaborated per layer, and `Super` in a template is the
  literal bound row rather than a second rigid variable, so the emitted instance is not literally
  `template[σ]`; an anonymous `typing refused` after a successful template check is still possible
  (`docs/OBJECTIVE-BEND.md:310-317`). Ancestry specs and non-plain operands keep the whole-target rule.
  Cross-package instances unaddressed.

### 2. Faré's target, for contrast (LTUO §8.4.1.3, read at `ltuo-readable.txt:4143-4171`)

```text
type ModExt inherited required newlyProvided =
  ∀ super, self : Type
    self ⊂ required self, super ⊂ inherited self ⇒
        super → self → super∩(newlyProvided self)
mix : ModExt j∩p s q → ModExt i r p → ModExt i∩j r∩s p∩q
```

READ. Three differences from ours: (1) Faré's is **first-class** (a type of values, quantified), ours is a
second-class template; (2) Faré's relies on **subtyping** (`⊂`) and **intersection**, we have neither (rows
compared canonically; `Super with {…}` plays the role of `super ∩ newlyProvided`); (3) Faré's `mix` has a
type that **reconciles assumptions** (`r∩s`, `i∩j`), ours composes open layers only at `fix`. Faré on
second-class types, §8.4.3.1 (`:4203-4207`, READ): "you cannot at all deduce types for first-class classes
from types for second-class classes … That is why typing first-class prototypes is more general and more
useful than only typing second-class classes". §8.4.2 (`:4173-4185`, READ) dismisses MyType "pseudo-variables
with complex 'matching' rules" in favour of ordinary variables with subtyping constraints.

### 3. What it commits us to

1. **No subtyping, ever, in the core**, so width is handled by lower bounds at instantiation only.
2. **Open specs are second-class.** A library cannot export a higher-order combinator over open extensions
   ("given any extension over `Self has {x}`, return one over `Self has {x, y}`") — only over closed ones.
3. **Typing is whole-program at `fix`**: the front end must see every layer's concrete types to type a chain.
   That is compatible with publish-time replay (topic 07) but not with separate compilation of open
   components across packages (LT5).
4. **Theorem cost stays flat**: the machine proofs never see a type variable.

### 4. Literature (LIT-W1 §3–§10; quotes and pages there)

- **Cook, Hill & Canning 1990** ("Inheritance Is Not Subtyping", POPL §3.2) is **our design, published**:
  "abstracting the type of self and replacing type recursion by type-dependency. The type recursion is
  reintroduced when the object is constructed"; a parent is `∀t ≤ F[t]. t → F[t]`, instantiation is `Y(P[σ])`.
  The soundness condition is `G[t] ≤ F[t]` **for all t, with the same t on both sides**. READ. Canning, Cook,
  Hill, Olthoff, Mitchell 1989 ("F-bounded Polymorphism for Object-Oriented Programming", FPCA §4.1–4.3):
  F-bounded functions keep differently-extended objects unmixable. READ.
- **Bruce 2002** (*Foundations of Object-Oriented Languages*, MIT Press, §16.1.3, Fig. 16.9, §18.1) and
  **Bruce, Schuett, van Gent, Fiech 2003** (PolyTOIL, TOPLAS 25(2), pp. 231–234): MyType with **matching**
  (`<#`, MyType identified on both sides) is the exact analogue of rigid `Self` with a lower bound. Bruce's
  soundness conditions: (a) bodies checked only under the matching assumption, never under an alias of the
  bound — our D2; (b) subclass types match the parent's with MyType identified; (c) static types are exact,
  no widening — the `breakIt` counter-example is excluded because we have no subsumption; (d) self distinct
  from the object type, with an explicit `close`. READ. §18.1 states the **cost of dropping subtyping**: no
  heterogeneous collections, and a parameter "supporting at least {m}" must become `∀G <# T` or a **hash
  type** `#T` (an existential over a matching bound). READ. We have neither.
- **Abadi & Cardelli** (book not obtained; "A Theory of Primitive Objects: Second-Order Systems", 1995,
  §3.4, §5.1–5.2, and their 1996 OOPSLA tutorial): the Self quantifier gives "inheritance for methods that return
  self or take arguments of the type of self … but without subtyping"; *overriding from the outside* is unsound
  without care because the object "might have been built as an element of" a proper subtype. That hazard needs
  subsumption; we have none. READ (W1 §4).
- **Rémy 1989** (POPL) and **Rémy & Vouillon 1998** ("Objective ML", TAPOS §3, App. 3): self is an open row
  closed at `new`; "inheritance is not subtyping"; classes are second-class: "it would be possible to make them
  first-class … The little gain in practice is probably not worth the complication". READ. **The closest
  implemented precedent, and it chose second-class as we did.** It uses equi-recursive object types; we use
  nominal recursive records.
- **Wand 1987/1989** ("Complete Type Inference for Simple Objects", LICS 1987; "Type Inference for Record
  Concatenation and Multiple Inheritance", LICS 1989 §5): with record concatenation "it is impossible to assign a
  principal type"; complete sets of types up to 2^{nk}. READ. This is the literature's best argument **for**
  templates over polymorphic core terms: our `extend` is concatenation, and instantiation at concrete types
  sidesteps non-principality.
- **Pierce & Turner 1994** ("Simple Type-Theoretic Foundations for Object-Oriented Programming", JFP 4(2) §6,
  §10): classes as records abstracted on self, instantiated by `rec`; existential encodings do not support strong
  binary methods. READ.
- **Odersky & Zenger 2005** ("Scalable Component Abstractions", OOPSLA §2.3): self-type soundness = (1) a
  class's selftype is a subtype of its bases' selftypes, (2) at `new`, the selftype is a supertype of the
  created object's type. READ. Our `requires` + `fix` discharge is rule (2).
- **Flatt, Krishnamurthi, Felleisen 1998** ("Classes and Mixins", POPL §3–4): a mixin's *inheritance
  interface* bounds its super — our `Super has`. Second-class, like ours. READ (OCR).
- **LTUO §8.4.1.3, §8.4.3.1** (section 2 above): Faré's `ModExt` is first-class, uses subtyping and
  intersection, and types `mix` with reconciled assumptions; "you cannot at all deduce types for first-class
  classes from types for second-class classes". READ.

**Code answers to W1's questions** (read on main): (i) *which type is `Self` at a nominal F-bound?* The final
self comes from the closed layers, else the enclosing definition's result type, else an annotated `let`
(`docs/OBJECTIVE-BEND.md:249-252`); in `Heavier.obend`, `node` returns `Node` and `colored` returns
`ColoredNode`, so `Self := Node` / `ColoredNode`, the nominal record, and the seed supplies the remaining
fields. (ii) *Does the safety theorem exclude field cycles?* No: divergence and blackholes remain
(`docs/OBJECTIVE-BEND.md:581`). (iii) *`Super with {y}` over a Super that already has `y` at another type:*
an instance-time refusal exists, `provided-mismatch` ("the composition provides members of the final self at
other types than it declares", `Compiler/ObjectiveBendElaborate.lean:1533`), and `inherited-mismatch`
(`:1476`); so this case is decided at **instantiation**, not by the once-only template check (INFERRED from
where the refusal lives) — which is exactly the gap `instance_accepted` would close.

### 5. Questions for GPT-6

- **Q2-1 (sharpest).** *Is second-class enough?* Every typed precedent with inheritance interfaces (Objective
  ML, MixedJava, POPL '90 templates) chose second-class mixins; Faré (§8.4.3.1) says first-class types cannot be
  recovered from second-class ones, and GPT-6's own bar was "a composite specification that crosses a stable
  higher-order interface". With no subtyping, the first-class route is Bruce's hash types (an existential over
  a matching bound) — a new Core4 type former and a case in every preservation proof (the cost MODULAR-TYPING
  D1 avoided). Is there a third route (e.g. dictionary-passing an open extension as a record of instantiation
  functions) that gives first-class open extensions without a core `∃`?
- **Q2-2.** *The substitution lemma.* POPL '90 and Bruce discharge soundness with one theorem: a body checked
  once under an abstract self with a matching bound stays well-typed at every instantiation satisfying the
  bound, self identified on both sides. Ours is `Discharges.check_instantiate` about the **checker**; the
  front-end corollary `instance_accepted` is missing because instances are re-elaborated, and
  `provided-mismatch` is decided at instance time. What is the right statement — and must `Super` become a
  second rigid variable (with presence/absence information à la Rémy, because `extend` is Wand's
  concatenation) for "checked once" to mean what it says?
- **Q2-3.** *Composition of open layers has no type.* Faré types `mix : ModExt j∩p s q → ModExt i r p →
  ModExt i∩j r∩s p∩q`; we never merge bounds symbolically and discharge each layer at `fix`. Without subtyping
  or intersection, what is the type of `compose(AddY, AddZ)` as an open value, and do we need one (it is what
  makes a library of composable open pieces possible)?
- **Q2-4.** *What does dropping subtyping cost in practice for us?* Bruce §18.1's list: heterogeneous
  collections; "any value supporting {draw}" parameters. In Mini, objects interact through `call`/`send` by
  method name with first-order data, so heterogeneity may live at the kernel boundary instead of the type
  system. Is that a sound place for it, or are we deferring the problem to an untyped boundary?


---

## 03-specification-and-reflection

<!-- source: 03-specification-and-reflection.md -->

## 03 — `Specification<T>` and the reflection contract

Code: minidregg main `4ef4e808`, read only. Design record: `docs/objective-bend/REFLECTION.md`.
Literature: LIT-W1 §7 (Pierce–Turner, existentials), LIT-W2 §D (reflection and equivalence).

### 1. Current design

- `Specification<T>` = `specification(SpecMeta, Extension<T>)`, with built-in first-order sums
  (`docs/OBJECTIVE-BEND.md:116-124`):
  `SpecMeta = declared{name, interface, laws} | composed{inherited, wrapping} | extension{}`,
  `SpecLaws = none{} | law{name, status, rest}`. Modules may not declare them (`builtin-type`).
- `compose(a, b)` = `specification(SpecMeta.composed{inherited: P a, wrapping: P b}, mix a b)`.
  Laws, ancestry and composition change the metadata *value*, never the type:
  `composeTy_closed` (`Compiler/ObjectiveBendSpecificationClosure.lean:44`), `twice_accepted` (`:184`),
  `law_spec_accepted` (`:192`).
- **Observers** (REFLECTION.md "Observers (edition 1, complete)"): `metadata(s)`, `reflect(p)`,
  `targetOf(p)` (forces the target only), application/`fix`/`mix` (behaviour), `==` on `String` fields of
  `SpecMeta`. No observer of closure code, law code, interface structure beyond a string, or heap identity.
- **Two equivalences**: behavioural `≈b` (contexts using a and b only through application, `fix`, `mix`;
  completed runs) and reflective `≈r` (`≈b` + equal metadata). `mix` is associative up to `≈b`, **not** up
  to `≈r`; probes R01/R02 (`tests/objective-bend-source/ltuo/AssociationProvenance.obend`) are a program that
  tells the associations apart. **Neither equivalence is a theorem**: `composition_associative`
  (`Theory/ObjectiveBendExtensions.lean:76`) is list concatenation on a separate model, not `Term.mix`.
- **Resource observations** are explicitly outside `≈b`: the machine distinguishes `finished`,
  `suspended`, `divergent`, `yielded`; "a resource-preserving rewrite needs its own statement. None is stated."
- **Prototypes**: `prototype(spec, target)` is a raw lazy pair; its typing checks components independently
  (`Ty.prototype spec target`, `Theory/ObjectiveBendTypes.lean:23` per OB-FAREOO-REVIEW U1), so `reflect(p)`
  proves nothing about how `targetOf(p)` was built. Open: `instantiate(spec, seed) = prototype(spec,
  fix(spec, seed))` with a theorem; and **R(Y M) vs Y(R∘M)**: is `self` the prototype (reflection inside the
  knot) or does the prototype wrap a finished target?
- **Why first-order data, not an existential** (REFLECTION.md): an existential needs a new Core4 type former
  and packing rule (every preservation proof grows a case) and makes provenance unobservable; first-order
  metadata needs no Core4 change and is matchable. "Metadata cannot carry closures, which is right: a closure
  nobody calls is a promise nobody keeps."
- Lane D4 (not on main): the interface label carried source spans, so moving code or adding a comment changed
  what a program computes; fixed by `withoutSpans` and qualified parent keys, theorem
  `interface_label_span_free` (OB-FAREOO-REVIEW D4; LTUO §7.3.5.7 shape determinism).

### 2. What it commits us to

1. **Every observer is a reason a rewrite is unsound.** With `metadata` observable, the compiler and any
   optimizer can only use `≈b` laws where no `metadata` observer reaches the rewritten spec. That is a
   whole-program side condition.
2. **Metadata is part of the package's meaning**, so the *front end* fixes what metadata a program can
   see (names, interface strings). Any change in how the front end renders an interface label is a change
   in program meaning (D4 showed one by accident) and a re-genesis.
3. **Provenance is not authenticated**: anyone can pair any spec with any target.
4. **Laws are listed but never discharged** (status always `unchecked`), so reflection can observe a
   promise nobody keeps — in tension with the stated rationale for excluding closures.

### 3. Literature (LIT-W2 §D; LIT-W1 §1, §7; quotes and pages there)

- **Wand 1998** ("The Theory of Fexprs is Trivial", *Lisp and Symbolic Computation* 10, Lemma 6–7, Cor 1–2):
  an observer that receives an injective, decidable coding of a term makes contextual equivalence
  α-congruence ("identical" with first-order variable coding); any adequate compositional semantics must then
  map each term to itself. READ. Applied (INFERRED, W2): `declared{…}` leaves are a quotient (equal
  declared fields are indistinguishable); but `composed{inherited, wrapping}` embeds sub-spec metadata
  recursively, so `metadata` is **injective on construction trees** and, under that observer, equivalence of
  composed specs *is* tree equality. Non-associativity under `≈r` is therefore forced by Wand's mechanism, not
  incidental. A coarser `composed` (a flattened list of declared names) would restore associativity.
- **Felleisen 1991** ("On the Expressive Power of Programming Languages", SCP 17, Thm 3.14): an extension that
  breaks an operational equivalence of the base language is non-conservative and cannot be macro-expressed.
  READ. `metadata` is such an extension; the R01/R02 probes are the Thm 3.14 witness, and the right framing is
  "metadata strictly adds expressive power", stated as a theorem, not a caveat.
- **Smith 1984** ("Reflection and Semantics in Lisp", POPL; causal connection "from event to description,
  and from description back to event") and **Kiczales, des Rivières, Bobrow 1991** (*The Art of the
  Metaobject Protocol*, Part I: introspective vs intercessory protocols). READ (front matter only for AMOP).
  `SpecMeta` is introspection only. If behaviour could ever depend on `metadata(self)`, that is intercession
  and behavioural associativity fails too: we need a **non-interference** theorem (behaviour of `mix`/`fix`/
  application is independent of metadata). R(Y M) vs Y(R∘M) is introspection vs intercession in fixpoint
  clothes: R inside the knot sees every self-call (intercession); R around the finished target only
  introspects (INFERRED, W2 §D3).
- **Pierce & Turner 1994** (§10) and **LTUO §8.4.3**: a first-class type descriptor is an existential
  ("there is a type T with this interface"). We chose first-order metadata over an existential to keep Core4
  unchanged and provenance observable; the literature does not require either, but Wand says observability of
  provenance has exactly the price we measured (R01/R02). READ (W1 §7; `ltuo-readable.txt:4191-4199`).
- **Cook 1989** thesis §4.4: inheritance already breaks encapsulation (the inheritor sees the parent's
  self-reference pattern); construction-history metadata is a second channel of the same kind. READ (W1 §1).

### 4. Questions for GPT-6

- **Q3-1 (sharp).** *Is `composed` meant to be injective on construction trees?* If yes, under the metadata
  observer we have Wand's trivial theory for the composition fragment, and every optimizer or refactoring that
  reassociates `compose` must prove no `metadata` observer reaches it (a whole-program side condition). If no,
  what quotient (flattened declared names? a multiset of declaration keys?) restores associativity while keeping
  the provenance that justified reflection in the first place?
- **Q3-2.** *Non-interference.* The weak form holds by inspection of the rules: applying a specification
  ignores its metadata (`applySpecification`, `Theory/ObjectiveBendOpenRecursion.lean:253-254`, READ), and only
  `metadata` reads it. But a program may `match` on `metadata(s)` of a spec it is handed and change behaviour —
  intercession by the back door, which W2 (Smith, AMOP) says is what breaks behavioural laws. Is the weak
  form the right theorem to state, or should metadata be readable only in a stratum whose results cannot flow
  into a spec's behaviour (and is that even expressible without an information-flow type)?
- **Q3-3.** *R(Y M) or Y(R∘M)?* Given the above, is the intended reflective power introspection only (R around
  the finished target, `instantiate(spec, seed) = prototype(spec, fix(spec, seed))` with a theorem relating
  `targetOf` to `fix`), or must `self` itself be the prototype? What breaks in each for laziness (forcing the
  target must not force the spec, and vice versa)?
- **Q3-4.** *Promises in metadata.* Laws appear in metadata with status `unchecked`, while closures are excluded
  because "a closure nobody calls is a promise nobody keeps". Should an unchecked law be observable at all?
  (Joint with Q6-1.)


---

## 04-activities-resume-checkpoints

<!-- source: 04-activities-resume-checkpoints.md -->

## 04 — Activities, answer slots, resume-with-view, checkpoint transparency

Code: minidregg main `4ef4e808`, read only. Literature: `lit/LIT-W2-laziness-reflection-continuations.md`
(§B effects and laziness, §C guardedness, §E continuations/durable execution) and LIT-W3 §7 (Khan).

### 1. Current design

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

### 2. What it commits us to

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

### 3. Literature (LIT-W2 §B, §C, §E; LIT-W3 §6–§7; quotes and pages there)

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

### 4. Questions for GPT-6

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


---

## 05-call-and-send

<!-- source: 05-call-and-send.md -->

## 05 — `call` (deferred writes, re-entry refusal) and `send` (inboxes, postage, forwarding)

Code: minidregg main `4ef4e808`, read only. Lane notes: `hbox:/tank/dregg-build/claude-lanes/ob8/STATUS.txt`
(OB7 and OB8 decisions with reasons). Open items 5.4 come from DEPUTY-OB-ENG's 2026-10-06 message (it is
not coding them because they change meaning). Literature: `lit/LIT-W3-calls-sends-contracts.md`.

### 1. Current design

**Call** (`Kernel/ObjectiveCall.lean`, header `:1-60`). An `invoke` turn calls one method of one object;
the method may synchronously call other objects' methods in the same turn, depth first, to `callDepth` 8.
- A method is a declaration of the object's **pinned** package, lowered by the kernel's own front end
  (`loadMethod`), of type `method(view: {version, state}, args: X) -> Activity<P, R, {result, write}>`,
  `P ⊆ {call, send}`, `R ⊆ {returned, queued}`. Every yield is answered in the same turn; a method whose
  Plan admits `await` is refused `notCallable` before running ("an Activity cannot be called").
- **Re-entry is refused, mandatorily**: `reentry_refused` (`:886`; a call whose target is on the stack
  errors `.reentry`), `invocation_reentry_free` (`:1217`; every frame stack of an admitted invocation is
  `Nodup`).
- **Writes are deferred to frame return**, applied to the frame's own object only, judged by that object's
  law on (the state the frame was shown, the new state) under that frame's facts:
  `invocation_writes_from_view` (`:1233`). The callee's view is the snapshot plus every write an earlier
  frame of this turn applied at its return. Two calls to one object compose in order.
- **Authority**: the root frame carries the signer; a nested frame carries the signer as `request/subject`
  only under a scoped grant `{object, method, uses}` of the invocation, spending one use (`grantSpent`).
  Without a grant every law atom reading the subject fails closed. `request/caller` names the calling object.
  Docstring names Daml's non-transitive delegation and Pact's scoped, counted capabilities (`:24-33`).
- **One declared envelope** for the tree (`runCounted`, proven equal to `runBounded`); exhaustion refuses
  the invocation and charges nothing.
- Reasons recorded by the lane (OB8 STATUS "DECISIONS + REASONS (OB7)"): per-frame law judgement because
  turn-end judgement "lets a granted later frame launder an ungranted earlier write"; apply-at-return +
  own-object writes + re-entry refusal ⇒ no frame-conflict abort needed; frames resume the machine's own
  yielded state, so calls need no `ForcingTransparent` premise. Evidence: journey C1–C8 51/51; a
  guard-removed mutant "commits the DAO (bank 40 / thief 60)" (MERGE-QUEUE.md line 225).

**Send** (`Kernel/ObjectiveSend.lean`, `Kernel/Inbox.lean`, `Kernel/AnswerSlot.lean`).
- A frame yields `send {to: object n | slot n, method, args}`, answered at once with `queued {slot}`; the
  message id `H(turn, index)` names its reply slot.
- The invocation declares `postage`, the envelope each message is delivered under; each send escrows its
  price into the purse of the queue holding it (`uncovered` otherwise).
- Inboxes are per-(sender, target) FIFO queues, bound `Inbox.bound = 16` (`Kernel/Inbox.lean:61`),
  `lawful_fifo` (`:146`), `reorder_unlawful` (`:172`); `queueFull`.
- `deliverMessage` (anyone) pops the head and runs the target's method as a root frame with
  `caller = sender` and **no subject**, paid from the inbox purse only
  (`MessageDelivery.debits_only_purse`, `Kernel/ObjectiveSend.lean:283`). It decides the reply slot, whose
  decider is the role `delivery m` (`decide_delivery_refused`, `Kernel/AnswerSlot.lean:251`). A failed
  delivery pops, decides `broken`, commits no write (`failed_delivery_pops`, `Kernel/ObjectiveSend.lean:333`).
- **Restricted pipelining**: a send to `slot n` (reply of an undelivered message) queues on that slot; the
  turn deciding the slot forwards it when the reply is an object reference, else refunds; a send onto the
  reply of a send that is itself only queued is refused `notPipelinable` (depth 1).
- Not built (`docs/OBJECTIVE-BEND-EVENTS.md` "Not built"): an activity yielding `call`/`send`; an activity
  awaiting a message; sends from a delivered message (refused as a failure); deeper pipelining; objects
  holding capabilities.

### 2. What it commits us to

1. **Synchronous calls across trust boundaries.** This is the root's OPEN 1 for Ember
   (`ROOT-PROGRAM-MODEL-DECISIONS-20261004.md:118-119`): "Synchronous cross-principal `call` at all, versus
   Agoric's 'never synchronous across trust boundaries'. Root's lean: yes, with Daml authority + scoped
   grants + mandatory re-entry refusal." Re-entry refusal is what makes this safe; its cost is unmeasured
   (root resolution D1: "the cost of refusing all re-entry is unmeasured. Keep the refusal and measure it on
   Mini's own cohorts").
2. **Refusing re-entry forbids callbacks**: observer patterns, a vault calling back a borrower (flash-loan
   shape), "A asks B, B asks A for a quote" all need either `send` or restructuring. SeRIF and ECF (below)
   are the two literatures on permitting *safe* re-entry.
3. **Views are snapshot+applied-earlier-writes, writes at return.** A caller's own pending write is
   invisible to its callees; a caller's decision computed from a callee's *returned value* can be stale by
   the time the caller's frame returns if a later sibling call changed the callee (INFERRED; the law judges
   only the caller's own object, so this is a correctness rather than a safety question).
4. **Send is asynchronous, FIFO per pair, bounded, prepaid.** Postage is fixed at send time; delivery by
   anyone; caller identity flows (`caller = sender`), subject authority does not.
5. **Answer slots unify replies and decisions**: one decider, one deadline, one terminal decision.
   Message reply slots have the role decider `delivery m`. (Delivery slots never expire today — OB-ENG item 2.)

### 3. Literature (verified by worker W3 against primary text; LIT-W3 has quotes and line numbers)

- **Miller 2006, *Robust Composition* (PhD thesis, JHU), §13.1 (plan interference), §14.1–14.2 (turns,
  vats), §16.2–16.5 (pipelining, datalock, broken-promise contagion), §19 (E-ORDER); Miller, Tribble,
  Shapiro 2005, "Concurrency Among Strangers", TGC, §7.1.** READ (LIT-W3 §1). E never banned synchronous
  calls: a turn *is* a synchronous call tree, but only among objects in one vat, for mutual exclusion without
  locks. Plan interference (nested publication, nested subscription, aborting the wrong plan) needs a callee
  running on the caller's live, mid-update heap. **Ours removes two of the three** (snapshot views + deferred
  writes; re-entry refusal) and **keeps "aborting the wrong plan"**: a callee's law refusal aborts the whole
  invocation. In code this is uncatchable by construction, since a frame's response type is
  `returned | queued` with no failure arm (`Kernel/ObjectiveCall.lean:60-63`; refusal `lawDenied`, `:461`).
  E's cure for that hazard is `send`. W3: "no paper studies exactly this point"; defensible, new.
- **E-ORDER (Miller §19.2)** is stronger than our per-(sender, target) FIFO: a reference passed in `args`
  lets the receiver send to the same target on a *different* queue and overtake the sender's earlier
  messages. READ.
- **CapTP / OCapN and Cap'n Proto RPC** (`rpc.capnp` `Disembargo` ll.688-735). READ (LIT-W3 §2). Our
  forwarding is the "same-vat" case: atomic with resolution, so the multi-path races (Tribble 4-way race)
  cannot arise, **but** the `foo()`/`bar()` ordering question survives locally: where does a forwarded
  message enter the FIFO relative to direct sends made between send and resolution? Pipelining into
  *fields* of a result (`op:get`, `op:index`) is a real loss vs ours (object-reference replies only). In a
  single kernel pipelining saves turns, not round trips.
- **Daml** (Bernauer et al. 2023, arXiv:2303.03749, §3.6 authorization rules). READ (LIT-W3 §4). Exercise
  consequences are checked in the context *S ∪ C* (signatories ∪ controllers of the callee's template);
  "Delegation is not transitive … deliberate". **Difference of kind**: Daml's nested authority is
  *callee-declared consent*; ours is *caller-delegated* (the signer's scoped grant). Mini has no signatory
  referent on `ObjectRecord` (REVIEW-SCHOLAR-LAWS D-6). Also: Daml re-entry into a *consuming* choice fails
  because the contract is already archived (re-entry protection by linearity).
- **Soroban authorization** (Stellar docs, `objective-bend-grounding/stellar-soroban-authorization.txt`
  ll.63-82) and **Pact capabilities** (Kadena manual). READ. Both bind **arguments** (Soroban: an authorized
  invocation *tree* with args, nonce, expiry, each node marked "exhausted" once matched; Pact: capability
  with args, "managed" capabilities with a diminishing quantity). Ours is `{object, method, uses}`:
  **any frame holding the grant can call that method with arbitrary args as the signer** — a confused-deputy
  exposure if a malicious object sits mid-tree.
- **SeRIF** (Cecchetti, Yao, Ni, Myers 2021, "Compositional Security for Reentrant Applications", IEEE S&P,
  §4.1 Def 1, Fig 4, §4.2 Def 2). READ (LIT-W3 §5). Re-entrancy is defined by *integrity labels*, "deliberately
  not by object boundaries": object-level refusal over-refuses (Fig 4b) and **misses application-level
  re-entry across mutually trusting objects** (Fig 4c, A → B → C with A and C halves of one app — the Parity
  wallet shape). Permitted safe forms: tail re-entrancy, Town Crier's deliver/cancel. "Banning all reentrancy
  might seem appealing, but this solution would be overly restrictive" (§2.3).
- **ECF** (Grossman, Abraham, Golan-Gueta, Michalevsky, Rinetzky, Sagiv, Zohar 2018, "Online Detection of
  Effectively Callback Free Objects with Applications to Smart Contracts", POPL; Fig 14). READ. On 2015–17
  Ethereum, callbacks were **0.16% then 1.0%** of executions (Fig 14 `Callbacks` column); non-ECF 0.004% then
  <0.001%. So the cost of a blanket refusal is bounded between ~1e-7 and ~1e-2 of executions and **unmeasured**
  for us. W3: with deferred writes and snapshot views, read-only re-entry is harmless by construction, so the
  refusal is "belt over braces", not the mechanism that excludes the DAO shape. (Our journey plant
  "guard-removed mutant commits the DAO (bank 40 / thief 60)", MERGE-QUEUE.md:225, says the guard *is*
  load-bearing in at least one program: **the two claims conflict and the plant should be re-read** —
  INFERRED; see Q5-1.)
- **Aptos Move** module lock (Dedaub, "Insights from 300+ Audits", 2025-09-17; `objective-bend-grounding/
  dedaub-aptos-reentrancy.txt`). READ. Production precedent for exactly our rule (direct and indirect
  re-entry refused); its auditors list the bypasses: state held in a third party's resource, and closure
  re-entry within one module. "A per-object lock is only as good as the guarantee that the invariant lives in
  one object."
- **Internet Computer** (DFINITY interface spec and "message execution properties", paperbin). READ
  (LIT-W3 §6). Nearly our `send`: pairwise ordering of *starts* only; a call is queued only if the sender
  returns without trapping; exactly one reply-or-reject; cycles escrowed at send with a reserve for the
  **response leg**. Two IC scars: unbounded waits wedge callers (we have mandatory deadlines), and a
  bounded wait yields `SYS_UNKNOWN` (callee ran, caller told otherwise). Ours avoids `SYS_UNKNOWN` **today**
  only because delivery slots never expire (`Kernel/AnswerSlot.lean:15-22`, `expire_delivery_refused`); item
  5.4.2 (activities awaiting a message, with a deadline) would reintroduce it.
- **NEAR** (cross-contract docs; READ) makes callback gas a *second* declared number; EIP-150 (READ) shows the
  call-depth attack needs a caller that can catch a callee failure — ours cannot (above).
- **Block-STM** (Gelashvili et al., PPoPP 2023, Corollary 2) and **CALM** (Hellerstein & Alvaro, CACM 2020,
  Theorem 1; Bailis et al. 2014 Claims 11–14). READ (LIT-W3 §8–9). Deferred-write frames match Block-STM's
  per-transaction write set; the read set must be recorded per (object, field, version). The only monotone
  mutations we have are unbounded appends and write-once decisions; the inbox bound (16), postage escrow and
  consume-once are all non-monotone, so cross-domain or parallel `send` is limited by exactly the features that
  make it safe.
- **Durable Functions critical sections** (Burckhardt et al. 2021, §3.4.1): may call only pre-locked entities;
  the nearest published relative of a scoped grant, for state rather than authority (INFERRED, W3).

**Code answers to some of W3's questions** (read on main): a sibling call *does* see an earlier sibling's
write — the callee's view is "the snapshot, plus every write an earlier frame of this turn already applied
at its return" (`Kernel/ObjectiveCall.lean:21-23`), taken at frame **entry**; a full queue refuses the whole
turn by name (`queueFull`, `:66`); a frame cannot catch a callee refusal (no failure arm in `R`); seat exit
rules are only `onDemand | afterDeadline` (no Zoe `waived`, `Kernel/Seat.lean:58-62`), and
`seat_offer_safe_forever` is a reachable-state invariant from a seatless genesis (`:1287`), with
`seat_debit_authorized` (`:1383`) enumerating the only debit paths (reallocate by the seat's instance, exit,
terminate). W3's remark that "a second write to the same slot aborts (R-CALLS D2)" describes the root's design
resolution D2, **not** the code: OB7 applies writes in order at return and has no frame-conflict abort
(`Kernel/ObjectiveCall.lean:45-48`).

### 4. Open design items handed over by DEPUTY-OB-ENG (meaning changes; not coded)

**5.4.1 Sends from a delivered message** (cv 01a10ae9-79e1). Today a frame running under `deliverMessage`
that yields `send` has no paying account, so the delivery fails (pops, `broken`). Options: (a) the original
sender prepays a bounded postage *tree* declared at send; (b) the target object pays from an object-held
purse (needs objects holding accounts + authority to spend from a subjectless frame); (c) forbid by type
(a delivered method's Plan type excludes `send`). (c) is a typing rule; (a)/(b) change cost/authority
semantics. Bread's pay flows want (a) or (b).

**5.4.2 An activity awaiting a message reply** (cv 01a10ae9-7a1a). Reply slots are decided only by the
`deliverMessage` that pops that id, a subjectless turn anyone may run. Awaiting one makes the activity's
resume depend on that. Interacts with resume-with-view, timeout/abandon (delivery slots never expire), and
exhaustion. Needs: must an await on a never-expiring slot carry a timeout arm? Do `upgraded`/abort apply?

**5.4.3 Pipelining depth > 1** (cv 01a10ae9-79fd). Pipelined sends queue on the reply slot with postage in
the holding inbox's purse; a pipelined message's own slot opens only when forwarded ⇒ depth 1. E/CapTP-style
promise pipelining needs a contagion rule; OB8 explicitly refused deciding a slot from a non-matching turn.

### 5. Questions for GPT-6

- **Q5-1 (sharpest).** *Where does a cross-object invariant live?* Laws judge one object's (old, new,
  request); re-entry refusal is per object. SeRIF Fig 4c, the Aptos bypasses and eUTxO's whole-transaction
  validators all say per-object guards miss invariants split across objects (A → B → C, A and C one app).
  Options: (a) the object model *declares* that an invariant lives in one object (plus a publish-time lint);
  (b) laws see sibling frames' writes (eUTxO), coupling every write to the turn; (c) trust-labelled
  re-entrancy à la SeRIF. Which, and what Lean statement replaces "no object twice on the stack" as the
  theorem that matters? Sub-question: is the re-entry refusal load-bearing given snapshot views + deferred
  writes (W3 says no; our DAO mutant plant says yes)?
- **Q5-2.** Scoped grants `{object, method, uses}` do not bind arguments; Soroban and Pact do (and Soroban
  binds the sub-invocation tree, a nonce, an expiry). Is the confused-deputy exposure real under our model, and
  what is the right matching rule? Separately: Daml-style callee-declared consent (signatories) vs our
  caller-delegated grants — should Mini have both, named?
- **Q5-3.** Synchronous cross-principal `call` at all (root OPEN 1)? E would say: only within a vat.
  Our variant has no live heap and no re-entry, but keeps "aborting the wrong plan" (an untrusted callee's
  refusal aborts the caller's whole turn). Is "a caller who will not underwrite a callee uses `send`" an
  adequate answer, or should a frame be able to observe a callee's refusal (and if so, how do we avoid the
  EIP-150 call-depth attack class)?
- **Q5-4.** Send ordering: forwarded-on-resolution vs direct sends (Cap'n Disembargo); E-ORDER forks for
  references passed in args; datalock (can the delivery deciding slot S send to S?). Which order do we promise?
- **Q5-5 (OB-ENG 5.4.1–5.4.3).** Who pays onward sends from a delivered message — prepaid postage tree,
  object-held purse, or forbidden by type? Must an activity's await on a (never-expiring) message reply slot
  carry a timeout, and how do we avoid the IC's `SYS_UNKNOWN` when it does (remove the message and refund in
  the same transition)? What contagion rule makes pipelining depth > 1 sound? And who pays the *reply* leg
  (IC reserves for the response; NEAR declares callback gas separately; we have one `postage`)?


---

## 06-laws-and-seats

<!-- source: 06-laws-and-seats.md -->

## 06 — Laws as decidable predicates; offer safety and seats

Code: minidregg main `4ef4e808`, read only. Literature tags: **READ** (read at the cited place, by me or a
worker), **VIA-SCHOLAR** (from an earlier scholar report, named, not re-verified here), **INFERRED**.
Worker verification of eUTxO/Zoe/Daml primary texts: `lit/LIT-W3-calls-sends-contracts.md`.

### 1. Current design

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

### 2. What it commits us to

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

### 3. Literature

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

### 4. Questions for GPT-6

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


---

## 07-admission-by-reexecution

<!-- source: 07-admission-by-reexecution.md -->

## 07 — Native admission by re-execution

Code: minidregg main `4ef4e808`, read only. Tags as in the index. Block-STM and CALM primary-text checks:
`lit/LIT-W3-calls-sends-contracts.md` §8–§9.

### 1. Current design

There is **no proof system in admission**: a receiver admits an Objective invocation by re-running the
front end and re-executing the method (`docs/OBJECTIVE-BEND.md:495-543`; `docs/ZK.md` is the empty proof
carrier).

- **Publish** (`Host/ObjectivePackageAuthor.lean`): the Host's own front end runs on the package; exactly
  `publishedCore` (`Compiler/ObjectiveBendPublication.lean`) is published; package edition 3 names one
  front-end identity.
- **Quote** (`Host/ObjectiveInvocationQuote.lean`): the local Host derives the final command from the
  member's retained request; it never accepts a remote command, output or input.
- **Admit** (`Kernel/ObjectiveBendNativeAdmission.lean`, `prepareCore` then `admit`): the registered
  policy re-encodes exactly; the declared envelope ≤ the policy maximum; `proofWork` equals the tariff's
  price of the declared envelope; funding checked before execution; sources and inputs only as current
  authenticated reads with exact guards; the receiver **re-runs the named front end** and admits only a
  byte-identical typed core; the applied term is type-checked; `executeWith` runs under the declared
  limits; the result is lowered to a Plan whose effects must equal the command's (`Output.exact`); measured
  usage must fit the declared envelope.
- **What it proves** (`Kernel/ObjectiveBendAdmissionSemantics.lean`): `admitted_source_semantics` (`:26`):
  the admitted run is a finished `runBounded` and its Data is *the* deep reference evaluation of the
  applied term; `admitted_data_unique` (`:44`): two admissions of the same applied term extract the same Data
  under any deployments, capacities and codecs ("a capacity envelope admits or refuses a run; it never
  changes what the run means"); `admitted_front_end` (`:97`): the typed core is byte-for-byte this front
  end's lowering of the package sources and is never refused by the machine.
- **Fees are priced on declared envelopes, never measured work** (`refund_measurement_free`,
  `Kernel/ObjectiveActivity.lean:2927`; `exhaustion_charges_declared`, `:3084`). Exhaustion is a paid,
  committed turn.
- **The front end is trusted.** "Source semantics" in these theorems is Core4's reference semantics, not
  `.obend`'s (GPT-6 §6; topic 00 row LT3). A replaying receiver reproduces the compiler's bytes, wrong or
  right.

### 2. What it commits us to

1. **Determinism is the whole security argument.** Every node must compute bit-identical results from the
   same inputs: no measured quantity may reach state or fees. Our theorems state determinism of the
   reference semantics (`source_evaluates_unique`) and resource independence (`runBounded_resource_independent`,
   `Theory/ObjectiveBendDemandAdequacy.lean:3636`). The C backend is differential-tested only
   (`docs/OBJECTIVE-BEND.md:644-647`), so a second executor is not covered by these theorems.
2. **Re-execution costs every validator the full work**, so the tariff must price the worst case it
   admits (declared envelope), and the envelope must also bound the front end's own re-run. Read: the
   checker's `typeFuel` is a priced lane of the tariff (`Kernel/ObjectiveTariff.lean:50`) and is passed to
   the replay (`Kernel/ObjectiveBendNativeAdmission.lean:395,418-419`, run "last, after every cheap
   refusal"); the policy bounds `sourceBytes` (`:79`). Not found: any bound or price on the parser,
   the elaborator, C4 linearization or template instantiation as such. INFERRED: their cost is bounded only
   indirectly, by source size, and no theorem states that bound.
3. **Admission is sequential per turn**; parallel admission would need a Block-STM-like guarantee that the
   parallel result equals a preset sequential order (the root's "root = sequential fold";
   VIA-SCHOLAR REVIEW-SCHOLAR-CALLS scope line).
4. **Privacy is out of scope**: laziness leaks through access patterns and timing; a private backend
   needs a both-arms `case` and a public resource bound (`docs/OBJECTIVE-BEND.md:642-652`).

### 3. Literature

- **State machine replication** (Schneider 1990, "Implementing fault-tolerant services using the state
  machine approach", ACM Computing Surveys): replicas agree if commands are deterministic and applied in
  the same order. Re-execution admission is SMR with the program as part of the command. INFERRED (classic;
  not re-read for this packet).
- **Execute-order-validate** (Androulaki et al. 2018, "Hyperledger Fabric: A Distributed Operating System
  for Permissioned Blockchains", EuroSys; paperbin `androulaki-hyperledger-fabric-2018.pdf`): Fabric does not
  re-execute at validators; it validates endorsed read/write sets, because chaincode may be nondeterministic.
  Our choice is the opposite and depends on Core4 determinism being total. INFERRED from my knowledge of the
  paper; not re-read for this packet.
- **Block-STM** (Gelashvili et al., PPoPP 2023; paperbin `gelashvili-block-stm-2022.pdf`): parallel
  optimistic execution; Corollary 2: the snapshot after join "returns the exact same values at exact same
  paths as would be persisted at the end of a sequential run"; termination (Thm 2) rests on `VM.execute` being
  wait-free; and "a single location for gas updates could make any block inherently sequential". READ
  (LIT-W3 §8). Our deferred-write frames are Block-STM's per-transaction write set, and no intra-turn
  read-your-writes across frames keeps validation per location — **provided** read sets are recorded per
  (object, field, version) and fee/escrow credits are commutative deltas rather than read-modify-write on one
  sink.
- **CALM** (Hellerstein & Alvaro, "Keeping CALM: When Distributed Consistency Is Easy", CACM 2020;
  paperbin `hellerstein-keeping-calm-2019.pdf`), Theorem 1: "A program has a consistent, coordination-free
  distributed implementation if and only if it is monotonic." READ. LIT-W3 §9 grades our operations: only
  unbounded appends and write-once slot decisions are monotone; the inbox bound, postage escrow, consume-once,
  deadline expiry and view reads all need the log (with Bailis et al. 2014 Claims 11–14 for the counter cases).
- **Durable functions** (Burckhardt et al. 2021, OOPSLA, Lemma 6.5 "Deterministic Replay", Thm 6.4): replay
  and stored-state models are bisimilar given determinism of the step, which "in a mainstream programming
  language … is not implicitly guaranteed" (§6.3). READ (LIT-W2 §E2). Our re-execution admission puts the
  determinism obligation on the *machine* (provable in Lean) rather than on user code — the stronger position.

### 4. Questions for GPT-6

- **Q7-1.** Is "admit by byte-identical front-end re-run + deterministic re-execution" a sound basis for a
  multi-party ledger when the front end itself is trusted and unverified against a surface semantics
  (LT3)? Concretely: what does a receiver actually guarantee a *source author* today, and what would LT3 add?
- **Q7-2.** Fees on declared envelopes: type-checking fuel is priced, elaboration is not (as read). Is there
  a package engineered to be cheap to execute and expensive to *elaborate* within the policy's source-size
  bound (C4 on a wide DAG, template instantiation blow-up — MODULAR-TYPING D1 admits "code grows with the
  number of distinct instances")? Should elaboration be a metered lane with a theorem bounding it by
  declared fuel?
- **Q7-3.** What determinism obligations does call-by-need impose that call-by-name would not (heap
  addresses in checkpoints, GC order), and are they all covered by `admitted_data_unique` + the checkpoint
  codec, or is there a nondeterminism channel through checkpoint *bytes* (topic 04)?


---

## 08-swarm-work-lifecycle

<!-- source: 08-swarm-work-lifecycle.md -->

## 08 — The swarm's work-item lifecycle (not Objective Bend; Ember asked for it in the packet)

### How a work item lives today (measured over 10-04 → 10-06)
author (agent, on a warm lane clone) → single-file checks (`lane-check` 4-7 s, or `lean-ask` 0.4 s) → affected-module build in a
build slot → named acceptance (journeys on scratch worlds, cohorts with planted faults) → `- [QUEUED]` line in MERGE-QUEUE.md →
one merge keeper rebases batches onto main → ONE full gate per batch (umbrella ~10-13 min on a fast box + pins + objective-proofs
snapshot + hyp-ledger + filtered Rust + touched journeys) → fast-forward main, move `green` → warm bases advanced by copy.

### Recurring friction (each observed, with counts where known)
- Rebase churn in hot clusters: ~9 lanes in the activity/object files at once; most WIP at a pause was never compiled on the
  current tree. Fixed by a one-owner-per-cluster rollup; fan-out stays for non-overlapping files.
- Duplicate verification: each landing once paid ~5 full builds (lane gate, keeper gate, second keeper gate, base rebuild per box);
  cut to ~1 (VERIFY-ONCE), measured −58 build-minutes per landing.
- False greens: stale imported .oleans under bare `lake env lean`; gate rows passing only inside `all`; regenerated fixtures disarming
  mutation tests; a queue line marked LANDED that never reached main; "test-only fixes" that relax checks.
- Re-gate churn from GENERATED PINS: build-surfaces, host-closure, the objective-proofs statement snapshot and the native-accepted
  fixture are regenerated in nearly every batch; each regeneration is an audit burden (was anything removed or weakened?).
- Slot starvation and IO starvation on shared boxes; agents waiting on builds; a merge gate starved behind lane builds (fixed by a
  reserved slot).
- Context ceilings: veterans at 500-900K tokens; renewal via `cv distill` (≈1/6 tokens, 28/30 probe answers) vs lossy prose handoffs.
- Coordination by message relay through the root (the root becomes the bottleneck); deputies now address each other directly.
- Journeys under-run: several ranges compiled but never executed on a world before queueing.

### Questions for GPT-6
1. Is a merge-queue with ONE full gate per batch and optimistic main (`green` lags) the right shape for a proof-heavy monorepo
   with ~1,400 Lean modules and generated pins, or should we move to a stacked/speculative merge (à la Bors/merge-train, Zuul's
   speculative pipelines) where each candidate's gate starts on the speculative tip?
2. Generated pins (statement snapshots, closure lists) are both our strongest anti-weakening instrument and our biggest source of
   re-gate churn. Is there a design that keeps the audit value (no statement silently removed or weakened) without regenerating a
   global artifact every batch — e.g. per-module content-addressed statement manifests, or a monotone "ratchet" that only accepts
   additions and explicit, signed deletions?
3. What's the right granularity of a work item for agent lanes in a dependent-typed codebase: per theorem, per module, per feature,
   and how should the dependency graph of the Lean modules drive scheduling (critical-path first, avoid co-scheduling items whose
   affected closures intersect)?
4. Context management: is distill-and-resume (keep decisions/intents/facts, drop tool output) a sound way to extend an agent's
   effective horizon, and what does the literature on long-horizon agents suggest about what must be retained?
5. Verification evidence classes (compiled / executed / proved) — is there a standard taxonomy we should adopt so a landing's
   evidence is machine-checkable rather than prose?


# Appendix A — Objective Bend work rows (private notes, inlined)


---

## OB-LTUO-20261005

<!-- source: OB-LTUO-20261005.md -->

## Objective Bend vs LTUO — rows from GPT-6's source audit at 259a2fb (2026-10-05)
Verdict: Core4's kernel (mix with one final self + whole super, real knot, lazy cells) is RIGHT; keep it. The gap is the
AUTHORED type system and what proofs claim. Full review text: pasted by Ember into root session ce776c01 on 10-05 (retrieve with `cv show ce776c01 --grep "trivial non-modular"`).
Supersedes/extends OB-COMPLETION rows OB1 and OB5.

LT0 PROBES FIRST (sonnet ok): write GPT-6's 11 characterization probes as real front-end cohort rows (the zip lives in GPT's
  sandbox; recreate from the review): positive controls (review/self/super = 7, GenericExtension, heterogeneous XYZ), and
  witnesses: `def twice(e: Extension<Nat>) -> Specification<Nat>: compose(e, e)` (predicted REFUSED: metadata shape
  {name,interface,laws:{}} vs compose's {operator,inherited,wrapping}); a spec with a `law` vs Specification<T>; recursive
  record `record Node: combine(other: Node) -> Node` ("recursive row annotation requires explicit future-row binder"); a
  one-method spec forced to accept a whole-T seed; `requires` as unchecked metadata; `law impossible: false` accepted. Each row
  states the CURRENT outcome and the TARGET outcome; target rows start red and turn green as LT1-LT3 land.
LT1 SPECIFICATION<T> CLOSED UNDER COMPOSE: a public spec type whose metadata is either a parameter with an opaque/existential
  public interface or one uniform inspectable metadata representation; decide by the reflection contract (LT4). Laws and
  composition must not change the public type. Acceptance: LT0's `twice` and the law row typecheck.
LT2 AUTHORED MODULAR TYPING (opus, the big one): source binders for the future self and the inherited row
  (row-polymorphic `spec S[Self ⊇ {review}, Super ⊇ {}]`-style), an extension checked ONLY against its declared assumptions,
  preservation of unrelated inherited structure, composition reconciling assumptions, `fix` discharging final-self
  requirements (this IS checked `requires`), and recursive records / binary self methods through the explicit future-row
  binder. Acceptance: an extension typed yesterday survives a fourth field added tomorrow without edits; Node.combine compiles;
  the review example needs no placeholder seed; the no-refusal theorem still holds over the new rules.
LT3 SURFACE SEMANTICS (= OB1, now concrete): define .obend meaning independently and prove lowering preserves it, starting with
  compose ORDER and ancestry (a compiler that swaps layers must fail the theorem); plus the C4 proof package: well-formedness
  premises, ancestor coverage, duplicate elimination, precedence, suffix preservation, and the link from the linearization to
  method-combination behaviour (renaming invariance alone is satisfied by "refuse everything").
LT4 REFLECTION CONTRACT: state the permitted observers; separate behavioural equivalence of extensions from equivalence of
  reflective specs (compose associativity holds for behaviour, not provenance); resource observations (ticks, heap, suspension)
  stated separately. A provenance-establishing prototype constructor (projection relates to fix(spec, seed)), distinct from the
  raw pair; decide R(Y M) vs Y(R∘M) placement explicitly.
LT5 ECOSYSTEM ACCEPTANCE: package A (datatype + behaviour), B (a protocol), C extends a shared spec integrating them without
  editing A or B, and existing references inside the ecosystem see the final definitions. Needs a source path to another
  package's root, open types (LT2), coherent rebinding, a defined ecosystem scope.
LT6 PROMISES SEPARATED: `law` is checked code with a stated status (checked/unchecked/discharged), not silently retained;
  guardedness/productivity claims cover ALL demanded recursion in a turn, not only resident self-calls under perform.
Docs: OBJECTIVE-BEND overview roadmap is stale vs 259a2fb (activity ops registered); `&&` strict vs `||` lazy noted in the guide.


---

## OB-COMPLETION-20261005

<!-- source: OB-COMPLETION-20261005.md -->

## Objective Bend completion wave (2026-10-05) — P0, ahead of every other workboard row
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


# Appendix B — Literature notes


---

## LIT-W1-oo-calculus-typing

<!-- source: LIT-W1-oo-calculus-typing.md -->

## LIT-W1: OO calculus and typing literature against Objective Bend "Core4"

Worker: literature W1 (DEPUTY-GROUNDING). No code, no builds.
Corpus: `~/paperbin/objective-bend-grounding/<slug>.pdf` plus `<slug>.txt` (pdftotext -layout; Wand 1987, Flatt et al. 1998 and Pierce-Turner were scans or font-garbled and were OCR'd with tesseract, so quotes from them are OCR-grade and may carry typos).

Tags: **READ** = read in the text at the cited place. **INFERRED** = my reasoning or memory, not read at the place cited.

Vocabulary map used throughout (Core4 on the left):
- spec `C -> V -> W` = Cook's *wrapper* (self -> super -> result) = Bracha-Cook *mixin* = Pierce-Turner *class* (a record abstracted on self).
- `fix spec inherited` = Cook's `fix(generator)`, Pierce-Turner's `rec`.
- Self rigid with lower bound `Self has {...}` = Cook-Hill-Canning `t <= F[t]` (F-bound) = Bruce's `MyType` with the assumption `MyType <# ObjectType tau` = Rémy-Vouillon open row in the self type = Abadi-Cardelli's `Self <: Q`.

---

### 0. Corpus caveats (what was and was not obtained)

- Abadi & Cardelli, *A Theory of Objects* (1996): the book was NOT obtained (Springer blocked, no Anna's md5 reachable). Read instead, by the same authors: (a) "A Theory of Primitive Objects: Second-Order Systems" (SCP/ESOP, 1995 draft, `cardelli-primobj-2nd`), §2.5, §3.4, §5; (b) their 1996 OOPSLA tutorial slides (`abadi-cardelli-oopsla-tutorial`), slides 59-64, 85-86. The Springer chapter list confirms book chapters 14 "Second-Order Calculi", 18 "Imperative Calculi with Self Types", 20 "A Second-Order Language" (title-level only; contents not read). I give NO other book chapter numbers.
- Wand 1989 LICS (not "1991 Info & Comp") is what `wand-concat91.pdf` actually contains (header `CH2753-2/89`, pp. 92-97). The journal version (Inf. & Comp. 93(1), 1991) was not read.
- Rémy 1989: abstract and introduction READ; the Pre/Abs-flag machinery INFERRED from memory, but Wand's paper (§4) describes the `pres/absent` field encoding and attributes it to Rémy (READ).
- Bruce PolyTOIL: the file is the TOPLAS 25(2), 2003 journal version (pp. 225-290) of the ECOOP '95 paper; pp. 225-235 read. Bruce's 2002 book read via Ch. 16 and Ch. 18.
- Pierce-Turner: the PDF is the 1993 preprint (header "J. Functional Programming 1 (1)... 1993"); the published version is JFP 4(2):207-247, 1994.
- Rémy-Vouillon: the file is "Objective ML: An effective object-oriented extension to ML", TAPOS 4(1), 1998 (the paper the task calls "Objective ML, TAPOS 1998").
- Odersky-Zenger: pdftotext without layout; §2.2, §2.3, §4 read.

---

### 1. Cook 1989 thesis; Cook & Palsberg, "A denotational semantics of inheritance and its correctness" (OOPSLA 1989; Inf. & Comput. 114(2), 1994)

Read: Cook-Palsberg §3.1-3.2 (PDF pp. 4-8) and §4.3 (p. 12). Thesis (Brown 1989, `cook-thesis89`) §2.5, §2.6 (pp. 17-19) and §4.1-4.4 (pp. 30-32).

Mechanism (READ). A class is a *generator* `G : Behavior -> Behavior`; an instance is its fixed point. A subclass is a *wrapper* `W : self -> super -> modification-record`, and "wrapper application" is `W ⊛ G = λ self. (W(self)(G(self))) ⊕ G(self)` (Cook-Palsberg §3.2): self is distributed to both wrapper and parent, and the wrapper's record is `⊕`-overlaid on the parent's. The wrapper "contains just the information in the subclass definition". Correctness (Thm 2, `send = behave`) relates the method-lookup semantics to `fix` of the composed generators (§4.4). The thesis §4.1 types a generator as `σ -> τ`: σ = the type of self-reference ("the assumptions the generator makes about its fixed point"), τ = the type of the fixed point; §4.2: a generator is *consistent* (has a fixed point) iff τ <= σ, and abstract classes are exactly the inconsistent generators; §4.3: "The type of self-reference of an inheritor must be a subtype of the type of self-reference of its parents" and "it is not necessary for the child external interface to be a subtype of the parent external interface". Thesis §2.5: multiple inheritance = wrapper over a *tuple* of parents, "the wrapper is responsible for resolution of all conflicts"; strict variant `⊕⊥` makes conflicts error values. Thesis §2.6: "generalized inheritance" `G' = M ∘ G ∘ P` lets the *self passed to the parent* be modified (renaming).

Bearing on Objective Bend: **AGREES, and SHARPENS.**
- Core4's `C -> V -> W` is Cook's wrapper with one difference (READ vs the Core4 statement): Cook's wrapper returns only the *delta* and the application operator does the `⊕`; Core4's extension takes the *whole* super and returns the *whole* result, so `mix` is plain composition and no `⊕` lives in the operator. INFERRED consequence: `mix(mix a b) c` and `mix a (mix b c)` both equal `λs.λu. c s (b s (a s u))`, so `mix` is associative on the nose, with no hypothesis on `⊕` (Bracha-Cook need "assuming ⊕ is associative", see §2).
- Thesis §4.2/4.3 is the classical statement of what Core4's homogeneous `fix` (target -> inherited -> target) specializes: consistency `τ <= σ` collapses to `τ = σ` when subtyping is dropped. The thesis's observation that the child's external type need not be a subtype of the parent's is what licenses `-> Super with {y: Nat}`.
- Risk/question: the thesis explicitly flags `M ∘ G ∘ P` (self-modification before the parent sees it) as useful for renaming; Core4 passes the *same* self to every layer (INFERRED from the `mix` definition). That is a deliberate narrowing; renaming/hiding of inherited members has to be a different mechanism.
- Thesis §4.4 warns inheritance breaks encapsulation (the inheritor sees the parent's self-reference pattern). Core4's metadata (`SpecMeta`) exposes construction history, which is a second channel of the same kind.

### 2. Bracha & Cook, "Mixin-based inheritance" (OOPSLA/ECOOP 1990)

Read: whole paper; §3.1 (critique of linearization) and §4 ("Inheritance as composition of mixins") closely.

Mechanism (READ). "Mixins are the basis ... Inheritance is then formulated as composition of mixins." The composition operator is `M1 ⋆ M2 = fun(i) M1(M2(i) ⊕ i) ⊕ M2(i)`; "In case of conflict, ⋆ gives priority to the first parameter. In M1, super/inner is bound ... to M2. In M2, super/inner is bound to the formal parameter i of the result" (§4). "Assuming the basic attribute combination operator ⊕ is associative, ⋆ is associative." There is "no need for implicit linearization: a programmer would explicitly select the order of all mixin components. If a component is composed more than once it will appear as multiple copies in the result; duplication is avoided by explicitly applying two components to a shared parent." §3.1 criticizes CLOS linearization as "violating encapsulation": the relationship between a class and its declared parents "may be modified during linearization" (Graduate lands between Doctor and Person against Doctor's declared parent).

Bearing: **AGREES on the primitive, DISAGREES on two conventions.**
- ORDER (READ + INFERRED): Bracha-Cook's `⋆` is *most-specific-first*: first argument wins and is the outer layer. Core4's `mix lower upper = λself.λsuper. upper self (lower self super)` makes `upper` outer, i.e. the same operator as `M1 ⋆ M2` with arguments flipped, and the task statement says `compose` is least-specific-first (rightmost wins). So Core4 `mix` is "Unix pipeline order"; Bracha-Cook, Flatt et al. (§10 below) and Faré's POOF `(mix c p)` (READ in `~/dev/fareoo/sources/poof-paper.md` l.29: `(lambda (f b) (c f (p f b)))`, c outer) are all most-specific-first. Not wrong, but `extends` (most-specific-first) and `compose` (least-specific-first) pointing opposite ways inside one language is a documented foot-gun the literature does not share.
- DIAMONDS (READ): Bracha-Cook *duplicate* a twice-composed component ("multiple copies") and dedup only by explicit shared parent; Core4's C4 dedups by qualified declaration key. These are different semantics for `compose(a, compose(a, b))` vs `extends` linearization, which is exactly the compose/extends asymmetry the task describes; the literature's position is that the explicit-order primitive does not dedup.
- Risk: §3.1's complaint (linearization rewrites declared parent relationships) applies to C4 as much as C3; C4's suffix property mitigates for declared suffixes only (see §11).

### 3. Canning-Cook-Hill-Olthoff-Mitchell, "F-bounded polymorphism for object-oriented programming" (FPCA 1989); Cook-Hill-Canning, "Inheritance is not subtyping" (POPL 1990)

Read: FPCA '89 §3.3, §4.1-4.3, §5 (pdftotext, two-column; no page numbers in the text, section numbers given). POPL '90 §1 (pp. 125-126), §3.1-3.2 (pp. 127-128), conclusion (p. 134).

Mechanism (READ). A type `A` satisfies the F-bound `t <= F[t]` when `A <= F[A]`: "A must have the methods a_i and these methods must have arguments as specified by σ_i[A], which are defined in terms of A" (FPCA §4.1). The problem it solves: `Number` is not a subtype of `PartialOrder = {lesseq: PartialOrder -> Bool}` (negative recursion), yet `minimum : ∀t <= F-PartialOrder[t]. t -> t -> t` works (§4.3). POPL '90 §3.2 is the *template* design: "abstracting the type of self and replacing type recursion by type-dependency. The type recursion is reintroduced when the object is constructed." A parent is `P : ∀t <= F[t]. t -> F[t]`; a child is `C : ∀t <= G[t]. t -> G[t]` with `G[t] <= F[t]` for all t; "Object instantiation must now include the type of the object being created, as in Y(P[σ])". §3.1 shows the failure of "simple typing": a child redefining the binary method `eq` (reading `o.b`) cannot be typed because `τ1 ⊄ σ'`. The title's claim: an inherited type "is not necessarily a subtype of the type from which it was derived" (§1, p. 126), and F-bounded functions "prevent objects with different inherited types from being mixed together".

Bearing: **AGREES (this is the strongest literature match for the template design) and SHARPENS.**
- Core4's `extension AddY[Self has {x: Nat}, ...]` + "each use re-instantiated with concrete types at `fix`" is POPL '90's `∀t <= F[t]. t -> F[t]` plus `Y(P[σ])`, with "has" in place of "<=" (READ, §3.2; the mapping is INFERRED).
- Key precision (READ): the condition is `G[t] <= F[t]` *for all t*, with the same `t` on both sides (self-referential occurrences are identified). Under Core4 the entailment `Self has {heavier(other: Self) -> Self}` must be discharged against the *final* concrete type S with `Self := S` substituted on both sides, i.e. F-bound entailment, not entailment against the bound's own expansion. Where Core4 says "`Self` may not be used where exactly {x: Nat} is expected", this is the same refusal as Cook's `τ1 ⊄ σ`.
- Heterogeneity: F-bounded quantification keeps differently-extended objects unmixable (READ). Core4 states heterogeneity lives in `mix`; the literature's price for that is precisely "no mixed collections" (see §8, hash types).
- Question: FPCA §4.1 bounds a recursive type by `A <= F[A]` using *subtyping* on the record part (width). Core4 has no subtyping, so "has" must be a purpose-built width-only relation on rows. That is Bruce's `<#` (§8), which is the thing to cite for its soundness.

### 4. Abadi & Cardelli, *A Theory of Objects* (1996) (via the 1995 second-order paper and the 1996 tutorial; see caveat §0)

Read: second-order paper §2.5 (p. 5), §3.4 "The Self Quantifier" (pp. 9-10), §5.1 "Overriding from the Outside" and §5.2 "Recoup" (pp. 18-19). Tutorial slides 59-64 (classes and pre-methods), 85-86 (Self types, "inheritance ... without subtyping"). Book chapters: not read (§0).

Mechanism (READ). A *class* is an object with a `new` generator plus "pre-methods" `li = λ(xi) bi`; "Inheritance is the reuse of pre-methods" (tutorial slides 60-61). An object has type `[li:Bi]` "if it has at least the methods li, with a self parameter of some type A <: [li:Bi]" (slide 63): a pre-method's self is a *bounded* variable. Object types are invariant, so `P2 <: P1` fails for movable points, and "if we somehow allow P2 <: P1, we obtain an inconsistency" (paper §2.5). Their fix is the Self quantifier `ς(X)B = μ(Y)∃(X<:Y)B`, "recursion going through the bound" (§3.4), which yields "inheritance for methods that return self or that take arguments of the type of self ('binary methods'), but without subtyping" (slide 86). Constructing a `ς`-object is easy because methods need work only for the actual type; *overriding from the outside* is not: "the new method must work for any possible B<:A, because o might have been built as an element of B" (§5.1); "we cannot synthesize a value of type Self from scratch"; the naive rule is unsound (the `r2`/`R1 <: R2` example) because the self available at override time "may be shorter than the subtype used originally". Their fix is a `recoup` method returning self, with a run-time invariant (§5.2).

Bearing: **AGREES with the rigid-Self-with-lower-bound design; raises one specific risk.**
- A rigid Self bounded below, usable only through its bound, with creation only at the closing `fix`, is exactly §3.4/§5.1's treatment (READ for the A-C side; mapping INFERRED).
- Soundness hazard A-C found does NOT arise in Core4 for the reason they identify: it needs *subsumption* to build an object from a proper subtype of its own type. Core4 has none and instantiates at exact concrete types at `fix` (INFERRED). That is a real benefit of dropping subtyping, worth stating as a design invariant ("every value's static type is its exact type") because Bruce's `breakIt` counterexample (§8) is the same bug.
- Residual risk (INFERRED): `-> Super with {y: Nat}` *does* synthesize a value whose type is a function of the rigid `Super`. That is sound only if the type system treats `Super with {y}` as row extension of the unknown tail with presence/absence information (Rémy, Wand §5); see Sharpest question 1.

### 5. Wand 1987 LICS, "Complete type inference for simple objects"; Wand 1989/91, "Type inference for record concatenation and multiple inheritance"

Read: 1987 (OCR) abstract and the comparison with Cardelli's C84, PDF pp. 6-7; 1989 LICS abstract, §3 (objects as record operations, p. 93), §5 "Dealing with concatenation".

Mechanism (READ). 1987: records are typed with row variables; inheritance is polymorphism: a function `twicea = λu. 2 × (u.a)` "may be applied to any object (that is, any record) containing an a component" and so "to any descendant of Π((a, int))", with principal types by let-polymorphism. Wand closes with a warning about *structural* inheritance: "there is no guarantee that the id-number fields for submarines and weapons systems will be compatible", and "many real object-oriented systems use name inheritance, in which the inheritance can be more tightly controlled" (OCR, p. 7). 1989 §3 encodes a class as `λ(z1..zn). λself. (P(Q..) self) with [a1 = M1; ...]` and notes "we must be careful ... to make sure that in any instance of this class, self in the methods of the parent class is bound to the entire object, not just the portion" (the same wrapper insight as Cook); with this encoding "classes are ... values which can be passed as parameters". §5: with record *concatenation* "it is impossible to assign a principal type"; `λxy.((x ‖ y).a + 1)` has two incomparable types (`Π(absent) -> Π(pres(int)) -> int` and the reverse), the fix is "a finite complete set of types" generated by disjunctions, "as large as 2^{nk}" (n labels, k concatenations): "a reflection of a real difficulty in object-oriented programming systems: systems with multiple inheritance go to great lengths to determine from which ancestor a particular method is inherited."

Bearing: **SHARPENS the case for templates over polymorphic core terms.**
- Core4's `extend` (first match wins, i.e. overlay) is Wand's concatenation, and Wand's theorem is the literature's reason a single polymorphic core type for it does not exist (READ). Core4's choice (check the template once with Self rigid; type each use by re-instantiation at concrete types in a closed program) is the "finite complete set of types" idea realized by *instantiation* instead of by a disjunctive type scheme (mapping INFERRED). That is a genuine point in favor.
- Wand's 1987 closing caution maps onto Core4's qualified identity: shared field names alone do not mean compatible fields. Core4's "identity = qualified declaration key" is the "name inheritance" position (INFERRED).
- Risk: because shadowing is first-match-wins, whether `Super with {y: Nat}` over a rigid Super whose bound is silent on `y` is typed as "overwrite" or "add" is a concatenation-style ambiguity, the exact thing that destroys principality.

### 6. Rémy 1989 POPL, "Typechecking records and variants in a natural extension of ML"; Rémy & Vouillon, "Objective ML" (TAPOS 1998)

Read: Rémy §abstract and introduction (pp. 77-78: "replacing inclusion rules by extra information in record types"). Rémy-Vouillon §3 "Classes" (typing rules, fig. 3), §4 "Coercion", Appendix 3 "Binary methods" (pp. 17-18), note 2 (p. 15).

Mechanism (READ). Rémy 1989 abstract: "We solve this problem by giving an ordinary status to records without any ad hoc assertions, replacing inclusion rules by extra information in record types", giving ML-style polymorphism over records. Objective ML: "Row variables provide parametric polymorphism for method invocation. Instead of using row variables, many other languages use subtyping polymorphism" and "row variables are essential here to keep type inference". A class type is `sig (τ_self) φ end`: "the type τ_y of self (i.e. the type an object of this class would have)" plus field/method bindings; in the concrete syntax a method in τ_self but not in φ "is flagged virtual". Binary methods: `class virtual comparable ... virtual leq : α -> bool`; "`int_comparable = rec α.⟨leq: α -> bool; getx: int⟩` is not a subtype of `comparable`: inheritance is not subtyping", yet `int_comparable` "is an instance of `ρ#comparable`"; "the type of self is kept open while typing classes: adding the method `getx` to class `comparable` simply amounts to instantiating the row variable in the type of self." The class closes the row only at instantiation (`new`): "Otherwise, the class is virtual and can only be inherited". Subtyping is available only as explicit coercion (§4). Note 2: redefined methods must keep the same type; relaxing it to subtypes "would lose a property we believe important: ... the type of self in a class unifies with the type of any object of a subclass". Classes are second-class: "it would be possible to make them first-class ... however, class types should be provided explicitly in abstractions. The little gain in practice is probably not worth the complication" (§3).

Bearing: **AGREES, and Objective ML is the closest implemented precedent.**
- "Self is an open row, closed at instantiation; inheritance instantiates the row variable; binary methods stay binary; no subtyping" is Core4's design (READ + INFERRED mapping). The row tail is Core4's "bounded type variables keep row tails".
- Second-class classes with explicit class types (READ, §3) is the same trade as "open templates are second-class".
- One divergence to name: OCaml uses *equi-recursive* object types (`rec α.⟨...⟩`) with unification; Core4 uses *nominal* recursive records (`record Node: heavier(other: Node) -> Node`) plus rigid Self. The literature gives no precedent for how a nominal recursive record is identified with a structural final Self at an F-bound (see Sharpest question 2).
- Note 2's rationale (method redefinition must preserve type so that Self unifies) is the OCaml analogue of "templates are checked once"; Core4's `-> Super with {y}` signature should be examined for the same invariance on overridden members.

### 7. Pierce & Turner, "Simple type-theoretic foundations for object-oriented programming" (JFP 4(2), 1994; 1993 preprint read)

Read: §1 (pp. 1-2), §5-6 (pp. 11-17), §10 (pp. 30-31).

Mechanism (READ). Objects are existentials over a hidden state type (`Point = ∃Rep. {state: Rep, methods: {getX: Rep -> Int, ...}}`); inheritance is "just a matter of programming". A class is "a record of methods, abstracted on a record `self` of methods with the same types", instantiated "by supplying it as the argument to the polymorphic fixed point operator `rec`"; "classes themselves are values, not types", and "the type of a colored point class is not a subtype of the type of a point class, although the type of colored point objects is a subtype of the type of point objects" (§6). Classes polymorphic in the final representation type pass `get`/`put` extractors (`FinalR`). §10: the model "supports neither directly" strong binary methods and supports weak ones only via the recursive-type route; strong binary methods need "partially abstract types".

Bearing: **SHARPENS (supports first-order metadata; flags binary-method limits of existential encodings).**
- Their class-as-record-of-methods-abstracted-on-self with `rec` is Core4's spec + `fix` (READ; mapping INFERRED).
- Why `SpecMeta` as first-order data rather than an existential (INFERRED, not claimed by the paper): packing a spec existentially hides its construction history, which is exactly what reflection needs to expose; and §10 shows existential encodings pay a price on binary methods (strong binary methods are unsupported), which Core4's F-bounds are designed to support. So a first-order sum for metadata is consistent with, but not required by, this paper.
- Their `FinalR`/`get`/`put` trick is the pre-F-bound way to make a class polymorphic in the final self; it is evidence that "inheritance at a recursive type" costs a family of coherence arguments the F-bound/MyType systems avoid.

### 8. Bruce, *Foundations of Object-Oriented Languages* (MIT Press 2002) Ch. 16 & 18; Bruce-Schuett-van-Gent-Fiech, "PolyTOIL" (ECOOP 1995; TOPLAS 25(2) 2003)

Read: book §16.1.3 "Loss of subtyping, gain of matching" (pp. 306-309), §16.2 incl. Fig. 16.9 class rule and Lemma 16.2.2 (pp. 314-315), §18.1 "Can we drop subtyping?" (pp. 349-351). PolyTOIL pp. 225-235 (abstract, §1-2: matching, MyType, the `breakIt` example).

Mechanism (READ). `MyType` names the type of self; "Object type T *matches* object type U iff every method in U also occurs in T, and the types of corresponding methods are in the subtype relation ... In determining matching, occurrences of MyType in both types are treated as being the same. Thus DoubleNodeType matches NodeType, even though they are not subtypes" (Def. 16.1.2, p. 309). Soundness discipline, in Bruce's words (PolyTOIL p. 231): "methods are type-checked under the assumption that MyType <# ObjectType τ. ... By type-checking under this assumption, we need not worry about the type safety of the method when it is inherited in subclasses ... the types of objects generated from subclasses will be guaranteed to match ObjectType τ." In the class rule (Fig. 16.9), methods are checked against an abstract type function `M'` constrained by `M' <# M`, with a separate `SelfType` (instance variables visible) and `close: SelfType -> MT` to turn self into the hidden-state object type (e.g. `newNext.setPrevious(close(self))`). Subtyping is lost exactly when MyType occurs contravariantly (as a parameter): "if MyType only occurs in the return types of methods, the corresponding object types will be in the subtype relation" (p. 308). The unsoundness being excluded (PolyTOIL p. 234): `breakIt(sn1, sn2: NodeType){sn1.setNext(sn2)}` called with a `DNodeType` receiver would run `setNext` expecting a `DNodeType` argument; "PolyTOIL only allows the user to deduce that DNodeType <# NodeType". Ch. 18 §18.1: "Virtually every use of subtype-bounded polymorphism can be replaced by match-bounded polymorphism"; dropping subtyping costs: (1) heterogeneous collections ("an array of graphical objects of different types ... This would not be possible if we only had matching"), (2) a function parameter "that supports at least the methods of Graphical" must become `∀(G <# Graphical). G -> Void`, "more painful for the programmer"; the repair is *hash types* `#T` (the existential over `G <# T`). Covariant specialization of an instance variable (CircleClass/ColorCircleClass) is not handled by MyType and needs a parameterized class (§18.1, p. 350).

Bearing: **AGREES (this is the exact analogue, and it supplies the soundness conditions), and DISAGREES only on what Core4 omits.**
- The conditions Bruce needs for binary methods, to be mirrored in Core4's checker (READ): (a) method bodies are checked only under the matching assumption about self, never under an alias of the bound's expansion; (b) a subclass's object type must *match* the parent's with MyType identified across the two; (c) static types of values are not widened, so a value statically `NodeType` is exactly `NodeType` (no `breakIt`); (d) self is distinct from the hidden-state-free object type, with an explicit conversion (`close`).
- Core4's "rigid Self is not an alias of its row; may not be used where exactly {x: Nat} is expected" is (a)+(d): READ (Bruce side) + INFERRED (mapping).
- What dropping subtyping costs here (READ, §18.1): hash types or equivalent. Core4 has second-class open templates and no existentials, so it forgoes exactly (1) and (2). That is a deliberate trade, but it is the literature's stated cost, not a free lunch.
- Open point: Bruce's soundness argument is by translation to a higher-order calculus with subject reduction; PolyTOIL claims "provably typesafe via subject reduction". Core4 has a proof-producing checker but no stated substitution lemma for template re-instantiation (Sharpest question 1).

### 9. Odersky & Zenger, "Scalable component abstractions" (OOPSLA 2005)

Read: §2.2 "Class linearization", §2.3 self-types, §4 (selftype abstraction), the paragraphs around "Selftypes can be arbitrary".

Mechanism (READ). A self-type annotation (`class BaseNode requires Node`) sets "the type of `this` inside the class" and is "the key construct for lifting static systems to component-based systems". Soundness: "(1) the selftype of a class must be a subtype of the selftypes of all its base classes, (2) when instantiating a class in a `new` expression, it is checked that the selftype of the class is a supertype of the type of the object being created." Selftype abstraction is "a more concise alternative to member abstraction... somewhat akin to the difference between structural and nominal typing"; a compound selftype `A requires (A with B with C)` replaces imports. Linearization (§2.2): `L(C) = {C} +~ L(Cn) +~ ... +~ L(C1)` (right-to-left, duplicates removed from the *left* operand), which "always contains the linearization of its direct superclass as a suffix", but "linearization in Scala is not monotonic".

Bearing: **AGREES with `requires` = Self bound; SHARPENS the soundness pair.**
- Core4's `requires m(...) -> R` is a selftype member constraint; `fix` discharging requirements from the seed is O-Z's rule (2) (check at instantiation that the concrete type meets the selftype) (READ + INFERRED mapping). Rule (1) (selftype of a subclass includes those of its bases) corresponds to the template entailment `G[t] <= F[t]` (§3).
- O-Z note selftype abstraction trades precision for concision; Core4's `requires m(...) -> R` is member-level (the precise form), whereas `Self has {...}` is bound-level; both exist in Core4, and O-Z say they are interchangeable up to verbosity (READ).
- Useful fact for C4: Scala achieves the suffix property by removing duplicates from the left, at the cost of monotonicity (READ). C4's contribution is having both (Faré, §11).

### 10. Flatt-Krishnamurthi-Felleisen, "Classes and mixins" (POPL 1998); Dreyer & Rossberg, "Mixin' up the ML module system" (ICFP 2008); Hirschowitz & Leroy, "Mixin modules in a call-by-value setting" (ESOP 2002)

Read: FKF §3-§4.4 (OCR; "inheritance interface", `compose`, "viewable as", ambiguity discussion); MixML abstract, §1.2-1.3, §2 linking, "Dynamic Semantics and Type Soundness"; Hirschowitz-Leroy abstract, §1, §3 (dependency graphs).

Mechanism (READ).
- FKF: a MixedJava mixin `extends` an *inheritance interface* (a bound on its super, not a class) and `implements` an interface; "Composition is allowed only when the right-hand mixin implements the left-hand mixin's inheritance interface"; "Method declarations in the left-hand mixin override declarations in the right-hand mixin". Mixins are declared definitions composed at definition level, not run-time values. A diamond yields duplication: `LockedMagic` "is a subtype of `Secure`, but it contains two copies of `Secure`", so subsumption is ambiguous and replaced by a restricted "viewable as" relation.
- MixML: linking performs "mixin composition ... in the style of Bracha's merge operator, assuming they are compatible"; MixML "does not attempt to support any form of overriding"; "mixin composition is essentially a bidirectional generalization of ML-style signature matching"; dynamics by "evidence translation" with a "backpatching semantics, using lazy reference cells to enable recursive linking".
- Hirschowitz-Leroy: call-by-name CMS "puts no restrictions on recursive definitions, allowing ill-founded ones such as `let rec x = 2 * y and y = x + 1`", and "illegal recursive definitions can appear a posteriori when we take the sum A + B of two mixin modules, at a time where only the signatures of A and B are known". Their remedy: dependency graphs in mixin signatures, edges labeled 0 (immediate) or 1 (under a lambda), "all cycles ... must be composed of 1 edges only", and "the sum of two safe graphs is not necessarily safe" so the typing rule for sum re-checks safety.

Bearing: **SHARPENS (three concrete points).**
1. `Super has {...}` is FKF's inheritance interface; "compose allowed iff the right side implements the left side's interface" is Core4's bound entailment check at `mix` (READ + INFERRED mapping). FKF's mixins are second-class definitions; Core4's open templates being second-class agrees with FKF and Rémy-Vouillon (§6) and is the common position of every typed system read here that has inheritance interfaces.
2. Core4's "the package as a record knot" (records of separate lazy suspensions tied by one heap address) is MixML's backpatching with lazy cells (READ + INFERRED). MixML needs a type system that handles the "cross-eyed double vision" interaction of recursion and sealing; Core4 has no sealing/abstraction of fields, so it avoids that class (INFERRED), but it also gets no type-level guarantee about the knot.
3. Hirschowitz-Leroy: composition of independently checked pieces can create ill-founded recursion not visible from either piece's signature. In Core4, call-by-need on lazy field suspensions turns that into a runtime black-hole/divergence rather than a type error; whether the soundness theorem covers it (progress "or diverges") is not stated in the brief (Sharpest question 3).
- Conflict semantics differ: MixML merges (error on overlap), FKF/Bracha-Cook/Core4 override. Core4 is on the override side with FKF, but with the opposite argument order (§2).

### 11. Barrett, Cassels, Haahr, Moon, Playford, Withington, "A monotonic superclass linearization for Dylan" (OOPSLA 1996); Faré's C4 (read in `ltuo-readable.txt` §7.4.4)

Read: C3 paper "Computing linearizations" and "Why Monotonicity?" sections (PDF pp. 3-5). Faré: lines 3760, 3781, 3791 of `~/dev/fareoo/raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt` ("Lambda: the Ultimate Object", Rideau et al.).

Mechanism (READ). C3: "The linearization used in Dylan merges the local precedence order of the class being defined with the linearizations of its direct superclasses"; "A monotonic linearization is one in which every property inherited by a class is inherited or defined by one of its direct superclasses"; "If there is no possible merged output sequence which is consistent with all the input sequences, the class heterarchy is inconsistent." Tie-breaking: select the class "that has a direct subclass closest to the end of the output sequence" (CLOS/Dylan rule). The C3 paper nowhere states a suffix property. Faré (l.3791): "monotonicity states that the precedence list of an ancestor must be an ordered subset of that of the specification, though its elements need not be consecutive"; "I define my own algorithm C4 as an extension of C3, that in addition to the constraints of C3, also respects the suffix property for specifications that are declared as suffixes, and otherwise exempts suffix specifications and their ancestors from the extended precedence constraint", via a per-spec `suffix?` Boolean.

Bearing: **AGREES, with a scoping correction.**
- Core4's "C3 + suffix property" should say *for specs declared suffix* (READ in Faré). Subsequence-monotonicity (C3) is strictly weaker than suffix; so C4 rejects some C3-valid hierarchies only when a declared-suffix spec is involved. The brief's phrasing could be read as "all specs are suffixes".
- Scala (§9) and Ruby reach the suffix property without C3's local-order/monotonicity guarantee (READ in Faré l.3760, O-Z §2.2); C4 is the claim of having both.
- Risk (INFERRED): the C3 paper is about *multimethod dispatch order*; the order here also decides override priority and `combine`/`around` nesting. `around` + C3 interplay is not in this paper.

---

### Sharpest questions

1. **Template instantiation soundness: is there a substitution lemma, and does it survive `Super with {y}` and binary methods?** Every F-bound/MyType system read (Cook-Hill-Canning §3.2 `G[t] <= F[t]` for all t; Bruce Fig. 16.9 `M' <# M`) discharges soundness by *one* theorem: a body checked once under an abstract self with a matching bound stays well-typed under every instantiation satisfying the bound, with the self occurrences identified on both sides. Core4's "checked once with Self rigid; re-instantiated at `fix`" needs exactly that lemma; the brief states the design, not the lemma. Two concrete failure candidates: (a) `-> Super with {y: Nat}` where Super's bound is silent on `y` and `extend` is first-match-wins: a Super whose real row already has `y: Bool` changes the result row's `y` type, which is Wand's concatenation non-principality (§5) and why Rémy needs presence/absence information; (b) a bound that mentions Self contravariantly (`heavier(other: Self)`), where entailment must be checked with Self := S on both sides, not against the bound's own expansion. Is (a) rejected, typed as overwrite with an explicit tail-lacks-`y` constraint, or deferred to instantiation (in which case "checked once" is weaker than claimed)?

2. **Nominal recursive records vs structural final Self at an F-bound.** OCaml (§6) and Cook/Bruce (§3, §8) tie the knot with equi-recursive or `ς`/MyType types so that `Self`'s occurrences inside the bound and the concrete final type are *the same type by construction*. Core4 has `record Node: heavier(other: Node) -> Node` (nominal) and `Self has {heavier(other: Self) -> Self}` (rigid). When Self is instantiated at the fix's concrete row (Node's fields plus `weight`), is `Self` equal to `Node`, to a fresh anonymous recursive row, or neither? If it is not `Node`, a `Node`-typed parameter cannot receive the final value, and if it is `Node` the extra fields are exactly Bruce's hidden-state/`close` distinction (a `SelfType` that is not the object type). No source read covers a nominal-recursion variant.

3. **What does dropping subtyping cost, and is the cost accepted?** Bruce §18.1 states it: no heterogeneous collections of "things supporting {m}" and no ordinary function parameters of such a type without hash types (existential over a matching bound) or an explicit `∀ G <# T` parameter; Core4's open templates are second-class, so neither is available. Cook-Hill-Canning make the same point from the other side (F-bounded functions keep differently-extended objects unmixable). Concretely: how does Core4 express a registry/list of specs or objects with different final types, a callback accepting "any value supporting `{draw}`", or `Specification<T>` over varying T? If the answer is "monomorphize at the closed program", say so; if it is "a hash type later", the second-class-templates claim is provisional.

4. **Soundness with composition-created recursion.** Hirschowitz-Leroy (§10) show that mixin composition can create ill-founded recursive definitions invisible in either component's signature, and that a modular check must carry dependency information in the signature ("the sum of two safe graphs is not necessarily safe"). Core4's call-by-need records of lazy suspensions make `x = self.y; y = self.x` a runtime loop, not a type error, and its templates are checked once. What exactly does the stated safety theorem guarantee: progress except for black-hole/divergence, or absence of field cycles? If the latter, where is the dependency analysis (it cannot be per-template); if the former, say so and consider whether `fix` should reject cyclic requirement discharges.

5. **Order and identity conventions: three places the design departs from every cited source at once.** (a) `mix lower upper`/`compose` is least-specific-first, but Bracha-Cook `⋆` (§2), FKF `compose` (§10) and Faré's own `(mix c p)` are most-specific-first (READ), while `extends` is most-specific-first in Core4 itself. (b) Bracha-Cook and FKF *duplicate* a component composed twice (diamond) and dedup only through an explicit shared parent; Core4 dedups by qualified key under `extends` but, as a function composition, `mix a (mix a b)` applies `a` twice (INFERRED from the definition). So behaviour-associativity holds (INFERRED, derivation in §1) but `extends`-linearization and `compose` give different results on diamonds, and `metadata(compose(a,b))` records history that linearization would have collapsed. (c) C4's suffix property applies only to specs declared suffix (§11). Which of these are intended, and is the diamond asymmetry between `extends` and `compose` specified, with a test, rather than only noted?


---

## LIT-W2-laziness-reflection-continuations

<!-- source: LIT-W2-laziness-reflection-continuations.md -->

## LIT-W2: laziness, effects-under-sharing, guardedness, reflection, serializable continuations

Worker W2, DEPUTY-GROUNDING (Mini swarm). Literature only; no builds, no code edits, no git.
Downloads: `~/paperbin/objective-bend-grounding/<name>.pdf` plus `<name>.txt` (`pdftotext -layout`).
Papers already in `~/paperbin/world-program-model/` are cited from there.

Tags: **READ** = I read that passage in the extracted text. **INFERRED** = my reasoning, or a secondhand report inside a paper I did read.
Page numbers are PDF page indices unless "printed" is stated. For the two-column layout PDFs I re-extracted without `-layout` to read in order.

### 0. Corpus status (what was actually obtained)

| Paper | Status |
|---|---|
| Launchbury 1993 | `launchbury-natural-semantics-lazy-1993.pdf`. Scanned, OCR is partly garbled. Read the legible passages; theorem statements taken from Breitner 2017, which restates them cleanly. |
| Sestoft 1997 | NOT OBTAINED (Cambridge, ResearchGate and author-site fetches all failed). Only reported secondhand by Breitner §2.3. Nothing below claims to have read Sestoft's machine. |
| Ariola/Felleisen/Maraist/Odersky/Wadler 1995 | NOT OBTAINED. Read Chang & Felleisen ESOP 2012 instead, which restates λ_af, its relation to call-by-name, and Launchbury. Secondhand for Ariola. |
| Breitner 2017 (JFP, adequacy) | `breitner-adequacy-launchbury-2017.pdf`. Read §1, §2.3, §3, §4.1-4.3. |
| Peyton Jones 2001 | `peytonjones-awkward-squad-2001.pdf`. Read §1, §2.6, §3.2-3.3. |
| Levy CBPV (HOSC 2006) | `levy-cbpv-hosc-2006.pdf`. Read §1, §2.2, §3, Fig 3, §7.2 and Fig 8. |
| McDermott & Mycroft, "Call-by-need effects via coeffects" | `mcdermott-call-by-need-effects-coeffects.pdf`. Read abstract and §1-2. Venue not stated in the text I read (INFERRED: Open Computer Science, 2018); cite by title and authors. |
| Nakano 2000 | `nakano-modality-recursion-2000.pdf`. Read §1. Math glyphs are lost in extraction; the prose is intact. |
| Atkey & McBride 2013 | `atkey-mcbride-productive-coprogramming-2013.pdf`. Read §1 (pp 1-3). |
| Abel & Pientka | `abel-pientka-copatterns-jfp-2015.pdf` is the JFP version (Wellfounded Recursion with Copatterns and Sized Types), not the ICFP 2013 paper. Read §1 and the bfs example. |
| Xia et al. 2020 ITrees | `xia-interaction-trees-2020.pdf`. Read §1-2 (Ret/Tau/Vis). Added: load-bearing for perform/resume. |
| Wand 1998 | `wand-fexprs-trivial-1998.pdf` (converted from the author's .ps). Read in full. |
| Smith 1984 | `smith-reflection-semantics-lisp-1984.pdf` (2009 author reprint of the POPL paper, pagination "RL·n"). Read the abstract, the causal-connection discussion, and the 3-Lisp reflective-procedure and reification passages. |
| Felleisen 1991 | `felleisen-expressive-power-1991.pdf`. Read §1, Thm 3.8, Thm 3.14. |
| Mitchell 1993 | NOT OBTAINED (Springer/ScienceDirect paywalled). Felleisen 1991 carries the equivalence-relative-to-language argument, so nothing is lost for our purpose. |
| Kiczales/des Rivières/Bobrow 1991 | `kiczales-amop-1991.pdf` is only the front matter and introduction (739 lines). Read the roadmap of Part I. |
| Cejtin/Jagannathan/Kelsey 1995 (Kali) | NOT OBTAINED. Termite (Scheme Workshop 2006) and Pettyjohn et al. are used instead for serializable continuations. |
| Burckhardt et al. 2021 | `~/paperbin/world-program-model/burckhardt-durable-functions-semantics-2021.pdf`. Read §3.5, §5-6, Lemmas 6.5-6.7, Thm 5.3, Thm 6.4. |
| Khan 2026 | `~/paperbin/world-program-model/khan-resume-means-resume-2026.pdf`. Read §3 in full, §4.2 liveness. Two-column layout; re-extracted in reading order. |
| Germain/Feeley/Monnier 2006 (Termite) | `germain-termite-scheme-2006.pdf`. Read §3.1-3.2, §4.9, §5 serialization notes. |
| Pettyjohn et al. 2005 | `pettyjohn-continuations-stack-inspection-2005.pdf`. Read abstract, §3.5, the digest-labelling paragraph. Added. |
| Ahman & Pretnar 2021 (in paperbin) | Abstract and §1 only. |
| Grosen et al. 2023 AARA (in paperbin) | Abstract only. First-order resource analysis; not load-bearing here. |
| Li, Xia, Weirich ICFP 2021, "Garden of Forking Paths" | Downloaded, §1 skimmed only. Pointer for cost of call-by-need (see Q3). |

Net: the call-by-name vs call-by-need equivalence, the value/computation split, productivity, reflection-and-equivalence and replay-based resume are all grounded in text I read. The Kali paper and Sestoft's machine are not.

---

### A. Laziness

#### A1. Launchbury 1993
John Launchbury, "A Natural Semantics for Lazy Evaluation", POPL 1993, pp 144-154.
Read: abstract, §1-2 (the `let f = λx. f x` black-hole discussion, p. 148), §5.2 (denotational semantics, Correctness §5.2.2, Adequacy §5.2.3). Correctness and adequacy statements via Breitner 2017.

Mechanism (READ). "The only computational structure we introduce is a set of bindings which corresponds closely to a heap." Application is restricted to a variable argument (`e x`), so every argument becomes a named heap binding. A `let` allocates bindings; evaluating a variable reduces its binding and writes the value back, so each binding is evaluated at most once. The judgement is `Γ : e ⇓ Δ : v`, heap in, heap out. Correctness is stated against a standard denotational semantics: `⟦e⟧{{Γ}} = ⟦v⟧{{Δ}}` (Breitner Thm 1). Adequacy: if `⟦e⟧{{Γ}} ≠ ⊥` then some `Δ, v` exist with `Γ : e ⇓ Δ : v` (Breitner Thm 3, §4). Launchbury notes that a self-dependent binding is a detected black hole only when the variable rule removes the binding during its own evaluation, and that the loop `let f = λx. f x in f 2` is not a black hole at all (p. 148). Breitner confirms that rule VAR "models blackholing by removing a binding from the heap during its evaluation" (§2.3.2).

Bearing on Objective Bend: **AGREE** on the overall shape, with three **SHARPEN**s.
1. Launchbury has native recursive `let`, so a cell may point to itself. This is the right ancestor of `fix` tying a heap address to itself, much closer than the Ariola-Felleisen calculi (see A3). The reference-vs-machine theorem in the design is a Launchbury correctness theorem with the heap-as-cell structure. READ.
2. Adequacy is existential: derivation exists iff denotation is not bottom, with no bound on derivation size. This matches "completeness is finite but has no resource bound". Breitner's resourced semantics is the only route in this literature to a step-indexed version (Lemma 8: `N⟦e⟧{{Γ}} r ≠ ⊥` implies a derivation) and the proof is hard (A2). If the design wants a bound it needs an explicit cost model; the machine step count is not given for free by the natural semantics. INFERRED.
3. Blackholing is a feature of the operational side that the denotation does not share. Breitner Lemma 6: only the weaker "denotational blackholing" holds. For OB: `bad = self.bad` forced is a blackhole in the machine and ⊥ in the reference, which agree as ground observations (no value), but any observer that can distinguish "blackhole" from "ran out of fuel" is outside the theorem. INFERRED.

#### A2. Breitner 2017
Joachim Breitner, "The Adequacy of Launchbury's Natural Semantics for Lazy Evaluation", J. Functional Programming 2017 (preprint). Read §1, §2.3, §3, §4.1-4.3.

Mechanism (READ). First rigorous, machine-checked (Isabelle) adequacy proof. It skips Launchbury's intermediate natural semantics and works with a resourced denotational semantics plus a change that "ensures that while evaluating an expression with finite resources, values on the heap are used with fewer resources" (§1). Two incidental findings matter: Launchbury's own Theorem 2 (correctness, generalized) "is false" as stated (§2.3.3), because an environment ρ carrying compatible but better information about a heap variable breaks `ρ ⊔ ⟦v⟧`; the fix is a right-biased update `++S`, and closedness of the judgement (`fv(Γ,e) ⊆ dom Γ ∪ L`) is required (§2.3.2).

Bearing: **SHARPEN**. The published, long-trusted correctness theorem for lazy heaps was false until formalised, and the failure was precisely about *which environment/heap the theorem quantifies over*. The OB theorem "a finished bounded machine run equals the reference evaluation for ground observations" has the same exposure: a statement about heaps is only as good as its side conditions (closedness, freshness, which cells the observation may read). Risk: state the quantifier over initial heaps/environments explicitly and make the Lean statement name it. Question: does the Lean theorem quantify over arbitrary initial heaps (the ρ in Breitner's counterexample) or only the empty or well-formed ones?

#### A3. Ariola/Felleisen et al. 1995, via Chang & Felleisen 2012
Primary (Ariola, Felleisen, Maraist, Odersky, Wadler, "A call-by-need lambda calculus", POPL 1995) NOT OBTAINED. Read instead: Stephen Chang and Matthias Felleisen, "The Call-by-need Lambda Calculus, Revisited", ESOP 2012 (arXiv 1201.3907), §1, §4.3, §5, §6.

Mechanism (READ, secondhand for Ariola). Call-by-need "evaluates an argument at most once, and only if needed" (p. 2). Ariola-Felleisen's λ_af "defines the same evaluation function as the call-by-name λ calculus" and Chang-Felleisen §5 shows λ_need equals Launchbury's semantics extensionally (Thm 4, `eval_need = eval_natural`, p. 18). Maraist-Odersky-Wadler's λ_mow is NOT equal: `eval_mow ≠ eval_name`, example `(λx.λy.x) Ω` (p. 4). Equivalence is stated for the evaluation function (does the closed program reach an answer, and which), and soundness is "with respect to observational equivalence" under contexts `C = [] | λx.C | C e | e C` (§4.3, Thm 3, p. 12). Recursion is explicitly out: "does not include an explicit letrec constructor for cyclic terms ... applying their solutions should pose no problems" (p. 19).

Bearing on the question asked ("what equivalence holds, and does it survive effects?"): **AGREE** that call-by-name is the right reference for ground, effect-free observations, with two caveats.
1. The result is extensional: same answers and same divergence, not same cost, not same cell-evaluation order. INFERRED from the statement. Nothing about intensional properties such as "one cell evaluated at most once" transfers to the reference.
2. None of these calculi contains effects; I found no effect or state discussion in the sections read. So the name-need equivalence does NOT demonstrably survive `perform`. The only direct treatment I found is McDermott-Mycroft (B3), which shows it fails.
3. Cyclic sharing (`fix`/letrec) is outside λ_af and λ_need as published; Core4's `fix` needs the Launchbury or Ariola-Blom cyclic setting. Question: which cyclic call-by-need calculus is the reference-vs-machine theorem anchored in?

---

### B. Laziness meets effects

#### B1. Peyton Jones 2001
Simon Peyton Jones, "Tackling the Awkward Squad: monadic input/output, concurrency, exceptions, and foreign-language calls in Haskell" (Marktoberdorf lecture notes, 2001). Read §1 (p. 2), §2.6 (p. 12), §3.2-3.3 (pp 16-17).

Mechanism (READ). "laziness and side effects are, from a practical point of view, incompatible" (p. 2): for `xs = [printChar 'a', printChar 'b']`, whether anything prints depends on whether elements are demanded. Haskell's answer is to make I/O actions values of type `IO a`; running them is a separate act. `unsafePerformIO :: IO a -> a` escapes this, and "Whenever you use it, you are promising the compiler that the timing of this I/O operation, relative to all the other I/O operations of the program, does not matter. You must undertake this proof obligation" (§2.6, p. 12). The semantics is stratified in two levels (§3.2, p. 16): an inner denotational semantics for pure terms, an outer labelled transition semantics for IO, and primitive IO operations are *values* ("No further work can be done on this term in the purely-functional world; it is time to hand it over to the outer, monadic semantics", p. 17).

Bearing: **AGREE, and SHARPEN the vocabulary.** `perform plan` yields a Plan to the host is exactly the stratification: pure kernel inside, effect transitions outside. And `unsafePerformIO` is exactly "perform under an update frame": it is the case where running an effect is demanded by forcing a shared thunk, so the effect's timing (and whether it happens at all) becomes an artefact of evaluation order. The `sharedEffect` refusal is the structural answer to the awkward-squad problem, where Haskell leaves it as an unchecked proof obligation. One distinction the paper draws and the design may be blurring: an IO *action* is a shareable value; it is *running* it that is not shareable. The design says "an activity type is never shareable". Question: is a Plan (the description) shareable while the running of an activity is not? See Q2.

#### B2. Levy, Call-by-push-value
Paul Blain Levy, "Call-By-Push-Value: Decomposing Call-By-Value And Call-By-Name", Higher-Order and Symbolic Computation 19, 2006. Read §1, §2.2, §3, Figs 2, 3, 8, §7.2.

Mechanism (READ). Two disjoint classes of term and of type: "a value is, whereas a computation does" (§3, p. 8). Value types `A ::= U B | Σ A_i | 1 | A×A`, computation types `B ::= F A | Π B_i | A → B`. "an identifier in CBPV can be bound only to a value, so it must have value type" (p. 8). `thunk M : U B` is a value; `force V : B` runs it; `return V : F A` and `M to x. N` sequence computations. The paper deliberately keeps "the distinction between a term (computation) and its thunk" (p. 8) and shows the monadic metalanguage erasing it is the problem (p. 7). Effects (divergence, `print c. M`, cell store) are computation-level (Fig 3, p. 10). CBN translates `M N` to `(thunk N^n)‘M^n`, a variable to `force x`, and `print c. M` to `print c. M^n` (Fig 8, p. 18); the CBN-to-CBPV relation is a bisimulation (Prop 7, p. 18). Forcing a `U B` thunk of an effectful computation re-runs its effects each time; CBPV has no memoisation (Levy does not treat call-by-need; I grep'd the text and found no mention; INFERRED that memoising is therefore only sound for effect-free `B`).

Bearing: **SHARPEN**, and this is the most useful structural reference for the design.
1. CBPV says exactly why effects force a value/computation split: a shared binding holds *values*; computations (anything that "does") are re-run when forced. A call-by-need cell memoising a computation is only sound if the computation is effect-free, i.e. its result is a value regardless of how many times it runs. "An activity type is never shareable" is the CBPV rule "no memo cell for an `F`-typed computation that performs". INFERRED.
2. CBPV places the line at **types**, not at runtime frames. The design instead refuses at runtime when `perform` is reached under an update frame. The type-based line is the cleaner one: cells may only hold terms whose type contains no effect (value types and pure `U B`), activities live only in sequenced (`to`/bind) positions, and `sharedEffect` becomes unreachable in well-typed programs. The runtime refusal is then defence in depth, not the contract. INFERRED.
3. CBPV permits a `U (F A)` value (a *suspended* activity) that can be stored, passed and forced many times, each re-performing. That is the Haskell reading (B1). The design's blanket "no effect can sit in a field/argument/payload" is stricter than CBPV: it forbids even storing a suspended activity. Decide deliberately whether Plans are values (storable, duplicable, run-many) or a linear resource (run once). If run-many, each forcing is a new perform and the nullifier story must be per-force. INFERRED.

#### B3. McDermott & Mycroft, call-by-need effects
Dylan McDermott and Alan Mycroft, "Call-by-need effects via coeffects" (title and authors as in the file; venue not read). Read abstract and §1-2 (p. 2).

Mechanism (READ). "Tracking effects is a harder problem for call-by-need than for call-by-value and call-by-name." With `inc` incrementing a counter: `let x = inc () in let y = inc () in y + x` increments twice, but `let x = inc () in let y = x in y + x` increments once, at the use of `y`. "In call-by-need, using one variable can change the effect of another." Under call-by-name both programs increment twice. The key difficulty is "determining where arguments and let-bound variables are evaluated", which they address with a coeffect system tracking the order of first use.

Bearing: **DISAGREE with the sufficiency of call-by-name as spec once `perform` is present.** With any effect that can occur while forcing a shared cell, call-by-name and call-by-need are observably different programs. The reference semantics (name) would perform at each use, the machine (need) at the first. The design avoids this *only* by refusing `perform` under an update frame. Therefore the equivalence theorem is necessarily conditional on "no perform reached while forcing a shared cell", and the reference semantics must say what it does in that case (see Q1). Note also the first-use order dependency: refusal is raised at the first force, which depends on evaluation order, so whether a program is refused is itself an evaluation-order-sensitive fact unless the reference semantics also has the notion. READ for the example; the application to OB is INFERRED.

---

### C. Guardedness and productivity

#### C1. Nakano 2000
Hiroshi Nakano, "A Modality for Recursion", LICS 2000. Read §1 (pp 1-3).

Mechanism (READ). A modality `●A` ("A holds one step later") makes self-reference sound: "as long as `X` occurs only in scopes of the modal operator in `A`, the interpretation of `X` is well-defined and given as a fixed point ... which is actually shown to be unique" (p. 3). Fixed-point combinators (Curry's Y) are typed through `●`. The motivating example is a specification `Nat` of objects with a binary method whose method takes another object of the same type, a self-referential specification where a careless but type-correct definition (`add'`) diverges while `add` does not: "the divergence is caused by a program which is supposed to satisfy the same specification" (p. 1). Types here carry convergence information, as in "specifications ... convergence of programs can be expressed by types" (p. 2).

Bearing: **AGREE**, and this is nearer to the design than the usual stream citation. Open recursion `mix`/`fix` over objects with self-reference is Nakano's own motivating case (self-referential object specifications, binary methods). The typed fixpoint is `fix : (●A → A) → A`; for specs this reads `spec : ●Self → Self ...`. The design's `{good = 7, bad = self.bad}.good` is `7` precisely because `good` does not use `self` in a position that must be evaluated now; Nakano's discipline would *reject* `bad`, while the design's laziness *accepts* it as a field that is ⊥ if forced. These are two different disciplines: total (reject) versus partial and lazy (accept, blackhole on forcing). Question: which does OB want for specs a resident actually ships? INFERRED for the mapping.

#### C2. Atkey & McBride 2013
Robert Atkey and Conor McBride, "Productive Coprogramming with Guarded Recursion", ICFP 2013. Read §1 (pp 1-3).

Mechanism (READ). Productivity "means that, even if a program generates an infinite amount of data, each piece will be generated in finite time" (abstract). Guardedness is moved into types via `▷A` ("a value of A that is only available tomorrow", p. 2) with `fix : (▷A → A) → A` (p. 2). `▷` is an applicative functor but not a monad: "a join operation of type `▷(▷A) → ▷A` would allow us to collapse multiple guardedness obligations" (p. 2). Guarded recursion alone cannot observe finite prefixes, so they add clock variables κ, with `fix : ∀κ.(▷κ A → A) → A` and final coalgebras `∀κ.Stream_κ` (p. 3). The model is "an untyped lazy λ-calculus" (p. 1) with multiply step-indexed types, and a syntactic guardedness checker is rejected as non-compositional, with `mergef f` as the higher-order counter-example (p. 2). They also type Bird's circular `replaceMin` (p. 1, §1.3).

Bearing: **SHARPEN**, with two concrete messages.
1. "Each resumed segment terminates" is a **productivity** statement for the resident seen as a stream of turns: each turn (piece of data) delivered in finite time. The across-turn self-call "sits under a perform", which is exactly a constructor guard in the Nakano sense, so cross-turn recursion is productive by construction. What is NOT covered is the within-turn segment, which a guard does not bound; that is a termination problem (see C3, C4).
2. Type-based guardedness is compositional where a syntactic check is not, and `mix lower upper` is a higher-order function in the `mergef` sense: whether `fix (mix a b)` is productive depends on the behaviour of `upper`. So a syntactic "self only under perform/constructor" scan over specs will be rejected by exactly the argument the paper makes. If a check is wanted it should be type-directed (`self : ▷Self`), not a scan. INFERRED.

#### C3. Abel & Pientka, sized types and copatterns
Andreas Abel and Brigitte Pientka, "Wellfounded Recursion with Copatterns and Sized Types", J. Functional Programming (the file is the JFP version). Read §1 (p. 3-4) and the bfs example (p. 10).

Mechanism (READ). Infinite data is defined by observations (copatterns) rather than constructors. "In the presence of copatterns, productivity is subsumed under plain termination": `repeat a` "terminates in all contexts since it does not unfold by itself and consumes one projection in each unfolding" (p. 4). Termination is by well-founded induction on size/depth ("depth of a function is the maximal size of arguments it can safely handle", p. 3); this is contrasted with syntactic guardedness that "is difficult to handle higher-order programs such as `g f = cons 0 (f (g f))`" (p. 3). The cyclic breadth-first-numbering program (`bfs`, p. 10) is accepted by an appropriate size assignment. A record "defined by observations" such as `Result = ν^∞{tree; rest}` "is just a lazy product".

Bearing: **AGREE on the fit, SHARPEN on the discipline.** An OB object is a record defined by its fields and observed by projection, with open recursion through `self`. That is the copattern view: a spec unfolds only when a field is projected, so productivity reduces to termination of each projection. This is the cleanest statement of what to prove: every field observation of a well-formed `fix spec` terminates, by induction on a size/fuel index that decreases per projection of a self-reference. It also says the design's fuel-bounded machine is the operational face of a sized-type argument. INFERRED for the mapping; READ for the sized-type mechanism.

#### C4. Xia et al., Interaction Trees (added; not on the brief)
Li-yao Xia et al., "Interaction Trees: Representing Recursive and Impure Programs in Coq", POPL 2020 (arXiv 1906.00046). Read §1-2 (pp 4-5).

Mechanism (READ). `itree E R` is coinductive with constructors `Ret r`, `Tau t` (silent step) and `Vis e k` (a visible event `e` whose answer type feeds the continuation `k : A → itree E R`). They support divergence without fuel: `spin := Tau spin`; they note guardedness is "inherently non-compositional" (p. 5) and use `Tau` so that "silently diverging computations" are expressible. Equivalence is weak bisimulation (`eutt`) which ignores finitely many `Tau`s.

Bearing: **SHARPEN.** `perform plan` resumed with a response is literally `Vis plan k`. A turn is a (finite) `Tau*` prefix ending in `Vis` or `Ret`. The natural equivalence for "the stored checkpoint ends every segment as the machine's continuation would" is `eutt` on the interaction trace, not equality of machine state. This also makes the divergence case crisp: a turn that diverges inside is an infinite `Tau` chain, which a host cannot distinguish from "still running" without a fuel bound. Question: is out-of-fuel a `faulted` outcome (consensus-visible, so the bound must be a protocol constant)? See Q3.

---

### D. Reflection and equivalence

#### D1. Wand 1998
Mitchell Wand, "The Theory of Fexprs is Trivial", Lisp and Symbolic Computation 10, 1998, pp 189-199. Read all.

Mechanism (READ). A pure λ-calculus extended with `fexpr` (which "rei[fies] its unevaluated actual parameter as a λ-term in normal form using the Mogensen-Scott coding") and `eval`. Result: "two terms are contextually equivalent iff they are α-congruent" (Cor 1, p. 195). The proof builds, for any term `M`, a context `Eq_{M,σ}` that returns `T` on the coding of `M` and `F` on any non-congruent `N` (Lemma 6-7). Section 4 notes that with a first-order coding of variables "two terms are contextually equivalent iff they are identical, not just α-congruent" (p. 196). Section 5 (Cor 2, p. 196-197): any weakly adequate compositional denotational semantics "must (up to isomorphism) map each term to itself, so no useful abstraction is possible".

Bearing: **SHARPEN, the key theoretical warning for `SpecMeta`.** What triggers triviality is that the observer receives an *injective, decidable coding of the term itself*. Whether our metadata does that is the crux.
- `declared{name, interface, laws}`: a quotient, since two specs with equal declared fields are indistinguishable by a metadata observer. Not Wand-trivial at the leaves.
- `composed{inherited, wrapping}` records the construction history; if `inherited` and `wrapping` hold the sub-specs' metadata recursively, `metadata(compose(a, b))` is injective on construction trees (over declared leaves). Then equivalence under a metadata observer is exactly equality of construction trees, i.e. Wand's trivial theory over the composition fragment. So "compose is associative for behaviour but not under the metadata observer" is not an incidental asymmetry; it is the expected, unavoidable shape. INFERRED, but the mechanism is Wand's Lemma 6.
- Escape routes: (a) metadata coarser than construction (an `Eq` context cannot be built if the coding is non-injective), e.g. record only a flattened set of declared names, which would restore associativity; (b) accept the trivial theory for that observer and say so. Both are legitimate; accidentally having the injective one is the risk. Question: is `composed` meant to be injective on trees or a quotient?
- Cor 2 also warns: a *compositional* semantic model that is adequate for a language containing a metadata observer cannot equate anything the observer separates. So the Core4 reference semantics (behavioural) and the reflective layer must be separate languages with separate equivalences, which is what "list the observers" does.

#### D2. Felleisen 1991
Matthias Felleisen, "On the Expressive Power of Programming Languages", Science of Computer Programming 17, 1991. Read §1, Thm 3.8 (p. 14), Thm 3.14 (p. 18).

Mechanism (READ). A language `L1 = L0 + {F1, ...}` is a conservative extension of `L0` if theorems restricted to `L0` are unchanged. Thm 3.14 (i): "If the operational equivalence relation of `L1` restricted to `L0` expressions is not equal to the operational equivalence relation of `L0`, i.e. `=0 ≠ (=1 | L0)`, then `L0` cannot macro-express the facilities `F1,...`". Slogan in the text: "new programming constructs add to the expressive power of a language if their addition affects existing operational equivalences" (p. 18). Equivalence is always relative to a language of contexts.

Bearing: **AGREE, and it supplies the exact statement.** Adding a `metadata` observer is a non-conservative extension: `compose(compose(a,b),c) =_0 compose(a,compose(b,c))` holds among Core4 contexts but fails among Core4+metadata contexts (Thm 3.14(i)), so metadata *strictly increases expressive power*. That is the correct framing and it matches "list the observers, state each equivalence against its observers": the literature's standard method is the same, indexed by the language of contexts. Risk: the design should also state which equivalences remain under the metadata observer (e.g. `declared` leaves) and treat the failure of associativity as a theorem (Thm 3.14 witness) rather than a caveat. INFERRED for the application.

#### D3. Smith 1984 and Kiczales et al. 1991
Brian Cantwell Smith, "Reflection and Semantics in Lisp", POPL 1984 (author reprint). Read abstract, RL·8, RL·38, RL·48. Gregor Kiczales, Jim des Rivières, Daniel Bobrow, *The Art of the Metaobject Protocol*, MIT Press 1991. Read only the front matter and Part I roadmap (p. 8-9).

Mechanism (READ). Smith requires the embedded theory to be "causally connected, so that the reflective accounts of objects, events and states of affairs are directly tied to those self-same objects ... This causal relationship must run both directions: from event to description, and from description back to event" (RL·8). 3-Lisp reflective procedures "are: (i) run not at the level at which the invocation occurred, but one level higher ... and (ii) given as arguments those structures being passed around in the reflective processor" (RL·38); it reifies the environment and the continuation and absorbs the rest (RL·48). AMOP divides protocols into "introspective protocols, which make it possible to analyze the structure and definition of a program" (Part I, Ch 2) and "intercessory protocols" that "step in or intercede in the behavior of the system" (Ch 3) (pp 8-9).

Bearing: **SHARPEN.**
1. Direction of causal connection is the design question. `SpecMeta` as a *record of construction history* is event-to-description only (introspection). Smith's test of real reflection is the other direction too. If metadata can ever flow back into behaviour (a spec that dispatches on `metadata(self)`), that is intercession and compose is not associative *for behaviour either*. The design needs a non-interference theorem: behaviour of a spec is independent of its metadata (metadata may not be read by `mix`/`fix`/`perform`, only by designated observers). INFERRED.
2. The open question R(Y M) vs Y(R∘M) is the introspection-vs-intercession question in fixed-point clothes. R inside the knot (Y(R∘M)) means every self-call goes through the reflective wrapper, which is intercession at every internal call site (the AMOP/3-Lisp "one level up" reading). R wrapping the finished target (R(Y M)) sees only the outside, introspective. If the prototype's metadata is observed only from outside, R(Y M) is the introspective choice; if the wrapper must be able to affect internal self-calls, only Y(R∘M) works. INFERRED.
3. Smith reifies the **continuation**; our checkpoint is a reified continuation (heap, control, stack). Smith's "causal connection in both directions" is the right informal statement of `ForcingTransparent`: the description (checkpoint) must reconstitute the very event (continued run), not merely resemble it. INFERRED.

---

### E. Serializable continuations and checkpoint transparency

#### E1. Khan 2026, "Resume Means Resume"
Sajjad Khan, "Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and Resume Semantics in Workflow Persistence Layers", arXiv 2608.03836v3, Aug 2026. Read §3 (the Resume Contract), §3.3-3.4, §4.2 liveness. Section numbers per the paper's own headings.

Extracted properties (READ; verbatim where quoted).
- **Definition 1 (Resume plane)** (§3.1): tasks 1..N, one interrupt-gated, durable log of `⟨t, valid⟩` records, durable frontier `F`, a crash erases volatile state, recovery "chooses a continuation point as a function of the durable log".
- **PC** (Property 1, prefix continuation, §3.2): "Recovery continues from the durably recorded frontier state ... execution after recovery begins in the state `S_F` recorded at frontier `F`, or in a state re-derived deterministically from the durable log alone that equals `S_F`. Memoized replay conforms ... provided every prefix effect is served from the durable record ... Re-deriving state from initial values, or traversing the prefix against live effects, violates PC." Equality is observable-state equality via the public state API.
- **EO** (Property 2): "effect `e_t` fires at most once on a branch across any sequence of interrupts, crashes, and resumes" (a safety invariant; "exactly" needs the liveness obligation).
- **FD** (Property 3): fork-intent resumes with values `v_1..v_m` addressed to the same interrupt checkpoint yield `o_k = f(v_k)`.
- **CV** (Property 4): "Every persisted checkpoint record satisfies the state schema: a write that would persist schema-invalid state is rejected with an error, not stored."
- **CO** (Property 5), two clauses: **CO-c** (consumption count): an interrupt is consumed by at most one resume. **CO-e** (effect inertness): a resume without fork intent addressed to a completed run or already-consumed interrupt, including byte-identical re-delivery, is inert w.r.t. effects. The clauses are independent: a gate serving its effect idempotently "can consume one human approval twice while the effect count stays at one".
- **RD** (Property 6): "two recoveries from identical durable logs make identical decisions"; the reported hazard also demands order-invariance of the recovery decision across more than one legal log.
- **FI** (Property 7, fork-intent expressibility): the resume API must be able to express the discriminator of Def 2 on the wire (a distinct resume ordinal, an explicit fork flag, or a branch-creating address). Protocol obligation, not model-checked.
- **Lemma 1** (§3.3), FD-CO incompatibility without a discriminator: on a wire protocol with no branch discriminator, "no responder, deterministic or randomized, satisfies both `FD_ι` and `CO_ι` on all traffic the protocol admits". Proof is an indistinguishability argument between a transport duplicate and a caller-requested fork carrying the same value.
- **Liveness obligation** (§4.2): `EventuallyCompletes` under weak fairness. "a framework that refuses every resume satisfies all six safety invariants, so the contract pairs them with EventuallyCompletes"; named "safety vacuous, progress dead" when a crash leaves persistence unrestorable.
- **Prop 1** (§3.4): FD is independent of the conjunction of the others; no theorem of minimality or completeness is claimed; candidate sevenths named as scope exclusions: checkpoint-migration validity, an effect-visibility ordering obligation, and loud-vs-silent disposition of discarded resumes.
- Remark 4: EO is per-branch; a deployment that cannot tolerate even requested branch duplication composes FD with an idempotency key at the effect.

Bearing on Objective Bend: mixed, with the most specific claims in this note.
1. **AGREE: CO-c is the nullifier.** "Each resume consumes the await like a nullifier bound to the checkpoint digest" is CO-c plus CO-e. Khan's measured failure (k concurrent resumers of one parked interrupt fire the effect k times) was a non-atomic claim in a shared store. OB's nullifier is chain state committed atomically with the turn, which removes that mechanism, assuming one writer ordering per object. INFERRED.
2. **DISAGREE by design with PC, and the design should say so.** PC says recovery continues from the *recorded* frontier state. OB's resume-with-view deliberately resumes with the object's state *read in the resuming turn*. So PC as written is violated on purpose; the right statement is "control and heap continue from the checkpoint; object state comes from the view". Risk: a pre-yield read cached in the checkpoint heap and used after resume is a stale read that resume-with-view does not cover. The guarantee "no write is computed from a stale read" needs a discipline: pre-yield reads must not flow to post-resume writes, or reads before a yield are invalidated (a taint/freshness property). Question: how is that enforced for values already in the heap? INFERRED.
3. **FI.** The nullifier is bound to the checkpoint digest only. Per Lemma 1, with no resume ordinal or fork flag, FD is unsatisfiable together with CO, so OB must not claim FD. That is probably intended (no forks), but then it should be stated that forking a checkpoint is refused (CO wins) and that a retry of a lost resume is distinguished from a duplicate only by commit status: the nullifier must be consumed iff the turn commits (or commits `faulted`). INFERRED.
4. **AGREE: `faulted` is the liveness fix.** Refusing a turn leaves the await parked (Khan's vacuity hole); committing `faulted` consumes the await and terminates the obligation. A refusal path that leaves a nullifier unconsumed re-opens "safety vacuous, progress dead". INFERRED.
5. **SHARPEN: not in Khan: CV for the checkpoint itself.** CV rejects a write that would persist invalid state. For OB the checkpoint is settled, GC'd and serialized; CV analogue: the checkpoint load refuses a digest/schema mismatch (the design already says old shapes refuse to load). The §3.4 scope exclusion "checkpoint-migration validity" is precisely the epoch story.

#### E2. Burckhardt et al. 2021, Durable Functions
Sebastian Burckhardt, Chris Gillum, David Justo, Konstantinos Kallas, Connor McMahon, Christopher S. Meiklejohn, "Durable Functions: Semantics for Stateful Serverless", Proc. ACM Program. Lang. 5, OOPSLA, Article 133, Oct 2021. Read §3.5, §5, §6, Lemmas 6.5-6.7, Thm 5.3, Thm 6.4.

Mechanism (READ). The compute-storage model is shown a weak simulation of the high-level model (Thm 5.3). The replay-based model stores orchestration state as a history of events and rehydrates by replay because "the state of the orchestration ... is not serializable by default" in mainstream languages (§6 intro). It is proved bisimilar to persisting intermediate states (Thm 6.4, §6.3), resting on Lemma 6.5 (Deterministic Replay: `h ⊲↠ x` and `h ⊲↠ x'` imply `x = x'`), Lemma 6.6 (Record/Replay) and Lemma 6.7 (Transparency of Recording). "Note that Lemma 6.5 relies on the determinism of the execution, which in this model is easy to prove for our simple lambda calculus. In a mainstream programming language, nondeterminism is not implicitly guaranteed" (§6.3). The guidelines (§3.5): "the orchestration code must be deterministically replayable. Any code that reads non-deterministic data sources or calls I/O should not be done directly in the orchestration, but must be wrapped in an activity".

Bearing: **AGREE on the proof shape, DISAGREE on the mechanism, SHARPEN on the premise.**
1. Their transparency theorem has the same shape as `ForcingTransparent` (persisted representation vs in-memory continuation), proved as a **bisimulation** whose load-bearing lemma is determinism of the step function (Lemma 6.5). So `ForcingTransparent` should be stated as a bisimulation (or at least simulation) on the interaction trace, and its premise list must include determinism of the machine's segment step, with no hidden inputs (heap addresses, fuel, clock, GC timing). INFERRED.
2. They *replay* a history because the host-language state is not serializable; OB serializes the machine state directly. That is the stronger and rarer design (E4 cites Termite/Pettyjohn for the serialization side), and it removes DF's determinism-of-user-code requirement, replacing it with determinism of *the machine*, which the Lean model can discharge. This is a real advantage and the design should state it.
3. DF reads state through activities/entity calls recorded in the history, so after replay the orchestration sees the *recorded* value, never a fresh one. OB's resume-with-view is the opposite choice: fresh view at resume. DF therefore cannot serve as a precedent for the resume-with-view guarantee; Khan's PC cannot either (E1).

#### E3. Termite Scheme (Germain, Feeley, Monnier 2006) and Pettyjohn et al. 2005
Guillaume Germain, Marc Feeley, Stefan Monnier, "Concurrency Oriented Programming in Termite Scheme", Scheme and Functional Programming 2006 (read §3.1-3.2, §4.9, §5). Greg Pettyjohn, John Clements, Joe Marshall, Shriram Krishnamurthi, Matthias Felleisen, "Continuations from Generalized Stack Inspection", ICFP 2005 (read abstract, §3.5, §4 labelling).

Mechanism (READ). Termite serializes "every first class value in the language, including closures and continuations", with limits: "It will not be possible to serialize a closure or a continuation if it has a direct reference to one of these objects in their environment" (ports, devices) (§3.1, p. 2); non-serializable resources are replaced by process proxies so serialization is "just a pid". Mutation is removed: "To keep the semantics clean and simplify the implementation, mutation of variables and data structures is not available" (§3.2, p. 2). The format preserves sharing and cycles (SRFI 38 notation with a hash table to detect shared data) (§5), and deserialization requires "the same compiled code" (p. 8). Pettyjohn et al. give a translation that eliminates continuation capture via stack inspection, with a correctness theorem as a simulation (Thm 1, §3.5: `CMT⟦eval_SL(p)⟧ = eval_TL(CMT⟦p⟧)`, via a simulation Lemma 2: each source step corresponds to at least one target step). Serialized continuations carry defunctionalised-closure labels derived from "a message digest based on the syntactic structure of the program"; if the program changes non-trivially "the computed message digest changes ... Values published with the old key become obsolete and the server can fail gracefully" (p. 7).

Bearing: **AGREE, with three concrete requirements on the premise.**
1. A non-serializable thing in the environment makes the closure non-serializable: Termite's rule is the effect-in-the-cell rule from the opposite end. "No effect can sit in a field/argument/payload" is what makes the checkpoint serializable at all. INFERRED.
2. Code identity belongs in the checkpoint digest (Pettyjohn, Termite): a resume under a different program or machine version must refuse, not reinterpret. The design already binds the digest; the transparency premise should name the code/machine digest as part of "the checkpoint".
3. Neither source proves that a serialize/deserialize round trip is transparent. Pettyjohn proves the capture/reinstate *translation*; the serializer is engineering. Termite has no theorem. So `ForcingTransparent` as an open premise is where the literature is also silent. Nothing I found proves a heap-serializing round trip transparent for a lazy machine with sharing; the closest are Burckhardt's bisimulation (replay not serialization) and Pettyjohn's simulation (stack, not heap). INFERRED from absence in the papers read; Kali Scheme (Cejtin et al. 1995) was not obtained and might contain more.

#### E4. Ahman & Pretnar 2021 (in paperbin; abstract only)
"Asynchronous Effects", POPL 2021. Read abstract: it decouples "the execution of operation calls into signalling that an operation's implementation needs to be executed, and interrupting a running computation with the operation's result". **AGREE** as framing: `perform plan` followed by resume with a response is signal-then-interrupt. I did not read the semantics, so no further claim.

---

### F. Synthesis: how the literature lines up with the design

| Design element | Literature says | Verdict |
|---|---|---|
| call-by-name reference, call-by-need machine | equal on effect-free ground observations (Ariola-Felleisen, Launchbury, Chang-Felleisen); NOT equal once an effect can run while forcing a shared cell (McDermott-Mycroft, CBPV) | AGREE for pure; refusal makes the claim conditional |
| `fix` ties a heap address to itself | Launchbury native letrec; Ariola-Felleisen/λ_need exclude cyclic | SHARPEN: anchor in Launchbury |
| completeness finite, no resource bound | adequacy is existential (Launchbury/Breitner); bounds need a resourced semantics | AGREE; bound needs a cost model |
| perform refused under update frame | Haskell leaves it an unchecked obligation (`unsafePerformIO`); CBPV puts it in types | AGREE on rule; SHARPEN: type it |
| activity type never shareable | CBPV/Haskell: description is a value, running is not | SHARPEN: decide plan-as-value |
| no guardedness check | Nakano/Atkey-McBride: type-directed; copatterns: productivity = termination of projections | under-specified |
| ForcingTransparent | bisimulation with a determinism premise (Burckhardt); simulation (Pettyjohn) | under-specified |
| resume-with-view | opposite of Khan PC and of DF replay | no precedent; needs its own statement |
| SpecMeta, compose | Wand/Felleisen: observer-relative; injective coding trivialises | AGREE with method; SHARPEN on injectivity |

---

### Sharpest questions

**Q1. Is a call-by-name reference semantics the right spec once `perform` exists, and what does the reference do where the machine refuses?**
McDermott-Mycroft's `inc` example (p. 2) and CBPV's CBN translation (Fig 8, `print c. M ↦ print c. M^n`, `x ↦ force x`) both show name re-runs an effect at each use and need runs it at the first. The machine refuses at the first force (`sharedEffect`); a CBN reference never refuses and may perform twice. So "finished machine run equals reference evaluation" cannot hold for programs where `perform` is reachable under a shared cell, and whether the machine refuses depends on the evaluation order (first force). Either the reference semantics gets the same refusal (a perform reachable in any argument/field/cell position is stuck in both), or the theorem is explicitly restricted to a class that excludes it, with the class defined syntactically or by type. Which?

**Q2. Is "refuse perform under an update frame" the right line, or is CBPV's value/computation split cleaner?**
CBPV puts the line in the type system: a binding holds a value; `F`-typed (effectful) computations are sequenced, not memoised. The design's runtime frame check is a dynamic approximation that, by Q1, is order-dependent. A typed line makes `sharedEffect` unreachable in well-typed programs and lets the Lean theorem quantify over typed programs. Second half: Haskell and CBPV both allow a *suspended* activity (`IO a`, `U (F A)`) as a storable value and make *running* it the unshareable act. The design bans even storing an activity in a field. Should a Plan be a duplicable value (run-many, each a new perform, nullifier per run) or a linear one-shot resource?

**Q3. What guardedness/termination discipline fits a resident whose self-call is under perform?**
Cross-turn recursion under a perform is productive by construction (a `Vis` constructor in the ITree sense, a guard in the Nakano sense). The open obligation is the within-turn segment: each `Tau*` run must be finite. Candidates from the literature: type-directed `self : ▷Self` for spec recursion (Atkey-McBride, which rejects `bad = self.bad` where the current design accepts it as lazily ⊥), or sized/fuel-indexed projection (Abel-Pientka). Also: out-of-fuel is consensus-visible, so the fuel bound and the step-count cost model must be protocol constants, and the natural semantics does not fix step counts (Breitner needs a resourced semantics). Is out-of-fuel a `faulted` commit, which would also close Khan's liveness hole? Does OB want total (reject unproductive specs) or partial (accept, blackhole on forcing)?

**Q4. What exactly must ForcingTransparent state?**
From Burckhardt (Thm 6.4, Lemma 6.5), Pettyjohn (Thm 1, Lemma 2), Termite, ITrees, and Khan: (a) equivalence is weak bisimulation on the (perform plan, response) trace and the final outcome, not equality of machine state; (b) the step function is deterministic with no hidden inputs, in particular no observable heap addresses; (c) at a yield the stack contains no update frame and no blackholed cell, which follows from the `sharedEffect` refusal and should be a stated invariant ("settled") rather than a hope; (d) serialize-after-GC is a heap isomorphism preserving sharing and cycles, with `fix`'s self-pointing cell as a test case; (e) the code and machine digest is part of the checkpoint and a mismatch refuses; (f) it quantifies over all responses and all views, and the comparison object is an idealised in-memory machine that *also* reads the view at resume. Without (f) the statement compares against a machine that holds stale state, which contradicts resume-with-view. Which of (a)-(f) does the current premise cover?

**Q5. Is SpecMeta injective on construction trees, and does metadata ever flow back into behaviour?**
Wand: an observer with an injective, decidable coding of the term makes contextual equivalence trivial (Thm 1, Cor 1). If `composed{inherited, wrapping}` embeds the sub-specs' metadata recursively, then under the metadata observer equivalence of composed specs is equality of trees, so non-associativity is forced, not incidental; a coarser `composed` (flattened declared names) would restore associativity. Felleisen (Thm 3.14(i)) says the extension is non-conservative and strictly more expressive; the statement belongs there. Smith and AMOP: introspection (event to description) is safe; intercession (description to behaviour) is what would break behavioural associativity, so a non-interference theorem (behaviour independent of metadata) is needed. The same split decides R(Y M) vs Y(R∘M): R inside the knot intercedes at every self-call, R around the finished target only introspects. Which is the intended reflective power?


---

## LIT-W3-calls-sends-contracts

<!-- source: LIT-W3-calls-sends-contracts.md -->

## LIT-W3: calls, sends, activities, laws, seats, admission — primary-text check (2026-10-06)

Worker: literature W3 for DEPUTY-GROUNDING. No builds, no code edits, no git.
Primary sources: `~/paperbin/world-program-model/` (called `WPM/` below). New downloads: `~/paperbin/objective-bend-grounding/`
(`stellar-soroban-authorization`, `stellar-soroban-cross-contract`, `dedaub-aptos-reentrancy`, `pact-manual-capabilities`,
`pact-capability-theory-wiki`, `eip-150`; each .html with a .txt beside; ~100 KB total). Kagi queries used: 8 of 20.
Disk: Mac data disk 99% (115 Gi free) before and after; I wrote only small text files.

Tags: **READ** = read in the primary text at the cited place. **VIA-SCHOLAR** = taken from a scholar report, not re-verified
(report named). **INFERRED** = my reasoning, not in the source. AGREE / DISAGREE / SHARPEN is about *our* design (see the brief).

Scholar reports are abbreviated: CALLS = `SCHOLAR-CALLS-CONCURRENCY-20261004.md`, FRONTIER = `SCHOLAR-FRONTIER-AGORIC-20261004.md`,
LAWS = `SCHOLAR-LAWS-CONTRACTS-20261004.md`, R-CALLS = `REVIEW-SCHOLAR-CALLS-20261005.md`.

---------------------------------------------------------------------------------------------------------------------

### 0. Headline findings (read this if nothing else)

1. **Our `call` is E's immediate call with both hazard sources removed, not a point E ever occupied.** E's plan-interference
   hazards (Miller §13.1) need a callee that runs *on the caller's live, mid-update heap* and can re-enter. We remove the live heap
   (snapshot + deferred writes) and the re-entry (refusal). No paper I read studies exactly this point (INFERRED). It is a
   defensible, probably-good point, but the literature names three things it does NOT fix: failure attribution (§1), invariants
   that span objects (§5, §10), and sibling visibility inside one frame (§Q2).
2. **Object-granularity re-entry refusal is both too strong and too weak.** SeRIF (Cecchetti et al. §4.1, Fig. 4) shows
   object re-entrancy is the wrong boundary: it over-refuses (Fig 4b) and misses application-level re-entry across *mutually
   trusting* objects (Fig 4c: A -> B -> C with A and C halves of one app; the Parity wallet shape). Aptos Move ships exactly our
   rule (module lock, direct and indirect) and its own auditors list the bypasses (§5).
3. **IC inter-canister calls are almost our `send`**: `call_perform` queues, acts only after the sender's message returns without
   trapping, pre-deducts a response reserve, guarantees *exactly one* reply-or-reject once `err_code` is 0, and gives pairwise
   FIFO of *starts* only (§6). The IC's two scars are directly ours to avoid: unbounded waits wedge the caller, and a bounded wait
   produces `SYS_UNKNOWN` (the callee ran, the caller was told otherwise).
4. **Scoped grants without argument binding are weaker than the two production precedents.** Soroban authorizes an invocation
   *with its arguments*, as a tree, with a nonce and an "exhausted" mark; Pact scopes a signature to a capability *with args*.
   Ours is {object, method, uses} (§4, Q3).
5. **Zoe's "judged on every reallocation" has a hole in the source I read**: the mint/burn path commits a reallocation with
   neither conservation nor offer-safety checked in `zcfSeat.js` (§3). Our kernel must make "every path" literal.
6. **Three scholar mis-citations / mis-corrections** (full list in the "Corrections" section), notably R-CALLS's "misquote"
   correction of the Grossman figure is itself backwards, and the OCapN "ordering bug" claim is not in either OCapN file.

---------------------------------------------------------------------------------------------------------------------

### 1. Miller 2006 "Robust Composition" and Miller/Tribble/Shapiro 2005 "Concurrency Among Strangers"

Files: `WPM/miller-robust-composition-2006.txt`, `WPM/miller-concurrency-among-strangers-2005.txt`.

#### What the primary text says

- **Turn, vat, immediate call vs eventual send. READ.** Thesis §14.1 (thesis p.106): "Within a single thread of control, E has
  both a normal execution stack for immediate call-return and a queue containing all the pending deliveries. Execution proceeds by
  taking a pending-delivery from the queue, delivering its message to its object, and processing all the resulting immediate-calls
  in conventional call-return order. This is called a turn." So a turn already *contains* a synchronous call tree; E never banned
  synchronous calls, only synchronous calls **across vats**.
- **Why sync only within a vat. READ.** §14.2 (p.107): "eventual references carry only eventual-sends, not immediate-calls — an
  immediate-call on an eventual reference throws an exception." TGC p.206: "Only near references provide one object synchronous
  access to another. Therefore an object has synchronous access to state only within its own vat. Taken together, these rules
  guarantee that a running turn — a sequential call-return program — has mutually exclusive access to everything to which it has
  synchronous access." The reason is *mutual exclusion without locks*: a turn that only touches near objects needs no isolation
  mechanism. It is not a reentrancy argument.
- **Plan interference. READ.** §13.1 (p.97-100), three sequential hazards in the listener pattern: (1) **aborting the wrong
  plan** ("A listener that throws an exception prevents some other listeners from being notified … and possibly aborts the
  publisher's plan"), (2) **nested subscription**, (3) **nested publication** ("a listener may cause a publisher to publish a new
  status … After that inner invocation returns, the outer invocation of setStatus continues notifying listeners of the older,
  pre-deposit balance"). Miller's diagnosis (p.100): "The statusHolder, by running each subscriber's plan during a step of a
  publisher's plan, has provoked plan interference." TGC p.204: "all of the sequential hazards (e.g., Nested Publication) and many
  of the concurrent hazards (deadlock) occur because the statusChanged method is also invoked immediately: the publisher's plan is
  set aside to pursue the listener's plan." The cure is `<-` (eventual).
- **Pipelining. READ.** §16.2 (p.117-118): messages sent on a promise "'move' as close to the arrowhead as possible"; if the
  promise resolves locally on the target vat, "z(r2) is immediately queued on VatB's to-do list"; if it resolves on VatA the message
  is "streamed back towards VatA just behind the message informing VatA of r1's resolution"; if on a third vat it is forwarded.
  Pipelining there is onto *any* promise, not only promises of object references.
- **Datalock. READ.** §16.3 (p.118-119): a promise whose resolution requires already knowing it; "the not() message is forever
  buffered in the promise which only not()'s delivery could resolve". Miller counts "only two datalock bugs" in "perhaps 60
  programmers".
- **Broken promise contagion. READ.** §16.5: the vat catches the turn's exception and "breaks the promise by resolving the promise
  to a broken reference"; any call or send to a broken reference breaks the result.
- **E-ORDER. READ.** §19.1-19.4 (p.137-139): fail-stop FIFO per reference; reference **forks** at argument passing (Hasse
  diagram); CAUSAL order rejected because "we don't know how to enforce it among mutually defensive machines." §19.1 note:
  same-vat near calls may jump ahead of earlier eventual sends.
- **Turns never block, so cannot deadlock. READ.** TGC p.207: "computation within a turn can never block — it can only run, to
  completion or forever."
- **Defensive consistency. READ.** TGC §7.1 (p.208-209): defensive correctness = correct despite arbitrary client behaviour;
  defensively consistent = "incorruptible by its clients"; "If P relies on R, then P also relies on all of R's other clients
  unless R is defensively correct."

#### Is our sync call with re-entry refusal a known-bad or known-good point?

**Neither; it is a new point whose two ingredients have precedents.** (INFERRED, from the above.)

| E hazard (§13.1) | Needs | Ours |
|---|---|---|
| nested publication | callee sees/acts on caller's mid-update state, and re-enters the publisher | removed twice: callee reads the turn snapshot and never sees a caller's pending write; re-entry refused |
| nested subscription | same, plus a mutable collection iterated during the call | removed: collections are state, writes deferred |
| aborting the wrong plan | a callee failure propagates to the caller's plan | **kept, and made worse**: a callee law refusal aborts the whole turn (R-CALLS OPEN 1 agrees) |

- **AGREE** with R-CALLS OPEN 1 that the DAO shape is excluded. **SHARPEN**: E's own cure for "aborting the wrong plan" is
  isolating failure by turn (`<-` + broken promise). Our only failure isolation is `send`. So the rule "a caller who will not
  underwrite the callee uses `send`" is not a courtesy, it is E's whole answer to hazard (1); the design should say that `call`
  failure is *never* catchable in-frame (otherwise we reintroduce a catch inside a deferred-write frame; see EIP-150 in §6 for what
  catchable callee failure did on the EVM).
- **SHARPEN (new hazard E does not have).** Because the callee runs on the snapshot and its write is judged at frame return, two
  *sequential* siblings of one caller (stack pops between them, so re-entry refusal does not fire) both read the pre-state. R-CALLS
  §2.5/D2 handles same-slot double write. It does not say whether sibling 2 sees sibling 1's *returned* write (Q2).
- **Reliance argument.** TGC's "P also relies on all of R's other clients" is the case for the law: each object must be
  defensively consistent against its own writers. That is exactly the law as the gate. AGREE (VIA-SCHOLAR CALLS A2 says the same;
  I confirm the quote above).
- **E-ORDER bears on `send`.** Fail-stop FIFO per reference plus forks is stronger than our per-(sender, target) FIFO: ours
  has no fork rule (an object reference passed in `args` can be used by the receiver to send to the same target on a *different*
  (receiver, target) queue, so receiver messages may overtake the original sender's earlier queued messages). Miller §19.2's
  Alice/Bob/Carol example is exactly this. Whether to care is a design choice (INFERRED); Miller says do, for the "Alice
  delegates querying to Bob" pattern.

---------------------------------------------------------------------------------------------------------------------

### 2. CapTP / Cap'n Proto RPC

Files: `WPM/ocapn-captp-spec.md`, `WPM/ocapn-implementation-guide.md`, `WPM/capnproto-rpc.capnp`, `WPM/capnproto-rpc.html`.

- **Pipelining. READ.** OCapN spec "Promise pipelining" (~l.188-200): a message sent with `answer-pos` creates a promise on the remote
  session that later messages reference with `desc:answer`; "When a promise is fulfilled to an object, messages sent to the promise
  will be delivered to that object." `op:get` (l.686), `op:index` (l.728), `op:untag` pipeline into *fields* of a result. Cap'n Proto:
  `PromisedAnswer{questionId, transform}` with `getPointerField` ops (rpc.capnp l.1115-1126).
- **Who names the answer. READ.** OCapN `answer-pos` "must be unique within the CapTP session" (l.590); the sender chooses it.
  **Ours differs and is better for consensus:** the message id names the reply slot (nobody submits a slot name). (INFERRED; R-CALLS
  §1 already credits Ozone for this.)
- **Embargo / E-order on resolution. READ.** `Disembargo` (rpc.capnp l.688-735): "if foo() is called on a promise, and that promise
  happens to resolve before bar() is called, then the two calls may travel different paths over the network, and thus could arrive in
  the wrong order. In this case, the call to bar() must be embargoed." "Note that in the case where Carol actually lives in … the
  same vat that the promise already pointed at, no embargo is needed, because the pipelined calls are delivered over the same path
  as the later direct calls." Also the "Tribble 4-way race".
- **Three-party handoff. READ.** OCapN spec §"Third Party Handoffs" (l.280-373): Gifter signs a `desc:handoff-give`; Receiver wraps
  it in a `desc:handoff-receive`; Exporter's `withdraw-gift` consumes the gift once ("handoffs cannot be used multiple times",
  guide l.529), with an anti-replay count; the guide (l.531) says ordering of gift deposit vs withdraw "does not matter".
- **Compare to our restricted forwarding.**
  - *Ours is the "same-vat" case only.* All our objects live in one kernel, so forwarding on resolution is a local queue move.
    CapTP's embargo/disembargo and the Tribble race arise from multiple vats and multiple paths; none arises when forwarding is
    atomic with resolution in one turn (INFERRED). **AGREE** that nested pipelining and cross-host handoff can wait.
  - *The ordering gap survives locally anyway* (SHARPEN, Q4b): a send to slot S (queued on S) followed by a direct send to the
    now-known target is the exact `foo()`/`bar()` example. If slot-queued messages are forwarded into the (sender, target) FIFO at
    the instant of resolution, a message sent *before* the resolution but forwarded *at* it can land behind direct sends made in
    between, or ahead, depending on the resolving turn's position. The design must state which; Cap'n's answer is "embargo so that
    send-order wins".
  - *Restriction to object-reference resolutions is a real loss versus CapTP's field pipelining* (`op:get`/`op:index`): a reply
    that is a record containing an object cannot be pipelined into. Acceptable for v1 (INFERRED). The Cap'n text calls
    pipelining "absolutely critical" to object interfaces over a network (capnproto-rpc.html l.206); that argument is about
    latency, which a single kernel does not have, so **our gain from pipelining is turn count, not RTT** (INFERRED; CALLS idea
    on Agoric kernel-pipelining-off VIA-SCHOLAR agrees).
  - *Datalock* (Miller §16.3) applies if a method can send to its own reply slot and then be required to resolve it from that
    send. Per-delivery run-to-completion makes it unlikely but the design should say a reply slot cannot be the target of a send
    made by the message that decides it (INFERRED).

---------------------------------------------------------------------------------------------------------------------

### 3. Agoric Zoe / ERTP: offer safety and payout liveness

Sources: `WPM/agoric-src-offerSafety-2026.js`, `agoric-src-zcfSeat-2026.js`, `agoric-src-zoeSeat-2026.js`,
`agoric-zoe-offer-safety-docs.txt` (docs "Offer Safety", "How Zoe Ensures You Won't Leave Empty-Handed" updated Jan 2020,
"Zoe v0.24.0, Aug 2022"), `agoric-doc-zoe-proposal-2026.md`, `agoric-doc-zoe-offer-enforcement-2026.md`.

- **Offer safety, definition. READ.** Doc "Offer Safety": "the user is guaranteed to either get at least what they wanted, or get back
  a full refund of what they offered — and never worse." Code `offerSafety.js` `isOfferSafe(proposal, allocation) =
  satisfiesGive(proposal, allocation) > 0 || satisfiesWant(proposal, allocation) > 0`, each `satisfiesInternal` = for every
  keyword in give/want, `AmountMath.isGTE(allocation[kw], required)`; a missing keyword in the allocation is unsatisfied (returns 0).
  FRONTIER's formula and its note on total slots are correct (VIA-SCHOLAR confirmed by READ).
  **Note the shape:** `isOfferSafe(proposal, newAllocation)`: a predicate on the new allocation and the *fixed original proposal*;
  it does not take the old allocation. Safety by induction: every committed allocation was safe, the first (the escrowed `give`)
  is safe, so the current allocation is always safe.
- **Where it is enforced. READ.** `zcfSeat.js` `atomicRearrange` (l.243-297): all seats active; `assertRightsConserved`;
  `isOfferSafe(seat.getProposal(), allocation) || Fail`; then "COMMIT POINT … The effects must succeed atomically".
- **Payout liveness. READ.** Doc "How Zoe Ensures…": "once the exit of an offer is triggered, Zoe ensures that the payout of that
  offer will be made promptly, no matter what the contract code does at that point." Triggers: contract wants out, client wants
  out, system error. Mechanism in `zoeSeat.js` `doExit` (l.71-84): `withdrawFacet.withdrawPayments(currentAllocation)` then
  `finalPayouts`. The payout is of the *current allocation held by Zoe*, not something the contract computes.
- **Exit is NOT unforbiddable in Zoe. READ.** `agoric-doc-zoe-proposal-2026.md` l.55-61: `exit` is one of `{onDemand}` (default),
  `{waived}` ("The offering party can't cancel and relies entirely on the smart contract to complete (finish or fail) their
  offer"), `{afterDeadline}`. FRONTIER l.293 lists these correctly (VIA-SCHOLAR, now READ).
- **A gap in "every reallocation". READ.** `zcfSeat.js` l.323-346, `zcfMintReallocator.reallocate`: "Unlike the zcf.atomicRearrange
  method, this one does not check conservation, and so can be used internally for reallocations that violate conservation, like
  minting and burning." It also contains no `isOfferSafe` call (the only call sites in these files are l.175-184 the seat method
  and l.269 `atomicRearrange`). I have not read `zcfMint.js`, so the caller may check elsewhere: **READ for the seat manager, UNKNOWN
  for the whole of Zoe**.

**Compare to seats ("a seat holds balances under an offer whose safety is a law judged on every reallocation, with an exit no clause
can forbid").**
- **AGREE** on the shape (R-CALLS/FRONTIER already say so): law = fixed-per-offer predicate, checked at the single commit point.
- **SHARPEN 1: "exit no clause can forbid" is strictly stronger than Zoe.** Zoe permits `waived`; our seat must not offer that
  variant, or the sentence is false. State whether a deadline-only exit is allowed (it is not "no clause can forbid"
  if the exit is only available after a deadline).
- **SHARPEN 2: the induction needs a reachable-state invariant, and a base case.** Zoe's safety of the *current* allocation holds only
  because the initial allocation equals the escrowed give and *every* write path is checked. Ours: the seat's initial balance must
  be established by a kernel action whose law is satisfied by construction, and `exit` must withdraw exactly the current balance
  (not "what the contract says"). Same pattern as R-CALLS §2.2 `reachable_records_typed` (INFERRED).
- **SHARPEN 3: "every reallocation" must include non-`atomicRearrange` paths** (mint, burn, fee debit, postage escrow, refund).
  Zoe's own seat manager has a bypass (mint path). Each kernel entry point that changes a seat balance needs the same law call
  (INFERRED from the READ gap above).
- **SHARPEN 4: Zoe's check is per-seat over proposed new allocations only for the seats named in the rearrangement** ("touched
  seats"). Seats not named are unaffected and unchecked. Our `call` tree can touch seats transitively; the rule "every seat whose
  balance changed in the turn is judged" must be stated at turn commit, not at the call site (INFERRED).
- Doc l.290-300 ("the contract never has access to your digital assets", assets are not sent to the contract, only information) is
  the property seats must keep: a seat's owner object is never handed its balance (VIA-SCHOLAR; READ in offer-enforcement doc).

---------------------------------------------------------------------------------------------------------------------

### 4. Daml (Bernauer et al. 2023, arXiv:2303.03749) authorization vs our signer/subject/scoped grant

File: `WPM/bernauer-daml-2023.txt`.

- **Model. READ.** Templates declare `signatory` (non-empty; authorize creation; notified), `observer`, and per-choice `controller`
  (§2.1-2.3, ll.150-217). A command is a tree of Create / Exercise / Fetch actions (§3.4, ll.470-500).
- **The authorization rule. READ.** §3.6 (ll.528-545), with authorization context A a set of parties:
  - Create is well-authorized iff S ⊆ A (all signatories are in A).
  - Fetch: A ∩ (S ∪ O) ≠ {} (a signatory or observer).
  - **Exercise: C ⊆ A (the choice's controllers), AND the *consequences* tx are checked in the context S ∪ C**, "the signatories
    and controllers". "This encodes that a signatory has pre-authorized the consequences of the choices when the contract instance
    was created. Delegation is not transitive, though, as the authorization context A of the Exercise action does not propagate to
    the consequences."
  - "Delegation not being transitive is a deliberate design choice … the authorization context for a choice implementation is
    determined solely by the template definition and thus independent of the calling context." "If the consequence … were instead
    checked in the augmented context A ∪ S ∪ C, then the additional parties in A could make a subaction well-authorized that in
    isolation would not be." Transitivity is opt-in by listing the needed parties as controllers of an inner exercise (Settle
    example, Fig 4).
  - A transaction is well-authorized if all top-level actions are.
- **Consuming choices. READ.** §3.3 exercise semantics (ll.472-492), step 4: the choice body is interpreted in the state where
  the exercised contract is already `Archived` if the choice is consuming; step 1 requires the contract to be Active. So re-entering a
  consuming choice of the same contract fails at step 1: re-entry protection by linearity. Non-consuming choices are re-enterable.

**Comparison with our model.**

| | Daml | Ours |
|---|---|---|
| Authority of a nested step | S ∪ C of the *callee's own template*: the callee's declared parties | the signer, as `request/subject`, only under a scoped grant {object, method, uses} |
| Source of nested authority | the callee's signatories pre-authorized it at creation | the signer's grant at invoke time; the callee declares nothing |
| Does the caller's authority flow in? | never (non-transitive, deliberate) | only through the grant; otherwise `request/caller` is an object name |
| Atomic tree | yes | yes |

- **SHARPEN (difference of kind, not degree).** Daml's nested authority is *callee-declared* (pre-authorization by the callee's
  signatories); ours is *caller-delegated* (the signer's grant). These answer different questions. Daml's rule ("who must have
  consented to this consequence") is a *consent* rule; ours ("on whose behalf may this frame act") is a *delegation* rule. Daml
  cannot express "Alice lets Bob's contract do X on her behalf this once"; that is what Soroban and Pact grants do (below). Conversely a
  grant model cannot express "this object's owners pre-consented to every consequence of this method" unless the object's law
  does. **Recommendation (INFERRED): keep both and name them**: law = callee-declared consent; grant = signer-delegated authority.
- **Daml's argument for non-transitivity is the argument for our `request/caller` + scoped subject.** AGREE: the non-transitive
  default ("the authorization safety analysis for the building blocks remains unaffected") is what `request/subject` absent-by-default
  gives us.
- **The grant is under-specified relative to production precedents (new, Q3).**
  - **Soroban (READ, `stellar-soroban-authorization.txt` ll.63-82):** the signer signs `SorobanAuthorizationEntry` carrying an
    **authorized invocation tree** (contract, function, *args*, sub-invocations), a **nonce** unique among unexpired signatures,
    and an expiry; each match marks the node **"exhausted"** so it cannot be matched twice; `require_auth_for_args` lets the callee
    constrain which args are covered. That is {object, method, **args**, tree shape, uses, expiry} against our {object, method, uses}.
  - **Pact (READ, `pact-manual-capabilities.txt` ll.94-141; `pact-capability-theory-wiki.txt` ll.55-120):** a signature is scoped to a
    capability reference *with arguments* (`TRANSFER from to amount`); `with-capability` pushes granted tokens on the call stack and
    pops them (dynamic scope = our frame scope); **managed capabilities** carry "a diminishing amount of a certain resource"
    ("watering can"), i.e. our `uses`, but as a quantity, and the manager function decides how a use decrements it.
  - So a grant that names only (object, method) lets any frame holding it call that method with arbitrary args under the signer's
    authority. **Confused-deputy exposure:** a malicious object in the middle of a tree that the signer called for another reason
    can spend the grant on its own args, as long as the (object, method) matches. Soroban and Pact both bind args.
  - Daml's "Fetch needs a signatory or observer" has no analogue of ours: reads see the turn snapshot (ambient read).
    That is a visibility choice, not a bug (INFERRED), but it is where a privacy-sensitive object would need Daml's rule.

---------------------------------------------------------------------------------------------------------------------

### 5. SeRIF (Cecchetti, Yao, Ni, Myers 2021) and ECF (Grossman et al. 2018)

Files: `WPM/cecchetti-serif-reentrant-2021.txt`, `WPM/grossman-ecf-callback-free-2018.txt` (also `grossman-ecf-2018.txt`, identical
size).

#### SeRIF. What it permits and how it types it. READ.
- **Def 1 (ℓ-reentrancy, §4.1):** "If computation C1 calls computation C2, which then (possibly indirectly) calls C3, the execution
  is reentrant with respect to label ℓ if C1 and C3 are trusted at ℓ, but C2 is not." Defined by *integrity labels*, deliberately not
  by object boundaries: "We avoid object reentrancy because it relies on object boundaries — a fundamentally syntactic construct."
- **Fig 4:** (a) boundaries match; (b) a partly trusted object can create *object* reentrancy that is not ℓ-reentrancy (call into
  an untrusted part of A: harmless); (c) "mutually-trusting objects can create ℓ-reentrancy that is not object reentrancy",
  with the Parity Wallet (two famous attacks) as the example: "For an application split across A and C, if A calls B, then a call
  from B into C … is a reentrant call into the application."
- **Def 2 (§4.2):** "A program is ℓ-reentrancy-secure if every ℓ-integrity property, such as a program invariant, that holds for
  all non-ℓ-reentrant executions holds for all executions."
- **Permitted safe forms:** *tail reentrancy* (the last operation is the untrusted call; "performing all state modifications before
  calling other contracts" is the folk rule made principled), and Town Crier's `deliver`/`cancel` (§2.3: "Banning all reentrancy
  might seem appealing, but this solution would be overly restrictive"; status is updated before calling the untrusted callback).
  Enforced by an IFC type system plus run-time locks (§5, "combining a static IFC type system with a dynamic locking mechanism").
  Others they criticize: "some limit expressiveness by outlawing reentrancy entirely [14, 17]".

#### ECF (Grossman et al.). READ.
- **Definition:** a run is dECF if there exists "an equivalent execution of the contract without callbacks" from the same initial
  state to the same final state; sECF if all executions are. Omitting calls is allowed when constructing the equivalent run (§2.2).
- **Decidability:** Thm 6.1: checking dECF of an execution is undecidable (it is stated for dECFofs executions); Thm 6.6:
  decidable for objects over a finite variable domain; "non-ECF executions which occur in high depth of nesting must also occur in
  depth 2" (§1). Thm 7.1: if the object is sECF_fs then states reachable in a run of the most-general client include all
  quiescent-reachable states, so the object can be verified on its own; "the analysis simply assumes ECF, and does not require
  to prove it": a runtime that enforces dECF suffices.
- **Online check:** an instrumented algorithm, a *stronger* requirement than ECF "inspired by conflict serializability" (§2.3);
  Thm 8.13: acyclic IOC relation implies ECF (a **soundness** theorem); the time bound O(nm^2) is the §8.3 analysis (ll.1103-1164),
  overhead 3.38% time / 17% memory (Fig 17).
- **Measured (Fig 14, l.1221):** Ethereum 30.VII.2015-30.III.2017: 81,097,421 executions, **128,670 "callbacks"**, 3,315 non-ECF
  (0.004%); 30.III-23.VI.2017: 15,311,650 executions, **155,662 callbacks**, 6 non-ECF (<0.001%). Text l.1182: "only 10 executions
  out of about 100 million were legitimately non-ECF". All 2,288 ETC non-ECF were DAO copies.

#### Is our refusal stronger than needed, and what does it cost?
- **Stronger than ECF requires: yes, in two ways (INFERRED).** (1) ECF accepts re-entry that is equivalent to a callback-free run;
  we refuse all of it. In particular a re-entry that only *reads* the re-entered object is trivially equivalent to a callback-free
  run and costs nothing under ECF; in our model the re-entered frame reads the snapshot and its writes are deferred and
  conflict-checked, so read-only re-entry is harmless by construction. Refusing it buys nothing. (2) Our deferred writes already
  make the DAO shape impossible without the refusal: a re-entrant frame cannot see the outer frame's pending write, and a second
  write to the same slot aborts (R-CALLS D2). So the refusal is **belt over braces**, not the only mechanism. Keep it if cheap, but
  do not describe it as the mechanism that excludes re-entrancy attacks.
- **Cost of the blanket refusal, upper and lower bound (READ numbers, INFERRED reading).** Fig 14's `Callbacks` column counts
  invocations that were callbacks (re-entries into an object on the stack): 128,670 / 81.1M = **0.16%** of executions in the first
  window and 155,662 / 15.3M = **1.0%** in the second (growing: "the number of executions with callbacks increased significantly,
  indicating more complex contracts"). Blanket refusal would refuse up to that share if they were all valid; ECF refusal refuses
  <=0.004% (and ~1e-7 legitimate). The cost of OUR refusal is therefore **between ~1e-7 and ~1e-2 of executions on 2015-17 Ethereum
  and is not measured** (R-CALLS §2.5 reaches the same "unmeasured"). Only the ECF side is measured.
- **The mis-correction.** R-CALLS §2.5 ("My misquote… came from my final relay message. My report's text … says non-ECF.") and scribe
  note D1 claim the figure "10 of ~100M legitimately reentrant" is wrong and should be "non-ECF". The paper's own sentence is "only
  10 executions out of about 100 million were legitimately non-ECF" (l.1182). The original (CALLS E1) quotation is accurate; what is
  true is that "legitimately non-ECF" is a statement about ECF violations, not about re-entrancy, and that blanket refusal's cost is
  the `Callbacks` column. Use that column, not the 10.
- **The misfit that matters more (SHARPEN, Q1).** SeRIF Fig 4c/Def 2: invariants hold "for all executions" only if the notion of
  "re-entrant" tracks *trust*, not object identity. Our refusal makes Def 2 hold **for single-object invariants only**. FRONTIER
  l.731 says the guard "makes true" the theorem "every admitted re-entrant turn is equivalent to some non-re-entrant turn"; that
  holds trivially for object-level re-entry (there are none) and says nothing about A -> B -> C with A, C halves of an application.
  The law judges only the object's own (old, new, request); a cross-object invariant (A.balance + C.balance = K) is judged by no law
  that sees both. See §10.
- **Aptos Move is the production precedent for our rule, and documents its holes. READ**
  (`dedaub-aptos-reentrancy.txt`, Dedaub, 2025-09-17, "Insights from 300+ Audits"): the VM tracks `active_modules` and, when a
  module lock is active and the callee module is already active, errors "Reentrancy disallowed: reentering `{}` via function `{}` (module
  lock is active)", covering **direct and indirect** re-entry (A -> A, A -> B -> A). A second layer locks *resources* "preventing
  it from being accessed in a reentrant fashion". Documented bypasses: (1) **third-party resources are not locked** (Move 2.2
  closures): a contract whose state lives in another module's resource can be re-entered through a closure; (2) **direct
  closure-based re-entry within one module** bypasses the check ("the lock check only triggers on cross-module entries").
  These are exactly Q1 (state split across objects) and a "same object, different entry" analogue; the first says
  **a per-object lock is only as good as the guarantee that the invariant lives in one object**.

---------------------------------------------------------------------------------------------------------------------

### 6. Internet Computer, NEAR, EIP-150

Files: `WPM/dfinity-docs-message-execution-properties-2025.md`, `dfinity-docs-security-inter-canister-calls-2025.md`,
`dfinity-ic-interface-spec-2025.md`, `near-crosscontract-doc.txt`, `near-callbacks-security.txt`, `near-sigmaprime-xcc.txt`,
`objective-bend-grounding/eip-150.txt`.

#### IC, compared point by point. READ.
| Question | IC (source) | Ours | Verdict |
|---|---|---|---|
| Ordering | Property 3 (docs): "if a canister A sends m1 and m2 to canister B in that order, then, if both are accepted, m1 is executed before m2"; spec "Ordering guarantees": per *pair* of canisters, "start executing in order"; **responses have no ordering guarantee** relative to each other or to calls | per-(sender, target) FIFO | **AGREE** (same unit). The IC also guarantees order only of *starts*; say so. Ours is stricter on nothing, but we must not claim reply ordering |
| Queue & backpressure | `ic0.call_perform` returns `err_code` 0 or 2; 0 means "exactly one of the reply or reject callbacks will be executed"; 2 = refused, no callbacks | queue bounded 16, answered "queued {slot}" at once | **SHARPEN**: what happens at the 17th? IC refuses at the point of the call with a defined code; ours says "answered at once with queued", so full-queue must be a defined refusal of the yielding frame (Q4d) |
| Queued only if the sender succeeds | spec: "queues the call message … but does not actually act on it until the current WebAssembly function returns without trapping"; trap discards state and queued calls (Property 5) | sends yielded by a frame; turn aborts discard them (INFERRED) | **AGREE** |
| Reentrancy at await | **Every await is a commit point** (Property 2, 5): "code after the await … is executed as a separate message execution"; Property 4: interleaving of different calls has "no reliable execution ordering"; security doc: TOCTOU and double-spend bugs, locks that never release when a callback traps | `await` is a yielded Plan; resumed in a *later turn with a fresh view* | **AGREE** and this is the IC's whole bug class; R-CALLS §2.3 already says "the view gives freshness, not isolation". The IC security doc's remedy is a *journal as lock* ("the journal acts as a lock on the critical section"), which an activity cannot get from a view |
| Cycles attached | Property 10: for unbounded-wait calls, "the sum of cycles accepted by the callee, and those refunded to the caller equals the amount that the caller attached"; `call_perform` "deducts `MAX_CYCLES_PER_RESPONSE`" set aside for response processing; `ic0.call_cycles_add` deducted immediately, moved back if the call cannot be performed | postage escrowed into the inbox purse per send | **AGREE** on escrow-at-send + refund; **SHARPEN**: the IC reserves for the *response* as well as the request (spec l.2285: "the cost for the transmission of the largest possible response, and the cost for executing the largest possible response callback … partially refunded"). Who pays for the **reply resolution and the resumption** in ours? R-CALLS mentions an escrowed fee pair; the design text should show it covers the reply leg |
| Who pays for callee execution | callee's own balance: the call is delivered only if `liquid_balance(callee) ≥ MAX_CYCLES_PER_MESSAGE`, which is *deducted* then refunded (spec l.4794-4823); sender pays call overhead and bytes | sender's postage pays the callee's execution ("paid from the inbox purse only") | **DISAGREE by design, fine**: IC is the "reverse gas" model; ours is sender-pays. Sender-pays needs the declared envelope to bound the callee (we have it) and makes spam cost the sender (good) |
| Reply/reject | Property 7: "Every inter-canister call is guaranteed to receive a single response, either from the callee, or synthetically produced by the protocol"; reject may come from callee or ICP; a reject "doesn't guarantee that the receiver's state wasn't changed" | `broken` on failed delivery; slot: one decider, one deadline, one terminal decision | **AGREE** (one terminal decision), **SHARPEN** with the next two rows |
| Unbounded wait | Property 8/9: unbounded-wait call can be delayed "arbitrarily long if it is willing to put in the required cycles"; security doc ("Make sure there are no loops in call graphs", "calling untrustworthy canisters") gives a DoS and deadlock class; a canister with a pending callback cannot be cleanly stopped/upgraded | mandatory deadline on every await/slot | **Ours is strictly better** (INFERRED) |
| Bounded wait | Property 9/11: a bounded-wait call "may generate a reject response … even if the call is successfully delivered to the callee and the callee responds"; this is `SYS_UNKNOWN`; the real response "will get dropped"; attached cycles "may get lost" | deadline expiry decides the slot `broken` | **SHARPEN, the sharpest transfer (Q4a)**: our expiry decision is a `SYS_UNKNOWN` unless the queued message is *removed and its escrow refunded in the same transition*; if it can still be delivered later, the caller is told `broken` and the effect happens |
| Call-graph cycles | security doc: "Loops in the call graph (A->B->C->A) may lead to canister deadlocks" | `send` cycles cannot deadlock a frame (no waiting); `call` cycles refused by the re-entry rule | **AGREE** (INFERRED) |

#### NEAR. READ (`near-crosscontract-doc.txt` ll.4-5, 73-109; `near-callbacks-security.txt`).
- Calls are asynchronous; "The calling function and the callback execute in different blocks (typically 1-2 blocks apart)… If the
  external call fails, the calling function has already completed successfully; there's no automatic rollback."
- **Prepaid gas, declared by the caller per promise:** `with_static_gas(CALL_GAS)` for the call and a separate `CALLBACK_GAS` for
  the callback ("Always reserve gas for the callback. It executes in a separate receipt, so it can fail independently if it does not
  receive enough gas"), plus `with_unused_gas_weight` to divide leftovers proportionally (default weight 1; "If you forget that
  the default weight is 1, a callback or parallel promise can receive more of the remaining gas than you expected").
- **Compare to our `postage`:** NEAR's per-promise static gas is our "postage = the envelope each message is delivered under"; NEAR
  makes the *callback* envelope a second explicit number. Ours has one postage per invocation covering all sends. **SHARPEN:** one
  postage for all messages of an invocation cannot price a reply-resumption leg differently from a request leg; NEAR learned to
  separate them (a callback that runs out of gas is the classic failure). The weight mechanism is the cost of *not* knowing the
  envelope up front; our "priced on declared envelopes" avoids that (AGREE).
- NEAR's forged-callback and stake-twice races (VIA-SCHOLAR, CALLS E12; `near-callbacks-security.txt` is the source, not
  re-read in full) are the NEAR instance of "view gives freshness, not isolation".

#### EIP-150. READ (`eip-150.txt` ll.37-58).
"Define 'all but one 64th' of N as N - floor(N / 64)" ; a call that asks for more gas than that "call[s] with all but one 64th".
The rationale for EIP-114 (l.58): "replacing the call stack depth limit with a 'softer' gas-based restriction, thereby eliminating
call stack attacks." **Bearing on us:** the 2016 *call-depth attack* needed a callee failure the caller could *observe and handle*
(the attacker burns stack so the victim's inner call fails and the victim continues in a bad branch). We have a hard depth of 8 and
one declared envelope for the whole tree, so there is no 63/64 question. But the depth limit becomes attackable exactly if a frame
can catch a callee's refusal; R-CALLS says a callee's refusal aborts the whole turn (no catch). **Keep it that way and say so**
(INFERRED; ties to §1).

---------------------------------------------------------------------------------------------------------------------

### 7. Khan 2026 "Resume Means Resume"; Burckhardt et al. 2021 durable functions

#### Khan (`WPM/khan-resume-means-resume-2026.txt`, arXiv:2608.03836v3). READ.
- **Properties (abstract, §3):** six safety properties over the persistence API, "prefix continuation, effect exactly-once, fork
  determinism, checkpoint validity, consume-once, recovery determinism — plus fork-intent and liveness obligations". EO (Property 2)
  is a *safety* invariant (at-most-once); "the 'exactly' is supplied by pairing with the liveness obligation of Sec. 4".
  Liveness is `EventuallyCompletes` under **weak fairness only** (§4.1, ll.595-597, 678); its role is "closing a vacuity hole" so a
  framework with "Safety vacuous, progress dead" fails.
- **Lemma 1 (l.338) and Definition 2 (l.296-312):** FD (fork determinism) and CO (consume-once) are jointly unsatisfiable on
  identical traffic *unless* the wire carries a branch discriminator (FI, Property 7). Lemma 1 "is deliberately not an explanation of
  LangGraph's defect."
- **Measured (l.1044-1054, probe 168):** 40 cells, 400 protocol executions, "The gated effect fires 2,628 times where exactly-once
  predicts 400", saturation 1.0 in 36 of 40 cells; cross-host racers duplicate 10/10; abstract: saturation "never below 0.933".
  **The repair:** "an opt-in gate claims consumption in the shared store, serving one racer and refusing the rest before any node
  executes"; the paper states twice (l.1211-1213) "a repair placed at the persistence write path was powerless while the same repair
  placed at the durable-state read path succeeded." CALLS C6 and R-CALLS §1 are accurate on all of this (VIA-SCHOLAR, now READ).
  Caveat Khan states (l.1227): the no-latency claim is "not for every possible write-path design".
- **Fit:** R-CALLS §1's table (PC/EO/RD/CO yes, FD/FI "not offered, correctly", CV per step only, liveness no then fixed) is
  consistent with Khan's definitions. **SHARPEN:** weak-fairness liveness assumes some action eventually runs; for us that is
  "anyone may run `deliverMessage`/decide an expired slot". A chain with **no** such actor is not live; this is an economic fact
  (someone must be paid to run it), so the postage/escrow must *pay the runner of expiry and delivery*, else the liveness
  obligation is satisfied only in the model (INFERRED).

#### Burckhardt et al. (`WPM/burckhardt-durable-functions-semantics-2021.txt`). READ.
- **Thm 5.3 (l.1117):** "∼ is a weak simulation relation, when hiding commit messages" (compute-storage model vs high-level model:
  observably exactly-once). **Thm 6.4 (l.1239):** replay-based and storage-of-state models are bisimilar for deterministic code.
  Footnote on why simulation vs bisimulation (l.1229-1231). CALLS C1 correct.
- **Critical sections (§3.4.1, l.559-563):** a section must name all entities up front; "while executing, it can call only entities
  that are already locked, it cannot call sub-orchestrations, and it cannot enter another critical section." Global lock order is
  *implementation* (footnote 6, l.590: "acquiring the locks in a globally consistent order, one at a time"), not a semantic rule.
- **What the proofs exclude (§5, ll.980-990, "Future Extensions"):** "The compute-storage model currently does not include external
  calls or critical sections."
- **Fit:** durable-functions *calls entities from orchestrations* with replay of recorded task results (history), which is the
  resumption story our `await` replaces with a checkpoint digest. Their rule that critical sections may call only pre-locked entities
  is the nearest published relative of "a scoped grant {object, method, uses}" **for state**, not authority (INFERRED).

---------------------------------------------------------------------------------------------------------------------

### 8. Block-STM (Gelashvili et al. 2022/23)

File: `WPM/gelashvili-block-stm-2022.txt`. READ unless marked.

- **The guarantee.** Abstract ll.21-27 ("must yield the same deterministic outcome"), ll.56-58 ("The final outcome is equivalent to
  the sequential execution of transactions in the preset order in which they appear in the block"), **Corollary 2 (l.1333):** "A call
  to MVMemory.snapshot() after a thread joins returns the exact same values at exact same paths as would be persisted at the end
  of a sequential run of all transactions"; Lemma 1 (l.1141). Mechanism: preset order + multiversion data structure + ESTIMATE
  markers; a transaction that reads an ESTIMATE of a lower transaction suspends and is re-validated; no read/write sets needed in
  advance. **Termination is Theorem 2** (l.1364): "If threads keep taking steps … and VM.execute is wait-free, then all threads
  eventually join": termination rests on the VM being wait-free, which on a chain means gas/step bounds.
- **Gas hot-spot, READ (l.918-921):** "In Blockchain systems, there is usually an associated 'gas' cost to executing transactions. A
  single location for gas updates, could make any block inherently sequential. However, this issue is typically avoided by tracking
  gas natively, burning it or having specialized types or sharded implementation." Also (l.923 area) "Diem VM currently does not
  support suspending and resuming transaction execution." Measured: up to 30% overhead when completely sequential (l.107) and
  the 17x/20x figures (l.34-35).
- **Bearing on deterministic re-execution admission.** AGREE: re-execution equals the command's effects iff the effects are a
  deterministic function of (command, state). Block-STM's equivalence is to the *preset order*, which our admission has for free
  (log order; R-CALLS §2.5). The guarantee is only as strong as `VM.execute` being a pure function of its reads (Algorithm 3: the VM
  "does not write to MVMemory", reads its own write_set first, records a read-set of (location, version)).
- **Is our deferred-write call tree friendly to it? Largely yes (INFERRED).**
  - Frames' writes are buffered and applied at frame return, never visible to a callee: this is exactly Block-STM's per-transaction
    `write_set` (a read of a location in the txn's own write_set returns the txn's value, Algorithm 3 ll.84-85). Our rule is simpler:
    callees do **not** read the caller's pending write at all. No intra-turn read-your-writes across frames means a turn's read
    set is the snapshot reads only, so validation stays per-location.
  - No suspension inside a turn: a frame never suspends while a callee runs from its own stack (all depth-first, to completion).
    The Diem VM limitation quoted above is therefore not an issue for `call`; it *is* the reason `await` must be a turn boundary
    (it already is).
  - **Two precision requirements (SHARPEN, Q6):** (a) the read set must be recorded per (object, field), not per object, or the
    "judged against exactly the state the frame was shown" check over-conflicts; the design says "turn's snapshot", Block-STM needs the
    *versions actually read*. (b) The fee sink: "Fees priced on DECLARED envelopes" removes *measured gas*, but each turn still
    debits the signer and credits something. Where the credit lands (a protocol treasury, an inbox purse) is a single location every
    turn writes: the inherently-sequential-block pattern the paper names. Make fee/escrow credits per-turn deltas judged by
    commutative laws (the R-CALLS D2 "commutative delta" escape), not read-modify-write.
- R-CALLS §2.3's "version check = Block-STM validation, build once, delete `Record.reads`" is **AGREE** (VIA-SCHOLAR, consistent with
  the algorithm above).

---------------------------------------------------------------------------------------------------------------------

### 9. CALM (Hellerstein & Alvaro, "Keeping CALM", CACM 2020)

File: `WPM/hellerstein-keeping-calm-2019.txt`. READ for the theorem; analysis of our operations is INFERRED.

- **READ:** Def 1 (l.136) monotonic; **Theorem 1 (CALM), ll.142-146:** "A program has a consistent, coordination-free distributed
  implementation if and only if it is monotonic." Distributed deadlock detection is monotone ("decisions based on incomplete
  information are stable"); distributed garbage collection is not (§1.3.1-1.3.2). Bailis et al. (`WPM/bailis-coordination-avoidance-
  2014.txt`) Claims 11-14 (ll.447-448, 1173-1204): counter increments I-confluent with `>` threshold, **not** with `<`; decrements
  the reverse. CALLS F7 correct (VIA-SCHOLAR, READ).
- **What CALM does and does not say for us (INFERRED).** CALM concerns *coordination-free distributed* implementations. We have a
  consensus order, so we always "coordinate". The use of CALM is to say **which operations could run outside the ordered path
  (cross-domain, parallel admission, light-client reads) and which must stay inside**.

| Operation | Monotone? | Why |
|---|---|---|
| `send` appended to a per-(sender, target) queue, unbounded | **yes** | grow-only sequence, one writer per queue (the sender), so no merge conflict |
| `send` with the **bound of 16** | **no** | "queue has room" is a `<`-threshold on an increment (Bailis Claim 12: not I-confluent). Two concurrent sends can both see room |
| postage escrow (`balance >= price`, decrement) | **no** | `>` threshold under decrement (Bailis Claim 13). Needs an ordered check or an escrow-split (Bailis's "escrow" amortization) |
| `deliverMessage` (pop the head) | **no** | destructive and "anyone may run it": two runners race for one head; consume-once is exactly Khan's claim-at-decide |
| answer slot: "this slot has a terminal decision" | **yes** | a write-once register; once true stays true |
| answer slot: decide *before the deadline* vs expire *after* | **no** | needs the height order: "undecided as of h" is not monotone. The one-decider rule removes the race among deciders, not between decider and expiry |
| await consumption (nullifier bound to checkpoint digest) | **add: yes; test-then-act: no** | set insertion monotone; "act only if absent" is the non-monotone read (same shape as GC) |
| view reads in a resume | **no** | freshness of a read depends on the order of prior writes |
| a law judging (old, new, request) | **depends on the law** | laws of the form "new >= old" (a le atom) are monotone and checkable without the total order; "new + old = K" are not (INFERRED from R-CALLS/LAWS use of `le`) |

- **SHARPEN.** The *only* monotone, order-free mutations are unbounded appends and write-once decisions. Everything involving the
  bound, the purse or consume-once needs the log. So parallel/cross-domain execution of sends is limited by exactly the three
  features that make them safe (bound, escrow, one-shot). That is a design fact, not a defect: say which operations a cross-domain
  `send` may use (VIA-SCHOLAR, FRONTIER's cross-domain deal cells would sit here).

---------------------------------------------------------------------------------------------------------------------

### 10. eUTxO (Chakravarty et al. 2020) and Move resources, briefly

File: `WPM/chakravarty-eutxo-2020.txt`. READ.

- **The validator signature (l.120-133):** outputs are `(ν, value, δ)`; "to check that an input with redeemer ρ that is part of the
  transaction tx is entitled to spend an output (ν, value, δ), we check that ν(value, δ, ρ, tx) = true". "we pass the entirety of
  the transaction that attempts to spend the output … to the validator invocation", so a validator can enforce *contract continuity*.
  Later formalized as `TxInfo` (ll.375-420, 488: "For all i ∈ t.inputs, ⟦i.validator⟧(i.data, i.redeemer, toData(toTxInfo(t,i,l)))
  = true").
- **CEM (§4.1, ll.528-545):** `step : S -> I -> Maybe (S × TxConstraints)`; "There is no notion of initial state, since we would not
  be able to enforce it on the blockchain level"; final states are *halting* ("a CEM final state indicates that the machine must
  halt … will not appear in the UTXO set"). **Weak bisimulation** with the ledger, mechanised in Agda (abstract l.31-33; CALLS E6
  says "bisimulation": the paper says weak).
- **Compare to laws over (old, new, request).**
  - **AGREE** on shape: validator = predicate over (old datum, redeemer, tx context incl. proposed new datum); our law = predicate over
    (old state, new state, request facts). "Code proposes, law disposes" is the CEM's off-chain `step` plus on-chain validator
    (the validator only checks the proposed next state). eUTxO's `Maybe` result (no valid transition = refusal) is our law refusal.
  - **DIFFER (a):** the eUTxO validator sees the **entire transaction**, i.e. *all* other inputs and outputs, so multi-object
    invariants are expressible and enforced by *each* input's validator. Ours sees only this object's (old, new) plus request facts.
    **A law cannot see a sibling frame's write unless `request facts` carry it.** This is the same gap as SeRIF Fig 4c and Aptos's
    third-party-resource edge (Q1). eUTxO closes it by giving the validator the whole tx; if we do the same the law is no longer
    "decidable over one object" and writes of an object become coupled to every other write in the turn.
  - **DIFFER (b):** the validator runs only on *spend* (the old output is consumed). Creation has no validator: "no notion of initial
    state". Our law "judges every write to an object's declared state", including birth? If birth is not judged, the same
    initial-state hole appears (the Zoe base case in §3 and R-CALLS §2.2).
  - **DIFFER (c):** eUTxO validators are *spend authorizations tied to the consumed UTXO*, so concurrency is by construction
    (a UTXO is consumed once; no read-write conflict). Our laws run on an object whose state persists, so the consume-once is
    replaced by the turn order (Block-STM, §8).
- **Move resources, briefly. READ** (`blackshear-move-resources-2020.txt` l.1080-1083): Move avoids dynamic dispatch by "moving the
  dynamism to the withdrawal code" (the caller supplies the logic; the callee has no callback into it): the capability answer to
  callback hijack. Relevance: the cheapest anti-re-entry design is a call model with *no callback target the callee chooses*. In
  our `call`, the callee's target is chosen by the *caller's* method; a callee that calls the caller's other objects is the
  only dispatch freedom (INFERRED).

---------------------------------------------------------------------------------------------------------------------

### Corrections to earlier scholars

1. **CALLS A4 (OCapN): "No embargo. The spec has no embargo, and the implementation guide reports an ordering bug introduced by a latency
   optimisation."** The spec indeed has no embargo (no hit). The implementation guide has **no** such report: `grep` for bug/race/optimi
   returns nothing; its only ordering remark (l.531) is that gift *deposit vs withdraw* order "does not matter". The embargo mechanism
   is in `capnproto-rpc.capnp` (`Disembargo`, ll.688-735). Mis-citation; the lesson (order belongs in the semantics) may still be right
   but is not sourced from these files.
2. **CALLS A1: broken promises "contagious, like NaN (§16.5)".** "Broken Promise Contagion" is the §16.5 title and the mechanism is
   as described; the NaN analogy does not appear in the thesis. Embellishment, harmless.
3. **CALLS E1: "Checkable online in O(nm^2) (Thm 8.13)".** Thm 8.13 is the soundness statement (no cycle in the IOC relation implies ECFc);
   the O(nm^2) bound is the §8.3 time analysis (ll.1103-1164). Also Thm 6.1 is stated for dECFofs executions.
4. **R-CALLS §2.5 and scribe note D1 "correction" of the Grossman figure is backwards.** The paper does say "only 10 executions out of
   about 100 million were legitimately non-ECF" (l.1182; also l.73-74 "just one such legitimate non-ECF contract"). What R-CALLS should
   have flagged is that this measures ECF violations, not re-entrancy; the relevant cost of blanket refusal is the `Callbacks` column
   of Fig 14 (0.16% then 1.0% of executions). See §5.
5. **R-CALLS OPEN 1, "Production precedent: … Tezos depth-first (CALLS E2)" for synchronous cross-principal `call`.** Tezos is not a
   synchronous-call precedent. `tezos-michelson-doc.txt` ll.472-473: "Internal operations are run … after the contract execution, in
   depth-first order … any contract calls emitted by a contract C are executed after contract C successfully finishes execution
   returning its result". It is `send` with depth-first delivery inside one atomic operation. The synchronous value-returning
   precedents in the list are Mina (VIA-SCHOLAR, CALLS E18, not re-read) and Daml exercise trees (READ here: but in Daml the callee sees
   live state, with the consumed contract already archived: the *opposite* of our snapshot rule).
6. **CALLS C1 (durable functions): "Locksets are declared, acquired in a global order … What the proofs exclude: external calls, critical
   sections and *versioning*".** The global order is an implementation footnote (l.590), not part of the semantics; and "versioning"
   appears nowhere in the paper (0 hits for versioning/upgrade); the excluded features are external calls and critical sections
   (§5 "Future Extensions", ll.980-990). The versioning exclusion is the scholar's inference.
7. **CALLS E6 (eUTxO): "Bisimulation with the ledger".** The paper claims a *weak* bisimulation (abstract). Minor.
8. **FRONTIER F1, l.731: "the SCHOLAR-CALLS re-entry guard makes [SeRIF's Def 2-style theorem] true by refusing re-entry".** True only for
   *object* re-entry; SeRIF's Def 2 is stated over trust-labelled ℓ-reentrancy and Fig 4c is the case an object guard misses. The Lean
   statement to prove must be about invariants of a *named* object, not "every re-entrant turn".
9. **R-CALLS §4 OPEN 1: "Grossman found 0.004% non-ECF executions on Ethereum history (E1)" as support for sync calls.** The figure is
   correct for the first window (3,315 / 81,097,421), and for the second 6 (<0.001%); but it measures an *ECF monitor's detections* (a
   stronger-than-ECF check) in a 2015-17 chain with call-depth heuristics in place ("attacking is harder as Ethereum employs … heuristics
   to limit callbacks", l.1320-1322), so it is a weak support for "refusal is cheap".
10. **Confirmed (no correction needed):** CALLS A1 turn / plan interference / E-ORDER / CAUSAL-too-strong; A2 defensively consistent;
    A5 Disembargo and Tribble race; A12/A13 Zoe; C6 Khan (all numbers); E4 IC; E7 Block-STM (Corollary 2, gas hot-spot quote); E5 Daml
    non-transitive; FRONTIER Zoe `isOfferSafe` formula and exit shapes; the SES clean-stack quote (`endo-ses-readme-2026.md` l.837-840).
11. **Not verified:** Soroban "re-entry disallowed by default" (memory, no primary text found in three Soroban pages and Kagi); Mina
    (CALLS E18) and Orleans (CALLS B2/B3) quotes; NEAR forged-callback race text (only the doc's headline read).

---------------------------------------------------------------------------------------------------------------------

### Sharpest questions

**Q1. Where does a cross-object invariant live, and who judges it?** (SeRIF Fig 4c + Def 2; Aptos third-party-resource edge; eUTxO
validator sees the whole tx.) Laws judge (old, new, request) of ONE object; re-entry refusal is per object. An application split
across objects A and C (A calls B calls C) is exactly the Parity/Uniswap shape SeRIF names, and the exact bypass Aptos's own
auditors list. Either (a) declare that an invariant must live in one object and say so in the object model, with a lint over
published packages, or (b) give laws access to the sibling frames' writes in `request facts` (eUTxO's whole-tx context) and accept
that a law is then coupled to the turn's other writes. The design currently says neither, and FRONTIER's "the guard makes the SeRIF
theorem true" is wrong for this case.

**Q2. Sibling visibility and failure inside one frame.** (E §13.1, Daml §3.3 step 4, EIP-150.) The design says a callee never
sees a caller's *pending* write and writes are judged against "exactly the state the frame was shown". Undefined: (i) after callee
B1 returns, does the caller's continuation, and a later sibling B2, see B1's write? If yes the rule is asymmetric and B2's judged
state is not the turn snapshot; if no, a caller cannot use any effect of a callee, only its result. (ii) Is the "state the frame
was shown" the turn-start snapshot or the state at call time? (iii) Can a frame catch a callee's refusal? If yes, the EVM
call-depth-attack class returns (EIP-150's reason for removing the depth limit) and "aborting the wrong plan" becomes
"continuing the wrong plan". The answers decide whether Block-STM read-set recording (§8) is per object or per frame.

**Q3. Does a scoped grant bind arguments?** (Soroban authorized invocation trees with args + nonce + "exhausted"; Pact capabilities
with args and managed quantity; Daml's callee-declared consent.) {object, method, uses} lets any frame holding the grant call that
method with arbitrary args as the signer, including a malicious object in the middle of a tree the signer called for another
purpose (confused deputy). Soroban and Pact both bind the args (Soroban also the sub-invocation shape and an expiry/nonce). What is
the grant's matching rule: args predicate, tree position, expiry height? And which of Daml's consent semantics (callee-declared)
vs delegation semantics (signer-granted) does `request/subject` mean?

**Q4. Send protocol edge cases, all with direct precedent in the IC and CapTP.**
(a) **Expiry vs delivery (IC `SYS_UNKNOWN`):** when a slot is decided `broken` by deadline, is the queued message removed and its escrow
refunded *in the same transition*? If it can still be delivered, the caller is told `broken` while the effect happens.
(b) **Forwarded-on-resolution vs direct sends (Cap'n `Disembargo`, Miller §19.2):** a message queued on a reply slot and a later direct
send to the resolved target; where does the forwarded message enter the (sender, target) FIFO, and is a reference passed in `args`
a "fork" (Miller) that lets the receiver overtake the sender's queued messages?
(c) **Datalock (Miller §16.3):** can the deciding delivery of slot S send to S, and what happens then?
(d) **Bound of 16:** the IC refuses at the call with a defined error; ours is "answered at once with queued". What does the 17th
send do (refuse the yielding frame? abort the turn? `broken` slot)? It is non-monotone (CALM §9) so it needs the log.
(e) **Who pays for the reply resolution and resumption** (IC reserves `MAX_CYCLES_PER_RESPONSE`; NEAR makes callback gas a separate
number)? One `postage` per invocation cannot price the reply leg.

**Q5. Seats: is "exit no clause can forbid" an invariant over reachable states?** Zoe's guarantee is an induction (initial
allocation = escrowed give; every path checked; exit pays the *current* allocation), it permits `waived` exit, and the seat
manager's mint path commits with no offer-safety call. For us: what kernel action establishes the first balance, which entry
points (mint, burn, fee debit, postage escrow, refund, `call`-tree transfers) call the seat law, and is `exit` defined as "pay
the current balance" so that a contract cannot choose the payout? Without the reachable-state theorem this is the same hole as
R-CALLS §2.2.

**Q6. Where do fees and purses land, and is the read set per field?** (Block-STM gas hot-spot; Bailis Claim 13.) Declared-envelope
pricing removes measured gas, but every turn still credits some sink and debits a purse. If these are read-modify-write on one
location, Block-STM's "inherently sequential" pattern is rebuilt by our own fee design, and `postage` escrow (`balance >= price`)
is a non-monotone check on every send. Should fee/escrow credits be per-turn commutative deltas judged by a `le`-style law, and must
the recorded read set be (object, field, version), not "the snapshot", for parallel admission to be correct?


# Appendix C — GPT-6's earlier LTUO audit (verbatim)

```text
bw from gpt6:



<pasted_content id="1402">
hi :) **My verdict is: Objective Bend has the right computational heart, but its authored type system still restricts some of the modularity LTUO is trying to make available.** There is a substantial difference between “correctly implements a calculus of lazy open recursion” and “lets independently written specifications participate in the strongest forms of modular programming described by LTUO.” I found good evidence for the first, and concrete limitations in the second.  

I pinned the implementation review to **`259a2fb`**, rather than following a moving `main`. I inspected the reference semantics, demand machine, typing rules, elaborator, C4 implementation, and example expectations. **This is a source-level audit, not an independently completed Lean rebuild.** The new regression witnesses below are predictions from that inspection, not claims that I executed them.

The most revealing comparison is actually in LTUO itself: Faré calls §8.2.1 **“Trivial Non-Modular Types for Modular Extensions.”** Parts of Objective Bend’s *surface* type system are much closer to that starting point than the guide’s discussion of future self types might initially suggest. 

## 1. First, how to think in Objective Bend

An extension is not primarily a class, a method dictionary, or a completed object. It is a computation that says:

> Given the eventual context in which I will participate, and what has been constructed beneath me, here is my contribution.

In Objective Bend’s argument order:

```text
extension : FinalSelf → Inherited → Provided
```

`self` means **the eventual whole**, including extensions composed above the current one. `super` means **the inherited result below this particular extension**, constructed using that same eventual whole.

The core’s composition operation is:

```text
mix(lower, upper) =
  λself. λsuper.
    upper self (lower self super)
```

That equation is actually present as `mixBody`, not merely promised by the documentation. 

The crucial distinction is that **composition transforms specifications before they are closed**. You do not first finish two independent objects and then merge their already-bound methods.

Closing happens with:

```text
fix(spec, seed)
```

A useful mental model is the recursive binding:

```text
let rec result = spec result seed
in result
```

But this is an operational construction, not permission to choose any mathematical solution of an equation. The reference semantics unfolds the computation; the demand machine ties a heap cell back to itself.  

### The example that makes `self` and `super` click

The repository’s review example has three contributions:

```text
record Review:
  review(value: Nat) -> Nat
  twice(value: Nat) -> Nat

spec Base for Review:
  def review(value: Nat) -> Nat:
    value + 1n

spec Twice for Review:
  requires review(value: Nat) -> Nat
  def twice(value: Nat) -> Nat:
    self.review(self.review(value))

spec Augmented for Review:
  def review(value: Nat) -> Nat:
    super.review(value) + 1n
```

They are combined as:

```text
fix(compose(Base, Twice, Augmented), seed)
```

Here, the rightmost contribution is the outermost wrapper. The actual repository example supplies a seed with identity implementations of both methods.  

Now derive the result:

```text
Base.review(x)       = x + 1
final.review(x)      = Base.review(x) + 1 = x + 2
final.twice(3)       = final.review(final.review(3))
                     = final.review(5)
                     = 7
```

**`Twice` sees the augmentation even though it was written independently of it.** That is the point of open recursion.

Conversely, replacing `super.review(value)` in `Augmented` with `self.review(value)` would call the final method again—namely the augmentation itself—rather than the implementation beneath it. The distinction is not “current class versus parent class”; it is **final context versus inherited computation**.

There is an important wrinkle in that seed: needing a fully populated `Review` seed is a feature of the current `spec … for Review` typing, **not an inherent requirement of this model of OO**. We will return to that.

### Laziness is part of the meaning

A record can have a useful field and a divergent field without the latter poisoning every observation of the record. Similarly, an unused argument need not run.

The machine implements this with separate field thunks, delayed application arguments, and cached results. Forcing an already-evaluating cell produces a blackhole/divergence outcome. This is a real sharing implementation, rather than simply a substitution interpreter described as lazy. 

Also, do not infer “everything short-circuits” from “the language is lazy”: in this edition, `&&` is a strict binary primitive, whereas `||` lowers to a conditional. Use `if` when guarding a potentially divergent branch. 

## 2. The central mechanism really is implemented in the right way

On the important foundational questions, I found the right machinery:

**One final self.** `mixBody` passes the identical final-self expression through both layers.

**Whole super.** The upper layer receives the result of applying the lower layer, not just a specially selected “previous method.”

**A real recursive knot.** The machine’s `fix` allocates one tied address; it does not independently instantiate a fresh self for each layer.

**Lazy structure.** Records, specifications, and prototype components have separately delayed representations. Extending a record forces its outer record structure, but not all its fields.  

Nor is everything secretly restricted to method overrides. Ordinary `extension` values can construct scalar results and capture ordinary arguments. The `GenericExtension` example manufactures extensions from a `delta`, returns them from functions, and composes the resulting values. The heterogeneous example genuinely composes:

```text
XYZ → X  → XY
XYZ → XY → XYZ
```

before closing the result. These are meaningful demonstrations of functionality beyond a conventional method dictionary.  

One superficial difference from the book is harmless: Faré’s presentation uses an inherited-first argument convention in the relevant equations; Objective Bend uses self-first. The operations correspond after permuting arguments and composition conventions. That is not a semantic defect. [Faré](https://fare.tunes.org/files/cs/poof/ltuo.pdf)

**I would preserve this kernel.** The problems I found are primarily about what authors can express through its public language, and what additional claims its proofs establish.

## 3. The largest LTUO gap is independently modular typing

This is where I would push considerably harder than the existing roadmap.

Faré’s chapter 8 explicitly distinguishes typing an extension against one already-known complete context from typing it without knowing unrelated fields that future collaborators will introduce. His starting-point types already support heterogeneous inherited/provided values; that alone does not deliver modular typing. 

### `spec S for T` currently assumes much more than its contribution

The elaborator gives both implicit parameters the same target type:

```text
self  : T
super : T
```

and gives the resulting layer type:

```text
T → T → T
```

This comes directly from `selfSuperParams`, `globalType`, and `layer`. Record agreement is exact canonical equality, not general width subtyping.  

Consequently, a specification that contributes one method still expects an inherited value already typed as the whole `T`. This explains the placeholder methods in the review example’s seed.

The lower-level `extension` form improves matters: inherited and provided types can differ. But the heterogeneous example still names the same concrete `XYZ` as `self` in every layer. It demonstrates **heterogeneity along the inheritance chain**, not abstraction over arbitrary future contexts.

That distinction matters when someone adds a fourth field tomorrow. Can yesterday’s independently typed extension be reused without rewriting its self annotation to name tomorrow’s completed record?

In the inspected source path, that ability is not generally exposed.

### Core type variables are not automatically source-level polymorphism

`ObjectiveBendTypes.lean` contains useful machinery: rigid variables, bounds, retained row tails, type substitution, and an `ExtensionFamilies` structure. Those are real ingredients. But their existence is not equivalent to an authored binder that lets a programmer quantify over future self types or unknown inherited rows. 

A particularly clear boundary is recursive records. A type such as:

```text
record Node:
  combine(other: Node) -> Node
```

runs into the elaborator’s explicit refusal:

```text
recursive row annotation requires explicit future-row binder
```

Yet the inspected surface type resolver does not provide that binder. Recursive sums have separate support; that does not solve recursive record/self typing. 

This is exactly why I would not treat `binary_method_changes_with_future_self` as evidence that the *authored language* supports independently reusable binary-self methods. That theorem establishes a fact about type substitution. It does not exhibit such a source program passing through the compiler. 

### Checking `requires` is necessary—but not the whole repair

At present, `requires` is metadata. The elaborator preserves it in the interface label rather than using it as the authoritative typing contract for composition. 

That **does not by itself refute the no-refusal theorem**. Actual field accesses still have to typecheck. The present system often obtains safety by demanding *more prior knowledge*—the complete target type—rather than by checking a minimal dependency interface.

The stronger design obligation is something like:

> An extension is checked using only its declared inherited and final-context assumptions; it preserves whatever unrelated inherited structure its contract promises; composition reconciles those assumptions; closing the knot discharges the final-context requirements.

Those are several obligations, not one `requires`-row lookup.

I would therefore promote **authored future-self/row abstraction and its composition rules** above several of the roadmap’s smaller surface additions. Simply adding unchecked flexibility would be worse; the goal is to retain the safety theorem while making its premises genuinely modular.

## 4. A concrete API problem: `Specification<T>` is not closed under `compose`

This is the clearest implementation-level witness I found.

Consider the natural helper:

```text
edition ObjectiveBend 1

def twice(e: Extension<Nat>) -> Specification<Nat>:
  compose(e, e)
```

**My source-derived prediction is that this is rejected by the checker.** Not because composing `e` with itself is invalid, but because the declared result type and the composition result have incompatible metadata types.

The elaborator interprets `Specification<T>` using metadata of this shape:

```text
{
  name: String,
  interface: String,
  laws: {}
}
```

But `compose` constructs metadata of this shape:

```text
{
  operator: String,
  inherited: <type of left operand>,
  wrapping: <type of right operand>
}
```

The metadata is part of the specification’s exact type. There is no general conversion between those shapes.   

There is a related problem even without composition: adding a `law` changes the exact `laws` row, so a named specification with a law does not have the empty-law metadata type expected by `Specification<T>`.

This does **not** mean specifications are never first-class. A particular composition-shaped result can be inferred in some contexts, and ordinary extension values clearly are higher-order. The narrower, important finding is:

**The advertised `Specification<T>` annotation is not a stable common interface for specifications produced by the language’s own composition operation.**

You can express the behavior using an ordinary extension wrapper:

```text
def twice(e: Extension<Nat>) -> Extension<Nat>:
  extension(self: Nat, super: Nat) -> Nat:
    e(self, e(self, super))
```

But that workaround does not retain the reflective composition structure.

I would treat this as an API-design issue, not merely an inference inconvenience. Possible repairs include a metadata parameter together with an opaque/existential public interface, or a uniform inspectable metadata representation. Neither should be adopted blindly: the choice determines what reflection can observe and what clients can depend upon.

## 5. A sophisticated reading also asks what reflection and extensibility actually mean

### A prototype pair does not establish provenance

The core’s:

```text
prototype(spec, target)
```

is a lazy pair. Its typing rule checks the components, but does not establish that `target` was produced by enacting `spec`. The components need not even be related by a construction invariant. 

That is perfectly reasonable as a low-level representation constructor. But it means:

> `reflect(p)` retrieves the stored specification; it does not, by itself, prove how `targetOf(p)` was constructed.

A higher-level prototype constructor could establish a relationship by construction. For ordinary nonrecursive pairing, that could relate projection to `fix(spec, seed)`. More elaborate prototype models need a more carefully stated relationship.

Faré’s recursive conflation distinction is relevant here: wrapping a completed knot, schematically `R(Y M)`, differs from placing the wrapper inside the knot, `Y(R ∘ M)`. In the latter case, recursive self-reference also goes through the wrapper. [Faré](https://fare.tunes.org/files/cs/poof/ltuo.pdf)

Objective Bend’s pair provides ingredients for constructions of this kind; it does not automatically implement all of them. In an ordinary record-target spec, `self` is the target record—not automatically a reflective prototype supporting `reflect(self)`.

**This is not a reason to reject the core. It is a reason to distinguish “prototype representation exists” from “the intended reflective object model has been implemented.”**

### Composition has behavioral algebra and observable history

By expanding `mix`, both associations produce the same extension behavior:

```text
C self (B self (A self super))
```

But surface `compose` retains its construction tree in metadata. Thus:

```text
compose(compose(A, B), C)
compose(A, compose(B, C))
```

have differently structured provenance—and generally differently structured metadata types—even when their target behavior agrees. 

That is not inherently wrong. It means the language needs an explicit distinction between **equivalence of extension behavior** and **equivalence of reflective specifications**.

An optimizer cannot simply say “composition is associative” and rearrange every program if programs can inspect the association history.

There is a further distinction once resources matter: equal answers when both runs finish do not imply equal heap use, equal tick consumption, or equal outcomes under one fixed budget. The demand machine explicitly exposes suspension as distinct from completion. 

I would write down the permitted observers before adding more reflection or asserting broad optimization laws.

### The package knot is a start, not yet an extensible ecosystem

The package elaborator does build a global recursive namespace, and its root is represented as a specification that overlays inherited fields. That is a useful architectural choice. But the documentation also says that source code cannot yet name another package’s root. 

Here is the stronger acceptance test I would use:

> Package A defines a datatype and some behavior. Package B independently defines another protocol. Package C adds their integration by extending a shared specification—without editing either package—and existing references inside the resulting ecosystem see the final extended definitions.

This tests substantially more than “an AST node somewhere contains a specification.”

It requires the source-level access path, suitable open types, coherent rebinding, and a defined scope for the resulting ecosystem. Merely exposing a root name without addressing those other requirements would not finish the job.

Similarly, named C4 ancestry and ordinary computed composition are distinct mechanisms. The former currently resolves statically identified declarations; the latter operates on values. Having both is useful, but it does not imply that arbitrary computed specification values can participate in all the declared-ancestry machinery. 

## 6. What the proofs establish—and what they do not

The repository has substantial core-level proof work. Its documented theorem statements cover machine/source agreement, preservation, absence of specified refusals for checked programs, observations of completed runs, and typed activity resumption. Those are significant properties. They still allow divergence, blackholes, and resource suspension. 

But there is an important terminological trap:

**In many of these theorems, “source semantics” means the reference semantics of the Core4 term—not an independently defined semantics of `.obend` source text.**

The front-end documentation explicitly acknowledges that no independent surface semantics exists. Its adequacy results connect the accepted packet to the elaborator’s actual term and then to the checked core execution. 

So the situation is approximately:

```text
.obend source
     │
     │ parser / elaborator / ancestry lowering
     │ no independent surface-semantics preservation theorem
     ▼
checked Core4 term
     │
     │ substantial machine/reference-semantics theorems
     ▼
observations
```

Why care? Imagine an erroneous compiler that reverses two homogeneous extension layers. Its output might still be well typed. The machine could execute that output perfectly faithfully. A receiver replaying the same compiler could obtain exactly the same bytes.

All those guarantees would be useful—and none would establish that source-level `compose` meant the intended order.

That is an illustration of the proof boundary, **not an allegation that the current compiler reverses composition**.

### C4 needs more than the currently named invariance property

The C4 implementation is present. `OrderedPresentationInvariant`, however, is a proposition being stated, not a proved general theorem; the implementation points to finite vector and randomized evidence. 

Its choice of *ordered* presentation is correct: parent ordering is semantic input. Demanding a renaming-equivariant strict order for every bare symmetric graph would be the wrong specification.

However, **renaming invariance alone would not establish C4 correctness anyway**. An algorithm that refuses every graph is renaming-invariant.

The useful proof package also needs appropriate well-formedness premises and properties about ancestor coverage, duplicate elimination, precedence constraints, suffix preservation, and the relationship between the resulting list and method-combination behavior.

### “Law,” “requires,” and “guarded” need separate promises

A `law` is retained Boolean-valued code, not a discharged proof. A specification containing `law impossible: false` is therefore not inherently a rejected specification. That is documented behavior, not a contradiction in Lean. 

Likewise, the roadmap’s proposed guardedness condition needs care. Guarding resident self-recursion beneath `perform` does not alone prevent an unrelated pure helper from looping before the yield, or a demanded plan component from diverging. A per-turn termination claim must control **all demanded recursion relevant to the turn**, not only syntactic resident self-calls. The existing safety theorems do not already supply that productivity claim. 

## 7. How I would learn it—and what I would change first

For learning, I would start with **captured scalar extensions**, then the **review/self/super example**, then **heterogeneous rows**, and only then ancestry and method combination. That progression separates the computational model from the extra mechanisms built around it.

Use `preview-cohort.json` as the guide to which examples are supposed to succeed. The tests directory includes intentional refusals: notably, `ReflectLazyPrototype.obend` contains a scalar-target `spec`, and the preview cohort explicitly expects that fixture to be refused. It should not be mistaken for a successful typed reflection tutorial. 

Also, the overview’s roadmap is not fully current. The reviewed commit registers activity Host operations that the overview still describes as unavailable. Registration is not evidence that I verified end-to-end deployment, but it is enough to show that the roadmap cannot be treated as a precise status ledger. 

My implementation priorities would be:

1. **Give specifications a usable public type interface closed under composition.** Resolve the metadata problem while explicitly preserving—or deliberately restricting—the reflection contract.
2. **Expose genuine modular typing to authors.** Future-self/row parameters, independently checked assumptions, preserved inherited structure, and checked closure at `fix` should work in actual `.obend` programs.
3. **Prove the next semantic boundary.** Define the relevant surface behavior and connect ancestry/composition lowering to it, rather than treating typing and replay as substitutes.

I prepared **11 characterization probes**, with positive controls and witnesses for the metadata, future-self, recursive-record, `law`, and `requires` boundaries:

objective-bend-ltuo-probes.zip[Download the Objective Bend / LTUO probe pack](sandbox:/mnt/data/objective-bend-ltuo-probes.zip)

It includes `.obend` sources, source-derived expected outcomes, and a runner using the actual Lean front end’s batch command. **The new Objective Bend probes have not been executed here.** The runner checks parsing/elaboration/typing, not runtime evaluation; the README keeps those evidence classes separate.

**Bottom line:** I would not throw away Core4 or call this fake OO. It implements the right central mechanism. But the strongest LTUO claim should be earned by an independently authored extension that survives an unknown future context, a composite specification that crosses a stable higher-order interface, and an extended namespace whose existing collaborators all see the final whole. Those are more consequential milestones than adding more object-oriented syntax.
</pasted_content id="1402">

```
