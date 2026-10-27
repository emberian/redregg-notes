# Syntax ideas for Objective Bend

Ember, 2026-10-27: the nano interface shows many s-expressions; is there a surface syntax less "the way it is right now", or should it stay; at least it could be pretty-printed with Unicode.

This document renders one program in sixteen syntaxes.
Each rendering is complete.
Each carries a six-line verdict.
The end ranks them and costs the cheapest large improvement.

Sources read (nanodregg `origin/main` at 5711173): `README.md` "One program", `Lang/Surface.lean` (`grammar`, `declsOf`, `relDecl`, `methodHead`), `Lang/Read.lean` (`grammar`), `Lang/Claim.lean`, `Lang/Package.lean` (`checkClaim`, `checkEffects`), `Lang/Proofs/Print.lean`, `docs/spec/2-structure.md`, `world/escrow/Escrow.ob`, `world/resident/Bell.ob`.

## The sample

The sample is the README's program with five additions the brief asks for.

- The hole has a context entry `c`, so each candidate is a term over `c`, and `bump` passes `state.count` as the substitution.
- `choose` and `make` take bounded arguments.
- `make` declares a grade, `(effect (moves 0))`.
- The package declares an invariant `le100` and a claim `keeps le100 cap`.
- Every `ok` leaf of `cap` lies under the test `le100 new`, the shape `Term.guardedBy` accepts.

`make` installs a package and moves no value.
A grade of 0 on a method whose type cannot move value is allowed (`checkEffects`: "a grade a type does not use is allowed").

### A finding: today's surface cannot write a `keeps` claim

`Package.checkClaim` requires the invariant to be an interface field of type `fn S bool` whose body is a literal `lam`.
No surface declaration makes such a field.
`declsOf` accepts `type`, `state`, `rel`, `method`, `law`, `guard`, `activity`, `machine`, `import`, `doc`, `layer`, `claim` and `hole`.
A surface `guard` has the relation-guard type `state req edit old`, not `fn S bool`.
So a surface `(claim keeps INV LAW)` lowers, and install refuses it `claimNotInvariant INV`.
`Lang/Journey/Claims.lean` exercises claims only through packages built in Lean (LK0) and through that refusal (LK0b).
The checker also requires the law's test to be the literal `app (lam S ib) new`.
So a surface `invariant` form must inline its lambda at each use in a law, or the checker must accept `app (get self le100) new`.
The sample writes the missing form as `(invariant le100 e)`, binding `state`, and marks the line.
This is the one line of candidate 1 the reader refuses today.

## 1. Today's s-expression surface

```
(package
  (doc "a counter whose step is chosen in context; it makes parameter packages")
  (state (rec (count nat)))
  (invariant le100 (<= state.count 100))   ; not in today's surface: see the finding above
  (claim keeps le100 cap)
  (rel choice (key (k nat)) (val nat) (limit 1))
  (hole step ((c nat) ⊢ nat)
    (select choice (record (k 0)))
    (candidate (+ c 1))
    (candidate (+ c 10) (cell #G)))
  (method bump
    (done (with state (count (hole step state.count)))))
  (method choose (arg (rec (i (nat 0 1)))) (edits 1)
    (done state (upsert choice (record (k 0)) arg.i)))
  (method make (arg (rec (n (nat 1 1000)))) (calls (install)) (effect (moves 0))
    (done state
      (install (pkg (cat (u64be #0a00000b00000004000004000106016e010000000800010f016e010408 arg.n)
                         #00010000010000020000000000030000040000050000)))))
  (law cap
    (on (adopt birth invoke) (if (le100 new) ok (refuse "over 100")))
    (on retire (if (le100 new) (if (== old.count 0) ok (refuse "not empty")) (refuse "over 100")))
    (else (refuse "frozen"))))
```

- **Buys.** One reader for surface and core (`Read.parse`); every node has a character offset; the grammar fits in twenty-one lines.
- **Costs.** Nothing new; the price is reading: closing-paren runs, `(record (k 0))` for a one-field key, and no visual difference between a declaration and a term.
- **Holes and supports.** `(candidate e fact…)` reads well; the context `((c nat) ⊢ nat)` reads well; a use `(hole step state.count)` hides which context entry the argument fills.
- **Refusal position.** `Refusal.text` names the refusal and the line of the form's offset: `noHole step line 12`; exact for the text as written.
- **Surface or printer.** The surface; every other candidate is measured against it.
- **Audience.** Max von Hippel reads it without effort; a programmer tolerates it; a member reading a refusal in a dialog sees a line number into text they may not have written.

## 2. Unicode pretty-print of the same tree

```
package — a counter whose step is chosen in context; it makes parameter packages

  state   ⟨count : ℕ⟩
  inv     le100 ≔ state.count ≤ 100
  claim   le100 kept by cap

  rel     choice : ⟨k : ℕ⟩ ↦ ℕ                     limit 1

  hole    step : [c : ℕ ⊢ ℕ]                        selected by choice⟨k ≔ 0⟩
    ◯₀    c + 1
    ◯₁    c + 10                                    ⊣ live G

  method  bump
    done  state⟨count ≔ ◯step[c ↦ state.count]⟩

  method  choose ⟨i : ℕ ∈ 0‥1⟩                      edits 1
    done  state · choice⟨k ≔ 0⟩ ← arg.i

  method  make ⟨n : ℕ ∈ 1‥1000⟩                     calls install · moves ≤ 0
    done  state · install pkg(#0a00000b00000004000004000106016e010000000800010f016e010408 ‖u64 arg.n
                              ⧺ #00010000010000020000000000030000040000050000)

  law     cap : old → new → req → Verdict
    birth ∨ adopt ∨ invoke  ↦  if le100 new then ⊤ else ⊥ “over 100”
    retire                  ↦  if le100 new
                                 then if old.count = 0 then ⊤ else ⊥ “not empty”
                                 else ⊥ “over 100”
    write ∨ relaw           ↦  ⊥ “frozen”
```

