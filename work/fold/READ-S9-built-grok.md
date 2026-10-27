VERDICT: RELEASE S9-BUILT

Base `origin/main` = `ac345215f386e83287b6736f06d327ee9bdc8214` (fetched). No build. The candidate is the patch, not the local tree (that checkout is behind and deleted). Conditions from `READ-S9-grok.md`, all five kept.

## (1) The five conditions

**1. Kept.** The recheck arm has its own constructor, and its wire is the bare string.

[READ patch `Lang/LiveHoles.lean`] `HoleRefusal.instanceRecheck` is a nullary constructor, distinct from `instanceType (e : TypeErr)`. The printer is `| .instanceRecheck => "holeInstanceType"` and `| .instanceType e => s!"holeInstanceType {e.text}"`. The throw is `| .error _ => throw .instanceRecheck` on `checkE Δ body p.iface (Ω := [])`, the `TypeErr` discarded, which is today's bare arm (`origin/main:Lang/LiveHoles.lean:158–159`, `throw "holeInstanceType"`). `admitContextual` is the other spelling: `.program (HoleRefusal.instanceType e).wire` [READ patch `Lang/Program.lean`], today's `s!"holeInstanceType {e.text}"` (`origin/main:Lang/Program.lean:188`).

The plant is `recheck-arm-reachable` [READ patch `Lang/Journey/ContextualChecks.lean`]: `refusedAs (instantiateHoles (view none (some 1)) … wideP) .instanceRecheck && (instantiateHoles … p).isOk`, with `wide := 10 ^ 300` written into the ROM name and the body hole. [MEASURED `fold/S9-cchecks-plantoff.txt:51,69`] that row is the only `FAIL`, and the file ends `contextual-checks: RED (1)`. The mutated source is not in the receipt; [READ IMPACT-S9 BUILT] the mutation was `.instanceType e`, then reverted. A single-row failure is what swapping the two constructors does, and it is not what a broken printer of every other row would do. [INFERRED]

**2. Kept.** One field, two uses, no alias.

[READ patch `Lang/Bounds.lean`] `def holeGuardFuel : Nat := 256`, its own `def`, not `reasonMax` or `docMax`. The docstring says so. Fuel: `run [] Bounds.stackMax Bounds.holeGuardFuel …` [READ patch `Lang/LiveHoles.lean`, `runHoleGuard`]. Coefficient: `Package.holeCharge` is `… + Bounds.holeGuardFuel * p.holes.length`. `holePreparationPerHole` does not occur. `holeCandidatesMax := 64` and `holeSignatureMax := 16` are their own fields. The journey's `List.replicate 65` / `17` stay literals; they are the probes that exceed the bounds, not the bounds. `methodsMax` / `importsMax` are untouched.

**3. Kept.** (A). No wrapper. Every call names `Ω`.

[READ patch `Lang/Check.lean`] the seven `(Ω : HoleSignature := [])` defaults are gone (`inferE`, `inferFields`, `inferArms`, `inferSubst`, `infer`, `checkE`, `check`). No `checkClosed`. The two positional passes inside `Check.lean` (`inferE Δ Γ t Ω`, `inferSubst Δ Γ ts As Ω`) become `(Ω := Ω)`. Closed calls in the patch are `(Ω := [])`: `checkLib`, `Package.checkWith`, `HoleROM.check`, the recheck, `admitContextual`, `Resident`, `StdActivity`, and the closed theorem API. The journey probe that shows the split is now `(Ω := sig)` against `(Ω := [])` [READ patch `ContextualChecks.lean`], not three positional `[]`. `[]` still appears as `Δ` or `Γ` (`inferE Δ [] t (Ω := Ω)`); that is the local context, not the signature. Files on `origin/main` that call `Lang.infer` / `Lang.check` / `checkE` / `inferE` and omitted `Ω` are all in the patch. `Contextual/Core.lean`'s `infer` is a different function and is not this checker.

**4. Kept.** One formula, two `m`s, both floors 1.

[READ patch `Lang/LiveHoles.lean`]

```
def Package.holeCharge (p : Package) (m : Nat) : Nat :=
  if p.holes.isEmpty then 0
  else Term.nodes p.body * (m + 1) + Bounds.holeGuardFuel * p.holes.length
```

