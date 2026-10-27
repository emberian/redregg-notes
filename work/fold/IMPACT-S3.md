# IMPACT-S3 — delete P5, the games, the nogoods, the material guards and C/P1 (consolidation step S3)

Worker: CX-FOLD (Claude). Written 2026-10-22 (after LAND a9ab514). Base: nanodregg `origin/main` = **a9ab514**
(S1 f665e94/82ac944/6eb92fe, S2 a9ab514). Worktree `hbox:/tank/dregg-build/nanodregg/wt/cxfold`, measured by a scratch
deletion and restored (clean). Nothing landed. Map: §1.3, §2.2 D-JUDGE, §3.1 row S3, §4.2 row S3. Tool and method as
IMPACT-S1 §3/§5 (script `logs/cxfold/step.sh S3` on hbox). Tags READ / MEASURED / INFERRED.

## 0. Answer first

**No surviving module, theorem, definition, gates row, lakefile target or rows fixture is weaker after S3.** Census
diff of the whole tree (11 libraries) a9ab514 → scratch deletion: 1,027 constants vanish, every one a constant of
the 11 modules; 0 surviving statements change; 0 value hashes change; 0 new; one lazily realized lemma of the
surviving `Closure.Iface.mk` (`Iface.mk.congr_simp`) is re-owned, statement identical; **0 surviving constants
reference any of the 1,028 constants of the 11 modules** (same `Census.Journal.expressionEdges` detector whose
control fired in IMPACT-S1) [MEASURED `fold/diff-S3.txt`]. Whole-tree build after the deletion GREEN (530 jobs =
541 − 11). `gates/check.py` GREEN with the generated SIZE.

Nothing for the reader to rule beyond the delete list itself; one note in §6.

## 1. The eleven modules [MEASURED lines, importers, declarations; READ imports]

| # | file | lines | imported by (all inside this set at a9ab514) | user theorems | other user decls |
|---:|---|---:|---|---:|---|
| 1 | `Lang/Contextual/P5.lean` | 136 | C/Games, C/Nogoods, C/P1, P/P5 | 0 | 165 (LogicalStatus, Need, Limit, Problem, Refutation, Formula, Evaluation, Machine, priceReceiver, judge, …) |
| 2 | `Lang/Proofs/Contextual/P5.lean` | 255 | P/NogoodGames | 25 | 8 |
| 3 | `Lang/Contextual/Games.lean` | 36 | C/NogoodGames, P/Games | 0 | 19 |
| 4 | `Lang/Proofs/Contextual/Games.lean` | 114 | P/NogoodGames | 8 | 7 |
| 5 | `Lang/Contextual/NogoodGames.lean` | 58 | P/NogoodGames | 0 | 21 |
| 6 | `Lang/Proofs/Contextual/NogoodGames.lean` | 136 | — | 11 | 0 |
| 7 | `Lang/Contextual/Nogoods.lean` | 76 | P/Nogoods | 0 | 29 |
| 8 | `Lang/Proofs/Contextual/Nogoods.lean` | 105 | — | 9 | 0 |
| 9 | `Lang/Contextual/Material.lean` | 101 | P/Material | 0 | 79 |
| 10 | `Lang/Proofs/Contextual/Material.lean` | 101 | — | 9 | 0 |
| 11 | `Lang/Contextual/P1.lean` | 155 | C/Material | 0 | 87 |
| | **total** | **1,273** | | **62** | |

Imports out of the set (they survive S3): `Lang.Contextual.Protocol` (C/P5), `Lang.Proofs.Contextual.Protocol` (P/P5),
`Lang.Contextual.Closure` (C/NogoodGames, C/P1), `Lang.Contextual.ProvenanceRepairs` and its proof (C/Nogoods,
P/Nogoods; S4 deletes them), `Lang.Proofs.Contextual.Judge` (P/Material). After S3, `Protocol` (R1) loses its
importers C/P5 and P/P5; `ProvenanceRepairs` loses C/Nogoods and P/Nogoods.

Theorem count vs the map's 60: the two extra are the fields of the Prop structure `P5.AlternatingSimulation`
(`inputs`, `outputs`). `gates/size.py`'s count moves 6,288 → 6,228 (−60).

**Reason (map §2.2 D-JUDGE, law 1):** second, third and fourth judges and their status types, beside the closure's
`Contextual.judge`/`Status` and the deployed hole judgment:
- `C/P5` + `P/P5`: `P5.judge` over its own `Problem`/`Refutation`, `LogicalStatus` (witnessed/open/refuted/outside),
  `Formula`/`Evaluation` (suspended negation), `Machine`/`Refines`/`AlternatingSimulation` (its own transition
  systems), `priceReceiver`. Its deliverables include the review's H2 examples: `refuted_ne_outside` (constructor
  no-confusion), `not_unfilled_suspends` and `negation_preserves_suspension` (`simp [evaluate]`).
- `C/Games` + `P/Games`, `C/NogoodGames` + `P/NogoodGames`: game statuses (`OutsideReason`, `checkDraw`, certificates)
  over P5.
- `C/Nogoods` + `P/Nogoods`: `RecordedClosure` and `judgeRecorded`, a second judgment beside `Closure.judge`.
- `C/Material` + `P/Material`, `C/P1`: P1's finite interaction guards and the material guards, each with its own
  `Report`/`Verdict`.
None of their subjects is a deployed object; the only non-P5 object any statement mentions is LANG-67's
`Protocol.Coin` example (`uniform_coin_problem_refuted`), itself under ruling R1.

## 2. `grep` of every deleted name [MEASURED, scope as IMPACT-S1 §2, the 11 files excluded]

