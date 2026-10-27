# HOLISTIC-RUST · the Rust layer of nanodregg, judged against the field

Reader: the RUST layer (nd and its step loop, the attempt store, custody, the mux/supervisor, the
hosted launcher: keybroker, nd-members, grain-launch; and their tests), 2026-10-24, nano at
`origin/main f9657bd`. This is a judgment written from yesterday's whole-file read
(READ-RUST.md). No edits, no builds. Tags: **READ** (path in nano), **INFERRED** (my reasoning).
Citations are to work I know; where I am unsure of a year I name the line of work instead.

---

## 1. What this layer is, in the field's terms

### 1.1 The shape: a sans-I/O decider with an untrusted effect handler

The core of `client/` is a **pure decider that yields effect requests, driven by a dumb effect
handler that performs them and resumes it** (READ: `client/src/run.rs:229-320`,
`Protocol/Command/Machine.lean`).
- `host follow` (Lean) answers each command with a *step*: `Sign`, `SignNext`, `SignIncoming`,
  `Precommit`, `Host op payload`, `Submit call`, `Done`. Each step carries an opaque continuation
  `k`.
- `nd` (Rust) performs the step and sends back `resume(k, outcome)`.
- The order of effects, what is signed, what is printed and every exit is the decider's
  (CLIENT-2/HOST-9).

