# What Mini needs from fn 6.6.0, and the Lean–ACL2 contract (2026-10-04)

From the Mini root to the fn team (fn session and Ember). Status of every fn fact is the fn team's own
verdict in `redregg/work/FN-CHECK-20261004.md` at fn `origin/dev` = `deb5a1167`, which overrides the
scholar draft where they conflict. Mini's program model is `designs/MINI-PROGRAM-MODEL-20261004.md`
(§I fn, §B activities, §G metering). fn dev has since moved (`0312bde92`, read 10-04 04:53); statuses
here are not re-checked at that coordinate. Mini facts were read at `minidregg` `cbd849c4`.

Ids: `M` = must-have for 6.6.0, `S` = should, `L` = later (the hot-log gate, §4). `F` = an obligation
fn owes Mini, `N` = one Mini owes fn. `QF` = a question fn can answer, `QE` = one for Ember.
**Scribe notes** mark where the evidence pushes against a root position or another document; the
positions themselves are unchanged.

---

## 1. Summary

**What Mini uses fn for in 6.6.0.** fn is Mini's archive, feed and inter-domain transport of exact
bytes, and nothing else:

- **Archive and feed:** finalized blocks and their receipts, bundled (§3.3), as signed articles in a
  Mini-domain group. Followers and auditors read them by cursor or `ARTICLE <msgid>`.
- **Replay kits:** package bytes plus receipts, enough for anyone to re-execute.
- **Published package bytes,** identified by package hash.
- **Inter-domain transport:** cross-domain deal and saga messages and their replies, through the
  consumer cursor (local today, remote once D49's remote consumer lands).

Signed articles are never reclaimable (`fn-rcl-signed-article-is-never-reclaimable`). That is the
right property for permanent history, and it is why everything above, and nothing superseded, goes
to fn.

**Top asks, in priority order (all must-have for 6.6.0):**

1. **M1. A durable-after-ack theorem about the commit the node runs.** PRF-936 is stated over
   `owner-batch`, which the served `owner-commit-pipeline` never calls, and it is outside the image
   closure.
2. **M2. Served bytes = stored bytes.** PRF-1287 is planned, and the P1/P3 bridge is pending.
3. **M3. Idempotent same-bytes resend, certified** (P4) on the paths Mini posts through.
4. **M4. Store identity by command:** genesis node identity, schema digest, format word, history-id,
   incarnation, image revision. No command prints the genesis fields today.
5. **M5. Exported grammars** for the cursor, the control frames and `--json` outputs Mini reads, and
   the exit words. Each carries a version word and an ACL2 round-trip theorem, so Mini generates its
   decoder instead of hand-parsing.
6. **M6. One opaque-body article profile in ACL2**, with a version word and an exported grammar.
7. **M7. The remote consumer on dev and in the release image** (D49 already puts it in the cut).
8. **M8. A release image built from cut source, with F1–F8 re-measured on it.** Nothing has been
   measured since 09-28.

**What Mini will not ask fn to be:**

- a mutable key-value store;
- an authenticated state map (Merkle root, inclusion proofs): Mini's world root stays in Mini;
- an orderer or consensus: order comes from Mini heights and Simplex certificates;
- the store under every Mini turn in 6.6.0;
- the home of activity checkpoints or any superseded record;
- an interpreter of Mini payloads or a judge of Mini validity;
- the enforcer of deal session, sequence or timeout: those are Mini laws in the deal cell;
- a low-latency path;
- the only copy of anything Mini needs, until the §4 gate passes.

For 6.6.0 Mini also does not ask for rebase, multi-group selection, competing consumers, the
zmq-pattern surface or D12 peer retention receipts. pub/sub = group + cursor and req/rep = article +
correlated reply are enough.

---

## 2. The asks

Status is FN-CHECK's. "NOT" means nothing in specs, books or host.

### Must-have for 6.6.0

**M1. Durable-after-ack about the served commit.**
- *What:* an ACL2 theorem stating that an article the running node acknowledged survives every crash
  point of the append, barrier and extend programs, and every cut of recovery. Two routes give it:
  - restate the theorem over `owner-commit-pipeline`;
  - or prove a refinement from the pipeline to `fn-owb-*`.

  Also tie the pipeline's STOP to recover-to-prefix (today `fn-owb-uncertain-batch-recovers-to-a-prefix`
  is over `owner-batch`).
- *Why:* it is the only fact that makes fn's accepted reply a retention fact on that node. Without it,
  fn is a transport and Mini must keep its own copy of everything it publishes forever. The §4 gate is
  impossible without it.
- *Check:*
  - the theorem name (PRF-936's successor) appears in the default image closure's certify manifest with
    a certified verdict at the cut digest;
  - `green_check --strict` on that closure covers it;
  - P10's three outside coordinates (`log-truncated`, `recovery-stage-unlinked`,
    `fnn-log-complete-rotation`) are either inside it or named as assumptions.
