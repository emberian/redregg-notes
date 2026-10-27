host: the fuel restart reopens in process and drops no frame (D4); the resident is never silent (D8 startup half)

What. `serve` takes no carried frame any more: a frame that does not fit a batch goes back into
the port (`Port.unread`), so the loop holds nothing between batches. `Host.restarts` is the
resident's one fuel-and-restart loop. On `fuel` it reopens the Store IN PROCESS through
`Host.reopenAt` (the one openAt, with a fresh read handle; the locked append handle stays the
lock), asserts the reopened (height, chain, position, tag, index length) equal what the loop
held, and serves the next round on the same port. `fuelBatches` 2^24 -> 2^12.

Why. `| 0, r, _ => finish .fuel r` discarded the carried frame, and exit 4 killed the process,
taking every queued frame and every client connection with it. The reader's budget was frames,
and it reported `eof` when spent (a silent exit 0 after 2^24 frames). Under the macOS floor
without hw.ncpu the reader ran inline and serve answered nothing, rc 0.

Theorem. Host.Proofs.Loop.drainM_conserves: over a list model of the port,
batch ++ port' = first :: port, with a non-empty batch of at most max 1 batchMax frames (the
batch cut drops, duplicates and reorders nothing). Second-read by OPS (law 6).

Refuses, by name. Exit.reopenFailed (NAME) and Exit.reopenDiverged (fatal); Exit.lifetime
(restartsMax, unreachable before the reader's 2^48-frame lifetime); Exit.stream (Stop:
truncated | badLength | lifetime | readFailed), where it was `eof`; `refused noThreads` at
startup (measured under PERF's floor profile: rc 2, where HEAD hung); FrameRefusal.stopped
answers every still-queued frame at a process-ending exit. STATUS lines on stderr at open and
at exit.

Plants (host-sim seeds 1-3 ALL PASS; host-file-sim 1-3 ALL PASS through the real reopenAt in
rounds of 5):
  PASS fuel restarts: 31 in-process reopens, one reply per request, the same replies in the same order as without restarts, the same chain
  PASS plant-drop-unread: a port that drops a put-back frame loses replies (173 of 200), so the check above can see a dropped frame
  PASS plant-reopen-diverged: a reopen missing the last synced byte stops the resident `reopenDiverged`
WASTE (seed 1): submit bytes-per-turn 1.354, fsyncs-per-batch 1.000, open bytes-read-per-record
1.006, seal bytes-per-appended-byte 1.708.

Flag day. Exit code 4 (fuel) is no longer emitted by `host`. New statuses in OPS's table:
reopenFailed 38, reopenDiverged 39, noThreads 42 (fatal); lifetime 40, stream 41 (restart).
`Host.Follow.loop` takes its download state as an IO.Ref (it survives a round).
Port gains `unread` and `close`: every Port value must supply them (Protocol/Rows/Writer.lean
now uses `channelPort`).
D9 (same commit; the temp-file ban refuses the file this commit touches): `host-file-sim SEED
[DIR]` (default .lake/host-file-sim) makes a fresh DIR/run-SEED-N, refuses to reuse one, and
removes only that directory. IO.FS.withTempDir is gone from Host. Its second writer run goes
through the deployed channelPort with byte-cut batches.

Decision: HOST-19 in decisions/host.md.

SIZE: Lean modules: Host/Proofs/Loop.lean, the conservation theorem (a proof module, by C3)
SIZE: Lean proof-modules: the same file
SIZE: Lean lines (Host): Host.restarts, reopenAt, the stdio resident (threadsLive, STATUS, refuseQueued), named exits, the D4 plants
SIZE: Lean lines (deployed): the restart loop, the never-silent startup and exit, Port.unread/close, five exit statuses
SIZE: Lean lines (tooling: Sim, Rows, Journey, Census, Emit): the sim's in-process reopen, the D4 plants, the file-sim directory argument
SIZE: max dependents of a non-foundation module: Host.Proofs.Loop imports Host.Loop
SIZE: theorems: go_full, go_empty, go_over, go_take, drainM_go_conserves, drainM_conserves

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
