# READ-HOSTING — whole-file read of nanodregg `Hosting/` at origin/main f9657bd (2026-10-24)

Reader: one sub-opus, per `work/readers/BRIEF.md`. Nothing edited. Tags: READ (path:line), MEASURED
(a command I ran), INFERRED.

## Verdict

I read the resident path whole: `Resident/Sockets.lean`, `Resident/Run.lean`, `Resident/Bell.lean`,
`Resident/Trace.lean`, `Proofs/ResidentRun.lean`, `Proofs/Socket.lean`, `Proofs/Resident.lean`,
`Proofs/Committed.lean`, `Hosting/Reply.lean`, `Hosting/Broker.lean` and `Hosting/Allowance.lean`.
I read most of `Proofs/Lifetime.lean` and `Proofs/BellConform.lean`. For `Proofs/SocketStrong.lean`,
`Proofs/BellRow.lean`, `Proofs/Broker.lean`, `Proofs/Allowance.lean` and `Proofs/Reply.lean` I read
the header, the first 120 lines (SocketStrong) and every theorem statement. I also read the
docstrings of seven more proof modules, `decisions/hosting.md` HOSTING-42..46 whole, the
`stdio-leg` row, Q7 of `launcher/tests/resident_bell.rs`, and the parts of `Host/Follow.lean`,
`Protocol/Command/Machine.lean` and `Lang/Print.lean` that the premises name. In all, about 6,300
of the layer's 12,468 lines were read in full; for another ~3,000 I read the statements.

The resident's tick tree, the order theorems and the strong socket theorem are well built. Each
socket trigger has a plant, and the strong theorem's premise chain holds together.

**The three worst things:**

1. **A theorem whose disjunct is almost surely true.** `Committed.journal_committed`
   (Committed.lean:47) ends in a "second preimage" disjunct, and `BellRow.answered_row_committed`
   (BellRow.lean:214) inherits it. The disjunct ranges over every call admissible at ANY World that
   holds the bell, not over follow's path. A 32-byte hash over that unbounded set has second
   preimages of any fixed target. Cryptographic hardness is about FINDING one, not about whether
   one exists. So "committed by this call ∨ (true)" bounds nothing. This is the 10-20 minted class
   (`CollidesAmong` over an explicit list is the sound form).
2. **A parse failure renders as "nothing pending" (law 7), and the cross-tick one-ask theorem
   certifies the second ask that follows.** A read reply whose stdout is not UTF-8 becomes `""`,
   which reads as "no ring pending" (Run.lean:400, :360; Trace.lean:32). The kept answer is
   forgotten and the ring is asked about again, so the meter is charged twice.
   `BellConform.Frees` (BellConform.lean:50-53) counts that read as freeing the ring, so
   `bell_resident_conforms` allows the double ask. An honest follower cannot produce such bytes;
   the trusted relay can.
3. **A named refusal that never reaches the re-read branch repeats forever.** HOSTING-46's
   question. `declined NAME` (exit 53: unauthenticated, early window, refusal budget) and every
   other exit that is neither ok nor refused are retried every tick (Run.lean:367). Nothing bounds
   them and they never end by name. The code's own rule, at Run.lean:137-139, is that "a refusal
   must not repeat forever". `deliverAfter_unsettled`'s docstring calls these exits "crash-stop"
   (Socket.lean:516); they are retry-forever.

On the questions the brief named:
- The `stdio-leg` row is not one sentence about bytes. It bundles four trusts: topology, follow's
  World dynamics, durability and continuation selection (finding Q1).
- `Reach` over any continuation and any result is necessary, not too weak (Q2).
- `run`'s start state is guaranteed by code reading, not by a theorem (Q3).
- `shape_provenance`'s "same object" comes from the argv being a function of the fixed config. No
  digest is checked, although the description prints `object` and `package` lines that the
  resident ignores (B2/Q4).
- Q7 really stages the race. It is not just waiting (A1).

---

