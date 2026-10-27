import Lang.Surface
import Lang.Print
import Lang.Bell
open Nanodregg.Lang
def main (args : List String) : IO UInt32 := do
  let src ← IO.FS.readFile "world/resident/Bell.ob"
  match Surface.readPackage src with
  | .error e => IO.println s!"REFUSED {e.text src}"; return 1
  | .ok p =>
    let some core := Print.package p | IO.println "no core text"; return 1
    if args = ["--write"] then IO.FS.writeFile "world/resident/Bell" core
    IO.println s!"core {core.length} chars; methods {p.methods}; rels {p.rels.map (·.1)}; laws {p.laws}"
    match p.checkWith [] with
    | .ok () => IO.println "checkWith: ok"
    | .error e => IO.println s!"checkWith: REFUSED {e.text}"
    IO.println s!"package bytes {(Wire.encodePackage p).map (·.size)} (eventBytesMax {Nanodregg.Kernel.Bounds.eventBytesMax})"
    let E := editTy p.rels
    IO.println s!"E text {((Print.ty E).map (·.length))}"
    for (ℓ, d) in p.rels do IO.println s!"rel {ℓ}: val text {((Print.ty d.val).map (·.length))}; relEditTy text {((Print.ty (relEditTy d)).map (·.length))}"
    match p.iface with
    | .record ts => for (n, T) in ts do IO.println s!"iface {n}: {((Print.ty T).map (·.length))}"
    | _ => pure ()
    match p.body with
    | .record fs => for (n, t) in fs do IO.println s!"body {n}: {((Print.term t).map (·.length))}"
    | _ => pure ()
    let .record fs := p.body | IO.println "body not a record"; return 1
    for n in ["answer", "ring", "aimed", "rung"] do
      match Row.find? n fs with
      | some t => IO.println s!"== {n}\n{(Print.term t).getD "?"}"
      | none => IO.println s!"== {n} MISSING"
    match p.iface with
    | .record ts => for n in ["answer", "ring"] do IO.println s!"== ty {n}\n{((Row.find? n ts).bind Print.ty).getD "?"}"
    | _ => pure ()
    IO.println s!"shapeOk: {Bell.shapeOk p}; imports {decide (p.imports = [])}; holes {decide (p.holes = [])}; state {decide (p.state = Bell.S)}; rels {decide (p.rels = Bell.rels)}"
    let .record ts := p.iface | return 1
    IO.println s!"answerTy {decide (Row.find? "answer" ts = some Bell.answerTy)}"
    let .record fs := p.body | return 1
    IO.println s!"answer term {decide (Row.find? "answer" fs = some Bell.answer)}; rung term {decide (Row.find? "rung" fs = some Bell.rung)}"
    let firstDiff (x y : String) : String :=
      let i := (List.range (min x.length y.length)).find? (fun i => x.toList[i]! != y.toList[i]!)
      match i with
      | some i => s!"first diff at {i}:\n  got  …{String.ofList (x.toList.drop (i - 60) |>.take 160)}\n  want …{String.ofList (y.toList.drop (i - 60) |>.take 160)}"
      | none => s!"no diff in the common prefix (lengths {x.length} {y.length})"
    match Row.find? "answer" fs, Print.term Bell.answer with
    | some t, some w => if t != Bell.answer then IO.println (firstDiff ((Print.term t).getD "") w) else pure ()
    | _, _ => IO.println "answer: unprintable"
    match Row.find? "answer" ts, Print.ty Bell.answerTy with
    | some T, some w => if T != Bell.answerTy then IO.println ("TY " ++ firstDiff ((Print.ty T).getD "") w) else pure ()
    | _, _ => IO.println "answerTy: unprintable"
    match Row.find? "rung" fs, Print.term Bell.rung with
    | some t, some w => if t != Bell.rung then IO.println ("RUNG " ++ firstDiff ((Print.term t).getD "") w) else pure ()
    | _, _ => IO.println "rung: unprintable"
    return 0
