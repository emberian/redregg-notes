VERDICT: RELEASE S3

Nothing that survives is weaker. Protocol stands without P5, so deleting P5 neither forecloses nor prejudges R1. The census summary is 1,027 vanished and 0 statement or value-hash changes; the size drop is the eleven files, not fourteen.

Base read: `origin/main` = `a9ab51421ef5c0e9c849da9f632f503d1b2c8d85` after `git fetch origin` (S2, the commit IMPACT-S3 names). Local `HEAD` is `7e02852`, behind that tip. Nothing below was read from the working tree. No build. `git grep <rev>` is blocked from this sandbox; name searches are `git log -S` (a string with an empty log never occurs in any blob) and `git show origin/main:<path>`.

## (1) No surviving module, theorem, gates row, or fixture is weaker

The eleven are a closed import cluster. Every `import` of them that ever existed is either one of the eleven or a module S1 already deleted (`Interfaces`, `P/Interfaces`, `P/P1`, `NogoodGameBridge`, `ProvenanceExperiments`, `P11bExperiments`). [MEASURED pickaxe, spot-check 1] `lakefile.lean` is `globs := #[.submodules X]` for every `lean_lib`, and no `root :=` names any of the eleven. [READ `lakefile.lean` whole at `origin/main`] `git log -S` of `Lang/Contextual/P5`, `Contextual.P5`, `NogoodGames`, and `judgeRecorded` over `gates/`, `rows/`, and `lakefile.lean` is empty. The only surviving hits of `judgeRecorded`, `RecordedClosure`, and `NogoodGames` are prose in `decisions/lang.md`. That file is the append-only record, not a gates row, and S3 appends `### LANG-74.3` rather than editing it.

Near-misses, none of them the `audit_append` shape:

- `uniform_coin_problem_refuted` (`Lang/Proofs/Contextual/P5.lean:247`) is a `P5.judge` fact about `Protocol.Coin`. It is not the only statement about that example, and the example is not a deployed object. `Coin.no_foresight`, `Coin.foresight_iff_names_separate`, `Coin.response_indexed_names_have_foresight`, and `Coin.response_dependent_succeeds` are declared in `Lang/Proofs/Contextual/Protocol.lean`, which does not import P5. [READ that file's header and its three import lines; MEASURED `rg` of the whole file for `P5|Refines|Machine` is empty] The deployed nano program is `Hosting.Resident.Prog`, reached by `nano_runs_iff` / `nano_interp_agrees` / `nano_interp_runs` in the same module, which imports `Hosting.Proofs.ResidentRun` and `Lang.Contextual.NanoBridge`, not P5. S1 re-homed `audit_append` because it was the only composition law for the deployed `Kernel.Receive.audit`. Nothing in these 62 statements is that. [MEASURED `git log -S "theorem audit_append"`: the surviving home is `Kernel/Proofs/Audit.lean` at `82ac944`; the Integration copy left at `6eb92fe`]

- `Refines`, `AlternatingSimulation`, `refines_refl`, `refines_trans`, `simulation_preserves_safety` are the tree's only alternating-simulation theory, and their subject is `P5.Machine`, not `Protocol.Prot` and not a deployed program. [READ `Lang/Proofs/Contextual/P5.lean:74–91`, `Lang/Contextual/P5.lean` `structure Machine`] Deleting them removes no consumer of a surviving theorem. `priceReceiver` occurs only in `C/P5`, `P/P5`, and the already-deleted `P/Interfaces`. [MEASURED pickaxe]

- `judgeRecorded` / `RecordedClosure` and `Material.inspectCandidate` are consumers of `Contextual.judge`, not its meaning. `judge_verified_iff` stays in `P/Judge`. After this deletion `P/Judge` is still imported by `HoleBridge`, `Provenance`, `Repair` (keep) and by `Acyclic`, `Boundary`, `Stability`, `ProvenanceTeeth` (later steps). [MEASURED pickaxe of `import Lang.Proofs.Contextual.Judge`] `candidate_verified` is an instance of that iff, not a second statement of it.

- `C/ProvenanceRepairs` and `P/ProvenanceRepairs` lose their only outside importers (`C/Nogoods`, `P/Nogoods`). [MEASURED pickaxe: those two imports, plus the proof module's own import of the def] The pair becomes an unimported Lang-glob leaf until S4, which deletes it. Statements unchanged. Unimported is not weaker, same as `P/P5` sitting unimported between S1 and S3.

- `Iface.mk.congr_simp` changes module and does not change its statement. S1 had already recorded it as a lazily realized congruence of surviving `Closure.Iface.mk`, re-owned into `P/Material` (`IMPACT-S1.md` §5.2). S3 deletes that owner, so it is realized somewhere else. [MEASURED `fold/diff-S3.txt`: `type-digest changed 0`, `value-hash changed 0`, `module changed 1`] Not a declaration of the eleven, and not a survivor made weaker.

- SIZE's "Lean lines (deployed)" falls 30,937 → 30,375 (−562). That is `gates/size.py` counting the six definition modules as deployed when no exe root reaches them, which the map already flags (§5.8, fix at S6). [MEASURED `fold/S3-size-preview.txt`] The Host closure line is absent from the preview, so it did not move. No generated file is in the preview.

`gates/size.py` theorems move 6,288 → 6,228 (−60). The appendix's 62 entries count the two fields of `structure AlternatingSimulation : Prop` (`inputs`, `outputs`), which that regex does not. 25 − 2 + 8 + 11 + 9 + 9 = 60. Not a hidden survivor.

## (2) Deleting P5 does not foreclose or prejudge R1. Protocol stands without P5.

The edges run from P5 into Protocol, never back. [MEASURED, spot-check 2]

At `a9ab514` the R1 cluster is:

- `Lang/Contextual/Protocol.lean` — no `import`, and the text does not contain `P5`
- `Lang/Contextual/NanoBridge.lean` — `Protocol`, `Hosting.Resident.Trace`
- `Lang/Proofs/Contextual/ProtocolTyping.lean` — `Protocol`
- `Lang/Proofs/Contextual/Protocol.lean` — `ProtocolTyping`, `NanoBridge`, `Hosting.Proofs.ResidentRun`
- `Lang/Proofs/Contextual/Negotiation.lean` — `Lang.Proofs.Contextual.Protocol` only

`import Lang.Contextual.Protocol` was ever added only in `C/P5`, `NanoBridge`, and `ProtocolTyping`. `import Lang.Proofs.Contextual.Protocol` was ever added only in `P/P5` and `Negotiation`. After S3 the remaining importers are all inside the R1 five. Those five files are not in the delete list, and nothing they import is either.

`Refines` cannot be reused as fork A's refinement. Its statement is `Refines (impl : Machine SI I O) si (spec : Machine SS I O) ss`, and `polarized_matching` only borrows `Protocol.Polarity` (`ours` / `theirs`) as the owner of a `P5.Action`. [READ `P5.lean` `Action.owner`; `P/P5.lean:83`, `:140`] `Protocol.Prot` is `ret | call | hole`. Negotiation's 36 theorems (`template_hasProt`, `lost_reply_blocks_replan`, `separate_witnesses_over_substitutions`, …) are already the theory over that `Prot`, and they do not mention P5. Fork A (resident `Prog` gains holes and becomes `Prot`) is still a HOSTING+LANG card written later, over `Prot`. Fork B (delete the five at S14) is still open, and S3 is what makes the map's premise true: after S1 and S3 nothing outside the five imports them. That premise is the question R1 asks Ember, not an answer. [INFERRED only on "prejudge"; the import direction is measured]

## (3) Census diff: confirmed, with the label "14" not meaning fourteen files

I did not re-elaborate. From `fold/diff-S3.txt`, which is the measured summary:

```
before 53652 after 52625
vanished 1027 of which outside the declared 14 modules 0
declared-module constants 1028 all vanished: False
new 0 type-digest changed 0 value-hash changed 0 module changed 1
   Nanodregg.Lang.Contextual.Iface.mk.congr_simp
```

1027 vanished, 0 new, 0 type-digest changes, 0 value-hash changes. 1027 + 1 re-owned = 1028 declared-module constants, so every constant of the declared set is accounted for and nothing outside that set vanished or changed statement or value hash. [MEASURED the file]

The word "14" is not the file count. `fold/S3-size-preview.txt` moves Lean modules 529 → 518 (−11), proof-modules 285 → 280 (−5), Lang lines 46,067 → 44,794 (−1,273). The eleven line counts in IMPACT-S3 §1 sum to 1,273, and the split is six definition modules plus five proof modules. A scratch deletion of fourteen files would have moved the module count by 14. The three names the label has room for contribute no file and no constants (the S1 modules are already absent at this tip; see spot-check 1). "All within the eleven" is the size drop plus `outside = 0`, not the numeral in the format string. IMPACT-S3 §5 drops the "14" when it quotes the line. The quote matches the counts and not that word. [MEASURED both files; INFERRED that "14" is a stale format string or a declared-name list containing empty names, not three extra deleted modules]

## Spot-checks

### 1. The eleven exist; their importers do not survive outside the set

Command:

```
git -C /Users/ember/dev/nanodregg ls-tree -r --name-only origin/main -- \
  Lang/Contextual/P5.lean Lang/Proofs/Contextual/P5.lean \
  Lang/Contextual/Games.lean Lang/Proofs/Contextual/Games.lean \
  Lang/Contextual/NogoodGames.lean Lang/Proofs/Contextual/NogoodGames.lean \
  Lang/Contextual/Nogoods.lean Lang/Proofs/Contextual/Nogoods.lean \
  Lang/Contextual/Material.lean Lang/Proofs/Contextual/Material.lean \
  Lang/Contextual/P1.lean Lang/Proofs/Contextual/P1.lean \
  Lang/Contextual/Interfaces.lean Lang/Proofs/Contextual/Interfaces.lean \
  Lang/Proofs/Contextual/NogoodGameBridge.lean
```

Output: the eleven paths, and not `P/P1`, `Interfaces`, `P/Interfaces`, or `NogoodGameBridge`.

Commands (each `--pretty=format:%h --name-only origin/main`):

```
git log -S "import Lang.Contextual.P5"
git log -S "import Lang.Proofs.Contextual.P5"
git log -S "import Lang.Contextual.Games"
git log -S "import Lang.Proofs.Contextual.Games"
git log -S "import Lang.Contextual.NogoodGames"
git log -S "import Lang.Proofs.Contextual.NogoodGames"
git log -S "import Lang.Contextual.Nogoods"
git log -S "import Lang.Proofs.Contextual.Nogoods"
git log -S "import Lang.Contextual.Material"
git log -S "import Lang.Proofs.Contextual.Material"
git log -S "import Lang.Contextual.P1"
git log -S "import Lang.Proofs.Contextual.P1"
```

Surviving files named, and the import line read with `git show origin/main:<path>`:

| import | still present in |
|---|---|
| `Lang.Contextual.P5` | `C/Games:5`, `C/Nogoods`, `C/P1`, `P/P5:2` |
| `Lang.Proofs.Contextual.P5` | `P/NogoodGames` |
| `Lang.Contextual.Games` | `C/NogoodGames`, `P/Games` |
| `Lang.Proofs.Contextual.Games` | `P/NogoodGames` |
| `Lang.Contextual.NogoodGames` | `P/NogoodGames` |
| `Lang.Contextual.Nogoods` | `P/Nogoods` |
| `Lang.Contextual.Material` | `P/Material` |
| `Lang.Contextual.P1` | `C/Material` |

`import Lang.Proofs.Contextual.P1` and `import Lang.Proofs.Contextual.NogoodGames` and `import Lang.Proofs.Contextual.Nogoods` and `import Lang.Proofs.Contextual.Material`: only files S1 deleted. Empty of survivors.

Direct imports read off the eleven, matching IMPACT-S3 §1:

- `C/P5` → `Lang.Contextual.Protocol` only
- `P/P5` → `Lang.Contextual.P5`, `Lang.Proofs.Contextual.Protocol`
- `C/Games` → `Lang.Contextual.P5`
- `P/Games` → `Lang.Contextual.Games`
- `C/NogoodGames` → `Lang.Contextual.Games`, `Lang.Contextual.Closure`
- `P/NogoodGames` → `NogoodGames`, `P/Games`, `P/P5`
- `C/Nogoods` → `Lang.Contextual.ProvenanceRepairs`, `Lang.Contextual.P5`
- `P/Nogoods` → `Nogoods`, `P/ProvenanceRepairs`
- `C/Material` → `Lang.Contextual.P1`
- `P/Material` → `Material`, `Lang.Proofs.Contextual.Judge`
- `C/P1` → `Lang.Contextual.P5`, `Lang.Contextual.Closure`

`fold/S3-grep-suffix.txt` is `dotted relative forms 1431 with hits 0`.

### 2. Protocol does not import P5; `Refines` is over `Machine`; Coin's theorem stays

Command: `git show origin/main:Lang/Proofs/Contextual/Protocol.lean`, then `rg` of that output for `^import |P5|Refines|Machine|priceReceiver|LogicalStatus`.

Output:

```
26:import Lang.Proofs.Contextual.ProtocolTyping
27:import Lang.Contextual.NanoBridge
28:import Hosting.Proofs.ResidentRun
```

No other hit. The header of that same file names `Coin.no_foresight` as a theorem of this module.

Command: `git show origin/main:Lang/Contextual/Protocol.lean`, then `rg` for `P5|Games|Nogood|Material|import `. No hits. `inductive Polarity | ours | theirs` is defined in this file; `inductive Prot` is `ret | call | hole`.

Command: `git show origin/main:Lang/Proofs/Contextual/Negotiation.lean` (head):

```
import Lang.Proofs.Contextual.Protocol
```

one import. `git show origin/main:Lang/Contextual/NanoBridge.lean` (head): `import Lang.Contextual.Protocol` and `import Hosting.Resident.Trace`.

Command: `git show origin/main:Lang/Proofs/Contextual/P5.lean` at the refinement block:

```
structure AlternatingSimulation {SI SS I O : Type} (impl : Machine SI I O)
    (spec : Machine SS I O) (R : SI → SS → Prop) : Prop where
def Refines {SI SS I O : Type} (impl : Machine SI I O) (si : SI)
    (spec : Machine SS I O) (ss : SS) : Prop :=
  ∃ R, R si ss ∧ AlternatingSimulation impl spec R
```

and `uniform_coin_problem_refuted` feeds `Protocol.Coin.wins` to `P5.judge`, with the comment that `no_foresight` is the independent impossibility theorem.

Command:

```
git log -S "import Lang.Contextual.Protocol" --pretty=format:%h --name-only origin/main
git log -S "import Lang.Proofs.Contextual.Protocol" --pretty=format:%h --name-only origin/main
```

Output: definition importers `C/P5` (`b72e5a8`), `NanoBridge`, `ProtocolTyping` (`8c31ace`). Proof importers `P/P5` (`b72e5a8`), `Negotiation` (`8c31ace`, which also touches `P/Protocol` itself). No third survivor.

### 3. The diff file and the size drop

Command: read `fold/diff-S3.txt` and `fold/S3-size-preview.txt` (full; both are short).

`diff-S3.txt`:

```
before 53652 after 52625
vanished 1027 of which outside the declared 14 modules 0
declared-module constants 1028 all vanished: False
new 0 type-digest changed 0 value-hash changed 0 module changed 1
   Nanodregg.Lang.Contextual.Iface.mk.congr_simp
```

`S3-size-preview.txt`:

```
-| Lean modules | 529 | — |
-| Lean proof-modules | 285 | — |
+| Lean modules | 518 | — |
+| Lean proof-modules | 280 | — |
-| Lean lines (Lang) | 46067 | — |
+| Lean lines (Lang) | 44794 | — |
-| Lean lines (deployed) | 30937 | — |
+| Lean lines (deployed) | 30375 | — |
-| max dependents of a non-foundation module | 351 | — |
-| theorems | 6288 | — |
+| max dependents of a non-foundation module | 349 | — |
+| theorems | 6228 | — |
```

−11 modules, −5 proof modules, −1,273 Lang lines, −60 theorems. 46,067 − 44,794 = 1,273. 6,288 − 6,228 = 60.
