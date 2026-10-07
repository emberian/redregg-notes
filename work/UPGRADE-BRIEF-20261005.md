# UPGRADE brief (2026-10-05): the governed upgrade turn, built on OBJECT-RECORD R1/R2/R3

**Author.** SCHOLAR-OS, who built R1–R3 and now stops as a consultant.

**Tags.**
- **READ**: I read the code at the named commits.
- **RULING**: a root decision (`work/ROOT-PROGRAM-MODEL-DECISIONS-20261004.md`, section "Root rulings on the 2026-10-05
  scholar reviews", UPGRADE bullet).
- **PROPOSED**: my design. Override it if the code says otherwise.

## 0. Ground truth you build on (READ)

**Branches** (burst-lane1 `ember@162.43.189.7:/srv/lanes/object-record/src`, queued in `MERGE-QUEUE.md`):
- R1 `feb33aeb`;
- R2 `c42ce907` + `13a4e7cc` on `lane/object-record-r2m`;
- R3 `0b62c6d1` on `lane/object-record-r3`.

All of them sit on HISTORIAN `4015fd72`, which sits on BREAD resume-view `46b9d4fd`, which sits on ACTIVITY-NATIVE. Base on whatever the
merge keeper has landed. If R1–R3 are not on main yet, fetch `lane/object-record-r3` (persvati keeps the R1/R2 git history
under `/home/ember/workbox/claude-lanes/object-record/src`; its `.lake` was removed).

**`Kernel/ObjectRecord.lean` (R1):**
```lean
inductive UpgradePolicy | frozen | governed (authority : Pred) (floors : List Pred)
structure ObjectRecord where
  id : Digest; pin : Digest; schemaVersion : Nat; law : Pred
  upgrade : UpgradePolicy; continuity : Nat; payer : AccountId
structure Facts where subject : SubjectId; height : Nat; target : Nat; turn : Nat   -- turn: 1 birth 2 delivery 3 write 4 create
def admitWrite (r : ObjectRecord) (f : Facts) (old : Option Data) (new : Data) : Except WriteRefusal Unit
def UpgradePolicy.permits : UpgradePolicy → UpgradePolicy → Bool       -- may only tighten
theorem admitWrite_ok_iff, admitWrite_lawDenied_fails, admitWrite_payer_irrelevant,
        frozen_absorbing, strengthens_sound, permits_tightens, record_roundTrip
```

**`Kernel/ObjectiveActivity.lean` (R2/R3):**
- `objectCell domain object` holds the record under `Role.object` (tag 4); `readObject`; the `create` turn.
- `birth` refuses `notAnObject` and `pinMismatch`.
- `judgeWrite` / `judgeWritten` wrap BREAD's `stateWrite` result (`StateWritten {before, after, post}`).
- `Birth/Delivery/StateWrite.write_judged`.
- Each activity `Record` already carries its OWN `pin`, and `deliver` loads `record.pin`, not the object's pin. Drained activities
  therefore keep running their old package with no change to delivery.
- `AwaitOutcome.upgraded` already exists in the outcome sum, and every activity's response type must type it at birth
  (`kernelOutcomes`).
- R3: envelopes are `ObjectiveInvocationClaim.Capacity`, priced by `ObjectiveTariff.Tariff.workOf`, admitted only if
  `Config.covers`.

**Other lanes' pieces you rely on:**
- HISTORIAN's exhaustion/abandonment turns, record frame v4/v5 with `tried`, and `abandon_delivery_exclusive`.
- BREAD's `ObjectState {version, value}` in its own state cell, and field-edit Plan writes (`keep | set | add`). Births are never
  blind: a first segment may not `set` present state (`blindWrite`).

## 1. What to build (RULING, with my mechanism PROPOSED)

The object record gains a phase:
```lean
inductive UpgradePhase
  | open
  | draining (next : Pending) (deadline : Nat)          -- ADOPTed, old activities still live
  | migrating (next : Pending) (cursor : MigrationCursor) -- multi-turn MIGRATE, object closed
structure Pending where
  pin : Digest; stateType : Ty; migration : MigrationTerm; law : Pred
  upgrade : UpgradePolicy; dropped : List String          -- fields the migration explicitly drops (linearity)
  rebirth : List Digest                                    -- activity ids chosen for REBIRTH
```

**ADOPT turn** (one admitted turn).
- **Authority.** The signer's request facts satisfy `governed authority _`, where `frozen` refuses by name. The receiver
  additionally checks a capability on the object (objectHolder, as for `create`).
- **Policy.** `UpgradePolicy.permits old.upgrade next.upgrade`.
- **Floors.** For each floor `f`, `Pred.Sat` decides `allL [next.law, not f]`. It must return `.unsat` with a certificate that
  `checkAll` accepts (`certificate_unsat`). `Pred.Sat` returns `none` for `witnessed`, `hashEq`, `ran` and for DNFs past
  `dnfCap = 1024`; refuse those floors at publish so they never reach here.
- **Migration.** It type-checks as `oldStateType → newStateType` with the REAL checker, and is linear (§3 trap 3).
- **Commit.** Write the record with `phase := draining next (height + drainPatience)`, where `drainPatience` is declared and at
  most a config ceiling, and bump `continuity`.

**While draining** (RULING: "no new births or calls unless the old state type is a subtype of the new").
- A birth is refused `draining` unless `stateSubtype old new`. When it is a subtype, the birth must name `next.pin` (not
  `record.pin`) and runs on the unmigrated state.
- A direct write (`writeState`) is refused, or judged exactly like an old activity's write (see the next point). Pick one, and
  write it down.
- **An old activity's write** (RULING) is admitted only if `migrate(s')` type-checks at the new type AND satisfies `next.law`, on
  top of today's `admitWrite` under the OLD law. That is what makes the final MIGRATE unable to fail. It costs one migration run
  per drained write, so price it: `Config.covers` must include the migration's ticks in the envelope (R3's `covers` is the place).

**ABORT after the deadline.** At or after `deadline`, an `abortDrained` turn may be submitted by anyone, paid from the
activity's escrow like HISTORIAN's abandonment. It resumes the old activity with `upgraded`, and spends the await nullifier so
the activity can never also be delivered. Mirror `abandon_delivery_exclusive`. Since resuming with `upgraded` runs old code, it
runs on the old package and its write is still judged as above. If you would rather end the activity without resuming it, end
it `faulted "upgraded"` and say so: the ruling says "ABORT with `upgraded`".

**MIGRATE.** It runs when no live activity pinned to the old package remains (trap 4). It:
- runs `migration` on the current `ObjectState.value` and types the result at `newStateType`;
- judges it with `admitWrite nextRecord ⟨…, turn := 5⟩ (some migrated) migrated`, so state clauses must hold and two-state
  clauses see no change (design C);
- writes `pin`, `law`, `upgrade`, `schemaVersion + 1`, `continuity + 1` and `phase := open`, with the state bumped to
  `version + 1`.

Large states use `migrating` over several turns. The object is closed during them (births, calls and writes are refused
`migrating`). A cursor cell holds the progress, and any holder of the upgrade capability advances it one envelope at a time
(RULING, OS W3).

**REBIRTH** (RULING, replaces REPLAY; there is no MAP). Chosen per activity at ADOPT. At MIGRATE, or at that activity's
ABORT, the activity is ended and re-born on the new package from `record.input` on the migrated state. "Restartability
checked at publish" means:
- the new package's entry domain types the OLD stored input (check `typeData` on the stored input bytes at ADOPT, per chosen
  activity);
- its first segment can only `keep`/`add` on present state, which BREAD's never-blind rule already enforces at birth.

Have publish record a `restartable` flag only if you can state what it guarantees.

**Epoch rule** (RULING C3). A Core4 or codec epoch change is always a re-genesis. Never try to drain across one.

## 2. Theorems (statements, with their premises; pin every one with `#assert_axioms`)

