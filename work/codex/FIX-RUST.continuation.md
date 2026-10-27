# FIX-RUST continuation (written by FIX-RUST at park, 2026-10-24 ~06:40 EDT)

Read first: /Users/ember/dev/redregg/work/codex/FIX-RUST.report.md (what landed, hashes, plants).
Worktrees: hbox /tank/dregg-build/nanodregg/wt/fixrust (land from here), local ~/dev/nanodregg-wt/fixrust
(edit here), hbox /tank/dregg-build/nanodregg/wt/fixrust3 (card-3 test tree, Lean built: emit-broker,
emit-hosting, emit-units, host, hosting-*). Own target dirs: wt/fixrust-scratch/target, target3.
SYNC TRAP (measured, cost me a false plant reading): rsync -a carries the LOCAL mtime, older than a
build, so cargo does not rebuild. Use the checksum, no-times sync
(scratchpad/fixrust/sync.sh = rsync -rlpc). The shared scratchpad is shared with sibling lanes: use
your own subdir.

## State at park (see the report's 08:15 entry: card 1b fix also in flight)
- Card 1 (A6, CLIENT-37): LANDED a7bccd8.
- Card 2 (A19, CLIENT-38): in the FULL landing queue (gates/*.py changed) behind fixhost's ticket 221;
  lander pid file wt/fixrust-scratch/commit2.pid, log commit2.log, msg msg2.txt. If REFUSED: read the
  log's PRE-PUSH RED lines (it already failed once on SIZE lines + a runs.tsv drives column; both fixed).
- Card 3 (A18, CLIENT-39): BUILT and planted GREEN/RED in wt/fixrust3 (plants3.log, plants3c.log,
  t7.log, t8.log); NOT landed. It overlaps card 2's files (mux.rs, keybroker.rs, nd-members.rs,
  BrokerExit.lean, Ops/Units.lean, launcher/tests/common/mod.rs), so it lands AFTER card 2:
  1. after card 2 lands (wt/fixrust moved to the new main), sync local -> wt/fixrust with sync.sh;
  2. re-emit in wt/fixrust: `lake build emit-broker emit-units` then
     `.lake/build/bin/emit-broker X; emit-units DIR` into scratch and copy (the emitters refuse an
     existing path: never `--help`, it writes a file named --help);
  3. message: CLIENT-39 is already appended to decisions/client.md (local); SIZE lines will be asked for
     (Rust lines, client library, nd-members, Lean Hosting/deployed/tooling, generated); the client
     library and nd-members ceilings will need rows raised again by exactly the measured amount;
  4. paths: client/Cargo.toml client/src/{frame,sockets,mux,fsx,attempt}.rs client/tests/{sockets,custody,attempt}.rs
     launcher/src/residents.rs launcher/src/bin/{keybroker,nd-members}.rs launcher/tests/{broker,members}.rs
     launcher/tests/common/mod.rs launcher/src/broker_generated.rs Hosting/BrokerWire.lean Hosting/BrokerExit.lean
     Emit/Broker.lean Ops/Units.lean deploy/units/EXITS.md decisions/client.md gates/ceilings.tsv SIZE.md is generated.
  Subject prefix `client:`; --cross-layer naming HOSTING, OPS, CODEC.

## Card 4 (A17, law 2) — NOT STARTED; the design, decided:
1. Bounds/layout widths from Lean, tied at compile time:
   - Protocol/Frames.lean: `frameLenBytes := Codec.Stream.u32.size 0` (the socket frame IS
     `Stream.bytesOf frameBytesMax` of a nonempty body `op ‖ payload`; bytesOf = u32le len ‖ bytes,
     Codec/Stream.lean:171). Host/Wire.lean: `connBytes := Codec.Stream.u32.size 0`, and
     `bodyMax := frameBytesMax + connBytes`. Emit FRAME_LEN_BYTES, CONN_BYTES, CHILD_BODY_MAX
     (Emit/Rust.lean `bounds`, line ~92).
   - Rust: frame.rs HEADER -> g::FRAME_LEN_BYTES with `const _: () = assert!(FRAME_LEN_BYTES as usize
     == size_of::<u32>())` (a Lean width change then fails the Rust BUILD); mux.rs CONN, stdio.rs:93,100,109,
     join.rs:76-81 -> CONN_BYTES / CHILD_BODY_MAX.
   - mux.rs close_frame (~:155-166): the `u32::try_from(..).unwrap_or(u32::MAX)` becomes a refusal: build
     every child frame through ONE `pub fn child_frame(conn, op, payload) -> Result<Vec<u8>, FrameError>`
     (write_body's checks), used by the mux and by the vectors test.
2. Custody rotation record (custody.rs:531,541-549, `u64le ‖ 32 ‖ 32`, read as 72): a Lean layout
   `Protocol.Table.rotationLayout := [.u64 "attempt", .bytes "incoming", .bytes "pending"]` emitted by
   structFor (name `ArmedRotation`), plus `rotationBytes` (its size at 32-byte keys, 8+4+32+4+32 = 80, with a
   theorem) emitted. FLAG DAY: the rotation file is 80 bytes; a 72-byte one refuses (Length) by name.
3. Vectors (encode in Lean, decode in Rust and back) as new sites in Emit/Vectors.lean `sites` (~:735):
   "wire/frame" (Stream.bytesOf frameBytesMax, bodies 1..N), "wire/child" (Stream.bytesOf Host.bodyMax,
   bodies conn‖op‖payload, print via Host.decodeBody as `ok conn=N op=N payload=HEX`), "client/rotation"
   (the layout codec, print `ok attempt=N incoming=HEX pending=HEX`). Print formats chosen so Rust can
   render the same text. `lake exe codec-vectors --write gates/codec-vectors.tsv` draws them (new sites
   only; vectors.py allows new sites). A Rust test (client/tests/frame.rs or a new vectors test with a
   runs.tsv row if the runs gate demands one) reads gates/codec-vectors.tsv via devtools::repo(),
   decodes each row with read_body / the mux split / generated ArmedRotation, renders, compares the
   text, re-encodes, compares bytes. Plant: swap two fields in the Rust decode.
4. Receipt line prefixes (attempt.rs:57-59; Machine.lean:963 receiptText): Lean defs
   `receiptLinePrefix`/`headLinePrefix`/`settleLinePrefix` used BY receiptText and emitted; attempt.rs and
   the tests' stand-in follow (client/tests/attempt.rs:23-25, run.rs:52-58) use the emitted ones.
5. Socket names: Hosting/Plan.lean has brokerSock/memberSock/followSock (:88,:93,:146); add hostSock
   (Ops/Units.lean:528,653 spell "host.sock" as String: use the Lean name there too). Emit
   FOLLOW_SOCK/HOST_SOCK/MEMBER_SOCK/BROKER_SOCK into client/src/generated.rs (launcher reads client's).
   Rust: nd.rs:72-76, nd-members.rs:189-190,458-459,602,621,651-652, keybroker.rs:514,518.
6. nd-members restart constants (nd-members.rs:60-63, comment cites the deleted nd-member@):
   Ops/Units.lean restartSeconds (:211), startBurst, startIntervalSeconds -> emit-broker; TICK (200 ms,
   nd-members.rs:55 and keybroker.rs:80) -> a Lean `Broker.Bounds.tickMs`, emitted, both use it.
7. grain_name_ok (launcher/src/lib.rs:136): Lean labelOk = Path.clean && labelByte (Hosting/Plan.lean:50,61).
   Emit LABEL_BYTES (the bytes labelByte accepts); Rust = generated path_clean && all bytes in LABEL_BYTES.
8. "signal = code ≥ 128": residents.rs decider_end and grain-launch.rs:113-116,387-395 restate it
   unconditionally; use nanodregg_sandbox::killed_by_signal (the platform fact) — Rust law 1, no Lean.
9. foreign.rs X1b (client/tests/foreign.rs:342): assert the refusal NAME, and fix the :352-354 comment
   (F16) to what the test checks.
10. resident_bell's 2048 sequential writes (launcher/tests/resident_bell.rs:589-592): look for a batch
    write or height-advance helper (none known); if none, leave and say so in the report (do not invent
    a test-only patience: LANG's call, READ-RUST §4).
Decision: CLIENT-40 (critique + meta-critique). The generated-file gate covers the re-emits.
