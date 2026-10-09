# kern-r1 — `objective_refines_step` + OB invariants as World corollaries (R1 of train `kern`)

You are a Codex worker (gpt-6-astra) on the Mini repo. Deputy: DEPUTY-KERNEL (Claude). Your lane is based on
R0 (lane/kern-r0): `Turn.absent` exists, `Turn.ofIntent` no longer refuses absence guards, and the deployed
history is pinned as `Minidregg.Kernel.DeployedHistory.history` (Kernel/DeployedHistory.lean — read it).

## FIRST: read, then paste into WORKLOG.md the real signatures
`deployed_refines_step` and its premises (Kernel/HostRefinesWorld.lean ~:687-716), `ofAdmission_run`
(~:1022-1035), `deployedRepresents_cells` (~:1052), `DeployedRepresents`, `SnapRepresents`, `Represents`,
`Turn.ofLoaded` (:410), `Turn.ofAdmission` (~:1012), `NativeHostReplay.NativeAdmission` (Kernel/NativeHostReplay.lean
~:1095), the activity receiver `Verdict` and `Prepared.intent` (Kernel/ObjectiveActivityReceiver.lean ~:1255,1352),
the seat receiver's verdict (Kernel/SeatReceiver.lean), `execute`/`Installs`/`storeAfter`/`Schedule`
(Kernel/ObjectiveCheckpointInvariant.lean ~:1683-1703 and wherever they are defined), `payloads`,
`DeployedBridge.decodeCell` (DeployedBridge.lean :93,132,160), `ProtectedCell.decode_canonical` (ProtectedCell.lean :137),
and the statements of `stored_checkpoints_typed`, `reachable_delivery_typed`, `reachable_delivery_stored_complete`
(ObjectiveCheckpointInvariant.lean ~:1736-1760), `domain_holds_forever` (ObjectiveDomainInvariant.lean ~:420),
`live_counts`, `migrate_cannot_fail` (ObjectiveUpgradeInvariant.lean ~:1-25).

## The theorem (design §3 (c); adapt names to the real signatures, never weaken the shape)
New file `Kernel/ObjectiveRefinesWorld.lean`:
```lean
theorem objective_refines_step (H := DeployedHistory.history) {w} (rep : DeployedRepresents opened.durable w)
    (verdict : ObjectiveActivityReceiver.Verdict …) {t}
    (derived : Turn.ofLoaded bridge H opened.durable verdict.intent = .ok t) (schedule : Schedule) :
    let o := execute schedule opened.durable.snapshot verdict.intent
    (Installs o = true → ∃ w', World.step H w t = some w' ∧
        SnapRepresents bridge (o.storeAfter _) (opened.durable.height + 1) w' ∧
        payloads (o.storeAfter _).canonicalBytes = payloadsOf w') ∧
    (Installs o = false → SnapRepresents bridge (o.storeAfter _) opened.durable.height w)
```
with `payloadsOf w c := (w.cells c.value).bind fun cell => (cell.storeAt .objectiveActivity).bind payloadAt`, and
the SAME theorem for the seat receiver's verdict (`seat_refines_step`). For EVERY `Schedule` (no schedule fixed).
Use the deployed history, not a parameter instantiated nowhere; if the proof is generic over `H`, state the generic
one AND instantiate it at `DeployedHistory.history` as a named theorem.
Key new lemma (in DeployedBridge.lean): `payloads_of_represents : SnapRepresents bridge snap h w →
payloads snap.canonicalBytes = payloadsOf w` (deployedRepresents_cells ∘ decodeCell at objectiveActivity ∘
ProtectedCell.decode_canonical).

## Plant (must go RED, recorded in WORKLOG, then restored)
Post-admission substitution: after the verdict, replace the final post's bytes with different bytes, SAME cell
id, SAME pre-root (e.g. a wrapper `tamper : DataIntent → DataIntent` that rewrites the last post's new value).
Show concretely that `objective_refines_step` no longer goes through for the tampered intent: either the
derived turn differs from the one `World.step` applies to the represented world (state the theorem that
`payloadsOf w'` disagrees with the tampered store), or the step's precondition fails. Write the plant as a
named theorem that is TRUE (e.g. `tamper_breaks_payload_view : … payloadsOf w' ≠ payloads (tampered…)`) plus the
WORKLOG record of the build going red if you splice the tampered intent into objective_refines_step.

## Corollaries
Restate over the World view (via payloads_of_represents + the existing proofs, which are over payload views):
`stored_checkpoints_typed`, `domain_holds_forever`, `live_counts`, `migrate_cannot_fail` (and
`reachable_delivery_typed`/`_stored_complete` if cheap). Each corollary's statement must quantify over a World
reached by `World.step` under `DeployedRepresents` and conclude the invariant about `payloadsOf w`, NOT about the
snapshot it started from. KEEP the originals (R2 restates `Step`/`Reachable` and may delete them then).

## Rules
- Files: Kernel/ObjectiveRefinesWorld.lean (new), Kernel/DeployedBridge.lean, Kernel/HostRefinesWorld.lean
  (only if a lemma there needs generalizing; say why), Kernel/ObjectiveCheckpointInvariant.lean,
  Kernel/ObjectiveDomainInvariant.lean, Kernel/ObjectiveUpgradeInvariant.lean (corollaries only, originals kept),
  the umbrella import list. Ask for others.
- OFF LIMITS: scripts/pipeline, native/spk-host, deploy/, journey.d, Theory/AuthTrie*, Compiler/DurableIndex*,
  `Represents.spent`.
- No sorry/admit/axiom/native_decide; `#assert_axioms` on every headline theorem. No vacuous statements: no
  conclusion that follows from the premises alone without the receiver (check: would it still prove if `verdict`
  were replaced by an arbitrary intent? If yes, it is not about OB — tell me), no `∨ Collision` over an infinite
  type, no history with zero byte functions.
- Builds only via request_build; end your turn after each; never poll. Submit with the umbrella green; in the note,
  paste every new theorem statement in full plus the plant evidence.
