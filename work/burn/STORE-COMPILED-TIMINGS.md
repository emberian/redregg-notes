# Store compiled timings: full image vs light open (BURN-BENCH, 2026-10-07)

Measurement only. No kernel code changed. Box burst2-a (16 threads), tip cfdaf64d.
Harness: `Host/BenchStoreCompiled.lean` (lean_exe `bench-store-compiled`), branch `lane/bench-store` (b4f63f83) in burst2-a:/srv/git/minidregg.git; lane /srv/lanes/bench-store; raw logs /srv/lanes/bench-store/logs/measure-{300,3000,30000,30000b}.txt; driver scripts/bench/store-compiled-measure.sh.

## Method (exact)
- Store: real SQLite helper (minidregg-link-sqlite-store from the cfdaf64d artifact set), real codecs/MAC/accumulator/spent map. Grown to N records through `receiveLoadedDetailed` on the live image, `checkpointEvery := 64` (Host.Main's deployment default), each record = one 1001-byte cell write + one nullifier (same shape as Kn2StoreBench). Final checkpoint at 256 / 2944 / 29952.
- One process per measurement (so /usr/bin/time -v peak RSS is per measurement). Each measurement run 3 times, **best of 3 reported**, all three shown. "Wall" = whole process wall time (includes the store-helper spawn and Lean startup); "ms" = in-process monotonic clock around the named step. Append runs use a fresh `cp -r` of the grown store each time.
- (a) full open = `DurableReceiverIO.load`; light open = `DurableServed.openHead`.
- (b) append = one record: full = `load` then `receiveLoadedDetailed`; light = `openHead` then `DurableServed.receiveServed`. "append only" excludes the open.
- (c) past read at 20 heights `floor(cp*(i+1)/21)`, i=0..19, cp = last checkpoint height (all below the last checkpoint): image = `Loaded.atPrefix` over the loaded image; Reader = `Reader.stateAt` (full: `readerOf` on the loaded image; light: `Opening.reader`). Timing excludes the open. Reading cell 3's canonical bytes after each.
- (d) `since`: windows of 256 via verified `Reader.range`, last 256 and last 2560 records (at N=300 only 300 exist). Image = the unverified encoded tail `loaded.image.accepted.drop c` (`recordFrame.encode`, length summed).
- Concurrency: a single-threaded background job (the N=30000 atPrefix) shared the 16-thread box during some runs; everything else here is single-threaded, so contamination is negligible.

## (a) open, ms (best of 3) and peak RSS
| N | full open ms (3 runs) | full RSS MB | light open ms (3 runs) | light RSS MB |
|---|---|---|---|---|
| 300 | **63** (65,73,63) | 96 | 147 (157,158,147) | 87 |
| 3000 | 425 (460,463,425) | 292 | **202** (220,202,203) | 89 |
| 30000 | 4275 (4510,4275,4465) | 2248 | **194** (194,205,209) | 86 |

Process wall (full / light): 0.09/0.17 s, 0.47/0.23 s, 4.52/0.22 s. Crossover is between N=300 and N=3000 (roughly 1000). Full open is linear (~0.14 ms/record) and RSS is ~75 KB/record. Light open is flat at 150-220 ms and ~87 MB.

## (b) one append after open, ms
| N | full open | full append only | full total | light open | light append only | light total |
|---|---|---|---|---|---|---|
| 300 | 65 | 14 | 79 | 146 | 15 | 161 |
| 3000 | 462 | 60 (60,100,64) | 522 | 206 | 26 | 232 |
| 30000 | 4314 | 312 (312,330,337) | 4626 | 200 | 77 (79,79,77) | 277 |
Peak RSS follows the open (99 / 292 / 2248 MB full; 86 / 89 / 87 MB light). Light append is cheaper than full append at every N and grows with N more slowly (15, 26, 77 ms); not profiled further.

## (c) 20 past states, ms
| N | atPrefix over loaded image | Reader.stateAt, full open | Reader.stateAt, light open |
|---|---|---|---|
| 300 | **72** (83,80,72) | 758 | 769 |
| 3000 | 7397 (7496,7587,7397) | 922 | **934** |
| 30000 | **3,397,338 (56.6 min), ONE run only** | 858 | 815 |

Peak RSS: image 96 / 292 / 2301 MB; Reader on light 86-88 MB at all N.
- stateAt is flat in N: ~40 ms per state (it resumes from at most one checkpoint and replays <=63 records).
- atPrefix is **O(h^2)** for any height below the last checkpoint (it falls back to a genesis fold of `prefixImage h`): single heights at N=30000: h=300 13 ms, h=1000 120 ms, h=3000 1221 ms, h=10000 29802 ms. So the compiled picture reverses the interpreted one: at N=300 stateAt is ~10x SLOWER than atPrefix (the interpreted probe said ~4x), at N=3000 stateAt is 8x FASTER, at N=30000 atPrefix needs ~1 hour for 20 states (stateAt 0.8 s). The ROOT/PORT-D worry ("if stateAt stays slower at 3000") does not hold: it is faster at 3000 compiled. (Runs 2 and 3 of the N=30000 atPrefix were not made: I killed the driver; the one run is shown.)

## (d) since window, ms (verified Reader.range, windows of 256)
| N | window | image tail (unverified, encode only) | Reader.range full open | Reader.range light open |
|---|---|---|---|---|
| 300 | last 256 | 8 | 62 | 62 |
| 300 | last 2560 (only 300 exist) | 6 | 71 | 71 |
| 3000 | last 256 | 7 | 61 | 63 |
| 3000 | last 2560 | 73 | 743 | 731 |
| 30000 | last 256 | 9 | 70 | 68 |
| 30000 | last 2560 | 82 | 857 | 799 |
Range verification costs ~0.3 ms/record, identical on full and light openings (it is the same function); the image tail is ~10x cheaper because it verifies nothing (that is the point). The only cost difference between paths is the open: whole-process wall at N=30000 is 6.1 s (full) vs 1.1 s (light).
(N=300/3000 image-tail rows use a re-run of the fixed harness, 3 runs each: 8,8,10/9,7,6 and 8,7,8/82,80,73; N=30000 rows are from the main run. A first version of the harness let the tail be optimised away, printing 0 ms; those 0 ms numbers in the raw logs for N=300/3000 are invalid.)

## Where the light path loses, at profile level
No `perf` on the box; sub-phases from `MINI_OPEN_TIMING=1` (the product's own laps, cumulative ms) and timed pieces of stateAt.

Light open (run 1, cumulative ms):
| phase | N=300 | N=3000 | N=30000 |
|---|---|---|---|
| read (store read from checkpoint) | 3 | 4 | 5 |
| checkpoint (open sealed + tag verify) | 8 | 9 | 9 |
| records, chain, tags, frontier (<=63 records) | 17 | 20 | 17 |
| index rows read (helper call) | 49 | 73 | 67 |
| index (`checkIndex` of the suffix) | 147 | 208 | 183 |
| replay and root | 157 | 220 | 193 |
- Head verification, checkpoint verification, per-record tag verification: ~20 ms in total at all N (O(suffix) <= 63 records plus one checkpoint).
- **The light open loses at small N because of the index stage: ~50 ms (rows read) + ~100-135 ms (`checkIndex` re-deriving the suffix's index rows)**, i.e. 70-80% of 150-200 ms, a fixed cost independent of N. Full open at N=300 is 63 ms because it does not pay this. (The "shallow 48-bit then deep" fallback in `extendVerified` is a candidate for part of the cost; I did not test whether the fallback fires. Not measured, so a lead, not a finding.)

stateAt (20 heights, light, N=30000; baseOf and range are timed separately from the full stateAt call, so replay is a residual):
| piece | ms total / 20 | per state |
|---|---|---|
| baseOf (checkpointAt + openSealed + atHeight) | 137 | 6.9 |
| range after base (verifies 567 records) | 210 | 10.5 (0.37 ms/record) |
| replay + snapshot (residual) | ~480 of 829 | ~24 |
(N=300: 92 / 147 / residual 530 of 767; N=3000: 124 / 184 / residual 530 of 836.) Replay of the verified records dominates (~55-60%), then range verification (~25%), then baseOf (~15%); every piece is constant in N. Per-state cost ~40 ms is therefore a fixed (<=63-record) price, which the light path and the full path pay identically. ROOT's "verify a window once and fold" idea would amortise the 40 ms across consecutive heights but was not tried.

Summary: the light path is a win for N >~ 1000 on open time, memory (flat 87 MB vs 75 KB/record), append and past reads. It loses for N <~ 500 on open (fixed ~150 ms index stage) and, for small N, on past-state reads (40 ms/state vs ~3.6 ms/state for atPrefix when heights are within a few hundred records of genesis). Neither "full image is the cheaper reader" holds beyond that.

## Finding for DEPUTY-KERNEL: PORT-D's `FAIL commit 1001` is the probe, not a Store bug
My compiled grow went through record 1001 and on to 3000 and 30000 with no failure (checkpointEvery 64; note PORT-D's probe used 16 and `receive ... 3`). PORT-D's probe (scripts/kn2/doc-history-past.lean) has `seed.available := fun _ => 1000` and every step `exactCharge := fun _ => 1`: the budget is exhausted after 1000 records. I reproduced minimally by changing only my seed to `available := fun _ => 1000`: `append 1001 did not confirm` (an `.ordinary` outcome from `receiveLoadedDetailed`, run to 1001 on a fresh store). So the crash is a correct refusal on an exhausted budget; the probe needs `available` >= N (my bench uses 1000000000). I did not read out the refusal's exact text (the harness only reports the `.ordinary` constructor), so "budget" is the cause established by changing only that number, not by a message.
