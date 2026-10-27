# s10edit.py ROOT — S10: P9's all-environment provenance replaces the env-specialized twin (CX-FOLD-3)
import os, re, sys
R = sys.argv[1]
def rd(p): return open(os.path.join(R, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(R, p), "w", encoding="utf-8").write(s)
def cut(s, a, b=""):
    assert s.count(a) == 1, (a[:80], s.count(a)); return s.replace(a, b)

# 1. C/Provenance's definitions (without `specialize`) replace the twin in C/Closure.
p9 = rd("Lang/Contextual/Provenance.lean")
body = p9.split("variable {D : CalculusData} {E : Type}\n", 1)[1].rsplit("end Nanodregg.Lang.Contextual.P9", 1)[0]
body = cut(body, '''/-- The original token polynomial recovered by evaluating precisely envLits (Prop15 p20). -/
def specialize (I : Iface D E) (env : E) (ms : List (Monomial D)) :
    List (List Token × List Token) :=
  (ms.filter (Monomial.envOK I env)).map fun m => (m.supports, m.blockers)

''')
body = cut(body, '''/-- Grädel–Tannen §6 p19: no environment argument, hence no erased guard branch.
Only the immutable typing problem is specialized. -/''', '''/-- THE provenance polynomial of a hole (Grädel–Tannen §6 p19): one monomial per well-typed candidate. It has
no environment argument: the guard and the budget stay literals of the monomial (`envLits`), so the same
polynomial answers at every world (`provenance_iff`). Only the immutable typing problem is specialized. -/''')
header = '''/-! ## Provenance

Finite dual-literal provenance, retaining environmental conditions: Grädel–Tannen (2024), Def4 p9, §6
pp19–20; de Kleer (1986), pp144–145. Candidates are Doyle (1979) IN/OUT justifications, not ATMS labels. The
computed polynomial is a label; its Boolean image forgets multiplicity, not conditions. -/

'''
cl = rd("Lang/Contextual/Closure.lean")
cl = cut(cl, '''/-- The provenance polynomial of a hole at a world: one monomial (a product of tokens) per candidate
that passes everything but its supports; the hole is justified iff some monomial is all live. -/
def provenance (I : Iface D E) (env : E) (cs : List (Candidate D)) :
    List (List Token × List Token) :=
  (cs.filter fun c => D.check I.ctx c.filling I.ty && I.guard env c.filling &&
      decide (c.cost ≤ I.budget)).map fun c => (effSupports I c, c.blockers)

''', header + body.strip("\n") + "\n\n")
wr("Lang/Contextual/Closure.lean", cl)
os.remove(os.path.join(R, "Lang/Contextual/Provenance.lean"))

# 2. P/Provenance: namespace P9 -> Contextual; the two theorems about the twin go with it.
pp = rd("Lang/Proofs/Contextual/Provenance.lean")
pp = cut(pp, "import Lang.Contextual.Provenance\n")
pp = cut(pp, "/- P9: all-environment bridge and the ATMS label discipline. -/", "/- Provenance: the all-environment bridge and the ATMS label discipline (P9). -/")
pp = cut(pp, "namespace Nanodregg.Lang.Contextual.P9\n", "namespace Nanodregg.Lang.Contextual\n")
pp = cut(pp, "end Nanodregg.Lang.Contextual.P9", "end Nanodregg.Lang.Contextual")
pp = cut(pp, '''/-- Grädel–Tannen §6 pp19–20: the SAME retained polynomial works for EVERY world/environment.
This new namespace preserves the landed fixed-environment theorem and its name. -/''', '''/-- **The provenance bridge** (Grädel–Tannen §6 pp19–20): a hole has a verified candidate at `w` iff some
monomial of its ONE retained polynomial evaluates true at `w`, for EVERY world and environment. This is the
bridge to `judge_verified_iff`. -/''')
i = pp.index("/-- Grädel–Tannen Prop15 p20: specializing retained env literals recovers the old polynomial,")
j = pp.index("/-- Grädel–Tannen Def4 p9: complementary token literals cannot both evaluate to true. -/")
pp = pp[:i] + pp[j:]
wr("Lang/Proofs/Contextual/Provenance.lean", pp)

# 3. Judge: the env-specialized provenance_iff goes with its def.
jd = rd("Lang/Proofs/Contextual/Judge.lean")
i = jd.index("/-- **The provenance bridge.** `provenance I env cs` is a polynomial over tokens computed from the")
j = jd.index("/-- **The obstruction is real.**")
assert "theorem provenance_iff" in jd[i:j] and jd[i:j].count("theorem") == 1
jd = jd[:i] + jd[j:]
wr("Lang/Proofs/Contextual/Judge.lean", jd)

# 4. ClosureStatements: Monomial.holds had only the twin's theorem.
cs = rd("Lang/Proofs/Contextual/ClosureStatements.lean")
cs = cut(cs, '''/-- A monomial holds in a world: its positive literals live, its negative literals dead. -/
def Monomial.holds (w : World E) (m : List Token × List Token) : Prop :=
  (∀ t ∈ m.1, w.live t = true) ∧ (∀ b ∈ m.2, w.live b = false)

''')
wr("Lang/Proofs/Contextual/ClosureStatements.lean", cs)

# 5. The twin's tooth has no subject.
os.remove(os.path.join(R, "Lang/Proofs/Contextual/ProvenanceTeeth.lean"))

# 6. tm_decEq_toy: the reflexive conjunct proves nothing about the instance.
co = rd("Lang/Proofs/Contextual/Core.lean")
co = cut(co, '''theorem tm_decEq_toy :
    (Tm.letbox (.box [.base] (.var 0)) (.mvar 0 [.var 0]) ≠
      .letbox (.box [.base] (.var 0)) (.mvar 0 [.var 1])) ∧
    Tm.mvar 3 [.lam .base (.var 0)] = Tm.mvar 3 [.lam .base (.var 0)] := by decide''', '''theorem tm_decEq_toy :
    Tm.letbox (.box [.base] (.var 0)) (.mvar 0 [.var 0]) ≠
      .letbox (.box [.base] (.var 0)) (.mvar 0 [.var 1]) := by decide''')
wr("Lang/Proofs/Contextual/Core.lean", co)
print("s10edit: ok")
