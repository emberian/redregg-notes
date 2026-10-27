VERDICT: RELEASE S10

Choice (a): delete `specialize`, `specialize_eq`, and `provenance_update`. The kept polynomial is P9's. The tooth names the twin, not the one being kept. `tm_decEq_toy` drops a reflexive conjunct and does not claim less. The 20 other type-digest hits are binder order, no premise gained. Nothing outside this step's files moves.

Base `origin/main` = `ac345215f386e83287b6736f06d327ee9bdc8214` (fetched). S10's patch is against the S9 candidate; the provenance files' before-side matches `ac34521` (S9 did not edit them). No build. Census names are `fold/diff-S10.txt`; the type strings behind those names were not re-printed here.

## (1) `tm_decEq_toy`

The dropped conjunct is vacuous. The new statement says the same, not less.

[READ `ac34521:Lang/Proofs/Contextual/Core.lean:885–889`, and the patch hunk, and `fold/S10-s10edit.py`]

Old:

```
theorem tm_decEq_toy :
    (Tm.letbox (.box [.base] (.var 0)) (.mvar 0 [.var 0]) ≠
      .letbox (.box [.base] (.var 0)) (.mvar 0 [.var 1])) ∧
    Tm.mvar 3 [.lam .base (.var 0)] = Tm.mvar 3 [.lam .base (.var 0)] := by decide
```

New:

```
theorem tm_decEq_toy :
    Tm.letbox (.box [.base] (.var 0)) (.mvar 0 [.var 0]) ≠
      .letbox (.box [.base] (.var 0)) (.mvar 0 [.var 1]) := by decide
```

The inequality is copied character for character. The conjunct that leaves is `Tm.mvar 3 [.lam .base (.var 0)] = Tm.mvar 3 [.lam .base (.var 0)]`. [READ `Lang/Contextual/Core.lean:68`] `mvar` is `| mvar (u : Nat) (σ : List Tm)`, both fields explicit, so the two sides are the same constructor application. That is `Eq.refl`. No hypothesis, no `DecidableEq`, no fact about the calculus. `P ∧ (x = x)` is the same proposition as `P`.

[MEASURED `git grep tm_decEq_toy ac34521`] one hit, the declaration. Nothing projects the conjunction. [MEASURED `diff-S10.txt`] it is the only TYPE line whose name is not a provenance constant, and it is also in VALUE, which is the proof still being `decide` on a smaller goal. Map §2.2 named this conjunct as the one to drop.

## (2) The twin

The tooth refuted the definition S10 deletes. Not a STOP.

[READ `ac34521:Lang/Proofs/Contextual/ProvenanceTeeth.lean` whole]

```
theorem provenance_env_specialized :
    Nanodregg.Lang.Contextual.provenance toothIface toothWorld.env [toothCandidate] = [] ∧
    judge toothIface ((Edit.setEnv true).apply toothWorld) toothCandidate = .verified := by
  decide
```

That application is three arguments after the name: iface, env, candidate list. That is the def in `Closure.lean`, return type `List (List Token × List Token)`, the one that filters on `D.check && I.guard env && cost ≤ budget`. [READ `Closure.lean:234–239`] The kept def is P9's, two arguments, no env, return type `List (Monomial D)`, filter `D.check` only. [READ `Provenance.lean:42–43` and the patch's inserted `def provenance`] The tooth's statement does not type-check against the kept def. Its `= []` is the property the kept def does not have: the guard stays a literal.

The witness is aimed at the filter. [READ the three private defs] `toothIface`'s guard is `fun env _ => env`, `toothWorld.env` is `false`, budget `10`, candidate cost `1`. At env `false` the three-argument filter drops the candidate. `Edit.setEnv true` is what the second conjunct says makes `judge` return `.verified`. I did not re-run `decide`. The statement names the deleted def either way.

Who read the deleted def. [MEASURED `git grep` of `provenance`, `Contextual.provenance`, `specialize`, `Monomial.holds`, `import Lang.Contextual.Provenance` over `ac34521`] Lean hits are only:

