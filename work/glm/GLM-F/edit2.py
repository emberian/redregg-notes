import sys

def edit(path, subs):
    with open(path) as f:
        t = f.read()
    for old, new in subs:
        if t.count(old) != 1:
            print(f"FAIL {path}: pattern count {t.count(old)} for {old[:70]!r}")
            sys.exit(1)
        t = t.replace(old, new)
    with open(path, "w") as f:
        f.write(t)
    print(f"ok {path}")

# --- Lang/Journey/Gen.lean: GN25, the surface twin of GN23 ---
edit("Lang/Journey/Gen.lean", [
    (
        '''* GN24 a bounded package whose `set` (no install or createOf arm) declares it produces an interface:
  install refused `badProduces set`.
-/''',
        '''* GN24 a bounded package whose `set` (no install or createOf arm) declares it produces an interface:
  install refused `badProduces set`.
* GN25 the same promise in the authoring text: a generator whose `generate` declares
  `(effect (moves 0) (produces …))` with `reset` in the interface is written in surface text, lowered
  and installed, and generate is refused `produces generate: lacks reset`, nothing born.
-/''',
    ),
    (
        '''  r := note r48 s!"GN24 a bounded package whose set declares it produces an interface: {v48}"
    (programRefused v48 "badProduces set")
  return r''',
        '''  r := note r48 s!"GN24 a bounded package whose set declares it produces an interface: {v48}"
    (programRefused v48 "badProduces set")
  -- GN25 the same promise written in surface text (the surface's produces clause)
  let text25? : Option String :=
    match I' with
    | .record row => (row.mapM fun (ℓ, T) => (Print.ty T).map fun t => s!"({ℓ} {t})").map fun fs =>
      "(package (doc \\"claims to install a package with reset\\") (state (rec))\\n" ++
      s!"  (method generate (calls (install)) (effect (moves 0) (produces (rec {" ".intercalate fs})))\\n" ++
      s!"    (done state (install (pkg #{hexOf bytes500})))))"
    | _ => none
  let some text25 := text25? | return note r "GN25 the declared interface has no text" false
  let .ok p25 := Surface.readPackage text25 | return note r "GN25 the surface generator reads" false
  let (r49, v49, g49?) := generator r "GN25" p25
  let some (gpkg49, G49) := g49? | return note r49 s!"GN25 {v49}" false
  let (r50, v50, t50) := generate r49 gpkg49 G49
  r := note r50 s!"GN25 the same generator written in surface text, its effect clause saying (produces (rec … reset …)) ({v49}); generate: {v50}; nothing born: {t50.isNone}"
    (programRefused v50 "produces generate: lacks reset" && t50.isNone)
  return r''',
    ),
])
