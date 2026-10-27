#!/usr/bin/env bash
set -uo pipefail
cd ~/nd-land/glm-b
echo "[pipeline] waiting for pristine build pid $(cat build-submit.pid)"
while kill -0 "$(cat build-submit.pid)" 2>/dev/null; do sleep 15; done
echo "[pipeline] pristine build tail:"; tail -3 build-submit.log
echo "[pipeline] eval BEFORE:"
scripts/nd-build lake env lean names-eval.lean 2>&1 | tail -8
echo "[pipeline] rename:"
./rename-verdicts.sh > rename.log 2>&1 || { echo "[pipeline] RENAME FAILED:"; tail -25 rename.log; exit 1; }
tail -8 rename.log
echo "[pipeline] insert theorem:"
awk 'ins!=1 && /^  \| rejected r => cases r <;> rfl$/ {print; while ((getline l < "insert-theorem.txt") > 0) print l; close("insert-theorem.txt"); ins=1; next} {print}' Kernel/Proofs/Refusals.lean > Kernel/Proofs/Refusals.lean.new && mv Kernel/Proofs/Refusals.lean.new Kernel/Proofs/Refusals.lean
grep -c "Verdict.name_injective" Kernel/Proofs/Refusals.lean
echo "[pipeline] build after:"
scripts/nd-build lake build Kernel.Receive.Submit Kernel.Proofs.Refusals > build-after.log 2>&1
echo "build exit: $?"; tail -4 build-after.log
echo "[pipeline] eval AFTER:"
scripts/nd-build lake env lean names-eval.lean 2>&1 | tail -6
echo "[pipeline] ALL DONE"