That is, precisely:
- **Defunctionalized algebraic effects** (Plotkin and Pretnar's handlers, 2009) with the
  continuation reified into bytes, and the handler in another process and another language.
- In the verified-systems vocabulary, it is an **Interaction Tree** (Xia et al., POPL 2020) whose
  visible events are exactly the step constructors, interpreted by an unverified handler.
- In industrial vocabulary it is the **sans-I/O protocol pattern** (h11, quinn-proto): the protocol
  is a pure state machine and the I/O shell is swappable.
- The continuation round-tripped through the client is the old **stateless-server /
  client-held-continuation** trick: web continuations in the Queinnec line of work, SYN cookies.

Where it matches the state of the art (INFERRED): this is the right shape for "the decisions are
proved, the plumbing is not". It is how a verified core composes with an unverified OS.
- seL4's userland servers, miTLS/Everest's verified protocol over an unverified network stack, and
  EverParse's verified parsers inside unverified C programs all draw the line the same way: the
  decider has a specification and the shell has an interface.
- nano draws the line further toward "the shell decides nothing" than most of those systems do.
  T0 (`e2905e7`) made follow re-check a submitted call's settlement on its own World before it
  answers `ok` (READ: `Machine.lean:1051-1071`). After that the shell cannot manufacture success,
  which is the property that matters.

Where it is behind (INFERRED):
1. **The continuation is not authenticated.** The decider trusts the handler to hand back `k`
   byte for byte; the HOSTING stdio-leg TCB row says so verbatim (READ: `gates/tcb.tsv:54`, "gave
   follow back byte for byte every continuation follow handed out"). The stateless-server
   literature solved this decades ago: MAC the continuation under a key the decider keeps (SYN
   cookies, signed session state in web frameworks). That would move "the relay did not forge or
   replay a continuation" out of the TCB at almost no cost.
2. **The relay has no model.** The relay ("move bytes, preserve order, return every `k`") is
   specified by one prose row of the TCB table, not by a Lean definition that Rust traces could be
   checked against. Verdi (Wilcox et al., PLDI 2015) and IronFleet (Hawblitzel et al., SOSP 2015)
   both give the shell a *network semantics* and prove the composition. nano proves the decider
   and states the shell as a premise (`Hosting.Proofs.Socket.StdioLeg`). That is a legitimate
   design point, Verdi's "verified system transformer" minus the transformer, but it is one rung
   below them.

### 1.2 The attempt store: an outbox for at-most-once over an untrusted Host

`attempt.rs` is a **durable client-side request log**: freeze the exact signed bytes, write a
marker before each send, and settle only from a verdict (READ: `client/src/attempt.rs:1-21`). It
instantiates three classic ideas at once:
- **At-most-once RPC with idempotency tokens** (Birrell and Nelson, 1984, and every payment API's
  idempotency key since). The signed call is a *self-certifying* idempotency token: the writer's
  journal dedups by its transaction id.
- **The end-to-end argument** (Saltzer, Reed and Clark, 1984). The Host's status byte is a hint,
  and the member's own fold decides (PROTOCOL-46, CLIENT-27; READ: `run.rs:116-130` `hint`, and
  `attempt.rs` settling only from `Receipt`).
- **A full-validating light client.** The member does not trust the writer's claim of inclusion; it
  re-executes the pages and settles on its own World. That is the
  certificate-transparency / transparency-log stance (RFC 6962's "don't trust, verify") with
  re-execution in place of Merkle inclusion proofs. The charter rules out proof systems (READ:
  CHARTER.md §Scope), so re-execution is the consistent choice.

Where it matches: the Host-lies analysis is at venue grade. CLIENT-27 documents that a
Host-status settlement locks a rotating member out both ways ("ok" for an unlanded rotate, and
"refused" for a landed one), and that a naïve `confirm` deadlocks because the old key's envelope is
refused after the rotate lands. Then it designs the incoming-key envelope exception narrowly
(READ: decisions/client.md CLIENT-27). That is the kind of adversarial case analysis a security
program committee wants to see.

Where it is behind, and this is the architectural point of yesterday's F1. A request log is half
of exactly-once; the other half is **recovery**. ARIES-style redo, transactional-outbox sweepers
and Lamport's client-request IDs in Paxos deployments all make "resolve every in-flight request
before issuing a new one" a structural step of restart. nano's store has the log and not the
sweeper:
- only an armed rotation's attempt is ever reloaded (READ: `run.rs:191-195` is the only
  `Attempt::load` caller in `client/src`);
- the Lean docs and decisions promise the rest ("the next run looks it up": READ:
  `attempt.rs:18-21`, `Protocol/Attempt.lean:38,90,99`).

So the design the literature would call exactly-once is implemented as at-most-once *per run*.
Above it, a restart-class exit makes every caller (a member, the resident's tick) re-run, and a
re-run signs a new call.

### 1.3 Custody: pre-rotation, in the KERI sense

`custody.rs` holds a current key and a **precommitted next key whose public half is published
before it is used**. The next secret is held elsewhere (removable media, or another account), and
a rotate is signed by the next key itself (READ: `client/src/custody.rs:1-16`, CLIENT-13). This is
**KERI's pre-rotation** (Smith's Key Event Receipt Infrastructure line of work, 2019 onward)
almost exactly.
- What nano adds is a two-phase *arming*: a rotation is bound to one frozen attempt and reconciled
  before any other command (READ: `run.rs:184-210`, `custody.rs:529-564`). Its incoming key may
  sign only read envelopes while it is armed, which is domain separation by prefix
  (`ENVELOPE_DOMAIN`, READ: `custody.rs:505-527`).
- I do not know a name in the literature for "a key rotation whose commit is decided by the
  rotating party's own re-execution, with a client-side armed state that blocks further rotation
  and narrows the incoming key to reads". It is a sound, small, idiosyncratic refinement of
  pre-rotation. Novel as engineering, not as an idea.
- The observer record (sign envelopes only) and the stdio custody (never rotate) are
  **attenuation by construction of the signer**. That is the macaroon/biscuit idea (Birgisson et
  al., NDSS 2014) applied to the *signing oracle* rather than to the token: the same move as an
  HSM key policy.

Where it is behind: the signer is a **policy-light signing oracle**. Custody signs whatever bytes
follow hands it, except for the envelope-domain fence (READ: `custody.rs:442-453`). The
hardware-wallet literature ("what you see is what you sign") and typed signing requests would have
custody parse and display, or at least classify, what it signs. In nano, follow is the member's
own Lean, so the confused deputy is the member's own decider. That is acceptable for a single-node
vat (INFERRED), but it means the custody boundary adds no defence-in-depth against a compromised
follow binary.

### 1.4 The supervisor and the sandbox: crash-only supervision with path-based confinement

`nd-supervise` puts one Lean child behind a Unix socket. The design:
- a mux with one writer thread per connection;
- every close named by an emitted `CloseReason`;
- bind-after-child, and SIGTERM converted into named closes;
- the child confined by bwrap (Linux) or sandbox-exec (macOS), with a deny-by-default allow-list;
- "the service manager restarts the pair, one restart path" (READ: `client/src/mux.rs:1-26`,
  `client/src/bin/nd-supervise.rs`, `sandbox/src/lib.rs`).

The design intent is **crash-only software** (Candea and Fox, HotOS 2003) with a supervisor tree in
the Erlang/OTP (Armstrong's 2003 thesis) and daemontools/s6 tradition, delegated to systemd.
- The named closes are the transport-level analogue of HTTP/2 GOAWAY codes or WebSocket close
  codes: prior art, well done.
- The sandbox is the bubblewrap/Landlock family of **namespace-view confinement**.

Where it is behind, on two fronts, both at the field's level and not as bugs:
1. **Death propagation is not structural.** In OTP a link makes a child's fate follow its parent.
   In s6 the supervisor *is* the parent and dies last. On Linux the primitives are
   `PR_SET_PDEATHSIG`, `PR_SET_CHILD_SUBREAPER`, pidfds and one cgroup per service. nano uses only
   bwrap's `--die-with-parent`, on the confined grandchild (READ: `sandbox/src/lib.rs:435`). None
   of its own four binaries links its life to its parent, and the test harness relies on Rust
   `Drop` (READ: `devtools/src/lib.rs:204-210`).
   - In deployment systemd's cgroup papers over this (KillMode=control-group).
   - In tests nothing does: 328 orphans on hbox (cv 01a16b44).
   - The decision record says a death signal is impossible without `unsafe` (READ: CLIENT-29
     CRITIQUE). rustix 1.1.2, already a dependency, exports it as a safe function (READ:
     rustix-1.1.2 `src/process/prctl.rs:66`).
   That an estimate ("needs `unsafe`") became a constraint is exactly the substitution the project's
   own CLAUDE.md names.
2. **Confinement is path-based, so connect authority is ambient within a view.** CLIENT-20 records
   that on Linux a file grant on a directory is a *connect grant* to every socket in it (READ:
   decisions/client.md CLIENT-20; `gates/tcb.tsv` row `CONNECT_FILTERED`). The capability answer
   is Capsicum (Watson et al., USENIX Security 2010), and more simply fd-passing (`SCM_RIGHTS`):
   the supervisor hands the child *connected descriptors*, and the child has no namespace in which
   to name a socket at all. nano compensates with views that hold one socket each
   (`socketDirShared`, READ: `launcher/src/bin/nd-members.rs:458-484`). That is careful
   compensation for an ambient-authority mechanism, not an object-capability design.

### 1.5 The hosted launcher: a credential-injecting broker under a decided policy

keybroker is a **credential-injecting proxy** (the "secretless broker" pattern). The resident never
holds the provider key. A Lean decider (`hosting-broker`) decides every grant, and Rust adds only
the key header, TLS, the pin check and two key-echo fences (READ:
`launcher/src/bin/keybroker.rs:1-37, 659-737`). The pattern is the state of the art for "the agent
may spend but never see the key". Its decider being a total Lean function over the World's
allowances is better than any production instance I know, which is a policy file or OPA.

grain-launch and nd-members are **reconcilers** in the Kubernetes-controller sense:
- ask the decider which residents exist, converge the processes to that set, tick
  (READ: `nd-members.rs:318-415`, `grain-launch.rs:361-383`);
- the controller's memory laws ("one child per grain, reports in order") are stated as premises on
  the Rust (READ: `launcher/src/lib.rs:6-9`).
This is a sound modern shape. What it lacks relative to the field is the controller's usual
liveness discipline: every wait bounded by a deadline, and a decider that misses one restarted.
The decider reads have no timeout (READ: `launcher/src/residents.rs:13-21`).

### 1.6 The emitted tables: EverParse-lite

Every bound, opcode, status, close reason, custody refusal, the attempt decision table and the
layout codecs reach Rust as files emitted from Lean, checked by `emit-rust --check` (READ:
`client/src/generated.rs:1-3`, `gates/generated.tsv`). This is the **EverParse idea** (Ramananandro
et al., USENIX Security 2019): generate the low-level parser from the high-level format so that
there is one source of truth.
- Behind EverParse: the Rust *template* inside the emitter is trusted, and there is no proof that
  the emitted decoder is the Lean decoder. `launcher/tests/path_vectors.rs` is the right
  instinct: verdict vectors evaluated by Lean, checked against the Rust. It is translation
  validation on a finite sample. It exists for one function only (READ).
- At the state of the art the next step is Aeneas (Ho and Protzenko, ICFP 2022), which translates
  the Rust into Lean so that the emitted decoder can be *proved* equal to `Codec`'s. For a
  generated, loop-free codec that is a tractable proof.

---

## 2. The architecture judged (from where the Rust sits)

### 2.1 The twelve laws as seen from the Rust

**Load-bearing and correct:**
- **Law 2 (Lean decides, Rust moves bytes).** This law is the reason the layer is good. It forced
  T0, it forced the end-to-end settlement, and it forced the custody refusals to be follow's to
  render. My re-count found 16 Rust decision sites on the stdio leg, none of which can produce a
  member-visible `ok` (READ-RUST §1). That is a strong place for a mixed-language system to be.
- **Law 7 (refusals by name)**, applied to the transport. Named closes, named supervisor exits,
  named custody refusals. It is cheap, it is what operators need, and it is rarer than it should be.
- **Law 12 (size ratchet).** The client library is about 2.5k lines (READ: CLIENT-32 size line).
  The ratchet is why `client/` stayed a relay and did not grow a second protocol implementation,
  which is minidregg's failure mode (DESIGN.md §7 lists the deleted modules).

**Aspirational for the Rust (stated, not what the code does):**
- **Law 1 (one of everything).** Inside Rust there are hand copies:
  - of Lean's printed formats (`receipt `/`head `/`settle `, `refused NAME`);
  - of socket names;
  - of the child-wire id width, three times;
  - of the "≥ 128 means signal" rule, three times;
  - of the restart cadence;
  - and the tests copy Lean's printer once more as stand-ins (READ-RUST F7, F8, F12, F13).
  The emitter carries numbers and enums but no strings, so every string-shaped fact leaks into a
  twin. Law 1 holds for *tables*; it does not yet hold for *formats*.
- **Law 4 (a static bound on everything).** The Rust's time bounds are per syscall, not per
  reply: `SO_RCVTIMEO` in `sockets.rs:45-50`, and keybroker's `UPSTREAM_TIMEOUT`. Some waits have
  no bound at all: the decider reads. `attempts/` grows forever and is listed on every submit
  (READ: `run.rs:353-365`). TigerStyle as practised at TigerBeetle means *deadlines* carried
  through an event loop. The Rust here has *timeouts* attached to sockets, which bound silence but
  not trickle.
- **Law 10 (decisions examined).** The examination is real and often excellent (CLIENT-27,
  CLIENT-30). But the decision files are append-only prose with no supersession links, so they
  drift: CLIENT-29 describes a layout HOSTING-32 replaced, and `client/DESIGN.md` describes the
  Host-settled store CLIENT-27 deleted (READ). Architecture-decision records (Nygard's ADR
  practice) solve this with a mandatory "superseded by" field. Here a gate could check that a
  decision cited by a path still matches that path.

**Wrong-headed in light of the field:**
- **Law 2's corollary, "Rust (if any) is transport", has been read as "the Rust needs no
  specification".** The field's lesson from Verdi and IronFleet is that the shell's correctness is
  itself a statement ("delivers in order, returns every continuation, never fabricates a reply"),
  and it is best stated as a model the shell is checked against. nano states it as one row of
  `gates/tcb.tsv` (READ: row `stdio-leg`). The consequence is visible: the Rust's tests check Rust
  against Rust's reconstruction of Lean (`ScriptedFollow`, the python stand-in follow; READ:
  `client/tests/run.rs:28-58`, `client/tests/roundtrip.rs`). That is how the missing attempt
  resume (§1.2) stayed green. Law 2 is right that Rust must not *decide*. It is wrong to imply that
  what Rust *does* needs no spec.

### 2.2 The cuts

- **Rust/Lean at custody, sandbox, sockets, threads: right.** These are the OS-facing and
  crypto-library-facing parts, where Lean has no ecosystem (ed25519-dalek, rustls, bwrap). The TCB
  table names them honestly, with a lift condition each (READ: `gates/tcb.tsv`).
- **Rust/Lean through the attempt store and the step loop: the wrong cut.**
  - The attempt store is *state plus a decision procedure over crash points*. Its decision table is
    already Lean's (`Protocol.Attempt.next`, emitted), and its settlement is now Lean's (T0). The
    driver loop, the fuel, the payload composition, the resume policy (missing), the arming order
    and the durability protocol are Rust's (READ-RUST §1, S6-S11).
  - This is the one place where the cut splits a single state machine across the language boundary.
    It is also where the layer's worst defect lives. A state machine split across a boundary is
    one where neither half's theorems talk about the whole.
- **client vs launcher crates: a cut by history.** nd-members lives in `launcher/` because the
  residents codec is the launcher's emitted file and the client cannot depend on it (READ:
  CLIENT-29 "Placement"). A shared emitted crate would remove the cycle. That is minor.
