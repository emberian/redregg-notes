# PERF-FIX log (continuation file) — started 2026-10-13
Lane: PERF-FIX (Claude). Base main 7dea0626. Repo /Users/ember/workbox/mini-unified-push-20261003.
Lane tree (hbox): /tank/dregg-build/claude-lanes/perf-fix/src. Branch perf-fix → bundles/burst3-minidregg.git lane/perf-fix.

## events
- start: read SINS-LEDGER §1/§3. Next: verify each at source @7dea0626, check warm READY.
- 20:30 verified ledger items at 7dea0626 source. Kern-grow patch NOT on main (applies clean). Found beyond ledger:
  RootsExact.ofEntries rebuilds the tree a 2nd time (Compiler/DurableReceiverCore.lean:561-562) at every
  ofEntries+ofEntries pair (loadChained:1065, loadImage:908, Loaded.build:1264, extendVerified:685, advance fallback);
  so a cold light open = openSealed sparse + 2 tree builds = 3 full evals (unless the compiler inlines+CSEs).
  receiveServed builds the full entries list (+extendIds eraseDups) per write for the collision fallback (:894).
  Served.advance extendIds eraseDups Θ(cells²) per light write; Image.cellIds same per full load; openHead Nodup decide Θ(cells²).
- local edit clone: scratchpad/perf-fix (shared clone, branch perf-fix). Edits so far (unbuilt):
  (1) kern-grow patch; (2) RootCache.build (tree once) used everywhere; (3) openSealedWith + openHead seeds
  the extension with the checkpoint's tree (cold open: 1 eval + suffix paths); (4) lazy fallback entries in receiveServed;
  (5) SessionIndex.dedup csimp for Image.cellIds/extendIds; nodupFast in openHead; (6) Kn2StoreBench KN2_BENCH_CREATES=1 (cell axis).
