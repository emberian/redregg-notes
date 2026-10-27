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

# --- docs/spec/2-structure.md: the method-effect grammar ---
edit("docs/spec/2-structure.md", [
    (
        '''```
grade ::= { moves n }
```

`moves` bounds the sum of `amount` over the `transfer` and `credit` calls one run returns.
A method with no grade has the grade `{ moves 0 }`.
Lean: `Lang/Package.lean` `structure Effect`, `Package.effectOf`.''',
        '''```
grade ::= { moves n } | { moves n, produces I }
```

`moves` bounds the sum of `amount` over the `transfer` and `credit` calls one run returns.
A method with no grade has the grade `{ moves 0 }`.
`produces I` names the interface every package the run installs or makes must have: a record of
method and law names and types, the same shape a package's interface has (LANG-103).
The core text writes the grade as `(ℓ n)` or `(ℓ n I)`; the surface writes the clause
`(effect (moves n) [(produces I)])`, `I` that record written as a type.
Lean: `Lang/Package.lean` `structure Effect`, `Package.effectOf`, `producesOk`.''',
    ),
    (
        '''         [(effects (ℓ n)…)] [(claims (keeps ℓ ℓ)…)] [(holes holerom…)])''',
        '''         [(effects (ℓ n [I])…)] [(claims (keeps ℓ ℓ)…)] [(holes holerom…)])''',
    ),
])
