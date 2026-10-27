# READ-CODEC — nanodregg CODEC + EMIT, whole-file read (2026-10-24, origin/main f9657bd)

Reader: one sub-Opus. Edited nothing in nanodregg. One scratch measurement under my own scratchpad
(`/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a167c9-1142-7bc2-a1e6-b2cf23dfde66/scratchpad/esc/`).

## Verdict

I read the definition side of Codec whole: Kernel, Stream, Raw, Varint, Refusal, Deployed, Tree, Tag,
Path, Layout, World, WorldSize and Digest. On the proof side I read Proofs/Deployed, Proofs/Refine,
Proofs/RefineTooth and Proofs/Digest whole. I read the statement and definition parts of Proofs/Stream,
Proofs/Raw, Proofs/Kernel, Proofs/Tag, Proofs/Varint, Proofs/Tree, Proofs/Hash, Proofs/Sha512,
Proofs/ListingPin and Proofs/RowsReached, plus about half of Ed25519.lean. I read Emit/Rust, Vectors,
Hosting, Broker and Pins whole. From Lang I read the data and package codec: Wire.lean,
Wire/Data.lean, Package.lean §Wire, Proofs/Data, and the version section of Proofs/Wire. I followed
call sites into Lang/Call, Lang/Program, Protocol/Command/{Machine, Verb, Text}, Protocol/Frames,
Protocol/Proofs/Command, Host/Proofs/Refine, Host/Wire, gates/refusals.py, gates/vectors.py,
Census/Refines, and the Rust under client/src.

The codec core is in good shape. `Lawful`/`LawfulOn` state canonicity in both directions:
`occurs_of_get` is unrestricted, so whatever decodes is exactly the bytes of the value it decodes to.
`eq_callBytes_of_decodeCall` is unconditional. The package codec is lawful on exactly
`packageWire ∧ fits`. The data codec has `decodeData_eq_ok_iff`. I found no non-canonical decoder
anywhere in Codec, and no `native_decide`, `partial`, `unsafe` or `#guard` in Codec or Emit.

**The three worst things:**

1. **The CODEC-4 gate protects against one spelling of the hazard, and recommends a spelling that
   reproduces it (MEASURED).** `gates/refusals.py` refuses only the source text `\xHH<hex>`. Its own
   advice, `"\x00" ++ "b"`, is constant-folded by LCNF into the C literal `"\x00b"`. `"a\u0000b"` is
   emitted as `"a\x00b"` and slips past the regex. Compiled code gives `[11, 0]`; the interpreter
   gives `[0, 98]`. The tree is clean today (grep), so this is a latent defect in the gate, not live
   damage.
2. **Law 2 does not hold as stated: the emitted files are not the only Rust that knows a byte
   layout.** These are hand-written in Rust:
   - `client/src/frame.rs`: the socket frame;
   - `client/src/mux.rs`: the child wire and the close frame, assembled inline twice, one with
     `unwrap_or(u32::MAX)`;
   - `client/src/custody.rs`: the rotation record `u64le ‖ 32 ‖ 32`, read back as 72 bytes;
   - the constants `HEADER = 4` and `CONN = 4`.

   The emitted readers, `path_clean` and `frameIo` are also hand-written Rust, kept as string
   templates inside `Emit/Rust.lean`. Only `path_clean` has a differential check (19 vectors).
3. **Compiled-side conformance of the deployed hash and signature code is not checked.** Every
   published vector (SHA3, cSHAKE, KMAC, SHA-512, RFC 8032) is `decide +kernel`. The deployed host
   runs the compiled code. CODEC-4 is exactly a case where kernel and compiled disagree. SHA-512's one
   vector, and both RFC Ed25519 tests, use single-block SHA-512 inputs, while deployed calls are
   multi-block.

The rest are debts:
- Decision entries contradicted by the code: CODEC-3, -4, -5, -22, -36.
- Comments that misdescribe the layout under them: `Codec/Kernel.lean:25`, `Codec/Stream.lean:9`
  and `:16`, `Tag.lean:9`, `Refusal.lean:17`.
