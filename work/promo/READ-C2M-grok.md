VERDICT: OTHER-BRANCH

Cross-family read of IMPACT-C2-MEASURE, against nano `origin/main` = `4916f3ad` (fetched; the closure and hole blobs below are that commit, not the checkout, which is 40 behind). No build. The scratch statement was not re-elaborated; the builder's "one `sorry` warning" is theirs [MEASURED there]. Tags below are this read.

The plan's trigger is §8.1: (a) > 0 or (c) ≥ 2. Both survive this read. (c) alone is enough, so a dispute about which of the seven binders are real cannot flip the branch. The builder's §6 alternative (generalize `Token`, add blockers and cost to `HoleROM`) has no deployed consumer.

## 1. The seven (a)-binders — three are real, four are how it was stated

[READ `promo/C2-measure-statement.lean:57–74`, `Closure.lean` `Token`/`judge`/`Iface.hyps_real`, `LiveHoles.lean` `selectHole`/`changedHypotheses`/`runHoleGuard`, `HoleROM.lean` `HoleROM`, `LangInstance.lean` `langData.check`]. The elaborated theorem's binders beyond `kernelWorld`'s inputs (`dec`, `digestOf`, `look`, `rv`, `self`, and the env the theorem already passes) are a1, a2, a4, a5, a6, a7. a3 is not a binder.