The same hole, printed under the view `(view (select step 1) (dead #G))`:

```
  hole    step : [c : ℕ ⊢ ℕ]                        selected by choice⟨k ≔ 0⟩ = 1
    ◯₀    c + 1
    ◉₁    c + 10                                    ⊣ live G ✗
          ⇒ refused holeSupportDead 0 cell:G
```

Glyph table (each glyph maps to exactly one token or form):

| text | glyph | text | glyph |
|---|---|---|---|
| `nat` | `ℕ` | `(rec (f T)…)` | `⟨f : T, …⟩` |
| `<=` | `≤` | `(record (f e)…)` | `⟨f ≔ e, …⟩` |
| `==` | `=` | `(with e (f x))` | `e⟨f ≔ x⟩` |
| `->` | `→` | `(hole u e…)` | `◯u[x ↦ e, …]` |
| `cat` | `⧺` | `(upsert r k v)` | `r⟨k⟩ ← v` |
| `deq` | `≡` | `(insert r k v)` / `(retract r k)` | `r⟨k⟩ ⊕ v` / `r⟨k⟩ ⊖` |
| `ok` | `⊤` | `(refuse "r")` | `⊥ “r”` |
| `and` / `any` / `not` | `∧` / `∨` / `¬` | `(row r k 3)` | `r⟨k⟩₃` |
| `(none T)` | `∅` | `(lam x T e)` | `λx:T. e` |

- **Buys.** The highest readability gain per line of code: types read as types, the hole reads as CMTT's `u[σ]`, and ✓/✗ against a view shows which support killed a candidate.
- **Costs.** A printer `SExp → String` with a layout pass and the glyph table; no new parser if display-only; a token-level round trip if the reader also accepts the glyphs (see the last section).
- **Holes and supports.** Best of all candidates: `◯₁ … ⊣ live G ✗` puts the candidate, its fact and the fact's state on one line.
- **Refusal position.** The printer keeps a map from printed token to source offset, so a refusal highlights the printed token; the line number stays the source's.
- **Surface or printer.** A printer; it becomes a second spelling of the same surface only if the reader accepts the glyph aliases.
- **Audience.** All three prefer it: von Hippel for the notation he already writes, a programmer for `≤` over `<=`, a member for ✗ beside the dead fact.

## 3. Lean-4-style declarations

```lean
package Counter where
  doc "a counter whose step is chosen in context; it makes parameter packages"

  structure State where
    count : Nat

  invariant le100 (state : State) : Bool := state.count ≤ 100

  relation choice (k : Nat) : Nat
    limit 1

  hole step : [c : Nat ⊢ Nat]
    select choice ⟨k := 0⟩
    | c + 1
    | c + 10   requires live G

  method bump : Result :=
    done { state with count := ?step[state.count] }

  method choose (i : Nat) (_ : i ∈ 0..1) : Result
    edits 1 :=
    done state [upsert choice ⟨k := 0⟩ i]

  method make (n : Nat) (_ : n ∈ 1..1000) : Result
    calls [install]
    effect (moves 0) :=
    done state [install (pkg ((#0a00000b00000004000004000106016e010000000800010f016e010408).u64be n
                              ++ #00010000010000020000000000030000040000050000))]

  law cap (old new : State) (req : Req) : Verdict :=
    match req.occasion with
    | .birth | .adopt | .invoke => if le100 new then ok else refuse "over 100"
    | .retire => if le100 new then (if old.count = 0 then ok else refuse "not empty") else refuse "over 100"
    | .write | .relaw => refuse "frozen"

  theorem cap_keeps : keeps le100 cap := by shape
```

- **Buys.** Familiar to the people who read the rest of the repository; `{ s with f := e }` and `match … with | .birth` are precise.
- **Costs.** A full layout parser with `where` blocks; `theorem … := by shape` invites the reading that Lean proved it, when install's `checkClaim` checked a shape; a `.ob` file that looks like Lean sits beside Lean files it is not.
- **Holes and supports.** `?step[state.count]` is Lean's metavariable spelling, which is close to right; `requires live G` reads well.
- **Refusal position.** Line and column; layout errors become a new refusal class (`badIndent`).
- **Surface or printer.** A second surface; a new reader, a new printer, a new round-trip theorem beside `readPackage_package`.
- **Audience.** Von Hippel likes it until he tries `#check` on it; a programmer finds it heavy; a member gains nothing over candidate 2.

## 4. ML / OCaml-style

```ocaml
(** a counter whose step is chosen in context; it makes parameter packages *)
package Counter = struct
  type state = { count : nat }

  let le100 (state : state) : bool = state.count <= 100
  claim keeps le100 cap

  relation choice : { k : nat } -> nat  limit 1

  hole step : (c : nat) |- nat
    select choice { k = 0 }
    | c + 1
    | c + 10  needs [cell g]

  method bump () =
    done { state with count = step state.count }

  method choose ~(i : nat [@range 0 1]) [@edits 1] =
    done state [ upsert choice { k = 0 } i ]

  method make ~(n : nat [@range 1 1000]) [@calls install] [@moves 0] =
    done state [ install (pkg (u64be 0x0a00000b00000004000004000106016e010000000800010f016e010408 n
                               ^ 0x00010000010000020000000000030000040000050000)) ]

  law cap old nw req =
    match req.occasion with
    | Birth | Adopt | Invoke -> if le100 nw then ok else refuse "over 100"
    | Retire -> if le100 nw then (if old.count = 0 then ok else refuse "not empty") else refuse "over 100"
    | Write | Relaw -> refuse "frozen"
end
```

