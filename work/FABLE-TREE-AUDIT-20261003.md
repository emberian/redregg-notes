# Whole-tree audit of Mini: census and subsystem findings

From: Claude (Fable), at ember's request. 2026-10-03. Follows
`FABLE-REVIEW-20261003.md`, which covered Objective Bend and the last 31 hours
of commits. This file covers everything else in `minidregg` at `fe60a569`.

Part 1 is a mechanical census I ran myself. Part 2 collects the deep reads of
each older subsystem as they come in, with what I re-verified marked.

## Part 1: census

### The gates, then and now

`scripts/local-gates.sh` defines thirteen gates. Six of them need no build. I
ran those against three trees: an archived copy of `cfaa2e5d` (the last commit
before the reviewed range, 2026-10-01 23:58), an archived copy of `cace986a`
(2026-10-03 04:33), and current main.

| Gate | `cfaa2e5d` | `cace986a` | `fe60a569` (now) |
| --- | --- | --- | --- |
| proof hygiene | PASS (961 files, 360 pinned footprints) | FAIL | FAIL |
| build closure | PASS, 914 of 914 modules rooted | FAIL, 4 unrooted | FAIL, 170 of 1,259 unrooted |
| host closure | PASS, closure equals pin (439 modules) | FAIL, 2 entered | FAIL, 45 entered |
| import tiers | PASS | FAIL | FAIL, 7 edges |
| host operations | not run | not run | PASS |
| exports | not run | not run | PASS (16 exports) |

So 31 hours ago the tree passed its own static gates, and the gate runner is
well designed (every gate runs, a partial run can never read green). The gates
went red during the last day's integration and stayed red. The build-requiring
gates (`lake-build`, `hyp-ledger`, `cold-start`, `prover-glue`, `rust-tests`,
`journey`) I did not run; whether main builds at all is unknown.

The 170 unrooted modules: 85 in `Compiler/`, 33 in `Kernel/`, 22 in `Theory/`,
18 in `Host/`, 12 in `Assurance/`. 115 are Bend files, 18 are Simplex files, 37
are neither (bounded Nock machine, oblivious network, portable continuation,
private backend boundary, joint receiver pieces, `CheckedCarry`).

### Continuous integration

GitHub Actions runs `scripts/local-gates.sh` on every push (`.github/workflows/build.yml`).
I pulled the summaries of every completed run (80 runs since 2026-10-01; 35 of
them reached the summary line, the rest were cancelled or failed early):

| Gate | PASS | FAIL | Note |
| --- | --- | --- | --- |
| host-operations | 22 | 0 | |
| hygiene | 21 | 14 | red since the bare `#print axioms` landed |
| lake-build | 14 | 21 | last green 2026-10-03 09:29 at `3edf7ee0`; red since |
| cold-start | 35 | 0 | passes vacuously when the Host binary is absent: `/usr/bin/time` on a missing file reports 0 CPU and 1 MB, and the script only checks upper bounds (`scripts/check-host-cold-start.sh:25-35`) |
| hyp-ledger | 1 | 34 | the instrument's own self-test fails in CI ("planted refuted family: FAIL", "scan deleted: FAIL"); it has never functioned there |
| drift | 35 | 0 | |
| prover-glue | 0 | 35 | has never run in CI: "no default toolchain configured" (the script does not use `lake env`) |
| build-closure | 3 | 32 | |
| host-closure | 7 | 28 | |
| import-tiers | 3 | 32 | |
| exports | 35 | 0 | |
| rust-tests | 0 | 35 | has never been green in CI |
| journey | 0 | 35 | has never been green in CI |

CI has never passed. The red count went from 3 to 9 of 13 over two days. At
`fe60a569` the Lean build itself fails: `Kernel/ResourceTransaction.lean:20`
imports `Kernel.BendNativeRun` and `Kernel/DeclaredResourceController.lean`
imports `Kernel.BendPreparedOutput`, and neither file was committed
(`fd8d3dfc`, "Compose signed Bend execution … (WIP)"). Because
`ResourceTransaction` is the core transaction module, every receiver that
imports it fails too. The missing files arrive at `b627a442` on `origin/main`
(pushed after my review range), so the build may recover there; the other
eight red gates do not.

Three of the thirteen gates (`cold-start`, `hyp-ledger`, `prover-glue`) are
not measuring anything in CI, two by their own failure and one by passing on
nothing. "Gate the gates" is one of the sixteen laws.

The README at `fe60a569` still says "`lake build Minidregg` builds green (9,294
jobs)" and "815 library modules, every one imported from the `Minidregg`
umbrella (`scripts/check-build-closure.sh` fails otherwise)". On `origin/main`
the README has since been rewritten (`d2b68997`, "Rewrite README around the
shared world") and no longer makes those claims; the claims audit in Part 2
covers the new text.

### Growth

Tracked bytes on main, evidence files excluded:

| Date | Lean | Rust | Shell |
| --- | --- | --- | --- |
| 2026-08-08 | 1.1 MB (51 files) | 0 | 0 |
| 2026-08-15 | 9.9 MB (474) | 0.3 MB | 0.1 MB |
| 2026-09-25 | 13.4 MB (623) | 0.5 MB (40 files) | 0.2 MB |
| 2026-09-28 | 15.9 MB (864) | 3.9 MB (151) | 1.0 MB |
| 2026-10-02 | 18.6 MB (964) | 5.4 MB (204) | 1.9 MB |
| 2026-10-03 now | 22.8 MB (1,324) | 10.9 MB (439) | 2.7 MB |

The Rust layer is eight days old and doubled in the last 31 hours. Library
modules went from 914 to 1,259 in the same 31 hours.

### Theorem shapes

A classifier over every `theorem` in the library directories, by the shape of
its proof: `rfl`, a bare `decide`, a one-line `simp`, a one-line term, three
lines or fewer, or longer. Proof shape is a triage signal only. A `decide` on a
hostile fixture is a legitimate tooth, and a long proof can be vacuous.

| Directory | Files | Lines | Theorems | One-liners | Longer than 3 lines |
| --- | --- | --- | --- | --- | --- |
| Theory | 129 | 57,047 | 2,764 | 41.8% | 1,057 |
| Selvage | 150 | 77,013 | 2,858 | 25.8% | 1,609 |
| Pred | 9 | 4,052 | 231 | 40.3% | 118 |
| Kernel | 437 | 141,306 | 4,518 | 46.8% | 1,781 |
| Compiler | 287 | 82,983 | 3,165 | 43.3% | 1,236 |
| Assurance | 146 | 58,522 | 2,313 | 50.1% | 739 |
| Host | 92 | 28,428 | 118 | 50.8% | 44 |
| All | 1,252 | 449,789 | 15,980 | 41.9% | 6,584 |

The same classifier on the tree of 31 hours ago gives 13,253 theorems and 42.1%
one-liners. The last day did not change the proportion. What it changed is
volume and the gates. Selvage stands apart from everything else.

`#assert_axioms` lines went from 939 to 2,212 in the same 31 hours.

### What the running Host reaches

From the project's own host-closure table (current tree):

| Library | In `Host.Main` closure | Built by the gate | Tracked |
| --- | --- | --- | --- |
| Theory | 67 | 108 | 130 |
| Kernel | 325 | 401 | 434 |
| Compiler | 120 | 202 | 287 |
| Selvage | 12 | 151 | 151 |
| Assurance | 0 | 135 | 147 |
| Host | 61 | 75 | 93 |

Twelve of the proof system's 151 modules are in the deployed executable.

### The public record

The repository is public and has a project site. The README says, in the
present tense: 878 Lean files, 815 library modules "every one imported from the
`Minidregg` umbrella (`scripts/check-build-closure.sh` fails otherwise)", every
`#print axioms` pinned "(`scripts/check-proof-hygiene.sh` fails on a bare
one)", and "`lake build Minidregg` builds green". On main today there are 1,324
Lean files, 170 unrooted modules, and both named scripts fail. A full claims
audit is in Part 2.

