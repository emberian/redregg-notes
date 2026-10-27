# Eight surfaces for Objective Bend

ASTRA · 2026-10-27

I would build a declarative package header with expression bodies as the authoring language.
I would make the testground open on a member-facing view of that package and its pinned context.
I would retain the s-expression reader as the exact interchange surface.
These are three presentations of one language.

## The comparison

Every main example below renders the complete counter from the README's “One program.”
The examples retain its documentation string, state, relation, two candidates, three methods, generator bytes, and law.
The generator bytes appear in full in every rendering.
`#G` has the README's meaning: replace it with the grant's actual id before reading the package.
None of the eight proposed spellings is implemented by this memo.

The README's counter has no carried claim.
It has no explicit effect entry.
Its relation holds a natural selection index rather than value.
Adding these declarations would change its package identity.
Each alternative therefore includes a separate feature probe for claims, grades, and held value.
Those probes are schematic fragments outside the counter.
`INV` and `LAW` in a probe name actual interface fields in the package being described.
They are not new logical variables in Objective Bend.

All authoring alternatives use the current surface's defaults unless they explicitly show a field.
An omitted method argument is the empty record.
An omitted read set is empty.
An omitted slot count is zero.
An omitted grade has effective bound `moves 0`.
An omitted grade entry must remain absent in the encoded package.
Printing an explicit zero entry in its place would break exact round trips.

The proposed expression forms lower to the existing terms.
`done` constructs a result containing suspended fields.
An edit inside that result does not immediately mutate a row.
An `install` item returns a call containing bytes.
It does not execute an installation while evaluating the expression.
Every `with` below uses the current surface's expansion.
The sequence of edits and calls determines their respective slot orders.

The distinctions that the notation must preserve are small enough to state directly.
The context `Ψ` is an ordered context of typed term variables.
Candidate supports are facts about the caller's pinned World view.
A hypothesis attaches an optional support to one position of `Ψ`.
These are three different things.
A hole guard sees the Boolean `present` for its own optional pin.
It does not acquire an arbitrary query interface to the World.

The installed package commits the candidate list.
The selection row stores an index into that list.
Invocation preparation resolves the holes against the caller's pins.
A blocked resolution becomes a typed refusal term.
The refusal ends the run only when evaluation demands that term.
Repair writes a different selection through an admitted method call.
There is no automatic fallback to candidate 0.

A grade bounds the amounts in returned transfer and credit calls.
It is not a tick budget.
Held value requires backing movements into and out of the object's account.
It is not a balance annotation on a natural.
`keeps INV LAW` is encoded in package identity.
Its admission check recognizes a particular term shape.
An equivalent Boolean expression does not automatically satisfy that check.
In particular, attaching a claim to the README's inline comparison is not a complete implementation of a claim.

Every proposal preserves metering by preserving the lowered term.
Pretty syntax must not introduce runtime helper applications merely to factor repeated text.
Such applications can change both ticks and the shape inspected by the claim checker.
Byte generation, hole preparation, field extraction, and ordinary evaluation keep their existing charges.
Invocation budgets remain request data.
Law and guard budgets remain runtime bounds.

## 1. Contextual judgments

The principle is to make the contextual judgment the most prominent declaration.
The brackets mark an open term with an explicit context.
The `under` clause names World supports outside that context.

```text
package
  doc "a counter whose step is chosen in context; it spawns parameter packages"
  state : {count : nat}
  relation choice : key {k : nat} => nat limit 1

  step :: [· ⊢ nat]
    selection = choice[{k = 0}]
    candidate 0 = [· ⊢ 1]  under {}
    candidate 1 = [· ⊢ 10] under {cell #G}

  method bump =
    done (state with {count = state.count + step⟨⟩})

  method choose (arg : {i : nat}) edits 1 =
    done state [upsert choice {k = 0} arg.i]

  method spawn (arg : {n : nat}) calls [install] =
    done state [install {pkg =
      cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
          #00010000010000020000000000030000040000050000)}]

  law cap : old, new, req ⊢ Verdict
    adopt | birth | invoke ⇒
      if new.count <= 100 then ok else refuse "over 100"
    retire ⇒ if old.count == 0 then ok else refuse "not empty"
    otherwise ⇒ refuse "frozen"
end
```

`step⟨⟩` is the hole under the empty substitution.
A nonempty use is `step⟨e₀, e₁⟩`.
A contextual binder can read `x : nat @ row rates {k = 0} version 7`.
Its support belongs to that binder rather than to every candidate.
The candidate's separate `under` list is always required to hold.
A declaration can add `guard cell #G => present`.
The numerals following `candidate` assert consecutive list positions.
They do not create arbitrary candidate ids.

