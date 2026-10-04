# SCHOLAR-FN — fn as Mini's persistent storage node: what fn is, what Mini uses, what Mini will need, and contract shapes (2026-10-04)

Read-only scholar report for the Mini root, which will write the Mini→fn requirements/contract document.
Nothing in `~/dev/fn`, the live node, or any Mini tree was modified. Mini was read from a fresh clone of
`github.com/emberian/minidregg` at `5df8bb07` (scratch: `…/scratchpad/mini-fn-scholar`).

## How to read this file

**Tags.**
- **READ**: I read it at source. For fn that means `origin/dev` = `39a0db8cf` (2026-10-04 00:53), or the named branch. For Mini it means `5df8bb07`. For hbox it means a read-only `ssh` (`systemctl status/cat`, `ls`, `ps`).
- **RECORD**: a document, register or evidence file says it. I did not re-run or re-derive it.
- **INFERRED**: my reasoning from the READ/RECORD facts.

**FN-nn ids.** Every claim about fn carries an `FN-nn` id so the fn session can check it against its tree claim by claim. It offered to; please send it §1 and the FN-ids in §3–4. Claims about Mini carry `MI-nn`.

**Caveat on fn's tree.** The local `dev` checkout is 57 commits behind `origin/dev`, so all fn source is read from `origin/dev` with `git show`. D49 is read from `integrator/d49@38d8e30c0`, and `specs/applications.md` from `origin/lane/apps@23d02fe96`. Neither branch is on dev yet.

---

## 0. Short answer

- **What fn is.** fn is an append-only, crash-recoverable, signed-exact-bytes **event log and feed store** whose interface is NNTP plus a local control socket. ACL2 makes every decision; an SBCL host does the I/O.
  - It is not a key-value store.
  - It has no authenticated state map: no Merkle root over its contents, no inclusion proofs.
  - It has no cross-node order and no consensus.
  - It already has the hard parts a storage node needs:
    - acknowledge only after the barrier;
    - accepted, refused and uncertain kept distinct;
    - idempotent resend of the same bytes;
    - a chained record log with named open refusals;
    - an export/import theorem;
    - a store-scoped, versioned consumer cursor.
- **What Mini's model needs from it.** The fit is **archive + feed + transport of exact bytes**:
  - finalized blocks and receipts;
  - sealed checkpoints at a cadence;
  - inter-domain messages, including deal/escrow traffic;
  - audit/replay kits.

  The fit is not "the hot store under every admitted turn", at least not in 6.6.0. On record, fn's per-record heap cost, its open time at 40k records, a live node capped at 32,768 transactions, and a single serialized owner at 36 POST/s on hbox's ZFS all rule out the hot path until the D41 page representation lands (§3.2).
- **Proof status.** fn's served durability theorem for the format-10 record log is `fn-lgu-acknowledged-article-is-recoverable-at-every-crash-point`. It exists, and it is **not certified at current source** (FN-31).
  - The better-known byte-store crash keystones (`fn-bs-*`) are over the retired per-file layout. fn's own generated view marks them "unreachable in composition" (FN-32).
  - No image built from current fn source has run yet (FN-40).
  - A contract the root writes today is therefore a contract against **specified source with earlier native evidence**, not against a qualified release.

---

## 1. What fn IS today

### 1.1 Identity and architecture

- **FN-01 (READ, `README.md`, `docs/architecture.md`).** fn is "a news server for people and programs". It speaks NNTP (RFC 3977/5536/5537, STARTTLS 4642, AUTHINFO 4643), and "ACL2 makes every decision". Every answer is accepted, refused or uncertain.
  - The core is `step(state, event) -> (state', effects)`.
  - A Common Lisp host performs socket and disk I/O and reports outcomes.
  - The core never receives arbitrary Lisp from a client.
- **FN-02 (READ, `docs/architecture.md` §Purpose).** The stated long-term direction is a "high-assurance persistent event-log substrate between Robigalia systems, with minidregg and breadstuffs layered on or integrated with it (ember, 2026-09-30)". The doc also states that this does "not claim those integrations are complete or select a replacement wire protocol".
- **FN-03 (READ, `docs/architecture.md` "Three representations").**
  - Articles and statements are **portable**.
  - Journal sequence numbers, disk offsets, NNTP article numbers, cache contents and paths are **local**.
  - Replication exchanges portable objects, never database pages.
- **FN-04 (READ, `integrator/d49:planning/decisions.md:1771`).** D49, ember, verbatim: "6.6.0 is *for* being good enough to start treating as a foundational component for the rest of the distributed OS / mini." Its consequences:
  - The remote consumer is in the cut, built with its producer.
  - A zmq-pattern surface (pub/sub, req/rep, push/pull, pair) is *permitted*, generated rather than hand-written.
  - The minidregg-facing contract in `specs/applications.md` is part of the cut.
- **FN-05 (RECORD, swarm plan quotes).** Ember's words for the destination:
  - "semantic web hyperredis … disguised as a newserver … bounded-metered-backflow-safe/DoS-resilient/QoS-operable";
  - "the redis of it all";
  - "the persistent event log between systems".

  "Persistent storage node" in the brief corresponds to these.

### 1.2 Data model

- **FN-06 (READ, `specs/storage.md` STO-001/027, history-classes table).** The committed record log is authoritative, and indexes are derived from it. Durable classes:
  - article records (exact authored source, D01);
  - retention undertakings and releases;
  - identity/keyring evidence;
  - consumer positions;
  - topic admission;
  - BP handoffs;
  - the allocation frontier;
  - configuration history;
  - checkpoints, which are derived and never authoritative.

  The served "catalog" (`fn-cat`) holds Message-ID binding, local numbers, per-version visibility and retained octets as columns.
- **FN-07 (READ, D01 in `decisions.md:95-117`).**
  - The durable source of a native article is its **exact authored bytes**, signed.
  - Path, Xref, Injection-* are separate projections. Xref is rendered at reply time and never stored.
  - `fn-rcompat-served-payload-inserts-one-line`: the served octets are one Xref line followed by the stored octets unchanged.
- **FN-08 (READ, D09).** Native authorship requires Ed25519 **and** ML-DSA-65; there is no classical-only fallback. Signing is randomized (ML-DSA), so a re-sign is a different carrier (see FN-24).
- **FN-09 (READ, D27 `decisions.md:1182`; `books/article.lisp:25`, `books/frame-octets.lisp:30`).** "A constant that bounds data is a defect."
  - Article size, groups per article, transactions, history octets and similar quantities are operator profile fields, refused by name at the operator's bound.
  - Codec ceilings are about 4 GiB: `*fn-article-max-octets*` = 4,261,412,864 and `*fn-frame-max-payload*` = 2^32−1.
  - Work per request stays bounded.
- **FN-10 (READ, `planning/experiments/e1-e2-agent-exchange.md`; Mini `docs/FN-PORTABLE-E1.md`).** An application payload travels **as an RFC 5536 article**. In the E1/E2 envelope that is a fixed MIME header set plus canonical base64 at 76 characters per line, about 4/3 overhead.
  - There is no opaque-record kind outside the article grammar. The control socket's `hybrid-author` takes a source blob, but the source is still an article.
  - **No mutable key-value cells.** Withdrawal/cancel is a record (D29); there is no update in place.
