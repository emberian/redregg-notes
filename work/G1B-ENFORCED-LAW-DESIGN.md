# G1b: `law` in `.obend` is an enforced predicate (GPT-6 row G) — design

Author: DEPUTY-OB-ENG, 2026-10-07. Status: design, not built. Builds on G1 (`41ca9444`: a spec property
nothing checks is a `claim`, and a spec clause `law ...` refuses at parse) and on object-pin
(`effectiveLaw = all [pinClause pin, law]`, derived from the record, so it cannot be omitted).

## What the word means after this

`law NAME: EXPR` is a TOP-LEVEL declaration of a package (never inside a spec). It states an admission
law over the declared state of every object created from the package. Every write to that object's
state is judged by it in the kernel, on every route, before commit. Nothing that is not judged
that way may be spelled `law`.

## The fragment (exactly what compiles to `Pred`, nothing else)

The source fragment is the image of the decidable `Pred` atoms that the object judge already
evaluates over `ObjectRecord.views` (`state/<field>` slots from `stateSlots`, `request/*` from
`Facts.slots`):

    EXPR  ::= EXPR or EXPR | EXPR and EXPR | not EXPR | EXPR implies EXPR | ( EXPR ) | ATOM
    ATOM  ::= REF == INT | REF <= INT | REF in [INT, ...]
            | REF == REF | REF <= REF | REF <= REF + INT
            | monotone(FIELD) | writeOnce(FIELD)
    REF   ::= new.FIELD(.FIELD)* | request.subject | request.caller | request.height | request.turn
    INT   ::= integer literal

`FIELD` paths must name natural or boolean leaves of the object's declared state type (checked against
the package's declared `stateType` at elaboration; an unknown path refuses by name). `old.` appears only
through `monotone` and `writeOnce`, because that is all `Pred` can say about the old state. `witnessed`,
`hashEq` and `ran` are NOT in the fragment: `Pred.Sat` returns `none` for them, and ADOPT's floor check
would refuse them anyway. Anything outside the grammar refuses at elaboration with
`law outside the enforced fragment: <construct>`. There is no fallback to `claim`.

## Compilation and its theorem

`Compiler/ObjectiveBendLaw.lean` defines:

- `LawExpr`, the fragment's AST, and `LawExpr.denote : LawExpr → State → State → Bool`, its OWN
  meaning, written over the slot views and independent of `Pred`;
- `compile : LawExpr → Pred`.

The theorem is `compile_sound : ∀ e old new, Pred.eval (compile e) old new = e.denote old new`. Both
poles are needed: a planted wrong translation (for example `<=` compiled to `eq`) makes `compile_sound`
fail, and `denote` must not be defined by calling `compile`.

## Where the compiled law lives and who installs it

- Publication: the elaborated package carries `laws : List (String × Pred)` inside the published
  artifact. The artifact's identity, and therefore the pin, commits to them. They are replayed from
  source by the receiver, as the core already is: `PublicationReplay` must recompute them, and a
  tampered law refuses like a tampered core.
- `create`: `effectiveLaw r := all [pinClause r.pin, all (packageLaws r.pin), r.law]`. It is still
  DERIVED from the pin, so a creator cannot omit the package's laws. The creator's own law stays a
  further conjunct, so it can only tighten. The create seed is judged by the package laws as well.
- Upgrade: ADOPT's `next.law` is computed the same way from `next.pin`. The floor-entailment check
  (`adopt_floors_entailed`) then covers package laws, and a package law change is an upgrade like any
  other.
- Theorems on the admitting functions:
  - `package_law_enforced`: every admitted declared-state write satisfies every package law;
  - `package_law_not_removable`: no admitted turn other than ADOPT/MIGRATE changes the set.

## Open choices (mine to settle, recorded here)

1. Declare laws at top level (chosen) or on the record type. A package can export several object types
   only when the record carries an explicit `object` marker, which does not exist yet, so laws attach
   to the package's declared state type (the create's `stateType`).
2. Integer literals vs naturals: `Pred` slots are `Int`, and state fields are `Nat`/`Bool` (Bool as
   0/1). Literals are integers, and a negative bound against a Nat field is accepted and is simply
   always false or true. It is NOT refused, because refusing would bake typing into the fragment for no
   safety gain.

## Re-emits

The published artifact shape gains `laws` (an artifact/package version bump, and every package
re-publishes). The front-end identity changes. Activity COMMAND is unchanged. OBJECT-RECORD is
unchanged, since the law is derived and not stored. Worlds re-genesis because pins change.