### Secrets

`gitleaks` over 2,878 commits of history, redacted: 164 hits, none of them a
live credential by my reading. 112 are already-redacted key fingerprints in a
committed sshd log whose client addresses are all loopback. The rest are
digests, test vectors and one TLS test-fixture private key
(`native/spk-host/tests/fixtures/browser-proxy-test.key`). Host-identifying
material is present by design: `deploy/shell/FRIENDS.md`, `OPERATOR.md` and
`deploy/pay/enrol.json` each name one public IPv4 where invited users connect
by SSH, and about 700 evidence files contain `/home/ember` paths.

## Part 2: subsystem deep reads

Eight readers, one per slice. For each I re-read the headline findings against
the source before recording them; items marked (verified) are those.

### `native/resource-client`: the older core, cryptography and custody

Reader covered `private.rs`, `roomkey.rs`, `keys.rs`, `key_service.rs`,
`hiding.rs`, `channel.rs`, `relay.rs`, `proxy.rs`, the signing paths in
`main.rs`, and the pre-existing payment code. Items marked (verified) I
re-read.

**Primitives are library code and pinned.** Ed25519 and X25519 from dalek,
XChaCha20-Poly1305, cSHAKE and KMAC from `sha3`, Argon2id for the key cache,
ML-KEM from aws-lc-rs, rustls for the one TLS client. All dependencies are
`=`-pinned and none are git sources. Hand-written: SP 800-185 framing (37 lines,
checked against a Lean vector), a bignum for the Host's base-255 naturals,
base64 and SSHSIG framing, and 22 hex codecs. Randomness is `/dev/urandom`
everywhere, with no seeds from time or pid. The private-room scheme is sound in
its parts: every KDF input is length-prefixed with a per-purpose customization
string, the X25519 key is derived from the seed rather than reused, wraps are
ECIES with contributory checks and full AAD, envelopes use random 192-bit nonces
with a commitment re-verified on open, and sizes are bucketed to 64 bytes.

**The composition has three holes, all against an active operator.**

1. **Proxy-mode clients sign bytes the box chose** (verified,
   `main.rs:1163-1194`, `1591-1598`). In `--remote` mode the client sends
   `author`, `inspect`, `signatures` and `assemble` to the operator's Host
   over the socket (`workspace_host` is the empty path in that mode,
   `workspace.rs:295-305`), then signs the headers that come back with no
   local check that they encode the user's intent. The deploy README promises
   the operator "holds no key that signs as you". It holds no key; it chooses
   what the key signs. A compromised box can have a friend sign a delegation
   of all their capabilities on their next `submit`. Fix: run the pinned Host
   image locally for author, inspect, signatures and assemble, and send only
   prepare, submit, challenge and query to the box.
2. **Wraps carry no founder signature, so a served wrap at epoch N+1 captures
   the room** (verified, `roomkey.rs:255-275`, `326-329`, `624-636`).
   `wraps_in_view` accepts any atom of the wrap schema in the served view;
   `current_epoch` is the maximum epoch any wrap names; `sync` opens every wrap
   addressed to the member's public X25519 key and inserts the result. The
   operator mints a key, writes one wrap per member at `max+1`, serves the
   view, and every writer seals under the operator's key from then on. The
   Lean `keysLaw` governs what the kernel admits from subjects, not what an
   operator serves. This is distinct from the first-pass unsigned-record
   finding and worse.
3. **No epoch monotonicity on the client** (verified, `roomkey.rs:657-664`):
   `current_key` seals under the served view's epoch, never the local ring's
   highest. Serving the pre-kick view makes everyone seal under the key the
   kicked member still holds.

Also: the envelope AAD binds room, cell, address and epoch but not revision, so
a document edit can be rolled back to an earlier ciphertext at the same atom
id (`private.rs:294-305`); the primary signing-key loader `read_secret`
(`main.rs:850-860`) checks nothing about ownership or mode and does not zeroize,
while four other loaders in the crate do; `MINI_KEYCACHE_PASSPHRASE` is
inherited by the spawned Host and ssh; `docs/PRIVATE-CELL.md` documents a wrap
atom layout the code does not use, and `PRIVACY.md`, cited from four places,
does not exist.

Promise versus delivery, as the reader tabulated it: "not a key, not a
plaintext" holds against a passive operator and fails against an active one
(holes 2 and 3); "cannot move an envelope to another cell, address or room"
holds except for same-address revision rollback; "a removed member gets nothing
new" fails under hole 3; the hosted-invitee refusal does not fire in proxy mode
because it reads a list that exists only on the box.

Payments: the older `pay.rs` computes no amounts itself (they come from the
Lean tariff view), the watcher requires `finalized` from at least two
endpoints, and the v1 memo binds mint, address and key but not amount or payer,
so a memo is replayable but only credits its own key.

### The live attack surface (the box with friends' keys on it)

Reader traced every entry point from the network edge inward, using the
deploy wiring in `~/dev/dregg-infra/edge/mini/` (sshd drop-in, units,
install script) as well as this repo. Items marked (verified) I re-read.

**Edge map.** SSH on port 22 under `Match User mini` with a root-owned
`AuthorizedKeysFile`, no `ForceCommand`, per-key `restrict,pty,command=`
lines, all forwarding off (verified, `50-mini.conf`). Two key kinds: hosted
shell (one `mini shell --line` per command) and proxy (raw frames to the
public socket, or the credential key service). A public unix socket relay and
an operator socket, both mode 0600. An enrollment-bootstrap HTTP listener on a
private address behind Caddy. A Discord interactions endpoint with
`verify_strict`, a replay cache and `env_clear`. The SPK broker as root. Every
one of these except the broker runs as the single uid `mini`.

**Findings.**

1. **Every tenant, the Store, the operator socket, the BYOK seal key and the
   sponsor key share one uid.** (verified: `install.sh:73` creates one
   `mini` user with `/bin/bash` as its shell; `transport.rs:1587-1596` admits
   any process whose uid equals the Host's to operator operations;
   `install.sh:120` gives `mini` a passwordless sudo rule.) Isolation between
   friends is the shell's argument parser, not the kernel. The motd says
   "root can read it"; the true statement is that any other friend's process
   can, one path-taking verb away.
2. **`say --operation-record ABS_PATH` creates an attacker-named file in any
   `mini`-owned 0700 directory** (verified, `chat.rs:306-310` requires only
   that the path be absolute; `fleet.rs:357` checks only that the parent is
   euid-owned 0700, then `private_file` creates the file). Friend A can squat
   `sessions/ember/requests/room-lab.json` so ember's next `room new lab`
   fails forever, or drop files into the Store's sponsor and public
   directories. The deploy README's invariant "nothing may name a path outside
   [the session home]" (`deploy/shell/README.md:93-94`) is false.
3. **`tail --discover FILE` reads an arbitrary path** (verified,
   `chat.rs:376-380`, `chat.rs:1090`). Contents are not echoed, so it is an
   existence and JSON-shape oracle over everything `mini` can read.