- `Closure.lean` — the three-argument def (and a docstring "provenance `ab + c`", not a use)
- `Judge.lean:112–122` — `provenance_iff` with `Monomial.holds`, deleted in this patch
- `P/Provenance.lean:33,40,46` — `specialize_eq` and `provenance_update`, deleted in this patch
- `ProvenanceTeeth.lean:16` — the tooth
- `ClosureStatements.lean:43` — `Monomial.holds`, deleted in this patch
- `C/Provenance.lean` — P9, which is the kept side, including `specialize`'s own def

`import Lang.Contextual.Provenance` is `P/Provenance.lean:2` only. Nothing imports `ProvenanceTeeth`. [MEASURED the same grep on `HoleBridge.lean`, `StdHoleModel.lean`, `StdHole.lean`, `StdContextualHole.lean`, `LiveHoles.lean`, `Journey.lean`, `Journey/Contextual.lean`, `Journey/ContextualChecks.lean`] no `provenance`. `HoleBridge` imports `Lang.Contextual.LangInstance`. `StdHoleModel` imports `Lang.Contextual.Trace`. The journey file does not contain the string.

P8's rows do not read either polynomial anymore. [READ `ac34521:decisions/lang.md` at the S2 entry] the four changes already landed: the "trace rejudged" half is gone; "live provenance" (`P9.provenance` over the toy — the kept one, not the twin) became "live authority" off the kernel view; the re-pinned tombstone row was deleted; the mismatched pin is the real commit refused by the live provider. S10's patch has no journey hunk.

`Rule` / `lfpIter` / `supportCount` / `countRun` are already absent at `ac34521`. [MEASURED `git grep` empty] S5 took them. S10 does not touch that deletion, and does not owe it.

The name `Contextual.provenance` changes meaning: the three-argument list leaves, P9's two-argument polynomial takes the name. [READ `fold/S10-twin-rows.txt`] the census drops the five colliding twin rows (`provenance`, `provenance.eq_1`, `provenance_iff`, `_simp_1_2`, `_simp_1_3`, modules Closure and Judge) before the diff, so the TYPE line for `provenance` is P9 against the moved P9, not the twin against P9. The twin is a deletion, accounted in that file, not a silent rewrite of a token multiset. No outside constant's type or value mentions it. [MEASURED `diff-S10.txt`: vanished 10, undeclared 0, new 0]

## (3) Choice (a)

Delete them. They are the bridge to the twin, not a fact about the kept polynomial that would otherwise go unstated.

[READ `ac34521:P/Provenance.lean:29–48`]

```
theorem specialize_eq (I : Iface D E) (env : E) (cs : List (Candidate D)) :
    specialize I env (provenance I cs) =
      Nanodregg.Lang.Contextual.provenance I env cs

theorem provenance_update … :
    Nanodregg.Lang.Contextual.provenance I (e.apply w).env cs =
      specialize I (e.apply w).env (provenance I cs) :=
  (specialize_eq I (e.apply w).env cs).symm
```

The fully qualified name on one side of each equation is the three-argument def. `provenance_update` is that equation at `e.apply w`. [MEASURED grep] `specialize` and `specialize_eq` occur only in `C/Provenance.lean` and `P/Provenance.lean`. No surviving proof cites them.

What the kept polynomial still says, and these two do not: [READ `provenance_iff` and `monomial_verified`, not in the deletion hunk]

```
(∃ c ∈ cs, judge I w c = .verified) ↔ ∃ m ∈ provenance I cs, m.eval I w = true
judge I w c = .verified ↔ D.check … = true ∧ (monomial I c).eval I w = true
```

`Monomial.eval` is `envOK` (the guard and the budget literals) and the token literals. That is the all-environment bridge, and it stays. `label_iff` rewrites by `provenance_iff`. [READ `P/Provenance.lean:190`]

What `specialize_eq` adds on top of that is list equality, order and multiplicity, with the twin's body. Restating it after the deletion means writing that body inline on the right-hand side: the second shape, under no name. The LHS does mention the kept `provenance`. The fact it proves is still "you get the twin back." Once the twin is gone, that fact has no subject and no consumer. (a).

## (4) The 20

Binder order. Not a new premise. Not the S6 matcher class, though seven of the twenty are equation lemmas of that shape.

