VERDICT: RELEASE S7

The three theorems are `Term.shiftAt_unshiftAt`, `hasType_unshiftAt_live`, and `usesVar_shiftAt`. Their statements are unchanged, source and digest. The `._proof_N` shift is which abstracted sub-proof an index denotes, not a premise. The other residual is the same generated matcher/equation class as S6, plus 22 private copies of `renameVar`/`renameVarList` matchers that `P/HoleBudget` stops realizing once it shares `Subst`. No user theorem is in the TYPE list, so none gains a hypothesis. After the patch, `Kernel/Proofs/InvokeWitness`, `Kernel/Proofs/Logic/History`, and `Ledger/Proofs/EscrowRun` no longer reach `C/Core`, `P/Core`, or `P/Typing`: the only edge was `LangRenaming` → `P/Core`, and `Lang/Proofs/Subst` imports `Lang.Proofs.Index` instead. The toy core is not reached by a deployed def-module or by a proof of a deployed object. It is reached by `P/Core`, `P/Typing`, `C/CoreCalculus`, the leaf `P/CoreInstance`, and the leaf `P/ProvenanceTeeth`. `P/Judge` and `P/LangInstance` reach `Closure`, not the CMTT core.

`origin/main` after `git fetch origin` is `d3e850d7c104b7095a07a4a5ddcbe458d9b1f8ca` (`d3e850d`, S6). The candidate is `fold/S7-candidate.patch` (921 lines, 12 `diff --git` headers, 15 paths: 3 renames count twice). No build. The builder's GREEN, the closure sizes 97/123/141, and the aux-statement multiset are theirs; the import edges, the hunk ranges, and `fold/diff-S7.txt` were checked here.

## (1) Move invariant

[MEASURED `fold/diff-S7.txt`] `before 51195` `after 51176` (`51195 − 26 + 7 = 51176`). `vanished 26 declared 0 UNDECLARED 26`. `new 7`. `type-digest changed 2`. `value-hash changed 5`. `module changed 581 of which from a module the step does not move 0`. Every module-change source is one of `P/Core`, `P/HoleBudget`, `P/LangFilling`, `P/LangOccurrences`, `P/LangRenaming`, `P/LangSubstitution`.

The three theorems, and only these three user constants, are in VALUE. None of them is in TYPE. [READ `Lang/Proofs/Contextual/LangRenaming.lean:263`, `:272–273`, `:381–383`]

```
theorem usesVar_shiftAt (x : Nat) (t : Term) :
    Term.usesVar x (Term.renameVar (liftIdx x) t) = false
theorem Term.shiftAt_unshiftAt {x : Nat} {t : Term} (hu : Term.usesVar x t = false) :
    Term.renameVar (liftIdx x) (Term.renameVar (lowerIdx x) t) = t
theorem hasType_unshiftAt_live … (h : HasType (Ω := Ω) Δ Γ t T) (hu : Term.usesVar x t = false) :
    HasType (Ω := Ω) Δ (Γ.eraseIdx x) (Term.renameVar (lowerIdx x) t) T
```

[READ `fold/S7-candidate.patch`] the `LangRenaming` → `Subst` diff has two hunks, `@@ -1,9 +1,17 @@` (header, import `P/Core` → `Lang.Proofs.Index`, namespace) and `@@ -415,4 +423,140 @@` (append `LangSubstitution`, `end`). Lines 263, 272, and 381 sit in neither hunk, so the statements and the proof scripts move byte-identical. The binders `h` and `hu` are the premises. They do not change.

The `._proof_N` residual is a proof-term artifact. [MEASURED `diff-S7.txt`, the whole TYPE/VALUE/VANISHED/NEW blocks]

| theorem | vanished | kept, type changed | new | theorem itself |
|---|---|---|---|---|
| `Term.shiftAt_unshiftAt` | `._proof_1_1`, `._proof_1_2` | — | `._proof_1_3`, `._proof_1_4` | VALUE, not TYPE |
| `hasType_unshiftAt_live` | `._proof_1_1` | `._proof_1_2` (TYPE and VALUE) | `._proof_1_3` | VALUE, not TYPE |
| `usesVar_shiftAt` | `._proof_1_1` | `._proof_1_2` (TYPE and VALUE) | `._proof_1_3` | VALUE, not TYPE |

