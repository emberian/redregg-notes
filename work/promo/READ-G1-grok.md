VERDICT: RELEASE G1

Cross-family read of the unlanded census patch `base2-final.patch` against nanodregg `origin/main` = `f8d04ac` (fetched 2026-10-22; local checkout `HEAD` is `7e02852`, and `git log 7e02852..origin/main -- Census/Statements.lean gates/census.py Kernel/Proofs/Fold.lean Protocol/Proofs/Settle.lean Host/Proofs/Backup.lean` is empty, so those files are the tip). No build. No tree edit. The census logs and the plant source were read from the builder's scratchpad `.../scratchpad/plant/`, not re-run.

## 1. The rule

**Yes. That sentence is the pigeonhole vacuity, and it is what the patch implements.** [READ patch `escape` / `leftFree`; READ `Kernel/Proofs/Fold.lean:30–31` `CollidesAmong`; READ `Kernel/Proofs/Trie.lean:852` `CollAmong`]

A disjunct is an escape when it is true of any map into a finite codomain, with none of the theorem's premises. KERNEL-56's shape is `∃ a b, a ≠ b ∧ f a = f b` with `a` and `b` chosen by the statement. `∃ p ∈ S, ∃ q ∈ S, …` over a list `S` the theorem already has (`chainPres`, `bindingPres`, a pair of `linkPre`s) is not that: `S` can be shorter than the codomain, and `Separates.elim` deletes the disjunct. The patch's test is the same sentence in elaborated terms: an `Eq` whose two sides are different applications of one head, both mentioning an `∃`-bound variable that no conjunct `t ∈ L` has struck, where `L` itself mentions no `∃`-bound variable. `∃ S, CollidesAmong hash S` stays RED because `S` is chosen, so the membership does not strike. [READ fixtures 2 and 3 in the patch; MEASURED `census-new.out` names `chain_binds_chosen_list` for ``E.hash p.fst p.snd = E.hash q.fst q.snd``]

**The vacuous shape it misses that matters here** is a membership that finites a projection and forgets the witness: [INFERRED, not compiled]

```lean
theorem forgotten (hE : E.Lawful n) :
    True ∨ ∃ a b : ByteArray,
      a.size ∈ [n + 1] ∧ b.size ∈ [n + 1] ∧ a ≠ b ∧ E.hash "x" a = E.hash "x" b
```

`[n + 1]` mentions no chosen variable, and `leftFree` strikes every chosen fvar inside the element term, so `a.size` strikes `a`. The equation is then judged with nothing chosen, and the row reads ok. It is nevertheless `lawful_collides`: `hE.size` says a digest has `n` bytes (`256 ^ n` of them) and there are `256 ^ (n + 1)` strings of length `n + 1`. Same proof as the plant's `lawful_collides`, which compiled. This is the builder's critique example, pinned to a length that actually exceeds the codomain. It matters because every digest input in this tree is a `ByteArray`.

**Of the five misses, none is a landed vacuous disjunct today.** [READ the whole `statements-tree.tsv`, 250 data rows, every verdict `ok`]

| miss | on main? |
|---|---|
| second preimage `∃ x ≠ c, f x = f c` | the *form* is three landed disjuncts (`windowedIn_refused`, `settle_refused_final`, `settle_refused_absorbed`: `txIdOf X c' = txIdOf X c`). Not vacuous: pigeonhole does not hand you a partner for a given `c`, and each is also bounded by `recordOf … ∈ S`. See §2. `git show origin/main:Kernel/Proofs/Fold.lean \| rg '∃ [A-Za-z]+ ≠'` and the same on `Trie.lean`: no hit. |
| closed list long enough that `CollidesAmong hash L` is pigeonhole | not in the TSV. Every `CollidesAmong` / `CollAmong` argument is built from the theorem's own objects (`chainPres`, `foldPres`, `bindingPres`, `headPres ++ readPres`, a two-element list of `pinPre` / `linkPre` / `rowPre`). |
| contradictory premise | not this wound. `forallTelescope` drops premises before judging; a `False → …` would not show up as a collision row. No such disjunct in the TSV. |
| def outside the census roots, or deeper than four unfolds | `CollidesAmong` and `CollAmong` are one unfold, both under `Kernel`, which is a census root. The plant's one-deep `Escape` was read RED (§3). Nothing in the TSV is a collision hiding behind an opaque head. |
| `a.size ∈ L ∧ hash a = hash b` | not in the TSV. No disjunct contains `.size ∈`. |

