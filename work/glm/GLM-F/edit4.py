import sys
path = "Lang/Journey/Gen.lean"
t = open(path).read()
old = '(package (doc \\"claims to install a package with reset\\") (state (rec))\\n" ++'
new = '(package (doc \\"claims in surface text to install a package with reset\\") (state (rec))\\n" ++'
n = t.count(old)
assert n == 1, f"count {n}"
open(path, "w").write(t.replace(old, new))
print("ok")
