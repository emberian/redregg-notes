#!/usr/bin/env bash
# mut-journey.sh LANE SURVIVORS.jsonl OUTDIR -- phase 2: for each BUILD-GREEN mutant, build the mutated Lean host
# in the lane, swap it into a copy-by-symlink of the baseline artifact set, run the journey rows that exercise the file.
export PATH=/srv/pipeline/scripts:$PATH
[ -f /srv/pipeline/box.env ] && . /srv/pipeline/box.env
export PIPELINE_LAKE_CACHE=/srv/lanes/mut-cache LAKE_CACHE_DIR=/srv/lanes/mut-cache LAKE_ARTIFACT_CACHE=true
lane=$1; list=$2; out=$3
src=/srv/lanes/$lane/src; mkdir -p "$out" /srv/lanes/$lane/logs
BASE=/srv/artifacts/cfdaf64df8f869f5e45c86a85055457345fc5ae1
cd "$src" || exit 1
rowsfor() {
  case "$1" in
    ObjectiveCall|ObjectiveCallReference) echo "call objective";;
    ObjectiveSend|Inbox|AnswerSlot) echo "send call objective";;
    ObjectiveDomain|ObjectiveDomainInvariant) echo "domain objective";;
    ObjectiveActivityUpgrade) echo "upgrade activity objective";;
    ObjectiveActivity|ObjectiveActivityReceiver|ObjectiveActivityWire|ObjectiveActivityGate|ObjectiveActivityGateRoute|ObjectiveActivityCell) echo "objective activity objectrecord bounty seats journey";;
    SeatStore) echo "seats bounty rooms journey";;
    ReceivingLaw|ReceivingLawFixture) echo "activity rooms objective journey";;
    *) echo "journey objective rooms";;
  esac
}
while IFS= read -r row; do
  id=$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["id"])' "$row")
  [ -f "$out/$id.json" ] && continue
  mkdir "$out/.claim-$id" 2>/dev/null || continue
  f=$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["file"])' "$row")
  base=$(basename "${f%.lean}")
  git checkout -q -- "$f"
  python3 - "$row" <<'P' || continue
import json,sys
m=json.loads(sys.argv[1]); L=open(m['file'],encoding='utf-8').read().split('\n')
assert L[m['line']-1]==m['old']
L[m['line']-1]=m['new']; open(m['file'],'w',encoding='utf-8').write('\n'.join(L))
P
  lg=/srv/lanes/$lane/logs/$id
  lake-slot minidregg-host >"$lg.host.log" 2>&1; hrc=$?
  res="{}"; : > "$lg.rows.tsv"
  if [ $hrc -eq 0 ] && [ -x .lake/build/bin/minidregg-host ]; then
    SET=/srv/lanes/$lane/set; rm -rf "$SET"; mkdir -p "$SET/bin"
    for e in "$BASE"/*; do [ "$(basename "$e")" = bin ] || ln -s "$e" "$SET/$(basename "$e")"; done
    for e in "$BASE"/bin/*; do ln -s "$e" "$SET/bin/$(basename "$e")"; done
    rm "$SET/bin/minidregg-host"; cp .lake/build/bin/minidregg-host "$SET/bin/minidregg-host"
    for r in $(rowsfor "$base"); do
      O=/srv/lanes/$lane/rowout/$id/$r; mkdir -p "$O"; R=$(mktemp -d /tmp/mj.XXXXXX)
      ( SRC=$src SET=$SET BIN=$SET/bin MANIFEST=$SET/manifest.json RUN=$R OUT=$O LEANENV=1
        export SRC SET BIN MANIFEST RUN OUT LEANENV
        cd "$R" && timeout 1500 bash -c ". '$src/scripts/pipeline/journey-rows'; row_$r" ) >"$O/row.out" 2>"$O/row.err"
      rc=$?; rm -rf "$R"
      printf '%s\t%s\t%s\n' "$r" "$rc" "$(tail -1 "$O/row.err" | tr '\t' ' ' | cut -c1-200)" >> "$lg.rows.tsv"
    done
  fi
  python3 - "$row" "$hrc" "$lg.rows.tsv" "$out/$id.json" <<'P'
import json,sys
m=json.loads(sys.argv[1]); hrc=sys.argv[2]
rows=[l.rstrip('\n').split('\t') for l in open(sys.argv[3]) if l.strip()]
red=[r[0] for r in rows if r[1] not in ('0','99','98')]
v='HOST-BUILD-FAIL' if hrc!='0' else ('JOURNEY-RED' if red else 'JOURNEY-GREEN')
json.dump(dict(id=m['id'],host_rc=hrc,verdict=v,red_rows=red,rows=rows),open(sys.argv[4],'w'))
P
  git checkout -q -- "$f"
done < "$list"
echo "JW $lane DONE" > /srv/lanes/$lane/STATUS.txt