| # | real? | why |
|---|---|---|
| a1 `enc`/`dec`/`hdec` | artifact as a binder | `Token` is `{id, ver : Nat}`; a pin is `(rel, key bytes, ver)` or cell bytes [READ]. The gap is real, the binder is not: a single defined injection `SupportPin ↪ Token` (ver copied, the bytes Gödel-coded into `id`) makes `hdec` a lemma, not a premise of this iff. Generalizing `Token` — the builder's other fix — would be a price on every landed theorem over `World`/`Candidate`/`Iface`. A definition is not that price. [INFERRED that the injection is provable; not built.] |
| a2 `hsel` | real | `judge` judges a given candidate. `World` does not say which `HoleCode` the selection row names. The ↔ as written (and the plan's own `romCandidate h i`) is false without "the row decodes to `i` and `h.code[i] = c`": a verified `c` is not the selected `c`. Not discharged by `kernelWorld`. |
| a3 `E := Bool`, `romGuard` | artifact | Not a binder. `romGuard` and `kernelWorld`'s `E` are definitions (`C2-measure-statement.lean:25–44`). An `Iface` built from the ROM already supplies its guard. Counting the encoding as a hypothesis inflates (a). |
| a4 `hfuel` | artifact for this iff | `romGuard` maps a non-Bool result to `false`, so a fuel fault makes `selectHole = error guardFault` and `judge = conflict guardFails`. Both sides of success ↔ `.verified` are false. [INFERRED from the two defs.] `hfuel` is needed only for a clause this statement does not contain (`guardFault` distinct from `guardFails`). |
| a5 `hreal` | artifact | `Iface.hyps_real` is a field of the constructed interface, and `langData.lookup` is `List.get?` [READ]. `zipIdx` indices are `< hypotheses.length`. `HoleROM.check` already refuses `hypotheses.length ≠ ctx.length` (`LiveHoles.lean` `HoleROM.check`, the `context` arm). From that equality, `hreal` is provable inside `romIface`; filtering to in-range indices makes it true by construction. The builder threaded the proof out as a premise. [INFERRED the proof; not run.] |
| a6 `hpinned` | real | Not implied by `World.live`. `changedHypotheses` calls `supportPinned` on every hypothesis pin, used or not; `effSupports` keeps only pins the filling uses. An unused hypothesis whose pin is unpinned makes `selectHole` throw `.unpinned` while `judge` can still return `.verified`. Same for the guard pin: `runHoleGuard` throws `.unpinned` before the term runs, but `kernelWorld`'s env is merely `supportLive = false`, and the guard term may return true on `false`. The candidate-support conjunct is redundant for this particular iff (an unpinned support is not live, so not `.verified`). The hypothesis and guard conjuncts are not. |
| a7 `hchecked` | real | `judge`'s first test is `langData.check`, i.e. `Lang.infer []` [READ `LangInstance.lean`]. `selectHole` does not re-check. `HoleROM.check` checks `inferE Δ` at the imports' interfaces. A body that fails the empty-import check and passes the import check is `.ok` from `selectHole` and `.conflict .illTyped` from `judge`, so the ↔ is false. The install check does not imply `hchecked`. This is the objects, not the statement. |

Corrected (a) = 3 (a2, a6, a7). Still > 0. These three are premises the bridge theorem would land with. They are not edits to theorems that have already landed; the card's "on any landed theorem" is the §8.1 reading (the bridge cannot be stated as "the World is `kernelWorld`" alone), not a claim that `selectHole_origin` and its neighbours gain binders. [READ §8.1 and the C2 card; the measurement's "both triggers fire" drops the card's "landed" word but matches §8.1.]

## 2. 18 of 22 — the closure is coarser, not too small

[READ `LiveHoles.lean` `HoleRefusal`, 22 constructors.] The plan's "5 of 21" is the same five, counted before `supportDead`. The measurement's split is right: `selectHole` returns 9, and 4 of those are judgments.

The only refusals a judgment of a selected candidate produces:

- `derivationMoved` — a row support is not at its ROM version (`rowSupportHolds` false; cells skip this arm)
- `supportDead` — a cell support is pinned and not live
- `supportMoved` — a hypothesis pin is observed, not live, and the body uses it
- `guardBlocked` — the guard term returned `false`

Those four are exactly the ones with a `Status`: the three not-live arms all go to `suspended missing`, and `guardBlocked` goes to `conflict guardFails` [READ `judge`, `Closure.lean` ~226]. The collapse is real coarseness (the journey already prints `support0 moved` / `support0 dead` as different texts). It is not a missing constructor. A closure that grew three suspended arms would be a second copy of `selectHole`'s names.

The other 18, and none of them is a verdict the closure is too small to say:

Pre-judgment, the candidate cannot be read (5). `selectionAbsent` / `selectionType` / `selectionIndex`: no code index. `unpinned`: a cell support, a hypothesis pin, or the guard pin is not in the caller's view (`World.live` has no "unobserved"). `guardFault`: the guard did not return a Bool within fuel. The plan already calls this pre-judgment. It is a machine fault, not an admissibility class; `Status` should not grow a fuel arm to mirror `run`.

Install, the ROM or the package is malformed (9). `type`, `context`, `candidates`, `guardType`, `candidateType` from `HoleROM.check`; `package`, `signatureBound`, `duplicate`, `bodyType` from `Package.checkContextual`. No `selectHole` reaches them.

After a selection, or at install admission, and outside the candidate judgment (4). `expansion` (`fillBounded`, also `unresolvedBody`). `provenance` — digest literals of the filled body must be among the template's and the selected originals'; this is not the closure's polynomial. `instanceRecheck` — `instantiateHoles`'s `checkE Δ`. `instanceType` — `admitContextual`'s second `checkE` (`Program.lean:201–202`); on the live path that is the same check `instanceRecheck` already made. These are bounds, literal integrity, and "the package does not type". The retypecheck gap is a7, a premise, not a missing `Status` constructor.

So the 18 are not uniformly "World unreadable or ROM malformed": the last four are post-selection package checks. None of them is a judgment of the selected candidate that `judge` lacks. The closure is the wrong spine because it is a second, coarser shape of four live answers, plus two arms nothing on the ROM produces. It is not too small.

## 3. No ROM consumer for blockers or per-candidate cost

[READ `HoleROM.lean:15–34` `HoleCode` = `body` + `supports`; `HoleROM` has no blocker field and no cost. `romCandidate` therefore sets `blockers := []`, `cost := 0` by the objects, not by the statement.]

What the journey and the generator actually have:

- Blockers, on the row machine, not on the ROM. `StdHole.lean` `holeCandidate` has `blocker : Option holeSupport`; `holeDecision` returns `pruned` when that support's probe is live; `prune` writes it; `holeStatus` has a `pruned` arm and no `uncovered` arm. Journey row LH8p admits `prune` and reads back `pruned "policy"`; LH8q refuses `select` with `pruned` (`Journey.lean:2099–2106`). That status is `holeStatus`, computed by the generated term `holeDecision`. Nothing in that path calls `Closure.judge`.
- The ROM beside it does not. `contextualHole` stores the caller's `HoleROM` as `holes := [h]` and does not add blockers or a cost (`StdContextualHole.lean:49–72`). `p8ContextBundle`'s ROM code is `[⟨.var 0, []⟩, ⟨.var 0, []⟩]` with `guardPin := none` (`Journey.lean:1927–1933`).
- The cap is a clause, not `uncovered`. The same bundle passes `prim.le value cap` as the hole clause. LH5c, value 50 past cap 10, is recorded `conflict "clause"` (`Journey.lean:2043–2045`), and `execute` refuses the same clause as `"conflict"` (`StdContextualHole.lean:60–62`). `Package.holeCharge` / `preparationCost` is a package-level syntax-node charge against the call budget (`runMeasured` throws `holeTicks`). That is not `Candidate.cost ≤ Iface.budget`.

`LangInstance.lean`'s `holeModelCandidate` does put a blocker token into `Candidate.blockers`, and the file says no deployed module imports it [READ]. That is the `HoleBridge` proof fragment the other branch already deletes. It is not a run, and it is not a ROM field.

Adding blockers or a per-candidate cost to `HoleROM` would invent a second producer for a judgment the row machine already runs, and a cost no row asks for. §6's alternative is breadth. The other branch stands. (c) = 2 is `pruned` and `uncovered` as `Status` constructors: no run builds those constructors. LH8p does not: it builds a different sum. The `conflict illTyped` arm is not a third unproduced constructor. `judge` produces it whenever `langData.check` fails; the live path never asks, and the install check does not make that failure impossible (a7). The measurement's "unreachable on a checked ROM" is true only under `hchecked`, not under `HoleROM.check`.

## 4. What stays in `Lang/Contextual` — delete `Closure.lean`, do not pour it into the proof modules

[READ charter law 8: a module exports definitions or proofs, split by a `Proofs` path. Law 1: a second shape is a defect. R-0021 keeps the protocol calculus.]

`CalculusLaws` and `langLaws` do not use `judge`. `CalculusLaws` (`ClosureStatements.lean`) quantifies over `CalculusData` and `HasTy`. `langLaws` instances it at `langData` (`Proofs/Contextual/LangInstance.lean`). `Protocol.lean` has no import of `Closure` (the file opens at its namespace). `NanoBridge.lean` imports `Protocol` and the resident trace. That is the calculus Ember kept.

After `judge` / `Status` / `provenance` leave, everything else in `Closure.lean` exists to feed them: `Token`, `World`, `Edit`, `Iface`, `Candidate`, `Slot`, `propose`/`select`/`fill`/`accept`/`prune`/`rejudge`, `repair`*, `Outcome`, `Op`, `Session`, `Consumer`, `label`. `Template.Typed` and the hole-model fragment in `LangInstance.lean` (`holeModelIface`, `holeModelCandidate`) go with `HoleBridge`, which C3 does not consume once C3–C5 are restated over `selectHole`.

The one definition that must survive is `CalculusData`. It moves into `Lang/Contextual/LangInstance.lean`, beside `langData`, which is already that concept. It does not move into a `Proofs` file (law 8). `CalculusLaws` stays a proof-module structure. `Closure.lean` then has no concept left; keeping it as a drawer of leftovers is the second shape again.

The repair theorems (`alternative_sound`, `replacement_sound`, `strengthening_sound`, `suspended_sound` in `Outcomes.lean`) are statements over `World`/`Iface`/`Slot`. Their deployed teeth already exist over `selectHole`, in `Proofs/LiveJourney.lean`: `strengthening_factor` :53, `kept_context` :69, `alternative_same_filling` :77, `replacement_filling` :85, `used_hypothesis_suspends` :93 [READ]. C5 restates the soundness theorems next to those teeth, in a proof module. The definitions they quantify over stay in `Lang/LiveHoles.lean`. Moving `Closure.lean`'s remains into `Lang/Proofs/LiveHoles*` would put definitions in a proof module and mix the dead spine into the live one.

`Lang/Contextual` then holds one module per concept that is still a concept: `LangInstance` (the deployed term language as `CalculusData`), `Protocol` and `NanoBridge` (the protocol calculus), and `Core`/`CoreCalculus` until R3 deletes them. The live judgment is `LiveHoles.lean`. That is the split law 8 and law 1 both want.