- **FN-11 (READ, `planning/decisions.md` D08 row).** fn's recommendation for its own portable objects is "restricted deterministic CBOR, exact schema versions, bounded parsing; unknown objects may be carried opaquely but not interpreted as authority". It is still an open decision (`docs/cbor-interop.md` exists).

### 1.3 Persistence and durability

- **FN-12 (READ, `specs/storage.md` "Commit protocol").** The phases are validate+reserve+stage, then make object bytes durable, then make the commit record durable, then publish and reply.
  - STO-003: success only after the durable commit result. Completions name transaction and generation, so stale or duplicate completions cannot publish.
  - A disconnected requester does not cancel a durable transaction.
- **FN-13 (READ, STO-033).** One batch of prepared commits is in flight at a time.
  - Members are acknowledged only after the batch's barrier, in prepare order.
  - The batch closes on log-thread return or on operator bounds, never on a timer.
  - A **failed barrier makes every in-flight member uncertain and fences the store.** Recovery holds the committed records plus a prefix of the batch.
- **FN-14 (READ, STO-004/005).** A known abort and an indeterminate I/O result are distinct. After an indeterminate result, mutation is fenced and recovery runs.
  - "It is valid for an unacknowledged transaction to appear after recovery; it is not valid for a modeled acknowledged commit to vanish."
  - Recovery yields an invariant-preserving history containing every acknowledged transaction and no partial one.
- **FN-15 (READ, STO-009/022, "One format").** Format 10 is a single **record log**: `journal/000000.log` is the genesis frame (KIND 3), followed by chained segments.
  - Each entry is self-checking and chained to its predecessor by `fn-frame-digest` (BLAKE3).
  - There is one fdatasync per batch.
  - The open scans the segments and finds every acknowledged record, or refuses by name: `log-chain-broken`, `history-short-of-checkpoint`, `checkpoint-damaged`, `log-damaged at=SEG:OFF …`.
  - A torn tail is recovered to the last complete entry, with a log line.
  - Damage to committed data followed by valid entries is **refused**, never silently truncated. The operator repair `store ROOT recover --repair truncate SEG:OFF` quarantines the segment first.
- **FN-16 (READ, `specs/storage.md` "committed-history boundary").** **Not detected:** replacing the whole store with an older valid copy. That needs a freshness anchor (D14), and the configuration history and BP stores are also outside the check.
  - Mini's own Store already has a sibling head anchor for exactly this threat (MI-04).
  - INFERRED: fn is weaker than Mini's current SQLite store on whole-store rollback.
- **FN-17 (READ, `specs/failures.md`).** The named assumptions the durability proofs are conditional on:
  - A-DURABILITY: a completed barrier preserves the bytes and namespace updates.
  - A-WRITE-ISOLATION.
  - A-HOST: the host reports honestly. It is constrained, and no theorem takes it as a hypothesis yet.
  - A-CRYPTO-TRAILER: a tear never validates unless exact, at about 2^-128 per chosen pattern.
  - A-CHECKPOINT-PUBLICATION and A-RECOVERED-OPEN.
  - A-CRYPTO-NATIVE: the BLAKE3 C library computes BLAKE3.
  - A-SIG-NATIVE: PQClean ML-DSA-65.
  - A-TLS-NATIVE and A-SBCL-RUNTIME.

  Power-loss behaviour is "not qualified".
- **FN-18 (READ, D14 text).** The disk failure model is "pure crash model first; qualify one Linux local-filesystem profile before deployment durability claims". The release checklist's power-loss rig for the log route "was NOT RUN" (`planning/current.md` M5, RECORD).

### 1.4 History and versioning

- **FN-19 (READ, STO-010 table).** Only three capabilities remove durable state:
  - **P (packing)** keeps the identical record list. On format 10 this is `store compact`: checkpoint, rotate, and drop the covered segments.
  - **H (history compaction)** replaces a prefix by a summary that must answer every future decision identically. It is **not implemented** and needs D13.
  - **C (content reclamation)** removes payload bytes only after the retention obligation is released and no reader pin or BP handoff holds them. On the log it is `store reclaim`. Article *records* stay (anti-resurrection).
- **FN-20 (READ, same table; D03).**
  - **Default lifetime is forever:** D03 is "keep until explicit authorized release, no automatic expiry; refuse new obligations at capacity".
  - Local numbers are never reused, even for removed articles. The allocation frontier is monotone.
  - The anti-resurrection summary "does not exist yet".
  - Under D03 with no release, "every class above grows monotonically until admission refuses by name (`:unaffordable`)".
- **FN-21 (RECORD, fn session reply; STO-010 "C … Not implemented for article content" vs M5 `store reclaim`).** Reclaim works **offline** today. Live reclaim funding is being decided now. RET-008 per-group expiry is defined as an authorized release.
  - The two statements in the tree read inconsistently: "C … not implemented for article content" in STO-010, against `store reclaim` certified in M5.
  - The fn session should say which one is current.
- **FN-22 (READ, `specs/consumer-progress.md` "Identity and version boundary"; `books/store-genesis.lisp` header).** Genesis records:
  - a 32-octet CSPRNG node identity;
  - schema digest, profile digest and history salt;
  - created-at and image revision.

  The cursor names a `history-id` and an `incarnation-id`. Incarnation changes on copy, restore or replacement. Crash and replay keep both. Compaction keeps them only with an explicit position mapping.
  - INFERRED: this is the store-incarnation identity that the 09-24 "store identity on the wire" candidate said did not exist. It exists now in the cursor. Whether NNTP exposes it (`XFN-STORE`) I did not find.

### 1.5 Format, re-genesis, backup

- **FN-23 (READ, D34, STO-028, release checklist row 1).**
  - There is one store format, `fn-store-10`.
  - **No migrations.** D38 (a reader of a previous format) was withdrawn.
  - Every format change is a fresh deploy. `store export/import` carries data across one.
  - A foreign format is refused at open: `reason=store-format … redeploy fresh`.
  - At the cut the format is renamed `fn-store-1` (checklist §2b row 1) and then frozen.
  - The 09-29 genesis-schema change (`00a3713c4`) probably makes the next deploy a re-genesis (RECORD, swarm plan §2 item 7; fn reply).
- **FN-24 (READ, STO-028, PRF-205, PRF-370).**
  - `store export DIR` streams the committed history chunk by chunk, with a BLAKE3 MANIFEST rendered by ACL2.
  - `store import` builds a new store **with its own genesis**, checks the archive in two passes, and admits it through the ordinary open.
  - Proved and **certified**:
    - `fn-sxp-import-of-export-replays-the-same-history` (PRF-205);
    - `fn-sxd-crash-is-incomplete-or-complete` (PRF-370): a crash leaves no MANIFEST or a complete archive.
  - Stated limit: the two-pass check "does not bind every record byte across passes … not an atomic snapshot of a mutable archive".
  - INFERRED: an import has a new genesis, so it gets a new node identity and new history/incarnation ids. Every consumer cursor is refused after a restore. There is **no rebase command** (FN-29), so consumers re-register.

