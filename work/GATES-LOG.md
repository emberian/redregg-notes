# GATES-LOG — BUILD-GATES continuation (2026-10-16, main 4bdf47f)

Owner of nanodregg's build and gates (CHARTER row CLOSURE). Repo `~/dev/nanodregg`; my editing worktree
`~/dev/nanodregg-wt/gates` (detached at main). Decisions: `decisions/gates.md` GATES-1..9. Earlier dossier:
`DELETE-CLOSURE-20261016.md` (minidregg module graph; Selvage enters the Host via the cSHAKE→Merkle-controller edge).

## The build
- `lakefile.lean`, no packages (GATES-1). Read by `gates/tree.py:lakefile()` with a STRICT grammar: package with
  the three leanOptions; `@[default_target] lean_lib X where globs := #[.submodules `X]`; `@[default_target]
  lean_exe «n» where root := `M`; one `extern_lib «ndhost»` compiling every `Host/c/*.c` (cc -fPIC -O2 -Wall
  -Wextra -Werror) into libndhost.a. Any other top-level form = C0 red. Layers add their own lib/exe lines
  (lakefile.lean is SHARED in OWNERS). Exe roots declare only `main` (C7).
- Proof-modules = a `Proofs` path component. Lean v4.30 `module` system was measured NOT to stop proof edits
  rebuilding importers (GATES-2), so the split is by file.

## Each gate: what and where (all in `gates/`, driven by `check.py`)
| gate | file | red on |
|---|---|---|
| closure C0–C8 | closure.py | C0 unknown lakefile form/missing option; C1 .lean outside a glob-rooted lib, top-level module; C2 import not tree/Init/Std (Lean only in Census); C3 def-module exports theorem or a Prop-valued statement (`is_prop`: result type Prop/Sort 0 after `:`/`→`), proof-module exports a non-Prop def; C4 def-module imports proof-module; C5 import of Census; C6 exe root missing/proof-module; C7 exe root declares more than `main`; C8 C source outside an extern_lib `<Lib>/c` |
| refusals | refusals.py | sorry; `admit` tactic (not the identifier); #guard/#eval/#print/#check/#reduce/#guard_msgs/#exit; example; axiom; partial; unsafe; @[extern]/@[implemented_by] outside `gates/native-allow.tsv` (Host.File); set_option heartbeat/recdepth/synthInstance budgets and autoImplicit/warningAsError/linter overrides; `List UInt8` in def-modules |
| size | size.py | SIZE.md `now` ≠ measured candidate; above ceiling; rise vs the MEASURED parent tree without `SIZE: <metric>: <why>`; raised ceiling without `SIZE-CEILING:`. Computes modules, lines per lib, deployed lines, Host closure (exe `nanodregg-host`), max dependents, theorems, partial, sorry, native count (ceiling 8), C lines (ceiling 146), Rust lines (client/src ceiling 2000), protocol ops (Protocol.Table `Op`, ceiling 6), call kinds (Kernel.Receive `Call`, 7), command verbs (Protocol.Command `Verb`, 20), refusal constructors (Kernel.World `Reject` + Kernel.Receive `Refusal`). Rows it does not compute are kept verbatim. Ceiling with no measurer → `WARN unmeasured` |
| waste | waste.py | table: ceiling raised / row removed without `WASTE: <op>: <why>`, measured>ceiling. `--measured FILE` (standing): pinned row above ceiling or unmeasured = red; measurement without row = `unpinned` |
| owners | owners.py + OWNERS | subject prefix (kernel/codec/emit/host/protocol/rows/client/sandbox/lang/gates/build/charter/root) must own every changed path per the PARENT's OWNERS; `CROSS-LAYER: <reason>` overrides |
| targets | check.py | a lib/exe in the parent lakefile missing from the candidate, without `LAKE-DROP: <name>: <why>` |
| census | census.py + Census/Axioms.lean | `#axiom_census "gates/axioms-allow.tsv" <libs>` over every tree module except Census and exe roots: only propext/Quot.sound/Classical.choice or an allow row (native_decide → Lean.ofReduceBool needs a row); stale allow rows red |
| generated | generated.tsv | `lake exe emit-rust --check client/src/generated.rs` differs |
A closure/refusal red the PARENT already has prints `PRE-EXISTING` and does not block (check.py, `--base-tree`).

## How scripts/commit judges (scripts/commit, scripts/pre-push, scripts/gate-lib.sh)
1. Outer loop (≤ COMMIT_RETRIES=5): materialize refs/heads/main into `<git-common>/nanodregg-commit-main/<pid>`
   and run THAT copy's scripts/commit and pre-push (never a working tree's). Exit 75 = main moved → re-read.
2. Private GIT_INDEX_FILE = main + `git add -A -- PATH…`; SIZE.md regenerated for the candidate (SIZE.md may be a
   PATH only to change ceilings); refuse any diff outside PATH… + SIZE.md.
3. pre-push --index: materialize candidate → `<common>/nanodregg-gate/tree` (incremental .lake), base = main →
   `…/base`; run candidate's gates/check.py and the parent's (both must pass; `GATE-CHANGE: <why>` lets a
   deliberate gate change pass the parent's); `lake build` changed modules + reverse dependents + every exe
   (ALL if lakefile/toolchain changed or cold); census; generated files; cargo check/clippy -D warnings/fmt
   --check per changed crate (CARGO_TARGET_DIR under common). `--no-build` needs `NO-BUILD: <why>`. One PID lock.
4. commit-tree + `update-ref refs/heads/main NEW BASE` (CAS). Then: primary checkout → reset landed index
   entries; worktree → reset landed entries to NEW, checkout NEW's SIZE.md, `checkout --detach NEW`.
- Hook `scripts/hooks/commit-msg` refuses every plain `git commit` (core.hooksPath=scripts/hooks).
- `scripts/worktree LAYER` → `~/dev/nanodregg-wt/LAYER`, detached at main. `scripts/size-sync` is legacy
  (scripts/commit regenerates SIZE.md) — delete it.

## Plants (each went red by name)
- `owners: KERNEL commit touches gates/plant.tmp, owned by GATES` → `scripts/commit: REFUSED by scripts/pre-push`
- `C4 Kernel.Planted (def-module) imports proof-module Kernel.Proofs.Admit`
- `C3 Kernel/A.lean:1 def-module exports statement inductive Foo (its type is Prop); …` / `C3 Kernel/Proofs/B.lean:1 proof-module exports def bar`
- `sorry: Kernel/Proofs/Planted.lean:2: theorem plantedSorry : 1 = 2 := sorry`; `admit` tactic line
- `AXIOM-CENSUS red (1): Nanodregg.Kernel.plantedSorry (Kernel.Proofs.Planted) uses sorryAx`
- `size: 'Lean lines (deployed)' rose 0 -> 578: the commit message needs 'SIZE: …'`
- `waste submit bytes-per-turn: measured 3.4 > ceiling 3.0` (+ `unpinned read cells-touched 1.2`)
- C: `Host/c/bad.c:1:25: error: unused variable 'y' [-Werror,-Wunused-variable]` (extern_lib prototype)
NOT yet planted in-tree: C0 unknown lakefile form, C7 exe root with logic, C8 stray .c, targets/LAKE-DROP,
generated-file staleness, stale allow row. Plant these first.

## Standing (scripts/standing.sh [REV]) — one line, appended to `<common>/nanodregg-standing/verdicts.log`
`STANDING <sha> gates= build= census= sim= rows= waste=(pinned, unpinned) unmeasured= => GREEN|RED|INCOMPLETE`
- gates/build/census: always run. census also fails on a stale generated file.
- sim: ABSENT until a lean_exe named `*-sim` exists; each runs `lake exe X SEED`, seeds `${SIM_SEEDS:-1 2 3}`;
  pass = exit 0 and last line `ALL PASS`; else RED naming the first `FAIL <check>`. kernel-sim exists (ROOT);
  host-sim is HOST-2's.
- rows: ABSENT until an executable `rows/run` exists (PROTOCOL-2); exit 0 = pass.
- waste: ABSENT until a sim prints `WASTE <op> <metric> <ratio>` or waste.tsv has a row.
- Any ABSENT or unmeasured ceiling ⇒ INCOMPLETE. Last measured: ee08ee6 INCOMPLETE (sim/rows ABSENT), 1m52s.

## Open items
- Plants listed above as NOT yet planted. Delete scripts/size-sync. `protocol status / step codes` and
  `conformance rows` SIZE rows are still hand-kept: compute them (Protocol.Status/Step constructors, Rows count).
- Host-closure metric uses exe name `nanodregg-host`; set it to whatever HOST names the server exe.
- Pin the first waste rows once HOST/KERNEL print WASTE lines (ceiling = first measurement).
- `max dependents of one module` has no ceiling (GATES-6 proposes one); 2-minute rebuild target unmeasured.
- Gate tree caches live under `.git/nanodregg-{gate,standing,commit-main,commit-size}` and `cargo-target` there;
  watch disk (Mac nearly full). No box builds.
- OWNERS has no row for `README.md`/top-level docs (default ROOT).

## Hindsight: the one change
Split SIZE.md's two roles: ceilings in a hand-edited `gates/ceilings.tsv` (GATES-owned, SIZE-CEILING ratchet),
SIZE.md a purely generated view. Today SIZE.md is half generated (`now`) and half hand-kept (ceilings, a few
hand rows), which is exactly what produced ROOT's 0f7c2d7 revert of PROTOCOL's rows and the "pass SIZE.md as a
PATH only to edit ceilings" special case in scripts/commit. (Runner-up: I bootstrapped the first gate commits by
hand from private indexes and caused two of the day's incidents — the gate should have landed first, minimal,
through itself.)

## ROOT note 10-16 for a GATES successor
- scripts/commit refused a ROOT commit of CHARTER.md with "ROOT commit touches decisions/client.md" when the worktree was detached at an OLDER main (484fa50 vs newer): the ownership diff appears to be computed against the worktree HEAD, not refs/heads/main. Re-detaching to main fixed it. Either rebase the candidate onto current main before judging (intended) or refuse with "worktree behind main: git checkout --detach main" by name.

## GATES-2 (2026-10-17) — continuation

Landed (Mac, before the load freeze): 9db4020 stale-worktree refusal + `--base` to pre-push (GATES-9);
9268939 post-landing primary move + origin push, standing `--here`/noParent/rows WASTE/strict GREEN;
fc7de01 SIZE split (gates/ceilings.tsv hand-edited, SIZE.md generated and refused as a PATH, status/step/rows
computed, C-lines-under-.git fix, gates/foundations.tsv with 7 foundations, ceiling 8, ROOT accepted all 7),
scripts/size-sync deleted; 5be0d98 owners prefixes hosting/ops/perf/transport (`kernel:` owns LEDGER paths),
closure C10 (nothing outside Ops imports Ops), temp-file refusal (createTempFile segfaults under a missing
TMPDIR, measured exit 139). Plants quoted in each message.
Pending as the FIRST hbox commit (patch `~/dev/nanodregg-wt/gates.hbox.patch` + untracked `scripts/mac-pull`,
message `<scratchpad>/gates2/msgE` with HBOX-PLANT-* placeholders to fill): landing guard
(`nanodregg.landing`), mac-pull, N flock judge slots, `nanodregg.buildwrap`, `nanodregg.worktrees`, every
target built + censused every commit (`affected` deleted; the stale-allow-row plant was GREEN before), RED
summary prints every gate's reds (LAKE-DROP printed none), GATES-9/10/11 in decisions/gates.md.

How things work now (deltas to the table above): size.py reads gates/ceilings.tsv + gates/foundations.tsv and
judges rises against the parent TREE; check.py has no --base-size; owners.SUBJECT maps a prefix to a SET of
layers; standing GREEN iff every stage value is exactly `ok` and no ceiling unmeasured; scripts/commit refuses
the primary checkout, a branch checkout, a stale PATH, SIZE.md as a PATH, (hbox commit:) a reader clone.

Open:
- Host/Sim/File.lean:67/:112 `IO.FS.withTempDir` — PRE-EXISTING temp-file red; HOST-4 told (via ROOT) to land
  D9 first; standing RED on gates until then.
- GATES-9's hole: a full-file Write of a buffer read before `checkout --detach main` reverts with HEAD = main
  (GATES-10 reopens on the first such revert).