- Module names and paths: no hit outside the set (`git grep -E 'Contextual[./](P5|Games|NogoodGames|Nogoods|Material|P1)\b'`
  and `judgeRecorded|RecordedClosure|P5\.(judge|LogicalStatus)` over Lang Kernel Ledger Host Hosting Protocol Census
  Codec Emit Bench Ops gates rows docs CHARTER.md: empty). Bare words `P5 P1 NogoodGames Nogoods Material` in
  surviving Lang/Kernel/Ledger/Host/Census sources: no hit (one `P11a` heading in `P/Worlds`, S5's).
- 477 user declarations, 238 distinct last components: fully qualified names 0 hits; 1,431 dotted relative forms
  0 hits (`fold/S3-grep-suffix.txt`); 93 bare last components occur elsewhere as ordinary words (`fold/S3-grep.txt`),
  none a use (§3).

## 3. Reverse dependencies from the elaborated environment [MEASURED]

0 of the 52,624 constants outside the 11 modules reference any of their 1,028 constants (type, value and shape edges
by `Census.Journal.expressionEdges`/`shapeEdges`).

## 4. Gates tables, lakefile targets, rows fixtures [MEASURED]

No `lakefile.lean` target or root names a deleted module (globs only); the scratch build plans 530 jobs (541 − 11).
No `gates/*.tsv` row, `rows/run` line or golden names a deleted module, path or namespace (the §2 grep includes
`gates` and `rows`). No generated file or wire vector changes.

## 5. Census statement-digest diff and SIZE [MEASURED `fold/diff-S3.txt`, `fold/S3-size-preview.txt`]

```
before 53652 after 52625
vanished 1027 of which outside the declared modules 0
declared-module constants 1028 all vanished: False      (1 re-owned: Iface.mk.congr_simp)
new 0 type-digest changed 0 value-hash changed 0 module changed 1
```
SIZE (generated): Lean modules 529 → 518; proof-modules 285 → 280; Lean lines (Lang) 46,067 → 44,794 (−1,273);
"Lean lines (deployed)" 30,937 → 30,375 (−562: the six def modules, which size.py counts as deployed though no exe
reaches them; map §5.8); theorems 6,288 → 6,228; max dependents 351 → 349; Host closure unchanged (91).

## 6. Note (no ruling needed unless you disagree)

`P/P5` holds the program's only refinement/simulation theory (`Refines`, `refines_refl`/`refines_trans`,
`AlternatingSimulation`, `simulation_preserves_safety`), over P5's own `Machine`, not over `Protocol.Prot` or any
deployed program. If R1 (Ember) keeps the open-protocol calculus as nano's one protocol shape (fork A), a
refinement notion for it would be written over `Prot` then; P5's machine-level one is not that notion [INFERRED from
the statements in the Appendix]. Default: delete with the rest.

## 7. Planned S3 diff and gates

