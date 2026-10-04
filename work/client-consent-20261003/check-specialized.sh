#!/usr/bin/env bash
set -euo pipefail
cd /home/hbox/workbox/codex-client-consent-20261003/src
export LEAN_PATH=/home/hbox/workbox/codex-client-consent-20261003/deps LEAN_NUM_THREADS=2
for package in /tank/dregg-build/claude-hostnext-r1/main-build/src/.lake/packages/*; do
 if [ -d "$package/.lake/build/lib/lean" ]; then LEAN_PATH="$LEAN_PATH:$package/.lake/build/lib/lean"; fi
done
export LEAN_PATH
for module in PayClaimQuote PayClaimStatus NativeHostPayClaims NativeSpecializedConsent; do
 /home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -o /home/hbox/workbox/codex-client-consent-20261003/olean/Kernel/$module.olean --c=/home/hbox/workbox/codex-client-consent-20261003/c/$module.c Kernel/$module.lean
 ln -sf /home/hbox/workbox/codex-client-consent-20261003/olean/Kernel/$module.olean /home/hbox/workbox/codex-client-consent-20261003/deps/Kernel/$module.olean
 echo SCOPED-PASS-$module
 done
