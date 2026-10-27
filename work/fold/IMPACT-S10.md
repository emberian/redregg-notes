# IMPACT-S10 — the provenance twin: P9's all-environment `provenance` replaces the env-specialized one (consolidation step S10)

Worker: CX-FOLD-3 (Claude). Written 2026-10-22, after building the candidate in scratch (`hbox:logs/cxfold/S10-tree`,
a copy of `wt/cxfold` at the S9 candidate, which is in the FULL judge as this is written). Base for every measurement:
the S9 candidate (`fold/S9-candidate.patch` on ac34521). Map: §1.5 (two `provenance`, two `provenance_iff`), §2.2
(:427–428, :443–444), §3.1 row S10, §3.2, §4.2 row S10. Tags READ / MEASURED / INFERRED. Judge: fast (`lang:`).
Candidate diff: `fold/S10-candidate.patch` (7 files). Edit script: `fold/S10-s10edit.py` (asserts every anchor).
Rename map: `fold/S10-renames.tsv` (one row: `Nanodregg.Lang.Contextual.P9` → `Nanodregg.Lang.Contextual`).
Census diff: `fold/diff-S10.txt`.

## 0. Answer first

The contextual spine has two provenance polynomials [READ]:
- `Contextual.provenance I env cs` (`Lang/Contextual/Closure.lean`:234–239): evaluates the guard and the budget at ONE
  environment and keeps only the token literals. Its theorem `Contextual.provenance_iff` (`P/Judge.lean`:106–125).
- `Contextual.P9.provenance I cs` (`Lang/Contextual/Provenance.lean`): keeps the guard and the budget as literals
  (`envLits`), so ONE polynomial answers at every world. Its theorem `P9.provenance_iff` (`P/Provenance.lean`:18).
- `P9.provenance_env_specialized` (`P/ProvenanceTeeth.lean`) is a theorem that the first loses an answer after an
  environment edit.

S10 keeps one. **P9's becomes THE `provenance`** (namespace `Nanodregg.Lang.Contextual`, no `P9`), its definitions
move into `Lang/Contextual/Closure.lean` at the place of the twin, and the twin goes with everything whose subject
it was. `tm_decEq_toy` loses its reflexive conjunct (map §2.2).

**No surviving theorem gains a hypothesis; none changes meaning** [MEASURED, §3]: 1 statement change
(`tm_decEq_toy`, a conjunct removed); 20 type-digest changes that are the implicit binder order `{D} {E}` → `{E} {D}`
(token multisets equal, MEASURED), because `Closure.lean` declares `variable {E}` before `variable {D}` and the moved
definitions now follow the convention of `judge`, `effSupports` and every other definition in that file.

## 1. What is deleted, and why

| constant | where | statement / role | reason |
|---|---|---|---|
| `Contextual.provenance` (+ `.eq_1`) | `C/Closure`:234–239 | the env-specialized polynomial `List (List Token × List Token)` | the twin: P9's polynomial at every env is the stronger object (map §2.2) |
| `Contextual.provenance_iff` (+ `_simp_1_2`, `_simp_1_3`) | `P/Judge`:106–125 | `(∃ c ∈ cs, judge I w c = .verified) ↔ ∃ m ∈ provenance I w.env cs, Monomial.holds w m` | the surviving `provenance_iff` has the SAME left side; its right side is one polynomial for every env (map §3.1) |
| `Contextual.Monomial.holds` | `P/ClosureStatements`:42–44 | `(∀ t ∈ m.1, live) ∧ (∀ b ∈ m.2, dead)` on a pair | its only use is the twin's theorem [MEASURED grep: `Judge.lean`:114 only]; `Monomial.eval` is the surviving evaluation |
| `P9.provenance_env_specialized` + private `toothIface`, `toothCandidate`, `toothWorld` | `P/ProvenanceTeeth` (whole file) | `Contextual.provenance toothIface toothWorld.env [toothCandidate] = [] ∧ judge … (setEnv true) … = .verified` | a tooth against the twin; no subject once it is gone (map §2.2:428) |
| `P9.specialize` (+ `.eq_1`) | `C/Provenance`:46–49 | evaluate `envLits` at one env, keep the token pair | its only theorems are the two below [MEASURED grep] |
| `P9.specialize_eq` | `P/Provenance`:29–42 | `specialize I env (provenance I cs) = Contextual.provenance I env cs` | Prop15 relates P9's polynomial TO the twin; its right side is the deleted def |
| `P9.provenance_update` | `P/Provenance`:44–48 | `Contextual.provenance I (e.apply w).env cs = specialize I (e.apply w).env (provenance I cs)` | `specialize_eq` at `e.apply w`; same subject |

`specialize`, `specialize_eq` and `provenance_update` are NOT in the map's S10 list (map §3.1 names only the twin's
theorem and the tooth). They are here because their statements name the twin. **The one choice for the reader**
(default: delete as listed):
- (a) delete (default). Keeping Prop15 would mean restating `specialize_eq` with the twin's body written inline on the
  right, which is the twin under no name: law 1's "second shape".
- (b) keep `specialize` and restate `specialize_eq` against the inline filter/map. RULE (b) if Prop15 is wanted as a
  fact about the one polynomial.

Statement counts: 4 theorems leave (`Judge.provenance_iff`, `specialize_eq`, `provenance_update`,
`provenance_env_specialized`) [MEASURED SIZE theorems 6078 → 6074]; 3 definitions (`provenance` twin,
`Monomial.holds`, `specialize`) and 3 private tooth constants.

## 2. What moves

