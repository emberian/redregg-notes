/- Evaluator probe (ASSEMBLY-lang-docs): G1's laws restated at main d1f483e's reqTy, run through the
real receivers with Lang.program under Sim's toy parameters. Three questions:
H1 does the birth hole hold at HEAD (packaged object seeded with a full quorum)?
H2 does a law on a DATA object survive its own removal (the `law` receiver judges old = new)?
H3 can a true per-window rate limit be written with the signed window (KERNEL-10), no clock holder? -/
import Lang.Journey
namespace Probe
open Nanodregg.Kernel Nanodregg.Kernel.Receive Nanodregg.Lang
open Nanodregg.Lang.Journey hiding D
abbrev D := Nanodregg.Lang.Journey.D

def sortRow {α : Type} (fs : List (Label × α)) : List (Label × α) := (fs.toArray.qsort (fun a b => a.1 < b.1)).toList
def okT : Term := .inj verdictTy "ok" (.record [])
def refusedT (why : String) : Term := .inj verdictTy "refused" (.bytes why.toUTF8)
def lawOf (S : Ty) (body : Term) : Term := .lam S (.lam S (.lam reqTy body))
def old (f : Label) : Term := .get (.var 2) f
def new (f : Label) : Term := .get (.var 1) f
def rq (f : Label) : Term := .get (.var 0) f
def guard (c : Term) (why : String) (rest : Term) : Term := .ite c rest (refusedT why)
def guards : List (Term × String) → Term → Term
  | [], t => t
  | (c, w) :: r, t => guard c w (guards r t)
def allOf (l : List (Term × String)) : Term := guards l okT
def andT (a b : Term) : Term := .ite a b (.bool false)
def anyOf : List Term → Term
  | [] => .bool false
  | c :: r => .ite c (.bool true) (anyOf r)
def notT (a : Term) : Term := .ite a (.bool false) (.bool true)
def n (k : Nat) : Term := .nat k
def pow2 : Nat → Nat | 0 => 1 | k + 1 => 2 * pow2 k
def bit (t : Term) (i : Nat) : Term := .prim .mod (.prim .div t (n (pow2 i))) (n 2)
def popcount (t : Term) (cnt : Nat) : Term := (List.range cnt).foldl (fun acc i => .prim .add acc (bit t i)) (n 0)

def quorum (S : Ty) (members : List ByteArray) (k : Nat) (guarded : Label) : Term :=
  let cnt := members.length
  let changed := notT (.prim .eq (new guarded) (old guarded))
  let approvalFor (m : ByteArray) (i : Nat) : Term :=
    andT (.prim .eq (bit (old "approvals") i) (n 0))
      (andT (.prim .eq (new "approvals") (.prim .add (old "approvals") (n (pow2 i))))
        (.prim .beq (rq "agent") (.bytes m)))
  lawOf S (guards
    [(anyOf (members.map fun m => .prim .beq (rq "agent") (.bytes m)), "not a member"),
     (.prim .lt (new "approvals") (n (pow2 cnt)), "approvals out of range")]
    (.ite changed
      (allOf [(.prim .le (n k) (popcount (old "approvals") cnt), "no quorum"),
              (.prim .eq (new "approvals") (n 0), "approvals not reset")])
      (.ite (.prim .eq (new "approvals") (old "approvals")) okT
        (guard (anyOf (members.zipIdx.map fun (m, i) => approvalFor m i)) "bad approval" okT))))

/-- A per-window rate limit from the SIGNED window: the call's window lies inside one epoch of
width `W`, so `World.admit` lands it in epoch `notBefore / W`; the state's epoch must be that one. -/
def windowed (S : Ty) (W limit : Nat) (guarded : Label) : Term :=
  let e := Term.prim .div (rq "notBefore") (n W)
  let inc := Term.ite (.prim .eq (new guarded) (old guarded)) (n 0) (n 1)
  lawOf S (guards [(.prim .eq (.prim .div (rq "validUntil") (n W)) e, "window spans epochs"),
                   (.prim .eq (new "epoch") e, "epoch is not the call's window")]
    (.ite (.prim .eq (new "epoch") (old "epoch"))
      (allOf [(.prim .eq (new "count") (.prim .add (old "count") inc), "count not bumped"),
              (.prim .le (new "count") (n limit), s!"rate limit {limit}")])
      (allOf [(.prim .lt (old "epoch") (new "epoch"), "epoch went back"),
              (.prim .eq (new "count") inc, "count not reset")])))

