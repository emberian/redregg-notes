#!/bin/bash
# usage: launch.sh <name> [model]   — starts one Codex worker from codex/<name>.brief.md
set -u
name="$1"; model="${2:-gpt-6-astra}"
D=/Users/ember/dev/redregg/work/codex; W="$D/$name"; mkdir -p "$W"
touch "$D/$name.report.md"
{ echo "# $name"; echo; cat "$D/RULES.md"; echo; echo "# YOUR BRIEF ($name)"; echo; cat "$D/$name.brief.md"; } > "$W/prompt.md"
cd "$W" && nohup codex exec --ephemeral -m "$model" -s danger-full-access -c approval_policy='"never"' -C "$W" --skip-git-repo-check \
  -o "$W/last.md" - < "$W/prompt.md" > "$W/run.log" 2>&1 &
echo $! > "$W/run.pid"; echo "$name pid $(cat "$W/run.pid") model $model"