This makes substitution, strengthening, and candidate scope easy to inspect.
It makes the common empty-context case look more formal than its computation.
The notation also risks suggesting that a support is a proof term supplied by the programmer.
The runtime still checks the support against pins.

A refusal would display `step / candidate 1 / support cell:G` beside `holeSupportDead 0 cell:G`.
The first label is a proposed presentation path.
The second text retains the runtime's name and coordinate.
The view would highlight `cell #G` and link every use of `step⟨⟩`.
It would not claim to know which use was demanded without execution evidence.

The feature probes read `claim keeps INV LAW`, `method pay … moves <= 5 = …`, and `relation escrow : key {k : nat} => {give : {amount : nat, asset : digest}} limit 8 holds give`.
The claim remains a package declaration.
The grade remains attached to a method.
The held leg remains attached to a relation value field.

This is an authoring reader.
It needs a bracket-aware lexer, expression precedence, and scope handling for contextual binders.
Its main proof burden is ordered substitution through the named context.
A total printer also needs an explicit core form for bodies that do not match these declarations.
Its cost is medium to high.

## 2. Addressed outlines

The principle is to give every consequential clause a visible address.
The outline is also the shape of the diagnostic navigator.
An address beginning with `@` is source metadata.
It does not enter package bytes.

```text
package:
  doc: "a counter whose step is chosen in context; it spawns parameter packages"
  state: {count: nat}

  relation choice @relation.choice:
    key: {k: nat}
    value: nat
    limit: 1

  hole step @hole.step:
    context: []
    result: nat
    selection @selection: choice[{k = 0}]
    candidate 0 @base:
      term: 1
      supports: []
    candidate 1 @ten:
      term: 10
      supports:
        @grant: cell #G

  method bump @method.bump:
    body: done (state with {count = state.count + hole step()})
  method choose @method.choose:
    arg: {i: nat}
    edits: 1
    body: done state [upsert choice {k = 0} arg.i]
  method spawn @method.spawn:
    arg: {n: nat}
    calls: [install]
    body: done state [install {pkg =
      cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
          #00010000010000020000000000030000040000050000)}]

  law cap @law.cap:
    on [adopt, birth, invoke] @count:
      if new.count <= 100 then ok else refuse "over 100"
    on retire @empty:
      if old.count == 0 then ok else refuse "not empty"
    else @frozen:
      refuse "frozen"
```

The hole is an explicit record of context, result, selection, and candidates.
Supports have individual addresses within a candidate.
A supported binder would have its own `hypothesis:` field.
A guarded hole would add `guard: {pin: cell #G, body: present}`.
This makes missing pins distinguishable from missing selection rows without reading an expression tree.

The refusal position would be `@hole.step/@ten/@grant`, qualified by the package id and source document.
Changing whitespace would leave that position intact.
Renaming an anchor would change only the source map.
Reordering candidates would still change candidate indices and package bytes.
The system must never treat anchors as wire identities.

This makes large generated declarations easy to navigate.
It makes small expressions occupy substantial vertical space.
The authored anchors also need duplicate detection and scoped lookup.
Stable addresses solve a diagnostic problem rather than a computation problem.

The feature probes are `claim: keeps INV LAW`, a method field `effect: {moves: 5}`, and a relation field `holds: give` beside `value: {give: {amount: nat, asset: digest}}`.
A refusal of a carried claim can point to its declaration immediately.
A more precise location inside the law needs a checker path that the current claim refusal does not supply.

This is an authoring reader.
It needs layout tokens and an expression parser.
Anchor preservation belongs to source round trips rather than package round trips.
A canonical printer can regenerate anchors from structural paths.
The package theorem then ignores anchor spelling.
Its cost is medium.

## 3. Review rows

The principle is to make a law change a row change.
Every occasion gets its own row.
The syntax refuses a missing occasion.
The syntax has no default arm.

