# Silicon-to-semantics alignment: the co-design map (2026-11-05)

Status: design map. Tags: [READ] inspected source; [MEASURED] reproducible count or run;
[SOURCED] cited, not reproduced; [INFERRED]; [PROPOSED]. Companions in degg-research:
`research/GOVERNANCE-CLAIM-LATTICE.md` (the claims these constructions serve),
`research/governance-foundations-critique.md` (W1-W11: what the foundations actually prove today),
`research/governance-codex-synthesis.md` (two adversarial rounds with gpt-6-astra and what they
changed), `experiments/mma-field-mapping/` (counts experiment).

## Thesis, and the correction to it

The ambition: **one semantics, from gates through AIR through a kernel to the receipt a regulator
checks**, so that "the device did X" and "the proof says X" are about the same X by definition,
not by a differential test.

The correction, forced by the critique and by Codex. One Lean definition generating three
artifacts gives *three identically wrong implementations* if the definition is wrong, and it
gives nothing at all if the three outputs have no refinement theorem to the definition. So the
aligned stack is not "one source". It is a chain of **typed obligations whose statements share
subjects**:

```
  gates  ──refines──▶  RTL semantics  ──refines──▶  Lean function f  ◀──denotes──  AIR descriptor
    ▲                                                   ▲                              ▲
 installation (T4)                           Claim.predicate mentions f       verifier accepts ⇒ relation
    │                                                   │                              │
  coverage premise ───────────────▶  receipt = (subject, f, window, tier, eps, assumes)
```

Every arrow is a theorem or a named assumption, never a diagram edge. The design points below are
the places where two or more of these arrows can be made to share an object, so that one theorem
does the work of two.

Who is near the whole stack [SOURCED]:
- **FlexHEG** (Petrie et al., ARIA-commissioned report v2, arXiv 2506.15093 and 2506.03409):
  a Guarantee Processor plus a Secure Enclosure, with updateable verification.
- **Lucid's validation cluster:** Assurance Node, VJM, SmartNIC gateway.
- **Peigné et al. 2606.05433v3:** TAP on inter-node links, or an attested SmartNIC, with per-step
  Poseidon Merkle roots.
- **IETF draft-das-ai-factory-silicon-finality-02:** "execution finality" enforcement profiles for
  GPUs, DPUs, RDMA, CXL and photonic boundaries. Read only the title and abstract.
- None of them carries a machine-checked statement from the device's step function to the
  receipt's predicate. That is the unoccupied point. It is narrow, and it is real.

---

## (a) One MMA datapath: inference arithmetic, STARK field arithmetic, FHE transforms

**Design point.** One tensor-core instruction stream serves three things:
- MXFP4 inference;
- prime-field dot products for sumcheck and LDE, via limb decomposition;
- RNS/NTT arithmetic for FHE.

It comes with a machine-checked exactness side condition that names the accumulator.

