# kern-oom — the call/send journey rows OOM (>24 GB) since cfdaf64d: diagnose AND fix

You are a Codex worker (gpt-6.1-sol) on the Mini repo, lane at 546c1c88 (main). Deputy: DEPUTY-KERNEL (Claude).
Reported by DEPUTY-PRODUCT (READ by the deputy on the box): the pipeline journey rows `call` and `send` are
OOM-killed even alone: call's scope peaked 25.77 GB vs MemoryMax 24G, killed at 12:40:59, the last completed
steps being `c5-thief`, `c5-bank-kept`, `c6-direct installed confirmed` (so the kill is in the step AFTER c6-direct).
`send` likewise after 601 s; `domain`/`objectrecord` died the same way in a concurrent pass. They PASSED at
cfdaf64d. The runner attributes it to 417e8438 "Preserve charged objective-activity disposition…" (UNVERIFIED —
it is the runner's bisect guess). Evidence: ~/deputy-prod/kr-{call,send,domain,objectrecord}/<tip>/rows/<row>/
(scope.properties, scope.log, call.out, call.err). Reproducer (from a lane with the e0a8ba21 artifact set):
`bash scripts/pipeline/journey-runner --once --tip <sha> --rows-file scripts/pipeline/journey-rows --row call --results-root DIR`.

## Do
1. Find WHICH process grows (Host binary? a driver's `lake env lean` mutation/elaboration step? a client?) and at
   which step. Read the call row's driver and its step after c6-direct. Use request_journey to run a wrapper script
   (new, under scripts/kern/) that runs the row with per-process RSS sampling (e.g. `ps`/`/proc/<pid>/status` every
   2 s to a file in the run dir) and a MemoryMax so it dies early (≤ 12G) — never let it eat the box.
2. Read `git show 417e8438` and the cfdaf64d..546c1c88 range for the implicated code. Name the mechanism (a
   reduction under whnf/decide? an unbounded replay? a quadratic structure? a recursion with no sharing?) with
   the evidence. The deputy will check the mechanism, not just the symptom — DERIVE it from the code.
3. FIX it at the cause (no raised MemoryMax, no skipped step, no `|| true`, no reduced coverage). Before editing,
   `ask_deputy` with the mechanism and the files you need; the deputy widens --allow. Off limits without asking:
   scripts/pipeline/* (train `prod` owns it — if the fix is there, say so and the deputy routes it), Theory/AuthTrie*,
   Compiler/DurableIndex*, and the Kernel files trains kern-r0/kern-r1 hold (World, TurnOfIntent, TurnCensus,
   HostRefinesWorld, DeployedBridge, DeployedHistory, Objective*Invariant, ObjectiveRefinesWorld).
4. Show: the row `call` and `send` pass with peak RSS printed (and well under 24G), and the plant: revert your fix,
   peak RSS grows past your cap again.

## Rules
Builds/runs only via request_build / request_journey / request_cargo; end your turn after each; never poll. No
`| tail` in scripts, no `pkill -f`, no fixed /tmp paths. Submit with the umbrella green.
