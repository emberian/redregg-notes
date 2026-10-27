# TRACE-READ: what one read costs, derived from the code at main 7dea0626

Lane TRACE-READ (Claude, read-only). Repo /Users/ember/workbox/mini-unified-push-20261003 at
`7dea062655060d673ccaad3a8d55493374672a95`. Every path:line is `git show origin/main:<path>`. Tags: **READ** (I read the
code at that line), **DERIVED** (follows from code I read; the number is an estimate), **MEASURED** (the WORKLOAD's
number, hbox busy, ~70 records, Store ~840 KB). Nothing was built or run. PERF-FIX's lane (`lane/perf-fix`) already
fixes some of what is below on its branch; this note describes **main**.

## 0. Headline: the "40×" is mostly the process model, not `atPrefix`

The two measured reads take **different paths**. READ, from the workload script
(hbox `warm-7dea0626/src/scripts/perf/workload.py:15,161-179`):

- **current read** = `mini activity --action view` → op **214** over the workspace socket, answered by the
  **resident** session Host (`Host/Main.lean:5974-5982`). MEASURED p50 ~135 ms.
- **past read** = `mini query --host H --config C … --view at`, **with no `--socket`**. That runs
  `query_once` → `authorize_observation` (`native/resource-client/src/main.rs:2150-2175, 1754-1806`). Every
  Host verb in it falls through `process` → `local_process` (`main.rs:1173-1191`), so each one spawns a **cold
  Host**. MEASURED p50 5.2–6.6 s.

Per `mini query --view at` (READ for the step list; DERIVED for the costs):

| # | step | process | Store work | term |
|---|---|---|---|---|
| 1 | `author` intent | fresh `Host codec`, used for ONE frame (`client_consent.rs:559-575`) | none | ~40 ms init (MEASURED by PERF-FIX: 0.38 G instr) |
| 2 | `client_consent::intent` | consent process | none | constant |
| 3 | `challenge` | fresh Host → `NativeHost.challenge` → `openExisting` (`Host/Main.lean:8043`, `Kernel/NativeHost.lean:670-673`) | **full cold open + validate** (§3) | O(history bytes) + Θ(cells·256·H)×3 + O(state bytes) |
| 4 | `inspect challenge` | fresh `Host codec` | none | ~40 ms |
| 5 | consent observation + `signatures` | consent + fresh `Host codec` | none | ~40 ms + consent |
| 6 | `observe-assemble` | fresh `Host codec` | none | ~40 ms |
| 7 | `query` | fresh Host → `NativeHost.query` → `openExisting` **again** (`Host/Main.lean:8057`, `NativeHost.lean:916-919`) | **second full cold open + validate**, then authorize, then `atPrefix` (§2) | as step 3, plus replay of ≤h records |
| 8 | `inspect` view | fresh `Host codec` | none | ~40 ms |

DERIVED budget: 2 × (full open + validate) ≈ 2 × 1.5–2.2 s (the cold reopen is MEASURED at 2.4 s and does a little
more: it also does the light open and the serve start, §3). Add 5–6 codec execs plus 2 consent execs ≈ 0.3–0.5 s,
and the replay ≈ 0.1–0.5 s. That gives **≈ 3.5–5.4 s of the 5.2–6.6 s, with no genesis-replay pathology needed**.
`atPrefix` is real but is the minority term at ~70 records. It becomes the majority term only once history is long.
D7 measured it at 56.6 min at 30k.

The same verb over the session costs much less. With `--socket`, `challenge` goes to op 4 and `query` to op 5
(`main.rs:1283-1284`). Both run on the resident session (`Host/Main.lean:2052-2064`), so steps 3 and 7 drop to two
refreshes (§1).

## 1. CURRENT read (op 214, resident session)

