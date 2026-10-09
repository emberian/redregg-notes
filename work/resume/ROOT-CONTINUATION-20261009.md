# ROOT CONTINUATION — 2026-10-09 ~02:00Z (session ce776c01 / breadstuffs-e3), written for the harness restart

This is an INDEX, not a summary. Each line points at the file whose author knows. Where this file and a pointed file
disagree, the pointed file wins. Facts below are MEASURED at ~02:00Z unless marked.

## Read in this order
0. `work/PROTOCOL-20261009.md` (gen 1 DRAFT, how we work now) and `work/MATURATION-MAP-20261009.md` (what gets built next, in order).
1. `work/RETRO-20261008.md` — the transcript-grounded retrospective (ten obstructions, protocol shape, software-rethink
   evidence). Ember's standing instruction: learn from it, then move "methodically and carefully" toward a usable-demo
   milestone. The protocol rewrite replaces DEPUTIES-20261006.md / WORKER-BRIEF-20261005.txt / LANE-PROTOCOL-20261004.txt /
   tools/cxo/README.md; it is NOT written yet, and Ember reads the retro first.
2. `work/DECISIONS-FOR-EMBER-20261008.md` — 15 decisions with options and resolve commands; Ember has not marked it up.
3. `work/grounding/GPT6-RESPONSE-ROWS-20261008.md` — GPT-6's rows (T1/T2/T3/L, V1–V7) and its answers to our questions.
4. `work/OB-WORLD-DESIGN-20261008.md` — the join of Objective Bend to `World.admit` (§1–6; R0–R2 LANDED on train kern,
   R3+ held), §7 agentwiki (set aside by Ember), §8 the SPK powerbox as grants (approved direction, not started).
5. `work/DEPUTY-KERNEL-CONTINUATION-20261008.md` and `work/DEPUTY-PRODUCT-CONTINUATION-20261008.md` ("FINAL STATE") — every
   unlanded branch with sha, contents, evidence, blocker.
6. `work/SHIP-PLAN-20261008.md` with the root's corrections in `work/CXO-EXPERIMENT-3.md`; THE BAR = cv 01a0f9c0-521b.
7. `work/TASK-TRIAGE-20261008.md` + `.tsv` — 560 tasks bucketed; 81 verified close-done not yet run; 141 other-project to park.
8. `work/resume/STALL-WATCH-20261007.md` — the root's hour-by-hour log, 10-07 05:21Z → now.

## State of the code (measured)
- GitHub main = **1c7e46da** (kern LANDED after the prune; 5896a594 was the product tip). NOT Deployable: its standing journey run (correct runner) has call/send/domain/objectrecord
  OOM at 24G (fixed on train kern), jpay2–4 / welcomecontinuity / sshe2e red on missing `clockGenesisNow` (clock flag day
  fallout), hostupgrade-EF red (stale epoch; fix on lane/train-prod 5019da6a), m6grain red (GRAINS_ROOT).
- Train kern **LANDED** as main 1c7e46da: static gate red=0, standing run 109 rows with no new reds and the four OOM rows
  (call/send/domain/objectrecord) fixed. Remaining main reds are all product/clock-side (see above).
- Unlanded: lane/train-prod 5019da6a (derived StoreEpoch; gate red=3 pins), lane/snap-prod-rowfix 3ad3a35d (runner install
  fix + genesisNow helper + ssh-e2e trap fix, unreviewed), lane/prod-v4 a4a2af4d (DROPPED: §8 subsumes), lane/snap-prod-demo1
  256ca79a (paused), kern-grow WIP patch (root cache fix PARTIAL: 44.5→36.7 s/create @1000 cells; cv 01a11e1b-0adc),
  dregg-infra branch `edge/mini-certify` 7c28bf7 on the Mac (EMBER PUSHES; DEPLOY-3 prerequisite).
- Public node dregg-workhorse still serves candidate 5688775a (Oct 1). DEPLOY-3 rehearsed, never shipped; needs the certify
  unit + clock v2 params; dregg-infra has 10 files of uncommitted 10-02 WIP (RustDesk 0.0.0.0/0 firewall + ignore_changes
  are Ember's call; see the decisions memo).

## Infrastructure (measured)
- burst3-a (Latitude sv_BDXM5E4JzNrpk, 67.213.117.177, f4-metal-medium, $1.52/h; ssh -F ~/.ssh/burst3-20261008.conf):
  KEPT through the reorient (Ember 10-09). Shared remote /srv/git/minidregg.git (lane/* only), mirrored to hbox every
  10 min (hbox:/tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git). Warm base 546c1c88 (stale vs main; advance
  with scripts/pipeline/advance-base-burst.sh from a gated lane). Latitude credit left ≈ $125.
- cxo hub on burst3-a at redregg `f5f5bbf` (all ten fixes installed 01:45Z; selftest-local 65/66, the one fail is a Linux
  TERM→KILL timing in the orphan-kill test). Codex credential = Ember's relogged account (used 6%, resets 10-16),
  copied to ~/.cxo/codex-home/auth.json at 02:00Z; remove at teardown. Known dual-copy hazard: a refresh on either side
  can revoke the other. Default model gpt-6.1-sol; astra for Lean.
- fn: dev pin build 6679dae0e at /srv/fnbin/6679dae0e; fn's qualified pin 4b22a49bc staged at /srv/fnbin/4b22a49bc
  (sha 7d7f77c4…866f). Production pin stays d420a2b5 until a rehearsal + Ember's go. fn is draining toward its own freeze.
- hbox: tank ≈ 168G free (fine, per Ember); `special_small_blocks=0` applied to tank/dregg-build; burst2 mirror key retired.
- Codex CLI: npm latest (0.161.0), never brew.

## Rules in force (Ember)
- Be gentle with Claude tokens; Codex does the heavy lifting; few Claude agents.
- Function first; THE BAR before new demo apps; agentwiki set aside.
- Never git stash; no unfiltered cargo tests; bounded operational keys OK (record, remove at teardown); disk is Ember's.
- No main push without the standing journeys at the tip (root's landing rule, 10-08 22:50Z).
