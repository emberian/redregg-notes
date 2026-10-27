# CONSENT-MODEL log (continuation file) — started 2026-10-14 11:30
Lane: CONSENT-MODEL (Claude, architect-implementer). Item: the client consent provider (minidregg-client-consent).
Lane dir hbox:/tank/dregg-build/claude-lanes/consent-model. src = clone of bundles/burst3-minidregg.git, branch
consent-model = origin/main 30a5009a + merge lane/perf-fix 5b7cae0d + lane/perf-client c1cc0a89 + lane/fleet-race-land
19e9fe30 (conflict in client_consent.rs resolved: perf-client's exchange() returns (op, body); fleet-race's stale-observation
record moved into round_trip) = 50e3440c. `next` not yet published on the mirror (11:30); rebase onto it when it exists.
.lake = full `cp -a` of perf-fix/src/.lake (no hardlinks, so no unlink step needed; 5.1G).
Pushes -> lane/consent-model.

## method
- mkcand.sh (BASE=<packed candidate> mkcand.sh NEW COMMIT MINI) = perf-client's mkcand generalised over the base.
- cand-0 = perf-fix cand-M (Host+consent @fb23f296 tree) + perf-client mini-P3b (c1cc0a89). Profiling baseline.
- wl.sh CAND TAG N M K (WLSRC=worktree with scripts/perf) -> /tmp/cm-TAG, runs/TAG.out.

## events
- 11:46 w0 (cand-0, N=8 M=8 K=4, 38 records): checkpoint red by design (history < 64), else PASS.
- MEASURED prof-0 (prof.sh: perf record instructions:u -c 4M, dwarf; one read-at, birth, invoke on /tmp/cm-w0):
  consent provider = 85% (at), 95% (birth), 97% (invoke) of client-tree samples. Inside the provider (children, % of
  provider samples; dwarf truncates deep Lean stacks so the column under-counts): invoke: verifyInitial 52.6
  (ConsentAnchor.resume 42.8 of which walkSuffix [re-admission of records after the anchor] 34.1, validateLoaded at the
  anchor 3.0; loadChained full Store open 10.0), the ONE plan (activityPlanLoaded via expectedPlanBytes) 5.3, lean_initialize 1.3.
  read-at: verifyInitial 48 (resume 43, walkSuffix 37, validateLoaded 16.5), lean_initialize 12, checkObservation 4.1.
  => the plan/frame is ~5%; C's one-decision already holds on the consent side (activityPlanLoaded = planDecision).
  The per-process cold start (init, full Store open, cut + validate at the anchor) and the suffix re-admission dominate.
- Anchor binding check: every sponsor command (query, workspace create, activity submit) uses config bytes 3cc5e0e1…
  (per-attempt config.json copies are byte-identical), so the sponsor workspace already has ONE retained anchor.
  The suffix a step re-admits = the records written since the sponsor's previous consent process (1–2 in a
  steady single-client loop; more when other workspaces write in between).

## DESIGN (12:40)
What consent must keep: custody signs only bytes it derives itself from the retained request on a prefix it admitted
(native re-execution of every record, CLIENT-SIGNING-CONSENT.md). Termination on rollback, rewrite, invalid extension.
The re-admission of each NEW record once is the trust-model floor (no proof system: project-no-proof-system-in-mini-admission).
Everything else per CLI process is repetition:
  P1 Lean process init (~0.38 G), P2 full Store open (loadChained: decode + chain every record: O(history)),
  P3 cut at the anchor + validateLoaded (O(world): root, directory, authority, law check), P4 `withPinnedSignature`
  (copy+chmod+exec of the verifier), then the floor F (suffix admission) and the frame W (one decision).

