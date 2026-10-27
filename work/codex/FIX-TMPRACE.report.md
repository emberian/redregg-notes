# FIX-TMPRACE report (cv 01a17007-bdbe; decision GATES-25)

2026-10-24 22:30Z READ  logs/root-converge-readers3.log:2,8-9 — the red at 743a4fb: `run concurrency cargo:devtools:workspace + script:scripts/bar.sh: RED(shared scratch: … /tmp/rustix_test_can_compile …)`, attributed to 743a4fb, 3794975, 2d5056e, 1ab410e (none caused it).
2026-10-24 22:32Z READ  hbox ~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustix-1.1.2/build.rs `can_compile`: `rustc … -o std::env::temp_dir().join("rustix_test_can_compile")`. Three probes run unconditionally (use_static_assertions, has_lower_upper_exp_for_non_zero, diagnostic::on_unimplemented), whatever CARGO_CFG_RUSTIX_USE_LIBC etc. say: there is NO switch to pin the probe off. So option 2 of the brief does not exist; the fix is the per-run TMPDIR.
2026-10-24 22:35Z READ  gates/runs.py run(): cargo/script rows got ND_LEAN_BIN + CARGO_TARGET_DIR, exe rows the judge's env; nobody set TMPDIR. gates/readset.py excludes .lake/runs/ and .lake/cargo-target/ from writes; /tmp paths are WR absolute.
2026-10-24 22:40Z INFERRED+MEASURED-length  TMPDIR under {fresh} is wrong: client/tests/supervise.rs binds `temp_dir()/nd-sup-exposed-<pid>.sock`; under a gate tree's .lake/runs/<row>… that is >120 bytes (sun_path 108). So the runner makes `tempfile.mkdtemp(prefix="nd-runtmp-")` (0700, ~24 bytes) per run, and readset excludes it.
2026-10-24 22:50Z MEASURED  plant (wt/fixtmprace-plant = cp -a of the standing tree at 743a4fb; cargo cache restored from a pristine copy before each plant with rustix's dev build-script run removed and release cold; the two real rows; gates/runs.py --slots 2, private slots dir; driver hbox logs/fixtmprace-plant.sh, outputs logs/fixtmprace-plant-{old,sharedtmp,new,old-alone,new-alone}.out):
  - main's runner, together: `runs: ok` — BLIND. Both rows NS=true, re-run alone on a warm cache; the first (cold) run's read-sets hold WR+RM /tmp/rustix_test_can_compile in BOTH rows, but the check read only the verdict run.
  - main's runner, alone-from-start (the 743a4fb schedule, `_walls.json` ns): the convergence's exact RED line, reproduced.
  - union check + shared /tmp (TMPDIR lines removed): the same RED, under concurrency.
  - this card, together and alone: `runs: ok`, both rows pass (devtools 2 runs, BAR control + 60 standing + 1000 full, PASS); tmp-class paths 219→2 / 239→24 (bwrap's /tmp/newroot, /tmp/oldroot only); /tmp/rustix_test_can_compile mtime unchanged; no nd-runtmp-* left.
2026-10-24 23:45Z MEASURED  this card's runner over EVERY row of the plant tree (standing benches included, --slots 2): `runs: ok (83 runs of 58 exes)`, no concurrency red, 0 nd-runtmp-* left (logs/fixtmprace-all-rows.out). A different TMPDIR does not re-key cargo (devtools' alone re-run 1 s, warm).
2026-10-24 23:50Z READ  scan for other fixed /tmp paths (git grep scripts/ gates/ */tests/*.rs */src/*.rs build.rs *.lean): none a row writes —
  - client/tests/supervise.rs:53,341 `/tmp/nd-never.sock` and client/tests/stdio.rs:215 `ND_WORKSPACE=/tmp`: argv strings refused before any file is touched;
  - temp_dir() users (attach, client mux/sockets/supervise, devtools workspace, sandbox confine): pid-named, and now inside the private TMPDIR;
  - devtools::scratch `$HOME/.cache/nd-t/<pid-named>`: custody requires an owner-only chain, so it cannot move to /tmp; safe by name;
  - launcher CARGO_TARGET_TMPDIR names: pid-named (note: under .lake/cargo-target, which readset excludes, so the check cannot see them; safe by name only);
  - bar.sh mktemp ${TMPDIR:-/tmp}/ndbar-build.XXXXXX (now private), $HOME/ndbar.XXXXXX, $HOME/.nd-bar/run.XXXXXX: random;
  - gates/*.py plants: tempfile.mkdtemp, now private and reaped;
  - sandbox/tests/custody.rs:210 reads /tmp as the refused object (not a row).
  OBSERVED, not this card: scripts/bar.sh:664 appends to `$here/gates/bar.tsv`, a tracked file of the judged tree.
2026-10-24 23:55Z DECISION GATES-25 (decisions/gates.md): per-run TMPDIR; readset `scratch` exclusion, key v8; a re-run-alone row checked on the union of both runs' read-sets (Row.beside). Critique + meta-critique in the entry.
2026-10-25 00:40Z MEASURED  LANDED ad90a47 (scripts/commit, full judge by main's code: `PRE-PUSH GREEN tree 5aaacbfeea9f`, 38 rows run at up to 4 at once, no concurrency red; pushed to origin). hbox logs/fixtmprace-land1.log.
2026-10-25 00:42Z DONE  cv 01a17007-bdbe closed with ad90a47. Removed my own scratch only: wt/fixtmprace-plant (1.7G copy of the standing tree), wt/fixtmprace-pristine-ct (710M), wt/fixtmprace-scratch. Kept: worktree wt/fixtmprace (detached at main), logs/fixtmprace-*.
INFERRED  until the next convergence runs THIS runner, the 743a4fb sighting stays in converge-state; the next convergence at another main re-keys every row (v8) and should read the pair FIXED, not REVERT-PENDING. Worth a glance at that convergence's line.
