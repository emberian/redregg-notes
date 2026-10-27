VERDICT: RULE S1

The fourteen beside-modules do not weaken a gates row, a lakefile target, a rows fixture, or a surviving spine theorem. They do delete the only statement of two facts about deployed objects. Those two are re-homed, or they do not go. Everything else in S1 may go.

## What is weaker

`private theorem audit_append_to` (`Lang/Proofs/Contextual/Integration.lean:205–208`) is the only proof that `Kernel.Receive.audit` composes over `++`:

```
audit X w pre = .ok mid → audit X mid suffix = .ok final → audit X w (pre ++ suffix) = .ok final
```

It is pinned to `Host.Deployed.D` / `Host.Deployed.X`, but the proof is an induction on `audit`'s own recursion (`:209–223`) and uses nothing about Host. The deployed function is `def audit` at `Kernel/Receive/Audit.lean:68`. [READ both files at `origin/main`]

The shape-twin that survives is `Kernel.Proofs.Fold.fold_append` (`Kernel/Proofs/Fold.lean:287`), and it is about `World.fold`, not `audit`. `Kernel/Receive/Audit.lean:1–8` says the difference on purpose: fold trusts the writer's derivations; audit re-derives each step. `theorem audit_ok` (`Kernel/Proofs/Audit.lean:275–277`) is `audit = fold ∧ Honest`. There is no `Honest`-append lemma, so `audit_ok` plus `fold_append` does not state this. [READ; MEASURED the name search below]

`theorem recovery_preserves_consumption` (`Integration.lean:230`) is the only statement that a `Host.openWith` whose decoded base has `ledgerLeft transferBase grant cell = .ok (i, 0)` (`SpentCheckpoint.spent`, `:201–202`), and whose tail audits, admits zero further grant movement on `l ++ future`. The proof is `openWith_trusted`, `openWith_world`, `audit_append_to`, then `Ledger.Proofs.grant_moves_le_cap` at left `0`, then `Nat.eq_zero_of_le_zero`. [READ `:230` to end of file]

What survives and does not replace it:

- `openWith_trusted` states that the opened world is `CheckpointTrusted`. It does not mention a grant. [MEASURED: the name lives in `Host/Proofs/Trusted.lean` and this file only]
- `grant_moves_le_cap` states the cap for one audit. It survives, and it already has consumers (`Ledger/Proofs/GrantCapTooth.lean`, `Ledger/Proofs/EscrowAdmitted.lean`, the certificate pin). No Host proof mentions `ledgerLeft`. [MEASURED]

Nano objects and who re-homes them:

- `Kernel.Receive.audit`. Re-home a polymorphic `audit_append` (any `D` `audit` quantifies over, not `Host.Deployed.D`) into `Kernel/Proofs/Audit.lean`. Owner: KERNEL.
- `Host.openWith` over `Host.Deployed` at a spent grant. Re-home `recovery_preserves_consumption` (and `SpentCheckpoint`, which is only its premise bundle) into a Host proof module, `Host/Proofs/Trusted.lean` or a sibling, after the kernel lemma exists. Owner: HOST.

S1's Lang fast path cannot carry them. That is not permission to drop them. `Integration.lean` is not deleted until both statements are on main. The other thirteen files, and the p8 half of Integration through `reexecute_committed_effect` (`:179` area), are not this condition.

## What is not weaker

No surviving module, gates row, lakefile target, or rows fixture loses its subject. [MEASURED, spot-checks 1–3]

