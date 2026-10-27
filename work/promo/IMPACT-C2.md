# IMPACT-C2 — the other branch: the abstract closure leaves Lang; the CMTT core (R3) with it; C3/C4a/C5 restated over `selectHole`

Worker: CX-PROMO-2 (successor of CX-PROMO). 2026-10-22. Base: nano main `e9c126f` (hbox `wt/promo`). Rulings: R-0032
(the other branch), R-0033 (its shape). Plan: PROGRAM-20261022 §3 P2 (C2, R3, C5, C4a, C3, C6), §8.1, §8.2.
Spec read: `promo/READ-C2M-grok.md` (§4 is the shape).

The candidate was BUILT for measurement while this file waits for its read (predecessor's lesson 6: building for
measurement is fine, the read decides). Every number tagged MEASURED was taken on that candidate in hbox
`wt/promo`; artifacts are in `promo/C2/`.

## 0. Answer first

- **Deleted, 15 modules, 4,346 lines, 209 theorems** [MEASURED `C2/diffstat.txt`; SIZE theorems 6,075 → 5,866]:
  `Lang/Contextual/{Closure, Core, CoreCalculus}.lean`, `Lang/Proofs/Contextual/{ClosureStatements, Judge, Repair,
  Outcomes, Operations, Soundness, History, Provenance, HoleBridge, Core, CoreInstance, Typing}.lean`, plus the
  hole-model fragment of `Lang/Contextual/LangInstance.lean` (`holeModelCandidate`, `holeLive`, `holeBlocked`,
  `holeModelIface`, `holeModelTemplate`). C2's part: 2,504 lines of deleted files / 103 theorems; R3's part: 1,780 lines / 106.
- **Moved, statements byte-identical** [MEASURED]: `CalculusData` (+ its `DecidableEq` instance) →
  `Lang/Contextual/LangInstance.lean` beside `langData`; `CalculusLaws` + `weaken_never_var` →
  `Lang/Proofs/Contextual/LangInstance.lean` beside `langLaws`; `holeDecision_verified_iff`, `holeDecision_label`
  (HoleBridge's Std.hole half: they read no closure object) → `Lang/Proofs/StdHole.lean`, namespace
  `Nanodregg.Lang.Std` (the only two RENAMES).
- **R3 rides in this landing**, not the next: `CoreCalculus.lean` imports `Closure.lean` and `CoreInstance.lean`
  imports `ClosureStatements.lean`, so deleting Closure without R3 would mean re-homing `cmttData`/`cmttLaws` onto
  the moved `CalculusData` for one landing, then deleting them (a second shape for a day). [READ the imports]
- **Digest diff** [MEASURED `C2/diff-C2.txt`, base digest under the 2-row rename map]: before 51,346 constants,
  after 49,512; vanished 1,834, every one declared (UNDECLARED 0); **new 0; type-digest changed 0; value-hash
  changed 0**; 45 module moves, every one out of a module this step moves code from. Nothing that survives changed
  its statement or its proof term.
- **Reverse deps** [MEASURED `C2/moddeps-base.tsv`, exporter over every module at `e9c126f`]: of the 1,871 constants
  defined in the 15 modules, the ONLY users outside them are the two `LangInstance` modules: `langData`,
  `langLaws`, `lang_strengthen_toy`, `lang_template_toy` (through `CalculusData`/`CalculusLaws`, which move) and the
  hole-model fragment (deleted). No deployed module, no journey, no gates table, no other layer.
- **Premise price: 0.** No surviving theorem gains a hypothesis or a binder (type-digest changed 0).
- **Host closure 89 → 89** (no `Lang.Contextual` module was ever in it) [MEASURED `gates/size.py --write`]; Lean
  modules 491 → 476; proof-modules 264 → 252; Lang lines 42,153 → 37,910; max dependents 347 → 346.
- **Whole-tree build GREEN** (740 → 725 jobs) [MEASURED `logs/promo/c2-cand-whole.log`]; `gates/check.py` all ok
  [MEASURED `C2/check-cand.log`]; `lang-journey` GREEN and byte-identical to C9's run (the exe was not relinked:
  no compiled input changed) [MEASURED `diff j-c9.txt c2/journey-cand.txt` empty]; codec vectors untouched (no
  Codec/Emit/wire file changes). **Gate: `lang:` fast** (no wire byte moves) + the whole-tree build above.
