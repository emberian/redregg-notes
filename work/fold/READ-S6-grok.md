VERDICT: RELEASE S6

No moved user statement gains a premise, changes its elaborated type, or disappears outside the five declared deletions. The 15 type-digest hits and the 37 undeclared vanishings are generated matcher/equation lemmas, named below, not theorems a consumer cites. `ΔOf` / `holeBound` are the legacy no-op, used only by their own three lemmas (not two). `Term.nodes` belongs in `HoleBudget`. The `HoleModel` merge does not change a statement and does not make a pile. `holeTy` is an honest name for the lookup. Codec sources are untouched, so this is `lang:`. The Host exe closure loses the CMTT definition module at S6; `P/Core` was never in that closure and stays on the proof path until S7.

`origin/main` after `git fetch origin` is `a27b2da7fbbae31ef097e5b002f9784b3cbba6e9`. Local `main` is `7e02852`, behind 32. Everything below is `git show` / `git blame -L` / `git log -S` / `git ls-tree` of `origin/main`, plus `fold/S6-candidate.patch`, `fold/diff-S6.txt`, `fold/S6-renames.tsv`, `fold/S6-diff_rn.py`, `fold/S6-digest_rn_cmd.lean`. No build. The builder's GREEN, the codec `--check`/`--write`, and the census elaboration are theirs; the source, the import chain, and the digest's name lists were checked here.

## (1) Move invariant

Under the 45-row rename map, every user declaration that survives has the same elaborated type. [MEASURED `fold/diff-S6.txt`: `type-digest changed 15`, and every one of the 15 is an `.eq_N` or `.eq_def` of `fillRefs` / `fillRefsList` / `fillRefsRow` / `usesRefList` / `usesRefRow` / `usesVarArms` / `usesVarList` / `usesVarRow` / `upR`. None of those names is a user theorem, def, structure, or instance. The renamed defs themselves (`upR`, `holeTy`, `Term.fillRefs`, …) are not in the TYPE list.]

No user statement's premises grew. The two renamed theorems keep their statements with `tyOf` rewritten to `holeTy` [READ `Lang/Proofs/Contextual/LangInstance.lean:16–38` against the patch's `holeTy_some` / `holeTy_filter`]. `langData`'s field list is copied verbatim [READ `LangCalculus.lean:590–603` and the patch's `LangInstance` block]. `HoleDecl`'s three fields are unchanged [READ `Lang/Contextual/HoleDecl.lean` whole, 10 lines; patch `Lang/HoleDecl.lean`].

What the literal "0 type changes" reading still sees, all generated, none a premise:

- TYPE (15): `Term.fillRefs.eq_16`, `Term.fillRefs.eq_17`, `Term.fillRefs.eq_def`, `Term.fillRefsList.eq_def`, `Term.fillRefsRow.eq_2`, `Term.fillRefsRow.eq_def`, `Term.usesRefList.eq_def`, `Term.usesRefRow.eq_2`, `Term.usesRefRow.eq_def`, `Term.usesVarArms.eq_2`, `Term.usesVarArms.eq_def`, `Term.usesVarList.eq_def`, `Term.usesVarRow.eq_2`, `Term.usesVarRow.eq_def`, `upR.eq_2`. [MEASURED `diff-S6.txt`]
- VANISHED but not on the delete list (37): `Term.fillRefs.match_3`, `Term.usesVarList.match_1`, `Term.usesVarRow.match_1`, and 34 private `.eq_*` / `.splitter` lemmas of those matchers in `P/HoleBudget`, `P/LangFilling`, `P/LangOccurrences`, `P/LangRenaming`. [MEASURED the UNDECLARED block; it is exactly the VANISHED block minus the 11 declared names.]
- NEW (26): `upR.match_1` plus private equation lemmas of `upR.match_1`, `Term.renameVar.match_1`, `Term.renameVarRow.match_1`. Same cause, the other direction. [MEASURED]

