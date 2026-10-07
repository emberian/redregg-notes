# External review of FN-OPEN-DECISIONS-20261004 (GPT-6, via ember, 2026-10-04)

This review is verbatim. It was written against the *first* version of the decision doc, before the RL-01 update about A being unsafe; it reached the same counterexample independently. The reviewer read public fn at `65389a90e601` and did not certify anything. Its claims about the repo are observations to check, not facts.

---

I agree with much of the direction, but I would not sign off on RL-01 option A as written. There is a crash-safety objection to the proposed in-place rewrite that matters more than its startup cost—and the existing byte model already contains the ingredients to exhibit it.

I reviewed the decision packet and selected implementation, model, proof, and deployment-status files at public revision `65389a90e601`, dated October 4. This was a source review, not an independent ACL2 certification or native qualification run; I treat the packet's newer certification and lane-progress statements as reported, not reproduced.

| Decision | My recommendation |
|---|---|
| RL-01: failed-barrier recovery | Reject unconditional in-place rewriting as presently justified. Develop non-destructive re-materialization, with crash-safe publication and an explicit cached-versus-durable model. Preventing automatic restart after a known storage fence is useful interim containment. |
| RL-02: checkpoint slot | B+C by reason, plus token-specific settlement, explicit retry triggers, and a log-growth budget that preserves maintenance headroom. |
| Live reclaim | Keep the guaranteed-reserve mechanism, but make the capability explicitly selectable by mission/profile. Do not make every archive pay. Enable on the two deployments only after checking their actual limits. |
| S025 | 5, Resource Exhaustion, for this pressure-triggered policy. The larger issue is whether a stalled, already-started transfer can retain a slot indefinitely. |
| Mini's three decisions | Exported grammar: yes. Rotation exclusion: only with enforceable scope boundaries. M2 deferral: conditionally acceptable as a checked composition, not as an equivalent durability/readback guarantee. |
| Competing consumers | Defer. Their lease and recovery semantics deserve their own design rather than entering through an ostensibly small interface extension. |

## 1. RL-01: the proposed repair can endanger previously durable data

### The original failure is credible; the repair argument is insufficient

The packet correctly distinguishes a process restart from a power loss: recovery may read bytes that remain visible in the kernel cache but were not persisted. PostgreSQL's current documentation explicitly warns that retrying a failed synchronization can appear to succeed despite lost data, and defaults to stopping rather than trusting that retry. That supports taking this failure class seriously; it does not establish identical behavior on every target filesystem.

But option A proposes rewriting all validated bytes below the frontier in place, including bytes belonging to previously acknowledged records. Its justification concerns what is true after the rewrite and barrier succeed. It does not establish what remains true when recovery itself crashes during that rewrite.

Counterexample shape:

```text
A is durable and has been acknowledged.
The node restarts.
Recovery rewrites A's identical bytes in place.
Power fails during that rewrite.
A touched write unit becomes zero or garbage.
The formerly durable A is no longer intact.
```

This is not importing an extravagant new disk-failure model. `books/byte-store.lisp` already allows a pending write unit to survive as old bytes, new bytes, zeros, or arbitrary garbled bytes. Nothing in those selectors exempts a write because its intended value equals the previous value.

More importantly, `books/store-log-durable.lisp` explains exactly why the current committed-prefix argument works: committed records lie below the frontier, and pending segment writes start at or above it. Rewriting below the frontier removes that protection.

Logical idempotence is not crash idempotence. An operation can be the identity when completed and destructive when interrupted.

This objection would change under an appropriately strong, qualified platform guarantee about rewriting identical sectors. But that would be a new assumption to name and defend—not a consequence of the existing model, and not a portable default for the targets in the packet.

### There is also a model gap precisely where this defect lives

In the byte-store implementation I inspected, the visible view is constructed from durable tables plus pending operations. A failed `fn-bs-fsync-file` applies a selected subset of pending writes and removes those writes from the pending list. There is no independent retained-clean-cache field in that state. Consequently, that model does not directly represent the packet's crucial condition:

> The bytes remain readable, are absent from durable storage, and are no longer dirty.

The source even explains recovery's visible/durable agreement by observing that the pending list is empty after a crash. That is appropriate for its modeled crash, but it cannot also silently stand for a same-kernel process restart after failed writeback.

