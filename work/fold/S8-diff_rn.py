"""diff_rn.py BEFORE_RN AFTER DELNAMES MOVEDMODS [LIST] — the census digest diff of a MOVE step (CX-FOLD-2).
BEFORE_RN is the before tree digested under the step's rename map (mkdigest_rn.sh), AFTER the candidate under the
empty map. DELNAMES: one declared deleted name per line (component-wise prefix: generated constants go with it).
MOVEDMODS: modules the step moves code out of (one per line). The verdict lines:
  every vanished name is declared; no surviving statement (renamed) changes; every module change starts in a
  moved module. Prints every exceptional name (no truncation) when LIST is given, else at most 60."""
import hashlib, sys, collections, re
# Binder names are not part of a statement. A hygienic binder name embeds its module and a counter
# (x._@.Lang.HoleDecl.1180826132._hygCtx._hyg.10), so a module move changes it: erase every one.
HYG = re.compile(r"[^\s():\[\]{}]*\._@\.[^\s():\[\]{}]*?\._hyg\.[0-9]+")
def load(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        f = l.rstrip("\n").split("\t")
        d[f[0]] = (f[1], f[2], hashlib.sha256(HYG.sub("_hyg_", f[3]).encode()).hexdigest(), f[4], f[5] if len(f) > 5 else "-")
    return d
b, a = load(sys.argv[1]), load(sys.argv[2])
dels = [l.strip() for l in open(sys.argv[3]) if l.strip()]
moved = {l.strip() for l in open(sys.argv[4]) if l.strip()}
full = len(sys.argv) > 5
def declared(n):
    return any(n == d or n.startswith(d + ".") for d in dels)
gone = sorted(n for n in b if n not in a); new = sorted(n for n in a if n not in b)
undecl = [n for n in gone if not declared(n)]
tchg = sorted(n for n in b if n in a and b[n][2] != a[n][2])
vchg = sorted(n for n in b if n in a and b[n][3] != a[n][3])
mchg = sorted(n for n in b if n in a and b[n][0] != a[n][0])
mbad = [n for n in mchg if b[n][0] not in moved]
ren = sum(1 for n in b if b[n][4] not in ("-", ""))
print("before", len(b), "(rows carrying a renamed-from name:", ren, ") after", len(a))
print("vanished", len(gone), "declared", len(gone) - len(undecl), "UNDECLARED", len(undecl))
print("new", len(new), "type-digest changed", len(tchg), "value-hash changed", len(vchg))
print("module changed", len(mchg), "of which from a module the step does not move", len(mbad))
pairs = collections.Counter((b[n][0], a[n][0]) for n in mchg)
for (x, y), c in sorted(pairs.items()): print("   module", x, "->", y, c)
lim = None if full else 60
for tag, xs in (("VANISHED", gone), ("UNDECLARED", undecl), ("NEW", new), ("TYPE", tchg), ("VALUE", vchg), ("MODBAD", mbad)):
    for n in xs[:lim]: print("  ", tag, n, b.get(n, a.get(n))[0])

# For every constant whose value changed, compare the multiset of its abstracted sub-proofs' statements
# (`n._proof_*`) before and after: a renumbering keeps the multiset; a changed sub-proof does not.
def auxset(d, n):
    return sorted(d[m][2] for m in d if m.startswith(n + "._proof_"))
for n in vchg:
    if "._proof_" in n: continue
    xb, xa = auxset(b, n), auxset(a, n)
    if xb or xa:
        print("   AUX", n, "sub-proofs before", len(xb), "after", len(xa), "statement multisets equal:", xb == xa)
