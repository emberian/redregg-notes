# DESIGN-PCC — what a proof about an INSTALLED program is in nano, what the kernel can check, and the smallest true thing (real 2026-10-26)

Author: FABLE-PCC (a Fable), axis 2 of `FRONTIER-AXES-20261026.md`. Read against nano `origin/main ad90a47`
(mirror `~/dev/nanodregg`, hbox worktree `/tank/dregg-build/nanodregg/wt/fable-pcc`). Inputs: VERDICT-20261024 §3,
HOLISTIC-GATES, HOLISTIC-LANGPROOFS (§1 "proof-carrying authorization", §4 the `MethodSpec` tier), TOPLEVEL-SPEC
§3.3 (B3, the law clause) and §10.3, memory `project-no-proof-system-in-mini-admission` (mini's `witnessed`
compiled to FALSE), CHARTER scope item 1, and the code: `Lang/Term.lean`, `Lang/Eval.lean`, `Lang/Check.lean`,
`Lang/Package.lean`, `Lang/Program.lean`, `Lang/Law.lean`, `Lang/Std.lean`, `Lang/StdOfferEscrow.lean`,
`Lang/Proofs/{BigStep,Std,Receiver,Chain,Rel}.lean`, `Kernel/Receive/Derive.lean`, `Kernel/Bounds.lean`,
`Kernel/Proofs/Logic/History.lean`, `world/escrow/Escrow.ob`. Tags: **READ** (path), **MEASURED** (a command I
ran, on hbox at ad90a47), **INFERRED** (attack first).

## 0. The answer in one page

**The kernel already checks one proof about every installed program: its type.** `checkE ifaces body iface`
(READ `Lang/Package.lean` `Package.checkWith`, `Lang/Check.lean` `inferE`) is a proof checker in Necula's original
sense: the claim is the interface type, the proof is the term itself, the checker is a one-pass syntax-directed
function, and the Lean metatheorem (`Lang/Proofs/Check.lean` `inferE_sound`, `Lang/Proofs/Sound.lean`
`run_sound`) says a term that checks never gets `stuck`. Typed assembly language (Morrisett et al. 1998) was the
first PCC whose proofs were the annotations in the code; nano's install check is that. So the question "what
would it take for the kernel to check a proof about a program" has an existing answer whose shape is the right
one, and the real question is: **what richer claim language can the install check decide in one pass, with the
term (plus its own control structure) as the proof?**

**The second thing the kernel already does is stronger than any proof for one whole class of claims.** Every
step of every object is judged by its laws by re-execution, on every member (B3: "your law was run"). A claim of
the form "the state after each admitted step satisfies P(old, new, req)" needs no proof: it is MONITORED, at
29–108 ticks per judgment (MEASURED below), out of a `lawTicks` budget of 100,000. Schneider's enforceability
result (TISSEC 2000) is the theorem here, and LANGPROOFS §3(c) already names the receiver as the monitor. Necula's
economic argument for PCC — avoid the runtime check — is worth 33 ticks per step in nano. That is not what a
proof buys here.

**What a proof buys in nano is a SUMMARY the World vouches for.** Today a member deciding whether to create an
object of package P, to post a leg into an object of P, or to adopt a law package L has exactly two sources: the
term (27,865 chars of core for the Bell) and the doc string ("exactly one payout", READ `world/escrow/Escrow.ob`,
which the kernel never reads). VERDICT §3's sentence — "every defect I found yesterday sat under such a sentence"
— is about Lean docstrings, and it is equally true of package docs: the World cannot tell a package whose doc
lies from one whose doc is true. A CLAIM is a sentence in a small fixed language, carried by the package in its
identity, that the kernel REFUSES TO INSTALL unless the term bears it. That is the trust architecture of PCC
(the consumer trusts the checker, not the producer), and the checker is small because the claim language is
small. It also closes the gap TOPLEVEL-SPEC §3.3(ii) leaves open by design: B3 promises "your law was run", not
"your law means its name"; a claim is the kernel-checked piece of "means".

**The proof object is the certifying SHAPE of the term, and the checker is Lean, not the machine.** The brief's
"one way this is wrong" — reflection inside a metered interpreter — is avoided, not solved: the checker runs
where `checkE` runs, inside `checkInstall`, which is not metered (an `install`'s tree pool is 0, READ
`Kernel/Receive/Derive.lean` `poolOf`) and is bounded by the package's own wire bounds (`Wire.nodeMax`,
`depthMax`, `rowMax`) because it is O(|term|). A nano term never checks a proof; the kernel does, once, at
install, as it already types the term. No proof is run by the machine, so no ticks are spent on it ever.

