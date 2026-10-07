# REVIEW-SCHOLAR-FN (2026-10-05): fn in the program model, and the fn integration on main

**Reviewer.** SCHOLAR-FN.

**What I read.**
- The design: `designs/MINI-PROGRAM-MODEL-20261004.md` §I, §B (answer slots), §G and §6 L13.
- The root's decisions: `work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md` §I and its resolutions.
- fn's corrections: `work/FN-CHECK-20261004.md` and `work/FN-660-RESPONSE-20261004.md`.
- Code: `minidregg` main at `36fca3ac`, the fn integration in `Host/Main.lean`, `Kernel/Fn*` and `Kernel/AnswerSlot.lean`.
- fn source: read at `origin/dev` `65389a90e` (`host/native/consumer-local.lisp`, `books/outcome-class.lisp`, `books/native-control.lisp`) to check exit codes.

I own `designs/MINI-FN-660-REQUIREMENTS-20261004.md`, and I have rewritten it in place against fn's response. Its §7 holds the three decisions for Ember, with Mini's view.

## Verdict

- **The placement is right**: fn as archive, feed and exact-byte transport now, and the hot log later behind a gate.
- **The design's §I mechanism text is stale on five points** that fn's response has since corrected (§2 below).
- **The landed integration had a real defect that no fn change would have fixed.** Eight ack sites read fn's refusal as exit 2, a code fn has never emitted, so every real refusal was mislabelled and a recovery path never ran. I fixed it in lane `scholar-fn`, together with the poll paths' refused/uncertain collapse and the `partial` base64 decoder.

## 1. What the design and the code got right

- **Placement (§I, root §I).**
  - Archive, feed and transport only.
  - **No checkpoints in fn** (SN-1, accepted). fn proved this from its side: a signed payload is never reclaimable (PRF-088), so a superseded checkpoint posted signed would be kept forever.
  - SQLite plus `MINIANC1` stay authoritative.
- **Pin.** The root's §I already includes genesis node identity and schema digest, because history-id survives export/import. fn confirmed that import carries history-id, incarnation and cursors and changes only the genesis.
- **E1/E2 shape in code.**
  - `Kernel/FnConsumerOperation.lean` keys operations by (consumer domain, semantics, application, operation) and gives a changed source conflict evidence, never a second effect.
  - The ack follows Mini's own commit, and the signed artifact is persisted before posting (B3).
  - That is exactly fn's contract: the application owns the inbox, transition and outbox before the ack (`specs/applications.md`).
- **Bounded, exact readers.**
  - Every fn subprocess read is size-bounded.
  - JSON field sets are exact.
  - The cursor and report are re-read to detect a change during the call.

## 2. What is wrong or missed, with replacement text

### 2.1 §I Mechanism: per-block articles, the outcome mapping, the pin

**The text says:**
- "one signed article per finalized block";
- a mapping of fn outcomes with three words;
- the pin "(fn image digest, store history-id, format word)";
- in Decision, "checkpoints at cadence" (still in the design text, though SN-1 removed it from root §I).

**Against the evidence:**
- **Per-block articles.** fn: T = H/512 on the friend rungs, and H binds as well as T. Each consumer ack is a transaction plus up to 364 octets of H. Bundling saves T and per-record heap, not H (FN-660-RESPONSE §3.3).
- **The pin.** history-id cannot detect an import (FN-CHECK FN-24).
- **The outcome mapping.**
  - fn has seven exit classes: 0, 1, 3, 4, 5, 6, 7, and no 2.
  - Exit 1 includes the transient refusals `busy`, `clock-unusable` and no owner reached.
  - Exit 4 can follow a durable commit (`fn-fs-classify`).
- **The post path.** NNTP POST answers 441 for duplicate, conflict, refused and uncertain alike.

**Replacement for §I Decision + Mechanism:**

> **Decision.** fn is Mini's archive, feed and transport for exact bytes now: bundled finalized blocks with their receipts, replay kits, published package bytes, and cross-domain deal and saga messages. No checkpoint of any kind goes to fn. Hibernated object data and replay logs go only if paid for as permanent history. fn sits under the hot per-turn log later, behind the gate in `MINI-FN-660-REQUIREMENTS` §4.
>
> **Mechanism.** One signed archive article carries the finalized blocks of heights [h, h+K) and their receipts. Its Message-ID is Mini's digest of the bundle bytes. K is chosen so a bundle fits fn's article bound A and one poll page. The operator sizes fn's T and H together (`REQUIREMENTS` §3.3). Every Mini post goes through fn's control socket (`hybrid-author`), never NNTP POST, so duplicate, conflict, refused and uncertain arrive as distinct words.
>
> fn's exit classes map as follows:
> - 0 → transport accepted;
> - 1 `conflict` → Mini keeps its own carrier as evidence, since fn stores none;
> - 1 `busy` / `clock-unusable` / no owner → retry the same bytes;
> - 1 with any other reason → refused with that reason, a budget reason becoming `AwaitsFunding`;
> - 3, 4 and 6 → unknown, resolved only by an authoritative lookup or a same-bytes resend;
> - 5 → a Mini defect;
> - 7 → nothing was sent.
>
> Mini pins (fn running-image digest, format word, genesis node identity, schema digest, history-id, incarnation). It keeps its SQLite hot log and head anchor.