1. `adopt_requires_authority`: ADOPT admitted → `record.upgrade = .governed a fl` ∧ `eval a facts facts = true` ∧
   `UpgradePolicy.permits record.upgrade next.upgrade`.
2. `frozen_never_adopts`: `record.upgrade = .frozen` → ADOPT refused `frozen`. Use `frozen_absorbing` for later policies.
3. `adopt_floors_entailed`: ADOPT admitted → `∀ f ∈ floors, ∀ old new, eval next.law old new = true → eval f old new = true`.
   The premise is the certificate check. The proof goes through `certificate_unsat`, so read its exact statement in
   `Pred/Satisfiable*` before writing yours.
4. `draining_refuses_births`: phase `draining` ∧ `stateSubtype old new = false` → birth = `.error .draining`.
5. `drained_write_migratable`: a drained activity's write admitted → `∃ m, migrate s' = some m ∧ TypedAt new m ∧
   admitWrite next … = .ok ()`.
6. `migrate_cannot_fail`: every write since ADOPT was admitted (theorem 5), no old-pinned activity is live, and the envelope
   covers it → MIGRATE is admitted. This is THE ruling's promise. If its premise has to be weakened, stop and report; don't
   ship a weaker statement under the same name.
7. `migrate_judged`: MIGRATE admitted → the post-state satisfies `next.law` ∧ `schemaVersion` and `continuity` each rose by 1
   ∧ `phase = open`.
8. `abort_after_deadline_exclusive`: an admitted `abortDrained` spends the await claim ∧ requires `deadline ≤ height`. No
   delivery of that await is accepted after it (reuse `spent_claim_never_accepted`).
9. `rebirth_from_stored_input`: a rebirth's new record has `input = old.input` ∧ `pin = next.pin` ∧ generation 0 ∧ a first
   write that is never blind.
10. `upgrade_payer_irrelevant`: authority and every judgment ignore `payer` (extend `admitWrite_payer_irrelevant`).

Forbid yourself vacuous forms. A theorem whose premise is the structure field it concludes is a restatement; state it about
the admitting FUNCTION (`adopt config snapshot height request = .ok a → …`), as R2's `birth_refuses_*` do.

## 3. Traps I know of

1. **There is no Core4 type codec.** `Theory/ObjectiveBendTypes.Ty` (`natural | label | boolean | variable | arrow reuse
   quantity domain codomain | emptyRow | field | specification | prototype | custody | variant | computation`) has no
   `StreamCodec`. That is why R1's record has `schemaVersion` but no `stateType`, and why R3 could not cache the package
   type-check verdict at publish: `loadProgram` still re-checks the whole artifact every turn, now paid via `Config.covers`
   typeFuel. **Build `StreamCodec Ty` first**, with `ty_roundTrip`, a strict decoder (`framed_canonical` style), and codecs for
   `Reuse`/`Quantity`. It unblocks `stateType` in the record, `Pending.stateType`, and the verdict cache. The verdict cache is
   a cell keyed by pin holding the checked definition's domain and type. That is sound because checking is a deterministic
   function of committed bytes and a checker change is an epoch, which is a re-genesis.
2. **There is no declared state type anywhere yet.** BREAD's `applyWrite` checks only the field shape, and nothing types
   `ObjectState.value` at a declared `Ty`. Derive the state type from the pinned package (the `write` field of the Plan type in
   the checked definition), or add it to `create`. Either way, MIGRATE and theorem 5 need `TypedAt`, so do this before the
   upgrade turn.
3. **Linearity.** Core4's linear checking is at-most-once (affine). A migration `Old → New` that silently forgets a field
   type-checks. Require `dropped : List String` and check at ADOPT that every old field is either read by the migration term
   or named in `dropped`. That is a syntactic check over the term's field projections; say exactly what it inspects. Faré's
   ch. 5 is the source (SCHOLAR-OS-LINEAGE §F1).
4. **"No old activity remains" is not computable today.** Activities are derived (record cells keyed by object), and the
   kernel cannot enumerate cells. I told HISTORIAN that ObjectRecord stores no activity list. Add a COUNTER instead: either
   `live : Nat` per object, or per pin as `liveOld`. Increment it at birth, and decrement it at done, faulted, abandoned,
   aborted and reclaimed. Every one of those turns is HISTORIAN's or its successor's (ACTIVITY-RETENTION-PAYERS). Agree on
   one function (`ObjectRecord.release`) that they call, and state `live_counts` (the counter equals the number of awaiting
   records with that pin). Without it, MIGRATE either waits forever or migrates under live old activities.
5. **Drained writes see the OLD law and must also pass the NEW one.** Judge both in one turn, and charge both. A write that
   passes the old law but not the new one is refused by name (`upgradeConflict residual`). Don't let it through and fail
   MIGRATE later.
6. **`stateSubtype` must be about values, not width.** Adding a record field is NOT a subtype for "old state is a valid new
   state" (closed records); adding a variant case is. Define it on first-order rows only, refuse arrows, `custody` and
   `computation`, and prove `stateSubtype a b → TypedAt a v → TypedAt b v`.
7. **The request facts need a new turn code.** `Facts.turn` is 1 birth, 2 delivery, 3 write, 4 create. Use 5 MIGRATE, 6 ADOPT
   and 7 abort, and document them in `ObjectRecord.Facts`.
8. **Record frames.** HISTORIAN took ACTIVITY-RECORD v4 and R3 took v5; your phase and counter bump the OBJECT-RECORD frame
   (`DREGG/OBJECTIVE/OBJECT-RECORD/v1` → v2). Say so in the commit; it means a re-genesis.
9. **Interface compatibility** (design C: "new interface ⊇ every referenced facet") has no substrate: there is no facet table
   in the kernel. Don't fake it. Name it as the next item.
10. **Process.**
    - Follow VERIFY-ONCE: build only the changed modules plus their dependents, and run the named checks. The merge keeper
      gates.
    - Burst boxes take at most two Lean builds each: `flock -n /srv/build-slot-1 … || flock /srv/build-slot-2 …`. Use
      `SWARM_MEM_MAX=24G`; a 16G umbrella attempt was OOM-killed.
    - The burst boxes are deleted 2026-10-05 15:55Z. Queue ranges before then, and keep a fetchable copy on persvati.
    - Talk directly to ACTIVITY-NATIVE-2 (`a459cac9427484a0c`), whose native route must expose adopt, migrate and abort, and to
      ELABORATOR-2 (`a8d6cf0b983a195f0`), whose publish replay is where restartability and the verdict cache are checked.

## 4. Acceptance

**Compiled.** The changed modules build, with every theorem in §2 pinned.

**Teeth** (each a named theorem on the admitting function, or an executed row on ACTIVITY-NATIVE-2's route; no `#guard`):
- an ADOPT signed outside `authority` is refused;
- ADOPT on a frozen object is refused;
- a floor the new law violates is refused, naming the floor;
- a birth during a draining type change is refused `draining`;
- a drained write that the new law would refuse is refused `upgradeConflict`;
- after the deadline, abort resumes with `upgraded`, and a second delivery of that await is refused;
- MIGRATE succeeds and the object's next birth runs the new pin;
- a rebirthed Tally (`world/activity/Tally.obend`) continues from the migrated count.

**Executed.** One upgrade of a live Tally on a scratch native world, end to end through the route, after ACTIVITY-NATIVE-2's
Q1 lands.