## Answers to the brief's named questions (each also ranked below where it is a finding)

**A1. Q7 (218 s): measuring the race, not just waiting.** READ resident_bell.rs:578-650.
1. The provider is held (`hold.store(true)`).
2. The test waits for `asks() == before + 1`, so the resident has read `pending` and its ask is in
   flight.
3. The owner retires the ring, and the test asserts that the retire took.
4. The hold is released.
5. The test waits for the log line "the ring is no longer pending". Only the re-read-gone branch
   prints it (Run.lean:365).
6. It asserts `asks == before + 2` and no new `answerRefused`.

So the window between read and answer is forced by construction. The gone line also tells this
branch apart from the decideTick path: if a refusal were treated as "unsettled", the next tick
would see the ring gone anyway and ask `after`, and the ask count alone would stay green. Most of
the time goes to the 2048 sequential `w.run(["write"…])` processes that move the World past
PATIENCE, not to the race (HOSTING-46 prices it at ~135 s). Not a defect.

**A2. Bell check at the first describe: what if the describe is of another object?** Under
`StdioLeg` it cannot be. `Cmd.argv .describe = describeArgv c` (Run.lean:273, Bell.lean:298),
`describeArgv_parse` (SocketStrong.lean:51) and `run_describe_ok` tie the description to
`digestOf c.bell`. HOSTING-43's plant P1 reds the strong theorem when the describe names another
id. Without the premise, nothing in the resident checks that the reply describes `c.bell`: see
B2/Q4.

**A3. `deliver_gone_continues`: which refusal names do not reach the branch?** The branch is taken
only when `r.exit = CommandExit.refused.code` (1) (Run.lean:349). These invoke exits all take the
"answer unsettled" arm (Run.lean:367) with no counter: `uncertain` (2), `behind` (51), `client`
(52), `declined` (53, "refused by name, NOT recorded", Protocol/Command/Exit.lean:25-27), `open`
(54), `hostContradicted` (55) and `pageIo` (57). A transport `.error` does the same, including the
resident's own `argvPastBound` (Sockets.lean:72). See D3.

---

## Findings, ranked

### DEFECT

**D1. `journal_committed`'s third disjunct is a second preimage over an unbounded universe, so
the theorem bounds nothing; `answered_row_committed` inherits it.**
- READ Committed.lean:54-59. The conclusion is
  `w₀.journalAt … = some e ∨ (∃ v v' t, Q v ∧ … receive X v c = .ok t ∧ admit …) ∨ ∃ v v' b c' t, Q v ∧ X.decodeCall b = some c' ∧ receive X v c' = .ok t ∧ World.admit X.env v t = .ok v' ∧ b ≠ X.callBytes c ∧ X.env.hash domTx b = txIdOf X c`.
- `v` is ANY World satisfying `Q` (here `PackageAt X v o P pc`: a World that holds the bell). The
  module doc says so itself (Committed.lean:19-22: "nor that `v` lies on the particular path follow
  took"). The shape comes from `Protocol.Proofs.FollowJournal.JournalFrom` (FollowJournal.lean:32-37,
  READ), whose provenance disjunct is "admitted at some `Q` World", not "absorbed on this chain".
- Why it is wrong: the set of byte strings `b` that decode to a call admissible at some
  bell-holding World is unbounded. Worlds may carry arbitrary member keys, and the arguments are
  arbitrary. So the set has far more than 2^256 elements.
- What follows: for a 32-byte hash, a second preimage of the fixed target `txIdOf X c` then exists
  with overwhelming likelihood. Collision resistance and second-preimage resistance say such a `b`
  is hard to FIND. They say nothing against its EXISTENCE, and the disjunct is pure existence. The
  docstring's defence, "a SECOND PREIMAGE of `c`'s id, `c` fixed by the premises; not a collision
  the statement may choose" (Committed.lean:16-17), answers the wrong question: fixing the target
  does not help when the domain is unbounded.