That is 4 vanished aux, 4 new aux, the 2 TYPE lines (both the reused name `._proof_1_2`, which now denotes the other sub-proof), and the 5 VALUE lines (the three theorems plus the two reused aux). Nothing else. A `._proof_N` is Lean's name for an abstracted sub-proof inside the term, not a hypothesis on the theorem. [INFERRED, not re-elaborated] the counter skips names already in the environment; sharing a module with `upR`'s matcher lemmas shifts the index. The impact's "multiset of auxiliary statements, 2 = 2" is their comparison of the quoted types. `diff-S7.txt` lists names only, and this read did not rebuild, so that multiset was not re-derived. It is not needed: the theorem types are absent from TYPE, and the source binders are outside every hunk.

Anything else, all generated, none a premise. Same class as the S6 read (matcher `.eq_N` / `.splitter`, realized in whichever module unfolds the def first):

- VANISHED, 22, all `_private…Term.renameVar.match_1.{eq_1..eq_18,splitter}` and `renameVarList.match_1.{eq_1,eq_2,splitter}`, module `P/HoleBudget`. Private copies. Not re-issued: NEW has no `renameVar.match_1` row. They were realized again because `HoleBudget` did not yet see the matchers `LangRenaming` had; `HoleBudget` now imports `Fill` which imports `Subst`.
- NEW, 3: `_private.Lang.Proofs.Subst.0.Nanodregg.Lang.upR.match_1.{eq_1,eq_2,splitter}`.
- Module `P/Core` → `Lang.Proofs.Subst`, count 4, not in TYPE or VALUE. [INFERRED from the count plus where `upR` is first unfolded] the impact's names `upR.eq_1`, `upR.eq_2`, `liftIdx.eq_1`, `lowerIdx.eq_1`. `diff-S7.txt` does not list them one by one. Not a changed statement: a realization moved.

[READ `fold/S7-renames.tsv`] 101 user rows (`Nanodregg.Lang.Contextual.X` → `Nanodregg.Lang.X`) and 5 `_private:` rows, including `upR_upR` and `upR_id` as rows 100–101. The impact's "99 user names" is a stale count; the two index lemmas are the `P/Core` → `Lang.Proofs.Index` 2. No user name is vanished, new, or TYPE-changed.

[READ `Lang/Proofs/Contextual/Core.lean:68–73` against `fold/S7-candidate.patch` `Lang/Proofs/Index.lean`] `upR_upR` and `upR_id` are the same two lines of statement and the same `funext i; cases i <;> rfl`. `P/Core` keeps `import Lang.Proofs.Contextual.Typing` and adds `import Lang.Proofs.Index`. Its `rename_rename` still rewrites with `upR_upR` (the use is not in the deletion hunk).

## (2) The closure

Before, one chain, three consumers. [READ / MEASURED `git blame -L` and `git show origin/main:`]

- `Kernel/Proofs/InvokeWitness.lean:38` `import Lang.Proofs.Contextual.ClosedLeaf`
- `Kernel/Proofs/Logic/History.lean:51` `import Lang.Proofs.Contextual.LawReceiver`
- `Ledger/Proofs/EscrowRun.lean:59–60` `ClosedLeaf` and `LawReceiver`

Both branches meet:

```
ClosedLeaf:1 → ClosedDeployment:2 → LiveHoles:3 → HoleBudget:3 → LangFilling:2
                                                      → LangSubstitution:4 → LangRenaming:4
LawReceiver:1 → LawMeaning:2 ↗                              → P/Core:24 → P/Typing:8 → C/Core:28
```

`LangRenaming.lean:4` is `import Lang.Proofs.Contextual.Core`. `P/Core.lean:24` is `import Lang.Proofs.Contextual.Typing`. `P/Typing.lean:8` is `import Lang.Contextual.Core`. `C/Core.lean:28` imports `Lang.Index` and nothing else, so the modules unique to this edge are exactly the trio. `Lang.Proofs.Load`, `Lang.Proofs.Run`, and `Lang.Proofs.Extract` do not contain `Contextual.Core` [MEASURED `git blame -L '/Contextual.Core/'` exit 128, no match]. No second edge.