- Six copies of the hex digit.
- A tooth named for a regression it cannot see: `rawList_refuses_overclaimed_count`.
- `argvSize` as a second size computation that no theorem ties to the command codec.

## Answers to the brief's specific questions

- **Canonicity, both directions.**
  - Generic: `Lawful` (`Codec/Proofs/Stream.lean:23-28`) and `LawfulOn` (`Codec/Proofs/Raw.lean:15-20`)
    carry both `get_of_occurs` (decode ∘ encode = id on the domain) and `occurs_of_get`, which is
    unrestricted (encode ∘ decode = id on everything decodable, and the decoded value is in the
    domain). READ.
  - Call codec: `decodeCall_callBytes` needs `Call.Fits` (`Codec/Proofs/Kernel.lean:368-371`).
    `eq_callBytes_of_decodeCall` has no premise and returns `Call.Fits ∧ b = callBytes c`
    (`:373-381`, and at the deployed instance `Codec/Proofs/Deployed.lean:39-41`). READ.
  - PROTOCOL-69's step-3 check (`Protocol/Command/Machine.lean:1292`,
    `X.decodeCall (X.callBytes c) ≠ some c → badCall`) re-checks the Fits-conditional direction at
    run time, for a call `⟨u, s2.signature⟩` whose Fits nothing carries. It can be reached:
    - a custody signature longer than `callMax`. The frame allows up to 262,144 bytes and
      `rawBytes callMax` refuses it on read;
    - or any `nat64` field at or above 2^64 in the plan.
    READ (sites); INFERRED (reachability).
  - The other direction is never assumed in the codec. Host's `hX` premise is discharged at the
    deployed `Ctx` from `eq_callBytes_of_decodeCall` (`Host/Proofs/Refine.lean:444-445`). READ.
  - A non-canonical encoding that decodes: none in Codec, Lang.Wire or Protocol.Text (lowercase hex
    only, `Protocol/Command/Text.lean:30-33`). `Lang/Call.lean:24-25`'s "not canonical, by design" is
    about data → Body, not bytes. READ.
- **`Conforms` and `ofData`'s domain.**
  - `ofData_of_conforms` (`Lang/Proofs/Data.lean:340`) gives Conforms ⊆ domain at every type.
  - `toData_ofData` with `toData_conforms` gives domain ⊆ Conforms at `T.wf` types. INFERRED by
    composition; no named iff exists. Both use "first arm with that label", so they agree at non-wf
    types too. READ.
  - `encodeData_of_conforms` (`:365`) is exactly the needed totality at `dataTy`. Both sets are wider
    than the deployed digest (see Q-3).
- **Package version.**
  - `packageVersion` (`Lang/Package.lean:797-799`) refuses any first byte other than 5 as
    `rejected 0 "lang/package-version/5"`, before any tree is read
    (`decodePackage_wrong_version`, `unversioned_package_refused`, `Lang/Proofs/Wire.lean:842-862`).
  - Install surfaces it by name (`Lang/Program.lean:236-238`, `decodeText e`).
  - The run-time read of an installed cell does not: `readPackage` maps every decode refusal to
    `malformedCell id 0` (`Lang/Program.lean:73-76`). See Q-5. READ.
- **argv 132,096 (PROTOCOL-68).**
  - `Protocol/Table.lean:422`: `2 * Kernel.Bounds.eventBytesMax + 1024`.
  - Hex is counted: `toHex_utf8ByteSize`, two bytes per byte (`Protocol/Proofs/Command.lean:47-68`).
  - The argv framing is counted as `argvSize = 4 + Σ(4 + len)` (`Protocol/Command/Verb.lean:234`).
  - The frame's op byte is counted: `argv_fits_frame : argvBytesMax + 1 ≤ frameBytesMax`
    (`Protocol/Proofs/Table.lean:105`).
  - `receipt_argv_fits` assumes `call.size ≤ eventBytesMax`. That is the Turn's `event = callBytes c`
    bound, not the per-field `callMax`, so it is the right premise.
  - Gaps:
    - `argvSize` is not tied to the codec's size (D-9);
    - `cancel CALL` has no fit theorem (it does fit: 4 + 10 + 4 + 131,072 = 131,090);
    - the `+ 1024` is unexplained.

    READ.
