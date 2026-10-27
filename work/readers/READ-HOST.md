# READ-HOST — nanodregg `Host/` read whole (origin/main f9657bd), 2026-10-24

Reader: one sub-Opus, read-only. Nothing in nanodregg was edited. Tags: READ (path:line), MEASURED
(a command I ran; every MEASURED here is a grep, no build was run), INFERRED.

## Verdict

I read 26 of Host's 63 files whole: Serve, Follow, Deployed, Loop, Batch, Wire, Cli, Store, Open,
File, Physical, Check, Record, Keys, Bounds, Log, Tail, Base, Segment, Page, IdentityImage,
Sim/MemStore, Proofs/Serve, Proofs/Trusted, Proofs/Refine and Proofs/Follow, plus `Host/c/file.c`.
That is about 7,900 of 18,005 lines. I also read the statements and module headers of
Proofs/Deployed, Backup, Cli, Batch, Loop, Open, Tail, Coherence, StoreIndex, Index and Seal, and
the heads of Exit, Carry, Sim/File and Sim/Run. Outside Host I read what Host leans on:
`Protocol/Attempt.lean`, `Command.absorbStep`/`step` (Protocol/Command/Machine.lean:428-530,
1160-1360), `Kernel/Receive/Audit.lean`, `World.admit`/`checkWith` (Kernel/World.lean:1406-1560),
and `client/src/run.rs:117-129`.

The writer and the follower are mostly what their docs say. The writer's step is `judge`'s
(`step_submit`, `machine_commits`). Replies leave only after the fsync. The follower re-derives
every logged event kind by the kernel's own functions and trusts none from bytes. The codec premise
is proved, not assumed (§Answers).

The three worst things:

1. **(DEFECT)** The writer refuses a never-admitted frame with the FINAL status. A frame still
   queued at an exit gets `refused stopped`, and its own docstring says resending it is safe. The
   client reads `refused` as the Host's final word, asks follow to confirm, follow says `open`, and
   the run ends `contradicted (hostContradicted refused open)`. An honest Host shutting down is
   reported to the member as a Host that lied.
2. **(DEFECT, the theorem is about the wrong object)** `host_run_audits` / `host_run_kept` say "the
   follower's audit accepts what the Host staged". That audit is `Kernel.Receive.audit` over
   `Step`s, which no deployed follower runs. `host follow` runs `Protocol.Command.absorbStep` over
   `Page.stepEvent` bytes, a second re-deriver of the same fact (law 1). For those bytes I found the
   completeness direction ("an honest writer's page is absorbed") proved only for cancels.
3. **(DEBT, with a law-4 QUESTION)** HOST-64 moved the writer lock off the append fd onto the key
   file's read handle. That handle is now a held-but-unused value, kept alive by a dummy re-`flock`
   (`Writer.hold`) at five call sites: the exact pattern CHARTER law 4 says must never recur. Law 4
   (CHARTER.md:74-78) and HOST-19 (decisions/host.md:406) still say the lock is the append fd. One
   Ops plant covers `serve`; nothing covers `follow`'s lock.

`WriterLife`/`writer_life_trusted` is not vacuous, but it promises a member nothing (§F5).

---

## Findings, ranked

### DEFECT

