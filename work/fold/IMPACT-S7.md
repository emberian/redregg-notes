# IMPACT-S7 — the deployed-subject substitution and filling proofs leave `Contextual`: `Lang/Proofs/{Index,Subst,Fill,HoleBudget}` (consolidation step S7)

Worker: CX-FOLD-2 (Claude). Written 2026-10-22. Base: nanodregg `origin/main` = **d3e850d** (S6). Candidate:
uncommitted in `hbox:/tank/dregg-build/nanodregg/wt/cxfold`; the whole diff is `fold/S7-candidate.patch`
(15 paths). Map: §2.1 "Deployed-subject proofs", §3.2, §4.2 row S7. Tags READ / MEASURED / INFERRED.

- **Rename map:** `fold/S7-renames.tsv`. It has 101 user names, `Nanodregg.Lang.Contextual.X` → `Nanodregg.Lang.X`,
  and 5 private-prefix rows `_private:<old module>` → `_private:<new module>`. The digest tool now also rewrites the
  module part of a private name (`fold/S7-digest_rn_cmd.lean`).

## 0. Answer first

- **The Kernel/Ledger proof closures no longer contain the CMTT core** [MEASURED import closure from source,
  `logs/cxfold/closure.py`]:

  | consumer | closure at d3e850d | candidate | CMTT modules left |
  |---|---:|---:|---|
  | `Kernel/Proofs/InvokeWitness` | 97 | 94 | none (was `C/Core`, `P/Core`, `P/Typing`) |
  | `Kernel/Proofs/Logic/History` | 123 | 120 | none |
  | `Ledger/Proofs/EscrowRun` | 141 | 138 | none |

  What still reaches them from `Lang/Proofs/Contextual/` is exactly S8's set: `ClosedDeployment`, `ClosedLeaf`,
  `LawMeaning`, `LawReceiver`, `LiveHoles`, `LiveInvoke`.
- **No landed theorem gains a hypothesis; no user statement changes** [MEASURED `fold/diff-S7.txt`, full lists]:
  - before (d3e850d under the rename map) 51,195 constants; after 51,176;
  - 0 declared deletions (S7 deletes no declaration);
  - 581 module changes, all out of the six modules the step edits;
  - type-digest changes 2, value-hash changes 5, vanished 26, new 7: all generated or explained in §3.
- The moved text is `diff`-identical to the old bodies, blank lines and two section headers aside (Subst, Fill,
  HoleBudget checked) [MEASURED].
- Whole tree with `host` and `lang-journey`: GREEN (627 jobs). The journey: GREEN (787 lines). `gates/check.py`:
  GREEN with the generated SIZE [MEASURED]. No deployed module, wire byte or codec table is touched. Every edited file
  is a proof module, plus one comment in `Lang/Subst.lean`'s header.

## 1. What moves

| from (d3e850d) | to | content |
|---|---|---|
| `P/Core.lean` (the two at :68–73) | **`Lang/Proofs/Index.lean`** (new) | `upR_upR`, `upR_id`, the only `P/Core` facts the deployed proofs used [MEASURED: `grep -owFf` of P/Core's declaration names over the five modules finds `upR_upR`, `upR_id`, plus `shiftAt_unshiftAt`/`infer_complete`, which are LangRenaming's own `Term.shiftAt_unshiftAt` and `Lang.infer_complete`] |
| `P/LangRenaming.lean` (418) + `P/LangSubstitution.lean` (142) | **`Lang/Proofs/Subst.lean`** | `hasType_renameVar(_live)`, `hasType_unshiftAt(_live)`, `Term.shiftAt_unshiftAt`, `upR_lookup`, `substList_typed`, the capture teeth, … |
| `P/LangFilling.lean` (212) + `P/LangOccurrences.lean` (312) | **`Lang/Proofs/Fill.lean`** | `hasType_signature`, `fillHoles_typed` (+Fields/Arms), the `hasType_declaresHole` family, `usesRef` through renaming/substitution/fill |
| `P/HoleBudget.lean` (168) | **`Lang/Proofs/HoleBudget.lean`** | `renameVar_nodes`, `fillRefs_nodes`, `substList_nodes`, `fillBounded_bounds`, … |

All of these go from `Nanodregg.Lang.Contextual` to `Nanodregg.Lang`. The map's §3.2 already lists these
namespace moves. Collision check before moving: none of the 99 user names exists at `Nanodregg.Lang.*` in the d3e850d
environment [MEASURED against the S6 digest]. `P/Core` keeps everything else, imports `Lang.Proofs.Index`, and its
header names where the two went.

