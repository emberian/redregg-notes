# Silicon theorem repairs: proposals for obend's owner (2026-11-06)

Status: PROPOSED statements, not built. Nothing in obend was edited or built for this. Two
theorems in obend carry the right pipeline and the wrong object
(`degg-research/research/governance-foundations-critique.md` W1, W2). This note gives the
repaired statements, written to the accumulator contract of the Codex Astra statement audit
(`zkml-research/notes/astra/governance-statement-audit.md` S01/S02), with corrected numbers. Each
statement comes with the lemma it reuses, a non-vacuity witness and a falsifier.

Tags: [READ] inspected source; [MEASURED]; [PROPOSED].

---

## R1. The silicon kernel: from a `tag == 1` comparator to a universal node checker

**Today [READ].**

`Lower/Proofs/SiliconKernel.lean:270` `silicon_kernel_5stage_check_sound`:
- The statement covers five fixed declarations.
- The RTL gate (`kernelGateBody`, line 221) computes `tag == 1`.
- The tag comes from `encodeDeclStatusTag` (line 171), which runs `exprContainsSorry`,
  `encodeKExprNode`, `stepCamInferNodeWord` and `stepCamDefEqNodeWord` in host Lean.

`real_silicon_kernel_node_check_sound` (line 696):
- It does run lowered node inference and checking in RTL.
- It covers about 15 fixtures.
- The encoding is still done on the host.

**What already exists that makes a universal theorem cheap [READ].**
- `Hardware/Compiler.lean:657` `compileTermSat_sound` is universal: for every `t : Term`, if
  `compileTermSat … t = some e`, then `evalTermHwSat … t = some (evalRtlExpr … e)`.
- `stepCamInferNodeWord` (`SiliconKernel.lean:137`) is a pure `Nat` function of four words, built
  only from `hwEq01`, `hwAnd01`, `hwLe01`, `Nat.add`, `Nat.mul` and `Nat.sub`, with no recursion.
- So the only missing link is between `evalTermHwSat`, which is saturating 64-bit hardware
  arithmetic, and the `Nat` meaning of the function.

**R1a, node inference, universal at bounded width [PROPOSED]:**
```lean
/-- Inputs small enough that no Nat intermediate of stepCamInferNodeWord exceeds 2^64. -/
def NodeWordInRange (tag a0 a1 env : Nat) : Prop :=
  tag < 2^8 ∧ a0 < 2^16 ∧ a1 < 2^16 ∧ env < 2^16

theorem stepCamInferNode_rtl_universal (m : RtlModule)
    (hc : compileBookToRtlSat "infer_node" inferNodeBook = some m) :
    ∀ tag a0 a1 env, NodeWordInRange tag a0 a1 env →
      evalModuleOutputs m (nodeInputs tag a0 a1 env) (fun _ => 0#64) =
        [("out_inferTypeNode", BitVec.ofNat 64 (stepCamInferNodeWord tag a0 a1 env))]
```

Proof route:
1. `compileTermSat_sound` gives the RTL in terms of `evalTermHwSat`.
2. A new lemma, `evalTermHwSat_eq_nat_of_bounds`, shows that saturating BitVec ops equal `Nat`
   ops when the operands and results are below 2^64. That is the actual content to prove. The
   bound has to cover every intermediate, not just the inputs, which is Astra's S01 point for
   accumulators applied here.
3. Unfold the definition to `stepCamInferNodeWord`.

**R1b, declaration check over a stated fragment, with the encoder named [PROPOSED]:**
```lean
theorem silicon_decl_check_sound (decl : KConstInfo) (hfrag : InNodeFragment decl)
    (m : RtlModule) (hc : compileBookToRtlSat "decl_check" declCheckBook = some m) :
    evalModuleOutputs m (declInputs (encodeDeclWords decl)) (fun _ => 0#64) =
      [("out_check", if kernelCheckDecl stdKernelEnv 8 decl then 1#64 else 0#64)]
```
- `declCheckBook` must lower `stepCamInferNodeWord` and `stepCamDefEqNodeWord` *and* the
  sorry flag. It must not lower their result.
- `encodeDeclWords`, which stays on the host, is the named residual. Its correctness is a
  separate host theorem: `encode_faithful : InNodeFragment decl → decodeWords (encodeDeclWords
  decl) = decl`.
- Without that theorem, the encoder can supply the answer. Astra's line on F1: "encoding must not
  supply unverified typing answers".

**Witness and falsifier.**
- Witness: the existing fixtures (`eAppGood` accepted, `eAppBadDom` refused) become instances of
  R1a.
- Falsifier, which should fail to prove and so shows the statement is not vacuous: replace
  `stepCamInferNodeWord` with a constant `1` in `inferNodeBook`, and R1a must fail on the
  `eAppBadDom` encoding.
- Second falsifier, for R1b: an encoder that writes the expected type code into `arg1` makes
  `kernelCheckDecl` and the RTL disagree on `invalidMismatchDecl`.

**Cost.** R1a is a week: the composition plus the no-overflow lemma. Whether `bv_decide` may be
used is the owner's policy call. R1b is the research: `InNodeFragment` and `encode_faithful`.

---

## R2. Ozaki FP4 / MFMA: from Int identities to an accumulator refinement

**Today [READ].**
- `Hardware/Accelerators.lean` has `ozaki_base13_klimb_dot_exact`, `amd_gpu_mfma_dot4_exact` and
  `systolic_tpu_eq_dsp58_cascade_eq_kulisch_dot`.
