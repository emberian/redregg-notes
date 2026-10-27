VERDICT: RULE S9

Build S9 on (A), not (B). Do not build the card exactly as written. Five conditions, then the four answers. Base read: nanodregg `origin/main` = `ac34521` (fetched 2026-10-22). No build.

Conditions:

1. **`instanceType` wire.** One constructor whose wire is `holeInstanceType {e.text}` is legal only together with a theorem that `instantiateHoles`'s `checkE` error arm is uninhabited. `instantiateHoles_typed` is not that theorem: it is `.ok → HasType`. Until that theorem exists, the arm keeps its own constructor whose wire is exactly `holeInstanceType` (no text, no path). Reachable bytes do not move on a path the journey does not execute.
2. **One guard allowance.** The fuel `256` and the per-hole charge `256` are one bound. One field in the existing `Lang.Bounds`, used as the `run` fuel and as the coefficient in `holeCharge`. Not two names. Do not alias it with `reasonMax` or `docMax`, which are also `256` and are different facts.
3. **(A), and the empty context is named.** No `checkClosed` / `checkContextual` wrapper over the term checker. Every call passes `Ω`. A closed call is written `(Ω := [])`, not a positional `[]`.
4. **The charge merge keeps both `m`s and the floor of 1.** `holeCharge p m` is the shared formula. Actual `m` is `resolutionMax` (foldl of resolution-body nodes, init `1`). Static `m` is the existing foldl of `Term.nodes c.body` over `p.holes.flatMap (·.code)`, init `1`. The two copies are the same formula and not the same number.
5. **Do not widen the inductive to make §3's line range typecheck.** `contextualPrintMismatch` / `contextualPrintRead` stay `Except String`. `holeUnresolved`, `holeTicks`, and the `StdContextualHole` generator strings stay out. `resultName` / `refusedBy` rows stay string comparisons of the wire. `ContextualChecks.lean:97` stays a prefix check on `Refusal.program`. The two `fillBounded` rows match `ExpansionBound`, not `HoleRefusal`.

---

## (1) The refusal type

The inductive in IMPACT-S9 §1 covers every `throw` / `.error` of the live preparation path. It does not use a catch-all. It does not drop a name or a path the string carries today, except the one change the design itself names, and that change is not justified.

Mapped, from `Lang/LiveHoles.lean` at ac34521 [READ]:

| site | today | constructor | string info kept |
|---|---|---|---|
| :14 | `holeType {h.name}` | `type n` | the name |
| :15 | `holeContext {h.name}` | `context n` | the name |
| :16 | `holeCandidates {h.name}` | `candidates n` | the name. The `64` is not in the string. |
| :19 | `holeGuardType {h.name}` (`\| _ =>`, both a type error and a non-bool) | `guardType n` | same collapse the string already makes |
| :22 and :23 | `holeCandidateType {h.name} {i}`, both arms | `candidateType n i` | name and index. The `:23` arm is `\| .error _` and already drops the `TypeErr`. The string never had the path. Not a new loss. |
| :26 and :27 | `throw e.wire` for `checkShape` and `checkFields` | `package e` (`e : CheckError`) | not collapsed: the payload is the `CheckError`. `CheckError.wire` (`Lang/Package.lean:266`) is the name, the label, and for `illTyped` the `TypeErr.text`. Today the thrown string is `e.wire`, not `e.text`. The design's printer matches that. |
| :28 | `holeSignatureBound` | `signatureBound` | nothing else was in the string |
| :29 | `holeDuplicate` | `duplicate` | same |
| :32 | `holeBodyType {e.text}` | `bodyType e` | `TypeErr.text` is `name @path` (`Lang/Check.lean:83`). The path stays in the payload and in the wire. |
| :40 | `holeUnpinned` | `unpinned` | same. This string also surfaces from `changedHypotheses` (:71), `runHoleGuard` (:79) and `selectHole` (:101) via `← holeRow`. One constructor is right. |
| :73 | `holeSupportMoved {h.name} {pi.2}` | `supportMoved n i` | name and index |
| :84 / :85 | `holeGuardBlocked` / `holeGuardFault` | `guardBlocked n` / `guardFault n` | the name |
| :101–:104 | absent / type / index / derivation | the four constructors | the name. `selectionAbsent` already covers every non-`.row` leaf; the string did too. |
| :155 | `holeProvenance` | `provenance` | the string does not say which literal. The constructor doesn't either. |
| `HoleBudget.lean:84–85` | `holeWorkBound` / `holeSizeBound`, propagated bare by `←` at `LiveHoles.lean:153` and by `unresolvedBody` (`Program.lean:168`) | `ExpansionBound.work` / `.size`, then `HoleRefusal.expansion` | no name, no limit, same as the string |
| `LiveHoles.lean:159` | bare `holeInstanceType`, the `TypeErr` discarded (`\| .error _`) | `instanceType e` | **this adds `{e.text}`.** See condition 1. |
| `Program.lean:188` | `holeInstanceType {e.text}` | the same constructor | path kept, and this spelling is the one a consumer reads |

