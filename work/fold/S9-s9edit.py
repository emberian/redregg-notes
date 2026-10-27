# S9 edit script (CX-FOLD-2): the deployed half. Run in wt/cxfold root at ac34521.
import re
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)
def sub1(s, a, b, p):
    assert s.count(a) == 1, (p, a[:80], s.count(a)); return s.replace(a, b)
def edit(p, pairs):
    s = rd(p)
    for a, b in pairs: s = sub1(s, a, b, p)
    wr(p, s)

# --- Bounds: the four hole bounds, named
edit("Lang/Bounds.lean", [("/-- The machine's stack bound.", """/-- A contextual hole's ROM lists at most this many candidate codes (`HoleROM.check`, LANG-P7). -/
def holeCandidatesMax : Nat := 64

/-- A package declares at most this many contextual holes (`Package.checkContextual`, LANG-P7). -/
def holeSignatureMax : Nat := 16

/-- The guard allowance of one contextual hole (LANG-P7): the ticks its selection guard may run
(`runHoleGuard`'s fuel), and so the preparation charged per declared hole (`Package.holeCharge`). One
allowance, two uses; not `reasonMax`/`docMax`, which are other facts that happen to be 256 too. -/
def holeGuardFuel : Nat := 256

/-- The machine's stack bound.""")])

# --- HoleBudget: fillBounded refuses with its own two bounds
edit("Lang/HoleBudget.lean", [
 ("/-- Refuse oversized expansion before constructing it.",
  "/-- The two expansion bounds `fillBounded` refuses by name. -/\ninductive ExpansionBound where\n  | work\n  | size\n  deriving DecidableEq, Repr\n\n/-- Refuse oversized expansion before constructing it."),
 ("(σ : Nat → Option Term) (t : Term) : Except String Term :=\n  if Term.nodes t * (candidateMax + 1) > limit then .error \"holeWorkBound\"\n  else if Term.fillNodes σ t > limit then .error \"holeSizeBound\"",
  "(σ : Nat → Option Term) (t : Term) : Except ExpansionBound Term :=\n  if Term.nodes t * (candidateMax + 1) > limit then .error .work\n  else if Term.fillNodes σ t > limit then .error .size")])

