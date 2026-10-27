# TRACE-CREATE: what one Objective CREATE costs, derived path by path (2026-10-13)

Tracer: TRACE-CREATE (Claude, read-only). Repo `/Users/ember/workbox/mini-unified-push-20261003` at
`7dea0626`. Workload: hbox `warm-7dea0626/perf/r1`, 20 births, store 12 to 52 records during births, 80 at the end.
Tags: **READ** (path:line at 7dea0626), **DERIVED** (follows from the code read), **MEASURED** (number + source),
**UNRESOLVED** (the code read does not settle it; see §6 for the run that would).

## 0. Calibration: what each CLI step costs, attributed from r1's `perf.csv` (MEASURED)

`perf stat -I 250 -e instructions:u` wraps the whole workload, `mini serve` and its Host child included
(`scripts/perf/workload.sh:40-41`). I split it at each step's end, using the mtime of `transcript/NNN-*.rc`.
Error is about ±0.25 s per boundary.

| step (CLI) | first (h≈12) | last (h≈52) | slope | median |
|---|---|---|---|---|
| `resource-bNNNN` (`mini workspace --action create`) | 32.3 G / 3.6 s | 73.5 G / 5.7 s | **+2.2 G per birth** | 52.6 G / 5.0 s |
| `create-bNNNN` (`mini activity --action submit`, kind create) | 20.1 G / 1.7 s | 50.1 G / 3.2 s | **+1.6 G per birth** | 34.6 G / 2.5 s |
| `001-constants` (one cold Host spawn, `objective-constants`) | 0.0 G / 0.04 s | | | |
| `view-r*` (`mini activity --action view`: 1 socket op 214 + `mini` start) | | | | 1.8 G / 0.13 s |
| `117-reopen-probe` (a new `mini serve`: Session.start + query, h=80) | | 38.2 G / 2.5 s | | |

What these numbers already decide (DERIVED from them):
- **The cost is not process start.** A cold Lean Host spawn is about 40 ms and about 0 G. The Store is
  served by ONE warm Host (`mini serve` → `transport.rs` `supervise_bounded` → one `HostProcess` in `stdio` mode,
  `Host/Main.lean:6638-6643`). `w/public/serve.log` names one host pid. So the ledger's D6 (cold Host per CLI step) is
  **not** the regime this workload measures. Only the codec verbs 7–11 spawn (see A5/B2).
- **Both steps grow linearly with history, at about 1 G per record per step.** Births add 2 records each (the
  resource birth and the create). The intercepts are ~20 G (resource) and ~10 G (create) at h=0. A CREATE costs more
  than one cold reopen at h≈40.
- On hbox (cpu_core and cpu_atom) the run sustains ~10–12 G instr/s, so this is single-thread CPU in the server
  Host. The client is not the cost.

## 1. Path A: `mini workspace --action create` (the resource step)

Client: `workspace.rs:6848` → `create_with_template` (`:4819`) → `birth` (`:4458`) → `complete_birth` (`:4116`).
Server ops go through the socket (`workspace.rs:369` pins SOCKET from workspace.json). Each socket op runs
`dispatchSession`/`fnDispatch` in the warm Host, and almost every op starts with `sessionCurrent`
(`Host/Main.lean:1210`) → `NativeHostSession.refresh` (`Kernel/NativeHostSession.lean:166-183`).

