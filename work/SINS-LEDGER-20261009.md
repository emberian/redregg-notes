# SINS LEDGER — the Mini software's structural sins, derived from code (2026-10-09)

Scout: SINS-LEDGER (Claude). Repo `/Users/ember/workbox/mini-unified-push-20261003` at `origin/main = 1c7e46da`. This is the software half of the retro (the process half is `RETRO-20261008.md`).
It is a diagnosis, not a plan. Tags: **READ** (path:line at 1c7e46da) · **MEASURED** (number + source) · **INFERRED**.
Paths without a prefix are repo-relative. `H` = one pure-Lean cSHAKE256 node hash (no `@[extern]`,
READ `Theory/Sp800185Cshake256Fast.lean:28`).

## 0. Top five

1. **The executable state is a closure chain over `List`s.** Every lookup after `k` installs walks `k` closures, and
   `history` grows by list snoc. `atPrefix` (56.6 min at 30k) and the SURPASS 10³→10⁴ blow-up both come from this.
2. **The world root is an uncompressed 256-level tree that no process keeps.** Every cold open evaluates it in full
   twice, Θ(cells·256·H). Every client CLI step is a fresh Host process, so it pays that cost again. The kern-grow patch
   fixes only a session refresh, so client time stays 22 s at 1000 cells.
3. **Persisted shapes are 738 hand-numbered string labels plus a hand-maintained epoch.** 177 of those labels were bumped
   since 10-01, 53 are written by hand in both Lean and Rust, and the derived epoch (`PersistedCodecTags`) is not on main.
4. **The log and the checkpoint hold whole post images.** The log entry is not the Turn, so 11 facts have two homes
   each (FD-1). The admission inductive has grown from 33 to 51 constructors.
5. **Gates pin change, not meaning.** The ledger has 94,514 lines (90,520 of them "redefined"), against 41,177 pinned
   rows. 6 of 7 regenerated fixtures have no authority. The growth row measures updates, while the bar fails on creates.

## 1. Data structures on the hot path

**D1. The snapshot is functions, not a map.** READ `Kernel/DurableCommitProtocol.lean:150-160`. `install` sets
`roots := fun c => (lookupPost c writes).getD (before.roots c)`. `consumed` and `available` are built the same way.
`history := before.history ++ [event]` (`:159`) is an O(h) snoc. READ `Kernel/DurableDataIntent.lean:240-244`:
`canonicalBytes` is a closure layered the same way.
- **Asymptotics:** a root or bytes lookup after `k` installs costs Θ(k). A fold over `h` records costs Θ(h²) from the
  history snoc alone.
- **What bounds it:** only the full path's rebase at `baseHeight + 2·checkpointEvery`
  (READ `Compiler/DurableReceiverIO.lean:403`). INFERRED: the light `Opening` advances by `install` with no flattening
  until the next process starts.
- **Measured:** SURPASS reports, for the `DFinsupp.update` model twin, 10³ turns in 84 ms and 10⁴ in 8.3 s
  (MEASURED `b2.md:57-59`, quoted at SURPASS §2b item 4). The deployed `Snapshot.install` has the same shape (READ).
- **Right structure:** a persistent ordered or hash map for `roots`, `bytes`, `spent` and `allowance`, and a
  height-indexed `Array` for history. Prove it equal to the spec by `@[csimp]`, not `implemented_by` (SURPASS item 4).
**D2. The checkpoint's materialized table is a linear list.** READ `Kernel/DurableCheckpoint.lean:65-69` stores
`cells : List (CellId × List UInt8)`. READ `:76-85,108-111` define `rootTable` and `tableLookup`, a linear scan, and
`roots c := tableLookup c table`.
- `entriesOf` over all cells (READ `Compiler/DurableReceiverCore.lean:474-477`) is Θ(cells²) comparisons on every open.
- `rootTable` rehashes every cell's full bytes on every open: Θ(total state bytes·H).
- **Right structure:** a map keyed by `CellId`, with the per-cell root stored beside the bytes in the checkpoint
  (it is MAC-covered already).
**D3. The world-root tree is uncompressed, 256 levels deep.**
- READ `Kernel/WorldRootCache.lean:39-75`: `Tree = empty | leaf | node digest l r`. A leaf sits only at height 0, and
  `set` recurses along a `List Bool` path of length `depth`.
