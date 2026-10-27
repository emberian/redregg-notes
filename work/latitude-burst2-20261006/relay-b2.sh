#!/usr/bin/env bash
# relay-b2.sh TIP : copy burst2-a's FROZEN warm base (gated tree at TIP) to burst2-b's /srv/warm-base, through
# this Mac (the boxes have no keys for each other). relay-base.sh with the burst2 ssh config: .lake/packages is
# not sent (the receiver hardlinks its own; same lake-manifest), src swapped in by rename, mk-lane --verify 0.
set -euo pipefail
T=$1; F=$HOME/.ssh/burst2-20261006.conf; SD=/srv/warm-base/src
ssh -F $F burst2-a "cd $SD && [ \$(git rev-parse HEAD) = $T ] && [ -z \"\$(git status --porcelain --untracked-files=no)\" ]"
ssh -F $F burst2-b "set -e; W=/srv/warm-base; old=\$(sed -n 's/^tip=//p' \$W/FROZEN); [ \"\$old\" != $T ]; git -C \$W/src fetch -q burst2-a:/srv/git/minidregg.git $T || git -C \$W/src fetch -q https://github.com/emberian/minidregg.git $T; git -C \$W/src diff --quiet \$old $T -- lake-manifest.json lean-toolchain || { echo manifest changed; exit 9; }; grep -q 'git remote remove base' \$W/mk-lane.sh || sed -i '/^git remote remove github/a git remote remove base 2>/dev/null || true' \$W/mk-lane.sh; rm -rf \$W/src.new; mkdir -p \$W/src.new/.lake; cp -al \$W/src/.lake/packages \$W/src.new/.lake/packages"
s=$(date +%s)
ssh -F $F burst2-a "tar -C $SD --exclude=./.lake/packages -cf - . | zstd -3 -T8 -q -c" | ssh -F $F burst2-b "zstd -d -q -c | tar -C /srv/warm-base/src.new -xf -"
echo "relay: $(( $(date +%s) - s ))s"
ssh -F $F burst2-b "set -e; source ~/.profile; W=/srv/warm-base; T=$T; old=\$(sed -n 's/^tip=//p' \$W/FROZEN); cd \$W/src.new; [ \$(git rev-parse HEAD) = \$T ]; [ -z \"\$(git status --porcelain --untracked-files=no)\" ]
echo \"advancing \$old -> \$T (copy from burst2-a) \$(date -Is)\" > \$W/NOT-READY.txt
mv \$W/src \$W/src.prev-\${old:0:8}; mv \$W/src.new \$W/src
printf 'tip=%s\nfrozen_at=%s\nbuilt_in=burst2-a:/srv/warm-base/src (gated tree; copied by relay through the Mac; .lake/packages hardlinked from prev)\nprev=%s (kept at %s)\nrule=read-only base; lanes come from /srv/warm-base/mk-lane.sh <lane>; never build in /srv/warm-base/src\n' \$T \"\$(date -Is)\" \$old \$W/src.prev-\${old:0:8} > \$W/FROZEN.new; mv -f \$W/FROZEN.new \$W/FROZEN; rm -f \$W/NOT-READY.txt
p=mk-verify-\${T:0:8}; timeout 550 \$W/mk-lane.sh --verify \$p 2>&1 | tail -1; rm -rf /srv/lanes/\$p; head -1 \$W/FROZEN"
