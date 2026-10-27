VERDICT: RELEASE S11

`collect` and its three lemmas move, statement-identical, into the modules that already own the generated hole's coverage check. They do not drag Trace's toy types. The seventeen deleted theorems are about the cache/repair adapter over the abstract closure; none is the only statement of a fact about `Std.hole`, `Std.activity`, the journey, or the live path. The journey's trace/repair rows are already gone (S2, landed). The census diff has 0 type-digest changes and 0 module moves from a module this step does not touch. No build.

Base read: nanodregg `origin/main` = `ac34521` (fetched 2026-10-22). Local `main` is `7e02852`, behind; nothing below was read from the working tree. The candidate is `fold/S11-candidate.patch`, read whole (550 lines, 4 files), stacked on S10. S9 and S10 did not edit those four files: the patch's old side of `Lang/Contextual/Trace.lean`, `Lang/Proofs/Contextual/Trace.lean`, `Lang/StdHoleModel.lean` and `Lang/Proofs/StdHoleCoverage.lean` matches `origin/main`.

## (1) The move

[READ `fold/S11-renames.tsv`] four rows, and only these:

| old | new |
|---|---|
| `Nanodregg.Lang.Contextual.Trace.collect` | `Nanodregg.Lang.Std.collect` |
| `Nanodregg.Lang.Contextual.Trace.collect_sound` | `Nanodregg.Lang.Std.collect_sound` |
| `Nanodregg.Lang.Contextual.Trace.collect_total` | `Nanodregg.Lang.Std.collect_total` |
| `Nanodregg.Lang.Contextual.Trace.collect_missing` | `Nanodregg.Lang.Std.collect_missing` |

`collect` lands in `Lang/StdHoleModel.lean`, immediately before `holeCoverageOutcome`. The three lemmas land in `Lang/Proofs/StdHoleCoverage.lean`, immediately before `holeCoverageCheck_application`. [READ the patch hunks; READ `fold/S11-s11edit.py`] the edit script slices the text between docstring anchors (`between`) and asserts `collect` occurs once and the slice contains exactly three `theorem`s. It does not retype them.

[READ `origin/main:Lang/Contextual/Trace.lean` and the inserted block] `collect`'s docstring, binders and equations are the same bytes:

```
def collect {A B R : Type} (missing : A → R) (read : A → Option B) :
    List A → Except R (List B)
  | [] => .ok []
  | k :: ks =>
    match read k with
    | none => .error (missing k)
    | some v => match collect missing read ks with
      | .error e => .error e
      | .ok vs => .ok (v :: vs)
```

[READ `origin/main:Lang/Proofs/Contextual/Trace.lean` against the inserted block] `collect_sound`, `collect_total` and `collect_missing` match byte for byte, proofs included. Their statements:

```
theorem collect_sound {A B R : Type} (missing : A → R) (read : A → Option B)
    (f : A → B) (agree : ∀ k v, read k = some v → v = f k)
    (ks : List A) (vs : List B) (h : collect missing read ks = .ok vs) :
    vs = ks.map f ∧ ∀ k ∈ ks, read k = some (f k)

theorem collect_total {A B R : Type} (missing : A → R) (f : A → B) (ks : List A) :
    collect missing (fun k => some (f k)) ks = .ok (ks.map f)

theorem collect_missing {A B R : Type} (missing : A → R) (read : A → Option B)
    (ks : List A) (k : A) (hk : k ∈ ks) (hn : read k = none) :
    ∀ vs, collect missing read ks ≠ .ok vs
```

No `Guard`, `Snapshot`, `Candidate`, `World`, `CalculusData`, `Token` or `Missing` in any of the four. The namespace change is the surrounding `namespace`, which is the rename map. [MEASURED `fold/diff-S11.txt`] `type-digest changed 0`, so the elaborated statements match under that map.

The homes are the right ones, and the move does not drag the toy.

[READ `origin/main:Lang/StdHoleModel.lean`] the module is the generated hole's observable model (`holeProbeClosure`, `holeAdmission`, `HolePoint`, `holeCoverageOutcome`, `holeCheckedAdmission`). Its only use of Trace is the import and one call. After the patch that call is `collect` on three `(Bool × String)` roles the module already writes: `"support0 withdrawn"`, `"support1 withdrawn"`, `"pruned"`. The arguments are unchanged. Those roles, `Fault` and `Val` are this module's objects. `collect` is the fold they already specialize; it does not quantify over Trace's types, so nothing of `Guard` / `Cached` / `repair` comes with it. The import of `Lang.Contextual.Trace` (and through it `Lang.Contextual.Closure`) is dropped, not widened.

