# hcloud burst plan (2026-10-05) — PROPOSED, nothing rented until Ember says go

Why: execution is the bottleneck (hbox shared with fn; persvati 24 cores carrying ~10 Lean lanes; cold
umbrella ~25 min with Mathlib cache on 24 cores; Host link dominates; journeys and split-tenancy need
machines we do not have). Window: 4 hours, then delete everything.

## Shape (Ember picks the budget; prices to be checked with `hcloud server-type list` before ordering)
- 3 x dedicated-vCPU boxes (CCX53 32 vCPU / 128 GB, or CCX63 48 vCPU / 192 GB), one location (fsn1/nbg1),
  Ubuntu 24.04, an ephemeral SSH key generated for this burst only.
  - BOX-GATE: the merge keeper's post-merge gate + a third warm base (cold build from `lake exe cache get`
    in ~15 min on 48 cores), so landings stop queuing behind lane builds.
  - BOX-LANES: warm base + mk-lane.sh; 4-6 Lean lanes at LEAN_NUM_THREADS=8 (object-record, resume-view,
    metering, laws-pin, seats, elaborator successor).
  - BOX-E2E: DISPOSABLE scratch worlds: jsplit-tenancy.sh on a real multi-uid box (it refuses on live/build
    boxes; this is exactly the VM it wants), jdeploy3 on the candidate, native Objective + activity journeys,
    agreement replicas as 4 processes for timing work.
- Optional 4th: a CI-runner-sized box for the journey-gate diagnosis.

## Setup (one script, run by a lane; ~20 min to first useful build)
cloud-init: apt build deps + capnp 1.5.0 + bun 1.3.11 (pinned, sha256) + elan with the repo's lean-toolchain +
rustup stable; clone https://github.com/emberian/minidregg.git; `lake exe cache get`; build the umbrella once;
copy mk-lane.sh from the persvati base. No secrets of any kind on these boxes: devnet keys stay on hbox/
persvati/the Mac; e2e worlds genesis fresh throwaway keys. Optional: join the headscale tailnet with a
one-hour pre-auth key (headscale on dregg-workhorse) so lanes reach them by name; otherwise plain ssh.

## Rules
- Lanes push nothing from the boxes; commits come back by `git fetch` from the Mac/hbox; the merge keeper
  lands from the Mac checkout as today.
- Hard stop: at T+4h (or when Ember says), a lane collects logs/branches, then `hcloud server delete` for
  every burst box (irreversible by intent; listed by a label `burst=20261005`), then `hcloud server list`
  shows none. Volumes: none. Cost reported at the end.

## What it unblocks (the "new phase")
Parallel Lean lanes without box contention; a dedicated gate so main stays green under higher landing
rate; the first real split-tenancy run; DEPLOY-3 candidate + jdeploy3; agreement timing on separate
processes; then widening the swarm with the scholars' quest list (send, call, seats, upgrade lane, Studio
invoke, paid invocation, CI journey).

## Ember decides
1. Budget/size (3 x CCX53 vs 3 x CCX63; 4 h). 2. Tailnet join or plain ssh. 3. Go.