Delete the 11 files (this list is the landing's explicit deletion authorization); append `### LANG-74.3` to
`decisions/lang.md`; SIZE regenerated. Before landing: the 11 paths asserted absent; digest diff re-run against main;
`gates/check.py`; reached build; `scripts/commit` fast path, subject `lang: delete P5, the games, the nogoods, the
material guards and C/P1 (S3 of the consolidation)`.

## Appendix — the 62 deleted theorem statements [MEASURED: `ppExpr` of each elaborated type at a9ab514]

#### `Lang.Contextual.P5` — D-JUDGE

- non-theorem declarations: 23 constructor, 122 definition, 10 inductive, 10 recursor (names in `S3-decls.tsv`)

#### `Lang.Proofs.Contextual.P5` — D-JUDGE

- :8 `Nanodregg.Lang.Contextual.P5.checkRefutation_sound` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {r : Nanodregg.Lang.Contextual.P5.Refutation A}, Nanodregg.Lang.Contextual.P5.checkRefutation p r = true → ∀ (a : A), a ∈ p.domain → p.accepts a = false` — DELETE (D-JUDGE)
- :15 `Nanodregg.Lang.Contextual.P5.witnessed_sound` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {cs : List A} {r : Option (Nanodregg.Lang.Contextual.P5.Refutation A)} {limit : Option Nanodregg.Lang.Contextual.P5.Limit} {a : A}, Nanodregg.Lang.Contextual.P5.judge p cs r limit = Nanodregg.Lang.Contextual.P5.LogicalStatus.witnessed a → a ∈ p.domain ∧ p.accepts a = true` — DELETE (D-JUDGE)
- :29 `Nanodregg.Lang.Contextual.P5.refuted_sound` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {cs : List A} {r : Option (Nanodregg.Lang.Contextual.P5.Refutation A)} {limit : Option Nanodregg.Lang.Contextual.P5.Limit} {e : Nanodregg.Lang.Contextual.P5.Refutation A}, Nanodregg.Lang.Contextual.P5.judge p cs r limit = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted e → ∀ (a : A), a ∈ p.domain → p.accepts a = false` — DELETE (D-JUDGE)
- :45 `Nanodregg.Lang.Contextual.P5.no_certificate_never_refuted` : `∀ {A : Type} [inst : DecidableEq A] (p : Nanodregg.Lang.Contextual.P5.Problem A) (cs : List A) (limit : Option Nanodregg.Lang.Contextual.P5.Limit) (r : Nanodregg.Lang.Contextual.P5.Refutation A), Nanodregg.Lang.Contextual.P5.judge p cs none limit ≠ Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted r` — DELETE (D-JUDGE)
- :52 `Nanodregg.Lang.Contextual.P5.exhausted_is_open` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {cs : List A}, List.find? p.valid cs = none → Nanodregg.Lang.Contextual.P5.judge p cs none = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.searchRemaining []` — DELETE (D-JUDGE)
- :56 `Nanodregg.Lang.Contextual.P5.refuted_ne_outside` : `∀ {W R O L : Type} (r : R) (l : L), Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted r ≠ Nanodregg.Lang.Contextual.P5.LogicalStatus.outsideThisProcedure l` — DELETE (D-JUDGE)
- :61 `Nanodregg.Lang.Contextual.P5.not_unfilled_suspends` : `∀ (env : Nat → Option Bool) (n : Nat), env n = none → Nanodregg.Lang.Contextual.P5.evaluate env (Nanodregg.Lang.Contextual.P5.Formula.atom n).neg = Nanodregg.Lang.Contextual.P5.Evaluation.suspended n []` — DELETE (D-JUDGE)
- :65 `Nanodregg.Lang.Contextual.P5.negation_preserves_suspension` : `∀ {env : Nat → Option Bool} {f : Nanodregg.Lang.Contextual.P5.Formula} {n : Nat} {ns : List Nat}, Nanodregg.Lang.Contextual.P5.evaluate env f = Nanodregg.Lang.Contextual.P5.Evaluation.suspended n ns → Nanodregg.Lang.Contextual.P5.evaluate env f.neg = Nanodregg.Lang.Contextual.P5.Evaluation.suspended n ns` — DELETE (D-JUDGE)
- :74 `Nanodregg.Lang.Contextual.P5.AlternatingSimulation.inputs` : `∀ {SI SS I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {R : SI → SS → Prop}, Nanodregg.Lang.Contextual.P5.AlternatingSimulation impl spec R → ∀ (si : SI) (ss : SS), R si ss → ∀ (i : I) (ss' : SS), spec.receive ss i = some ss' → ∃ si', impl.receive si i = some si' ∧ R si' ss'` — DELETE (D-JUDGE)
- :76 `Nanodregg.Lang.Contextual.P5.AlternatingSimulation.outputs` : `∀ {SI SS I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {R : SI → SS → Prop}, Nanodregg.Lang.Contextual.P5.AlternatingSimulation impl spec R → ∀ (si : SI) (ss : SS), R si ss → ∀ (o : O) (si' : SI), (o, si') ∈ impl.emit si → ∃ ss', (o, ss') ∈ spec.emit ss ∧ R si' ss'` — DELETE (D-JUDGE)
- :83 `Nanodregg.Lang.Contextual.P5.refines_refl` : `∀ {S I O : Type} (m : Nanodregg.Lang.Contextual.P5.Machine S I O) (s : S), Nanodregg.Lang.Contextual.P5.Refines m s m s` — DELETE (D-JUDGE)
- :91 `Nanodregg.Lang.Contextual.P5.refines_trans` : `∀ {S1 S2 S3 I O : Type} {a : Nanodregg.Lang.Contextual.P5.Machine S1 I O} {b : Nanodregg.Lang.Contextual.P5.Machine S2 I O} {c : Nanodregg.Lang.Contextual.P5.Machine S3 I O} {s1 : S1} {s2 : S2} {s3 : S3}, Nanodregg.Lang.Contextual.P5.Refines a s1 b s2 → Nanodregg.Lang.Contextual.P5.Refines b s2 c s3 → Nanodregg.Lang.Contextual.P5.Refines a s1 c s3` — DELETE (D-JUDGE)
- :107 `Nanodregg.Lang.Contextual.P5.simulation_receives` : `∀ {SI SS I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {R : SI → SS → Prop}, Nanodregg.Lang.Contextual.P5.AlternatingSimulation impl spec R → ∀ (is : List I) {si : SI} {ss ss' : SS}, R si ss → Nanodregg.Lang.Contextual.P5.receiveAll spec ss is = some ss' → ∃ si', Nanodregg.Lang.Contextual.P5.receiveAll impl si is = some si' ∧ R si' ss'` — DELETE (D-JUDGE)
- :125 `Nanodregg.Lang.Contextual.P5.narrowing_breaks_peer` : `∀ {SI SS I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {si : SI} {ss ss' : SS} {i : I}, spec.receive ss i = some ss' → impl.receive si i = none → ¬Nanodregg.Lang.Contextual.P5.Refines impl si spec ss` — DELETE (D-JUDGE)
- :140 `Nanodregg.Lang.Contextual.P5.polarized_matching` : `∀ {SI SS I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {R : SI → SS → Prop}, Nanodregg.Lang.Contextual.P5.AlternatingSimulation impl spec R → ∀ {si : SI} {ss : SS}, R si ss → (∀ (a : Nanodregg.Lang.Contextual.P5.Action I O), a.owner = Nanodregg.Lang.Contextual.Protocol.Polarity.theirs → ∀ (ss' : SS), Nanodregg.Lang.Contextual.P5.Moves spec ss a ss' → ∃ si', Nanodregg.Lang.Contextual.P5.Moves impl si a si' ∧ R si' ss') ∧ ∀ (a : Nanodregg.Lang.Contextual.P5.Action I O), a.owner = Nanodregg.Lang.Contextual.Protocol.Polarity.ours → ∀ (si' : SI), Nanodregg.Lang.Contextual.P5.Moves impl si a si' → ∃ ss', Nanodregg.Lang.Contextual.P5.Moves spec ss a ss' ∧ R si' ss'` — DELETE (D-JUDGE)
- :170 `Nanodregg.Lang.Contextual.P5.simulation_preserves_safety` : `∀ {SI SS P I O : Type} {impl : Nanodregg.Lang.Contextual.P5.Machine SI I O} {spec : Nanodregg.Lang.Contextual.P5.Machine SS I O} {R : SI → SS → Prop}, Nanodregg.Lang.Contextual.P5.AlternatingSimulation impl spec R → ∀ (peer : Nanodregg.Lang.Contextual.P5.Machine P O I) (n : Nat) {si : SI} {ss : SS} {p : P}, R si ss → Nanodregg.Lang.Contextual.P5.SafeFor spec peer n ss p → Nanodregg.Lang.Contextual.P5.SafeFor impl peer n si p` — DELETE (D-JUDGE)
- :190 `Nanodregg.Lang.Contextual.P5.price_refines` : `∀ {small large : Nat}, small ≤ large → ∀ {outs outs' : List Bool}, (∀ (b : Bool), b ∈ outs' → b ∈ outs) → ∀ (s : Bool), Nanodregg.Lang.Contextual.P5.Refines (Nanodregg.Lang.Contextual.P5.priceReceiver large outs') s (Nanodregg.Lang.Contextual.P5.priceReceiver small outs) s` — DELETE (D-JUDGE)
- :215 `Nanodregg.Lang.Contextual.P5.price_seven_breaks` : `Nanodregg.Lang.Contextual.P5.receiveAll (Nanodregg.Lang.Contextual.P5.priceReceiver 10 [true, false]) false [7] = some true ∧ Nanodregg.Lang.Contextual.P5.receiveAll (Nanodregg.Lang.Contextual.P5.priceReceiver 5 [true]) false [7] = none` — DELETE (D-JUDGE)
- :219 `Nanodregg.Lang.Contextual.P5.price_seven_not_refinement` : `¬Nanodregg.Lang.Contextual.P5.Refines (Nanodregg.Lang.Contextual.P5.priceReceiver 5 [true]) false (Nanodregg.Lang.Contextual.P5.priceReceiver 10 [true, false]) false` — DELETE (D-JUDGE)
- :223 `Nanodregg.Lang.Contextual.P5.price_reply_expansion_not_refinement` : `¬Nanodregg.Lang.Contextual.P5.Refines (Nanodregg.Lang.Contextual.P5.priceReceiver 10 [true, false]) true (Nanodregg.Lang.Contextual.P5.priceReceiver 10 [true]) true` — DELETE (D-JUDGE)
- :229 `Nanodregg.Lang.Contextual.P5.four_status_session` : `Nanodregg.Lang.Contextual.P5.runSession Nanodregg.Lang.Contextual.P5.statusSession = [Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.searchRemaining [], Nanodregg.Lang.Contextual.P5.LogicalStatus.witnessed 1, Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted { excluded := [0, 1] }, Nanodregg.Lang.Contextual.P5.LogicalStatus.outsideThisProcedure Nanodregg.Lang.Contextual.P5.Limit.unsupportedFragment]` — DELETE (D-JUDGE)
- :235 `Nanodregg.Lang.Contextual.P5.incomplete_certificate_refused` : `Nanodregg.Lang.Contextual.P5.judge { domain := [0, 1], accepts := fun n => n == 1 } [0] (some { excluded := [0] }) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)
- :239 `Nanodregg.Lang.Contextual.P5.positive_candidate_refutes_certificate` : `Nanodregg.Lang.Contextual.P5.judge { domain := [0, 1], accepts := fun n => n == 1 } [] (some { excluded := [0, 1] }) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)
- :243 `Nanodregg.Lang.Contextual.P5.out_of_domain_witness_refused` : `Nanodregg.Lang.Contextual.P5.judge { domain := [0], accepts := fun x => true } [1] none = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.searchRemaining []` — DELETE (D-JUDGE)
- :247 `Nanodregg.Lang.Contextual.P5.uniform_coin_problem_refuted` : `Nanodregg.Lang.Contextual.P5.judge { domain := [false, true], accepts := fun c => Nanodregg.Lang.Contextual.Protocol.Coin.wins false (Nanodregg.Lang.Contextual.Protocol.subst (Nanodregg.Lang.Contextual.Protocol.Coin.answer c) Nanodregg.Lang.Contextual.Protocol.Coin.planHole) () && Nanodregg.Lang.Contextual.Protocol.Coin.wins true (Nanodregg.Lang.Contextual.Protocol.subst (Nanodregg.Lang.Contextual.Protocol.Coin.answer c) Nanodregg.Lang.Contextual.Protocol.Coin.planHole) () } [false, true] (some { excluded := [false, true] }) = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted { excluded := [false, true] }` — DELETE (D-JUDGE)
- non-theorem declarations: 1 constructor, 5 definition, 1 inductive, 1 recursor (names in `S3-decls.tsv`)

