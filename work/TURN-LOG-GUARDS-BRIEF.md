# TURN-LOG GUARDS-FROM-INTENT implementer brief (from TURN-LOG-4, 10-15)

You are an Opus implementer lane working in TURN-LOG's tree. Log as you go under "## GUARDS implementer" at the END of
/Users/ember/dev/redregg/work/TURN-LOG-LOG.md (append only; events, raw numbers). Report to TURN-LOG-4 by your final message.

## SAFETY (obey verbatim)
Read /Users/ember/dev/redregg/work/SAFETY-BLOCK.txt and obey it verbatim. Quoted from ember's CLAUDE.md, verbatim:
"## Stopping processes: PID file or nothing (incident 2026-10-10)
A subagent ran `pkill -f "cat" -u ember` to clear its own stuck `cat`. `-f` matches the whole
command line, every app lives under `/Appli**cat**ions`, and 44 of my apps and agents got SIGTERM.
- **Never kill by pattern.** No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`.
- **A process you started is stopped by the PID in its PID file**, and only that. Every detached job
  writes one (`nohup ... & echo $! > job.pid`). No PID file, no kill: tell me instead.
- If you must look first, `pgrep -fl` and read the list; it is never the argument to a kill.
- Every subagent brief you write quotes this block verbatim."
Never `git stash`. Never an unfiltered test suite. Write nothing large on the Mac.

## WHERE (all on burst4: `ssh -F ~/.ssh/burst4-20261015.conf burst4-a`)
- Tree: /srv/lanes/turn-log/src, branch `turn-log` = 7716f3fa (lane/turn-log 7877e6e7 + merge of lane/hp-6-sim 75887614).
  Untracked Kernel/CellTableCodec.lean, Kernel/WorldCheckpoint.lean are step-1 drafts: leave them alone, do not commit them.
- Builds: `/srv/pipeline/slots/with-lean-slot swarm-build lake build <targets>` (after `. /srv/pipeline/box.env; export LEAN_NUM_THREADS=4`),
  launched DETACHED with a PID file, e.g. write runs/gN.sh then on the box:
  `cd /srv/lanes/turn-log/runs && setsid nohup ./gN.sh > gN.log 2>&1 < /dev/null &` then `echo $! > gN.pid` as a SEPARATE statement
  (do not chain `&&` before the `&`: it backgrounds the whole chain). Wait in the FOREGROUND with a bounded loop on that pid
  (`for i in $(seq 1 120); do kill -0 $(cat gN.pid) 2>/dev/null || break; sleep 60; done`) — never "wait for a notification".
  Fast single-file checks: /srv/pipeline/scripts/lean-ask check <File.lean> (`--reload` after a full build) or /srv/pipeline/scripts/lane-check.
- Build b1 (runs/b1.pid, log runs/b1.log; targets Kernel Host objective-turn-totality turn-log-follower world-sim) was started by
  TURN-LOG-4 at ~05:00; wait for it (its log ends "rc=N") before your first full build. If it is red, that red is on 7716f3fa: fix it first.

## THE RULING (ROOT, 10-15) you implement
Guards come from the INTENT. `Turn.ofIntent` (Kernel/TurnOfIntent.lean:724 turnOf, :740 ofCells) today derives guard legs from the
HELD state (`guardLeg` = whole-value reads of the held cell, :687) and never reads `DataWrite.expectedPre` / `ReadGuard.expectedRoot`
(Kernel/DurableDataIntent.lean:71-82), so a stale intent re-derives into a Turn World.admit ADMITS; only the receiver preflight refuses
(HP-6 world-sim counts these as `receiver-only`, Host/WorldSim.lean:180-189). Required: the Turn's guards are built from what the intent
asserts; World.admit's guard check is THE staleness refusal (`guardFailed` by name); the receiver preflight becomes a corollary.

## THE DESIGN (TURN-LOG-4's decision; implement it, raise a flag in the log only if a step is false as stated)
1. Kernel/World.lean:
   - `History` (:410) gains `cellDigest : Option (Cell R) → D` (no default; the digest of a slot's canonical bytes, absent included).
   - `Turn` (:371) gains `pins : List (CellId × D) := []` — each a cell and the digest the turn asserts its pre-slot has.
   - `pinCheck w t : Option Reject := ` first pin (in list order, index i) with `(w.retired c).isSome ∨ H.cellDigest (w.cells c) ≠ d`
     ↦ `some (.guardFailed c i)` (document: for a pin, the index is its position in `t.pins`). It is the FIRST check in `turnCheck`
     (:512), so staleness is refused as guardFailed before nullifier/charge/absence/cell checks (after the replay check, which stays first).
   - `Turn.footprint` includes the pins' cells. Repair every theorem in World.lean the new check touches; restate (never weaken)
     and record old/new for the commit. Every `History` literal gets `cellDigest` (World.lean:2240 toyH, Kernel/WorldBench.lean:58,
     Kernel/TurnCensus.lean:145, Kernel/HostRefinesWorldCore.lean:792, Kernel/WorldRoot.lean:701 `cshakeHistory` gains a parameter,
     and the deployed instance that applies cshakeHistory: deployed `cellDigest o = ResourceBirthCodec.rootBytes (encodeCell o)`,
     the same digest `DeployedTurnCompact.cellDigest` (Kernel/DeployedTurnCompact.lean:111) uses; make that one function, not two).
2. Kernel/TurnOfIntent.lean:
   - `Bridge` (:540) gains `pin : Theory.TypedAuthorization.Digest → D` (deployed: `id`; prove/state injectivity where needed).
   - `turnOf`: `pins := intent.writes.map (fun w => (w.cellId.value, B.pin w.expectedPre)) ++ intent.readGuards.map (fun g => (g.cellId.value, B.pin g.expectedRoot))`
     (intent order, duplicates KEPT: a later step reconstructs readGuards exactly from the pins).
   - `legs` := write legs only (`deltas … filterMap leg?`); guard legs (`guardLeg`) are DELETED (they were state-derived and always
     passed; their storage bytes were 0 since reads write nothing, so the charge does not move — check DeployedCharge.lean and
     Kernel/ObjectiveTurnTotalityStorage.lean, which use guardLeg/legsOf, and delete their guard-leg terms).
   - `absent` := the guard cells whose asserted digest is the absent slot's: `guardIds` filtered by `B.pin g.expectedRoot = H.cellDigest none`
     (from the INTENT, not from `cells c = none`); the exact absence check stays, after the pins.
   - Keep the derivation's `retiredCell` refusal for guards (a refusal is fine; only ADMITTING from held state is the sin).
3. Kernel/DeployedHistory.lean `encodeTurn`/`decodeTurn` (+ `decodeTurn_encodeTurn`) and Kernel/DeployedTurnCompact.lean
   `encodeTurnAt`/`decodeTurnAt` (+ `decodeTurnAt_encodeTurnAt`) carry `pins` (list of (nat, digest)); the turn digest binds them.
   (No Store holds Turn bytes yet; step 2's LOG v3 does. Do not touch PersistedCodecTags.)
4. THEOREMS (named, `#assert_axioms`-style axiom record as the files already do; no `#guard`, no sorry, no vacuous premise):
   - `ofIntent_stale_refused`: `Turn.ofIntent B H w intent = .ok t → w.head ≠ none (or = some _) → w.journal t.txId = none →
     (∃ wr ∈ intent.writes, H.cellDigest (w.cells wr.cellId.value) ≠ B.pin wr.expectedPre) ∨ (∃ g ∈ intent.readGuards, …expectedRoot) →
     ∃ c i, World.admit H w t = .error (.guardFailed c i)`. (Any shape premise you need must be one Derived already gives.)
   - The honest direction: `admit_of_accepted` (Kernel/SnapRepresents.lean:372) keeps its conclusion; it will need a coherence
     fact `∀ bytes o, B.codec.decode bytes = some o → H.cellDigest o = B.pin (rootBytes bytes)` — state it as a named predicate,
     PROVE it for the deployed bridge/history (canonical decode: look for decode_canonical / encode_decodePrefix for the cell
     codec; if missing, prove it), so no deployed use carries it as an unproved hypothesis. Retired cells: pinned cells are never
     retired on an accepted intent (writes: writeRefusal; guards: the retiredCell refusal) — show it.
   - Corollary `preflight_of_admit` (name free): the derived turn admitted ⇒ every read guard and write pre matches the snapshot
     root (`readGuardsMatchCheck before intent = true` and the writes' expectedPre = roots), under SnapRepresents + coherence +
     `B.pin` injective. This is "the receiver preflight is a corollary".
5. Downstream: everything the umbrella builds (Kernel Host objective-turn-totality turn-log-follower world-sim) green. Kernel/TurnGen.lean
   and Host/WorldSim.lean (HP-6 sim) construct Turns/Histories: adapt them (presented-turn probes may need pins). The sim's classifier
   (Host/WorldSim.lean:180-189) must NOT be loosened: `receiver-only` stays defined as receiver refuses + world admits.

## ACCEPTANCE (measure, raw numbers in the log)
- Build rc=0 on the five targets (job count).
- `scripts/gates/check-world-sim .lake/build/bin/world-sim` PASS, and the summary line's `receiver-only=0` for every seed
  (before your change: 11-26 per seed). Also seeds 1-20 x 300: `.lake/build/bin/world-sim seeds 1 20 300 50`, receiver-only total.
  If a plant stops firing at its recorded seed/step because the turn shapes changed, re-record it in check-world-sim only after
  confirming it still fires (state old/new seed/step); a plant that no longer fires anywhere is red.
- `lake build` of the files carrying #assert_axioms for the new theorems shows only the standard axioms.

## COMMIT (one commit on `turn-log`, do NOT push; TURN-LOG-4 verifies and pushes)
Message via file (`git commit -F`), subject like `turn-log(guards)!: a Turn's guards are the intent's — pins carry the asserted
digests; World.admit's pin check is the one staleness refusal (guardFailed)`. Body: the shape change (Turn.pins, History.cellDigest,
Bridge.pin, guard legs deleted, encodeTurn/encodeTurnAt layout), every restated theorem old → new, the collision bound said out loud
(a pin is a 256-bit cSHAKE digest: guard exactness is now collision-level, 2^128, where the deleted whole-value guard legs were exact
but state-derived and so checked nothing about the intent), the sim numbers before/after, what re-emits (nothing persisted holds Turn
bytes yet). End with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `git add` NAMED files only.
