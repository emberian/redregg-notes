import Host.Open
import Host.Keys
open Nanodregg Nanodregg.Host Nanodregg.Codec

def kOf (b : UInt8) : Digest := (Digest.ofBytes? (ByteArray.mk (Array.replicate 32 b))).getD Digest.zero
def c : Cadence := { sealMinBytes := 64, worldBytesMax := 1024, recordBytesMax := 1 <<< 25 }
def W := UInt64
def step : UInt64 → ByteArray → Except String UInt64 := fun w _ => .ok (w + 1)
def recs (n : Nat) : List ByteArray := (List.range n).map fun i => s!"batch-{i}".toUTF8
def show' (tag : String) (keys : Keys) (base : ByteArray) (seg : ByteArray) : IO Unit := do
  let r : Except (StoreFault String) (Opening UInt64) :=
    Id.run (openWith keys c Stream.u64 step base seg.size (fun off len => pure (.ok (seg.extract off (off+len)))))
  match r with
  | .ok o => IO.println s!"{tag}: OPENS records={o.opened.records} validLen={o.opened.validLen} torn={o.opened.torn} (writer truncates to {o.pos.offset} of {seg.size})"
  | .error e => IO.println s!"{tag}: refused {e.name}"

def main : IO Unit := do
  let kA := Keys.ofKey (kOf 1); let kB := Keys.ofKey (kOf 2)
  let segA := Log.encodeAll kA.segment segmentInitial (recs 40)
  let segB := Log.encodeAll kB.segment segmentInitial (recs 5)
  let tagB5 := Log.lastTag kB.segment segmentInitial (recs 5)
  let z : Digest := Digest.zero
  let baseB0 := (Base.file kB c Stream.u64 (0 : UInt64) 0 z).toOption.get!
  let baseB5 := (Base.file kB c Stream.u64 (5 : UInt64) segB.size ⟨tagB5, (kB.segment.tag_size _)⟩).toOption.get!
  IO.println s!"segA {segA.size} B, segB {segB.size} B, frameMax {Log.frameMax c.recordBytesMax}"
  show' "own segment, genesis base" kB baseB0 segB
  show' "A's segment under B's genesis base (offset 0)" kB baseB0 segA
  show' "own segment, base at 5" kB baseB5 segB
  show' "A's segment under B's base at offset 5" kB baseB5 segA
