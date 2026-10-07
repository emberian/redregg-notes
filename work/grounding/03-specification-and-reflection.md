# 03 — `Specification<T>` and the reflection contract

Code: minidregg main `4ef4e808`, read only. Design record: `docs/objective-bend/REFLECTION.md`.
Literature: LIT-W1 §7 (Pierce–Turner, existentials), LIT-W2 §D (reflection and equivalence).

## 1. Current design

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

## 2. What it commits us to

1. **Every observer is a reason a rewrite is unsound.** With `metadata` observable, the compiler and any
   optimizer can only use `≈b` laws where no `metadata` observer reaches the rewritten spec. That is a
   whole-program side condition.
2. **Metadata is part of the package's meaning**, so the *front end* fixes what metadata a program can
   see (names, interface strings). Any change in how the front end renders an interface label is a change
   in program meaning (D4 showed one by accident) and a re-genesis.
3. **Provenance is not authenticated**: anyone can pair any spec with any target.
4. **Laws are listed but never discharged** (status always `unchecked`), so reflection can observe a
   promise nobody keeps — in tension with the stated rationale for excluding closures.

## 3. Literature (LIT-W2 §D; LIT-W1 §1, §7; quotes and pages there)

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

## 4. Questions for GPT-6

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
