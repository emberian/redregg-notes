# DESIGN-SANDBOX — the child confines itself (nanodregg CLIENT-48, 2026-10-27)

Ember (10-27): "are we being hamstrung by bwrap limitations? we might wanna just replace that with usage of excellent community rust crates." Yes. bwrap needs user namespaces and mounts, so it fights the outer sandbox: the demo writer needed an exception row and still died (`openat2` → ENOSYS under `RestrictSUIDSGID=yes`, TENANT-2). It also leaked child trees, needed a root-installed copy plus an AppArmor profile, turned signal deaths into exit codes, and confined by PATH: any directory a child could see let it connect to every socket in that directory.

## The shape
`sandbox::command(policy, program, args)` on Linux returns a `Command` for the program itself, with a pre-exec step (`nanodregg/sandbox/src/linux.rs`). The **launcher** builds everything before the fork. The **child** then makes only system calls on what was built, between fork and exec:
`setsid` → `PR_SET_PDEATHSIG(SIGKILL)` (plus a getppid check for a parent that died during the fork) → clear CLOEXEC on the connector → `landlock_restrict_self` (which also sets `no_new_privs`) → two `seccomp` filters. All of this survives `execve`, and the child cannot undo any of it. There is no helper binary, no namespace and no mount call. It does not use `openat2`: Landlock is enforced inside the kernel's own path walk whatever call opens the file, so `RestrictSUIDSGID=yes` cannot break it.

## What each confined process may touch
| | grant |
|---|---|
| **files**: Landlock, ABI 3 required, newer rights best effort | Each rule holds an `O_PATH` **descriptor** opened by the launcher at launch, so the grant is the inode. A rename or symlink swap over the name later does not move it. **read**: the floor (`/usr /lib /lib64 /bin /etc/ld.so.cache`), the program, `read`, `exec`. **execute**: the program, `exec`, and the program's interpreters (its `#!` line and ELF `PT_INTERP`). **write**: read, write, create, rename and remove under `write`; never execute there, never create a socket, fifo or device. Devices: `/dev/null` rw; `/dev/zero`, `/dev/random`, `/dev/urandom` r. Anything else: **EACCES** |
| **syscalls**: seccomp allow-list, EPERM by default | File I/O, memory, threads, time, polling, and I/O on sockets it was *handed*. `socket`/`socketpair`: refused. `clone`: only with `CLONE_THREAD`, so no child processes. `execve`: allowed by seccomp, and Landlock decides which file may run. `kill`/`tgkill`: only of itself (the launch's copy of the filter has the pid written into it after the fork). `clone3` and `io_uring_*`: ENOSYS. No ptrace, mount, namespace, bpf, keyring, memfd, execveat, or SysV IPC |
| **address families** | None can be created. Landlock handles TCP bind and connect with no rules (ABI ≥4). Signals and abstract unix sockets are scoped to the child's own domain (ABI ≥6) |
| **unix sockets**: the CONNECTOR | A child with `connect` entries is handed one seqpacket socketpair end (`ND_CONNECTOR=<fd>`). It sends a path. The launcher connects only if that path is one of the policy's entries, and hands the connected socket back over `SCM_RIGHTS`. Anything else gets EACCES. The launcher connects again on every ask, so a restarted server's new socket is the one reached. Clients: `sandbox::connect_unix` (nd, probe) and `Host/c/sock.c` |
| **/proc** | Nothing is granted, so it cannot be opened (the same as bwrap, which mounted none). Landlock does not mediate `readlink`, though, so the Lean interpreter's `readlink /proc/self/exe` works. Measured: `lean --run` started confined and elaborated `import Lean`. Compiled `host` reads `/proc/sys/vm/overcommit_memory`, `/proc/version_signature` and `/sys/.../cpu/online`, all optional; it serves without them (QA-2's input checked: no `/proc` rule is needed) |

The kernel's Landlock rules apply to inodes, so where a binary lives no longer decides anything. A runnable file (the program, or an `exec` file with an x bit) may sit inside a hidden tree: it is granted as that one inode, so `host` under `~/nd-land` runs with `--hide /home` (TESTGROUND-4; measured: `host serve` from `~/nd-land/sandbox/.lake` served under `--hide /home`). Still refused as `Exposed`: a read or write grant, or a directory, inside a hidden tree, and a non-executable file named as the program there.

## What is lost vs bwrap, and why that is acceptable
- **The private mount view.** The child sees the host's names. `stat`, `readlink` and path walks are not mediated, so it can tell that a hidden path exists and read its metadata, but not its contents. `ProtectProc=invisible`, `ProtectHome` and `InaccessiblePaths` under systemd hide names where that matters.
- **uid mapping and PID namespace.** These never confined anything we rely on: the child runs as its own uid.
- These processes are our own code. The kernel's grants (Lean's decisions, custody) confine the AGENT. The OS sandbox is defence in depth, and it must COMPOSE with the host's own sandbox rather than fight it.
- Running the ELF loader with another file as its argument executes that file without Landlock's execute check. This gains nothing: the file was already readable and mappable, and it runs in the same confined process (no fork).
- On ABI 5 (hbox) signal scoping comes from seccomp alone.

## systemd
The unit's drop-ins form the outer layer and need **no exception row**. `RestrictNamespaces=yes`, `ProtectKernelTunables=yes`, `ProcSubset=pid`, `RestrictSUIDSGID=yes`, `MemoryDenyWriteExecute=yes` and `RestrictAddressFamilies=AF_UNIX` all stay on. One line changes: `SystemCallFilter=@system-service @sandbox` replaces `@system-service @mount`. `@sandbox` is landlock_* plus seccomp, calls that can only restrict the process that makes them. It is strictly smaller than `@mount`. Without it the launch is refused by name: `confine: landlock is missing`. Measured on hbox (systemd 256, kernel 6.11, Landlock ABI 5) with `nanodregg/deploy/live/confined-unit.sh`: the writer and a member's follower each ran as a transient system unit with the full drop-ins, and the member created, wrote and read back.

## macOS
Keep `sandbox-exec`. It is a policy interpreter rather than a nested sandbox: it already filters exec, fork and connect by path literal, and it composes with nothing we deploy. Landlock does not exist there. The connector is Linux-only, and `connect_unix` falls back to a plain connect, which sandbox-exec filters.

## TCB rows (gates/tcb.tsv) replacing nd-bwrap, its AppArmor profile, burst5's copy, EXEC_FILTERED and CONNECT_FILTERED
`Landlock (Linux)`, `seccomp-bpf (Linux)`, the crates `landlock 0.4.5`, `seccompiler 0.4.0`, `enumflags2(_derive) 0.7.12`, and `connector (Linux)`. All are trusted-unverified. Each lifts when a verified confinement mechanism replaces it.

## Crate choice
`landlock` (the LSM maintainers' crate) and `seccompiler` (rust-vmm/Firecracker), not `extrasafe`. extrasafe builds and applies its filters in the calling thread, and it allocates while doing so. A child of a multi-threaded launcher must instead apply programs built beforehand between fork and exec, and `RulesetCreated::restrict_self` and `seccompiler::apply_filter` do exactly that. `rustix` (already in the TCB) provides the socketpair, SCM_RIGHTS, setsid and pdeathsig. The crate's only `unsafe` sites are the `pre_exec` call and the connector's descriptor claim.
