# IMPACT-S5 — delete the worlds, the acyclic adapter and stability, with the experiment-4 definitions they alone used (consolidation step S5)

Worker: CX-FOLD (Claude). Written 2026-10-22 (after LAND a747368). Base: nanodregg `origin/main` = **a747368** (S1
f665e94/82ac944/6eb92fe, S2 a9ab514, S3 e1ccc50, S4 a747368). Candidate: uncommitted in
`hbox:/tank/dregg-build/nanodregg/wt/cxfold` (5 deleted files + `fold/S5-spine.diff`, 56 lines, deletions only, in
`Lang/Contextual/Closure.lean` and `Lang/Proofs/Contextual/ClosureStatements.lean`). Nothing landed. Map: §1.3,
§2.2 D-RULES, §3.1 row S5, §4.2 row S5. Tags READ / MEASURED / INFERRED.

## 0. Answer first

**No surviving theorem, gates row, lakefile target or rows fixture is weaker after S5.** Census diff of the whole tree
a747368 → candidate: 500 constants vanish: the 458 constants of the 5 modules and **42 constants of exactly seven
declared definitions in two surviving spine modules** (with their generated constants), §2; 0 surviving statements
change; 0 value hashes change; 0 new; 0 re-owned; 0 surviving constants referenced any of the 458 [MEASURED
`fold/diff-S5.txt`, before-run refs column]. Whole-tree build + `host` + `lang-journey` GREEN (630 jobs); the journey
GREEN. `gates/check.py` GREEN with the generated SIZE.

**One ordering choice for the reader (§2), default as proposed:** S5 deletes the experiment-4 definitions
`Rule`/`lfpIter`/`supportCount`/`countRun` from `Closure` (the map scheduled them for S10) and the Prop definitions
`ValueGuard`/`StableUnder`/`Derives` from `ClosureStatements` (the map did not list them), because S5 deletes the last
theorems that mention any of them. Kept until S10 they would be definitions with no theorem — the no-op CLAUDE.md
forbids — and READ-S1's note asked exactly this: "S5 deletes `counting_keeps_cycle_over_worlds` while `countRun` still
exists … S5 must delete `countRun` or keep that tooth."

## 1. The five modules [MEASURED; READ imports]

| # | file | lines | imported by | imports | user theorems | other user decls |
|---:|---|---:|---|---|---:|---:|
| 1 | `Lang/Contextual/Worlds.lean` | 123 | P/Worlds | C/Closure | 0 | 63 |
| 2 | `Lang/Proofs/Contextual/Worlds.lean` | 326 | — | C/Worlds, P/Stability | 21 | 1 |
| 3 | `Lang/Contextual/Acyclic.lean` | 65 | P/Acyclic | C/Closure | 0 | 55 |
| 4 | `Lang/Proofs/Contextual/Acyclic.lean` | 219 | — | C/Acyclic, P/Judge | 18 | 17 |
| 5 | `Lang/Proofs/Contextual/Stability.lean` | 86 | P/Worlds | P/Judge | 6 | 0 |
| | **total** | **819** | | | **45** | |