**F1. `refused stopped` (and lookup's `refused undecodableCall`) uses the final status for "nothing was decided".**
- READ Host/Serve.lean:66-68: `FrameRefusal.stopped`, "nothing of it was admitted, and resending it
  to the restarted Host is safe".
- READ Host/Cli.lean:368: `refuseQueued port (named FrameRefusal.stopped.name) …`. `named` is
  `Protocol.Status.refused.code` (Serve.lean:88-89).
- READ client/src/run.rs:117-129: `hint` maps status `refused` to `Seen::Refused` by the status
  byte alone; the payload is not consulted.
- READ Protocol/Attempt.lean:118-119 and 128: `(submit, refused)` and `(lookup, refused)` lead to
  `confirm`, then `(confirm, open)` to `contradicted`.
- Why it is wrong: law 7 says the status is the verdict. PROTOCOL-41 introduced `declined`
  (refused by name, NOT final) for exactly this class, and Serve uses it for an undecodable submit
  (Serve.lean:135) and cancel (176, 179). Two arms keep `refused`:
  - `stopped`;
  - lookup's undecodable payload (Serve.lean:149), whereas submit's identical condition is
    `declined`.
- What shows it (INFERRED from the table, not run):
  1. Queue a submit behind a batch whose append fails, so the resident exits `uncertain` and
     `refuseQueued` answers the queued frame `refused stopped`.
  2. The client's attempt goes submit/refused, then confirm.
  3. Follow answers `open` (the call is absent and its window is live). The run ends
     `contradicted`, naming the Host as having said `refused`.
  4. The attempt stays open on disk (Attempt.lean:25-26), so the next run recovers. The damage
     is a false accusation of the Host and a stopped run, not a lost call.
- The same mismatch appears in `wrongSocket`, `notServed` and `unknownOp`, all `refused`, though
  those do not reach a submit. `pageIo` is also `refused`, and the follower reads it as "not now"
  by NAME (Loop.lean:293-295, Machine.lean:1359). That is a status overridden by a payload string,
  the shape law 7 exists to kill.

**F2. The Host's refinement says the follower accepts the Host's log, about a re-deriver the follower does not run.**
- READ Host/Proofs/Refine.lean:243-254 (`host_run_audits`) and 451-461 (`host_run_kept`). The
  conclusion is `audit X w (staged steps) = .ok w'`, with `audit = Kernel.Receive.audit`
  (Kernel/Receive/Audit.lean:68-76).
- The module doc says: "`host_run_audits` says the follower's audit accepts what the Host staged"
  (Refine.lean:17-19).
- READ Host/Page.lean:10-11: "The follower re-judges each one and takes the same step
  (`Kernel.Receive.audit`)." That is false. The deployed follower is `Host.Follow.answer`, then
  `Protocol.Command.step`, then `absorbPage`, `absorb` and `absorbStep` (Machine.lean:437-464),
  over the bytes `Page.stepEvent` writes (Page.lean:95-99).
- The two re-derivers differ:
  - `auditTurn` re-derives a Turn (`rederive X w t`); `absorbStep` decodes call bytes and runs
    `submit`.
  - `auditRefusal` compares the recorded refusal `r' = r`; `absorbStep` cannot, because a page
    carries only the call. It records the follower's own `judge` result and relies on the page-end
    chain check.
  - `auditRefusal` refuses `staleRecorded` by name; `absorbStep` does not test it.

  Two definitions of "re-derive a logged step" is law 1's defect.
- MEASURED (grep of Protocol/Proofs, Host/Proofs and Kernel/Proofs for `absorbStep`, `Honest` and
  `stepEvent`): the absorb theorems are soundness-direction: what absorb accepts is a
  `World.step`, `absorbStep_step` (Protocol/Proofs/Command.lean:461). The honest-page completeness
  theorem exists only for cancels (`absorbStep_cancelEvent`, Command.lean:819). I found none for
  `eventTurn ‖ t.event` of an admitted Turn or `eventRefusal ‖ r.event` of a judged refusal.
- What shows it: a change to `absorbStep`'s Turn arm that refuses every honest Turn event
  (e.g. replacing `submit` by `.error (.eventMismatch pos)`) leaves `host_run_audits`,
  `host_run_kept` and the whole Refine module green. Only the rows would go red.
- What would decide it: a theorem, at the deployed `X`, that `absorb X w #[] (staged.map
  (stepEvent ∘ fst))` returns `(admitBatch w qs).1` for every batch, or deleting `Kernel.audit` in
  favour of the one the follower runs.

### DEBT

**F3. The writer lock is a held-but-unused handle again, and law 4 and HOST-19 describe the old one.**
- READ Host/Store.lean:19-20, 341-353, 379-380: the lock is `File.open (keyPath dir) .read` plus
  `tryLock`. It is never read or written after that; `Writer.hold` re-`flock`s it only to be a "later
  use" (Store.lean:351-353).
- Call sites: Cli.lean:300, 318, 386, 407, 453 and Sim/File.lean:79.
- READ CHARTER.md:74-78: "must be the handle actually in use, never a held-but-unused value …
  until the lock became the append fd itself (HOST 7e23642)".
- READ decisions/host.md:406: "the locked append handle stays the lock".
- MEASURED `git log -S"Writer.hold"`: the move landed in eb7028d (HOST-64), whose entry I did not
  find stating it.
- The lock's role (answering the brief):
  - It is the SAFETY argument for one writer per Store. Nothing else excludes a second appender:
    no owner epoch in the files, no fencing token. Two interleaved appenders would chain frames
    from stale tags, and the next open refuses `corrupt`.
  - `flock` is released by the kernel at process death, SIGKILL included (READ file.c:126-134), so
    there is no stale-lock-file state.
  - A second `openWriter` gets `locked` (Store.lean:380), which is fatal-class by ROOT's ruling
    (Exit.lean:13-14).
  - `flock` is advisory: anything that does not call it (an rsync into the directory, an operator's
    `cp`) is not excluded.
- Plants: Sim/File.lean:76-79 tests a second `openWriter` IN PROCESS after `serve` returns, with
  its own `wr.hold` after. It would stay green if `serveVerb` dropped its `wr.hold`. Ops'
  `seal-live-writer-locked` (Ops/Plants.lean:797-835) does run a live `host serve` child and is the
  real tooth for `serve`.
- QUESTION: no plant runs a second process against a live `host follow` Store. `followVerb`
  (Cli.lean:389-408) relies on the same `wr.hold`. Lean's closure conversion may capture
  projections of `wr`, which would free `wr.lock` early. What would decide it: a `follow-live-locked`
  plant (a live follower, then `host seal` on its Store gets `locked`), or putting the lock back on
  a handle the loop uses.

**F4. Follow's `stepTooLarge` is not "before the machine": a step's effects persist while its reply is refused.**
- READ Host/Follow.lean:25-27 lists `stepTooLarge` among "Refusals before the machine".
- READ Follow.lean:63-66: `stepOut` returns `(fs', p, refused stepTooLarge)` WITH the step's
  `Persist p`.
- READ Follow.lean:108-116 and 117-133: the loop appends `p`'s steps (or seals the adopted base)
  and moves `dl`, then sends the refusal.
- `Reply.bytes` is `none` when a reply field is past `frameBytesMax`, or the step is a `.host`
  submit (READ Protocol/Command/Wire.lean:4-8, 41). A `read`/`describe` render too large for a frame
  on the last page of a catch-up therefore persists the page's steps and answers `refused`.
- Safety holds (the steps were re-derived). But the comment is false, and a `refused` reply whose
  effects are durable contradicts the writer's rule that a reply never misstates what was
  committed.

**F5. `WriterLife` / `writer_life_trusted`: what it promises a member is "nothing", and "trusted" overstates.**
- READ Host/Proofs/Trusted.lean:76-82, `CheckpointTrusted o w`. It says `w` folds by `World.fold`
  from some genesis or import `w₀` whose origin is `o`, which passed `budgetFault` and is `Kept`.
- "Admitted" there is `World.step`, which checks bounds, window, journal, value, nullifiers, rows,
  charge and creates, and no signature (READ Kernel/World.lean:1406-1420; authority lives in
  `Receive`, which the fold never calls).
- The import disjunct is over ANY bytes `f` that `Carry.read` accepts (Trusted.lean:80-81), so
  "trusted" admits any budget-bounded World a crafted carried file makes. The module says so
  itself (Trusted.lean:123-125: "instantiated at `w.origin` itself it certifies any World some start
  admits, a forged import included").
- So the content is: origin = `o`, `Kept`, size ≤ `worldBytesMax`, potential ≤ `potentialMax`.
  It says nothing about who authorized the steps.
- READ Trusted.lean:239-248: `WriterLife` links quantify over arbitrary `H I S` (header, index,
  segment bytes) and an arbitrary admitted list `l`. A life is any sequence of abstract
  open/fold/seal events; it is tied to `Loop.serve` only by "read off" (Trusted.lean:228-232,
  HOST-69). `writer_life_trusted` is `trusted_fold` and `sealed_trusted` iterated.
- The case a MEMBER is in, a thin adopt of a received base, is exactly the one not discharged
  (Trusted.lean:43-47). `Follow.loop`'s adopt arm (Follow.lean:117-133, Machine.lean:1326-1351)
  checks the pin digest, `atGenesis` and origin. It checks no budget, so an adopted World above
  `potentialMax` is accepted (PROTOCOL-22 `untrustedAdopt`, named there).
- So `writer_life_trusted` promises the WRITER that its next seal never refuses `worldTooLarge`
  from tail growth. It promises a member nothing; the docstrings ("holds trusted bases
  throughout") read like more.
- Not vacuous: `life_refutes_potential` (Trusted.lean:324-329) is a real tooth.

**F6. The `Honest` conjunct of `host_step_folds` has no witnessed tooth at a decoding `Ctx`.**
- READ Refine.lean:324-355: `host_step_folds_tooth_unjudged` is stated at
  `X' := {X with decodeCall := fun _ => none}`, where `Honest` is False for every nonempty log
  (each arm needs `decodeCall` to return `some`). It shows `Honest` refuses everything there, not
  that it separates a judged step from an unjudged one.
- READ Refine.lean:377-383: the meaningful tooth, `_censor`, says of itself: "The premises' joint
  satisfiability … is not witnessed in Lean." A tooth whose premises may be unsatisfiable proves
  nothing; this is the falsifier-that-stopped-falsifying class.
- What would decide it: one instance (toy `Ctx`) of `hj`, `he`, `hk` and `hr` together, or a lemma
  that `World.refuse` accepts the judged-refusal record of an admissible call (KERNEL's
  `checkRefusal` shape).

**F7. Base.lean's module doc describes the pre-HOST-64/71 base and open.**
- READ Host/Base.lean:4-5 gives the layout `shapes32 ‖ world ‖ u64 offset ‖ tag32 ‖ u64
  indexCount ‖ indexLast32`. The codec (Base.lean:94-100) also carries `retainedFrom` and
  `indexFrom`, and the file carries Physical's generation-and-MAC trailer (Physical.lean:15-17,
  Store.lean:594).
- Base.lean:38-44: "Open reads the base…, the origin frame at 0 (at most `originMax` bytes,
  checked against the base World's origin, HOST-25)". `openWith` (Open.lean:179-225) never reads
  offset 0; it checks the base file's checkpoint header (`headerFault`), as Open.lean:21-24 and
  Check.lean:41 say.
- `originMax` is not defined anywhere in Host (MEASURED grep: only `chainBytesMax`,
  Base.lean:68-69, whose docstring calls it "`originMax`").

**F8. `host seal`'s "the ONE effect that writes" and HOST-43's "at a sealed position it writes nothing" are false after a crash.**
- READ Cli.lean:410-412 and 420-422 (`sealWith`: "any refusal before it is answered by name with
  nothing written").
- READ decisions/host.md:2141: "At a Store whose newest base is already at its tip it seals
  nothing".
- The open is `openWriter` (Cli.lean:444), which truncates a torn tail and orphan index entries and
  syncs (Store.lean:385-393). With `--retain` it also unlinks surplus files (Store.lean:394).
- `seal_writes_iff` (Proofs/Cli.lean:114-122) models `open_` as pure, so it cannot see this. The
  writes are correct, and the comments say they do not happen.

**F9. `openFollower` has a live-sounding name and no deployed caller; Check's doc says it uses it.**
- READ Store.lean:398-402: "Open the Store as a follower of its directory".
- `host follow` opens with `openWriter` (Cli.lean:398), by HOST-22.
- MEASURED grep: `openFollower` is called only by Sim/File.lean:89. Check.lean:4 says check
  uses it, but check calls `openAt` (Check.lean:226).

**F10. `memCheckpoint.adopt` checks a different precondition than `prepareAdoption`.**
- READ Sim/MemStore.lean:67-85 requires `b.index.isEmpty ∧ synced.size = pos.offset ∧ origin old =
  origin w ∧ pos.offset = frameSize (origin old)`, plus the header check.
- READ Store.lean:452-466 (deployed) requires `newest = pos.offset ∧ k0 = 0 ∧ …`, then `body = 0 ∧
  h.start = pos.offset ∧ rf ≤ pos.offset`, then the `headerFault` at count 0, then `Base.seal`'s
  `indexMoved` over the real index size.
- The memory twin has no `newest`/`body = 0` arm. The plants that drive it (the rows' thin adopt
  over memory) therefore test a guard the binary does not run. Law 1, at the plant layer.

**F11. The live-backup theorem is over the one-file model; retention rewrites what it calls append-only.**
- READ Proofs/Backup.lean:1-7 and 525-536. The copies are `I ++ x` and `S ++ y` of one index file
  and one segment byte array, and "the index file and the segment are append-only".
- Under `--retain N`, a seal writes `index.<k0'>.log` through `index.tmp`/rename, unlinks
  `index.<k0>.log`, and unlinks dropped `seg.*.log` (Store.lean:579-600). Copying in
  `backupOrder` (Base.lean:441-443) racing such a seal can find the index file the copied base
  names already gone.
- The refusal is by name (`missing index.<k0>.log`), so nothing is silent. But `openWith_backup`'s
  "never refuses …" list is a statement about a Store shape the deployed writer no longer has once
  retention is on, and Backup.lean's premises list does not say so.

**F12. The open theorems are over `openWith` in `Id` with logical readers; the deployed `openAt` path is read off.**
- READ Store.lean:287-323. The deployed open adds `missingOf`, `readBounded`,
  `physicalBaseRead`, `Base.peek` (an unauthenticated choice of files), `readHeader` with the
  generation, `Segs.size`/`cover` walking headers, and an index reader that answers
  `ByteArray.empty` below `k0·eb`.
- Every theorem in Proofs/Open, Backup, Seal, Deployed and Trusted takes
  `Id.run (openWith … (segReader I) (segReader S))`. HOST-71 states the mapping is "read off the
  code" (decisions/host.md:3244-3253).
- Recorded here because a reader citing `host_reopen_folds` as "the crash edge" would take it as
  being about `host serve`'s open; it is about `openWith` over two byte arrays.

**F13. host-sim's loop plants run a toy machine, not `Host.Serve.machine`.**
- READ Sim/Run.lean:46-52: the frames carry a STEP and are committed by `World.step`, "the sim
  exercises the log, the open and the pages, not the receive layer".
- So plants 1-6 of Sim/Run (replay answers `ok`, crash cuts, seal cadence) are over a twin
  handler. HOST-51's plant (one deployed submit through `judge`) is the only serve-path tooth there.
- The doc discloses this; it is listed because Sim/Run.lean:9-11 ("a resend of the same txId …
  answers `ok` with the original receipt") reads as a claim about the writer.

**F14. HOST-22's title still announces a mechanism the code no longer has.**
- READ decisions/host.md:542-553 (title: "open refuses `tailTooManyTurns`") against 586-590 (the
  amendment deleting `sealTurns`, `tailTurnsMax` and `tailTooManyTurns`).
- MEASURED grep: none of the three exists in Host. The status line says SUPERSEDED, so this is
  minor, but the title is what `grep -n '^## '` shows.

### QUESTION

**Q1. `host export` requires a STOPPED writer and does not ask the lock.**
- READ Cli.lean:154-171 ("Take it from a STOPPED writer (RUNBOOK §6)"). `Check.openClean`
  (Check.lean:221-231) takes no lock.
- A live export reads a consistent verified prefix, or refuses `missing` if a retention drop races
  it. That is probably harmless, but the premise is stated in prose and not asserted (law 4: an
  assertion for every premise). What would decide it: whether an export of a live writer's
  prefix is ever wrong. If never, delete the "STOPPED" requirement; if sometimes, `tryLock` and
  refuse `locked`.

**Q2. Frames read by the reader after `refuseQueued` closes the channel get no reply.**
- READ Loop.lean:420-428: `pump` reads a frame and `ch.send` fails after close; it returns `.eof`
  and the frame is dropped.
- READ Cli.lean:368: close happens after the rounds end. Loop.lean:399-401 says "no accepted
  request goes unanswered". Whether a frame read from stdin but not enqueued is "accepted" is the
  question.
- The mux sees the child exit and fails the connection (INFERRED; I did not read mux.rs's child-exit
  path).

**Q3. `agrees` (the fuel-restart pair assertion) does not compare the base the loop believes in.**
- READ Loop.lean:373-376 compares the World's mark, position, tag, base index count and last, and
  index size. It does not compare `sealed.offset`, `sealed.steps`, `sealed.digest` or
  `sealed.bytes`, which the next `read` page states (Page.lean:251-260) and an inviter pins
  (Machine.lean:532-540).
- A loop whose installed `Sealed` drifted from `base.world` would serve stale `baseSteps`/
  `baseDigest` hints until the next seal. The member's `pinOf` refuses rather than pins them
  (Page.lean:235-236), so this is liveness, not safety. What would decide it: whether any path
  installs a `Sealed` that is not the bytes just renamed in. I found none (`settle`, Loop.lean:215-224).

**Q4. `Log.badTail`'s forward scan is O(frameMax × record length) on a hostile tail.**
- READ Log.lean:115-119: for each of up to `frameMax` (~16.8 MB) offsets, `verifiesAt` MACs
  whatever length the 4 bytes there decode to, up to `recordMax`.
- An honest torn frame is cheap (small decoded lengths dominate). Crafted bytes can make one open
  hash on the order of 10^12 bytes (INFERRED arithmetic, not measured). Only someone who can
  write STORE can plant them (HOST-16), so this is a static-bound question (law 4: "a static bound
  on everything"), not an attack surface.

---

## Answers to the brief's specific questions

- **Law 4, the writer lock.** It is the SAFETY argument: the only exclusion of a second appender,
  with no fencing in the bytes. Stale lock: none possible; `flock` dies with the process (file.c:126-134).
  Two writers: the second `openWriter` gets `locked` (Store.lean:380), fatal-class, never
  auto-restarted (Exit.lean:13-14). It is advisory, so non-`flock` writers are not excluded. The
  handle is a held-but-unused value; see F3.
- **WriterLife's object.** A base FILE (bytes) related to the next base file by an abstract
  open/fold/seal over arbitrary segment and index bytes. `writer_life_trusted` promises that every
  base a life ends at holds a World with origin `r`, `Kept`, size ≤ `worldBytesMax` and potential
  ≤ `potentialMax`. To a member it promises nothing it would check: its case, a received base, is
  outside the theorem, and "trusted" carries no authorization (F5).
- **`absorbStep` re-derives every event.** READ Machine.lean:437-464:
  - tag 0, a Turn, by `submit` on the decoded call;
  - tag 1, a judged refusal, by `judge`, which must record;
  - tag 2, a cancel, by `cancel` under the event's signature, which must record;
  - anything else is `eventMismatch`.

  No kind is taken from bytes. Its trust points are elsewhere and are rulings:
  - follow's REOPEN folds its own records by `World.fold` with no signature verified (HOST-22);
  - an adopt trusts a base by its pinned digest, with no history and no budget check (F5);
  - page roots are not compared per step, only the page-end (steps, chain) is (`absorbPage`,
    Machine.lean:510-519), which covers them up to the chain's collision bound.

  The re-deriver twin is F2.
- **The attempt store and at-most-once.**
  - The attempt store is PROTOCOL's (`Protocol/Attempt.lean`). It persists the frozen signed call
    and a send count (Attempt.lean:4-8; client CLIENT-3). Host has no retry path.
  - On a failed append or sync, every reply of the batch is `uncertain` and the resident exits; it
    never retries (Loop.lean:362-365, HOST-4).
  - If a crash lands after the fsync and before the reply, the call is durable and journaled. The
    client's lookup or resend then gets `ok` with the ORIGINAL receipt, journal first, never
    re-judged (Serve.lean:137-138, 151-152; `step_journaled`, Proofs/Serve.lean:186-192).
  - If a crash lands before the fsync, the frame is torn (truncated) or whole (committed), and the
    client was told `uncertain`, so it looks up.
  - Past `journalForgets` the Host answers `uncertain forgotten`, never a re-judged `refused`
    (Serve.lean:140, 157).
  - So the writer honours `submit_at_most_once`. The one mis-classed answer on that path is
    `refused stopped` (F1).
- **The deployed codec premise.** `eq_callBytes_of_decodeCall` is PROVED for every `program`
  (READ Codec/Proofs/Deployed.lean:39-41, from Codec/Proofs/Kernel.lean:373-380, `Lawful` of the
  deployed digest codec). `deployed_canonical` (Refine.lean:441-443) consumes it at `Host.Deployed.X`.
  No axiom, no hypothesis. MEASURED grep: there are no `native_decide`, `sorry`, `partial def`,
  `unsafe` or `axiom` in Host. The only FFI is file.c and sock.c behind `opaque` handles.
- **Host/Allowance and callsOf twins.** There is no `Host/Allowance*` file at f9657bd (MEASURED
  `ls`). The only `callsOf` in Host is `Host.Check.callsOf` (Check.lean:98-103). It decodes each
  committed Turn's `event` back to its call for `use=`, a different function from
  `Lang.callsOf` (Lang/Call.lean:201, a method result's call slots). They share a name, not a fact;
  no twin.
- **Rust-side decisions Host delegates (law 2).**
  - Host trusts the supervisor to FRAME (Wire.lean:8-9) and stops by name on a bad length.
  - The op and status bytes and the bounds come from the generated table (client/src/mux.rs:301,
    361, 424 read `limits.frame.frame_bytes_max`).
  - `wrongSocket` is decided in Lean (Serve.lean:190-191, Follow.lean:82).
  - The client's `hint` (run.rs:117-129) classifies a reply by status byte alone. It decides
    nothing beyond the table, which is why F1's wrong status byte reaches the member unfiltered.

---

## Files not read (sizes in lines)

Statements or headers only:
- Proofs/Deployed 1068: header, theorem list, `recorder_encode_size_le`.
- Proofs/Coherence 933: header.
- Proofs/StoreIndex 855: header.
- Proofs/Base 845: not opened.
- Proofs/Backup 776: header and `openWith_backup`.
- Proofs/Page 685: grep only.
- Proofs/Index 589: header.
- Proofs/Seal 438: header.
- Proofs/Log 320: not opened.
- Proofs/Cli 230: statements.
- Proofs/Loop 209: statements.
- Proofs/Batch 135: statements.
- Proofs/Open 73: statements.
- Proofs/Tail 66: statements.
- Exit 285: lines 1-80.
- Carry 175: lines 1-60.
- Sim/File 1196: lines 1-90.
- Sim/Run 1616: lines 1-60, greps.

Not opened:
- Proofs: Physical 225, Genesis 207, Carry 205, Segs 187, Size 172, Names 112, SpentCheckpoint 76,
  Exit 53, Check 47, Join 35.
- Sim: Files 90, Toy 87, Join 71, Sock 46, Main 11, FileMain 3, SockMain 3.
- Sock 45, Main 3, Host/c/sock.c.
