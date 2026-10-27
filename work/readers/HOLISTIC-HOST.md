# HOLISTIC-HOST — the writer, the follower, the lock, the Store, the refinement (nanodregg f9657bd)

Author: the HOST whole-file reader (READ-HOST.md, 2026-10-24), stepping back. No edits, no builds.
Tags: READ (path) for claims about nano's code; INFERRED for my reasoning. Citations are to work I
know; where I am unsure of a year I name the line of work instead.

---

## 1. What this layer is, in the field's terms

### 1.1 The design it instantiates

Host is a **single-writer, deterministic, durable state machine with group commit**. In front of
it sits an **authenticated append-only log**. Behind it sits **auditing replicas that re-execute
rather than agree**. Taking the pieces in turn:

- **The writer** is the classic redo-only write-ahead log with group commit, as in database
  recovery since ARIES (Mohan et al., 1992). Host drops undo because the state transition is a pure
  function. The loop is (READ Host/Loop.lean:4-15):
  1. take one blocking frame plus whatever is queued;
  2. run a pure `admitBatch`;
  3. append one record;
  4. fsync;
  5. only then reply.

  Group commit happens "with no timer": the queue that forms while one fsync runs becomes the next
  batch. The modern references are TigerBeetle's style (TigerStyle is named in law 4) and SQLite
  WAL's write discipline. Separating a pure decision from the effect shell ("functional core,
  imperative shell") is what makes it provable.
- **The log** is a keyed hash chain of frames: `u32 len ‖ r ‖ MAC(prev ‖ r)` (READ Host/Log.lean:7).
  It is the Schneier–Kelsey secure audit log (1999) without forward-secure key evolution. One
  integrity-at-rest key protects segment, base, index and headers under four domains (READ
  Host/Keys.lean:17-24). The forward scan that tells a torn tail from corruption (READ Log.lean:111-119)
  is the standard recovery question that Pillai et al. ("All File Systems Are Not Created Equal",
  OSDI 2014) showed applications usually get wrong. Here it is a theorem over arbitrary bytes
  (`open_sound`).
- **The checkpoint** is a whole-World snapshot sealed off-loop in a Task, with the log as the
  redo tail (READ Host/Bounds.lean:8-13, HOST-14). This is the Redis RDB+AOF / LSM-manifest shape:
  replace the base atomically by tmp+fsync+rename+dirsync (READ Host/Store.lean:91-97). The amortised
  "seal every quarter of the base" cadence is a choice of write amplification that the decision
  record prices (HOST-14).
- **The follower** is not a replica in the Paxos/Raft sense. It is an **accountability witness**.
  It re-derives every logged event from the member-signed call (READ Protocol/Command/Machine.lean:437-464)
  and refuses the log by name when the result differs. Its closest relatives:
  - **PeerReview** (Haeberlen, Kouznetsov, Druschel, SOSP 2007): tamper-evident logs plus
    deterministic replay by witnesses.
  - **SUNDR**, the family of single-untrusted-server systems (Li, Krohn, Mazières, Shasha, OSDI
    2004), and its successors SPORC (Feldman et al., OSDI 2010) and Depot (Mahajan et al., OSDI
    2010).
  - **Certificate Transparency monitors** (RFC 6962, 2013): an append-only log that clients audit.
- **The refinement** `Host ⊑ Kernel` (READ Host/Proofs/Refine.lean:1-53) has the shape of the
  implementation layer of IronFleet (Hawblitzel et al., SOSP 2015) or Verdi (Wilcox et al., PLDI
  2015). The state's World component IS the abstract state, and each step is a fold of at most one
  kernel step. It is stated over the pure handler, not over the IO loop.
- **The crash theorems are format theorems, not file-system theorems.** `open_encodeAll`,
  `open_torn`, `open_sound`, `openWith_backup` and `sealed_opens` are all about functions over byte
  arrays (READ Host/Proofs/Open.lean, Backup.lean, Seal.lean). FSCQ (Chen et al., SOSP 2015, Crash
  Hoare Logic), DFSCQ (SOSP 2017), Yggdrasil's crash refinement (Sigurbjarnarson et al., OSDI 2016),
  and Perennial / GoJournal (Chajed et al., SOSP 2019 / OSDI 2021) all prove against a disk model
  with crashes and asynchronous writes. Nano has such a model only as a test harness (READ
  Host/Sim/MemStore.lean:15-32: `synced`, `pending`, `crashImage`). No theorem quantifies over it.