**Consumers edited** (imports and `open` lines only):
- `P/LangInstance`: `import Lang.Proofs.Fill`.
- `P/LiveHoles`: `import Lang.Proofs.HoleBudget`.
- `P/LiveHoles`, `P/LiveCost` and `P/Deployed` each drop `open Contextual`. That namespace is no longer declared in
  their import closure, and Lean refuses `open` of an unknown namespace [MEASURED first build:
  `P/LiveHoles.lean:8:5: unknown namespace Contextual`]. Nothing they use was from it.
- No Kernel/Ledger file changes; their import lines move in S8.

## 2. Deleted

No declaration is deleted. Five files are deleted as files, their content moved (§1): `Lang/Proofs/Contextual/
{LangRenaming,LangSubstitution,LangFilling,LangOccurrences,HoleBudget}.lean`. This list is the landing's deletion
authorization for the paths.

## 3. The digest residual, by cause [MEASURED `diff-S7.txt`]

1. **Auxiliary-proof numbering.** `Term.shiftAt_unshiftAt`, `hasType_unshiftAt_live` and `usesVar_shiftAt` each have
   two abstracted sub-proofs `._proof_1_k`. Their numbering shifted, so `._proof_1_1`/`_1_2` became `_1_2..1_4`. The
   effects:
   - 4 vanished and 4 new constants;
   - 2 type changes, on the name `._proof_1_2`, which now denotes the other sub-proof;
   - 5 value changes: the three theorems, whose proofs cite the renumbered names, and two of the auxiliaries.

   **The statements of the three theorems are identical** (not in the TYPE list). For each theorem, the multiset of
   its auxiliary statements before equals the multiset after (2 = 2, equal) [MEASURED]. INFERRED cause: the
   counter skips names already present in the environment, and that environment differs now that the proofs share
   a module with `upR`'s matcher lemmas.
2. **Lazily realized matcher lemmas follow the merge.** 22 private equation/splitter lemmas of
   `Term.renameVar.match_1`/`renameVarList.match_1` that `P/HoleBudget` realized for itself are no longer realized
   there; they are found in the merged module. Three private `upR.match_1` lemmas are now realized in
   `Lang.Proofs.Subst`. `upR.eq_1/eq_2`, `liftIdx.eq_1` and `lowerIdx.eq_1` (realized in `P/Core` before) are now
   realized in `Lang.Proofs.Subst`, which is where `upR` is unfolded first. That accounts for the remaining 22
   vanished and 3 new constants, and 4 of the module changes.

## 4. `grep` and tables [MEASURED]

- `git grep LangRenaming|LangSubstitution|LangFilling|LangOccurrences|Contextual.HoleBudget` outside `decisions/`
  had one hit: `Lang/Subst.lean`'s header comment. It is rewritten to name `Lang.Proofs.Subst`/`Lang.Proofs.Fill` (a
  `/- -/` comment, no olean change).
- No explicit `Contextual.<moved name>` qualification anywhere (checked over all 99 names).
- No gates row, lakefile target or rows fixture names these modules.

## 5. SIZE [MEASURED `fold/S7-size-preview.txt`]

| row | before | after | why |
|---|---:|---:|---|
| Lean modules | 499 | 498 | −5 proof modules, +4 (Index, Subst, Fill, HoleBudget) |
| Lean proof-modules | 270 | 269 | the same |
| Lean lines (Lang) | 42,177 | 42,185 | +8: the three new headers and two section titles, net of the moved theorems |
| theorems, Host closure | unchanged | | no theorem added or removed; no deployed module touched |

## 6. Inverted question: is anything that survives weaker?

No.
- Every user statement is identical under the map.
- The three theorems whose proofs moved auxiliary names keep their statements and their auxiliaries' statements.
- No check, bound or refusal is touched.
- `P/Core` loses two lemmas that now live in `Lang.Proofs.Index` with identical statements. Its own proofs use them
  unchanged (through the parent namespace).

## 7. Planned landing

The paths of `fold/S7-candidate.patch` plus the four new files; `### LANG-74.7`; subject
`lang: the deployed-subject substitution and filling proofs leave Contextual — Lang/Proofs/{Index,Subst,Fill,HoleBudget}
(S7 of the consolidation)`. Fast path. Then S8 (the four Kernel/Ledger import lines, CROSS-LAYER).