### 1.6 Replication and federation

- **FN-25 (READ, `specs/replication.md` REP-001..005).**
  - Nodes exchange immutable objects and scoped statements.
  - Ingestion tolerates duplicates and reordering. Set union of validated facts is associative, commutative and idempotent under a fixed validation profile.
  - Forks and conflicting claims "do not disappear through arrival order".
  - The claim explicitly excludes identical local numbering, policy, quotas or visibility.
  - Transports are NNTP peering (CNS-004), BPv7 with TCPCLv4 (F7: 10 MiB ADU validated), and carried media.
  - **No consensus, no total order, no state-machine replication, no Merkle reconciliation yet**: REP-004 says a canonical set representation would be needed.
- **FN-26 (RECORD, fn reply; READ, D12/A-PEER).** Peers are trusted transport peers in the first trust profile (decision 2026-09-23 "first cross-silo trust boundary"). Releasing forwarding responsibility needs committed matching evidence (D12, open). There is no failure-domain or replica-count policy.
  - D36: the public node peers with nobody yet. The hbox node's record says "peered with fn.fg-…" (truncated in `current.md`; I did not verify the live peering).

### 1.7 Query and consumer model

- **FN-27 (READ, `specs/storage.md` STO-027; `planning/current.md` P3/T17).**
  - NNTP reads (GROUP, LISTGROUP, ARTICLE by number or Message-ID, OVER, HDR, NEWNEWS) go through the catalog over a pinned committed view.
  - `fn-own-pinned-view-survives-other-post`: a reader's view answers the same across others' posts, and numbers are never reassigned. Its caller bridge is pending.
  - Known live defects: NEWNEWS/HDR/XPAT 8-entry cache loop "pins the owner", and the web face serves one connection at a time (swarm plan §1).
- **FN-28 (READ, `specs/consumer-progress.md`, `origin/lane/apps:specs/applications.md`).** The local consumer cursor `fncu` v1 is 346 octets max.
  - It names history, incarnation, consumer, principal, query, query/view version, registration epoch and scanned position.
  - A cursor from another store, incarnation or epoch is refused before any ack.
  - **Poll** is a read.
  - **Ack** declares only the consumer's own processing, and is monotone and idempotent. `position` settles an uncertain ack.
  - **Wait** sleeps on the owner's commit signal. At most 12 waits run at once, and a 13th is refused as `waiters`.
  - Delivery is at least once. **The application owns dedup, inbox, transition and outbox before ack.**
  - Withdrawals arrive as withdrawal events.
  - **A cursor creates no retention pin**: reclaimed content shows as an explicit gap.
  - Transport is FNCT frames over a mode-0600 Unix socket with same-UID peer credentials.
- **FN-29 (READ, applications.md "Not yet").** Not yet built:
  - views that change and rebase (the local profile fixes query v1/view v0 over one group; there is no `rebase` command);
  - multi-group selection;
  - retention pins;
  - a non-NNTP inter-node protocol;
  - competing consumers (push/pull).
- **FN-30 (READ, applications.md "Remote consumer"; `lane/apps@25dd82d5a`).** The remote consumer is on a lane, not on dev.
  - It runs over a TLS listener, as the account's bound consumer.
  - Operator controls stay private, and register/rebase/unregister are refused (`operator-control`).
  - The proved ACL2 keystones are `fn-crbd-route-is-the-accounts-bound-operation`, `fn-crbd-operator-controls-stay-private` and `fn-crbd-another-login-is-refused`. There is an interim per-connection funding draw.
  - Native evidence is "pending".

### 1.8 Proofs: what ACL2 proves, about what, and at which coordinate

fn keeps four coordinates apart: **implemented**, **proved** (certified at current digest), **qualified** (on a tested image) and **deployed**. `planning/current.md` is generated from them. Read it, not prose.

- **FN-31 (READ, `planning/proofs.json` PRF-936; `books/store-log-durable.lisp:865,891`).**
  - **The served durability keystone** is `fn-lgu-acknowledged-article-is-recoverable-at-every-crash-point`: an article in the owner layer's acked list is held by the kernel recovered from every admissible crash image of every crash point of the append, fence and extend programs. This includes a barrier that failed after landing, the "fsyncgate" outcome.
  - Its recovery half is `…-at-every-cut-of-recovery`.
  - Status: **`uncertified-at-current-digest`**.
- **FN-32 (READ, `planning/current.md` P10).** P10 ("every cut is a model crash point") cites `fn-lg-open-program-keeps-the-relation-at-every-cut`, also uncertified at the current digest. Three coordinates sit outside it:
  - `log-truncated`;
  - `recovery-stage-unlinked`;
  - `fnn-log-complete-rotation`, which runs with "no cut and no model step".

  The host's syscall order is checked "as source text, not proved". The per-file `fn-bs-*`/K0 family is "the byte model's record, marked unreachable-in-composition in PRF-041".
  - INFERRED, a correction to the 10-03 audit's framing. The deferred `fn-bs-acknowledged-record-survives-byte-crash` and its siblings matter as proof-base health. They are **not** the theorem Mini would lean on for durable-after-ack on format 10. FN-31 is.
- **FN-33 (READ, `current.md` table).** Capabilities at `origin/dev`:
  - **P2:** 240 only after a consumed completion, else uncertain, never a refusal. Certified.
  - **P5:** a connection-local fault costs one connection, and a shared-action fault fail-stops. Certified.
  - **P6:** live reconfiguration; crash recovers the live or the whole published generation. Certified.
  - **P9:** refuse the unaffordable at budget (`fn-sbud-prepare-refuses-at-budget`). Certified.
  - **M5:** compaction/reclaim decided in ACL2 (`fn-lgr-decide-checkpoints-the-rewrite`). Certified, lab-only qualified.
  - **P4:** idempotent duplicate vs conflict, `fn-pb-same-article-is-answered-already-stored`. "Closure moved", not certified at the current closure.
  - **P3:** pinned view. Caller bridge pending.
  - **P10:** uncertified.
  - Nothing is qualified or deployed at current source.
  - `proofs.json` counts: 401 certified, 147 uncertified-at-current-digest, 140 planned.
- **FN-34 (READ, `docs/architecture.md` "Trust boundary").** The digest left the trust boundary: BLAKE3 is a guard-verified ACL2 function (format 10), checked against published vectors as evidence. Collision and preimage resistance remain the assumption A-CRYPTO.
  - Signatures (Ed25519 via libsodium, ML-DSA-65 via PQClean), TLS (OpenSSL/LibreSSL), Roughtime SHA-512, the OS, SBCL and the C ABI are trusted.
  - The fn reply's "signatures/TLS/OS are trusted primitives" matches this.
