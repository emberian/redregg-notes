# What Mini needs from fn 6.6.0, and the Lean–ACL2 contract (2026-10-04, revised 2026-10-05)

**From** the Mini root to the fn team (fn session and Ember).

**Owner of this file:** SCHOLAR-FN. One writer.

**Sources, in priority order:**
1. The fn root's response, `redregg/work/FN-660-RESPONSE-20261004.md`, read at fn `origin/dev` = `0312bde92`. It overrides 2 below where they conflict.
2. FN-CHECK, `work/FN-CHECK-20261004.md`, at `deb5a1167`.
3. The scholar draft, `work/SCHOLAR-FN-STORAGE-NODE-20261004.md`.

Mini's program model is `designs/MINI-PROGRAM-MODEL-20261004.md` (§I fn, §B activities, §G metering). Mini facts were read at `minidregg` `36fca3ac`.

**Ids.**
- `M` = must-have for 6.6.0, `S` = should, `L` = later (the hot-log gate, §4).
- `F` = an obligation fn owes Mini; `N` = one Mini owes fn.
- `QF` = a question fn can answer; `QE` = one for Ember.

**Sizes** are the fn root's lane-days (S ≤ 1, M 2–5, L 5–10).

**Revision of 2026-10-05.** fn's response corrected 14 claims in the first version. Each correction is now in the text where it applies, marked **[fn-resp]**. The three decisions fn put to Ember are in §7, each with Mini's view. The Mini-side commitments in §6 now carry their status. Items 2 and 3 are implemented in lane `scholar-fn`: commits `48cf51f0` and `ec53f8c2` on main `3b709c87`, queued in MERGE-QUEUE.md.

---

## 1. Summary

**What Mini uses fn for in 6.6.0.** fn is Mini's archive, feed and inter-domain transport of exact bytes, and nothing else:

- **Archive and feed.** Finalized blocks and their receipts, bundled (§3.3), as signed articles in a Mini-domain group. Followers and auditors read them by cursor, or by `ARTICLE <msgid>`.
- **Replay kits.** Package bytes plus receipts: enough for anyone to re-execute.
- **Published package bytes,** identified by package hash.
- **Inter-domain transport.** Cross-domain deal and saga messages and their replies, through the consumer cursor. Local today; remote once D49's remote consumer lands.

Signed articles are never reclaimable (`fn-rcl-signed-article-is-never-reclaimable`, PRF-088). That is the property permanent history needs, and it is why everything above goes to fn and nothing superseded does.
- **[fn-resp]** PRF-088 is *stated and uncertified at current digest*. Recertifying it is S5.

**Every Mini post goes through the control socket (`hybrid-author`), never NNTP POST.**
- **[fn-resp]** Over NNTP, `duplicate`, `conflict`, `refused` and `uncertain` all answer `441`. They are told apart by text alone.
- The control socket gives them distinct status words and exit classes.

**Asks for 6.6.0, in priority order:**

1. **M1. Durable-after-ack over the log kernel the node runs**: 4–7 lane-days, segment rotation as a named hypothesis (§7 D-M1).
2. **M3. Idempotent resend, certified** (PRF-117 + P4) on the control-socket path: 1–2 days.
3. **M4. Store identity by command:** genesis node identity, schema digest, format word, both image revisions. 3–5 days.
4. **M5. Exported grammars** for FNCT reply frames, the `fncu` cursor and the exit/reason words, with both round trips in ACL2. Mini decodes the frames directly; `--json` leaves the contract. 4–6 days.
5. **M6. One application article kind in ACL2:** a grammar of the *authored source*, with a version header. 3–5 days, after its decision row.
6. **M7. The remote consumer on dev and in the release image:** 2–4 days plus box time, via batch R.
7. **M8. A release image built from cut source, with F1–F8 *re-measured* on it.**

**Moved to 6.6.x** (§7 D-M2):
- **M2**, served bytes = stored bytes. Its real subject is PRF-1286, the captured ARTICLE path, L. Only the re-cites and the PRF-243 recertify stay in 6.6.0.
- Meanwhile Mini's authority on read-back is its self-certifying content identity plus its own record of acknowledged Message-IDs (§3.4).

**What Mini will not ask fn to be:**
- a mutable key-value store;
- an authenticated state map (Merkle root, inclusion proofs);
- an orderer or consensus;
- the store under every Mini turn in 6.6.0;
- the home of activity checkpoints or of any superseded record;
- an interpreter of Mini payloads;
- the enforcer of deal session, sequence or timeout;
- a low-latency path;
- the only copy of anything Mini needs, until the §4 gate passes.

For 6.6.0 Mini also does not ask for rebase, multi-group selection, competing consumers, the zmq-pattern surface, or D12 peer retention receipts.

---

## 2. The asks

### Must-have for 6.6.0

**M1. Durable-after-ack over the log kernel.**

