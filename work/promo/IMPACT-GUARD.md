# IMPACT-GUARD — the stale-path guard becomes a declaration diff from the census environment (R-0023)

Worker: CX-GUARD (Claude). Written 2026-10-22, BEFORE the build, for the cross-family read. Base: nanodregg
`main` = **f8d04ac** (E1 has since landed as 4916f3a); worktree `hbox:/tank/dregg-build/nanodregg/wt/guard`
(own `.lake`, copied from wt/cxfold at f8d04ac). Card: R-0023, cv 01a15f18-2636. Tags: READ / MEASURED / INFERRED.
Owner: GATES (gates/, scripts/, decisions/gates.md only; no cross-layer file).


## BUILT — under R-0034's three conditions (this section supersedes §0–§8 where they differ)

Worktree `hbox:/tank/dregg-build/nanodregg/wt/guard`, rebased on main `2d3bf14`. Files: `gates/decls.py` (new),
`gates/decls_plants.py` (new), `gates/decls-plants.tsv` (the pinned maps), `gates/rebase.py`, `gates/runs.tsv`
(one `script:` row), `scripts/pre-push`, `scripts/commit`, `decisions/gates.md` (GATES-20t). Whole outputs under
`hbox:/tank/dregg-build/nanodregg/logs/guard/`.

**Condition 1, the map is checked** [BUILT; plants]. The verbs:
- `RENAMES: OLD → NEW` and `RESTATES: OLD → NEW`: both compare the elaborated statements under the map, and a
  mismatch is `rename not equal` / `restate not equal`, with the statement diff. An arrow at an unrelated declaration
  is refused (synthetic case `restates-unrelated`).
- `RESTATES-MEANING: OLD [→ NEW]`: a deliberate change of meaning. Without it a changed theorem is
  `undeclared restatement: NAME`, with the token diff of the two statements (the kernel printer's text; the digest
  decides).
- `DELETES: NAME`.
- `DELETES-MODULE: M` (condition 2): a removed module is one explicit line, never a free pass. An undeclared one is
  `undeclared module deletion: M (N declarations)`.

**Condition 3, pinned plants, each asserting refusal NAMES** [MEASURED, plants-all-1.out + plants-R2.out]:
- H4 832a815 (one of the 10-20 trio): GREEN with its 22-line map. H4- reads `undeclared restatement: …import_genesis_iff`.
- H1 P7: GREEN with its 111-line map, which names no `escrow_link_bites`: the move is explained by the declaration.
- R2 = GATES-20p's removal of `escrow_link_bites` from the real P7 file: reads BOTH `undeclared deletion` and
  `stale declaration` naming it.
- H3 S9, the PRICE fixture, not a false positive: GREEN with 27 lines, the same count IMPACT-S9's census gave.
  H3- reads `runHoleGuard_cost`.
- H2 E1: GREEN with the FULL 66-line map (48 RESTATES-MEANING, 18 DELETES) and no `--reverts`. H2- reads
  `undeclared restatement: Nanodregg.Lang.selectHole_origin`. MEASURED: H2's `--lean-lacks` file is empty, so under
  plain 20b (20p's rule deleted) `stale` finds no lack in E1. E1's bite was 20p's rule, not a stale copy; that the
  replay conflicts is INFERRED from the empty file and 20b's rule.
- C0 reads `unused map line`.
- R1, a1ca640's members.rs plus one line: `stale path` (the text half).
- R3, 0856ca3^'s Emit/Rust.lean: `stale declaration: Nanodregg.Emit.Rust.bounds`, a value reverted that check 1
  cannot see.
- Standing synthetic row: 23 cases GREEN; its `--harness-control` reads RED naming harness-control.
- End to end, this pre-push `--fast` in a real slot: red (undeclared deletion, with the line to paste), green (a
  moved theorem, 30 s for the whole fast judge), stale (stale declaration).

**§6 price, MEASURED** [plant wall times]:
- The judge's step (reach export plus diff): 8.5 s at 87 modules, 11.8 s at 217, 12.4–16.7 s at 218, 14.0 s at 278.
- Bootstrap (a miss): one parent build delta, plus a 15.7–19.1 s whole export at 1.6 GB RSS.
- Cache: about 2.0 MB per tree.
- The statement text for diffs uses the kernel printer: +3 s, where `ppExpr` would cost +37 s.
- The shared cache is pre-seeded for main's tree at e9c126f by the end-to-end runs.

**Not done here, filed:** cv 01a165b2-5689 (the convergence re-exports a cached digest whole and compares it; kept
off the landing path, as the read asked).

## 0. Answer first

- **What is replaced.** `gates/rebase.py stale` decides "this landing reverts commit C on path P" from TEXT for every
  path, and for `.lean` paths carries GATES-20p's Python Lean lexer (`active_lean_statement`, the `^theorem … := by`
  regex) as a third special case. For `.lean` paths that decision moves to the ELABORATED ENVIRONMENT: the
  declarations Lean itself reports (name, kind, statement, value, and the source lines the elaborator records for
  each, `findDeclarationRanges?`), exported from the census environment of the candidate and of its parent.
