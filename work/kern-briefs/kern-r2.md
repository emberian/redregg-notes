# kern-r2 — `Admissible cfg w t` over the exact Turn, consumed by the durable writer; `WStep`/`Reachable` over `World` (train `kern`)

You are a Codex worker (gpt-6-astra) on the Mini repo. Deputy: DEPUTY-KERNEL (Claude). Your lane starts at the train
`kern` tip 1c2d798b, which contains: R0 (`Turn.absent`, `Delta.burn`, OB create refuses `.stateRetired`) and kern-r1
(`Kernel/ObjectiveRefinesWorld.lean`: `payloads_of_represents`, `intent_refines_step`, `objective_refines_step`,
`seat_refines_step`, `ReceiverIntent`, and one-step corollaries `stored_checkpoints_typed`, `domain_holds_forever`,
`live_counts`, `migrate_cannot_fail`, plus `tamperLast`/`tamper_breaks_payload_view`). Design: work/OB-WORLD-DESIGN-20261008.md
in ~/dev/redregg (§3 and §4 "R1"/"R2"; the train's naming is shifted by one: THIS range = design R1's certificate + design R2's WStep).
Two siblings converge forward in parallel (no locking): kern-oom edits Kernel/ObjectiveActivityReceiver.lean (byte codec for
Reject — keep your edits to that file minimal), kern-charge adds Kernel/ObjectiveTurnTotalityStorage.lean.

## FIRST: read, then paste into WORKLOG.md the real signatures of (anchors measured by the deputy at 1c2d798b)
- `World` (Kernel/World.lean:264), `Turn` (:370), `Reject` (:424), `World.admit` (:607), `World.step` (:630).
- `Turn.ofLoaded` (Kernel/HostRefinesWorld.lean:410), `deployed_refines_step` (:699), `ofAdmission_run` (:1023).
- `Loaded` (Compiler/DurableReceiverIO.lean:783) and `Loaded.judge` (:1506) — `Except RejectReason Unit` today, i.e. a
  verdict that carries no evidence. Find, and paste, the function(s) that actually append an accepted intent to the durable
  log for the activity and seat receivers (grep from Kernel/NativeHost.lean and Kernel/NativeHostReplay.lean `advance`).
- `derived_route` (Kernel/ObjectiveActivityGateRoute.lean:49).
- `ObjectiveCheckpointInvariant.Step` (:1683, constructors turn | inert | foreign) and `Reachable` (:1699).
- The activity receiver `Verdict`/`Prepared` and the seat receiver `Accepted`, `ActivitySeatEnd.finish`, `AdmittedTurn.finalIntent`.

## The work
1. **Certificate.** New `Kernel/ObjectiveAdmissible.lean`: `Admissible (cfg) (w : World …) (t : Turn …) : Type` (data, not
   Prop, so the writer can consume it), indexed by the EXACT `Turn` that `World.step` applies. Its constructors are the
   receiver's checked runs (activity: AdmittedTurn + finish + seal; seat: the accepted seat verdict; plus the ordinary
   `foreign`/`inert` arms if the writer needs them), each with the equation `Turn.ofLoaded … (finalIntent …) = .ok t`.
   `CheckedCommit cfg w := Σ t, Admissible cfg w t`.
2. **The writer consumes it.** `Loaded.judge` (or a new judge beside it, then delete the old one — no two shapes) returns the
   certificate; the durable append for OB intents takes a `CheckedCommit` and writes exactly `t` (its bytes are a function
   of the certificate's index; there is no separate intent argument to substitute). `derived_route` becomes a one-line
   corollary. `NativeHostReplay.advance` re-admits into certificates. No wire/byte change in this range (stage 0): if a
   byte change becomes necessary, ASK first.
3. **WStep / Reachable over World.** `inductive WStep cfg H : World → World → Prop | mk (cert : Admissible cfg w t)
   (step : World.step H w t = some w')` (H := `DeployedHistory.history`), `Reachable` over it from a genesis world.
   Restate kern-r1's four corollaries over `Reachable` (MULTI-step induction from genesis, not one step): conclude
   `CheckpointsTyped`/`DomainsHold`/`LiveCounts`/`MigratableStates` of `payloadsOf w` for every reachable `w`. Restate
   `inert_agree`/`foreign_preserves` (ObjectiveUpgradeInvariant.lean:305, ObjectiveCheckpointInvariant.lean:1707) over WStep.
   Then DELETE the snapshot-level `Step`/`Reachable` if nothing outside proofs-of-themselves still needs them (design R6
   allows keeping them one more range; say which you chose and why).
4. **The four T1.1 acceptance plants** (GPT-6's): a post-authorization mutation that keeps the cell id and the pre-root must be
   impossible through the checked API or refused before commit, for (i) an activity business write, (ii) a newborn law
   source (package publish / seedless create with law source), (iii) a refund, (iv) an omitted domain guard (the mutated
   turn drops a read guard). The RIGHT shape is a functional dependency, not a universal negation: state
   `Admissible.turn_determined : Admissible cfg w t → Admissible cfg w t' → (same authorization: ingress / signed command
   digest equal) → t = t'` and, per plant, a concrete TRUE theorem that the mutated turn ≠ the certified turn while the
   authorization is unchanged (so the mutated turn has no certificate under that authorization, and the writer has no other
   entry point). Do NOT state `¬ Admissible cfg w (mutate t)` unless it is true for every authorization. Record in WORKLOG,
   per plant, the build going RED when the mutated turn is spliced into the checked writer, with the error, then restore.

## Rules
- Files: Kernel/ObjectiveAdmissible.lean (new), Kernel/ObjectiveRefinesWorld.lean, Kernel/ObjectiveCheckpointInvariant.lean,
  Kernel/ObjectiveDomainInvariant.lean, Kernel/ObjectiveUpgradeInvariant.lean, Kernel/ObjectiveActivityGateRoute.lean,
  Compiler/DurableReceiverIO.lean, Kernel/NativeHostReplay.lean, Kernel/NativeHost.lean, Kernel/ObjectiveActivityReceiver.lean,
  Kernel/SeatReceiver.lean, Kernel.lean. Ask (ask_deputy) for others; I widen with `allow`.
- OFF LIMITS: scripts/pipeline, native/spk-host, deploy/, journey.d, the clock subject, Theory/AuthTrie*,
  Compiler/DurableIndex*, `Represents.spent` (R3+ is not this train).
- No sorry/admit/axiom/native_decide; `#assert_axioms` on every headline theorem. No vacuous statements: no `∨ Collision`
  over an infinite type, no identity-carrier binding (`fun _ _ v => v`), no premise that is unsatisfiable (for each headline,
  name a concrete instance that inhabits its premises, or explain why one exists). A corollary that would still prove with
  the certificate replaced by an arbitrary intent is not about OB — tell me rather than ship it.
- Builds only via request_build (targets e.g. `Kernel.ObjectiveAdmissible`, then the umbrella); end your turn after each;
  never poll; long commands in the sandbox are refused, use request_build/request_cargo/request_journey.
- Submit with the default umbrella green on the exact tree. In the submit note paste every new/changed theorem STATEMENT in
  full, the four plant records, and what you deleted.
