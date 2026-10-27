import Kernel.World
import Codec.Stream

open Nanodregg.Kernel Nanodregg.Codec

/-- A distinct 32-byte id per (i, salt). -/
def dig (i salt : Nat) : Digest :=
  (Digest.ofBytes? (Stream.u64.bytes (UInt64.ofNat i) ++ Stream.u64.bytes (UInt64.ofNat salt)
    ++ Stream.u64.bytes (UInt64.ofNat (i * 7)) ++ Stream.u64.bytes 0)).getD Digest.zero

/-- A BAR record: a data object with an owner and one 128-byte state slot. -/
def recordCell (i : Nat) : Cell :=
  { kind := 2, discipline := .ram,
    slots := [(1, (dig i 1).bytes), (16, ⟨Array.replicate 128 (UInt8.ofNat i)⟩)] }

def world (n : Nat) : World Digest :=
  let cells := (List.range n).foldl (fun m i => m.insert (dig i 0) (Entry.live (recordCell i))) {}
  let journal := (List.range n).foldl (fun m i => m.insert (dig i 2) (i + 1, dig i 3)) {}
  { cells, journal, spent := {}, height := n, chain := dig n 4, allowance := 1 <<< 40 }

/-- A whole-World encoding from the combinators (the shape a base would have). -/
def putCell (c : Cell) (buf : ByteArray) : ByteArray :=
  let buf := Stream.u32.put (UInt32.ofNat c.kind) buf
  let buf := Stream.u8.put (match c.discipline with | .rom => 0 | .appendOnly => 1 | .ram => 2) buf
  let buf := Stream.u32.put (UInt32.ofNat c.slots.length) buf
  c.slots.foldl (fun buf (k, v) =>
    Stream.u32.put (UInt32.ofNat v.size) (Stream.u32.put (UInt32.ofNat k) buf) ++ v) buf

def encodeWorld (w : World Digest) : ByteArray :=
  let buf := ByteArray.emptyWithCapacity (1 <<< 20)
  let buf := Stream.u64.put (UInt64.ofNat w.height) buf
  let buf := Stream.digest.put w.chain buf
  let buf := Stream.u64.put (UInt64.ofNat w.allowance) buf
  let buf := Stream.u32.put (UInt32.ofNat w.cells.size) buf
  let buf := w.cells.foldl (fun buf id e => match e with
    | .live c => putCell c (Stream.u8.put 1 (Stream.digest.put id buf))
    | .tomb => Stream.u8.put 0 (Stream.digest.put id buf)) buf
  let buf := Stream.u32.put (UInt32.ofNat w.journal.size) buf
  let buf := w.journal.foldl (fun buf id (h, d) =>
    Stream.digest.put d (Stream.u64.put (UInt64.ofNat h) (Stream.digest.put id buf))) buf
  let buf := Stream.u32.put (UInt32.ofNat w.spent.size) buf
  w.spent.foldl (fun buf n => Stream.digest.put n buf) buf

def main (args : List String) : IO UInt32 := do
  for n in (args.map String.toNat!) do
    let w := world n
    -- force the World before timing
    IO.println s!"n={n} cells={w.cells.size}"
    let reps := 20
    let mut best := 0
    let mut size := 0
    for r in [0:reps] do
      let t0 ← IO.monoNanosNow
      let b := encodeWorld { w with height := w.height + r }
      size := b.size
      (← IO.getStdout).write (b.extract (b.size - 1) b.size)
      let t1 ← IO.monoNanosNow
      if r = 0 ∨ t1 - t0 < best then best := t1 - t0
    IO.println s!"K1 n={n} bytes={size} encode-best-us={best / 1000}"
  return 0
