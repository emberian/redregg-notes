VERDICT: RELEASE GUARD-BUILT

Worktree `hbox:/tank/dregg-build/nanodregg/wt/guard`, detached at `2d3bf14`, uncommitted. Read against R-0034's three conditions (READ-GUARD-grok.md). No build. The combined plant log is not the last word on R2; the rerun is, and the code matches the rerun.

## (1) Each condition

**Condition 1, the arrow compares. Kept, under a renamed meaning verb.** [READ `gates/decls.py`]

The digest is not the census exporter and not the fold's `digest_rn`. It is a fresh elaboration at pre-push. `scripts/pre-push` step `decls`, both modes, after the build, runs the judge's `gates/decls.py`. That writes `#decl_export` into `.lake/gates/DeclRun.lean` and interprets it with `lake env lean`, the census shape (lib modules, exe roots excluded) but a different command from `census.py`. One row per constant `findDeclarationRanges?` finds. Serialization is in that Lean: post-order DAG, hash-consed on the token, binder names dropped (`lam`/`forallE` keep binder info only), constants abstracted to a first-visit index. Python takes `sha256(shape ‖ constants)` (`digest_row`). The parent side is the cached digest under the identity map. A two-name line is inverted on the candidate (`NEW → OLD`, longest component-wise prefix) before hashing, so the cache is never recomputed under a map. Exporter id is `sha256(LEAN ‖ "v2")[:12]`, currently `9880f7b79e6a`.

`RENAMES: OLD → NEW` and `RESTATES: OLD → NEW` both require that digest equal (`judge`, the `same()` branch). A mismatch is `rename not equal` / `restate not equal`, and the refusal prints the kernel-printer token diff. The text is never the decision. Same-name `RESTATES` cannot smuggle a meaning change: if the digest differs it is `restate not equal`; if it does not, the line is `unused map line`. The meaning verb is `RESTATES-MEANING: OLD [→ NEW]`, and the statement must differ (equal → unused, and the message says to write `RENAMES`). Absent any such line, a changed theorem is `undeclared restatement: NAME`. [MEASURED plants-all-1.out] H2- reads `undeclared restatement: Nanodregg.Lang.selectHole_origin`; H3- reads `runHoleGuard_cost`; H4- reads `import_genesis_iff`, with the token diff (`digestHex` → `pinHex`).

The condition's last sentence is not the spelling that landed. A cross-name change of meaning is one `RESTATES-MEANING` arrow, not `DELETES` plus a new declaration. That arrow rewrites constants (so callers do not become false restatements) and is refused when the statements are equal. It is not refused when they are merely unequal. See (6). The pinned maps contain no arrows at all: 83+48+27+21 `RESTATES-MEANING` lines, all same-name, plus `DELETES`. [MEASURED `gates/decls-plants.tsv`]

**Condition 2, a missing module is one line. Kept.** [READ `gates/decls.py`] `DELETES-MODULE: M` is a verb. A module in the parent and absent from the candidate, with no such line, is `undeclared module deletion: M (N declarations)`, one line for every declaration in it. There is no "declarations go with their file" free pass. A `DELETES-MODULE` of a module that is not gone is `unused map line` (`still a module`, or `not a module of the parent`). No historical plant deletes a module. The refusal is the synthetic cases `module-deleted` / `module-declared` / `module-unused` (below).

**Condition 3, plants pinned, and the script asserts the name.** [READ `gates/decls_plants.py`] A RED plant passes only when every expected string is in the output (`all(e in out for e in p.expect)`). Exit 1 with the wrong sentence is a FAIL. The mutation is checked before the verdict (file bytes differ; `theorem escrow_link_bites` absent).

