# OPS — nanodregg's operations, looked at (real 2026-10-27)

Lane: OPS (Claude), from OVERLOOKED-20261027.md items A4, A5, A9, B1 and the operator items. Worktree
`hbox:~/nd-land/ops` (from origin/main 8fe58cbf). Four landings by rule 1, three cards filed.

## Cards filed (not built)
- 01a17e36-6510 a member's lost key file: what is and is not recoverable, a row (OVERLOOKED B2)
- 01a17e36-6541 the provider pin expires 2026-12-20: a dated check before the hosted resident depends on it (B5)
- 01a17e36-655b macOS: the sandbox-exec half unrun since 10-17 (A8)
- 01a17e36-89c7 KEYS.certified lives on one box: an off-box monotone copy (OPS-21's alternative c)

## Landings
(in progress; hashes added as each lands)
ROOT (real 10-27): the infra lane's two deviations when installing 6087dd4a on dregg-demo, to write into RUNBOOK as the real procedure: (1) `run.sh genesis` refuses an existing store directory and the tenant's store is a quota mount, so genesis ran in a staging directory as the tenant and the store, gb/, run/ and genesis.txt were moved into place (better: let `run.sh genesis` accept an existing EMPTY directory or a mount point); (2) verify-tenant.sh is written for hbox's `nd` user; on the box it ran with `nd-testground` substituted, as root against the installed unit (make the uid a parameter).
