# DESIGN-TYPES — the type system nano's surface should have: graded effects, linearity where it lives, refinements the checker decides, and a World as a member (FABLE-TYPES, real 2026-10-26)

Axes 7 and 6 of FRONTIER-AXES-20261026.md. Written under ONE HISTORY ∧ INTEGRITY (TOPLEVEL-SPEC §3, §13): nothing
here weakens a check, and every new refusal is by name. Claims about the code are tagged MEASURED (I ran or read it at
ad90a47) or INFERRED. Design claims are mine.

## 0. The answer in one page

**What the surface has, in the field's terms.** nano's method type is already a one-shot effect row. A method's type
`fn R (fn S (fn A (fn reqTy {calls, edits, state})))` declares what it READS (`R`: the relations, points, ranges, live
and receipt columns), the KINDS of call it may make (each slot a sub-sum of the five call arms, `callOf kinds`,
`callSlotOk`; MEASURED `Lang/Package.lean:139-145, 280-284`), and how many EDITS it returns. The kernel enforces the
read half (pins; `receive_congr`), the checker enforces the kinds (a body that returns a `transfer` in a slot typed
without one does not check), and the kernel asserts the rest where calls enter (`notCallable`, `tooManyCalls`,
`rowParent`, `duplicateEffect`: law 4). This is Lucassen–Gifford's effect typing (POPL 1988) with Koka's row shape
(Leijen, MSFP 2014: a row of effect labels on the arrow), realised the way Interaction Trees realise effects (Xia et
al., POPL 2020): effects are DATA the host interprets, one round per Turn, so the "handler" is `Kernel.Receive.dispatch`.
Move's `acquires` annotations (Blackshear et al., 2019) are the ledger-language analogue, and nano's are stronger: Move
declares the resources a function touches; nano declares AND the kernel pins them AND disjoint footprints commute as a
theorem (LT7/LS10).

**What it lacks is the GRADE.** The row says WHICH effects; nothing says HOW MUCH. A method typed `(calls (transfer))`
may move the object's whole balance in one run, and MEASURED (`Kernel/Receive/Call.lean:337`, `Lang/Program.lean:326-339`)
no law can see it: `judge` reads `old new : Slots` and `Req`, never the calls. The only bounds on what a method moves are
the kernel's (`belowFloor`; a grant's `transfer cap` when the method spends through `via`). A method moving the object's
OWN accounts (actor = obj, no via; `Derive.lean:215-233`) is bounded by the balance alone. The escrow's "every retract
pays its leg" is a run-sound THEOREM about one generator (LANG-75.18's P8d/P8e plants), not a check any package gets.
That is the hole with teeth, and it is the one a graded effect system (Katsumata, POPL 2014: parametric effect monads;
Orchard–Petricek–Mycroft, ICFP 2014; Gaboardi et al., ICFP 2016) closes: the arrow carries a quantity, and the checker
compares quantities.

**The design (§2).** Keep the row in the type; put the grade beside it, indexed by the method label, because `Ty` is
monomorphic first-order data with no indices and must stay so (LANG-3; the codec, the checker and ~2,000 theorems are
over it). A package carries `effects : List (Label × Effect)`; `Effect` is a record of grades, first `moves : Nat`: the
most the method's one run may transfer or credit, summed over the calls it returns. Install refuses by name
`effectExceeded ℓ` a method whose TYPE names a value-moving arm (`transfer`, `credit`) under a grade of 0 (the default:
a method that declares nothing moves nothing). Run refuses by name `effectExceeded` a run whose returned calls move
more than the grade. Both decide in O(size of the type) and O(number of calls), under the ticks the run already pays.
The theorem: a returned run moves at most its grade. Next grades, in order of what they buy: `writes` (the relations an
edit slot may name, as a sub-sum of `editTy`, the pattern `callOf` already uses: install-only, no run check needed past
typing), `grants` (the rights a method may delegate), `moves` per asset by digest literal, `invokes` by package id.

**Linear value in the type (§3): a category error, and what the reader actually is.** Move needs linear types because
a Move program HOLDS a resource in a local. A nano method never holds value: no term has a value type; `transfer` is
data the method returns and the kernel is the only mover. There is nothing for a linear type to type. PROT-8 declined
the `Cap`/`Val` split "for lack of a reader"; the reader is here, and it is not a type: it is (i) `admit_value`, the
kernel's one count; (ii) the `moves` grade, an AFFINE bound on what a run may ask the kernel to move; and (iii) the
one coupling nano's data model does hold linearly, a ROW THAT HOLDS A LEG: a relation declared `(holds give)` whose
rows are born exactly when the leg moves in and retracted exactly when it moves out. That coupling is checkable at run
by name (`legStranded`), O(edits × calls), and it is the P8d/P8e tooth as a refusal every package gets rather than a
theorem one generator has. It sits BESIDE `admit_value` (law 1: one count; this is a coupling, not a count) and does
not subsume it.