- `answered_row_committed` (BellRow.lean:214-237) carries the same disjunct (:235-237). Its first
  disjunct, `wb.journalAt … = some e`, is literally its premise `hj` when the caller picks
  `wb := wf`, which `Reach.refl` allows. Its "good" middle disjunct is about some World `v'` at
  which the call is admitted, not about follow's `wf`.
- `Socket.lean:39-41` advertises this theorem as taking the row "to the World that commits the
  call".
- Mutation that shows it: none is needed. The statement is satisfiable for every call `c` by the
  existence of a second preimage. INFERRED, a counting argument: it cannot be proved in Lean, but
  it is true in any model where the hash behaves like a function on an infinite domain.
- Sound form: the third disjunct over the calls actually absorbed on follow's frames (an explicit
  list `S`, `CollidesAmong hash S`), which needs `JournalFrom` to record the path, not a `Q`.
- No consumer outside docstrings (grep: only Socket.lean:41, BellRow, SocketStrong.lean:638).
- Severity: DEFECT. The theorem says "the journal entry at a call's id was put by committing that
  call" (Committed.lean:2) and does not.

**D2. Law 7: an ok read whose stdout is not UTF-8 is read as "nothing pending"; the kept answer is
forgotten and the ring is asked about again, and `bell_resident_conforms` calls that legal.**
- READ Run.lean:400 (`Ring.readAll sh ((String.fromUTF8? r.stdout).getD "")`), Run.lean:360 (the
  same in the re-read) and Trace.lean:32 (`readRings`, the same). MEASURED with
  `lean t.lean` on the repo's toolchain:
  - `"".splitOn "\n" = [""]`;
  - filtered, it is the empty list;
  - `String.fromUTF8? ⟨#[0xff, 0x0a]⟩` is `none`.
  So `Ring.readAll sh "" = .ok []`.
- What follows:
  - in `actOn`, `decideTick [] (some kept) = .idle` → `forgetThen` (Run.lean:379);
  - in `deliverP`'s re-read, `ring ∉ []` → forget (Run.lean:363-366);
  - the next tick reads the ring pending again with nothing kept → `.ask` → a second spent ask,
    charged to the meter. That breaks "Exactly one ask per ring (each ask costs the meter)"
    (Bell.lean:26).
- The theorem side agrees with the bug: `Frees r (.cmd (.read sh) y)` holds when
  `readRings sh y = some p ∧ r ∉ p` (BellConform.lean:52). A non-UTF-8 reply gives `some []`, so
  `bell_resident_conforms` (:356) allows the second ask. `tick_order`/`TickCore` (via `readRings`)
  state the same reading.
- Reachability: an honest follower prints every byte string as `"text"` or `#hex`
  (Lang/Print.lean:94-97, READ), so its stdout is always UTF-8. The input therefore needs the
  trusted relay to corrupt bytes, which is exactly the boundary premise law 4 says to assert where
  it enters.
- Mutation: an ok reply frame to `read OBJ pending 64` whose stdout is the single byte `0xff`. The
  resident forgets the kept answer and asks again.
- Law 7 (READ CHARTER.md:96-97): "a parse failure is never rendered as a verdict". Here a decode
  failure renders as the verdict "nothing pending". The describe path does the same (`getD ""` →
  `noCore` → `bellShape`), but that one ends the process by name, which is fine. The read and
  re-read are not.
- Severity: DEFECT (law 7; a double charge on the input; a cross-tick theorem that blesses it).

**D3. Every invoke exit other than ok and refused repeats forever with no bound and no named end,
`declined NAME` included; the docstring calls it "crash-stop".**
- READ Run.lean:367: `else .say s!"answer unsettled exit {r.exit}" (.done (.next m))`, and
  :344 for `.error`.
- `Mem.unread` counts only refusals whose re-read failed (Run.lean:352-355), with the stated rule
  "a refusal must not repeat forever" (Run.lean:137-139). `declined` is a refusal by name
  (Protocol/Command/Exit.lean:25-27: "the writer refused the call by name and did not record it";
  Protocol/Attempt.lean:27-28: "unauthenticated, an early window, the member's refusal budget").
  It never reaches either counter.
