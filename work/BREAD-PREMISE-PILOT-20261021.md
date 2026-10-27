# Bread premise pilot: from floor census to an obligation journal

[MEASURED] Date: 2026-10-21. Bread checkout: `/Users/ember/dev/breadstuffs`,
`22fad151e9f118e3aa001a823e075918ffa139e8`. This was a read-only scout.
The only new files are this memo and scratch under `/Users/ember/dev/redregg/work/`.

[INFERRED] Verdict: reuse `FloorCensus` as a *floor exposure instrument*, but do not
pretend that its TSV already contains a theorem's full proof supports, its ordinary
consumers, or an audit revision ledger. The historical “14 lines” is a lexical
sample, not fourteen current defects. The first actual repair unit should be one
live global `OrBreak` component and its named-pair successor, with a separate
contract dependency export before automatic reuse is authorized.

## 1. What the instrument computes

[READ `metatheory/Dregg2/Verify/FloorCensus.lean:1-152`] The file describes a
read-only command, `#floor_census`, over an imported Lean environment. It is
an elaborated-term instrument, replacing a source-text regex ruler that missed
floors, credited file-level discharges, and once failed open on a bad path.

[READ same:14-52] Pass 0 discovers `Prop` definitions whose unfolded body
matches an injectivity shape. Pass 0b finds proof statements refuting those
floors, including nested negations under conjunction, existential and universal
claims, and distinguishes parametric from closed-instance refutations. Pass 0c
looks for assumption-free positive witnesses: parametric provability and
particular satisfiable instances are separate poles. A conditional witness is
neither pole.

[READ same:53-77] Pass 1b scans `Prop` definition *bodies*, not just theorem
binders, and follows `Prop` definitions to a fixpoint. It records `prop-body`,
`propdef-user`, and `embedded` appearances. Pass 1u repeats exposure scanning
for unrefuted floors; the older implementation's zero for this class meant
“not measured.”

[READ same:78-126] Pass 1 classifies a floor hypothesis in a declaration's
elaborated type against the proof term. `endpoint` applies it; `threader` passes
it; `dead` does not use it; `no-value` has no inspectable value; `tooth` has a
`False` conclusion. Auxiliaries are chased, and bundles expose structure fields
via projections. `SHAPE` records an injectivity spelling that a name-only scan
would miss. The floor-flow DAG follows passed floor hypotheses, including a
higher-order pass into another hypothesis, statement coupling through Prop
definitions, and compiler-generated auxiliaries. `ho-opaque` and `ho-local`
flags warn when a computed level is an unsafe work order.

[READ same:128-151; :1140-1328] The command refuses a partial environment:
it requires at least 500,000 constants, named floor sentinels, refutations for
sentinels that need them, Prop-body sentinels, and the higher-order keystone.
The source computes DAG levels to a bounded fixpoint and errors on cycles.
These are coverage guards, not proof of semantic adequacy.

[READ same:132-151] The source quotes its line schema as:

```text
FLOOR    name status witness closed? named? via provable-by satisfiable-by
PROVABLE floor witness
SATWIT   floor witness
UCARRIER name module file startLine endLine kind class conc floors flags
CARRIER  name module file startLine endLine kind class conc level floors flags
BUNDLE   struct
PROJ     proj struct floor
SHAPE    name module file line injective-head
RELEVEL  name v1-level v2-level
COMBO    floors carriers threaders
SUMMARY  key value
```

[READ same:1131-1328] The actual emitter also writes `MODULE` lines. The
`FLOOR` line's fields are formatted as documented. `CARRIER` rows do not emit
the `edges` or `hoEdges` arrays used to compute level. Consequently the TSV
contains a level and classification, but not the reconstructible DAG edge list.

[READ same:151] The source's own scope sentence is decisive: the tool only
measures. It proves nothing, ports nothing, and a clean report does not say
the system is verified.

[MEASURED] Warm `.olean` files for `Dregg2` and `FloorCensus` exist locally.
I invoked `lake env lean` on a scratch file importing `Dregg2` and asking for
`#floor_census` to write the scratch TSV. This invokes Lean over cached imports;
it is not a whole-tree build. The process produced no output or TSV within a
180-second cap and was stopped by the timeout. Its empty captured log is under
`/Users/ember/dev/redregg/work/CX-BREAD-PREMISE-scratch/`. Thus this pilot
has no fresh full-environment census receipt. A longer run or a build would
be separate work; neither is inferred from the empty output.