- **FN-35 (RECORD, `FABLE-FN-SESSION-20261003.md` §Short version 5–6; swarm plan §4 wave 2).** Recorded soundness wounds:
  - **The served read path is unproved.** `host/owner-host.lisp` routes reads through `fn-av-mca-read-span`, a `:program`-mode generated copy, instead of `fn-mca-read-span` with its `-keeps-funded` theorems. PRF-1287 records the proof as owed.
  - **A keystone citation was removed and never restored.** `fn-cat-may-seal-is-the-prepare-gate` was removed from `definterface fn-owner-cat-may-seal`. The keystone that replaces it is still owed.
  - **"Funded" is unpriced.** `fn-owner-output-tariff-preview` returns `:unpriced`. On cost obligations: 1,442 of 1,449 dispatched entries have none. The fn reply says "1 of 28 command families priced". The Fable audit (10-03) said 0, so lane/apps' tariff work may account for the difference. Unreconciled.
  - **The world deferred 85 theorems.** A 2M-step loader cap refused only two of them; all 85 certified separately on 10-03 (FN-41).

### 1.9 Performance on record

(RECORD, `planning/release-v6.6.0.md` §2. These were measured on dev `33bbfae9c` and `d5ab87aecc40`, 2026-09-27/28, on a loaded hbox.)

| fundamental | figure | bar status |
|---|---|---|
| **FN-36** F3, POST durability cost | 0.30 fsync/POST on NVMe and 0.34 on ZFS at 8 posters; **257 POST/s on NVMe, 36 POST/s on `tank` (ZFS)**; 117–225 POST/s on the edge; design target 0.125 at batch 8 (gap F3-G open) | OPEN |
| F1, heap per stored octet | 1.0–1.3 B per payload octet **+ 3.6 KB per record after reopen** (9.5 KB while posting); 1,000-post reopen at 60 MiB RSS | MET |
| F6, open at scale | **20k articles open in 7.9–8.1 s (850 MiB peak); 40k in 16–22 s (1.2–1.7 GiB peak)**; compaction of 40k × 2 KiB takes 98–139 s at 4.7–7.5 GB | OPEN |
| F2, reads | ARTICLE 1.1–1.2 ms; OVER 1–2000 takes 372–386 ms at N = 10,000 | OPEN |
| F4, latency | control p99 6.1 s and max 8.0 s under the mixed hour; read max 10.35 s | OPEN |
| F8, memory | 672 MB reserved empty, 1,407 MB after 1k posts, against a 256 MB bar | OPEN |
| F5 / F7 | an idle connection costs 7.7–9.2 KiB; BP 10 MiB ADU validated | MET / OPEN |

- **FN-37 (READ, STO-001/033; `docs/architecture.md`).** **One owner serializes all mutations.** "Only one shared-state transaction commits at a time." Connections stage input concurrently within quotas.
- `store digest` of a 1,000,000-record store fits in 5.9 GB (STO-028).

### 1.10 Operational model (hbox read-only)

- **FN-38 (READ, ssh hbox).**
  - `fn-node.service` runs node #2, image `fn-a3553e6b4a23`, source dev `a3553e6b4` (09-28). It is active since 2026-09-28 12:33 EDT.
  - It runs as user `hbox`, `ProtectSystem=strict`, `ReadWritePaths=/tank/fn/node`, `MemoryMax=2G`, `Restart=on-failure`.
  - The process is SBCL `--dynamic-space-size 1397` on `fn-host.core`, currently 43.5 MB RSS.
  - The listener is LAN-only (`192.168.50.39:119/563`), with auth required and `protected_only`.
  - The store at `/tank/fn/node/store` holds **468 KB in total**. The log holds `000000.log` (genesis, 259 B) and `000002.log` (1 MiB preallocated, last write **2026-09-28 13:04**).
  - **No `[resources]` section in `fn.toml`**, so the node runs unaccounted, which matches the fn reply.
  - The control socket is `store/control.sock`.
  - The old format-9 store is kept beside it.
  - The public node `fn.fg-goose.online` (fsn1) runs the same image (RECORD, `current.md`).
  - INFERRED: neither live node holds anything Mini depends on, so re-genesis costs Mini nothing today.
- **FN-39 (READ, `ps` on hbox).** pid 3153612 is a separate `qual-bbf52159` image under `/tank/fn/gates/`, up 6 days. It is Mini's gitweb preview gate (swarm plan §5), and the swarm plan forbids cleanup under `/tank/fn/gates/`.

### 1.11 Engineering state and the 6.6.0 plan as the fn session understands it

- **FN-40 (RECORD, swarm plan §1–2; fn reply).**
  - `make check` was 48/91 red at `d4e53323c`.
  - The current source does not `ld` to native entry.
  - The last published image set is 1,064 commits behind.
  - "Current source has not yet run in an image — the first image set is hours away."
  - Both deployed nodes run 6.6.0 built from 09-28 source and were never cut.
- **FN-41 (RECORD, swarm plan wave 1).** The 85 deferred theorems are classified as two real failures and 83 collateral. Certify-first-then-compose is the route. Exit criterion: `deferred_defthms: {}`.
- **FN-42 (RECORD, swarm plan §2, §4, D49).** The wave plan: wave 0 ground truth; wave 1 one world plus a published image; wave 2 strands, live-defect bridges and a redeploy of both nodes.
  - Wave 3 is the "plump" design packets: tariff/resource vector, bounded reclaim, BP catch-up, owner carrier, host-into-ACL2, zmq surface.
  - Wave 4 is the tcb-shrink actors interleaved with the D41 stages: ST1 generators, then ST2 page-word boundary, ST3 paged catalog, ST4 dense runs, ST5 history rows, ST6 resource vector, ST7 linear hashing.
  - The cut comes when F1–F8 are MET and ember says so.
  - D49 adds the remote consumer and `specs/applications.md` to the bar.
  - INFERRED: the items Mini cares about most sit in waves 3–4, beyond the next image: reclaim, the resource vector, paged history that removes per-record heap, and the zmq/remote surface.

### 1.12 The fn session's reply, checked against the tree

| fn reply point | verdict | where |
|---|---|---|
| Three distinct acknowledgements (transport ACK, retention receipt, application outcome) | **READ, confirmed** | `docs/architecture.md` §Purpose; decision 2026-09-23 "first application experiment" |
| `uncertain` is real; resend the same exact bytes, never re-sign | **READ, confirmed** | STO-004; applications.md item 2 (ML-DSA randomized) |
| Per-node numbers; portable identity is digest/Message-ID; no cross-node order; conflicts kept | **READ, confirmed** | FN-03, REP-001/002 |
| Log/feed store, not mutable KV; checkpoints map to appends + cursor | **READ, confirmed** | FN-10, FN-19 |
| Mini owns the canonical payload codec, and fn treats it as opaque | **INFERRED, consistent with the tree with one caveat.** fn hashes and signs the *article* bytes. Mini's payload is opaque inside the article body, but the article grammar (headers, CRLF, line length, base64) is a shared codec both sides must agree on | FN-10 |
| The Lean–ACL2 contract is codec-level (shared byte vectors + named boundary functions) | design position; engaged in §4.2 | — |
| An ambiguous persistence failure stops the node for recovery | **READ, confirmed** | STO-033 ("fences the store"), P5 fail-stop |
| POST is barrier-bound, about 0.3 fsync/POST; not a hot KV | **RECORD, confirmed** | FN-36 |
| Re-genesis across format bumps until `fn-store-1` | **READ, confirmed** | FN-23 |
| D49 / D34 / D27 / D01 / D09 as stated | **READ, confirmed** (D49 on `integrator/d49`, not yet on dev) | FN-04, 23, 09, 07, 08 |
| "1 of 28 command families priced" | **unverified**: the 10-03 audit said 0 | FN-35 |
| Live reclaim funding open, offline reclaim works | RECORD; tree text inconsistent | FN-21 |

