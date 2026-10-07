# 08 — The swarm's work-item lifecycle (not Objective Bend; Ember asked for it in the packet)

## How a work item lives today (measured over 10-04 → 10-06)
author (agent, on a warm lane clone) → single-file checks (`lane-check` 4-7 s, or `lean-ask` 0.4 s) → affected-module build in a
build slot → named acceptance (journeys on scratch worlds, cohorts with planted faults) → `- [QUEUED]` line in MERGE-QUEUE.md →
one merge keeper rebases batches onto main → ONE full gate per batch (umbrella ~10-13 min on a fast box + pins + objective-proofs
snapshot + hyp-ledger + filtered Rust + touched journeys) → fast-forward main, move `green` → warm bases advanced by copy.

## Recurring friction (each observed, with counts where known)
- Rebase churn in hot clusters: ~9 lanes in the activity/object files at once; most WIP at a pause was never compiled on the
  current tree. Fixed by a one-owner-per-cluster rollup; fan-out stays for non-overlapping files.
- Duplicate verification: each landing once paid ~5 full builds (lane gate, keeper gate, second keeper gate, base rebuild per box);
  cut to ~1 (VERIFY-ONCE), measured −58 build-minutes per landing.
- False greens: stale imported .oleans under bare `lake env lean`; gate rows passing only inside `all`; regenerated fixtures disarming
  mutation tests; a queue line marked LANDED that never reached main; "test-only fixes" that relax checks.
- Re-gate churn from GENERATED PINS: build-surfaces, host-closure, the objective-proofs statement snapshot and the native-accepted
  fixture are regenerated in nearly every batch; each regeneration is an audit burden (was anything removed or weakened?).
- Slot starvation and IO starvation on shared boxes; agents waiting on builds; a merge gate starved behind lane builds (fixed by a
  reserved slot).
- Context ceilings: veterans at 500-900K tokens; renewal via `cv distill` (≈1/6 tokens, 28/30 probe answers) vs lossy prose handoffs.
- Coordination by message relay through the root (the root becomes the bottleneck); deputies now address each other directly.
- Journeys under-run: several ranges compiled but never executed on a world before queueing.

## Questions for GPT-6
1. Is a merge-queue with ONE full gate per batch and optimistic main (`green` lags) the right shape for a proof-heavy monorepo
   with ~1,400 Lean modules and generated pins, or should we move to a stacked/speculative merge (à la Bors/merge-train, Zuul's
   speculative pipelines) where each candidate's gate starts on the speculative tip?
2. Generated pins (statement snapshots, closure lists) are both our strongest anti-weakening instrument and our biggest source of
   re-gate churn. Is there a design that keeps the audit value (no statement silently removed or weakened) without regenerating a
   global artifact every batch — e.g. per-module content-addressed statement manifests, or a monotone "ratchet" that only accepts
   additions and explicit, signed deletions?
3. What's the right granularity of a work item for agent lanes in a dependent-typed codebase: per theorem, per module, per feature,
   and how should the dependency graph of the Lean modules drive scheduling (critical-path first, avoid co-scheduling items whose
   affected closures intersect)?
4. Context management: is distill-and-resume (keep decisions/intents/facts, drop tool output) a sound way to extend an agent's
   effective horizon, and what does the literature on long-horizon agents suggest about what must be retained?
5. Verification evidence classes (compiled / executed / proved) — is there a standard taxonomy we should adopt so a landing's
   evidence is machine-checkable rather than prose?