- *Status:* **NOT.**
  - PRF-936 is `uncertified-at-current-digest`, and 107 of 193 closure files have changed since its
    last pass.
  - It is outside the 1134/1084 closures.
  - It is stated over a layer the host does not call.

**M2. Served bytes = stored bytes.**
- *What:* PRF-1287 proved and certified:
  - the selective-chain refinement to `fn-proto-archive-command-available-reference`;
  - guards verified;
  - rows re-cited.

  Also the P1/P3 caller bridge, and the captured-result path of `fn-asto-mca-read-span` inside the
  proved chain or removed.
- *Why:* Mini reads back archive articles, replay kits and inbound messages. Until this holds, Mini's
  content-derived identity is the only exactness check (§3.4, F2).
- *Check:* PRF-1287 certified at the cut digest. `fn-rcompat-served-payload-inserts-one-line` is in a
  registry row and certified.
- *Status:* **PARTLY.**
  - The generated chain is `:logic`, and its four funding keystones are certified, but it is
    refinement-unproved.
  - `fn-rcompat-…` passed at dev bytes; its PRF-243 row reads uncertified.
  - PRF-1287 is planned, PRF-1287-OWED is open, and the bridge is pending.

**M3. Idempotent resend, certified.**
- *What:* `fn-pb-same-article-is-answered-already-stored` (P4), or its successor, in a registry row and
  certified at its current closure. It must cover every path Mini posts through: the control-socket
  `hybrid-author` and authenticated NNTP POST.
- *Why:* Mini resolves `uncertain` by resending the same bytes (§3.5). That is safe only if a duplicate
  is answered "already stored" and never makes a second copy.
- *Check:* the registry row and the certify verdict. A native test covers both paths: exit 0 on an
  identical resend, the conflict reason on different bytes.
- *Status:* **NOT certified.** P4 is uncertified at closure and in no registry row (it passed at its
  own bytes 10-01).

**M4. Store identity by command.**
- *What:* one command, offline on `ROOT` and online over the control socket, rendered in ACL2 with a
  version word. It prints:
  - format word;
  - genesis node identity;
  - schema digest and profile digest;
  - history-id and incarnation;
  - image revision.

  Over NNTP, the same in an `XFN-STORE`-class verb, so a remote consumer can check it.
- *Why:* Mini pins fn (§3.7). history-id survives export/import, so only the genesis node identity
  and schema digest reveal an import re-genesis.
- *Check:* run the command on a store and on its `store export | store import` copy:
  - format word and history-id are equal;
  - node identity differs;
  - the output parses with the M5 grammar.
- *Status:* **NOT.** "Nothing else reads a genesis field", no command prints it, and store identity on
  the wire is "not implemented" (`decisions.md:1144`).

**M5. Exported grammars and fn-side round-trip theorems.**
- *What:* a versioned data file, generated from the ACL2 definitions and checked for drift by a `make`
  target, for:
  - the `fncu` cursor bytes;
  - the requests and replies of every command Mini runs (consumer bootstrap / register / poll / wait /
    ack / position / status, `consumer-project`, `consumer-article`, `hybrid-author`,
    `hybrid-verify-source`), FNCT frames included;
  - every `--json` output Mini reads, with a version key added;
  - the exit-word table (0 accepted, 1 refused, 3 uncertain, 4 fault, 5 usage) and the refusal-reason
    words.

  For each grammar: ACL2 theorems `decode ∘ encode = id`, and `encode ∘ decode = id` on accepted
  inputs; plus a vector file emitted by the ACL2 encoder.
- *Why:* Mini today re-parses fn's host-format status line and `consumer-inspect` text in Lean (§6).
  That is a second decoder of an fn-owned codec, which fn's own architecture rules out ("cannot infer
  processing from printed output").
- *Check:*
  - the exporter target;
  - the file's version word;
  - the named theorems certified;
  - Mini's generated decoder accepts every vector and re-encodes it to identical bytes.
- *Status:* **NOT.**
  - The frame grammars are ACL2 data (`books/frame-fields.lisp`, `*fn-nhctrl-*-spec*`), and an emitter
    pattern exists (`protocol_emit.py`, `event_emit.py`).
  - None covers `fncu`, FNCT or `fnce`.
  - `fncu` is hand-coded in `consumer-position.lisp`.
  - `--json` is ACL2-rendered (`fn-ncr-json-line`) with no version key.
  - The text status line is a host format string.

**M6. One opaque-body article profile in ACL2.**
- *What:* an ACL2 renderer and parser for one application profile:
  - a fixed RFC 5322 header set, ASCII VCHAR/WSP, `Newsgroups` required;
  - a version word;
  - an author-supplied `Date`;
  - a body of canonical base64 in CRLF lines of a fixed width, with nothing else in the authored
    region.

  Its grammar is exported as in M5, with round-trip theorems.