- **Buys.** The match on the occasion is exhaustive, which states in the syntax what the lowering already enforces (one arm per occasion, no default).
- **Costs.** `new` is an OCaml keyword, so the law's binder is renamed, and the language's own names now depend on a host's keyword list; attributes `[@…]` are an awkward home for grades; a second parser.
- **Holes and supports.** `(c : nat) |- nat` is ASCII for `⊢` and reads fine; `needs [cell g]` reads well.
- **Refusal position.** Line and column; a missing `|` arm refuses at the `match`, which is where a reader looks.
- **Surface or printer.** A second surface.
- **Audience.** A verification researcher who writes Coq or OCaml reads it at once; a programmer from Rust or TypeScript reads it with mild effort; a member gains nothing over candidate 2.

## 5. Haskell-style layout

```haskell
package Counter where
  -- | a counter whose step is chosen in context; it makes parameter packages

  data State = State { count :: Nat }

  le100 :: State -> Bool
  le100 s = count s <= 100

  claim keeps le100 cap

  choice :: Rel { k :: Nat } Nat
  choice = rel `limit` 1

  step :: [c :: Nat ⊢ Nat]
  step = select (choice { k = 0 })
    [ c + 1
    , c + 10 `given` [live g] ]

  bump :: Method ()
  bump = done state { count = step (count state) }

  choose :: Method { i :: Nat `within` 0..1 }
  choose = done state [upsert choice { k = 0 } (i arg)]
    where edits = 1

  make :: Method { n :: Nat `within` 1..1000 }
  make = done state [install (pkg (a `u64be` n arg <> b))]
    where calls = [Install]
          moves = 0
          a = 0x0a00000b00000004000004000106016e010000000800010f016e010408
          b = 0x00010000010000020000000000030000040000050000

  cap :: State -> State -> Req -> Verdict
  cap old new req = case occasion req of
    o | o `elem` [Birth, Adopt, Invoke] ->
          if le100 new then Ok else Refuse "over 100"
    Retire
      | le100 new, count old == 0 -> Ok
      | le100 new                 -> Refuse "not empty"
      | otherwise                 -> Refuse "over 100"
    _ -> Refuse "frozen"
```

- **Buys.** Guards read the law the way a person states it; `where` puts grades after the body, where they are least in the way.
- **Costs.** Haskell layout is the hardest layout rule to implement and to prove a printer against; the `_ ->` default must lower to one arm per remaining occasion; guards must lower so that each `Ok` lies under the literal `le100 new` test, or `claimUnproved` fires on a law that reads correct.
- **Holes and supports.** `step (count state)` hides that `step` is a hole; a reader cannot tell a hole use from a function call.
- **Refusal position.** Line and column; layout errors are notoriously hard to explain to a non-Haskeller.
- **Surface or printer.** A second surface.
- **Audience.** A PL researcher likes it; a programmer outside Haskell does not; a member is lost at `` `elem` ``.

## 6. Rust-like braces

```rust
/// a counter whose step is chosen in context; it makes parameter packages
package Counter {
    struct State { count: nat }

    invariant le100(state: &State) -> bool { state.count <= 100 }
    claim keeps(le100, cap);

    rel choice: { k: nat } => nat, limit 1;

    hole step: [c: nat ⊢ nat] select choice { k: 0 } {
        c + 1,
        c + 10 where live(G),
    }

    fn bump(state) -> Result {
        done!(State { count: step![state.count], ..state })
    }

    #[edits(1)]
    fn choose(state, i: nat in 0..=1) -> Result {
        done!(state; upsert choice { k: 0 } => i)
    }

    #[calls(install)]
    #[effect(moves = 0)]
    fn make(state, n: nat in 1..=1000) -> Result {
        done!(state; install pkg(u64be(x"0a00000b00000004000004000106016e010000000800010f016e010408", n)
                                 ++ x"00010000010000020000000000030000040000050000"))
    }

    law cap(old: State, new: State, req: Req) -> Verdict {
        match req.occasion {
            Birth | Adopt | Invoke => if le100(new) { ok } else { refuse!("over 100") },
            Retire => if le100(new) {
                if old.count == 0 { ok } else { refuse!("not empty") }
            } else { refuse!("over 100") },
            Write | Relaw => refuse!("frozen"),
        }
    }
}
```

- **Buys.** The widest programmer audience; braces make block structure unambiguous without layout rules; attributes are a known home for grades.
- **Costs.** A second parser with precedence and macros-that-are-not-macros (`done!`, `step!`); it promises Rust semantics (borrowing in `&State`, `..state` move) the language does not have; a natural `if !le100(new) { refuse }` is refused `claimUnproved`, since the checker wants the positive test.
- **Holes and supports.** `step![…]` marks the hole use; `where live(G)` reads well.
- **Refusal position.** Line and column; a brace mismatch is easy to report.
- **Surface or printer.** A second surface.
- **Audience.** A programmer prefers it; von Hippel finds it noisy; a member sees code that looks like it should compile with `cargo` and does not.

## 7. WebAssembly text format, folded