#### `Lang.Contextual.Games` — D-JUDGE

- non-theorem declarations: 2 constructor, 15 definition, 1 inductive, 1 recursor (names in `S3-decls.tsv`)

#### `Lang.Proofs.Contextual.Games` — D-JUDGE

- :22 `Nanodregg.Lang.Contextual.P5.Games.solved_exclusive` : `∀ {V : Type} {moves : V → List V} {b : Bool} {x : V}, Nanodregg.Lang.Contextual.P5.Games.Solved moves b x → ¬Nanodregg.Lang.Contextual.P5.Games.Solved moves (!b) x` — DELETE (D-JUDGE)
- :36 `Nanodregg.Lang.Contextual.P5.Games.trap_unsolved` : `∀ {V : Type} {moves : V → List V} {region : List V}, (∀ (x : V), x ∈ region → ∃ y, y ∈ moves x) → (∀ (x : V), x ∈ region → ∀ (y : V), y ∈ moves x → y ∈ region) → ∀ {b : Bool} {x : V}, x ∈ region → ¬Nanodregg.Lang.Contextual.P5.Games.Solved moves b x` — DELETE (D-JUDGE)
- :49 `Nanodregg.Lang.Contextual.P5.Games.checkDraw_sound` : `∀ {moves : Nat → List Nat} {root : Nat} {region : List Nat}, Nanodregg.Lang.Contextual.P5.Games.checkDraw moves root region = true → Nanodregg.Lang.Contextual.P5.Games.Draw moves root` — DELETE (D-JUDGE)
- :67 `Nanodregg.Lang.Contextual.P5.Games.outside_draw_sound` : `∀ {moves : Nat → List Nat} {root : Nat} {region reported : List Nat}, Nanodregg.Lang.Contextual.P5.Games.judgeDraw moves root region = Nanodregg.Lang.Contextual.P5.LogicalStatus.outsideThisProcedure (Nanodregg.Lang.Contextual.P5.Games.OutsideReason.drawn reported) → reported = region ∧ Nanodregg.Lang.Contextual.P5.Games.checkDraw moves root region = true ∧ Nanodregg.Lang.Contextual.P5.Games.Draw moves root` — DELETE (D-JUDGE)
- :80 `Nanodregg.Lang.Contextual.P5.Games.loop_is_draw` : `Nanodregg.Lang.Contextual.P5.Games.judgeDraw Nanodregg.Lang.Contextual.P5.Games.loopMoves 0 [0] = Nanodregg.Lang.Contextual.P5.LogicalStatus.outsideThisProcedure (Nanodregg.Lang.Contextual.P5.Games.OutsideReason.drawn [0]) ∧ Nanodregg.Lang.Contextual.P5.Games.Draw Nanodregg.Lang.Contextual.P5.Games.loopMoves 0` — DELETE (D-JUDGE)
- :86 `Nanodregg.Lang.Contextual.P5.Games.sink_is_not_draw` : `Nanodregg.Lang.Contextual.P5.Games.judgeDraw (fun x => []) 0 [0] = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation [] ∧ Nanodregg.Lang.Contextual.P5.Games.Solved (fun x => []) false 0` — DELETE (D-JUDGE)
- :94 `Nanodregg.Lang.Contextual.P5.Games.escape_is_not_draw` : `Nanodregg.Lang.Contextual.P5.Games.judgeDraw (fun x => if x = 0 then [0, 1] else []) 0 [0] = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation [] ∧ Nanodregg.Lang.Contextual.P5.Games.Solved (fun x => if x = 0 then [0, 1] else []) true 0` — DELETE (D-JUDGE)
- :104 `Nanodregg.Lang.Contextual.P5.Games.unrelated_loop_is_not_draw` : `Nanodregg.Lang.Contextual.P5.Games.judgeDraw (fun x => if x = 1 then [1] else []) 0 [1] = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation [] ∧ Nanodregg.Lang.Contextual.P5.Games.Solved (fun x => if x = 1 then [1] else []) false 0` — DELETE (D-JUDGE)
- non-theorem declarations: 2 constructor, 3 definition, 1 inductive, 1 recursor (names in `S3-decls.tsv`)

