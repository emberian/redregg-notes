#!/usr/bin/env bash
set -euo pipefail
cd /home/hbox/workbox/codex-client-consent-20261003/src
export LEAN_PATH=/home/hbox/workbox/codex-client-consent-20261003/olean:/home/hbox/workbox/codex-root-consent-20261003/olean:/home/hbox/workbox/codex-agreement-20261003/reader-pass-r2/reader-olean
for package in /tank/dregg-build/claude-hostnext-r1/main-build/src/.lake/packages/*; do
 if [ -d "$package/.lake/build/lib/lean" ]; then LEAN_PATH="$LEAN_PATH:$package/.lake/build/lib/lean"; fi
done
export LEAN_PATH LEAN_NUM_THREADS=2
/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean -o /home/hbox/workbox/codex-client-consent-20261003/olean/Host/ClientConsentSession.olean --c=/home/hbox/workbox/codex-client-consent-20261003/c/ClientConsentSession.c Host/ClientConsentSession.lean
echo SCOPED-PASS-native-client-consent-session
