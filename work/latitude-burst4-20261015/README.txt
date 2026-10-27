burst4 (2026-10-15), project dregg (proj_jmlR57Ro4NWgY), team Lunar Town
host:      burst4-a   (ssh alias in ~/.ssh/burst4-20261015.conf: `ssh -F ~/.ssh/burst4-20261015.conf burst4-a` = ember@207.188.7.163;
           the conf also carries hbox, because -F replaces ~/.ssh/config for burst-up's ssh calls)
server id: sv_R82A0y4Rga6mM (label 254S012948)
plan:      f4-metal-medium (EPYC 4564P Zen5, 16c/32 threads, 187G RAM, 2x480G + 2x1.9T NVMe), hourly
site:      DAL (US in stock 10-15: DAL/CHI/MIA2; LON2 not needed)
IP:        207.188.7.163 (v6 2605:6440:5002:205::2)
cost:      $1.52/h (~$36.50/day) from ~2026-10-15T03:27Z
tag:       burst4-20261015 = tag_wpQbrjg1p2Tnz66BdgbvcVleYwQZ ("burst4: second build box for the HP ranges; review 2026-10-18")
ssh key:   ssh_dmkONWq9oajL1 (Mac id_ed25519)
state:     burst-up --id burst4 from /tmp/burst4-src (worktree of mini-unified-push-20261003 at origin/next a5483db3), tip
           a5483db36cf7aaf34378a15c90b68c2de538f16a. Warm base FROZEN a5483db3 by a COLD build on the box (1017 s, 1318 lines,
           verified replay): no hbox tree at a5483db3 existed to relay (integrator-next is c3b667b4, land-7ffd6524 older).
           burst-check 0 DIFF (after staging --briefs; see below).
slots:     root.sh pipeline slots: 6 lane x 6 threads, 2 small, 2 gate (/srv/build-slot-*; box.env), slice cap 158G.
           with-lean-slot: /srv/pipeline/slots/with-lean-slot, FIFO (adapted from hbox's 10-14 23:04 copy), 6 slots x THREADS=4,
           tickets /srv/pipeline/slots/waiters/<pid>.pid. NOTE: these are two slot systems on one box; a lane uses one or the other.
box.env:   regenerated with box-env --shared-git /srv/git/minidregg.git --set MINI_FN_LAUNCHER/MINI_FN_CORE (fnbin below).
           user.sh has no pass-through for these: re-running the user phase drops them (re-run the box-env line in BURST4-UP-LOG).
shared remote: /srv/git/minidregg.git: main/next/green from GitHub (main 7ffd6524, next a5483db3, green cfdaf64d) + 509 refs/heads/lane/*
           + old/next-20261003, seeded from hbox /tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git by a git push RUN ON
           hbox into a hook-less /srv/git/seed.git (puller key; box-peer-gate admits receive-pack under /srv/git), then fetched
           locally into minidregg.git; tips identical; seed.git removed. Nothing relayed through the Mac.
fnbin:     /srv/fnbin/6679dae0e/fn-6679dae0e (fn-host, fn-host.core, developer variants), rsync RUN ON hbox from
           /tank/dregg-build/pipeline/inputs/fnbin/ over a temporary key (burst4-fnbin-tmp@hbox, command="rrsync -wo /srv/fnbin",
           restrict); tree hash equal on both sides (5f7297e1); the temp key is REVOKED on the box and DELETED on hbox.
           4b22a49bc is not on hbox, not copied. fn-host runs on the box's glibc 2.39 (help path).
hbox puller (bounded operational key, Ember 10-07): hbox ~/.ssh/burst4_pull (burst4-pull@hbox), authorized on burst4-a as
           box-peer-gate (git fetch / read-only rsync / lane pushes under /srv/git). Timer pull-burst4-remote.timer (10 min) ->
           /tank/dregg-build/claude-lanes/bundles/burst4-minidregg.git (513 refs at 03:53Z). REMOVE at teardown: the timer + service +
           ~/.local/bin/pull-burst4-remote + ~/.ssh/burst4_pull{,.pub} on hbox.
smoke:     landing.sh --check a5483db3 (PIPELINE_ROOT=/srv/pipeline; logs/landing-check-a5483db3.log on the box): rc=12,
           "no finished standing run at /srv/journeys/a5483db3" -- the plumbing resolves; no gate/publish/journey run exists yet.
briefs:    /srv/briefs = SAFETY-BLOCK.txt + BURST4-BOX.txt (source: this dir's briefs/).
script findings (not fixed): (1) stage as the login user fails after a boot-user stage (/tmp/burst-up owned by ubuntu): re-stage
           with --boot. (2) check DIFFs `briefs` unless --briefs is passed. (3) user.sh cannot carry extra box.env exports (--set).
log:       /Users/ember/dev/redregg/work/BURST4-UP-LOG.md; burst-up logs ~/.cache/burst-up/burst4/ and this dir's burstup-*.log.
teardown:  scripts/burst/burst-down (read it first); delete server sv_R82A0y4Rga6mM; remove the hbox puller pieces above.

persvati (third host, laptop: keep <= half the cores) -- added 2026-10-15T04:07Z, STOPPED at the disk guard
how:       burst-up from lane/burst-noroot-host 9066a518 (worktree /tmp/burst4-src; pushed to burst4's shared remote + GitHub):
           BURST_SSH_OPTS="-F ~/.ssh/burst4-20261015.conf" scripts/burst/burst-up --id burst4 --tip a5483db36cf7aaf34378a15c90b68c2de538f16a \
             --gate burst4-a --srv /home/ember/mini-pipeline --no-root --thread-budget 12 --threads-per-slot 4 --slice-pct 50 \
             --briefs <this dir>/briefs-persvati --set "SWARM_NICE=15 SWARM_MEM_MAX=20G WITH_LEAN_SLOT_N=3 WITH_LEAN_SLOT_THREADS=4 WITH_LEAN_SLOT_NICE=15" \
             --phase stage,root,user,keys,base,check persvati
           (the root phase here is root.sh --no-root, run AS ember: no sudo was used anywhere on persvati)
layout:    /home/ember/mini-pipeline (box.env; `. ~/mini-pipeline/activate`; ~/.profile and ~/.bashrc NOT touched; global git
           config NOT touched: user.email ember@elide.dev, commit.gpgsign true -> lanes commit with -c commit.gpgsign=false)
slots:     3 lane slots x 4 threads (thread budget 12 of 24) + 2 small; with-lean-slot = ~/mini-pipeline/pipeline/slots/with-lean-slot
           -> ../scripts/with-lean-slot (repo copy), 3 x THREADS=4, build nice 15. swarm-build in ~/mini-pipeline/pipeline/bin,
           SWARM_NICE=15, per build 20G, user swarm.slice MemoryMax=41G (50% of 83G; memory controller is delegated to the user
           slice, so the cap is enforced without root). Units pipeline-sccache/pipeline-slots: Nice=15 + idle IO drop-ins;
           sccache cache capped at 30G.
remote:    lanes push to burst4's shared remote (git push burst4-gate:/srv/git/minidregg.git HEAD:refs/heads/lane/<name>), which hbox
           mirrors; no shared remote and no hbox puller on persvati.
keys:      persvati ~/.ssh/box_peer (box-peer@persvati) authorized on burst4-a as box-peer-gate; Host burst4-gate appended to
           persvati ~/.ssh/config. REMOVE at teardown (the authorized_keys line on the box dies with it; the Host block and
           ~/.ssh/box_peer{,.pub} on persvati are ours to remove).
NOT installed for lack of root (~/mini-pipeline/burst/NO-ROOT.txt): pkg python3-venv (ensurepip), python3-nacl, pkg-config, sqlite3,
           age. None is a lane-build input (pkg-config only optional for aws-lc-sys); nacl/sqlite3 are journey inputs -> no journeys
           on persvati. capnp 1.5.0 WAS built user-local (system has 1.1.0). earlyoom active, linger yes.
base:      pulled from burst4 by rsync over the peer key, run ON persvati (190 s, full copy incl. .lake/packages; nothing via the Mac).
           HEAD/clean checks passed on the copy. The verify probe REFUSED: mk-lane "disk: lanes would drop below 15% free".
           persvati / was 245G free of 1.9T (12.9%) before anything was written; now 234G (12.3%); ~/mini-pipeline = 12G (all ours).
check:     1 DIFF (warm-base NOT-READY: the disk refusal), 1 ABSENT (pkg:sqlite3, declared). Every other row ok, incl. slots-sized
           3 x 4 for 12, swarm.slice 41G declared, profile:untouched, peer-gate:slots. Small build: NOT RUN (no lane can be cut).
open:      cv task 01a13dc4 (Ember): free space on persvati and re-run `--phase base,check persvati`, or remove ~/mini-pipeline.
