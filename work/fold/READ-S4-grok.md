VERDICT: RELEASE S4

Nothing that survives is weaker. The fourteen modules are a closed import set on `origin/main` `e1ccc50`: every importer of any of them is one of them. The live package, `LangCalculus`, the `Std.hole` generator, and the journey do not use a repair, transport, or boundary notion from these fourteen. No deleted theorem is the only statement of a deployed repair behaviour. The hole package's repair rows stay, and they do not depend on these modules or on `Closure.repair` / `Trace.repair`.

The Trace docstring fix is yes. It is in the proposed diff, and it belongs there.

`origin/main` after `git fetch origin` is `e1ccc508d330e5835ef271fbad15f806d8cf5753` (`lang: delete P5, the games, the nogoods, the material guards and C/P1`). Local `main` is `7e02852`, behind. Nothing below was read from the working tree. No build.

## What is not weaker

The deployed repair behaviours of the hole package already have their own statements, and S4 does not touch them. [READ `Lang/Proofs/Contextual/Deployed.lean:43,59,67,75,83`]

- `strengthening_factor`, `kept_context`, `alternative_same_filling`, `replacement_filling`, `used_hypothesis_suspends` are about `Std.contextualHole` / `selectHole`.
- `selectHole_origin`, `resolveHole_refusal`, `hole_rejudge_status`, `hole_judgment_admission_bridge` stay in `LiveHoles` and `HoleBridge`. [READ `Lang/Proofs/Contextual/LiveHoles.lean:39,60`; `HoleBridge.lean:113,228`]

The spine's repair stays. `Closure.Outcome` is the five cases `kept`, `replacement`, `strengthening`, `alternative`, `suspended`. [READ `Lang/Contextual/Closure.lean:179–187`] `repair_agrees_from_scratch`, `repair_rejudged_eq_touched`, and `conditional_soundness` stay in `P/Repair` and `P/Soundness`. [READ `Lang/Proofs/Contextual/Repair.lean:112`; `Soundness.lean:16`] `RepairObjects.Outcome` is a second type: `| existing (outcome : Outcome D)` plus `| transported`. [READ `Lang/Contextual/RepairObjects.lean:36–39`] Its `conditional_soundness` is about that second type. Deleting it does not thin the spine's.

`judge_frame` is the spine's boundary lemma ("An edit that does not touch a candidate leaves its judgment unchanged") and it stays. [READ `Lang/Proofs/Contextual/Judge.lean:34–36`] So do `judge_pruned`, `judge_verified_iff`, `withdraw_never_refutes`, `withdraw_never_prunes`. [READ `Judge.lean:57,94,162,175`] `pruning_explanation_reopens_region` is a corollary of those over a private search session, not the only statement, and not a statement about `selectHole`.

`Trace.collect` stays. `StdHoleModel.holeCoverageOutcome` is its one deployed caller. [READ `Lang/StdHoleModel.lean:63–68`] `Trace.repair` and `dirtyReaders` are not called from the hole package; S11 owns them, not S4.