- **`partial` / `unsafe` / `native_decide` / `#guard` in Codec and Emit:** none.
  - MEASURED: `grep -rnE '\bpartial\b|\bunsafe\b|native_decide|#guard|implemented_by|@\[extern|sorry'`
    over Codec and Emit; the only hits are prose.
  - The tree's one `native_decide`, `Hosting.Proofs.invoke_slots` (`Hosting/Proofs/Deployed.lean:60-62`,
    allow row in `gates/axioms-allow.tsv`), runs `Wire.encodeData` and the compiled package and slot
    codecs. It is the one theorem that trusts the C backend through the codec. Its path holds no
    string literal with a control character (grep). INFERRED: it is safe today.
- **CODEC-4 (`\x` escapes).** No Lean source has `\xHH` followed by a hex digit. MEASURED:
  `git ls-files '*.lean' | xargs grep -nE '\\x[0-9a-fA-F]{3}'` is empty, and the two `\x00` hits are
  comments (`Emit/Rust.lean:407`, `Host/Sim/Sock.lean:9`). The hazard is wider than that spelling
  (D-1).

---

## Findings, ranked

### DEFECT

**D-1. The miscompile gate is spelling-based, and its advice reproduces the miscompile.**
`gates/refusals.py:59-66`, `decisions/codec.md:745-748` (CODEC-27).
- **What is wrong.**
  - The gate refuses only `\xHH` directly followed by a hex digit, inside one literal
    (`GREEDY_X`, l.66).
  - Its comment tells the author to "end the literal (`"\x00" ++ "b"`)".
  - Lean 4.30's LCNF constant-folds `String.append` of two literals (toolchain
    `Lean/Compiler/LCNF/Simp/ConstantFold.lean:434`).
  - `quoteString` (`Lean/Compiler/LCNF/EmitC.lean:213-227`) then writes every char ≤ 31 other than
    `\n \r \t` as a two-digit `\x`, which C reads greedily.
  - So the hazard is "a control character followed by a hex-digit character, in any literal the
    compiler can fold". It is not one source spelling.
- **Why it is wrong.** A gate that names a fix producing the very bytes it guards against is a check
  that cannot see its own class (law 6/7 spirit; "a falsifier that stopped falsifying").
- **Mutation that shows it (MEASURED).** `scratchpad/esc/Esc.lean`:
  - `def viaAppend : String := "\x00" ++ "b"` and `def viaUnicode : String := "a\u0000b"`;
  - `lean -c` emits `m_data = "\x00b"` and `m_data = "a\x00b"`;
  - the compiled binary prints `[11, 0] [97, 11, 0]`;
  - `lean --run` prints `[0, 98] [97, 0, 98]`;
  - neither spelling matches `GREEDY_X`.
- **Current exposure.** None found: no `\uXXXX` control escape in source. The `\\u…` and `\\b\\f` in
  `Hosting/Proofs/Reply.lean:71,117` are escaped backslashes. No source file holds raw control bytes.
  MEASURED (grep).
- CODEC-27's sentence "No Lean source in this repo has `\xHH` followed by a hex digit" is true, but it
  names the wrong invariant.
- Severity DEFECT, in the gate. The codec is unaffected.

**D-2. Law 2: hand-written Rust knows byte layouts that Lean also defines.**
- **The hand-written Rust:**
  - `client/src/frame.rs:1-6,69,98,130`: `u32le len ‖ op ‖ payload`, `HEADER = 4`. Its Lean twin is
    `Host/Wire.lean:3-6,25,48-56`.
  - `client/src/mux.rs:41,155-166,453`: the `u32 conn` child wire, `CONN = 4`, and `close_frame` built
    by hand. `u32::try_from(...).unwrap_or(u32::MAX)` writes a wrong length silently on overflow,
    where `frame::write_body` refuses.
  - `client/src/join.rs:76`: `frame_bytes_max.saturating_add(4)` restates Lean's
    `bodyMax = frameBytesMax + 4`.
  - `client/src/custody.rs:531,541-549`: the persisted rotation record `n u64le ‖ incoming 32 ‖ pending 32`,
    read as exactly 72 bytes.
