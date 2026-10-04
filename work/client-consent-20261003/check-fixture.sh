#!/usr/bin/env bash
set -euo pipefail
cd /home/hbox/workbox/codex-client-consent-20261003/src
export LEAN_PATH=/home/hbox/workbox/codex-client-consent-20261003/deps LEAN_NUM_THREADS=2
for package in /tank/dregg-build/claude-hostnext-r1/main-build/src/.lake/packages/*; do
 if [ -d "$package/.lake/build/lib/lean" ]; then LEAN_PATH="$LEAN_PATH:$package/.lake/build/lib/lean"; fi
done
export LEAN_PATH
/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -o /home/hbox/workbox/codex-client-consent-20261003/olean/Host/SpecializedFixture.olean --c=/home/hbox/workbox/codex-client-consent-20261003/c/SpecializedFixture.c Host/SpecializedFixture.lean
echo SCOPED-PASS-SpecializedFixture
