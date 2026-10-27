VERDICT: RULE E2b — the byte premise stands and is not reopened; before the socket theorems are built, name this theorem's plant (not T0's) and say a commit whose reply is lost is PROT-5

CX-E2b re-read, 2026-10-23, nano `origin/main` = `b4a7f38` (fetched; `d0d67f1` is its parent, not the tip). (a) `bell_resident_conforms` is that commit. T0 is not on `origin/main`; it is the candidate diff in `promo/E2/T0-candidate.diff` (IMPACT §4). No build. Nothing in the tree edited. Tags: READ, MEASURED (a command), INFERRED.

## (1) The premise is one sentence about bytes, and none of the three can yield ok

The row, exact text (IMPACT §5.1; the §2.3 row is withdrawn, and it is not in `gates/tcb.tsv` at `b4a7f38`):

```
stdio-leg	client/src/{stdio,run,sockets,frame,mux}.rs, client/src/bin/nd-supervise.rs (tree)	trusted-unverified	HOSTING	an ok reply whose exit is CommandExit.ok is the follower's Lean done of that command: nd --stdio gave follow the resident's argv, gave follow back byte for byte every continuation follow handed out, and the resident decoded follow's done (Hosting.Proofs.Socket.StdioLeg)	nd --stdio's relay proved in a verified transport
```

The trusted-for clause is one sentence. It says Rust moved three byte fields (argv into `start`, each continuation back into `step`, the `done` out to the resident). It does not classify a reply, and it does not mention an attempt end. `attempt.rs` is not in the path list. That is right: the attempt loop is R4–R8, and after T0 it only chooses the `result` a step is handed.

It does not trust the three from the first read.

