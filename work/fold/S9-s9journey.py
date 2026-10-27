import re
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)
def sub1(s, a, b, p):
    assert s.count(a) == 1, (p, a[:80], s.count(a)); return s.replace(a, b)
# HoleRefusal gets DecidableEq (CheckError, TypeErr, ExpansionBound have it)
p = "Lang/LiveHoles.lean"; s = rd(p)
s = sub1(s, "  | instanceType (e : TypeErr)\n", "  | instanceType (e : TypeErr)\n  deriving DecidableEq\n", p)
wr(p, s)
p = "Lang/Journey/ContextualChecks.lean"; s = rd(p)
s = sub1(s, "def named {α : Type} (r : Except String α) (why : String) : Bool :=\n  match r with | .error e => e == why | .ok _ => false\n",
 "def named {α : Type} (r : Except String α) (why : String) : Bool :=\n  match r with | .error e => e == why | .ok _ => false\n\n/-- The refusal is exactly this constructor (LANG-74.9: preparation refusals are values, not strings). -/\ndef refusedAs {ε α : Type} [DecidableEq ε] (r : Except ε α) (why : ε) : Bool :=\n  match r with | .error e => decide (e = why) | .ok _ => false\n", p)
s = sub1(s, '(fun _ _ => .error "must-not-prepare-closed")', "(fun _ _ => .error .provenance) -- never called: a closed package does not prepare", p)
pairs = [('"holeType 0")', ".type 0)"), ('"holeContext 0")', ".context 0)"), ('\n      "holeCandidates 0")', "\n      .candidates 0)"),
 ('"holeGuardType 0")', ".guardType 0)"), ('\n      "holeCandidateType 0 0"),\n    ("candidate-context-scope"', '\n      (.candidateType 0 0)),\n    ("candidate-context-scope"'),
 ('\n      "holeCandidateType 0 0"),\n    ("signature-bound"', '\n      (.candidateType 0 0)),\n    ("signature-bound"'),
 ('"holeSignatureBound")', ".signatureBound)"), ('"holeDuplicate")', ".duplicate)"),
 ('"holeSelectionType 0")', "(.selectionType 0))"), ('"holeSelectionIndex 0")', "(.selectionIndex 0))"),
 ('\n      "holeDerivationMoved 0")', "\n      (.derivationMoved 0))"), ('"holeGuardFault 0")', "(.guardFault 0))"),
 ('"holeWorkBound")', ".work)"), ('"holeSizeBound")', ".size)")]
for a, b in pairs: s = sub1(s, a, b, p)
s = s.replace(".type 0)", "(.type 0))").replace(".context 0)", "(.context 0))").replace(".candidates 0)", "(.candidates 0))").replace(".guardType 0)", "(.guardType 0))")
# the rows that compared HoleRefusal strings now use refusedAs; print rows keep `named`
for lab in ["signature-context-type", "signature-hypothesis-length", "signature-candidate-bound", "signature-guard-type",
            "candidate-result-type", "candidate-context-scope", "signature-bound", "signature-name-unique",
            "selection-data-type", "selection-code-index", "selection-support-version", "guard-budget",
            "expansion-work-bound", "expansion-size-bound"]:
    s = sub1(s, f'("{lab}", named ', f'("{lab}", refusedAs ', p)
s = s.replace('      | .error why => why.startsWith "holeBodyType" | _ => false),', "      | .error (.bodyType _) => true | _ => false),")
wr(p, s)
p = "Lang/Journey/Contextual.lean"; s = rd(p)
s = sub1(s, '| .error why => why == "holeCandidateType 0 0" | .ok () => false', "| .error why => decide (why = .candidateType 0 0) | .ok () => false", p)
wr(p, s)
print("ok")
