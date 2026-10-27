LAND-WITH-FIXES — three exact documentation/message changes below; nineteen statements accepted. Pre-landing review only: PROTOCOL-61 must land first, and the landed-binary join confirmation remains CX-HOST's post-landing obligation.

## WORKLOG

2026-10-21 03:40 UTC — CX-READER-HOST71, read-only adversarial second reader. A DEMONSTRATION MINI CAN TAKE. No source edited, no worktree created, no scripts/commit launched, no agent spawned. All build/runtime work ran on hbox in the designated warm wt/host22. Mac writes are this report only.

Read: lane rules in full; CX-HOST.report.md in full through ROOT's reader/order ruling and the subsequent ownership entry; HOST-LOG.md HOST-22 handoff and part 2; REENTRY specialist procedure; hbox main CHARTER.md and gates/OWNERS; decisions/host.md HOST-64 through HOST-70 (including HOST-66), and candidate HOST-71 in full (HOST-71 is not on main yet). Read the original four-line crash probe, the 19-path/message files, all new definitions and all nineteen proof statements/bodies, changed deployed paths and plants. The old cv task locator 01a155a1-f562 does not resolve as a session in current cv; no claim to have recovered that conversation. Current brief and recorded ROOT rulings supply this review's scope.

Reviewed candidate: wt/host22 HEAD 0cd046c8b94456835d11574b9c64090e7869d287; main 2232ea67b1449db1f107861744138d8855e4326f. All 19 files still match logs/CX-HOST-host71-reviewed-candidate/manifest.json at completion. Host/Proofs/Physical.lean SHA256 d3cc255df3e4d7c7abfe9a7fb61171472a3e10707f829dd7c5598575a33a156b. Candidate host binary SHA256 2794b2b29097eed29dd7559ca7bf2c22e2dc6e72d74f33135b5c05e2758a1782. The worktree also holds the separately sequencing PROTOCOL-61 WIP; this verdict does not authorize bundling it into host!.

### Exact fixes for CX-HOST to apply

1. decisions/host.md:3247-3250 (unlanded HOST-71 premise paragraph).

OLD:
```
Landed theorems restated: none. In particular sealed_opens / seal_facts retain their
statements over LOGICAL readers, and host_run_folds / host_run_kept retain submit/cancel
as the World movers. Physical identity correspondence is a NEW invariant, proved from
genesis and preserved through append, truncate, rotation, seal, adoption and retention.
```
NEW:
```
Landed theorems restated: none. sealed_opens / seal_facts retain their statements over
LOGICAL readers. HOST-68's StoreIndexes, sealed_indexes / sealed_indexes_deployed,
sealed_indexes_same / sealed_indexes_deployed_same, and its deployed page theorems
are unchanged. HOST-69's WriterLife / writer_life_trusted, genesis_life_trusted,
import_life_trusted and life_opened_size_le are unchanged; received-base adoption
still does not discharge CheckpointTrusted or become a WriterLife admitted-fold link.
host_run_folds / host_run_kept retain submit/cancel as the World movers. The NEW
IdentityLife induction proves filename/header correspondence for the modeled genesis,
put, body, publish and drop operations. Mapping the IO writer paths to these operations
is read off the code under the stated filesystem assumptions, not an IO refinement theorem.
```
Reason: name the two explicitly requested landed theorem families and keep the abstract invariant's scope distinct from a proof of the IO implementation. No theorem or premise changes.

2. Host/Proofs/Physical.lean:148-149, identity_at docstring only.

OLD:
```
/-- A selected physical file really fronts the requested LOGICAL offset in the base's
 generation. This is the correspondence supplied to segRead_logical, not a new seal premise. -/
```
(The source has no leading space before `generation.`; match the text accordingly.)
NEW:
```
/-- A selected image's header names the requested LOGICAL offset and base generation.
This is filename/header correspondence only: it does not establish SlicesOf, file
availability, or IO refinement. The existing logical-reader seal premises are unchanged. -/
```
Reason: identity_at proves precisely its two equalities. It neither supplies the independent SlicesOf body equations nor is called by segRead_logical. The interrupted-open frame theorem separately preserves the prior reader.

3. logs/CX-HOST-host71-msg.txt:22, split the existing OPS declaration so the brief's three column-zero CROSS-LAYER lines name the actual granted scopes without inventing a third owner.