I would make this distinction explicit without attempting to model an entire kernel. A sufficient abstraction could separately track durable contents, visible cached contents, and pending writeback, with different transitions for process death and loss of volatile cache.

Then require the model to express both the original RL-01 trace and interruptions of its proposed repair.

### What I would build instead

My preferred direction is non-destructive re-materialization:

Write the validated recovery image into a fresh object, establish its durability, and publish its binding through a crash-safe protocol while preserving the previous recoverable basis until publication is established.

That is a direction, not a claim that "copy, fsync, rename" automatically solves everything. The protocol still owes proofs for failed directory barriers, partially completed publication, subsequent recovery attempts, and cleanup. It also needs reserved temporary disk space and bounded streaming workspace.

The key recovery obligation should be something like:

> At every interruption of recovery—including interruptions of later recovery attempts—previously acknowledged, still-retained records remain recoverable from an old or a successfully established replacement generation.

That is stronger and more useful than "every byte was written by this run before its successful barrier."

Also inspect the whole dependency set. Re-materializing only the active log does not automatically establish the durability of a checkpoint, feed journal, or other object that recovery subsequently treats as authoritative. Relabeling checkpoint read-back as an encoder check is honest; saying the next open verifies it "under A" needs an actual argument about that checkpoint, not just the log. The packet identifies those additional surfaces but does not supply that argument.

### Answers to the subsidiary questions

The permanent write cost: possibly acceptable for a correctly proved recovery protocol. But "bounded by segment rotation" is not a sufficient release argument when rotation is excluded from M1. Measure the largest active prefix the shipped, admitted profile can actually produce, including startup latency, temporary disk demand, and repeated unsuccessful opens.

A′ and absence-based markers: a marker can be useful, but absence is not inherently trustworthy. The promising ordering is: establish a dirty marker durably before permitting mutations; remove it only after quiescence and successful persistence of everything it covers. Marker-establishment failure must prevent entry into writable service. This deserves its own failure-ordering proof; I would postpone it as an optimization rather than make it part of the first repair.

Automatic restart: yes, stop automatic restart after a known storage-fence failure until recovery is qualified. But classify that as containment. It does not solve manual restart, an unobserved earlier failure, or a stale namespace observation.

Directory synchronization: the corresponding distinction between visible namespace and durable namespace must also be accounted for. Repeating a barrier is not the same operation as reconstructing and safely publishing the required binding.

### I made the counterexample concrete

I executed a small independent Python countermodel demonstrating both the poisoned-cache trace and the interrupted identity rewrite. I also prepared an ACL2 byte-model witness using the repository's actual function names. The Python checks passed; the ACL2 witness is proposed and unexecuted. Neither is a native filesystem experiment. *(The zip was in the reviewer's sandbox; not transferred.)*

For the real native regression, insist that the harness separately controls what recovery can read and what survives loss of cache. Merely raising EIO, or merely killing the process, does not demonstrate that the relevant failure state was exercised.

## 2. RL-02: agree with B+C, but make the lifecycle precise

The proposed reason-sensitive deferral is the right direction. Clearing the stuck marker alone can turn a permanent failure into expensive work on every POST; leaving it stuck silently is worse.

Refinements:

"Permanent" should identify an invalidation condition. Rather than a permanent/transient boolean, classify failures by what can make another attempt meaningful. An unencodable history may be blocked until a code, format, profile, or history change. A dependency still in flight may become eligible on a completion event. A genuinely transient condition may warrant a timer. Ordinary POST activity must not continually reset or bypass the backoff. Time-based eligibility also matters: a backoff expressed only in successful commits can become inert after admission has been stopped to protect the remaining log budget.

Settlement must belong to the captured publication. The slot should have a publication identity, with terminal completion or cancellation settling that identity. Otherwise, a late callback from publication A can accidentally release a slot now occupied by publication B. (A review obligation, not a found race.) Two properties hide inside "every captured publication releases its slot":
- Safety: a terminal outcome settles its own capture exactly once and cannot release another capture.
- Liveness: a capture eventually reaches a terminal outcome under stated execution, I/O, or cancellation assumptions.
An indefinitely blocked physical operation cannot be wished away by an unconditional liveness theorem. Nor should logical slot release imply that memory or disk work has physically disappeared when it has not.

