# IMPACT-P3-MEASURE · the half-day measurement that opens phase three

CX-PROMO-3, 2026-10-22, nano main `100ad08`. Plan PROGRAM-20261022.md §3 P3 ("Measure first"), §2 refuter, §8.5.
All READ at `100ad08` unless tagged. Nothing built.

## 0. The population: every ActivityPlan and the Bell

`git grep` for `ActivityPlan` and for `(activity ` across every Lean file and every `world/**/*.ob`. The population is
exhaustive.

| instance | where | plans | deployed? |
|---|---|---|---|
| **Bell** | `world/resident/Bell.ob` (LANG-58/59; the resident: `Hosting/Resident/Bell.lean`) | `ask` (arg `{text}`, resp `bytes`) | yes: the resident World |
| **Std.hole** | `Lang/StdHole.lean:239` `holePlan` (+ P8 `p8CommitPackage`, `Lang/Journey.lean:2198`) | `fill` (captured V, resp `{}`) | yes: the generator; P8 rows |
| teeth fixture | `Lang/Proofs/StdActivityTeeth.lean:8` `actPlan` | `step`, `other` | proof-only fixture |
| surface fixture | `Lang/Journey/Activity.lean:10` | `step` | journey row (install check only) |

Not activities, but read for (a)/(c) because they are the other multi-party deployed protocols: Escrow
(`world/escrow/Escrow.ob`), Lifecycle (`world/grain/Lifecycle.ob`, a `machine`), Allowance (`world/hosting/Allowance.ob`).

## 1. The three counts

### (a) Distinct kernel-side roles signing a step

A "role" is a signer predicate a receiver checks (`req.agent` compared against a state field or a row key).

