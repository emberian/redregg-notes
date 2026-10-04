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
- fn is Mini's archive, feed and transport for exact bytes now (finalized blocks, receipts, checkpoints at
  cadence, deal messages, replay kits); under the hot per-turn log later, gated on fn's page
  representation and the fn-store-1 freeze. Contract after the fn session's FN-CHECK.

## OPEN for Ember
1. Synchronous cross-principal `call` (D1) at all, versus Agoric's "never synchronous across trust
   boundaries". Root's lean: yes, with Daml authority + scoped grants + mandatory re-entry refusal.
2. Laws: generate from `.obend` now, unify later (root's lean), or unify now.
3. REPLAY as an upgrade disposition at all, or DRAIN/ABORT only.
4. Order of building: answer slots and the resume contract first, then `call`, pipelines, seats, protocol
   objects; cross-domain pipelining last.
