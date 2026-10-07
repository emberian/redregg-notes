# 01 — Open recursion with lazy cells, C4 ancestry, method combination, Core4 primitives

Code: minidregg main `4ef4e808`, read only; the method-combination fixes D1–D5 are on `lane/ob-review`,
not main (`work/OB-FAREOO-REVIEW-20261005.md`). Book: Rideau, *Lambda: The Ultimate Object — Object
Orientation Elucidated* (draft, 2026; mirror `~/dev/fareoo/raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt`),
cited "LTUO §n". Classic OO literature: `lit/LIT-W1-oo-calculus-typing.md`; laziness:
`lit/LIT-W2-laziness-reflection-continuations.md` §A–B.

## 1. Current design

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

## 2. What it commits us to

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

## 3. Literature (LIT-W1 §1–2, §10–11; LIT-W2 §A; quotes and pages there)

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

## 4. Open item handed over by DEPUTY-OB-ENG: a `digest` primitive (Core4 semantics change, held for this round)

`Theory/ObjectiveBendDigest.lean` (W30, d8f7ca48) defines `digest a b` = cSHAKE256 under
`DREGG.OBEND.DIGEST/v1` over `len(a):8 ‖ a ‖ b` (preimage `:123`, `Admissible` `:127`), with
`binds_or_collides` proved and hiding **assumed**; the C export `minidregg_obend_digest` exists, but
`Primitive.digest` (W30 3c541dd5) is **not on main**. Adding it adds a Core4 constructor, a typing rule, a
machine step and a meter row. cv 01a1088f-47a0 proposes a size-aware meter (≤ 3 Keccak-f per step at
`scalarBits` 512) against "one tick, like multiply". Motivating use: ballot hiding, commitment =
digest(vote, salt) (OB3 in `work/OB-COMPLETION-20261005.md`). Questions: one-tick vs size-aware pricing;
Nat-in/Nat-out vs a bytes type; and whether a hash belongs in the language at all versus a kernel-supplied
value or a `Pred.hashEq` law clause (which already exists, `Pred/Core.lean:190-194`).

## 5. Questions for GPT-6

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
