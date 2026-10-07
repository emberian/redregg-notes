# Renting compute for fn: what we learned (2026-10-04)

The first day of renting boxes for the fn swarm: Hetzner fn-cloud1/2 and Latitude fn-lat1. Each lesson below is paired with the fix that keeps it from biting twice.

## What we rented, what it cost, what it did

| box | provider / type | cores / RAM | price | per-core speed |
|---|---|---|---|---|
| fn-cloud1 | Hetzner ccx33 (dedicated) | 8 / 32 GB | $0.26/h | not measured |
| fn-cloud2 | Hetzner cpx52 (shared) | 12 / 24 GB | $0.19/h | not measured |
| fn-lat1 | Latitude vm.xlarge, DAL (EPYC Genoa, Zen 4) | 32 / 128 GB | $1.02/h | 0.71 s, ≈ hbox's i9-12900 (0.69 s); laptop 1.25 s |

The benchmark is a single-thread Python loop. Latitude's f4-metal-small (Zen 5, 4.4 GHz, $1.09/h) should be faster per core, but we never got one; see the quotas below.

**Compute was cheap; agent tokens were not.** About $30 of boxes for the day, against roughly $125 of overflow tokens burned in about an hour by ~17 concurrent agents. So prefer more boxes and fewer agent-tokens: long box jobs (image builds, native suites, certifies, scenario tiers) that cost no tokens while they run.

What the boxes delivered:
- the first image built off-hbox (batch 4 on lat1);
- batch 6;
- dozens of overlay verdicts;
- the full image closure certified at dev (1135/1135 default, 1085/1085 dtn);
- scenario tiers;
- a full `make check`;
- a flake recheck.

## Lessons, each with its fix

1. **Provider quotas are the first wall, and only a human can move them.**
   - Hetzner project `dregg`: 8 dedicated cores and about 18 shared (6 already used by the dregg servers), so every ccx63/53/43 was refused.
   - Latitude: 2 bare-metal servers per team, and 2 VMs as a separate class.
   - Fix: request raises *before* a burst day (both requests are pending now), and apply for LLC cloud credits (Microsoft for Startups, AWS Activate).
   - The bootstrap is provider-agnostic, so any x86-64 Linux box can join.

2. **Certificates carry over only with byte-identical toolchains at the same paths.** Toolchain identity is a digest of the SBCL runtime, the ACL2 core and the launcher. Replicate `/tank/fn` (toolchain, certcache, images) at the same paths and hbox's certificates install as-is.
   - It must be x86-64 with glibc ≥ the SBCL build's (2.38). ARM boxes would need a second certified toolchain.
   - The laptop's Homebrew SBCL is a *different* identity; its certs never serve hbox or the boxes.

