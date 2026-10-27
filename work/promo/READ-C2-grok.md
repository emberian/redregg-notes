VERDICT: RELEASE C2

Cross-family read of IMPACT-C2, against nano `origin/main` = `e9c126f` (fetched this session; the checkout is behind, so every blob below is `git show e9c126f:<path>`, not the working tree). No build. No edit of the tree. The candidate patch and `C2/diff-C2.txt` were read; the digest and the whole-tree log were not re-run. Tags are this read.

R-0032 and R-0033 are the shape this landing builds. R-0035 still gates the commit (the bar). This line does not lift it.

## 1. The 209, by module

Count [READ the declarations, not the impact's table]: proof modules only. `Closure.lean`, `Core.lean`, `CoreCalculus.lean`, `ClosureStatements.lean` contain no `theorem`. Deleted theorems: Judge 18 (19 declared, `weaken_never_var` moved) + Repair 16 + Outcomes 12 + Operations 13 + Soundness 14 + History 8 + Provenance 13 + HoleBridge 9 (11 declared, two moved) = 103; Core 99 + CoreInstance 6 + Typing 1 = 106. Total 209. The impact's name lists match these declarations one for one, including all 99 of `Proofs/Contextual/Core.lean`.

Lines: the 15 deleted files are 4,284 lines (C2's ten files 2,504, R3's five 1,780) [READ `C2/diffstat.txt` per-file counts, summed]. The headline 4,346 is the diff's deletion count, which also counts 62 lines taken out of survivors (the hole-model fragment, four docstrings). Not a second pile of theorems.

**(iii) none.** The audit_append class (R-0006: the only statement of a fact about a deployed object) is empty. The three theorems that would have been (iii) if deleted are moved, statement-identical: `weaken_never_var` into `Proofs/Contextual/LangInstance.lean`; `holeDecision_verified_iff` and `holeDecision_label` into `Proofs/StdHole.lean` (namespace `Nanodregg.Lang.Std`). [READ the patch hunks against `e9c126f` Judge.lean:70 and HoleBridge.lean:37–56; the `CalculusLaws` fields match `ClosureStatements.lean` except the `weaken_avoids` docstring, which drops the `drop_removes` mention.] `holeDecision_meaning` does not use them; `holeCheckedAdmission_evaluated_iff` takes the label-membership as a premise those two discharge. Deleting them would have been the precedent. Moving them is the precedent.

### (i) — abstract statement, deployed tooth already over `selectHole`

Outcomes: `strengthening_sound` (teeth `strengthening_factor` :53, `kept_context` :69), `suspended_sound` (`used_hypothesis_suspends` :93, `cell_support_dead_refused` :117, plus `selectHole_cell_support` / `revoked_support_refused`), `alternative_sound` (`alternative_same_filling` :77), `replacement_sound` (`replacement_filling` :85). [READ `LiveJourney.lean` and `Journey/Contextual.lean` `declaration` / `view`.]

History: `select_requires_available` → `selectHole_origin` (`LiveHoles.lean` proofs :50; every support of the selected code is live, `s.original = c.body`). `reissued_support_unverified` → `revoked_support_refused`.

Judge: `judge_verified_iff` is the abstract shape of `selectHole_origin` plus T4 below. It is not a fact about `judge` that the deployment still has: `selectHole` does not call `judge`.

### (ii) — CMTT core, superseded by a theorem over real terms (R-0022)

Core proofs, the ones with a deployed counterpart I confirmed still declared at `e9c126f`: `subst_lemma` → `substList_typed` (`Proofs/Subst.lean:531`); `msubst_lemma`, `hasTy_msubst_gen`, `hasTy_msubstP` → `fillHoles_typed` (`Proofs/Fill.lean:123`) and `langLaws.msubst_lemma`; `strengthen`, `hasTy_unshiftAt`, `strengthen_needs_unused` → `hasType_unshiftAt_live` (`Proofs/Subst.lean:389`); `shiftAt_unshiftAt` → `Term.shiftAt_unshiftAt` (`Proofs/Subst.lean:280`); `infer_sound`, `infer_complete`, `check_sound`, `check_complete`, `inferL_sound`, `inferL_complete` → `infer_sound` / `infer_complete` / `inferE_sound` (`Proofs/Check.lean:313–345`); `subject_reduction` → `step_preserves` (`Proofs/Sound.lean:216`); `step_deterministic` → `bigStep_deterministic` (`Proofs/BigStep.lean:104`). CoreInstance: `cmttLaws` → `langLaws` (the instance that remains). These are about the toy `Tm` (`box` / `letbox` / `mvar`). `Core.lean`'s proofs import `Proofs/Index` and `Proofs/Contextual/Typing` only [READ].

`bell_resume_computes` / `bell_resume_toy` are that toy (`bellK := .box`, `bellResume := .letbox`), not the resident Bell. The resident's facts are elsewhere (`deployed_cycle_*`, `Hosting/Proofs/ResidentRun`). Not (iii).

### (iv) — the rest

Everything else in those 209. Feeders and list lemmas of `judge` / `repair` / `Session` / `Monomial`, the CMTT renaming algebra, every `*_toy`, `box_cannot_capture*`, `letbox_needs_box*`, `HasTy.mvar'`, `holeEnv_*`, `bell_template_toy`, `cmtt_strengthen_toy`.

Named so they are not later called (iii):

- `drop_removes`. Its premise `weaken x (var x) = var x` is false at `langData` (`weaken` is `renameVar (liftIdx x)`, and `liftIdx x x = x + 1`) [READ `LangInstance.lean` `langData`, `Index.lean:12–15`]. It says nothing about `Term`. `weaken_never_var` stays.
- `withdraw_never_refutes`, `token_edit_conflict_iff`, `withdraw_never_refutes_closure`. True of `judge` (conflict reads the checker and the guard env, not a token) and false of `selectHole`: `runHoleGuard` reads the guard pin's liveness, so withdrawing that pin can return `guardBlocked` [READ `LiveHoles.lean:157–166`]. Deleting a theorem the deployment refutes is the point of the other branch.
- `conflict_illTyped_refutes`, `judge_conflict_iff`. No deployed producer. Typing of a candidate is `HoleROM.check` (`inferE Δ h.ctx`, `LiveHoles.lean:67–77`) and `instantiateHoles`'s `checkE`. Those theorems do not mention `judge`.
- HoleBridge's nine deleted theorems. `hole_select_iff` / `hole_fill_iff` / `hole_rejudge_status` quantify over `Closure.select` / `fill` / `rejudge`, not the generated methods [READ the bodies]. `hole_judgment_admission_bridge` and `holeAdmission_judge_iff` equate a `BigStep` of `holeCheckedJudge` / `holeVerdictCheck` to `judge = .verified`. The `BigStep` half is already `holeCheckedAdmission_evaluated_iff` (`Proofs/StdHoleCoverage.lean:143`), which HoleBridge imports and which does not import HoleBridge. `holeModel_*` is about `holeModelCandidate`, deleted with the fragment, and `LangInstance.lean`'s own header says no deployed module imports it.
- `consumer_boundary`, `Consumer`, `Consumer.holds`. C6's deletion half. No consumer. The deployed boundary is the definitions `holeSignature` / `Package.holeCharge`, not this theorem.
- Repair 16, Operations 13 + `Grows`, Soundness 14, Provenance 13, History's `executed_prefix_blocks_replan` and three `session_preserves_*` / `fromScratch_wellFilled`, Judge's `judge_congr`, `judge_frame`, `blockers_empty_iff`, `missing_empty_iff`, `judge_pruned`, `withdraw_never_prunes`, `hyp_var_cites`, `set_live`, `reissue_never_reenables`, `find_*`, Outcomes' five acceptance/lookup helpers. Kernel at-most-once and the row machine's `pruned` (`holeVerdictLabel`, `StdHole.lean:101`) do not depend on them.

Reverse deps [READ `C2/moddeps-base.tsv`, 15 lines]: of the constants defined in the 15 modules, the only users outside them are `langData`, `langLaws`, `lang_strengthen_toy`, `lang_template_toy`, and the hole-model fragment. That fragment is deleted. The four that remain follow `CalculusData` / `CalculusLaws`, which move. A deployed importer would be a row. There is no row.

## 2. The protocol calculus

[READ imports at `e9c126f`.] `Protocol.lean` has no `import` and no occurrence of `Closure`, `Core`, `CalculusData`, or `cmtt`. `NanoBridge.lean` imports `Lang.Contextual.Protocol` and `Hosting.Resident.Trace` — not Core. `ProtocolTyping.lean` imports `Protocol`. `Negotiation.lean` imports `Proofs/Contextual/Protocol`. `Proofs/Contextual/Protocol.lean` imports `ProtocolTyping`, `NanoBridge`, and `Hosting.Proofs.ResidentRun`. `ResidentRun` imports `Resident.Trace` and `Proofs/Resident`. `Trace` imports `Resident.Run`. None of those is a deleted module. The patch does not touch them. `Lang/Contextual` after this landing is LangInstance + Protocol + NanoBridge; the proof side is LangInstance + Protocol + ProtocolTyping + Negotiation. That is R-0021.

They were not rebuilt here (the read forbids it). [INFERRED they still build: the cone does not name a deleted module, and the builder's whole-tree log is the measurement of the candidate.]

## 3. C3, C4(a), C5 as statements

Not in this landing (the patch adds no `selectHole_*` theorem). Judged as the statements in `C2/C5-statements.lean`.

**T2 `selectHole_hypotheses`.** Nano object: `changedHypotheses` inside `selectHole` (`LiveHoles.lean:144–154`), the `strengthened` field. Weaker without it: nothing general. `selectHole_origin` does not mention `strengthened`. `kept_context` is one ROM (`strengthened = []`); the journey row `kept-context` checks `isEmpty` [READ `Journey/Contextual.lean:139`]. Disjunct: no hash-collision disjunct. The `∀` is vacuous only when every hypothesis is `none`; the fixture's are `some`, and both directions of the `↔` are inhabited (live pins kept, dead unused pins removed). Not a rename of `used_hypothesis_suspends`. The impact's m1, m4, m5 are already red at that tooth, at `strengthening_factor`, and at `kept_context` respectively — a global edit of `changedHypotheses` hits the one ROM those teeth run. The mutation they do not catch: a dead unused hypothesis pin that is a `.cell`. Every tooth's hypothesis pin is a `.row` (`factPinAt`); `withCell` puts the cell in `c.supports`, which refuses at `supportDead` before `changedHypotheses`. Special-case `.cell` to not append, and every LiveJourney tooth stays, `selectHole` still returns `.ok`, and T2's `↔` is false. That is the plant.

**T3 `selectHole_factor`.** Nano object: `factorHole` plus the re-embedding `selectHole` applies (`LiveHoles.lean:170–177`, `:206–208`). `hchk` is `HoleROM.check`, which `instantiateHoles` runs first; a premise of the new theorem, not a new hypothesis on a landed one. Weaker without it: `selectHole_nodes` has `Term.nodes s.body = Term.nodes s.original` only; `instantiateHoles_typed` types the package after `checkE` and stays true if a wrong body fails that check, or if a wrong body of the same type passes it. Disjunct: a conjunction, both conjuncts inhabited on the fixture (`strengthening_factor` has `body = .var 1 = original` and `inferE` at the reduced context). Not a rename of that tooth and not a rename of `CalculusLaws.strengthen_factor` (one variable, abstract, and it stays). The impact's m2 is already `strengthening_factor` (unfiltered embedding sends `.var 1` to `.var 0`). m6 is already `replacement_filling`: that tooth strengthens two positions (`view (some 2) none (used := none)`, body `.nat 9`, context `[]`); folding `removed` instead of `removed.reverse` leaves a nonempty context. The impact's "one position" understates the teeth. The mutation they do not catch: no tooth has `removed` nonempty and two variables kept (strengthen keeps one, replacement keeps zero, the others remove nothing). A closed `.nat` does not consult the embedding. Point the second kept variable at 0 only in that case: teeth stay, node count stays, `HasType` stays if the two kept variables have one type, `s.body = s.original` fails. That is the plant. [INFERRED the equality holds on the fixture, by the teeth's `rfl`; I did not elaborate the general statement.]

**T4 `selectHole_live_selects`.** Nano object: `selectHole` as a function, the completeness direction `selectHole_origin` does not have. The premises are the refusal arms (`unpinned`, `selectionAbsent` / `Type` / `Index`, `derivationMoved`, `supportDead`, `supportMoved`, `guardBlocked`, `guardFault`), read off the definition; they are not binders added to a landed theorem. Disjunct: an implication whose premises are jointly inhabited (`strengthening_factor`'s view selects). Not a rename of `cell_support_live_selects`. m7 (refuse every dead hypothesis, used or not) is already `strengthening_factor` and `replacement_filling`. `kept_context` does not see it: both of its pins are live. The mutation the teeth do not catch: refuse when the guard pin is live, before the guard term runs. The fixture guard is `.ite (.var 0) (.bool false) (.bool true)`, so it returns true only when the pin is dead, and every success tooth uses `blocker := none`. A ROM with `guard := .bool true` and a live pin selects today and is refused by the mutation; T4 says it selects; no tooth has that guard. That is the plant.

**C4(a): docstring.** No `environment` field, no `selection_monomial_sound`. Nano object would have been the receipt. Nothing reads it: `Program.lean:222` keeps `(instantiateHoles …).map (·.body)`; `instantiateHoles_sources` reads `original.digestLits`, not a monomial. The product "supports ++ used hypothesis pins, all live" is `selectHole_origin` plus T2. A theorem of it is a rename. Adding the field would be the plan's price on `selectHole_origin`, `selectHole_nodes`, `resolutionMax_committed` (the constructor in `selectHole`'s `pure ⟨…⟩` changes). Trigger, as the impact says: a reader of the receipt. [READ]

**C3: docstring, plus the move already in this landing.** The row-grain label is `holeVerdictLabel` (`StdHole.lean:101–107`), read by the moved `holeDecision_verified_iff` and tied to the generated term by `holeDecision_meaning` (`Proofs/StdHole.lean:65`). A new `live_label_iff` is that pair renamed. A ROM label (indices for which T4's premises hold now) has no reader: `Hosting/Resident/Bell.lean` does not mention a hole or a candidate [READ]; the impact's Hosting/Host grep is theirs [MEASURED there]. Lands when a tick reads it. Not before.

`cellLive_pinned` stays out. No `kernelWorld` on this branch, and C9 already made it a docstring (R-0031). Its fact is `selectHole_cell_support`.

§8.2: −209 in this landing, +0 here. The +3 is C5's card, and only with the three plants above. m1–m7 do not justify them.

## 4. Price

No landed theorem gains a hypothesis. [READ the patch: survivors' edits are docstrings (`HoleDecl`, `Index`, `Proofs/Index`, `Subst`), the `CalculusData` / `CalculusLaws` / `weaken_never_var` moves with the same fields and the same statement, the hole-model deletion, and the two `holeDecision_*` moves with the same statement and a new docstring. `langData`'s body is unchanged. `langLaws` is unchanged.] The digest is the builder's [MEASURED `C2/diff-C2.txt`]: before 51,346, after 49,512, vanished 1,834 all declared, new 0, type-digest changed 0, value-hash changed 0, 45 module moves all out of a module this step moves. I did not re-export it. Under the §8.1 reading the bridge would have landed with a2, a6, a7; it is not in the patch.

Host closure 89 at `e9c126f` [READ `SIZE.md`]. The patch touches no Host file. The deleted modules are not in that closure: nothing outside the two LangInstance modules uses them (§1), and LangInstance's header is right that no deployed module imports it. After = 89 is the builder's measurement; the before and the import fact are this read.

Journey byte-identical is the same shape. The patch touches no `Journey`, `Codec`, `Emit`, or `Host` file, and the exe does not import `Lang.Contextual.LangInstance`. [INFERRED the binary does not relink; the empty `diff` of the two journey logs is the builder's MEASURED, not re-run.]

## 5. One landing

One landing. The import edge is real and I checked it: `CoreCalculus.lean` imports `Closure` (`cmttData : CalculusData`), `CoreInstance.lean` imports `ClosureStatements` (`cmttLaws : CalculusLaws …`). A Closure-only commit would repoint those two imports onto the moved `CalculusData` / `CalculusLaws` and then the next commit would delete them. That intermediate is not a concept anyone bisects: it is the toy core standing on the surviving calculus for one commit, during which "langLaws is the only instance" is false. R-0032 already allows the same landing or the next. Splitting would make a shape whose only purpose is to be deleted, which is the thing this branch is deleting.

The record is the decision, not a second hash. LANG-75.3 and the commit message name both rulings and both counts (103 of the closure, 106 of the CMTT core), and do not say the closure was 209 theorems.

## What the decision says

- R-0032 / R-0033: the other branch, this shape. `Closure.lean` deleted whole. `CalculusData` beside `langData`. `CalculusLaws` and `weaken_never_var` beside `langLaws`. The two `holeDecision_*` re-homed, not deleted.
- R-0022 in the same commit: the five CMTT files. No (iii) left behind.
- C3 and C4(a) are docstrings. C5's three statements are not docstrings and are not this commit; their plants are the three mutations in §3, not m1–m7.
- Price 0. Host closure 89. Journey not relinked.
- R-0035 still holds the commit until the bar diagnosis says otherwise.
