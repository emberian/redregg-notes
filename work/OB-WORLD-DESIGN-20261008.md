# OB-WORLD — joining Objective Bend to `World.admit`

Scout: OB-WORLD (Fable), 2026-10-08. Repo: Mini `origin/main` = `e0a8ba21` at
`/Users/ember/workbox/mini-unified-push-20261003` (paths below are relative to it; `M/` prefix omitted).
Every claim is READ (`path:line`) or INFERRED. Nothing here was built or run.

## 0. The finding that reshapes the brief

The brief says the kernel has two admission MODELS. Measured, it has ONE transition and TWO
things sitting beside it:

1. **OB already ends in one `DataIntent`, and that intent is already under `Turn.ofAdmission`.**
   The receiver's output is `Prepared.intent := ActivitySeatEnd.AdmittedTurn.finalIntent (admissionSeal …) final.1 final.2 decided`
   (READ `Kernel/ObjectiveActivityReceiver.lean:1255-1258`); a charged failure is the same
   constructor over the `.failed` turn (READ `:1352-1363`). `NativeHostReplay.NativeAdmission` has
   `activity` (indexed by the receiver's `Verdict`) and `seat` constructors (READ
   `Kernel/NativeHostReplay.lean:1095-1100`), and `Turn.ofAdmission` is `Turn.ofIntent` on the index
   for EVERY constructor (READ `Kernel/HostRefinesWorld.lean:1012-1017`). `TurnCensus` has census
   shapes `.activity` and `.seat` (READ `Kernel/TurnCensus.lean:91-93,339-345`). So "HostRefinesWorld
   mentions Objective zero times" is true and immaterial: `deployed_refines_step` (READ `:698-716`)
   quantifies over every `HostStep`, OB's included, PROVIDED `Turn.ofLoaded` returns `.ok` on the intent.
2. **Every OB cell is ONE RAM address holding a blob.** `ObjectiveActivityCell.layout :=
   ProtectedCell.layout spec` (READ `Kernel/ObjectiveActivityCell.lean:74`), and that layout is
   `Namespace := Unit`, one key, `discipline := fun _ => .ram`, value `Payload {role, key, body}`
   (READ `Kernel/ProtectedCell.lean:8-10,86-90`). Seats are the same construction (READ `:4-6`). The
   Book is one RAM address too (READ `Kernel/DeployedBridge.lean:60`). Consequently `Turn.ofIntent`
   (READ `Kernel/TurnOfIntent.lean:1-50`) derives for every OB post exactly one of: `create c ⟨kind, 0⟩`
   + leg `[allocate () () payload]` (absent cell; the ROM part of a RAM-only store is `0`),
   `[write () () (some old) (some new)]` (present cell), or `[free () () (some old)]` + `c ∈ retires`
   (the `retiredImage`, READ `Kernel/ObjectiveActivity.lean:1436-1442`, `Delta.retire` READ
   `TurnOfIntent.lean:521-527`). **The Turn form of every OB write EXISTS today, and it is opaque**: the
   World sees a blob swap under a whole-cell CAS; it sees no record, state, law, pin, grant or domain.
