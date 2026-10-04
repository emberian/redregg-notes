# Root's program-model decisions (2026-10-04, proposed; to be decided with Ember)

Inputs: eight scholar reports in this directory (SCHOLAR-BREAD-PROGRAM-MODEL, SCHOLAR-LAWS-CONTRACTS,
SCHOLAR-CALLS-CONCURRENCY, SCHOLAR-OS-LINEAGE, SCHOLAR-FRONTIER-AGORIC, SCHOLAR-BREAD-METATHEORY,
SCHOLAR-HISTORIAN-CAPABILITY-SYSTEMS, SCHOLAR-FN-STORAGE-NODE) and ROOT-READING-NOTES-PROGRAM-MODEL (spot
checks at source). Ember's steer: calls across objects rich; more laws and contracts; more concurrency;
checkpoint/heap design kept; ambitious; re-genesis free. Positions marked OPEN are for Ember.

## A. Objects and state
- An object is a cell with a stable id (never its package hash). It holds: DECLARED durable state (typed,
  first-order, versioned Core4 data; the declaration is mandatory `.obend` syntax from day one), its law, a
  package pin (interface type + package hash), an upgrade-policy capability set at creation (frozen by
  default; may only tighten), a continuity counter, and its activities.
- Why: every persistent capability system kept whole-machine persistence for crashes and found it unworkable
  as the thing that migrates (Landau 1992, Frantz 2008 "a choice between easy persistence and easy upgrade",
  Morningstar 2006, Agoric discarding heaps at upgrade). The law judges and upgrade transforms declared
  state only.

## B. Activities and checkpoints
- Keep the exact whole-machine Core4 checkpoint for in-flight activities. A checkpoint lives as long as its
  awaits, is pinned to the package hash that made it, is storage-charged after GC at the yield, and is
  decoded and type-checked before the root moves.
- Capture rule at yield: only immutable values, resources moved in, and send-only references; never a
  mutable alias of object state; turn-scoped authority (signer grants, fee meter, handlers) never enters a
  checkpoint or a cell. Resume spends the await id like a nullifier, bound to the checkpoint digest, and
  revalidates the read versions it recorded (stale -> re-run and a typed Conflict).
- Every await resolves to Reply | Refused | Unknown | TimedOut | Broken | Upgraded; every await carries a
  height deadline and escrows the fees for its resume and timeout turns.

## C. Upgrade
- One governed, all-or-nothing turn. Authority is a law-governed capability, visible on the object's card;
  no superuser. Checks: declared-state subtype, else a typed linear migration Old ⊸ New; the law re-judged
  on migrated state; frozen floors entailed (decided as unsat(new ∧ ¬floor) with a certificate); interface a
  supertype of every referenced facet.
- Activity dispositions, decided INSIDE the upgrade turn or the upgrade is refused: DRAIN (default:
  activities continue on their pinned old package until their awaits end; Erlang's two live versions;
  sound because checkpoints hold no mutable state) and ABORT (resolves awaits to Upgraded). REPLAY only if
  the replay succeeds within the upgrade turn. NO "map" (rewriting resume points onto new code): the
  historian's record (KeyKOS clock surgery "ugly beyond belief"; Agoric's replay-after-commit "wishful
  thinking") outweighs the OS/calls scholars' proposal. A Core4 or codec epoch change drains or aborts.

## D. Calls across objects (rich, three forms)
1. `call`: synchronous, in-turn, through a held capability; the callee runs its pinned package against the
   turn's snapshot and returns (value, Plan fragment); depth-first; authority per Daml's four rules
   (callee consequences run under the authority its signatories pre-granted plus the node's controllers;
   delegation not transitive); RE-ENTRY into an object already on the stack is REFUSED (mandatory; 10 of
   ~100M Ethereum executions were legitimately reentrant); a frame that read a version another frame wrote
   aborts the turn.
