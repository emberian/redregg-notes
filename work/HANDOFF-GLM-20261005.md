# Handoff to GLM — Mini (minidregg) swarm state, 2026-10-05

Written by the Claude root (session ce776c01) for Ember to hand tasks to GLM. Claude's weekly limit resets **Oct 11, 10:00 ET**.
Everything below is checked against disk/GitHub at the time of writing unless marked ASSUMED.

---

## 0. Read these first, in this order
1. `~/dev/breadstuffs/CLAUDE.md` — **greenfield doctrine** (breaking formats is free; never defer the right fix; say what you broke)
   and the short list of things that DO need Ember (key custody, weakening a check, outward/irreversible acts, real design forks).
2. `~/.claude/CLAUDE.md` — Ember's global rules. The ones that bite: **never delete to free disk (stop, measure, report)**;
   **never `git stash`**; **never run an unfiltered `cargo test -p <crate>`**; **hbox builds only under `swarm-build`**;
   no "quick fixes"; no `#guard` for facts (name them as theorems + `#assert_axioms`).
3. `~/dev/redregg/work/` — the swarm's working notes. Key files:
   - `MERGE-QUEUE.md` — what's queued/landed/held/bounced (header explains format; LOG at the bottom).
   - `SWARM-LEDGER-20261004.txt` — append-only event log of the whole swarm (grep it).
   - `resume/` — per-lane continuation notes; `resume/PRIORITY-ON-RETURN.md`; `resume/MORNING-DIGEST-20261005.md`.
   - Binding protocols: `LANE-PROTOCOL-20261004.txt`, `VERIFY-ONCE-20261005.txt`, `PIPELINE-20261005.txt`,
     `WORKER-BRIEF-20261005.txt`, `HBOX-HOLD-20261005.txt`.
   - Design/plan rows: `OB-COMPLETION-20261005.md`, `OB-LTUO-20261005.md` (Objective Bend), `designs/MINI-PROGRAM-MODEL-20261004.md`.

## 1. What Mini is (one paragraph)
Mini (GitHub **emberian/minidregg**, public) is Ember's capability OS replacing "Bread" (`~/dev/breadstuffs`). **Lean 4 owns the
semantics**: a Host written in Lean admits every turn by *deterministic re-execution* (no proof system in admission). Rust is the
client/custody boundary (`native/`, `mini` CLI, consent client, key broker). **Objective Bend** is Mini's object language: a Core4
kernel with lazy open recursion (mix/fix, final self vs inherited super, C4 ancestry), a Lean parser/elaborator (the only front end),
and a native activity system (yield/resume with answer slots, objects with records/laws/pinned packages, seats with offer safety,
synchronous `call`, async `send` with inboxes). The overview doc was just rewritten: **`docs/OBJECTIVE-BEND.md` on main** — read it.
**fn** (`~/dev/fn`, ACL2) is a separate project Mini uses as archive/feed/transport; another Claude session ("fn root") owns it.

