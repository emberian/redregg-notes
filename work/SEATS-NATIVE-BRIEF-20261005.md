# SEATS-NATIVE: brief for the successor of SCHOLAR-FRONTIER (2026-10-05)

Quest, approved by ROOT: put seats and invitations on the native signed-command route; make an
activity's end close every seat it holds; settle a two-party swap on a scratch world through
signed commands. Ask me (SCHOLAR-FRONTIER) anything with SendMessage; I hold the Agoric/Zoe context
and wrote L7.

Evidence tags in this brief: **READ** = I read it at source today; **ASSUMED** = my inference, which you
should verify before building on it.

## 0. What exists

1. **L7, on lane/seats** (`persvati:/home/ember/workbox/claude-lanes/seats/src`, commit `aa6c8047`
   on main `5f9aa259`, QUEUED in `work/MERGE-QUEUE.md`, gate green: logs `seats/logs/gate-1.log` and
   `gate-seats1.summary`). READ, I wrote it.
   - `Kernel/Invitation.lean`, namespace `Minidregg.Kernel.Invitations`:
     - `Instance {id, package : Digest, clause : Pred}`;
     - `Invitation {id, inst, package, role, terms, holder : SubjectId}`;
     - `Registry {instances, live, spent}`;
     - `mint` (acting instance = the invitation's instance, same package, fresh id), `handOver`
       (holder only), `Expectation {inst, package, role}`, `spend` (holder + assay, then the id moves
       to `spent`);
     - theorems `spend_once`, `spent_never_minted`.
   - `Kernel/Seat.lean`, namespace `Minidregg.Kernel.Seats`:
     - `ExitRule = onDemand | afterDeadline due`, `Proposal {give want : List (AssetId × Nat), exit}`;
     - `atLeast` (zero-safe), `offerSafe : Proposal → Pred`, `view` (the total balance view),
       `safeAt book account proposal : Bool`;
     - `Transfer`, `post`, `settle` (membership + funded source), `payout` (moves the whole
       balance);
     - `Seat {account, inst, offerer, payee, proposal, isOpen}`,
       `World {book, owners, registry, seats}`, `Actor = subject | inst`,
       `Action = create | mint | handOver | offer | reallocate | exit | terminate`;
     - `step world height actor : Action → Except Refusal World`, `closeSeat`, `closeAll`,
       `Inv`, `Reachable`;
     - theorems `seat_offer_safe_forever`, `exit_enabled`, `exit_after_deadline`,
       `exit_pays_allocation`, `seat_conserves`, `seat_debit_authorized`, `safeAt_mono`,
       `view_total`, `payout_exact`;
     - `Example`: the swap after a price move, raid refused, locked contract cannot stop exit,
       zero want, the Nat-encoding tooth, the absent-slot tooth, `swap_opening_reachable`, all by
       `decide +kernel`.
   - What L7 is NOT: wired to stored cells. Its `World.book` is a `Book` value, `owners` is a list
     standing in for ownership, `Registry` is a list, and the `inst` actor has no native meaning.
     Those are exactly what this quest replaces.

2. **The precedent route: the kernel activity as signed native commands.**
   `persvati:/home/ember/workbox/claude-lanes/activity-native/src`, branch `lane/activity-native`
   (the ROOT calls it `-wip`), tip `93c55464`. Read these commits whole before writing anything:
   - **`ed608774` (`registry!`), protected coordinates.**
     - `Compiler/CanonicalCellRegistry` gains `Kind.objectiveActivity` (tag 19, schema 91018) and
       `Kernel/ObjectiveActivityCell.lean`, with roles `record | slot | state | package`.
     - Coordinate = `2^256 + cSHAKE(domain, role, key)`. `UserShape` is false for the kind, and
       `UserInitial` requires `cellId < 2^256` (`userInitial_not_activity_coordinate`).
     - Every exhaustive `Kind` match was touched: LegacyStoreCarry, DeployedBridge,
       ResourceTargetAdmission, ContentResourceAudit, ResourceObservationAdmission. It is a FLAG DAY
       (re-genesis every Store).
   - **`04536ff8` (`activity(native)!`), the route itself.** It touched 25 files. The module to copy
     is `Kernel/ObjectiveActivityReceiver.lean`:
     - `Turn` wire, `Command {subject, nonce, authority root, turn}`, `commandCodec` /
       `ingressCodec`, `decodeIngress`, `marker`;
     - `configOf` (from the deployment's Objective policy; disabled with `objective-core4`);
     - `decideTurn`, `Decided.intent` (literally the kernel's own `Birth.intent`/`Delivery.intent`
       under the receiver's `Seal`);
     - `Declaration` and `effectDigest`: the signature binds the decided posts;
     - `objectHolder` (the authority layer's `capabilityAdmissibleCheck`) and `accountHolder` (owner
       grant + admissible `transfer`);
     - `Prepared` / `prepare`, `admitDecodedNative`, `Accepted`;
     - theorems `intent_writes_activity_or_book`, `intent_writes_lawful`,
       `birth_requires_object_holder`, `native_delivery_consumes_once`,
       `native_resume_binds_checkpoint`.
   - **Same commit, Book wiring.** `Kernel/ObjectiveActivity.lean` fees are Book postings: `BookCell`,
     `bookOf`, `Postings pre` = a `Batch` with `AcceptedBatch pre batch`, and `Postings.write` to
     `config.bookCell = deployment.resourceBookId`. The purse is a Book account at the record cell's
     id.
   - **Same commit, Host wiring:**
     - `Kernel/NativeHost.lean`: session ops 210 plan, 211 assemble, 212 submit, 213 lookup,
       214 public view;
     - consent 224 reproduces op 210 (`Kernel/NativeSpecializedConsent.lean`);
     - `Kernel/NativeHostReplay.lean` re-admits on reopen;
     - `Kernel/TurnCensus.lean` row;
     - `Host/ObjectiveActivityJson.lean`; `native/resource-client/src/activity.rs` (`mini activity`),
       `transport.rs`, `main.rs`, `client_consent.rs`;
     - the acceptance driver `native/resource-client/objective-activity-native-acceptance.py`, which
       runs on a scratch world made by `newparticipant-acceptance.sh` with a second enrolled
       subject (40).
   - **`69cfd4e4`, Host closure pin.** `scripts/check-host-closure.sh --update`.

   **Merge state (READ in MERGE-QUEUE at 11:50).** The activity-native range `ae1455a6..9c9608b0` and
   resume-view (`46b9d4fd`, which changes the activity record frame, the outcome sum, Plan writes
   keep|set|add, and removes `conflict`) are in batch c2. The route commits above are on the lane
   branch; I did not see them queued. Base your work on whatever main holds when you start, plus the
   route if it has not landed: ask ROOT which tip to base on. Do not fork a second copy of the route.

## 1. What to build: modules and functions

### A. Protected cells: `Kernel/SeatCell.lean` (new), plus a registry Kind (FLAG DAY)

- Follow `ObjectiveActivityCell` exactly. Either add a new Kind (tag 20 or the next free; schema id
  the next free) with roles `instance | invitation | seat | spent`, or add roles to the activity
  kind. Prefer a new Kind: seats are not activities.
- Coordinates `2^256 + cSHAKE(domain, role, key)`:
  - instance key = instance id;
  - invitation key = invitation id;
  - seat key = H(offer transaction);
  - spent marker = invitation id (use the durable nullifier / claim mechanism the activity uses for
    awaits instead of a list, if that fits better; ASSUMED).
- **The seat's Book account id IS its seat cell's coordinate**, like the activity purse. This
  replaces L7's `RegistrationAdmission` + `seatAccountOwned` checks with structure: no user can own,
  squat or pre-fund a coordinate ≥ 2^256.
- Every exhaustive `Kind` match gains the new kind. Mirror `ed608774`'s file list and
  `userInitial_not_activity_coordinate`.

### B. The kernel: refactor `Kernel/Seat.lean`; do not fork it

The native receiver must commit exactly what `Seats.step`, or its successor, decides. No second
transition function: two that agree today are a twin.

1. **Replace `post` / `settle` / `payout` with one `Batch`** built per turn, admitted by
   `AcceptedBatch` on the loaded `BookCell`, like `ObjectiveActivity.postings`.
   - Keep `safeAt` / `view` / `offerSafe` as they are (they read a `Book`).
   - Re-prove `seat_conserves` from `AcceptedBatch` conservation.
   - Re-prove the per-account lemmas (`settle_untouched`, `settle_credit_only`, `payout_exact`)
     against the batch's postings, or derive them from `Batch` lemmas if `CanonicalResourceKernel`
     has them (`Batch.conservation` exists; READ).
   - Funding check: Book `Admission.sourceSolvent` is exactly L7's "funded source".
2. **Replace `World.owners`** with the receiver's `accountHolder` (owner grant + admissible
   `transfer`) for the funding account. Refuse a payee ≥ 2^256 (a protected coordinate). Refuse a
   payee that is not a Book account, as L7 does.
3. **Give the `Actor.inst` authority a native meaning.** An instance is an object (a native resource
   cell). `mint`, `reallocate` and `terminate` are signed by a holder of an admissible capability on
   that instance object (`objectHolder`), exactly as activity `writeState` is.
   - Say plainly in the docstring that this is operator-controlled reallocation. Offer safety, exit
     and conservation protect the offerers whoever controls the instance, which is the point of
     Zoe. "Contract code proposes the reallocation" arrives when a package's Plan can carry
     `reallocate`: later, not now.
   - `create` (instantiate a package as an instance) is a birth of the instance object plus its
     instance cell; use `objectHolder` on the new object.
4. **Seats held by activities.**
   - The activity record must list the seats it holds (it holds the offer it made).
   - Whatever terminal path the activity kernel has when you start (done / faulted / timedOut end;
     ABORT if L10 upgrade has landed) must call `closeSeat` for each held, open seat, in the same
     intent.
   - Theorem: `activity_end_closes_seats` (every seat the activity held is closed and paid to its
     payee in the ending turn).
   - ASSUMED: the activity kernel has no ABORT yet. If so, state the theorem for the ends that
     exist and leave a named hook (`closeHeldSeats`) the upgrade lane calls.
5. **Keep L7's statements, now about the stored world.**
   - Restate `Inv` over the decoded seat/registry cells and the loaded Book.
   - Prove the bridge, as `native_resume_binds_checkpoint` does: the Host commits exactly the
     `Decided.intent` of the seat step under its seal. Then `seat_offer_safe_forever`,
     `exit_enabled`, `exit_pays_allocation`, `seat_conserves` and `seat_debit_authorized` hold of
     what the Host writes.

### C. The receiver: `Kernel/SeatReceiver.lean` (new)

Copy the shape of `ObjectiveActivityReceiver`:
- `Turn = create | mint | handOver | offer | reallocate | exit | terminate`, with capability ids
  where authority is needed;
- `Command`, codecs with new frames (`DREGG/SEAT/COMMAND/v1`, `DREGG/SEAT/SIGNED/v1`);
- `decideTurn`, `Decided.intent`, `Declaration` / `effectDigest` binding the decided posts;
- `prepare`, `admitDecodedNative`, `Accepted`, replay.

Theorems:
- `intent_writes_seat_or_book`, `intent_writes_lawful`;
- `offer_requires_account_holder`;
- `reallocate_requires_instance_holder`;
- `exit_requires_offerer_or_instance_or_deadline` (the kernel's `exitAuthorized`; no clause
  consulted);
- `native_offer_spends_invitation_once`.

### D. Host and client

- Session ops: the next free contiguous block. Ops 210–214 and 224 are taken by the activity; grep
  `Kernel/NativeHost.lean` and `NativeSpecializedConsent` for every number in use.
- A consent op reproducing the plan op.
- `NativeHostReplay` re-admission, a `TurnCensus` row, `Host/SeatJson.lean` (author/inspect/view).
- `native/resource-client/src/seat.rs` (`mini seat --action …`), transport, main, client consent.
- `scripts/check-host-closure.sh --update`, `python3 scripts/lean-build-surfaces.py generate`.

### E. Acceptance: `native/resource-client/objective-seat-native-acceptance.py`

The scratch world is made by `newparticipant-acceptance.sh` with a second enrolled subject, every
turn a signed `mini seat` command. Rows (each with roots-unchanged checks on refusals):
1. Create the instance; mint two invitations; a stranger's mint is refused; a mint with the wrong
   package is refused.
2. Alice offers (give 10 X, want ≥ 5 Y); Bob offers (give 7 Y, want ≥ 9 X); an offer naming another
   subject's funding account is refused (`notAccountOwner`); a re-used invitation is refused.
3. **The price moved:** the reallocation settles at 7 Y to Alice and 10 X to Bob. The Book total of X
   and of Y is unchanged after every turn.
4. A raid (Alice gets 4 Y, loses 10 X) is refused by her seat law with roots unchanged.
5. **Locked instance:** a second instance whose clause refuses all reallocations. Its reallocation
   is refused, and Alice's exit still pays her 10 X back.
6. **Zero want:** a gift seat (give 10 X, want 0 Y) is fully taken, and that is admitted.
7. A stranger's exit is refused; an exit after a deadline seat's due height by a third party is
   admitted.
8. **An activity holding a seat ends** (timedOut path), and its seat is closed and paid in that turn.
9. Lost reply: lookup and exact resubmit both replay. Reopen: the replay walk re-admits and the view
   is identical.

**Gate:** `lake build Minidregg +Host.Main:leanArts ObjectiveProofs minidregg-host
minidregg-client-consent` plus `merge-gate-checks.sh`. Filtered Rust tests for the touched crate
only (never a bare `-p`).

## 2. Traps I know about

1. **Twin.** L7's `settle` / `payout` and the activity's `Postings` are two posting paths. Delete
   L7's after the Batch refactor (B1). Do not keep both "because the theorems use them".
2. **Coordinates, not user ids.** L7 checks seat-account freshness and non-ownership because it lets
   the offerer name the account. On the native route the account is the seat cell's protected
   coordinate. Drop the user-named account from the command entirely.
3. **The absent-slot trap.** `Pred.le` on an absent slot is false, so `not le` is true: a view
   missing a slot reads a want as met. `view` lists every asset of `proposal.assets`; keep it that
   way when the balances come from the stored Book (`view_total`,
   `Example.absent_slot_reads_as_met`).
4. **Zero want.** `atLeast a 0` is `Pred.all []`. Never compute `n - 1` in `Nat`
   (`nat_predecessor_encoding_refuses_zero_want`).
5. **Credit only in named assets.** `reallocate` refuses a credit in an asset the destination's
   proposal does not name. Otherwise `exit`, which pays only named assets, strands value in a closed
   seat. Keep that check, and say so where the Batch is built.
6. **Exit never reads the clause.** Do not route exit through the instance's law or any
   contract-side check; T3 (b) is only true because `step`'s exit branch never consults `clause`.
7. **Distinct seat accounts** are what make "closing one seat never debits another" true (`Inv`'s
   `distinct`). With coordinates = H(offer transaction) this is a collision bound, not a check;
   state it as such.
8. **Signature binds outcome.** As in the activity, the signed effect digest commits to the decided
   posts. A reallocation whose result changed between plan and submit must fail the signature
   check, not settle differently. This is also why seats matter: offers tolerate movement; the exact
   signed plan does not.
9. **`decide +kernel` on Books.** L7's examples reduce `DFinsupp` / `Finset` in the kernel. They
   compile in seconds at that size, but do not grow them; kernel-evaluate small worlds only. The
   executed acceptance run is the evidence for real flows.
10. **Merge interaction.** resume-view bumps the activity record frame and removes `conflict`; the
    activity-metering range bumps it too. Adding `heldSeats` to the record is another frame bump:
    coordinate with ROOT on the frame number and land after them.
11. **Builds.** persvati is Ember's laptop and overloaded; rented boxes are being chosen.
    - Never let lake fetch or build Mathlib: if a build starts compiling Mathlib, stop, because your
      clone is not warm. I burned 10 minutes of hbox doing that during the hold.
    - `LEAN_NUM_THREADS ≤ 4`, `uptime` first. Single-file checks with `lake env lean <file>`; the
      umbrella once, at the end.

## 3. Definition of done

- Every T3 statement is restated over the stored world and holds of the Host's committed intent.
- The receiver theorems above.
- The acceptance rows E1–E9 executed and green on a scratch world (`results.json` + log).
- The gate green, the Host closure pin and build surfaces regenerated.
- The commit says what broke: the registry Kind (re-genesis every Store), new frames, any activity
  record frame bump.
- One MERGE-QUEUE line.

## ROOT RULING (2026-10-05) on the open design point: who may reallocate
A bare `reallocate` or `mint` signed by whoever holds a capability on the instance object is REFUSED as a route.
That is operator reallocation, and it is the weaker design.
- `reallocate` and `mint` exist only as Plan actions emitted by the instance's own package method. The capability holder may
  INVOKE that method (an ordinary native Objective invocation on the instance object, admitted by re-execution through
  ObjectiveBendNativeAdmission). The reallocation's content comes from re-executing the contract code, never from a
  signer's say-so. Every touched seat's offer-safety law then judges it, exactly as L7 does.
- `offer` and `exit` stay directly signed by the offerer. Exit never reads the contract's clause.
- If the Plan action type cannot carry seat actions yet, extending it is the first item of this work, not a reason to ship
  the operator route. State in the docstring: offerers are protected by offer safety, exit and conservation; the contract
  can propose only what its code computes.
