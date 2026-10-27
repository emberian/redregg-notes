# INPUTS-HBOX log (2026-10-14)

Lane: /tank/dregg-build/claude-lanes/inputs-hbox/src, branch lane/inputs-hbox (base next 0125b224), pushed to the
hbox mirror: 7c48beb0, f72dbdc5. GitHub: hbox has no key -> ROOT pushes.

## Box changes on hbox (to undo: restore the .before-inputs-hbox copies, rm -rf the inputs dir)
- /tank/dregg-build/pipeline/box.env regenerated with box-env (same args + --set): adds MINI_TEST_PROVIDER_BIN,
  MINI_LAUNCH_GATE_BIN, MINI_FN_LAUNCHER, MINI_FN_CORE. Previous: box.env.before-inputs-hbox.
- /tank/dregg-build/pipeline/inputs/fnbin/6679dae0e/: cp -a of /tank/fn/scratch/mini-fnbin/6679dae0e/fn-6679dae0e
  (+README); image.sha256 verified. /tank/fn was only read.
- /tank/dregg-build/pipeline/inputs/fixtures/7ffd6524/: mini-hermes-test-provider (cargo --release --locked,
  target /tank/dregg-build/claude-lanes/inputs-hbox/target) + launch-gate (rustc -O launch-gate.rs); SHA256SUMS.
- absent-inputs.tsv: removed m7, jpay/JPAY6, exchange; m6grain kept, reason rewritten. Previous: .before-inputs-hbox.
- NOT created: no user, no sudoers, no linger change (see m6grain).

## Findings
- m7: all four READY sets (7dea0626 d37eee80 30a5009a 7ffd6524) share compiled inputs (8c469027ee9a) and outputs
  (ced39aeb5bd6) -> runner picks the newest other same-input READY set. First run FAILED on the row predicate
  `(.checks|length)==5` vs m7.sh's 6 checks; fixed by name.
- JPAY6: the userns probe tested /usr/bin/bwrap while jpay6.sh falls back to /usr/local/libexec/mini-grain-bwrap
  (root:hbox 0750, AppArmor profile mini-grain-bwrap loaded since 09-27; userns works through it, measured). With
  inputs supplied it ran: (1) genesis lacked clockTickers/tailBound (fixed), (2) now FAILS: client consent provider
  refuses jpay6's config keys continuityProviderResourceId/providerMetering (Host/ClientConsentCore.lean allowlist).
- m6grain: row requires the runner itself at uid 1001 (two-world-journey.sh hard-codes 1001 and operator `ember`);
  creating an account cannot move the verdict while the service runs as uid 1000, and behind it product_userns on
  /usr/bin/bwrap (spk-host sandbox.rs pins it) is the hermes AppArmor decision. Left declared.
- hostupgrade/HOST-UPGRADE-PREVIOUS: main -> 7dea0626 is the only READY main set; resolves at the next landing.

## Verdicts (single rows, next 7ffd6524, lane runner, results /tank/dregg-build/pipeline/runs/inputs-hbox{,-r1}/)
- m7 PASS 22 s: candidate 7ffd6524 reproduces 30a5009a
- exchange PASS 50 s: local fn stopped; exact selected packet admitted and signed readback verified
- jpay/JPAY6 FAIL 6 s: minidregg-client-consent: unsupported settings in client consent provider (JPAY1-4 PASS)
- m6grain UNCONFIGURED 1 s: missing input: operator uid 1001 (runner is uid 1000)

## cv tasks
- 01a13c42-dc55 JPAY6 consent-provider red
- 01a13c42-dc75 per-tip test fixtures in publish-artifacts
- 01a13c42-dc99 M7 reference independence (shared sccache)
- 01a13c42-dcb6 m6grain uid 1001 / userns