- **What is wrong.** The charter says Rust "consumes Lean-generated tables (opcodes, bounds), never
  hand-copied constants". The brief asks whether the emitted Rust is the ONLY Rust that knows a byte
  layout. It is not.
- **Inside Emit:**
  - The `Cursor` readers and `put_*` writers (`Emit/Rust.lean:270-391`), `path_clean` (`:420-433`)
    and `frameIo` (`:493-561`) are hand-written Rust held as Lean string templates.
  - The emitter fills in constants and field lists. The control flow is a twin of
    `Codec.Layout.codec`, `Codec.Path.clean` and the Lean pipe framing.
  - Only `path_clean` is differentially checked (19 `PATH_VECTORS`, `launcher/tests/path_vectors.rs`).
    No vector checks the emitted `Command`/`Step`/`Action` decoders against Lean's codec.
- `client/tests/roundtrip.rs:1-8` is a third copy in Python, labelled "STAND-IN … replaced … once HOST
  commits those executables". HOST has committed them.
- **Mutation that shows it.** Change `Host.Wire.bodyMax` to `frameBytesMax + 8`. Every Rust consumer
  keeps `+ 4`, and nothing re-emits or reds. INFERRED.
- Severity: DEFECT against law 2's text. The framing is transport, which law 2 allows Rust to own,
  but not as a hand copy of a Lean constant.

### QUESTION

**Q-1. Compiled conformance of hash and signature code.**
`Codec/Proofs/Hash.lean:5-8` ("No `native_decide` is used and no compiler is trusted"),
`Codec/Proofs/Sha512.lean`, `Codec/Proofs/Ed25519/Test1.lean:5-9`.
- **What is wrong.**
  - Every published vector is `decide +kernel`, so it proves the kernel's reduction of
    `Hash.digest` / `Sha512.hash` / `Ed25519.verify`, not what the `host` binary computes.
  - CODEC-4 measured kernel ≠ compiled once, for string literals.
  - No compiled-side run of the FIPS/SP800-185/RFC 8032 vectors exists. MEASURED: no row in
    `gates/runs.tsv`, and the non-proof `.lean` files have no published-vector check.
  - A compiled miscompile of Keccak would be self-consistent between writer and follower, both
    compiled, so no sim or row reds.
- **Second gap.** SHA-512 has one vector, "abc", a single block (`Sha512.lean` proofs l.8-11). RFC
  TEST 1 and TEST 2 hash 64- and 65-byte inputs, also single block. Deployed calls hash
  `R ‖ A ‖ callMessage` of hundreds of bytes, so multi-block padding has no Lean-side published
  vector at all.
- **What would decide it.**
  - Is there an interop test in which Rust custody (an independent Ed25519) signs a multi-block
    message and the compiled Lean `verify` accepts it? INFERRED from the launcher tests: probably
    yes, covering SHA-512 and Ed25519 multi-block, but not cSHAKE.
  - Does any run of the compiled `host` print `Hash.digest` of a published sample?

**Q-2. Law 1: the Lang wire carries a second digest shape, sized by the Sim.**
`Lang/Wire/Data.lean:33,57`, `Lang/Bounds.lean:20-22`, `Lang/Proofs/Data.lean:25`.
- **What is wrong.**
  - A Lang `.digest` datum is `bytesOf digestBytesMax`: a u32 length, then 0 to 32 bytes.
    `Codec/Digest.lean:1-3` says "A digest is exactly 32 bytes", and the charter's law 1 says "one
    digest type (32 fixed bytes)".
  - The 32-byte bound is chosen because "the Sim's is 8" (Bounds l.20).
  - At deployment, a 5-byte `.digest` datum conforms, encodes (`encodeData_of_conforms`), travels as
    an invoke's `args` and decodes in the callee. It is refused only where `digestOf` is asked
    (LANG-38).
  - The codec vectors pin "a 31-byte digest before a 32-byte one" as an ordinary key
    (`Emit/Vectors.lean:581-585,598-601`).
  - A deployed digest datum costs 36 bytes where 32 would do.
