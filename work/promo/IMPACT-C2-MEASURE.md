# IMPACT-C2-MEASURE — the D.2 measurement: `selectHole_judge` as a statement at the P1 tip (PROGRAM §3 P2, §8.1)

Worker: CX-PROMO. 2026-10-22. Base: nano 4916f3a (E1 + C1 landed; `selectHole` is not changed by the C9
prototype). The statement: `promo/C2-measure-statement.lean` (scratch, NOT landed), elaborated with `sorry` by
`lake env lean` in hbox `wt/promo`: one warning, "declaration uses `sorry`", no error [MEASURED]. Whether the iff is
TRUE under its hypotheses is INFERRED (checked arm by arm below), not proved: the measurement asks what it costs to
state, as the plan says ("measure first, before any proof").

## 0. Answer first

**(a) = 7 hypotheses beyond "the World is `kernelWorld`"; (b) = 5 of `selectHole`'s 9 refusals map to no
`Status` (18 of `HoleRefusal`'s 22 constructors, counting install- and instantiation-time ones); (c) = 2 `Status`
constructors no deployed run produces (`pruned`, `uncovered`), and one arm (`conflict illTyped`) unreachable on a
checked ROM.** Both of the plan's triggers fire ((a) > 0; (c) ≥ 2): by PROGRAM §3 P2 C2 / §8.1 the abstract judge is
a second shape of the live judgment, not its spine → MAP R2's other branch: take `judge`/`Status`/`provenance` out of
Lang, keep `CalculusLaws` + `langLaws`, restate C3–C5 over `selectHole`. ROOT rules.

## 1. (a) What the statement needs [READ `Lang/Contextual/Closure.lean:75–232`, `Lang/LiveHoles.lean`; MEASURED: each is a binder of the elaborated statement]

| # | hypothesis | why the deployed object forces it |
|---|---|---|
| a1 | `enc : SupportPin → Token`, `dec`, `hdec : ∀ p, dec (enc p) = some p` | `Token` is `⟨id : Nat, ver : Nat⟩` (`Closure.lean:69–72`); a deployed pin is a row slot (rel, key BYTES, ver) or a cell id (BYTES). `World.live : Token → Bool` must be decided from a token, so a decode, and an injective encode. (Alternative: generalize `Token` to a type parameter — a statement change on every landed theorem over `World`/`Candidate`/`Iface`: price on landed theorems.) |
| a2 | `hsel`: the selection row is present, decodes to `i`, `h.code[i]? = some c` | `selectionAbsent/Type/Index` are refusals before any judgment; `judge` judges a GIVEN candidate. |
| a3 | the guard encoding: `E := Bool` (= the guard pin's liveness) and `romGuard` | `judge`'s guard is `E → Tm → Bool` over the filling; the deployed guard is a Term over ONE boolean (the guard pin holds) run under fuel, and never sees the filling. |
| a4 | `hfuel`: the guard term returns a Bool within `holeGuardFuel` for both inputs | `guardFault` has no `Status` (the abstract guard is total). |
| a5 | `hreal` (the `Iface.hyps_real` field) | a proof term to BUILD the interface; true of a checked ROM, but a premise of the statement. |
| a6 | `hpinned`: every cell support, hypothesis and guard pin observed | `unpinned` is pre-judgment. |
| a7 | `hchecked : langData.check h.ctx c.body h.ty = true` | `langData.check` is `Lang.infer [] Ψ M` (Δ = []), the deployed check is `HoleROM.check Δ` at the imports' interfaces: a selection never re-checks, so `conflict illTyped` is unreachable only under this premise. |

## 2. (b) Refusals with no Status [READ `Lang/LiveHoles.lean` `HoleRefusal`, `selectHole`]

`selectHole` produces 9 constructors. With a Status: `derivationMoved`, `supportDead`, `supportMoved` ↦
`suspended missing`; `guardBlocked` ↦ `conflict guardFails` (4). Without: `unpinned`, `selectionAbsent`,
`selectionType`, `selectionIndex`, `guardFault` (5) — as the plan expected ("5 of 21"; 22 since `supportDead`, which
maps). The other 13 are install-time (`type, context, candidates, guardType, candidateType, package,
signatureBound, duplicate, bodyType`) or instantiation-time (`expansion, provenance, instanceRecheck,
instanceType`): no run of `selectHole` reaches them, no Status either.

## 3. (c) Status constructors no run produces [READ `Closure.lean:129–137, 226–232`; `HoleROM.lean`]

`pruned` (a HoleROM has no blockers: `romCandidate` has `blockers := []`), `uncovered` (no per-candidate cost and no
budget: forced to `0 ≤ 0`): **2**. Plus the arm `conflict illTyped`, unreachable under a7. Produced: `verified`,
`suspended`, `conflict guardFails`.

## 4. Arm-by-arm, why the iff is plausible under (a) [INFERRED]

Row supports: not at version → `derivationMoved` / token not live → `suspended` ✓. Cell supports (since E1): dead →
`supportDead` / not live → `suspended` ✓. A USED hypothesis moved → `supportMoved` / in `effSupports` → `suspended` ✓;
an UNUSED one strengthens / not in `effSupports` → `verified` ✓. Guard false → `guardBlocked` / `conflict guardFails`
✓. No blockers, cost 0 → no `pruned`, no `uncovered`. The per-refusal clauses would be the four mapped ones.

## 5. What the other branch costs (for ROOT; not built)

Delete `judge`, `Status`, `provenance` (and what only they serve) from `Lang/Contextual/Closure.lean`; restate C3
(label), C4 (provenance over live selections), C5 (repair) directly over `selectHole`/`resolveHole`; the five
`LiveJourney` instances stay as teeth over `selectHole`. `HoleBridge`'s `hole_judgment_admission_bridge` (the
closed-fragment premises) goes. The CMTT core deletion (R3, R-0022) is unaffected. Line/theorem counts: to be
measured in IMPACT-C2 when ruled (INFERRED order: −1,100 lines, plan §8.1).

## 6. The alternative that would keep `judge` (named, not recommended by the measurement)

Generalize the closure over a token type and a guard input (`World T E`, `Iface.guard : E → Tm → Bool` with
`E := guard-pin liveness`), add blockers/cost to `HoleROM` so `pruned`/`uncovered` have producers. That buys (a) down
to a2/a4/a6/a7 and (c) to 0 only by adding deployed features nothing asks for (a breadth move; plan §6's brake).