No catch-all. `package`, `bodyType`, `instanceType` embed inductives that already exist (`CheckError`, `TypeErr`). That is the right reuse, not a junk drawer.

**The unreachability claim is false.** [READ `Lang/Proofs/LiveHoles.lean:83–86`]

```
theorem instantiateHoles_typed … (h : instantiateHoles rv self Δ p = .ok i) :
    HasType Δ [] i.body p.iface ∧ Term.nodes i.body ≤ Wire.nodeMax
```

That is the success direction. The comment at `LiveHoles.lean:157` says a proof connects the recheck to contextual substitution. No theorem in the tree says the `.error` arm is empty: repo-wide, `holeInstanceType` occurs only at the bare throw, at `Program.lean:188`, and at the prefix test `ContextualChecks.lean:97` [MEASURED, grep below]. `fillHoles_typed` (`Lang/Proofs/Fill.lean:123`) would be the shape of the missing proof (each substitute has the declared type), and it is not applied to this arm.

[INFERRED] A Lean-level witness that the arm is inhabited: `Lang.Bounds.reasonMax` is `256` (`Lang/Bounds.lean:39`), `reasonOk` rejects a longer reason, and `HoleROM.name` is an unbounded `Nat` (`Lang/HoleROM.lean:25`) with no check in `HoleROM.check`. A `supportMoved` / `candidateType` string whose decimal width exceeds `reasonMax` makes `.refuse T why.toUTF8` fail `badReason`, `checkE` returns `.error`, and `admitContextual`'s prepare-error arm (`Program.lean:184`) puts the bare `holeInstanceType` on the wire as `Refusal.program`. I did not check whether the package codec can deliver a `Nat` that wide. The arm is not proved dead either way. Condition 1.

**Who reads the string.** Changing a wire string is a consumer change. The design names the bytes and the one exception; the exception's justification is the part that fails.

- The journey's executing caller reads the bytes. [READ `Lang/Journey/Contextual.lean:132–159`] `resultName == "execute: refused holeSelectionAbsent 0"`, and the same for `holeUnpinned`, `holeGuardBlocked 0`, `holeSupportMoved 0 1`, `holeDerivationMoved 0`. `ContextualReceive.lean` uses `refusedBy` on those same strings. `ContextualCycle.lean:26` builds `.refuse .bool "holeUnpinned".toUTF8`. These stay string comparisons, and they are the gate. They do not mention `holeInstanceType`.
- `Contextual.lean:145` compares `checkContextual`'s `Except String` to `"holeCandidateType 0 0"`. That one becomes a constructor. The design says so. Right.
- `Contextual.lean:159` compares `resultName` to `"holeTicks"`. That string is `Program.lean:439`, a `Refusal.program` literal, not a preparation `Except`. Leaving it out of `HoleRefusal` is right, and the row keeps reading it.
- `ContextualChecks.lean:97` is `why.startsWith "holeInstanceType"` on `Refusal.program`, and the prepare it passes returns `.ok` of an ill-typed body, so it exercises `Program.lean:188` (the with-text spelling), not the bare arm. A prefix check still passes if the bare arm grows a suffix. It does not lock the bare bytes. It must stay a wire check (condition 5), not a `HoleRefusal` match: `admitContextual` still returns `Except (Refusal D)`.
- `named` (`ContextualChecks.lean:55`) is `e == why` on `Except String`. The signature rows, `selectHole` rows, and the two `fillBounded` rows have to change type. The `fillBounded` rows (`:85–86`) compare `ExpansionBound`, because `fillBounded` itself returns `Except ExpansionBound`, not `HoleRefusal`. The print rows (`:87–88`, `Lang/Print.lean:264–267`) are a different `Except String` (`contextualPrintMismatch`, `contextualPrintRead`). §3's "lines 60–97 become constructor comparisons" swallows both. Condition 5.
- Rust does not read these strings. [MEASURED] `git grep` of the hole-refusal literals over `*.rs *.py *.json *.tsv` at ac34521 is empty. `client/` matches `refused` only as custody / follow vocabulary. No Rust change. The wire consumers are the Lean journey and `Refusal.program` / `Term.refuse` bytes.
- `StdContextualHole.lean:48–82` throws `holeSelectionKey`, `holeRootType`, `holeRootBody`, `holeImports`, `holeRootTooLarge`. Those are bundle-generation errors. `StdHole.lean` already has constructors for `.imports` and `.rootTooLarge`. Out of the live path, as the design says. Not a hole in *this* inductive. They remain law-7 debt outside S9.
- `holeUnresolved` (`Eval.lean:189`, `Program.lean:170`, and the theorems in `BigStep`, `Derives`, `LawMeaning`, `Agree`, `Sound`, `LiveTeeth`) is the machine's fault name inside a refusing body, not a preparation `throw`. Touching it would move a large statement set the design correctly refuses. `holeTicks` likewise stays a `.program` string.

