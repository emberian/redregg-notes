import re,difflib
HYG=re.compile(r"[^\s():\[\]{}]*\._@\.[^\s():\[\]{}]*?\._hyg\.[0-9]+")
def load(p):
    d={}
    for l in open(p,encoding="utf-8"):
        f=l.rstrip("\n").split("\t"); d[f[0]]=f
    return d
b=load("S9-before.tsv"); a=load("S9-after.tsv")
names=[l.split()[1] for l in open("S9-diff.txt") if l.strip().startswith("TYPE ")]
gen=re.compile(r"\.(_|match_|eq_|proof_|inj|injEq|sizeOf_spec|ctorIdx|noConfusion|casesOn|rec|below|brecOn|binductionOn|recOn|induct|fun_cases|eq_def|_unfold|_sunfold)")
def toks(s): return re.findall(r"\w+|[^\s\w]",HYG.sub("_hyg_",s))
for n in names:
    if gen.search(n) or a[n][2]!="theorem": continue
    tb,ta=toks(b[n][3]),toks(a[n][3])
    sm=difflib.SequenceMatcher(None,tb,ta,autojunk=False)
    ch=[(" ".join(tb[i1:i2])," ".join(ta[j1:j2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!="equal"]
    arrows=(tb.count("→")+tb.count("∀"), ta.count("→")+ta.count("∀"))
    print(n.split(".")[-1], "arrows/foralls", arrows, "|", "; ".join(f"[{x}]->[{y}]" for x,y in ch))