- READ `Kernel/WorldRoot.lean:630-642`: `deployedIx` is the 256 bits of cSHAKE(key), and `depth := 256`.
- READ `Kernel/WorldRootCache.lean:241-242`: `ofEntries` is `foldl insertWrite`.
- **Asymptotics:** each insert costs 256·H, whatever the tree size. The patch's own theorem says so
  (`insertWrite_nodeHashes`, READ patch `WorldRootCache.lean` hunk). A full build costs Θ(cells·256·H). With 1000
  random keys, only about the top 10 levels are shared.
- **Measured:** the uncached evaluation took 0.5 s for 10 slots (MEASURED `Kernel/WorldRootCache.lean:7`, C1).
  INFERRED: H is roughly 0.2 ms.
- **Right structure:** a compressed sparse Merkle tree (a leaf at its shortest unique prefix, the empty-subtree table
  for the rest; Jellyfish/Patricia style). That is about log₂(n) ≈ 10 hashes per insert instead of 256.
- It changes the root, so it needs a re-genesis, which is cheap.
**D4. `RootCache` drags its proof carrier at runtime.** READ `Compiler/DurableReceiverCore.lean:448-461`. The
cache holds `entries : List (Key × Digest)`, which is "the slot writes since the tree was built". Every `write` does
`entries ++ [(key,value)]`: a Θ(len) copy, and the list grows without bound.
- `injectiveCheck` (READ `:509-512`) walks every entry with a 256-step `find`.
- The list exists so that `Good … (slotsOf … entries)` can be stated (READ `:452-454`).
- **Right structure:** state the invariant over the abstract map (erased/ghost) and drop the runtime list.
**D5. `extendVerified` rebuilds the whole root on every extension.** READ `Compiler/DurableServed.lean:683-688`.
Each extension computes:
- `Served.entriesOf` over every cell: Θ(cells);
- `RootCache.ofEntries`: Θ(cells·256·H);
- `RootsExact.ofEntries`, whose `injectiveCheck` is Θ(cells·256) (READ `DurableReceiverCore.lean:561-562`);
- `extendIds`, which is `(ids ++ writes).eraseDups` (READ `DurableServed.lean:63-64`): Θ((cells+writes)²) comparisons.

On a cold open, `openSealed` first recomputes the checkpoint's whole root (READ `Compiler/DurableCheckpointCodec.lean:603-608`,
`worldRoot` at `:538-539` = `deployedRoot (stateEntries …)`). So **two full root evaluations happen per cold open.**

