# SANDBOX report: bwrap replaced by self-confinement (nanodregg 7ec94566, CLIENT-48, 2026-10-27)

**Landed** on emberian/nanodregg main as 7ec94566. Rule 1: rebased on 7d30fc1, then built and tested what the change touched, then pushed. The push was accepted. Design is at redregg `work/promo/DESIGN-SANDBOX.md`.

## What changed
- `sandbox/src/linux.rs` (new). On Linux `sandbox::command` returns the program itself, plus a pre-exec step. The launcher prepares everything before the fork:
  - a Landlock ruleset whose rules hold O_PATH descriptors. Read: the floor, the program, `read`, `exec`. Execute: the program, `exec`, and the program's `#!`/PT_INTERP interpreters. Read/write under `write`, but no exec and no making sockets, fifos or devices there. `/dev/{null,zero,random,urandom}` are granted. TCP is handled with no rule. Signal and abstract-socket scope apply where the kernel has ABI 6.
  - two seccomp programs. The first returns ENOSYS for clone3 and io_uring. The second is an EPERM-default allow-list: no socket or socketpair, `clone` only with CLONE_THREAD, kill/tgkill only of itself (the pid is patched into the launch's copy of the filter).
  - for policies with `connect` entries, a seqpacket **connector**.

  The child itself then runs, in order: setsid, PDEATHSIG SIGKILL (with a getppid race check), clear CLOEXEC on the connector, landlock_restrict_self (no_new_privs), and the two seccomp installs. No openat2 is used anywhere.
- `sandbox/src/connector.rs`, `sandbox::connect_unix`, and `Host/c/sock.c` (`nd_connector_ask`). The child sends a path over `ND_CONNECTOR`. The launcher dials it only if it exactly matches a policy entry, and returns the socket over SCM_RIGHTS or the errno (EACCES otherwise). It connects fresh on every ask, so a restarted server is reached. The client sockets (`nd`) and the probe go through it.
- **Deleted:**
  - `EXEC_FILTERED`, `CONNECT_FILTERED`.
  - `ConnectOverlap`, `SocketInGrant`, `GrantUnlisted`, removed from the sandbox and from `Hosting.LaunchFailure` (codes 14–16; `launcher/src/generated.rs` re-emitted).
  - the bwrap 128+N rule in `killed_by_signal`.
  - `sandbox/apparmor/nd-bwrap`.
  - AF_NETLINK in the units (`deploy/units` re-emitted).
- **TESTGROUND-4.** A runnable file (the program, or an `exec` file with an x bit) inside a hidden tree is granted as that one inode, so `host` under `~/nd-land` runs with `--hide /home`. Measured from `~/nd-land/sandbox`: `host serve` served. Still `Exposed`: a read/write grant or directory inside a hidden tree, and a non-executable file used as the program.
- **QA-2's /proc input.** No rule is needed. Landlock does not mediate `readlink`, so the Lean interpreter's `/proc/self/exe` works. Measured: `lean --run` started confined and elaborated `import Lean`. Compiled `host` reads only optional /proc and /sys files.
- **TCB rows** now cover Landlock (Linux), seccomp-bpf (Linux), landlock 0.4.5, seccompiler 0.4.0, enumflags2(_derive) 0.7.12, and the connector. They replace the three nd-bwrap rows and EXEC/CONNECT_FILTERED. `gates/tcb.py` passes.
- **Decision entry** `decisions/client.md` CLIENT-48 (Ember's words). The deploy docs (RUNBOOK, live/README, testground) and `deploy/live/{harness,broker}.sh` now check for Landlock instead of nd-bwrap.
- **New plant** `deploy/live/confined-unit.sh ROOT BIN [FILTER] [TAG]`.

## Crates
I chose `landlock` 0.4.5 and `seccompiler` 0.4.0 (APIs read from `~/.cargo/registry`), not `extrasafe`. extrasafe is not in the local mirror, and it applies in the calling thread and allocates. A child of a multi-threaded launcher must instead apply prebuilt programs between fork and exec. The crate's lint went from `unsafe_code = forbid` to `deny`. There are exactly two allowed sites, each with a SAFETY note: the `pre_exec` call, and the claim of the connector fd.

## Measured on hbox (Ubuntu 24.10, 6.11.0-29, Landlock ABI 5, systemd 256), all on the rebased tree, all filtered
- sandbox confine (9), connect (5), custody (10). The new plants:
  - an open outside the ruleset gets EACCES by name;
  - a written file cannot be executed;
  - an exec of an unlisted program is refused, while its own program can re-exec;
  - no fork;
  - it can signal itself but not another process;
  - a sibling socket and a self-made socket are refused;
  - a socket bound under a read grant is not reached;
  - a program inside a hidden tree runs and exposes only itself.
- client supervise (11, incl. the confined Lean host answering, and the signal death seen as childSignaled), real, stdio, join, sockets.
- launcher: isolation (10), resident (2), members (12), broker (13), grain, sock, path_vectors. resident_bell (1, 688 s) passed on the pre-rebase tree.
- fence (3, real nd/nd-hosted uids, the group socket reached through the connector). It must run with `CARGO_TARGET_DIR` and `ND_LEAN_BIN` outside /home: nd cannot traverse `/home/hbox`, which is a fence fact, not a sandbox one.
- clippy clean and fmt clean for the three crates. Lean builds; `emit-units --check` and `emit-hosting --check` are OK.
- Transient system units with the demo box's FULL drop-ins:
  - lines: `RestrictNamespaces=yes ProtectKernelTunables=yes ProcSubset=pid RestrictSUIDSGID=yes MemoryDenyWriteExecute=yes RestrictAddressFamilies=AF_UNIX`, plus PrivateDevices, ProtectProc=invisible, IPAddressDeny, NoNewPrivileges and an empty CapabilityBoundingSet.
  - The writer (`host serve`) and a follower were both active. The member ran `create`, `write`, then `read` and got `1=hello-from-the-unit`.
  - With `SystemCallFilter=@system-service @sandbox`: works.
  - With `@system-service` alone: `nd-supervise: confine: landlock is missing`, exit 64.

## What it costs, said plainly
- The child now sees the host's names. `stat`/`readlink`/path walks are not mediated, so a hidden path's existence and metadata are visible; its contents are not.
- On ABI 5 (hbox), signal scoping comes from seccomp alone.
- A unit filter must include `@sandbox`. That is the only line the demo writer changes, and it replaces `@mount`. Note it is not literally "no SystemCallFilter change".
- Exec of the ELF loader with a file argument bypasses Landlock's execute check. That runs only what the process could already read, in the same confined process, so it is no escape.

## Handoffs
- `demo-box-provisioning-plan` (SendMessage, sent; not yet read): the exception row is gone. The writer unit becomes the full contract with `SystemCallFilter=@system-service @sandbox` and `RestrictAddressFamilies=AF_UNIX`, and the tarball must be rebuilt at 7ec94566.
- TENANT.report.md and TESTGROUND.report.md were appended: rebuild the tarball at 7ec94566. The TESTGROUND-4 /home refusal is fixed.

## Left as found
- `gates/readset.py` still holds the bwrap pivot translation. It is dead now but harmless; delete it at the next touch of that gate.
- The repo's own `deploy/units` carry no SystemCallFilter or RestrictNamespaces lines. Adding them is now possible but unmeasured on a unit box.
- Cleaned up: `/srv/nd-sbx`, `/tank/dregg-build/nanodregg/scratch-sandbox`, and the local scratch worktree. The hbox worktree `~/nd-land/sandbox` is kept at 7ec94566 (warm `.lake`, `target`).

## Tenant tarball at 7ec94566 (coordinator's follow-up)
- **Tarball:** `hbox:/tank/dregg-build/nanodregg/logs/tenant/nd-testground-7ec94566.tar.gz`, sha256 `db967c9b241fa4015d30f899abcdd7360e44ea17ca2aa70acac7950c3e8d29e5`.
- **kernel.wasm:** sha256 `dd44a38451873a56fe64422a53a789ef21f4d306906b431ab35d68639364fb61`, 4,257,318 B. Built clean at 7ec94566 with lean v4.30.0 and emcc 6.0.9.
- **How it was built.** I followed the PUBLISH.md recipe, then packed with `pack-tenant.sh`. The wasm half ran in a private copy of the build cache, `~/.cache/nd-testground/sbx-7ec94566`, for this reason:
  - The shared `~/.cache/nd-testground/v4.30.0/lean4` has a hand edit in `src/runtime/object.cpp`: `string_to_list_core`'s nil changed from `lean_box_uint32(0)` to `lean_box(0)`.
  - `patch-rt.sh` then refuses that cache ("expected 4 files changed").
  - I reverted the edit in my copy only, so this kernel is the tree's recipe as committed.
  - On wasm32 that edit looks like a real fix: the nil of a List must be a scalar. Whoever made it should land it in `patch-rt.sh`. It was not mine to land, and I did not touch the shared cache.
- **Unit verified under:** `…/logs/tenant/nd-testground-writer-7ec94566.service`, the plain contract described in the next section.
- **How it was verified:** with `…/logs/tenant/verify-tenant.sh`:
  - The tarball's own binaries ran from `/opt/nd-tg-verify`, and the unit was installed in `/run/systemd/system`.
  - Only the uid, the paths and the unit name were substituted.
  - The unit was active with every hardening line on.
  - A member's create, write and read synced: `1=synced-through-the-plain-contract`.
  - Everything was torn down afterwards.
- **Sent** to `demo-box-provisioning-plan`.
- `testground/build/gate.sh` was not run on this kernel; the lane was asked only for the unit check.

## Closing

**What a confined process may touch (Linux, CLIENT-48).**
- **Files:**
  - read: the floor (`/usr /lib /lib64 /bin /etc/ld.so.cache`), its program, its `read` and `exec` grants;
  - execute: its program, its `exec` grants and their `#!`/ELF interpreters, nothing else;
  - read/write/create/remove under its `write` grants, but never execute and never make a socket, fifo or device there;
  - `/dev/null` rw; `/dev/zero`, `/dev/random`, `/dev/urandom` r;
  - every other open is EACCES.
  - Each grant is the inode behind a descriptor the launcher opened, so where a binary lives does not matter.
- **System calls:**
  - an allow-list, EPERM by default;
  - no socket creation, no process creation (threads only), signals only to itself;
  - no mount, namespace, ptrace, bpf, keyring, io_uring, memfd or execveat;
  - no openat2 is needed.
- **Network and sockets:**
  - no address family can be created;
  - TCP is handled by Landlock with no rule;
  - at ABI 6 (Debian 13), signals and abstract sockets are scoped to its own domain;
  - unix sockets are reachable only through the connector, and only the policy's exact paths.
- **Names:** the host's names are visible (stat, readlink); contents are not.

**What was deleted.**
- bwrap as the Linux mechanism: `/usr/local/libexec/nd-bwrap`, `sandbox/apparmor/nd-bwrap`, and the deploy steps that installed them.
- `EXEC_FILTERED` and `CONNECT_FILTERED`.
- `ConnectOverlap`, `SocketInGrant`, `GrantUnlisted`, including `Hosting.LaunchFailure` codes 14–16.
- The `128+N` reading in `killed_by_signal`.
- `AF_NETLINK` in the units.
- The demo writer's exception row: 5 directives restored, `@mount` dropped for `@sandbox`.

**The TCB rows (gates/tcb.tsv), all trusted-unverified, owner CLIENT, each lifted when a verified confinement mechanism replaces it.**

| row | covers |
|---|---|
| `Landlock (Linux)` | ABI 3 required; ABI 5 on hbox, 6 on Debian 13 |
| `seccomp-bpf (Linux)` | the two programs in `sandbox/src/linux.rs` |
| `landlock 0.4.5` | crate |
| `seccompiler 0.4.0` | crate |
| `enumflags2` / `enumflags2_derive 0.7.12` | crates |
| `connector (Linux)` | the launcher dials only the policy's exact paths |

These replace the rows `nd-bwrap (hbox)`, `nd-bwrap AppArmor profile (hbox)`, `nd-bwrap (burst5)`, `EXEC_FILTERED` and `CONNECT_FILTERED`.

## SANDBOX-2 (CLIENT-52): CRIT-SANDBOX answered — landed nanodregg main 5c0c2055 (2026-10-27)
- **Landed:** `5c0c2055` "sandbox!: the confinement an outside review could not break …" (rebased twice over CLIENT-51 and SPEC-19/20; the decisions conflict was two appended entries, both kept). Decision entry: `decisions/client.md` CLIENT-52, with its critique.
- **What the predecessor's scratch diff became:** it compiled nowhere as written (seven `Policy` literals lacked `landlock_abi`). Fixed, and it went in with: `launcher/src/generated.rs` re-emitted (LaunchFailure 14 `connectOverlap`, 15 `privileged`, 16 `landlockAbi`); the Rust connector client's 30 s reply bound; the C client's reply bound (the connection's timeout). Both clients drain a late reply before the next ask, so a timed-out reply never answers a later one.
- **Test stubs:** `members.rs`'s python deciders now run as `/usr/bin/python3 -I -c CODE DIR`. The two self-killing deciders/controllers (`broker.rs`, `isolation.rs`) are the launcher probe placed as `killself`, which SIGKILLs itself.
- **THE PROBE.** `sandbox/src/bin/sandbox-probe.rs` is a compiled plant making raw syscalls. `sandbox/tests/probe.rs` runs it in 5 tests:
  - 26 operations, each refused confined with the expected errno, and each NOT so refused unconfined (the control): fchmodat, fchmodat2, chmod, utimensat, utimes, chown, setxattr on a same-uid sibling; fchmod in the grant; read of a sibling (EACCES); mkfifo in the grant; kill, tgkill, rt_sigqueueinfo and pidfd_open on the parent; kill(-1); F_SETOWN, F_SETOWN_EX, F_SETSIG, O_ASYNC; PR_SET_PDEATHSIG 0; socket, socketpair, memfd, clone(SIGCHLD) (all EPERM); io_uring (ENOSYS); exec of a file it wrote (EACCES).
  - A leaked non-CLOEXEC fd: EBADF in the child, open unconfined.
  - A renamed-away socket ancestor: the child still reaches server A; unconfined reaches B.
  - The granted socket name swapped for a link: ECONNREFUSED; unconfined follows it.
  - Launch-time refusals: a `/` read grant (Exposed), a quoted socket name (UnnameablePath), a socket directory inside the write grant (ConnectOverlap), landlock_abi 99 (LandlockAbi).
  - The named residual: standalone, the loader still maps a written file.
  - Mutations went red: admitting PR_SET_PDEATHSIG, or removing the close-on-exec sweep, each turned the probe red.
- **Production profile, rendered:** `Ops.Units.Node.profile` (+ `Node.landlockAbi`, theorem `ofNode_landlock_abi`) puts the following into `nd-host-serve.service` and `nd-hosted-follow@.service`:
  - `--landlock-abi 6`;
  - `ProtectSystem=strict`, `ReadWritePaths=` the Store (and the follower's socket directory), `NoExecPaths=` the Store;
  - the kernel-surface lines;
  - `MemoryMax=2G TasksMax=64 LimitNOFILE=1024 LimitFSIZE=4G`.
  - The quota is a deployment input (RUNBOOK §2). `deploy/live/confined-unit.sh` now reads the profile lines out of the rendered unit; `PROBE=1` runs the probe through nd-supervise there.
- **Measured on hbox** (6.11, ABI 5, systemd 256):
  - Filtered tests green:
    - sandbox: confine 9, connect 5, custody 10, probe 5;
    - client: join, real, stdio, sockets, supervise 11;
    - launcher: broker 13, grain, isolation 10, members 12, resident 2, sock;
    - fence 3, as nd and nd-hosted, with the target, Lean bins and scratch on /tank.
  - confined-unit.sh:
    - at `ABI=5`, the writer and follower served create/write/read under the rendered profile;
    - at the unit's 6, refused `confine: landlock ABI 5, the policy requires 6` (exit 64);
    - with `PROBE=1`, 25/25 refused in the unit, and the loader case was refused by NoExecPaths (`failed to map segment from shared object`).
- **Tenant tarball at 5c0c2055:** `hbox:/tank/dregg-build/nanodregg/logs/tenant/nd-testground-5c0c2055.tar.gz`, sha256 `f78c373e6f1064d6892271f100c40137aa0d532eeec332195e4363acc536d1e1`.
  - kernel.wasm `2e000f6a79444c6189d0315254993143648051a225741a3fd8e6e3ec395875e3` (4,406,103 B, clean tree, lean v4.30.0, emcc 6.0.9; the shared cache `~/.cache/nd-testground/v4.30.0` built without refusal).
  - host `7ffffd96…fd6c`, nd `838ae515…745e`, nd-supervise `6250f3d8…48f4`.
  - The tarball's own binaries served a member under the profile at ABI 5.
  - gate.sh not run.
  - Both the unit lines and the hashes were sent to `demo-box-provisioning-plan` (it already committed a 2 GiB Store filesystem, dregg-infra-demo-vm 717113a).
- **Not reached:** ABI 6 itself (no 6.12 kernel here); the connector's peer-uid refusal and `privileged` (one uid, no root in tests); a test of the connector timeouts. Grants are canonicalized before they are opened (a concurrent real-directory rename is assumed away), and stdio is passed through unchecked.
- **Left as found:** hbox worktree `~/nd-land/sandbox2` at 5c0c2055 (warm `.lake`, `target`, a built kernel.wasm), plus `~/nd-land/s2b.sh` and `~/nd-land/s2-logs/`. Removed: `/srv/nd-sbx2` and `/tank/dregg-build/nanodregg/scratch-sandbox2` (both this lane's own). No unit is left running.