#### `Lang.Contextual.NogoodGames` — D-JUDGE

- non-theorem declarations: 3 constructor, 16 definition, 1 inductive, 1 recursor (names in `S3-decls.tsv`)

#### `Lang.Proofs.Contextual.NogoodGames` — D-JUDGE

- :12 `Nanodregg.Lang.Contextual.P5.NogoodGames.accepted_wins` : `∀ {A : Type} {p : Nanodregg.Lang.Contextual.P5.Problem A} {a : A}, a ∈ p.domain → p.accepts a = true → Nanodregg.Lang.Contextual.P5.Games.Solved (Nanodregg.Lang.Contextual.P5.NogoodGames.moves p) true Nanodregg.Lang.Contextual.P5.NogoodGames.Position.question` — DELETE (D-JUDGE)
- :22 `Nanodregg.Lang.Contextual.P5.NogoodGames.excluded_loses` : `∀ {A : Type} {p : Nanodregg.Lang.Contextual.P5.Problem A}, (∀ (a : A), a ∈ p.domain → p.accepts a = false) → Nanodregg.Lang.Contextual.P5.Games.Solved (Nanodregg.Lang.Contextual.P5.NogoodGames.moves p) false Nanodregg.Lang.Contextual.P5.NogoodGames.Position.question` — DELETE (D-JUDGE)
- :35 `Nanodregg.Lang.Contextual.P5.NogoodGames.checkCertificate_sound` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {supports : A → List Nanodregg.Lang.Contextual.Token} {nogoods : List (List Nanodregg.Lang.Contextual.Token)} {c : Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A}, Nanodregg.Lang.Contextual.P5.NogoodGames.checkCertificate p supports nogoods c = true → ∀ (a : A), a ∈ p.domain → ∃ n, (a, n) ∈ c ∧ n ∈ nogoods ∧ (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ n → t ∈ supports a) ∧ p.accepts a = false` — DELETE (D-JUDGE)
- :51 `Nanodregg.Lang.Contextual.P5.NogoodGames.refuted_recorded` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {retained : List A} {supports : A → List Nanodregg.Lang.Contextual.Token} {nogoods : List (List Nanodregg.Lang.Contextual.Token)} {certificate : Option (Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A)} {limit : Option Nanodregg.Lang.Contextual.P5.Limit} {c : Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A}, Nanodregg.Lang.Contextual.P5.NogoodGames.judge p retained supports nogoods certificate limit = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted c → certificate = some c ∧ ∀ (a : A), a ∈ p.domain → ∃ n, (a, n) ∈ c ∧ n ∈ nogoods ∧ (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ n → t ∈ supports a) ∧ p.accepts a = false` — DELETE (D-JUDGE)
- :71 `Nanodregg.Lang.Contextual.P5.NogoodGames.refuted_is_lost` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {retained : List A} {supports : A → List Nanodregg.Lang.Contextual.Token} {nogoods : List (List Nanodregg.Lang.Contextual.Token)} {certificate : Option (Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A)} {limit : Option Nanodregg.Lang.Contextual.P5.Limit} {c : Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A}, Nanodregg.Lang.Contextual.P5.NogoodGames.judge p retained supports nogoods certificate limit = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted c → Nanodregg.Lang.Contextual.P5.Games.Solved (Nanodregg.Lang.Contextual.P5.NogoodGames.moves p) false Nanodregg.Lang.Contextual.P5.NogoodGames.Position.question ∧ ∀ (a : A), a ∈ p.domain → ∃ n, n ∈ nogoods ∧ (a, n) ∈ c ∧ ∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ n → t ∈ supports a` — DELETE (D-JUDGE)
- :90 `Nanodregg.Lang.Contextual.P5.NogoodGames.witnessed_is_won` : `∀ {A : Type} [inst : DecidableEq A] {p : Nanodregg.Lang.Contextual.P5.Problem A} {retained : List A} {supports : A → List Nanodregg.Lang.Contextual.Token} {nogoods : List (List Nanodregg.Lang.Contextual.Token)} {certificate : Option (Nanodregg.Lang.Contextual.P5.NogoodGames.Certificate A)} {limit : Option Nanodregg.Lang.Contextual.P5.Limit} {a : A}, Nanodregg.Lang.Contextual.P5.NogoodGames.judge p retained supports nogoods certificate limit = Nanodregg.Lang.Contextual.P5.LogicalStatus.witnessed a → a ∈ p.domain ∧ p.accepts a = true ∧ Nanodregg.Lang.Contextual.P5.Games.Solved (Nanodregg.Lang.Contextual.P5.NogoodGames.moves p) true Nanodregg.Lang.Contextual.P5.NogoodGames.Position.question` — DELETE (D-JUDGE)
- :108 `Nanodregg.Lang.Contextual.P5.NogoodGames.recorded_loss_example` : `Nanodregg.Lang.Contextual.P5.NogoodGames.judge { domain := [0], accepts := fun x => false } [] (fun x => [{ id := 1, ver := 0 }]) [[{ id := 1, ver := 0 }]] (some [(0, [{ id := 1, ver := 0 }])]) = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted [(0, [{ id := 1, ver := 0 }])]` — DELETE (D-JUDGE)
- :114 `Nanodregg.Lang.Contextual.P5.NogoodGames.unrecorded_refused` : `Nanodregg.Lang.Contextual.P5.NogoodGames.judge { domain := [0], accepts := fun x => false } [] (fun x => [{ id := 1, ver := 0 }]) [] (some [(0, [{ id := 1, ver := 0 }])]) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)
- :119 `Nanodregg.Lang.Contextual.P5.NogoodGames.unrelated_record_refused` : `Nanodregg.Lang.Contextual.P5.NogoodGames.judge { domain := [0], accepts := fun x => false } [] (fun x => [{ id := 2, ver := 0 }]) [[{ id := 1, ver := 0 }]] (some [(0, [{ id := 1, ver := 0 }])]) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)
- :125 `Nanodregg.Lang.Contextual.P5.NogoodGames.uncovered_candidate_refused` : `Nanodregg.Lang.Contextual.P5.NogoodGames.judge { domain := [0, 1], accepts := fun x => false } [] (fun x => [{ id := 1, ver := 0 }]) [[{ id := 1, ver := 0 }]] (some [(0, [{ id := 1, ver := 0 }])]) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)
- :130 `Nanodregg.Lang.Contextual.P5.NogoodGames.stale_record_refused` : `Nanodregg.Lang.Contextual.P5.NogoodGames.judge { domain := [0], accepts := fun x => true } [] (fun x => [{ id := 1, ver := 0 }]) [[{ id := 1, ver := 0 }]] (some [(0, [{ id := 1, ver := 0 }])]) = Nanodregg.Lang.Contextual.P5.LogicalStatus.open Nanodregg.Lang.Contextual.P5.Need.invalidRefutation []` — DELETE (D-JUDGE)

