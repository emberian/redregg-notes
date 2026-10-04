#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-bend-efficiency-20261003/src
lane_root=/tank/dregg-build/codex-bend-efficiency-20261003
lane_common=/home/hbox/workbox/codex-unified-integration-20261003/src
lane_lean=/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean
python3 - "$lane_common/.lake/build/lib/lean" /tank/dregg-build/codex-private-lifecycle-20261003/olean "$lane_root/olean" <<'PY_OVERLAY'
from pathlib import Path
import sys
out=Path(sys.argv[3])
for root in map(Path,sys.argv[1:3]):
 for src in root.rglob('*'):
  if not src.is_file(): continue
  dest=out/src.relative_to(root)
  dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists() and not dest.is_symlink(): dest.symlink_to(src)
for module in ['Theory/BendBookIndex','Theory/BendLiveMachine']:
 for suffix in ['.olean','.ilean','.olean.server','.olean.private']:
  dest=out/(module+suffix)
  if dest.is_symlink(): dest.unlink()
PY_OVERLAY
export LEAN_PATH="$lane_root/olean:/tank/dregg-build/codex-private-lifecycle-20261003/olean:$lane_common/.lake/build/lib/lean"
for lane_package in "$lane_common"/.lake/packages/*; do
 export LEAN_PATH="$LEAN_PATH:$lane_package/.lake/build/lib/lean"
done
export LEAN_NUM_THREADS=2
for lane_module in Theory/BendBookIndex Theory/BendLiveMachine; do
 "$lane_lean" -j2 "$lane_module.lean" -o "$lane_root/olean/$lane_module.olean"
 printf 'BEND BOOK INDEX MODULE PASS %s\n' "$lane_module"
done
"$lane_lean" -j2 tests/BendBookIndexBenchmark.lean
printf 'BEND BOOK INDEX SOURCE PASS\n'
