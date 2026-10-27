# JUDGE — what the judgment layer does per request that it should not do at all

TRACE-JUDGE (Claude, read-only). Repo `/Users/ember/workbox/mini-unified-push-20261003` at `origin/main = 7dea0626…`.
Tags: **READ** (path:line at 7dea0626) · **DERIVED** (follows from the code read) · **MEASURED** (number + source) ·
**INFERRED** (an estimate). The shared tail (Store open, root rebuild, replay, commit, checkpoint) belongs to the other
tracer. Here it is only named, as **[TAIL]**.

## 0. The answer in one paragraph

One UPDATE (an `invoke` on an existing object, one frame, no sends) is **two `mini activity submit` processes**: a
`--prepare-only` probe that learns the front-end quote, then the real submit. Each process plans the turn twice: once on
the serving Host (op 210) and once in a freshly spawned local consent provider (op 224). **Each plan decides the turn
five times.** Each decision of an invoke loads its method. **Each load re-runs the whole source front end** on the
pinned package: parse, two elaborations, four typed-core packet renders, three checker runs and two identity hashes.
That package is content-addressed, and the kernel already replayed it when it was published. Counting the server
admission and the consent provider's re-admission of the previous record gives **≈22 decisions and ≈22 front-end
replays per UPDATE**, where one of each would do. A CALL or a SEND adds one more load per decision (the callee frame or
the deliverability check), so it pays ≈22 more replays. That matches the measured +2 s (≈8 s against ≈6 s).

## 1. UPDATE path: step table

Volume per UPDATE. `P` = one `mini activity submit` process (×2 per invoke). `d` = one `decideTurn` (Core:552).
`L` = one `loadMethod` (ObjectiveCall:437). The shares in the last column are INFERRED from the §3 split and are rough.