4. **Terminal escape injection through shared documents** (verified:
   `render/text.rs:22-24` strips only newlines; `chat.rs:1330-1338` has a
   `clip` that strips control characters, used for chat but not documents).
   A member appends an OSC 52 clipboard-write sequence to a shared document;
   whoever next runs `doc show` over `ssh -t` has their clipboard written.
5. **One Host thread with a 600-second deadline, reachable by any paying
   stranger** (reader, structure read, not timed): the self-enrollment path
   issues a proxy key automatically once a Solana payment lands, and public
   operations accept frames up to about 12 MB.
6. `job` verb names are validated on two of eight actions; the rest join the
   raw name into a path (`job.rs:205-206`). Traversal reads another session's
   file, though the later reference check stops any field from printing.
7. A paying stranger reaches a root-executed code path (`key_service` →
   `sudo` → `credential-namespace.py`). The helper itself is careful
   (symlink-safe mkdir and chown, ancestor custody walk); the problem is that
   the sudo rule belongs to the uid every tenant runs as.

**Well done.** The authorized-keys renderer (strict regexes,
content-addressed atomic replace, fail-closed), the sshd drop-in, the shell's
word syntax with no expansion, the Discord entrance, the bootstrap's HTTP
parser (duplicate headers, transfer-encoding, pipelining all refused), and the
root credential helper.

**Reader's verdict, which I share:** not with strangers' keys, today. Nothing
found lets A sign as B, but two shipped verbs already step outside the session
home and one uid holds everything. The three blockers: a uid per session with
the Store, operator socket and seal key out of reach; confine
`--operation-record` and `--discover` like every other `@FILE` and add a test
that greps the shell for `is_absolute()`; a public deadline well under 600
seconds with per-operation budgets.

### Selvage, the proof system

This is the subsystem the README leads with, and it is the best work in the
tree. The reader followed the keystone chain end to end. Items marked
(verified) I re-read.

**What is proved, in plain terms.** The number on the label comes from
`Assurance/ErrorBudget.lean:292-351`, `soundnessError_bound`: over an
independent product of four coin blocks, for a Reed–Solomon code with the
proximity parameter in the one-third unique-decoding band, the union of four
algebraic failure events is bounded by
`(t+k)·k·(n+1)/|F| + k·v·d/|F| + q(q-1)/2^{h+1} + n/|F|`. Then
`deployedBudget_secure` says that expression is at most `2^-55` at the deployed
parameters. It is interactive soundness with a lazily sampled random oracle,
not knowledge soundness, not QROM, and the bounded event is δ-closeness of the
full folded word: no term accounts for a verifier that reads `t` of `2^20`
columns.

**Genuinely strong** (reader read these, not skimmed):
`OB2_depth_composition_nonneg_proved` (`Selvage/Depth.lean:1959`, the WARP
depth-composition theorem for an arbitrary reduction and an adaptive prover),
`OB2_depth_composition_false` (`:545`, the tree refuting its own earlier
statement at `Z = ∅`), the WHIR mutual-correlated-agreement lemma for every
linear code with the paper's typo and two implicit hypotheses made explicit
(`CorrelatedAgreement.lean:325`), the hypothesis-free RS proximity gap at
`(1-ρ)/3` with the bad set computed exactly (`ProximityGapUD.lean:409-501`),
the light-client chain induction with an attained bound
(`LightClientSound.lean:520`, `LightClientGrinding.lean:455`), the sumcheck
handler laws, and `CharTwoWall.lean` with its gate. Zero `sorry`, zero
`axiom`, 652 pinned axiom footprints: all verified by grep.

**Findings.**

1. **The BCS and Fiat–Shamir theorems at "the deployed alphabet" are true of
   nothing at deployed parameters** (verified). `BindingCommitment`'s binding
   field is unconditional, so every inhabitant has an injective commit, and
   `Selvage/Commitment.lean:180-183` proves the type is empty whenever the root
   space is smaller than the word space. A 248-bit Merkle root over
   `|F|^n > 2^248` words is such a root. Thirty Selvage files take
   `S : BindingCommitment` as a hypothesis, including `accFsSound_bcs`
   (`AccRbrBcs.lean:748-751`). The tree knows this: `Assurance/SelvageV0.lean:19-24`
   replaced the carrier with an `AuthMap` reduction in the capstone. The README's
   sentence about BCS-style soundness at the deployed alphabet still describes
   the empty-carrier theorems.
2. **The two-sided budget bounds a formula, not an adversary** (verified).
   `deployedBudget_secure` and `deployedBudget_ceiling`
   (`ErrorBudget.lean:450-459`) are both `norm_num` on a record of constants.
   The README reads the lower bound as proof that the bound is not vacuously
   loose; it cannot be, since it bounds the expression and not any adversary's
   success. `soundnessError_bound` itself is instantiated only at `F_5`, where
   the budget evaluates to `133/10` (`:513`). The only sub-one numbers in the
   tree are arithmetic on formulas.
3. **Model gaps not on the label.** No query-sampling term; the grinding set is
   pre-committed before the coins (no answer-dependent queries, which is what a
   grinding adversary does); the composed sumcheck is the non-adaptive one
   (`Sumcheck.lean:227-249`) although an adaptive version exists
   (`SumcheckReduction.lean:296`); four separately quantified adversaries on a
   product space, which is the only one of these in the file's own floor list.
4. **Sponge indifferentiability is a stated `Prop`, not a theorem**
   (`SpongeIndiff.lean:1094-1100`, "STATED, not proved"); the components are
   proved and `advantage_zero_queries` is the only end-to-end theorem.
5. **The README misattributes the refutation to the paper** (verified).
   `README.md:103-105` says a published theorem's literal statement fails at a
   corner. `Depth.lean:459-464` says "The paper never meets this corner …
   Specialization 7 of Selvage/Rbr.lean … opened the hole." The refuted
   statement was the project's own transcription.
6. **The prover ledger is stale by two months** (verified). `GOAL.md:1222,1229`
   record a FRI low-degree test with 83 tests and a three-way fold agreement.
   That code was deleted on 2026-08-09 (`b297c7dd`, `19ecaef6`, `47050358`).
   `prover/src` today has sumcheck kernels, MLE and tower arithmetic, and
   cSHAKE; no FRI, no Merkle, no Poseidon2 (the Lean BCS files are
   Poseidon2-based), no transcript, no verifier. The one Lean-to-Rust
   conformance link is the `m=3` sumcheck vector.
7. **Nothing that runs verifies a Selvage proof.** Twelve modules reach the
   Host through two importers that only use `BinaryLookup` and `Commitment`;
   `Host/` references zero Selvage names; `Deployed.lean` says admission is by
   re-execution, not by proof. `website/maturity.html` states this candidly.
8. Definitional theorems still advertised: `decider_sound := Iff.rfl`
   (`Decider.lean:88-90`, verified) is listed in `Selvage.lean:37` although
   `SelvageV0.lean:53-59` retracted it as a leg. 28 Selvage hypothesis
   families are allow-listed as toothless, 8 with no pole at all. All event
   witnesses are at `|F|=5, n=4, d=2`, where every bound exceeds one.
   `Selvage/Statements.lean`, the advertised home of statement-first, is six
   lines.

The honest label would be: a mechanized interactive-soundness composition for
a WHIR-shaped accumulator at unique decoding, with an explicit formula and a
real refutation discipline, whose deployed-parameter number is arithmetic on
that formula, whose binding and query-sampling legs are open, and which no
running component consumes.

### `grain-runtime`, `spk-host` and `spk-rpc`: the older core

Reader fully read the sandbox, seccomp, spawn gate, setid filter, resident
launch, the capnp bridge, the provider gateway, credentials, and about 5,500
lines of `grain-runtime/src/main.rs` by region. Items marked (verified) I
re-read.

