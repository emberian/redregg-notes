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

# --- Lang/Surface.lean ---
edit("Lang/Surface.lean", [
    # grammar: the method line gains the produces clause, and a line for I
    (
        '''  "          | (method ℓ [(reads (rel (points n) | (range m k))…)] [(arg A)] [(calls (kind…)…)] [(edits n)] [(effect (moves n))] body)\\n" ++
  "          kind    ::= account | credit | grant | install | transfer | (invoke T)   — T the argument the invoke sends (LANG-77)\\n" ++''',
        '''  "          | (method ℓ [(reads (rel (points n) | (range m k))…)] [(arg A)] [(calls (kind…)…)] [(edits n)] [(effect (moves n) [(produces I)])] body)\\n" ++
  "          kind    ::= account | credit | grant | install | transfer | (invoke T)   — T the argument the invoke sends (LANG-77)\\n" ++
  "          I       ::= (rec (ℓ T)…), the interface of the packages it produces: method and law names and types (LANG-103)\\n" ++''',
    ),
    # the field's doc
    (
        '''  /-- `(effect (moves N))`: the method's grades (LANG-89) -/
  effect : Option Effect := none''',
        '''  /-- `(effect (moves N) [(produces I)])`: the method's grades (LANG-89), `I` the interface of the
  packages it produces (LANG-103), written as the surface writes a package's interface: a record of
  method and law names and types -/
  effect : Option Effect := none''',
    ),
    # the signature takes the context: the produces interface is read by the surface's own type reader
    (
        "def methodHead (h : MethodHead) : List SExp → P (MethodHead × SExp)",
        "def methodHead (c : Ctx) (h : MethodHead) : List SExp → P (MethodHead × SExp)",
    ),
    (
        "    methodHead { h with reads := Row.sort reads } rest",
        "    methodHead c { h with reads := Row.sort reads } rest",
    ),
    (
        "  | .list _ [.atom _ \"arg\", a] :: rest => methodHead { h with arg := a } rest",
        "  | .list _ [.atom _ \"arg\", a] :: rest => methodHead c { h with arg := a } rest",
    ),
    (
        "    methodHead { h with calls } rest",
        "    methodHead c { h with calls } rest",
    ),
    (
        "    | some n => methodHead { h with edits := n } rest",
        "    | some n => methodHead c { h with edits := n } rest",
    ),
    # the moves-only case, then the producing case beside it
    (
        '''  | .list q [.atom _ "effect", .list _ [.atom _ "moves", .atom r n]] :: rest =>
    if h.effect.isSome then .error (.duplicate q "effect") else
    match n.toNat? with
    | some n => methodHead { h with effect := some { moves := n } } rest
    | none => .error (.badClause r)''',
        '''  | .list q [.atom _ "effect", .list _ [.atom _ "moves", .atom r n]] :: rest =>
    if h.effect.isSome then .error (.duplicate q "effect") else
    match n.toNat? with
    | some n => methodHead c { h with effect := some { moves := n } } rest
    | none => .error (.badClause r)
  | .list q [.atom _ "effect", .list _ [.atom _ "moves", .atom r n], .list _ [.atom _ "produces", i]] :: rest =>
    if h.effect.isSome then .error (.duplicate q "effect") else
    match n.toNat? with
    | some n => do
      let I ← ty c Read.depthMax i
      methodHead c { h with effect := some { moves := n, produces := some I } } rest
    | none => .error (.badClause r)''',
    ),
    (
        "  let (h, body) ← methodHead {} xs",
        "  let (h, body) ← methodHead c {} xs",
    ),
])

# --- Lang/Read.lean: the core grammar's effects entry ---
edit("Lang/Read.lean", [
    (
        '''  "            (body e) [(effects (l n)…)] [(claims (keeps INV LAW)…)] [(holes hole…)])\\n" ++''',
        '''  "            (body e) [(effects (l n [I])…)] [(claims (keeps INV LAW)…)] [(holes hole…)])\\n" ++''',
    ),
])