| # | what runs (READ) | what it traverses | ×/req | term |
|---|---|---|---|---|
| A0 | `mini` start; `host_image_sha256` over the **173 MB** Host image (`main.rs:483-534`, cached per process only) | 173 MB SHA-256 | 1 per `mini` process | O(image), ~0.4–0.7 G DERIVED (SHA-NI ~2–4 instr/B) |
| A1 | `birth`: birth context JSON, `participant_namespace::reserve`, blinding (`workspace.rs:4504-4680`) | local files | 1 | constant, small |
| A2 | `signed_view(…factory…,"resource")` (`workspace.rs:4736`): op 4 challenge plus op 5 query. **The step's FIRST request refreshes the session over the previous step's create record**, which op 212 never adopted (B3). | see R below | 1 refresh-with-entry | O(h)+O(cells·257·H), see R |
| A3 | `current_birth::author` (`current_birth.rs:79`): copies source/config, then `session_invoke` op 91 → `CurrentResourceBirthAuthoring.intentLoadedAuthorized` (`Main.lean:7422-7435`) | signed observation verify on `opened` | 1 | UNRESOLVED (observation authorization) |
| A4 | `submit_once` (`main.rs:1851`): `authorize_observation` (challenge + signatures), op 1 prepare (`prepareAuthorizedLoaded`, `NativeHost.lean:829`), `inspect plan` + `signatures` + `assemble` (verbs 8/9/11: **each spawns a fresh local Host `codec` process**, `client_consent.rs:549-575`), op 2 submit, `inspect outcome` (one more spawn) | 4 Host spawns at ~40 ms each | 4 | ~0.16 s wall, ~0 G |
| A5 | op 2 → `submitDisclosedWith` → `ResourceBirthReceiver.receiveLoaded` (`Kernel/ResourceBirthReceiver.lean:497`): `replay` (journal lookup), `admitDecodedNative`, `DurableReceiverIO.receiveLoaded` → `receiveCandidateWithFresh` (`Compiler/DurableReceiverIO.lean:247`): `prepare` (executes the intent), `judge` (3 gates), `prepareAppend` (index rows read, `Loaded.extend` = **incremental** root advance, one 257-hash path per written slot, `DurableReceiverCore.lean:1126-1135`), `append`, `readBackEntry`, `storeCheckpoint` when due (every 64th: whole state plus full root, ledger D9) | the record (~10 KB, MEASURED 840 KB/80 records), w+1 tree paths | 1 | O(record)+(w+1)·257·H |
| A6 | op 2's `confirm` = `sessionConfirmed` (`Main.lean:1271-1286`) → `sessionOpened` → **refresh over the record this same request just wrote** → `historicalReceiptVia` (`NativeHost.lean:1532`) → `historyReader` (Reader per call) | see R | 1 refresh-with-entry | O(h)? + O(cells·257·H) |
| A7 | `complete_birth`: writes refs, maybe more views | local | 1 | small |

**R: one session refresh over k new entries** (`NativeHostSession.refresh`, READ `Kernel/NativeHostSession.lean:166-183`):
1. `DurableReceiverIO.extendFrom` (`DurableReceiverIO.lean:357-412`): `transport.read`, decode k records, `verifyTags`,
   `walkFrontier`, then `Loaded.replay` = **execute each new record again** (`prepare` + `Loaded.extend`), compare
   `rootLog`.
2. `light.refresh` → `Opening.extend` → `extendVerified` (`Compiler/DurableServed.lean:648-712`): decodes the same k
   records **again**, `chainPrefixesStored`, `verifyTags` again, index rows plus `checkIndex`, **`replay` again over the
   light state**, then **`Served.entriesOf` over every cell, `RootCache.ofEntries` (a full 256-level tree build,
   Θ(cells·257·H)) and `RootsExact.ofEntries`** (`:683-686`). Then `extendIds` = `(ids ++ writes).eraseDups`.
3. `validateLoadedFrom` (re-decodes only the moved cells).

`RootsExact.ofEntries es` is defined as `⟨…, (RootCache.ofEntries es).injectiveCheck, …⟩`
(`DurableReceiverCore.lean:561-562`). It builds the tree **a second time** unless the compiler inlines it and
CSEs the two calls (DERIVED; not checked in the IR). The same pair appears in `loadChained` (`DurableReceiverCore.lean:1065-1066`,
`RootCache.ofEntries … , RootsExact.ofEntries …`).

**Path A totals (DERIVED):** the step's records are executed 1 (commit) + 2 (A6 refresh: full and light) times. The
previous step's create record is executed 2 more times (A2 refresh). Full root-tree builds: 2 (two light refreshes),
or 4 without CSE. Codec Host spawns: 4. 173 MB image hashes: ≥1.

## 2. Path B: `mini activity --action submit` with `kind: create` (the headline)

Client (READ `native/resource-client/src/activity.rs:95-152`) runs 7 Host ops in sequence:
214 view → 7 author → 210 plan → 8 inspect → 211 assemble → 212 submit → 8 inspect.