**What `grain-runtime` is.** The per-task controller for one agent grain: it
holds the task's custody keys and a durable `journal.json`, serves a control
socket for the SSH friend and an admin socket for the operator, and launches
one worker at a time (a Hermes ACP process under bwrap, or an allowlisted
command). Every effect on Mini goes through `mini submit` with a Lean-authored
source file. Rust decides nothing about admission and everything about
recovery, holds, settlement and what the model may ask for.

`src/main.rs` is 20,131 lines in one file: config types, about forty journal
record structs for four purse slots, validation, file primitives, a `Runtime`
with dispatch purse v2 and v3 side by side (about 3,100 lines of live twins),
receipt verification, the one path to Lean (`transition_as_with_witness`,
lines 8170-8525), MCP tool handling, the provider gateway, resource birth,
foreground tools, attach and fence lifecycle, Hermes session spawn, the ACP
loop, recovery, the serve loop with about thirty admin verbs, `main` with
twenty subcommands, and tests. It is one coherent single-threaded state
machine with features appended rather than factored. The reader's carve:
config, journal, custody primitives, one Lean-submit module, the four purses
as instances of one retained-operation state machine stated in Lean, worker,
ACP, tools, recovery, serve, CLI; delete v2.

**The resident capability boundary, stated plainly.** A prompt-injected
resident in restricted room mode can post anything it has read into its own
stream or into documents it holds a write grant for, and spend its budget;
each write is one line of the pinned `mini shell` and pays a turn first. In
unrestricted mode it also has Hermes's own shell and file tools inside the
bwrap, workspace tools, publish to operator-allowlisted targets, and
operator-pinned app routes with a fresh permit per call. It cannot reach the
host network (`--unshare-net`; the only socket is the controller's gateway,
which pins model and endpoint), read controller state or custody keys (the
launcher refuses any mount containing them), obtain the provider key (resolved
per reserve in controller memory, passed to curl on stdin with `env_clear`,
and responses are scanned for the bearer), choose a provider or payer, or send
a second provider request while one is in flight. Credentials do not appear
in journals or in `docs/evidence`.

**The sandbox, stated plainly.** bwrap with user, pid, ipc, uts, cgroup and
net namespaces, `--disable-userns`, all capabilities dropped, a sealed seccomp
allowlist passed by fd, a root-owned read-only image by fd, the app's own
`/var` by fd (task-owned, separate device, at most 16 GiB), 128 MiB tmpfs,
cleared environment, bounded manifest argv and env re-derived at spawn, bwrap
pinned by hash and inode, `execveat` on the pinned fd. The seccomp policy
denies namespaces, mounts, ptrace, bpf, io_uring, keyctl, userfaultfd, kernel
modules and the rest; `clone3` is ENOSYS. The capnp bridge exports a
`SandstormApi` with no methods (verified, `spk-rpc/src/protocol.rs:95-99`), so
every app-to-host request fails by construction. A malicious SPK cannot see
the host, reach any socket, escalate, or ask the host for anything. It can
burn its budget, fill its volume, call `sync`, and serve any HTML to the
browser. The 2026-09-30 sandbox-floor audit ran a hostile probe inside the
real sandbox with a negative control; that is the right kind of evidence.

**Findings.**

1. **A crash in the journal rename window fences the task forever**
   (verified, `main.rs:2585-2597`). `atomic_json` refuses if `journal.json.tmp`
   exists; all 157 `save()` sites go through it, including startup recovery,
   so after a power loss between write and rename every command and every
   recovery verb fails until a human deletes the file. A test pins this
   behaviour. The rename is the commit point; a leftover tmp is garbage.
2. **The resident keeps `CAP_SETUID` and `CAP_SETGID` with no namespace
   restriction** (verified, `broker.rs:1117-1121`; no `RestrictNamespaces`
   anywhere in the file). This confirms the first-pass suspicion. The resident
   is the process that parses app-controlled capnp bytes. Its own setid filter
   bounds `setresuid` and `setresgid` but says nothing about `unshare`,
   `setns` or `clone` with namespace flags. Move the uid switch into the root
   broker or a transient unit with `User=`, so the parser holds nothing.
3. **Every digest in the controller is a subprocess of `/usr/bin/openssl`**
   (verified, `main.rs:2302-2344`; 61 and 109 call sites; `sha2` is already a
   dependency). A 12 MB retained frame is piped through a child three times
   during recovery, and a host whose openssl prints differently makes every
   transition uncertain.
4. **Plain `status` dumps the raw journal to the SSH friend** (verified,
   `main.rs:17664-17669`; advertised by `deploy/grain-host/grain-ssh:18`). The
   journal embeds the whole config: key paths, credential roots, provider
   table, operator sockets. The framed client deliberately projects these away;
   the plain connector does not.
5. The hard-interrupt callback runs three `systemctl` subprocesses under the
   attachment mutex that the documentation says must never block
   (`control.rs:177-179` versus `main.rs:17552-17557`).
6. Hosted app responses get no `frame-ancestors` policy (suspected; the host
   strips app headers and adds only `no-store` and `nosniff`).
7. `reconciliation_log` is an unbounded vector rewritten and synced on every
   save.
8. No reachable panic on untrusted bytes was found in the files read; no
   double-applying retry was found (`recover` looks up before it re-settles).

**Tests.** No gate runs any `spk-host` or `spk-rpc` test (verified:
`check-journey.sh` only builds them). The sandbox argv test compares a string;
the seccomp test interprets the BPF in-crate against synthetic data; only
`resident_launch.rs:578-625` runs a hostile program in the real sandbox, and
it is `#[ignore]` and root-only, run by hand.

**Well done.** `provider.rs:1431-1509` (curl locked down, bearer on stdin,
echo check), `credentials.rs:76-108` (a `Secret` type with redacted Debug,
zero on drop, one `expose`), the empty `SandstormApi`, the async-signal-safe
spawn gate, and `gitweb_worker.rs` (path grammar, `GIT_CONFIG_NOSYSTEM`,
protocol version pinned).

### The public record: README, website, docs, deploy guides, licences

Reader extracted every checkable claim from the public documents at
`fe60a569` and gave each a verdict. Tallies: README 24 claims (9 true, 3
stale, 5 false, 4 overstated, 3 unverifiable by reading); the six website
pages 24 claims (3 true, 6 stale, 6 false, 7 overstated); `docs/README.md` 7
(4 true, 2 overstated); `docs/DEVELOPING.md` 9 (7 true, 2 unverifiable);
`docs/OBJECTIVE-BEND.md` 16 (8 true, 1 false, 5 overstated); FRIENDS.md 14
(6 true, 1 stale, 4 overstated, 3 unverifiable). Items marked (verified) I
re-checked.

**The website is a 2026-08-10 snapshot** (verified: every page has one
commit). It still calls the proof system "Loom" (renamed Selvage on
2026-08-13), links `docs/LOOM-RECOMPOSITION.md` and `D-0004-why-loom.md`
(neither exists), describes a repository carve with no `native/`, `Host/`,
`Effects/` or `Verify/`, says "native source is limited to fallible
arithmetic, transform, hash and MLE/lookup candidate compute plus generated
artifact/dispatch data" (261K lines of hand-written Rust say otherwise), and
its maturity page footnote admits "update both, or generate this page from
the ledger later". Nothing generates it and nobody has updated it in 54 days.

