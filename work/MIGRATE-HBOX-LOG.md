# MIGRATE-HBOX-LOG — nanodregg's main moves to hbox (2026-10-17)

Owner: MIGRATE-HBOX (subagent of ROOT). Order: hbox is where nanodregg is BUILT, GATED and RUN; main
lives on hbox; GitHub (emberian/nanodregg) is the mirror; the Mac is a pull-only reader.

## 1. hbox prerequisites (verified 2026-10-17 ~00:05Z, `ssh hbox`, user hbox, 24 cores)
- elan: ~/.elan/bin; toolchains v4.17.0, **v4.30.0** (lean-toolchain pin; `lean --version` = 4.30.0 d024af09), v4.34.1. Nothing installed.
- cargo 1.100.0-nightly (2026-08-22), clippy 0.1.100, rustfmt 1.10.0-nightly; default `nightly-x86_64-unknown-linux-gnu`.
  client/ and sandbox/ carry no rust-toolchain file; the Mac runs cargo 1.98.0-nightly (2026-06-20). Newer clippy may add lints: a
  first clippy red on hbox is a version delta, fixed forward by the crate owner (not by pinning backward).
- python3 3.12.7, git 2.45.2, bwrap 0.10.0 (/usr/bin), flock (/usr/bin), gh, swarm-build (/usr/local/bin; swarm.slice MemoryMax=96G shared).
- /tank/dregg-build: 364G free (56%).
- No root change was needed for prerequisites.

## 2. The repository on hbox (built 2026-10-17 04:04Z)
- `/tank/dregg-build/nanodregg/main` — normal clone of github emberian/nanodregg; the PRIMARY checkout, detached at
  main, read-only by rule, moved only by scripts/commit. `/tank/dregg-build/nanodregg/main.git` is a symlink to
  `main/.git` (the one live repository; `$common/..` = primary, as the scripts assume).
- `/tank/dregg-build/nanodregg/wt/<layer>` for kernel codec host protocol client lang gates root hosting ledger
  transport ops perf (detached at main). Hooks: core.hooksPath=scripts/hooks.
- Local repo config: user ember arlynx <tobb@ember.software>, commit.gpgsign=false, nanodregg.landing=true (THE landing
  marker; GATES-11), nanodregg.worktrees=/tank/dregg-build/nanodregg/wt, nanodregg.buildwrap=swarm-build.
- Baseline: `STANDING 28de15e6afd0 gates=ok build=ok census=ok sim=ok rows=INCOMPLETE(4 pending) waste=ok(pinned 6,
  unpinned 0) unmeasured=0 => INCOMPLETE`, cold, 6 min 54 s under swarm-build, standing dir 84 MB.

## 3. GitHub write deploy key (bounded operational key — REMOVE AT TEARDOWN)
- id **166727747**, title "hbox nanodregg deploy (write) 2026-10-17", key ~/.ssh/nanodregg_deploy on hbox
  (comment hbox-nanodregg-deploy-20261017); ssh alias `Host github-nanodregg` in hbox ~/.ssh/config
  (backup ~/.ssh/config.before-nanodregg-20261017); origin = git@github-nanodregg:emberian/nanodregg.git.
- Teardown: `gh api -X DELETE repos/emberian/nanodregg/keys/166727747` (from the Mac); on hbox
  `rm ~/.ssh/nanodregg_deploy{,.pub}; cp ~/.ssh/config.before-nanodregg-20261017 ~/.ssh/config`.
- Logged in /tank/dregg-build/pipeline/box-changes.md (2026-10-17T04:04:19Z) with the undo.

## 4. Cutover
- ROOT froze the Mac (no scripts/commit, pre-push or lake running; lanes parked) ~04:15Z.
- **CUTOVER 2026-10-17T04:16:33Z**: on hbox `git fetch origin && git update-ref refs/heads/main origin/main` →
  main = **463200a** (= GitHub main = Mac main). From this moment main LIVES on hbox; GitHub is its mirror (pushed by
  scripts/commit after each landing); the Mac's ~/dev/nanodregg is a reader.
- First hbox commit: GATES-2's GATES-11 batch (landing guard, judge slots, build wrapper, worktree root, mac-pull).

# RECIPE FOR THE LANES (from 2026-10-17)

**main lives on hbox. Build, gate, run and commit ONLY there. The Mac builds nothing.**

## Where
- ssh host: `hbox` (from the Mac: `ssh hbox`, user `hbox`, 192.168.50.39; `hbox-ts` = tailscale 100.64.0.2 if off-LAN).
- Your worktree: `/tank/dregg-build/nanodregg/wt/<layer>`, layer ∈ kernel codec host protocol client lang gates root
  hosting ledger transport ops perf (all exist, detached at main). A new one: `cd /tank/dregg-build/nanodregg/main &&
  scripts/worktree <layer>` (root read from `git config nanodregg.worktrees`).
- Read-only reference: `/tank/dregg-build/nanodregg/main` (primary checkout, moved by scripts/commit; never edit it).
- Logs/scratch of your own: `/tank/dregg-build/nanodregg/logs/` (name files by layer).

## Commit (the only way)
    ssh hbox
    cd /tank/dregg-build/nanodregg/wt/<layer>
    git checkout --detach main            # before editing, and whenever scripts/commit says "behind main"
    # ...edit...
    scripts/commit -m '<layer>: what, why, what it refuses' PATH...      # or -F msgfile
