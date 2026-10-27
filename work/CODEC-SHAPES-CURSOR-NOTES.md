# CURSOR continuation notes (item: ByteArray cursor for StreamCodec)
Tree: hbox /tank/dregg-build/claude-lanes/codec-shapes/src, branch codec-shapes, HEAD 13cc5a51.
Local read-only mirror of *.lean: scratchpad/mirror (session b3795e84).

## Design chosen
- StreamCodec gets 3 defaulted fields after encode_decodePrefix:
  decodeAt : ByteArray → Nat → Option (α × Nat) := cursorOfPrefix decodePrefix
  decodeAt_spec : ∀ bytes start, decodeAt bytes start = cursorOfPrefix decodePrefix bytes start := by intro _ _; rfl
  cursorNative : Bool := false   (dispatch bit: true iff decodeAt is a native loop all the way down)
  cursorOfPrefix d b s := (d (b.data.toList.drop s)).map fun r => (r.1, b.size - r.2.length)
- Hand instances keep the default (materializes the suffix: O(size) per call => NOT native).
- toLawful gets @[csimp] toLawful = toLawfulCursor: decode l := if cursorNative then decodeCursor l.toByteArray else list path.
  So every fully-native codec tree decodes through the cursor everywhere, statements unchanged; a tree with a hand
  instance stays on the List path (no quadratic suffix materialization).
- decodeBytes : ByteArray → Option α (explicit entry), decodeBytes_eq : = toLawful.decode bytes.data.toList.
- DurableCheckpointCodec.lean holds CODEC-SHAPES' uncommitted hunk: do not commit that file (csimp on toLawful covers Framed.decode).

## Progress (22:40–23:10)
- Tower256ConcreteBackend.lean: DONE, single-file green (hbox build-logs/cursor-t3.log). Work copy: scratchpad/work/T.lean.
- Callers switched (work copies uploaded before ub1): ObjectiveSourcePackage.decodeBytes(+_eq), ObjectiveBendSourceArtifact.decodeBytes(+_eq),
  Host/ObjectiveStudioPublication uses them, GenericSimplexServe receipt file -> receiptFileStream.decodeBytes.
- Umbrella cursor-ub1 launched 22:41 (pid build-logs/cursor-ub1.pid), waiting for a slot.
- Round 2 (NOT uploaded yet; wait for ub1 to finish — never edit the tree mid-build): scratchpad/work/{Compiler/FiniteDependentMapCodec,
  Compiler/StoreCodec, Kernel/ClockCell, Kernel/SystemCell, Kernel/PayCell, Kernel/PayEnrolMemo, Kernel/PayEnrolClaim}.lean
  = store payload on the cursor: FDM.entryStream native decodeAt, StoreCodec.unitStream native, tagCursor/withTagCursor/one_octet_tag,
  Wire.cursorReady + payloadStream bit, namespace enums via withTagCursor, coded streams (journalReason/pendingReason/mode) + memoField native.
  Prototyped green locally against a stub (scratchpad/ltest: Stub/Core.lean + Test1.lean, LEAN_PATH via ltest/env.sh using ~/dev/minidregg mathlib, same rev).

## DONE (2026-10-15 ~01:10)
- Commit affd741c on codec-shapes (on 6b279b20, root amended 13cc5a51 meanwhile). Not pushed.
- Umbrella cursor-ub1: only the 3 expected reds; AxiomCensus none on sorryAx. codec-bench numbers in the commit message.
- Left: DurableReceiverCore Entry.record stays List (decode converts once via the csimp); other hand-written codecs stay on the
  list path (default decodeAt, cursorNative false) — overriding one is mechanical (see PayEnrolMemo/Claim, withTagCursor).