#### `Lang.Contextual.Nogoods` — D-JUDGE

- non-theorem declarations: 2 constructor, 23 definition, 2 inductive, 2 recursor (names in `S3-decls.tsv`)

#### `Lang.Proofs.Contextual.Nogoods` — D-JUDGE

- :9 `Nanodregg.Lang.Contextual.P9.findNogood_sound` : `∀ {ngs : List (List Nanodregg.Lang.Contextual.Token)} {supports ng : List Nanodregg.Lang.Contextual.Token}, Nanodregg.Lang.Contextual.P9.findNogood ngs supports = some ng → ng ∈ ngs ∧ ∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ supports` — DELETE (D-JUDGE)
- :16 `Nanodregg.Lang.Contextual.P9.findNogood_complete` : `∀ {ngs : List (List Nanodregg.Lang.Contextual.Token)} {supports ng : List Nanodregg.Lang.Contextual.Token}, ng ∈ ngs → (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ supports) → ∃ core, Nanodregg.Lang.Contextual.P9.findNogood ngs supports = some core` — DELETE (D-JUDGE)
- :29 `Nanodregg.Lang.Contextual.P9.judge_respects_nogoods` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D} {ng : List Nanodregg.Lang.Contextual.Token}, ng ∈ cl.nogoods → (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ Nanodregg.Lang.Contextual.effSupports I c) → ∃ core, Nanodregg.Lang.Contextual.P9.judgeRecorded cl I w c = { status := Nanodregg.Lang.Contextual.Status.conflict Nanodregg.Lang.Contextual.Evidence.guardFails, nogood := some core } ∧ core ∈ cl.nogoods ∧ ∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ core → t ∈ Nanodregg.Lang.Contextual.effSupports I c` — DELETE (D-JUDGE)
- :39 `Nanodregg.Lang.Contextual.P9.nogood_never_suspended` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D} {ng : List Nanodregg.Lang.Contextual.Token}, ng ∈ cl.nogoods → (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ Nanodregg.Lang.Contextual.effSupports I c) → ∀ (missing : List Nanodregg.Lang.Contextual.Token), (Nanodregg.Lang.Contextual.P9.judgeRecorded cl I w c).status ≠ Nanodregg.Lang.Contextual.Status.suspended missing` — DELETE (D-JUDGE)
- :47 `Nanodregg.Lang.Contextual.P9.judgeRecorded_verified` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D}, (Nanodregg.Lang.Contextual.P9.judgeRecorded cl I w c).status = Nanodregg.Lang.Contextual.Status.verified ↔ Nanodregg.Lang.Contextual.P9.findNogood cl.nogoods (Nanodregg.Lang.Contextual.effSupports I c) = none ∧ Nanodregg.Lang.Contextual.judge I w c = Nanodregg.Lang.Contextual.Status.verified` — DELETE (D-JUDGE)
- :54 `Nanodregg.Lang.Contextual.P9.recordedLabel_iff` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {cs : List (Nanodregg.Lang.Contextual.Candidate D)}, (∃ c, c ∈ cs ∧ (Nanodregg.Lang.Contextual.P9.judgeRecorded cl I w c).status = Nanodregg.Lang.Contextual.Status.verified) ↔ ∃ m, m ∈ Nanodregg.Lang.Contextual.P9.recordedLabel cl I cs ∧ Nanodregg.Lang.Contextual.P9.Monomial.eval I w m = true` — DELETE (D-JUDGE)
- :67 `Nanodregg.Lang.Contextual.P9.recordedRepairs_sound` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {cs : List (Nanodregg.Lang.Contextual.Candidate D)} {ts : List Nanodregg.Lang.Contextual.Token}, ts ∈ Nanodregg.Lang.Contextual.P9.recordedRepairPlans cl I w cs → ∃ c, c ∈ cs ∧ (Nanodregg.Lang.Contextual.P9.judgeRecorded cl I (Nanodregg.Lang.Contextual.applyAll (Nanodregg.Lang.Contextual.P9.tokenEdits w ts) w) c).status = Nanodregg.Lang.Contextual.Status.verified` — DELETE (D-JUDGE)
- :76 `Nanodregg.Lang.Contextual.P9.recorded_refuted` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D} {ng : List Nanodregg.Lang.Contextual.Token}, Nanodregg.Lang.Contextual.P9.classifyRecorded cl I w c = Nanodregg.Lang.Contextual.P5.LogicalStatus.refuted ng → ng ∈ cl.nogoods ∧ (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ Nanodregg.Lang.Contextual.effSupports I c) ∧ ∀ (v : Nanodregg.Lang.Contextual.World E), (Nanodregg.Lang.Contextual.P9.judgeRecorded cl I v c).status ≠ Nanodregg.Lang.Contextual.Status.verified` — DELETE (D-JUDGE)
- :95 `Nanodregg.Lang.Contextual.P9.select_respects_nogoods` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E : Type} {cl : Nanodregg.Lang.Contextual.P9.RecordedClosure D E} {I : Nanodregg.Lang.Contextual.Iface D E} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D} {u i : Nat} {ng : List Nanodregg.Lang.Contextual.Token}, cl.find u = some I → (cl.slot u).cands[i]? = some c → ng ∈ cl.nogoods → (∀ (t : Nanodregg.Lang.Contextual.Token), t ∈ ng → t ∈ Nanodregg.Lang.Contextual.effSupports I c) → ∀ (p : Nanodregg.Lang.Contextual.Party), Nanodregg.Lang.Contextual.P9.selectRecorded cl w p u i = Except.error (Nanodregg.Lang.Contextual.Refusal.notVerified (Nanodregg.Lang.Contextual.Status.conflict Nanodregg.Lang.Contextual.Evidence.guardFails))` — DELETE (D-JUDGE)

#### `Lang.Contextual.Material` — D-JUDGE

- non-theorem declarations: 11 constructor, 58 definition, 5 inductive, 5 recursor (names in `S3-decls.tsv`)

#### `Lang.Proofs.Contextual.Material` — D-JUDGE

- :6 `Nanodregg.Lang.Contextual.Material.material_mem` : `∀ {A : Type} {tests : List (Nanodregg.Lang.Contextual.Material.Test A)} {c : Nanodregg.Lang.Contextual.Material.Filling A} {cell : List Bool × Nanodregg.Lang.Contextual.Material.Stop A}, cell ∈ Nanodregg.Lang.Contextual.Material.material tests c ↔ ∃ t, t ∈ tests ∧ Nanodregg.Lang.Contextual.Material.visit c t.path = cell` — DELETE (D-JUDGE)
- :13 `Nanodregg.Lang.Contextual.Material.verified_scope` : `∀ {A : Type} {tests : List (Nanodregg.Lang.Contextual.Material.Test A)} {c : Nanodregg.Lang.Contextual.Material.Filling A} {r : Nanodregg.Lang.Contextual.Material.Receipt A}, Nanodregg.Lang.Contextual.Material.inspect tests c = Nanodregg.Lang.Contextual.Material.Verdict.verified r → r.against = tests ∧ r.fragment = Nanodregg.Lang.Contextual.Material.material tests c ∧ ∀ (t : Nanodregg.Lang.Contextual.Material.Test A), t ∈ tests → Nanodregg.Lang.Contextual.Material.complete t c = true` — DELETE (D-JUDGE)
- :29 `Nanodregg.Lang.Contextual.Material.visited_gaveUp_partial` : `∀ {A : Type} {tests : List (Nanodregg.Lang.Contextual.Material.Test A)} {c : Nanodregg.Lang.Contextual.Material.Filling A} {t : Nanodregg.Lang.Contextual.Material.Test A}, t ∈ tests → (Nanodregg.Lang.Contextual.Material.visit c t.path).snd = Nanodregg.Lang.Contextual.Material.Stop.gaveUp → Nanodregg.Lang.Contextual.Material.inspect tests c = Nanodregg.Lang.Contextual.Material.Verdict.incomplete` — DELETE (D-JUDGE)
- :41 `Nanodregg.Lang.Contextual.Material.visited_gaveUp_never_verified` : `∀ {A : Type} {tests : List (Nanodregg.Lang.Contextual.Material.Test A)} {c : Nanodregg.Lang.Contextual.Material.Filling A} {t : Nanodregg.Lang.Contextual.Material.Test A}, t ∈ tests → (Nanodregg.Lang.Contextual.Material.visit c t.path).snd = Nanodregg.Lang.Contextual.Material.Stop.gaveUp → ∀ (r : Nanodregg.Lang.Contextual.Material.Receipt A), Nanodregg.Lang.Contextual.Material.inspect tests c ≠ Nanodregg.Lang.Contextual.Material.Verdict.verified r` — DELETE (D-JUDGE)
- :50 `Nanodregg.Lang.Contextual.Material.material_mono` : `∀ {A : Type} {s t : List (Nanodregg.Lang.Contextual.Material.Test A)}, (∀ (x : Nanodregg.Lang.Contextual.Material.Test A), x ∈ s → x ∈ t) → ∀ (c : Nanodregg.Lang.Contextual.Material.Filling A) (cell : List Bool × Nanodregg.Lang.Contextual.Material.Stop A), cell ∈ Nanodregg.Lang.Contextual.Material.material s c → cell ∈ Nanodregg.Lang.Contextual.Material.material t c` — DELETE (D-JUDGE)
- :58 `Nanodregg.Lang.Contextual.Material.required_exposes_giveUp` : `Nanodregg.Lang.Contextual.Material.material [Nanodregg.Lang.Contextual.Material.left] Nanodregg.Lang.Contextual.Material.sample = [([false], Nanodregg.Lang.Contextual.Material.Stop.answer 7)] ∧ Nanodregg.Lang.Contextual.Material.inspect [Nanodregg.Lang.Contextual.Material.left] Nanodregg.Lang.Contextual.Material.sample = Nanodregg.Lang.Contextual.Material.Verdict.verified { against := [Nanodregg.Lang.Contextual.Material.left], fragment := [([false], Nanodregg.Lang.Contextual.Material.Stop.answer 7)] } ∧ Nanodregg.Lang.Contextual.Material.inspect [Nanodregg.Lang.Contextual.Material.left, Nanodregg.Lang.Contextual.Material.right] Nanodregg.Lang.Contextual.Material.sample = Nanodregg.Lang.Contextual.Material.Verdict.incomplete` — DELETE (D-JUDGE)
- :66 `Nanodregg.Lang.Contextual.Material.bad_answer_rejected` : `Nanodregg.Lang.Contextual.Material.inspect [Nanodregg.Lang.Contextual.Material.left] ((Nanodregg.Lang.Contextual.Material.Filling.answer 8).fork Nanodregg.Lang.Contextual.Material.Filling.gaveUp) = Nanodregg.Lang.Contextual.Material.Verdict.rejected` — DELETE (D-JUDGE)
- :72 `Nanodregg.Lang.Contextual.Material.candidate_verified` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E A : Type} {I : Nanodregg.Lang.Contextual.Iface D E} {tests : E → List (Nanodregg.Lang.Contextual.Material.Test A)} {project : E → D.Tm → Nanodregg.Lang.Contextual.Material.Filling A} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D}, (Nanodregg.Lang.Contextual.Material.inspectCandidate I tests project w c).fst = Nanodregg.Lang.Contextual.Status.verified → Nanodregg.Lang.Contextual.judge I w c = Nanodregg.Lang.Contextual.Status.verified ∧ (Nanodregg.Lang.Contextual.Material.inspectCandidate I tests project w c).snd.against = tests w.env ∧ (Nanodregg.Lang.Contextual.Material.inspectCandidate I tests project w c).snd.fragment = Nanodregg.Lang.Contextual.Material.material (tests w.env) (project w.env c.filling) ∧ ∀ (t : Nanodregg.Lang.Contextual.Material.Test A), t ∈ tests w.env → Nanodregg.Lang.Contextual.Material.complete t (project w.env c.filling) = true` — DELETE (D-JUDGE)
- :90 `Nanodregg.Lang.Contextual.Material.candidate_gaveUp_refused` : `∀ {D : Nanodregg.Lang.Contextual.CalculusData} {E A : Type} {I : Nanodregg.Lang.Contextual.Iface D E} {tests : E → List (Nanodregg.Lang.Contextual.Material.Test A)} {project : E → D.Tm → Nanodregg.Lang.Contextual.Material.Filling A} {w : Nanodregg.Lang.Contextual.World E} {c : Nanodregg.Lang.Contextual.Candidate D} {t : Nanodregg.Lang.Contextual.Material.Test A}, t ∈ tests w.env → (Nanodregg.Lang.Contextual.Material.visit (project w.env c.filling) t.path).snd = Nanodregg.Lang.Contextual.Material.Stop.gaveUp → (Nanodregg.Lang.Contextual.Material.inspectCandidate I tests project w c).fst ≠ Nanodregg.Lang.Contextual.Status.verified` — DELETE (D-JUDGE)

#### `Lang.Contextual.P1` — D-JUDGE

- non-theorem declarations: 10 constructor, 67 definition, 5 inductive, 5 recursor (names in `S3-decls.tsv`)