| # | what runs (READ) | traverses | ×/req | term |
|---|---|---|---|---|
| B0 | `mini` start plus the 173 MB image hash (as A0) | 173 MB | 1 | ~0.5 G DERIVED |
| B1 | op 214 (`Main.lean:5974`): `sessionOpened`. Its refresh is empty here, because A6 adopted the resource record. Then `activityViewLoaded` (`NativeHost.lean:2428`): `loadDeployment` (decodes the authority cell) plus the requested cells | authority cell | 1 | O(authority bytes) |
| B2 | ops 7, 8, 8 → `session_invoke` → `codec_frame` → **a fresh local Host `codec` process per call** (`client_consent.rs:549-575`) | | 3 spawns | ~0.12 s wall |
| B3a | op 210 → `activityPlanLoaded` (`NativeHost.lean:2350-2366`): commandCodec decode, then **five separate kernel runs over the same (snapshot, command)**: `signingHeader` (`ObjectiveActivityReceiver.lean:182`, which calls `planOutcome` and `loadDeployment`), `planReport` (`:207`), `planOutcome`, `planVerdict` (`:167`, `decideTurn` + `ActivitySeatEnd.finish`) and `planFrontEnd` (`:228`). Each one calls `configOf` and `decideTurn` afresh. | 5× decide, 2× authority decode, 5× configOf | 5 | 5·D |
| B3b | op 211 → `activityAssemble`: decode the plan, encode the ingress | O(plan bytes) | 1 | small |
| B3c | op 212 → `activitySubmitLoaded` (`NativeHost.lean:2377`) → `ObjectiveActivityReceiver.receiveLoaded` (`:38-60`): `decodeIngress`, `replay` (journal), `admitDecodedNative` (gate: authority decode, **decide again**, native signature check), `receiveObjective` → `proposal.check` (**the R2 certificate re-derivation, which runs the kernel once more**) → `receiveCandidateWithFresh` (as A5: execute, judge, incremental root advance, append, readback, checkpoint if due) | ≥2 more decides, plus 1 execute | 1 | 2–3·D + O(record) |
| B3d | **op 212's confirmation = `NativeHost.confirmed` (`NativeHost.lean:1245-1253`) = `openExisting config` = a FULL COLD OPEN inside the warm server**, just to read back one receipt. `DurableReceiverIO.load` → `loadChained` (`DurableReceiverCore.lean:1065`-region `loadChained`) does: `transport.read 1 true` (**the whole log**); decode **every** record; `chainPrefixesStored` (hashes **every** stored record's bytes); `verifyTags` (MAC over **every** tag); `openSealed` if a checkpoint exists (decode it and **recompute its whole root**, ledger C2); `walkFrontier`; **`resume` = replay from the checkpoint, or from genesis while h<64, as during all 20 births**; `RootCache.ofEntries` and `RootsExact.ofEntries` over every cell; `PresenceIndex.ofRecords`, `LinkIndex.ofRecords`, `TxIndex.ofRecords` and `CellIds.ofImage` over every record. Then `validateLoaded` (`Kernel/NativeHostContext.lean:550`): `loadDirectory` (decodes **every** cell), `loadDeployment`, `cellsLawful` per cell. The result is thrown away; the session is not updated. | O(h·record) + O(h executes) + O(state bytes) + 1–2 full trees | 1 | **O(h)**, the dominant growing term |
| B4 | the NEXT CLI step's first request refreshes over this record (R): 2 more executes, 1–2 full tree builds | | 1 | O(cells·257·H) |

`Creation.intent` (READ `Kernel/ObjectiveActivity.lean:3564-3568`) is cheap: `intentOf` over `created.posts` plus two
guards. `storageDeposit` (`:2053`) encodes the record once per decide to measure its length, so that happens ×7–8.

**Path B totals (DERIVED):** per CREATE, `decideTurn` on the same input runs **~7–8×**: 5 in plan, 1 in gate, 1 in
`proposal.check`, plus the execute. The create record is then executed 1 (commit) + 1 (inside the cold open's
replay) + 2 (the next refresh) times, and **all h earlier records are executed once more** by the cold open's `resume`.
Full root-tree builds: 1–2 (cold open) + 1–2 (next refresh). Whole-log reads/decodes/MACs/hashes: 1.

## 3. The same value recomputed (DERIVED, from §1–2)

| value | computed | where |
|---|---|---|
| decided turn for (snapshot, command) | 7–8× per CREATE | B3a ×5, B3c ×2–3 |
| `configOf deployment profile ambient` | ≥7× | each plan* fn, gate |
| authority (`loadDeployment`, decodes the authority cell) | ≥4× | B1, `signingHeader`, gate, `validateLoaded` |
| each new record's execution | 3–4× after commit | commit, extendFrom, extendVerified, cold-open resume |
| world root (full tree from all cells) | 2–4× per committing step | light refresh (R2), cold open (B3d); ×2 if `RootsExact.ofEntries` is not CSE'd |
| the checkpoint's root | once per cold open, although the MAC already binds it | `openSealed` (ledger C2) |
| every record's bytes: decode, chain hash, MAC | once per CREATE (B3d) plus twice per new record (R1 and R2 each decode and `verifyTags`) | |
| session state | kept in `Session`, then **rebuilt from scratch beside it** by `confirmed` | B3d |
| 173 MB Host image SHA-256 | once per `mini` process, i.e. per CLI step | A0/B0 |

## 4. `List UInt8` concatenation and length on the path (READ, with n)

