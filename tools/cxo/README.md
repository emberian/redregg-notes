# cxo — the Codex hub (read this in 2 minutes)

`cxo` lets a Claude deputy run Codex workers without shelling out to `codex exec`.
- One resident hub on **burst3-a** owns a private `codex app-server` (codex 0.160.0, `~/cxo/codex/bin/codex`).
- It also owns the worker registry, events, build tickets and the rate-limit gate.
- Workers talk back through tools the hub defines: `report`, `ask_deputy`, `request_build`, `build_status`, `submit`.
- Design and evidence: `redregg/work/CODEX-ORCHESTRATION-DESIGN-20261008.md`.

**From the Mac use `tools/cxo/cxo-b3 …`.** It is ssh to burst3-a, and stdin passes through. On the box, use `~/cxo/cxo …`.
Every command prints terse lines, and failures start with `ERR`.

## The deputy loop
```sh
cxo-b3 limits                                   # used% of the weekly window, pace ok?
cxo-b3 spawn kern-store-a -d kern --mklane --from next -m gpt-5.6-sol \
       --allow 'Kernel/Store*' --allow 'scripts/store/*' < brief.md
cxo-b3 wait -d kern -t 540                      # foreground; returns events, or (no events)
cxo-b3 answer kern-store-a a17 "use the v4 frame"   # reply to an ASK
cxo-b3 send kern-store-a "also cover the empty case"        # delivered at its next report
cxo-b3 send kern-store-a --now "STOP touching Host/"        # steer the live turn
cxo-b3 status -d kern                           # name gen deputy STATE model turn rep=count/age item=age tok sha
cxo-b3 log kern-store-a -n 30                   # condensed: say / run [exit] / edit / tool / turn end
cxo-b3 retire kern-store-a verified and queued
```

**Spawn modes:**
- `--mklane [--from main|next]` makes a warm lane at `/srv/lanes/NAME/src`. This is the normal mode for Mini.
- `--repo PATH [--base REF]` makes a git worktree at `~/.cxo/wt/NAME` on branch `cx/NAME`.
- `--wt PATH` uses an existing tree.

**Other spawn flags:**
- `-m` sets the model. The default is `gpt-5.6-sol`; use `gpt-6-astra` for Astra.
- `-e` sets the effort (default `high`).
- `--budget` sets a token budget (default 3M). Past the budget the hub interrupts the turn and raises `BUDGET`.
- `--protect GLOB` adds to the default protected set: NativeAcceptedFixture*, AxiomCensus*, TokenCensus*, Theory/AxiomPin, scripts/gates, scripts/pipeline, .github, lakefile*, lean-toolchain, lake-manifest.json.
- `--no-default-protect` drops that default set.
- `--force` skips the pace gate.

**Events from `wait`:**

| event | what to do |
|---|---|
| `SUBMIT` | the range, files, claims and the push to `lane/NAME` are in the event; verify it (below) |
| `SUBMIT_REFUSED` | the guard findings are in the event. The worker usually fixes them itself; you may `send` |
| `ASK aID NAME Q… default…` | `answer`; the worker has ended its turn and waits |
| `NOTE` | a non-blocking question; the worker went on with its default |
| `GUARD` | a protected file was edited mid-turn; the hub already steered it |
| `STALL` | 15 min with no activity in a live turn |
| `NO_SUBMIT` | it ended two turns without submitting |
| `BUDGET`, `ERROR`, `TURN_FAILED` | look at `log`, then `send`, `renew` or `retire` |
| `BUILD` | a worker's build finished |
| `RESUMED` | the hub restarted; the worker is idle, so `send` it "continue" |

## Rules the hub enforces (so you don't have to)
- **Names, not ids.**
  - `send` or `answer` to a RETIRED or DEAD name is **refused**.
  - A retired name cannot be respawned. Pick a new name, or use `renew`.
  - Tool calls from a retired generation get "stop now".
