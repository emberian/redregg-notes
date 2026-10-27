#!/usr/bin/env bash
# mirror-github.sh : mirror the shared remote's main/next/green (authoritative, burst2-a) to GitHub,
# from this Mac (the boxes have no GitHub credentials). Backs off on failure 2 min, doubling, cap 15 min.
# Exits when GitHub equals the shared remote. Keeps the full stderr of the last failed push in
# $LOG for the ROOT. Run again after every publish.
set -u
F=$HOME/.ssh/burst2-20261006.conf; R=$HOME/dev/minidregg; GH=https://github.com/emberian/minidregg.git
LOG=${LOG:-/Users/ember/dev/redregg/work/logs/mirror-github-last-failure.txt}
mkdir -p "$(dirname "$LOG")"
delay=120; first_fail=""
while :; do
  GIT_SSH_COMMAND="ssh -F $F" git -C "$R" fetch -q burst2-a:/srv/git/minidregg.git \
    +refs/heads/main:refs/remotes/shared/main +refs/heads/next:refs/remotes/shared/next +refs/tags/green:refs/remotes/shared/green || { sleep 60; continue; }
  want=(); for r in main next green; do
    s=$(git -C "$R" rev-parse refs/remotes/shared/$r)
    [ $r = green ] && dst=refs/tags/green || dst=refs/heads/$r
    g=$(git ls-remote "$GH" "$dst" | cut -f1)
    [ "$s" = "$g" ] || want+=("+$s:$dst")
  done
  [ ${#want[@]} = 0 ] && { echo "mirror: GitHub = shared ($(date -u +%H:%MZ))"; exit 0; }
  if out=$(git -C "$R" push -v "$GH" "${want[@]}" 2>&1); then
    echo "mirror: pushed ${want[*]}"; delay=120; first_fail=""; continue
  fi
  [ -n "$first_fail" ] || first_fail=$(date +%s)
  { echo "# $(date -u -Is) git push -v $GH ${want[*]}"; echo "$out"; } > "$LOG"
  echo "mirror: push failed ($(( ($(date +%s) - first_fail) / 60 )) min failing); retry in $((delay/60)) min"
  sleep "$delay"; delay=$(( delay * 2 > 900 ? 900 : delay * 2 ))
done