OLD:
```
CROSS-LAYER: OPS (ROOT granted the two Plants helpers for the HOST-71 flag day, real 10-21, the missing-file diagnostic wording in Ops/Units.lean, and the regenerated deploy/units/STORE.md and deploy/units/EXITS.md).
```
NEW:
```
CROSS-LAYER: OPS (ROOT granted the two Ops/Plants.lean helpers and the missing-file diagnostic wording in Ops/Units.lean for the HOST-71 flag day, real 10-21).
CROSS-LAYER: OPS (ROOT granted regenerated deploy/units/STORE.md and deploy/units/EXITS.md for the HOST-71 flag day, real 10-21; ordinary generator output only).
```
Keep the existing HOSTING line immediately after them. The current two-line message already passes owners; this change satisfies the brief's literal three-line requirement while preserving exactly the granted path set. No new foreign owner/path is needed: the freshly generated codec vectors are unchanged.

These are documentation/message fixes, not a design fork or weakened check. After applying them and after PROTOCOL-61 lands, run the mandatory source gates for the actual final landing snapshot. No further reader pass is required for these exact prose changes; changed theorem statements or behavior need another read.

### Statement verdict and implementation boundary

2026-10-21 READ GREEN — all nineteen new statements passed the DISJUNCT CHECK; none has a disjunctive conclusion. Read individually:
- segmentIdentity_injective: both offset bounds are material; without them offset overflow aliases a generation.
- physicalHeaderRead_ok / physicalHeaderRead_foreign: accepted or refused result of the deployed pure reader is constrained by authenticated generation and logical start, not a surrogate identity.
- nextGeneration_gt / nextGeneration_fresh: membership of a real existing filename and the offset bound establish allocation freshness; freshness is not merely assumed by the composed allocation theorem.
- generationFault_moved / generationFault_same: opposite branches of the actual live-tail check, with pinned decoder outputs.
- identity_empty / identity_put / identity_body / identity_publish / identity_drop: structural frame/preservation lemmas; publish leaves the files map alone. They assert filename/header consistency, not base availability or World trust.
- identity_life: induction from the modeled genesis through all five operation forms; not an arbitrary initial invariant assumption.
- identity_at: the selected file's generation/start follow from correspondence and bounded injectivity, with the documentation correction above.
- adoption_prepared_at / adoption_prepared_base: fresh generation preserves every old selected file and the old base/index/generation. Dropping freshness admits the original in-place failure.
- adoption_allocated_at: discharges freshness from nextGeneration and the old filename in the directory list.
- adoption_interrupted_opens: a prior successful open is preserved through a genuinely different put state, using the same segRead/openWith core and the allocator. It preserves the entire Opening; it does not assume success after the interruption. The learned starts/size are held fixed in this abstract frame property; the deployed selection uses the unchanged base generation.
- adoption_published_at: publication selects the prepared header; the committed and uncommitted states are observably distinct.

PRICE PREMISES: none of the landed HOST-71-relevant theorems gains a hypothesis; none is restated. git diff is empty for Host/Proofs/Seal.lean, Host/Proofs/StoreIndex.lean and Host/Proofs/Trusted.lean. headerFault's definition is unchanged. Normal rotate still calls it after checking the physical wrapper/generation. prepareAdoption checks the old header, uses Base.seal, creates a new file with writeNew, syncs the directory, then adopt atomically installs the wrapped base. Genesis/rotation use the same identity naming/wrapping; append/truncate preserve headers; normal seal preserves generation and retainedFrom; retention removes files only after publication. Adoption's retainedFrom is pos.offset, matching HOST-68's run start and adopted step count. No old header is replaced by this path.

Closure C3: IdentityImage/SegmentImage data and operations are in definition modules; IdentityCorresponds and IdentityLife are in Host/Proofs/Physical.lean. The source closure gate passes. No new axiom, sorry, partial definition, native_decide or guard was added.

### Executed and read evidence

2026-10-21 BUILD GREEN — one affected-target build under SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2: `lake build Host Ops host host-sim host-file-sim emit-units codec-vectors hosting-controller`, 355 jobs, complete output logs/CX-READER-HOST71-build.log. Independently re-elaborated all nineteen statements with `lake env lean -DmaxHeartbeats=200000 Host/Proofs/Physical.lean`, same resource cap, exit 0, logs/CX-READER-HOST71-proof.log. No whole Hosting library/Hosting.Proofs.Reply build was reached or launched, so no 16G raise occurred beside the live judge benchmark. Existing warm proof modules, including Seal/StoreIndex/Trusted, were validated by the affected build; CX-HOST-host71-build11.log records their successful earlier rebuild and was read whole.

2026-10-21 SOURCE GREEN — own `gates/check.py` against the actual 19-path list and message: closure, refusals, size, paths, runs, rebase, tcb, vectors, waste, owners all ok (logs/CX-READER-HOST71-gates.log). diff --check and message/generated placeholder scans clean. Foreign paths are exactly Ops/Plants.lean, Ops/Units.lean, deploy/units/STORE.md, deploy/units/EXITS.md, launcher/tests/grain.rs, all explicitly granted. No OPS predicate or grain assertion was removed.