- **C5, C4a, C3 restated over `selectHole`** (§6): three new theorems for C5 (`selectHole_hypotheses`,
  `selectHole_factor`, `selectHole_live_selects`), each elaborated as a statement with `sorry` and NO hypothesis
  beyond the deployed objects [MEASURED `C2/C5-statements.lean`: three `sorry` warnings, no error], each with a
  deployed mutation no landed theorem catches in general. C4a: no `environment` field (no reader of the receipt);
  its monomial is `selectHole_origin` + `selectHole_hypotheses`, a docstring. C3: the row-grain live label is the
  moved `holeDecision_verified_iff`; no ROM label theorem (no tick consumer). They land in their own cards.
- `cellLive_pinned` (built once for C9) does **not** land: under this branch there is no `kernelWorld`, so C2 has no
  World for it to pin. Its fact (a live cell was pinned) is `selectHole_cell_support` already.

## 1. Every deleted statement, by name, with its successor or its reason

Theorems (209). "Teeth" = the closed instances in `Lang/Proofs/LiveJourney.lean` (`strengthening_factor :53`,
`kept_context :69`, `alternative_same_filling :77`, `replacement_filling :85`, `used_hypothesis_suspends :93`,
`cell_support_dead_refused`, `cell_support_unpinned_refused`), which stay. T2/T3/T4 are C5's new theorems (§6).

### 1.1 `Lang/Proofs/Contextual/Judge.lean` (19; 1 moved, 18 deleted)

| name | successor / reason |
|---|---|
| `judge_verified_iff` | T4 (`selectHole_live_selects`, ←) + `selectHole_origin` + T2 (→): the deployed verified judgment IS a successful `selectHole`. |
| `judge_congr`, `judge_frame` | `judge` is deleted; `selectHole` is a function of `(digestOf, look, rv, self, h)` and reads nothing else (definitional); the kernel side is `receive_congr`. |
| `blockers_empty_iff`, `missing_empty_iff` | list lemmas of `judge`'s arms; no successor needed. |
| `judge_conflict_iff`, `conflict_illTyped_refutes` | the deployed run never re-checks a candidate: typing is install-time (`HoleROM.check`, `Package.checkContextual`) and instance-time (`instantiateHoles_typed`); READ-C2M (a7): `conflict illTyped` has no deployed producer. |
| `judge_pruned`, `withdraw_never_prunes` | a `HoleROM` has no blockers (READ-C2M §3); the row machine's `pruned` is `holeVerdictLabel`'s, covered by `holeDecision_verified_iff` (moved). |
| `hyp_var_cites` | T2's second conjunct: a used hypothesis's pin must hold (`used_hypothesis_suspends` the tooth). |
| `withdraw_never_refutes`, `token_edit_conflict_iff` | **no deployed counterpart, and false of the guard**: the deployed guard reads its pin's liveness (`runHoleGuard`), so a withdrawal of the guard pin CAN produce `guardBlocked`. For candidate supports the deployed fact is the refusal NAME (`supportMoved`/`derivationMoved`/`supportDead`, never `guardBlocked`), which is `selectHole`'s text. |
| `set_live`, `reissue_never_reenables` | `World`/`Token` deleted; the deployed liveness is `cellLive` over the pinned view (E1); a re-issue is a new cell id, a revoked cell stays a tombstone (KERNEL-60). |
| `find_name_self`, `find_self`, `find_some` | `Closure.find` helpers. |
| `drop_removes` | **vacuous at the one instance**: its premise `weaken x (var x) = var x` is false at `langData` (`liftIdx x x = x + 1`); its own docstring says it covers only named-variable calculi (the CMTT toy, deleted by R3). The general form `weaken_never_var` stays. |
| `weaken_never_var` | MOVED to `Lang/Proofs/Contextual/LangInstance.lean`, statement identical (laws-only). |

### 1.2 `Repair.lean` (16)

`judge_restatus`, `restatus_self`, `repairPass_fst`, `repairCands_map`, `repairPass_snd`, `repairCands_eq`,
`repairHole_cands`, `repair_slot`, `repair_agrees_from_scratch`, `repair_coherent`, `fromScratch_coherent`,
`repair_carries_untouched`, `locality`, `withdraw_never_refutes_closure`, `iface_eq_of_name`,
`repair_rejudged_eq_touched` — **reason**: nano has no repair function and no stored status. A selection is
recomputed on every invocation from the caller's pinned view (`selectHole`: "Selection is fresh on each
invocation"), so "incremental repair agrees with from-scratch" is true by construction: there is only
from-scratch. The Std.hole row machine's recorded status is advisory and re-read by `rejudge`
(`holeStatusOf_meaning`).

