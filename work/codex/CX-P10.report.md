## WORKLOG
2026-10-20 — Started CX-P10; no landing authorized. Created detached worktree /tank/dregg-build/nanodregg/wt/CX-P10 at b72e5a8 via main's actual Git directory (parent nanodregg is not a repository). Disk /tank: 308G available. Read lane rules, brief, CHARTER, OWNERS, relevant literature §2.11/§4.2/§4.12, and CX-READER-ACT2 complete-observation HIGH. Read original Mokhov–Mitchell–Peyton Jones ICFP 2018 PDF online (author-hosted build-systems-original.pdf), Def 2.1 p79:3 and §4.2.2 pp79:14–15; the named PDF is absent from paperbin. New code will use a finite keyed environment projection to construct guards, retain actual observed values (no hash-collision assumption), include all positive/negative token reads, and distinguish missing observations from pinned absence at its checked observation boundary. Existing loose holePackage is concurrent work, not silently certified by this extension.
2026-10-20 PRICE PREMISES — Landed theorems gaining a hypothesis: none. Landed statements restated: none. New cache-correctness statements require the cache coherence invariant, established by initialization and preserved by refresh. Finite read-set completeness will be established by construction, not assumed of an arbitrary guard.
2026-10-20 WORKLOG — Trace + TraceExamples data/proof modules now build GREEN (logs/CX-P10-build9.log, 6G/two threads, default finite heartbeat cap). 21 generic theorems plus 14 executable CMTT teeth/invariant statements so far. checkedJudge_sound derives exact world judgment from successful capture and authenticity of PROVIDED observations; there is no completeness premise. Scope: the adapter is executable Lean, but current main has no StdHole files, and the concurrent activities tree owns that unlanded generator. No existing package receive-path repair is claimed. Read activities/StdHole.lean through holeVerdictCheck and main Rel.relReads to confirm the exact integration boundary. Next: appendix docstrings, mutation teeth, source gates and decision/message drafting. No background helper or judge is running.
2026-10-20 WORKLOG — Correction to earlier interim count: final code has 34 new theorems, 20 generic + 14 concrete teeth/invariant statements. Five landed Lean files have trailing add_decl_doc commands only; a byte-prefix audit against HEAD passes for every landed path. All landed theorem names, types and proof bodies are unchanged. The appendices name from-scratch consistency, Davies–Pfenning closedness, Doyle IN/OUT-list ancestry, and AGM recovery's same-proposition distinction. Read Davies–Pfenning PDF's text p.7, Stein Thm.6.1 text, and AGM original p.513; Doyle full-paper retrieval returned HTTP 429, so its ancestry is based on the supplied literature note and the original article's bibliographic page range, not a claimed direct full-paper read.
2026-10-20 VALIDATION — hbox logs/CX-P10-docbuild.log: scoped build GREEN (92 dependency jobs, 6G/two threads, finite default 200000 maxHeartbeats). logs/CX-P10-control.log: real isolated tooth source GREEN. Eight mutations in CX-P10-plants.py each compiled before the tooth ran; all eight entire tooth outputs and mutant-build logs read. Restored source GREEN in CX-P10-restored.log. logs/CX-P10-gates1.log: all 11 source gates GREEN, including closure C3, ownership and refusals. No new gate, ceiling, pin, wire or Store change; no key material touched. All work is unlanded.

### Real mutation evidence
All paths below are under /tank/dregg-build/nanodregg/logs/. Each mutation source is retained as CX-P10-mutant-<name>.lean. The helper restores the definition in finally; no mutation remains. No detached job or PID file was needed; every job was foreground and finished normally. The grep control found only expected Lean theorem errors, no unbound variable, missing file or Traceback.
- guard-trace: CX-P10-plant-guard-trace.log:1, actual `Tactic decide proved that the proposition ... is false`; removed environment observation, breaking unchanged_status_cutoff, guard_change_propagates and repeated_fillings_once.
- support-trace: CX-P10-plant-support-trace.log:1/5, same real kernel error; dropped effective supports, breaking both explicit-support and context-hypothesis withdrawal.
- blocker-trace: CX-P10-plant-blocker-trace.log:1, same kernel error; omitted negative dependency, breaking blocker_assertion.
- always-dirty: CX-P10-plant-always-dirty.log:1/4/7/10; unrelated edit, same-value write, precise log and refreshed-trace second pass all become false.
- never-dirty: CX-P10-plant-never-dirty.log:1/4/9/13/17/21; real guard/support/blocker changes and duplicate-candidate logging become false.
- no-cutoff: CX-P10-plant-no-cutoff.log:1; input change incorrectly propagated despite equal output, refuted by unchanged_status_cutoff.
- stale-trace: CX-P10-plant-stale-trace.log:1; cache status updated but old trace retained, refuted by updated_trace_stays_clean.
- missing-blocker: CX-P10-plant-missing-blocker.log:1/10, actual `Tactic rfl failed` on missing-token refusal after replacing omitted blocker by observed false. Both the allowed-guard and failing-guard coverage teeth fail. No fake diagnostic was used as input.

