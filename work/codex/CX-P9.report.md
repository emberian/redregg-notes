## WORKLOG
2026-10-20 CX-P9 START: demonstration Mini can take. Worktree /tank/dregg-build/nanodregg/wt/CX-P9 created detached at b72e5a8 via main (the contract parent directory is not a Git repository). No landing will be launched. Local report is the only Mac write.
2026-10-20 PRICE PREMISES, before source edits: landed theorems gaining hypotheses: none; landed statements restated/edited: none. New module provenance_iff will be namespaced P9; the old fixed-environment bridge remains unchanged. Every-env provenance retains guard and budget as explicit literals because E is opaque; no undeclared environment-key representation is invented. New declarations only; extending records uses a new namespaced extension, following P4, rather than editing landed constructors.
2026-10-20 READ: lane rules 1..18, complete program/card P9, literature §1 de Kleer/GKT/Grädel–Tannen and §4, CHARTER, gates/OWNERS; relevant decisions LANG-66..73 (older cost entries partially read). Original PDFs extracted and read: Grädel–Tannen pp9,19,20,22,23 (Def4, Props15/16); de Kleer pp18–19 (printed144–145); GKT pp3–4. REENTRY says specialists need not replay root history. Source Closure and Judge read completely. No claim to have read older unrelated decision history.
2026-10-20 GREEN: tooth built first (CX-P9-tooth.log); all-env provenance, specialization/update, complementary literals, absorption, sound/complete globally minimal token repairs, P4 residual adapter, recorded nogoods/P5 refutation/selection now build under 6G/two threads/default maxHeartbeats 200000. Scoped target Lang.Proofs.Contextual.ProvenanceExperiments (17 jobs), log CX-P9-experiments-3.log.
2026-10-20 WORKLOG: hbox logs/CX-P9-plants.py is the sequential mutation driver; logs/CX-P9-plants.pid names its own Python process. Source is restored in finally after each mutation; no landing/judge launched. Def-only scratch probe logs/CX-P9-probe.lean avoids importing stale proof artifacts. Seventeen mutations target guard, budget, typing, complementary products, absorption and its three literal sets, edit polarity/missing edits, repair specialization/consistency, nogood lookup/whole-subset matching/hypothesis supports, P5 refutation, selection.

2026-10-20 GREEN: all 17 mutants built successfully and then failed semantic Lean probes; control and restored probe GREEN. Read EVERY full mutant output and every build output. Diagnostic control scanned error|unbound|No such file|Traceback: 42 expected Lean diagnostic lines, zero harness errors. Restored source byte-equals all saved pre-mutation originals. No running mutation or landing remains.
2026-10-20 EVIDENCE: hbox logs/CX-P9-plant-{guard,budget,typing,complements,absorption,positive-subsumption,negative-subsumption,env-subsumption,edit-polarity,missing-edits,repair-env,repair-consistency,nogood-bypass,nogood-partial,hypothesis-support,refutation,selection}.log. Each log's line 1 is a REAL failure captured from the Lean run. Sixteen begin with the decide tactic proving a proposition false; refutation begins with Application type mismatch at probe line 65, rejecting refuted versus open. All include the complete rejected proposition or constructor equality. Exact indexed diagnostic capture: logs/CX-P9-plant-diagnostics.txt. Driver: logs/CX-P9-plants.py; finished PID recorded at logs/CX-P9-plants.pid. Restored scoped build: logs/CX-P9-plant-restored-build.log, probe: logs/CX-P9-plant-restored.log (empty, exit 0 in driver log). No scratch deleted.

## VACUITY READ — all 52 new theorems (2026-10-20, CX-P9 self-read)
Read the actual statements and proofs. This is the lane's self-read, NOT ROOT's independent second reader. Landed statements are untouched. All universe/instance parameters are substantive: the generic results apply to arbitrary CalculusData/World/retained candidate lists; the concrete teeth use the actual cmttData checker. Empty collections are lawful edge cases, never an assumption used to discharge the general results. No theorem claims typing soundness from an unchecked CalculusData.

