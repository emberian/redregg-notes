CRIT-SANDBOX, 2026-10-27.

I would not call the writer confined to its declared write grant at commit `7ec94566beb370053d81f1d0f079ace88e133c0c`.
The seccomp policy permits filesystem mutations that Landlock does not mediate.
The connector delegates authority over names whose targets it resolves again after validation.
The implementation does not establish a closed inventory of inherited descriptors.
These are containment defects after compromise of the native process.
The fact that the process runs our own code does not remove that threat.
The Lean grant system constrains requests processed by the intended program.
It does not constrain arbitrary native execution after a runtime, FFI, or memory-safety failure.

I fetched `origin/main` on hbox and found the reviewed commit at its tip.
I read `CHARTER.md`, `CLIENT-48`, the supplied design, the sandbox implementation, the relevant launcher and supervisor paths, the C connector client, the confinement tests, and the generated writer service.
I inspected the previous Linux platform implementation to establish what bwrap actually supplied.
I inspected the installed Landlock and seccompiler crate implementations for the pre-exec path.
This is a source review, not an executed exploit report.
I made no repository changes and ran no builds or attack probes.
The brief specifies ABI 6 for the target.
The design and CLIENT-48 record their measurements on ABI 5.
The implementation accepts ABI 3 and treats newer protections as best effort (`sandbox/src/linux.rs:77–82,195–205`).
Those are three different security profiles.

The child applies the restrictions before `execve`, not in the writer's `main` function (`sandbox/src/linux.rs:499–529`).
The ELF loader and Lean runtime therefore start under the restrictions.
Fresh ordinary file opens outside the Landlock read and write grants are denied.
The minimum ABI includes truncate mediation.
The seccomp filter rejects socket creation and direct `connect`.
It rejects process creation through `fork`, `vfork`, and `clone` without `CLONE_THREAD`.
It rejects `ptrace`, `process_vm_readv`, `process_vm_writev`, `pidfd_getfd`, namespace entry, mount operations, BPF, keyrings, perf events, userfaultfd, and SysV IPC.
The installed filters and no-new-privileges survive exec.
These controls prevent many direct routes from a compromised writer to unrelated file contents and processes.
They do not protect the writer's own Store against the writer.
They do not preserve application-level grant checks after native compromise.
They do not make the permitted upstream services safe against malicious protocol requests.

The first loss from bwrap is the private filesystem view.
The previous implementation constructed a new root containing explicit bind mounts.
The replacement leaves the outer service's namespace visible.
The child can probe ungranted names with `stat`, `readlink`, `access`, and `O_PATH` opens where ordinary DAC permits traversal.
It cannot necessarily enumerate an ungranted directory.
The distinction matters because a guessed pathname remains usable for operations outside Landlock's mediation.
The design's claim that this loss concerns only metadata disclosure is false.
The loss matters after compromise of our own code.
Systemd's `ProtectHome` and inaccessible mounts compensate only for paths they actually mask.
`ProcSubset=pid` does not remove `/proc/self`.