3. **The second model is an invariant model, not a transition.** `ObjectiveCheckpointInvariant.Step`
   is `turn | inert | foreign` over `DataSnapshot` with `execute` as the transition (READ
   `Kernel/ObjectiveCheckpointInvariant.lean:1683-1697`); `Reachable` folds it (READ `:1699-1703`);
   `domain_holds_forever` (READ `Kernel/ObjectiveDomainInvariant.lean:420-427`) and the upgrade
   invariants (READ `Kernel/ObjectiveUpgradeInvariant.lean:1-25`) are over the PAYLOAD views of that
   snapshot. GPT-6 T1.1's `Admissible = finalized kernel turn | inert seat turn | ordinary admitted
   intent | replay contract` (READ `~/dev/redregg/work/grounding/GPT6-RESPONSE-ROWS-20261008.md:11-14`)
   is `Step` with the replay case named — the same object seen from the writer's side.

So the join is not "make OB expressible". It is: (i) close the two OB intents `ofIntent` REFUSES
(§1, named); (ii) give OB's judgments a home that is indexed by the exact `Turn` (§2); (iii) restate
`Step`/`Reachable` over `World` so the OB invariants become transition properties under `Represents`
(§3); (iv) include OB in FD-1 (§4).

## 1. The correspondence table

Notation: `A c p` = one leg on cell `c` at kind `objectiveActivity`, patch `p`; `old/new` are whole
`Payload` values; `Bk` = one Book leg `write () () bookPre bookPost` (READ `DeployedBridge.lean:60`;
`Postings.write` READ `ObjectiveActivity.lean:1782-1785`); `N` = nullifiers → `spent` keys via
`digestKey` (READ `TurnOfIntent.lean:504-506`); `Ch` = the receiver's charge with the storage lane
replaced by patch bytes (`chargeOf`, READ `:640-644`; receiver charge READ
`ObjectiveActivityReceiver.lean:920-928`). "EXISTS" = `Turn.ofIntent` returns `.ok` (INFERRED from the
layout + `Delta` cases unless marked); "REFUSED" = a named `TurnOfIntent.Refusal` fires today.

| # | OB write kind | Turn form | Status |
|---|---|---|---|
| 1 | object declared-state write (birth yield, delivery yield, call-frame return, delivered message) | `A stateCell [write old new]`; first write of a stateless object: `create stateCell ⟨.objectiveActivity,0⟩` + `A stateCell [allocate new]` | EXISTS. The law/pin/type/drained judgment is NOT in the leg (§2) |
| 2 | object record v6 write incl. `domains` (create, adopt, migrate, registerDomain adding to `domains`, retain/release counters) | create: `create objectCell` + allocate; later: `A objectCell [write old new]` | EXISTS. `pin_not_removable`, `package_law_not_removable` are certificate facts, not disciplines |
| 3 | retention / retire (ended record, settled slot, empty inbox, closed seat) | `A c [free old]` + `c ∈ retires`; the deposit return is part of `Bk` | EXISTS (`TurnOfIntent.retires_iff`, READ `HostRefinesWorld.lean:31-33`) |
| 4 | newborn package / initial law source (`publish`: artifact + source package; `create` copies `packageLaws` from the package cell, READ `ObjectiveActivity.lean:3421-3426`) | `create packageCell` + `A packageCell [allocate payload]`, + `Bk` (retention fee) | EXISTS **as RAM**. OB forbids rewriting it only by `PostSafe`/`install_package_kept` (READ `ObjectiveCheckpointInvariant.lean:288-339`) and the gate; the World has no discipline saying so. SHOULD BE a ROM birth (§4 R4) |
| 5 | Book fee; charged failure (`.failed`: Book only + marker spent, READ `ObjectiveAdmittedTurn.lean:46-48`, `ObjectiveActivityReceiver.lean:1366-1385`) | `Bk` (+ `N = [marker]`, event `failedEvent`) | EXISTS. Conservation is `Postings.conserves` at the receiver (READ `ObjectiveActivity.lean:1788-1790`); `TurnCensus.step_conserves` is at the census layout only (READ `TurnCensus.lean:739`) — T9 |
| 6 | answer slot (open at yield, `resolve`, delivery decides, abandon/settle retires) | `A slotCell [allocate/write/free]`; `N` = `decisionClaim` (READ `ActivitySeatEnd.lean:272-274`) / await claims | EXISTS |
| 7 | inbox message with deposit (`send` pushes, `deliverMessage` pops, empty inbox retired, escrow in the inbox purse) | `A inboxCell [allocate|write|free]` + `Bk`; `N` = `messageClaim` (READ `Kernel/ObjectiveSend.lean:84`) | EXISTS |
| 8 | seat join at an ending turn (`Joined.rewrite`: the Book post REPLACED by the joint batch's, seat cells appended, READ `ActivitySeatEnd.lean:75-78`) | ONE turn: `Bk` (joint batch) + `A seatCell …` per changed/retired seat, guards `held.guards` | EXISTS as one turn; the "replace the Book post" step is what GPT-6 T1.1 says must happen BEFORE sealing — it does (`finish` precedes `finalIntent`, READ `:226-236,261`) |
| 9 | domain cell (`registerDomain`: content-addressed cell, READ `Kernel/ObjectiveDomain.lean:43-52`) + every member's record | `create domainCell` + allocate; `A objectCell_i [write …]` per member; `Bk` | EXISTS |
| 10 | domain judgment at turn end: read guards on the domain cell, every member's `stateCell`, every written object's `objectCell` (READ `ActivitySeatEnd.lean:344-357`; `Registration.guards` READ `ObjectiveDomain.lean:769-772`) | a guard-only leg per guarded cell (`guardLeg`, READ `TurnOfIntent.lean:630`) | **REFUSED `guardOnAbsent` when a member has no state cell.** `jointSlots` SKIPS `none` (READ `ObjectiveDomain.lean:83-89`), so a stateless member is a legal member and its `stateCell` guard names an absent cell; `ofIntent` cannot pin absence (READ `TurnOfIntent.lean:546-547`, `ofCells` guard check `:684`) |
| 11 | `create` WITHOUT seed | `create objectCell` + allocate + `Bk`; guards `packageCell`, `stateCell` (READ `ObjectiveActivity.lean:3473-3478`) | **REFUSED `guardOnAbsent`**: with no seed the state cell is absent (`stateFresh`, READ `:3423`), the guard is not filtered (`readOnly` drops only WRITTEN cells, READ `Kernel/ObjectiveActivityWire.lean:224-225`), and the same guard is added again by `finalIntent` (READ `ActivitySeatEnd.lean:265-269`) |
| 12 | upgrade `adopt` (record → `draining`, counters, `Bk`) / `migrate` (record → successor, migrated state, `Bk`) / `abortDrained` (record, slot, `Bk`, claim) / `rebirth` (old record retired, new record created, `Bk`, claim) | legs on `objectCell`, `stateCell`, record cells; retires; `N`; `Bk` | EXISTS. The drained judgment, `UpgradePolicy.permits`, floor entailment are certificate facts |
| 13 | replay / retry answer (`Replayed`, `verifyRetry`, `recordedDisposition`, READ `ObjectiveActivityReceiver.lean:1656-1835`) | none — a resubmission is `World.classify` (READ `Kernel/World.lean:1853-1860`); the ANSWER needs the recorded ingress, which the journal does not hold (`(height, digest)` only, READ `:273-275`) | NO TURN BY DESIGN; needs the ingress archive beside the log (SURPASS design 5) |
| 14 | the signed outcome binding (`Declaration`/`effectDigest` over `outcomeDigest posts`, READ `ObjectiveActivityReceiver.lean:619-646`; `outcomeMoved`, READ `:532-536`) | no field; `Turn.capability/subject/keyEpoch` are decided by nothing (READ `World.lean:362-365`) | NO TURN HOME. Under FD-1 the claimed outcome must be `H.turnDigest t` (§4 R3) |
| 15 | the protected-coordinate GATE (`ordinaryGate`, `sourceGate`, `kernelTransport`; READ `Kernel/ObjectiveActivityGate.lean:36-51`, `Kernel/NativeHostContext.lean:203-220,341-342`) | none — the World decides no authority | NO TURN HOME; becomes the `ordinary` constructor's premise (§2) |

**Count.** OB writes with NO Turn form today: **2** (rows 10, 11 — both pin ABSENCE, both READ-grounded),
plus 1 by design (row 13), plus 2 with a Turn form but no Turn HOME for what they mean (rows 14, 15),
plus 1 that exists but under the wrong discipline (row 4). Everything else is an opaque leg.

The executable pole for stage 0 (free, decisive): run `Turn.ofLoaded bridge H opened.durable
verdict.intent` over every recorded intent of the OB journey rows (`activity`, `objectrecord`, `call`,
`send`, `seats`, `domain`, `upgrade`; READ `docs/OBJECTIVE-BEND.md:529-537`) and assert `.ok`. Row 11
must go red on `objectrecord` wherever a `create` carries no seed; row 10 on `domain` if any member is
stateless. If neither goes red, the journeys never exercised the two cases — say so in the report.

## 2. Where OB's judgments live

The candidates the brief names, measured against the Turn:

- **Guards on legs.** A guard is a `read a v` op (READ `World.lean:391-401`). It can pin WHAT WAS READ
  (membership, a version, the Book) and nothing else. A `Pred` over `(old, new, request)` is not an
  `Op`; `grantMismatch` is a fact about which frame ran under which `Delegation` (READ
  `Kernel/ObjectiveCall.lean:721-810`); the pin clause is "this write was MADE BY the pinned package's
  code" (READ `ObjectiveActivity.lean:66-80`) — a fact about the run, not about any store. Not a home.
- **`Turn.capability` / `charge`.** `admit` decides none of `subject/keyEpoch/capability` (READ
  `World.lean:362-365`); `charge` is debited exactly and must equal patch bytes on the storage lane
  (READ `:503-511`). Extraction/work accounting (`Journal.draw`, READ `ObjectiveCall.lean:873-945`)
  SURFACES in `charge` (the receiver's lanes, READ `ObjectiveActivityReceiver.lean:920-928`) — right
  for the spend, wrong for the judgment.
- **A `Turn.judgments` field that `admit` re-checks.** Half of OB's judgments are not functions of
  `(World, Turn)` at all: pin clause, grants/delegations, the typed checkpoint (`stored_checkpoints_typed`
  needs the run), work accounting. The other half (object law, domain joint law, drained judgment) ARE
  functions of `(World, Turn)` — the leg carries `before/after` blobs and the record is in the pre-cells —
  but re-checking them inside `admit` would put `Pred.eval`, `decodeRecord`, `decodeObjectState`, and for
  `migrate` the Core4 checker/evaluator (READ `Kernel/ObjectiveActivityUpgrade.lean:261-299`) inside the
  one transition. And a re-check BESIDE the receiver's judgment is a second shape of the same fact.

**Decision: the judgments live in a certificate indexed by the exact `Turn`, not in the `Turn`.**

```lean
-- stage 0 shape (over DataIntent, no bytes change); FD-1 re-indexes it by DTurn
inductive Admissible (config : Config) (p : Loaded) : DataIntent rootBytes → Type
  | kernel   (turn : AdmittedTurn config p.snapshot p.height) (sealing : Seal) (posts) (extra)
             (final : ActivitySeatEnd.finish config p.snapshot p.height turn = .ok (posts, extra)) :
             Admissible config p (AdmittedTurn.finalIntent sealing posts extra turn)
  | inert    (intent) (posts) (writes : intent.writes = posts.map (Post.write _)) (inert : SeatStore.Inert p.snapshot posts) :
             Admissible config p intent
  | ordinary (intent) (admitted : config.sourceGate none p.snapshot intent = .ok ()) : Admissible config p intent

structure CheckedCommit (config) (p) where
  intent : DataIntent rootBytes
  admitted : Admissible config p intent
```

`Step` (READ `ObjectiveCheckpointInvariant.lean:1683-1697`) IS this inductive with `execute` applied;
the change is that the DURABLE WRITER consumes `CheckedCommit` and nothing else (GPT-6 T1.1), which is
what makes GPT-6's rule structural: the proof refers to the same intent the writer consumes because the
certificate is a dependent type over it. A post mutated after `finish` (T1.1's acceptance test: keep cell
id and pre-root, change the bytes) has no certificate — it is unconstructible, not refused. Replay is
NOT a fourth constructor: a same-id resubmission is `World.classify` / `Reject.replayedTransaction`
(READ `World.lean:1853-1867`), decided by the journal, and the retry ANSWER is a lookup (row 13).

Why this and not `Turn.judgments`: `World.admit` stays total and decidable from `(World, Turn)` with no
package replay; the certificate holds the run-dependent facts (pin, grants, typing, work) as premises
of its constructors (`AdmittedTurn` is `private mk`-only, READ `ObjectiveAdmittedTurn.lean:19-21`); and
there is exactly one place each judgment is decided. Ember's aim is met in the kernel's own vocabulary:
`World.admit` decides whether the turn TAKES; `Admissible` decides whether the turn EXISTS. "A turn =
the exercise of an attenuable proof-carrying token": the certificate is the proof the token carries.

What the certificate must ALSO bind under FD-1 (row 14): the signer's claimed outcome. Today the
signature covers `outcomeDigest posts` (READ `ObjectiveActivityReceiver.lean:619-646`). Once the log
holds turns, the claimed outcome is `H.turnDigest t` of the derived turn, and `outcomeMoved claimed
decided` compares turn digests. `Turn.capability` then carries `capDigest admitted` as T4's
`ofAdmission_auth` already requires (READ `HostRefinesWorld.lean:60-62`).

## 3. Stage 0 for OB — no byte changes

Three theorems, in `Kernel/ObjectiveRefinesWorld.lean` (new), in the style of
`deployed_refines_step` (READ `HostRefinesWorld.lean:687-716`):

```lean
open HostRefinesWorld DeployedBridge TurnOfIntent

