# latitude.sh burst plan (2026-10-05) — PHASE 1 INVENTORY + PROPOSALS. Nothing created.

Lane LATITUDE-BURST. All figures read from the Latitude API on 2026-10-04 (~evening, US) with the
team's key; no secrets in this file. Project `dregg` = `proj_jmlR57Ro4NWgY` (team "Lunar Town",
created 2026-10-04). Sibling plan for Hetzner: `HCLOUD-BURST-PLAN-20261005.md`.

## Account state (measured)
- Servers in project: **0**. VMs: 0. SSH keys (team and project): **0**. Tags: 0.
- `GET /billing/usage?filter[project]=…` → `available_credit_balance: -20000`, `amount: 0`,
  `threshold: 10000`, period 2026-10-04 → 2026-11-04. Read as cents in Stripe sign convention:
  **$200.00 credit, $0 spent**. The same -20000 shows on "Default Project" → the credit is team-wide,
  one pool. `threshold: 10000` = a $100 billing threshold (an invoice is cut when usage reaches it;
  ASSUMED credit is consumed first — not stated by the API; verify on the dashboard if it matters).
  This endpoint is the spend meter for every later report.
- Billing type: project is `on_demand`; servers take `billing: "hourly"` at create.
- Resource quotas (max bare-metal count for a brand-new team) are **not exposed by the API** — only
  in the dashboard (Usage & billing → Resource quotas). A new team may be capped at 1–2 bare-metal
  servers; the first create that exceeds it will fail loudly. Check the dashboard before Phase 2 if
  convenient.
- Traffic quota endpoint: no per-region quota listed for the project.

