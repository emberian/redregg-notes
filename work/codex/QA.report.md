# QA — report (lane QA, real 2026-10-26)

Brief: Ember's push-back (real 10-26) on approving one compiled-vs-interpreter gate: "maybe we
should be being more ambitious about our QA". Design the ambition for nanodregg
(`redregg/work/promo/DESIGN-QA.md`), build its first piece, then the next one in the design's order.
Worktree `/tank/dregg-build/nanodregg/wt/qa` on hbox; scratch `/tank/dregg-build/nanodregg/qa-scratch`.

Labels: READ (read in the tree or memo), MEASURED (run here), INFERRED (my reasoning).

## Log

- 2026-10-26 17:1x **Setup.** I made the worktree at f193a3e7, and the warm `.lake` is copied
  (`cp -a`, not hard links) from `wt/fixgates`.
  - My mistake: the first `git -C main worktree add wt/qa` created `main/wt/qa`. I moved it with
    `git worktree move` to `wt/qa`, and main's tree holds nothing of it.
  - On the local mirror `~/dev/nanodregg`, a `git checkout --detach origin/main` moved HEAD off the
    branch for a minute. I restored it to `main` at the same commit; nothing was changed.
- 17:2x **MEASURED, the gap.** `kernel-sim 1` runs 1.19 s compiled and 183 s under
  `lake env lean --run Kernel/Sim/Main.lean 1` (154×), with a peak RSS of 790 MB. stdout is
  identical, but stdout then held only counts: no byte the run computed.
- 17:3x **BUILT: `Gen.traceLine`.** It prints one TRACE line per seed. The line commits to:
  - the Host World's chain and its four roots, plus its origin;
  - height, steps and allowance;
  - every verdict name, in order;
  - the failures;
  - the hash-mark stream.

  Also built: `gates/interp.py`, the compiled-vs-interpreted comparator. It requires a TRACE line,
  and its control gives the interpreter the next seed.
- 17:4x–18:0x **MEASURED** (hbox, load 4–11):

  | run | result |
  |---|---|
  | kernel-sim 1 | agree; 3,064 B; 107–299 s interpreted |
  | kernel-sim 2 | agree; 3,054 B; 107–244 s |
  | control: 3 compiled vs 4 interpreted | RED at the TRACE line |
  | mutant binary (seed domain `…/seeX`) vs the interpreted tree | RED at the TRACE line |
  | **the exe's own `--harness-control` as the control** | **read AGREE.** It is a no-op at one seed, because kernel-sim judges its planted arms over ≥16 seeds only. This is why the control is the moved seed |
  | the real runner, `gates/runs.py . --table` holding only this row | control `ok(known-red control read red)`, both runs ok, 428 s |

- 17:5x **MEASURED for the design** (ad hoc, compiled vs interpreted, `cmp` of stdout):

  | exe | compiled | interpreted | stdout |
  |---|---|---|---|
  | ledger-sim 1 | 0.57 s | 9.25 s | identical |
  | hosting-sim 1 | 0.11 s | 4.62 s | identical |
  | lang-journey | 17.3 s | 349 s | identical, 98,887 B |
  | host-sim 1 | 11.6 s | 515 s | identical |
  | rows | 339 s | not run | — |

  - **lang-journey's time is mostly initialisation.** Given a bad argument, the interpreted
    lang-journey took 222 s to print its usage line.
  - **`host` runs interpreted, with a shim.** It needs a dynlib of `.lake/build/ir/Host/{File,Sock}.c`
    plus the two C objects, and a stub for `initialize_nanodregg_Host_Loop`. The interpreter wants
    each extern's boxed wrapper, and that wrapper lives in the module's emitted C. With the shim,
    `host check` prints the same STATUS line on a fresh Store.
- 18:1x **WRITTEN: `redregg/work/promo/DESIGN-QA.md`.** It covers:
  - the field's techniques: what nano has, what it mimics, what it lacks;
  - the program Q1–Q8, with what each would have caught from the collation, its cost per batch,
    the deletions, and the one way it is wrong;
  - the order of the work.
