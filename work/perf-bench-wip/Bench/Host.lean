/-
# Bench.Host — numbers for the deployed Host path (PERF; ASSEMBLY-perf ID-8)

Tooling (closure C9: nothing deployed imports `Bench`). Every measured operation is a DEPLOYED
definition called as `host` calls it: `Host.Deployed.X` (CODEC's digest, cSHAKE256, codecs,
RFC 8032 Ed25519, LANG's program), `Receive.submit`, `Host.Deployed.world`, `Base.file`,
`Base.read`, `Host.genesis`, `Host.fileCheckpoint`, `Host.commitBatch`, `Host.openWriter`,
`Host.openFollower`, `foldStep` and `auditStep`. Nothing here re-implements what it measures; the
only code of its own drives those calls and reads the clock.

Each call's inputs come through an `IO.Ref` and each result is forced into one before the clock
is read again (P3's sink pattern: a pure call the compiler can hoist measures nothing). A timing
is the MEDIAN of N runs with its p99 and max beside it, never a best-of; every report line names
its operation, its size and its unit:

    BENCH <op> <size> <metric> <value>

and the run states its machine (`BENCH load …`, `BENCH device …`). A number without them is not
a number.

The records are births (`create`, a data object with one state slot), signed by a founder with
CODEC's `Ed25519.sign` and admitted by `Receive.submit` under the deployed `Ctx`, so the World a
base seals holds real member, grant and object cells, real journal entries and real chain values.
-/
import Host.Deployed
import Host.Cli
import Kernel.Sim.Gen

namespace Nanodregg.Bench.Host

open Nanodregg.Kernel Nanodregg.Kernel.Receive Nanodregg.Codec Nanodregg.Host
open Nanodregg.Host.Deployed

/-! ## Clock and report -/

def load : IO String := do
  try
    let o ← IO.Process.output { cmd := "sysctl", args := #["-n", "vm.loadavg"] }
    if o.exitCode = 0 then return o.stdout.trimAscii.toString
    return (← IO.FS.readFile "/proc/loadavg").trimAscii.toString
  catch _ => return "unknown"

/-- This process's resident set now, in KiB (`ps`: there is no getrusage in Lean core). -/
def rssKiB : IO Nat := do
  try
    let o ← IO.Process.output { cmd := "ps", args := #["-o", "rss=", "-p", toString (← IO.Process.getPID)] }
    return o.stdout.trimAscii.toString.toNat?.getD 0
  catch _ => return 0

def line (op : String) (size : String) (metric : String) (value : String) : IO Unit :=
  IO.println s!"BENCH {op} {size} {metric} {value}"

/-- Nanoseconds as milliseconds, three decimals. -/
def ms (ns : Nat) : String :=
  let f := toString ((ns / 1000) % 1000)
  s!"{ns / 1000000}.{"".pushn '0' (3 - f.length)}{f}"

/-- Nanoseconds as microseconds, one decimal. -/
def us (ns : Nat) : String := s!"{ns / 1000}.{(ns / 100) % 10}"

def sorted (ns : Array Nat) : Array Nat := ns.qsort (· < ·)

def pct (a : Array Nat) (q : Nat) : Nat := a.getD (min (a.size - 1) (a.size * q / 100)) 0

/-- Report median, p99 and max of `ns` (nanoseconds) in `unit` ("ms" or "us"). -/
def report (op size : String) (unit : String) (ns : Array Nat) : IO Unit := do
  let a := sorted ns
  let fmt := if unit = "us" then us else if unit = "ns" then toString else ms
  line op size s!"median-{unit}" (fmt (pct a 50))
  line op size s!"p99-{unit}" (fmt (pct a 99))
  line op size s!"max-{unit}" (fmt (a.back?.getD 0))
  line op size "n" (toString a.size)

/-- Time `f` on the value in `input`, `n` times; the result's `force` goes into a sink. -/
def timeN {α β : Type} (n : Nat) (input : IO.Ref α) (f : α → β) (force : β → Nat) : IO (Array Nat × Nat) := do
  let sink ← IO.mkRef 0
  let mut ns := #[]
  for _ in [0:n] do
    let x ← input.get
    let t0 ← IO.monoNanosNow
    let y := f x
    sink.modify (· + force y)
    let t1 ← IO.monoNanosNow
    ns := ns.push (t1 - t0)
  return (ns, ← sink.get)

/-! ## Founders and births, under the deployed `Ctx` -/

def worldName : ByteArray := "bench".toUTF8

/-- A founder's 32-byte seeds: the current key and the precommitted next key. -/
def seed (i : Nat) (next : Bool) : ByteArray :=
  ⟨Array.ofFn fun j : Fin 32 => ((i * 131 + j.val * 7 + if next then 97 else 0) % 256).toUInt8⟩

structure Founder where
  id : D
  seed : ByteArray
  pk : ByteArray

def founders (k : Nat) : List Founder :=
  (List.range k).map fun i => ⟨founderId X worldName i, seed i false, Ed25519.publicKey (seed i false)⟩

def genesisWorld (fs : List Founder) : World D :=
  Receive.genesis X worldName allowanceMax
    (fs.zipIdx.map fun (f, i) => (f.pk, nextKeyDigest X (Ed25519.publicKey (seed i true))))

/-- A birth by `f` at the World `w`: a data object whose one state slot is `payload`. -/
def birth (w : World D) (f : Founder) (payload : ByteArray) : Call D :=
  let u : Unsigned D :=
    { member := f.id, key := f.pk, notBefore := w.height, validUntil := w.height + 1 + 100,
      pins := Sim.Gen.S.pinsFor X.env w [f.id], maxCharge := 1 <<< 40,
      body := .create none [] [(stateBase, payload)] }
  { unsigned := u, signature := Ed25519.sign f.seed (X.unsignedBytes u) }

/-- The `i`-th birth's payload: `bytes` bytes, unique per `i` (so every call's txId differs). -/
def payload (i bytes : Nat) : ByteArray :=
  let tag := Sim.Gen.nat i
  tag ++ ⟨Array.replicate (bytes - min bytes tag.size) (i % 251).toUInt8⟩

/-- Admit `n` births round-robin over `fs` from `w`, each through `Receive.submit`; the Turns and
the World after them, or the first refusal by name. -/
def births (fs : List Founder) (w : World D) (start n bytes : Nat) :
    Except String (Array (Turn D) × World D) := Id.run do
  let mut w := w
  let mut ts := #[]
  for i in [start:start + n] do
    let f := fs.getD (i % fs.length) ⟨w.chain, ByteArray.empty, ByteArray.empty⟩
    match Receive.submit X w (birth w f (payload i bytes)) with
    | .error v => return .error s!"birth {i}: {Sim.Gen.vname v}"
    | .ok (t, w') => ts := ts.push t; w := w'
  return .ok (ts, w)

/-! ## The benches -/

/-- Ed25519 verify per call, at a real birth's signed bytes; and `Receive.submit` per call. -/
def verifyBench (n : Nat) : IO UInt32 := do
  let fs := founders 2
  let g := genesisWorld fs
  let c := birth g (fs.getD 0 ⟨g.chain, .empty, .empty⟩) (payload 0 16)
  let msg := X.unsignedBytes c.unsigned
  let input ← IO.mkRef (c.unsigned.key, msg, c.signature)
  let (ns, ok) ← timeN n input (fun (pk, m, s) => Ed25519.verify pk m s) (fun b => if b then 1 else 0)
  if ok ≠ n then IO.eprintln s!"bench: verify refused a real signature ({ok}/{n})"; return 1
  report "ed25519-verify" s!"{msg.size}B" "us" ns
  let cin ← IO.mkRef (g, c)
  let (ns, ok) ← timeN n cin (fun (w, c) => Receive.submit X w c)
    (fun r => match r with | .ok _ => 1 | .error _ => 0)
  if ok ≠ n then IO.eprintln "bench: submit refused a real birth"; return 1
  report "submit-birth" s!"{(X.callBytes c).size}B" "us" ns
  let sin ← IO.mkRef (fs.getD 0 ⟨g.chain, .empty, .empty⟩, msg)
  let (ns, _) ← timeN (max 1 (n / 4)) sin (fun (f, m) => Ed25519.sign f.seed m) ByteArray.size
  report "ed25519-sign" s!"{msg.size}B" "us" ns
  return 0

/-- 32-byte `Digest` order and equality as the World's maps call them: `reps` calls per sample,
reported per call in nanoseconds. -/
def digestBench (n : Nat) : IO UInt32 := do
  let a := Hash.digest "bench/a" "x".toUTF8
  let b := Hash.digest "bench/b" "x".toUTF8
  let input ← IO.mkRef (a, b)
  let reps := 1000
  let (ns, _) ← timeN n input
    (fun (a, b) => (List.range reps).foldl (fun acc i =>
      acc + (if compare a (if i % 2 = 0 then b else a) = .lt then 1 else 0)) 0) id
  report "digest-compare" "32B" "ns" (ns.map (· / reps))
  let (ns, _) ← timeN n input
    (fun (a, b) => (List.range reps).foldl (fun acc i =>
      acc + (if a = (if i % 2 = 0 then b else a) then 1 else 0)) 0) id
  report "digest-eq" "32B" "ns" (ns.map (· / reps))
  return 0

/-- The base at each size in `sizes` (births, 16-byte payloads, from one run): the World's bytes,
its encode, the base sealer's MAC over them, `Base.file` (encode + MAC, the seal) and `Base.read`
(MAC + decode, the base half of every open), and RSS after. The base's record index is empty
here; `worstcut` seals a base with its real index. -/
def baseBench (sizes : List Nat) (reps : Nat) : IO UInt32 := do
  let fs := founders 2
  let keys := Keys.ofKey (Hash.digest "bench/key" ByteArray.empty)
  let mut w := genesisWorld fs
  let mut done := 0
  for n in sizes do
    let t0 ← IO.monoNanosNow
    match births fs w done (n - done) 16 with
    | .error e => IO.eprintln s!"bench: {e}"; return 1
    | .ok (_, w') => w := w'; done := n
    let t1 ← IO.monoNanosNow
    line "births" s!"{n}" "generate-ms" (ms (t1 - t0))
    let k := if n ≤ 10000 then reps else max 1 (reps / 3)
    let win ← IO.mkRef w
    let (ns, bytes) ← timeN k win (fun w => world.bytes w) (fun b => b.size / k)
    line "world" s!"{n}" "bytes" (toString bytes)
    report "world-encode" s!"{n}" "ms" ns
    let bin ← IO.mkRef (world.bytes w)
    let (ns, _) ← timeN k bin (fun b => keys.base.tag b) ByteArray.size
    report "base-mac" s!"{n}" "ms" ns
    let (ns, _) ← timeN k win (fun w => Base.file keys c world w 0 Digest.zero [])
      (fun r => match r with | .ok f => f.size | .error _ => 0)
    report "base-seal" s!"{n}" "ms" ns
    let file := match Base.file keys c world w 0 Digest.zero [] with | .ok f => f | .error _ => .empty
    let fin ← IO.mkRef file
    let (ns, h) ← timeN k fin (fun f => Base.read keys c world f)
      (fun r => match r with | .ok (b, _, _) => b.world.height | .error _ => 0)
    if h ≠ k * w.height then IO.eprintln "bench: Base.read did not read back the sealed World"; return 1
    report "base-read" s!"{n}" "ms" ns
    line "rss" s!"{n}" "kib" (toString (← rssKiB))
  return 0

/-- Births with state `bytes` from `w`, one Turn at a time, each with the World after it. -/
def birthSteps (fs : List Founder) (w : World D) (start n bytes : Nat) :
    Except String (Array (Turn D × World D)) := Id.run do
  let mut w := w
  let mut out := #[]
  for i in [start:start + n] do
    let f := fs.getD (i % fs.length) ⟨w.chain, ByteArray.empty, ByteArray.empty⟩
    match Receive.submit X w (birth w f (payload i bytes)) with
    | .error v => return .error s!"birth {i}: {Sim.Gen.vname v}"
    | .ok (t, w') => out := out.push (t, w'); w := w'
  return .ok out

/-- THE worst cut (ASSEMBLY-perf ID-8): a real Store in `dir` whose newest durable base holds
`baseN` births (16-byte state, THE BAR's base at 1000) with its real index, and whose segment
after it is filled with the largest births an event allows, in batches of up to `Record.turnsMax`,
until the next frame would leave `tailMax` (the loop's own bound, `withinTail`, decides each
frame through `commitBatch`'s proof argument). Then the cold opens a restart performs, from the
files: `openFollower` with the writer's fold (`foldStep`, what `openWriter` runs before it locks)
and with a follower's audit (`auditStep`: every Turn re-derived, signatures verified). -/
def worstcut (dir : System.FilePath) (baseN bigBytes reps : Nat) : IO UInt32 := do
  let fs := founders 2
  let key := Hash.digest "bench/key" dir.toString.toUTF8
  let keys := Keys.ofKey key
  let g := genesisWorld fs
  match ← (Host.genesis dir key keys c world recorder.mark g : IO (Except (StoreFault (Record.Fault (Reject D))) Unit)) with
  | .error f => IO.eprintln s!"bench: genesis {f.name}"; return 1
  | .ok () => pure ()
  let opened ← openWriter dir keys c world recorder.mark foldStep
  if let .error f := opened then IO.eprintln s!"bench: openWriter {f.name}"; return 1
  let .ok wr := opened | return 1
  let store := fileStore wr.segment
  let mut r := wr.opening.resident
  -- 1. the base: baseN small births, committed in batches, then sealed with the real index
  let res := birthSteps fs r.world 0 baseN 16
  if let .error e := res then IO.eprintln s!"bench: {e}"; return 1
  let .ok small := res | return 1
  for j in [0:small.size:Record.turnsMax] do
    let chunk := small.extract j (j + Record.turnsMax)
    let some (_, w') := chunk.back? | continue
    let rec_ := recorder.encode w' (chunk.map (·.1))
    if h : withinTail c r.sealed r.pos.offset (frameSize rec_) = true then
      match ← commitBatch c r.sealed store keys.segment r.pos rec_ h with
      | .error e => IO.eprintln s!"bench: commit {e}"; return 1
      | .ok pos =>
        let (hgt, chain) := recorder.mark r.world
        r := { r with world := w', pos, index := r.index.push ⟨hgt, r.pos.offset, chain⟩ }
    else IO.eprintln "bench: the base phase left tailMax"; return 1
  match ← (fileCheckpoint dir keys c world (async := false)).write r.world r.pos.offset r.pos.tag r.index with
  | .error f => IO.eprintln s!"bench: seal {f.name}"; return 1
  | .ok (bytes, digest) =>
    let (hgt, chain) := recorder.mark r.world
    r := { r with sealed := ⟨r.pos.offset, bytes, hgt, chain, digest⟩ }
  line "worstcut" s!"base{baseN}" "base-world-bytes" (toString r.sealed.bytes)
  line "worstcut" s!"base{baseN}" "tailMax-bytes" (toString (c.tailMax r.sealed.bytes))
  -- 2. the tail: the largest births, a batch at a time, while the next frame stays within tailMax
  let mut i := baseN
  let mut turns := 0
  let mut records := 0
  let mut maxRecord := 0
  let mut full := false
  for _ in [0:c.tailMax r.sealed.bytes / bigBytes + 2] do
    if full then break
    let res := birthSteps fs r.world i Record.turnsMax bigBytes
    if let .error e := res then IO.eprintln s!"bench: {e}"; return 1
    let .ok steps := res | return 1
    -- the most of this batch whose frame fits
    let mut k := steps.size
    let mut placed := false
    while k > 0 && !placed do
      let take := steps.extract 0 k
      let some (_, w') := take.back? | break
      let rec_ := recorder.encode w' (take.map (·.1))
      if h : withinTail c r.sealed r.pos.offset (frameSize rec_) = true then
        match ← commitBatch c r.sealed store keys.segment r.pos rec_ h with
        | .error e => IO.eprintln s!"bench: commit {e}"; return 1
        | .ok pos =>
          let (hgt, chain) := recorder.mark r.world
          r := { r with world := w', pos, index := r.index.push ⟨hgt, r.pos.offset, chain⟩ }
          turns := turns + k; records := records + 1; maxRecord := max maxRecord rec_.size
          placed := true
      else
        k := k - 1
    if k < steps.size then full := true
    i := i + k
  let tail := r.pos.offset - r.sealed.offset
  line "worstcut" s!"base{baseN}" "tail-bytes" (toString tail)
  line "worstcut" s!"base{baseN}" "tail-records" (toString records)
  line "worstcut" s!"base{baseN}" "tail-turns" (toString turns)
  line "worstcut" s!"base{baseN}" "tail-max-record-bytes" (toString maxRecord)
  line "worstcut" s!"base{baseN}" "recordBytesMax" (toString c.recordBytesMax)
  wr.segment.sync  -- the writer's handle, and its lock, live to here
  -- 3. the cold opens, from the files
  let mut fold := #[]
  let mut aud := #[]
  for _ in [0:reps] do
    let t0 ← IO.monoNanosNow
    match ← openFollower dir keys c world recorder.mark foldStep with
    | .error f => IO.eprintln s!"bench: reopen (fold) {f.name}"; return 1
    | .ok o => if o.opened.world.height ≠ r.world.height then IO.eprintln "bench: fold reopened short"; return 1
    fold := fold.push ((← IO.monoNanosNow) - t0)
    let t0 ← IO.monoNanosNow
    match ← openFollower dir keys c world recorder.mark auditStep with
    | .error f => IO.eprintln s!"bench: reopen (audit) {f.name}"; return 1
    | .ok o => if o.opened.world.height ≠ r.world.height then IO.eprintln "bench: audit reopened short"; return 1
    aud := aud.push ((← IO.monoNanosNow) - t0)
  report "worstcut-reopen-fold" s!"base{baseN}" "ms" fold
  report "worstcut-reopen-audit" s!"base{baseN}" "ms" aud
  line "rss" s!"worstcut-base{baseN}" "kib" (toString (← rssKiB))
  return 0

def usage : String :=
  "usage: bench-host verify N | digest N | base REPS SIZE... | worstcut DIR BASE_N BIG_BYTES REPS"

def main (args : List String) : IO UInt32 := do
  IO.println s!"BENCH load - - {← load}"
  let code ← match args with
    | ["verify", n] => verifyBench n.toNat!
    | ["digest", n] => digestBench n.toNat!
    | "base" :: reps :: sizes => baseBench (sizes.map String.toNat!) reps.toNat!
    | ["worstcut", dir, n, big, reps] => worstcut dir n.toNat! big.toNat! reps.toNat!
    | _ => do IO.eprintln usage; pure 2
  IO.println s!"BENCH load-after - - {← load}"
  return code

end Nanodregg.Bench.Host
