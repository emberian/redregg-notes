# HOLISTIC-CODEC — a judgment of nanodregg's CODEC + EMIT layer against the field (2026-10-24)

Author: the reader who wrote READ-CODEC.md yesterday (origin/main f9657bd). That memo is the defect
list. This is the judgment around it. Every claim about the code is tagged READ (path) or INFERRED.
I cite literature by name and venue/year only where I am confident; otherwise I say "the X line of
work". No edits, no builds.

---

## 1. What this layer is, in the field's terms

### 1.1 The design it instantiates

CODEC is a **verified binary-format combinator library with a canonicity guarantee**, plus a
**structural schema-fingerprint scheme** for stored and signed data, plus an **unverified
code generator** that projects a subset of the formats into Rust.

Its three parts sit in three distinct literatures:

1. **Verified parser/serializer combinators with non-malleability.**
   - The closest work:
     - **EverParse** (Ramananandro, Delignat-Lavaud, Fournet, Swamy et al., USENIX Security 2019),
       and its 3D front end for C data formats (PLDI 2022, "hardening attack surfaces");
     - **Narcissus** (Delaware, Suriyakumari, Pit-Claudel, Ye, Chlipala, ICFP 2019): encoders and
       decoders derived in Coq, correct by construction;
     - **Comparse** (Wallez, Protzenko, Bhargavan, CCS 2023): message formats for verified
       cryptographic protocols, where injectivity of the format is a security lemma;
     - the recent Verus-based combinator work (the "Vest" line);
     - in spirit, the LangSec programme (Sassaman, Patterson, Bratus et al.): parse fully before
       acting, and treat any two spellings of one value as an attack surface.
   - nano's `Lawful` (`Codec/Proofs/Stream.lean:23-28`, READ) is that literature's
     **parser-serializer inverse in both directions**. EverParse calls it "parse ∘ serialize = id and
     the parser is injective / non-malleable". nano states it as `get_of_occurs` plus an unrestricted
     `occurs_of_get`.
   - It is phrased as **occurrence at an offset** in a byte array rather than as a prefix
     decomposition of a list. That is a good engineering choice: product, array and tagged compose by
     adding offsets, with no list in sight (READ `Codec/Proofs/Stream.lean:20-28`).
   - `LawfulOn P` (`Codec/Proofs/Raw.lean:15-20`, READ) is EverParse's "refined parser": a parser
     whose accepted set is a predicate on the value, with the canonicity half unrestricted.

2. **Content addressing and schema identity.**
   - `Tag.of label c = H(domain, label ‖ shape-bytes)` (`Codec/Tag.lean:53-59`, READ) is a
     **structural schema fingerprint**. Its relatives:
     - Avro's canonical-form fingerprints;
     - Cap'n Proto's schema IDs;
     - most directly, **Unison**'s content-addressed definitions, which hash the *structure* so that
       renaming is free and editing structure changes identity;
     - Git and IPFS/IPLD content identifiers, for the "the bytes are the name" half.
   - Two pieces of the design are less common:
     - **the store refuses to open under a different stamp** (Host's `shapeMismatch`, READ
       `Host/Base.lean:474,516`): content-addressed *schema*, not just content-addressed *data*.
       Avro's object container embeds its writer schema and *resolves* old against new; nano refuses.
       Given greenfield, refusal is the right choice.
     - **canonical World bytes as a function of contents.** The World codec rebuilds every trie from
       its listing and never reads a node hash from the wire (`Codec/World.lean:83-86`, READ). This is
       the **history-independent data structure** property (the Micciancio / Naor–Teague line on
       history independence) made a codec theorem: equal Worlds have equal bytes whatever insertion
       order produced them.

