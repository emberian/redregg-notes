VERDICT: RULE E2 — shrink the transport premise to one byte-relay sentence before any socket theorem is built; (a) may land now

CX-E2 pre-build read, 2026-10-22, nano `origin/main` = `1fc905f` (fetched; HEAD of the checkout is behind, so every nano path below is `git show origin/main:<path>`). No build. Nothing in the tree edited. Tags: READ, MEASURED (a command), INFERRED.

The card as priced in IMPACT-E2 PART 2 does not pass NVM §E.2. T0 is the right decider and it is necessary. R4, R5, R6 and R8 do not have to move. The `gates/tcb.tsv` row as written is not law 2: it trusts three replies Rust synthesizes. Shrink that row, or the model is a model of Rust.

## (1) The measurement — the nine are real; R7 is the one that can say ok

COUNT = 9 stands (READ the Rust and the Lean it calls, at `1fc905f`). Each is a branch on the resident's `cmd` path that changes the `Except String Reply` the resident's `Runs` sees, or changes which reply a later branch will hand it. NVM §E.2's refuter is met: the count is greater than zero past byte transport and lifecycle, so a Lean decider comes first and the price rises by it. The IMPACT's PART 1 is right about which one.

| id | real? | changes what the resident sees | can it make `exit = ok`? |
|---|---|---|---|
| R1 | yes, but not on this resident's argv | `.ok {exit = refused}` if it fired | no |
| R2 | yes | `.ok {exit = client}`, which `deliverP` treats like `.error` | no |
| R3 | yes, dormant under stdio custody | `.ok {exit = hostContradicted}`, same treatment | no |
| R4 | yes | which non-ok end, via the attempt | no |
| R5 | yes | whether the attempt settles, via the three-line parse | only by relaying follow's own `settle` word |
| R6 | yes | the loop around `Attempt.next`, including the fuel end | no: `next` returns `.committed` only from a confirm/probe seen `.committed` |
| R7 | yes | step 4's result byte | **yes. the only one** |
| R8 | yes | a nested sign/submit becomes `Lost`, not a resident exit | no |
| R9 | yes, and it is lifecycle | `.error` until the follower has answered | no |