def tyQ : Ty := .record (sortRow [("approvals", .nat), ("total", .nat)])
def tyR : Ty := .record (sortRow [("count", .nat), ("epoch", .nat), ("total", .nat)])
def methodOf (S A : Ty) (fields : List (Label × Term)) : Term := .lam S (.lam A (.lam reqTy (.record (sortRow fields))))
def keep (f : Label) : Term := .get (.var 2) f
def approveM := methodOf tyQ .nat [("approvals", .prim .add (keep "approvals") (.var 1)), ("total", keep "total")]
def commitM := methodOf tyQ .nat [("approvals", n 0), ("total", .var 1)]

def pkgOf (S : Ty) (laws : List (Label × Term)) (methods : List (Label × Ty × Term)) : Package :=
  let laws := sortRow laws
  let ms := sortRow methods
  { imports := [], state := S,
    iface := .record (sortRow (laws.map (fun (l, _) => (l, lawTy S)) ++ ms.map (fun (l, A, _) => (l, methodTy S A)))),
    body := .record (sortRow (laws ++ ms.map (fun (l, _, t) => (l, t)))),
    methods := ms.map (·.1), laws := laws.map (·.1) }

def nb (k : Nat) : ByteArray := (nat64 k).getD .empty

/-- `Sim.signed` with a chosen window (Gen.signed's body, re-signed). -/
def signedW (st : Sim.State) (m : Sim.Member) (pins : List (D × D)) (body : Body D) (lo hi : Nat) : Call D :=
  let P := Sim.toy
  let u : Unsigned D := { member := m.id, key := P.pub m.key, notBefore := lo, validUntil := hi, pins := pins, maxCharge := 1000000, body := body }
  { unsigned := u, signature := P.sign m.key ((P.ctx {}).unsignedBytes u) }

def probe : Run := Id.run do
  let prog := langProgram
  let fk : List (ByteArray × ByteArray) := [("f0".toUTF8, "f0-n".toUTF8), ("f1".toUTF8, "f1-n".toUTF8), ("f2".toUTF8, "f2-n".toUTF8)]
  let X := ctxWith prog {}
  let g := genesis X Sim.worldName 100000000 (fk.map fun (k, nx) => (k, nextKeyDigest X nx))
  let members := fk.zipIdx.map fun ((k, nx), i) => (⟨founderId X Sim.worldName i, k, nx⟩ : Sim.Member)
  let mut r : Run := { st := { rng := ⟨1⟩, reg := {}, host := g, members } }
  let a := members.getD 0 ⟨0, .empty, .empty⟩
  let b := members.getD 1 ⟨0, .empty, .empty⟩
  let c := members.getD 2 ⟨0, .empty, .empty⟩
  let idb (m : Sim.Member) := Sim.u64le m.id
  let sg (r : Run) (m : Sim.Member) (ids : List D) (body : Body D) := Sim.signed r.st m m.key (Sim.S.pinsFor r.st.host (m.id :: ids)) body
  let newId (t : Option (Turn D)) : D := (t.bind fun t => (createdIds Sim.env t).head?).getD 0
  -- H1 birth hole, packaged
  let qp := pkgOf tyQ [("quorum", quorum tyQ [idb a, idb b, idb c] 2 "total")] [("approve", .nat, approveM), ("commit", .nat, commitM)]
  let some qb := Wire.encodePackage qp | return note r "H1 quorum has no bytes" false
  let (r1, v1, t1) := go prog r (sg r a [] (.install qb))
  r := note r1 s!"H1a install quorum ({qb.size} bytes at HEAD's wire): {v1}" (v1 == "admitted")
  let pkg := newId t1
  let (r2, v2, t2) := go prog r (sg r a [pkg] (.create (some pkg) [] [(stateBase, nb 7), (stateBase + 1, nb 5)]))
  r := note r2 s!"H1b A creates quorum object seeded approvals=7 (all three): {v2}" (v2 == "admitted")
  let o1 := newId t2
  let (r3, v3, _) := go prog r (sg r a [o1, pkg] (.invoke o1 1 (nb 77) 100000 none))
  r := note r3 s!"H1c A commits 77 alone: {v3}, total = {totalOf r3.st.host o1}" (v3 == "admitted")
  -- H2 relaw hole, data object with the quorum as an extra law
  let lp := pkgOf tyQ [("quorum", quorum tyQ [idb a, idb b, idb c] 2 "total")] []
  let some lb := Wire.encodePackage lp | return note r "H2 law package has no bytes" false
  let (r4, v4, t4) := go prog r (sg r a [] (.install lb))
  r := note r4 s!"H2a install law-only quorum package: {v4}" (v4 == "admitted")
  let lid := newId t4
  let (r5, v5, t5) := go prog r (sg r a [lid] (.create none [lid] [(stateBase, nb 0), (stateBase + 1, nb 5)]))
  r := note r5 s!"H2b A creates data object \{approvals 0, total 5} under the quorum law: {v5}" (v5 == "admitted")
  let o2 := newId t5
  let (r6, v6, _) := go prog r (sg r a [o2, lid] (.write o2 [(1, some (nb 77))] none))
  r := note r6 s!"H2c CONTROL A writes total 77 alone: {v6}" (v6.startsWith "refused lawDenied" && (v6.splitOn "no quorum").length > 1)
  let (r7, v7, _) := go prog r (sg r a [o2, lid] (.law o2 [] none))
  r := note r7 s!"H2d A removes the quorum law (judged old = new): {v7}" (v7 == "admitted")
  let (r8, v8, _) := go prog r (sg r a [o2] (.write o2 [(1, some (nb 77))] none))
  r := note r8 s!"H2e A writes total 77 alone after removing the law: {v8}" (v8 == "admitted")
  -- H3 windowed rate limit, W = 50, limit 2, on a data object
  let W := 50
  let wp := pkgOf tyR [("windowed", windowed tyR W 2 "total")] []
  let some wb := Wire.encodePackage wp | return note r "H3 no bytes" false
  let (r9, v9, t9) := go prog r (sg r a [] (.install wb))
  r := note r9 s!"H3a install windowed(W=50, limit 2): {v9}" (v9 == "admitted")
  let wid := newId t9
  let ep (r : Run) := (r.st.host.height + 1) / W
  let win (r : Run) := (W * ep r, W * ep r + W - 1)
  let sw (r : Run) (ids : List D) (body : Body D) (lo hi : Nat) := signedW r.st a (Sim.S.pinsFor r.st.host (a.id :: ids)) body lo hi
  let e0 := ep r
  let (lo, hi) := win r
  let (r10, v10, t10) := go prog r (sw r [wid] (.create none [wid] [(stateBase, nb 0), (stateBase + 1, nb e0), (stateBase + 2, nb 0)]) lo hi)
  r := note r10 s!"H3b create \{count 0, epoch {e0}, total 0} window [{lo},{hi}] at height {r.st.host.height}: {v10}" (v10 == "admitted")
  let o3 := newId t10
  let wr (r : Run) (cnt e tot : Nat) (lo hi : Nat) :=
    sw r [o3, wid] (.write o3 [(0, some (nb cnt)), (1, some (nb e)), (2, some (nb tot))] none) lo hi
  for (i, want) in [(1, true), (2, true), (3, false)] do
    if ep r != e0 then r := note r "H3 crossed an epoch early; probe inconclusive" false
    let (lo, hi) := win r
    let (r', v', _) := go prog r (wr r i e0 i lo hi)
    r := note r' s!"H3c write #{i} in epoch {e0}: {v'}" (if want then v' == "admitted" else (v'.splitOn "rate limit 2").length > 1)
  let (rx, vx, _) := go prog r (wr r 3 e0 3 0 1000)
  r := note rx s!"H3d cheat: a window spanning epochs [0,1000]: {vx}" ((vx.splitOn "window spans epochs").length > 1)
  let fut := e0 + 5
  let (ry, vy, _) := go prog r (wr r 1 fut 3 (W * fut) (W * fut + W - 1))
  r := note ry s!"H3e cheat: claim future epoch {fut} by signing its window: {vy}" (vy.startsWith "rejected")
  -- advance into the next epoch with unrelated admitted turns (data objects without laws)
  let mut guardN := 0
  while ep r == e0 && guardN < 3 * W do
    let (rz, _, _) := go prog r (sg r b [] (.create none [] [(stateBase, nb guardN)]))
    r := { rz with log := r.log, bad := r.bad }
    guardN := guardN + 1
  let e1 := ep r
  let (lo, hi) := win r
  let (rw, vw, _) := go prog r (wr r 1 e1 4 lo hi)
  r := note rw s!"H3f next epoch {e1} (height {r.st.host.height}), count reset to 1: {vw}" (vw == "admitted" && e1 == e0 + 1)
  return r

def main : IO UInt32 := do
  let p := probe
  for l in p.log do IO.println l
  IO.println s!"probe: {if p.bad = 0 then "AS EXPECTED" else s!"{p.bad} unexpected"}"
  return 0
end Probe
def main : IO UInt32 := Probe.main
