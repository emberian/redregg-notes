t = open("Lang/Journey/Gen.lean").read()
old = "let (r52, v52, t52) := generate r51 gpkg49 G49"
new = "let (r52, v52, t52) := generate r51 gpkg51 G51"
n = t.count(old)
assert n == 1, f"count {n}"
open("Lang/Journey/Gen.lean", "w").write(t.replace(old, new))
print("ok")