**The fragment, honestly: control-dominance claims.** The first claim class is `keeps I by L`: every state an
object of this package ever holds satisfies the Boolean field `I : S → bool`, because the law `L` refuses every
birth, adoption, write and invoke whose new state fails `I`. Its proof is the law's control structure: every
`ok` leaf of `L`'s body lies in the true branch of `ite (I new) …` (the relaw arm excepted, where the kernel
holds the state fixed, READ `Derive.lean` `law`: `judge … (stateOf cell) (stateOf cell)`; the adopt arm is NOT
excepted: an adoption is a base case like a birth, the incoming law judging the state it is adopted over,
KERNEL-27, so a law in shape refuses to be adopted over a state that fails its invariant). The checker is a
dominator walk (§3.2); its soundness is one Lean theorem over `BigStep` (§3.3); its lift to the World is one
composition with `object_history_chain` (READ `Kernel/Proofs/Logic/History.lean:341`). The second class
(§5), `pays m` (a method's call slot is a transfer of a stated field to a stated party), is the same idea over
the `calls` row, and together with a `keeps` on the phase field it turns the Escrow's doc "exactly one payout"
into two kernel-checked sentences. What this fragment cannot say — anything quantified over inputs that the
control structure does not decide, anything about two runs, anything about cost — is listed in §6 with the
proof object each would need (a certificate the checker re-runs, a WP derivation), and the price of each.

**What the top-level spec gains.** INTEGRITY gets a fourth sentence, B4: "every claim an installed package
carries holds of every object of it along every audited log", with its own FLOOR (`uncheckedInstallKernel`: a
kernel that accepts claims without the checker; it installs a package claiming `total ≤ 100` by a law that
admits everything, and one `set 101` refutes the sentence) and its inhabitant (journey row LK1). It is not a
consequence of B3: B3 is true of a kernel that ignores claims. It is a strengthening of B3's clause (ii) from
"your law was run" to "your law MEANS its claim", for exactly the claims in the fragment.

## 1. What a package is today, and what the kernel checks of it at install (READ)

A `Package` (READ `Lang/Package.lean:33`) is `{imports, state, iface, body, methods, laws, rels, doc, holes}`:
imports by digest, a data state type, a canonical record interface, ONE body term of that type, which fields
are methods (`methodTy`) and laws (`lawTy S = S → S → reqTy → verdictTy`), the relations, a 256-byte doc
"never run, never judged", and the contextual ROM. Its id is the content digest of its ROM cell, so it commits
to the import ids and through them to the closure.

`install pkg` (READ `Kernel/Receive/Derive.lean:110`) is `X.program.checkInstall look pkg` then a ROM cell.
`checkInstall` (READ `Lang/Program.lean`) decodes the bytes (canonical or refused by name), loads the import
closure through the one admission every run uses (`admitContextual`, LANG-78), and admits the package by that
admission: `Package.checkWith ifaces p` = shape bounds (`checkShape`), the body at its interface (`checkE`,
naming the failed rule and path), then the fields (`checkRels`, `checkMethods`, `checkLaws`: each law is a
field of type `lawTy S`), then the id-literal boundary (`checkLits`, LANG-38). Nothing else. A package's doc, its
docstring in a `.ob`, and every theorem in `Lang/Proofs/` are outside the World.

What the kernel checks of a package PER STEP: every law in force on `old → new` under `req` (`judge`), each
under `lawTicks`; every row edit's guard (`guardEdits`); the calls' kinds (`callsOf_callable`); value
conservation over the whole Turn (`admit_value`). Laws see `(old, new, req)`. They do NOT see the calls a method
made (INFERRED from `judgeOneWith`'s arguments and `invoke`'s order in `Derive.lean:196`: the run returns
`(new, calls, rows, used)`, the judge gets `old new r`, the calls are derived after). This is the one
per-step gap that is not a monitor's today: "the escrow pays what the want leg says" is about the calls, and no
law can refuse a wrong payment. (LANG-82 put that check INSIDE the method's own term, `escrowFairT`, which is
right for the generated escrow and invisible to a reader of a hand-written one.)

