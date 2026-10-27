#!/bin/bash
# plant6.sh NAME PYEDIT — C5 plants on the landed shape (hbox wt/promo): edit Lang/LiveHoles.lean; relink the journey;
# elaborate the five teeth from a copy of Lang/Proofs/LiveJourney.lean that does not import the C5 module; build
# Lang.Proofs.LiveHoles (the C5 theorems, by name); witnesses; journey; restore + rebuild.
set -u
N=$1; ED=$2
W=/tank/dregg-build/nanodregg/wt/promo; L=/tank/dregg-build/nanodregg/logs/promo/c5plants2; C=/tank/dregg-build/nanodregg/logs/promo/c2; mkdir -p $L
cd $W && export CARGO_TARGET_DIR=$W/target
python3 $ED Lang/LiveHoles.lean || { echo EDIT-FAILED; exit 1; }
git diff --stat -- Lang/LiveHoles.lean
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build lang-journey Lang.Proofs.Check Lang.Proofs.BigStep Lang.Journey.ContextualCycle > $L/$N-exe.log 2>&1; echo "exe build exit $? relinked: $(grep -c 'lang-journey' $L/$N-exe.log)"
sed 's/^import Lang.Proofs.LiveHoles$/import Lang.Proofs.Check/' Lang/Proofs/LiveJourney.lean > $L/$N-Teeth.lean
LEAN_NUM_THREADS=2 lake env lean $L/$N-Teeth.lean > $L/$N-teeth.log 2>&1; echo "teeth exit $?"; grep -E 'error' $L/$N-teeth.log | head -5
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build Lang.Proofs.LiveHoles > $L/$N-thm.log 2>&1; echo "C5 module exit $?"; grep -E 'error' $L/$N-thm.log | head -6
LEAN_NUM_THREADS=2 lake env lean $C/Witness.lean > $L/$N-witness.log 2>&1; echo witness:; head -4 $L/$N-witness.log
timeout 600 .lake/build/bin/lang-journey > $L/$N-journey.txt 2>&1; echo "journey exit $?"; tail -1 $L/$N-journey.txt
git checkout -q HEAD -- Lang/LiveHoles.lean 2>/dev/null; cp /tank/dregg-build/nanodregg/logs/promo/c5-cand-LiveHoles.lean Lang/LiveHoles.lean
SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build lang-journey Lang.Proofs.LiveJourney > $L/$N-restore.log 2>&1; echo "restore exit $?"; git status --short