## 2. Git state
- **main = `4ef4e808`** (docs rewrite, pushed ungated on Ember's word; its `overview` gate row was then run green with teeth).
- **green tag = `d94a8817`** (last full gate). **next = `d94a8817`**.
- Push checkout on the Mac: `/Users/ember/workbox/mini-unified-push-20261003` (has push credentials). Landing = fast-forward only:
  `git fetch <bundle-or-lane> <sha> && git merge-base --is-ancestor origin/main <sha> && git push origin <sha>:main`. Never force main.
- Commit identity used by the swarm: `git -c commit.gpgsign=false -c user.name="ember arlynx" -c user.email="cmrx64@gmail.com" commit -F msgfile`
  (write messages to a file; backticks in `-m` get eaten by zsh). Every breaking commit says what refuses and what re-emits.

### Not on main yet
| Item | Where | State |
|---|---|---|
| ForcingTransparent proof finish (no-free-premise stored-checkpoint theorems) | hbox `/tank/dregg-build/claude-lanes/forcing-3/src`, branch `lane/forcing-3` @ `8f3a3287` (bundle `bundles/forcing-3.bundle`) | Proved; needs rebase onto main, full rebuild, `check-objective-proofs.sh proofs --update`, pins, `transparency` gate (planted mutant red), hyp-ledger, then queue. STATUS in that lane. |
| fn wire-grammar re-pin — NOW TARGET fn root `d420a2b5e2b3db18be134ba5a503160da84a31c3` (mini-contract-3 slice 2, merging to fn dev): 211503 octets, BLAKE3 `d00558d008108f98b0fcbc96c0ead68e3fc2c92076974f17f1c00463cf9324a5`, 1028 vectors (supersedes `7e542c054`, 81688 octets) | hbox `/tank/dregg-build/claude-lanes/fn-wire-repin/src` (uncommitted edits) | File vendored + pin edited; NOT built/checked. Build `Compiler.FnWirePinned`, run `scripts/check-fn-wire.sh`, commit, queue. Spec: `resume/PENDING-FN-WIRE-REPIN.md`. |
| SPK v4 fixture (restart lookup test) | hbox lane (see `persvati:~/workbox/claude-lanes/bundles/PN-FIXTURE.STATUS.txt`) | Works on a scratch world; mutation run not yet shown red; 3 WIP commits to squash. |
| Calculus review vs Faré (`~/dev/fareoo`) | not produced | Never got past reading. Brief is in the cron prompt text: compare Core4/elaborator to LTUO, write `work/OB-FAREOO-REVIEW-20261005.md`, fix defects. |
| W05-REWRITER-CODECS | MERGE-QUEUE `[HELD]` | Held because it drops the `inputRefs+1 <= 16` check from a public refusal. Restore the check before it can land. |

## 3. Machines (the rented Latitude boxes are DELETED)
- **hbox** (`ssh hbox`, user hbox): the build box. Mini may run **two** Lean builds there (fn agreed), each
  `flock /tank/dregg-build/claude-lanes/build-slot-{1,2} swarm-build lake build …` with `LEAN_NUM_THREADS=4 SWARM_MEM_MAX=32G`.
  Slot-1 is reserved for the merge gate; lanes use slot-2. **When fn pings for a heavy job, drop to one build.**
  Warm base: `/tank/dregg-build/claude-lanes/warm-base` (FROZEN at `d94a8817`); new lane: `…/warm-base/mk-lane.sh <name>`.
  After a rebase, check single files with `scripts/pipeline/lane-check FILE.lean` (bare `lake env lean` reads stale imports → false greens).
  Merge-gate clone lives on the NVMe root pool: `/home/hbox/kn-gate` (because tank is IO-starved, see §6).
- **persvati** = **Ember's laptop** (`ssh persvati`). At its disk floor (~119G free). **Do not write builds there.**
- **The public boxes**: `dregg-anchor` (5.75.245.0) runs **fn's** public node; `dregg-workhorse` (2.28.141.27) runs **Mini's** 10-01
  candidate. Touch neither without Ember's explicit go.
- Never: `/tank/fn` (fn's), `lat1` (fn's rented box), the live agreement mesh, live worlds. Never filesystem-wide `find` on hbox.

## 4. How to land work (the merge-keeper job — currently nobody is doing it)
Per `VERIFY-ONCE` + `PIPELINE`: lanes check only what they changed; the keeper runs ONE full gate per batch:
`lake build Minidregg +Host.Main:leanArts ObjectiveProofs` plus `scripts/check-host-closure.sh`, `check-import-boundary.sh`,
`check-proof-hygiene.sh`, `python3 scripts/lean-build-surfaces.py check`, `check-objective-proofs.sh`, the hyp-ledger row (compare to
its known-red baseline; a NEW red stops `green`), and touched Rust rows **filtered**. Gate tools: `scripts/pipeline/` on main.
Regenerating generated pins (surfaces, host-closure `--update`) in the batch is fine; anything else red → bounce to the owner.
After landing: push main, move tag `green`, advance the hbox warm base by swapping in the gated tree, log in MERGE-QUEUE.

## 5. Task list for GLM (prioritized; each is self-contained)
1. **Land what's ready**: ForcingTransparent finish and the fn wire re-pin (§2 table) through one gate; move `green`.
2. **Migrate the pay families onto `Kernel.Receiving.Family`** (one law-judgement path). Blockers to solve first:
   `Family.prepare` lacks the checked signature for capability authorization; account-cell births need a `birthParent`.
   Design: cv task `01a109bd-8682`. Acceptance: a pay turn violating the clock law is refused naming the clause; commits when the
   check is removed (assert it); pay journeys pass.
3. **Objective Bend completion** (`OB-COMPLETION-20261005.md`, `OB-LTUO-20261005.md`, "What is open" in `docs/OBJECTIVE-BEND.md`):
   surface semantics + elaborator correctness (LT3/OB1, incl. compose order and C4 proof package); `instance_accepted`;
   digest primitive callable from `.obend` (then make `world/ballot` hiding); sum-typed entry args (OB6); law clauses parsed (LT6);
   reflection contract + provenance-establishing prototype (LT4); upgrade turns (`UPGRADE-BRIEF-20261005.md`).
4. **OB8 follow-ups** (cv tasks `01a10ae9-…`): sends from a delivered message, deeper pipelining, activity awaiting a message,
   retention theorems for send/deliverMessage, "only these two turns write inboxes" theorem.
5. **Journeys**: add rows that run the `call` and `send` drivers; run the fixed `seats` row; JP2 red at row 10 (pre-existing).
6. **Store open at 3000 records** (PRIORITY #6): authenticated verify-at-use (every history read verifies inclusion against the
   anchor-bound root, theorem that no read returns unverified bytes, `mini store audit` full check) + incremental nullifier set.
7. **Plan-scoped replay** (serve consent only the plan's read footprint, filtered by observe authority, with a witness).
8. **Hypothesis ledger**: 5 known-red families on main — make each genuinely green (named satisfying + refuting instances), never
   by allowlisting. 3 theorems with unused premises: cv `01a109c1-2828`.
9. Bread ports remaining (`BREAD-TRANSITION-MAP-20261005.md` NOW/SOON lists).
Backlog: `cv task list --repo ~/dev/minidregg` (open tasks). **Any deferral goes into `cv task open --repo … --body … "TITLE"`.**

## 6. Decisions waiting on Ember (don't act on these)
- **fn public-node redeploy**: `resume/FN-REDEPLOY-DECISION.md` (root recommends GO in daylight; choose fresh init vs importing the
  old export after a full-size import rehearsal). fn's lanes will ask; node steps need Ember's explicit go.
- **hbox `tank` is choking**: special vdev `nvme0n1p3` (13.6G, unmirrored) is **100% full**; tank 88% (332G free).
  **Root cause found: `tank/dregg-build` has `special_small_blocks=32K`**, so every ≤32K block of every build tree (Lean's
  thousands of small .olean/.ilean/.c files) lands on the special vdev. Options for Ember: `zfs set special_small_blocks=0
  tank/dregg-build` (stops the bleed, reversible, moves nothing), mirror/enlarge the special vdev, and free space.
  Largest under /tank: dregg-build 905G (bread-union-20260930 74G, integrate-20260929 54G, hcargo 54G, poa-dailylife 45G,
  games-deploy 34G, claude-lanes 31G, general-live-35632 26G, …), /tank/fn 819G (fn's), chreatures 147G,
  backups/hbox-pre-harden-2026-06-30 517G. Nothing deleted.
- **persvati disk**: `resume/PERSVATI-DISK-20261005.md` (ranked lane dirs; landed lanes' `.lake/build` are candidates).
- `cv distill` (in `~/dev/cv` branch `distill`) point release: Ember's call.

## 7. Cross-project etiquette (fn)
fn's root session messages over `uds:/tmp/cc-socks/*.sock` (Claude-only). From GLM, coordinate through Ember or files in
`~/dev/fn/build/coordinator/`. Standing agreements: Mini ≤ 2 hbox builds, drop to 1 when fn pings a heavy job; fn image builds
never on persvati; Mini's PQ-only fn client (X25519MLKEM768, no classical fallback) stays held until fn confirms hosts after redeploy.

## 8. Things that went wrong before (so you don't repeat them)
- False greens: stale oleans after rebase (use lane-check); gate rows that only pass inside `all`; fixtures re-emitted that disarm
  mutation tests — always show a planted fault turning a check red.
- A "LANDED" queue line that wasn't actually on main — verify with `git merge-base --is-ancestor` / patch-id.
- Lake has no `-j`; three full builds at once OOM a 96G box. One build per slot.
- Weakening sneaks in as "test-only fixes" or allowlist rows; a fix that makes a check pass by checking less is a regression.
- Don't spawn helpers that run unbounded `find`/`du` on hbox; they stall the shared pool.