```wat
(package $counter
  (doc "a counter whose step is chosen in context; it makes parameter packages")
  (type $State (rec (field $count nat)))
  (state $State)
  (invariant $le100 (param $state $State) (result bool)
    (nat.le (rec.get $count (local.get $state)) (nat.const 100)))
  (claim (keeps $le100 $cap))
  (rel $choice (key (field $k nat)) (val nat) (limit 1))
  (hole $step (param $c nat) (result nat)
    (select $choice (rec.new (field $k (nat.const 0))))
    (candidate (nat.add (local.get $c) (nat.const 1)))
    (candidate (nat.add (local.get $c) (nat.const 10))
      (support (cell (digest.const $G)))))
  (method $bump
    (done (rec.with $count (local.get $state)
            (hole $step (rec.get $count (local.get $state))))))
  (method $choose (param $i nat (range 0 1)) (edits 1)
    (done (local.get $state)
      (upsert $choice (rec.new (field $k (nat.const 0))) (local.get $i))))
  (method $make (param $n nat (range 1 1000)) (calls install) (effect (moves 0))
    (done (local.get $state)
      (install (pkg (bytes.cat
        (bytes.u64be
          (bytes.const "\0a\00\00\0b\00\00\00\04\00\00\04\00\01\06\01\6e\01\00\00\00\08\00\01\0f\01\6e\01\04\08")
          (local.get $n))
        (bytes.const "\00\01\00\00\01\00\00\02\00\00\00\00\00\03\00\00\04\00\00\05\00\00"))))))
  (law $cap (param $old $State) (param $new $State) (param $req $Req) (result $Verdict)
    (case (rec.get $occasion (local.get $req))
      (arm (birth adopt invoke)
        (if (result $Verdict) (call $le100 (local.get $new))
          (then (verdict.ok))
          (else (verdict.refuse "over 100"))))
      (arm (retire)
        (if (result $Verdict) (call $le100 (local.get $new))
          (then (if (result $Verdict) (nat.eq (rec.get $count (local.get $old)) (nat.const 0))
                  (then (verdict.ok))
                  (else (verdict.refuse "not empty"))))
          (else (verdict.refuse "over 100"))))
      (arm (write relaw) (verdict.refuse "frozen")))))
```

- **Buys.** Typed operator names (`nat.add`, `bytes.cat`) state the monomorphic primitive at each use, which is exactly the language's typing; `$` sigils separate names from keywords.
- **Costs.** About twice the length of candidate 1; it is still an s-expression, so it answers the question "less like it is now" with "more like it is now"; the parser is today's parser with a new head-word table.
- **Holes and supports.** `(hole $step …)` and `(support (cell …))` read clearly; no gain over candidate 1.
- **Refusal position.** Character offset of the form, as today.
- **Surface or printer.** Either; as a printer of the core text it is a plausible "verbose core" view, since the core is already folded s-expressions.
- **Audience.** A reader of the Wasm spec feels at home; nobody else gains.

## 8. Indentation only, keywords, no brackets

```
package counter
  doc: a counter whose step is chosen in context; it makes parameter packages
  state:
    count: nat
  invariant le100: state.count <= 100
  claim: keeps le100 cap

  relation choice:
    key: k nat
    value: nat
    limit: 1

  hole step:
    context: c nat
    type: nat
    select: choice k=0
    candidate: c + 1
    candidate: c + 10
      needs: live G

  method bump:
    done: state with count = step(c = state.count)

  method choose:
    arg: i nat 0..1
    edits: 1
    done: state
      upsert choice k=0 := arg.i

  method make:
    arg: n nat 1..1000
    calls: install
    effect: moves 0
    done: state
      install pkg(u64be(0x0a00000b00000004000004000106016e010000000800010f016e010408, arg.n)
                  ++ 0x00010000010000020000000000030000040000050000)

  law cap:
    on birth adopt invoke:
      if le100 new: ok
      else: refuse "over 100"
    on retire:
      if le100 new:
        if old.count == 0: ok
        else: refuse "not empty"
      else: refuse "over 100"
    else: refuse "frozen"
```

- **Buys.** The declaration skeleton becomes a form a member can fill in; each clause is one line with its keyword.
- **Costs.** Terms still need brackets or precedence, so it is two syntaxes in one file; YAML-style indentation is fragile under copy and paste in a dialog; a whitespace-sensitive reader and its round trip.
- **Holes and supports.** `candidate:` / `needs:` read as plainly as anything here.
- **Refusal position.** Line and column; a mis-indented `else:` changes meaning silently unless the reader refuses ambiguous dedents.
- **Surface or printer.** Either; as a printer of the declaration skeleton, with terms in candidate 2's notation, it is a good inspector view.
- **Audience.** A member writing a first package prefers it; a programmer accepts it; von Hippel distrusts whitespace semantics.

## 9. Smalltalk / Self message sends

```smalltalk
Package subclass: #Counter
    doc: 'a counter whose step is chosen in context; it makes parameter packages'
    state: 'count <Nat>'.

Counter invariant: #le100 is: [:state | state count <= 100].
Counter claim: #le100 keptBy: #cap.

Counter relation: #choice key: 'k <Nat>' value: Nat limit: 1.

Counter hole: #step context: 'c <Nat>' type: Nat
    selectedBy: (#choice at: (k: 0))
    candidates: {
        [:c | c + 1].
        [:c | c + 10] needing: (Cell live: G) }.

Counter >> bump
    ^ self done: (state count: (self step: state count))

Counter >> choose: i <Nat from: 0 to: 1>
    <edits: 1>
    ^ self done: state with: (#choice upsert: (k: 0) value: i)

Counter >> make: n <Nat from: 1 to: 1000>
    <calls: #(install)>
    <moves: 0>
    ^ self done: state with: (Install pkg:
        ((#[16r0a 16r00 16r00 16r0b 16r00 16r00 16r00 16r04 16r00 16r00 16r04 16r00 16r01 16r06 16r01
            16r6e 16r01 16r00 16r00 16r00 16r08 16r00 16r01 16r0f 16r01 16r6e 16r01 16r04 16r08] u64be: n),
          #[16r00 16r01 16r00 16r00 16r01 16r00 16r00 16r02 16r00 16r00 16r00 16r00 16r00 16r03 16r00
            16r00 16r04 16r00 16r00 16r05 16r00 16r00]))

Counter law: #cap judges: [:old :new :req |
    req occasion
        caseOf: {
            #(birth adopt invoke) -> [(self le100: new)
                ifTrue: [ok]
                ifFalse: [refuse: 'over 100']].
            #(retire) -> [(self le100: new)
                ifTrue: [old count = 0 ifTrue: [ok] ifFalse: [refuse: 'not empty']]
                ifFalse: [refuse: 'over 100']].
            #(write relaw) -> [refuse: 'frozen'] }].

"A member then writes: counter choose: 1. counter bump. counter make: 7."
```