[MEASURED] The checked-in `docs/artifacts/floor-census-v2-2026-07-26/floor-census-v2.tsv`
has 1,925 `CARRIER` records. It is historical v2 evidence, not a current v3
run: its floor names and source ranges include pre-cutover declarations.
The dry run uses a fresh TSV if Lean produced one, otherwise labels this archive.
No archived row may authorize reuse at the current source revision.

## 2. Journal mapping and missing fields

[READ `HOLES-FOR-PROOF-ENGINEERING-20261020.md`, “A theorem as an enduring
obligation”] The nano proposal gives a stable claim identity and immutable
revision: elaborated target, telescope, universes, definition closure,
deployment instance, toolchain, and advertised interpretation. A candidate has
proof, reconstruction recipe, versioned supports, blockers, and receipts.
Withdraw and repair are revisioned events, never retroactive edits to history.

[INFERRED] Use one declaration/theorem as an obligation *only after* its
contract is pinned. A declaration name is an address, not immutable identity.
The current TSV gives the name, module, file, source span, declaration kind,
floor-specific class, conclusion shape, level, recognized floors, and flags.
`FLOOR` gives a refutation witness and, in v3, positive poles. These are good
seed records for a *floor-obligation adapter*.

[INFERRED] Map `endpoint` to a likely re-proof step; `threader` to a likely
consumer restatement; clean theorem `dead` to a strengthening candidate;
`prop-body`, `propdef-user`, `embedded`, `BUNDLE` and `PROJ` to contract or
structural redesign units. This is a work queue, not a theorem: an endpoint
classification is about a *floor binder*, not the whole proof dependency set.
The `tooth` and `refut-witness` rows are anti-floor evidence, not ordinary
port targets. Keep `ho-opaque` unresolved rather than inventing a topological
order from its reported level.

[INFERRED] In nano vocabulary, supports must include both (a) what the
*contract* unfolds and (b) what the *proof* uses, including its axiom closure.
The census extracts some floor-related subgraph from elaborated types and
values. It does not export every declaration mentioned in the target, every
constant in the proof, every reduction/unfolding actually performed, or the
axiom set of each theorem. `#assert_axioms` elsewhere checks a whitelist, but
it is not a row in this TSV. An exporter must keep contract, proof, and recipe
supports separate; they invalidate under different edits.

[READ `docs/audit/META-REVIEW-STATEMENTS.md:1-151`] A named theorem can be
kernel-clean while its advertised claim is hollow: the dated review identifies
`deco_attestation_uc_realizes`'s ZK conjunct as a definitional tautology and
its advertised tooth as concerning a different view. That is a claim blocker,
not a missing axiom or failed proof. Its earlier `b201f7d76` review is not
a current verdict on an immutable theorem revision.

[READ `docs/audit/NON-VACUITY-MANIFEST.md:1-268`] The manifest names
`fires` and `bites` companions per security property. It records later
repairs, including the removed `UCRealizesFAtt` tautological conjunct.
A row is audit evidence with a date, exact subject, and successor, not a
permanent blocker attached to a bare declaration name.

[READ `metatheory/docs/AXIOM-HYGIENE.md:1-104`;
`metatheory/docs/SOUNDNESS-RESIDUAL-CENSUS.md:1-220`] Those records
separate proof axiom hygiene, assumptions bound as hypotheses or fields,
and whether the live implementation forces the assumed condition. A theorem
can have a clean axiom closure and still carry a premise that the deployed
circuit never forces. Model `premise-carried` and `implementation-forced`
as different edges with different repair jobs.

[INFERRED] Missing journal fields in the TSV: stable obligation ID;
source/object hash; exact elaborated target and universe instantiations;
instance binding; all contract/proof/reconstruction dependencies; axiom
closure; negative blockers with subject revision and dated disposition;
alternative candidates; checked kernel receipt; cost/resource contract;
consumer edges and preservation contract; withdraw/repair events; and
successor relation. A source span is useful navigation, never a revision key.

[INFERRED] A redesign day is an event sequence: withdraw the old contract or
advertised interpretation; invalidate only claims supported by that revision;
retain old receipts as history; state successor theorem(s); recheck them;
record consumer transports and residuals. `Refuted` needs a scoped Lean
impossibility result. A failed tactic, an absent candidate, or a stale audit
is an open/blocked obligation, not refutation.

## 3. Fresh inventory of the historical “14 lines”