[READ `origin/main:Lang/Proofs/StdHoleCoverage.lean`, `StdHoleLookup.lean`, `StdHole.lean`] coverage already proves the emitted check. `holeCoverageOutcome_ok_iff` is the eight-case enumeration of this fold (`simp [holeCoverageOutcome, Contextual.Trace.collect, Except.map]`, retargeted to `collect`). The import chain `StdHoleCoverage → StdHoleLookup → StdHole → StdHoleModel` already opens `Nanodregg.Lang.Std`, so the lemmas see `collect` with no new import and no Trace import. Map §2.3 (line 456) puts these three lemmas here because they are the specification of that collector: `collect_missing` is the general form of what `holeCoverageOutcome_ok_iff` checks by cases. [READ the proof file] nothing else in `StdHoleCoverage` calls the three lemmas today; their only callers were `capture_sound` and `checkedJudge_total`, which are in the delete set. Keeping them is the map's keep, not a new pile. They are theorems in a proof module; the `def` stays in `StdHoleModel`.

[INFERRED] a generic list module would also type-check. It would be a second home for a function with one caller. Beside `holeCoverageOutcome` is the home the map names, and it is the one that already owns the roles.

## (2) The deletions

[READ both Trace files at `origin/main`] the proof file has twenty theorems. Three move. The other seventeen are exactly map §3.1's S11 list, and exactly the user theorems in the census VANISHED lines:

`seed_valid`, `refresh_valid`, `refresh_consistent`, `repair_entries`, `from_scratch_consistency`, `repair_minimal`, `repair_once`, `early_cutoff`, `repair_valid`, `capture_sound`, `checkedJudge_sound`, `checkedJudge_total`, `changed_iff`, `tagged_filter`, `evaluate_observe`, `guard_reads_only`, `observation_complete`.

No eighteenth user theorem. `Valid` is a `def` of a `Prop`, deleted with the cache, not a theorem.

The audit_append test (READ-S1: a deleted theorem that is the only statement of a fact about a deployed object must be re-homed). Applied to each group:

- Cache and repair (`seed_valid`, `refresh_valid`, `refresh_consistent`, `repair_entries`, `from_scratch_consistency`, `repair_minimal`, `repair_once`, `repair_valid`, `early_cutoff`, `changed_iff`). Subject is `Cached`, `Pass`, `seed`, `refresh`, `repair`, `dirtyReaders` over `CalculusData`. [READ `LiveHoles.lean` in the S9 patch, the comment that survives from `origin/main`] selection is fresh on each invocation. There is no deployed cache these theorems are about. Map §2.2 group D-TRACE.
- Observation adapter (`evaluate_observe`, `guard_reads_only`, `observation_complete`, `capture_sound`, `checkedJudge_sound`, `checkedJudge_total`). Subject is `Guard.install`, `observe`, `evaluate`, `capture`, `checkedJudge`, and `judge` after that install. [READ `Trace.lean`] `checkedJudge`'s own docstring: "a checked adapter, not a claim that an existing package calls it." This `checkedJudge` is not `holeCheckedJudge`. The generated one, and `holeCheckedJudge_application` / `holeCheckedAdmission_evaluated_iff`, stay in `StdHoleCoverage` untouched except for the inserted lemmas above them.
- `tagged_filter`. A list identity, `((xs.map fun x => (x, p x)).filter Prod.snd).map Prod.fst = xs.filter p`. Its only caller in the file is `capture_sound`. Not a deployed object.

None of the seventeen mentions `Std.hole`, `Std.activity`, `selectHole`, `instantiateHoles`, the journey, or the live loader. The statements that are about those objects stay: `holeCoverageOutcome`, `holeCoverageCheck_application`, `holeCoverageOutcome_ok_iff`, `holeDecision_application`, `holeJudge_application`, `holeVerdictCheck_*`, `holeCheckedJudge_application`, `holeCheckedAdmission_evaluated_iff` [READ `StdHole.lean` and `StdHoleCoverage.lean` at `origin/main`]. The three `collect_*` lemmas, which are the general spec of the deployed collector, are the ones that move.