```text
package {
doc = "a counter whose step is chosen in context; it spawns parameter packages";
state = {count: nat};

relation | key      | value | limit
choice   | {k: nat} | nat   | 1;

hole | context | result | selection
step | []      | nat    | choice[{k = 0}];

candidate | body | supports
step[0]   | 1    | []
step[1]   | 10   | [cell #G];

method | arg      | reads | edits | calls     | body
bump   | {}       | []    | 0     | []        |
  done (state with {count = state.count + hole step()})
choose | {i: nat} | []    | 1     | []        |
  done state [upsert choice {k = 0} arg.i]
spawn  | {n: nat} | []    | 0     | [install] |
  done state [install {pkg =
    cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
        #00010000010000020000000000030000040000050000)}];

law | occasion | body
cap | adopt    | if new.count <= 100 then ok else refuse "over 100"
cap | birth    | if new.count <= 100 then ok else refuse "over 100"
cap | invoke   | if new.count <= 100 then ok else refuse "over 100"
cap | relaw    | refuse "frozen"
cap | retire   | if old.count == 0 then ok else refuse "not empty"
cap | write    | refuse "frozen";
}
```

The bars are delimiters rather than alignment requirements.
A continuation after a body's bar belongs to that body until the next row header.
Strings and bracketed expressions protect their own delimiters.
The displayed column widths carry no meaning.

The hole table separates the selection source from the candidate table.
Its supports remain attached to a particular candidate row.
Context entries would use `{name: x, type: nat, hypothesis: cell #G}`.
A guard would be another column with explicit pin and Boolean body.

This makes changes to adoption and law replacement easy to compare.
It makes a law's complete act coverage visible in one block.
It makes a deeply nested method body awkward to edit.
It also duplicates the counter's shared comparison three times.
That duplication is deliberate in a review representation.

A refusal would point to `law[cap,retire].body.else` for the corresponding source branch when that branch is known.
A hole refusal would point to `candidate[step,1].supports[0]`.
The runtime's existing coordinate remains visible alongside that row address.

The feature probes add a `claim | invariant | law` table containing `keeps | INV | LAW`, an `effect | moves` table containing `pay | 5`, and a `holds` column containing `give` on a relation whose value contains a leg field named `give`.
The effect table contains only actual entries.
An effective default is displayed in a separate annotation.

This is primarily a printer for review.
A reader for its canonical format is feasible.
It needs table framing, nested-expression boundaries, and duplicate-row checks.
Its law reconstruction is cheap because the core already has one arm per occasion.
Its general package printer still needs constructor expressions for bodies outside the method-and-law pattern.
Its cost is low for a view and medium for a reader.

## 4. Member cards

The principle is to show what a member can invoke and what can refuse it.
The package's own assertions are separated from observations about a particular invocation.
The example below is the full static card before a view has been supplied.

```text
PACKAGE
  Says: "a counter whose step is chosen in context; it spawns parameter packages"
  State: count : nat
  Carried claims: none
  Explicit grades: none

RELATION choice
  Key: {k : nat}
  Value: nat
  Row limit: 1
  Sum column: none; cap: 0
  Retraction: disabled
  Guard: none
  Held value: none

OPEN DECISION step : [empty context |- nat]
  Selection comes from: choice at {k = 0}
  Candidate 0 returns: 1
    Supports: none
  Candidate 1 returns: 10
    Supports: cell #G must be live in the caller's pinned view
  Guard pin: none
  Guard body: true
  Current selection: no view supplied

METHOD bump
  Argument: {}
  Reads: none; edit slots: 0; call slots: 0
  Value movement bound: 0, by omission
  Result: done (state with {count = state.count + hole step()})

METHOD choose
  Argument: {i : nat}
  Reads: none; edit slots: 1; call slots: 0
  Value movement bound: 0, by omission
  Result: done state [upsert choice {k = 0} arg.i]

METHOD spawn
  Argument: {n : nat}
  Reads: none; edit slots: 0; call slots: 1 of kind install
  Value movement bound: 0, by omission
  Result: done state [install {pkg =
    cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
        #00010000010000020000000000030000040000050000)}]

LAW cap
  adopt:  if new.count <= 100 then ok else refuse "over 100"
  birth:  if new.count <= 100 then ok else refuse "over 100"
  invoke: if new.count <= 100 then ok else refuse "over 100"
  relaw:  refuse "frozen"
  retire: if old.count == 0 then ok else refuse "not empty"
  write:  refuse "frozen"
END PACKAGE
```

The hole reads as a decision whose available fillings are already committed.
The selected index is a separate observation.
When a view is supplied, the card shows its identity next to that observation.
Each support gets one of the states observed-live, observed-failing, or unpinned.
The labels distinguish an absent selection from a selection whose support failed.
A guard result is another observation.
A contextual binder has a type and a separately displayed hypothesis.

This makes revocation and repair easy to understand.
It makes the exact term tree harder to scan.
The full expression remains available because a summary cannot determine execution order by itself.
The static card must not call candidate 1 “available” before a pinned view has been checked.
The `choose` card must not promise that selecting an index makes that candidate usable.

