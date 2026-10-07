# 02 — Modular typing: templates, rigid Self, F-bounds, `requires`, `fix` discharge

Code: minidregg main `4ef4e808`, read only. Design record: `docs/objective-bend/MODULAR-TYPING.md`
(D1–D6). Classic literature: `lit/LIT-W1-oo-calculus-typing.md`. Book: LTUO §8 (Rideau, *Lambda: The
Ultimate Object*, mirror `ltuo-readable.txt`).

## 1. Current design

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

## 2. Faré's target, for contrast (LTUO §8.4.1.3, read at `ltuo-readable.txt:4143-4171`)

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

## 3. What it commits us to

1. **No subtyping, ever, in the core**, so width is handled by lower bounds at instantiation only.
2. **Open specs are second-class.** A library cannot export a higher-order combinator over open extensions
   ("given any extension over `Self has {x}`, return one over `Self has {x, y}`") — only over closed ones.
3. **Typing is whole-program at `fix`**: the front end must see every layer's concrete types to type a chain.
   That is compatible with publish-time replay (topic 07) but not with separate compilation of open
   components across packages (LT5).
4. **Theorem cost stays flat**: the machine proofs never see a type variable.

## 4. Literature (LIT-W1 §3–§10; quotes and pages there)

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

## 5. Questions for GPT-6

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
