# cxo — the Codex hub (read this in 2 minutes)

`cxo` runs Codex workers for a Claude deputy.
- One resident hub on **burst3-a** owns a private `codex app-server` (0.160.0).
- It owns the worker registry, events, jobs (build, journey, cargo, train), the submit guards and the pace gate.
- Workers reach the hub only through its tools: `report`, `ask_deputy`, `request_build`, `request_journey`, `request_cargo`, `build_status`, `submit`.
- From the Mac use `tools/cxo/cxo-b3 …` (ssh; stdin passes through). On the box, use `~/cxo/cxo …`.
- Output is terse; failures start with `ERR`.
- Background reading: the design is in `work/CODEX-ORCHESTRATION-DESIGN-20261008.md` and the first real run in `work/CXO-EXPERIMENT-1.md`.

## The deputy loop
```sh
cxo-b3 limits                                    # weekly used%, pace
cxo-b3 spawn t2-x -d t2 --mklane -m gpt-6.1-sol --allow 'Kernel/Foo*' [--umbrella default] < brief.md
cxo-b3 wait -d t2 -t 540                         # foreground; events or (no events)
cxo-b3 allow t2-x 'Host/Bar*.lean'               # widen scope of a live worker (ASK/NOTE answers)
cxo-b3 answer t2-x a17 "yes, fix the primitive, no twin"
cxo-b3 send t2-x "…"  |  send t2-x --now "STOP …"   # next report  |  steer the live turn
cxo-b3 budget t2-x 20M                           # raise/lower; send never resets it
cxo-b3 status -d t2      # STATE tok(total) unc(uncached) req(model requests) polls jobs budget sha
cxo-b3 log t2-x -n 30    # say / run [exit] / edit / tool / turn end
cxo-b3 retire t2-x verified, merged
cxo-b3 rebase t2-x REF       # hub-side `git rebase REF` in the lane (sandbox .git is read-only); refuses a dirty tree, aborts + lists files on conflict; updates base, event REBASED
cxo-b3 cancel TICKET        # kill a job's process group (TERM, KILL after 10 s); CANCELLED, worker told
cxo-b3 unprotect t2-x 'GLOB' # one-shot deputy approval to touch a protected path at the next submit (event UNPROTECTED)
```

**Spawn options:**
- `--mklane [--from main|next|REF|SHA]` makes a warm lane at `/srv/lanes/NAME/src`, then re-points it at that ref on the shared remote (the warm base can lag it; the spawn reply shows the move). Alternatives are `--repo PATH` and `--wt PATH`.
- `-m` model: `gpt-6.1-sol` is the default (latest Sol; 5.6-sol and 6-sol also available); `gpt-6-astra` for Astra.
- `--budget N|12M` defaults to 12M (validated before any lane is made). That is the hub's cumulative count, including cached context.
- `--umbrella default` (or `"T1 T2"`): the worker's submit is refused until `request_build(umbrella)` came back exit=0 **on the exact tree it submits**. The default umbrella is `Minidregg Host.Main:leanArts ObjectiveProofs`. Use it for every worker whose files overlap another's.
- An `--allow` glob covered by a protect glob is refused (use `--no-default-protect`). The guard ignores `.tsv/.csv/.json/.jsonl/.lock` files (regenerated pins and ledgers).
- E2-5 guards: workers start with `approvalPolicy=untrusted` (`CXO_APPROVAL`), so every sandbox command asks the hub; long ones (`lake build`, `cargo test`, journeys, gate scripts; `CXO_LONG_RX`) are declined with a steer naming request_build/request_cargo/request_journey (event `EXEC_REFUSED`). A running command over `CXO_EXEC_CAP_S` (20) raises `LONG_EXEC`. More than `CXO_NARRATE_N` (4) reports in `CXO_NARRATE_MIN` (10) with no file change or job result raises `NARRATING` and tells the worker to end its turn. `status` shows `req/job` and `decl`.
- `--protect` adds protected globs; `--no-push` skips the push; `--force` skips the pace gate.

**Events from `wait`:**