Actual: `p.holeCharge (resolutionMax rs)` with `rs := p.holes.map (resolveHole …)`. `resolutionMax` is not in the diff, so it is still `foldl (max · nodes) 1` [READ `origin/main:Lang/LiveHoles.lean:137–138`]. Static: `p.holeCharge ((p.holes.flatMap (·.code)).foldl (max · nodes) 1)` [READ patch `Lang/Program.lean`]. `instantiateHoles_cost` is still `i.cost ≤ p.preparationCost`. Old static `(1 + m)` and old actual `(resolutionMax + 1)` are now both `(m + 1)`; the proof drops `Nat.add_comm` and keeps `resolutionMax_committed`. `holeCharge` uses `p.holes.length`; `rs.length` equals it because `rs` is `p.holes.map`. [INFERRED from `List.length_map`, and from the old proof already rewriting to `p.holes.length`.]

**5. Kept.** The inductive is not widened.

Not constructors: `contextualPrintMismatch` / `contextualPrintRead` (the two rows still `named` on `Except String` [READ patch `ContextualChecks.lean`]); `holeUnresolved` (still the string inside `.refuse`, [READ patch `Lang/Program.lean`]); `holeTicks` (not in the patch; `origin/main:Lang/Program.lean:439`); the generator strings `holeSelectionKey`, `holeRootType`, `holeRootBody`, `holeImports`, `holeRootTooLarge` (`origin/main:Lang/StdContextualHole.lean:48–82`). The two `checkContextual` calls there are `.mapError HoleRefusal.wire`, so the generator's `Except String` stays. `resultName` / `refusedBy` rows are not in the diff except `Contextual.lean`'s `wrong-context`, which becomes `decide (why = .candidateType 0 0)` — the one row the design said becomes a constructor. `admission-prepared-type` is past the hunk and stays `why.startsWith "holeInstanceType"` on `Refusal.program` (`origin/main:Lang/Journey/ContextualChecks.lean:91–93`). The two `fillBounded` rows compare `ExpansionBound` (`.work`, `.size`), not `HoleRefusal`. The closed sentinel is `.error .provenance` with the comment that prepare is never called; no constructor was added for it. Reusing `.provenance` as a dead dummy is uglier than a private throw, and it is not a new refusal.

## (2) The printer

`HoleRefusal.wire` reproduces today's strings. No byte differs. Compared each old `s!` / literal (`git show origin/main:Lang/LiveHoles.lean`, `HoleBudget.lean:84–85`, `Program.lean:188`) to the printer's case [READ patch `Lang/LiveHoles.lean`]:

| old throw | printer |
|---|---|
| `s!"holeType {h.name}"` | `s!"holeType {n}"` |
| `s!"holeContext {h.name}"` | `s!"holeContext {n}"` |
| `s!"holeCandidates {h.name}"` | `s!"holeCandidates {n}"` |
| `s!"holeGuardType {h.name}"` | `s!"holeGuardType {n}"` |
| `s!"holeCandidateType {h.name} {i}"` | `s!"holeCandidateType {n} {i}"` |
| `throw e.wire` (shape and fields) | `.package e => e.wire` |
| `"holeSignatureBound"` / `"holeDuplicate"` / `"holeUnpinned"` / `"holeProvenance"` | the same literals |
| `s!"holeBodyType {e.text}"` | `s!"holeBodyType {e.text}"` |
| `s!"holeSupportMoved {h.name} {pi.2}"` | `s!"holeSupportMoved {n} {i}"` |
| `s!"holeGuardBlocked {h.name}"` / `s!"holeGuardFault {h.name}"` | the same |
| `s!"holeSelectionAbsent {h.name}"` / `Type` / `Index` / `s!"holeDerivationMoved {h.name}"` | the same |
| `"holeWorkBound"` / `"holeSizeBound"` | `.expansion .work` / `.size` |
| `"holeInstanceType"` | `.instanceRecheck` |
| `s!"holeInstanceType {e.text}"` | `.instanceType e` |

Braces hold the same `Nat` / `TypeErr.text`. `.package` does not reimplement `CheckError.wire`. A blocked body is `.refuse T why.wire.toUTF8` where it was `.refuse T why.toUTF8` and `why` was that string.

