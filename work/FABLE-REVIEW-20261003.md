# Review for Codex: Objective Bend and the last day on Mini main

From: Claude (Fable), at ember's request. 2026-10-03.
To: the Codex root and lane owners.

This is feedback from a peer who read your work cold. It is meant to be acted
on, so every claim has a file and line, and I say which things I verified myself
and which were found by a delegated reviewer and then spot-checked.

## What I looked at

- Objective Bend design: `redregg/designs/BEND-*`, `PREOSCRIPT-OBJECTIVE-BEND-*`,
  `CONSTRUCTION-PROOF-CONTRACTS`, the first part of `GRADED-EXECUTION-ARCHITECTURE`,
  `redregg/work/*` (linker record, raised bar, candid check-in, resume), and
  `minidregg/docs/OBJECTIVE-BEND*.md` with its evidence index.
- Objective Bend source: all 16 `ObjectiveBend*.lean` modules, `BendCoreAdmission`,
  the workshop and collective `.bend` examples, and the upstream kernel rules
  they depend on (`bendtt.lean` `Term.called`, `Walk`, `Eval`, the claims).
- Mini main, `cfaa2e5d..fe60a569`: 588 non-merge commits, 1,988 files,
  +288,190 lines in about 31 hours. Six independent reviewers each took a slice
  (two Lean, two Rust and operations, Bend backends, cryptography and consensus).
  Nothing was built; this is a reading review.

## Short version

1. The semantic anchor is right and the public guide is honest. Keep both.
2. Objective Bend is not a language yet. No `.bend` file says `self`, `super` or
   `spec`. The only composition in the tree is six `Spec` literals typed by hand
   in Lean.
3. What exists is link-time method resolution. It cannot express cyclic
   self-calls, it re-links a whole Book per instance, it type-checks the whole
   program three times per method call, and nothing about a spec is visible from
   inside Bend.
4. The theorem inventory around the object model is mostly restatement. 45
   theorems, 48 `#assert_axioms`, longest proof about 22 lines. Axiom-clean is a
   property of a proof. It says nothing about whether the statement has content.
5. Main is drifting from its own founding laws faster than at any point so far.
   The import-boundary gate is red. The tree is 2.7 times its line budget. The
   evaluator registry is still `[nock]` while 133 Bend Lean files sit beside it,
   115 of them outside the build gate.
6. The next step is depth, not more lanes: one Objective Bend method, written in
   source, from text to a durable native receipt.

## What is strong

- **`BendCoreAdmission.Checked`** (`Compiler/BendCoreAdmission.lean:19-26`). A
  private constructor that carries `Book.check book = .ok ()`, so every consumer
  gets `WellTyped` and `Live` from the upstream `book_check`. This is the right
  shape for a certified checker result.
- **Runtime semantics are `Eval` and `Walk`, never the checker's `wnf`.** The
  semantics audit holds this line everywhere, and its list of compiler
  mismatches (rewrite evidence erased, dead lets dropped, 48-bit naturals, F32
  NaN handling) is the most useful document in the set.
- **No second evaluator.** Composition elaborates into the core Book and the
  object layer is gone before execution. That is the derived-path instinct.
- **Three orders kept apart**: behavior ancestry, authority, and declaration
  order. The `Nat`/`Nat.arms` dead-reference cycle that forced live versus dead
  references (`ObjectiveBendLinker.lean:28-41`) was found by a real consumer.
- **`ObjectiveBendLinkerRefinement`**: lookup equivalence gives `Eval` and
  exact-count `Trace` transport across reordering. Small, general, and true.
- **`prepared_pin_preserved`** reuses the store's general ROM theorem instead of
  checking one generated object.
- **Laws written in Bend.** `OrderedCapacity.allocation_conserves` is a real
  inductive proof, authored in source and checked by the kernel.
  `ContractedReview.bend` (39 lines) is the most interesting file in the tree;
  see the last section.
- **`docs/OBJECTIVE-BEND.md` and the evidence index.** Clear prose and a useful
  vocabulary (authored, checked, executed, joined, deployed).
- **The adversarial persistence review**, point 1: stored checkpoint bytes are
  neither a reachability proof nor an affine resource. Exactly right.

## Objective Bend: the object model

### 1. There is no source language

Verified by reading. `git ls-files '*.bend'` gives 38 files and 4,082 lines.
None contains a spec declaration, `self.` or `super.` outside a comment. The
single composition is `Compiler/ObjectiveBendWorkshop.lean:35-52`: six `Spec`
values written in Lean, with

- interface types as raw core terms (`.All .Q2 (.Ref "CatalogReview.Candidate") …`),
- spec ids `1..6` and each `order` list typed by hand,
- captured data built by hand (`bytes [4]`),
- source attribution indices typed by hand (the catalog provision in spec 1
  says source `2`; the audit in spec 5 says source `3`).

The `.bend` side is ordinary Bend in which every method takes its collaborators
as callback parameters (`review_with_policy(policy, final_catalog, candidate)`),
and the Lean manifest says which argument is `self.catalog`. That is dependency
injection configured out of band. A member cannot write an Objective Bend
program; an agent with Lean can. The station and collective examples are called
Objective Bend and use no composition at all.

The encoding also costs expressiveness. The callbacks are affine closures
(`final_catalog: @+key: …`, bound at `.Q1` in the manifest), and closures are
not `Data`, so a method can call each collaborator at most once per invocation.
A method that needs `self.review(a)` and `self.review(b)` cannot be written.
With real `self.m` syntax elaborated to a global `Ref`, this limit disappears,
because a reference to a definition is not an affine variable.

Direction:

- A surface form for specs (requires, provides, parents, `self.m`, `super.m`),
  elaborated in Lean to `Partial` artifacts. The compiler grows the vocabulary;
  nobody types `Spec` literals.
- Compute the linearization. `Spec.order` is an input that `OrderCertificate`
  checks (`ObjectiveBendComposition.lean:57-71`). Two lawful orders give
  different behavior and nothing selects one. Compute C3 or C4, prove the result
  satisfies the certificate, and prove it is the unique order that does under
  those constraints.
- Move `ObjectiveBendWorkshop.lean` out of `Compiler/`. It is a fixture.

### 2. This is link-time resolution, not objects