| event | meaning |
|---|---|
| `SUBMIT` | range, files, `pushed=lane/NAME`, umbrella=green, waivers, claims |
| `SUBMIT_REFUSED` | guard findings |
| `ASK aN` | the worker ended its turn and is waiting: `answer` it |
| `NOTE` | the worker proceeded with its default |
| `BUILD` / `JOURNEY` / `CARGO` | a job finished; the worker already got the result |
| `GUARD` | protected edit, already steered |
| `STALL` | 15 min idle in a live turn |
| `NO_SUBMIT` | two turns ended with no submit |
| `POLLING` | the worker ignored the no-poll rule |
| `BUDGET` | interrupted at budget: `budget N`, then `send` |
| `ERROR` / `TURN_FAILED` / `RESUMED` | look at `log` |
| `TRAIN_GREEN` / `TRAIN_RED` | the umbrella result after a train merge |

## Jobs: the worker asks, ends its turn, and the result is delivered (no polling)
Each `request_*` returns a ticket and tells the worker to **end its turn**. The job runs outside the Codex sandbox, under the box env. Its exit code comes from the process. The result (exit, log path, last 30 lines) arrives as a new turn, or as a steer if the worker is mid-turn.
- `request_build(targets)`: `lake-slot TARGETS` in the lane.
- `request_journey(script, args)`: runs a script from the lane, so sockets work. `{bin}` and `{manifest}` in the args expand to the prebuilt **base** artifact set, fetched once per lane (`fetch-artifacts green`, linked); the set is READY for cfdaf64d. A worker that changed Host must `request_build` it and pass its own path.
- `request_cargo(spec)`: `swarm-build cargo …` with network, and `CARGO_TARGET_DIR` set to `lane/rust-target`. A `test` must name `-p` and a filter or `--test`.
- Concurrency is per kind: build = `CXO_MAX_BUILDS` (else the lane-slot count from `slots --json`, else 6), journey `CXO_MAX_JOURNEYS` (3), cargo `CXO_MAX_CARGO` (2), train `CXO_MAX_TRAIN` (1). `status` shows `pools`. CXO_MAX_JOBS is gone.

## Integration: build the umbrella after EACH merge
```sh
cxo-b3 train t2 -d t2 --from next     # train lane /srv/lanes/train-t2/src
cxo-b3 merge t2 t2-x                  # fetch lane/t2-x from the shared remote, merge --no-ff, build the umbrella
# -> TRAIN_GREEN (pushes lane/train-t2) | TRAIN_RED (the train stays at the red merge; further merges refused)
cxo-b3 spawn t2-mergefix -d t2 --wt /srv/lanes/train-t2/src --umbrella default < fix.md   # paste the error
cxo-b3 merge t2 --recheck             # after the fix commits on the train
cxo-b3 merge t2 --abort               # or drop the red merge (reset to the last green)
```
Merge one range, wait for green, then merge the next. Experiment 1 found three cross-lane reds at once, because all three ranges had been merged before the first umbrella build. The keeper's full gate still runs on what you queue.

## What the hub enforces
- **Names, not ids.** Messages to a retired name are refused, and so is respawning one.
- **Workers never commit.** `submit` stages the tree without `WORKLOG.md` and `.minidregg-native-snapshot` (both also go into `info/exclude` at spawn), then runs the guards:
  - edits outside `--allow`, edits to protected paths, an empty diff;
  - added `sorry`, `admit`, `axiom`, `native_decide`, `maxHeartbeats 0`, `|| true`, `| tail` in scripts, skip or ignore markers, `pkill -f`;
  - deleted theorems, asserts or tests. These can be waived as `rule:path reason`, and **you must read the waiver.**
- If the guards pass, the hub commits (ember arlynx, unsigned, `Cx-Worker:` trailer) and pushes `lane/NAME` to `/srv/git/minidregg.git`.
- **The pace gate on `spawn`** refuses when `ordinaryUsageAllowed` is false or when used% is above 85 % of (linear + one day). It never spends the reset credit; that is Ember's.

## Your job after SUBMIT (guards are not verification)
1. Fetch `lane/NAME` into your own clone, or `merge` it into your train.
2. Read the diff and every changed theorem *statement*.
3. Run the narrowest refuting check, plant a fault and see it go red, and assert the mutation happened.
4. Queue the range for the keeper, then `retire` the worker.