A refusal would highlight `OPEN DECISION step → Candidate 1 → cell #G`.
The detail line would retain `holeSupportDead 0 cell:G`.
A link would open the corresponding source span when the package has associated source.
Otherwise the link would open the core path.
The card would offer the `choose` method as the repair action.
It would not invoke that method automatically.

The feature probes display `Carried claim: keeps INV LAW`, `Declared value movement bound: 5`, and `Each row holds: give.amount of give.asset in this object's account`.
The claim card also names whether installation admitted the package.
Reading unattested bytes is not evidence that a claim was admitted.

This is a printer and interactive view.
I would not accept its prose as source code.
Its cost is low to medium because there is no new language parser.
The correctness task is provenance for every displayed fact.
The exact export remains the existing core printer.
The view needs a generic fallback for arbitrary terms and unrecognized generators.
It must never invent a high-level activity merely because a body resembles one.

## 5. Constructor blocks

The principle is to expose the package tree's structure with named fields and readable binders.
This is the diagnostic view closest to the encoded object.
It exposes the empty tables that the authoring surface omits.
The aliases below are textual type abbreviations local to this listing.
They introduce no runtime terms.
`record {}` constructs suspended record fields.
`inject T tag value` retains the sum annotation that the core requires.

```text
types {
  U = rec {};
  S = rec {count: nat};
  K = rec {k: nat};
  AChoose = rec {i: nat};
  ASpawn = rec {n: nat};
  V = sum {ok: U, refused: bytes};
  Q = rec {
    agent: digest,
    caller: sum {none: U, some: digest},
    notBefore: nat,
    occasion: sum {adopt: bytes, birth: U, invoke: nat,
                   relaw: bytes, retire: U, write: U},
    principal: digest, self: digest, validUntil: nat
  };
  EditRow = rec {key: K, val: nat};
  ChoiceEdit = sum {insert: EditRow, upsert: EditRow};
  E = sum {choice: ChoiceEdit};
  OE = sum {none: U, some: E};
  Install = sum {install: rec {pkg: bytes}};
  OInstall = sum {none: U, some: Install};
  RBump = rec {calls: U, edits: U, state: S};
  RChoose = rec {calls: U, edits: rec {e0: OE}, state: S};
  RSpawn = rec {calls: rec {c0: OInstall}, edits: U, state: S};
}

package {
  imports = [];
  doc = "a counter whose step is chosen in context; it spawns parameter packages";
  state = S;
  iface = rec {
    bump: U -> S -> U -> Q -> RBump,
    cap: S -> S -> Q -> V,
    choose: U -> S -> AChoose -> Q -> RChoose,
    spawn: U -> S -> ASpawn -> Q -> RSpawn
  };
  methods = [bump, choose, spawn];
  laws = [cap];
  rels = {
    choice: {key: [(k, nat)], val: nat, limit: 1,
             sum: none, cap: 0, retract: false, guard: none, holds: none}
  };
  body = record {
    bump = lambda rows: U, state: S, arg: U, req: Q =>
      record {calls = record {}, edits = record {},
              state = record {count = add(state.count, hole(0, []))}};
    cap = lambda old: S, new: S, req: Q =>
      case req.occasion {
        adopt _ => if le(new.count, 100)
          then inject V ok (record {}) else inject V refused "over 100";
        birth _ => if le(new.count, 100)
          then inject V ok (record {}) else inject V refused "over 100";
        invoke _ => if le(new.count, 100)
          then inject V ok (record {}) else inject V refused "over 100";
        relaw _ => inject V refused "frozen";
        retire _ => if eq(old.count, 0)
          then inject V ok (record {}) else inject V refused "not empty";
        write _ => inject V refused "frozen";
      };
    choose = lambda rows: U, state: S, arg: AChoose, req: Q =>
      record {calls = record {}, edits = record {
        e0 = inject OE some (inject E choice (inject ChoiceEdit upsert
          (record {key = record {k = 0}, val = arg.i})))
      }, state = state};
    spawn = lambda rows: U, state: S, arg: ASpawn, req: Q =>
      record {calls = record {
        c0 = inject OInstall some (inject Install install (record {pkg =
          cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
              #00010000010000020000000000030000040000050000)}))
      }, edits = record {}, state = state};
  };
  effects = [];
  claims = [];
  holes = [{
    name: 0, context: [], result: nat,
    selection: {relation: 0, key: #0000000000000000},
    hypotheses: [], guardPin: none, guard: true,
    code: [{body: 1, supports: []},
           {body: 10, supports: [cell #G]}]
  }];
}
```