`ObjectiveBendElaboration.definition` (lines 71-76) renames `self.x` and
`super.x` to concrete definition names and substitutes captures into the body.
An instance is a ROM pin to a complete relinked Book
(`ObjectiveBendInstance.lean:22-25`). The consequences, all verified by reading:

**No cyclic self-calls.** `orderLoop` (`ObjectiveBendLinker.lean:63-71`) refuses
any live cycle between definitions, because upstream `Term.called`
(`bendtt.lean:1209-1216`) admits only earlier definitions or a descending call
to the same definition. So if `A` calls `self.B` and an extension's `B` calls
`self.A`, the composition is refused. That is the central use of open recursion.
Today `finalSelf` means late binding over a DAG.

The smallest refuter: one spec provides `even(n)` calling `self.odd(pred)`,
another provides `odd(n)` calling `self.even(pred)`. It descends structurally
and should be accepted. The linker returns `.cycle`.

Upstream already solves this. `safe.ts:1059-1062`: "kernel has no mutual
recursion, so a def k and its helpers go out as one def, their group. A mention
of a member is a call at its selector." The linker should form the same groups:
merge each strongly connected component of the live graph into one
selector-indexed definition and let `Book.check` judge the descent. That is a
contained change with upstream precedent.

**Per-call cost is three full type-checks.** On the reference path:

- `ObjectiveBendReferenceSource.lean:39` runs `BendCoreAdmission.admit` and
  keeps only `.isOk`,
- `ObjectiveBendReferenceLoader.lean:62` runs `admit` again on the same bytes,
- `ObjectiveBendInstanceLoader.loadPin` calls `construct`, which calls `link`,
  which calls `admit` a third time (`ObjectiveBendLinker.lean:134`).

Each `admit` is a parse, a re-encode, and `Book.check` over every definition.
`link` also runs `order` twice (lines 130 and 149) and decides deep equality on
every definition (lines 136-138, 154-156). All of this happens inside
`ObjectiveBendCallContext.bind`, which runs on every invocation, before a
single step of the method. Admission belongs at publication. The call path
should consume a receipt for an admitted Book identity.

**Overriding re-elaborates.** Because `self.x` is a rename, overriding `x`
changes the text of every method that mentions it, and the whole Book is checked
again. Two instances with different captured data are two different programs.

**Nothing is first-class inside Bend.** Specs are Lean values and byte
artifacts. A Bend program cannot receive a spec, extend it, or inspect its
methods. "Reflective source-authored tools" cannot be reached from this design.

**Interfaces match by syntactic equality of core terms**
(`ObjectiveBendComposition.lean:73-74`, `136-140`). No conversion, no refinement
of a result type, and an alias differs from its unfolding. `compatible` also
requires one type per selector across the whole composition, with no rename,
hide or exclude operator, so two unrelated mixins that both define `label`
cannot be composed.

**The pin is ROM** (`ObjectiveBendInstance.lean:57-61`), so an instance can
never change behavior. Governed evolution has no carrier, and object identity
across evolution is not specified.

You named the alternative yourselves, in one sentence of `BEND-WORLD-LANGUAGE`:
"a single checked tagged dispatcher with explicit descending fuel and immutable
method graph Data." I think that is the destination and the current design is a
detour. See "Objects as data" at the end.

### 3. The theorems restate their definitions

16 modules, 1,859 lines, 45 theorems, 48 `#assert_axioms`. I read all of them.

- `finalSelf_cursor_independent := rfl` and `priorSuper_is_prefix := rfl`
  (`ObjectiveBendComposition.lean:116-123`) are the two arms of `resolve`.
- `same_instance_on_demand := rfl` (`ObjectiveBendCallContext.lean:189-191`),
  where `Demand.self _ := request.self` ignores its argument (lines 164-166).
  No implementation could make this theorem false.
- `constructed_method_exact := construction.entries …`
  (`ObjectiveBendElaboration.lean:103-109`) projects a field of its own
  hypothesis. So do `linked_method`, `linked_helper`, `linked_retains`,
  `reflected_source_exact` and `checked_exact_ancestry`.
- `constructed_invocation` (lines 114-125) is the upstream `Eval.call`
  constructor applied to hypotheses that already include the `Walk`.
- `after_same_prototype := rfl`.

By my count about seven carry content: `select_provider_bounded`,
`super_provider_strictly_earlier`, `ancestorPool_exact`,
`prepared_pin_preserved`, `candidate_exact`, `lookup_equivalent`, and the
`Eval`/`Trace` transport.

Two things follow.

