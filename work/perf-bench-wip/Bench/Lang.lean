/-
# Bench.Lang — an invoke through LANG's program behind a closure of packages (PERF; ASSEMBLY-perf ID-2)

Tooling (closure C9). The numbers LANG's load memo (ID-2) is to move: one `invoke` of
`Lang.Journey.owned`'s `set`, admitted by `Receive.submit` under the DEPLOYED `Ctx`
(`Host.Deployed.X`: CODEC's digest and hash, Ed25519, `Lang.program`), with `owned` importing a
chain of `depth` library packages, so every invoke loads, relocates and (LANG-16) re-checks a
closure of `depth + 1` packages. Calls are signed before the clock starts; each sample is one
`Receive.submit` (so it includes one Ed25519 verify, which `bench-host verify` prints alone).

The library package is the scout's (P2) test input: a record of `width` constant fields, the
closure's decode/check weight. It is an input to the deployed code, not a copy of any of it.
-/
import Bench.Host
import Lang.Journey

namespace Nanodregg.Bench.Lang

open Nanodregg.Kernel Nanodregg.Kernel.Receive Nanodregg.Codec Nanodregg.Host.Deployed
open Nanodregg.Lang Nanodregg.Bench.Host

/-- A library: `width` fields `fNNN = j + 1` (P2's closure member). -/
def libPkg (imports : List ByteArray) (width : Nat) : Package :=
  let nm (j : Nat) : String := "f" ++ (if j < 10 then "00" else if j < 100 then "0" else "") ++ toString j
  { imports, state := Journey.S, iface := .record ((List.range width).map fun j => (nm j, Ty.nat)),
    body := .record ((List.range width).map fun j => (nm j, Term.prim .add (.nat j) (.nat 1))),
    methods := [], laws := [] }

/-- A signed call by `f` at `w` pinning `ids`. -/
def call (w : World D) (f : Founder) (ids : List D) (body : Body D) : Call D :=
  let u : Unsigned D :=
    { member := f.id, key := f.pk, notBefore := w.height, validUntil := w.height + 1 + 100,
      pins := Sim.Gen.S.pinsFor X.env w ids, maxCharge := 1 <<< 40, body }
  { unsigned := u, signature := Ed25519.sign f.seed (X.unsignedBytes u) }

def admit (w : World D) (c : Call D) (what : String) : Except String (World D × List D) :=
  match Receive.submit X w c with
  | .ok (t, w') => .ok (w', createdIds X.env t)
  | .error v => .error s!"{what}: {Sim.Gen.vname v}"

/-- Install the chain and `owned`, create the object; then `calls` invokes, each timed. -/
def scenario (depth width calls : Nat) : Except String (World D × Array (Call D)) := do
  let fs := founders 2
  let a := fs.getD 0 ⟨Digest.zero, .empty, .empty⟩
  let mut w := genesisWorld fs
  let mut prev : Option D := none
  let mut libs : List D := []
  for _ in [0:depth] do
    let some bytes := Wire.encodePackage (libPkg (prev.toList.map Digest.bytes) width) | throw "lib bytes"
    let (w', ids) ← admit w (call w a (a.id :: libs) (.install bytes)) "install lib"
    let some id := ids.head? | throw "lib id"
    w := w'; prev := some id; libs := libs ++ [id]
  let some top := Wire.encodePackage { Journey.owned with imports := prev.toList.map Digest.bytes } | throw "owned bytes"
  let (w', ids) ← admit w (call w a (a.id :: libs) (.install top)) "install owned"
  let some pkg := ids.head? | throw "owned id"
  w := w'
  let some owner := Wire.encodeData .bytes (.bytes a.id.bytes) | throw "owner bytes"
  let some n0 := Journey.nat64 0 | throw "0"
  let (w', ids) ← admit w (call w a (a.id :: pkg :: libs) (.create (some pkg) [] [(stateBase, owner), (stateBase + 1, n0)])) "create"
  let some obj := ids.head? | throw "object id"
  w := w'
  let mut cs := #[]
  for i in [0:calls] do
    let some arg := Journey.nat64 (i % 100) | throw "arg"
    cs := cs.push (call w a (a.id :: obj :: pkg :: libs) (.invoke obj 0 arg 10000 none))
  return (w, cs)

def bench (depths : List Nat) (width calls : Nat) : IO UInt32 := do
  for d in depths do
    match scenario d width calls with
    | .error e => IO.eprintln s!"bench-lang: depth {d}: {e}"; return 1
    | .ok (w, cs) =>
      let sink ← IO.mkRef 0
      let win ← IO.mkRef w
      let mut ns := #[]
      for c in cs do
        let w ← win.get
        let t0 ← IO.monoNanosNow
        let r := Receive.submit X w c
        sink.modify (· + match r with | .ok _ => 1 | .error _ => 0)
        ns := ns.push ((← IO.monoNanosNow) - t0)
      if (← sink.get) ≠ cs.size then IO.eprintln s!"bench-lang: depth {d}: an invoke was refused"; return 1
      report "invoke-submit" s!"closure{d + 1}-width{width}" "us" ns
  return 0

def main (args : List String) : IO UInt32 := do
  IO.println s!"BENCH load - - {← load}"
  let code ← match args with
    | width :: calls :: depths => bench (depths.map String.toNat!) width.toNat! calls.toNat!
    | _ => do IO.eprintln "usage: bench-lang WIDTH CALLS DEPTH..."; pure 2
  IO.println s!"BENCH load-after - - {← load}"
  return code

end Nanodregg.Bench.Lang
