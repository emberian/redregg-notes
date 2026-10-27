open Lean Elab Command

/-- CX-FOLD-2 scratch tool (not landed): `#fold_digest_rn OUT RENAMES` writes one row per constant of the
nanodregg tree AFTER applying the rename map RENAMES (lines `old<TAB>new`; a constant is renamed by the
LONGEST map entry that is a component-wise prefix of its name, so generated constants (`.eq_1`, `.match_1`,
`._sunfold`, `.mk`, `.rec`, …) move with their owner). The rename is applied to the row's name, to every
constant in the elaborated type, and to every constant in the value before hashing. Run on the BEFORE tree;
the AFTER tree is digested with an empty map. Columns: name, module, kind, quoted type, value hash, the
renamed-from name (or `-`). -/
syntax (name := foldDigestRn) "#fold_digest_rn " str str : command

def foldRootsRn : List String :=
  ["Lang", "Kernel", "Ledger", "Host", "Hosting", "Protocol", "Census", "Codec", "Emit", "Bench", "Ops"]

partial def renamePublic (m : Std.HashMap Name Name) (n : Name) : Name :=
  let rec go (p : Name) : Option Name :=
    match m.get? p with
    | some q => some (n.replacePrefix p q)
    | none => match p with
      | .anonymous => none
      | .str q _ => go q
      | .num q _ => go q
  (go n).getD n

/-- A private name `_private.<Module>.0.<user name>` is renamed in its user-name part, and its module prefix by
the map's `_private:<OldModule>` rows (a module move changes the prefix Lean writes). -/
def renameName (m : Std.HashMap Name Name) (n : Name) : Name :=
  match Lean.privatePrefix? n, Lean.privateToUserName? n with
  | some pfx, some u => (m.getD pfx pfx) ++ renamePublic m u
  | _, _ => renamePublic m n

def privPfx (mod : String) : Name := .num (`_private ++ mod.toName) 0

def parseKey (s : String) : Name :=
  if s.startsWith "_private:" then privPfx (s.drop 9).toString else s.toName

@[command_elab foldDigestRn]
def elabFoldDigestRn : CommandElab
  | `(#fold_digest_rn $path:str $ren:str) => do
    let env ← getEnv
    let txt ← liftM (m := IO) (if ren.getString == "" then pure "" else IO.FS.readFile ren.getString)
    let mut m : Std.HashMap Name Name := {}
    for l in txt.splitOn "\n" do
      match l.splitOn "\t" with
      | [a, b] => m := m.insert (parseKey a) (parseKey b)
      | _ => pure ()
    let rn := renameName m
    let fix : Expr → Expr := fun e => e.replace fun
      | .const c us => some (.const (rn c) us)
      | _ => none
    let h ← IO.FS.Handle.mk path.getString .write
    let mut n := 0
    let mut moved := 0
    for (c, ci) in env.constants.map₁.toList do
      let some idx := env.getModuleIdxFor? c | continue
      let mod := env.header.moduleNames[idx.toNat]!
      unless foldRootsRn.contains mod.getRoot.toString do continue
      let k := Census.Journal.kind ci
      let vh : String := match ci.value? (allowOpaque := true) with
        | some v => toString (fix v).hash
        | none => "-"
      let c' := rn c
      if c' != c then moved := moved + 1
      let from_ := if c' != c then toString c else "-"
      h.putStrLn s!"{c'}\t{mod}\t{k}\t{(toString (fix ci.type)).quote}\t{vh}\t{from_}"
      n := n + 1
    h.flush
    logInfo m!"FOLD DIGEST RN: {n} constants; {m.size} map entries; {moved} constants renamed"
  | _ => throwUnsupportedSyntax
