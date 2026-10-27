#!/usr/bin/env bash
set -uo pipefail
cd ~/nd-land/glm-b
echo "[p2] stopping old pipeline pid $(cat pipeline.pid)"
kill "$(cat pipeline.pid)" 2>/dev/null; sleep 1
export PATH=$HOME/.elan/bin:$PATH
LEANY() { ionice -c3 nice -n 15 lake env lean names-eval.lean 2>&1 | tail -8; }
echo "[p2] eval BEFORE (bare, idle):"
LEANY
echo "[p2] rename:"
./rename-verdicts.sh > rename.log 2>&1 || { echo "[p2] RENAME FAILED:"; tail -25 rename.log; exit 1; }
tail -8 rename.log
echo "[p2] insert theorem:"
awk 'ins!=1 && /^  \| rejected r => cases r <;> rfl$/ {print; while ((getline l < "insert-theorem.txt") > 0) print l; close("insert-theorem.txt"); ins=1; next} {print}' Kernel/Proofs/Refusals.lean > Kernel/Proofs/Refusals.lean.new && mv Kernel/Proofs/Refusals.lean.new Kernel/Proofs/Refusals.lean
grep -c "Verdict.name_injective" Kernel/Proofs/Refusals.lean
echo "[p2] build after (queued via nd-build):"
scripts/nd-build lake build Kernel.Receive.Submit Kernel.Proofs.Refusals > build-after.log 2>&1
echo "build exit: $?"
tail -4 build-after.log
echo "[p2] eval AFTER (bare, idle):"
LEANY
echo "[p2] ALL DONE"
