# HOST-LOG — BUILD-HOST continuation (written by BUILD-HOST, 2026-10-16, at ~350K tokens)

Repo `~/dev/nanodregg`, main only. Commit ONLY with `scripts/commit -F MSG [--cross-layer R] PATH...`;
subject prefix `host:`; a SIZE rise needs `SIZE: <metric>: <why>` lines. Decisions go in
`decisions/host.md` (DECISIONS.md is frozen; HOST-1..7 + LAW-4 live there). Never the shared index.

## Landed (all pre-push GREEN)
- 07288a2 Host/DESIGN.md, proposals/host.md, HOST-1..7, LAW-4 argument.
- a17339d / 424e919 Host/Log.lean + Host/Proofs/Log.lean (recover_encodeAll, recover_torn, encodeAll_recover);
  HOST-4a/7a/8/9/10 moved to decisions/host.md.
- f8f078f Host/Batch.lean + Proofs (run_append, staged_foldlM, replies_size); HOST-11 (log/read grant gating).
- 020ee52 Host/Wire.lean, Host/Loop.lean (`serve`, fuel+restart, group commit, uncertain on failed sync),
  Host/Sim/{MemStore,Toy,Run}.lean; HOST-12 (forward-scan torn/corrupt; NoFrameInside premise).
- d5cb893 Host/c/file.c + Host/File.lean (nine POSIX calls, F_FULLFSYNC fails rather than weakens),
  gates/native-allow.tsv row Host.File; HOST-13.

## Exact commands

Build (from the tree, Mac):

    cd ~/dev/nanodregg && lake build Host

Commit (the only way; builds main + your paths, regenerates SIZE.md, CAS-lands):

    cd ~/dev/nanodregg && scripts/commit -F MSGFILE PATH...      # subject `host: …`, `SIZE: <metric>: <why>` per rise

