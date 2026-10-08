#!/usr/bin/env bash
# Run ON burst3-a. Updates ~/cxo/codex to the npm linux-x64 (musl) package. Run with the hub STOPPED and no worker live:
#   ~/cxo/cxo hub stop && bash cxo-update-codex.sh [VERSION] && ~/cxo/cxo hub start
set -euo pipefail
V=${1:-0.161.0}
pidf=${CXO_HOME:-$HOME/.cxo}/hub.pid
if [ -f "$pidf" ] && kill -0 "$(cat "$pidf")" 2>/dev/null; then echo "REFUSED: hub is running (pid $(cat "$pidf")); cxo hub stop first" >&2; exit 1; fi
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
curl -fsSL "https://registry.npmjs.org/@openai/codex/-/codex-$V-linux-x64.tgz" -o "$t/c.tgz"
tar xzf "$t/c.tgz" -C "$t"
n=$t/package/vendor/x86_64-unknown-linux-musl
"$n/bin/codex" --version | grep -q "$V" || { echo "version mismatch: $("$n/bin/codex" --version)" >&2; exit 1; }
rm -rf ~/cxo/codex.old; mv ~/cxo/codex ~/cxo/codex.old; cp -r "$n" ~/cxo/codex
~/cxo/codex/bin/codex --version
echo "updated; previous kept at ~/cxo/codex.old"