| step | where (READ) | traverses | times | term | share of 135 ms (DERIVED) |
|---|---|---|---|---|---|
| `mini` process start, read workspace.json | `activity.rs:39-55` | — | 1 | const | small |
| **SHA-256 of the 173 MB Host image** | `main.rs:556` `session_invoke` → `host_image_sha256` `main.rs:483-530`; the cache is a process-local `Mutex`, so every CLI process re-hashes | 173 MB | 1 per CLI process | O(Host bytes) | **~60–85%** (≈ 90–120 ms at ~1.5–2 GB/s with SHA-NI; more without) |
| socket connect, frame | `transport::invoke_pinned_with_local` | — | 1 | const | small |
| `sessionCurrent` → `NativeHostSession.refresh` | `Host/Main.lean:1211-1221`, `Kernel/NativeHostSession.lean:164-180` | | | | |
| ├ `extendFrom`: read the key file, `withTempDir`, store helper **fork+exec** `durable-read` (sqlite open), write and read `read.bin` | `Compiler/DurableReceiverIO.lean:357-370`, `DurableReceiverCore.lean:211-226`, `NativeCoprocess.lean` header (the helper runs `<binary> args` as **its own child**) | — | 1 | const (an exec) | ~5–15% |
| └ `light.refresh` → `Opening.extend`: a **second** `durable-read` exec of the same suffix | `Kernel/NativeHostLight.lean:52-57`, `Compiler/DurableServed.lean:774-786` | — | 1 | const (an exec) | ~5–15% |
| `activityViewLoaded`: **`loadDeployment` re-decodes the authority cell** although `opened.authority` holds exactly that `Loaded` | `Kernel/NativeHost.lean:2430-2431` vs `Kernel/NativeHostContext.lean:401-402` | authority-cell bytes | 1 | O(authority cell) | small–medium (grows with grants) |
| `configOf … activityAmbient` evaluated once for `extractTicks` and **once more per quote** | `NativeHost.lean:2434-2437, 2459-2462` | — | 1+q | const·q | small |
| `bookOf` decode of the Book cell; `canonicalBytes`/`roots` lookups | `NativeHost.lean:2464-2465`; `Kernel/DurableCommitProtocol.lean:150-160` (closure chain) | Book bytes; ≤128 closures, then a linear `tableLookup` | per asked cell | O(k) + O(cells) | small at 70 |

What it should not do at all: hash the Host image (the workspace can pin `hostSha256`, which is how a remote client
already works, `main.rs:484-489`), exec the Store twice to learn that nothing changed, and decode the authority cell
it already holds.

## 2. PAST-STATE read `at h` (the `query` Host, after its full open)

`atCovered` (`Kernel/NativeObservationController.lean:1310-1323`, READ) calls `durable.atPrefix (h − G)` once, then
`grantStanding` → `loadDeployment` on the past snapshot. That decodes the authority cell of that snapshot (READ
`Compiler/CredentialAuthorityDomainReceiver.lean:131-140`). Then it reads `canonicalBytes target`.

`Loaded.atPrefix` (`Compiler/DurableReceiverCore.lean:1307-1312`, READ) has **exactly one base**:
- `h ≥ baseHeight` → `resume` from the loaded checkpoint state;
- otherwise → `resume … 0 (State.ofSeed seed)`, which is the **genesis fold of h records**.

At ~70 records the full open's base is the checkpoint at 64. So every workload `at` read inside an object's life
(heights below 64) takes the genesis branch.

Per `resume` (`Kernel/DurableCheckpoint.lean:151-156`, READ):

