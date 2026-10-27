import re

# Lang/Surface.lean: keep the faerie's kind/createOf lines and my produces lines together.
t = open("Lang/Surface.lean").read()
head = '''<<<<<<< HEAD
  "          | (method ℓ [(reads (rel (points n) | (range m k))…)] [(arg A)] [(calls (kind…)…)] [(edits n)] [(effect (moves n))] body)\\n" ++
  "          kind    ::= account | credit | grant | install | transfer | (invoke T) | (createOf T)\\n" ++
  "                      T of an invoke the argument it sends (LANG-77); T of a createOf the state of the object it births (LANG-96)\\n" ++
  "          item    ::= (kind (f e)…), in `done`: (install (pkg e)) | (createOf (pkg e) (state e)) | (transfer …) | …\\n" ++
=======
  "          | (method ℓ [(reads (rel (points n) | (range m k))…)] [(arg A)] [(calls (kind…)…)] [(edits n)] [(effect (moves n) [(produces I)])] body)\\n" ++
  "          kind    ::= account | credit | grant | install | transfer | (invoke T)   — T the argument the invoke sends (LANG-77)\\n" ++
  "          I       ::= (rec (ℓ T)…), the interface of the packages it produces: method and law names and types (LANG-103)\\n" ++
>>>>>>>'''
ours = '''  "          | (method ℓ [(reads (rel (points n) | (range m k))…)] [(arg A)] [(calls (kind…)…)] [(edits n)] [(effect (moves n) [(produces I)])] body)\\n" ++
  "          kind    ::= account | credit | grant | install | transfer | (invoke T) | (createOf T)\\n" ++
  "                      T of an invoke the argument it sends (LANG-77); T of a createOf the state of the object it births (LANG-96)\\n" ++
  "          I       ::= (rec (ℓ T)…), the interface of the packages it produces: method and law names and types (LANG-103)\\n" ++
  "          item    ::= (kind (f e)…), in `done`: (install (pkg e)) | (createOf (pkg e) (state e)) | (transfer …) | …\\n" ++'''
assert t.count(head) == 1, t.count(head)
t = t.replace(head, ours)
open("Lang/Surface.lean", "w").write(t)
print("surface resolved")