### Per-theorem VACUITY READ, including the DISJUNCT CHECK
Read every statement against its definitions and proof. None has an Or conclusion, unbounded collision escape, or unrestricted existential witness standing in for the computed output. Iff conclusions were checked in both directions. Structural lemmas and concrete computations below are identified as such, not advertised as independent semantic invariants.

Lang/Proofs/Contextual/Trace.lean (20):
- evaluate_observe: equality of the complete computed status with the landed judge for arbitrary candidates/worlds; no success premise. Definitional factorization, not an admission theorem by itself.
- guard_reads_only: equality on declared input keys yields equality of actual installed guard results; arbitrary environments, terms, and guard programs. Its premise does not assert guard equality.
- observation_complete: equal complete finite observations imply equal entire judgments; the observations include both signed token lists. Does not assume judgment equality or global world equality.
- collect_sound: successful actual collection plus authenticity of supplied values yields exact ordered values AND coverage of every declared key. Coverage is concluded, never assumed. Empty lists are a base case, not the only inhabitant.
- collect_total: constructs actual collection success for any total reading function; no prior success premise. This inhabits the boundary's positive path.
- collect_missing: any missing declared key rules out every successful output. Membership and absence are independently satisfiable; concrete blocker and environment omissions exercise them.
- seed_valid: initialization establishes the cache invariant by construction. Classified as a constructor invariant, not a separate claim about arbitrary forged caches.
- refresh_valid: cache coherence is preserved in both actual branches; dirty caches must be re-evaluated. Clean-branch reuse of its invariant is not a disjunct permitting dirty-branch bypass.
- refresh_consistent: a coherent trace at any prior observation yields actual new-world judgment after refresh. No premise supplies the new judgment or a dirty/clean flag.
- repair_entries: exact list traversal equation; preserves candidate order and identifies each actual refresh call. Structural helper, not a claim about value correctness.
- from_scratch_consistency: all actual pass outputs equal fresh judgment in order, for arbitrary coherent entries and new worlds. Cache validity refers to stored trace values, not the requested new world.
- repair_minimal: iff between actual log membership and an in-range candidate whose trace differs. Existential is bound by original list lookup; no arbitrary candidate can discharge it. Both clean and dirty examples occur.
- repair_once: actual rejudgment log has no duplicate index for every candidate list, including duplicate fillings. Operational claim is limited to the structural pass; it does not assert a time bound for verification scans.
- tagged_filter: generic list-algebra equality used by capture_sound. No semantic admission claim, no fallback branch.
- capture_sound: successful collection and authenticity of PROVIDED values yield the exact complete observation of the world. Neither completeness nor a supplied status is assumed. Missing blocker mutation breaks the premise-to-output mechanism as tested independently.
- checkedJudge_sound: any successful checked judgment equals the actual old judge at the world on the constructed guard interface. Result status arbitrary (including refusals-as-status); does not assume verified. Authenticity is distinct from completeness and remains a receiver obligation.
- checkedJudge_total: complete world observations produce the exact old judgment, without any success premise; avoids a soundness-only function that always refuses.
- changed_iff: actual changed-output log iff retained-index lookup and unequal before/after computed status. Existential bound by lookup; no alternative return permits unconditional dirty propagation.
- early_cutoff: fresh judgment equality plus valid cached entry yields empty dirtyReaders for the hole reading its index. The hypothesis compares semantic judgments, not the dirty flag or output log; the conclusion checks propagation. It covers both clean and genuinely rejudged candidates, with the latter concretely witnessed. The consumer observes status only, with a fixed selection index.
- repair_valid: every actual pass entry remains coherent, enabling repeated repairs. Membership ties the output to the computed pass; no witness substitution.