**Refinements (§4): three tiers, and the boundary with PCC.** A refinement is checked at one of three places, and the
place is the design: at INSTALL when its witness is in the text (a literal amount under a grade, an arity, an enum arm,
a digest literal against the World: LANG-38 is already an install-time refinement check); at RUN by name when its
witness is a value (`Bound`s on arguments, `"text 1..200"`: already a run-checked refinement system, `Surface.lean:633-650`;
`effectExceeded`; the escrow's `unfairLegs`); and by a PROOF a member supplies when it quantifies over every run (FABLE-PCC).
The checker DECIDES tiers one and two in bounded ticks; it VERIFIES tier three against a supplied witness. A law that
IS a type is tier two already (a law is a refinement on `(old, new)` judged at every step); tier three is what lets a
member CLAIM the law holds of every method so a reader can rely on it without re-running — and the law still runs
(law 2; "No proof system in Mini admission": a proof is a second channel, never a skipped judge).

**A World as a member (§6).** To another World, a World IS its head object plus a key: `Std.headStateTy =
{head : sum {at {height, roots, steps}, forked {held, other, steps}}, world : digest}` (MEASURED `Lang/StdHead.lean`),
posted by the member that follows it, judged by `headLaw` (steps never fall; equal steps keep the head; height never
falls; a fork freezes), and consumed through the `(receipt)` column every method may declare. So the TYPE of a World as
a term is `headStateTy`, a root law typed over a member World's head is exactly `lawTy headStateTy` (`headLaw` is one),
and federation is recursion for free: a relation `members : {world : digest} → headTy` in a root object, one row per
member World, keyed by the member's head object (cell-keyed, so `(live)` and `(receipt)` reads work), its guard
`headLaw` per row — "the receiver is the monitor" one level up. The root's own head posted into a grand-root is the
same object again. What a World-as-member CANNOT be: an object the root invokes (charter: no cross-World call; a
member World's state moves only by its own writer's posts). What is missing, and whose it is: a `certified` column
(TRUST's T3 authority on the posted head) so the root's law can require a head the member World's writer signed, not
one a follower posted; and `Req.caller` so a root law can know WHICH member World's object called it (the LANG
reader's fourth embarrassment; a week).

**The one way this is wrong.** A type system the metered machine cannot check in bounded ticks at install or at run is
a docstring. Every check here is a fold over a finite list the package already carries, under bounds the wire already
enforces (`callsMax`, `editsMax`, `rowMax`); the design refuses, by construction, any grade whose check would need to
run the method (that is PCC's tier). If a future grade needs the body's VALUES at install, it is not a grade; it is
either a run check by name or a proof.

## 1. The surface's type system today, measured

| the type says | enforced where | by | refusal |
|---|---|---|---|
| reads: relations, points, ranges, `(live)`, `(receipt)` (`R`) | kernel + runtime | pins, `RowView`, `readsData`; `receive_congr` | `unpinned`, `rowUnpinned`, `rangeUnpinned`, `liveNotCellKeyed`, `receiptRead`, `headDead` |
| call kinds per slot (`callOf kinds`, `invokeOf A`) | install (typing) + kernel assertion | `callSlotOk`; `checkE`; `notCallable` | `badMethod`, `illTyped`; `notCallable` (unreachable past typing, `callsOf_callable`) |
| the invoke argument type `A` (LANG-77) | install + callee's run | `invokeArgOk`; the callee decodes at ITS `A'` | `badMethod`; `program "arguments: …"` |
| edit COUNT (`editsTy rels m`) | install | `editSlotsOf`: every slot at the whole `editTy rels` | `badMethod` |
| the state type `S`, the argument `A` | install + run | `isRecordData`, `isData`; decode at the type | `stateNotData`, `program "state …"` |
| digest literals | install + every load | `checkLits` against `digestOf` (LANG-38) | `notDigest` |
| argument bounds `(bytes 1 2000)`, `nat lo..hi` | run, by name | `boundCheck` (`Surface.lean:633-650`) | `"text 1..200"` |
| amount moved, target invoked, right granted, relation edited | NOTHING | — | — |

The last row is the design's object. Two more measurements shape it:

- **Laws are blind to calls.** `Program.judge : Pinned D → Option D → List D → Slots → Slots → Req D → …`
  (`Kernel/Receive/Call.lean:337`). A law judges `old → new` state. The calls a run returned are derived AFTER the judge
  (`Derive.lean:230-233`: `judge`, then `deriveCalls`). So "a law can require a caller's effect be within a bound" cannot
  be a law over state; it must be either a grade the install check compares (this design) or a `Req` field (`caller`)
  the callee's law reads (priced in §7).
- **The row already has sub-sum discipline.** `callOf kinds` filters the five arms; `callSlotOk` requires each arm at
  exactly its canonical type. Generalising the same discipline to edit slots (`editTy` over a subset of the relations)
  is a one-function change in the one place that reads edit slots (`editSlotsOf`), and `editsOf` (Rel.lean) needs no
  change: it reads the relation by label, and a label of a sub-sum is a label of the sum.

## 2. Graded effects: the design

### 2.1 Shape

```lean
/-- A method's GRADES (LANG-89): the quantities its row of effects is bounded by. The row (which kinds, which
relations, which reads) is in the method's TYPE; the grade sits beside it because `Ty` carries no quantities. -/
structure Effect where
  /-- the most one run may move: the sum of `amount` over the `transfer` and `credit` calls it returns -/
  moves : Nat := 0
  deriving DecidableEq, Repr

structure Package where
  … (as today)
  /-- each method's grades, labels ascending; a method absent here has the zero grade (moves nothing) -/
  effects : List (Label × Effect) := []
```

Wire: one more child of the package node, `node 4 [effect*]`, each `node 0 ℓ [node 0 u64 moves]`; the version byte
5 → 6 (`lang/package/6`, `lang/package-version/6`): a version-5 package refuses before its tree is read, never
reinterpreted (the LANG-60 rule). Surface: `(method ℓ … (effect (moves N)) body)`.

### 2.2 What install decides (syntactic: the type against the grade)

`checkEffects`: `effects` ascending, every label a method (`noMethod ℓ` else), at most one per method; then for every
method, `movesKinds(type) ⊆ (if grade.moves = 0 then ∅ else {transfer, credit})`: a method whose any call slot names
`transfer` or `credit` under a grade of 0 is refused **`effectExceeded ℓ`**. This is "the body syntactically exceeds the
declared effect": the body checks at its type, and the type names the arm. A grade with no such arm is allowed (a
declared capacity left unused, as a slot left `none` is).

The default is the SAFE one. A package that declares nothing has every method at `moves = 0`, so every value-moving
method in the tree declares its grade or does not install. Today that is three packages (MEASURED §0 of the report):
`world/escrow/Escrow.ob`, `Std.offerEscrowPackage`, the journey's P8 commit package. They re-emit with a grade; the
rest of the tree's packages are byte-identical but for the version byte and the empty node.

### 2.3 What run refuses (dynamic: the returned calls against the grade)

After `callsOf` reads the returned calls as `Body`s and before any is derived:
`movesOf calls := Σ amount over .transfer … amount … and .credit … amount …`; `movesOf calls ≤ grade.moves` or the run
is refused **`program "effectExceeded"`** (the first token is the name: law 7's `program` convention). O(callsMax).
The whole tree then fails, as any run refusal fails it.

Where: `Lang.runMeasuredWith`, the one run path (`runMeasured`, `runMeasuredLive`, `runMethod` are its instances), so a
measured number is the deployed run's and THE BAR's denominator is unchanged.

### 2.4 The theorem (the statement, not a docstring)

```lean
/-- A returned run moves at most the method's grade: the calls `runMeasuredWith … = .ok (_, calls, _)` returns
satisfy `movesOf calls ≤ (p.effectOf ℓ).moves` for the resolved method `ℓ` of `p`. -/
theorem runMeasuredWith_moves_le …
```
Its plant: delete the `checkMoves` line; EF3 (below) reds and the theorem reds. Its floor: a `Lang.program` whose
`checkMoves` is `.ok ()` is refuted by EF3 (the run moves 20 under a grade of 10 and is admitted).

### 2.5 The rows (`Lang/Journey/Effect.lean`, §EF)

A Treasury package: state `{asset, payee}`; method `pay {amount}` typed `(calls (transfer))` with `(effect (moves 10))`,
moving `amount` from the object's own account to the payee. A `drain` package: the same method under no grade.
- EF0 setup: install Treasury; a well; the object's account funded with 50.
- EF1 within the grade: `pay {amount 10}` admitted; the object 50 → 40.
- EF2 the body exceeds the grade: install `drain` (a `transfer` slot, no effect) refused by name `effectExceeded pay`.
- EF3 the run exceeds the grade: `pay {amount 20}` refused by name `program effectExceeded`; the object still 40.
- EF4 two calls: a `pay2` with two transfer slots and `moves 10`, run with 6 + 6, refused (the grade is the SUM).

### 2.6 The next grades, each one function and one name

- **`writes : List Label`** — which relations the method's edit slots may name: `editSlotsOf` accepts an edit slot at
  `optTy (editTy (rels.filter (· ∈ writes)))` (the sub-sum), refusing `effectExceeded ℓ` at install when a slot names
  a relation outside. No run check: typing closes it, as it closes call kinds. Buys: a layer (`mix`) can inherit a
  package whose log relation only `ring` may write, and a hand-written method of the layer cannot touch it. (The
  LB13 rows show guards hold across layers; `writes` makes the restriction visible in the type, and makes
  `activity_monitor_safe`'s premise on the guard a premise on the TYPE.)
- **`grants : List Label`** — the right kinds a `grant` call may carry (a method may delegate `observe` and not
  `transfer`): `rightsTy` becomes a sub-row, install-only.
- **`moves` per asset** — `List (ByteArray × Nat)` by digest literal (checked against the World at install like any
  literal, LANG-38), run-checked per denomination. Buys an escrow whose grade is "5 α and 7 β", not "12 units of
  anything".
- **`invokes : List ByteArray`** — the package ids the method's `invoke` calls may target: the kernel reads the
  callee's package slot at dispatch (`packageOf`, `Derive.lean:186`), so the check is one slot read per call. Buys:
  a package whose nested calls are confined to packages it names, the ocap "no ambient authority" discipline on calls.

## 3. Linear value: why not in the type, and what the reader is

**The category error.** Linear logic (Girard 1987) and its type systems (Wadler 1990; Rust's affine ownership; QTT,
Atkey 2018; Nomos, Das–Balzer–Hoffmann–Pfenning–Santurkar 2021) control DUPLICATION AND DROPPING OF A TERM. Move
needs them because a Move function holds a `Coin` in a local variable and could copy or forget it. A nano method holds
no value, ever: `Ty` has no value type, a `transfer` is a datum the run returns, and `World.admit` is the only thing
that moves a balance (`admit_value`, of EVERY admitted Turn, forged logs included: `Kernel/Proofs/Value.lean` header).
A `Val` type in the surface would type a term that does not exist. PROT-8 (LANG-75.18) declined it as "a second
count of value with no reader", which is right, and the reason is deeper than "no reader": there is nothing to count.

**What the reader is.** The three things linearity buys in Move, and where nano already has or now gets each:

| Move's linear type guarantees | nano's reader |
|---|---|
| a resource is never duplicated or created from nothing | `admit_value` (a kernel equality; the one count, law 1) |
| a function cannot move more than it was handed | the `moves` grade (§2): an affine bound per run, by name |
| a resource is never DROPPED (left in a dead local) | nothing today for packages; the escrow has `escrow_take_run_sound` etc. as theorems, one generator — this is the gap |

**The third row is the real linear discipline nano's data model holds: a ROW HOLDS A LEG.** An escrow offer's row is
born when its leg moves in (`post`) and retracted when it moves out (`take`/`fuse`/`withdraw`); P8d/P8e/P8f planted
exactly the drops (a retract that pays nothing strands the leg). The design: a relation may declare `holds : Option
Label`, the field of its value that is a leg `{amount, asset}`. The runtime then checks, per edit of such a relation,
in the same run: an `insert`'s leg has a matching `transfer` INTO one of the object's accounts of that asset for at
least that amount among the returned calls; a `retract`'s old row's leg has a matching `transfer` OUT for at least it.
Refusal by name **`legStranded`** (a retract with no outgoing leg) / **`legUnfunded`** (an insert with no incoming
one). O(edits × calls). This is `activity_monitor_safe`'s shape ("the receiver is the monitor") applied to value:
the invariant lives with the RELATION, and every method of the package, generated or hand-written, keeps it. The
theorem: a `holds` relation's rows are each backed by a leg the object received and not yet released (an inductive
invariant over the object's history, provable from the per-run check plus `admit_value`'s conservation).

Does it subsume `admit_value`? No, and it must not: `holds` is a coupling between a row and a call the run RETURNED;
whether the call moved what it said is the kernel's (`transfer` may be refused `belowFloor` and then the tree fails
whole, so the coupling holds trivially of admitted Turns). One count (law 1), one coupling. It sits beside.

Price: `RelDecl` gains a field (wire: one more child of `relTree`; the same flag day as §2), `checkRel` checks the
field names a `{amount, asset}` record in the value, `guardEdits`'s neighbour gets a `checkLegs`. The escrow declares
`holds := some "give"`; P8d/P8e become refusals EF-side instead of theorem reds. The run-sound theorems of the escrow
stay (they say more: WHICH account). `escrow_fuse_admitted`'s "both legs moved" becomes a corollary of the check plus
the row acts, for every package, not one. This is the second landing of this axis (§9).

## 4. Refinement and dependent types: the decidable fragment, and the boundary with PCC

**What nano already has, named.** `Bound` (`Surface.lean:617-650`): `(bytes 1 2000)`, `nat lo..hi` on argument fields,
compiled to a `boundCheck` prefix of the method body that refuses by the bound's NAME. That is a refinement type
`{x : bytes | 1 ≤ |x| ≤ 2000}` whose check is deferred to run. Liquid types (Rondon–Kawaguchi–Jhala, PLDI 2008)
discharge the same predicates statically with an SMT solver; nano has no solver and must not (bounded ticks, one
machine). `checkLits` is a refinement `{d : digest | d ∈ World}` decided at install. `callSlotOk`/`invokeArgOk` are
refinements on TYPES decided at install. So the surface already has refinements in two tiers; the design names the
tiers and says which refinement goes where.

**The trichotomy.**

| tier | the witness is | decided by | examples | refusal |
|---|---|---|---|---|
| INSTALL | in the text (a literal, an arity, a label, a type) | `checkWith`: a fold over the package, no evaluation | grades vs arms (§2.2); `writes`; digest literals; `callSlotOk`; a `transfer` whose `amount` is a LITERAL ≤ the grade | `effectExceeded ℓ`, `notDigest`, `badMethod` |
| RUN | a value the run computed | the runtime, after extraction, O(result) | `moves` vs the returned calls; `Bound`s; `holds` legs; `unfairLegs` | by name, `program "…"` |
| PROOF | a derivation over all runs | PCC's checker, against a member-supplied witness | "every run of `pay` keeps `balance ≥ reserve`"; "the law preserves the invariant" | PCC's names |

**The rule that places a refinement:** if deciding it needs the method's VALUES it is RUN; if it needs ALL runs it is
PROOF; otherwise INSTALL. The smallest install-decidable fragment that is new and worth having: (i) grades against
arms (§2.2); (ii) `writes`/`grants` sub-rows; (iii) LITERAL-witnessed grades: a `transfer` arm whose `amount` is a
`.nat k` literal in the body with `k ≤ moves` needs no run check — the checker can mark the slot "statically within
grade" and skip the run sum. (iii) is an optimisation, not a guarantee; I would not build it until a measured run
shows the sum costs anything (it is ≤ 8 additions).

**A law that IS a type.** A law `lawTy S = fn S (fn S (fn reqTy verdictTy))` is a refinement on the transition
`(old, new)` at the RUN tier (judged every step). The dependent-type reading "a method whose type states its
postcondition" is the same law attached to a method: `(method pay … (ensures P))` where `P : S → S → bool` is a term;
the runtime judges it after the run like a law with `occasion = invoke m`. That exists today as a law arm on
`invoke m` (`Escrow.ob`'s `(on invoke m …)`). So "a method whose type states its postcondition" is already
expressible and is the RUN tier; what it is not is a theorem anyone else can rely on without re-running, and THAT is
PCC's tier three.

**`Call.Fits` as a type a package carries.** `callFits` (`Lang/Call.lean:95-104`) is a refinement on `Body` (amounts
below `natLimit`, `once` within `bytesMax`) decided at run; its install-tier twin is `callSlotOk` on the slot's type.
"A package carries Call.Fits" means: the install check decides the type-level half (it does), the run decides the
value-level half (it does), and a package cannot carry more than that without a proof. The design adds nothing here;
it names what exists so nobody builds a third copy.

**The boundary with FABLE-PCC, stated so both can build.** TYPES owns every check the install check DECIDES from the
package text and the run DECIDES from the result, with no witness supplied by the member: grades, sub-rows, literal
refinements, legs. PCC owns every claim that needs a WITNESS: a proof object carried with the package, verified at
install by a reflected checker, stating a property of all runs or of the law. The interface between them: a proof's
STATEMENT may name the grades (`∀ run, movesOf run ≤ moves` is TYPES' theorem for free; `∀ run, balance' ≥ reserve`
is PCC's), and a grade is a hypothesis PCC's proofs may assume (the checker has decided it). Neither replaces the
judge: the law runs under both. Agreed by report line; PCC's report to confirm or fork.

## 5. What the kernel checks at install vs at run, by name (the whole list)

| when | check | refuses | cost |
|---|---|---|---|
| install | `effects` ascending, each a method, one per method | `noMethod ℓ`, `badEffect ℓ` | O(methods) |
| install | a value-moving arm under grade 0 | `effectExceeded ℓ` | O(size of the type) |
| install (next) | an edit slot naming a relation outside `writes` | `effectExceeded ℓ` | O(size of the type) |
| install (next) | a `holds` field not a `{amount, asset}` record of the value | `badRel ℓ` | O(rels) |
| run | `movesOf calls > grade.moves` | `program "effectExceeded"` | O(callsMax) |
| run (next) | an insert/retract of a `holds` relation with no matching leg call | `program "legUnfunded"` / `"legStranded"` | O(editsMax × callsMax) |
| never | anything that needs the body evaluated at install, or all runs | — | that is PCC |

No kernel refusal constructor is added: the grade is Lang's, the refusal is `program` with its name first (law 7's
convention for `program` reasons), and the kernel's own assertions where calls enter are unchanged. KERNEL-74 stays
reserved, unused.

## 6. Composition of Worlds: a World as a member

**What a World is, to another World (MEASURED).** E5 holds a World A's head in World B as an object of
`Std.headPackage` (`headStateTy`), posted by a member of B that follows A (`post {height, roots, steps}`), frozen by
`fork` when two posters disagree at one step count, judged by `headLaw` (`otherWorld`, `staleHead`, `forkedHead`,
`badHead`, `badFork`). A method of any package in B that reads a cell-keyed relation `(receipt)` gets, per key naming
such a head object, the column `{height, turn, tx}` that `Protocol.Foreign.check` verified against the head
(`notHead`, `forkedHead`, `badReceipt`, `notCommitted`, `headMismatch`, `pathMismatch`, `forgotten` by name) — under
the named premise that the held head is a head of a fold of A (`foreign_receipt_sound`'s `hr`).

**The type of a World as a term.** `headStateTy`. Nothing more is needed, and nothing more is honest: a World has no
callable surface from outside (charter; no cross-World atomic act), so to another World it is a VALUE that advances
(a head) and a set of FACTS about it (receipts). That is exactly a resident of read-only type whose transitions are
judged by a law and whose facts enter as checked columns — the IBC light-client shape (Goes 2020) with the proof
replaced by a posted head a member vouches for, which DESIGN-TRUST §1.4 already names as the head channel.

**A root law typed over a member World's head.** `lawTy headStateTy`, and `headLaw` is one. A root World that
federates N member Worlds holds a relation `members : {head : digest} → {world : digest}` (cell-keyed by the member's
head OBJECT in the root, so `(live)` says the head object is not retired and `(receipt)` verifies a member World's
receipts against it), or simply N head objects. The root's law over all member heads at once ("one head per origin")
is the kernel's (keys are unique in the rows trie). The root's law over EACH member head is `headLaw` as that head
object's own law. A root method that reads all member heads in one range read `(range 0 8)` sees up to
`rangeRowsMax` of them with columns — a federation-wide read of eight heads per Turn, which is the bound the design
accepts (a wider federation pages by prefix).

**Federation as recursion.** The root posts ITS head into a grand-root as a `Std.head` object; a head object of a head
object is a head object. The member-World's writer is enrolled in the root as a MEMBER (a key with a sponsor: `enroll`),
and its `post`s are judged like any member's. There is no second kind of thing: a World is a member exactly as a
person or an agent is (DESIGN-TRUST M6: "agents and people are the same kind of member"; now Worlds too). This is
Polkadot's relay/parachain shape (Wood 2016) and Plasma's child chains (Poon–Buterin 2017) with the exit game
replaced by re-execution: a root member who holds the child's log audits it (admission is re-execution, both levels).

**What is missing, and whose it is.**
1. **A `certified` column (TRUST).** Today a posted head is the POSTER's word; `headLaw` orders heads and freezes
   forks and cannot tell an honest head from a lie (`StdHead.lean` header; HOLISTIC-LANG §2.3). T3 of DESIGN-TRUST
   (writer-signed heads under a genesis `Authority`) makes a head CERTIFIED; the runtime column `(certified)` beside
   `(live)`/`(receipt)` is where the root's law reads it, and `Protocol.Foreign.check` is where it is verified (the
   one verifier Lang calls, `ReceiptCheck`; Lang has and must have no signature primitive). Then a root law can
   require: a member head advances only to a certified head. TYPES' part is the column's TYPE (`seenTy` gains
   `certified : bool`, or a second column); the check is TRUST's.
2. **`Req.caller : opt digest` (LANG; a week).** A member World's object cannot today tell the root's law WHICH
   object called it (the LANG reader's fourth point). For federation this is "which member World acts": a root law
   on `invoke m` wants the caller's package (= the member World's registered head package) in `Req`. Priced in §7.
3. **Head posting by the member World's own writer (TRUST's T2).** Today a member of B posts A's head; for A to be
   a member of B, A's writer key is enrolled in B and posts its own head. No new kernel act; one enrolment and T2's
   self-head post.

