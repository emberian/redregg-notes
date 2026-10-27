# HP-1 BOUNDS log (continuation file) — started 2026-10-14
Lane: HP-1 (Claude). Design docs/HP-DESIGN.md @ lane/hp-design 4329b99c (§1.6, §5.2 HP-1, §6 limits).
Base next 0125b224. Lane tree hbox:/tank/dregg-build/claude-lanes/hp-1-bounds/src (git clone of mirror, branch hp-1-bounds;
.lake/build = cp -a of hyp-instances (built at 0125b224), .lake/packages cp -al from warm-7dea0626 (privatise traces before build)).
## events
- 18:50 start; read design whole; lane tree cloning.
- 19:20 measured journey record sizes (TURN-LOG j1 Stores, durable_log.record max): send 128,346 B, domain 54,174, call 54,173,
  seats 53,338, activity 33,066, upgrade 25,471, objectrecord 23,978. Design §6 values kept except frameBytesMax = 12,102,760
  (FnEvidenceCodec.maxHostFrameBytes, the fn consumer route's derived need; design's 8 MiB is below it).
- Decisions: refusal detail text `over-bound NAME VALUE > LIMIT` under the existing RefusalReason.malformed (frame) and
  prepareAppend's error channel (Result.unavailable) — no new RefusalReason wire tag (would touch 25 files + the outcome codec).
  Rust constants emitted by `#eval emitRust` in Kernel/Bounds.lean (the MinidreggV1NativeGlue precedent), drift gate =
  scripts/check-prover-glue.sh (module + file added). Decoder choke point needs lane/turn-log (not in next): commit B merges
  lane/turn-log b1152e5d and adds decodeEntry + follower wiring; commit A (bounds, prepareAppend, serveSession, Rust) is on next alone.
- Commit A edits in tree (unbuilt except Kernel/Bounds.lean via lake env lean, OK; cargo check resource-client rc=0).
- 21:50 commit A 22857866 pushed to mirror lane/hp-1-bounds. Build (slot) Kernel.Bounds Compiler.DurableReceiverIO Host.DryRun Host minidregg-host rc=0.
  Plants: codec+stdio frame 12102761 -> `over-bound frameBytesMax 12102761 > 12102760`; at-bound controls reach the decoders.
  intentBounds compiled: nullifiers 65 / cell 1048577 / legs 257 refused by name; 64 / 1048576 accepted. bounds.rs drift: match + mutated control red.
  Plant dirs: hp-1-bounds/plant (store copied from turn-log j1/send, chmod 700, head-anchor copied).
- next: commit B = merge lane/turn-log b1152e5d + decodeEntry (p_tl.py in scratch) + follower --plant-pad.
- 10-15 04:00 rebased onto next a5483db3 (carries turn-log b1152e5d): A = e8bdf528. B = 55a5269d (decodeEntry, followFrom/writeLog, follower --plant-pad),
  built on burst4-a /srv/lanes/hp-1-bounds (Kernel, Host, minidregg-host, turn-log-follower rc=0). Plant: follow 0-activity/2-call ROOT = exporter root;
  --plant-pad 3 -> `STOP over-bound 3 turnBytesMax 1048577 1048576`. Pushed shared (burst4), hbox mirror, GitHub (from hbox; burst4 lacks a GitHub key).
  Candidate + rows running on burst4: cand.sh (pid cand.pid, status cand.status, rows in /srv/lanes/hp-1-bounds/rows).