- **Buys.** The invocation side reads naturally (`counter choose: 1`), which matches the object model: an object answers the messages its package names.
- **Costs.** Keyword messages make the declaration side verbose; binary-operator precedence (`state count <= 100` parses left to right) differs from every other candidate; a second parser.
- **Holes and supports.** `[:c | c + 10] needing: (Cell live: G)` is clear; `self step: state count` hides that `step` is a hole.
- **Refusal position.** Line and column within a method; Smalltalk tradition reports errors per method, which matches a per-method lowering.
- **Surface or printer.** A second surface for packages; the message form is a good printer for CALLS in the dialog (`counter choose: 1`).
- **Audience.** A member reading what a call does prefers the message form; a programmer finds the declarations odd; von Hippel is indifferent.

## 10. Datalog / Prolog for laws (and holes), the rest in candidate 2

The declarations other than the law and the hole, in candidate 2's notation:

```
package — a counter whose step is chosen in context; it makes parameter packages
  state   ⟨count : ℕ⟩
  claim   le100 kept by cap
  rel     choice : ⟨k : ℕ⟩ ↦ ℕ                     limit 1
  method  bump                                     done state⟨count ≔ ◯step[c ↦ state.count]⟩
  method  choose ⟨i : ℕ ∈ 0‥1⟩     edits 1          done state · choice⟨k ≔ 0⟩ ← arg.i
  method  make ⟨n : ℕ ∈ 1‥1000⟩    calls install · moves ≤ 0
                                                   done state · install pkg(#0a00000b00000004000004000106016e010000000800010f016e010408 ‖u64 arg.n
                                                                            ⧺ #00010000010000020000000000030000040000050000)
```

The invariant, the law and the hole, as clauses:

```prolog
% the invariant
le100(S) :- S.count =< 100.

% the law cap: exactly one verdict per (occasion, old, new)
verdict(cap, O, _Old, New, ok)                 :- member(O, [birth, adopt, invoke]), le100(New).
verdict(cap, O, _Old, New, refused("over 100")) :- member(O, [birth, adopt, invoke]), \+ le100(New).
verdict(cap, retire, Old, New, ok)             :- le100(New), Old.count =:= 0.
verdict(cap, retire, Old, New, refused("not empty")) :- le100(New), Old.count =\= 0.
verdict(cap, retire, _Old, New, refused("over 100")) :- \+ le100(New).
verdict(cap, O, _, _, refused("frozen"))       :- member(O, [write, relaw]).

% the hole step :: [c : nat ⊢ nat], selected by choice{k=0}
candidate(step, 0, C, V) :- V is C + 1.
candidate(step, 1, C, V) :- live(cell(g)), V is C + 10.
```

- **Buys.** Two checks become syntactic over clause heads: the claim is "every clause with head `…, ok)` has `le100(New)` in its body", and a support is a clause body literal, so a dead support is a failed body literal by name.
- **Costs.** The compiler must prove the clauses functional and exhaustive (exactly one verdict per input), which a `case` on the occasion gives by construction; negation needs stratification; the lowering to `case`/`ite` is a real compiler, not a reader.
- **Holes and supports.** The best semantic fit of any candidate: a candidate is a clause, its facts are its body, and "refused because `live(cell(g))` failed" is what a Prolog trace already says.
- **Refusal position.** A clause and a body literal: `cap clause 4, literal Old.count =\= 0`; precise, and meaningful to a reader.
- **Surface or printer.** A second surface for laws, and research: it changes what the checker can see, not only how text looks.
- **Audience.** Von Hippel prefers it for laws; a programmer reads it with effort; a member reads a refusal that names a clause as well as one that names a line.

## 11. Agda-style, Unicode and mixfix

```agda
module Counter where
  -- a counter whose step is chosen in context; it makes parameter packages

  record State : Type where
    field count : ℕ

  le100 : State → Bool
  le100 s = count s ≤ᵇ 100

  choice : Rel ⟨ k ∶ ℕ ⟩ ℕ
  choice = relation limit 1

  step : [ c ∶ ℕ ⊢ ℕ ]
  step = select choice ⟨ k ≔ 0 ⟩
    ∣ c + 1
    ∣ c + 10  ⊣ live G

  bump : Method ⟨⟩
  bump = done (state ⟨ count ≔ step [ c ≔ count state ] ⟩)

  choose : Method ⟨ i ∶ ℕ ∈ 0 ‥ 1 ⟩ ⦃ edits 1 ⦄
  choose = done state ⸴ choice ⟨ k ≔ 0 ⟩ ↤ i

  make : Method ⟨ n ∶ ℕ ∈ 1 ‥ 1000 ⟩ ⦃ calls install ⦄ ⦃ moves≤ 0 ⦄
  make = done state ⸴ install (pkg (A ‖ᵘ⁶⁴ n ⧺ B))
    where
      A = 0x0a00000b00000004000004000106016e010000000800010f016e010408
      B = 0x00010000010000020000000000030000040000050000

  cap : (old new : State) → Req → Verdict
  cap old new req with occasion req
  ... | birth  = if le100 new then ok else refuse "over 100"
  ... | adopt  = if le100 new then ok else refuse "over 100"
  ... | invoke = if le100 new then ok else refuse "over 100"
  ... | retire = if le100 new then (if count old ≡ᵇ 0 then ok else refuse "not empty") else refuse "over 100"
  ... | write  = refuse "frozen"
  ... | relaw  = refuse "frozen"

  cap-keeps : keeps le100 cap
  cap-keeps = by-shape
```