2. `send`: eventual; a Plan action on a per-(sender,target) FIFO inbox cell; each delivery is its own paid
   turn; breadth-first. Answer slots named H(turn, call site) with exactly one decider; sends to an
   unresolved slot queue there and are forwarded in the resolving turn; broken slots propagate and refund.
3. Pipeline invocation: a signed, straight-line, non-recursive pipeline of calls on capabilities and prior
   results (Sui PTB, Cap'n Web shape), re-executed as one turn; partially signed pipelines from several
   parties compose into one turn = in-domain multi-party atomicity without 2PC.
- Scoped grants (Pact): the signer attaches capped, parameterized capabilities to the invocation; they
  count down as nested code uses them. Bounds what callees do with the caller's authority.
- Output gate: nothing externally visible leaves a domain before its turn commits (and is final in a
  committee domain).
- Promise pipelining proper (early delivery to the callee's host) only on cross-domain links, after answer
  slots and their upgrade semantics exist.

## E. Laws and contracts
- The decidable law language stays the judge at every write; code proposes, law disposes; package proofs
  are extra evidence, never a substitute.
- Richer, still decidable: two-state atoms (new[a] ≤ old[b] + k); request atoms (method, invoker,
  capability presented, height); necessity sugar `from A to B onlyIf C`; relational/action-scoped clauses
  over the cells the Plan co-touches; past-time temporal laws compiled to kernel-maintained history slots.
- Three points: method guards (checked before any code runs; refusal costs no execution), state laws (every
  write), proposals.
- Seats: an offer creates a seat = a Book account + a law whose clause is offer safety (want, or full
  refund of give), judged on every reallocation for the seat's life; exit is a kernel action no contract
  can override; payout liveness is a kernel theorem for Book assets.
- Protocol objects: a choreography's remaining global type is the object's state; its law admits exactly a
  legal next step for the signer's role.
- Deny by default; clauses indexed by method; forbid overrides permit; per-clause coordination grade
  computed at publish; publish-time checks (entailment, grade, upgrade compatibility) with certificates;
  admission only evaluates closed laws. Refusal explanations carry the residual predicate, under a
  redaction policy.
- OPEN: generate laws from `.obend` declarations now (root's lean) vs unify laws into a decidable Objective
  Bend fragment later.

## F. Concurrency
- Several activities per object; they share state only through committed cells; resume revalidates reads;
  split hot state into sub-cells with their own laws; exclusivity across a yield only by a law-governed
  lease, never a default lock.
- Deterministic parallel admission with Block-STM semantics: footprints LEARNED during admission
  (declarations are hints), root = the sequential fold (single-threaded auditors suffice), delta actions
  first-class, the dependency DAG published for parallel replay. (Resolves calls vs OS in calls' favour.)
- Coordination grades from laws decide which turns commute, which skip ordering, and who votes. Escrow
  quotas (local quotas summing to the budget) let many activities draw on one balance.
- Cross-domain: a deal cell in a domain all parties accept, offer safety as its decision law, write-once
  with a timeout height and default abort; everything else as choreographed sagas.

## G. Metering and storage
- One signed envelope per invocation (decided 10-04); a Lean cost theorem: metering is a function of
  pre-state and invocation and meter ≥ machine transitions INCLUDING kernel work (codec, GC at yield, law
  checks, Merkle updates). Exhaustion parks the activity and refunds the unused remainder; never terminates.
- Meters are accounting, not scheduling (KeyKOS, EROS, Coyotos all abandoned meter-tree scheduling).
- Every retention structure (inbox, await index, watcher table, recovery list) is a cell with a payer;
  storage is a deposit; unfunded objects hibernate (evicted to their Merkle hash, restorable), never
  deleted; in-domain GC traces cycles; termination is O(1) by detaching the subtree.

## H. Presentation and debugging
- Every object answers describe / affordances / history; an affordance is Hidden, Disabled(reason) or
  Enabled, the reason computed by the same law check admission uses; projection code is effect-free.
- Causal edges on every receipt; unhandled faults route to the object's keeper.

## I. fn
- fn is Mini's archive, feed and transport for exact bytes now: finalized blocks and receipts (bundled
  several blocks per article), replay kits, published package bytes, cross-domain deal and saga messages.
  NO checkpoints of any kind in fn (signed articles are never reclaimable by theorem); hibernated object
  data and replay logs only if paid for as permanent history. Under the hot per-turn log later, gated on
  fn's page representation and the fn-store-1 freeze. Mini pins fn by image digest, node identity, schema
  digest, format word and history-id (history-id alone survives export/import). Contract:
  designs/MINI-FN-660-REQUIREMENTS-20261004.md (scribe notes SN-1..SN-6 accepted by root 10-04).

## OPEN for Ember
1. Synchronous cross-principal `call` (D1) at all, versus Agoric's "never synchronous across trust
   boundaries". Root's lean: yes, with Daml authority + scoped grants + mandatory re-entry refusal.
2. Laws: generate from `.obend` now, unify later (root's lean), or unify now.
3. REPLAY as an upgrade disposition at all, or DRAIN/ABORT only.
4. Order of building: answer slots and the resume contract first, then `call`, pipelines, seats, protocol
   objects; cross-domain pipelining last.

## Root resolutions of the design scribe's notes (2026-10-04 night)
- A1 identity: an object's id is its cell id and nothing derived from its schema. If `ObjectRef.kind` carries
  a schema digest, split it: `kind` names the semantic kind; the schema digest is a separate, mutable field.
- B1 capture rule: accepted; it constrains the kernel's activity record, Core4 values satisfy it by construction.
- B2: add `Conflict` to the await outcome sum (Reply | Refused | Unknown | TimedOut | Broken | Upgraded | Conflict).
- B3: kernel-produced checkpoints are well-typed by theorem; the before-root check is codec validity plus the
  digest binding to the producing turn; no foreign checkpoint is ever admitted.
- B4: GC at yield is a build item (its own lane), and storage is charged on the post-GC size once it exists.
- C1 DRAIN, refined to a two-phase upgrade: (1) ADOPT turn: new package pinned for new activities; the object's
  declared state is NOT migrated while any old activity remains; (2) old activities run on their pinned
  package against the unmigrated state until their awaits end OR a mandatory drain deadline height, after
  which they are aborted with Upgraded; (3) MIGRATE turn: state migrated and the law re-judged when the last
  old activity ends. Looping residents are bounded by the deadline.
- C2 REPLAY: dropped for now (needs a full interaction log Mini does not keep; the historian's record agrees).
  Dispositions are DRAIN (with deadline) and ABORT. This answers OPEN 3 provisionally; Ember may reopen it.
- C3: a Core4 or codec epoch change is always a re-genesis (greenfield); frozen objects therefore never need
  to survive one.
- D1: the "10 of ~100M" figure counts legitimately non-ECF executions, not re-entrant ones; the cost of
  refusing all re-entry is unmeasured. Keep the refusal (conservative) and measure it on Mini's own cohorts.
- D2 write-write: two frames of one turn writing the same slot abort the turn, unless that slot's law
  declares the write a commutative delta (then deltas compose and the law judges the sum).
- D3: in a multi-party pipeline each signer's envelope covers that signer's segment; the turn is refused if
  any segment exceeds its envelope.
- E1: protocol objects are compiled at publish time into a finite transition table; payload-dependent
  conditions are law atoms on payload fields at a transition (control states stay finite).
- G1 refunds: the never-refund rule covers MEASURED quantities (unused envelope, ticks); exhaustion parks the
  activity and its resume needs a new envelope. Deterministic, measurement-free amounts MAY be returned:
  postage of sends that were never delivered (broken slots) and the unused one of an escrowed resume/timeout
  fee pair. No refund ever depends on how much computation ran.
- fn: SN-1..SN-6 accepted (see §I).
OPEN for Ember after these: 1 (sync cross-principal `call`), 2 (laws generate-now vs unify), 3 (replay:
provisionally dropped), 4 (build order).

## Root rulings on the 2026-10-05 scholar reviews (historian, Bread, frontier, OS converge)
- RESUME WITH VIEW (supersedes T1(e) and the earlier "Conflict" outcome): every resume delivers its outcome
  TOGETHER WITH a fresh view of the object's declared state (with its version), read in the same turn; a
  Plan state write is refused if that version moved since the view (optimistic, retry-able); Plans write
  fields or deltas, not whole records. `conflict` leaves the outcome sum. Refused/broken reasons are a small
  fixed sum delivered to the activity. (Bread D-1/R1, historian F2, frontier 1.)
- OBJECT AUTHORITY: object state cells live in their own kernel namespace; every declared-state write needs a
  facet capability of that object AND is judged by the object's law (old vs new); the payer is never
  authority; birth/delivery/invocation refuse a non-object cell by name. (OS W1, Bread D-2, historian F1,
  frontier 2.)
- UPGRADE (refines C1): while an upgrade drains, the object admits NO new births or calls unless the old
  state type is a subtype of the new; an old activity's write is admitted only if migrate(s') type-checks and
  satisfies the new law, so the final MIGRATE cannot fail (OS W2, historian F5, frontier 5). Large objects
  migrate over several turns: object closed, a cursor cell holds progress, any upgrade-capability holder
  advances it (OS W3). Dispositions: DRAIN, ABORT, and REBIRTH (abort + re-birth from the record's stored
  input on the migrated state; restartability checked at publish) (historian F6). REPLAY stays dropped.
- METERING: exhaustion charges the full declared envelope (historian F3); one shared tariff and usage vector
  for native admission and activities, package type-check verdict cached at publish, checkpoint encode/decode
  priced, a storage deposit on each checkpoint re-priced at each yield (OS W4, W7; Bread D-5).
- DISPOSAL: records deleted on done/faulted; abandon turn after deadline + grace; decided slots reclaimed;
  every retention cell has a payer (historian F4, Bread D-6, frontier 3).
- PRESENTATION: affordance states Hidden / Disabled(reason) / Possible (law satisfiable) / Enabled (simulated
  admission succeeds) (OS W8).
- SEATS: invitations bound to a contract instance, who may debit a seat named, offerSafe corrected for zero
  `want` (frontier 4).
- OPEN QUESTIONS — all four reviewing scholars agree with the root's leans: (1) synchronous cross-principal
  `call`: YES, callee reads the turn snapshot, writes deferred/applied at frame return, re-entry refused,
  callee billed to the caller's envelope; (2) laws generated from .obend now; (3) REPLAY dropped, REBIRTH
  added; (4) build order: OBJECT-RECORD and RESUME-WITH-VIEW before `call`, then seats/scoped grants, then
  `call`, then `send`. Recommended to Ember as settled unless she objects.
- FOR EMBER (custody): the mini-keys broker holds all three secret classes in one account (OS W9).
- LAWS (2026-10-05, from REVIEW-SCHOLAR-LAWS): D-1 SECURITY: the native Objective path projects no artifact/method
  slot into the law state, so dropping the claim turns an Objective command into an ordinary one with the same
  writes; fix = project objective/artifact and objective/method slots from the signed claim + a pin clause on
  object state cells at creation (QUEST-LAWS-PIN, running). D-2: the single Receiver must evaluate every
  written cell's law itself (receive_committed_lawful + kernel-only cell registry) before more families move
  onto it (QUEST-LAWS-RECEIVER, next). Q2 recommendation refined: unify the SYNTAX now (invariant / guard /
  permit / forbid clauses compiled by the Lean elaborator to Pred, refusing anything outside the fragment);
  Pred stays the judge; Objective Bend method `law`s stay package evidence. Seats with empty `want` need an
  explicit `donate`; ObjectRecord gains `creators` (Daml signatories); floors outside the fragment refused at
  install.