`Lang/Contextual/Provenance.lean` is deleted; its definitions (`EnvLit`, `EnvLit.eval`, `Monomial`, `Monomial.envOK`,
`Monomial.eval`, `monomial`, `provenance`, `Monomial.consistent`, `Monomial.subsumes`, `minimal`, `label`) are inserted
verbatim into `Lang/Contextual/Closure.lean` at the twin's place, under a `## Provenance` section header that keeps
the file's citations (Grädel–Tannen, de Kleer, Doyle). The `provenance` docstring now says it is THE polynomial.
`Lang/Proofs/Contextual/Provenance.lean` stays a file; its namespace `…Contextual.P9` becomes `…Contextual`, its
`import Lang.Contextual.Provenance` goes (it reaches Closure through `P/Judge`), and `provenance_iff`'s docstring
no longer says it "preserves the landed fixed-environment theorem and its name".

Name map (one row, component prefix): every `Nanodregg.Lang.Contextual.P9.X` → `Nanodregg.Lang.Contextual.X`.
124 constants carry the rename [MEASURED]. After the map, `Contextual.provenance` and `Contextual.provenance_iff`
name P9's objects: the surviving names are the twin's names with the stronger content.

## 3. Census digest diff (S9 candidate → S10 candidate, under the map) [MEASURED `fold/diff-S10.txt`]

- 10 vanished, all declared (§1): `Monomial.holds`, `provenance_env_specialized`, `provenance_update`, `specialize`,
  `specialize.eq_1`, `specialize_eq`, the 4 private tooth constants. The 5 twin rows (`provenance`, `.eq_1`,
  `provenance_iff`, `_simp_1_2`, `_simp_1_3`) collide by name with P9's renamed objects; they are dropped from the
  before digest by name + module and listed in `fold/S10-twin-rows.txt`.
- 0 new constants. 72 module changes, all `Lang.Contextual.Provenance` → `Lang.Contextual.Closure`, 0 from any
  other module.
- 21 type-digest changes:
  - `tm_decEq_toy`: `A ≠ B ∧ C = C` → `A ≠ B`. The dropped conjunct is reflexive; nothing cites the theorem.
  - 20 others (`EnvLit.eval`, `Monomial.envOK`, `Monomial.eval`, `monomial`, `provenance`, `label` and their `eq_N`;
    `provenance_iff`, `label_iff`, `minimal_eval`, `monomial_verified`, `monomial_complementary_dead`,
    `eval_consistent`, `subsumes_eval`): each before/after type string has the SAME token multiset and length
    [MEASURED]. The difference is the order of the implicit binders `{D : CalculusData} {E : Type}` and the matching
    explicit argument order in applications (`judge E D …` was already the Closure order). No binder is added.
- 25 value-hash changes: the same moved definitions and their proofs, from the binder order.
- Kernel/Ledger/Host/Census: 0 vanished, 0 type, 0 value changes.

## 4. Consumers [MEASURED `git grep` over Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench Ops gates rows lakefile.lean]

- `Contextual.provenance` (twin): `P/Provenance`:33,40,46 (the two deleted theorems), `P/ProvenanceTeeth`:16. Nothing
  else.
- `provenance_iff`: `P/Judge`:112 (deleted), `P/Provenance`:18 (survives), `:190` (`label_iff`'s proof, now the
  survivor by the same name).
- `Monomial.holds`: `P/Judge`:114 only. `specialize*`, `provenance_update`, `P9.*`: only inside the two P9 files and
  the tooth.
- `import Lang.Contextual.Provenance`: `P/Provenance`:2 only. `ProvenanceTeeth`: no importer.
- gates tables, rows, lakefile: no hit (the lakefile globs `Lang`); `gates/certificate-grant.json.gz` decompressed: no
  hit. Decisions: `decisions/lang.md` LANG-P9 (:3681ff) names `P9.provenance_iff`, `specialize_eq`,
  `provenance_update`; append-only, so the S10 decision is the pointer.

## 5. The inverted question: what surviving module or row is weaker?

None [MEASURED + READ]. The only theorem relating judgment to a provenance polynomial that survives is
`provenance_iff` (P9's): same left side as the deleted one, for every world; `label_iff` still rests on it. The
deleted `Judge.provenance_iff`'s right side is implied at each world by the survivor's (evaluate `envLits` at `w.env`),
so nothing a consumer could use is lost; and it has no consumer. Prop15 (`specialize_eq`) is the one fact that goes
without a stronger survivor; it was a fact about the relation to the twin (§1, the reader's choice).

## 6. Gates [MEASURED, scratch tree]

`lake build Lang` GREEN (224 jobs); whole tree `Lang Kernel Ledger Census Host Hosting Protocol Codec Emit Bench Ops
host lang-journey codec-vectors` GREEN (624 jobs); `lang-journey` byte-identical to the S9 candidate's (787 lines);
`gates/check.py` GREEN with the generated SIZE (Lean modules 494 → 492, proof modules 265 → 264, theorems 6078 → 6074;
Lang lines 42368 → 42286). Re-emit: none. Nothing refuses to load: no persisted or wire object names these.

## 7. What breaks (said in the commit)

`Lang/Contextual/Provenance.lean` and `Lang/Proofs/Contextual/ProvenanceTeeth.lean` no longer exist; `Contextual.P9.*`
no longer resolves (the names lose `P9`); `Contextual.provenance` and `Contextual.provenance_iff` now mean the
all-environment objects; `Monomial.holds`, `specialize`, `specialize_eq`, `provenance_update` are gone; the moved
definitions take `{E} {D}` implicitly in that order. Nothing in the tree outside these files uses any of them.