**README claims that are false at `fe60a569`** (each verified by running the
named gate or by grep): "815 library modules, every one imported from the
umbrella" (1,259 modules, 170 unrooted); "every `#print axioms` is pinned"
(25 bare lines in `Verify/JointDecisionRecovery.lean`); "no `#guard` in any
library module" (63 lines in six library modules, added 2026-10-02);
"`Theory/` imports only Mathlib and Theory" (seven tier edges, two from
`Theory/`); "Rust is generated glue or opaque fallible computation, never a
semantics". The README on `origin/main` was rewritten an hour later and no
longer makes the numeric claims; the website still does.

**Promises to invited users that the code does not keep.** FRIENDS.md says of
private rooms "a room whose words the node stores but cannot read" and the
template README says "not a key, not a word"; both hold only against a
passive operator (see the client cryptography section). FRIENDS.md says
"nobody can bypass [a locked law], not you as owner and not me" while the
operator holds and resets the Store, and "a law no step can satisfy is
refused on the spot" while `Host/LawSat` can return a witness for an
unsatisfiable `delta`-only law. The guide also publishes a public IPv4 in
three places and a contact handle and e-mail; OPERATOR.md adds a hostname and
absolute paths on the box.

**Objective Bend claims.** "Mini's primary authored language and live
computing environment" and "compose behavior as first-class specifications"
describe the destination, in the present tense. The one false sentence is the
oblivious-controller coverage line, already recorded.

**Licences** (verified). `LICENSE` is AGPL-3.0 and `NOTICE` says first-party
code is AGPL-3.0-or-later; both arrived in the last commit of the range.
`NOTICE:19` refers to `LICENSING.md`, which does not exist in the tree (it
appeared as an untracked file at session start and is gone now). `NOTICE:16-18` says two Hyperdocument crates "declared MIT OR
Apache-2.0" in earlier revisions; both still declare it. Four crates
(`bend-proof-entropy`, `joint-agreement-crypto`, `portable-archive`,
`prover`) have no `license` field. No source file carries an SPDX or
copyright header. The vendored fhe.rs (MIT) is not named in NOTICE. The
copyright holder named in NOTICE differs from the author name in git and on
the site.

**No generated claims ledger exists** (ATLAS law 7). The three generators in
the tree run the other way, rewriting GENERATED regions of `Assurance/*.lean`
from JSON and Rust. README numbers were computed by hand once on 2026-09-30.
`GOAL.md`, which README and the site both call "the evidence ledger", has a
"current authoritative snapshot" dated 2026-08-10 and a 2026-09-05 status
block at its head.

**Accurate and worth keeping:** `docs/evidence/2026-10-03-objective-bend.md`
(dated, pinned, every checkable item checks), `docs/DEVELOPING.md` ("what this
command does not do"), `OBJECTIVE-BEND-SURFACE.md`, `TRAFFIC-PRIVACY.md` (it
disclaims anonymity, Host-blind execution and forward secrecy; its arithmetic
checks), OPERATOR.md and the custody paragraphs of FRIENDS.md, README's "honest
gate" paragraph, and PROJECT.md's maturity ladder and public-claim gate. The
ladder and the gate are good rules that no 2026-09 or 2026-10 work applied.

**Continuous integration** is covered in Part 1: it runs every gate on every
push and has never been green.

### The deployed Kernel core: what is actually proved about the running Host

Reader traced a signed `invoke` (opcode 2) from bytes on the socket to a
durable append through the snapshot of 31 hours ago, reading
`DeclaredResourceController`, `ResourceTransaction`, the signature admission
chain, `DurableDataIntent`, `DurableCommitProtocol`, `DurableReceiverIO`,
`NativeHostReplay` and `HostRefinesWorld` in full. Items marked (verified) I
re-read.

**The life of one command.** Frame, strict decode, load the session state
(new log entries have their KMAC tags checked and are replayed through the
checkpoint executor; no signature is re-admitted on this path), dispatch on
the `SignedCall` constructor, `prepareFrom` (nonempty and distinct targets,
authority and clock loaded, content runs executed, nullifier unspent, and
the Nock claim re-executed by `Run.checkRun`), then `admit` (read guards,
per-target signature verification and policy admission, field coverage),
then the charge is decided in `preflight` and the record is appended by a
compare-and-swap on height, read back, and the receipt sealed. IO enters at
five places: Ed25519 verification, the Store's read, append and CAS, the MAC
key file, the monotonic clock for traces only, and a temp directory. There is
no randomness on the path; the clock is a signed `ClockTick` record.

**What is proved.** The pieces are real: `consumed_nullifier_refused`,
`stale_read_guard_rejected`, `execute_no_partial_data_commit`,
`install_exact_debit`, `resume_sound`, `tail_bounded`, `extendExact` (a
live-appended record is one more verified replay step),
`CheckedLeg.fields_covered`, `PreparedInvocation.run_sound`,
`checked_signer_live` with `select_revoked_refused`, and the old money
receivers' real conservation (`JobMoney.escrow_conserved` lifted to
`JobMoneyReceiver.Prepared.conserves` through the generic
`Batch.conservation`).

**What is not.** Nothing composes them over the dispatcher. `Host/Main.lean`
has 133 opcode arms calling 74 receiver entry points, and four of those names
appear in any theorem; `submitLoadedVia`, the whole opcode-2 path, has none.
The one history-level object, `NativeHostReplay.AdmittedReplay`, is a type
produced by an IO walk, not a theorem, and the ordinary session never builds
it. `Kernel/HostRefinesWorld.lean`, the file that would state "the Host
refines the world step", is outside the Host closure and its bridge ignores
its input (verified, `:1006-1011`): `Turn.ofAdmission … (_admitted : …) :=
Turn.ofIntent B H w intent`. The target theorem `host_submit_is_step` is a
code block in a comment. What it would take: a per-receiver theorem that a
confirmed `receiveLoaded` yields an admission the Store appended; `ofAdmission`
derived from the actual `Accepted` object; the `Represents` relation
tightened; the module imported by `Host.Main`.

**Findings.**

1. **Expensive-to-reject input runs before any signature check** (verified,
   `DeclaredResourceController.lean:1215-1238`: `prepareFrom` at line 1231,
   `admit` at line 1235; `checkCommandRun` at `ResourceTransaction.lean:742`).
   `prepareFrom` re-executes the Nock claim and runs content actions. The only
   pre-filter is a one-million-step sync budget (about one second). The
   session loop is sequential and refused commands are never charged. Any
   client with the socket sends well-formed commands with a near-budget
   `steps` and garbage envelopes, and each costs the Host about a second
   before the signature refusal. Verify the authority envelope first; it is
   one Ed25519 check over bytes already bound to the command.