- Mutation: a resident whose member key the writer does not recognise (unauthenticated → declined)
  logs `answer unsettled exit 53` once a second for up to `lifetimeTicks` = 2^48 ticks (Run.lean:113).
  It never exits, so the controller's `crashLoop` (an exit count, Run.lean:75-76) never sees it. The
  same holds for:
  - a persistent `client` (52) or `hostContradicted` (55);
  - the resident's own `argvPastBound` (Sockets.lean:72; unreachable for Bell-bounded texts,
    INFERRED from `argvBytesMax = 2·eventBytesMax + 1024`, Protocol/Table.lean:422);
  - a describe refused `wrongKind` (the config names a non-object cell), which loops at
    Run.lean:412-413 forever. That one is unlike `missingCell`, the birth race HOSTING-35 means to
    retry.
- `Socket.deliverAfter_unsettled` (Socket.lean:516-521) is a true one-tick iff, but its docstring
  says "R2 and R3 are crash-stop to the resident". Across ticks the resident is retry-forever:
  the docstring lies about the behaviour the theorem's name evokes.
- HOSTING-42 cites this theorem as covering R1-R3 ("is followed by what a failure is followed by").
  That is true, and it is the problem: a failure is followed by an unbounded retry.
- Severity: DEFECT (a refusal by name that repeats forever, against the code's own rule; the
  HOSTING-46 question's answer is "yes, `declined` and five other exits").

### QUESTION

**Q1. The `stdio-leg` row (gates/tcb.tsv:54) is not one sentence about bytes.**
- READ the row: "served, in the order it sent them, by ONE follower (nd-supervise's one child, host
  follow, whose World moves only by the frames it answers): an ok reply … is that follower's Lean
  done of that command, run from a World it reached from where the previous ok command's done was
  handed out: nd --stdio gave follow the resident's argv, gave follow back byte for byte every
  continuation follow handed out, and the resident decoded follow's done".
- It holds at least four distinct trusts:
  1. Topology: one child behind the socket for the resident's whole process life.
  2. Follow's World dynamics: "moves only by the frames it answers". In Lean this is
     `Host.Follow.loop` (Host/Follow.lean:91-133, IO), which no theorem states; HOSTING-43(a) says
     "READ".
  3. Durability and reopen: a follow restart reopens exactly the World its acknowledged appends
     persisted (HOST-22). That is Store, fsync and OS, not bytes on a socket.
  4. Continuation SELECTION: `FollowRun.step` (Socket.lean, `hk : r.cont = some k`) requires that
     nd resend THIS command's continuation. `k` is unauthenticated, and nd's attempt loop chooses
     which `k` and which result to send. HOSTING-42's meta-critique names this but the row's
     "trusted for" does not.
