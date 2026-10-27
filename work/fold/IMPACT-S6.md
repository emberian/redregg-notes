# IMPACT-S6 — the deployed term operations leave `Contextual`: `Lang/Index`, `Lang/Subst`, `Lang/HoleDecl` (consolidation step S6)

Worker: CX-FOLD-2 (Claude; successor of CX-FOLD). Written 2026-10-22. Base: nanodregg `origin/main` = **a27b2da** (S5).
Candidate: uncommitted in `hbox:/tank/dregg-build/nanodregg/wt/cxfold`, the whole diff is `fold/S6-candidate.patch`
(22 paths). Nothing landed. Map: §1.5 F1/F2/F6, §2.1 "Deployed language", §2.2 D-NOOP, §3.2, §3.4, §4.2 row S6.
Tags READ / MEASURED / INFERRED. **The rename map is `fold/S6-renames.tsv`** (45 rows, old → new, component-wise
prefix: generated constants move with their owner).

## 0. Answer first

- **The Host closure goes from 91 to 89 modules** [MEASURED `gates/size.py`, `fold/S6-size-preview.txt`]. It no longer
  contains `Lang.Contextual.Core` (the CMTT core), `Lang.Contextual.Closure` (the abstract closure) or
  `Lang.Contextual.LangCalculus`; it gains `Lang.Index` and `Lang.Subst`; `HoleDecl` changes directory. No deployed
  module imports anything under `Lang/Contextual/` any more [MEASURED: `grep ^import` of the closure's modules].
- **No landed theorem gains a hypothesis, and no user statement changes** [MEASURED `fold/diff-S6.txt`]. The census
  digest diff compares a27b2da with the candidate under the rename map. Every user declaration (every theorem, def,
  structure and instance written in a source file) has an identical elaborated statement and an identical value
  hash. The only deleted user declarations are the five declared ones (§2). What remains in the diff is generated
  constants only (§4): the matchers Lean shares, the equation lemmas of those matchers, and three projection values.
- **No wire byte changes.** `lake exe codec-vectors --check gates/codec-vectors.tsv` is ok (263 vectors at 56 sites,
  54 of them at `lang/package/4`). `--write` regenerates a table that is byte-identical to the landed one (`cmp`)
  [MEASURED]. `Lang/Term.lean`, `Lang/Package.lean` and `Lang/Wire*.lean` are not in the diff. So this is not a
  `lang!`.
- The whole-tree build with `host`, `lang-journey` and `codec-vectors` is GREEN (631 jobs). `lang-journey` is GREEN
  (787 lines). `gates/check.py` is GREEN with the generated SIZE [MEASURED].

**Three choices for the reader, each with a default** (§5):
- (a) `Term.nodes` stays in `Lang/HoleBudget.lean` (the map said `Lang/Subst`);
- (b) `C/HoleModel` merges into the new `C/LangInstance` now (the map's §2.1 target, which no step row named);
- (c) the hole projection `tyOf` is renamed `holeTy`, because the move collides with `Lang.Wire.tyOf`, and its two
  lemmas are renamed `holeTy_some`/`holeTy_filter`.

## 1. What moves [READ the sources at a27b2da; MEASURED the text check]

| from (a27b2da) | to | content | namespace |
|---|---|---|---|
| `Lang/Contextual/Core.lean` :70–74, :354–360 | **`Lang/Index.lean`** (new, 17 lines, no imports) | `upR`, `liftIdx`, `lowerIdx` | `Contextual` → `Nanodregg.Lang` |
| `Lang/Contextual/LangSubstitution.lean` (95, deleted) | **`Lang/Subst.lean`** (new) | `Term.renameVar*`, `Term.upVarSubst`, `Term.substVar*`, `Term.substListFn`, `Term.substList` | `Contextual` → `Nanodregg.Lang` |
| `Lang/Contextual/LangCalculus.lean` :21–576 (deleted file) | **`Lang/Subst.lean`** | `Term.decEq/decEqList/decEqRow`, `Term.instDecEq`, `Term.usesVar*`, `Term.usesRef*`, `Term.fillRefs*`, `tyOf` → **`holeTy`** | `Contextual` → `Nanodregg.Lang` |
| `Lang/Contextual/HoleDecl.lean` (10, deleted) | **`Lang/HoleDecl.lean`** | `structure HoleDecl` | `Contextual` → `Nanodregg.Lang` |
| `Lang/Contextual/LangCalculus.lean` :589–602 | **`Lang/Contextual/LangInstance.lean`** (new) | `langData : CalculusData` | unchanged (`Contextual`) |
| `Lang/Contextual/HoleModel.lean` (47, deleted) | **`Lang/Contextual/LangInstance.lean`** | `holeModelCandidate`, `holeLive`, `holeBlocked`, `holeModelIface`, `holeModelTemplate` | unchanged |
| `Lang/HoleBudget.lean` (file stays) | — | `Term.nodes/rowNodes/listNodes`, `upNodeSubst`, `Term.substNodes*`, `nodeListFn`, `Term.fillNodes*`, `Term.fillBounded` | `Contextual` → `Nanodregg.Lang` (map F6) |

Text check [MEASURED, the predecessor's lesson]. The bodies of `Lang/Subst.lean` and `Lang/Contextual/LangInstance.lean`
are `diff`-identical to the concatenated old bodies, blank lines aside and `tyOf` → `holeTy` applied. The only other
edits to the moved files are the namespace lines, the imports, and new header docstrings for the new files.
`Core.lean` loses exactly the three definitions and gains `import Lang.Index` (`git diff`, in the patch).

### 1.1 Consumers edited (map §3.4; every edit is a name-resolution or import edit) [MEASURED `git diff --stat`]

| file | edit |
|---|---|
| `Lang/Check.lean` | `import Lang.HoleDecl`; `Contextual.HoleDecl` → `HoleDecl` in `HoleSignature` |
| `Lang/HoleROM.lean` | `import Lang.Subst`; `Contextual.HoleDecl` → `HoleDecl` in `HoleROM.decl` |
| `Lang/LiveHoles.lean` | drop `open Contextual` (nothing else from it is used) |
| `Lang/Program.lean` :168, :214, :216 | `Contextual.Term.fillBounded` / `Contextual.Term.nodes` → `Term.…` |
| `Lang/Journey/ContextualChecks.lean` :46–56, :85–86 | `Contextual.Term.` → `Term.` (10 call sites) |
| `Lang/Contextual/Closure.lean` | `import Lang.HoleDecl` |
| `Lang/Proofs/Contextual/LawMeaning.lean`, `LawReceiverTeeth.lean` | `Contextual.Term.` → `Term.` (statement text; elaborated statements identical, §3) |
| `Lang/Proofs/Contextual/LangRenaming.lean`, `LangSubstitution.lean` | `import Lang.Subst` |
| `Lang/Proofs/Contextual/HoleBridge.lean` | `import Lang.Contextual.LangInstance` (was `HoleModel`) |
| `Lang/Proofs/Contextual/LangInstance.lean` | `import Lang.Contextual.LangInstance`; the three D-NOOP lemmas deleted; `tyOf` → `holeTy` |

All the other proof modules compile unedited. Inside `namespace Nanodregg.Lang.Contextual`, `Term.renameVar` now
resolves to `Nanodregg.Lang.Term.renameVar` through the parent namespace. Kernel, Ledger, Host, Hosting, Protocol,
Census, Codec, Emit, Bench, Ops: **no edit** [MEASURED].

## 2. What is deleted (D-NOOP, map §2.2 F2) — the explicit deletion authorization of this landing

| name | where (a27b2da) | statement | why |
|---|---|---|---|
| `holeBound` (def) | `C/LangCalculus.lean`:579 | `List (HoleDecl (List Ty) Ty) → Nat` | its only users were `ΔOf` and `lt_holeBound` |
| `ΔOf` (def) | `C/LangCalculus.lean`:586 | `List (HoleDecl …) → List Ty`, "Legacy name-indexed type projection retained for its lookup API" | no caller outside its own two lemmas [MEASURED `git grep -w ΔOf`]; CLAUDE.md: never keep a no-op |
| `lt_holeBound` | `P/LangInstance.lean`:40 | `∀ {Ω} {d}, d ∈ Ω → d.name < holeBound Ω` | about the no-op only |
| `ΔOf_getElem?` | `P/LangInstance.lean`:48 | `tyOf Ω n = some A → (ΔOf Ω)[n]? = some A` | about the no-op only |
| `ΔOf_nil` | `P/LangInstance.lean`:54 | `ΔOf [] = []` | about the no-op only |

Census: these 5 user declarations plus their 6 generated constants (`holeBound.eq_1`, `ΔOf.eq_1`, `lt_holeBound._f`,
`._proof_1_4`, `._proof_1_5`, `.match_1_1`) = **11 declared vanished**, all present in `diff-S6.txt` [MEASURED].
`grep -w` of `ΔOf|holeBound` across Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench Ops gates rows
lakefile, after the edit: 0 hits outside `decisions/` [MEASURED].

## 3. The census digest diff under the rename map [MEASURED `fold/diff-S6.txt`, script `fold/S6-diff_rn.py`]

Method. The digest tool (`fold/S6-digest_rn_cmd.lean`, which extends the predecessor's `FoldDigest`) imports every
non-exe module of the 11 libraries. It writes one row per constant: name, module, kind, elaborated type, value hash.
Under a rename map it rewrites every constant name in the row, the type and the value. Private names
`_private.<M>.0.<user name>` are rewritten in their user-name part.
- **before** = a27b2da (`logs/cxfold/S5-after.tsv`, the digest the predecessor took of exactly this tree, 51,239
  constants).
- **after** = the candidate digested under the INVERSE map (`S6-renames-inverse.tsv`), which writes every new name
  back to its old one, so the comparison is by old name.

Types are compared as printed elaborated expressions, with hygienic binder names (`x._@.<Module>.<n>._hyg.<k>`,
which embed the module and a counter) erased. Binder names are not part of a statement. User-chosen binder names are
compared as written.

```
before 51239 after 51217
vanished 48   declared 11 (§2)   other 37 (generated matchers, §4)
new 26        (generated matchers, §4)
type-digest changed 15   (all generated equation lemmas, §4)
value-hash changed 36    (all generated constants or projections, §4)
module changed 510       from a module the step does not move: 0
   Lang.Contextual.Core            -> Lang.Index                     3
   Lang.Contextual.HoleDecl        -> Lang.HoleDecl                 18
   Lang.Contextual.HoleModel       -> Lang.Contextual.LangInstance   8
   Lang.Contextual.LangCalculus    -> Lang.Contextual.LangInstance   1
   Lang.Contextual.LangCalculus    -> Lang.Subst                   437
   Lang.Contextual.LangSubstitution-> Lang.Subst                    43
```

(`Lang.HoleBudget`'s constants keep their module and change only their name, so they do not appear as module
changes. 956 after-constants were renamed back by the inverse map [MEASURED digest log].)

**Every user declaration's statement and proof are identical under the rename**: no user theorem, def, structure
or instance is among the 15 type changes or the 36 value changes [MEASURED: the full lists in `diff-S6.txt`, no
truncation]. The two renamed theorems, by statement (with `tyOf` → `holeTy`, digest-identical under the map):
- `holeTy_some : holeTy Ω n = some A → ∃ d ∈ Ω, d.name = n ∧ d.ty = A`
- `holeTy_filter : (∀ d ∈ Ω, d.name = n → p d = true) → holeTy (Ω.filter p) n = holeTy Ω n`

## 4. The residual: generated constants only, by cause [MEASURED `diff-S6.txt`; mechanism INFERRED]

1. **Lean shares structurally identical matchers within a module.**
   - With `usesVar*`, `fillRefs` and `renameVar*` now in one file, `Term.usesVarList`/`usesVarRow` reuse
     `Term.renameVarList.match_1`/`renameVarRow.match_1`, and `Term.fillRefs` reuses `Term.renameVar.match_1`.
     So `usesVarList.match_1`, `usesVarRow.match_1` and `fillRefs.match_3` vanish, together with their 34 lazily
     realized private equation/splitter lemmas in `P/HoleBudget`, `P/LangFilling`, `P/LangOccurrences` and
     `P/LangRenaming` (37).
   - Conversely, `upR` in its own file gets `upR.match_1` (+3 private lemmas in `P/Core`). The renamed reuses add
     22 private lemmas in `P/LangFilling`/`P/LangOccurrences`. Total 26 new.
   - Example: `Term.usesVarList.eq_def`'s right side was `… usesVarList.match_1 …` and is `… renameVarList.match_1 …`.
2. **Equation lemmas of the moved functions name those matchers** and take their binder names from the shared
   matcher (`upR.eq_2`: `∀ ρ v` → `∀ ρ i`). That gives 15 type changes, every one an `.eq_N`/`.eq_def` of `fillRefs*`,
   `usesRef*`, `usesVar*` or `upR`.
3. **The same shared matchers change the compiled bodies** (`._f`, `._sunfold`, `._unsafe_rec`, `.eq_def`) of the
   same seven functions and `upR`: 33 value changes.
4. **The three `HoleDecl` projections** (`.name`, `.ctx`, `.ty`): their values are `Expr.proj` nodes keyed by the
   structure name, which the renamer (constants only) does not rewrite. Their types are equal. That is 3 value
   changes, a limit of the tool, not of the move.

No user statement mentions a matcher [MEASURED: none of the 15 is a user declaration], so none of this reaches a
statement a consumer cites.

## 5. Choices, with defaults [INFERRED unless tagged]

- **(a) `Term.nodes` stays in `Lang/HoleBudget.lean`** (map §2.1 said `Lang/Subst`).
  - `Term.nodes/rowNodes/listNodes` are one mutual block with the other node counts (`substNodes`, `fillNodes`, the
    bound `fillBounded`). Moving one block member splits a concept, and moving all of them makes `Subst` the budget
    module too.
  - What the map wanted, `Program.lean`:214–216 calling `Term.nodes` without `Contextual.`, is achieved by
    HoleBudget's namespace move.
  - S9's "one preparation charge" will decide where the charge lives.
  - **Default: as built.**
- **(b) `C/HoleModel` merged into `C/LangInstance` in S6.** S6 creates `C/LangInstance` (map §2.1: "absorbs `langData`
  + `C/HoleModel`"), and no later step row owns the merge. The merge is a pure move: 8 constants change module and
  nothing else (§3). **Default: as built.**
- **(c) `tyOf` → `holeTy` (+ its two lemmas).**
  - At `Nanodregg.Lang` the hole projection collided with `Nanodregg.Lang.Wire.tyOf` (decode a type tree).
  - `Lang/Proofs/WireTeeth.lean`:80 (`open … Nanodregg.Lang.Wire`, in namespace `Nanodregg.Lang.Teeth`) silently
    resolved `tyOf (.node …)` to the hole projection and failed to elaborate [MEASURED first build, `logs/cxfold/
    S6-build.log`]. Two `tyOf`s one `open` apart is the hazard. The build only caught it because the types differ.
  - `holeTy Ω n` names its subject. Users: `Lang/Subst.lean` and `P/LangInstance` only.
  - **Default: as built** (rename map rows 5, 44, 45). The alternative, qualifying `Wire.tyOf` at the tooth, keeps
    two `tyOf`s.
- **Not in S6, outside the grant:** map §5.8 asks S6 to make `gates/size.py`'s "Lean lines (deployed)" mean "in an exe
  closure". Today it means "not a proof module and not tooling" (`size.py`:126), so `Lang/Contextual/*` still counts
  as deployed (+1 line this step: the new header docstrings outweigh the 12 deleted lines). `gates/` is not under
  R-0002. **Default: not in S6; a cv task for the GATES owner** (opened at landing). RULE if it belongs here.

## 6. `grep` and tables [MEASURED on the candidate]

- `git grep` for every old qualified spelling: `Contextual[./](LangCalculus|LangSubstitution|HoleModel|HoleDecl)`,
  `Contextual.(upR|liftIdx|lowerIdx|tyOf|holeBound|ΔOf|HoleDecl|upNodeSubst|nodeListFn)`, and
  `Contextual.Term.(renameVar|substVar|…|fillBounded)`, over the whole tree except `decisions/`. Result: 0 hits. The one
  apparent hit is `import Lang.Proofs.Contextual.LangSubstitution`, the proof module, which S7 moves.
- No lakefile target or root, `gates/*.tsv` row, `rows/run` line or golden names a moved or deleted module. The
  codec vector table is unchanged (§0). No generated file changes.
- Kernel/Ledger proof closures: they still reach `P/Core`/`P/Typing` through `P/LangRenaming`. That is S7's cut, as the
  map orders.

## 7. SIZE [MEASURED `fold/S6-size-preview.txt`]

| row | before | after | why |
|---|---:|---:|---|
| Lean modules in the Host closure | 91 | 89 | −Core, −Closure, −LangCalculus, LangSubstitution→Subst, HoleDecl moved, +Index |
| Lean modules | 499 | 499 | −4 files (HoleDecl, HoleModel, LangCalculus, LangSubstitution), +4 (Index, Subst, HoleDecl, C/LangInstance) |
| Lean lines (Lang) | 42,192 | 42,177 | −15: ΔOf/holeBound and their three lemmas, net of the new headers |
| Lean lines (deployed) | 29,554 | 29,555 | +1 under size.py's current meaning (§5) |
| theorems | 6,081 | 6,078 | the three D-NOOP lemmas |

## 8. Inverted question: is anything that survives weaker?

No.
- No statement changes (§3), and no check is relaxed: every refusal string, bound and checker is untouched (the
  diff is imports, namespaces and moves).
- The deleted lemmas spoke only of the deleted no-op.
- `langData` and the `Std.hole` fragment are unchanged in meaning and module-local, and `langLaws` and `HoleBridge`
  build against them unedited (only an import line).
- The journey's contextual checks (`ContextualChecks.lean`) run the same functions under their new names, and the
  journey stays GREEN.

## 9. Planned landing

The paths of `fold/S6-candidate.patch`; `### LANG-74.6` in `decisions/lang.md`; SIZE regenerated. Subject:
`lang: the deployed term operations leave Contextual — Lang/Index, Lang/Subst, Lang/HoleDecl (S6 of the
consolidation)`. Fast path (no wire byte, no statement change). Before landing:
- the digest diff re-run if main moved;
- `gates/check.py`;
- deleted paths asserted absent with `git ls-tree`.