2. **Durable rollback is undetected across restarts** (verified,
   `DurableReceiverIO.lean:137-157`, `412-420`). A log tag depends only on
   its prefix, a stored log with no checkpoint is accepted and started from
   the seed, and a checkpoint can be replaced by an older valid one. With
   write access to the SQLite file and no MAC key, truncate the log below
   height `h` and drop the checkpoint: `load` succeeds, nullifiers consumed
   above `h` are unconsumed, and the dropped records' full signed ingress
   bytes replay. Only an already-running session notices ("durable log shrank
   beneath the session", `:747`). A monotone high-water mark outside the log,
   checked in `load`, closes it.
3. **Signature verdicts enter deployed pure code as bare `Bool`s** (verified).
   `CredentialSignatureAdmission.CheckedSignature` is private, and its only
   proof field, `admitted : finish prepared.controller (.ok true) = .ok
   admission`, holds for every `prepared` (`:278-290`). It is a capability by
   module privacy, not a proposition about key, message and signature.
   `PayEnrolDecision.Verified` is `{mini : Bool, ssh : Bool}` (`:54-57`);
   `ParticipantKeyEnrollment.Accepted` carries `possessionVerified : Bool`
   with a proof that it is `true`, tied to nothing (`:399-405`). The
   `PayClaimCommand.Checked` finding from the first pass is this pattern's
   newest instance, not its first.
4. **One deployment-lifetime meter, never replenished, no per-subject lane**
   (verified, `NativeHost.lean:399-409`; `feeDebit … := 0` at
   `DeclaredResourceController.lean:1132`). Any authorized subject can spend
   the deployment's proof-work and storage lanes to zero for everyone.
5. The audit walk (`derive`) is a second dispatcher that sniffs thirty codecs
   in a fixed order and lacks checks the live path has (`overSyncBudget`,
   the legacy-intent gateway). No theorem relates live acceptance to audit
   acceptance in either direction.
6. `validUntil` is signer-chosen; the Host only suggests a window. The
   nullifier makes a leaked plan one-shot, so this is minor.
7. The clock has a lower bound only (`clock_monotone`): a tick holder can jump
   `clock/now` forward and expire every lease. An undocumented trust
   assumption.
8. The "exactness" theorems `source_request_epoch_current` and
   `…revision_current` are `rfl` because `requestFor` builds those fields from
   the snapshot; the real binding is the `wrongMessage` check on signed bytes.

**Policy legs.** The `authorizedSlot := 1` self-answering pattern does not
recur in the deployed core. Receivers write verb tags (`authority/operation/<verb> = 1`)
that the genesis authority law routes on, which is the receiver stating its
own identity. `PayEnrolReceiver` exposes its own decision tag to the law (the
law can veto, not recompute). `JobMoneyReceiver` hard-codes
`("request/verb", 2)` rather than projecting it (suspected).

**Replay and nullifiers.** Per-step only. Payment observations from two
receivers share one nullifier namespace, so cross-receiver double consumption
is blocked. No trace-level theorem ("each nullifier in at most one record")
exists; `install_consumes` and `install_preserves_other_nullifier` are the
lemmas it would be assembled from. Whoever holds the journal file and the
MAC key can author any state, by design.

**Genuinely strong.** `CapabilityDelegation.DescentReady` (child id fresh
across all kinds, unregistered, unrevoked, ancestors registered); the
signed-envelope controller's ordering (nothing reaches crypto before framing,
epoch and replay checks); `TargetsValid` with `prepareTuple` injectivity
(empty, duplicate and authority-as-target refused); `expectedTargetRoot =
pre.root` on every target kind; `public_refusal_uniform`; and the
`NativeIORefinement` and `EufCmaKeyCustody` structures that state what is not
proved.

### The older `Theory/`, `Pred/`, `Effects/` and `Compiler/`

Reader read the derivation engines, the predicate algebra, authorization and
money theory, Nock and the evaluator registry, the Lean cSHAKE, and the
consensus and confluence files, all in the snapshot of 31 hours ago. Items
marked (verified) I re-read.

**Does the founding thesis exist in code?** Three derivation engines exist;
one runs.

- `Compiler/Signature` → `Air` → `Effects/EffectSpec` is the initiality
  engine. `fold_unique` is a real six-line W-type induction. It is used in
  three files, `EffectSpec` has one declaration (`moveEffect`) and zero
  consumers, and `Effects/` is not in the Host closure. The collapse ATLAS
  describes is real mathematics instantiated at n=1 three times and consumed
  by nothing deployed.
- `Compiler/Emit`, the gate descriptor, has two unconditional iffs
  (`emit_faithful`, `emit_accepts_iff`) and says in its own header that "no
  current native module consumes this descriptor" (verified). In the
  snapshot no `Kernel/` or `Host/` file names it; today five `Host/BendLogic*Emit`
  files do, which are the per-fixture circuit emitters from the first review.
- `Compiler/PredCompile` is the one that runs. Its input is the syntactic
  `Pred` AST with no function fields (verified by reading `Pred/Core.lean:159`);
  its headline `lower_correct` is a real two-sided refinement over every
  constructor with four side conditions, all decided at runtime by
  `CanonicalPolicyConfig.verifies`, and 26 in-closure receivers route their
  policy leg through it. But there is no prover. `Deployed.lean:9` says it
  (verified): "Mini admits by re-execution, not by proof (decision 10-01)".
  The verifier builds the assignment, runs the emitted witness generator,
  evaluates the constraint list itself, and `lower_correct` says the answer
  equals `Pred.eval`. The deployed arithmetization is an executed twin of the
  evaluator, proved equal, sent nowhere.

Numbers: of 79,877 Kernel lines in the Host closure, about 21,000 are in the
26 receivers whose law evaluation is derived. Inside them, `prepare` (35
in-closure definitions), `project` (29 hand-written projections) and
`inductive Reject` (32) are hand-written per feature. The law evaluation is
derived once; the admission skeleton around it is written about thirty times.
This predates the last day.

**`Pred`.** One AST, one evaluator, structural so `decide` works, with real
theorems: `firstFailingLeaf` iffs, `eval_congr_slot`, and `dial_sound` (an
I-confluence proof by AST induction with a genuine negative pole). The
opaque `→ Bool` fields in the tree are crypto portals and a declaration-derived
fill verifier, none on the policy path. One hazard: atoms fail closed on an
absent slot, so `not` of an atom is fail-open; the house guard idiom
`any [c, not (eq "request/verb" 2)]` admits any clause if `request/verb` is
missing from a projection. Every projection checked starts with
`requestSlots`, by convention, not by theorem.

**Authorization.** `attenuation_admits_subset` (`TypedAuthorization.lean:851`)
and its strict form are real, and the family patch carries attenuation as a
proof field (`AttenuateEvidence.strict`), with child freshness across all
kinds, registered live ancestors and allocate-only planes, so re-grant after
revoke is refused and cycles are impossible. Revocation authority is held by
whoever has `revokeCapability` on the resource, not by the grantor
(`CapabilityRevocationController.lean:208`): a resource-admin model, correct
as written, undocumented as a choice. Bearer holders cover every subject in
Theory and the deployed portal refuses bearer use.

**Money.** `Batch.conservation` (`CanonicalResourceKernel.lean:446-495`) is
over the real ordered batch with explicit issuer wells, integer balances, no
truncation, and solvency on intermediate books. Four receivers consume it.
The operation language has no authority field; "payment authority required
separately for every posting source" is a Kernel promise.

**Nock and the registry.** `exec_sound`, `step_runs`, `crash_runs`,
`exec_shift`, `run_crash_iff` and `steps_stable` are real inductions; the
registry fields for Nock are these proofs repackaged. `oracle_is_export` is a
jam/cue round-trip, with the semantic content in `oracle_ok_step` and
`oracle_crash`. Spec fidelity to Nock 4K checked by reading.

**cSHAKE.** The first-pass trust table said `Sp800185Cshake256Fast.lean:27-28`
uses `implemented_by` and `extern`; those lines are a comment saying it does
not (verified). The fast path is attached by two `@[csimp]` lemmas proved for
all inputs and kernel-checked (`:853`, `:858`). The spec was read against
FIPS 202 and SP 800-185 and matches; the NIST sample 3 vector and
SHAKE256("") are pinned; the `count = 1` padding branch has no vector.

