# DELVE-SCOUT — what delvetalk2 did to Objective Bend, its ATproto layer, and fn-as-ATproto (2026-10-14)

DELVE-SCOUT (Claude, read-only). Repos: `~/dev/delvetalk2` (`DT/`) at `128ab1b5` (main, 2026-10-14); Mini `/Users/ember/workbox/mini-unified-push-20261003` (`MINI/`) at origin/main `7ffd6524`; fn `~/dev/fn`. Tags: READ (path) · MEASURED (number from a doc that measured it, cited) · DERIVED · INFERRED. Sessions: `cv ls --cwd ~/dev/delvetalk2` gives 98 sessions, **all codex gpt-6.1-sol lanes** (e.g. `01a138a9` cx-night, `01a133e3`, `01a1390b`); no Claude root session is recorded under that cwd. The repo's own docs are dense, dated and commit-cited, so this report leans on them and on code, not on transcripts.

## 0. One-paragraph answer

DelveTalk is a resident Lean process (`delvetalk-obend serve`) that holds a directory of worlds and answers JSON lines over two unix sockets. A Python transport around it reads delve.town (AppView, PDS records), runs turns and writes answers. Its language is a **fork of Mini's Objective Bend** taken at Mini `dcab86da` (2026-10-08) and edited independently ever since. Mini has not touched those files since the fork, while DT grew them 1.5–4×. A counter bump costs **0.7 ms of turn work once the method is compiled** (MEASURED, `DT/docs/PERF.md` "Before and after"). Mini's comparable UPDATE costs ≈6 s, of which about ⅓ is ≈22 front-end replays (`redregg/work/perf-trace/JUDGE.md` §0). The difference is mostly not cleverness. **DT compiles a package once per process and holds the checked entry by its pin**; Mini re-runs parse/elab/check on every `loadMethod`. DT's ATproto layer is substantial and real. The town's journal is a signed atproto repo (`did:web:gsb.fg-goose.online`), and residents act by writing records into their own PDS repos, which the transport proves (DID document key + MST path) before the host runs the turn under
**principal = the DID string**. That is §7's Stage-B binding, with the verifier in the transport rather than the kernel. fn has no ATproto work at all. Its model (signed immutable articles, local journal, peer replication of portable objects) maps most naturally onto a **PDS + relay** pair, not an AppView.

## 1. What delvetalk2 did to Objective Bend

### 1.1 Provenance and divergence (READ)
- `DT/spec/bend/origin.json`: `"upstream": Mini, github.com/emberian/minidregg, commit dcab86da…`. Its scope is "Historical source attribution only … independently maintained local fork". The fork was internalized at DT `bf9a288a` (2026-10-09, "Internalize Objective Bend as the editable DelveTalk fork"). `lake-manifest.json` has
  **no packages**: the fork is vendored, not a dependency.
- Mini is 68 commits past `dcab86da`, and `git diff --stat dcab86da origin/main` is **empty** for every OB compiler and theory file checked. Mini has stood still on OB since the fork; every change is DT's (DERIVED):

| file | Mini lines | DT lines |
|---|---|---|
| `Compiler/ObjectiveBendLaw.lean` | 353 | 1526 |
| `Compiler/ObjectiveBendElaborate.lean` | 2194 | 3266 |
| `Compiler/ObjectiveBendParse.lean` | 834 | 1391 |
| `Compiler/ObjectiveBendFrontEnd.lean` | 333 | 620 |
| `Theory/ObjectiveBendDemandMachine.lean` | 284 | 567 |
| `Theory/ObjectiveBendOpenRecursion.lean` | 607 | 829 |

  DT also adds files Mini lacks: `ObjectiveBendBlame`, `ObjectiveBendSurface`, `CheckpointV3(+RoundTrip)`, `DemandCollect(+Proofs)`, `DemandSettleProofs`, `DataConformance`, `FiniteDataTyping` (`ls DT/spec/bend/*`), plus the whole `DT/spec/Delvetalk/` host (≈51K Lean lines total in `spec/`).
- Map of the kernel as DT now has it: `DT/docs/KERNEL-HANDOFF.md` §1 (stage table, proof obligations, proved/not).