| work | where | term |
|---|---|---|
| `Admissible` = `admissibleAgainst image.cellIds` (an `eraseDups` over every write in the prefix) | `:132-147` | O(writes²) unless the `@[csimp]` in `Kernel.SessionIndex` is visible (PERF-FIX B7) |
| `State.snapshot`: `rootTable` hashes **every base cell's full bytes**; `spent := prefix.flatMap nullifiers`; `history := prefix.map`; `journal := …reverse` | `:101-125` | O(state bytes·H) + O(prefix) |
| per replayed record, `IntentRecord.bind?`: cSHAKE of **every written cell's full post image** | `Kernel/DurableReceiver.lean:81-98` | O(post bytes), and the log carries whole post images (C3) |
| per record, `execute`: `lookupRecorded` walks the **whole journal** linearly | `Kernel/DurableDataIntent.lean:429-433`, `DurableCommitProtocol.lean:129-136` | O(k) per record ⇒ O(h²) |
| per record, `preflight`: `roots`/`consumed`/`available` through the closure chain; at the bottom, `nullifier ∈ spent` is a **linear list** | `DurableDataIntent.lean:326-351`; `DurableCheckpoint.lean:111` | O(k) + O(#nullifiers) |
| per record, `install`: `history ++ [event]` | `DurableCommitProtocol.lean:159` | O(k) ⇒ O(h²) |

DERIVED: at h ≤ 64 this is tens to hundreds of ms. That is real but not the 5 s (§0). It grows as Θ(h²) plus
Θ(Σ post bytes).

**What already exists for the replacement (READ):**
- **Every checkpoint is retained.** `durable_checkpoint` does `INSERT … ON CONFLICT(height) DO UPDATE` and its doc
  says "Every checkpoint is retained: a state read at a past height (`durable-checkpoint-at`) resumes from the latest
  one at or below it" (`native/hyperdocument-link-sqlite-store/src/lib.rs:1273-1292`). The Lean transport exposes it
  as `checkpointAt` (`Compiler/DurableReceiverCore.lean:387-406`). **The ledger's D7 premise ("needs every 64th
  checkpoint retained, not just the latest") is false. Nothing persisted has to change.**
- `Reader.stateAt` exists and is complete (`Compiler/DurableHistoryStoreCore.lean:155-185`): `baseOf` (`:134-153`)
  takes `checkpointAt h` → `openSealed` → the chain check at the base, then `range` for ≤63 verified records, then
  `replay`. It costs one Store exec, one checkpoint open and ≤63 records, against today's h records from genesis.
- **What `stateAt` still pays that it should not:** `openSealed` recomputes the checkpoint's **full world root**
  before checking the MAC (§3). So a `stateAt` read still pays Θ(cells·256·H) per past read, and the swap alone
  does not reach >100×.
- Wiring needed: `atCovered` is pure over `durable.atPrefix`, and `atCovered_sound`
  (`NativeObservationController.lean:1327-1340`) states its result through `atPrefix`. Moving to `stateAt` means
  `atCovered` becomes IO over the Reader, and that statement changes. → **DESIGN** (a theorem statement, no bytes).

**The session makes it worse over time (READ, new):** `extendFrom` rebases at `base + 2·checkpointEvery`
(`DurableReceiverIO.lean:403`). `Loaded.rebase` sets `baseHeight := head` (`DurableReceiverCore.lean:1185-1199`). So
after 128 records in a resident session, **every** `at h < head` is a genesis replay. The session also discards the
checkpoint base it opened from. The rebase itself re-materializes every cell, rehashes every cell
(`rootTable`), and rebuilds `history`/`spent`/`journal` over **all** records: Θ(h + state bytes·H) each time.

**Certify** (`Kernel/TailBound.lean:1-37`, READ) only writes the system cell (certified height and chain). It seals
nothing and indexes nothing, so it does not bound past-read work. Checkpoints come from the write path at
`height % 64 == 0` (`Compiler/DurableServed.lean:918`).

## 3. COLD REOPEN (2.4 s MEASURED): everything before the first answer

`mini serve` → `Host … stdio` (`Host/Main.lean:6636-6641`) → `withPinnedSignature` → `NativeHostSession.start`
(`Kernel/NativeHostSession.lean:154-162`) = **`openExisting` (the full open) AND `NativeHostLight.start` (the light
open)**, two independent opens of the same Store.

| step | where (READ) | term | est. share (DERIVED) |
|---|---|---|---|
| client `serve`: SHA-256 of the Host image plus a sealed **memfd copy** of all 173 MB | `transport.rs:1346-1380` (`start_pinned`, `sealed_snapshot`) | O(Host bytes) ×2 | 10–20% |
| Host process init (Lean initializers) | PERF-FIX MEASURED 0.38 G instr | const | ~2% |
| `withPinnedSignature`: read, write and chmod (an exec) the verifier, then exec it once | `Host/Main.lean:2704-2717` | 3 execs | ~2–5% |
| **full open** `loadChained`: `peekSeed` exec + `read 1 true` exec (**whole log** from height 1, plus seed and checkpoint) | `DurableReceiverCore.lean:989-1001` | O(store bytes) | |
| ├ `decodeRecordsFrom 1`: **every** record decoded into `List UInt8`, only the post-checkpoint ones replayed | `:1008-1013` | O(history bytes) | PERF-FIX: 17% of a bench open |
| ├ `chainPrefixesStored`: hash **every stored record's bytes** from height 1 | `:1017` | O(history bytes·H) | |
| ├ `verifyTags key 0`: KMAC every tag from height 1 | `:1034` | O(h) | |
| ├ `openSealed` (`DurableCheckpointCodec.lean:660-666`): decode the whole state, then **`worldRoot` first** (`:595` = `deployedRoot` over `rootBytes` of every cell: Θ(state bytes·H) + Θ(cells·256·H)), then the MAC, which **re-encodes the whole body** (`bodyStream.encode`, `:620-624`) although the original bytes are in hand | | Θ(cells·256·H) + 2·O(state bytes) | ~1 root eval |
| ├ `resume`: `rootTable` rehashes every cell again, then replays ≤127 records | `DurableCheckpoint.lean:101-156` | O(state bytes·H) | |
| ├ `RootCache.ofEntries` + `RootsExact.ofEntries` (the second rebuilds the same tree, PERF-FIX 6913c4a7) | `DurableReceiverCore.lean:1065-1066` | 2·Θ(cells·256·H) | ~2 root evals |
| └ `PresenceIndex`/`LinkIndex`/`CellIds`/`TxIndex` over **all** records | `:1067-1070` | O(h) | |
| `validateLoaded`: decode every cell, `cellsLawful` over every cell, the directory | `Kernel/NativeHostContext.lean:550-552` | O(state bytes) | |
| **light open** `openHead`: `peekSeed` + `readFromCheckpoint` (2 execs), **`openSealed` again** (a 4th root eval), `base.snapshot` (rootTable again), then `extendVerified` = `RootCache.ofEntries` + `RootsExact.ofEntries` (5th and 6th) + an index-row read exec | `Compiler/DurableServed.lean:714-772, 648-711` | 3·Θ(cells·256·H) + execs | ~3 root evals |
| first op 214: refresh (2 execs) + view | §1 | const | small |

DERIVED: **6 full world-root evaluations per cold reopen at main.** PERF-FIX measured ≈ 0.33 s per evaluation at
128 cells (998 ms for a 3-evaluation light open), so at the workload's ~60–100 cells that is ≈ 1–1.5 s of the 2.4 s.
The cell table is a linear list. `tableLookup` (`DurableCheckpoint.lean:81-85`) is a scan, so every
`entriesOf`/`roots c` over all cells is Θ(cells²) (D2).

## 4. The per-CLI-step process model

- **A resident session exists and is complete for reads.** `Host stdio` holds `Session = {opened (full Loaded +
  decoded directory and authority), light, openingCache, walked?}` (`NativeHostSession.lean:154-162`). Ops 4 and 5
  (challenge and query) run on it (`Host/Main.lean:2052-2064`), and so do ops 7–11 (pure codec,
  `Host/Main.lean:2070`). The client already routes `challenge`/`query` to it when `SOCKET` is set (`main.rs:1181`,
  `1283-1284`).
- **What still spawns per step even with a socket:** `process` checks `pure` **before** the socket (`main.rs:1174-1180`).
  So `author`/`inspect`/`signatures`/`observe-assemble`/`assemble` always run on a local `Host codec` child, and
  `local_frame` spawns a new one **per frame** and drops it (`client_consent.rs:559-575`). That child is a resident
  loop (`Host/Main.lean:6633`, `serveCodec`) used one-shot.
- **What a resident Host would keep:** the `Loaded` (closures flattened at rebase), the decoded `authority` and
  `directory`, the world-root tree (`RootCache`), the light `Opening`, the Host-image digest, and a height→`State`
  map of every checkpoint it has opened or sealed, which makes past reads nearest-checkpoint replays.

## 5. THE TOP FIVE constant-term offenders

1. **Two cold full opens per signed read (the `mini query` path without `--socket`).** Should not happen at all,
   because a resident session already holds the validated opening and serves ops 4/5 (`Host/Main.lean:2052-2064`).
   Elimination: the client uses the workspace's `socket` for `challenge`/`query` whenever the workspace names one
   (`activity` already does), and the workload passes `--socket`. ~2 × 1.5–2.2 s → 2 refreshes. **LOCAL** (client
   and driver only).
2. **One `Host codec` process per pure-codec frame** (5–6 per signed read; ~140 per tiny workload run,
   PERF-FIX MEASURED). Should not happen at all, because `serveCodec` is a loop: keep the child in a process-wide
   static, as `SESSION` already is for consent (`client_consent.rs:42`). Across CLI steps, send ops 7–11 to the
   local session socket, which already answers them. The in-process reuse is **LOCAL**. Routing consent codecs
   to the serving Host is **DESIGN**: it changes which process the client's consent trusts (key and custody
   scope, CLAUDE.md pause 1).