- 05:45 candidate on burst4 at 4a83fdb7 (= 55a5269d + cherry-pick of lane/seat-count 195506cb, the native-host seat count; consent had exited 75 on 2 seats):
  host/consent/rust/pack rc=0; rows journey PASS 201 s (J0-J8, JROT, JROTL, JRLANE, JGATE, JAUDIT), call PASS 63/63, send PASS 192/192, objectrecord PASS 39/39.
  Pushed lane/hp-1-bounds = 4a83fdb7 to burst4 shared, GitHub (via shared's github remote), hbox mirror. DONE; report sent to ROOT.

## CONTINUATION (HP-1 at ~340K tokens; successor starts here) — 10-15 06:00
State: lane/hp-1-bounds = 4a83fdb7 (e8bdf528 A, 55a5269d B, 4a83fdb7 seat-count cherry-pick) on next a5483db3; pushed burst4 shared,
GitHub, hbox mirror. Lane tree burst4-a:/srv/lanes/hp-1-bounds/src (built warm: Kernel, Host, minidregg-host, turn-log-follower; candidate
at /srv/lanes/hp-1-bounds/candidate; scripts build.sh, cand.sh (host/consent w/ seat retry, rust, pack, rows), run-rows.sh; plant/ has
turn-log 4a exports 0-activity, 2-call). Push GitHub from burst4: `git -C /srv/git/minidregg.git push github lane/hp-1-bounds` after
`git push shared HEAD:refs/heads/lane/hp-1-bounds`. hbox lane tree /tank/dregg-build/claude-lanes/hp-1-bounds/src (frame plant: plant_frame.py,
plant/ store copy + mini.config; PlantAppend.lean).

ROOT rulings to implement (next commits on lane/hp-1-bounds), then rebuild + candidate + rows journey/call/send/objectrecord once at the end:
1. `overBound` RefusalReason WIRE TAG (not detail text). Findings:
   - Compiler/RefusalReason.lean: enum (15 ctors, no payload), `name`, `describe`, `all`/`mem_all`, `name_injective`, `stream` tags 0..14,
     `stream_unknown_tag` (15 → bump to 16; statement changes: say so). Add `overBound` tag 15, name "over-bound". The detail keeps
     `Bounds.Refusal.render` (NAME VALUE > LIMIT). Only Kernel/NativeHost.lean, Kernel/ObjectAudienceInstall.lean reference the newest ctor
     (audienceTransition) — matches are mostly catch-all. Rust: native/grain-runtime/src/provider.rs:902 maps reason names; check spk-host
     reason tables. Outcome codec tag "DREGG/NATIVE-HOST/OUTCOME/v5" appears in Lean + native/spk-host/*.rs + journey-stranger.py: decide
     whether to bump to v6 (greenfield: bump so old peers refuse; then every v5 literal moves).
   - Frame path: Host/RequestRefusal.lean `answer` maps IO.Error marker `tag` → malformed. Add a second marker (e.g. "minidregg-host bound")
     + `RequestRefusal.overBound (r : Kernel.Bounds.Refusal) : IO.Error`, `answer` → `.refused .overBound (phase op) (clip r.render)`,
     theorem answer_overBound; answer_refused proof gets one more split. Host/Main serveSession/serveCodec: replace
     `RequestRefusal.malformed refusal.render` with `RequestRefusal.overBound refusal` (3 sites).
   - Append path: today prepareAppend returns `.error render` → receiveCandidateWithFresh maps to Result.unavailable (WRONG kind).
     Cleanest found: Kernel/DurableDataIntent.RejectReason gains `overBound (name : Bounds.Name) (value limit : Nat)` (precedent:
     `tailBound head certified bound`); Kernel/NativeHost.lean `durableRefusal` (line ~116) maps it to `refused .overBound "bound" render`
     (+ theorem like durableRefusal_tailBound). WHERE to check: prepareAppend's Except String can't carry it, and Host/DryRun.lean
     theorems (dryReceive_admission_reaches_append, dryReceive_tail_refusal_agrees) state the receive path's shape with `admitted : prepare … = .inl ready`.
     Options: (a) check inside the durable `prepare` (Kernel side, returns `.inr (.rejected r)`), so `admitted` implies within-bounds and DryRun
     statements stay; check whether any completeness theorem states `prepare … = .inl` from hypotheses (grep `= .inl` in Kernel/DurableCheckpoint*);
     (b) change prepareAppend's error to a sum and update DryRun statements (say so). I lean (a). Remove the prepareAppend string check then.
2. cellBytesMax := 8 MiB, single home: make Kernel/GrainResourceBirthPolicyController.lean `maxSourceBytes := Kernel.Bounds.cellBytesMax`
   (move, not a tie), packageBytesMax := cellBytesMax; FnEvidenceCodec.maxPackageBytes (1 MiB, fn-specific) stays — replace
   Host.Main.fnPackage_eq_bound with `≤`. CHECK turnBytesMax (1 MiB) < 8 MiB cell: a turn creating an 8 MiB cell would be refused at
   decodeEntry. Raise turnBytesMax (≥ cellBytesMax + overhead; e.g. = frameBytesMax 12,102,760, keeping turnBytes_le_frameBytes) and add
   theorem cellBytes_le_turnBytes. Regenerate bounds.rs (build emits it; prover-glue gate compares). Update the Bounds.lean docblock.
3. TURN-LOG 4a keeps the append check (ROOT told TURN-LOG-4). 4. File count waived.
Then ROOT offers HP-5 ASSERT to whoever holds this lane (design §1.7, §6 invariants table; baseline 0 runtime assertions, 56 partial defs).

## HP-1b (successor; started 10-15 06:10 from the CONTINUATION above)
- 06:10 read log, protocol, tree. Plan A: RefusalReason.overBound tag 15 (stream_unknown_tag 15→16); RequestRefusal second marker
  "minidregg-host bound" + overBound/answer_overBound, 3 Host/Main sites; append path: DataIntent.bounds/checkBounds move to
  Kernel/DurableDataIntent (RejectReason.overBound name value limit), checked FIRST in DurableCheckpoint.prepare (so it also guards
  replay/reopen: a record past a bound refuses to load), prepareAppend check + prepareAppend_overBound removed; NativeHost.durableRefusal
  → refused .overBound "bound" render (+durableRefusal_overBound), birthReason maps it; blind submissions stay undisclosed
  (bounds of a DERIVED intent may depend on state). OUTCOME/v5 → v6 (PersistedCodecTags census ⇒ StoreEpoch moves ⇒ old Stores refuse).
  Plan B: cellBytesMax 8 MiB; GrainResourceBirthPolicyController.maxSourceBytes DELETED (sites read Kernel.Bounds.cellBytesMax);
  packageBytesMax := cellBytesMax; fnPackage_le_bound; turnBytesMax := frameBytesMax; cellBytes_le_turnBytes.
  Objective-manifest decisions (RefusalReason ctor, prepare redefined) are NOT drafted here (needs lake build ObjectiveProofs): flagged to ROOT.
- 06:30 build of both rulings on burst4-a: lake build (build.sh targets) rc=0, 7587 jobs. Committed separately; the A commit was NOT built on its own.
  1a871252 = ruling 1 (overBound wire tag 15, stream_unknown_tag 16, RequestRefusal.overBound/answer_overBound, 3 Main sites,
  RejectReason.overBound checked first in DurableCheckpoint.prepare, durableRefusal_overBound, OUTCOME v5→v6 + v5_outcome_refused, Rust tables).
  e59ea490 = ruling 2 (cellBytesMax 8 MiB; maxSourceBytes deleted; packageBytesMax := cellBytesMax; fnPackage_le_bound; turnBytesMax := frameBytesMax;
  cellBytes_le_turnBytes; bounds.rs re-emitted). Pushed to burst4 shared + GitHub (ls-remote github lane/hp-1-bounds = e59ea490).
- Append plant observed (compiled: real DurableCheckpoint.prepare on a genesis image → NativeHost.durableRefusal → outcomeCodec encode/decode;
  program saved at redregg/work/HP-1b-PlantAppend2.lean):
    plant nullifiers 65: wire DREGG/NATIVE-HOST/OUTCOME/v6 reason-byte-prefix [1, 1, 0, 15] -> refused over-bound phase bound detail over-bound nullifiersPerTurnMax 65 > 64
    control nullifiers 64: past the bound check; rejected later by RejectReason.unguardedEventOnly
    plant post 8388609 B: ... -> refused over-bound phase bound detail over-bound cellBytesMax 8388609 > 8388608
    control post 8388608 B: prepared; old-bound post 1048577 B: prepared (accepted since ruling 2)
    plant writes 257: ... -> refused over-bound ... legsPerTurnMax 257 > 256; control writes 256: prepared
- 06:50 PAUSED by ROOT (usage wall; burst4 deleted). Candidate at e59ea490 was mid host-Lean compile (388/776); stopped by its PID (cand.sh pgid). No rows ran.

## CONTINUATION (HP-1b, paused 10-15 06:50) — successor starts here
State: lane/hp-1-bounds = e59ea490 on GitHub (1a871252 ruling 1, e59ea490 ruling 2, on 4a83fdb7 / next a5483db3). Both rulings are DONE in source and
the Lean umbrella is built green. Still UNVERIFIED: the Rust build (spk-host OUTCOME/v6 literals, provider.rs, replan.rs), the candidate, the rows, and the
frame and follower plants on the new build. burst4 is gone, so redo on hbox:
1. Clone lane/hp-1-bounds from GitHub into /tank/dregg-build/claude-lanes/hp-1-bounds (the old tree there is at 22857866/55a5269d: fetch and reset
   to e59ea490), cp -al a warm .lake + unlink scripts, then build:
   with-lean-slot swarm-build lake build Kernel.Bounds Kernel.DeployedTurnCompact Kernel.TurnLog Compiler.DurableReceiverIO Host.DryRun Host.TurnLogFollower Kernel Host minidregg-host turn-log-follower
2. Build the candidate (the recipe in PERF-FIX-LOG.md; burst4's cand.sh did host, consent w/ seat retry, rust, pack, then run-rows.sh journey call send objectrecord).
   Before building, move old artifacts/, consent-out/ and native-out/ out of the way (build-native-host refuses to overwrite them).
3. Plants on the new host: (a) frame: plant_frame.py (hbox lane dir) in `codec` mode with FRAME=12102760; expect `over-bound frameBytesMax 12102761 > 12102760`
   with reason tag 15 in the v6 frame. Session mode needs a FRESH store: the StoreEpoch moved, so old store copies refuse. Make one with
   objective-call-native-journey.py --bin CAND/bin --root DIR. (b) follower: turn-log-follower follow <export> --plant-pad 3; expect
   `STOP over-bound 3 turnBytesMax 12102761 12102760`. The exports carry no StoreEpoch, but burst4's plant/ exports are lost: re-export from a fresh row store.
4. Report to ROOT: shas 1a871252/e59ea490, the rows, the plant lines. Flags for ROOT: objective-manifest events not drafted (INTEGRATOR pins at merge).
   A grain source at exactly cellBytesMax may produce a birth cell a little over 8 MiB, which would be refused over-bound at the append. Not checked.
HP-5 (not started; no code): notes so far. 55 partial defs in Kernel/Compiler/Host on this tree, 0 panic!/assert!. Lean's panic! prints and CONTINUES
by default. lean.h exports `lean_set_exit_on_panic(bool)`: an @[extern] binding called at Host/follower start makes a panic! assertion a real crash.
Candidate pairs: TurnLog.followFrom after each admit (head = (h+1, chain'), sysPost_head; journal, sysPost_journal; spent, sysPost_spent), proved
never-firing on honest logs inside followFrom_writeLog; prepareAppend codec pair (recordFrame decode of recordBytes = record) before the append;
readExactly/discardExactly/readBounded* made total with fuel = byte count. HP-5 branches from lane/hp-1-bounds tip as lane/hp-5-assert.
