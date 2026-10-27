import re

# decisions/lang.md: both sides appended at EOF. Keep HEAD's entries then ours; our row is GN26 now.
t = open("decisions/lang.md").read()
m = re.search(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n", t, re.S)
assert m, "no conflict block"
head, ours = m.group(1), m.group(2)
ours = ours.lstrip("\n").replace("GN25", "GN26")
t = t[:m.start()] + head + "\n\n" + ours + ("\n" if not t[m.end():].startswith("\n") else "") + t[m.end():]
open("decisions/lang.md", "w").write(t)
print("decisions resolved")