The hole's name is visibly a numeric field.
Its candidate list is visibly ordered.
The relation key is visibly encoded data.
This removes any suggestion that `step` is a wire-level name.
The original source name belongs in an optional gutter annotation.

This makes identity changes and codec investigations easy to inspect.
It makes ordinary programming laborious.
The counter is already long enough to demonstrate why the authoring surface derives method types.
The type aliases reduce repetition without hiding any definition.
A printer can expand every alias independently.

A refusal would name `holes[0].code[1].supports[0]` and the support's wire coordinate.
A type error would navigate `body.choose` through its binders and result fields.
Every displayed leaf has a corresponding package field or term position after alias expansion.

The feature probes are `claims = [keeps(INV, LAW)]`, `effects = {pay: {moves: 5}}`, and a relation record with `holds: some(give)` and the corresponding leg value type.
The constructor form can represent the invariant's ordinary interface field directly.
No special invariant declaration is needed.

This is a reader and an exact printer.
It is a symbolic view of the package tree rather than a claim that braces are the binary wire format.
It needs only constructors, scoped names, and type aliases.
It does not need type inference or reverse engineering of authoring sugar.
Its round-trip proof is structurally close to the existing core proof.
Alias expansion and fresh binder naming are its main additions.
Its cost is medium initially and low per new core constructor.

## 6. Dafny-shaped declarations

The principle is to give verification-oriented programmers familiar declaration boundaries.
Methods have argument records and explicit results.
Laws have named act cases.
This borrows a reading style rather than Dafny's semantics.

```text
package {
  doc "a counter whose step is chosen in context; it spawns parameter packages";
  state { count: nat }
  relation choice key {k: nat} value nat limit 1;

  hole step() returns nat {
    selection choice[{k = 0}];
    candidate 0 supports [] { 1 }
    candidate 1 supports [cell #G] { 10 }
  }

  method bump() {
    return done(state with {count = state.count + hole step()});
  }

  method choose(arg: {i: nat})
    edits 1;
  {
    return done(state, upsert(choice, {k = 0}, arg.i));
  }

  method spawn(arg: {n: nat})
    calls [install];
  {
    return done(state, install({pkg =
      cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
          #00010000010000020000000000030000040000050000)}));
  }

  law cap(old, new, req) {
    on adopt, birth, invoke {
      if new.count <= 100 { ok } else { refuse "over 100" }
    }
    on retire {
      if old.count == 0 { ok } else { refuse "not empty" }
    }
    otherwise { refuse "frozen" }
  }
}
```

A hole's parameter list is its contextual telescope.
The empty parentheses are an empty context rather than a function call convention.
A candidate is checked under those parameters.
Its `supports` clause is part of the committed candidate.
A supported parameter can read `x: nat supported by cell #G`.
The optional hole guard reads `guard(cell #G) { present }`.

This makes method signatures and record expressions familiar.
It makes the contextual distinction easy to miss because holes resemble methods.
The explicit `hole` keyword at each use prevents that distinction from disappearing entirely.
The statement-like body also invites an imperative reading of `upsert`.
Here `return done` is one expression with result items.
The design introduces no general statement execution or mutable local variables.

A refusal would point to `hole step / candidate 1 / supports[0]` with an ordinary line and column.
A law refusal would open the named act block when the occasion is available.
The existing refusal reason would remain the primary diagnostic text.

The feature probes read `claim keeps INV LAW;`, `method pay … moves <= 5;`, and `relation escrow key {k: nat} value {give: {amount: nat, asset: digest}} limit 8 holds give;`.
I would not spell a claim `ensures INV`.
That spelling would suggest a method postcondition and obscure the named law that establishes the claim.
I would not spell a grade `modifies`.
The bound concerns transferred amounts rather than a set of mutable locations.

This is an authoring reader.
It needs a conventional expression parser and declaration parser.
Keeping bodies as single expressions avoids a statement-to-expression translation.
Its round-trip cost is medium to high because a general core body does not always reconstruct as these declarations.
A core block remains necessary for exact printing of arbitrary installed packages.

## 7. Prefix syntax with semantic Unicode

The principle is to spend new glyphs only on distinctions they explain.
The contextual brackets separate a hole type from an ordinary type.
The turnstile separates context from result.
Angle brackets mark explicit substitution.
The comparison glyph replaces a two-character comparison token.
The remaining forms keep the current prefix discipline.

