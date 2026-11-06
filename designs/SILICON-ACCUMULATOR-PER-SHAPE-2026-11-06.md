# Accumulator contract per MMA shape: answer to R2 (2026-11-06, initiative 14)

Answers `SILICON-THEOREM-REPAIRS-2026-11-06.md` R2a-R2c. The statements are **checked**, not proposed:
minidregg branch `lane/mma-exact`, `Theory/MmaAccumulatorExact.lean`. The file is core Lean, checks
standalone, and uses at most the `propext` and `Quot.sound` axioms. The counts are in zkml-research
`notes/construction-search/mma_counts.py`; the reasoning is in `notes/tensor-core-holography/F3-MODEL.md`.

## What changes in R2

1. **R2b's order is too narrow.** PTX leaves the accumulation order unspecified. `hw_exact` quantifies over
   every summation tree, deriving the per-subtree bound (Astra S01).
2. **A post-addition `addStep` cannot express multi-term alignment.** That is the Fasi group adder, which
   aligns addends to the group's largest exponent before adding. `groupAdd` / `group_exact` model it.
   - Inside the bound the alignment quantum is 1, so the result is exact.
   - Witness: `group_inside`. Falsifier: `group_fails_outside` (128 + 1 gives 128 at m = 7).
   - **The probe must therefore measure the alignment width, not only which integers the output register
     holds.**
3. **The integer accumulator is a different contract.**
   - `.s32` wraps (PTX), and `hwWrap_eq` holds in any order.
   - Reads: signed exact up to 33,025 u8 products; unsigned up to 66,051; parity (GF(2) matrices) at every
     length.
4. **"At 14 bits the FP4 point is probably dead" is withdrawn.**
   - Promoting to INT32 every K_p ≤ 255 products gives N·64 < 2^31.
   - The cost is ~61 SIMT ops per BabyBear^8 element pair (scale by 4 for doubled E2M1, cvt, iadd).
   - Whether FP4 wins is a bytes-and-encode question per SKU (F3-MODEL.md §1.2). On B300 it leads FP8 by
     1.18x only when limbs are stored in HBM, and only under the assumed encode costs.
5. **First failure is not "one past the bound".** At P = 64, m = 14 the bound is 255, 256 is exact, and 257
   fails. For FP8 (P = 225) the bound is 72 and 73 fails. Both come from exact search over reachable sums.

## Probe

degg-research `experiments/mma-accumulator-probe/`. It holds the layout-free `.u8` wrap and e4m3 C-path
probes (uncompiled) and a one-hour protocol for when ember grants a GPU.
