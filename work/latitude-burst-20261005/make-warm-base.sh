#!/usr/bin/env bash
# On burst-gate, as ember: freeze a copy of the cold-built /srv/mini as /srv/warm-base/src.
set -euo pipefail
W=/srv/warm-base
R=$(readlink -f /srv/mini-logs/cold-build-latest.result)
grep -q '^build_rc=0 ' "$R" || { echo "cold build not green: $R"; exit 1; }
TIP=$(sed -n 's/^tip=//p' "$R")
[ "$(git -C /srv/mini rev-parse HEAD)" = "$TIP" ] || { echo "/srv/mini moved off $TIP"; exit 1; }
[ ! -e "$W/src" ] || { echo "$W/src exists"; exit 1; }
mkdir -p "$W/logs"
echo "base being built $(date -Is)" > "$W/NOT-READY.txt"
rsync -aH /srv/mini/ "$W/src/"
cp -p "$(readlink -f /srv/mini-logs/cold-build-latest.log)" "$W/logs/green.log"
cp -p "$R" "$W/logs/green.result"
for p in "$W"/src/.lake/packages/*/; do git -C "$p" config core.trustctime false; done
git -C "$W/src" config core.trustctime false
[ -z "$(git -C "$W/src" status --porcelain --untracked-files=no)" ] || { echo "base tracked tree dirty"; exit 1; }
install -m 755 /srv/mini-logs/mk-lane.sh "$W/mk-lane.sh"
cat > "$W/FROZEN" <<F
tip=$TIP
frozen_at=$(date -Is)
built_on=$(hostname):/srv/mini
$(grep -E '^(build_wall|build_rc)' "$R" | tr ' ' '\n' | grep -E '^build_(wall|rc)=')
rule=read-only base; lanes come from $W/mk-lane.sh <lane>; never build in $W/src
F
rm -f "$W/NOT-READY.txt"
echo "warm base frozen at $TIP"; du -sh "$W/src" "$W/src/.lake"