[INFERRED, not re-elaborated] Those equation lemmas mention the matcher they were compiled against. Moving `usesVar*` / `fillRefs` into the file that already holds `renameVar*` makes Lean share the matcher, so `usesVarList.eq_def`'s right-hand side names `renameVarList.match_1` instead of `usesVarList.match_1`, and `upR` in its own file grows `upR.match_1` (binder names taken from that matcher). That changes the printed type of the equation lemma. It does not change the type of `usesVarList` or `upR`. No consumer cites a `.match_` or an `.eq_def`. I did not see the before/after type strings — `diff-S6.txt` lists names only — so the binder/matcher account is the builder's, and it matches the names and Lean's sharing rule.

Value hashes, which are not the type invariant: `upR` itself and `HoleDecl.name` / `.ctx` / `.ty` are in the 36 VALUE lines. [MEASURED `diff-S6.txt`] IMPACT §3 says no user def is among those 36; that sentence is too strong. §4 then explains both (matcher in `upR`'s compiled body; `Expr.proj` keyed by the structure name, which the constant renamer does not rewrite). The source of `upR` is the same three lines [READ patch `Lang/Index.lean` against the `Core.lean` deletion]. Not a weaker statement.

Nothing else vanished. Declared user deletions are exactly `holeBound`, `ΔOf`, `lt_holeBound`, `ΔOf_getElem?`, `ΔOf_nil`, plus six generated constants of those (`holeBound.eq_1`, `ΔOf.eq_1`, `lt_holeBound._f`, `._proof_1_4`, `._proof_1_5`, `.match_1_1`) = 11. [MEASURED]

The diff header `renamed under the map: 51239` is the script counting a 6th TSV field on every before-row (`S6-diff_rn.py`), not the 956 inverse-map rewrites the impact cites from the digest log. The exceptional names are a coherent set, not a shifted-column scramble. [INFERRED]

## (2) The deletions

Three lemmas, not two: `lt_holeBound`, `ΔOf_getElem?`, `ΔOf_nil`, plus the two defs.

[READ `Lang/Contextual/LangCalculus.lean:575–587`]

```
def tyOf (Ω : List (HoleDecl (List Lang.Ty) Lang.Ty)) (n : Nat) : Option Lang.Ty :=
  (Ω.find? (·.name == n)).map (·.ty)
def holeBound (Ω) : Nat := Ω.foldr (fun d m => max (d.name + 1) m) 0
/-- Legacy name-indexed type projection retained for its lookup API.
Live LangHasTy uses HoleSignature directly; … Undeclared positions use a placeholder
only in this projection and do not authorize a hole in the deployed checker. -/
def ΔOf (Ω) : List Lang.Ty :=
  (List.range (holeBound Ω)).map fun n => (tyOf Ω n).getD .nat
```

`holeBound` is used only to build that list. `ΔOf` writes `.nat` into every undeclared slot. The live checker does not read it: `inferE` on `.hole` looks up `Ω.find?` [READ `Lang/Check.lean`, the `.hole` arm], and `LangHasTy` is `HasType` at a `HoleSignature` [READ `LangInstance.lean`, `def LangHasTy`].

[READ `Lang/Proofs/Contextual/LangInstance.lean:40–54`] `lt_holeBound` speaks only of `holeBound`. `ΔOf_getElem?` is `tyOf Ω n = some A → (ΔOf Ω)[n]? = some A`. `ΔOf_nil` is `ΔOf [] = [] := rfl`. The patch deletes those three and no other theorem in that file.

[MEASURED `git log -S 'ΔOf' --name-only origin/main`] the string occurs only in `Lang/Contextual/LangCalculus.lean`, `Lang/Proofs/Contextual/LangInstance.lean`, and `decisions/lang.md` (commits `2b6e5e1`, `d7989d9`, `f665e94`). [MEASURED `git log -S 'holeBound'`] the same two Lean files plus `decisions/lang.md`. No deployed module, no other proof, no gates row. The full `LangCalculus` body does not mention either name above the tail [READ the 604-line file].

## (3) The three defaults

**(a) `Term.nodes` stays in `HoleBudget`.** Right home. [READ `Lang/HoleBudget.lean:8`, `:30`, `:60`, `:83`] `Term.nodes` / `rowNodes` / `listNodes` are one mutual block. `substNodes*` (`:30`) and `fillNodes*` (`:60`) are two later mutual blocks, not the same one — the impact's "one mutual block with the other node counts" overstates it. `fillBounded` (`:83`) calls both `Term.nodes` and `Term.fillRefs`. Moving only `nodes` splits the counter from the bound; moving the whole file's contents makes `Subst` the budget module. The map's actual consumer wish, `Program` calling `Term.nodes` without `Contextual.`, is already achieved by the namespace change to `Nanodregg.Lang` [READ the patch hunks at `Program.lean`]. Default stands.

**(b) `HoleModel` merges into `C/LangInstance`.** No statement changes. [READ `Lang/Contextual/HoleModel.lean` whole] `holeModelCandidate`, `holeLive`, `holeBlocked`, `holeModelIface`, `holeModelTemplate` are the same defs; each is typed at `langData` (`Candidate langData`, `Iface langData`, `Template langData`). The patch prepends `langData` (verbatim from `LangCalculus.lean:590–603`) and a header, and drops a trailing blank. [MEASURED `diff-S6.txt`] 8 constants change module `HoleModel → LangInstance` and 1 (`langData`) changes `LangCalculus → LangInstance`; none of those names is in the TYPE or VALUE lists. The file is the data instance plus the one fragment the `Std.hole` bridge is stated over — map §2.1 names this merge, and no later step owns it. Not a pile.

**(c) `tyOf` → `holeTy`.** Honest. [READ `LangCalculus.lean:574–576`] it is `(Ω.find? (·.name == n)).map (·.ty)`, the first declaration's type, which is what the docstring says. It is not a term's type and not a wire decode. [READ `Lang/Wire.lean:109`] `Nanodregg.Lang.Wire.tyOf : Tree → Option Ty` decodes a type node. Today the hole function is `Nanodregg.Lang.Contextual.tyOf`, so they do not meet. The namespace move would put a second `tyOf` in `Nanodregg.Lang`. [READ `Lang/Proofs/WireTeeth.lean:13–15`, `:80`] `namespace Nanodregg.Lang.Teeth` / `open Nanodregg.Lang.Wire` / `tyOf (.node 0 ⟨#[0]⟩ [])`. A parent `Lang.tyOf` would take that call and fail, because the types differ. `holeTy` removes the clash instead of leaving two `tyOf`s. The lemmas stay `holeTy_some` / `holeTy_filter` in namespace `Contextual`, which is where `P/LangInstance` lives (rename-map rows 44–45).

## (4) Wire, `lang:` not `lang!`

Sufficient. The patch's 20 `diff --git` entries (22 paths counting the two renames) are the move, the import edits, and the three lemma deletions. Not among them: `Lang/Term.lean`, `Lang/Package.lean`, `Lang/Wire.lean`, `Lang/Wire/`, `Lang/HoleWire.lean`, `gates/codec-vectors.tsv`. [MEASURED by reading `fold/S6-candidate.patch` whole, 761 lines.]

[READ `Lang/Wire.lean:27–29`, `:109`] the term/type codec imports `Codec.Tree`, `Lang.Term`, `Lang.Bounds` only. [READ `Lang/HoleWire.lean` whole] the ROM section encodes with `termTree` / `termOf` / `tyOf` / `tyTree` in `namespace Nanodregg.Lang.Wire` — that `tyOf` is the wire one, in the same namespace, and the file is not edited. `HoleDecl` derives nothing and is not a codec. The moved functions are rename, subst, fill, occurrence, `decEq`, `holeTy`. Their bodies are the old bodies [READ the patch against `LangSubstitution.lean` and the `LangCalculus` tail]. An untouched encoder that calls an unchanged body cannot change a byte.

The builder's `codec-vectors --check` / `--write` byte-identical `cmp` was not re-run here (no builds). It is the right gate, and this diff cannot make it fail for a wire-byte reason. `lang:`.

## (5) Host closure 91 → 89

[MEASURED `git show origin/main:SIZE.md`] `| Lean modules in the Host closure | 91 | 150 |`, Lang lines `42192`, deployed lines `29554`, theorems `6081`. The preview's before-column matches. After: 89, `42177`, `29555`, `6078` (−3 theorems = the three lemmas). [READ `fold/S6-size-preview.txt`]

The chain at `a27b2da`, each edge read or pickaxed:

- `Host/Main.lean` imports `Host.Cli` [READ the file, two lines]
- `Host/Cli.lean:55` imports `Host.Deployed` [MEASURED `git blame -L`]
- `Host/Deployed.lean:15` imports `Lang.Program` [READ]
- `Lang/Program.lean:26` imports `Lang.LiveHoles` [MEASURED `git blame -L`]
- `Lang/LiveHoles.lean:3` imports `Lang.HoleBudget` [READ]
- `Lang/HoleBudget.lean:3` imports `Lang.Contextual.LangCalculus` [READ]
- `Lang/Contextual/LangCalculus.lean:15–17` imports `LangSubstitution`, `Core`, `Closure` [READ]
- `Lang/Check.lean:18` imports `Lang.Contextual.HoleDecl`; `HoleROM.lean:3` also imports `LangCalculus` [READ]

After the patch those edges become `HoleBudget` / `HoleROM` → `Lang.Subst` → `Lang.Check` + `Lang.Index`, and `Check` → `Lang.HoleDecl`. [READ the patch]

What leaves the closure: `Lang.Contextual.Core`, `Lang.Contextual.Closure`, `Lang.Contextual.LangCalculus`, `Lang.Contextual.LangSubstitution`. What enters: `Lang.Index`, `Lang.Subst`. `HoleDecl` changes directory and stays. Net −4 + 2 = −2. The impact's opening sentence names Core, Closure, and LangCalculus leaving and Index and Subst entering, and forgets `LangSubstitution` in that sentence; the SIZE table in §7 has it. The arithmetic that matches 91 → 89 is the table's.

`Core` and `Closure` are not reached again by a host def-module. [MEASURED `git log -S 'import Lang.Contextual.Core'`] surviving def-module importers are `LangCalculus`, `LangSubstitution` (both deleted here) and `CoreCalculus` (`:9–10`). `CoreCalculus`'s importers that still exist are proofs (`P/CoreInstance`, `P/ProvenanceTeeth`). [MEASURED `git log -S 'import Lang.Contextual.CoreCalculus'`] [MEASURED `git log -S 'import Lang.Contextual.Closure'`] surviving def-module importers besides `LangCalculus` are `Trace.lean:2`, `Provenance.lean`, `CoreCalculus`. `Trace` is imported by `StdHoleModel.lean:4` and the journey; `StdHoleModel` is imported only by `Lang/Proofs/StdHole.lean` [MEASURED `git log -S 'import Lang.StdHoleModel'`]. Journey and Census are tooling; C9/C4 keep them out of the Host exe closure. `HoleModel` is imported only by `P/HoleBridge` [MEASURED `git log -S 'import Lang.Contextual.HoleModel'`]. The new `LangInstance` (which imports `Closure`) is imported by the patch only from `P/HoleBridge` and `P/LangInstance`.

So the toy CMTT **definition** module is out of the Host exe closure at S6, not at S7.

`P/Core` is not in that closure before or after: a def-module cannot import a proof-module (closure C4). It remains on the proof path. [MEASURED `git blame`] `Lang/Proofs/Contextual/LangRenaming.lean:4` still imports `Lang.Proofs.Contextual.Core` (the patch keeps that line and only swaps `LangCalculus` for `Lang.Subst`). `P/Core.lean:24` imports `P/Typing`. `P/Typing.lean:8` imports `Lang.Contextual.Core`. Kernel/Ledger proof closures that reach `LangRenaming` still reach the CMTT core. That cut is S7, as the map orders. [INFERRED from those three edges plus map §4.2 row S7; the full Kernel walk was not re-derived.]

`gates/size.py`'s "deployed lines" still means "not a proof and not tooling" (`size.py` `measure`, the row that goes 29554 → 29555). Contextual theory still counts. The map wanted S6 to redefine it as "in an exe closure". The builder left it, because `gates/` is not in this step's grant. Agreed: not a condition of this landing. The closure row, which is the claim, is the one that moves 91 → 89.

## Spot-checks

```
git -C /Users/ember/dev/nanodregg fetch origin
git -C /Users/ember/dev/nanodregg rev-parse origin/main
→ a27b2da7fbbae31ef097e5b002f9784b3cbba6e9
  a27b2da lang: delete the worlds, the acyclic adapter and stability, … (S5)

git -C /Users/ember/dev/nanodregg log -S 'ΔOf' --name-only --pretty=format:'COMMIT %h' origin/main
→ f665e94  decisions/lang.md
  d7989d9  Lang/Contextual/LangCalculus.lean
           Lang/Proofs/Contextual/LangInstance.lean
  2b6e5e1  Lang/Contextual/LangCalculus.lean
           Lang/Proofs/Contextual/LangInstance.lean
           decisions/lang.md

git -C /Users/ember/dev/nanodregg log -S 'holeBound' --name-only --pretty=format:'COMMIT %h' origin/main
→ f665e94  decisions/lang.md
  2b6e5e1  Lang/Contextual/LangCalculus.lean
           Lang/Proofs/Contextual/LangInstance.lean

git -C /Users/ember/dev/nanodregg blame -L '/theorem ty_payload_refused/,+1' origin/main -- Lang/Proofs/WireTeeth.lean
→ WireTeeth.lean:80  theorem ty_payload_refused : tyOf (.node 0 ⟨#[0]⟩ []) = none

git -C /Users/ember/dev/nanodregg blame -L '/def tyOf/,+2' origin/main -- Lang/Wire.lean
→ Lang/Wire.lean:109  def tyOf : Tree → Option Ty

git -C /Users/ember/dev/nanodregg show origin/main:SIZE.md
→ | Lean modules in the Host closure | 91 | 150 |
  | Lean lines (Lang) | 42192 |
  | Lean lines (deployed) | 29554 |
  | theorems | 6081 |

git -C /Users/ember/dev/nanodregg ls-tree -l origin/main -- Lang/Contextual/LangCalculus.lean
→ 229683288bf21b87836e09bf07da7e141b7a58ea   (patch index 2296832)
```

`fold/diff-S6.txt` head, checked against the listed names rather than the prose:

```
before 51239 (renamed under the map: 51239 ) after 51217
vanished 48 declared 11 UNDECLARED 37
new 26 type-digest changed 15 value-hash changed 36
module changed 510 of which from a module the step does not move 0
   Lang.Contextual.Core             -> Lang.Index                     3
   Lang.Contextual.HoleDecl         -> Lang.HoleDecl                 18
   Lang.Contextual.HoleModel        -> Lang.Contextual.LangInstance   8
   Lang.Contextual.LangCalculus     -> Lang.Contextual.LangInstance   1
   Lang.Contextual.LangCalculus     -> Lang.Subst                   437
   Lang.Contextual.LangSubstitution -> Lang.Subst                    43
```