(The "other user decls" column is from the elaborated environment, `fold/S5-decls.tsv`; theorem counts match the
map's 45.)

**Reasons (map §2.2 D-RULES):** a second rule semantics beside the closure.
- `C/Worlds` + `P/Worlds`: P3's alternative worlds / stable-model rule programs with their own `Report` ("not a
  second kernel World or an admission path" — which is what it is beside). It holds the program's last copies of the
  counting teeth `cycle_loses_grounding_over_worlds` and `counting_keeps_cycle_over_worlds`, over P3's own rule
  programs.
- `C/Acyclic` + `P/Acyclic`: P12's rank-witnessed hole-unrolling adapter with its own `Expr`, `Graph`, `Refusal` and
  its own `Derives`; `P/DeployedCycle` compiles a grounded cycle into a deployed filling, the substrate version.
- `P/Stability`: `lfpIter_sound`, `stability_class`, value-guard facts; its consumers were Experiments (S1),
  TransportKinds (S4) and Worlds.

## 2. The seven spine definitions that leave with them [MEASURED `git grep -w` over `*.lean` at a747368]

| definition | module | every use outside the 5 deleted files |
|---|---|---|
| `Rule` (structure) | `Lang/Contextual/Closure.lean`:548 | `lfpIter`/`supportCount`/`countRun` (same section), `ClosureStatements.Derives` |
| `lfpIter` | `Closure.lean`:553 | none |
| `supportCount` | `Closure.lean`:558 | `countRun` |
| `countRun` | `Closure.lean`:563 | none |
| `ValueGuard` (Prop def) | `Lang/Proofs/Contextual/ClosureStatements.lean`:75 | none |
| `StableUnder` (Prop def) | `ClosureStatements.lean`:79 | none |
| `Derives` (inductive Prop) | `ClosureStatements.lean`:83 | none (`Lang/Proofs/Complete.lean`'s `Derives` is `Lang.Derives`, a different constant; `P/Acyclic`'s is its own, deleted here) |

Their only theorem consumers were `P/Stability` (`lfpIter_sound` etc.), `P/Worlds` and, before S1, `P/Experiments`.
The diff removes the section `/-! ## Support closure: least fixpoint versus counting (experiment 4) -/`
(`Closure.lean`:546–566) and `ClosureStatements.lean`:74–85, and nothing else (`fold/S5-spine.diff`, 56 lines, only `-`
lines). The 42 non-module constants that vanish are exactly these seven and their generated constants (`.rec`,
`.casesOn`, `.mk`, `.injEq`, `._sunfold`, `.match_1`, …) [MEASURED, listed in `logs/cxfold` output, reproduced in
§5].

Price [INFERRED]: `Closure.lean` is in the Host closure, so this rebuilds the Host (the candidate built `host` GREEN);
"Lean lines (deployed)" falls by those 21 lines as well, a real reduction of the Host closure's source. No
statement elsewhere names them, so no theorem gains or loses a premise. The alternative is to keep the seven until
S10, as definitions with no theorem.

## 3. `grep` of every deleted name [MEASURED, scope as IMPACT-S1 §2]

181 user declarations of the 5 modules, 125 distinct last components: fully qualified 0 hits; 537 dotted relative
forms 0 hits; 47 bare components occur elsewhere as words (`fold/S5-grep.txt`), none a use (refs column empty).
Concept words (`Worlds WorldsField Acyclic Stability P3 P12 lfpIter countRun`) in surviving Lang Kernel Ledger Host
Census sources: only Kernel/Host prose about kernel `World`s, and the two `Closure.lean` definitions this step deletes.

## 4. Gates tables, lakefile targets, rows fixtures [MEASURED]

No lakefile target or root, no `gates/*.tsv` row, `rows/run` line or golden names a deleted module or definition. No
generated file or wire vector changes.

## 5. Census digest diff and SIZE [MEASURED `fold/diff-S5.txt`, `fold/S5-size-preview.txt`]

```
before 51739 after 51239
vanished 500 of which outside the declared modules 42      (the seven definitions of §2 and their generated constants)
new 0 type-digest changed 0 value-hash changed 0 module changed 0
```
SIZE: Lean modules 504 → 499; proof-modules 273 → 270; Lean lines (Lang) 43,047 → 42,192 (−855 = 819 + 36);
"Lean lines (deployed)" 29,763 → 29,554 (−209: C/Worlds 123 + C/Acyclic 65 + Closure's 21); theorems 6,126 → 6,081;
Host closure 91 (unchanged in modules).

## 6. Planned S5 diff and gates

Delete the 5 files and the seven definitions (this list is the landing's explicit deletion authorization);
`### LANG-74.5` in `decisions/lang.md`; SIZE regenerated. Before landing: paths asserted absent; digest diff re-run
against main; `gates/check.py`; reached build (Host included); `scripts/commit` fast path, subject `lang: delete the
worlds, the acyclic adapter and stability, with the experiment-4 definitions only they used (S5 of the
consolidation)`. After S5 the map's pure-deletion phase is complete (S1–S5).

## Appendix — the 45 deleted theorem statements [MEASURED: `ppExpr` of each elaborated type at a747368]

#### `Lang.Proofs.Contextual.Worlds` — D-RULES

- :15 `Nanodregg.Lang.Contextual.Worlds.derives_head` : `∀ {E : Type} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {v : Nanodregg.Lang.Contextual.Worlds.Alternative} {x : Nat}, Nanodregg.Lang.Contextual.Derives (Nanodregg.Lang.Contextual.Worlds.reduct P w v) (fun x => false) x → x ∈ Nanodregg.Lang.Contextual.Worlds.heads P` — DELETE (D-RULES)
- :26 `Nanodregg.Lang.Contextual.Worlds.closed_complete` : `∀ {R : List Nanodregg.Lang.Contextual.Rule} {n : Nat}, Nanodregg.Lang.Contextual.Worlds.closed R (Nanodregg.Lang.Contextual.Worlds.ground R n) = true → ∀ {x : Nat}, Nanodregg.Lang.Contextual.Derives R (fun x => false) x → Nanodregg.Lang.Contextual.Worlds.ground R n x = true` — DELETE (D-RULES)
- :38 `Nanodregg.Lang.Contextual.Worlds.check_iff_stable` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {v : Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.closed (Nanodregg.Lang.Contextual.Worlds.reduct P w v) (Nanodregg.Lang.Contextual.Worlds.ground (Nanodregg.Lang.Contextual.Worlds.reduct P w v) rounds) = true → (Nanodregg.Lang.Contextual.Worlds.check rounds P w v = some true ↔ Nanodregg.Lang.Contextual.Worlds.Stable P w v)` — DELETE (D-RULES)
- :61 `Nanodregg.Lang.Contextual.Worlds.check_decides` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {v : Nanodregg.Lang.Contextual.Worlds.Alternative} {b : Bool}, Nanodregg.Lang.Contextual.Worlds.check rounds P w v = some b → (b = true ↔ Nanodregg.Lang.Contextual.Worlds.Stable P w v)` — DELETE (D-RULES)
- :72 `Nanodregg.Lang.Contextual.Worlds.unfounded_excluded` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {v : Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.check rounds P w v = some true → ∀ {S : Nat → Prop}, (∀ (r : Nanodregg.Lang.Contextual.Rule), r ∈ Nanodregg.Lang.Contextual.Worlds.reduct P w v → S r.head → ∃ y, y ∈ r.body ∧ S y) → ∀ {x : Nat}, S x → ¬x ∈ v` — DELETE (D-RULES)
- :81 `Nanodregg.Lang.Contextual.Worlds.collect_checked` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {vs ws : List Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.collect rounds P w vs = some ws → ∀ (v : Nanodregg.Lang.Contextual.Worlds.Alternative), v ∈ vs → ∃ b, Nanodregg.Lang.Contextual.Worlds.check rounds P w v = some b` — DELETE (D-RULES)
- :99 `Nanodregg.Lang.Contextual.Worlds.collect_mem` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {vs ws : List Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.collect rounds P w vs = some ws → ∀ (v : Nanodregg.Lang.Contextual.Worlds.Alternative), v ∈ ws ↔ v ∈ vs ∧ Nanodregg.Lang.Contextual.Worlds.check rounds P w v = some true` — DELETE (D-RULES)
- :137 `Nanodregg.Lang.Contextual.Worlds.analyze_exact` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {ws : List Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.analyze rounds P w = some ws → ∀ (v : Nanodregg.Lang.Contextual.Worlds.Alternative), v ∈ ws ↔ v ∈ Nanodregg.Lang.Contextual.Worlds.subsets (Nanodregg.Lang.Contextual.Worlds.heads P) ∧ Nanodregg.Lang.Contextual.Worlds.Stable P w v` — DELETE (D-RULES)
- :153 `Nanodregg.Lang.Contextual.Worlds.mem_subsets_iff` : `∀ (v xs : List Nat), v ∈ Nanodregg.Lang.Contextual.Worlds.subsets xs ↔ v.Sublist xs` — DELETE (D-RULES)
- :168 `Nanodregg.Lang.Contextual.Worlds.analyze_sublist_exact` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {ws : List Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.analyze rounds P w = some ws → ∀ (v : Nanodregg.Lang.Contextual.Worlds.Alternative), v ∈ ws ↔ List.Sublist v (Nanodregg.Lang.Contextual.Worlds.heads P) ∧ Nanodregg.Lang.Contextual.Worlds.Stable P w v` — DELETE (D-RULES)
- :173 `Nanodregg.Lang.Contextual.Worlds.alternatives_sound` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {positive negative : Nat} {proposed left right : Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.report rounds P w positive negative proposed = Nanodregg.Lang.Contextual.Worlds.Report.alternatives left right → Nanodregg.Lang.Contextual.Worlds.Stable P w left ∧ Nanodregg.Lang.Contextual.Worlds.Stable P w right ∧ positive ∈ left ∧ negative ∈ right ∧ left ≠ right` — DELETE (D-RULES)
- :204 `Nanodregg.Lang.Contextual.Worlds.noJustification_sound` : `∀ {E : Type} {rounds : Nat} {P : Nanodregg.Lang.Contextual.Worlds.Program} {w : Nanodregg.Lang.Contextual.World E} {positive negative : Nat} {proposed : Nanodregg.Lang.Contextual.Worlds.Alternative}, Nanodregg.Lang.Contextual.Worlds.report rounds P w positive negative proposed = Nanodregg.Lang.Contextual.Worlds.Report.noJustification → ∃ ws, Nanodregg.Lang.Contextual.Worlds.analyze rounds P w = some ws ∧ ws ≠ [] ∧ ∀ (v : Nanodregg.Lang.Contextual.Worlds.Alternative), v ∈ ws → ¬positive ∈ v ∧ ¬negative ∈ v` — DELETE (D-RULES)
- :234 `Nanodregg.Lang.Contextual.Worlds.Experiment.two_rule_worlds` : `Nanodregg.Lang.Contextual.Worlds.analyze 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial = some [[1], [0]] ∧ Nanodregg.Lang.Contextual.Worlds.check 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial [0] = some true ∧ Nanodregg.Lang.Contextual.Worlds.check 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial [1] = some true` — DELETE (D-RULES)
- :240 `Nanodregg.Lang.Contextual.Worlds.Experiment.admissible_not_union_closed` : `Nanodregg.Lang.Contextual.Worlds.check 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial [0] = some true ∧ Nanodregg.Lang.Contextual.Worlds.check 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial [1] = some true ∧ Nanodregg.Lang.Contextual.Worlds.check 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial (Nanodregg.Lang.Contextual.Worlds.Experiment.union [0] [1]) = some false` — DELETE (D-RULES)
- :246 `Nanodregg.Lang.Contextual.Worlds.Experiment.union_not_stable` : `¬Nanodregg.Lang.Contextual.Worlds.Stable Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial (Nanodregg.Lang.Contextual.Worlds.Experiment.union [0] [1])` — DELETE (D-RULES)
- :253 `Nanodregg.Lang.Contextual.Worlds.Experiment.withdraw_and_reassert` : `Nanodregg.Lang.Contextual.Worlds.session 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules [Nanodregg.Lang.Contextual.Edit.withdraw Nanodregg.Lang.Contextual.Worlds.Experiment.pToken, Nanodregg.Lang.Contextual.Edit.withdraw Nanodregg.Lang.Contextual.Worlds.Experiment.qToken, Nanodregg.Lang.Contextual.Edit.assert Nanodregg.Lang.Contextual.Worlds.Experiment.pToken, Nanodregg.Lang.Contextual.Edit.assert Nanodregg.Lang.Contextual.Worlds.Experiment.qToken] Nanodregg.Lang.Contextual.Worlds.Experiment.initial = [some [[1], [0]], some [[1]], some [[]], some [[0]], some [[1], [0]]]` — DELETE (D-RULES)
- :260 `Nanodregg.Lang.Contextual.Worlds.Experiment.reissue_does_not_restore_rule` : `Nanodregg.Lang.Contextual.Worlds.analyze 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules (Nanodregg.Lang.Contextual.applyAll (Nanodregg.Lang.Contextual.reissue 10 0 1) Nanodregg.Lang.Contextual.Worlds.Experiment.neither) = some [[]] ∧ (Nanodregg.Lang.Contextual.applyAll (Nanodregg.Lang.Contextual.reissue 10 0 1) Nanodregg.Lang.Contextual.Worlds.Experiment.neither).live { id := 10, ver := 1 } = true ∧ (Nanodregg.Lang.Contextual.applyAll (Nanodregg.Lang.Contextual.reissue 10 0 1) Nanodregg.Lang.Contextual.Worlds.Experiment.neither).live Nanodregg.Lang.Contextual.Worlds.Experiment.pToken = false` — DELETE (D-RULES)
- :266 `Nanodregg.Lang.Contextual.Worlds.Experiment.four_reports` : `Nanodregg.Lang.Contextual.Worlds.report 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.neither 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.noJustification ∧ Nanodregg.Lang.Contextual.Worlds.report 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.alternatives [0] [1] ∧ Nanodregg.Lang.Contextual.Worlds.report 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial 0 1 Nanodregg.Lang.Contextual.Worlds.Experiment.both = Nanodregg.Lang.Contextual.Worlds.Report.conflictingEvidence Nanodregg.Lang.Contextual.Worlds.Experiment.both ∧ Nanodregg.Lang.Contextual.Worlds.report 0 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.initial 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.unfinished` — DELETE (D-RULES)
- :274 `Nanodregg.Lang.Contextual.Worlds.Experiment.no_world_is_distinct` : `Nanodregg.Lang.Contextual.Worlds.report 2 [{ head := 0, body := [], absent := [0], supports := [] }] Nanodregg.Lang.Contextual.Worlds.Experiment.initial 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.noWorld ∧ Nanodregg.Lang.Contextual.Worlds.report 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.neither 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.noJustification ∧ Nanodregg.Lang.Contextual.Worlds.report 2 Nanodregg.Lang.Contextual.Worlds.Experiment.twoRules Nanodregg.Lang.Contextual.Worlds.Experiment.withdrawn 0 1 [] = Nanodregg.Lang.Contextual.Worlds.Report.supported [[1]]` — DELETE (D-RULES)
- :280 `Nanodregg.Lang.Contextual.Worlds.Experiment.cycle_loses_grounding_over_worlds` : `Nanodregg.Lang.Contextual.Worlds.session 4 Nanodregg.Lang.Contextual.Worlds.Experiment.cycle [Nanodregg.Lang.Contextual.Edit.withdraw Nanodregg.Lang.Contextual.Worlds.Experiment.pToken, Nanodregg.Lang.Contextual.Edit.assert Nanodregg.Lang.Contextual.Worlds.Experiment.pToken] Nanodregg.Lang.Contextual.Worlds.Experiment.initial = [some [Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle], some [Nanodregg.Lang.Contextual.Worlds.Experiment.afterCycle], some [Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle]] ∧ Nanodregg.Lang.Contextual.Worlds.check 4 Nanodregg.Lang.Contextual.Worlds.Experiment.cycle Nanodregg.Lang.Contextual.Worlds.Experiment.withdrawn Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle = some false` — DELETE (D-RULES)
- :287 `Nanodregg.Lang.Contextual.Worlds.Experiment.counting_keeps_cycle_over_worlds` : `∀ (n : Nat), Nanodregg.Lang.Contextual.countRun (Nanodregg.Lang.Contextual.Worlds.reduct Nanodregg.Lang.Contextual.Worlds.Experiment.cycle Nanodregg.Lang.Contextual.Worlds.Experiment.withdrawn Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle) (fun x => false) (List.contains Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle) n 1 = true ∧ Nanodregg.Lang.Contextual.countRun (Nanodregg.Lang.Contextual.Worlds.reduct Nanodregg.Lang.Contextual.Worlds.Experiment.cycle Nanodregg.Lang.Contextual.Worlds.Experiment.withdrawn Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle) (fun x => false) (List.contains Nanodregg.Lang.Contextual.Worlds.Experiment.beforeCycle) n 2 = true` — DELETE (D-RULES)

#### `Lang.Proofs.Contextual.Acyclic` — D-RULES

- :29 `Nanodregg.Lang.Contextual.Acyclic.holds_product` : `∀ {E : Type} (w : Nanodregg.Lang.Contextual.World E) (p q : Nanodregg.Lang.Contextual.Acyclic.Polynomial), Nanodregg.Lang.Contextual.Acyclic.Holds w (Nanodregg.Lang.Contextual.Acyclic.product p q) ↔ Nanodregg.Lang.Contextual.Acyclic.Holds w p ∧ Nanodregg.Lang.Contextual.Acyclic.Holds w q` — DELETE (D-RULES)
- :45 `Nanodregg.Lang.Contextual.Acyclic.holds_append` : `∀ {E : Type} (w : Nanodregg.Lang.Contextual.World E) (p q : Nanodregg.Lang.Contextual.Acyclic.Polynomial), Nanodregg.Lang.Contextual.Acyclic.Holds w (p ++ q) ↔ Nanodregg.Lang.Contextual.Acyclic.Holds w p ∨ Nanodregg.Lang.Contextual.Acyclic.Holds w q` — DELETE (D-RULES)
- :49 `Nanodregg.Lang.Contextual.Acyclic.mem_edges` : `∀ {n : Nat} (g : Nanodregg.Lang.Contextual.Acyclic.Graph n) (i j : Fin n), (i, j) ∈ g.edges ↔ j ∈ (g.body i).refs` — DELETE (D-RULES)
- :53 `Nanodregg.Lang.Contextual.Acyclic.validate_iff` : `∀ {n : Nat} (g : Nanodregg.Lang.Contextual.Acyclic.Graph n), Nanodregg.Lang.Contextual.Acyclic.validate g = none ↔ Nanodregg.Lang.Contextual.Acyclic.Ranked g` — DELETE (D-RULES)
- :64 `Nanodregg.Lang.Contextual.Acyclic.depends_rank` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n}, Nanodregg.Lang.Contextual.Acyclic.Ranked g → ∀ {i j : Fin n}, Nanodregg.Lang.Contextual.Acyclic.Depends g i j → g.rank j < g.rank i` — DELETE (D-RULES)
- :70 `Nanodregg.Lang.Contextual.Acyclic.cycles_not_ranked` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {i : Fin n}, Nanodregg.Lang.Contextual.Acyclic.Depends g i i → ¬Nanodregg.Lang.Contextual.Acyclic.Ranked g` — DELETE (D-RULES)
- :74 `Nanodregg.Lang.Contextual.Acyclic.expand_sound` : `∀ {n : Nat} {E : Type} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {w : Nanodregg.Lang.Contextual.World E} {lookup : Fin n → Nanodregg.Lang.Contextual.Acyclic.Polynomial}, (∀ (i : Fin n), Nanodregg.Lang.Contextual.Acyclic.Holds w (lookup i) → Nanodregg.Lang.Contextual.Acyclic.Derives g w (Nanodregg.Lang.Contextual.Acyclic.Expr.hole i)) → ∀ (e : Nanodregg.Lang.Contextual.Acyclic.Expr n), Nanodregg.Lang.Contextual.Acyclic.Holds w (Nanodregg.Lang.Contextual.Acyclic.Expr.expand lookup e) → Nanodregg.Lang.Contextual.Acyclic.Derives g w e` — DELETE (D-RULES)
- :91 `Nanodregg.Lang.Contextual.Acyclic.unroll_sound` : `∀ {n : Nat} {E : Type} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {w : Nanodregg.Lang.Contextual.World E} (fuel : Nat) (i : Fin n), Nanodregg.Lang.Contextual.Acyclic.Holds w (Nanodregg.Lang.Contextual.Acyclic.unroll g fuel i) → Nanodregg.Lang.Contextual.Acyclic.Derives g w (Nanodregg.Lang.Contextual.Acyclic.Expr.hole i)` — DELETE (D-RULES)
- :97 `Nanodregg.Lang.Contextual.Acyclic.expand_complete` : `∀ {n : Nat} {E : Type} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {w : Nanodregg.Lang.Contextual.World E} {lookup : Fin n → Nanodregg.Lang.Contextual.Acyclic.Polynomial} (e : Nanodregg.Lang.Contextual.Acyclic.Expr n), (∀ (i : Fin n), i ∈ e.refs → Nanodregg.Lang.Contextual.Acyclic.Derives g w (Nanodregg.Lang.Contextual.Acyclic.Expr.hole i) → Nanodregg.Lang.Contextual.Acyclic.Holds w (lookup i)) → Nanodregg.Lang.Contextual.Acyclic.Derives g w e → Nanodregg.Lang.Contextual.Acyclic.Holds w (Nanodregg.Lang.Contextual.Acyclic.Expr.expand lookup e)` — DELETE (D-RULES)
- :118 `Nanodregg.Lang.Contextual.Acyclic.unroll_complete` : `∀ {n : Nat} {E : Type} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {w : Nanodregg.Lang.Contextual.World E}, Nanodregg.Lang.Contextual.Acyclic.Ranked g → ∀ (fuel : Nat) (i : Fin n), g.rank i < fuel → Nanodregg.Lang.Contextual.Acyclic.Derives g w (Nanodregg.Lang.Contextual.Acyclic.Expr.hole i) → Nanodregg.Lang.Contextual.Acyclic.Holds w (Nanodregg.Lang.Contextual.Acyclic.unroll g fuel i)` — DELETE (D-RULES)
- :133 `Nanodregg.Lang.Contextual.Acyclic.adapt_correct` : `∀ {n : Nat} {E : Type} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {i : Fin n} {p : Nanodregg.Lang.Contextual.Acyclic.Polynomial}, Nanodregg.Lang.Contextual.Acyclic.adapt g i = Except.ok p → ∀ (w : Nanodregg.Lang.Contextual.World E), Nanodregg.Lang.Contextual.Acyclic.Holds w p ↔ Nanodregg.Lang.Contextual.Acyclic.Derives g w (Nanodregg.Lang.Contextual.Acyclic.Expr.hole i)` — DELETE (D-RULES)
- :144 `Nanodregg.Lang.Contextual.Acyclic.adapt_acyclic` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {root : Fin n} {p : Nanodregg.Lang.Contextual.Acyclic.Polynomial}, Nanodregg.Lang.Contextual.Acyclic.adapt g root = Except.ok p → ∀ (i : Fin n), ¬Nanodregg.Lang.Contextual.Acyclic.Depends g i i` — DELETE (D-RULES)
- :153 `Nanodregg.Lang.Contextual.Acyclic.cycle_refused` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {i : Fin n}, Nanodregg.Lang.Contextual.Acyclic.Depends g i i → ∀ (root : Fin n), ∃ reason, Nanodregg.Lang.Contextual.Acyclic.adapt g root = Except.error reason` — DELETE (D-RULES)
- :161 `Nanodregg.Lang.Contextual.Acyclic.refusal_explained` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n} {root : Fin n} {reason : Nanodregg.Lang.Contextual.Acyclic.Refusal}, Nanodregg.Lang.Contextual.Acyclic.adapt g root = Except.error reason → ∃ i j, j ∈ (g.body i).refs ∧ g.rank i ≤ g.rank j ∧ reason = if i = j then Nanodregg.Lang.Contextual.Acyclic.Refusal.fixedPointDependency ↑i else Nanodregg.Lang.Contextual.Acyclic.Refusal.rankNotDecreasing ↑i ↑j` — DELETE (D-RULES)
- :175 `Nanodregg.Lang.Contextual.Acyclic.ranked_accepted` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n}, Nanodregg.Lang.Contextual.Acyclic.Ranked g → ∀ (i : Fin n), Nanodregg.Lang.Contextual.Acyclic.adapt g i = Except.ok (Nanodregg.Lang.Contextual.Acyclic.unroll g (g.rank i + 1) i)` — DELETE (D-RULES)
- :180 `Nanodregg.Lang.Contextual.Acyclic.expand_congr` : `∀ {n : Nat} (e : Nanodregg.Lang.Contextual.Acyclic.Expr n) (f f' : Fin n → Nanodregg.Lang.Contextual.Acyclic.Polynomial), (∀ (j : Fin n), j ∈ e.refs → f j = f' j) → Nanodregg.Lang.Contextual.Acyclic.Expr.expand f e = Nanodregg.Lang.Contextual.Acyclic.Expr.expand f' e` — DELETE (D-RULES)
- :195 `Nanodregg.Lang.Contextual.Acyclic.unroll_stable` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n}, Nanodregg.Lang.Contextual.Acyclic.Ranked g → ∀ (k m : Nat) (i : Fin n), g.rank i < k → g.rank i < m → Nanodregg.Lang.Contextual.Acyclic.unroll g k i = Nanodregg.Lang.Contextual.Acyclic.unroll g m i` — DELETE (D-RULES)
- :209 `Nanodregg.Lang.Contextual.Acyclic.unroll_equation` : `∀ {n : Nat} {g : Nanodregg.Lang.Contextual.Acyclic.Graph n}, Nanodregg.Lang.Contextual.Acyclic.Ranked g → ∀ (i : Fin n), Nanodregg.Lang.Contextual.Acyclic.unroll g (g.rank i + 1) i = Nanodregg.Lang.Contextual.Acyclic.Expr.expand (fun j => Nanodregg.Lang.Contextual.Acyclic.unroll g (g.rank j + 1) j) (g.body i)` — DELETE (D-RULES)

#### `Lang.Proofs.Contextual.Stability` — D-RULES

- :12 `Nanodregg.Lang.Contextual.valueGuard_iff` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E V : Type} (value : D.Tm → V) (g : E → D.Tm → Bool), Nanodregg.Lang.Contextual.ValueGuard value g ↔ ∀ (e : E) (t t' : D.Tm), value t = value t' → g e t = g e t'` — DELETE (D-RULES)
- :27 `Nanodregg.Lang.Contextual.stability_class` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E V : Type} (value : D.Tm → V) {g : E → D.Tm → Bool}, Nanodregg.Lang.Contextual.ValueGuard value g → ∀ {s : D.Tm → D.Tm}, (∀ (t : D.Tm), value (s t) = value t) → Nanodregg.Lang.Contextual.StableUnder g s` — DELETE (D-RULES)
- :34 `Nanodregg.Lang.Contextual.judge_stable` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E V : Type} (value : D.Tm → V) {I : Nanodregg.Lang.Contextual.Iface D E}, Nanodregg.Lang.Contextual.ValueGuard value I.guard → ∀ {w : Nanodregg.Lang.Contextual.World E} {c c' : Nanodregg.Lang.Contextual.Candidate D}, value c'.filling = value c.filling → D.check I.ctx c'.filling I.ty = D.check I.ctx c.filling I.ty → c'.blockers = c.blockers → Nanodregg.Lang.Contextual.effSupports I c' = Nanodregg.Lang.Contextual.effSupports I c → c'.cost = c.cost → Nanodregg.Lang.Contextual.judge I w c' = Nanodregg.Lang.Contextual.judge I w c` — DELETE (D-RULES)
- :48 `Nanodregg.Lang.Contextual.lfpIter_sound` : `∀ {R : List Nanodregg.Lang.Contextual.Rule} {F : Nat → Bool} (n x : Nat), Nanodregg.Lang.Contextual.lfpIter R F n x = true → Nanodregg.Lang.Contextual.Derives R F x` — DELETE (D-RULES)
- :59 `Nanodregg.Lang.Contextual.no_facts_no_derivation` : `∀ {R : List Nanodregg.Lang.Contextual.Rule} {F : Nat → Bool}, (∀ (x : Nat), F x = false) → (∀ (r : Nanodregg.Lang.Contextual.Rule), r ∈ R → r.body ≠ []) → ∀ {x : Nat}, ¬Nanodregg.Lang.Contextual.Derives R F x` — DELETE (D-RULES)
- :72 `Nanodregg.Lang.Contextual.unfounded_not_derivable` : `∀ {R : List Nanodregg.Lang.Contextual.Rule} {F : Nat → Bool} {S : Nat → Prop}, (∀ (x : Nat), S x → F x = false) → (∀ (r : Nanodregg.Lang.Contextual.Rule), r ∈ R → S r.head → ∃ y, y ∈ r.body ∧ S y) → ∀ {x : Nat}, S x → ¬Nanodregg.Lang.Contextual.Derives R F x` — DELETE (D-RULES)
