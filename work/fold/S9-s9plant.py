p = "Lang/Journey/ContextualChecks.lean"; s = open(p, encoding="utf-8").read()
a = "  let fill := fun _ => some (Term.var 0)\n"
assert s.count(a) == 1
s = s.replace(a, a + """  -- LANG-74.9 plant: a hole name whose refusal text is wider than `Bounds.reasonMax` makes the blocked
  -- hole's `.refuse` ill-typed, so the closed re-check in instantiateHoles refuses (`.instanceRecheck`).
  let wide : Nat := 10 ^ 300
  let wideP := { p with holes := [{ h with name := wide }],
    body := .record [("value", .hole wide [.bool true, .nat 7])] }
""")
b = '    ("contextual-print-mismatch", printMismatch),\n'
assert s.count(b) == 1
s = s.replace(b, """    ("recheck-arm-reachable", refusedAs (instantiateHoles (view none (some 1)) (3 : Sim.D) [] wideP) .instanceRecheck &&
      (instantiateHoles (view none (some 1)) (3 : Sim.D) [] p).isOk),
""" + b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
