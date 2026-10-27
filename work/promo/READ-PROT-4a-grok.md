VERDICT: RULE PROT-4a

Conditions: (1) The `/-!` block this patch adds to `Lang/Proofs/Rel.lean` says a plant that computes the guards and ignores their verdict reds `run_edits_guarded` by name and nothing else. Delete that sentence. The whole log does not name `run_edits_guarded`, and it reds two landed proofs. (2) Do not call P3 `activity_monitor_safe`'s tooth, in LANG-75.9 or elsewhere. Under P3 `Lang.Proofs.StdActivityMonitor` built; the only red is `activity_fixture_monitored`. P2 is `waiting_no_replay` and `activity_answer_no_replay`, and the monitor module was not built. (3) `activity_program_safe`'s comment says the statement covers `Std.hole`'s fill log. It does not, on the generator as written (`holePackage`'s body is an `.app`; the linked root has imports). The fixture witness is the coverage that was decided. The Bell is not a witness in this patch.

Read at nano `origin/main` = `51089fb` (fetched). Nothing built. The candidate is `promo/PROT4a/` (not on main). Local `main` is behind that sha; the blobs below are `git show origin/main:…`.

## 1. The three statements (READ of the patch; plants MEASURED)

`run_edits_guarded` is the sentence, stated on `runMeasuredWith`, with one premise.

The hypothesis is only `runMeasuredWith … = .ok (s, calls, rows, t, n)`, for an arbitrary setup. [READ `candidate.diff`] That is not a premise past extraction adds and this one piles on. The public past-extraction theorems (`Provenance.lean:1159`, `:1184`, `:1214`, `:1269`) assume `Lawful` (and, for the two `program.run` forms, `X.program = Lang.program`) plus setup, the machine run, and extraction, and conclude equality to the do-block whose last bind is `guardEdits`. This theorem assumes none of those. Its one premise is the admitted run, which those theorems do not assume: their right-hand side is still a `guardEdits` bind, and that bind may be an error.

The conclusion is the per-edit success of that bind, not the name `guardEdits es = .ok ()` (that equation is `runMeasuredWith_ok`'s conjunct). [READ `Program.lean:428-441`, `:443-461`] `guardEdits` is `es.mapM (guardOld digestOf rv r.self)` then `(es.zip olds).forM`, and `rv` is the view the run was given, once, not a view updated between edits. `S.state` is the state the setup read, before `run`. For `decl.guard = none` the arm is `.ok ()` and the theorem's `∀ gl, guard = some gl → …` is vacuous. For `some gl` the only arm that returns `.ok ()` is `runLaw … = .ok (.ok ())`; `.ok (.error _)` and `.error _` are `.lawDenied`. The theorem says that, plus `rows = es.map (·.slot, ·.act)`. That is "every edit in the result passed its declared guard, judged against the pre-run view."

It is stated on `runMeasuredWith`, which is what `runMeasured` and `runMeasuredLive` are (`Program.lean:472-482`), and `program.run` is `runMeasuredLive` mapped down to the 4-tuple (`:548-551`). The theorem does not mention `program.run`. The docstring's "and so `Lang.program`'s `run`" is the map, not a second hypothesis. No package shape, no `Lawful`.

`guardEdits_ok` is its own fact. `runMeasuredWith_ok` is the converse, and it has no plant of its own.

Four questions, `guardEdits_ok`:

- Nano object: `guardEdits` returning `.ok ()`. Not a run. [READ the statement]
- Weaker without it: no landed theorem. `guardEdits_never_stuck` is "not `.error .stuck`"; `guardEdits_unpinned` is a refusal. [READ `Rel.lean` as cited in READ-PROT-1; the new proofs sit after both, and P1b's only error is at line 983, past them.] `run_edits_guarded` and `activity_monitor_safe` are proved by it (`exact guardEdits_ok`, and the monitor's `obtain … := guardEdits_ok`). A follower that only has the do-block equality does not have the verdict.
- Disjunct: the landed match has one success arm for a declared guard, `.ok (.ok ())`. The `none` arm is the other success and is excluded from the `runLaw` claim by the implication. The theorem does not stay true by a disjunct a landed theorem already owns.
- Mutation nothing landed catches: P1b. [MEASURED `plant-P1b.diff`, `plant-P1b-whole.log`] The arm `.ok (.error _)` becomes `.ok ()`. The only error is `Rel.lean:983`, goal `runLaw = .ok (.error why)` ⊢ `runLaw = .ok (.ok ())`, inside `guardEdits_ok` (the theorem starts at new line 967). `Lang.Proofs.Provenance` built. Failed targets: `Lang.Proofs.Rel` only. Lean exited on that error, so `run_edits_guarded` (new line 1026) is not a second line in the log. Its statement is the same verdict, so it is false under P1b too; the log does not name it.

Four questions, `runMeasuredWith_ok`:

- Nano object: one `runMeasuredWith` result. The real runner, any setup.
- Weaker without it: the converse is not a corollary of past extraction. Those theorems take the pieces as hypotheses. You cannot invert them. `run_edits_guarded` is `obtain := runMeasuredWith_ok`. What it drops, and this lemma keeps, is `guardEdits = .ok ()` as an equation, plus setup, the `.value`, the extract shape, and `editsOf`. It does not keep `callsOf` (`⟨-, -, rfl, -, -⟩` discards it). That is a thinner converse, not a false one.
- Disjunct: P1 is the extra success arm (`let _ := guardEdits`, verdict ignored). The proof's goal becomes `⊢ guardEdits = .ok ()` with that hypothesis gone. [MEASURED `plant-P1-whole.log` at `Rel.lean:1019:79`, which is the `‹guardEdits … = .ok ()›` in `runMeasuredWith_ok`'s last line, new line 1019.] The theorem is exactly the claim that `.ok` went through that bind.
- Mutation nothing else catches: none was run. P1 also reds `runMeasured_past_extraction_of` and `runMeasuredLive_past_extraction_of`. P1b does not falsify this lemma: `guardEdits` still has to return `.ok ()` for the run to. It is a real converse, and it is a lemma of `run_edits_guarded`, not a tooth.