- Item 2 checked (READ Machine.lean:1347-1351): the loop's `.adopt` branch sets `world := w'`
  (Follow.lean:133), and `Command.step`'s adopt arm returns `({ world := w', … }, .adopt w', …)`, so
  `f'.world = w'` and the move IS a `Moves`. Consistent.
- What would decide it: split the row into (a) the relay of three byte fields, (b) one-follower
  topology, (c) follow's durability (HOST's row?), and (d) continuation choice. Check whether (b)
  and (c) already have rows elsewhere in tcb.tsv (20 HOSTING rows; I did not read the rest).

**Q2. `Reach` over `Command.step` with ANY continuation, ANY result and ANY Follow carrying that
World: too weak to be about this resident? No.**
- READ Socket.lean (`Moves`: `∃ f f' kb res p r, f.world = w ∧ Command.step … f kb res = (f', p, r) ∧ f'.world = w'`).
- The deployed follow answers a `resume` frame with whatever `k` the frame carries
  (Host/Follow.lean:76-80). Any client of the member socket can send any bytes, so a `Moves` over
  ANY `kb` is what is TRUE of the deployed follower. A narrower premise would be false.
- Permissiveness in `Reach` makes `StdioLeg` easier to satisfy, so the theorem is STRONGER. It
  speaks of this resident through `FollowRun`'s chain from `Command.start … (c.argv conf)`, linked
  by `r.cont`.
- A hostile continuation from elsewhere lands inside `Reach`, and the theorems only use facts every
  step keeps (`step_packageAt`, `step_journalFrom`).
- `FollowRun.step` also runs the step at an arbitrary `g` whose World is reached, with its
  `download`/`verified` memory free. That too only widens the premise.
- The residual hole is the one HOSTING-42 names: a relay that substitutes another of follow's OWN
  continuations inside the chain. It is outside the premise, so it is a trust, not a proof gap.
- No defect. Recorded because the brief asked.

**Q3. `run`'s start state is discharged by reading `run`, not by a theorem; and one follower per
process life is a premise the deployment may not keep across a member re-genesis.**
- READ:
  - `delivered_answer_committed_strong` (SocketStrong.lean:640-658) takes `Lifetime w m es`,
    `m.shape = none` and `KeptOk m.kept`.
  - `run` builds `m := { shape := none, kept }` (Run.lean:453), with `kept` from `seedOf held`, and
    `seed_ok` (Lifetime.lean) proves `KeptOk` of any seed.
  - `run`'s `for` loop (Run.lean:454-458), which calls `tick w m` and threads `m'`: no theorem says
    its effects form a `Lifetime`.
  - `interp_runs` is at the recording handler only, and `ResidentRun.lean:31-33` says so ("that IO's
    bind sequences effects is the runtime's").
  So the premise chain stops at code reading for `run`, which is fine and is stated.
- The sharper question: `Lifetime` + `StdioLeg` need ONE follower whose World only moves forward
  for the resident's whole process life. Greenfield re-genesis is routine (CLAUDE.md). If the
  member's follower Store is replaced while the resident keeps running, these persist and are
  never re-derived:
  - `Mem.shape`;
  - the kept file `vol/kept-<bell hex>` (Run.lean:442);
  - the config's bell id.
  Then `Reach` is false and the theorems go silent, while the resident acts on a shape described
  on the old chain.
- What would decide it: whether the resident grain is restarted whenever its member's
  nd-supervise/nd-members is re-genesised (Ops/Units.lean; not read past the grep), or whether the
  resident re-describes.

**Q4. `Mem.shape` persists across ticks; "same object" is checked by nothing at runtime.**
- READ:
  - `shape_provenance` (Lifetime.lean:243-268) gets "same object" from `Cmd.argv` being a function
    of the fixed `w.conf`, plus `StdioLeg`. There is no digest.
  - The description prints `object HEX` (Machine.lean:622) and `package HEX` (Machine.lean:612).
  - `bellCore` reads only the `core` line (Bell.lean:138-143). It never compares `object` with
    `c.bell`, nor `digest(core)` with the `package` id.
- Law 4 (CHARTER.md:66-68): "an assertion for every PREMISE the types do not carry (decoded bytes …
  anything that crosses a boundary), placed where the premise enters". The premise "this reply
  describes `c.bell`" crosses the member socket. A check against the `object` line costs one line
  compare.
- Mutation: the relay hands the describe reply for another Bell-shaped object. The resident
  accepts it (`shapeOk` is shape, not identity; HOSTING-45's critique) and caches it for the
  process life.
- Under `StdioLeg` it is unreachable (A2).
- Severity: QUESTION, whether law 4 demands the assertion when a trusted row already covers it.
  Decide by ruling on whether "trusted-unverified" rows exempt their premise from law 4.

**Q5. `Hosting.Proofs.Reply` does not build at 10 GB, sits in the default target, and was not
built in HOSTING-43's control.**
- READ decisions/hosting.md:2337: "all 469 library modules but Hosting.Proofs.Reply (OOM at 10G
  alone; not built)". The module is in `lean_lib Hosting`'s globs (lakefile.lean:41-42, READ).
