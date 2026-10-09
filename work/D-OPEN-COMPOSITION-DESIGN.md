# Row D: open component contracts. Where we are, and the design

Author: DEPUTY-OB-ENG, 2026-10-07. Code read at `next` 424a5d94.

## Acceptance (done)

`be32eeb0` adds tests/objective-bend-source/three-package (Shop/Pricing/Taxes/Integration) and the
preview rows D1 and D1b. C composes two separately authored specs, A (`Pricing`, which `requires tax`) and
B (`Taxes`, which `requires price`). C does not edit either one; it overrides `price`. Both A's `total` and
B's `tax` read C's `price` through the final self: the result is 300, against the uncomposed baseline of
30. This is the current semantics of compose + fix + requires across modules. No language change was
needed for the acceptance.

## What the code does today (READ)

`chainFix` (Compiler/ObjectiveBendElaborate.lean ~1400-1535) already computes GPT-6's
`F_{A;B} = F_B(S, F_A(S, I))`. Each layer is instantiated at the row beneath it
(I₀ = the seed's type, Iₖ = overlay(defsₖ, Iₖ₋₁)). At `fix` it discharges against the final self:
a missing member refuses `requires-unprovided` and names which spec required it, a surplus refuses
`seed-extra`, and a type mismatch refuses `provided-mismatch`. Each spec's `requires` is checked against the
closed target (~1677). The contract is therefore discharged at fix, but only INSIDE fix. `compose` itself
produces `Specification<T>` with uniform public metadata. No first-class `C_{A;B}` exists that a
component artifact could carry or that could be checked before the closing `fix`.

## The design (proposed)

1. **The contract is data the front end computes at compose, not only at fix.**
   `Contract = {assumes : Row (members read from the final self: requires + self.m uses), consumes : Row
   (super members read), provides : Row (members defined/overridden)}`.
   `contract(A;B) = {assumes = A.assumes ∪ B.assumes, consumes = A.consumes ∪ (B.consumes \ A.provides),
   provides = overlay(B.provides, A.provides)}`.
   This is the row-level reading of `C_A ∧ C_B(S, F_A)`. It is computed by the elaborator for every
   `compose`. It is recorded in the spec's interface metadata, which is first-order data, so
   Specification<T> stays uniform and SpecMeta gains a `contract` field. It is checked at `fix` by ONE
   discharge function: `discharge(contract, seedRow, targetRow)`. Today's three refusals become its three
   arms.
2. **Theorem (front end, Lean):** `discharge (contract (compose A B)) seed T = ok ↔` `chainFix` accepts
   `fix(compose(A,B), seed)` at T. Plus `contract_assoc`: contract composition is associative, which must
   hold as row algebra even though SpecMeta trees are not. That is the reflection caveat REFLECTION.md
   already names.
3. **Staged modularity, said so:** a component artifact is `(term, contract)`. It is checked
   separately: its own `requires`, plus typing of its body against `assumes`/`consumes`. It is linked
   before closed Core4 by `compose` + `fix`. Nothing below Core4 changes, and the checker still receives a
   closed term. The open artifact is a front-end object.
4. **The commuting square** (`template ∘ subst = elaborate(instance)`): LT2's
   `Discharges.check_instantiate` covers the checker side. The missing half is the front end. Elaborating
   an open template, then substituting the final self, must give the same core term as elaborating the
   instance directly. State it over `abstractWith`/`instantiate` for the extension case first.
5. **Super abstract with per-operation constraints:** `add m` needs `m ∉ consumes ∪ provides(below)`,
   `override m` needs `m ∈ below` at a compatible type, and `replace m` changes the type and is refused
   unless declared. These are refusals on the contract algebra.

## Order

(1) the contract as metadata, with `discharge` replacing today's three refusals behaviour-identically.
The gate: all LTUO probes and D1/D1b unchanged. Then (2) the iff theorem, (4) the square for
extensions, (3)/(5).
Re-emits: SpecMeta gains `contract`, so the front-end identity, the reference packets and every spec
package change (as G1 did).

## Update 2026-10-07 ~07:50Z (DEPUTY-OB-ENG abfb6abb71f0a4311)

- DONE, queued `obeng-d2` fd4f69db. The contract algebra is `Compiler/ObjectiveBendContract.lean` (run_append is the
  C_{A;B} law), and chainFix decides every contract refusal through it. NEW `replace-undeclared` is one of the
  per-operation constraints. SpecMeta exposure of the contract is DROPPED as not needed: the composition law is a
  theorem about the code that runs, and reflection can be added when a program needs it.
- The square, re-scoped after reading the code. MODULAR-TYPING.md §6 already names the gap: "`Super` in a template is
  the literal bound row, not a second rigid variable, so the emitted instance is not literally `template[σ]`."
  The checker already types `get`/`extend` through a bounded variable (Self works this way), so this needs NO
  Core4 change:
  - D3a. `openBinding` gives Super its own rigid bounded variable (bound = the Super row). `Super with {f}` is then
    `field f T (variable s)`. A use of `super` where a value of its bound row is expected is refused
    `super-rigid`, mirroring self-rigid.
  - D3b. An instance is EMITTED as `instantiate σ template` (σ = {Self ↦ T, Super ↦ I_{k-1}}, annotations substituted
    then canonicalized) instead of re-elaborating the layer (`layerAt` for open declarations is deleted). The square
    then holds by construction.
  - D3c. A decided front-end `discharges σ bounds` check, plus the theorem that an instance emitted that way of a
    rigidly accepted template is accepted (Theory `Discharges.check_instantiate`). This is MODULAR-TYPING's
    `instance_accepted`.