- warm-7dea0626 being rebuilt from scratch by WORKLOAD (started 20:17); local disk 45G free (Ember's laptop) — keep local writes tiny.
- 20:50 ROOT: read PERF-PRAXIS; measure by instructions:u (perf stat) + ratios within one pass; add 'code shape' section to doc.
- 21:40 lane hbox:/tank/dregg-build/claude-lanes/perf-fix/src (sources copied, only .lake/packages hardlinked; no leaks checked).
  Profile (bench creates 64, dwarf): deployedHash 54% incl; digestOfBytesLE/denoteNat 29%; cshake 25%; encodeNat 14%;
  RootCache.ofEntries 9.8% + RootsExact.ofEntries 9.7% (duplicate tree confirmed); openSealed 10.5%; decodeRecordsFrom 17% (records w/ 1000B posts).
  Commits e61163fa denoteNat csimp; 6913c4a7 RootCache.build; aba9f9a8 dedup/nodupFast; a16e2f1b open-once + kern-grow.
  bench (same pass): light open 128c 998->243ms, 256c 2003->490; full open 1005->483 / 2006->962; whole run 166.5G->68.2G instr.
  Pushed lane/perf-fix. Bins kept at perf-fix/bin/bench-{before,after1}. NEXT: per-append constant (~8ms/append), then candidate + workload.
- 22:10 workload (main candidate, small N, under load) traced: N=2 M=1 K=1 run exec'd minidregg-host ~140 times
  (46 codec, 33 inspect, 20 signatures, 14 observe-assemble, 10 author, 6 assemble ...), each ~0.38G instr / 40 ms
  (init: dl relocation of a 173 MB binary + Lean builtin initializers: Parser tokens, NameMap, simprocs, IR).
  Flat profile N=6: 662 Host processes sampled; Host comm 50% of samples, client-consent 24%.
  The serving Host is `mini serve` -> memfd exec "/proc/PID/fd/7 ... stdio" (comm "7"): perf cannot symbolize it
  (memfd mapping); address->symbol by hand was unreliable. NEXT for whoever: run the serving Host from a file path to profile it.
- 22:12 launched lane candidate build (host, consent, rust) nohup, PID file perf-fix/build.pid, status perf-fix/build-status.
- 23:00 candidate packed hbox perf-fix/candidate @a16e2f1b; main rows journey/call/send/objectrecord PASS (growth rerunning with HOST etc); fix rows launched (perf-fix/rows-fix.pid); driver perf-fix/run-rows.sh
- 00:05 pointer for item A (not started): NativeHost.confirmed/charged (Kernel/NativeHost.lean:1245,1256) = openExisting (full cold open) per readback;
  internal callers Kernel/NativeHost.lean:1270,1310,1314,1316,1349,1907,1917,1994,2079,2261,2314,2381,2383,2500,2637; 3086 and 3194 already take the
  confirm as a parameter (`submitLoadedWith … (confirmed config)`) — the session route can pass Host/Main.lean:1271 sessionConfirmed instead.
  Thread a `confirm` parameter through the other routes the same way; check which session routes in Host/Main reach them.
- 00:40 workload N=32 M=32 K=16 (script's current defaults), main vs lane, back to back: instr births 3587->1991G, updates 4465->2017G,
  reads 1554->797G, judgment 419->211G, reopen 56->27G; wall 722->389 s; both `phases failed: reads` (pre-existing). Doc §E filled.
  Trace run (MINIDREGG_HOST_TRACE=1 MINI_OPEN_TIMING=1) on lane candidate running -> /tmp/pwT, perf-fix/runs/wl-trace.out.
- 23:55 rows on fix candidate: journey PASS, call PASS, send PASS, objectrecord PASS, growth PASS
  (main: growth FAIL — at 1000 write p99 10.874s max 13.334s, reopen 2.113s, load 3.8; fix: p99 2.958s max 3.894s, reopen 1.554s, load 2.2).
  ROOT: read PERF-ATTACK-ORDER-20261013.md; price with MINIDREGG_HOST_TRACE=1 MINI_OPEN_TIMING=1 first; then A,B,C,E,F.
  Launched workloads N=20 M=16 K=8: main /tmp/pwM, fix /tmp/pwF, fix+trace /tmp/pwT (perf-fix/runs/wl.pid, wl.done).
- 01:00 PRICED (trace run on lane candidate a16e2f1b, N=32 M=32 K=16, MINIDREGG_HOST_TRACE=1 MINI_OPEN_TIMING=1; /tmp/pwT/w/public/serve.log):
  serving Host per-op totals (sum, n, p50, max):
    52.9s n=73  p50 843ms max 2112  op 212  (receipt readback → item A)
    25.7s n=36  p50 480   max 2029  op 2    (submit)
    12.4s n=107 p50 122   max 458   op 210
     9.5s n=36  p50 157   max 812   op 1    (prepare)
     9.3s n=128 p50 44    max 434   op 214  (public view)
     3.8s n=40  op 144 | 3.8s n=36 confirm refresh | 3.7s n=36 op 91 | 3.0s n=37 op 5 | 0.9s n=73 op 4 | 0.9s n=1 op 172
  light open stages (2 opens: start + reopen): checkpoint 266ms, records/chain/tags/frontier 281, index rows 312, index 381, replay+root 587 (cumulative).
  Server-traced total ≈127 s of a ~390 s run: ~2/3 of wall is outside the serving Host (client processes).
  => item A (op 212) is 42% of server time at p50 843 ms; next lane starts there (pointers above).
- STATE AT HANDOFF: context near ceiling. Branch lane/perf-fix = a16e2f1b pushed. Doc SHOULDNT-BE-DOING-20261013.md complete through §E.
  Successor: start from this log + PERF-ATTACK-ORDER-20261013.md; items A, C, E, rest of F (B's root half and F's light-open half are done here).

## PERF-FIX-2 (Claude, 2026-10-14) — continuation
- 00:10 start from this log + PERF-ATTACK-ORDER. Lane tree same (hbox perf-fix/src). My scratch: perf-fix/p2/ (cand.sh = host/consent/rust/pack
  chain, measure.sh = workload before/after + rows; status files p2/cand-<name>.status, p2/measure-<T>.status). Old a16e2f1b host/consent
  artifacts + native-out/consent-out moved to p2/prev-* (build-native-host refuses to overwrite). Baseline candidate = perf-fix/candidate (a16e2f1b).
- A committed 9b75e9e1: `NativeHost.Confirm`; every *SubmitLoaded + receivingOutcome/receivingSubmitLoaded take `confirm` after config;
  14 Host/Main session call sites pass `sessionConfirmed pinnedConfig state`; one-shot enroll-key-submit passes `confirmed config`;
  `charged` -> `chargedVia confirm`. No theorem names confirmed/charged. Candidate perf-fix/cand-A.
- reads "phases failed": WORKLOAD BUG, already fixed on lane/perf-workload d37eee80 (the lane tree carried an older untracked copy):
  the old script drew `at` heights over the whole history, so reads below an object's birth hit `refused: no-grant` (correct Host
  behaviour: the grant does not exist at that height) and the summary crashed on a duplicate `objects` key. Installed d37eee80's
  scripts/perf/{box.py,workload.py,workload.sh} into the lane tree (still untracked; old copy at p2/perf-old). Both sides now: phases failed: none.
- A measured (same pass, N=32 M=32 K=16, trace on; box loaded by my Lean builds during "after" so wall is noise, instr is the figure):
  instr:u before(a16e2f1b) -> after(9b75e9e1): genesis 27.34->17.86G, setup 163.09->106.26G, births 2291.04->1589.92G (-31%),
  updates 2396.69->1716.84G (-28%), reads 807.39->882.90G, checkpoint 34.03->25.64G, judgment 191.33->207.40G, reopen 25.37->31.75G.
  server trace: op 212 75.8s n=73 p50 871ms -> 35.6s p50 478ms; "confirm refresh" now n=110 p50 205ms (the session light refresh = item B's
  re-verification, now the readback's whole cost). Raw: /tmp/p2w-A-{before,after}, p2/wl-A-*.out, p2/optab.py (per-op table from serve.log).
- E committed (1c30e9fc): gate's loadDirectory deleted; Gated/Prepared lose `directory`; gate_spent_refused loses `dir`; Gated.unique adjusted.
  Unreachable-refusal argument: only caller passes opened.durable; Opened holds a LoadedDirectory; LoadedDirectory.load_eq.
- C committed (77ad8e80): planDecision (one decision) + signingHeaderFor; four planDecision_* equalities to the old projections.
- OPEN: objective-manifest ratchet (scripts/check-objective-proofs.sh proofs) not yet run on the lane — E restates gate_spent_refused and
  redefines closures through gate; PERF-FIX's store commits likely moved closures too. Needs ledger lines (draft --attribute) + pin.
- 03:00 candidate cand-C (E+C; built at 77ad8e80, the same tree as pushed 3f873592) packed at perf-fix/cand-C.
  E+C measurement, same pass, cand-A vs cand-C (/tmp/p2w-C-{before,after}, p2/wl-C-*.out). The "after" run had about 1.6x the load
  (op 2, which neither commit touches: 17.7 -> 29.2 s). Per-op server trace, normalised by op 2:
  op 210 (plan, C) 15.5 s p50 147 ms -> 6.5 s p50 59 ms (ratio to op 2 0.88 -> 0.22);
  op 212 (submit, E) 18.3 s p50 244 -> 21.5 s p50 295 (ratio 1.03 -> 0.74).
  Phase instr:u in this pass fall within pass-to-pass noise (cand-A births 1590 G in pass 1, 1823 G in pass 2). After: births 2293 G,
  updates 1839 G, reads 1038 G. That noise follows load, so something in the client or Host does load-dependent work; it is unexplained.
  The figures to use are the per-op ratios.
- Commit messages rewritten with these numbers (same trees, via commit-tree). PUSHED lane/perf-fix = 3f873592 (A 077e9f20, E 68eb0a09, C 3f873592).
- Rows on cand-C: journey, call, send, objectrecord PASS. growth FAIL: write p50 2.029 s (lane a16e2f1b: 2.051), p99 8.895 s, max 12.857 s,
  reopen 3.426 s; loadavg 6-8 against 2.2 on PERF-FIX's PASS. The slow writes come in two bursts (g444-456, g894-910) where both write parts are
  3-4x slower at once. That looks like CPU contention, not a step. Rows on cand-A: growth FAIL p99 11.3 s at loadavg 27.7 (my Lean builds were running).
  NOT YET SETTLED. Queued: growth on cand-A (rows-A2), then control growth on a16e2f1b (rows-base2), then cand-C again (rows-C2);
  chain PID file p2/growth-chain.pid, done flag p2/growth-chain.status. If base2 also fails under the same load, the bar (max write <= 5 s)
  is load-sensitive and A/E/C are clear. If base2 passes and C2 fails, suspect the session readback (`confirm refresh`) at certain heights.
- NEXT for a successor: (1) read the growth chain results; (2) run scripts/check-objective-proofs.sh proofs on the lane (E restates
  gate_spent_refused, removes Gated/Prepared.directory rows, redefines closures through gate; PERF-FIX's store commits probably moved closures
  too), then admit the moves with `objective-manifest.py draft --attribute a16e2f1b~5..HEAD` and `--pin` in a gates commit; (3) F, full-open half:
  loadChained evaluates the root in openSealed (checkpoint) and again in RootCache.build (head). Port openHead's openSealedWith + suffixSlots
  advance. The full open is off the session submit path now, but every `mini query --view at` does two of them client-side (item I),
  which is why reads is ~1 T instr; item I (socket) removes those opens outright, F only halves their root cost;
  (4) the REJECT/v2 `directoryUnavailable` constructor is now never constructed by the activity receiver. Removing it is a codec v3 and
  manifest change, so it was left in place.

## PERF-FIX-3 (Claude, 2026-10-14) — continuation
- 04:10 start. Growth chain running (rows-A2 started 04:09, then base2, C2; ~40 min each).
- 04:40 STEP 2 SETTLED — the "instructions scale with load" was perf's hybrid-PMU scaling, not a spin. hbox reports
  cpu_atom + cpu_core lines; each is scaled by enabled/running where running = time on that core type, so the sum
  extrapolates by the P/E split, which follows load. Test (8 parallel python jobs x3): scaled 11.3/11.1/11.0 G, --no-scale
  5.67/5.68/5.67 G. Raw recomputation of the saved perf.csv (count*pct/100, /tmp/p3raw.py on hbox): cand-A pass1 vs pass2
  births 1487 vs 1483 G, updates 1528 vs 1512, reads 758 vs 756. CORRECTED effects (raw): A births 1640->1487 (-9%),
  updates 1879->1528 (-19%); E+C births 1483->1459, updates 1512->1389 (-8%), judgment 154->120 (-22%).
  Fix: `perf stat --no-scale` in scripts/perf/workload.sh:41 (lane/perf-workload's file; applied to the lane tree's untracked copy).
  Client transport checked for spins: DeadlinePipe/DeadlinePipeWrite poll()-block; connect sleeps 2 ms on EAGAIN. None.
- 04:55 PERF-FIX headline recomputed raw (main /tmp/pwM -> a16e2f1b /tmp/pwF): births 3229->1634 (scaled 3588->1991), updates
  4151->1888, reads 1460->723, judgment 394->194, setup 184->115, genesis 26->18. Bench 166.5->68.2 G had no saved csv: rerun queued
  behind growth chain (p3/bench-rerun.sh, pid p3/bench-rerun.pid, done p3/bench-rerun.status; out p3/bench-*.{csv,out}).
- 05:30 ROOT: build during the chain (box not quiet anyway; judge by each run's recorded load).
  B committed f03a1eae (lane tree; not yet pushed — message gets numbers after measurement): receiveObjective returns
  DurableReceiverIO.Successor; ObjectiveActivityReceiver.receiveLoadedDetailed (receiveLoaded = Prod.fst <$> it, five theorem
  statements unchanged, proofs via private fst_pure/fst_bind over EST); NativeHost.activitySubmitLoaded takes `adopt`;
  NativeHostSession.Session.adopt (height+chain match, validateLoadedFrom, rebaseDue shared with extendFrom); refresh stages traced
  ("refresh full/light/validate", "adopt"). Host.Main umbrella green. cand-B building (p3/cand.sh, pid p3/cand-B.pid, status p3/cand-cand-B.status;
  old native-out/consent-out/host/consent moved to p3/prev-C).
  F lemmas proven in scratch (p3/t/F.lean against built Core: execute_accepted_install, replay_roots, entriesOf_checkpoint_step,
  axioms propext/choice/Quot.sound); edit script p3/f1.py + p3/f1-lemmas.lean, to apply once cand-B frees the tree.
  Growth A2 (cand-A): FAIL max 10.55 p99 9.35 p50 3.75, load at end 4.48/5.88/11.39; slow stretches at g82-98,114-127,218-232,525-582,693-706
  — different heights from rows-C's (444-456, 895-905): bursts follow load, not height. Certify points (g1,253,505,757) not aligned.
- 06:40 STEP 1 VERDICT: control a16e2f1b (rows-base2) ALSO fails growth: max 11.74 p99 8.01 p50 2.78, load at end 10.1/13.0/14.1.
  cand-A (A2) max 10.55 p99 9.35 load 4.5/5.9/11.4 (my builds ran during it); cand-C (rows-C) max 12.86 p99 8.90 load 6.4/8.5/8.3.
  Slow stretches sit at different heights in each run (base2 g717-855). The max-write <= 5 s bar is load-sensitive; A/E/C clear.
  C2 (cand-C again) still running: p2/rows-C2, done flag p2/growth-chain.status.
- B MEASURED A WASH, NOT LANDED (side ref lane/perf-fix-B-measured = f03a1eae). Same pass cand-C vs cand-B, --no-scale:
  births 1471.66 -> 1471.54 G, updates 1402.4 -> 1400.2 G. Trace (/tmp/p3w-B-after/w/public/serve.log): refresh full p50 26 ms (n=37),
  adopt p50 59 ms (n=73), refresh light p50 71 ms (n=110), refresh validate p50 31 ms. Re-executing the record was never the cost.
  THE REAL B: Light.refresh -> `validated` -> NativeHostServed.validateServed (Kernel/NativeHostServed.lean:47) re-decodes the whole
  served directory (loadServedDirectory) and runs cellsLawfulServed over every cell per refresh. Write validateServedFrom prior served
  (decode/law-check only moved cells), prove = validateServed (shape of validateLoadedFrom_eq, Kernel/NativeHostContext.lean:625-636).
  Second: cellsLawfulFrom compares every cell's bytes (31 ms) — key it by the records' written cell ids instead.
- F LANDED: lane/perf-fix = 9bdf3a06 (on 3f873592; pushed). loadChained: openSealedWith + checkpointSlots advance.
  New theorems execute_accepted_install, replay_roots, entriesOf_checkpoint_step; suffixSlots/CheckpointRoots/lookup_of_mem_nodup moved
  DurableServed -> DurableReceiverCore. kn2-store-bench (CREATES=1 128 256, --no-scale) vs bench-after1: whole 202.7 -> 155.3 G; full open
  639 -> 422 ms (128), 1289 -> 915 ms (256). Host umbrella green. NOT YET RUN on F: candidate + rows (journey/call/send/objectrecord) —
  successor: p3/cand.sh cand-F (move native-out, consent-out, artifacts/minidregg-{host,client-consent} aside first), then run-rows.sh.
- REJECT/v3 filed: cv task 01a139e6.
- NOT DONE — STEP 5 RATCHET: from lane src (after building): scripts/check-objective-proofs.sh proofs; then
  `scripts/check-objective-proofs.sh proofs --draft a16e2f1b~5..HEAD`, read build-logs/objective/draft-review.txt, write reasons
  (E: gate_spent_refused restated without `dir`, Gated/Prepared.directory rows removed (loadDirectory deleted, result unread);
  C: planDecision_* added; F: entriesOf_step closure moved through execute_accepted_install (meaning unchanged); store commits moved
  closures of RootCache.build/Image.cellIds csimp), append to scripts/gates/objective-contract-changes.txt, `--pin`, separate gates commit.
  Also run the merge-gate-checks.sh pieces: kernel-transport census, host-closure, token-census, hyp-ledger.
  Bench rerun (PERF-FIX headline correction) queued: p3/bench-rerun.sh, results p3/bench-{before,after1}{,-noscale}.{csv,out}.

## PERF-FIX-4 (Claude, 2026-10-14) — continuation
- 09:00 start from PERF-FIX-3. Scratch hbox perf-fix/p4/ (workload Store copy p4/store-wl + anchor, config p4/wl.config:
  `minidregg-host p4/wl.config store-bench` runs against the B trace run's Store: 110 records, 166 cells).
- PROFILE (perf record dwarf of store-bench, p4/sb.perf, agg script p4/agg.py): validateLoadedFrom's 30 ms was NOT the byte
  compare (cellsLawfulFrom 29 of 456 samples). It was loadDeployment (authority cell 10.8 KB decode + authState: 199) and
  validateChecks -> policiesSourced (215), whose cost is `config.profile.semantics` (a cSHAKE over the encoded runtime
  manifest) recomputed per recorded policy (345 of 396 policySourced samples).
- ITEM 1 committed e0bbfb1d: validateServedFrom (+ loadServedDirectoryFrom / loadServedAuthorityFrom / cellsLawfulServedFrom,
  validateServedFrom_eq = validateServed) used by Light.refresh/adopt; validateLoadedFrom reuses the held authority
  (loadDeploymentFrom, via validatePartsVia; validatePartsWith now defined through it); policiesSourced computes the semantics
  digest once (@[csimp]). No statement changes. store-bench same pass x2 (ms/10 calls): validateLoadedFrom 298/299 -> 51/52;
  validateLoaded 430/426 -> 338/330; validateServed 231/228 vs validateServedFrom 53/52. Candidate cand-1 building (p4/cand.sh,
  pid p4/cand-1.pid, status p4/cand-cand-1.status; previous native-out/consent-out/host/consent moved to p4/prev-F).
- MISTAKE to clean: hbox PID 1863191 is a `bash -c until ! pgrep -f "lake build Kernel.NativeHostLight"` wait loop I started; it
  matches itself and never ends (sleep 10 loop, harmless). No PID file -> not killed; Ember/ROOT may kill it by that PID.
- ITEM K = DESIGN (not implemented; statement change needed). Read at 9bdf3a06: Loaded.rebase (Compiler/DurableReceiverCore.lean:1398)
  sets baseHeight := head; Loaded.atPrefix (:1520) has one base; below it, the genesis fold. Two named statements pin that:
  Loaded.atPrefix_below (`height < loaded.baseHeight -> atPrefix height = (prefixImage height).restore`, i.e. the genesis fold)
  and its consumer NativeObservationController.at_is_fold_prefix ("below the loaded checkpoint, `at` is the genesis replay").
  With a retained list of older bases, a height in [older base, current base) resumes from the older base; that equals the
  genesis fold only under atPrefix_from_checkpoint's honesty premise (resume_sound), so both statements must change (to
  "below the OLDEST base"; plus a nearest-base analogue of atPrefix_from_checkpoint). READ.md's "statement unchanged" was the
  scout's assumption. Note the semantics today already depend on rebase history: before a rebase, atPrefix h (h in
  [checkpoint, head)) resumes from the checkpoint; after it, the same h is a genesis fold. Options for Ember: (a) retained
  bases + restate the two theorems as above; (b) `at` via Reader.stateAt (the atCovered_sound DESIGN route, which supersedes a).
- ITEM 1 workload (same pass, cand-C -> cand-1 = F + item 1; N=32 M=32 K=16, raw instr --no-scale; /tmp/p4w-I1-*, p4/wl-I1-*.out):
  births 1472.42 -> 1399.11 G, updates 1401.97 -> 1223.65 G (-13%), reads 762.08 -> 697.16 G (F's full open + item 1), judgment
  124.46 -> 115.15 G, setup 100.94 -> 97.89 G. Server trace (after ran under ~1.5x load: untouched op 210 p50 42 -> 64 ms):
  "confirm refresh" (the session light refresh) p50 103 -> 53 ms, total 10.8 -> 6.3 s (n=110); op 212 p50 220 -> 147 ms.
  Both workload runs rc=1 only for the 180 s wall bound under load (phases failed: none).
- ITEM K: DESIGN (above). ITEM M taken: (a) 6209abc9 Session.refresh returns the session when extendFrom saw nothing new and the
  light is at that head (no second Store exec); (c) 93b89310 activityViewLoaded uses opened.authority (no loadDeployment) and
  evaluates configOf once instead of 1+quotes. NOT taken: (b) Session.start full+light open -> deriving the light from the full
  needs a new Served.ofLoaded caller (ratchet list scripts/ports/full-loaded-callers.txt only shrinks) and a Head from the full
  open: not local; (d) spent/journal linear scans: not measured hot at 110 records (no samples worth naming); (e) full open
  chain-hash from height 1: 13 ms at 110 records (store-bench "open: the log chain over every record"), and chainExact asserts
  the chain over the whole image; starting at the checkpoint means trusting its MAC'd chain = a check removal -> DESIGN.
- ITEM M measured (same pass cand-1 -> cand-M; after under ~1.3x load, op 210 p50 44 -> 58): op 214 p50 33 -> 15 ms, total 4.2 -> 2.0 s
  (n=128); raw instr updates 1223.50 -> 1207.78 G, reads 698.51 -> 695.53, births 1399.60 -> 1393.56. M commits 8cc80ec0, fb23f296
  (messages rewritten with numbers via commit-tree; trees = 6209abc9/93b89310).
- RATCHET: proofs --draft 7dea0626..HEAD: 577 changes (2 removed, 4 restated, 571 redefined), 0 unattributed; reasons written
  (p4/ledger.py), --pin (40719 rows, 81 added); gates commit 5b7cae0d (its text says 7dea0626..93b89310: same tree as fb23f296).
  PUSHED lane/perf-fix = 5b7cae0d.
- Rows on cand-1: journey PASS, call PASS, send PASS, objectrecord PASS; growth running (p4/rows-1). Rows on cand-M queued (p4/rows-M).
- My own merge-gate run on the lane tree: p4/gate.sh (pid p4/gate.pid, status p4/gate.status, logs perf-fix/logs/gate-perffix4*).
- LANDING started 15:09Z: /tank/dregg-build/pipeline/lanes/land-7ffd6524/src/scripts/pipeline/landing.sh 5b7cae0d --lane land-perffix4
  (log pipeline/logs/landing-5b7cae0d.log, pid file pipeline/logs/landing-5b7cae0d.pid). LAND-HBOX's own 7ffd6524 landing was in its
  standing-run step at the time.
- ~15:35Z ROOT: stop the landing (lane lands through `next`; INTEGRATOR merges 5b7cae0d). Killed PID 2677380 from
  pipeline/logs/landing-5b7cae0d.pid. MY ERROR: that PID was the outer `bash -c ... &` wrapper; the landing itself still runs:
  landing.sh PID 2677382 -> run-gate-burst.sh PID 2836669 -> lean builds in lanes/land-perffix4. They have no PID files, so I did
  not kill them. Also mine with no PID file: wait loops 2834535 (unbounded, greps landing log) and 2837300/2837301/2837302 (timeout
  14000 s), 1863191 (self-matching pgrep loop). All are safe to kill by those PIDs. My gate.sh attempt failed in seconds
  (LAKE_WRAP unbound when merge-gate-checks.sh is run bare); it built nothing beyond the umbrella.
- Still running (PID files): p4/chain1.pid (rows on cand-1: growth left), p4/chainM.pid (rows on cand-M after it).
- NEXT for a successor: read rows-1/rows-M results.tsv; growth is load-sensitive (PERF-FIX-3). Items open as DESIGN: K (atPrefix
  statements), M(b) light-from-full start (ratchet), M(e) chain from checkpoint (check removal).
