# LIT-W2: laziness, effects-under-sharing, guardedness, reflection, serializable continuations

Worker W2, DEPUTY-GROUNDING (Mini swarm). Literature only; no builds, no code edits, no git.
Downloads: `~/paperbin/objective-bend-grounding/<name>.pdf` plus `<name>.txt` (`pdftotext -layout`).
Papers already in `~/paperbin/world-program-model/` are cited from there.

Tags: **READ** = I read that passage in the extracted text. **INFERRED** = my reasoning, or a secondhand report inside a paper I did read.
Page numbers are PDF page indices unless "printed" is stated. For the two-column layout PDFs I re-extracted without `-layout` to read in order.

## 0. Corpus status (what was actually obtained)

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

## A. Laziness

### A1. Launchbury 1993
John Launchbury, "A Natural Semantics for Lazy Evaluation", POPL 1993, pp 144-154.
Read: abstract, §1-2 (the `let f = λx. f x` black-hole discussion, p. 148), §5.2 (denotational semantics, Correctness §5.2.2, Adequacy §5.2.3). Correctness and adequacy statements via Breitner 2017.

Mechanism (READ). "The only computational structure we introduce is a set of bindings which corresponds closely to a heap." Application is restricted to a variable argument (`e x`), so every argument becomes a named heap binding. A `let` allocates bindings; evaluating a variable reduces its binding and writes the value back, so each binding is evaluated at most once. The judgement is `Γ : e ⇓ Δ : v`, heap in, heap out. Correctness is stated against a standard denotational semantics: `⟦e⟧{{Γ}} = ⟦v⟧{{Δ}}` (Breitner Thm 1). Adequacy: if `⟦e⟧{{Γ}} ≠ ⊥` then some `Δ, v` exist with `Γ : e ⇓ Δ : v` (Breitner Thm 3, §4). Launchbury notes that a self-dependent binding is a detected black hole only when the variable rule removes the binding during its own evaluation, and that the loop `let f = λx. f x in f 2` is not a black hole at all (p. 148). Breitner confirms that rule VAR "models blackholing by removing a binding from the heap during its evaluation" (§2.3.2).

Bearing on Objective Bend: **AGREE** on the overall shape, with three **SHARPEN**s.
1. Launchbury has native recursive `let`, so a cell may point to itself. This is the right ancestor of `fix` tying a heap address to itself, much closer than the Ariola-Felleisen calculi (see A3). The reference-vs-machine theorem in the design is a Launchbury correctness theorem with the heap-as-cell structure. READ.
2. Adequacy is existential: derivation exists iff denotation is not bottom, with no bound on derivation size. This matches "completeness is finite but has no resource bound". Breitner's resourced semantics is the only route in this literature to a step-indexed version (Lemma 8: `N⟦e⟧{{Γ}} r ≠ ⊥` implies a derivation) and the proof is hard (A2). If the design wants a bound it needs an explicit cost model; the machine step count is not given for free by the natural semantics. INFERRED.
3. Blackholing is a feature of the operational side that the denotation does not share. Breitner Lemma 6: only the weaker "denotational blackholing" holds. For OB: `bad = self.bad` forced is a blackhole in the machine and ⊥ in the reference, which agree as ground observations (no value), but any observer that can distinguish "blackhole" from "ran out of fuel" is outside the theorem. INFERRED.

### A2. Breitner 2017
Joachim Breitner, "The Adequacy of Launchbury's Natural Semantics for Lazy Evaluation", J. Functional Programming 2017 (preprint). Read §1, §2.3, §3, §4.1-4.3.

Mechanism (READ). First rigorous, machine-checked (Isabelle) adequacy proof. It skips Launchbury's intermediate natural semantics and works with a resourced denotational semantics plus a change that "ensures that while evaluating an expression with finite resources, values on the heap are used with fewer resources" (§1). Two incidental findings matter: Launchbury's own Theorem 2 (correctness, generalized) "is false" as stated (§2.3.3), because an environment ρ carrying compatible but better information about a heap variable breaks `ρ ⊔ ⟦v⟧`; the fix is a right-biased update `++S`, and closedness of the judgement (`fv(Γ,e) ⊆ dom Γ ∪ L`) is required (§2.3.2).

