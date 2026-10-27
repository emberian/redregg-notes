VERDICT: RULE PROT-1

Conditions: do not widen `ObjectStep`. Do not grant `Kernel/Proofs/Logic/{History,HistoryWitness}.lean` or `Ledger/Proofs/{EscrowAdmitted,EscrowInvokes}.lean` for this card. The guard-grain fact ("an admitted activity edit is an enabled action of the log-row projection") is PROT-4's `activity_monitor_safe`, stated at Lang grain (`run_edits_guarded` as a corollary of `program_run_past_extraction`, composed with the landed `waiting_*_iff`). NanoBridge stays; PROT-3 owns `nano_runs_iff`. A world-phase `Reach` is not this card: no deployed mutation reds it without already redding a landed theorem (`activity_answer_no_replay`, `program_run_past_extraction`, or `rowsRun_eq`).

Read at nano `origin/main` = `51089fb`. Nothing built.

## 1. No landed theorem says an admitted run's edits passed their guards (READ)

The finding holds. The card does not shrink to a name that already exists. It does shrink in the proof of `run_edits_guarded`: that implication is an unstated corollary, not a fresh reading of the do-block.

Grep of `guardEdits` over `Lang/Proofs`, `Kernel/Proofs`, and `Ledger` on `51089fb`. Nothing in `Kernel/Proofs` or `Ledger`. In `Lang/Proofs` the names are:

- `guardEdits_never_stuck` (`Lang/Proofs/Rel.lean:635`) and `guard_never_stuck` / `guard_run_ok` (`:552`, `:524`): past extraction, each `runLaw` on a declared guard is not `.error .stuck`. Not "returned `.ok (.ok ())`".
- `guardEdits_unpinned` (`Rel.lean:686`): an unpinned upsert or retract is `rowUnpinned` before any guard. A refusal, not acceptance.
- `runMeasured_past_extraction` (`Provenance.lean:1159`), `program_run_past_extraction` (`:1214`), `program_run_past_extraction_live` (`:1184`), `runMeasured_past_extraction_sim` (`:1269`): if setup, the machine run, and extraction succeeded, then `program.run` **equals** the do-block whose last bind is `guardEdits`. They connect a run to the guard *call*. They do not say the call returned ok. Inverting the do-block under `run = .ok` is the missing lemma, and it is short.

`runSetup_spec` (`Lang/Proofs/Load.lean:419`) is the front half only: bounds, load, method, state, args, reads. No guard.

`method_live_run_sound` (`Lang/Proofs/LiveInvoke.lean:16`) is `RunOK` of the method body (`apply4`) at `resultTy`. `guardEdits` runs after extraction, outside that run (`Program.lean:461`).

`LawMeaning.lean`: the theorems are law-term correspondence (`law_bigStep_back`, `LawTerm.same`, `lawTerm_fill`, …). None mentions an edit guard. `activity_start_state` / `activity_resume_state` (`StdActivityMethods.lean:9`, `:64`) are BigStep facts about the generated method's *state*; the resume docstring says the row guards judge the emitted edits separately.

So obstacle 3 is real. Naming `program_run_past_extraction` is why route (i) is a corollary. It is not a landed `run = .ok ⇒ guards accepted`.

## 2. The trace drops the rows; carrying them is one history, more information (READ)

Confirmed from the constructors. `ObjectStep.invoke` (`History.lean:96`) and `.nested` (`:107`) bind `rows` from `X.program.run … = .ok (s, calls, rows, used)` and store `(look, pkg, laws, r, stateOf cell, s, calls)` (`:103`, `:114`). `write` (`:84`) and `law` (`:92`) have no rows. `Req` (`Call.lean:317`) holds agent, principal, self, window, occasion. Not args, not edits. `object_history_runs` (`History.lean:404`) gives the rows back only as `∃ rv method args fuel rows used`. That existential is not the admitted rows: another `args` could return the same `(new, calls)` and different edits. Rows are not a function of the trace.

Putting them on the trace element is the right shape for a theorem that names the admitted edits: one inductive, the witness the constructors already required, a bijection with today's histories (`write`/`law` carry none). It is not fork C. It does not by itself change what the state-law chain or the payout bound say. It does change elaborated statement digests, which GATES-20t records as meaning (`decisions/gates.md` GATES-20t; `gates/decls.py` `STATEMENT_KINDS = {theorem, axiom}`).

What each restatement actually is. "Same claim" means the consumer-facing proposition is unchanged and the digest moves only because the carrier moved. Not a stronger conclusion, not a different object.

`History.lean`, the seven public theorems, all mention `ObjectStep` or the 7-tuple, so all seven digests move:

| theorem | what the restatement is |
|---|---|
| `object_step_none` `:127` | Same claim: a `none` step keeps the entry. |
| `object_step_some` `:157` | Same claim about judge, state, calls, *unless* the restatement pins `e.rows` to the run. That pin is a stronger conclusion, and it is the only one in this file. |
| `object_step_live` `:209` | Same claim: a judged step starts live. |
| `object_history_of_audit` `:235` | Same claim: an audited log is a history. The witness trace is richer; the theorem does not use the new field. |
| `object_history_chain` `:357` | Same claim: judged steps are a `Std.Chain (Step [] t)` with the req/new-state map. The chain is still a state law. Rows do not enter it. |
| `object_history_runs` `:404` | Same claim about calls if rows stay existential. The natural restatement (the trace's rows are the run's) is a stronger conclusion. |
| `object_history_start` `:427` | Same claim: a judged history starts at a state the law reads. |

The five private theorems in that file do **not** move, and a `RESTATES-MEANING` line for any of them is `unused map line`: `invokeRun_occasion` `:143`, `admit_kind` `:220`, `judge_mem` `:290`, `reqData_occasion` `:329`, `occasion_relaw` `:335`. None mentions `ObjectStep` or the tuple. The IMPACT's "5 private ones, because the type differs" is wrong.