Nothing of §6 is built in this lane (TRUST owns `Std.head` and `Protocol/Foreign`); the design is here so TRUST's T2/T3
land with the recursion in view and the `seenTy` column's type agreed by report line.

## 7. The price, in the spec's terms

**TOPLEVEL-SPEC.** INTEGRITY B3 (law) gains one clause the author is promised: "and every run of your method moved at
most its declared grade" (a conjunct of `RunMeans e`, read off `runMeasuredWith_moves_le`). B2 (value) is untouched:
conservation does not depend on grades. B1 (authority) untouched. The floor gains `ungradedKernel` (a `Lang.program`
whose `checkMoves` is `.ok ()`), refuted by EF3. ONE HISTORY untouched.

**Landed theorems that change (map lines, measured on the build; INFERRED here).**
- `Lang/Proofs/Load.lean`: `runSetupWith_spec`/`runSetup_spec` if they spell `RunSetup`'s record (a new field):
  RESTATES-MEANING ×2.
- `Lang/Proofs/Wire.lean`: `packageCodec_label`, `packageVersion_lawful`, `decodePackage_refused_label`,
  `packageCodec_get_refused` and the `lang/package-version/5` spellings: RESTATES (label) ×~6; `packageOf_packageTree`-
  style round trips gain the `effects` child: RESTATES-MEANING ×~4.