Codec vectors would not have caught a difference. [MEASURED] `git grep` of `holeType`, `holeInstanceType`, `holeWorkBound`, `holeUnpinned`, `holeProvenance`, `holeSignatureBound` over `origin/main:gates/codec-vectors.tsv` is empty. The 44 `hole` hits are the package field `holes := []` and one ROM fixture (`lang/package/4` row 42), plus `Term.hole` / `Term.refuse` as package bytes. Refusal text is `Refusal.program` and `.refuse` reason bytes, not package bytes. `--write` leaving the tsv identical is the control the design named, not a lock on `wire`.

What does lock bytes: the executing rows that still compare strings (`holeSelectionAbsent 0`, `holeUnpinned`, `holeGuardBlocked 0`, `holeSupportMoved 0 1`, `holeDerivationMoved 0`, `holeTicks`). They are not in the diff, so they still compare those characters. The constructor rows, including the new plant, compare values, not `wire`. The bare `holeInstanceType` has no exact byte row; `admission-prepared-type` is a prefix check of the with-text spelling only. A printer edit that kept the constructor `.instanceRecheck` and changed its string would stay green. That is not a byte that differs today. It is the gap the vectors do not cover.

## (3) The 27

[MEASURED `fold/S9-typediff.txt`] 27 lines, each `arrows/foralls (0, 0)`. [MEASURED `fold/diff-S9.txt`] the user-theorem TYPE lines are exactly those 27. No other user theorem changes TYPE. The rest of the TYPE section is the defs whose types were supposed to move (the seven checkers, the preparation functions, `HoleResolution.blocked`, `fillBounded`) and generated `match_` / `inj` / `sizeOf` / `splitter` / `inferE._mutual._proof_*`.

Each of the 27 is a re-spelling. No exception, no binder added:

- `String` → `HoleRefusal` on the prepare binders and on `Except` hypotheses (`admitContextual_closed`, `admitContextual_inv`, `admitContextual_lits`, `blocked_has_no_receipt`, `checkContextual_shape`, `holeRow_authenticated`, `instantiateHoles_cost`, `instantiateHoles_sources`, `instantiateHoles_typed`, `loadAll_closed_live`, `loadContextual_top`, `loadUsing_leaf_closed`, `load_closed_live`, `selectHole_nodes`, `selectHole_origin`, and the six `DeployedContextual` successes).
- `why.toUTF8` → `why.wire.toUTF8` on `blocked_step` and `resolveHole_refusal`, plus the `String` → `HoleRefusal` on `why`.
- `"holeSupportMoved 0 1"` → `.supportMoved 0 1` on `used_hypothesis_suspends`. The token diff is split across string tokens; the forall count is still `(0, 0)`.
- `256` → `Bounds.holeGuardFuel` on `runHoleGuard_cost`.
- `String` → `ExpansionBound` on `fillBounded_bounds`. Its source is not in the patch; the statement is still `fillBounded … = .ok result → nodes result ≤ limit ∧ …` [READ `origin/main:Lang/Proofs/HoleBudget.lean:154–156`]. The error type rides on `.ok`.

**The 6 that did not move,** all in §3's 33, none a meaning change:

| theorem | why the digest stays |
|---|---|
| `resolutionMax_committed` | [READ `origin/main:Lang/Proofs/LiveHoles.lean:340–343`] `resolutionMax (map resolve) ≤ foldl nodes 1`. Two `Nat`s. The blocked reason is not in the statement. VALUE moves (the proof unfolds `HoleResolution.body`); TYPE does not. |
| `loadLive_checked` | [READ `:275–280`] `loadLive … = .ok` implies `checkShape`, `checkFields`, `packageWire`. `loadLive`'s type is `Except (Refusal D)`, and that did not change. VALUE moves because the proof applies `admitContextual_inv`. |
| `loadLive_libTy` | [READ `:261–265`] `LibTy` of a `loadLive` success. Same reason. |
| `loadLive_of_load` | [READ `origin/main:Lang/Proofs/LiveClosed.lean:122–127`] `load = .ok` implies `loadLive = .ok` and `preparationCost = 0`. No `String`, no `256`. The proof calls `load_closed_live`, whose type did move; this statement does not. |
| `method_live_run_sound` | [READ `origin/main:Lang/Proofs/LiveInvoke.lean:16–25`] `RunOK` of `run` after `loadLive = .ok`. Neither TYPE nor VALUE. |
| `invoke_live_never_stuck` | [READ `:38–51`] the same, via `loadLive_checked`. Neither TYPE nor VALUE. |