| # | step | where (READ) | what it traverses | count / UPDATE | term | share |
|---|---|---|---|---|---|---|
| 1 | client protocol: probe plan, then real submit | `native/resource-client/activity_world.py:327-328,337-387` (`quote_front_end` runs `submit --prepare-only`) | the whole of rows 2–9 | 2 P | ×2 on everything | (multiplier) |
| 2 | mini hashes the 173 MB Host image (SHA-256) before the first socket op | `src/main.rs:483-541`, `:546-559` (cache is per process) | 173 MB | 2 | O(image) | ~1–2% INFERRED |
| 3 | pure codec verbs, each a fresh Host exec: author (op 7) and inspect plan (op 8); the real submit adds inspect outcome | `src/activity.rs:79-86,121,125,145` → `client_consent.rs:549-575` (spawns `host codec` per call) | Lean init ≈0.38 G instr each (MEASURED, `SHOULDNT-BE-DOING-20261013.md` §"Workload") | 5 | constant | ~2% |
| 4 | op 214 view, read only for `authorityRoot` | `activity.rs:106` → `Host/Main.lean:5974-5982` → `NativeHost.lean:2428` (`loadDeployment` decodes the authority cell; loads the Book) | authority cell + Book bytes | 2 | O(auth+book bytes) + [TAIL] refresh | small |
| 5 | **op 210 plan on the server: 5 decisions + 3 `finish`** | `Kernel/NativeHost.lean:2350-2365`: `signingHeader`→`planOutcome` (d+finish), `planReport` (d), `planOutcome` (d+finish), `planVerdict` (d+finish), `planFrontEnd` (d); bodies at `ObjectiveActivityReceiver.lean:167-235`, `ObjectiveActivityReceiverCore.lean:2707-2719` | each d: one L + run + posts + Book; each finish: `judgeDomains` | 2×5 d, 2×5 L | 5× O(turn) | **~20%** |
| 6 | **op 224 consent re-plan: the same 5 decisions** | transport calls `check_signing_plan_reply` after every 210 (`transport.rs:1146`, `:902-908`) → `client_consent.rs:583-588` → `Kernel/NativeSpecializedConsent.lean:81-83` (`activityPlanLoaded` again) | same | 2×5 d, 2×5 L | 5× O(turn) | **~20%** |
| 7 | consent provider cold start per mini process: spawn, offer anchor (228), check Store against it, re-admit records after it | `client_consent.rs:76-91,104-127`; the anchor's root re-validation is [TAIL]; re-admission = `NativeHostReplay.lean:2341-2349` → `admitDecodedNative` (gate+verify+d+finish) + `Derived.judge` (`:2943`) | the previous update's record: 1 d, 1 L, 1 CheckedCommit | 2 starts, ~1–2 d | [TAIL] + O(turn) per new record | ~15–20% (24% of all samples, MEASURED SHOULDNT §Workload) |
| 8 | op 211 assemble: decodes header and command again | `NativeHost.lean:2367-2375` | ingress bytes | 2 | O(bytes) | small |
| 9 | **op 212 admit** (real submit only) | `ObjectiveActivityReceiver.lean:38-61` → `Core:2366-2414` | see rows 9a–9g | 1 | | ~15% + [TAIL] |
| 9a | `decodeIngress` (ingress, command, envelope) and replay lookup; `event` re-encodes the whole ingress and cSHAKEs it (twice in `replay`) | `Core:417-427,914-921,2651-2670` | ingress bytes | 1 + ~4 event hashes per admission | O(bytes·H) | small |
| 9b | **gate: `loadDirectory` decodes EVERY cell** | `Core:818` → `Compiler/CredentialAuthorityDomainReceiver.lean:288-307` → `DurableReceiverCore.lean:851-853` (`cellIds.map canonicalBytes`) | all cells; each a closure-chain lookup (ledger D1) plus a decode | 1 per admission (server + consent) | **O(cells·(k + cell bytes))** | grows |
| 9c | gate: `loadDeployment` (authority cell decode), stale-root check, spent marker, `configOf` (decodes the policy bytes again), `authorized` (re-encodes the command for `cost`, and again plus a cSHAKE for `argsDigestBytes`), `funding` → `loadBook` (whole Book decode) | `Core:682-760,789-800,815-832`; `ObjectiveKernelConfig.lean:44-60` | authority cell, Book, command | 1 | O(auth + book + cmd) | small |
| 9d | native signature verify | `Core:2374-2377` | — | 1 | constant | small |
| 9e | `prepare`: d + finish once more | `Core:874-892` | as row 5 | 1 d, 1 L | O(turn) | ~4% |
| 9f | `PhysicalShape` decided at runtime: `Nodup`, `expectedPre = roots c`, `PhysicalPostLaw`, `ActivityOrBook` (payload decode + a coordinate cSHAKE per write), `isRetired(canonicalBytes)` | `Core:2292-2306,2232-2277` | writes × (root lookup + decode + H) | 1 | O(writes·(k+bytes+H)) | small |
| 9g | **CheckedCommit (R2)**: `Turn.ofLoaded` decodes each written cell's pre and post (`deltaOf` is reached from `writeRefusal`, `createsOf`, `retiresOf`, `legsOf` and `chargeOf`: up to ~5 per write without CSE), `storageOf` re-encodes every leg; then `Installs (execute .complete …)`; then `receiveCandidateWithFresh` runs `DurableCheckpoint.prepare`, **a second execute of the same intent** | `Kernel/ObjectiveAdmissible.lean:117-133`; `Kernel/HostRefinesWorldCore.lean:409-412`; `Kernel/TurnOfIntent.lean:655-764`; `Compiler/DurableReceiverIO.lean:274-281,245-258` | written cells' bytes ×~5; intent ×2 executes ([TAIL] roots) | 1 server + 1 per consent re-admission | O(writes·bytes) + 2×[TAIL] execute | ~5% |
| 10 | [TAIL] session refresh before every server op (`sessionCurrent` → `NativeHostSession.refresh`) | `Host/Main.lean:1210-1221,1245-1248` | — | 7 (214,210,211 ×2; 212) | [TAIL] | [TAIL] |

**Within one decision `d` of an invoke (one frame), READ `ObjectiveCall.lean:2314-2352,1114-1209`:**
- `exec .enter`: a `stack.any` re-entry check; `touch` (a `find?` over the journal, then `readObject` and `readState`,
  each a coordinate cSHAKE, a closure-chain lookup and a decode); `frameAuthority`; then **`loadMethod` (`:1134`)**.
