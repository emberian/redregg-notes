# IMPACT-BAR: the bar harness fix (PERF-13, R-0037)

**Changes** (hbox wt/bar-e9c126f, now on main e33a9b1, uncommitted until landing):
- `scripts/bar.sh`:
  - Re-runs one end only: exit `command_exit::DECLINED` with stderr exactly `declined stale`. The `refused
    stale` match is DELETED; a recorded stale is a kernel violation and stays RED by name.
  - Reads `DECLINED` (53) and `host_op::SUBMIT` (1) from `client/src/generated.rs`, the emitted table nd is
    built from. The name `stale` stays a literal, because no emitted table exposes `rejectNames`; the forced
    stale is its tooth.
  - In --standing, forces exactly ONE contention. A relay on friend1's host socket holds its first SUBMIT
    frame while resident's next planned write of friend1's object commits, then releases it. The writer
    declines `stale`; bar.sh syncs and re-runs; the write commits.
  - bar.sh then requires `1 1 0` exactly, and is RED `forced stale: …` otherwise.
  - --harness-control expects 2 stale writes, and that comparator must fire for the control to count.
  - The stale count line's false text (recorded, spends budget) is rewritten.
- `gates/waste.tsv`:
  - New rows `bar stale-writes 1`, `bar stale-reruns 1`, `bar stale-after-sync 0`.
  - The source text of `bar steps-per-command` is corrected. Its ceiling stays 1.000; no ceiling rose.
- `decisions/perf.md`:
  - PERF-1 :76 now says `declined stale`.
  - :119 FINDING 2 is marked CLOSED by KERNEL-54.
  - New entry PERF-13, with critique and meta-critique.

**Measured** (logs/barfix-*.log):
- Standing, at e9c126f twice and at e33a9b1 once: PASS. Each run reads 1/1/0, and every other pinned WASTE
  line equals its row (steps 1.000, seg-bytes 757.700, reopen-tail 350.300, …).
- Control: RED harness-control, with all comparators fired, the forced stale included.
- Full N=1000: UNJUDGED on load 11, p99 62.5 ms. Before the fix, full runs were RED.

**Plants** (each RED by name):
- STALE_MAX=0 reads `RED friend1 nd write exit 53: declined stale`.
- The pre-fix `refused stale` matcher reads the same.
- The forced stale switched off reads `RED forced stale: stale-writes 0 … want 1 1 0 (holds 0)`.

**Not widened:**
- STALE_MAX stays 8.
- No other exit-53 reason is accepted, and a stale must be exit 53 with exactly `declined stale`.
- No limit, load rule or ceiling moved.

**Flag day:** none. This is harness and gate data only. No deployed code, wire or Store changes.

**Judge:** the landing touches `scripts/` and `gates/`, so it runs as FULL through scripts/commit.

**Worktrees:**
- wt/bar-e9c126f: its one-line edit is ABSORBED into this change.
- wt/bar-f8d04ac: its one-line edit is REVERTED (`git checkout -- scripts/bar.sh` there).