- *What.* **[fn-resp]** The record-level state the host holds is the log kernel. Its ack count is `fn-lgk-acked` (`books/store-log-kernel.lisp:53`). Its relation R (`fn-lgk-relp`, `:163`) includes `ACKED ≤ len COMMITTED`. The host acks through `fnn-log-ack` → `fn-lgc-finish-one`.
  - Neither route in the first version works.
    - `owner-commit-pipeline` holds no records. It already proves the ordering half: PRF-272 and PRF-354 are certified.
    - A pipeline→`owner-batch` refinement is unnecessary.
  - The keystone (QF-1), over the host run from the open:
    - for any host operation sequence, every record in `take(fn-lgk-acked ks, fn-lgk-committed ks)` is in the committed records recovered from every admissible crash image of every cut of append, fence, failed fence and extend, and of the recover program;
    - every member that COMPLETE answers accepted is one of those records;
    - it is lifted to the concrete kernel by PRF-282.
  - Plan:
    - M1-a: restate `store-log-durable.lisp:821-891` over the kernel and drop the `owner-batch` include. S.
    - M1-b: R holds at every state of the host run. M, 1–2 days.
    - M1-c: link the reply to the records through `fn-oab-*`. M, 1–2 days.
    - M1-d: corollary through PRF-282, a registry row, both image closures. S.
    - M1-e: rotation keeps R. L, 3–5 days.
- *Why.* It is the only fact that makes fn's accepted answer a retention fact on that node. Mini's read-back can detect a wrong byte but not an omission (§3.4), so nothing on Mini's side substitutes for M1.
- *Check.*
  - The theorem appears in the default **and** dtn image closures' certify manifests, with a certified verdict at the cut digest.
  - A new `planning/current.md` capability row names it.
  - Segment rotation is either proved (M1-e) or enters the statement as a **named hypothesis**, not as a restriction to rotation-free runs (§7 D-M1).
- *Status.* **NOT.**
  - PRF-936 is `uncertified-at-current-digest`. It is a Makefile root only and is stated over `owner-batch`.
  - The kernel survival lemmas are already written (`store-log-durable.lisp:266,320,390,572,770`).
  - No M-ask is owned by any wave of FN-SWARMPLAN today. M1 needs a proof lane in wave 2, which depends on wave 1's recertification.

**M3. Idempotent resend, certified, on the path Mini posts through.**

- *What.* PRF-117 (`fn-sr-a-signed-retry-is-already-stored`, `books/source-routes.lisp:217`) is the host-called verdict over `fn-store-existing-action` for both post paths.
  - Recertify it at current bytes.
  - Make it the M3 keystone, and cite P4 (`fn-pb-same-article-is-answered-already-stored`) in a registry row.
- *Why.* Mini resolves `Unknown` by resending the same persisted signed bytes (§3.5).
- *Check.*
  - The registry row and its certify verdict.
  - A native test on `hybrid-author`: an identical resend is `:duplicate`, exit 0; changed bytes are `:conflict`, exit 1, and the second carrier is not stored.
- *Status.* **NOT certified.** PRF-117 is uncertified at digest. P4 is in no row and covers the NNTP POST reply only.
  - **[fn-resp]** The unproved glue is the `:duplicate` → reply path, host `:program` code at `hybrid-control.lisp:189`. Status → exit is proved: `fn-native-control-exit-is-fenced-iff-uncertain`.

**M4. Store identity by command.**

- *What.* One ACL2-rendered answer, with a version word, from an offline verb on `ROOT` (M4-a, M), a control request (M4-b, S) and an NNTP `XFN-STORE` row (M4-c, M). It prints:
  - format word;
  - genesis node identity;
  - schema digest and profile digest;
  - history-id and incarnation;
  - the **creating** image's revision (genesis);
  - the **running** image's revision.
- *Why.* Mini pins fn (§3.6). history-id survives export/import, so only the genesis node identity reveals an import re-genesis. The running revision is what Mini's binary pin (`fnBinary` hash) corresponds to.
- *Check.* Run it on a store and on its `store export | store import` copy:
  - format word and history-id are equal;
  - node identity differs;
  - the output decodes with the M5 grammar.
- *Status.* **NOT** for the genesis fields.
  - **[fn-resp]** history-id and incarnation are printed today by `fn consumer-inspect` (a host format string).
  - `fn-gen-decode` exists (`store-genesis.lisp:239`), and nothing reads it.

**M5. Exported grammars with fn-side round-trip theorems; Mini decodes frames directly.**

- *What.* A versioned JSON file written by an **ACL2-evaluated** emitter (a `make` target with `--check`). It covers:
  - every FNCT request and reply frame Mini exchanges, keyed by **family**. **[fn-resp]** FNCT kind 4 is both hybrid-enroll and consumer-request under one magic;
  - the `fncu` cursor;
  - the `fn-e` poll report bytes;
  - the exit-class table (`*fn-outcome-codes*`) and the status and reason words (`*fn-nctrl-statuses*`, the refusal reasons);
  - vectors produced by `enc_G`;
  - for each grammar, both `dec ∘ enc = id` and `enc ∘ dec = id` on accepted inputs.
    - FNCT spec-driven frames already have both directions generically (`books/frame-invariants.lisp:568,599`), so most are instantiations.
    - `fncu` has `dec ∘ enc` (`fn-cp-cursor-decode-encode-roundtrip`, `books/consumer-position.lisp:1050`) and needs `enc ∘ dec`.
- *Why.* Mini today hand-parses fn's CLI text lines and runs a `consumer-inspect` subprocess to read its own cursor (§6 item 1). fn has no ACL2 JSON parser, so `--json` would need one before `enc ∘ dec` could be stated. That is why `--json` and the CLI text lines leave the contract (§7 D-codec).
- *Check.*
  - the exporter target and its `--check`;
  - the file's version word;
  - the named theorems certified;
  - Mini's generated decoder accepts every vector and re-encodes it to identical bytes.
- *Cost to Mini.* Mini speaks the 0600 control socket instead of running the CLI. The remote FNCR framing (M7) must be in the same file; whether FNCR reuses FNCT is QF-12.
- *Status.* **NOT.** `protocol_emit.py` is a non-evaluating Python reader covering NNTP only. It has no committed file and no version key.