## 2. The measurement the brief asked for

MEASURED on hbox (`lake env lean --run logs/MeasureLaw.lean` in wt/fable-pcc at ad90a47; the script calls
`Lang.run` on `applyAt (get (ref 0) "escrow")` exactly as `runLaw` does and reads `used`):

| law, occasion | ticks |
|---|---|
| `Escrow.escrow`, birth open→open | 47 |
| `Escrow.escrow`, invoke deposit open→held | 94 |
| `Escrow.escrow`, invoke release held→released | 108 |
| `Escrow.escrow`, invoke release from released (refused `settled`) | 53 |
| `Escrow.escrow`, write (refused `frozen`) | 29 |
| journey `Owned.bounded`, set 50 | 33 |
| journey `Owned.ownerOnly`, set 50 | 49 |

Against `lawTicks = 100,000` per law per step and THE BAR's counter invoke at 34 ticks (gates/waste.tsv), a
monitor costs about as much as the method it judges. Two consequences for the design:

1. **Ticks are not the argument for static checking.** Adding an invariant as an extra monitored law would cost
   ~30–50 ticks per step forever; a static check costs one O(|term|) pass at install. The saving is real and
   irrelevant at these sizes. The argument is the summary (§0), not the budget.
2. **Reflection is ruled out by the budget, as the brief guessed.** A proof checker written AS a nano term and
   run by the machine would cost, per proof node, the machine's ~1.58 ticks per required step (waste.tsv
   `ticks-per-required-step`) times the checker's own interpretive overhead (a `case` per rule, a `get` per
   field at 2 rules each, record fields re-evaluated at every selection, LANG-2). A 500-node derivation checked
   by a term interpreter would land in the tens of thousands of ticks, against an install that has no budget
   at all and a tree pool of 131,072 for every run under one call. More to the point, nothing is gained: the
   machine is Lean-compiled code, and so is the checker; running the checker through the machine adds one
   interpreter between the same two trusted things. The checker lives beside `checkE`, in Lean, unmetered,
   bounded by the wire. The cost that matters is then the PACKAGE's size, which the claim does not increase (two
   labels) and the certifying shape increases by the invariant's repetition inside the law (one `app I new`
   per guarded leaf; §3.4).

## 3. The design: claims, the certifying shape, the checker, the theorem

### 3.1 What a package carries

```lean
/-- A claim a package makes of itself, checked at install (LANG-83). -/
inductive Claim
  /-- every state an object of this package holds satisfies the interface field `inv : fn S bool`,
  because the law `law` refuses every birth, write and invoke whose new state fails it -/
  | keeps (inv law : Label)
```

`Package.claims : List Claim := []`. Wire: a ninth child of the package tree, `node 4 .empty (claims.map
claimTree)` with `claimTree (.keeps i l) = node 0 .empty [labelLeaf i, labelLeaf l]`; `packageWireVersion` 5 → 6,
the refine labels `lang/package/6`, `lang/package-version/6`. Text: an optional section `(claims (keeps inv
law) …)` after `(body …)` and before `(holes …)`, printed only when non-empty, so every shipped core text is
unchanged and every package re-ids (the version byte). Surface: a declaration `(claim keeps inv law)`. The claim
is in the package's identity on purpose: a reader who trusts an id trusts its claims, and a package cannot gain
or lose a claim without becoming another package.

The ticks a claim costs: none at run time (nothing is added to any law or method); at install, one dominator
walk of the law's body per claim, O(|law|), unmetered like `checkE`. There is no "proof too costly" refusal in
this class because there is no proof object to size; §6's certificate classes get one.

### 3.2 The certifying shape and the checker

A law in certifying shape for `keeps I` has every `ok` leaf dominated by the test `I new`. The checker
`Term.guardedBy I k r t : Bool` walks `t` with `k` the de Bruijn index of `new` and `r` of `req` at the current
depth (`k = 1, r = 0` under the law's three binders, LANG-5's convention `var 2 old, var 1 new, var 0 req`):

