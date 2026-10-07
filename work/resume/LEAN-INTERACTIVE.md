# LEAN-INTERACTIVE — interactive Lean for the Mini swarm (2026-10-06/07, burst2-b)

Ember asked: "can we be using lean more incrementally / interactively than we are?" and "we can upgrade to a
newer lean version maybe". Evidence classes: READ = toolchain/Lake source or release notes, EXECUTED = run on
burst2-b. Logs are in hbox:/tank/dregg-build/claude-lanes/bundles/lean-interactive-logs.tgz.

## 1. What v4.30.0 offers (READ: ~/.elan/toolchains/leanprover--lean4---v4.30.0/src/lean)
- **Language server incrementality** works today. `lake serve` re-elaborates a document from its first
  *syntactic* change on (Lean/Language/Lean.lean `process`). LSP extensions: `textDocument/waitForDiagnostics`,
  `$/lean/plainGoal`, `$/lean/plainTermGoal`, and `didOpen.dependencyBuildMode` = always|once|never. With `never`,
  the worker runs `lake setup-file --no-build`, so it never builds outside a slot. `LAKE` env selects the lake binary.
- **REPL** (leanprover-community/repl) has tag v4.30.0 (dde7dd43). It supports command/tactic mode, `env` reuse,
  and pickling envs and proof states to .olean (mmapped, imports not duplicated). A pickle carries declarations,
  not compiled code: `#eval` of a pickled def fails (EXECUTED). The REPL's file mode names its input `<input>`,
  so files that compute their own directory fail there (EXECUTED; hence `--after` goes through the server).
  Pantograph exists but was not needed.
- **Module system** is enabled on 4.30 (`experimental.module` is a no-op). Imports can be `public`, `meta` or `all`;
  defs are private unless `@[expose]`; theorem bodies go to `.olean.private` and positions to `.olean.server`.
  A `module` file may import only `module` files (Environment.lean: "cannot import non-`module` X from `module`").
  Lake (Build/Module.lean `computeExportInfo`/`addImport`): a module importer's trace mixes only the imported
  module's public `.olean` hash. A non-module importer mixes `allArtsTrace` (the private olean too), and so does
  every legacy importer downstream of it. Mathlib at our pin is already `module`.
- **Lake artifact cache** is local and per toolchain (`enableArtifactCache`/`LAKE_ARTIFACT_CACHE`,
  `LAKE_CACHE_DIR`), keyed by input hash. Lake's own help says its hashes are *not cryptographically secure*,
  so remote uploads are scope-prefixed. Cross-box sharing goes through `lake cache put/get` (an S3-compatible
  endpoint via curl, `LAKE_CACHE_KEY`) or `lake cache stage/unstage <dir>` plus rsync. Not trialled: our `cp -al`
  warm bases already give the within-box effect. 4.31 fixed missing `meta import` IR under the cache, which is a
  hazard on 4.30 once modules exist.
- Lake 4.30 has no `-j`; `--old` (ignore transitive deps) exists, but it is exactly the stale-olean false green.

## 2. Built: `lean-ask` (EXECUTED; lane/lean-interactive d5ac086b on main 7b093d19, QUEUED)
`scripts/pipeline/lean-ask` (Python, stdlib only) plus `lean-ask-install-repl` and `lean-ask-selftest`.
They are installed at /srv/pipeline/scripts on burst2-a and burst2-b, with the REPL at /srv/pipeline/repl.
One daemon per tree (under swarm-build, 2 h idle exit) holds `lake serve` and up to 3 REPL envs.
- `check FILE[:FROM]`, `goals FILE:LINE[:COL]`, `eval CMDS --file F | --imports A,B | --env-pickle P | --after F`
  (`--after` = a virtual sibling document of F through the server; nothing is written to disk).
- **Staleness**: before each answer the tool takes a stat fingerprint of the loaded local import closure (sources,
  .oleans, lake-manifest, lean-toolchain, lakefile). On any change it REFUSES with exit 3 and names the changed
  paths. `--reload` rebuilds stale imports the lane-check way (`lake build --no-build`, else a build in a slot)
  and then reloads.
- `lean-ask-selftest` PASSED 3 times against /srv/warm-base/src. It checks: a false theorem goes red (check and
  eval); a committed change to an import makes check and eval refuse, naming it; `--reload` sees the planted
  declaration; the base .olean stays byte-identical.