**M6. One application article kind in ACL2.**

- *What.* A grammar of the **authored source**, not of the served article.
  - **[fn-resp]** D01 signs the exact authored source. ARTICLE serves Xref, Path, Injection-Info and the FN-Authorship carrier lines before it.
  - The kind is:
    - a fixed RFC 5322 header set (ASCII VCHAR/WSP, From, Subject and Newsgroups required; Path, Xref and Injection-* refused);
    - a **version header**;
    - an author-supplied `Date` and `Message-ID`;
    - a body of canonical padded base64 in CRLF lines of 76 characters, with nothing else in the authored region.
  - One book holds the renderer, the recognizer, both round trips, and **a theorem that every article of the kind is accepted by `fn-article-parse` and the injection decision**.
  - The grammar is exported as in M5, and the file names the extraction `fn-hc-authored-source`.
- *Naming.* **[fn-resp]** "Profile" means the D27 store profile in fn, so this ask needs a fn decision row under another word. This document says "article kind".
- *Why.* Two kinds exist today and differ:
  - fn's e1/2 is a Python convention: five headers, then an `fn-app: e1/2` body line and `key: value` metadata.
  - Mini's E1 (`Kernel/FnPortableSource.lean`) has seven headers, including `Content-Type` and `Content-Transfer-Encoding: base64`.

  One kind replaces both, and e1/2 is re-expressed on it or deleted.
- *Facts that make the kind simple* **[fn-resp QF-7, QF-8]**:
  - injection performs no Date check;
  - with Date and Message-ID supplied, no Injection-Date is added, so the injected article does not depend on the clock;
  - no path refuses an article as too old; peers refuse only Date more than 24 h in the future;
  - article size A is a live store-profile field. A bare `init` writes 16 MiB; the development, scale and friend presets write 32,768.
- *Check.*
  - the grammar file and its version header;
  - the round-trip and acceptance theorems certified;
  - shared vectors pass Mini's generated renderer and decoder.
- *Status.* **NOT in ACL2.**

**M7. Remote consumer on dev and in the release image.**

- *What.* The D49 remote consumer:
  - a separate TLS listener, `[remote_consumer]`;
  - poll, wait, ack, position and status routed to the account's bound consumer;
  - register, rebase and unregister kept `:operator-control`.
- *Why.* Cross-domain transport between Mini domains on different machines. It also makes the Mini Host and fn separate failure domains (QE-5).
  - **[fn-resp]** A remote Mini cannot register its own consumer. Re-registration after a pin change is an fn-operator step (§3.6).
- *Check.*
  - `fn-crbd-*` keystones certified at the cut digest;
  - the narrow `native-config` recertify run;
  - five new remote scenario selectors pass on the release image;
  - D49 merged to dev.
- *Status.* Lane-only: `lane/apps@23d02fe96`, in the integrator's batch R. Laptop REPL admission only. No native has run. At dev the path is closed by construction.

**M8. A release image from cut source, F1–F8 re-measured.**

- *What.* M8-a: an image set from dev HEAD with the 12 core natives. M8-b: `cut_release --to 9` plus one fundamentals run on a frozen candidate. M8-e: both nodes redeployed on it.
- *Ask, precisely.* **Re-measured**, not MET. MET is fn's own cut bar.
  - A *qualified* image additionally needs the row-8 crash-campaign tool (M8-c, M, not yet built).
- *Check.* `planning/evidence-index.tsv` rows whose coordinate is the release image.
- *Status.* **NOT.**
  - No fundamentals row after 09-28 and no `qual-*` from current source.
  - The set-0312bde92 image is being built and is unpublished.

### Should (6.6.0 if it fits; Mini works around each)

- **S1. Import commits a new incarnation.**
  - **[fn-resp]** This is an fn defect against fn's own spec (`consumer-progress.md:541-542`): the old store and its import can be two writable futures under one incarnation.
  - Fix: import reuses clone's rollover fence. M, 2–3 days.
  - Placement: 6.6.0 if a lane frees up, else 6.6.x.
  - Mini's workaround is M4's node identity in its pin.
- **S2. A head-commitment query:** the record count and the `fn-frame-digest` of the last entry, and the digest at a given index. NOT. M, 6.6.x.
- **S3. Accounted mode on the nodes Mini uses.**
  - ARTICLE is priced and certified (1 of 25 families).
  - The `[resources]` opt-in is `lane/tariff2-optin`, in batch R.
  - Mini maps a budget refusal to `AwaitsFunding`.
- **S4. Archive-volume figures on the release image,** run with M8-b: open time and anonymous RSS after reopen at 10^5 and 10^6 records, and the largest T and H that fit `MemoryMax=2G`.
- **S5. Recertify PRF-088** (signed payloads never reclaimable). S.
  - **[fn-resp]** No retention setting, `Expires:` or per-group expiry removes a signed payload, as PRF-088 is stated.
  - A **cancel is a withdrawal, not a removal.** The bytes stay, ARTICLE answers `430 withdrawn`, and the cursor delivers an `FNWD` report. Mini's read-back keeps "withdrawn" distinct from "absent" (N11).
- **S6 (withdrawn).** "Conflicts visible to the consumer" has nothing to show.
  - **[fn-resp]** Every post path refuses the second carrier and does not store it. Mini's own persisted copy is the only second carrier.
  - Whether peer ingest keeps both is QF-13.