## 2. `activity_monitor_safe` is in this half. P2 is not its plant.

Not deferred. [READ `promo/PROT4a/StdActivityMonitor.lean`] `waiting_body_step`, `activity_monitor_safe`, `activity_program_safe` are in the candidate. The impact leaves the iff (`waiting_*_iff`) for PROT-4b. That split matches the statements: this half is "admits ⇒ step", not "step ⇒ admits".

The sentence, precisely: if the package's relation `ℓ` is guarded by a field that is the `activityWaiting` term, the value type is `activityLogVal`, the capture type is well formed, and the resumer is `NoRef`, then every edit at `ℓ` in a `runMeasured` that returned is a `WaitingStep` over `guardOld`'s row, the request, and the pre-run state. Not every edit of the object: the cursor is `activityQueued`, and the quantifier is `x.label = ℓ →`. `WaitingStep` is the log row's three edges. [READ `activityWaiting`, `StdActivity.lean:69-88`] Insert requires the key's agent and an unanswered value; upsert requires the resumer, the same capture, and the plan's own answer; retract of an answered row is `okT` for every requester (`activity_retire_some_meaning` says so). `WaitingStep.retire` has no actor. That matches the guard; it is not a dropped conjunct.

`activity_program_safe` is the same conclusion for `(Lang.program …).run`, via `runMeasuredLive_leaf_closed`, and only if `p.imports = []` and `p.holes = []`. [READ the statement]

The doubled environment is real, and it is why this is not `exact waiting_upsert_iff`. [READ `app3_vars_inv`, `Lang/Proofs/StdActivity.lean`] The landed iff evaluates `activityApply (activityWaiting …) [.var 2, .var 1, .var 0]` in `i::q::s::env`, so the body runs in `i::q::s::i::q::s::env`. `waiting_body_step` evaluates `lawBody` in `guardIn::req::state::cenv`. No finite `env` makes those lists equal. After the edit `case` conses, both put payload, input, req, state at vars 0–3, and `activityWaiting`'s own term does not read var 4; a tail lemma could exist and does not. The landed statements do not say the `lawBody` fact. `waiting_body_step` is that fact, at any `cenv`, which is what `runLaw_ref_admits` returns.

P2 is the brief's plant (answered upsert → `okT`) and it is already a tooth. [MEASURED `plant-P2.diff`, `plant-P2-whole.log`] `Lang/Proofs/StdActivity.lean:144` is `case_known hans rfl` expecting `some (refusedT _)` and finding `("some", okT)`. That is `waiting_no_replay`. `StdActivityTeeth.lean:87` is `actGuard "r" (upsert of an answered row) = some "answered"`, `decide` stuck: `activity_answer_no_replay` (origin's `:72–73` plus the 14 lines this patch inserts above it). Failed targets: those two modules. `Lang.Proofs.Rel` and `Lang.Proofs.Provenance` built, so `run_edits_guarded` stayed green, as it should: the guard ran and returned ok. `StdActivityMonitor` imports `Lang.Proofs.StdActivity` and was not built. P2 was not measured against `activity_monitor_safe`. It duplicates `waiting_no_replay` and `activity_answer_no_replay`. It does not duplicate `activity_answer_once` (that tooth is an admitting row; the module doc is right to leave it).

P3 is not a substitute tooth for the theorem. [MEASURED `plant-P3-whole.log`] `Lang.Proofs.StdActivityMonitor` built (job 649). The only failure is `StdActivityTeeth.lean:45`, `activity_fixture_monitored`, `decide` stuck on `d.guard == some "waits_waiting"`. The theorem is an implication whose package premises are false for that one package and true for any other package that still has the guard. Dropping the generator's guard does not falsify it. The impact's "activity_monitor_safe's tooth" is the fixture witness. Say that.