### 1.2 Language changes (READ `DT/docs/FOUNDATION.md` §1, §4; `KERNEL-HANDOFF.md` §17, §21, §23, §27)
- **One effect dialect.** `Activity<A>` = `computation Message Data A`. Its only yield is a world call `world.X(arg)` / `world.X::<T>(arg)` against `world/lib/World.obend`'s `protocol world`, resumed at the call site's type. Surface `perform(...)` and three-argument `Activity<P,R,A>` are **refused by name** (§21). `write {f: op v}` is sugar for `world.write` over edits derived from the state record.
- **The State is the schema** (§23). `Edits`/`keep()` are derived from `record State` (`fixed` fields get no edit). A `form` block declares its method's input record and `forms()`, and a hand-written `forms()` beside blocks is refused.
- **Relations in state** (§14/§22/§15): `insert`/`upsert`/`retract` in `write {…}`, `relationCount`, `relationLookup` (binary search by declared key), `relations: [{field,key,limit,retain?}]` in the artifact.
- **Rank-1 generics with inferred type arguments** (`DT/spec/Delvetalk/Generics.lean`), `layer over`, sealed imports, document templates.
- **Hosted text primitives** (`textHasAny`, `textCanonicalCompare`, `natText`, `textLength`, `sha256Text`, `textJoin`, `toData`, `refuse`). KERNEL-HANDOFF §1 lists them as "hosted extensions, not upstream". The tariff charges text by bytes touched (`textStepCost`) and arithmetic past a machine word by bit length.
- **`refuse(line)`**: an activity can end its turn refused with a computed reason (§26).
- **One clause language, three modalities** (FOUNDATION §4; KERNEL-HANDOFF §27): `law NAME "reading": EXPR` refuses at commit. `rule NAME "reading": EXPR then SPELL` fires at commit under its writer. `want NAME "reading": EXPR asks SPELL` is a held lack, judged at read and at commit. The atom grammar is far past Mini's fragment. Mini's law reads only top-level nat/bool fields and `request.subject/caller/height/turn` (`redregg/work/OB-WORLD-DESIGN-20261008.md` §7.1, citing `MINI/docs/OBJECTIVE-BEND.md:727-733`). DT adds `count(new.F where COL == T and …)`, column membership `T in new.F.COL`, cross-object `"OBJECT".F`, `changed(TERM)`, `changed(new.F.COL) by T`, `insertOnly`/`appendOnly`/ `writeOnce`/`unchanged`/`monotone`, `under "kind/x"` (inherit a kind's clauses), `"OBJECT" wants NAME`, text equality, `request.clock/verb/object`. `DT/docs/LAW.md` is the design argument ("is the law impoverished?", measured against 1,763 archived posts).
- **Tenure** (FOUNDATION §4): a kind's clauses act in each instance as principal `@<id>`, which no DID can spell. The kind owner lends no authority to instance code, and the instance owner lends none to kind text.

### 1.3 What "fareoo" is
`~/dev/fareoo` is the scholar corpus on Faré's *Lambda: the Ultimate Object* (LtUO) and its Scheme sources (READ `redregg/work/OB-FAREOO-REVIEW-20261005.md:1-14`: "Objective Bend vs *Lambda: the Ultimate Object*"). In DT the fareoo influence is **architectural**, and it is in `DT/docs/WHOLENESS.md:3`. Faré's rule ("I/O effects are system calls into an outside program, the controller"; a tower's fixed top "limits the access rights of all implementations", citing FAREOO.md §8 and `fci` §5.1–5.2) becomes **the controller as an object named `world`**: its `protocol world` is the fixed top and the host is the implementation below. The lineage given is LambdaMOO `#0` plus Smalltalk VM-as-object. Concretely, the one-dialect `world.X` yield (§1.2) *is* the fareoo move. It deleted the closed sum of host ops in favour of an object interface (WHOLENESS "three changes … each deletes a closed sum or a convention"). Mini's `C4` linearization (`ObjectiveBendC4.lean`, inherited, from LtUO's `c4-linearize`) is unchanged in DT.

### 1.4 Compiler / runtime optimizations Mini should take

**(a) Held entries by pin, in a resident process (the big one).** READ `KERNEL-HANDOFF.md` §2. `PackageSession.step` keeps two per-process caches. One holds **prepared closures** (parse once, generics, `elaboratePackage`, closure check; ≤ 8 MiB source, `Bounds.frontCacheSourceBytes`). The other holds **held entries indexed by `packetSha256`** (≤ 64 MiB, `Bounds.entryCacheBytes`). `run`/`turn-start`/`turn-resume` accept `{"packetSha256": pin}` alone. `Entry.lean`'s `CheckedEntry {pin, source, checked, fuel}` and `Package.compileEntryFrom`/`executeEntry` — "None decodes the packet or re-checks the package". The memo discipline is in `DT/spec/Delvetalk/Memo.lean`, whose header says the memo "answers a pure function of its key, so which entries it holds changes only how fast an answer comes". It evicts one key, never the whole map. There is also an optional cross-process disk cache (`Host/DiskCache.lean`): the binary stamp is in the path, and every packet read is **decoded and re-checked** before use, so a damaged file fails closed to a compile. Its header names it TCB-like.
- Mini contrast: JUDGE.md §1 "Within one `loadMethod` L" gives 2 elaborations, 4 packet renders and 3 checker runs per load, and §2 says "there is no per-turn memo keyed by pin", ×≈22 per UPDATE. **Every input except `view`/`args` is a function of the pin** (JUDGE §1). DT built exactly that cache.
  - DERIVED: a pin-keyed `CheckedEntry` memo inside Mini's `loadMethod` would remove ≈30 G of ≈90 G instructions per UPDATE without any protocol change (JUDGE's INFERRED split).
  - Making Mini's Host resident (DT's `serve`) would also remove the per-process P term.

**(b) Front-end costs measured and cut** (READ `KERNEL-HANDOFF.md` §29; `DT/docs/review/slowness-2026-10-12/ ROUTING.md`):
- Cold compile of a 16-module, 135 KB closure: 50–170 ms (parse 53, generics 60, elaborate 30, whole-closure check 26), plus 2–7 ms per entry (MEASURED §29).
- `Generics.demand` memoizes each binding's `M IType` (Kind: 331M → 207M instructions).
- The quadratic `List ++` was taken out of the checkpoint encoders (`encodeTermOnto`, `@[csimp]`, proved equal: a 5,000-item start went 1.73 s → 0.78 s).
- SHA-256 now runs over an unboxed schedule window (1 MB 9.8 → 5.9 ms) (MEASURED `PERF.md`).
- Merge `c1decab7` (lane/fast-suite): "laws and library modules parsed once; journal records verified once; every compiled package cached".
- Still open: re-check of selected entries after the whole-closure check (row 7; needs a pruning or packet round-trip theorem), and the elaborator's O(k²) let chains (§16 item 27).

**(c) Where a turn then spends its time** (MEASURED `PERF.md` "What remains"): `Turn.conclude` 51.6% (checkpoint encode + digest), `prepareResumeEntry` 25.5%, the machine itself only 11.1%. The proposed fix is "do not checkpoint a segment the host answers at once". DERIVED: Mini's activity record *is* its checkpoint (OB-WORLD-DESIGN §7.1), so once (a) lands, Mini hits the same wall next.

**(d) Proved machinery Mini lacks.** `stateV3_roundTrip`, `checkpoint_resume_segment` (resuming `collect(trim(collect(settle s)))` gives the same verdict, ticks and Data), `conformsUnder_iff` (the runtime data check equals declarative typing), `stepRawFast_eq_stepRaw`, `encode_injective` for DAG-CBOR. Not proved, as DT itself says: the `noActivity` static guard vs `perform_under_update_refused`, and the CBOR decode round trip (`#guard`ed only; FOUNDATION §1).

### 1.5 Runtime structure (READ `DT/spec/Delvetalk/Serve.lean:1-4`; `docs/ROOT.md` §1.4; FOUNDATION §7)
- **One process**: `delvetalk-obend serve` takes the state directory's lock and holds every world's journal and each principal's scratch worlds. It answers **one request at a time, in arrival order**, through the world named in the envelope. The C socket glue is in `spec/native/serve.c`.
- **Two sockets.** The public socket (0600) serves front, bridge and interpreter. The root socket (0660, group) carries `world-root/dump/library/settings/fork/snapshot`; a root op on the public socket is refused, class `opener`.
- **Turns are suspend/resume**: `turn-start` → `yielded {plan, checkpoint}` → host answers the world call → `turn-resume`. A checkpoint resumes only against a digest this process issued (≤ 65,536 held), bound to `(packetSha256, object, principal, intent, rootsDigest)`.
- **Journal**: a CID-chained append log with fsync in C (`spec/native/sync.c`). Snapshots exist, and reopen replays the journal (ROUTING row 34).
- **"Carry"** replaces migration. When the program changes, the town is replayed whole into a new edition (now edition 20, `e78bd3cf`), and every name and receipt survives. This is Mini's re-genesis made lossless.
- **Python decides nothing** (FOUNDATION §7: "A Python file that chooses roles, layouts, guards or transitions is a bug"). It carries bytes and credentials only.
- Contrast: Mini runs per request as `mini activity submit` processes, each re-opening the Store and re-planning, with a consent provider spawned per process (JUDGE.md §1 rows 1, 7).

### 1.6 Divergences to know before absorbing (DERIVED from §1.1–1.5)
- **Effects.** DT's activity yields arbitrary world-protocol calls. Mini's OB turn writes only activity cells and the Book (`intent_writes_activity_or_book`, OB-WORLD-DESIGN §7.4). DT's `world` object reaches far more, and that reach is checked by the host, not by a receiver theorem.
- **Proposals and checking.** DT has no consent provider, no signed effect digest, no multi-decision planning. Admission is "judge once at commit" in one trusted process. Most of Mini's ≈22× multiplier is Mini's separate-verifier design; only the front-end-replay part is waste by DT's standard.
- **Wire and hashing.** DT is DAG-CBOR + sha256 CIDs everywhere (KERNEL-HANDOFF §3); Mini uses cSHAKE and its own framing. DT checkpoints are edition v3 only, and v1/v2 are refused.

## 2. Its ATproto / PDS integration

READ `DT/docs/ATPROTO.md` (694 lines; decisions at the end of every section), `docs/REPO.md`, `docs/POSTING.md`, `docs/design/SPACES.md`. Code: `DT/transport/{repo,requests,identity,hosted,serviceauth,oauth,lexicon,firehose, mirror}.py`, `transport/atproto/{cbor,mst,sign}.py`; lexicons under `DT/lexicons/online/fg-goose/gsb/`.

- **DT is its own repo, and a PDS-like host for its guests.** The town is `did:web:gsb.fg-goose.online`.
  - The journal is a signed atproto repo with **one commit per journal height** over an MST whose only collection is `online.fg-goose.gsb.entry/<rev>`, holding `{entry: <CID link>, height}`. Signing is k256, deterministic RFC 6979, low-S; `rev` is a TID from clock×6e7+height. Carries and key rotations open epochs with a sync commit (REPO.md "The signed repository").
  - getRepo, `since`, listRecords and getRecord are served.
  - `subscribeRepos` is built but off by default.
  - Per-reader views (cards, pages, answers) are **projections outside the tree**, via `online.fg-goose.gsb.getProjection`, because what a reader may see varies (REPO.md).
- **It is a client of delve.town.** `pds.delve.town` (v0.5.34) has a gated firehose (401). So DT polls `com.atproto.sync.listRepos` and `getLatestCommit`, then lists each participant's `online.fg-goose.gsb.request` collection (ATPROTO §2a, `transport/requests.py`).
- **Posts are a second way in.** Mentions of `@livedelvetalk.delve.town` are a fictional handle matched as text. Replies are drafted to an outbox, and Ember posts them by hand as `ember.delve.town` (README §1; `transport/post.py` behind `--i-am-ember-and-authorize-posting`).
- **How a record becomes a turn.** A resident writes `{service: did:web:gsb…, mode: act|plan, calls:[{spell}…], if:[{object,version,cid?}]}` in their own repo.
  - The bridge fetches it by `com.atproto.sync.getRecord`, gets the signed v3 commit and the MST path, and
    **verifies the signature under the DID document's `#atproto` key**. did:plc resolves via plc.directory; did:web via its host; the document is cached for 10 minutes.
  - It then runs `world-turn` with **principal = DID** and **intent = the at-uri**.
  - A URI is consumed once, under its first proven CID, so `putRecord` over an answered request does not re-run it.
  - A request older than the world's `since` is never run.
  - `if:` is commit-if-unchanged, refused `moved`.
  - The answer is written as `online.fg-goose.gsb.answer/<did>.<rkey>`, holding a strongRef to the request, `outcome`, and `receipt {slug, height, entry CID}`. It is the anonymous reader's projection only (ATPROTO §2).
- **Trust** (FOUNDATION §7; ATPROTO §2):
  - Post authors are observed through the AppView and treated as UNVERIFIED in `bridge.py`. "Posting on delve.town is the authentication: the PDS vouches for the author".
  - Request records are **proven** ("The first act in the town whose author is proven, not observed").
  - The host trusts whatever principal its public-socket caller names. The DID check lives in Python transport, not in Lean (DERIVED from ROOT.md §1.4 and FOUNDATION §7).
- **Identity mapping** (ATPROTO §4, `identity.hosted_identity`):
  - External residents keep their own did:plc / did:web as principal.
  - Invitation guests and Zulip users get hosted DIDs, `did:web:<name>.guest.<host>` and `did:web:<id>.<realm>.zulip.<host>`, with k256 keys derived by HKDF from the town key. These are request-only repos, written with a bearer credential.
  - All of this is **built but off** (`hosted_accounts=false`; Ember declined wildcard DNS).
  - The web front's identity claim is atproto OAuth, scope `atproto`, identity only, with tokens revoked at once (`oauth.py`).
  - Inbound service auth is `serviceauth.py`; its nonces are retained durably (`79bcb9b8`).
- **Persistence.** The journal and its blocks are in `<state>/worlds/<world>/`. The repo ledger is `repo.json`. Request scan state is `requests.json` plus `observe.sqlite`, and answers go under `answers/`. Hosted accounts are `<state>/hosted/<origin>/<name>.json`.
- **Next (designed, not built).** atproto Spaces: a private *desk* per resident for requests, *seats* for hidden views, and a public **digest of every turn** in the signed tree (`DT/docs/design/SPACES.md`, merge `128ab1b5`).

**Mini's angle (against OB-WORLD-DESIGN §7).**
- **Does DT already do the binding?** Yes, at the transport layer. §7.3 called "the owner's `merge` is the only consent" the honest limit: "a statement about an atproto signature the kernel cannot verify", with Stage B binding DID↔subject. DT ships Stage B's *mechanism* for record-borne acts. The principal *is* the DID, proven by commit signature + MST inclusion before the turn. DT does not close the honest limit, though; it relocates it. The Lean host never sees the proof, so "the DID signed this" is a property of `transport/requests.py` plus `atproto/{mst,sign}.py` (Python), not of the receiver (DERIVED). For Mini that is exactly Stage A's labelled trust relocation, made precise and narrower.
- **Reusable verbatim** (INFERRED that they port cleanly; all are self-contained Python):
  - `transport/atproto/{cbor,mst,sign}.py`: the DAG-CBOR, MST and k256 commit code. DT tests them against 166 AppView `record`/`cid` pairs (KERNEL-HANDOFF §3).
  - The request→turn consumer: proven fetch, once-per-URI-under-first-CID, the `since` floor, `if:` as swapRecord at object grain. This is §7.2's idempotence table with the nonce = record CID idea already built.
  - The request/answer lexicon pair (`DT/lexicons/online/fg-goose/gsb/`), as a template under Mini's own NSID.
  - The "journal as signed repo, one commit per height, entry CID as the only leaf, projections outside the tree" design. It answers how Mini publishes a Turn log without publishing private state.
- **What Mini should do differently.** Lift the DID-signature check into the kernel's evidence. Mini already has a signed command + nonce (§7.2), so the proven `(did, at-uri, cid, commit sig, MST path)` should ride as checked input, not as a transport assertion. That is the step DT's architecture cannot take, since its host trusts the socket.

## 3. fn as ATproto (one page; mostly INFERRED, because fn has no ATproto design)

**What fn is** (READ `~/dev/fn/README.md`; `docs/architecture.md`; `docs/glossary.md`). fn is a news server that speaks NNTP. ACL2 makes every decision through a `step(state, event) → (state', effects)` core, with a Common Lisp I/O host.
- **Content objects** are immutable typed bytes under a domain-separated BLAKE3 digest. The **Message-ID** is a separate news identity.
- **Articles** are signed over their *exact authored bytes*: D09 requires **both Ed25519 and ML-DSA-65**. Mutable NNTP trace headers are kept in separate projections.
- **Statements and receipts** are immutable issuer-scoped assertions, with authority checked separately.
- The **journal** is the authoritative local transaction log, with checkpoints. Retention obligations, reservations and pins are first-class.
- **Replication** exchanges portable objects and statements (never pages) with peers, carried media, or Bundle Protocol. Sequence numbers are local; articles are portable.
- The stated long-term direction is "a persistent event-log substrate … with minidregg and breadstuffs layered on" (architecture.md "Purpose", ember 2026-09-30).
- Grep across `docs/` and `planning/`: the only matches for atproto/"at protocol" are false positives ("at protocol-only"). **fn has no ATproto work** (READ).

**Role fit (INFERRED).**
- **PDS (fits best).** A PDS holds one signed repo per account; fn holds signed authored objects per principal.
- **Relay (fits second).** fn's replication machine already does inventories, batches and duplicate suppression of portable signed objects. A relay is that, over firehose frames. fn's retention obligations ("why do I keep this, what evidence releases it") are the thing relays lack.
- **AppView (fits least).** NNTP groups are fn's *projections*, so an AppView-shaped role exists, but it is the thin part.

**What fn would have to expose:**
1. **DID documents.** Each fn principal needs a `did:web` (or did:plc) whose `#atproto` key is secp256k1 or p256.
   - ATproto does not accept Ed25519 or ML-DSA as the repo signing key. fn would either sign repo commits with an
     **additional** k256 key, keeping D09's dual signature on the article bytes inside the record, or define the article signature as a record field that the commit merely carries.
   - DERIVED: two signatures with distinct meanings: the commit vouches for inclusion, the article signature for authorship.
2. **A repo per principal**: an MST of records, where an article is `<nsid>.article/<tid>` holding the authored bytes or a blob ref, with Message-ID, groups and the dual signature.
   - Commits are DAG-CBOR v3 with sha256 CIDs, so fn's BLAKE3 object ID becomes a field, not the CID.
   - fn already has an ACL2 CBOR profile (`books/cbor.lisp`, `docs/cbor-interop.md`). DAG-CBOR's canonical rules (map key order by length then bytes, tag 42 links) are a profile delta, and DT's `Canonical.lean` plus its 166-pair AppView fixture is the reference to test it against.
3. **XRPC**: `com.atproto.sync.{getRepo,getRecord,getLatestCommit,listRepos}` and `com.atproto.repo.{describeRepo, listRecords,getRecord}` read-only first; write methods only for local principals.
4. **Firehose**: `subscribeRepos` `#commit` frames. These are fn's replication batches re-framed. Mapping `#sync`/rev semantics onto fn's per-origin **incarnation** (which stops a restored node from reusing sequence ids) is the subtle part.

**Mini's Turn log in that world (INFERRED).** Use DT's shape, not "every Turn is a record":
- a Mini node is a repo `did:web:<node>`;
- one record per committed Turn under a Mini NSID (`<nsid>.turn/<rev>`), holding `{turn: <CID link to the canonical Turn bytes>, height, effectsDigest}`, signed per height;
- private state stays in projections outside the tree (DT REPO.md).

Requests arrive as records in the requester's own repo, as in DT §2a, and a lexicon pair (request/receipt) is the API. fn's part is to carry and retain those repos (relay + obligations) across sleeping and disconnected peers, which is what fn is for.

**Smallest experiment (INFERRED).** A read-only `did:web` repo exported by fn for **one** principal:
- MST + v3 commit over its existing articles as `<nsid>.article` records, signed with a fresh k256 key.
- Serve `getRepo` and `getRecord` from the NNTP node's existing web face (WEB-005).
- Pass = DT's own verifier (`transport/atproto/mst.py` + `sign.py`, the same `proven` path its bridge uses), plus an off-the-shelf atproto client, fetching and verifying one article with its inclusion proof.

This touches no fn decision logic; it is a projection. It would show whether fn's object and journal model exports losslessly before anyone designs a relay.

## 4. The one thing Mini should take first

**A pin-keyed checked-entry memo inside `loadMethod`**, in the shape of DT's `PackageSession` held entries (`DT/spec/Delvetalk/Entry.lean`, `Memo.lean`; KERNEL-HANDOFF §2):
- the package's prepared closure and each method's checked entry are computed once per process per `packetSha256`, with bounded single-key eviction;
- every later decision reuses them, re-running only the request-dependent `check applied [] typeFuel` on `view args`.

JUDGE.md shows everything else in a load is a function of the pin. This needs no protocol change, and it is the largest single line item in Mini's ≈22× per-UPDATE multiplier (≈⅓ of instructions, JUDGE §2 INFERRED split). A resident Host (DT's `serve`) is second, the ATproto request consumer third.