- **Two checks, both in the judge after the build, both refusing by name** (§3):
  1. **The declaration diff (new, the card's design).** Every declaration of the parent that is absent from the
     candidate, and every theorem of the parent whose statement differs in the candidate, must be declared by the
     landing's message: `RESTATES: old → new` (or `RESTATES: name`), `RENAMES: old → new` (statement must be
     equal under the map), `DELETES: name`. Declarations of a module the landing deletes go with their module.
     A declared line that does not apply is refused (`drop the line`), so the map cannot rot.
  2. **The stale-copy resolution (what the text check was for).** The language-agnostic text detector still finds
     "your copy lacks C's change to P" (GATES-20b + 20b′, kept). For a `.lean` P the lack is no longer the
     verdict: C's lines are located in main's copy, mapped by the PARENT environment's declaration ranges to the
     declarations that hold them, and the lack is EXPLAINED when every such declaration is present in the
     candidate as main has it (theorem: same statement, proof free; anything else: same type and same value) or is
     declared in the map. Unexplained → `stale declaration: NAME (P:a-b) …`. Lines of C's change that lie in no
     declaration and are not blank stay a text verdict (`--reverts C` remains the escape).
- **Non-Lean paths stay textual, unchanged** (GATES-20b, 20b′): no environment can see a Rust or TSV line, and the
  text detector is not a Lean parser; it is line containment.
- **Deleted:** GATES-20p's lexer and regex and `missing_added_theorem`'s special refusal (four functions in
  rebase.py), and the `.lean` branch of the text verdict.
- **Price, MEASURED on the built tree at f8d04ac:** the whole-environment export (460 modules imported, 20,577
  rows) takes **12.5 s wall, 1.6 GB RSS** (`logs/guard/export-main.log`). A landing exports only the modules its
  change reaches; the parent's digest comes from a per-tree cache composed at each landing (§3.4), so no landing
  builds its parent except the first after a cache miss. Final numbers for both modes in §6 after the build.
- **Design fork named (§4):** check 1 makes every restated theorem a declared line, which is what `PRICE PREMISES:
  restated: …` already claims in prose. Default: do it. The alternative (only declarations a recent commit
  touched) is cheaper in message lines and blind to old ones.

## 1. What the guard must still REFUSE (cases)

| case | old guard | new guard |
|---|---|---|
| (a) a landing whose tree LACKS a declaration a recent commit added, no restate/delete recorded (a stale `.lean` copy) | `stale path: P` (text) | `undeclared deletion: NAME (module M)` (check 1) and, when C is in the window, `stale declaration: NAME …` (check 2) |
| (a′) a landing whose `.lean` copy reverts a DEFINITION body a recent commit changed (statement unchanged) | `stale path: P` (text) | `stale declaration: NAME (P:a-b): main holds C's value, the landing's differs` (check 2: value digest) |
| (a″) a restated theorem nobody declared | not seen unless C is recent and the text differs | `undeclared restatement: NAME` (check 1) |
| (b) a landing that silently reverts NON-Lean lines another lane landed (members.rs V1/V2, GATES-20b) | `stale path: P` | **unchanged, textual**: `stale path: P` |
| (c) a `.lean` lack whose changed lines lie outside every declaration (an import, an `open`, a plain comment) | `stale path: P` | unchanged: `stale path: P` (text verdict stands; `--reverts C`) |

## 2. What it must PASS

