# DESIGN-META — generators as nano objects: a World that installs what its own programs emit (real 2026-10-26)

Author: FABLE-META (a Fable), axis 1 of FRONTIER-AXES-20261026. Read first: VERDICT-20261024 §2–3,
HOLISTIC-LANG §1.2/§3.2(iii)/§4, TOPLEVEL-SPEC §3.3/§10.3/§11, DESIGN-CTX §0–1, DESIGN-TRUST §0; then the
code at nano `origin/main ad90a47`: `Lang/Term.lean`, `Lang/Eval.lean`, `Lang/Package.lean`,
`Lang/Program.lean`, `Lang/Call.lean`, `Lang/Std.lean`, `Lang/StdHead.lean`, `Lang/StdActivity.lean`,
`Lang/HoleSyntax.lean`, `Lang/Bell.lean`, `Lang/Wire.lean`, `Codec/Tree.lean`,
`Kernel/Receive/{Call,Derive}.lean`, `Kernel/Proofs/{Tree,Ledger,InvokeTree}.lean`, `Protocol/Foreign.lean`,
`Lang/Journey/Head.lean`. Tags: READ (a path), MEASURED (a command I ran), INFERRED (my reasoning; attack
these first). Non-vacuity lives at the top-level clause (§4) and nowhere else.

## 0. The answer in one page

**A generator is an ordinary nano package whose method returns the call `install BYTES`.** Nothing else is
new. The kernel already has the receiver (`Kernel.Receive.install`, READ `Derive.lean:107-111`): it ignores
who the actor is beyond the birth index, runs `X.program.checkInstall` on the bytes, and bears a ROM cell whose
id is the content digest (`romIdOf`, READ `World.lean:712`; KERNEL-3). The one thing that stops an object
from installing today is `Body.callable` (READ `Call.lean:516-518`), the kernel's assertion where a method's
calls enter, which lists five kinds and not `install`. Widening it by one constructor, and giving `Lang.callTy`
the matching arm `install : rec {pkg : bytes}`, makes **"install a generated package" a nested call of a
Turn**: the signer invokes the generator object, the generator's method computes the package bytes and
returns `install b`, the tree derives it AS THE OBJECT (`effect_as_signed`, READ `Kernel/Proofs/Tree.lean:68-80`)
through the same `dispatch` a signed `install` goes through, and the package cell `romIdOf b` is born in that
Turn. Every follower re-derives it. No new cell kind, no new slot, no new right, no new receiver.

**The receipt of a generation is the Turn.** A generated package is a package cell `P` born in a Turn `t`
whose signed call was `invoke G generate a`; `t` is in the journal, a member holds its receipt
(`Protocol.Receipt`), and "P is `F a`" is the composition of two statements: the kernel's (`P`'s bytes were
returned by the method run the tree dispatched, and passed `checkInstall` at the signer's pinned view —
`tree_package_checked`, §4) and the generator's meaning theorem (that run returns `[install (encodePackage (F a))]`
— `generate_run_sound`, §4). There is no "receipt object"; the journal row and the ROM id are the receipt,
exactly as a Turn is the receipt of a transfer. Because the id is content-addressed, two generators that
emit the same bytes install ONE cell, and a generation repeated installs nothing new (the second birth of
an existing id is `idTaken`): generation is idempotent up to refusal, which is Unison's property.

**Hygiene is free, and the de Bruijn "embarrassment" is why.** A generated package's body is a CLOSED de
Bruijn term whose `ref i` indices name its OWN `imports`; a nano generator holds no names, so there is
nothing for a generated term to capture. The only way the generator's data enters the generated code is as
a LITERAL (`nat`, `bytes`, `digest`), and a digest literal is re-checked against the World at install
(`checkLits`, LANG-38). MetaML needs a type of code to get this; Template Haskell gets it by renaming;
Racket by scope sets; nano gets it because its object language was never named in the first place. The
reader's complaint (HOLISTIC-LANG §3.2(iii)) is about the AUTHORING of the Lean generators, where a human
counts binders, and it stands; it is not about the wire the generators emit, and it is the wire a nano
generator writes.

**The kernel checks a generated package exactly as it checks an installed one.** `checkInstall` is the
stage-2 type checker of this staging system: the generator's output is checked AFTER it is spliced into the
World, against the World's own `digestOf` and the imports' interfaces, through the signer's pins. That is
Template Haskell's choice (untyped splices, checked after) rather than MetaML's (a type of code whose
well-typedness is static), and it is the right one here because the install check already exists, is
total, and is the thing every follower runs. A generator that emits an ill-typed package is refused by
name at the nested install (`program illTyped …`), and the Turn fails whole: a generator cannot half-install.

**Laws are derived from specifications in Lean, and the receipt says which.** The honest boundary (axis 2
is the proof system inside the kernel; this axis is not it): a generated package's law MEANS what the
generator's meaning theorem says it means, for the arguments the receipt names. Today the Std generators
carry those theorems (`Lang.Proofs.Std*`); a generator object carries them unchanged, since it emits the
same bytes. What changes is WHERE the instantiation happens: in the World, under a Turn, by a member who
need not hold Lean.