---

## 2. What Mini uses from fn TODAY

- **MI-01 (READ, `docs/DURABLE-STORE.md`; Host `Settings`).** **Mini's own durable Store is not fn.** It is SQLite (`forward-link.sqlite3`, schema v3) behind the Rust helper `minidregg-link-sqlite-store`. The helper's verbs are `durable-init`, `durable-read`, `durable-append ROOT HEIGHT RECORD TAG` and `durable-checkpoint`; it holds opaque bytes, and Lean owns all meaning.
  - Its tables are `durable_seed`, `durable_log(height, record, tag)` and `durable_checkpoint(height, bytes)`, of which the latest two are kept.
  - Each entry carries a KMAC256 tag over (keyId, h, chain_h), with `chain_h = H(chain_{h-1} ‖ H(record_h))`.
  - Checkpoints are MAC'd over (keyId, height, worldRoot, H(body)).
  - The open verifies chain, MACs and checkpoint root, then replays the suffix.
- **MI-02 (READ, same).** Mini's write path:
  - append at `head+1` under compare-and-swap on the head;
  - SQLite commit, then fsync, rename and directory-fsync of the anchor;
  - read back and confirm on exact equality.

  An error after commit is "an uncertain result, never permission to submit a different operation". The checkpoint cadence is `checkpointEvery` (default 64).
- **MI-03 (READ).** Mini's world root is a sparse Merkle root over cells (SHA-256, cached tree). fn has no counterpart (FN-25; I found no Merkle structure in fn's store, only in Roughtime anchors).
- **MI-04 (READ).** Mini detects whole-store rollback with an independently retained 80-byte head anchor (`MINIANC1`) outside the store directory. fn does not detect it (FN-16).
- **MI-05 (READ, Mini `Kernel.lean`, `Deployed.lean`, `Host/Main.lean:590-593`).** Mini already carries a substantial fn integration: 51 `Fn*` files and about 8.2k lines across Kernel, Host and Compiler, imported by `Kernel.lean` and `Deployed.lean`. The last touches were 10-02/03 audience-metadata and law-authority commits. Host config keys:
  - `fnGateway` (`GatewayPinSettings`: application, subject, target, capability, policyAddress), which pins *which* Mini receiver and grant an fn-originated report may drive;
  - `fnPoll` (origin config, fn pin, scope, policy, `controlPath`);
  - `fnReplyPoll` (adds R/Q pins and claims);
  - `fnReplyCatalog`.
- **MI-06 (READ, `Host/Main.lean` ~2420-2530, 2981-3270, 4071-5605).** **The integration mechanism is a subprocess of a hash-pinned fn binary on the same machine.**
  - Mini snapshots the operator's `fnBinary` (up to 64 MiB, mode 0500) and the ML-DSA public key.
  - It calls `fn --fn consumer poll|ack|position|status CONTROL …`, `consumer-project`, `consumer-inspect`, `consumer-article --json` and `hybrid-verify-source`.
  - Output is parsed with bounded reads and exact token/field checks: `["consumer","status","accepted",ack,frontier,distance]`, and the cursor field names `history, incarnation, consumer, principal, query, …`.
  - INFERRED, a seam finding: Mini's Lean Host re-parses fn's cursor fields and status line. That is a **second decoder of an fn-owned codec**. The fn decoder lives in `books/consumer-position.lisp`. Today they agree by test, not by construction (see §4.2).
- **MI-07 (READ, `docs/FN-CONSUMER-E1.md`, `FN-PORTABLE-E1.md`, `FN-E2-*.md`).** What the experiments established:
  - **E1:** a Mini consumer operation keyed by (consumer domain, semantics, application, operation) and an even/odd nonce rule.
    - A fresh operation installs binding + Q (reply), plus an inbox atom on the portable route.
    - A changed source writes conflict evidence and never a second effect.
    - Ack happens only after the Mini transaction is durably settled.
    - Proofs are about `decide`. The docs disclaim fn verdicts, collision resistance and physical durability.
  - **E2:** a live poll, then decide, then Mini operation, then ACK against an isolated fn developer image (`1d26e01f`, 09-24), not `/tank/fn/node`.
  - **B3 reply publication:** Mini constructs the RFC 5536 article for Q in Lean, with a Message-ID from a domain-separated digest of typed fields, a two-slot SQLite CAS outbox, and the publication persisted before post.
  - **A→B→A two-store:** "harness prepared; composed owner not yet run" (09-24).
- **MI-08 (READ, `docs/FN-PUBLICATION-DISCLOSURE.md`, `FN-SELECTIVE-ORIGIN-PROPOSAL.md`, `FN-RELEASE-DESIGN.md`).** Mini treats fn as a **"semi-untrusted transport of the exact signed release"**.
  - `FnEvidence.verify` re-admits the whole accepted origin prefix and does not trust fn's position or signature.
  - The R article base64-encodes the entire prefix package: 139,470 B of package becomes a 191,283 B article.
  - Selective disclosure and authorized release are proposals only.
- **MI-09 (READ fn source; RECORD Mini doc).** `docs/FN-UPSTREAM-REQUESTS.md` (09-26) status:

| request | ask | status at fn `origin/dev` |
|---|---|---|
| PKT-codex-001 | `two_store_join.py` per-side Mini identity/config | **Done in source**: `tools/runbooks/two_store_join.py:903,1258` cite it (READ) |
| PKT-codex-002 | qualified image with wider signed-composite/poll codec; fix stale 196,608/196,963 prose | Image found by Mini itself (`bbf52159`, 09-26). The stale numbers no longer appear in `specs/consumer-progress.md` (READ). Mini's "selected operator profile + end-to-end evidence" is still owed |
| PKT-codex-003 | `hybrid-author` control source ceiling (v1 = 65,535) refused Mini's 191,283 B source | **Done in source**: `books/native-hybrid-control.lisp:23-41` widens the field to the frame's u32 remainder and cites PKT-codex-003 (READ). Not on any deployed or qualified image (FN-40) |

---

## 3. What Mini's emerging program model needs from a persistent storage node

### 3.1 Needs, mapped

The needs come from the program-model reports: OS-lineage §1, §4, §6, §8; calls-concurrency Part III ideas 3, 5, 7, 8; root notes; `docs/BEND-PERSISTENT-COMPUTATION-20261003.txt`. Mini-side items are INFERRED from those reports. fn-side items cite FN-ids.