[MEASURED `diff-S10.txt`] 21 TYPE lines. One is `tm_decEq_toy`. The other 20:

| kind | names |
|---|---|
| defs, both `D` and `E` | `EnvLit.eval`, `Monomial.envOK`, `Monomial.eval`, `monomial`, `provenance`, `label` |
| their equation lemmas | `EnvLit.eval.eq_1`, `.eq_2`, `Monomial.envOK.eq_1`, `Monomial.eval.eq_1`, `monomial.eq_1`, `provenance.eq_1`, `label.eq_1` |
| theorems whose statement applies one of those defs | `monomial_verified`, `provenance_iff`, `monomial_complementary_dead`, `eval_consistent`, `subsumes_eval`, `minimal_eval`, `label_iff` |

[READ `Closure.lean`] `variable {E : Type}` is at the world section; `variable {D : CalculusData}` is later, before Judgment, which is where the block is inserted. [READ `C/Provenance.lean:9`] the old file was `variable {D : CalculusData} {E : Type}`. Section variables are prepended in declaration order, so a def that mentions both elaborates `{D} → {E} → …` there and `{E} → {D} → …` in Closure. The source of each def, apart from `provenance`'s docstring and the deleted `specialize`, is the P9 text. [READ the patch] No new binder in the source. Closure has no other `variable` and no instance variable.

The proof file's own line stays `variable {D : CalculusData} {E : Type}`. [READ the patch: that line is not in a hunk] So the theorems' outer binders do not flip. What flips is the implicit arguments of the moved constants inside the elaborated type (`eval` / `provenance` / `monomial` / `label` now take `E` before `D`). `judge` was already defined in Closure, so it was already that order. The control is `provenance_complementary_dead`: its statement calls `judge` and `effSupports`, not a moved def, and it is VALUE but not TYPE. [MEASURED `diff-S10.txt`] Its hypotheses `hp` and `hn` are outside every hunk.

Same filter on the defs that do not mention `E`. `Monomial.consistent`, `subsumes`, `minimal`, `subsumes_iff`, `subsumes_trans`, `minimal_subset`, `minimal_covers`, `provenance_minimal` are in neither TYPE nor VALUE. They moved module (part of the 72) and the digest matched. A gained premise or a changed relation would have put them in TYPE.

[INFERRED, not re-elaborated] Token-multiset equality is the builder's comparison. `diff-S10.txt` lists names only, and this read did not print types. The source accounts for a swap of `{D}` with `{E}` and for nothing else: the seven theorem statements are not in a hunk, and the six defs are the P9 equations. That is the same honesty bracket as the S6 and S7 reads, where the digest file also listed names only. It is not the S6 matcher class (those were `.eq_def` / `.match_` of a def whose own type did not change) and not the S7 `._proof_N` renumbering. The seven `.eq_N` here are equation lemmas, and their types move because the parent def's type moved.

VALUE but not TYPE, four, none a premise:

- `provenance_complementary_dead`, the control above. Proof term only.
- `Monomial.supports`, `.blockers`, `.envLits`. Projections. `Monomial` does not take `E`, so this is not binder order. Same residue as S6's `HoleDecl.name` / `.ctx` / `.ty`: the structure moved, the type matches under the rename, the value hash does not. Not a statement.

## (5) Outside

[MEASURED `diff-S10.txt` whole, 62 lines] `module changed 72 of which from a module the step does not move 0`, and the only arrow is `Lang.Contextual.Provenance → Lang.Contextual.Closure`. `new 0`. `vanished 10 declared 10 UNDECLARED 0`, every one a twin, tooth, or `specialize` constant. No Kernel, Ledger, Host, Census, Journey, or Std hole name appears.

[READ the patch, 7 files] `Closure.lean` (the insertion), `C/Provenance.lean` and `ProvenanceTeeth.lean` deleted, `P/Provenance.lean` (namespace, docstring, the two bridge theorems), `Judge.lean` (the three-argument `provenance_iff`), `ClosureStatements.lean` (`Monomial.holds`), `Core.lean` (the conjunct in (1)). The `Core.lean` hunk is the one edit outside the provenance files, and it is the declared statement change. No other hunk.