- PROTOCOL-4 to add `WASTE invoke ticks-per-call` / `packages-checked-per-call` from the bar row and pin rows in
  waste.tsv (told the format).
- OPS item 3: a gates/generated.tsv row for `emit-units --check ops/units` when Ops/Units.lean lands; `bar=`
  standing stage RETRACTED by PERF (no wall-clock benching until near the end); Bench not in TOOLING_LIBS.
- After the hbox cutover: measure the always-build no-op cost and the 4-slot memory under swarm-build; run
  standing on hbox to see GREEN (needs HOST's temp-file fix).

### GATES-2 after the hbox cutover (10-17)
- Landed on hbox: 194cefb (landing guard, mac-pull, 4 flock slots, swarm-build wrap, every target built +
  censused; its message lost 3 plant quotes to shell substitution — verbatim in decisions/gates.md GATES-11
  status, ec2a88f), d5871cb (KILLED(load): signal 15/9 with no real Lean error ⇒ pre-push exit 76, scripts/commit
  "NOT JUDGED … re-run"; per-tree logs `<slot>/<tree12>.log`, newest 20 kept; census stale-row reason in summary).
- Work only in hbox `/tank/dregg-build/nanodregg/wt/gates`; Mac worktree deleted. Plant helpers in `hbox:~/gates2/`
  (plant.sh NAME BUILD PATH=FILE… judges main + mutation via pre-push, never lands; killwrap.sh). Lesson: build
  commit messages LOCALLY and scp them; a heredoc inside `ssh '…'` command-substitutes backticks.
- Plants: a plant's mutated file must be taken from MAIN, not the worktree (my allow-row plant used a stale
  worktree copy and dropped HOSTING's rows — the stale class again, in my own harness).
- Declined: per-module memory seats (a second scheduler beside lake). Report to CODEC via ROOT: Codec.Proofs.Ed25519
  (and Ed25519Sig) peak 9–14 GB per module — the real cause of the KILLED judges.
- Leftovers: `main/.git/nanodregg-gate{,.lock}` (pre-slot layout, unused; remove once nothing old runs).
- aa4c0ab (OPS asks): check.py gate `paths` (case-colliding paths red; APFS reader), OWNERS `deploy/ OPS` replaces
  `ops/`, Ops in TOOLING_LIBS (deployed count excludes it, C9 covers it). Note: any size.py change to a row NAME
  needs GATE-CHANGE (the parent renders the old name). Pending from OPS: generated.tsv `emit-units deploy/units`
  row lands WITH the files (CROSS-LAYER GATES, pre-agreed); store-plants standing stage when OPS sends the command.
- 41e9b2a: standing `plants=` stage (OPS's store-plants; ok at 808f38e) and sims no longer stop at the first red
  (a red sim used to cascade into a false waste red). Standing at 808f38e:
  `gates=ok build=ok census=ok sim=RED(hosting-sim 1: exit 0, last line: hosting-sim: GREEN) rows=INCOMPLETE(5 pending)
  plants=ok waste=ok(pinned 6, unpinned 0) unmeasured=0 => RED`. The sim red is HOSTING's: it must end `ALL PASS`.
- 84f3115 (ROOT/HOSTING): gates/runs.tsv + gates/runs.py — every lean_exe has a row (verdict runs or `-`); pre-push
  RUNS the exes whose closure holds a changed module (all on lakefile/toolchain/runs.tsv/C change), waste --partial at
  commit time; a run/waste red the parent shares is PRE-EXISTING (parent judged lazily, only when the candidate is red,
  with the CANDIDATE's runner+table, in the same slot, then re-materialized). standing: one `runs=` stage over the table.
  Cost: whole table ~17 s; plants 118–135 s end to end. f548ab5: runs.tsv SHARED in OWNERS.
- Standing at f548ab5: `runs=RED(rows : RED(ROW grain FAIL line 4: got refused program, expected ok))` — a real red on
  main (PROTOCOL/HOSTING's grain row), reported to ROOT.
- Plant harness on hbox: ~/gates2/plant2.sh (candidate = main + worktree gate files + mutation), plant3.sh (BASE=commit).
- e9d06c3 (HOST-6): conflict-marker lines (`^<{7}|>{7}( |$)`) anywhere in the tree are red (check.py `paths`). Cause of
  4c327a7: not a judge merge (scripts/commit never merges) but a lane's `git apply --3way` relay leaving markers in the
  worktree file, committed whole; GATES-9 cannot see it (HEAD = main by then).
- 23a1f31 (HOSTING-2): runs.tsv `cargo:CRATE:TEST<TAB>EXE,…<TAB>exit 0` rows (cargo test after the build, ND_LEAN_BIN = built
  bin, selected when CRATE/ changed or a driven exe is selected; RED names `---- NAME stdout ----`); first row
  cargo:launcher:isolation (hosting-drive). Agreed HOST-6's HOST-27 ceiling raise (native 9, C lines 161) as CROSS-LAYER.
- cb99f02 (ROOT): `ledger:` -> {LEDGER}, `kernel:` -> {KERNEL} only; OWNERS `Ledger/ LEDGER`, `world/escrow/ LEDGER`.
  f6992f0: `launcher/src/broker_generated.rs CODEC`. Agreed HOSTING-3's deletion of lifecycle_text_reads' two allow rows.
- OPEN (ROOT 10-17): CAS churn — landings needed up to 6 attempts (CLIENT-2 ran COMMIT_RETRIES=10). Design if it
  recurs: a FIFO judge queue (ticket file under $common, flock'd) so a lander is judged on the tip it will land on,
  instead of every miss re-judging from scratch; the CAS stays as the safety.
- 0f4a2ae (HOSTING-3/ROOT, fail-open): judging the parent with the candidate's table, a run the parent's OWN table does
  not hold row-for-row (or a cargo row whose test file the parent lacks) is `NOT RUN`, never a red, so the candidate's
  red is NEW (cc4f6fe's new broker row had landed as PRE-EXISTING). Audit of every parent comparison: size now reds a
  ceiling the parent measured and the candidate does not (was WARN only); closure/refusals/waste/census/owners sound.
- f4b00a2 (CODEC-27): refusals reject a string literal's `\xHH` followed by a hex digit (Lean v4.30.0 C backend emits it
  verbatim; C's \x is greedy). Lift when the toolchain splits the C literal; re-run the plant then.
- Agreed LANG-7's re-pin `invoke ticks-per-call` 30 → 34 (LANG-33 result record, deterministic +4) as CROSS-LAYER with a
  WASTE line. OPEN critique handed to LANG: ticks-per-call is an ABSOLUTE count, not a law-5 ratio; it rises with every
  honest semantic change, so ceilings get raised routinely and hide real waste. Owed: ticks ÷ required ticks (e.g.
  machine ticks over the BigStep derivation size), pinned near 1.
- 248fcea (ROOT, workspace): OWNERS `Cargo.toml SHARED`, `Cargo.lock SHARED`, `devtools/ CLIENT`. LANDED 6460e1f after CLIENT-3's cb6df3f: rust_changed -> `workspace` on root Cargo.*/member paths;
  pre-push judges the workspace once (`cargo check/clippy --locked --workspace --all-targets`, `fmt --all --check`);
  runs.py cargo rows `cargo test --locked --manifest-path Cargo.toml -p PACKAGE --test TEST`. Plant to run then: a member
  that does not build -> cargo-check RED.
- 6460e1f: workspace judge (see above). 2ed0386 (OPS-2): generated.tsv `cargo:BIN` rows (`cargo run --locked --bin BIN --
  --check PATH`), one `generated_check` for pre-push+standing (wraps inside: a shell function cannot be handed to
  swarm-build); CARGO_TARGET_DIR set once per judge. OPS-2 lands `cargo:emit-anchors deploy/tls/anchors.pem` CROSS-LAYER.
  Agreed HOSTING-4's broker-row edit (drives hosting-broker,host).
- Agreed LANG-9: replace `invoke ticks-per-call` with `invoke ticks-per-required-step` (machine ticks ÷ BigStep rule
  instances + forced suspensions; Lang/Sim/Need.lean), old row deleted. Conditions: the count is pinned EXACTLY to the
  derivation (an overcounting Need := ticks would satisfy `≤ ticks` and hide all waste); a plant (needless machine work)
  must push R over the ceiling by name; vacuity reader on the statement.

### GATES-2 HANDOFF (10-17, ~430K tokens; successor = GATES-3)
State: every GATES-2 change is landed on hbox main and pushed; hbox wt/gates is clean at main. Work ONLY in hbox
`/tank/dregg-build/nanodregg/wt/gates` (Mac is a reader). Write commit messages locally, scp them (heredocs inside `ssh '…'`
eat backticks). Plant harness: `hbox:~/gates2/plant2.sh NAME BUILD PATH=FILE…` (candidate = main + the worktree's files
listed in its `for f in` line + the mutation; never lands), plant3.sh (BASE=commit). Take mutated files from MAIN.
Pending with others (agreed, they land):
- CODEC-6: refine census (Census/Refines.lean, gates/refines-allow.tsv) CROSS-LAYER; conditions: head-constant Lawful/
  LawfulOn conclusion, allow rows name their Equiv theorem, 3 plants, land only after HOST-9's host/base theorem.
- LANG-9: waste row swap to `invoke ticks-per-required-step` (exact count theorem + a waste plant).
- OPS-2: generated.tsv `cargo:emit-anchors deploy/tls/anchors.pem` with the bin.
- HOST-6: HOST-27 ceilings (native 9, C lines 161). HOSTING-4: broker row drives hosting-broker,host.
Open for GATES-3:
- CAS churn → FIFO judge queue if landings exceed ~3 attempts again.
- Measure always-build + runs cost on 4 warm slots; remove `main/.git/nanodregg-gate{,.lock}` (pre-slot leftovers, mine).
- GATES-10 reopen trigger: a silent revert with HEAD = main (stale editor buffer).
- Standing at f548ab5 was RED on rows (grain FAIL), PROTOCOL/HOSTING's; re-run standing.

## GATES-3 (2026-10-17, successor of GATES-2)
- LANDED 53af302 (GATES-12): gates/tcb.py, check.py gate `tcb`. Refuses by name: locked crypto/TLS crate (CRATES/PREFIXES
  data in tcb.py) with no gates/tcb.tsv row or pin != locked version set; stale crate row; lean4 row missing/!= lean-toolchain;
  native_decide allow row with no `native_decide:<thm>` row pinned to the toolchain (+ stale converse); native-allow.tsv
  module with no `extern:<module>` row (+ converse); lake-manifest package with no row; malformed / unknown kind / owner /
  duplicate. 42 rows added to HOSTING-5's 0eb0803 table (texts from HOSTING-5, CLIENT-3, CODEC-6). Plants:
  hbox `logs/gates3-plants.sh` (8 mutations + control through pre-push --no-build, ~7 s each), output `logs/gates3-plants.out`.
  Named hole: a crypto crate under a name the list does not know passes (reopen GATES-12 if one lands).
- CODEC-6 adds Codec.Sha512 + Codec.Hash rows itself (free-form components; only columns/kind/owner/uniqueness checked).
- Agreed + landed by LANG-9: 03f942a `invoke ticks-per-required-step` ceiling 1.546 (34/22 rounded UP), printed 1.545.
- STANDING 53af3023c400 gates=ok build=ok census=ok runs=ok waste=ok(pinned 24, unpinned 0) unmeasured=0 => GREEN (127 s warm).
- CAS churn measured from lanes' commit logs (last 60): max 3 `main moved` retries (host8-commit3, 4 attempts), all others
  <= 1. At the trigger, not over it: FIFO queue NOT built. Rebuild trigger stands (> ~3 retries recurring).
- Slot cost (bytes, apparent / on-disk ZFS): slots 1-4 = 2283/1548/991/612 MB apparent (on-disk 1120/763/489/301 MB);
  per slot .lake 427-1340 MB + cargo-target 178-935 MB + base 5 MB + 20 logs. standing 936 MB. Memory per slot unmeasured.
- Removed (mine, pre-slot): main/.git/nanodregg-gate (177 MB apparent, 86 MB on disk, last used 10-17 04:27); no .lock existed.
- Pending as they arrive: CODEC-6 refine census (HOST-9's Base.codec_lawfulOn landed 40fe056, so ordering condition met);
  HOST-33 flag day (HOST-9 sends waste rows first; conditions sent: WASTE line per raised/deleted op, new rows pinned at
  first measurement rounded UP, quote printed lines, tell me of generated.tsv changes).
- CODEC-6's refine census LANDED 10fd373 (Census/Refines.lean, gates/refines-allow.tsv 2 rows naming their Equiv/decode
  theorems; census.py requires `REFINE-CENSUS ok` beside `AXIOM-CENSUS ok`, so an absent verdict is red). Its 3 plants are
  quoted in its commit. Standing at 10fd373: GREEN (`REFINE-CENSUS ok: 26 refine sites, 24 with a lawfulness theorem, 2 by
  allow row`). Codec.Sha512 + Codec.Hash tcb rows landed in the same commit.
- LANDED d13c5b0 (GATES-13, CODEC-6 ask on ec2db07 codec vectors): gates/vectors.py, check.py gate `vectors`: rows under a
  (site, tag) shared with the parent's gates/codec-vectors.tsv must be identical (edited/removed/added red). Plants
  hbox logs/gates3-vplants.sh (.out). OWNERS left GATES on the table (SHARED would loosen owners: pause item, not needed).
- HOST-33 waste rows AGREED (sent to HOST-9) with conditions: one `WASTE: seal:` line naming the six rising seal rows and
  the trade (per-entry MAC → open reads one entry); 0.001 falls printed <= ceiling; the new `page index-entries-read-per-
  request-at-N` absolute counts (7/8/9/10) replaced by ratio rows `page index-entries-read-per-log-bound-at-N` = read ÷
  (1+⌈log₂ entries⌉), pinned at first measurement rounded UP; resident rows 1.000 ok; emit-units re-emit judged byte for byte.
  Awaiting its sha; on landing, run standing.
- HOST-33 LANDED ff60a08 under the conditions (page rows as log-bound ratio 1.000). Its codec-vectors re-draw (host/entry
  dropped, host/base renamed host/base/index-count) is covered: Emit/Vectors `check` reds a live site with no current-tag
  rows and every orphan row; vectors.py covers same-tag edits. A site removed from Emit/Vectors' `sites` list is CODEC's
  review (no gate ties `sites` to the refine census's 26 sites — candidate next gate if a site ever goes missing).
- STANDING 2d76795b53d4 gates=ok build=ok census=ok runs=ok waste=ok(pinned 32, unpinned 0) unmeasured=0 => GREEN.
- Queue empty at ~2d76795. Open: slot memory per judge unmeasured; FIFO queue on recurrence (>3 retries); GATES-10 reopen
  trigger unchanged.
- Law-6 read of the two refines-allow rows DONE by CODEC-7 (decisions/codec.md CODEC-30, c0548be): both stand, non-vacuous,
  canonicity exact on bytes; Equiv is forced by World.journal being a Std.TreeMap. Transmutable, not terminal: a canonical
  journal type (sorted-list subtype or a second Trie.T) would give `=` and must delete both rows in that commit (the census
  reds an allow row for a site with a plain theorem). KERNEL's call; asked CODEC-7 to file it with KERNEL as a cv task.
- AGREED HOST-10's HOST-35 ceiling raise `C lines` 156 -> 159 (nd_file_sync fails ENOENT on st_nlink = 0: acknowledged writes into an
  unlinked seg.log were lost), cross-layer, with the plant-sync-unlinked red + named control quoted, and the extern:Host.File tcb row
  amended if macOS behaviour differs.
- HOST-35 LANDED e285406: C lines ceiling 159 with the agreed SIZE-CEILING line, plant-sync-unlinked control + refusal quoted,
  extern:Host.File tcb row states the st_nlink fact (Linux measured, macOS/APFS UNMEASURED). Verified on main.
- AGREED LANG-11 prose-only edit of waste.tsv `invoke ticks-per-required-step` source (two plants waste-app 1.818 / waste-extract
  2.136, MOVED/BLIND checks in rows); plant values stay in Protocol/Rows/Run.lean, not waste.tsv; asked for exact-string MOVED
  compare + one MOVED plant quoted. cv 01a14abb-aa73.
- AGREED PROTOCOL-7's KERNEL-42 re-pin: admit hashes-per-touched-cell 8.915 -> 8.969, hashes-per-nullifier 3.211 -> 3.336 (id-draw
  workload; control 9.002 / 3.413; no hashing code changed). Critique filed cv 01a14afe-7380 (KERNEL): replace both with a
  shape-normalized ratio (required hashes counted from the built trie), draw-independent, pinned near 1; per-insert plant.
- LANG-11 LANDED e2c1b4c (prose-only waste.tsv source; MOVED exact-string; MOVED red quoted `plant waste-extract MOVED 2.136≠0.000`).

## GATES-5 (2026-10-18, successor of GATES-3/GATES-4's faerie)
- LANDED 56f4689 GATES-15 landing A (fail-open): pre-push read only `run …: RED` keys, so a crashed runs.py was
  `runs: ok` (old judge measured: `PRE-PUSH GREEN tree c260c49f760b`). Now: no verdict line / rc1-unnamed / ABSENT =
  `runs: NO VERDICT` RED, never PRE-EXISTING; PRE-EXISTING per FAIL line (`    red RUN: LINE` keys); cargo rows 4th col
  `nobin RED|nobin ok` (ND_LEAN_BIN = empty dir, run first; UNREAD otherwise); ≥1 test passed; rust_changed fail-closed;
  in-tree `scripts/plant [--build] [--with PATH]... NAME EXPECT [PATH=FILE]...` with its own known-red control
  (replaces ~/gates2/plant2.sh). Plants: hbox logs/gates5-plants.sh, gates5-plants2.sh, gates5-oldjudge.sh.
- STANDING 56f46893a7c7 GREEN (pinned 41). The six earlier GREENs checked: verdict lines present, no traceback.
- Audit (subagent) of every runner: Lean exes fail-closed inside; open: kernel-sim parseSeeds drops unknown args + <16
  seeds skips plants yet ALL PASS; host-sim/host-file-sim drop unknown args; lang-journey takes no args;
  deploy/live/harness.sh journal across runs (OPS-4 fixed it: 2d4c38d OPS-16); bar.sh plant never run (PERF cv 01a14e19-a82f).
- Landing B (ROOT ruled: I write all hooks, ONE cross-layer commit; owners see diffs: HOST-12, PROTOCOL-12
  ab85c36fd01b6c4eb, OPS-4 aed11c6f616bf7fbe, LANG-15; ROOT stands in for HOSTING/LEDGER; kernel-sim after KERNEL-18's
  day with its yes): `--harness-control` per exe, one never-met expectation inside the ordinary run; runs.tsv requires the
  column on every verdict row (delete the landing-A leniency clause in runs.py table()); close cv 01a14e41-d666 then.
- FIFO trigger (10-18 landing logs): max 4 `main moved` (protocol11-commit.log), then 2 (protocol9-5, host12-43,
  kernel13-land4, lang15); one landing over 3 retries. Not recurring: no queue built.
- B DRAFTED (uncommitted in hbox wt/gates on 66815ff; whole patch logs/gates5-landb-hooks.patch md5 7ecd6144, per-owner
  gates5-landb-{Host,Protocol,Ops,Lang,HostingLedger}.patch; hook script logs/gates5-hooks.py). Built + judged via
  `scripts/plant --build --with … landb-green GREEN`: build ok, runs ok 43, all 7 controls RED by name (only SIZE lines
  missing). Diffs sent: PROTOCOL-12, OPS-4 direct; HOST-12, LANG-15 via ROOT; ROOT for Hosting/Ledger.
  TO FINISH B after KERNEL-18 lands (it reviews the kernel patch first): on its tip, Kernel/Sim/Main.lean strips
  `--harness-control`, parseSeeds refuses unknown args / `--seeds 0` (exit 2), report adds "harness-control" to the
  required list, <16 seeds prints `PLANTS NOT JUDGED (<16 seeds)` exit 3 (control run must still be judged: use
  `--seeds 16 --harness-control`); runs.tsv kernel-sim control `--seeds 16 --harness-control`; delete runs.py's
  LANDING A clause (3-col Lean rows); B plants: a control made to pass (UNREAD + `harness: the known-red control passed`),
  a verdict row without a control (check.py red), `host-sim foo` exit 2, `kernel-sim foo` exit 2; SIZE lines; close
  cv 01a14e41-d666 with the hash. Then standing after the trie day (vectors listings byte-identical claim; SIZE lines
  row should FALL with KERNEL-35's plumbing deleted).
- B reviews: PROTOCOL-12 YES (control reaches only the `.caught` rows, 27 on main / 29 after PROTOCOL-47; runs.py
  needs only "reads red naming harness-control", no count; PROTOCOL-13 succeeds it). OPS-4 YES; its two notes are applied
  in the worktree (usage string `[--harness-control]`; comment: the control proves judge/count/exit, not the `say` rows).
  Put both scopes in the B critique. Waiting: HOST-12, LANG-15 (via ROOT), ROOT for Hosting/Ledger, KERNEL-18's day.
- KERNEL-18's trie day landed d377d5b. kernel-sim hook written on its tip (logs/gates5-landb-Kernel.patch md5 4cd3a380,
  sent for review); runs.py LANDING A clause deleted; whole B = logs/gates5-landb-all.patch md5 1772074e (12 files, in
  wt/gates uncommitted). B plants (logs/gates5-plantsB.sh, gates5-args.out): all 7 controls RED by name (kernel:
  `never met: [harness-control]`), rows-control-inert -> `harness: the known-red control passed` + UNREAD,
  verdict-row-no-control refused by check.py, unknown args exit 2 on kernel-sim/host-sim/host-file-sim/lang-journey,
  `kernel-sim 1` INCOMPLETE(PLANTS NOT JUDGED). Only SIZE lines red (the commit message needs them: Host +18, Hosting +6,
  Lang +11, Ledger +6, Ops +6ish, Protocol +8, Kernel, tooling — read the exact list from the judge at landing).
  NOTE: after a RED judge the slot's binaries are the PARENT's (pre-push re-materializes but does not rebuild the
  candidate) — never run slot binaries by hand after a red judge.
- STANDING b040f213c593 GREEN (pinned 44). Trie day: vectors +4 rows new site kernel/proof only, `vectors: ok` x5;
  SIZE did not fall (Kernel +1755 lines of compressed-trie proofs outweighed KERNEL-35's deleted plumbing; no ceiling moved).
- Waiting: KERNEL-18 yes; HOST-12, LANG-15 (via ROOT), ROOT for Hosting/Ledger; ROOT on whether to wait the full day.
- KERNEL-18 YES to gates5-landb-Kernel.patch (4cd3a380), no changes; cite it in CROSS-LAYER. Main at 8ad3982 (no Kernel/Sim change). Still waiting: HOST-12, LANG-15, ROOT (Hosting/Ledger + timing).

## GATES-6 (2026-10-19, successor of GATES-5)
- wt/gates moved d377d5b -> 8ad3982 by `checkout --detach main` carrying the edits (no B file changed between; diff md5
  1772074e before and after; saved as logs/gates6-landb-wt.patch). decisions/gates.md GATES-15 gained the Landing B /
  Plants (B) / Critique (B) / Status paragraphs (logs/gates6-dec.py). Message logs/gates6-msgB.
- LANDED 0e1b027 GATES-15 landing B (1 `main moved` retry for bada768). Landing judge gate log
  main/.git/nanodregg-gate-1/af9231e6f720.log: all 8 Lean controls `ok(known-red control read red)`, runs ok 44/30.
  cv 01a14e41-d666 DONE. HOST-13 and LANG-16 sent yes after ROOT's stand-in (acked; no DIR-only host-file-sim caller,
  git grep).
- STANDING 0e1b027ef2c4 gates=ok build=ok census=ok runs=ok waste=ok(pinned 44, unpinned 0) unmeasured=0 => GREEN.
- Slot cost (bytes, 10-19, apparent / on-disk ZFS): gate-1 8754/3924 MB, gate-2 4198/1979, gate-3 2525/1202,
  gate-4 1624/758, standing 2365/1079. gate-1 breakdown: tree/.lake 1528 MB, cargo-target 7210 MB, of which
  cargo-target/tmp 5739 MB = 1628 leaked test dirs (iso-/isob-/kb-PID-NAME from launcher/tests, never removed;
  grows per judged landing). Filed cv 01a14ed7-79cf (HOSTING). Deleted nothing. Since GATES-3, slot 1 grew 2283 -> 8754 MB,
  mostly from that leak.
- Next: standing duty as KERNEL-19, PROTOCOL-13, HOST-13, LANG-16, HOSTING-8 and PERF-1 land.
- PERF-1 asked for a yes on logs/perf1-gates.diff (runs.tsv row kind `script:PATH`, scripts/bar.sh --standing,
  always selected, ~16 s). YES with conditions: (1) env.pop ND_BIN in the script branch (an inherited ND_BIN judged
  prebuilt non-candidate nd binaries: a fail-open); (2) --root {fresh} inside the judge scratch (the $HOME default
  leaves ndbar.* on SIGKILL); (3) control limit 0, not x0.0001 (independent of clock speed). Plants: control inert ->
  UNREAD, a `-` script row refused, a non-exec script refused; GATE-CHANGE (the parent's check.py reads "names no
  lean_exe"); CROSS-LAYER naming GATES-6. On landing: standing.
- cv 01a14ed7-79cf FIXED by HOSTING b9cd50f (isolation.rs `Tree` removes on drop, panic included). Verified: standing
  b9cd50f ran all cargo:launcher rows + nobin controls; standing cargo-target/tmp 203 dirs before = 203 after. Closed.
  Pre-fix leftovers remain (slot tmp dirs 1772/544/139/36, standing 203): Ember's to clear, reported to ROOT.
- STANDING b9cd50fbc88c gates=ok build=ok census=ok runs=ok waste=ok(pinned 44, unpinned 0) unmeasured=0 => GREEN.
- PERF-1 LANDED de718bf (script:scripts/bar.sh row) meeting conditions 1-3. Custody workspaces + sockets stay in a mktemp
  dir under $HOME (custody StrictModes refuses keys under any 775 ancestor; /tank paths are 775), KB, trap-removed,
  left behind only on SIGKILL. Accepted. STANDING de718bf752d5 GREEN (pinned 49).
- LANDED 12cadcc: scripts/plant plants a file with its own mode (it had been 100644 always; --with had taken main's mode).
  Plants in logs/gates6-plantmode.out: new bar-exec GREEN, bar-nonexec RED "no executable", old tool bar-exec-old FAIL.
- AGREED PERF-3: Bench in TOOLING_LIBS + lean_lib Bench + bench-count exe + `-` row; asked for the size.py tooling label
  to be renamed (+Bench) with a SIZE line in that commit, and the C9 red without the line quoted.
- STANDING f82a6b081cdc (KERNEL-19, refusalsCounted flag day) GREEN (pinned 49). Vectors: the moved sites are exactly the 12
  the commit names (refusal-leaf, refusal-order, journal, refusals, refusals-disjoint, steps, world-budget, rows,
  rows-headed, rows-parented, host/base/index-count, + new refusals-counted). kernel/refused is unmoved, consistent: the
  member goes in RefusalLeaf, not in Refused.
- AGREED HOSTING-9 emit-pins (lean_exe + generated.tsv row; empty deploy/tls/pins). No gate refuses a zero-byte file.
  Asked for plants: one byte added is red, a deleted file is red (missing must never equal empty), and the runs.tsv `-` row.
- LANDED 148ac60 GATES-16 (ROOT's judge finding, KERNEL-19 attempt 2 isolation TIMEOUT): a timeout is re-run once,
  then UNREAD(timeout twice …) with the partial last line, runs exit 76, `PRE-PUSH NOT JUDGED`, standing UNJUDGED =
  INCOMPLETE; no longer a key (never RED, never PRE-EXISTING); ND_RUN_DEADLINE knob. Plants logs/gates6-g16plants.out.
- FLAKE seen under a plant: cargo:launcher:broker a_bad_socket_directory_stops_keybroker_by_name red on the candidate, green
  on the parent minutes later in the same slot (keybrokerGone; sockDir under $HOME/.cache/nd-t shared by every slot).
  Sent to HOSTING-9.
- PERF-1 has orphaned strace/nd-supervise/host trees (ppid 1, ~2.5 h, PIDs 779667, 818024). Told PERF-1; I touched nothing.
- LANDED 7de131e GATES-17 (ROOT ruling via PERF-1: PERF-5's bench-worstcut is standing-only). runs.tsv key `standing:EXE`,
  run by runs.py --standing (standing.sh only), pre-push prints NOT RUN(standing-only); a `-` standing row and a second row
  for the exe are refused. Plants logs/gates6-g17plants.out. The standing side gets verified on PERF-5's first standing.
  (A PID file was not written for that landing because of a shell var slip; the job ended on its own. Fixed in my next launch form.)
- HOSTING-9: the broker flake is interleaved stderr (keybroker eprintln! in pieces + decider's keybrokerGone line); fix is
  one write_all per end line, in its next landing. Per-pid scratch, so no collision. Closes with its hash.
- STANDING c392f512db4b (PERF-5 bench-worstcut, first standing row) GREEN (pinned 56): `run standing:bench-worstcut {fresh}
  --harness-control (control): ok(known-red control read red)`, `run standing:bench-worstcut {fresh}: ok`. GATES-17 standing side verified.
- AGREED PROTOCOL-15: rows row gains a `--deployed` run (67 s) in pre-push; one toy control; asked for the deployed control
  read + plant line + `run rows --deployed: ok` to be quoted.
- HOSTING-9 LANDED 9df02da: emit-pins + generated row + runs row; broker flake fixed (one write_all). Its pins plants ran as
  direct `emit-pins --check` exit codes (byte added: 1, deleted: 1), not through scripts/plant. Equivalent, because the
  generated step is exactly that command. STANDING 9df02da3bd2d GREEN (pinned 56).
- PERF-2 (PERF-6): YES to the worstcut waste rise 20.374 -> 33.959 (ROOT first-measurement ruling). NO to a control that
  builds only `writes`; asked for all three shapes with the impossible expectation on the LAST shape counted.
- AGREED HOSTING-10 HOST-52 (Host.Sock): native-allow row, ceilings native 9->12 and C lines 159->315 (exact), host-sock-probe
  `-`, cargo:launcher:sock nobin RED, tcb extern:Host.Sock (Linux measured, macOS unrun, MSG_NOSIGNAL toothless named),
  lakefile exe. Also agreed in advance: landing 2 (lean_exe resident, `resident -`, cargo:launcher:resident_bell nobin RED).
- KERNEL-20: YES to the waste row `audit verifies-per-refusal`; ratified c18e028's `refuse verifies-per-refusal` (it landed under
  a CROSS-LAYER reason not naming GATES; owners.py checks that a reason exists, not whom it names). Check that the next standing measures both.
- CLIENT-8: YES to size.py `Rust lines (nd-members)` + ceiling 550 (equal to the measured count); runs.tsv `cargo:launcher:members` row REQUIRED
  (nobin RED with the exes it drives, else nobin ok selected by emit-broker).
- STANDING a13008767f2b GREEN (pinned 57): refuse verifies-per-refusal measured 1.000 (c18e028's row judged); rows --deployed ran.
- LANDED 98e686d GATES-18 (ROOT ruling): CROSS-LAYER must name the owner layer of each foreign path (word match, `-N` lane
  ok, `_` `/` separate; `HOSTING` does not name HOST). scripts/plant's default line names every OWNERS layer + ROOT;
  `--cross-layer REASON` overrides. Plants logs/gates6-g18plants.out. Replay of 150 commits: the new rule refuses 16 of 55 CROSS-LAYER
  commits, most often for an unnamed GATES owner (codec-vectors.tsv / waste.tsv / ceilings.tsv). Watch: if codec-vectors.tsv
  naming becomes noise, argue an OWNERS row.
- AGREED PERF-8 standing:bench-worstworld (34 s), waste worstworld decode-trie-hashes-per-entry 2.000 (scale-free).
- GATES-19 (ROOT: the judge-queue trigger fired; HOST-52 took 6 runs). Measured over 36 h of commit logs: 216 landings,
  attempts 153/45/10/7/1, one gave up, 90 GREEN judges lost to the CAS, 19 behind-main runs. DESIGN at
  /Users/ember/dev/redregg/work/GATES-19-DESIGN.md. ROOT ruled: 3-way merge yes; queue by readiness with an age
  bound (after 2 displacements, head); keys plus a final re-check, so a stale verdict cannot land. Replay: reuse
  42.9% static / 58.6% traced; it pays (306 to 216 full judges, the tail bounded at 3 passes, 19 manual re-applies
  become merges). NOT BUILT: handed to GATES-7 (design §5, §6, §7, §8).

### GATES-6 continuation for GATES-7
- Main on hbox; wt/gates is clean, detached at main. My landings: 0e1b027 (GATES-15 B), 12cadcc (plant mode), 148ac60
  (GATES-16 timeout = UNREAD), 7de131e (GATES-17 standing: rows), 98e686d (GATES-18 CROSS-LAYER names owners).
  Last standing: a13008767f2b GREEN (pinned 57).
- Open yeses not yet verified on landing: PERF-6 (worstcut control must build all 3 shapes, impossible expectation on the
  LAST shape; I refused the writes-only control), PERF-8 bench-worstworld (verify its first standing control line),
  CLIENT-8 nd-members (runs.tsv cargo:launcher:members row required), KERNEL-20 audit row (verify measured in
  standing), HOSTING-10 landing 2 (resident).
- PERF-1/PERF-2 left orphaned strace trees in wt/perf (PIDs 779667, 818024 at 10-19): theirs to stop. Pre-fix
  launcher tmp dirs remain in the slots (Ember's call).
- Standing duty: run scripts/standing.sh after each landing wave; a fail-open finding outranks everything.
- Build GATES-19 from the design file. First write gates/rebase.py as a pure function with its plants, then the
  scripts/commit queue, merge and re-base loop, then scripts/plant --rebase.

## GATES-7 (2026-10-18/19, successor of GATES-6) — building GATES-19
- Built in wt/gates (unlanded while this is written): gates/rebase.py (merge, keys, verify, check), gates/land.py (the
  queue), gates/doc-allow.tsv (`decisions/`), runs.py --keys/--reuse/--record, pre-push --record/--reuse/--verify,
  scripts/commit (merge at entry; outer loop = the lander: ticket fd 6 + lander dir; land.py instead of the bare CAS;
  record.new -> record.prev on 75), gate-lib.sh new_ticket, scripts/plant --rebase B0 [--forge UNIT] [--onto REV].
- Merge plants (logs/gates7-merge.sh/.out, scratch worktree wt/gates-plant at 35daeab): old judge `worktree behind main
  on gates/runs.tsv`; new: clean merge writes both edits and judges; same-spot insert refused with hunks, worktree md5
  unchanged; deleted-vs-changed refused.
- Queue plants (logs/gates7-queue.sh/.out, scratch ref refs/nanodregg-plant/queue): judging lander blocks no ready one;
  a displaced-twice lander makes a ready younger one wait (`queue: waiting for … (displaced 2)`), lands, and the
  younger is displaced; a dead head (holder stopped by its PID) is released by flock; age bound: displaced on passes
  1 and 2, head on pass 3 while a younger ready lander waits; CAS still refuses a stale base.
- FINDING (design correction): a run's key must cover EVERY binary, not its own exe's: rows runs `lake exe NAME`
  (Protocol/Rows/Run.lean), store-plants drives {host}. Re-replay of the key as built (logs/gates7-reuse.py, 150
  pairs): static reuse 10.4% (5.4% before SIZE.md was excluded as derived), not 42.9%. The traced read-set (§7) is
  where the reuse is; it is the next GATES item.
- ROOT additions folded into GATES-19: (0) LANG-18's selection gap: any changed non-.lean path outside
  gates/doc-allow.tsv and SIZE.md selects every row (96/150 landings: the cost, stated); (0b) standing-only is a
  cost choice: a standing row whose inputs changed (data path or closure module) runs in pre-push.
- Plants pass 2/3 (logs/gates7-keys2.*, gates7-p3.*): g19-select-old GREEN (the bug) / g19-select RED resident_bell;
  g19-standing-input runs bench-worstcut in pre-push; g19-doc all reused; g19-data all re-run; g19-forge RED stale
  verdict, unforged control `verify: ok (24 units …)`; g19-semantic RED after `re-run (key changed)`; g19-allow RED;
  merge clean/conflict/deleted; inert control RED, timeout NOT JUDGED, unnamed owner RED.
- Standing: 07f31d60c050 GREEN (pinned 59; HOSTING-10 landing 2 resident_bell control read red; PERF-8 bench-worstworld
  control read red); f68f968280b2 GREEN (CLIENT-8 ecb02bf: members row nobin RED, nd-members ceiling 550 = measured);
  b48c10fea029 GREEN (KERNEL-54: vectors moved exactly the named families incl. new varint64/row-leaf-hashed; WASTE
  exactly 3 ruled rises + 3 falls, measured equal; SIZE lines present; CROSS-LAYER names every owner; its attempt-1
  owners refusal on LEDGER files = GATES-18 working); 482aeccd143a GREEN (KERNEL-56: no gates/ change, theorems
  4141 -> 4201 = +60 as its SIZE line says).
- Agreed HOSTING-11 (HOSTING-33): lakefile exe hosting-residents + runs.tsv `-` row + members row drives
  hosting-residents,host (nobin RED kept; quote the control line) — it has since landed as e1e8084.
- LANDING launched: logs/gates7-commit19.log (pid file gates7-commit19.pid), message logs/gates7-msg19.
- The landing itself, under the OLD judge: attempt 1 PRE-PUSH GREEN 798fad809639, main moved; attempt 2 GREEN
  fb631ddbb3a9, main moved; attempt 3 judging as this is written (each a full row set + both benches, ~25 min).
  The class GATES-19 removes, measured on GATES-19.

### GATES-7 continuation for GATES-8
- Check logs/gates7-commit19.log first. If it LANDED: run scripts/standing.sh on main and quote it; tell ROOT the
  hash; tell lanes to `git checkout --detach main` so their outer scripts/commit holds a ticket (an old outer loop
  works but gets no reuse record and starts at zero displacements). If it GAVE UP (5 attempts): relaunch the same
  command (message logs/gates7-msg19; paths in the message's file list: gates/rebase.py gates/land.py
  gates/doc-allow.tsv gates/runs.py gates/check.py scripts/pre-push scripts/commit scripts/gate-lib.sh scripts/plant
  decisions/gates.md). The edits are in wt/gates (uncommitted until it lands); decisions/gates.md has GATES-19 appended.
- NEXT GATES ITEM (ROOT): traced read-sets (design §7). They carry both the narrowing of the fail-closed selection
  (today every data-path change runs every row, 96/150 landings) and the real reuse (static 10.4%). Shape: standing
  (or each judge) runs every row under `strace -f -qq -e trace=openat,open,execve` and records per row the tree paths
  opened, dirs listed and binaries exec'd, keyed to the tree it ran on; selection = closure ∪ rows whose trace opened
  a changed path ∪ every row with no trace; run keys = the traced set instead of every non-.lean path and every
  binary; no trace / non-zero / unparsable = the static fallback. Plants per §7 (traced world/x.ob re-runs; strace
  missing falls back and re-runs) plus: a path added to a directory a row lists selects it.
- Open: the gate_slot fallback waits on slot (pid mod n) even when another frees (seen 10-18: my plant waited ~10 min
  with slots 3/4 free). Small, GATES'.
- Scratch to clear (mine): wt/gates-plant worktree (git worktree remove), refs none left, logs/gates7-*,
  <common>/nanodregg-plant/queue-g19 (dead tickets), logs/gates7-mut, gates7-mut2, gates7-up.

## GATES-8 (2026-10-18/19, successor of GATES-7)
- GATES-19 LANDED as 1a6163b (pushed). It took 7 judges under the OLD judge: run 1 (logs/gates7-commit19-run1.log)
  attempts 1-4 PRE-PUSH GREEN then lost the CAS; attempt 5 NOT JUDGED (the bench-worstcut control timed out twice past
  600 s while hand jobs ran: a `lean logs/protocol19-StaleOnly.lean` at ~1170% CPU / 19 GB and wt/lang's own
  bench-worstcut). Run 2 (logs/gates8-commit19.log, pid file gates8-commit19.pid) attempt 1 GREEN lost to PERF-3 +
  HOSTING-35 (both landed during ROOT's first, time-boxed hold); attempt 2 landed in the unconditional empty window.
  5 GREEN judges thrown away + 1 killed by load, for one commit.
- Standing 1a6163beb767 GREEN (pinned 58). 59 -> 58 traced to 3467955 (KERNEL, ROOT-ruled): nine per-thing hash rows
  traded for eight *-per-required rows (hashes-per-nullifier folded into the admission share); stated in its WASTE lines.
  Observation sent to ROOT: per-required rows are exact against Kernel.Sim.Required, which moves with the kernel
  (KERNEL-23 2263 lowers insertReq with it), so a costlier DESIGN reads 1.000; absolute cost is held by worstcut/bar only.
- Agreed KERNEL-23 2263 waste.tsv part (logs/kernel23-2263.patch md5 9bc8cd6a): 8 lines, op/metric/ceiling/measured
  byte-identical, source prose only.
- Slot-wait bug (c): fixed in wt/gates scripts/gate-lib.sh (unlanded as written): all-busy => retry every slot each 5 s
  for 30 min, take the first freed. Plant logs/gates8-slotplant.sh (3 slots held, release one other than pid mod 3):
  main's lib `did NOT take the freed slot 3` after 15 s; new `took the freed slot 2`.
- GATES-20 measurement: logs/gates8-trace.py runs the tree's own runs.py --standing with each run under
  `strace -f --seccomp-bpf -e trace=%file,execve` (traces in logs/gates8-traces, one per run incl. controls) on the
  standing tree at 1a6163b, under the standing lock; logs/gates8-replay.py replays main's last 150 landings.
  Trace %file, not only openat: cargo's fingerprint STATs sources without opening them, and a failed probe (ENOENT)
  is a read of absence.
- FAIL-OPEN found by the traces, fixed as GATES-20a = 6527d9f (landed pass 3: displaced twice by c0cd535/1e90c0b, then
  head: the age bound working; its first launch refused after waiting 30 min on ONE slot, the bug it fixes). store-plants
  ({host}) and rows (`lake exe lang-journey`) were selected by their own closure only: 10/150 landings pre-push GREEN
  without the run (standing the backstop); resident rows ran hosting-residents undeclared. Fix: runs.reach (IO.Process in
  closure => every exe), lean_bin drives check + second-door check, runs.tsv drives, static key holds doc/.lean NAMES
  (devtools:workspace stats decisions/), KEY_VERSION v2, slot fix. Plants logs/gates8-selplant.py (6 missed under main,
  6 caught under 20a, edit control ok both), logs/gates8-slotplant.sh. Decision GATES-20a in decisions/gates.md.
- Standing 6527d9f146e0 GREEN (pinned 58).
- GATES-20 design: redregg/work/GATES-20-DESIGN.md. Replay logs/gates8-replay2.py/.out: selection 2994 -> 1672,
  reuse 10.4% -> 53.4%, 512 re-runs = binary-closure floor. ROOT: F1 = trace in EVERY judge; F2 = standing REPORTS
  outside-tree reads with a census (tempdirs vs real, per row), RED is GATES-20b with a dated trigger "census sorted";
  fail-closed fallback + standing re-trace RED on any difference both required; numbers go in the decision.
- BUILD NOTES for GATES-20 (draft gates/trace.py in my Mac scratchpad, copied to hbox logs/gates8-trace-lib.py):
  (1) a STAT must be content-keyed like an open: cargo's fingerprint compares mtime/size, so a stat'ed source is a
  content proxy (design §2's mode-only M was unsound; T = touched by name, keyed by bytes). (2) cargo reads C vs stats
  depending on its cache, so the re-trace check is fresh ⊆ recorded under an equal key, not equality. (3) selection
  needs validity on the PARENT, which is not built at selection time: validate git-tracked T/L components on $G/base disk
  + no .lean of reach changed in diff(S,B); X and .lake paths only enter the reuse key (C0 vs C1, both built).
  (4) pre-push runs the CANDIDATE's runs.py (judge_runs copies $G/tree/gates/*.py): asked ROOT whether selection and
  reading should come from J (main's) with only runs.tsv from the candidate.
- GATES-20 BUILD (wt/gates, uncommitted): gates/readset.py (new: wrap/reduce/union/key/touched_by/subset_violation/
  store), runs.py (TRACING; run() under strace; row_line/valid_readset/reach_of/traced_selected/added_or_deleted;
  main: --traces --git-dir --base --base-table --tree-oid; traced reuse `t:KEY` with the read-set in the payload;
  standing re-trace check over stored read-sets VALID on this tree (own key re-computed), fresh ⊆ stored else RED;
  `outside EXE:` report), rebase.py (traced_now: verify re-keys a `t:` unit from its payload), pre-push (runs.py and
  waste.py from $J; the candidate supplies runs.tsv only; --traces etc. on the candidate run; parent run static),
  standing.sh (--traces, `outside=N(traced|untraced)` in the line).
  Found while building: (1) relative names under a dirfd/chdir were mis-placed (bogus `2240469/ns`, `raw-dylibs`
  tree paths): fixed with `strace -y` (AT_FDCWD</cwd>, N</dir> annotations) + getdents64 for listings. (2) the
  re-trace check compared only records with key == the FRESH key, i.e. the key of the fresh read-set itself: vacuous
  (a differing read-set always has a different key). Now: every stored read-set whose own key re-computes equal on
  this tree. Plants: logs/gates8-g20plant.py (S1-S6 function-level over the real store), logs/gates8-g20e2e.sh
  (R1 evil runner, R2 traced reuse, R3 forge), logs/gates8-tr2.sh (two traced standing passes = plant 8 determinism
  + store), scratch store logs/gates8-store (v0 = the buggy reducer's, kept for comparison).
- ROOT ruling 10-20: the judge's CODE is main's; candidate supplies DATA only (runs.tsv, waste.tsv); a new row KIND and
  its first rows are two commits; plant: a candidate runs.py reporting ok changes no verdict. Built (pre-push: $J/runs.py
  + $J/waste.py; judge dir gets runs.tsv only). R1 `g20-evil-runner` RED: `runs: NEW RED run cargo:launcher:resident_bell`.
- HOST-61 (bd39f78) 4th pass answered: case 2 (tickets 21 and 22 both at two displacements; oldest first). Bound held.
- Selection plants S1-S6 all caught (logs/gates8-g20plant.py). Determinism: 24/25 rows fresh ⊆ stored on pass 2;
  host-file-sim RED on its own .lake/host-file-sim/run-<random> scratch -> readset excludes run-created (mkdir=0) dirs;
  re-measured clean (logs/gates8-hfs.sh). Replay as built (logs/gates8-replay3.py, store gates8-store-r3): selected
  3025 -> 1922, reuse 41.8% (design's 53.4% was the unsound mode-only-stat figure), floor 804 binary-closure.
- Outside census (F2): ~/.cache/nd-t 472 (test temps), PATH/LD_LIBRARY_PATH probes (hacl-star, HOL, r05, solana),
  ~/.nd-bar + ~/ndbar.* (bar scratch), /tmp/nd-attach-*; REAL inputs no key covers: ~/.gitconfig, ~/.config/git,
  ~/.lake/config.toml. GATES-20b (RED) dated 2026-10-27, first item: those three (key them or HOME=fresh).
- STAGED, NOT YET IN wt/gates (logs/readset-next.py; copy to wt/gates/gates/readset.py once gates8-g20e2e finishes):
  toolchain classification fix (".cargo" w/o slash), and the traced key now holds rustc -Vv / cargo -V / python
  version (the first traced key had none: a rustc upgrade would have carried a cargo verdict). Because the key
  function changes, re-run R2+R3 of logs/gates8-g20e2e.sh after installing it (sed out R1 or keep it).
- Decision draft: Mac scratchpad dec20.md (also copy at hbox logs/gates8-dec20.md once uploaded); placeholders
  R2_LINE / R3_LINE to fill from logs/gates8-g20e2e.out. Commit paths: gates/readset.py gates/runs.py gates/rebase.py
  scripts/pre-push scripts/standing.sh decisions/gates.md. Under the OLD judge this commit is judged by its own
  runs.py (the last time): say so in the message.

### GATES-8 continuation for GATES-9 (written at GATES-8's context ceiling, 2026-10-19)
STATE: main has GATES-19 (1a6163b) and GATES-20a (6527d9f); standing on both GREEN. GATES-20 is BUILT in hbox wt/gates,
UNCOMMITTED: gates/readset.py (new), gates/runs.py, gates/rebase.py, scripts/pre-push, scripts/standing.sh,
decisions/gates.md (it holds only GATES-19's "measured first day" paragraph so far; GATES-20's decision draft is at
hbox logs/gates8-dec20.md, an OLDER copy: the Mac scratchpad has the final one, so fill it from this log: R2 =
`PLANT g20-data GREEN (control)`, reused 24 / re-run 2 (census and cargo:devtools:workspace, which lists world/ and saw
the added path) where GATES-19's static key re-ran every row; R3 = see logs/gates8-g20e2e-b.out). Planted: S1-S6
(logs/gates8-g20plant.py), R1 evil runner RED, R2 reuse, R3 forge (rerun with the final readset.py: logs/gates8-g20e2e-b.*),
determinism (logs/gates8-tr2*, gates8-hfs*). NOT in a judge.
ORDER (ROOT): FIRST the silent-revert fix (outranks GATES-20), THEN land GATES-20.
1. SILENT REVERT (ROOT via HOSTING-13): scripts/commit's re-base re-reads a touched PATH from the lane's WORKING TREE.
   HOSTING-13's worktree sat at a1ca640 while CLIENT-31 (cdc0e9a) added 70 lines to launcher/tests/members.rs; attempt 5
   would have landed the stale copy. Where to look: main scripts/commit lines 101-131. The merge runs only when
   `git diff HEAD $base -- PATHS` is non-empty, with base = HEAD's copy (rebase.py merge --head HEAD --main $base
   --bases $ND_LANDER_DIR/merged.tsv), and then `git add -A -- PATHS` takes the WORKING copy. Suspected gaps (UNVERIFIED by
   GATES-8): (a) between attempts the working copy is re-read whole; a lane editing it mid-judge, or a HEAD moved by
   `checkout --detach main` under a stale working file, makes HEAD==main for that path, so `behind` is empty and the
   stale working copy is taken whole; (b) merged.tsv records the base only for files merged on an earlier attempt.
   ROOT's rule: for EVERY touched path take the 3-way merge (lane's RECORDED base blob, working copy, main's blob); main
   wins where the working copy equals the lane's base; conflict refused by name; refuse `stale path: P` when the landed
   path would reduce to the lane's copy while main changed it. Plant: a path edited on main after the lane's base with
   a stale working copy lands as main + the lane's hunk. The decision says how GATES-19's merge missed it.
   Fold in LANG-21 (c1166ce): its attempt 2 GAVE UP after 5 CAS displacements while "head regardless"; the outer
   COMMIT_RETRIES=5 give-up (scripts/commit line 45-56) predates GATES-19 and must not count tie displacements against a
   head lander (it waits for the tie winners, it does not fail). Read logs/lang21-commit*.log first.
2. Then land GATES-20: scripts/commit -F <msg> gates/readset.py gates/runs.py gates/rebase.py scripts/pre-push
   scripts/standing.sh decisions/gates.md (append dec20 + fill R2/R3). Say: this is the LAST runs.py change judged by its
   own runner (the old pre-push copies the candidate's gates/*.py). After landing: standing, quote it, check the line
   carries `outside=N(traced)` and no re-trace RED; tell lanes (via ROOT) a new row KIND is now two commits.
3. GATES-20b dated 2026-10-27: outside reads -> RED; first the three real inputs (~/.gitconfig, ~/.config/git,
   ~/.lake/config.toml). GATES-21 merge-train PROPOSED: redregg/work/GATES-21-PROPOSED.md, build only if the tie tail
   stays long under GATES-20 (measure a day of `queue: head (displaced N)` lines).
Scratch (mine, deletable): logs/gates8-*, logs/readset*.py, logs/patch20-*.py, wt store logs/gates8-store*,
main/.git/nanodregg-plant/g20-*, main/.git/nanodregg-traces (populated by the plants: content-addressed, valid-by-key,
harmless; keep it as the seed store or clear it).
- UPDATE: R3 read `PLANT g20-forge RED: stale verdict: run:cargo:devtools:workspace (recorded key t:355e479e…, now
  t:1823186b…)`. hbox logs/gates8-dec20.md is now the FINAL GATES-20 decision text (R2/R3 filled): append it to
  decisions/gates.md in wt/gates before committing. Every GATES-20 plant is done; only the commit and landing remain.

## GATES-9 (2026-10-21, successor of GATES-8)
- Saved GATES-20's uncommitted wt/gates diff BEFORE touching it: hbox logs/gates9-saved-20.patch (md5 d9e37572…),
  whole files in logs/gates9-saved-20/ (BASE = 6527d9f), readset.py also logs/gates9-saved-20-readset.py (== readset-next.py).
  wt/gates then reset to main for GATES-20b.
- SILENT REVERT VERIFIED (logs/gates9-verify.sh; main's judge, stub pre-push, scratch worktree wt/gates9-plant): merge ran
  only where HEAD's copy != main's (base = HEAD), then `git add -A` the working copy. V1 (a1ca640 copy + lane line, HEAD ==
  main) and V2 (`git reset main` under an edited file): candidate 1003 lines, CLIENT-31's 70 gone. V0 (HEAD at real base)
  merges. HOSTING-39 itself was safe (its HEAD stayed at a1ca640).
- GATES-20b BUILT: rebase.py snapshot/candidate/stale/writeback (merge + merged.tsv deleted), land.py --charge (CAS-refused
  counts as a displacement), scripts/commit (record at first attempt; stale on the final candidate; --reverts C; outer loop
  charges only non-head displacements). ROOT ruled: 300-commit window (oldest live worktree base 297 behind), --reverts needs
  C's owner named in CROSS-LAYER, REVERTS: hunk into the message, refusal prints the exact addition; replay cost 14/150
  landings accepted ("say what you broke" at the gate). Plants: logs/gates9-plants.sh (-old/-new.out), gates9-wb.sh,
  gates9-loop.sh (+ -budget2), gates9-stale-replay.py/.out, gates9-hunks.out. Decision text logs/dec20b.md, msg logs/msg20b.txt.
- Landing launched 06:13 hbox: log logs/gates9-commit20b.log; judge pid 1698517 in logs/gates9-commit20b.judge.pid
  (gates9-commit20b.pid holds the WRAPPER subshell: I backgrounded `cd && L= && nohup …` as one list; HOSTING-13's lesson, repeated).
- GATES-20b LANDED 8c2c5fd (attempt 3: displaced twice, head, CAS; all three judges GREEN under main's old judge). Standing
  8c2c5fdef123 GREEN (pinned 60). Agreed KERNEL-23 cv 01a15107-2281 waste.tsv (patch md5 6c091a5f: admit trie-hashes-per-turn
  14.074 -> 13.754, others prose only).
- GATES-20 re-applied --3way (clean) on 8c2c5fd; decision logs/gates9-dec20.md (outside-reads RED renumbered GATES-20c,
  dated 2026-10-27); msg logs/gates9-msg20.txt; landing launched, judge pid 2720254 (logs/gates9-commit20.pid, a correct
  PID this time), log logs/gates9-commit20.log.
- GATES-20 LANDED 145283a (attempt 4: charged 2, one free tie). STANDING 145283aa3e71 RED: re-trace on 13/14 cargo rows,
  all extras = dirs + rustc absent `mod` probes (warm judge records vs a compiling standing). ROOT ruled GATES-20d (C =
  compile reads by rustc pids incl. clones; C compared only vs a compiled record; implied ancestor dirs; escaped name =>
  trace invalid, `untraced EXE`, standing INCOMPLETE). Plants logs/gates9-20d.sh/-check.out/-forge.out. Launched pid 139516,
  log logs/gates9-commit20d.log. OWED: GATES-20c dated 2026-10-27 = (1) outside reads RED (~/.gitconfig, ~/.config/git,
  ~/.lake/config.toml), (2) the warm-cargo mod-probe blind spot ((a) daily cold compile, (b) probe paths from every stored C).
  GATES-21 stays PROPOSED: measure `queue: head (displaced N)` + `not charged` lines over a day.
- GATES-20d LANDED be8ee18. STANDING be8ee181df91 GREEN (pinned 63, untraced=0) — re-trace VACUOUS this pass (key v2:
  no v1 record re-keys; seeding). PERF-4's fail-open (waste.tsv is a JUDGE input no trace holds; 41e041f's bench rows
  NOT RUN while their ceilings moved) -> GATES-20e (W = waste rows a row measured; selection + key v3; orphan rule).
  Plants logs/gates9-20e.py/.out (main: bench not selected; new: selected). Launched pid 325798, log gates9-commit20e.log.
  Told HOST-17 YES on rowbar 1.017 -> 1.064 (needs `WASTE: rowbar: …` in the message).
- GATES-20e LANDED c8ebb06 (attempt 3; its first launch refused by a HOSTING isolation stderr-interleave flake, fixed by
  HOSTING-14 in 2e84396). Bench trace cost measured: 799 traced syscalls per bench-worstcut run (seccomp-bpf), so the
  tracer is NOT why the bench crosses 600 s; routed to ROOT/PERF (bench size vs deadline). KERNEL-24's reds: devtools ok
  (control output), bench UNREAD x2 = NOT JUDGED, the red was SIZE lines. Agreed K23 e096 waste.tsv (prose only).
- GATES-20f built (reap_dead in scripts/commit; plant logs/gates9-reap.sh/.out) and launched pid 1792571; standing c8ebb06
  pid 1792561 (seeding pass, key v3).

## GATES-10 (2026-10-21, successor of GATES-9)
- 20fg LANDED fc4022d (attempt 1, head, displaced 0). PROTOCOL-22 told. STANDING c8ebb067f057 GREEN (SEEDING pass, key v3; ~33 min).
  Standing fc4022d launched: pid file logs/gates10-standing-fc4022d.pid (2148866), log logs/gates10-standing-fc4022d.log,
  start epoch in logs/gates10-standing-fc4022d.start (the 20g "before" wall). First REAL re-trace comparison under v3.
- 20g DRAFTED, PARKED (ROOT: 20b′ then 20h outrank it): local scratchpad g10/ (patch_runs.py, patch_readset.py, patch_sh.py;
  applied copies in g10/gates, g10/scripts). Design: rows concurrent up to N = slot_count; own slot/standing lock = 1 row, extra
  rows BORROW free nanodregg-gate-K.flock non-blocking, never while a lander waits (gate_slot writes nanodregg-slot-wait/<pid>);
  standing holds ≤ N-1 judge slots. readset S = scratch roots written (.lake/X, tree path, tmp:/tmp/X, home:X); any two rows
  whose roots overlap = `run concurrency A + B: RED(shared scratch …)`; a row run beside others with no read-set is re-run
  ALONE. Untraced (parent judge) = sequential. Not yet planted/measured.
- GATES-20b′ (PERF-6's stale false positive): lacks() = merge clean AND changes X AND NOT holds(X) (every added block present
  contiguously, removed blocks absent). Plants logs/gates10-lacks-plant.sh/.out: P9 PERF-12 lakefile main=stale, new=passes;
  GATES-9 P1/P2/P7 still refused. Landing pid file logs/gates10-commit20bp.pid, log logs/gates10-commit20bp.log.
- GATES-21 data so far (all logs/*.log, ~307 landing logs): `queue: head (displaced 2)` 13, `(displaced 0)` 10, `(1)` 7,
  `(3)` 3, `(4)` 3; `not charged … a tie` 8 (5 at 2 before, 3 at 3 before).
- STANDING fc4022db3447 GREEN, the FIRST REAL re-trace comparison under v3 (c8ebb06 was seeding); wall 41 min (20g "before").
- 20h MEASURED (logs/gates10-fluid-measure.py + .out variants; replay of the 24 h queue: 57 landed, 27 displaced, 61 re-judges):
  skip-as-specified 0/61 (30 judge change = mostly gates/*.tsv data; 19 cargo:devtools:workspace; 4 attach; 7 flag day);
  code-only judge change 0/61; + stat-by-kind (approx) 5/61. ROOT ruled: HOLD the skip, land ONE 20h = (a)+(b)+(c); if the
  replay is still < 1/3, GATES-21 (merge train) goes PROPOSED -> BUILT.
- Built 20h SKIP (held, not landed): scratch worktree wt/gates10 (fc4022d + 20b′ + rebase.py fluid/attribute, pre-push
  --gates-only, scripts/commit fluid branch + judged/judged.new + record.*.rows, runs.py --selected, standing ATTRIBUTION).
  Plants logs/gates10-fluid-plant.sh (shared scratch clone, real outer loop, stub pre-push) -> -new.out: S1 disjoint lands
  with calls `full gates-only` + FLUID line; S2 traced path / S3 module in reach / S4 `!` / S5 gates change / S6 no rows all
  `full full` naming why.
- KERNEL-26's three upward waste re-pins at KERNEL-58: AGREED (sent).
- HOSTING-15 fence: rule built + planted (logs/gates10-fence-plant.sh/.out; local g10/fence/runs.py, patch g10/patch_fence.py):
  `skipped: ` line on a cargo run => INCOMPLETE(skipped: N, first: …) (main's runner reads it ok: the fail-open shape);
  row kind `cargo-untraced:CRATE:TEST` runs without strace (MEASURED: strace --seccomp-bpf sets no_new_privs, `sudo -n -u nd
  true` exit 0 plain / 1 traced). HOSTING adds `cargo-untraced:launcher:fence` after my hash (needs OPS-6 UMask 0027 first).
  Blocking-on-skip (RED on the landing clone) is ROOT's call; default INCOMPLETE (pending).

### CONTINUATION for GATES-11: 20h proper = (a) + (b) + (c), ROOT's ruling, design worked out, NOT built
(a) readset.reduce: a pid set CARGO (exec of basename `cargo`, clones inherit; an execve of anything not cargo/rustc
    REMOVES the pid: the test binary cargo spawns is not cargo). Stat-like calls (stat lstat newfstatat statx access
    faccessat faccessat2 readlink readlinkat) by a pid in neither CARGO nor comp go to a new set K, keyed by KIND
    (DIR/FILE/ABSENT/OTHER via os.stat) not bytes; K -= T at the end. key(): put("K "+p+" "+kind); VERSION -> v4 (next
    standing is SEEDING again). touched_by: p in T∪C, OR p in K and p in added_or_deleted. subset_violation: fresh K ⊆ rec
    K∪T∪C; a fresh T path the record had only in K IS an extra. Plants: a tree walk (devtools:workspace) keyed by kind does
    not re-run on a content-only edit of a walked file; a Cargo.toml edit still re-runs it (opened, T); a cargo fingerprint
    stat (cargo pid) still keys content.
(b) fluid/plan: judge change = gates/*.py + scripts/ only. gates/runs.tsv: a selected row whose row LINE differs B0 vs M
    intersects. gates/waste.tsv: a selected row whose W rows changed intersects (readset.waste_changed). Any other gates/*.tsv
    on one side + a .lean on the other: census re-runs.
(c) `rebase.py plan` replaces `fluid` (zero-row case = today's skip): writes PLAN = build all|exes E…|none, census run|carry,
    cargo run|carry, generated <outs>|none, rows <intersecting>. build all + census run iff NOT build-disjoint (importer
    rule already in fluid) or a non-module build input moved; else build only the intersecting rows' exes (lake build E…).
    pre-push --plan FILE: gates always; build/census/cargo/generated per plan; runs.py --only ROWS --carry record.prev
    (carried rows printed `ok (carried: FLUID …)` and written to record.new how=`carried`; selected = only ∪ carried).
    rebase.verify accepts how=carried WITHOUT a key re-check (the approved weakening; say so in the decision). After a
    partial re-judge: judged.new base = M. Zero rows + nothing to build => --gates-only (no slot), as built. Message line
    `FLUID: judged on B0 … re-ran rows R… carried …`; standing ATTRIBUTION as built.
    Plants: the six S1–S6 + (a)'s three + (c): an intersecting re-base runs exactly the intersecting rows (real pre-push
    --plan on an index candidate in a slot, no landing), a build-reaching delta still builds all + census.
    Then re-run logs/gates10-fluid-measure.py with the plan rules (count zero-row skips AND partials) and send ROOT the number;
    < 1/3 => build GATES-21.
- 20b′ attempt chain 1 (pid 2167762): displaced twice (fc4022d->5325ab5->ececba1), then REFUSED `gate: every judge slot busy
  for 30 min; refusing` (gate_slot exit 2 -> "REFUSED by scripts/pre-push"). OPEN ITEM: a slot timeout is NOT a verdict; it
  should exit 76 (NOT JUDGED), not read as a refusal. Relaunched pid file logs/gates10-commit20bp-2.pid, log -2.log.
- Fence rule: ROOT ruled pre-push skip = INCOMPLETE named in the verdict line `(pending: …)`, standing skip = RED. Patches
  logs/patch_fence.py (runs.py) + logs/patch_fence_sh.py (pre-push); apply to wt/gates after 20b′ lands, commit `gates:
  GATES-20j`; message HOSTING-16 (a4976f6a42319a0a4) the hash. HOST-20 codec-vectors.tsv AGREED (verified comm -3: 2 out, 6 in).
  HOST-20 (a49735f6091ae518b) also waits for 20b′'s hash.

### CONTINUATION for GATES-11 (written by GATES-10 at its budget; supersedes the 20h continuation above in PRIORITY)
EMBER RULED (via ROOT): converge periodically, not judge every landing. GATES-21 (merge train) and 20i (batch) -> NOT NEEDED
(say so in the decision). 20h/20g are SUPERSEDED in priority by GATES-22; their material stays useful (below).
GATES-22 THE FAST LANDING + CONVERGENCE (ROOT's text, condensed):
 (1) scripts/commit default path: rebase from the recorded copy (20b + 20b′ stale guard stay), cheap gates only (owners,
     closure, size, secrets, stale-path, message format = check.py + parent check.py: pre-push --gates-only as built in
     wt/gates10 is most of it), `lake build` of ONLY the libraries the diff reaches (tree.dependents of changed modules,
     their lean_lib/exe targets) + cargo check of a touched crate, then land. No rows, benches, census, standing rows, no
     queue ticket/CAS dance beyond plain rebase-and-retry (keep update-ref CAS; drop land.py's head/age logic).
 (2) CONVERGENCE = scripts/standing.sh on a SCHEDULE (every 3 h while lanes land; `converge now` by ROOT/Ember), one at a
     time box-wide (its lock), labelled with the commit range since the last GREEN. A RED names the commits in the range
     whose read-sets intersect the red row: rebase.py attribute (built in wt/gates10, FLUID-line based) generalizes to: for the
     red row's stored read-set (newest valid), list range commits whose diff touched_by(rs) / reach. ROOT routes; a red unfixed
     by the next convergence is reverted with --reverts C naming the owner.
 (3) FULL judge (today's pre-push) ONLY for `!` subjects and gates/ + scripts/ changes (self-judge rule).
 (4) Per convergence print: landings since last green, reds found, time-to-fix. The before: 61 re-judges/24 h for 57
     landings (logs/gates10-fluid-measure.out), plus 41 min standing wall, plus 20b′'s own landing: ~2.5 h through the queue
     with two displacements and one 30-min slot-starvation refusal.
 Plants: fast landing breaking a reached library refused at build; fast landing breaking an unreached row caught by the next
 convergence and attributed by read-set; a `!` commit still gets the full judge.
MATERIAL ON DISK: wt/gates10 (scratch worktree at fc4022d+20b′+20h skip: pre-push --gates-only, rebase.py fluid/attribute,
 runs.py --selected, scripts/commit fluid branch) — reuse --gates-only and attribute; logs/gates10-fluid-plant.sh is a working
 harness for the real outer loop in a shared scratch clone with a stub pre-push (adapt for the fast-path plants).
 20g draft (concurrent rows) also copied to hbox logs/gates10-20g-draft/ (patch_runs.py, patch_readset.py, patch_sh.py; apply to the 20fg runs.py/readset.py/scripts); originals 
 7c10f132-0e99-4487-aaaa-62ea34c9f1c0/scratchpad/g10/{patch_runs.py,patch_readset.py,patch_sh.py} — copy them to hbox logs/
 if wanted: under GATES-22 convergence is the only full run, so 20g (41 min -> ~N-way parallel) is worth landing NEXT.
FENCE RULE (GATES-20j, owed to HOSTING-16 a4976f6a42319a0a4): patches hbox logs/patch_fence.py (runs.py) and
 logs/patch_fence_sh.py (pre-push), planted (logs/gates10-fence-plant.sh/.out). Apply in wt/gates, decision text, land
 (it is gates/: full judge), message HOSTING-16 the hash. Under GATES-22 the row runs only at convergence (standing: skip =
 RED, ROOT's ruling) — say so.
OPEN: a slot wait past 30 min should be NOT JUDGED (76), not a refusal (gate_slot exit 2 -> "REFUSED by pre-push").

## GATES-11 (2026-10-21, successor of GATES-10) — GATES-22 the fast landing + convergence
- Worktree hbox wt/gates11 (GATES-10 still on wt/gates with 20b′; rebase.py untouched by 22). Local drafts:
  scratchpad g11/new/{gates/fast.py,gates/converge.py,gates/land.py,gates/readset.py,scripts/{commit,pre-push,standing.sh,gate-lib.sh,converge}}, decision g11/dec22.md.
- Built: gates/fast.py (mode/targets/crates), pre-push --fast, scripts/commit fast default (no ticket; FAST_RETRIES 12;
  land.py --fast yields to a twice-displaced full lander ≤60 min; `JUDGED: fast` message line), standing.sh cargo= and
  generated= stages + per-sha runs.out, gates/converge.py (record: range since last GREEN, units, attribution by read-set,
  owner, FIXED time-to-fix, revert rule; owners), scripts/converge (lock, wt/converge reset+re-exec, timer --install,
  --revert C), readset K (20h (a), key v4), gate_slot timeout -> NOT JUDGED 76.
- Plants: logs/gates11-fast-plant.sh/-new.out (F1–F6 lander side), logs/gates11-yield.out (land.py --fast),
  logs/gates11-converge-plant.sh/-new.out (C0–C3: attribution by real read-set store, revert lands, FIXED),
  logs/gates11-fast-judge-plant.sh/.out (real pre-push --fast in a slot: P0 doc, P1 leaf type error, P2 crate error, P3 leaf green).
- GATES-20b′ LANDED a108b15 (attempt chain 2: displaced 3 times, head; ~2.5 h end to end incl. the starved chain 1). PERF-6,
  HOST-20, ROOT told. No standing on it (rebase.py only, no row reads it; GATES-22 replaces per-landing standing).
- Agreed: ROOT-DOCS path rewrite in decisions/gates.md; `docs/` appended to gates/doc-allow.tsv (no reader; rebase.check holds it).
- SLOT CLEANUP (logs/gates10-slot-cleanup.sh/.out): standing 200 dirs, 294 MiB freed. gate-1..4 NOT DONE: every judge slot
  stayed held for the whole 45-min window (19:12 EDT). OWED to GATES-11: re-run `bash logs/gates10-slot-cleanup.sh` when the
  slots free (it takes each slot's own flock, deletes only {iso,isob,isom}-<pid>-<name> dirs older than the newest running
  judge's start; measured 2.5G/737M/205M/53M at 15:20). Its slot-hold is itself a GATES-22 before-number.
GATES-10 STOPS HERE (budget). Live processes of mine: none.
- ROOT reordered: 20j (fence) FIRST. Applied GATES-10's patches in wt/gates (now mine), plant logs/gates11-fence-plant.sh/.out
  (+ a --standing case: skip reads RED). Landing 1 (pid file logs/gates11-commit20j.pid): GREEN, displaced, GREEN, displaced,
  then REFUSED by the old 30-min slot wait (~2 h). Relaunched: logs/gates11-commit20j-2.{pid,log}. HOSTING-16 (a4976f6a42319a0a4)
  waits for its hash (it adds the cargo-untraced:launcher:fence row itself, "GATES-11 agreed").
- ROOT's lane adds folded into 22: (a) source gates before any slot (pre-push pre-lint on a private copy), (d) docs-only = no-slot
  fast path, (f) keep place (gate_slot waits 4 h, names holders every 30 min), (b) decisions/*.md append-only merge in
  rebase.py candidate (plant logs/gates11-append-plant.out). (e) flake retry = its own commit after 22. (c) = the fast path itself.
- Judge plants v3 logs/gates11-fast-judge-plant3.sh/.out: P0 doc 21 s no slot; P4 missing SIZE lines RED before slot in 18 s;
  P1 leaf type error build RED (Codec only; waited ~45 min for a slot, holders printed); P2 crate error cargo-check RED (4 pkgs).
- To land 22 after 20j: run logs/rebase22.sh equivalent (scratch g11/rebase22.sh: 3-way merge my files onto main in wt/gates11,
  append g11/dec22.md), then scripts/commit -F msg22.txt from wt/gates11 with the 11 paths.
- LATE FINDING (KERNEL-26, verified): the GATES-20 tracer itself fails intermittently: `/usr/bin/strace: ptrace(PTRACE_LISTEN,pid:N,
  sig:0): Input/output error` -> the run exits 1 -> runs.py reads RED (main.git nanodregg-gate-2/4c04f20aa738.log
  cargo:launcher:resident; gate-3/2b29a0426731.log cargo:launcher:broker, 10-21 ~19:15). Fails CLOSED (false refusal). OWED
  (GATES-11, before or with GATES-22's convergence, since standing would read it RED too): in runs.run, output holding
  `strace: ptrace(` (a tracer failure) => UNREAD(tracer: LINE), re-run once like a timeout; twice => NOT JUDGED (76), never RED;
  the trace of that run is discarded. Plant: a wrapper that makes strace exit with that line reads UNREAD, not RED.
- GATES-22 LANDED e568634 (attempt 2 launch: GREEN, displaced, GREEN, displaced, head-landed; launch 1 refused by the
  rebase.py doc-allow literal gate -> gates/append-only.tsv). Timer nanodregg-converge.timer installed (every 3 h at :17).
  First convergence on 0b86cb067bec: logs/gates11-converge1.{log,pid} (seeding key v4).
- 20j relaunched (logs/gates11-commit20j-3.*; attempts 1 and 2 were both refused by the OLD 30-min slot wait after GREEN judges).
- GATES-20k (tracer flake: UNREAD(tracer), retry once, twice NOT JUDGED, `flake` lines, flakes=N) launched from wt/gates11:
  logs/gates11-commit20k.{pid,log}; plant logs/gates11-tracer-plant{,-new}.out.
- OWED after: tell HOSTING-16 (a4976f6a42319a0a4) 20j's hash; each convergence verdict to ROOT; 20g (concurrent standing
  rows; draft hbox logs/gates10-20g-draft/); slot cleanup re-run (logs/gates10-slot-cleanup.sh; ~3.5 G in gate-1..4 tmp).
- FIRST CONVERGENCE 0b86cb067bec GREEN (range fc4022db3447..0b86cb067bec, 17 landings, 46 min; seeding key v4). ROOT told.
- GATES-22 fix LANDED 2a0de84 (scripts/commit:119 `${ND_TICKET:-/dev/null}`; KERNEL-28's crash; plant logs/gates11-fastfix-plant.out).
  My 22 plants PRINTED the unbound line and my summary grep missed it: grep plant logs for `unbound|No such file|Traceback`.
  KERNEL-28 (ac5a6433f2fea8b56) told.
- 20j attempt 3 refused: decisions/gates.md conflict (b50da06 edited above the end; 22's append rule needed both sides pure
  appends). Fix GATES-22 (b) fix (lander-only append) launched from wt/gates11b: logs/gates11-commit22b.{pid,log}; plant
  logs/gates11-append2-plant.out. 20j re-applied on main and relaunched from wt/gates: logs/gates11-commit20j-4.{pid,log}.
- 20k (tracer) in flight from wt/gates11: logs/gates11-commit20k.{pid,log}.

### CONTINUATION for GATES-12 (written by GATES-11 at ~420K)
IN FLIGHT (read each log's last `scripts/commit:` line; relaunch from the same worktree if REFUSED by a slot wait or a
decisions/ conflict, re-applying on main as for 20j: patches logs/patch_fence.py + patch_fence_sh.py + logs/dec20j.md;
logs/patch_tracer.py + patch_tracer_sh.py + logs/dec20k.md; logs/patch_append2.py + logs/dec22b.md):
  20j  wt/gates    logs/gates11-commit20j-4   -> on landing: message HOSTING-16 (a4976f6a42319a0a4) the hash (it adds
       `cargo-untraced:launcher:fence<TAB>host,hosting-broker,hosting-residents<TAB>exit 0<TAB>nobin RED` itself).
  20k  wt/gates11  logs/gates11-commit20k     (tracer flake; standing flakes=N)
  22b  wt/gates11b logs/gates11-commit22b     (lander-only append)
CONVERGENCE: timer nanodregg-converge.timer (systemctl --user list-timers), log <common>/nanodregg-standing/convergence.log and
  converge-timer.log; send ROOT each verdict line with its range and RED attribution. A REVERT lands by itself (wt/converge-revert).
  First real re-trace comparison under key v4 is the SECOND convergence: a RED `(re-trace)` there may be a K-set seeding
  artefact (stat-by-kind); read the extra paths before attributing.
NEXT: 20g (concurrent standing rows; draft hbox logs/gates10-20g-draft/ against the 20fg runs.py: re-base onto 22's runs.py/
  readset.py; convergence is now the only full run, 46 min wall). Slot cleanup: re-run logs/gates10-slot-cleanup.sh when
  slots are free (gate-1 tmp 2.5G, gate-2 737M, gate-3 205M, gate-4 53M at 10-21 18:40; both runs so far NOT DONE: busy).
OPEN: a FAST lander whose worktree is behind 22 runs the old outer loop (no fast budget, retries until it lands); fine.
  converge.py attribution of `build`/`census` is coarse (modules named in errors / every module change).
- 22b LANDED fa8fec3. 20j-4 and 20k still in flight at handoff.
- ROOT asks (Ember: why 46 min?): measured from convergence 1 (started 00:05 EDT; first row read-set stored 00:07:52;
  log closed 00:51:21): gates + full build + census + generated + cargo= ~3 min warm; the ROWS ~43 min serial on one slot.
  Per-row times cannot be read from the read-set store mtimes (other judges write it concurrently). OWED to GATES-12:
  (1) standing.sh prints a per-stage time line (gates, build, census, generated, cargo, runs, waste) and runs.py a
  per-row wall (`  time ROW: N s`) so each CONVERGENCE line carries `stages: …`; (2) 20g with measured before/after;
  (3) convergence skip by read-set: rows whose stored read-set (valid key on the last GREEN tree) the delta since the last
  GREEN does not touch carry that GREEN's verdict (the GATES-19/20 traced-key machinery already decides this per row);
  build/census skip when no module changed; a docs-only delta = minutes. A skipped row must still be re-run at least
  daily (the re-trace check is how a narrowed record is caught) — say so in the decision.
- 20k LANDED 94d5bb6. 20j-4 refused: merge conflict in gates/runs.py with 20k (both edit run()). Re-applied fence patches on
  94d5bb6 in wt/gates (20k's tracer check now keyed on `traced`, so a cargo-untraced row is never read as a tracer failure;
  tracer plant re-run green on the merged runs.py; the fence plant re-run was blocked by the standing lock, held by GATES-12's
  meas20g.sh). Relaunched: logs/gates11-commit20j-5.{pid,log}.
- HOSTING-16 asked GATES to carry `cargo-untraced:launcher:fence<TAB>host,hosting-broker,hosting-residents<TAB>exit 0<TAB>nobin RED`
  in 20j. It cannot ride in 20j: the candidate's runs.tsv is judged by MAIN's runner (GATES-20), which does not know the kind
  until 20j lands. After 20j lands it is a gates/runs.tsv data change = a FAST landing (no slot, seconds): GATES-12 or HOSTING
  lands it (`gates:` or `hosting:` prefix; runs.tsv is SHARED).

## GATES-12 (2026-10-20 hbox clock, successor of GATES-11) — 20g concurrent rows + 20l the carry
- 20k LANDED 94d5bb6 (GATES-11's launch; head, displaced 2x). ROOT told. 20j-4 REFUSED (merge conflict with 20k in runs.py
  run(): the tracer block vs the skipped block); GATES-11 relaunched it as logs/gates11-commit20j-5 (ROOT: wait on that pid).
  After 20j lands: the fence row as a one-line FAST data commit (ROOT's exact row), tell ROOT.
- Slot cleanup re-run (logs/gates12-slot-cleanup.{out,pid}): gate-2 736 MiB, gate-3 203 MiB freed; gate-1/gate-4 busy (retrying 45 min).
- 20g/20l drafts: hbox logs/g12/new/{gates,scripts} (base = main 94d5bb6 + 20j resolved = logs/g12/runs20j.py), patch scripts
  logs/g12/new/patch20g_{runs,readset,sh,standing,converge}.py (rep-style, re-apply on main after 20j lands), plant
  logs/g12/new/plant20g.sh (16 cases P1..P10, 5/5 runs all PASS; fake tree + real strace + fake common dir).
- MEASURED (logs/g12/meas.*): concurrent rows on the standing tree at 0b86cb0 (convergence 1's tree, 43 min serial rows):
  805 s wall (13.4 min), 15 rows on borrowed slots, waste ok 79/79 (counts unmoved by load). First model (S roots: first
  component under home/tmp) red 90 pairs: home:.cache (tests' ~/.cache/nd-t/<unique>, 7295 leaked dirs: not mine, ROOT) and
  /tmp/newroot,/tmp/oldroot (bwrap's pivot dirs INSIDE its own mount namespace). Remodelled: WR/O/RM/LD (own made dirs are
  roots, getdents-only listings), NS (mount-namespace rows run alone; scheduled alone after the first sighting), chdir/fchdir/
  child cwd tracked. Run 2 with the new model: logs/g12/meas2.*.
- Run 2 (learning, new model): 2157 s, 0 collisions, 12 NS rows found (re-run alone + neighbours). Run 3 (steady): 875 s
  (14.6 min; 16 concurrent rows ~558 s, critical path bench-worstcut-rows 436 s; 12 NS rows alone 317 s), waste 79/79 ok.
- Fail-open candidate (ROOT approved containment inside 20g): NS read-sets (sandbox-view paths) never narrow/reuse/carry;
  proper fix GATES-20m filed cv 01a15816-7439. ~/.cache/nd-t leak (7295 dirs) is CLIENT's; ROOT filed; do not delete.
- 20j LANDED 3120c94 (GATES-11's 20j-5). Fence row LANDED FAST 81e0507 (cross-layer HOSTING-16 agreed). ROOT told.
- Slot cleanup DONE: 3525 MiB freed (gate-1 2532, gate-2 736, gate-3 203, gate-4 52).
- 20g+20l landing launched from wt/gates11b at 81e0507: logs/gates12-commit20g.{pid,log} (pid 1274244, hand-written: the
  launch's `cd && nohup &` put the pid write in the wrong cwd). Message logs/g12/msg20g.txt, decision logs/g12/dec20g.md
  (appended in the worktree), plants logs/g12/new/plant-final.out + plant20l.out. If refused: re-apply the patch scripts
  logs/g12/new/patch20g_{runs,readset,sh,standing,converge}.py on main (rep-style) + append dec20g.md, relaunch.
- CONVERGENCE 81e0507f35cf GREEN (range 0b86cb0..81e0507, 11 landings, 52 min serial, old runner); fence row ran ok. ROOT told.
- 20g+20l LANDED 199e9e3 (attempt 3, head; landed files byte-identical to logs/g12/new/*). ROOT told.
- FINDING (PROTOCOL-23): 20k's TRACER `^strace: ` never matched the real line `…/usr/bin/strace: ptrace(…)` (argv[0], after
  libtest dots); its plant was a mirror. Fix `(?:^|/)strace: ` + decision note; plant logs/g12/plant20k2.sh over the 3 real
  lines; launched logs/gates12-commit20k2.{pid,log} from wt/gates11b at 199e9e3.
- OPEN: first 20g convergence (next timer slot): read TIMES/ROWS, NS rows alone, carried=0 expected (runner bytes moved).
