import sys
t = open("Lang/Surface.lean").read()
# the leftover label of the conflict marker glued after the item line
frag = '" ++ b91bc1d2 (lang: a method' + chr(39) + 's effect clause in the authoring text can name the interface it produces (LANG-103' + chr(39) + 's surface form))\n'
n = t.count(frag)
assert n == 1, f"count {n}"
open("Lang/Surface.lean", "w").write(t.replace(frag, '" ++\n'))
print("ok")