## 2. The five false positives, and what the tightening hides

All five are real case splits. One side of the equation is the theorem's own object; none is provable from `E.Lawful` or from the instance alone. [READ the statements]

- `Protocol.Settle.windowedIn_refused`, `settle_refused_final`, `settle_refused_absorbed` (`Protocol/Proofs/Settle.lean:437–442`, `:458–463`, `:489–496`). Right disjunct: `∃ c' v a, recordOf X c' v a ∈ S ∧ txIdOf X c' = txIdOf X c ∧ c'.unsigned.validUntil < c.unsigned.validUntil`. `c` and `S` are the theorem's. `c'` is drawn from `S`. The left disjunct is a window fact about that same `c`. New TSV rows 248–250 and old TSV rows 170–172, all `ok`.
- `Host.openWith_backup` and `openWith_backup_restart` (`Host/Proofs/Backup.lean:525–537`, `:757–771`). The disjunct the first draft saw is `∃ o' more, R = .ok o' ∧ o'.sealed = o.sealed ∧ …`. `o` and `R` are the theorem's open and the backup's open. The other arms are named faults (`tailTooLong`, `corrupt`, `record j`). New TSV rows 14–15, `ok`.

The two tightenings are what cleared them, and they do not clear a real landed vacuity:

- "Both sides chosen" clears `txIdOf X c' = txIdOf X c` and `o'.sealed = o.sealed` because `c` and `o` are telescope binders, not `∃`-bound. A one-sided equation is not pigeonhole (§1). `Tag.of_eq` (`Codec/Proofs/Tag.lean:234–241`) is the same shape on two messages the theorem already has, and its proof uses the hypothesis `Tag.of l c = Tag.of l' c'`, not `Lawful`.
- "A `∈` anywhere in the `∧` spine strikes every chosen fvar in the element" clears the Settle witnesses via `recordOf X c' v a ∈ S`. It is also what lets `forgotten` through (§1). That hole is not on main. Closing it by going back to "one chosen side is enough" is how the five real theorems went red; the builder fixed the rule instead of allow-listing them. [READ patch `gates.md` GATES-23a; READ new TSV rows 14–15 and 248–250]

Refuter (PROGRAM §3 G1, REVIEW H4): more than ~5 of the listed disjunctions going red means the detector is wrong. Measured red on the tree: **0**. [MEASURED `census-tree.out`: `STATEMENT-CENSUS ok: 250 disjunctions … (fixtures: 2 RED, 2 ok as required)`, exit 0; the `ok` line is printed only when `bad` is empty. READ every row of `statements-tree.tsv`: verdict column is `ok`.]

## 3. The plant

The three vacuous theorems are real, and they are not in the patch. They live in `scratchpad/plant/src/Plant/Vacuous.lean` (104 lines, no `sorry`). [READ the file; MEASURED `plant-compile.out`: `plant compile exit 0`]

| theorem | statement | proof | census |
|---|---|---|---|
| `chain_binds_inline` | `chain_binds`'s binders, conclusion `l₁ = l₂ ∨ ∃ dom a b, a ≠ b ∧ E.hash dom a = E.hash dom b` | `fun … => .inr (lawful_collides hE)` — the chain premises are not used | RED |
| `chain_binds_alias` | `l₁ = l₂ ∨ Escape E.hash`, `Escape` a one-line `def` of the same `∃` | same | RED |
| `chain_binds_chosen_list` | `l₁ = l₂ ∨ ∃ S, CollidesAmong E.hash S` | `.inr` of a two-element list built from `lawful_collides` | RED |
| `chain_binds_named` | the landed statement, `:= chain_binds hE` | the real theorem | ok |

