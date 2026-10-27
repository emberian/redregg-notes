VERDICT: RELEASE S8

No landed theorem gains a hypothesis. `foldMax_member`'s statement is unchanged, source and digest; its proof value changes because the nil-case `simp at ha` no longer emits its own auxiliary. The two kept-separate modules are forced: merging `LiveNeed` cycles through `Provenance`, and merging `LiveInvoke` adds `Lang.Proofs.Invoke` and `Lang.Proofs.Read` to `InvokeWitness`. The result is one module per concept, stricter than the map, not a new pile. The Kernel/Ledger diff is exactly four import lines, and after them no Kernel or Ledger module imports `Lang.Proofs.Contextual` or `Lang.Contextual`.

`origin/main` after `git fetch origin` is `3944bbff0139f08765d1fc81d3d75adc4e1095f3` (`3944bbf`, S7). The candidate is `fold/S8-candidate.patch` (923 lines, 16 files). No build. The builder's GREEN, the closure sizes 94/120/138, and the byte-equality of the two simp-aux types are theirs; the import edges, the hunks, and `fold/diff-S8.txt` were checked here.

## (1) Move invariant

[MEASURED `fold/diff-S8.txt`] `before 51138` `after 51135` (`51138 − 3 + 0 = 51135`). `vanished 3 declared 0 UNDECLARED 3`. `new 0`. `type-digest changed 0`. `value-hash changed 5`. `module changed 555 of which from a module the step does not move 3`. There is no TYPE line.

`foldMax_member` is the one user constant in VALUE. It is not in TYPE.

[READ `Lang/Proofs/Contextual/LiveCost.lean:36–39`]

```
theorem foldMax_member {α : Type} (f : α → Nat) (xs : List α) (n : Nat)
    (a : α) (ha : a ∈ xs) : f a ≤ xs.foldl (fun n a => max n (f a)) n := by
  induction xs generalizing n with
  | nil => simp at ha
```

[READ `fold/S8-candidate.patch`, the `LiveHoles` addition] the same four lines, binders and conclusion and the nil-case `simp at ha`, copied into the `LiveCost` section. Not a weaker statement.

The auxiliary. `foldMax_member._simp_1_1` is one of the three vanished names, and nothing is new, so the nil-case simp did not mint a replacement constant. [MEASURED `diff-S8.txt`] The parent is in VALUE, so the proof term changed and the type did not. That is what Lean's per-module simp-aux cache does when a lemma of the same type is already in the file: it cites the old one and drops the new name. The lemma the impact names, `loadAllUsing_inv._simp_3`, already lives in `P/LiveHoles` [READ `LiveHoles.lean:217–232`, the `simp`/`simp at h` sites in that proof]. Its type string was not re-read here — `diff-S8.txt` lists names only, and this read did not elaborate — so "byte-equal" is the builder's comparison. It is the only account that fits vanished + new 0 + parent in VALUE not TYPE. A different statement would have been a new constant or a TYPE line.

Anything else, all generated, none a premise:

