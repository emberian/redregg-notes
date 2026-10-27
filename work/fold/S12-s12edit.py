# s12edit.py ROOT [--devtools] — S12: the P6 certificate reader leaves Lang for Census (CX-FOLD-3; GRANT R-0015)
import os, sys
R = sys.argv[1]; DEV = "--devtools" in sys.argv
def rd(p): return open(os.path.join(R, p), encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(R, p)), exist_ok=True)
    open(os.path.join(R, p), "w", encoding="utf-8").write(s)
def cut(s, a, b="", n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); return s.replace(a, b)
OLD = "Nanodregg.Lang.Contextual.Certificate"; NEW = "Census.CertificateReader"
moves = [("Lang/Contextual/Certificate.lean", "Census/CertificateReader.lean"),
         ("Lang/Proofs/Contextual/Certificate.lean", "Census/Proofs/CertificateReader.lean"),
         ("Lang/Journey/Certificate.lean", "Census/CertificateReaderTests.lean"),
         ("Lang/Journey/CertificateMain.lean", "Census/CertificateReaderMain.lean")]
imports = [("import Lang.Contextual.Certificate\n", "import Census.CertificateReader\n"),
           ("import Lang.Proofs.Contextual.Certificate\n", "import Census.Proofs.CertificateReader\n"),
           ("import Lang.Journey.Certificate\n", "import Census.CertificateReaderTests\n")]
for old, new in moves:
    s = rd(old)
    for a, b in imports: s = s.replace(a, b)
    assert OLD in s
    s = s.replace(OLD, NEW)
    wr(new, s); os.remove(os.path.join(R, old))
for p in ["Census/Certificate.lean", "Census/CertificateData.lean", "Census/Proofs/Certificate.lean"]:
    s = rd(p)
    for a, b in imports: s = s.replace(a, b)
    s = s.replace(OLD + ".", NEW + ".")
    assert "Lang.Contextual" not in s and "Lang.Proofs.Contextual" not in s, p
    wr(p, s)
lk = rd("lakefile.lean")
lk = cut(lk, """-- LANG: environment-relative certificate reader tests.
@[default_target] lean_exe «certificate-tests» where
  root := `Lang.Journey.CertificateMain""", """-- CENSUS: environment-relative certificate reader tests.
@[default_target] lean_exe «certificate-tests» where
  root := `Census.CertificateReaderMain""")
wr("lakefile.lean", lk)
if DEV:
    d = rd("devtools/certificate_plants.py")
    d = cut(d, 'root / "Lang/Contextual/Certificate.lean"', 'root / "Census/CertificateReader.lean"')
    d = cut(d, '"Lang.Proofs.Contextual.Certificate"', '"Census.Proofs.CertificateReader"')
    wr("devtools/certificate_plants.py", d)
print("s12edit: ok", "(devtools too)" if DEV else "")
