#!/bin/bash
# plant-remote.sh NAME FILE MODS... (old/new text in plant-old.txt / plant-new.txt beside this script)
L=/tank/dregg-build/nanodregg/logs/promo
NAME=$1; FILE=$2; shift 2; MODS="$*"
cd /tank/dregg-build/nanodregg/wt/promo || exit 1
python3 - "$FILE" "$L/plant-old.txt" "$L/plant-new.txt" <<'PY' || exit 1
import sys
p,o,n=sys.argv[1:4]; s=open(p).read(); a=open(o).read(); b=open(n).read()
assert s.count(a)==1, ("count", s.count(a)); open(p,"w").write(s.replace(a,b)); print("PLANTED", p)
PY
export CARGO_TARGET_DIR=$PWD/target
SWARM_MEM_MAX=8G LEAN_NUM_THREADS=2 swarm-build lake build lang-journey > $L/plant-$NAME-build.log 2>&1
echo "journey build exit $?"
if [ -n "$MODS" ]; then
  SWARM_MEM_MAX=8G LEAN_NUM_THREADS=2 swarm-build lake build $MODS > $L/plant-$NAME-proofs.log 2>&1
  echo "proof modules ($MODS) build exit $?"
  grep -E 'error: Lang' $L/plant-$NAME-proofs.log | cut -c1-160 | head -8
fi
grep -E 'error: Lang|error: Ledger' $L/plant-$NAME-build.log | cut -c1-160 | head -8
if grep -q 'Built «lang-journey»' $L/plant-$NAME-build.log; then echo "journey exe REBUILT under the plant"; else echo "STALE: the journey exe was NOT rebuilt under the plant; its verdict below is unread"; fi
.lake/build/bin/lang-journey > $L/plant-$NAME-journey.txt 2>&1; echo "journey exit $?"
grep -E 'FAIL|lang-journey:' $L/plant-$NAME-journey.txt | cut -c1-230
echo "control greps (unbound|No such file|Traceback): $(grep -cE 'unbound|No such file|Traceback' $L/plant-$NAME-journey.txt)"
.lake/build/bin/lang-journey --contextual-checks > $L/plant-$NAME-cc.txt 2>&1; echo "cc exit $?"
grep -E 'FAIL|checks:' $L/plant-$NAME-cc.txt