Decision: ORDER (3) BEFORE (1). Measured, (1) as briefed (a MAC'd persisted frontier image) removes P2+P3 but not P1/P4,
and adds a new trust premise (a MAC'd validated image accepted without re-validation) plus a codec for the whole Opened.
(3) a resident provider per workspace binding removes P1–P4 per CLI step with NO new premise: it is exactly today's
in-process warm provider (`invoke` already keeps one provider per process and never restarts it to drop its frontier),
kept across CLI processes. The anchor (already persisted, owner-private, binding = provider file identity + settings
bytes) stays the cold-start path for the daemon; (1) remains only a daemon-cold-start optimisation, judged after (3)+(2)
are measured. (2) = memo of the front end per package digest inside the resident provider (JUDGE offender 2 (c)),
measured after (3): with a resident provider every record admission and plan of the same package hits it.

(3) shape (Rust, client side only; the Lean provider is unchanged):
- `mini` connects to `<anchor_dir>/<binding>.sock`; if absent it starts `mini consent-resident` (detached, its own
  session) which flocks `<binding>.lock` (one daemon per binding), writes `<binding>.pid`, starts the Lean provider
  exactly as `start_in` (anchor offer 228 first), binds the socket 0600 in the owner-private anchor dir, serves frames
  one at a time (a Mutex over the provider; frames are self-contained), retains the anchor (229) after every frame as
  `invoke` does, and exits when the provider dies or after MINI_CONSENT_IDLE_S (default 600) without a frame.
- Both ends check the peer (SO_PEERCRED uid == own euid); the socket and dir must be owner-private. The daemon is the
  client user's process; the serving Host never sees it.
- Failure semantics preserved: a provider refusal frame is relayed verbatim (stale-observation tag included); a dead
  provider ends the daemon, the CLI frame fails (no silent fallback); the next CLI start begins a new daemon from the
  retained anchor, which refuses a rolled-back/rewritten Store exactly as a per-process start does today.
- Same-length rewrite: today each new process re-checks the Store's chain at the anchor height (checkStore); a warm
  provider's `refresh` (extendFrom) returns the held image when the Store's head equals its height without comparing
  anything. Kept warm across processes, that would stop detecting a same-height rewrite between commands. MUST CLOSE
  before (3) lands: refresh compares the Store's head tag at the held height with the held `headTag` (Lean, small).
- MINI_CONSENT_RESIDENT=0 keeps the per-process provider (for tests and for an operator who wants it).
- 12:30 prof-32 (N=32 M=32 K=16 root /tmp/cm-w32, cand-0), % of provider samples (children): read-at: verifyInitial 49,
  loadChained 25, prefixAt 12.6, walkSuffix 10, validateLoaded 4.4, deployedHash (root) 48.6 inclusive; birth: loadChained 26,
  prefixAt 12.9, resume 15, consent frame 7.9; invoke: resume 39.6, walkSuffix 30, loadChained 17, prefixAt 8.4.
  => at realistic size the per-process cold start (P1–P3) is the larger term; suffix re-admission next; the frame small.
- INCIDENT (mine, 12:15): a background `until [ -s /dev/null ]` wait (wrong condition) left an orphan spin on hbox,
  PID 3319589 (100% one core, no PID file). Not killed (rule); reported to ROOT.
- 12:50 commits on branch consent-model: 561e603e (Lean: frame 233 / ConsentAnchor.recheckStore, checkStored,
  checkStore_eq_checkStored, checkStored_ok); cbea85b9 (Rust: resident provider, `mini consent-resident`, socket
  <anchor_dir>/r-<binding[..16] hex>.sock — the full 64-hex name overflowed sun_path in tests). Lean build of
  Kernel.ConsentAnchor + Host.ClientConsent{Core,Session} green (build-logs/cm-lean1.log). Rust filtered tests:
  resident_provider_rechecks_each_connection_and_serves_all_of_them PASS (opcodes 233,220,229,221,229,233,222,229;
  reserved 228/229/233 refused; idle exit removes socket+pid), retained_anchor x3, stale, round_trip PASS.
- 12:55 ROOT: Lean builds only via /tank/dregg-build/pipeline/slots/with-lean-slot. cand.sh uses it.
  Candidate cand-R building (cand.sh, pid logs/cand-R.pid, status logs/cand-R.status).
- 14:40 cand-R packed (lane-build host/consent/rust/pack, slot): Host sha 4f768171… (= cand-M: the Host closure is
  untouched), consent e1038b5f… (has ConsentAnchor_recheckStore), mini from cbea85b9.
- STEPBENCH sb-r1 (/tmp/cm-w32, N=32 root; base cand-0 vs new cand-R alternated, median of 3; instructions:u
  --no-scale over the client process tree PLUS the resident provider's daemon + Lean child via perf stat -p;
  the consent executable pinned per candidate with MINI_CONSENT_HOST/MINI_LOCAL_HOST/MINI_CONSENT_CONFIG):
  | step | base instr / CPU / wall | new instr / CPU / wall |
  | view    | 0.001 G / 3 ms / 24 ms     | 0.001 G / 2 ms / 25 ms |
  | read-at | 40.331 G / 3024 ms / 6617 ms | 26.441 G / 2236 ms / 6493 ms |
  | invoke  | 19.477 G / 1468 ms / 4052 ms | 1.633 G / 251 ms / 4399 ms |
  | birth   | 18.900 G / 1565 ms / 3139 ms | 4.696 G / 548 ms / 2215 ms |
  (first sb-r1 attempt invalid: both candidates ran cand-0's consent binary because the w32 workspace has no pins and
  falls back to host.with_file_name; fixed by pinning per candidate.)
  read-at's remainder is in the resident provider and GROWS per read (13.8, 26.1, 27.1 G): profile (profres-1) =
  checkObservation -> NativeObservationController.challengeAt -> past-state materialisation (StoreCodec.encode,
  Materializer.rootOf): the client twin of item K (`at` below the rebased base = genesis fold).
- PLANTS (cand-R, MINI_CONSENT_ANCHOR_DIR private per root):
  rollback (plant-rollback.sh /tmp/cm-pl): at-1 rc=0, invoke rc=0, at-2 rc=0 (control), Store restored to the snapshot,
  at-3 rc=1 "consent refused: the Store's head 26 is below the retained consent anchor at 27: the accepted history was
  rolled back"; the resident ended (pid file removed). Not discriminating for 233 (extendFrom also refuses a shrink).
  SAME-HEIGHT FORK (plant-fork.sh /tmp/cm-pf, the discriminating one): resident admits A at 28, Store restored to 27,
  B written at 28 by a per-process provider on its own anchor dir (admits the fork), resident alive, at-2 rc=1
  "consent refused: the Store's accepted history up to height 28 differs from the retained consent anchor: the prefix
  this client admitted was rewritten". (First run of the fork plant was vacuous: the resident had never admitted A,
  so B at that height was simply the next record — correct acceptance; the plant now reads after A first.)
  RED control queued: cand-red = cand-R with mini built with the per-connection recheck disabled (bins/mini-norecheck,
  never committed; NOTE rust-target/release/mini is that red build until the next bmini.sh).
- ROWS cand-R (rows-R): journey PASS (J0–J8, JROT, JROTL, JRLANE, JGATE, JAUDIT), call PASS 63, send PASS 192;
  seats, fleetsign running.

## DESIGN 2 (approved by ROOT 14:20): past states only from the provider's OWN admission
FINDING (derived from code at 50e3440c, pre-dates this lane): a consent provider's opening is NOT wholly its own.
verifyInitial opens the Store with loadChained, whose base is the Store's sealed checkpoint (openSealedWith under the
Store/operator key); ConsentAnchor.resume cuts it with Loaded.prefixAt, which KEEPS that base when it is at or below
the anchor (Compiler/DurableReceiverCore.lean:1505-1508) and takes the stored roots from the operator's tags. The
anchor comparison then binds only the cut's FINAL root (= the anchor root, the client's own). So the current state is
the client's own, but `at h` for h in [Store checkpoint base, anchor) resumes from an operator-sealed state bound only
through the later root: a forged base cell overwritten before the anchor height passes the anchor check and shows in a
past read the client signs an observation of. STATE-AT's keptAt would widen exactly that to every kept checkpoint.
Shape (statement level):
- `Loaded.Kept` gains a second provenance. Today: `authentic` = opened under the Store key, root = rootLog[h-1].
  New: `Own` — a base the provider computed: (prior : Loaded) with prior.image.accepted = loaded.image.accepted.take
  prior.height, state = State.ofSnapshot prior.image prior.snapshot, and prior's base itself Own or genesis
  (inductive provenance `Admitted`: genesis | step (records replayed by NativeHostReplay from an Admitted base)).
  resume_sound's premises (seedValid, Admissible base.state, prefix replay = atBase) hold for Own by induction on the
  provenance (the replay IS the genesis fold restricted to records the provider re-executed): theorem
  `Kept.own_sound : (k : Kept.Own) -> atPrefixFrom (some k) h = (prefixImage h).restore` for k.height ≤ h < baseHeight.