No lakefile root names a deleted module. `lean_lib Lang` is `globs := #[.submodules `Lang]`. [READ `lakefile.lean:35–36`] No `gates/*.tsv` row and no `rows/run` line names one. [MEASURED the grep in spot-check 3]

Two importers shrink and do not go empty of content:

- `P/History` is imported only by `P/RepairObjects`. [MEASURED spot-check 3] After S4 the glob still builds it. Its theorems (`select_requires_available`, `executed_prefix_blocks_replan`, `consumer_boundary`, `session_preserves_*`) are the spine's, and they stay. Unimported is not toothless. [READ `Lang/Proofs/Contextual/History.lean:15,41,85`]
- `P/Stability` is imported by `P/TransportKinds` and `P/Worlds`. After S4 only `P/Worlds` remains. [MEASURED spot-check 3] That matches IMPACT §1. Not weaker. S5's problem, not this one.

## The live path does not use the fourteen

There is no `Lang/Contextual/Live*.lean`. The live files are `Lang/LiveHoles.lean` and `Lang/Proofs/Contextual/Live{Holes,Invoke,Cost,Need}.lean`.

`LiveHoles` imports `Package`, `HoleBudget`, `Eval`, `Wire.Data`, `Kernel.Receive.Call`. [READ `Lang/LiveHoles.lean:2–6`] `selectHole` / `resolveHole` speak `Except String` / `HoleResolution`. [READ `LiveHoles.lean:100,130`] `LangCalculus` imports `LangSubstitution`, `Core`, `Closure`. [READ `Lang/Contextual/LangCalculus.lean:15–17`] `StdHole.holePackage` and `Std.contextualHole` do not import the fourteen. `StdHoleModel` imports `Trace` only, and uses `collect` only.

The hole package's repair journey rows are `Journey.Contextual.boundaryRows`. The name collides with the module; the function does not. Its docstring: "Positive and negative boundary probes, also called by the signed journey. These are not a replacement for submit/World.admit rows." [READ `Lang/Journey/Contextual.lean:100–102`] The rows that are the repair behaviours are `strengthened-value`, `strengthened-context`, `kept-context`, `alternative-same-filling`, `replacement-value`, `used-hypothesis-withdrawn`, `derivation-withdrawn`. They call `selectHole`, `resolveHole`, and `program.run` on `Std.contextualHole`. [READ `Contextual.lean:17–42,102–155`] Imports of that file: `StdContextualHole`, `Print`, `Program`, `Kernel.Sim`. `ContextualReceive` replays them ("Deployed contextual repair through signed Receive.submit and World.admit") and imports `Journey` and `Journey.Contextual` only. [READ `Lang/Journey/ContextualReceive.lean:1–3,22`]

`Std.holeCheckRows` is the other hole-package journey list: refusal rows for `select`, `propose`, `fill`, `accept`, `posted`, `proposed`, `shape`. [READ `Lang/Journey/HoleChecks.lean:1,86–130`] It imports `Journey.Hole`, which imports `StdHole`. The word `repair` does not occur in it.

So those rows depend on the live hole package. They do not depend on the fourteen, and they do not depend on `Closure.repair` or `Trace.repair`.

`BoundarySearch.Term` is `binary | linear | var | hole`, "not an encoding of deployed Lang terms." [READ `Lang/Contextual/Boundary.lean:64–70`] The one `repair` call in that file is the spine's `repair` on the toy session, a client of `Closure`, not a provider to the live path. [READ `Boundary.lean:175`] A grep of the fourteen for `LiveHoles`, `fillRefs`, `holePackage`, `Std.hole` is empty. [MEASURED spot-check 2]

## (2) The diff

Confirmed from the diff, not re-elaborated.

[MEASURED `fold/diff-S4.txt`]

```
before 52625 after 51739
vanished 886 of which outside the declared modules 0
declared-module constants 887 all vanished: False
new 0 type-digest changed 0 value-hash changed 0 module changed 1
   Nanodregg.Lang.Contextual.Iface.decl.eq_1
```

`52625 − 51739 = 886`. The 887th constant did not vanish: `Iface.decl.eq_1` changed module. `Iface.decl` is the surviving def at `Closure.lean:121` (`HoleDecl` of name, ctx, ty). [READ] `type-digest changed 0` and `value-hash changed 0` are the "no statement or value-hash change outside" claim. I did not re-run the census. The import closure below agrees with the "nothing outside refers" half.

[MEASURED `fold/S4-size-preview.txt`] modules 518 → 504 (−14), proof-modules 280 → 273 (−7), Lang lines 44794 → 43047 (−1747), theorems 6228 → 6126 (−102), "Lean lines (deployed)" 30375 → 29763 (−612).

The −102 is the `theorem` keyword count, not the appendix's 109. [MEASURED `git grep -c` of `^theorem ` / `^private theorem `] Boundary 29, ModalBoundary 8, ContextMorphisms 9, RepairChanges 10, TransportKinds 9, RepairObjects 23, ProvenanceRepairs 14. Sum 102. The seven extra in the appendix are fields of Prop structures (`Repair.Sound.coherent` / `.problem`, `Correspondence.Checked`'s four, `RepairChanges.Laws.update_difference`), which `size.py` does not count as theorems. [INFERRED from IMPACT's list plus this count; not re-elaborated]

The −612 "deployed" lines are the seven def modules (179+86+36+35+48+188+40). [MEASURED arithmetic against IMPACT §1's line counts] `size.py` counts def modules under `Lang` as deployed. They are not in the host import closure. [INFERRED] The host does not get weaker by that line.

## (3) The Trace docstring

Yes. [READ `Lang/Contextual/Trace.lean:125–127`]

```
/-- Only holes reading a changed selection status are dirtied. Other behavior needs its
own Boundary declaration. Mokhov et al. 2018, §2.3 p.79:5, §4.2.2 p.79:15. -/
def dirtyReaders
```

After S4 there is no Boundary declaration. `dirtyReaders` filters reader pairs by `r.2 ∈ p.changed` and nothing else. [READ `Trace.lean:127–128`] The proposed sentence ("Only holes reading a changed selection status are dirtied; no other dependency is tracked here.") matches the def. It is a docstring on a def S11 deletes. The olean of `Trace` changes in that comment only. Land it in S4. Leaving the sentence would leave a false pointer in a surviving def; the proposal does not leave it.

Pickaxe: the sentence entered in `0a8c780`, file `Lang/Contextual/Trace.lean` only. [MEASURED spot-check 3]

## Spot-checks

### 1. Import closure of the fourteen, at `e1ccc50`

Command:

```
git --git-dir=/Users/ember/dev/nanodregg/.git grep -n "import Lang.Contextual.Boundary\|import Lang.Proofs.Contextual.Boundary\|import Lang.Contextual.ModalBoundary\|import Lang.Proofs.Contextual.ModalBoundary\|import Lang.Contextual.ContextMorphisms\|import Lang.Proofs.Contextual.ContextMorphisms\|import Lang.Contextual.RepairChanges\|import Lang.Proofs.Contextual.RepairChanges\|import Lang.Contextual.TransportKinds\|import Lang.Proofs.Contextual.TransportKinds\|import Lang.Contextual.RepairObjects\|import Lang.Proofs.Contextual.RepairObjects\|import Lang.Contextual.ProvenanceRepairs\|import Lang.Proofs.Contextual.ProvenanceRepairs" e1ccc508d330e5835ef271fbad15f806d8cf5753
```

Every hit is inside the fourteen:

- `Boundary` ← `ModalBoundary`, `P/Boundary`
- `P/Boundary` ← `P/ModalBoundary`
- `ModalBoundary` ← `P/ModalBoundary`
- `ContextMorphisms` ← `P/ContextMorphisms`
- `RepairObjects` ← `ProvenanceRepairs`, `RepairChanges`, `TransportKinds`, `P/RepairObjects`
- `RepairChanges` ← `P/RepairChanges`
- `P/RepairObjects` ← `P/RepairChanges`
- `TransportKinds` ← `P/TransportKinds`
- `ProvenanceRepairs` ← `P/ProvenanceRepairs`

`Lang/Journey.lean` does not import `TransportKinds`. The map's outside edge is gone. [MEASURED]

```
git --git-dir=/Users/ember/dev/nanodregg/.git log -S "import Lang.Contextual.TransportKinds" --pretty=format:"%h %s" --name-only e1ccc508d330e5835ef271fbad15f806d8cf5753
```

- `a9ab514` `lang: drop the journey's p8 toy calculus…` — `Lang/Journey.lean` (the removal)
- `ad96bab` — `Lang/Journey.lean` (the add)
- `f15b70f` — `P/TransportKinds.lean`

```
git --git-dir=/Users/ember/dev/nanodregg/.git log -S "import Lang.Contextual.RepairObjects" --pretty=format:"%h %s" --name-only e1ccc508d330e5835ef271fbad15f806d8cf5753
```

`c58757f` `ProvenanceRepairs.lean`; `f15b70f` `RepairChanges.lean`, `TransportKinds.lean`; `06da84f` `P/RepairObjects.lean`. No file outside the fourteen, ever.

```
git --git-dir=/Users/ember/dev/nanodregg/.git log -S "import Lang.Contextual.Boundary" --pretty=format:"%h %s" --name-only e1ccc508d330e5835ef271fbad15f806d8cf5753
```

`f15b70f` `ModalBoundary.lean`; `1b6cd0d` `P/Boundary.lean`. No file outside, ever.

### 2. The private language, the second Outcome, and the live repair rows

[READ `Lang/Contextual/Boundary.lean:1–2,64–70,175`] header "no wire or existing judgment changes"; `Term` is `binary | linear | var | hole`; `pruningReport` calls spine `repair` on `BoundarySearch`'s own closure.

[READ `Lang/Contextual/Closure.lean:179–187` and `RepairObjects.lean:36–39`] five outcomes versus `existing` plus `transported`.

[READ `Lang/Journey/Contextual.lean:1–5,100–155`] `boundaryRows` is the live ROM. [READ `Lang/Proofs/Contextual/Deployed.lean:3–4`] imports `Journey.Contextual` and `LiveHoles`, not the fourteen, and states `strengthening_factor`, `kept_context`, `alternative_same_filling`, `replacement_filling`.

```
git --git-dir=/Users/ember/dev/nanodregg/.git grep -n -e "LiveHoles" -e "fillRefs" -e "holePackage" -e "Std.hole" e1ccc508d330e5835ef271fbad15f806d8cf5753 -- Lang/Contextual/Boundary.lean Lang/Contextual/RepairObjects.lean Lang/Contextual/TransportKinds.lean Lang/Contextual/ProvenanceRepairs.lean Lang/Proofs/Contextual/Boundary.lean Lang/Proofs/Contextual/RepairObjects.lean Lang/Proofs/Contextual/TransportKinds.lean Lang/Proofs/Contextual/ProvenanceRepairs.lean
```

Empty.

```
git --git-dir=/Users/ember/dev/nanodregg/.git grep -n -e "RepairObjects" -e "TransportKinds" -e "ModalBoundary" -e "ContextMorphisms" -e "RepairChanges" -e "ProvenanceRepairs" -e "BoundarySearch" e1ccc508d330e5835ef271fbad15f806d8cf5753 -- Lang/LiveHoles.lean Lang/Contextual/LangCalculus.lean Lang/StdHoleModel.lean Lang/StdContextualHole.lean Lang/Std.lean Lang/HoleROM.lean Lang/Journey.lean Lang/Journey/HoleChecks.lean Lang/Journey/Contextual.lean Lang/Journey/ContextualReceive.lean Lang/Proofs/Contextual/LiveHoles.lean Lang/Proofs/Contextual/HoleBridge.lean Lang/Proofs/Contextual/Deployed.lean
```

Empty.

### 3. Gates, rows, lakefile, History, Stability, the docstring

```
git --git-dir=/Users/ember/dev/nanodregg/.git grep -n -e "Boundary" -e "RepairObjects" -e "TransportKinds" -e "repair" e1ccc508d330e5835ef271fbad15f806d8cf5753 -- rows/run gates lakefile.lean
```

Hits are `gates/journal-report.md` prose ("Protocol repair theorem", "repaired support"). No tsv row, no `rows/run` line, no lakefile hit. [READ `lakefile.lean:7,35–36,108`] globs, and `lang-journey`'s root is `Lang.Journey.Main`.

```
git --git-dir=/Users/ember/dev/nanodregg/.git grep -n "import Lang.Proofs.Contextual.Stability\|import Lang.Proofs.Contextual.History\|import Lang.Contextual.Trace" e1ccc508d330e5835ef271fbad15f806d8cf5753 -- "*.lean"
```

- `History` ← `P/RepairObjects` only
- `Stability` ← `P/TransportKinds`, `P/Worlds`
- `Trace` ← `P/Trace`, `Lang/StdHoleModel.lean`

```
git --git-dir=/Users/ember/dev/nanodregg/.git log -S "own Boundary declaration" --pretty=format:"%h %s" --name-only e1ccc508d330e5835ef271fbad15f806d8cf5753
```

`0a8c780`, only `Lang/Contextual/Trace.lean`.

All fourteen paths are in `git ls-tree -r --name-only e1ccc50 -- Lang/Contextual Lang/Proofs/Contextual`.
