#!/opt/homebrew/bin/bash
# emits one line per worker exit and per new READY/ASK/DONE/RED/VERDICT/landed report line
cd /Users/ember/dev/redregg/work/codex || exit 1
declare -A seen alive
for d in */; do n=${d%/}; [ -f "$n/run.pid" ] && ps -p "$(cat "$n/run.pid")" >/dev/null 2>&1 && alive[$n]=1; done
for r in *.report.md; do seen[$r]=$(wc -l < "$r"); done
while true; do
  for n in "${!alive[@]}"; do
    ps -p "$(cat "$n/run.pid" 2>/dev/null)" >/dev/null 2>&1 || { echo "EXITED $n"; unset "alive[$n]"; }
  done
  for d in */; do n=${d%/}; [ -z "${alive[$n]:-}" ] && [ -f "$n/run.pid" ] && ps -p "$(cat "$n/run.pid")" >/dev/null 2>&1 && alive[$n]=1; done
  for r in *.report.md; do
    c=$(wc -l < "$r"); p=${seen[$r]:-0}
    if [ "$c" -gt "$p" ]; then tail -n +"$((p+1))" "$r" | grep -E "READY|ASK|DONE|RED|LAND|landed|VERDICT" | cut -c1-220 | sed "s/^/${r%.report.md}: /"; seen[$r]=$c; fi
  done
  sleep 20
done
