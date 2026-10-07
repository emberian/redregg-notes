#!/usr/bin/env bash
# burst gate: Mathlib cache + ONE cold umbrella build at GitHub main's tip. Run as ember.
set -uo pipefail
source ~/.profile
cd /srv/mini
git fetch -q origin && git checkout -q main && git merge -q --ff-only origin/main || { echo "git sync failed"; exit 1; }
if [ -n "${PIN_TIP:-}" ]; then git checkout -q -B main "$PIN_TIP" || { echo "pin failed"; exit 1; }; fi
TIP=$(git rev-parse HEAD)
TS=$(date -u +%Y%m%dT%H%M%SZ)
R=/srv/mini-logs/cold-build-$TS.result
echo "tip=$TIP" > "$R"
echo "cache_start=$(date -Is)" >> "$R"
s0=$(date +%s)
lake exe cache get > /srv/mini-logs/cache-get-$TS.log 2>&1; echo "cache_rc=$? cache_wall=$(( $(date +%s)-s0 ))s" >> "$R"
echo "build_start=$(date -Is)" >> "$R"
s1=$(date +%s)
SWARM_MEM_MAX=${COLD_MEM:-64G} swarm-build lake build Minidregg +Host.Main:leanArts ObjectiveProofs > /srv/mini-logs/cold-build-$TS.log 2>&1
rc=$?
echo "build_rc=$rc build_wall=$(( $(date +%s)-s1 ))s build_end=$(date -Is)" >> "$R"
echo "built_lines=$(grep -c '\] Built ' /srv/mini-logs/cold-build-$TS.log)" >> "$R"
ln -sfn "cold-build-$TS.log" /srv/mini-logs/cold-build-latest.log
ln -sfn "cold-build-$TS.result" /srv/mini-logs/cold-build-latest.result