### 1.3 `Outcomes.lean` (12)

| name | successor / reason |
|---|---|
| `strengthening_sound` | T2 (exactly the dead hypotheses are strengthened, none used) + T3 (the factor types at the smaller context and re-embeds to the ROM code); teeth `strengthening_factor`, `kept_context`. |
| `suspended_sound` | T2's second conjunct + `revoked_support_refused` + `selectHole_cell_support`; teeth `used_hypothesis_suspends`, `cell_support_dead_refused`. |
| `alternative_sound` | tooth `alternative_same_filling` + T3 (`s.body = s.original`: two codes with one body run one body). The deployed "alternative" is the chooser re-pointing the selection row, not an automatic reselect. |
| `replacement_sound` | tooth `replacement_filling` + row P8.3 (the chooser's `choose_code` Turn selects the second provider's code). A replacement is a chooser's Turn, offered by nothing. |
| `repair_keeps_accepted`, `repairHole_accepted`, `repairSelected_accepted` | acceptance is executed history: the kernel's at-most-once (rows P8.4 replay / committed artifact / competing use). |
| `findIx_some`, `findIx_none`, `isVerified_iff`, `repairHole_some`, `rejudged_get` | helpers of `reselect`/`repairSelected`. |

### 1.4 `Operations.lean` (13 + `structure Grows`)