| `t` | `guardedBy I k r t` |
|---|---|
| `ite c a b` | `(c == app I (var k) ∨ guardedBy I k r a) ∧ guardedBy I k r b` |
| `case s arms` with `s == get (var r) "occasion"` | every arm `(ℓ, body)`: `ℓ ∈ {adopt, relaw} ∨ guardedBy I (k+1) (r+1) body` |
| `case s arms` otherwise | every arm: `guardedBy I (k+1) (r+1) body` |
| `inj _ "ok" _` | `false` (an unguarded `ok`) |
| `inj _ ℓ _`, `ℓ ≠ "ok"`; `refuse _ _` | `true` |
| anything else (`var`, `get`, `app`, `lam`, `fix`, `record`, `extend`, `prim`, literals, `ref`, `hole`) | `false` |

The last row is what makes the checker sound by construction and incomplete by design: the only way a term in
the checked tree can MEAN `inj "ok" w` is through a literal `inj` leaf, since every other former that could
yield a verdict (a variable bound to state data whose sum type happens to be `verdictTy`; a `get` of a record
field; an applied lambda) is refused outright. A law written through a helper lambda, or one that returns a
verdict it read from its state, is not in certifying shape and its claim is refused `claimShape` — the
author rewrites the law, exactly as a certifying compiler emits checkable code. Every `Std` law is in shape
already up to one detail (§3.4). The `I` compared is the literal term of the interface field `inv` (closed:
`lam S ib`), so no de Bruijn shifting is needed: `app I (var k)` is syntactic equality of the closed `I` and the
one index `k`.

`Package.checkClaims p : Except CheckError Unit`, run by `checkWith` after `checkFields`: for each `keeps inv
law`: `law ∈ p.laws` (else `claimNotLaw law`); `inv` a field of `p.iface` at type `fn p.state bool` (else
`claimNotInvariant inv`); `p.body = record fs` with `find? inv fs = some I` and `find? law fs = some (lam S (lam
S (lam reqTy b)))` (else `claimShape law`); `guardedBy I 1 0 b` (else `claimUnproved law`). Four refusals, by
name, on the wire as `program "claimUnproved bounded"` like every `CheckError`. A layer (`extend (ref 0) adds`,
READ `Lang/Surface.lean` `layerOf`) inherits its super's laws and cannot see their bodies, so a layer's claim on
an inherited law is `claimShape` in this landing; the inheritance rule (a layer may claim what its super claims,
refused `claimRequired` when the super does not) is the first item of §5 because the kernel lift for layers
(`object_history_chain` wants `p.body = record fs`) is the same gap B3 already has.

### 3.3 The theorem, in three layers, each over the real definitions

**(a) The term layer** (`Lang/Proofs/Claim.lean`, NEW): the dominator walk is sound for `BigStep`.

```lean
/-- `ib` (the invariant's body, `var 0` the state) holds of `n`. Stated as `Std.Admits` is, over some
closure environment: `ib` is typed `bool` under `[S]` at install, so it reads only `var 0`. -/
def Keeps (lib : List Term) (ib : Term) (n : Data) : Prop :=
  ∃ env, BigStep lib (n.toVal :: env) ib (.ok (.bool true))

theorem guardedBy_sound {I ib : Term} (hI : I = .lam S ib) : ∀ {t : Term} {k r : Nat} {env : Env} {w : Val},
    Term.guardedBy I k r t = true → BigStep lib env t (.ok (.inj "ok" w)) →
    (∃ x, env[k]? = some x ∧ ∃ env', BigStep lib (x :: env') ib (.ok (.bool true))) ∨
    (∃ rq ℓ x, env[r]? = some rq.toVal ∧ rq.field "occasion" = some (.inj ℓ x) ∧ (ℓ = "relaw" ∨ ℓ = "adopt"))

/-- A law in certifying shape that ADMITS a birth, write or invoke leaves a state that keeps `I`. -/
theorem keeps_step (hg : Term.guardedBy (.lam S ib) 1 0 b = true) (h : Std.Admits lib (.lam S (.lam S (.lam reqTy b))) rq n o)
    (ho : rq.field "occasion" = some occ) (hc : Std.IsChange occ ∨ ∃ x, occ = .inj "birth" x) : Keeps lib ib n

/-- Along a `Std.Chain` of the law's steps (`Std.Step`: `Admits`, and a relaw/adopt keeps the state), every
state keeps `I` once the first does. -/
theorem chain_keeps (hg : …) (h0 : Keeps lib ib o) (hc : Std.Chain (Std.Step lib law) o steps) : ∀ s ∈ steps, Keeps lib ib s.2
```