First, `#assert_axioms` is being reported as evidence ("Every named
#assert_axioms gate passed", linker record). It checks which axioms a proof
uses. An `rfl` passes it. Please stop counting it as qualification of a
statement.

Second, none of the 45 has the ATLAS keystone fields. The only teeth are a
runner printing `EXPECTED missing finalSelf.audit` (`ObjectiveBendWorkshop.lean:61-63`),
which is an `IO` side effect and not a Lean statement. No theorem in the tree
exhibits an inhabited `Construction`.

`CONSTRUCTION-PROOF-CONTRACTS` section 1 lists the right missing statements.
What landed are the identity lemmas. The keystones I would state first, each
with a satisfiable witness and a refuted hostile instance:

- **K1, dispatch adequacy.** Define the reference meaning of a composition as
  the fold of its layers (Faré's mix and fix, bounded by acyclicity or a clock).
  Prove that evaluating the linked entry in the linked Book agrees with it.
  Teeth: swapping two layers changes the value (your own "replace with 0, then
  add 1" example).
- **K2, composition algebra.** Associativity and identity of spec composition up
  to renaming of generated names; the shadowing law for overrides.
- **K3, linker completeness.** `link` succeeds exactly when the composition is
  closed, the grouped live graph is acyclic, and `Book.check` accepts. Then
  `.lostDefinition`, `.changedBook` and `.changedMethod` are proved unreachable
  and deleted, and `entries` becomes a lemma (distinct names and a permutation
  give lookup) instead of a runtime `decide`.
- **K4, incremental admission.** Appending fresh-named definitions to a checked
  Book preserves the check of the prefix. Then a prototype is a checked prefix,
  and instance creation and override cost the size of the change.
- **K5, behavioral interfaces.** A requirement may carry a law type, and every
  provider, including every override, must inhabit it.

### 4. Smaller findings

- `ObjectiveBendCallContext.lean:78`: the request is bound by setting
  `command.nonce` to a hash of it. `BendActivityIngress.lean:113,163`
  (`actionNonce`) does the same with a different preimage, and so do
  `ApplicationLifecycleCompletionSource.lean:137` and its V2 twin at `:134`.
  Four features now define the nonce as "the hash of my payload", separated
  only by domain strings, and replay protection for an Objective Bend call
  depends on a `salt` field. The signed command needs a typed, versioned
  statement field. Your own design says so ("BendInvocation is one framed
  complete statement").
- `ObjectiveBendPersistence.lean:23-25`: an open requirement is stored as a
  definition whose body is `Efq`. It is safe only because that Book is never
  checked. Represent an absent body as absent.
- `ObjectiveBendLinker.orderLoop` is cubic in string comparisons. Fine at 91
  definitions, not at ten thousand.
- `#assert_axioms` on plain `def`s (`construct`, `checkAll`, `captures`) adds
  nothing.


## Bend execution backends

Found by a delegated reviewer who read about 90 of the Bend backend files in the
hbox lanes in full. I re-checked each item marked (verified) on main.

The good news first: no backend refines the checker's reducer. Every theorem
that exists targets the real `Eval` and `Walk`. The vendored kernel is faithful
(a namespace wrapper and two `if_pos` rewrites). There are no `sorry`, `axiom`
or `opaque` declarations in the Bend files.

The state of each path:

| Path | What exists | Link to `Eval` |
| --- | --- | --- |
| Reference machine (`BendLiveMachine.executeChecked`) | Proof-carrying evaluator: every completed run carries a real `Eval` trace to a `Value` | Sound by construction. No completeness, determinism, fuel monotonicity or cost statement |
| Closure machine | 512-line machine, good invariants (`StateDenotes`, `WalkPrefix`, `beta_source`) | Conditional only, see below |
| Oblivious controller | Hand-written gate blocks for 7 control tags | None. Zero theorems in all 8 files (verified) |
| Trace and AIR | Boolean-DAG to IR2 lowering, constraints force gate equations | None. The files import no Bend machine (verified) |
| Logic circuits | Four template matchers and one jet | Per-fixture theorems |
| Homomorphic | Session and key bookkeeping, checks by shelling out to a Rust binary | Outside Lean |

Findings:

1. **The closure machine has no simulation theorem** (verified,
   `Theory/BendClosureSupportedRun.lean:222-263`). `covered_run_complete`
   requires the caller to supply `Covered`, which demands that every state be
   `Handled`. `Handled` has 14 constructors and none for variable lookup,
   annotation, reference, unspine, walk or classify. So no run that reads a
   variable or calls a Book definition is covered. The reviewer checked the
   machine's own first fixture, `(λx.x) ok`: tick 7 evaluates `var 0` and falls
   outside. `covered_run` has no consumer anywhere. The invariants are the right
   ones. What is needed is the step theorem: `Inv s src` implies there is a
   `src'` with `Inv (step s) src'` and either `src' = src` or `Eval src src'`,
   by case analysis on control and code, plus `start_denotes`.
2. **The unverified machine is the product path.** `BendActivity.advance` runs
   the closure machine. The compensating check that re-runs `executeChecked` and
   compares (`BendActivityYieldSource.bind`) has no consumer. `executeChecked`
   is wrapped four separate times, each with its own `Evaluated` structure.
   Register the reference machine as the one `Evaluator` now, and let the
   closure machine join when finding 1 is closed.
3. **`compile` is equality with a fixture** (verified).
   `Compiler/BendLogicMux.lean:118-120`:
   `if nPublic ≤ 4 ∧ source = sourceTerm then some (descriptor nPublic) else none`.
   The same shape is in `BendLogicSpecialization.lean:84-88`,
   `BendLogicPreludeCase.lean:17-20` and `BendLogicPreludeMux.lean:18-21`. The
   circuit is written by hand per file. This is the thing the derived-path law
   forbids. The one compiler with the right shape is the `BendNatural*` set
   (syntactic expression IR, structural circuit, one theorem for all
   expressions and inputs), which exists only in the bend-logic lane and is
   marked uncompiled. Grow that one to cover `Mat`, `Prj` and λ over finite
   data, and the four templates become corollaries to delete.
4. **The oblivious blocks imitate `step` by hand.** The reviewer compared the
   lookup and unspine blocks against the machine and found no discrepancy, and
   nothing in Lean says so. The theorem to state is
   `decode (network.evaluate (encode s)) = some (step limits library s)`. Better:
   emit the blocks from a syntactic description of `step`, which is what this
   repository exists to do.
5. **The public guide overstates the oblivious controller** (verified).
   `docs/OBJECTIVE-BEND.md:187-189` says it "covers all 12 controls of the
   closure machine; its compiled conformance checks cover 64 concrete
   state/codec cases." The tracked `Compiler/BendObliviousController.lean` is 46
   lines, composes three blocks, and its own header says "construction in
   progress … Current coverage: lookup1/2, unspine5, complete8, refused9,
   reverse10, install11". Evaluate, returned, apply, walk and classify are
   absent, so no computation step is covered. The only check file has eight
   fixtures on an empty library. I found one copy of this file on hbox and it is
   the same. This is the one place the guide makes a quantitative backend claim
   and I could not find source behind it.
6. **Canonical charge has four unrelated notions and no law.** `Trace` count,
   machine `sourceSteps`, `Expr.sourceCount`, and a caller-declared `Capacity`.
   `branch_charge_independent` (verified, `BendPrivateCapacity.lean:50-54`) is
   `rfl` on a function that ignores its usage argument. Your own lemmas show
   `Eval` count is a poor meter: unary `Nat.add a b` costs `a+1`, a whole
   case-tree walk is one step, and `same_output_different_source_count` shows it
   leaks the branch. Define the charge on source, prove it unique (this needs
   `Eval` determinism, which nobody has stated), then prove each backend's meter
   equals it.
7. **Fragmentation.** 131 file names, 521 copies across lanes, 32 names with
   divergent content, and the integration tree is not always the newest copy.
   Paths B through F do not compose with each other; only the reference path
   reaches native effects. There are two Bool representations (`Lab "true"` and
   `Tup Q1 (Lab "True") (Lab "()")`) with nothing joining them.
8. **Names.** Of 485 theorems in the integration tree's Bend files, 18 are
   `rfl`, 22 are field projections and about 56 are codec round-trips, all among
   413 `#assert_axioms` pins. `source_at_restore` returns its own hypotheses.
   `resume_new_segment` is `Trace book 0 t t`. Files named `BendTrace*` contain
   no Bend. Grep finds no satisfiable or teeth witness in 116 files, with one
   exception worth copying: `BendLogicCase.descriptor_correct` paired with
   `wrong_output_refused`.

## Mini main: the Lean

Found by two delegated reviewers pinned at `cace986a`. I re-read every item
marked (verified) myself. Authorship note: of the commits in range, 156 carry a
Claude co-author trailer and most of the rest are attributed to ember with no
trailer, so I cannot tell from git which of these are yours. Take what applies.

### The gates

- **The import-boundary gate is red** (verified: I ran
  `scripts/check-import-boundary.sh`, exit 1). Seven edges outside the tier
  table, including `Kernel/NativeHostReserveBirth.lean:3` importing `Host`,
  `Compiler/CarriedSegmentIO.lean:13` importing `Host`,
  `Theory/LawComposition.lean:14` importing `Pred.Core`, and
  `Theory/BendTTSource.lean:8` importing `Std.Data.HashMap`. CLAUDE.md says to
  keep this gate green. The same range also widened the Host row of the table.
- **Four files are in no build target, so their checks never run** (verified:
  zero importers). `Theory/CheckedCarry.lean` (381 lines, 14 `#assert_axioms`),
  `Compiler/LegacyStoreCarryChecks.lean`, `Compiler/CarryConfigurationChecks.lean`
  and `Verify/JointDecisionRecovery.lean`. The last calls itself a gate and is
  18 bare `#print axioms`, which cannot fail.
- **The build-closure gate is red: 170 of 1,259 library modules are never
  elaborated by the gate** (verified: I ran `scripts/check-build-closure.sh`,
  exit 1). That includes 115 of the 133 Bend files, all 16 `ObjectiveBend*`
  modules, and every backend keystone discussed above (`BendClosureSupportedRun`,
  `BendClosureSimulation`, `BendObliviousController`, `BendLogicMux`,
  `BendTraceConstraints`). The other 18 Bend files, including `BendTTSource`,
  `BendLiveMachine` and `BendCoreAdmission`, are reached through the Host
  executable. Whatever checked the rest was a scoped build on hbox.
- **The host-closure gate is red** (verified, exit 1): 45 modules entered the
  import closure of `Host.Main` without the pin being rewritten, 18 of them
  Bend. The running Host's dependency set changed and nobody recorded that it
  was meant.
- **The proof-hygiene gate is red** (verified, exit 1), on the bare
  `#print axioms` lines in `Verify/JointDecisionRecovery.lean`.
- So four of the six gates that need no build are red on main. The gate runner
  (`scripts/local-gates.sh`) is well designed: every gate runs, a partial run
  can never read green. It is simply not being run before landing.
- Three Kernel files that are in the build closure describe themselves as
  uncompiled in their headers (`PayClaimQuote.lean:3`, `PayClaimDecision.lean:2`,
  `PayEnrolV2Legs.lean:4`). Either the banners are stale or the files are.

### Statements that say less than their names

- `Compiler/ObliviousEvaluator.lean:254-257`, `phaseSchedule_same` (verified).
  The statement is `f n = f n` after rewriting two length hypotheses.
  `phaseSchedule` is used nowhere else, and no access trace exists in the model.
  The word "oblivious" is carried by the name alone. Either the evaluator
  returns its address list and you prove it depends only on public sizes, or
  the module is renamed and the theorem deleted.
- `Compiler/StoreHiding.lean:219-225`, `commitment_hides := premise _ _`
  (verified). `Indistinguishable` is a universally quantified relation, so
  `fun _ _ => True` satisfies the premise.
- `Kernel/PayClaimReceiver.lean:239-244` (verified). The policy leg evaluates
  the law on a state where `project` itself writes
  `(authorizedSlot, 1)` and `(operationSlot, 1)`. `PayClaimLaw.clause` is
  exactly `authorizedSlot = 1 ∧ operationSlot = 1`. The receiver passes a law it
  answers for itself. ATLAS says to bind the policy term, not the decision bit.
- `Kernel/PayClaimCommand.lean:130-133` (verified). `Checked` is a record
  holding `valid : Bool`, built for invalid signatures too. No proposition
  relates `valid` to a key, a message or a signature. `CapabilityRenounce` and
  `SubjectKeyRotation` do this properly; reuse their token.
- `Kernel/PayEnrolV2Legs.lean:409-415`, `economic_partition` (verified). It
  destructures its hypothesis and returns one conjunct, under a docstring that
  says it is "not a parallel arithmetic result". The batches that actually move
  money (`enrolBatch`, `renewBatch`) appear in no theorem, although a real
  generic `Batch.conservation` exists in `Theory/CanonicalResourceKernel`.
- `Kernel/PayClaimQuote.lean:171,438` (verified).
  `def Response.priceReserved (_ : Response) : Bool := false`, then
  `theorem no_reservation … := rfl`, axiom-pinned.
- `Assurance/StoryLaw.lean`: the "sealed" theorems rest on an `ActiveComponent`
  premise that only `checkInstalled` could discharge, and `checkInstalled` has
  no callers. The Lean `law` is a hand copy of the Rust client's `table_law`,
  proved equal by `rfl` on one fixture (reviewer).
- `Host/LawSat.lean`: the solver treats `delta` slots as free variables, while
  the kernel defines `delta = after − before`. A law that no step can satisfy
  still gets a `witness`, so the lockout guard stays silent on a real lockout.
  `unsat` remains sound (reviewer).
- `Theory/LawComposition.lean`: an absent selector slot makes the guard skip the
  restriction, so composition fails open (reviewer).
- `Theory/KeyPreRotation.lean:309`, `old_key_refused_after_rotation`, concludes
  that an epoch differs and a row is set. Nothing in it says a signature is
  refused (reviewer).

Of 930 theorems added to `Kernel/` in the range, the reviewer's classifier found
72 that are `rfl`, 135 that are `decide` on a fixture, 90 that are a one-line
`simp` of definitions, and 111 that are one-line terms.

### Is it still a kernel

No (counts verified on the current tree). `Kernel/` is 436 files and 139,749
lines. `lakefile.toml:42` still describes it as "the 3 verbs (create · gwrite ·
move)". `Kernel.Verbs` is imported only by the umbrella and one manifest; the
running Host does not reach it. `Effects/`, which was to hold the open handler
registry, is 436 lines.

What exists is one hand-written receiver per feature. Files that each define
their own: `inductive Reject` 56, `structure Accepted` 52, `inductive Result`
49, `structure Prepared` 46, `def receiveLoaded` 32, `def replay` 29,
`theorem readGuards_readonly` 28, and an identical three-line `requireSome` 22.
`PayCell` and `PayCellLegacyV4` are 98% identical. This is the shape ATLAS was
written to prevent.

The collapse target is already in the tree. `CapabilityRenounce` and
`SubjectKeyRotation` keep the gate and its theorems in `Theory/` and leave about
400 lines of plumbing in `Kernel/`. `WorldKindInstance` lowers a descriptor to a
layout and a patch. One `Receiver` declaration (command codec, marker, gate,
patch per cell, nullifiers), with `receiveLoaded`, `replay`, `intent`, `charge`
and their three standard theorems defined and proved once, replaces the family.

### Twins

- `PayEnrolV2*` (2,180 lines) landed beside v1, which stays live. The
  payer-authored memo bytes choose which arithmetic runs
  (`NativeHostPayClaims.lean:116-129`). A shared nullifier blocks double mint.
  No retirement condition is written down.
- `Kernel/` holds 33 version-suffixed files. Lifecycle `Begin`, `BeginV2` and
  `BeginV3` coexist.
- `PolicyRecordCodec.LegacyV4` duplicates the v6 codec tower, and four
  `vN_frame_refused` proofs are copies although a generic
  `framed_other_frame_refused` exists.
- `Theory/BendTTSource.lean` (3,903 lines) and `vendor/bend/bendtt.lean` (3,892
  lines) are both tracked.
- `Host/Json.lean` is 5,993 lines of per-type encoders and decoders with no
  round-trip theorem. `Host/Main.lean` has about 150 numeric opcode arms.

### Strong, and worth generalizing

- `Pred/SatisfiableTotal.lean:1033`, `decide_unsat_iff`, with checked
  certificates and re-evaluated witnesses. Sound and complete on its fragment,
  and fuel exhaustion returns no verdict.
- `Compiler/RefusalReason.lean:857`, `narrowed_congr`: a real two-run
  non-interference statement with teeth.
- `Theory/Renounce.lean:240`: a carrier discharged from the real validated
  patch, then used. This is the template for every other carrier.
- `Kernel/ContentElementTree.lean:1005-1030`: an `Admitted` inductive over the
  real `run`, with acyclicity proved over all 14 actions.
- `Kernel/RoomBirthGate.lean:119`, `decideRoom_ok_iff`: a real iff on the
  deployed decision. `Kernel/LinkIndex.lean:561-600`: index sound and complete
  against the log.
- `Kernel/RoomKick.lean`: the pre-fix defect is kept as a theorem.

## Mini main: `native/resource-client`

61,172 Rust lines added through `cace986a`, 25.7% of them tests. Found by a
delegated reviewer; items marked (verified) I re-read.

### Defects

1. **`rotate-key` cannot recover from a crash after the Host admits the
   rotation** (verified, `key_rotation.rs:374-378`, `456-476`). The attempt
   directory is `rotate-{epoch+1}` where `epoch` is read from Host status. The
   rotation changes that status. If the process dies after operation 142 is
   admitted and before the key files are replaced, the rerun reads the new
   epoch, opens a fresh `rotate-{epoch+2}`, never sees the retained attempt,
   and the workspace keeps signing with a revoked key. The install itself is
   several unjournaled file replacements. The module has one unit test.
2. **Private-room keys are wrapped to an unsigned key record served by the
   operator** (`roomkey.rs:353-358`, `848-857`; reviewer verified that the
   client checks no member signature over the record). An operator that serves
   its own key as a member's record receives the next room key on the next
   kick or rewrap. The header promises the operator sees "Not a key, not a
   plaintext". Sign the record with the member's identity key, or state the
   passive-operator assumption next to the claim.
3. **The paid-entry rate limiter can lock out every new client** (verified,
   `enrollment_bootstrap.rs:533-535`). The table is keyed by full IP address
   and refuses new keys when full. One IPv6 /64 fills it.
4. **`credit status --inbox` can strand the room reference** (verified,
   `credit.rs:449-451`). The current reference is renamed away before the new
   one is read and imported. A crash in between leaves no reference, and every
   later attempt fails at the same rename.
5. **A missing tariff entry makes Hermes turns free** (verified,
   `credit.rs:812`, `unwrap_or("0")`). A nearby unchecked `u128` addition wraps
   in release builds.
6. **Hex decoders panic on non-ASCII input** (verified, `private.rs:98-108`,
   and five copies). They slice a `&str` by byte index and are fed Host-served
   views.
7. Seven durable-write implementations with different guarantees. Some write
   key material straight to the final name, some rename without syncing the
   directory. A correct one already exists at `receipt_continuity.rs:214-250`.

### Structure

- **The Lean boundary is a subprocess and hand-read JSON.** No generated code.
  `protocol/host-operations.json` is maintained by hand, and 30 new call sites
  pass literal opcodes.
- **Rust re-decides what Lean decides.** `pay_memo_v2.rs:67-146` re-implements
  the 229-byte codec that `Kernel/PayEnrolMemoV2.lean` proves round-trip and
  injective. `transport.rs:263-323` is a third copy of route exposure. A test
  keeps a version string in step by scanning Lean source text
  (`workspace.rs:7040-7049`). `pay_claim.rs:156-173` shows the alternative
  already works: ask the pinned local Host.
- **Rust is the sole authority** for key rotation install, all end-to-end
  encryption, dispatch-once fencing, every recovery journal, and whether Hermes
  is owed payment. None has a Lean model.
- **The same custody pattern is typed again per feature**: reserve a directory,
  retain artifacts with hashes, write a marker, recover by lookup. Eight
  modules do it with different crash coverage. The crate has 20 copies of
  `decimal`, about 18 hex codecs, 8 key loaders and 6 flock wrappers. One
  retained-operation ledger and codecs emitted from the Lean structures would
  remove an estimated 30 to 40 percent of the new lines.
- **Most new tests are in no gate** (verified). `scripts/check-rust-tests.sh:56`
  runs four name filters, about 83 of 805 tests, and did not change in the
  range. No unit test crosses the real Lean boundary.

### Keep

`hermes_handoff.rs:112-122` (verify the exact bytes, then parse those bytes),
`scheduled_transport.rs:399-433` (marker durable before the effect),
`web.rs:190-250` (loopback, exact Host and Origin, constant-time token),
`app_document.rs:344-400` (curl with cleared environment and no redirects).

## Mini main: other native crates, scripts and operations

Found by a delegated reviewer through `cace986a`. Items marked (verified) I
re-read. Nothing was executed.

### Defects

1. **Operator-to-root escalation in the SPK broker's `ExportVolume`**
   (verified by reading, not exploited; `native/spk-host/src/broker.rs:1188-1245`).
   The broker runs as root with no hardening directives
   (`deploy/spk-host/mini-spk-broker.service`). `<root>/<store>` is created and
   chowned to the operator, mode 0700 (`InitStore`, lines 780-794), so the
   operator controls everything under it. `ExportVolume` checks `exports` by
   path (line 1201), freezes the volume, copies up to gigabytes into
   `exports/<app>-<stamp>.ext4`, then calls `std::os::unix::fs::chown` on that
   path (line 1239). That call follows symlinks. During the copy the operator
   can replace `exports` with a symlink to a directory in which the predictable
   file name points at any file on the host, and root chowns it to the
   operator. The create branch has the same race at line 1204. The read side of
   the same file already does this correctly with `O_NOFOLLOW` and fd walks
   (lines 328-373, 412-428). Use one fd-relative primitive for every root touch
   of an operator-owned tree.
2. **`fsfreeze` has no crash recovery** (verified: four call sites, two freeze
   and two thaw, all inside request handlers). If the broker dies during the
   copy the volume stays frozen, the app hangs, and later exports fail until a
   human thaws it. `Backup{}` copies every volume into a root-only directory
   with no retention or quota and can be called in a loop.
3. **Root loop-mounts an operator-supplied ext4 image.** The comment in
   `deploy/spk-host/spk-var-volume:153-176` says the hash was "checked against
   the signed export", but the hash comes from the same operator request and
   the broker verifies no signature. Only `e2fsck -fn` stands between an
   unprivileged user and the kernel's ext4 parser.
4. **The setid filter bounds numbers that the bounded capabilities can
   redefine** (reviewer, suspected, untested). The resident holds
   `CAP_SETUID`/`CAP_SETGID` and nothing restricts `unshare(CLONE_NEWUSER)`.
   Keep those capabilities out of the process that parses app bytes.
5. **Inference scheduler capacity leaks permanently.** Only queued and placed
   jobs expire. An uncertain job keeps its slot, and the operator verbs are
   status and drain. One hung provider call in a one-slot group starves the
   group until someone edits `state.json`. The scheduler has no Lean model at
   all, and every transition rewrites and syncs the whole state.
6. **A kernel edge without a wire wedges apps, and the journey scores it PASS**
   (verified, `scripts/spk-platform/jspk1.sh:271-272`). A START whose BEGIN
   reply is lost leaves the app claimed forever. Lean has the transition and no
   receiver exists. The journey row passes by grepping stderr for
   "reconcileFailedStart receiver is absent". ATLAS law: capability and wire
   land in the same commit.

### Structure and evidence

- **`protocol/host-operations.json` is a hand-maintained twin of the Lean
  dispatcher** (verified, `protocol/HOST-OPERATIONS.md`: "There is no Lean
  compilation in this check"). 170 opcodes typed into 2,093 lines of JSON,
  checked by a 318-line Python regex scanner that keys on indentation in
  `Host/Main.lean`. Each opcode number now lives in four places. Define one
  Lean `inductive HostOp` with route and receiver fields, emit the Rust
  constants and the allowlist, and delete the JSON and the scanner.
- **Story law derivation runs backwards.** Rust generates the law, a Python
  script rewrites a GENERATED region inside `Assurance/StoryLaw.lean`, and Lean
  checks one table by `rfl`.
- **The gate runs no tests for most of this slice.** `check-rust-tests.sh` has
  four rows. Nothing runs the tests of `spk-host` (49K lines, including the
  sandbox, seccomp and broker tests), `inference-scheduler`, `pay-watcher` or
  the sqlite store. `sandbox.rs:429-431` says "A change to the sandbox floor
  must change this test", and nothing runs that test.
- **Committed evidence records very slow operations as PASS** (verified,
  `docs/evidence/2026-10-01-spk-ws/jspk1/rows.tsv`): stop 2,298 seconds, kill
  recovery 1,375 seconds, start 843 seconds. No journey row has a time budget.
- **Evidence files are write-only.** 665 added in range, 105 of them empty, 259
  from one refused-run directory, none referenced by a gate. 4,544 evidence
  files are tracked in total, and about 700 contain `/home/ember` paths.
- **The custody pattern is typed again at least 14 times** in these crates
  (`write_root_text`, `write_atomic`, `save_snapshot`, `publish_bytes`,
  `retain_exact_private`, and more), and once more in Python. One exact-effect
  journal with crash-phase hooks, as `anchor.rs:137-180` already has, with its
  state machine stated once in Lean.
- `native/grain-runtime/src/main.rs` is 20,130 lines. `config_migration.rs`
  (2,033 lines) decides in Rust which controller config fields may change, and
  no script or journey invokes it.

### Keep

`sandbox.rs` (fixed bwrap floor, fds for image and seccomp, bounded argv),
`broker_endpoint.rs:113-149` (`SO_PEERCRED`, `deny_unknown_fields`),
`http_entrance.rs:446-738` (duplicate-header and transfer-encoding refusal,
Origin and Fetch-Metadata checks), the pay-watcher's durable pending tick and
locked-down curl, and `scripts/local-gates.sh` (not-run counts as red).

## Cryptography and consensus (the 19 commits after `cace986a`)

Found by a delegated reviewer; items marked (verified) I re-read. Nothing was
built. Your own documents are unusually candid here (registrar trust, no
forward secrecy, variable-time field arithmetic), so this list favours what the
documents do not say.

What these components are, so nobody has to guess:

- `native/fhe-bend` vendors fhe.rs 0.1.1. The reviewer diffed it against
  upstream: the changes are visibility widening and a share codec behind a
  feature that is off. Primitives are not hand-written.
- `native/private-backend` implements ASKS, Gather, VABA and ACS from ePrint
  2024/677, and dZK, PrivSend, ACSS-Id and Sh2t-Id from ePrint 2024/1666. The
  thresholds, the coin, share freezing and instance binding read correctly.
  The field, the stream cipher and the commitments are hand-written.
- `pq_mailbox.rs` uses library ML-KEM-768 and XChaCha20-Poly1305 in a new
  four-layer mix composition.
- The Simplex files follow arXiv:2609.32985 (I checked that the paper exists:
  Losa, Wang, Xiang and Yu, "Simple and Fast Signature-Free Blockchain
  Consensus").

Findings:

1. **The Simplex safety proof is outside every build target and does not reach
   the engine** (verified with the build-closure gate: 18 of the 22 Simplex
   library modules are unrooted, including `GeneralSimplexReachability`,
   `GenericSimplexVAInvariant`, `Causal`, `Local` and `Structure`; the engine
   `GenericSimplex.lean` itself is built). The statement itself is
   good. `committed_prefix_consistency`
   (`Kernel/GeneralSimplexReachability.lean:109`) assumes only local guards on
   honest parties, an explicit `3f+1` roster and a fault bound; it does not
   assume agreement. But `LocalFaithful` is never constructed for any trace,
   and `GenericSimplexStructure.lean:199-201` says so. There is no satisfiable
   witness and no teeth at `f+1` faults. An edit that breaks a guard in the
   engine would leave every gate green and the theorem still quotable. Import
   the chain, prove `Reachable → AuditRefinement`, and add the two witnesses.
2. **One enrolled Byzantine sender can halt any private-backend receiver**
   (verified, `authenticated_ingress.rs:280-289`). Replay capacity is one pool
   across all senders, sequence numbers are sender-chosen, and nothing is
   pruned. Filling the pool with valid no-op packets refuses every later honest
   packet. That breaks the stated liveness with a single fault.
3. **A crash during a journal append bricks the replica** (verified,
   `transition_journal.rs:66-88`). `open` refuses a torn tail forever, and a
   test asserts that behaviour. The outbox is only released after fsync, so
   truncating a torn tail is safe. The crate's notes call it crash-durable.
4. **An unauthenticated stranger can kill a cohort link for its lifetime**
   (verified, `cohort_tcp.rs:811-813`). The first TCP connection wins. Garbage
   from anyone fails the open and the process exits, with no re-accept. The
   registrar needs every contribution, so one dead link stops the cohort.
5. **VABA and ACS view change has never executed in a test.** Three tests, four
   parties, one silent, deciding in view 0. No equivocation and no adversarial
   schedule. `vaba.rs:4-5` says the implementation differs from two printed
   predicates and "does not claim the printed theorem transfers". The reviewer
   argued safety by hand and found no bug. That is an argument, not evidence.
6. **The BFV depth limit is a declared integer over an unmeasured margin**
   (verified that `fhe-bend` has no tests and never calls `measure_noise`). The
   parameter set is n=4096 with a 109-bit modulus. The only security statement
   is upstream's docstring. No estimator run is recorded, and the reviewer's
   recollection is that this set has no slack at 128 bits classical and falls
   short in the quantum model. Run the lattice estimator, check in its output,
   and have the owner harness assert measured noise at each depth.
7. **The mix format is a new composition with no classical hybrid**, although
   `x25519-dalek` is already a dependency, and a single enrolled client can
   abort every epoch without attribution.
8. **`private-backend` has no channel.** Every module header requires
   authenticated private reliable channels. The only authority implementation
   is a test fixture, nothing encrypts, and no other crate consumes this one.
   Dealer coefficients and plaintexts are journalled in clear. No protocol
   states a concrete security bound; the reviewer's arithmetic for dZK at the
   default profile is about 103 bits classical.
9. **`native/bend-ir2-proof` is not reproducible from this repository**
   (verified: no `Cargo.toml` or lockfile is tracked). `provision.py` writes
   one with git dependencies and path patches into a breadstuffs checkout. Its
   `FullDegreeChallenger` changes Fiat–Shamir sampling with soundness
   explicitly unclaimed.
10. None of this Rust is derived from Lean: about 11.7K lines of protocol
    beside the formal core.

Keep: bounded decoding with canonical re-encode checks everywhere
(`consensus_wire.rs:160-186`), apply-on-clone then fsync then release
(`transition_journal.rs:117-140`), the frozen accepted share before the echo
(`asks.rs:291-295`) with its regression test, and the fork-refusing RNG.

## Drift from the founding laws

These are measurements on main at `fe60a569`, taken by me.

- **Size.** Tracked code is 458,823 lines of Lean, 260,783 of Rust, 49,454 of
  shell and 20,777 of Python: about 790K lines against a founding budget of
  290K for the whole project. The range added 288,190 lines.
- **"The derived path is the only path."** No code crosses the Lean and Rust
  boundary by generation. Each opcode number is typed in four places. The Bend
  circuits and the oblivious gate blocks are written by hand. About 130K lines
  of Rust landed beside the Lean in this range.
- **"Nothing lands beside what it supersedes."** `Compiler/Evaluator.lean:431`
  is still `def registry : List Evaluator := [nock]`. 133 Bend Lean files sit
  beside it and none registers. `Kernel/` has 33 version-suffixed files.
- **"Statement-first, with satisfiable, teeth and premise-inhabitation."** No
  Bend file has them. No `Keystone` structure exists anywhere in the tree.
- **"Naming is faking."** In the Bend Lean files (vendored kernel excluded) the
  word "exact" appears 697 times and "actual" 235 times. Fifty commit subjects
  in the range contain "exact". These words are standing in for theorems. A
  thing is exact when a statement says what it equals.
- **"`Theory/` is candidate-independent."** The gate is red.
- **"Quote the pessimistic number."** See the oblivious controller claim.

To ember rather than Codex: the budget and the tree now disagree by a factor of
2.7 and the tree is winning. Either the law changed, and CLAUDE.md and ATLAS
should say so, or it did not, and the next week is deletion. The collapse
targets are concrete: one `Receiver`, one emitted operation table, one custody
ledger, one evaluator.

## Process

- **Breadth is outrunning the join.** About 35 lanes ran today. Your own candid
  check-in names it: "independently green adapters can outrun the
  source-program-to-installed-result contract." Its recommended repair 3 is the
  right one and has not happened. I would stop opening lanes until one
  Objective Bend method goes the whole way: `self` and `super` written in
  source, admitted once at publication, run by a registered evaluator, its Plan
  admitted under current law, a durable receipt, and a private return released.
  Everything else in the Bend portfolio either serves that slice or waits.
- **Make "checked" a build fact.** Ember asked for work-in-progress on main, so
  main will hold unchecked source. Then the tree must say which is which
  without prose. Today 133 Bend files are in no umbrella, four other files are
  in no target, and three files inside the build closure call themselves
  uncompiled. Put unchecked modules under a separate library target, keep the
  main umbrella and its gates green, and delete header banners.
- **Generate the claims.** The guide's oblivious sentence is what a
  hand-written status produces under compaction. ATLAS already says the claims
  ledger is generated and cannot be parked. Emit the evidence table from the
  build: theorem names, their statements, whether they have witnesses.
- **Write records a cold reader can parse.** The redregg records are the memory
  a compacted root re-reads, and they are degrading: "HEAD947db722…",
  "Lean4.34.0", "Evalsteps38/55/39", "ownparent/publication",
  "Independentguardianreleased exit0". `docs/OBJECTIVE-BEND.md` shows you can
  write clearly. Use sentences, keep spaces around numbers, one fact per line.
- **Provenance in git.** 591 of the 636 commits in range are authored as ember
  under four email addresses. 156 carry a Claude trailer, 41 are authored as
  Codex, and 441 of the ember-authored commits carry no trailer at all. In a
  project about provenance, `git log` cannot answer who wrote a line. Add
  `Agent:` and `Lane:` trailers with a commit-msg hook.
- **Tests and journeys.** Most new Rust tests are in no gate. One journey
  passes by matching refusal text. Journey rows have no time budget, so a
  38-minute stop is a PASS.
- **The Lean seat.** Half-hour waits for two-second checks come from a
  341-import foundation that every small module sits on. A lease script treats
  the symptom. Split interfaces into small files and keep enum growth out of
  the foundation.
- **Second opinions.** The adversarial review asked two outside models and both
  timed out, so it had no counterview. Make a statement-only audit by a reader
  who did not write the code a standing step for each tranche. It is cheap and
  it found most of what is in this file.

## Directions worth the ambition

1. **Objects as data.** An object is `Data`: a table of method labels plus
   captured data. For each composition the elaborator emits one grouped
   definition, as `safe.ts` does for mutual recursion, whose arms are the method
   bodies and whose self-calls are recursive calls on a descending argument or
   an explicit clock. Then objects copy freely at `Q2`, cyclic self-calls are
   admitted, instances share one Book and differ only in data, an override is a
   new table, and reflection is pattern matching on the table from inside Bend.
   The clock is the public resource bound you must declare anyway. I have not
   built this. The discriminating experiment is small: the even and odd
   composition, and a method that calls `self.review` twice. Both fail today.
2. **The turn boundary as the later modality.** Inside one turn, recursion must
   descend, and `halts` covers it. Across turns, recursion is guarded: a
   resident is a guarded fixed point whose unfolding costs one admitted turn.
   Your Activity checkpoint machinery is already the operational half. Giving
   it a type turns "a persistent lifetime is not one total invocation" from a
   caveat into a rule, with a theorem: a well-typed guarded object never
   diverges within a turn, and each resume consumes exactly one generation.
3. **Laws as interface members, policy as type.** `ContractedReview.bend`
   already returns a result paired with a proof about it. Make that the normal
   form of a requirement, so an override of `review` must re-establish "a
   denied review stays denied" and the kernel checks it. Then translate the one
   predicate algebra into Bend types, so a method can carry a proof that its
   Plan satisfies the governing law for every input. Admission of such a method
   cannot be refused by that law. `Pred/SatisfiableTotal.decide_unsat_iff` can
   discharge the difference-logic fragment automatically. Governed evolution
   gets the same treatment: adopting a new revision requires a migration lemma.
4. **Derive the backends from `step`.** The closure machine's step function is
   exactly the kind of Lean definition this repository was founded to compile
   to constraints. Emit the AIR, the oblivious schedule and the gate blocks
   from a syntactic description of `step`, with one refinement theorem, and
   delete the hand-written blocks and templates.
5. **Admit once.** Prove Book weakening (appending fresh definitions preserves
   the check of the prefix). A prototype becomes a checked prefix, publication
   records an admission receipt for its identity, and the call path consumes
   the receipt. Three type-checks per call become zero.
6. **Run the swarm on Mini.** CLAUDE.md names helm as the first target
   application. Your build-seat queue is a capacity allocation by frozen
   request order with handoff, which is what `OrderedCapacity.bend` proves
   conserved. The source inbox, the leases and the handoff receipts are rooms,
   posts and receipts. Coordinating the swarm through the system it is building
   would be the first real multiuser agentic workload, and it would have found
   the per-call cost and the missing evaluator registration on day one.
7. **Differential fuzzing of the three semantics.** The semantics audit lists
   distinguishing probes and says none was executed. Generate well-typed Books
   by mutating the workshop sources, run upstream native code, the reference
   machine and the closure machine, and compare. This refutes cheaply before
   any refinement proof is attempted.

## Suggested order of work

1. Fix the defects with security or data-loss consequences: the broker export
   race, `rotate-key` recovery, the unsigned room-key record, the stranded
   credit reference, and the items in the cryptography section.
2. Turn the import-boundary gate green. Move unchecked modules under their own
   target. Correct the oblivious sentence in the guide.
3. Register the reference machine as the Bend `Evaluator`, stating the
   obligations it does not yet meet (determinism, completeness, metering).
4. Build the vertical slice for one Objective Bend method.
5. Add group formation to the linker, with the even and odd composition as
   teeth. State K1 with its witnesses before proving it.
6. Collapse the receivers into one `Receiver` declaration and emit the
   operation table from a Lean `HostOp`.
7. Close the closure machine step theorem.
8. Grow the `BendNatural` compiler and delete the four templates.
