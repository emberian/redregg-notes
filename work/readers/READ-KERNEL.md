# READ-KERNEL — whole-file read of nanodregg `Kernel/` at origin/main f9657bd (2026-10-24)

Reader: one sub-Opus, read-only. Nothing in `~/dev/nanodregg` was edited. Tags: **READ** (path:line),
**MEASURED** (a command I ran), **INFERRED** (my reasoning, not checked by a build or a run).

## Verdict

I read the whole deployed path: `Kernel/World.lean` (1851 lines), `Turn.lean`, `Cell.lean`, `Value.lean`,
`Check.lean`, `Bounds.lean`, `Trie.lean`, `TrieBinding.lean`, `Sim.lean`, and all seven `Kernel/Receive/*`
files (Call, Derive, Authority, Ledger, Submit, Audit, Follow). I also read `Proofs/Receive.lean`,
`Proofs/Audit.lean` and `Proofs/Lawful.lean` whole. I read the statements, and the regions around them, of
every theorem the brief names: `audit_ok`, `stale_behind_forever`, `object_history_chain`, `admit_value`,
`admit_row_touch` (KERNEL-65), `audit_package_fixed` (KERNEL-64), `receive_congr`, `submit_object_head`,
`submit_refused_final` and the refusals-head family, `fold_refusals_bounded`, `chain_binds` /
`fold_reaches_host`, plus the retry-window family in Journal.lean and the whole-trie binding. That is about
9,800 of the layer's 36,789 lines read in full, and about 2,500 more in regions. Most of the 2,346-line
`Proofs/Trie.lean` and the 3,062-line `Sim/Gen.lean` went unread.

The kernel's own transition is careful. I found no `partial`, `unsafe`, `native_decide`, `sorry`,
`implemented_by` or `extern` anywhere in `Kernel/` (MEASURED). Every `CollidesAmong` list I checked is built
from the theorem's own objects and is not provable from the premises. The finality and conservation theorems
say what their names say.

**The three worst things:**

1. **The receivers run on the Host's current cells before any pin is checked.** `submit` runs `receive`
   first and `World.admit`'s pin check second. So a call whose pin is stale gets the verdict of whichever
   receiver or law fails on the new state: `lawDenied`, `program`, `missingCell`, `noGrant` and so on. That
   verdict is authenticated, so `judge` RECORDS it. It is charged to the member's `refusalsPerWindow`, and
   the txId becomes final. This defeats KERNEL-54's stated purpose for every receiver refusal ("honest
   contention must not spend the spam budget"). It also contradicts two claims in the code: "an AHEAD stale
   is not final" (Submit.lean:147) and "World.admit's pin check refuses the Turn when the Host's cells are not
   what the signer saw" (Call.lean:9-11). (DEFECT)
2. **No receiver retires anything but a grant** (Derive.lean:329 is the only `.retire`). The kernel's
   parent-retirement machinery for rows is unreachable on any audited log: `checkRowsRemain`, `dropHeads`,
   `dropHeadsU`, KERNEL-63's seal of retired heads, and the parent-tombstone disjunct of the row and range
   stale theorems. Objects, accounts and members are immortal. Retirement credit (KERNEL-15/19) can never
   reclaim them, so the one World storage budget only falls. (DEBT/QUESTION)