2026-10-21 RUNTIME GREEN — whole outputs read, not verdict-only greps:
- Seed 1: CX-HOST-host71-memory-sim.log and CX-HOST-host71-green2.log ALL PASS; the later memory-seal addition's complete restored control is CX-HOST-host71-memory-restored-green.log, ALL PASS.
- Seeds 2 and 3: this reader ran both host-sim and host-file-sim at 6G/2 threads, sequentially, all exit 0 and ALL PASS. Complete outputs are logs/CX-READER-HOST71-memory-{2,3}.log and CX-READER-HOST71-files-{2,3}.log. Both file runs include the final memory-seal plant.
- OPS: CX-HOST-host71-ops.log, complete 81 lines, ALL PASS.
- Grain: original CX-HOST-host71-grain.log and this reader's CX-READER-HOST71-grain.log read whole. Reader ran only `the_owner_stops_a_grain_and_a_start_only_grantee_cannot` with --test grain and --exact, explicit ND_LEAN_BIN=$PWD/.lake/build/bin and CARGO_TARGET_DIR=$PWD/target; 1/1 PASS in 1.96 s.
- Client: original CX-HOST-host71-join-candidate.log and this reader's CX-READER-HOST71-join-candidate.log read whole. Reader ran only `join_from_a_signed_invitation_refuses_forgeries_and_serves_a_write` with --test join and --exact, explicit ND_LEAN_BIN=$PWD/.lake/build/bin and own cargo target; 1/1 PASS in 1.68 s. This is the CANDIDATE binary, not a falsely claimed landed binary.

2026-10-21 TEETH GREEN/RED — original logs/CX-HOST-probe/result.log read whole: the old in-place repair makes both reopens foreignSegment before the base write. Current file plants reopen both at the previous base after prepare, preserve every old file, skip the orphan on publication, reject missing selected file by exact identity filename, reject authenticated identity mismatch foreignSegment, reject damaged outer wrappers baseCorrupt/checkpointCorrupt, and reject an old live Tail foreignSegment. Adopt → append → check passes with the retained run start. All eight mutation outputs were read whole: CX-HOST-host71-{inplace,identity,wrapper-mac,live-tail,old-shape,retained-start,orphan-generation,memory-seal}-red.log. Each shows its real runtime failure; the harness source requires successful builds and a nonzero run, then restores source. The rejected compile-only identity mutant is not counted. Own error/unbound/No-such-file/Traceback scans find only the intentional OPS missing-store refusal and the memory simulator's intentional pageIo plant; no harness failure.

2026-10-21 GENERATED GREEN — fresh `codec-vectors --write` to previously absent logs/CX-READER-HOST71-vectors.tsv emits 260 vectors / 56 sites, byte-identical by cmp to gates/codec-vectors.tsv. Fresh emit-units to logs/CX-READER-HOST71-units is byte-identical by recursive diff to deploy/units, including STORE.md and EXITS.md. No repository-generated file was rewritten by this reader. Every Store re-geneses; the old-layout plant reaches shapeMismatch before World decode/identity traversal. Logical codecs/vectors remain unchanged; physical shape stamping and operator descriptions move.

## Handoff

All reader commands have exited. No detached reader jobs/PID files, no source edits, no unlanded implementation from this lane. Reader artifacts are only logs/CX-READER-HOST71-* plus this report; file-sim removed only its own run fixtures beneath the reader-prefixed scratch root. No other files/caches removed. /tank has 307G available. CX-HOST owns wt/host22 and the live PROTOCOL-61 lander; neither was stopped or altered.

The ordering creates a necessary evidence distinction: ROOT requires this review before the host! landing, so the landed HOST-71 binary does not yet exist for the required final join test. Preserve PROTOCOL-61 hash → apply these fixes/source gates → host! full judge → verify landed source/binary and run the ONE named join test with explicit ND_LEAN_BIN, reading its entire output. This is an outstanding CX-HOST completion check, not permission to call candidate evidence landed.

2026-10-21 VERDICT LAND-WITH-FIXES: three exact documentation/message fixes; all nineteen new statements accepted; affected build, source gates, simulations seeds 1–3, OPS plants, filtered grain/join and fresh generated-file comparisons GREEN.
2026-10-21 OUTSTANDING: CX-HOST applies fixes, preserves PROTOCOL-61-first sequencing, lands host!, then records the named join test against the landed binary with explicit ND_LEAN_BIN. Candidate-only pass is not that confirmation.
DONE 2026-10-21 — read-only review complete; landed hashes by this lane: none.
