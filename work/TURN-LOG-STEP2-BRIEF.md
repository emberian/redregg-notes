# TURN-LOG STEP 2 brief (from TURN-LOG-4, 10-15): the log entry is the Turn; the ingress lives in an archive

Same SAFETY, tree, build recipe and logging as /Users/ember/dev/redregg/work/TURN-LOG-GUARDS-BRIEF.md (read its SAFETY + WHERE
sections; they apply verbatim). Base: `turn-log` after the GUARDS commit (Turn.pins from the intent, History.cellDigest, Bridge.pin).
Log under "## STEP 2 implementer" in TURN-LOG-LOG.md. Read TURN-LOG-LOG.md's "SCOUT (step-2 surfaces" bullet and "STEP 2 PLAN"
bullet first: they list every decoder of log entries and every reader of record.event.canonicalBytes (file:line at 7877e6e7).

## 0. Carries first (ROOT ruling 10-15, small, its own commit)
Kernel/CarriedSegment.lean:204 `intent` charges `exactCharge := fun _ => 0` (:210) yet writes values; since the charge switch its append
is refused (storage lane ≠ the turn's). Ruling: a carry IS a World turn and is charged its World storage like every other turn
(storage lane := DeployedCharge.storageCharge of its writes/guards/event, i.e. what Turn.ofIntent derives). If a carry must be free for
its sponsor, that is an EXPLICIT allowance credit visible in the same turn, never an uncharged write: first find out whether the carry's
target Store can fund it (its genesis allowance); if it cannot, say so in the log and in the commit, and do NOT add a credit mechanism on
your own — report it as the open question it is. Restate `install_allowance` (:227) to the debit (old/new statement in the commit),
fix CarriedSegmentIO / NeutralCarriedSegmentIO / NeutralPolicyCarry consumers, and run the carry journey row if one exists
(grep scripts/ and docs/JOURNEY.md for "carry"); otherwise a filtered test that exercises a carry append.

## 1. Step 2 proper (one commit, a flag day; say what breaks)
1. ARCHIVE: a new DurableIndex family (Compiler/DurableIndex.lean:184 `namespace Family`: spent 0, transaction 1 → `archive : UInt8 := 2`),
   key = primaryOf archive (event digest bytes), value = the event's `StableEvent.canonicalBytes` (the ingress). Written as NodeWrites
   in the SAME `Transport.append` transaction (Compiler/DurableReceiverCore.lean:104) as the entry, so entry and ingress are atomic.
   Check the Rust/sqlite transport treats space-3 node rows as opaque (no Rust change expected; verify, do not assume).
2. LOG v3: the stored entry's record bytes = `encodeTurnAt w t` (Kernel/DeployedTurnCompact.lean) with the event replaced by its
   digest (the compact event). Bump `durable_log_byte_v2` → v3 in Compiler/PersistedCodecTags.lean:209 (StoreEpoch is derived and moves;
   old Stores refuse by epoch name). With pins carrying the intent's digests, write legs no longer need their own digest guard: drop
   the per-leg digest from the compact leg (olds reconstructed from the held cell; a moved cell is refused by the pin, guardFailed) and
   restate decodeLegAt_other accordingly (the collision argument now sits on the pin).
3. THE CHAIN is the World's: chain over `encodeTurn` of the decoded turn (H.turnDigest), the same value as `World.head`'s chain.
   The Store's chain over IntentRecord bytes (`DurableLogTags.chainPrefixesStored`, `chainPrefixes`) is DELETED, not kept beside.
   The accumulator leaf may keep hashing the stored bytes (they are now the compact turn).
4. DECODE IS WORLD-RELATIVE, so decode + fold are ONE pass: `decodeRecordsFrom` (DurableReceiverCore.lean:1305) + `foldRecords` (:1096)
   become one fold from the genesis/checkpoint World: decode entry at w (archive lookup for the event by digest; a missing archive row
   refuses by name), admit, next. eventBytes for the charge comes from the archived bytes (nothing persisted as a number).
5. `recordsOf`: the IntentRecord reconstructed from (pre-World, Turn, post-World, archived event) so `image.accepted` and the ~95 walker
   files keep compiling. Fields: txId/subject/event from the turn+archive; writes = the leading pins whose cells the turn writes
   (expectedPre = pin, canonicalPostBytes = the post slot's canonical bytes, exactPost = rootBytes of them); readGuards = the remaining
   pins in order with duplicates; nullifiers = inverse of `nullifierCode` (it is a linear stream code: write `nullifierOfCode` +
   round-trip theorem); exactCharge = t.charge (the charge switch makes them equal). PROVE `recordsOf` = the appended record on the
   admitted prefix (the Host's record = IntentRecord.ofIntent intent). KNOWN GAP: a `Delta.absent` write (absent over absent, not a
   retirement) leaves no leg/create, so its pin is indistinguishable from a guard asserting absence. MEASURE FIRST how many records of
   the 7 retained OB Stores (hbox /tank/dregg-build/claude-lanes/turn-log/runs/j1/stores.json; or HP-6's world-sim corpus mode) have a
   Delta.absent write. If 0: the derivation refuses it by name (`absentWrite`: a write that changes nothing is a guard) and say so. If >0:
   report the count and the receivers, and carry a write count in the Turn's pins (model-level), not a codec side-channel.
6. Replay classify (`lookupRecorded` + sameCheck over erase, Kernel/DurableCommitProtocol.lean:129) reads the archive-backed recordsOf;
   the scout's (c) list says which fields it compares.
7. Every decoder in the scout list (e) moves to the new entry (or is deleted with a reason). The frozen native accepted fixture
   (Assurance/NativeAcceptedFixture*) re-emits at range end via scripts/native-accepted-fixture/generate.sh — note it, TURN-LOG-4 does it.
8. Commit message: shape changes (entry = compact turn ‖ event digest; archive family 2; log tag v3; chain = World chain; per-leg digest
   dropped), what refuses (every pre-v3 Store, by epoch), what re-emits (all Stores, the native accepted fixture, the objective-manifest
   PersistedCodecTags row scripts/gates/objective-manifest/Compiler.PersistedCodecTags.tsv:245 — list it, INTEGRATOR re-pins), theorems
   restated old → new.
GATES: build rc (Kernel Host objective-turn-totality turn-log-follower world-sim + every module the scout list names), world-sim gate
PASS with receiver-only=0. Rows/pole/follower on FRESH Stores are TURN-LOG-4's range-end job; do not claim them.

## ADDENDUM (ROOT 10-15): HP-1 BOUNDS meets step 2
lane/hp-1-bounds (4a83fdb7 on next a5483db3; GitHub, fetch via `git fetch github lane/hp-1-bounds` or burst4 `shared`) adds
Kernel/Bounds.lean, an over-bound check in prepareAppend (legs ≤256, cells touched ≤512, cell bytes, nullifiers ≤64) and `decodeEntry`
in Kernel/DeployedTurnCompact.lean that `followFrom` uses to stop by name on an over-bound entry. BEFORE you touch prepareAppend / the
log entry / followFrom (i.e. after the carries commit, before step 2 proper), MERGE lane/hp-1-bounds into turn-log (or cherry-pick
e8bdf528 + 55a5269d), build, and then keep every bound check and that decoder through step 2 (LOG v3's decoder IS decodeEntry, extended;
bounds stay refusals by name). Pins count toward "cells touched" — say how you counted them.