3. **SHA-256 of the 173 MB Host image in every `mini` process** (`main.rs:556`, `483-530`): ≈ most of the 135 ms
   current read. Should not happen at all, because the server runs a sealed memfd pinned at `serve` start and
   checks the sha the client names. The client can name the workspace's pinned `hostSha256` (the remote path
   already does, `main.rs:484-489`). **LOCAL** if the workspace pin is written at workspace creation. Weakening it
   to an mtime cache would be a check change (DESIGN).
4. **Full world-root re-evaluation on every open, 6× per cold reopen and 1× per `stateAt`.** `openSealed` computes
   `worldRoot` **before** the MAC that already binds that root, then re-encodes the whole body for the MAC. Then
   both opens rebuild the tree, twice each. Should not happen at all in a resident process: build the tree once
   and keep it; check the MAC first over the **stored** body bytes; hand the checked tree onward (PERF-FIX a16e2f1b
   on the light path). Dropping the root recompute behind a valid own-key MAC is **DESIGN** (it removes a check).
   Open-once, ordering and reuse are **LOCAL**. Persisting tree nodes or a compressed SMT is **DESIGN**
   (re-genesis).
5. **Past reads replay from genesis when every checkpoint is on disk** (`atPrefix` single base; `rebase` →
   base = head). Should not happen at all: `checkpointAt` plus `Reader.stateAt` exist (§2). Elimination: route
   `at` through `stateAt` (**DESIGN**: `atCovered`/`atCovered_sound` become IO and Reader-based). Or, with no
   statement change, give `Loaded` a retained list of `(height, State)` checkpoint bases so `atPrefix` picks the
   nearest one ≤ h, keeping `atPrefix`'s spec (**LOCAL**: a field plus proofs, no bytes, statement unchanged).
   Plus an indexed cell table (`HashMap CellId (bytes, root)`, D2; **LOCAL** via `@[csimp]`) so the base costs
   O(1) per lookup.

