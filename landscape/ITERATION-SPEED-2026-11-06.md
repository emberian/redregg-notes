# Iteration speed, 2026-11-06

Ember asked: "are we caught up on wretchedly slow iteration times?" Not yet. This file has the
measurements, what was fixed, and what is left. The iteration lane (Claude Opus 5.5) wrote it,
with one helper lane for the Mac packages. Raw data is on bb2 under `/home/build/iterspeed/`:
`md-modules.tsv`, `bs-modules.tsv`, `md-table.md`, `bs-table.md`, `prof/`. The analysis script is
`bin/analyze.py`.

## How it was measured

- **Builds.** Cold builds on dregg-build2 (bb2) under `swarm-build`:
  - minidregg at f54c4205e, the umbrella targets (`scripts/pipeline/umbrella-targets`);
  - breadstuffs `metatheory` at 274f65a80, the lakefile defaultTargets.
- **Per-module wall time and peak RSS.** A fake `LEAN_SYSROOT` (`/home/build/iterspeed/sysroot-<v>`)
  holds a copy of `lake` and a `bin/lean` that runs the real lean under `/usr/bin/time` and logs
  `wall, maxrss, user, sys, rc` per module. The same wrapper limits how many lean processes run at
  once with flock slots; the slot count lives in a file, so it can be changed during a run.
- **Load.** LEAN_NUM_THREADS was 4. bb2's load rose to 60-90 after about 20:00 UTC (other lanes),
  so wall times after that are inflated. Peak RSS is not affected by load.
- **Stopped early.** At ember's word ("just fix") both builds were stopped before they finished.
  minidregg was stopped in its last module, TokenCensus, after 75+ minutes. breadstuffs was stopped
  after 2,115 of its modules. From then on, each fix was verified with one single-module check.
- **Profiles.** One module at a time, with `-Dprofiler=true -Dtrace.profiler=true`
  (`bin/tprof.sh`). The trace attributes kernel time to declarations. Caution: the profiler can
  blame the next command (a kernel check runs asynchronously and blocks the next `addDecl`). Read
  the `[Kernel] typechecking declarations [...]` line, not the command it is nested under.

## minidregg (1,403 modules measured, all but TokenCensus)

| measure | value |
|---|---|
| summed lean wall | 8,296 s |
| span to the last finished module | 2,550 s; TokenCensus then ran 75+ min and was stopped |
| top 20 modules' share of summed wall | 47% |
| max import depth | 93 (AxiomCensusResearch) |
| weighted critical path | 1,719 s: AxiomCensusResearch(412) <- Tower256SuccinctReceiptCodec(191) <- Tower256SuccinctHonestRun(933) <- Tower256FinalPolynomialCheck(72) <- ... |
| modules > 60 s / > 4 GiB / > 12 GiB | 16 / 27 / 3 |

By peak RSS:

| # | module | peak GiB | wall s | cause (profile) | owner |
|---:|---|---:|---:|---|---|
| 1 | Kernel.ObjectLaw | 16.5 | 70 | `sumEq_and_hashEq_meaning_decides`: `decide +kernel` evaluates the deployed hash (`digestWith deployed`) in the kernel; 81 s kernel | free |
| 2 | Kernel.ResourceBirthController | 13.1 | 62 | `authorityWrites_postLaw`: 60 s, 14 GB of kernel check. Bisected: the `have decoded : decode (authorityWrite post).canonicalPostBytes = some ...`, `unfold PhysicalPostLaw` and `rw` steps alone cost 71 s with the final step replaced by `sorry`. Each `rfl` alone is 3 s | free (unfixed) |
| 3 | Compiler.Tower256FinalPolynomialCheck | 12.3 | 72 | not profiled | Tower256 lane |
| 4 | Assurance.DeployedCredentialLifecycle | 11.6 | 53 | `decide` over concrete policy states (lines 114-135) | free |
| 5 | Compiler.StoreCodecBook | 9.4 | 77 | not profiled | free |
| 6 | Kernel.EffectsRevival.HostTeethProofs | 8.3 | 35 | `ratchet_moves`: `decide +kernel` over one cSHAKE256 step (deliberate, documented) | free |
| 7 | AxiomCensusResearch | 8.0 | 412 | whole-tree import (~8 GB) plus `#assert_axioms_tree` over 197,569 constants | free |
| 8 | Minidregg (umbrella) | 8.0 | 6 | import only: the whole-tree olean floor | - |
| 9 | Assurance | 7.7 | 5 | import only | - |
| 10 | Theory.NockCost.Summaries | 7.3 | 73 | 11 `native_decide`s, each re-running `cue` of the 566 KB forge.jam in the interpreter: 6-8 s each, 76 s interpretation | free |
| 11 | Kernel.ProviderExecutionLease | 7.1 | 52 | two async kernel checks of 25 s each; the `#print axioms` waits on them | free |
| 12 | Assurance.DreggNetProviderConsumer | 7.1 | 54 | not profiled | free |
| 20 | Theory.NockCost | 5.6 | 54 | 12 `native_decide`s on forge, same cause, 65 s interpretation | free |

By wall time:

