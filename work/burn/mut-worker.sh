#!/usr/bin/env bash
# mut-worker.sh LANE SHARD.jsonl OUTDIR   -- run each mutant in LANE (a mk-lane lane), phase 1 + downstream.
# Writes OUTDIR/<id>.json  {id,verdict,module_rc,broken,down_rc,down_broken,secs}
export PATH=/srv/pipeline/scripts:$PATH
[ -f /srv/pipeline/box.env ] && . /srv/pipeline/box.env
export PIPELINE_LAKE_CACHE=/srv/lanes/mut-cache LAKE_CACHE_DIR=/srv/lanes/mut-cache LAKE_ARTIFACT_CACHE=true
lane=$1; shard=$2; out=$3
src=/srv/lanes/$lane/src; mkdir -p "$out" /srv/lanes/$lane/logs
cd "$src" || exit 1
while IFS= read -r row; do
  id=$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["id"])' "$row")
  [ -f "$out/$id.json" ] && continue
  f=$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["file"])' "$row")
  mod=$(echo "${f%.lean}" | tr / .)
  git checkout -q -- "$f"
  python3 - "$row" <<'P' || { echo "apply failed $id" >&2; continue; }
import json,sys
m=json.loads(sys.argv[1]); L=open(m['file'],encoding='utf-8').read().split('\n')
assert L[m['line']-1]==m['old'], 'old mismatch'
L[m['line']-1]=m['new']; open(m['file'],'w',encoding='utf-8').write('\n'.join(L))
P
  t0=$(date +%s); log=/srv/lanes/$lane/logs/$id
  slot.sh swarm-build lake build "$mod" >"$log.mod.log" 2>&1; mrc=$?
  down=-; drc=-
  if [ $mrc -eq 0 ]; then
    slot.sh swarm-build lake build Minidregg +Host.Main:leanArts ObjectiveProofs >"$log.down.log" 2>&1; drc=$?
  fi
  python3 - "$row" "$mrc" "$drc" "$log" "$(( $(date +%s)-t0 ))" "$out/$id.json" <<'P'
import json,sys,re
m=json.loads(sys.argv[1]); mrc,drc,log,secs,outp=sys.argv[2:7]
def errs(p):
    try: t=open(p,errors='replace').read()
    except: return []
    return [l for l in t.split('\n') if l.startswith('error:')]
me=errs(log+'.mod.log'); de=errs(log+'.down.log') if drc!='-' else []
at=f"{m['file']}:{m['line']}:"
def cls(e): return 'ATSITE' if at in e else 'ELSEWHERE'
if mrc!='0':
    if me and all(cls(e)=='ATSITE' and 'axioms' not in e for e in me): v='INVALID'
    else: v='BUILD-RED'
elif drc!='0': v='DOWNSTREAM-RED'
else: v='BUILD-GREEN'
broken=sorted(set(re.sub(r'^error: [^ ]+ ','',e)[:160] for e in me if 'axioms' in e or cls(e)=='ELSEWHERE'))
open(outp,'w').write(json.dumps(dict(id=m['id'],file=m['file'],line=m['line'],kind=m['kind'],old=m['old'].strip(),new=m['new'].strip(),verdict=v,module_rc=mrc,down_rc=drc,errors=[e[:240] for e in me[:12]],down_errors=[e[:240] for e in de[:12]],secs=int(secs)),ensure_ascii=False))
P
  git checkout -q -- "$f"
done < "$shard"
echo "WORKER $lane DONE" > /srv/lanes/$lane/STATUS.txt
