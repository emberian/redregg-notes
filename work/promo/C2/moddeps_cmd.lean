open Lean Elab Command

/-- CX-PROMO-2 scratch tool (not landed): `#promo_moddeps OUT MODS` writes one row per constant of a module NOT in
MODS whose elaborated type or value uses a constant DEFINED in a module in MODS: name, module, used constants. -/
syntax (name := promoModdeps) "#promo_moddeps " str str : command

@[command_elab promoModdeps]
def elabPromoModdeps : CommandElab
  | `(#promo_moddeps $path:str $mods:str) => do
    let env ← getEnv
    let txt ← liftM (m := IO) (IO.FS.readFile mods.getString)
    let ms : List String := (txt.splitOn "\n").filterMap (fun l => if l.trim.isEmpty then none else some l.trim)
    let roots := ["Lang", "Kernel", "Ledger", "Host", "Hosting", "Protocol", "Census", "Codec", "Emit", "Bench", "Ops"]
    let modOf (n : Name) : Option String := (env.getModuleIdxFor? n).map fun i => (env.header.moduleNames[i.toNat]!).toString
    let mut out := ""
    let mut defd : Nat := 0
    for (n, ci) in env.constants.toList do
      let some mod := modOf n | continue
      if ms.contains mod then defd := defd + 1; continue
      unless roots.any (fun r => mod == r || mod.startsWith (r ++ ".")) do continue
      let used := (ci.type.getUsedConstants ++ (match ci.value? with | some v => v.getUsedConstants | none => #[])).filter
        (fun c => match modOf c with | some m => ms.contains m | none => false)
      if used.isEmpty then continue
      out := out ++ s!"{n}\t{mod}\t{",".intercalate (used.toList.map toString).eraseDups}\n"
    liftM (m := IO) (IO.FS.writeFile path.getString (s!"# constants defined in MODS: {defd}\n" ++ out))
  | _ => throwUnsupportedSyntax