Journey. [MEASURED `git log origin/main -- Lang/Journey.lean`] the last commit that touches it is `a9ab514` (S2). [READ that diff] it drops `import Lang.Contextual.Trace` and the calls `Contextual.Trace.seed` / `Contextual.Trace.repair`. The "trace rejudged …" half of P8.1 goes; the kernel half stays (`usable == "admitted"`). P8.2's provenance read becomes `p8Live` (a kernel pin read). The tombstone `guardFails` row and the P8.3 transport/`unknownCertificate` row go. What remains does not name `collect`, `repair`, `Guard`, `seed` (the Trace one), `refresh`, `capture`, `checkedJudge`, or any of the seventeen theorems.

[READ `origin/main` `Lang/Journey/Contextual.lean`, `ContextualChecks.lean`, `Hole.lean`, `HoleChecks.lean`, `Activity.lean`] no import of Trace and no use of the deleted names. `Journey.Contextual.seed : Slots` is an initial slot fixture for the live invoke. It is not `Contextual.Trace.seed`. [READ the S9 patch's journey hunks, `Contextual.lean` and `ContextualChecks.lean`, and the patch through `StdContextualHole.lean` (1118 lines)] S9 retargets refusals to `HoleRefusal` and adds `recheck-arm-reachable` (`instantiateHoles … = .error .instanceRecheck`). It does not name Trace, `collect`, `repair`, or the seventeen. S9's file set does not include the four S11 files. [READ IMPACT-S10] S10's files are Closure, Provenance, the provenance proof, ProvenanceTeeth, Judge, and the `tm_decEq_toy` home; the journey is byte-identical to S9's, and none of those files is an S11 file. The S11 patch does not touch `Lang/Journey.lean` or `Lang/Journey/`.

[MEASURED `git log -S`] `seed_valid` only ever in `P/Trace` and `TraceExamples` (deleted at S1, `f665e94`). `early_cutoff` only in `P/Trace` and `decisions/lang.md`. `dirtyReaders` only in the two Trace files and `TraceExamples`. `collect_missing` only in `P/Trace`. `Contextual.Trace`'s occurrence count last changed at S2. The string remains in the two Trace files (deleted here), in `StdHoleModel` and `StdHoleCoverage` (retargeted to the unqualified name), and in `decisions/lang.md` (append-only prose, not a consumer; the S11 patch does not edit it).

## (3) Zero type changes, nothing outside

[MEASURED `fold/diff-S11.txt`, read whole, 201 lines]

```
before 51326 (rows carrying a renamed-from name: 22) after 51151
vanished 184 declared 184 UNDECLARED 0
new 9 type-digest changed 0 value-hash changed 1
module changed 13 of which from a module the step does not move 0
   module Lang.Contextual.Trace -> Lang.StdHoleModel 7
   module Lang.Proofs.Contextual.Trace -> Lang.Proofs.StdHoleCoverage 6
```

`51326 − 184 + 9 = 51151`. Lines 7–190 are 184 `VANISHED` lines, every one module `Lang.Contextual.Trace` or `Lang.Proofs.Contextual.Trace`. No `TYPE` line.

The one value change is `Nanodregg.Lang.Std.collect.eq_def`, module column `Lang.Proofs.Contextual.Trace` (the before module). [INFERRED, matching IMPACT-S11 §3 and the shape of the S8 `eq_def` notes] its type digest did not move; the proof term cites the per-clause matcher, and that matcher's private name embeds the module that realizes it. Not a statement change.

The 9 new names are `_private.Lang.Proofs.StdHoleCoverage.0.Nanodregg.Lang.Std.collect.match_{1,3,5}.{eq_1,eq_2,splitter}`. The same nine vanish under `_private.Lang.Proofs.Contextual.Trace.0.…`. The rename map rewrites the constant's namespace, not the `_private.<module>` prefix, so the census cannot see them as one row. They are the generated matchers of the moved `def`, not new theorems.

The 13 module moves are all out of the two Trace modules. The diff does not itemize them; it does say none comes from a module the step does not move.

[READ the patch] files touched, and no others: delete `Lang/Contextual/Trace.lean`, delete `Lang/Proofs/Contextual/Trace.lean`, edit `Lang/StdHoleModel.lean` (drop the import, insert `collect`, unqualify the call), edit `Lang/Proofs/StdHoleCoverage.lean` (drop the import, insert the three lemmas, unqualify the `simp`). No journey file, no `lakefile.lean`, no `gates/`, no Kernel, Ledger, Host, or Census file.

Builder's `lake build` and journey byte-equality were not re-run here.
