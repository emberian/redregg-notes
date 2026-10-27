VERDICT: RELEASE E2b-LANDING

CX-E2c re-read, 2026-10-23. hbox wt/e2 HEAD `28e2d88`, uncommitted: `Hosting/Proofs/Socket.lean` (536), `gates/tcb.tsv`, `decisions/hosting.md`. No build. The tree was not edited. Tags: READ, MEASURED (the row compare; the plant logs as saved).

## (1) The row

Yes. The live `stdio-leg` line equals the sentence in READ-E2b §1, six tab fields, byte for byte. `SocketRel` did not grow back: an `.ok` claims a `FollowRun` only when `exit = ok`; `.error` is `True`.

## (2) `delivered_answer_committed`

The statement is R-0065's text grain, not the strong form. Conclusion: the kept pair (or this tick's `keep`), and a journal entry `wf.journalAt (txIdOf ⟨u, sig⟩) = some (hh, td)` of a call planned on follow's World that invokes `o = digestOf conf.bell` at `sh.answer`, args = `Lang.argsOf` of the text `answerArg r t` at that object's method, grant included because the argv carries it. Codec premise `hX` is `Host.Proofs.Refine`'s (`decodeCall b = some c → callBytes c = b`), named as discharged by `Codec.Proofs.Deployed.eq_callBytes_of_decodeCall`. No `callArg = answerDatum`. No collision disjunct (`settle_committed` is `journalAt = some`). `answer_args_at_answerArgTy` takes no `StdioLeg`; the equality is under `sg.arg = answerArgTy`.

The three triggers are in HOSTING-42, including (iii) as Protocol Describe + `readTy_ty` + wf of a loaded package's arg types. The lost-reply sentence is in the module docstring, the theorem docstring, and HOSTING-42: a commit whose reply is lost is PROT-5's at-most-once; the converse of ok ⇒ journaled is not claimed.

The argv plant (`Cmd.argv`'s invoke arm prints `answerArg r r.text`) reds that theorem and not T0's. Both saved whole-tree tails (`plantArgv.log` at e2905e7, `plantArgv-tip.log` at 28e2d88) have one failure, `Hosting.Proofs.Socket`, at `:484` (`rw` of `answerArg r t` inside `delivered_answer_committed`): the goal is `answerArg r r.text` against the text for `(r, t)`. `ResidentRun` and `BellConform` rebuilt green in the same logs. On the planted tree, `plantArgv-tip-green.log` elaborates `settled_ok`, `step_settled_ok`, `tick_counts`, `bell_resident_conforms`, `answerArg_reads` (axioms propext, choice, Quot.sound) and `#print`s the planted argv. Deployed Q2 (`plantArgv-bell.log`) reds by name: answers `from-c` / `from-op`, not `hello back`.

## (3) `answered_row_is_kept_answer`

A docstring only (module header, the theorem's doc, HOSTING-42). No declaration of that name. The trigger named is the Bell witness: `activity_monitor_safe` plus the compiled `answer` method. LITP's journey-row sentence is not deleted.

## (4) sorry, decls, price

No `sorry`, `admit`, or `native_decide` in `Socket.lean` (`decide` on the hex lemmas is kernel `decide`). No landed `.lean` is in the diff, so no Hosting or Protocol statement moved: decls CHECK 1 has nothing to name (0 map lines; the judge was not re-run). Price 0. New hypotheses sit on the new theorems only.

## (5) `hosting:` fast

Right. The change is a Hosting proof module, one tcb data row, and a decision. No Lang path, no Protocol path, no layout. `gates/fast.py` is `fast` unless the subject is a flag day or `gates/*.py` / `scripts/` change; `hosting:` is neither.