*The unmerged patch* (`kern-briefs/kern-grow-WIP-20261009.patch`, READ) adds `Start.roots : Option CachedRoots` and,
when it is `some`, advances the cache by `suffixSlots` with `RootsExact.advance`. Only `Opening.extend` passes
`some` (patch hunk at `:889`). `openHead` passes `none` (hunk at `:868`). **What it leaves:**
- (a) every cold open still pays 2·Θ(cells·256·H): `openSealed` plus `ofEntries`;
- (b) `entries` is still built as a value for the `else deployedRoot entries` fallback and the `RootsExact` index
  (INFERRED: Lean's strict `let` evaluates it unless the compiler floats it into the branch);
- (c) `extendIds` `eraseDups` is untouched;
- (d) D4's `entries ++` snoc now runs per written slot.

MEASURED (DEPUTY-KERNEL-FINAL:22, paired at 1000 cells): total 44.5→36.7 s, host 21.8→15.0 s, client 22 s unchanged.
The term left is **Θ(cells·256·H) per cold open** (INFERRED).
**D6. The client is a cold open per CLI step.** READ `native/resource-client/src/main.rs:1173-1191`: with no socket,
`process` → `local_process` spawns a fresh Host binary. READ `Kernel/NativeHostLight.lean:38-39`: each such Host
calls `NativeHostLight.start` → `DurableServed.openHead`, which is D5 with `roots := none`. READ `Host/Main.lean:8078-8081`:
`dry-run` additionally runs `NativeHost.openExisting`, i.e. `DurableReceiverIO.load`, the full replay
(READ `Kernel/NativeHost.lean:40-43`).
- **So:** one `workspace --action create` spawns ≥3 Hosts (`lookup`, `dry-run`, `submit`; READ `workspace.rs:4008,4086`
  `retry(…,"lookup")`). Each rebuilds the root twice, and the dry-run also fully loads. INFERRED: this is the
  unchanged 22 s client term.
- **Right structure:** one long-lived process holding the `Opening` (the `SOCKET` path exists), or a persisted tree
  (C2). Either one removes the term. The tree change of D3 shrinks it by about 25×.
**D7. `atPrefix` is a genesis replay per historical read.** READ `Compiler/DurableReceiverCore.lean:1307-1312`: below
the checkpoint, it resumes from `State.ofSeed` over `accepted.take height`. READ `Kernel/NativeObservationController.lean:1310-1320`:
one `at height` read is one such replay.
- **Cost:** with D1's history snoc, Θ(h²) per read. MEASURED 56.6 min at 30k (RETRO:312).
- **The replacement is already named in-tree:** `Reader.stateAt` = checkpoint + ≤63 records
  (READ `Compiler/DurableHistoryReader.lean:20`). It needs every 64th checkpoint retained, not just the latest.
**D8. Bytes are linked lists.** MEASURED (`git grep -c`, `Kernel Compiler Host`): `List UInt8` appears 4,659 times,
`ByteArray` 328 times.
- READ: `Entry.record`/`Entry.tag` (`Compiler/DurableReceiverCore.lean:59-62`) and `DataWrite.canonicalPostBytes`
  (`Kernel/DurableDataIntent.lean:71-76`) are lists. The index is `Std.HashMap (List Bool) Row`
  (READ `Compiler/DurableServed.lean:611`), keyed by 256-cell lists.
- INFERRED: about 16–32× memory per byte, and a pointer chase per byte absorbed by every hash.
- **Right structure:** `ByteArray`/`Subarray` at runtime, with `List` only in specs and a `@[csimp]` bridge.
**D9. Checkpoint and tail boundaries do whole-state work inside a write.**
- READ `Compiler/DurableServed.lean:917-923`: at `height % checkpointEvery == 0` (default 64, READ
  `DurableReceiverCore.lean:141`), the write seals `checkpointState`, i.e. every cell's full bytes
  (`:856-857` → `State` with `cells` in full). Sealing re-derives the full root (`sealAt`).
- READ `DurableReceiverIO.lean:403`: the full path rebases at base+2·64.
- The tail bound `L = 256` (READ `Host/ApplicationBirthAuthoringCheck.lean:44`; `Compiler/RefusalReason.lean:85-88,133`)
  refuses every non-certify write past certified+L.
- **Cost:** each 64th write pays Θ(state bytes + cells·256·H). INFERRED: this is the G row's p99 (2.2 s at 1000
  updates) against its median.
- **Right structure:** incremental checkpoints (only cells dirtied since the last one, plus persisted tree nodes),
  Θ(dirty·log n).

## 2. Encodings ("informatics")

**E1. Count (MEASURED, `git grep` at 1c7e46da).**
- Labels: 738 distinct `"DREGG…/vN"` labels in Lean (664 base names); 88 in Rust; **53 hand-written in both**.
  The version histogram is v1:498, v2:119, v3:47, v4:36, v5:12, v6:10, … up to v16.
- Codecs: 1,471 `def *Frame/*Codec/*Stream :` declarations in 307 Lean files, `StreamCodec` in 510 files, and 115
  Rust `fn encode*/decode*` in 48 files.
- Churn since 10-01: **159 of 1,377 main commits touch a versioned label**, and **177 base names were bumped** (an old
  version removed and a new one added in the same period; `git log -G'/v[0-9]+"' -p`).
**E2. Global counters.**
- READ `Compiler/DurableCheckpointCodec.lean:156-159`: `StoreEpoch.current` is five hand strings,
  `"state-key/tagged-v4"`, `"schema-refs/v6"`, `logTagLabel` (`"…LOG-TAG/v4"`, `:129`),
  `"history/mmr-v1;index/trie-v1;checkpoint/v4"` and `"commands/v2"`.
- READ `Kernel/ConsentAnchor.lean:274-292`: the tripwires `storeEpoch_stateKey/_schemaRefs/_commands` fail the build
  when a component moves without the string. That is a hand cross-reference, and two lanes collide on it.