`lawful_collides` is KERNEL-56's pigeonhole written out (inject `256^n + 1` strings through `E.bytes`, contradict `nodup_lt_len`). [READ `Vacuous.lean:40–65`]

[MEASURED `census-new.out`] `STATEMENT-CENSUS RED (3)`, exactly those three, each `right disjunct: \`E.hash … = E.hash …\` compares two inputs the statement chooses`, exit 1. `chain_binds_named` is not in the list. [MEASURED `statements-old.tsv:154–157`] main's census, same four theorems, all four rows `ok` — the name rule cannot see them. [MEASURED `census-old.out`] `STATEMENT-CENSUS ok: 171 disjunctions`, exit 0.

Leaving `Census/Plants/Vacuous.lean` out of the diff is right. A permanent copy would make every later census RED. The card's plant is the side run; the thing that lands is the fixtures.

**Fixtures, GATES-15.** [READ patch `fixtures`; READ `decisions/gates.md` GATES-15: the known-red control runs first, and a control that reads green refuses the run by name] Before the tree, every run judges four fixed statements: the bare `∃ a b, a ≠ b ∧ a % 2 = b % 2` and the same under `∃ L, ∃ a ∈ L, ∃ b ∈ L` must be RED; the same over `[x, y]` for bound `x y`, and `∃ a b, (a, b) ∈ S ∧ …` for a bound `S`, must be ok. A miss is `throwError` of `STATEMENT-CENSUS harness: fixture … read {RED|ok} over {n} disjunctions; it must read … over 1`. [MEASURED `census-tree.out`] the success line says `fixtures: 2 RED, 2 ok as required`, so this run's controls did fire. I did not re-run the two detector mutations (no builds). The refusal text quoted in the patch's GATES-23a is what that `throwError` prints; there is no `harness.out` in the scratchpad.

## 4. The walk

The new walker records a disjunction under `∧`, `↔`, `∃`, and up to four unfolds of a definition whose module has a census root as a prefix. Main's walker recorded only an outermost `Or` after `forallTelescope`. [READ both elaborators]

**Counts.** [MEASURED]

- `statements-old.tsv`: 171 data rows, header + the four `Plant/Vacuous.lean` rows (lines 154–157). Tree-only outermost disjunctions: 171 − 4 = **167**. `census-old.out` says 171. REVIEW H4's 166 is the 10-21 tree (`fe89edf`); the tip has one more outermost `Or`. The control TSV is this run, not a file embedded in the review.
- `statements-tree.tsv`: **250** data rows, no `Plant/` rows. `census-tree.out` says 250.
- 250 − 171 = 79 compares the new tree-only run with the old tree-plus-plant run. The newly listed tree disjunctions are 250 − 167 = **83**, if each of the 167 survived as one row. I did not diff the two sets with a script (a counter outside the scratchpad was blocked). Spot checks that did survive: `chain_binds` (new row 70), the three Settle theorems (new 248–250), `HeadSound.root_binds` (new 149).

**Three that are new, and real, and not red.** Each is absent from the old TSV's slice of that file, and each conclusion's outermost connective is not `Or`.

1. `Protocol.Settle.final_iff_recorded` (`Settle.lean:63–66`). Conclusion is a `↔` whose right side is `recordedNow o = true ∨ refusedAnswer ≠ none ∨ validUntil ≤ height`. New TSV row 247: left `recordedNow o = true`, right the rest of the `∨` chain, `ok`. The walker does not split a nested `Or`; one maximal disjunction, which is what is there.
2. `Protocol.Attempt.next_final` (`Attempt.lean:27–29`). Conclusion `∃ r s, l = some (r, s) ∧ (r = .confirm ∨ r = .probe)`. Old TSV lists `next_ends_open` and `next_submit` only. New row 233, `ok`.
3. `Protocol.Command.absorbStep_refusal_recorded` (`Command.lean:626–633`). The `∨` sits under `∃ c v a, r = recordOf … ∧ ((refusal shape) ∨ (cancel shape))`. Old TSV lists `derivePins_rowPins` and `step_verified` only. New row 237, `ok`.