- `Lang/Proofs/StdOfferEscrow*.lean`: nothing unless a theorem spells `offerEscrowPackage` as a record literal
  (`escrow_shape` is about the VALUE type, not the package: MEASURED, unchanged).
- `Emit/Vectors.lean`: the package site's 54 rows re-draw (first byte 05 → 06 and the empty `node 4` child); one new
  vector row for a package with effects.
- Journeys: every World re-runs from genesis (as every `lang!`); P8's commit package and the escrow declare grades;
  `Escrow.ob` declares `(effect (moves 1000))` (its Ledger rows move ≤ that; MEASURED before landing).
- `Hosting/Proofs/Package.lean`, `Hosting/Proofs/Allowance.lean` use `methodSig` (type only): unchanged.

**`Req.caller` (not in this lane).** `Req` gains a field; `reqTy` gains `("caller", optTy .digest)`; every law and
method's binder type changes, so every generated package re-emits and every theorem that spells `reqTy` or `reqData`
restates (`Lang/Proofs/{Bell,StdOffer*,StdActivity*,LawMeaning}`: dozens). A week, one `lang!`. The first grade that
NEEDS it is `invokes`-from-the-callee's side ("only my peer may call `take`"), which the escrow wants (LANG-77's K).

## 8. How it composes with META's generators and PCC's proofs