### Later: the hot-log gate (§4)

These are listed so fn can see where Mini is heading. None is a 6.6.0 ask.
- **L1.** Conditional append.
- **L2.** D41 ST3/4/5/7 served by default.
- **L3.** `fn-store-1` frozen.
- **L4.** A release path for superseded records, with live reclaim funded (S152).
- **L5.** Power-loss qualification.
- **L6.** The zmq surface.
- **L7.** D12 receipts.
- **L8.** M2's PRF-1286.
- **L9.** M1-e rotation, if it is a hypothesis in 6.6.0.

---

## 3. The contract

### 3.1 Boundary placement

- **Now:** fn is the archive, feed and transport. The scholar report calls this B1 + B2.
  - Mini's SQLite store (`minidregg-link-sqlite-store`, `durable_log` + `durable_checkpoint`, anchored by `MINIANC1`) stays the store under every turn and the home of every checkpoint.
- **Later:** fn under the hot log (B3), when §4 passes.
- **Division of labour.**
  - Lean owns semantics, admission, order and validity.
  - fn owns durability on its node, the identity of the bytes it holds, and delivery undertakings.
  - Neither side imports the other's theorems.
- **Output gate:** Mini posts only bytes whose turn has committed and, in a committee domain, is final (program-model decision D).
- **No checkpoint of any kind in fn** (scribe note SN-1, accepted by the root).
  - Hibernated object preimages and replay logs go to fn only if funded as permanent history (QE-6).

### 3.2 Codec ownership

| codec | owner | the other side |
|---|---|---|
| Mini payload (block bundle, receipt, package, deal/saga message) | **Mini**, in its Lean canonical encoding | opaque octets |
| Application article kind (M6): the **authored source's** headers, version header, base64 lines | **fn**: ACL2 renderer, recognizer and acceptance theorem, with an exported grammar | Mini *generates* its renderer and decoder |
| FNCT frames, `fncu`, `fn-e` report bytes, exit and reason words (M5) | **fn**: ACL2 | Mini *generates* its decoder from the export and never hand-parses. Text lines and `--json` are outside the contract |

**The contract statement.** For each fn-owned grammar `G` at version `v`, each side proves both round trips in its own logic, about the same exported artifact:
- fn proves them for `enc_G` and `dec_G`.
- Mini proves them for `enc'_G` and `dec'_G`, generated from the same file.

fn emits vectors from `enc_G`. Mini's CI checks that `dec'_G` accepts every vector and `enc'_G` re-encodes it to identical bytes. The vectors check that the two *generators* agree; the two same-logic theorems are the verification.

An unknown version word is refused by name on both sides.

**Mini-side codecs already shared at one owner.** Mini's base64, used in E1 bodies, selected-release articles and the enrollment memo, is now one module, `Kernel/Base64.lean` (§6 item 3). It is total, with both round trips proved. M6's generated codec replaces the article-level parts; the byte codec stays.

### 3.3 Identity

- **Portable identity is Mini's own digest of Mini's canonical bytes.**
  - The Message-ID is rendered from it (`Selection.messageId`: cSHAKE256 under `DREGG.FN.REPLY-MSGID/v3`).
  - A package's identity is its package hash.
  - fn's BLAKE3 digest is never Mini's reference.
- **Mini never stores as a reference** an fn article number, Xref, journal position, acceptance stamp or arrival order. Cursor positions are per-pin bookkeeping.
- **Signatures are randomized.**
  - Mini persists the signed article before its first send, and resends those bytes and only those.
  - A re-sign under the same Message-ID is a conflict.
- **Conflicts.** **[fn-resp]** fn refuses the second carrier on every post path (`books/nntp-post.lisp:606-607`; `fn-native-control-conflict-is-a-refusal`). It keeps one.
  - Mini's evidence is its own persisted carrier plus fn's refusal.
  - Under a Mini-authored identity, a conflict is a Mini defect (a re-sign or key misuse) and is raised to the operator.
  - Under a foreign identity, the receiving law decides.
- **Archive bundling.** One archive article carries the finalized blocks of heights `[h, h+K)` with their receipts. Its identity is Mini's digest of the bundle bytes.

**Sizing K (replaces scribe note SN-2).** **[fn-resp]**
- **T is not fixed at 32,768.** That is the 16 MiB friend rung: a capacity-free `init` takes the largest rung that fits, H ∈ {64, 32, 16} MiB, with **T = H/512**. A bare `init` defaults T to 2^32−1.
- **T, H and A are operator store-profile fields**, raised by `policy set` (STO-038):
  - applied live if the heap figure fits the reservation;
  - otherwise recorded and effective at next start, with no data moved;
  - refused by name if the machine cannot hold the value.
- **H binds alongside T.** The admission gate is committed record octets + prospective ≤ H.
- **Each consumer ack is one transaction plus up to 364 octets of H.** Register, rebase and unregister cost one each. Reclaim and compaction never free transactions.
- **A store's archive lifetime** at block interval `b`, with the setup records `s` (fnce bootstrap, register) subtracted, is about

      min( (T − s) / (1 + acks per article),  H / (article octets + ack octets) ) × K × b

  So bundling K blocks per article multiplies the transaction-bound lifetime by K, cuts per-record heap and open time (both about linear in records), and **does not save H**.
- **K must also respect:**
  - A, the article bound;
  - the proposed poll page budget of 262,144 returned octets;
  - the `:oversize` rule: an event a poll reply cannot carry is refused by name, with no skip contract. A bundle larger than a poll page can never be delivered by cursor.