`update_at`, `propose_ok`, `select_ok`, `deselect_ok`, `accept_ok`, `prune_ok`, `rejudge_eq`, `fill_ok`,
`Grows.trans`, `repair_grows`, `propose_grows`, `select_grows`, `history_is_prefix` — **reason**: the abstract
session operations. The deployed operations are Std.hole's generated methods (`propose/select/fill/accept/prune/
rejudge`, `Lang/StdHole.lean`); their admission is `holeCheckedAdmission_evaluated_iff` ∘ `holeDecision_verified_iff`
(select/fill admit exactly when observation is complete and the label is verified) and `holeStatusOf_meaning`
(rejudge); the history is the kernel's append-only log.

### 1.5 `Soundness.lean` (14)

`conditional_soundness`, `derivable_of_wellFilled`, `conditional_soundness_closure`, `find_eq_of_mem`,
`update_preserves`, `slotFilled_set`, `repairCands_getElem?`, `repairHole_slotFilled`, `repair_wellFilled`,
`propose_wellFilled`, `select_wellFilled`, `op_preserves_wellFilled`, `fill_preserves_derivable`,
`op_preserves_coherent` — **successor**: `instantiateHoles_typed` (the filled package types at its interface, the
closing `checkE`) with `fillHoles_typed` / `langLaws.msubst_lemma` (the deployed `Derivable`).

### 1.6 `History.lean` (8)

| name | successor / reason |
|---|---|
| `select_requires_available` | `selectHole_origin` (every support holds) + T2 (every used hypothesis holds). |
| `reissued_support_unverified` | `revoked_support_refused` (a tombstoned cell refuses by itself). |
| `executed_prefix_blocks_replan` | kernel at-most-once, rows P8.4. |
| `consumer_boundary` | C6: `Consumer` has no consumer; the deployed boundary is typing + cost (`holeSignature`, `Package.holeCharge`), C6's docstring. |
| `session_preserves_coherent`, `session_preserves_tpl`, `session_preserves_wellFilled`, `fromScratch_wellFilled` | sessions deleted (§1.4). |

### 1.7 `Provenance.lean` (13)

`monomial_verified`, `provenance_iff`, `monomial_complementary_dead`, `provenance_complementary_dead`,
`eval_consistent`, `subsumes_iff`, `subsumes_trans`, `subsumes_eval`, `minimal_subset`, `minimal_eval`,
`minimal_covers`, `provenance_minimal`, `label_iff` — **reason** (C4a/C3, §6): a ROM candidate has no blockers and
no environment literal (cost and guard are per hole, not per candidate), so its monomial is one positive product:
`c.supports` ++ the pins of the hypotheses `c.body` uses; `selectHole_origin` + T2 say a selection's product is all
live. The row machine's label is `holeVerdictLabel`, its live reading `holeDecision_verified_iff` (moved). The ROM
label (the indices selectable now) has no reader.

### 1.8 `HoleBridge.lean` (11; 2 moved, 9 deleted)

`holeDecision_verified_iff`, `holeDecision_label`: MOVED (RENAMED into `Nanodregg.Lang.Std`), statements
identical. `holeModelTemplate_typed`, `holeModel_verified_iff`, `holeAdmission_judge_iff`,
`holeJudge_fixed_observations`, `hole_judgment_admission_bridge`, `hole_judgment_admission_fixed_observations`,
`hole_select_iff`, `hole_fill_iff`, `hole_rejudge_status`: the closed-fragment bridge to `judge` (plan C2:
"deletes `hole_judgment_admission_bridge`'s closed-fragment premises"; `hctx : I.ctx = []`, `hhyps : I.hyps = []`
were the fragment). **Successor of the deployed half**: `holeCheckedAdmission_evaluated_iff`
(`Lang/Proofs/StdHoleCoverage.lean`) with `holeDecision_label` discharging its `hl` and `holeDecision_verified_iff`
reading `l = "verified"`: admission ↔ complete observation ∧ allowed ∧ ¬blocked ∧ both probes live. No composite
theorem is added (it would be a rename of the two).

### 1.9 R3: `Lang/Proofs/Contextual/{Core (99), CoreInstance (6), Typing (1)}.lean`

**Reason** (R-0022, plan R3): `Term.hole n σ` IS `clo(u,σ)`; `HoleCode.body` is `box` at ROM grain. Successors of the
CMTT theorems that have a deployed meaning: `subst_lemma` → `substList_typed` (`Lang/Proofs/Subst.lean:531`, Thm
4.2); `msubst_lemma`, `hasTy_msubst_gen`, `hasTy_msubstP` → `fillHoles_typed` (`Lang/Proofs/Fill.lean:123`, Thm 4.3)
and `langLaws.msubst_lemma`; `strengthen`, `hasTy_unshiftAt`, `strengthen_needs_unused` → `hasType_unshiftAt_live`
and T3; `shiftAt_unshiftAt` → `Term.shiftAt_unshiftAt`; `infer_sound`/`infer_complete`/`check_sound`/
`check_complete` (+`inferL_*`) → `Lang.infer_sound`/`infer_complete`, `inferE_sound`; `subject_reduction` →
`step_preserves` (`Lang/Proofs/Sound.lean:216`); `step_deterministic` → `bigStep_deterministic`
(`Lang/Proofs/BigStep.lean:104`); `cmttLaws` → `langLaws` (THE instance). The rest are CMTT-internal
(renaming/substitution algebra of the toy `Tm`, `box`/`letbox`/`mvar` blocking, `bell_resume_*`, every `*_toy`):
`rename_rename renameL_renameL rename_id renameL_id mren_mren mrenL_mrenL mren_rename mrenL_renameL substFn_rename
substFnL_renameL rename_substFn renameL_substFnL mren_substFn mrenL_substFnL substFn_substFn substFnL_substFnL
substFn_var substFnL_var substFn_congr substFnL_congr ofList_nil subst_nil ofList_getElem? ofList_comp subst_comp
hasTy_rename hasTy_weaken hasTy_weaken_append hasTy_mren hasTy_mweaken hasTy_substFn shiftSub_length
shiftSub_getElem? ofList_shiftSub hasSubst_shiftSub hasSubst_id hasSubst_proj MEnv.cons_insert MEnv.cons_eq_insert
hasTy_uses_lt hasSubst_nil hasSubst_cons box_cannot_capture box_ambient_free box_cannot_capture_toy mvar_blocked
subst_keeps_blocked msubst_mvar_self msubst_unblocks msubst_other_blocked mvar_blocked_toy subst_lemma_toy
subst_comp_toy msubst_lemma_toy letbox_toy strengthen_toy weaken_toy hasTy_beta lam_no_step no_step_under_box
no_step_under_box_toy var_no_step mvar_no_step letbox_needs_box letbox_needs_box_toy letbox_needs_box_toy_typed
bell_resume_computes bell_resume_toy tm_decEq_toy check_toy rename_congr renameL_congr unshiftAt_toy msubstPL_eq
uses_rename usesL_renameL uses_shiftAt renameL_eq mrenL_eq substFnL_eq msubstL_eq usesL_of_getElem? usesL_true`,
`holeEnv_nil holeEnv_filter holeEnv_some bell_template_toy cmtt_strengthen_toy`, `HasTy.mvar'`. Drops cv task
01a1587d-9a98 by name (its trigger moves to `Lang.Term`).