- **Buys.** The type-theoretic content is on the page: `[ c ∶ ℕ ⊢ ℕ ]` is the declaration in the paper's notation; one arm per occasion is visible.
- **Costs.** Mixfix parsing (operator sections, precedence declarations) is the most expensive parser here; Unicode input needs an input method; `cap-keeps = by-shape` again suggests a proof term that does not exist.
- **Holes and supports.** `step [ c ≔ count state ]` is the explicit substitution, spelled correctly; `⊣ live G` reads well.
- **Refusal position.** Line and column; mixfix ambiguity errors are hard to explain.
- **Surface or printer.** A second surface; candidate 2 takes its best ideas without the mixfix parser.
- **Audience.** Von Hippel prefers it; a programmer does not; a member cannot type it.

## 12. The package as a table

The declarations:

| # | kind | name | type | body | facts / grade |
|---|---|---|---|---|---|
| | doc | | | a counter whose step is chosen in context; it makes parameter packages | |
| | state | | ⟨count : ℕ⟩ | | |
| | invariant | le100 | State → bool | state.count ≤ 100 | |
| | claim | keeps | le100 ⊣ cap | checked at install by shape | |
| 0 | relation | choice | ⟨k : ℕ⟩ ↦ ℕ | | limit 1 |
| 0 | hole | step | [c : ℕ ⊢ ℕ] | selected by choice⟨k ≔ 0⟩ | |
| 0.0 | candidate | | | c + 1 | none |
| 0.1 | candidate | | | c + 10 | live G |
| 0 | method | bump | ⟨⟩ | done state⟨count ≔ ◯step[c ↦ state.count]⟩ | |
| 1 | method | choose | ⟨i : ℕ ∈ 0‥1⟩ | done state · choice⟨k ≔ 0⟩ ← arg.i | edits 1 |
| 2 | method | make | ⟨n : ℕ ∈ 1‥1000⟩ | done state · install pkg(A ‖u64 arg.n ⧺ B) | calls install · moves ≤ 0 |
| 0 | law | cap | old → new → req → Verdict | the decision table below | |

`A` = `#0a00000b00000004000004000106016e010000000800010f016e010408`, `B` = `#00010000010000020000000000030000040000050000`.

The law `cap` as a decision table:

| occasion | le100 new | old.count = 0 | verdict |
|---|---|---|---|
| birth, adopt, invoke | true | any | ok |
| birth, adopt, invoke | false | any | refused "over 100" |
| retire | true | true | ok |
| retire | true | false | refused "not empty" |
| retire | false | any | refused "over 100" |
| write, relaw | any | any | refused "frozen" |

- **Buys.** The index column states the method and hole numbers a call uses (`bump` is 0); the law table makes the claim checkable by eye: every `ok` row has `le100 new = true`.
- **Costs.** A table cannot hold a nested term such as the escrow's `invoke` arm or the Bell's `answer`; as source it would need a cell grammar plus the term grammar inside cells.
- **Holes and supports.** One row per candidate with its facts in a column; a view adds a column of ✓/✗, which is the clearest display of a hole there is.
- **Refusal position.** A row and a column: `law cap, row 4, verdict "not empty"`; the best target for a member in a dialog.
- **Surface or printer.** A printer; the testground's inspector already shows a package this way.
- **Audience.** A member prefers it; a programmer uses it as an index; von Hippel uses the decision table and reads terms elsewhere.

## 13. Literate form

```
§1  A counter keeps one natural, and never more than 100.

    ⟨state⟩ ≡
      (state (rec (count nat)))
      (invariant le100 (<= state.count 100))

§2  The package claims that its law keeps the invariant. Install checks
    the claim against the law's shape (§6).

    ⟨claim⟩ ≡
      (claim keeps le100 cap)

§3  How far a bump moves is decided in context. A one-row relation holds
    the choice; the hole offers two steps, and the larger one relies on
    the grant G being live.

    ⟨choice⟩ ≡
      (rel choice (key (k nat)) (val nat) (limit 1))
      (hole step ((c nat) ⊢ nat)
        (select choice (record (k 0)))
        (candidate (+ c 1))
        (candidate (+ c 10) (cell #G)))

§4  bump applies the chosen step; choose writes the choice.

    ⟨methods⟩ ≡
      (method bump
        (done (with state (count (hole step state.count)))))
      (method choose (arg (rec (i (nat 0 1)))) (edits 1)
        (done state (upsert choice (record (k 0)) arg.i)))
      ⟨make⟩

§5  make writes the bytes of a package that exports n, and installs them.
    It moves no value, and says so.

    ⟨make⟩ ≡
      (method make (arg (rec (n (nat 1 1000)))) (calls (install)) (effect (moves 0))
        (done state
          (install (pkg (cat (u64be #0a00000b00000004000004000106016e010000000800010f016e010408 arg.n)
                             #00010000010000020000000000030000040000050000)))))

§6  The law admits a birth, an adoption or an invocation only at count at
    most 100, a retirement only at count 0, and refuses writes and law
    replacements. Every ok sits under the test le100 new, which is what
    §2's claim requires.

    ⟨law⟩ ≡
      (law cap
        (on (adopt birth invoke) (if (le100 new) ok (refuse "over 100")))
        (on retire (if (le100 new) (if (== old.count 0) ok (refuse "not empty")) (refuse "over 100")))
        (else (refuse "frozen")))

    ⟨package⟩ ≡
      (package
        (doc "a counter whose step is chosen in context; it makes parameter packages")
        ⟨state⟩ ⟨claim⟩ ⟨choice⟩ ⟨methods⟩ ⟨law⟩)
```