DISJUNCT CHECK applied to every row: the only explicit conclusion Or is in mem_changes (an iff characterizing two signed cases). Neither branch follows from just a token/monomial or just a world: the positive case needs support membership AND false liveness; the negative case needs blocker membership AND true liveness. Instances exercise each separately. Every other row has an equality, inequality, conjunction, forall/exists, or iff without an escape disjunct. Concrete conjunctions are computed observations, not purported universal results disguised by a true disjunct.

| Theorem (under Nanodregg.Lang.Contextual.P9, except Experiments as noted) | Vacuity/evidence read |
|---|---|
| provenance_env_specialized | Actual false-to-true env edit; absent old monomial AND new verified candidate. Built first. |
| monomial_verified | Independent original judge versus deferred literal evaluation; includes typing, guard, both token signs and budget. |
| provenance_iff | Arbitrary retained polynomial reused at every environment; membership pins witness to cs. No selected-candidate premise. |
| specialize_eq | Exact old-polynomial equality, including order/multiplicity; not mere implication of success. |
| provenance_update | Consumes actual Edit.apply; specialization law corollary, explicitly not incremental-performance evidence. |
| monomial_complementary_dead | Both polarities force inconsistent liveness; premises inhabited by [t]/[t], arbitrary env. |
| provenance_complementary_dead | Transfers complementary impossibility to original judge, with effective hypotheses included. |
| eval_consistent | A genuinely evaluated product cannot contain complementary literals. |
| subsumes_iff | Executable subset test characterization; labelled algebraic helper, no repair claim. |
| subsumes_trans | Three independent products, literal-inclusion composition. |
| subsumes_eval | Smaller obligations follow from larger satisfied product; all three literal components used. |
| minimal_subset | Algorithm cannot invent an explanation; membership gives an original product. |
| minimal_eval | Both directions of existential validity survive computed absorption; nonempty teeth expose deletion errors. |
| minimal_covers | Each input product contains a retained product, not only successful inputs. |
| provenance_minimal | Arbitrary surviving pair cannot be a strict inclusion; multiple incomparable products occur in experiments. |
| label_iff | Original judge remains equivalent after BOTH complementary deletion and absorption. |
| tokenEdits_live | Actual applyAll interpreter; arbitrary initial accumulator, duplicate tokens assign one target polarity. |
| tokenEdits_env | Frame property of token edits, not environment synthesis. |
| mem_changes | Exact signed membership iff; two branches need different live bits and corresponding membership (disjunct check above). |
| changes_satisfy | EnvOK and noncomplementarity do not already make supports live; computed edits establish it. |
| repairs_of_provenance | Membership in repairable specialization produces an original candidate verified after actual edits. Not claimed for impossible raw env literals. |
| changes_necessary | Successful arbitrary update contains every false original literal's required flip. |
| provenance_of_repair | Every repair yields a retained monomial with a subrepair; no prior candidate choice hypothesis. |
| minimal_repairs_of_provenance | Global minimality turns subrepair inclusion into set equality; duplicates/order irrelevant. |
| repairPlans_sound | Returned algorithmic plans execute to verification; no caller-supplied soundness predicate. |
| repairPlans_cover | All successful updates contain a computed alternative. |
| repairPlans_antichain | Two actual output plans cannot strictly include one another. |
| repairPlans_minimal | Global minimality among ALL successful token updates, obtained via coverage, not only pairwise output comparison. |
| repairPlans_complete | Every globally minimal repair appears up to token-set equality. |
| residualRepairPlans_minimal | P4 residual's saved world/problem used, with actual lookup; returned alternatives have the general minimum guarantee. |
| findNogood_sound | Found core actually recorded and fully contained; no arbitrary evidence accepted. |
| findNogood_complete | Any fully contained recorded core is detected, including the empty one. |
| judge_respects_nogoods | Actual judgeRecorded status becomes conflict with a recorded core regardless of liveness; missing-support tooth. |
| nogood_never_suspended | Distinguishes conflict from any suspended token list, not just one concrete missing list. |
| judgeRecorded_verified | Original verification plus no recorded inconsistent subset, both directions. |
| recordedLabel_iff | Same consistency-aware judge and label at every env. |
| recordedRepairs_sound | Computed recorded-policy repairs verify through that very judge, not only the old one. |
| recorded_refuted | Recorded core membership/subset and non-verification at ALL worlds; relative to policy, candidate-specific, not proof of logical False. |
| select_respects_nogoods | Operational refusal despite possible old verification; names exact retained candidate and interface. |
| Experiments.environment_literals_retained | Guard and budget candidates retained symbolically; false/true specialization differs. |
| Experiments.computed_minimal_repairs | Exact [[a,b],[c]], eliminating complementary/over-budget/strictly larger alternatives. |
| Experiments.computed_repairs_execute | Both alternatives run actual edits; omitted blocker deletion leaves pruned status. |
| Experiments.token_repairs_respect_environment | False env and excessive cost produce no token repair, explicit capability limit. |
| Experiments.absorption_and_complements | Concrete larger explanation and complementary explanation both removed. |
| Experiments.nogood_beats_missing | Original suspended versus recorded conflict for same candidate/world, real boundary. |
| Experiments.recorded_repairs_and_refutation | Policy changes plans and produces exact recorded refutation; unrelated missing support stays open. |
| Experiments.nogood_matching | Empty nogood always matches; unrelated nogood does not. |
| Experiments.recorded_selection_refused | Original select succeeds after repair; recorded select refuses same candidate because of DB. |
| Experiments.nogood_checks_hypotheses | Empty explicit supports cannot hide a used token-backed context hypothesis. |
| Experiments.residual_computes_repairs | P4 residual consumer returns real alternatives; unknown hole distinguished. |
| Experiments.typing_stays_checked | Ill-typed CMTT variable enters neither polynomial nor repair plans. |
| Experiments.absorption_reads_all_literals | Negative and env obligations cannot be silently ignored; partial nogood membership insufficient. |