3. **Seed new boxes from a cloud box, not from hbox.** hbox uploads at ~8–10 MB/s and its cache disk is busy. Seed cloud1 from hbox once, then everything else from cloud1. lat1 bootstrapped in **403 s**: 35 s system, 5 m 45 s data, 10 s checks.
   - Boxes hold ~8.8K certificate keys (1.1 GB: the current toolchain's), not hbox's full 20 GB cache. Anything missing is certified on the box and copied back to hbox.

4. **A box is not usable until it is *qualified*; "registered" is not enough.** The gaps we hit, each found late and each costing runs or agent time:
   - **No docker on lat1.** reader_clients ran nothing.
   - **No `dilithium-py`.** consumer_exchange failed 7 of 11, because the signature verifier answered "undecided".
   - **`remote_check.sh` had no `FN_ACL2` for the rented boxes.** Every lane's remote check failed with "no FN_ACL2" until fairy/cloud 9ed960450. Nobody noticed for hours, because lanes read "failed" as "red".
   - **The evidence archive** was read as `hbox:/tank/fn/evidence`, unreachable from the boxes. Fixed with a local copy plus a 5-minute mirror timer.
   - **Image sets were only mirrored *from hbox*,** so a set built on lat1 had to be relayed through the laptop to reach the others.
   - **The fix for all of these: `tools/box_qualify.sh BOX`** (to be built; see below). A box receives work only after it passes, and a failed qualification names the gap.

5. **Classify a red on a new box with an hbox control run before believing it.** The integrator re-ran batch 4's own images on hbox (`ctl-55ff708a6`) and split "lat1 environment" from "implementation" in one pass. Make this automatic: qualification includes the env-sensitive modules compared against hbox.

6. **Overlay cores lose one known race.** `test_native_state_checkpoint`'s running-owner compaction test fails on any *re-saved* core (overlay or re-saved production) and passes on published cores. It's a test-timing issue to fix in the test (wait for the publication). Until then, an overlay red in that one case is not evidence.

7. **Providers reuse IP addresses.** A deleted VM's host keys in `~/.ssh/known_hosts` blocked its replacement at the same IP. The fix (already live): rented boxes' keys go in `~/.ssh/known_hosts.fn-boxes`, via `Include ~/.ssh/fn-boxes.conf`.

8. **Idle paid boxes are the failure mode.** Meanwhile the laptop, ember's machine, hit load 131 on 12 cores because lanes defaulted to it. Fixes:
   - lanes certify and run REPLs on rented boxes only, and the laptop runs no ACL2 (COMMON.md);
   - **a scheduler (boxq) places jobs by free capacity,** with integrator > lane > fill priority;
   - **a fill queue:** idle boxes run scenario tiers, closure certifies and `make check`, and every red becomes a ledger item. One fill fairy produced 23 items and a warm cache for a few tokens.

9. **Teardown must pull results back first.** Teardown copies new certificates into `hbox:/tank/fn/certcache` before deleting any box. The timer is a laptop `nohup` + `caffeinate` script that re-reads a `DEADLINE` file every minute, so an extension is a one-line edit.
   - A plain `sleep` timer pauses while the laptop sleeps, so `caffeinate` (or a server-side scheduled delete) is needed.
   - Deletion only ever targets labelled servers (`fn-burst=…`), never the dregg servers.

10. **Batches are slow for structural reasons, not for lack of cores.** Batch 3: acquire 20 min (now ~1), image builds + host-ld ~26 min, natives ~18 min wall. More boxes help the natives, but the big wins are elsewhere:
    - overlay-first batches, with no image build for host-only changes;
    - only the natives a change affects;
    - fast natives: test-profile deadlines and warm owners;
    - cached verdicts.
    The cloud lane, the scenarios lane and the Fable iteration lane own these.

## Keeping it working

1. **`tools/box_qualify.sh BOX`**, run by `box_bootstrap.sh` at the end and by boxq before placing work, and again whenever a box's image set or toolchain changes. It checks:
   - toolchain identity equals hbox's; glibc; architecture;
   - required system packages: docker, the openssl test tool, pip modules including `dilithium-py`;
   - every tool resolves the box: farm, `remote_check`, `proof_repl`, `hbox_native --box`, `scenario_suite --box`, evidence store;
   - a narrow certify that installs from cache;
   - the env-sensitive native modules (reader_clients, consumer_exchange, a BP module, state_checkpoint on a published core) agree with hbox's verdicts on the same image set.
   Output: one line per check, plus a qualified/unqualified record in `~/.config/fn/boxes.json`. boxq refuses unqualified boxes.
2. **A unit test that every box-aware tool knows every registered box**, so a new box can't be half-registered again.
3. **The package list lives in one place** (`box_bootstrap.sh`'s system step), and qualification reads it. Adding a test dependency means adding it there.
4. **Publication fans out from the builder** to every qualified box, so image sets don't hub through hbox.
5. **`docs/boxes.md` in the fn repo** holds the operational parts of this file: bootstrap, qualify, teardown, quotas, and the known-hosts arrangement. It contains no IPs, credentials or account identifiers (origin is public).