**Replacement for the §I Why sentence about caps.**
- Instead of "a live cap of 32,768 transactions", write: "fn's transaction budget is an operator profile field. The live nodes run the 16 MiB friend rung, T = 32,768 = H/512, and a raise needs a heap figure that fits the reservation."
- Instead of "Its durability theorem for the current format is not certified at current source", write: "fn's durable-after-ack keystone is stated over a batch layer the served commit never calls. Its successor is a log-kernel theorem, 4–7 lane-days, which fn has scoped (`REQUIREMENTS` M1)."

### 2.2 §I conflates a post's transport outcome with an await's answer (missed)

- The design maps fn outcomes "to the outcome sum of §B".
- The landed `Kernel/AnswerSlot.lean` makes a slot **write-once**: `decided_refuses`, plus the cell CAS and the claim spend. `unknown` is one of its terminal decisions.
- If an fn post's `uncertain` were written into the awaiting activity's slot, the slot would be closed, and the post's later resolution (it landed after all) would have nowhere to go.
- These are two layers:
  - **the outbound post's fn outcome**, which belongs to the sender's outbox;
  - **the counterpart's answer**, which belongs to the slot and is decided by the counterparty's admitted reply.

**Replacement paragraph for §I (after Mechanism):**

> fn outcomes are transport facts of an outbound post and are never written into an answer slot. The sender's outbox owns them: it retries the same persisted bytes on `Unknown` and on transient refusals until fn gives a definite answer, and records that answer. The slot is decided only by its decider: for a cross-domain call, the counterpart's reply, admitted when it arrives as an fn article. Otherwise the slot expires at its deadline (`TimedOut`).
>
> A definite, non-transient refusal of the outbound message (for example `author-not-enrolled` or `unknown-group`) cannot decide the counterpart's slot. If the activity must learn of it before the deadline, the kernel needs a sender-side `broken` rule: open question QF-B below.

**QF-B, for the calls lane.** May the sending kernel break its own pending slot when its outbox records a definite transport refusal? That is Bread's "breakage is contagious" applied to the transport. Without it, a misaddressed message costs the activity its full deadline.

### 2.3 L13's acceptance check (§6 build plan)

**The text says:** "one finalized block per article, fetched back by Message-ID and verified by Mini."

**Replacement:**

> **L13. fn archive and transport.** Modules:
> - `Kernel/FnArchive` (bundle codec, Message-ID, K sizing);
> - the publisher in Host over `hybrid-author`;
> - the acknowledged-Message-ID record under `MINIANC1`;
> - N1/N2 named.
>
> Acceptance:
> - a bundle of K finalized blocks is posted once;
> - an identical resend answers `:duplicate`, exit 0, with no second record;
> - the bundle is fetched back by Message-ID, and its authored source is extracted and verified by Mini's content identity;
> - a `430 withdrawn` answer is reported distinctly from absence;
> - a post during an fn restart resolves through `consumer position` or lookup, never through a new identity.

### 2.4 §G storage deposits vs. fn's permanent history (missed)

- §G: "storage is a deposit; unfunded objects hibernate (evicted to their Merkle hash, restorable)".
- An fn archive article can be neither evicted nor refunded: PRF-088 says it is never reclaimable.
- So fn-published history is the one storage class in Mini that is **not** a deposit.

**Replacement sentence for §G:**

> Bytes Mini publishes to fn are permanent by fn's theorem (PRF-088). They are charged a non-refundable permanent-history fee at publication, sized by octets and fn transactions, never a deposit; an unfunded publication is refused before posting, never hibernated. Who receives the fee is QE-6.

### 2.5 What the code missed (and what I fixed)

1. **Exit 2 read as "refused", at eight ack sites in `Host/Main.lean`** (the selected-release ack, the empty-page ack, the article ack session, the A own-R ack, the A reply acks).
   - fn's code table has had no exit 2 since `53d7bca5c` (2026-09-26, PRF-143). Before that, the store CLI's table was 0/1/3/4/5 (specs/host.md), so it never had one either.
   - Every real refusal (exit 1) became `transport-fault`, and each site's "refused, but already covered by the durable frontier" recovery was dead code.
   - **Fixed** (`Host/FnOutcome.ackStatus`, theorems `ackStatus_refused_iff`, `ackStatus_uncertain_iff`, `ackStatus_durableAccepted_iff`).
2. **`invokeFnConsumerPoll`, `invokeFnConsumerPollRaw`, `queryFnConsumerStatus` and `queryFnConsumerPosition`** collapsed every nonzero exit into "refused or was uncertain", with `stderr := .null`.
   - **Fixed.** One `runFnLocal` helper drains a bounded stderr prefix concurrently. `fnLocalRefusal` names fn's class and reason word.
   - `invokeFnConsumerPoll` now also requires the exact `consumer accepted` line, matching `Raw`. fn's text-mode accepted poll prints exactly that (`fnn-consumer-say`).
