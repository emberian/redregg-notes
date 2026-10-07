# ORDER-INFRA (VISIT-B, 2026-10-04 ~19:20Z; main d27d1cad). Group: LAWS-RECEIVER, FN-WIRE, FN-DIRECT, AGREEMENT-2, SCHEMA-V2-2.
Verdicts: READY 3 (LAWS-RECEIVER, FN-WIRE, FN-DIRECT) / NEEDS-LANE 1 (AGREEMENT-2) / BLOCKED-ON 1 (SCHEMA-V2-2: its own growth run) / SUPERSEDED 0.
Details: the "## VISIT" section of each resume/<LANE>.md. Burst boxes die 2026-10-05T15:55Z.

## Wave 1 (now)
- FN-WIRE (burst-gate, lane/fn-wire-visit @f5bdcaa5): green at main, unblocks FN-DIRECT's decoders; mostly single-file lane-check, one slot at the end.
- LAWS-RECEIVER (burst-gate, lane/laws-receiver-visit @199e86c1): rebased + 9 modules green; only the fixture (one ambiguous name, 13 cascading errors) stands between it and the queue.
- AGREEMENT-2 (persvati, lane/agreement-2-visit @51c57926): one-line parse error in its WIP; persvati builds take no burst slot, so it costs the burst boxes nothing.

## Wave 2 (as slots / the run free up)
- FN-DIRECT (burst-lane1 Lean; burst-e2e native with the read-only copy of lat1 image d5b0b9100762): READY now and may start its Lean-side items at once, but switches to FN-WIRE's decoders once FnWirePinned lands; burst-lane1 load is ~27.
- SCHEMA-V2-2 (burst-lane1, lane/schema-v2-2-visit @8f18bc6b): starts when growth-levels reaches 3000; then lane-check + native builds; queue after LAWS-RECEIVER (shared Kernel/NativeHostReplay.lean), rebasing on `next`.

Slots: burst-gate holds the merge keeper + FN-WIRE + LAWS-RECEIVER (two Lean slots: FN-WIRE's final closure build and LAWS-RECEIVER's go one at a time). burst-lane1 is loaded (27): FN-DIRECT lane-checks only until SCHEMA-V2-2's run ends.