- **client-exit.** READ `client/src/stdio.rs` `answer`: the `Err` arm builds `CommandReply { exit: command_exit::CLIENT, .. }`. MEASURED `git grep command_exit::` at `b4a7f38`: production Rust assigns `REFUSED` (`stdio.rs` screen, `join.rs`) and `CLIENT` (`stdio.rs`, `nd.rs`'s process exit). It never assigns `command_exit::OK`.
- **hostContradicted.** READ `client/src/run.rs` `reconcile`: an armed rotation whose drive ends `Contradicted` returns `Some((t.host_contradicted, [], line))` and `run` returns that without calling `follow.command`. Not `OK`.
- **status → Seen.** READ `run.rs` `hint` and `Protocol/Attempt.lean` `next`. A Host status of ok becomes `Seen.committed`, and `next` on `(.submit, .committed)` or `(.lookup, .committed)` is `.confirm`, never `.committed`. `Action.committed` is only `(.confirm, .committed)` and `(.probe, .committed)`, which are follow's `settle` word (`settleSeen`), not the Host status. The mapping cannot write an exit, before or after T0.

Who writes `exit = CommandExit.ok`. READ the only two Lean producers, `Protocol/Command/Machine.lean`: `printed` (`:168`) and `settled`'s committed arm (`:985` at `b4a7f38`). `printed` is read, describe, range, sync, receipt, init's join line, adopt, invite, and a recorded cancel (`:1048`). An `invoke` matches none of those arms (`step`'s match, `:1092–1281`): its only `done ok` is phase 4. Rust's `command` returns `Ok((exit, stdout, stderr))` only from `Step::Done { exit, stdout, stderr }` (`run.rs`); `stdio.rs` copies that `exit` into `CommandReply`. The resident decodes `commandReplyLayout`, which is `Step.layout .done` (`Protocol/Command/Stdio.lean:61`). Continuations: `next` is `State.bytes` (`Machine.lean:243–245`); `FollowSocket::resume` sends `Resume { k: k.to_vec(), .. }` (`client/src/sockets.rs`); follow's `answer` passes the decoded `k` to `Command.step` (`Host/Follow.lean`). No branch rewrites `k`.

So the sentence is a byte-relay claim. It is not a decision claim: it does not say what Lean must have checked before it emitted ok.

**T0 is what makes the ok bit Lean's, and it is not on main.** At `b4a7f38`, `settled`'s committed arm is `result[0] = Action.committed`, World unread. A plant that writes that byte (R7) makes follow say ok for a call the World has not admitted. The candidate (`T0-candidate.diff`) changes that arm to `ownSettle = some (.committed _ _)`, i.e. `decodeCall cb` and `settleOf` on the follower's current World, and proves `settled_ok` and `step_settled_ok`. READ the diff: every other arm of `settled` stays a non-ok exit. After that landing, no synthesized reply and no synthesized result byte yields ok unless the follower's own World journals the call. The 727-job green is the builder's measurement (IMPACT §4); this read did not rebuild.

The sentence is therefore true of the relay on `b4a7f38`, and it is a byte-relay claim rather than a decision claim only once T0 has landed as that candidate. Building `delivered_answer_committed` against `b4a7f38` would quantify over R7. The card already orders T0 first (§5.5). That order is binding. It is not a new fight about the sentence.

## (2) The socket theorems

`SocketRel` as restated (§5.2) matches the sentence: `.error _` is `True`; an `.ok` claims a `FollowRun` only in the consequent of `exit = ok`. R1–R3 are not in it. `FollowRun` quantifies the `result` and allows the World to extend between frames, which is what `Follow.loop` does (one frame, other commands absorb). Right shape for ok ⇒ admitted.

### `delivered_answer_committed`

- **Nano object.** One deployed tick, `Runs (tickP w m)`, and the member follower's World at the `done` of that invoke's argv. `tick` performs `tickP` (`interp_runs`). Not the Bell's row, not a `Glob`.
- **Weaker without it.** `bell_resident_conforms` says an ok invoke frees the ring. `tick_counts` says the invoked pair was the kept answer. Nothing joins that pair to `journalAt` of the call whose argument is `answerDatum r t` at `(conf.bell, sh.answer)`. Under the premise an ok reply is some follower `done`; without this theorem that `done` is not this ring's answer bytes.
- **Disjunct check.** The route is `settle_committed` (`Protocol/Proofs/Settle.lean`, section Member). READ it: `ofReceipt _ _ _ _ (Receipt.build E w tx).answer = .committed h td → w.journalAt E tx = some (h, td)`. The flags are arbitrary, so `settleOf` (which is `ofReceipt` of that answer, `Machine.lean:902–904`) inherits it. No `CollidesAmong`. The `check_committed` route in §2.4 is withdrawn. The collision disjunct in `settle_refused_final` is the refused arm; this proof must not pick it up.
- **This theorem's mutation, not T0's.** P-T0c (the committed arm trusts `result[0]`) reds `settled_ok`. That is T0's tooth. `deliverP` forgetting on exit `client` reds `deliverAfter_unsettled`; it does not make this statement false, because the statement is about `exit = ok`.

  The tooth is the argv join. READ `Hosting/Resident/Run.lean:268–272`: `Cmd.argv` of `.invoke sh r t` sends `invokeArgv c sh` of `answerArg r t`, and the event stays `.cmd (.invoke sh r t)`. Plant that arm to print `answerArg r r.text` (the ring's own text in the `text` field; `ringText` is still `r.text`, so the bell's `rung: text` guard still admits, `Hosting/Resident/Bell.lean` header and `world/resident/Bell.ob` `answer`). For a kept answer `t ≠ r.text` the tick's ok invoke journals `answerDatum r r.text`, not `answerDatum r t`. `delivered_answer_committed` RED. `settled_ok` and `step_settled_ok` GREEN (the call that was submitted decodes and is committed). `tick_counts` and `bell_resident_conforms` GREEN (the event still carries `t`; an ok invoke still frees `r`). `answerArg_reads` GREEN (it is about `answerArg`, which the plant did not change). Deployed, the bell row answers `ask` of the ring text, not the kept answer: the answer-text row of `resident_bell.rs` RED.

  `invoke_done_ok_phase4`, `step_submit_cont`, and `invokeArgv_body` are real lemmas, not padding. READ: an invoke's only `done ok` is phase 4; phase 3's continuation is `again 4 […, X.callBytes c]`; `body`'s invoke arm is `Lang.argsOf` of the argument text (`Machine.lean:331–334`), and `parse` of `invoke OBJ METHOD ARGS --via` keeps that text (`Verb.lean:349–352`). The description/`readTy` roundtrip inside `invokeArgv_body` is the large piece, as the builder says. It is part of (b). It is not `step_submit_planned`.

### `answered_row_is_kept_answer` — a real dependency, not a deferral

The row is `Bell.ob`'s `answer`: upsert `rings[(ringer, notBefore)]` to `answered (some (ask arg.text))` and retract `pending`. READ `Lang/Proofs/StdActivityMonitor.lean` header: `activity_monitor_safe` covers a package whose guard field is the generated waiting guard, and "the compiled Bell's `rung` field is the waiting guard is the next witness, not decided here." `WaitingStep.answer` is the shape of an upsert, not this method's `ask` of this text. No landed theorem reads the compiled Bell. Holding the name for a LANG card (`bell_monitored` / the `answer` method off `runMeasured`) is the dependency PROT-4 already named. `one_ask_per_ring` waiting on the same witness is the same fact. LITP's journey-row sentence stays. Do not delete it in this landing.

## (3) Crash-stop, and the commit whose reply is lost

`.error` is already quantified. READ `Hosting/Proofs/ResidentRun.lean:53`: `Runs.cmd` takes `(x : Except String Reply)`, and `:76` `DeliverAfter`'s `.error` arm is `rest = []` (no forget, kept stays). Every theorem over `Runs (tickP …)` is over every such `x`, including connect failure, a mux close (`Reply.ofBody`, status ≠ ok → `.error`), a short frame, an undecodable body.

The model says nothing about a follower that commits and then dies before the reply. READ `Host/Follow.lean` `loop`: on `.steps ts`, `append` runs and only then `port.send`. A crash in that window leaves the step in follow's store and no reply. The resident sees `.error` (`Sockets.command`, `io …`) or, if `nd` is what dies inside `run`, `.ok {exit = client}` (`RunError::Follow`). `SocketRel` claims nothing in either case (the ok-implication is vacuous; `.error` is `True`). It does not say the step was not committed, and `delivered_answer_committed` does not say ok is the only way a commit happens.

That is PROT-5, not this card. PROGRAM §3: `submit_at_most_once` (B9) over Submit's journal-first retry; a lost reply must not admit twice. The resident already behaves as a retry: READ `deliverP` (`Run.lean`, the refusal paragraph) — "a delivery that landed but whose reply was lost" is re-read and forgotten when the ring is no longer pending. That prose is not a theorem here. §5.3's NOT claimed list (stdout, custody, restarts, liveness, `Attempt.next`) does not name this window. Say so, in the module docstring and in §5.3: a commit whose reply is lost is PROT-5's at-most-once, out of scope; this card does not claim the converse of ok ⇒ journaled.

## (4) Price

**0 on landed theorems**, as statements. Nothing in §5 adds a hypothesis to `tick_order`, `tick_counts`, `kept_follows`, `interp_runs`, `step_submit_planned`, `settle_committed`, or `answerArg_reads`. T0's four `settled_*` restate with a binder each; that price belongs to T0's landing, not this one. The three new Protocol lemmas are new declarations. INFERRED from the statement diff; the decls diff at the build is the measurement. This read did not build.

**The tcb row** is the sentence in §1. `hosting:` fast: `Hosting/Proofs/Socket.lean`, `gates/tcb.tsv`, no byte, no row fixture, the Bell does not re-cut. The three Protocol lemmas are `protocol:` proof-only under the cross-layer grant (no layout: T0's call bytes are one more element of `stateLayout`'s `.list acc`, and `stateLayout` does not change). Not `protocol!`. Not a flag day.

RESTATES none in this landing. DELETES none. The ResidentRun header may name the shrunk premise; it must not read as a hypothesis `tick_order` gained.

## What the build must contain

1. T0 is on main as the candidate: `done ok` at phase 4 only when `ownSettle` is `.committed`. Not true of `b4a7f38`.
2. The plant that is run for `delivered_answer_committed` is the argv plant in §2, and the log shows `settled_ok` still green.
3. The NOT claimed sentence in §3 is in the module docstring.