- It judges in one of 4 box-wide judge slots (flock; a 5th lander waits, deadline 30 min), builds under
  `swarm-build` (cgroup in the shared 96G swarm.slice, taskset 0-15, nice 15) with LEAN_NUM_THREADS=4, lands by CAS on
  refs/heads/main, moves your worktree and the primary, and pushes origin. A push WARNING leaves the landing standing.
- Any build/test/run you do by hand on hbox: prefix `swarm-build` (e.g. `swarm-build lake build Kernel`,
  `swarm-build lake exe kernel-sim 1`). Filtered tests only. Long jobs: `nohup … & echo $! > logs/<layer>-<job>.pid`;
  stop ONLY by that PID. Never `pkill -f`/`killall`. Every wait loop sleeps and has a deadline. Never background a
  build and wait for a notification: foreground-wait with a deadline.
- Standing verdict: `cd /tank/dregg-build/nanodregg/main && scripts/standing.sh` (one at a time box-wide; cold ~7 min,
  warm much less).

## Carrying an in-flight edit off the Mac (the ONE sanctioned relay)
Only text patches of YOUR OWN uncommitted work in YOUR Mac worktree:
    # on the Mac
    git -C ~/dev/nanodregg-wt/<layer> diff --binary > /tmp/<layer>.patch      # tracked edits
    git -C ~/dev/nanodregg-wt/<layer> status --porcelain                      # list untracked files you created
    scp /tmp/<layer>.patch hbox:/tank/dregg-build/nanodregg/logs/<layer>.patch
    scp <each untracked file of yours> hbox:/tank/dregg-build/nanodregg/wt/<layer>/<same path>
    # on hbox
    cd /tank/dregg-build/nanodregg/wt/<layer> && git checkout --detach main
    git apply --3way /tank/dregg-build/nanodregg/logs/<layer>.patch && git status --short
Then delete YOUR Mac worktree yourself (`git -C ~/dev/nanodregg worktree remove ~/dev/nanodregg-wt/<layer>`) once the
edit is on hbox. Nobody else deletes it. Never rsync trees, never copy .lake, never copy another layer's files.

## The Mac reader
    ~/dev/nanodregg/scripts/mac-pull          # fast-forwards refs/heads/main from origin, moves the primary when clean
Read it, grep it, never build or commit there. scripts/commit on the Mac REFUSES (no `nanodregg.landing` in its config).

## Forbidden
- Any lake/cargo/lean build, test, sim or standing on the Mac. Any scripts/commit outside hbox.
- `git push` by hand (scripts/commit pushes); editing the primary checkout; `git stash`; `git add -A`; history rewrites.
- Unbounded jobs: always `swarm-build`, `nice`, ≤ 4 judges (the slots enforce it). hbox is Ember's: an art project
  uses the GPU and fn runs acl2 jobs.
- Touching anything under /tank/dregg-build that is not nanodregg's; deleting anything you did not create.

## 5. Verification (2026-10-17)
- standing at 463200a on hbox: `STANDING 463200afeb91 gates=ok build=ok census=ok sim=ok rows=INCOMPLETE(4 pending)
  waste=ok(pinned 6, unpinned 0) unmeasured=0 => INCOMPLETE` (a verdict, not a tooling failure).
- First hbox landing: **194cefb** (GATES-2, GATES-11 batch: landing guard, 4 flock slots, swarm-build wrapper,
  worktree root from config, scripts/mac-pull), pushed to origin.
- First landing THROUGH the new scripts: **09ff240** `root: decisions/root.md records that main lives on hbox`
  from /tank/dregg-build/nanodregg/wt/root: PRE-PUSH GREEN (gates, parent-gates, build, census, generated), CAS onto
  main, "pushed 09ff240 to origin"; 8 min 12 s wall (a cold slot: every target builds now).
- Mac reader: `~/dev/nanodregg/scripts/mac-pull` → "at 09ff240"; GitHub main = 09ff240. (Bootstrap was one
  `git fetch origin main:refs/heads/main` since mac-pull arrived in that pull.)
- Mac refusal: `scripts/commit` from ~/dev/nanodregg-wt/root → `scripts/commit: REFUSED — this clone is a reader;
  main lives on hbox: …` (GATES-2 also planted it on hbox via a GIT_CONFIG override).
- Concurrency: GATES-2 ran two judges at once → slots nanodregg-gate-1 and -2.
- ⚑ Memory: a cold full build in a slot was earlyoom-SIGTERMed in Codec.Proofs.Ed25519 at 9 GB (box at 92 GB:
  another slot + a hand build in wt/ledger compiling the same proofs at 11–14 GB). It shows as `build: RED` with
  `Lean exited with code 143`: that is load, not your commit — re-run scripts/commit. Slots are pre-warmed serially
  by `/tank/dregg-build/nanodregg/logs/warm-slot.sh K` (MIGRATE-HBOX; holds the slot's flock) so lanes land warm.
- Leftovers of the pre-slot layout: `main/.git/nanodregg-gate{,.lock}` (unused by the new scripts; GATES or
  MIGRATE-HBOX removes them once nothing old runs).
- Slot warming: slot 4 warm at 9eb73b8 (248 jobs, cold). Slot 1 was busy with a real judge (lanes landing), so it
  was not touched; slots 2 and 3 had already built through real judges. GATES-2's d5871cb now reports a judge
  killed under load as `KILLED(load) — re-run`, not RED.

## Who is who (from 2026-10-17 12:00Z)
The live agent-id table is on hbox at `/tank/dregg-build/nanodregg/logs/ROLES.txt` (a copy of `redregg/work/ROLES.txt`, refreshed by ROOT at every spawn/retire). Message another lane directly by its id (SendMessage); never relay through a third lane or through ROOT.