- Its teeth are `decide +kernel` on JSON strings (Proofs/Reply.lean:71-152).
- MEASURED (`git log 9df02da..origin/main` on Hosting/Reply.lean, Broker.lean, BrokerWire.lean,
  Proofs/Broker.lean, Codec/Proofs/Layout.lean): no commit touched them since it was introduced.
  Transitive imports were not checked.
- Law 9: "`lake build` of the commit's import closure passes BEFORE push". On the laptop bound
  (6 GB) it cannot.
- What would decide it: one hbox build of `Hosting.Proofs.Reply` at f9657bd with a raised
  `SWARM_MEM_MAX`, and a record of who last built it green.

**Q6. Same key, same text, re-rung between derive and commit: a stale pin may end the resident
`answerRefused`.**
- READ Run.lean:21-23: the client pins `pending[k]` and `rings[k]` itself.
- If the ring at `k` is retired and re-rung with the same text after `derivePins` and before the
  commit, the invoke is refused (stale pin). The re-read lists a ring equal to `r` (same key, same
  text), so the resident ends `answerRefused` (Run.lean:363), although a retry would succeed. The
  Run.lean header discusses key reuse but not this ordering.
- INFERRED: I did not read `derivePins` or the kernel's pin refusal.
- Decide by reading the client's pin derivation, and whether a stale pin refuses as `refused`
  (exit 1) or as something else.

### DEBT