3. **Documentation that lies about authority and reachability.** `Body.transfer` and `Body.credit` say
   "through `via`'s grant chain for `mutate`" (Call.lean:85, :90); the code requires `.transfer`/`.credit`
   and KERNEL-60 says mutate moves no value. `duplicateEffect` says "no receiver does: a probe meets it"
   (Call.lean:175, echoed in Gen.lean's `planted` docstring), but an invoke whose run returns two transfers
   from one account reaches it, and LedgerNext.lean:709 relies on it being reachable. The decision file
   still carries KERNEL-17 "the journal is not pruned … Status: open" (decisions/kernel.md:280-292), which
   KERNEL-33 reversed. (DEBT)

---

## Findings, ranked

### DEFECT

#### D1. A stale pin is judged by the receivers on the CURRENT cell; their refusal is recorded, charged and final

- **Where (READ):**
  - `Kernel/Receive/Submit.lean:32-44` (`submit`: journal → refusedAnswer → `receive` → `World.admit`).
  - `Kernel/Receive/Submit.lean:158-169` (`judgeBy`: only `.rejected (.stale _)` is declined; everything
    else authenticated is recorded).
  - `Kernel/Receive/Call.lean:422-423` (`pinned` returns `w.live E c`, the Host's current cell, whatever the
    pin's digest says).
  - The receivers then judge that cell: `Derive.lean:146-155` (`write`: `readKind`, then
    `X.program.judge … old new` with `old := stateOf cell` of the CURRENT cell), `Derive.lean:219-228`
    (`invoke`: the run on the current state), `Ledger.lean:101-115` (`transfer` reads current balances),
    `Authority.lean:33-47` (`walk` reads the current grant, and a retired grant is `missingCell`).
- **What is wrong.** The Turn's pins are the caller's observation. They are compared only inside
  `World.admit` (`touchCheck`, World.lean:999-1001). `receive` runs first, on the Host's World, before that
  comparison. When the pinned cell has moved (BEHIND) or the pin names a future version (AHEAD), any receiver
  or law that fails on the new state refuses first. That refusal is not `stale`, so `judgeBy` records it:
  `authenticatedBy` passes, then `World.refuse`.
- **Why it is wrong.**
  - KERNEL-54 (decisions/kernel.md:2539) exists so that "honest optimistic concurrency" does not spend the
    flood budget. Its "What it does NOT fix" lists refusals "that depend on UNPINNED World state". This class
    depends on PINNED state that moved, and no entry names it.
  - Submit.lean:147-148 says "an AHEAD stale is not final". A recorded receive refusal is final
    (`submit_refused_final`, `submit_refused_never`), so an AHEAD call refused by a law becomes final.
  - Call.lean:9-11 claims `World.admit`'s pin check refuses the Turn when the Host's cells are not what the
    signer saw. Admission is never reached.
  - The recorded code is wrong by law 7. The refusal's real cause is a stale read, but it is recorded and
    answered as `lawDenied` or `program`.
- **Mutation / input (INFERRED from READ code; not run).**
  - (a) BEHIND, honest contention. Object O has an extra law "slot 16 strictly increases". A pins O at
    version 3 (slot16 = 4) and signs `write O {0 ↦ 5}`. B's `write O {0 ↦ 6}` lands first (version 4).
    A's call: `write` judges `old = 6 → new = 5`. The verdict is `refused lawDenied`, verified, so it is
    recorded. A's budget falls by one, and the txId is final as `lawDenied`. With `touchCheck` reached it
    would have been `stale`, declined and unrecorded.
  - (b) AHEAD, honest pipelining. A signs write #1 (pins v3), then write #2 pinning the version #1 produces
    (v4), with a law that judges the step. #2 arrives first and is judged on v3. `lawDenied` is recorded,
    and #2 can never land after #1. Without the receive refusal it would have been AHEAD-stale (declined,
    not final) and admissible once #1 landed.
  - (c) The same with an escrow's release/refund race (`program` from the method), or a grant revoked
    between observation and landing (`missingCell` from `readKind`).
- **Side effect (INFERRED).** A call with garbage pins pays a full derivation before it is declined `stale`
  unrecorded: a signature verify plus up to `treeTicksMax` = 131072 ticks of LANG run. Checking the pins
  before `receive` would make stale the cheap refusal it was designed to be.
- **What would decide it.** A kernel-sim arm with two writers on a lawed data object, expecting
  `declined stale` for the loser and asserting that the loser's refusal count did not move.
- **Severity: DEFECT.**

### DEBT

#### B1. Parent retirement for rows is unreachable on every audited log; objects, accounts and members are immortal

- **Where (READ):**
  - `Kernel/Receive/Derive.lean:329` (`revoke`, the only receiver that emits `.retire`, and only at a cell
    read as a grant).
  - `Kernel/World.lean:1317-1342` (`dropHeads`, `dropHeadsU`), `:1391-1401` (`checkRowsRemain`), and
    `:1246-1249` (`orphanRow` for a parent the turn retires).
  - KERNEL-63 (decisions/kernel.md:3107).
  - `Proofs/ObjectHead.lean:16-18`: `audit_object_head` proves an object live at an audited log's start is
    live at its end.
  - `Proofs/Versions.lean:25-28` (the `w'.entry parent = some .tomb` disjunct).
- **What is wrong.**
  - Heads are declared only by `create` at the object it births (Derive.lean:132-136).
  - No receiver retires an object. `audit_object_head` makes that a theorem.
  - So on any log the follower accepts, `dropHeads` drops nothing, `rowsRemain` never fires, and the
    parent-retired disjunct of `row_stale_behind_forever` / `range_stale_behind_forever` is never the case.
  - The code is reachable only by hand-made Turns. `World.fold` admits those, and the audit refuses them
    `eventMismatch`.
- **Why it matters.**
  - The rows parent-retirement design (KERNEL-46/48/63, the overlay retains, the floor reset and its tooth
    `rowPin_old_floor_recurs`) is machinery with live-sounding names that no deployed path exercises.
  - Storage retirement credit (KERNEL-15/19) reaches only grants. Every object, account (`account` opens one
    for ANY `owner` id, Ledger.lean:90-91) and member cell is permanent, so the one World allowance only
    falls (also Q3).
- **Mutation.** Delete `checkRowsRemain` from `checkWith` (World.lean:1414). Every audited path is unchanged
  (INFERRED). Only kernel-sim's forged turns could notice.
- **Severity: DEBT** (and the design question in Q3).

#### B2. `Body.transfer` / `Body.credit` docs grant `mutate` the authority KERNEL-60 removed

- **Where (READ):** `Kernel/Receive/Call.lean:84-86` ("with the authority of `src`'s owner (directly, or
  through `via`'s grant chain for `mutate`)") and `:89-91` (credit: "through `via` for `mutate`").
- **The code:** `Ledger.lean:105` (`ownerAuthority … (.transfer 0) via`) and `:130` (`.credit 0`).
  `Call.lean:27-29` itself (`Right.mutate`: "on an account it authorises nothing").
- **Why it is wrong.** A comment that lies about who may move value, on the type every client and
  LANG author reads. KERNEL-60 (decisions/kernel.md:2933): "`mutate` moves no value."
- **Mutation.** A transfer through a `mutate` grant is refused `grantRight` (kernel-sim arm
  `transfer-mutate:grantRight`); the doc says it is admitted.
- **Severity: DEBT** (lie in a comment).

#### B3. `duplicateEffect` is documented unreachable by receivers; it is reachable

- **Where (READ):**
  - `Kernel/Receive/Call.lean:175` ("a receiver gave one cell two effects (no receiver does: a probe meets
    it)").
  - `Kernel/Sim/Gen.lean:2761-2768` (`planted`'s docstring: "`duplicateEffect`, which no receiver can
    produce and the probe meets straight at `sealTurn`").
- **What is wrong.**
  - `invoke` returns a run's calls, and `deriveCalls` derives them as the object (Derive.lean:229-231).
  - A method returning `[transfer (of self a) X 1, transfer (of self a) Y 1]` derives two effects at the
    object's account, and `effectsPinned` (Call.lean:483-488) refuses `duplicateEffect`.
  - `Proofs/LedgerNext.lean:709` and `:765` rely on exactly that refusal ("no other receiver of the same
    tree moved either balance").
- **Why it matters.**
  - The comment hides a real limit of the receivers: one call cannot debit one account twice, so a method
    cannot pay two parties from one account in one Turn.
  - The sim's claim that `duplicateEffect` can only be met by a probe means no journey row tests the honest
    path to it.
- **Mutation.** A two-transfer method in `lang-journey` meets `refused duplicateEffect` on the signed path.
- **Severity: DEBT** (comment lie; a sim plant that does not exercise the reachable path).

#### B4. KERNEL-17 and other decision entries contradict the code they describe

- **Where (READ):** decisions/kernel.md.
  - `:280-292` (KERNEL-17 "The journal is not pruned … (72 bytes, charged in `Turn.growth`)", `Status: open`)
    against World.lean:1450-1462 (`kept`, `pruneJournal`) and Turn.lean:211-215 ("Its journal entry is not
    growth").
  - `:568` (KERNEL-23 `Status: proposed`) against the trie as built (KERNEL-30).
  - `:463`, `:579`, `:637`, `:662` (titles "not yet built" for KERNEL-23/24/25/26, all built).
  - `:2816` (KERNEL-55 `Status: PROPOSED`, though `:2818`/`:2824` record it RULED and BUILT).
- **Why it is wrong.** The charter forbids a decision entry the code no longer matches. A reader who opens
  KERNEL-17 learns the opposite of what the World does: entries ARE pruned, and absence past
  `journalForgets` is `forgotten`.
- **Severity: DEBT.**

#### B5. Three duplicate detectors for one fact (law 1)

- **Where (READ):**
  - `Kernel/Check.lean:34-39` `firstDup` (Ord, a `TreeSet`; touches, nullifiers, op keys, creates,
    effects).
  - `Kernel/Receive/Call.lean:537-540` `dupBy` (DecidableEq, O(n²); a call's row effects).
  - `Kernel/World.lean:1356` (`rowsRun`'s inline `find?`/`filter` count, O(n²); a turn's row slots).
- **Why it is wrong.** Law 1: "one of everything". Their semantics differ.
  - `firstDup` is correct only under a lawful `Ord`, which is why `row_stale_behind_forever` and the
    InvokeTree route carry `[Std.TransOrd D] [Std.LawfulEqOrd D]` (KERNEL-54 AS BUILT, kernel.md:2632).
  - The two row detectors need no order.
  - So the touch-uniqueness check and the row-uniqueness check rest on different premises for the same
    property.
- **Severity: DEBT.**

#### B6. `rowsRun` re-checks bounds `checkBounds` already checked; `rowStepOn`'s declare re-checks `rel < 256`

- **Where (READ):** `World.lean:1352-1355` (`rowsMax`, `rangesMax`, `rel < 256`, `k.size ≤ keyBytesMax`,
  all already in `checkBounds`, World.lean:911-921) and `:1235` (`rel < 256` again at a declare).
- **Why it is wrong.** In `checkWith` these run after `checkBounds` and cannot fail: refusals that cannot be
  reached on the deployed path. They are twins of one bound under one name (`overBound .rows`).
- **Mutation.** Delete World.lean:1352-1355. `World.admit` is unchanged on every input (INFERRED: `checkWith`
  runs `checkBounds` first). Only direct callers of `rowsRun`, the proofs and `rowsAfter`, could tell.
- **Severity: DEBT.**

#### B7. `World.admit`'s journal and refused-final checks are unreachable from `submit`

- **Where (READ):** `Kernel/Receive/Submit.lean:33-37` (journal, then `refusedAnswer`) against
  `Kernel/World.lean:926-932` (`checkJournal`: the same two lookups, the same two refusals).
- **What is wrong.** On the Host path `submit` has answered both before `receive`, so `checkJournal`'s
  `replayed` and `refusedFinal` arms are dead there. They are live only for `World.fold` and the audit.
- **Why it matters.** The pre-check is justified (Submit.lean:4-6: a retried rotation must not be
  re-judged), but it is a second copy of the same two reads. `refusedAnswer` and `checkJournal`'s inner
  match are twins of the KERNEL-44 finality read, and the Proofs carry both (`submit_refused_final` reads
  `refusedAnswer`, `admit_refusedFinal` reads `checkJournal`).
- **Severity: DEBT.**

#### B8. `rowView` names a missing relation `rangeUnpinned`

- **Where (READ):** `Kernel/Receive/Call.lean:432-437`. `rangeOf … = none`, which happens when the
  relation has NO HEAD (World.lean:1121-1125), refuses `.rangeUnpinned parent rel`. The constructor's own
  doc (Call.lean:202) says "a run read a range … the caller did not sign".
- **Why it is wrong.** Law 7. The caller DID sign the range (`u.ranges.filter …` selected it); the
  relation does not exist. The kernel's own name for this is `noRelation` (World.lean:1380). A client told
  `rangeUnpinned` re-signs the same range and gets the same answer.
- **Mutation.** Sign a range on `(obj, rel)` for an undeclared `rel` and invoke a method that reads it:
  the answer is `refused rangeUnpinned` (INFERRED).
- **Severity: DEBT** (a refusal by the wrong name).

#### B9. One wire name for two different refusals: `Verdict.name` is not injective

- **Where (READ):** `Refusal.missingCell` / `Reject.missingCell` (Call.lean:131, :231; World.lean:78,
  :148), `Refusal.rangeTooLong` / `Reject.rangeTooLong` (Call.lean:205, :267; World.lean:118, :168), and
  `Refusal.duplicateRow` / `Reject.duplicateRow` (Call.lean:210, :269; World.lean:120, :169).
  `Verdict.name` (Submit.lean:71-73) returns the bare constructor name.
- **Why it is wrong.** `Refusal.name_injective` (Proofs/Receive.lean:15) and `Reject.name_injective` hold
  per type, but law 7 is about the name on the wire. `codeName` (Submit.lean:91-92) maps two different
  codes to one string, so a client reading names cannot tell a receive `missingCell` (an unpinned-but-named
  cell is absent) from a kernel `missingCell` (a write or retire of an absent cell).
- **Severity: DEBT.**

#### B10. `spendAt`'s "ledger full" refusal reuses the "too much" name

- **Where (READ):** `Kernel/Receive/Authority.lean:78-84` (`short` is returned both for
  `units > left` and for `i > ledgerSpendsMax`).
- **What is wrong.** For a carve, `checkParent` passes `.grantWidens p` (Derive.lean:300-302). So a child
  grant that narrows its parent is refused `grantWidens` once the parent's ledger holds 257 entries.
  `transferSpent`/`creditSpent` document the double meaning (Call.lean:159-164); `grantWidens`
  (Call.lean:151-153) does not.
- **Severity: DEBT** (refusal by a misleading name).

#### B11. A public grant used by a non-member agent fails as `wrongKind`/`unpinned`, not `noGrant`

- **Where (READ):** `Kernel/Receive/Authority.lean:27`. `(readKind look agent kindMember).map …`
  propagates `readKind`'s own error.
- **Why it is wrong.** For an object agent (a nested call through a public grant) the answer is
  `wrongKind obj 4`. The docstring (Authority.lean:18-22) says "Anything else is `noGrant g`".
- **Severity: DEBT.**

#### B12. Theorems in a definitions module

- **Where (READ):** `Kernel/World.lean:1570-1595` (`bind_ok_iff`, `checkWith_rows`,
  `World.admit_eq_admitImpl` with `@[csimp]`).
- **Why it matters.** Law 8 says a module exports definitions OR proofs. A `@[csimp]` theorem has to be in
  scope wherever callers compile, which is a plausible reason. But World.lean is imported by nearly
  everything, so an edit to these proofs rebuilds the tree, which is the cost law 8 names. If it is a
  sanctioned exception, the exception should be recorded where `gates/closure.py` C3 can see it.
- **Severity: DEBT** (QUESTION: is there a C3 allow-row for it?).

#### B13. The header's order of checks omits four of them

- **Where (READ):** `Kernel/World.lean:14-19` lists "bounds → window → journal → shape → touches → value →
  nullifiers → charge → created ids". `checkWith` (World.lean:1406-1420) runs `checkRowsRemain`,
  `checkRanges` and `rowsRun` between nullifiers and charge, and `checkSteps` last.
- **Why it matters.** Which refusal a client sees for a multiply-bad Turn depends on this order (the KERNEL-7
  answers), and the header is what PROTOCOL and CLIENT read.
- **Severity: DEBT.**

#### B14. The kernel-sim forgery plant vanishes silently when the log has nothing to forge

- **Where (READ):** `Kernel/Sim/Gen.lean:2750-2756` (`match forge st.log with | none => st`).
  `forge` (Gen.lean:1519-1531) needs a write of a non-value key.
- **Why it is wrong.** "A falsifier that stopped falsifying." On a seed with no such write, the audit's
  re-derivation tooth (`eventMismatch` at the forged index) is not run, and nothing records that it was
  skipped. It is counted only in `refusedAsExpected`, not as a required arm. The forged-refusal arm just
  above it (`refusal-forged-code`, Gen.lean:2709-2719) uses `arm`, and its `none` case `failWith`s.
- **Mutation.** Make the generator produce no RAM writes. The run stays green with the forgery tooth never
  executed (INFERRED; whether some other seed always hits it is what would decide it).
- **Severity: DEBT.**

### QUESTION

#### Q1. A possession proof is not bound to a World

- **Where (READ):** `Kernel/Receive/Call.lean:467-469`
  (`possessionMessage = tagPossession ‖ sponsor ‖ next ‖ key`) and `Derive.lean:91`.
- **The question.** KERNEL-24 binds every call to its World, and decisions/ops.md:42 says "every signature
  over old bytes … possession proofs … NOT carried".
  - A carry keeps member ids (KERNEL-40), so a sponsor `S` of World A is `S` in carried World B.
  - The possession signature `S` received in A verifies in B. `S` can enrol the same key again there, or
    again in A, with a fresh `enroll` call: a second member cell holding that key, without the key holder's
    new consent.
- **What would decide it.** Is possession consent to "this sponsor, once, in this World", or to "this
  sponsor, anywhere"? If the former, the message needs the World's origin (and a nonce, or the sponsor's
  enroll ledger index). Either way ops.md:42's "possession proofs not carried" is false as written: nothing
  stops one from being carried.

#### Q2. `carry`'s `fromOrigin` is not checked against anything

- **Where (READ):** `Kernel/Receive/Follow.lean:221-224`. `fromOrigin` is a free parameter, and `Carried`
  (World.lean:302-308) has no origin field.
- **The question.** The new origin "commits" the lineage (Follow.lean:219-220, KERNEL-29), but the lineage
  committed is whatever the caller passes. `carry_inj` makes the origin bind `fromOrigin`; nothing binds
  `fromOrigin` to the World whose state was exported.
- **What would decide it.** Whether HOST's import check (HOST-28) compares `fromOrigin` to the exported
  base's own origin. If it does, the kernel signature is fine and the docstring should say so. If not,
  lineage is an operator's claim.

#### Q3. One World storage budget, with immortal objects and accounts and no per-member bound

- **Where (READ):** `Kernel/Receive/Ledger.lean:86-91` (`account` for any `owner`, no read),
  `Derive.lean:123-136` (`create`), and B1 (nothing but grants retires).
- **The question.** Any member can permanently spend the World's allowance (`overAllowance` for everyone
  after), and no receiver can give it back. KERNEL-15/16 record per-member budgets as a fork.
- **What would decide it.** Whether "a World whose allowance is spent refuses every further turn"
  (KERNEL-15) is acceptable once one member can cause it alone and nothing retires what it bought. This is
  the price of B1, not a separate defect.

#### Q4. `admit_row_touch`'s witness rows are existential and unrelated to the World

- **Where (READ):** `Kernel/Proofs/Rows.lean:793-797`.
  `∃ r0 r1, Canon r0 ∧ rowStep E w t r0 τ = .ok r1 ∧ rowAt E w'.rows (.row key) = r1.get …`.
- **The question.**
  - For insert, upsert and retract the act fixes `r1`'s leaf at the slot, so the per-act corollaries
    (`admit_upsert_row` etc.) say something.
  - For `.keep`, `r1 = r0` and `r0` is free, so the theorem says nothing about the slot.
  - The upsert's version is existential (KERNEL-65's own critique).
- **What would decide it.** Does any consumer apply `admit_row_touch` to a `.keep` or need the version?
  If so, the statement should name `r0` as the fold's prefix from `w.rows`.

#### Q5. A program refusal spelled `cancelled` and a member's cancel share one code

- **Where (READ):** `Kernel/Receive/Submit.lean:198-199`, `Audit.lean:39`, and
  `Proofs/Audit.lean:366-373` (`audit_unsigned_is_judged`: "a program refusal spelled `cancelled` is read
  as a program refusal").
- **The question.** The refusals LEAF is `.refused h code member` (World.lean:220). It does not hold the
  cancel field, so a phone reading the refusals trie against a head (`head_refusal_read`) sees the same leaf
  for both. The audit tells them apart; a head-only reader cannot.
- **What would decide it.** Whether `Program`'s `Refusal` results are restricted. I found no LANG site
  constructing `.cancelled`, `.staleRecorded` or `.eventMismatch` (MEASURED: grep over Lang/Kernel/Host/
  Protocol, non-proof). If they are restricted, say so in `Program`'s type or docstring. If not, the leaf
  needs the bit.

---

## Checked and found sound (so the next reader need not re-do them)

- **Escape hatches (MEASURED).** `grep -rn "partial def|unsafe def|sorry|implemented_by|@[extern"` and
  `grep -rln native_decide` over `Kernel/` returned nothing. The only `Classical` uses are three
  `byContradiction`s in proofs (RowsRange.lean:434, RowsSep.lean:164, Rows.lean:73). The one `@[csimp]` is
  World.lean:1586 (see B12).
- **`CollidesAmong` lists (READ, all 130 occurrences listed; statements read for about 35).** Every list is
  built from the theorem's own objects:
  - pin-input pairs (`pinPre`, `rowPre`);
  - `leafPres` of the two listings;
  - `inclPres` / `readPres` (the proof's climb bytes and the trie's path bytes);
  - `headPres` (link, roots and fold links of the given log);
  - `chainPres` / `foldPres` (bounded by the two logs);
  - `retryPres` (the retry's event and the log's events);
  - `bindingPres` (both tries' node and value inputs);
  - origin and account pairs.

  None is quantified away. The two-element ones are proved distinct inside the theorem (e.g.
  `stale_behind_forever` builds `pinPre_adv_ne`; `check_reads_kept` refutes the domain equality), so the
  disjunct cannot be satisfied by `p = q`. The "tooth" theorems whose conclusion IS a collision
  (`head_refused_not_absent`, `refusal_inclusion_wrong_leaf`, …) are refutations under `Separates`, not
  claims. `shadow_call_window` (Journal.lean:820) takes any `S ⊇ retryPres`, but it is the induction helper;
  its public form instantiates `S := retryPres t l`. I found no list that contains its collision by
  construction.
- **`touchCheck` against the pre-entry (READ, World.lean:999-1013).** It is sound because `checkShape`
  (one touch per cell, `firstDup`) runs before the `mapEx touchCheck` (World.lean:1410-1411), and a born
  id's touch is refused `bornTouched` later. Under a lawful `Ord`, every touched cell's pre-entry is its
  entry at the time of the touch. Under an unlawful `Ord`, two touches of one value cell would each subtract
  the pre-value (a mint). The value theorems carry `[Std.TransOrd D] [Std.LawfulEqOrd D]`, and the deployed
  `Digest` has both (Codec/Proofs/Digest.lean:24, :29).
- **KERNEL-44 finality (READ).** `submit_refused_final` / `submit_refused_never` (Refusals.lean:478-525):
  - A recorded call is answered `refusedFinal` below `h + 2·windowMax` and never admitted after.
  - The prune horizon outlives the call's window: `validUntil ≤ notBefore + windowMax` is checked by both
    `checkBounds` and `checkRefusedBounds`.
  - Carry drops refusals (World.lean:302-308), and old calls are `wrongWorld` in the new World.
  - Reachability: only `authenticated` verdicts inside the window are recorded. Early and late calls,
    `badSignature`, `unknownKey`, `wrongWorld` and `notPrecommitted` are declined. Whether the right
    verdicts are recorded is D1.
- **KERNEL-60 grant slots (READ, Call.lean:385-404, Authority.lean:67-94, Derive.lean:266-303).**
  - The ranges 16, 17, 1024..1280, 2048..2304, 2560..2816 and 4096+m are disjoint.
  - `spendAt` refuses past `ledgerSpendsMax` before writing.
  - `checkRights` forbids two counted kinds per grant.
  - The carve debits the immediate parent's ledger, and the child's ledger is spent through `spendVia` at
    the first link.
  - KERNEL-61's contiguity is what makes `ledgerLeft`'s `led.length` index right.
  - I found no mismatch with kernel.md:2919-2944.
- **Conservation (READ, Proofs/Value.lean:402-417).** `admit_value` is an equality, and `admit_floors` is
  exempt exactly for born ids' bytes. A born non-ROM id is unchecked by the kernel (Turn.lean:16-17 relies
  on the audit), but `FloorsBorn` (`admit_birth`) keeps a reborn-denomination mint out, because a fresh id
  has floor sum 0.
- **`audit_ok` (READ, Proofs/Audit.lean:275).** True, and close to definitional: `Honest`
  (Audit.lean:195-200) restates `auditStep` as a Prop. It is a correct characterization, and its strength is
  exactly `receive` + `recordedBy`'s determinism. It is not a vacuity, but it adds nothing beyond D1's
  semantics: an Honest log records whatever D1 records.
- **`receive_congr` (READ, Proofs/Receive.lean:38-51).** The premises are the origin, `w.live` at the pinned
  ids, and `rowView` equality. That is complete for `receive`'s reads (`Program` sees only `look`/`rv`).
  Note it is congruence in the CURRENT cells at pinned ids, not in the pin digests; that is the hinge of D1.
- **`audit_package_fixed` / `submit_object_head` (READ, ObjectHead.lean:232-306).** They say what they
  claim, over `audit` and `submit` (never a bare fold). The docstring is explicit that a bare fold is not
  covered.
- **`stale_behind_forever` (READ, Versions.lean:240-254).** W0 form: observed at `w₀` on the fold. The
  collision list is `[pinPre w₀, pinPre w']`, proved distinct.
- **`fold_refusals_bounded` (READ, RefusalsBound.lean:285).** It has no receive premise, and
  `refusalsFull_independent` shows the total cap binds where the per-member one does not.

## Files I did NOT read in full (lines)

Read in REGIONS only (statements and their neighbourhood):

| File | Lines |
|---|---|
| Kernel/Sim/Gen.lean | 3062 |
| Kernel/Proofs/Versions.lean | 1880 |
| Kernel/Proofs/Journal.lean | 1262 |
| Kernel/Proofs/InvokeTree.lean | 1028 |
| Kernel/Proofs/Rows.lean | 843 |
| Kernel/Proofs/Value.lean | 755 |
| Kernel/Proofs/RefusalsBound.lean | 626 |
| Kernel/Proofs/Refusals.lean | 573 |
| Kernel/Proofs/Local.lean | 564 |
| Kernel/Proofs/Fold.lean | 513 |
| Kernel/Proofs/Carry.lean | 496 |
| Kernel/Proofs/RefusalsHead.lean | 481 |
| Kernel/Proofs/Logic/History.lean | 456 |
| Kernel/Proofs/StaleOnly.lean | 430 |
| Kernel/Sim/Required.lean | 371 |
| Kernel/Proofs/ObjectHead.lean | 316 |
| Kernel/Proofs/Origin.lean | 243 |
| Kernel/Proofs/TrieBinding.lean | 153 |

Not read:

| File | Lines |
|---|---|
| Kernel/Proofs/Trie.lean | 2346 |
| Kernel/Proofs/RowsHead.lean | 1392 |
| Kernel/Proofs/RowsComm.lean | 966 |
| Kernel/Proofs/Ledger.lean | 943 |
| Kernel/Proofs/RowsRange.lean | 892 |
| Kernel/Proofs/LedgerNext.lean | 802 |
| Kernel/Proofs/RefusalsCounted.lean | 695 |
| Kernel/Proofs/Rooted.lean | 658 |
| Kernel/Proofs/InvokeNext.lean | 597 |
| Kernel/Proofs/Weight.lean | 574 |
| Kernel/Proofs/Admit.lean | 535 |
| Kernel/Proofs/Cells.lean | 525 |
| Kernel/Proofs/Authority.lean | 484 |
| Kernel/Proofs/InvokeTreeWitness.lean | 467 |
| Kernel/Proofs/WriteNext.lean | 445 |
| Kernel/Proofs/InvokeWitness.lean | 412 |
| Kernel/Proofs/RootedDeployed.lean | 345 |
| Kernel/Proofs/RowsHeadRead.lean | 319 |
| Kernel/Proofs/TrieRetain.lean | 298 |
| Kernel/Proofs/Refuse.lean | 288 |
| Kernel/Proofs/CellsFit.lean | 283 |
| Kernel/Proofs/JournalHead.lean | 266 |
| Kernel/Proofs/Tree.lean | 256 |
| Kernel/Proofs/Logic/Frame.lean | 255 |
| Kernel/Proofs/TrieMap.lean | 251 |
| Kernel/Proofs/Frame.lean | 243 |
| Kernel/Proofs/Logic/Triple.lean | 241 |
| Kernel/Proofs/RowsSep.lean | 225 |
| Kernel/Proofs/Bytes.lean | 173 |
| Kernel/Proofs/Logic/HeadRead.lean | 172 |
| Kernel/Proofs/Check.lean | 152 |
| Kernel/Proofs/Logic/HistoryWitness.lean | 149 |
| Kernel/Proofs/RotateStale.lean | 116 |
| Kernel/Proofs/Budget.lean | 109 |
| Kernel/Proofs/TrieOrder.lean | 66 |
| Kernel/Proofs/RootedFold.lean | 60 |
| Kernel/Proofs/RowsOverlay.lean | 55 |
| Kernel/Proofs/CarryRooted.lean | 40 |
| Kernel/Proofs/RowsRangeDeployed.lean | 36 |
| Kernel/Sim/Deployed.lean | 35 |
| Kernel/Sim/Shadow.lean | 32 |
| Kernel/Proofs/LedgerDeployed.lean | 31 |
| Kernel/Sim/Main.lean | 17 |

The unread `Proofs/*` are where a statement weaker than its name would hide. My reading of the deployed
definitions says nothing about them. A follow-up reader should start with `Proofs/Weight.lean` (the
potential bound HOST reads by name), `Proofs/Ledger.lean` (`transfer_authorized`), and
`Proofs/RowsRange.lean` (the range pin's soundness).
