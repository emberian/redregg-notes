# PERF-MEMO log (continuation file) — started 2026-10-14
Lane: PERF-MEMO (Claude). Item: JUDGE.md item 2 — every loadMethod re-runs the front end on a content-addressed package.
Lane tree hbox:/tank/dregg-build/claude-lanes/perf-memo/src, branch perf-memo @ 5b7cae0d (no `next` on the mirror at 14:50;
.lake/build = full copy of perf-fix/src's (built at 5b7cae0d), .lake/packages cp -al).

## DESIGN (read at 5b7cae0d)
- Gate culture: repo prefers @[csimp] theorems over trusted implemented_by (DurableReceiverCore:1069; check-exports.sh counts
  implemented_by). An IO.Ref memo cannot be csimp. => PURE memo of Thunks, carried as a value; Lean's Thunk caches its value at
  runtime, so a held Thunk forced in one request is free in the next. No unsafe, no implemented_by.
- Carrier: Ambient (ObjectiveKernelConfig, "what the Host knows of the moment a turn is decided in") gains `held : LoadMemo`;
  configOf copies it into Config.held (default {}). Every theorem quantifies over config, so all hold unchanged.
- Replay config pin depends on config only via typeFuel -> `ReplayAt fuel pin` (before Config), `abbrev Replay config pin :=
  ReplayAt config.typeFuel pin`; `replayPackageAt maxBytes fuel stored pin` = old body; LoadMemo entries (pin-keyed) carry
  stored + maxBytes + fuel + Thunk + proof `get = replayPackageAt …` (private mk; only constructor computes it).
  replayPackage config stored pin := config.held.replay … ; theorem replayPackage_eq (= replayPackageAt, any memo).
  Lookup checks entry.stored = stored (exact bytes, no hash premise) and the two Nats; else computes.
- Method level: ReplayAt carries `methods : List (Σ' name, Thunk (Except Diagnostic (MethodFront parsed em name)))` for the entry
  module's decl names + exactness; MethodFront = lowering, lowered eq, accepted, generated (render #4 once) + eq.
  methodOf uses r.front method (theorem front_eq = methodFront …). Per-request: check applied, labelsWithin.
- Population: the session must know pins before a decision (a pure decision cannot report misses). Plan: session scans package
  cells (bodyOf .package) at open/refresh, pin = identity(artifact), adds entries for the config's (maxBytes, fuel).
- 15:10 IMPLEMENTED (unbuilt; local copies scratchpad pm/): ObjectiveActivity: Config moved below Refusal; MethodFront/methodFront,
  Fronts (+front_eq), ReplayAt (+fronts field), replayPackageAt, Held/Held.of/answer, LoadMemo (+replay_eq, hold, holds),
  Config.held; Replay = abbrev ReplayAt config.typeFuel; replayPackage via config.held (replayPackage_eq);
  Replay.generatedCore = artifact.typedCore (+_eq; no render). ObjectiveCall: methodOf uses definition.fronts.front;
  Method gains generated/generatedExact; Method.generatedCore = generated (+_eq). Ambient.held; configOf copies it.
  NativeHost: activityAmbient/activityPlanLoaded/activitySubmitLoaded take `held` (explicit); view passes {}; seatAmbient
  struct-instance. NEW Kernel/NativeHostHeld.lean: process IO.Ref {memo, domain, seen cells}; heldFor scans unseen cells for
  package bodies, holds pin -> Held.of (lazy). Host/Main 210/212 + NativeSpecializedConsent 210 pass heldFor.
  Build b1 (Kernel.ObjectiveCall) on hbox: w/b1.{pid,log,status}.
- 16:00 REBASED onto next 0125b224 (ROOT): lane commit 815e97c3 "WIP perf-memo" (repo-local identity set in lane src).
  Fix: SourceModule lives in ObjectiveBendFrontEnd. `lake env lean Kernel/ObjectiveActivity.lean` clean.
  Builds: w/run.sh NAME TARGETS (slot; NAME.{log,status,pid}). b2 = Kernel.ObjectiveCall Kernel.NativeHostHeld.
  The hbox lane tree is the source of truth now; the scratchpad pm/ copies are stale.
- 10-15 00:30 MOVED TO burst4-a (ROOT): hbox slot starvation (b4 waited ~3 h). hbox lane commits 815e97c3+493bc9c7 pushed to the
  hbox mirror lane/perf-memo and burst4 /srv/git/minidregg.git (from hbox with ~/.ssh/burst4_pull). burst4 lane
  /srv/lanes/perf-memo/src = mk-lane from next a5483db3 + cherry-picks 690a26c7, eaa852d3 (branch perf-memo). w/run.sh NAME TARGETS.
  Added since: Ambient ⟨4⟩ literals in NativeHostReplay/ObjectiveRefinesWorld get `{}` (replay path keeps no memo);
  Inhabited Held; theorem LoadMemo.hold_answers_only_its_bytes; heldFor control MINIDREGG_HOST_HELD=0 (measurement only:
  memo off vs on in the SAME binaries). Measurement plan (ROOT/Ember: one range, measure once at end): hbox perf-memo/w/measure.sh
  + cand.sh (Lean steps via with-lean-slot). b5 = Host.Main + NativeSpecializedConsent + ObjectiveRefinesWorld on burst4.
- 01:00 b5 GREEN on burst4 (Host.Main + NativeSpecializedConsent + ObjectiveRefinesWorld, 3739 jobs).
  PLANT (mutation): Held.answer without the `held.stored = stored` conjunct (w/mut/ObjectiveActivityMut.lean): the build refuses.
  Held.answer's match fails (`exact : replay.get = replayPackageAt … stored✝ pin` is not about the queried bytes), and
  hold_answers_only_its_bytes fails (⊢ False). replay_eq / replayPackage_eq / Birth.conserves … then depend on sorryAx.
  Log w/mut/mut.log. So no memo through this API can serve an entry computed from other bytes.
- 06:00 burst4: squashed to ONE code commit fa004154 (final message; numbers go in the report/log per ROOT's "measure once").
  Umbrella Minidregg+ObjectiveProofs+TokenCensus: green except TokenCensus red ONLY on Compiler.DurableServed.CachedRoots.mk
  (red on next a5483db3 already; not mine). My census rows added (ReplayAt.mk, Fronts.mk, Held.mk, MethodFront.mk + mints: notes).
  check-exports OK (no new implemented_by). Ratchet: 55 added / 2012 redefined / 8 removed / 19 restated; decisions with reasons
  appended to scripts/gates/objective-contract-decisions.txt (uncommitted); NEXT: `proofs --pin` + gates commit after the
  candidate's host step frees the tree. Candidate: w/cand.sh cand-1 (PID w/cand-1.pid, status w/cand-cand-1.status).
  Measure: memo off (MINIDREGG_HOST_HELD=0) vs on, same binaries (w/measure.sh to port from hbox), then rows.

## CONTINUATION (PAUSED 10-15 ~06:30 by ROOT: usage wall; burst4 being deleted)
- Branch lane/perf-memo = 77355fdf on GitHub (verified with ls-remote) and on burst4's remote (going away). The hbox mirror still
  holds the OLD pre-rebase WIP 493bc9c7: overwrite it from GitHub.
  - fa004154: the code commit (final message), on next a5483db3.
  - 77355fdf: WIP gates. Decision reasons are appended to scripts/gates/objective-contract-decisions.txt; `proofs --pin` NOT run.
- Verified on burst4 at fa004154:
  - lake build Host.Main + Kernel.NativeSpecializedConsent + Kernel.ObjectiveRefinesWorld GREEN.
  - Minidregg + ObjectiveProofs GREEN.
  - TokenCensus red ONLY on Compiler.DurableServed.CachedRoots.mk, which is red at base and not mine.
  - check-exports OK.
  - Mutation plant done (see 01:00).
  - Candidate cand-1: host step done (host-rc=0). It was stopped during consent/rust, so there is NO packed candidate. NOTHING MEASURED.
- Successor, first steps (on hbox, which keeps lane builds):
  1. Clone lane/perf-memo from GitHub into a lane tree (warm .lake from a next a5483db3 build if one exists).
  2. Build Host.Main via with-lean-slot.
  3. Run `scripts/check-objective-proofs.sh proofs`. It must show only the rows admitted in 77355fdf. If HEAD moved, re-draft
     with `--draft a5483db3..HEAD`, swapping the commit column.
  4. `proofs --pin`, then amend the gates commit (drop "WIP").
  5. Candidate: hbox perf-memo/w/cand.sh, with the Lean steps through with-lean-slot.
  6. Measure: perf-memo/w/measure.sh CAND. It runs the workload N=32 M=32 K=16 with the memo OFF (MINIDREGG_HOST_HELD=0),
     then ON, in the same binaries, with MINIDREGG_HOST_TRACE=1. Per-op table: perf-fix/p2/optab.py on serve.log (ops 210/212),
     plus the updates/judgment phases. Raw instructions are in <root>.perf.csv (--no-scale).
  7. Rows journey/call/send/objectrecord via perf-fix/run-rows.sh.
  8. Then decide whether to keep the MINIDREGG_HOST_HELD knob. It is a measurement control; delete it if ROOT says so.
- Known not done:
  - The consent re-admission path (NativeHostReplay admitDecodedNative, ambient literal `{}`) gets no memo.
  - drawQuote/frontEndQuote still decode the stored pair per load.
