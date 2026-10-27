# STATEMENTS — readers' B5, "statements weaker than their names" (nanodregg)

Brief: readers/COLLATION-20261024.md §B5, the READ-*.md memos; WORK-RULES-20261027. Worktree hbox `~/nd-land/statements` (from origin/main 9c170a8b, rebased onto 9c0e51e8); lander dir `~/nd-land/statements-land`.

## 2026-10-27

- READ each B5 statement on the tree at 9c170a8b. Table below: (a) already strengthened by a later landing (hash), (b) strengthened here as a composition of existing lemmas, (c) a design matter (cv task).
- BUILT (one `lake build` of the changed modules and the Host refinement, `swarm-build` 6G, 2 threads): 224 jobs green. Then `scripts/commit` (ND_LAND_DIR=~/nd-land/statements-land) built the touched libs (Kernel Protocol Host Lang Codec Hosting Ledger Spec, 518 then 422 jobs) green; no row touched.
- First landing attempt: CONFLICT in decisions/kernel.md (KERNEL-71 appended upstream meanwhile); rebased, kept both entries, relanded (rebuilt over LANG-89's generator changes, green).
- LANDED on origin/main: **979b6c51** lang (LANG-98: take/fuse/escrow iffs at `apply4`, teeth restated, `live_row_authenticated`, `ofData_iff_conforms`), **b34be3de** kernel (KERNEL-76: `admit_row_touch` + `admit_keep_row`, `refuse_admissible`, Refine docstrings), **f20a5444** protocol (`command_size`, `commandFrame_argv_within`), **98006f96** spec README (`NoRef` gloss).
- Coordination: SPEC.report.md line (the README `NoRef` gloss).
- Hazard met (worth the next lane knowing): the session scratchpad holds ANOTHER agent's nanodregg copy at `scratchpad/nd/` (a `base` commit plus uncommitted Protocol/Rows/Adversary work). My first `scp` landed seven files in it; I restored the two that differed from its base with `git checkout` (StdOffer.lean, StdOfferFuse.lean; the other five were byte-equal to its base). Its own uncommitted edits to Loopback.lean, lakefile.lean, Adversary*.lean were untouched. My staging moved to `scratchpad/statements-lane/`.

| B5 item | verdict | what |
|---|---|---|
| `take_iff_compliant` in a doubled env, docstring says "as the receiver applies it" | (b) | restated over `apply4 g "take"` at `[req, arg, state, rows]`, premises `hlib`/`hf` (what `load_top` gives); the seven refusal teeth and `fuse_refused_disjoint` restated at the same grain; `method_app` deleted. Via `offerTakeTree_decides` + `apply4_method_iff` (new). LANG-98. |
| the fuse has only `fuse_run_sound` since e7c2b13 | (b) | `fuse_iff_compliant` (Std.offer), and the escrow's too: `escrow_take_iff_compliant`, `escrow_fuse_iff_compliant` (`∧ LegsMatch`) via `offerTakeTree_decides_fair` + `escrowFair_eval`. LANG-98. |
| no authentication theorem for a live RANGE read | (b) | `live_row_authenticated` (Lang/Proofs/Rel.lean): the range twin of `cited_authenticated`, from `rangeRowData_getElem` + `keyColumns_ok`. LANG-98. |
| `EscrowLegMoved` omits the X/Y coupling | (a) 0829f4ec (LANG-82) | `EscrowLegMoved … P o q` takes the two offers as parameters and `escrow_fuse_admitted` concludes `∃ ox oy, EscrowLegMoved … x' ox oy ∧ EscrowLegMoved … y' oy ox`. |
| `audit_ok` close to a restatement | skip | deleted by HOST-78 (per brief). |
| `admit_row_touch` says nothing for a `keep` | (b) | conclusion gains `r0.get … (.row key) = rowAt E w.rows (.row key)` (and `foldRows_touch_get` the same); `rowStep_keep`, `admit_keep_row` new. KERNEL-76. |
| the live-backup theorem models one append-only file that retention breaks | (c) | cv 01a17c30-bde2: a multi-file Store model with the retention seal as a step, or a retention-safe `backupOrder`. |
| the open theorems cover the pure open, not the deployed path | (c) | cv 01a17c30-be07: `openAt` as (IO read into a snapshot) then `Id.run (openWith …)`, so the deployed open IS the proved one. |
| the `Honest` half of the Host refinement with no tooth known to fire | (b) | `Kernel.Receive.refuse_admissible` (new Kernel/Proofs/RefuseAdmissible.lean): for a call `judge` admits, with refusal budget left, `World.refuse` accepts `refusedOf X c v`, so `host_step_folds_tooth_censor`'s premises hold together; Refine's docstrings now cite it. KERNEL-76. |
| `Conforms`/`ofData`: one inclusion named, no iff | (b) | `ofData_iff_conforms` (Lang/Proofs/Data.lean): `(∃ x, Wire.ofData T d = some x) ↔ Conforms d T` at `T.wf`. |
| `argvSize` not tied to the command codec's size | (b) | `command_size` (the codec's size of a command payload is `argvSize` of its argv) and `commandFrame_argv_within` (Protocol/Proofs/FrameFit.lean). |
| refinement census drops premises | skip | deleted with the judge (per brief). |
| Spec/README.md's `NoRef` gloss "laws without holes" | fixed | `NoRef` = no `ref` anywhere, holes allowed; says what B3's chain clause does not cover (CRIT-SPEC). SPEC.report.md line. |

Stale comments fixed on the way (they lied about the code below them, READ-LANGPROOFS F7): StdOffer's header ("its matcher", "The matcher's code is not a premise"), StdOfferEscrow's header ("`fuse` makes no row act").

Not done, named: the run-grain converse of `take_run_sound` (needs a completeness lemma for the machine at `Bounds.stackMax`), so the iffs are the strongest TERM statements, not run statements (LANG-98's critique).