## 3. Measured win (EXECUTED, burst2-b, 4 edit cycles each; logs bench3.tsv)
| edit | lane-check | lean-ask check |
|---|---|---|
| Kernel/ObjectiveResumeContract.lean, proof at l.600 | 3.6 s | 0.40 s |
| Theory/ObjectiveBendTemplates.lean, proof at l.1145 | 6.9 s | 0.35 s |
| Theory/ObjectiveBendTemplates.lean, proof at l.387 | 7.0 s | 5.0 s (everything below re-elaborates) |
- First open: 4–8 s. `goals`: 0.03 s.
- `eval` against ResumeContract's imports: 2.6 s to load, then 0.03 s per query. `eval --after`: 4.4 s first, then 0.017 s.
- The REPL's RSS reads ~11 GB, mostly mmapped Mathlib/Mini oleans (shared page cache). Sessions are capped at 3 envs.

## 4. Module-system pilot (EXECUTED; lane/lean-modpilot 440461ba, PROPOSAL, not queued)
- **Cluster**: Theory.AxiomPin, ObjectiveBendTypes, ObjectiveBendOpenRecursion, ObjectiveBendTyping and
  ObjectiveBendTemplates (5 modules, 3.5k lines), converted with `module`, `public import` and
  `@[expose] public section`. One fix was needed: `meta def standard` in AxiomPin.
- **Edit**: a proof edit inside Ty.isRow_mono in Typing, both on the same line and adding a line.
- **Legacy**: 4 of 4 targeted modules rebuild, and Typing.olean changes.
- **Module**: Typing.olean is byte-identical after both edits, and the module importer Templates is not rebuilt.
  The legacy importers DemandTyping and TermWire still rebuild, exactly as derived from Lake.
- **Scale**: Typing has 562 transitive dependents. Today all of them rebuild on any proof edit. That drops to 1
  only once the whole reverse closure is `module`, and conversion has to go bottom-up.
- **Measured cost per module**: low with the blanket expose recipe (1 fix in 5 modules).

## 5. Upgrade trial: v4.34.1 + Mathlib v4.34.1 d13f23b7 (EXECUTED; lane/lean-upgrade-trial 0b78cae9, PROPOSAL)
- **Versions**: newest stable Lean is v4.34.1 (2026-09-24), and Mathlib has tag v4.34.1. 4.35 is rc4 only.
- **Setup**: `lake update` took 57 s and `cache get` 3 s. The cold umbrella build in one slot stopped after 59 s.
- **Result**: **28 modules fail. 1,078 of the 1,230-module umbrella sit behind them and were never checked; 124
  checked clean.**
- **Failure kinds in the first wave**:
  - 6 `#guard_msgs`/axiom pins (message reflow, and pins that now include `Classical.choice`: an assurance review item)
  - 14 simp/rw/`decide` breakages (8 `decide`)
  - 3 kernel deep recursions in `norm_num` primality of 31-bit primes (Compiler.BabyBear and Selvage.BabyBearExt4 are foundational)
  - 5 elaboration/typeclass/API errors
  - 0 native_decide and 0 Lake-config problems
- **Extrapolation** at 18% of the checked modules: on the order of 150–250 failing modules in total. Unknown
  until wave 2.
- **What it gives this goal (READ, reference-manual Releases v4_31..v4_34)**:
  - 4.32 adds experimental `lean --incr-save/--incr-load`: lane-check could become incremental across processes.
  - 4.33 and 4.34: editor responsiveness; incremental `set_option … in` tactic blocks.
  - Lake: `requiresModuleSystem`, content-stable .ltar, `lake cache get --package`, cache robustness fixes, and
    detection of truncated .oleans.
  - Kernel soundness: 4.33 (incl. #14609 module-system `partial` leak, metaprogramming-only) and 4.34 (three
    routes to False, sticky refcounts).
  - `import Mathlib` is ~10% faster.
- **Recommendation: LATER, as one dedicated campaign, and BEFORE any module-system conversion beyond the pilot.**
  Nothing in this goal requires the upgrade: lean-ask and the module cut both work on 4.30. The real reasons to
  upgrade are the kernel soundness fixes and the 4.33 module-system fix.
  - Estimate: 2–3 lanes for about a day, working in waves of one umbrella build each.
  - Wave 1 is 28 modules, mostly mechanical.
  - The BabyBear primality fix unblocks the largest subtree.
  - The `Classical.choice` widening needs a reader, not a re-pin.
  - Re-pin `lean-ask-install-repl` to the matching REPL tag (v4.34.0 exists; v4.34.1 must be checked).

## Next steps
1. MERGE-KEEPER lands lane/lean-interactive (QUEUED). After that, lanes use `lean-ask check` as their inner loop
   (usage is in BURST2-BRIEF).
2. Upgrade campaign (when Ember picks a window):
   - Start from lane/lean-upgrade-trial, fix wave 1, rebuild, count wave 2.
   - Then pin the REPL for the new toolchain.
3. After the upgrade: convert to the module system bottom-up from the Objective Bend core, starting with the
   pilot recipe, and measure the dependents saved per wave. Set `requiresModuleSystem` on the package last.
