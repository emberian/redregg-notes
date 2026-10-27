# CENSUS-REVIEW log (lane census-review, base next 0125b224)
- 10-14 16:40 start. Brief: review every "layer-1 review pending" TokenCensus row; remove the pending tier.
- At 0125b224: Table has 403 rows: 12 L1, 391 L2, 371 "review pending", 3 restrict rows (FOLLIES' 417 = rows ADDED since 10-01; 371 remain pending at next).
- Lane clone: hbox /tank/dregg-build/claude-lanes/census-review/src, branch lane/census-review off origin/next.
- 17:00 review fanned out to 6 Opus reviewers (scratch .../scratchpad/cr/BRIEF.md, out/batchN.tsv); batch2 done: 51 L1, 3 L1-NEW, 4 WRONG.
- Instrument redesign drafted (scratch cr/edit): TokenCensus/Core.lean (machinery), TokenCensus.lean (census run, no plants),
  TokenCensus/SelfTest.lean (401 forgeries + restriction plants), 4-column rows `ctor | home | L1 <thm> / defect <cv task> | reason`,
  no L2, no kind column (encapsulation/no-guarantee privates lose `private`). NEW check: an L1 witness must name an index at an
  EXPLICIT position (x.field mentions every param implicitly, so the old index check passed `x.committed`-style statements).
  Gate: defect rows ratchet (only shrink, set-based vs FROM); plants + plant-script modes only when the instrument changes.
- 17:40 REVIEW DONE (391 L2 rows; verdict TSVs hbox census-review/review/out/batchN.tsv): L1 207 existing field + 134 new witness
  theorems (L1-NEW) = 341; WRONG 21 (cv 01a13c42-48cc..4dd5, map review/tasks.tsv); NOT-A-TOKEN 19 + ENCAPSULATION 9 -> private dropped;
  StoreIdentity -> new layer `restricted ofOpen,ofScratch` (reviewer missed its restrict rows; dropping private would weaken check 6).
  26 L1 rows with partial guarantees (IO-only signature verdicts etc.) -> one cv task 01a13c42-7613.
  Consistency: ApplicationLifecycleRetryCompletionV4Report.Checked moved L1->WRONG to match its 3 identical siblings.
- Commits (unpushed yet): 6 batch commits on lane/census-review (old 5-col grammar, WRONG rows L2 "defect cv"), then the census commit
  (instrument + 4-col table) pending build. Reasons sanitized (" -> ') since the table is a string literal.
- Build: warm .lake = full cp -a of pipeline/lanes/land-7ffd6524/src/.lake (no hardlinks); slow on loaded tank.
- Pushed the 6 batch commits (2287f581) to mirror + GitHub lane/census-review (hbox has a deploy key now).
- build1: 3 failures out of 134 new witnesses + Core (Core `let mut found ← match` parse; PFP insert landed inside a 2-line field;
  CDR needed CredentialAuthorityPolicyRegistry.storedCapabilityDigest). build2: Assurance.NativeAcceptedFixture refused its honest
  call (probe: admitRun -> Reject.objectiveSource). CAUSE: the FrontEnd witness was inserted into Compiler/ObjectiveBendFrontEnd.lean,
  a file fingerprinted byte-for-byte into ObjectiveBendFrontEndIdentity.identity; the recorded package names the old identity.
  FIX: the witness lives in ObjectiveBendFrontEndIdentity.lean (not fingerprinted), with a note. build3 running.

## CONTINUATION (paused 10-15 for the usage wall)
- Branch lane/census-review @ 95861a59 (GitHub + hbox mirror; verified with ls-remote). Clone: hbox
  /tank/dregg-build/claude-lanes/census-review/src (warm .lake = full cp of land-7ffd6524; built through build 2).
- Commits: 6 batch commits d4a8..2287f581 (reviewed rows, old grammar) + 95861a59 WIP census instrument (UNVERIFIED).
- Running at pause: build 3 = `with-lean-slot swarm-build lake build TokenCensus`, attached to an ssh from the Mac session;
  log census-review/build3.log (ends with EXIT=<rc>). It may have died with the ssh. Last verified state: build 2 green except
  Assurance.NativeAcceptedFixture (FrontEnd fingerprint; fix is in 95861a59).
- Successor first: (1) read build3.log; if no EXIT line, rerun build 3 (same command, attached, under the slot). (2) Fix any red:
  likely L1 witnesses the NEW explicit-index check refuses (faults name the row), or census faults; a refused witness means either
  a better field or the row is really a defect (open a cv task, `defect <id>`). (3) `lake build TokenCensus.SelfTest` once.
  (4) Run plant modes: for m in positive ignored-index tautology closed unlisted-minter old-rule implicit-index pending-layer
  unlisted-vacuous; bash scripts/kn2/plant-token-census-v2.sh $m (each must print its expected red / positive green).
  (5) Check scripts/check-build-closure.sh + lean-build-surfaces.py accept TokenCensus/Core + SelfTest; objective-proofs ledger will
  list restated/redefined for the 134 new theorems + privacy drops (admit as 0125b224 did). (6) Squash WIP into a clean census commit
  message (drop WIP), push mirror + GitHub, report counts to ROOT.
- Review data: hbox census-review/review/out/batchN.tsv (verdicts), review/tasks.tsv (ctor -> cv task), cv 01a13c42-7613 (gaps).

## 10-16 BUILD 3 NON-TERMINATION — diagnosis (build-free, by reading 95861a59)
- I started build 3 WITHOUT A PID FILE (census-review/build.pid = build 2's shell 2317424; cp.pid = the copy). Reported NO PID FILE to
  ROOT; with-lean-slot pid 2772377 / lean TokenCensus.lean pid 3285761 (39 h, 100% CPU) is Ember's to stop. Lesson: the attached
  form `echo $$ > build.pid` was used for build 2 only; build 3 copied the command minus the PID write.
- build3.log ends at `Built AxiomCensusResearch`: every dependency built; the hang is TokenCensus.lean's own `#assert_token_census`.
  The plants are NOT in this module any more (SelfTest), so the plant enumeration is not the cause.
- CAUSE (derived from the code, not measured): check 3 calls `l1WitnessFaults` once per L1 row, and its `trivialConclusion` runs
  `whnf conclusion` and, for an Eq conclusion, `isDefEq lhs rhs` at DEFAULT transparency; and `isDefEq type conclusion` per Prop binder.
  At 0125b224 that ran on 12 rows. The review made 341 rows L1, and 77 of those witnesses are `*Exact` equation fields of the form
  `x.field = <deployed function of …>` (codec encodes/decodes, Sha256/identity digests, worldRoot, requestDigest, allocate …).
  `isDefEq` on such a pair lazily delta-unfolds the closed or partially closed side through the deployed hash/codec (the
  POSEIDON2/SHA "reduction bomb" class: one permutation under whnf = tens of GB/hours), and `set_option maxHeartbeats 0 in
  #assert_token_census` (TokenCensus.lean:32) removes the only bound. So one witness's triviality test can run without end.
  Suspect #2 (lower): `explicitFVars` is a `partial def` that walks the Expr TREE with no visited cache; on a DAG-shared conclusion
  it is exponential. Conclusions are small and implicit args are skipped, so this is less likely than the defeq.
- FIX (successor; no build until written): (1) `trivialConclusion` decides triviality SYNTACTICALLY: `withReducible` for the whnf and
  both isDefEq calls (reflexive `a = a`, `True`, a repeated premise are visible without unfolding anything deployed). (2) Bound each
  witness: run `l1WitnessFaults` under `withTheReader Core.Context ({· with maxHeartbeats := 2000000})` (or catch the heartbeat
  exception) and turn a timeout into a FAULT naming the row ("witness statement too expensive to inspect"), never a hang. Keep
  `maxHeartbeats 0` only for the outer scan. (3) Memoize `explicitFVars` (a `StateT (HashSet Expr)` or `Expr.forEach`-style
  visited set). (4) Then rebuild TokenCensus ONCE with a PID file (`nohup … & echo $! > census-review/build4.pid`, a parent that
  stays alive for with-lean-slot), expecting ~1100 s minus the plants.
- 10-16 FIX APPLIED (Mac, build-free; pushed to GitHub lane/census-review b11020da, NOT the hbox mirror):
  5c1b63da triviality test reducible-only (withReducible + whnfR; comment names the class); 8c2df180 per-witness heartbeat budget
  (witnessHeartbeats 400000; tryCatchRuntimeEx turns exhaustion into a fault naming the witness), perConstant fresh counts for every
  scan call and each self-test plant, maxHeartbeats 0 removed from TokenCensus.lean and SelfTest.lean; b11020da explicitFVars memoized
  (StateT HashSet Expr). Checked: Core.lean elaborates alone (lean 4.30); smoke file: PW.sound passes, implicit-index and x = x fault by
  name. NOT checked: the tree build (INTEGRATOR-4 builds it with a PID file).

## CENSUS-2 (successor, 2026-10-17, burst5)
- Lane: burst5 /srv/lanes/census-2/src (mk-lane census-2, branch lane/census-2 off lane/integrator-batch2 5b4f5b99).
  Build script /srv/lanes/census-2/tc.sh <tag> (with-lean-slot from /srv/lanes/cf-new/src/scripts/pipeline: the installed
  /srv/pipeline/scripts copy refuses, its lake-cache-audit gets --tree '' because /srv/pipeline/scripts is not a git tree;
  /srv/pipeline/slots/with-lean-slot symlink can't find lib.sh), timeout 2200, PID files logs/<tag>.pid, logs/<tag>.log.
- 04:26Z baseline at 5b4f5b99 REPRODUCED: `token census failed (70)`, ~16 min (deps fetched from the lake cache).
- Fast row check: /srv/lanes/census-2/l1check.lean (`#l1 ctor home witness`, the census's own l1WitnessFaults; 3 s).
- Instrument (Core.lean): the L1 branch resolves the row type from the constructor's own inductive and a private witness
  as mkPrivateNameCore home (private structures Walked/SuffixWalked/CachedRoots carry `_private.` names: 3 of the 6
  "does not exist" were name resolution, not missing theorems). New plant mode `private-structure` (gate list updated).
- Mine: CertifyReceiver/ClockTickReceiver rows named `Prepared.certified_advances`/`Prepared.clock_monotone`; the theorems
  are top-level `CertifyReceiver.certified_advances`/`ClockTickReceiver.clock_monotone` (pass). CachedRoots.sound (private,
  ids.Nodup ∧ RootsExact cache entries). `mints:` for Held.of, Fronts.of (compute their value, exact by rfl/construction),
  AcceptedCellEffect.toReceiptEvent (argument = public proof-field structure). NB justifiedMinters reads up to the next `;`
  then splits on `,`: `mints:` must END the note (a parenthetical after it is parsed as part of the name).
- Fan-out: 6 Opus row lanes census-2-{a..f} (brief /srv/lanes/census-2/BRIEF.md; groups group-{a..f}.txt). Handed back:
  a 9 L1 (2432a124), b 11 L1 (2b254204), c 12 L1 (6d903e42), e 8 L1 + 1 defect 01a14819-4402 (b933f153;
  ResourceObservationAdmission.Prepared: marker/capability/contextBytes phantom, ~40 consumers). Pattern a/b: conjunct
  `validateLoaded config (exactCandidate old derived ready) = .ok readback.after` (ExactReadback.validated) names config.
- Defect ratchet: main cfb68bf9 has no TokenCensus/Core.lean, so batch 3 (FROM=main) SKIPs token-census-defects.
- Lanes d (613964e9: 9 L1 + defect 01a1481a-f045 CapabilityRenounce.PreparedOn; `bound` field on 3 Accepted types) and f
  (f68e6461: 9 L1; HistoryBcsGameSecurity phantom indices dropped; 4 silently-dropped declarations restored, cv 01a1482c-b713).
  Gaps ticketed (not faults): 01a14831-bfba, 01a14831-bfcb.
- r2 (a,b,c,e + mine): 19 faults = exactly d+f's rows. r3 05:20Z GREEN at 86f01584.
- [usage wall 05:20Z-09:18Z]
- Squashed 1ba54216; INTEGRATOR-5 rebased batch 2 to 441cccf8 -> lane/census-2 d540d0b3 (clean rebase); r4 09:34Z GREEN:
  "token census: 379 private constructors, all listed, none minted abroad; 356 L1 rows backed by their witness; 23 reviewed
  defects" (355 L1 + 1 restricted + 23 defects).
- 5ff346b8: old-rule plant matched the pre-change Core line (no-op, its grep refused) -> repointed.
- 1ce5571b gates(objective): 53 decision lines (40 added, 9 redefined MEANING CHANGES for `bound`, 3 restated Accepted.mk,
  RenewLegs.sound restated stronger); --pin: "40 added, 403 redefined, 4 restated; 0 unadmitted"; "pinned 41331 rows";
  self-tests a,b (theory, mathlib), c, d, e, f PASS.
- Plants: EXIT 0 positive ignored-index tautology closed unlisted-minter implicit-index pending-layer unlisted-vacuous
  private-structure SelfTest (at 1ba54216), old-rule + positive (at 1ce5571b). scoped-unlisted RED: TokenCensus.Fixtures is
  red on known-red NativeAcceptedFixture 01a146dd (same 5 native_decide pins at 441cccf8; INTEGRATOR-5 confirmed).
- Process hygiene: an early op.sh kill orphaned 3 children (no PID file; timed out at 3600 s). Fixed: /srv/lanes/census-2/job.sh
  starts every job as its own session/process group and writes the PGID (kill -- -PGID; removes a stale pidfile first).
- cv 01a14806-97c3 DONE. lane/census-2 = 1ce5571b (GitHub + /srv/git), in INTEGRATOR-5's batch 2.
- Lane trees on burst5 (mine): /srv/lanes/census-2, census-2-{a..f}, census-2-p{1,2,3}. Not deleted.
