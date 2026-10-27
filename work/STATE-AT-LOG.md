# STATE-AT log (continuation file) — started 2026-10-14
Lane: STATE-AT (Claude), lane name state-at. Items: SINS-LEDGER §1 D1 (closure-chain snapshot, list-snoc history), D2 cell
table as a list (coordinate with STORE-ROOT via ROOT: one checkpoint-shape change), D7/item K (past reads replay from genesis;
route `at` through the nearest kept checkpoint; restate at_is_fold_prefix / atPrefix_below / atCovered_sound; plant: tampered
kept checkpoint refuses by name).

## events
- start: read SAFETY-BLOCK, SINS-LEDGER §1, perf-trace/READ.md, PERF-FIX-4 item K design, STORE-ROOT-LOG.
- ROOT rulings: base on main 30a5009a (mirror `next` is stale); checkpoint = one World shape, codec owned by TURN-LOG; MY part =
  cells MAP representation as a named sub-codec + equality theorems TURN-LOG imports; do NOT bump the checkpoint tag. (b) now.
  Send TURN-LOG (via ROOT) the exact representation within the day.
- lane tree hbox /tank/dregg-build/claude-lanes/state-at/src (git clone of mirror; .lake/build cp -a from perf-fix@5b7cae0d (private copy,
  0 shared), .lake/packages cp -al). Branch state-at @30a5009a.
- ROOT: STORE-ROOT-2 owns RootCache/RootsExact (moving to Kernel/WorldRootCache.lean) — do NOT edit them; rest of DurableReceiverCore mine.
- (b) CODED (unbuilt at this line): Compiler/DurableCheckpointCodec.lean + openSealedRooted (additive, = openSealed paired with worldRoot);
  DurableReceiverCore: Loaded.atPrefix DELETED -> Loaded.Kept (key field; MAC/root/key-id via openSealed; sealed root = rootLog[h-1])
  + Loaded.atPrefixFrom kept h + theorems atPrefixFrom_{current,below,kept,from_checkpoint} + IO Loaded.keptAt (refuses by name
  "past state refused: the kept checkpoint at N ..."); NativeObservationController: atBytes/atCovered/queryResult take `kept`;
  at_is_fold_prefix gains `kept` + `unused` premise (kept:=none => old statement verbatim); new at_is_fold_prefix_kept (honesty premises);
  NativeHost.keptFor + both queryLoaded (NativeHost, OpeningCache) read kept after admission. Bench: Host/Kn2StoreBench KN2_BENCH_AT=1.
- build w/b1 (lake build Kernel.NativeObservationOpeningCache Kernel.NativeHost) started ~11:50; NO pid file (my ssh backgrounding slipped):
  it is rebuilding most of the tree because perf-fix's .lake is downstream of e61163fa (Bignum). Should have used warm-7dea0626's .lake.
- sent ROOT the CellTable sub-codec proposal (Kernel/CellTable.lean, Std.TreeMap Nat bytes, ascending-id canonical stream, get_ofList bridge).
- (a) PLAN: CellTable module + @[csimp] State.snapshot = snapshotFast (TreeMap for roots/bytes, HashSet for spent) — statements unchanged;
  history snoc/journal lookups: measure after (b) before touching generic Snapshot.
- b2: everything through NativeObservationController built green; Kernel.PayEnrolReceiver SIGTERM (143, load 40, earlyoom?) — rerun as b3 (pid w/b3.pid)
- ROOT: all Lean builds via /tank/dregg-build/pipeline/slots/with-lean-slot (w/build.sh switched after b3)
- 13:05 b4 GREEN (Kernel.NativeObservationOpeningCache Kernel.NativeHost Host.Kn2StoreBench, 3542 jobs). PLANT PASS:
  scripts/kn2/past-checkpoint-tamper.lean (lake env lean --run, helper w/store-helper = perf-fix/bin/minidregg-link-sqlite-store):
  controls at 10/35/20 = genesis fold; flipped MAC -> "does not open (badMac)"; row16 := cp32 -> "names height 32";
  dishonest seal under the Store key -> "differs from its log entry's root" (also proves honest sealed root == log tag root).
  b5 = lake build kn2-store-bench (exe) running.
