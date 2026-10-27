# TESTGROUND-2 continuation (real 2026-10-26) — read TESTGROUND.report.md's TESTGROUND-2 lines first

State:
- Landing 1 (CLIENT-42, the lying writer): `scripts/commit` FAST in hbox `wt/testground`, PID `.lake/tg2/land1.pid`,
  log `.lake/tg2/land1.log`, message `.lake/tg2/msg1.txt`. Never kill it; read the log.
- Landing 2 (CLIENT-43, the hosted World): message drafted `scratchpad/tg2/msg2.txt` (this session's scratchpad).
  Files (local worktree `scratchpad/tg2/nd`, synced to hbox `wt/testground-b` by `tg2/syncb.sh`):
  Web/Sim/Testground.lean Web/c/glue.c testground/{nd.js,transport.js,guestbook.mjs,hosted-run.mjs,package.json,testground.js,build/build.sh}
  deploy/testground/{ws-relay.py,run.sh,README.md,units/nd-testground.service} decisions/client.md gates/ceilings.tsv.
  Land it from `wt/testground` AFTER landing 1: `git checkout --detach origin/main` there, rsync the files above
  (`tg2/sync.sh`), FAST `scripts/commit -F msg2 PATHS` (SIZE lines: recount Lean lines if the judge asks).
- Hosted World test state on hbox: `wt/testground-b/.lake/hosted` (STOPPED at park; `PORT=18787 deploy/testground/run.sh
  start .lake/hosted` restarts it on the same Store), then `ssh -N -L 18787:127.0.0.1:18787 hbox` and serve
  tg2/nd/testground on 127.0.0.1:18732 for the Playwright scripts (both stopped at park).
- At park (~19:55): landing 1 passed gates/build/census/decls on its first judged attempt, then main moved and it
  re-based; it is queued again for a slot (PID file unchanged, the lander's own process).
- Checks: `node testground/lies-run.mjs [--honest]` (7 CAUGHT / 5 CLEAN + 2 n/a), `node testground/demo-run.mjs document`,
  `node testground/hosted-run.mjs ws://127.0.0.1:18787/ws [basic|document]`, Playwright `tg2/shoot.mjs`, `tg2/shoot-hosted.mjs`.
- Open cv: 01a17a6b-f7e2 (fork across two tabs), -f801 (axis demos), -f80f (hosted relay lies + lies-run gate),
  -f81d (thin joiner vs certified head after TRUST-SEED). Close 01a17a48-b31e when landing 1 is on main and
  01a17a48-b346 when landing 2 is.
- TRUST-SEED's `protocol!` PROTOCOL-77.1 is in its full judge: it moves the kernel (re-run build.sh c + wasm) and
  may change `Protocol.selfHeadSeed` (the forkedPost scene substitutes {@sponsor}/{@world}).

- ~20:05: LANDING 1 LANDED 41af1fc6 (FAST green; cv 01a17a48-b31e done). LANDING 2 launched from wt/testground
  on top of it: PID `.lake/tg2/land2.pid`, log `land2.log`, message `.lake/tg2/msg2.txt`. If it is refused for SIZE
  lines, add them to msg2 and relaunch (same paths). When it lands: `cv task done 01a17a48-b346`.