- `RootCache.write`: `entries ++ [(key,value)]` per written slot (`DurableReceiverCore.lean:459-460`): n = slots
  written since the tree was built (ledger D4).
- `fixedStream.decodePrefix`: `if width ≤ octets.length` (`Compiler/Tower256ConcreteBackend.lean:309-313`) walks the
  **whole remaining byte list** for every fixed-width field (`digest256Stream`, `height64Stream`; 12 uses in
  `Kernel/ObjectiveActivity.lean`, e.g. `:281-303`). Decoding m fixed fields from an n-byte buffer costs **O(m·n)**.
  Every Objective record/cell decode pays this, ×7–8 per CREATE plus every replay. Not in the ledger.
- `extendIds`: `(ids ++ writes).eraseDups` (`DurableServed.lean:63-64`): O((cells+w)²) comparisons per refresh.
- `digestStream` = `StreamCodec.nat` base-255 (`Tower256ConcreteBackend.lean:255`): each node hash encodes two
  256-bit Nats digit by digit into lists before cSHAKE. The Keccak itself is the unboxed `@[csimp]` one
  (`Theory/Sp800185Cshake256Fast.lean:1-30`), so the ledger's "pure Lean over List UInt8" premise for **H** is out
  of date: the list cost is in the framing, not in the permutation.
- `outcomeCodec.encode`, `toUTF8.toList`, `commandCodec.decode`: every frame crosses as `List UInt8` and is copied
  back and forth (`payload.toList` at `Main.lean:2670`).
- Client side: `splitPair`/`pair` copy payloads (`main.rs:1260-1275`); this is small.

## 5. TOP FIVE constant-term offenders

1. **`confirmed`/`charged` cold-open the whole Store inside the warm server to read back one receipt** (B3d,
   `NativeHost.lean:1245-1263`). The same `confirmed` sits on ≥12 session submit routes (`NativeHost.lean:1270, 1316,
   1349, 1907, 1917, 1994, 2079, 2261, 2314, 2381, 2500, 2637`). *Should not happen at all, because* the commit
   already holds the extended `Loaded`: `publishAfter`'s `.exact` branch (`DurableReceiverIO.lean:212-221`) has the
   successor and the entry it read back. Ordinary births already confirm through the session (`sessionConfirmed`)
   and adopt it. **Elimination:** route op 212 (and every `confirmed` caller under `stdio`) through
   `sessionConfirmed` or `sessionExactConfirmed` (`Main.lean:1288-1297`), so the receipt is read off the adopted
   successor. LOCAL. Expected: removes the O(h) growth of the CREATE row and most of its intercept (DERIVED; the
   slope match is in §6).