What breaks it. [READ `fold/S7-candidate.patch`] `Lang/Proofs/Subst.lean` replaces that import with `import Lang.Proofs.Index`. `Lang/Proofs/Index.lean` imports `Lang.Index` only (no `import` line in `Lang/Index.lean` [MEASURED blame exit 128]). `LiveHoles` line 3 becomes `import Lang.Proofs.HoleBudget`. `HoleBudget` imports `Lang.Proofs.Fill` instead of `LangFilling`. `Fill` imports `Lang.Proofs.Subst` only. `P/LangInstance` imports `Lang.Proofs.Fill` instead of `LangOccurrences`. No Kernel or Ledger file is in the patch. `Lang.Proofs.Check`, which `Subst` still imports, imports `Lang.Proofs.Typing` (the deployed one, `Lang/Proofs/Check.lean:8`), not `P/Typing`.

So after S7 those three closures still contain, from `Lang/Proofs/Contextual/`, `ClosedLeaf`, `ClosedDeployment`, `LiveHoles`, `LawReceiver`, `LawMeaning`. `LiveInvoke` is not on those three chains; `Lang/Proofs/Provenance.lean:36–37` imports it and `ClosedDeployment`, and that closure loses the trio by the same cut. The absolute sizes 97→94, 123→120, 141→138 are the builder's `closure.py`. The −3 is this trio, and the patch removes no other edge into it.

Not reached by anything deployed, nor by a proof of a deployed object.