- **Buys.** The reason for each declaration sits beside it; the README already works this way, and `Lang/Journey/Readme.lean` already extracts the block from prose.
- **Costs.** A tangler (chunk names, expansion order) and a rule that a refusal maps back through it; prose drifts from code unless a gate reads both, as `Readme.lean` does.
- **Holes and supports.** As in whichever syntax the chunks use; the prose explains why a candidate relies on its fact, which no other candidate does.
- **Refusal position.** A chunk name and a line within it: `⟨choice⟩ line 4`.
- **Surface or printer.** A document format over any surface; orthogonal to the choice of term syntax.
- **Audience.** All three readers of the README prefer it there; nobody wants to write a package this way in a dialog.

## 14. Concatenative (Factor / Forth) for method bodies

The declarations stay in candidate 2's notation; the bodies and the law are stack words.

```factor
! state ⟨count : ℕ⟩ · rel choice ⟨k : ℕ⟩ ↦ ℕ limit 1 · claim le100 kept by cap
! hole step [c : ℕ ⊢ ℕ] selected by choice⟨k ≔ 0⟩ : ◯₀ c + 1 · ◯₁ c + 10 ⊣ live G

INVARIANT: le100 ( state -- ? )  count>> 100 <= ;

M: bump ( state -- result )
    dup count>> step >>count done ;

M: choose ( state i: 0..1 -- result )  EDITS: 1
    [ choice { k 0 } ] dip upsert done ;

M: make ( state n: 1..1000 -- result )  CALLS: install  MOVES: 0
    #0a00000b00000004000004000106016e010000000800010f016e010408 swap u64be
    #00010000010000020000000000030000040000050000 cat
    pkg install done ;

L: cap ( old new req -- verdict )
    occasion>> {
        { { birth adopt invoke } [ nip le100 [ ok ] [ "over 100" refuse ] if ] }
        { { retire } [ dup le100
                       [ drop count>> 0 = [ ok ] [ "not empty" refuse ] if ]
                       [ 2drop "over 100" refuse ] if ] }
        { { write relaw } [ 2drop "frozen" refuse ] }
    } case ;
```

- **Buys.** Very short bodies; the stack effect `( state -- result )` is a method's type in one line; `step` used as a word makes the hole's context entry the top of the stack.
- **Costs.** Stack shuffling (`nip`, `dip`, `2drop`) carries no meaning a reader wants; the claim checker needs `le100` applied to `new`, which in stack form is a dataflow analysis, not a shape check; a type error surfaces at a word far from its cause.
- **Holes and supports.** `dup count>> step` hides which value fills `c`; supports stay in the declaration, outside the stack language.
- **Refusal position.** A word index in a body: `cap word 9`; precise and useless to a member.
- **Surface or printer.** A second surface for bodies only, and a poor one for this language: terms are typed trees with binders, and a stack form erases the binders the checker and the claim walk use.
- **Audience.** A Factor programmer enjoys it; von Hippel and a member do not.

## 15. Typed EDN data literal

```clojure
{:package/doc "a counter whose step is chosen in context; it makes parameter packages"
 :state      {:count :nat}
 :invariants {:le100 (<= state.count 100)}
 :claims     [[:keeps :le100 :cap]]
 :rels       {:choice {:key {:k :nat} :val :nat :limit 1}}
 :holes      [{:name       :step
               :context    [[:c :nat]]
               :type       :nat
               :select     [:choice {:k 0}]
               :candidates [{:term (+ c 1)}
                            {:term (+ c 10) :facts [[:cell #id "G"]]}]}]
 :methods    {:bump   {:body (done (with state {:count (hole :step state.count)}))}
              :choose {:arg {:i [:nat 0 1]} :edits 1
                       :body (done state (upsert :choice {:k 0} arg.i))}
              :make   {:arg {:n [:nat 1 1000]} :calls [:install] :effect {:moves 0}
                       :body (done state
                               (install (pkg (cat (u64be #hex "0a00000b00000004000004000106016e010000000800010f016e010408" arg.n)
                                                  #hex "00010000010000020000000000030000040000050000"))))}}
 :laws       {:cap {:on   [[#{:birth :adopt :invoke} (if (le100 new) :ok (refuse "over 100"))]
                           [#{:retire} (if (le100 new) (if (== old.count 0) :ok (refuse "not empty")) (refuse "over 100"))]]
                    :else (refuse "frozen")}}}
```

- **Buys.** The declaration skeleton is a map, so field order does not matter, which matches the reader's canonical sorting; any EDN or JSON tool can read the skeleton.
- **Costs.** Terms stay s-expressions inside the map, so it is two syntaxes; tagged literals (`#hex`, `#id`) need a reader extension; the wire is a binary tree codec, not EDN, so "the wire's own shape" is an analogy only.
- **Holes and supports.** `:facts [[:cell #id "G"]]` is explicit and machine-friendly; a person reads it as configuration.
- **Refusal position.** A key path: `[:holes 0 :candidates 1 :facts 0]`; exact for a tool, opaque for a member.
- **Surface or printer.** A printer for tools (a JSON export of the package skeleton for the testground and for clients); not a surface for people.
- **Audience.** A client programmer prefers it as an export; von Hippel and a member do not.

## 16. APL-style terse symbolic form

