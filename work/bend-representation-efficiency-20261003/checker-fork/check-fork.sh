#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/src
export LEAN_NUM_THREADS=2
/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -j2 Theory/BendTTSource.lean -o /tank/dregg-build/codex-bend-efficiency-20261003/checker-fork/olean/Theory/BendTTSource.olean
printf 'BEND CHECKER EMPTY ENV FORK PASS\n'