**Consensus and confluence theory.** `EpistemicConsensus`'s "Byzantine"
theorems say knowledge of a constant proposition is the constant, and the
file admits it. `RevocationConsensus.revocation_needs_consensus` is
`(∀v∈P, A v) → (∀v, A v → B v) → ∀v∈P, B v`. `Confluence`, `Finality`,
`ViewMerge`, `LaceMerge`, `Knowledge` are all outside the Host closure.

**Findings.**

1. **Hash binding is stated as `a = b ∨ Collision H` where `Collision H` is
   true for every finite-range hash** (verified, `Pred/HashEqDigest.lean:304-314`;
   inherited by `PredCompile.lean:1750`). The proof exhibits the colliding pair
   and discards it. For the deployed 32-byte digest the right disjunct holds
   by pigeonhole, so the theorem never forces two openings equal. This is
   ATLAS law 2's wound verbatim. Conclude with the pair.
2. **Global digest-injectivity premises** (verified,
   `Theory/CausalVersionDag.lean:101-104`, `CellSlot.lean:248`): "address left
   = address right → left = right" over an infinite preimage type is false at
   every deployed hash, so `merge_converges`, `crossCanonical_of_binding`
   and friends hold of nothing deployed. The pair-scoped
   `CellState.PairBindingPremise` beside them is the honest form; delete the
   twin.
3. **`EffectDeclaration` conservation is vacuous** (verified,
   `Theory/EffectDeclaration.lean:367`): `exactBalance` holds for every
   declaration because each constructor's deltas sum to zero syntactically,
   so `balanceCheck` is always true and the `.balance` rejection arms are
   dead. `accountMove.guardCheck = true` means no solvency. `digestWords`
   (`:208`) is a non-modular FNV that collides trivially. Live exposure is
   low; the store-level `DeclaredActionLowering.Accepted.conserves` is the
   correct twin.
4. **Build-time `#eval` writes into the working tree by relative path**
   (verified, `EmitSerialize.lean:146-147`, `SumcheckConformance.lean:159`,
   ten sites). Move generation to a lake script target.
5. The trivial-shape sweep: `ValidatedPatch.resultAt := fun _ _ => rfl`,
   seventeen `request_*_exact` that are `congrArg` of one field,
   `holds_iff_discharged_witness := Iff.rfl`, `derived_agrees` comparing a
   fold with the same fold unrolled.

**Genuinely strong.** `PredCompile.lower_sound/complete/correct` and
`CanonicalPolicyAdmission.verifies` (the verdict is literally
`systemAccepts (lower …)`; no second evaluator); the cSHAKE `csimp` proofs;
the Nock inductions; `Batch.conservation`; `CredentialAuthorityEffects`'
evidence-as-proof-fields; the deployed portal with `PEmpty` for unused faces;
`Store.run_frame` and `CellState.validate` (one store, one validator);
`DeclaredActionLowering.Accepted.conserves`.

### The feature families in `Kernel/` and all of `Assurance/`

Reader dumped every theorem header in the `Application*`, `Fn*`, `World*`,
`Provider*`, `Grain*`, `Participant*`, `Agent*`, `Content*`, hyperedge and
`Joint*` families and in the 125 Assurance files, then read the keystones.
Items marked (verified) I re-read.

**Census.** `Application*` is 119 files and 19,378 lines, 111 of them
deployed; `Fn*` 43 files and 6,750 lines; the rest are small. Version twins:
Begin V1/V2/V3, Claim V1/V2/V3, Completion V1/V2 are all in the Host closure.
Fresh submission accepts only the newest of each, yet the Host's own operator
operations 44/45, 50/51 and 52/53 still emit the older ingress versions that
its submit path refuses (reader; I verified that `Host/Main.lean:1101-1104`
accepts only Completion V2 while
`Host/ApplicationLifecycleCompletionOperator.lean:198` decodes the V1 source).
`FnConsumerProgress` is a legacy twin that proves its definitions equal to
its replacement's by `rfl`.

**Instance or bespoke tower.** Measured by diff after renaming the family
token (verified for the first pair): `ApplicationAgentLifetimeGrantAtomicBirth`
and `ApplicationShareIssueAtomicBirth` differ in 2 of 172 lines; the two
`FnPollReceiver`s differ in error strings; the two Participant receivers in
17 of 175 lines; the five Completion V1/V2 pairs in 11 to 59 lines each.
Every receiver retypes the same skeleton: `event`, `nullifier`, `readGuards`
with `readGuards_readonly` and `readGuards_current`, `writes` with
`writes_unique`, per-lane `charge`, `intent` with `intent_event_version :=
rfl`, `replay` with `replay_only_original`, `receiveLoaded`. The reader's
estimate: about 20K of this slice's 37K lines is retyped skeleton; Application
19.4K would become 5 to 6K. The declaration that generates them is half
present already (`PreparedInvocation` and `PreparationPlan`).

**The one-turn model is not on the deployed path.** `TypedCellHyperedge` and
`MultiCellHyperedge` are well stated (balanced, cone, re-validated joint
patch, five `no_commit_of_*` negatives, a real repeated-write tooth). But
nobody constructs a `Commit` on the running path (verified: `jointEvidence :=`
appears only in the hyperedge modules and three Hyperdocument modules, none
in the Host closure). Deployed receivers stop at `AcceptedLegs` and assemble
their own write lists. `PurseRefill.lean:14` says it: the shape of
`Commit.aggregateBalanced`, reimplemented by hand. `Admission.rejected_atomic
:= rfl` is named atomic and confessed definitional.

**Authority in the app and agent families.** What bounds a delegate is real:
`eligibleBits_within` and `self_escalation_refused` bound requested bits by
the ticket ceiling; `AgentGrain`'s `interrupted_worker_refused` and
`tripped_worker_refused` are general over `Pred.eval`; the issuer's lineage
is re-read at each dispatch. Hunts:

1. **Share tickets never expire and cannot be tombstoned** (verified:
   `Ticket` at `ApplicationDispatchAuthority.lean:100-106` has no window;
   `ticketPolicy` at `ShareIssueSource.lean:295-296` admits only verbs 1, 3, 4
   and 5, never a mutation, so the tombstone path is unreachable). Revocation
   is only indirect, by revoking a capability that kills every ticket the
   issuer ever issued, and no theorem relates either revocation to dispatch
   refusal.
2. **The lifecycle wedge is broader than the first pass found** (verified,
   `ApplicationGrain.lean:163-183`): reconciliation edges exist only `3→2`
   and `9→2`; claimed phases 8, 10 and 11 have only completion edges; there
   is no failure report; `reconciliationSlot` is projected by no receiver;
   `reconcileFailedStart`, `retire`, `servingWitness` and `checkpoint` have
   no authoring code anywhere. An install whose report is lost sits in
   phase 8 forever and cannot be retired.
3. Grant lifetimes are counted in accepted turns, so on an idle host nothing
   expires and on a busy one grants expire in minutes. Session revocation is
   enforced only by a hard-coded `.active` guard with no theorem.

**`Fn*`.** Selective release is bound end to end over the live path
(`signedPreimage_injective`, `ordinary_gateway_refused`). Poll coverage is
self-described testimony: `FnSelectedPollCoverage.lean:2-6` says "not a proof
that a remote service offered every article", and its only theorem is
`transition_candidate := rfl`. The frontier automaton that is the actual
coverage invariant has zero theorems. `FnPortableSource.decodeGroups` is a
`partial def` base64 decoder with no theorem.