3. **Code generation from a specification.**
   - The literature is **fiat-crypto** (Erbsen, Philipoom, Gross, Sloan, Chlipala, IEEE S&P 2019),
     **Low\*/KaRaMeL** (Protzenko et al., ICFP 2017), **EverParse**'s C extraction, and, from the other
     direction, **Aeneas** (Ho & Protzenko, ICFP 2022), which translates safe Rust into a pure
     functional model you can prove things about in Lean.
   - nano's `Emit/Rust.lean` is none of these. It is a **string-template generator**: hand-written
     Rust in Lean string literals, with tables and constants spliced in (READ `Emit/Rust.lean:270-561`).
     It is closest to protobuf's `protoc` or Cap'n Proto's codegen: trusted, unverified, and kept
     honest only by tests.

### 1.2 Where nano matches the state of the art

- **Canonicity as a two-sided theorem, proved once per combinator.** Here nano is at parity with
  EverParse and Narcissus at the *specification* level, and ahead of almost every deployed system.
  - Deterministic CBOR (RFC 8949 §4.2), protobuf (explicitly non-canonical) and Ethereum's SSZ
    (canonical by spec, tested not proved) all fall short of it.
  - The defects this kills are the famous ones: Bitcoin's transaction malleability through
    non-strict DER (BIP 66), ASN.1 BER versus DER, overlong UTF-8.
  - nano's varint refuses overlong spellings by construction (READ `Codec/Varint.lean:33`), which is
    exactly the DER "minimal encoding" rule as a theorem rather than a lint.
- **Every refusal is named and positioned** (`Codec/Refusal.lean`, READ). EverParse's validators
  return error codes with positions for the same reason: a parse failure is never a value.
- **Decoding never trusts a count for allocation** (READ `Codec/Raw.lean:99-100`). This is the
  standard post-2014 hardening (allocation bombs in ASN.1, zip and protobuf). nano measured it on
  hbox and fixed it (decisions/codec.md, the over-claimed count).
- **Order-preserving key encoding with a proof** (`Lang/Proofs/KeyOrder.lean:206-208`,
  `keyBytes_compare`, READ). Memcomparable formats (FoundationDB's tuple layer, CockroachDB's key
  encoding, the "lexicographic key" practice in LSM stores) are folklore. A theorem that byte order
  equals declared field order is uncommon and worth having.