- **META (generators as installed packages).** A generator emits a package; it emits its `effects` too, as data. A
  generator that is itself a nano program emits a package WITH grades, and the install check decides them exactly as
  for a hand-written one: the grade is on the generated package, not on the generator, so "install a generator" needs
  no new rule. What META gains: a generator's OWN grade (`invokes`, `writes`) bounds what the packages it installs may
  do only if the install act is a call the generator makes — `Body.install` is not callable by an object today
  (`Body.callable`); if META makes it callable, the grade `installs : Bool` is one more label in §2.6's list.
- **PCC (proofs a member supplies).** A grade is a HYPOTHESIS PCC's checker may admit without a witness (the install
  check decided it); a proof's statement may quantify over runs under that hypothesis. The boundary is §4's rule.
  The escrow's "receives" claim (LANG-82's `LegsMatch`) stays a theorem/PCC claim; `holds` (§3) makes its "moved"
  half a run check.
- **CTX (slots, holes).** A hole's candidates are closed terms checked at the hole's context; a candidate that
  returns a `transfer` lives in a method whose grade bounds it: the grade is per METHOD, not per candidate, so
  selection cannot escape it. No interaction with `instantiateHoles` (the grade is read after extraction).
- **TRUST (heads).** §6: the `seenTy`/`certified` column type is TYPES'; the check is TRUST's.
- **AGENT (the resident as a member).** An agent's package gets grades like any other: "an agent that may move at
  most 10 per ring" is `(effect (moves 10))` on `answer`, the smallest true thing axis 3 asked for ("laws that
  constrain what it may do") stated in the type.

