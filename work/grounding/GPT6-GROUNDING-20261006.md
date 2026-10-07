# GPT-6 grounding packet — Objective Bend's design commitments against the literature (2026-10-06)

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

## Files

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

## Executive summary

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

## The sharpest questions, ranked

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

## How to use this with GPT-6

- Send `00` first. It is GPT-6's own audit with our response, and it asks GPT-6 to say whether LT2 meets its
  bar.
- Then send the ranked questions with their topic files. Each topic file stands alone: design, commitments,
  literature, then questions.
- The worker notes in `lit/` carry the verbatim quotes, in case GPT-6 disputes a reading.
- Every code claim is pinned to `4ef4e808`. If main moves before the round, re-check the four "not on main"
  notes in topics 00, 01 and 03.

## Also in this packet: 08-swarm-work-lifecycle.md (Ember asked: how should work items move through the swarm?)

## Addendum (root, 10-06): a new finding for the transparency topic
ForcingTransparent is now proved on the DEPLOYED kernel (segment heap limits counted from the segment's own start; growth declared
and paid at delivery, refused `heapUncovered`; StoredComplete names the run's own retained yield; the absolute-limit version is
refuted in-kernel by `absolute_limits_refuted`). But the CONVERSE is false: a stored (forced, settled, collected) checkpoint can
COMMIT where the program's own lazy run is refused, by tick exhaustion or by a result-extraction budget fault, because cached
cells save ticks and plan budget. That the difference is "resources only" is unproved (cv 01a113f0-4ff6).
QUESTION for GPT-6: is a resource-monotone, one-directional simulation the right contract for checkpointed lazy execution
(cf. Launchbury's natural semantics, Sestoft's abstract machine, cost-semantics work on call-by-need), or should admission be defined
against a cost model in which forcing is free, making both directions equal? What do durable-execution systems (Temporal, Khan)
promise about replay costs?