## Billing model (docs.latitude.sh, read)
- On-demand **hourly**, no minimum term ("create and delete as you wish … paying only for the time
  you use"; price derived from 730 h/month). Hourly granularity assumed rounded **up per started
  hour** (conservative; not stated).
- Delete (`DELETE /servers/{id}`) is immediate; "may take up to an hour for the deletion to reflect
  on your billing summary" — billing stops at deletion, the meter lags.
- Monthly billing (50% off) has no pro-ration/refund on delete → **never use monthly** here.
- `schedule_deletion` exists but is "end of billing cycle" (monthly concept) — useless as a timer;
  Phase 3 deletes explicitly.
- VMs: shutting down does NOT stop billing; only delete does.

## Images / keys / tagging
- `ubuntu_24_04_x64_lts` is provisionable on every plan below and is an **instant deploy** in the US
  (seconds-to-minutes) — but only without a custom disk layout/RAID. So: deploy without RAID, then
  mkfs+mount the second NVMe at `/srv` in bootstrap (multi-drive plans).
- SSH: `POST /ssh_keys` (team) or project-scoped; create takes `ssh_keys: [id]`. Plan: register
  `~/.ssh/id_ed25519.pub` (public half only).
- Create-server has **no tags field**; tags are `POST /tags` then `PATCH /servers/{id}` with tags.
  Belt and braces: hostnames `burst-20261005-gate`, `-lane1`, … so Phase 3 can select by tag AND
  hostname prefix.
- VMs (`POST /virtual_machines`): root login disabled, you get a sudo user — useradd/sudo/systemd
  work (full KVM guest).

## Inventory — plans in stock, US first (hourly USD, on-demand)
| plan | CPU | cores | GHz | RAM GB | disk | US stock (sites) | $/h |
|---|---|---|---|---|---|---|---|
| vm.medium | vCPU | 8 vCPU | – | 32 | 320 GiB | high (DAL, ASH) | 0.35 |
| vm.large | vCPU | 16 vCPU | – | 64 | 640 GiB | high (DAL, ASH) | 0.65 |
| vm.xlarge | vCPU | 32 vCPU | – | 128 | 1.28 TiB | medium (DAL, ASH) | 1.02 |
| c3-small-x86 | Xeon E-2386G | 6 | 3.5 | 32 | 800 GB | low (ASH, ~1) | 0.52 |
| m4-metal-small | EPYC 4244P (Zen4) | 6 | 3.8 | 48 | 2×960 GB | high (DAL, NYC, MIA2, LAX2, SJC2) | 0.81 |
| **f4-metal-small** | **EPYC 4484PX (Zen5)** | **12** | **4.4** | **96** | 2×960 GB | **high (DAL, NYC, CHI, LAX2, SJC2, ASH2)** | **1.09** |
| m4-metal-medium | EPYC 9124 (Zen4) | 16 | 3.0 | 128 | 2×480+2×1.9 TB | low (DAL, MIA2) | 1.25 |
| **c3-large-x86** | **EPYC 7443P (Zen3)** | **24** | **2.85** | **256** | 2×1.9 TB | **low (NYC, CHI, LAX)** | **1.36** |
| f4-metal-medium | EPYC 4564P (Zen5) | 16 | 4.5 | 128 | 2×480+2×1.9 TB | none in US (LON2, AMS low/med) | 1.52 |
| **s3-large-x86** | **EPYC 7443P (Zen3)** | **24** | **2.85** | **512** | 2×3.8 TB | **low (NYC, CHI)** | **1.78** |
| m3-large-x86 | EPYC 7543P | 32 | 2.8 | 1024 | 2×3.8 TB | low (NYC) | 2.57 |
| m4-metal-large | EPYC 9254 | 24 | 2.9 | 384 | 2×480+2×3.8 TB | high (7 US sites) | 4.06 |
| f4-metal-large | EPYC 9275F | 24 | 4.1 | 768 | … | low (DAL, 1) | 5.25 |
| rs4-metal-large | EPYC 9354P | 32 | 3.25 | 768 | … | high (DAL, NYC, MIA2) | 6.44 |
| m4-metal-xlarge | EPYC 9455P | 48 | 3.15 | 768 | … | none in US (TOR/FRA/AMS) | 9.52 |
| rs4-metal-xlarge | EPYC 9554P | 64 | 3.1 | 1536 | … | low (DAL, NYC) | 10.88 |
Prices are the same across US/CA/EU sites for a plan; LatAm/APAC are 15–40% dearer. Per-site counts
(LKS view, a subset of sites): f4-metal-small LAX2 10 / CHI 2 / DAL 2; s3-large CHI 1; c3-large 0 in
the LKS sites (NYC/CHI/LAX listed in-stock "low" by `/plans`) → **c3-large / s3-large may be 1–2
units total; expect to fall back.**

Value for Lean (per $/h): f4-metal-small = 12 Zen5 cores at 4.4 GHz (≈1.7–1.9× a 7443P core
single-thread) at 8 GB/core; c3-large = 24 Zen3 cores at 10.7 GB/core; s3-large = same CPU at
21 GB/core for +$0.42/h. Everything ≥ m4-metal-large is 3–8× the price per core → out.
Reference: cold umbrella with Mathlib cache ≈ 25 min on 24 cores (HCLOUD plan / persvati).

## Budget
$200 credit, 15% margin → **spend cap $170**. Proposals below are sized for 24 h; each states its
runway to the cap.

## Proposal A (recommended) — fast gate, two big-RAM lane boxes, cheap E2E VM
| role | plan | site | $/h |
|---|---|---|---|
| burst-gate | f4-metal-small (12c Zen5 4.4 GHz, 96 GB) | NYC/CHI | 1.09 |
| burst-lane1 | c3-large-x86 (24c, 256 GB) — 6 lanes × ~40 GB headroom | NYC | 1.36 |
| burst-lane2 | c3-large-x86 (fallback s3-large-x86 512 GB @ 1.78) | CHI | 1.36 |
| burst-e2e | vm.medium (8 vCPU, 32 GB, sudo) | ASH/DAL | 0.35 |
**$4.16/h × 24 h = $99.84** (12 h = $49.92); with the s3 fallback $4.58/h × 24 = $109.92.
Runway to the $170 cap: ~40 h (37 h with fallback). 12 lane slots + gate.

## Proposal B — max throughput for 24 h
| role | plan | $/h |
|---|---|---|
| burst-gate | f4-metal-small | 1.09 |
| burst-lane1 | s3-large-x86 (24c, 512 GB) — 6–8 lanes, also a second cold-build host | 1.78 |
| burst-lane2 | c3-large-x86 (24c, 256 GB) — 6 lanes | 1.36 |
| burst-lane3 | f4-metal-small (12c, 96 GB) — 3–4 lanes, fastest critical path | 1.09 |
| burst-e2e | vm.large (16 vCPU, 64 GB) — can do its own cold build | 0.65 |
**$5.97/h × 24 h = $143.28** (12 h = $71.64). Runway to cap ~28 h. ~16 lane slots + gate.
Depends on both Zen3 big-RAM boxes being in stock (likely ≤2 units total).

## Proposal C — stock-safe, all fast cores (no low-stock plans)
| role | plan | $/h |
|---|---|---|
| burst-gate | f4-metal-small | 1.09 |
| burst-lane1..3 | 3 × f4-metal-small (3 lanes each at ≤24 GB, 4 if lanes stay ≤20 GB) | 3.27 |
| burst-e2e | vm.medium | 0.35 |
**$4.71/h × 24 h = $113.04** (12 h = $56.52). Runway to cap ~36 h. 9–12 lane slots + gate.
Every box comes from the high-stock pool (LAX2 alone shows 10). Weakness: 96 GB per box caps
concurrent heavy lanes; 12 cores per box makes a 6-lane box impossible.

## Notes for the chooser
- E2E as a VM is the cheapest real-root-equivalent box (sudo user, systemd, useradd). If the journey
  insists on literal root login or bare metal: c3-small-x86 @ 0.52 (ASH, ~1 unit) instead.
- All three keep the gate on the Zen5 box: post-merge gates are critical-path bound, so clock beats
  core count there; 96 GB covers one cold umbrella build.
- The second NVMe on each metal box is mounted at /srv in bootstrap (instant deploy forbids RAID).

## Phase 2 / 3 record
- chosen: **C** (root + Ember, 2026-10-04): 4 × f4-metal-small in LAX2 + vm.medium. Reason: builds are
  single-core bound → every metal box is Zen5 4.4 GHz.
- **Bare-metal quota = 2.** The third create (lane2) was refused, verbatim:
  `DEPLOYMENT_ERROR (unprocessable_entity): "Your team can deploy only 2 bare metal servers. If you
  require additional deployments, please contact sales."` lane2/lane3 NOT created; whether to ask sales
  is Ember's call.
- vm.medium is offered only in DAL/ASH (not LAX2) → e2e is in DAL (root approved).
- First server created **2026-10-04T15:55:25Z** → planned deletion **2026-10-05T15:55Z** (root re-checks
  at 2026-10-05T03:55Z).
- SSH key registered: `ssh_dmkONWq9oajL1` (public half of the Mac's `~/.ssh/id_ed25519`).
  Tag: `burst-20261005` = `tag_RdmQ2BwPyKIE742DmwwQsOgjvvB3`, applied to all three.

| host (ssh alias) | id | plan | site | public IPv4 | $/h | created (UTC) |
|---|---|---|---|---|---|---|
| burst-20261005-gate (burst-gate) | sv_6B9VaL7VX57vr | f4-metal-small 12c/24t Zen5, 93 GB | LAX2 | 67.213.124.13 | 1.09 | 15:55:26 |
| burst-20261005-lane1 (burst-lane1) | sv_y9815XgDkNvEk | f4-metal-small | LAX2 | 162.43.189.7 | 1.09 | 15:55:35 |
| burst-20261005-e2e (burst-e2e) | vm_jmlR57pmzaWgY | vm.medium 8 vCPU/31 GB | DAL | 152.236.4.24 | 0.35 | 15:57:06 |
Total **$2.53/h → ≈ $60.72 for 24 h** (well under the $170 cap).

- No private network: boxes have only public IPs (eno2 has no address; a VLAN would be a new
  resource). Base copies between gate and lane1 go over the public IPs within LAX2 via ssh.
- Bootstrap (`bootstrap.sh`, no secrets): second NVMe → `/srv` (ext4, no RAID); build-essential, git,
  curl, cmake, clang, python3, earlyoom (enabled); user `ember` (Mac key, NOPASSWD sudo, linger);
  capnp 1.5.0 from the GitHub v1.5.0 tarball, sha256
  d5ebdf858e9885c33d4b3f765006d68bd66e9b002bf4d607ff4317ef9c1aac6a (Homebrew formula checksum) checked;
  elan + the repo's lean-toolchain; rustup stable + the repo's rust-toolchain.toml nightly; bun 1.3.11;
  clone at `/srv/mini`. Metal only: `/usr/local/bin/swarm-build` (hbox contract: per-build
  `SWARM_MEM_MAX`, default 80G, MemorySwapMax=0, nice 10, all scopes in a user `swarm.slice` capped at
  84G total).
- SSH config: `~/.ssh/burst-20261005.conf`; Ember adds `Include ~/.ssh/burst-20261005.conf` at the TOP
  of `~/.ssh/config`.
- Bootstrap fixes found on the way (folded into the script): Latitude's Ubuntu 24.04 image lacks
  `libpam-systemd` (user@.service could not start → no user bus → `systemd-run --user` failed);
  `/srv/mini` needed ember ownership; toolchain PATH must precede `.bashrc`'s interactive guard for
  ssh remote commands. Scripts: `work/latitude-burst-20261005/` (bootstrap.sh, cold-build.sh,
  make-warm-base.sh, mk-lane.sh — no secrets).

### Warm bases (2026-10-04)
Ember's change: lane1 built its own copy in parallel instead of an rsync from the gate. Nothing was
transferred from the Mac or persvati except the ssh public key and these small scripts.
| box | tip | `lake exe cache get` | cold umbrella build (9639 jobs, 1159 Built) | warm base | `mk-lane.sh --verify` |
|---|---|---|---|---|---|
| gate | 5f9aa259ccfd | 50 s | **592 s (9 m 52 s)**, 16:04:36→16:14:28Z, rc 0 | /srv/warm-base (11 GB), FROZEN 16:15:17Z | VERIFIED, 0 modules compiled, 21.6 s |
| lane1 | 5f9aa259ccfd (pinned) | 51 s | **596 s (9 m 56 s)**, 16:15:47→16:25:43Z, rc 0 | /srv/warm-base, FROZEN 16:26:28Z | VERIFIED, 0 modules compiled |
- Logs: `/srv/mini-logs/` on each (cache-get-*, cold-build-*.log/.result, verify-replay-*.log);
  `/srv/warm-base/logs/green.log` = the positive control for --verify.
- Refusals tested on lane1: FROZEN missing → `REFUSED base not frozen`; wrong tip → `REFUSED base HEAD
  … != recorded tip …` (both exit 65).
- Gate's merge-keeper tree is `/srv/mini` (moves forward); the frozen base is a separate real copy.
- Lanes: `ssh burst-laneN` → `/srv/warm-base/mk-lane.sh [--verify] <lane>` → `/srv/lanes/<lane>/src`;
  build with `LEAN_NUM_THREADS=4 SWARM_MEM_MAX=16G swarm-build lake build …`. 93 GB box: 4 lanes at
  16 GB under the 84 GB slice cap.
- e2e (DAL): toolchains + repo at /srv/mini only, no Lean build; lanes copy built binaries to it.

### ⚠ Another tenant on the same credit
The API shows a VM this lane did NOT create in the same project: `fn-lat1` (`vm_BDXM5E2Ywarpk`,
vm.xlarge $1.02/h, untagged, created 16:13:44Z; a vm.large was created 16:10:31Z and destroyed
16:13:23Z). Author "ember arlynx" (same API identity). It shares the $200 credit. It is untagged, so
Phase 3 (tag + hostname prefix) will not touch it.

### Spend
- 16:27Z: billing meter `amount` = $4.20 team-wide (first started hour of each product):
  ours $2.53 (2 × f4 $1.09 + vm.medium $0.35), fn's $1.67. Credit still shows -20000.
- Run rate: ours $2.53/h; team $3.55/h with fn-lat1. Ours to the 15:55Z deletion ≈ $60.72.