- A **moved** declaration (same name, same statement; within a file or across modules; proof edited): P7's
  `escrow_link_bites` (d7989d9 on fe89edf, the GATES-20p input).
- A **restated** declaration whose name is in the landing's `RESTATES:` lines: E1's `runSetupWith_spec` /
  `runSetup_spec` in `Lang/Proofs/Load.lean` (4916f3a on f8d04ac; landed under R-0029's `--reverts d7989d94af13`).
- A **deleted** declaration on the landing's `DELETES:` list, and every declaration of a deleted module.
- A **renamed** declaration on `RENAMES:` (statement equal after the map is applied to the constants it names).
- The text half's existing passes: PERF-12's lakefile (20b′), HEAD-at-real-base merges (P3/P6 of GATES-20b).

**On the brief's "the fold's S9 bit (a moved theorem)" [MEASURED, `logs/guard/replay80.out`]:** replaying main's
current `stale` over main's last 80 landings (each on its parent) refuses 4: `d7989d9` on `gates/axioms-allow.tsv`
(a true deletion; it carried `--reverts 42c261b`), and three `.lean` restatements from 10-20 (`80419cf`
Host/Proofs/StoreIndex.lean, `832a815` Host/Proofs/Cli.lean, `eb7028d` Host/Proofs/Genesis.lean). CORRECTED by the
read (READ-GUARD-grok.md §4): they landed under the live guard (8c2c5fd is their ancestor); today's stricter 20p rule
refuses them.
No S-step of the consolidation is refused, and no S9 land log holds a `stale path` line. The moved-theorem bite is
P7's (REVIEW-20261021 timeline, REFUSE #3). S9 is kept as the third fixture for what it really is: the
restatement-heavy landing (27 user theorems change type, IMPACT-S9) that check 1 makes declare its price.

## 3. The design

### 3.1 The export (judge's Lean, interpreted, no new module)

`gates/decls.py` holds a Lean command `#decl_export OUT ROOTS…` as text and writes it after the imports into
`.lake/gates/DeclRun.lean`, exactly as `census.py` writes CensusRun (the census environment: every lib module but
the exe roots). It is the JUDGE's code (main's `gates/decls.py`, GATES-20), not a tree module, so no build target is
added and a change to it is judged in full (gates/*.py). One row per constant that HAS A DECLARATION RANGE (the
elaborator's own record of "this came from source": generated `.eq_1`, `match_`, `_proof_`, `_simp_` have none)
in a module of the tree: name, module, kind, first and last line, the statement's canonical serialization and the
constants it names, and for a non-theorem the value's (a theorem's proof is irrelevant). Module docs are rows too.

Serialization: post-order DAG of the term, hash-consed on the emitted token (so sharing is canonical and binder
NAMES are erased; binder INFO kept), constants abstracted to indices into a first-visit-order list. Python takes
`sha256(shape ‖ constants)`. No hash is used as equality inside Lean; the only digest is SHA-256 (128-bit truncation
is not used).

### 3.2 The declared map (the commit message)

```
RESTATES: Nanodregg.Lang.Proofs.Load.runSetup_spec             (same name, new statement)
RESTATES: Nanodregg.A.old → Nanodregg.B.new                     (replaced by another declaration)
RENAMES: Nanodregg.Lang.Contextual.X → Nanodregg.Lang.X         (statement must be equal under the map)
DELETES: Nanodregg.Lang.Foo.bar
```
A rename/restate entry also renames the constant inside every other statement (longest component-wise prefix, so
generated children follow the owner, as the fold's `digest_rn` did). It is applied to the CANDIDATE side, inverted,
so the cached parent digest never needs recomputing under a map. A refusal prints the exact lines to paste. The
lines are in the message, so `git log --grep RESTATES:` finds every restatement six weeks out ("say what you broke").
The brief allowed "or a file the message names": not built; a file outside the tree is not durable and one inside is
a second record of the same thing.

### 3.3 Where it runs

`scripts/pre-push`, both modes, right after the build step (fast: after `lake build $targets`; full: after the
whole build), as the step `decls`: `python3 "$J/decls.py" judge …`. A landing that changes no `.lean` file has an
empty reach and skips the export (`decls: ok (no module changed)`). `--no-build` with a changed `.lean` file is RED
`decls: a changed module cannot be judged without a build` (it could not be judged before either; now it says so).
`scripts/commit`'s `stale` step keeps the text detector; for `.lean` paths it no longer refuses but writes the lacks
(path, C, the blocks and their lines) to a file handed to pre-push (`--lean-lacks`). `--reverts C` is unchanged: a
named C is not forwarded.

### 3.4 The parent's digest: a per-tree cache, composed

A landing exports only its REACH (the changed modules and their dependents, what fast mode already builds): a
module outside the reach of both trees has identical source and identical imports, so its declarations are
identical. The candidate's whole digest = the parent's rows outside the reach ∪ the candidate's export of the reach;
it is written to `$common/nanodregg-decls/<tree>-<exporter>.tsv.gz` (atomic rename) and is the next landing's parent
digest (main's tree after the compare-and-swap is exactly the candidate's tree). On a miss (the first landing after
this lands; any exporter change) the judge materializes the parent in its slot, builds the libs, exports whole,
caches it, and re-materializes the candidate. Entries are keyed by tree id and exporter digest; the newest 64 are
kept (this judge's own files). The composition is exact by the reach argument; the convergence can re-export a
cached tree whole to check it (a follow-up, cv task, not this card).

### 3.5 Refusals (law 7: by name, each with its fix)

`undeclared deletion: NAME (M)` · `undeclared restatement: NAME (M)` · `stale declaration: NAME (P:a-b): C's
change … the landing's copy …` · `unused map line: RESTATES: NAME (…)` · `rename not equal: NAME → NEW` ·
`decls: NO VERDICT …` (an export that failed is RED, never ok: GATES-15).

## 4. The design fork (named, default taken)

Check 1 compares the candidate with its parent directly, so EVERY restated theorem and every vanished declaration
must be declared, not only those a window commit touched. Cost: flag-day messages get long (S9: 27 lines; E1: to be
measured). Gain: the message's `PRICE PREMISES` prose becomes a checked list (E1's message said "PRICE PREMISES: none"
while its digest diff showed binders added on 8 statements). The alternative (only what a window commit added) keeps
messages short and is blind to restating an old theorem. Default: the direct diff. A reader who prefers the window
form changes one function.

## 5. Plants (`gates/decls_plants.sh`, whole outputs under `logs/guard/`)

Historical, each must PASS (with the map the landing would have carried; then RED by name with one map line
removed, so the pass is not vacuous): **H1** P7 (d7989d9 on fe89edf, moved `escrow_link_bites`); **H2** E1 (4916f3a
on f8d04ac, restated `runSetup*_spec`); **H3** S9 (6c31cab on ac34521, 27 restatements).
Stale, each must be REFUSED: **R1** GATES-20b's V1 (a1ca640's members.rs + one line on main: `stale path`, the text
half); **R2** a real stale `.lean` copy from an older main that still builds (a theorem a window commit added is
absent: `undeclared deletion` + `stale declaration`); **R3** a stale copy reverting a definition body (`stale
declaration` by value). Each plant asserts its mutation happened before reading the verdict.

## 6. Price (MEASURED after the build; placeholders until then)

- Export, whole environment at f8d04ac: 12.5 s wall, 1.6 GB RSS, 20,577 rows (MEASURED).
- Reach export per landing (fast and full): TBD. Python diff: TBD. Cache entry: TBD bytes.
- Bootstrap (cache miss): one parent build delta in the slot + one whole export: TBD.

## 7. What it deletes

rebase.py: `active_lean_statement`, `added_theorem_statement`, `retained_added_theorem`, `missing_added_theorem`,
the missing-statement branch of `lacks` and of `stale`'s hunk printer, and the `.lean` refusal. GATES-20p is
superseded by GATES-20t (append-only record: a new entry, the old text kept).

## 8. Critique

- Check 2 trusts declaration ranges: a declaration's range covers its docstring and attributes, but not a plain
  `--` comment above it; C's change to such a comment reads as lines outside every declaration and stays a text
  verdict (a false refusal, cost one `--reverts`). Measured on the plants.
- The cache composition is only as exact as the reach: a module whose declarations change without its source or
  imports changing (a toolchain change) is covered because `lean-toolchain` is a build input that reaches every
  target (fast.py), so the reach is the whole tree.
- Generated declarations are not judged; a stale copy that only changes generated code cannot exist without a
  source change that is judged.