- `runCounted` (the Bend run, bounded by envelope ticks), then `ObjectiveBendDemandData.complete` (extraction),
  `decodeReturn`, `frameReturn` (`decodeWrite`, `applyWrite`, `ObjectRecord.judge`: the law over the one object's slots,
  `Kernel/ObjectRecord.lean:483-500,841-856`, DERIVED cheap).
- `postMail` and `postControls` (no-ops for UPDATE); `loadBook` (a whole-Book decode, the 2nd per decision with
  `funding`); `postings` (the Book admission over the batch).
- `finish` → `finalize` (seats: `ending` is `none` for invoke) → `judgeDomains`
  (`Kernel/ObjectiveDomain.lean:263-282`). It covers only written objects' domains: **not** all members, **not** all
  cells. It decodes each post's cell 2–4× (`keepsDomains`, `writtenObjects`, `postedDomains`, `finalRecord`). Its
  term is O(posts·cell bytes + Σ members of the touched domains). DERIVED: bounded, not a whole-world scan.

**Within one `loadMethod` L.** READ `ObjectiveCall.lean:437-462,374-419`; `ObjectiveActivity.lean:936-955,977-982`;
`Compiler/ObjectiveBendPublication.lean:36-74,141-155`; `Compiler/ObjectiveBendFrontEnd.lean:84-99,221-280,304-330`.
1. `decodeStored` (framed `List UInt8` decode of the package cell), then `drawQuote` → `frontEndQuote`, which runs
   `decodeStored` again plus an artifact decode and a package decode.
2. `replayPackage`:
   - a third artifact decode and a second package decode;
   - **`identity artifact`** (re-encode the artifact, then cSHAKE it) and **`identity package`** (re-encode, then cSHAKE);
   - `selectedDeclaration`;
   - `replayAccept` = `parsePackage`. Per module this is a UTF-8 decode, a parse to a `Json` AST, `Sha256.hex` of the
     source, and an import transcript compared by **`Json.compress` on both sides**.