Closed-admission sentinel [READ `ContextualChecks.lean:58`]: `(fun _ _ => .error "must-not-prepare-closed")` produces a string. After `prepare : … → Except HoleRefusal`, it must typecheck. It is not a wire consumer (`holes.isEmpty` returns before `prepare`). Do not add a constructor for it.

## (2) The signature fork — rule (A)

**(A).** One checker. The default `(Ω : HoleSignature := [])` comes off `inferE`, `inferFields`, `inferArms`, `inferSubst`, `infer`, `checkE`, `check` (`Lang/Check.lean:90,186,196,212,225,228,234`). Law 1: a second name is a second shape. The charter's rule for an existing thing is to delete the old shape, not to keep both. (B)'s `checkClosed := checkE · · · []` is a second name over one core, and it is how the two drift: the wrapper is the one a later edit "just adjusts". The design's objection is right, and the count it leans on is real: the closed checker lemmas are applied at `(Ω := [])` thirteen times, `Lang/Proofs/Check.lean:314–359` [MEASURED, the thirteen lines are listed in the spot-check]. Restating those over `checkClosed` buys a name and a place for the two to diverge.

**How a reader sees that the context is empty.** Not by a positional `[]`. `inferE Δ Γ t Ω` already takes two list arguments before the term (`Δ` and `Γ`). The journey probe that *shows* the split is `inferE [] [] termHole` versus `inferE [] [] termHole sig` (`ContextualChecks.lean:63`). After the default dies, a positional reading is `inferE [] [] termHole []`: three empty lists, and only the last one is the hole signature. The closed/contextual split is visible when the parameter is named: `(Ω := [])` against `(Ω := holeSignature p.holes)` (the one call that already does this, `LiveHoles.lean:31`) or `(Ω := sig)`. `checkE` at the invocation boundary (`LiveHoles.lean:158`) is today the hidden closed call — `checkE Δ body p.iface` with the default. It becomes `checkE Δ body p.iface (Ω := [])`. That is the whole of the visibility. `HoleSignature` is `List (HoleDecl …)` (`Check.lean:22`); `[]` is the empty signature, and the name `Ω` is what says so.

The design's "closed callers write `[]`" is accepted only in that named form. That is still (A): no second function, no default.

The `141` / `12` files figure is exact [MEASURED, spot-check]. The `27` is not. `git grep -c 'Ω :=' ac34521 -- Lang/Proofs/Check.lean` is 27 lines, and those lines include `HasType (Ω := Ω)` and the thirteen `(Ω := [])` lemma applications, not 27 of the 141 checker occurrences. The checker calls that already pass `(Ω := …)` are 31: 21 recursive calls in `Lang/Check.lean`, 9 in `Lang/Proofs/Check.lean`, and `LiveHoles.lean:31`. The conclusion the design draws still holds: most call sites omit `Ω` and mean closed by default. The number does not.

Elaborated statements of callers that already meant `[]` stay the same once they write `(Ω := [])`. I did not re-elaborate (no build). [INFERRED from Lean's default-argument elaboration, and from the design's own census gate.] That is not a condition. The census gate as written ("TYPE changes ⊆ §3") is a theorem-type gate; the `def`s' own types are supposed to change. Don't let a declaration-wide digest fail the card for `checkContextual`'s type moving.

## (3) The statement price