The second loss is the previous read-only mount enforcement.
The bwrap implementation used `--ro-bind` for the program, read grants, and exec grants.
The replacement grants Landlock read rights without making those filesystem objects read-only.
`linux.rs:274–276,396` allows `fchmod`, `fchmodat`, `utimensat`, and x86-64 `chmod`.
Landlock leaves permission and timestamp changes outside its filesystem access controls. [Landlock API](https://docs.kernel.org/userspace-api/landlock.html#filesystem-flags)
Consequently, a compromised child can call `chmod(path, 0000)` on an otherwise ungranted file that its UID owns and can reach on a writable mount.
It can change that file to mode `0666` instead.
The latter exposes the file to other processes without making it readable to the confined child itself.
It can alter timestamps outside its write grant.
The ordinary ownership and read-only-filesystem checks still apply. [chmod semantics](https://man7.org/linux/man-pages/man2/chmod.2.html)
This makes same-UID sibling state and launcher-owned files concrete targets.
`RestrictSUIDSGID` does not forbid ordinary permission changes.
An outer `ProtectSystem=strict` helps outside its writable exceptions.
A service-wide writable exception does not isolate children from one another inside that exception.
This loss matters for integrity and availability even when nobody executes foreign source code.

The third loss is the private PID namespace supplied by the old `--unshare-all` invocation.
`setsid` creates a session, not a PID namespace.
The new filter compensates for direct outgoing signals by restricting `kill` and `tgkill`.
It does not hide host process identifiers.
The broad `fcntl` permission supplies another signal mechanism.
`F_SETOWN`, `F_SETSIG`, and `F_SETFL(O_ASYNC)` arrange kernel-generated signals to a selected process subject to UID permission checks. [fcntl signal ownership](https://man7.org/linux/man-pages/man2/F_SETOWN.2const.html)
Those signals do not execute the child's filtered `kill` syscall.
On the accepted ABI 3–5 profiles, the claim that seccomp alone confines all signals to self is therefore false.
ABI 6 signal scoping is the additional boundary intended to close cross-domain signaling.
The existing signal test exercises `kill -0`, not asynchronous I/O signaling (`sandbox/tests/confine.rs:267–298`).
This loss matters to a same-UID supervisor and other same-UID tenants.

The fourth loss is the old network namespace.
The new filter removes fresh sockets instead of providing an isolated network stack.
That blocks ordinary direct network use with the intended descriptor inventory.
An inherited or received socket remains a route to the network it already reaches.
`RestrictAddressFamilies=AF_UNIX` restricts socket creation rather than revoking inherited sockets.
The fifth loss is the old IPC namespace.
The new syscall and filesystem rules block the principal fresh SysV and POSIX shared-memory routes.
Neither replacement erases shared objects already represented by descriptors.
These losses matter chiefly when descriptor hygiene fails or a permitted peer delegates additional authority.

The sixth loss is bwrap's user-namespace setup and explicit `--cap-drop ALL`.
UID mapping is not equivalent to assigning each tenant a different host UID.
The replacement does not change credentials or explicitly clear existing capabilities.
No-new-privileges prevents privilege gain through exec rather than removing privileges already held.
The empty capability bounding set in the transient test unit supplies a deployment condition that `sandbox::command` does not establish.
This loss is small for a correctly configured unprivileged service with no capabilities.
It matters when the API is reused by a privileged launcher.

The seventh loss is a separate minimal device filesystem.
The old code used `--dev /dev`, so its device tree was not literally empty.
The replacement grants `/dev/null`, `/dev/zero`, `/dev/random`, and `/dev/urandom` through Landlock (`linux.rs:68–75,208–218`).
ABI 5 adds device-ioctl mediation.
That mediation does not revoke rights on already-open device descriptors. [Linux 6.12 Landlock limitations](https://docs.kernel.org/6.12/userspace-api/landlock.html#ioctl-support)
An inherited terminal or device is therefore a different authority from those four fresh opens.
This loss matters to interactive launches and accidental descriptor inheritance.
Systemd's `PrivateDevices` supplies a separate device view for the service when enabled.
The remaining UTS and cgroup namespace losses primarily expose host identity and topology under this syscall policy.
Neither old bwrap namespaces nor the replacement impose CPU, memory, or disk quotas by themselves.

Landlock is not a complete filesystem-operation firewall.
The other documented gaps include `chown`, xattrs, locking, directory changes, and descriptor controls.
This filter denies chown and xattr syscalls but admits the chmod, timestamp, locking, and descriptor-control families.
Its general `ioctl` permission exposes regular-file, filesystem, and socket ioctl interfaces even on ABI 6.
The device-specific Landlock right is not a command allowlist for every ioctl target.
The distinction between already-open objects and fresh opens also applies to ordinary read and write access. [Landlock descriptor rights](https://docs.kernel.org/userspace-api/landlock.html#rights-associated-with-file-descriptors)

The `/proc` claim needs correction.
Landlock does not explicitly mediate every object reachable through procfs magic links.
Pipes and internal kernel objects reached through `/proc/<pid>/fd` or `/proc/<pid>/ns` have documented exceptions.
Landlock also imposes a domain-hierarchy restriction on ptrace-style access. [Linux 6.12 special filesystems](https://docs.kernel.org/6.12/userspace-api/landlock.html#special-filesystems)
It is false that Landlock has no ptrace protection.
This implementation additionally denies the direct ptrace syscall family.
`readlink /proc/self/fd/N` discloses descriptor targets without a directory-listing grant.
Reopening a regular file through a magic link does not automatically bypass Landlock's check on the resulting file.
Direct use of a leaked readable or writable descriptor needs no reopening at all.
An `O_PATH` descriptor supplies naming and metadata authority rather than ordinary file-content access. [O_PATH semantics](https://man7.org/linux/man-pages/man2/open.2.html)
The absence of a `/proc` rule does not establish the absence of `/proc` authority.

ABI 6 scopes abstract AF_UNIX socket destinations.
It does not add pathname AF_UNIX connect mediation.
Pathname AF_UNIX resolution is a later Landlock feature, introduced at ABI 9. [Landlock filesystem rights](https://docs.kernel.org/userspace-api/landlock.html#filesystem-flags)
The current seccomp filter denies `connect`, `bind`, `listen`, `accept`, and `accept4` regardless of family.
It allows addressed `sendto`, `sendmsg`, and `sendmmsg` without argument restrictions.
The intended connector returns stream sockets, so it does not itself provide an unconnected datagram endpoint.
A leaked AF_UNIX datagram descriptor changes that conclusion.
On ABI 6, abstract destinations receive scope checks, but pathname destinations do not receive the missing Landlock pathname check.
An inherited connected network descriptor also retains its existing communication authority.
The socket-inventory premise is part of the security boundary.

The combined seccomp policy is an actual syscall allowlist (`linux.rs:453–482`).
The first filter is a four-entry denylist returning `ENOSYS` for clone3 and io_uring.
The second filter returns `EPERM` for every unlisted syscall.
Composing them does not turn the final policy into a denylist.
Seccompiler emits an architecture check before its syscall comparisons.
Unlisted syscall numbers remain denied, including x32-numbered calls that do not match the native entries.
The problem is the breadth of arguments within allowed syscall numbers.
The kernel documentation distinguishes syscall filtering from a complete sandbox. [Seccomp design](https://docs.kernel.org/userspace-api/seccomp_filter.html)
Chromium likewise separates resource isolation from kernel attack-surface reduction. [Chromium sandbox design](https://chromium.googlesource.com/chromium/src/%2Bshow/719a425c/docs/linux_sandboxing.md)

`prctl` is allowed without an option check (`linux.rs:322`).
The child can clear its parent-death signal with `prctl(PR_SET_PDEATHSIG, 0)`.
The source comment that every setup property can never be undone is false. [Parent-death signal API](https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html)
`fcntl`, `ioctl`, `setsockopt`, and `arch_prctl` also expose whole operation families without a demonstrated runtime need for each operation.
The clone rule checks only the presence of `CLONE_THREAD` rather than an approved flag set.
That condition does prevent ordinary process forks.
It is not a thread-count limit.
`mmap` and `mprotect` permit executable mappings in the inner policy.
`execve` remains available for the lifetime of the process.
An allowed loader or interpreter can consume readable bytes as program input without an execute check on those bytes.
Overlapping write and execute grants also accumulate rights because the policy does not reject that overlap.
The written-file test checks a direct `execve` failure rather than code provenance (`sandbox/tests/confine.rs:224–264`).
Outer `MemoryDenyWriteExecute` and `NoExecPaths` add restrictions that must be attributed to the outer profile.
They do not prove that writable data cannot influence execution in an already-compromised process.

The absent syscall families are mostly deliberate restrictions rather than omissions to fix.
There is no reason to add process creation, socket creation, ptrace, mount, or io_uring support for this writer.
There are compatibility omissions such as `fchmodat2`, newer futex interfaces, and wait-family calls.
Their denial is not a security defect.
A runtime upgrade that starts using them requires a targeted compatibility decision.
Returning `EPERM` for an optional new interface can prevent libc fallback that expects `ENOSYS`.
The existing clone3 treatment recognizes that distinction.

The `openat2` finding is real for systemd 256.
Its `RestrictSUIDSGID` implementation rejects that syscall with `ENOSYS` because the mode and flags reside in an indirect structure that classic seccomp cannot inspect. [systemd 256 implementation](https://raw.githubusercontent.com/systemd/systemd/v256/src/shared/seccomp-util.c)
The replacement explicitly allows `openat2` in its inner filter (`linux.rs:261`).
An inner allow cannot override an outer denial.
Landlock does not require callers to use `openat2` for filesystem mediation.
The recorded workload therefore avoids this compatibility failure.
The broader claim that bwrap 0.12 inherently requires `openat2` is inaccurate.
Upstream 0.12's `safe_openat` falls back on `ENOSYS`, `EINVAL`, or `EPERM` when the fallback is compiled in.
The fallback is compiled out when its assumed minimum kernel is at least 5.6. [bwrap 0.12 source](https://raw.githubusercontent.com/containers/bubblewrap/v0.12.0/safe_openat.c)
The observed package failure does not establish the absence of an upstream fallback.
The namespace and mount restrictions remain independent reasons that the previous invocation cannot run inside the stated unit policy.

The connector provides a capability to request connections from one broker.
Each returned connected socket is an object reference.
The process as a whole is not in Capsicum-style capability mode.
Capsicum removes ambient global-name lookup and constrains descriptor-relative traversal. [Capsicum paper](https://www.cl.cam.ac.uk/research/security/capsicum/papers/2010usenix-security-capsicum-website.pdf)
This child can still issue absolute-path `openat` calls.
It can still traverse `..` for operations the remaining kernel checks permit.
Landlock, not the dirfd, blocks a fresh content open outside its grants.
The metadata-mutation gap survives that traversal.

The brief's directory-descriptor premise is not implemented in the reviewed code.
The launcher opens `O_PATH` descriptors to construct Landlock rules.
It does not pass a state directory descriptor to the writer through the connector.
The connector's only reply object is a connected AF_UNIX stream socket (`linux.rs:589–637`).
The resident receives filesystem paths in argv (`launcher/src/lib.rs:168–180`).
The writer receives a Store pathname from `nd-supervise`.
The generated writer service has no connect grant, so its external protocol transport is the supervisor's pipes rather than the connector.
This is pathname access under an LSM policy, with socket brokering added.

The connector compares request bytes against the original and canonical names captured at launch.
It does not accept an arbitrary child-selected path.
It then calls `connect` on the stored canonical pathname afresh.
The socket-type, owner, mode, and ancestor checks run only during initial policy resolution (`sandbox/src/connect.rs:22–59`).
No corresponding validation or peer-credential check occurs in `dial`.
A replacement symlink at an approved name can redirect the broker to another socket that the launcher can reach.
This attack requires authority to replace that name or an ancestor.
A different-UID tenant excluded by the ancestor permissions does not obtain that authority merely by knowing the pathname.
A same-UID unconfined sibling or an overlapping writable grant is a relevant attacker.
The removed overlap refusal makes the latter a policy configuration that the sandbox API now accepts.
A sandboxed child cannot bind a new socket, but it can create a symlink inside a write grant.
The broker performs the redirected connection outside the child's Landlock domain.
The connection therefore cannot rely on the child's pathname or abstract-socket restrictions to validate the broker's destination.
Restart support requires replaceable server instances.
It does not require trusting an unchecked replacement name.

An allowed peer can pass further descriptors through the returned socket because `recvmsg` remains allowed.
The child can also delegate descriptors with `sendmsg`.
That is normal capability delegation, but it makes the allowed peer part of the authority boundary.
The receiving server observes the connector process's connection credentials rather than a fresh connection made by the child.
UID checks remain equivalent only while launcher and child share the intended credentials.
PID-based attribution is different.
The connector also lacks a per-child request-rate limit.
Its response send is blocking.
A child that stops receiving can strand the connector thread while keeping its endpoint open.
The C client's connector request ignores its advertised connection timeout (`Host/c/sock.c:94–118,139–146`).
These are availability and accounting problems rather than arbitrary-path acceptance.

The ordering prevents writer request parsing before confinement.
`nd-supervise` spawns the confined writer before it binds the public listener (`client/src/bin/nd-supervise.rs:111–139`).
The forked child has one surviving thread when it installs its per-thread filters.
Subsequent threads inherit those restrictions.
There is no need for TSYNC against nonexistent sibling threads at that point.
The parent still parses launch frames, resolves policy paths, inspects executables, and constructs rules before the child is confined.
The launcher is therefore part of the trusted computing base.
The connector continues processing untrusted child messages in that launcher after launch.

Pinning an inode after validation does not make validation atomic.
`resolve` canonicalizes strings before `ruleset` opens them (`lib.rs:290–360`; `linux.rs:180–227`).
An attacker who controls a path component can replace it between those operations.
`ruleset` even obtains the file-versus-directory classification with a separate `p.is_dir()` lookup after opening the rule descriptor.
The interpreter parser opens the executable more than once.
An inode pin prevents a later rename from retargeting that particular grant.
It does not freeze the inode's contents or all descendants of a granted directory.
Trusted immutable package directories and protected policy roots are necessary assumptions here.

The hidden-path validator contains a separate deterministic bug.
Its overlap predicate ignores every allowed path equal to `/` (`sandbox/src/lib.rs:347–352`).
The comment justifies a macOS runtime-floor exception for root-directory listing.
The code applies the exception to Linux and to explicit recursive policy grants.
A policy with `read: ["/"]`, a named executable, and a hidden subtree passes this check.
Linux then receives a recursive read rule for `/`.
The hidden declaration does not become a Landlock deny rule.
The same predicate also mishandles an explicit recursive root grant on macOS.
Automatically discovered interpreter grants are absent from the hidden-path comparison.
These defects invalidate the claim that every policy overlapping hidden state is refused.

The child setup does not close every inherited descriptor except an explicit allowlist (`linux.rs:499–584`).
It intentionally clears CLOEXEC on the connector.
Other descriptors survive according to their existing CLOEXEC flags and the caller's stdio configuration.
Rust's normal CLOEXEC defaults reduce accidental leakage but do not establish a sandbox invariant for arbitrary callers.
The writer inherits stderr.
The resident launch inherits stdout and stderr (`launcher/src/bin/grain-launch.rs:238`).
Any inherited writable file, terminal, or connected socket carries authority beyond the path policy.
The Landlock crate's successful restriction path uses prebuilt state and syscalls.
The local error paths still construct heap-backed `io::Error::other` values after fork (`linux.rs:506,514,517,519,528`).
The pre-exec safety argument must cover failure paths as well as success.
A post-fork allocator deadlock is a failed launch that can hang instead of returning a refusal.

A compromised writer can destroy or corrupt every object in its granted Store.
It can fill the filesystem through permitted writes and fallocate.
It can consume its available memory and CPU.
It can create threads until an external limit intervenes.
It can congest allowed services through legitimate descriptors.
The chmod gap extends damage to reachable same-UID files outside that Store.
The ABI 3–5 signal gap extends damage to same-UID processes.
A different-UID tenant remains protected by DAC where no shared writable path or delegated service bridges the boundary.
The shared Linux kernel remains exposed through every permitted syscall family.
Application fuel and grant bounds do not constrain a compromised native runtime.
The transient test supplies `MemoryMax=256M` and `TasksMax=64`.
The generated writer service itself contains only `NoNewPrivileges=yes` from the discussed hardening set (`deploy/units/linux/nd-host-serve.service`).
The stated production drop-ins must therefore be treated as deployment inputs rather than properties of that generated service.
The transient test does not include `NoExecPaths`.
Its successful round trip does not verify the brief's exact production profile.

macOS uses a separate Seatbelt policy through `/usr/bin/sandbox-exec` (`sandbox/src/lib.rs:395–447`).
It does not use the Linux connector.
It allows ordinary connects to listed pathname sockets through `network-outbound` rules.
Its filesystem rules have different mediation semantics from Landlock.
Its `file-write*` rule is broader than the individual Linux write-right selection.
Linux ABI evidence does not validate those rules.
The profile denies process fork by default.
It permits execution of the named program and exec subpaths.
Those execute rules still do not establish a general code-provenance guarantee for interpreters.
The implementation supplies no Linux-style session or parent-death setup in this branch.

The macOS profile builder has a concrete input-encoding defect.
It interpolates the original connect path directly into quoted SBPL (`lib.rs:439–443`).
`connect::entry` validates a canonical parent and socket metadata.
It does not reject quotes or backslashes in the socket basename or validate the original spelling as a profile string.
The general `canonical` string check therefore does not protect this interpolation.
A policy-supplied socket name can introduce SBPL syntax instead of remaining a literal name.
Policy-injection reachability depends on who chooses accepted connect paths.
The shared sandbox API does not enforce a safe encoding boundary.
This defect must be fixed before describing macOS connect policy as exact.
macOS also lacks the Linux `SO_PEERCRED` implementation in `sandbox/src/custody.rs:196–202`.
That is an explicit unsupported path, not cross-platform authentication equivalence.

The first change I insist on is a syscall policy that closes Landlock's missing mutation and control operations.
Deny pathname chmod and timestamp changes in the writer profile.
Move any indispensable metadata operation behind a narrow broker over validated objects.
Allow only demonstrated `fcntl`, `ioctl`, and `prctl` operations.
Refuse changes to the established parent-death signal.
Exclude asynchronous signal ownership and notification operations unless their targets are constrained.
Restrict clone flags to the runtime's actual thread-creation contract.
Add negative tests that target a same-UID sibling outside the write grant through direct syscalls.
The tests must cover chmod, timestamps, asynchronous I/O signals, and parent-death-signal clearing.
The existing read, fork, direct-exec, and kill tests do not cover these claims.

The second change I insist on is a sealed authority inventory at launch and at broker delegation.
Close all inherited descriptors except explicit stdio and connector entries.
Validate the types and intended rights of those retained descriptors.
Build filesystem grants from descriptors whose identity is checked without returning to mutable names.
Fix the recursive-root hidden-path exemption.
Include implicit interpreter grants in policy validation.
Protect connector directories against every confined principal.
Bind each reconnect to that protected namespace and validate the resulting peer's expected credentials.
Do not treat a second pathname stat before connect as a race-free fix.
Bound connector requests and response waits.
Encode macOS policy strings from validated canonical values.
Add adversarial tests for leaked descriptors, ancestor replacement, approved-name symlink replacement, root grants, and quoted socket names.

The third change I insist on is an explicit production confinement profile whose prerequisites are enforced.
Require ABI 6 for the production profile described in this brief.
Report the active ABI and enforcement result rather than silently equating partial enforcement with the target profile.
Make an unprivileged identity with no retained capabilities an enforced launch condition.
Make the required systemd mount restrictions and finite resource limits part of the deployed service definition.
Include a disk-space or quota boundary because `MemoryMax` does not bound permitted file writes.
Run the hostile syscall probes through the actual writer launch path under those exact unit properties.
Include the actual `NoExecPaths` policy in that run.
Test the standalone sandbox separately so an outer denial cannot disguise an inner-policy defect.
Describe the resulting guarantee as containment of named resources and operation families.
Do not describe it as inability to run attacker-controlled instructions.

The one implementation I would delete is the launcher's handwritten generic ELF/shebang interpreter discovery (`sandbox/src/linux.rs:116–175`).
The production writer is a known native binary.
Its loader requirement belongs in an explicit package/runtime manifest.
The current parser processes executable-controlled lengths in the more privileged parent.
Its ELF program-header allocation is not capped to a small format bound.
A zero entry size reaches `chunks(0)` after a zero-length table read.
The parser also introduces repeated pathname opens before confinement.
An explicit immutable runtime manifest removes that parser and makes the implicit execute authority reviewable.

DONE 2026-10-27. [Review written](/Users/ember/dev/redregg/work/critiques/CRIT-SANDBOX.md). Reviewed 7ec94566beb370053d81f1d0f079ace88e133c0c. No landings.
Required before calling the writer confined: close the syscall gaps, seal descriptor and connector authority, and enforce the exact production profile.
