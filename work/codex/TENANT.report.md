# TENANT — nd-testground on the demo box (real 2026-10-27, ~03:15-03:45Z)

Lane: produce nano's testground tenant for the demo VM, at the demo-box session's request.

## Delivered
- dregg-infra **demo-vm `884ec86`** (pushed: origin = hbox + anchor; fast-forward from 8fca5ad). New files only, in `/Users/ember/dev/dregg-infra-demo-vm/edge/demo/tenants/nd-testground/`: `tenant.env`, `site.caddy`, `systemd/nd-testground.service`, `writer/nd-testground-writer.service`, `nd-testground-serve`, `README.md`, `TRUST.md`.
- Listener: **127.0.0.1:8795**, loopback TCP. It is not a Unix socket because ws-relay.py binds TCP only, and the contract's TENANT_LISTEN is a port. Hostname: **nano.demo.dregg.online**.
- Tarball: **`hbox:/tank/dregg-build/nanodregg/logs/tenant/nd-testground-914f2d7e.tar.gz`**, sha256 **`933ab71be47d0f8e303351c2b03d0875798442cf57c46634824cbd30c1f15a3c`**. Built from nanodregg `914f2d7eb9a6f09cbf3934416fd9dc22aac869f3` in a clean worktree, `hbox:…/nanodregg/wt/tenant`. The pack script `pack-tenant.sh` and the build logs sit beside the tarball.
- The demo-box session got the details by SendMessage. TESTGROUND-3 got a section in `TESTGROUND.report.md`.

## Shape (re-done mid-lane)
- The demo-box session committed a tenant contract while I worked (434aeb6: `tenants/README`, `tenants.slice` with 1G and one vCPU, nftables `tenant_uids`, `tenants.d` Caddy import, and install-demo checks). My first draft was one unit with its own 2G slice and a sysusers file. I rewrote it to the contract:
  - two units in `tenants.slice`;
  - no Mini paths or `AmbientCapabilities` anywhere in a unit file (install-demo greps for them);
  - a literal host in site.caddy.
- **Contract conflict, left for the infra lane to decide (it widens a check):** nd-supervise confines `host serve` with bwrap and refuses to run it unconfined. So the writer cannot carry `RestrictNamespaces=yes`.
  - I split the units. The front unit (node guest-book + python relay, the network-facing parsers) carries every contract line. The writer has no network at all and keeps MDWE and `@system-service @mount`.
  - The writer sits in `writer/`, which install-demo does not read. In `systemd/` it would stop the whole install.

## Measured (hbox)
- Builds:
  - `swarm-build cargo build --release --locked -p nanodregg-client --bin nd-supervise --bin nd`: 25 s.
  - `lake build host`, starting from a warm `.lake/build` copied with `cp -a` from wt/testground. The copy itself took ~25 min on a loaded box (load 42).
  - `build.sh c` built 111 tree modules + 649 toolchain modules.
  - `build.sh wasm` first failed twice:
    - my seeded lean4 checkout lacked src/util (my own seeding mistake; fixed by a fresh clone);
    - main's build.sh has no libuv headers on hbox; fixed with CPATH set to libuv v1.48.0.
  - Result: kernel.wasm 4,200,502 B, 804,679 B gzipped.
- Binaries need at most GLIBC_2.39 (nd-supervise, nd); host needs 2.17.
- Both units ran under systemd 256 from `/run/systemd/system`, rendered from the committed files with only the uid, slice, paths, port and unit names substituted.
  - Both active. The guest-book synced and invited. `GET /world.json` returned 200. Two visitors were enrolled through `/enroll`.
  - A writer restart restarted the front unit (PartOf), and the World came back from its Store.
  - Memory: writer 14 MB, front 170 MB (peak 287 MB).
  - First runs found two lines that bwrap needs off: `ProcSubset=pid` and `ProtectKernelTunables`.
  - I tore the test units and slices down; `systemctl list-units` shows 0 left. I removed the scratch state dirs.
- site.caddy passes `caddy validate` 2.11.4, imported through `tenants.d/*.caddy`, and passes install-demo's host and upstream checks.
- Through a local Caddy in front of an hbox relay: `/world.json` 200, `/ws` 101, `/enroll` answered, any other path 404.

## Found
- ⚠ nanodregg at 914f2d7e: after join and enrolment, a visitor's sync and every command are `refused badResult`.
  - Reproduced under systemd, by hand with run.sh, and with testground-b's own binaries.
  - Reported to TESTGROUND-3. The demo is not usable by visitors until it is fixed and the tarball rebuilt.
- My own mistake, caught before it mattered: a `pgrep -f` wait loop that would have matched its own ssh command line. I stopped it at once and killed nothing.