| # | Mini need | fn has (FN-ids) | fn lacks | could add / who |
|---|---|---|---|---|
| N1 | **Durable cells and their Merkle roots** (the sparse-Merkle world root, MI-03) | exact-byte durable records (FN-07, 12–15); BLAKE3 chain over the log (FN-15) | any authenticated map, root or inclusion/non-inclusion proof; any in-place cell update (FN-10) | **Keep roots in Mini.** fn stores *blocks and checkpoints* whose bytes commit to Mini roots. fn should not grow a Merkle map for Mini: that would be a twin of Mini's root |
| N2 | **The log of admitted turns** (today SQLite `durable_log`, MI-01) with append-at-head CAS | append; acknowledge only after the barrier; uncertain kept distinct (FN-12–14); idempotent same-bytes resend (FN-33 P4) | an **append-at-expected-head** precondition: fn allocates its own order; one owner (FN-37); 36 POST/s on ZFS (FN-36); 3.6 KB heap per record (F1); live node T=32,768 (FN-38/STO-038); forever-retention metadata (FN-20) | Short term: **batch** many Mini records per fn record (one per finalized block or checkpoint interval), keyed by a Message-ID derived from (domain, height, block hash). For fn to sit under the hot path it would need a "conditional append" control op or a per-stream sequence check, plus the D41 paged representation (ST3–ST5) |
| N3 | **Activity checkpoints** (Core4 machine state) and their **lifetimes**: short-lived by policy, pinned to the package, superseded at each resume (OS §1, §4; calls idea 3) | append; a cursor to find the latest; content reclamation **C** after an authorized release (FN-19); offline `store reclaim` (FN-21) | lifetimes other than "forever until an authorized release" (FN-20); live reclaim; H compaction; record metadata is forever even after C, so a superseded checkpoint still costs a record (anti-resurrection) | A **retention class** of "superseded-by-successor in stream S", releasable by the stream's next record. That is an authorized release whose authority is the stream writer. Needs D13 or an anti-resurrection rule for it; wave 3 row 2. **Ask fn.** Until then: checkpoints in fn only at the `checkpointEvery` cadence, as backup, not per yield |
| N4 | **Receipts and history for replay/audit** ("a replay kit: packages + receipts suffice for anyone to re-execute"; OS §4) | exactly fn's strength: immutable, signed, exact bytes, forever by default, replicated by set union (FN-20, 25); export/import proved (FN-24) | an index by Mini key (height, cell, activity); NNTP gives Message-ID, number and group | Mini derives Message-IDs deterministically (already done in B3, MI-07), so "fetch block h" is `ARTICLE <msgid(h)>`. No fn change needed |
| N5 | **Indexes / derived index cells** for queries over non-resident data (OS §4) | Message-ID index, catalog columns, OVER/HDR (FN-27) | general secondary indexes; HDR/NEWNEWS have a live owner-pinning defect (FN-27) | Keep Mini-semantic indexes as Mini cells. fn's Message-ID lookup suffices for content addressing |
| N6 | **Deal/escrow domains**: messages between domains bound to session + sequence; timeout heights (calls idea 7) | at-least-once delivery, cursor, idempotent resend, withdrawal events (FN-28); remote consumer on lane (FN-30); BP for disconnected peers | competing consumers; non-NNTP inter-node protocol; rebase; multi-group (FN-29); fn does not enforce sequence or session, and should not | fn as the **mailbox transport** between domains. Session/sequence/timeout and offer safety stay Mini laws in the deal cell. The zmq req/rep and pub/sub mapping (D49) is the natural surface |
| N7 | **Replication across failure domains** | set-union convergence over trusted peers (FN-25/26); BP across outages | replica-count/failure-domain policy; any ordering; any proof of retention by a peer (A-PEER is an assumption) | Order comes from Mini's Simplex mesh. fn spreads finalized, certified blocks as facts, which gives a catch-up/archive feed for followers. A "retention receipt" from a peer (D12) is the fn feature Mini would want for "k copies exist" |
| N8 | **Snapshot/restore** | `store export/import`, certified (FN-24) | restore keeps the history but **gets a new genesis/incarnation**, so every cursor is refused and there is no rebase (FN-24, 29); whole-store rollback undetected (FN-16) | Mini must treat an fn restore as "re-register consumers from Mini's own durable position". Mini keeps its head anchor (MI-04). Ask fn for rebase-by-mapping (consumer-progress already specifies the mapping obligation) |
| N9 | **Re-genesis** | cheap and expected; a foreign format is refused by name (FN-23) | stability before `fn-store-1` | Pin by (fn image digest, store history-id, format word). Mini already pins the binary hash (MI-06). Add the history-id to Mini's `fnGateway`/poll pin so a silently re-genesised fn is detected |
| N10 | **Metering of storage** (refundable deposits; charge the post-GC encoded delta; insolvency becomes AwaitsFunding, never deletion; OS §4, §6) | capacity vector, retention undertaking charge, `:unaffordable` refusal (P9 certified, FN-33); live limits (STO-038) | a priced tariff: `:unpriced` (FN-35); the live node runs without `[resources]` (FN-38); per-principal storage accounts | Mini meters its own cells in Mini law. fn needs only a per-account quota that **refuses by name** (exists), so Mini can map the refusal to `AwaitsFunding`. The tariff is wave 3 row 1 |
| N11 | **Exactly-once effects / outbox** (calls idea 3: outbound effects wait for commit; deterministic outbox ids) | idempotent same-bytes resend; uncertain; ack only after the consumer's own commit (FN-28, 33) | — | Already the E1/B3 pattern (MI-07). Codify it in the contract (§4.4) |
| N12 | **Parallel admission** (Block-STM; root = sequential fold; calls idea 5) | — (one serialized owner, FN-37) | — | Irrelevant to fn if fn stores *results* (blocks) rather than participating in admission. No ask |
| N13 | **Upgrade/migration records** (migration chain in the cell; dispositions) | append-only history of whatever Mini writes | — | No ask |

### 3.2 The quantitative wall (INFERRED from FN-36/37/38 and F1/F6)

- **Per-turn records are too many.** One fn record per Mini turn at a modest 10 turns/s is 864k records/day.
  - F1 puts retained heap at about 3.6 KB/record after reopen: roughly 3 GB/day of owner heap.
  - F6 puts the open at 16–22 s for 40k records.
  - The live node's transaction budget is 32,768. It is raisable live up to u32, but only within the heap reservation (STO-038).
  - That is the *current* representation. D41's stages (paged catalog ST3, dense runs ST4, history rows ST5) exist to remove per-record heap, and they are wave 4.
- **Per-block or per-checkpoint records fit.** At one fn record per finalized block (say every few seconds), or per checkpoint interval (64 turns by default), the same node holds weeks of history inside today's bars.
- **So the 6.6.0 recommendation is:** fn holds *batches*, Mini keeps its SQLite hot log, and the "fn replaces the SQLite helper" move waits on named fn deliverables: D41 ST3–ST5, conditional append, the superseded-checkpoint retention class, live reclaim and rebase.

---

## 4. Candidate shapes for the Lean–Lisp contract

### 4.1 Where the boundary sits

Three placements, in increasing intimacy (INFERRED):

- **B1. fn as archive + feed of finalized Mini history.** Recommended now.
  - Mini writes one signed article per finalized block. Its body is Mini canonical bytes: block, receipts, and optionally a sealed checkpoint at cadence.
  - The Message-ID is `H(domain, semantics, height, blockHash)`.
  - Followers, auditors and new mesh members consume by cursor or `ARTICLE <msgid>`. fn peering spreads the facts.
  - Lean decides what is valid. fn decides only "durably held, exact bytes, by this identity".
  - **No new fn semantics.** It uses what FN-12–15, 24, 25, 28 already give.