[READ `/Users/ember/dev/redregg/work/STUDY-FINDINGS-20261021.md:345-376`;
`cv task show 01a15630-cf60`] The task title says “14 lines in 3 files.”
The study's own paragraph says **14 lines in 4 files** and explicitly includes
`Dregg2.lean` import comments; it also says one `FirstDivergence` form is
already sound. These were grep observations at the same checkout hash,
`22fad151e`, not fourteen identified theorem obligations.

[MEASURED] I re-inventoried the three named implementation files
`Circuit/FirstDivergence.lean`, `Shielded/RealCrypto.lean`, and
`Verify/FreeConclusionRatchet.lean` using `rg` and source reads. The table is
an auditable *14-line sample* from those files. “Consumers” means **TSV
consumer rows**, not source mentions. The census does not export general
constant-to-consumer edges; all fourteen entries have `0 / unavailable` in
the historical TSV. That is a coverage result, not “no consumers.”

| ID | path:line | declaration / role | disjunct reading | census consumers |
|---|---|---|---|---|
| F139 | `FirstDivergence.lean:139` | `globalBreak_free` | Deliberately proves the global escape free under noninjectivity; refutation witness, not repair target. | unavailable |
| F149 | `FirstDivergence.lean:149` | `indexedBreak_not_free` | Negates universal freedom of a named-pair residual; negative control. | unavailable |
| F171 | `FirstDivergence.lean:171` | `leafPair_binds_or_coll` | Pair is `(enc a, enc b)` from this instance; sound indexed residual. | unavailable |
| F230 | `FirstDivergence.lean:230` | `zipFirst_binds_or_coll` | Total extractor returns a pair in these two lists; sound indexed residual. | unavailable |
| F311 | `FirstDivergence.lean:311` | `foldLast_binds_or_coll` | Total fold extractor returns the pair; sound indexed residual. | unavailable |
| F399 | `FirstDivergence.lean:399` | `resolve` | Consumes a named-pair dichotomy under `¬ Coll h p`; already prices the instance. | unavailable |
| F431 | `FirstDivergence.lean:431` | `Site.sound` field | Bundle's `find h i` binds each residual to its instance; structure field, not a theorem. | unavailable |
| R380 | `RealCrypto.lean:380` | `Poseidon2Tree.root_binds_or_collides` | `rootCollFind l₁ l₂` is the two claimed leaf lists. | unavailable |
| R417 | `RealCrypto.lean:417` | `forged_set_is_honest_or_collides` | Uses that same `rootCollFind forged leaves`. | unavailable |
| R519 | `RealCrypto.lean:519` | `deployed_forged_set_is_honest_or_collides` | Instantiates the indexed theorem at deployed tree. | unavailable |
| G89 | `FreeConclusionRatchet.lean:89` | comment, free example | Shows `xs = ys ∨ SpongeCollision hash` as rejected shape. | not a declaration |
| G90 | `FreeConclusionRatchet.lean:90` | comment, sound example | Shows `xs = ys ∨ SpongeColl hash xs ys`. | not a declaration |
| G897 | `FreeConclusionRatchet.lean:897` | error-message string | Recommends a named-pair repair. | not a declaration |
| G911 | `FreeConclusionRatchet.lean:911` | error-message string | Explains why outer ∃ is free. | not a declaration |

[MEASURED] The dry-run output labels these roles rather than promoting all
fourteen to obligations. In the three files, one theorem proves the defect,
one refutes it as a negative control, several theorems/one field encode its
repair, and four lines are comments/string literals. The four-file historical
count also has import comments. This refutes the task title's implication
that fourteen current Lean claims need the same restatement.

[READ `FirstDivergence.lean:1-110,139-171,215-235,300-320,390-440`]
`Coll h p := p.1 ≠ p.2 ∧ h p.1 = h p.2` has no existential. Its generic
`globalBreak_free` proves `P ∨ ∃ p, Coll h p` for arbitrary `P` from
noninjectivity. `indexedBreak_not_free` uses a collapsing sponge and an
equal pair to refute the corresponding universal indexed statement. These
are directly relevant controls for any adapter's “vacuous” classification.

[READ `RealCrypto.lean:340-420,505-525`]
`Poseidon2Tree.root_binds` has an explicit per-instance `hnc : ¬ SpongeColl
T.sponge (rootCollFind l₁ l₂)` premise; `forged_set_forces_collision` and
`nonmember_refused` likewise use named-pair side conditions. The deployed
`_or_collides` theorem has no such premise because it keeps the honest
collision residual in its conclusion.