The proof of `guardedBy_sound` is an induction on `t` with the inversion lemmas `Lang/Proofs/Meaning.lean`
already has (`bigStep_ite_ok`, `bigStep_case_ok`, `bigStep_getVar`, `bigStep_inj_ok`); the `app I (var k)` case
is `app` inversion plus the `lam` rule: the closure is `clo ib env`, the argument is `env[k]`, and the body ran
under `x :: env`, which is the witness. `keeps_step` is `guardedBy_sound` at `k = 1, r = 0` with the occasion
read off `reqData` as `lawCase5_arm` reads it. No renaming lemma, no typing premise. The `∃ env` in `Keeps` is
the one weakness worth a sentence: `ib` is typed under `[S]` so it reads only `var 0` (`hasType_usesVar_lt`), but
`Lang/Proofs` has no "BigStep ignores unused variables" lemma; until it does, `Keeps` is stated as `Admits` is
and is exactly as strong on typed terms, by determinism over a fixed environment.

**(b) The install layer** (same module): what `checkInstall` admitted carries the witness.

```lean
theorem install_claims (h : checkInstall digestOf look b = .ok ()) (hp : Wire.decodePackage b = .ok p)
    (hc : .keeps inv law ∈ p.claims) :
    law ∈ p.laws ∧ ∃ fs ib b', p.body = .record fs ∧ Row.find? inv fs = some (.lam p.state ib) ∧
      Row.find? law fs = some (.lam p.state (.lam p.state (.lam reqTy b'))) ∧ Term.guardedBy (.lam p.state ib) 1 0 b' = true
```

**(c) The World layer** (`Kernel/Proofs/Logic/Claims.lean`, NEW, cross-layer): the composition with THE LIFT.
`object_history_chain` gives, for a `NoRef` law in force at every judged step of an `ObjectHistory`, a
`Std.Chain (Std.Step [] t)` from the object's state, step for step; `chain_keeps` walks it.

```lean
/-- B4, the claim clause of INTEGRITY. -/
theorem object_history_keeps (hX : X.Lawful) (hprog : X.program = Lang.program …) (hpkg : readPackage … = .ok p)
    (hc : .keeps inv law ∈ p.claims) (hchk : p.checkWith ifaces = .ok ()) (hnr : NoRef t) …
    (h : ObjectHistory X obj w w' tr) (hin : ∀ e ∈ tr, lawId ∈ laws-in-force e ∧ readPackage e.1 lawId = .ok p)
    (h0 : Keeps [] ib o) : ∀ e ∈ tr, ∃ n, readState … e.new = .ok n ∧ Keeps [] ib n
```

Its premises are B3's (§3.3 of TOPLEVEL-SPEC: `NoRef`, the law in force at every step, the package read as `p`
in every view) plus the claim and the start state; its floor and inhabitant are §4. The start state is the
BIRTH's: `create` judges the seed as `birth` with `old = new = seed` (READ `Derive.lean:146`), and the birth arm
is not exempt, so `keeps_step` gives `Keeps ib seed`; the kernel-side theorem that a born object's state was so
judged is `create`'s next-slots lemma, to be named in the landing (INFERRED that `write_next_slots`'s sibling
for `create` exists in `Kernel/Proofs/WriteNext.lean`; if not, `h0` stays a premise and the row discharges it).

### 3.4 What this does to the generators

`Std.bounded S f max` (READ `Lang/Std.lean:132`) is `lawOf S c c (fun _ => okT) c` with `c a = allOf [(le
(newF f) max, …)]`: its relaw arm is a bare `okT` (exempt, correct), its other arms are `ite (prim le (get (var
2) f) (nat max)) ok refused` — in shape except that the test is INLINE, not `app I new`. Two ways to make `Std`
packages claimable: (i) a renaming lemma for `BigStep`, so the checker may match the invariant's body shifted
to depth `k` (a simulation proof over `BigStep`/`Sel`/`Ext` with a value relation, as `Lang/Proofs/LawMeaning.lean`
does for hole blocking: ~250 lines, and it unlocks every future claim that relates terms at different depths);
(ii) `Std.keeps S inv` as the generator of a certifying-shape law (`c a = guard (app inv a.new) "invariant" okT`),
and `Std.bounded` re-emitted through it. The landing takes (ii) for the prototype (the journey's package is
hand-written) and files (i) as the next step; it is the one piece of proof infrastructure this design needs
that the tree lacks.

## 4. What the top-level spec gains: B4