# --- LiveHoles: one refusal type, named bounds, one charge
s = rd("Lang/LiveHoles.lean")
s = sub1(s, "open Nanodregg.Kernel Nanodregg.Kernel.Receive\n", """open Nanodregg.Kernel Nanodregg.Kernel.Receive

/-- Why live contextual preparation refuses: one constructor per refusal (law 7). `wire` is the one printer;
its text is what the kernel's `Refusal.program` and a blocked hole's `.refuse` carry. -/
inductive HoleRefusal where
  | type (hole : Nat)
  | context (hole : Nat)
  | candidates (hole : Nat)
  | guardType (hole : Nat)
  | candidateType (hole code : Nat)
  | package (e : CheckError)
  | signatureBound
  | duplicate
  | bodyType (e : TypeErr)
  | unpinned
  | supportMoved (hole position : Nat)
  | guardBlocked (hole : Nat)
  | guardFault (hole : Nat)
  | selectionAbsent (hole : Nat)
  | selectionType (hole : Nat)
  | selectionIndex (hole : Nat)
  | derivationMoved (hole : Nat)
  | expansion (b : ExpansionBound)
  | provenance
  | instanceRecheck
  | instanceType (e : TypeErr)

def HoleRefusal.wire : HoleRefusal → String
  | .type n => s!"holeType {n}"
  | .context n => s!"holeContext {n}"
  | .candidates n => s!"holeCandidates {n}"
  | .guardType n => s!"holeGuardType {n}"
  | .candidateType n i => s!"holeCandidateType {n} {i}"
  | .package e => e.wire
  | .signatureBound => "holeSignatureBound"
  | .duplicate => "holeDuplicate"
  | .bodyType e => s!"holeBodyType {e.text}"
  | .unpinned => "holeUnpinned"
  | .supportMoved n i => s!"holeSupportMoved {n} {i}"
  | .guardBlocked n => s!"holeGuardBlocked {n}"
  | .guardFault n => s!"holeGuardFault {n}"
  | .selectionAbsent n => s!"holeSelectionAbsent {n}"
  | .selectionType n => s!"holeSelectionType {n}"
  | .selectionIndex n => s!"holeSelectionIndex {n}"
  | .derivationMoved n => s!"holeDerivationMoved {n}"
  | .expansion .work => "holeWorkBound"
  | .expansion .size => "holeSizeBound"
  | .provenance => "holeProvenance"
  | .instanceRecheck => "holeInstanceType"
  | .instanceType e => s!"holeInstanceType {e.text}"
""", "LiveHoles")
reps = [
 ("def HoleROM.check (Δ : List Ty) (h : HoleROM) : Except String Unit := do", "def HoleROM.check (Δ : List Ty) (h : HoleROM) : Except HoleRefusal Unit := do"),
 ('throw s!"holeType {h.name}"', "throw (.type h.name)"),
 ('throw s!"holeContext {h.name}"', "throw (.context h.name)"),
 ('unless h.code.length ≤ 64 do throw s!"holeCandidates {h.name}"', "unless h.code.length ≤ Bounds.holeCandidatesMax do throw (.candidates h.name)"),
 ("  match inferE [] [.bool] h.guard with", "  match inferE [] [.bool] h.guard (Ω := []) with"),
 ('| _ => throw s!"holeGuardType {h.name}"', "| _ => throw (.guardType h.name)"),
 ("    match inferE Δ h.ctx c.body with\n    | .ok T => unless T = h.ty do throw s!\"holeCandidateType {h.name} {i}\"\n    | .error _ => throw s!\"holeCandidateType {h.name} {i}\"",
  "    match inferE Δ h.ctx c.body (Ω := []) with\n    | .ok T => unless T = h.ty do throw (.candidateType h.name i)\n    | .error _ => throw (.candidateType h.name i)"),
 ("def Package.checkContextual (Δ : List Ty) (p : Package) : Except String Unit := do\n  match p.checkShape with | .error e => throw e.wire | .ok () => pure ()\n  match p.checkFields with | .error e => throw e.wire | .ok () => pure ()\n  unless p.holes.length ≤ 16 do throw \"holeSignatureBound\"\n  unless (p.holes.map (·.name)).eraseDups.length = p.holes.length do throw \"holeDuplicate\"",
  "def Package.checkContextual (Δ : List Ty) (p : Package) : Except HoleRefusal Unit := do\n  match p.checkShape with | .error e => throw (.package e) | .ok () => pure ()\n  match p.checkFields with | .error e => throw (.package e) | .ok () => pure ()\n  unless p.holes.length ≤ Bounds.holeSignatureMax do throw .signatureBound\n  unless (p.holes.map (·.name)).eraseDups.length = p.holes.length do throw .duplicate"),
 ("  match checkE Δ p.body p.iface (Ω := holeSignature p.holes) with\n  | .error e => throw s!\"holeBodyType {e.text}\"",
  "  match checkE Δ p.body p.iface (Ω := holeSignature p.holes) with\n  | .error e => throw (.bodyType e)"),
 ("    Except String (Option RowLeaf) :=\n  match (rv.points self rel).find? (fun p => decide (p.1 = key)) with\n  | none => .error \"holeUnpinned\"",
  "    Except HoleRefusal (Option RowLeaf) :=\n  match (rv.points self rel).find? (fun p => decide (p.1 = key)) with\n  | none => .error .unpinned"),
 ("    Except String (List Nat) :=", "    Except HoleRefusal (List Nat) :="),
 ('else if Term.usesVar pi.2 c.body then .error s!"holeSupportMoved {h.name} {pi.2}"', "else if Term.usesVar pi.2 c.body then .error (.supportMoved h.name pi.2)"),
 ("def runHoleGuard {D : Type} (rv : RowView D) (self : D) (h : HoleROM) : Except String Nat := do", "def runHoleGuard {D : Type} (rv : RowView D) (self : D) (h : HoleROM) : Except HoleRefusal Nat := do"),
 ("  match run [] Bounds.stackMax 256 0 (State.init h.guard [.bool present]) with", "  match run [] Bounds.stackMax Bounds.holeGuardFuel 0 (State.init h.guard [.bool present]) with"),
 ('  | .value (.bool false) _ => .error s!"holeGuardBlocked {h.name}"\n  | _ => .error s!"holeGuardFault {h.name}"', "  | .value (.bool false) _ => .error (.guardBlocked h.name)\n  | _ => .error (.guardFault h.name)"),
 ("def selectHole {D : Type} (rv : RowView D) (self : D) (h : HoleROM) : Except String HoleSelection := do", "def selectHole {D : Type} (rv : RowView D) (self : D) (h : HoleROM) : Except HoleRefusal HoleSelection := do"),
 ('| throw s!"holeSelectionAbsent {h.name}"', "| throw (.selectionAbsent h.name)"),
 ('| throw s!"holeSelectionType {h.name}"', "| throw (.selectionType h.name)"),
 ('| throw s!"holeSelectionIndex {h.name}"', "| throw (.selectionIndex h.name)"),
 ('do throw s!"holeDerivationMoved {h.name}"', "do throw (.derivationMoved h.name)"),
 ("  | blocked (name : Nat) (ty : Ty) (reason : String)", "  | blocked (name : Nat) (ty : Ty) (reason : HoleRefusal)"),
 ("  | .blocked _ T why => .refuse T why.toUTF8", "  | .blocked _ T why => .refuse T why.wire.toUTF8"),
 ("    Except String HoleInstance := do", "    Except HoleRefusal HoleInstance := do"),
 ("  let body ← Term.fillBounded Wire.nodeMax (resolutionMax rs) (resolutionEnv rs) p.body\n",
  "  let body ← (Term.fillBounded Wire.nodeMax (resolutionMax rs) (resolutionEnv rs) p.body).mapError .expansion\n"),
 ('ss.flatMap (fun s => s.original.digestLits)).any (fun a => decide (a = b))) do throw "holeProvenance"', 'ss.flatMap (fun s => s.original.digestLits)).any (fun a => decide (a = b))) do throw .provenance'),
 ("  match checkE Δ body p.iface with\n  | .error _ => throw \"holeInstanceType\"\n  | .ok () =>\n    pure ⟨body, ss, rs, if p.holes.isEmpty then 0 else\n      Term.nodes p.body * (resolutionMax rs + 1) + 256 * rs.length⟩",
  "  match checkE Δ body p.iface (Ω := []) with\n  | .error _ => throw .instanceRecheck\n  | .ok () => pure ⟨body, ss, rs, p.holeCharge (resolutionMax rs)⟩"),
 ("/-- Actual syntax cost and guard steps are charged before evaluation.",
  "/-- THE preparation charge of a contextual package, at the largest candidate size `m` it may expand: the\nexpansion bound of `Term.fillBounded` plus one guard allowance (`Bounds.holeGuardFuel`) per declared hole;\nthe same formula at two different `m`s, not the same number. The invocation's\nactual cost is this at the resolved candidates (`instantiateHoles`); the static charge is this at the largest\ncommitted candidate (`Package.preparationCost`). -/\ndef Package.holeCharge (p : Package) (m : Nat) : Nat :=\n  if p.holes.isEmpty then 0\n  else Term.nodes p.body * (m + 1) + Bounds.holeGuardFuel * p.holes.length\n\n/-- Actual syntax cost and guard steps are charged before evaluation."),
]
for a, b in reps: s = sub1(s, a, b, "LiveHoles")
assert '"hole' not in s.split("def HoleRefusal.wire")[0].split("inductive HoleRefusal")[0], "leftover"
wr("Lang/LiveHoles.lean", s)

