# BURST5-UP LOG (continuation file for BURST5-UP)
2026-10-17T01:42:37Z created server sv_zrPm0dBJ65KOw (label 255S055720) burst5-a DAL f4-metal-medium hourly $1.52/h, 207.188.6.69 / 2605:6440:5002:20a::2; tag burst5-20261016 = tag_xG6mROjVd9TX4YB2olzAHVgBJAo. payload: latitude-burst5-20261016/create-payload.json. US in stock: DAL, MIA2. ssh conf ~/.ssh/burst5-20261016.conf.
2026-10-17T01:49:08Z phases stage,root,user OK (root: 6 lane x 6 threads, slice 158G; user 01:48:13Z). deploy key: box ~/.ssh/minidregg-deploy (Host github.com in ~/.ssh/config), GitHub key id 166720422 'burst5 minidregg deploy (write) 2026-10-16'. shared remote /srv/git/minidregg.git remote github added.
2026-10-17T01:50:53Z hbox phase OK (puller burst5_pull, timer pull-burst5-remote 10 min; logged in hbox box-changes.md). seed: git push RUN ON hbox from burst3 mirror -> box /srv/git/seed.git (32 s) -> fetch: 519 lane/* + old/next-20261003; main cfb68bf9 / next 2c27b08b equal to GitHub; tips identical (md5 of ref lists); lane/cycle-fix c38b994a fetched from GitHub (not in hbox mirror); seed.git removed.
2026-10-17T01:57:58Z lane/cycle-fix (base 2c27b08b) REBASED onto main cfb68bf9 on the box (/srv/scratch/cf-rebase): conflicts check.sh (kept main's peer-gate row + cycle-fix lake-cache row), box-env (kept main's --srv; --lake-cache default: flag > $srvdir/lake-cache > $PIPELINE_ROOT/lake-cache), with-lean-slot add/add (took cycle-fix's FIFO+waits.tsv; kept main's nice knob as PIPELINE_LEAN_SLOT_NICE; user.sh comment renamed WITH_LEAN_SLOT_* -> PIPELINE_LEAN_SLOT*; persvati's --set must rename). build-native-host auto-merged (main's cc-object.sh object cache + seated lake build). Pushed lane/cycle-fix-cfb68bf9 = 44637105 (shared remote + GitHub). lane/cycle-fix itself untouched.
2026-10-17T02:02Z cycle-fix checks (box, on lane/cycle-fix-cfb68bf9 44637105): test_lake_cache_audit 4 OK; check-unit-tests.sh PASS (32 modules); native-build-locks.py 3 PASS (16 jobs / 3 seats, refusal 75, TERM holds seat).
  FINDING test-with-lean-slot.sh: FAIL "grant order: h2 p h1 w1 w2 w3 w4 w5" -- 3/3 runs, IDENTICAL on the un-rebased c38b994a (so not the rebase).
  Mechanism (read from scripts/pipeline/with-lean-slot): the grant test `if [ "$(oldest_live)" = "$$" ]` admits only THE single oldest live
  ticket per poll; h1 and h2 enqueue in the same second (touch -d "@$enq", 1-s mtime), so one of them is not "oldest", finds no slot to try,
  and `sleep 15` -- with a free slot. By its next poll the PRIORITY ticket p (backdated a day) is oldest, so p passes h1. On a box: every
  waiter after the first behind a freshly freed batch of slots idles up to 15 s, and same-second tickets tie-break by `ls -tr` name order.
  Not patched.
2026-10-17T02:06:02Z fnbin: rsync RUN ON hbox (temp key burst5-seed-tmp, rrsync -wo /srv/seed, restrict) -> /srv/fnbin/6679dae0e, 26 s; tree hash ea34e2ed equal both sides. warm tree: hbox warm-cfb68bf9/src -> box /srv/seed/warm-cfb68bf9-src (rsync -aH -z on hbox nice 15, 732 s, 12G); HEAD cfb68bf9 clean. temp key revoked on box + deleted on hbox (logged in hbox box-changes.md). base: relay-base.sh TIP local local /srv/seed/warm-cfb68bf9-src (pid file /srv/seed/relay.pid, log /srv/seed/relay.log) -> verify probe.
2026-10-17T02:12Z base: first relay verify REFUSED (0 compiled; umbrella red on known-red NativeAcceptedFixture cv 01a146dd). ROOT ruling -> lane/burst5-base-known-red f4a6ab6d (scripts/pipeline/known-red-modules + mk-lane --verify: failed set must EQUAL the list). Bugs found by testing it: set -e killed the verify at `vrc=$?` (fixed: `&& vrc=0 || vrc=$?`), pipefail on absent list / no importers (|| true). Real verify rc 0, 27 s, 0 compiled, carries NativeAcceptedFixture (importer Assurance). Mutations refuse rc 65: empty list, no file, extra listed Kernel.World. Positive control: hbox integrator-next ub-979d639c.out (6 Built lines) copied by one-shot temp key burst5-seed-tmp2 (deleted). Base PUBLISHED. Told INTEGRATOR-5 (batch 3).
2026-10-17T02:22Z slot fix: lane/cycle-fix-cfb68bf9 3fcc7f46 (queue.lock; take iff ahead < free; poll 1 s). test PASS 3/3 (h2 h1 w1 p w2 w3 w4 w5); old wrapper FAIL (h1 idle >3 s); no-FIFO mutation FAIL (p last). Installed: /srv/pipeline/scripts <- 3fcc7f46 (prev scripts.cfb68bf9). box.env from that tree's box-env (lake cache /srv/lake-cache always on; seats 4, lean slots 6x4, native jobs 16). perf_event_paranoid -> 1 (box-changes.md).
2026-10-17T02:25:29Z §1.2 attempt 1: comment line APPENDED at END of Kernel/World.lean -> lane A built 1 module in 6.4 s (Replayed 105): an end-of-file comment leaves World.olean's dependents' inputs unchanged, so no cascade; the probe must shift positions. attempt 2: comment at line 1.
2026-10-17T02:53Z §1 SHARED CACHE (lanes cf-a, cf-b from the warm base, both at a8b8df55 = lane/cycle-fix-cfb68bf9 3fcc7f46 + a line-1 comment in Kernel/World.lean; box.env LAKE_ARTIFACT_CACHE=true LAKE_CACHE_DIR=/srv/lake-cache; lake-slot Host.Main +Host.Main:leanArts):
  A: rc 0, wall 806.8 s, 444 "] Built", 48 Replayed; Kernel/World.olean link count 2.
  B: rc 0, wall 2.0 s, 0 "] Built", 444 "Fetched"; Kernel/World.olean link count 3.   (before: hbox lanes re-compiled e.g. 823 modules in 8,046 s)
  lake-cache-audit --cache: 1767 entries checked, 0 bad; --scan-tree B: 0 lines. unit test 4 OK; check-unit-tests PASS 32.
2026-10-17T02:47:41Z FINDING (burst recipe): lane-build rust runs cargo --offline --locked, and user.sh never fetches the cargo deps: on a fresh box the rust step fails 'can't checkout from https://github.com/emberian/dregg.git: offline mode' (sandstorm-package via native/spk-host). Fixed on the box by one 'cargo fetch --locked' from the lane tree (142 s; ~/.cargo registry 315M + git 1.2G). Recipe gap, not patched in the repo.
2026-10-17T02:55Z §2.2-2.3 WARM CANDIDATE, NEW builder (lane cf-new = 3fcc7f46, MINIDREGG_LEAN_SEATS=4 THREADS=4):
  host: rc 0, step wall 95.4 s, manifest elapsed_seconds=92; "lean-closure 784 modules PASS 1s"; compiled_source_modules=0; max_concurrent_real_lean=1 (nothing to compile); lean_maxrss p95/max 0 (no compiles).
        (before: loop 634-661 s, host step 1,040-1,108 s elapsed)
  host binary_sha256=6e6b9c3105afab462050cdf36b439f2381cc5da18f5bd116b3296ac27dc2c712 == hbox integrator-next cand-979d639c-host (old builder, same Lean tree) 
  consent: rc 0, 34.6 s (elapsed 32), lean-closure 12 modules PASS 1s, binary_sha256=9043118f... == hbox cand-979d639c-consent; companion-recheck 3205 OK, 0 non-OK.
  rust: rc 0, 120.8 s (after the cargo fetch); pack: rc 0, 3.9 s, "compiled inputs identical at 3fcc7f461cd3" for host and rust roles.
2026-10-17T03:15Z §2.4 IDENTITY (same sha 3fcc7f46 tree; cf-old = + cfb68bf9's scripts/build-native-host.sh, which refuses MINIDREGG_NATIVE_JOBS/LEAN_THREADS other than 1|2 -> run at 2/2):
  OLD builder: host step 831.3 s (elapsed_seconds=828, ordered loop), consent 42.3 s.  NEW: host 95.4 s (92), consent 34.6 s.
  reusable-artifact-sha256.txt: native-out 11,947 vs 11,947 lines, diff 0; consent-out 11,423 vs 11,423, diff 0.
  binary_sha256 host 6e6b9c31... == ; consent 9043118f... ==  (and both == hbox's cand-979d639c, old builder, other box).
2026-10-17T03:33Z §2.5 EDIT CASE, cache OFF (lane cf-edit = a8b8df55, LAKE_ARTIFACT_CACHE=false, seats 4 x threads 4): host step 880.2 s, elapsed 877;
  compiled_source_modules=444; "lean-closure 784 modules PASS 789s"; max_concurrent_real_lean=4 (= seats); wrapper_invocations=445.
  sum of per-module compile walls (lean-module-rss.tsv) 1,660 s -> 789 s closure wall = 2.1x at 4 seats (state-at's loop: 4,423 s for its set).
§3.1 RSS (first per-module numbers, 444 compiled modules): lean_maxrss p50 4.03 GB, p90 4.20 GB, p95 4.24 GB, p99 13.5 GB, max 19.36 GB.
  >8 GB: 10 modules, >12 GB: 6, >16 GB: 5 (Kernel.PayEnrolReceiver 19.36 GB/98 s, PayObservationReceiver 19.33/60 s, PayEnrolV2Receiver 19.17/92 s,
  PayCellDomain 18.93/56 s, Compiler.CredentialAuthorityDomainReceiver 16.41/47 s).
  FINDING (sizing rule): seats = floor(MemoryMax / p95) = floor(48G / 4.24G) = 11, threads = 32/11 = 2. The p95 hides the tail: three of the five
  >16 GB modules seated together exceed the 48G swarm-build cap (even 4 seats can: 4 x 19.4 = 77G). Box left at 4 x 4 (it compiled all 444 at max
  concurrency 4 without an OOM); not resized to 11 x 2. Needs a memory-weighted seat (or a heavy-module class), ROOT's call.
2026-10-17T03:38Z §2.6 UMBRELLA mode (cf-new, lane-build.sh host --umbrella --umbrella-target Host.Main): rc 0, 91 s (elapsed 88), compiled 0, max_concurrent_real_lean=1 (<= 4), wrapper_invocations=2, binary_sha256 6e6b9c31... (same).
§3.3 test-with-lean-slot.sh PASS 3/3 (after the 3fcc7f46 fix). §3.4 real build through the repo wrapper (cf-b, with-lean-slot swarm-build lake build Host.Main): rc 0, 1 s; waits.tsv: enq=granted (0 s wait), slot 1, rc 0. /srv/pipeline/slots/with-lean-slot -> ../scripts/with-lean-slot = the 3fcc7f46 repo copy; BURST5-BOX.txt brief names the lane-tree path.
INTEGRATOR-5 note (03:0xZ): batch 2 (lane/integrator-batch2 df29f625) moves the fixture to Fixtures.NativeAcceptedFixture (lean_lib Fixtures) and mk-lane --verify to `lake build $(bash scripts/pipeline/umbrella-targets)`; it will rename the known-red row when merging f4a6ab6d. burst5's base mk-lane.sh is the f4a6ab6d copy: refresh it when the base advances past batch 2/3.
2026-10-17T04:10Z ROOT rulings (after verification accepted): (1) memory-weighted seats, (2) user.sh cargo fetch, (3) handoff.
  cold RSS measurement (lane cf-cold = 3fcc7f46, no .lake/build, cache off): 784 compiled, lean-closure 933 s at 4 seats, elapsed 1033 s,
    binary_sha256 6e6b9c31 (same bytes cold as warm); p95 4.21 GB, max 19.36 GB; 5 modules > 16 GB (same five), DurableIndex 13.56 GB.
  lane/cycle-fix-cfb68bf9 5e29e086 build-native-host!: memory-weighted seats (cap = MINIDREGG_LEAN_MEM_CAP | tightest cgroup memory.max |
    SWARM_MEM_MAX | 48G; seat = cap/seats; weight = ceil(maxrss/seat) from committed scripts/pipeline/lean-module-rss.tsv (784 modules) +
    MINIDREGG_LEAN_RSS_FROM; unrecorded = all seats; over-cap refuses by name; all-or-nothing FIFO acquisition under a mkdir lock; SEATS log line;
    held-weight bound). native-build-locks.py 7 PASS; mutation (all weights 1) FAILS the heavy test.
  lane/cycle-fix-cfb68bf9 0b3de7f1 burst: user.sh cargo fetch --locked once (no-root: probe + NO-ROOT.txt); check.sh cargo-deps row (ok; DIFF with ~/.cargo/git moved aside).
  REAL edit build, weighted, 48G scope cap (cf-mw = 0b3de7f1 + World line-1 comment, cache off): rc 0, 917 s step, lean-closure 827 s (count-based: 789 s),
    444 compiled, cap detected 50331648 KiB from the scope's memory.max, seat 12 GiB, heavies weight 2, unrecorded 0, max held weight 4, max heavies
    together 1 (the DAG never offered two), max concurrent recorded RSS sum 34.8 GiB, sampled scope peak 24.4 GB, binary 6e6b9c31 (same).
  REAL over-cap refusal (MINIDREGG_LEAN_MEM_CAP=16G): rc 64 before Lake, names PayCellDomain/PayEnrolReceiver/PayEnrolV2Receiver/PayObservationReceiver
    (CredentialAuthorityDomainReceiver 16.43 GB < 16 GiB cap: correctly not named).
  REAL 24G-cap OOM test (cf-mw24, same commit, SWARM_MEM_MAX=24G -> scope memory.max 24 GiB detected; seat 6 GiB; the five heavies weight 4 = ALL
    seats, CredentialAuthorityDomainReceiver 3): rc 0, NO OOM, lean-closure 1025 s, 444 compiled, max held weight 4, max heavies together 1,
    max concurrent recorded RSS sum 19.4 GiB (= one heavy ALONE: each heavy ran with nothing else), binary 6e6b9c31 (same).
  Pushed lane/cycle-fix-cfb68bf9 = 0b3de7f1 (GitHub + shared remote); installed on burst5 /srv/pipeline/scripts.

## HANDOFF (BURST5-UP, 2026-10-17T04:35Z) -- box handed to INTEGRATOR-5 as box A; BURST5-UP stops here
Box:   burst5-a = Latitude sv_zrPm0dBJ65KOw, DAL, f4-metal-medium hourly $1.52/h since 2026-10-17T01:42:51Z, 207.188.6.69,
       tag burst5-20261016 (tag_xG6mROjVd9TX4YB2olzAHVgBJAo). ssh -F ~/.ssh/burst5-20261016.conf burst5-a. Facts: latitude-burst5-20261016/README.txt.
State: warm base /srv/warm-base cfb68bf9 READY (known-red rule, mk-lane.sh = lane/burst5-base-known-red f4a6ab6d copy; known-red-modules
       UNTRACKED in the base tree). /srv/pipeline/scripts + candidate = lane/cycle-fix-cfb68bf9 0b3de7f1 (prev scripts.cfb68bf9).
       box.env: lake cache /srv/lake-cache always on, MINIDREGG_LEAN_SEATS=4 (memory-weighted from 0b3de7f1) THREADS=4, NATIVE_JOBS=16,
       PIPELINE_LEAN_SLOTS=6x4, PIPELINE_LANES=/srv/lanes, PIPELINE_SHARED_GIT, fn paths. perf_event_paranoid=1. ~/.cargo deps fetched.
       Units active: pipeline-sccache, pipeline-slots, pipeline-artifacts, shared-remote-sync.timer. Every box change: burst5-a ~/box-changes.md.
       /srv 87G used of 1.8T. Already in use by other lanes (census-2*): not mine, untouched.
Mine on the box (throwaway, delete freely): /srv/lanes/cf-{a,b,new,old,edit,cold,mw,mw24}, /srv/seed (12G seeded copy + logs), /srv/scratch.
Branches pushed (GitHub + shared remote): lane/cycle-fix-cfb68bf9 0b3de7f1 (batch 3), lane/burst5-base-known-red f4a6ab6d (batch 3);
       INTEGRATOR-5 told for both (fixture rename to Fixtures.* in batch 2: rename the known-red row; RSS table has no Fixtures rows -> serialized until measured).
Open findings (not patched): none left from this lane beyond the above; the plan's §0 `--layout /srv/pipeline` is wrong for the burst layout (used no --layout).
TEARDOWN LIST (complete):
  1. scripts/burst/burst-down --id burst5 burst5-a (read it first) -- collect to hbox.
  2. Delete server: curl -X DELETE -H "Authorization: Bearer $(cat ~/.latitude-key)" https://api.latitude.sh/servers/sv_zrPm0dBJ65KOw
     (tag tag_xG6mROjVd9TX4YB2olzAHVgBJAo may be deleted after).
  3. GitHub deploy key: gh api -X DELETE repos/emberian/minidregg/keys/166720422  ("burst5 minidregg deploy (write) 2026-10-16").
  4. hbox puller: systemctl --user disable --now pull-burst5-remote.timer; rm ~/.config/systemd/user/pull-burst5-remote.{service,timer}
     ~/.local/bin/pull-burst5-remote ~/.ssh/burst5_pull{,.pub}; systemctl --user daemon-reload. KEEP the mirror
     /tank/dregg-build/claude-lanes/bundles/burst5-minidregg.git (526 refs at 04:35Z). Log the undo in hbox box-changes.md.
  5. hbox scratch (ours): /tank/dregg-build/claude-lanes/burst5-seed. Temp keys burst5-seed-tmp{,2}: already deleted/revoked.
  6. Mac: ~/.ssh/burst5-20261016.conf, ~/.ssh/known_hosts.burst5, ~/.ssh/cm-burst5-* sockets; scratch worktree <scratchpad>/burst5-src
     (git -C ~/dev/minidregg worktree remove).
  7. OPS-2 live harness on burst5-a (ROOT ruling 2026-10-17; added BEFORE running):
     - mechanism, the one root write: `sudo install -D -o root -g root -m 0755 /usr/bin/bwrap /usr/local/libexec/nd-bwrap`
       undo: `sudo rm /usr/local/libexec/nd-bwrap` (and `sudo rmdir /usr/local/libexec` if empty and created by it).
     - unit links (systemctl --user link): ~/.config/systemd/user/nd-ops-live-{serve,serve2,follow,fsize}.service
       undo: `for u in serve serve2 follow fsize; do systemctl --user stop nd-ops-live-$u; systemctl --user disable nd-ops-live-$u; rm -f ~/.config/systemd/user/nd-ops-live-$u.service; done; systemctl --user daemon-reload`
     - data: /srv/scratch/ops2-live (OPS-2's; harness Stores, units, report).
     - DONE 2026-10-17 10:38Z (burst5 clock, UTC) by OPS-2 on ROOT's word: the four units stopped and disabled, their four
       links removed (only links pointing into /srv/scratch/ops2-live), daemon-reload; /usr/local/libexec/nd-bwrap removed and the
       empty /usr/local/libexec it created removed. Verified: no nd-ops link left, /usr/local/libexec absent. KEPT: the data at
       /srv/scratch/ops2-live (run1–run4 Stores and reports; deleted with the box). A later run asks ROOT first; the install is one command.

## BOX CHANGES by INTEGRATOR-5 (2026-10-17)
- /srv/pipeline/box.env: MINIDREGG_NATIVE_JOBS, MINIDREGG_LEAN_SEATS, MINIDREGG_LEAN_THREADS made overridable (${VAR:-16}/${VAR:-4}/${VAR:-4}) so pre-cycle-fix trees (builder: NATIVE_JOBS/LEAN_THREADS must be 1 or 2) publish with =2. Undo: cp /srv/lanes/integrator5/runs/box.env.before-i5 /srv/pipeline/box.env (then re-add the two lines below if wanted).
- /srv/pipeline/box.env += ARTIFACT_ROOT=/srv/artifacts, JOURNEY_ROOT=/srv/journeys (pipeline-journeys unit sources box.env only; died "JOURNEY_ROOT: unbound variable"). Undo: delete the lines.
- journey units installed (install-journey-units from /srv/warm-base/src; timer every 5 min).
- /srv/pipeline/absent-inputs.tsv: hostupgrade declared absent (old candidate e0a8ba21 is on hbox only). cv 01a14a21-768e-7361-ab97-cf3fdd248de7: copy /tank/dregg-build/pipeline/artifacts/e0a8ba21* -> /srv/artifacts/ and remove the line; install uidmap (/usr/bin/newuidmap) for m6grain.
- All of the above also in burst5 ~/box-changes.md.

## 8. OPS-3 keybroker harness on burst5-a — PLANNED, NOT RUN (recorded before running; waits for ROOT + INTEGRATOR-6's window)
- mechanism, the one root write: `sudo install -D -o root -g root -m 0755 /usr/bin/bwrap /usr/local/libexec/nd-bwrap`
  undo: `sudo rm /usr/local/libexec/nd-bwrap && sudo rmdir /usr/local/libexec` (rmdir only if it creates it; it is absent now, checked 2026-10-18).
- unit links (systemctl --user link): ~/.config/systemd/user/{nd-ops-live-keybroker,nd-ops-live-hfollow@,nd-ops-live-grain@}.service
  (ROOT's yes covers the follower and grain-launch units with the same undo shape)
  undo: `for u in nd-ops-live-keybroker nd-ops-live-hfollow@w nd-ops-live-hfollow@x nd-ops-live-grain@w nd-ops-live-grain@x; do systemctl --user stop $u; systemctl --user reset-failed $u; done; rm -f ~/.config/systemd/user/nd-ops-live-keybroker.service ~/.config/systemd/user/nd-ops-live-hfollow@.service ~/.config/systemd/user/nd-ops-live-grain@.service; systemctl --user daemon-reload`
- data: /srv/scratch/ops3-live (src bundle scp'd from hbox logs/ops3-src, ~21 MB; run dirs run1..). Goes with the box.
- §8 RUN: nd-bwrap installed 2026-10-17T18:04:47Z by OPS-3 (window opened by INTEGRATOR-6, main 334316df).
- §8 UNDO DONE 2026-10-17T18:07:40Z (burst5 clock) by OPS-3: the five unit instances stopped + reset-failed, the three links
  removed, daemon-reload; /usr/local/libexec/nd-bwrap removed and /usr/local/libexec (created by the install) removed.
  Verified: 0 nd-ops links, 0 nd-ops units, /usr/local/libexec absent. KEPT: /srv/scratch/ops3-live (src bundle, run1, run2,
  reports; goes with the box). Runs: run1 FAIL 2 (keybroker's RestrictAddressFamilies lacked AF_NETLINK), run2 ALL PASS.

## TEARDOWN DONE 2026-10-18T04:35:02Z (INTEGRATOR-7, on Ember's word via ROOT)
1. Idle check 03:39:48Z: standing units only (pipeline-artifacts/sccache/slots, timers shared-remote-sync + pipeline-journeys); no gate/lane pid alive.
   One orphan: INTEGRATOR-5 seats-try `mini serve` pid 2034732 (+ children 2034734, 2034743). On ROOT's (a): stopped by its PID file
   /srv/lanes/integrator5/runs/seats-try/s/w/public/server.pid (kill rc 0); all three exited.
2. Collect: `BURST_SSH_OPTS="-F ~/.ssh/burst5-20261016.conf" scripts/burst/burst-down --id burst5 burst5-a` (minidregg checkout dcab86da's collector),
   rc 0, fail=0, 04:33:20Z: 24G box-side (/srv/burst/down-20261018T034055Z) -> hbox /tank/dregg-build/claude-lanes/bundles/burst5/burst5-a (13G on disk),
   226,319 files, counts match. Re-checked per dir (files / apparent bytes, identical both sides): artifacts 682 / 7,112,829,371 (8 sets);
   box 113,166 / 12,414,254,478; journeys 112,215 / 3,397,410,088; lanes 255 / 1,810,239,583 (21 lanes); shared-remote.bundle sha256 71f50bee...
   equal, `git bundle verify` OK against the burst5 mirror, main 334316df. Separately (collect.sh does not take /srv/scratch): ops3-live (84 files,
   246,529,357 B) + ops2-live (147 files, 91,113,065 B) tar|zstd -> bundles/burst5/burst5-a-scratch, counts + bytes equal (9 unix sockets skipped).
   Tank after: 336G free (81%).
   FINDING (not patched): scripts/burst/remote/collect.sh rsyncs $SRV/burst/ into $OUT/box/burst/ while $OUT is under /srv/burst, so the collection
   copies its own partial output (the 12G box/ is mostly that duplicate). Fix: exclude /down-* there, or put OUT outside /srv/burst.
3. Server delete: Latitude DELETE /servers/sv_zrPm0dBJ65KOw -> HTTP 204 at 2026-10-18T04:33:54Z; GET -> 404.
   COST WINDOW: 2026-10-17T01:42:51Z -> 2026-10-18T04:33:54Z = 26.85 h x $1.52/h = ~$40.81 ($41.04 if billed per whole hour, 27 h).
   Tag tag_xG6mROjVd9TX4YB2olzAHVgBJAo NOT deleted (list: "may be deleted after", no command) -- for Ember.
4. GitHub deploy key 166720422 deleted (gh api -X DELETE; GET -> 404).
5. hbox puller: pull-burst5-remote.timer disabled --now; removed ~/.config/systemd/user/pull-burst5-remote.{service,timer}, ~/.local/bin/pull-burst5-remote,
   ~/.ssh/burst5_pull{,.pub}; daemon-reload; 0 burst5 units left. KEPT mirror bundles/burst5-minidregg.git (535 refs). Undo logged in hbox
   /tank/dregg-build/pipeline/box-changes.md (04:34:22Z).
6. hbox scratch /tank/dregg-build/claude-lanes/burst5-seed: NOT removed (no listed command) -- for Ember.
7. Mac: ssh control master closed (-O exit); removed ~/.ssh/burst5-20261016.conf, ~/.ssh/known_hosts.burst5 (no cm-burst5-* sockets left);
   scratch worktree .../b3795e84-.../scratchpad/burst5-src existed, clean, removed by `git -C ~/dev/minidregg worktree remove` (no --force).
