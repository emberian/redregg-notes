# Lean v4.30.0 -> v4.34.1 full-closure trial (BURN-LEAN434)

Lane `/srv/lanes/lean434-trial/src` on burst2-b, branch `lane/lean434-trial` (pushed to burst2-a:/srv/git/minidregg.git, tip c041190d), from green cfdaf64d.
Toolchain v4.34.1, Mathlib `d13f23b7` (the v4.34.1 tag rev the earlier trial used; `lake update mathlib` clean, `cache get` hit all 8908 oleans, 0 Lake-config problems). Private Lake cache (`$LANE/lake-cache`).
Target per round: `lake build Minidregg +Host.Main:leanArts ObjectiveProofs` through lake-slot. Lake always keeps going past a failed module and builds everything not downstream of one, so each round is a full "keep going" build.
Logs: `/srv/lanes/lean434-trial/logs/round{1..32}.log`, `summary.txt`; copy at `work/burn/lean434-logs.tgz`. Tooling: `l434-fix.py` (log parser plus mechanical editor), `l434-loop.sh`, `l434-graph.py` (import-closure blocked count).

Nothing here is a proof repair. The "stub" rounds are a MEASUREMENT device (see below), not a fix, and the branch must not be landed.

## 1. Failure counts per round

Import closure of the three targets is 1298 modules (my import-graph count; Lake's own job count differs).

| round | what changed | failed modules | error lines | modules blocked behind failures | closure modules clean and not blocked |
|---|---|---|---|---|---|
| R1 | none (pure bump) | 31 | 144 | 1075 | 192 |
| R2 | re-pin 40 `#guard_msgs` axiom pins | 32 | 132 | n/a | n/a |
| R3 | re-pin 18 more (newly reachable) | 30 | 120 | 1042 | 226 |
| R4-R14 | sorry-stub erroring tactic lines/blocks, comment out consequent `#assert_axioms` (11 rounds) | 24, 18, 18, ... stuck at 18 | 108 -> 59 | 994 | 286 |
| R15-R16 | decl-level stub (replace a failing theorem body by `by sorry`) | 18, 15 | 92, 147 | | |
| R17-R20 | repeated | 23, 19, 13, 12 (new modules become reachable as blockers clear, so the count is not monotone) | ~125 | | |
| R20-R32 | fixpoint: my tooling can no longer make progress | 12 | 122 | 953 | 333 |

Headline: the earlier trial's "28 fail, 1078 unchecked" was right to within a few. The pure-bump R1 number is **31 failed modules, ~1075 of 1298 unchecked behind them**. Even after every mechanical and stub round I could run, **12 modules still fail and ~953 modules stay unchecked.** The stub rounds uncovered about 140 more clean modules, and no failure in them that is not a mechanical kind, but the reachable fraction is still only about 26%.

Caveat on the stub fixpoint: some of the 12 are artefacts of my stubbing (Theory.ObjectiveBendDemandAdequacy cascades from stubbed definitions: `Unknown identifier graph_*`, `represented : sorry is not an inductive datatype`; Compiler.EmitSerialize fails only because `#eval` depends on a stubbed sorry). Treat the stub rounds as a lower bound for reachability, and the 12 as an upper bound of real hard modules. A real count of genuinely hard modules is around 9-10 (list in section 5).

## 2. Mechanical fixes applied (all logged in git history of the lane)

| fix | count | commits |
|---|---|---|
| `#guard_msgs` axiom-set pins re-pinned to v4.34.1's output (docstring only; the direction is almost all "now includes Classical.choice", plus a line-wrap reflow of the message) | 40 (R2) + 18 (R3) + 3 + 27 (later rounds) = ~90 | 16d7df0c, 31d439dc, stub rounds |
| `#assert_axioms` lines commented out because they are consequences of a stubbed sorry | 57 | stub rounds (measurement only) |
| tactic line or block replaced by `sorry` (measurement only) | 117 lines, 12 multi-line, 12 `by`-blocks | R4-R14 |
| declaration body replaced by `sorry` (measurement only) | 134 | R16-R25 |
| skipped as unsafe to edit automatically | ~49 unbalanced-bracket tactics; 25 decls with an error in the signature | |

Only the first row is a genuine fix (a repin). It is still not "free": 20 of the 60 R1 `#guard_msgs` failures contained `sorryAx` (consequences of an upstream failure, not a drift) and were deliberately not repinned. A repin of an axiom list that grows `Classical.choice` is a change to a stated assurance claim and should get a reviewer: the pins say, for example, `append_allowedBy_iff` now depends on Classical.choice where it did not. That is still within "the standard three" but it IS a loosening of the recorded pin.

Not done: 358 deprecation warnings in R1 (`if_false` 76, `dif_pos` 72, `if_true` 65, `if_pos` 40, `if_neg` 40, `cond_true` 33, `dif_neg` 18, `cond_false` 8) are non-blocking and I did not touch them. They are the only bulk-mechanical edit available (sed-able rename) and would be a part of any real upgrade.

## 3. Failures by error kind (R1, 144 errors in 31 modules)

| kind | count | examples |
|---|---|---|
| `#guard_msgs` pin mismatch | 60 | 40 are pure drift (an axiom list gaining `Classical.choice`, or wrapping across lines) e.g. `Theory/TypedAuthorization.lean:187` `[propext, Quot.sound]` now `[propext, Classical.choice, Quot.sound]`; 20 contain `sorryAx` (consequence of an upstream failure) |
| consequence of failures: `depends on axioms outside the standard three: [sorryAx]` from `#assert_axioms` | 27 | `Kernel/RefusalLane.lean:214` `Lane.refill_closed`; `Selvage.PS.polishchuk_spielman` |
| simp-set / simp normal form change ("After simplification, term ... Type mismatch") | 13 | `Theory/BinaryTowerFanPaar.lean:123` `(binaryTowerEmbed ..).toRingHom c` is now simp-normalised to `(binaryTowerEmbed ..) c`; `Kernel/GenericSimplexAuditProjection.lean:129`; 7 in `ObjectiveBendDemandAdequacy` |
| `simp` / `dsimp` made no progress | 9 | `Compiler/AirFlatten.lean:291` (x6); `Theory/Noun.lean:526` |
| rewrite pattern not found | 7 | `Theory/Confluence.lean:139` `Finset.mem_mk` against `Five.enumList` (a `{ val := ↑l, nodup := _ }` Finset membership now elaborates to a different shape); `Assurance/SemanticReceiptRelation.lean:51,142`; `Selvage/Depth.lean:519,1590` |
| `decide` failed / Decidable instance does not reduce | 8 | `Compiler/PredCompile.lean:1655,1659,1677`; `Selvage/Proximity.lean:1233,1295,1363,1380`; `Selvage/ZK.lean:427`. Instance unfolding changed; these are the `Decidable` reductions that stuck on `decEq` |
| unsolved goals | 6 | `Theory/Bignum.lean:193`; `Kernel/ObjectAudienceController.lean:57` |
| kernel deep recursion (31-bit prime `norm_num`) | 4 | `Compiler/BabyBear.lean:18`; `Theory/CyclotomicInertia.lean:122,124,126`; plus `Selvage/BabyBearExt4.lean:84` max recursion |
| failed to synthesize instance | 3 | `Theory/Channel/Lease.lean:303` `Decidable (cellAt 0 238 ∈ assembleByHeaderOnly ..)`; `Effects/EffectSpec.lean:376` |
| application type mismatch / Mathlib API signature change | 3 | `Selvage/PolishchukSpielman.lean:438` `IsPrimitive.dvd_of_fraction_map_dvd_fraction_map` argument shape changed |
| anonymous-constructor / elaboration change | 2 | `Theory/ZkmlTensorOps.lean:160` `⟨..⟩` on `List.Mem` now has more than one constructor; `Compiler/ObjectiveBendTermWire.lean:289` dependent elimination |

By the requested buckets: renamed decl = 0 hard errors (all renames are deprecations, warnings only; 358 of them); tactic behaviour / simp-set change about 29 (13 + 9 + 7); `decide` / reduction change 8; elaboration or instance change about 12; kernel recursion 4-5; Mathlib API change about 3; pin drift 60 plus consequences 27 (87, mostly mechanical or downstream); other 4.

The count of real independent breakages is therefore about 55-60 error sites, not 144; the rest are pins and sorry consequences.

## 4. Estimate (module counts; no hours)

- Direct failures: 31 modules in R1; 12 survive my stub fixpoint, about 9-10 of which are genuine (the rest are my own stubbing artefacts).
- Behind them: about 953 of 1298 closure modules were never reached, because the failing 12 sit near the bottom of the lattice (Theory.Noun, Theory.Confluence, Theory.ResourceCost, Selvage.Depth, SemanticReceiptRelation, DomainEpoch, FnWireGrammar...). Unknown unknowns there: the failure-per-module rate in the 333 reachable modules is 12/345 (3.5%) post-pins. Extrapolating that rate to the 953 gives roughly 30-40 more failing modules, with a wide error bar (the sampled modules are the Theory/ Mathlib-light layer, the blocked ones are Kernel/Host/Compiler-heavy and more simp-heavy).
- Expected total: about 40-50 modules need a hand edit; about 20 of the 40-50 are one-liner `rw` replacements or simp-set follow-ups.
- Dominant term: simp / rewrite normal-form drift in Mathlib-adjacent proofs (about 29 error sites in R1, and the dominant thing in `ObjectiveBend*`, which is also the most-edited family and has the heaviest merge pressure). Second: `decide` instances that stopped reducing (8; each needs `decide +kernel` or restating, and `+kernel` adds an axiom-accounting question). Third: the four 31-bit prime `norm_num` proofs that overflow the kernel stack (`Nat.Prime` of BabyBear/KoalaBear/Mersenne31 needs a `Nat.Prime` certificate, e.g. a Pratt chain or `decide +kernel`, not a bump of `maxRecDepth`).
- Governance cost beyond edits: the axiom pins move for about 90 declarations (all gaining `Classical.choice`); anything keyed to `#assert_axioms`/axiom census/gate ledgers will need re-baselining and a reviewer decision on whether "gains Classical.choice" is acceptable, since it is a silent loosening.

## 5. Hard set at fixpoint (to repair by hand first)

Theory.Noun (simp no progress, 526), Theory.Confluence (Finset mem rewrite, 137), Theory.ResourceCost (rewrite, 46), Assurance.SemanticReceiptRelation (rewrite, 45/127), Selvage.Depth (structure fields now missing, 505), Compiler.FnWireGrammar and Kernel.DomainEpoch (`have` type inference, 155 / 125), Theory.HyperdocumentOperations (structure instance fields, 396), Theory.ObjectiveBendTemplates (rcases / fields, 418/474/503), Theory.EpistemicConsensus and Theory.Confluence (multi-line `#guard_msgs` pins my script does not rewrite). Plus artefacts: Theory.ObjectiveBendDemandAdequacy, Compiler.EmitSerialize.

## 6. Cheapest next spike

A one-person edit pass over only the **6 `rewrite`/`simp` modules at the head of the lattice** (Theory.Noun, Theory.Confluence, Theory.ResourceCost, Assurance.SemanticReceiptRelation, Selvage.Depth, Compiler.FnWireGrammar) on top of `31d439dc` (R3, repins only; NOT the stub tip) plus the `if_*`/`cond_*` deprecation sed. That clears the lattice head; one more keep-going round then gives the true downstream failure count (my 30-40 extrapolation) at the cost of that pass plus one 1-minute-per-round replay. Do NOT start from the stub commits: they exist only to measure reachability. Resuming point: branch `lane/lean434-trial`; the commit to branch from is 31d439dc.

## 7. Decision recorded (ROOT, 2026-10-07)

Ember accepts the new `Classical.choice` dependencies. The re-baselining of the axiom pins (about 90 declarations, section 2) is approved for when the upgrade happens, so it is no longer a blocker or a reviewer question; the only remaining pin work is mechanical.
