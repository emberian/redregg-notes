# COORD-AUDIT 2026-10-07 — the Mini swarm's coordination toolchain

Lane COORD-AUDIT, 04:50–06:00Z. Trigger (Ember): build slots sat HELD-but-unused while lanes queued 25+ min on a
hard-coded `flock /srv/build-slot-1`, both boxes at 5–25 % load. Scope read whole: minidregg `scripts/pipeline/*`
(main c1df1f08 and BURST2-SATURATE's `lane/burst2-saturate`), `scripts/local-gates.sh` + the `check-*.sh` it calls,
both burst2 boxes' installed copies (`/srv/pipeline`, `/srv/warm-base/mk-lane.sh`, `/usr/local/bin/swarm-build`,
`/srv/build-slot-*`, `~/.profile`), the provisioning dirs `latitude-burst-20261005/` and `latitude-burst2-20261006/`,
hbox's `warm-base/mk-lane.sh` + `swarm-build` (read only), and the protocols WORKER-BRIEF, DEPUTIES (+amendments),
BURST2-BRIEF, VERIFY-ONCE, PIPELINE, FOREMAN-WORKER-ADDENDUM, LANE-PROTOCOL, queue/README, SWARM-LEDGER tail.

Severity: **S1** = lanes lose capacity or a false verdict can land; **S2** = a wait/stall or a hidden failure;
**S3** = hygiene. Status: **FIXED** (repo branch `lane/coord-audit` + installed on both boxes, tested) ·
**FIXED-BY-SATURATE** (already on its branch; I reviewed) · **HANDED** (named owner, not done) · **OPEN**.

## 0. Live measurement at the start (the bug was still happening)

burst2-b 04:58Z (`/proc/locks`, `ps`): load 14/32, 149 GB available, **slot-5, slot-6, small-1, small-2 FREE**, and
nine `flock /srv/build-slot-{1,3,4} …` processes BLOCKED for 8–36 min: slot-4 had holder 2380916 (obeng-g,
check-objective-frontend) and waiters 2381182 (1034 s), 2530659 (951 s, upgrade-turns-b4), 2531347 (940 s,
kn2-token-next), 3151283 (463 s), 3152814 (451 s, kn2-fixture); slot-1 had a 2154 s waiter (deposit-fixpoint);
slot-3 a 1027 s waiter. burst2-a: load 14/16, slot-4 and both small slots free. Every waiter's command line was a
hand-typed chain from a brief (`flock -n s1 … || flock s4`), none used the installed `slot.sh`.

Also measured: six lean-ask daemon scopes `failed` with `Result=oom-kill` (MemoryMax 16 GiB; one `lean` worker at
15.0 GB anon RSS), and a journey chain scope (24 G) lost a `lean` the same way. `fuser`/`lsof` were not installed on
either box: an ad-hoc "no holders" was a missing command.

## 1. Findings

### A. Slot acquisition and visibility

**A1 · S1 · FIXED (protocol) — hand-typed flock chains in every brief.** `WORKER-BRIEF-20261005.txt:9`
(`flock -n /srv/build-slot-1 CMD || flock /srv/build-slot-2 CMD`), `BURST2-BRIEF-20261006.txt:13-14` (chains over
slots 1–4 only), `FOREMAN-WORKER-ADDENDUM-20261005.txt:7,41-47`. Failure: the LAST flock blocks on ONE named slot
while others (5, 6, small) are free; `||` re-runs a FAILED cmd in the next slot (a red build costs two slots and
twice the time); the chains name slots that do not exist on burst2-b (5, 6) and name the gate's slot-1 on burst2-a.
This is the 25-minute queue. Fix: every brief now says `slot.sh CMD` / `build-anywhere TARGET…` only (edited at
source: WORKER-BRIEF items 2 and 6, BURST2-BRIEF SLOTS+Build block, FOREMAN addendum items 2/12/13, PIPELINE item 5,
LANE-PROTOCOL header, DEPUTIES amendment 05:35Z). Root's 05:20Z amendment supersedes the rest.