- **Ed25519.**
  - Verification rejects S ≥ L and non-canonical y, and is cofactored (READ
    `Codec/Ed25519.lean:203-224`). In the taxonomy of Chalkias, Garillot and Nikolaenko ("Taming the
    many EdDSAs", SSR 2020), nano is a strict, cofactored verifier. It is stricter than Zcash's
    ZIP-215 on encodings (it refuses non-canonical points) and, like ZIP-215, it accepts small-order
    A and R. INFERRED from the code: I see no small-order check.
  - That is a defensible point in a space the field only recently mapped. It should be *named* in a
    decision entry, because ZIP-215 and RFC 8032 disagree, and libsodium and dalek disagree with both.

### 1.3 Where it is behind

1. **The specification of the primitives is the implementation.** Keccak, SHA-512 and Ed25519 are
   written once in Lean and pinned to FIPS/RFC by known-answer tests (READ `Codec/Proofs/Hash.lean`,
   `Codec/Proofs/Sha512.lean`, `Codec/Proofs/Ed25519/Test1.lean`).
   - **HACL\*** (Zinzindohoué, Bhargavan, Protzenko, Beurdouche, CCS 2017) and its successors prove the
     implementation against a separate, small, readable specification.
   - **fiat-crypto** proves field arithmetic generically.
   - nano has done real work on the field and curve: CODEC-18 and CODEC-23 prove the field ops and the
     Edwards law (INFERRED from decisions/codec.md, l.349-389 and l.520-658; I did not read
     `Field.lean` or `Curve.lean` whole).
   - But "`verify` is RFC 8032 §5.1.7" is a sample claim, not a theorem. For hashing there is no spec
     at all beyond four vectors.
2. **The emitter is a trusted pretty-printer of hand-written templates.**
   - **fiat-crypto's printer is also trusted**, but it prints a *verified intermediate
     representation*.
   - **EverParse's extracted C** is the verified program.
   - nano verifies `Layout.codec`, then prints *different code* (the Rust `Cursor`), whose relation
     to the verified codec is "written to follow it byte for byte" (READ `Emit/Rust.lean:114-118`).
3. **The compiler is trusted silently.**
   - The Lean kernel checks the vectors; the Lean compiler produces the deployed binary.
   - The field's answers to that gap, roughly in order of cost:
     - translation validation (Pnueli, Siegel, Singerman, TACAS 1998; and the CompCert
       validated-passes line);
     - differential testing of compiled code against the reference (Csmith-style; the
       fiat-crypto/HACL\* test harnesses);
     - verified compilation (CompCert; CertiCoq for Coq's extraction).
   - nano has none of these for its codec and crypto. CODEC-4 is a *measured* instance of the gap
     (READ `gates/refusals.py:59-66`; MEASURED yesterday).

### 1.4 What the literature has no name for

- **The relabelling residue, proved.** `slot_relabel_unseen` (READ
  `Codec/Proofs/RefineTooth.lean:86-98`) proves the following. A refinement whose `accept` and `back`
  are changed *together* (two same-typed constructors swapped) keeps its shape, its tag and every
  lawfulness theorem, yet means something else for the same bytes.
  - This is the classic gap between **structural** identity (Unison-style hashing) and **nominal
    meaning**.
  - I do not know a paper that proves the gap as a theorem about its own schema-hash scheme and then
    builds a *detector* for it: the codec-vectors table, red on a meaning change under an unchanged
    tag (READ `Emit/Vectors.lean:866-895`, `gates/vectors.py:36-58`).
  - The detector itself is golden or snapshot testing, keyed by the schema hash. The combination is
    novel in presentation, principled, and small.
  - I would call it a genuine contribution of a workshop paper's size: "schema fingerprints are sound
    only up to relabelling; here is the theorem, and here is a cheap, complete-for-the-drawn-vectors
    detector".
- **Refinement chains as named, ordered decode-time invariants** (READ `Codec/World.lean:229-308`,
  nine `refine`s from journal to world-budget). Here a decoded checkpoint *carries* the kernel's
  reachability invariants (`world_decode_journalOk`, `…refusalsOk`, `…height_le_steps`; READ
  `Codec/Proofs/Deployed.lean:80-130`).
  - This is "parse, don't validate" (the Alexis King folklore, 2019) taken to a checkpoint.
  - The closest formal relative is EverParse's refinement types on parsed values, applied to whole
    states.
  - It is idiosyncratic in its naming (each invariant is a separate wire refusal with its own tag),
    but sound, and the naming pays for itself in refusals by name.

---

## 2. The architecture judged (from where CODEC stands)

### 2.1 The twelve laws, as seen from the codec

| law | verdict from CODEC |
|---|---|
| 1 one of everything | **Load-bearing and right; aspirational in the small.** |
| 2 Lean decides, Rust moves bytes | **Right as a goal; aspirational as stated.** |
| 3 bytes end to end | **Load-bearing and true in Codec.** |
| 4 TigerStyle | **Mostly true, one real hole.** |
| 5 performance designed | **True where CODEC touches it.** |
| 6 named theorems, never `#guard` | **Right, with one blind spot.** |
| 7 refusals by name | **True in Codec.** |
| 8 small modules | Engineering, correct; it is a Lean 4.30 artefact (GATES-2). |
| 9 / 11 / 12 | Process; neutral from here. |
| 10 decisions examined | **Aspirational: the file has drifted from the code.** |

What each verdict rests on:

- **Law 1.**
  - Its big uses hold:
    - one `Stream` family;
    - one digest type in Codec;
    - one canonical World;
    - the store refusing old shapes.
  - Its small uses do not:
    - twin codecs per wire shape: `bytesOf`/`rawBytes`, `array`/`rawList`;
    - six hex printers;
    - Lang's variable-width `digest` datum.

    (READ, as in yesterday's D-5, D-7 and Q-2.)
  - The law is right. The census that enforces it counts modules and refine sites, not "two functions
    computing the same bytes", which is where the twins live.
- **Law 2.**
  - The emitted constants and opcode tables do satisfy it.
  - The client's frame and mux code, the custody record and the emitter's templates do not (READ
    yesterday's D-2).
  - It is also slightly wrong-headed as phrased. "Rust moves bytes" forgets that *parsing is
    deciding*. Every refusal in an emitted `decode` is an accept/refuse decision made in Rust.
  - The law should say: *Rust may run decisions only as code mechanically derived from, and checked
    against, the Lean decision.* That is what EverParse does for C.
- **Law 3.**
  - Codec is ByteArray-native with offset-based proofs (READ).
  - The few `List` uses (`leNat`'s index list in Ed25519; `Protocol.Text.unhex` over `List Char`)
    are outside the hot codec.
- **Law 4.**
  - Static bounds are everywhere.
  - The hole: the Raw family's `put` *silently truncates* outside its domain (`UInt32.ofNat`,
    `UInt64.ofNat`; READ `Codec/Raw.lean:23,33,79,93`). The domain is therefore a premise the types do
    not carry, and the law's own wording says the assertion belongs where the premise enters.
  - PROTOCOL-69's step-3 round-trip check is exactly that assertion, placed late (READ
    `Protocol/Command/Machine.lean:1292`).
- **Law 5.**
  - `size` is computed without encoding and proved equal to the encoding (READ
    `Codec/Proofs/Stream.lean:25`, CODEC-10).
  - Record bytes equal the log weight (`turn_size_logWeight`, READ `Codec/Proofs/Kernel.lean:440`).
  - That theorem is the kind of thing a performance-designed system should have and almost none do.
- **Law 6.**
  - The blind spot is that `decide +kernel` known-answer tests are named theorems about the
    *kernel's* evaluation. The deployed artefact is the *compiler's*.
  - The law correctly flags `#guard` as silent compiler trust. It has no clause for the converse:
    kernel-only evidence about a property that matters only compiled.
    - `rawList_refuses_overclaimed_count` is the clean example: a "plant" for an allocation bug that
      the kernel cannot see (READ `Codec/Proofs/Raw.lean:577-609`).
- **Law 7.**
  - `Refusal` is total and positioned.
  - Lang's run-time read of an installed package erases the name (READ `Lang/Program.lean:73-76`).
    That is outside Codec.
- **Law 10.** CODEC-3, -4, -5, -22 and -36 describe a codec that no longer exists (READ
  decisions/codec.md).

  "A decision without both critiques is not made" is a good rule. "A decision whose text the code
  contradicts is unmade" is the missing twin, and it has no gate.

### 2.2 The layer cuts, as they cross CODEC

- **Codec is not "below Kernel".**
  - It is a primitive library below Kernel, plus four modules above it: `Codec/Kernel.lean`,
    `World.lean`, `WorldSize.lean` and `Deployed.lean` all import Kernel (READ).
  - CODEC-0 named one such module. The real shape is a **sandwich**, and that is fine: codecs of
    kernel types must know kernel types.
- **The cut that costs is the hash preimages.**
  - Kernel writes its own preimage bytes: `rowKeyBytes`, `rowLeafBytes`, `rangePinBytes`, `natBytes`.
  - Codec then proves its codecs produce the same bytes (`rowKeyBytes_eq`, `rowLeafBytes_eq`, CODEC-40;
    READ decisions/codec.md l.1599-1612; INFERRED from the theorem names in `Codec/Kernel.lean:92-96`).
  - That is law 1's "two shapes that agree today", held together by a theorem. It is better than
    nothing and worse than one source.
  - The right cut: Kernel's `Env` takes the codec and hashes `codec.bytes`. The kernel is already
    generic in `Env.bytes` (READ `Codec/Deployed.lean:23-27`), so this is a re-plumbing, not a
    redesign.
- **The Lang data codec lives in Lang (`Lang/Wire/Data.lean`, READ).**
  - This cut is correct: the type language is Lang's.
  - It is built only from Codec's combinators, and its canonicity is Codec's.
  - The census sees its refine sites globally (READ `gates/census.py:37`). Good.
- **The missing cut is a format-description layer between `Codec.Layout` and Rust.**
  - `Layout` is a small format DSL (READ `Codec/Layout.lean:14-31`), the right idea (it is 3D in
    miniature).
  - What is missing is a *semantics* for the emitted side, so that "the Rust follows the Lean byte for
    byte" is a statement rather than an intention.
- **Single writer, receipts between Worlds, no agreement engine.**
  - From the codec's chair this is the right call, not a deferral. Canonical bytes plus
    content-addressed identity are exactly what make a receipt checkable by a party who holds only a
    head.
  - That property is what Certificate Transparency (RFC 6962, 2013) and the transparency-log line
    (Trillian, the verifiable data structures line, Crosby & Wallach, USENIX Security 2009) need from
    their encodings, and nano has it as a theorem.
  - An agreement engine (Tendermint-style or Calvin-style deterministic ordering) would consume the
    same codec unchanged. Nothing in Codec would have to move. That is a sign the cut is right.

### 2.3 The verification method: gates, census, plants, judge

**What the method is.** It is closer to **mutation analysis of specifications** than to anything in
the seL4/CompCert tradition. Its relatives:
- the "vacuity detection" line in model checking (Beer, Ben-David, Eisner, Rodeh, CAV 1997);
- mutation analysis for Dafny/Alloy-style specs.

A "plant" is a hand-chosen mutant that must make the theorem fail. A "tooth" is a proved negation for
a mutated definition, as in `refine_not_lawful_of_*` (READ `Codec/Proofs/Refine.lean:61-82`).

**Is it sound or hollow?** Sound for what it claims, and the claim is narrower than it sounds.
- A tooth proves that *this* mutant is caught. It says nothing about the mutants nobody wrote.
- Vacuity detection is valuable precisely because statements in this repo *have* been vacuous (the
  memory's 61 disjunct theorems; the apex at BabyBear). The project has paid for the lesson twice.
- But it is a discipline about **statements**, not about **coverage of behaviour**.

**How the classic projects establish trust.** CompCert, seL4 and IronFleet differ in kind:
- **CompCert** (Leroy, CACM 2009) has one top-level theorem, semantic preservation.
- **seL4** (Klein et al., SOSP 2009) has a chain of refinements, from an abstract spec through an
  executable spec to C, then translation validation to binary (Sewell, Myreen, Klein, PLDI 2013).
- **IronFleet** (Hawblitzel et al., SOSP 2015) refines a protocol layer to a small, human-readable
  high-level spec.

In each, the trust anchor is *a small spec a human can read*, and everything else is proved to refine
it.

**Does nano have one?**
- Partially. `Host.Proofs.Refine` states `Host ⊑ Kernel`: every Host step is an honest fold of the
  kernel's, every reopen a fold, and the codec's canonicity is its one generic premise (READ
  `Host/Proofs/Refine.lean:1-45`). That is a genuine IronFleet-shaped layer, and Codec supplies
  exactly the premise it needs (READ `:444-445`).
- But the "spec" it refines to is the Kernel: 36,789 lines (READ `SIZE.md`). That is an executable
  specification the size of an implementation.

**What a mechanised-metatheory practitioner would say about the 6,305 theorems** (READ `SIZE.md`):
- They are a large set of local properties around an executable spec. That is the Verdi/Coq practice
  *before* the top-level theorem lands.
- The missing artefact is a **small abstract model**: a few hundred lines of "a World is a map; a turn
  is a guarded update; a receipt is a membership proof". The kernel would be proved to refine it, so
  the human-readable claim "what nanodregg guarantees" has one statement.
- Without it, the plants are the only defence against a kernel that is *consistently* wrong. Plants
  catch the mutants their authors imagined.

**For Codec specifically, the top-level statement exists and is the right one.**
- `decode_eq_ok_iff` says one value, one byte string. The generic `Lawful` structure IS the spec.
- At the codec level, nano's method is adequate. The gap is entirely at the two compilers:
  - Lean source → binary;
  - Lean templates → Rust.

  The method's instruments do not look at either.

---

## 3. The details judged

### 3.1 Three choices I would defend at a top venue

**(a) Canonicity as occurrence, proved per combinator, composed by offset.**
- **What it is** (READ `Codec/Proofs/Stream.lean:20-28,85-101`, `Codec/Proofs/Raw.lean:15-20`):
  - `OccursAt b i w` plus the two laws;
  - `LawfulOn` with an unrestricted canonicity half;
  - `refine_lawfulOn_where` for refinements that carry a further invariant.
- **Why it is publishable:**
  - It is EverParse's non-malleability, restated for a dependently typed host language over native
    byte arrays.
  - It has a cleaner composition principle than the list-prefix formulations; minidregg's 22
    non-canonical decoders were in fact admitted by a round-trip-only law (READ decisions/codec.md
    l.44-46).
  - The *negative* lemmas make the refinement theorems **checks on `accept`** rather than promises:
    `refine_accept_iff` and the three `refine_not_lawful_of_*` (READ `Codec/Proofs/Refine.lean`).
  - I have not seen that framing stated this crisply. It answers the reviewer's question "how do you
    know the predicate in your lawfulness theorem is the one the parser checks?".

**(b) Structural schema fingerprints, store refusal, and the proved relabelling residue with its
detector.**
- **What it is** (READ `Codec/Tag.lean`, `Codec/Proofs/Tag.lean:225-241`,
  `Codec/Proofs/RefineTooth.lean:86-98`, `Emit/Vectors.lean`, `gates/vectors.py`):
  - the tag is injective in (label, shape) up to a named collision of two given messages (not a
    chosen one: the honest form);
  - the residue is a theorem;
  - the detector is a table that `--write` can never launder, because same-tag rows are kept verbatim
    (READ `Emit/Vectors.lean:861-865`) and the gate compares against the parent commit.
- **Why it is publishable.** It is a complete story of schema evolution under content addressing,
  with its one known hole both proved and covered.
- The Unison and IPLD communities would recognise the problem. As far as I know, neither has the
  theorem.

**(c) The checkpoint decodes to a World that carries the kernel's reachability invariants.**
- **What it is** (READ `Codec/World.lean:229-308`, `Codec/Proofs/Deployed.lean:43-139`):
  - a refinement chain on the decoded World;
  - the trie rebuilt from the listing, so history independence holds;
  - theorems that every decoded base is `JournalOk`, `RefusalsOk`, `RefusalsDisjoint` and
    `height ≤ steps`, rows headed and parented, budget below 2^64, with no premise.
- **Why it is publishable.** It is "parse, don't validate" lifted to a durable checkpoint, with the
  invariants that *reachability* would give you re-established by decoding.
- A crash-recovery story then needs no "the file was written by us" assumption. Ordinarily that
  assumption sits in the trusted computing base of every storage system: compare the FSCQ/DFSCQ line
  (Chen et al., SOSP 2015/2017), where on-disk invariants are carried by the crash logic rather than
  re-checked on read.
- nano's design is cheaper to trust: a corrupted or adversarial base either decodes to a World the
  kernel could have reached in its invariants, or it is refused by name. One caveat:
  `world_decode_canon` and friends establish the invariants, not *reachability itself*. A decoded
  World satisfying every invariant need not be one a fold reaches. The paper should say so.

### 3.2 Three choices I would be embarrassed to present

**(i) The Lean→Rust boundary is unverified string templates plus hand-written Rust framing.**
- **What it is** (READ `Emit/Rust.lean:270-561`; `client/src/frame.rs`, `mux.rs`, `custody.rs`):
  - the verified object is `Codec.Layout.codec`;
  - the deployed Rust decoders are a separate program;
  - `path_clean` is a hand port checked by 19 vectors;
  - the socket framing, child framing and custody record are written again in Rust with literal
    constants.
- **Why it embarrasses.** A reviewer from the EverParse, fiat-crypto or Aeneas communities would say
  the proofs stop exactly where the attack surface begins. On the client side the Rust *is* the
  parser of attacker-supplied bytes.
- **What a strong PhD student would build, three steps in increasing cost:**
  1. One week. Make every emitted `Layout` bilateral. The Sim generator already draws values for
     Lean's codecs (READ `Emit/Vectors.lean:46-70`). Emit those vectors for each Layout, *including
     refused byte strings*, into a Rust test that decodes and re-encodes them with the emitted code.
     Fold the hand framing (frame, mux, custody record) into `Layout`s, so that it is emitted too.
  2. One to two months. Replace string templates with a tiny Rust AST in Lean, plus an interpretation
     of that AST. Prove the interpretation of the emitted decoder equals `Layout.codec.get`. This is
     the fiat-crypto pattern: verify the IR, trust only a printer.
  3. A semester. Run **Aeneas** on the emitted Rust to obtain a Lean model of the deployed decoder,
     and prove it equal to `Layout.codec`. That closes the boundary for real. Aeneas already targets
     Lean 4, which makes nano an unusually good fit.

**(ii) Kernel-checked known-answer tests stand in for conformance of compiled crypto and codecs.**
- **What it is** (READ `Codec/Proofs/Hash.lean:5-8`, `Codec/Proofs/Sha512.lean`,
  `Codec/Proofs/Ed25519/Test1.lean:5-9`, `gates/runs.tsv`):
  - every FIPS/SP 800-185/RFC 8032 vector is `decide +kernel`;
  - the binary that signs, hashes and stores is never run on them;
  - SHA-512 has one single-block vector;
  - the CODEC-4 gate polices one source spelling of a C-emitter bug, and its advice reproduces the
    bug (MEASURED yesterday).
- **Why it embarrasses.** The project *measured* that the kernel's view and the compiler's view of a
  string literal differ, then kept treating kernel-evaluated evidence as evidence about the binary.
  - In the field's terms there is no translation validation and no differential testing of the
    extraction.
  - The Coq world learned this with extraction bugs, and is why CertiCoq exists.
- **What a strong PhD student would build:**
  - One week. One more column in the same vectors table, "compiled verdict": a `lake exe` that runs
    the *compiled* codecs, `Hash.digest`, `Sha512.hash` and `Ed25519.verify` over every kernel-checked
    vector and over the codec-vectors table, red on any disagreement. Add the NIST SHA-512 multi-block
    vectors and the RFC 8032 1023-byte TEST.
  - Fix the CODEC-4 gate to scan the *emitted C* for a `\x` escape followed by a hex digit, instead of
    scanning the Lean source. The emitted C is the thing that is wrong, and `lean -c` is cheap.
  - A year, if wanted: a validated path, i.e. emit the codec through a verified pipeline. That is not
    the right use of this project's time; the differential column buys most of it.

**(iii) Domain-predicate bounds with truncating writers, threaded as premises.**
- **What it is** (READ `Codec/Raw.lean:1-13`; the `Fits` family in `Codec/Proofs/Kernel.lean`;
  `Lang/Wire/Data.lean:33,57`):
  - the kernel's types are plain `Nat`, `List` and `ByteArray`, so the codec is lawful only on a
    `Fits` predicate;
  - `put` silently wraps outside it;
  - `Call.Fits` and `World.CodecFits` become premises that callers must discharge;
  - three listing-count premises are not discharged anywhere I could see (READ
    `Host/Proofs/Deployed.lean:459-461`);
  - one premise is re-checked at run time late, by a round trip at step 3;
  - beside that, a Lang `digest` datum is a 0–32 byte length-prefixed string because the Sim's digest
    is 8 bytes.
- **Why it embarrasses.** EverParse, Comparse and every refinement-typed format library put the bound
  in the *type of the value*, so the serializer is total and the round trip is unconditional. CODEC-3
  said the same thing on day one (READ decisions/codec.md l.55-68). The kernel then went the other way
  for convenience, and the codec paid in premises.
- **What a strong PhD student would build:**
  - A few days. Make the Raw writers refuse rather than truncate (`put : α → ByteArray →
    Option ByteArray`, or a `Fits`-indexed writer). Make `callBytes` return `Option`. The step-3 check
    becomes the type, not a run-time afterthought.
  - Weeks, as a KERNEL change. Bounded types in the kernel (`UInt64` for counters, bounded vectors for
    lists), so `Fits` disappears.
  - The Lang digest at `dc`'s fixed width is a re-genesis and a one-file change (INFERRED).

---

## 4. What to do

### 4.1 The one structural change: make the codec-vectors table the single conformance artefact, with three evaluators

The change, in two parts:
1. **Three evaluators.** Every row of `gates/codec-vectors.tsv` is evaluated by three things:
   - **the kernel**: as today, by a `decide +kernel` theorem over a sample of rows, or by the
     generator's own pure definition;
   - **the compiled Lean binary**: the same exe, with "compiled" asserted, i.e. run as the shipped
     artefact;
   - **the emitted Rust**: a generated `cargo test` that decodes each row's bytes with the emitted
     decoder and compares the verdict, refusal name and offset, and re-encodes on accept.
2. **Fold the hand framing into `Layout`s.** `frame.rs`, mux's child wire and the custody rotation
   record become `Layout`s, emitted and vector-covered. Add the published hash and signature KATs as
   rows of their own sites.

What it would make true:
- **law 2's** "the emitted Rust is the only Rust that knows a layout", checked, not asserted;
- **compiled = kernel** on every pinned vector, which closes the CODEC-4 class *at the artefact*, for
  every spelling;
- one place where a codec change is visible across Lean, binary and Rust at once.

Cost: weeks, not months. The generator, table, gate and parent-diff already exist (READ
`Emit/Vectors.lean`, `gates/vectors.py`). The Rust side is a printer of a test file, the kind
`Emit/Rust.lean` already writes for `PATH_VECTORS` (READ `Emit/Rust.lean:403-414,489-491`).

The ratio is the best in the layer: about three yesterday-findings of DEFECT/QUESTION weight close
with no change to a single proof.

### 4.2 The one thing to stop doing

**Stop writing byte-handling Rust by hand, including as Lean string templates.** Every hand-written
Rust line that reads or writes a byte layout is outside every instrument the project has:
- not in the census;
- not in the vectors;
- not in any theorem;
- not in the law-2 gate.

`client/src/frame.rs`, the inline frames in `client/src/mux.rs`, and the 72-byte record in
`client/src/custody.rs` (READ) should be emitted or deleted. New Rust that needs bytes should get a
`Layout` first.

The template bodies in `Emit/Rust.lean` should stop growing, until they are either covered by
bilateral vectors (§4.1) or replaced by an AST with a semantics (§3.2(i), step 2).

### 4.3 Overall grade

The two halves get very different grades.

**The Lean-side codec: A−.**
- Its canonicity laws are at the level of EverParse's and Narcissus' specification half.
- Its schema-identity story (shape-hashed tags, store refusal, the proved relabelling residue and its
  detector) is ahead of deployed practice and, in one respect, ahead of the literature I know.
- The minus is for twins and premises:
  - the truncating Raw writers;
  - the hash preimages written twice and proved equal;
  - decision text that contradicts the code.

**The layer as deployed: B−.**
- **The emitted Rust boundary: C.**
- **The compiled-artefact trust story: C.**

The sentence that justifies it: *the proofs establish exactly what a top venue would want of a codec,
but every deployed byte on either side of the Lean→Rust boundary is produced by an unverified
compiler or an unverified printer that none of the project's instruments examine, and the one time
the project measured that gap (CODEC-4), it patched a spelling instead of the artefact.*