- **B2. fn as inter-domain transport.** Recommended now, and it already exists as E1/E2.
  - Deal/escrow messages, replies and publications travel as articles between per-domain Mini nodes.
  - fn's at-least-once delivery with Mini-owned dedup is exactly calls-idea-7's "bind every message to session and sequence".
  - Needs: the remote consumer (D49), and the zmq req/rep and pub/sub mapping.
- **B3. fn as the durable log under Mini's store helper.** This replaces `minidregg-link-sqlite-store durable-*`. Target it, gated.
  - It requires fn to provide conditional append at an expected stream head, per-record cost that does not grow the owner heap (D41), a superseded-checkpoint retention class, live reclaim, rebase-by-mapping, and a whole-store-rollback detector at least as strong as Mini's anchor (MI-04).
  - INFERRED: B3 should not be attempted before `fn-store-1` freezes. Each fn re-genesis would otherwise re-genesis Mini's primary store.

In all three, **Lean owns semantics and admission; fn owns durability, identity of bytes, and delivery.** Neither side's theorems are imported by the other.

### 4.2 Wire and codec: who owns which canonical bytes

There are three codecs at the seam. Each needs exactly one owner (INFERRED):

| codec | owner | the other side's role |
|---|---|---|
| Mini payload (block/receipt/checkpoint/deal message bytes) | **Mini (Lean)** | fn: opaque octets. fn hashes and signs the *article*, never interprets the payload |
| The article envelope (RFC 5536 headers, `fn-app` envelope, MIME, CRLF, base64 folding, Message-ID syntax) | **shared, the risky one**: Mini renders it in Lean (B3, `FnPortableSource`); fn parses it in ACL2 (`article-parser`, D01 projections) | must agree byte for byte, or the signature or projection differs |
| fn control and cursor frames (`FNCT`, `fncu` v1, status lines, `--json` outputs) | **fn (ACL2)** | Mini today re-parses them in Lean (MI-06): a second decoder |

Two ways to make two logics agree. Both need shared vectors; they differ in what the vectors mean.

- **(a) One codec per format, with differential tests on a shared corpus.** Cheap, and the status quo in spirit. But per the repo's own doctrine ("a differential test is a confession"; "Lean model + Rust differential ≠ verified") this is evidence, not verification. It also drifts silently when one side changes; Mini's 196,608 ceiling note (MI-09) is a past example.
- **(b) Generated from one source.** fn already writes frame grammars as data, for example `(:nat (:blob . 32) (:blob . 64) (:blob . 3309) :text)` in `books/native-hybrid-control.lisp`, and fn's frame-field records. The proposal:
  - Emit each such spec as a versioned data file.
  - Generate both decoders from it: ACL2 `def-*` on fn's side, a Lean decoder on Mini's.
  - Have **each side prove its own `decode ∘ encode = id` and `encode ∘ decode = id on accepted inputs` against the spec**, in its own logic.
  - Keep the shared vectors as a cross-check that the two *generators* read the spec the same way.

  This turns "theorem-to-theorem across logics", which the fn session rightly says is impossible, into two same-logic theorems about one artifact.
- **Recommendation.**
  - **(b) for fn's frames and cursor.** Mini should stop hand-parsing fn's status and cursor output. It should either treat the cursor as opaque bytes, asking fn's verified `consumer-inspect` for fields, or consume a decoder generated from fn's spec.
  - **Mini payloads stay opaque to fn.** fn never needs a Mini decoder.
  - **For the article envelope, minimise the shared surface.** Ask fn for an **opaque-body article profile**: fixed header set, `Content-Transfer-Encoding: binary` or a single canonical base64 rule, and no header projection inside the authored region. Then (b) applies to a five-field grammar instead of RFC 5536.
  - The named boundary functions would be fn's `fn-hsig-*` verify/encode and the projection function, and Mini's `FnPortableSource` decode and `FnReplyPublication` render, each proved against the shared spec.

### 4.3 Theorems each side owes the other (at its own coordinate)