- *Why:*
  - The signature covers the whole article, so the shared codec is RFC 5322 header syntax plus CRLF,
    and both sides must agree byte for byte.
  - Binary bodies are ruled out: a bare CR or LF is `:invalid-header`.
  - Two profiles exist today and differ:
    - fn's e1/2 (a Python convention): five headers, then an `fn-app: e1/2` body line and `key: value`
      metadata;
    - Mini's E1 in `Kernel/FnPortableSource.lean`: seven headers including `Content-Type` and
      `Content-Transfer-Encoding: base64`.

  One profile replaces both.
- *Check:*
  - the profile's grammar file and its version word;
  - the ACL2 parser accepts exactly what the renderer emits (round-trip theorems certified);
  - shared vectors pass Mini's generated renderer and decoder.
- *Status:* **NOT in ACL2.** e1/2 exists as an application convention.

**M7. Remote consumer on dev and in the release image.**
- *What:* the D49 remote consumer:
  - served over TLS as the account's bound consumer;
  - operator controls private;
  - in the release image;
  - native evidence run.
- *Why:* cross-domain transport between Mini domains on different machines. It also lets the Mini
  Host and fn be separate failure domains and operators (QE-5).
- *Check:*
  - `fn-crbd-route-is-the-accounts-bound-operation`, `fn-crbd-operator-controls-stay-private` and
    `fn-crbd-another-login-is-refused` are certified at the cut digest;
  - the five consumer scenarios of `specs/applications.md` pass over the remote transport on the
    release image.
- *Status:* **lane-only.** It exists on `lane/apps`. At dev the path is closed by construction
  (`(:unavailable :remote-operation-entry-installer)`).

**M8. A release image, qualified and measured.**
- *What:* an image built from the cut source, running the consumer scenarios, with the F1–F8 harness
  re-run on it and recorded in `planning/evidence-index.tsv`.
- *Why:* every fn fact Mini relies on is today "specified, with source and an earlier native
  coordinate". No image from current source has run.
- *Check:* evidence-index rows whose coordinate is the release image. Both live nodes run it.
- *Status:* **NOT.**
  - The image build at `deb5a1167` stopped in its interfaces preflight.
  - Nothing has been qualified since `qual-69046a76`.
  - Nothing has been measured since 09-28.

### Should (6.6.0 if it fits; Mini works around each)

- **S1. Import commits a new incarnation.** `consumer-progress.md:541-542` requires a writable
  restore to commit a new-incarnation transition before consumer service; only `checkpoint clone`
  does. *Workaround:* M4's node identity in Mini's pin. *Check:* a cursor from the source store is
  refused by its import. *Status:* NOT.
- **S2. A head-commitment query.** Report the record count and the `fn-frame-digest` of the last
  entry, and the frame digest at a given record index. *Why:* Mini's anchor could then bind fn's head
  as it binds its own (§3.4, F9). *Status:* NOT. The Roughtime `anchor.fnan` sits inside the store
  root and is not checked at the served open.
- **S3. Accounted mode on the nodes Mini uses.**
  - What: `[resources]` set, and budget refusal by name (P9, certified) reachable on the article path.
  - Why: Mini maps that refusal to `AwaitsFunding`.
  - Status: ARTICLE is priced in accounted mode at dev; 1 of 25 families is priced. Deployed: 0, and
    the live nodes run unaccounted.
- **S4. Archive-volume figures on the release image:**
  - open time and anonymous RSS after reopen at 10^5 and 10^6 records;
  - the largest `--max-transactions` that fits `MemoryMax=2G`.

  Why: Scribe note SN-2.
- **S5. A statement that no retention setting removes a signed payload.** This covers
  `retention set released-by-all-holders | release-after DAYS`, RET-008 per-group expiry and
  `Expires:`. Then archive permanence is the theorem, not an operator setting. The certification
  status of `fn-rcl-signed-article-is-never-reclaimable` should be stated as well.
- **S6. Conflicts visible to the consumer.** When two carriers share a Message-ID, the consumer can
  read both, or a conflict event naming both.

### Later: the hot-log gate (§4)

These are listed so fn can see where Mini is heading. None of them is a 6.6.0 ask.

- **L1.** Conditional append at an expected stream head.
- **L2.** D41 ST3, ST4, ST5 and ST7 served in the default image.
- **L3.** `fn-store-1` frozen.
- **L4.** A release path for superseded records, with live reclaim funded (S152).
- **L5.** Power-loss qualification on the deployment filesystem.
- **L6.** The zmq-pattern surface.
- **L7.** D12 peer retention receipts.

---

## 3. The contract

### 3.1 Boundary placement

- **Now:** fn is the archive, feed and transport (placements B1 + B2 in the scholar report).
  - Mini's SQLite store (`minidregg-link-sqlite-store`, `durable_log` + `durable_checkpoint`, anchored
    by `MINIANC1`) stays the store under every turn and the home of every checkpoint.
