-- HOST-3's base bench (out of tree on purpose; copy to Host/Bench/Base.lean with a local
-- `lean_exe «base-bench» where root := `Host.Bench.Base`, never commit).
-- The REAL base path: Codec.Deployed.world, Host.Base.file under Keys.ofKey (KMAC256), Base.read.
import Host.Keys
import Codec.Deployed

open Nanodregg.Kernel Nanodregg.Codec Nanodregg.Host

def dig (i salt : Nat) : Digest :=
  (Digest.ofBytes? (Stream.u64.bytes (UInt64.ofNat i) ++ Stream.u64.bytes (UInt64.ofNat salt)
    ++ Stream.u64.bytes (UInt64.ofNat (i * 7)) ++ Stream.u64.bytes 0)).getD Digest.zero

def recordCell (i : Nat) : Cell :=
  { kind := 2, discipline := .ram,
    slots := [(1, (dig i 1).bytes), (16, ⟨Array.replicate 128 (UInt8.ofNat i)⟩)] }

def bar (n : Nat) : World Digest :=
  let cells := (List.range n).foldl (fun m i => m.insert (dig i 0) (Entry.live (recordCell i))) {}
  let journal := (List.range n).foldl (fun m i => m.insert (dig i 2) (i + 1, dig i 3)) {}
  { cells, journal, spent := {}, height := n, chain := dig n 4, allowance := 1 <<< 40 }

/-- `act` takes a run-time nonce so the compiler cannot hoist the work out of the loop. -/
@[noinline] def best (k : Nat) (act : Nat → Nat) : IO (Nat × Nat) := do
  let mut b := 0
  let mut out := 0
  for i in List.range k do
    let t0 ← IO.monoNanosNow
    out := act (t0 % 2)
    if out = 1234567 then IO.println "."
    let dt := (← IO.monoNanosNow) - t0
    if i = 0 || dt < b then b := dt
  return (b, out)

def ms (ns : Nat) : String := s!"{ns / 1000000}.{(ns / 10000) % 100 / 10}{(ns / 1000) % 10}"

def main (args : List String) : IO Unit := do
  let key := dig 99 99
  let keys := Keys.ofKey key
  let c := Cadence.deployed
  for n in (args.map String.toNat!) do
    let w := bar n
    let reps := if n ≤ 10000 then 10 else 3
    let wv := fun j => { w with height := n + j }
    let (tEnc, sz) ← best reps fun j => (Deployed.world.bytes (wv j)).size
    let bytes := Deployed.world.bytes w
    let (tMac, _) ← best reps fun j => (Hash.mac key domBase (bytes.push (UInt8.ofNat j))).bytes.size
    let fileOf := fun j => match Base.file keys c Deployed.world (wv j) 0 Digest.zero with | .ok f => f | .error _ => ByteArray.empty
    let file := fileOf 0
    let file1 := fileOf 1
    let (tSeal, _) ← best reps fun j => (fileOf j).size
    let (tRead, h) ← best reps fun j => match Base.read keys c Deployed.world (if j = 0 then file else file1) with | .ok (b, _) => b.world.height | .error _ => 0
    IO.println s!"records {n}: base {sz} B (file {file.size}); encode {ms tEnc} ms, MAC {ms tMac} ms, seal (encode+MAC) {ms tSeal} ms, open (MAC+decode) {ms tRead} ms [height {h}]"