**The Std library as installed objects.** `Std.headPackage` becomes `Std.headGenerator`, a nano package whose
`generate` emits `Std.headPackage`'s bytes; the sponsor installs the generator and creates one object of it at
genesis time (a `world/std/*.ob` fixture, as the Bell is), and anyone holding `[invoke generate]` installs
`Std.head` by a Turn. The journey proves byte identity by CELL-ID EQUALITY: the package the generator bore
has id `Protocol.Foreign.headPackageId` (READ `Protocol/Foreign.lean:29`), the deployed constant the receipt
check compares against. That is the strongest "byte for byte" there is: one digest.

**The price, in the spec's terms (§5).** ONE HISTORY, CONSENT, DURABILITY, THE BELL: unchanged. INTEGRITY
B1 (authority): unchanged — a package cell has no owner and never CHANGES; B1 is about changes. B3 (law):
unchanged — ROM. The generator-spec tier (TOPLEVEL-SPEC §10.3) gains one clause, PROVENANCE OF CODE (§4),
whose floor is the kernel whose nested `install` skips the check. Kernel theorems gaining a premise: **0**.
Proofs gaining a CASE: three (`tree_zeroBorn`, `bodyOf_callData`/`callData_*`, `bodyOf_live_fixed`), each by
a new arm. Wire: no byte moves for rung 1 (`callOf kinds` filters the arms by name, so no deployed method
type changes). Rung 2 (§3) is one package-wire flag day.

**The one way it is wrong (§6).** It stages at the BYTE level. A generator builds a package as a byte string
and the kernel re-parses it; nothing in the generator's TYPE says it emits a package, let alone which. That
is exactly the "fixed-arity rows as lists" workaround (HOLISTIC-LANG §1.4) raised to the meta level, and it is
chosen on purpose: a `code` type with constructors needs a bounded sequence type and a type of types, which
nano does not have, and a bytes-level stage costs no new type and one flag day. The design says so and names
the type that replaces it when the language gets lists (§6.2). Its second wrongness: a nested call returns
nothing, so a generator cannot `create` an object of the package it just bore in the same Turn (it cannot
hash the bytes to learn the id); "generate and instantiate" is two Turns, or §6.3's `createOf` arm.

---

## 1. What a generator IS, as a nano object

### 1.1 The field's generators, and which one nano is

| lineage | stage separation | hygiene | where the output is checked | nano |
|---|---|---|---|---|
| Lisp `defmacro` / quasiquote | expansion time vs run time, same process | none (capture by name) | after expansion, by `eval` | the surface (`.ob`) is already a Lisp; a generator is a macro whose expansion is a Turn |
| MetaML (Taha–Sheard 1997) | `<_>`/`~`/`run`, levels in the type | by construction: a type `⟨A⟩` of closed code | STATICALLY: `⟨A⟩` is well typed at stage 1 | not this: nano has no type of code (§6.2) |
| Template Haskell (Sheard–Peyton Jones 2002) | splices run at compile time | by renaming (fresh names) | AFTER splicing, by the ordinary type checker | **this**: untyped splice, checked after, by `checkInstall` |
| Racket's macro tower (Flatt 2002) | phases: phase-1 code runs to produce phase-0 code; separate instantiations | scope sets | per phase, by the expander | the GENERATION Turn is phase 1, the generated package's runs are phase 0; the phase boundary is the receipt; each phase is its own Turn, so instantiations are separate by construction |
| Lean's elaborator | `MetaM` elaborates syntax to kernel terms; the KERNEL re-checks every term | de Bruijn in the kernel, names in the elaborator | the kernel re-checks what the elaborator produced | **this**, with the roles: the `.ob` reader (`Lang.Surface`, outside the TCB) is the elaborator; `checkInstall` is the kernel; a nano generator is an elaborator written in the object language |
| Unison (content-addressed code) | — | — | hash = identity | `romIdOf`: a generated package IS its content digest; generation is idempotent |
| certified program generation (the Std generators today) | Lean function emits a closed term; its meaning is a Lean theorem | the author counts binders | at generation (`checkWith`) AND at install | the Lean generator stays as the SPECIFICATION of the nano generator; `generate_run_sound` ties them |

### 1.2 The object

A generator is a package `G` with:
* state: any data record (`rec {}` for the Std ones: a generator keeps nothing);
* one or more methods whose calls row holds a slot of call type `callOf ["install"]` — a sum with the one arm
  `install : rec {pkg : bytes}` (§2.1) — and whose body computes `pkg` from its argument and state;
* laws as any package has them (a generator may be quorum-gated: `Std.quorum` over a `generated : nat`
  counter gives "a package is installed only when k of n approve", with no new machinery).