- bcbb415a committed (b) on branch state-at (message numbers pending). cand-b candidate building (w/cand.sh, pid w/cand-b.pid, status w/cand-cand-b.status). benches m1 (1000 3000, genesis compare) m2 (10000 30000 kept only) running (w/m*.pid, .out, .perf)
- m1 numbers INVALID (genesis 0 ms): the pure `force` lets floated out of the timed span. Bench fixed with IO.lazyPure (uncommitted in
  tree: Host/Kn2StoreBench.lean); m2 killed by its PID file; b6 (bench exe rebuild) waits for a Lean slot behind cand-b's host build.
  m1 still useful: records 1000 open 184 ms / 3000 open 644 ms; kept checkpoints found at 192/448/704/1472/2240 (nearest ≤ h) as designed.

## CONTINUATION for (a) (successor or me after renewal) — context ~255K at this line
State: (b) = bcbb415a on branch state-at (lane tree hbox /tank/dregg-build/claude-lanes/state-at/src, base main 30a5009a). Not yet pushed
(push after numbers: amend message with bench + rows; push mirror lane/state-at + GitHub lane/state-at).
(a) NOT STARTED in code. Design (sent to ROOT for TURN-LOG 12:xx):
 1. Kernel/CellTable.lean: `abbrev CellTable := Std.ExtTreeMap Nat (List UInt8) compare` (EXT tree map: extensional Eq via
    ext_getElem?, needed so decode∘encode = id holds as Eq). get t c := t[c.value]?; ofList = foldl insertIfNew (first wins = Seed.lookup);
    entries = toList mapped to CellId ascending. Theorems: get_ofList (= Seed.lookup), ofList_entries, entries_ascending, get_insert.
    Lemmas live in Std/Data/ExtTreeMap/Lemmas.lean (getElem?_insertIfNew :703 @[grind =], ordered_keys_toList :856,
    getElem?_ofList_of_mem :1312, ext_getElem? :3834). Toolchain v4.30.0.
 2. Compiler/CellTableCodec.lean: cellTableStream (nat count, (nat id, bytesStream) ascending; decode refuses non-ascending/dups).
    TURN-LOG imports it into the World checkpoint; I don't bump tags.
 3. Runtime: @[csimp] State.snapshot = State.snapshotFast (roots/canonicalBytes via CellTable built once from state.cells with
    first-wins; consumed via Std.HashSet of prefix nullifiers). Statements unchanged. Prove field-wise funext.
 4. Measure first, then decide on generic Snapshot.history (List snoc, Θ(h)/install) and journal lookupRecorded (Θ(h)/execute):
    both are Θ(h) per record, so Θ(h·63) per kept-checkpoint read; only change the generic Snapshot if the bench names them.
 RootCache/RootsExact: STORE-ROOT-2's; never edit.
- ROOT asked CellTable-alone vs TURN-LOG-2 defines it: answered TURN-LOG-2 defines from my spec (context 255K); I adopt.
- c1629626 = (b) + bench lazyPure fix (amended). b6 green; cand-b relaunched; benches m3 (1000 3000 + genesis) m4 (10000 30000 kept) launched.
- m3 (same pass, ms, kept vs genesis): 1000: at250 7/14, at500 7/55, at750 10/126; 3000: at750 9/135, at1500 11/616, at2250 9/1597. m5 = 10000 with genesis launched.
- m5 10000 (same pass): at2500 kept 15/genesis 2515 ms; at5000 25/11262; at7500 15/27853. chain.sh (pid w/chain.pid) waits cand-b then rows journey call send objectrecord growth -> w/rows-b/results.tsv
- 14:xx PUSHED d951d57a (= c1629626 tree, message with numbers) to mirror lane/state-at. GitHub push from hbox: no key -> ROOT pushes. Pending: m4 (30k), cand-b + rows (chain.sh).
- m4 30k (kept only; ms): at7500 kept 30, at15000 59, at22500 165 (vs ledger 56.6 min; genesis at 30k NOT measured — extrapolating m5's
  quadratic, at22500 ≈ 9×27.9 s ≈ 250 s in this bench). 10k rerun: 78/10/14. 30k open 6565 ms, grow 1354 s.
  The kept read still grows with h (30 -> 165 ms): Θ(h) terms = prefixImage take, State.snapshot spent flatMap/history map/journal,
  lookupRecorded (journal walk) and consumed (`∈ spent` list) per replayed record => (a) item 3/4 targets, measured.