READ, the ok path. `Protocol/Command/Machine.lean:981-985`: `settled` takes `(X, out, result)` and no World. `result[0] = Action.committed` is `.done CommandExit.ok`. The phase-4 arm is `:1218`, `| _, 4, [_, _, _, out] => same (settled X out result)`. The byte is built in `client/src/run.rs` on `Step::Submit`: `State::Settled { committed: true, .. }` becomes `Action::Committed`. `Attempt.next` (`Protocol/Attempt.lean`) returns `.committed` only for `(.confirm, .committed)` and `(.probe, .committed)`, and those `Seen` values are follow's `settle` word (`settleSeen`), never the host status (`hint` in `run.rs` only classifies `submit`/`lookup`). So R4 cannot forge ok. R5 can only report committed when follow's `receipt` command printed `settle committed`, which is `settleOf` (`Machine.lean:902-911`, printed at `:1153-1155`). R6's fuel end is `Action::Uncertain` (`attempt.rs`, `for _ in 0..=3 * sends_max + 1`). R8's `nested()` is a `RunError::Follow`, and `receipt()` turns that into `Reply::Lost` (IMPACT's "via R5" is the wrong arm; the effect is still Lost). None of those is `exit = ok` unless R7's byte says committed.

**The trust gap, named, and it is not this card's.** Today the follower can report `done ok` for a call its own World has not admitted. `settled` never reads `settleOf`. The docstring at `:978-980` says committed and refused are "only as the member's follow settled them"; the function does not look. A plant that answers step 4 `Committed` on a declined end (IMPACT §2.1) makes follow say ok, `deliverP` (`Hosting/Resident/Run.lean`, the `exit = ok` arm) forgets the kept answer, and the ring is still pending. Call it **step-4 byte trust**: a member's invoke success on the deployed path is Rust's reading of the attempt end, not a check follow makes at the moment it says ok. PROTOCOL-46's nested `receipt` command does check the World; step 4 trusts Rust to relay that word. Independent of E2. T0 closes it. It should be named in the decision whether or not E2 lands.

R1 (READ `client/src/stdio.rs` `answer`, and `Protocol/Command/Stdio.lean`). `undecodable` and `notOnSurface` are a refusal synthesized in Rust. Lean has `Verb.onStdio`, `stdioWords`, and `StdioRefusal`; it has no function from argv to that reply. The resident's own argv cannot hit it: `describeArgv` and `pendingArgv` start `read`, `invokeArgv` starts `invoke` (`Hosting/Resident/Bell.lean`), and both verbs are `onStdio` (`Stdio.lean`). The empty-argv arm of `Cmd.argv` is the `answerArg = none` node, which `deliverP` does not build. R1 changes what *nd* would answer a stranger; it does not change this resident's trace. Counting it is what the refuter's "synthesis of a reply" asks, and discharging it by `resident_argv_on_stdio` is right.

R2 (READ `stdio.rs` `answer`'s `Err` arm, `command_exit::CLIENT`, frame status still `status::OK`). The resident sees `.ok`, not `.error`. `deliverP`'s else arm is `answer unsettled exit N` and `.next m` with `kept` unchanged, the same effect as the `.error` arm. `DeliverAfter` (`ResidentRun.lean:75-84`) already says both tails are `rest = []`.

R3 (READ `run.rs` `reconcile`). An armed rotation whose attempt ends `Contradicted` returns `Done (hostContradicted, …)` and never starts the resident's command. Stdio custody is `refusing_rotation` (`stdio.rs`), so this resident does not arm one. Another nd on the same workspace can. Dormant on the single-resident path, still a branch in the function every command calls.

R9 (READ `decisions/hosting.md:2270`, HOSTING-41, line confirmed). The stdio pair starts only after an empty command decodes as a `Step`. The decision's own words: "No theorem added; this is Rust lifecycle plumbing." The resident sees `.error` from `Sockets.command` (`Hosting/Resident/Sockets.lean`, connect failure → `.error s!"io {e}"`). That is the lifecycle the refuter told the measurement to count, and it needs no decider.

## (2) The decider — only R7 moves; the premise as written covers decisions

**What must move.** R7, and nothing else of R4–R6, R8.

T0 (`settled` answers `.done ok` only when `X.decodeCall cb = some c` and `settleOf X me w c = .committed` on the World `Follow.loop` is holding) is the move that makes ok a Lean decision. READ `Host/Follow.lean` `loop`: `answer` calls `Command.step` on `⟨r.world, …⟩` and the next iteration is `{ r with world := fs'.world }`. The nested `receipt` command and the outer resume share that World. After T0, a lied `result[0]` with a World that has not admitted the call is `hostContradicted`, not ok.

R4–R6 and R8 then choose the `res` that `FollowRun` already quantifies, and they choose whether an ok happens. They cannot make ok true of a World that has not admitted the call. Moving the attempt loop into Lean would be a completeness theorem ("if the World committed, the resident sees ok"), which this card does not claim (§2.5, liveness absent). Leaving them as hints is what makes the model a model of Lean. Putting them in the premise, or in a second decider "so the count is zero", would be the twin.

**What the premise has to be.** One sentence, law 2, Rust moving bytes:

> an `.ok` reply whose `exit` is `CommandExit.ok` is the follower's Lean `done` of that command: `nd --stdio` gave follow the resident's argv, and gave follow back, byte for byte, every continuation follow handed out (`State.bytes`, `stateLayout = [.list argv, .byte phase, .list acc]`, `Machine.lean:215`), and the resident decoded follow's `done`.

`k` is opaque to Rust (`run.rs` resumes with the `k` follow returned). Adding the call bytes to phase 4's `acc` does not change `stateLayout`. That sentence does not trust a branch.

**The row in IMPACT §2.3 has grown, and the refuter fires on it.** It says the reply is follow's `done` *or one of nd's three named ends* (`notOnSurface`/`undecodable`, `client`, `hostContradicted`). Those three are R1, R2, R3: replies Rust synthesizes. `SocketRel`'s `.ok` arm is a disjunction that includes them, and `StdioLeg` is hypothesized by `answered_row_is_kept_answer`. A premise that classifies synthesized replies is a decision inside the trust boundary. NVM §E.2: the theorem would quantify over a Rust behaviour Lean does not decide. Shrink. Do not land that `tcb.tsv` row.

The shrink, precisely. For `exit = ok`, `SocketRel` is the `FollowRun`. Every other `.ok` exit, and every `.error`, is `True` — no claim, the same shape `.error` already has. R1–R3 are not inside the premise. They are discharged, where the resident cares, by two lemmas that trust nothing about Rust:

- `resident_argv_on_stdio`: a `Cmd` that `tickP` builds has an on-stdio first word (READ the three `*Argv` functions). This is why R1 is not on this trace.
- `deliverAfter_unsettled`: `exit ≠ ok ∧ exit ≠ refused` gives the same `DeliverAfter` tail as `.error` (READ the `else rest = []` arm, `:84`, and `deliverP`'s else). R2 and R3 are crash-stop *to the resident* as a theorem about `deliverP`, not as a fact the transport is trusted to guarantee.

`bell_resident_conforms` does not use the premise. It is not blocked on the shrink.

## (3) The model

`SocketRel` as written (IMPACT §2.2) is the grown one. After the shrink it is: `.error _` and any `.ok` whose exit is not ok are `True`; `.ok` with `exit = ok` is a `FollowRun` of `Command.start` on that argv, ending in that `done`. `FollowRun`'s `res` is some result, not a trusted one, and the World may fold between frames (`Follow.loop` serves one frame at a time; other commands can absorb). That over-approximation is the right one for ok ⇒ admitted.

**`x = .ok {exit = ok}` ⇒ a step whose receipt the follower built and checked.** Not from `SocketRel` alone. From the shrunk premise + T0 + `settle_committed`, yes, and the collision disjunct is not part of it.

- T0's `step_settled_ok`: a phase-4 `done ok` gives `settleOf X me f.world c = .committed h td` for the call in the continuation.
- `settleOf` *is* `ofReceipt` of `(Receipt.build …).answer` (`Machine.lean:902-904`).
- `settle_committed` (`Protocol/Proofs/Settle.lean`, section Member): that equality is `w.journalAt tx = some (h, td)`. No `CollidesAmong`. No `JournalCanon`. The other arms of `build_answer` contradict `.committed`.
- "Checked": `check_build` (`Receipt.lean`) says the receipt `build` produced checks against that World's own head as the answer it states. For a committed answer the `journalForgets` side condition is vacuous (`answer ≠ absent`). `check_build_reached` discharges canon/fit/refusals on a World folded from `genesisWorld`. READ `Host/Follow.lean` header: follow's Store is reopened as the writer's, folded with `World.step`. INFERRED the deployed follower World is such a fold; if the socket proof does not want to import `open`, the journal equality from `settle_committed` is the conclusion to state, and "checks" is `check_build` under that fold hypothesis on the *new* theorem only.

Routing (b) through `check_committed` (`Receipt.lean:43`, READ) is valid and strictly weaker: the conclusion gains `∨ CollidesAmong hash L` where `L` is the explicit list `check_committed` names (`rootsPre` of the receipt and the World, plus `inclPres` of the journal path). That list is bounded. It is not an unbounded `∃ a b, a ≠ b ∧ hash a = hash b`. The disjunct check passes if it stays. It should not stay. `settle_committed` already has the journal entry.

The continuation join is the premise, not T0. `step_settled_ok` says the call *in the continuation* is committed. That it is the call step 3 submitted is `FollowRun` requiring `r.cont = some k` and `step_submit_planned` (`Command.lean:303`: a `.submit` is `plan` on follow's World of that command's body). Rust substituting `k` is outside the shrunk premise, which is the right place for it: it is byte relay. Phase 4's `acc` is unauthenticated, as today (`Machine.lean` header: `k` cannot steer what is signed). Naming which call is checked, by bytes follow itself wrote and Rust returns verbatim, is the same trust the argv already needs.

**Crash-stop.** `.error` is already quantified. `Runs.cmd` takes `(x : Except String Reply)` (`ResidentRun.lean:53`), and every theorem over `Runs (tickP …)` is over every such `x`. `DeliverAfter`'s `.error` arm is `rest = []`: no forget, kept stays, next tick retries. That is crash-stop of connect failure, a mux close (`Reply.ofBody`, status ≠ ok → `.error s!"status {n}"`, `Sockets.lean`), a short frame, an undecodable body. It is **not** R2 or R3. Those are `.ok` with another exit. The plan's sentence "x = .error _ = crash-stop, already quantified by Runs" is true, and it does not cover the synthesized exits. `deliverAfter_unsettled` is the missing sentence, and it is a resident lemma, not a premise.

## (4) The theorems

### `answered_row_is_kept_answer` — do not land it under this name

The plan's statement (NVM §B.4, B8): every answered row is the text of some tick's kept answer. The Bell's `answer` method (`world/resident/Bell.ob`) upserts `rings[(agent, notBefore)]` to `answered (some (ask arg.text))` and retracts `pending`. No landed theorem says that about the compiled Bell (the IMPACT is right; PROT-4a left the Bell as the next witness). A theorem whose conclusion is the follower's journal entry is not that statement.

- **Nano object of what can actually be proved:** one deployed tick (`Runs (tickP w m)`, the tree `tick` performs) together with the member follower's World: an invoke of `(sh, r, t)` answered `exit = ok` means the kept pair is `(r, t)` (or this tick kept it) and follow's World journals the call whose argument is `answerDatum r t` at `(conf.bell, sh.answer)`.
- **Weaker without it:** exit ok is not tied to a committed call. The two projections do not join. The answered *row* stays a journey row either way, until the Bell witness exists.
- **Disjunct check:** `settle_committed` has none. If the proof goes through `check_committed` instead, the disjunct is `CollidesAmong` over that theorem's explicit list, which passes, and it is a weakening the route does not need. An unbounded `∃ a b` would fail the census. Do not write one.
- **Mutation:** revert T0 (the committed arm trusts `result[0]` again) and `step_settled_ok` has no object: RED. `deliverP` forgetting on exit `client`: the resident half RED, and `deliverAfter_unsettled` RED. Both are real.
- **Rename → docstring.** Landing this as `delivered_answer_committed` is the honest name for the journal conclusion. The plan's name does not silently move. `answered_row_is_kept_answer` stays as a docstring that the row (`rings[…].answered = some (ask t)`) is not stated, and it lands with the Bell witness or not at all. Do not delete LITP's "the join stays a journey row" until that statement exists. The IMPACT's DELETES line is wrong under its own rename.
- **The cited route stops one lemma short.** `step_submit_planned` gives `plan` of the command's `body`. `body`'s invoke arm (`Machine.lean:331-334`) is `Lang.argsOf` of the argument text, not `answerDatum`. `callArg = some (answerDatum r t)` and `callTarget = (conf.bell, sh.answer)` need the parse of `invokeArgv` (hex bell, decimal method, `Print.data` of `answerDatum`, `--via` grant) and the print/read roundtrip. That lemma is part of (b). It is not `step_submit_planned`.

The resident half (the kept pair) does not need `StdioLeg` or T0. The member half needs both, after the shrink.

### `bell_resident_conforms` — the cross-tick statement, not the projection

The plan's sentence (LITP §C.1, PROGRAM §3): `tick_order`'s `TickCore` path is a path of `proj bellG resident` via `nano_runs_iff`. There is no `Glob` in this card. `nano_runs_iff` lives in `Lang/Proofs/Contextual/Protocol.lean`; `NanoBridge.lean` is the embedding and says so. A theorem that only re-reads `tick_order` through that embedding has `tick_order`'s tooth and no new one.

READ why the plant does not bite the plan's sentence. `ActCore` *is* `match decideTick` (`ResidentRun.lean:98-104`). `tick_order` (`:273`) says the core is `TickCore`, which follows `decideTick`, whatever `decideTick` returns. `decideTick` (`Bell.lean`): `some (r, t)` with `r ∈ pending` is `.answer`, not `.ask`. Drop the membership test so a kept ring is asked again (`| some (r, t) => match pending with | q :: _ => .ask q`) and `tick_order` / `tick_counts` stay green. `decide_kept_first` / `decide_ask` (`Hosting/Proofs/Resident.lean`, the IMPACT's cites) go red. INFERRED from the definitions; the plant run is the build's, and sorry-ing those two only in the plant log is the right way to let the new name appear.

The builder's (a) is the statement the tooth fits. `Ticks` over successive `Runs (tickP)`, and between two spent asks of `r` (`askText ≠ none`: the frame left) some event `Frees` `r`: an invoke of `r` with `exit = ok`, or a read/reread whose `readRings` omits `r`. A not-sent ask is excluded, which matches the meter (a not-sent ask is forgotten and may be asked again). A failed read does not free, which matches `deliverP` (kept stays).

- **Nano object:** every chain of deployed ticks of one process life. `interp_runs` says `tick` performs `tickP`. `nano_runs_iff` reads the same path as a `Prot`. Cited, not re-proved. NanoBridge stays.
- **Weaker without it:** `tick_counts` is one ask *per tick*. Nothing says the next tick will not ask the same ring again while it is still pending and the answer has not been taken. Q2 ("two rings, two asks") and Q6 ("a restart asked again") have no theorem. One process life only: across restarts it is `resume_durable` / `seedOf`, which this statement does not compose (IMPACT §2.5, right).
- **Disjunct check:** `Frees` is a match on `Ev`. No hash. Nothing for the census to catch.
- **Mutation:** the `decideTick` plant above → (a) RED, `tick_order` GREEN. That is the tooth. The plan's projection sentence does not go red under it, so that sentence is a docstring: "not stated; this card has no `Glob`; PROT-3's object half is `bell_object_conforms`." The name `bell_resident_conforms` may stay on the cross-tick theorem only with that docstring. A rename that drops the projection claim without the docstring fails the same rule as the row.

(a) needs no premise and no T0. It is not blocked by this RULE. Landing it first, `hosting:`, is the right order.

## (5) Price

**0 on the theorems the plan names,** as statements, for (a) and for (b) after the shrink. READ: `tick_order`, `tick_counts`, `kept_follows`, `interp_runs` quantify over every `Except String Reply` already; nothing in (a) or in `StdioLeg` is a hypothesis of them. `check_committed`, `check_refused_sound`, `settle_final_never_admits`, `settle_committed` do not mention `settled` or the resident. `audit_ok` is not on this path (INFERRED: the card does not edit Kernel). `step_submit_planned`'s *statement* does not change; its proof calls `settled_ne_submit`, which is a proof edit.

**T0's own price.** `settled` gains the World, the self, and the call bytes. READ the four statement-level theorems, at the lines the IMPACT names:

- `settled_ne_submit` `Protocol/Proofs/Command.lean:217`
- `settled_uncertain` `:1130`
- `settled_ne_host` `:1281`
- `settled_cont` `Protocol/Proofs/Incoming.lean` (the theorem is `settled X out result`.cont = none)

Each gains binders and no hypothesis. I could not `git grep` the whole tree (the sandbox blocks `git grep` outside this scratchpad); those two modules are the ones the IMPACT names, and they contain exactly these four. The decls diff at the build is the measurement that there is not a fifth. `stateLayout` does not change (the new bytes are one more element of `.list "acc"`). INFERRED no codec vector moves, so the gate is `protocol:`, not `protocol!`, and not a flag day. If the build's vector diff is non-empty, that inference is wrong and the gate is `protocol!`; say so then, do not pre-declare the flag day. No Store re-genesis on what I read. Hosting's part is `hosting:` (proofs, `gates/tcb.tsv`, test docs). The Bell does not re-cut.

**RESTATES:** the four `settled_*`, binders only. Hosting: none.

**DELETES:** none in nano for this landing. The ResidentRun header may *name* the shrunk premise as what the join still trusts; it must not read as a hypothesis `tick_order` gained. LITP's "the join stays a journey row" is not deleted by the journal theorem. It is deleted by `answered_row_is_kept_answer` stating the row, which this card does not.

**Not claimed, and should stay unclaimed.** Who else holds the resident's key (the converse, "no answered row that is not a kept answer", needs HOSTING-32's sandbox). Restarts. Liveness. That R4–R6 implement `Attempt.next` faithfully. That an ok reply's stdout is the receipt text (`settled` returns `out`, which step 3 stored from the *pre-submit* `receive`, not from the committed journal — T0 must not start trusting `out`).

## What would make this RELEASE

1. The `tcb` row is the one sentence in §2, and `SocketRel` claims nothing about R1–R3.
2. T0 is in before (b). R4–R6 and R8 are not in Lean and not in the premise.
3. (b)'s member half is `settle_committed`, journal entry, no collision disjunct; the invoke-argv lemma is named; the Bell row is a docstring under `answered_row_is_kept_answer` until a LANG card states it.
4. (a) is the cross-tick theorem, with a docstring that it is not `proj bellG`.
5. The step-4 byte trust is named as a deployed gap T0 closes, not as something E2 invented.
