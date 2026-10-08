# CXO continuation (CODEX-ORCH, written by the agent itself, 2026-10-08 ~06:05Z)

For a successor who owns `cxo`. Read `tools/cxo/README.md` first (2 min), then this file.

## State
- **Code:** `redregg/tools/cxo/cxo.py` (one file, about 1,090 lines), plus `cxo-b3` (the Mac ssh wrapper) and `README.md`.
  - The copy deployed on burst3-a is `~/cxo/cxo.py`. Check `sha1sum` against the repo copy before trusting either.
  - Box env is `~/cxo/env.sh`: `CXO_CODEX` = `~/cxo/codex/bin/codex` 0.160.0 (the musl package), `CXO_BUILD_CMD` = lake-slot, and `CXO_PUSH_REMOTE` = `/srv/git/minidregg.git`.
  - The hub runs as `~/cxo/cxo hub start`; its state is in `~/.cxo`.
- **Credential:** `~/.cxo/codex-home/auth.json` on burst3-a is a copy of the Mac's Codex login. **It must be removed at box teardown** (`rm -rf ~/.cxo/codex-home`). The box is tagged "delete by 2026-10-09".
- **Self-test:** 16/16 at 05:58Z, 0.3M tokens. The train was probed separately (green, then cleaned up).
- **Artifacts:** I published cfdaf64d with `publish-artifacts` (READY, 605 s; labels green and main). The mirror to hbox failed because the box has no mirror key; the set is local only.
- **Shared-remote hygiene:**
  - Two self-test runs pushed `lane/selftest-1008055005` and `lane/selftest-1008055259`, and the train probe pushed `lane/train-cxoprobe`. I deleted all three.
  - The hbox puller (10-minute timer) may have copied them into `hbox:/tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git`. They are harmless toy refs.
  - The self-test now runs `--no-push`.

## Decisions and why
- The app-server runs **on the box**, not the Mac, because workers' tools execute where the app-server runs: lanes, slots and the remote are all local there.
- **No `thread/goal`.** Measured on the Mac: goals auto-continue turns and self-mark complete. The budget is enforced in the hub.
- **No tool call is held open.** Measured: a blocking `ask_deputy` made the model spin, going from 60K to 619K tokens in 9 min. Experiment 1 then showed that `build_status` polling dominated cost (34M on one item).
  - So every `request_*` returns a ticket plus "END YOUR TURN". The hub runs the job and delivers the result as a new turn, or as a steer if the worker is mid-turn.
  - The worker state is `WAITING_JOB` with a pending count, and the end-of-turn nudge is suppressed while jobs are pending.
- **Umbrella gating** is by tree id. `tree_id()` uses a temp index excluding IGNORE, so it has no side effects. The tree is recorded when the build is requested and becomes `green_tree` if the build exits 0 and its targets include the worker's umbrella set. `submit` compares the current tree against it.
- **Train:** merge one range, then build the umbrella. On red the train stays at the red merge and further merges are refused until `--recheck` or `--abort`. This follows the experiment's lesson that each lane was green alone and the merge was red.
- **Budget:** `tok` is cumulative including cached context (the experiment's 65M). `unc` is uncached input plus output. The default is 12M. `send` never resets the budget and refuses while the worker is over budget.

## Open / next
- Not yet exercised live: `request_cargo`, `renew --fork`, the BUDGET interrupt, TRAIN_RED, and a real-lane journey using `{bin}`.
- Cost model: about 2.8M hub tokens per weekly point (experiment 1, noisy). The window read 33 % at 2 % elapsed at 05:58Z, so the pace gate refuses spawns without `--force`. Scaling is gated on quota, not on boxes.
- Unrelated gate-ordering bug, for the keeper: in `scripts/pipeline/merge-gate-checks.sh`, scripts-elab runs before hyp-ledger builds AxiomCensusResearch (`CXO-EXPERIMENT-1.md`).