# --- Program: the contextual loader carries HoleRefusal; one charge
edit("Lang/Program.lean", [
 ("def unresolvedBody (p : Package) : Except String Term :=\n  if p.holes.isEmpty then .ok p.body\n  else Term.fillBounded Wire.nodeMax 1",
  "def unresolvedBody (p : Package) : Except HoleRefusal Term :=\n  if p.holes.isEmpty then .ok p.body\n  else HoleRefusal.expansion <$> Term.fillBounded Wire.nodeMax 1"),
 ("def admitContextual (prepare : List Ty → Package → Except String Term)", "def admitContextual (prepare : List Ty → Package → Except HoleRefusal Term)"),
 ("    match p.checkContextual ifs with\n    | .error e => .error (.program e)\n    | .ok () =>\n      match prepare ifs p with\n      | .error e => .error (.program e)\n      | .ok body =>\n        match checkE ifs body p.iface with\n        | .error e => .error (.program s!\"holeInstanceType {e.text}\")",
  "    match p.checkContextual ifs with\n    | .error e => .error (.program e.wire)\n    | .ok () =>\n      match prepare ifs p with\n      | .error e => .error (.program e.wire)\n      | .ok body =>\n        match checkE ifs body p.iface (Ω := []) with\n        | .error e => .error (.program (HoleRefusal.instanceType e).wire)"),
 ("def Package.preparationCost (p : Package) : Nat :=\n  if p.holes.isEmpty then 0\n  else Term.nodes p.body *\n    (1 + (p.holes.flatMap (fun h => h.code)).foldl\n      (fun n c => max n (Term.nodes c.body)) 1) + 256 * p.holes.length",
  "def Package.preparationCost (p : Package) : Nat :=\n  p.holeCharge ((p.holes.flatMap (fun h => h.code)).foldl (fun n c => max n (Term.nodes c.body)) 1)"),
 ("  match p.checkContextual ifaces with\n  | .error e => throw (.program e)\n  | .ok () => checkROMLits digestOf p", "  match p.checkContextual ifaces with\n  | .error e => throw (.program e.wire)\n  | .ok () => checkROMLits digestOf p"),
])

# --- StdContextualHole: its generator stays Except String; checkContextual's refusal is printed
s = rd("Lang/StdContextualHole.lean")
n = s.count("  p.checkContextual (")
assert n == 2, n
s = s.replace("  p.checkContextual (bundle.libraries.map (·.iface))\n", "  (p.checkContextual (bundle.libraries.map (·.iface))).mapError HoleRefusal.wire\n")
s = s.replace("  p.checkContextual (b.libraries.map (·.iface))\n", "  (p.checkContextual (b.libraries.map (·.iface))).mapError HoleRefusal.wire\n")
wr("Lang/StdContextualHole.lean", s)

# --- Check: no default hole signature
s = rd("Lang/Check.lean")
k = s.count("(Ω : HoleSignature := [])")
assert k == 7, k
s = s.replace("(Ω : HoleSignature := [])", "(Ω : HoleSignature)")
wr("Lang/Check.lean", s)
print("ok")