`HistoryWitness.lean`, four statements move (the IMPACT's "3" lists four lines):

| theorem | what moves |
|---|---|
| `object_history_chain_witnessed` `:27` | Same claim: the lift's premises hold together and the chain has length 1. |
| `h_history` `:114` (private) | Same claim: that write is an `ObjectHistory`. A write has no rows. |
| `write_history_witnessed` `:121` | Same claim: a write moves state (`e.new ≠ e.old`). |
| `object_history_needs_inForce` `:132` | Same tooth: drop in-force and there is no chain of that length. |

`h_receive`, `h_admit`, `h_live` do not move.

`EscrowInvokes.lean` (importer of `History`):

| theorem | what moves |
|---|---|
| `pair_steps` `:40` (private) | **Not in the IMPACT's list.** Same lemma: zip calls with chain steps. Must be named or the landing is `undeclared restatement`. |
| `escrow_invokes_one_payout` `:66` | Same claim: `payoutCalls ≤ 1`. Calls projection unchanged. |
| `escrow_invokes_deployed` `:97` | Same claim, deployed `Ctx`. |

`EscrowAdmitted.lean` (imports `EscrowInvokes`, so it is in the transitive reach; `gates/tree.py` `dependents` is transitive):

| theorem | what moves |
|---|---|
| `hist` `:332` (private) | **Not in the IMPACT's list.** Same witness history. Must be named. |
| `escrow_history_witnessed` `:339` | Same claim: the premises hold and `payoutCalls = 1`. |
| `escrow_deposit_spends_cap` `:356` | Same claim: the deposit's one transfer spends the cap. |
| `escrow_short_cap_refused` `:380` | Same tooth: cap `amount - 1` is `transferSpent`. |

`Lang/Proofs/Chain.lean:29` is a docstring and the module does not import `History`, so it is not in the reach. No line.

No other `.lean` file mentions `ObjectHistory`. The cone is these four modules. Count of statements whose digest moves: 7 + 4 + 3 + 4 = **18**, not "7 + 5 + the lines they listed". The five they included do not move; `pair_steps` and `hist` do. "0 hypotheses" matches the design (a field, not a premise) and is INFERRED until a digest exists. It is not a reason to pay the 18.

## 3. A is B plus a carrier (READ)

B, as this read was given it: every admitted step on an activity object is an enabled action of its projection. That is PROT-4's `monitor_safe`.

A's formula (`IMPACT-PROT-1` §2) is that sentence spelled at guard grain: for each log edit in the trace, `(phase of its old row, the edit, phase of its new value) ∈ activityEdges`, plus signer / capture-unchanged / answered-before-retract. Those conjuncts are `waiting_insert_iff`, `waiting_upsert_iff`, `waiting_retract_iff`, `waiting_no_replay`, `waiting_upsert_preserves_capture` (`Lang/Proofs/StdActivity.lean:208`, `:320`, `:88`, `:117`, `:233`). They are what "enabled" means for `activityWaiting`. They are not a further theorem.

The comment on that formula mentions `Reach activityEdges (phase at w) (phase at w')`. The formula does not state it. Phases are read off the edits in the trace, and `guardEdits` (`Program.lean:428`) judges every edit of one run against the pre-run view (`es.mapM guardOld`, then `forM`). There is no intra-run threading to prove. Cross-step threading of `w.rows` is `rowsRun_eq` (`Kernel/Proofs/Admit.lean:400`) plus the seal of the run's rows into `Turn.rows` (`Call.lean:550`, `sealTurn` `:568`). That is a landed kernel fact about every turn, not an activity fact. A `Reach` stated on `w.rows` would go red if admit stopped applying row touches, and that same edit reds `rowsRun_eq`. It is not a tooth of a new theorem.

The separator this read was told to look for does not separate them. `world/resident/Bell.ob:11–20`: `answer` is an author method. It upserts `rings` and retracts `pending` itself; it does not call `resume_ask` (`ring` at `:22` is the one that calls `start_ask`). The log guard is still `rung`, i.e. `activityWaiting` (`Bell.ob:8`, `StdActivity.lean:69`). A method outside the generated machine that passes every row guard is the deployed Bell, and both A and B are true of it. The plan's tooth ("a method outside the declared machine → no Reach") is a tooth of a method-indexed machine. `Std.activity` has no phase field (`StdActivity.lean:91`) and `machine_reached` (`StdChain.lean:100`) is a `Chain` of `machineLaw` over a state field. That composition has no object. The IMPACT is right about obstacle 1, and right that this method is not a red of the guard-grain statement (`IMPACT` §2 P3).

So A adds nothing B lacks. Fold the step fact into PROT-4. Do not land it as a history card, and do not pay 18 restatements to write ∀ steps, B(step) on a wider trace.

## 4. The plants are not PROT-1's teeth (READ)

P1 and P2 are distinct mutations. Neither is a tooth of a history theorem.

- **P2** deletes `activityWaiting`'s upsert arm `("some", refusedT "answered")` (`StdActivity.lean:88`). That is already `activity_answer_no_replay` (`StdActivityTeeth.lean:72–73`): `actGuard "r" (upsert of an answered row) = some "answered"`, `decide +kernel`. It is also `waiting_no_replay` (`StdActivity.lean` proofs `:117`). Both go red before any history theorem is asked. `run_edits_guarded` stays true: the guard ran and returned ok, the ok is now "accept a second answer". P2 is not PROT-1's tooth.
- **P1** deletes the `guardEdits` line in `runMeasuredWith` (`Program.lean:461`). The guard term is untouched, so `activity_answer_no_replay` stays green. The equality in `program_run_past_extraction` (`:1214`) becomes false: its right-hand side is that line. A history statement "edits in the trace are edges" stays true of every method that still emits only legal edits; dropping the call does not by itself emit `answered → answered`. The IMPACT's plant is two edits compressed into one (drop the call, and emit a bad upsert). The half that reds the edge set is P2's edit. The half that reds "guards ran" is already the landed pipeline equation.

## 5. The price (MEASURED against GATES-20t; the "0 hypotheses" is INFERRED)

GATES-20t: a theorem or axiom whose elaborated statement digest differs needs `RESTATES-MEANING`, and the statement must differ; a line for an unchanged statement is `unused map line`. Hypotheses are not what the gate counts.

Under A the gate would accept a map that names the 18 statements in §2 and does not name the five private lemmas. The IMPACT's map is not that map. Zero new hypotheses is consistent with adding a field and no premise, and is not yet a digest.

Public theorems whose statements a consumer outside Lang sees: `escrow_invokes_one_payout`, `escrow_invokes_deployed`, `escrow_history_witnessed`, `escrow_deposit_spends_cap`, `escrow_short_cap_refused`. They do not get stronger and they do not become a different proposition. Each still says what it says about calls, the cap, and `transferSpent`. The binder's trace type changes, so the digest changes, so the gate wants a line. The ledger gains nothing it can use. That is the reason not to grant the restatement, not a dispute about the count.

## 6. NanoBridge stays, and `nano_runs_iff` is PROT-3's tool (READ)

`Lang/Contextual/NanoBridge.lean` embeds `Hosting.Resident.Prog` (`cmd | keep | forget | ask | say`) as a `Prot` with index `Unit` and no holes. It is not an activity, and it does not mention a log row. `nano_runs_iff` (`Lang/Proofs/Contextual/Protocol.lean:906`):

`ResidentRun.Runs p es a ↔ ∃ tr, Runs (ofProg p) tr () a ∧ tr.map toEv = es`.

`tick_order` (`Hosting/Proofs/ResidentRun.lean:273`) is `Runs (tickP w m) es a → TickCore`. The plan's `bell_resident_conforms` is that order read across this equivalence. PROT-1 deletes nothing in `NanoBridge.lean`. PROT-3 consumes it. The plan's "becomes the activity instance, or goes" has no object: the two embeddings are different programs.