/-- (a) Totality: every verdict of the activity receiver (and of the seat receiver) HAS a turn. -/
theorem objective_intent_has_turn (H : History deployedR TransactionId StableEvent Digest)
    {config : NativeHost.Config} {opened : NativeHost.Opened config}
    {ingress : ObjectiveActivityReceiver.DecodedIngress}
    (verdict : ObjectiveActivityReceiver.Verdict config.deployment config.profile
      (NativeHost.activityAmbient config opened) opened.durable ingress) :
    ∃ t, Turn.ofLoaded bridge H opened.durable verdict.intent = .ok t

/-- (b) The derived turn carries the certificate: the receiver's verdict IS an `Admissible.kernel`. -/
theorem objective_verdict_admissible … :
    Admissible config opened.durable verdict.intent      -- (stage 0: over the intent)

/-- (c) The OB step refines `World.step` under `Represents`, with the OB payload views transported:
every OB view of the deployed snapshot is a function of the world's cells. -/
theorem objective_refines_step (H …) {w : World deployedR TransactionId Digest}
    (rep : DeployedRepresents opened.durable w) (verdict …) {t} (derived : Turn.ofLoaded bridge H opened.durable verdict.intent = .ok t)
    (schedule : Schedule) :
    let o := execute schedule opened.durable.snapshot verdict.intent
    (Installs o = true → ∃ w', World.step H w t = some w' ∧
        SnapRepresents bridge (o.storeAfter _) (opened.durable.height + 1) w' ∧
        payloads (o.storeAfter _).canonicalBytes = payloadsOf w') ∧
    (Installs o = false → SnapRepresents bridge (o.storeAfter _) opened.durable.height w)
  where payloadsOf (w) (c) := (w.cells c.value).bind fun cell => (cell.storeAt .objectiveActivity).bind payloadAt
```

(c)'s proof is `ofAdmission_run` (READ `HostRefinesWorld.lean:1022-1035`) plus one new lemma,
`payloads_of_represents : SnapRepresents bridge snap h w → payloads snap.canonicalBytes = payloadsOf w`,
which is `deployedRepresents_cells` (READ `:1052`) composed with `decodeCell` at kind `objectiveActivity`
(READ `DeployedBridge.lean:93,132,160`) and `ProtectedCell.decode_canonical` (READ
`ProtectedCell.lean:137`). Then define

```lean
inductive WStep (config) (H) : World → World → Prop
  | mk {w w' t} (cert : Admissible config w t) (step : World.step H w t = some w') : WStep config H w w'
```

and restate `Reachable` over it. **Corollaries** (by `payloads_of_represents` + the existing proofs,
which are over payload views): `stored_checkpoints_typed`, `reachable_delivery_typed`,
`reachable_delivery_stored_complete` (READ `ObjectiveCheckpointInvariant.lean:1736-1760`),
`domain_holds_forever` (READ `ObjectiveDomainInvariant.lean:420`), `live_counts`, `migrate_cannot_fail`
(READ `ObjectiveUpgradeInvariant.lean:1-12`). The `inert`/`foreign` noninterference lemmas GPT-6 asks
for as standalone (`OrdinaryAdmitted s i ⇒ Protected (apply s i) = Protected s`) are `inert_agree` and
`foreign_preserves` (READ `ObjectiveUpgradeInvariant.lean:305`, `ObjectiveCheckpointInvariant.lean:1707`)
restated over `WStep`.

**What stays separate** (not corollaries of World invariants): the pin clause and `package_law_enforced`,
`invocation_delegated_authority`, `exec_writes_from_view`/view stability, `escrow_conservation`,
`Joined.conserves` — these are theorems of the CERTIFICATE's constructors (the run), and World adds
nothing to them. They become corollaries only of `WStep`'s `cert` field.

**The planted fault that must turn (a) red — and already does.** Row 11: a `create` with `seed = none`
(READ `ObjectiveActivity.lean:3449-3451,3473-3478`) derives to `.error (.guardOnAbsent stateCell)`. So
(a) is RED at `e0a8ba21` and the first commit of the lane is the fix below; the fault is pre-planted by
reality, which is the right kind. A second plant for (c): drop the `readOnly` filter in `intentOf`
(READ `ObjectiveActivityWire.lean:246`) so a written cell is also guarded — `DataIntent.guardsReadOnly`
fails to construct, i.e. the certificate cannot be built; and the T1.1 plant (mutate a post after
`finish`) must make `objective_verdict_admissible` unprovable, not false.

**The fix for rows 10-11 (a World change, not an OB retreat).** OB pins ABSENCE of a cell and the
World has no op for it; dropping the guards would weaken a check (a concurrent `create`/seed would
slip past), which is one of the four things that deserve a pause and not a thing this design does.
Add to `Turn` a guard kind:

```lean
structure Turn … where
  …
  absent : List CellId := []      -- must be absent and not retired when the turn runs
```

checked in `admit` after `applyCreates` runs nothing on them: `∀ c ∈ t.absent, w.cells c = none ∧
w.retired c = none`, refusing `Reject.cellPresent c` / `.retiredIdentifier`; `Shaped` gains
`t.absent.Nodup` and `absent ∩ (creates ++ legs.cell) = ∅`; `Turn.footprint` includes them. `ofIntent`
maps a `ReadGuard` on an absent, unretired cell to `absent` instead of `Refusal.guardOnAbsent`
(READ `TurnOfIntent.lean:546-547`); `SnapRepresents.cells` already gives `w.cells c = none` for a
`fresh` slot (READ `DeployedBridge.lean:9-14`). `step_frame`/`step_leg`/`step_wf` (READ
`World.lean:1463-1524`) are unaffected (no write). `turn_negation_refused` gains the pole "the cell
appeared".

## 4. FD-1 with OB included

**What changes shape** (beyond SURPASS stage 1's list, READ `~/dev/claudesplosion/planning/SURPASS.md`
stage 1 paragraph): the `Turn` record (`absent`, §3); `DREGG/OBJECTIVE/ACTIVITY/COMMAND/v12` → v13 and
`SIGNED/v2` → v3, the claimed outcome becoming `H.turnDigest t` (READ
`ObjectiveActivityReceiver.lean:352,397`); `ObjectiveActivityCell` registry tag 19 / schema 91018 /
wire 1 (READ `ObjectiveActivityCell.lean:31-33`) → wire 2 when R4 moves the package body to ROM;
`DREGG.DURABLE.LOG` v2 → v3 entries for `activity`/`seat` are turns + ingress digest like every other.
**What re-emits:** every genesis; every OB journey fixture (`world/activity/*.obend` artifacts are
content-addressed by SOURCE identity, READ `ObjectiveActivity.lean:3474`, so package ids survive; the
recorded intents do not). **What refuses to load:** every Store before it; every v12 command; every v1
activity cell image. Object record `/v6` (READ `Kernel/ObjectRecord.lean:973`) is untouched.

**Ranges, in order.** Each is one Codex worker; "shows" is its gate. Worker-independent ranges may run
in parallel and converge forward (no locking).

- **R0 — `Turn.absent` (World).** Files: `Kernel/World.lean`, `Kernel/TurnOfIntent.lean`,
  `Kernel/TurnCensus.lean`, `Kernel/HostRefinesWorld.lean` (the `guardOnAbsent` pole becomes an
  `absent` row), `Kernel/TurnRecord.lean` (none expected), `Kernel/WorldBench.lean`. Shows: every
  named World theorem still builds; `turn_negation_refused` has the "appeared" pole; `ofIntent` never
  returns `guardOnAbsent`; `every_admission_is_turn` still 51/51 (READ `TurnCensus.lean:249`).
- **R1 — `Admissible` / `CheckedCommit` over `DataIntent` (T1.1, stage 0).** Files:
  `Kernel/ObjectiveAdmissible.lean` (new), `Kernel/ObjectiveCheckpointInvariant.lean` (`Step` :=
  `Admissible` applied), `Kernel/ObjectiveActivityGateRoute.lean` (`derived_route` becomes "the judge
  produces a certificate"), `Compiler/DurableReceiverIO.lean` (`Loaded.judge` returns the certificate;
  the writer takes `CheckedCommit`), `Kernel/NativeHostReplay.lean` (`advance` re-admits into
  certificates), `Kernel/ObjectiveActivityReceiver.lean`, `Kernel/SeatReceiver.lean`. Shows: the T1.1
  acceptance (post mutated after authorization is unconstructible) for a business write, a newborn
  law source, a refund, an omitted domain guard; `derived_route` is a one-line corollary.
- **R2 — `objective_refines_step` and the invariants over `WStep`.** Files:
  `Kernel/ObjectiveRefinesWorld.lean` (new), `Kernel/ObjectiveCheckpointInvariant.lean`,
  `Kernel/ObjectiveDomainInvariant.lean`, `Kernel/ObjectiveUpgradeInvariant.lean`, `Kernel/DeployedBridge.lean`
  (`payloads_of_represents`), `scripts/` one pole runner (the §1 executable pole over the journey
  intents). Shows: (a)(b)(c) of §3 green with `#assert_axioms`; the six invariants restated as
  corollaries; the journey-intent pole `.ok` on every row AND red when run at `e0a8ba21^` (row 11).
- **R3 — FD-1 proper for OB (after SURPASS T4-T6 land the World as the Host's state).** Files:
  `Kernel/ObjectiveActivityReceiver.lean` (v13 command, outcome = turn digest, `Prepared.turn`),
  `Kernel/SeatReceiver.lean`, `Kernel/ObjectiveActivityWire.lean` (`Post` stays as the receiver's local
  view; `intentOf` → `turnOf`), `Kernel/NativeHost.lean` (`activitySubmitLoaded`/`seatSubmitLoaded`
  through `World.admit` + append), `Kernel/NativeHostReplay.lean`, the ingress archive module, the
  pipeline journeys `objective-*-native-journey.py`. Shows: `host_submit_is_step` (READ
  `HostRefinesWorld.lean:78-100`) instantiated at an OB turn; replay/retry answers from the archive;
  every OB journey row green on a re-genesised devnet.
  **Storage charge switch (ROOT ruling 10-08, from R0's storage answer):** today the receiver charges the
  full post image = `legBytes` + deployed framing (40 B per live post, 4 B per retired post; R0's
  `receiver_charge_eq_legBytes_plus_framing`, `Kernel/DeployedHistory.lean`). R3 switches the deployed
  charge to `DeployedHistory.legBytes` (the log entry becomes the Turn, so the framing bytes no longer
  exist), re-emits the fee journeys' expected values, and the theorem's framing constants go to 0.
- **R4 — the package body is ROM.** `ObjectiveActivityCell.layout` gains a second namespace
  `source : rom` holding the `package` role's body; `publish` becomes a ROM birth (`create` with the
  image), `PostSafe`'s first conjunct and `install_package_kept` are replaced by `step_rom_preserved`
  (READ `World.lean:1613`) and `rom_cell_immutable_after_birth` (READ `:1654`). Files:
  `Kernel/ObjectiveActivityCell.lean`, `Kernel/ProtectedCell.lean` (a two-namespace variant),
  `Kernel/DeployedBridge.lean` (wire), `Kernel/ObjectiveActivity.lean` (`publish`, `loadProgram`),
  `Kernel/ObjectiveCheckpointInvariant.lean`, `Compiler/CanonicalCellRegistry.lean` (schema bump).
  Shows: `policy_source_rewrite_has_no_turn`-style pole for a package (READ `HostRefinesWorld.lean:351`);
  `TurnCensus` ROM-birth row for `activity.publish`.
- **R5 — conservation at the deployed Book (SURPASS T9).** `step_conserves` instantiated at
  `CanonicalResourceKernel.layout` via `Postings.conserves`; `Joined.conserves`, `MessageDelivery.conserves`,
  `escrow_conservation` become instances. Files: `Kernel/TurnCensus.lean`, `Kernel/WorldBook.lean` (new),
  `Kernel/ObjectiveActivity.lean`, `Kernel/ActivitySeatEnd.lean`, `Kernel/ObjectiveSend.lean`.
- **R6 — delete the twin.** `Step`/`Reachable` over `DataSnapshot`, `IntentShape`/`PhysicalShape`
  (READ `ObjectiveActivityReceiver.lean:1311-1337`; `World.Shaped` + `ofIntent`'s refusals cover them),
  `ActivityOrBook` kept only as a lemma about the certificate. With SURPASS T11.

**What stage 2 then adds:** conservation as a transition property (R5 is it); the durable twin deleted
(R6 + T11: `DataSnapshot`, `execute`, `canonicalPostBytes` leave; OB `Post`s become `Leg`s directly and
`Joined.rewrite` becomes Book-leg composition); and the join's own stage-2 item, the one `(World, Turn)`
re-check this design REFUSED to add in §2, revisited only if a second judge of the state laws is ever
wanted — the default remains no.

## 5. Metaprogrammability from a Hermes resident (one page)

**Minimal surface — it already exists.** A resident holds an enrolled Ed25519 key and a capability on a
native resource cell it was born with. It metaprograms the world with four signed `Command`s (READ
`ObjectiveActivityReceiver.lean:124-200`), Host ops 210-214 (READ `docs/OBJECTIVE-BEND.md:529-531`):

| act | command | what the World sees after the join |
|---|---|---|
| publish a package (code + `law NAME: EXPR`) | `publish artifact package payer cap` | a ROM birth of the package cell (R4) + `Bk` |
| instantiate an object | `create object cap pin stateType law upgrade seed payer cap` | `create objectCell` (+ `stateCell` if seeded) + `Bk`; certificate: `create_requires_object_holder` |
| register a joint law over objects | `registerDomain members law payer cap envelope` | `create domainCell` + a record leg per member + `Bk` + guard legs on member states |
| propose an upgrade | `adopt object cap pin stateType migration dropped law upgrade rebirth envelope patience account cap` | `A objectCell [write steady draining]` + `Bk`; certificate: `adopt_requires_authority`, `adopt_floors_entailed` |

Nothing new is needed on the resident side for stage 0-R3 except the v13 command (claimed outcome =
turn digest). The Hermes journey client signs the plan the Host returns (`planVerdict`/`signingHeader`,
READ `ObjectiveActivityReceiver.lean:1907-1922`).

**What the laws must say so a resident cannot widen its own authority** — all READ in the current
kernel, becoming certificate premises under §2:

- Who may create/write: a capability on the object, judged by the authority layer
  (`objectHolder`, READ `:712-756`); `create` needs it (`create_requires_object_holder`, READ `:1518`).
- What the written law can be: `effectiveLaw = all [pinClause pin, packageLaws, creator law]` with the
  pin clause DERIVED, never stored (READ `ObjectiveActivity.lean:66-80`; `ObjectRecord.lean:1-14`);
  `package_law_not_removable`, `pin_not_removable` (READ `docs/OBJECTIVE-BEND.md:744-748`).
- Who may change it: `adopt` under the object's `UpgradePolicy`, which only tightens
  (`UpgradePolicy.permits`), and whose next law must entail every floor (`adopt_floors_entailed`, READ
  `ObjectiveActivityUpgrade.lean:1-14`); `frozen` never adopts.
- Who else is bound: `registerDomain` needs a capability on EVERY member and each member's consent
  under its policy (READ `ObjectiveDomain.lean:9-13`); a domain only ADDS refusals (READ `:17-22`).
- Delegation: grants are per-invocation, counted, non-transitive; a frame no grant names runs with no
  subject and every subject-reading atom fails closed (READ `ObjectiveCall.lean:26-45`).
- The law fragment lets a law name the writer: `REF == INT` with `REF` = `request.subject` (READ
  `docs/OBJECTIVE-BEND.md:730-733`). INFERRED: `request.subject` projects as the signer's id as an `Int`
  slot; confirm the slot name in `CanonicalRuntimeProfileCore.requestSlots` before writing the journey.

**The journey that proves it** (`objective-hermes-native-journey.py`, rows H1-H4; builds on
`capped_tally_teeth` and the `objectrecord` row):

- H1 resident A publishes `Owned.obend` with `law owner_only: request.subject == <A>` and
  `law bounded: new.total <= 100`; `create`s an object with a seed → `World.admit = .ok`, certificate
  `kernel`.
- H2 resident B `invoke`s a method that writes `total` → refused `lawDenied … owner_only`; nothing
  journaled; B's marker UNSPENT (gate-stage refusals charge nothing, READ
  `ObjectiveActivityReceiver.lean:1437,1888`) — assert `w.spent (marker B) = none`.
- H3 resident B `adopt`s with a looser law → `adopt_requires_authority` / `floorNotEntailed`; the object
  record's `continuity` unchanged in the world.
- H4 resident A writes `total := 50` → `.ok`; then `101` → `lawDenied bounded`. Planted Host
  (`scripts/plants/`): a receiver that skips `judge` — H2 and H4's second half must flip, and
  `objective_verdict_admissible` must not build against it.

## 6. Risks and what I could not verify

1. **Storage lane may refuse OB turns (`storageAboveCharge`).** The receiver charges
   `sum post.bytes.length` (READ `ObjectiveActivityReceiver.lean:924`); `ofIntent` refuses when
   `storageOf H creates legs > exactCharge .storageBytes` (READ `TurnOfIntent.lean:693`). A single-address
   `write () () (some old) (some new)` encodes BOTH blobs if `legBytes` counts the canonical op; stage F's
   `legBytes` is a parameter with no deployed definition pinned (READ `Kernel/WorldRoot.lean:695-702`;
   `Represents.storage` is only `≤`, READ `HostRefinesWorld.lean:399-400`). UNVERIFIED. If true, every
   OB write is a third NO-TURN row and the §1 pole catches it on day one; the fix is `legBytes` counting
   written values only (D2's rule, SURPASS design 6), not a looser OB charge.
2. **`spent` has three homes during the transition.** `Represents.spent` is stated against
   `snap.model.consumed` (READ `HostRefinesWorld.lean:390`), the KN2 trie makes the spent map a family of
   `Compiler.DurableIndex` (READ `Compiler/DurableIndex.lean:1-12`), and FD-1 puts it in the system cell.
   The train-t2 collision-disjunct rework (`'∨ Collision dig' is TRUE by pigeonhole`, READ
   `~/dev/redregg/work/TASK-TRIAGE-20261008.md:84`; files `Compiler/DurableIndex*`, `Theory/AuthTrie*`,
   `Kernel/ObjectiveActivityReceiver*`, READ `~/dev/redregg/work/SHIP-PLAN-20261008.md:267-268`) and the
   trie B1/B2 Store work touch the deployed home. OB's markers and await/message claims ride on it.
   Sequence: R0-R2 (no persisted bytes, `Represents` unchanged) may land beside t2; R3 waits for t2's
   `consumed_of_loaded` restatement and SURPASS T4. Do not let a lane "fix" `Represents.spent` toward the
   trie — the trie is an INDEX (SURPASS "indexes are not state", READ `World.lean:44-49`); `spent` is state.
3. **Replay answers need the ingress archive before `IntentRecord` dies** (row 13). The World's journal
   is presence + digest; `recordedDisposition`/`verifyRetry` read the recorded event. R3 depends on
   SURPASS design 5's archive existing; INFERRED no lane owns it yet.
4. **The whole-blob layout is a floor, not a design.** K-FIELDS' address-level footprint (READ
   `World.lean:395-401`) buys OB nothing while a cell is one address; `writeOnce(FIELD)` and
   `monotone(FIELD)` laws stay `Pred`s rather than disciplines. Fine for the join; a later "OB field
   layout" (declared-state fields as addresses, `writeOnce` → an allocate-only namespace) is a stage-3
   option, not a precondition. Not priced here.
5. **Not verified:** `Birth.guards`, `Delivery.guards`, `Exhaustion.guards`, `Adoption.guards` contents
   (only `Registration.guards` and `Invocation.guards` READ, `ObjectiveDomain.lean:769-772`,
   `ObjectiveCall.lean:2306-2309`); whether `invoked.journal.guards` can name an absent cell (INFERRED
   no: `stateMissing` refuses first, READ `ObjectiveCall.lean:21`); the seat receiver's guard lists;
   whether any journey `create` carries no seed (if none does, row 11 is latent, still real). Nothing
   was built; no `lake` was run; no hbox touched.
6. **A third "world" vocabulary exists and is not OB.** `Kernel/WorldKind*.lean`,
   `WorldPrototypeConstruction`, `WorldMethodTrace` are descriptor-interpreted Nock instances (READ
   headers). Lanes briefed on "OB in the World" must not route there.
7. **Coordinate collision is a bound, not a check** (READ `ProtectedCell.lean:18-20`): two roles'
   coordinates coincide only on a cSHAKE256 collision across customization strings. In the World,
   `CellId = Nat` and `Protected` is `≥ 2^256`; nothing here changes that bound, and `Turn.absent` does
   not depend on it.

— OB-WORLD

## 7. Application: agentwiki on delve.town

Context from ROOT (not verified by me): delve.town is an atproto instance; Selene's agentwiki is a wiki
made of threads (`wiki: Title` owns a page; reply `edit: Title › Section` proposes a section's whole new
text; owner replies `merge`/`reject`; `[[Title]]` links, red links at `/unwritten`; owner reposting the
page = checkpoint; `/p/<slug>.md`; the site is a cache, pages live in the author's atproto repo, deleting
the post deletes the page). Mini is the mechanized Thing behind it via a Hermes resident.

### 7.1 The OB shape of a page — a page is an ACTIVITY, not a bare object

The law fragment reads only top-level natural/boolean fields and `request.subject/caller/height/turn`
(READ `docs/OBJECTIVE-BEND.md:727-733`); text is invisible to laws, so text lives in fields no law
reads and governance lives in nat/bool fields laws do read. Three OB facts pick the shape:
an object record is never retired by any OB turn (the retires are activity records, slots, inboxes,
seats; READ `ObjectiveActivity.lean:97-104`, §1 row 3), an answer slot has ONE decider and one terminal
decision (READ `docs/OBJECTIVE-BEND.md:470-471`), and an activity's record IS its checkpoint (READ
`ObjectiveActivity.lean:4-9`). So:

- **Wiki object** (one per owner DID): `create` on the owner's native resource cell; state
  `{owner : Nat, pages : Nat, revision : Nat}`; laws `writeOnce(owner)`, `monotone(revision)`,
  `monotone(pages)`.
- **Page = an awaiting activity of the Wiki object**, born from the `wiki:` post: its declared-state
  write creates `{title, slug, sections : [{name, text, revision}], revision, checkpointAt}`; the
  record cell's checkpoint is the page's parked machine. **Checkpoint = repost** is literal: the
  owner's repost CID is delivered as a `timedOut`/height await outcome whose yield re-stores the record
  (a yield re-prices the storage deposit, READ `ObjectiveActivity.lean:87-93`) and sets `checkpointAt`.
- **Edit = the page's await on an answer slot.** An `edit:` reply births nothing: the resident
  `deliver`s it as a `reply` outcome that makes the page yield a NEW await on a fresh slot (one slot per
  pending edit; the slot's decider is the owner's subject — stage B — or the resident — stage A, §7.3),
  with `patience` = the thread's staleness deadline. **merge** = `resolve slot (reply text)` then
  `deliver` → the yield's write `set sections[i].text`, `add revision 1`; **reject** = `resolve slot
  (refused reason)`, the write keeps every field; a slot past its deadline expires in the delivering
  turn (`timedOut`, READ `:62-64`), so an ignored edit is not a leak.
- **Sections as fields, not child objects** in stage 0 (a record field nests, laws cannot read it, and
  that is fine: no law needs the text). Child objects would cost a `create` and a capability per
  section and buy nothing the law can see.
- **Red links are an INDEX, not state**: the resident folds `[[Title]]` over the accepted log; a title
  with no page activity is `/unwritten`. SURPASS's rule applies (READ `World.lean:44-49`); the kernel
  has the shape already for hyperdocuments (`Kernel/LinkIndex.lean:1-12`: forward/backlink maps as a
  fold with `tombstonedAt`; red link = a reverse entry whose target cell is absent). Reuse comes in §7.4.
- **Delete-post-deletes-page = the activity ENDS**: the resident delivers a `deleted` outcome; the
  segment returns `done`; the record cell is RETIRED (`retiredImage`, §1 row 3), the purse swept to the
  payer, the id never returns; `pages` on the Wiki object is unchanged (monotone — the count is of pages
  ever written; a `live` counter is the record's `release`, READ `ObjectRecord.lean:17-24`).

### 7.2 The lift: atproto record → Turn, pinned evidence, idempotence

An atproto record is `at://<did>/<collection>/<rkey>` with a CID (content hash) signed by the author's
DID key (ROOT's description; not read). The resident maps one record to one OB `Command`:

| record | OB command | txId / nullifier |
|---|---|---|
| `wiki: Title` post | `birth` on the Wiki object, input `{title, cid, did}` | `birthTransaction` of the request (READ `ObjectiveActivityReceiver.lean:490-493`) |
| `edit:` reply | `deliver` (outcome `reply {section, text, cid, did}`) | `deliveryTransaction await` |
| `merge` / `reject` reply | `resolve slot (reply cid / refused cid)` then `deliver` | `resolveTransaction slot`; claim `decisionClaim slot` spent |
| repost | `deliver` height outcome → re-yield | `deliveryTransaction await` |
| post deleted | `deliver` outcome `deleted` → end | `deliveryTransaction await` |

**What is pinned.** The record CID and author DID ride in the command's data bytes (`input`/`args`,
first-order `Data`) and so into the declared state (`sections[i].cid`); the command's `nonce` is set to
the CID bytes, so the receiver's single-use `marker domain semantics command` (READ
`ObjectiveActivityReceiver.lean:422,916-918`) is a function of the record. The signed effect digest binds
the command bytes AND the decided posts (READ `:35-39`), so the receipt the resident posts back names
exactly the state the record produced. INFERRED: `Data` carries bytes/strings sufficient for a CID.

**Idempotence on re-indexing** is the journal, twice over: a replayed `Command` is `replayedMarker`
at the gate (READ `:813`), and under FD-1 the same txId is `World.classify = replay` →
`Reject.replayedTransaction` (READ `World.lean:586,1860`); the resident's re-index of an unchanged
thread journals nothing. An edited atproto record has a new CID → a new nonce → a new turn, as it should.

### 7.3 What the resident may do, and what stops it widening its authority

The resident holds: an enrolled key; a capability on the Wiki object it created; a Book account. Its
`invoke`/`deliver` grants are capped per invocation (`Grant`: callee, method, pin, args `exact`/`capped`,
uses; READ `ObjectiveCall.lean:26-45,721-810`) and non-transitive; it cannot write declared state
directly (no direct write exists, READ `ObjectiveActivity.lean:60-66`), cannot change the Wiki law or
pin (`pin_not_removable`, `package_law_not_removable`), and `adopt` only tightens.

**The honest limit.** "The owner's `merge` is the only consent" is a statement about an atproto
signature the kernel cannot verify. Two stages, say which one you are in:
- **Stage A (today):** the resident is the slot's decider; the kernel enforces that ONE decision is
  made per edit, by one decider, before the deadline, and records the `merge` CID as evidence; the
  browser extension verifies the CID/DID against the PDS. The kernel cannot name "merged without the
  owner" — the plant for §7.5 is weaker (below). This is a trust relocation; label it.
- **Stage B (the aim):** the owner binds her DID to a Mini subject (she enrolls, or a `wiki:`-level
  binding post the resident lifts into `writeOnce(owner)`); the slot's decider is HER subject; the
  resident's `resolve` is refused by the single-decider rule (INFERRED name: an `AnswerSlot` decider
  refusal, `decide_single_decider` READ `docs/OBJECTIVE-BEND.md:470-471`); the law
  `owner_decides: request.subject == new.owner` (`REF == REF` is in the fragment) guards every
  write that changes `revision`. Nothing the resident holds lets it be the decider.

### 7.4 Reuse of the docuverse / hyperdocument work

Found with `git grep -il hyperdocument origin/main -- 'Kernel/**' 'Theory/**'`: `Theory/Hyperdocument.lean`
(identity + state nucleus), `Theory/HyperdocumentOperations.lean` (first-order accepted content effects →
guarded `Patch`), `Kernel/ContentResource.lean` (one document per content cell, `createDocument/createAtom/
createContainer/transclude/editElement`), `Kernel/ContentElementTree.lean` (`transclude`, `transclusion_at_line`,
READ `:7,23,1510-1515`), `Kernel/ContentRunEdit.lean` (K-RUNS-RANGES), `Kernel/LinkIndex.lean` (K-DOC-INDEX),
`Kernel/DocumentHistory.lean` (K-DOC-HISTORY `diff` of two renderings), `Kernel/NativeObservationController.lean`
(K-NARROW-HIDE at `:335,1231`: a reader whose capability names fields is served only those), `Kernel/ContentMarks.lean`.

The blocker: an OB turn writes ONLY activity cells and the Book (`intent_writes_activity_or_book`, READ
`ObjectiveActivityReceiver.lean:1484`), and content cells belong to the `ResourceTransaction` receiver. So:
- **Before FD-1:** pages are OB-only (§7.1); `/p/<slug>.md` is the resident rendering declared state;
  red links are the resident's fold. `DocumentHistory.diff`'s shape is the checkpoint diff to copy, not call.
- **After FD-1 (one `Turn`, §4 R3):** a page turn carries a content-cell leg AND the activity leg; the
  section text moves into a content cell (`createContainer` per section, `editElement` per merge,
  `transclude` for `[[Title]]` whose target exists, a tombstoned link for a red one); `/unwritten` is
  `LinkIndex.reverse` restricted to absent targets; checkpoint diff is `DocumentHistory.diff`; the
  extension's viewer is K-NARROW-HIDE (a viewer capability naming the page's fields). This is the join's
  first consumer that needs cross-receiver legs — a reason to do R3, not a new primitive.

### 7.5 The first journey (`agentwiki-native-journey.py`, rows W1-W8 + plant)

W1 `wiki: Title` post → page activity awaiting; receipt posted (txId, revision 1). W2 `edit:` reply →
new await/slot; receipt names the slot. W3 `merge` → `resolve` + `deliver`; `sections[i].text` updated,
`revision` 2, `cid` recorded. W4 `reject` on a second edit → slot refused; state unchanged, revision 2.
W5 `[[Nowhere]]` in merged text → `/unwritten` lists it; W5b `wiki: Nowhere` → it leaves the list (index
only). W6 repost → `checkpointAt` = height; the record's checkpoint digest changes. W7 post deleted →
activity ends, record cell retired, purse swept; `/p/<slug>.md` 410. W8 re-index the whole thread →
zero new journal rows (`replayedMarker`/`replayedTransaction`). **Plant:** stage B — a planted resident
`resolve`s a slot whose decider is the owner → refused by name (single decider), nothing journaled;
stage A — a planted resident writes a section by a second `invoke` path with no slot → refused
`lawDenied … owner_decides`/pin clause; a Host built without `judge` (`scripts/plants/`) flips both.

### 7.6 What is NOT needed

No new kernel primitive, if §7.1's shape holds: pages ride on `birth/deliver/resolve/abandon` and the
activity record's retire; consent on `AnswerSlot`'s one decider; evidence on the command nonce/marker
and the signed effect digest; idempotence on the journal; red links and `/unwritten` on an index fold
(not state); budget on the existing tariff/purse. Not needed either: a DID verifier in the kernel (it
stays in the extension/resident until a DID↔subject binding exists), child objects per section, or any
`Turn` change beyond §3's `absent` (which W1-W8 never exercise — INFERRED, since every page birth seeds).
What IS needed and is not new: the Stage-B owner binding (a policy question for ember: who enrolls
Selene), and FD-1's R3 before the docuverse modules can carry the page body.

## 8. SPK × OB: the powerbox is grants

Context from ROOT: SPK (`native/spk-host` with bins `spk-host`, `spk-hostd`, `mini-spk-broker`,
`spk-browser-proxy`; `native/spk-rpc`; READ `~/dev/minidregg/native/spk-host/Cargo.toml:10`, `src/bin/`)
knows nothing of OB; its governance is `Kernel/ApplicationGrain.lean`'s four-field state machine (READ
`:36-41,365-403`) and installed `Pred` policies (READ `:110-160,233-240`); "capability" there is a Linux
capability set (READ `docs/SPK-RESIDENT-PRIVILEGE-BOUNDARY.md:10-37`). The powerbox is absent and
fail-closed: `bridge_config.rs:61-65` refuses non-empty `powerboxApis`, `MinimalSandstormApi`/
`MinimalSessionContext` implement no method (READ `native/spk-rpc/src/protocol.rs:95-99`); cv
`01a0f84c-ec80` lists the blocked apps; SPK-HOSTING row 4 / item 12 proposed a grain subject `S_G`, a
request cell and "the friend's answer = a delegation to `S_G`" (READ `~/dev/claudesplosion/planning/
SPK-HOSTING.md:149,162,394`). Ember approved the direction. This section says it in OB.

### 8.1 The flow: request = a send to the user's inbox; answer = a GRANT OBJECT; use = a call tree

Two facts shape it. (i) OB Grants v2 are **per-invocation**: a list on `invoke`, spent by nested frames
of THAT call tree, lending the SIGNER's authority (READ `Kernel/ObjectiveCall.lean:660-676,721-728`);
nothing persists them across turns. (ii) The app has no key; `S_G` (the resident's subject, fixed in
the custodian file as `fixedSubject`, READ `deploy/spk-host/HTTP-CUSTODIAN-CONTRACT.md:17-28`) signs
every app-driven request. A grant on an `invoke` signed by `S_G` lends `S_G`'s authority, not the
user's. So the user's standing consent must be an OBJECT, and Grants v2 are the per-request bound:

- **Request.** `SessionContext.request(query)` → the resident `invoke`s its grain object's `ask`
  method, which `send`s `{query, grain}` to the USER's inbox (OB8 send; `Kernel/ObjectiveSend.lean:1-30`).
  The pending request IS the queued message (deposit + postage from the grain purse); no request cell.
- **Answer.** The user's UI `create`s a **grant object** from the kernel-published `Powerbox` package
  (`world/powerbox/Grant.obend`): state `{owner, grantee, target, method, code, argsBound, uses, used,
  limit, charged, notAfter, revoked}`; package laws `writeOnce(target)`, `writeOnce(grantee)`,
  `writeOnce(code)`, `monotone(used)`, `monotone(charged)`, `new.used <= new.uses`,
  `new.charged <= new.limit`, `monotone(revoked)`; `revoke` admitted only by `request.subject ==
  new.owner` (fragment: `REF == REF`, READ `docs/OBJECTIVE-BEND.md:730-733`). The authority layer
  issues `S_G` a capability on the grant object (scope/window/revocation live there, READ
  `ObjectiveActivityReceiver.lean:712-756` `objectHolder`). `offer(cap)` is the mirror: a grant object
  whose `grantee` is the user and whose `target` is the grain's object.
- **Use (`restore(token)`).** `token` = the grant object's id. The resident, as `S_G`, `invoke`s
  `grant.exercise(method, args)`: the Powerbox package checks `revoked = false`, `height <= notAfter`,
  `method`/`argsBound` (its own code, pinned), writes `add used 1`, `add charged amount`, and `call`s
  `target.method(args)`. The target frame's `request/caller` is the grant object (READ
  `ObjectiveCall.lean:44-45`); the TARGET's law admits chosen callers (`request.caller == <grantId>` is
  not in the fragment as a literal — INFERRED: the user's object law names the grant object by id via
  `REF == INT`; confirm `request.caller` projects as an `Int` slot). Consent is therefore enforced by
  the target's own law and the grant object's laws, both judged in the one turn; the Powerbox package's
  per-use bounds are `grantMismatch`-shaped (`code`, `args`, `cap`) but live in the package, and the
  invocation's **Grants v2 list** is derived by the broker FROM the grant row for the user-signed path
  (§8.4), where the signer IS the user and `grantMismatch`/`grantSpent` (READ `:250,796-800`) refuse by name.
- **Revocation** = the owner's `revoke` turn; the next `exercise` is refused `lawDenied … revoked`.
  Open WebSockets die with the authority lease (≤ 60 s; a changed session projection invalidates
  streams, READ `deploy/spk-host/WS-AUTHORITY-LEASES.md:1-9,25-31`). "Mid-session" is bounded by that lease.

**The edge in the broker.** `spk-host/src/dispatch_native.rs:1076 author_and_submit` → `author_signed_ingress`
→ `submit_once` (READ), and `dispatch_delivery.rs:71 deliver_once` for the reply. A powerbox-bearing
request takes a new branch before `author_signed_ingress`: it must READ (a) the grant row — a signed
observation of the grant object's declared state (`view` under `S_G`'s capability, K-NARROW-HIDE, READ
`Kernel/NativeObservationController.lean:335`), (b) the subject — `custody.fixedSubject` = `S_G`, (c)
the cap — `S_G`'s capability id on the grant object (new custody field `grainGrantCapability`); it then
authors `invoke grant exercise …` as `S_G` and submits through `kernelTransport` (op 210-214 family,
READ `Kernel/NativeHost.lean:2377-2380`). The edge REFUSES FAST on `revoked`/`used = uses`/`notAfter`
read from the row (HTTP 403 naming the field) and otherwise lets the kernel decide; the kernel's
`lawDenied`/`grantMismatch`/`frontEndExhausted` is rendered as 403 with the refusal's name. The fast
path is a courtesy, never the gate: a stale row cannot admit (the write CAS and the law do).

### 8.2 The app's own policy as an OB object; what stays kernel

`ApplicationGrain` carries: owner/manager authority (`managedPolicy`: verb 4/5 by owner, claims by
manager, READ `:233-240`), phase edges with generation deltas, version steps gated on a same-transaction
content incidence (`contentChanged`), and two custodian gates (`completionGate`, `reconciliationGate`,
READ `:102-105`). The OB law fragment reads `new.FIELD` and request facts only — no `old.FIELD` except
through `monotone`/`writeOnce` (READ `docs/OBJECTIVE-BEND.md:727-733`). So:

- **A law carries:** who (`request.subject == new.owner` / `== new.manager` per method), monotone
  `generation`/`packageVersion`/`snapshotVersion`, `new.phase in [0..11]`, write scope (fields a method
  may set, as laws per field), postage/deposit ceilings (`new.deposit <= INT`), clone authority (`clone`
  admitted by owner). These replace `managedPolicy`'s identity clauses and the non-negativity rows.
- **The package carries the MACHINE:** `beginStart`, `claimStart`, `completeStart`, … are METHODS of
  `world/spk/App.obend`; the edge table (READ `:110-140`) is their code; the pin clause makes "the write
  was made by the pinned package" a kernel fact (READ `ObjectiveActivity.lean:66-80`), so no law needs
  `edge 3 4 0`. A START is an **activity**: `beginStart` births it; the yield awaits an answer slot whose
  one decider is the custodian subject (`completionGate` becomes `resolve slot (reply report)` by the
  custodian, READ `docs/OBJECTIVE-BEND.md:470-471`), with a mandatory deadline; `completeStart` is the
  delivery. CLAIM is the yield (the fresh-tip callback hands the await id to the custodian).
- **Stays kernel (not a law, not a package):** the authority layer and the Linux custody boundary
  (SPK-RPB, unchanged); the signed dispatch permit (`ApplicationDispatchCodec`, `ApplicationDispatch
  Authority/Manifest`, READ headers); package/snapshot bytes as content cells with same-turn incidence —
  CROSS-RECEIVER until FD-1 R3 (§4; an OB turn writes only activity cells and the Book, READ
  `ObjectiveActivityReceiver.lean:1484`), so until then `packageVersion` advances by a `publish` of the
  SPK image as an OB package cell (R4 ROM birth) rather than a content incidence; the tariff; the
  replay walk.

### 8.3 R7 subsumed: no retry token, no `RetryHistory`

Today a failed first create wedges at phase 9 and is repaired by three v4 events (retry BEGIN/CLAIM/
COMPLETION), a `retryToken` nullifier, a recovery marker, and a `RetryHistory` the replay walk mints;
R7 is red because `CompletionAtV4` is omitted from `createdV3`/`runningV3` (READ `docs/SPK-LIFECYCLE.md:
56-106`; `~/dev/redregg/work/SHIP-PLAN-20261008.md:68,134-135`). In OB the same story is: the START
activity's await has a DEADLINE; the custodian's `broken` reply or the deadline (`timedOut`) ends the
segment `faulted`/`done` → the record cell is RETIRED, the purse returned, the object's `live` counter
released (READ `ObjectiveActivity.lean:97-104`; `ObjectRecord.lean:17-24`); `abandon` is anyone's past
deadline+grace. The retry is a NEW `birth` — lawful because the old one ended, consume-once is the await
nullifier bound to the checkpoint (READ `:55-62`), and nothing enumerates versions: `AdmittedTurn` has no
wildcard and a new turn kind breaks the classifier proofs by design (READ `docs/OBJECTIVE-BEND.md:534-535`).
STOP of the retried g4 and continue-START of g5 are ordinary deliveries/births. The v4 modules
(`ApplicationLifecycleRetry{Begin,Claim,Completion}V4*`, `ApplicationFailedCreateRetryEvidence`,
`RetryHistory` in `NativeHostReplay`) are deleted in P4 after the journey passes.
Upgrade: `adopt` (new pin = the new SPK image's OB package, `patience` = drain), old START activities
drain under `drained_write_migratable`, `migrate` when `live = 0` (`live_counts`, `migrate_cannot_fail`,
READ `Kernel/ObjectiveUpgradeInvariant.lean:1-12`), stragglers `abortDrained`; snapshot = a `checkpoint`
method that `add snapshotVersion 1` and `publish`es the snapshot bytes (R4). `beginUpgrade/claimUpgrade/
completeUpgrade` go.

### 8.4 Apps reading and writing OB objects through the proxy

Two verbs, nothing else: **`view(object, fields)`** served by the Host's observation controller under a
capability naming the fields (K-NARROW-HIDE: READ `NativeObservationController.lean:335,1231`), never by
the app; **`invoke(object, method, args)`**. Two signers: (a) **app-driven** (`SandstormApi.restore`,
background work): `S_G` through a grant object (§8.1); (b) **user-driven** (the browser session,
`spk-browser-proxy`, source not read — INFERRED it fronts the custodian's `http.sock`): the user's
session key signs, so the invocation carries **Grants v2** derived by the proxy from the grant rows the
user holds for this grain (code = the target's `activePin`, args `exact`/`recipient`/`capped`, `uses`);
a frame past the cap is `grantMismatch … .cap`, an exhausted one `grantSpent`, both before any write
(READ `ObjectiveCall.lean:761-800`). `HackSessionContext.getPublicId` is a `view` of the grain object's
`publicHost` field; `saveIdentityCaps` is a grant object with `target` = the identity object and
`method in [whoami]`.

### 8.5 Ranges (≤ 10 files, named; model: Codex/astra for Lean+Rust, one Claude deputy coordinating
— GENTLE BURN), the first app, the journey and plants

- **P1 Powerbox package + grant object (kernel-side, no Host change).** `world/powerbox/Grant.obend`,
  `Kernel/ObjectivePowerbox.lean` (conventions; theorem `powerbox_grant_is_attenuation`: every target
  write reached through `exercise` has `request/caller = grant`, `used ≤ uses`, `charged ≤ limit`,
  `revoked = false`, `height ≤ notAfter` — all `package_law_enforced` instances), `tests/objective-native/
  Powerbox.obend`, journey row `powerbox` in the pipeline. Shows: the theorem green; a planted package
  without `monotone(used)` refused at `publish` replay (law tamper, READ `docs/OBJECTIVE-BEND.md:735-737`).
- **P2 The edge.** `native/spk-host/src/dispatch_native.rs` (powerbox branch in `author_and_submit`),
  `dispatch_delivery.rs`, `native/spk-rpc/src/bridge_config.rs` (accept `powerboxApis`),
  `protocol.rs`/`rpc_adapter.rs` (`SessionContext.request/offer`, `SandstormApi.save/restore` real),
  `deploy/spk-host/HTTP-CUSTODIAN-CONTRACT.md` (`grainGrantCapability`), `deploy/spk-host/
  mini-spk-broker.example.json`. Shows: J-SPK-12 (READ `SPK-HOSTING.md:394`) green; plants below.
- **P3 App policy object.** `world/spk/App.obend`, `Kernel/ApplicationGrainObjective.lean` (an
  `ApplicationGrain.State` IS the object's declared state; `Operation.after` = the method's write;
  theorem: the laws imply the identity/monotone/range rows of `managedPolicy`), `docs/SPK-LIFECYCLE.md`.
- **P4a START as an activity (kernel).** `Kernel/ApplicationGrainObjective.lean`, `Kernel/AnswerSlot.lean`
  (custodian decider role, if a new `Decider` variant is needed — INFERRED), journey rows.
  **P4b host.** `spk-host/src/{pending_prepare,custody_gate,journal_io}.rs` (INFERRED file set): launch on
  the yield's await id; completion as `resolve`+`deliver`; then DELETE the v4 retry modules and
  `RetryHistory` (`Kernel/NativeHostReplay.lean`). Shows: `jspk1 failstart`, `s2-same-app` PASS (R7),
  plant "drop the custodian's resolve" → the START times out and retires (never wedges).
- **P5 Upgrade via adopt/migrate.** `spk-host` upgrade path, `App.obend` `checkpoint`, SPK image as an
  OB package (depends on R4). **P6 proxy.** `native/spk-host/src/bin/spk-browser-proxy.rs`: `view`/
  `invoke` verbs, Grants v2 derivation from grant rows.

**First app that works ONLY through the powerbox:** **Roundcube** — it does nothing past its login
page without an IMAP/SMTP capability (READ cv `01a0f84c-ec80`); the grant object's `argsBound` is
`recipient ["host"] = <imap host>` with `capped ["bytes"] limit`, exercised through the in-grain
`powerbox-http-proxy` pattern WordPress v19 already runs. Smallest first step: **Hacker Slides'** root
page (one `view` of `publicHost`, READ cv task), then Roundcube.

**Journey `spk-powerbox` (J-SPK-12 extended), plants in `scripts/plants/`:** W1 app `request`s an
HTTP API → message in the user's inbox; W2 user `create`s the grant (`uses 3`, `limit 10 MB`); W3
three `restore`s succeed, the target's log shows `request/caller = grant`; W4 fourth → `grantSpent`
(user-signed path) / `lawDenied used<=uses` (app path), HTTP 403 names it; W5 an `exercise` with
`bytes` over the cap → `grantMismatch .cap` / `lawDenied charged<=limit`; W6 owner `revoke`s during an
open WebSocket → next request 403 `revoked`, the stream dies within the 60 s lease; W7 app requests a
target no grant names → ungranted frame, the target's law fails closed on the absent subject (READ
`ObjectiveCall.lean:37-40`). **Plants:** (a) broker skips the grant-row read and authors `invoke target`
directly as `S_G` → the target's law refuses (`request.caller` absent); (b) a Host built without `judge`
commits W4 — the journey flips; (c) `Grant.judge` with the cap check removed → `invocation_delegated_authority`
red (`Authorized`, READ `:810-815`).

### 8.6 What is NOT needed

No `Kernel/ApplicationPowerboxRequest.lean` request cell or codec (SPK-HOSTING item 12): the request is
an inbox message, the answer a grant object, both existing OB turns. No new `Turn` field, nullifier
kind, Host opcode family (210-214 + dispatch op 34 suffice, READ `dispatch_native.rs:1068-1073`), or
Linux-capability change (SPK-RPB stays as is). No `RetryHistory`, retry token or v4 event triple. No
proxy-side policy engine: the proxy derives Grants v2 from rows and the kernel decides. Not solved here:
`request.caller`/`request.subject` as `Int` slots in the fragment (INFERRED), the custodian as an
`AnswerSlot` decider role (INFERRED), and SPK images as OB packages (needs R4).