2. **The plan runs the kernel five times on one input, and submit runs it twice more** (B3a/B3c). *Should not
   happen at all, because* `decideTurn config snapshot height command` is a pure function of values that are equal
   across all five calls. **Elimination:** one `decideTurn` (and one `finish`) in `activityPlanLoaded`, with
   header/report/outcome/verdict/frontEnd projected from that `Decided`. At submit, let `proposal.check` consume the
   gate's `Decided` instead of re-deriving it. LOCAL for the plan. For submit it touches the `Proposal.check`
   statement, so DESIGN (it is R2's certificate shape).
3. **Every committed record is re-executed and re-verified 2–3 more times, and the root tree is rebuilt from all
   cells on each light refresh** (R: `extendFrom` + `extendVerified` + replay). This happens because a commit never
   advances the *light* opening: A6 refreshes over the record it just wrote, and op 212's record waits for the next
   request. *Should not happen at all, because* this process wrote the entry and holds the `Loaded`/`Opening` it
   came from: an append is the one case where "verify the suffix another writer appended" has no other writer.
   **Elimination:** after `.exact` readback, advance BOTH openings by the record (`Light.adopt` exists,
   `NativeHostLight.lean:58-61`, and `receiveServed` is the light write path). `extendVerified` must advance
   `roots` by `RootsExact.advance` (the unlanded kern-grow patch) instead of `ofEntries`. LOCAL. The persisted /
   compressed tree (ledger D3) is DESIGN.
4. **`fixedStream` decodes call `List.length` on the remaining buffer per field** (§4). This is O(fields·bytes) on
   every Objective record, cell, plan and ingress decode, and those run ×7–8 per CREATE plus every replay.
   **Elimination:** decode by consuming `width` bytes with a bounded take that fails on a short list
   (`List.splitAt` plus a length check on the *taken prefix*), and prove that equal to the spec by `@[csimp]`.
   Better: `ByteArray`/`Subarray` cursors for every codec (ledger D8). LOCAL. No byte changes.
5. **Every CLI step is a fresh `mini` process that SHA-256s the 173 MB Host image, and the codec verbs 7–11 spawn a
   fresh Host each** (A0/A4/B0/B2: 4 spawns per resource step, 3 per create). *Should not happen at all, because*
   the warm server already answers ops 7–11 itself (`dispatchSession` `| 7 | 9 | 10 | 11 => pureCodec`,
   `Main.lean:2070`), and the image pin could be checked once per server, not per client process.
   **Elimination:** send 7–11 over the socket when one is pinned (it is already a `socket_process` arm,
   `main.rs:1287-1290`), and cache the image digest by (dev, ino, mtime, size) on disk. Long-term, one client session
   per workload. LOCAL. It is minor in instructions (~0.5 G and ~0.15–0.3 s wall per step) but it sets the floor for
   a 100× target, so it has to go.

## 6. What the ledger (§1) did not name, and what is still UNRESOLVED

New against `SINS-LEDGER-20261009.md` §1:
- **N1 (offender 1).** The warm server cold-opens on every `confirmed`. D6 names cold Hosts in the *client*. This
  one is inside the session server, on ≥12 routes, and it is the CREATE headline's O(h) term.
- **N2.** The commit does not advance the openings it came from, so every record is re-verified 2–3× (offender 3).
  D5 names `extendVerified`'s rebuild, not that the writer pays it for its own append.
- **N3.** The five-fold (seven-to-eight-fold) `decideTurn` (offender 2).
- **N4.** `fixedStream` `octets.length` per field (offender 4). It lives in exactly the fixed-width codecs added so
  that storage deposits are value-independent.
- **N5.** `RootsExact.ofEntries` rebuilds the tree it certifies (`DurableReceiverCore.lean:561-562`). Whether it
  doubles every full build depends on inlining. CHECK: `lean --c` IR of `extendVerified` / `loadChained`.
- **N6.** The ledger's D6 regime does not match r1. The workload has a warm socket Host, and its cost still grows
  ~1 G per record per step. The ledger's premise that H is pure Lean over List UInt8 is out of date (§4).
- **N7.** The client hashes the 173 MB image per `mini` process; codec verbs spawn per call (offender 5).

UNRESOLVED (the reading does not close these, and I will not dress them up):
- **The per-record constant.** The slopes are MEASURED: create ≈ +0.75 G per record of history, resource ≈ +1.1 G
  per record. B3d replays every record once per CREATE, which explains the create slope's *shape*. But the
  resource step has no cold open and grows *faster*. So something in A2/A3/A6 is also O(h) with a ~1 G-per-record
  constant. Candidates, all READ but unpriced: `historyReader`/`DurableHistoryStore.readerOf` per
  `historicalReceiptVia` (A6); the signed-observation `authorize` against `observationContext` (A2/A3); the op 5
  `queryWireLoaded`; `consumed := decide (nullifier ∈ spent)` over `prefixRecords.flatMap` (`DurableCheckpoint.lean`,
  `State.snapshot`), linear per query.
- **H.** The root rebuilds use the unboxed Keccak plus Nat-digit framing. I estimate H at 10–50 k instructions, so a
  full tree at ~100 cells is ≈0.3–1.3 G (DERIVED, unmeasured). That is enough to matter for the intercept and **not**
  enough to explain a ~1 G-per-record slope. So the ledger's ranking (root tree first) may be wrong for this regime.
- **One run settles all of it**, with instruments that already exist and were off in r1: `MINIDREGG_HOST_TRACE=1`
  on `mini serve` (`phaseTrace`: "op1 refresh", "op5 refresh", "confirm refresh", `Main.lean:1206-1208,2047,2063,1279`)
  and `MINI_OPEN_TIMING=1` (`openHead` laps: "records, chain, tags, frontier", "index rows read", "index", "replay
  and root", `DurableServed.lean:718-720`). A one-line `phaseTrace` around `confirmed`'s `openExisting` would price
  N1 directly. I did not run it (read-only brief); PERF-FIX's lane owns runs.

## 7. Order of elimination (DERIVED)

Do N1 (confirm through the session) first. It is LOCAL, a few lines, and removes the CREATE row's O(h) term. Next,
N2 plus kern-grow's `advance` (no self re-verify, no `ofEntries` on refresh), then N3 (one decide), then N4 (codec
length), then N7. After those, the per-request work should be decide once + execute once + (w+1) tree paths +
append + readback. With ~10 KB records that is ~10⁷–10⁸ instructions, which is the >100× the brief asks for.
Anything still left above that is the UNRESOLVED A-path term, and the trace run above names it.