3. **`FnPortableSource.decodeGroups` was a `partial def`.** Nothing could be proved about Mini's E1 or selected-release body decoders. Three more files carried copy-pasted imperative `while` encoders.
   - **Fixed.** New `Kernel/Base64.lean`:
     - total padded `encode`/`decode`;
     - `decode_encode` (all byte strings) and `encode_decode` (canonicity);
     - the whole-group codec *moved* out of `Kernel/PayEnrolMemo.lean`, so there is one base64 in Mini;
     - `encode_eq_b64Encode`, `encode_append`, `chunks_flatten` and `encodeLines`.
   - The four copies are deleted.
4. **Not fixed, and QUEST below:**
   - the hand parsers of fn's text lines (`parseFnConsumerStatus`, `parseFnConsumerInspect`) and the `consumer-inspect` subprocess. They wait on fn's M5 export, and §7 D-codec sends Mini to FNCT directly;
   - N1/N2 unnamed;
   - the pin lacking node identity, which waits on M4.

## 3. The four OPEN questions, where fn bears on them

- **OPEN 3 (REPLAY).** My domain supports the provisional DRAIN/ABORT answer.
  - REPLAY needs every activity's full (Plan, Response) log retained.
  - fn cannot be its home cheaply: signed history is permanent by theorem (PRF-088), and each record costs a transaction and H.
  - SQLite would carry it uncharged, against §G.
  - Evidence: PRF-088 (`books/store-reclaim-holders.lisp:930`) and the cost model in FN-660-RESPONSE §3.3. If Ember reopens REPLAY, the log is a priced Mini cell, not fn.
- **OPEN 4 (build order).** fn needs nothing from answer slots to start.
  - L13 (archive) and the outbox fixes can land before `call`.
  - Cross-domain *transport* through fn (§2.2) depends on answer slots and on the outbox owning transport outcomes. So "answer slots and the resume contract first" also unblocks fn transport.
  - Evidence: `Kernel/AnswerSlot.lean`'s write-once rule.
- **OPEN 1 and 2.** No evidence from my domain.

## 4. Commits

Lane `scholar-fn` on burst-lane1 (`/srv/lanes/scholar-fn/src`, branch main), on GitHub main `3b709c87`, queued in MERGE-QUEUE.md:
- `48cf51f0`: `Host/FnOutcome.lean`, `Kernel/Base64.lean`, and the Host/Main, FnPortableSource, FnSelectiveReleaseArticle, GrainOriginSource and PayEnrolMemo{,V2} rewiring.
- `ec53f8c2`: `scripts/fn-e1e2/render-grain-origin-r.lean` now calls `Host.GrainOriginSource.render`. It was a drifted twin that did not elaborate on main ("Missing cases": no `.append` arm). The host-closure pin and build surfaces are regenerated.

Evidence class: COMPILED. The changed modules plus `Host.Main` built at `5f9aa259`: 3583 jobs, rc=0. All theorems are `#assert_axioms`-clean. Hygiene and import-boundary pass.

Not recompiled after the rebase onto `3b709c87`; the merge keeper gates it.

## 5. The quest I want next

**QUEST FN-DIRECT: the fn archive publisher, and Mini speaking fn's frames.**

- **Scope.**
  1. **`Kernel/FnArchive`**:
     - the bundle codec over finalized blocks and receipts;
     - Message-ID = Mini digest;
     - K sizing against A and the 262,144-octet poll page;
     - **N1** named: equal bundle bytes ⇒ equal Message-ID, with no IO in the definition.
  2. **The Host publisher**:
     - posts through `hybrid-author` only;
     - persisted before send, exact-bytes resend, **N2** named;
     - the acknowledged-Message-ID record under `MINIANC1`;
     - read-back through `hybrid-verify-source`, keeping `430 withdrawn` distinct.
  3. **Retire the hand parsers.** When fn's M5 export lands, generate the FNCT/`fncu`/`fn-e` decoders from it and delete `parseFnConsumerStatus`, `parseFnConsumerInspect` and the `consumer-inspect` subprocess.
     - Until then, a Lean `fncu` decoder transcribed from `books/consumer-position.lisp` would be a third hand decoder. I would not write it.
  4. **Extend `FnPollScopePin`** with node identity and schema digest once M4 prints them.
- **Acceptance.**
  - The L13 acceptance in §2.3, on an isolated fn developer image under `/tank/fn/gates`-style isolation (never `/tank/fn/node`).
  - N1 and N2 `#assert_axioms`-clean.
  - `lake build Minidregg +Host.Main:leanArts` green.
- **Dependencies.**
  - Items 1–2 depend only on Mini.
  - Item 3 waits on fn M5, and item 4 on fn M4. The requirements doc lists both as fn's 6.6.0 work.
