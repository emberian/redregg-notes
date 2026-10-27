import Lang.Journey.Contextual
open Nanodregg Nanodregg.Lang Nanodregg.Lang.Journey.Contextual

def wCells : Kernel.Receive.Pinned Kernel.Sim.D := fun g => if g = 77 then .ok none else noCells g

def wShow (r : Except HoleRefusal String) : String := match r with | .ok s => s!"ok {s}" | .error e => s!"refused {e.wire}"

/-- T2's plant witness: the unused bool hypothesis pinned as a CELL at its tombstone. -/
def hT2 : HoleROM :=
  { declaration with selectionRel := 5, selectionKey := key, hypotheses := [some (SupportPin.cell (Kernel.Sim.dc.bytes 77)), some (factPinAt 4)] }
#eval wShow ((selectHole Kernel.Sim.digestOf wCells (view (some 0) (some 1)) (3 : Kernel.Sim.D) hT2).map
  (fun s => s!"strengthened {s.strengthened}"))

/-- T4's plant witness: a guard that is `true` whatever its pin, the pin live. -/
def hT4 : HoleROM := { declaration with selectionRel := 5, selectionKey := key, guard := .bool true }
#eval wShow ((selectHole Kernel.Sim.digestOf noCells (view (some 0) (some 1) (blocker := some 1)) (3 : Kernel.Sim.D) hT4).map
  (fun s => s!"index {s.index}"))

/-- T3's plant witness: three hypotheses, the middle one (bool) dead and unused; code 0 uses the two nats. -/
def hT3 : HoleROM :=
  { declaration with selectionRel := 5, selectionKey := key, ctx := [.nat, .bool, .nat], hypotheses := [some (factPinAt 4), some (factPinAt 1), some (factPinAt 4)], code := [⟨.prim .add (.var 0) (.var 2), [factPinAt 2]⟩] }
#eval wShow ((selectHole Kernel.Sim.digestOf noCells (view (some 0) none) (3 : Kernel.Sim.D) hT3).map
  (fun s => s!"strengthened {s.strengthened} body-is-original {decide (s.body = s.original)}"))
