#!/bin/bash
# blocks until RULINGS.tsv gains a row or the report gains a ROOT line; prints them
W=/Users/ember/dev/redregg/work
r0=$(wc -l < $W/RULINGS.tsv); c0=$(grep -c '^ROOT' $W/codex/CX-PROMO.report.md)
for i in $(seq 1 ${1:-55}); do
  r=$(wc -l < $W/RULINGS.tsv); c=$(grep -c '^ROOT' $W/codex/CX-PROMO.report.md)
  if [ $r -ne $r0 ] || [ $c -ne $c0 ]; then tail -n $((r-r0)) $W/RULINGS.tsv; grep '^ROOT' $W/codex/CX-PROMO.report.md | tail -n $((c-c0)); exit 0; fi
  sleep 10
done
echo NOTHING-YET
