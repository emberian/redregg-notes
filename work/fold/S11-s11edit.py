# s11edit.py ROOT — S11: the Trace split. collect -> Lang/StdHoleModel (Nanodregg.Lang.Std), its three lemmas ->
# Lang/Proofs/StdHoleCoverage; the rest of C/Trace and P/Trace deleted (CX-FOLD-3)
import os, sys
R = sys.argv[1]
def rd(p): return open(os.path.join(R, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(R, p), "w", encoding="utf-8").write(s)
def cut(s, a, b=""):
    assert s.count(a) == 1, (a[:80], s.count(a)); return s.replace(a, b)
def between(s, a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

ct = rd("Lang/Contextual/Trace.lean")
collect = between(ct, "/-- Bounded complete collection; the first omitted read refuses by its key.", "/-- Coverage comes from the guard declaration")
pt = rd("Lang/Proofs/Contextual/Trace.lean")
lemmas = between(pt, "/-- Successful collection establishes coverage and exact values, assuming only that PROVIDED", "/-- Cache coherence is an independently checkable relation")
assert collect.count("def collect") == 1 and lemmas.count("theorem") == 3

hm = rd("Lang/StdHoleModel.lean")
hm = cut(hm, "import Lang.Contextual.Trace\n")
anchor = "/-- P10's complete collector, specialized to the emitted finite dependency"
hm = cut(hm, anchor, collect + anchor)
hm = cut(hm, "  (Contextual.Trace.collect\n", "  (collect\n")
wr("Lang/StdHoleModel.lean", hm)

hc = rd("Lang/Proofs/StdHoleCoverage.lean")
hc = cut(hc, "import Lang.Proofs.Contextual.Trace\n")
hc = cut(hc, "    Contextual.Trace.collect, Except.map]", "    collect, Except.map]")
anchor = "/-- The actual emitted check equals P10 collect on all eight coverage cases."
hc = cut(hc, anchor, lemmas + anchor)
wr("Lang/Proofs/StdHoleCoverage.lean", hc)

os.remove(os.path.join(R, "Lang/Contextual/Trace.lean"))
os.remove(os.path.join(R, "Lang/Proofs/Contextual/Trace.lean"))
print("s11edit: ok")