Bearing: **SHARPEN**. The published, long-trusted correctness theorem for lazy heaps was false until formalised, and the failure was precisely about *which environment/heap the theorem quantifies over*. The OB theorem "a finished bounded machine run equals the reference evaluation for ground observations" has the same exposure: a statement about heaps is only as good as its side conditions (closedness, freshness, which cells the observation may read). Risk: state the quantifier over initial heaps/environments explicitly and make the Lean statement name it. Question: does the Lean theorem quantify over arbitrary initial heaps (the ρ in Breitner's counterexample) or only the empty or well-formed ones?

### A3. Ariola/Felleisen et al. 1995, via Chang & Felleisen 2012
Primary (Ariola, Felleisen, Maraist, Odersky, Wadler, "A call-by-need lambda calculus", POPL 1995) NOT OBTAINED. Read instead: Stephen Chang and Matthias Felleisen, "The Call-by-need Lambda Calculus, Revisited", ESOP 2012 (arXiv 1201.3907), §1, §4.3, §5, §6.

Mechanism (READ, secondhand for Ariola). Call-by-need "evaluates an argument at most once, and only if needed" (p. 2). Ariola-Felleisen's λ_af "defines the same evaluation function as the call-by-name λ calculus" and Chang-Felleisen §5 shows λ_need equals Launchbury's semantics extensionally (Thm 4, `eval_need = eval_natural`, p. 18). Maraist-Odersky-Wadler's λ_mow is NOT equal: `eval_mow ≠ eval_name`, example `(λx.λy.x) Ω` (p. 4). Equivalence is stated for the evaluation function (does the closed program reach an answer, and which), and soundness is "with respect to observational equivalence" under contexts `C = [] | λx.C | C e | e C` (§4.3, Thm 3, p. 12). Recursion is explicitly out: "does not include an explicit letrec constructor for cyclic terms ... applying their solutions should pose no problems" (p. 19).

Bearing on the question asked ("what equivalence holds, and does it survive effects?"): **AGREE** that call-by-name is the right reference for ground, effect-free observations, with two caveats.
1. The result is extensional: same answers and same divergence, not same cost, not same cell-evaluation order. INFERRED from the statement. Nothing about intensional properties such as "one cell evaluated at most once" transfers to the reference.
2. None of these calculi contains effects; I found no effect or state discussion in the sections read. So the name-need equivalence does NOT demonstrably survive `perform`. The only direct treatment I found is McDermott-Mycroft (B3), which shows it fails.
3. Cyclic sharing (`fix`/letrec) is outside λ_af and λ_need as published; Core4's `fix` needs the Launchbury or Ariola-Blom cyclic setting. Question: which cyclic call-by-need calculus is the reference-vs-machine theorem anchored in?

---

## B. Laziness meets effects

### B1. Peyton Jones 2001
Simon Peyton Jones, "Tackling the Awkward Squad: monadic input/output, concurrency, exceptions, and foreign-language calls in Haskell" (Marktoberdorf lecture notes, 2001). Read §1 (p. 2), §2.6 (p. 12), §3.2-3.3 (pp 16-17).

Mechanism (READ). "laziness and side effects are, from a practical point of view, incompatible" (p. 2): for `xs = [printChar 'a', printChar 'b']`, whether anything prints depends on whether elements are demanded. Haskell's answer is to make I/O actions values of type `IO a`; running them is a separate act. `unsafePerformIO :: IO a -> a` escapes this, and "Whenever you use it, you are promising the compiler that the timing of this I/O operation, relative to all the other I/O operations of the program, does not matter. You must undertake this proof obligation" (§2.6, p. 12). The semantics is stratified in two levels (§3.2, p. 16): an inner denotational semantics for pure terms, an outer labelled transition semantics for IO, and primitive IO operations are *values* ("No further work can be done on this term in the purely-functional world; it is time to hand it over to the outer, monadic semantics", p. 17).

Bearing: **AGREE, and SHARPEN the vocabulary.** `perform plan` yields a Plan to the host is exactly the stratification: pure kernel inside, effect transitions outside. And `unsafePerformIO` is exactly "perform under an update frame": it is the case where running an effect is demanded by forcing a shared thunk, so the effect's timing (and whether it happens at all) becomes an artefact of evaluation order. The `sharedEffect` refusal is the structural answer to the awkward-squad problem, where Haskell leaves it as an unchecked proof obligation. One distinction the paper draws and the design may be blurring: an IO *action* is a shareable value; it is *running* it that is not shareable. The design says "an activity type is never shareable". Question: is a Plan (the description) shareable while the running of an activity is not? See Q2.

### B2. Levy, Call-by-push-value
Paul Blain Levy, "Call-By-Push-Value: Decomposing Call-By-Value And Call-By-Name", Higher-Order and Symbolic Computation 19, 2006. Read §1, §2.2, §3, Figs 2, 3, 8, §7.2.

Mechanism (READ). Two disjoint classes of term and of type: "a value is, whereas a computation does" (§3, p. 8). Value types `A ::= U B | Σ A_i | 1 | A×A`, computation types `B ::= F A | Π B_i | A → B`. "an identifier in CBPV can be bound only to a value, so it must have value type" (p. 8). `thunk M : U B` is a value; `force V : B` runs it; `return V : F A` and `M to x. N` sequence computations. The paper deliberately keeps "the distinction between a term (computation) and its thunk" (p. 8) and shows the monadic metalanguage erasing it is the problem (p. 7). Effects (divergence, `print c. M`, cell store) are computation-level (Fig 3, p. 10). CBN translates `M N` to `(thunk N^n)‘M^n`, a variable to `force x`, and `print c. M` to `print c. M^n` (Fig 8, p. 18); the CBN-to-CBPV relation is a bisimulation (Prop 7, p. 18). Forcing a `U B` thunk of an effectful computation re-runs its effects each time; CBPV has no memoisation (Levy does not treat call-by-need; I grep'd the text and found no mention; INFERRED that memoising is therefore only sound for effect-free `B`).

Bearing: **SHARPEN**, and this is the most useful structural reference for the design.
1. CBPV says exactly why effects force a value/computation split: a shared binding holds *values*; computations (anything that "does") are re-run when forced. A call-by-need cell memoising a computation is only sound if the computation is effect-free, i.e. its result is a value regardless of how many times it runs. "An activity type is never shareable" is the CBPV rule "no memo cell for an `F`-typed computation that performs". INFERRED.
2. CBPV places the line at **types**, not at runtime frames. The design instead refuses at runtime when `perform` is reached under an update frame. The type-based line is the cleaner one: cells may only hold terms whose type contains no effect (value types and pure `U B`), activities live only in sequenced (`to`/bind) positions, and `sharedEffect` becomes unreachable in well-typed programs. The runtime refusal is then defence in depth, not the contract. INFERRED.
3. CBPV permits a `U (F A)` value (a *suspended* activity) that can be stored, passed and forced many times, each re-performing. That is the Haskell reading (B1). The design's blanket "no effect can sit in a field/argument/payload" is stricter than CBPV: it forbids even storing a suspended activity. Decide deliberately whether Plans are values (storable, duplicable, run-many) or a linear resource (run once). If run-many, each forcing is a new perform and the nullifier story must be per-force. INFERRED.

### B3. McDermott & Mycroft, call-by-need effects
Dylan McDermott and Alan Mycroft, "Call-by-need effects via coeffects" (title and authors as in the file; venue not read). Read abstract and §1-2 (p. 2).

Mechanism (READ). "Tracking effects is a harder problem for call-by-need than for call-by-value and call-by-name." With `inc` incrementing a counter: `let x = inc () in let y = inc () in y + x` increments twice, but `let x = inc () in let y = x in y + x` increments once, at the use of `y`. "In call-by-need, using one variable can change the effect of another." Under call-by-name both programs increment twice. The key difficulty is "determining where arguments and let-bound variables are evaluated", which they address with a coeffect system tracking the order of first use.

Bearing: **DISAGREE with the sufficiency of call-by-name as spec once `perform` is present.** With any effect that can occur while forcing a shared cell, call-by-name and call-by-need are observably different programs. The reference semantics (name) would perform at each use, the machine (need) at the first. The design avoids this *only* by refusing `perform` under an update frame. Therefore the equivalence theorem is necessarily conditional on "no perform reached while forcing a shared cell", and the reference semantics must say what it does in that case (see Q1). Note also the first-use order dependency: refusal is raised at the first force, which depends on evaluation order, so whether a program is refused is itself an evaluation-order-sensitive fact unless the reference semantics also has the notion. READ for the example; the application to OB is INFERRED.

---

## C. Guardedness and productivity

### C1. Nakano 2000
Hiroshi Nakano, "A Modality for Recursion", LICS 2000. Read §1 (pp 1-3).

Mechanism (READ). A modality `●A` ("A holds one step later") makes self-reference sound: "as long as `X` occurs only in scopes of the modal operator in `A`, the interpretation of `X` is well-defined and given as a fixed point ... which is actually shown to be unique" (p. 3). Fixed-point combinators (Curry's Y) are typed through `●`. The motivating example is a specification `Nat` of objects with a binary method whose method takes another object of the same type, a self-referential specification where a careless but type-correct definition (`add'`) diverges while `add` does not: "the divergence is caused by a program which is supposed to satisfy the same specification" (p. 1). Types here carry convergence information, as in "specifications ... convergence of programs can be expressed by types" (p. 2).

Bearing: **AGREE**, and this is nearer to the design than the usual stream citation. Open recursion `mix`/`fix` over objects with self-reference is Nakano's own motivating case (self-referential object specifications, binary methods). The typed fixpoint is `fix : (●A → A) → A`; for specs this reads `spec : ●Self → Self ...`. The design's `{good = 7, bad = self.bad}.good` is `7` precisely because `good` does not use `self` in a position that must be evaluated now; Nakano's discipline would *reject* `bad`, while the design's laziness *accepts* it as a field that is ⊥ if forced. These are two different disciplines: total (reject) versus partial and lazy (accept, blackhole on forcing). Question: which does OB want for specs a resident actually ships? INFERRED for the mapping.

### C2. Atkey & McBride 2013
Robert Atkey and Conor McBride, "Productive Coprogramming with Guarded Recursion", ICFP 2013. Read §1 (pp 1-3).

Mechanism (READ). Productivity "means that, even if a program generates an infinite amount of data, each piece will be generated in finite time" (abstract). Guardedness is moved into types via `▷A` ("a value of A that is only available tomorrow", p. 2) with `fix : (▷A → A) → A` (p. 2). `▷` is an applicative functor but not a monad: "a join operation of type `▷(▷A) → ▷A` would allow us to collapse multiple guardedness obligations" (p. 2). Guarded recursion alone cannot observe finite prefixes, so they add clock variables κ, with `fix : ∀κ.(▷κ A → A) → A` and final coalgebras `∀κ.Stream_κ` (p. 3). The model is "an untyped lazy λ-calculus" (p. 1) with multiply step-indexed types, and a syntactic guardedness checker is rejected as non-compositional, with `mergef f` as the higher-order counter-example (p. 2). They also type Bird's circular `replaceMin` (p. 1, §1.3).

Bearing: **SHARPEN**, with two concrete messages.
1. "Each resumed segment terminates" is a **productivity** statement for the resident seen as a stream of turns: each turn (piece of data) delivered in finite time. The across-turn self-call "sits under a perform", which is exactly a constructor guard in the Nakano sense, so cross-turn recursion is productive by construction. What is NOT covered is the within-turn segment, which a guard does not bound; that is a termination problem (see C3, C4).
2. Type-based guardedness is compositional where a syntactic check is not, and `mix lower upper` is a higher-order function in the `mergef` sense: whether `fix (mix a b)` is productive depends on the behaviour of `upper`. So a syntactic "self only under perform/constructor" scan over specs will be rejected by exactly the argument the paper makes. If a check is wanted it should be type-directed (`self : ▷Self`), not a scan. INFERRED.

### C3. Abel & Pientka, sized types and copatterns
Andreas Abel and Brigitte Pientka, "Wellfounded Recursion with Copatterns and Sized Types", J. Functional Programming (the file is the JFP version). Read §1 (p. 3-4) and the bfs example (p. 10).

Mechanism (READ). Infinite data is defined by observations (copatterns) rather than constructors. "In the presence of copatterns, productivity is subsumed under plain termination": `repeat a` "terminates in all contexts since it does not unfold by itself and consumes one projection in each unfolding" (p. 4). Termination is by well-founded induction on size/depth ("depth of a function is the maximal size of arguments it can safely handle", p. 3); this is contrasted with syntactic guardedness that "is difficult to handle higher-order programs such as `g f = cons 0 (f (g f))`" (p. 3). The cyclic breadth-first-numbering program (`bfs`, p. 10) is accepted by an appropriate size assignment. A record "defined by observations" such as `Result = ν^∞{tree; rest}` "is just a lazy product".

Bearing: **AGREE on the fit, SHARPEN on the discipline.** An OB object is a record defined by its fields and observed by projection, with open recursion through `self`. That is the copattern view: a spec unfolds only when a field is projected, so productivity reduces to termination of each projection. This is the cleanest statement of what to prove: every field observation of a well-formed `fix spec` terminates, by induction on a size/fuel index that decreases per projection of a self-reference. It also says the design's fuel-bounded machine is the operational face of a sized-type argument. INFERRED for the mapping; READ for the sized-type mechanism.

### C4. Xia et al., Interaction Trees (added; not on the brief)
Li-yao Xia et al., "Interaction Trees: Representing Recursive and Impure Programs in Coq", POPL 2020 (arXiv 1906.00046). Read §1-2 (pp 4-5).

Mechanism (READ). `itree E R` is coinductive with constructors `Ret r`, `Tau t` (silent step) and `Vis e k` (a visible event `e` whose answer type feeds the continuation `k : A → itree E R`). They support divergence without fuel: `spin := Tau spin`; they note guardedness is "inherently non-compositional" (p. 5) and use `Tau` so that "silently diverging computations" are expressible. Equivalence is weak bisimulation (`eutt`) which ignores finitely many `Tau`s.

Bearing: **SHARPEN.** `perform plan` resumed with a response is literally `Vis plan k`. A turn is a (finite) `Tau*` prefix ending in `Vis` or `Ret`. The natural equivalence for "the stored checkpoint ends every segment as the machine's continuation would" is `eutt` on the interaction trace, not equality of machine state. This also makes the divergence case crisp: a turn that diverges inside is an infinite `Tau` chain, which a host cannot distinguish from "still running" without a fuel bound. Question: is out-of-fuel a `faulted` outcome (consensus-visible, so the bound must be a protocol constant)? See Q3.

---

## D. Reflection and equivalence

### D1. Wand 1998
Mitchell Wand, "The Theory of Fexprs is Trivial", Lisp and Symbolic Computation 10, 1998, pp 189-199. Read all.

Mechanism (READ). A pure λ-calculus extended with `fexpr` (which "rei[fies] its unevaluated actual parameter as a λ-term in normal form using the Mogensen-Scott coding") and `eval`. Result: "two terms are contextually equivalent iff they are α-congruent" (Cor 1, p. 195). The proof builds, for any term `M`, a context `Eq_{M,σ}` that returns `T` on the coding of `M` and `F` on any non-congruent `N` (Lemma 6-7). Section 4 notes that with a first-order coding of variables "two terms are contextually equivalent iff they are identical, not just α-congruent" (p. 196). Section 5 (Cor 2, p. 196-197): any weakly adequate compositional denotational semantics "must (up to isomorphism) map each term to itself, so no useful abstraction is possible".

Bearing: **SHARPEN, the key theoretical warning for `SpecMeta`.** What triggers triviality is that the observer receives an *injective, decidable coding of the term itself*. Whether our metadata does that is the crux.
- `declared{name, interface, laws}`: a quotient, since two specs with equal declared fields are indistinguishable by a metadata observer. Not Wand-trivial at the leaves.
- `composed{inherited, wrapping}` records the construction history; if `inherited` and `wrapping` hold the sub-specs' metadata recursively, `metadata(compose(a, b))` is injective on construction trees (over declared leaves). Then equivalence under a metadata observer is exactly equality of construction trees, i.e. Wand's trivial theory over the composition fragment. So "compose is associative for behaviour but not under the metadata observer" is not an incidental asymmetry; it is the expected, unavoidable shape. INFERRED, but the mechanism is Wand's Lemma 6.
- Escape routes: (a) metadata coarser than construction (an `Eq` context cannot be built if the coding is non-injective), e.g. record only a flattened set of declared names, which would restore associativity; (b) accept the trivial theory for that observer and say so. Both are legitimate; accidentally having the injective one is the risk. Question: is `composed` meant to be injective on trees or a quotient?
- Cor 2 also warns: a *compositional* semantic model that is adequate for a language containing a metadata observer cannot equate anything the observer separates. So the Core4 reference semantics (behavioural) and the reflective layer must be separate languages with separate equivalences, which is what "list the observers" does.

### D2. Felleisen 1991
Matthias Felleisen, "On the Expressive Power of Programming Languages", Science of Computer Programming 17, 1991. Read §1, Thm 3.8 (p. 14), Thm 3.14 (p. 18).

Mechanism (READ). A language `L1 = L0 + {F1, ...}` is a conservative extension of `L0` if theorems restricted to `L0` are unchanged. Thm 3.14 (i): "If the operational equivalence relation of `L1` restricted to `L0` expressions is not equal to the operational equivalence relation of `L0`, i.e. `=0 ≠ (=1 | L0)`, then `L0` cannot macro-express the facilities `F1,...`". Slogan in the text: "new programming constructs add to the expressive power of a language if their addition affects existing operational equivalences" (p. 18). Equivalence is always relative to a language of contexts.

Bearing: **AGREE, and it supplies the exact statement.** Adding a `metadata` observer is a non-conservative extension: `compose(compose(a,b),c) =_0 compose(a,compose(b,c))` holds among Core4 contexts but fails among Core4+metadata contexts (Thm 3.14(i)), so metadata *strictly increases expressive power*. That is the correct framing and it matches "list the observers, state each equivalence against its observers": the literature's standard method is the same, indexed by the language of contexts. Risk: the design should also state which equivalences remain under the metadata observer (e.g. `declared` leaves) and treat the failure of associativity as a theorem (Thm 3.14 witness) rather than a caveat. INFERRED for the application.

### D3. Smith 1984 and Kiczales et al. 1991
Brian Cantwell Smith, "Reflection and Semantics in Lisp", POPL 1984 (author reprint). Read abstract, RL·8, RL·38, RL·48. Gregor Kiczales, Jim des Rivières, Daniel Bobrow, *The Art of the Metaobject Protocol*, MIT Press 1991. Read only the front matter and Part I roadmap (p. 8-9).

Mechanism (READ). Smith requires the embedded theory to be "causally connected, so that the reflective accounts of objects, events and states of affairs are directly tied to those self-same objects ... This causal relationship must run both directions: from event to description, and from description back to event" (RL·8). 3-Lisp reflective procedures "are: (i) run not at the level at which the invocation occurred, but one level higher ... and (ii) given as arguments those structures being passed around in the reflective processor" (RL·38); it reifies the environment and the continuation and absorbs the rest (RL·48). AMOP divides protocols into "introspective protocols, which make it possible to analyze the structure and definition of a program" (Part I, Ch 2) and "intercessory protocols" that "step in or intercede in the behavior of the system" (Ch 3) (pp 8-9).

Bearing: **SHARPEN.**
1. Direction of causal connection is the design question. `SpecMeta` as a *record of construction history* is event-to-description only (introspection). Smith's test of real reflection is the other direction too. If metadata can ever flow back into behaviour (a spec that dispatches on `metadata(self)`), that is intercession and compose is not associative *for behaviour either*. The design needs a non-interference theorem: behaviour of a spec is independent of its metadata (metadata may not be read by `mix`/`fix`/`perform`, only by designated observers). INFERRED.
2. The open question R(Y M) vs Y(R∘M) is the introspection-vs-intercession question in fixed-point clothes. R inside the knot (Y(R∘M)) means every self-call goes through the reflective wrapper, which is intercession at every internal call site (the AMOP/3-Lisp "one level up" reading). R wrapping the finished target (R(Y M)) sees only the outside, introspective. If the prototype's metadata is observed only from outside, R(Y M) is the introspective choice; if the wrapper must be able to affect internal self-calls, only Y(R∘M) works. INFERRED.
3. Smith reifies the **continuation**; our checkpoint is a reified continuation (heap, control, stack). Smith's "causal connection in both directions" is the right informal statement of `ForcingTransparent`: the description (checkpoint) must reconstitute the very event (continued run), not merely resemble it. INFERRED.

---

## E. Serializable continuations and checkpoint transparency

### E1. Khan 2026, "Resume Means Resume"
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

### E2. Burckhardt et al. 2021, Durable Functions
Sebastian Burckhardt, Chris Gillum, David Justo, Konstantinos Kallas, Connor McMahon, Christopher S. Meiklejohn, "Durable Functions: Semantics for Stateful Serverless", Proc. ACM Program. Lang. 5, OOPSLA, Article 133, Oct 2021. Read §3.5, §5, §6, Lemmas 6.5-6.7, Thm 5.3, Thm 6.4.

Mechanism (READ). The compute-storage model is shown a weak simulation of the high-level model (Thm 5.3). The replay-based model stores orchestration state as a history of events and rehydrates by replay because "the state of the orchestration ... is not serializable by default" in mainstream languages (§6 intro). It is proved bisimilar to persisting intermediate states (Thm 6.4, §6.3), resting on Lemma 6.5 (Deterministic Replay: `h ⊲↠ x` and `h ⊲↠ x'` imply `x = x'`), Lemma 6.6 (Record/Replay) and Lemma 6.7 (Transparency of Recording). "Note that Lemma 6.5 relies on the determinism of the execution, which in this model is easy to prove for our simple lambda calculus. In a mainstream programming language, nondeterminism is not implicitly guaranteed" (§6.3). The guidelines (§3.5): "the orchestration code must be deterministically replayable. Any code that reads non-deterministic data sources or calls I/O should not be done directly in the orchestration, but must be wrapped in an activity".

Bearing: **AGREE on the proof shape, DISAGREE on the mechanism, SHARPEN on the premise.**
1. Their transparency theorem has the same shape as `ForcingTransparent` (persisted representation vs in-memory continuation), proved as a **bisimulation** whose load-bearing lemma is determinism of the step function (Lemma 6.5). So `ForcingTransparent` should be stated as a bisimulation (or at least simulation) on the interaction trace, and its premise list must include determinism of the machine's segment step, with no hidden inputs (heap addresses, fuel, clock, GC timing). INFERRED.
2. They *replay* a history because the host-language state is not serializable; OB serializes the machine state directly. That is the stronger and rarer design (E4 cites Termite/Pettyjohn for the serialization side), and it removes DF's determinism-of-user-code requirement, replacing it with determinism of *the machine*, which the Lean model can discharge. This is a real advantage and the design should state it.
3. DF reads state through activities/entity calls recorded in the history, so after replay the orchestration sees the *recorded* value, never a fresh one. OB's resume-with-view is the opposite choice: fresh view at resume. DF therefore cannot serve as a precedent for the resume-with-view guarantee; Khan's PC cannot either (E1).

### E3. Termite Scheme (Germain, Feeley, Monnier 2006) and Pettyjohn et al. 2005
Guillaume Germain, Marc Feeley, Stefan Monnier, "Concurrency Oriented Programming in Termite Scheme", Scheme and Functional Programming 2006 (read §3.1-3.2, §4.9, §5). Greg Pettyjohn, John Clements, Joe Marshall, Shriram Krishnamurthi, Matthias Felleisen, "Continuations from Generalized Stack Inspection", ICFP 2005 (read abstract, §3.5, §4 labelling).

Mechanism (READ). Termite serializes "every first class value in the language, including closures and continuations", with limits: "It will not be possible to serialize a closure or a continuation if it has a direct reference to one of these objects in their environment" (ports, devices) (§3.1, p. 2); non-serializable resources are replaced by process proxies so serialization is "just a pid". Mutation is removed: "To keep the semantics clean and simplify the implementation, mutation of variables and data structures is not available" (§3.2, p. 2). The format preserves sharing and cycles (SRFI 38 notation with a hash table to detect shared data) (§5), and deserialization requires "the same compiled code" (p. 8). Pettyjohn et al. give a translation that eliminates continuation capture via stack inspection, with a correctness theorem as a simulation (Thm 1, §3.5: `CMT⟦eval_SL(p)⟧ = eval_TL(CMT⟦p⟧)`, via a simulation Lemma 2: each source step corresponds to at least one target step). Serialized continuations carry defunctionalised-closure labels derived from "a message digest based on the syntactic structure of the program"; if the program changes non-trivially "the computed message digest changes ... Values published with the old key become obsolete and the server can fail gracefully" (p. 7).

Bearing: **AGREE, with three concrete requirements on the premise.**
1. A non-serializable thing in the environment makes the closure non-serializable: Termite's rule is the effect-in-the-cell rule from the opposite end. "No effect can sit in a field/argument/payload" is what makes the checkpoint serializable at all. INFERRED.
2. Code identity belongs in the checkpoint digest (Pettyjohn, Termite): a resume under a different program or machine version must refuse, not reinterpret. The design already binds the digest; the transparency premise should name the code/machine digest as part of "the checkpoint".
3. Neither source proves that a serialize/deserialize round trip is transparent. Pettyjohn proves the capture/reinstate *translation*; the serializer is engineering. Termite has no theorem. So `ForcingTransparent` as an open premise is where the literature is also silent. Nothing I found proves a heap-serializing round trip transparent for a lazy machine with sharing; the closest are Burckhardt's bisimulation (replay not serialization) and Pettyjohn's simulation (stack, not heap). INFERRED from absence in the papers read; Kali Scheme (Cejtin et al. 1995) was not obtained and might contain more.

### E4. Ahman & Pretnar 2021 (in paperbin; abstract only)
"Asynchronous Effects", POPL 2021. Read abstract: it decouples "the execution of operation calls into signalling that an operation's implementation needs to be executed, and interrupting a running computation with the operation's result". **AGREE** as framing: `perform plan` followed by resume with a response is signal-then-interrupt. I did not read the semantics, so no further claim.

---

## F. Synthesis: how the literature lines up with the design

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

## Sharpest questions

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
