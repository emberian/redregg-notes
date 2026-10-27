# HERMES-BWRAP log (2026-10-14)
Lane: hbox /tank/dregg-build/claude-lanes/hermes-bwrap/src, branch lane/hermes-bwrap (base next).
## events
- start: read SAFETY-BLOCK, INPUTS-HBOX-LOG (JPAY6, m6grain), LAND-HBOX-LOG.
- 21:20Z lane at hbox hermes-bwrap/src = next 0125b224 + lane/inputs-hbox (f72dbdc5, ff; it rewrote product_userns, so mine supersedes it without a conflict).
  New deploy/grain-host/resolve-bwrap: prints the physical bwrap (profiled /usr/local/libexec/mini-grain-bwrap when present+userns works, else /usr/bin/bwrap; MINI_BWRAP selects one of those two only). Users: hermes-journey.sh + jpay6.sh (launcher via the existing, previously unused deploy/grain-host/materialize-bwrap.py instead of cp / string replace), grain-journey.sh (spk-host profile `bwrap`, resolved lazily at profile write; floor() exempts task name mini-grain-bwra), hermes_catalogue_probe.rs, journey-rows product_userns (runs the set's resolver, exports MINI_BWRAP; resolver-less sets keep the legacy probe).
- 21:22Z hermes single row launched (run-row.sh, pid file run-row.pid) vs next=7ffd6524, results /tank/dregg-build/pipeline/runs/hermes-bwrap/. cargo check grain-runtime --tests started (check.pid).
- 21:28Z VERDICT hermes PASS 342 s (single row, next 7ffd6524, lane runner; runs/hermes-bwrap/): launcher materialized for /usr/local/libexec/mini-grain-bwrap; SIGKILL mid-write op 14, unit restart NRestarts=1, op 14 resolved performed by restart recovery, readback 1, delegation to friend.
  Negative control MINI_BWRAP=/usr/bin/bwrap: hermes UNCONFIGURED 0 s "missing input: unprivileged user namespaces for bwrap (MINI_BWRAP /usr/bin/bwrap: ... Permission denied ...)". m6grain UNCONFIGURED 1 s on uid 1001 only.
  cargo check grain-runtime --bin --tests: ok (no warning in hermes_catalogue_probe).
- absent-inputs.tsv: hermes removed, m6grain reason rewritten; previous absent-inputs.tsv.before-hermes-bwrap.
- committed a63c33ff on lane/hermes-bwrap (next 0125b224 + inputs-hbox f72dbdc5), pushed to mirror; GitHub: hbox has no key -> ROOT.
- m6grain note: no uid 1001 exists on hbox; when it does, it needs exec on mini-grain-bwrap (root:hbox 0750, ACL only mini-hbox-app-00) or the resolver falls back to /usr/bin/bwrap and the row says 98 by name. That is a custody decision (Ember).
- 21:35Z jpay row (same lane, next 7ffd6524): JPAY1-4 PASS; JPAY6 FAIL 2 s on the known consent red (cv 01a13c42-dc55): "query parent-witness-tool-pre: minidregg-client-consent: unsupported settings in client consent provider". It fails before the bwrap section, so this run doesn't exercise the new launcher path.
- DONE. Report sent to ROOT.
