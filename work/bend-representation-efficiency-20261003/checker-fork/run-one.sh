#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/src
export LEAN_PATH=/tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/olean
export LEAN_NUM_THREADS=2
set +e
timeout 60 /home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -j2 --run CheckOne.lean DrEXSettlementPlanDemonstration.bendtt
lane_exit=$?
set -e
printf 'BEND FORK DEF262 VERDICT EXIT %s\n' "$lane_exit"
exit "$lane_exit"