`Std.hole`'s fill log is not an instance of the deployed theorem. [READ `Lang/StdHole.lean`] `holePackage` sets `body := .app (.lam _ (.record _)) (holeCheckedJudge …)`, so `p.body = .record fs` fails. `HoleBundle.link` sets `imports := ids`, so `activity_program_safe`'s `p.imports = []` fails on the installed root. `activity_fixture_monitored` is `actPkg`, the activity fixture, not the Bell and not the hole. The Bell sentence (an author `answer` upserts `rings`, `Bell.ob`) is true of the surface method; this patch does not decide that the compiled Bell's `rung` field is the `activityWaiting` term.

## 3. P1 does not red `run_edits_guarded` by name, and it does not spare what landed (MEASURED)

`plant-P1.diff`: `guardEdits …` becomes `let _ := guardEdits …` in `runMeasuredWith`. `plant-P1-whole.log`, the lake transcript's own failure list:

- `Rel.lean:1019:79` `assumption` failed. The goal is `⊢ guardEdits bytesOf digestOf S rv pkg r v✝ = Except.ok ()`, in the success context of `runMeasuredWith` with no `guardEdits` hypothesis. That line is `runMeasuredWith_ok`'s closing `exact`, the `‹guardEdits … = .ok ()›`. Not `run_edits_guarded`.
- `Provenance.lean:1081:23` unsolved goals. The two sides of the equation are `editsOf` then `pure`, against `editsOf` then `guardEdits` then `pure`, under `runSetup`. Line 1081 on `51089fb` is the `| ok calls =>` arm of `runMeasured_past_extraction_of` (`:1037`).
- `Provenance.lean:1131:23`, the same goal under `runSetupLive`. Line 1131 is the `| ok calls =>` arm of `runMeasuredLive_past_extraction_of` (`:1087`).

Failed targets, the summary line: `Lang.Proofs.Rel`, `Lang.Proofs.Provenance`. Nothing else. The public theorems at `:1159`, `:1184`, `:1214`, `:1269` are one-line uses of those two private lemmas (`:= runMeasured_past_extraction_of …`, and the live one likewise); they have no error line of their own because they do not re-simp. The module failed. Importers of `Rel` were not built, which the impact says. The saved logs start at the first rebuilt job (505 for P1); the closing "Some required targets logged failures" is the whole-tree set.

The impact's table matches this log. The patch's docstring does not. CX-PROMO-3's "P1 reds only the new theorem" was the `Lang.Proofs.Rel` closure, and this whole log is the correction. P1b, not P1, is the tooth that leaves that family green (§1).

## 4. Price (READ of the diff; the digest was not in the artifacts)

No landed theorem in `candidate.diff` gains a binder. The edits to existing files are the four new declarations at the end of `Rel.lean`, `activity_fixture_monitored`, and `activityLog`'s value written as `activityLogVal` — the same `.record [("answered", optTy (activityResponses plans)), ("captured", activityCaptured plans)]`. [READ `Lang/StdActivity.lean:46-48` against the patch]

`promo/PROT4a/` has the module, `candidate.diff`, four plant diffs, four whole logs, `plants.out`. No decls map, no `RESTATES-MEANING` line, no digest diff. "The judge confirms it" is not a file here. [MEASURED by the directory listing] GATES-20t counts elaborated statement digests of theorems and axioms, not hypotheses. [READ as quoted in READ-PROT-1] Zero new hypotheses is the diff. Zero map lines is what that diff should produce, because no existing theorem's syntax changed and a `def`'s body is not elaborated into another declaration's statement. That is INFERRED. I did not run the judge.

Count of new theorem declarations in the patch: 4 in `Rel.lean` (one private), 16 in `StdActivityMonitor.lean` (10 private), `activity_fixture_monitored`. 21. The impact's 5881 → 5902 matches that count. Not a digest.

`plants.out`: restore build exit 0 with the candidate files still modified. That is the green tree they recorded. I did not rebuild it.

## 5. The consumer is `rederive`'s `receive`, and nothing in `Audit.lean` calls `guardEdits` (READ)

`Kernel/Receive/Audit.lean`: `rederive` is `decodeCall`, then `receive X w c`, then `t' = t`. No `guardEdits`. `audit` is `rederive` then `World.admit`. The module docstring of `StdActivityMonitor.lean` says a follower that re-runs a method re-runs the guards. Operationally that is `rederive` → `receive` → `program.run` → `guardEdits`, not a call of `guardEdits` and not an application of these theorems. [INFERRED the `receive` → `program.run` step; READ `program.run` and `rederive`.] LANG-75.9 is not in the candidate. The impact's §5 says the decision will record the PROT-1 fold and P1's correction; it does not say the decision names audit. The journey was not run under P1b or P3 (the impact says so; P3's log builds `«lang-journey»:exe` and does not run it). PROT-3's `answered_row_is_kept_answer` is named as a later consumer, not one this patch calls.

The theorem a follower can cite is `activity_program_safe` / `activity_monitor_safe`, for a package that meets the premises. The fixture is the only such package this patch decides.