[READ `FreeConclusionRatchet.lean:1-160`] The existing gate derives
freeness witnesses from Lean's environment and scans positive conclusions.
It explicitly distinguishes global `SpongeCollision` from `SpongeColl` at a
named pair, tests pattern discrimination, and keeps a bare-event rule for
idle hypotheses. This is stronger evidence than a new regex scanner.

[INFERRED] For a genuinely live repair pilot, use
`Distributed.HistoryAggregation.verified_history_conserves_orBreak` and
`root_tooth_pins_kernel_orBreak` (and the source-noted third
`conserves_from_verification_orBreak`) against their already landed
`*_or_collides`/`*_of_noColl` successors. The gate's header says these
were vacuous at field-bounded sponges. Compare the old and successor
obligation revisions; do not reopen the sound `FirstDivergence` sample as
if it were broken.

## 4. Dry-run adapter and its output

[MEASURED] Script: `/Users/ember/dev/redregg/work/CX-BREAD-PREMISE-scratch/premise_pilot.py`.
Run command: `python3 -I /Users/ember/dev/redregg/work/CX-BREAD-PREMISE-scratch/premise_pilot.py`.
It reads a current scratch census TSV if available, otherwise the historical
v2 artifact, and the four audit documents. It validates each source line,
emits a source hash, class, potential audit hits, a placeholder for missing
support/axiom export, and a `dry-run-discover` event. It writes no repo file.

[MEASURED] Its complete JSON output is included as the companion artifact
`/Users/ember/dev/redregg/work/CX-BREAD-PREMISE-scratch/premise-pilot-output.json`.
The following is the script's `--summary` output, a lossless per-obligation
ID/class/TSV-hit projection from the first run (historical census, 1,925
carrier rows):

```text
mode=DRY_RUN_ONLY  census=floor-census-v2.tsv  coverage=14 lexical lines
F139 globalBreak_free                             free-witness      0
F149 indexedBreak_not_free                        negative-control  0
F171 leafPair_binds_or_coll                       indexed-theorem   0
F230 zipFirst_binds_or_coll                       indexed-theorem   0
F311 foldLast_binds_or_coll                       indexed-theorem   0
F399 resolve                                      indexed-consumer  0
F431 Site.sound                                   structure-field   0
R380 Poseidon2Tree.root_binds_or_collides         indexed-theorem   0
R417 forged_set_is_honest_or_collides             indexed-theorem   0
R519 deployed_forged_set_is_honest_or_collides    indexed-theorem   0
G89  free-shape-example                           comment           0
G90  indexed-shape-example                        comment           0
G897 repair-example                               string-literal    0
G911 quantifier-warning                           string-literal    0
supports.elaborated_constants=UNEXPORTED  supports.axioms=UNEXPORTED
census_consumers=NOT_EMITTED_BY_FLOOR_CENSUS
not_an_obligation_count=true
```

[INFERRED] The adapter's lexical mentions are leads only. For example,
`RealCrypto.forged_set_is_honest_or_collides` calls
`Poseidon2Tree.root_binds_or_collides`; the deployed theorem instantiates
`forged_set_is_honest_or_collides`; `Circuit/BundleCutoverCheck.lean`
checks the latter. Those source reads demonstrate real consumers even
though all three have zero historical `CARRIER` matches. A truthful
journal needs a *new* elaborated constant dependency export, not the
`CARRIER` table relabeled as the whole reverse dependency graph.

## 5. Premise price and successor contract

[INFERRED] PRICE PREMISES for this scout and script: landed bread theorems
gaining a hypothesis: **none**; landed theorem statements restated:
**none**. It is read-only and makes no claims authorized by new proofs.

[READ `RealCrypto.lean:378-430,516-520`] In the existing pair-indexed
repair, the unconditional theorems
`Poseidon2Tree.root_binds_or_collides`,
`forged_set_is_honest_or_collides`, and
`deployed_forged_set_is_honest_or_collides` gained **no premise**.
The equality/refusal consumers `Poseidon2Tree.root_binds`,
`forged_set_forces_collision`, and `nonmember_refused` explicitly
carry `¬ SpongeColl` at the pair they use. Those are the named premise
prices of deriving a plain binding claim rather than a disjunction.
The old `spongeCR` structure field was deleted; at the reference tree it
is discharged, while the deployed tree retains the per-instance residual.