Yes to a log-growth budget—and reserve the means of recovery. The budget must preserve enough headroom to perform maintenance or recovery, not merely enough space for one more article. This is where RL-01, RL-02, and live reclaim meet: a recovery strategy requiring a shadow object cannot be guaranteed by a resource policy that allows ordinary traffic to consume its shadow space. For unencodable history, investigate the stronger invariant: every history admitted by the store remains representable by the checkpoint mechanism selected for that profile.

## 3. Live reclaim: retain the guarantee, stop making it universal

The owner-work-reserve mechanism is conceptually sound. Reserving the maximum of mutually exclusive open and live-pass demands is the right accounting shape provided their non-overlap is established.

Recommendation: when live reclaim is enabled, guarantee its reserve across the admitted profile. When disabled, refuse it explicitly and retain offline maintenance. Prefer that to a "best-effort" middle mode. Reducing a small node's supported archive capacity to fund a maintenance operation its owner never requested is a poor default for an archival substrate.

Deployment check: the inspected deployment record lists `MemoryMax=2G` for both deployed nodes. Check the launcher-selected profile and actual service limit together before enabling the new reserve.

Check whether the reserve accounting includes retained reader generations, writes arriving during the pass, cancellation/completion custody, and the distinction between the declared Lisp heap and the entire process's memory demand.

Does Mini need it? Not necessarily: never-reclaimable articles weaken the case for live content reclaim, but not for checkpointing, indexing, journal management or representation maintenance. Don't postpone a well-qualified capability; stop charging missions that don't need it.

## 4. S025: choose 5, but separate empty sessions from stalled transfers

For pressure-triggered eviction, 5 (Resource Exhaustion) is defensible. RFC 9174 also defines 1 (Idle Timeout) for pure idleness policy. The RFC does not establish "3 means retry later, 5 means back off hard."

dtn7-rs at `4daf02d7`: `TcpSession::receive` handles SESS_TERM by replying with the received reason and terminating both directions; no branch between Busy and Resource Exhaustion. µD3TN's official docs list TCPCLv3, not v4. HDTN unknown.

Policy gap: "a session mid-transfer is never expired" means: complete setup, start a transfer, never complete it, stay alive via keepalive → the slot is held forever. S025 solves empty-session retention, not stalled-transfer retention. Ask for a separate, configurable no-progress policy for active transfers. Make "progress" about actual transfer advancement, audit both directions; a locally queued ACK must not manufacture remote progress. RFC 9174 forbids inserting SESS_TERM inside an unfinished message.

## 5. Mini

M1 wording: "acknowledged records are exactly recovered records" cannot be the client-level contract (persist, barrier succeeds, crash before the client sees acceptance, record recovered → present but unacknowledged to the client). The client-level statement is {records whose acceptance the client observed} ⊆ {records recovered}. An internal ACKED count may make the equality correct; clarify the vocabulary.

Rotation exclusion: `store-log-route-programs.lisp` records that writable open can run `fnn-log-complete-rotation` before its modeled recovery program, and excludes that from the theorem's scope. The release must establish the argument or ensure an M1-covered deployment cannot reach the excluded operation, including recovery and maintenance routes. "Maximum archive span" must account for whatever durable events consume history; publish the capacity contract and separately workload estimates.

M2 deferral: content identity detects wrong bytes when the expected identity is held independently, but not omission, enumeration completeness or cursor correctness. Condition: a Mini adapter contract: Mini exposes application bytes only after verification against its independently held expected identity; missing or invalid objects do not silently count as consumed; acknowledged identities remain available for reconciliation. Never describe hashes as equivalent to read-path refinement.

Exported grammar: yes, but ACL2's round-trip theorems do not make Mini's separately written interpreter correct; it needs a common semantic specification and an eventual correspondence argument (differential tests meanwhile). Expand vectors around consumption and failure: every truncation boundary, noncanonical encodings, oversized declared lengths, unknown versions, wrong trailers, concatenated frames, exact unconsumed suffixes. A refusal that consumes the wrong number of bytes desynchronizes the stream. "Decidable" is weaker than "affordable": the fragment needs an explicit work/allocation bound, especially before allocating from an externally declared length.

## 6. Smaller calls

