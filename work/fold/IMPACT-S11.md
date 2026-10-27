# IMPACT-S11 — the Trace split: `collect` joins the generated hole's model; the rest of P10's trace is deleted (consolidation step S11)

Worker: CX-FOLD-3 (Claude). Written 2026-10-22 after building the candidate in scratch (`hbox:logs/cxfold/S11-tree`),
**stacked on the S10 candidate** (`fold/S10-candidate.patch`, itself on the S9 candidate). S11 touches no file S10
touches. Map: §1.1 (:84, :87), §1.3 row P/Trace (SPLIT), §2.3 (:456), §3.1 row S11, §3.2 (:494–495), §4.2 row S11.
Tags READ / MEASURED / INFERRED. Judge: fast (`lang:`). Candidate: `fold/S11-candidate.patch` (4 files). Edit script:
`fold/S11-s11edit.py` (asserts every anchor; moves text verbatim). Rename map: `fold/S11-renames.tsv`. Census diff:
`fold/diff-S11.txt`.

## 0. Answer first

`Lang/Contextual/Trace.lean` (130 lines) and `Lang/Proofs/Contextual/Trace.lean` (306 lines) are P10's verifying-trace
model over the abstract closure. One thing in them is REACHED [MEASURED grep]: the 8-line list fold
`Contextual.Trace.collect`, used by `Lang/StdHoleModel.lean`:63 (`holeCoverageOutcome`, the generated hole's
coverage check) and unfolded by `Lang/Proofs/StdHoleCoverage.lean`:32. Everything else has no consumer outside the two
files since S1 (Integration, TraceExamples) and S2 (the p8 rows).

S11: `collect` → `Lang/StdHoleModel.lean` as `Nanodregg.Lang.Std.collect`, its three lemmas (`collect_sound`,
`collect_total`, `collect_missing`) → `Lang/Proofs/StdHoleCoverage.lean` in the same namespace, both verbatim; the two
Trace files are deleted. **0 statement changes; 17 theorems deleted, exactly map §3.1's list** [MEASURED].

## 1. Deleted, by name

Theorems (17) [MEASURED, the census VANISHED list]: `seed_valid`, `refresh_valid`, `refresh_consistent`,
`repair_entries`, `from_scratch_consistency`, `repair_minimal`, `repair_once`, `early_cutoff`, `repair_valid`,
`capture_sound`, `checkedJudge_sound`, `checkedJudge_total`, `changed_iff`, `tagged_filter`, `evaluate_observe`,
`guard_reads_only`, `observation_complete`.

Definitions: `Guard` (+ `install`, `reads`, `run`), `Snapshot`, `observe`, `evaluate`, `Missing`, `capture`,
`checkedJudge`, `Cached`, `seed`, `meets`, `refresh`, `Pass`, `repair`, `dirtyReaders`, `Valid`, with their derived
instances and generated constants. 184 constants vanish, all under `Nanodregg.Lang.Contextual.Trace` or the two
modules' private prefixes (declared); 0 undeclared.

Reason (map §2.2/§3.1): a cache/early-cutoff model of the abstract closure with no nano object behind it; its
consumers were Integration (S1), TraceExamples (S1) and the p8 rows (S2), all gone. The one function the deployed
generated hole uses survives, next to its user.

## 2. Moved, statement-identical

| old | new | file |
|---|---|---|
| `Contextual.Trace.collect` | `Std.collect` | `Lang/StdHoleModel.lean` (before `holeCoverageOutcome`) |
| `Contextual.Trace.collect_sound` / `_total` / `_missing` | `Std.collect_sound` / `_total` / `_missing` | `Lang/Proofs/StdHoleCoverage.lean` |

`StdHoleModel` drops `import Lang.Contextual.Trace`; `StdHoleCoverage` drops `import Lang.Proofs.Contextual.Trace`.
Their callers write `collect` (same namespace). No name collides in `Nanodregg.Lang.Std` [MEASURED: the build].
The three lemmas have no consumer today besides the deleted `capture_sound` / `checkedJudge_total`; they are kept as
the map says (§2.3:456) because they are the specification of the deployed collector (`collect_missing`: an omitted
declared read prevents success, the general form of what `holeCoverageOutcome_ok_iff` checks by enumeration) [INFERRED].

## 3. Census digest diff (S10 candidate → S11 candidate, under the map) [MEASURED `fold/diff-S11.txt`]

- 184 vanished, all declared; 0 undeclared.
- 0 type changes; 1 value change: `Std.collect.eq_def` (realized in the proof module; its value cites the matcher of
  the module that realizes it).
- 9 new: `_private.Lang.Proofs.StdHoleCoverage.0.Nanodregg.Lang.Std.collect.match_{1,3,5}.{eq_1,eq_2,splitter}`; the
  9 vanished `_private.Lang.Proofs.Contextual.Trace.0.…collect.match_*` are the same generated lemmas, whose private
  name embeds the module that realizes them.
- 13 module changes, all from the two Trace modules (7 → `Lang.StdHoleModel`, 6 → `Lang.Proofs.StdHoleCoverage`).
- No exe closure changes (every `lean_exe` root's import closure compared, S10 → S11) [MEASURED].

## 4. Consumers [MEASURED `git grep` over Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench Ops gates rows lakefile.lean]

`Contextual.Trace`: only `StdHoleModel`:4,63 and `StdHoleCoverage`:3,32 outside the two files. No gates table, row,
fixture or lakefile entry names either module (the lakefile globs `Lang`).

## 5. The inverted question: what surviving module or row is weaker?

None [MEASURED]. `StdHoleModel` and `StdHoleCoverage` compute and prove exactly what they did (0 type, 0 user value
changes); the journey (default, `--contextual`, `--contextual-checks`) is byte-identical to the S9 candidate's. The 17
deleted theorems have no reader in the tree.

## 6. Gates [MEASURED, scratch]

`lake build Lang` GREEN (222 jobs); whole tree with `host lang-journey codec-vectors` GREEN (622 jobs); journeys
byte-identical; `gates/check.py` GREEN with the generated SIZE (modules 492 → 490, proof modules 264 → 263, theorems
6074 → 6057, Lang lines 42286 → 41908). Re-emit: none; nothing refuses to load.

## 7. What breaks

`Lang/Contextual/Trace.lean` and `Lang/Proofs/Contextual/Trace.lean` no longer exist; `Contextual.Trace.*` no longer
resolves; `collect` and its three lemmas are `Nanodregg.Lang.Std.*`.
