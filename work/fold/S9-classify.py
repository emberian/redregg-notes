import sys,re
rows={}
for l in open("S9-after.tsv",encoding="utf-8"):
    f=l.rstrip("\n").split("\t"); rows[f[0]]=f
names=[l.split()[1] for l in open("S9-diff.txt") if l.strip().startswith("TYPE ")]
gen=re.compile(r"\.(_|match_|eq_|proof_|inj|injEq|sizeOf_spec|ctorIdx|noConfusion|casesOn|rec|below|brecOn|binductionOn|recOn|induct|fun_cases|eq_def|_unfold|_sunfold)")
user=[];g=[]
for n in names:
    k=rows[n][2] if n in rows else "?"
    (g if gen.search(n) else user).append((k,n,rows[n][1] if n in rows else "?"))
from collections import Counter
print("user",len(user),Counter(k for k,_,_ in user)); print("generated",len(g),Counter(k for k,_,_ in g))
for k,n,m in sorted(user,key=lambda x:(x[0],x[2],x[1])): print("U",k,m,n)