Competing consumers: defer; keep transport receipt, durable consumer progress and application outcome separate.

Fresh init on redeploy: preserve the old store and an explicit recovery/export route; a fresh store must be distinguishable from its predecessor wherever cursors, receipts or consumer progress depend on store history.

Per-peer refused-offer memory: agree; check invalidation dependencies, since a refusal caused by current policy, capacity or temporary state must not become permanent.

Push deferrals: agree; suspension must not become permission to discard the delivery obligation.

Tariffs, `:step-of`, read-only entries: keep partial pricing explicitly partial; keep host-loop correspondence explicitly owed; read-only correctness still includes authorization, snapshot lifetime and correct outputs.

## 7. What the repository most needs next

Put the next assurance effort into composition across failure boundaries: a process dies but its kernel cache doesn't; a publication fails but its slot remains owned; a read finishes logically but physical resources are retained; a session stays alive but its transfer stops advancing. The review question: after each failure, what survives it, and which component still owns the surviving obligation?

Extend "teeth": hypothesis-removal witnesses test nonvacuity inside the chosen model; they can't discover an environmental state the model can't express. Add model-enrichment counterexamples, where an omitted cache state or failure transition refutes the larger product claim without refuting any existing theorem.

For D49, one narrow assurance chain with visible links: client-observed acceptance → the intended durable record → survival through failures and recovery failures → successful open under declared resource/platform conditions → exact application bytes, or an explicit detected failure.

Overall: make recovery safe during recovery, not merely after it returns.

---

# Round 2 (GPT-6, after learning the lane had withdrawn A; verbatim excerpts)

Vote: A2. Additions:

1. **Physical replacement vs logical rotation.** Size "A2a: fresh physical file, unchanged logical segment": re-materialize the validated prefix while preserving logical segment identity, record sequence, predecessor binding and offsets; establish durability; then safely replace the physical backing. A2a still owes publication, discovery, failure, handle-rebinding and cleanup arguments, but may avoid every semantic consequence of rotation. "The question worth testing is whether the repair needs to change history, or only where that history is physically represented." *(Root note: m1-durable-2's A2 design is already this. Same index K, same bytes, lineage, genesis and checkpoint rows; only the inode changes.)*

2. **"A recoverable copy remains", including through failed publication.** At every interruption, previously acknowledged, still-retained records remain recoverable through a *discoverable* old or successfully established replacement representation. Writable service resumes only after the replacement's contents *and required namespace bindings* are established. Key test: a process restart after the replacement's directory barrier fails, then another recovery attempt, then power loss. A currently visible replacement name must not stand in for a binding known to survive cache loss. Don't treat a later absence of an error as proof the earlier operation persisted (Linux errseq is cursor-based). Say "no new storage assumptions", not "no assumptions". If temporary space is unavailable, refuse by name and preserve the old basis; never downgrade to in-place rewriting.

3. **A1's quantifier problem.** Durable [A, zero] and readable [A, B] give a rewrite [A, B] that does not equal the durable bytes. So A1's premise ("a write whose octets equal the durable octets") does not apply to that write at all, including its already-durable A portion. Any A1 needs a per-unit preservation contract. SQLite's powersafe-overwrite protects bytes *outside* the written range and allows old/new/random/mixed *inside* it, which is the opposite of what A1 needs. Naming an assumption makes an honest conditional claim; it doesn't make a deployment satisfy it. A1 is not an automatic fallback.

4. **B is not "no write; exact".** OpenZFS documents that direct reads stay coherent with buffered writes (a direct read after a buffered write returns the buffered data), and some configurations ignore O_DIRECT or convert it to buffered I/O. Linux `open(2)` distinguishes O_DIRECT from O_SYNC persistence. B is at most a backend-specific optimization that must establish what a direct read observes after failed buffered writeback. It is not a portable durability oracle.

Proposed decision: "Approve A2 as the implementation direction, conditional on the recovery/publication keystone covering repeated interrupted recoveries and failed namespace barriers. Size physical re-materialization preserving logical segment identity alongside full segment rotation. Preserve the old recoverable basis until replacement is established, reserve the required disk headroom, and refuse safely when it is unavailable. A1 is not an automatic fallback. B remains an optional backend-specific optimization." The successful-barrier half is a component result, not the release gate.
