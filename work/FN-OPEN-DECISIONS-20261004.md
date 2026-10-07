# fn 6.6.0: open decisions (2026-10-04)

A decision document for ember and an outside reviewer. It is self-contained: no repository access is needed. Each section gives the context, the options with their costs, the swarm's recommendation, and the questions worth pressing on. The swarm's recommendations are positions, not conclusions; argue with them.

## Background: what fn is

**What it is.** fn ("formal news") is an NNTP news server whose every decision is made by a function in ACL2, the theorem prover. The ACL2 *books* hold the decisions, and their theorems are mechanically checked. A thin host layer in Common Lisp (SBCL) does the I/O and calls those functions.

**How it stores.** The store is an append-only record log plus checkpoints. Articles are exact bytes, signed and identified by a BLAKE3 digest.

**Why it matters now.**
- Version 6.6.0 is the release that is "good enough to start treating as a foundational component for the rest of the distributed OS / Mini" (ember, decision D49). Mini is a sibling system written in Lean that will use fn as its archive, its feed and its inter-domain transport for exact bytes.
- fn also has its first external collaborator, who runs their own news server and wants to peer with ours.

**House rules that shape every option below:**
- **Accepted, refused and uncertain stay distinct.** A client must never be told "accepted" for something that may not survive, and an uncertain outcome is never reported as a refusal.
- **Durable acceptance comes only from persisted state.** An acknowledgement means the bytes are on disk.
- **No ceilings on stored data (D27).** Limits are profile parameters, derived from the store's declared size. Exceeding one is refused *by name*, never by silent truncation.
- **Decisions live in ACL2.** The host may not decide anything a theorem should cover. A *keystone* is the theorem a capability rests on. It must be stated about the function the host actually calls, and it ships with *teeth*: witnesses that it is not vacuous, and that it fails if any hypothesis is removed.
- **Replacement, not reverts.** A theorem that is temporarily bypassed becomes a named "proof-owed" item rather than a blocker.

**Where things stand.** Current source certifies whole, and the first current-source images exist. Seven of the 12 core native test modules pass; the rest are classified and owned. Several decisions below are blocking merges or redeploys.

---

## 1. RL-01: recovery after a failed write barrier

**The defect.** Found by reading the code; not yet reproduced.
1. A batch of posts is appended to the active log segment and its `fdatasync` fails (EIO).
2. fn does the right first thing: it fences the store, and the process exits without acknowledging anything in that batch.
3. systemd restarts it. Recovery reads the segment with `read(2)` and validates the records.
4. **The trap:** on Linux, failed writeback pages are marked *clean* and stay in the page cache. The error is reported once, then forgotten. This is the 2018 "fsyncgate" behaviour that PostgreSQL redesigned around. Recovery therefore finds the failed batch, valid, in cache, and treats it as committed history. Because the pages are clean, no later barrier will ever write them.
5. The node serves those articles and appends new batches after them. Those batches are **acknowledged** with good barriers.
6. **Power loss.** The disk holds garbage or zeros where the failed batch "was", followed by valid acknowledged batches. The next open refuses with `log-damaged`. The only repair, truncate at the hole, **drops acknowledged entries**.

**Where else it appears.**
- Peer feed journals have the same pattern.
- Checkpoint read-back verification reads from cache, so it verifies the encoder, not the disk.

**Exposure.** It needs a device write error, an automatic restart and then a power loss. That is rare, but it is exactly the case barriers exist for. The release targets are Linux on ZFS and ext4, plus OpenBSD, so the fix should not depend on Linux-specific cache control.

**Options:**

| | what | for | against |
|---|---|---|---|
| **A** | On every open, rewrite in place the bytes recovery just validated below the frontier, then `fdatasync`. | OS- and filesystem-agnostic. Provable: "after recovery, every octet below the frontier was written by this run before its barrier." If the device is still failing, the barrier fails again and the node fences again, which is correct. | One extra write of the active segment per open, bounded by segment rotation. The recovery program gains a step (the identity on the byte model). |
| **A′** | Like A, but only after an unclean stop. | Saves the write on clean restarts. | Needs a reliable "previous run was unclean" signal. Writing that marker is itself a disk write that can fail the same way. More states to prove. |
| **B** | Read with O_DIRECT, bypassing the cache. | No extra write; exact. | Not on ZFS before 2.3, not on OpenBSD, plus alignment rules. A fallback is needed anyway, so it becomes A plus complexity. |
| **C** | `posix_fadvise(DONTNEED)` before recovery. | Cheap. | Advisory only. ZFS's ARC ignores it; it isn't on OpenBSD. Nothing to stand a theorem on. |
| **D** | Document it: a device error requires operator restore. | No work. | Acknowledged data can be lost after an automatic restart, which contradicts the core promise. |

