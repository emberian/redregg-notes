#!/usr/bin/env bash
set -euo pipefail
export PATH=/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin:$PATH
python3 /home/hbox/workbox/codex-client-consent-20261003/link-fixture.py