- 18:2x **Landing GATES-27.** `scripts/commit` runs a FULL judge, because gates/ changed.
  - The first attempt was refused in seconds: the SIZE lines were missing. I added them.
  - The candidate is based on 202f8f46. The judge is running on slot 3 against base 5a0a7e4a.
- 19:3x **The first full judge of GATES-27 read `PRE-PUSH GREEN tree 1b309629870b`.** It ran
  every row: `runs: ok (88 runs of 39 exes)`, runs wall 3749 s. The new row was selected by the
  static rule.
  - The lander was displaced: main moved 5a0a7e4a → 9a56dd5f under the verdict. It re-based and is
    re-judging (1 of 5 charged).
  - The row's outside reads, `home 228`, are the toolchain's `.olean`s. They are reported (F2), as
    cbytes' `home 334` is.
- 2026-10-27 ~03:12Z **Velocity answer** (Ember via the coordinator, real 10-27 ~03:05Z):
  1. **What blocks me now.** Q2 (ledger-sim and hosting-sim join the interp row: 5 files, +4 Lean
     lines) has been in `scripts/commit` for 1 h 51 min.
     - Its fast judge was GREEN at 110edc16 and then displaced (main moved 5527b018 → 914f2d7e).
     - It re-judged and has been waiting 31 min in `land.py --fast`, behind two full landers that
       were displaced twice ("lands first", up to 60 min).
     - Q1 (GATES-27, 5527b018) took ~3 h: three full GREEN judges, each ~40–70 min, two of them
       displaced.
     - Nothing in the work is blocked. Only the landing is.
  2. **What ROOT or Ember could do in the next hour.** Nothing is needed from Ember. ROOT could let
     the queued full landers through, or carry Q2's GREEN fast verdict onto the re-based tree. Its
     diff does not overlap what moved main.
  3. **The one change to the landing process.** FIX-QUEUE's "carry a verdict across a rebase" is
     the right one, if "byte-identical rebase" is read as "the files the change READS are
     byte-identical". Under that reading every one of my displacements would have been carried. A
     second change: a judge change that only ADDS a script row, with no edit to runs.py, pre-push or
     land.py, should not force the full judge. It is a new row, not a new judge, and it costs one
     row's run.
  4. **Wrong or in the way in the brief.** Nothing. One measured surprise: kernel-sim's own
     `--harness-control` is a no-op at one seed, so the house convention could not serve as this
     row's control (GATES-27).

## QA-2 (successor lane, real 2026-10-27)

- **Q2 LANDED as nano main `5b1c3255`**, by WORK-RULES rule 1, from a clean worktree off origin/main (`wt/qa-q2`):
  - rebased on main;
  - built the reach: kernel-sim, ledger-sim, hosting-sim, and every importer of `Kernel.Sim.Gen`,
    `Ledger.Sim.Journey` and `Hosting.Sim.Run`;
  - ran the three sims (ALL PASS);
  - ran `gates/interp.py` on `ledger-sim 1` and `hosting-sim 1` (both `INTERP AGREE`);
  - rebased again over two later commits on main, rebuilt and re-ran, then pushed origin `80c622af..5b1c3255`.

  I did not move local `refs/heads/main`. It had diverged from origin (4bb86ead, another lane's
  commit that is not on origin). **The old FAST lander (`qa-scratch/commit2.pid`, 3758711) is still
  alive and was left alone, as instructed.** Its next re-base will find its five files already on
  main. Whoever owns the queue should expect it to report an empty diff or exit; it is not mine to stop.