### 1.10 Definitions

- `Closure.lean` (deleted): `Token, World, World.set, Edit, Edit.apply, reissue, applyAll, Party, Iface, Iface.decl,
  Evidence, Status, Obligation, Candidate, Slot, Slot.empty, Event, Outcome, Refusal, Template, Closure, effSupports,
  deps, judge, EnvLit, EnvLit.eval, Monomial, Monomial.envOK, Monomial.eval, monomial, provenance,
  Monomial.consistent, Monomial.subsumes, minimal, label, touches, hypOf, holeTouched, Closure.find,
  Closure.selectedCand, Closure.sigma, Closure.support, holeObligations, Closure.Φ, observe, Closure.update, propose,
  select, fill, deselect, accept, prune, rejudge, findIx, repairPass, repairCands, rejudgedIn, suspendObligations,
  isVerified, keptOutcome, reselect, repairSelected, repairHole, Outcome.event, repair, withdraw, fromScratch, Op,
  Op.run, Op.next, Session.run, Consumer, Consumer.holds` — the abstract closure; R-0033: every one exists only to
  feed `judge`/`Status`/`provenance`. `Consumer`/`Consumer.holds` are C6's deletion half (no consumer).
  `CalculusData` + `instDecidableEqTm`: MOVED.
- `ClosureStatements.lean` (deleted): `Template.Typed, Derivable, SlotFilled, WellFilled, Settled, Available,
  Coherent` (closure predicates); `CalculusLaws`: MOVED.