2026-10-20 WORKLOG: implementation is eight NEW Lang files only, plus append to decisions/lang.md (LANG-P9) and generated SIZE.md. Totals +811 Lean lines (+189 deployed), +52 theorems, +8 modules (+5 proof modules). No old Lean file or theorem touched; no foreign path, no pins/wire/gates/ceilings changes; no ASK item or design approval pending. ROOT's independent theorem reader is still required before landing. scripts/commit --help is unsupported on this revision (unknown flag); read the actual scripts/commit usage header instead. It was not launched to land.

2026-10-20 GREEN: final source gates all pass (closure/refusals/size/paths/runs/rebase/tcb/vectors/waste/owners/targets), logs/CX-P9-source-gates-final.log. Draft and all generated sources read back; no placeholders. No existing Lean source changed; decisions/lang.md is a pure +107-line append. Source totals +811 lines, +52 theorems; all 17 mutation originals match restored source. No running lane job remains.
READY 2026-10-20 CX-P9: /tank/dregg-build/nanodregg/wt/CX-P9, detached b72e5a8. Scoped build GREEN, source gates GREEN, 17 mutation teeth RED with restored GREEN; 52 per-theorem disjunct reads above.
CHANGED: Lang/Contextual/{Provenance,ProvenanceRepairs,Nogoods}.lean; Lang/Proofs/Contextual/{Provenance,ProvenanceRepairs,Nogoods,ProvenanceTeeth,ProvenanceExperiments}.lean; decisions/lang.md; generated SIZE.md. Exact landing paths: /tank/dregg-build/nanodregg/logs/CX-P9-paths.txt (excludes generated SIZE.md as required).
DRAFT MESSAGE: /tank/dregg-build/nanodregg/logs/CX-P9-message.txt. ROOT must supply the independent second reader and land; no premise additions or ASK items pending.
DONE 2026-10-20 CX-P9. Landed hashes: none, as instructed; prepared work remains uncommitted for ROOT.