Lang/Proofs/Contextual/TraceExamples.lean (14):
- unrelated_environment: key 99 edit produces an empty rejudgment log for candidate-specific keys 0 and 1; always-dirty mutation refutes it.
- equal_value_write: writing the existing value produces empty work, independently of an edit being issued.
- unchanged_status_cutoff: key 0 changes 1→2; actual log is [0] AND downstream dirty list is empty. Both conjuncts compute; this is not an escape disjunction.
- updated_trace_stays_clean: a second pass after the equal-output refresh has no work; stale-trace mutation refutes it.
- guard_change_propagates: key 0 changes 1→0; statuses are exactly conflict guardFails / verified AND only reader 7 is dirty.
- support_withdrawal: withdrawing declared support 1 computes suspended [1] / verified, not a generic negative label.
- hypothesis_withdrawal: withdrawing token-backed used hypothesis 2 computes suspended [2] / verified, exercising effSupports beyond explicit support lists.
- blocker_assertion: asserting blocker 3 computes pruned [3] / verified, exercising negative read completeness.
- omitted_blocker_refused: absent observation (none) of blocker 3 computes Missing.token 3; false-by-default mutation fails it.
- observed_absence_accepted: explicit observed false for that blocker computes verified, distinguishing absence from omission and inhabiting acceptance.
- omitted_environment_refused: missing declared key 0 computes Missing.environment 0.
- failing_guard_still_requires_coverage: missing blocker refuses even though supplied guard values would fail; early status computation cannot bypass coverage.
- repeated_fillings_once: two identical retained candidates generate distinct indices [0,1], each exactly once.
- cached_valid: proves both actual initialized entries satisfy the generic consistency invariant. Constructor-invariant witness, not independent package soundness.

2026-10-20 WORKLOG — Draft decision is appended as LANG-P10 in decisions/lang.md; message /tank/dregg-build/nanodregg/logs/CX-P10-message.txt and exact landing paths /tank/dregg-build/nanodregg/logs/CX-P10-paths.txt. SIZE.md generated, not an explicit landing argument. Source gates GREEN, placeholders scan clean; final whitespace cleanup touched appended blank lines only and prefix audit stayed GREEN. Scope/integration caveat is in decision and message, not hidden in this report. ROOT's second-reader review and integration/landing remain ROOT-owned; no lane was spawned and no judge was launched.
2026-10-20 FINAL VALIDATION — Exact final source scoped build GREEN in /tank/dregg-build/nanodregg/logs/CX-P10-final-build.log; all 11 source gates GREEN in CX-P10-gates-final.log. git diff --check clean. Generated/append-only content and message contain no __N__/TODO/XXX placeholders. Final prefix audit preserves every byte of each landed source/decision prefix. SHA256 manifest: logs/CX-P10-sha256.txt. Size: +4 modules, +2 proof modules, +601 Lang lines (+179 deployed), +34 theorems; max non-foundation dependents unchanged at 310. Disk remains 308G available. All foreground helpers finished; no processes or judges remain.

Changed paths (relative to the worktree):
- Lang/Contextual/Closure.lean — appended Candidate documentation only.
- Lang/Contextual/Trace.lean — new trace/observation/checking implementation.
- Lang/Contextual/TraceExamples.lean — new CMTT fixtures.
- Lang/Proofs/Contextual/Core.lean — appended box_ambient_free documentation only.
- Lang/Proofs/Contextual/Judge.lean — appended reissue_never_reenables documentation only.
- Lang/Proofs/Contextual/Protocol.lean — appended from-scratch consistency documentation only.
- Lang/Proofs/Contextual/Repair.lean — appended from-scratch consistency documentation only.
- Lang/Proofs/Contextual/Trace.lean — new 20-theorem proof module.
- Lang/Proofs/Contextual/TraceExamples.lean — new 14-theorem executable examples/invariant module.
- decisions/lang.md — append-only LANG-P10 decision and verification.
- SIZE.md — generated view; omit from scripts/commit explicit paths.

2026-10-20 READY — /tank/dregg-build/nanodregg/wt/CX-P10 at b72e5a8; final scoped builds and source gates GREEN; 34 theorem disjunct reads and eight real mutation teeth recorded above.
2026-10-20 READY — Changed paths: /tank/dregg-build/nanodregg/logs/CX-P10-paths.txt; drafted message: /tank/dregg-build/nanodregg/logs/CX-P10-message.txt. Complete-observation adapter is proved; concurrent Std.hole receive-path integration is not claimed.
DONE 2026-10-20 — No landed hashes: landing deliberately left to ROOT. No running jobs.