**A2 · S1 · FIXED-BY-SATURATE — `slot.sh`/`lib.sh` on main know two hard-coded slots and block on the second.**
`scripts/pipeline/slot.sh:5-7` (main): `flock -n slot-1 || exec flock slot-2` — blocks on slot-2 forever while 3/4
are free; `lib.sh` read `PIPELINE_SLOT_1/2` from `~/.profile`, which a non-login `ssh host 'cmd'` never sources, so
lanes on burst2-a silently fell back to the GATE's slot-1. SATURATE's `lib.sh` sources `/srv/pipeline/box.env`
directly (`PIPELINE_SLOTS`, polled every 5 s, all slots) and `box-env` writes it per box. Verified installed on both
boxes; a lane cannot mask it either (box.env re-exports, see test T5).

**A3 · S1 · FIXED — no way to see who holds what.** No `slots` command; `fuser`/`lsof` absent (root's probe read
"nothing"). Fix: `psmisc lsof` installed (05:28Z) and added to `bootstrap.sh`; **`scripts/pipeline/slots`** (SATURATE's
python: holder lane/pid/age/CPU of the holder's tree, waiters flagged "NAMED-SLOT WAIT while a slot is free", IDLE
state, `--reclaim` after 15 idle min, `--watch` timer) **+ my `--free`** (live list of free lane slots, exit 1 when
none). Note `fuser` lists waiters and holder alike; `slots` reads `/proc/locks`, where `->` marks the blocked.

