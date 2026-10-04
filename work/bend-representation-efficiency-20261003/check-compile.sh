#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-bend-efficiency-20261003/src
lane_root=/tank/dregg-build/codex-bend-efficiency-20261003
lane_common=/home/hbox/workbox/codex-unified-integration-20261003/src
lane_lean=/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean
export LEAN_PATH="$lane_root/olean"
for lane_package in "$lane_common"/.lake/packages/*; do
 export LEAN_PATH="$LEAN_PATH:$lane_package/.lake/build/lib/lean"
done
export LEAN_NUM_THREADS=2
"$lane_lean" -j2 Compiler/BendClosureCompileIndexed.lean -o "$lane_root/olean/Compiler/BendClosureCompileIndexed.olean"
printf 'BEND INDEXED CODE MODULE PASS\n'
"$lane_lean" -j2 --run tests/BendClosureCompileIndexedBenchmark.lean  /home/hbox/workbox/codex-objective-linker-20261003/publication/complete.bendtt  /home/hbox/workbox/codex-objective-linker-20261003/publication/alternate.bendtt  /home/hbox/workbox/codex-bend-logic-20261003/BoolChooseSource.bendtt
printf 'BEND INDEXED CODE CHECK PASS\n'