- **Later:** fn under the hot log (B3), when §4 passes.
- **Division of labour:**
  - Lean owns semantics, admission, order and validity.
  - fn owns durability on its node, the identity of bytes it holds, and delivery undertakings.
  - Neither side imports the other's theorems.
- **Output gate:** Mini publishes to fn only bytes whose turn has committed and, in a committee
  domain, is final (program-model decision D).

> **Scribe note SN-1.** `ROOT-PROGRAM-MODEL-DECISIONS-20261004.md` §I and `MINI-PROGRAM-MODEL-20261004.md`
> §I both list "checkpoints at cadence" among fn's contents. Root position 1 excludes in-flight activity checkpoints, and FN-CHECK shows why
> any checkpoint is wrong there: a signed article is never reclaimable, so every superseded checkpoint
> would be kept forever. This document puts **no checkpoint of any kind** in fn for 6.6.0.
> - A sealed state snapshot at a finalized height, if a replay kit ever needs one, is permanent
>   history and is priced as such.
> - Both §I texts should drop "checkpoints at cadence".
> - The same reasoning keeps hibernated object preimages (program model §G) and REPLAY interaction
>   logs (its scribe note C2) out of fn unless they are funded as permanent history (QE-6).

### 3.2 Codec ownership and the generated decoder

| codec | owner | the other side |
|---|---|---|
| Mini payload (block bundle, receipt, package, deal/saga message) | **Mini.** Lean canonical encoding | Opaque octets. fn stores, hashes and signs the article containing them and never interprets them |
| Article profile (M6): headers, CRLF, base64 lines, version word | **fn.** ACL2 renderer and parser, exported grammar | Mini *generates* its renderer and decoder from the exported grammar |
| fn control frames, `fncu` cursor, `--json` outputs, exit and reason words (M5) | **fn.** ACL2 | Mini *generates* its decoder from the exported grammar and never hand-parses |

**The contract statement.** For each fn-owned grammar `G` at version `v`, both sides prove the round
trip in their own logic, about the same exported artifact:

| | fn (ACL2) | Mini (Lean) |
|---|---|---|
| functions | `enc_G`, `dec_G` | `enc'_G`, `dec'_G`, generated from the same file |
| `dec ∘ enc = id` | yes | yes |
| `enc ∘ dec = id` on accepted inputs | yes | yes |

- **Vectors.** fn emits a vector file from `enc_G`. Mini's CI checks, for every vector, that `dec'_G`
  accepts it and `enc'_G` re-encodes it to identical bytes.
  - The vectors test that the two *generators* read the grammar the same way.
  - They are not the verification. The two same-logic theorems are.
- **Boundary functions.**
  - **fn side:** the encoder of each output Mini reads (the `fncu` encoder in `consumer-position.lisp`,
    `fn-ncr-json-line`, the M6 parser), each named in the grammar file.
  - **Mini side:** one generated module per grammar, named in §6.
- **Unknown version word:** refused by name on both sides, never reinterpreted.

> **Scribe note SN-3.** FN-CHECK (e) recommends that Mini "consume `--json` now". Root position 5
> requires a generated decoder.
> - Writing a hand decoder for `--json` would add a third hand-written decoder of an fn-owned codec,
>   and it would be deleted when M5 lands.
> - The scribe's recommendation is to rank M5 must-have, as above, and replace the two existing
>   text parsers directly with the generated decoder.
> - The cost is that the host-format status line, the weakest of the current inputs, stays in use
>   until M5 lands.

### 3.3 Identity

- **Portable identity is Mini's own digest of Mini's canonical bytes.**
  - The Message-ID is rendered from it, as `Selection.messageId` already does: cSHAKE256 under
    `DREGG.FN.REPLY-MSGID/v3`, over typed fields and the frozen creation context.
  - A package's identity is its package hash.
  - fn's BLAKE3 digest is fn's own and never Mini's reference.
- **Mini never stores as a reference** an fn article number, Xref, journal position, acceptance stamp
  or arrival order, and no Mini decision depends on cross-node order.
  - Cursor positions are bookkeeping for one pinned fn store (§3.7). They are discarded when that pin
    changes.
- **Signatures are randomized, so article bytes are not a function of the payload.**
  - Mini persists the signed article before its first send, and resends those bytes and only those.
  - A re-sign under the same Message-ID is a conflict, by design.
- **Conflicting evidence is Mini's to judge.** fn keeps both carriers (REP-002). Mini judges them:
  - Under a Mini-authored identity, a conflict means a Mini re-sign defect or key misuse. Mini records
    the evidence and raises it to the operator.
  - Under a foreign identity, the receiving law decides.
- **Archive bundling.** One archive article carries the finalized blocks of heights `[h, h+K)` with
  their receipts. Its identity is Mini's digest of the bundle bytes, which commit to the first and
  last block hashes. `K` is a Mini operator parameter sized by SN-2.