**Sentence.** Every claim an installed package carries is true of every object of that package along every
audited log: for `keeps inv law`, every state the object's cell ever holds (its seed included) satisfies `inv`.

**TODAY: unstatable** (no package carries a claim; the doc is the only sentence and it is never read).
**After the landing: true** for the fragment, with B3's restrictions (NoRef laws; a record-literal body).

**FLOOR.**
* Refuted by `uncheckedInstallKernel`: `checkInstall` with `checkClaims` replaced by `.ok ()` (the plant
  `skip-claims`). It installs `Kept'` (claims `keeps le100 by bounded` where `bounded` is `ok` on every
  occasion); `set 101` is admitted; the object holds `total = 101`; `inv` is false of it. Row LK2 must flip to
  ADMITTED under the plant, as L4 flips under `skip-judge`.
* Refuted by `unjudgedKernel` (B3's floor): the claim checks at install and no law runs; `set 101` admits.
  B4 is strictly stronger than "install checked the claim": it needs B3's clause (ii) underneath.
* Inhabited by LK1: `Kept` (claims `keeps le100 by bounded`, `bounded` in certifying shape) installs; an
  object is born at 0; `set 50` admits and the cell reads 50 ≤ 100; `set 101` is refused `lawDenied bounded:
  over 100`, and the cell still reads 50.

**Where it sits in §10 of TOPLEVEL-SPEC.** Load-bearing, as a clause of INTEGRITY beside B1–B3; it is the first
clause of the spec that is about a sentence a MEMBER WROTE, checked by the kernel, rather than about a sentence
the kernel's authors wrote. That is the whole point: with B4, `Spec/` can state "the Escrow pays exactly once"
as "the deployed Escrow's package carries claims C1, C2 (checked by `install_claims`), and C1 ∧ C2 ⇒ exactly
once (a Lean lemma over `Keeps`)" instead of as a 20-witness existential over the escrow's term.

## 5. The next steps this design gives, in order

1. **`pays m c (amount, to)`** — the second claim class, over methods: call slot `c` of method `m` is, on every
   path that returns, `some (transfer {amount = state.amount, dst = of {owner = state.to, asset = state.A}, src =
   of {owner = req.self, …}})`, by the same dominator walk over the `calls` row literal of `resultT` (READ
   `Package.lean` `resultT`, `callsT`). With `keeps` on the Escrow's phase field this states `world/escrow/
   Escrow.ob`'s doc as two kernel-checked claims; the hand-written Escrow becomes the first package whose
   summary the World vouches for. The soundness theorem is the `calls` half of `runMeasuredWith_ok`
   (`Lang/Proofs/Rel.lean:1172`) composed with `callsOf`'s reading. A week.
2. **The renaming lemma for `BigStep`** (§3.4(i)), so `Std.bounded`, `Std.quorum`'s `reset`, and any inline
   test can be matched at depth; then every `Std` law gets its `keeps` for free and the escrow's `escrowFairT`
   becomes a claim `fair` on `take`/`fuse`. One to two weeks; it is also the first lemma the WP logic of
   LANGPROOFS §3(2) needs.
3. **Claims through layers** (`claimRequired`): a layer inherits its super's claims on inherited laws and
   is refused when it claims what the super does not; needs the lift extended to `extend (ref 0)` bodies
   (the same extension B3 wants, TOPLEVEL-SPEC §11.6). A week.
4. **Laws that see the calls**: `lawTy S` gains the calls row, so a monitor can refuse a wrong payment per step
   (the per-step gap of §1); then `pays` has a dynamic twin and the two are reconciled by one theorem. This is
   KERNEL's `judge` signature (cross-layer) and a `lang!`. Two weeks.
5. **`describe` prints claims**: `nd read OBJ ?` lists the package's claims first, after the doc
   (PROTOCOL's `packageLines`), so a member sees the kernel-checked summary where it sees the unchecked one.
6. **Certificate classes** (§6): a claim whose proof is a small object the checker re-runs — the first worth
   having is a TICK BOUND for a law (`costs L ≤ k`), because a law that exhausts its budget wedges its object
   for ever (every step refused `exhausted`) and no row today refutes that class of package.

## 6. What this fragment cannot say, and what each would cost

| claim | why the dominator walk cannot decide it | proof object that would | price |
|---|---|---|---|
| "`I(old) ∧ law admits ⇒ I(new)`" where `I` is not tested literally (an invariant implied by arithmetic, e.g. `count ≤ limit` from `count = old.count + inc ∧ …`) | needs reasoning, not shape | a WP/Hoare derivation over `BigStep` (LANGPROOFS §3(2)), shipped as a term of a `Deriv` type and checked by a Lean `Deriv.check` with one soundness theorem: foundational PCC in Appel's sense, with Lean as the meta-logic | the logic: 1–2 months; the checker: a week once the logic exists; package size grows by the derivation |
| a tick bound on a law or method | cost is semantic (lazy fields re-evaluate per `get`; a `fix`-free typed term is not linearly bounded) | a per-node cost certificate the checker sums (Hofmann/Hoffmann's amortised style, or Nomos's potential) | a month; it is the class whose absence lets a package wedge its own object |
| non-interference ("the law's verdict does not depend on `req.agent`") | a two-run property | a syntactic non-use check IS the proof (`usesField`), and its theorem is a two-run simulation | the simulation is the renaming lemma's sibling; two weeks |
| anything about a counterparty's package | the checker sees one package | claims are per package; composition is a Lean lemma over two packages' claims, never a kernel check | free once both carry claims |
| liveness | measured, never proved (charter) | — | — |

The honest boundary: nano's kernel can decide claims whose proofs are the term's shape; everything beyond needs
a proof OBJECT, and the first one worth building is the WP derivation, because LANGPROOFS already wants the
logic for the generator proofs and the escrow's `fair` and `pays` would be its first two clients.

## 7. The one way this is wrong, said first, and the three after it

**The brief's: reflection costs too many ticks.** True, and avoided rather than solved (§2): no nano term checks
a proof, the kernel does, unmetered, as it types. If a future claim class needs the MACHINE to evaluate
something at install (e.g. `I` on a seed), it runs under `lawTicks` like a law and refuses `exhausted` by name.

**The real one: a claim language is a second place to be wrong, and the doc is still there.** The claim's
MEANING (`Keeps`, `Std.Admits`'s shape) is a Lean definition a reader must read; a reader who trusts the
claim's NAME (`keeps`) without reading `Keeps` is back to trusting a docstring, one level up. Two mitigations,
one of them structural: the meaning is a single short definition per claim class, not a theorem per package
(the field's lesson: trust the spec, not the catalogue), and the plant `skip-claims` keeps a row that must flip.
The doc stays, as prose; what changes is that a reader now has a sentence the kernel refused to let be false.

**Incompleteness as a tax on authors.** A law not in certifying shape cannot claim. The `Std` generators pay
it once (§3.4); a hand author pays it per law, and the refusal `claimShape` names the law but not the leaf.
The next landing makes the checker name the path to the first unguarded `ok` (as `TypeErr` names the failed
rule and path), which is cheap and what law 7 asks.

**It is not a proof system, and the charter says so.** CHARTER scope item 1 rules out circuits, STARKs and
accumulators; this design builds none and would not under any of §6's classes either — a `Deriv` checker is a
type checker's cousin, deterministic, re-executed by every member like everything else. The confusion to avoid
in briefs: "add a proof" here means "add a claim and write the law in shape", never "add a prover".

## 8. The prototype (what lands, in two landings)

**L1 (`lang:`, fast judge; no byte moves):** `Lang/Claim.lean` (`Claim`, `Term.guardedBy`), `Lang/Proofs/
Claim.lean` (`Keeps`, `guardedBy_sound`, `keeps_step`, `chain_keeps`), `Std.keeps` in `Lang/Std.lean` with its
`NoRef`/`IsLaw` lemmas, and journey rows that run the checker as a function (a certifying law checks; a law that
leaks an `ok` under `case` does not; a `var`-returning law is `claimShape`).

**L2 (`lang!:`, full judge; the flag day):** `Package.claims`, the ninth wire child and version 6, the text
section and surface declaration, `checkClaims` in `checkWith` with its four refusals, `install_claims`,
`Kernel/Proofs/Logic/Claims.lean` (`object_history_keeps`, cross-layer), journey `Lang/Journey/Claims.lean`
rows LK0 (text reads and prints back with a `(claims …)` section), LK1 (true claim: installed; the state kept),
LK2 (false claim: refused `claimUnproved`), LK3 (no proof: a law returning a verdict it read from state,
refused `claimShape`), LK4 (a claim naming a method, refused `claimNotLaw`), plant `skip-claims` (LK2 flips),
re-drawn `gates/codec-vectors.tsv`, LANG-83 in `decisions/lang.md`. What re-emits: every package re-ids (the
version byte); shipped core TEXTS are unchanged (the section is optional); a re-genesis is owed for any World
holding package cells. What refuses to load: package bytes at version 5 (`lang/package-version/6`, by name).

Status at the time of writing is in `redregg/work/codex/FABLE-PCC.report.md`. L1 built green on hbox (guardedBy_sound,
keeps_step, chain_keeps proved; LK1–LK4 green; plant P1 red by name) and was sent to land as LANG-92. L2 shares its
wire bump with FABLE-TYPES's LANG-89 (version 6, an effects child): whoever lands second takes version 7 (ROOT, 05:10Z).

## BUILT (FABLE-PCC-2, real 2026-10-26): L2, the carried claim — LANG-93 + KERNEL-73

Landed as `<<HASH>>` on origin/main (full judge). What §8's L2 said, with three corrections the code forced:

1. **The check lives in `checkFields`, not beside `checkE` in `checkWith`.** `checkWith` is only the CLOSED admission; a package with holes is admitted by `checkContextual`, which runs `checkFields` and never `checkWith` (READ `Lang/LiveHoles.lean`, `Lang/Program.lean` `admitContextual`). Putting `checkClaims` last in `checkFields` makes every admission check claims — install's, a run's load of the closure, a hole package's — and makes `install_claims` a corollary of the loader's invariant (`Inv`: every package of a loaded closure passed `checkFields`), so it holds of every package in a closure, not only the one being installed.
2. **The claim's literal shapes are exact.** `checkClaim` demands the invariant literal `lam S ib` and the law literal `lam S (lam S (lam reqTy b))` at the package's own `S` (what `checkE` would force anyway), so `install_claims` yields `keeps_step`'s premise with no typing argument; a law written through a helper lambda is `claimShape`, an unguarded `ok` is `claimUnproved` (journey LK7, LK6). The conditions are decidable Props and a `match` on the walk, because `split` degenerates on a Bool `if` in a hypothesis.
3. **The start state is a premise of the lift.** `object_history_keeps` (KERNEL-73) takes `Keeps [] ib o` for the live object the history starts from: `Kernel/Proofs/WriteNext.lean` has `write_next_slots`/`law_next_slots` and no `create` twin, so the birth's judgment (the seed, judged as `birth`, which the shape does not exempt) is discharged by the row (LK5b), not by a theorem. A `create_next_slots` lemma closes it; it is the first item of the next list.

Measured (hbox `wt/fable-pcc` on c82f171): whole tree GREEN; `lang-journey` GREEN with LK0 (the text round trip, the section optional, the claim in the id), LK0b (the surface declaration lowers; `claimNotInvariant decider`), LK5–LK5d (the inhabitant), LK6 `claimUnproved bounded`, LK7 `claimShape bounded`, LK8 `claimNotLaw set`, LK8b `claimNotInvariant owner`, LK9 `lang/package-version/6`; PLANT `skip-claims` (`Mode.skipClaims`, §4's `uncheckedInstallKernel`): LK6/LK7/LK8/LK8b ADMITTED, LK5d still refused by the law. Vectors: 55 `lang/package/6` rows (54 moved, one new claiming package), 2 version rows, nothing else moves. `world/doc/Section` root re-emitted (helper ids moved); the shipped core texts unchanged. B4 (§4) is now TRUE for the `keeps` fragment under B3's premises plus the start state.

Wire: version 6 and the claims child at `node 4`, by ROOT's rule (the version on origin/main when the judge started, + 1; CTX's LANG-84 and TYPES's LANG-89 were in flight at 6 as well — landing order decided; see FABLE-PCC.report.md for the final numbers).

Next (§5, re-ordered by what this landing exposed): (0) `create_next_slots` and the birth's `Keeps` (closes the premise of KERNEL-73); (1) `claimShape` names the path to the first unguarded `ok`; (2) `pays m` over the Escrow's calls row; (3) the `BigStep` renaming lemma (unlocks `Std.bounded`'s inline test, LK4); (4) claims through layers (`claimRequired`); (5) laws that see the calls (with TYPES: their graded effects are the type-side twin); (6) `describe` prints claims.