3. `lowerParsed` of the entry (**elaboration #1**).
4. `accept`:
   - `l.proposal`;
   - `l.packet` = `proposalJson` + `packetJson` **again** (`Lowering.packet` is a `def`, `FrontEnd.lean:264`: it is
     recomputed at every use);
   - `decodePacket`, then `check` (**checker #1**).
5. **`lowering.packet.compress.toUTF8.toList = typedCore`**: packet render #2, a JSON string turned into a `List UInt8`,
   compared bytewise against the stored core. Then laws are compared.
6. `methodOf`:
   - `lowerParsed` of the method (**elaboration #2**);
   - `accept` (proposal ×2, **packet render #3**, decode, **checker #2**);
   - `check applied [] typeFuel` on `view args` (**checker #3**: the only step that depends on the request);
   - two `labelsWithin`.
7. `generatedCore` = **`m.lowering.packet.compress.toUTF8.toList.length`** (`ObjectiveCall.lean:415-419`): **packet
   render #4**, done only to measure a length for the meter.

So one L does 2 elaborations, 6 `proposal` computations, 4 packet renders, 2 compress-to-`List UInt8`, 2 packet decodes,
3 checker runs, 2 artifact/package identity cSHAKEs, a SHA-256 per module and 3 decodes of the stored pair.
**Every input except `view` and `args` is a function of the pin.** The pin is content-addressed, and the cell holds only
an artifact this kernel replayed at publish (READ `ObjectiveActivity.lean:1077-1082` docstring; `publish` at
`decideTurn` `.publish`, Core:556-558). The term is O(S) for parsing, superlinear for elaboration (the measured rate is
0.78 µs/B at 91 KB and 1.9 µs/B at 256 KiB, READ `activity_world.py:33-38`), plus an O(core) checker.

## 2. CALL / SEND / DELIVER: what differs

- **CALL (granted).** The root frame yields `.call` → `exec .enter` for the callee → **a second `loadMethod`**
  (`ObjectiveCall.lean:1134`). This happens even when the callee pins the **same package**: there is no per-turn memo
  keyed by pin. Grant lookup is `spendGrant` over `journal.grants` with the callee's `activePin` as the code digest
  (`:782-800,1094-1103`). It is a short linear list, and `Grant.judge` compares digests and checks `ArgsBound`, all
  DERIVED cheap. The extra work is `typeData` of the returned value (`:1170`), a second `touch`, a second state post,
  and `judgeDomains` over 2 objects.
- **SEND.** `Mail.send` → `deliverable` → **a `loadMethod` of the TARGET's method at send time** (`:1409`; theorem
  `Mail.send_object_deliverable` `:2133-2150`). The same replay runs again at delivery (`ObjectiveSend.runMessage` →
  `exec`, `ObjectiveSend.lean:99-104`). The inbox is generation-addressed. `holdInbox` reads the pair cursor
  (`readInboxGeneration`, `ObjectiveActivity.lean:1552-1562`), then one inbox cell (`ObjectiveCall.lean:1296-1318`):
  **O(1), no scan** (DERIVED). The cost is a constant: `inboxCell …` is recomputed 3× in `holdInbox`, each time a
  cursor decode plus a coordinate cSHAKE.
- **DELIVER (`deliverMessage`).** A cursor read, an inbox read, `runMessage` (1 `loadMethod`), a slot close and Book
  postings (`ObjectiveSend.lean:375-428`). It is not an invoke, so the driver runs no front-end probe: **one** mini
  process (READ `activity_world.py:325-328`, quoting only for `kind == invoke`).

DERIVED consistency check with the MEASURED p50s (task brief). Let P = per-process fixed cost, D = per-decision cost
excluding loads, L = one load.
- UPDATE = 2P + 22(D+L) ≈ 6 s.
- CALL = SEND = 2P + 22(D+2L) ≈ 8 s, so **L ≲ 2 s / 22 ≈ 90 ms ≈ 1.3 G instr per load** (at the measured
  ≈15 G instr/s, i.e. 90 G / 6 s). The bound holds because the CALL/SEND extra also includes a second post and frame.
- DELIVER = 1P + ~11(D+L) + delivery ≈ 5.5 s. That fits P being large: consent start, codec execs, image hash and
  [TAIL] refreshes.

INFERRED split of the ≈90 G UPDATE:
- **≈30 G (~1/3)** goes to the 22 front-end replays.
- **≈15–25 G** goes to the other per-decision work for 22 decisions: run, extraction, Book decode ×2, `judgeDomains`,
  coordinate cSHAKEs and closure-chain lookups.
- **≈35–45 G** is per-process and [TAIL]: two consent cold starts with Store open and root, 7 refreshes, commit, 5
  codec execs, 2 image hashes.
- The serving Host has no per-request profile yet (it runs from a memfd, SHOULDNT §B2), so this split is a derivation,
  not a measurement.

## 3. TOP FIVE constant-term offenders

**1. The plan decides the turn five times, on both sides. LOCAL.**
- `activityPlanLoaded` (`NativeHost.lean:2350-2365`) calls `signingHeader` (→`planOutcome`), `planReport`,
  `planOutcome`, `planVerdict` and `planFrontEnd`. Each one re-runs `configOf` + `decideTurn` (+`finish` ×3), and the
  compiler cannot CSE across these separate top-level functions (DERIVED).
- The consent provider re-runs the identical function (`NativeSpecializedConsent.lean:81-83`).
- *Should not do at all because* all five are projections of one `Except Reject (Decided …)` and one `finish` result,
  over the same snapshot, height and command.
- *Elimination:* one `planOf : … → Plan` that decides once and projects `outcome/report/verdict/frontEnd/header` from
  that one value. Keep the five defs as `theorem planX_eq : planX … = (planOf …).x` so every downstream statement keeps
  its form. **This cuts 10 decisions to 2 per mini process, i.e. 20 → 4 decisions and 20 → 4 front-end replays per
  UPDATE.** It touches no persisted bytes.

**2. Every frame load re-runs the whole source front end of a content-addressed, already-replayed package.**
LOCAL part + DESIGN part. (READ §1 "Within one `loadMethod`".)
- *Should not do at all because* the replay is a pure function of `(pin, method, typeFuel, maxArtifactBytes)`. The pin
  is the artifact identity, publish already established `Replayed`, and only `check applied` depends on the request.
  Inside one turn it is not even memoized: a CALL into the same package, or a SEND's deliverability check, replays again.
- *LOCAL eliminations:*
  - (a) make `Lowering.packet` / `proposal` a computed field (or `let` it once in `replayAccept`, `accept` and
    `methodOf`), which removes 3 of 4 renders and 4 of 6 proposals per load;
  - (b) get `generatedCore` from the render already compared, not a fresh `packet.compress…length`;
  - (c) memo `(pin, method) ↦ Method-sans-applied` in the call `Journal`/`Mail` for the turn;
  - (d) drop the redundant `decodeStored`/`frontEndQuote` re-decodes.
- *DESIGN elimination:*
  - Accept the stored typed core once at publish.
  - At invoke, load `(accepted source, annotations, laws)` from the pinned cell, checked by identity only (the pin
    already commits the core), or from a process-level `pin ↦ Replay` cache whose refinement theorem is
    `replayPackage` itself.
  - This reverses the stated choice "the typed-core bytes are a commitment it compared, never a value it parses"
    (`ObjectiveBendPublication.lean:12-14`). That is Ember's call; it is a semantics decision, not a perf trick.
- Payoff: ~1/3 of the UPDATE (INFERRED), and ~half of CALL/SEND.

**3. An invoke is planned in two separate cold client processes (probe + submit). DESIGN; LOCAL on the client side.**
- `activity_world.py:337-387` runs a full `submit --prepare-only` to read `frontEnd`, then a second full submit.
- That doubles everything per process: rows 2–8, including a consent cold start and 10 decisions.
- *Should not do at all because* the front-end draw is fixed by the pins: each load draws the pair's quote (source,
  stored core) plus (source bytes, generated core). Op 214 already publishes `pins[].frontEnd`, "so a client declares it
  and never probes" (READ `ObjectiveActivity.lean:977-982` docstring). The one unpredictable term is `generatedCore`,
  the length of a method's re-render.
- *Elimination:*
  - DESIGN: meter the method lowering by the stored quote (as the entry already is), so the envelope is computable from
    op 214 alone.
  - LOCAL interim: do probe and submit in **one** mini process, so the consent provider, image hash and codec session
    are shared (`client_consent.rs:84-91` already keeps one provider per process).

**4. Each CLI process cold-starts a consent provider that re-plans and re-admits by full re-execution. LOCAL for
warmth, DESIGN for the rest.**
- `client_consent.rs:76-91,107-127` spawns `minidregg-client-consent stdio` per mini process. It checks the Store
  against the anchor and re-validates the image at the anchor ([TAIL] root).
- It re-admits every record after the anchor through `admitDecodedNative`. That is the full gate (with row 9b's
  whole-world directory), decide, front-end replay and CheckedCommit (`NativeHostReplay.lean:2341-2349,2943-2947`).
- Then it re-runs the 5-decision plan (offender 1). MEASURED: consent processes = 24% of all workload samples
  (SHOULDNT §Workload).
- *Should not do per request because* the anchor already pins the admitted prefix, and the provider is torn down with
  the process (`impl Drop for Session`, `:36-41`), so its warm frontier is thrown away every CLI step.
- *Elimination:*
  - LOCAL: a long-lived provider per (binary, settings) binding, beside the Host socket, offered the same anchor.
  - DESIGN: "client re-executes what the server executed" is the trust model (no proof system; memory
    `project-no-proof-system-in-mini-admission`), so the re-admission itself stays until a proof carrier exists. What
    can go is the *per-process* repetition.

**5. `gate` decodes the whole world into a directory the Objective kernel never reads. LOCAL.**
- `ObjectiveActivityReceiverCore.lean:818` runs `loadDirectory durable`, which is
  `DirectoryImage.decode registry (durable.cells …)`: every cell id, a closure-chain lookup each, and a decode of every
  cell's bytes (`CredentialAuthorityDomainReceiver.lean:288-307`, `DurableReceiverCore.lean:851-853`).
- The result is stored in `Gated.directory`/`Prepared.directory` and **read nowhere** on the Objective path (DERIVED:
  `git grep 'prepared\.directory\|gated\.directory'` hits only Certify/ShareIssue/AgentLifetime, never `Objective*`).
- It runs once per admission, on the server and on every consent re-admission.
- *Should not do at all because* it is a whole-world scan whose only effect is the `directoryUnavailable` refusal when
  some unrelated cell fails to decode.
- *Elimination:* delete the field and the call. `gate_spent_refused` (`Core:901-911`) loses its `dir` hypothesis, which
  weakens a hypothesis and strengthens the theorem. Term removed: O(cells·(k + cell bytes)) per admission.

Runners-up, all LOCAL:
- (6) CheckedCommit executes the intent twice: `Proposal.check`'s `Installs (execute …)` and then
  `DurableCheckpoint.prepare` in `receiveCandidateWithFresh`. Fix: hand the checked execution to the writer. Separately,
  `turnOf`'s deltas are recomputed per field: compute `deltas` once.
- (7) `DecodedIngress.bytes` re-encodes the ingress for every `event`, `receipt` and `charge .turnBytes` query
  (`Core:426-427,917-936`). `charge` is a closure, so each lane query re-encodes. Fix: keep the received bytes.
- (8) `configOf` re-decodes the policy (~7×/plan); the command is re-encoded and re-hashed per capability check.
- (9) mini SHA-256s the 173 MB Host image per process (`main.rs:483-541`); cache by inode identity on disk.

## 4. What the SINS ledger (`SINS-LEDGER-20261009.md`) did not name

The ledger is about data structures, encodings, caching, twins and gates in the durable/shared layer. It names none of
the judgment layer's per-request repetition:
1. **Five decisions per plan, ×2 sides** (offender 1). This is invisible to a data-structure audit: it is the same
   pure function called five times.
2. **Front-end re-elaboration per frame load per decision**: 4 packet renders per load, a JSON render to measure a
   length, and no memo across frames, sends or decisions (offender 2). The ledger's E/C sections never mention the
   front end.
3. **The invoke probe protocol doubles every client process** (offender 3). The ledger's D6 counts 3 Hosts for
   `workspace create`. It does not see that `activity submit` for an invoke runs twice, or that each run spawns a
   consent provider.
4. **The consent provider as a per-process re-planner** (offender 4). The ledger has no consent entry. SHOULDNT names
   its 24% share but not the cause: the 5× plan plus re-admission per cold start.
5. **The OB gate's unused whole-world directory decode** (offender 5). The ledger's D2/C3 list `entriesOf`, `rootTable`
   and `cellIds` but not `loadDirectory` on every admission.
6. CheckedCommit's double execute and delta recomputation. Ledger T10 says CheckedCommit "is not on main": stale, it
   is (`ObjectiveAdmissible.lean:117-133`, used by `DurableReceiverIO.receiveObjective:274-281`).
7. The client's per-process 173 MB image SHA-256 (runner-up 9).

## 5. Checked and NOT offenders (DERIVED)

- Inbox after kern-pole: cursor → one generation cell, O(1); nothing is scanned for the next id.
- `judgeDomains`: only touched objects' domains and touched domain cells, deduplicated and metered (`domainWork`).
- Laws: once per frame write over one object's slots (`ObjectRecord.judge`), once per touched domain (`judgeJoint`).
- Grants: a linear `find` over the request's own grant list, comparing digests; no world lookup, no signature re-check.
- No `decide`/`native_decide` census at request time. Runtime `Decidable` (`PhysicalShape`, `ofCells` Nodups) is over
  a handful of writes.

## 6. Toward >100×: the honest arithmetic

- Offenders 1+3 alone take an UPDATE from ≈22 decisions to ≈2 (one plan, one admission), and from 2 client processes
  to 1.
- Offender 2 (DESIGN) makes each decision's load ~O(check applied) instead of a full front end.
- Offender 4 (warm provider) and offender 5 remove the remaining per-process and per-admission whole-world work.
- INFERRED: that is ~5–10× on the judgment layer. The remaining ~35–45 G is [TAIL] (cold opens, root, refresh,
  commit). **>100× needs both:** the judgment layer's work done once per pin and once per turn, *and* the tail's root and
  open done once per process (ledger sin 1).
- First measurement to take: `perf record` of the serving Host run from a file path, not the memfd (SHOULDNT §B2),
  sorted by `ObjectiveBendElaborate.elaborate`, `Lowering.packet`, `Json.compress`, the checker, `decideTurn` and
  `loadDirectory`. It would confirm the replay and decision counts.