The 33 names are real, they add up (15+5+7+2+1+1+1+1), and each change is a re-spelling. None gains a premise. None changes what is claimed, provided condition 1 holds and the new `Bounds` fields are definitionally the old numerals.

Re-spelling, not a new fact:

- **Error type only, same proposition.** `holeRow_authenticated`, `selectHole_origin`, `selectHole_nodes`, `checkContextual_shape`, `instantiateHoles_typed`, `instantiateHoles_sources`, `instantiateHoles_cost` (the inequality stays `i.cost ≤ p.preparationCost`; `HoleInstance` mentions `HoleResolution`, whose `blocked` payload moves `String → HoleRefusal`), `resolutionMax_committed`, `admitContextual_inv`, `admitContextual_closed`, `admitContextual_lits`, `load_closed_live`, `loadAll_closed_live`, `loadUsing_leaf_closed`, `fillBounded_bounds` (`Except String → Except ExpansionBound`; the node bounds stay), `unresolvedBody_field`, `loadContextual_top`, and the six `DeployedContextual` successes (`selected_uses_context`, `strengthening_factor`, `strengthening_uses_argument`, `kept_context`, `alternative_same_filling`, `replacement_filling`). `strengthening_factor`'s proof says `Except.ok (ε := String)` (`LiveJourney.lean:58`); that is a proof edit, and the statement's meaning (the ok tuple, including `inferE [] s.context s.filling = .ok .nat`) is the same once `Ω` is explicit.
- **`why : String` becomes `why : HoleRefusal`, and the bytes are `why.wire`.** `blocked_has_no_receipt`, `resolveHole_refusal` (`LiveHoles.lean:70–72`, today `why.toUTF8`), `blocked_step` (`:77–79`). The domain of `why` shrinks from every string to the inductive. That is law 7, not a new premise. The claim "the machine faults with those bytes" is the same claim iff `wire` reprints today's string.
- **One string equality becomes one constructor.** `used_hypothesis_suspends` (`LiveJourney.lean:93–96`) is `.error "holeSupportMoved 0 1"`. It becomes `.error (.supportMoved 0 1)`. Same refusal. The wire row at `Contextual.lean:151` still checks the characters, so the printer and this theorem have to agree. No new premise.
- **A literal becomes its name.** `runHoleGuard_cost` (`LiveHoles.lean:120`) is `used ≤ 256`. Same bound iff `holeGuardFuel = 256`. The proof applies `run_used_le` at fuel `256` (`:127`); that occurrence moves with the name. `instantiateHoles_cost`'s proof (`:368`, `:382`) mentions `256 * p.holes.length` and lines the two formulas up with `Nat.add_comm`. The statement does not change its inequality.

`loadLive_checked`, `loadLive_libTy`, `loadLive_of_load`, `method_live_run_sound`, `invoke_live_never_stuck` are in the 33, but `loadLive`'s written type is `Except (Refusal D) (Loaded × Nat)` (`Program.lean:207`) and does not mention `String`. Their statements may not move. The gate is ⊆, so a superset is safe. I am not calling them meaning changes. They do not gain a premise. [READ the statements; INFERRED that a type-only census will not flag them unless it follows `loadLive`'s body.]

**Nothing that compares a preparation-refusal string is missing.** [MEASURED] Every `Except String Term` prepare binder in `Lang/Proofs` is one of: `admitContextual_closed` (`LiveClosed.lean:29`), the section variable of `load_closed_live` / `loadAll_closed_live` (`:37`), `loadUsing_leaf_closed` (`:209`), `admitContextual_inv` (`LiveHoles.lean:135`), `admitContextual_lits` (`Provenance.lean:610`). All five are in the list. The only theorem whose statement equates a preparation error to a string is `used_hypothesis_suspends`, and it is in the list. `why : String` on `HoleResolution.blocked` is the three theorems above, all in the list.

The `holeUnresolved` theorems (`LawMeaning.lean:36,333,360`, `BigStep.lean:50`, `Derives.lean:36`, `Sound.lean:278`, `Agree.lean:232`, `LiveTeeth.lean:156–197`) compare a string S9 does not change. They should stay off the list. Sweeping them in would be a meaning change the card does not own.

Generated `HoleResolution.blocked.inj` / `injEq` / `sizeOf_spec` move because the payload moves. Same re-spelling. `selected`'s generated lemmas do not have a `String` payload; leave them out unless the elaborator says otherwise.

