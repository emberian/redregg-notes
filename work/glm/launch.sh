#!/bin/bash
# glm/launch.sh NAME [model]  — runs claude-glm (Z.AI GLM via Claude Code) on glm/NAME.brief.md as a detached worker.
# Report channel: the brief names its report file. PID file glm/NAME/run.pid; log glm/NAME/run.log.
set -euo pipefail
name="$1"; model="${2:-glm-5.3}"
here="$(cd "$(dirname "$0")" && pwd)"; brief="$here/$name.brief.md"
[[ -r "$brief" ]] || { echo "no brief $brief" >&2; exit 1; }
mkdir -p "$here/$name"; cd "$here/$name"
GLM_MODEL="$model" nohup claude-glm -p "$(cat "$brief"; echo; cat /Users/ember/dev/redregg/work/METHOD-20261027.md)" --dangerously-skip-permissions --output-format text > run.log 2>&1 &
echo $! > run.pid; echo "$name pid $(cat run.pid) model $model"