## 6. What SINS-LEDGER-20261009 did not already name (or got wrong)

- **WRONG premise, D7:** checkpoints are **all retained** in the SQLite store (`lib.rs:1273-1292`). `stateAt` is
  unblocked today, so no persisted change is needed for nearest-checkpoint replay.
- **The 40× compares different paths.** The current read is resident op 214; the past read is a socketless
  `mini query` that cold-opens the Store **twice** (challenge, then query). The ledger's D6 names cold CLI opens for
  `workspace create`, not for signed reads.
- **The client re-hashes the 173 MB Host image per CLI process** (`main.rs:483-530`), and `serve` hashes and
  memfd-copies it again. Neither the ledger nor PERF-FIX names this. DERIVED as the majority of the current read.
- **Every session request execs the Store twice even when nothing changed** (`extendFrom` + `Opening.extend`, each
  a `durable-read` exec through the helper's own child, plus `withTempDir` and a key-file read).
- **`Session.start` performs both a full and a light open** (`NativeHostSession.lean:154-162`). The ledger says
  "two root evaluations per cold open"; at main a cold session start does **six**.
- **`openSealed` order and re-encode:** the root is evaluated before the cheap MAC check, and the MAC re-serializes
  the entire body instead of hashing the stored bytes (`DurableCheckpointCodec.lean:620-624, 660-666`).
- **`activityViewLoaded` re-decodes the authority cell** although `Opened.authority` holds it (the same pattern recurs at `NativeHost.lean:485,2025,2531`)
  (`NativeHost.lean:2430` vs `NativeHostContext.lean:401-402`), and it evaluates `configOf` once per quote.
- **Linear `spent` membership and linear `lookupRecorded`:** after any checkpoint or rebase,
  `consumed n = n ∈ spent` scans every nullifier ever (`DurableCheckpoint.lean:111`). Every `execute` walks the
  whole journal (`DurableCommitProtocol.lean:129-136`) although `Loaded` carries a `TxIndex`. Both are O(h) per
  write and per replayed record.
- **Rebase discards the checkpoint base:** a session past 128 records has `baseHeight = head`
  (`DurableReceiverCore.lean:1185-1199`), so every `at` below head is a genesis replay. That is worse than a cold
  open, which at least starts from the latest checkpoint.
- **Full open decodes and chain-hashes the whole log from height 1** (`DurableReceiverCore.lean:1008-1017`),
  although only the suffix after the checkpoint is replayed. The chain could resume from the checkpoint's MAC'd
  `chain` (the light open already does: `DurableServed.lean:752-760`).

## 7. Cheap confirmations (instruments already in tree, no new code)

`MINI_OPEN_TIMING=1` prints light-open laps (`DurableServed.lean:718-722`). `MINIDREGG_HOST_TRACE=1` prints the
op1/op5 refresh time (`Host/Main.lean:1206-1208`). `strace -f -e execve` on one `mini query --view at`
should show 2 Store-opening Hosts and 5–6 `codec` Hosts (§0). Rerunning the same verb with `--socket` gives the
ratio that item 1 claims.
