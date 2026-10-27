# PUBLISH — the nanodregg testground on GitHub Pages (real 2026-10-26/27)

**URL: https://emberian.github.io/nanodregg/** (Pages source `gh-pages` `/`, HTTPS enforced, legacy build).

- 23:05 EDT tip recorded: nanodregg origin/main **914f2d7e** (CLIENT-43, the hosted World). hbox worktree
  `wt/publish` (detached; `.lake/build` copied `cp -a` from `wt/testground`, 1.4 GB apparent).
- 23:12–23:24 Lean half on hbox: `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 JOBS=3 swarm-build testground/build/build.sh c
  wt/publish/.lake/pub/work` (FRESH work dir; PID file `.lake/pub/c.pid`). 111 tree modules + 649 toolchain modules,
  0 FAIL. pack.tgz 8,095,230 B, sha256 9c4464e3…6b24.
- 23:27 wasm half on the laptop (emcc 6.0.9): `CPATH=<work>/libuv/include build.sh wasm WORK`, libuv headers cloned at
  v1.48.0 (the toolchain's own wasm pin) because main's build.sh still takes uv.h from CPATH (Homebrew 1.53 here);
  landing 3's build.sh pins them itself. **kernel.wasm 4,200,503 B, 804,105 B gzip -9** (Pages serves it gzipped at
  853,857 B), sha256 ec3a83d6bed5e1dbaa7e28ea1ab2296cb7107bb9afbcae22158bf88a9c39601d; kernel.mjs sha256 38b2c6c5….
  Link warnings: 10 signature mismatches (lean_io_create_tempfile/tempdir and eight `nd_file_*`/`nd_dir_sync`: the
  Lean externs pass the world token, file.c's C does not) — the in-memory Store the page drives never calls them; they
  would trap if called. The design doc names two; Host.File's now adds eight.
- Checks on the built kernel (node 26): `lies-run.mjs` 7/7 CAUGHT; `demo-run.mjs document` DEMO OK.
- Local Chromium (python3 -m http.server, PID file): desktop drawn in 239 ms, six icons, Writer menu with 7 lies,
  "Start here" step 1 `alice$ nd create` → **`exit ok · 46.5 ms · 11 frames`**. promo/testground-local-914f2d7.png.
- 23:28 published: orphan `gh-pages` commit **ae9318a6** (unsigned) holding only what the browser loads: index.html,
  testground.{js,css}, nd.js, transport.js, demos.js, kernel.{mjs,wasm}, world/{doc,escrow,head,resident}, LICENSE,
  .nojekyll, README.md (what the branch is, built from 914f2d7e, the hosted parameter). 26 MB tree (world/ texts dominate).
- Pages: pushing `gh-pages` enabled Pages by itself (the POST answered 409 "already enabled"); build `built` in 21 s.
- Published Chromium: desktop drawn in 882 ms (network), same icons and Writer menu, step 1 **`exit ok · 36.9 ms ·
  11 frames`**. **promo/testground-published.png**.
- Hosted mode: selected ONLY by the URL — `?hosted=wss://HOST/ws&join` (testground.js `hostedDefault()`, line 104/445).
  Without it the page runs the World in the tab and opens no socket. The published README documents the parameter and
  says no hosted World is published yet; nothing points at wss://nano.demo.dregg.online. (The World window's
  "Join the hosted World…" button prompts with ws://127.0.0.1:8787/ws as its placeholder — loopback, not a dead host.)
- What a visitor sees: a blue early-00s desktop (World, alice, bob, Wire, Start here, Demos; taskbar with
  "writer: honest"); the World window with origin/nonce/founders/chain and "kernel loaded in N ms; genesis in N ms, in
  this tab"; two terminals; the six-step tour (create, write, describe, grant, the declined race, the lying writer);
  the Writer menu; the Wire window of every frame; Demos ▸ the document.

## FOUND: main moved to 00b4f793 (PROTOCOL-77.1) while I built; its kernel breaks one lie scene
- 23:35–23:51 rebuilt at **00b4f793** (same recipe, work2): kernel.wasm 4,225,228 B / 808,985 B gz, DEMO OK, but
  `lies-run.mjs` **6/7: MISS forkedPost** — `STOPPED at "argv" with refused program` (expected `refused forkedPost`).
  TESTGROUND-3 predicted it: 77.1 changes what the forkedPost scene substitutes ({@sponsor}/{@world}, selfHeadSeed).
  lies-run is not a gate on main yet (landing 3 adds it as `script:testground/build/gate.sh`), so 77.1 landed green.
- So the PUBLISHED page stays at 914f2d7e (all 7 lie scenes work). Republish after landing 3 (rebased onto 77.1;
  its gate will read this red) or after a fix to the scene: one run of testground/PUBLISH.md. Owner: the testground
  lane (CLIENT); not touched here.

## The recipe
- `testground/PUBLISH.md` + `testground/publish-check.mjs` (the Playwright check) landing on main via `scripts/commit`
  FAST from hbox `wt/publish` (`client:`), launched after ROOT's hold ended (00b4f793 = PROTOCOL-77.1 on main);
  lander PID file `wt/publish/.lake/pub/land.pid`, log `land.log`, message `msg.txt`. Copy of the recipe:
  scratchpad `publish/PUBLISH.md`.
- 00:20 the recipe's lander (PID 525110) is judged — candidate 48cd3c97 on base 00b4f793 — and is waiting in
  `gates/land.py --fast`, which by design lets displaced FULL landers (6 queued) land first; it lands and pushes by
  itself. If it is refused, relaunch from `wt/publish`: `scripts/commit -F .lake/pub/msg.txt testground/PUBLISH.md
  testground/publish-check.mjs` (files are untracked there).
- 00:40 my recipe landing did NOT land, and should not: CLIENT-49 (7d30fc1d, "the live World is a door on the
  desktop") landed its own testground/PUBLISH.md + publish-check.mjs first, a superset of mine (build/publish.sh,
  kernel.json with the kernel's sha256, the live World wss://nano.demo.dregg.online/ws stamped into deployment.json,
  `publish-check.mjs --live`). scripts/commit stopped on the add/add conflict; I removed my untracked copies from
  wt/publish. The published gh-pages (ae9318a6, built from 914f2d7e) predates CLIENT-49; republish by main's
  PUBLISH.md, which also brings the forkedPost fix question (MISS at 00b4f793) to whoever runs it.
- 05:2x UTC gh-pages was republished by the CLIENT-49 lane: 3b95821a, built from 7d30fc1d (kernel.json sha256 946fd46c…, 4,257,334 B). My check against it: see promo/testground-published-7d30fc1d.png. ae9318a6 (mine) is superseded.