- Host exe: S7 does not add an import. The only def-module edit is a comment in `Lang/Subst.lean` (the header names `Lang.Proofs.Subst` / `Lang.Proofs.Fill`). `Lang/Subst.lean:15–16` imports `Lang.Check` and `Lang.Index`. `C/Core` left the Host closure at S6 and does not re-enter.
- Proofs of deployed objects that used to ride `LangRenaming`: `LiveHoles`, `LiveInvoke`, `ClosedDeployment`, `ClosedLeaf`, `LawMeaning`, `LawReceiver`, `Lang/Proofs/Provenance`, and `P/HoleBridge` → `P/LangInstance` → `LangOccurrences`. Each of those now stops at `Fill` → `Subst` → `Index`. `P/ContractTeeth` imports only `P/LangInstance` (`ContractTeeth.lean:2`).
- `P/Judge.lean:2` imports only `ClosureStatements`, which imports `Lang.Contextual.Closure` (`ClosureStatements.lean:2`). `Closure.lean:34` imports `Lang.HoleDecl` only. `P/LangInstance` imports `Lang.Contextual.LangInstance`, `Fill`, `ClosureStatements`. The def `Lang/Contextual/LangInstance.lean:13–14` imports `Lang.Subst` and `Lang.Contextual.Closure`. Neither reaches `C/Core`.
- What still reaches the toy core: `P/Typing:8` and `C/CoreCalculus.lean:9` import `C/Core` directly. `P/Core:24` imports `P/Typing`. `P/CoreInstance.lean:17–19` imports `CoreCalculus`, `P/Typing`, and `P/Core`. `P/ProvenanceTeeth.lean:2–3` imports `Judge` and `CoreCalculus`. [MEASURED `git log -S 'import Lang.Proofs.Contextual.CoreInstance' origin/main`] empty, so `CoreInstance` is a leaf. [MEASURED `git log -S 'import Lang.Proofs.Contextual.ProvenanceTeeth'`] only `ProvenanceExperiments`, which is not in the tree. `Lang/Journey.lean` does not mention `CoreCalculus` [MEASURED blame exit 128]. `ProvenanceTeeth` is the env-specialized tooth over `cmttData` (S10's deletion), not a deployed subject.

`P/Core` importing `Lang.Proofs.Index` points the toy at a deployed lemma. It does not point any deployed module back at the toy.

## (3) Premises

[MEASURED `fold/diff-S7.txt`] the TYPE block is two lines, both `._proof_1_2`. A gained hypothesis is a different elaborated type. No user theorem, def, or structure has one. The digest rewrites names and every constant inside the type before hashing [READ `fold/S7-digest_rn_cmd.lean:48–65`, `fix` on `ci.type`].

Source side, the patch's non-move edits are imports, two `namespace` lines, `open Contextual` dropped in `Deployed`, `LiveCost`, and `LiveHoles`, two section headers, and the `Lang/Subst.lean` comment. Dropping `open Contextual` cannot add a binder. The impact's failed build (`unknown namespace Contextual` at `LiveHoles.lean:8`) is what you get once `HoleBudget` no longer brings that namespace in; the names `LiveHoles` uses (`fillBounded_bounds`, `HasType`) are in `Nanodregg.Lang` after the move, which is the namespace `LiveHoles` is already in.

## Spot-checks

```
git -C /Users/ember/dev/nanodregg fetch origin
git -C /Users/ember/dev/nanodregg rev-parse origin/main
→ d3e850d7c104b7095a07a4a5ddcbe458d9b1f8ca
  d3e850d lang: the deployed term operations leave Contextual: … (S6)

git -C /Users/ember/dev/nanodregg blame -L '/import Lang.Proofs.Contextual.ClosedLeaf/,+1' origin/main -- Kernel/Proofs/InvokeWitness.lean
→ InvokeWitness.lean:38  import Lang.Proofs.Contextual.ClosedLeaf

git -C /Users/ember/dev/nanodregg blame -L '/import Lang.Proofs.Contextual.LawReceiver/,+1' origin/main -- Kernel/Proofs/Logic/History.lean
→ History.lean:51  import Lang.Proofs.Contextual.LawReceiver

git -C /Users/ember/dev/nanodregg show origin/main:Ledger/Proofs/EscrowRun.lean
→ :59 import Lang.Proofs.Contextual.ClosedLeaf
  :60 import Lang.Proofs.Contextual.LawReceiver

git -C /Users/ember/dev/nanodregg blame -L '/^import Lang.Proofs.Contextual.Core/,+1' origin/main -- Lang/Proofs/Contextual/LangRenaming.lean
→ LangRenaming.lean:4  import Lang.Proofs.Contextual.Core

git -C /Users/ember/dev/nanodregg show origin/main:Lang/Proofs/Contextual/Typing.lean
→ :8 import Lang.Contextual.Core

git -C /Users/ember/dev/nanodregg show origin/main:Lang/Proofs/Contextual/Core.lean
→ :24 import Lang.Proofs.Contextual.Typing
  :68 theorem upR_upR (ρ ρ' : Nat → Nat) :
  :69     (fun i => upR ρ (upR ρ' i)) = upR (fun i => ρ (ρ' i)) := by
  :72 theorem upR_id : upR (fun i => i) = (fun i => i) := by

git -C /Users/ember/dev/nanodregg blame -L '/^theorem usesVar_shiftAt/,+1' origin/main -- Lang/Proofs/Contextual/LangRenaming.lean
→ :263 theorem usesVar_shiftAt (x : Nat) (t : Term) : Term.usesVar x (Term.renameVar (liftIdx x) t) = false

git -C /Users/ember/dev/nanodregg log -S 'import Lang.Proofs.Contextual.CoreInstance' --pretty=format:'COMMIT %h' --name-only origin/main
→ (empty)
```

`fold/diff-S7.txt`, checked against the names rather than the prose:

```
before 51195 (rows carrying a renamed-from name: 384 ) after 51176
vanished 26 declared 0 UNDECLARED 26
new 7 type-digest changed 2 value-hash changed 5
module changed 581 of which from a module the step does not move 0
   Lang.Proofs.Contextual.Core             -> Lang.Proofs.Index           2
   Lang.Proofs.Contextual.Core             -> Lang.Proofs.Subst           4
   Lang.Proofs.Contextual.HoleBudget       -> Lang.Proofs.Fill           25
   Lang.Proofs.Contextual.HoleBudget       -> Lang.Proofs.HoleBudget    140
   Lang.Proofs.Contextual.LangFilling      -> Lang.Proofs.Fill           63
   Lang.Proofs.Contextual.LangOccurrences  -> Lang.Proofs.Fill          132
   Lang.Proofs.Contextual.LangRenaming     -> Lang.Proofs.Subst         181
   Lang.Proofs.Contextual.LangSubstitution -> Lang.Proofs.Subst          34
TYPE  hasType_unshiftAt_live._proof_1_2
TYPE  usesVar_shiftAt._proof_1_2
VALUE Term.shiftAt_unshiftAt
VALUE hasType_unshiftAt_live
VALUE hasType_unshiftAt_live._proof_1_2
VALUE usesVar_shiftAt
VALUE usesVar_shiftAt._proof_1_2
```