- `Lang/Contextual/LangInstance.lean`: `holeModelCandidate, holeLive, holeBlocked, holeModelIface,
  holeModelTemplate` deleted (HoleBridge's fragment).
- R3 definitions: `Lang/Contextual/Core.lean` (`Ty Ctx MEnv MEnv.nil MEnv.cons MEnv.insert Tm rename renameL mren
  mrenL mshift upS mshiftS substFn substFnL ofList subst comp shiftSub idSub proj msubst msubstL uses usesL headKnown
  Ty.decEq Ty.decEqL Tm.decEq Tm.decEqL infer inferL check shiftAt unshiftAt msubstP msubstPL`, the `Step` relation
  and `HasTy`), `CoreCalculus.lean` (`holeEnv`, `cmttData`).

The full declared list (with every generated constant) is `C2/delnames.txt` (1,831 rows, prefix-matched; 1,834 constants vanished, every one under a row).

## 2. What moves where (law 8: definitions in a def module, proofs and `Prop` structures in a proof module)

| object | from | to | statement |
|---|---|---|---|
| `CalculusData`, `instDecidableEqTm` | `Lang/Contextual/Closure.lean` | `Lang/Contextual/LangInstance.lean` (beside `langData`) | identical (digest) |
| `CalculusLaws` | `Lang/Proofs/Contextual/ClosureStatements.lean` | `Lang/Proofs/Contextual/LangInstance.lean` (beside `langLaws`) | identical; its `weaken_avoids` docstring drops the `drop_removes` mention |
| `weaken_never_var` | `Lang/Proofs/Contextual/Judge.lean` | `Lang/Proofs/Contextual/LangInstance.lean` | identical |
| `holeDecision_verified_iff`, `holeDecision_label` | `Lang/Proofs/Contextual/HoleBridge.lean` (`…Contextual`) | `Lang/Proofs/StdHole.lean` (`Nanodregg.Lang.Std`) | identical; RENAMED; docstrings added (C3's live label; `hl` discharged) |

Docstring edits (no code): `Lang/HoleDecl.lean`, `Lang/Subst.lean`, `Lang/Index.lean`, `Lang/Proofs/Index.lean`
stop naming the deleted modules. `Lang/Contextual` ends as **LangInstance + Protocol + NanoBridge**;
`Lang/Proofs/Contextual` as **LangInstance + Protocol + ProtocolTyping + Negotiation** (the protocol calculus,
R-0021; it never imported the closure [READ: `Protocol.lean` has no import; `NanoBridge` imports Protocol + the
resident trace]).

## 3. The RESTATES/DELETES map

- RENAMES (the digest's map, 2 rows): `Nanodregg.Lang.Contextual.holeDecision_verified_iff →
  Nanodregg.Lang.Std.holeDecision_verified_iff`; `…Contextual.holeDecision_label → …Std.holeDecision_label`.
- MOVES (name kept, module changes; 45 constants with generated ones) [MEASURED]: Closure → LangInstance 28;
  ClosureStatements → Proofs/LangInstance 14; HoleBridge → Proofs/StdHole 2; Judge → Proofs/LangInstance 1.
- DELETES: §1, `C2/delnames.txt`.
- RESTATES: none in this landing. C5's three theorems (§6) are NEW statements over deployed objects, landed by C5.

## 4. Gates tables and fixtures

`grep` of every deleted name and module across Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench Ops
gates scripts CHARTER [MEASURED]: no gates table row (`tcb.tsv`, `axioms-allow.tsv`, `refines-allow.tsv`,
`size-allow.tsv`, `runs.tsv`, `codec-vectors.tsv`), no fixture, no journey row names any of them; the matches of
the 87 names that also occur elsewhere are unrelated homonyms (`select`, `Status`, `Op`, `World`, …, in other
namespaces) — the exporter's reverse-dependency table (§0) is the authority. `gates/journal-report.md` mentions
`Lang.Contextual` in prose ("closure contains no Lang.Contextual module"): still true. No vector, bundle or package
id moves; no re-genesis; nothing refuses to load.

## 5. Premise price [MEASURED]

0. Type-digest changed 0 and value-hash changed 0 over every surviving constant: no landed theorem gains a
hypothesis or a binder, and none even changes its proof term. (Under the plan's §8.1 reading the bridge would have
landed with three premises (a2, a6, a7); it is not built.)

## 6. C5, C4(a), C3 over `selectHole` / `resolveHole` — AS STATEMENTS (they land in their own cards)

Elaborated against this candidate with `sorry`: `C2/C5-statements.lean` (three "declaration uses `sorry`", no
error) [MEASURED]. Objects: `selectHole`, `changedHypotheses`, `factorHole`, `runHoleGuard`, `supportLive`,
`supportObserved`, `supportPinned`, `HoleSelection` (`Lang/LiveHoles.lean`), `HoleROM.check`.

**T2 `selectHole_hypotheses`** (C5; successor of `strengthening_sound`, `suspended_sound`'s hypothesis arm,
`hyp_var_cites`, `select_requires_available`):

```lean
theorem selectHole_hypotheses (hs : selectHole digestOf look rv self h = .ok s) :
    ∃ c, h.code[s.index]? = some c ∧ s.original = c.body ∧
      ∀ x p, h.hypotheses[x]? = some (some p) →
        (x ∈ s.strengthened ↔ supportLive digestOf look rv self p = false) ∧
        (supportLive digestOf look rv self p = false → Term.usesVar x c.body = false)
```

Nano object: `changedHypotheses` inside `selectHole`. Deployed mutations that make it false: (m1) drop the
`Term.usesVar` test (a dead USED hypothesis is strengthened instead of `supportMoved`: second conjunct false — the
plan's B4 tooth); (m4) keep a dead unused hypothesis (`else .ok removed`: ← false); (m5) strengthen a live one (→
false). Today only the closed instance `used_hypothesis_suspends` sees m1, at one ROM.

**T3 `selectHole_factor`** (C5 transport; successor of `strengthening_sound`'s factor clause and, at the deployed
runtime, of `CalculusLaws.strengthen_lemma`/`strengthen_factor`):

```lean
theorem selectHole_factor {Δ : List Ty} (hchk : h.check Δ = .ok ())
    (hs : selectHole digestOf look rv self h = .ok s) :
    HasType Δ s.context s.filling h.ty ∧ s.body = s.original
```

`hchk` is the install check `instantiateHoles` runs first (`p.checkContextual Δ` → `h.check Δ`), a deployed fact on
every live path, not an assumption about the world. Nano object: `factorHole` + the embedding `selectHole` applies.
Mutations: (m2) the embedding unfiltered (`List.range h.ctx.length`): `s.body ≠ s.original` as soon as one
position is strengthened; (m6) lower in increasing order (`removed` for `removed.reverse`): the filling mistypes
with two strengthened positions. Teeth: `strengthening_factor` (one ROM, one position). Reading: strengthening is
receipt-only; the body a hole instantiates is exactly its ROM code.

**T4 `selectHole_live_selects`** (C5 completeness; successor of `judge_verified_iff` ←, `select_ok`):

```lean
theorem selectHole_live_selects {amount ver i used : Nat} {bytes : ByteArray} {c : HoleCode}
    (hrow : holeRow rv self h.selectionRel h.selectionKey = .ok (some (.row amount bytes ver)))
    (hdec : Wire.decodeData .nat bytes = .ok (.nat i)) (hc : h.code[i]? = some c)
    (hsup : ∀ p ∈ c.supports, supportObserved digestOf look p = true ∧
      supportLive digestOf look rv self p = true)
    (hhyp : ∀ x p, h.hypotheses[x]? = some (some p) →
      supportPinned digestOf look rv self p = .ok () ∧
      (Term.usesVar x c.body = true → supportLive digestOf look rv self p = true))
    (hgp : ∀ p, h.guardPin = some p → supportPinned digestOf look rv self p = .ok ())
    (hguard : run [] Bounds.stackMax Bounds.holeGuardFuel 0
      (State.init h.guard [.bool (h.guardPin.all (supportLive digestOf look rv self))]) = .value (.bool true) used) :
    ∃ s, selectHole digestOf look rv self h = .ok s ∧ s.index = i ∧ s.version = ver
```

Its premises are observations of the caller's view and the ROM, the hypotheses of a completeness statement, not
premises added to a landed theorem. Mutation: (m7) over-refusal — refuse on any dead hypothesis pin, used or not
(strengthening disabled): T2 stays true (vacuously, no selection), T4 false. Today only the closed instances
`strengthening_factor`/`kept_context` see m7.

**C4(a)** — no new theorem, no `HoleSelection.environment` field. Reason: nothing reads the receipt —
`Lang/Program.lean:222` keeps `(instantiateHoles …).map (·.body)`; the kernel record does not hold a
`HoleSelection`; `rederive` re-executes [READ]. The selection's monomial (one positive product: `c.supports` ++ the
used hypothesis pins) is all live by `selectHole_origin` + T2. Docstring on `HoleSelection` saying so; trigger for the
field: a reader of the receipt (an audit row or a kernel record that keeps it). This also avoids the plan's price
(statement edits on `selectHole_origin`, `selectHole_nodes`, `resolutionMax_committed`).

**C3** — the live label at the row grain IS `holeVerdictLabel`, read by `holeDecision_verified_iff` (moved here,
docstring "C3 at the row grain") and tied to the generated term by `holeDecision_meaning`. A ROM label (the indices
`i` for which T4's premises hold now) has no reader: no hole resident's tick reads candidates [MEASURED: `grep`
Hosting/Host for Std.hole: none]. Plan: "Lands only with the tick consumer" → C3 = this move + a docstring on
`selectHole` naming the trigger. 0 new theorems.

**§8.2 count for P2 so far:** −209 (this landing) + 3 (C5) = −206; every new theorem has a named mutation not
caught in general by a landed one; plants measured at C5's build.

## 7. The closure of the Host before and after

89 → 89 [MEASURED `gates/size.py`]: the Host exe closure never contained a `Lang.Contextual` module. The deleted
modules are proof-path only (their only importers were each other and the two `LangInstance` modules).

## 8. Reader questions (defaults in bold)

1. `CalculusLaws` placement: **into `Lang/Proofs/Contextual/LangInstance.lean` beside its one instance** (the file
   name `ClosureStatements` names a deleted object) — or keep `ClosureStatements.lean` holding only it.
2. `drop_removes`: **delete** (its premise is false at `langData`, the only instance after R3) — or move with
   `weaken_never_var`.
3. R3 in this landing: **yes** (the import graph forces it; §0).
4. T4 (completeness): **land with C5** (its mutation m7 is invisible to T2/T3) — or docstring.
5. C4(a): **no field, docstring** (no receipt reader) — or add `environment` now.
6. C3: **the moved row-grain theorem + a docstring; no ROM label** — or a `liveIndices` def + iff now.

## 9. Landing plan after RELEASE C2

The candidate is the build above (`C2/C2-candidate.patch`). Rebase onto main's tip, re-run the whole-tree build only
if main moved under Lang, `gates/check.py`, `scripts/commit` fast path `lang:` (no wire byte moves), decision
`### LANG-75.3` (critique + meta-critique naming a bias), commit message stating: what is deleted (15 modules), what
moves (4 rows), that nothing re-emits and no loaded shape changes, the digest verdict line.
