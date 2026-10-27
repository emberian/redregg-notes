#!/bin/bash
# collects out/*.json (phase1) and jout/*.json (phase2) from both boxes -> RESULTS.tsv, SURVIVORS.md in $1
D=${1:-/Users/ember/dev/redregg/work/burn}; mkdir -p $D/raw
for h in a b; do ssh -F $HOME/.ssh/burst2-20261006.conf burst2-$h 'cd /srv/lanes/mut-sweep; for d in out jout; do [ -d $d ] && for f in $d/*.json; do [ -f "$f" ] && { echo "$d"; cat "$f"; echo; }; done; done' > $D/raw/$h.txt 2>/dev/null; done
python3 - "$D" <<'P'
import sys,json,glob
from collections import defaultdict,Counter
D=sys.argv[1]; p1={}; p2={}
for h in 'ab':
    cur=None
    for l in open(f'{D}/raw/{h}.txt',errors='replace'):
        l=l.strip()
        if l in('out','jout'): cur=l; continue
        if not l: continue
        try: j=json.loads(l)
        except: continue
        (p1 if cur=='out' else p2)[j['id']]=j
rows=[]; surv=[]
for i,m in sorted(p1.items()):
    jv=''; red=''
    if m['verdict']=='BUILD-GREEN':
        j=p2.get(i)
        if j: jv=j['verdict']; red=','.join(j['red_rows'])
        else: jv='PENDING'
    broken=';'.join(sorted(set(e.split(' depends on')[0].split(': ',1)[-1].split(' ')[-1] if 'axioms' in e else e[:80] for e in m['errors'][:6])))
    if m['verdict']=='DOWNSTREAM-RED': broken='DOWNSTREAM: '+';'.join(e[:90] for e in m['down_errors'][:3])
    rows.append((i,f"{m['file']}:{m['line']}",m['kind'],m['verdict'],broken,(jv+(' red='+red if red else '')).strip()))
    if m['verdict']=='BUILD-GREEN' and jv in('JOURNEY-GREEN','PENDING','HOST-BUILD-FAIL'): surv.append((m,jv))
open(f'{D}/RESULTS.tsv','w').write('mutant\tfile:line\tkind\tbuild_verdict\tbroken_theorems_or_errors\tjourney_verdict\n'+'\n'.join('\t'.join(r) for r in rows)+'\n')
c=Counter(r[3] for r in rows); cj=Counter(r[5].split(' ')[0] for r in rows if r[5])
out=[f'# Mutation survivors (Mini cfdaf64d)\n\nmutants run: {len(rows)}  build verdicts: {dict(c)}  journey verdicts (of BUILD-GREEN): {dict(cj)}\n\nA survivor changed NO verdict: lake build of the module, the umbrella + ObjectiveProofs, and (JOURNEY-GREEN) the journey rows that exercise the file all stayed green. PENDING = journeys not yet run.\n']
byf=defaultdict(list)
for m,jv in surv: byf[m['file']].append((m,jv))
for f,L in sorted(byf.items()):
    out.append(f'\n## {f}  ({len(L)})\n')
    for m,jv in sorted(L,key=lambda x:x[0]['line']):
        out.append(f"### {m['id']}  line {m['line']}  {m['kind']}  [{jv}]\n```lean\n- {m['old']}\n+ {m['new']}\n```\n")
open(f'{D}/SURVIVORS.md','w').write('\n'.join(out))
print(len(rows),dict(c),dict(cj))
P