**What Assurance assures.** About 45 files are fixture checks, of which five
run the deployed function; about 45 are general theorems about Selvage and
Compiler objects the Host does not run; 18 are manifests and game plumbing;
five files named `*Audit` contain zero theorems and only axiom pins; and
about 12 are models of external systems. Of those models (verified):
`HyperdocumentLinkSqliteTransactionalStore` defines `crash` as
`{ state with transaction := .idle }` (`:132-133`), so
`crash_after_insert_recovers_absent := rfl` says nothing about SQLite, and its
`PhysicalSqliteDurabilityCeiling` has eight Prop fields and no inhabitant;
`Ext6GateProofPositiveExecution`'s "runner" is a Lean constant returning the
accepted receipt; `DreggNetProviderConsumer` is 980 lines of literal
fixtures assuring a lease module that is not deployed. The honest exceptions:
`Assurance/SheetLaw.lean` is a mechanical embed of the real JSON with a gated
drift check, and the zkML and sumcheck conformance vectors are real Lean-to-Rust
links (the generated files are tracked, which the reader doubted). `ItemLaw`
is a hand copy with no check.

**Kernel audit files.** `AgentGrainAudit` and `ContentResourceAudit` are
legitimate case teeth: `decide` on hostile fixtures against the real
`accepts` and `run`. Keep them.

**Vacuity sweep.** `current_grant_count … = 6 := rfl` and nine more lengths
of list literals; `candidate_event_version … = 26 := rfl` six times;
`Ready.birth_empty (_ready)` with an unused hypothesis;
`physical_step_observed := refinement.simulates …` projecting its hypothesis
in a module that "constructs no instance"; six ceiling structures whose
fields are the property and which have zero constructions, all confessed.
`HistoryHeadInhabitation` records that `VerifiedHistoryHead` was uninhabited
until 2026-09-30 and two modules over the empty type were deleted: the team
has caught this class before.

**Genuinely strong.** `HostRefinesWorld.host_trace_represents_fold` (the
refinement that exists, outside the closure); `AgentGrain` budget and
generation theorems; `ApplicationDispatchAuthority` ceiling theorems; the
five `no_commit_of_*` negatives; `ProviderRoute.charge_le_reserve` and
`route_cannot_downgrade_at_settle`; the selective-release chain;
`ContentResource.run_executes` with its audit; `SheetLaw` and
`ReleaseGateRouting`.

## Part 3: what the whole tree says

Eight readers, about 3.3 million tokens of reading, every headline finding
re-checked by me against the source. This is a reading audit; nothing was
built or run except the project's own static gates and `gitleaks`.

### The answer to "was it only the last day"

No. The last day added volume at the same quality and stopped running the
gates. The proportion of one-line theorems is 42% before and after. The
patterns the first review named in the Objective Bend work (names standing in
for statements, carriers projected as theorems, hand-written twins beside the
derived path, fixtures counted as general results, status prose outrunning
the code) are present in the eight-week-old core at the same density. What
the older tree had that the last day lost was green gates and a README whose
numbers were once computed.

### Where the real content is

Ranked by how much of what is stated is actually established:

1. **Selvage.** Real mathematics with a refutation discipline. Its label
   overstates the deployed-parameter number, the binding leg, and the
   query-sampling gap, and nothing runs it.
2. **The Pred compiler and the policy leg.** One syntactic AST, one evaluator,
   a two-sided refinement, and the Host's verdict is literally the compiled
   system. It is an executed twin of the evaluator, proved equal, with no
   prover behind it. The project says so in `Deployed.lean`.
3. **The durable commit layer.** Nullifier consumption, stale-read rejection,
   no partial commit, exact debit, checkpoint resume: real theorems on the
   real transition.
4. **Authorization and money theory.** Attenuation as proof fields on the
   family patch; conservation over the real ordered batch with explicit
   wells; four receivers consume it.
5. **The sandbox.** Fixed bwrap floor, allowlist seccomp, an empty host API,
   a hostile probe actually run with a negative control.
6. **The private-room cryptography**, sound in its parts.
7. **Nock and cSHAKE**, proved as inductions and `csimp` equalities, with
   vectors.

Everything else is either skeleton retyped per feature, a model proved about
itself, or a name.

### The eleven defects that matter most, across both files

1. Operator-to-root symlink race in the SPK broker's export (first review).
2. Proxy-mode friends sign bytes the box authored.
3. Served room-key wraps need no founder signature; the operator can mint the
   next room key.
4. Every tenant, the Store, the operator socket and the seal key share one
   uid; two shell verbs already step outside the session home.
5. Nock re-execution and content runs happen before the signature check on
   the live path; refused commands are never charged.
6. A truncated durable log replays without the MAC key.
7. `rotate-key` cannot recover from a crash after the Host admits the
   rotation (first review).
8. A crash in the grain controller's journal rename window fences the task
   forever; a torn private-backend journal bricks the replica.
9. The resident holds `CAP_SETUID` with no namespace restriction while
   parsing app bytes.
10. One Byzantine sender can exhaust the private backend's replay pool; one
    stranger can kill a cohort link for its lifetime.
11. Share tickets cannot expire or be revoked except by killing every ticket
    the issuer ever issued; an install whose report is lost wedges forever.

### The structural facts

- CI has never passed. The build itself has been red since 07:30 on
  2026-10-03 because of two imports of uncommitted files.
- 170 library modules, including every Objective Bend module, every Bend
  backend keystone and the Simplex safety chain, are elaborated by no gate.
- 133 opcode arms, four named in any theorem. The refinement bridge to the
  world model ignores its admission argument and lives outside the closure.
- The skeleton is written about thirty times in the deployed core and about
  thirty more in the feature families; two files differ in 2 of 172 lines.
- No generated claims ledger exists. The website is a 2026-08-10 snapshot
  that names a proof system that was renamed on 2026-08-13.
- Three of thirteen gates measure nothing in CI (cold-start passes on a
  missing binary; the hypothesis ledger's self-test fails; prover-glue has
  no toolchain).

### What I would do, in order

1. **Take the box off the public internet for strangers**, or at least stop
   issuing proxy keys automatically on payment, until items 1 through 6
   above are closed. Friends who already hold keys should be told what the
   operator could do today with an active attack, in the same register
   FRIENDS.md already uses for "root can read it".
2. **Make the build green and keep it green**: commit the two missing files,
   move every unrooted module under a separate `WIP` library target so the
   umbrella and its gates mean something, fix the three non-measuring gates,
   and require a green CI run before anything lands on main. The gate runner
   is good; it needs to be obeyed.
3. **Regenerate or delete the public record.** The website is wrong in
   every quantitative sentence. Generate the claims page from the tree
   (theorem names, statements, witness status, closure membership) or take
   it down. Fix NOTICE and the four unlicensed crates.
4. **Collapse the receivers.** One `Receiver` declaration, with the eight
   standard definitions and their theorems written once, is the single
   change with the largest reduction in both lines and risk. The feature
   families are where to start, since two of them already differ by two
   lines.
5. **State the Host theorem.** Per-receiver "confirmed implies admitted and
   appended", derive `Turn.ofAdmission` from the `Accepted` object, tighten
   `Represents`, import `HostRefinesWorld` into `Host.Main`. Until this
   exists, the honest sentence is "each receiver is checked in isolation;
   nothing is proved about the dispatcher."
6. **Fix the statement shapes that recur**: the `… ∨ Collision H` disjunct,
   global digest injectivity, `Bool` signature verdicts, `rfl` on
   constructor-stored fields. Each is a one-line pattern that a linter over
   the theorem table could flag, which would be the vacuity instrument the
   README promises.
7. **Relabel Selvage honestly** and connect one thing to it. It deserves the
   lead paragraph; the paragraph should say what it proves.
8. **Then** Objective Bend, as the first review laid out.