| instance | roles (method: check) | count |
|---|---|---|
| Bell | **ringer** (`ring` → `start_ask`: the `pending`/`rings` insert is keyed by `req.agent`, guard `notYours`); **resident** (`answer`: `deq req.agent state.resident`, "notResident"; also the activity's resumer). The generated `start_ask`/`resume_ask` are not exported (`(expose)` with no names, `Lang/Surface.lean:789`). | **2** |
| Std.hole | **chooser** (`fill`, `select`, `prune`: `canChoose`, "notChooser"); **acceptor** (`accept`: "notAcceptor", which runs `start_fill`; `resume_fill`: `holeResumer` = acceptor); **poster/proposer** (`post`/`repin`/`unpost`, `propose`: any member, rows owned `by = req.agent`, "notYours") | **3** (2 named in state + any member as row owner) |
| Std.hole's activity alone (`fill`) | start (through `accept`) and resume are BOTH the acceptor | **1** |
| P8 (Std.hole + `commit`) | the chooser signs `commit` (select + `transfer … via grant`); B issues the grant (a kernel `grant` call, not a hole method); providers post facts | 3 hole roles + the grant issuer |
| Escrow | depositor (`deposit`); beneficiary or arbiter (`refund`); depositor or arbiter (`release`) | 3 |
| teeth/surface fixtures | starter (key agent) + resident (resumer) | 2 |

Also measured, not a role: the Bell's `open`, `close` and `retire` check no signer. Any member can close the Bell, and
any member can retire an ANSWERED ring (`rung`'s retract arm needs `old` answered). The law `bell` only keeps
`resident` fixed. This is not a P3 finding; recorded so nobody counts it as a role.

**Plan's expectation "Bell = 2 kernel roles": MET.**

### (b) Resume arms inserting another `waits` row (a second round)

- The generic resume (`activityResumeResult`, `Lang/StdActivity.lean:136`) emits exactly two edits: an UPSERT of the
  log row (answered) and a RETRACT of the cursor row. It inserts nothing. The author's `resume` term returns STATE
  only (`Ty.fn S (.fn captured (.fn response (.fn reqTy S))))`, `activity`'s check at `:222`), so no author code can
  add an edit to a resumption.
- Bell `answer` (custom, `Bell.ob`): upsert `rings` + retract `pending`. 0 inserts.
- Std.hole `resume_fill`: the generic one. 0. `accept` STARTS the activity (the one insert pair); nothing re-inserts.
- The log guard (`activityWaiting`, `:65`): an answered row refuses every further upsert ("answered"). Insert is by
  the key's signer with `answered = none`. A second round on the SAME key is refused. A second round on a NEW key is
  a new `start_*`: another ring, not a continuation.

**(b) = 0 everywhere.** Every deployed activity is one exchange deep: start, then one answer.

### (c) Object steps depending on another object's row

- Row reads are SELF-ONLY: a method's `rows` view is built from `rv.points self i` (`Lang/Rel.lean:179`; the ROM
  hole's `holeRow` likewise, `Lang/LiveHoles.lean:93`; E1 kept it, READ-E1 R3). No method of any instance reads another object's ROW. **(c) = 0.**
- The cross-object dependencies that DO exist are cells and derived calls, not rows:
  - Std.hole's six judging methods (`accept`, `fill`, `propose`, `prune`, `rejudge`, `select`) read `facts` with the
    `live` column: `cellLive look g` of the cell a fact names, any object's cell (E1, LANG-75.1). They depend on
    another object's CELL being live, never on its rows or its version.
  - P8's `commit`: one `transfer` (amount from the hole, `via` the grant), checked by the kernel ledger in the same
    Turn.
  - Escrow `deposit`/`refund`/`release`: one `transfer` each, against account cells.

### Grep: dispatched-awaiting state across Turns between cells

`git grep -i "dispatch|awaiting|in.flight|inflight"` over every non-proof, non-journey Lean file:
- Kernel `dispatch` (`Kernel/Receive/Derive.lean:336`): the derived call tree, run INSIDE one Turn (depth
  `callDepthMax`). Nothing survives the Turn.
- In-flight states that DO cross Turns are all HOST-side, between a member/host and a World, never between two cells:
  a seal in flight (`Host/Loop.lean:127`), the keybroker's one ask per resident (`Hosting/BrokerWire.lean:89`), a key
  rotation armed (`Protocol/Command/Machine.lean:815`, `Protocol/Table.lean:323`).
- Activity rows (cursor/log) wait across Turns, but within ONE object, for a MEMBER's answer (the resident, the
  acceptor), never for another cell.
- `Lang/Contextual/Protocol.lean`'s `inflight` is the protocol calculus (R-0021 KEEP), not deployed state.

**No cross-cell in-flight state. Plan's expectation MET.**

### The activities proposal: any ≥ 2-round negotiation?

READ `ACTIVITIES-PROPOSAL-20261022.md` (whole: §4 intents, §5 polarity, the integration experiment at :362) and the
negotiation rows of `ACTIVITIES-DESIGN-20261022.md`.
- §4: a completion space `C_w(P) = {θ | …}`, "the SAME θ must satisfy all conditions". Negotiation is ONE
  substitution θ satisfying both parties' constraints, found by search. The proposal's own example
  (buyer ≤ 5, seller ≥ 7, no shared price) has no rounds: either a θ exists or it does not.
- §5: "an unresolved peer response stays an interaction with a response-dependent continuation". That is ONE response
  with a continuation, which is the activity's start/resume.
- The integration experiment (:362, journey LH9): "two cells negotiate a one-use capability, with alternative
  providers, a deadline, and a cancellation path". Providers propose (one row each), the chooser selects one, the
  acceptor accepts (one activity round). Alternatives are SUMS (candidates), not rounds. Cancellation is the deadline
  (`closes`) or not accepting.
- The design (`ACTIVITIES-DESIGN-20261022.md:120`, `:470`): multi-party agreement with two WRITERS and mini's
  multi-signer `Hyperedge` are OUT (charter item 3). "The two-cell negotiation is two …" objects, each with one
  writer.
- No counter-offer, no re-proposal on an answer, no second round anywhere.

**Negotiation = one θ. Plan's expectation MET.**

## 2. What the counts select (plan §3 P3, §8.5)

Every expectation holds: Bell = 2 roles, 1 round, broker host-side, no cross-cell in-flight state, negotiation = one θ.
By the plan's own branch:
- **PROT-3's kernel half collapses to `machine_reached` + a docstring**: one round, so the global type of the Bell is
  ring → answer. The joining theorem (B8) and E2's socket remain, and those are the resident's half.
- **PROT-4 is cheap**: the monitor is the activity guard (`activityWaiting`), which already refuses every off-protocol
  edit by name; the `activity_*_requires_*` teeth are its instances.
- **PROT-5(b) is host-side only**: the only cross-Turn in-flight states are host's.
- **PROT-6 = "two offer rows + one guard `A θ ∧ B θ` + atomic consumption"**: (c) = 0 means the fuse's read of the
  OTHER object's offer row is NEW (E1's foreign read exists for cells; for rows, `rv.points parent rel` exists in the
  kernel, `Kernel/Receive/Call.lean:277–285`, and only Lang's self-only view, `Lang/Rel.lean:179`, restricts it). That widening is
  PROT-6's one real Lang change, and it is the first deployed (c) > 0.
- The higher-count shapes (HYC/Bocchi multi-round) are NOT selected.

## 3. Plan §2's refuter: which Worlds' state each row changes

"If any row needs two Worlds changed atomically, P6 moves before P5 and E6 is on the path."

| row / card | Worlds whose state it changes | atomic across Worlds? |
|---|---|---|
| B1 P8.2 revoked grant refuses | one (the P8 World: no change on refusal; the revoke itself is a Turn there) | no |
| B2 LH14 support of a digest never had | one | no |
| B3 P8.4 use-once + authority | one: hole cell + value cell + grant in ONE Turn of ONE World | no (one World, one Turn) |
| B4 `selectHole_judge` (other branch landed) | none (a theorem) | — |
| B5 P8.3 / P8.3r repair, monomial | one | no |
| B6 label after revoke | one | no |
| B7 F1/F2 fuse | one: two OBJECTS (cells) in one World, one Turn | no: two cells, not two Worlds |
| B8 Bell + member socket (LB4/LB7, `resident_bell.rs`) | one World (the resident's); the member is a follower of it, never a second writer | no |
| B9 P8.4 replay, at-most-once | one | no |
| B10 X1/X2/X3 receipts | X1: A's Turn (offer) in A, THEN B's Turn (accept on A's receipt) in B: two Worlds, SEQUENTIAL, each by its own writer. X2/X3 (forged receipt, forked head): B refuses, A unchanged. | **no**: asynchronous by design (§2(a): "NOT atomic cross-host commitment") |
| P3 PROT-1..8 rows (F1/F2, LB*, escrow) | one World each | no |
| P4 M1/M2 | none (measurements) | — |
| P5 E5 X1–X3 | as B10 | no |
| P6 E7 availability row + one-host plant | one World, replicated (one decided log) | no: replicas of one World are not two Worlds |
| P7 E6's trigger row ("two members exchange value in one Turn without escrow") | one World, one Turn, two SIGNERS | no: multi-signer, not multi-World |

**No row in §1 or §3 needs two Worlds changed atomically. P5 before P6 stands; E6 stays off the path (P7, trigger
only).**

## 4. What I did not measure

- The Rust-decision count on the stdio leg (PROT-3's E.2 measurement, plan §8.4) is PROT-3's own first step, not
  this card's.
- Whether PROT-6's row widening (a method reading another object's ROW) needs a pin of that row or only of the parent
  cell: INFERRED from `Call.lean:277–285` that the kernel already pins rows by `rowPins`, so it is a Lang-side view
  change. This is the first question for PROT-6's IMPACT.
