# CYCLE-FIX log: lane/cycle-fix (Claude, Mac-authored, built nothing)

- **Branch:** `lane/cycle-fix` on GitHub, made from main 2c27b08b.
- **Worktree:** `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/cycle-fix`.
- **Design and measurements:** `work/CYCLE-TIME-20261016.md`.

## Commits (one per fix)

| fix | sha | subject |
|---|---|---|
| 2 | `6b7b0c00` | build-native-host!: one parallel Lake build, seated per compiler, instead of a 775-process loop at one Lean |
| 1 | `ca6e7ac8` | pipeline!: the shared Lake cache is on by construction; its audit is a pipeline step from the tip tree |
| 3 | `c38b994a` | native-host+slots: per-module peak RSS from the seated Lean wrapper; with-lean-slot's FIFO is a repo script |

### Checks run on the Mac (no Lean, no cargo)
- `python3 scripts/overnight-tests/native-build-locks.py`: PASS. 16 jobs over 3 seats with a peak of 3, balanced. One RSS line per compile. The refusal returns 75 and leaves owners intact. A wrapper that receives TERM keeps its seat until the compiler exits.
- `cd scripts/pipeline && python3 -m unittest test_lake_cache_audit`: 4 OK. Covers a clean cache, a written-through artifact (purged), an unprefixed initializer (purged), and a broken audit (exit 2).
- `bash scripts/overnight-tests/native-success-prefix-guard.sh`: PASS. The prefix functions are unchanged.
- The RSS-table fragment was checked on a synthetic wrapper log.
- `bash -n` is clean on every edited shell script.
- **Not run here:**
  - `scripts/pipeline/test-with-lean-slot.sh`, because the Mac has no `flock`.
  - `deploy/candidate/test-lane-build.sh`, which needs `readelf`.

### What depends on serial order
- **Modes that keep the ordered loop.** The loop is now seated. These modes checkpoint or reuse a byte-checked prefix, or start at a named module:
  - `--checkpoint-resume`, `--resume-failed`, `--resume-complete-lean`, `--reuse-success-prefix-from`
  - `--incremental-host-from`, `--incremental-suffix-from`
- **Nothing else.** I found no theorem or gate that needs serial order.
  - The only check of the serial invariant was `scripts/overnight-tests/native-build-locks.py` (`maximum == 1`). No gate runs it, and it had already stopped parsing after the seat-count change. It is rewritten for the new invariant.
  - The loop goes back to 8305b6ef, where a bare `lean -o -i -c` had to run one module at a time. 5e20f114 replaced that call with Lake and kept the loop around it.

## Commands for the first burst box to run

Run these as the box user, in a lane tree at `lane/cycle-fix`. Use `swarm-build` for anything that builds. Run every step in the foreground.

### 0. Box settings
```
scripts/pipeline/box-env --layout /srv/pipeline --slots "<lane slots>" --lean-threads 4 --lake-cache /srv/lake-cache \
  --set "MINIDREGG_LEAN_SEATS=6 MINIDREGG_LEAN_THREADS=4 MINIDREGG_NATIVE_JOBS=16 PIPELINE_LEAN_SLOTS=6 PIPELINE_LEAN_SLOT_THREADS=4"
grep -E 'LAKE_|MINIDREGG_LEAN|PIPELINE_LEAN' /srv/pipeline/box.env
```
- **Expect:** `LAKE_CACHE_DIR=${LAKE_CACHE_DIR:-/srv/lake-cache}`, `LAKE_ARTIFACT_CACHE=${LAKE_ARTIFACT_CACHE:-true}`, and the `--set` values. `--no-lake-shim` should refuse by name.
- **Why 6 × 4:** burst4 ran 6 × 4 inside a 158 G slice. This is the starting point; resize after step 3b.

### 1. Shared cache (fix 1)
1. Run `cd scripts/pipeline && python3 -m unittest test_lake_cache_audit`, then `bash scripts/check-unit-tests.sh | tail -3`.
   - **Expect:** 4 OK. The new row is green.
2. Prove the cache shares work across lanes. Make two lanes from the warm base, A and B, both at the same lane/cycle-fix commit plus one throwaway commit. That commit adds a comment line to `Kernel/World.lean`, which rebuilds 516 modules in the research umbrella, 436 of them in Host.Main.
   - In A: `time scripts/pipeline/lake-slot Host.Main +Host.Main:leanArts`. Record the wall time and `grep -c '] Built'` of its output.
   - Then in B: the same command.
   - **Expect:** B compiles about 0 modules and takes well under a minute, against A's minutes.
   - **Before-number:** each hbox lane recompiled modules other lanes had built, for example 823 modules in 8,046 s.
   - Then run `stat -c %h B/src/.lake/build/lib/lean/Kernel/World.olean`.
   - **Expect:** a link count of 2 or more, because the file is a hard link to the cache artifact.