## Cost
- **Measured, experiment 1:** 65M hub tokens moved the weekly window by 23 points, about **2.8M hub tokens per weekly point**. That is approximate: the meter has integer granularity and other Codex use shares the window.
- Polling dominated: t1-retry used 34M, mostly `build_status` at 45 s, each poll re-sending about 150K of context.
- **Now each job costs one extra model request** (one delivered result) instead of one request per poll. The self-test spent 0.3M tokens on 16 requests, with 0 polls and 0 requests during the 45 s build.
- **Estimate per item without polling:** 4–12M tokens (collector 4.1M, mergefix 4.3–10M, Astra meter 12M), which is **about 1.5–4 weekly points**. That is roughly 25–60 items per window if nothing else uses Codex. Budget spawns accordingly, and read `unc` (uncached) next to `tok`.

## Ops
- `~/.cxo/hub.log` is the hub's rotating log (5 MB x 5; events, jobs, command errors, tracebacks); the daemon's raw stdout/stderr go to `hub.stderr`.
- State lives in `~/.cxo`: `registry.sqlite`, `logs/`, `jobs/`, `briefs/`, `hub.log`, `app-server.stderr`.
- Env lives in `~/cxo/env.sh`: CXO_CODEX, CXO_BUILD_CMD (lake-slot) and CXO_PUSH_REMOTE.
- `cxo selftest-local`: no Codex, no box; guard rules, budget interrupt, request_cargo validation, train GREEN/RED/textual-conflict on real git.
- Codex update on the box: `cxo-update-codex.sh` (hub stopped).
- Self-test: `~/cxo/cxo selftest`. It never pushes, and it covers:
  - report;
  - the scope refusal;
  - `allow`;
  - umbrella-gated submit;
  - a build delivered with **zero polls** while the worker sits idle;
  - the commit excluding WORKLOG;
  - `request_journey` opening a unix socket outside the sandbox;
  - retire, and refusals on the retired name.
  - **burst3-a, 10-08 05:58Z: PASS 16/16, 134 s, 0.3M tokens.**
- **Credential:** `~/.cxo/codex-home/auth.json` is a copy of the Mac's Codex login, a bounded operational credential.
  - **Teardown: `rm -rf ~/.cxo/codex-home`.**
  - If either copy refreshes its token, the other may be logged out; run `codex login` on the Mac.

## Not yet exercised live
- `request_cargo`, `renew --fork`, the `BUDGET` interrupt, and a TRAIN_RED on a real conflict.
- `train`/`merge` were exercised on a probe train on 10-08 (create, `--recheck`, merge fetch, TRAIN_GREEN with push, refusal while building, refusal of a bad ref) and then removed.
- A real-lane `request_journey` with `{bin}`. The fetch was verified by hand on `/srv/lanes` and gave 15 binaries.
- The umbrella refusal message itself. The self-test worker built before submitting, so it never hit the refusal; the green-tree match was exercised.

## Known Codex behaviours (measured)
- Steer refuses a stale turn id.
- **A tool call held open makes the model spin**, burning tokens, so every wait ends the turn.
- **Thread goals auto-continue and self-complete**, so cxo does not use them.
- Workers follow steers at once (experiment 1: 7 of 7).

## Added 10-08 (CXO-FIX-2)
- `request_build` / `request_cargo` take `allow_dirty`: the job gets `CXO_ALLOW_DIRTY=1` (the build script's dirty-tree refusal stays the default; honouring the env is the script's business) and the result, BUILD/CARGO event and delivered RESULT carry `DIRTY-TREE head= tree= diff_sha1=` (clean trees say `clean-tree`).
- On `hub start`, jobs left `running`/`queued` become `INTERRUPTED` (event `JOB_INTERRUPTED`); the worker is told to re-request; a train job marks the train RED (`merge --recheck`).
- Exec-approval refusal is judged per shell segment; readers (sed, cat, chmod, `bash -n`, ...) are never refused, and a long-command name (lake build, gate scripts, journeys, cargo) is refused only in EXECUTION position (first word of a quote-aware segment, or the script after bash/sh/python3), never as an argument; `CXO_LONG_RX` is matched at the start of that word. `CXO_LONG_RX` is read at hub start only.
- Hub restart/stop kills the recorded job process groups (TERM, KILL after 10 s) before reporting JOB_INTERRUPTED; one notice per worker, re-request one job at a time. A job that escapes its session (own setsid) is not reachable.
