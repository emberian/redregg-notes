# FN-DIRECT: Mini's fn archive publisher (brief, 2026-10-05)

**From** SCHOLAR-FN, now this lane's consultant (reach me with SendMessage through the root).
**Approved by** ROOT 10-05.

**Read these whole before your first command:**
- `/Users/ember/dev/redregg/work/LANE-PROTOCOL-20261004.txt`
- `/Users/ember/dev/redregg/work/BURST-LANE-BRIEF-20261005.txt` (and its 16:45Z amendment: build slots)
- `/Users/ember/dev/redregg/work/VERIFY-ONCE-20261005.txt`
- `/Users/ember/dev/redregg/designs/MINI-FN-660-REQUIREMENTS-20261004.md`, the contract: §3.3 identity and K sizing, §3.4 N1/N2/N10/N11, §3.5 failure semantics, §6, §7
- `/Users/ember/dev/redregg/work/REVIEW-SCHOLAR-FN-20261005.md` §2.2–2.5 and §5

Claims below are tagged READ (I read the code or the fn source), RECORD (a document says so) or ASSUMED.

## 0. Where you start

- **Branch.** `burst-lane1:/srv/lanes/scholar-fn/src`, branch `main` = `ec53f8c2` on GitHub main `3b709c87`. It is queued in `MERGE-QUEUE.md` as `scholar-fn`. The same branch is mirrored on the Mac at `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/c1e4d723-6d9e-4af8-a2e6-bc8abe106ecc/scratchpad/scholar-fn-bundle/scholar-fn.bundle`.
- **Your lane.** Make your own (`/srv/warm-base/mk-lane.sh fn-direct` on a burst box). Then `git fetch` that bundle, or wait for `scholar-fn` to land and rebase onto GitHub main.
- **Two commits you build on** (READ):
  - `Host/FnOutcome.lean`:
    - `inductive Class | accepted | refused | fenced | fault | usage | interrupted | notConnected`;
    - `classify : Nat → Option Class` (fn codes 0/1/3/4/5/6/7, and no code 2);
    - `Class.mayHaveActed`, with `mayHaveActed : Nat → Bool` treating an unknown code as may-have-acted;
    - `answerLine : List UInt8 → Option Answer` (`consumer STATUS[ DETAIL]`);
    - `describe`, `ackStatus`, and the theorems `classify_code`, `classify_two`, `mayHaveActed_false_iff`, `ackStatus_*_iff`.
  - `Kernel/Base64.lean`:
    - `encode`/`decode : List UInt8 → List UInt8 / Option (List UInt8)`, padded and total;
    - `decode_encode`, and `encode_decode` (canonicity);
    - `encodeLines : List UInt8 → String` (57-byte chunks → 76-character CRLF lines plus a final CRLF);
    - `chunks`, `chunks_flatten`, `encode_append`.

## 1. What FN-WIRE owns, not you

Lane FN-WIRE (agent a09e2ea1b3ec8a5cc) builds the Lean interpreter of fn's wire grammar and replaces the `fncu` hand parser. These are FN-WIRE's to delete:
- `parseFnConsumerStatus`, `parseFnConsumerInspect`;
- the `consumer-inspect` subprocess.

These stay FN-WIRE's to replace:
- FNCT and `fncu` decoding;
- the CLI text lines.

Do not write a decoder of any fn-owned byte format.
- Where you need fn's answer, use `Host.FnOutcome.classify`/`describe` on the exit code and answer line until FN-WIRE's interpreter exists, then switch to it.
- Coordinate through the root on any edit to `Host/Main.lean`'s fn helpers (`runFnLocal`, `fnLocalRefusal`, `invokeFnConsumerPoll*`, `queryFnConsumer*`).

## 2. What to build

### 2.1 `Kernel/FnArchive.lean` (new, pure)

- **Bundle codec.** A bundle is the finalized blocks of heights `[h, h+K)` with their receipts. Use Mini's canonical encoding (reuse `StreamCodec`, as `Kernel/FnReplyPublication.lean` does). Give it a version word, and prove `decode ∘ encode = id` and canonicity.
- **Message-ID.** `"<mini-archive-" ++ hex(cSHAKE256("DREGG.FN.ARCHIVE-MSGID/v1", preimage)) ++ "@" ++ domain ++ ">"`. The preimage is the framed (domain, semantics, first height, last height, bundle digest).
  - Pattern READ from `Kernel/FnReplyPublication.lean` `Selection.messageId`: cSHAKE256 under a versioned customization over a framed `identityPreimage`. Framed, because unframed concatenation admits boundary aliases (its own docstring).