- R1 is a1ca640's `launcher/tests/members.rs` plus one lane line, parent `4916f3a`. [MEASURED plants-all-1.out] `stale path: launcher/tests/members.rs: the landing would revert 0cd046c8b944's change`. The log names the other lacks too (`978c9cf`, `ea52a4a`, `cdc0e9a`). 0.2 s, refused in `stale`, before any build.
- R2 is GATES-20p's removal: `drop_link_bites` cuts `escrow_link_bites` and its docstring out of d7989d9's `Ledger/Proofs/EscrowWitness.lean`, on H1's parent `fe89edf`. [MEASURED plants-all-1.out] the combined run is `decls plants: RED (1)`. R2 died in `stale` on `--reverts 42c261b` as a KERNEL cross-layer, and the two declaration names were not in that output. H1 in the same run accepted that revert, because d7989d9's message has `CROSS-LAYER: KERNEL` (line 165) and R2's message that run did not. [MEASURED plants-R2.out, plants-R2-1.log] the rerun carries P7's message (`REVERTS: 42c261b93025` printed, `stale` exit 0), then the judge reads both `undeclared deletion: Nanodregg.Ledger.Proofs.escrow_link_bites (theorem, Ledger.Proofs.EscrowWitness:229-252)` and `stale declaration: … e86f237e0533`. `decls plants: GREEN`. Current `plants()` passes `cand=d7989d9` into R2, which is that fix. The docstring at the top of `decls_plants.py` still describes the old R2 (`Ops/Proofs/Units.lean`, `writer_keeps_all`). The code and GATES-20t do not.

The standing synthetic row is 23 cases in `synthetic()`, wired as `script:gates/decls_plants.py` in `gates/runs.tsv`, including `restates-unrelated` and `module-unused`. [READ] No run of it is in `logs/guard`. The "23 cases GREEN" line in the built section is not a measurement I could find. It runs at convergence, not in these plants.

## (2) What it still refuses

**A Lean declaration a recent commit added, absent, no map line.** Both names. [MEASURED plants-R2.out] `escrow_link_bites`, added by `e86f237`, is `undeclared deletion` (check 1, the whole parent diff, not the window) and `stale declaration` (check 2, because that commit is in the 300-window and the text detector forwarded lines 229-253). [MEASURED e2e/out-red] deleting `writer_keeps_all` from current `Ops/Proofs/Units.lean`, with an empty lacks file, is still `undeclared deletion: Nanodregg.Ops.Units.writer_keeps_all` and the line to paste. Check 1 does not need the window.

**A non-Lean silent revert.** Still refused, and it is not a bag of lines. [READ `gates/rebase.py`] `holds`/`lacks` are GATES-20b′ again: `git merge-file` first (a conflict is neither, and is not forwarded), then each added block of `pre → post` must occur contiguous at line boundaries and each removed block must not (`_blocks`, `SequenceMatcher`, `autojunk=False`). [MEASURED plants-all-1.out] R1 is `stale path`. The four Lean functions are gone from this path; a `.lean` lack is written to `--lean-lacks` and not refused here (`lean_module`, and `lakefile.lean` stays on the text verdict).

**A definition value a window commit changed, statement untouched.** [MEASURED plants-all-1.out, e2e/out-stale] R3 and the e2e stale both read `stale declaration: Nanodregg.Emit.Rust.bounds`, add side and remove side. Check 1 cannot see it. [READ] a replay that conflicts is still neither, so a value reverted only inside a conflict is not forwarded and not a check-1 event. That is GATES-20t's own critique (a), and it is the old 20b rule. 20p's "force the lack even where the replay conflicts" was the theorem special case, and check 1 now covers a missing theorem without it.

Out-of-declaration `.lean` lines (import, `open`, a plain `--`) stay a text verdict inside the judge: `stale path: P … outside every declaration`, escape `--reverts C`. [READ]

## (3) What it no longer refuses wrongly

All three the brief named pass, and the one the design said was the real 10-20 false positive passes too. [MEASURED plants-all-1.out]

- **GATES-20p / P7 (H1, d7989d9 on fe89edf).** GREEN. 278 modules, 111 map lines, 83 meaning changes, and the map does not name `escrow_link_bites` (0 hits in the tsv). `stale` still forwarded the lack (`EscrowWitness.lean`, `e86f237`, add 229-253, 17.5 s). The judge explained it by the declaration. The negative control is the deletion, R2, not a dropped line. H1 has no H1-.
- **E1 (H2, 4916f3a on f8d04ac).** GREEN with the 66-line map (48 `RESTATES-MEANING`, 18 `DELETES`) and no `--reverts d7989d94af13`. The map contains `runSetup_spec`, `runSetupWith_spec`, and `selectHole_origin`. H2's `lean-lacks` is empty, so under plain 20b this landing has no text lack; the bite was 20p's rule, which is deleted. Dropping `selectHole_origin` is `undeclared restatement: Nanodregg.Lang.selectHole_origin (Lang.Proofs.LiveHoles:47-62)`. A green verdict on this judge means every reached parent declaration that vanished or whose statement digest differs is in that map. That is the completeness check, not a hand count of the diff.
- **S9 (H3, 6c31cab on ac34521).** GREEN, 217 modules, 27 map lines, 27 meaning changes. H3- reads `undeclared restatement: Nanodregg.Lang.runHoleGuard_cost`. This is the price fixture. It is not a historical false positive: the design's read stands, and GATES-20t says so. It passes as a fixture for "check 1 makes you write the price."
- **H4, 832a815**, the 10-20 restatement the design said belonged in the pass set. GREEN, 87 modules, 22 lines. H4- names `import_genesis_iff` and shows the statement diff. The other two of that trio (`80419cf`, `eb7028d`) are not planted.

## (4) Cost

Incremental. A landing exports its reach: changed modules, their transitive importers (`tree.dependents` is the fixpoint), and importers of a deleted module. A module outside both reaches is copied from the parent's cache. No `.lean` in the change: `decls: ok (no module changed)`, no export. A toolchain / lakefile / manifest change makes the reach the whole tree. [READ]

The added step, on a hit, is that export plus the diff. [MEASURED plants-all-1.log and plants-R2-1.log, the harness's own wall clock, not re-run here]

| reach | judge step |
|---|---|
| R3, 4 modules / 54 parent decls | 6.9 s |
| H4, 87 / 3624 | 8.5 s |
| H3, 217 / 9140 | 11.8 s |
| H2, 218 / 9229 | 12.4 s and 16.7 s |
| H1, 278 / 10663 | 14.0 s |
| R2 rerun, same 278 | 18.9 s |

A miss exports the parent whole, after building the libs in the slot. [MEASURED] 15.7 s / 20,577 rows (H2's parent, f8d04ac's tree), 18.7 s / 20,587 rows, 19.1 s / 21,366 rows. The only RSS sample is `logs/guard/export-main.log`: the same 20,577-row export, 12.48 s, maximum resident 1,600,088 kB. The plant bootstraps were not under `time`. The 1.6 GB figure is that one sample. [READ the comment, not a log I re-timed] `ppExpr` was rejected at 37 s; the kernel printer is what these exports use.

Cache entries for exporter `9880f7b79e6a` are 1.9–2.0 MB gzipped. [MEASURED `ls` of both caches]

What a fast landing pays now. The e2e (`logs/guard/e2e/out-*`) is this pre-push `--fast` on one planted file: green moved `writer_keeps_all` and exported **1 module, 37 parent decls**, no map line, `PRE-PUSH FAST GREEN`; red and stale are above. The green gate log was not kept, so the decision's "30 s, of which 21 s the gates already ran" is its number, not one I can see. The decls step on a 4-module reach is the 6.9 s above; a one-module reach is that shape, not the 12.5 s / 1.6 GB whole export.

The miss is not hypothetical for the next landing. [MEASURED] `$common/nanodregg-decls` (the main repo's git dir) holds four trees from the e2e hour. The parent key `5ff0dba` is **c066b93**'s tree, written 18:48. `2d3bf14` landed at 18:52:56, tree `b9f28415`, and that id is not in the cache. e9c126f's tree `3de07306` is not either. The built section's "pre-seeded for main's tree at e9c126f" is false. The first fast landing on current main pays the bootstrap once (parent lib build + a ~16–19 s whole export), then the reach.

## (5) The deletion

[READ the diff] Gone from `gates/rebase.py`: `active_lean_statement`, `added_theorem_statement`, `retained_added_theorem`, `missing_added_theorem`, the `missing_added_theorem` early `return True` in `lacks`, the `@@ added theorem statement absent from candidate @@` hunk, and `holds`'s call to `retained_added_theorem`. What remains of `stale` is the window (300), block containment, `merge3`, `--reverts`, the foreign-layer demand, and the `REVERTS:` note. A `.lean` module is forwarded, not refused. GATES-20p's entry is still in `decisions/gates.md`; GATES-20t is appended and says it supersedes it.

Python that still looks at Lean text, and is not this verdict:

- `gates/tree.py` `_DECL` plus `blank()`: a header scan (kind, name, header chopped at `:=`). `decls.py` uses `tree.read` for the module graph and the reach. It does not call `tree.decls`.
- `gates/journal_pilot.py`: a `^theorem ` regex, called from the journal plants, not from `pre-push` or `rebase.py`.

`decls.py` does not parse Lean source. The Lean in it is data, interpreted by `lean`.

## (6) A lie in the map

**`RESTATES: OLD → NEW` at an unrelated declaration is refused.** [READ `judge`] inequality of the two statement digests under the map is `restate not equal: RESTATES: OLD → NEW`, with the token diff. The synthetic case `restates-unrelated` is `RESTATES: Demo.B.t → Demo.B.u` on shape `X` vs `Z` and expects that string. It is the plant. It has not been executed in `logs/guard`. The same compare is what H2-/H4- measured on real statements, for a missing line rather than a lying arrow.

**`DELETES-MODULE` of a module that still exists is refused.** [READ] `unused map line: DELETES-MODULE: M (M is still a module)`. Synthetic case `module-unused`. Same: planted, not run in these logs. A module that is gone with no line is `undeclared module deletion`, not a pass.

**The residual the condition's last sentence was about.** `RESTATES-MEANING: OLD → NEW` passes whenever NEW exists, OLD is gone, and the statement digests differ. An unrelated NEW differs, so it passes, and both checks are then excused (`named` covers OLD). It cannot claim the statements are the same: that is `unused map line`, and the hint is to write `RENAMES`. No pinned map uses an arrow, and there is no synthetic case for a meaning-arrow at a decoy. This is the one unchecked correspondence left. It is labeled as a change of meaning, which is the price the guard exists to make grep-able, and it is also the constant rewrite a real cross-name change needs. It is not the `RESTATES` lie R-0034 refused.