**UPDATE (later the same day): option A as written is unsafe under fn's own crash model.** The lane wrote the keystone first and found a counterexample before writing any code:
- **The crash model.** fn's byte-level crash model lets every unit of a pending write land as old, new, zero or garbage. A failed fsync also lands a torn selection.
- **Why the current design is safe.** Nothing is ever written below the frontier: the durability invariant requires every pending write to sit at or above it.
- **Why A breaks that.** A deliberately rewrites the acknowledged prefix in place. A crash *during the rewrite* can zero or garble a unit that holds acknowledged records.
- **The ground witness.** Three records acknowledged; restart; A's rewrite of the first 168 octets; a crash that zeros the first 4-octet unit. The next open recovers 0 records instead of 3.
- **The open problem.** "M1 across restarts" is false for A. The ok-outcome half of the keystone (if the rewrite and its barrier succeed, the prefix is durable) still holds; only the crash-during-rewrite cuts break.

Three ways to make it provable:

| | what | for | against |
|---|---|---|---|
| **A1** | A plus a named device assumption: a write whose octets equal the durable octets lands each unit as old or new, never zero or garbage. | Small. Plausible on ZFS (copy-on-write, checksummed, never overwrites in place) and for in-place overwrites of already-allocated blocks on ext4/xfs, where zero-fill is a delayed-allocation effect on *new* blocks. | An assumption on the label: fn's claims are designed to carry none. A power cut mid-overwrite can still leave a sector unreadable (a media error), losing acknowledged records even where "old or new" otherwise holds. |
| **A2** | Never write below the frontier. Copy the validated prefix into a fresh (spare) segment, fsync it, then switch atomically with rename plus a directory fsync. | Keeps the invariant that made M1 provable; no new assumption. The same write volume as A. The spare-segment machinery already exists. | Touches segment rotation and lineage (the new segment's identity and first entry change), and M1 currently excludes rotation. More work; the size estimate is pending. |
| **B** | O_DIRECT re-read, with A1 as the fallback. | No write. | Platform-specific, as above, and inherits A1's assumption where unavailable. |

**Updated recommendation: A2.** Its cost is the work of bringing segment switching into M1's proof, which 6.6.x wanted anyway. If A2 proves too large for 6.6.0, the honest fallback is A1 with the assumption *named on the label*, not silently. The lane is proving the ok-outcome keystone and sizing A2, and won't implement either until this is decided.


**UPDATE 2 (evening): A2 designed and sized, with the external review folded in.** Full text: fn `build/coordinator/lanedumps/m1-durable.md`, sections "A2 design" / "A2 design v2".
- **Mechanism.** The open validates and copies in one pass into a fresh staged inode (`staging/.stage-recover-K`): the validated prefix, then zeros. It fsyncs that file, `rename(2)`s it over `journal/K.log`, and fsyncs the directory before anything in K is acknowledged.
  - The old inode is never written, so the invariant that made M1 provable holds.
  - Segment index, bytes, lineage, genesis and checkpoint rows are unchanged; only the inode changes.
  - It needs a new rename-with-replace primitive, a sweep of staged names, and a temporary-disk reserve. Without that reserve, the open refuses by name (`:recover-copy-no-space`).
- **Model gap confirmed and designed.** A wrapper adds a "clean but not durable" cache state, with exit / evict / lose-cache transitions, so both the RL-01 trace and every interruption of the repair are expressible.
- **Rotation at open: confirmed reachable.** It is reachable in any M1 deployment, because automatic checkpoints rotate. So M1 needs the argument, not a non-reachability claim. That argument falls inside A2's scope.
- **Dependency set.** Closed segments are safe. Checkpoint-name durability ordering and config/profile fences are being verified now. FNFD feed journals are the same class and may want their own lane.
- **Containment, done.** systemd `RestartPreventExitStatus=3` on fence exits. Remaining gap: launchd restarts on any failure.
- **The native.** The page cache controls what recovery reads; dm-flakey under the dm-log-writes rig controls what survives. EIO-only and kill-only controls must stay green. Risk: the first write into unwritten ext4 extents may abort the journal instead of producing the clean-cached state.
- **Size.**
  - Full "M1 across restarts": the cache model, A2, the epochs theorem, complete-rotation, restating the open's theorems, the dependency set, host, native and cost. About **12–14 lane-days**.
  - Smallest shippable slice: the cache model plus A2 for the log, two keystones and the native. About **7–8 lane-days**.
- **Already landed (common to every option).** Any read content O with a durable read prefix and a zero tail establishes the recovery relation. It is proved; certification is queued.
- **The question for ember.** A2 now, at 7–8 lane-days for the log slice, with the rest after? Or A1 with the named assumption for 6.6.0, and A2 in 6.6.x? Nothing starts until this is decided.

~~**Recommendation.** A, for the log and the peer feed journals.~~ *(superseded by the update above)*

Original recommendation, kept for the record: A, for the log and the peer feed journals. Relabel checkpoint read-back honestly as an *encoder* check. On-disk verification then happens at the next open, under A.

**Status (superseded, see the update above).** A lane was to build A behind a single switch, statement-first. It extends the newly certified "durable after acknowledgement" theorem (M1, §5) across a failed barrier and restart, with a native test that injects barrier failure, restart and simulated power loss. It will measure the worst-case open-time cost on the largest preset. Nothing merges until this decision is made.

**Questions to ponder:**
- Is "one extra write of the active segment per open" acceptable as a permanent cost? Segment size is bounded by rotation, but rotation is out of 6.6.0's M1 scope (see §5).
- A′'s marker problem: is there a marker that can't fail the same way? For example, absence-based, as in "a clean shutdown deletes a file".
- Should the node, after a fenced barrier failure, refuse to auto-restart at all (exit code → systemd `RestartPreventExitStatus`) and require an operator? That is safer and less available.
- Does the same reasoning apply to directory fsync after segment creation? (A related fix already landed: a failed directory sync is never retried; the store fences and reports uncertain.)

---

## 2. RL-02: a checkpoint that fails early never releases its slot

**The defect.** A checkpoint publication marks itself in flight, then fails before producing a result. The cause is either an "unencodable" history verdict or a history row refused by name. The step that clears the marker runs only on the success path. For the rest of the run:
- no automatic checkpoint happens;
- every manual compact or checkpoint answers "coalesced";
- reclaim is refused as "in flight";
- the record log grows without bound;
- the next open replays the whole suffix and may hit the same refusal.

Serving continues and a log line says "CHECKPOINT auto failed", so in practice it is silent until the disk fills.

**Options:**

| | what | for | against |
|---|---|---|---|
| **A** | Release the slot on any early failure. | Trivial. | The due rule re-arms on every count change, so every POST triggers a full history walk plus rotation plus the same refusal: a work storm. |
| **B** | Release, plus a *blocked* deferral that stops automatic checkpoints until the operator acts. Health shows it. | No storm; visible; the operator decides. | An unattended node stops checkpointing while the log grows. |
| **C** | Release, plus bounded exponential backoff (by commits or time, capped). | Self-heals transient refusals. | A permanent refusal retries forever (bounded, but forever). |
| **B+C by reason** | Classify the refusal in ACL2. Transient reasons (e.g. a suffix still in flight) get C. Permanent ones (e.g. unencodable) get B plus a health alarm. | Matches the two kinds of failure. | The classification must be decided and proved; it is a decision, so it belongs in ACL2 anyway. |

**Recommendation.** B+C by reason. Add a liveness keystone, "every captured publication releases its slot", which the code lacks today. Add a health line naming the deferral and its reason. A permanent refusal means history fn cannot encode, which is a bug, so it should be loud. Roughly a day for one lane.

**Questions to ponder:**
- Is there any refusal that is truly permanent, or is "permanent" really "permanent until the code changes", in which case B is just "page the operator"?
- Should a node whose log is growing with checkpoints blocked eventually refuse new posts by name (a budget), rather than fill the disk? D27 suggests yes. That would be a third leg: a log-growth budget.

---

## 3. Live reclaim: who pays for the memory?

**Context.** Reclaim removes superseded or expired content. Offline reclaim exists and works. *Live* reclaim, while serving, is new since the last release. It builds a whole second copy of the in-memory store (store, catalog and history columns) and swaps it in. That copy is proportional to the store. It shrinks only once pages become the state, a later stage (D41 stage 5).

**The design built.** A design lane chose and implemented this; five keystones are certified.
- The launcher reserves an **owner's work reserve** up front, sized as the larger of the open's transient demand and the live pass's demand at the profile's bounds. Open and live reclaim never run at the same time, so one reserve covers both.
- The pass borrows the reserve and returns it, and user requests never draw on it. Live reclaim is therefore guaranteed at every fill level.
- Rejected alternatives: a completion reserve alone (the launcher sizes from the store on disk, so the pass would draw memory the process never got); and room in the store budget (live reclaim would be refused above about half full, exactly when it's needed, and POSTs would be refused while a pass runs).

**The cost, if every node pays.** Heap at the profile's bounds; "excess" is what `init` must additionally promise:

| profile | open at bounds | live-pass demand | extra `init` must promise |
|---|---|---|---|
| small floor (8 MiB, T 16,384) | 130 MB | 358 MB | +228 MB |
| 16 MiB (T 32,768) | 180 MB | 705 MB | +525 MB |
| 32 MiB (T 65,536) | 281 MB | 1,400 MB | +1,119 MB |
| 64 MiB (T 131,072) | 482 MB | 2,789 MB | +2,307 MB |
| scale (T 4,096, 768 MiB) | 2,783 MB | 9,736 MB | +6,953 MB |

Consequences:
- On a 2 GiB machine, `init` picks one rung smaller (8 MiB where it got 16 MiB).
- On 3 GiB: 16 instead of 32.
- Deployed nodes' MemoryMax must be checked before a redeploy.

**Options:**
- **As built: every node pays.** Live reclaim is guaranteed everywhere, in line with D27 ("full-store maintenance").
- **Opt-in.** Same mechanism; the reserve exists only when configuration asks for live reclaim. Without it, live reclaim is refused by name (as 6.6.0 answered "offline-only") and offline reclaim remains. Needs a config field. Small machines keep their capacity.

**Lean.** Default-on for the public and home nodes, which have room and should showcase 6.6.0 as a foundation. Ship the opt-out key for small machines.

**Questions to ponder:**
- Is a 2–7× memory premium for live reclaim reasonable when the representation (not the algorithm) is what makes it expensive? Or should live reclaim wait for D41 stage 5 and stay offline-only in 6.6.0?
- Is "guaranteed at every fill level" the right promise? The alternative is "best effort, refused by name when the reserve isn't held".
- Mini uses fn as an archive of signed, never-reclaimable articles. Does Mini's use even need live reclaim?

---

## 4. S025: which reason code ends an idle incoming DTN session?

**Context.** fn also speaks Bundle Protocol over TCPCLv4 (RFC 9174) for delay-tolerant networking. An *incoming* TCPCL session that completed setup but makes no transfer progress can hold a slot forever, while the incoming pool is full.

**The design decision.** Such a session is terminated after `passive-ms` (proposed 120 s) of no transfer progress, but only when the incoming class is at capacity.
- *Progress* means a segment received or an ack sent; keepalives don't count.
- A session mid-transfer is never expired.
- The pool is re-checked when the timer fires.

**The open choice:** which SESS_TERM reason code (RFC 9174 §6.1, Table 9)?
- **3, "Busy"** ("the entity is too busy to handle the current session"). One external reviewer's pick; it describes the node's state.
- **5, "Resource Exhaustion"** ("the entity has run out of some resource"). The other reviewer and the lane picked this, because the trigger is a full pool.

**Lean.** 5. It's a small call.

**Question to ponder:** what will peer implementations (e.g. DTN7, µD3TN, HDTN) do differently on 3 vs 5? Is either treated as "retry later" versus "back off hard"?

---

## 5. Mini's 6.6.0 requirements: three decisions

**Context.** Mini listed eight must-haves for fn 6.6.0, M1–M8:
- M1: durable-after-ack on the commit the node serves.
- M2: served bytes equal stored bytes.
- M3: idempotent resend on every post path.
- M4: an identity command.
- M5: grammars exported from ACL2 with round-trip theorems.
- M6: an opaque application article kind.
- M7: the remote consumer.
- M8: a qualified release image with fundamentals re-measured.

fn's response and Mini's root agree on all three decisions below. Ember's sign-off is what's missing.

1. **M2, served = stored, moves to 6.6.x.** The real proof (the captured read path refines the reference reader) is 5–10 lane-days. Meanwhile Mini's authority is its own self-checking content identity plus its record of acknowledged Message-IDs.
2. **M1 excludes log segment rotation.** This is conditional on history-budget exhaustion refusing *by name*, with 6.6.0 stating Mini's maximum archive span at the shipped budget.
   - **Update:** M1 is now certified. At every crash point, the records acknowledged are exactly the records recovered. It is stated over the server's real log operations under any outcomes, with no unestablished hypotheses and one removal witness per hypothesis.
   - A distinct `:history-exhausted` refusal word is being built.
3. **Codec boundary.** Mini decodes fn's control frames and cursor *directly*, from an exported grammar file:
   - grammars are data;
   - one ACL2 interpreter carries both round-trip theorems;
   - Mini writes one Lean interpreter of the same language.
   Mini adopted this format with five requirements: canonical encodings, a decidable constraint fragment, wrong-trailer vectors as a named refusal, versioned vectors, and byte-exact refusal and uncertain vectors.
   The opaque article kind (M6) is done and proved.

**Question to ponder:** is leaving served = stored (M2) out of 6.6.0 compatible with D49? Mini would treat fn as a foundation without a proof that it serves back what it stored, relying on content digests instead.

---

## 6. Also yours, smaller

- **Competing consumers with leases** (zmq-style push/pull where workers compete for messages) need new owner state, which collides with D46. Proposed: outside 6.6.0. Pub/sub, pair, fixed-worker push/pull and req/rep are in.
- **Redeploy timing.** Both public nodes run the 09-28 source with known hangs. The plan is to redeploy from the first image whose natives are green, and the first external peer meets the redeployed node.
  - A store-format change since 09-28 probably means initializing fresh rather than migrating.
  - Separately, the redeploy was blocked by a node that could not start current source at the installed launcher's heap. That is fixed and pending an image.
- **Native tests** now start nodes exactly as an installed node starts (the launcher's decided heap), not at a generous fixed heap. That would have caught the startup blocker. About 18 test setups must move off a profile no real launcher can start.

## 7. Calls the swarm already made on ember's behalf (for review, not blocking)

- **Refused-offer memory is per peer.** A refusal that depends on one peer's bytes no longer blackholes that Message-ID for every other peer. The keystone: one peer's offer never changes another peer's answer.
- **Push-feed "try later" never drops an article.** Deferrals and connection losses are counted separately. A dropped entry releases its queue capacity immediately.
- **An oversized log record is refused at submission by name**, with no log-format change. This closed M1's last open hypothesis.
- **The tariff pass-through is removed only when the last of 30 kinds is priced**: 25 command families plus 5 non-command input kinds. Today 4 of 30 are priced.
- **`:step-of` interface vocabulary.** A host entry that runs one step of a fold may cite the fold's keystone. It is displayed as "keystone via fold; host-loop correspondence owed", never as proved.
- **Read-only entries** need no vacuous preservation theorem, but still owe the guard bridge.

---

## Summary of what is being asked

| # | decision | recommendation |
|---|---|---|
| 1 | RL-01 recovery after a failed barrier | **A2** (copy the prefix to a fresh segment, switch atomically); A as written is unsafe; A1 only with its assumption named on the label |
| 2 | RL-02 stuck checkpoint slot | B+C by reason, with a liveness keystone |
| 3 | live reclaim reserve | default-on for the public and home nodes, opt-out key for small machines; or offline-only until D41 stage 5? |
| 4 | S025 reason code | 5 (Resource Exhaustion) |
| 5 | Mini: M2 → 6.6.x; M1 without rotation; direct codec | yes to all three (Mini agrees) |
| 6 | competing consumers outside 6.6.0 | yes |
