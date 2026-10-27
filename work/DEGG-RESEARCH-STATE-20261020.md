# Dark Egg Research — state for ROOT

20 October 2026. Read-only Mac scout; no hbox access, build, test, or landing.

## Reading boundary

- READ (`/Users/ember/dev/degg-research/AGENTS.md`): this is a public research memory, not a production protocol or deployment repository.
- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md`): the transition handoff is a snapshot dated 18 August 2026.
- READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md`): the designated operational truth page still says “Last reviewed: 2026-08-18.”
- READ (`/Users/ember/dev/degg-research/README.md`): its later front-page summary includes the Clear energy oracle.
- READ (`/Users/ember/dev/degg-research/experiments/README.md`): its experiment inventory was updated 22 August.
- READ (`/Users/ember/dev/degg-research/filing/2026-08-cftc/README.md`): the filing set is a separate, later submission-build inventory.
- READ (`/Users/ember/dev/degg-research`, `git log --format='%h %ad %s' --date=short | head -60` and `git status`): HEAD is `03d1ee6` (27 August 2026); working tree was clean at inspection.
- INFERRED: treat the handoff, verdict page, experiment records, and later filing artifacts as dated evidence, not one synchronized release statement.
- READ (`/Users/ember/dev/degg-research/notes/README.md`, `notes/archive/README.md`): notes define a dated claim-status discipline; the archive preserves rejected or superseded work.
- READ (`/Users/ember/dev/degg-research/output/pdf/`): 59 local PDF files are present, including five `FILING-*.pdf` builds; filename alone is not a submission receipt.
- READ (`/Users/ember/dev/degg-research/LICENSING.md`): original material is AGPL-3.0-or-later; sibling material and third-party work retain separate rights.

## Thesis, in the files' words

> “The central bet is that a useful market or confidential operating plan does not need an arbitrary encrypted virtual machine.”

- READ (`/Users/ember/dev/degg-research/README.md`): the sentence continues with “a small collection of precise relations” for aggregation, crossing, feasibility, optimization, allocation, conservation, policy activation, net settlement, and selective release.

> “The strongest version is a dark relation: nobody learns private inputs or intermediate state beyond a declared leakage function, yet anyone can verify that the specified result and settlement followed from the committed inputs.”

- READ (`/Users/ember/dev/degg-research/docs/RESEARCH_STANCE.md`): this is a research objective, not a property demonstrated by the current experiments.

> “A system that hides the book from traders while granting a permanent omniscient operator or government key has not achieved the Dark objective.”

- READ (`/Users/ember/dev/degg-research/docs/RESEARCH_STANCE.md`): anti-oppression constrains the trust and observation architecture, not just the ciphertext choice.
- READ (`/Users/ember/dev/degg-research/AGENTS.md`): Clear means public computation; Shielded names an authorized viewer; Dark requires no actor to learn beyond frozen leakage and its own authorized output under an explicit corruption model.
- READ (`/Users/ember/dev/degg-research/docs/PRIVACY_MODES.md`): threshold encryption is usually Shielded unless release constraints and the security definition establish the stronger claim.
- INFERRED: Ember's “dark coordination” ambition is end-to-end: market semantics, input inclusion, availability, verification, output release, and settlement must agree on one frozen relation.

## Designed, built, measured