> **Scribe note SN-2.** The scholar's §3.2 estimate ("one fn record per finalized block … holds weeks
> of history inside today's bars") does not survive the arithmetic.
> - Both live nodes run T = 32,768, and a store admits one transaction fewer. At one article per block
>   and a block interval of `b` seconds, that lasts `32,767·b` s: 18 h at `b = 2`, 45 h at `b = 5`.
>   ASSUMED: one article is one transaction, and each consumer ack is one more (QF-9).
> - The F6 open at 40k records is 16–22 s, with a 1.2–1.7 GiB peak on a node capped at
>   `MemoryMax=2G`.
> - I found no block interval in Mini source, so `b` is a parameter, not a fact.
>
> Consequences:
> - Mini bundles blocks into archive articles, and the operator sizes T (D27: T is a profile field).
> - At month scale, the archive role also depends on the D41 representation. Hence S4.
>
> - `MINI-PROGRAM-MODEL-20261004.md` §I's mechanism ("one signed article per finalized block",
>   Message-ID `H(domain, semantics, height, blockHash)`) inherits the scholar's estimate. The bundle
>   identity above is the same construction over a height range, and it is content-derived because
>   block hashes commit to block bytes.
>
> This refines root position 1 and does not change it.

### 3.4 Obligations

**fn owes Mini** (statements in fn's terms; status per FN-CHECK):

| id | obligation | theorem or check | status |
|---|---|---|---|
| F1 | An acknowledged article survives every crash point and every recovery cut, **on the served commit path** | PRF-936 successor over `owner-commit-pipeline` (M1) | NOT: over `owner-batch`, uncertified, outside the closure |
| F2 | Served bytes = Xref line ++ stored authored bytes | `fn-rcompat-served-payload-inserts-one-line` + PRF-1287 + P1/P3 bridge (M2) | PARTLY: funding-proved, refinement-unproved |
| F3 | Identical bytes under a Message-ID → "already stored" (exit 0); different bytes → conflict, both kept | P4 `fn-pb-same-article-is-answered-already-stored` (M3) | uncertified at closure, in no registry row |
| F4 | After a consumed completion: accepted or uncertain, never a guessed refusal | P2, PRF-015 `fn-own-240-follows-consumed-completion` | certified |
| F5 | An ambiguous barrier stops the node (exit 3); recovery holds a prefix | P5 certified; the STOP-to-prefix link is still over `owner-batch` (M1) | PARTLY |
| F6 | Cursor: at-least-once delivery; ack monotone and idempotent; a foreign store, incarnation or epoch is refused before any ack; the cursor is at most 346 octets | `books/consumer-position`, `fn-cp-cursor-encode-length-bound` | PARTLY: the book passed at dev bytes; keystones not individually checked |
| F7 | Signed payloads are never reclaimed | `fn-rcl-signed-article-is-never-reclaimable` (S5) | cited by FN-CHECK; certification not stated |
| F8 | Export/import replays the same history; a crash mid-export leaves an incomplete archive or a complete one | PRF-205, PRF-370 | certified |
| F9 | A budget refusal is by name, never truncation | P9 `fn-sbud-prepare-refuses-at-budget` | certified at closure |
| F10 | Each grammar Mini reads round-trips, at a version word | M5/M6 theorems | NOT |
| F11 | Store identity is observable | M4 command | NOT |
| F12 | A writable restore changes the incarnation | S1 | NOT for import |

**Mini owes fn** (properties of Mini's own functions, proved or checked in Lean):

| id | obligation | check | status at `cbd849c4` |
|---|---|---|---|
| N1 | Message-ID and payload bytes are functions of Mini-canonical persisted fields only: no clock read at send, no retry nonce, no fn-local number | a named Lean theorem over the Message-ID function, e.g. that equal `identityPreimage` gives an equal Message-ID, plus no `IO` in its definition | the shape is in `Kernel/FnReplyPublication.lean`; theorem not named |
| N2 | The signed article is persisted before the first send; on uncertain, Mini resends it byte for byte and never re-signs | `Kernel/FnOriginOutbox.lean` two-slot CAS outbox; a Lean theorem that the resend path reads only the persisted article | B3 pattern exists; theorem owed |
| N3 | A consumer ack follows Mini's own durable commit of that event; an ack is never Mini's commit | `Kernel/FnConsumerOperation.lean` (E1) | exists |
| N4 | Duplicates and late arrivals are harmless: dedup by operation id, including an article that appears after fn recovery without an acknowledgement | E1 operation keying | exists |
| N5 | A payload is decoded only after its identity (digest, signature) checks against Mini's expectation; fn's verdict is never authority | `Kernel/FnEvidence.lean` `verify` re-admits the prefix | exists |
| N6 | Only committed, and in a committee domain final, bytes are posted | the output gate (decision D) | owed for the archive publisher |
| N7 | Mini decodes fn output only with M5-generated decoders | §6 | owed: hand parsers today |
| N8 | Exit words are handled distinctly; refusal reasons are kept | §3.5, §6 | **violated today** (§6) |
| N9 | fn is never the only copy until §4 passes | the SQLite store remains authoritative | holds |

**Authority on read-back (root position 2).** Until F1 and F2 are certified, Mini judges what it reads
back from fn by two checks:
- **Exactness.** The content-derived identity is self-certifying: Mini recomputes its digest from the
  served payload and compares it with the Message-ID.
- **Omission or rollback.** Mini's own record of the Message-IDs fn acknowledged. An acknowledged
  identity that fn later cannot serve is evidence against fn, not a Mini loss.

> **Scribe note SN-4.** "Mini keeps its own head anchor" needs a precise reading.
> - `MINIANC1` (`native/hyperdocument-link-sqlite-store/src/anchor.rs`) anchors Mini's SQLite store,
>   not fn. Mini has no anchor over fn's head today.
> - Until S2 exists, the authority for fn read-back is the pair above (self-certifying identity +
>   Mini's acknowledged-ID record), which Mini holds under its own anchor.
> - S2 would let Mini bind fn's head directly.

### 3.5 Failure semantics

| fn answer | Mini outcome | Mini action |
|---|---|---|
| exit 0 `accepted`, or "already stored" | `Reply` | Record the transport acknowledgement |
| exit 1 `refused(reason)` on a first send | `Refused(reason)`; a budget refusal becomes `AwaitsFunding` | Keep the reason word |
| exit 1 with conflict (same Message-ID, other bytes) | `Refused(conflict)` | Keep both carriers as evidence (§3.3) |
| exit 1 on a resend after `Unknown` | stays `Unknown` | The original may have landed: `applications.md` item 2 (a revoked enrolment refuses the resend of an accepted article) |
| exit 3 `uncertain` | `Unknown` | Resolve as below |
| exit 4 `fault`, a lost connection, the node stopped for recovery, or a `health` refusal (exit 19–27) | `Unknown` | Wait; then resolve as below. Being stopped for recovery is a normal state, not data loss |
| exit 5 `usage` | `Refused(usage)` | Nothing was done. Raise a Mini defect to the operator |

**Resolving `Unknown`.** Mini uses only these:
- `ARTICLE <msgid>` returning bytes whose identity checks;
- `consumer position`;
- the cursor delivering the event;
- an idempotent resend of the same persisted bytes answered with exit 0.

Mini never resolves `Unknown` by absence from a bounded page, and never by sending under a new identity.

**Deadlines.** A Mini await reaching its height deadline resolves the *activity* as `TimedOut`. The
fn post stays `Unknown` until resolved. A late landing is harmless, because identity is content-derived
and a deal cell's law rejects a message after its timeout height.

**Three acknowledgements, kept apart:**
1. **fn's transport acknowledgement:** this node answered accepted.
2. **A retention receipt:** evidence that a holder has undertaken to keep the bytes.
   - On one node: the committed record under F1 and F7.
   - Across peers: D12, which is open.
3. **The application outcome:** the receiving Mini domain's own admission.

Mini commits only on its own admission. An fn acceptance is never a Mini commit, and a Mini ack to fn
is never a Mini commit either.

> **Scribe note SN-5.** Root position 4 maps three fn outcomes. fn's exit table has five words.
> - This document maps `fault` to `Unknown` and `usage` to `Refused`. That extends the position; it
>   does not change it.
> - The `fault` mapping is conservative until fn answers QF-3: can exit 4 follow a durable commit?

### 3.6 Versioning and re-genesis

> **Scribe note SN-6.** Root position 6 and program model §I pin (image digest, history-id, format
> word). FN-CHECK (N9) shows that history-id survives export/import, so that triple cannot detect an
> import re-genesis. Root position 6 already requires fn to expose genesis node identity and schema
> digest, so the pin below adds them. Program model §I should be updated to match.

**Pin.** Mini's fn pin is the tuple:
- fn image digest (already pinned: `fnBinary` snapshot, mode 0500, 64 MiB bound);
- format word;
- genesis node identity;
- schema digest;
- history-id;
- incarnation.

All but the image digest come from M4.

| fn event | what changes | Mini action |
|---|---|---|
| Fresh re-genesis (format bump, D34) | node identity, history-id, maybe the format word and schema digest | Refuse the old pin; re-register; re-publish the archive from Mini's own copy |
| `store export` / `store import` | node identity (new genesis); history-id kept; incarnation kept today (S1) | Refuse the old pin; the operator re-pins deliberately |
| `checkpoint clone` | incarnation | Refuse the cursor; re-register |
| fn image upgrade | image digest | The operator re-pins deliberately |
| Whole-store rollback to an older copy | nothing fn reports | Detected only by Mini's acknowledged-ID record (§3.4), or later by S2 |

Further rules:
- **Before `fn-store-1` freezes, no fn store is the only copy of anything Mini needs.** The dev
  schema change `00a3713c4` means the next deploy *will* re-genesis.
- **Re-genesis is independent on each side.**
  - A Mini re-genesis opens a new Mini domain/semantics, with a new Message-ID namespace and new
    groups.
  - An fn re-genesis opens a new fn store history.
  - Neither forces the other.
- **Version words** (the M5 grammars, the M6 profile, Mini's payload codecs) refuse by name on a
  mismatch.

### 3.7 Trusted primitives

These are cited as assumptions on both sides, never as theorems:
- **fn:**
  - A-SIG-NATIVE: PQClean ML-DSA-65 verify. libsodium Ed25519 is named for the anchor signature.
  - A-TLS-NATIVE.
  - A-SBCL-RUNTIME.
  - A-DURABILITY.
  - A-HOST.
  - A-CRYPTO: BLAKE3 collision and preimage resistance. The function itself is guard-verified ACL2.
  - A-CRYPTO-NATIVE.
  - The read-path assumptions FN-CHECK added: A-DURABLE-EXTENT, A-DURABLE-LZ, A-ARENA-STORED,
    A-HOST-EXCLUSIVE-READ, A-CARRIED-PAIR, A-OWNER-INVARIANT-CARRIED, A-PGS-HOST-IO, A-IDENTITY,
    A-EXTRACT, A-TARGET-COMPILER.
  - The temporary native dispatch trust exceptions.
- **Mini:**
  - collision resistance of cSHAKE256 and SHA-256;
  - Mini's signature primitives;
  - SQLite plus fsync/rename semantics;
  - the OS;
  - the Lean compiler and runtime.
- **Inherited and uncovered:**
  - power loss on unqualified filesystems (D14; the release row 14 rig was not run);
  - a malicious fn host;
  - whole-store rollback of fn, outside Mini's §3.4 check.

---

## 4. The gate for fn under Mini's hot log

fn replaces `minidregg-link-sqlite-store durable-*` only when every criterion holds on a released,
deployed fn image. Each criterion is a check fn can run.

| id | criterion | measured or proved by |
|---|---|---|
| G1 | F1 (durable-after-ack on the served path) and F2 (served = stored) certified in the image closure | M1, M2 |
| G2 | `fn-store-1` frozen, and one later fn release opens a `fn-store-1` store without re-genesis | release notes + an open on the later image |
| G3 | D41 ST3, ST4, ST5 and ST7 served by the **default** image, not a variant; host references > 0 | image manifest |
| G4 | No per-record cost at open: open time and anonymous RSS after reopen at 10^7 records each within 2× the 10^5 figure | fundamentals harness on the release image |
| G5 | No regression against the store it replaces. On the same box and disk (hbox `tank`), sustained acknowledged-append rate ≥ Mini's measured SQLite rate, and p99 append-to-ack ≤ Mini's measured SQLite p99, at the same durability (an fsync before every ack) | Mini publishes its SQLite baseline (§6); fn runs the same workload |
| G6 | Conditional append: an append whose expected stream head ≠ current head is refused before any write; an accepted one carries F1 | ACL2 theorem certified (L1; QE-3) |
| G7 | Superseded records are releasable: a writer-authorized release over unsigned (`:absent`) records, or a deliberate change to `fn-rcl-signed-article-is-never-reclaimable` (QE-2); live reclaim funded (S152 closed, PRF-1315 certified) with bounded work per step | theorems + a measured reclaim pass at 10^6 records |
| G8 | Power-loss qualification of the deployment filesystem profile (release row 14) | the rig's run on the release image |
| G9 | S2 head commitment served, so Mini's anchor binds fn's head | command + Mini anchor check |

---

## 5. Questions

Deduplicated against FN-CHECK §4.6. Questions it already answered are not repeated: import needs no
rebase; there is no checkpoint retention class; there is no compare-and-append; binary bodies conflict
with CRLF; the tariff is 1 of 25 families.

### fn can answer

- **QF-1.** Which route for M1: restate the keystone over `owner-commit-pipeline`, or a pipeline→`owb`
  refinement? Is it in the 6.6.0 cut, and under which theorem name will the image closure carry it?
- **QF-2.** Is PRF-1287 in the cut? Will the captured-result path of `fn-asto-mca-read-span` be inside
  the proved chain or removed?
- **QF-3.** Can exit 4 `fault`, or a dropped connection, follow a durable commit? If never, Mini maps
  `fault` to `Refused`.
- **QF-4.** What reason word and exit does a conflict get on `hybrid-author` and on NNTP POST? How does
  a consumer see the second carrier (S6)?
- **QF-5.** Does P4 cover both `hybrid-author` and NNTP POST?
- **QF-6.** Will M5's grammar file cover the `fncu` bytes, so Mini can decode the cursor itself and
  drop its `consumer-inspect` subprocess? In what data language?
- **QF-7.** For M6:
  - Is the version word a header or a body line?
  - Is a deterministic author-supplied `Date` accepted however old it is? Does any fn path refuse an
    article as too old, for example on a resend after a long outage, or in peering?
- **QF-8.** What is the default profile's article size bound? Mini sizes archive bundles (K) by it.
- **QF-9.** Does each accepted article cost one transaction against `--max-transactions`, and each
  consumer ack one more? What is the largest T that fits `MemoryMax=2G` (S4)?
- **QF-10.** Will import commit a new incarnation (S1) in 6.6.0?
- **QF-11.** Is `fn-rcl-signed-article-is-never-reclaimable` certified at dev? Can any operator
  retention setting or `Expires:` remove a signed payload (S5)?

### Needs Ember

- **QE-1.** Is fn under the hot log (§4) a 6.6.x target? Does D41 move from AGREED DIRECTION to
  DECIDED?
- **QE-2.** Under the hot log, do Mini's superseded records go to fn unsigned (`:absent`, authority =
  Mini's MAC), or does fn grow a writer-authorized release over signed payloads? The second reopens
  `fn-rcl-signed-article-is-never-reclaimable`.
- **QE-3.** Conditional append needs a "stream key" and a place for its head. That is new fn
  vocabulary. Accept it in fn's model?
- **QE-4.** Rollback detection: does fn grow an external anchor (D14/D22), or does Mini keep that duty
  permanently? Mini keeps it until then either way.
- **QE-5.** Deployment shape: Mini Host and fn as the same UID on one machine (the 0600 socket, today),
  or separate failure domains and operators over the remote consumer and TLS post?
- **QE-6.** Who pays for fn's archive storage? It is permanent by theorem, and program model §G rules
  out "storage nobody pays for". Is it charged through
  Mini's storage deposits (decision G) to an fn account, or is it an operator cost outside Mini
  metering?
- **QE-7.** Confirm that Mini needs no D12 peer retention receipts or replica-count policy for 6.6.0,
  because archive replication comes from Mini's own committee members, each publishing to its own fn
  node.

---

## 6. What Mini commits to on its side

All paths are in `minidregg`.

1. **Delete the hand parsers of fn output and replace them with M5-generated decoders.**
   - The parsers: in `Host/Main.lean`, `parseFnConsumerStatus` (it splits the host-format line
     `consumer status accepted …`) and `parseFnConsumerInspect` (`fn-consumer-inspect-v1 …` text).
   - Their callers: `queryFnConsumerStatus`, `inspectFnConsumerCursor`, `queryFnConsumerPosition`,
     `classifyFnEmptyPoll` and `projectFnPoll`.
   - The new decoder module is generated; its name is chosen when M5's file exists.
   - Its Lean round-trip theorems are named in the module, and CI runs fn's vectors.
2. **Handle the five exit words distinctly (§3.5) and keep the refusal reason.**
   - `invokeFnConsumerPoll` today maps every nonzero exit to one error ("refused or was uncertain")
     and sets `stderr := .null`.
   - That violates root position 4, and it is fixed whatever fn delivers.
3. **One article profile.**
   - Replace `Kernel/FnPortableSource.lean` with an M6-generated decoder and a Lean round-trip theorem
     against the Mini renderer, and move `Kernel/FnReplyPublication.lean`'s rendering onto the same
     profile:
     - today the decoder uses `partial def decodeGroups` (no termination proof) and a fixed 7-header
       layout;
     - today no theorem relates it to the renderer.
   - Profile limits move from `Compiler/FnEvidenceCodec.lean` into the grammar.
4. **Pin the full tuple (§3.6).**
   - Extend the fn pin structures in `Host/Main.lean` (the `fnBinary`/`FnPollScopePin` pins) and
     `Kernel/FnConsumerProgress.lean` `Scope` with format word, node identity and schema digest.
   - A changed tuple refuses and re-registers.
5. **Name the identity theorems N1 and N2** in `Kernel/FnReplyPublication.lean` and
   `Kernel/FnOriginOutbox.lean`.
6. **Keep the SQLite store and `MINIANC1` authoritative.**
   - `native/hyperdocument-link-sqlite-store/src/anchor.rs` and `docs/DURABLE-STORE.md` are unchanged.
   - Add the acknowledged-Message-ID record (§3.4) under that anchor.
7. **Build the archive publisher.** It is a new module. It bundles finalized blocks and receipts
   (K by SN-2) and posts only after finality (N6), persisted-before-post through the outbox pattern.
   It also publishes replay kits and package bytes the same way.
8. **Publish Mini's hot-log baseline for G5:** the SQLite store's sustained append rate and p99
   append-to-ack, on hbox `tank`, at the default `checkpointEvery`.
9. **Treat fn cursor positions as per-pin bookkeeping only.** The empty-page records written by
   `classifyFnEmptyPoll` are scoped to the pinned store and discarded on a pin change. Nothing in Mini
   state uses an fn position as identity.