- VANISHED, the other two: `_private…selectHole.match_5.splitter._sparseCasesOn_3` and `match_8.splitter._sparseCasesOn_3`, module `P/LiveCost`. [MEASURED]
- VALUE, the other four: `Need.runBy.eq_def`; `selectHole.match_5.splitter`; `selectHole.match_8.eq_2`; `selectHole.match_8.splitter`. The three `selectHole` lines are the shared splitters the impact describes. `Need.runBy.eq_def` is an equation lemma. [MEASURED]
- MODBAD, three: `Need.runBy.eq_1`, `.eq_2`, `.eq_def`, module `Lang.Proofs.Need` → `Lang.Proofs.CostTeeth`. Neither file is in the patch [MEASURED `git apply --stat`]. Not in TYPE, so the types match. [INFERRED, the impact's account] the census keeps whichever importer realizes the equation lemma first, and the new module names change that order.
- One module-pair the impact's prose does not name: `ClosedDeployment → LiveHoles` count 1, beside `ClosedDeployment → LiveClosed` 83. Not TYPE, not VALUE, not MODBAD, so a realization home moved between two modules this step does move. Not a statement. The source of `ClosedDeployment` stays in `LiveClosed` [READ the rename hunk]; the constant is not a declaration that was pasted into `LiveHoles`.

No user name is vanished, new, or TYPE-changed. The nine renamed user names are ContractTeeth's eight teeth plus private `identityCandidate_typed` [READ `fold/S8-renames.tsv`, 21 lines: those 9 and 12 `_private:` rows]. Their statements are the deleted `ContractTeeth` body, pasted into `LiveTeeth` [READ both]. The namespace leaves `Contextual`. That is a rename, and none of those names is in TYPE or VALUE.

## (2) The two deviations

Map §2.1 puts `P/LiveNeed` and `P/LiveInvoke` inside `Lang/Proofs/LiveHoles`, with `P/LiveHoles` and `P/LiveCost`. §4.2's "11→6" does not match that row: the row's sources are 12 (4+2+1+1+2+2). Landed is 12 files → 8 modules. [MEASURED `SIZE.md` on `origin/main`: 498 modules, 269 proof-modules, Lang lines 42185; `fold/S8-size-preview.txt`: 494, 265, 42279.] Net −4 is the four merges that did happen, not the six the map counted. The two that did not are these.

**`LiveNeed` kept separate. The cycle is real.** Today there is none: `P/LiveHoles` imports `Load`, `HoleBudget`, `Run` only [READ the header], and that closure does not reach `Need` or `Provenance` (walked below). `P/LiveNeed` imports one module [READ `LiveNeed.lean:2`, and the patch keeps that import in its own file].

```
LiveNeed:2 → NeedComplete:17 → Need:30 → Extract:60 → Provenance:36–37
                                                      → LiveInvoke:1 → LiveHoles
                                                      → ClosedDeployment:2 → LiveHoles
```

[MEASURED `git grep -e '^import '` at `3944bbf` for the four numbered edges; READ `Provenance.lean:36–37` `LiveInvoke` and `ClosedDeployment`; READ `ClosedDeployment.lean:2` and `LiveInvoke.lean:1`.] Merged into `LiveHoles`, the `NeedComplete` import sits on a module `Provenance` already reaches, by both return edges. The patch's own header says this, a little loosely ("Provenance uses LiveHoles"): the direct imports are `LiveInvoke` and `ClosedDeployment`. The top-level `variable {D} {bytesOf} {digestOf}` [READ `LiveNeed.lean:4`] is why the body is wrapped in `section`; it is not what forces the separate file.

**`LiveInvoke` kept separate. The widening is real.** It imports `LiveHoles` and `Invoke` [READ `LiveInvoke.lean:1–2`]. `Invoke` imports `Load`, `Data`, `Canon`, `Read` [READ `Invoke.lean` header]. `Read`'s only importer in the tree is `Invoke` [MEASURED `git grep import Lang.Proofs.Read` at `3944bbf`, one hit]. `Invoke`'s importers are exactly five: `History.lean:50`, `CallLive.lean:18`, `LiveInvoke.lean:2`, `EscrowRun.lean:58`, `Protocol/Proofs/Command.lean:18` [MEASURED `git grep import Lang.Proofs.Invoke`].

`InvokeWitness` reaches none of those five. Its proof imports are `InvokeNext`, `Wire`, `Receiver`, `ClosedLeaf` [READ `InvokeWitness.lean:33–38`]. `ClosedLeaf` → `ClosedDeployment` → `LiveHoles` → `Load`, `HoleBudget`, `Run`. Following proof imports out of that set (Tree, Frame, Fold, Receive, Lawful, Std, Fill, Subst, Data, Canon, the codec proofs under Wire and Lawful) never imports `Lang.Proofs.Invoke`, `CallLive`, `Extract`, `Provenance`, or `LiveInvoke`. The only `import Lang.Proofs` lines under `Kernel/Proofs` and `Codec/Proofs` are `InvokeWitness` itself, `History`, and the two witnesses that import those [MEASURED `git grep 'import Lang.Proofs'` on those two trees]. So `Invoke` and `Read` are not in the closure.

`Data` and `Canon` already are: `Receiver` → `Std` → `StdData` imports both [READ those headers]. `Load` already is, through `LiveHoles`. `Lang.Read` (the def) already is, through `Program` [READ `Program.lean:23`]. Merging `LiveInvoke` into `LiveHoles` therefore adds exactly two modules to `InvokeWitness`: `Lang.Proofs.Invoke` and `Lang.Proofs.Read`.

The arithmetic the impact quotes matches that. `ClosedLeaf` and `ClosedDeployment` are both in the closure and become one `LiveClosed` [READ `fold/S8-closures.txt`: lost those two plus `LiveHoles`, gained `LiveClosed` and `LiveHoles`]. 94 − 1 = 93 kept apart; 94 − 1 + 2 = 95 if merged. `History` stays 120 because it already imports `Invoke` at line 50 and already reaches `LiveInvoke` through `Extract` → `Provenance` [READ `History.lean:48–51`; READ the closures file: lost and gained `LiveInvoke`]. `EscrowRun` already imports `Invoke` at line 58, so the same merge widens it by nothing; 138 → 137 is only the leaf/deployment collapse. `LiveJourney` would gain the same pair (`Deployed` imports `LiveHoles` and `Journey.Contextual` only [MEASURED]), which is a leaf, not the Kernel closure the map's law 8 is about.

**Not a new pile.** The map's "one module per concept" had stacked need-bounds and invoke-soundness onto the live-hole file. Keeping them apart is that rule, applied where the import graph forbids the stack. What did merge is the map's own grouping: cost with the live holes, the leaf forms with closed deployment, the two tooth files, the journey facts with the cycle filling. Eight homes, each the concept §2.1 already named, with two of its piles undone.

## (3) The four foreign lines

[MEASURED `git apply --stat --summary fold/S8-candidate.patch`] Kernel and Ledger appear as three files: `InvokeWitness` 2 lines, `History` 2, `EscrowRun` 4. Nothing else outside `Lang/Proofs/`. The hunks are import lines only [READ the patch]:

```
InvokeWitness.lean:38   import Lang.Proofs.Contextual.ClosedLeaf  → import Lang.Proofs.LiveClosed
History.lean:51         import Lang.Proofs.Contextual.LawReceiver → import Lang.Proofs.LawReceiver
EscrowRun.lean:59       import Lang.Proofs.Contextual.ClosedLeaf  → import Lang.Proofs.LiveClosed
EscrowRun.lean:60       import Lang.Proofs.Contextual.LawReceiver → import Lang.Proofs.LawReceiver
```

`EscrowRun:58` `import Lang.Proofs.Invoke` is untouched context. `Lang/Proofs/Provenance.lean:36–37` changes the same way (`LiveInvoke`, `LiveClosed`); that file is Lang, not one of the four.

Before, those four lines are the only `import Lang.Proofs.Contextual` or `import Lang.Contextual` in all of `Kernel/` and `Ledger/` [MEASURED `git grep` at `3944bbf`]. The patch rewrites each of them. After it, no Kernel or Ledger module — proof or otherwise — imports either prefix.

[READ `fold/S8-closures.txt`] `InvokeWitness` 94 → 93, `History` 120 → 120, `EscrowRun` 138 → 137, `Provenance` 87 → 87, `Host.Main` 89 → 89. What each loses is a `Contextual` proof module; what it gains is the renamed home. No new dependency. The −1 on `InvokeWitness` and `EscrowRun` is `ClosedLeaf` + `ClosedDeployment` becoming `LiveClosed`. `History` never imported `ClosedLeaf`, so its count does not move.

## (4) Premises

[MEASURED `fold/diff-S8.txt`] type-digest changed 0. A gained hypothesis is a different elaborated type. No user theorem, def, or structure has one.

Source side, the non-move edits are headers, import paths, and `section`/`end` around each old file. Checked against the hunks: `LawMeaning` (import `ClosedDeployment` → `LiveClosed`, section), `LawReceiver`, `LiveInvoke` (`LiveHoles` path only; `import Lang.Proofs.Invoke` stays), `LiveNeed` (section around the existing `variable`), `LiveClosed` (appended `ClosedLeaf` theorems, statements copied), `LiveJourney` (appended `DeployedCycle`, plus that file's two imports). The four leaf theorems `InvokeWitness` and `EscrowRun` consume are the deleted `ClosedLeaf` body [READ `ClosedLeaf.lean` in the patch, against the `LiveClosed` addition]. Binders unchanged. Dropping no `open` and adding no binder.

## Spot-checks

```
git -C /Users/ember/dev/nanodregg fetch origin
git -C /Users/ember/dev/nanodregg rev-parse origin/main
→ 3944bbff0139f08765d1fc81d3d75adc4e1095f3
  3944bbf lang: the deployed-subject substitution and filling proofs leave Contextual: … (S7)

git --git-dir=…/.git grep -e "import Lang.Proofs.Contextual" -e "import Lang.Contextual" 3944bbf -- Kernel Ledger
→ InvokeWitness.lean:38   import Lang.Proofs.Contextual.ClosedLeaf
  History.lean:51         import Lang.Proofs.Contextual.LawReceiver
  EscrowRun.lean:59       import Lang.Proofs.Contextual.ClosedLeaf
  EscrowRun.lean:60       import Lang.Proofs.Contextual.LawReceiver

git --git-dir=…/.git grep -e "import Lang.Proofs.Invoke" 3944bbf
→ History.lean:50
  CallLive.lean:18
  LiveInvoke.lean:2
  EscrowRun.lean:58
  Protocol/Proofs/Command.lean:18

git --git-dir=…/.git grep -e "import Lang.Proofs.Read" 3944bbf
→ Lang/Proofs/Invoke.lean:18

git -C /Users/ember/dev/nanodregg blame -L '/theorem foldMax_member/,+4' origin/main -- Lang/Proofs/Contextual/LiveCost.lean
→ :36 theorem foldMax_member …
  :39   | nil => simp at ha

git -C /Users/ember/dev/nanodregg show origin/main:SIZE.md
→ | Lean modules in the Host closure | 89 | 150 |
  | Lean modules | 498 |
  | Lean proof-modules | 269 |
  | Lean lines (Lang) | 42185 |
  | max dependents of a non-foundation module | 349 |
```

`fold/diff-S8.txt`, checked against the names rather than the prose:

```
before 51138 (rows carrying a renamed-from name: 290 ) after 51135
vanished 3 declared 0 UNDECLARED 3
new 0 type-digest changed 0 value-hash changed 5
module changed 555 of which from a module the step does not move 3
   ClosedDeployment -> LiveClosed 83
   ClosedDeployment -> LiveHoles   1
   ClosedLeaf       -> LiveClosed 13
   ContractTeeth    -> LiveTeeth  10
   Deployed         -> LiveJourney 30
   DeployedCycle    -> LiveJourney  3
   LawMeaning       -> LawMeaning 159
   LawReceiver      -> LawReceiver  57
   LawReceiverTeeth -> LiveTeeth   44
   LiveCost         -> LiveHoles   22
   LiveHoles        -> LiveHoles   96
   LiveInvoke       -> LiveInvoke   2
   LiveNeed         -> LiveNeed    32
   Need             -> CostTeeth     3
VANISHED foldMax_member._simp_1_1
VANISHED selectHole.match_5.splitter._sparseCasesOn_3
VANISHED selectHole.match_8.splitter._sparseCasesOn_3
VALUE    Need.runBy.eq_def
VALUE    foldMax_member
VALUE    selectHole.match_5.splitter
VALUE    selectHole.match_8.eq_2
VALUE    selectHole.match_8.splitter
MODBAD   Need.runBy.eq_1
MODBAD   Need.runBy.eq_2
MODBAD   Need.runBy.eq_def
```