## 9. Sequence

1. **LANG-89 (this lane, built):** `Effect {moves}`, the package field, the wire bump, `effectExceeded` at install and
   at run, `runMeasuredWith_moves_le`, the EF rows, the three packages' grades. `lang!`.
2. **LANG-90:** `holds` on relations (§3): `legUnfunded`/`legStranded`; the escrow declares `holds := some "give"`;
   P8d/P8e re-read as refusals. `lang!` (RelDecl wire).
3. **LANG-91:** `writes` and `grants` sub-rows (§2.6): install-only. `lang:` if the wire needs no new node (the
   sub-sum lives in the type; `Effect` gains the two lists — that is wire, so `lang!` again; fold into 2 if close).
4. `Req.caller` (§7), then `invokes` by package and `moves` per asset.
5. With TRUST: the `certified` column type; with PCC: the hypothesis interface of §4.

## 10. Three ways this design is most likely wrong

1. **The grade belongs in `Ty` after all.** If a future `Ty` gains an indexed form (bounded naturals `nat≤n`, which
   the codec could carry as a `u64` with a checked bound), the `transfer` arm's `amount : nat≤n` would put the grade
   in the arrow and `effects` would be a twin. I judge that a year away (every metatheorem over `Ty`), and the
   package field is deletable in a day when it comes. Watch for it; do not pre-build it.