An invoke of `G.generate a` is a Turn whose tree is `[install b]` under the invoke: the Draft's `creates`
holds `(romIdOf b, packageCell b)`; nothing else moves (the generator's own state write, if any).

### 1.3 Three grains of generator, and which is built

**Rung 0 — the constant generator** (`Std.generatorOf b`, BUILT tonight, §7). The method returns `install`
of a byte literal `b`. It is a generator the way a constant is a function: every mechanism is exercised
(the callable arm, the nested install, the check at the nested actor, the ROM id, the receipt), and the
output is byte-identical to the Lean function's by construction, but no parameter varies. `Std.headGenerator`
is the first installed generator; it IS `Std.headPackage` as an object, byte for byte, and the journey's
GN rows check it as one digest. The reader may call this a floor inhabitant; it is also the only honest
first rung, because the next one needs the language to write bytes it cannot write today (§3).

**Rung 1 — the template generator** (needs §3's primitives; the next landing). The method splices
PARAMETERS into fixed positions of the package tree: a doc, a refusal name, an allowlist of member ids, a
limit, a patience, a cap. Every Std generator with scalar parameters (`bounded`, `windowed`, `allowlist`,
`activity`'s limits and patience, `offer`'s bounds) is a template generator. The method's text is a `cat`
expression over literal framing bytes and encoded parameters; the Lean generator it mirrors is its
specification, and `generate_run_sound` for it says `run = [install (encodePackage (F a))]` for every `a` in
the generator's refusal-free domain.

**Rung 2 — the structural generator** (needs lists; §6.2). The method chooses the SHAPE of the package from
its argument: how many plans an activity has, how many edges a machine has, how many members a quorum
masks. Today each of those is a Lean `List` fold emitting a chain whose length is the list's; without a
bounded sequence type in nano, a method cannot fold. The honest shape is `Ty.seq n T` with a canonical
codec and a fold primitive; that is axis 7's language change, and this design does not pretend to it.
Until then, structural generators stay Lean functions, and a WORLD gets their outputs through rung 0
(install the emitted package) — which is what the Std library is today, under a receipt.

### 1.4 Why a generator is a package and not a method of the kernel, a term, or a new cell kind

* Not a kernel act ("the kernel generates"): the kernel has one language interface, `Receive.Program`, and
  generating is running a program; the one new line is in the kernel's list of what a program may ask for.
* Not a term that "evaluates to a package the kernel then installs": a term's value is `Val`, which is not a
  package; the kernel takes bytes (`install (pkg : ByteArray)`), so the term's job is to produce the bytes,
  and the call carries them. Making `Package` a `Val` would put the package wire inside the machine's values
  (a twin of the codec, law 1).
* Not a new cell kind ("generator cells"): a generator has nothing a package lacks. The reader's own
  minted lesson applies: every new kind is a premise on every theorem that quantifies over kinds.

---

## 2. What the kernel must check, and what it already does

### 2.1 The change, exactly

**KERNEL (`Kernel/Receive/Call.lean`).** `Body.callable` admits `.install`:
```lean
def Body.callable : Body D → Bool
  | .invoke .. | .transfer .. | .account .. | .credit .. | .grant .. | .install .. => true
  | _ => false
```
and `notCallable`'s docstring names six kinds. `Body.callable` is the kernel's ASSERTION where calls enter
(law 4); widening it is a weakening of a check, which deserves the pause the charter asks for. The argument
that it is sound: `install` takes no authority from its actor — a signed `install` by ANY member is admitted
(READ `Derive.lean:107-111`: no `ownerAuthority`, no grant, no owner slot; the cell is ROM, content-addressed,
owned by nobody), so an object installing is an act every member could already perform, with the same
check, and the tree derives it with the object as actor only for the birth index. What an object still may
NOT do: `create` (an object born under an invoke would be owned by the signer, through the object's choice:
a confused deputy), `enroll`, `rotate`, `write`/`law` (KERNEL-28: effects are derived as signed, and those
spend authority), `revoke`, `issue`. The line between the two lists is "spends nobody's authority and
changes no cell": `install` is the only receiver on that side, and `account` is its value-side cousin
(already callable, for the same reason).

**LANG (`Lang/Package.lean`, `Lang/Call.lean`).** The arm, in canonical label order:
```lean
def installArm : Label × Ty := ("install", .record [("pkg", .bytes)])
def callArms : Option Ty → List (Label × Ty)
  | some A => [accountArm, creditArm, grantArm, installArm, ("invoke", invokeArm A), transferArm]
  | none => [accountArm, creditArm, grantArm, installArm, transferArm]
```
`callData (.install pkg) = some (.inj "install" (.record [("pkg", .bytes pkg)]))`; `bodyOf` reads it back;
`callFits (.install pkg) = pkg.size ≤ Bounds.bytesMax` (a package the language can hold as a value: 128 KiB;
MEASURED: `Std.offerEscrow`, the largest, is 42,216 bytes, LANG-80). `callOf kinds` and `invokeOf A kinds`
filter by name, so no existing method type gains an arm: no deployed package's bytes move, no VK, no
re-genesis (MEASURED: `grep -rho "(calls [^)]*)" world/` names only `transfer`).

**SURFACE.** `(calls (install))` works unchanged: the reader takes kind atoms as labels and `callOf` keeps
the ones it knows (READ `Surface.lean:607-623`, `:670-673`); an unknown kind is an empty sum, refused
`badMethod` at install as before.

### 2.2 What the kernel checks of a generated package (nothing new)

At the nested `install b` (READ `Derive.lean:107-111`, `:340`):
1. `X.program.checkInstall look b` — the SAME function as for a signed install, with the SIGNER's pinned
   view `look`: `decodePackage` (canonical bytes or a named codec refusal), the import closure loaded by the
   one admission (LANG-78), every package of the closure re-checked at its own holes, the package's body
   checked at its interface, the fields, the bounds, the id literals against the World (`checkLits`). So:
   **well-typed, within bounds, and every id it names is a digest of the World as the signer observed it.**
2. `bornAt X c a.base [{kind := kindPackage, discipline := .rom, slots := [(0, b)]}]` — the cell is born at
   the tree's birth index, id `romIdOf`; `World.admit` refuses a duplicate id `idTaken`.
3. The tree's pool: the generator's run is charged like any method; the install itself costs no ticks
   (a receiver, not a program). The tree depth bound (`callDepthMax`) and `callsMax` apply.

What the kernel does NOT check, and must not pretend to: that the generated package is the one the
generator's AUTHOR meant. That is `generate_run_sound` (§4), a theorem about the generator package, which the
receipt lets a reader INSTANTIATE: the receipt names `G` (by id) and `a` (the argument bytes), so "what did
this Turn install" is answered by the theorem at `(G, a)`, not by trusting the generator object.

### 2.3 Hygiene, stated as what cannot happen

A generated package's `body` is parsed from bytes by `termOf`; a `.var i` in it is an index into ITS OWN
binders; a `.ref i` is an index into ITS OWN `imports` (relocated at load to the closure's indices, LANG-16).
Neither can name a binder or a closure package of the generator's run, because those are not in the bytes:
the generator's environment is `[req, args, state, rows]` as VALUES, and a value enters bytes only through
the term's literal nodes (`nat`, `bool`, `bytes`, `digest`). The capture that hygienic macro systems prevent
("the generated code refers to the installer's `x`") is unstatable here. What a generator CAN do that a
reader should know: bake the SIGNER's id into a law (`req.agent` → a `digest` literal, rung 1), which is
authority by naming, as `Std.allowlist` is today — and `checkLits` makes it a digest of the World the
installer pinned, so a generator cannot smuggle an id the installer did not observe.

---

## 3. Rung 1: parameters (the next landing; one package-wire flag day)

### 3.1 The obstacle, measured

The package wire is one `Codec.Tree`: `u8 tag ‖ varint |payload| ‖ payload ‖ varint |children| ‖ child*`
(READ `Codec/Tree.lean:1-14`, CODEC-13), under a version byte. It is CONCATENATIVE: the bytes of a node are
a function of the bytes of its children by `++`. So a nano method with `cat` can build ANY package tree
from byte fragments — except that the language cannot write the three numbers the framing needs: a
payload's length (varint), a child count (varint), and the payloads of `nat`/`var`/`ref` literals
(`u64Bytes`, `u32Bytes`, READ `Lang/Wire.lean:156-173`). The core's byte primitives are `beq`, `cat`, `lenLe`
(READ `Term.lean:15-25`); there is no `nat → bytes`.

### 3.2 The primitives (INFERRED; the smallest set that makes every tree writable)

Three binary primitives, each O(1) work (law 4's cost model, LANG-64 charges bytes walked):
* `len : bytes → nat` — the size (`lenLe` is its Boolean; `len` is what the framing needs). Walks nothing.
* `varint : nat → bytes → bytes` — `putVarint n ++ b`: the LEB128 of `n` (≤ 10 bytes) before `b`. Walks `|b|`
  (a copy): charged as `cat` is.
* `be : nat → nat → bytes` — `n` as a `w`-byte big-endian string (`w ∈ {4, 8}`; any other `w` faults
  `stuck`-free by name, `badWidth`): the `u32Bytes`/`u64Bytes` of literal payloads. Walks nothing.

With them `node tag p kids = cat (bytes [tag]) (cat (varint (len p) p) (varint k kids))` where `k` is the
child count the generator knows by construction, and `Lang.Quote.packageTerm : Package → Term` (Lean, NEW)
emits a nano term that computes `encodePackage p` — a staging compiler whose theorem is
`eval (packageTerm p) = .bytes (encodePackage p)` for every `p` within bounds. A template generator is
`packageTerm` with some literals replaced by `be 8 (get arg "limit")`, `get arg "doc"` under a `lenLe`
bound, or `req.agent`'s digest bytes — and here is the second obstacle: a `digest` value has no bytes
(LANG-38 made ids a type that is never MADE from bytes; the reverse direction, `digest → bytes`, was never
needed). A fourth primitive `idBytes : digest → bytes` is sound (it leaks nothing: every digest in a run
came from the World) and lets a generator name a member in a law it emits.

### 3.3 The flag day

A primitive is a term wire tag (`primCode`, READ `Wire.lean:164`), so a new primitive is a NEW TAG: the
package wire version moves 5 → 6, the refine label `lang/package/5` → `6` (`packageCodec_label` fails the
build otherwise, LANG-60), `gates/codec-vectors.tsv` gains the refused-boundary row that now reads, and
EVERY installed package's bytes change by their version byte: every `.ob` fixture re-emits (same content,
new version byte, new `romIdOf`), `Protocol.Foreign.headPackageId` moves, the Bell's shipped core re-emits
(LB0/LBw read it), the devnet re-genesises. The old version byte REFUSES TO LOAD (`lang/package-version/5`
row LV). That is a `lang!` landing with the full judge; it is a rebuild, not a migration, and this document
is where it is findable. Rust: the primitive table is Lean's (the client decodes no terms; MEASURED:
`grep lenLe client/` finds nothing), so nothing in Rust moves.

Why not land it tonight: the rung-0 landing is where the MECHANISM is judged (the callable arm, the receipt
theorems, the journey); putting a wire flag day under it would make the judge's one question ("may an
object install?") two. Rung 1 is the next card, designed here, priced here, and it is small.

---

## 4. The statements (what is proved, and the clause the spec gains)

### 4.1 Kernel: what an object's call may bear, extended

`tree_package_checked` (NEW, `Kernel/Proofs/Generated.lean`, modelled on `tree_zeroBorn`, READ
`Kernel/Proofs/Ledger.lean:513-553`): every package cell a nested call's Draft creates holds bytes that
passed `X.program.checkInstall` at the signer's pinned view:
```lean
theorem tree_package_checked {X : Ctx D} {look : Pinned D} {rv : RowView D} {c : Call D} :
    ∀ n wk a b r, tree X look rv c n wk a b = .ok r →
      ∀ p ∈ r.1.creates, p.2.kind = kindPackage →
        ∃ bytes, p.2 = { kind := kindPackage, discipline := .rom, slots := [(0, bytes)] } ∧
          X.program.checkInstall look bytes = .ok ()
```
Its floor: the kernel in which the nested `install` arm is `stepped wk (.ok ⟨bornAt …⟩)` without the check
(the trivial generator kernel: "an object may install anything"). Inhabited by GN0.

`tree_zeroBorn` keeps its statement; its proof gains the `install` case (a package cell is not a value cell:
`ofCell_not_value`).

### 4.2 Lang: the generator means what the Lean generator emits

`generate_run_sound` (NEW, `Lang/Proofs/StdGen.lean`, modelled on `take_run_sound`): for the package
`Std.generatorOf b doc` read at `pkg`, every admitted run of method 0 returns the calls `[.install b]`, no
row acts, and the empty state:
```lean
theorem generate_run_sound (bytesOf digestOf) {rc} {look rv pkg state args r budget s calls rows used} {b doc}
    (hid : digestOf (bytesOf pkg) = some pkg)
    (hp : readPackage look pkg = .ok (Std.generatorOf b doc))
    (h : (Lang.program bytesOf digestOf rc).run look rv pkg state 0 args r budget = .ok (s, calls, rows, used)) :
    calls = [.install b] ∧ rows = [] ∧ s = []
```
and `headGenerator_emits : Std.headGenerator = Std.generatorOf Protocol.Foreign.headPackageBytes …` is
definitional, so the composition at the Sim's parameters is the journey's cell-id equality.

### 4.3 The clause the generator-spec tier gains (TOPLEVEL-SPEC §10.3)

**PROVENANCE OF CODE.** Every package cell in an audited log was born in a Turn whose signed call was an
`install` of its bytes, or an `invoke` whose dispatched tree returned `install` of its bytes from a method
run the laws judged; in both cases the bytes passed `checkInstall` on the signer's pinned view; and for a
generator with a meaning theorem, the bytes are the theorem's at the receipt's arguments. Sentence for the
reader of a receipt: *"this package is what generator G computes for a, and the kernel checked it as it
checks anything a member installs."* FLOOR: the kernel whose nested install skips the check
(`tree_package_checked`'s tooth); the Lang program whose `callsOf` reads an `install` datum as some other
kind (the `bodyOf_callData` round trip's tooth). INHABITED: GN0–GN2.

---

## 5. The price, in the spec's terms

| claim | statement change | premise added | proof case added |
|---|---|---|---|
| ONE HISTORY (§2) | none | 0 | 0 |
| INTEGRITY B1 authority (§3.1) | none: `Authorized … package never` is about CHANGES; a birth is not a change | 0 | 0 |
| INTEGRITY B2 value | none | 0 | `tree_zeroBorn`: the install arm (a ROM cell is not a value cell) |
| INTEGRITY B3 law | none: ROM, `audit_package_fixed` | 0 | 0 |
| CONSENT, DURABILITY, THE BELL | none | 0 | 0 |
| generator-spec tier | + PROVENANCE OF CODE (§4.3) | — | — |
| Lang call round trip (`bodyOf_callData`, `callData_isSome`, `callData_conforms`, `bodyOf_live_fixed`, `find_some`) | none | 0 | one arm each |

Rung 1's price is the flag day of §3.3 and nothing in the claims.

---

## 6. The one way it is wrong, and two smaller ones

### 6.1 Bytes are not a type of code

A generator's method type says `calls : rec {c0 : opt (sum {install : rec {pkg : bytes}})}`. It does not say
it emits a package, which package, or at which interface; the kernel learns that by parsing. MetaML's
`⟨A⟩` says it; so would `Ty.pkg` in nano. The consequence is real: a generator that composes two
generators' outputs (install `mix l u`) must do it on bytes, and nothing in the language relates the bytes
of `l`, `u` and the mix. This is the "list as fixed-arity row" workaround at the meta level, chosen because
the alternative is §6.2, and the design names the moment to replace it: when nano gets a bounded sequence
type, `code` is a one-week change over it.

### 6.2 What replaces it: `code` over a bounded sequence type (axis 7)

`Ty.seq n T` (a bounded list with a canonical codec) and `Ty.code` (an opaque type whose values are closed
`Term`s, encoded by `termTree`, with constructor primitives `qlam : ty → code → code`, `qapp`, `qvar : nat
→ code`, `qrec : seq n (rec {l : bytes, t : code}) → code`, …) make a generator a function to `code`, the
install arm `install : rec {pkg : pkgTy}`, and `checkInstall` the same check at a typed input. Hygiene stays
free (closed de Bruijn). The meta-typing (`code` well typed at a type) stays with the kernel's install check,
not with a static stage-1 type: that is the Template Haskell choice again, kept on purpose.

### 6.3 A generator cannot instantiate what it generated, in one Turn

A nested call returns nothing (fixed-arity calls; LANG-23), and a method cannot hash, so after `install b`
the generator does not know `romIdOf b` and cannot `create (some id) …`. Two Turns: generate, then create.
If one Turn is wanted, the honest arm is `createOf : rec {pkg : bytes, laws, state}` — "create an object of
the package these bytes install", derived by the kernel as `install` then `create` with the id it computed —
and its authority question is the one `create` has (the object would be owned by the SIGNER, through the
object's choice: a confused deputy, KERNEL-28). Not in this design; named so it is not forgotten.

---

## 7. What is built tonight (landing 1, `lang:` with KERNEL-75 cross-layer), and the next step

**LANDED as nano `c82f171` (2026-10-26; fast judge GREEN; lang-journey GREEN with GN0–GN5).** `headGenerator_wire` (a
`native_decide` that the generator has bytes) was dropped: nano's axiom census admits no `native_decide`, and GN0's
row is the fact. Files (all under nano, worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-meta`):
* `Kernel/Receive/Call.lean`: `Body.callable` + the `notCallable` docstring.
* `Kernel/Proofs/Ledger.lean`: the install case of `tree_zeroBorn`.
* `Kernel/Proofs/Generated.lean` (NEW): `tree_package_checked`.
* `Lang/Package.lean`: `installArm`, `callArms`. `Lang/Call.lean`: `callData`, `bodyOf`, `callFits` arms.
* `Lang/Proofs/Call.lean`, `CallLive.lean`, `CallTeeth.lean`: the arm in each round-trip and liveness proof;
  a tooth that an `install` datum reads as `.install`.
* `Lang/StdGen.lean` (NEW): `installSlot`, `generateMethod`, `generatorOf`, `headGenerator`.
* `Lang/Proofs/StdGen.lean` (NEW): `generate_run_sound`, `generate_resolve` and `generator_body` (both `rfl`), `noRef_generate`.
* `Lang/Journey/Gen.lean` (NEW) + `Main.lean`: GN0 the sponsor installs `Std.headGenerator` and creates G;
  GN1 B invokes `G.generate`: admitted, the Turn bears one package cell, its id `= headPackageId`; GN2 B
  creates a head object of THAT id and posts an advance (the generated package runs); GN3 a second
  `generate`: `idTaken` (idempotent up to refusal); GN4 a generator whose bytes do not decode: refused by
  name at the nested install (`program decode …`), nothing born — the floor's deployed run; GN5 a generator
  emitting an ill-typed package: `program illTyped …`.
* `decisions/lang.md` LANG-83, `decisions/kernel.md` KERNEL-68 (cross-layer line).

What re-emits: nothing. What refuses to load: nothing. The judge's question: may an object install, and
is what it installs checked as a member's is.

Next: rung 1 (§3), as its own `lang!` card: the three primitives, `Lang.Quote.packageTerm` with its theorem,
`Std.boundedGenerator` (the first template generator: `bounded S f max` with `max` an argument), the flag
day inventory of §3.3 executed.

## 8. BUILT — rung 1 (FABLE-META-2, 2026-10-26; LANG-87; LANDED as nano `1bdd5ba0`, package wire 5 → 6, full judge GREEN)

**What was built differs from §3.2 in three ways, each a correction read off the code, not a retreat.**

1. **Three binary appends, not four primitives of mixed arity.** `Term.prim` is binary everywhere (the `primL`/`primR`
   frames, the checker's `p.left`/`p.right`, `BigStep.prim`); `len : bytes → nat` and `idBytes : digest → bytes` are
   unary and would have needed a dummy operand. The primitives built are the codec's own `put`s, buffer first:
   `u64be : bytes → nat → bytes` (`Stream.u64be.put`), `sized : bytes → bytes → bytes` (`Stream.bytesV`'s put: varint
   length then bytes), `dsized : bytes → digest → bytes` (the same for an id). One writer per scalar literal kind
   (`nat`, `bytes`, `digest`); `bool` by `ite`. `len` and `varint` were not needed by any template (child counts and
   closed payload lengths are constants; a parameter's own length is written by `sized`). `idBytes` raw was refused:
   an id's bytes enter a byte string only as a codec payload (LANG-38, strengthened).
2. **The quoter is over OPEN terms, and parameters are free variables.** §3.2 imagined `packageTerm : Package → Term`
   with literals "replaced"; what was built is `Quote.quoteTerm ps d buf t` over a template whose free `var i`
   (`i ≥ depth`) is a stage-1 parameter — cross-stage persistence — with the specification `Term.fill` and the theorem
   `quotePackage_sound`: the quoted term appends exactly `encodePackage (fillPackage vals p)`. Every closed subterm is
   one literal fragment; a node's frame is `Tree.putD`'s own prefix.
3. **`Std.bounded`'s refusal lost its number** (`"{f} over the bound"`), because a nano program cannot render decimal
   and the alternative — a nano generator emitting a DIFFERENT law text from the Lean generator — would have been two
   bounded laws. `bounded S f max := boundedWith S f (natT max)`: one definition, a term-shaped bound.

**Landed (nano, LANG-87):** `Lang/Term.lean`, `Lang/Eval.lean` (`appended`, `primBytes.written`), `Lang/Wire.lean`
(codes 12–14), `Lang/Print.lean`, `Lang/Read.lean`, `Lang/Bounds.lean` (version 6), `Lang/Package.lean` (labels /6),
`Lang/Quote.lean` (NEW), `Lang/Proofs/Quote.lean` (NEW: `quoteTerm_sound`, `quotePackage_sound`, `noRef_quotePackage`,
`putD_of_fits`, `putD_frame`, the four `appends_*`), `Lang/Std.lean` (`boundedWith`), `Lang/StdGen.lean`
(`boundedPackageWith`, `boundedPackage`, `boundedGenerator`, `maxParam`, `installOf`, `setMethod`),
`Lang/Proofs/StdGen.lean` (`generate_bounded_sound`, `fill_boundedPackage`), `Lang/Journey/Gen.lean` (GN6–GN8),
`Lang/Proofs/{Sound,Cost,LawMeaning,Provenance,Extract,Std,Receiver,WireTeeth,Teeth}.lean` (the writer cases),
`Emit/Vectors.lean`, `gates/codec-vectors.tsv`, `Lang/Journey.lean` (LV at 6), `decisions/lang.md` LANG-87.

**The rung as it stands.** GN6: `generate {max = 100}` bears the cell of `encodePackage (boundedPackage {n : nat} n
100)`; GN8: the generated law refuses 101 by name. `generate_bounded_sound` has two named premises: the Lean
generator's package has bytes, and those bytes fit a byte value (128 KiB) — the honest limit of staging at the byte
level (§6.1), now a theorem's hypothesis rather than prose.

**Next by this design:** `Std.allowlistGenerator` (a `digest` parameter through `dsized`; authority by naming);
`createOf` (§6.3); a quorum-gated generator; then rung 2 with TYPES's `Ty.seq`.

**Landed after §8 was written (same night):** `c327ba13` LANG-88 — `Std.ownerGenerator`, a generator with NO argument whose
output names its INVOKER (`agentParam = ⟨digest, get req "agent"⟩` through `dsized`; `generate_owner_sound`; GN9–GN11: A, granted
invoke by B, is refused "owner: not on the allowlist" by the package B generated) — §2.3's "authority by naming", with the receipt
as the only input. `74d42e77` LANG-88.1 — `Std.templateGenerator A ps p doc` and ONE theorem `generate_template_sound` (an admitted
run installs `encodePackage (fillPackage vals p)` under `Params`; `hres`, the resolution of `generate`, is `rfl` at any concrete
argument type); the bounded and owner theorems are its ten-line instances. A third template generator now costs a template, a
fill lemma and a `Params` proof.

**Rung 1 is closed.** What remains of this design, in order of value: (a) `createOf` (§6.3) — a KERNEL receiver arm
(`install` then `create` with the id the kernel computed), a Body wire arm (`kernel!`), the Lang call arm, and the confused-deputy
question answered as `create`'s is (the object owned by the SIGNER): coordinate with TRUST's column (Kernel/Receive) by report
line first; (b) a quorum-gated generator — a generator package WITH state and laws (`Std.quorum` over a `generated` counter, the
`generate` method committing the proposal while it installs), which needs a generator method that writes state (not
`templateMethod`) and the quorum's commit arm matched exactly: a journey-heavy card; (c) rung 2 (§1.3, §6.2) over TYPES's `Ty.seq`.

## 9. BUILT — `createOf` and the quorum-gated generator (FABLE-META-3, 2026-10-27; KERNEL-77, LANG-96, LANG-99)

**`createOf` (§6.3, now built).** `Body.createOf pkg laws state` is derived by the two receivers that exist: the package's content id
is read through the signer's pins (a live cell is reused; none means `install`, its check, one birth index on), then `create (some id)`
AS THE SIGNER over the view with the new cell (`withBorn`). The authority question §6.3 left open is answered: the object is the
SIGNER's (`c.unsigned.member`), never the calling object's. Read against the code, a nested `create` would have been owned by the
OBJECT (`objectCell X a.actor`), a shape the kernel has never had; owner = signer keeps "every object's owner signed the Turn that bore
it", and spends nobody's authority (the signer could make the same two cells itself). The object is born first, so its id does not
depend on whether the package was installed. Lang: the call arm `createOf : rec {pkg : bytes, state : T}`, its state a VALUE of the
slot's declared state type, laid out by the codec a birth's seed uses; `Std.templateCreator` / `Std.boundedCreator`;
`make_template_sound`, `make_bounded_sound`; journey GN12–GN17; the testground's `creator` demo and tour step.

**The quorum-gated generator.** `Std.quorumGenerator r f members k`: a generator object under `Std.quorum` over `generated`; its
`generate` commits the approved proposal and installs the template at it in one Turn, so the law's commit arm gates the install
(`generate_quorum_sound`; GN18–GN20). What it lacks is the quorum law's own meaning theorem (LANG-99's critique).

## 10. The `code` type, with TYPES (a design note, not a build)

A generator's type should say PACKAGE, not bytes, and the cheapest honest shape is not a type of terms (§6.2's `Ty.code` with
constructor primitives) but a type of INSTALLED INTERFACES: `Ty.pkg I`, whose values are package bytes that `checkInstall` accepts at
interface `I` (state type, method signatures, laws by label), with one introduction (a quoted template whose interface is `I` with
its parameters' types in it, checked at the GENERATOR's install, where the template is closed except for typed stage-1 holes) and no
elimination in the language (the only consumer is the kernel's `install`/`createOf`, whose arms become `pkg : pkg I`). The quoter
already knows the template's interface (it is the template's `iface`, untouched by filling: parameters live in bodies), so
`quotePackage_sound` plus "filling preserves `checkWith` at `I`" — a substitution lemma over the checker, TYPES's column, where the
graded effects of LANG-89 already add the one quantity an interface must carry (`moves`) — would let install re-check nothing a
generator's own install did not; createOf's state `T` is then `I`'s state type, not a second slot parameter (LANG-96's critique). The
price: one Ty constructor (a premise on every `Ty` induction), the substitution lemma for typed holes, and the decision that
interface equality is syntactic (no subtyping). It is still Template Haskell's choice, typed: the stage-2 check stays the kernel's;
what moves is that a generator whose output cannot check at `I` is refused at ITS install, not at each generation.

## 11. DECIDED and BUILT — the quorum's meaning, and the interface a method produces (FABLE-META-4, 2026-10-27; LANG-102, LANG-103)

**The quorum's meaning (LANG-102).** The one-step theorem §9 said was missing existed already (`quorum_change_needs_k`). What was
missing was its meaning over a history. `Std.quorum_commit_attested` (Lang/Proofs/StdQuorum.lean): along any history of
`quorumLaw` from a state with no approvals, over distinct members, a commit of `v` follows approvals of exactly `set v` by `k`
distinct members, each a step of the same history. `Std.quorumGenerator` is now a checked constructor (it had let `k = 0` install
with no approval, and a repeated member hold two bits). `quorumGenerator_installs_attested` is §9's composition as one theorem.

**`Ty.pkg I`, decided against for now; the interface is a grade (LANG-103).** §10's type needs one introduction the checker can
check, a quoted template. The quoter is a Lean function that writes a `bytes` term, so no such introduction exists. A `Ty.pkg I`
today would be a coercion or a subtyping rule, a case on every `Ty` and `Term` induction, and no static check. The property
("a method that returns a package cannot return one of the wrong shape") is a fact about a method's calls, which is what grades
are. So `Effect.produces I`: the run refuses by name (`produces generate: lacks reset`) a package whose `iface` is not `I`, and
install refuses `badProduces` a method that cannot install. `runMeasured_produces` is the statement. The static form (refuse the
generator at its own install) waits for rung 2's checker-visible `quote`, which will check against the same `produces I`. LANG-96's
critique (createOf's `T` should be `I`'s state type) stays open: `iface` carries no state type.