Kernel, Ledger, Hosting: no mention of `checkContextual`, `instantiateHoles`, `fillBounded`, `unresolvedBody`, `HoleResolution`, `admitContextual` [MEASURED, empty grep]. The design's "no Kernel/Ledger TYPE change" holds on the source. `judgeOneContextual_leaf_closed` and `runMeasuredLive_leaf_closed` cite `unresolvedBody` / `instantiateHoles` only inside the proof (`LiveClosed.lean:229,261`), not in the statement. A Kernel proof that only uses those statements does not gain a premise from S9.

## (4) One charge — the two copies are the same formula, not the same number

[READ both, quoted in the spot-check.]

Actual, `instantiateHoles`, `LiveHoles.lean:162–164`, with `rs := p.holes.map (resolveHole …)` at `:151` so `rs.length = p.holes.length`:

```
if p.holes.isEmpty then 0 else
  Term.nodes p.body * (resolutionMax rs + 1) + 256 * rs.length
```

`resolutionMax` (`:137–138`) is `foldl (fun n r => max n (Term.nodes r.body)) 1`.

Static, `Package.preparationCost`, `Program.lean:212–216`:

```
if p.holes.isEmpty then 0 else
  Term.nodes p.body * (1 + foldl (fun n c => max n (Term.nodes c.body)) 1 over p.holes.flatMap (·.code))
  + 256 * p.holes.length
```

Same formula: empty → `0`, else `nodes(body) * (1 + m) + 256 * length`, and both folds start at `1`. `(m + 1)` versus `(1 + m)` is `Nat.add_comm`, which `instantiateHoles_cost` already uses (`LiveHoles.lean:382`). Not a defect. Not two charges to average together.

They are not the same number, and they must not become one. Actual `m` is the max node count of *resolution bodies* (a selected body, or a 1-node `.refuse`). Static `m` is the max node count of *every committed candidate body*. `selectHole_nodes` (`:301`) and `factorHole_nodes` (`:297`) show a selected body's node count equals the candidate's, so a selected `m` is one of the static candidates. A blocked body is `Term.nodes (.refuse _ _) = 1` (`HoleBudget.lean:8`), and the fold's floor is `1`. `resolutionMax_committed` (`:340`) is `actual m ≤ static m`. `instantiateHoles_cost` is `i.cost ≤ p.preparationCost`. The design's `holeCharge p m` with two call sites is the faithful merge. Condition 4 is only: "max over the committed code" means that foldl, init `1`, not `List.maximum?` which is `0` on an empty code list (today an empty code list still contributes `m = 1`, multiplier `2`).

The two `256`s are the guard allowance (fuel at `:82`, charge coefficient at `:162` and `:216`). One field (condition 2). `reasonMax = 256` and `docMax = 256` in `Lang/Bounds.lean:39` and `:52` are other facts. `Lang.Bounds` already exists (`:12`); the new names go there, not in a second record. `methodsMax = 64` and `importsMax = 16` (`Package.lean:230–231`) are the same numerals as the hole bounds and are not those bounds. `holeCandidatesMax` and `holeSignatureMax` as new names are right; reusing `methodsMax` / `importsMax` would be a false merge.

---

## Spot-checks

All against `ac345215f386e83287b6736f06d327ee9bdc8214`. Commands run with `git --git-dir=/Users/ember/dev/nanodregg/.git` so the sandbox would allow them. Outputs trimmed only where noted.

### S1. Every live `throw` is in §1

```
git grep -n -E 'throw |\.error ' ac34521 -- Lang/LiveHoles.lean Lang/HoleBudget.lean
```

`LiveHoles.lean`: lines 14, 15, 16, 19, 22, 23, 26, 27, 28, 29, 32, 40, 73, 84, 85, 101, 102, 103, 104, 155, 159. `HoleBudget.lean:84–85`. Each row of §1's table hits one of these, and each of these hits a row. `Program.lean:188` (the with-text `holeInstanceType`) and `Program.lean:168` (`unresolvedBody` → `fillBounded`) are the two sites outside those files. `Program.lean:439` `holeTicks` is the budget string §1 excludes; confirmed present, confirmed not a `HoleRefusal` site.

### S2. The bare spelling has no exact consumer

```
git grep -n 'holeInstanceType' ac34521 -- '*.lean' '*.rs' '*.py' '*.json' '*.md'
```

