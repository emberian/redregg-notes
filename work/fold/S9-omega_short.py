# usage: omega_short.py FILE FUNC NARGS  -- append (Ω := []) after the NARGS-th explicit argument of each `FUNC ` call lacking Ω
import re,sys
f,fn,nargs=sys.argv[1],sys.argv[2],int(sys.argv[3])
s=open(f).read()
def skipws(i):
    while i<len(s) and s[i]==' ': i+=1
    return i
def arg_end(i):
    o={'(':')','[':']','⟨':'⟩','{':'}'}
    if s[i] in o:
        st=[o[s[i]]]; i+=1
        while st:
            c=s[i]
            if c in o: st.append(o[c])
            elif c==st[-1]: st.pop()
            i+=1
        return i
    j=i
    while j<len(s) and s[j] not in ' )\n],': j+=1
    return j
out=[];last=0;n=0
for m in re.finditer(r'(?<![\w.])'+re.escape(fn)+r' ',s):
    i=m.end()
    for k in range(nargs):
        i=skipws(i); i=arg_end(i)
    rest=s[i:i+12]
    if '(Ω' in s[m.start():i] or rest.lstrip().startswith('(Ω'): continue
    out.append(s[last:i]+' (Ω := [])'); last=i; n+=1
out.append(s[last:]); open(f,'w').write(''.join(out)); print(f,fn,n)