- `lakefile.lean` is `globs := #[.submodules X]` for every `lean_lib`, and no `root :=` names any of the fourteen. Deleting the files drops fourteen glob jobs and dangles nothing. [READ whole `lakefile.lean` at `origin/main`]
- `withdraw_last_support`, `TraceExamples`, and `P11bExperiments` do not occur under `gates/`, `rows/`, or `lakefile.lean`. [MEASURED]
- `one_use_consumption` is `grant_moves_le_cap` with the same premises and the same `≤ 1` conclusion (`Integration.lean`, the `Counted` section). `reexecute_committed_effect` is `submit_replayed`. `progress_under_ready_writer` is `simp [submit]` on the four branches. Those aliases may go. `commitment_binds_receipt` is a conjunction of `submit_ok`, `receiveWith_sealed`, `sealTurn_ok`, `admit_journaled`; each conjunct stays landed. It is not the only statement about those kernel objects.
- `countRun` stays in `Lang/Contextual/Closure.lean` until S10, but the tooth that counting keeps a withdrawn cycle does not live only in `Experiments`. `Worlds.Experiment.counting_keeps_cycle_over_worlds` (`Lang/Proofs/Contextual/Worlds.lean:293–311`, `by` the induction at `:311`) survives S1, next to `cycle_loses_grounding_over_worlds`. The tooth does not stop biting at this step. (It will, at S5, while `countRun` still exists. That is S5's problem.)
- `ProvenanceTeeth` is imported only by `ProvenanceExperiments` [MEASURED]. After S1 the tooth module is unimported and still built by the Lang glob. The counterexample stays stated until S10. Unimported is not toothless.
- `P/P5`, `P/Nogoods`, `P/NogoodGames` lose every importer at S1 (their importers are in this delete set: `P/Interfaces`, `P/P1`, `P/NogoodGameBridge`, `P/ProvenanceExperiments` — map §1.3). Their statements do not change, and S3 deletes them. Not weaker.
- `stable_iff_labelling` dies with `WorldsField`. Its subject, `StableLabelling`, is defined in that same file (`WorldsField.lean`, `def StableLabelling`). `Worlds.Stable` keeps `check_decides`. Not a deployed object.
- I did not re-elaborate. The builder's digest diff (595 vanished, 0 outside the 14, 0 type-digest changes, 4 equation-lemma owners moved) is their measurement. The import and name checks below agree with the "nothing outside refers" half. They do not re-prove the digest half.

`origin/main` moved. Census base `3070fac`; tip is `71db964` (`gates: the charter 1 MB file law…`). [MEASURED `git rev-parse origin/main` after `git fetch origin`] That commit touches only `decisions/gates.md`, `gates/check.py`, `gates/size-allow.tsv`, `gates/size_limit.py`, `gates/size_limit_plants.py`. [MEASURED `git log --name-only -1 origin/main`] The Lean tree of the fourteen is the tree the census read. The commit message says `gates/check.py` is RED on main until the certificate is re-pinned. That red is not caused by S1, and it is not a weakening. It does mean "check.py was green at 3070fac" is not true of the tip S1 would land on.

Local `main` is `7e02852`, behind `origin/main` by 25. Nothing below was read from the working tree.

## Spot-checks

### 1. Closure docstring, lines 6–8

Command: `git -C /Users/ember/dev/nanodregg cat-file -p origin/main:Lang/Contextual/Closure.lean` (head)

Output, lines 4–8:

```
The object of ACTIVITIES-PROPOSAL doc 2 §9, over an ABSTRACT calculus (its data `CalculusData` here, its laws
`CalculusLaws` in the proof module), so the theory
does not wait on a particular CMTT core. Two instances exist: the toy of
`Lang.Proofs.Contextual.Experiments`, and the CMTT core's, `Lang/Proofs/Contextual/CoreInstance.lean`,
which lands as the second commit.
```

The builder's quotation matches. [READ `Lang/Contextual/Closure.lean:6–8`]

### 2. Module-name references, whole history of `origin/main`

Commands (pickaxe; a string with an empty log never occurs in any blob):

```
git -C /Users/ember/dev/nanodregg log -S "Lang.Proofs.Contextual.Experiments" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -G "Lang.Proofs.Contextual.Experiments" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "Lang.Proofs.Contextual.Integration" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "Lang.Contextual.Interfaces" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "Lang.Contextual.TraceExamples" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "Lang.Contextual.AcyclicExamples" --name-only --pretty=format:%h origin/main
```

Output:

- `Experiments`: one commit, `1e94183`, files `Lang/Contextual/Closure.lean` and `Lang/Proofs/Contextual/Experiments.lean`. The `-G` run names the same two files. No other file, ever.
- `Lang.Proofs.Contextual.Integration`: empty. Nothing imports it, and the file does not spell its own name.
- `Lang.Contextual.Interfaces`: `998f75a`, only `Lang/Proofs/Contextual/Interfaces.lean` (the proof twin's import; both files are in the delete set).
- `Lang.Contextual.TraceExamples`: `0a8c780`, only `Lang/Proofs/Contextual/TraceExamples.lean`.
- `Lang.Contextual.AcyclicExamples`: `19635c9`, only `Lang/Proofs/Contextual/AcyclicExamples.lean`.

Same for the gates claim:

```
git -C /Users/ember/dev/nanodregg log -S "TraceExamples" --name-only --pretty=format:%h origin/main -- gates rows lakefile.lean
git -C /Users/ember/dev/nanodregg log -S "P11bExperiments" --name-only --pretty=format:%h origin/main -- gates rows lakefile.lean
git -C /Users/ember/dev/nanodregg log -S "withdraw_last_support" --name-only --pretty=format:%h origin/main
```

First two empty. `withdraw_last_support`: `1e94183`, only `Lang/Proofs/Contextual/Experiments.lean`.

`git -C /Users/ember/dev/nanodregg ls-tree -r --name-only origin/main -- Lang/Contextual Lang/Proofs/Contextual` lists all fourteen paths. They exist at the tip.

### 3. No landed twin of the audit composition

```
git -C /Users/ember/dev/nanodregg log -S "audit_append" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "recovery_preserves_consumption" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "SpentCheckpoint" --name-only --pretty=format:%h origin/main
git -C /Users/ember/dev/nanodregg log -S "ledgerLeft" --name-only --pretty=format:%h origin/main -- Host Kernel Ledger Lang
git -C /Users/ember/dev/nanodregg log -S "grant_moves_le_cap" --name-only --pretty=format:%h origin/main
```

Output:

- `audit_append`: `ad96bab`, files `Lang/Proofs/Contextual/Integration.lean` and `decisions/lang.md`. Nowhere else.
- `recovery_preserves_consumption` and `SpentCheckpoint`: `ad96bab`, only `Integration.lean`.
- `ledgerLeft` under Host/Kernel/Ledger/Lang: `Integration.lean`, `Lang/Journey.lean`, `Ledger/Proofs/GrantCap.lean`, `GrantCapTooth.lean`, `EscrowAdmitted.lean`, and Kernel receive/proof files. No `Host/Proofs/*` file.
- `grant_moves_le_cap`: Integration, GrantCap, GrantCapTooth, EscrowAdmitted, certificate tooling, decisions. The real theorem keeps a consumer after Integration goes.

[READ `Kernel/Proofs/Audit.lean` whole: theorems are `audit_ok`, `audit_cancel_signed`, `audit_cancel_forged`, `audit_unsigned_is_judged`, `auditRefusal_stale`, and the judge/cancel block. No append.] [READ `Kernel/Proofs/Fold.lean:287` `fold_append`.] [READ `Kernel/Receive/Audit.lean:68`.]

## Rulings

**(a) Closure.lean:6–8, fix inside S1. Yes.**

The deletion makes the sentence false, and it is already incomplete: `toyLaws` occurs only in `Experiments.lean` [MEASURED `git log -S toyLaws`], `cmttLaws` in `CoreCalculus.lean` and `CoreInstance.lean`, `langLaws` in `LangCalculus.lean` and `LangInstance.lean`. After S1 the two survivors are `cmttLaws` and `langLaws`. Use the builder's sentence. The price they name (a comment edit in a Host-closure module, dependents rebuild, no statement change) is [INFERRED from the import of `HoleDecl` only, `Closure.lean`, and the map's closure claim]. I did not rebuild.

Same landing, same reason, one sentence the builder did not flag. `Lang/Proofs/Contextual/Worlds.lean:321–322`:

```
The new WorldsField proof module proves stable_iff_labelling independently:
model closure plus absence of unfounded IN sets equals reduct semantics.
```

S1 deletes that module. Strike or rewrite the sentence. Do not keep `WorldsField` to save a comment.

**(b) `recovery_preserves_consumption` and `audit_append_to`. Do not delete.**

Default was delete. Overridden. They are the only statements of the two deployed facts named above. Re-home before `Integration.lean` disappears: KERNEL writes `audit_append` in `Kernel/Proofs/Audit.lean`; HOST writes the recovery theorem. The p8 half of Integration, and the three pure aliases (`one_use_consumption`, `reexecute_committed_effect`, `progress_under_ready_writer`), go with the module.