- **One nd-supervise per socket**, so two supervisors and two bwraps per resident (READ: CLIENT-29
  static bounds: processes ≤ 2 + 4·1024). The cost is processes, and it buys per-socket fault
  isolation, which is the OTP trade. Defensible. A single event-loop supervisor multiplexing N
  sockets would be the TigerBeetle/seastar choice and would make deadlines natural (§3).

### 2.3 Single writer + receipts + no agreement engine, from the client's chair

From the Rust layer's point of view the single writer is the *right* call (INFERRED).
- With one writer and a journal, "did my call commit" has a unique answer, and the client's whole
  uncertainty problem reduces to at-most-once plus end-to-end verification. That is exactly what
  §1.2 implements.
- With an agreement engine (Tendermint-style decided logs, Calvin's deterministic pre-ordering) the
  client would need finality reasoning as well. The charter is right to rule that out of scope.
- The instructive point: **even with one writer, the client's exactly-once is the hard part, and
  it is the part that is not done.** The deferral of agreement did not defer the hardest
  distributed-systems problem in the client. It only made it look small.

### 2.4 The verification method: plants, gates, census

**Plants are mutation testing** (DeMillo, Lipton and Sayward, 1978) used as an *adequacy criterion
for tests and as a vacuity check for theorems*. As a vacuity check they are sound and better than
most practice: seL4 and CompCert rely on reviewers to notice vacuous specs, and nano mechanises the
question "would anything go red?".

For the Rust layer, though, plants are the *only* evidence, and three things make them hollow
there (INFERRED from READ-RUST F1, F7, F17):
1. A plant that runs against a stand-in proves the Rust matches the stand-in, not Lean.
2. A plant whose "next step" is performed by the test itself (`Attempt::load` + `drive` in
   `client/tests/attempt.rs:340-355`) proves the library *can* do the thing, not that the system
   *does* it.
3. A mutation list chosen by the author (CLIENT-27's M1–M10, CLIENT-30's S1–M5) covers the
   mutations the author thought of. Automated mutation tools (cargo-mutants) would have produced
   "delete the call to reconcile", which reds, and "add a resume pass", which no test can tell
   from today's code: the absence is invisible to mutation testing by construction.

**Against CompCert/seL4/IronFleet:** those establish trust through *one top-level refinement
theorem* plus a small, audited TCB. nano establishes it through about 6,300 local theorems
(READ: SIZE.md) and a TCB table. For my layer, the top-level statement that would matter is short:

> (a) every `CommandExit.ok` a member or resident sees for a submitted call corresponds to a call
> its own fold holds committed; (b) for each intent the member issues, across any interleaving of
> crashes, timeouts and re-runs, at most one call commits.

(a) is now true modulo the stdio-leg premise (T0 + `StdioLeg`). (b) is false today, and no local
theorem could have shown that, because (b) quantifies over *runs of the system*, not steps of a
function.
- That is precisely what FSCQ's crash Hoare logic (Chen et al., SOSP 2015) and Yggdrasil's crash
  refinement (Sigurbjarnarson et al., OSDI 2016) exist for. The crash-atomicity mistake in `fsx`
  (create+write in place, READ: `client/src/fsx.rs:47-55`) is the ALICE paper's canonical example
  (Pillai et al., OSDI 2014).
- A mechanised-metatheory practitioner would say: 6,000 theorems with no statement that the system
  refines a spec is a well-tested library, not a verified system. The spec need not be large. It
  must exist, and it must be over *traces*.

---

## 3. The details judged, from this layer

### Three I would defend at a top venue

1. **End-to-end settlement by the member's own re-execution, after T0** (READ: `Machine.lean:
   1051-1071`, `client/src/run.rs:116-161`, CLIENT-27).
   - "The Host hints; the member's fold settles", with the Host-lies case analysis (lockout both
     ways, the incoming-key envelope) and the result that the untrusted relay cannot manufacture
     success, is a clean instance of the end-to-end argument with a mechanised decider.
   - Combined with pre-rotation custody whose commit is decided by the same fold, it is a
     publishable systems-security contribution in the "verifiable client over an untrusted
     service" line: transparency logs, verifiable ledgers, and SUNDR's fork consistency (Li,
     Krohn, Mazières and Shasha, OSDI 2004), which is the closest ancestor for "the client checks
     the server's history itself".
2. **The sans-I/O step protocol with one emitted vocabulary** (READ: `generated.rs` `layout::Step`,
   `run.rs:229-320`).
   - Seven effect constructors, an opaque continuation, every bound and name emitted from Lean,
     and a Rust interpreter of about 100 lines.
   - This is the right engineering shape for a verified decider, and it is the reason the Rust is
     2.5k lines instead of minidregg's 113k (READ: `client/DESIGN.md:86`).
   - A reviewer would ask for the continuation to be authenticated and for the relay to have a
     model; both are additions, not redesigns.
3. **Least-privilege confinement as a measured artefact** (READ: CHARTER law 2's platform-fact
   clause, CLIENT-9, `sandbox/`). A platform floor is a table with a plant proving no over-allow
   and a recorded bisection proving minimality.
   - I know of no name for this in the literature. The nearest are syscall-policy minimisation
     tools in the seccomp-generation line of work.
   - It is a small methodological contribution: treating a sandbox profile as a claim with two
     sides (sound and minimal), each with evidence.

### Three I would be embarrassed to present

1. **An exactly-once client without recovery** (§1.2; READ: `run.rs:191-195`,
   `attempt.rs:18-21`). The docs and decisions describe the full protocol; the code implements
   the log and not the sweeper; the tests drive the sweeper by hand.
   - What a strong PhD student would build: the client's attempt store as a Lean state machine
     over crash points, with the theorem "while an attempt is open, no new call for the same intent
     is issued", in the FSCQ/Yggdrasil style. Or, more cheaply, a TLA+ spec of store + Host +
     re-runs model-checked for the at-most-once invariant, which would find the missing resume in
     seconds.
   - Then the fix: every run resolves every open attempt before follow plans anything.
   - **Cost:** the TLA+ check is a week. The Lean state machine with its theorem is one to two
     months (Attempt.next and its proofs exist). The code fix alone is days.
2. **Lifetime by `Drop`, time by `SO_RCVTIMEO`** (READ: `devtools/src/lib.rs:204-210`,
   `client/src/sockets.rs:45-50`, `launcher/src/residents.rs:13-21`).
   - Process lifetime is tied to destructors that never run on SIGKILL. Deadlines are per syscall.
     Some waits are unbounded.
   - The mux is a hand-rolled thread-per-connection state machine with atomics and a one-slot
     channel. Its `replyBacklog` rule is a scheduling race (READ-RUST F21) that no model of the mux
     exists to catch.
   - What a strong student would build:
     - supervision as structure: `PR_SET_PDEATHSIG` in every binary's `main`, a subreaper or
       cgroup per test (days);
     - the mux as a single-threaded poll loop over absolute deadlines, sans-I/O like quinn-proto,
       so that every close reason is a function of (state, now);
     - the concurrency checked with Loom, or CHESS-style systematic testing (Musuvathi et al.,
       OSDI 2008), or the mux state machine written in Lean beside its Rust loop.
   - **Cost:** a week for death propagation and per-reply deadlines; one to two months for the
     poll-loop mux with a model.
3. **Tests that verify Rust against Rust's reconstruction of Lean** (READ: `client/tests/run.rs`
   `ScriptedFollow`, `client/tests/attempt.rs:23-25`, the python stand-ins in `roundtrip.rs`).
   This is the "mirror" failure the project's own doctrine names. The receipt format, the step
   order and follow's verdicts are re-typed in the tests, so a Lean change leaves the Rust suite
   green.
   - What a strong student would build: model-based testing driven by the real decider. Lean emits
     *traces* (sequences of steps and expected outcomes over a scripted Host) and the Rust handler
     is run against them, the "conformance test generated from the model" approach of the
     model-based-testing line of work. Alternatively, the real `host follow` in every test: it
     is fast, and `real.rs` already does it.
   - **Cost:** a week to emit attempt and step traces from the existing Lean rows; days to delete
     the stand-ins.

---

## 4. What to do

### The one structural change: move the attempt machine into follow

**Make the attempt store follow's state and the attempt loop follow's phase, so Rust performs only
`Host submit` / `Host lookup` exchanges and `fsync`s.** (INFERRED design; READ for the pieces.)
- Follow already sees every `Submit` and now keeps the call bytes in its continuation (T0, READ:
  `Machine.lean:1032-1035` `ownSettle … cb`).
- `Attempt.next` is already a Lean function with theorems (READ: `Protocol/Attempt.lean:115-140`).
- The settlement is already follow's.
- What remains in Rust is the loop, the fuel, the payload, the arming order, the resume policy and
  the files: exactly the split state machine of §2.2.

Put the frozen calls in follow's own durable record. This must NOT be a new kind in the World's
trie: the project's own minted lesson (10-17) is that a third slot kind put a `Canon` premise on
about 150 cell theorems. A separate append-only file beside follow's Store, with the same `fsync`
discipline, avoids that. Follow then begins every command by planning "resolve open attempts"
steps.

What it makes true:
- (b) of §2.4 becomes a Lean theorem over follow's state ("no new call while one is open for this
  intent").
- R4–R8 of IMPACT-E2 and S6–S11 of my re-count leave Rust entirely.
- `client/src/attempt.rs` (327 lines) and most of `run.rs`'s `reconcile`/`drive` are deleted.
- The stdio-leg TCB row shrinks to byte relay.
- The rotation arming becomes one Lean state, not a Rust file ordering.

Cost: the premise price above (keep it out of the World), one new durable record in follow, and
re-cutting the run.rs tests onto the real follow. A month, perhaps two. That is a large ratio of
"made true" to cost. It also completes the trajectory T0 started rather than adding a new one.

### The one thing to stop doing

**Stop writing Rust-side stand-ins of Lean behaviour and calling them plants.**
- `ScriptedFollow`, the hand-typed receipt lines, the python follow stand-ins and Rust copies of
  the Bell's patience are reconstructions.
- Every one of them can only confirm that Rust agrees with the author's memory of Lean.
- Use the real `host follow` (fast), or traces emitted by Lean. Where a stand-in is unavoidable (a
  lying Host), emit its script from the Lean row that defines the lie (`Protocol/Rows`), so the
  stand-in is the spec's and not the author's.

### Grade

**B−** against the bleeding edge. The architecture is the right one and the execution is uneven:
- The architecture: a sans-I/O decider under an untrusted effect handler, end-to-end settlement by
  the member's own re-execution, KERI-style pre-rotation with a decided commit, and an emitted
  vocabulary. Its central boundary is executed with research-grade care: after T0 the untrusted
  Rust cannot make anyone see success.
- The execution elsewhere: the two boundaries that have no theorems behind them, *time* and
  *process lifetime*, get hobby-grade care. The one distributed-systems property the client
  exists for, at-most-once across re-runs, is documented as done and implemented only for key
  rotations. Its tests mostly check the Rust against the author's own copy of Lean's behaviour.