**B1. Two line splitters for one output grammar (law 1).**
- `Ring.readAll` splits with `String.splitOn "\n"` and drops blank pieces (Bell.lean:201-202).
- `Shape.read` splits with `splitLines` (Bell.lean:98-104).
- HOSTING-43(iii) replaced `splitOn` for the description only ("The resident's `Shape.read` now
  splits with `splitLines`"). The range read is still on the old splitter, with its own "a blank
  line is no row" rule.
- No theorem relates the two splitters. `rangeLines_reads` is about the lines, but which splitter
  reads them back is a second fact.

**B2. The shape is read twice, from two sources, and the decoded package is thrown away (law 1).**
- `Shape.read` (Bell.lean:167-170) does `let _ ← bellCore ls`, which decodes the package `p` and
  checks `Lang.Bell.shapeOk p`. It then derives the `Shape` from the PRINTED lines (`answerWords`,
  the `rel (pending …)` line).
- `shapeOk p` already fixes `p.rels = rels` (with pending's limit) and `answer`'s type
  (Lang/Bell.lean:106-108). So the `answerType`, `pendingType` and `pendingLimit` refusals of
  `Shape.ofLines` (Bell.lean:148-162) restate it. They hold because `describe_shape` proves that
  the printer agrees with the package.
- The index of `answer` and the pending declaration could be read from `p` directly. Two readings
  of one fact are two readings that can drift.

**B3. `textMax = 2000` is a twin of `Lang.Bell.answerBounds`, and the comment's justification is now false.**
- READ Bell.lean:231-234: "The description shows the argument's type, not its bound. So this is
  the one copy of the bound".
- `Lang.Bell.answerBounds` (Lang/Bell.lean:85) holds the same 2000, and Hosting imports `Lang.Bell`
  (Bell.lean:37).
- Since HOSTING-45 the description carries the package bytes, so the bound is visible.
- No theorem ties `textMax` to `answerBounds` (grep: `textMax` appears only in Hosting/Bell.lean,
  Proofs/Resident.lean and Proofs/Lifetime.lean).
- Mutation: set `answerBounds` to 1000. Hosting stays green, and every answer over 1000 bytes is
  refused → `answerRefused`, a stop.

**B4. Two inductives for one process's ticks, and a duplicated lemma (law 1).**
- `BellConform.Ticks` (BellConform.lean:41-47) and `Lifetime.Lifetime` (Lifetime.lean:27-30) both
  mean "each tick a `Runs (tickP w m)` path from the memory the last went on with". `Ticks` splits
  per tick and carries a `stop`-ended last tick; `Lifetime` flattens.
- `core_append` is proved twice (Lifetime.lean:32, BellConform.lean:133).
- `bell_resident_conforms` and `shape_provenance`/`lifetime_invoke_kept` are therefore about two
  objects. A consumer that wants both must bridge them, and no bridge exists.

**B5. The tick program is restated as a Prop next to itself (law 1, mild).**
- `readRings` and `describedShape` (Trace.lean:30-39) repeat the inline decode logic of `readP`,
  `deliverP` and `tickP` (Run.lean:356-419). They are not called by it.
- `TickCore`/`ActCore`/`DeliverAfter` (ResidentRun.lean:76-124) transcribe the tree's branches.
- The proofs tie the two, so nothing lies. But `tick_order` is largely "the program, re-written",
  and its force is in the `order_refuses_*` teeth and `tick_counts`.
- Calling `readRings` from `readP` would make it one definition.

**B6. `bellShape`'s exit detail drops the reason (law 7, minor).** `tickP`'s failure ends
`.stop .bellShape "description"` (Run.lean:419). The reason (`notBell`, `noCore`, `answerType`, …)
appears only in the preceding `say` line. HOSTING-45 documents the stderr line
`resident: bellShape notBell`. The process prints that line and then `bellShape description`.

**B7. `fit` names "(empty reply)" for a non-empty reply.** `utf8Prefix.go` walks back over
continuation bytes to 0 when every byte up to `textMax` is `10xxxxxx` (Bell.lean:243-245). `fit`
then answers `(empty reply)` (Bell.lean:252-254), although the provider sent 2001+ bytes. This is
unreachable through `Broker.reply`, which requires UTF-8 (Reply.lean `reply`), so it is only a
misnomer in a total function.

**B8. `unread` "in a row" is not in a row.** `Mem.unread` (Run.lean:134-135, "refusals in a row
whose bell state could not be re-read") is reset only by an ok answer or a gone-forget (Run.lean:348,
:366). Ticks between two such refusals, such as an invoke `.error` or a successful read, do not
reset it. The comment and the counter disagree on what "in a row" means.

**B9. The general JSON-reader facts exist only as closed instances.** Proofs/Reply.lean:71-152
checks, each by `decide +kernel` on one fixed string:
- a repeated `content` is refused;
- a repeated `text` is refused;
- a raw control byte is refused;
- trailing bytes are refused;
- the depth bound holds.
The header states the general fact: "A key that occurs twice in any object of the body, at any
depth … the body is refused" (Reply.lean header). GUARD-DISCIPLINE's rule is to prove the general
fact where the guard is one instance of it. These closed instances are also what OOMs the module
(Q5).

**B10. The name `answered_row_is_kept_answer` reads as a universal.** HOSTING-44's own critique
says so. I record it because the docstring of Socket.lean:39-41 now advertises the join as
reaching "the World that commits the call", which D1 shows is not what `answered_row_committed`
says.

---

## What I checked and found right (so the next reader need not)

- `notSent` vs spent (Sockets.lean:89-104): `.notSent` only before `writeAll` returns. INFERRED:
  `nd_conn_write_all` errors only before the last byte, so `notSent` means "not in full" and
  keybroker sees a truncated frame and makes no call.
- `decide_kept_first` / `decide_ask` / `decide_answer` (Proofs/Resident.lean) match `decideTick`
  (Bell.lean:218-227); `order_refuses_*` reject the orders the header lists.
- `deliver_gone_continues` (ResidentRun.lean:509-546): the statement is exactly the gone branch and
  excludes `answerRefused`. Its plant is recorded in HOSTING-46.
- `step_invoke_ok` / `run_invoke_ok` / `start_ne_ok` (Socket.lean): an `ok` for the resident's
  invoke can only be the phase-4 settlement. `LegFrom` reads the `ok` bit as a Nat compare before
  `toUInt8`, so a wide exit cannot alias 0.
- The strong theorem's join (SocketStrong.lean:660-700): it runs from describe to invoke through
  `legFrom_suffix`; the plants P1-P3 of HOSTING-43 each target one link.
- The adopt move is a `Moves` (Q1, READ Machine.lean:1347-1351).
- Bell bounds: the ring's text (`bytes 1 2000`, world/resident/Bell.ob:29) equals `ringText`'s
  (:12), so the re-sent text always fits.
- Broker (Broker.lean, Proofs/Broker.lean statements): `decide_ok`, `grant_allowed`,
  `capped_decide`, `start_window_refused` and `step_encodes` are stated about the deployed `decide`
  and `step`. I found no vacuous premise in the statements I read.
- Allowance: `allowanceOf_sound` / `seed_reads` say what the header says.

---

## Files NOT read (or read only in part), with sizes

Not read at all:

| file | lines |
|---|---|
| Hosting/Proofs/Loop.lean | 664 |
| Hosting/Proofs/ResidentVolume.lean | 606 |
| Hosting/Proofs/Controller.lean | 415 |
| Hosting/Proofs/Plan.lean (docstring only) | 359 |
| Hosting/BrokerWire.lean | 307 |
| Hosting/Wire.lean | 300 |
| Hosting/Sim/Journey.lean | 267 |
| Hosting/BrokerExit.lean | 217 |
| Hosting/BrokerCli.lean | 205 |
| Hosting/Proofs/Package.lean (docstring only) | 198 |
| Hosting/Loop.lean | 193 |
| Hosting/Proofs/Wire.lean | 186 |
| Hosting/Cli.lean | 175 |
| Hosting/Plan.lean | 167 |
| Hosting/Sim/Allowance.lean | 140 |
| Hosting/LaunchExit.lean | 134 |
| Hosting/Drive.lean | 122 |
| Hosting/Resident/Args.lean | 121 |
| Hosting/Controller.lean | 120 |
| Hosting/Package.lean | 110 |
| Hosting/Proofs/BrokerExit.lean | 82 |
| Hosting/Lifecycle.lean | 77 |
| Hosting/Resident/Volume.lean | 73 |
| Hosting/Proofs/Open.lean (docstring only) | 73 |
| Hosting/ResidentsCli.lean | 70 |
| Hosting/Proofs/Deployed.lean (docstring only) | 64 |
| Hosting/Proofs/Lifecycle.lean (docstring only) | 60 |
| Hosting/Proofs/Residents.lean (docstring only) | 57 |
| Hosting/Proofs/LaunchExit.lean | 56 |
| Hosting/Sim/Run.lean | 52 |
| Hosting/Proofs/Frame.lean (docstring only) | 39 |
| Hosting/Track.lean | 35 |
| Hosting/Pins.lean | 30 |
| the six 3-line `*Main.lean` files | 18 |

Read in part:

| file | lines | what I read |
|---|---|---|
| Hosting/Proofs/SocketStrong.lean | 733 | lines 1-120, the theorem list, the strong statement and the first 60 lines of its proof |
| Hosting/Proofs/BellRow.lean | 250 | header and statements |
| Hosting/Proofs/Broker.lean | 936 | statements only |
| Hosting/Proofs/Allowance.lean | 368 | statements only |
| Hosting/Proofs/Reply.lean | 154 | statements only; not built, per the brief |
| Hosting/Proofs/Lifetime.lean | 540 | about 330 lines whole; the bounds lemmas by statement |
| Hosting/Proofs/BellConform.lean | 365 | about 150 lines and the main statement; `ticks_debt` / `debtRun_frees` not read |
| decisions/hosting.md | 2459 | HOSTING-42..46 whole; titles of the rest |

`Proofs/ResidentVolume.lean` (the volume contract) and `Proofs/Loop.lean` (the controller round)
are the largest unread files. The next reader should start there.