Three hits: `LiveHoles.lean:159` (`throw "holeInstanceType"`), `Program.lean:188` (`s!"holeInstanceType {e.text}"`), `ContextualChecks.lean:97` (`why.startsWith "holeInstanceType"`). No `== "holeInstanceType"`. No Rust hit (the `*.rs` grep for the whole refusal vocabulary returned empty).

### S3. The 141, and the 27 that isn't

```
git grep -o -w -E 'inferE|inferFields|inferArms|inferSubst|checkE' ac34521 -- '*.lean' | wc -l
→ 141
```

Twelve files: `Lang/{Check,LiveHoles,Package,Program,Resident,StdActivity}.lean`, `Lang/Journey/ContextualChecks.lean`, `Lang/Proofs/{Check,LiveJourney,Print,PrintWire,StdFits}.lean`. That is 6 + 1 + 5, as claimed.

```
git grep -o -E '(inferE|inferFields|inferArms|inferSubst|checkE) \(Ω :=' ac34521 -- '*.lean' | wc -l
→ 30
```

plus the trailing form `checkE Δ p.body p.iface (Ω := holeSignature p.holes)` at `LiveHoles.lean:31`, which that prefix pattern misses. 31, not 27.

```
git grep -n 'Ω :=' ac34521 -- Lang/Proofs/Check.lean | wc -l
→ 27
```

Those 27 lines run 15, 151, 161, 205, 231, 237, 252, 258, 261, 264, 269, 274, 288, 291, then the thirteen closed applications 314, 319, 324, 327, 332, 337, 340, 343, 346, 349, 353, 356, 359 (`inferE_sound_live (Ω := [])` through `check_iff_live (Ω := [])`). The thirteen is the design's "13 closed checker theorems", and that part is exact.

### S4. The 33, and the string-comparing theorems

Prepare binders, whole of `Lang/Proofs`:

```
git grep -n 'Except String Term' ac34521 -- 'Lang/Proofs/*.lean' 'Lang/Proofs/**/*.lean'
```

`LiveClosed.lean:29,37,209`, `LiveHoles.lean:135`, `Provenance.lean:610`. All named in §3.

```
git grep -n 'holeSupportMoved' ac34521 -- 'Lang/Proofs/*.lean'
→ Lang/Proofs/LiveJourney.lean:96    .error "holeSupportMoved 0 1"
```

That is `used_hypothesis_suspends`, in §3. No other proof statement equates a preparation refusal to a string. `holeUnresolved` hits are the excluded set (`Agree`, `BigStep`, `Derives`, `LawMeaning`, `Sound`, `LiveTeeth`).

`git grep -l` of `checkContextual|instantiateHoles|fillBounded|unresolvedBody|HoleResolution|admitContextual` over `Kernel`, `Ledger`, `Hosting` at ac34521: empty.

### S5. The two charge copies

`resolutionMax` and the actual cost (`LiveHoles.lean:137–164`):

```
def resolutionMax (rs : List HoleResolution) : Nat :=
  rs.foldl (fun n r => max n (Term.nodes r.body)) 1
…
let rs := p.holes.map (resolveHole rv self)
…
| .error _ => throw "holeInstanceType"
| .ok () =>
  pure ⟨body, ss, rs, if p.holes.isEmpty then 0 else
    Term.nodes p.body * (resolutionMax rs + 1) + 256 * rs.length⟩
```

`Package.preparationCost` (`Program.lean:212–216`):

```
def Package.preparationCost (p : Package) : Nat :=
  if p.holes.isEmpty then 0
  else Term.nodes p.body *
    (1 + (p.holes.flatMap (fun h => h.code)).foldl
      (fun n c => max n (Term.nodes c.body)) 1) + 256 * p.holes.length
```

Same formula, two `m`s, both floors `1`, both coefficients `256`. `instantiateHoles_cost` proves `≤`, not `=`.

### S6. Charter laws the card is answering

`git show origin/main:CHARTER.md`, laws 1, 4, 7: one of everything (a second shape is a defect); a static bound on everything, in `Bounds`; every refusal a constructor with a name on the wire. `Lang/Bounds.lean` is already that record for the language (`stackMax`, `reasonMax = 256`, `docMax = 256`). The inline hole bounds are the four the design names, and only those, in the live path: `≤ 64` (`LiveHoles.lean:16`), `≤ 16` (`:28`), fuel `256` (`:82`), charge `256` (`:162` and `Program.lean:216`), plus the theorem/proof copies at `Proofs/LiveHoles.lean:120,127,368,382`.