- **The operator therefore sizes H and T together, and Mini chooses K so that one bundle ≤ min(A, page budget).** S4 supplies the 2G ceiling. No block interval exists in Mini source yet, so `b` is a parameter.

### 3.4 Obligations

**fn owes Mini** (statuses per fn's response at `0312bde92`):

| id | obligation | theorem or check | status |
|---|---|---|---|
| F1 | An acknowledged record survives every crash point and every recovery cut of the host run | M1 kernel keystone (QF-1 shape) | NOT; 4–7 d; rotation per §7 D-M1 |
| F2 | Served bytes = Xref, Path, Injection-Info, carrier lines ++ stored authored source | PRF-1286 (captured ARTICLE path); PRF-1287-OWED (fallback); `fn-rcompat-…` is conditional and pre-dot-stuffing | **6.6.x**. 6.6.0 keeps the re-cites and the PRF-243 recertify |
| F3 | Identical bytes under a Message-ID → `:duplicate`, exit 0 on the control socket; different bytes → `:conflict`, exit 1, second carrier **not stored** | PRF-117 + P4 (M3) | uncertified; 1–2 d |
| F4 | After a consumed completion: accepted or uncertain, never a guessed refusal | P2, PRF-015 | certified |
| F5 | An ambiguous barrier stops the node (exit 3); recovery holds a prefix | compose `fn-owb-recovered-kernel-after-a-failed-fence` (no `owb` hypotheses), `fn-ocs-failed-barrier-stops-telling-no-member` and `fn-lgk-crash-of-related-state-is-a-prefix` | S, 0.5–1 d, fits 6.6.0. **The prefix half carries A-CRYPTO-TRAILER** |
| F6 | Cursor: at-least-once delivery; ack monotone and idempotent; a foreign store, incarnation or epoch refused before any ack; ≤ 346 octets | `fn-cp-cursor-decode-encode-roundtrip` (`:1050`), `fn-cp-cursor-encode-length-bound` | book passed at dev bytes; keystones not individually checked |
| F7 | Signed payloads are never reclaimed | PRF-088 | uncertified; S5 |
| F8 | Export/import replays the same history; a crash mid-export leaves an incomplete or a complete archive | PRF-205, PRF-370 | certified |
| F9 | A budget refusal is by name, never truncation | P9 | certified at closure |
| F10 | Each grammar Mini reads round-trips, at a version word | M5/M6 | NOT |
| F11 | Store identity is observable | M4 | NOT for genesis fields |
| F12 | A writable restore changes the incarnation | S1 | NOT for import; an fn spec defect |
| F13 | `usage` (exit 5) means no Store or socket effect | one-line keystone | by construction today; S if Mini relies on it |

**Mini owes fn** (properties of Mini's own functions):

| id | obligation | check | status at `36fca3ac` + lane `scholar-fn` |
|---|---|---|---|
| N1 | Message-ID and payload bytes are functions of Mini-canonical persisted fields only | a named Lean theorem over the Message-ID function | shape in `Kernel/FnReplyPublication.lean`; theorem owed |
| N2 | Signed article persisted before first send; on `Unknown`, resent byte for byte, never re-signed | a Lean theorem that the resend path reads only the persisted article | B3 pattern exists; theorem owed |
| N3 | A consumer ack follows Mini's own durable commit; an ack is never Mini's commit | `Kernel/FnConsumerOperation.lean` | exists |
| N4 | Dedup by operation id, including an article that appears after fn recovery unacknowledged | E1 operation keying | exists |
| N5 | A payload is decoded only after its identity checks; fn's verdict is never authority | `FnEvidence.verify` | exists |
| N6 | Only committed, and in a committee domain final, bytes are posted | the output gate (decision D) | owed for the archive publisher |
| N7 | fn output decoded only by M5-generated decoders of FNCT, `fncu` and `fn-e`, never CLI text or `--json` | §6 item 1 | owed: hand parsers today |
| N8 | fn's seven exit classes kept distinct; the refusal reason kept; an unknown code read as may-have-acted | `Host/FnOutcome.lean` | **implemented in lane `scholar-fn`** (§6 item 2) |
| N9 | fn is never the only copy until §4 passes | SQLite authoritative | holds |
| N10 | Every Mini post uses the control socket (`hybrid-author`), never NNTP POST | the archive publisher and B3 | B3 replies already post through `hybrid-author`; the grain-origin R route (`docs/FN-UPSTREAM-REQUESTS.md`, 09-26) used authenticated NNTP POST and must move; owed for the archive publisher |
| N11 | Read-back extracts the authored source and keeps `withdrawn` distinct from `absent` | `hybrid-verify-source` already returns the authored source; withdrawn handling owed | PARTLY |

**Authority on read-back.** Until F1 is certified (and F2 in 6.6.x), Mini judges what it reads back from fn by two checks:
- **Exactness.** Mini recomputes its content digest from the extracted authored source and compares it with the Message-ID.
- **Omission and rollback.** Mini keeps its own record of the Message-IDs fn acknowledged, under `MINIANC1`. An acknowledged identity fn later cannot serve is evidence against fn.

`MINIANC1` anchors Mini's SQLite store, not fn's head; S2 would let Mini bind fn's head (SN-4).

### 3.5 Failure semantics

**[fn-resp]** fn has seven exit classes (`books/outcome-class.lisp:26-28`). There is **no exit 2**.

| fn answer | Mini outcome | Mini action |
|---|---|---|
| 0 `accepted` (control `:accepted` or `:duplicate`) | `Reply` | record the transport acknowledgement |
| 1 `refused(word)` with `conflict` | `Refused(conflict)` | keep Mini's own carrier as evidence; fn stored nothing |
| 1 `refused(word)` with `busy`, `clock-unusable`, or no owner reached (`no-owner`) | `Refused(word)`, **transient** | retry the same bytes; exit 1 is not terminal |
| 1 `refused(word)`, any other word | `Refused(word)` (a budget word → `AwaitsFunding`) | keep the word |
| 1 on a resend after `Unknown` | stays `Unknown` | the original may have landed (a revoked enrolment refuses the resend of an accepted article) |
| 3 `fenced` / uncertain | `Unknown` | resolve as below |
| 4 `fault` | `Unknown` | **[fn-resp QF-3]** a fault *can* follow a durable commit (`fn-fs-classify`). Mapping it to `Refused` would be unsound |
| 5 `usage` | `Refused(usage)` | nothing was done (by construction; F13); a Mini defect, raised to the operator |
| 6 `interrupted` (BP) | `Unknown` | — |
| 7 `not-connected` (BP) | `Refused`, transient | nothing left the node |
| `health` 19 or 20–29 | the node is not serving | wait; being stopped for recovery is a normal state |

- A lost connection reaches a control client as **1** (before submission) or **3** (after). `hybrid-author` marks after-submission right after connect, so it errs toward 3.
- An accepted ack whose output file then fails to write is reported **3**. `position` settles it.

**Resolving `Unknown`.** Mini uses only these:
- `ARTICLE <msgid>` returning an authored source whose identity checks (`430 withdrawn` is a distinct answer, not absence);
- `consumer position`;
- the cursor delivering the event;
- an idempotent resend of the same persisted bytes answered exit 0.

Never absence from a bounded page; never a new identity.

**Deadlines.** A Mini await that reaches its height deadline resolves the *activity* as `TimedOut`; the fn post stays `Unknown`. A late landing is harmless, because identity is content-derived and a deal cell rejects a message after its timeout height.

**Three acknowledgements, kept apart:**
1. fn's transport acknowledgement;
2. a retention receipt: on one node F1 + F7; across peers D12, which is open;
3. the receiving Mini domain's admission.

Mini commits only on its own admission.

### 3.6 Versioning and re-genesis

**Pin.** Mini's fn pin is:
- the fn running-image digest (pinned today by the `fnBinary` snapshot);
- format word;
- genesis node identity;
- schema digest;
- history-id;
- incarnation.

All but the first come from M4. Mini records the creating-image revision but does not pin it.

| fn event | what changes | Mini action |
|---|---|---|
| Fresh re-genesis (format bump, D34) | node identity, history-id, perhaps format word and schema digest | refuse the old pin; the **fn operator** re-registers the consumer (remote cannot, M7); Mini re-publishes the archive from its own copy |
| `store export` / `store import` | node identity (new genesis). history-id, incarnation and cursors **carry over** **[fn-resp]** | refuse the old pin, because of the node identity; the operator re-pins deliberately. Cursors still decode, which is why the node identity, not the cursor, is the check |
| `checkpoint clone` | incarnation | refuse the cursor; re-register |
| fn image upgrade | running-image digest | the operator re-pins deliberately |
| Whole-store rollback to an older copy | nothing fn reports | detected only by Mini's acknowledged-ID record, or later by S2 |

Further rules:
- Before `fn-store-1` freezes, no fn store is the only copy of anything Mini needs. Dev's `00a3713c4` schema change means the next deploy *will* re-genesis.
  - **[fn-resp]** The genesis word at dev is still `fn-store-10`; the rename is not done.
- Re-genesis is independent on each side.
- Version words refuse by name on mismatch.

### 3.7 Trusted primitives

Cited as assumptions on both sides, never as theorems.

**fn:**
- A-SIG-NATIVE (PQClean ML-DSA-65 verify; libsodium Ed25519 for the anchor signature);
- A-TLS-NATIVE, A-SBCL-RUNTIME, A-DURABILITY, A-HOST;
- A-CRYPTO (BLAKE3 resistance; the function itself is guard-verified ACL2) and A-CRYPTO-NATIVE;
- **A-CRYPTO-TRAILER**, carried by F5's prefix half;
- the read-path set: A-DURABLE-EXTENT, A-DURABLE-LZ, A-ARENA-STORED, A-HOST-EXCLUSIVE-READ, A-CARRIED-PAIR, A-OWNER-INVARIANT-CARRIED, A-PGS-HOST-IO;
- A-IDENTITY, A-EXTRACT, A-TARGET-COMPILER;
- the temporary native dispatch trust exceptions;
- **in 6.6.0, the rotation hypothesis of M1** (§7 D-M1).

**Mini:** collision resistance of cSHAKE256 and SHA-256; Mini's signature primitives; SQLite plus fsync/rename semantics; the OS; the Lean compiler and runtime.

**Inherited and uncovered:** power loss on unqualified filesystems; a malicious fn host; whole-store rollback of fn outside Mini's §3.4 check.

---

## 4. The gate for fn under Mini's hot log

fn replaces `minidregg-link-sqlite-store durable-*` only when every criterion holds on a released, deployed fn image.

| id | criterion | measured or proved by |
|---|---|---|
| G1 | F1 with **rotation proved** (M1-e, not a hypothesis) and F2 (PRF-1286) certified in the image closure | M1, L8 |
| G2 | `fn-store-1` frozen, and a later fn release opens a `fn-store-1` store without re-genesis | release notes + an open on the later image |
| G3 | D41 ST3, ST4, ST5 and ST7 served by the default image; host references > 0 | image manifest |
| G4 | Open time and anonymous RSS after reopen at 10^7 records each within 2× the 10^5 figure | fundamentals harness |
| G5 | On hbox `tank`, sustained acknowledged-append rate ≥ Mini's SQLite rate, and p99 append-to-ack ≤ Mini's SQLite p99, at an fsync before every ack | Mini publishes its baseline (§6 item 8); fn runs the same workload |
| G6 | Conditional append: refused before any write when the expected stream head ≠ current; an accepted one carries F1 | ACL2 theorem (L1; QE-3) |
| G7 | Superseded records releasable (unsigned `:absent` records under a writer-authorized release, or a deliberate change to PRF-088; QE-2); live reclaim funded (S152's A/B/C decided and closed, PRF-1315 certified) | theorems + a measured reclaim pass at 10^6 records |
| G8 | Power-loss qualification of the deployment filesystem profile | the rig's run on the release image |
| G9 | S2 head commitment served, so Mini's anchor binds fn's head | command + Mini anchor check |

---

## 5. Questions

### Answered by fn's response (kept for the record)

| id | answer |
|---|---|
| QF-1 | M1's subject is the log kernel; the keystone shape is in M1 |
| QF-2 | PRF-1287 is the wrong row for ARTICLE; the captured path is PRF-1286, and it is 6.6.x |
| QF-3 | Exit 4 can follow a durable commit, so `fault → Unknown` |
| QF-4 | Control: `conflict`, exit 1. NNTP: 441 + text. Peers: 437/439. The second carrier is not stored |
| QF-5 | P4 covers NNTP POST only; PRF-117 covers both paths |
| QF-6 | Yes: the export covers `fncu`; the data language is JSON written by an ACL2-evaluated emitter |
| QF-7 | The version word is a header. No Date check; nothing refuses old Dates; peers refuse > 24 h future |
| QF-8 | A is a live field: a bare init writes 16 MiB, the presets 32,768. Carrier v1 limits the source to 65,535; v2 lifts it |
| QF-9 | One transaction per article; one per ack, plus ≤ 364 octets of H; the 2G ceiling is S4 |
| QF-10 | S1 is M (2–3 d): 6.6.0 if a lane frees up, else 6.6.x |
| QF-11 | PRF-088 is uncertified; no retention setting removes a signed payload as stated |

### Open, for fn

- **QF-12.** Does FNCR (remote) reuse FNCT framing? M5's file must cover whichever it is.
- **QF-13.** Does peer ingest (IHAVE/TAKETHIS, BP) keep a second carrier under one Message-ID (REP-002), or refuse it as the post paths do?
- **QF-14.** Will M5's export include the `fn-e` poll report bytes and the `FNWD` withdrawal report, so Mini's read of a delivered event is generated too?

### Needs Ember

- **The three decisions in §7.**
- **QE-1.** Is fn under the hot log a 6.6.x target? Does D41 move from AGREED DIRECTION to DECIDED?
- **QE-2.** Under the hot log, do superseded records go unsigned (`:absent`), or does fn grow a writer-authorized release that reopens PRF-088?
- **QE-3.** Conditional append needs a "stream key" and a home for its head: new fn vocabulary.
- **QE-4.** Does fn grow an external rollback anchor (D14/D22), or does Mini keep that duty permanently?
- **QE-5.** Deployment shape: Mini Host and fn as the same UID on one machine (direct FNCT on the 0600 socket), or separate failure domains over the remote consumer?
  - Coupled to D-codec: direct FNCT decoding locally, plus FNCR remotely, are two framings in one grammar file.
- **QE-6.** Who pays for fn's archive storage, which is permanent by theorem?
- **QE-7.** Confirm that 6.6.0 needs no D12 receipts, because each committee member publishes to its own fn node.
- **fn-side items awaiting Ember** (from fn's list): S152's A/B/C; F7's reading; D49's merge to dev.

---

## 6. What Mini commits to on its side

All paths are in `minidregg`.

1. **Delete the hand parsers of fn output.** OWED; it waits on M5.
   - The parsers: `parseFnConsumerStatus` and `parseFnConsumerInspect` in `Host/Main.lean`, and their callers `queryFnConsumerStatus`, `inspectFnConsumerCursor`, `queryFnConsumerPosition`, `classifyFnEmptyPoll` and `projectFnPoll`.
   - Replace them with generated FNCT, `fncu` and `fn-e` decoders over the 0600 socket, which retires the `consumer-inspect` subprocess.
   - This is the QUEST in `REVIEW-SCHOLAR-FN-20261005.md`.
2. **Keep fn's seven exit classes distinct and the refusal reason.** **IMPLEMENTED in lane `scholar-fn`.**
   - New `Host/FnOutcome.lean`: `classify` with fn's code table, `mayHaveActed` (an unknown code fails closed), `answerLine` (`consumer STATUS[ DETAIL]`), and `ackStatus`.
   - Theorems:
     - `classify_code`;
     - `classify_two` (exit 2 is no class);
     - `mayHaveActed_false_iff`;
     - `ackStatus_refused_iff`, `ackStatus_uncertain_iff` and `ackStatus_durableAccepted_iff`.
   - Fixed in `Host/Main.lean`:
     - `invokeFnConsumerPoll`, `invokeFnConsumerPollRaw`, `queryFnConsumerStatus` and `queryFnConsumerPosition` now name the class and reason. They drain a bounded stderr prefix instead of `.null`, through one helper, `runFnLocal`.
     - **Eight ack sites read fn's refusal as exit 2**, which fn never emits. Every real refusal (exit 1) was reported `transport-fault`, and the covered-by-frontier recovery behind `refused` never ran. They now use `ackStatus`.
3. **One base64.** **IMPLEMENTED in lane `scholar-fn`.**
   - New `Kernel/Base64.lean` holds the padded codec (`encode`/`decode`, total) with `decode_encode` (every byte string round-trips) and `encode_decode` (canonicity: only canonical encodings decode). It also holds the whole-group codec moved out of `Kernel/PayEnrolMemo.lean`, with its theorems, plus `encode_eq_b64Encode`, `encode_append`, `chunks_flatten` and `encodeLines`.
   - Deleted:
     - `FnPortableSource.decodeGroups` (a `partial def`);
     - the duplicated `base64Line`/`base64Lines` loops in `Kernel/FnSelectiveReleaseArticle.lean`, `Host/GrainOriginSource.lean` and `scripts/fn-e1e2/render-grain-origin-r.lean`.
   - The article-level parsers still hand-split headers; M6 replaces that layer.
4. **Pin the full tuple (§3.6).** OWED; small once M4 exists.
   - Extend `FnPollScopePin` and `Kernel/FnConsumerProgress.lean` `Scope` with format word, node identity and schema digest.
   - A changed tuple refuses.
5. **Name N1 and N2** in `Kernel/FnReplyPublication.lean` and `Kernel/FnOriginOutbox.lean`. OWED, small, Mini-only. QUEST.
6. **Keep SQLite and `MINIANC1` authoritative;** add the acknowledged-Message-ID record under that anchor. OWED.
7. **Build the archive publisher**, through `hybrid-author` only (N10), bundling to §3.3's K, post-finality (N6). OWED.
8. **Publish Mini's hot-log baseline for G5.** OWED.
9. **Treat fn cursor positions as per-pin bookkeeping only.** Holds.
10. **Read-back extracts the authored source and keeps `430 withdrawn` / `FNWD` distinct from absent (N11).** OWED.

---

## 7. The three decisions for Ember, with Mini's view

| decision | fn's recommendation | Mini's view (SCHOLAR-FN, owner of this file) |
|---|---|---|
| **D-M2.** Served bytes = stored bytes. Real subject PRF-1286, L, 5–10 d | 6.6.x; 6.6.0 keeps the re-cites and the PRF-243 recertify | **Agree.** Mini's content identity is self-certifying, so a served-byte error is *detected* whatever fn proves. 6.6.0 Mini authority: identity check on the extracted authored source, plus the acknowledged-ID record |
| **D-M1.** Durable-after-ack over the log kernel, 4–7 d; segment rotation in or out | name rotation out of scope for 6.6.0 (+3–5 d to prove) | **Agree to defer the proof, not to shrink the statement.** Rotation is not rare: every state checkpoint rotates the log, including the owner's automatic one (STO-034). A theorem stated over rotation-free host runs covers only the history since the last checkpoint. M1-b's induction over the host run must go *through* `:rotate` with "rotate keeps R" as a **named hypothesis**, listed in §3.7 and discharged by M1-e in 6.6.x. Separately, the release states the shipped T and H, so Mini can size K (§3.3) |
| **D-codec.** M5/M6 boundary | Mini decodes FNCT and `fncu` directly from fn's exported grammar (4–6 d); M6 gets a decision row | **Agree.** Direct decoding, `--json` out of the contract, M6 named an "article kind" (not D27's store "profile"). Include the `fn-e` report and `FNWD` bytes (QF-14) and key frames by family (the FNCT kind-4 collision). This couples to QE-5: same-UID direct FNCT now, FNCR remote later, both in one grammar file |

If Ember agrees with all three, fn's added work is about four lanes in waves 2–3: M1 kernel durability, M4 identity, M5 grammar export, and the M6 decision plus implementation. M3 and M7 are in flight, and M8 comes at the cut.

## Addendum 2026-10-05 (from the GPT-6 review of fn 6.6.0 decisions, work/FN-GPT6-REVIEW-20261004.md §5)
- **M1, client-level wording.** fn's durability contract as Mini relies on it is {acceptances the client observed} ⊆ {records recovered}.
  A record may be recovered whose acceptance the client never observed; that is a legitimate `Unknown` outcome, resolved by lookup
  of the same Message-ID, never by assuming absence.
- **M2 deferral is acceptable only as a checked composition, via a Mini adapter contract** (Mini-side obligations, built in FN-DIRECT):
  1. Mini exposes application bytes only after verifying them against its independently held expected identity
     (the content digest / Message-ID Mini recorded at post time).
  2. A missing or invalid object never silently counts as consumed: the cursor does not advance past it, and it is a named refusal.
  3. Every acknowledged identity stays available for reconciliation (the acknowledged-Message-ID record under Mini's anchor).
  Content identity alone does not detect omission, enumeration incompleteness or cursor errors; (2) and (3) are what cover those.
- **M5, grammar semantics.** The language description is the shared normative semantics. fn's ACL2 round-trip theorems do not
  make Mini's Lean interpreter correct; Mini's own theorems plus the CI decode/re-encode run over fn's vectors (including failure
  and consumption vectors) are Mini's evidence until a correspondence argument exists.
