# kern-grow — per-create latency is linear in cell count (derive, then fix)

You are a Codex worker (gpt-6.1-sol) on the Mini repo. Deputy: DEPUTY-KERNEL (Claude). Lane = train `kern` tip.

## The measurement (DEPUTY-PRODUCT, burst3-a quiet, artifact set e0a8ba21 — MEASURED, not mine)
Each write = `mini workspace --action create --dir $NODE/sponsor --name record-N --storage declared --predicate permit-all --fields 2`
(a NEW cell per write; certify every ~80 so the log tail stays small). wall_s by record: 1→0.98, 25→2.7, 50→4.4, 75→6.5,
100→9.6, 150→12.9, 200→19.3, 250→24.3. Linear per write in the number of cells (quadratic total), over the 5 s bar from ~55.
Contrast: growth G, 1000 writes to EXISTING cells, max 3.49 s → the cost scales with CELL COUNT, not accepted history.
Not yet split client vs host; the consent/credential-verifier is spawned per create (visible in ps).
Evidence: burst3-a:/tmp/jcert.NtK7Ajqx/records.tsv (record, acceptedCount, wall_s); driver
/srv/lanes/infra-certify/src/edge/mini/journey/jcertify.sh (read it; do not edit it — it belongs to another lane).

## Do
1. DERIVE before measuring: read the create path (client `workspace --action create` → host submit → `Loaded.judge`/append →
   root cache / presence index / cell enumeration / snapshot encode) and find the step whose work is Θ(#cells) per create
   (candidates to check, not conclusions: `Loaded.cells`/`cellIds` enumeration, `RootsExact`/`RootCache` rebuild, PresenceIndex,
   canonical snapshot re-encode, a client-side listing, the per-create verifier spawn reading the whole store). Write in
   WORKLOG the derivation with file:line.
2. Confirm with ONE cheap split measurement (client vs host time per create at ~50 and ~200 cells) via request_journey with a
   script under scripts/kern/; per-row memory cap; no sockets in the sandbox.
3. Fix the primitive (incremental update, cached index — no second implementation beside the old one; delete the slow path).
   Keep every theorem about the cached structure (`*Exact` invariants) proved for the new update. Show the curve flat-ish
   (per-create wall at 250 cells within ~1.5x of at 25) with the same driver shape.
4. ROOT's bar: state the fix's correctness (which invariant of the cached structure it preserves, proved), and give the
   per-create cost bound as a theorem if the cost lives in Lean (e.g. the update touches O(1)/O(log n) entries), AND measure
   uncontended per-create wall at 300 / 1000 / 3000 cells before and after (one journey each side; sample, not every record).
   Candidate loops ROOT named (check, do not assume): an index rebuild, a full-image fold, the light open's checkIndex.
5. As soon as you have NAMED the loop (file:line + why it is Θ(#cells)), send a `report` with phase "diagnosis" — before fixing.
## Rules
- Files: ask (ask_deputy) with exact paths before editing anything outside scripts/kern/. Another worker (kern-r1) is editing
  Compiler/DurableReceiverIO.lean, Compiler/DurableReceiverCore.lean, Kernel/ObjectiveAdmissible.lean and the OB receivers;
  if your fix is there, say so and I coordinate.
- OFF LIMITS: scripts/pipeline, native/spk-host, deploy/, journey.d, the clock subject, edge/ (infra's).
- No sorry/admit/axiom/native_decide; no `| tail` in scripts; no unfiltered cargo. Builds via request_build, journeys via
  request_journey; end your turn after each; never poll. Submit with the default umbrella green and the before/after curve.
