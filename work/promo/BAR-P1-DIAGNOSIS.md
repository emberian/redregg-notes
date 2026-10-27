# BAR after phase one: diagnosis (2026-10-22, hbox)

**Verdict: phase one did not cause this. It is a harness red that predates it. It has been latent since
b48c10f (KERNEL-54, 2026-10-18 15:54), 153 commits before f8d04ac.** bar.sh re-runs a contended write only
when nd prints `refused stale`. Since KERNEL-54 the kernel *declines* stale and nd prints `declined stale`
(exit 53), so the first honest contention in full (concurrent) mode is fatal. E1, C1 and the v5 package wire
are not involved: a write in THE BAR's mix pins no package and no Std.hole fact.

## The runs

| tree | harness | verdict | key line |
|---|---|---|---|
| e9c126f (ROOT, logs/root-bar-P1.log) | stock | RED | `friend2 nd write exit 53: declined stale` (load 2.77/4.07) |
| f8d04ac (wt/bar-f8d04ac, logs/diag-bar-f8d04ac-1.log) | stock | **RED** | `friend1 nd write exit 53: declined stale` (load 2.82/3.01; writer at step 502, second half) |
| e9c126f (main, logs/diag-bar-e9c126f-1.log) | stock | RED | `friend1 nd write exit 53: declined stale` (load 2.93/3.03) |
| f8d04ac (logs/diag-bar-f8d04ac-patched.log) | line 338 → `declined stale` | UNJUDGED (load1 2.43/3.13) | stale-writes 4, re-runs 4, stale-after-sync 0; p99 86.6 ms; reopen 67.5 ms; follow reopen 108.1 ms; use 3/3; at-tip ok |
| e9c126f (wt/bar-e9c126f, logs/diag-bar-e9c126f-patched.log) | same one-word patch | UNJUDGED (load1 3.64/4.98) | stale-writes 2, re-runs 2, stale-after-sync 0; p99 62.7 ms; reopen 77.9 ms; follow reopen 159.6 ms; use 3/3; at-tip ok |

All logs are under hbox:/tank/dregg-build/nanodregg/logs/. Every run used full mode at N=1000. Every binary
was reported fresh to its tree; the patched runs show `1 dirty tracked paths`, which is the bar.sh edit. The
box never got below load1 2: two 15-day-old fn `sbcl` processes hold about 2–3 of load. So no run here
can be JUDGED, and the clock figures are reported only (37–80× inside the limits).

**Last full-mode run before f8d04ac:** de718bf, 2026-10-18 12:59Z, UNJUDGED (gates/bar.tsv's last `run`
row). It predates b48c10f, so it met stale as `refused stale` and re-ran it. Since then every BAR in the logs
(perf3/perf4/kernel23*, converge's `script:scripts/bar.sh` row at f8d04ac and at e9c126f) was `--standing`,
which is serial. A serial run never contends, so it never reaches the retry path.

## Mechanism

- `scripts/bar.sh:338` (identical at f8d04ac and e9c126f):
  `if r.returncode and r.stderr.strip() == "refused stale" and attempt < STALE_MAX:`. Anything else ends the
  command and is appended to `red`.
- b48c10f `kernel!` (KERNEL-54 shape N, decisions/kernel.md "KERNEL-54 RULED"): "`judge` DECLINES stale,
  which is never recorded. `auditRefusal` refuses a recorded stale by name." A stale is now final through
  version monotonicity (`stale_behind_forever`), not through a record. `Kernel/Proofs/Audit.lean:155`
  `judge_stale_declined`.
- nd's reply: `Protocol/Command/Machine.lean:987` `| some .declined => declined txt`, and `:177`
  `def declined (name) := .done CommandExit.declined.code … s!"declined {name}\n"`. The exit code is
  `Protocol/Command/Exit.lean:51` `declined => 53`.
- b48c10f changed the reply and did not touch bar.sh. Nothing exercised the stale path afterwards, because
  `gates/runs.tsv:50` runs THE BAR `--standing` only.
- With the match fixed, the declined attempt is harmless. The client leaves it open on disk
  (`client/src/attempt.rs` header: "Every other end (declined, …) leaves the attempt open"). The re-run after
  `nd sync` is a new call with fresh pins and commits; stale-after-sync was 0 in both patched runs.

**Is it a flake?** Only in the sense that contention is timing-dependent. Today 3 of 3 stock full runs went
RED, and the patched runs met 2 and 4 stales. The b9cd50f runs in decisions/perf.md met 15 and 0. A stock
full run passes only on a draw with zero contention. It is a pre-existing harness defect, not a race in the
system: the system's answer (declined, not recorded, no budget spent) is the one KERNEL-54 designed.

**Is it a regression from E1?** No. The version bump (package wire 4 → 5), the live column and the re-emitted
Std.hole bundle are not on the `nd write OBJ SLOT VAL [--via GRANT]` path. f8d04ac, without any of them, fails
identically. Patched, e9c126f and f8d04ac produce the same counts within the run-to-run draw: steps/cmd 1.000,
use 3, fds 0, seg-bytes/cmd 750.6 vs 753.2, records/cmd 0.548 vs 0.566.

## Fix shape (PERF owns scripts/bar.sh)

1. **bar.sh:338: re-run on `declined stale` only, and delete the `refused stale` match.** Under KERNEL-54 a
   *recorded* stale is a kernel violation (`auditRefusal` refuses it), so `refused stale` from nd must stay
   RED by name, never retried. Better still, derive the pair (exit 53, name `stale`) from the emitted units
   (`CommandExit.declined.code`, the refusal name) rather than from a string literal. A literal is what went
   silently stale here. This narrows what is accepted, so it does not widen a check.
2. **bar.sh:495's text is false since KERNEL-54.** It reads "writes that met `refused stale` … A stale refusal
   is a recorded step and spends the member's refusal budget". Rewrite it: declined, not recorded, no budget.
   decisions/perf.md PERF-1 says the same at :76 and :119 ("An honest stale re-run spends the refusal budget").
   That was FINDING 2, which KERNEL-54 closed. Mark it closed there.
3. **The gate gap: the stale path has no standing exercise.** The standing row is serial by design (PERF-1
   alt (c)), so the retry path can rot unseen. That is what happened here, for 4 days and 153 commits.
   Proposed: the standing run forces exactly one contention, in which actor A writes B's object through the
   grant with a pin taken before B's next write. The row then requires `stale-writes 1 stale-reruns 1
   stale-after-sync 0`, and `--harness-control` expects 2. A recurrence of this class then turns the standing
   row RED on every judge.
4. THE BAR stays unjudgeable on hbox while load1 ≥ 2 holds from the fn sbcl pair. This is not a reason to
   relax the quiet-box rule. A JUDGED run needs a window when those are idle, or another box.

Not proposed: anything that changes the kernel's stale answer, widens STALE_MAX, or accepts any exit 53. Only
`declined stale` is honest contention; `declined refusalBudget` etc. must stay RED.

## Scratch left on hbox

The two worktrees are wt/bar-f8d04ac and wt/bar-e9c126f. Each holds a copy of `.lake`, a release `target`,
and the one-line bar.sh patch, uncommitted. The four logs are logs/diag-bar-*.log. Nothing outside these was
written. Only the `lake build host bench-count` (a no-op) and cargo client build ran in `main`, through bar.sh,
exactly as ROOT's run did.