**Who is near.**
- TensorZKP (USENIX Security '26, ePrint 2026/1250) [SOURCED, lit notes]: BabyBear, UINT8 limbs
  into INT32 MMA, N < 33,025 per exact block, a 2^25-gate HyperPlonk/Brakedown proof in 215 ms on
  an H100.
- CROSS (HPCA'26) and MORPH (DAC'26): FHE and ZK as INT8 GEMMs on TPU v6e (from
  `zkml-research/docs/HARDWARE.md`) [SOURCED].
- Fasi, Higham, Mikaitis, Pranesh (2021) measured non-IEEE tensor-core accumulation.
- "Formal proof for delayed finite-field arithmetic using floating-point operators" (2007,
  cs/0703026, Codex's citation) occupies the *proof* of FP-exact modular arithmetic, before tensor
  cores existed.
- Ours: `obend/lean/Obend/Hardware/Accelerators.lean`, Ozaki base-13 over Int [READ, critique W2].

**What we measured [MEASURED, `experiments/mma-field-mapping/RESULTS.txt`].**
- The model reproduces TensorZKP's N < 33,025 exactly.
- FP4-E2M1 base-13 balanced limbs need 9 limbs and 81 limb-products per BabyBear multiply, against
  16 for INT8.
- So FP4 is worth it only on a SKU where TOPS(FP4)/TOPS(INT8) > 5.06. FP8-E4M3 needs > 4.00.
- Exact block lengths for FP4 limb pairs: 116,508 under a 24-bit accumulator; 113 under a 14-bit
  truncated accumulator (the precision DeepSeek-V3 reports for H800 FP8 GEMM [SOURCED]).
- Codex's attack, accepted: this is a schoolbook operation count, not a performance threshold. It
  ignores reduction cost, layout and memory. It is a necessary condition, not a sufficient one.

**So the design point is SKU-conditional, and that is the interesting part.** Vendors are
shifting tensor throughput toward FP4/FP8 and away from INT8 [INFERRED from the direction of
Blackwell-Ultra marketing; check per-SKU datasheets before quoting a number]. Once
TOPS(FP4)/TOPS(INT8) crosses about 5, the proof arithmetic should move onto the same FP4 pipe the
inference runs on. At that point "the hardware that served the model" and "the hardware that
proved it" are the same functional unit, under one accumulator model. The aligned claim this
enables: **a sampled-recompute or a proof that runs on the same pipe, in the same formats, as the
served inference, so exactness (lattice §0.2) is a property of one datapath and not a
cross-platform hope.**

**Theorem that makes it a construction [PROPOSED].**
```
structure AccModel where m : ℕ        -- significand bits; truncating alignment
def hwMma (A : AccModel) : List (FP4 × FP4) → Acc   -- per-instruction semantics, block scale, order
theorem ozaki_exact_under_acc (A : AccModel) (xs ys) (hrep : ∀ d ∈ xs ++ ys, fp4Representable d)
    (hN : xs.length * 144 < 2 ^ A.m) :
    toInt (hwMma A (xs.zip ys)) = kulischDot xs ys
theorem field_dot_via_mma (p) (hp : p = babyBear) ... :
    reduceMod p (recombine13 (limbwise (hwMma A) ...)) = fieldDot p u v
```
Codex round 2 adds the missing hypotheses. `AccModel` must specify more than significand width:
- rounding, alignment, block-scale and exponent limits;
- zero initialisation and the accumulation schedule;
- equal-length inputs (`zip` silently truncates);
- and the bound must make every intermediate alignment and addition exact, not just the final
  sum.

`field_dot_via_mma` also needs canonical representatives, a proof that limb decomposition
reconstructs each operand, exact or width-proved recombination, and a proved modular reduction.
Primality plays no part in the identity; it only matters for calling the result a field element.

Codex is also right that measurement cannot *prove* an undocumented accumulator model. The honest
statement takes `A` as a premise, and the per-SKU probe is T3 evidence for that premise. It goes
in `assumes` (lattice §0), not into the proof.

**Cost.** The Lean work is small: the Int theorems exist, so what remains is a bounded-accumulator
refinement. The GPU probe is a day on any H100/B200. The kernel is TensorZKP-sized work, so compose
with theirs rather than rebuild it.

**First experiment.** A Fasi-style accumulator probe for FP4/FP8 MMA on one Blackwell SKU (rented
spot). It answers `m`, and therefore whether the 116,508 or the 113 column is the real one. Until
then, (a) is a hypothesis.

## (b) A verified in-path receipt device: commit before forward

**Design point.** A device on every egress path of a job or facility:
- an Orb-style emitted loop;
- running as a seL4 Microkit PD on a CHERI or RISC-V core, or as obend-lowered RTL on an FPGA;
- committing each *forwarded* frame's header, a payload digest and the current VJM root into an
  MMR *before* the frame leaves.

The receipt the device signs is the MMR root. The theorem is about the device's step function.

**Who is near [SOURCED].**
- **FlexHEG Guarantee Processor:** the concept, without a statement.
- **Peigné tier 2:** an attested SmartNIC/DPU exporting a root.
- **Lucid:** the SmartNIC gateway consumes the VJM.
- **TrInc (NSDI'09):** trusted monotonic counters as the minimal trusted hardware for
  non-equivocation.
- **VRASED (USENIX Sec'19):** a formally verified hybrid remote attestation architecture, the
  closest "verified tiny trusted device" precedent.
- **PeerReview (2007):** accountable execution through tamper-evident logs.
- **seL4:** functional correctness proofs for Arm, RISC-V and x86 kernels.
- **CHERI-seL4 / CHERI-Microkit:** released (CHERI Alliance).

**What we have [READ, critique W3/W6/W10].**
- A proved, emitted, byte-pinned Pancake function: a two-branch HTTP responder, demo-gated in the
  dataplane.
- A seL4 PD that verifies its own STARK, with no working network.
- MMR non-omission statements in Lean.
- Nothing that states coverage.

**Codex's attack D2, accepted in full.** Dense positions do not prove coverage: drop the packet
before numbering it. Headers do not bind payload or job. Power loss between forward and durable
log breaks "every frame". "Every *arriving* frame" is impossible with finite storage and
unrestricted arrival. So the statement is about *forwarded* frames, and refusal is an explicit
output.

**Theorem that makes it a construction [PROPOSED].**
```
-- the device is a step function over (state, input event) with outputs {forward f, refuse f, persist leaf}
theorem commit_before_forward (σ₀ : DevState) (evs : List Event) :
    let (σ, outs) := run step σ₀ evs
    ∀ f, forward f ∈ outs →
      ∃ i, (persisted σ)[i]? = some (leaf f σ.vjmRoot) ∧ persistIdx i < outIdx (forward f)
theorem leaf_binds (f) : leaf f r = H (hdr f ‖ H(payload f) ‖ r)        -- payload-bound, job-bound
theorem overflow_refuses : logFull σ → ∀ f, step σ (arrive f) = (σ', [refuse f])
theorem reboot_continuity : resume (persisted σ) = σ' → mroot σ'.log = mroot σ.log   -- no fork on reboot
-- with the existing MMR theorem, a window query over the device's root cannot omit a forwarded frame
-- (omission ⇒ collision). Coverage = commit_before_forward + the T4 premise "no bypass path".
```
**The sketch above is false as written (Codex round 2).** Its problems:
- it binds earlier frames to the *final* VJM root;
- repeated identical frames can share one witness;
- arbitrary initial states need not satisfy the invariants;
- `leaf_binds` is a definition, not a theorem;
- `overflow_refuses` leaves σ′ unbound and is vacuously satisfied by a device that always refuses;
- `reboot_continuity` is either trivial or false, because an old valid snapshot reproduces its own
  root while rolling history back.

Corrected statements:
- **`commit_before_forward`.** From a valid initial state, every forward *event occurrence* has a
  distinct, earlier durable-commit event. That event contains the occurrence's identifier, its
  bytes digest, the epoch, and the VJM root *at admission*. The commitment stays covered by the
  authenticated durable history through permitted crashes and compaction. This proves forwarding
  coverage, not delivery.
- **`leaf_binds`.** The encoding is injective, length-delimited, domain-separated, and includes the
  job/session id. Two unequal records opening the same leaf yield a collision in the outer hash or
  the payload hash. This is a reduction, not unconditional injectivity.
- **`overflow_refuses`.** Under insufficient reservable durable capacity, arrival `j` emits
  `refuse j`, creates no pending authorization for `j`, and cannot later forward `j` without a fresh
  admission. A companion theorem shows that a non-full execution does forward, so that permanent
  refusal does not satisfy the safety claim vacuously.
- **`reboot_continuity`.** Recovery reconstructs the durable prefix selected by a non-rollbackable
  epoch/counter anchor (TrInc-style), preserves every previously authorized forward, and resumes
  with fresh identifiers. Older snapshots, or an ambiguous recovery, cause refusal.

The bypass paths (a second NIC, NVLink and intra-node fabric [Peigné OP-10], management ports)
are enumerated in `assumes`. Each one is an installation-audit item.

**Cost.**
- The step function is small: a Poseidon2 or Blake3 absorb plus an MMR append, much smaller than
  the HTTP parser Orb already proved.
- The hard parts are durable persistence (a monotonic counter, TrInc-style, so a reboot cannot
  fork) and line rate.
- Line rate is not a Pancake loop at 400 Gb/s. At rate, (b) is FPGA RTL, which is why (d)
  matters.

**First experiment.** Lower `commitFrame` (MMR append over Blake3 compression with fixed-size
headers) through the existing Pancake emitter. Prove `commit_before_forward` for the
single-frame step. Replace the demo-gated `serve` with it behind the same flag. Measure frames/s
on the Mac. This is the smallest thing that turns lattice X-6 from "none" into "T2 for the
device step function".

## (c) Attestation and proof under one typed statement, with the residual-trust theorem

**Design point.** TEE quotes (CPU TD, SNP, the NVIDIA GPU report) and STARK proofs are *both*
evidence for one `Judgment` (lattice §0). Each opens the same typed statement:

```
Stmt := (device_epoch, session_key, program_digest, model_commitment, input_root, output_root, policy_id)
```

The quote's `report_data` commits `H(Stmt)`. The proof's public input is `Stmt`. The log is where
both are found, not what joins them.

**Codex's attack D3, accepted.** Co-location in an MMR creates no conjunction. A valid GPU quote
beside an unrelated valid proof both verify. The join is the shared `Stmt`, and the verifier
checks that both evidence items open the same one.

**Who is near [SOURCED].**
- RA-TLS (2018): attestation bound into the TLS channel.
- Automata DCAP and datachainlab zkdcap: DCAP quote verification inside RISC Zero/SP1 zkVMs.
- RFC 9334 RATS: evidence, appraisal policy and attestation results separated.
- No ZK verification of an NVIDIA SPDM/RIM report turned up in one search (that proves nothing
  either way).

**The theorem that says why both [PROPOSED].** The executable form is the residual-trust
enumeration with three arms (critique W5 repair):
```
admissible(public ∧ owners)                    = 377   [MEASURED today, includes the honest run]
admissible(... ∧ quote opens Stmt) | TEE sound = 1
admissible(... ∧ quote opens Stmt) | TEE broken= 377
admissible(... ∧ proof opens Stmt) | sound     = 1      regardless of TEE
```
**The Lean statement, corrected in round 2.** Define `Res(E, A) = {w ∈ Ω | A w ∧ E w}` over *one*
world space. Then `Res(E₁ ∧ E₂, A) = Res(E₁, A) ∩ Res(E₂, A)` is definitional, so it is not the
theorem. It also fails for *projected* subjects, where two pieces of evidence can admit the same
subject with incompatible hidden witnesses. Projection gives only inclusion.

The content theorems are the per-leg *interpretations*, and those are where the work is:
- The proof leg's residue on the output predicate is independent of the TEE assumptions.
- The TEE leg is the only one that can carry **occurrence** (lattice O-1: it ran here, now, on
  enrolled silicon) and **confidentiality** (C-1).
- Putting `H(Stmt)` in `report_data` does *not* by itself establish execution, occurrence or
  confidentiality. That needs the measured code's semantics, which is a separate premise.
- A shared commitment does not make the two assumption sets disjoint.

So "why both" is a pair of interpretation theorems over disjoint *predicates*, not a set
identity.

**Cost.**
- A `Stmt` schema.
- An NVIDIA GPU verifier in tee-verify (critique W4).
- Two new arms in `residual_trust.rs`.
- In-circuit DCAP verification is optional and expensive (zkVM-scale). The cheap version verifies
  the quote natively and puts `H(quote)` in the proof's public input.

**First experiment.** The two `residual_trust.rs` arms (hours). Then parse a public NVIDIA CC
report sample into a `GpuEvidence` struct (a day, no GPU needed).

## (d) One Lean function, three refinements: AIR, Rust, RTL

**Design point.**
- One Lean function `f` (for example the Poseidon2 S-box `x ↦ x^7 mod p`, or the `commitFrame`
  absorb of (b)).
- Three implementations, each with a refinement theorem to `f`:
  - the AIR descriptor, via the Dregg2 IR-v2 emitter, with `sat ↔ graph f`;
  - Rust, via an `@[export]`ed Lean object (the `dregg_deleg_admit` pattern), or via a proved
    interpreter;
  - RTL, via obend `compileBookToRtlSat`, with `evalModuleOutputs = f`.
- Then the in-path device of (b) computes `f` in gates, the proof about the device's log is a
  proof about `f`, and the receipt's predicate names `f`. They agree by refinement to one object.

**Codex's attack D4, accepted.**
- One source can generate three identical wrong implementations, so the theorems must be
  refinement to `f` *and* `f` must be the right spec.
- Clocked RTL also needs stalls, reset and memory-ordering semantics that `evalModuleOutputs`
  (combinational, critique W1) does not have.
- Codex proposed the alternative: **translation validation** (Necula PLDI'00) of independently
  produced artifacts by a small checker, which removes trust in the generators. That is the better
  default whenever a vendor's RTL is involved, because we will never generate Nvidia's or
  Xilinx's IP.

**Who is near [SOURCED].**
- Kami (ICFP'17): Coq, Bluespec-style, verified hardware generation.
- Cava/Silver Oak (Google, Coq to SystemVerilog, used for OpenTitan AES).
- CakeML: verified compilation.
- zksecurity's **clean**: a Lean 4 DSL for formally verified ZK circuits. This is the nearest Lean
  competitor to our Lean-authored AIR law, and it has no RTL leg as far as its announcement says.
- ZK-CEC (arXiv 2601.11173): zero-knowledge proofs of combinational equivalence between a
  *secret* circuit and a public spec. See (h).
- The unoccupied point is the *join*: a Lean function whose AIR and RTL refinements are both
  theorems, consumed by one receipt.

**Theorem [PROPOSED].**
```
-- corrected (round 2): correct endpoints do not make wrong intermediate columns satisfy the AIR
theorem air_denotes (e : SupportedAst) (x y) : (∃ aux, Sat (emitAir e) x y aux) ↔ y = denote e x
theorem air_sound   (e : SupportedAst) : ∀ x y aux, Sat (emitAir e) x y aux → y = denote e x
--   (+ range checks and the field-to-BitVec interpretation; f must be supported syntax, not any Lean fn)
theorem rtl_refines (e : SupportedAst) (m) (h : compileBookToRtlSat (bookOf e) = some m) :
    ∀ x, wellFormed x → evalModuleOutputs m (env x) = [(o, denote e x)]
--   combinational only; a clocked device needs sequential trace refinement under explicit reset,
--   handshake and memory assumptions, covering output order and no spurious outputs
theorem receipt_means (r : Receipt) (h : verifyReceipt r) : r.claim.predicate = Pred.graph f ...
```

**Cost.** The S-box is small enough to be a one-week experiment with `bv_decide`. A Poseidon2
permutation in RTL with sequential semantics is a quarter. It also forces the obend word-level
(BitVec) layer that `zkml-research/notes/hpu-seam-study.md` already says `fhegg-rtl` needs.

**First experiment.** `x ↦ x^7 mod BabyBear`:
1. Lower it through obend `compileBookToRtlSat`, proving `rtl_refines` by `bv_decide` at 32 bits.
2. Emit its AIR through the IR-v2 emitter (the Poseidon2 chip already exists).
3. State `air_denotes` against the same `f`.

If obend's lowering cannot carry a `mod p` multiply, the RTL leg of this map is research, not
engineering. That is worth knowing first.

## (e) Confidential-GPU E2EE sessions whose transcript commitment is the audited object

**Design point.** The ML-KEM-768 session of `dregg-chutes-e2ee` [READ] gives confidentiality.
Make the *ordered application-record transcript* the governed object:
- client and enclave each maintain an MMR over (seq, H(ciphertext), H(plaintext-response));
- the measured endpoint signs the terminal root;
- equivocation between the two roots is detectable by anyone holding both.

A provider can then prove "served exactly these n requests to this client, in this order, with
these outputs" without seeing plaintext, and the auditor's sample (T3) is drawn from the
transcript positions.

**Codex's attack D5, accepted.** ML-KEM supplies key establishment, not endpoint authentication,
transcript completeness, inference correctness or PQ attestation signatures. A commitment
authenticates nothing unless anchored. So this needs:
- an AKE (the TD quote binds the KEM public key, which our attest gate does [READ]);
- session-bound ordered records;
- an explicit truncation rule.

The quote signatures (ECDSA, from Intel/AMD/NVIDIA roots) are not post-quantum, whatever the KEM
is. Say so on the receipt.

**Who is near [SOURCED].** RA-TLS. Lucid AI Passports (a signed receipt per inference). Tinfoil
(attested inference enclaves).

**Theorem [PROPOSED].**
The first sketch conflated recorded and executed (Codex round 2). Corrected:
- **Record agreement.** Authenticated roots that bind the same session, length and canonical
  record schema imply record-by-record agreement, except with binding failure.
- **Execution and delivery.** Verified endpoint transitions connect records to execution and to
  acknowledged delivery. This is a separate theorem.
- **Truncation.** Detecting it needs a previously agreed terminal obligation and a deadline. A
  shorter prefix on its own is not misconduct.

**First experiment.** Add the per-session MMR to `dregg-chutes-e2ee` on the client side only, and
check it against a mock enclave that drops or reorders one record.

## (f) FHE/ZK "joint modulus" as a hardware statement: demoted

**Correction first.**
- Codex's attack D6 and our own seam study (`zkml-research/notes/hpu-seam-study.md` [READ]) agree.
- A common modulus is neither necessary for one NTT core nor sufficient for FHE: FHE needs RNS
  chains, noise bounds, key switching and negacyclic transforms.
- Zama's `ntt_core_gf64` has no multipliers: its twiddles are shifts, using ord(2)=192 in
  Goldilocks, which only reaches 192nd roots of unity. So a large STARK LDE cannot reuse its
  butterflies without generic twiddle multipliers.
- The HPU's ciphertext ring is Z/2^64, and Goldilocks is only its transform field.

**What survives as a design point.** The HPU's `ntt_acc_modsw` tap (409.6 GB/s, coefficient
domain, with free MLE framing) makes **audit-sampled proving of FHE execution** a *bandwidth
necessity* ("100%-proving is physically impossible at the tap"). So the hardware statement is
not "one modulus". It is "one memory system, a sampled tap, and the sampling theorem's q priced by
the tap rate". Concretely: AuditSampling's `q` becomes a function of the tap's FIFO budget, and
the claim is a T3 FHE-execution claim with an eps the hardware sets.

**Who is near [SOURCED].**
- F1 (2021) and Trinity (2024): programmable or shared FHE/crypto datapaths.
- UniZK (ASPLOS'25), the unified RISC-V vector NTT framework for FHE and ZKP (TCHES), and a
  unified NTT/MSM accelerator (TCHES).
- No FHE vendor claims STARK/Poseidon2 support (Zama HPU, Niobium, Optalysys; lit notes).

**Theorem [PROPOSED, corrected in round 2].** My first sketch pointed the wrong way. A capacity
ceiling cannot supply a detection-probability *floor*. The two halves are:
- **Feasibility (an upper bound on p).** Sustainable sampling at rate p requires
  `p · B_tap ≤ B_engine`.
- **Assurance (a floor on detection).** Under unpredictable selection and a service guarantee
  covering bursts and FIFO behaviour, every bad item is detected with probability at least
  `max(0, p(1−ε_chk) − ε_bind − ε_beacon)`.

Without the service guarantee, overload can selectively discard every useful audit, which is the
fail-open attack done in hardware. The value is still that a hardware number enters a governance
ε, but only through both halves.

**First experiment.** The rate/area spreadsheet that `HARDWARE.md` already lists as step 2, now
with its output fed into `AuditSampling.params`.

---

## (g) New: the attested choke point (coverage without a physical TAP)

**Design point.**
- Inside a confidential VM or TD, make the *only* network path a measured seL4 PD or virtio
  backend running the (b) step function.
- The TD quote's RTMRs measure that PD image.
- Then the coverage premise (lattice X-6) splits:
  - "no bypass inside the TD" is attested (T1): the measured image has one NIC and the device
    model allows no other;
  - "no bypass outside" is physical (T4).
- That converts most of Amodo workstream 12 (TAP installation, not on track) into an attestation
  statement, for the jobs that run in TEEs.

**Who is near [SOURCED].**
- Peigné tier 2 (attested SmartNIC).
- Lucid's SmartNIC gateway.
- FlexHEG (Guarantee Processor in the enclosure).
- What differs here: the choke point lives *inside* the attested boundary, and its step function
  carries the (b) theorem.

**Attack.** The TEE.Fail-class physical attacks extract the TD's keys, after which the attested
image is a fiction. And the GPU's own DMA path is a second egress unless TDISP/IDE is on. TDISP is
not shipping on a documented 2026 B200+TDX stack [SOURCED].

**First experiment.** Boot a Microkit image whose only device is virtio-net (M3, the wall
`sel4/README.md` names) running `commitFrame`. Record the measurement the image would produce.

## (h) New: zero-knowledge equivalence of vendor RTL to the public receipt function

**Design point.**
- The in-path device in a real facility will be vendor silicon (a DPU, a SmartNIC), whose RTL the
  vendor will not publish.
- The vendor proves, in zero knowledge, that its secret netlist is combinationally equivalent to
  the public `commitFrame` RTL of (d) (ZK-CEC, arXiv 2601.11173).
- It then commits the netlist hash into the device's attestation measurements.
- The regulator gets "the device computes the public function" without the IP.

This joins (d), (b) and ZK into one claim: (vendor attestation ∧ ZK equivalence ∧ public
refinement theorem) ⇒ the device's step is `f`.

**Who is near [SOURCED].** ZK-CEC is the primitive, aimed at IP-vendor trust. Not found in one
search: its use as a governance receipt for in-path devices.

**Attack.** The equivalence covers the netlist the vendor proved, not the netlist fabbed or
loaded (a bitstream-swap or supply-chain substitution). The FPGA variant can bind the bitstream
digest through DPR authentication; obend has a frame-digest refusal theorem,
`dpr_corrupt_crc_keeps_tile_isolated` [READ, name only]. An ASIC needs T4.

**First experiment.** None cheap. A paper-level design note, plus asking whether ZK-CEC handles
sequential circuits (the abstract says combinational).

## (i) New: claim-carrying receipts (the X-8 receipt format)

**Design point.**
- The receipt *is* a serialized `Judgment` (lattice §0): subject, predicate AST, window, tier,
  eps, assumes, evidence references.
- A Lean-decided `@[export]` verifier (the `dregg_deleg_admit` pattern, which is T2\*) computes the
  meet, refuses inconsistent assumption sets, and prints the residual `assumes`.
- RFC 9334 Attestation Results and the IETF AR4SI trustworthiness vectors are the nearest formats.
  They carry appraisal *outcomes* per trustworthiness dimension, not assumption sets or soundness
  errors [SOURCED, from familiarity with the drafts; recheck].
- CryptoVerif already produces concrete bounds in terms of primitive assumptions and session
  counts (Codex round 2). The expressiveness is occupied. What is new is using the judgment as the
  operational receipt that parties exchange and compose.

**Theorem [PROPOSED, corrected in round 2].** Acceptance cannot imply `Holds` deterministically
when ε > 0, and `verify` may accept everything. The statement is the composition rule of lattice
§0. For every adversary in a common experiment satisfying `A₁ ∪ A₂ ∪ B`, if `Pr[accᵢ ∧ ¬Pᵢ] ≤ εᵢ`
survives composition and `Bind` fails with probability at most `ε_b`, then `Pr[acc₁ ∧ acc₂ ∧ bind
∧ ¬(P₁ ∧ P₂)] ≤ min(1, ε₁+ε₂+ε_b)`.

The receipt verifier must also deduplicate evidence by identity, since composing a receipt with
itself doubles ε. The anti-vacuity witnesses are a verifier that rejects a forged binding, and a
pair whose composition is refused because the binding fails.

**First experiment.** Write `Judgment` and the composition rule in Lean (an afternoon). Encode three lattice rows,
M-2 ∧ M-4 ∧ Q-2, and check the meet's computed `assumes` against the prose in the lattice.

## (j) New, from Codex, adjudicated

Codex proposed six constructions (`governance-codex-synthesis.md` §1). My adjudication:

- **Proof-checked accelerator cutpoints** (Slalom, 2019): nonlinear ops in a TEE, linear blocks on
  the GPU checked by post-commitment Freivalds challenges. **Adopt** as the near-term inference
  design: it is lattice M-2 at T2-for-linear plus T1-for-nonlinear, and Freivalds is already our
  boundary tool. Note that it is 2019 prior art, not ours.
- **Device-bound consumable execution leases** (TrInc + macaroons): burn a monotonic-counter lease
  before releasing a result. **Adopt**: it is the repair of `dregg_deleg_admit`'s missing counter
  authority (critique W11) and gives lattice O-2 (once-only).
- **Per-artifact translation certificates** (Necula): **adopt** as the default for vendor
  artifacts (see (d), (h)).
- **Optimizer-state lineage capsules:** **adopt** into lattice L-1.
- **Proof-gated FHE decryption with a persistent DP budget** (PINQ plus verifiable computation):
  **adopt as a separate track**. It is the right governance object for *data* provision (query
  release under a budget). Prior art is heavy (PINQ 2009; verifiable DP work), so no novelty claim.
- **Leakage-preserving accelerator sharing** (SecVerilog): **adopt as a constraint on (a)**. If one
  datapath serves inference, proof and FHE tenants, it is also a side channel between them. That
  is the strongest argument *against* (a) as a multi-tenant design, and it belongs in (a)'s
  `assumes`.

## (k)-(n) New, from Codex round 2: silicon facts that remove a trusted party

Each one removes a party the regulator would otherwise have to trust. Each is adopted as a
direction; none is a novelty claim. Adjudication notes are mine.

- **(k) Retirement counters, giving accountable compute units (lattice H-2, O-3).**
  - Mechanism: couple accelerator completion signals to a protected counter weighted by
    instruction shape and active lanes. Prove that counter increments equal completed
    architectural operations, including retries, cancellation and reset.
  - Removes: trust in host utilization telemetry.
  - Nearest: RVFI (riscv-formal's retirement interface).
  - First experiment (laptop): model-check a tiny vector-MAC engine with stalls, then inject an
    unmetered completion path.
  - My note: this is the most direct answer to Ansari M5 / Peigné OP-22, and obend's RTL path is
    where we could state it. It measures operations executed, not useful ones.
- **(l) Authenticated memory reads, giving training-data provenance (lattice L-1, N-1).**
  - Mechanism: tag immutable dataset pages with (dataset root, record index, version), carry the
    tags through DMA and caches to the operand boundary, and prove that every consumed sample opens
    the declared dataset.
  - Closes the gap that breaks claim 2 of the lattice: absence proved over D while the model was
    trained on D′.
  - Nearest: AEGIS authenticated memory.
  - First experiment: a simulated loader and cache, attacked with stale pages, DMA remap and
    post-verification mutation.
- **(m) Key epochs in the memory controller, giving bounded retention (lattice H-5).**
  - Mechanism: a teardown state machine drains writes, clears plaintext buffers and destroys every
    epoch-key derivation path, with no rollback.
  - Claim: post-teardown confidentiality of retained ciphertext, under a no-prior-copy premise.
    This is not universal erasure.
  - Nearest: cryptographic erase, NIST SP 800-88r2.
  - First experiment: exhaustively explore a small controller model with outstanding DMA, reset and
    crash.
  - My note: this is the only route I have seen to H-5 above T4.
- **(n) PHY-timed distance bounding, giving enrolled-device proximity (lattice W-2).**
  - Mechanism: rapid challenge-response bound to a non-exportable device key and the receipt's
    execution epoch, with the bound derived from timing, clock error and fraud probability.
  - Nearest: UWB distance bounding (Tippenhauer et al., WiSec'15).
  - First experiment: a timed simulation with relay, early-response guessing and clock skew.
  - My note: this is strictly stronger than sovcert's ICMP/QUIC RTT, which bounds network paths
    rather than PHY response.

---

## Ranking: the five most ambitious alignments, each with its make-it-real theorem

1. **(b)+(g) Commit-before-forward at an attested choke point.**
   `commit_before_forward ∧ leaf_binds ∧ reboot_continuity` over the device step function. It turns
   every completeness claim (N-*, H-4, A-3) from "nothing in the log" into "nothing forwarded
   un-logged, except through enumerated bypasses".
2. **(c) Attestation and proof opening one `Stmt`.** Two interpretation theorems: the proof leg's
   output-residue is independent of the TEE assumptions, and only the TEE leg carries occurrence
   and confidentiality. Both are executable as enumeration arms over one world space. The set
   intersection is definitional and is not the theorem. It is the precise answer to "why both".
3. **(a) One FP4 datapath with a named accumulator.** `ozaki_exact_under_acc A`, with `A` measured
   per SKU. It holds only where TOPS(FP4)/TOPS(INT8) > 5.06 [MEASURED threshold], so the design
   point moves as vendors cut INT8.
4. **(d)+(h) Lean function → AIR + RTL, plus ZK equivalence for vendor netlists.** `air_denotes f ∧
   rtl_refines f`, plus ZK-CEC binding a secret netlist to the public RTL. The regulator's
   predicate, the proof's relation and the gates are one `f`.
5. **(i)+(l) Judgment-carrying receipts over authenticated data reads.** The §0 composition rule,
   with a binding leg, as a Lean-decided verifier. Paired with (l), it is the only route I found to
   lattice claim 2 that survives the D-versus-D′ attack. Every other item above becomes
   *composable* by a relying party who did not build it.

## What I would not do

- (f) as originally phrased. "Joint modulus" is the wrong hypothesis. Keep the sampled-tap
  version.
- Any construction that claims a first before the prior-art lines above are read in full. FlexHEG
  v2 Part II especially may already state device-level guarantees we would be restating.
- Growing `fhegg-rtl` gate-wise (the seam study's verdict stands).