**A4 · S1 · FIXED — no cross-box acquisition.** Nothing could use burst2-a's free slots from burst2-b. Fix:
`scripts/pipeline/build-anywhere TARGET…` (local free slot → `slot.sh`; else `ssh $PIPELINE_PEER slots --free` → push
the lane's HEAD to the shared remote as `lane/<lane>` → `peer-build` on the other box in `peer-<lane>` made from ITS
warm base, log streamed back, exit = the build's; else wait locally polling every slot) and `peer-build` as a
`box-peer-gate` forced command (`slots`, `slots --free|--json`, `peer-build LANE SHA T…`, args validated). Tested T6.

**A5 · S2 · FIXED — swarm-build scopes were anonymous.** `systemd-run --scope` without `--unit` → `run-r<hex>.scope`,
so `systemctl --user list-units` could not say which lane/build a scope was. Fix: `/usr/local/bin/swarm-build` (both
boxes + `bootstrap.sh` heredoc) names the scope `swarm-<lane>-<pid>` (lane from `/srv/lanes/<lane>/src`, or
`SWARM_BUILD_TAG`), sets `Description=<command>`, and prints `swarm-build: <unit> cap=<N> :: <cmd>` as the first
stderr line of every build log. Tested on both boxes (`swarm-coord-test-<pid>.scope … sleep 4`).

**A6 · S2 · FIXED — the gate's slot wait was unbounded.** `slot-mk.sh:5` `exec flock -E 75 /srv/build-slot-mk` with
no `-w`: a keeper stuck behind its own previous gate parks forever. Fix: `-w ${PIPELINE_GATE_SLOT_WAIT_S:-10800}`
→ a loud 75 after 3 h; `PIPELINE_GATE_SLOT` from box.env.

**A7 · S2 · HANDED (SATURATE, lean-ask owner) — lean-ask daemons OOM at 16 G.** `lean-ask:553` `LEAN_ASK_MEM_MAX`
default 16G; a single `lean --worker` reached 15 GB on `Host/SeatJson`; six daemons died (`Result=oom-kill`), each
restart reloads every import (minutes) and the lane sees "infra" errors. Fix: default 32G (the slice is 160G now) or
OOMPolicy that survives one worker; it is SATURATE's file.

### B. Base, lanes, copies

**B1 · S1 · FIXED — three divergent `mk-lane.sh` copies.** Installed `/srv/warm-base/mk-lane.sh` (md5 0612cb41) ≠
repo `scripts/pipeline/mk-lane.sh` (torn-copy guard + `--from next`) ≠ `latitude-burst2-20261006/mk-lane.sh`
(sed-patched in place by `relay-b2.sh:8`). Fix: ONE copy, the repo's; `advance-base-burst.sh` and `relay-base.sh`
install it to `$W/mk-lane.sh` by rename at every advance; `make-warm-base.sh` takes it from `/srv/mini` at the tip;
the provisioning dir keeps a labelled copy. Installed on both boxes.

**B2 · S2 · FIXED — mk-lane destination claim was a TOCTOU.** `mk-lane.sh:76,85` `[ ! -e $DEST ] … mkdir -p`: two
agents creating the same lane name get two half-copies interleaved into one tree. Fix: `mkdir "$DEST"` as the atomic
claim before the disk check. Tested T3: two concurrent `mk-lane.sh coord-audit-t` → exactly one `OK`, one `REFUSED
(or another mk-lane is creating it right now)` rc 65.

**B3 · S1 · FIXED — relay published an unverified base (wrapper answers for the work).** `relay-base.sh:17` and
`relay-b2.sh:16`: FROZEN rewritten and NOT-READY removed, THEN `timeout 550 mk-lane --verify | tail -1` — the pipe's
status is `tail`'s, a failed or timed-out replay changes nothing, lanes copy a base that recompiles. Same order in
`advance-base-burst.sh:35-38`. Fix: NOT-READY stays through the swap AND the verify (`verifying <tip>…`), the probe
runs with `MK_LANE_PROBE=1` (mk-lane admits only that marker), success removes NOT-READY, failure leaves it with the
reason and exits 8; no `| tail`.

**B4 · S2 · FIXED — nested-ssh quoting.** `relay-base.sh:8-17` and `relay-b2.sh` are 300-char double-quoted ssh
strings full of `\$`; one wrong escape silently runs on the wrong side. Fix: remote steps are quoted heredoc SCRIPTS
fed to `ssh HOST bash -s -- args` (no local expansion).

**B5 · S2 · FIXED — `mv src src.prev-<old>` into an existing dir.** Re-advancing through a tip whose `src.prev-`
already exists nests the base inside it. Fix: refuse (exit 7) in advance and relay; also refuse when NOT-READY is set
(a failed advance is not silently retried over).

**B6 · S2 · FIXED — `--from next` on a box with no next base** gave "base not frozen (/srv/next-base/FROZEN missing)".
Neither box has `/srv/next-base`, yet DEPUTIES 01:45Z says "LANES BUILD ON next" and WORKER-BRIEF says `--from next`.
Fix: a named refusal that says what to do (main lane + `git fetch github next && git rebase github/next`); LANE-ORIGIN
now says `first: git fetch github next`. **OPEN**: whether the keeper wants a real `next` base per box (it would make
`--from next` honest); the train currently has `next` = 41ca9444 ≠ main.

**B7 · S2 · FIXED — LANE-ORIGIN.txt taught a slot-less build.** `mk-lane.sh:140` `build: … swarm-build lake build`
(no slot) and `first: git rebase github/main`. Fix: `slot.sh swarm-build lake build`, lean-ask/lane-check for checks,
threads from box.env, and a "who holds what" line.

**B8 · S3 · OPEN — hbox `warm-base/mk-lane.sh` has no torn-copy guard** (the 2026-10-05 defect); hbox is fn's, not
touched. Persvati's copy likewise.

### C. Gates (where a verdict can be wrong or never arrive)

**C1 · S1 · FIXED — Lean built outside any slot or cap in the merge gate.** `merge-gate-checks.sh:25,30,52,64`
`${LAKE_WRAP:-nice -n 10} lake build …` — with LAKE_WRAP unset (anyone but the keeper's one tmux line) new targets,
exe roots, AxiomCensus and the ledger's imports compile with no slot and no memory cap. Fix: default
`LAKE_WRAP="$H/slot-mk.sh swarm-build"` when swarm-build exists.

**C2 · S2 · FIXED — no check or gate had a timeout.** `merge-gate-checks.sh:18` `run()` and `local-gates.sh:138`:
a hung journey/server parks the gate (FAIRY-GREEN 10-05: CI's "4 h hang" was a gate still running). Fix: every
`run` under `timeout -k 30 $PIPELINE_CHECK_TIMEOUT_S` (2 h) → `TIMEOUT(…s)` counts red; `local-gates.sh` runs each
gate under `timeout -k 30 $LOCAL_GATES_GATE_TIMEOUT_S` (3 h, 0 = none) → status TIMEOUT. Tested T4: `timeout` kills
the whole process group (0 survivors of a `sleep &; sleep; wait` tree).

**C3 · S1 · FIXED — `regen-pins.sh:6,9` `… | tail -1` hid a red re-check** (no pipefail): a Host-closure pin that
was still red after `--update` committed anyway. Fix: `set -euo pipefail`, output captured then printed.

**C4 · S2 · FIXED — `run-gate-burst.sh:8,11,17` hard-coded `/srv/lanes/mk-tools/…`** (absent on burst2-b; the
keeper's private copies drift from `/srv/pipeline/scripts`). Fix: `$here/…`; keeper's `mk-tools` copies refreshed
by rename (a running bash keeps its old inode).

**C5 · S2 · OPEN — gate `.done` ordering.** `run-gate-burst.sh` writes `gate-TAG.done` after the checks; readers
that poll `.done` then read `.summary` are fine, but nothing records a gate that died mid-way (no `.done`, no
`.failed`): the keeper reads "still running" forever. Suggest `trap` writing `gate-TAG.aborted` on EXIT≠0.

**C6 · S2 · noted — `hyp-ledger-baseline.txt` is empty on SATURATE's branch** (kn2-hyp-ledger 2e055e37: five red
families made green, baseline ratcheted to empty) vs five entries on main. Deliberate; the gate's KNOWN-RED arm is now
dead code until a new baseline — fine, just know a ledger red is a real red again.

### D. Artifacts, journeys, inner loop (SATURATE's files; reviewed, handed)

**D1 · S2 · HANDED — `publish-artifacts:50` exits 0 when another run holds the tip's lock** ("being published by
another run"). A hand invocation reads success with nothing published; `artifact-watch:36` cannot tell "done" from
"someone else's". Use exit 75 and treat it as in-progress.

**D2 · S3 · HANDED — `publish-artifacts:58` hard-codes `/srv/warm-base/src`** as the fallback tree (use
`$PIPELINE_WARM_BASE`).

**D3 · S2 · HANDED — `artifact-watch` sticks after 3 failures** (`$ARTIFACT_ROOT/.work/TIP.failed`, "not retried until
removed") with no message to anyone; the journey runner then never sees that tip. Emit a line into the merge queue
or a message, not only a file.

**D4 · S3 · HANDED — `pipeline_slot`/`pipeline_build_slot` read exit 75 as "slot busy"**; a CMD that itself exits 75
is re-run in the next slot. Rare; use `flock -E 253`.

**D5 · S2 · HANDED — `journey-runner:49` `rm -rf "$J"` on re-run of a tip** wipes the earlier evidence before the new
run writes any (retries that wipe progress). Rename to `$J.prev` first.

**D6 · ok — stale-olean false greens**: `lane-check` and `lean-ask` ask Lake (`lake build --no-build`) and
`lean-ask` refuses (exit 3) on a changed import; `lane-staleness-selftest` exists. PIPELINE item 5 and WORKER-BRIEF
item 2 still said bare `lake env lean` — fixed (A1). FOREMAN addendum item 2 too.

**D7 · S3 — `scripts/pipeline/install` is `rsync --delete`** of the installing checkout: anything installed by hand
into `/srv/pipeline/scripts` (my first `slots` draft) vanishes at the next install from a branch that lacks it. Not a
bug, a rule: nothing is installed that is not on the branch being installed; SATURATE and I now share one branch line
(`lane/coord-audit` on top of `lane/burst2-saturate`).

### E. Protocols that contradicted each other (all edited at source)

- WORKER-BRIEF:7 "never bare `lake env lean`" vs WORKER-BRIEF:8 "Inner loop: `lake env lean <file>`" vs PIPELINE:5 the
  same — one file both forbade and prescribed it. Now lean-ask/lane-check everywhere.
- Queue: WORKER-BRIEF:16 "`- [QUEUED]` line, the keeper's watcher matches only that" vs DEPUTIES 00:55Z "the keeper
  does NOT watch the file; SendMessage" vs queue/README "one file per range in work/queue/". Now: queue file + message.
- Mirror target: WORKER-BRIEF:17 persvati bundles (burst-1 era) vs BURST2-BRIEF:30 hbox bundles. Now hbox + shared remote.
- Threads: BURST2-BRIEF:9 `LEAN_NUM_THREADS=4` vs box.env 5 (a) / 6 (b). Now "from box.env".
- Slots: BURST2-BRIEF "4 per box", DEPUTIES "4 build slots per box", `/srv/SLOTS.txt` six on b. Now box.env is the list.
- LANE-PROTOCOL-20261004 is the hbox era (cp -al clones, hbox paths, hbox swarm-build 8G defaults); it is still
  "read first" in WORKER-BRIEF:4. Header now marks those sections historical and points at BURST2-BRIEF.
- DEPUTIES 01:45Z "LANES BUILD ON next" vs no next base on any box (B6).

### F. Provisioning (`latitude-burst2-20261006/`)

- `bootstrap.sh`: `psmisc lsof` added; swarm-build heredoc = the named-scope version; slot files still fixed at 4 +
  mk (SATURATE's `box-env` now sizes/declares them; **OPEN** for `burst-up`: size from nproc/RAM).
- `make-warm-base.sh:18` took `mk-lane.sh` from `/srv/mini-logs` (a hand scp) → now from the repo at the tip.
- `relay-b2.sh` is superseded by `scripts/pipeline/relay-base.sh` (same function, verify-before-publish, no sed patch of
  mk-lane). **OPEN**: both boxes now hold each other's peer keys; the relay still goes through the Mac — a direct
  `tar | ssh` would need `box-peer-gate` to admit it (write to `/srv/warm-base/src.new` only).
- Nothing here is one entry point; see "Next quest" below.

## 2. Tests run (artifacts)

- **T1 slots**: both boxes, table + `--free` + `--json`; burst2-b at 05:02Z showed slot-1..4 HELD with CPU 100–356 %,
  5/6 free, three waiters on slot-4 and one on slot-1 (the live bug, in the tool's own words).
- **T2 named scopes**: `SWARM_BUILD_TAG=coord-test swarm-build sleep 4` → `swarm-coord-test-<pid>.scope … sleep 4`
  listed on both boxes; first log line `swarm-build: swarm-coord-test-1404469 cap=24G :: sleep 4`.
- **T3 mk-lane claim race** (burst2-b): two concurrent `mk-lane.sh coord-audit-t` → A rc 0 `OK`, B rc 65 `REFUSED
  destination exists (or another mk-lane is creating it right now)`; one lane, LANE-ORIGIN as designed. Lane removed.
- **T4 timeout tree kill** (burst2-b): `timeout -k 1 2 bash -c 'sleep 31337 & sleep 31337; wait'` → rc 124, 0 survivors.
- **T5 box.env is authoritative**: `PIPELINE_SLOTS=""` in the environment is overwritten by box.env (a lane cannot
  mask or widen its slot list); the cross-box test needed a private `PIPELINE_ROOT`.
- **T6 build-anywhere, forced cross-box** (05:18Z): lane coord-audit-t on burst2-b with its only (fake) slot held →
  `no free slot here; building on burst2-a (free: /srv/build-slot-2) at c1df1f08` → `peer-build: making
  peer-coord-audit-t from this box's warm base` (45 s) → `swarm-peer-coord-audit-t-2261437 cap=24G :: lake build
  Kernel.Job` → `Build completed successfully (3026 jobs)`, rc 0, 58 s wall, log
  `/srv/lanes/coord-audit-t/logs/peer-build-20261007T051853Z.log`. Peer lane, test lane and the shared ref removed.
- **T7 gate query**: from burst2-b `ssh burst2-a slots --free` → `/srv/build-slot-2`, through `box-peer-gate`.
- Not tested live (would move a base): advance/relay verify-before-publish; the code path is the same `mk-lane
  --verify` the old scripts ran, now before NOT-READY is cleared. The keeper runs the next advance with it.

## 3. What remains (owners)

1. **SATURATE**: D1–D5, A7; merge `lane/coord-audit` (on top of its 9031f1d9) so its `install` carries `slots --free`,
   `build-anywhere`, `peer-build`, the gate hunk, mk-lane/advance/relay, gate timeouts; its `slots --watch` timer should
   be in `burst-up`.
2. **MERGE-KEEPER**: next advance with the new `advance-base-burst.sh` (NOT-READY stays through verify); decide B6
   (`next` base per box or drop `--from next`); C5 if wanted.
3. **ROOT/Ember**: B8 (hbox/persvati mk-lane copies), the relay through the Mac vs a direct peer tar.
4. **Next quest (root, 05:40Z)**: `scripts/burst/burst-up` / `burst-down` — one reproducible entry point for a box
   (packages, user, swarm-build, slots from nproc/RAM, sccache, Lake cache, pipeline scripts, publisher, journey runner,
   shared remote + hbox mirror key, warm base at a tip, briefs), proven on a clean user/dir. Everything in §F and
   SATURATE's hand-applied state (box.env, sccache server, slots timer, peer keys) is its input list.

## 4. Second quest (root, 05:40Z): one reproducible entry point — `scripts/burst/` (branch `lane/coord-audit-2`)

What was applied by hand on burst2 (SATURATE's list + mine): packages (bc ripgrep bubblewrap bsdextrautils xxd jq
sqlite3 python3-nacl psmisc lsof), slot files 5/6 + small-1/2 (0644 on b), /srv/{sccache,lake-cache,git,pipeline/spk},
swarm.slice 160G, `~/.profile` box.env line, the box-env invocations, the SPK package copy, cargo primes, peer keys
crosswise + aliases, mirror key, hbox's puller key + `pull-burst2-remote` timer on hbox, TRANSIENT `pipeline-slots` and
`pipeline-sccache` units (gone at reboot), the publisher and journey runner in tmux, a seed TIPS line, /srv/SLOTS.txt,
and everything `bootstrap.sh`/`cold-build.sh`/`make-warm-base.sh`/`relay-b2.sh` did by hand-scp. All of it is now a
line in `scripts/burst/` (README there): `burst-up` (phases stage, root, user, keys, hbox, base, check; idempotent),
`remote/root.sh` (slots SIZED FROM nproc/RAM: lane slots = round(threads/5), two small, gate box keeps slot-1 + mk;
slice = 85 % RAM), `remote/user.sh` (persistent units from `units/`), `remote/check.sh` (ok/DIFF rows, exit = DIFF),
`burst-down` + `remote/collect.sh` (relay to hbox, counts verified, refuses below 10 % tank free, never deletes),
`burst-container` (a fresh Ubuntu in nspawn as the stand-in box), `swarm-build`, `hbox-pull.sh`.

**Check against the hand-built boxes (05:47Z, `burst-up --phase stage,check`)**: burst2-a 8 DIFF, burst2-b 11 DIFF —
`scripts:provenance` (no `.installed-from`), `unit:pipeline-sccache` and `unit:pipeline-slots` TRANSIENT (lost on
reboot), `unit:artifacts` / `unit:journeys` in tmux, `briefs` absent, on b `slot:build-slot-5/6` not 0666 and
`repo-tip` 4ef4e808 ≠ c1df1f08; everything else (56 rows each) ok. That is Ember's "would it survive a rebuild" answer
in rows: the five DIFF classes are exactly what a reboot or rebuild loses.

**Bugs the fresh box found in the entry point itself** (run 1, 05:54Z): a minbase image has no rsync (staging now
goes tar-over-ssh); `ssh HOST "cmd | tail -4"` made a missing root.sh read as "root phase ok" (every remote step now
logs to a local file and returns the command's status: `remote_step`); the key for the container's boot user was
word-split through two shells (base64 now). Three instances of the audited class, in the auditor's own script, caught
by running it against a box that had nothing.

**Proof on a fresh box (06:12–06:17Z)**: `burst-container ember@67.213.117.179 burst-test 2222 <pubkeys>` made a debootstrap
noble container (73 s) reached over ssh exactly like a rented box. `burst-up --id burst-test --tip c1df1f08 ... --boot
burst-test=burst-test-boot --no-data-disk --sccache-port 4227 --base-from local:ember@67.213.117.179`: root phase 64 s (slots
6×6 threads from 32 threads/187 G, slice 158 G), user phase 69 s (toolchains, repo at tip, 47 scripts with provenance, sccache,
REPL, 4 persistent units active, shared remote + timer, 127 briefs), base relayed on the host's disk and replayed **0 modules**
in 68 s, `burst-check` **0 DIFF** on 62 rows. Behaviour, same script on the fresh box vs hand-built burst2-b: mk-lane 24 vs 25 s,
slot.sh replay 2 vs 1 s, lane-check 136 vs 138 s, lean-ask first 145 vs 150 s then 0 s, build-anywhere 4 vs 4 s. A full second
run of every phase on the built box: 0 DIFF, nothing rebuilt (idempotent). `burst-down` collected 166 MB and relayed 46 files
to hbox:/tank/dregg-build/claude-lanes/bundles/burst-test-down (counts verified; tank 211 GB free, guard at 10 %). Faults the
runs found and fixed on the way: relay must carry the source's green log (the verify's positive control, else it refuses as
disarmed, correctly), a stale probe lane blocks the next verify, `check.sh` reused `n` (7 instead of 2 DIFF), `install-sccache`'s
transient unit collided with the persistent one, the base's mk-lane.sh must be refreshed with the scripts. Container removed.

**G1 · S1 · FIXED (ROOT 06:15Z) — the 24 G per-build cap killed closure builds.** A closure `lake build` at 6 threads died with
SIGTERM 143 at `Assurance.CommittedTerminalRealizer`; the user journal shows **16 OOM-killed swarm scopes on burst2-b and 1 on
burst2-a in six hours** (finished scopes peak ≤ 15.6 G; the killed ones never record a peak, so the cap looked fine). Default
now 48 G in swarm-build, lake-slot, lane-check, lean-ask --reload, mk-lane --verify; the gate's umbrella 64 G; the box-wide
slice (158–160 G) is the guard. Installed on both live boxes; deputies told; the hand `SWARM_MEM_MAX=48G` is withdrawn.

**Left for the live boxes**: switching the running transient `pipeline-sccache`/`pipeline-slots` scopes and the tmux publisher and
journey runner to the persistent units is `burst-up --phase user` on each box; SATURATE cleared it between publications (no
`/srv/artifacts/.work/*.lock` held, last runner.log line DONE on b, publisher env MINI_CANDIDATE_CARGO_JOBS=12
PIPELINE_PUBLISH_MEM_MAX=32G). Not done in this session: it restarts the sccache server lanes are compiling through.

**B9 · S1 · INCIDENT (mine) · FIXED — 06:41Z, the keeper's live advance.** My 05:33Z refresh of the keeper's `mk-tools` used
`cp -n` for `mk-lane.sh`, so the stale 4ef4e808 copy (no `MK_LANE_PROBE`) survived; the new `advance-base-burst.sh` installed
`"$here/mk-lane.sh"` = that copy into the base, the probe was refused ("base not ready"), the base sat NOT-READY "verify
FAILED" and every lane on burst2-a was blocked ~5 min. The keeper repaired it by hand (both bases FROZEN at main 10e4f3ab).
Two lessons the audit itself had named: a swap of live tool copies without the owner's go (the keeper had asked), and "one
copy" enforced by convention, not by the script. Fix (coord-audit-2, second commit): advance installs the GATED TREE's
`scripts/pipeline/mk-lane.sh`, relay the copy that travelled with the tree, make-warm-base `/srv/mini`'s, burst-up the base
tree's own — and each REFUSES (exit 9) before touching the base when that file is missing or lacks `MK_LANE_PROBE`;
`burst-check` gains `mk-lane:probe-aware` and compares the base's copy against its tree's.