Simulation, today (no `main` may live in a lib module until GATES's exe-root census rule lands).
Write this driver OUTSIDE the tree (e.g. in your scratchpad as SimMain.lean):

    import Host.Sim.Run
    def main (args : List String) : IO UInt32 := Nanodregg.Host.Sim.run args

then

    cd ~/dev/nanodregg && for s in 1 2 3 4 5; do lake env lean --run /ABS/PATH/SimMain.lean $s | tail -1; done   # expect ALL PASS ×5

Simulation, once GATES lands the rule: `Host/Sim/Main.lean` holds only that `main`, lakefile has
`[[lean_exe]] name = "host-sim"` / `root = "Host.Sim.Main"`, and

    cd ~/dev/nanodregg && lake exe host-sim 1 && lake exe host-sim 2 && lake exe host-sim 3   # exit 0 + "ALL PASS"; a failure prints "FAIL <check>"

(GATES may add Main.lean itself; standing.sh's sim verdict is that exit code.)

C shim smoke test, out of tree (until GATES's lakefile.lean + extern_lib for Host/c lands). In an
empty scratch directory D: copy `~/dev/nanodregg/lean-toolchain`, then write `D/lakefile.lean`:

    import Lake
    open Lake DSL System
    package ffitest where
      srcDir := "/Users/ember/dev/nanodregg"
    lean_lib Host where
      globs := #[.submodules `Host]
    lean_lib Kernel where
      globs := #[.submodules `Kernel]
    lean_lib Protocol where
      globs := #[.submodules `Protocol]
    lean_lib FfiTest where
      srcDir := "D/T"            -- ABSOLUTE path to D/T
      roots := #[`FfiMain]
    target fileo pkg : FilePath := do
      let o := pkg.buildDir / "file.o"
      let srcJob ← inputTextFile "/Users/ember/dev/nanodregg/Host/c/file.c"
      buildO o srcJob #["-I", (← getLeanIncludeDir).toString, "-fPIC", "-Wall", "-Wextra", "-Werror"] #[] "cc"
    extern_lib ndfile pkg := do
      let o ← fetch <| pkg.target ``fileo
      buildStaticLib (pkg.staticLibDir / nameToStaticLib "ndfile") #[o]
    lean_exe ffitest where
      srcDir := "D/T"            -- ABSOLUTE path to D/T
      root := `FfiMain

and `D/T/FfiMain.lean`: import Host.File; open a fresh `seg.log` in a data dir under D with `.append`,
`tryLock`, `writeAll "hello "`, `writeAll "world"`, `sync`; reopen `.read`; check `size = 11`,
`readAt 6 5 = "world"`, a second handle's `tryLock = false`, `truncate 5` → `size = 5`, `syncDir`,
and `File.open p .createNew` throws. Then `cd D && lake build ffitest && .lake/build/bin/ffitest`
(exit 0; it printed `lock=true size=11 readAt=world secondLock=false truncated=5 createNewRefused=true`
on 2026-10-16). Syntax-only check without Lake:
`cc -std=c11 -Wall -Wextra -Werror -fsyntax-only -I$(lean --print-prefix)/include Host/c/file.c`.

## Open / next (in order)
1. When GATES lands lakefile.lean + extern_lib for Host/c and the exe-root census rule: add
   `Host/Sim/Main.lean` + host-sim exe; then `Host/Main.lean` exe `host` with verbs serve/follow/genesis.
2. `Host/Open.lean`: open = LOCK flock → newest valid base → delta records → batch records fold
   (World.admit) → truncate torn tail (File.truncate) or refuse corrupt; follower mode never truncates.
   Generic over CODEC's record decoder until CODEC lands Turn/batch/delta codecs (HOST-10).
3. `host follow` = same fold + KERNEL's Receive.rederive / Receive.audit; `log`/`read` gated by
   Receive.mayFollow (HOST-11).
4. Replace Host.Log.le32/ofLe32 (HOST-5 twin; Kernel.le32 is a third) with CODEC's u32le.
5. Measure a BAR-sized whole-World encode vs one fsync; if cheaper, re-argue K1/HOST-10 with the number.
6. Asked of KERNEL: `World.fold E w ts = .ok w' ↔ ts.foldlM (World.admit E) w = .ok w'` (carries
   staged_foldlM to World.fold); `absent_final` (HOST-8).

## Open decisions (decisions/host.md)
- **HOST-10 deltas**: base + delta records in the one framed log; PENDING CODEC's delta/base/Turn/batch
  encodings and KERNEL's `Delta.apply (w) (Delta.of w w') = w'`. Nothing of it is built.
- **K1 measurement**: encode a BAR-sized World (1000 records) once the World codec exists; if one encode
  in a Task is under one fsync, re-argue K1 (whole-World seal at cadence `max(sealMin, worldBytes/4)`)
  with the number. HOST-10's meta-critique states this test.
- **le32 twin (HOST-5)**: `Host.Log.le32`/`ofLe32` and `Kernel.le32` (Kernel/World.lean:84) both
  wait for CODEC's u32le; delete both then (Host/Proofs/Log.lean's `ofLe32_le32`/`le32_ofLe32` can move
  to CODEC). BUILD-CODEC was not reachable by name from this agent; route through ROOT.
- HOST-8 (`absent_final` asked of KERNEL), HOST-11 (`grantOf`/`mayFollow` name), HOST-12 (forward
  scan; the last-frame case stays undecidable by design), HOST-7a (thin consent: Ember's product call).
- Rulings pending at GATES: exe roots hold only `main` + census skips them; lakefile.lean + extern_lib
  for Host/c (every extern counted by the `native` SIZE metric; gates/native-allow.tsv row Host.File).

## HOST-2 (successor of BUILD-HOST; written 2026-10-16 at ~285K tokens)

Work ONLY in `~/dev/nanodregg-wt/host` (detached worktree; ROOT's rule after the shared-checkout
collisions). `scripts/commit -F MSG PATH...` from there lands on main by CAS and moves the worktree.
Write commit messages with a QUOTED heredoc (`<<'EOF'`): an unquoted one let zsh eat backticked
words in dbf6f04's message. Every SIZE rise needs its own `SIZE: <exact metric name>: <why>` line;
the gate names the metric (e.g. `Lean proof-modules`, `Lean lines (Host)`).

### Landed by HOST-2 (all pre-push GREEN)
- dbf6f04 HOST-5 twin deleted: Host.Log frames with `lenBytes`/`lenAt` over `Codec.Stream.u32`;
  Wire uses u32/u8 (undecodable body → `badLength`); Toy le64 = Stream.u64; recovery theorems
  re-proved over `u32_lawful` (lenAt_of_occurs/none/some). `lake exe host-sim` (Host/Sim/Main.lean).
  Sim follows KERNEL-7 (`sameTxId` answers ok with the original receipt, admits nothing).
- 9ec8b3a WASTE lines in host-sim + gates/waste.tsv rows: submit bytes-per-turn 1.448,
  submit fsyncs-per-batch 1.000, open bytes-read-per-record 1.000 (trivially 1 until the base lands).
  `read cells-touched-per-read` NOT pinned (no read served; a pinned unmeasured row is red).
- 1c1b696 HOST-14 (K1 re-argued): whole-World encode 0.18 ms @1000 records vs F_FULLFSYNC 3.9/6.4 ms.
  ACCEPTED by ROOT; HOST-10 deltas WITHDRAWN; law 5 amended (8aec65b). Bench sources (out of tree on
  purpose: a provisional World encoder would twin CODEC's): `~/dev/redregg/work/host-bench/K1.lean`
  (add a local `lean_exe «k1» where root := `Host.Bench.K1` after copying it to Host/Bench/, never
  commit), `fsync.py DIR`.
- 8da0dbf Host/Open.lean `openLog` (recover + foldRecords; refusals `corrupt offset`,
  `record index fault`; `torn` = bytes the writer truncates) + Proofs/Open.lean: foldRecords_ok,
  open_encodeAll, open_torn, open_sound. host-sim opens through it; plant-restart-at-every-cut.
- 9a6c989 Host/Serve.lean `machine X` over Kernel.Receive.Ctx: submit = decodeCall → journal
  (original receipt) → receive → admit; lookup → ok | absent; read/log `notServed`; command/resume
  `wrongSocket`; refusal payload = `repr` UTF-8 (until CODEC has a refusal codec). Proofs/Serve.lean:
  step_submit (= Receive.submit's World and staged Turn), step_journaled. Both go red if the journal
  lookup is deleted from handle.
- 7e23642 Host/Store.lean openWriter/openFollower (flock ON THE APPEND HANDLE: a separate LOCK
  handle is freed at its last use in compiled Lean, so the lock vanished mid-serve; found by
  plant-second-writer) + host-file-sim exe (real file, F_FULLFSYNC, torn-file truncation).

### Commands
    cd ~/dev/nanodregg-wt/host && lake build Host host-sim host-file-sim
    for s in 1 2 3; do lake exe host-sim $s | tail -1; .lake/build/bin/host-file-sim $s | tail -1; done   # ALL PASS ×6

### Next, in order
1. **Base + seal (HOST-14 conditions)** once CODEC lands `world : Stream (Kernel.World Digest)` +
   `world_lawful` (asked; ROOT queued it after CODEC-9 Ed25519 and `oneOf`). Base file `base-<h>.world`
   = a one-frame Host.Log segment holding the World record + the seg.log offset and tag it starts
   from; open = newest verifying base, then `openLog` from that offset (read the suffix only:
   `File.readAt off`). Conditions to land AS CODE: (1) `sealMinBytes` + the 1/4 ratio in Bounds and a
   pinned WASTE row `seal bytes-per-appended-byte`; (2) `worldBytesMax` with a named refusal + plant;
   (3) measure the base MAC when CODEC's kmac256 lands and re-read HOST-14 with it (the decision
   stays unless MAC at 10^5 records exceeds the cadence budget); (4) a theorem on the open path:
   open reads one base + ≤ one cadence (+ frameMax) of log. State the seal policy as a pure function
   the loop calls and prove its invariant.
2. **`host` exe** (`Host/Main.lean`, main only; `lean_exe «host»`): verbs `serve STORE`,
   `follow STORE`, `genesis STORE NAME (PUBKEY_HEX NEXTDIGEST_HEX)…` (CLIENT-2 was told this argv;
   STORE is the only path; CLIENT runs `.lake/build/bin/host` directly under deny-by-default
   sandbox-exec, real paths only). Blocked on the deployed `Kernel.Receive.Ctx`: CODEC's call codec,
   hash, and CODEC-9 Ed25519 verify (ROOT assigned). serve = openWriter + `serve (machine X) …`
   over `channelPort` (Loop.pump on stdin) + fileStore; exit codes: 0 eof, 3 uncertain, 4 fuel.
   The batch Recorder for the deployed Host = CODEC's batch record ((array Turn) × chain-after);
   open's `step` must CHECK the stated chain (a pair assertion, law 4).
3. **`host follow`** = openFollower (same openLog) + Kernel's `Receive.audit` as the fold step (the
   follower trusts no writer decision: audit re-derives every Turn), serving PROTOCOL's
   command/resume steps; `mayFollow` gating of log/read waits on PROTOCOL-2's signed read envelope
   (HOST-11; ROOT routed it to PROTOCOL). Pages for `log`: in-memory height → offset index.
4. CLIENT round trip: once 2 and 3 exist, the first follow command is the data-object write
   (host-read → sign → submit → done).
5. Debts: HOST-8 `absent_final` (asked of KERNEL, unanswered); the torn-tail forward scan's
   worst case hashes up to frameMax candidate frames of ≤ recordMax bytes each (failure path only,
   unmeasured; pin it as a WASTE row when a base exists); `segmentBytesMax` (1 GiB) is a stand-in
   until the base bounds the read.

### People
CODEC = `aca5ce91ec8e30814` (SendMessage by that id); GATES = `ab554f1302ac0f14d`;
CLIENT-2 = `a1612c507f0ff2b93`; ROOT = `main`. KERNEL has no reachable id from here: route via ROOT.

### HOST-2 addendum (after the handoff)
- CODEC landed `Codec.Hash` (17c0307). The Sealer is
  `tag b := (Hash.mac key "nanodregg/host/seal/v1" b).bytes`, `tag_size := fun b => (Hash.mac key _ b).size_eq`.
  `Hash.digest` is cSHAKE256. CODEC measured KMAC at 184 MB/s, so HOST-14 condition (3) is
  re-read in decisions/host.md and the decision stands. Re-measure it on the real base file.
  The Store key's custody (where the MAC key lives, and who may read it) is a key-material
  decision: raise it with ROOT before choosing.
- CODEC's next: the World codec + `world.size` (every Stream gains `size` with `size v = (bytes v).size`),
  which is the input for `worldBytesMax`; then the batch record.
- PROTOCOL-2 (`a45ff664477fefd42`) landed the READ ENVELOPE (5f7d90f). The API is
  `Protocol.Envelope.ofBytes X payload` → `Protocol.Envelope.check X w e : Except ReadRefusal Unit`,
  whose refusals are badEnvelope / unknownKey / badSignature / expired / noFollowGrant.
  `envelopeFrame` + `envelopeFrame_lawful` live in Protocol/Frames.lean.
  - Serve `read`/`log` only on `.ok`; this replaces the `notServed` branches in Host/Serve.lean
    `handle`.
  - The log reply is `logReplyLayout` = `[.list "events"]`: each Turn's `event` after `e.start`, in
    log order, as many as fit one frame. It needs the height → (offset) index plus CODEC's batch
    record decoder.
  - Asked of PROTOCOL: add the writer's (height, chain) after the last served event, so the
    follower can assert its fold matches (a pair assertion against omitted events).
  - Refusal payload convention (PROTOCOL's): the constructor NAME only, in UTF-8. Serve's `named`
    currently sends `repr`, so change it. That needs a total `name` function for each refusal type;
    I asked PROTOCOL how it renders ReadRefusal.
- PROTOCOL's audit row needs the name of the refusal for a corrupted segment. I answered
  `OpenFault.corrupt offset`, not their `frameMac`. Their row wants a height: consider adding
  `records : Nat` (frames verified before the bad bytes) to `OpenFault.corrupt`. A flipped byte in a
  SERVED event is PROTOCOL's eventMismatch, not ours.

## HOST-3 (successor of HOST-2; written 2026-10-16)

Worktree `~/dev/nanodregg-wt/host`; `git checkout -q --detach main` before work (a stray modified
`gates/__pycache__/*.pyc` blocks checkout: `git checkout -- <it>`). Commit with
`scripts/commit -F MSG [--cross-layer R] PATH...`. Messages go in the session scratchpad. Each
SIZE rise needs `SIZE: <exact metric>: <why>`; the gate names the metric. Lean `seal` is a keyword.
C3 forbids Prop defs in def-modules, so gates are Bools `= true`. Elaboration errors inside a
`first | …` alternative are not caught: destructure fully instead.

### Landed (all pre-push GREEN; host-sim + host-file-sim seeds 1-3 ALL PASS; rows: every non-PENDING PASS)
- 3fb65d5 + 1e43a54 **the base (HOST-14 landed)**:
  - STORE = key, seg.log, base.world (+ base.tmp).
  - `Host.Cadence` (Bounds.lean); `cadence = max(sealMin, base/4)`; `tailMax = 2·cadence + frameMax`
    (ROOT ACCEPTED "two cadences").
  - Loop seals in a Task; `Loop.makeRoom` waits or seals inline; `commitBatch` takes
    `withinTail … = true` as a proof.
  - `openWith` is THE open, generic in its monad; theorem `openWith_reads` over a recording reader.
  - Record.lean: CODEC's batch codec with a chain assertion.
  - Keys.lean: KMAC under STORE/key (HOST-16, ruled).
  - MAC numbers are in HOST-14. My "superlinear encode" was RETRACTED (CODEC: linear). Decode,
    ~20 ns/B, is the reopen term.
- 943cab7 **the `host` exe + `log`**:
  - Deployed.lean (CODEC Deployed ctx + LANG program) and Cli.lean (verbs); Main.lean holds only main.
  - `log`: Envelope.check in Serve.handle → `Answer.page`; the loop's `fillPages` runs after the
    fsync via Page.lean.
  - The index (one Entry per record) is carried by the base and rebuilt for the tail in open
    (HOST-17).
  - PROTOCOL-4 added `tip` (051a8cc).
- f654009 + ccec081 **`host follow STORE MEMBER GRANT`**:
  - Follow.lean: `answer X me w frame` is pure and generic in Ctx; `loop` appends absorbed Turns
    through the shared `Host.append` BEFORE replying.
  - It has its own Store, reopened with `Deployed.auditStep` (Record.step over Receive.audit).
- 483ce14 **`read` (HOST-15)**: Answer.defer (.log | .read) and ONE pager `Resident → Deferred → IO`.
  `Page.basePage` makes one pread of base.world at 4+start. `Sealed` carries height, chain and digest
  (Keys.worldDigest, unkeyed, once per base). Host.Sim.memBasePage serves PROTOCOL's rows.
- 7ad9053 **law 7**: Proofs/Names.lean, name_injective for every Host refusal type; Proofs/Page
  `budget_fits_event`. Genesis takes NEXT PUBLIC keys and computes nextKeyDigest (CLIENT-2).

### Commands
    cd ~/dev/nanodregg-wt/host && lake build host host-sim host-file-sim rows
    for s in 1 2 3; do .lake/build/bin/host-sim $s | tail -1; .lake/build/bin/host-file-sim $s | tail -1; done
    .lake/build/bin/rows | grep ^ROW
    host genesis D NAME KEY NEXTPUB  # prints founder member/grant; host serve D; host follow F MEMBER GRANT
    base bench (out of tree): ~/dev/redregg/work/host-bench/Base.lean (copy to Host/Bench + local lean_exe; never commit)

### Next, in order
1. CLIENT-2's real round trip is GREEN at a1bd695: create, write, read, refused expect, rotate,
   write, read against `host serve` + `host follow`, confined, in 0.5 s. The sandbox needed
   sysctl hw.ncpu (without it, `IO.asTask .dedicated` runs inline and the pump blocks). Open,
   routed to KERNEL: the genesis chain commits only to NAME, not to the founders. KERNEL-3 agreed
   and relayed it via ROOT to its successor. The fix: the chain hashes name ‖ the founder pieces,
   with a `genesis_binds` theorem and a plant. A re-genesis follows; HOST needs no change. Follow
   up with the CURRENT KERNEL owner (ask ROOT for the id), not ac54dee13ae098eaf.
2. `read` is served (483ce14). PROTOCOL-4 (a987d514b07b38010) lands the thin row and Thin.Page.toBytes;
   swap readReplyFrame.bytes for it if they ask. PROTOCOL-4 is also changing
   Follow's state to `Follow D` (a download in memory), and it may edit Host/Follow.lean itself.
   When a thin base is adopted, follow must seal its own base from it (`Host.adopt`, if they ask).
3. Plant owed: a forged Turn in a follower's own segment refused at reopen by the audit
   (PROTOCOL-4 lands it in the rows on the generic `answer`).
4. Unproved, stated in Proofs/Base: makeRoom's inline seal leaves the base at the loop's
   position. That is IO; the loop's branch after it is a named stop.
5. Debts: HOST-8 `absent_final` (KERNEL); the torn-tail forward scan's worst case is unmeasured.
   HOST-17's critique: the index is re-encoded whole every seal (WASTE seal 1.715 at toy scale).
6. Measure the real cold reopen of `host serve` at 10^5 records once the client can write many.
   CODEC offers a proven-equal fast World decode: ask aca5ce91ec8e30814 if reopen binds.

### People
CODEC aca5ce91ec8e30814 · PROTOCOL-4 a987d514b07b38010 (PROTOCOL-3 aed76cbdc2d5d6b3a retired) ·
CLIENT-2 a1612c507f0ff2b93 · ROOT main.

### HOST-3 addendum: stopped, another agent is live in the host worktree
- Another agent landed 9f2373e ("one genesis image": an ORIGIN frame, D4/BUILD-TRANSPORT) and holds
  uncommitted edits in ~/dev/nanodregg-wt/host. HOST-3 stopped editing. The open asks for the
  current owner:
  (1) PROTOCOL-4: `lookup` of a non-journaled call with w.height > validUntil answers `refused
      expired` (backed by KERNEL `absent_final`).
  (2) Refuse a follower's `adopt` unless its Store is at genesis (`notAtGenesis`), measured against
      the genesis image's end, not 0. PROTOCOL-4 landed adopt at a02b35c without that check.

## HOST-4 (successor of HOST-3; written 2026-10-17 at the context ceiling, under ROOT's Mac build stop)

### State: D4 + D9 + never-silent are WRITTEN, NOT LANDED
- The whole diff is in `~/dev/redregg/work/HOST-4-D4.patch` (against main 28de15e), with its commit
  message in `~/dev/redregg/work/HOST-4-D4.msg` (SIZE lines included). The same edits sit
  uncommitted in `~/dev/nanodregg-wt/host`.
- A first version built GREEN on 9f2373e: host-sim and host-file-sim seeds 1–3 ALL PASS, every row
  PASS/PENDING, PRE-PUSH GREEN. The CAS lost to OPS's 28de15e, and the run was refused for paths behind main.
- Since then, and NOT YET COMPILED (the build stop): the rebase onto 28de15e (Cli conflicts resolved
  by hand; `serving`/refuseStore kept), the five new statuses in Host/Exit.lean, the extended rcases in
  Proofs/Exit `name_of_status`, Follow.loop's download as an `IO.Ref`, drainM_conserves' size
  conjunct (with go_full/go_empty/go_over/go_take split out), host-sim's named `requests = replies at
  every fuel return`, and file-sim's run through the deployed `channelPort`.
- **First thing on hbox:** `git apply -3` the patch on current main (or reuse the worktree), then
  `lake build host host-sim host-file-sim rows`, fix whatever the blind edits broke (most likely spots:
  the Proofs/Exit rcases pattern, the `change` steps in Proofs/Loop, and the nested-do `s!` in Sim/Run's
  reopen), run sims 1–3 and rows, then `scripts/commit -F HOST-4-D4.msg --cross-layer "<PROTOCOL Writer.lean
  uses channelPort>" <paths from the patch>`.
- Decision HOST-19 is written (in the patch): carry deleted (Port.unread), `Host.restarts` reopens in
  process with the `agrees` pair assertion, fuelBatches 2^12, lifetimeFrames 2^48, `threadsLive`
  (measured: `refused noThreads` rc 2 under PERF's floor, where HEAD hung), STATUS at open/exit,
  `refused stopped` for queued frames at exit. Its critique: a ~5 s stall per 4096 batches at
  worldBytesMax, and the reader-in-hand frame residue.

### Agreed with others (act on these)
- OPS (aaae7695f4b65107d): D5/D6 on main (28de15e). I did the law-6 read of their statements
  (fine; verdict_none_iff ≈ a restatement, so their plant table is the evidence). OPS read D4
  (non-vacuous) and asked for three things, all now in the patch. Owed: OPS's origin-prefix finding.
  The bytes before base.offset are never read by an open, so a flipped origin byte opens clean. The
  follower's first audit must refuse `corrupt history` (mirror `Check.historyClean`), with a host-sim
  plant: flip a byte at originSize/2.
- CODEC-2 (a5db8dcb963c5d57d): D2 = ONE stamp at the head of the base record:
  `Hash.digest "nanodregg/host/shapes/v1" (Tag.of "host/world" world ‖ Tag.of "host/batch" record ‖ Tag.of
  "host/base" baseCodec)`. Hold it as a closed `def` in Deployed, never a hex literal. Base.read compares
  it before decoding and refuses `shapeMismatch (stored running)`. worldStart moves 4 → 36 (Page.basePage
  and HOST-15 depend on it). State the premise "no segment is read without its base". Cite
  `Codec.Proofs.Tag.Tag.of_eq`. Not started. It must land BEFORE KERNEL-23's flag day.
- KERNEL-4 (a18c18cfac4f4a41e; KERNEL-5 builds it): KERNEL-24 = `World.genesis E name nonce allowance
  founders`, `World.origin : D`, origin = H(domOrigin, name‖nonce‖allowance‖founders), chain₀ =
  H(domGenesis, origin), founder ids keyed by origin, `Unsigned.world` checked FIRST → `wrongWorld`.
  No Host refusal. HOST's part, when it lands: `host genesis` draws the nonce from IO.getRandomBytes 32
  (refuse `entropy`), takes `--nonce HEX` to reproduce a writer's genesis for a follower's own Store
  (TRANSPORT's ask), and prints `origin <hex>` and `nonce <hex>` lines (TRANSPORT a4652a8aa8280fcef
  consumes `origin`; there is NO serve-side origin output, which would be TOFU). The flag day:
  re-genesis.
- TRANSPORT landed the genesis image / origin frame (9f2373e). Its commit 2 (foreignSegment,
  HOST-18) waits on PROTOCOL; openWith's signature is unchanged.

### Next, in order (after the D4 landing)
1. D2 shape stamp (above).
2. ROOT's PROTOCOL-19: Envelope `expired` is checked against the WRITER's height. The fix: check expiry
   LAST, and make `expired` carry the writer's height, so the member re-signs with a bounded, named retry.
   Host-sim plant: a follower cold-starting two windows behind reaches the tip. Do it with PROTOCOL-5.
3. `lookup` of an un-journaled call with w.height > validUntil answers `refused expired`, backed by
   KERNEL's `absent_final` (HOST-8), never by a Host assumption.
4. `.adopt` refuses unless follow's own Store is at genesis (`notAtGenesis`; HOST-3's review, law 1).
5. PERF via ROOT: a WASTE row `open verifies-per-open`, and a Bound on the follower's unsealed tail in
   TURNS (the worst case: ~90k verifies ≈ 36 s at tailMax), with `openWith_reads` gaining a verifies
   term. Make `recordBytesMax` derive from the real cap (events ≤ 64 KB ⇒ ~8.2 MB), or delete it.
6. KERNEL-24 genesis (above), then KERNEL-23 absorption (cell root: base seal/open/pages) when
   KERNEL-5 and CODEC-2 report.
7. D8's rest: STATUS at each seal (the Loop needs a log hook), Tally. HOST-14 re-read at size. The owed
   forged-Turn-in-follower-segment plant.
8. drainM_conserves' bytes bound (OPS asked: the frames after the first stay within batchBytesMax),
   left out because it was written blind.

### Laws
- No law looks wrong. Law 4's "one unbounded loop" can't be written as unbounded without `partial`
  (the gate refuses it tree-wide, and `repeat` is core's partial), so `restarts` is bounded by
  `restartsMax`, which the reader's lifetime reaches first. The charter should say that this nested
  bound IS the sanctioned shape.
- ROOT BLESSED the nested bound (10-17) and is rewording law 4 to cite HOST-19. The restated law asks
  for "the theorem that exhausting it exits by name": HOST-5 adds it in Host/Proofs/Loop.lean when
  landing the patch, as `restarts_spent : restarts round reopen mark 0 r = pure (.lifetime, r)`, and
  says in HOST-19 that it is the exhaustion case (named `lifetime`, class restart, never silent).
- TRANSPORT (a4652a8aa8280fcef), 10-17: HOST-18 landed 99b5cbc (Status.foreignSegment 29, fatal). It asks for a
  connection HANG-UP on the child wire: a 4-byte body (`u32 conn`, no op) for nd-attach (CLIENT-12 B).
  My answer: yes, as a decoded `HangUp conn` constructor, not a reserved op. A hang-up never drops that
  conn's already-queued frames, only deferred pages after it. Host-sim plant: a hang-up mid-batch
  changes no other conn's reply. TRANSPORT writes it under `host:` with HOST-5's review, on top of D4.
  Also owed: the Loop-level theorem "every request frame gets exactly one reply with its own conn,
  `uncertain` included" (the mux's in-flight counter relies on it; host-sim checks it per fuel return).

## HOST-5 (successor of HOST-4; written 2026-10-17 at ~380K tokens)

Everything is on hbox: `ssh hbox`, worktree `/tank/dregg-build/nanodregg/wt/host`. Run
`git checkout -q --detach main` before editing. Land with `scripts/commit -F MSG [--cross-layer R] PATHS`.
Write message and decision text on the MAC under the session scratchpad and `scp` it to
`/tank/dregg-build/nanodregg/logs/host-*`. Remote heredocs through `ssh '…'` broke three times on
apostrophes. Keep long jobs under nohup with a PID file in logs/, and foreground-wait with a deadline loop.
The SIZE gate names its metric exactly (`Lean lines (tooling: Sim, Rows, Journey, Census, Emit, Ops)`,
`max dependents of a non-foundation module`, `Lean modules in the Host closure`). A WASTE ceiling
raise or row removal needs a `WASTE: <op>: <why>` line.

### Landed by HOST-5 (all PRE-PUSH GREEN; host-sim + host-file-sim 1–3 ALL PASS; rows PASS/PENDING)
- 808f38e **D4 + D9 + never-silent startup** (HOST-4's patch compiled, plus `restarts_spent`). HOST-19.
- ce61913 **D2 shape stamp** (HOST-20). `Base.shapeStamp` = H(Tag.of base codec ‖ Tag.of batch codec)
  lives in `Keys.shapes`, and the deployed value is `Deployed.shapes`. `Base.read` checks MAC → stamp
  → decode. A mismatch is `shapeMismatch` (exit 43). worldStart = 36. Theorems: read_stamped,
  read_shapeMismatch. Plant: plant-old-shape.
- 0689975 **lookup `refused expired`** (HOST-21). `FrameRefusal.expired`; handle_lookup_expired and
  lookup_expired_final come from KERNEL absent_final. Plant: plant-lookup-expired, which runs over
  the kernel-sim Ctx. Adopt notAtGenesis was already PROTOCOL's; HOST-21 says why there is no twin.
- 5582991 the turn cadence (HOST-22). SUPERSEDED by 7797070.
- c722b05 **Host.Tail** for HOSTING's controller (HOST-23). Tail.open/next/await/absorb,
  Record.stepTurns, Deployed.tailStep, Bounds.tailPollMs. Theorems: absorb_encodeAll,
  absorbRecords_ok. Plant: plant-tail. HOSTING has the signatures.
- 648c3a4 **D8 seal half** (HOST-24): a `STATUS seal …` line per seal. The Tally is NOT built.
- 7797070 **ROOT ruling on HOST-22 (a)**. The follower reopens with World.fold (foldStep).
  Deployed.auditStep is deleted, and so are sealTurns/tailTurnsMax/tailTooManyTurns (exit 44
  retired) and the verifies WASTE row. The seal WASTE row was re-pinned to 1.720 in 5582991: D2's
  stamp is the cause, not LEDGER. HOST-22's amendment records the ruling, and the follow-time tooth
  is the rows' audit/followVerifyAll.
- 59486b4 **drainM_bytes** (OPS's ask): batch payload ≤ max first batchBytesMax.

### In flight with others (act when they report)
- **PROTOCOL-5 (a4cd717157c6d458e)** lands `Protocol.Command.step_persists_admitted` +
  `absorb_admits`/`absorbPage_admits`. The absorb proofs are mine, at
  logs/host-ProofsFollow-for-protocol.lean. This is ROOT's condition 2 for 7797070. When it lands,
  check that the names match Host/Follow.lean's doc (it cites `Protocol.Command.step_persists_admitted`),
  then tell ROOT the condition is met.
- **KERNEL-5 (aaf0617c549722c7a)** builds KERNEL-24 as one cross-layer commit, including the Host/Cli
  genesis change I specified: IO.getRandomBytes 32, refusing `entropy`; `--nonce HEX`; print `origin`/`nonce`;
  no serve-side origin. Sim genesis gets a fixed nonce. The D2 stamp flips automatically. After it
  lands: (a) review the Cli change, which is mine now; (b) item 6 below.
- **TRANSPORT (a4652a8aa8280fcef)**: the hang-up (step_hangup, plus my ask: step_hangup_bad) and
  the reply-conn theorems (served_conns, uncertain_conns, applyPages). Both passed my law-6 read, and
  they land them under `host:`.

### Next, in order
1. **Origin prefix (OPS's `corrupt history`)**, once KERNEL-24 lands. At open, read the ORIGIN frame
   (bounded: ≤ Log.frameMax chainBytesMax at offset 0), verify its MAC from segmentInitial, and require
   its record = the genesis chain H(domGenesis, base.world.origin). That binds the base's World to the
   Store's own origin in O(1). It changes `openWith_reads` (two ranges). Plant: flip a byte at
   originSize/2, and a base from another origin. `host check`'s historyClean stays O(segment) for
   backups.
2. **KERNEL-23 absorption** (cell root: base seal/open/pages) when KERNEL-5 + CODEC-2 report.
3. HOST-14 re-read at size. Measure the real cold reopen at 10^5 records once the client can write
   many (PERF).
4. HOST-3's owed "forged Turn in a follower's own segment refused at reopen" is MOOT under the
   ruling: a MAC-valid forged tail is accepted, exactly as a MAC-valid forged base already was.
   Don't build it.
5. Standing at f548ab5 was RED on `ROW grain FAIL line 4: got refused program`. That is not host's
   (it appeared after HOSTING 6577e82 and PROTOCOL 92c0ad9); ROOT has been told.

### Laws
No law looks wrong. Observation: law 6's "every statement read by a second agent" worked here as
a two-way trade (OPS↔HOST, TRANSPORT↔HOST). The cheap form is a law-6 line in the lander's
message naming the reader.

### People
ROOT main · KERNEL-5 aaf0617c549722c7a · CODEC-2 a5db8dcb963c5d57d · PROTOCOL-5 a4cd717157c6d458e ·
TRANSPORT a4652a8aa8280fcef · HOSTING a665735e10cfc4da6 · OPS aaae7695f4b65107d.

### HOST-5 addendum (OPS-2 a493aca8608fbc234, after the handoff)
- `Ops.Units.hostAction : Status → String` (c835c6d) is exhaustive. Any HOST commit that adds or removes
  a `Status` constructor (or changes a class) must, in the SAME commit, add the arm
  (`--cross-layer "Ops/Units.lean: hostAction arm for <status>"`, plus one operator sentence) and re-render
  `.lake/build/bin/emit-units deploy/units`. OPS-2 pre-agreed this. Check that main's hostAction has no
  arm for the retired `tailTooManyTurns` (44, removed in 7797070).
- Fix Host/Exit.lean's doc: codes 1 and 2 stay reserved, but because Lean's runtime exits 1 on an uncaught
  exception (and 2 is the usage convention), not because of nd-supervise. nd-supervise now exits 64/65/66
  (Protocol.Exit).

## HOST-6 (successor of HOST-5; started 2026-10-17 ~13:00Z)

Same recipe as HOST-5 (hbox wt/host, `git checkout -q --detach main`, text written on the Mac
scratchpad then scp'd to logs/host-*, scripts/commit -F).

### Landed
- 51515fa **HOST-25 designed** (decisions/host.md only): open binds the origin frame to the base's
  World. One bounded read `[0, min (frameMax chainBytesMax) offset)` after the foreignSegment
  check; frame at 0 must verify from segmentInitial (else `.log (.corrupt 0)`, with openLog's
  corrupt offset made ABSOLUTE in the same commit — today it is base-relative; host-sim's
  `isCorrupt … 0` plants move to origin.offset), record must = `originChain b.world` (else new
  BaseFault/Status `foreignOrigin`, code 30, fatal). openWith gains `originChain : W → ByteArray`
  (deployed = KERNEL's named genesis-chain def). Theorems: openWith_reads (two ranges),
  openWith_origin, openWith_originCorrupt, openWith_foreignOrigin, genesisImage_origin, originChain
  invariant under foldStep (from fold_origin). Plants host-sim: plant-origin-flip,
  plant-foreign-origin (needs a base past the first record, else foreignSegment fires first).

### Asked / waiting
- KERNEL-5: expose `World.genesisChain E origin` + the genesis equation; keep admit_origin/fold_origin.
  BUILD NOTHING until KERNEL-5 says KERNEL-24 is on main; then review its Host/Cli genesis change.
- OPS-2 (a493aca8608fbc234, successor of BUILD-OPS): any new/removed Status needs an
  `Ops.Units.hostAction` arm + `.lake/build/bin/emit-units deploy/units` in the SAME commit,
  `--cross-layer "Ops/Units.lean + deploy/units: hostAction arm for <status>"` (pre-agreed). Asked
  them for a `serve`-path origin flip plant and a foreign-origin store-plant. Fix Host/Exit.lean's
  stale "never 1 or 2" doc (nd-supervise exits are 64/65/66 now) in the HOST-25 build commit.
- PROTOCOL-5: step_persists_admitted NOT on main as of 51515fa (grep); asked for ETA / handback.
- TRANSPORT landed 229c719 (one reply per request frame) on its own.
- PROTOCOL-5 landed f939943 (step_persists_admitted + absorb_admits/absorbPage_admits, Protocol/Proofs/Command.lean);
  law-6 read done by HOST-6; ROOT told condition 2 on 7797070 is MET.
- TRANSPORT 4c327a7 (Keys.domBaseDigest) reused number HOST-25 → renumbered HOST-26 by TRANSPORT (51036b4);
  4c327a7 also LANDED CONFLICT MARKERS in decisions/host.md (green, pushed) → removed by HOST-6 in d7393b6;
  GATES-2 (aedb775dc4517c504) asked to refuse marker lines + plant.
- GATES-2 e9d06c3: judged tree refuses conflict-marker lines by name (planted). Cause: a `git apply --3way` relay committed unresolved, not scripts/commit.
- PROTOCOL-5 RETIRED; PROTOCOL is PROTOCOL-6 abd8f012f13228e0b. Sent it HOST-25's row facts: (1) wrongWorld row's
  `.replayElsewhere` (Loopback.lean) reuses st.genesis = SAME origin after KERNEL-24 → the replay is ADMITTED → row red;
  needs a second genesis with another nonce (+ a same-nonce line expecting ok); (2) foreignOrigin is open-only,
  never on the wire; rows share Host.Sim.keys (fine unless a row splices seg bytes); reopenFlipped in [0,68) → corrupt 0;
  (3) open's corrupt offset becomes absolute; (4) asked agreement to add `originChain` at Protocol/Rows/Writer.lean's
  two openWith/memGenesis call sites, cross-layer, in the HOST-25 build commit.
- PROTOCOL-6 AGREED (4): HOST-25 commit may edit Protocol/Rows/Writer.lean's two openWith call sites (genesisStore/memGenesis,
  reopen) for originChain, --cross-layer, nothing else in Protocol. It re-cuts wrongWorld after KERNEL-24 (whole-log replay;
  line 7 other nonce → wrongWorld; line 8 same nonce → ok; plant nonceRepeats). No row expects foreignOrigin or a corrupt
  offset; reopenFlipped flips the BASE file only.
- OPS-2 AGREED: foreignOrigin 30 fatal; hostAction sentence = "the segment's origin frame verifies under this Store's key
  but names another World (two Stores share a key file, one's seg.log spliced over the other's): restore seg.log from this
  Store's own backup; never restart it". OPS-2 lands the serve-path origin flip (corrupt) + foreign-origin store-plant
  AFTER my HOST-25 build is on main: MESSAGE OPS-2 then.
- **79f5860 HOST-25 LANDED** (origin frame check; foreignOrigin 30; absolute corrupt offsets; Host.Proofs.Deployed +
  Host.Proofs.Follow new; law-6 read: none vacuous, two WEAK → discharged in Proofs/Deployed). OPS-2 lands the
  serve-path flip + foreign-origin store-plants.
- KERNEL is KERNEL-6 aa36c7021124d8bdb; it confirmed origin stays + genesisChain unchanged in the World port; chainNext
  becomes H(domChain, prev ‖ turnDigest ‖ root'); order LEDGER-2 D5a → port; it sends trie signatures to HOST+CODEC first.
- **2ba6746 HOST-27 LANDED**: SIGXFSZ ignored at startup (Host.ignoreFileSizeSignal, file.c signal()); ceilings native 9,
  C lines 156 (GATES-2 agreed). Plant = OPS-2's deploy/live LimitFSIZE unit (expect exit 3 + restart, was 153).
- **645116a HOST-28**: answer to OPS-P1 carry (one stamped file, required --digest, one genesis path, carryMismatch,
  stamped-not-stable). BUILD the verbs when KERNEL-29 (Receive.carry, in-window journal per PROTOCOL-30) + CODEC-2
  carried codec land.
- Workflow note: main moves under you constantly; `git diff > logs/x.patch; git checkout -f --detach main;
  git apply -3 patch; git reset -q; grep markers` before each scripts/commit. `emit-units --help` writes a dir named
  `--help` (it takes the arg as OUT) — don't.
- OPS-2 CONFIRMED HOST-27 live (burst5-a run 4: LimitFSIZE = fresh seg + 4096, mid-frame cross → reply uncertain,
  child exit 3, restarted, torn tail dropped; deploy/live/README.md 1d326dd). OPS-2 ACCEPTED HOST-28 as written
  (withdrew "rarer"; RUNBOOK §6 export from a stopped writer). Carry plants after my verbs + KERNEL-29 + CODEC carried.
- **HOST-29 (KERNEL-23 port, Host side) BUILT, NOT LANDED — KERNEL-7 (ac9b1fb8228590424) lands it in its kernel! commit.**
  Patch: hbox logs/host6-kernel23.patch, against main 4777611 + logs/kernel7-r4.patch (+ untracked Cells/TrieMap)
  + CODEC-2's logs/codec2-trie-r3/Codec/* (CODEC-3 a5c03e9649c328e52 owns those now). Record = List (Turn × root),
  end chain deleted; Record.runRooted checks every root (rootMismatch i); Machine.note; Kernel.Rooted/RootedFold
  (+ Kernel/Proofs/RootedFold.lean); Protocol Persist.turns pairs, follow theorems conclude RootedFold
  (PROTOCOL-6 condition); plant-flip-root (mutation red seen); WASTE submit 1.419→1.492. All exes ALL PASS on
  that tree. wt/host currently holds that whole uncommitted tree (kernel7 + codec + mine): do NOT scripts/commit
  from it; after KERNEL-7 lands, `git checkout -f --detach main`.
- PROTOCOL-6 ACCEPTED the HOST-29 statements (Rooted, RootedFold, absorb_admits, absorbPage_admits, step_persists_admitted, step_persists_folds); Protocol part may land in KERNEL-7's commit. Rows on ported tree = 14 PASS / 3 pending.
- Measured on the ported tree: rows prints 15 'ROW … PASS' lines (incl. ROW lang-journey) + pay/well/bounty PENDING, no FAIL.
- KERNEL-7 read Rooted/RootedFold/plant OK; applied my patch in wt/kernel + Hosting/Cli.lean:133 fix (tail outs now pairs → map Prod.fst; I had not built the hosting controller exe). 350/350 green. Waiting CODEC-3 review → KERNEL-7 scripts/commit → sha to me → then reset wt/host to main.
- **7c43273 KERNEL-23 port LANDED with HOST-29 inside** (KERNEL-7). Rooted/World.RootedFold moved to
  Kernel/Proofs/RootedFold.lean (gate C3 refuses Prop defs in Kernel/World.lean). wt/host reset to main.
  CODEC-3 note for future Host reopen theorems: take Canon/Slotted from Codec.Deployed.world_decode_canon /
  world_decode_slotted, never as premises (no Host theorem uses them today).
- NEXT: carry verbs (HOST-28) when KERNEL-29 + CODEC-22 land; HOST-14 re-read at size; HOST-17 index-in-base
  growth is still open.
- KERNEL-31 (genesis refuses outside GenesisFits; Host's name-size check deleted; Proofs/Deployed over genesisWorld): HOST-6 said OK to KERNEL-7, asked it to confirm GenesisRefusal.name injective. Patch logs/kernel31-final.patch; KERNEL-7 lands after D5c.
- KERNEL-7 confirmed GenesisRefusal.name_injective (Kernel/Proofs/Origin.lean); founder index not in name (Reject.name convention). KERNEL-31 review closed.
- KERNEL-7 retired after 2618fe3 (KERNEL-31 landed). KERNEL is KERNEL-8 a3757d866eb64f133; it sends KERNEL-29 sha for HOST-28 carry verbs.

## HOST-7 HANDOFF (written by HOST-6 at ~430K, 2026-10-17; ROOT spawns HOST-7 from this section)

### Recipe (unchanged; read MIGRATE-HBOX-LOG "RECIPE FOR THE LANES")
hbox worktree `/tank/dregg-build/nanodregg/wt/host`, currently detached at main (clean after the KERNEL-23 reset;
run `git checkout -q --detach main` anyway). Land only with `scripts/commit -F MSG [--cross-layer R] PATHS`.
Write text on the Mac scratchpad and scp it to `/tank/dregg-build/nanodregg/logs/host-*`; remote heredocs inside
`ssh '…'` break on apostrophes/backticks (bit HOST-6 once more): ship python patch scripts by scp and run them.
main moves constantly. Before each commit run `git diff > logs/x.patch; git checkout -f --detach main;
git apply -3 logs/x.patch; git reset -q`, then grep for `^<<<<<<<|^>>>>>>>` (gate e9d06c3 also refuses them now).
Never run `emit-units --help`: it writes a directory named `--help`. Build with `swarm-build`; long builds go
under nohup with a PID file in logs/ and a foreground deadline loop. Size gates: a raised count needs a `SIZE: <metric>: why`
line; a raised ceiling needs `SIZE-CEILING:` plus the owner's agreement (gates/ceilings.tsv = GATES); a WASTE
ceiling raise needs `WASTE: <op>: why`. A new or removed Host Status needs the `Ops.Units.hostAction` arm and
`.lake/build/bin/emit-units deploy/units` in the SAME commit (OPS agreed in advance, cross-layer).

### Landed by HOST-6 (all PRE-PUSH GREEN, pushed)
51515fa HOST-25 design · d7393b6 conflict-marker fix · **79f5860 HOST-25** (origin-frame check at every open:
`corrupt` at 0 / `foreignOrigin` exit 30; absolute corrupt offsets; Host/Proofs/Deployed + Host/Proofs/Follow) ·
**2ba6746 HOST-27** (SIGXFSZ ignored; LimitFSIZE → uncertain 3, OPS-2 confirmed live on burst5-a) ·
**645116a HOST-28** (carry design, OPS-2 accepted) · **7c43273** (KERNEL-7's port, with HOST-29 inside: records
are `List (Turn × root)`, `Record.runRooted` → `rootMismatch i`, `Machine.note`, `Kernel.Rooted`/`RootedFold` in
Kernel/Proofs/RootedFold.lean, Protocol follow theorems conclude RootedFold, plant-flip-root, WASTE submit 1.492).
Reviewed and OK'd: KERNEL-24's Cli genesis (9e91ede), KERNEL-31's Cli/Proofs-Deployed hunks (2618fe3).

### HOST-7's work, in order
1. **HOST-28 carry verbs**, when KERNEL-8 (a3757d866eb64f133) sends the KERNEL-29 sha (`World.carried`,
   `Receive.carry` with carry_carried / carry_origin_ne / carry_chain, journal-in-window per PROTOCOL-30) and
   CODEC-3 (a5c03e9649c328e52) lands CODEC-22's carried codec. Build exactly HOST-28 (decisions/host.md):
   - `host export STORE OUT` (openFollower + historyClean, read-only). It writes ONE file: stamp32 ‖ from ‖ height ‖ chain ‖
     carried bytes, and prints `carried <digest>` `from <hex>` `anchor H:C`.
   - `host import STORE NAME IN --digest HEX [--nonce HEX32]` (no `--digest` refuses `usage digest`).
     It goes through Host.genesis, then reopens with openWriter and compares the carried bytes.
   - One new fatal Status, `carryMismatch` (digest / reopen / decode on stderr); a stamp mismatch is `shapeMismatch`.
   - Theorems over the real verbs, plus a host-file-sim plant: one carried byte flipped must be refused.
   OPS-2 (a493aca8608fbc234) builds the store-plants afterwards: message it at landing. HOST-25 must hold for
   carried Stores (carry_chain = genesisChain of the carry origin).
2. **HOST-17 is a COUNT defect, not parked (ROOT 10-17).** Every seal re-encodes the WHOLE index, one Entry per
   record ever written (Base.codec's `rawList indexMax Entry.codec`). The metric is `bytes re-encoded per seal ÷
   bytes appended since the last seal`. Its index term grows with the number of batches, which you can prove from
   the index shape, with no timing. The existing WASTE row `seal bytes-per-appended-byte` measures a cousin of it.
   Build: a WASTE row for the index term that host-sim measures at several Store lengths (it must be shown
   growing), then the fix: a persistent index (only new entries written per seal), e.g. index pages appended as
   segment frames or a second append-only file with its own crash story (HOST-17 alternative (a); reargue it in
   decisions/host.md with both critiques), and re-pin the row bounded. Watch the D2 stamp (base shape change =
   re-genesis, refuse old shapes).
3. **HOST-14 at size is a COUNT re-check, not parked (ROOT 10-17).** Under store-plants' live writer (OPS-2's
   4ae6608: 48 creates of a 48 KiB slot with real 1 MiB seals), count per record: bytes written (segment +
   base), bytes read at reopen, and hashes. Then scale the count to THE BAR (1000 records) and to worldBytesMax
   from the measured per-record terms. Do not time anything. The questions: does seal bytes ÷ appended bytes stay
   ≤ 4 + floor as HOST-14 claims, and is reopen bytes ≤ one base + tailMax? Put the rows in gates/waste.tsv with
   their sources (coordinate the store-plants hook with OPS-2).
4. CODEC-3's rule: any new Host reopen theorem takes World Canon/Slotted from
   `Codec.Deployed.world_decode_canon` / `world_decode_slotted`, never as premises.

### Open edges known to HOST-6
- HOST-24's seal STATUS line has no in-process plant (seal thread stderr). OPS's live harness is its home.
- HOST-21's adopt argument rests on "follow never appends `.turns []`", which no theorem states (Follow.lean
  matches `.turns []` separately; a theorem over Follow.loop would close it).
- HOST-23's Tail does not follow segment rotation. There is no rotation today; if one is ever added, Tail must reopen.
- Law 6: HOST-6 used a spawned general-purpose vacuity reader (cheap, worked). Rate any statement it calls WEAK and
  discharge it at the deployed instance before landing.

### People (hbox logs/ROLES.txt is authoritative)
ROOT main · KERNEL-8 a3757d866eb64f133 · CODEC-3 a5c03e9649c328e52 · PROTOCOL-6 abd8f012f13228e0b ·
OPS-2 a493aca8608fbc234 · GATES-2 aedb775dc4517c504 · TRANSPORT a4652a8aa8280fcef · HOSTING a665735e10cfc4da6 (check ROLES).

## HOST-7 (successor of HOST-6; started 2026-10-17 ~22:05Z)

Recipe unchanged. Helpers on hbox: `logs/host7-rebase.sh NAME` (diff → checkout main → apply -3, fails
loudly on conflict; on a conflict resolve by hand, then `git reset -q`). host-sim builds warm in wt/host in
seconds (`swarm-build lake build host-sim`). A commit touching gates/waste.tsv needs
`CROSS-LAYER: gates/waste.tsv: …` IN THE MESSAGE and `SIZE: Lean lines (Host)` + `SIZE: Lean lines (tooling: …)`
for host-sim growth (Host/Sim counts in both).

### Landed
- **1b8ac0e** HOST-17 as a count: host-sim `indexTerm seed n` (Run.lean), rows
  `seal index-bytes-per-appended-byte-at-{100,200,400,800}` = 0.540 / 0.943 / 1.329 / 1.251 (max seeds 1–3).
  Grows while world/4 < sealMin, then PLATEAUS (unpruned journal grows the World, so the cadence too);
  deployed plateau ≤ 4·52/72 ≈ 2.9. HOST-30 PROPOSED in decisions/host.md (index.log, one page per seal,
  base names (indexOffset, indexTag), indexShort/indexCorrupt fatal, Task gets only new entries — also
  cures the shared-Array O(records) copy on push while a seal Task holds r.index).
- Asked ROOT for the HOST-30 ruling (base change) at 1b8ac0e.

### HOST-30 build plan (when ruled)
Files: Base.lean (Base: drop index, add indexOffset u64 + indexTag; genesisImage gains empty index; faults
indexShort/indexCorrupt; Base.file takes page entries + index pos, checks indexOffset+page ≤ worldBytesMax
→ indexTooLarge), Bounds.baseRecordMax (worldBytesMax + 8+32+8+32), Keys (domIndex sealer; Keys gets
`index`), Loop (Checkpoint.write gets new entries + index Position; Sealed/Pending carry index pos + count;
spawnSeal passes `r.index.extract count size`), Open.openWith (reader for index.log; recover [0,indexOffset),
chain must end at indexTag; Opening carries index pos + orphan len), Store (indexPath, genesis writes empty
index.log, openWriter truncates orphan, fileCheckpoint appends page + sync before installBase), Follow adopt
(index restarts; adopt is at genesis only, index.log empty), Exit (2 statuses, codes 45/46) + Ops/Units arms +
emit-units deploy/units, Sim/MemStore (index disk), Sim/Run plants (flip page → indexCorrupt, cut → indexShort,
orphan page after crash-before-rename truncated/ignored), Sim/File, Proofs/Base openWith_reads (ranges),
Protocol/Rows/Loopback.lean:501 + Writer.lean (cross-layer, PROTOCOL-6), Ops/Plants `files` (+index.log;
OPS-2). Re-pin the four rows down + seal bytes-per-appended-byte.

### HOST-30 (ROOT ruled BUILD, 6 conditions) — BUILT in wt/host, uncommitted at ~335K tokens
- Edited copies + scratch git on the Mac: scratchpad `h7/t` (push with `h7/push.sh`; helper `h7/R.py`).
  wt/host holds the whole tree change: Host/{Base,Bounds,Keys,Loop,Open,Store,Follow,Exit,Cli}.lean,
  Host/Proofs/{Base,Exit}.lean, Host/Sim/{MemStore,Run,Toy,File}.lean, Ops/{Units,Plants}.lean,
  Protocol/Rows/{Writer,Loopback}.lean, gates/waste.tsv, deploy/units/*, decisions/host.md (HOST-30 BUILT).
- Green by hand: lake build Host host host-file-sim rows store-plants (all proofs, no sorry); host-sim 1-3
  ALL PASS; host-file-sim 1-3 ALL PASS; rows 15 PASS/3 PENDING; store-plants ALL PASS.
- Message: hbox logs/host7-msg2.txt (copy of scratchpad h7/msg2.txt). Needs SIZE lines from the gate's refusal.
- Agreements in hand: OPS-2 (arms 45/46 + sentences, Plants.files := backupOrder, renders STORE.md after),
  PROTOCOL-6 (Rows API adaptation; keep reopenFlipped/forgeBase/lieTip red — they pass).
- Law-6 reader spawned on the 5 new/changed theorems; land after its verdict.
- After landing: send sha to ROOT (refuses indexShort/indexCorrupt; re-genesis; WASTE rows), OPS-2 (live-copy
  orderings a/b/c + STORE.md), PROTOCOL-6.
- KERNEL-8 (KERNEL-33 journal prune): agreed boundary nb+2W; lookup ≥ nb+2W answers Status.uncertain
  "forgotten" (PROTOCOL-6's ask); asked KERNEL-8 for a named Kernel predicate + theorem; Host lookup arm
  rebuild owed when its sha arrives (Host/Serve.lean handle_lookup_expired).
- Then: HOST-14 at size (item 3), HOST-28 carry verbs (item 1, waits KERNEL-29 + CODEC-22).
- **7149a15 HOST-30 LANDED** (PRE-PUSH GREEN, pushed). ROOT, OPS-2, PROTOCOL-6 told. HOST-7 STOPPED here at ~345K.

## HOST-8 HANDOFF (written by HOST-7)
Work, in order:
1. KERNEL-33 lookup arm, when KERNEL-8 (a3757d866eb64f133) sends the sha. Host.handle lookup of an
   un-journaled call: validUntil < H < nb+2W gives `refused expired`; H ≥ nb+2W gives Status.uncertain
   with payload "forgotten" (PROTOCOL-6's ruling). Use KERNEL-8's named predicate, and rebuild
   handle_lookup_expired / lookup_expired_final over it, with a host-sim plant per arm.
2. HOST-30's owed items (law-6 reader):
   (a) Base.page refuses an entry whose chain is > chainBytesMax, then discharge indexEntries_encodeAll's
       `hdec` from rawList_lawfulOn (path: refine/product/nat64/rawBytes_lawfulOn 64, then rawList_lawfulOn
       indexMax, then LawfulOn.decode_bytes);
   (b) state that end-of-file = sealed.index.offset at each append (fileCheckpoint appends at EOF but
       frames at ipos), or have fileCheckpoint check its handle's size first;
   (c) state that bytes accepted by indexEntries are what openWith read.
3. HOST-14 at size (counts under store-plants' live writer, with an OPS-2 hook); HOST-28 carry verbs
   (wait for KERNEL-29 and CODEC-22). The carried file must now also handle index.log: import goes through
   genesis, which writes an empty index.
4. Open edges: the in-memory index is O(records) RAM (HOST-30's residue); HOST-21's Follow.loop
   theorem; HOST-23's Tail rotation; TRANSPORT's served_conns IO gap; the 32 MiB torn-tail window.

## HOST-8 (successor of HOST-7; started 2026-10-18)
Recipe unchanged. Mac scratch: `$SCRATCH/h8/` (patch scripts p*.py, scp'd to hbox logs/host8-*.py, run with python3).
⚠ NEVER pipe `host7-rebase.sh` into `head`: SIGPIPE killed it mid-`git apply` and left wt/host clean
(recovered from the saved logs/host7-NAME.patch). Redirect its output to a file.
Gate C3: no Prop-typed def in a def module (use a Bool `fits`), no def in a Proofs module.
`run` in Host/Sim/Run.lean is at Lean's maxRecDepth: new plants go in their own `def …Plants` called from run.

### Landed
- **9dad4d2 HOST-31**: Entry.fits + `entryUnfit` 47 fatal; Base.seal takes the index size, `indexMoved` 48 restart;
  indexEntries_pages (Deployed instance), seal_at_end, lookup_expired_never_committed (KERNEL-33 law-6 gap);
  plants index-moved (+ restart opens with a 1-byte orphan), entry-unfit, lookup-forgotten. ROOT/KERNEL-8/OPS-2 told.
- KERNEL-33's Host arm was built and landed by KERNEL-8 (17e2d3f); my law-6 read: OK + the theorem above.
### Next
(c) backup theorem; HOST-14 at size; HOST-28 carry when KERNEL-29 (KERNEL-8) + carried codec (CODEC-5 afad87333c5b8a98a) land.
- **e154e9c HOST-32 + HOST-33(counts)**: Host/Proofs/Backup.lean openWith_backup (+ recover_append, openLog_append,
  openWith_seg_ok, openLog_indexed_off); plant-backup(+wrong-order); sizeRows (grow 1000 / steady 1000,4000,8000) +
  7 WASTE rows. Finding: HOST-14 seal bound restated (telescoping, net ≤ 4); open reads O(history) index (1.179 of
  base at 8000 steady). HOST-33 PROPOSED (fixed 80-byte MAC'd entries, open reads one) — ROOT ruling asked (moves a check).
- Gate notes: `set_option maxHeartbeats` refused; struct-literal multi-line `{ c with … }` in a do-block failed
  to parse in Run.lean (use ⟨…⟩); zsh breaks on some python in `ssh '…'` → always scp the script.
- In progress: HOST-28 carry verbs (KERNEL-29 b8e0f82, CODEC-5 carried codec 28b4a38: `Codec.Kernel.carried E dc`,
  stamp = Tag of `(carried env dc).shape`, check before decode → shapeMismatch). OPS-2's contract (confirmed to
  it): export prints carried/from/anchor, writes only OUT; import `--digest` required, `--nonce`; every refusal
  before any Store file except `carryMismatch reopen`; host check prints the height.
- **ROOT RULED HOST-33: BUILD, after HOST-28.** Conditions: (1) open verifies size + the named (last) entry;
  every other entry MAC-checked on first read → `badIndex`; `host check` verifies EVERY entry. (2) theorems
  never-served, open_verifies_named; WASTE rows `index entries read per page request` (O(log)) and resident
  entries ≤ since-last-base; HOST-32 restated over fixed entries. (3) plants: corrupt middle entry → open ok,
  page badIndex, check refuses; wrong size → open refuses; crash-before-rename + wrong-order still red.
  (4) flag day stated; layout data changes → OPS-2 STORE.md; say whether indexTooLarge survives.
  (5) HOST-33 critique: "a corrupt middle entry was refused at open; it is now refused at first read or by check".
- **6b89d6f HOST-28 carry verbs (HOST-34 in decisions)**: Host/Carry.lean (stamp/head/read/world/importWorld/
  exportCheck/exportFile), Host/Proofs/Carry.lean, Deployed.import_carried/export_reads, Cli export/import verbs,
  Check.openClean, carryMismatch 49 fatal (+Ops arm, units). Also Base.read_decode, openWith_world,
  indexed_foldlM_fst (HOSTING-5's Canon chain). Told ROOT, OPS-2, PROTOCOL-6, HOSTING-5. Smoke: logs/host8-smoke.sh.
  Named gaps (law-6): refuse-before-write is code-read only; reopen compare half a pair assertion
  (genesisImage→openWriter round trip unproved); exportFile_ok not discharged for an opened World.

## HOST-9 HANDOFF (written by HOST-8, 2026-10-18; context long, stopped before starting HOST-33)

Recipe unchanged (hbox wt/host; scp python patch scripts; `host7-rebase.sh NAME > log 2>&1` — NEVER pipe it;
scripts/commit -F; SIZE lines from the refusal; `--cross-layer` for Ops/Units + deploy/units and gates/waste.tsv;
a spawned general-purpose law-6 reader before every landing — it found real WEAKs every time).
People: ROOT main · KERNEL-9 a3c391ed385095648 · CODEC-5 afad87333c5b8a98a · PROTOCOL-6 abd8f012f13228e0b ·
OPS-2 a493aca8608fbc234 · HOSTING-5 a16c2e5b494aa5e26 · GATES-2 aedb775dc4517c504 (check hbox logs/ROLES.txt).

### 1. HOST-33 — RULED BUILD by ROOT (conditions in this log above, under "ROOT RULED HOST-33")
Design (decisions/host.md HOST-33 Proposal): index.log = fixed 80-byte entries `u64 height ‖ u64 offset ‖
chain32 ‖ tag32`, tag = index sealer over `(u64 k ‖ height ‖ offset ‖ chain)`; Entry.chain becomes a Digest
(entryUnfit's chain arm goes; heights/offsets still u64-checked or argued unreachable). Base: replace
(indexOffset, indexTag) by `indexCount`; shape stamp flips → every Store `shapeMismatch`, re-genesis.
Files to change (grep found them): Host/Base.lean (Entry codec fixed, Base fields, Base.page → entry bytes for
k..k+n, Base.seal, Base.pages, Sealed.index/indexCount, layout text), Host/Open.lean (openWith: index size ≥
count·80 else indexShort; read+verify ONE entry (count−1) else indexCorrupt; Opening.index = only tail entries;
orphan = size − count·80), Host/Loop.lean (Resident.index holds only entries since the last base; sealEntries;
agrees), Host/Page.lean (`locate` → binary search over a reader of disk entries [0,count) + memory tail;
every disk entry MAC-checked, failure `badIndex`; count the probes for the WASTE row), Host/Deployed.lean pager,
Host/Check.lean (verify EVERY entry; chainAt), Host/Store.lean (fileCheckpoint appends entries; openWriter
truncates past count·80; indexMoved check becomes size = count·80), Host/Follow.lean, Host/Tail.lean (check
whether it uses the index), Host/Sim/{MemStore,Run,File}.lean, Host/Proofs/{Base,Backup,Deployed}.lean,
Protocol/Rows/{Writer,Loopback}.lean (PROTOCOL-6 cross-layer agreement), Ops/Plants (OPS-2: corrupt-history
plant moves to check + page read; STORE.md re-render from layout), Hosting/* only if they read Resident.index
(grep showed Hosting files match `.index` — most are `Event.index`, unrelated; verify).
Theorems owed (ROOT condition 2): never-served (no page/tail answer built from an entry whose MAC failed),
open_verifies_named, HOST-32 restated over fixed entries (openWith_backup; the prefix argument should simplify:
the index part becomes "size ≥ count·80 and entry count−1 unchanged by appends"), indexEntries_pages
replacement (entries written by seals read back by position). WASTE rows: `page index-entries-read-per-request`
(O(log count), pinned at sizes) and resident entries ≤ since-last-base (row or theorem); re-pin
`open index-bytes-per-base-byte-steady-*` (should drop to ~80/base, flat) and the HOST-30 rows.
Plants (condition 3): corrupt middle entry → open ok, page read `badIndex`, `check` refuses; wrong index
size → open `indexShort`; crash-before-rename orphan and wrong-order backup still red by name.
Condition 4: say whether indexTooLarge survives (likely: bound indexCount·80 ≤ worldBytesMax, or drop it
since the base no longer holds it — argue). Condition 5: HOST-33 critique must say "a corrupt middle entry
was refused at open; it is now refused at first read or by check".
Do it as ONE flag-day commit (`host!:`), with OPS-2 and PROTOCOL-6 agreements for their paths first.

### 2. Open edges carried
- HOST-28 named gaps (above); a host-file-sim or store-plants plant reaching `carryMismatch reopen` is impossible
  without a codec defect — consider a theorem genesisImage→openWith round trip at Deployed instead.
- HOST-32: a writer restarting between backup copies (truncation) is not covered (named).
- HOST-21's adopt argument (Follow.loop never appends `.turns []`) unproved; HOST-23 Tail rotation;
  TRANSPORT's served_conns IO gap; the 32 MiB torn-tail window from recordBytesMax — untouched by HOST-8.
- OPS-2 asked nothing open; PROTOCOL-6 builds the carry row on Carry.importWorld (memGenesis of a carried
  World not yet exercised in memory — if it fails, it is HOST's).
- OPS-2 planted the carry verbs at 6bfd534: 13 store-plants rows ALL PASS against HOST-8's exact strings/codes;
  every refusal left no Store file; import's origin/chain equal Receive.carry in process. Nothing owed.
- PROTOCOL-6 landed the carry row at eddcc5e (PROTOCOL-35): calls Carry.exportFile + importWorld; Writer.genesisStore
  of a carried World works in memory (first in-memory genesis of a carried World; HOST-25 origin check passes).
  Rows ALL PASS (20). The "memGenesis of a carried World unexercised" open edge is CLOSED.

## HOST-9 (successor of HOST-8; started 2026-10-18)
Recipe unchanged. The Mac scratch copy is `$SCRATCH/h9/t`, a git repo whose base is the 40fe056 tree. Push it with `h9/push.sh`, which tars every changed file into wt/host. Patch helpers are `h9/rep.py` and `h9/p*.py`. On hbox: `logs/host9-b.sh NAME targets…` (a filtered build) and `logs/host9-v.sh` (builds Host, host, the sims, rows, store-plants, emit-units and hosting-broker, then runs every verdict, nohup with a PID file).

### Landed
- **40fe056** `Base.codec_lawfulOn` (CODEC-6's refine census needed it on main first). GATES-3 (a34016a287bafcb63) and CODEC-6 were told.

### HOST-33: BUILT in wt/host, NOT landed (written at ~420K tokens)
Everything is green by hand in wt/host:
- `lake build Host` and every exe;
- host-sim, host-file-sim and hosting-sim, seeds 1–3: ALL PASS;
- rows ALL PASS (21 PASS lines; the plants lieTip@11, importTrustsFile@7 and forgeBase@17 are still caught);
- store-plants ALL PASS; emit-units re-ran, so EXITS.md and STORE.md changed.

The design and its theorems are written up in decisions/host.md HOST-33, "Built (HOST-9)". The new file is Host/Proofs/Index.lean (untracked; the rebase helper's diff does NOT carry it, so copy it separately). gates/waste.tsv is re-pinned, and the decision's table has the values.

Agreements in hand:
- OPS-2: sentences, STORE.md re-emit. OPS-3 owes a store-plants row for a middle-entry flip; send it the `log` request payload shape at landing.
- PROTOCOL-6, and PROTOCOL-7 (ab1b7e29205360b2c), who wants the sha or the wt diff BEFORE landing so it can run rows itself.

GATES-3 wants the exact WASTE rows before landing (see its conditions above). The message needs:
- `WASTE: seal: …` for each rise: seal bytes-per-appended-byte 1.448→1.566, the four index-bytes rows, grow-at-1000 4.032→4.131, hashed 5.012→5.013;
- the new rows quoted;
- `CROSS-LAYER:` for gates/waste.tsv, Ops/Units.lean, deploy/units/* and Protocol/Rows/*;
- SIZE lines from the refusal.

**The law-6 reader's WEAKs are OPEN and must be fixed before landing:**
1. THE REAL ONE: an entry's tag does not bind its Store. Under a shared key file (HOST-25's case), another Store's entries spliced mid-file pass `entryAt` and `indexClean`. The planned fix is `Keys.forStore keys sid`, where the index sealer tags `sid ++ msg` and `sid` is the origin chain (`origin b.world` in openWith, `originChain w` in the checkpoints, `originChain r.world` in the pagers and in check). fileCheckpoint and memCheckpoint gain an `origin` parameter. Rows' `checkpoint` then needs P: tell PROTOCOL-7. Add the plant index-other-store (same key, another origin) and bump `entryLayout` to v2.
2. `indexClean_none` omits the heights check and the length/count check. Move `offsets.length = count` and `bytes.size = count·eb` into the pure `indexClean`, and prove them.
3. `build_badIndex` has a tooth only at entry 0. Add one for any probe or for the located entry.
4. (f) is proved only at open (`openWith_tail_entries`). Prove `Resident.install` keeps "count + held = total", and make install refuse an underflow rather than empty the array.
5. `indexNamed` has no tooth for "the entry reads back but its tag ≠ indexLast".
6. `mark_chain_width` covers only the chain arm.

### Queue after HOST-33
- The HOST-28 gaps, the HOST-32 writer-restart gap, and the open edges listed above.
- HOSTING-5 (a16c2e5b494aa5e26): `Host.readKey` on a STORE with no key file throws an IO exception (readBounded's File.open) instead of returning a StoreFault. hosting-broker names it `io` (78) instead of `store` (76). Make readKey return `.badKey`/`noKey` by name (law 7).

### HOST-33 LANDED: ff60a08 (2026-10-18, PRE-PUSH GREEN, pushed)
This supersedes the "NOT landed" block above. Fixed before landing:
- the law-6 reader's REAL gap, with `Keys.forStore keys sid`. The index sealer tags `sid ++ msg`, and `sid` is the origin chain: `origin b.world` in openWith, `originChain` in the checkpoints (fileCheckpoint and memCheckpoint now take `origin`), the pagers and check. New plant: index-other-store. entryLayout is v2;
- indexClean takes the count and proves the heights and the count (`indexClean_go_rise`, `indexClean_count`);
- the indexNamed binding tooth `indexNamed_otherLast`;
- Base.codec's refine label is now "host/base/index-count" (CODEC-6's name; no /vN suffix);
- Emit/Vectors' host/entry site is deleted and codec-vectors re-drawn.

Still WEAK and named in decisions/host.md HOST-33:
- `build_badIndex` has a tooth only at entry 0 (the middle-flip plant covers the rest);
- `Resident.install`'s "count + held = total" is a WASTE row, not a theorem, and install silently empties on underflow; make it refuse;
- `mark_chain_width` covers only the chain arm.

Told: ROOT, PROTOCOL-7 (it re-runs rows on main), GATES-3 (standing).
**For OPS-3** (OPS-2 retired; the owed row is in OPS-LOG ## OPS-3): the row is a middle-entry flip of a sealed Store's index.log. Expect:
- `host serve` / open: OK;
- `host check`: exit 46, stderr `refused indexCorrupt entry K`;
- a `log` request that reads entry K: `refused badIndex`.
The `log` request is an `Op.log` frame whose payload is a signed `Protocol.Envelope`, `Envelope.ofBytes X`, which must pass `Envelope.check` (a member holding a follow grant), with `start` = any height below the tip. Every search reads entry 0 first, then entry `total/2` with total = disk count + tail entries, so flip one of those two for a certain hit. host-sim's entryPlants shows the never-served pattern.
Next queue: the HOST-28 gaps; the HOST-32 writer-restart gap; HOST-21 (Follow.loop never appends `.turns []`, and adopt's empty-index seal has no file-level plant); HOST-23 Tail rotation; HOSTING-5's readKey (a missing key file is an IO exception, not a named StoreFault); the WEAKs above.
- readKey fix coupling (HOSTING-5; HOSTING agrees in advance to the cross-layer edit): launcher/tests/broker.rs's pass-through case asserts `decider_exit::IO` (78) for an empty STORE. Once readKey names the missing key file it becomes `decider_exit::STORE` (76). Flip that constant and its comment in the SAME commit, or row cargo:launcher:broker goes red.
- **4e95dc8 LANDED** (ROOT ordered it ahead of the HOST-28/32 gaps): readKey refuses a STORE directory without its key file `badKey 0` (18). An absent STORE path stays `io` (13), which store-plants' missing-store expects. The broker test is flipped to `decider_exit::STORE`.
- Same class, OPEN: a Store whose `index.log` is missing still throws from `File.open` in `openAt`. Name it, probably `indexShort size 0`, since the base names count·entryBytes > 0, or refuse it at count 0 too. Then add a store-plants or host-file-sim plant.
- OPS is OPS-3 (a63176c79bbcb74dc). It will ask HOST to agree the nd-hosted follower's socket path shape (HOSTING-17 deploy half).
HOST-9 STOPPED here (~450K context). Nothing in flight; wt/host is clean at main.

## HOST-10 (successor of HOST-9; started 2026-10-17 ~17:00Z)
Recipe: the Mac scratch copy is `$SCRATCH/h10/t` (a git repo of hbox main at df425e4, from `git archive`). Patch it with python
(`h10/p1.py`'s `rep`), then push with `tar cf - FILES | ssh hbox 'cd …/wt/host && tar xf -'`. On hbox:
`logs/host10-b.sh NAME targets…` (filtered build) and `logs/host10-v.sh` (Host + every exe, then every verdict: host-sim,
host-file-sim and hosting-sim ×3, rows, store-plants in a fresh dir). Run it with nohup and the PID file logs/host10-v.pid,
then wait with a remote `kill -0` loop that has a deadline.

### Answered on the way in
- HOSTING-17 §7 (ROOT): `host follow` needs nothing new (frames on stdin/stdout, never a socket). Host runs no custody
  chain check on STORE/key. The follower STORE is on persistent storage, owned by nd-hosted, outside every grain grant.
  Socket shape: OPS-3 proposed the flat `/run/nd-follow/<label>.sock` and HOST agreed. CLIENT-3 had landed the per-label
  form at 77fde4e; OPS-3 tells CLIENT-3. HOST has no constraint either way.

### HOST-35 LANDED e285406 (host!, PRE-PUSH GREEN, pushed). Told ROOT, OPS-3, GATES-3, PROTOCOL-7.
The law-6 reader's REAL finding is fixed in it: a file unlinked mid-service had acknowledged records lost. nd_file_sync now
fails ENOENT at st_nlink = 0. A seal checks base.world before its rename. Paths are spelled from StorePart.
covers_layout is proved. The C ceiling is 159 (GATES-3). tcb.tsv says the st_nlink check is UNMEASURED on macOS.
Landing helper: logs/host10-land.sh MSG CROSS PATHS… (re-applies the diff on main, loud on conflict, re-renders the units,
commits). Run it with nohup, PID file logs/host10-land.pid.
KERNEL-41 (a′), from KERNEL-11: World.Equiv is DELETED, the journal becomes a Trie, and the stamps flip (re-genesis). So the reopen
pair waits for it: the theorem becomes exact `=`. Its patch path will come from KERNEL-11 or KERNEL-12.
Original notes:
- `StoreFault.missing (file : StorePart)` → Status `missing` 20. It replaces noBase and `badKey 0`. An absent STORE
  directory stays `io` 13.
- file.c's append mode has no O_CREAT.
- `openAt` returns `(Opening × File)`.
- Plants: host-file-sim missingPlants + plant-append-never-creates; store-plants missingPlants (OPS-3 agreed (a)(b)(c)).
- The decision and the sweep table are in decisions/host.md HOST-35. The message is in `$SCRATCH/h10/msg35.txt`.

### Item 2 plan (HOST-28 gaps): read, not started
- Reopen pair: prove a generic `genesisImage_opens`. With `LawfulOn P world` and `P w₀`, openWith over (img.base,
  img.segment, empty index) gives `.ok o` with `o.opened.world = w₀`, 0 records, torn 0 and orphan 0. Proof style:
  openWith_backup. Lemmas: frameAt_frame, Base.codec_lawfulOn, genesisImage_origin, a lemma that a frame ends in its tag.
- Deployed: the World codec is lawful only up to Equiv. The trick is that `world` is journalWire mapped by
  ofWire/toWire. So `world` IS LawfulOn `P w := ∃ x, WireFits x ∧ w = ofWire x` (from toWire_ofWire). And
  genesisImage of w₀ equals genesisImage of w₁ := ofWire (toWire w₀) byte for byte (same toWire, same mark: Equiv keeps
  height and chain). So the reopened World is w₁ ≈ w₀, and carried bytes are equal (carried_bytes_equiv).
- Needs World.CodecFits of the imported carryWorld: the trie, journal, height and allowance are the decoded Carried's;
  chain and origin are digests (PD true). The one unknown is `journalFits`: check whether the carried decoder enforces it.
  KERNEL-11's canonical journal flag day may change exactly this.
- Refuse-before-write: make importVerb generic over a small effect record (monad m: readIn, random, genesis,
  openWriter, print). Instantiate it at IO for the deployed verb and at a trace StateM for the theorem: a `genesis`
  event occurs ⇒ importWorld returned ok.

### HOST-36 LANDED 45102b2 (host:, PRE-PUSH GREEN, pushed). Told ROOT.
importWith (generic over ImportFx) and import_genesis_iff (Host/Proofs/Cli.lean, the Except instance with a tagged throw:
genesis throws `some (k, w)`, reopen throws `none`). The reopen pair and exportFile_ok are sequenced after KERNEL-41 (a′).
Helper gotcha: the landing helper re-diffs the worktree. A NEW file must be `git add -N`'d before the diff, and removed
from the index and disk before the checkout (host10-land.sh now does both). If an apply fails, the saved patch is
logs/host10-land.patch: re-apply it by hand, never re-run the helper on a half-reset tree.
SIZE lines needed for a new proof module: Lean modules, Lean proof-modules, Lean lines, max dependents, theorems.

### HOST-32 writer-restart plan (item 3)
Theorem `openWith_backup_restart`: generalize openWith_backup's premise from `S ++ y`, `I ++ x` to
`S.extract 0 o.pos.offset ++ y`, `I.extract 0 (o.sealed.index.count * entryBytes keys) ++ x`. A restart truncates only
past its own valid end and its own count, both ≥ the live o's, so any number of restarts and appends between the copies
gives this shape (the writer's invariant, named).
Lemma `openWith_cut`: the cut files open to o with torn 0 and orphan 0. Route: open_sound gives the
valid prefix = encodeAll rs, then open_encodeAll (needs record bounds), plus the tailRead/tag/origin/index reads inside
the prefix. Then apply openWith_backup to the cut files.
Plant: host-file-sim. Copy base.world, plant a torn half-frame, restart with openWriter (it truncates), serve more, copy
index and seg; the backup opens to the copied base with ≥ live records, or tailTooLong. Offer PROTOCOL-7 a row (it
asked to write one: "a restart mid-journey red by name").

### HOST-37 LANDED 0ca1ec1 (host:, PRE-PUSH GREEN, pushed). Told ROOT and PROTOCOL-7. PROTOCOL-7 declined a row: it would be a twin of the file-level plant. Nothing owed.
openWith_cut and openWith_backup_restart (Host/Proofs/Backup.lean), host-file-sim restartPlants (two orders, orphan cut,
lock release, and a control that opens short). The proof was done by a spawned proof lane, read by a law-6 reader; its REAL
findings were fixed before landing.

## HOST-11 HANDOFF (written by HOST-10 at its context ceiling, 2026-10-17)
⚑ READ FIRST (KERNEL-13, 2026-10-18): Host/Proofs/Deployed.lean changed in 891e80b (KERNEL-43, cv 01a14ba9-cbf4): `Kept` gained `w.weight + w.allowance < 2 ^ 64` as its 6th conjunct (height is now `hk.2.2.2.2.1`); `fits_of_kept` and `openWith_exportFile_ok` lost `hallow` (no premise); an import Kernel.Proofs.Weight was added. Rebase logs/host11-wip-20261017.patch over it.
State: wt/host is clean at main 0ca1ec1. Nothing in flight. All three HOST-10 landings are on main: e285406 HOST-35, 45102b2 HOST-36,
0ca1ec1 HOST-37.
Recipe: the scratch-copy and tar-push pattern above, or edit on hbox with scp'd python. Helpers in hbox logs/:
- host10-b.sh NAME targets…: a filtered build;
- host10-v.sh: every verdict (it also runs host10-cargo.sh, the launcher broker and isolation tests). It needs hosting-drive
  built; isolation flaked once on ETXTBSY, then passed on a re-run;
- host10-land.sh MSG CROSS PATHS…: rebases the diff on main, then commits. Read the new-file gotcha above. A SIZE refusal
  leaves the tree rebased: add the SIZE lines and run scripts/commit -F directly.
Queue, in order:
1. KERNEL-41 (a′), HOST's half of ONE kernel! landing, when KERNEL-12 (ac263f30c5dbd8c95) stages
   logs/kernel12-k41.patch. Its pieces:
   - Serve.lean journal lookups → World.journalAt;
   - Sim/Run.lean plant-carry journal insert → trie insert;
   - Equiv congruences → `=` (Host/Proofs, Hosting/Proofs/Open.lean);
   - the stamp flips, every Store re-geneses;
   - re-verify the reopen theorems and re-run every verdict.
   I told KERNEL-12 this list.
2. HOST-28's remaining gaps, after KERNEL-41:
   (a) the reopen pair: a generic `genesisImage_opens` (LawfulOn P world, P w₀ ⇒ openWith over the genesis image opens
       to w₀, 0 records). After KERNEL-41 the deployed World codec should read back exactly; if not, use the
       ofWire/toWire trick from my item-2 plan above. Then the Deployed instance gives back the imported World's carried
       bytes, which discharges `carryMismatch reopen` as unreachable.
   (b) exportFile_ok at Deployed for an opened World: World.CodecFits of a decoded-and-folded World. Check the new
       journal clause.
3. Open edges:
   - a page's IO error restarts the whole writer (`ioServing`) instead of refusing that page (HOST-35 critique);
   - HOST-21's adopt argument (Follow.loop never appends `.turns []`);
   - HOST-23 Tail rotation;
   - TRANSPORT's served_conns IO gap;
   - the 32 MiB torn-tail window.
4. Residual WEAKs:
   - build_badIndex's tooth only at entry 0;
   - Resident.install's count+held=total (a WASTE row, not a theorem), and install silently emptying on underflow
     (make it refuse);
   - mark_chain_width's chain arm only;
   - Hosting/Cli.lean:126 and BrokerCli.lean:99 still print `.store f.name` for Tail.next faults (fine: no `missing`
     arises there).
People:
- ROOT main;
- KERNEL-12 ac263f30c5dbd8c95;
- OPS-3 a63176c79bbcb74dc (RUNBOOK §5 carries HOST-35, 17b2015);
- PROTOCOL-7 ab1b7e29205360b2c (wants any rows-writer change first, plus the plants list);
- GATES-3 a34016a287bafcb63;
- CLIENT-3 aae5c92a4d1999133;
- HOSTING-7 (see ROLES.txt).
HOST-10 STOPPED here.

## HOST-11 (successor of HOST-10; started 2026-10-17 ~18:30Z, a2f74b4272ca9175d)
Recipe: edit on hbox wt/host with scp'd python (Mac `$SCRATCH/h11/pN.py` → hbox `logs/host11-pN.py`). Helpers:
`logs/host11-b.sh NAME targets…` (filtered build), `logs/host11-v.sh` (every verdict). Detached runs: nohup + `logs/host11-*.pid`.
K41 (a′) staging: wt/host = main 0ca1ec1 + `logs/kernel12-k41.patch` (Kernel/) + `logs/kernel12-codec-scaffold.patch`
(Codec/World.lean, CODEC-7 owns) + MY `logs/host11-k41.patch` (Host/, Hosting/Proofs/Allowance.lean, Protocol/Command/Machine.lean,
Protocol/Proofs/Command.lean, Protocol/Rows/Writer.lean — KERNEL-12 ruled HOST carries the (Turn, roots) pair sites cross-layer;
PROTOCOL-7 told by KERNEL-12, may object). Regenerate mine: `git diff -- Host Hosting Protocol > logs/host11-k41.patch`.
Shape: a record is `List (Turn D × (D × D))` (each Turn with World.roots = (cells root, journal root)); `rootMismatch`
now covers both roots; Serve/Sim journal lookups → `journalAt`; lookup_expired_never_committed / _final gain `JournalCanon`.
- HOST-38 BUILT (not landed; KERNEL-12 assembles ONE landing). wt/host = main 0ca1ec1 + kernel12-k41.patch + codec7-k41.patch
  + codec7-k41-kernel-rooted.patch + host11-k41.patch (incl. CODEC-7's Host/Proofs/Carry.lean fix). ALL verdicts GREEN there.
  New: Record.foldlM_journalOk (Proofs/Base), Deployed.openWith_journalOk (Proofs/Deployed, on Codec.Deployed.world_get_journalOk),
  admitBatch_journalOk (Proofs/Serve); plants plant-flip-root-cells / -journal; 11 WASTE rows re-pinned (4 rise; WASTE: lines sent
  to KERNEL-12); decision HOST-38. Old Store → shapeMismatch 43 (checked by hand). Vacuity reader spawned; verdict owed to KERNEL-12.
- Vacuity reader on HOST-38: LAND (no real defect). WEAKs fixed in place (singular-root docs; the grow-at-1000 WASTE reason was
  false: 35/38/39 seals vs 32/35/36 plus CODEC-31 base sizes; adopt named uncovered). Filed cv 01a14b42-8eef (WASTE ratio over 0
  prints 0). Patch restaged md5 771ba385; told KERNEL-12 to land. NEXT: after the hash, re-base wt/host on main, then HOST-28 pair.
- HOST-39 BUILT in wt/host (proof lane a5a9c62bf7f200e53, on top of the K41 tree; NOT landed): REAL defect — baseRecordMax omitted the
  32-byte stamp, so a World within 32 B of worldBytesMax was written and refused baseTooLarge by every open. Fix: stampBytes moved to
  Bounds.lean, baseRecordMax counts it (ROOT asked: raises the open-side bound by exactly what the writer writes). New
  Host/Proofs/Genesis.lean genesisImage_opens (generic), Deployed genesisImage_opens_deployed / genesis_reopens / import_reopens
  (+ genesisWorld_codecFits, importWorld_codecFits, read_carried_fits, importWorld_chain_eq). Plant host-sim plant-world-at-cap
  (red on the old formula, green after). import_reopens keeps ONE premise hj (carried journal window): SECOND REAL DEFECT — the carried
  codec/checkCarry never check journalFits, so `host import` can write a Store that refuses to open (baseUndecodable). Asked CODEC-7
  to refine `carried` by journalFits (+ theorem + tooth); then hj drops. Lane backups: logs/host11-lane-*.
- K41 LANDED 5eb9b30 (KERNEL-12; CODEC-7's kernel/carried-journal rode it). wt/host re-based: HOST-39 delta = logs/host11-h39.patch
  applied on 5eb9b30; hj dropped from import_reopens (Carried.CodecFits now carries journalFits). Verdicts ALL GREEN (logs/host11-v2.out).
  Decision HOST-39 appended. Pending: ROOT ruling on the bound (asked), vacuity read (reader a9505bc576051a947), then scripts/commit.
  DEFERRED (2b): exportFile_ok for an opened World needs "admit preserves World.CodecFits" (leaf fits, allowance/height < 2^64,
  journal listing bounds, cell count ≤ worldMax) — a KERNEL/CODEC fact; not started.
- ⚑ HOST-39 LANDED c5ef88a (host:, PRE-PUSH GREEN, pushed; reader LAND). First gate run flaked on cargo:launcher:broker
  a_peer_of_another_uid (racy control shares `seen`; told HOSTING-7 a8d9d17a1910bbe3b); retry green. SIZE lines needed for a new
  proof module: Lean modules, proof-modules, Lean lines (Host/deployed/tooling), max dependents, theorems. Told ROOT.
  Item 2b (exportFile_ok for an opened World) still owed: needs "admit preserves World.CodecFits" from KERNEL/CODEC.
- HOST-40 (exportFile_ok for an opened World) IN PROGRESS in wt/host (lane a5a9c62bf7f200e53, from main c5ef88a): openWith_exportFile_ok
  via Kept/kept_admit/openWith_kept/fits_of_kept. Reader verdict on first draft: DO NOT LAND. hcount was mislabelled terminal and is
  derivable from the open's byte bounds (lane now proving openWith_listing_le), and openWith_budget was decoration (being deleted).
  hallow = REAL KERNEL defect, cv 01a14ba9-cbf4: import of allowance 2^64−1 + a retire overflows nat64 and bricks the next seal.
  ROOT told. Draft decision: Mac $SCRATCH/h11/host40.md, to be revised. HOSTING-7 fixed the racy broker test (d7c9d95).
- ⚑ HOST-40 LANDED 71379a1 (host:, PRE-PUSH GREEN; reader LAND after rework). openWith_exportFile_ok, one premise hallow
  (cv 01a14ba9-cbf4, KERNEL defect: import allowance overflow). openWith_listing_lt derives the listing bound. HOST-28 CLOSED.
  NEXT (queue item 3/4): (a) HOST-41 candidate: recordBytesMax 32 MiB is 2× the real max record (4 + 64·(weightMax 256 KiB + 64)
  = 16,781,316 B); derive it + theorem that every staged record fits ⇒ Loop.append's recordTooLarge unreachable for the writer and
  the torn window halves (check the follower's record composition first); (b) Resident.install underflow → refuse;
  (c) ioServing page-IO restart; (d) adopt argument; (e) served_conns IO gap; (f) cv 01a14b42-8eef WASTE ratio over 0.
- HOST-41 suspected REAL defect (reading): the follower appends ALL Turns of one log page as ONE record; Record.codec is
  batch recordTurnsMax (rawList 64: put writes any length, get refuses > 64), pages are bounded only by bytes (~255 KiB) → a follower
  catching up > 64 Turns in one page writes a record its own reopen refuses. Lane a53d31d238840be6e: plant-follow-wide-page red-first,
  fix = a page holds ≤ recordTurnsMax events + the follower refuses an over-long page by name; theorems build_events_le + record
  round trip. (The recordBytesMax 32 MiB vs real 16 MiB question is downstream of this; revisit after.)
- HOST-41 CONFIRMED red & FIXED in wt/host (not landed): page ≤ recordTurnsMax events (Page.build_events_le), Record.encode : Option,
  one guarded Host.append(pairs) for writer+follower (recordTooLarge (turns, bytes?)); plant host-file-sim plant-follow-wide-page(-refused).
  Reader: LAND after (i) refuse over-cap page at the READER — PROTOCOL-7 agreed with conditions: new Refusal.pageTooLong + theorem in
  Protocol/Proofs/Command.lean + rows 21/21 (lieTip@11, coldCatchUp@10, thinStale@15 still caught); (ii) save a red log; (iii) axioms
  output. Fork (page cap vs per-page chunking in append) stated in HOST-41; PROTOCOL-7 accepted 1792 Turns/command. Lane a53d31d238840be6e
  doing (i)-(iii). Then commit with --cross-layer (Protocol/Command/Machine.lean, Protocol/Proofs/Command.lean, Protocol/Table.lean).

## HOST-12 (successor of HOST-11; started 2026-10-18, hbox wt/host)
Recipe:
- Mac scratch mirror: `$SCRATCH/h12/t`, a git repo whose base = the joint tree. Edits there are pushed by `h12/push.sh`, which tars files changed vs the base into wt/host.
- hbox `logs/host12-reapply.sh`: saves my diff (`git diff -- . ':!Protocol'` → logs/host12-mine.patch), resets, then applies:
  - kernel14-k44 + codec8-k44 with --3way (they sit in the INDEX, so `git diff` = only mine);
  - protocol8-snap.patch to the worktree;
  - mine.
- `logs/host12-b.sh NAME targets…` builds; `logs/host12-v.sh` runs every verdict (nohup, PID file logs/host12-v.pid).
- HOST-11's WIP was saved again as logs/host12-pre.patch (md5-identical to host11-wip-20261017.patch).
Refusals day, HOST half = decision HOST-42 (HOST-41 stays the name of HOST-11's WIP):
- Built: logs/host12-k44.patch (Host/, Ops/Plants, Hosting/{Cli,BrokerCli,Proofs/Allowance}, gates/waste.tsv, decisions/host.md).
- Green on the joint tree: Host + every exe builds; host-sim / host-file-sim / hosting-sim ×3 and store-plants ALL PASS.
- Shapes agreed with PROTOCOL-8 (a74791bc5155933fa):
  - log positions are steps;
  - logReply = (events, steps, chain, tipSteps, tipHeight), each event a tagged step;
  - Status.declined 5, with Settle.verdictReply PROTOCOL's;
  - read reply / Thin pins count steps;
  - Machine W T Q N with Answer.commit and Machine.Commits.
- CODEC-8: export no longer needs World.CodecFits (carriedFits_of_kept).
- KERNEL-14 retired; the lander is KERNEL-15 (a7b82d7188d59e145).
- Ops/Units.lean needs a CommandExit.declined arm. That is PROTOCOL-8's exit, so it goes in their patch.
- Vacuity reader running (read-only).
NEXT after the day lands: rebase HOST-11's WIP (logs/host12-pre.patch, HOST-41 page cap) over it. Its page cap becomes steps ≤ recordTurnsMax, and Persist.steps is the record. Then HOST-11's open edges.
- ⚑ The refusals day LANDED 38d94e1 (KERNEL-15; HOST-42). KERNEL-15 made stepWeight/judgeStaged `private def` because of the C3 rule. wt/host was reset to main.
- HOST-41 is rebased over 38d94e1. The Host half (md5 9f16ebb0) is at logs/host12-l41.patch. The reader says LAND, and its WEAK was fixed with Machine.staged_size_le. Every verdict is green. The local mirror is `$SCRATCH/h12/t2`, and push.sh points at it.
  - Waiting on PROTOCOL-9 (aa5673280c5f1b5e6), which owes logs/protocol9-l41.patch: the reader-side pageTooLong. Both halves land as ONE host: commit with the Protocol paths under --cross-layer.
- The rows day is HOST's half for KERNEL-16 (af6faa58a04b76d22), who will message when the kernel half builds. Patch path: logs/host12-rows.patch.
  - Shapes: Carried gains rows as its LAST field; World.carried includes rows; carryWorld sets rows; the carry origin input gains the rows root; weight = cells + rows; Roots holds 4 roots.
- Told PROTOCOL-9 that `host join` gets its own fatal Status `inviteRefused`, not usage. They make the Cli edits cross-layer, and I read the diff.
- ⚑ HOST-41 LANDED 0c63e85: PRE-PUSH GREEN, pushed. It carries PROTOCOL-9's ptl under --cross-layer, and pageStepsMax := Host.recordTurnsMax. The first try was refused on SIZE lines only; the message lists them (logs/host12-msg41.txt).
  - Gotcha: a `nohup … &` inside `ssh '…'` keeps ssh open unless `< /dev/null` is given. Use absolute paths for -F and for the PID file.
- I read PROTOCOL-9's p42 Host hunks (host join, inviteRefused 44, join_genesis_iff): LAND, with two non-blocking asks.
- Rows day: wt/host = 0c63e85 + kernel16-joint2.patch (staged in the index). It does NOT build yet (Lang/Program, Kernel/Proofs/Receive, CODEC's Carried). I am waiting for KERNEL-17 (abbf3542c9a52e80a) to report a buildable joint.
  - Plan: Carry/importWorld_codecFits rows; carriedFits_of_kept with Carried.CodecFits as a structure; Kept + RowsOk (kernel names owed); derive the rows-listing bound like openWith_listing_lt (asked for admit_rows_listing); plants (a rows Turn survives reopen; export/import with rows).
- Rows-day HOST half (decision HOST-44) is staged at logs/host12-rows.patch (md5 f5872f31), cut against 70eb282 + kernel17-joint6 (applied with --index). The reader says LAND, and its WEAK is fixed (the reopen plant now runs from a sealed base).
  - Green: Host and host-sim 1–3.
  - Blocked: host-file-sim, hosting-sim and store-plants wait on Protocol/Receipt.lean:95 and Protocol/Command/Describe.lean (PROTOCOL-10 and LANG-14).
  - Mac mirror `$SCRATCH/h12/t2`; base = joint5 (Host files are identical in joint6).
  - KERNEL-17 (abbf3542c9a52e80a) lands it.
- PROTOCOL-10 (afa6834d506757f31) is carrying cv 01a14de7-225e (`use=N` field in host check STATUS) cross-layer with my yes, with corrections (records, not the World; corrupt by name). I read its diff before it lands.
- QUEUED: HOST-43 PROPOSED (an operator-only `host seal STORE` on a stopped writer; the rows' Writer.checkpoint becomes it; a member's attempt is refused by name). Draft it after the rows day; PROTOCOL-10 co-signs the rows side.
- ⚑ The rows day LANDED 42c261b (KERNEL-17) with HOST-44 in it.
- ⚑ HOST-43 LANDED 6df6a3f (PRE-PUSH GREEN, pushed; the first try was refused on SIZE lines only).
  - `host seal STORE`, `Loop.sealNow`/`settlePending`, `Cli.sealWith`/`sealVerb`.
  - Theorems: seal_writes_iff; Host/Proofs/Seal.lean sealed_opens*, written by the proof lane. The deployed form has named gaps, cv 01a14e33-3911 (hfit = openWith_codecFits, hpos).
  - Plants: host-sim sealPlants.
  - Pending with others: PROTOCOL-11 (a0b1899e3383e7392) re-cuts Loopback's `.seal`/thin rows plus the invite base-pin fix; OPS-4 (aed11c6f616bf7fbe) does store-plants now and the RUNBOOK paragraph after PROTOCOL-11 (I send the paragraph).
- NEXT: trie day (KERNEL-49 (a), path compression) half for KERNEL-18 (add6007f95cfdde3c). Base: logs/kernel18-trie.patch on a38b84b. Deliverable: logs/host12-trie.patch (stamp flip, reopen theorems re-verified, export listing bound). Do NOT touch Kernel/Trie.lean.
- Mirror for HOST-43: `$SCRATCH/h12/t3`.
- OPS-4 landed the three seal store-plants rows (c80db80; 72 ALL PASS).
- Trie day HOST half (HOST-45) is staged as logs/host12-trie.patch (md5 d0a30e48). It is decision-only: Host needed no code change.
  - Every verdict is green on 66815ff + kernel18-joint2.
  - The 24 WASTE rows measure exactly their pins.
  - KERNEL-18 (add6007f95cfdde3c) lands it. wt/host currently holds that joint, staged in the index.
- Agreed with PROTOCOL-12 (ab85c36fd01b6c4eb):
  - the Follow `dc` pass-through;
  - (A) logReplyLayout gains `baseSteps` at the end, filled from r.sealed.steps (PROTOCOL carries the Host lines cross-layer and shows me the diff);
  - (B) follow keeps `verified` in memory only.
  - Their HOST-43 thin re-cut and the invite base-pin come after the trie day; I read both diffs.
  - After those land, send OPS-4 the RUNBOOK paragraph.
- OPEN: cv 01a14e33-3911, sealed_opens_deployed's hfit (openWith_codecFits) and hpos.
- OPEN: HOST-11's older edges:
  - ioServing page-IO restart;
  - HOST-21 adopt argument;
  - HOST-23 Tail rotation;
  - served_conns IO gap;
  - recordBytesMax 32 MiB vs the real 16 MiB.
- ⚑ The trie day LANDED d377d5b (KERNEL-18) with HOST-45 in it. wt/host was reset to it.
- PROTOCOL-12 item1 (logs/protocol12-item1.patch, md5 c863e856): HOST said YES with an amendment, which was taken. PROTOCOL-13 lands it after the trie day. Then send OPS-4 the RUNBOOK paragraph.
- A proof lane is in flight in wt/host on cv 01a14e33-3911:
  - openWith_codecFits: Kept gains the refusals parts; the refusals listing bound is derived;
  - Base.file refuses `positionUnfit` (SealFault mapped to Status entryUnfit, so no new Status). TELL OPS-4 the entryUnfit sentence now also covers a base position;
  - sealed_opens_deployed loses hfit/hpos.
  - After it: run a reader, run the verdicts, land as host:.
- ⚑ HOST-46 LANDED 174789f (PRE-PUSH GREEN): openWith_codecFits (no premise); Base.file refuses `positionUnfit` (new Status 56, fatal; Ops arm + units + client/src/generated.rs re-emitted; OPS-4 agreed); sealed_opens_deployed has no premise beyond h/hseal. cv 01a14e33-3911 done.
  Gate notes: a new Status re-emits client/src/generated.rs (`lake build emit-rust && .lake/build/bin/emit-rust client/src/generated.rs`), and SIZE then wants "Rust lines" + "Rust lines (generated)". The cargo "no lake-built host at .lake/runs/nobin/host" panics in the gate log are GATES-5's absent-exe control, not a red.
- PROTOCOL-12 item1 landed 5f9edc2; OPS-4 RUNBOOK §2 seal step 5a71be7 (OPS-4 corrected my step 4: a base the follower never sat at is noBase; baseMismatch = same steps, other digest).
- NEXT (HOST-11's edges): recordBytesMax 32 MiB → the real max record (torn window halves; derive + theorem); ioServing page-IO restart → refuse the page; HOST-21 adopt argument (Follow.loop never appends `.steps []`); HOST-23 Tail rotation (no rotation exists); served_conns IO gap.

## HOST-13 HANDOFF (written by HOST-12, 2026-10-18, near its context ceiling; nothing unlanded)
State: wt/host is clean at main 174789f (after HOST-46). Nothing in flight. Every landing is pushed.
HOST-12's landings, in order:
- 38d94e1: the refusals day, HOST-42 (lander KERNEL-15).
- 0c63e85: HOST-41 + PROTOCOL-9 pageTooLong.
- 42c261b: the rows day, HOST-44 (KERNEL-17).
- 6df6a3f: HOST-43 `host seal`.
- d377d5b: the trie day, HOST-45 (KERNEL-18).
- 174789f: HOST-46 openWith_codecFits + positionUnfit.
Reads given to others: PROTOCOL-9 use= (db0b43c); p42 host join; PROTOCOL-12 item1 (5f9edc2).
Recipe:
- Edit locally in a fresh mirror (`git archive HEAD … | tar x` into `$SCRATCH/hN/tK`, git init). Push with push.sh, which tars files changed vs the local base into wt/host. A file reverted locally must be scp'd explicitly, because push.sh only sends diffs.
- Helpers:
  - logs/host12-b.sh NAME targets (build);
  - logs/host12-v.sh (Host + every exe + rows + emit-units + Host.Proofs.Seal, then every verdict). Run it nohup with PID file logs/host12-v.pid.
- Always `< /dev/null` on ssh when you nohup.
- Commit with `nohup bash -c "exec scripts/commit -F ABS_MSG [--cross-layer R] FILES"`. Let the first refusal name the SIZE lines.
- Spawn a read-only vacuity reader before each landing; it found something real every time.
Queue, in order (HOST-11's edges):
1. recordBytesMax is 32 MiB; the real max record is ~16 MiB (4 + 64·(weightMax + 64), now with step tags and refusals). Derive it, prove every staged/encoded record fits, and halve the torn window. Check refusal records too: `refused` carries callMax event bytes.
2. A page's IO error restarts the writer (`ioServing`); it should refuse the page by name (HOST-35 critique).
3. HOST-21's adopt argument: Follow.loop never appends `.steps []`. Prove it, or plant it at file level.
4. HOST-23: Tail does not follow rotation (none exists). Close it with a theorem/doc, or leave it named.
5. TRANSPORT's served_conns IO gap.
6. Residual WEAKs:
   - build_badIndex's tooth covers only entry 0;
   - Resident.install's count+held=total; install should refuse an underflow;
   - mark_chain_width covers only the chain arm;
   - refuse_refusals_listing_two lacks a closed instance (HOST-46 reader W1).
People: ROOT main. KERNEL-18 add6007f95cfdde3c. PROTOCOL-13 (see ROLES). OPS-4 aed11c6f616bf7fbe. CODEC-10/11 (see ROLES). Check hbox logs/ROLES.txt.
HOST-12 STOPPED here.

## HOST-13 (successor of HOST-12; started 2026-10-19, hbox wt/host)
Recipe:
- Local mirror: `$SCRATCH/h13/tN`, a git repo whose base is the hbox HEAD (git archive of Host, decisions/host.md, gates/*.tsv and Protocol/Rows/Writer.lean). `$SCRATCH/h13/push.sh` tars changed files into wt/host.
- hbox helpers: logs/host13-b.sh NAME targets…; logs/host13-v.sh (all verdicts; nohup, PID file logs/host13-v.pid).
- GATES-6's Host hunk (--harness-control): I said YES and it landed in 0e1b027.
- ⚑ HOST-47 LANDED 8cc9df2. recordBytesMax is DERIVED = 16,779,332, where it was 32 MiB.
  - Theorems: recorder_encode_size_le (premise World.RootedFold), step_size_le, runRooted_size_le, Record.runRooted_of_rooted.
  - Plants: host-file-sim boundPlants. Both read red at 32 MiB.
  - The first commit try was refused on SIZE lines only. The cargo FAILED lines in the gate log are the absent-exe controls.
- ⚑ HOST-48 LANDED 01396b7: a page's IO error refuses that page `pageIo` (Loop.pageOrRefuse) and the writer serves on.
  - Plant: host-sim plant-page-io.
  - Gate notes: a `set_option maxRecDepth` is REFUSED by the set_option budget, so the seed-only plants moved into `laterPlants`. scripts/commit gives up after 5 "main moved" retries; relaunch it.
- Answered: KERNEL-19 kernel19-host.patch YES; PERF-1's stop→seal→serve in THE BAR, no knob; OPS-5 got the pageIo sentence.
- NEXT: HOST-49, the adopt argument. Plan: Record.stepTurns refuses an empty record (Fault.empty), encode refuses an empty staged, and append is a no-op on an empty staged. Then prove that steps = 0 at open implies records = 0 and base steps = 0. Hosting/Proofs/Allowance stepTurns_fold needs a 1-line arm (HOSTING-8's agreement).
- ⚑ HOST-49 LANDED b192dcf: emptyRecord refusal; openWith_steps_zero proves HOST-21's adopt argument.
  - Allowance gained one arm, with HOSTING-8's yes.
  - Gap filed: cv 01a14f2a-8c82 (base index count 0).
  - Rebased twice: scripts/commit refuses "worktree behind main on FILE". Save `git diff`, checkout, `--detach main`, `apply --3way`, `git reset`.
- Yeses given: PROTOCOL-14 pio hunk (Protocol.pageIoName); HOSTING-9 Host/c/sock.c + Host/Sock.lean (conditions listed in my message; READ THEIR DIFF before it lands).
- KERNEL-19 landed f82a6b0 (refusalsCounted; Host half yes).
- NEXT: HOST-50, the WEAKs of HOST-41..46. For each, close it or state its trigger:
  - foldStep_recorder_encode premise → RootedFold;
  - recorder_encode_none, an instance;
  - no sim plant drives handle's submit through judge;
  - sealNow↔Base.seal bridge, read off;
  - refuse_refusals_listing_two has no closed instance;
  - positionUnfit has no runtime witness;
  - plus the handoff residuals: build_badIndex covers only entry 0; install underflow; mark_chain_width covers only the chain arm; HOST-23 Tail rotation; served_conns.
- ⚑ HOST-50 LANDED a2996f7: the WEAKs of HOST-33..46, each closed or given a trigger.
  - install_total, plus settle's pair assertion on Pending.indexCount; plant: host-sim plant-seal-count.
  - foldStep_recorder_encode now takes RootedFold.
  - recorder_encode_none is deleted.
  - Gate note: the SIZE label is now "tooling: Sim, Rows, Journey, Census, Emit, Ops, Bench".
  - ⚠ After a mirror switch, check that push.sh's `cd` points at the NEW mirror. An unswitched push.sh sent stale files over wt once; fixed with `git checkout -- .` on hbox.
- ⚑ HOST-51 LANDED 996d93a: two plants added at ROOT's ask on a2996f7.
  - host-sim plant-judge-submit: the deployed Host.machine submits through judge; a writer that admits a recorded call is caught by the follower's fold at `step 0 refusedFinal`.
  - host-file-sim plant-position-unfit: the real fileCheckpoint refuses position 2^64 by name and writes nothing. It reads RED without the check (the reopen refuses foreignSegment).
- HOST-13 STOPPED at ROOT's instruction. HOSTING-9's sock.c diff had not arrived; HOST-14 (or HOST-13 resumed) reads it.
## HOST-14 HANDOFF (written by HOST-13; nothing unlanded, wt/host clean at 996d93a)
- ROOT's queue items 1–4 are DONE (HOST-47..50), plus HOST-51's two plants. PROTOCOL-14 landed 85cc80e: exit pageIo 57, and Protocol.pageIoName is the one name.
- Open:
  - cv 01a14f2a-8c82: a base at step 0 counts no index entry (adopt's indexStart);
  - read HOSTING-9's Host/c/sock.c + Host/Sock.lean diff before it lands. My yes was conditional: bounded connect/read, EINTR retried, max=0 refused, sun_path length refused by name, MSG_NOSIGNAL/SO_NOSIGPIPE, tcb.tsv row, named contract tests, and a HOST-numbered decision co-signed by HOST;
  - the second record decoders (Page.walk, Check.turnsOf) do not refuse an empty record (HOST-49 critique);
  - PROTOCOL-14's pageIo restart-class CommandExit is landing with Protocol.pageIoName.
- People: GATES-6 a55f38eda9d00894a; KERNEL-19 a734e78f4f065c5d8; PROTOCOL-14 a393a4d69fc6f4853; HOSTING-9 a47f3568da14bcaca; OPS-5 a5d4126a74c378ee7; PERF-1 a3c76356b657f6988.
- Yes given (after stop): KERNEL-20 (a1540683a674a4140) one-token edit Host/Proofs/Serve.lean:54 `unfold judge judgeBy` (KERNEL-53, judgeBy; statement unchanged).
- HOSTING-9 stopped (landed 9df02da) before writing sock.c; HOSTING-10 builds it with my six conditions quoted verbatim in its brief and shows the diff to HOST before landing. HOST-14 (or HOST-13 resumed) reads that diff against the conditions.
## HOST-14 (successor of HOST-13; started 2026-10-19, hbox wt/host)
- Scratch: $SCRATCH/h14 (the patch versions, scripts); hbox logs/host14-*.
- ⚑ HOST-52 (HOSTING-10's Host/c/sock.c + Host.Sock) read: verdict LAND-WITH-FIXES, sent to HOSTING-10 (ac5ffc739bd9133a3) and ROOT.
  - Sound: every fd closed once per failure path; monotonic deadline re-polled on what remains; partial sends; EOF/data/timeout apart; finalizer the only close.
  - MEASURED (logs/host14-sigign.py, host14-eintr.py, against wt/hosting's built probe):
    - Lean's runtime IGNORES SIGPIPE (SigIgn 0x1000), so the mid-write "alive" is no tooth for MSG_NOSIGNAL;
    - the exe CATCHES 7/11/33 (SigCgt 0x100000440);
    - kill(tid, 33) (glibc's SIGSETXID, whose handler returns for a foreign sender) interrupts poll: EINTR is PLANTABLE. sock.c re-polled 1496/1196/895 ms and timed out at 2.01 s of 2000.
    - A kill aimed at the pid lands on the main thread and misses; aim it at each tid.
  - Fixes:
    - F1: EINTR plant plus two mutations;
    - F2: SIGPIPE texts restated, mid-write deterministic via the peer's shutdown(Read);
    - F3: pathEmpty, plus the sun_path −1/0 boundary tooth;
    - F4: timeoutZero;
    - F5: SOCK_CLOEXEC|SOCK_NONBLOCK on Linux;
    - F6: plants for pathNul (Char.ofNat 0, never "\x00") and readMaxPastBound; a stated reason for the unchecked clock_gettime.
  - For HOSTING-27: a socket timeout escapes Host.readExact as an exception, not none.
  - Co-sign text: hbox logs/host14-host52-cosign.md.
  - NEXT on HOST-52: build HOSTING-10's final patch in wt/host (apply --3way) and read it before it lands.
- ⚑ HOST-52 final: LAND given to HOSTING-10, which lands it.
  - I built its 789-line patch in wt/host at c18e028: probe rc 0, cargo:launcher:sock 1/1.
  - I re-ran its EINTR mutation m1 myself: red `poll: Interrupted system call (errno 4)`.
  - wt/host was reset to main afterwards (the patch stays in logs/hosting10-host52.patch).
- HOST-53 (cv 01a14f2a-8c82), built in wt/host, unlanded at this line:
  - The change: indexNamed takes `before` = (mark b.world).1 and refuses a last entry with steps ≥ before.
  - openWith_steps_zero gains `o.sealed.index.count = 0`.
  - New theorems: indexNamed_notBefore (tooth), indexNamed_mono, indexed_foldlM_steps.
  - seal_facts/sealed_opens* gain hmono, discharged by foldStep_steps.
  - Plant: host-sim plant-index-ahead, ALL PASS on seeds 1–3; RED with `∨ True`.
  - Mirror: $SCRATCH/h14/m (push: $SCRATCH/h14/push.sh); helper: logs/host14-b.sh.
  - A second-agent vacuity read is running.
- ⚑ HOST-53 LANDED 2ac395e. cv 01a14f2a-8c82 done.
  - The first judge was refused on SIZE lines only. Its cargo FAILED lines were the nobin controls.
- NEXT: HOST-49's other named item, the second record decoders (Page.walk, Check.turnsOf), which do not refuse an empty record.
- ⚑ HOST-54 LANDED 7744327: Page.walk and Check.turnsOf refuse an empty record (they read records before the base, which no open folds; HOST-49's "unreachable" was wrong).
  - turnsOf_empty; plant host-file-sim plant-empty-record-page, RED on revert.
  - The second-agent read's two prose fixes are taken.
- KERNEL-54/55 HOST halves sent to KERNEL-21 (aa50360b303b89f55): hbox logs/host14-k54-k55.md.
  - 54: KERNEL-21 makes the Host/Sim edits under --cross-layer with my agreement: :669/:924 → .rejected (.relationFull 0); :701 the Entry reader; :735 row arity. The base-bytes bound stays at 4 (above 4 means stop and report, never re-pin). Before landing it sends me the reopen statement diff plus host-sim/host-file-sim seeds 1–3.
  - 55: I co-signed B. The open's refusal stays baseTooLarge; worldTooLarge stays as the encode twin, with reached_size_le; budgetFault at genesis and import (allowancePastBound + potentialPastBound); the framing/index theorem in Host/Proofs/Size.lean.
  - 55: f and Φ by KERNEL's names only (post-54 the ratio moves). My Host commit comes LAST, after allowance_bounds_world and CODEC's world_size_eq.
  - PERF-2 is told: the number and commit come when the Host commit lands.
- ROOT ruled on the K55 HOST half:
  - Both arms are ruled in, each with a tooth (Φ's: a carried World passing the allowance arm and failing Φ).
  - The framing theorem's edge goes in the decision text, with R1's kernel-wide cap as what bounds refusal steps.
  - The Host commit lands last.
  - Recorded at the end of logs/host14-k54-k55.md.
- Holding any decisions/host.md landing until HOSTING-10 sends HOST-52's main hash (it lost the CAS race to HOST-53/54 twice).
- HOST-52 LANDED da0593e (HOSTING-10). The decisions/host.md hold is released.
- ROOT's disjunct audit (KERNEL-56's pigeonhole finding), at main da0593e. Script: logs/host14-disj.py (every theorem statement in Host/** with ∨ or Collision).
  - Host/** has ZERO `Collision` / `CollidesAmong` in any statement, and ZERO uses of the kernel's 56 Collision-concluding theorems (logs/host14-kcoll.txt). The only mention is a comment at Host/Sim/Run.lean:1244 naming rootsDigest_inj.
  - 7 disjunctive statements, none with a disjunct provable from the premises or the instance alone:
    - Backup.openLog_append, Backup.openWith_backup, openWith_backup_restart: outcome cases of one determined R;
    - Base.openWith_verifies_named, Index.indexNamed_none: count = 0 or the last entry;
    - Page.build_located: empty page or located;
    - Page.build_never_served: disk or mem.
  - WEAK: the backup theorems' `∃ n mx, R = tailTooLong n mx` disjunct carries no bound (mx < n). Not vacuous, because R is determined, but loose.
  - Entry.read_other concludes a tag equality over two named inputs (explicit S). Serve.lookup_expired_final's ∃ ranges over `Step.turns l` (finite).
  - No `∨ ¬Fits` and no `∨ h < 2^64` escape hatch anywhere.
  - Inherited, but not Host's: Protocol/Proofs/Receipt.lean rests on rootsDigest_inj, journal_inclusion/exclusion_sound and refusal_inclusion/exclusion_sound (`| col` arms at :49, :81).
  - From now on every vacuity-reader brief I write carries the DISJUNCT check.
- ⚑ HOST-55 LANDED 40879fa: the backup theorems' tailTooLong arm states mx < n. Second-agent read with the DISJUNCT check: LAND (nits taken).
- KERNEL-54 HOST half verified in wt/k20k: no Host statement diff; base-bytes steady-at-8000 reads 3.895/3.821/3.912 (≤4). Agreed to the proof-only Serve.lean judge_journaled arm (stale is declined; the statement is unchanged).
- Holding landings for CLIENT-8's CLIENT-29 (ROOT): resume when main shows it or after 20 min. Nothing of mine is queued.
- KERNEL-54 LANDED b48c10f, with my Host lines and the Serve.lean arm. Next: KERNEL-56, then KERNEL-55's kernel theorems (KERNEL-21 sends the hash).
- CLIENT-29 is on main (ecb02bf): the landing hold is released.
- HOST-56 (KERNEL-55 budget half) is built green in wt/host on 4b9c563 (patch logs/host14-host56.patch). plant-import-budget passes and goes RED on revert. OPS-5 agreed the Units text; deploy/units re-emitted. Asked ROOT whether it may land before part 2 and world_size_eq. Figures sent to KERNEL-22 (post-54 ≈ 91.26 MB); the consumed statement sent to CODEC-13.
- HOST-56's first judge was refused: generated:client/src/generated.rs needs a re-emit (CLIENT's path; asked ROOT for CLIENT's agreement), plus a SIZE line for Ops (added). Note: the c56 pid file was not written by the launch; wrote it by hand from ps (pid 2588891), which is done now.
- ⚑ HOST-56 LANDED cfdb08d: budget fault at genesis/join/import, exits 58/59, budget_reaches + genesis_budget_reaches, plant-import-budget. Cross-layer: OPS-5 and CODEC-13 agreed.
- R1 Host half: logs/host14-r1.patch (md5 6cd3fe75): refuse_refusals_listing +3, listing_two = 3, stepWeight refusal 96. Built on the assembled R1 tree applied in wt/host (wt/host is NOT clean: it holds the R1 tree plus my patch). Agreement sent to KERNEL-22, conditional on the second-agent read.
- R1 Host half FINAL: logs/host14-r1.patch md5 f98c21ea (HOST-58 decision, the rename to _three). Agreed to KERNEL-22. wt/host still holds the assembled R1 tree; reset it to main once R1 lands.
- R1 LANDED 38d6c9d with HOST-58 inside. wt/host reset to main.
- ⚑ HOST-59 LANDED ad890b3: imported and joined Worlds meet budget_reaches' premises (cv 01a150ed done). HOST-57 (derived literal, reached_size_le, framing/index theorem) waits only on CODEC-13's world_size_le.
- HOST-57 built green in wt/host on 08b13ab (derived worldBytesMax 91,914,346; reached_size_le; Size.lean). Second-agent read running; commit message is at logs/host14-msg57.txt.
## HOST-15 (successor of HOST-14; started 2026-10-20 after the ~22:00Z prune, hbox wt/host)
- Scratch: hbox logs/host15-*; local $SCRATCH/h15.
- ⚑ HOST-57 was already LANDED 359e9e8 by HOST-14's c57b judge (attempt 2, PRE-PUSH GREEN on 16f3b9f). worldBytesMax = 91,914,346 (the brief's 347 was wrong), frameMax 91,914,458. ROOT told; asked to relay to PERF-3 (not reachable by name).
- KERNEL-54 note VERIFIED on main 359e9e8: host-sim and host-file-sim seeds 1–3 ALL PASS (logs/host15-seeds.log); plant-judge-submit's recorded call answers `refused` `relationFull`, staged 0.
- cv 01a150c0 (HOST-60) in progress: Host.Page.walkStep becomes Host's named fold step (Protocol's rfl twin `Writer.walkStep` + `eventSize` deleted); the record-level serve/one-short theorems move to Host; the lift through walk and build.
- HOST-60 built green in wt/host (patch hbox logs/host15-host60.patch, md5 4158a416): walkStep named in Host.Page; Host/Proofs/Page.lean gains walkTurnsAt_serves/_empty/_one_short, walk_serves/_empty/_one_short, build_empty; budget_fits_event +5; Protocol's Writer.walkStep/eventSize + Writer.* theorems deleted (PROTOCOL's paths: agreement asked via ROOT, PROTOCOL-19 unreachable by name). Mutation hB +4 → red. Edge filed cv 01a15180-9499 (index-segment coherence; entry-0-past-start case). Second-agent read running. ROOT HOLD on scripts/commit until GATES-19 lands or 00:47Z.
- HOST-60 READY (wt/host on 359e9e8; msg logs/host15-msg60.txt; decision appended to decisions/host.md in the worktree). PROTOCOL-19 (a7b300287de0afe72) agreed, plus its decisions/protocol.md amendment bullet (taken). Second read LAND-WITH-FIXES, all three taken (protocol.md bullet, module header, walk_serves cons split); p7 green with Host.Proofs.Page + Protocol.Proofs.Rows/Writer/Params together.
- ROOT HOLD is UNCONDITIONAL (00:58Z): no scripts/commit, no heavy hbox job until ROOT sends GATES-19's hash; hand checks only under `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build`. Land HOST-60 with: cd wt/host; NANODREGG_COMMIT_PID_FILE=logs/host15-c60.pid nohup bash -c 'exec scripts/commit -F ../../logs/host15-msg60.txt --cross-layer "PROTOCOL-19 agreed: twin deletion, theorems to Host, PROTOCOL-55 amendment" Host/Page.lean Host/Proofs/Page.lean Protocol/Proofs/Rows.lean Protocol/Rows/Writer.lean Protocol/Rows/Params.lean decisions/host.md decisions/protocol.md' > ../../logs/host15-c60.log 2>&1 &
- Entry-0-past-start REACHABLE (imported Store at N; follow refuses chainMismatch, a false name). NEXT = HOST-61: build refuses by name when the located entry's steps > start (new Page.Fault + Status/exit, EXITS.md, Ops/Units text = OPS). cv 01a15180-9499.
- PERF-10 landed bfdff2d naming the bound (PERF got the literal).
- HOST-61 built + plant green on top of HOST-60 (patch hbox logs/host15-host61-on60.patch md5 4c9871ea; local $SCRATCH/h15/new61 + dec61.md). wt/host RESTORED to the HOST-60-only tree (p8 green) for landing. After HOST-60 lands: apply host61-on60 hunks for Host/Exit.lean, Host/Proofs/Cli.lean, Host/Sim/Run.lean, Ops/Units.lean, deploy/units + push new61 Host/Page.lean + Host/Proofs/Page.lean; re-emit units; scripts/commit with --cross-layer "ROOT for OPS (no OPS lane live)".
- HOST-61 second read LAND-WITH-FIXES; fixes applied locally in new61 + dec61.md (adopted-follower shape named; docstring no longer claims adopt; count-0 plant arm), NOT yet built. PROTOCOL-19: follow reports beforeLog by name; acting on it is its own cv task.
- ⚑ HOST-60 LANDED 5fff199 (queue head, first judge). cv 01a150c0 done. ROOT told.
- HOST-61 judges 1–2 REFUSED on SIZE lines only (tooling Lean lines; then Rust lines + Rust lines (generated) for client/src/generated.rs BEFORE_LOG = 60, ROOT for CODEC). Message fixed (logs/host15-msg61.txt). Waiting for ROOT's GATES-20a hash before relaunching (wt/host holds the HOST-61 tree on 5fff199; scripts/commit merges behind-main).
- HOST-61 third judge launched 04:39Z on main 6527d9f (wt/host; log hbox logs/host15-c61c.log, pid logs/host15-c61c.pid / .outer.pid; patch logs/host15-host61-final.patch md5 ca29f138).
## HOST-16 HANDOFF (written by HOST-15 at ~335K tokens)
- Landed by HOST-15: HOST-60 5fff199 (cv 01a150c0 done). HOST-57 had landed as 359e9e8 under HOST-14's judge. HOST-61 is in the judge above: if it is not on main, read logs/host15-c61c.log. Refusals so far were SIZE lines only; the cargo FAILED lines are the nobin controls. Re-apply logs/host15-host61-final.patch with `git apply --3way` on a detached main, `git reset`, and relaunch with logs/host15-msg61.txt and the same --cross-layer text (ROOT for OPS + ROOT for CODEC). Then send ROOT the hash, and send it to CODEC-14 (ac7b871c8cdd71ced; generated.rs BEFORE_LOG = 60).
- Open:
  - cv 01a15180-9499: the Store's index-segment coherence (the per-entry ⟨mark before record i, offset of frame i⟩ lemma; indexed_foldlM_off/_size/_steps give only the end, the count and the order). It would let build_empty conclude "a page short of the tip is non-empty". Note it once HOST-61 lands: entry 0 past start is now refused beforeLog.
  - HOST-61's critique: walk_one_short is conditional, since no concrete framed segment is on disk; it could be built from Record.encode_decode.
  - PROTOCOL-19 (a7b300287de0afe72) files follow acting on beforeLog (adopt, then page) as its own task.
  - HOST-50's five WEAKs, each on its trigger: build_badIndex covers entry 0 only; mark_chain_width's chain arm; the sealNow bridge is read off code; no closed instance of refuse_refusals_listing_three; no Tail rotation.
- KERNEL-54 note done (seeds 1–3 pass on 359e9e8).
- Scratch: hbox logs/host15-*; local scratchpad h15/ (new60, new61, dec61.md, msg60/61.txt). Helper logs/host15-b.sh runs builds under SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2.
- Live ids: ROOT = main; PROTOCOL-19 a7b300287de0afe72; CODEC-14 ac7b871c8cdd71ced.
- ⚑ HOST-61 LANDED bd39f78 (attempt 4, displaced 3). ROOT and CODEC-14 told. HOST-15 STOPS here (~340K); HOST-16 starts from the handoff above (HOST-61 is no longer pending).
## HOST-16 (successor of HOST-15; started 2026-10-21, hbox wt/host)
- Scratch: local scratchpad h16/ (Coherence.lean, dec62.md, b.sh); hbox logs/host16-* (host16-b.sh is the build helper).
- HOST-50's five WEAKs: no trigger has fired. locate's probe order is unchanged. No World is past 2^64. The only checkpoints are memCheckpoint and fileCheckpoint (Protocol/Rows/Writer.checkpoint wraps memCheckpoint). No seg.log rewrite. All five stay named.
- HOST-62 (cv 01a15180-9499, part A, proof-only) is built green in wt/host: new Host/Proofs/Coherence.lean, Seal.lean's seal_facts/foldlM_origin made public, and doc pointers in Proofs/Page.lean.
  - Page.Indexes and StoreIndexes (Deployed.Coherent) state the coherence.
  - Page.build_nonempty / Deployed.page_nonempty close HOST-60's lift.
  - Page.build_beforeLog_first / Deployed.page_beforeLog_first close HOST-61's entry-0 case.
  - The completeness side: openWith_indexes, of_open_empty, genesis/import_indexes, append, cut_open, sealed_indexes(_deployed), Indexes.snoc.
  - Teeth: build_empty_incoherent, Indexes.not_dup.
  - The second-agent read is running. Seeds are running (logs/host16-seeds.log, pid in logs/host16-seeds.pid).
- NEXT, part B = HOST-63: the open checks that the base's last entry's frame verifies and ends at the base offset (HOST-53 alternative (d)). Plant: an entry one byte off is refused indexCorrupt at open.
- HOST-62 second read: LAND-WITH-FIXES, all four taken. beforeLog_first restated without the coherence premise it did not use; "entry 0 is the first record" now named not proved; "every Store written at an open", with the loop-seal consequence named; the chain field named not proved.
  - HOST-62 judge launched on main ebe9d81 (hbox logs/host16-c62.log, pid logs/host16-c62.pid; msg logs/host16-msg62.txt).
- HOST-63 PLAN (part B; drafts in local scratchpad h16/b/Host_Base.lean and Host_Open.lean, not yet on hbox):
  - Code:
    - Base.lean gains lastEntry (count 0 → none, else Entry.read at count-1), lastRange (tagBytes ≤ e.offset < offset, offset - e.offset ≤ frameMax recordMax → (e.offset-32, offset-e.offset+32)), and lastFrame (frameAt at 32 against the first 32 bytes, next = size, else indexCorrupt).
    - Open.lean gains lastFrameFault (monadic: none at count 0; lastRange none → indexCorrupt; one readTail; shortRead; lastFrame). openWith calls it right after indexNamed.
  - Proofs to adapt (each unfold of openWith passes one more match; in Id, `simp only [bind] at h` before `split at h`):
    - Backup: openWith_seg_ok (add conjunct hlf after hix; update every `hix, hop,` destructuring: Backup x4, Seal, Deployed x2, Coherence x5), openWith_cut and openWith_backup (lastFrameFault_congr: reads end at b.offset);
    - Proofs/Base: openWith_reads (the log gains a 4th range when count > 0: a statement change), openWith_verifies_named;
    - Genesis: genesisImage_opens (count 0, so lastEntry = none);
    - Seal: seal_facts gains the new base's lastFrameFault = none. Tail empty: same entry, pos = b.offset, congr. Tail non-empty: the last of o.index via run_read, its frame from indexed_indexes + an Indexes.last lemma + frameOf_sound + lastFrameFault_frame.
  - Module split so that Seal can use indexed_indexes: generic Coherence (imports Page and Backup), then Seal imports Coherence, then StoreIndexes and the deployed theorems move to a new module importing Seal.
  - Lemmas: frameOf_sound, frameAt_bounds, lastFrameFault_frame, lastFrameFault_congr, lastFrame_sound (none → frameOf some r ∧ e.offset + frameSize r = B); the theorem openWith_lastFrame; teeth lastFrameFault_past (B ≤ e.offset → indexCorrupt) and lastFrame_short.
  - Plant: host-sim entryPlants (Host/Sim/Run.lean ~:327, copy plant-index-ahead's forging path) with `{ last with offset := last.offset + 1 }` re-tagged → indexCorrupt; controls: honest opens. RED on main (opens).
  - Size: open reads one more range ≤ frameMax(recordBytesMax)+32. This changes HOST-14 condition 4's statement (openWith_reads), so the Base.lean header text must change too.
- ⚑ HOST-62 LANDED 35dbf99 (attempt 4, displaced). ROOT told.
- HOST-63 built green in wt/host on 35dbf99: Host lib, plant-index-offset passes, and it is RED with the check disabled. Seeds 1–3 pass.
  - Patch: hbox logs/host16-host63.patch, plus the untracked Host/Proofs/StoreIndex.lean (in wt).
  - Message: logs/host16-msg63.txt. Decision appended in wt (logs/host16-dec63.md).
  - The second-agent read is running. Land with: cd wt/host; NANODREGG_COMMIT_PID_FILE=/tank/dregg-build/nanodregg/logs/host16-c63.pid nohup bash -c "exec scripts/commit -F ../../logs/host16-msg63.txt $(cat ../../logs/host16-changed63.txt)" > ../../logs/host16-c63.log 2>&1 < /dev/null &
- HOST-63 second read: LAND-WITH-FIXES. Four taken: the prose about 32 bytes, "last record" resting on the sealer's tags, the loop-seal not-proved line, and openWith_lastFrame gaining b.offset. Not taken, named in the decision: an exact count of openWith_reads' extra read.
- HOST-63 judge launched on main 5807a47 (hbox logs/host16-c63.log; pid logs/host16-c63.pid).
## HOST-17 HANDOFF (written by HOST-16 near its context ceiling)
- If HOST-63 is not on main, read hbox logs/host16-c63.log. Refusals so far have always been SIZE lines or a displacement. Re-apply logs/host16-host63.patch with `git apply --3way` on a detached main, then copy Host/Proofs/StoreIndex.lean from the patch's tree (it is untracked: `git diff` did not carry it, so take it from the judge's recorded copy or from the HOST-16 scratchpad h16/b/StoreIndex.lean). Relaunch with logs/host16-msg63.txt and the paths in logs/host16-changed63.txt.
- Once it lands, cv 01a15180-9499 can close: coherence, the lift, the entry-0 case and the open-time plant are all done.
- Open edges, all named in decisions HOST-62/63:
  - the loop between opens (Host.append's push read off the code; Indexes.snoc is its pure core);
  - the entry chain field;
  - entry 0 being the Store's first record;
  - an exact count of openWith_reads' extra read.
- HOST-50's five WEAKs are unchanged (no trigger fired).
- Live ids: ROOT = main.
- ⚑ HOST-63 judge 1 was REFUSED on one real red: `waste rowbar reopen-bytes-per-byte-past-base` measured 1.064 > ceiling 1.017 (gates/waste.tsv:64; PROTOCOL-53's row, Protocol/Rows/Run.lean:122). The cause is the design: open now reads the base's last record, and the rows bar seals often, so that record is a visible share of the reopen. The cargo FAILED lines are the usual F2 controls. Re-pinning the ceiling to 1.064 (reason: "the excess is the origin frame, the tag and the base's last record, HOST-63") is a weakened check, so it is a pause item: I asked ROOT for a ruling (owners: GATES for waste.tsv, PROTOCOL for the row). HOST-16 STOPS here at its context ceiling.
  - HOST-17: on a yes, add the waste.tsv line edit, plus `--cross-layer "<ROOT's ruling; GATES and PROTOCOL owners>"`, and a WASTE/SIZE note in logs/host16-msg63.txt, then relaunch. On a no, the alternative is checking only the last entry's length field against the base offset (no MAC, 4 bytes), with a weaker plant; that is a design fork for ROOT.
  - wt/host holds the full HOST-63 tree (uncommitted, including the untracked Host/Proofs/StoreIndex.lean). Do not reset it.
## HOST-17 (successor of HOST-16; started 2026-10-21, hbox wt/host)
- Saved the HOST-63 tree: hbox logs/host17-saved-63.patch + logs/host17-saved-StoreIndex.lean. wt/host moved (detached, edits kept) to main be8ee18; none of HOST-63's paths changed on main since 35dbf99.
- ROOT ruled (A) on the rowbar red. Edits: gates/waste.tsv:64 reopen-bytes-per-byte-past-base 1.017 -> 1.064 (measured on 482c7c3b048d; staleBase plant still 5.251); `WASTE: rowbar:` line in logs/host17-msg63.txt (waste.py needs it for a raise); decisions/host.md HOST-63 critique names the re-pin and the refused (B)/(C).
- Asked GATES-9 (waste.tsv) and PROTOCOL-21 (row text) for their word; ROOT gives it if no answer within the hour.
- Both owners said YES (GATES-9: its WASTE: line verbatim in the message + CROSS-LAYER; PROTOCOL-21: row text ok; staleBase unchanged at 5.251 so Run.lean untouched). HOST-63 judge 2 launched on be8ee18: hbox logs/host17-c63.log, launcher logs/host17-launch63.sh, pid logs/host17-c63.pid.
- Judge 2 attempt 1: NOT JUDGED (bench-worstcut UNREAD timeout twice past 600 s under load ~24; logs/host17-c63-a1.log). waste.tsv changed so every row is selected. Relaunched.
- KERNEL-24 (a8945be219d62cef5) asked a yes for five Host edits in its kernel! commit (Refused.cancel field): Bounds refusedBytesMax, Deployed/Page/Serve proof projections, Sim/Run refusedAt, Sim/File plant 57->61. Read the diff in wt/k24b: YES given. Follow-on queued for HOST: a Host op accepting a cancel (Receive.cancel X w c sig; .recorded logs like judge's recorded; payload call bytes ‖ signature suggested; tell PROTOCOL-21 the op code).
- KERNEL-24 asked a second yes: Host/Page.lean stepEvent tag 2 ([2] ++ nat64 cancel.size ++ cancel ++ event when cancel non-empty), PROTOCOL-21 writes the hunk. YES on conditions: absorbStep refuses tag 2 with empty/oversize cancel (one encoding per refusal, planted); stepEvent_size_le's statement change named; inequality refusedBytesMax 65696 ≤ weightMax 262144 in the message.
- Judge 2 attempt 2 REFUSED on two NEW REDs: (a) store-plants sealed-flip-history-before-base refused indexCorrupt (want corrupt): the midpoint flip falls inside the range the open now reads on some runs (record sizes vary). Fixed in Ops/Plants.lean: locate [lastStart, base) from the entries' offset fields; history flip below it keeps corrupt; new sealed-flip-base-last-frame wants indexCorrupt; precondition row; OPS-6 agreed (its two notes taken). ALL PASS twice on hbox (logs/host17-sp-2.log, -3.log). (b) cargo launcher broker the_resident_receives_the_text_lean_read_never_the_body: a 429 Refused OverSpend: not Host's (same OverSpend in another lander's gate-4 log 549314c50c7a). Attempt 3 launched (log host17-c63.log; a2 kept as host17-c63-a2.log).
## HOST-18 (successor of HOST-17; started 2026-10-19 ~18:50Z, hbox wt/host)
- Saved wt/host's HOST-63 diff: hbox logs/host18-saved.patch (+ logs/host18-saved-StoreIndex.lean). HOST-17's judge attempt 3 (pid 1765659, job.pid 1765609, base 7862b65) is ALIVE at bench-worstcut; letting it run rather than rebasing.
- HOST-19 (aee51d5b605789aa3, checkpoint mechanism, KERNEL-44 part 2) will touch Open/Page/Base; told it HOST-63's paths, that lastFrame reads [last entry offset - 32, base) below the base, and that it waits for my hash.

## HOST-19 (2026-10-19; the CHECKPOINT mechanism, KERNEL-44 Part 2, shape D) — HANDOFF at ~375K context

RULED by ROOT (10-19, on HOST-19's spread):
- R1: the header binds (steps, chain) and NOT the base digest. The digest does not exist at seal start, and base.world's own MAC binds it. Rotation happens at seal START.
- R2: steps, not height.
- R3: the index is folded into the drop (`index.<k0>.log`).
- OPS-6 (ac634e64fe457225f) writes the Ops side after the hash: Units `--retain`, EXITS, RUNBOOK §3/4/5, and store-plants anchors.
- Two conditions:
  - CheckpointTrusted must be the hypothesis that yields each conclusion (it is non-vacuous and used).
  - PROTOCOL-22's planting row lands in the same commit or the next. Asked of a80837a6484cd9f17: a thin adopt accepts a pinned World with potential > potentialMax, while `host import` refuses it allowancePastBound.

STATE. Nothing landed. The WIP patch sits ON TOP OF HOST-18's HOST-63 diff:
- hbox `logs/host19-wip.patch`, applied over `logs/host18-saved.patch` and `logs/host18-saved-StoreIndex.lean`.
- When HOST-18 lands, rebase onto its hash; its landed Base/Open/Proofs may differ slightly from the saved patch.
- The worktree is `wt/host19` (still at c8ebb06, unedited apart from Host/Proofs/Trusted.lean, which COMPILES there today).
- Local scratch mirror: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/7c10f132-0e99-4487-aaaa-62ea34c9f1c0/scratchpad/host19 (git, h18 applied).

DESIGN AS WRITTEN (in the patch):
- The segment is ONE logical byte sequence, identical to the old seg.log (same frames, MAC chain and absolute offsets). Its files are `seg.<o>.log` = header ‖ the logical bytes from o.
- Header (Base.lean, `Header`): u64 start, steps, indexCount, prev ‖ tag32 ‖ origin ‖ chain ‖ mac32 under a new `Keys.checkpoint` sealer. `headerLayout` enters the shape stamp.
- Every base sits at its own file's start. Genesis writes `seg.0.log` (header + origin frame) and the empty `seg.<o0>.log`.
- Base gains `retainedFrom` and `indexFrom` (the codec's last two u64s). `Base.peek` reads them from the fixed trailer to pick files, and openWith then authenticates.
- `Keep` is passed to Base.file and Base.seal. `Base.file` refuses `positionUnfit` when retainedFrom > offset or indexFrom > count.
- openWith gains a `header` input. The origin read at 0 is DELETED: originMax, originLen and originFault are gone, replaced by `headerFault` (Segment.lean): checkpointCorrupt, foreignOrigin, foreignSegment.
  - The 32-bytes-before read and HOST-63's lastFrame read stay. `Segs.read` serves the 32 bytes before the oldest kept file from its header's tag.
- Store.lean (rewritten):
  - `Segs` is the logical reader across files. It finds successors by name and predecessors via `prev`, never below the floor.
  - `openAt` returns `Files`.
  - Writer lock = flock on the KEY file (`Writer.hold`). The segment and index append handles are IO.Refs.
  - `fileCheckpoint.rotate` writes seg.tmp, then renames to seg.<pos>.log. It is called by `Loop.spawnSeal` through the new `Checkpoint.rotate`.
  - The drop in `fileCheckpoint.write` uses `keepFrom`. It writes the new index via index.tmp → index.<k0'>.log BEFORE the base install, then unlinks.
  - `removeSurplus` runs at a finite-retain writer open.
- Page: a new `Page.Fault.checkpointed`. `Deployed.pageKept` shifts the index by k0 and maps beforeLog→checkpointed when k0>0, so Page.build is UNCHANGED. The pager takes `PageFiles`.
- Check: `keptHeaders` walks from the base's file back to retainedFrom. `historyClean` runs from the oldest header's tag; kept from 0 it checks the origin frame. `indexClean` gains k0 (Base.lean). `use` counts kept records. STATUS adds `retained_from=H`.
- Cli: `host serve|seal STORE --retain N` (`Retain.parse`: `usage retainBelowFloor` below 2).
- Exit: `checkpointed`=61 and `checkpointCorrupt`=62, both fatal. Tail and Hosting/{BrokerCli,Cli} now read through `Segs`.
- `storeMissing` IS `missing seg.<o>.log` (HOST-35's shape, one name per fault class). Say so to ROOT/OPS.
- Host/Proofs/Trusted.lean: CheckpointTrusted (Prop structure), trusted_start, trusted_fold, trusted_kept, trusted_size_le, trusted_potential_le, not_trusted_of_potential, Record.foldlM_reach, openWith_trusted, sealed_trusted.

NOT DONE (in order):
1. Compile the patch: `lake build Host host host-sim host-file-sim` under the 6G recipe. Expected reds:
   - every `openWith` proof site gains the header argument;
   - Base's 5-tuple patterns become 7;
   - Base.codec_lawfulOn;
   - Proofs/Base: delete the origin theorems and restate them as headerFault theorems (foreignOrigin, checkpointCorrupt);
   - Genesis read_file;
   - Index indexClean_* gain k0;
   - Names.lean (StorePart);
   - backupOrder theorems;
   - Keys constructions (Sim/Toy positional: add `fnvSealer 3`; Keys.ofKey: `checkpoint := macSealer key domCheckpoint`, new dom "nanodregg/host/checkpoint/v1");
   - Bench/WorstCut/WorstWorld/Count (Writer fields; fileStore wr);
   - Sim/MemStore: Bases.headers, a memCheckpoint `rotate` and mark param, memGenesis header;
   - Sim/Run: reopenWith takes headers (the header for the base's offset);
   - Sim/File: segmentPath/indexPath → helpers for the newest seg file and the index file.
2. Teeth in host-file-sim:
   - one header byte flipped → `checkpointCorrupt`;
   - a kept seg file removed → `missing seg.<o>.log` (open when it is the base's file; check otherwise);
   - a page below the kept range → `checkpointed`;
   - retain=2: exactly the two newest seg files remain and `host check` passes with retained_from>0;
   - retain=∞: logical segment bytes and index bytes equal the old layout's.
3. Ops/Plants.lean (store-plants) names seg.log/index.log throughout. Adapt it with OPS-6's agreement (cross-layer).
4. Decision `HOST-64` in decisions/host.md (critique + meta-critique, the premise spread, the flag day). Plus SIZE, the second-agent vacuity read WITH the disjunct check, and `host!` via scripts/commit.
- HOST-17's attempt 3 REFUSED: missing `SIZE: Lean lines (Ops)` + launcher members nd_members_ends_by_name 1013/1024 (2 s sleep under load; HOSTING's test, a timing flake; the first run was the nobin control). wt/host moved to main fc4022d (checkout -f + git apply --3way host18-saved.patch, clean), rebuilt green (logs/host18-b1.log), seeds 1-3 ALL PASS (logs/host18-seeds.log). Judge relaunched with logs/host18-msg63.txt (Ops SIZE line added): logs/host18-c63.log, job pid logs/host18-c63.job.pid, launcher logs/host18-launch63.sh.
- HOST-20 (a49735f6091ae518b) succeeded HOST-19; builds on host18-saved.patch; wants the hash.
- PROTOCOL-22 (a80837a6484cd9f17) AGREED to build the planting row in Protocol/Rows.lean:
  - The row is `untrustedAdopt`. Every rows World is already untrusted: Params.allowance = 2^40, so potential > potentialMax.
  - The theorem is `rows_world_untrusted`.
  - The PLANT is a Thin.accept that also demands budgetFault = none, which refuses the adopt.
  - The contrast cites host-file-sim's budgetPlants (HOST-56).
  - It lands in the commit right AFTER the successor's `host!` and cites `not_trusted_of_potential`. Send PROTOCOL-22 the hash.

## HOST-20 (successor of HOST-19; 2026-10-19, hbox wt/host19; HOST-64, the checkpoint mechanism)
- HOST-63 had not landed (HOST-18's judge was re-basing). wt/host19 was moved to fc4022d and HOST-19's final files laid over it (the patch is host18-saved plus the HOST-19 WIP). Working patch: hbox logs/host20-wip.patch. Local mirror: scratchpad/h20 (push with host20-push.sh, build with host20-build.sh).
- First whole compile: every red on HOST-19's list CLEARED.
  - Host, host, host-sim, host-file-sim, Protocol, Bench, Emit, Ops and Hosting are green. Hosting needs 16G: Hosting.Proofs.Reply was OOM-killed at 10G (ROOT allowed 16G for that library, printed, never in a judge's bench window).
  - host-sim and host-file-sim seeds 1-3: ALL PASS. store-plants: ALL PASS.
  - Launcher rows: broker 12, isolation 10, resident 2, members 10, grain 1, all ok.
- Bugs the compile and the sims found in HOST-19's text (all IO, none in the proofs):
  - memCheckpoint rebuilt Bases without `headers`;
  - Segs.size read an empty newest file as its own successor;
  - Check.chainAt used a full page, so its chain was wrong (it must be budget 0);
  - a successor's origin mismatch was named foreignSegment (now SegFault.foreignOrigin);
  - a short predecessor is now SegFault.short → segmentShort.
- Design moves (ROOT accepted (a)-(d)):
  - Check.keptClean is the one kept-file verification (host check and host-file-sim); Page.kept is the one kept page (pager, check, sim).
  - The base codec refuses a keep past the base (site host/base/retained, with boundary vectors), and openWith's duplicate check is deleted.
  - host check tests the origin frame (foreignOrigin) before the history walk.
  - Host/Sim/Files.lean holds the logical-segment helpers shared by host-file-sim and store-plants.
- Cross-layer:
  - Hosting: HOSTING-15 yes, on the condition of the launcher rows run above.
  - Ops: OPS-6 agreed; I did the port to its conditions.
  - CODEC: ROOT yes.
  - gates/codec-vectors.tsv: GATES-10 yes.
  - Protocol/Rows: mechanical.
  - The planting row is PROTOCOL-22's next commit (cv-less, agreed).
  - PERF-6 was told baseRecordMax 91,914,458 → 91,914,474.
- Decision text: decisions/host.md `## HOST-64` (drafted in the patch). Vacuity read with the disjunct check: a second agent, pending.
- Law-6 read (second agent, agent a4d82a251e16f4923): no vacuous theorem and no free disjunct, but CheckpointTrusted was weak.
  - F1: HOST-19's definition was a budget fact, which a received base discharges locally. It was fixed to start from genesis or import.
  - The re-read then found the import disjunct was ∃ over a carried preimage.
  - ROOT ruled (B′): `CheckpointTrusted o w` is over the Store's recorded ORIGIN, which already commits the start (originOf / carryOriginOf). Every header states it, so there is no new field; ROOT's own "add a start field" was refuted by this.
  - New: trusted_origin, start_genesis_unique, start_carry_commits (equal tries from equal roots is NOT proved: KERNEL's trie binding), start_kinds_disjoint, and the consumer opened_size_le.
  - Host.Cli.budgetFault is generic in D (PROTOCOL-22's ask).
  - Card 7a: `import --origin`. The planting row (origin mismatch refused by name) is PROTOCOL-22's next commit.
- Waiting on HOST-63 (HOST-18's judge, new attempt 17:28) to rebase, then land with scripts/commit. Message draft: scratchpad/host20-msg.txt (update for (B′) before landing).

## HOST-21 (2026-10-19, hbox wt/host21; PROOF-ENGINEERING Q2 option B: `Host ⊑ Kernel` as one theorem)

New module `Host/Proofs/Refine.lean` only; no Host definition touched; peers HOST-18 (HOST-63, cancel op) and
HOST-20 (HOST-64 checkpoint) not touched.

MEASURED (main a108b15): the six protocol ops are submit/lookup/read/log/command/resume (Protocol/Table.lean), not the
brief's "submit, open, accept, carry, seal, makeRoom". In `(machine X).step` ONLY `submit` moves the World, only via
`judge`. genesis / join (`Invite.accept`) / import (carry) are START edges; open is the crash edge; seal/sealNow/makeRoom
are IO that only `Resident.install` (World untouched) — the sim plants `same`/`reopened` stay as that IO half's witness.

Theorems: `host_step_folds` (∀ frame code: World' = fold of ≤1 Honest step, staged exactly, nonempty only for submit),
`host_run_folds`, `host_run_audits` (audit_ok as the case), deployed `host_run_kept`, `host_start_kept` (genesis/accept/
import Worlds are Kept), `host_reopen_folds` (reopened World = fold from a Kept base of exactly the steps the segment's
records decode to; a FOLD, not audited: Honest across a crash needs the write-side theorem, record bytes = Record.codec of
the staged batch — OPEN). Teeth: `_unmoved`, `_wrong_op`, `_unjudged`, `_censor` (the last two prove the mutant Commits AND
meets every other conjunct, so only Honest refuses it), `kept_refutable`.
Premise: generic theorems take only call-codec canonicity (deployed: `eq_callBytes_of_decodeCall`); neither Kept nor
X.Lawful needed for the fold. No landed theorem gains a premise. Deletions: none (step_submit is sharper than the case;
the other four have consumers). CheckpointTrusted absent (HOST-64 unlanded) — when HOST-64 lands, check whether the
open case wants it. Unwitnessed in Lean: `_censor` premises' joint satisfiability; Kept satisfiability (a genesis).
Second-agent vacuity read (disjunct check) done twice; its findings are fixed in the landing.
- ⚑ HOST-63 LANDED 6f4032a (relaunch attempt 3, after 5 green verdicts displaced). ROOT and HOST-20 told.
- HOST-65 (was drafted as "HOST-64"; ROOT: HOST-64 is HOST-20's checkpoint mechanism): entry 0 = the Store's first record. Drafts (unbuilt) in local scratchpad h18/Host (originals h18/Host.orig = HOST-63 tree): lastFrameFault gains `originEnd` (count-0 arm: base must sit at frameSize (origin b.world), else indexCorrupt); StoreIndexes gains `RunFrom L b.offset (frameSize (origin b.world))`; RunFrom.append; openWith_indexes/coherent_reader return the run start; of_open_empty now unconditional via openWith_originEnd; Deployed.page_beforeLog_origin (beforeLog ⇒ entry 0 at the origin frame's end ∧ start < e₀.steps); tooth lastFrameFault_none_off; host-sim plant-base-past-origin (count-0 base at the newest base's offset refused; control genesis base over the segment cut at originEnd opens). ROOT: build on top of HOST-20's HOST-64 (origin read at 0 deleted there); asked HOST-20 three layout questions. wt/host is clean at 6f4032a.
- HOST-20 answered: a count-0 base sits only at originEnd (genesis/join/import); offsets LOGICAL; indexCount counts every entry; HOST-65's RunFrom scope = Stores keeping their whole index. I land HOST-65 AFTER HOST-64.
- Cancel op (cv 01a15543-39fd) agreed with PROTOCOL-22: Op.cancel code 7 on .host; payload = Protocol.cancelEvent sig call (tag 2 included), parsed by Command.cancelParts, byte0 ≠ eventCancel refused like an undecodable submit; Host: decodeCall, journaled txId → ok+receipt, else Receive.cancel (.recorded commits, refused cancelled final; .declined nothing). ONE commit (every_op_has_a_row): PROTOCOL-22 writes Table/Verb/Machine/Rows and LANDS; I hand it hbox logs/host18-cancel.patch. Order: KERNEL-26, HOST-64, P planting rows, cancel.
- HOST-65 BUILT GREEN on HOST-20's tree (wt/host = 6f4032a + wt/host19's 54 files copied + HOST-65): Host lib + host-sim; seeds 1–3 ALL PASS (logs/host18-seeds65.log); plant-base-past-origin PASS, RED with the arm disabled. HOST-65 delta over HOST-20's tree: hbox logs/host18-host65-on-h20.patch (local h18/host65-on-h20.patch; HOST-20 base copy h18/h20.orig). Decision draft local h18/dec65.md. Second-agent read running. ROOT HOLD: no new scripts/commit until GATES-22's hash; and HOST-65 lands after HOST-64.
- HOST-65 second read: LAND-WITH-FIXES, all taken (step-count half restored as Not proved; HOST-25/HOST-64 header pointer; plant reads the forged base's offset). Rebuilt green (logs/host18-b65f.log), host-sim 2 ALL PASS. Final delta: hbox logs/host18-host65-on-h20.patch; decision logs/host18-dec65.md. READY; lands after HOST-64 and GATES-22 (ROOT hold). Message still to write (SIZE lines: Host lines, theorems +5: RunFrom.append, lastFrameFault_none_off, openWith_originEnd, page_beforeLog_origin; RunFrom is a Prop def).
- KERNEL-26 (aa21b8d4f926a4787) asked YES for two Host/Proofs/Refine.lean edits (recordedBy_of_judge; host_step_folds_tooth_censor gains hk : r.cancel.size = 0, cancels covered by audit_cancel_forged). YES given with conditions (statement change named; CROSS-LAYER line).
- KERNEL-26's kernel! LANDED 7a1cdd7. wt/host moved there (HOST-20+65 tree saved as logs/host18-h20plus65-full.patch + -untracked.tgz; HOST-65 delta is logs/host18-host65-on-h20.patch).
- HOST-66 = the cancel Host op (cv 01a15543-39fd), BUILT GREEN on 7a1cdd7: hbox logs/host18-cancel.patch (md5 50f06d4e…, applies alone on 7a1cdd7; 7 paths incl. PROTOCOL's Table/Proofs.Table/Command.Machine (cancelParts moved to Table), Host Serve/Proofs.Serve/Proofs.Refine/Sim.Run). host-sim 1–3 ALL PASS, host-file-sim 1 ALL PASS; plant-cancel-op RED with an emptied signature. Refine's op conjunct restated to `op.effect = .write`. Decision logs/host18-dec66.md. Second read running. PROTOCOL-23 (a8e94a9ff437436be) lands it with Verb/Machine/Rows.
- HOST-66 second read LAND-WITH-FIXES, taken (generated.rs is PROTOCOL-23's half; docs; handle_commit tied to the frame; unjudged tooth widened to writing ops; plant names). Final patch logs/host18-cancel.patch md5 7c575f8b…; seeds 1–3 ALL PASS. Sent to PROTOCOL-23 with the reply-semantics warning (recorded cancel = `refused cancelled`; `ok` = already admitted). PROTOCOL-23 carries the cancelPagePlant `cancelForged` line under my agreement.
- STATE (HOST-18, 2026-10-20): waiting on HOST-64 (HOST-20's lander, green, displaced twice) and PROTOCOL-23's HOST-66 landing (they hold logs/host18-cancel.patch). wt/host = 7a1cdd7 + HOST-66 (uncommitted, green). NEXT when HOST-64 lands: rebase HOST-65 onto it: `git checkout -f --detach main` in wt/host (HOST-66 is saved as the patch), then `git apply --3way logs/host18-host65-on-h20.patch` (if HOST-20's landed tree differs from wt/host19's copy, port by hand: the edits are lastFrameFault's originEnd arg + count-0 arm, RunFrom in StoreIndex, openWith_originEnd/lastFrameFault_none_off in Coherence, genesisImage_opens `hoe` + `eq_true hoe`, plant-base-past-origin), rebuild Host + host-sim, seeds 1–3, red control (arm `if originEnd = originEnd`), then scripts/commit with logs/host18-dec65.md appended to decisions/host.md; message needs SIZE lines (run gates/size.py) and no cross-layer (Host-only).
- LANDED eb7028d (host!, HOST-64), 2026-10-20.
  - Judge GREEN three times, displaced twice, then landed by CAS. The earlier reds were all fixed:
    - a missing SIZE: Rust lines (generated) line;
    - the waste re-pins (seal +16 B per base; rowbar 1.064 -> 1.066; staleBase 5.251 -> 5.259 in Protocol/Rows/Run.lean);
    - client/src/generated.rs re-emitted (61/62);
    - rustfmt on grain.rs;
    - a broker load flake (12/12 on re-run).
  - Mid-landing I adapted 1d542f1's Host/Proofs/Refine.lean (header input) and PERF-12's Bench/WorstCut{,Retires}.lean (Writer API).
  - Hash sent to ROOT, PROTOCOL-23 (planting rows next), HOST-18 (HOST-65 builds on it), OPS-6 (RUNBOOK, Units retain) and PERF-6 (91,914,474 prose).
- FOR HOST-21:
  - `host import --origin` with PROTOCOL-61 (proposed refusal `wrongWorld`);
  - the trie-binding theorem request to KERNEL (equal roots => equal tries; start_carry_commits stops at roots);
  - StoreIndexes / page theorems for retained Stores (indexFrom > 0, Page.kept);
  - `Segs.read` = the logical extract, as a theorem;
  - rotate's early return reusing a header unchecked (fails closed);
  - the writer-life induction as one theorem.
- OPS-6's Ops side of HOST-64 is on main as 7790f68:
  - Node.retain renders `host serve --retain N`;
  - checkRetain refuses retainBelowFloor and retainOnFollower;
  - checkRetain_sound;
  - RUNBOOK §2–§5 and the archive role.
  The Units `--retain` item is CLOSED for HOST-21.
- PERF-6 measured eb7028d. The worst-cut shapes are 18.661 / 30.595 / 32.217 / 20.182 and worstworld 2.000, all unchanged, so my Writer-API edits to Bench moved no count. The three prose updates to 91,914,474 are staged behind ROOT's hold.
- ⚑ HOST-65 LANDED 273adb3 (fast path). ROOT and PROTOCOL-23 told. HOST-66 with PROTOCOL-23 to land.
- HOST-66 re-cut on 273adb3 (applies clean, builds, host-sim 1 ALL PASS): hbox logs/host18-cancel-273adb3.patch md5 83c3f961…; PROTOCOL-23 (a8e94a9ff437436be) lands it. wt/host = 273adb3 + HOST-66 (uncommitted; it is PROTOCOL-23's to land: do not commit it from wt/host).
- Filed for KERNEL (ROOT's word): cv 01a15849-3ae0 trie-binding theorem (equal roots ⇒ equal tries).
## HOST-19 HANDOFF (written by HOST-18 near its context line; nothing of mine unlanded except HOST-66, which PROTOCOL-23 lands)
- Landed by HOST-18: 6f4032a HOST-63 (with the rowbar re-pin 1.064), 273adb3 HOST-65 (entry 0 at the origin end; count-0 arm). HOST-66 (cancel op) built and handed off; if PROTOCOL-23's landing has not happened, ask it (a8e94a9ff437436be); semantics agreed: recorded cancel = `refused cancelled` (final), `ok` = already admitted, `declined NAME`, `uncertain forgotten`.
- NEXT (ROOT 10-20, cv 01a1583d-864c, HOST-64's named follow-ups), one `host:` each or grouped, fast path:
  1. `host import --origin` with PROTOCOL-23's PROTOCOL-61: agree the refusal name first (wrongWorld proposed).
  2. `Segs.read` = the logical extract, as a theorem.
  3. StoreIndexes for retained Stores (indexFrom > 0): the run begins at the oldest kept file's header (start, indexCount) per HOST-20; StoreIndexes today covers whole-index Stores only (RunFrom from the origin end).
  4. rotate's early-return header reuse.
  5. the writer-life induction as one theorem.
  6. HOST-65's named gap: entry 0's step count = the first World's (0 at genesis, the import's step). Idea: carry the origin World's steps in the header/base at genesis (HOST-64's header binds steps for its own file) or state it relative to genesisImage's base.
  Still named from HOST-62: the loop's push between opens (Indexes.snoc is its pure core); the entry chain field. HOST-50's five WEAKs: HOST-64 added a checkpoint mechanism and file rotation, so re-check the "a third checkpoint" and "no Tail rotation" triggers against eb7028d.
- Scratch: local scratchpad h18/ (drafts, msgs, decisions); hbox logs/host18-* (host18-b.sh build helper: `host18-b.sh NAME targets…`, SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2; host18-seeds65.sh = host-sim + host-file-sim seeds 1–3).
- Gotchas met: an ssh '…' with backticks/heredoc breaks zsh → write python locally, scp, run; `by_contra` is not available (no Mathlib) → by_cases; a red control must keep every variable used (warningAsError lint); the size pre-flight is `python3 gates/size.py . --write` then `git diff SIZE.md` then `git checkout SIZE.md`.
- PERF-6's prose follow-up landed as 744d00c (waste.tsv worstworld text, decisions/perf.md, RUNBOOK §8: baseRecordMax 91,914,474). All HOST-64 cross-layer follow-ups are done except PROTOCOL-23's planting rows and HOST-18's HOST-65.

## HOST-19 (the second; successor of HOST-18; 2026-10-20, hbox wt/host19b, own cargo target; local mirror scratchpad h19b/)
- Helpers: hbox logs/host19b-{b,bg,seeds,lt}.sh (6G recipe; bg writes logs/host19b-NAME.pid and a BUILD-RC marker), local h19b/push.sh (tree vs orig → wt/host19b).
- HOST-67 BUILT (items 1, 2, 4 of cv 01a1583d-864c): `host import --origin HEX --nonce HEX32` (Carry.Pin; `carryMismatch wrongWorld`, agreed with PROTOCOL-23; import_trusted_pinned), `Segs.read` → pure segRead/segGather + Host/Proofs/Segs.lean (segRead_logical, segRead_whole = the retain=∞ identity), rotate reuse checks headerFault else positionUnfit (+ `STATUS rotate … header=NAME`; sealed_opens_reused). Plants plant-import-origin / plant-rotate-reuse, both RED with their check disabled. All targets built, seeds 1–3 ALL PASS, store-plants ALL PASS, rows carry PASS. Second read LAND-WITH-FIXES, six taken. Landing: logs/host19b-land67.log (pid file logs/host19b-land67.pid), msg logs/host19b-msg67.txt. Carries PROTOCOL-23's one Loopback line (CROSS-LAYER).
- PROTOCOL-61 (PROTOCOL-23): Invite.Start agreed (genesis | carried origin name nonce from height chain; one startInput encoding; accept genesis-only + acceptStart). I proposed `host join STORE INVITE KEY [IN]` does the carried import itself (pin from the invitation). Host prints: genesis/join `input` = startInput, import prints `start HEX`. Waiting on its Start hash/patch after its PROTOCOL-63/62 landings.
- Remaining queue: (3) StoreIndexes for retained Stores (design: StoreIndexesKept, run from `if rf = 0 then originEnd else rf`, entries from k0, Indexes.drop), (5) writer-life induction, (6) entry 0's step count, then the HOST-50 WEAK triggers vs eb7028d. Not done: a store-plants row for the --origin CLI parse (Ops's; ask OPS).
- HANDOFF NOTES for items 3 and 6 (designed, not built). One statement change covers both: `StoreIndexes … s₀` with `RunFrom L at_ (o₀, s₀)`.
  - Arms: `[]` ⇒ at_ = o₀ ∧ (mark b.world).1 = s₀; `e :: _` ⇒ e.offset = o₀ ∧ e.steps = s₀.
  - (6) k0 = 0: o₀ = originEnd. s₀ is discharged at genesis/import as w₀.steps (0 at genesis; the import's height by importWorld_steps). Kept by append/cut_open/sealed: entry 0 is fixed. When L = [], openWith_indexes' head fact makes the open's first entry (b.offset, steps of b.world) = (o₀, s₀).
  - Then page_beforeLog_origin gains `start < s₀`: beforeLog refuses only steps before the first World.
  - (3) Retained Stores: the kept run is entries k0.. read at logical positions k0+i (Page.kept's `get (k0+k)`), with (o₀, s₀) = (rf, steps at rf).
    - The drop lemma: a base sealed at P counts ix'.count = every entry before P (seal_facts: ix'.count = sealed.count + index.size, and the run ends at P). So after later seals, entry ix'.count sits at P (the open's first new entry is at b.offset, the openWith_indexes head fact).
    - Hence keepFrom's (rf, k0 = header(rf).indexCount) points entry k0 at rf; Indexes.drop k0 gives coherence.
    - Page theorem: page_nonempty over Page.kept by shifting `get`.
  - Price it before building: Coherent gains s₀ at every consumer (page_nonempty, coherent_reader, sealed_indexes_deployed, genesis/import_indexes).
- (5) writer-life induction: compose genesis_trusted/import_trusted → openWith_trusted → sealed_trusted → … as one theorem over a list of (open, seal) events, stated over the abstract writer events. The loop's push between opens is still read off (HOST-62's item), so state it over opens and seals only, and name that.
- ⚑ HOST-67 LANDED 832a815 (fast, CAS). ROOT and PROTOCOL-23 told. wt/host19b now sits at 832a815, clean.
- PROTOCOL-61 plan agreed (PROTOCOL-23): it cuts the Protocol half (Invite.Start, accept genesis-only + acceptStart) after its 63 and 62 landings and sends a patch path. HOST writes the Host hunks and hands them back; PROTOCOL-23 lands one commit with them (HOST-66 pattern). The hunks: `host join STORE INVITE KEY [IN]`, where a carried start runs acceptStart then importWith under the signed name, nonce and `.origin`; genesis/join print `input` as startInput and import prints `start HEX`; Proofs.Cli join_genesis_iff plus a carried twin; Refine.
- STOPPED at the context line. NEXT for HOST-20 (the next HOST): PROTOCOL-61 Host hunks when the patch arrives; then items 3, 6 (one StoreIndexes s₀ change, notes above) and 5; then the HOST-50 WEAK triggers vs eb7028d.

## HOST-22 (successor of HOST-19 the second; 2026-10-20, hbox wt/host22 = wt/host19b RENAMED by `git worktree move` from main's repo: warm .lake kept, no copy, no rebuild; own cargo target = the worktree's target/; local scratchpad h22/orig = a read-only rsync mirror of main's Host/, decisions/, scripts/, gates/)
- Helpers: hbox logs/host22-{b,bg,seeds,lt}.sh (HOST-19's with paths swapped; 6G/2-thread recipe; bg writes logs/host22-NAME.pid + BUILD-RC marker).
- Queue: (A) PROTOCOL-61 Host hunks when PROTOCOL-23 sends its patch path; (B) items 3+6 as one StoreIndexes s₀ change (premise spread sent to ROOT before building: ONE landed theorem gains a hypothesis, sealed_indexes/_deployed's `hkeep`; page_nonempty/page_beforeLog_origin/coherent_reader take the base read `hb` to name k0; run start = `max b.retainedFrom originEnd`, not HOST-19's `if`, so count 0 needs no premise); (C) writer-life induction over (open, seal) events; (D) HOST-50 WEAK triggers vs eb7028d.
- Decisions taken so far: `max rf originEnd` for the run start (derivable at count 0 from the base codec's keep refinement + the open's count-0 arm); `host check` indexClean gains "first kept entry's steps = oldest header's steps" (a check added; plant in host-file-sim).
- ROOT GO on (B) with two conditions: hkeep's discharge as THEOREMS in the same commit (sealed_indexes_same; keep_of_header + keepNames_append/cut/seal), and the decision names the theorems that gained a hypothesis (sealed_indexes, sealed_indexes_deployed: hkeep) and the three restated over the deployed pager with hb (page_nonempty, page_beforeLog_origin, coherent_reader), plus the `max` line. Plant lines from a real run (rule 16).
- (B) BUILT at the file level: Host/Proofs/StoreIndex.lean (rewritten: RunFrom pair form, StoreIndexes s₀ from indexFrom, KeepNames, openWith_run, sealed_reads_new/sealed_reads, sealed_indexes[+_same], keep_of_header, keepNames_mono/append/cut/seal, coherent_reader/page_nonempty/page_beforeLog_origin over Page.kept, sealed_indexes_deployed[+_same], keepNames_seal_deployed, genesisImage_base_read, genesis/import_indexes at w₀.steps), Host/Proofs/Coherence.lean (build_error_shape, kept_ok, kept_beforeLog, kept_checkpointed; header prose), Host/Base.lean indexClean (+steps: first kept entry's steps = oldest header's), Host/Check.lean (oldest.steps), Host/Proofs/Index.lean (indexClean_none +conjunct, indexClean_first_steps tooth), Host/Sim/Run.lean (5 call sites), Host/Sim/File.lean (plant-first-entry-steps-{kept,full}, plant-index-from-off). Local copies: scratchpad h22/new/. Stage-A build running: logs/host22-bA.log (pid logs/host22-bA.pid); host-file-sim + Hosting (16G, NOT during a bench window: a judge's benches were running at 05:30Z) still to build.
- (B) MEASURED green on wt/host22: all default targets (Hosting at 16G, bench window closed), seeds 1–3 ALL PASS, store-plants 76/76, host-file-sim seed 1 97 PASS; plant-first-entry-steps-{kept,full} RED with the check disabled (logs/host22-red68.log); plant-index-from-off's expectation corrected to the measured `indexCorrupt` (the check opens first). Decision draft: scratchpad h22/decision-68.md. Second-agent read spawned (aa756632f90d43e61). Hosting build pid file logs/host22-bH.pid (done, RC=0). Store-plants dir logs/host22-sp-run1719665 (mine; delete at handoff).
- (B) second read LAND-WITH-FIXES (6, all to the decision text; none to statements), taken. HOST-68 appended to decisions/host.md on wt/host22; landing launched 05:42Z: scripts/commit PID 1852135 (logs/host22-land68.pid, log logs/host22-land68.log; the first pid written was the parent shell's, corrected). cv task opened 01a158b0-d455 (plant reaching keptHeaders' `indexCorrupt from`). (C) drafted locally while the landing runs: h22/new/Host/Proofs/Trusted.lean adds WriterLife (inductive Prop: open → admitted fold (the read-off push, as a premise) → Base.file; refl), link_trusted, writer_life_trusted, genesisImage_trusted, genesis_life_trusted, import_life_trusted, life_opened_size_le, life_refutes_potential (tooth). Push + build after the landing.
- ⚑ HOST-68 LANDED 80419cf (fast judge; built Protocol Host Hosting Emit Bench Ops + exes; cargo none). ROOT told. cv 01a1583d-864c noted (3, 6 closed). wt/host22 at 80419cf clean. Next: (C) HOST-69 build, (D) HOST-50 WEAKs.
- (C) HOST-69 second read LAND-WITH-FIXES (3 prose; the reader found `host_run_kept` is the per-batch fold bridge — cited), taken; decision appended; landing launched (logs/host22-land69.{log,pid}, PID = scripts/commit's own via land69.sh with stdin from /dev/null).
- (D) FINDING: HOST-50 WEAK (v)'s trigger FIRED at HOST-64 (segment rotation + drops). Tail follows rotation through Segs (plant-tail-rotation PASS, new) but a tail standing in a file a retention unlinked threw `open: No such file or directory (errno 2)` out of Segs.read (captured, host22-fsD.log) — FIXED in Host/Store.lean: Segs.size/Segs.read refuse `missing seg.<o>.log` by name (plant-tail-dropped PASS: `missing seg.2189.log`). Both in wt/host22 uncommitted (Store.lean, Sim/File.lean), to land as HOST-70 with the WEAK re-check decision after HOST-69 lands. Other WEAKs: locate unchanged since a2996f7; two real checkpoints (+ the Run.lean:949 test double); HOST-42's closed by HOST-51.
- ⚑ HOST-69 LANDED 7473d77 (its message's Host-lines SIZE line holds `+__N__`: a macOS `sed -i` failed silently; ROOT: never stop a judge; HOST-70's message + decisions/host.md HOST-69 carry the real `16701 → 16816`; ROOT adds lane rule 18: grep every message/generated file for placeholders and the pipeline output for `sed:`/`error` before launch).
- (D) HOST-70 built+measured: Segs.size/read `missing` guards; plants tail-rotation (RED: size not learning successors), tail-dropped (RED: the pre-guard exception), segs-dropped (RED: read guard off, host22-red70b.log); seeds 1–3 + store-plants 80/80 green; second read LAND-WITH-FIXES (3) taken. Decision h22/decision-70.md, msg h22/msg70.txt (SIZE placeholders __D__/__T__ to fill from the pre-flight — grep before launch!), launcher land70.sh.
- HOST-70 landing launched (scripts/commit PID 1955285, logs/host22-land70.{log,pid}); message and decisions grepped for placeholders (0) before launch. PROTOCOL-23 asked for PROTOCOL-61's patch path (or to say it is not coming soon). After HOST-70 lands: `cv task done 01a1583d-864c`; then only (A) remains in my queue → ask ROOT for the next item if PROTOCOL-23 is not ready.
- ⚑ HOST-70 LANDED f48965e. cv 01a1583d-864c DONE. ROOT told (queue = (A) only; context ~430K). wt/host22 clean at f48965e.

## HOST-22 HANDOFF (written by HOST-22 at its context line, 2026-10-20; nothing unlanded)
- LANDED by HOST-22 (all `host:`, fast judge, no flag day): HOST-68 80419cf (StoreIndexes s₀ + retained Stores + `host check` first-entry steps; cv 01a1583d-864c items 3, 6), HOST-69 7473d77 (WriterLife, writer_life_trusted; item 5; its MESSAGE has a `+__N__` SIZE placeholder — corrected in f48965e's message and decisions/host.md HOST-69), HOST-70 f48965e (HOST-50 WEAK re-check; Segs.size/read `missing seg.<o>.log`; plants tail-rotation/tail-dropped/segs-dropped). cv 01a1583d-864c DONE; follow-up 01a158b0-d455 open (a plant reaching keptHeaders' `indexCorrupt from`).
- NOT DONE, the only queue item: (A) PROTOCOL-61's Host hunks. Asked PROTOCOL-23 (a8e94a9ff437436be) for its patch path; no reply at handoff. The agreed shape: `host join STORE INVITE KEY [IN]`: a carried start runs acceptStart then importWith under the signed name, nonce and `.origin`; genesis/join print `input` = startInput, import prints `start HEX`; Proofs.Cli join_genesis_iff + a carried twin; Refine; hand the hunks back by path, PROTOCOL-23 lands ONE `protocol:` commit (HOST-66 pattern; a CROSS-LAYER line names it).
- Tree: hbox /tank/dregg-build/nanodregg/wt/host22 (= HOST-19's wt/host19b renamed; warm .lake; own cargo target) clean at f48965e. Helpers logs/host22-{b,bg,seeds,lt}.sh (6G/2-thread recipe; `MEM=16G` for Hosting only, after checking `ps -eo args | grep bench-` shows no judge bench). Landing pattern that WORKS: a launcher script (logs/land70.sh: cd on its own line, `nohup bash -c 'exec scripts/commit …' > LOG 2>&1 < /dev/null &`, `echo $! > PID`) — an inline `cd … && nohup … &` inside ssh backgrounds the whole list and records the wrong pid (happened at HOST-68; corrected by hand).
- Gotchas met this session: macOS `sed -i 's/…/…/' file` FAILS ("invalid command code") — use python for message edits and GREP THE MESSAGE FOR PLACEHOLDERS BEFORE LAUNCH (rule 18); `cv task note "… <o> …"` in zsh is a redirection (angle brackets eat the note); a red control's mutation on a Bool needs `|| true` (`∨ true` does not compile); `show` on a goal with structure-literal projections can time out — use `dsimp only`; `exact` across `entryBytes (keys.forStore …)` vs `entryBytes keys` is fine, `rw` is not (rewrite `entryBytes_forStore` first); `injection` timed out where `Option.some.inj` was instant; a second `obtain ⟨…, rfl⟩ := genesisImage_ok h` fails (img already substituted) — do it once at the top.
- Local scratchpad (this session's; gone with it): h22/new (the landed sources), h22/decision-{68,69,70}.md, h22/msg{68,69,70}.txt.
- Next for HOST-23: (A) when PROTOCOL-23 sends the path; else ask ROOT. Candidates seen while reading: `keepNames_*` chain is piecewise, never composed end-to-end for a real retained Store (named in HOST-68's decision: Store.keepFrom read off); the `read` guard's TOCTOU (named); 01a158b0-d455.

### HOST-22 HANDOFF, part 2 (ROOT's ask): the PROTOCOL-61 Host hunks, designed in full against main f48965e (real signatures pasted; PROTOCOL-23's Protocol half is NOT landed — it sits behind a full judge; write the hunks against its patch when it comes)
What exists today (f48965e), verbatim where it matters:
- `Host/Cli.lean`: `structure JoinFx (m) where key : m (Option Digest); genesis : Digest → World D → m (Except (StoreFault (Record.Fault (Reject D))) Unit); refuse : Status → String → m UInt32; report : List String → m Unit`. `def joinWith {m} [Monad m] (fx : JoinFx m) (inviteHex keyHex : String) : m UInt32` = ofHex INVITE (`usage invite`), ofHex KEY (`usage key`), `Protocol.Invite.accept X trusted inv` (`.inputs r` → `usage r.name`; other → `inviteRefused NAME`), `budgetFault w₀` (refused by its own status), `fx.key` (`entropy`), `fx.genesis key w₀`, then `fx.report (genesisLines w₀ i.nonce i.founders.length ++ [s!"sponsor {i.sponsor.toHex}", s!"input {Protocol.Text.toHex (Protocol.Invite.inputBytes X i.name i.nonce i.allowance i.founders)}"])`. `joinVerb store inviteHex keyHex` instantiates it at IO (key = 32 random bytes, genesis = `Host.genesis store key (Keys.ofKey key shapes) c world recorder.mark w₀`). Dispatch: `| ["join", store, inv, key] => joinVerb store inv key`.
- `structure ImportFx (m) where nonce : m (Except Status ByteArray); readIn : m (Except (StoreFault …) ByteArray); key; genesis; reopen : Digest → m (Except (StoreFault …) (World D × m Unit)); refuse; report`. `def importWith {m} [Monad m] (fx : ImportFx m) (name : String) (pinHex : PinArg) : m UInt32` = pin parse (`usage digest|origin`), nonce, readIn (`carryMismatch tooLarge` past `carriedMax`), `Carry.importWorld X Codec.Deployed.digestCodec name.toUTF8 nonce pin bytes` (`(s, n)` refusals incl. `carryMismatch wrongWorld` for `.origin o`), budgetFault, key, genesis, reopen + `carryMismatch reopen` compare, then `fx.report [s!"origin {back.origin.toHex}", s!"nonce …", s!"from {r.head.fromOrigin.toHex}", s!"height {back.height}", s!"chain {back.chain.toHex}"]`. `inductive PinArg | digest (hex) | origin (hex)` with `PinArg.parse : PinArg → Option (Carry.Pin D)`; `inductive Carry.Pin (D) | digest (want : Digest) | origin (o : D)`.
- `Host/Proofs/Cli.lean`: `theorem join_genesis_iff (inviteHex keyHex : String) (keyR : Option Digest) (k : Digest) (w : World D) : joinWith (m := Except (Option (Digest × World D))) { key := pure keyR, genesis := fun k₀ w₀ => throw (some (k₀, w₀)), refuse := fun _ _ => pure 1, report := fun _ => pure () } inviteHex keyHex = .error (some (k, w)) ↔ ∃ inv trusted i, Protocol.Text.ofHex inviteHex = some inv ∧ Protocol.Text.ofHex keyHex = some trusted ∧ Protocol.Invite.accept X trusted inv = .ok (i, w) ∧ budgetFault w = none ∧ keyR = some k` (proof: unfold, cases on the two ofHex, `simp only [bind, Except.bind, pure, Except.pure]`, `repeat' split`, `simp_all`). `import_genesis_iff` is its import twin (line 37). `join_budget_reaches` (176) and `genesis_budget_reaches` (109) discharge HOST-59's premises.
- `Protocol/Invite.lean` (landed): `structure Invitation (D) where name nonce : ByteArray; allowance : Nat; founders : List (ByteArray × D); pin : Thin.Pin; sponsor : D; key unsigned signature : ByteArray`; `def accept (X : Ctx D) (trusted bytes : ByteArray) : Except Refusal (Invitation D × World D)` = ofBytes (`badInvitation`), `inv.key ≠ trusted → notSponsor`, verify (`pinMismatch`), `genesis X name nonce allowance founders` (`.inputs r`). `inputBytes X name nonce allowance founders` is what `input` prints.
What PROTOCOL-61 adds (agreed with PROTOCOL-23 by HOST-19; CHECK ITS PATCH FIRST, names may differ): `Invite.Start` = `genesis` (today's inputs) | `carried origin name nonce` (from a height chain: the sponsor's exported origin pinned); ONE `startInput` encoding covering both (the line `host genesis`/`host join` print as `input`); `accept` stays genesis-only; new `acceptStart X trusted bytes : Except Refusal (Invitation D × Start D)` (or similar) that verifies the signature and returns the carried start without a World.
THE HOST HUNKS (hand back by path; PROTOCOL-23 lands them in its ONE `protocol:` commit; HOST's CROSS-LAYER line names `Host/Cli.lean`, `Host/Proofs/Cli.lean`, `Host/Proofs/Refine.lean` as HOST-owned paths carried by PROTOCOL):
1. `Host/Cli.lean` dispatch: `| ["join", store, inv, key] => joinVerb store inv key none` and `| ["join", store, inv, key, inp] => joinVerb store inv key (some inp)`; `join` with a carried start and no IN → `refuse .usage "in"`; a genesis start with IN → `refuse .usage "in"` (one arity per start kind; say which in the usage text).
2. `joinWith` gains `(inPath : Option String)`: after ofHex INVITE/KEY, run `Protocol.Invite.acceptStart X trusted inv` (refusals as today: `.inputs r` → `usage r.name`, else `inviteRefused NAME`); match the start: `.genesis …` → exactly today's path (budgetFault, key, genesis, report with `input` = `startInput` of the genesis start — PROTOCOL's encoder replaces `inputBytes` in the print); `.carried o name nonce` → `importWith fx' name.toString? (.originRaw o)`: the cleanest is to add to `PinArg` (or beside it) a parsed form so `importWith` can take a `Carry.Pin D` directly — add `def importWithPin … (pin : Carry.Pin D)` and let `importWith` call it after parsing; the carried arm calls `importWithPin` with `pin := .origin o`, `fx'.nonce := pure (.ok nonce)` (the SIGNED nonce, never a fresh one: `carryOriginOf` hashes name+nonce, HOST-67), `fx'.readIn := read IN` (`carriedMax`-bounded, `readBounded`), and its report prefixed by `s!"sponsor {i.sponsor.toHex}"` and ending with `s!"input {startInput …}"`; import's own report keeps `start HEX`? — AGREED SHAPE: genesis/join print `input` (= startInput), import prints `start HEX` (the startInput of the carried start it just made) so a joiner can invite onward from either. So `importWith`'s report gains `s!"start {Protocol.Text.toHex (startInput (.carried back.origin name nonce))}"` for an `.origin` pin (and for `.digest`? print it too: the start is the same bytes; PROTOCOL-23 to confirm).
3. `JoinFx` gains what the carried arm needs: `readIn : m (Except … ByteArray)` (IN), `reopen` (import's compare), or build an `ImportFx m` from a `JoinFx m` plus the two — simplest: `JoinFx` extends `ImportFx` minus `nonce` (nonce comes from the invitation). Keep ONE effect record if PROTOCOL-23's patch lets `importWith` be called with a pre-parsed pin; the pure `joinWith` must stay a function of its effects so the iff theorems elaborate by `unfold; split`.
4. `Host/Proofs/Cli.lean`: `join_genesis_iff` restated with `acceptStart … = .ok (i, .genesis …)` in the ∃ (same proof skeleton; `simp_all [Prod.ext_iff, and_comm]` may need the new constructor added to the `simp` set); NEW `join_carried_iff`: genesis is reached with `(k, w₀)` EXACTLY when INVITE/KEY parsed, `acceptStart` returned `.carried o name nonce`, IN read as `bytes`, `Carry.importWorld X dc name nonce (.origin o) bytes = .ok (w₀, r)`, `budgetFault w₀ = none`, `keyR = some k` — the carried twin; its ← half is the tooth (a join that imports under a fresh nonce or without the origin pin makes the claim false). Also `join_carried_trusted`: from the ← half + `import_trusted_pinned` → `CheckpointTrusted o w₀` at the SIGNED origin (this is the "one premise named once" link HOST-67's decision deferred to PROTOCOL-61: the joiner's base is trusted at the invitation's origin).
5. `Host/Proofs/Refine.lean`: the start enumeration (`* a start — host genesis, host join (Protocol.Invite.accept) and host import`, line 18 and ~411) gains the carried join = `Carry.importWorld` under the signed pin; whatever theorem lists the three starts (grep `Invite.accept` in Refine.lean) gets the fourth arm, discharged by the same `importWorld_*` lemmas as import (HOST-67 generalized them over every `pin`, so the `.origin` instance is free).
6. Plant (host-sim or store-plants, OPS's row for the CLI parse is OPS's): a carried join with the signed nonce imports and reopens to the sponsor's World (origin = the pinned one); the same invitation with the head's exported origin flipped, or IN of another World, refused `carryMismatch wrongWorld`; a genesis-start join with IN refused `usage in`. RED with the pin dropped (`.digest`-less accept-all) as plant-import-origin's control.
The one thing to check first: PROTOCOL-23's `acceptStart` return type and whether `Start.carried` carries the NAME as `ByteArray` (Invitation.name is `ByteArray`; `Carry.importWorld` takes `name nonce : ByteArray` — no `String` round trip, unlike `importWith`'s `name : String` today; `importWithPin` should take `ByteArray`).
Open follow-up 01a158b0-d455: a host-file-sim plant reaching `Check.keptHeaders`' `indexCorrupt from` (re-seal the oldest kept header under the Store key with `indexCount ≠ indexFrom`, all else honest, so the open passes and keptHeaders refuses; RED with that arm disabled). Needs: `Header.bytes keys {h with indexCount := …}` as plant-header-position does, written over the oldest kept file's header (File.lean checkpointPlants has the copy/forge pattern at "the header plants").
wt/host22: clean at f48965e; helpers /tank/dregg-build/nanodregg/logs/host22-{b,bg,seeds,lt}.sh (usage in each file's header), launcher pattern logs/land70.sh; all my logs logs/host22-*. Nothing of mine left to delete (store-plants run dirs removed).