**fn owes Mini** (FN-side, statements in fn's terms; status at `origin/dev`):

| obligation | fn theorem today | status |
|---|---|---|
| **Durable after ack.** An acknowledged article survives every crash point and every recovery cut | `fn-lgu-acknowledged-article-is-recoverable-at-every-crash-point` + `…-at-every-cut-of-recovery` (FN-31); P10 open program (FN-32) | uncertified at current digest; P10 has three coordinates outside it; power-loss rig not run (FN-18) |
| **Exact bytes.** What a poll, consumer-article or ARTICLE serves is the stored authored source; served = Xref line ++ stored | `fn-rcompat-served-payload-inserts-one-line` (FN-07); consumer-project keystones | certified status not checked by me; **the served read path routes through an unproved twin** (FN-35) — this must close before Mini relies on read-back exactness |
| **Idempotent identity.** The same poster bytes under a Message-ID give "already stored"; different bytes give a conflict | `fn-pb-same-article-is-answered-already-stored` (P4) | closure moved, uncertified |
| **Never a guessed refusal.** After a consumed completion: 240 or uncertain | `fn-own-240-follows-consumed-completion` (P2) | certified |
| **Prefix immutability / no reuse.** Acknowledged history is retained through mixed traces; numbers are never reassigned | `fn-snt-acknowledged-history-retained-through-mixed-trace` (`store-node-traces.lisp:734`); P3 pinned view | on the 85-deferral list; certified 10-03 per the scout (FN-41); P3 bridge pending |
| **Cursor.** At-least-once; ack monotone and idempotent; foreign store/incarnation/epoch refused before any mutation | CNS-001..009 keystones (`specs/consumer-progress.md`) | not individually checked by me |
| **Backup.** import ∘ export replays the same history; a crash mid-export is incomplete-or-complete | PRF-205, PRF-370 (FN-24) | certified |
| **Refusal at budget is by name**, never truncation | `fn-sbud-prepare-refuses-at-budget` (P9) | certified |
| **Fail-stop on an ambiguous barrier** | STO-033 + P5 | P5 certified; STO-033's batch layer "no host line calls it until …" (spec text) — **fn should state whether the served commit uses `owner-batch` today** |

**Mini owes fn** (Lean-side, as properties of Mini's own functions):

- **Deterministic identity.** Message-ID and bytes are functions of Mini-canonical fields only: no clock, no retry nonce, no fn-local number. B3 already does this (MI-07).
- **Resend, never re-sign.** On `uncertain`, Mini resends the stored signed artifact byte for byte. The signed artifact is persisted before the first send.
- **Ack after Mini commit.** A consumer ack is issued only after Mini's own durable transaction for that event (E1 does this). Ack is never used as Mini's commit.
- **Order-independence.** No Mini decision depends on fn's local number, arrival order or an acceptance stamp (FN-22 says stamps can regress). Ordering comes only from Mini's own heights and Simplex certificates.
- **Tolerate the unacknowledged-appears case.** An article Mini never saw acknowledged may appear after fn recovery (FN-14). Mini's dedup by operation id makes that harmless.
- **Decode only after identity check.** Mini decodes a payload only after checking its hash or signature against the Mini-side expectation. It never treats fn's verdict as authority (MI-08 already says so).

### 4.4 Failure semantics (the outcome algebra at the seam)

INFERRED from FN-12–15, 28, and the calls report's `Reply | Refused | Unknown | TimedOut | Broken | Upgraded`:

- **fn outcomes.**
  - `accepted` (240 / exit 0);
  - `already-stored` (duplicate, exit 0);
  - `conflict` (same Message-ID, different bytes);
  - `refused(reason)` by name: budget, policy, auth, saturation (`:mpx-saturated`);
  - `uncertain` (exit 3);
  - `node-stopped-for-recovery` (fenced, fail-stop).
- **Mini mapping.**
  - accepted and already-stored map to `Reply`.
  - conflict maps to `Refused(conflict)` and keeps both as evidence; that is the E1 rule.
  - refused maps to `Refused(reason)`, with the budget refusal becoming `AwaitsFunding`.
  - uncertain and node-stopped map to `Unknown`. Unknown is resolved only by authoritative lookup: `ARTICLE <msgid>`, consumer `position`, or the cursor delivering the event. It is never resolved by absence in a bounded feed, and never by a fresh identity (BEND-PERSISTENT-COMPUTATION item 4 already says this).
- **Torn writes** are fn's problem, by its crash model (FN-15). Mini sees only acknowledged-or-not.
- **Deliberately not covered:**
  - whole-store rollback (FN-16; Mini keeps its own anchor);
  - power loss on unqualified platforms (FN-18);
  - a malicious fn host (A-HOST).

  Mini should state these as assumptions it inherits.

### 4.5 Versioning and re-genesis

- **Pin the triple** (fn image digest, store `history-id`, format word) in Mini's fn configuration. The image digest is already pinned (MI-06); the other two are new.
  - A different history-id means fn re-genesised. Mini refuses its cursor and re-registers from its own durable position.
  - No Mini state may be lost when that happens, so until B3, fn is never the only copy of anything Mini needs. The fn reply says the same.
- **Re-genesis is independent on each side.** A Mini re-genesis starts a new Mini domain/semantics: new Message-ID namespace, new groups or streams. An fn re-genesis starts a new fn store history. Neither forces the other.
- **Before `fn-store-1`, plan for export/import on every fn bump.** Import gets a fresh genesis (FN-24), so Mini-visible fn identities change even though the article bytes and Message-IDs do not. INFERRED: this is why **Message-ID, not fn position, must be Mini's durable reference** to anything in fn.
- **The opaque-body article profile should carry its own version word.** A format change is then a refusal by name on both sides, never a reinterpretation (Mini CLAUDE.md doctrine).

### 4.6 Questions only Ember or the fn team can answer

1. **Placement (Ember).**
   - Is "fn as persistent storage node" B1+B2 (archive, feed, transport) for 6.6.0, with B3 (fn under Mini's hot log) as a 6.6.x target?
   - Or does Ember want B3 now, accepting that fn's current per-record heap and open-time bars put a hard cap on Mini's history volume?
2. **Retention for checkpoints (Ember + fn).**
   - Can fn get a "superseded-by-successor-in-stream" retention class, released by the stream writer's next record, before D13's general history compaction?
   - What anti-resurrection rule applies to a released checkpoint record?
3. **Conditional append (fn).** Is an "append iff stream S's head is H" control op acceptable in fn's model? It is a precondition on a Mini-owned stream key, not cross-node order. It is what B3 needs to replace Mini's CAS.
4. **Opaque-body profile (fn).** Will fn define a minimal article profile for application bytes, so the shared codec surface is a handful of fields rather than RFC 5536? Options: binary or one canonical base64 rule, fixed headers, a version word.
5. **Generated cross-language codecs (fn + Mini).** Will fn publish its frame and cursor grammars as data with a stable version, so Mini can generate its decoder rather than hand-parse (MI-06)?
6. **Rollback detection (fn).** Will fn adopt a head anchor or freshness anchor (D14/D22) for whole-store replacement, or should Mini keep that duty permanently?
7. **Durability keystone at current digest (fn).** What is the plan and date for certifying PRF-936 and closing P10's three outside coordinates? Does the served commit call `owner-batch` today (STO-033 says no host line did)?
8. **Read-path exactness (fn).** When will `fn-av-mca-read-span` be proved equal to `fn-mca-read-span` (PRF-1287)? Until then, read-back exactness is not a theorem.
9. **Remote consumer and rebase (fn).** Is rebase-by-mapping across compaction and restore in scope for 6.6.0, given that D49 puts the remote consumer in the cut?
10. **Peer retention receipts (Ember).** Does Mini need "k copies in distinct failure domains" as a checkable fact? That is D12/A-PEER work. Or does the Simplex committee's own replication suffice?
11. **Same-UID coupling (Ember).** Today Mini's Host must run as fn's owner UID on the same machine (mode-0600 control socket). Is that the intended deployment, or should Mini move to the remote consumer and TLS post, so Mini and fn can be separate failure domains and separate operators?

---

## Appendix — principal sources

- **fn** (`/Users/ember/dev/fn`, read via `git show origin/dev:`):
  - `README.md`, `docs/architecture.md`, `docs/proofs.md`;
  - `specs/storage.md` (§§ Authority, Commit protocol, Recovery, Checkpointing, History classes, One format), `specs/failures.md`, `specs/replication.md`, `specs/consumer-progress.md`;
  - `planning/current.md`, `planning/proofs.json`, `planning/release-v6.6.0.md`, `planning/experiments/e1-e2-agent-exchange.md`;
  - `books/byte-store-keystones.lisp`, `books/store-log-durable.lisp`, `books/store-genesis.lisp`, `books/native-hybrid-control.lisp`, `books/article.lisp`, `books/frame-octets.lisp`;
  - `integrator/d49:planning/decisions.md`, `origin/lane/apps:specs/applications.md`.
- **Notes:**
  - `~/dev/redregg/work/FN-SWARMPLAN-20261004.md`, `FABLE-FN-SESSION-20261003.md`, `FN-SESSION-REPLY-20261004.md`;
  - `SCHOLAR-OS-LINEAGE-20261004.md` Part I, `SCHOLAR-CALLS-CONCURRENCY-20261004.md` Part III, `SCHOLAR-BREAD-PROGRAM-MODEL-20261004.md` (grep), `ROOT-READING-NOTES-PROGRAM-MODEL-20261004.md`, `PROGRAM-MODEL-BRIEF-20261004.md`.
- **Mini** (`5df8bb07`):
  - `docs/FN-*.md` (all 11), `docs/DURABLE-STORE.md`, `docs/BEND-PERSISTENT-COMPUTATION-20261003.txt`;
  - `Host/Main.lean` (Settings, fn services, subprocess calls), `Kernel.lean`, `Deployed.lean`.
- **hbox** (read-only): `systemctl status/cat fn-node.service`, `ls /tank/fn`, `ls /tank/fn/node{,/store,/store/journal}`, `du -sh` of the store, `fn.toml` with secret-bearing lines filtered out, `ps -p 3153612`.