- **What would decide it.** A ruling on whether "toy parameters in the real pipeline" extends to a
  toy-driven width in the deployed wire, or whether `.digest` should be `Stream.digest` at
  `dc`'s width.

**Q-3. `Conforms` and `ofData`'s domain agree, but no theorem says so.**
`Lang/Proofs/Data.lean:340-368`.
- Inclusion one way is a theorem.
- The other way holds at `T.wf` by composing `toData_ofData` (l.111) and `toData_conforms` (l.264).
  INFERRED; not stated.
- What would decide it: a stated `(ofData T d).isSome ↔ Conforms d T` (at `T.wf`). That is a
  one-line corollary; it would make LANG-77's "the encoder never refuses checked output" read as an
  equivalence rather than a containment.

**Q-4. Codec-vector coverage is Sim-only.**
`Emit/Vectors.lean:21-23,722-813`.
- Every kernel site is drawn at `Sim.dc` (u64 digest). No vector exercises the deployed
  `Stream.digest` / `Digest.ofBytes?` / `Hash.digest` instance.
- Sound for refine meaning, since refine sites are generic in `dc`.
- The ListingPin byte pins (`Codec/Proofs/ListingPin.lean:89-149`) are also Sim-only.
- What would decide it: whether a deployed-instance row (one call, one World at `digestCodec`) is
  wanted as the compiled-codec plant (cf. Q-1).

**Q-5. The version refusal is erased at run-time package reads.**
`Lang/Program.lean:68-76`.
- `readPackage` maps every `decodePackage` refusal, including `lang/package-version/5`, to
  `malformedCell id 0`. Install keeps the name (`:236-238`).
- Old-version ROM cells should be unreachable after re-genesis (old Store shapes refuse to load), so
  this is low.
- What would decide it: is there any path where package bytes enter a ROM cell without
  `checkInstall` (genesis, carry import)? If so, law 7 wants the version name kept.

**Q-6. `rawList.put` silently wraps a count of 2^32 or more.**
`Codec/Raw.lean:93`, `Codec/World.lean:71` (`worldMax = 2^32 - 1`),
`Host/Proofs/Deployed.lean:459-461`.
- `put` writes `UInt32.ofNat l.length`, so a listing of 2^32 entries writes count 0 and its bytes
  decode as something else.
- `codecFits_of_kept` takes the three listing counts as premises (`hcount`, `hrcount`, `hfcount`).
- `rowsCodecFits_of_ok` takes `hlen` (`Codec/Proofs/RowsReached.lean:103-105`).
- The rows' parents are "not statically bounded" (`Codec/World.lean:206-208`). The budget
  `weight + allowance < 2^64` allows about 5·10^17 rows of at least 34 bytes, so it does not imply
  `hlen`.
- What would decide it: whether HOST's `worldBytesMax` (derived in `Bench/WorstWorld.lean`) is
  checked from `world.size` BEFORE `put`, and is below 2^32 × the minimum entry size. If it is, name
  that as the discharge of `hrcount`.

### DEBT

**D-3. Decision entries the code no longer matches** (`decisions/codec.md`; law 10).
- CODEC-4 (l.70-80): "Integers are fixed width, little-endian; no variable-length naturals …
  Status: open." Contradicted by:
  - `Codec/Varint.lean` (`varint`, `varint64`, `bytesV`; CODEC-13/37/40);
  - `Stream.u64be` (big-endian, LANG-57; `Codec/Stream.lean:146-158`).

  Its critique, "Today nothing sorts integers by bytes", is false since LANG-57 (`keyBytes_compare`).
- CODEC-5 (l.82-98): "No hand-written tag literal, no census, no fingerprint pins, no `/vN` chains."
  Contradicted by:
  - the refine census (`Census/Refines.lean`);
  - the byte pins (`Codec/Proofs/ListingPin.lean`);
  - the codec-vectors table;
  - the hand-versioned labels `lang/package/5` and `lang/package-version/5` (`Lang/Package.lean:798,817`).

  CODEC-28 explains the detector, but CODEC-5 still reads "Status: open" with the old claim.