```apl
⍝ a counter whose step is chosen in context; it makes parameter packages
S      ← ⟨count:ℕ⟩
le100  ← {⍵.count ≤ 100}                                ⋄ ⊢ le100 ⊣ cap
choice ← ⟨k:ℕ⟩ ⇸ ℕ ⍤1
step   ← [c:ℕ ⊢ ℕ] choice⌷0 ⍠ (c+1) (c+10 ⊣ G)
bump   ← {⍵ ⍮ count ← step ⍵.count}
choose ← {i∊0 1 ⋄ ⍵ ⍮ choice⌷0 ← i}                     ⍝ edits 1
make   ← {n∊⍳1000 ⋄ ⍵ ⍮ ⍈ pkg A ,u64 n , B}            ⍝ calls install · moves 0
cap    ← {occ∊birth adopt invoke: le100 new ⊃ ⊤ '⊥over 100'
          occ∊retire: le100 new ⊃ (0=old.count ⊃ ⊤ '⊥not empty') '⊥over 100'
          '⊥frozen'}
A ← 0a00000b00000004000004000106016e010000000800010f016e010408
B ← 00010000010000020000000000030000040000050000
```

- **Buys.** The whole package fits in twelve lines; a reader fluent in the glyphs sees all of it at once.
- **Costs.** A glyph vocabulary nobody here knows; `⍳1000` is 1‥1000 only in APL's origin-1 convention, which is the kind of ambiguity a ledger language cannot afford; a new parser.
- **Holes and supports.** `⍠ (c+1) (c+10 ⊣ G)` is compact and unreadable to anyone not told what `⍠` means.
- **Refusal position.** A column in a dense line; a member cannot act on it.
- **Surface or printer.** An experiment in density; neither.
- **Audience.** None of the three; it shows that candidate 2's density is near the useful limit.

## Ranking

### (a) What the testground should show by default

1. **Candidate 2, the Unicode printer**, of the text the member wrote, with a one-click toggle to the raw text (candidate 1).
2. **Candidate 12, the table**, in the inspector beside it: one row per declaration with its index, and the law as a decision table where the law's shape allows it.
3. Candidate 2's view-annotated hole (✓/✗ beside each fact) whenever a check or a run has a view.

Reasons.
The source of truth stays the raw text, so refusal offsets keep pointing at what was signed and installed.
The printer adds readability without adding a second meaning.
The table answers the questions a member asks first: which method is index 1, which candidate is live, which law row refused.

### (b) What the README should be written in

1. **Candidate 13, literate**, which is what the README already is, with chunks in candidate 1 today.
2. The chunks move to candidate 2 only when the reader accepts the glyph aliases.

Reasons.
`Lang/Journey/Readme.lean` reads the README's block and runs it, so the block must be text the reader accepts.
A README in a syntax the reader does not accept would be a second, unchecked copy of the program.

### (c) What a member should be allowed to write

1. **Candidate 1**, today's surface.
2. **Candidate 1 with candidate 2's glyphs accepted as aliases**, once the alias reader and its theorem land.
3. No second grammar now.

Reasons.
Each new reader doubles the refusal vocabulary, the round-trip proof obligations and the grammar text the testground shows.
Candidates 3 to 9, 11, 14 and 16 change appearance and buy no new checking.
Candidate 10 is the exception: laws and hole candidates as clauses make the claim check and the support check syntactic over clause bodies.
That is a research question about the checker, not a syntax preference, and it deserves its own design note.
Separately from syntax, the surface needs an `invariant` declaration before any surface package can make a `keeps` claim (the finding above).

## The cheapest big win: a Unicode printer over the existing reader

### What it is

A function `Surface.pretty : SExp → String` over the tree `Read.parse` already produces.
It has two parts.
The first is a glyph table: a map from atoms and small fixed forms to glyphs (`<=` ↦ `≤`, `nat` ↦ `ℕ`, `(record (f e))` ↦ `⟨f ≔ e⟩`, `(hole u e)` ↦ `◯u[x ↦ e]`, `ok` ↦ `⊤`).
The second is a layout pass: declarations at fixed columns, a law's arms aligned on `↦`, a hole's candidates one per line with their facts right-aligned.
It needs no knowledge of types and no lowering, because it prints the member's own surface tree.
With a view, a second function annotates each fact of each candidate with ✓ or ✗ using `ob`'s existing resolution.
The printer returns, with the text, a map from each printed token to the source offset of its atom, so the testground highlights the printed token a refusal names.

### What it is not

It is not a new surface.
It is not a printer of the lowered core package: inverting the lowering is not needed and not attempted.
It does not change install, the core text, the wire, or any refusal.
The ✓/✗ marks are a rendering of a check result, never part of the source.

### Two steps, and their price

Step one, display only: the glyph table, the layout pass, the offset map, the testground toggle, and the view annotation.
The proof obligation is small and worth stating: erasing glyphs and whitespace from `pretty x` gives back the token stream of `x` (`unglyph (pretty x) ≈ x` up to `Same`).
With the glyph table a bijection on atoms and the layout whitespace only, that theorem is a lemma about the table plus `Read.parse` ignoring whitespace.
This is two days: one for the printer and the testground toggle, one for the theorem and the view annotation.

Step two, accepted input: the reader's lexer accepts each glyph as an alias of its atom.
Then the README block, the grammar window and a member's text may use the glyphs, and `read_print_surface` extends by the alias lemma.
The cost is a second spelling of each atom in the grammar text and in highlighting.
The fixed forms (`⟨f ≔ e⟩` for `(record (f e))`) are not atoms; accepting them as input is a real grammar change and belongs in a later decision.
Step two is one to two more days for atom aliases alone.

Step one is the win: every package in the testground reads like candidate 2, the source of truth does not move, and nothing a member signs changes.