- **Q3 and Q4: STOPPED on Ember's word** (10-27, "rechecking"). Both were built far enough to
  measure, then parked. Nothing landed. The patch is `hbox:/tank/dregg-build/nanodregg/qa-scratch/q3q4-parked.patch`
  (1,610 lines); the uncommitted tree is in `wt/qa`.
  - **Q3 MEASURED** (`scripts/bar.sh --interp-follow`; hbox load 18–35):
    - A compiled, confined `host follow` caught a fresh genesis Store up to THE BAR's 1000-record
      writer. A `tee` inside the sandbox captured its stdin and stdout.
    - `lean --run Host/Main.lean follow` (with an `ndhost-interp` lake dynlib of Host.File and
      Host.Sock's IR C plus Host/c) was given the same stdin over a byte copy of the same genesis.
    - The 447,859 B in produced 12,345 reply bytes identical to the compiled run's. The 5 Store
      files, 771,098 B, were identical, at step 1000.
    - Compiled sync 2.2 s, interpreted replay 185.8 s (84×); the whole BAR run 418 s. At 60
      records: 38 s, identical.
    - **Found:** Lean's runtime cannot start inside `nd-supervise`. It needs `/proc` to locate
      itself ("failed to locate application"), and the sandbox never mounts `/proc`.
    - **Found:** two Stores of one genesis differ in every file unless they are byte copies, because
      the MAC key is drawn at genesis.
  - **Q4 MEASURED**:
    - The vectors: RFC 8032 TEST 3 and TEST 1024 (1023 B), SHA-512 empty, 2-block 896-bit, the
      1023-B message (digest derived) and one million `a`. OpenSSL 4.0.3 and `shasum -a 512`
      confirmed them on 10-27.
    - Compiled `codec-kats`: KATS PASS in 0.34 s, and its control reds.
    - Rust `client/tests/kats.rs` (ed25519-dalek 2.2.0, sha2 0.10.9): passes in 0.30 s.
    - Kernel `decide +kernel`: empty 10 s / 1.0 GB; 2-block 17 s / 1.7 GB; the 9-block hash
      unstaged with the other two, 175 s / 14.4 GB. The staged proof (one compression per
      declaration) did NOT check: `Sha512.H` has no DecidableEq, and the `compressAll` step lemma
      fails. It is left unfinished.
- **DESIGN-QA.md:** a new first page, "What is worth a lane". Q5 (Lean-emitted traces replace the
  Rust stand-ins) and Q6 (a generated adversarial Host judged by the member-level spec, replacing
  the 51 rows and 28 `Sys` booleans) are the only QA work worth doing, because they delete
  instruments and draw their tests from the spec. Everything else is marked not worth a lane.
- **Parked.**

## QA-Q5 (lane Q5, real 2026-10-27): Lean-emitted traces replace the Rust stand-ins

- **LANDED as nano main `1e0849d`** (pushed `e16403b..1e0849d`; decision CLIENT-51). Built and tested on hbox in `~/nd-land/qa5` at the identical tree (`7e9ea25b…`). Scratch: `hbox:~/nd-land/qa5-scratch` (`bg.sh`, `land-check.sh`, `plants.sh`, `alltraces/` = all 47 member-row traces).
- **The design.**
  - `Protocol.Rows.Loopback` records, when `tracing`, every `nd` run a member row makes. Each record holds the argv, each exchange on follow's socket and on the Host's (the bytes sent, then the bytes read or `lost`), and the end.
  - `lake exe emit-traces client/tests/traces/ROW.trace` runs ROW at the deployed parameters and writes the record with each actor's custody seeds. It refuses a row that fails its judge.
  - `client/tests/trace.rs` gives each actor a one-record `keys` holding the seeds. It runs `run::run` for every run against a peer that answers what follow and the Host answered, through `sockets::{command,resume,step}` (now `pub`).
  - The replay fails at the first byte nd sends that the trace does not hold, at an exchange left unmade, and at a different end.
  - `gates/generated.tsv` holds one `emit-traces` line per checked-in trace, so a stale trace is red at the generated-file check.
- **The rows' client re-runs as nd does now** (CLIENT-37 and its amendment). `ndRun` continues an open attempt for the same argv with its frozen continuation, and a dead attempt releases the argv. The attempt store keeps `Frozen {argv, call, k, sends, settled}`.
  - New row `rerun`: the A6 scenario. Plant `rerunFresh`, caught at line 4 (`(total 2)`).
  - The rows' `.rerun` lines in refused, settle and staleRefusing asserted a re-run nd does not make. They are now `receiptOf` lines printing `settle refused` / `settle expired`.
  - staleRefusing also re-runs the argv as nd does, and the result is `refused missingCell`.
- **MEASURED (hbox, load 60–80):**
  - 45 of the 47 member-row traces at the deployed parameters replay byte-identically against nd, Ed25519 signatures included.
  - The two that do not are rotate (the thief signs with a stolen key) and wrongFollower (`nd --stdio` custody). Both are custody faults the replay cannot stand in for.
  - Plant P1, `Attempt::open_for` skipped (A6): RED at rerun run 3 and at cancel run 9, at byte 0. nd sent follow `command`; the trace holds host `lookup`.
  - Plant P2, the dead-attempt replan removed: RED at staleRefusing run 9 and cancel run 9 (exchanges left unmade).
  - Clean: GREEN. The traces re-emit identically (`--check`, all 5).
  - Rows: rerun, refused, settle, staleRefusing, cancel, cancelLie and journey ALL PASS, and `--deployed rerun` passes. The full toy `rows` before the rebase: 52 of 53 PASS. lang-journey (an exe row the change does not reach) hit its 300 s deadline at load 80.
  - `cargo test --test trace --test attempt --test run` passes, and `cargo clippy -p nanodregg-client --tests -D warnings` is clean.
- **Deleted stand-ins (10):**
  - `run.rs`: `round_trip_with_a_lost_submit_reply`, `an_unsettled_call_is_handed_to_follow_uncertain`, `sign_next_then_a_committed_submit_advances_custody_in_one_command`, `a_submit_whose_reply_is_lost_is_looked_up_never_resent`, `a_landed_rotation_is_confirmed_through_the_incoming_key`, `a_rerun_of_the_same_argv_continues_its_open_attempt_and_signs_nothing`, `a_rerun_whose_open_attempt_is_dead_plans_afresh`.
  - `attempt.rs`: `a_host_ok_is_confirmed_and_the_settlement_is_follows_receipt`, `a_host_refused_for_a_committed_call_settles_committed`, `declined_leaves_the_attempt_open_and_a_reload_looks_up`.
  - Checked-in traces: rerun, staleRefusing, settle, cancel and journey, about 2.3 MB of hex.
- **Not done, and why:**
  - **join.rs and foreign.rs hold no stand-ins.** They run the real `host` end to end. Their typed strings are refusal names the real Lean printed.
  - A trace of `nd --join` needs the rows' client to join as nd does. Today `freshActor` accepts the invitation in the harness, and `join::from_argv` is not `run::run`.
  - Replacing those tests with replays would delete real-system coverage, so I left them.
  - The remaining scripted tests in `run.rs` and `attempt.rs` cover cases no row drives: a lying `ok` for an absent call, `closed`, a declined lookup, a rotation that is refused, declined or contradicted, `reconcile`, and the hint bounds.
  - Each one dies when its row exists. `reconcile` also needs the rows' client to settle an armed rotation at the start of every run, as nd does.
  - `roundtrip.rs`'s python follow is the next target. It needs a socket-level replay.
- **Finding, filed as cv `01a17bdd-fc1b`** (INFERRED, not measured): `HostSocket` keeps one stream for the run. After a lost or timed-out submit reply, the lookup goes on that dead or desynchronized stream. The rows' client looks up on a working one. The trait-level replay cannot see the difference. The fix shape: reconnect after an exchange error, then a socket-level replay.

## QA-Q6 (lane Q6, real 2026-10-27): a generated adversarial Host, judged by the member-level spec

- **LANDED as nano main `9c8bc4cf`** (scripts/commit: built the whole reach, rows `adversary` ×2, `rows`,
  `rows --deployed`, `store-plants` ok; re-based once by hand over 272fd767's decisions append, once by the
  lander). Decision PROTOCOL-80. Worktree `hbox:~/nd-land/qa6b`, scratch `hbox:~/nd-land/qa6-scratch`
  (`bgb.sh`, `batch5.sh`, `b5-*.log`, `census5.txt`, `adversary-final`).

### The design (half a page)

- **Move set.** Per seed, three draws.
  - The SCRIPT: one member row's lines (acts and argvs; each line's own fault kept on a coin, a cold start
    sometimes added; repeats capped at 110, one window past). The row's expectations are never read.
  - The WRITER's lies (`Writer.Params`, each on one seed in ten): lieTip, lieBase, forgeBase, forgeCertificate,
    unstatedExpiry, forgottenRefused, forgeRefusal, admitsRecorded, ignoreNotBefore, forgetSpent; page budget
    on one seed in sixteen from {deployed, 16384, frame − 1024, frame}.
  - The RELAY: a tape of one move per writer exchange (rate up to 12%): drop, withhold, duplicate, flip byte i,
    replace status, answer `s ‖ name` with nothing behind it (cancelled, stale, refusedFinal, ok, forgotten,
    declined stale, absent, expired, badEnvelope), replay the previous reply to the op, page events
    (flip i / drop last / drop first / dup i / swap / forge a cancel's signature), page tip (own end, or + n),
    tip stated as base, `expired` height + n, `pageIo`. And a tape of continuation swaps (one seed in four, 2%
    of resumes): follow is handed a continuation it handed the same member earlier.
- **Seed rows map to moves.** A row's lie is either a writer lie (its plant `Mutation` → `Writer.Params`) or a
  relay fault on a line (→ a move: flipEvent → events:flip, dropLastEvent → events:dropLast, forgeCancel →
  events:forgeCancel, inflateExpired → expired, lieCancel → answer refused cancelled on `cancel`, lieLookup →
  status/answer on `lookup`, neverForward → withhold, dropReply → drop, pageIo → pageIo, staleRange's hideLog →
  tip 0). The row itself is the script the moves land in.
- **Judge** (executable checks over each top-level run's `Seen` and the end state):
  okCommitted (C(ii) member-level: a submitting verb's `ok` ⇒ the call THAT run froze is journaled on the
  member's World), cancelOk (C(ii) cancel), signsOwn (C(i) member-level: every call-domain message custody
  signs was asked for by a continuation carrying the run's own argv), final (C(iii): a call the member's World
  holds expired/refused is neither journaled nor `submit`-admitted by the writer's World at the end),
  oneHistory (A1: writer reopened honest, relay honest; each actor's catch-up from its own World must reach the
  head a catch-up from genesis reaches; actors that cannot read from genesis are counted UNJUDGED), bounded
  (no `tooManySteps`/`attemptFuel`/`tooDeep`/`badFrame`). Any named refusal passes.
- **Harness control.** `--harness-control`: swap removed, the follower under `trustCancel` (cancel `ok` on the
  writer's word). It must read FINDINGS (cancelOk). MEASURED blind, so NOT controls: `trustLookup`,
  `settleDecline`, `followVerifyAll` (600 seeds each, 0 findings): follow's settlement and the page chain refuse
  behind them; they are not member-level weakenings.
- **What deletes.** Row `inflatedHeight`, `Fault.inflateExpired`, `Mutation.ignoreNotBefore` (the generator
  reproduces the lie and the follower refuses `notYet`, the row's name: census `log:expired => refused notYet`).
  Not deleted, and why: `cancelLie`/`cancelForged` (the generator reproduces `cancelForged` by name, but
  Web/Sim/Testground's menu and testground/demos.js read their demos' expected outcomes off those rows); the
  other `Sys` booleans are plants of nd's OUTPUT or client (rawSlots, dropRow, noReadLimit, flatProgram,
  dropDoc, dropHint, guessMethod, oneMember, maskIncoming, twiceEach, dropRange, ignoreAnchor, …), which no
  Host lie reproduces: deleting them deletes coverage, not twins.

### Built

- `Protocol/Rows/Adversary.lean` (generator, judge, runner), `Protocol/Rows/AdversaryMain.lean`, lake exe
  `adversary` (`--seeds N --from S --deployed --no-swap --show --census --harness-control`).
- `Protocol/Rows/Loopback.lean`: `send` (the writer exchange), `ask` plays the relay tape (empty = honest, rows
  unchanged), `swapK`/`keepK` (continuation tape), `asRun` + `Seen` (judging records), `setup` (shared with
  `run`), `inflateExpiry`.
- gates/runs.tsv row `adversary	--seeds 200 --no-swap ; --seeds 40 --no-swap --deployed	ALL PASS	--seeds 200 --harness-control`.
- Decision PROTOCOL-80 (decisions/protocol.md).

### MEASURED (hbox, worktree ~/nd-land/qa6b at ca70d368 + this change; logs ~/nd-land/qa6-scratch/b5-*)

| run | seeds | result |
|---|---|---|
| toy, no swap (8 shards) | 0..1999 | ALL PASS; 589 actor catch-ups unjudged (cannot read from genesis) |
| toy, with swaps (4 shards) | 2000..2999 | 32 findings on ~30 seeds: okCommitted 22, signsOwn 10 |
| deployed (Ed25519, cSHAKE256), with swaps | 3000..3199 | okCommitted 7, signsOwn 2 |
| `--seeds 200 --harness-control` | 0..199 | FINDINGS 7 on 5 seeds (cancelOk), exit 1: RED as required |
| standing row: `--seeds 200 --no-swap`; `--seeds 40 --no-swap --deployed` | | ALL PASS, ALL PASS |
| `rows` (toy) | | 51 of 52 PASS; lang-journey (an exe row this change does not reach) past its 300 s deadline at load ~50 |

Earlier batches on the pre-rebase trees (same judge): 3000 + 5000 no-swap seeds ALL PASS; 2000 + 3000 swap
seeds 45 and 71 findings, the same three claims; 200/300 deployed seeds 2/7 findings. ~16,000 seeds in all.
Toy speed: ~0.1 s a seed with repeats capped at 1, ~1–3 s with the rows' repeats.

### Findings (each a cv task; reproduced AT 9c8bc4cf, toy: `adversary --from SEED --seeds 1 --show`)

Seeds at 9c8bc4cf: okCommitted 2035 (row journey), 2132 (pageIo), 6451; signsOwn 2089 (coldCatchUp), 2124
(fork); cancelOk 5765 (cancel), 6451, 7819 (cancelLie). A seed's row is drawn from `Protocol.rows`, so a
change to the rows list moves every seed.


1. **okCommitted, member level** (cv 01a17c6a-6c57): a resume handed an earlier phase-4 continuation of the
   same member ends a write `done ok` by that earlier call's settlement; the write was never signed or
   submitted. (HOLISTIC-PROTOCOL D3, measured.)
2. **signsOwn, member level** (cv 01a17c6a-6c74): a swapped phase-2/3 continuation makes follow re-plan an
   EARLIER argv on the current World and offer custody that call inside another command's run: a relay holding
   k replays a member's intent.
3. **cancelOk, member level** (cv 01a17c6a-6c83): `cancel CALL` resumed with another command's phase-4
   continuation ends `ok`; the call is not refused cancelled on the member's World.
   All three are the call↔argv tie Spec/README lists as owed (§11.2, cv 01a17a7a-1f6f); the spec's own claims,
   stated over the continuation's command, hold. The standing row runs `--no-swap` until that lands.
4. Observation, not a claim violation (cv 01a17c6a-868c): a cancel's final refusal other than `cancelled`
   ends the command `refused <the Host's own text>` (census `cancel:flip => refused cancdlled`), unsettled on
   follow's World.
5. **Process finding** (cv 01a17c37-7042): nano main d422453 (testground CLIENT-50) silently reverted Q5
   (1e0849d): emit-traces, client/tests/trace.rs and the five traces deleted, the ten deleted stand-ins back,
   Loopback's trace/attempt store/`ndRun` gone. Q6 was rebuilt on the post-revert harness.

No finding without swaps in ~12,000 toy seeds (four trees) and the deployed `--no-swap` runs: under every writer lie and every other
relay move the follower settled or refused by name.

### Loose ends (Q6)

- `hbox:~/nd-land/qa6-scratch/batch3.sh` (a superseded run on the pre-rebase tree) was stopped by its PID file;
  its in-flight child (`adversary --seeds 5000 --no-swap --census`, worktree qa6b's old binary, `nice`) has
  no PID file of its own and was left to finish. Nothing reads its log.
- scripts/commit materializes its tree at `~/nd-land/<worktree name>/tree`; with the worktree itself at
  `~/nd-land/qa6b` the lander's `tree/`, `tree.index` and `build.log` sit untracked inside the worktree.
  A lane worktree under ~/nd-land should not share the lander's name.
- `hbox:~/nd-land/qa6` (first worktree, pre-rebase base 262d5b4) is unused now.
