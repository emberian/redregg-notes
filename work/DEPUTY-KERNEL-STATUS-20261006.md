# DEPUTY-KERNEL status (burst 2, 2026-10-06/07)
Workers (all build on burst2-a slots 2-4; scratch clones under breadstuffs scratchpad/<item>/):
- kn2-forcing (opus a51f9e4f86efea00c): PART 1 = gate lane/forcing-3r @09980bf4 (5 commits on 4ef4e808; bundle hbox bundles/forcing-3r.bundle) -> I queue. PART 2 = ROOT: ForcingTransparent true of the deployed kernel (kernel limits or kernel-reserved headroom) + StoredComplete names the actual yield (cv 01a113d9-53a5).
- kn2-hyp-ledger (sonnet a9ecd768469e0194e): poles for 5 simplex families + cv 01a109c1 decorative premises; authored be0a8719. DEMANDED: non-degenerate satisfying pole (a real commit) for AuditRefinement/LocalFaithful; delete-pole red logs.
- kn2-pay-family (opus a5162ba6014b61288): verified-claim token, PayObservation/PayEnrol(V2) onto Receiving.Family, birthParent; teeth fixtures.
- kn2-store-open (opus afdfcf33f426df0d7): design B approved with 6 conditions (views not O(history)/request; deployed hash; non-head tamper refused by name; old epoch refuses; pinned (2) API before port lanes; (1) queues alone only if Host still runs). LogAccumulator c1d54d95 compiled.
Coordination:
- mini store audit CLI: DEPUTY-PLATFORM (a0c673b5e18434531) lane adds main.rs + Host/Main arm; spec sent directly by kn2-store-open. Epoch: whoever lands second (vs PLATFORM P4) takes next number; no holds.
- DEPUTY-OB-ENG (a667f3ddb2cf279db): my port lanes port its sites; OB-ENG reviews hunks in ObjectiveActivity*/ObjectRecord/ObjectiveSend/Seat* before queue; small local hunks, rebase forward. Its upgrade-turns (COMMAND v5, OBJECT-RECORD v2) likely lands before store stage (2).
Closed: cv 01a0f63a-2348 (hygiene, already fixed on main).
Not yet started: LinkIndex 01a0f612-7ab3, doc-history 01a0f60e-2dcf (absorbed by store stateAt if natural).

## ROOT 10-07: at most TWO active workers; landing order ForcingTransparent (+kernel-limits fix) > pay families > Store stage 1.
- ACTIVE: kn2-forcing (opus: the kernel-limits proof needs it), kn2-pay-family (opus: token/Family design).
- PARKED (WIP committed + bundled to hbox bundles/, STATUS = restart file): kn2-hyp-ledger, kn2-store-open.
- mini store audit CLI is now DEPUTY-KERNEL's (PLATFORM winding down); spec in kn2-store-open STATUS.txt.
- Poll every 15-20 min.
- SUPERSEDED (ROOT correction, same night): all four running workers continue to completion; no NEW spawns beyond them. mini store audit CLI back to DEPUTY-PLATFORM (a0c673b5e18434531), spec sent directly by kn2-store-open.
  Port lanes for store stage (3) would be NEW spawns: ask ROOT before launching them.
- kn2-forcing PART 1 QUEUED 4ef4e808..eefea10c (MERGE-QUEUE line "[QUEUED] kn2-forcing"). PART 2 compiled (61778bc7), checks running.
- kn2-store-open API 729bfe3f REVIEWED: 4 holes sent back (unverified byTx absence; Reader not bound to anchor-verified head; stateAt bare snapshot; forgeable Footprint). Staging: (1)+(2a) queue together, (3) ports, (2b) drop prefix + measure.
- ROOT: (a) two Sonnet port lanes PORT-A/PORT-B, spawned only after the re-pin closes the 4 holes; non-overlapping partition from the store worker's committed partition file; store worker REVIEWS batches. OB-ENG reviews hunks in its files.
- MERGE-KEEPER 10-07: lane builds move to burst2-b slots 1-4 (burst2-a loaded; its slot-1/mk = gate). Store port lanes go on burst2-b.