### 1.2 Where nano matches the state of the art

- **fsync failure semantics.** A failed append or sync is never retried; every reply of the batch
  is `uncertain` and the resident stops (READ Loop.lean:13-15, 362-365, HOST-4). Darwin uses
  `F_FULLFSYNC` and fails rather than falls back (READ Host/c/file.c:9-12, 84-95). `sync` also
  fails when the file has no name left (the `st_nlink == 0` check). This is the post-"fsyncgate"
  consensus (Rebello et al., "Can Applications Recover from fsync Failures?", ATC 2020) carried out
  in full. Most production systems still get it wrong.
- **Replies after durability, with idempotent retry by content address.** The txId is the call's
  digest. A resend is answered from the journal with the ORIGINAL receipt, never re-judged (READ
  Host/Serve.lean:137-138; `step_journaled`). Past the journal's memory the answer is `uncertain
  forgotten`, never a false `refused` (READ Serve.lean:106-109). This is the end-to-end-argument
  form of exactly-once (Saltzer, Reed, Clark, 1984): at-most-once at the server plus a client that
  resends the same bytes. It is the right design, and Protocol/Attempt.lean is a small, total,
  table-emitted client policy for it.
- **Old shapes refuse to load.** Each base stamps the content-addressed tags of every codec it was
  written under, and a mismatch refuses `shapeMismatch` after the MAC and before any decode (READ
  Host/Base.lean:10-16, 134-136). The literature has no standard name for this. It is closer to
  Unison's content-addressed definitions than to anything in storage engines, which use version
  integers. It is correct and better than versioning.
- **Total loops with lifetime fuel.** No `partial`. The resident's restart loop is bounded by a
  constant no physical run reaches, and exhausting it exits by name (READ Loop.lean:384-397,
  Cli.lean:67-77). For a language whose logic requires totality this is the honest move. It matches
  how CakeML and the Iris/ITree communities treat nontermination (as fuel or coinduction), using
  the cheaper encoding.

### 1.3 Where nano is behind

- **No fork consistency.** A single untrusted server that clients audit is a solved problem class,
  and the bar is **fork consistency** (SUNDR 2004) or **fork-linearizability**, the Cachin–Shelat–Shraer
  line of work. The server may show different members different histories, but cannot join the
  forks again undetected. Nano's follower catches a writer that lies to *it*. Nothing makes two
  members' views comparable: no signed heads exchanged between members, no gossip of
  (steps, chain) anchors. The pieces are present and unwired:
  - `host check --anchor STEPS:CHAIN` (READ Host/Check.lean:25-31);
  - a sponsor-pinned base digest in invitations (READ Machine.lean:532-540);
  - receipts against held heads between Worlds (CHARTER §Scope 3).

  The charter rules the operator *trusted for confidentiality* (§Scope 2), not for integrity:
  the whole reason followers re-execute is that integrity is NOT trusted. So fork detection is
  inside the design's own threat model. INFERRED: this is the largest gap between what the
  follower apparatus is for and what it delivers.
- **No crash-semantic file-system model.** Above, nano is on par with Yggdrasil's *format* layer.
  Below, the IO is "read off". HOST-71 says outright that the mapping of the writer's IO paths onto
  the modelled operations "is read off the code" (decisions/host.md:3244-3253). HOST-69 says the
  same of the loop holding only open/`admitBatch` Worlds (READ Host/Proofs/Trusted.lean:228-232).
  The 2015–2021 verified-storage line made exactly this gap the object of study.
- **Refinement without a top-level observable spec.** IronFleet and Verdi end at a statement about
  *external behaviour*: linearizability of client operations for IronKV, a network-semantics
  safety property for Verdi. `Host ⊑ Kernel` ends at "the World is a fold of Honest steps" (READ
  Refine.lean:170-183). The right top-level spec for a durable single-writer server is
  **durable linearizability** (Izraelevitz, Mendes, Scott, DISC 2016), or its crash-recovery
  cousins in the Perennial line:
  - every acknowledged reply is consistent with the fold of the durable log;
  - after any crash, the recovered state is the fold of a prefix that contains every acknowledged
    step.

  Nano has every ingredient (`open_sound`, `host_run_kept`, replies-after-sync in code) and no
  sentence composing them.

### 1.4 What nano does that the literature has no name for

- **The in-process fuel-restart reopen as a standing pair assertion.** Every 4096 batches the
  writer reopens its own Store from disk through the one open and refuses `reopenDiverged` if the
  reopened state differs from the state it holds (READ Loop.lean:370-397, Cli.lean:67-69). This is
  crash-only software (Candea & Fox, HotOS 2003) turned into continuous translation validation of
  the recovery path (Pnueli, Siegel, Singerman, 1998, for the term). I know of no system that
  validates its own recovery against its live state on a timer. **Novel, and worth a paragraph in
  a paper.** It is cheap, it catches the "recovery code rots because it never runs" class, and it
  costs one open per 4096 batches.
- **One open for writer, follower, tail, check and backup**, with the follower's Store in the
  writer's format (READ Store.lean:22-26, 284-323; Host/Tail.lean:4-9). This is law 1 applied to
  recovery code. The field's systems typically have a recovery path, a replica-catch-up path and
  an fsck that drift apart. Idiosyncratic in its strictness rather than novel, but correct.
- **"Trusted" as a named, refutable premise rather than an axiom** (`CheckpointTrusted`,
  `not_trusted_of_potential`; READ Trusted.lean:73-82, 154-157). It is an honest instinct: name
  the premise every open rests on. As built, the predicate means "origin plus budget bound" and
  admits forged imports (READ Trusted.lean:120-125, READ-HOST F5). So the novelty is the naming
  discipline, not the property. Idiosyncratic.

---

## 2. The architecture judged

### 2.1 The twelve laws, from where Host stands

Load-bearing and correct:

- **Law 2 (Lean decides, Rust moves bytes).** In Host it is real.
  - The Rust client's reply classification is a status-byte lookup in a generated table (READ
    client/src/run.rs:117-129).
  - The C is POSIX calls behind opaque handles (READ Host/c/file.c).
  - Every accept/refuse in Serve and Follow is Lean (READ Serve.lean:126-191, Follow.lean:59-82).

  This is the most valuable law for a verified system. It is the TCB-minimisation stance of seL4
  (Klein et al., SOSP 2009) applied to a userland service. Its sharp corollary is that a wrong
  status byte in Lean reaches users unfiltered: Rust is a faithful amplifier of Lean's mistakes
  (READ-HOST F1). That is the law working as intended.
- **Law 7 (refusals by name).** It makes the system debuggable and the plants specific. It is
  mostly real, and the exceptions are architectural: a status class overridden by a payload string
  (`pageIo`, READ Loop.lean:293-295), and the final `refused` used for "nothing was decided"
  (`stopped`, READ Serve.lean:66-68, Cli.lean:368). The law should say *the status is the verdict
  and the name is the reason*; today it only says *every refusal has a name*. INFERRED: the
  missing half is why F1 exists.
- **Law 3 (bytes end to end, one-pass canonical decoders).** Correct. It is what makes "the
  segment's records are literally the bytes before validLen" (`open_sound`) a meaningful sentence.
- **Law 4's static bounds.** `recordBytesMax`, `worldBytesMax` and `tailMax` are DERIVED from
  kernel bounds with theorems (READ Host/Bounds.lean:47-91). That is better than TigerBeetle, which
  asserts its bounds rather than proving them.

Aspirational (stated, not what the code does):

- **Law 1 (one of everything).** In Host's neighbourhood there are three shapes of "the follower
  re-derives a step":
  - `Kernel.Receive.audit`, which the Host's refinement theorems use;
  - `Protocol.Command.absorbStep`, which the deployed follower runs;
  - the toy machine in host-sim.

  There are also two checkpoints, file and memory, with diverging adopt guards (READ
  Kernel/Receive/Audit.lean:64-76; Machine.lean:437-464; Host/Sim/MemStore.lean:67-85 vs
  Store.lean:452-466). Law 1 holds at the format level (one open, one record codec, one Store
  layout). It does not hold at the level of *what is proved about*.
- **Law 4's resource-lifetime sentence.** "Must be the handle actually in use, never a
  held-but-unused value" is contradicted by the current lock (READ Store.lean:341-353,
  `Writer.hold`). Worse, the charter's own example now describes code that no longer exists
  (CHARTER.md:74-78).

Wrong-headed in light of the field:

- **Law 6's "every theorem statement is read by a second agent".** As a *substitute* for a
  top-level spec it cannot work. A vacuity read checks that a statement is not trivially true; it
  cannot check that the statement is the one the system needed. The project found the first
  failure mode itself (the "disjunct provable from the premises" memory). The second failure mode
  has no detector. A system-level spec is the only instrument that finds "a true, non-vacuous
  theorem about the wrong object" (READ-HOST F2: a refinement about a follower that does not run).
- **Law 8's def/proof file split (measured: Lean v4.30's module system rebuilds importers).**
  It is a reasonable build engineering choice, not wrong. But it is enforced as a law, and
  separation by file has a cost: `IdentityImage.lean` is a definition module whose only consumer
  is a proof (READ Host/IdentityImage.lean:1). Models are being created so that there is something
  to prove. INFERRED.

### 2.2 The cuts

- **Kernel / Host: right.** The kernel's `World.step` is pure. The Host owns persistence, batching
  and the process. The Host "decides nothing" (READ Serve.lean:4-5), and `machine_commits` proves
  it (READ Proofs/Serve.lean:71-84). This is the cleanest cut in the system and the one a reviewer
  would praise.
- **Host / Protocol for the follower: wrong.**
  - Host owns the follower's process, Store, loop and persistence (READ Host/Follow.lean).
  - Protocol owns the follower's decision (`Command.step`, `absorbStep`).
  - Kernel owns a different follower decision (`audit`) that Host proves things about.

  The follower is the *other half* of the system's correctness argument: the writer is honest
  exactly when its followers agree. Yet no layer owns the follower as one object, so the theorem
  that would state the system's purpose ("an honest writer's pages absorb to the writer's World; a
  dishonest one is refused") falls between Host and Protocol and does not exist (READ-HOST F2).
  The design pays for a cut it should not have made.
- **A missing cut: an abstract Store interface with crash semantics.** The loop is already generic
  over a `Store` record of two IO actions and a `Port` record (READ Loop.lean:37-55, 105-125), and
  the simulation drives it over memory (READ MemStore.lean:21-28). That is one step away from the
  Interaction Trees discipline (Xia et al., POPL 2020): make the effects an event signature, write
  `serve` as an ITree, interpret it in a disk-with-crashes model, and prove the interpretation
  refines the spec. The cut that should exist is "Store semantics as a Lean model with crash
  points, used by proofs AND by the simulator", in place of the present "Store as IO, simulator
  beside it".
- **Host / Hosting / Ops: fine.** Ops renders units from Host's exit table (READ
  Host/Exit.lean:16-18). Nothing decided twice that I saw.

### 2.3 Single writer, receipts between Worlds, no agreement engine

**The right call for this system, not a deferral.** It is the same call as Calvin (Thomson et al.,
SIGMOD 2012) and the deterministic-database line: decide the order once and make execution a pure
function of it. Nano goes further and has no replication of the decider at all, which the charter
justifies by measured failure: an agreement mesh with one host (CHARTER §Scope). Once the
transition is deterministic and the log is authenticated, agreement buys availability, not
integrity. Integrity comes from re-execution, and availability for "two friends + a hosted
resident" (THE BAR) is a supervisor restart.

The deferral that IS hiding in this choice is fork consistency (§1.3). Without agreement, the
integrity guarantee to a *group* of members requires that their views be comparable. SUNDR got
fork consistency with one server and signed version vectors. Nano has signed members, a chain head
per step, and invitations that carry pins. Comparing views is weeks of work, not an agreement
engine. INFERRED.

### 2.4 Judge / gates / census / plants as a verification method

- **Plants are mutation testing applied to proofs** (DeMillo, Lipton, Sayward, 1978, for mutation
  testing). They are a sound check of *non-vacuity*: a theorem whose premise is unsatisfiable, or
  whose conclusion is implied by its premises, survives every mutation of the code. That is
  valuable, and I have seen it catch real vacuity in this project. It is hollow in two specific
  ways I found in Host:
  - **A plant can be green under the very regression it names, if it reconstructs its own context.**
    The second-writer plant re-locks in its own frame and calls `wr.hold` itself (READ
    Host/Sim/File.lean:76-79), so it would stay green if `serveVerb` dropped its hold. The real
    tooth is the Ops plant that runs a live binary (READ Ops/Plants.lean:797-835).
  - **A tooth with unwitnessed premises is a falsifier that may not falsify.**
    `host_step_folds_tooth_censor` says of itself that its premises' joint satisfiability "is not
    witnessed in Lean" (READ Refine.lean:377-383).
- **Compared to CompCert, seL4 and IronFleet.** Those establish trust by ONE top-level statement
  plus a small, explicit TCB:
  - CompCert (Leroy, POPL 2006 / CACM 2009): semantic preservation of the whole compiler.
  - seL4: functional correctness of the C against an abstract spec, then security properties
    proved of the spec.
  - IronFleet: the implementation refines a TLA-style spec, plus liveness.

  Thousands of lemmas exist in service of that one statement, and the trust question reduces to
  "do you believe the spec and the TCB?". Nano has thousands of theorems, a census of their axioms
  (good: that IS a TCB statement for proofs), and no top-level statement. A mechanised-metatheory
  practitioner would say:
  - the census tells me what the proofs assume, not what they establish;
  - "every theorem has a plant" tells me each theorem is non-trivial, not that the set covers the
    system;
  - without a top-level theorem, the set's coverage is unknowable, and the defects I found are
    exactly coverage defects (wrong object, read-off links, model beside code).
- **Should one exist?** For Host, yes, and it is writable (§4). For the whole system, a *small*
  number of top-level statements is the right target, not one, because the system has several
  observers: the writer's clients, a member's follower, a sponsor's invitation. Each deserves one
  spec. Nano has the vocabulary (Turn, receipt, `Settle`, `Honest`) and not the sentences.

---

## 3. The details judged (Host)

### 3.1 Three choices I would defend at a top venue

1. **The pure batch function under a durable shell, with replies only after fsync and no
   fsync-retry** (READ Host/Batch.lean:1-22, 74-92; Loop.lean:346-368).
   - `admitBatch` is total and pure, and generic in World, step, request and note.
   - `staged_rooted` proves the staged log is a rooted run to exactly the World kept (READ
     Host/Proofs/Batch.lean:63-66).
   - `step_submit` proves the per-request decision is `judge`'s (READ Proofs/Serve.lean:98-117).
   - The shell's only obligations are append-then-sync-then-reply and "uncertain on any failure".

   That is the shape that SOSP/OSDI verified-storage papers wish their baseline systems had. At a
   venue I would present it as "the decision is verified; the shell is ten lines and fsyncgate-correct".
2. **The authenticated chained segment with a theorem over arbitrary bytes** (READ Host/Log.lean;
   Proofs/Open.lean:57-60).
   - `open_sound`: for any bytes on disk, the opened World is the fold of records whose encoding
     is literally the prefix before `validLen`. That is a recovery theorem against an adversarial
     disk, stronger than the usual "a crash at any point leaves a consistent state".
   - The documented undecidable case (corruption inside the last frame looks like a torn write,
     READ Log.lean:22-24) is stated, not hidden.
   - The `foreignSegment` / `foreignOrigin` / per-position index MACs close the splice attacks that
     Pillai-style studies find.
3. **Continuous self-validation of recovery: the fuel-restart reopen and its pair assertion**
   (READ Loop.lean:370-397). Defended in §1.4. It is the one idea in Host I would expect other
   systems to copy.

### 3.2 Three choices I would be embarrassed to present

1. **The writer lock as an advisory `flock` on a separately held fd, kept by a dummy re-lock, with
   no fencing in the log** (READ Store.lean:19-20, 341-353, 379-380; Cli.lean:386, 407).
   - Field's terms: mutual exclusion of writers is a *safety* property of the log, and the
     literature's answer is that a lock is not enough. You need a **fencing token** or epoch
     carried in the data, checked by the storage, as Chubby's sequencers do (Burrows, OSDI 2006),
     and as every lease-based system learned.
   - Nano's correctness argument against a second writer is "the second `openWriter` gets
     `locked`". Its lifetime argument is "the compiled code happens to keep the handle alive
     because we call a no-op on it at the end". The project already paid for this class once (law
     4's own story).
   - What a strong student would build: a **writer epoch** in the base and in each segment header
     (the header is already MAC'd and positional, READ Host/Base.lean:178-215). `openWriter` bumps
     it durably (new base or header) before its first append. `commitBatch` appends under it, and
     open refuses a frame chain that crosses an epoch without a base naming it. The lock becomes a
     liveness device; safety moves into the bytes, where the theorems already live. Plus: make the
     lock the append handle again, so the "in use" clause is true by construction. **About a week**,
     plus a re-genesis, which the charter prices at zero.
2. **A refinement stated against a follower that does not run, an IO loop that is "read off", and
   a crash story proved over byte arrays instead of a disk model** (READ Refine.lean:243-254, 451-461;
   Trusted.lean:228-232; decisions/host.md:3244-3253).
   - Field's terms: the theorems are an *implementation-to-abstract-step* refinement à la IronFleet
     with the *interface* missing at both ends. The upper interface is a client-observable spec
     (durable linearizability). The lower is the effect semantics (an ITree or a disk model with
     crashes).
   - The component in the middle is correct. It is not connected to what users observe or to what
     the code does.
   - What a strong student would build:
     - (a) restate `serve` as an interpreter over an effect signature (Store.append, Store.sync,
       Port.recv/poll/send) that already exists as records;
     - (b) give a crash semantics in which a crash keeps `synced ++ prefix(pending)` (the very
       `MemStore.crashImage`, READ MemStore.lean:30-32);
     - (c) prove durable linearizability of replies against `World.fold` of the log.

     (a)+(b) is a month. (c) is a quarter, because it needs an invariant across the async seal Task
     and a statement about the reply buffer. A full FSCQ-grade POSIX model (rename atomicity,
     directory fsync ordering) is a year, and is the right *not yet*: keep those as named OS
     assumptions, as HOST-71 already does.
3. **`CheckpointTrusted` / `WriterLife`: trust as a predicate over arbitrary inputs, and a thin
   adopt with no history** (READ Trusted.lean:76-82, 239-248; Follow.lean:117-133).
   - Field's terms: this conflates a **state invariant** (the World is within the size and budget
     bounds: a type-level fact that should hold of every World the Store type can contain) with a
     **provenance claim** (this state has an authorized history). The literature handles provenance
     with signed heads and inclusion/consistency proofs (Certificate Transparency's signed tree
     heads, the Merkle-log line of work), or with per-member signed checkpoints (the SUNDR/SPORC
     line).
   - As built, "trusted" holds of any World a crafted carried file makes, with any origin (READ
     Trusted.lean:120-125). `writer_life_trusted` quantifies over arbitrary segment and index bytes
     and an arbitrary admitted list. The member's actual case, an adopted base, is exactly the one
     it does not cover.
   - What a strong student would build:
     - (i) the size/budget bound as an invariant carried by a subtype of World (or checked at every
       decode, which the codec almost does);
     - (ii) provenance as a **member-countersigned base digest**: a full follower that reached step
       S signs (S, chain, base digest), and a thin member adopts only a base countersigned by a
       sponsor it trusts out of band. The machinery is mostly there: the invite pins a digest the
       sponsor's own follow verified (READ Machine.lean:532-540).

     **About a month.** The value is that "trusted" would then mean what a reader assumes it means.

---

## 4. What to do

### 4.1 The one structural change: a writer–follower agreement theorem over BYTES, with one re-deriver

**The change.** Delete the second re-deriver. Either define `Protocol.Command.absorbStep` as
`Kernel.Receive.auditStep ∘ decode`, or retire `audit` in favour of `absorbStep`; one of them, not
both. Then state and prove, at the deployed `Host.Deployed.X`:

> For every World `w` with `Kept w` and every batch `qs`, let `l` be what `(machine X).admitBatch w qs`
> stages and `P` the log page `Page.build` serves over the durable records of `l` (events
> `Page.stepEvent`, with the writer's stated steps and chain). Then `Command.absorbPage X w P.events
> P.steps P.chain _ = .ok (((machine X).admitBatch w qs).1, …)`.
>
> Conversely (already largely present as `absorbStep_step`, `absorb_admits`), whatever a follower
> absorbs is an `Honest` fold.

**What it would make true.** This is the system's purpose statement for Host: *the follower
reaches exactly the writer's World on an honest log, and on any log it accepts it holds only steps
its own kernel took.*

- It closes READ-HOST F2.
- It puts law 1 back in the place where it matters most.
- It turns the rows' end-to-end test of follow (today the only evidence for completeness on Turns
  and judged refusals) into a theorem.
- It is the composable lemma the top-level durable-linearizability statement of §3.2(2) will need
  on the member side.

**Cost.** Weeks, not months. The cancel half already exists (`absorbStep_cancelEvent`, READ
Protocol/Proofs/Command.lean:819). The codec round-trip it needs is proved
(`eq_callBytes_of_decodeCall`, READ Codec/Proofs/Deployed.lean:39-41). `Page.build`'s walk has
coherence lemmas (READ Host/Proofs/Coherence.lean:1-45). What is new is the Turn arm (`submit` of
the decoded call re-derives the admitted Turn: `receive` is deterministic, which the kernel
proves) and the page-level induction. Ratio: the highest in the layer.

### 4.2 The one thing to stop doing

**Stop proving theorems about models standing beside the code.** The pattern recurs:

- `WriterLife` (abstract events, READ Trusted.lean:239-248);
- `IdentityImage` ("no deployed consumer", READ Host/IdentityImage.lean:1);
- `memCheckpoint` (a second checkpoint whose adopt guard differs, READ MemStore.lean:67-85);
- the host-sim toy machine (READ Host/Sim/Run.lean:46-52);
- `Kernel.audit` as "the follower's audit".

Each is reasonable alone. Together they produce green proofs whose connection to the binary is a
docstring saying "read off". The project's own rule ("iterate inside the substrate, never beside
it") forbids this. When a property cannot yet be stated over the deployed function, the honest
artefact is a named, cv-tracked gap, not a model that the next reader will cite as if it were the
code. Where a model is genuinely needed (the crash semantics), make it the ONE semantics that both
the simulator and the proofs use, as in §2.2's missing cut, so that it is the substrate rather than
beside it.

### 4.3 Grade

On a scale where A is "publishable as a verified system at SOSP/OSDI today" and C is "a careful
system with tests":

- **Format and recovery layer: A−.** The log, torn/corrupt, `open_sound`, shape stamps, fsync
  discipline and continuous self-validation of recovery are at or ahead of the field's practice.
- **Writer refinement: B.** `step_submit` and `machine_commits` are real and over the deployed
  handler. The loop above them and the follower beside them are not connected.
- **System guarantee: C+.** There is no statement of what a client or member may rely on. The
  follower's completeness rests on rows. There is no fork consistency. The writer lock's safety
  rests on a no-op call.

**Overall: B−.** Host's components are verified at a standard most systems never reach, and its
recovery engineering includes one genuinely new idea. But it has no top-level statement composing
those components into a guarantee anyone outside the layer can hold, and two of the theorems that
look like that guarantee are about objects the binary does not run.