- Commits since 10-01 (`-S`, MEASURED): `StoreEpoch` 12, `ConsentAnchor` 9, `schema-refs` 7. RETRO:302 says 4 of 5
  ejections were two lanes taking the same counter.
- `PersistedCodecTags` (the derived StoreEpoch) is **0 files on main**. It lives on the unlanded prod train 001b9a2c
  (READ DEPUTY-KERNEL-FINAL:15-16).
**E3. Θ(2ⁿ) and unary encoders.**
- **The two that were fixed:** `ObjectiveActivityReceiver`'s `Nat.pair` (absent on main: MEASURED, no hit), and
  `TurnOfIntent.bytesCode`, now base-256 positional and linear (READ `Kernel/TurnOfIntent.lean:479-486`).
- **Still present: unary `encodeNat v := List.replicate v 0 ++ [1]`.**
  - READ `Kernel/QuotaGcSettlement.lean:226`, used by `Grant.canonicalBytes` (`:360-366`) on
    `commandDigest.value` (a digest: 2²⁵⁶ bytes) and on `chargeCode` (a 10-deep `Nat.pair`, READ
    `Kernel/AuthorizedResourceCharge.lean:61-66`, whose bit length is ~2¹⁰× the largest lane's).
  - The same encoder appears in `Kernel/CanonicalEscrowMarket.lean:182-186` (`stateBytes`) and
    `Compiler/Tower256CshakeMerkleController.lean:44`.
  - A choice-based codec: `noncomputable countableCodec` (READ `Compiler/Ext6GateProofDeployment.lean:66-70`, "not a
    native executability claim").
- **Reachability:** `QuotaGcSettlement` is imported only by `Assurance/QuotaGcSettlementWitness.lean` and the umbrella.
  `CanonicalEscrowMarket` is imported by Assurance and `PrivateEscrowSettlement` (READ import grep). So none of these
  is on the Host path today (INFERRED).
- **The sin:** a declaration *named* `canonicalBytes` whose execution cannot terminate, waiting for the first lane that
  routes it.
- **Other `Nat.pair` on hashed keys:** `ProviderExecutionLease.lean:122,412` (two digest-sized operands, bounded) and
  `CredentialAuthorityEntryCodec.lean:211` (one pair). These are bounded, not exponential.
- **Lint that would catch it:** forbid `Nat.pair` and unary encoders in any `canonicalBytes`/`Codec` (a lint),
  and require every persisted codec to carry a length-linearity theorem.
**E4. What "derive persisted shapes from one source" would mean concretely (INFERRED design; options, not a plan).**
- (a) **The Turn is the only persisted log entry.** The checkpoint is the World. This is SURPASS §2b items 1, 5 and 6:
  `DREGG.DURABLE.LOG` v2→v3; `canonicalPostBytes`, `ReplayEnvelope` and `Snapshot.history` are deleted.
- (b) **Schema-first codecs.** One `StreamCodec` per persisted type, produced by a deriving handler from the Lean
  type. Its tag is **H(structural descriptor)**, content-addressed and not a counter. `StoreEpoch` = H(the sorted
  descriptor hashes); `PersistedCodecTags` is the start of this. Two lanes changing different types then never touch
  the same number, and a lane changing one type changes its tag automatically.
- (c) **Rust codecs are generated from the same descriptors.** The precedent is `NativeGlueGen` emitting
  `prover/generated/*.rs` (READ `Compiler.lean:100`). That deletes the 53 dual-homed labels and the T1–T3 twins.

Of FD-1's eleven two-home facts (SURPASS 318-460), (a) collapses **log entry, state, replay index, spent markers,
charge, the root and the clock** (7). Parentage and the presence index follow once `World` is the state (2). (b) and (c)
collapse no FD-1 fact directly. They collapse the codec/label class (E1, E2) and the Lean↔Rust frame twins.

## 3. Caching

**C1. The Lake cache was shared and writable, not content-addressed.** MEASURED 675 poisoned entries across 18 lane trees
(RETRO:146). On burst2-b, 79 `.c` files had an unprefixed `initialize_` (DEPUTY-KERNEL-STATUS-20261006:116).
`cp -al` hard-linked 444 `.ilean`, and in-place writers fail on them (DEPUTY-KERNEL-FINAL ops notes; memory
`reference-cp-al-clones-share-source-inodes`).
- **Fix shape:** key on every compile input (toolchain, options, module prefix) and write once, by one owner. Lanes
  read only.
**C2. The root is derived twice and cached never** (D5/D6).
- The checkpoint carries body + root + MAC (READ `DurableCheckpointCodec.lean:541-544`) but no tree nodes.
- The MAC already binds the root, yet `openSealed` recomputes it (`:607`). Then `extendVerified` rebuilds the tree.
- **Should be cached:** the tree's node digests, persisted (the MAC covers their root), or held by a long-lived process.
**C3. Post images are stored where patches would derive them.**
- READ `Kernel/DurableDataIntent.lean:71-76`: every log record carries each written cell's **whole** canonical post
  bytes.
- READ `Kernel/DurableCheckpoint.lean:65-69`: every checkpoint carries every cell's full bytes.
- So a one-field write to a large cell (e.g. the authority cell; `Host/Main.lean:1035` prints its size) re-logs the
  whole cell.
- **Cached that should be derived:** post images (derived from pre + patch, FD-1 item 1).
- **Derived that should be cached:**
  - `Image.cellIds`, an `eraseDups` over all history per load (READ `Kernel/DurableReceiver.lean:183-185`);
  - per-cell roots (`rootTable` rehash, D2);
  - the tree (C2).
**C4. Installed tool copies are a cache with no invalidation.** Box copies of runner, gate, hub and mk-lane diverged
from the tree ≥4 times (MEASURED RETRO:314). `--from main` resolved to a lagging warm base (RETRO:141).

## 4. Twins still present (one line each)

- **T1. Rust store-root twin.** `native/resource-client/src/hiding.rs:1-9,56-57,118` has a hand SP 800-185
  KMAC256/cSHAKE plus `DREGG.STORE.LEAF/v1` and `ROOT/v2`, beside `Compiler/Sp800185Kmac256.lean` (READ).
- **T2. 53 labels in both languages.** 21 in `native/spk-host`, 11 in `resource-client`, 1 in `mini-sdk`, 1 in the
  credential verifier. `NATIVE-HOST/OUTCOME/v5` alone is in 8 spk-host files (MEASURED).
- **T3. The Lean↔Rust boundary is process frames.** There are 16 `@[export]` in Host/Kernel/Compiler (5 files,
  MEASURED), so by the census-from-the-Lean-side heuristic every frame Rust consumes is a second codec.
- **T4. Versioned admission.** `NativeAdmission` has **51** constructors (READ `Kernel/NativeHostReplay.lean:976-1215`):
  `applicationLifecycleBegin`/`V2`/`V3` plus `RetryBeginV4`, Claim ×4, Completion ×3, `payEnrol`/`V2`, `fnEmptyPollV2`.
  It had 33 at 175e1114 (SURPASS). There are 66 `Kernel/ApplicationLifecycle*` modules and 12 spk-host
  `lifecycle_v3/v4_*.rs`.
- **T5. SPK v4 retry vs OB rebirth.** `RetryHistory` (`NativeHostReplay.lean:725`), `BeginAtV4`/`ClaimAtV4`/`CompletionAtV4`
  (`:650-706`) and `lifecycle_v4_retry_*.rs`, versus OB's "retry is a new birth after the old activity ended"
  (OB-WORLD §8.3). §8.3 deletes the v4 path.
- **T6. Two upgrade paths.** `ApplicationGrain` `beginUpgrade/claimUpgrade/completeUpgrade` (READ `Kernel/ApplicationGrain.lean:372,394`;
  8 files) versus OB `adopt`/`migrate` (`ObjectiveUpgradeInvariant`; 9 files, MEASURED).
- **T7. Two authority vocabularies.** SPK's 4-field grain machine plus installed `Pred` policies plus Linux
  "capabilities", versus OB grants and laws (READ via OB-WORLD §8 opening, `ApplicationGrain.lean:36-41,110-160`).
- **T8. Two state homes.** App persistent `/var` (`native/spk-host/src/materialize.rs:121,367,472`; `/var/lib/mini`,
  `grain-runtime/src/credentials.rs:42`) versus cells.
- **T9. Two Hermes drivers.** A scripted ACP stand-in (`native/grain-runtime/fixture/hermes-deterministic-acp`, python
  "whose model is a script") and `native/hermes-test-provider` (a deterministic OpenAI endpoint), versus live Hermes ACP
  plus `deploy/hermes-dispatch/mini-hermes-dispatch.py`. The journeys exercise the scripted pair.
- **T10. Two layers beside World.** OB's invariant `Step` over `DataSnapshot` (`Kernel/ObjectiveCheckpointInvariant.lean:1683-1697`,
  per OB-WORLD §0) and the judgment layer. `CheckedCommit` (the join) is not on main (RETRO:309-311).
- **T11. Two cost models.** `RootCache` keeps both the tree and a replayable `entries` list (D4). `deployedRoot` (the
  sparse evaluation) is kept as the fallback beside the cache (READ `DurableServed.lean:687`).

## 5. Gates whose meaning is not central

**G1. The manifest ratchet measures closure-hash change.**
- MEASURED: 596 `scripts/gates/objective-manifest/*.tsv` with 41,177 pinned rows. The ledger
  `objective-contract-changes.txt` has 94,514 lines: **90,520 `redefined`**, 3,341 `restated`, 609 `removed`,
  1 `axioms`. 22 ledger commits landed since 10-01.
- **What "redefined" means mechanically** (READ `scripts/objective-manifest.py:26-31`): statement hash unchanged and
  the *transitive closure* hash changed. Any edit to a shared codec therefore redefines every downstream declaration.
- **What admission is:** a ledger line `name, old, new, kind, commit, reason`. The top reasons are attributions:
  "root change: … collector now follows" ×14,567, "redefined: Kernel.ObjectiveActivityCell changed by 487b54fb" ×5,722,
  "…ClockCell changed by 93e18aac" ×4,926.
- **The meaning-bearing classes are `restated` and `removed`** (3,950 lines). The other 96% records *who* changed a
  dependency.
**G2. Fixtures are re-emitted by the implementation they check.**
- READ `scripts/kern/regenerate-native-fixture.sh:1-22`: it copies the current release binaries, runs the acceptance
  driver, and regenerates `Assurance/NativeAcceptedFixtureData.lean`.
- READ `scripts/pipeline/fixture-authorities.txt`: **7 regenerated artifacts, 1 `checked`, 6 `PENDING`** (MEASURED).
- MEASURED: 168 of 1,377 commits since 10-01 have fixture, re-pin, ledger or re-emit in the subject. Main waited
  77–83 min on fixtures three times (RETRO:81).
**G3. The growth row measures the wrong axis.**
- READ `docs/JOURNEY.md:64-72`: G times one signed write and one read at 10/100/500/1000 *accepted records*, with a
  bar of 5 s per write at 1000 records.
- MEASURED: updates to existing cells reach p99 2.2 s (green). Creates are linear in **cell count**: 24.3 s at 250
  cells (kern-grow brief) and 36.7 s at 1000 cells after the patch (DEPUTY-KERNEL-FINAL:22). That is 7× over the bar,
  and no row is red.
- **Right shape:** G parameterized over (cells, records, cell size), with creates as a row.
**G4. Verdicts depend on who ran the gate.** UNCONFIGURED rows counted as neutral, and the row count fell from 102 to
48–60 (RETRO:106). scripts-elab depends on row order. 214 mutants change no verdict (RETRO:316-318). No single place
defines what a row means.

## 6. Ranked table

| # | sin | cost class | blast radius | what replaces it | size (modules, INFERRED) |
|---|---|---|---|---|---|
| 1 | D3+D5+D6+C2: full 256-level root rebuilt twice per cold open, every CLI process | Θ(cells·256·H) per process; THE BAR (creates) | every write, every client call | compressed SMT + persisted nodes or a long-lived Opening; drop the double eval in `openSealed` | 3–5 (WorldRootCache, DurableReceiverCore root section, DurableServed, DurableCheckpointCodec, client socket default) + re-genesis |
| 2 | D1+D7: closure-chain snapshot, list-snoc history, genesis replay per `at` | Θ(k) per lookup, Θ(h²) per fold/read | long sessions, history reads, audit | ordered map + `@[csimp]`; `Array` history; retained 64-checkpoints → `Reader.stateAt` | 3–4 (DurableCommitProtocol, DurableDataIntent, DurableCheckpoint, DurableHistoryReader) |
| 3 | G3: growth row measures updates, the bar fails on creates | gate meaning | every perf claim | G over (cells, records, size), creates included | 1 script + JOURNEY.md |
| 4 | E1+E2: 738 hand-numbered labels, a hand StoreEpoch, ConsentAnchor tripwires | merge contention (4/5 ejections); 177 bumps in 8 days | every persisted shape, every lane | content-addressed tags from structural descriptors; derived epoch (land PersistedCodecTags, then generalize) | 1 generator + touch ~300 codec files mechanically |
| 5 | C3 + FD-1: log/checkpoint hold whole post images; 11 facts in two homes | Θ(cell size) per write; double maintenance | kernel, OB, SPK, audit | Turn log + World checkpoint (SURPASS stages 0–2) | ~50 (B2's count: 35 DataIntent, 37 canonicalPostBytes, 50 install/lookupRecorded) |
| 6 | G1+G2: closure-hash ledger (90,520 redefined), self-regenerated fixtures | a third of commits are bookkeeping; admission by attribution | all lanes' throughput | pin statements and contracts (restated/removed), with named semantic theorems for value-bearing defs; fixtures from an independent authority | 2 scripts + ledger reset |
| 7 | T4+T5+T6: 51 admission constructors with V2/V3/V4 versions; two upgrade paths | Θ(versions) proof and replay surface | SPK, replay walk | OB birth/adopt/migrate; delete v1–v4 lifecycle (OB-WORLD §8.3) | delete ~66 ApplicationLifecycle* + 12 rs; add ≤10 (OB §8.5) |
| 8 | T1–T3: Lean↔Rust frame twins (53 labels, hiding.rs KMAC/root) | divergence risk | client, spk-host | generated Rust codecs (E4c) or `@[export]` | 1 generator; delete hand codecs in ~48 rs files |
| 9 | D8: `List UInt8` everywhere (4,659 vs 328) | constant factor 16–32× memory, every hash | everything | `ByteArray` runtime + `@[csimp]` | broad, mechanical |
| 10 | D9: whole-state checkpoint inside the 64th write | p99 spikes | writes | incremental (dirty-cell) checkpoint with persisted nodes | 2 |
| 11 | E3: unary/`Nat.pair` "canonicalBytes" off-path | latent Θ(2ⁿ) | the first lane that routes them | lint + linear-size theorem per codec | 3 files + 1 lint |
| 12 | C1/C4: shared writable Lake cache; installed tool copies | poisoned builds, divergent gates | swarm | content-addressed write-once cache; tools run from the tree | infra, 0 Lean |

## 7. Which repairs make the system honest about THE BAR fastest, and which are the rethink

Three repairs make the system honest about THE BAR fastest:
1. **Make G measure what the bar fails on (G3).** Add creates at 1000 cells and parameterize over cell count. It is one
   script, and it turns today's false green into a red that names the real axis.
2. **Stop re-deriving the world root (sin 1).** Evaluate it once per open: trust the MAC'd checkpoint root or check it
   against the rebuilt tree, not both. Make the client hold one Opening instead of spawning a cold Host per step. Then
   replace the 256-level tree with a compressed sparse Merkle tree. These three steps remove the whole Θ(cells·256·H)
   term that the kern-grow patch leaves (client 22 s, host 15 s at 1000 cells).
3. **Replace the closure-chain snapshot with a real map and give history an array (sin 2).** This removes the Θ(h²)
   behind `atPrefix`, closes SURPASS's measured 10³→10⁴ cliff, and puts `Reader.stateAt` in place.

All three change data structures, not semantics, and each has an existing proof obligation to keep (`RootsExact`,
`@[csimp]` equality).
The architectural rethink proper is the rest:
- **The Turn as the only persisted entry and the World as the checkpoint** (FD-1, collapsing 7 to 9 of the eleven
  two-home facts and the whole-post-image log).
- **Persisted shapes derived from one structural source,** with content-addressed tags and generated Rust codecs,
  which removes the counters, the 53 dual-homed labels and the frame twins.
- **Folding SPK's versioned lifecycle and upgrade paths into OB births, adopt and migrate.**
- **Redefining the gate surface around meaning** (statements and named contract theorems) instead of closure-hash
  change admitted by attribution.

These four are one decision. "Derive persisted shapes from one source" only means something once there is one
persisted shape, the Turn. Until then every codec repair is another counter.
