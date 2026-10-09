# Host fuzz findings (BURN-BENCH, 2026-10-08)

## Status: NO FINDINGS. The fuzz run has not happened.
Wound down on ROOT's order before the first completed run. The harness is built and the corpus is captured, but no input has been judged under a working harness. "No findings" here means "nothing was run", not "nothing is wrong". The fuzzer has not been smoke-tested since its last fix (see Harness), so it is unproven.

## What exists
- Branch `lane/bench-store` at aca27bfe in burst2-a:/srv/git/minidregg.git, under `scripts/bench/`:
  - `host-tee` is a stdio frame proxy installed as `minidregg-host`. It records every request and reply, the config, and a sqlite snapshot plus `.head-anchor` per store head.
  - `host-fuzz-capture.sh` runs 13 real acceptance drivers through the proxy: activity, seat, call, send, domain, upgrade, bounty, objectrecord, work-account, quote-submit, charged-failure, welcome-continuity, rooms, and the journey J0-J8 + JROT + JPAY2 + JRLANE.
  - `host-fuzz.py` is the fuzzer: `corpus`, `run WORKER NWORKERS SECONDS`, `repro DIR`.
- Corpus, on burst2-a at /srv/lanes/bench-store/tee2/. The first attempt lacked the head-anchor and is in `tee2-old`. All 13 capture drivers exited 0, except `act`, which was still running at wind-down (not checked).
- Binaries: Host and consent at cfdaf64d were fetched from the artifact set (not rebuilt), in /srv/lanes/bench-store/set/bin.

## Harness
- Per batch it restores one snapshot (sqlite plus `.head-anchor`) into a private store and starts the real `minidregg-host CONFIG stdio` on it.
- Inputs:
  - (a) random bytes to every opcode;
  - (b) one mutation of a recorded request: bit flip, byte set, truncation, deletion, insertion, duplication, u32 length-field edit, JSON field edit, cross-op payload swap, payload splice;
  - (c) a tail-byte (signature region) flip, and an exact replay of each recorded submit.
- After the batch, the recorded requests are re-sent in order as controls, and each recorded submit is sent a second time as a replay.
- Violation classes:
  - crash, EOF or exit;
  - a hang over 30 s;
  - stderr matching a crash pattern;
  - an op-255 refusal with no outcome tag or no detail text;
  - leaky error text;
  - host RSS over 6 GB;
  - the store head moving on a mutated input;
  - an exact replay advancing the head.
- Reproducers: each distinct finding is written with a ddmin-minimized request, snapshot and config under `fz/findings/<class>-<sig>/`.
- Smoke status: the one smoke run, before the anchor fix, failed every input (the host refused to start), so it proved nothing and was discarded. The fixed harness has not been run.
- Setup learned the hard way:
  - copy `<storageRoot>.head-anchor` with the sqlite, or the host refuses with "missing anchor";
  - every ancestor directory must not be group-writable, or it refuses with "anchor directory is writable by another account";
  - use umask 077.

## Coverage gaps
- Ops in the corpus: 1-5, 86-89, 91-94, 103-105, 107, 123-125, 144, 150, 151, 173, 210-212, 214-217, 219.
- Missing: pay-enrol quote (121), pay-claim quote (182), reserve-birth, pure-client ops 7/10/11, selected-release, lifecycle.
- The `mini serve` socket envelope layer is not covered (only the stdio frame layer).
- The consent binary is not a separate fuzz target.

## Next (also in /srv/lanes/bench-store/CONTINUATION.txt)
1. `python3 fuzz.py run 0 1 100`. Check `fz/stats/w0.log` shows `control_fail` 0 and low `control_diff`.
2. Run about 12 workers for hours.
3. Triage `fz/findings` and send each class to its owning deputy.
