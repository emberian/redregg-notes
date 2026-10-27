#!/bin/bash
# plant5.sh NAME PYEDIT — on hbox wt/promo: apply a python edit to Lang/LiveHoles.lean, build teeth + journey,
# elaborate the scratch C5 theorems, run the journey, restore and rebuild.
set -u
N=$1; ED=$2
W=/tank/dregg-build/nanodregg/wt/promo; L=/tank/dregg-build/nanodregg/logs/promo/c5plants; mkdir -p $L
cd $W && export CARGO_TARGET_DIR=$W/target
python3 $ED Lang/LiveHoles.lean || { echo EDIT-FAILED; exit 1; }
git diff --stat
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build lang-journey > $L/$N-exe.log 2>&1; echo "exe build exit $?"; grep -c 'lang-journey' $L/$N-exe.log
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build Lang.Proofs.LiveJourney > $L/$N-teeth.log 2>&1; echo "teeth build exit $?"; grep -E 'error' $L/$N-teeth.log | head -5
LEAN_NUM_THREADS=2 lake env lean /tank/dregg-build/nanodregg/logs/promo/c2/T2.lean > $L/$N-thm.log 2>&1; echo "C5 theorems exit $?"; grep -E 'error' $L/$N-thm.log | head -5
LEAN_NUM_THREADS=2 lake env lean /tank/dregg-build/nanodregg/logs/promo/c2/Witness.lean > $L/$N-witness.log 2>&1; echo witness:; cat $L/$N-witness.log | head -4
timeout 600 .lake/build/bin/lang-journey > $L/$N-journey.txt 2>&1; echo "journey exit $?"; tail -1 $L/$N-journey.txt; grep -E '^(FAIL|fail|not ok|RED)' $L/$N-journey.txt | head -5
git checkout -q HEAD -- Lang/LiveHoles.lean
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build lang-journey Lang.Proofs.LiveJourney > $L/$N-restore.log 2>&1; echo "restore exit $?"; git status --short