2. **`moves` summed across assets is the wrong unit.** A grade of 12 that lets 12 α or 12 β move is a bound on units,
   not value. It is still a bound every run respects, and per-asset is §2.6's third item. If the first real package
   needs per-asset on day one, do that first.
3. **The run check should be the KERNEL's, not Lang's.** The kernel sees the calls (`invoke`, `Derive.lean:222`) and
   could enforce a grade carried in the package cell. It would need to read Lang's package (a layer inversion) or a
   grade in a kernel slot (a second copy). Lang's runtime already reads the calls against the declared slot types
   (`callsOf`); the grade is one more declared thing read in the same place. If TRUST's kernel work puts a per-object
   cap in a kernel slot (as grants have ledgers), the two should be reconciled then, not pre-empted now.

## BUILT — appended per landing

- 2026-10-26 (FABLE-TYPES, not yet landed): §2 as LANG-89 on hbox `wt/fable-types` over 18cd38b: `Effect {moves}`,
  `Package.effects`, wire 5 → 6, `effectExceeded` at install (`checkEffects`) and at run (`checkMoves` after `callsOf`),
  surface `(effect (moves N))`, core `(effects (ℓ N)…)`; the EF journey rows GREEN (EF1 admitted, EF2 refused at install
  by name, EF3 refused at run by name, nothing moved); vectors re-drawn (54 package rows). Pending: one proof
  (`readPackage_closedText`'s effects branch), the theorem `runMeasuredWith_moves_le`, the full judge, the landing.

## 10. What would make the other choice right (the grade IN `Ty`)

The grade sits beside the type (§2.1) because `Ty` carries no quantities. The other design, a refinement on the
transfer arm's `amount` (`nat ≤ n` as a type), becomes right exactly when `Ty` gains a bounded natural FOR ANOTHER
REASON: a `(nat lo..hi)` type that the checker decides on literals and the run checks on values would carry `Bound`
(§4) into the type and make the grade one instance of it. Then `Package.effects` is deletable in a day: `methodMoves`
reads the arm's `amount` bound instead of the table, `checkMoves` is the run's bound check, the wire loses `node 4`,
and `effectTree`/`effectOf`/`effectSx`/`Read.effect` go with it. Until `Ty` has that natural, the table is the one
place a quantity can live without reopening the checker, the codec and the metatheorems over `Ty` (LANG-3).

## BUILT (FABLE-TYPES-2, 2026-10-26)

- LANG-89 as §2 and §2.5 states, with EF4/EF5 (two transfer slots, `amount` of α and `amount + 1` of β — one effect per
  cell per Turn is the kernel's rule, `duplicateEffect`: 4 + 5 admitted, 5 + 6 refused: the grade is the SUM; a `movesOf` taking the largest
  call admits EF5's run: EF5 red). The text reader bounds nothing (`Read.effect` reads a bare
  `toNat?`, as `Read.rel` reads `limit`): the `< 2^64` bound is `effectWire`'s at encode, so `readPackage_closedText`
  holds as stated. Theorems `runMeasuredWith_moves_le` (any setup) and `runMeasured_moves_le` (the deployed setup:
  `(p.effectOf ℓ).moves`) in `Lang/Proofs/Effect.lean`. Wire version: **7** (META's 1bdd5ba took 6 while the full judge
  was green twice and displaced twice by a moved main). Landed **6e177d55** (RELAND-TYPES, 10-27) at wire version **8** (CTX's LANG-84 took 7).

## 3.1 BUILD SPEC for LANG-90 — `holds`: a row holds a leg (FABLE-TYPES-2, 2026-10-26; MEASURED at c82f171)

**The field.** `RelDecl.holds : Option Label` (eighth field; every `⟨…⟩` literal of a `RelDecl` gains it: `escrowDecl`,
`offerSessionDecl`, `Std.*` relation decls, `Emit.Vectors.relAll/relNone`, the fixtures — RESTATES-MEANING each). The
named field of `val` is a LEG: `legTy := .record [("amount", .nat), ("asset", .digest)]`, which is `escrowLegTy` today
(`Lang/StdOfferEscrow.lean:41`): the definition moves down to `Lang/Package.lean` and the escrow's name becomes an alias
or is deleted (prefer deleted: one name).

**Install (`checkRel`, O(rels)).** `holds = some f` ⇒ `val = .record fs` with `Row.find? f fs = some legTy`, else `badRel ℓ`.
Nothing else: a relation may hold a leg whether or not it is retractable.

**Run (`checkLegs`, beside `guardEdits`, O(edits × calls)).** `guardEdits` already computes `olds ← es.mapM guardOld`
(the old row's data as `optD`, `Lang/Rel.lean:348`); `checkLegs digestOf self calls es olds` runs right after it, on the
same `es.zip olds`. Per edit of a relation with `holds = some f`:
- `.insert`: the NEW value's leg (`e.data = .inj "insert" (.record [("key", _), ("val", v)])`, `v`'s field `f`) is
  `needIn (asset) += amount`.
- `.retract`: the OLD row's leg (`olds` at `optD (some o)`; `optD none` = no old row: the kernel refuses the retract
  anyway, count nothing) is `needOut (asset) += amount`.
- `.upsert`: BOTH — the new leg needs funding, the old leg (if any) needs paying out. Under the kernel's one effect per
  cell per Turn (`duplicateEffect`, `actFor`) a run cannot move the same asset both into and out of the object's one
  account, so an upsert that changes a held leg of one asset is refused `legStranded` by construction; that is right (a
  held leg is replaced by retract-then-insert over two runs, each paid), and it is said in the docstring.
A leg's `asset` is digest BYTES in `Data`; `digestOf` (in scope in `runMeasuredWith`) lifts it to `D`; bytes that are no
digest refuse `legUnfunded`/`legStranded` (the row cannot be backed). What the calls move, per asset `a` of the OBJECT's
accounts (`AcctRef.of self a`): `movedIn a = Σ amount over transfer … (dst := .of self a) … and credit _ (.of self a) …`;
`movedOut a = Σ amount over transfer (src := .of self a) …`. Refuse **`program "legUnfunded REL"`** when some asset has
`needIn a > movedIn a`; **`program "legStranded REL"`** when `needOut a > movedOut a` (REL the first relation that fails,
by edit order; the name first, law 7). Sums, not one-to-one matching: two inserts of 3 α under one transfer of 6 α into
self are backed; this is the per-asset conservation the rows need, and it is what `admit_value` lets the history theorem
use.

**Why not net (`needIn − needOut ≤ movedIn − movedOut`).** Net admits a retract that pays nothing when nothing else
moves (−5 ≤ 0): the value stays in the object with no row naming it — exactly P8d/P8e's stranding, the tooth of §3. Two
inequalities, one per direction, refuse it. Under `duplicateEffect` only one direction per asset happens in a run anyway.

**Wire (`lang!`, version 6 → 7, or 8 if PCC's L2 lands first: never two different sevens; agree by report line).**
`relTree` gains an eighth child `optLabelLeaf r.2.holds`; `relOf` matches eight; `relWire` adds `r.2.holds.all labelOk`;
`Lang/Proofs/Wire.lean`'s `relOf_relTree`, the package round trips, the fixture trees (`relAll`, the Wire teeth) follow;
`lang/package/7`, `lang/package-version/7`; vectors re-drawn (the package site: every tree gains the child; the two
`relAll`/`relNone` rows pin it set and unset).

**Text.** Core `relSx` gains `(holds)` / `(holds f)` as the eighth section (after `(guard …)`; `optLabelSx`), `Read.rel`
reads it (an eighth list element, mandatory in the core text as `(guard …)` is); surface `(rel ℓ … [(holds f)])` in
`relHead`. `Lang/Proofs/Print.lean` `rel_relSx`/`relSx_ok`/`rels_prints` gain the section; `relWf` is unchanged (a label).

**Theorem (`Lang/Proofs/Holds.lean`).** `runMeasuredWith_legs`: a returned run's edits and calls satisfy, for every
asset, `needIn ≤ movedIn ∧ needOut ≤ movedOut` over the `holds` relations (read off `checkLegs`, as
`runMeasuredWith_moves_le` reads `checkMoves`). The history theorem — every row of a `holds` relation is backed by value
the object received and has not paid out (Σ legs held ≤ the object's balance of that asset, an invariant over the
object's history from `admit_value` plus this per-run check and the row acts) — is the NEXT landing's, stated here so
nobody mistakes the per-run theorem for it.

**The escrow.** `escrowDecl` declares `holds := some "give"` (`offer`); `session` none. P8d/P8e (the take or withdraw pays
nothing) are then refused at RUN, `legStranded offer`, for the escrow and for every package: the journey gets rows that
show it without mutating a generator — a Vault package (`Lang/Journey/Holds.lean`, §EH): relation `vault (holds leg)`;
`deposit {amount}` inserts a row and transfers `amount` agent → self (admitted); `depositUnpaid` inserts without a
transfer (`legUnfunded vault`); `withdraw` retracts and pays self → agent (admitted); `withdrawUnpaid` retracts without
(`legStranded vault`); `depositHalf` inserts a leg of 10 under a transfer of 5 (`legUnfunded`); two deposits of 3 α under
one transfer of 6 α (admitted: sums). Plant: `checkLegs := fun … => .ok ()` reds the theorem and the two Unpaid rows.

**Price.** `lang!`; ~70 map lines again (every `RelDecl` literal and every fixture tree); every package re-ids; nothing
deployed holds one. A day.

**Critique.** `holds` names ONE leg field; a row holding two assets needs two relations or a later `holds : List Label`
(the sums generalise unchanged). The check reads the OLD row through `guardOld`, which needs the row pinned: an unpinned
retract is already `rowUnpinned`, so no new pin obligation. `credit` into self counts as funding though no deployed
package credits. The check is per RUN; a held leg paid out by a LATER run of another method with no retract (the
object's own `pay`) is the history theorem's concern, and until it lands the only guard is the grade (LANG-89).

- LANG-90 (`holds`) landed **b03731b6** (RELAND-TYPES, 10-27) at package wire 9, as §3.1 specifies, with one change: the
  field has a default (`holds := none`), so only anonymous literals restate. The history theorem is the next landing.