3. Run `python3 scripts/pipeline/lake-cache-audit --cache "$LAKE_CACHE_DIR" --tree "$PWD"`, then `python3 scripts/pipeline/lake-cache-audit --tree "$PWD" --scan-tree B/src | wc -l`.
   - **Expect:** `0 bad` and 0.

### 2. Builder (fix 2)
1. Run `python3 scripts/overnight-tests/native-build-locks.py`.
   - **Expect:** 3 PASS lines.
2. Warm candidate at the unchanged tip: `LANE_DIR=$L swarm-build deploy/candidate/lane-build.sh host`.
   - Read `grep -E 'lean-closure|elapsed_seconds|max_concurrent|compiled_source' $L/native-out/build.log $L/native-out/manifest.txt`.
   - **Before:** the loop alone took 634–661 s and the host step took 1,040–1,108 s elapsed (perf-fix p2/p3, fleet-race).
   - **Expect:** `lean-closure … PASS` in seconds. elapsed is then about the C phase only, until F3's object cache lands.
3. Run consent, rust and pack:
   ```
   LANE_DIR=$L swarm-build deploy/candidate/lane-build.sh consent
   LANE_DIR=$L swarm-build deploy/candidate/lane-build.sh rust
   LANE_DIR=$L deploy/candidate/lane-build.sh pack $L/cand
   ```
   - **Expect:** pack's compiled-inputs-equal check passes unchanged. `$L/consent-out/companion-recheck.log` reports all OK.
4. **Identity.** Run the same sha's host build with the old builder: a sibling lane, with `git show 2c27b08b:scripts/build-native-host.sh > scripts/build-native-host.sh` committed there. Compare:
   ```
   diff <(sort -k2 OLD/native-out/reusable-artifact-sha256.txt) <(sort -k2 NEW/native-out/reusable-artifact-sha256.txt)
   ```
   - **Expect:** no difference. Same .olean, .ilean, .c and .o bytes, and the same `binary_sha256` in both manifests.
5. **Edit case.** Add the `Kernel/World.lean` comment commit again and rebuild the host in a fresh lane with the cache disabled (`LAKE_ARTIFACT_CACHE=false`), so it really compiles.
   - **Expect:** `max_concurrent_real_lean` between 2 and `MINIDREGG_LEAN_SEATS`. The lean-closure wall should be well under the old loop's sum for the same set of modules (state-at's loop took 4,423 s).
6. **Umbrella mode (publish path).** Run `LANE_DIR=$L lane-build.sh host --umbrella --umbrella-target Host.Main` in a gated tree.
   - **Expect:** `max_concurrent_real_lean` ≤ seats, the wrapper log balanced, and a replay.

### 3. RSS and slots (fix 3)
1. After 2.5, run `head -20 native-out/lean-module-rss.tsv; grep lean_maxrss native-out/manifest.txt`.
   - These are the first per-module RSS numbers anyone has.
2. **Size the box.** The before-number is a single figure, "closure build dies at 24G" (lake-slot:8).
   - `seats = floor(<swarm-build MemoryMax> / lean_maxrss_kib_p95)`
   - `threads = nproc / seats`
   - Write both into box.env (`MINIDREGG_LEAN_SEATS`, `MINIDREGG_LEAN_THREADS`, `PIPELINE_LEAN_SLOTS`, `PIPELINE_LEAN_SLOT_THREADS`).
   - For a cold measurement of all 776 modules, build the host once in a fresh clone with `LAKE_ARTIFACT_CACHE=false`.
3. Run `scripts/pipeline/test-with-lean-slot.sh` (about 25 s).
   - **Expect:** `PASS (order: h1 h2 p w1 w2 w3 w4 w5 …)`.
4. Lanes switch from `/tank/dregg-build/pipeline/slots/with-lean-slot` to `<lane tree>/scripts/pipeline/with-lean-slot`. Both use the same locks and queue, so they coexist during the switch.
   - Then `tail slots/waits.tsv` measures real waits.
   - Remove the installed copy once SAFETY-BLOCK line 2 names the repo path.

## Known limits (not fixed here)
- **Lane umbrellas and gate builds are not seated.** Lane umbrellas (`ub.sh`, `lake-slot`, gate `lake build`) still run plain Lake. Their fanout is bounded only by the slot and the cgroup, not by per-compiler seats. Only build-native-host is seated.
  - Seating them is one step: run them through `seated_lake`, or make the wrapper a repo tool that `lake-slot` uses.
- **The C phase is unchanged.** Every host build still recompiles about 776 project C files, now at `MINIDREGG_NATIVE_JOBS` instead of 2. The content cache for C objects (a20cbc39, lane/v4-next) is still unlanded and is the next fix.