- All three are ring identities over unbounded `Int`.
- `vMfmaDot4` is modelled as `acc + Σ aᵢbᵢ` in `Int`.
- The file's `FloatInterval` machinery exists but is not connected to these operations (Codex
  round 1, F2).

**Numbers, corrected [MEASURED].** `degg-research/experiments/mma-field-mapping/RESULTS.txt`
after Astra's representation patch:
- **Limbs and break-even.** BabyBear needs 9 FP4-E2M1 base-13 limbs, so 81 limb products per
  multiply, against 16 for INT8. FP4 is worth it only if TOPS(FP4)/TOPS(INT8) > 5.06.
- **Representation.** The certified encoder's largest digit is 8, so the largest limb product is
  64 (not 144 as first written).
- **Exact block length** per limb pair: N ≤ 262,143 with a 24-bit accumulator, and **N ≤ 255 with
  a 14-bit accumulator**. The 14-bit figure is DeepSeek-V3's report for H800 FP8 GEMM [SOURCED].
  These replace my earlier 116,508 and 113.

**R2a, the accumulator model [PROPOSED].** The model is an explicit transition, not a final-sum
bound:
```lean
structure AccModel where
  sigBits   : Nat                 -- significand width m (24 for IEEE FP32; ~14 reported for H800 FP8)
  expRange  : Int × Int
  align     : AlignMode           -- truncate | roundNearestEven | ...
  order     : List Nat → List Nat -- accumulation schedule the hardware uses
def AccModel.addStep (A : AccModel) : AccVal → Int → AccVal   -- one aligned add
def AccModel.decodeInt : AccVal → Option Int

/-- The LOCAL lemma (Astra S01): one step is exact when both operands and the result are
integers of magnitude < 2^sigBits within exponent range. -/
theorem addStep_exact (A : AccModel) (acc : AccVal) (x : Int) (k : Int)
    (hacc : A.decodeInt acc = some k) (hx : x.natAbs < 2 ^ A.sigBits)
    (hsum : (k + x).natAbs < 2 ^ A.sigBits) (hk : k.natAbs < 2 ^ A.sigBits) :
    A.decodeInt (A.addStep acc x) = some (k + x)
```

**R2b, the MMA refinement [PROPOSED]:**
```lean
theorem ozaki_exact_under_acc (A : AccModel) (xs ys : List Int)
    (hlen : xs.length = ys.length)
    (hrep : ∀ d ∈ xs ++ ys, d ∈ fp4Digits13)        -- the certified encoder's digit set, max |d| = 8
    (hinit : A.decodeInt A.zero = some 0)
    (hbound : xs.length * 64 < 2 ^ A.sigBits)        -- every PREFIX sum then stays in range
    : A.decodeInt (hwMmaDot A xs ys) = some (kulischDot xs ys)
```
- The proof is induction over the schedule, using `addStep_exact`. The bound covers every prefix,
  because each partial sum is at most `k · 64 ≤ N · 64`.
- The bound is derived from the local lemma. It must not be defined as the conclusion (Astra:
  "defining it as the final equality would be `P → P`").

**R2c, field reconstruction [PROPOSED]**, Astra S02 shape:
```lean
theorem field_dot_via_mma (p : Nat) (hp : 1 < p) (A : AccModel) (u v : List (Fin p))
    (hlimbs : ∀ x ∈ u ++ v, recombine13 (encode13 x.val) = x.val)   -- encoder round trip
    (hblock : u.length * 64 < 2 ^ A.sigBits)
    (hwidth : RecombinationFitsInt64 u v) :
    (recombine13 (limbwise (hwMmaDot A) u v)) % p = (List.zipWith (·.val * ·.val) u v).sum % p
```
Primality is not a hypothesis of the identity. The encoder round trip is the Lean counterpart of
the asserts the patched `mma_limbs.py` runs.

**The premise is measured, not proved.** `A.sigBits` per SKU comes from a Fasi-style probe
(Fasi, Higham, Mikaitis, Pranesh 2021), and it enters the receipt's assumptions, not the kernel.
The governance consequence:
- At `sigBits = 24`, blocks of up to 262,143 products fit, so the design is practical.
- At `sigBits = 14`, blocks are capped at 255, so an off-MMA reduction is needed every 255
  products. Point (a) of the alignment map is then probably dead on that SKU. The kernel cannot
  decide this; the probe decides it.

**Witness and falsifiers.**
- Witness: one product `8 × 8` with zero init at `sigBits = 7` (64 < 2^7).
- Falsifier 1: nonzero initial accumulator.
- Falsifier 2: `sigBits = 6` with `xs = [8], ys = [8]`, so 64 ≮ 2^6. The theorem's hypothesis fails,
  and a truncating `addStep` really does lose the bit.
- Falsifier 3: unequal lengths, where `zip` truncates.

**Cost.** R2a and R2b take one to two weeks, since the `Int` theorems already exist and become
the specification side. The probe takes a GPU-day on rented spot capacity. That is not a Mac
job; hbox has no GPU.

---

## What these repairs buy the governance lattice

- **R1a** gives obend a universal hardware statement for a real kernel step. It is the first
  instance of `rtl_refines` from the alignment map (d) that is not a fixture table.
- **R2** turns the FP4 claim into `exact` on the lattice's exactness axis, conditional on a
  measured premise that is listed in the receipt.
- Neither repair is needed for the choke-point device (`experiments/chokepoint-step`). They are
  the silicon end of the same chain.