- CODEC-3 (l.55-68): "Bounds live in the value types". The kernel codecs are the Raw family
  (`Codec/Raw.lean:1-13`), whose bounds are domain predicates outside the types (CODEC-12). CODEC-3
  is not marked superseded.
- CODEC-22 (l.481-484): "under refine `kernel/carried/v1`". The code is `refine "kernel/carried"`
  (`Codec/World.lean:378`).
- CODEC-36 (l.438-449): labels `lang/package`, `lang/package/2`. Today they are `/5`.
- CODEC-11 (l.229) and CODEC-18 (l.389) still read "Status: open (owed …)" for work CODEC-18 and
  CODEC-23 record as built (l.658).
- Severity DEBT: a reader of the decisions file gets the wrong layout rules.

**D-4. Comments that misdescribe the code under them.**
- `Codec/Kernel.lean:25-26`: "`Unsigned`: member ‖ key ‖ notBefore ‖ validUntil ‖ pins ‖ maxCharge ‖
  body". The codec (`:311-318`) writes `world ‖ member ‖ … ‖ body ‖ rowPins ‖ ranges`. Three fields
  are missing, including the first (`world`, KERNEL-24). Line 15, "every count a u32", is also false
  for the rows varints described two lines below.
- `Codec/Stream.lean:9`: "canonicity (`Codec.Stream.Lawful`, in `Codec.StreamLaws`)". No such module
  exists (MEASURED: `git ls-files | grep -i StreamLaws` is empty). It is `Codec.Proofs.Stream`.
- `Codec/Stream.lean:16-17`: "Lengths and counts are `u32` and every variable-size value carries its
  bound in its type". False for `varint`, `bytesV`, `bytes8` and the Raw family.
- `Codec/Tag.lean:9-10`: "Nobody edits a version literal, no census lists the tags, and no
  fingerprint is pinned." The same docstring then cites the census and the vectors. The first
  sentence is the CODEC-5 text that D-3 shows is false.
- `Codec/Refusal.lean:17`: `badTag` is "A sum or option tag byte other than 0 or 1". It is also
  `oneOf`'s, `tagged`'s and `choice`'s refusal (`Stream.lean:291,330`), with tags up to 255.
- `Lang/Wire.lean:11-14,265`: `termWire` ("has a tree that reads back to it") does not bound a
  `.bytes`/`.digest` literal's payload by `nodeMax` (`:272`). `packageWire = true` therefore does not
  imply a tree in bounds. `encodePackage` re-checks `fits` (`Lang/Package.lean:819-822`), so behaviour
  is right and the comment over-claims.

**D-5. Six copies of one hex digit (law 1).**
- `Codec/Digest.lean:47-49`
- `Emit/Vectors.lean:815-817`
- `Emit/Rust.lean:393`
- `Kernel/Value.lean:22`
- `Lang/Print.lean:81`
- `Protocol/Command/Text.lean:13-19`

The same `if n < 10 then 48 + n else 87 + n`. `Text.toHex` has the size theorem
(`toHex_utf8ByteSize`); the other five do not and could drift (uppercase in one, say). READ.

**D-6. A tooth named for a regression it cannot see.** `Codec/Proofs/Raw.lean:577-609`.
- The section says `rawList`/`array` reserve `min n (b.size - j)`, because a 2^32-count claim once
  asked for about 32 GB, and that "Each tooth" guards it.
- The teeth are `decide +kernel` over `decode`. The kernel ignores `Array.emptyWithCapacity`'s
  argument.
- **Mutation:** `Array.emptyWithCapacity n.toNat` in `Codec/Raw.lean:100` and `Codec/Stream.lean:259`.
  All four theorems stay green, and the OOM returns. INFERRED (the kernel model has no capacity).
- What the teeth prove (refused at the first missing element) is true and useful. Their heading
  claims a guard against the reservation, which nothing provides; that needs a compiled run under a
  memory limit.