- The consent provider passes ONLY Own bases; its opening's base must be Own too: the cold start may not take the
  Store's checkpoint as its base. That is where (1) becomes the correct fix rather than an optimisation: the persisted
  frontier is the provider's OWN validated state at its anchor, MAC'd under the client's consent key, so a cold start
  has an Own base without a genesis fold, and no operator-sealed checkpoint is ever a client base.
- Resident: retains its image at each rebase point (bounded list, newest first); `at h` resumes from the nearest
  retained Own base at or below h; below the oldest, the genesis fold (as today).
- RED control (plant-fork.sh on /tmp/cm-pf2 with cand-red, 233 disabled): at-2 rc=1 "remote challenge differs from
  locally prepared intent" — the resident stayed on view A, the fork was neither named nor terminal. With 233: named
  "rewritten" and the provider ends. Signing safety held in both (the derived challenge differs); 233 restores the
  documented termination condition.
- Rows cand-R: journey, call 63, send 192, seats 91/91, fleetsign: all PASS.
- PUSHED mirror lane/consent-model = b7b007db (561e603e Lean frame 233; b7b007db = cbea85b9 tree, message with numbers).
  GitHub from hbox: no key (publickey denied) — ROOT pushes.

## CONTINUATION (for the successor; ROOT 14:55: implement DESIGN 2 + (1), acceptance = fork + rollback plants)
State: branch consent-model @ b7b007db on main 30a5009a + perf-fix + perf-client + fleet-race-land. state-at d951d57a
conflicts with perf-fix (DurableCheckpointCodec.lean, Kn2StoreBench.lean): INTEGRATOR merges; rebase onto `next`
once it holds perf-fix, perf-client, fleet-race-land and state-at (it held none at 14:00; origin/next = 68f78d23, 7 days old).
Tools in the lane dir: cand.sh NAME (host/consent in with-lean-slot, rust, pack), mkcand.sh (BASE=… swap mini),
bmini.sh/tmini.sh (rust-target/release/mini is currently the RED no-recheck build: rebuild before reuse),
stepbench.py ROOT BASE NEW REPS TAG (counts the resident via perf stat -p), prof.sh/profres.sh (dwarf profiles;
perf report takes ~10 min per file), plant-rollback.sh / plant-fork.sh CAND ROOT (in place; make roots with
`MINI_CONSENT_IDLE_S=60 WLSRC=/tank/dregg-build/claude-lanes/perf-client/wt-P3 ./wl.sh CAND TAG 4 4 2`), run-rows.sh.
Work, in order:
1. On `next` (with state-at's Loaded.Kept/atPrefixFrom), add the OWN provenance (DESIGN 2): an inductive `Admitted`
   base (genesis | replayed from an Admitted base by NativeHostReplay) and `Kept.own`; prove Kept.own_sound (the
   resume_sound premises by induction). The consent path (NativeClientConsent.checkObservation -> challenge ->
   atBytes/atCovered) passes only own kept bases.
2. Cold start without an operator base: the provider persists its OWN validated state at its anchor (item 1: frontier
   = Anchor + the Opened's State at that height, MAC'd under a client consent key held beside the anchor — the key is
   custody: generating/holding it is a pause item unless ROOT/Ember already scoped it), and resume builds its opening
   from that own base + the Store's records after it (chain-checked against the anchor), never from loadChained's
   Store checkpoint. Theorems: the persisted frontier's state = the re-executed prefix's (the Session.adopt /
   validateLoadedFrom_eq shape), and recheck/resume termination conditions unchanged (checkStore_eq_checkStored).
   Plant: tampered persisted frontier refuses by name; the fork + rollback plants above stay green.
3. Resident: retain own images at each rebase point (bounded), `at h` from the nearest own base; re-run stepbench
   read-at (target: no growth per read; today 13.8 -> 27 G).
4. Then the (2) front-end memo per package digest inside the resident (JUDGE offender 2 (c)): measure first with
   profres on an invoke; on cand-R the one plan is ~5% of a cold provider, so measure its share of the warm one.

## CONSENT-MODEL-2 (successor, 15:05 10-14) — PART A: own bases only (cv task 01a13bcd-7aa2)
`next` still absent on the mirror (15:07: only old/next-20261003); continuing on b7b007db.
FINDINGS (derived from code, b7b007db):
- The brief's "forged cell overwritten before the anchor" cannot be built: every DataWrite names its expectedPre and
  preflight refuses a stale pre-root (DurableCommitProtocol.preflight .stalePreRoot), so a record that overwrites a
  forged cell does not replay; loadChained refuses the open. The REAL hole is wider: the world root
  (entriesOf = system leaf + roots of image.cellIds) does not cover (a) a cell id the image never seeds or writes,
  (b) State.available. A Store-key-sealed checkpoint carrying either passes openSealedWith, the suffix replay, the
  head-root check AND the anchor's root comparison, and the forged component sits in the provider's CURRENT state
  (and every past state resumed from it), not only in past reads.
- Second operator-base surface inside the provider: NativeHistorySelection.select/selectAfter (lifecycle claim,
  completion, retry, failed-start histories) read `reader.stateAt index`, which resumes from the Store's latest
  checkpoint (DurableHistoryStore.baseOf). Those are "at h" the provider's ADMISSION depends on.
- The consent frames themselves (220/221/222) never evaluate a past state: challengeAt binds the current world root,
  height and the target's current cell root. So "at h the client signs" = past states its admission walk reads.
DONE (uncommitted until green):
- DurableReceiverCore: Loaded.prefixOwn (cut at h folded from the seed, rootLog = replicate none: no operator root
  kept; subtype carries baseHeight = 0, base = ofSeed seed, rootLog spec, all rfl); theorem Loaded.atPrefix_own
  (genesis-based image: atPrefix h = (prefixImage h).restore at EVERY h; resume_sound's premises by construction).
- DurableHistoryReader: OwnBase (seed, logStart, height, chain, state, fold: ∃ records of that length chaining to
  chain whose Image.restore is a snapshot with state = State.ofSnapshot) ; StateAt.baseAuthentic gains a third
  disjunct (an OwnBase on the verified log). DurableHistoryStoreCore: stateAt = stateAtFrom baseOf (unchanged);
  ownBaseOf (highest own base ≤ h for this seed + log start, its height's verified record must carry its chain,
  else refuse notIncluded; else the seed; NEVER a Store checkpoint); stateAtOwn; Reader.ownOnly.
- NativeHostReplay: advance_base, advanceSuffix_base, AdmittedSuffix.base (the suffix walk keeps its anchor's base).
- ConsentAnchor: resume cuts with prefixOwn; Anchored.startGenesis; ownOfGenesis; Anchored.opened_genesis (held
  image genesis-based by AdmittedSuffix.base); Anchored.own = [head own, anchor own]; Basis.own (.full -> []);
  the suffix walk's reader = reader.ownOnly [own at the anchor].
- ClientConsentCore: storeReader takes own bases and returns reader.ownOnly; serve threads `own` (retainOwn: the
  admission's own bases ahead of older ones, deduplicated by height, bounded 16 = retainedOwnBound); refresh and
  upgrade read through it. verifyInitial's full fallback reads with [] (genesis folds).
- PLANT scripts/consent/own-base-plant.lean (STORE-HELPER = cand-R/bin/minidregg-link-sqlite-store): toy Store,
  41 records, checkpointEvery 16; the operator re-seals checkpoint 32 under the Store key with cell 9 = [99] (never
  seeded/written). Same pass: operator cut (prefixAt 36) + Store Reader.stateAt 34 must SHOW [99] (plant live) with
  equal world roots at 36 (the anchor comparison is blind to it); own cut (prefixOwn 36), Reader.ownOnly [] at 34,
  ownOnly [own@36] at 38 (base 36) and at 34 (base 0) must read [].
- 15:30 Lean typecheck build in slot (logs/own-lean1.log).

## PART B DESIGN (PAUSED on Ember: key custody — NOT implemented)
Goal: a cold provider start with no genesis fold and no operator base. Persist the provider's OWN validated frontier
at its anchor, under the client's custody, MAC'd.
What is persisted (MINI-CONSENT-FRONTIER/v1, beside the anchor, same owner-private dir, same binding name):
  epoch tag ++ (anchor : Anchor) ++ (state : DurableCheckpoint.State at anchor.height, the own head's
  State.ofSnapshot) ++ mac. The MAC covers tag, binding id (provider file identity + settings bytes digest, as the
  anchor's binding), the anchor and the canonical state bytes (DurableCheckpointCodec's state stream; no new codec).
  NO derived indexes, no root cache, no Opened: all are recomputed from (records ≤ anchor, state) exactly as a cut
  does today (Loaded.build), so the only new premise is "these state bytes are what my own fold produced".
Which key — recommendation: a SUBKEY derived from the existing client consent key, not the key itself:
  k_frontier = cSHAKE256(key = client consent signing seed, custom "DREGG.MINI.CONSENT-FRONTIER-MAC/v1", binding id).
  Reasons: (1) no new secret to generate, back up or lose; custody of the frontier is exactly custody of the consent
  key it protects; (2) domain separation: a frontier MAC can never be a signature input or vice versa; (3) binding in
  the derivation means a frontier from another workspace binding fails the MAC, not a later comparison.
  Alternative (if Ember prefers the signing seed never be read by the provider process): a random 32-byte MAC key
  generated at first anchor write, stored 0600 next to the anchor. Cost: a second secret whose loss only costs one
  genesis fold (it is regenerable: delete key + frontier, fold once). This is the lower-blast-radius option and my
  second choice; it needs no access to the signing seed. THE CHOICE IS EMBER'S (custody).
Where it lives: <anchor_dir>/f-<binding[..16]>.frontier (0600, dir 0700, same uid check as the resident socket);
  the key never leaves the client user's process; the serving Host never sees either.
Lean shape: Kernel/ConsentFrontier.lean: encode/decode (exact, epoch-tagged, decode_encode), `Frontier.open key
  binding bytes : Except Refusal (Anchor × State)`; a new OwnBase provenance `persisted` (MAC verified under the client
  key) — stated as a TRUST PREMISE, once, like the anchor's ("the frontier bytes are the client's custody, written by a
  provider that had computed them"); resume_from_frontier: cut = Loaded.build image(take anchor) anchor.height state
  ... then validateLoaded and the SAME Anchor.ofOpened comparison (root + chain), then the suffix walk. Theorems: the
  frontier's state at the anchor equals the fold (the Session.adopt / validateLoadedFrom_eq shape, under the premise);
  checkStore_eq_checkStored unchanged (rollback/rewrite refusals before anything is read).
Refusals (each by name, none falls back silently): wrong epoch tag; noncanonical bytes; MAC mismatch ("the retained
  consent frontier does not authenticate under this client's key: it was altered or belongs to another binding");
  frontier anchor ≠ retained anchor ("frontier and anchor disagree"); Store contradicts the anchor (existing
  checkStore refusals); the frontier state does not reproduce the anchor's world root. A MISSING frontier is not a
  refusal: genesis fold (Part A), then write one. A tampered frontier is terminal for that start (no silent fold),
  because tampering with client custody is an incident the user must see.
Plants for B: flip a MAC byte -> refused by name; frontier from another binding -> refused (MAC); a frontier whose
  state carries an extra cell (sealed with the right key — the premise's pole) -> passes the MAC, refused by the
  anchor root ONLY if root-covered: so B must ALSO compare State.ofSnapshot of the fold-free cut with the frontier
  state's cell-id set = image.cellIds (State.ofSnapshot emits exactly image.cellIds; a frontier with extra ids or a
  different `available` is refused as noncanonical-for-this-image). That closes the root-coverage gap for B's base.
- 15:58 own-lean1: DurableHistoryReader + DurableReceiverCore + NativeHostReplay deps built; StoreCore failed (untyped
  `best`), fixed. own-lean2 sat 27 min in StoreCore at ~1% CPU (starved at nice 15 under load 40, not a bomb); I
  killed its lake by PID file (own-lean2.pid=497737); its lean child 513987 ORPHANED and holds slot lean-2.lock
  (fuser) -> reported to ROOT (no PID file, not killed). The seed equality now uses
  ResourceBirthCodec.lawful_encode_injective (as verifySuffixLoaded) instead of rw through toLawful.
- 16:40 own-lean4 queued for a slot (logs/own-lean4.{pid,log}).
- 17:35 ROOT/INTEGRATOR: b7b007db red in an isolated HOME on `--bin mini -- client_consent::`. Cause (r-*.log:
  "Unrecognized option: 'consent'"): the remote-plan worker is the test binary, so the resident spawn ran
  `<test binary> consent-resident` (libtest exit 101); anchors leaked into the real ~/.mini. FIX 84ebbddf (test only:
  worker env MINI_CONSENT_RESIDENT=0, HOME=stub dir, MINI_CONSENT_ANCHOR_DIR=stub/anchors). Gate tcc.sh 6: 6/6 green
  (14 passed, 1 ignored), 0 files in each fresh HOME. Pushed mirror lane/consent-model=84ebbddf (Part A Lean edits
  still UNCOMMITTED in the working tree).
- CORRECTION (measured by the plant, 20:40): an extra never-touched cell id in a sealed checkpoint does NOT pass:
  resume requires State.Admissible (cells ⊆ image.cellIds, absentBytes = the seed's), and loadChained refused the
  forged Store ("durable log suffix does not replay through the canonical executor"). The ONLY unbound component is
  State.available (the metering budget): not in the world root, not in Admissible, and a raised budget replays
  (fundedCheck is ≥). The plant now forges every budget lane +777 at checkpoint 32. Commit 25498ce4's message names
  "a cell id the image never touches" as forgeable: WRONG, corrected in the next commit.
- 19:50 Lean build of the Part A range GREEN (own-lean4: 3597 jobs, incl. ConsentAnchor, ClientConsentSession,
  DurableStoreAudit, DurableServed). Committed 25498ce4; pushed mirror + GitHub (hbox now has the deploy key).
- cand-O (cand.sh: host, consent, rust, pack) queued (logs/cand-O.pid).
- 10-15 04:30 MOVED to burst4-a (ROOT): lane /srv/lanes/consent-model (mk-lane at next a5483db3), branch rebased onto
  github/next (5 commits, textually clean) + 963d9818 (port: Loaded.atPrefixFrom_own, since state-at replaced atPrefix).
  Lean build of the range on next GREEN (own-b1, 3597 jobs). Pushed burst4 shared lane/consent-model=963d9818 (forced:
  rebase). GitHub still shows ac970311 (burst4 has no GitHub credentials; hbox mirror job carries it).
  hbox cand-O was stopped (its cand.sh child + slot waiter killed by ROOT: my PID file had held the nohup wrapper).
- burst4 cand-O started (cand.sh, logs/cand-O.{pid,status}); plant runs once the rust step yields the store helper.
- 05:05 PLANT PASS on burst4 (own-base-plant.lean, helper rust-helper/release/minidregg-link-sqlite-store; cargo fetch
  was needed first: burst4's cargo home had no git checkouts): operator cut@36 base 32 budget 1741 (forged; world root
  EQUAL to own cut's), own cut@36 base 0 budget 964; at 34 operator 1743 / own 966; Store Reader.stateAt 34 base 32
  1743; ownOnly [] at 34 base 0 966; ownOnly [own@36] at 38 base 36 962, at 34 base 0 966.
- cand-O waits for a host-wide native compiler seat (build-native-host exit 75; cand.sh now retries, bounded 4 h).
- 07:xx burst4: cand-O (lane HEAD 963d9818, Part A) and cand-B (/srv/lanes/consent-base, 2bf8e456 = rebased pre-Part-A
  84ebbddf, on next a5483db3) packed. (A cherry-pick of seat-count 195506cb into the base lane invalidated its host
  build: build-native-host.sh is a compiled input for pack; dropped, cand-rest.sh retries the seat instead.)
- PLANTS cand-O: fork (/tmp/cm-pf): at-2 rc=1 "the Store's accepted history up to height 27 differs from the retained
  consent anchor: the prefix this client admitted was rewritten"; rollback (/tmp/cm-pl): control at-2 rc=0, at-3
  rc=1 "the Store's head 26 is below the retained consent anchor at 27: the accepted history was rolled back".
- ROWS cand-O (rows-O): journey PASS 188 s, call PASS 63, send PASS 192, seats PASS 91/91, fleetsign PASS.
- stepbench root /tmp/cm-w32 (N=32 M=32 K=16) being made with cand-B.
- STEPBENCH sb-o1 (burst4, /tmp/cm-w32 N=32 M=32 K=16, 110 records; base cand-B = pre-Part-A on next, new cand-O =
  963d9818; alternated, median of 3, instructions:u --no-scale over client tree + resident; box under load from other
  lanes' gates):
  | step | base instr / CPU / wall | new instr / CPU / wall |
  | view    | 0.001 G / 2 ms / 21 ms       | 0.001 G / 2 ms / 25 ms |
  | read-at | 24.298 G / 2516 ms / 2667 ms | 24.819 G / 2542 ms / 2691 ms |
  | invoke  | 1.554 G / 269 ms / 520 ms    | 1.571 G / 266 ms / 516 ms |
  | birth   | 4.377 G / 587 ms / 1854 ms   | 4.450 G / 598 ms / 1936 ms |
  COLD (coldbench.py c1: read-at with MINI_CONSENT_RESIDENT=0, each command opens + resumes from its retained anchor):
  base 19.086 G / 1086 ms CPU / 1261 ms wall; new 19.168 G / 1097 ms / 1261 ms (+0.4%: the genesis fold to the
  anchor replaces the resume from the Store checkpoint; at 110 records it is small; it grows with history until Part B).
  read-at's resident cost (~24 G and growing per read, noted at cand-R) is unchanged by Part A: the remainder is the
  observation materialisation, not past-state bases.
- PART A DONE: lane/consent-model = 963d9818 (burst4 shared + GitHub via hbox mirror). Part B: design above, PAUSED
  on Ember's key ruling.

## CONTINUATION 2 (CONSENT-MODEL-2 handing off at ~430K tokens, 10-15) — for the successor
State: lane/consent-model = 963d9818 on next a5483db3 (burst4 /srv/lanes/consent-model, shared remote + GitHub via
hbox mirror), in ROOT's v4 queue. Part A DONE and measured (entries above). Part B PAUSED (design above; ROOT carries
the key decision to Ember: subkey from the client consent key vs a random 0600 key next to the anchor).
burst4 working tools in /srv/lanes/consent-model: cand.sh / cand-rest.sh (native seats retry; NEVER commit a script
change between a host build and pack: build-native-host.sh is a compiled input), wl.sh, run-rows.sh (SRC SET OUTROOT
ROW...), plant-fork.sh, plant-rollback.sh, stepbench.py, coldbench.py. Candidates: cand-O (Part A), base lane
/srv/lanes/consent-base cand-B (pre-Part-A). perf works on burst4. ssh: `ssh -F ~/.ssh/burst4-20261015.conf burst4-a`.
Detached jobs: `setsid nohup bash -c "echo \$\$ > logs/X.pid; exec CMD" ...` (the PID file then holds the real job).
NEXT QUEST (ROOT 10-15): cv task 01a13c42-dc55 "JPAY6 red: client consent provider refuses jpay6 config keys
continuityProviderResourceId/providerMetering". Diagnose: where the consent provider's settings allowlist lives
(Host/ClientConsentCore.lean loadSettings, around line 130-200: the accepted settings keys) and why the pay journey
writes those two keys into the consent config. Fix properly: either the two keys are NAMED in the allowlist with a
reason (what the provider does with them; if it ignores them, the journey should not write them: a key kept but
unused is a no-op the next reader trusts), or the journey stops writing them. No wildcard widening. Then run the jpay
rows on burst4 (run-rows.sh with the jpay row names from scripts/pipeline/journey-rows), push, report the row line and
close 01a13c42 with `cv task done`.

## CONSENT-3 (successor, 10-15 06:00Z) — JPAY6 (cv 01a13c42-dc55), then HOME leftovers
- Diagnosis (read at 963d9818): jpay6.sh writes continuityProviderResourceId + providerMetering into operator.json
  (since 97644f8f 10-01 "Hermes tariff by route") and copies them into deployment/continuity-config.json, which is the
  Host config AND (client_consent.rs invoke: no MINI_CONSENT_CONFIG -> the --config) the consent settings. The consent
  allowlist (ClientConsentCore.loadSettings; refusal text since 3dd5a7b1/96a4165f 10-03) lacks both. In the Host they
  are AUTHORING + service pins only: Settings.providerRoutes (grain birth / policy install law at the pinned purse),
  op 17 continuity session, op 19 metering quote, profile. NOT in NativeHost.Config, so not admission semantics.
  grain-runtime (systemd-run unit) also signs via `mini --config host_config`.
- burst4 inputs for JPAY6 built in lane: inputs/mini-hermes-test-provider (cargo --release --locked), inputs/launch-gate.
  jpay-run.sh: the jpay row with those inputs, MINI_CONSENT_ANCHOR_DIR=lane/anchors-run.
- FINDING (HOME): burst4 ~/.mini/consent-anchors holds 44 anchors written 05:32-06:13Z today: ROWS (mini without
  MINI_CONSENT_ANCHOR_DIR) write into the real HOME, not only the old tests.
- 06:40 baseline cand-O jpay (rows-jpay-O): JPAY1-4 PASS; JPAY6 FAIL "bootstrap: missing field clockTickers" (fixed on next
  by f72dbdc5). Rebased lane onto shared/next 03d338ee (3 commits; earlier ones already in next) + cherry-pick 195506cb
  (seats) as e7038991.
- DECISION (ROOT GO 06:45): (C) delete the Host's legacy scalar pair (continuityProviderResourceId, providerMetering;
  refuse by name), jpay6 & co write providerServices; (B) consent names AND uses providerServices: refuses a birth/
  policy-install draft for a grain at a service resource unless its law is ProviderRoute.policy <pinned schedule>.
  Requirements: commit names what refuses to load; plant (non-pinned schedule refused, visible in a test/row line);
  theorem names what the pinned schedule binds; grain-runtime legacy branch deletion its own commit.
- 07:00 ROOT: Ember ruled Part B key = MAC subkey DERIVED from the client consent key. Part B UNPAUSED, after the
  JPAY6 range reports rows. (Measure cold read-at vs the c1 numbers above at the end of Part B.)
- JPAY6 range edits (uncommitted, building b1 = Kernel.ProviderRouteConsent + Host.ClientConsentCore + ProviderUsage):
  Kernel/ProviderRouteConsent.lean (carries/carries_iff, transition_injective, policiesOf, checkRecord, check,
  checkIntent, check_binds, other_schedule_refused); ProviderUsage.ServiceSettings/checkedServices (one checker for
  Host + consent); Host Main: scalar pair deleted, refused by name; consent Settings.providerServices + check in
  consent (220-222) and thin (230-232); jpay6 writes providerServices + PLANT row (rogue-tariff birth intent refused
  at frame 230, pinned one consented); grain-runtime select_provider_metering legacy branch -> refusal (own commit);
  acceptance.sh, native-two-member.py, install-config-scope.jq, INTERFACES.md, hermes README, provider-services/Check.
- with-lean-slot GOTCHA: a WITH_LEAN_SLOT_PIDFILE outside slots/waiters is never "oldest" (oldest_live scans only
  waiters/), so the waiter NEVER gets a slot. Use the default pidfile.
- HOME (burst4): ~/.mini/consent-anchors also holds r-*.lock/.log (resident) files from rows at 05:47-05:48.

## CONTINUATION 3 (CONSENT-3 PAUSED 10-15 ~07:15Z: weekly wall + burst4 deletion) — for the successor
Branch lane/consent-model = 1e3ad928 on GitHub (force-pushed: rebased onto next 03d338ee). Commits on top of next:
e0c5e6fa/52d63eb7/5fe8c249 (Part A, built green before the rebase only), e7038991 (seat count, cherry-pick of 195506cb),
5fb20bc5 WIP JPAY6 range (C+B), 1e3ad928 WIP grain-runtime legacy-branch refusal (its own commit, as ROOT required).
LAST VERIFIED: nothing in 5fb20bc5/1e3ad928 has been compiled. Build b1 (Kernel.ProviderRouteConsent,
Host.ClientConsentCore, Host.ProviderUsage) never got a slot and was stopped by its PID file. Neither the Part A range nor
any row has been rebuilt or run on 03d338ee. Baseline (cand-O, 963d9818 on a5483db3): JPAY1-4 PASS; JPAY6 FAIL "bootstrap:
missing field clockTickers" (fixed on next by f72dbdc5). burst4 is DELETED, so lane trees, cand-O, inputs/ and rows-* are gone.
FIRST, in order:
1. Clone lane/consent-model on hbox (/tank/dregg-build/claude-lanes/consent-model, warm .lake by cp -al + unlink scripts).
   Typecheck Kernel/ProviderRouteConsent.lean first. Its proofs are drafts: transition_injective (simp lemma names and
   omega over the Int casts), carries_iff (split), check_binds (if_neg on isEmpty), and other_schedule_refused may need
   repair. Then build Host.ClientConsentCore and Host.Main (and the scripts/provider-services/Check.lean #eval). Then
   run cargo test for grain-runtime filtered to provider_profile_selects_one_pinned_service_without_cross_task_tariff.
2. Build a candidate (PERF-FIX-LOG recipe; never commit a script change between a host build and pack). JPAY6 needs
   GRAIN=set/bin/grain-runtime, TEST_PROVIDER (cargo build --release --locked native/hermes-test-provider) and
   LAUNCH_GATE (rustc -O deploy/grain-host/launch-gate.rs). On hbox, check the bwrap/userns input (INPUTS-HBOX-LOG).
   Run the jpay row (JPAY1-4, JPAY6). JPAY6 must show the PLANT row "consent refuses a purse law off the pinned tariff
   (plant) and consents to the pinned one" PASS. Report the row lines to ROOT, then
   `cv task done 01a13c42-dc55` quoting the JPAY6 line.
3. HOME: verify the jpay row leaves no new files in ~/.mini/consent-anchors (journey-runner now exports
   MINI_CONSENT_ANCHOR_DIR=$R/consent-anchors per row; jpay6 sets its own and passes --setenv to the controller unit).
   Run the fresh-HOME consent test set filtered (`--bin mini -- client_consent::`) as the control. On burst4 at 07:00,
   ~/.mini/consent-anchors held 50 files from rows (anchors 05:32-06:13, r-*.lock/.log 05:47). Delete nothing in
   Ember's homes.
4. PART B is UNPAUSED. Ember's ruling: the frontier MAC key is a SUBKEY DERIVED from the client consent key, not a separate
   file (the design above: cSHAKE256 of the consent signing seed, custom "DREGG.MINI.CONSENT-FRONTIER-MAC/v1", binding id).
   Build it from the PART B DESIGN section: persisted frontier, refusals by name, the plants listed there (including the
   cell-id-set / `available` canonical-for-image check). At the range end, measure cold read-at against c1 (base
   19.086 G / 1086 ms, Part A 19.168 G / 1097 ms). Push, then report.
with-lean-slot gotcha: never set WITH_LEAN_SLOT_PIDFILE outside slots/waiters/. A waiter there is never "oldest", so it
never gets a slot.