## Left for others
- Infra lane:
  - the writer exception;
  - `/usr/local/libexec/nd-bwrap`;
  - apt `nodejs` and `python3`;
  - fetching the tarball to `/opt/nd-testground/914f2d7e` with `current` pointing at it;
  - genesis (README);
  - the CONFINEMENT §6 row K (in TRUST.md).
- Ember: publish Pages from the tarball's `testground/`.
- TESTGROUND-3: the badResult bug; `run.sh serve`.

## TENANT-2 — the writer's `Can't mkdir parents for /dev: Function not implemented` on dregg-demo (real 2026-10-27)
- **Directive: `RestrictSUIDSGID=yes`.** Syscall: **`openat2`**. Not `SystemCallFilter`, `MemoryDenyWriteExecute`, `PrivateDevices` or `RestrictAddressFamilies`.
- Mechanism, read at source:
  - systemd 257 `src/shared/seccomp-util.c` `seccomp_restrict_sxid()` blocks `openat2` outright with `SCMP_ACT_ERRNO(ENOSYS)`, because its flags sit in a struct that seccomp cannot inspect. A second seccomp filter, so no `SystemCallFilter=` addition can re-allow it.
  - bwrap 0.12.0 opens every newroot path through `safe_openat()` → `openat2(RESOLVE_IN_ROOT)`. On ENOSYS/EPERM/EINVAL it calls `safe_openat_fallback()`. Debian builds with `-Dassume_kernel=5.10.0` (debian/rules), so the fallback is compiled out and returns ENOSYS. `ensure_newroot_parents_at("/dev")` fails first.
  - bwrap 0.10 (hbox's, and so TENANT's systest) has no openat2, which is why TENANT's hbox run was green with the identical unit. 0.13.1 (sid) is the same as 0.12.
- strace under the failing unit (`hbox:/tank/dregg-build/nanodregg/logs/tenant/tenant2/strace-a.txt`, line 9): `openat2(5, "/", {flags=O_RDONLY|O_DIRECTORY, resolve=RESOLVE_NO_MAGICLINKS|RESOLVE_IN_ROOT}, 24) = -1 ENOSYS (Function not implemented)`.
- Measured on hbox:
  - TENANT's systest writer unit, re-rendered for a fresh World in `…/tenant/tenant2/state`, with Debian 13's exact binary (`bubblewrap_0.12.0-1~deb13u1_amd64.deb`, bwrap sha256 `573236e5…985f`) bound over `/usr/local/libexec/nd-bwrap` by `BindReadOnlyPaths=`.
  - (a) As admitted: the same error, verbatim.
  - (b) The only change `RestrictSUIDSGID=no`: active, `STATUS serve`. With the front unit: `guestbook$ nd sync … → ok`, `nd invite … → ok`, `GET /world.json` 200.
  - (c) `RestrictSUIDSGID` replaced by `NoExecPaths=<state>`: also green.
  - Units were rendered in `…/tenant2/*.service`. All were torn down; `list-units t2*` shows 0.
- **No nd-supervise fix exists:** the openat2 call is inside bwrap. A self-built bwrap with the fallback compiled in is the weaker design (path-walk resolution instead of RESOLVE_IN_ROOT). No tarball rebuild is needed.
- **Residual of dropping it (the infra lane's call, since it weakens a check):**
  - `NoNewPrivileges=yes` already mounts everything nosuid inside the unit (exec-invoke.c `mount_nosuid`).
  - What is left is a setuid-`nd-testground` file persisting on disk. Its only persistent writable home is `/var/lib/nd-testground`, which is 0700 nd-testground, so no other non-root uid can reach it.
- Sent to `demo-box-provisioning-plan`: the unit's fourth omission, and install-demo's exception list extended to it.

## SANDBOX (2026-10-27): rebuild the tarball at nanodregg 7ec94566
- nd-supervise no longer uses bwrap (CLIENT-48). The child confines itself with Landlock and seccomp before exec. There are no namespaces, no mounts and no openat2, and nothing is installed (`/usr/local/libexec/nd-bwrap` and its AppArmor profile are retired).
- The writer unit can carry the FULL tenant contract: `RestrictNamespaces=yes`, `ProtectKernelTunables=yes`, `ProcSubset=pid`, `RestrictSUIDSGID=yes`, `RestrictAddressFamilies=AF_UNIX` (no AF_NETLINK). Exactly one line changes: `SystemCallFilter=@system-service @sandbox` instead of `@system-service @mount`. Without `@sandbox`, the launch is refused by name: `confine: landlock is missing`.
- Measured on hbox: `nanodregg/deploy/live/confined-unit.sh` ran the writer and a follower as transient system units with those drop-ins, and the member created, wrote and read back.
- Design: redregg `work/promo/DESIGN-SANDBOX.md`. Report: `codex/SANDBOX.report.md`.