**D-7. Twin codecs for one wire shape (law 1, low).**
- `bytesOf`/`rawBytes`, `array`/`rawList`, `u32`/`nat32` and `u64`/`nat64` share a `Shape` and write
  identical bytes, with separate definitions and separate lawfulness proofs (`Codec/Stream.lean:171`
  vs `Codec/Raw.lean:76`; `Stream.lean:249` vs `Raw.lean:90`).
- `nat16` writes a branching bit little-endian on the wire, while the node hash commits it big-endian
  (`Codec/World.lean:94-99`, which says so): two spellings of one number.
- `rangeRead` keeps `nat8`/`bytes8` for the relation and prefix (`Codec/Kernel.lean:188-190`), while
  `rowKey` and `rangePinWire` use `varint`/`bytesV` for the same fields (CODEC-40 records why).

READ.

**D-8. Package labels are hand literals beside an interpolated check.**
- `packageCodec_label` (`Lang/Proofs/Wire.lean:809-810`) ties only `packageCodec`'s label to
  `packageWireVersion`.
- These are literal `"…/5"`, and no theorem ties them to the version byte:
  - `packageVersion`'s `"lang/package-version/5"` (`Lang/Package.lean:798`);
  - `decodePackage`'s `"lang/package/5"` (`:836`);
  - every theorem that states them (`:842-862`).
- **Mutation:** bump the version to 6 and fix only `packageCodec`'s label. The vectors gate reds the
  `lang/package-version/5` site (row `[5]` turns from read to refused under an unchanged tag), so this
  is caught, but only by the table, not by a theorem. INFERRED (not built).

**D-9. `argvSize` is a second size computation.**
- `Protocol/Command/Verb.lean:234` defines `4 + Σ(4 + len)` and is what `parse` refuses by
  (`argvPastBound`) and what `receipt_argv_fits` bounds.
- What the wire refuses by is `(Layout.codec argvBytesMax commandLayout).size` under `within`
  (`Protocol/Frames.lean:24-27`).
- The two agree today (`array (bytesOf)` size), INFERRED, but no theorem equates them. A change to
  `commandLayout` would leave PROTOCOL-68's fit theorem proving a bound on a number the frame no
  longer uses.

**D-10. Refusal arms that cannot be reached.**
- `Codec/Stream.lean:261` (`array`: `if h : a.size ≤ max … else pastBound`, after reading exactly
  `n ≤ max` elements).
- `Codec/Tree.lean:69,76` (`getD`: `cs.size ≤ max … else pastBound`, after reading `m ≤ max` kids).
- They exist to build the subtype proof. Each looks like a live refusal of a separate condition and
  never fires. Low. READ.

**D-11. `Codec/Kernel.lean` decision trail for the 13 call kinds.**
- `BodyF : Fin 13` and `choice 13` hard-code the ceiling (`gates/ceilings.tsv:5` "call kinds 13").
- A 14th Body constructor fails the `back` match, so it does not build silently: good.
- The vectors cover all 13 (`each 13 Vectors.body`, `Emit/Vectors.lean:733`).
- No finding beyond noting that `13` appears three times by hand (BodyF, bodyWire, choice) instead of
  once. Low.

---

## What I checked and found right (so the next reader need not)

- `Stream.option`, `sum`, `oneOf`, `tagged` and `choice` all refuse unknown tags `badTag` at the tag's
  offset. `choice_lawfulOn` takes `n ≤ 256` (`Codec/Proofs/Raw.lean:433`). `dataStream_lawful` takes
  `tyWire`, which bounds arms by `rowMax = 256`. `dataStream` is called only behind `dataTy`
  (MEASURED grep: only `Emit/Vectors.lean:808`, on a fixed wf type).
- Varint canonicity:
  - overlong refused (`Codec/Varint.lean:33`);
  - a value past the limit refused (`:36`);
  - width exhaustion refused (`:28`);
  - the tenth byte of `varint64` refused at 2 or more (vectors `Emit/Vectors.lean:614-620`).
- `Tag.of_eq` (`Codec/Proofs/Tag.lean:234-241`): its collision disjunct is over the two given
  messages, not chosen ones, and each disjunct is unprovable alone. Not vacuous.