```text
(package
  (doc "a counter whose step is chosen in context; it spawns parameter packages")
  (state {count : nat})
  (rel choice (key {k : nat}) (val nat) (limit 1))
  (hole step [· ⊢ nat]
    (select choice {k = 0})
    (candidate 1)
    (candidate 10 (cell #G)))
  (method bump
    (done (with state {count = (+ state.count step⟨⟩)})))
  (method choose (arg {i : nat}) (edits 1)
    (done state (upsert choice {k = 0} arg.i)))
  (method spawn (arg {n : nat}) (calls (install))
    (done state
      (install (pkg (cat (u64be #0a00000b00000004000004000106016e010000000800010f016e010408 arg.n)
                         #00010000010000020000000000030000040000050000)))))
  (law cap
    (on (adopt birth invoke) (if (≤ new.count 100) ok (refuse "over 100")))
    (on retire (if (== old.count 0) ok (refuse "not empty")))
    (else (refuse "frozen"))))
```

Type fields use a colon.
Value fields use an equals sign.
Neither record form introduces mutable storage.
The Unicode spelling for a supported binder is `[x : nat @ cell #G ⊢ nat]`.
Candidate support clauses retain the existing `cell`, `law`, `runs`, and `row` words.
The guard retains `(guard pin expression)`.
Those words distinguish the support kinds more clearly than invented symbols would.

This makes contextual syntax and record fields easier to recognize.
It leaves large nested expressions structurally unchanged.
It therefore cannot solve the Section's repeated-type problem by itself.
It also requires deliberate font and input support.
The language can accept `|-` and `<=` as ASCII aliases outside strings.
The canonical printer chooses one spelling.

A refusal would select the same source node as the current surface after translation.
`step⟨⟩` expands to the existing named-hole use.
The support span remains the span of `(cell #G)`.
The diagnostic also retains the structural path when source text is absent.

The feature probes remain `(claim keeps INV LAW)`, `(effect (moves 5))`, and `(holds give)` within a relation whose value type contains `give : {amount : nat, asset : digest}`.
I would not replace `keeps`, `moves`, or `holds` with glyphs.
Their difference is part of the language's meaning.

This can begin as a printer.
Adding a reader requires a bounded translation into existing surface s-expressions.
The translation must tokenize strings before recognizing glyph aliases.
Its proof decomposes into token normalization and the existing lowering.
Its cost is low for the displayed subset.
A universal authoring printer still faces the current surface's representational limits.

## 8. Declarative header, expression bodies

The principle is to put a package's commitments above its computations.
The header declares the state, relation, hole, method shapes, and law membership.
The body section contains expressions at those declared shapes.
The separator is syntax rather than a comment convention.

```text
package {
  doc "a counter whose step is chosen in context; it spawns parameter packages";
  state {count: nat};
  relation choice key {k: nat} value nat limit 1;

  hole step : [| nat] {
    select choice[{k = 0}];
    candidate 0 = 1 supports [];
    candidate 1 = 10 supports [cell #G];
  }

  method bump;
  method choose(arg: {i: nat}) edits 1;
  method spawn(arg: {n: nat}) calls [install];
  law cap;

  ---

  bump = done (state with {count = state.count + hole step[]});

  choose = done state [upsert choice {k = 0} arg.i];

  spawn = done state [install {pkg =
    cat(u64be(#0a00000b00000004000004000106016e010000000800010f016e010408, arg.n),
        #00010000010000020000000000030000040000050000)}];

  cap = judge req.occasion {
    adopt | birth | invoke =>
      if new.count <= 100 then ok else refuse "over 100";
    retire => if old.count == 0 then ok else refuse "not empty";
    else => refuse "frozen";
  };
}
```

`[| nat]` is the ASCII empty-context judgment.
The Unicode printer can display `[· ⊢ nat]`.
A nonempty context reads `[x: nat, y: nat | nat]`.
A use `hole step[e₀, e₁]` supplies an ordered substitution.
A binder can add `supported by row rates {k = 0} version 7`.
A candidate's `supports` list stays separate.
The declaration can add `guard cell #G => present`.

The header is enough to see which methods can edit rows or return calls.
It also shows where every hole gets its selection.
The body is enough to see how the counter changes and what the law admits.
The design makes moving between a signature and its body necessary in large packages.
An editor should provide that link rather than duplicate the declaration.

A refusal would point to `hole step.candidate[1].supports[0]` in the header.
A type error in `bump` would point to the expression after `bump =`.
The diagnostic can show the relevant signature alongside the body.
The package id qualifies both positions.

