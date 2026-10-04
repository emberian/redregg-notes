#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/src
export LEAN_NUM_THREADS=2
for lane_artifacts in /tank/dregg-build/codex-private-lifecycle-20261003/olean /tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/olean; do
 export LEAN_PATH="$lane_artifacts"
 printf 'ACTUAL ENV SUB PROBE %s\n' "$lane_artifacts"
 /home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -j2 --run EmptyEnvProbe.lean
done
printf 'BEND ENV SUB ACTUAL RUN PROBE PASS\n'