- `refine_accept_iff` (`Codec/Proofs/Refine.lean:26-29`) does pin `accept`. `slot_relabel_unseen`
  (`RefineTooth.lean:86-98`) honestly proves the residue that only the vectors see.
- `Emit/Vectors.lean` `write` keeps same-tag rows verbatim (`:861-865`). `gates/vectors.py:36-58`
  refuses a same-tag row edited, added or removed against the parent. Laundering a relabel needs a
  rename, which is the intended announcement.
- The emitted `Command` total check sits at the same point with the same refusal as Lean's `within`
  (offset 0, limit, got = consumed): `client/src/generated.rs:436-443` against
  `Codec/Stream.lean:302`. READ.
- Ed25519 `verify` refuses S ≥ L, y ≥ p, and x = 0 with sign 1 (`Codec/Ed25519.lean:203-224`). READ.
- `World` decode rebuilds every trie from its listing and refuses any listing that is not the rebuilt
  trie's own (`listingAccept`, `Codec/World.lean:83-86`). No node hash is read from the wire.

---

## Files NOT read (or read only for statements), with sizes

Not read:

| file | lines |
|---|---|
| Codec/Proofs/WorldTooth.lean | 926 |
| Codec/Proofs/World.lean | 916 (grepped `CodecFits` only) |
| Codec/Proofs/Prime.lean | 514 |
| Codec/Proofs/Field.lean | 496 |
| Codec/Proofs/Group.lean | 394 |
| Codec/Proofs/WorldSize.lean | 380 |
| Codec/Proofs/Rows.lean | 375 |
| Codec/Proofs/TrieOrder.lean | 358 |
| Codec/Proofs/Ed25519/Decode.lean | 354 |
| Codec/Proofs/Curve.lean | 353 |
| Codec/Proofs/TrieOrderDeployed.lean | 294 |
| Codec/Proofs/Ladder.lean | 250 |
| Codec/Hash.lean | 248 |
| Codec/Proofs/RowOrder.lean | 247 |
| Codec/Proofs/SlotOrder.lean | 245 |
| Codec/Proofs/Complete.lean | 234 |
| Codec/Proofs/Ed25519/Sign.lean | 220 |
| Codec/Proofs/Carried.lean | 208 |
| Codec/Proofs/Path.lean | 188 |
| Codec/Proofs/TrieProof.lean | 185 |
| Codec/Proofs/PrimeL.lean | 157 |
| Codec/Proofs/Ed25519/Test2.lean | 117 |
| Codec/Proofs/Order.lean | 110 |
| Codec/Proofs/Ed25519/Bytes.lean | 101 |
| Codec/Sha512.lean | 96 (header only) |
| Codec/Proofs/Layout.lean | 89 |
| Codec/Proofs/Ed25519Stage.lean | 61 |
| Codec/Proofs/Ed25519/Tampered.lean | 55 |
| Codec/Proofs/Ed25519/Order.lean | 48 |

Read only in part or for statements:

| file | lines | read |
|---|---|---|
| Codec/Proofs/Stream.lean | 803 | l.1-140 |
| Codec/Proofs/Raw.lean | 610 | l.1-66, 285-340, 570-610, theorem list |
| Codec/Proofs/Kernel.lean | 464 | l.1-80, 250-464 |
| Codec/Proofs/Tag.lean | 243 | statements |
| Codec/Proofs/Varint.lean | 242 | statements |
| Codec/Proofs/Tree.lean | 216 | statements |
| Codec/Proofs/RowsReached.lean | 174 | statements |
| Codec/Proofs/ListingPin.lean | 149 | header and statements |
| Codec/Ed25519.lean | 272 | l.1-60, 183-240 |
| Lang/Proofs/Wire.lean | 1024 | l.800-930 and theorem list |
| Lang/Package.lean | 839 | l.680-839 |

Not built: nothing in the tree. My one compile was the scratch `Esc.lean` above (toolchain v4.30.0,
`lean -c` + `leanc`, under my scratchpad).