- **N1 (name it).** Equal bundle bytes and context give an equal Message-ID, and the definition does no IO. State it over the function; don't use `#guard`.
- **The authored source** is the article Mini signs.
  - Headers: From, Date, Newsgroups, Subject, Message-ID, plus Mini's version header.
  - Body: `Base64.encodeLines bundleBytes`.
  - `Date` is a fixed function of the bundle (for example the finalized height's committed time), never the wall clock at send. RECORD (FN-660-RESPONSE QF-7): fn performs no Date check, adds no Injection-Date when Date and Message-ID are supplied, and refuses nothing as too old.
  - Prove that extraction inverts rendering, as `Host/GrainOriginSource.render` carries `sourceExact` (READ).
- **K sizing.** Choose K so one source fits within fn's article bound A and one poll page (262,144 returned octets, proposed v1 policy). An event over the poll page is refused by name with no skip (RECORD, fn `consumer-progress.md:122-130`).
  - K is an operator parameter, refused at configuration if one bundle at the profile's maximum block size could exceed min(A, page).
  - The sizing arithmetic is requirements §3.3 (T = H/512 rung; acks cost a transaction plus ≤ 364 octets of H).

### 2.2 The Host publisher (new Host module, called from `Host/Main.lean`)

- **Post through fn's control socket with `hybrid-author` only, never NNTP POST** (N10).
  - RECORD (FN-660-RESPONSE M3): over NNTP, duplicate, conflict, refused and uncertain all answer 441, distinguishable only by text.
  - READ: Host has no `hybrid-author` call today. Only `scripts/fn-b3/*` and `scripts/fn-e1e2/*` drive it. Host calls `hybrid-sign-carrier` and `hybrid-verify-source` (`Host/Main.lean` near 8439/8454).
- **N2 (name it).** Persist the signed artifact (source + both signatures) in Mini's store before the first send. Every resend reads those bytes and never re-signs; ML-DSA is randomized, so a re-sign is a conflict.
  - Pattern: `Kernel/FnOriginOutbox.lean` with its two-slot CAS (READ).
- **Outcomes** via `Host.FnOutcome` (requirements §3.5):
  - 0, which covers both `:accepted` and `:duplicate`: transport-acknowledged; record it (§2.3);
  - 1 `conflict`: keep Mini's own carrier as evidence; fn stored nothing;
  - 1 `busy` / `clock-unusable` / `no-owner`: retry the same bytes;
  - 1, any other reason: refused with that reason, a budget reason becoming AwaitsFunding;
  - 3 / 4 / 6: Unknown, resolved only by lookup (`ARTICLE <msgid>`, the authored source extracted and its identity checked) or by a same-bytes resend answered 0;
  - 5: a Mini defect;
  - 7: nothing was sent.
- **Output gate (N6).** Only committed and, in a committee domain, final heights are bundled.

### 2.3 The acknowledged-Message-ID record under Mini's anchor

- Each exit-0 answer appends (Message-ID, heights, bundle digest, the fn pin) to a Mini-durable record.
- It lives in the SQLite store that `MINIANC1` anchors (READ: `native/hyperdocument-link-sqlite-store/src/anchor.rs`; `docs/DURABLE-STORE.md`). Do not add a sibling file.
- **Its role:** it is Mini's authority against fn omission or rollback.
  - An acknowledged Message-ID that fn later cannot serve is evidence against fn, not a Mini loss.
  - No certified fn theorem covers durable-after-ack on the running node yet (requirements M1).

### 2.4 Read-back: withdrawn is not absent (N11)

- Fetch by Message-ID. `hybrid-verify-source` returns the authored source (READ: `docs/FN-PORTABLE-E1.md`; Host near 3328). The served article carries Xref, Path, Injection-Info and carrier lines before the authored source, and the signature covers the authored source only (RECORD, FN-660-RESPONSE C-0a).
- Extract, then decode the bundle, then compare its digest with the Message-ID's preimage.
- `430 withdrawn` and the cursor's `FNWD` report are a distinct outcome from absence (RECORD, FN-660-RESPONSE S5: a cancel is a withdrawal, and the bytes stay).
  - Report it as such.
  - Never re-publish over a withdrawal.

## 3. The two layering rules this lane must not break

1. **fn outcomes live in the sender's outbox, never in an answer slot.**
   - READ: `Kernel/AnswerSlot.lean` slots are write-once (`decided_refuses`), and `Decision.unknown` is terminal there.
   - A post's `uncertain` written into an awaiting activity's slot would close it before the post resolves.
   - So the outbox owns the post's transport outcome and retries the same bytes.
   - The slot is decided only by its decider (for a cross-domain call, the counterpart's reply, admitted when it arrives as an fn article) or expires at its deadline.
   - A sender-side `broken` on a definite transport refusal is an open design question (review §2.2, QF-B). Do not invent it here.
2. **Archive storage is a non-refundable permanent-history fee, not a §G deposit.**
   - RECORD: fn never reclaims a signed payload (PRF-088, stated, uncertified; FN-660-RESPONSE S5).
   - Charge the fee at publication, sized by octets and by fn transactions (one per article).
   - An unfunded publication is refused before posting, never hibernated.
   - Who receives the fee is Ember's QE-6. Make the recipient a configured parameter with no default.

## 4. Acceptance (the narrowest checks that could refute you)

1. One bundle of K finalized blocks is posted once.
2. An identical resend answers `:duplicate`, exit 0, and fn holds one record (check with the consumer cursor or `ARTICLE`).
3. A changed source under the same Message-ID answers `conflict`, exit 1, and fn stores nothing.
4. The bundle is fetched back by Message-ID; the authored source is extracted, and the decoded bundle's digest matches the Message-ID.
5. A cancelled (withdrawn) archive article reads back as `withdrawn`, not absent.
6. A post across an fn owner restart resolves through lookup or a same-bytes resend, never under a new identity.
7. N1 and N2, plus the codec round trips, are `#assert_axioms`-clean, and the changed modules build.

**Where checks 1–6 run:** on an **isolated** fn developer image in your own directory (pattern: `docs/FN-E2-LIVE-2026-09-24.md`; the images under `hbox:/tank/fn/images/`).
- Never `/tank/fn/node`, never fsn1, never anything under `/tank/fn/gates/` that another session owns.
- hbox is held: ask the root before using it. If no fn image is reachable from a burst box, the root decides where the native run goes. Deliver 1–5 as Lean-side theorems and fixtures meanwhile, and say which checks ran natively.

**Builds:** only your changed modules, inside a build slot (`flock -n /srv/build-slot-1 … || flock /srv/build-slot-2 …`), `SWARM_MEM_MAX=32G`. The merge keeper runs the umbrella. If you add a Host module, re-pin `scripts/check-host-closure.sh --update` and run `python3 scripts/lean-build-surfaces.py generate`. On a rebase conflict in either pin, take main's and regenerate.

## 5. Dependencies and non-goals

- **No fn change is required for items 1–7.** Everything uses `hybrid-author`, `hybrid-verify-source`, ARTICLE, and the cursor as they exist (fn deployed 6.6.0 at 09-28 source; the dev source has not run in an image, RECORD).
- **Later, from fn's 6.6.0 asks** (requirements M4/M5): extend `FnPollScopePin` with genesis node identity and schema digest once fn prints them. That is yours once M4 lands. Decoding fn's frames is FN-WIRE's.
- **Non-goals:**
  - checkpoints in fn (none, of any kind: SN-1);
  - fn under the hot log (the §4 gate);
  - deal cells and sagas (L14);
  - any change to fn.

## ROOT ADDENDUM (2026-10-05): the M2 adapter contract is part of this lane's acceptance
See designs/MINI-FN-660-REQUIREMENTS-20261004.md, addendum. Add acceptance checks: (a) bytes are exposed to the application only
after verification against Mini's independently held identity (a tampered or substituted article is refused by name); (b) an
omitted or invalid object never advances the cursor (simulate an omission and show the cursor holds and a named refusal fires);
(c) every acknowledged identity is listed by a reconciliation query after restart. M1 wording: observed acceptances ⊆ recovered;
a recovered-but-unobserved record is Unknown, resolved by Message-ID lookup.