- READ (`/Users/ember/dev/degg-research/docs/ARCHITECTURE.md`): design separates semantic, typed IR, backend, transcript, settlement, availability, and formal-refinement layers.
- READ (`/Users/ember/dev/degg-research/docs/DARK_RELATION_IR.md`): proposed IR freezes bounds, exact arithmetic, ports, visibility, refusal codes, leakage, proof obligations, and settlement schema.
- READ (`/Users/ember/dev/degg-research/docs/DARK_RELATION_IR.md` addendum): one `dark-fba/n4-k4-q15/v0` module and Clear lowering are implemented; the general compiler remains proposed.
- READ (`/Users/ember/dev/degg-research/docs/research/DARK_FBA_RELATION.md`): the first relation is a padded four-slot, four-owner, four-price-tick frequent batch with exact integers and a frozen admission priority.
- READ (`/Users/ember/dev/degg-research/experiments/dark-fba/README.md`): Rust oracle executes Clear and single-executor Shielded semantics; DarkTarget refuses.
- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md` §3.1): its dated check recorded nine passing tests for that first oracle.
- READ (`/Users/ember/dev/degg-research/experiments/dark-fba-independent/README.md`): second oracle compared 300,436,169 enumerated batches with zero final divergences.
- READ (`/Users/ember/dev/degg-research/experiments/dark-fba-independent/README.md`): initial 11,587 refusal-class disagreements exposed unspecified check priority; later refusal agreement is conformance to the newly frozen order, whereas clearing/allocation remained independent.
- READ (`/Users/ember/dev/degg-research/experiments/relation-ir/README.md`): the IR lowering agreed with both oracles on 2,116,916 cases; ShieldedCommittee and DarkTarget lowering refuse.
- READ (`/Users/ember/dev/degg-research/experiments/relation-ir/README.md`): canonical bytes and SHA-256 identify module/data, while its receipt objects are unsigned and prove no security property.
- READ (`/Users/ember/dev/degg-research/experiments/inclusion-availability/README.md`): offline Merkle mountain range, admission log, root receipts, conflict verdicts, abort machine, and reserve refunds have 131 tests.
- READ (`/Users/ember/dev/degg-research/experiments/inclusion-availability/README.md`): availability is still a declared integer; network recovery, cryptographic attribution, and liveness are unmeasured.
- READ (`/Users/ember/dev/degg-research/experiments/leakage-lab/README.md`): Python projects four synthetic traces into public, executor, owner, and regulator views for Clear, Shielded, and hypothetical Dark surfaces.
- READ (`/Users/ember/dev/degg-research/experiments/leakage-lab/README.md`): its eight-slot disclosure budget is accounting over a hypothetical transcript, not a privacy proof.
- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md` §3.1): its dated check recorded seven deterministic leakage-lab tests.
- READ (`/Users/ember/dev/degg-research/experiments/shielded-baseline/README.md`): joined offline run composes the IR and admission objects with sealed payloads, owner checks, publication, and typed aborts.
- READ (`/Users/ember/dev/degg-research/experiments/shielded-baseline/README.md`): 52 tests and 90,082 assembly-path differential cases pass; the two sides share the evaluator, so this does not independently validate clearing semantics.
- READ (`/Users/ember/dev/degg-research/docs/research/SHIELDED_BASELINE.md`): one executor holds the modeled seal and sees the whole book; the seal is a SHA-256 counter keystream, not a real confidentiality mechanism.
- READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md` V3): of 1,125 alternate published runs, 377 pass all modeled checks, including all 33 well-formed public results; result correctness remains executor-trusted.
- READ (`/Users/ember/dev/degg-research/experiments/settlement-model/README.md`): separate offline custody/authorization/nullifier relation has 56 tests, idempotent retry, and exact conservation.
- READ (`/Users/ember/dev/degg-research/docs/research/SETTLEMENT_RELATION.md`): transparent per-claim settlement reconstructs owner, side, fill, and reservation from the public transcript.
- READ (`/Users/ember/dev/degg-research/docs/research/SETTLEMENT_RELATION.md`): it does not recheck hidden limit satisfaction, and upstream invalid-result trust is inherited.
- READ (`/Users/ember/dev/degg-research/docs/research/CONFIDENTIAL_ENERGY_DISPATCH_RELATION.md`): separate energy relation fixes three providers, three periods, two buses, integer quantities, physical feasibility, canonical optimum, and exact settlement.
- READ (`/Users/ember/dev/degg-research/research/confidential-energy-dispatch/README.md`): Clear exhaustive-search oracle and recomputing verifier have 25 tests; no private backend or succinct proof exists.
- READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md` V11): representative energy fixture has 468 feasible complete schedules, chooses cost 56, and rejects a conserving but suboptimal cost-60 plan.
- READ (`/Users/ember/dev/degg-research/experiments/bundling-invariance/README.md`): synthetic payoff corpus tests classification under costless bundle/split, with 16,320 objects and 56,936 decompositions; it does not decide law or profitability.
- READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md` V10): four candidate criteria show zero-cost classification arbitrage on that corpus and four are invariant; invariance alone does not make a criterion useful.
- READ (`/Users/ember/dev/degg-research/experiments/manipulation-cost/README.md`): exact synthetic constant-product sweep has 1,080 base rows and 8,640 off-hours rows.
- READ (`/Users/ember/dev/degg-research/experiments/manipulation-cost/README.md`): longer modeled holds can lower attack cost; original per-bucket estimate hypothesis is explicitly refuted; off-hours thin depth lowers cost subject to sample placement.
- READ (`/Users/ember/dev/degg-research/experiments/manipulation-cost/README.md`): recovery omits order flow, arbitrage, inventory constraints, gas, latency, and other venues; these numbers are bounded model evidence.
- READ (`/Users/ember/dev/degg-research/docs/regulatory/README.md`): regulatory track includes IAC, joint definitions, joint data, and perpetuals research documents; its text contains older draft-status wording.
- READ (`/Users/ember/dev/degg-research/filing/2026-08-cftc/README.md`): later filing set maps five submission builds to four dockets, with `iac-draft-16`, two joint `draft-15` sources, and `perpetuals-draft-4`.
- READ (`/Users/ember/dev/degg-research/filing/2026-08-cftc/SUBMISSION_CRIB.md`): crib instructs a human to save tracking numbers; its only tracking-number cell still says “(add).”
- READ (`/Users/ember/dev/degg-research/output/pdf/FILING-*.pdf` metadata/text heads): five submission builds contain a one-page cover, three-page IAC statement, three-page perpetuals comment, six-page data comment, and five-page definitions comment.
- INFERRED: local `FILING-*.pdf` bytes and a submission plan do not establish that any comment was filed; obtain external receipts before asserting filing status.

## Primitives and implementation boundary

- READ (`/Users/ember/dev/degg-research/docs/LOCAL_LINEAGE.md`): Breadstuffs carries historical real TFHE uniform-price clearing and BFV additive aggregation with an MPC nonlinear boundary.
- READ (`/Users/ember/dev/degg-research/docs/FHE_FRONTIER.md`): historical TFHE kernel timings span tens to hundreds of seconds; BFV plus MPC is millisecond-range under a materially weaker trust model.
- READ (`/Users/ember/dev/degg-research/docs/FHE_FRONTIER.md`): discrete CKKS, REFHE, nested RNS, functional bootstrapping, multi-key/threshold FHE, and verifiable FHE are literature/back-end candidates, not selected local implementations.
- READ (`/Users/ember/dev/degg-research/docs/ROADMAP.md` R4): proposed bakeoff compares TFHE, BFV/hybrid, discrete CKKS, and proof-carrying Clear on identical vectors with setup, communication, proof, failure, leakage, and provenance costs.
- READ (`/Users/ember/dev/degg-research/docs/ARCHITECTURE.md`): MPC committee and FHE backends are architecture proposals; Clear is the measured backend in this repository.
- READ (`/Users/ember/dev/degg-research/docs/LOCAL_LINEAGE.md`): Minidregg has fixed four-owner/four-price BFV input-validity semantics but no BFV runtime, FHE evaluator, threshold ceremony, vFHE, or encrypted clearing.
- READ (`/Users/ember/dev/degg-research/docs/LOCAL_LINEAGE.md`): Zama TFHE/HPU is a research baseline with patent and transitive-component concerns; its code is not imported here.
- READ (`/Users/ember/dev/degg-research/LICENSING.md`): no legacy implementation code was imported; crossing artifacts require producer commit, paths, license, generator, canonical bytes, digest, and receiver checks.
- READ (`/Users/ember/dev/degg-research/experiments/*/Cargo.toml`, `experiments/leakage-lab/README.md`): the nine experiment models have local or no Rust dependencies and no named production MPC/FHE library dependency.
- INFERRED: their Rust/Python code mostly models the contracts around a future private backend.

## Last handoff and live open questions

- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md` §6): its P1 asked for independent FBA oracle, typed IR Clear lowering, inclusion/availability, Shielded baseline, backend bakeoff, formal closure, and separate settlement.
- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md` 19 August addendum): it says all seven P1 packets landed and points to a cross-repo return handoff in Dragon's Clutch.
- INFERRED: the August 18 P1 list is historical; the experiments above close several offline modeling tasks, while backend bakeoff, deployed proof boundary, and private settlement remain open.
- READ (`/Users/ember/dev/degg-research/docs/research/SHIELDED_BASELINE.md` §9): next composition work names split log holder/executor, attribution, threshold decryption, verifiable evaluation, real availability, and settlement; relation-refused abort is marked done.
- READ (`/Users/ember/dev/degg-research/docs/research/SETTLEMENT_RELATION.md` §10): unresolved pre-admission refunds, omitted-position adjudication, attribution, public claim timing/deposit leakage, multi-batch custody, and chain binding are named.
- READ (`/Users/ember/dev/degg-research/docs/ROADMAP.md` Energy E1–E4): energy track still needs independent oracle/formal semantics, physical-source authentication, private backend comparison, optimality certificate, local output, and funded abort/settlement.
- READ (`/Users/ember/dev/degg-research/docs/EXPERIMENT_PROGRAM.md`): cost decomposition, backend bakeoff, leakage, censorship, verifiability, accelerator, and economic experiments require explicit falsifiers and comparable artifacts.
- READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md` V10): regulatory corpora are synthetic and do not validate an actual venue or legal classification.
- READ (`/Users/ember/dev/degg-research/CLAUDE_HANDOFF.md` §7): its named first-session sequence is read truth/specs, rerun offline checks, confirm Dark refusal, review filing gates, reconcile verified results, then choose independent FBA closure or IR Clear lowering.
- INFERRED: that recommended choice is overtaken by the landed independent and IR packets; do not reenact it as unfinished work.

## Three concrete next steps grounded in the record

1. READ (`/Users/ember/dev/degg-research/docs/VERDICTS.md`, `experiments/README.md`, `filing/2026-08-cftc/README.md`): reconcile the designated truth page and dated handoff with later experiments, energy result, and filing builds; mark submission as unverified until a receipt exists.
2. READ (`/Users/ember/dev/degg-research/docs/research/SHIELDED_BASELINE.md` §9, `docs/DARK_RELATION_IR.md` “Next lowering targets”): build the proof-carrying verify-not-find Clear result bound to the module digest, admitted root, exact result, and local outputs; test the 377/1,125 substitution class as the falsifier.
3. READ (`/Users/ember/dev/degg-research/docs/ROADMAP.md` R4 and Energy E1–E2, `docs/FHE_FRONTIER.md`): independently validate one bounded relation, then run TFHE/BFV+MPC/discrete-CKKS/proof-carrying-Clear candidates on identical vectors with full trust, leakage, setup, communication, proof, and failure ledgers.
- INFERRED: steps 2 and 3 are research packets, not a Dark promotion or deployment recommendation.

## What nano, mini, and Bread supply; what remains absent

- READ (`/Users/ember/dev/redregg/work/MINI-CONCEPTS-IN-NANO-20261018.md` §7): nanodregg has attenuable grant chains, revoke, authenticated journal receipts, and conserved value/storage; “proof-carrying” there means admission can be rederived, not a private-evaluation proof.
- READ (`/Users/ember/dev/redregg/work/ACTIVITIES-DESIGN-20261022.md`): nano's `Right.observe`/`Right.invoke`, grants, and grant-turn ledger model authority whose counted capacity can only fall.
- READ (`/Users/ember/dev/redregg/work/MINI-CONCEPTS-IN-NANO-20261018.md` §§2–6): nano has one-signer atomic multi-cell turns; a weak eager-shape/lazy-value guarded hole is expressible as a package, while first-class co-receipt/open-offer and multi-signer joint turns are absent.
- READ (`/Users/ember/dev/redregg/work/MINI-CONCEPTS-IN-NANO-20261018.md` §6): Mini's `HoleSpec` is Theory only; its runtime activities are typed Plan/response suspension, whereas nano intentionally cut `perform` in v0.
- READ (`/Users/ember/dev/degg-research/docs/LOCAL_LINEAGE.md`): Minidregg has mode-indexed private-computation semantics, sealed computation/separate authorized disclosure, public escrow/order/nullifier/retry, guarded advice, and BFV input-validity theory.
- READ (`/Users/ember/dev/degg-research/docs/research/GUARDED_EVENT_FOUNDATIONS.md`): weak guarded holes fix transition shape and authority before a late value arrives; strong late shape change is explicitly refuted in the model.
- READ (`/Users/ember/dev/degg-research/docs/LOCAL_LINEAGE.md`): Breadstuffs contributes real historical FHE, BFV/MPC, committee lifecycle pieces, private-book proof experiments, clear solver/certificate families, and Lean theory.
- READ (`/Users/ember/dev/redregg/work/NANO-VS-MINI-20261017.md` correction): Breadstuffs is Ember's whole prior system awaiting resumption or composting; Mini and nano are side explorations, not a production lineage ranking.
- INFERRED: degg relations can use counted rights for finite participation/release authority, grants for authorized local outputs, and receipts for input/output/settlement joins, but each needs a versioned relation-specific contract.
- INFERRED: none of the sibling receipts proves that the encrypted evaluator computed the right result or that public settlement preserves private positions.
- INFERRED: the missing joins are actual malicious-secure private execution, proof/verifier tied to exact admitted bytes, real availability/attribution, private local-output delivery, and custody with bounded leakage and finality.

## Risks named by the record

- READ (`/Users/ember/dev/degg-research/docs/PRIVACY_MODES.md`): ingress timing, endpoints, audit access, and public transfer graph can defeat a nominally private computation.
- READ (`/Users/ember/dev/degg-research/docs/research/SHIELDED_BASELINE.md`): executor compromise reveals every order; executor censorship and plausible wrong public results survive modeled checks.
- READ (`/Users/ember/dev/degg-research/docs/research/INCLUSION_AVAILABILITY.md`): root/inclusion receipts do not give payload availability, independent attribution, or permissionless liveness.
- READ (`/Users/ember/dev/degg-research/docs/research/SETTLEMENT_RELATION.md`): omission can strand obligations; absent attribution leaves no party to charge, and transparent settlement exposes the position graph.
- READ (`/Users/ember/dev/degg-research/docs/FHE_FRONTIER.md`): key ceremony, adaptive corruption, proof cost, accelerator side channels, attacks on cited FHE lines, and patent/provenance remain selection risks.
- READ (`/Users/ember/dev/degg-research/docs/RESEARCH_STANCE.md`): central master decryption, regulatory overreach, and an “operatorless” label without authority/liveness accounting violate the research stance.
- READ (`/Users/ember/dev/degg-research/docs/regulatory/README.md`, `filing/2026-08-cftc/SUBMISSION_CRIB.md`): draft/readme status conflicts with later filing-candidate bytes; legal claims, exact submission status, public disclosure, and provenance require their own evidence.
- READ (`/Users/ember/dev/degg-research/AGENTS.md`): no production deployment, keys, live orders, mainnet actions, regulator contact, or external publication is authorized by this repository.
