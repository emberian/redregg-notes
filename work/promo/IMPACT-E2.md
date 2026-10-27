# IMPACT-E2 · the member-socket model (E2) + PROT-3's host half (`bell_resident_conforms`)

CX-E2, 2026-10-23, nano `origin/main` = `1fc905f` (hbox `wt/e2`). Plan PROGRAM-20261022.md §1 B8, §3 P3 "PROT-3 + E2";
NANO-VS-MINI-20261022.md §B.4 E2 and §E.2 (the refuter); LITERATURE-PROTOCOLS-20261022.md §C.0/§C.1 PROT-3; ruling R-0052.
Tags: READ (read at `1fc905f`), MEASURED (a command's output), INFERRED. PART 1 was written before any model.

## PART 1 — the measurement: one resident `cmd`, end to end, and every Rust decision on it

### 1.1 The trace (READ)

One `Prog.cmd c k` node of the resident's tick, `c = .invoke sh r t` (the answer), followed to the writer's `submit`:

| # | where | layer | what happens |
|---|---|---|---|
| 1 | `Hosting/Resident/Run.lean:314` `ioHandler.cmd` | Lean (resident) | `Resident.command w.member (c.argv w.conf)`; argv is `Cmd.argv` (`:268-273`), a function of the node |
| 2 | `Hosting/Resident/Sockets.lean:71-80` `command` | Lean | `commandPayload` (Table's `commandLayout`, `:44-52`); one connection to `MEMBER/<r>/nd.sock`; frame `u32le len ‖ Op.command ‖ payload`; read one body; `Reply.ofBody` (`:61-68`): status ≠ ok → `.error "status N"`, else decode `commandReplyLayout` = `Step.layout .done` (`Protocol/Command/Stdio.lean:61`) |
| 3 | `client/src/bin/nd-supervise.rs:137` → `client/src/mux.rs:360-417` `forward` | Rust (mux) | the connection's frame re-tagged `u32le conn ‖ op ‖ payload` onto the child's stdin; closes named by Lean's `CloseReason` with Lean's bounds |
| 4 | `client/src/stdio.rs:92-117` `serve` → `:50-88` `answer` | Rust (`nd --stdio`) | decode `Command`; screen the first word against `STDIO_VERBS`; connect `follow.sock` and `host.sock`; `run::run` |
| 5 | `client/src/run.rs:213-225` `run` → `:184-210` `reconcile` → `:229-320` `command` | Rust | an armed rotation driven first; then perform follow's steps until `Done` |
| 6 | `client/src/sockets.rs:58-121` `FollowSocket` | Rust | `command(argv)` / `resume(k, outcome)` frames; status ≠ ok → io error |
| 7 | `client/src/bin/nd-supervise.rs` (the follower's own pair, started by nd-members) → `Host/Follow.lean:91-150` `loop` → `:58-84` `answer` | Lean (follower) | `Command.start` / `Command.step` (`Protocol/Command/Machine.lean`) on follow's World; absorbed steps appended before the reply |
| 8 | `Protocol/Command/Machine.lean:1186-1202` (step 3) | Lean | re-plan, compare with what custody signed, `receive X w c` on follow's World, then `.submit (X.callBytes c) k` |
| 9 | `client/src/run.rs:280-315` `Step::Submit` → `client/src/attempt.rs:224-296` `drive` | Rust | freeze the call; drive the attempt by the emitted `attempt::next` (`Protocol/Attempt.lean:115`): `submit`/`lookup` over host.sock, `confirm`/`probe` as a NESTED `receipt CALL` command on the same follow socket (`run.rs:135-161`) |
| 10 | host.sock: nd-supervise mux → `Host/Serve.lean` `submit` | Lean (writer) | `Receive.judge` once; commit what it returns (`Host.Proofs.Serve.step_submit`) |
| 11 | `client/src/run.rs:292-314` | Rust | the attempt's end → step 4's result `u8 Action.code ‖ payload` |
| 12 | `Protocol/Command/Machine.lean:1218` → `:981-996` `settled` | Lean (follower) | `result[0] = committed` → `.done CommandExit.ok`; `refused` → `refusedAt`; `open`/`contradicted`/`uncertain`/`badReply` → their exits |
| 13 | `client/src/stdio.rs:76-81, 109-115` | Rust | `Done (exit, stdout, stderr)` encoded as `CommandReply`, framed `conn ‖ status::OK ‖ bytes` |
| 14 | mux `route` (`mux.rs:421-470`) → resident `Reply.ofBody` → `deliverP` (`Run.lean:335-363`) | Rust → Lean | exit ok → forget the kept answer; exit refused → re-read `pending` and judge by rows; any other exit → `answer unsettled`, retry next tick |

Process lifecycle around it: nd-members (`launcher/src/bin/nd-members.rs`) starts the follower pair, then (HOSTING-41) the stdio pair.

### 1.2 The count (READ; criterion = charter law 2: an accept / refuse / select / order decision, or a reply synthesized, that is not a Lean definition, beyond byte transport, process lifecycle and key custody)

**COUNT = 9.** Refuter NVM §E.2 is MET: the count is greater than zero.

| id | path:line | kind | what Rust decides | Lean has | reaches the resident as |
|---|---|---|---|---|---|
| **R1** | `client/src/stdio.rs:57-67` (reply built `:31-41`) | refuse + synthesize a reply | `undecodable` and `notOnSurface` (first word ∉ `STDIO_VERBS`): exit `refused`, stderr `refused NAME [WORD]` | the list and the names (`Protocol/Command/Stdio.lean:23-56`); the RULE only as prose (`:7`); no definition of the screen or of its reply | `.ok {exit = refused}` |
| **R2** | `client/src/stdio.rs:82-86` | synthesize a reply | every `RunError` (follow or host socket failure, `StepsExhausted`, an attempt or custody error) becomes exit `client`, stderr `nd: …` | the code only (`CommandExit.client`) | `.ok {exit = client}` |
| **R3** | `client/src/run.rs:212-225, 184-210` | order + synthesize a reply | an ARMED rotation's attempt is driven before every command; a contradicted one ends the command with a Rust-built `Done (hostContradicted, "", "hostContradicted … (attempt DIR)")` (`:198-206`) | nothing (CLIENT-13 prose) | `.ok {exit = hostContradicted}` (stdio custody refuses rotation, `stdio.rs:44-46`, so an armed rotation needs another nd on the workspace) |
| **R4** | `client/src/run.rs:118-130` `hint` | select | the Host status byte → `Seen`, a hand-written mapping; a status not named → `Lost` | the mapping only as `Seen`'s docstring (`Protocol/Attempt.lean:57-62`); no emitted function | via R6 only (selects the next request) |
| **R5** | `client/src/attempt.rs:51-65` `Receipt::read`; `client/src/run.rs:135-161` `receipt` | accept / refuse | follow's nested `receipt CALL` answer is a settlement only if exit ok AND stdout is exactly the three lines `receipt `/`head `/`settle ` (the verdict's first word through the emitted `settle_seen`); otherwise `Lost` (stderr kept as hint) | the PRINTER (`Machine.lean:906-911`) and `settleSeen`; no parser | via R6, R7 |
| **R6** | `client/src/attempt.rs:224-296` `drive` | select + order | the attempt LOOP: which `(request, seen)` is `last`, the latched receipt that settles (`:245`), the fuel `3·sendsMax + 1` ending `Uncertain` (`:242, :291-295`), each end's payload (`:259-268`), the hint bound (`:287`) | each step's choice (`Attempt.next`, emitted, `Proofs.Attempt.next_final`); NOT the loop: no Lean definition of the driver (`git grep -n drive` over Protocol/Host: none) | via R7 |
| **R7** | `client/src/run.rs:292-314` | synthesize follow's input | the attempt's end → step 4's result (`Settled{committed}` → `Committed`, `Signed`/`Uncertain` → `Uncertain`, `Open` → its end and payload), and custody's settle on it | `settled` (`Machine.lean:981-996`) READS `result[0]` and answers `.done CommandExit.ok` on `committed` **without consulting follow's own World** | **`.ok {exit = ok}`**: the only Rust decision that can make an invoke reply say ok |
| **R8** | `client/src/run.rs:241-243, 281, 322-327` `nested` | refuse | a `receipt` inside an attempt that asks to sign-next, precommit or submit is an error | nothing | via R5 (`Lost`) |
| **R9** | `launcher/src/bin/nd-members.rs:608-615` `Pair::tend` (+ `Proc::ready` `:499-520`) | order (HOSTING-41) | the stdio pair starts only after the follower answered an empty command with a decodable `Step` | nothing (Rust lifecycle plumbing by HOSTING-41's own words) | `.error` only (no member socket yet: connect fails) |

Excluded, and why (READ):
- **Byte transport**: `sockets.rs:30-121` (one frame each way; any non-ok status is an io error, never a verdict), `frame.rs`,
  `stdio.rs:92-117` (in order, one reply per request), the mux's `forward`/`route` (`mux.rs:360-470`).
- **Process lifecycle**: the mux's named closes (`idle`, `replyTimeout`, `frameStalled`, `full`, `peerRefused`,
  `replyBacklog`: Lean's `CloseReason` with Lean's bounds; each reaches the resident as `.error "status N"` through
  `Reply.ofBody`), nd-supervise's exits, nd-members' restart cadence and crash loop. NOTE: `RESTART_AFTER`,
  `STARTS_MAX`, `STARTS_WINDOW` (`nd-members.rs:59-61`) are hand-copied constants, which law 2's "never hand-copied
  constants" forbids; lifecycle, not a decision on the leg; recorded.
- **Key custody** (law 2 lists it): `custody.rs` signs the bytes follow hands it; its refusals (`noRotation`, …) go
  back to follow as `refused ‖ CustodyRefused`, rendered by follow.
- `fresh` (`run.rs:353-365`): an attempt directory's number. Storage.

### 1.3 What the count means for E2 (INFERRED from 1.2)

Sort the nine by what the resident does with the reply (`deliverP`, `readP`, `tickP`):
- **exit ok** (the resident FORGETS its kept answer; E2's `x = .ok reply ⇒ a committed Step` direction): only R7, fed by
  R4–R6 and R8. Today an invoke reply's `ok` is Rust's attempt verdict relayed through `settled`, not a check follow
  makes. The planned transport premise ("the reply bytes are the follower's Lean `done` step") is TRUE of those bytes
  and NOT ENOUGH: the `done` step's `ok` is a function of a Rust-computed input. Stated over today's code, E2 would
  quantify over R4–R8, which Lean does not decide (NVM §E.2's law-2 violation).
- **exit refused** (the resident re-reads `pending` and judges by ROWS): R1, and R6/R7's refused end. The resident's
  action is safe whatever produced the reply (it re-reads), and R1 is unreachable from the resident's own argv
  (INFERRED: `Cmd.argv`'s first words are `read`/`invoke`, both `onStdio`; to be a theorem, PART 2).
- **any other exit** (client, hostContradicted, open, uncertain, declined): R2, R3; the resident retries at the next
  tick exactly as on `.error`. Observationally crash-stop (to be a theorem, PART 2).
- **`.error`**: R9 and every lifecycle close. Already quantified: `Runs` ranges over every `Except String Reply`.

So the ONE decision E2 depends on is R7 (with R4–R6, R8 behind it), and its Lean move is small: **follow settles step 4
on its own World** (`settled` checks `settleOf X me w c = committed` for the call it planned, the World being the one
the nested `receipt CALL` just caught up), making R4–R8 hints exactly as PROTOCOL-46 already makes the Host's status a
hint. R1–R3 and R9 need no decider: two resident-side lemmas show the resident's trace cannot tell them from `.error`
(R2, R3, R9) or cannot reach them (R1). PART 2 prices this.

## PART 2 — the model, priced by PART 1

### 2.0 What PART 1 changes in the plan (INFERRED)

The plan priced E2 at ONE transport premise and zero Lean moves. PART 1 says the premise "the stdio reply bytes are
the follower's Lean `done` step" is necessary and not sufficient: for an `invoke`, the `done` step's `ok` is follow's
rendering of a Rust-computed step-4 result (R7). So E2's price rises by ONE Lean move, card **T0** below (PROTOCOL's
file, not my grant: ASK in §2.7). With T0 in, R4–R8 become hints, the premise covers only byte relay plus nd's three
named ends (R1–R3), and R9 is crash-stop. Without T0, E2 is not built: its theorem would quantify over R4–R8.

### 2.1 T0 — follow settles step 4 on its own World (the Lean decider; PROTOCOL; ASK)

- Change (`Protocol/Command/Machine.lean`): step 3's continuation also carries the submitted call bytes,
  `again 4 [startB, signedB, ub, out, X.callBytes c]` (`:1201`); the step-4 arm (`:1218`) becomes
  `| _, 4, [_, _, _, out, cb] => same (settled X me w out cb result)`; `settled`'s `committed` arm answers
  `.done CommandExit.ok` only when `X.decodeCall cb = some c` and `settleOf X me w c = .committed h td` on follow's
  CURRENT World `w` (the one the nested `receipt CALL` just caught up: same process, `Follow.loop` threads `r.world`);
  otherwise `.done hostContradicted … "hostContradicted committed FOLLOWSAID"`. The `refused` arm likewise re-checks
  (`settleOf … = .refused _ ∨ .expired`). Every other arm unchanged.
- The continuation stays unauthenticated, as today (`Machine.lean:46-49`: "`k` cannot steer what is signed"). At
  step 4 `k` would name WHICH call is checked; returning `k` verbatim is inside the transport premise (2.3), the same
  trust the argv already needs. INFERRED: nothing else reads phase-4 continuations.
- New theorem (`Protocol/Proofs/Command.lean`), stated:
  ```lean
  theorem step_settled_ok {X : Ctx D} {dc : Codec.Stream D} {B : Thin.Base (World D)} {me : Self D}
      {f f' : Follow D} {p : Persist D} {kb result out err : ByteArray}
      (h : step X dc B me f kb result = (f', p, .done CommandExit.ok.code.toUInt8 out err))
      (h4 : phaseOf kb = some 4) :
      ∃ cb c h td, contCall kb = some cb ∧ X.decodeCall cb = some c ∧
        settleOf X me f.world c = .committed h td
  ```
  (`phaseOf`/`contCall` read the continuation's state as `step` does.) Nano object: follow's own `done ok` for a
  write. Mutation that makes it false: `settled`'s committed arm back to trusting `result[0]` (today's code).
- Price: `settled` gains three arguments, so `settled_ne_submit` (`Command.lean:217`), `settled_ne_host` (`:1281`),
  `settled_uncertain` (`:1130`), `settled_cont` (`Incoming.lean:182`) are RESTATES (a binder each, no hypothesis).
  0 hypotheses gained. Bytes: the phase-4 continuation grows by one item; no layout, no codec vector, no table moves
  (INFERRED; T0's own build measures `rows/` and the codec vectors). Gate `protocol:` unless a vector moves.
- Tooth (deployed, `launcher/tests/resident_bell.rs`, a by-hand CLIENT plant): `run.rs:292-307` answering step 4
  `Committed` on a `declined` end. Today: follow says ok, the resident forgets, the ring is still pending, the next
  tick asks again → Q2 "two rings, two asks" RED. Under T0: follow says `hostContradicted`, the resident retries,
  Q2 GREEN. Both measured before the landing.

### 2.2 SocketRel (Hosting/Proofs/Socket.lean, new; my grant)

```lean
/-- One command of follow's machine, as the stdio leg drives it: `start` on the argv, then `step` on each
continuation with SOME result, follow's state free to advance between frames by other commands' absorbed steps
(one `Follow.loop`, commands interleave), ending in a `done`. -/
inductive FollowRun (X : Ctx D) (dc) (B) (me : Self D) : Follow D → Reply → Follow D → Prop
  | done   : FollowRun X dc B me f (.done e o r) f
  | step   : r.cont = some k → (∃ l, World.fold X.env f.world l = .ok g.world) →
             step X dc B me g k res = (f', p, r') → FollowRun X dc B me f' r' f'' →
             FollowRun X dc B me f r f''

/-- The resident's `.cmd c x` and the member's follower: a failure is crash-stop (no claim); a reply is the
`done` step of a follower run of exactly `c`'s argv, or one of nd's own three named ends (PART 1 R1–R3). -/
def SocketRel (X) (dc) (B) (me) (conf : Conf) (c : Cmd) : Except String Reply → Prop
  | .error _ => True
  | .ok rr =>
    (∃ f₀ f₁, FollowRun X dc B me f₀ (Command.start X me f₀ (c.argv conf)) f₁ ∧
       f₁.lastDone = (rr.exit, rr.stdout, rr.stderr)) ∨
    (rr.exit = CommandExit.refused.code ∧ ¬ OnStdio (c.argv conf)) ∨          -- R1
    rr.exit = CommandExit.client.code ∨ rr.exit = CommandExit.hostContradicted.code   -- R2, R3

/-- The transport premise, NAMED (gates/tcb.tsv row `stdio-leg`): every member-socket event of a trace. -/
def StdioLeg (X dc B me conf) (es : List Ev) : Prop := ∀ c x, .cmd c x ∈ es → SocketRel X dc B me conf c x
```
(`lastDone` is notation for the `done` the run ended in; the build fixes the spelling.) It is satisfiable (every
`.error`) and refutable (an ok reply with no follower run), and it is a hypothesis of the NEW theorems only.

Two lemmas that discharge R1–R3 on the resident's side (no premise):
```lean
theorem resident_argv_on_stdio (c : Conf) (cmd : Cmd) (h : cmd built by tickP) : OnStdio (cmd.argv c)
  -- describe/read/reread start "read", invoke starts "invoke": both Verb.onStdio (Protocol/Command/Stdio.lean:23-26)
theorem deliverAfter_unsettled (hx : rr.exit ≠ ok ∧ rr.exit ≠ refused) :
    DeliverAfter sh r (.ok rr) rest ↔ DeliverAfter sh r (.error e) rest   -- R2/R3 are crash-stop to the resident
```
Mutations: `Cmd.argv`'s read built with a flag first (`--read`) → `resident_argv_on_stdio` RED; `deliverP`'s
other-exit arm forgetting → `deliverAfter_unsettled` RED (and `tick_order`).

### 2.3 The one transport premise, exact text for gates/tcb.tsv

```
stdio-leg	client/src/{stdio,run,attempt,sockets,frame,mux,table}.rs, client/src/bin/nd-supervise.rs (tree)	trusted-unverified	HOSTING	the stdio reply bytes are the follower's Lean done step for that command (PROTOCOL-40, decisions/protocol.md:998): the member socket and nd --stdio relay the resident's argv to follow's start and every continuation follow hands out back to follow's step byte for byte, and every reply the resident decodes is follow's done for that command or one of nd's three named ends (notOnSurface/undecodable, client, hostContradicted); Hosting.Proofs.Socket.StdioLeg	the relay and nd's three ends generated from a Lean stdio decider, or the leg proved in a verified transport
```
What it does NOT trust, by T0: the attempt loop (R4–R8: hints), the Host's status, custody's signatures (follow's
`receive` checks them at step 3), the mux's closes (`.error`). NOT a transport premise and not in this row: custody
of the resident's key (law 2 lists custody as Rust's; the theorems below never assume who else signs, §2.5).

### 2.4 The theorems, as statements (nano object; deployed mutation)

**(a) `bell_resident_conforms`** (Hosting/Proofs/ResidentRun.lean or a new BellConform.lean; no premise). PROT-3's
host half. Under the cheap branch there is no `Glob`: the resident's projection of the Bell's one round (ring →
one ask → one answer) is a CROSS-TICK fact, which `tick_order` (one tick) does not state:
```lean
inductive Ticks (w : Where) : Mem → List (List Ev) → Prop
  | nil  (m : Mem) : Ticks w m []
  | last {m es e d} : Runs (tickP w m) es (.stop e d) → Ticks w m [es]
  | next {m m' es ess} : Runs (tickP w m) es (.next m') → Ticks w m' ess → Ticks w m (es :: ess)

/-- What frees a ring for a second ask: its answer taken (an invoke of it answered ok), or a read that listed
the pending rings without it. -/
def Frees (r : Ring) : Ev → Prop
  | .cmd (.invoke _ r' _) (.ok rr) => r' = r ∧ rr.exit = CommandExit.ok.code
  | .cmd (.read sh) y | .cmd (.reread sh) y => ∃ p, readRings sh y = some p ∧ r ∉ p
  | _ => False

theorem bell_resident_conforms (h : Ticks w m ess) {pre mid post : List Ev} {q q' : Broker.Ask} {x x' : AskEnd}
    (hc : core ess.flatten = pre ++ .ask r q x :: mid ++ .ask r q' x' :: post) (hx : askText x ≠ none) :
    ∃ e ∈ mid, Frees r e
```
"A spent ask is never repeated for a ring until that ring's answer was taken or a read saw it gone." Nano object:
every chain of deployed ticks (`tickP`, the tree `tick` performs: `interp_runs`; as protocol paths: `nano_runs_iff`).
Proof route: `tick_counts` (one ask a tick), `kept_follows`, `decide_kept_first`/`decide_ask`, `DeliverAfter`.
**Mutation (the plan's): `decideTick` asking twice** — `| some (r, t) => match pending with | q :: _ => .ask q`
(the kept-pending check dropped). Tick j: kept `(r, t)`, the read lists `r` (no `Frees`), the plant asks `r` again.
RED. `tick_order`/`tick_counts` stay GREEN under it (`ActCore` follows whatever `decideTick` says): MEASURED at
the build, with `decide_kept_first`/`decide_answer` (`Hosting/Proofs/Resident.lean:71,100`, which the plant also
reds and which this module imports) `sorry`ed in the plant run only, so the log can name the new theorem.
Consumer: `resident_bell.rs` Q2 ("two rings, two asks") and Q6 ("a restart asked again") are its deployed rows;
the same plant reds Q2 there (HOSTING-31's "answering an answered ring" plant is its neighbour).

**(b) `answered_row_is_kept_answer`** (Hosting/Proofs/Socket.lean; premise `StdioLeg`; needs T0):
```lean
theorem answered_row_is_kept_answer (h : Runs (tickP w m) es a) (hs : StdioLeg X dc B me w.conf es)
    (hi : .cmd (.invoke sh r t) (.ok rr) ∈ core es) (hok : rr.exit = CommandExit.ok.code) :
    -- the resident: the invoked pair is the kept answer (the decision `answer`) or this tick's kept text
    ((m.kept = some (r, t)) ∨ ∃ x, askText x = some t ∧ .keep r t true ∈ core es) ∧
    -- the member: a follower run of exactly that invoke, whose submitted call is planned from it and settled
    -- committed on the follower's own World, and so is that World's journal entry
    ∃ f₀ f₁ c h td, FollowRun X dc B me f₀ (Command.start X me f₀ ((Cmd.invoke sh r t).argv w.conf)) f₁ ∧
      Submitted c f₀ f₁ ∧ callArg c = some (answerDatum r t) ∧ callTarget c = (w.conf.bell, sh.answer) ∧
      settleOf X me f₁.world c = .committed h td ∧
      (f₁.world.journalAt X.env (txIdOf X c) = some (h, td) ∨ CollidesAmong X.env.hash (…))
```
Nano object: the deployed resident's tick and the member's own follower World. Route: `tick_counts` (the invoke's
two arms), `StdioLeg` (the ok reply is a `done` of that argv: R1 out by `resident_argv_on_stdio`, R2/R3 out by the
exit), `step_submit_planned` (`Command.lean:303`: the submitted call is `plan` on follow's World of that command's
body), T0's `step_settled_ok`, `check_committed` (`Receipt.lean:43`) through `settleOf`'s `Receipt.build` (the
collision disjunct is over the EXPLICIT list `check_committed` names, never an unbounded `∃ a b`).
Mutations: T0 reverted (`settled` trusts `result[0]`) → the proof's `step_settled_ok` step has no object: RED;
`deliverP` forgetting on exit `client` (R2) → the resident side RED (`deliverAfter_unsettled`).
**The ROW.** The conclusion reaches the journal entry of the call carrying `answerDatum r t` to the Bell's `answer`.
That the entry's Turn wrote `rings[(r.notBefore, r.ringer)].answered = some (ask t)` is the Bell's `answer`
method (`world/resident/Bell.ob:13-20`), which no landed theorem states over the compiled Bell (PROT-4a named the
Bell as the next witness of `activity_monitor_safe`; READ-PROT-4a §2). So: default **(b) lands as stated, with the
journal entry as its conclusion, under the name `delivered_answer_committed`**, and `answered_row_is_kept_answer`
is its row corollary, landing with the Bell witness (a LANG card: `bell_monitored`, plus the `answer` method's
edit read off `runMeasured`). Q2 asks whether to hold the name for the row.

**(c) the join, `one_ask_per_ring`** (optional third landing; premise `StdioLeg`): (a) with `Frees` read through
the member's World: between two spent asks of `r`, the follower's World journaled the answer call carrying `r`'s
kept text ((b)), or rendered `pending` without `r` (`rangeLines_reads`, `Command.lean:938`, through `StdioLeg` for
the read's reply). This is B8's "they JOIN across the member socket" as one statement. Its own price is a
`FollowRun` lemma for the read arm; it waits for (a) and (b) to land.

### 2.5 What is NOT claimed

- Custody: who else holds the resident's key. (b) is "an ok reply means committed, carrying the kept text"; the
  converse reading ("no answered row that is not a kept answer") needs "only the resident's nd --stdio signs with
  its key" (HOSTING-32's sandbox), a custody premise this card does not add.
- Restarts: (a) is one process life. Across restarts it composes with `resume_durable`/`seedOf`
  (`ResidentVolume`); that composition is not stated here.
- Liveness: nothing says an ask is ever answered.

### 2.6 Price, RESTATES/DELETES, gate

- Landed theorems gaining a hypothesis: **0** (INFERRED now; MEASURED by the decls diff at the build).
  `tick_order`, `tick_counts`, `kept_follows`, `interp_runs`, `nano_runs_iff`, `step_submit_planned`,
  `check_committed`, `check_refused_sound`, `settle_final_never_admits`, `audit_ok` are used as stated.
- RESTATES: T0's four `settled_*` (Protocol, a binder each). Hosting: none.
- DELETES: LITP PROT-3's "the join stays a journey row, named" and ACT-D §4.4's "would need the member-socket model,
  which no proof has" (doc text in redregg, not nano). In nano: the `Hosting.Proofs.ResidentRun` header sentence
  "What is code, not theorem: …" gains the premise's name; nothing deleted. NanoBridge stays (`nano_runs_iff` is
  (a)'s protocol reading, cited, not re-proved).
- Gate: Hosting part `hosting:` proof-only (Hosting/Proofs/**, gates/tcb.tsv, launcher/tests/** docs); the Bell does
  not re-cut, no byte moves. T0 `protocol:` (`protocol!` only if a vector moves).
- Size (INFERRED): Hosting/Proofs +1 module (~350 lines: `FollowRun`, `SocketRel`, (b), two lemmas), (a) ~150 lines;
  T0 ~25 lines of Machine + ~60 of proof.

### 2.7 Order, and the questions (defaults in bold)

Order: **(a) first** (no premise, no T0, my grant, the plan's tooth); then T0 (PROTOCOL); then (b) + the tcb row;
then (c).

1. T0 lives in `Protocol/**`, granted to CX-P5 (R-0051), not to me (R-0052). **ASK: grant me
   `Protocol/Command/Machine.lean` (the step-3 continuation and `settled`) + `Protocol/Proofs/{Command,Incoming}.lean`
   (T0's theorem, the four restatements) under CROSS-LAYER: PROTOCOL, as one landing coordinated with CX-P5** — or
   rule that CX-P5 lands T0 and I wait for it.
2. The name: **(b) lands as `delivered_answer_committed` (the journal entry); `answered_row_is_kept_answer` waits for
   the Bell witness (a LANG card)** — or land (b) under the plan's name with the journal conclusion and the row
   named in its docstring as not stated.
3. bell_resident_conforms is the cross-tick (a), not a restatement of `tick_order` through `nano_runs_iff` (which
   would be a corollary with `tick_order`'s tooth and no consumer): **(a) as stated** — or the cheap docstring.
4. **(a) lands alone first (`hosting:`), before T0's grant is ruled**: it needs nothing outside my grant.

## 3. Candidate (a) BUILT, and its plant (MEASURED; appended after READY, same READY; nothing landed)

Artifacts: `promo/E2/` (`BellConform.lean` = the candidate module `Hosting/Proofs/BellConform.lean` in hbox `wt/e2`
at `1fc905f`; `plantA.diff/.log`, `plantAs.diff/.log`, `bc2.log`, `restoreA.log`).

- **Built GREEN**: `lake build Hosting.Proofs.BellConform`, 96 jobs (`bc2.log`); after the plants, restored and
  rebuilt GREEN (`restoreA.log`). `#print axioms bell_resident_conforms`: `propext, Classical.choice, Quot.sound`.
  No landed file touched (`git status`: one untracked file).
- **The statement as built** (§2.4 (a), with `frees : Ring → Ev → Bool` so the round is a fold):
  `bell_resident_conforms (h : Ticks w m ess) (hc : core ess.flatten = pre ++ .ask r q x :: mid ++ .ask r q' x' :: post)
  (hx : (askText x).isSome) : ∃ e ∈ mid, frees r e = true`. Route: `tick_order` + `kept_follows` per tick
  (`tickCore_debt`), induction over `Ticks` (`ticks_debt`), then `debtRun_frees`. `act_debt` reads `decideTick`'s
  OWN arms, not `Proofs.Resident.decide_*`, so the plant below can name it.
- **Plant A (the plan's "decideTick asking twice")**: `Hosting/Resident/Bell.lean:161`
  `| some (r, t) => if r ∈ pending then .answer r t` → `.ask r` (the kept ring, still pending, asked about again).
  - As planted (`plantA.log`): RED `Hosting/Proofs/Resident.lean:72` (`decide_kept_first`), `:90` (`decide_ask`),
    `:108` (`decide_answer`); Lake builds nothing past that module.
  - Planted with those three proofs `sorry`ed in the plant run only (`plantAs.diff`; file-level
    `warningAsError false`, never landed): `Hosting.Proofs.ResidentRun` BUILT, so `tick_order`, `tick_counts`,
    `kept_follows`, `interp_runs` stay TRUE of the planted `decideTick`; `Hosting.Proofs.BellConform` RED, the
    semantic error `BellConform.lean:211:4 unsolved goals` in `act_debt`'s ask arm with ring `q` OWED and `q ∈ p`:
    the goal is the planted second ask (`l = keep q intentText true :: ask q … :: rest`). The other two errors
    (`:189`, `:208-210`, "No goals"/an unused simp argument) are the answer arms the planted `decideTick` no longer
    has: script breakage, not a claim. So the new theorem is the only one downstream of the planted definition that
    goes red, and `tick_order` is not its tooth.
- Inhabited (INFERRED, not a witness theorem): a chain where tick 1 asks `r`, keeps the answer, invokes it, gets
  `ok` and forgets; tick 2's read lists `r` again (a re-ring at the same key and text after a retire) and asks:
  `hc` holds with `mid ∋` tick 1's ok invoke. A `two_asks_path_exists` witness can be added if the reader asks.

## 4. Candidate T0 BUILT (MEASURED; under R-0054's conditional grant; nothing landed)

Artifacts: `promo/E2/T0-candidate.diff` (5 files), `whole2.log`/`whole3.log`, `rows*.log`, `plantT0*.{diff,log}`.

- **What changed** (`Protocol/Command/Machine.lean`): step 3's continuation carries `X.callBytes c`; the step-4 arm is
  `| _, 4, [_, _, _, out, cb] => same (settled X me w out cb result)`; new `ownSettle X me w cb :=
  (X.decodeCall cb).map (settleOf X me w)` and `attemptContradicted`; `settled`'s `committed` arm is `done ok` only on
  `ownSettle = some (.committed _ _)`, its `refused` arm prints follow's OWN verdict only on `refused`/`expired`, and
  every other own verdict is `hostContradicted CLAIM FOLLOWSAID` (undecodable call bytes: `refused badResult`).
- **New theorems** (`Protocol/Proofs/Command.lean`), as built:
  ```lean
  theorem settled_ok (h : settled X me w out cb result = .done CommandExit.ok.code.toUInt8 o e) :
      ∃ c hh td, X.decodeCall cb = some c ∧ settleOf X me w c = .committed hh td
  theorem step_settled_ok (hst : State.ofBytes kb = some ⟨argv, 4, acc⟩)
      (h : step X dc B me f kb result = (f', p, .done CommandExit.ok.code.toUInt8 o e)) :
      ∃ cb c hh td, acc.getLast? = some cb ∧ X.decodeCall cb = some c ∧ settleOf X me f.world c = .committed hh td
  ```
- **Restated** (a binder each, no hypothesis; the `omit [Ord D] [DecidableEq D]` dropped because `settled` now reads
  `settleOf`): `settled_ne_submit`, `settled_ne_host`, `settled_uncertain` (Command.lean), `settled_cont`
  (Incoming.lean, proof rewritten: every arm is a `.done`). Expected map: **4 RESTATES-MEANING**, 0 DELETES
  (INFERRED from the statement diff; the judge's decls diff confirms at landing).
- **Consumers measured.** Whole tree GREEN, 727 jobs (`whole2.log`, `whole3.log` after the plants). ONE consumer
  outside R-0054 broke and is fixed in the candidate: `Protocol/Rows/Loopback.lean:1152`, the rows' `.rerun` calls
  `Command.settled` directly; it now passes the actor's `Self` (`selfOf l.actor .none`), its follow World and the frozen
  call (3 lines). **`rows` ALL PASS, `rows --deployed` ALL PASS, `rows --harness-control` RED (FAIL 44 of 45)** after
  ONE more change outside R-0054, in `Protocol/Rows.lean`: two rows' plant expectations.
- **The two rows are R7 already modelled, and T0 changes how they are caught** (MEASURED `rows.log` before the
  restatement): `settleDecline` (the attempt store takes `declined` as final, row `refused`) and `trustLookup` (the
  store ends on the Host's word without asking follow, the shape before PROTOCOL-46, row `settle`) were caught by
  the WRONG verdict reaching the member (`refused stale` at lines 13 and 6). Under T0 follow refuses to echo them:
  `hostContradicted refused open` at line 13, `hostContradicted committed open` at line 1 (with no confirm, follow
  never caught the call up, so its own World says open). The restated expectations:
  `.caught .settleDecline 13 (.contradicted "refused open")`, `.caught .trustLookup 1 (.contradicted "committed open")`.
  So PROTOCOL-46's "the attempt store asks its own follow" is no longer what keeps a lie out; it is what lets the
  honest path settle (without the confirm, follow says open and the member retries). The decision says so.
- **Plants** (each restored; whole tree rebuilt GREEN after):
  - **P-T0c** `settled`'s committed arm answers ok unconditionally (today's code): `settled_ok` RED
    (`Command.lean:238`, `:243`: the arms where follow's own settlement is not committed); `settled_cont` GREEN;
    `rows`: `settle` row FAIL (`trustLookup` BLIND at line 1), every other row PASS (`plantT0-rows.log`).
  - **P-T0r** the refused arm back to printing the store's text: `rows`: `refused` row FAIL (`settleDecline` BLIND
    at line 13) (`plantT0r-rows.log`); `settled_cont`'s script broke (a proof script, not a claim). No theorem states
    the refused arm (the resident consumes only `ok`); its tooth is the `refused` row.
- **ASK (new ground, sent 2026-10-23)**: the two Protocol files outside R-0054, `Protocol/Rows/Loopback.lean` (the
  rerun call) and `Protocol/Rows.lean` (the two plant expectations), under CROSS-LAYER: PROTOCOL.

## 5. E2b — the socket theorems, revised per R-0058 / READ-E2-grok (supersedes §2.2, §2.3, §2.4 (b)-(c), §2.6's DELETES)

Landed meanwhile: (a) `bell_resident_conforms`, `b4a7f38` (hosting:). T0 built (§4), waiting on its two Protocol paths.

### 5.1 The premise: ONE byte-relay sentence (replaces §2.3; the old row is withdrawn)

```
stdio-leg	client/src/{stdio,run,sockets,frame,mux}.rs, client/src/bin/nd-supervise.rs (tree)	trusted-unverified	HOSTING	an ok reply whose exit is CommandExit.ok is the follower's Lean done of that command: nd --stdio gave follow the resident's argv, gave follow back byte for byte every continuation follow handed out, and the resident decoded follow's done (Hosting.Proofs.Socket.StdioLeg)	nd --stdio's relay proved in a verified transport
```
It trusts Rust to MOVE bytes and nothing else: no synthesized reply (R1–R3 are not in it), no attempt end (R4–R8:
after T0 they only choose the `result` a step is handed, which `FollowRun` quantifies over), no classification.
`k` is opaque to Rust (`run.rs` resumes with the `k` follow returned); T0's call bytes are one more element of
`stateLayout`'s `.list acc`, so the layout does not change.

### 5.2 `SocketRel`, shrunk (replaces §2.2)

```lean
/-- One command of follow's machine as the leg drives it: `start` on the argv, then `step` on each continuation
follow handed out, with SOME result (the attempt store's, custody's, the Host's: chosen, never trusted), follow's
World free to fold between frames (one `Follow.loop`, other commands absorb), ending in a `done`. -/
inductive FollowRun (X : Ctx D) (dc : Codec.Stream D) (B : Thin.Base (World D)) (me : Self D) :
    Follow D → Reply → (UInt8 × ByteArray × ByteArray) → Prop
  | done : FollowRun X dc B me f (.done e o r) (e, o, r)
  | step : r.cont = some k → World.Extends X.env f.world g.world →
      step X dc B me g k res = (f', p, r') → FollowRun X dc B me f' r' end → FollowRun X dc B me f r end

/-- The resident's `.cmd c x` and the member's follower: an `ok`-exit reply is the `done` of a follower run of
exactly `c`'s argv; every other reply and every failure claims nothing (crash-stop, or a refusal the resident
judges by rows). -/
def SocketRel (X dc B me) (conf : Conf) (c : Cmd) : Except String Reply → Prop
  | .ok rr => rr.exit = CommandExit.ok.code →
      ∃ f₀, FollowRun X dc B me f₀ (Command.start X me f₀ (c.argv conf)) (rr.exit.toUInt8, rr.stdout, rr.stderr)
  | .error _ => True

def StdioLeg (X dc B me conf) (es : List Ev) : Prop := ∀ c x, .cmd c x ∈ es → SocketRel X dc B me conf c x
```
R1–R3 are not in it; where the resident cares they are two resident lemmas that trust nothing about Rust
(`resident_argv_on_stdio`: every `Cmd` `tickP` builds starts `read` or `invoke`, both `Verb.onStdio`;
`deliverAfter_unsettled`: an exit neither ok nor refused has `.error`'s `DeliverAfter` tail). `.error` is
crash-stop, already quantified by `Runs.cmd`; R2/R3 are `.ok` with another exit and are covered by the lemma,
not by the premise.

### 5.3 `delivered_answer_committed` (replaces §2.4 (b); premise `StdioLeg`; needs T0 landed)

```lean
theorem delivered_answer_committed (h : Runs (tickP w m) es a) (hs : StdioLeg X dc B me w.conf (core es))
    (hi : .cmd (.invoke sh r t) (.ok rr) ∈ core es) (hok : rr.exit = CommandExit.ok.code) :
    ((m.kept = some (r, t)) ∨ .keep r t true ∈ core es) ∧
    ∃ f₁ c h td, X.decodeCall … = some c ∧ callTarget c = (w.conf.bell, sh.answer) ∧
      callArg c = answerDatum r t ∧ f₁.world.journalAt X.env (txIdOf X c) = some (h, td)
```
(`f₁` the follower state the run ended at; the build fixes how `FollowRun` exposes it.) Route, every link named:
- resident half: `tick_counts`'s two invoke arms (no premise, no T0);
- the ok reply is a `done` of a run of `invokeArgv w.conf sh (answerArg r t)`: `StdioLeg`;
- that run's `done ok` is at phase 4: **NEW Protocol lemma `invoke_done_ok_phase4`** (for an `invoke` command,
  every `step`/`start` arm that answers `done ok` is the settlement arm; `printed` is read/describe/sync/receipt
  only), proved like `step_submit_planned` (`Command.lean:303`);
- the phase-4 continuation's last item is the call step 3 submitted: **NEW `step_submit_cont`** (a `.submit call k`
  step has `State.ofBytes k = some ⟨argv, 4, acc⟩` with `acc.getLast? = some call`, from `next` and the state codec's
  roundtrip) + `FollowRun` (the next frame's `k` is that `k`: the premise);
- that call is planned from the command's body on follow's World: `step_submit_planned` (as stated);
- committed on follow's own World: T0's `step_settled_ok`, then **`settle_committed`** (`Protocol/Proofs/Settle.lean`:
  `ofReceipt … (Receipt.build E w tx).answer = .committed h td → w.journalAt E tx = some (h, td)`): the journal
  entry, with NO collision disjunct (§2.4's `check_committed` route withdrawn);
- the call's target and argument: **NEW `invokeArgv_body`**: `parse` of `invokeArgv conf sh arg` is
  `.invoke (conf.bell) (sh.answer) arg _ (conf.grant)`, and `Lang.argsOf` of `answerArg r t` at a method whose
  argument type is `answerArgTy` is `answerDatum r t` (`answerArg_reads`, `Hosting/Proofs/Resident.lean:168`,
  composed with the parse); the method type is `answerArgTy` by the shape the resident read (`Shape.read` refuses
  any other), which is follow's own description of the package: the description/readTy roundtrip is part of this
  lemma and is its largest piece (INFERRED).
Nano object: one deployed tick and the member follower's own World. Mutations: T0 reverted (P-T0c, §4) →
`step_settled_ok` has no object, RED; `deliverP` forgetting on exit `client` → `deliverAfter_unsettled` RED.
NOT claimed: that an ok reply's stdout is the receipt (`settled` returns `out`, step 3's pre-submit `receive`; T0
does not trust it and neither does this); who else holds the resident's key; restarts; liveness; that R4–R6
implement `Attempt.next`.

### 5.4 `answered_row_is_kept_answer`: a docstring, not a theorem, in this card

The row (`rings[(r.notBefore, r.ringer)].answered = some (ask t)`) is the Bell's `answer` method, which no landed
theorem states over the compiled Bell. `delivered_answer_committed`'s docstring says the row is NOT stated and
names the Bell witness (a LANG card) as what would state it. LITP's "the join stays a journey row" is NOT deleted.
`one_ask_per_ring` (§2.4 (c)) waits for the same witness.

### 5.5 Price (revised)

- Landed theorems gaining a hypothesis: 0 (`tick_order`, `tick_counts`, `kept_follows`, `step_submit_planned`,
  `settle_committed`, `answerArg_reads` used as stated).
- New: Hosting/Proofs/Socket.lean (`FollowRun`, `SocketRel`, `StdioLeg`, `resident_argv_on_stdio`,
  `deliverAfter_unsettled`, `delivered_answer_committed`); Protocol/Proofs (`invoke_done_ok_phase4`,
  `step_submit_cont`, `invokeArgv_body` or its Protocol half) — Protocol/Proofs/Command.lean is in R-0054.
- `gates/tcb.tsv`: the one row of §5.1. Gate: `hosting:` + the Protocol proofs under CROSS-LAYER: PROTOCOL; no byte,
  row or fixture moves; RESTATES none; DELETES none.
- Order: T0 lands first (§4; its two Protocol paths asked); then E2b builds; READY-IMPACT E2b-BUILT before landing.

### 5.6 Per R-0062 (READ-E2b-grok), before the socket theorems are built
- **This theorem's own plant** (not T0's): `Cmd.argv`'s invoke arm (`Hosting/Resident/Run.lean:268-273`) prints
  `answerArg r r.text` (the ring's own text as the answer; `ringText` unchanged, so the bell's `rung: text` admits).
  Expected: `delivered_answer_committed` RED; `settled_ok`, `step_settled_ok`, `tick_counts`, `bell_resident_conforms`,
  `answerArg_reads` GREEN; `resident_bell.rs`'s answer-text row RED. To be measured at the build, the log showing
  `settled_ok` green.
- **NOT claimed, added**: a commit whose reply is lost (follow appends, then dies before `port.send`; the resident sees
  `.error` or exit `client`) is PROT-5's at-most-once and out of this card; nothing here claims the converse of
  ok ⇒ journaled. Said in the module docstring.
- T0 landed first: `e2905e7` (PROTOCOL-64). (a) landed: `b4a7f38`.