- 14:50 cand-b host build still queued for a Lean slot (log empty). chain.sh (pid w/chain.pid) will run rows when cand finishes:
  results -> /tank/dregg-build/claude-lanes/state-at/w/rows-b/results.tsv (status w/rows-b.status). NOT YET OBSERVED.
- STOPPING at ~270K (cap). Successor: (1) read rows-b results; if any row red, diagnose (only `at` reads + query path changed);
  (2) objective-manifest ratchet: scripts/check-objective-proofs.sh proofs --draft 30a5009a..HEAD, reasons = the statement list in
  d951d57a's message, --pin, separate gates commit; (3) adopt TURN-LOG-2's CellTable; then (a) items 3-4 per CONTINUATION above.
  Open mistakes: none running without PID files except — none (b1's build ended). m*/cand/chain all have PID files in w/.

## STATE-AT-2 (successor, started 10-14 ~14:40 EDT)
- read log + SAFETY. cand-b still queued (host log empty); chain.sh alive (PID w/chain.pid). lane/turn-log has NO CellTable -> defined it.
- 2da79e71 kernel(CellTable) committed + pushed mirror lane/state-at (standalone `lake env lean` green, axioms clean). ROOT told.
- bench edit (uncommitted, in tree): KN2_BENCH_STORE=DIR reuse (store in DIR/N, appends numbered from tip), at-heights = 64m+32
  (fixed 32-record suffix so the curve isolates h), best-of-3 at reads, "append alone" timing. w/benchk.sh NAME N.. (EXE=binary).
  w/base.sh (PID w/base.pid): b7 build bench -> w/bench-base -> mb baseline 1000 10000 30000 into w/stores (grows once, ~27 min).
- DESIGN (a): spec Snapshot/DataSnapshot unchanged (50+ consumers). Runtime: an Engine (CellTable bytes, HashSet spent, HashMap
  journal index, newest-first history) with view : Engine -> DataSnapshot; resume @[csimp] -> engine replay; then Loaded holds the
  engine (snapshot := view, inline) for the live append path. Admissible via HashSet of prefix written ids (eraseDups is O(h*cells)).
- MY MISTAKE: uncommitted bench edit made lane-build refuse cand-b ("commit first"); bench committed 9da33212 (did not compile: mut
  shadow) + fix 11c4226f (mirror). cand-b+rows relaunched: w/chain2.sh (PID w/chain2.pid) -> w/rows-b/results.tsv. Still slot-queued.
- trees: src = lane/state-at (candidate builds ONLY; keep clean). dev = worktree branch state-at-dev (private .lake/build copy) for (a).
  basetree = detached 11c4226f (baseline bench). git identity set in repo config.
- Kernel/DurableEngine.lean: Engine {absent, cells:CellTable, available, spent:HashSet, journal list + recorded:HashSet index,
  historyRev}; view/light; install/ofState/replay; theorems view_install, view_ofState, replay_view, admissibleFast_iff,
  @[csimp] resume_eq_resumeFast. DurableReceiverCore imports it. d1 build GREEN (dev c8a24556 WIP, message pending numbers).
- w/base2.sh (PID w/base2.pid): b8 builds baseline bench in basetree -> mb (1k/10k/30k, grows w/stores) then md1 (engine bench) same stores.
- ROOT: next = 0125b224 exists; rebase lane/state-at onto it at the next clean point (after C1 numbers). STORE-ROOT-2 folds
  openSealedRooted; don't touch. Objective-manifest ratchet: INTEGRATOR does it at merge (decided; C1 changes no def bodies).
- C2 DESIGN (live append flat): Loaded holds `engine` (snapshot := engine.view, inline); Engine.step (journal via index, preflight on
  light) replaces DurableCheckpoint.prepare on the receive path (Compiler/DurableReceiverIO.lean:250,337; Ready.next is a DataSnapshot,
  so Ready must carry the engine or a proof view next = ready.next); rebase reuses the live engine (no Θ(h) ofState). For at-read
  flatness: heights in the engine (spent: nullifier -> index, Loaded.txs for the journal) so the prefix sets are not rebuilt.
- cand-b (HEAD 11c4226f, = (b) + CellTable + bench) DONE; rows-b: journey PASS (J0-J8,JROT,JROTL,JRLANE,JGATE,JAUDIT), call PASS 63,
  send PASS 192, objectrecord PASS 39; growth pending at this line (w/rows-b/results.tsv).
- dev 468e619b "WIP history newest first": Snapshot.history NEWEST FIRST (install = event :: history; install_history restated
  OLD `(install b i).history = b.history ++ [i.event]` -> NEW `= i.event :: b.history`; new install_history_chronological gives the
  old statement over `.reverse`). Restated sites: Assurance/HyperdocumentAgentRuntimeScheduler (2 thms), Kernel/CarriedSegment
  install_history, DurableCheckpoint.State.snapshot history := (map).reverse, DurableServed history_length (+length_reverse).
  Why not Array: Lean Array.push copies when shared (Loaded snapshots are shared), a cons is O(1) persistent; view is then O(1).
  d2 GREEN (6902 jobs: DurableEngine, DurableServed, CredentialAuthorityDomainReceiver, CarriedSegment, the Assurance three,
  NativeHost, NativeObservationOpeningCache, kn2-store-bench). Umbrella NOT built.
- ROOT/Ember 10-14 evening: STOP per-commit measuring; build the new shape as ONE range, rows + one bench at the END.
  So the two WIP commits (c8a24556 engine, 468e619b history) + C2 are ONE range; squash or keep, one message with the end numbers.
  Baseline for the range: w/base2.sh (PID w/base2.pid) b8 (basetree bench at 11c4226f) -> w/mb.out on kept stores w/stores/{1000,10000,30000}
  (mb grows them once). md1/md2 (w/after.pid) also run — cheap, informational only.

## CONTINUATION (STATE-AT-3) — context ~cap at this line
Do C2 in dev (worktree /tank/dregg-build/claude-lanes/state-at/dev, branch state-at-dev, builds via w/buildd.sh NAME TARGETS):
 1. Loaded (Compiler/DurableReceiverCore.lean:783): field `snapshot` -> `engine : DurableEngine.Engine`; `def Loaded.snapshot :=
    engine.view rootBytes` (@[inline]; view is O(1) now). `resumed : resume … = some (engine.view rootBytes)`. Constructors at
    :908 (loadImage), :1063 (loadChained), :1139 (extend), :1194 (rebase), :1264 (build): need an ENGINE — add
    `DurableEngine.resumeEngine : Option Engine` with `resume = (resumeEngine …).map view` (resumeFast already is that shape).
 2. Engine.step e intent (recorded index + preflight on light + install) with `execute .complete (view e) intent = .accepted (view e')`;
    receive path (Compiler/DurableReceiverIO.lean:250 receiveCandidateWithFresh, :337 Loaded.replay) uses it; on step = none fall
    back to spec `prepare` for the Outcome (refusal/replay path). Ready (DurableCheckpoint:261) carries next : DataSnapshot — give
    extend the engine e' plus `view e' = ready.next`.
 3. rebase (:1185) must reuse the live engine (no ofState over the prefix).
 4. at path: atPrefixFrom still rebuilds prefix sets (ofState: HashSets over h). For flat, index heights: spent nullifier -> first
    index (new Loaded index, admitted per append), journal via Loaded.txs (txid -> first index); ofState bounded by height.
 5. One bench at the end: EXE=<bin> w/benchk.sh NAME 1000 10000 30000 (reuses w/stores) vs w/mb.out; rows via w/cand.sh + run-rows
    (src tree must be CLEAN — lane-build refuses uncommitted tracked changes); put dev commits on lane/state-at in src first.
 6. Rebase lane/state-at onto mirror `next` (0125b224 or its v2 carrying d951d57a+9da33212) at the end of the range.
 Objective-manifest ratchet: INTEGRATOR at merge. Pushes: mirror only (GitHub via ROOT).
- rows-b FINAL: journey/call/send/objectrecord PASS; growth FAIL (step G at 1000: write p50 3.73 p99 11.1 max 75.6 s > 5 s; reopen
  2.8 s; load 24 -> 30-33 / 24 CPUs). (b) touches no write path; PERF-FIX saw growth fail on controls too (max ~11 s). Unattributed;
  decide on the end-of-range candidate at low load. ROOT told.
- mb first attempt FAILED: Store refuses a group-writable anchor dir ("writable by another account"). Fixed: w/stores is mode 700,
  benchk.sh umask 022. Running now: w/bench3.sh (PID w/bench3.pid): mb (baseline, grows w/stores) then md2 (dev 468e619b binary
  w/bench-d2). Read w/mb.out, w/md2.out. md1 never ran validly (ignore md1.*). after.sh exited (md1 rc=1).
- STATE-AT-2 STOPS here (context cap). Successor = STATE-AT-3 from the CONTINUATION block above.

## STATE-AT-3 (started 10-14 ~19:45 EDT)
- read log, SAFETY, HP-DESIGN §0-§3, §5.1. bench3 (PID w/bench3.pid) still growing stores (mb baseline then md2).
- C2 CODED in dev (uncommitted, building): Loaded.engine replaces Loaded.snapshot (abbrev snapshot := engine.view);
  resumeEngine + resume_of_resumeEngine; Engine.execute + execute_eq; Loaded.prepare (+ prepare_eq = spec prepare) on
  receive/replay/audit/differential paths; extend installs into the engine (extend_snapshot: = ready.next);
  rebase TOTAL, keeps engine (DurableEngine.resume_rebase); rebaseD + entriesOf_rebase + seedLookup_map DELETED;
  replay_model/resume_model MOVED HostRefinesWorldCore -> DurableEngine (+ replay_history/resume_history).
  At-read: Engine gains spentBefore/recordedBefore oracles + Thunk journal/history; Engine.ofIndexed + view_ofIndexed;
  Loaded.spentAt/writesAt (SessionIndex.KeyIndex, below_eq); Loaded.admissibleAt; @[csimp] atPrefixFrom = atPrefixFast.
  nodupFast replaces decide Nodup in admissibleFast.
  Restated: rebase_agrees (old: p.rebase = some p' -> agreements; new: p.rebase.snapshot = p.snapshot ∧ height eq),
  represents_rebaseD -> represents_rebase (Represents B p.rebase w), IO Loaded.rebase_image deleted (Core's: total).
- build e1 (w/e1.pid) Kernel.DurableEngine queued on Lean slot (load 40+).
- e1 (DurableEngine target) waited ~70 min for a slot; failed only in SessionIndex (2 proof fixes applied). e2 (PID w/e2.pid)
  = the whole touched set + kn2-store-bench, slot-queued. Slots are the bottleneck (3 slots held by 2-4 h builds).
- e2..e4 iterated proof fixes (SessionIndex KeyIndex, resume_rebase congr, prepare_eq name clash). ROOT: hbox GitHub deploy key
  (pushed 11c4226f to GitHub lane/state-at); burst4-a up. Stopped hbox e5 (its slot waiter's own PID file + e5.pid).
- REBASED the range onto next a5483db3 in hbox scratch clone state-at/rb (branch c2): bench conflict merged (KN2_BENCH_CREATES
  + my KN2_BENCH_STORE reuse); Core reapplied onto next's RootCache.build / entriesOf_checkpoint_step open; my execute_accepted
  deleted in favour of next's DurableReceiver.execute_accepted_install. c2 = d0a8183f, pushed to burst4 shared remote as
  lane/state-at-c2 (hook allows lane/* only). burst4 lane /srv/lanes/state-at (mk-lane), branch state-at-c2;
  build k1 (w/k1.pid) via /srv/pipeline/slots/with-lean-slot. hbox dev tree is stale now (main-based): rb/c2 is the source.
- 10-15 ~05:00: burst4 k5 = touched set GREEN; u2 = UMBRELLA GREEN (Minidregg +Host.Main:leanArts ObjectiveProofs kn2-store-bench,
  13086 jobs) at c2 f7c998b6 (WIP commit amended via hbox w/pushb4.sh; burst4 w/go.sh NAME syncs + builds).
  Late fixes: Loaded.snapshot back to a STORED field + snapshotExact (abbrev made ServedBasis Ground time out: defeq unfolded
  the view and evaluated cSHAKE); DryRun 3 proofs + NativeHostReplay.extendExact rewrite by Loaded.prepare_eq;
  NativeHostReplay.advance/advanceCarriedIntent (the audit/replay walk) now call durable.prepare.
  ROOT told "engine wired".
- END phase: burst4 w/cand.sh cand-c2 (PID w/cand.pid) -> rows on burst4. Baseline bench lane /srv/lanes/state-at-base =
  next + the two bench commits (0d9dbcb8, 5600d263), build w/bb. Bench must run on hbox (perf; burst4 has none).

## PAUSED 10-15 (~06:50) — CONTINUATION (STATE-AT-4)
Branch: lane/state-at-c2 = f7c998b6 on GitHub + hbox mirror (source clone hbox /tank/dregg-build/claude-lanes/state-at/rb, branch c2,
clean). = next a5483db3 + CellTable (fce51951) + 2 bench commits + WIP engine + WIP history-newest-first + WIP C2 (one WIP msg each).
burst4 is DELETED; everything there is gone (its lane, cand-c2, stores). lane/state-at (11c4226f) is the old main-based tip, superseded.
VERIFIED at f7c998b6 (burst4): umbrella `Minidregg +Host.Main:leanArts ObjectiveProofs kn2-store-bench` GREEN 13086 jobs; candidate
host/consent/rust/pack done; rows ALL PASS: journey 200 s (J0-J8,JROT,JROTL,JRLANE,JGATE,JAUDIT), call 63, send 192, objectrecord 39,
growth PASS 1253 s (G at 1000: write p50 1.227 s p99 2.029 s max 3.323 s, reopen 1.520 s; load 7.0->12.1, kn2 benches ran concurrently).
BENCH (burst4, perf instructions:u whole process; same Store per N, base = next+bench commits, c2 = f7c998b6; base grew the Store):
 N=1000:  at224/480/736 kept ms base 7/7/8, c2 8/8/8, base2 5/6/9. instr c2 37.07G vs base2 37.71G (both reuse). append alone 21 vs 40/29 ms.
 N=10000: kept ms base 7/11/16, c2 6/8/10, base2 8/13/15. instr c2 145.95G vs base2 144.03G (+1.3%: open builds HashSets+spentAt/writesAt).
          open c2 1386 vs 1263/1291 ms. FRESH GROW 10k (live append path): c2 216 s / 1.558T instr vs base 288 s / 1.569T (-0.7% instr).
 N=30000: kept ms base 17/28/46, c2 6/11/32 (base2-30000 killed by the pause; no same-pass second baseline).
          open base 4854 / c2 4237 ms; append alone 225 vs 249 ms. instr not comparable (base grew the store: 5.687T; c2 0.431T).
 Reading: at-reads ~2-3x faster at 30k and flatter; the live append/grow instruction budget is NOT moved by the engine (-0.7%):
 the append path cost is elsewhere (store/MAC/root) — say so in the commit, do not claim a grow win.
NOT DONE: (1) objective ratchet: `scripts/check-objective-proofs.sh proofs --draft a5483db3..HEAD` was mid-run (killed by the pause);
 rerun on a box with the umbrella built, write decisions (restated: rebase_agrees, represents_rebaseD->represents_rebase; removed:
 rebaseD, rebaseD_image, entriesOf_rebase, seedLookup_map, IO Loaded.rebase_image, HostRefinesWorld replay_model/resume_model/
 lookup_map_self (moved to DurableEngine); added: the DurableEngine/KeyIndex/atPrefixFast set), `--pin`, gates commit.
 (2) squash the 3 WIP commits into one message with the numbers above + old/new statements + what re-emits (nothing persisted
 changed; no store/codec tag moved). (3) push as lane/state-at (force: rebased off 11c4226f; say so) to mirror + GitHub; report ROOT.
 (4) optional: NativeHostReplay 3602 extendExactReadback + JointControlBootstrapBundle still call spec prepare (cold paths).
SUCCESSOR FIRST STEP: on hbox, clone lane/state-at-c2 into a lane dir with a warm .lake at next (hbox has no next warm base: ask ROOT
 where the warm base for next lives now), build the umbrella once, then do NOT-DONE (1)-(3).