They were in the 33 because the design's census followed `loadLive` / `resolveHole`. The statements never mention the string or the literal. The gate was ⊆, and 27 ⊆ 33 holds.

[MEASURED `diff-S9.txt` AUX] `inferE._mutual` sub-proof statement multisets are not equal (24 before, 24 after). That is the mutual def's internal proofs moving with the checker type once the default is gone, which the BUILT section names. It is not a 28th landed theorem and not a new hypothesis. The closed API in `Lang/Proofs/Check.lean` changes source (`(Ω := [])`) and not digest: the default already elaborated to `[]`. One Kernel VALUE, `object_history_start`, no Kernel/Ledger/Host TYPE line. [READ the census, not the Kernel proof.]

## (4) The proof repairs

[READ the `Lang/Proofs/LiveHoles.lean` hunk, and the `LawMeaning` / `LiveClosed` / `LiveJourney` hunks.] No `sorry`. No `admit` tactic (`admitContextual` is the function). No `native_decide`. The `decide +kernel` lines that appear only gain `(Ω := [])`. No `open … in` is added; nothing changes what a name resolves to.

`unresolvedBody_field`'s statement is not in the diff. The proof gains one `split` for the explicit `match` on `fillBounded` and then the old `repeat' split`. `instantiateHoles_cost`'s statement is not in the diff (`i.cost ≤ p.preparationCost`); the proof unfolds both sides through `holeCharge` and still uses `resolutionMax_committed`. `used_hypothesis_suspends` is still `rfl`. `strengthening_factor` changes `ε := String` to `ε := HoleRefusal` and writes `(Ω := [])`; the ok tuple is the same. `runHoleGuard_cost` is `used ≤ Bounds.holeGuardFuel` with `run_used_le` at that name. None of these is a weaker claim.

## (5) The journey row

I did not re-run the journey. [READ IMPACT-S9 BUILT] reports default byte-identical (787 lines), `--contextual` byte-identical (182 lines), `--contextual-checks` identical plus `ok   LP recheck-arm-reachable`. That is consistent with the patch: `boundaryRows` changes one comparison from the string `"holeCandidateType 0 0"` to the constructor whose wire is that string, so a true row stays `ok`; the only new `gateRows` entry is the plant.

The new row's expected verdict is the refusal, not an admission. [READ patch `ContextualChecks.lean`] the Bool is `refusedAs … wideP .instanceRecheck && (instantiateHoles … p).isOk`. `ok   LP` means that Bool is true. The wide package must be `.error .instanceRecheck`. The `.isOk` is the name-0 control.

It does exercise the reachable arm, by a ROM name past `reasonMax`. [READ `origin/main:Lang/Journey/Contextual.lean:58–68`] `view none …` at rel 5 is `[(key, none)]`: the point is present and the leaf is absent. `holeRow` returns `.ok none` (unpinned is the key missing entirely). `selectHole` then throws `.selectionAbsent h.name` [READ `origin/main:Lang/LiveHoles.lean:101`, and the same arm in the patch]. `wideP` sets that name to `10 ^ 300` and leaves `selectionKey` as `key`, so the lookup still hits. The blocked body is `.refuse .nat "holeSelectionAbsent <digits>"`. [READ `origin/main:Lang/Bounds.lean:36–39`, `Lang/Check.lean:172–174`] `reasonOk` rejects `size > reasonMax` (256), and `inferE` on `.refuse` returns `.badReason`. `digestLits` of `.refuse` is `[]` [READ `origin/main:Lang/Package.lean:497`], so provenance does not fire first, and `checkShape` does not bound a hole name [READ `origin/main:Lang/Package.lean:431–436`]. `"holeSelectionAbsent "` is 20 bytes and the decimal of `10^300` is 301 digits: 321 > 256. The name-0 control is `"holeSelectionAbsent 0"`, 21 bytes, which `reasonOk` accepts, so the same view admits `p`. The arm the old design called dead is the arm this row demands.