| # | module | wall s | peak GiB | cause | owner |
|---:|---|---:|---:|---|---|
| 1 | Compiler.Tower256SuccinctHonestRun | 934 | 3.3 | interpreted honest prover (#guard) | Tower256 lane |
| 2 | Compiler.EvmStage0NativeDeployment | 457 | 3.8 | 16 #guard/#eval, 24 decide | free |
| 3 | TokenCensus.Fixtures | 453 | 3.3 | scoped token census | free |
| 4 | AxiomCensusResearch | 412 | 8.0 | see above | free |
| 5 | Compiler.CommittedTerminalController | 242 | 4.3 | 14 #guard, 18 decide | free |
| 6 | Compiler.Tower256SuccinctReceiptCodec | 191 | 3.3 | | Tower256 lane |
| 7 | Compiler.CommittedTerminalFactoredProver | 153 | 4.3 | 10 #guard | free |
| 8 | Compiler.DurableIndexProbe | 144 | 1.2 | | free |
| 9 | Compiler.CommittedTerminalFactored7 | 120 | 4.1 | 9 #guard | free |
| 10 | Compiler.CommittedTerminalFiatShamir | 118 | 4.1 | 16 #guard | free |
| 11 | Kernel.Job | 111 | 3.5 | 61 elaborator `decide`s over string-keyed demo states, ~9 s each (FIXED for RSS, below) | free |
| 17 | Kernel.DeclaredResourceController | 59 | 1.6 | 46 s tactic | free |
| 22 | Kernel.ProviderRoute | 52 | 2.0 | `reads_projection`: `simp` unfolding `Nat.repr`/`Nat.toDigits` to compare field-name strings, 54 s | free |
| 31 | Kernel.AgentGrain | 27 | 1.7 | the same `Nat.toDigitsCore` simp set, 115 s summed | free |

The tail is the census: AxiomCensusResearch (412 s), then TokenCensus (75+ min, unfinished),
which imports it. Both are serial at the end of the umbrella, so the tail alone is longer than
everything before it.

## breadstuffs metatheory (2,115 modules measured; stopped)

| measure | value |
|---|---|
| summed lean wall | 14,698 s |
| top 20 share | 32% |
| max import depth | 68 |
| weighted critical path | 887 s, ending at GnarkVerifier.InputOpenBatchEmit (804 s by itself) |
| modules > 60 s / > 4 GiB / > 12 GiB | 28 / 88 / 4 |

Peak RSS: MlKemFips203FullDim 18.0 GiB (363 s); MinaWrapOpeningGate 14.6 (Mina lane);
PiDeclarationDeployed 14.6; RotatedKernelRefinementAvailWideCompact 14.2; PastaCurveScheduled 11.9;
MinaWrapAggregationGate 10.8 and MinaWrapOpeningWeld 10.2 (Mina lane); PastaMsmAir 9.3. The
automata deputy measured MinaBodyPreimageBitsAir at 25.9 GB and MinaWrapCommitStages at 17.3 GB.
The Mina lane has since taken BodyPreimageBits to 5.6 GB (breadstuffs 7c90a9b60).

Wall: InputOpenBatchEmit 804 s and SelectorEmit 277 s (interpreted #guards over the gnark
templates: an 11,330-assert circuit, a 154 KB JSON); CrateGeneratedKats 587 s (7 KAT #guards);
MlKemFips203FullDim 363 s (14 `native_decide`, 23 `decide`); MinaWrapOpeningGate 298 s (Mina lane).

**The Mathlib import floor.** 31 modules sit at 6.4-6.6 GiB, the cost of importing `Mathlib`
whole. 15 files in `Dregg2` do so (`import Mathlib`), among them `ForMathlib/{PolishchukSpielman,
IntervalFFT, CertifiedInterval, IntervalConvolution, GuruswamiSudan}` and
`Crypto/{MlKemCodecSpec, DecapsCoreSpec, MlKemCorrect, Fips204CorrectReal, ...}`. Every module
downstream of them inherits the floor, so no amount of proof engineering below them gets a module
under 4 GiB. Fix: import minimization (`lake shake`) on those 15 roots, then rebuild their
dependents. It is not done yet: it touches each file's imports, and a whole-tree build has to
confirm it.

## Fixed (statements unchanged, one module per commit, pushed)

Before: the cold-build table (or its profile). After: one `lake lean <file>` with the imports
warm, on bb2 at LEAN_NUM_THREADS=4 unless noted.

| commit | module | before | after | how |
|---|---|---|---|---|
| minidregg 3fd5c0ba9 | Kernel.ObjectLaw | 69.5 s, **16.5 GB** | 5.1 s, **2.7 GB** | the hash-bearing sample law by `native_decide`; pin `#assert_compiled` |
| minidregg 8f77d90b0 | Kernel.EffectsRevival.HostTeethProofs | 34.5 s, 8.3 GB | 4.0 s, 1.45 GB | `ratchet_moves` (one cSHAKE step) by `native_decide` on the Rust kernel; `public meta import Compiler.HyperdocumentCell`; 2 pins → `#assert_compiled` |
| minidregg f502c83cd | Theory.NockCost | 54.1 s, 5.6 GB | 20.8 s, 4.6 GB | 7 forge facts → one `forge_facts` conjunction, one `native_decide`, projections; pins name the shared axiom |
| minidregg eceedcf55 | Theory.NockCost.Summaries | 72.7 s, 7.3 GB | 32.2 s (includes rebuilding NockCost), 4.6 GB | 11 forge facts → one `forge_summaries_facts` |
| minidregg 6a8bdd25c | Kernel.Job | 122 s, 3.77 GB | 110 s, 2.17 GB | elaborator `decide` → `decide +kernel` (74 sites). The policy's next step, `native_decide`, needs `meta` imports of Pred.Core and Compiler.CompiledListOps and a native `Pred.all`; tried, reverted, left to the owner |
| breadstuffs 8c6583326 | RotatedKernelRefinementAvailWideCompact (+E1) | 187.6 s, **14.2 GB** | 9.6 s, 3.7 GB | deployed side conditions by `native_decide`; 8 pins → `#assert_compiled`; E1 in the same commit because its keystones inherit |
| breadstuffs 739231cdf | Circuit.Emit.PiDeclarationDeployed | 240.7 s, **14.6 GB** | 27.1 s, 6.1 GB | 7 burn-descriptor facts by `native_decide`; 8 pins → `#assert_compiled` |
| breadstuffs a0a8cd4c6 | Crypto.PrivateGraphRewrite (`digest8`) | HGC 69.6/75.1 s, 3.55 GB (hbox) | HGC 45.6 s, 3.56 GB | `let out := H xs` outside the lane function; 8 reverse dependents rebuilt green |

Six modules went from 8-16.5 GB to under 4.7 GB, and five of them are under 4 GB. PiDeclarationDeployed is
left at 6.1 GB, its import floor: EffectVmEmitRotationV3.

**Tried and dropped: TokenCensus dependency filter.** Skipping Mathlib/core constants in the
census scans is exact, but TokenCensus still ran past 24 minutes with it, so it is not where the
time goes. Reverted, not committed. The open item is in minidregg `board/seats/build-loop.md`.

## Not fixed, with the owner's decision named

- **Ember's policy (2026-11-06)**: concrete data by the compiler, general theorems by the kernel.
  It is written into minidregg DEVELOPING.md and breadstuffs metatheory/BUILD.md (Rule 3), with
  the pin rules:
  - in this toolchain each `native_decide` mints `<theorem>._native.native_decide.ax_1_1`, not
    `Lean.ofReduceBool`;
  - pin such a theorem with `#assert_compiled`, never `#assert_axioms`;
  - update `#guard_msgs` over `#print axioms` and over the tree count in the same commit;
  - orb Hygiene needs the `nativeDecide` set.

  Gates surveyed, none edited:
  - minidregg: AxiomPin.lean:33 refuses by design; AssertCompiled.lean:32 is the pin;
    AssertAxioms.lean `#assert_axioms_tree` counts and does not refuse;
    scripts/lean-modularize.py:19,34; scripts/check-objective-examples.sh:9.
  - breadstuffs: orb/Hygiene.lean:46-51,107-119; Dregg2/Tactics.lean:161-169;
    scripts/axiom-hygiene-guard.sh is sorry-only; ci.yml:1591-1594.
- **Next under the policy (not done; owners free)**:
  - Assurance.DeployedCredentialLifecycle (11.6 GB): ~40 `decide`s over concrete policy states.
    Two downstream endpoint modules use its theorems, so their pins move in the same commit.
  - Compiler.StoreCodecBook (9.4 GB), Kernel.ProviderExecutionLease (7.1 GB),
    Assurance.DreggNetProviderConsumer (7.1 GB): not profiled.
  - breadstuffs MlKemFips203FullDim (18.0 GB): profile pending.
  - PastaCurveScheduled (11.9 GB), PastaMsmAir (9.3 GB), the MlKem/MlDsa spec modules: concrete
    KAT checks; the Mina lane's pattern applies.
- **ResourceBirthController `authorityWrites_postLaw`** (13-15 GB). Bisected as above. The next
  step is to prove `PhysicalPostLaw deployment (authorityWrite post)` from a lemma about
  `decodeCell`/`cellBytes` in CredentialAuthorityDomainReceiver, so the kernel never compares two
  `decode` applications.
- **String-keyed states** (Job, ProviderRoute, AgentGrain). Field names `"resource/field/12/after"`
  built with `Nat.repr` force `simp`/`decide` to compute strings. One `@[simp]` lemma per field
  name (proved once by `rfl`), or Nat-keyed slots, would remove it.
- **Interpreted #guard suites over 30 s**: Tower256SuccinctHonestRun (934 s, Tower256 lane),
  EvmStage0NativeDeployment (457 s), CommittedTerminal* (118-242 s), breadstuffs
  InputOpenBatchEmit (804 s, on the critical path), SelectorEmit (277 s), CrateGeneratedKats
  (587 s). All of these want the 4(c) treatment: a `lean_exe` whose `main` asserts the same
  guard list, run by the gate. Not landed today. Moving a build-time check into a gate-time exe
  needs each repo's gate to run the exe in the same commit, and that wiring is the gate owner's.
  minidregg's lakefile already has the pattern (`objective-cdiff`, `generic-simplex-harness`).
- **Census tail**: AxiomCensusResearch 412 s. Not profiled further.

## Structural

### (a) Olean snapshots across boxes: built, tested

`scripts/iter-check publish|fetch` is in both repos. A snapshot is
`~/olean-store/<repo>/<commit>/{lib,ir}`, read-only, hard-linked against the previous snapshot,
and never linked into a live tree. `fetch` picks the nearest ancestor commit the box holds and
checks that the manifest key matches.

- Lake's traces are content-hashed and path-independent. A tree copied to another path on bb2:
  `lake build --no-build Minidregg` → "All targets up-to-date (10418 jobs)".
- **Cold → warm, hbox → Mac**: 324 MB (the HierarchicalGraphCommitment closure at a0a8cd4c6) in
  135 s, then `--no-build` "All targets up-to-date (3006 jobs)" in 6 s. Building the same closure
  on hbox took 153 s; on the Mac, at load 180-490, it would be several times that.
- The generated `.c` must travel too. A trace lists its `.c` as an output, so an oleans-only
  snapshot left every module stale; this was found and fixed in the tool. `.o` files stay out.
- minidregg f54c4205e is published on bb2 (2.1 GB). Cold fetch to the Mac took 234 s, and then
  `lake build --no-build Kernel.ResourceBirthController` reported 1536 jobs up to date in 4 s.
- Reproducibility of the stamp: snapshots never feed `emit_descriptors`/the candidate pipeline,
  and Lake re-verifies every hash on use, so a stale snapshot costs a rebuild, never a wrong
  green. The minidregg pipeline's own Lake artifact cache (`LAKE_ARTIFACT_CACHE`) is off in every
  pool (`pool.env`). Its read-only shared packages and Lake's precedence rules
  (a workspace-level `enableArtifactCache` propagates to dependencies) conflict. That is why a
  per-commit snapshot is the working form today.

### (b) The Mac: correct Mathlib per manifest. Built; the switch is ember's

Root cause, from reflogs and transcripts (helper lane): the Mac minidregg tree's `.lake/packages`
are symlinks into breadstuffs' packages (v4.30 Mathlib), and `~/src/mathlib4` points at
breadstuffs-codex's Mathlib. Lanes running `lake` in the shared trees switch one checkout between
the two pins:
- 10-30 08:14 PDT: agent a141a9c5 copied the symlinks with `cp -cR`, then ran `lake update mathlib`,
  which unpacked 5,964 v4.35 oleans into the v4.30 checkout;
- the same flip-flop on 11-05 21:01 and on 11-06 at 11:47:30 (minidregg `lake env lean`) and
  11:47:48 (breadstuffs `lake env lean`).

The fix is read-only keyed dirs, `~/tools/lean-packages/{3a3779933df4 (minidregg),
856c40722ebb (breadstuffs)}`, and the tool `~/tools/lean-packages/lean-packages ensure|link|verify`.
A wrong-key `lake` now fails with "Permission denied" instead of moving the checkout. The
proposed switch for the shared trees is in `~/tools/lean-packages/README.md`; it is not performed.

Rule (both DEVELOPING.md): lanes never run `lake` in a shared tree. They use their own worktree
or clone, linked with `lean-packages link --mine`.

### (c) `lean_exe` for slow #guard suites: not landed (see above)

### (d) `make check-fast` / `check-full` / `check-umbrella` / `boxes`: in both repos

`scripts/iter-check` (python3) and a `Makefile` beside each lakefile, documented in
`DEVELOPING.md` (minidregg root, breadstuffs `metatheory/`).
- **check-fast**: the changed `.lean` files; imports `--no-build`-checked; at most 40 stale jobs
  rebuilt locally, else defer to check-full; then `lake lean FILE` per file. It uses `lake lean`
  because `lake env lean` skips the lakefile's `leanOptions` and minidregg's `--load-dynlib`.
- **check-full**: rsyncs the tree to a persistent clone on the least-loaded box, builds the changed
  modules plus their in-tree reverse dependents, and runs detached with a PID file. The log comes
  back to the Mac.

Box policy (root's rebalance, 2026-11-06):
- score = `load1/ncpu + used_rss/total`;
- a box is skipped when free memory < cap + headroom (40 GB on bb2/hbox, 4 GB on forge), during
  forge's 10:00-11:00 UTC pause, or while this lane already has a live run there;
- umbrella and 32G jobs go to bb2 only;
- LEAN_NUM_THREADS 8 on bb2, 6 on hbox and forge; forge uses `systemd-run --scope -p MemoryMax=12G`
  under `nice -n 15` in `/srv/lanes/iter-check`, with its own elan.

The first probe chose forge (score 0.26) over hbox (1.16), and refused bb2 (39 GB free < 32 + 40).

## The lane loop, before and after

The loop is: edit one Lean file, check it with its guards, land.

**Before, on the Mac.** There was no correct check:
- the shared Mathlib had 5,964 v4.35 oleans under a v4.30 checkout, and lanes flipped it between
  the trees' pins;
- single-file checks worked only through a borrowed Mathlib;
- a fresh lane tree had no oleans for the repo's own modules, so the first check of a deep module
  meant building its closure on a 12-core Mac at load 140-490;
- the automata gate ran 92-116 s against 17.8 s on hbox.

**Before, on the boxes.** A lane checked single files with lane-check on a pool tree, and an
umbrella took ~20 min on hbox (10,449 jobs), was OOM-killed at 12G, and was measured here at
2,550 s plus a census tail of 75+ min on bb2.

**After, on the Mac** (own clone + `lean-packages link --mine` + `iter-check fetch`):

| step | breadstuffs (HierarchicalGraphCommitment) | minidregg (Kernel.ProviderRoute) |
|---|---|---|
| one-time: link the keyed packages | seconds (dir already built; `ensure` ~2.5 min once per manifest) | same |
| one-time: fetch the snapshot | 135 s (324 MB, from hbox) | 234 s (2.1 GB, from bb2) |
| confirm warm (`lake build --no-build`) | 6 s, 3006 jobs up to date | 4 s, 1536 jobs up to date |
| edit → `make check-fast` | 158 s (file 124 s), Mac load 139 | 126 s (file 101 s), Mac load 170 |
| `make check-full` (box) | hbox: 34 s sync, then a build of the changed module + dependents | - |

**After, on bb2.** The single-module checks of the fixed modules take 4-32 s each (table above).
The same Mac loop lands in under 2 minutes when the Mac is not at load 140+. The Mac's own load,
not Lean, is now the largest term: the same HierarchicalGraphCommitment check is 45 s on hbox.

## Other findings

- **bb2's `flock` is not flock.** `/home/build/.elan/bin/flock` (an obend shim, 11-02) shadows
  `/usr/bin/flock` on the `build` user's PATH. It ignores the lock for most commands and wraps any
  `lake env lean` in `timeout 60s`. Every minidregg pipeline script that runs bare `flock` as
  `build` on bb2 is affected. Ember's call; not touched.
- **The Mac is overloaded.** Load averages were 180-490 on 12 cores during the day: obend runs, a
  VM, rustc, sbcl, z3, and 142 `node_repl` processes. That, not disk, is why per-file checks take
  5× longer than on hbox. An `import Mathlib` alone took 37 s there (helper lane).
- **The shared session scratchpad** is written by every lane, and one lane overwrote another's
  Codex outputs. Recommend one subdirectory per lane. This lane used `scratchpad/iterspeed/`.
- **Lake has no `-j`.** Concurrency is one lean process per ready module. An umbrella under a
  12 GB cap needs admission control, because the umbrella, the censuses and `Assurance` each load
  the ~8 GB whole-tree olean set. The timing wrapper's slot mechanism is the prototype: a
  `LEAN_SYSROOT` wrapper that admits a module only when the slots' summed RSS estimates (from
  `scripts/pipeline/lean-module-rss.tsv`, which build-native-host already uses for seat weights)
  fit under the cap. Not wired into the pipeline yet.