[READ `Circuit/StarkSoundReduce.lean:141,245,313` and
`Distributed/HistoryAggregation.lean:307,562,601,977,1061,1215`]
Other existing resolution theorems already name the corresponding prices:
`hood_of_reductions_of_no_sponge_collision`,
`algoStarkSound_transferV3_of_no_sponge_collision`,
`lightclient_unfoolable_deployed_of_no_collisions`,
`logRoot_binds_of_noColl`, `root_tooth_pins_state_of_noColl`,
`root_tooth_pins_kernel_of_noColl`,
`kernelChained_of_verified_of_noColl`,
`verified_history_conserves_of_noColl`, and
`logChained_of_verified_of_noColl`. These have no-global-collision or
named-pair conditions in their current sources; several global `¬
SpongeCollision` forms remain impossible at a deployed finite sponge and
should not be advertised as discharged deployed security.

[INFERRED] Asked literally which bread theorems in the fourteen-line
sample would **gain an explicit-list premise** under a restatement:
**none**. The positive sample is already pair-indexed, and the four gate
examples are not theorems. Bread's current resolution theorems use
`¬ Coll` / `¬ SpongeColl` at extracted pairs, rather than nano's
`¬ CollidesAmong hash S` over an explicit list. If a future adapter chooses
an explicit list `S`, it must prove that each extracted pair belongs to
`S`; then the plain-conclusion consumers named above would need an
`¬ CollidesAmong hash S` premise or a discharged equivalent. That is a
proposed interface change, not a current theorem price. Do not silently
replace a pair-specific condition by a universal or global collision ban.

[INFERRED] A future restatement of a *live* global `OrBreak` theorem should
leave the unconditional `P ∨ Coll h (find args)` with **no added premise**.
Its plain-`P` corollary gains `¬ Coll h (find args)` or a bounded adversary
advantage premise. The exact set of *newly* priced theorem names cannot be
certified from FloorCensus TSV; export consumer edges and read their types
before an edit. The already existing named corollaries above are evidence
of the expected shape, not a claim that this pilot added those premises.

[READ `Blake3FloorReduce.lean:140-280` and
`Circuit/Blake3FloorEffRegrounded.lean:1-210`] For BLAKE3, a bounded,
keyed advantage game is the successor; merely writing `∨ Blake3Collision`
was another free global existential. An explicit list/pair repair is suitable
for deterministic binding; it does not by itself express a computational
search bound. Keep logical and resource preservation contracts distinct.

## 6. Three likely failures and decisive measurements

[INFERRED] **Failure A: incomplete supports.** Floor rows omit ordinary
constants, projections, auxiliary proof code, definition bodies outside
injectivity shapes, and recipe inputs. Measurement: export type/value
constant closure plus axiom closure for a chosen component; mutate a
held-out support and compare journal reuse against independent fresh Lean
checking. One reused claim whose target or proof has changed refutes
support sufficiency. Also measure false invalidations; “everything touched”
refutes the proposed locality benefit.

[INFERRED] **Failure B: the journal follows the wrong claim.** A literal
`P ∨ Collision` is true but useless for binding; an audit tooth may target
another predicate, or a dated finding may already have a successor.
Measurement: replay the three HistoryAggregation global twins and named
successors, plus `globalBreak_free`/`indexedBreak_not_free`, through a
revisioned audit record. The journal must withdraw binding authorization
for the free twin, retain its literal kernel receipt, and permit the
indexed successor only with its exact target and teeth. Any “repair” that
marks the free twin as binding refutes the contract mapping.

[INFERRED] **Failure C: premise flow is too coarse or incomplete.** The
TSV's level omits the edges; `ho-opaque` may hide an actual dependency,
while bundles and Prop bodies can make a textual reverse graph misleading.
Measurement: export every floor-flow edge and compare predicted
endpoint/threader/bundle work against a held-out source edit, including a
higher-order `descriptorRefines` path. Count missed obligations and extra
rechecks under a fixed memory/time cap. One missed downstream obligation
refutes the flow as a safe repair order; near-whole-tree invalidation
refutes the claimed incremental value.

[INFERRED] The next implementable increment is an exporter for exact theorem
revision, type/value constant closure, axiom closure, and floor-flow edges,
with the current `FloorCensus` coverage sentinels retained. A small adapter
can then join dated audits by exact subject revision and record withdraw /
repair receipts. Only after that comparison should a journal authorize
reuse or describe a redesign day as complete.