The feature probes are header entries `claim keeps INV LAW;`, `method pay … moves <= 5;`, and `relation escrow … value {give: {amount: nat, asset: digest}} limit 8 holds give;`.
To make carried claims authorable, the header also admits `field INV : State -> bool;`.
Its body is an ordinary annotated lambda below the separator.
The current authoring grammar lacks that general interface-field declaration.
Adding it exposes an existing core capability.
It does not add a new core type or claim rule.
The law's certifying application must expand to the exact literal invariant term the current checker recognizes.
The compiler must not silently replace that application with an equivalent comparison.

This is an authoring reader.
Its parser has two small phases separated by a mandatory token.
The declaration phase supplies the types needed by the expression lowering.
A body without a declaration is refused.
A declaration without its required body is refused.
Its total printer needs a constructor escape for arbitrary package bodies.
Its cost is medium.
Its long-term advantage is a place to expose every interface field without pretending every field is a method.

## The round-trip obligation

The existing theorem is about reconstructed packages rather than recovered typography.
`Lang/Proofs/Print.lean` proves `readPackage_packageText` under explicit canonicality premises.
Those premises include `HolePrintable` for contextual declarations.
They also include well-formed produced interfaces in effect entries.
The source currently keeps a dynamic print-and-read check in `Print.package`.
The new surface must preserve that check until its own proof replaces the need for it.

For a new reader `readN`, the target is `readN(printN(P)) = ok P` on the declared printable domain.
Equality must be equality of packages.
Observational equivalence is too weak for content-addressed identity.
It is also too weak for metering and certifying-shape claims.
The proof must preserve candidate order, hole order, hypothesis order, support order, relation key order, imports, and claims.
Canonical sorting remains appropriate only where the current reader already sorts.

A second property concerns authored text: printing its parsed package must parse back to that same package.
That property does not promise to recover comments, anchors, aliases, grouped law arms, or original binder names.
A source-preserving formatter needs a concrete syntax tree for those details.
Source spans and presentation anchors must stay outside the hashed package.

A derived interface is easy to print for this counter.
An arbitrary interface assembled by `fix`, application, or extension is a different case.
No proposed authoring printer gets a universal theorem by recognizing only the pleasant examples.
A constructor escape gives it a total route for the rest of the core.
The core reader remains the final reader in that route.

The member cards have no new parsing theorem.
Their exact export uses the existing printer.
Their separate obligation is that each displayed assertion is derived from the package or the explicitly identified view.
The review rows can remain a view under the same rule.

## What the real packages demand

The Bell's authoring source uses an activity to generate pending and answered rows.
It also defines explicit wrappers around that activity.
An aimed answer returns a typed nested invocation with budget 100000.
The target call is part of the same Turn.
These facts argue for showing call slots beside method signatures.
They also argue for retaining activity sugar above the general expression language.
No new punctuation should force the Bell back into fully repeated method types.

The Bell declares relation keys in time-then-signer order.
Record type fields elsewhere are canonicalized by label.
A new formatter must preserve the distinction between declared key order and record field order.
Sorting both with the same pretty-printing helper would change behavior.

The document's Section is an instance of `Std.hole` over bytes.
Its contributors post candidate values into a relation.
The root package imports three helper packages.
Its relations include `candidates`, `facts`, `fills`, and `pending`.
Its methods include `propose`, `rejudge`, `select`, `accept`, and `repin`.
Its recorded candidate status can become `suspended "support0 dead"`.
The checked judgment recomputes usability from the pinned facts.
The recorded status is not a substitute for that judgment.

The Section's posted data candidates are not the README's ROM list of code candidates.
A common visual vocabulary can show selection and supports for both.
The view must still label where the candidates live and who can change them.
For the README it should say “committed code candidates.”
For Section it should say “posted candidate rows.”
Turning both into one source construct would require a separate semantic design.

The Section's expanded core text also demonstrates the limit of glyph substitution.
Repeated annotations and generated plumbing dominate its size.
Naming shared types in a view removes that repetition without changing runtime code.
Recovering an activity from arbitrary compiled bytes requires more evidence than pattern resemblance.
The constructor view is the fallback when that evidence is absent.

## The three I would pursue

I would pursue 8 as the authoring reader.
It separates declarations from computations without separating them into different files.
It has an explicit place for carried claims and effect bounds.
It also exposes ordinary interface fields that the current authoring grammar cannot declare.
Its critique is the distance between a signature and its body.
Its meta-critique is that familiar module structure can hide the language's contextual novelty.
Keeping the hole's selection and support list in the header counters that tendency.