- **Workers never commit.** `submit` stages the whole tree and runs the guards. It then commits as ember arlynx, unsigned, with a `Cx-Worker:` trailer, and pushes `lane/NAME` to `/srv/git/minidregg.git`.
- **The guards refuse:**
  - edits outside `--allow` and any protected path;
  - an empty diff;
  - added `sorry`, `admit`, `axiom`, `native_decide`, `maxHeartbeats 0`, `|| true`, `| tail` in scripts, skip/ignore markers, or `pkill -f`;
  - removed `theorem`/`lemma`/`example`, `#assert_*`, `#guard`, `assert…(`, or tests.
  - A worker can waive a deletion finding (`rule:path reason`) but never a scope or protected one. The waiver shows in the commit and in the `SUBMIT` event, so **read it.**
- **Builds go only through `request_build`.** That is `lake-slot TARGETS` in the lane under `swarm-build`. The exit code comes from the process, never from a log tail. At most 2 run at once (`CXO_MAX_BUILDS`).
- **Pace gate on `spawn`:** it is refused if `ordinaryUsageAllowed` is false, or if used% is above 85 % of (linear pace + one day). It never touches the reset credit; that is Ember's.

## Your job after SUBMIT (the hub's guards are not verification)
1. Fetch `lane/NAME` from `/srv/git/minidregg.git` into **your own** clone. Never read the worker's tree.
2. Read the diff against the brief. Read every changed theorem *statement*.
3. Run the narrowest refuting check, then plant a fault and see it go red. Assert that the mutation actually happened.
4. Queue the range for the keeper (VERIFY-ONCE), then `retire` the worker or `send` it the rework.

## Steering ladder
`send` (piggyback) → `send --now` (steer) → `interrupt` + `send` → `renew NAME --fork [--before-turn ID] "correction"` →
`renew NAME "note"`. The last one is a fresh thread from the worker's own WORKLOG.md, keeping the same tree and brief.
Renew at about 60 % context, after two compactions, or after twice-ignored steers. Never renew from a paraphrase.

## Ops
- Hub: `~/cxo/cxo hub start|stop|run`, state in `~/.cxo/`, which holds:
  - `registry.sqlite`, `events` (in the registry), `logs/`, `builds/`, `briefs/`;
  - `hub.log` and `app-server.stderr`.
- Env is in `~/cxo/env.sh`: CXO_CODEX, CXO_BUILD_CMD, CXO_PUSH_REMOTE.
- Self-test: `~/cxo/cxo selftest [-m MODEL]`. It runs spawn → report → planted scope violation refused → deputy send → clean resubmit → commit holds only the allowed file → retire → send to the retired name refused → respawn refused.
  - **burst3-a 10-08 03:00Z: PASS 9/9, 37 s, about 143K tokens.** The Mac also passed 9/9.
- **Credential:**
  - `~/.cxo/codex-home/auth.json` on burst3-a is a copy of the Mac's ChatGPT Codex login, copied 10-08 02:58Z: a bounded operational credential (mode 600, in a 700 directory).
  - **Teardown: `rm -rf ~/.cxo/codex-home` before the box is deleted.**
  - If either copy refreshes its token, the other may be logged out. The fix is `codex login` on the Mac.
- `~/.cxo/codex-home/config.toml` is minimal: no MCP servers, no global AGENTS.md or skills. Worker context starts lean.

## Untested paths (first use = watch it)
`--mklane` spawn, the push to the shared remote, `request_build` on a real lane, `renew --fork`, hub-restart resume, `BUDGET`.

## Known Codex behaviours (measured)
- `turn/steer` refuses a stale turn id.
- Tool calls block the turn until the hub answers.
- **Codex's `thread/goal` auto-continues turns and self-marks the goal "complete"**, so cxo does not use goals.
- **A long-held tool call makes the model spin**, writing "still waiting…" (60K → 619K tokens in 9 min). That is why `ask_deputy` returns at once and the worker ends its turn.
