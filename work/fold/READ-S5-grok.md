VERDICT: RELEASE S5

The seven spine definitions are not the semantics of a deployed judge. None of them is reached by `LangCalculus`, `langData`, `Lang/LiveHoles.lean`, `Std.hole` / `HoleBridge`, the journey rows, or the Host. Deleting them with the five modules does not weaken a surviving theorem, gates row, or fixture about a deployed object. The S10 pull-forward stays in this landing: `countRun` dies with the tooth, which is what LANG-74.1 already requires. The host rebuild is the price of that, not a reason to split.

`origin/main` after `git fetch origin` is `a747368` (the IMPACT's base). Local `main` is `7e02852`, behind. Everything below was read from `a747368` / `origin/main` via `git show`, `git blame -L`, and `git log -S`/`-G`. No working-tree file. No build. The builder's GREEN and the census elaboration are theirs; the arithmetic and the source diff were checked here.

## (1) The seven — none is a deployed semantics

`def judge` (`Lang/Contextual/Closure.lean:226–232`) reads `D.check`, `I.guard`, `c.blockers`, `effSupports`, and `c.cost`. It does not call `Rule`, `lfpIter`, `supportCount`, or `countRun`. [READ] `effSupports` (`:219–220`) and `Closure.support` (`:270`) are token lists. `supportCount` (`:558`) is a `Nat` over experiment-4 atoms. Same word, different constant. [READ]

`countRun`'s own docstring is "Naive COUNTING maintenance" (`Closure.lean:561–563`). [READ] That is the toy that keeps a withdrawn cycle, not the judge the host runs.

| definition | home at `a747368` | users still on main, outside the five |
|---|---|---|
| `Rule` | `Closure.lean:548` | `lfpIter` / `supportCount` / `countRun` (same section); `ClosureStatements.Derives` (`:83`, `List Rule`) |
| `lfpIter` | `Closure.lean:553` | `Worlds.ground` (`Worlds.lean:30–31`) and `P/Stability.lfpIter_sound`. Both go in this step |
| `supportCount` | `Closure.lean:558` | `countRun` only |
| `countRun` | `Closure.lean:563` | `P/Worlds` `counting_keeps_cycle_over_worlds` only (Experiments already gone at S1) |
| `ValueGuard` | `ClosureStatements.lean:75` | `P/Stability` only (TransportKinds went in `a747368`) |
| `StableUnder` | `ClosureStatements.lean:79` | `P/Stability` only |
| `Derives` | `ClosureStatements.lean:83` | `P/Stability` and `P/Worlds`. Not `Nanodregg.Lang.Derives` |

[READ the seven at those lines. MEASURED `git log -S` / `git log -G "List Rule"` on `origin/main`, intersected with `git ls-tree -r --name-only a747368`.]

`Nanodregg.Lang.Derives` is a different inductive: `BigStep` plus a size, `namespace Nanodregg.Lang`, `Lang/Proofs/Derives.lean:19`. [READ `:1–19`] `Complete.lean` counts the machine against it; the inductive itself is not declared there. The builder's "Complete.lean's Derives" is this constant. Deleting `Contextual.Derives` does not touch it. `P/Acyclic`'s `Derives` is its own inductive and leaves with that module. [MEASURED `git log -S "inductive Derives"`: `Acyclic.lean`, the old proof `Closure.lean`, `ClosureStatements.lean`, `Lang/Proofs/Derives.lean`, `Lang/Proofs/Need.lean`.]

Deployed objects, and what they actually use:

- `LangCalculus` imports `Closure` (`LangCalculus.lean:17`) so the Host closure rebuilds when `Closure.lean` changes. [READ] `langData` (`:589–602`) is `CalculusData` over `Term.fillRefs`, `Lang.infer`, `Term.usesVar`, `renameVar` / `lowerIdx` / `liftIdx`. No experiment-4 name. [READ]
- `LiveHoles.lean` (`open Contextual`, `:10`) calls `Term.usesVar`, `Term.renameVar (lowerIdx x)`, `Term.fillBounded`, `inferE` / `checkE`, and `run` on the guard. `selectHole` (`:113`) refuses with `holeDerivationMoved` / `holeSupportMoved` on ROM pins. It does not call `judge` or `countRun`. [READ the file]
- `HoleBridge.hole_judgment_admission_bridge` equates a closed-fragment `Std.hole` verdict with `judge … = .verified`. [READ the theorem at its introduction, `68e704d`] It uses `judge` and `effSupports`-shaped candidates. It does not mention `ValueGuard`, `StableUnder`, `countRun`, `lfpIter`, or `Rule`. [MEASURED path-limited `git log -S` empty for those names on `HoleBridge.lean`]
- The journey's experiment 4 is `Lang/Journey/ContextualCycle.lean`. `cyclePQ` (`:11–13`) is a term-level `ite` unrolling, "synchronous least-fixpoint", not `lfpIter`. `cycleRows` posts facts, runs `execute` on the live ROM, and checks that withdrawing grounding yields `(false, false, true)` and that an omitted pin refuses `holeUnpinned`. No experiment-4 name. [READ] `DeployedCycle` states the same fact as `BigStep` on `cycleTerm` (`deployed_cycle_p` at `:10`). [READ] It imports `ContextualCycle` and `BigStep`, not `Worlds` or `Acyclic`.
- Host, Kernel, Ledger: no import of the five, and no occurrence of `countRun` / `lfpIter` / `ValueGuard`. [MEASURED path-limited `git log -S` empty]

So `countRun` / `supportCount` do **not** encode counting for a deployed judge. They are not kept.

Importers of the five at the tip, same pickaxes: `C/Worlds` ← `P/Worlds` only; `P/Worlds` ← nothing (WorldsField went in S1); `C/Acyclic` ← `P/Acyclic` only; `Stability` ← `P/Worlds` only (Experiments and TransportKinds are gone). A closed leaf. [MEASURED `git log -S "import Lang.Contextual.Worlds"` and `git log -S "import Lang.Proofs.Contextual.Stability"`]

Deleting the seven changes no surviving statement. The only edit to a file that survives is `fold/S5-spine.diff`: the section at `Closure.lean:546–566` and `ClosureStatements.lean:74–85`, deletion lines only. `CalculusLaws`, `Derivable`, `WellFilled`, `Coherent`, `judge`, `effSupports`, `langData` are not in that diff. [READ the diff against the blame of those lines]

## (2) Nothing that survives is weaker about a deployed object

No surviving module, theorem, gates row, or rows fixture loses the only statement of a fact about a deployed object. Nothing is re-homed.

Near-misses, and why they are not `audit_append`:

- `counting_keeps_cycle_over_worlds` is the only remaining tooth that `countRun` keeps a withdrawn cycle. Its subject is `countRun` on `Worlds.reduct` (`Worlds.lean:24–31`), which the file itself calls a demonstration, "not a second kernel World or an admission path" (`:2–5`). [READ] The tooth and the function leave together. That is the choice LANG-74.1 already wrote down (below). The deployed grounding fact stays: `deployed_cycle_p` / `_q` / `_independent`, and the journey rows `LP E4 grounded cycle` / `LP E4 unfounded p/q both false, independent r remains true` in `ContextualCycle.lean`. [READ]
- `judge_stable` / `valueGuard_iff` / `stability_class` (`Stability.lean:12–48`) are the only theorems that a `ValueGuard` makes `judge` ignore the filling beyond its value. [READ] No surviving file contains `ValueGuard` or `judge_stable`. [MEASURED `git log -S`] `hole_judgment_admission_bridge` does not use them and does not change. The live guard is `runHoleGuard` (`LiveHoles.lean:86–95`), a different function. This is not the only statement about `Std.hole` or about `selectHole`.
- `gates/journal-report.md` says "the landed Worlds experiment" under a heading that already marks those rows historical and not shipped (`:19–21`, the cycle-grounding / alternative-worlds paragraphs). [READ `git log -G Worlds -p` on that file] Deleting the module does not change a check that runs. `gates/waste.tsv`'s "toy Worlds" is the kernel World in a seal-byte comment, not this module. [READ the `943cab7` hunk]
- `S5-grep.txt` ends `full-name hits outside deleted files: 0`. [READ] Bare-word hits (`World`, `Report`, `Graph`) are collisions. `lakefile.lean` never contained the module paths. [MEASURED `git log -S "Lang.Contextual.Worlds"` / `Stability` limited to `lakefile.lean gates rows` empty, except the historical journal report and `waste.tsv` above]

`cycle_loses_grounding_over_worlds` is the toy twin of `deployed_cycle_*`. The substrate version is the one that stays. The acyclic adapter's `Expr` / `Graph` / `Refusal` are a private language; nothing deployed imports them. [MEASURED the Acyclic import pickaxe]

## (3) 500 = 458 + 42, with a listing gap that does not refute it

[MEASURED `fold/diff-S5.txt`]

```
before 51739 after 51239          (difference 500)
vanished 500 of which outside the declared modules 42
declared-module constants 458 all vanished: False
new 0 type-digest changed 0 value-hash changed 0 module changed 0
```

`51739 − 51239 = 500` and `458 + 42 = 500`. Theorem counter in `fold/S5-size-preview.txt`: `6126 → 6081`, difference 45, the five modules' theorems and not the seven defs. Modules `504 → 499`. Lang lines `43047 → 42192` is `−855 = 819 + 36`, and `36 = 21` (Closure hunk `@@ -543,27 +543,6`) `+ 15` (ClosureStatements hunk `@@ -71,19 +71,4`). Deployed lines `−209 = 123 + 65 + 21`. [MEASURED those two files; the hunks were READ]

`all vanished: False` is the script's purity bit, not a survivor. The same bit is False on S1 (4 equation lemmas re-owned), S4 (1 re-owned), and S2 (`declared-module constants 0`, outside vanish 17). [READ `fold/diff-S1.txt`, `diff-S4.txt`, `diff-S2.txt`] On S5 it is False because 42 constants vanish outside the five files: the pull-forward. `module changed 0` says none of the 458 was re-owned instead of deleted.

The file then lists **40** names, not 42. Every one of the 40 is `Rule.*`, `lfpIter` / `lfpIter.*`, `countRun` / `countRun.*`, `supportCount`, `ValueGuard`, `StableUnder`, or `Derives` / `Derives.*`. [READ `diff-S5.txt:5–44`] The two unnamed constants are not in the artifact. They are not a refutation: the only source edit outside the five files is the spine diff, which deletes exactly these seven, and the header's other counters are 0 new / 0 type-digest / 0 value-hash / 0 module-changed. S1 already recorded that `countRun`'s equation lemmas are realized lazily (`decisions/lang.md`, LANG-74.1). [READ] I did not re-elaborate, so I cannot print the two names. The landing's cxfold log should. They do not, on this evidence, belong to some eighth definition.

## (4) Accept the pull-forward

Do not split S5 back into "five modules now, seven defs at S10".

The map's reason for S10-after-S6 is real: `LangCalculus.lean:17` imports `Closure`, so a Closure edit rebuilds the Host (`CONSOLIDATION-MAP-20261021.md` §1.5 F1, §4.2 row S10). [READ] That cost is due now anyway. LANG-74.1, already on main, says: S5 deletes `counting_keeps_cycle_over_worlds` while `countRun` still exists, so S5 must delete `countRun` or keep that tooth. [READ `decisions/lang.md`, the LANG-74.1 critique, commit `f665e94`] Keeping the tooth means not deleting `P/Worlds`. Deleting the tooth and keeping `countRun` leaves a definition with no theorem, which the map's own no-op rule forbids, and it leaves the bad semantics in the Host closure with nothing saying it is bad.

The three `ClosureStatements` defs cannot wait either. `Derives` is `inductive Derives (R : List Rule)` (`:83`). It does not typecheck if `Rule` goes and it stays. `ValueGuard` and `StableUnder` would be `Prop` defs whose only theorems are in `P/Stability`. [READ]

`ClosureStatements` is not in the Host closure (importers are `CoreInstance`, `Judge`, `LangInstance` — proofs). [MEASURED `git log -S "Lang.Proofs.Contextual.ClosureStatements"`: those three, at `b5f880b`] Only the four defs in `Closure.lean` rebuild the Host. They are one edit with `Derives`, so the rebuild is not separable from the Prop defs.

The builder's `host` + `lang-journey` GREEN is their measurement. I did not rebuild. It is not a condition on this verdict: the ordering is forced by the tooth and by `Derives`'s type, whether or not the binary is already warm.

## Spot-checks

### 1. Experiment 4 is not `judge`

Command: `git -C /Users/ember/dev/nanodregg blame -L 218,232 a747368 -- Lang/Contextual/Closure.lean` and `-L 546,566` on the same file.

`judge` (`:226–232`) is check, guard, blockers, `effSupports`, cost. The experiment-4 section is `:546–566`: `Rule` `:548`, `lfpIter` `:553`, `supportCount` `:558`, `countRun` `:563`. The IMPACT's line numbers match. [READ]

### 2. `countRun` never occurs on the deployed path

Commands (`git log -S countRun --name-only --pretty=format:%h origin/main`, then the same limited to the deployed paths):

Unrestricted history names only `Experiments.lean` (gone), `decisions/lang.md`, `P/Worlds.lean`, `Closure.lean`. [MEASURED]

Limited to `Lang/LiveHoles.lean`, `Lang/Contextual/LangCalculus.lean`, `Lang/Journey.lean`, `Lang/Journey/ContextualCycle.lean`, `Lang/Proofs/Contextual/HoleBridge.lean`, `Lang/Proofs/Contextual/DeployedCycle.lean`, `Lang/Proofs/Contextual/LangInstance.lean`: empty. Same empty result for `lfpIter` and for `ValueGuard` on those paths. [MEASURED]

`langData` at `:590–602` was read whole. It does not mention them. [READ]

### 3. The spine diff is only those seven, and the line arithmetic closes

`fold/S5-spine.diff` deletes `Closure.lean`'s experiment-4 section and `ClosureStatements.lean:74–85`, and nothing else. The deleted text matches `git blame -L` of `a747368` line for line. [READ both]

`819 + 36 = 855` and `123 + 65 + 21 = 209`, against `fold/S5-size-preview.txt`. [MEASURED] `6126 − 6081 = 45` theorems, which is Worlds 21 + Acyclic 18 + Stability 6, not a change to a surviving theorem.