I would pursue 4 as the member view.
It puts the support failure and available repair method on the same screen.
It can serve both committed code candidates and the Section's posted data candidates.
Its critique is that a prose summary can imply more than the package establishes.
Its meta-critique is that interface design tends to reward reassuring summaries over exact distinctions.
The view must preserve absent, unpinned, dead, selected, and usable as distinct states.

I would pursue 7 as the inexpensive printer experiment.
It isolates the value of better delimiters and meaningful Unicode.
It can improve the current surface without committing to a larger parser.
Its critique is that the largest programs stay large.
Its meta-critique is that a cheap typographic improvement can become an excuse to avoid the missing abstractions.
The experiment should be judged beside the Bell and Section as well as the counter.

I would keep 5 as the exact diagnostic fallback rather than the everyday authoring language.
I would borrow 2's position model for every presentation.
I would offer 3 as a law-review mode.
I would retain 1 as an expert view of contextual scope.
I would reject 6 as the primary surface because its function-like holes and statement-like results teach two misleading habits.

## Defaults

The testground should open on 4.
Its counter demonstration should show the committed candidates above the currently pinned selection.
Revoking `G` should mark candidate 1's cited support as dead.
The refused invocation should retain the runtime's exact reason.
The repair control should prepare an invocation of `choose` with index 0.
It should display that proposed call before the member submits it.
Tick use belongs beside the execution result.
The authoring text and constructor view belong one click away.
No source toggle should change the package id.

The README should use 8 after its reader exists.
The contextual judgment should print as `[· ⊢ nat]` there.
The ASCII spelling should remain accepted.
The complete byte-generating expression should remain visible.
A typed quotation syntax would be a separate proposal with a separate cost account.
Until the reader exists, the README should retain its executable current example.
An idea memo is not a reason to publish syntax that the journey cannot read.

## What I would preserve

I would preserve the small, explicit core tree.
I would preserve the core reader as an exact escape hatch.
I would preserve named constructors for `hole`, `candidate`, `select`, `claim`, `moves`, and `holds`.
I would preserve the visual difference between a declaration and a use.
I would preserve explicit substitutions at hole uses.
I would preserve refusal reasons as literal names.
I would preserve complete act coverage in the lowered law.
I would preserve ordered candidates and ordered relation keys.
I would preserve monomorphic type annotations in the core.
I would preserve the separation of package bytes from installed package identity.
I would preserve result construction as expressions with suspended fields.
I would preserve the same metered evaluator for every surface.
I would preserve ordinary method calls as the mechanism for repair.
I would preserve the current absence of automatic candidate fallback.
I would preserve `keeps` as a checked carried claim rather than a documentation badge.
I would preserve printable ASCII for every construct that a terminal user must enter.

## Reading record

Repository observations use origin/main at `571117332c2e1d3328722db426f2fa522fcb4f3c`.
Repository reads ran through SSH on hbox.
I read the README's complete counter and its explanation.
I read `Lang/Surface.lean`'s grammar, lowering contract, declaration reader, law lowering, hole lowering, and position lookup.
I read `docs/spec/2-structure.md` and `docs/spec/4-execution.md`.
I read `CHARTER.md`.
I read the relevant entries LANG-50, LANG-89, LANG-90, LANG-93, LANG-104, and LANG-105 in `decisions/lang.md`.
I inspected the round-trip statements and `HolePrintable` in `Lang/Proofs/Print.lean`.
I read `Lang/Claim.lean` and the claim journey's acceptance and refusal cases.
I read `world/resident/Bell.ob` and inspected the shipped Bell's declarations.
I inspected the shipped Section's declarations and helper linkage.
I read the Section generator and journey in `Lang/Journey/Doc.lean`.
I read the support probe, coverage check, judgment, and status code in `Lang/StdHole.lean`.
These inspections establish the design constraints rather than executable implementations of the proposed readers.

## WORKLOG

2026-10-27 — Read the language and package sources at the revision recorded above.
2026-10-27 — Wrote eight complete renderings of the README counter with separate probes for claims, grades, and held value.
2026-10-27 — Recommended the two-level reader for authoring and the member view for the testground.
2026-10-27 — Checked all eight renderings for matching generator byte strings, documentation, and refusal literals.
2026-10-27 — DONE. Wrote [SYNTAX-IDEAS-ASTRA.md](/Users/ember/dev/redregg/work/promo/SYNTAX-IDEAS-ASTRA.md) with eight complete renderings and recommended defaults. No repository edits or landings.