`slotBefore_iff` (`Codec/Proofs/TrieOrderDeployed.lean:30–32`) is a fourth: an `↔` whose right side is an `Or`, plus a second row from unfolding `SlotBefore` to the byte compare (new rows 11–12), both `ok`.

**Red among the new rows: 0.** Same evidence as §2. The three `Trie.CollAmong` rows are `climb_sound`, `exclusion_sound`, `inclusion_sound` (new 143, 144, 146), each over `readPres` / `climbPres ++ pathPres`, all `ok`. That matches the builder's "3 over Trie.CollAmong". I did not recount the `CollidesAmong` rows; every one I read, which is all of them in the TSV, is `ok`.

## 5. Law 7

Charter law 7 is "refusals by name" (`CHARTER.md:91–92`). For this gate that means a refusal the census prints is a named string, and `gates/census.py` does not treat it as success.

[READ `origin/main:gates/census.py:35`, unchanged by the patch except a docstring] success is `returncode == 0` and `"STATEMENT-CENSUS ok" in out` (and the axiom and refine lines). The patch's two failures:

- fixtures: `STATEMENT-CENSUS harness: fixture …` via `throwError`, before the tree is walked and before any `logInfo` of `ok`. The harness sentence does not contain the substring `STATEMENT-CENSUS ok` (`read ok` is not that substring).
- tree: `STATEMENT-CENSUS RED (n):` via `throwError`. Same.

Both make lean exit nonzero. `census.py` then prints `census: RED` and returns 1. There is no path in the new command from a failed fixture or a red disjunct to `STATEMENT-CENSUS ok`.

**No wall-clock timeout fails open.** `subprocess.run` has no `timeout`. A hung `lean` hangs the gate; a killed one has a nonzero code and no `ok` line. GATES-16's `UNREAD(timeout)` is `runs.py`, not this command.

**One budget fails open, and it is named.** `unfoldFuel = 4`. At 0, `disjunctions` returns `#[]` and `escape` returns `none`: a disjunction behind five unfolds of the tree's own definitions is not listed and cannot go red, and the run can still print ok. [READ patch `unfoldFuel`, the `fuel > 0` branches, GATES-23a critique] Nothing on main needs the fifth unfold (§1). The other silent-ok the builder names is also real: the fixtures pass even if the walk sees zero theorems, so a broken import list would print `STATEMENT-CENSUS ok: 0`. This run printed 250, so the walk ran. Pre-existing, not introduced: `census.py` returns 0 with `census: ok (no modules)` when `tree.read` yields no module, without running the statement census at all.

## Commands

```
git -C ~/dev/nanodregg fetch origin
git -C ~/dev/nanodregg rev-parse HEAD origin/main          # 7e02852, f8d04ac
git -C ~/dev/nanodregg show origin/main:Census/Statements.lean
git -C ~/dev/nanodregg log --oneline 7e02852..origin/main -- Census/Statements.lean gates/census.py
git -C ~/dev/nanodregg show origin/main:Kernel/Proofs/Fold.lean | rg -n "def CollidesAmong|theorem chain_binds "
git -C ~/dev/nanodregg show origin/main:Kernel/Proofs/Trie.lean | rg -n "def CollAmong"
git -C ~/dev/nanodregg show origin/main:Protocol/Proofs/Settle.lean | sed -n '434,496p'
git -C ~/dev/nanodregg show origin/main:Host/Proofs/Backup.lean | sed -n '525,537p;757,771p'
git -C ~/dev/nanodregg show origin/main:gates/census.py
# plant, not re-run:
#   scratchpad/plant/src/Plant/Vacuous.lean
#   scratchpad/plant/census-old.out   census-new.out   census-tree.out   plant-compile.out
#   scratchpad/plant/statements-old.tsv   statements-tree.tsv
```
