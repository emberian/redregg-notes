# FLOORS log (continuation file) — started 2026-10-14
Lane: floors (Claude). Issue emberian/minidregg#1 (akapug). Review: CONTRIB-REVIEW-20261014.md #1.
Base: mirror refs/heads/next = 68f78d23 (2026-10-08, STALE, older than main; not an INTEGRATOR publish) -> base main 30a5009a, rebase onto next when published.

## events
- 11:35 start. read issue, review, safety block. admission = Theory/CanonicalResourceKernel.lean Admission.sourceSolvent (isIssuerMint ∨ amount ≤ balance), duplicated in admissionConditions + Operation.refusal?.
- 12:40 lane hbox:/tank/dregg-build/claude-lanes/floors/src (git clone of mirror @30a5009a, branch floors; .lake/build cp -a (real copy, 667M) + .lake/packages cp -al from warm-7dea0626; warm Lean == 30a5009a Lean, no-op build confirmed).
  Edit copies in my scratchpad fl/ then scp.  Theory.CanonicalResourceKernel + BookInvariant GREEN: Book.floors field; ops setFloor (zero posting from the well) + sweep;
  Admission.sourceWithinFloor/wellFormed (isIssuerMint DELETED); refusals belowFloor/floorBelowBalance/sweepInexact, DeregistrationRefusal.floorRemains;
  RegistrationAdmission + DeregistrationAdmission + AccountSupported cover floors; theorems admitted_preserves_floors, Batch.apply_withinFloors,
  outstanding_le_sum_floors, sourceWithinFloor_iff_preFloorRule, admission_iff_preFloorRule, sweep_materializes_display; creditBook example + named refusals.
- PLANT (observed red, reverted): Book.floor := if account = asset then 1000000 else ... (wells unbounded = the deleted rule).
  Red: issuance_cap_refused (decide proved the proposition false, line ~1394) + admitted_preserves_floors/outstanding chain. Reverted, green.
- 13:30 DESIGN SETTLED (after one reversal): deregistration REFUSES a remaining floor (`floorRemains`), it does not erase it — erasing broke Seat's
  `Operation.apply_deregisterAccount` commutation; Seat gets Inv.floorFree (seat purses have floor 0 => ops_nonneg still holds).
  setFloor's verb = mintAsset in ResourceMoneyWire.operationVerb (extending credit = issuing). Genesis: Config.issuanceCap (frame GENESIS-SOURCE/v6,
  v5_config_refused), unfundedBook floors (asset,asset) := cap, Valid adds Σ initialBalance ≤ cap, initialBook_withinFloors.
  Codecs: Book wire frame DREGG/RESOURCE/3 + root DREGG.RESOURCE.STATE/v3 (tags resource_state_v3, dregg_resource__byte_v3), StoreCodecBook dregg/book/v2 (floor ns),
  op tags 5 setFloor / 6 sweep; realm well: WellOp.floor, DREGG/WELL/COMMAND/v2 (tag well_command_v2), Rust `mini well --action floor`, jwell rows a-caps-*, r-mints-past-cap-gold.
  Effects: Settlement.reconcile + KeyedTarget (ImplementationRefinement instance, duplicate_forward_no_second_effect, lost_reply_reconciled) — file compiles.
  Genesis JSON producers (20 scripts) carry "issuanceCap":"1000000000000000". PROJECT.md notes (floors; class 1/2/3).
  Waiting on umbrella u1 (stale, started 12:00) before a fresh build (no concurrent lake in one tree).
- 13:55 stopped my stale u1 (systemctl --user stop run-u21131.scope; scope found from ub.pid's child, Description = my ub.sh u1). targeted t1/t2 GREEN after Seat fixes
  (Inv.floorFree, closeDeregistration 5th conjunct). ROOT: all Lean builds via /tank/dregg-build/pipeline/slots/with-lean-slot (tb.sh updated).
  u2 = slotted deployed umbrella (floors/tb.sh u2 ..., status floors/tb.status, log src/build-logs/u2.log). Issue reply DRAFT at redregg/work/ISSUE1-REPLY.md (COMMIT-SHA placeholder).
  NEXT: u2 green -> objective-manifest ratchet (check-objective-proofs.sh proofs --draft) -> commit -> candidate -> fixture re-emits -> rows.
- 16:30 REBASED onto next 0125b224 (one WIP commit d1875b00 on lane branch floors, not pushed). u3 (pre-rebase) only PurseRefill red -> fixed; u4 (rebased) only JobMoney red -> fixed
  (simp floorSetting?, RegistrationAdmission .1.2.1, fixture well cap). u5 queued in slot. Host/PrivateCircuitPlanFixture red pre-existing (toJson unknown; never built on warm).
- 22:20 u7 (THREADS=1, outside slot per ROOT exemption) GREEN except two reds already on next: Host.PrivateCircuitPlanFixture (toJson) and
  Kernel.NativeCurrentMemberKey (NativeHostReplay.verifyLoaded signature; I touched neither). Deployed built; AxiomCensus: no sorryAx; minidregg-host exe built.
  COMMIT 5225376f on next 0125b224, pushed lane/floors (mirror from hbox; GitHub relayed from the Mac: hbox has no GitHub key).
  ratchet: rat.sh -> check-objective-proofs.sh proofs --draft 0125b224..HEAD (slot), log build-logs/rat1.log.
- 00:10 ratchet: 85 added / 8785 redefined / 15 removed / 16 restated, 0 unadmitted; reasons written per removed/restated row; pinned 40801 rows.
  COMMITS 5225376f (floors) + 1b029fee (gates pin), pushed lane/floors to mirror AND GitHub directly from hbox (deploy key now present).
  Rust roles built (logs-rust.out EXIT=0, warm rust-target copy). Candidate: floors/cand.sh (host/consent via slot, pack) status floors/cand.status.
- 05:30 moved candidate/rows to burst4 per ROOT (hbox queue stopped by PID: cand.pid + its direct child). burst4 lane /srv/lanes/floors (mk-lane, checkout floors 1b029fee).
  Candidate PACKED /srv/lanes/floors/candidate (host 775/775, consent after a seat wait, rust, pack). Rows running: rows1 (journey call send objectrecord bounty jpay), rows1.log.
- 07:00 ROWS on burst4 candidate (1b029fee binaries, SRC at 506182d1): journey PASS (J0-J8, JROT, JROTL, JRLANE, JGATE, JAUDIT), call 63/63, send 192/192,
  objectrecord 39/39, bounty 190/190 (after caps fix), JPAY1 15/15, JPAY2 18/18, JPAY3 24/24, JPAY4 25/25 (PAY_WATCHER_BIN=candidate/bin/pay-watcher), JPAY6 UNCONFIGURED (GRAIN input absent),
  journey J0-J5+KW (jwell) 19/19 incl. caps + past-cap refusal.
  Found+fixed my own bug: 14 producers had literal \"issuanceCap\" (JPAY2/3 SyntaxError) -> 506182d1. Bounty capped its wells -> 506182d1.
  Fixture re-emit f580e539 (NativeAcceptedFixtureData; authority unchanged & builds; transcripts PASS; fixture-authority OK; AxiomCensusResearch builds).
  Pushed lane/floors = f580e539 to burst4 remote + GitHub. rat3 (objective proofs at HEAD) running.
- 07:40 DONE. objective proofs at f580e539: no changes, 0 unadmitted. cv task 01a13e34 (sweep clock/grant binding, pay-well cap raise, veto). ISSUE1-REPLY.md SHAs filled. Final tip lane/floors f580e539.

## CONTINUATION (for a successor; FLOORS at ~590K tokens, 2026-10-15)
STATE: lane/floors = f580e539 on next v1 0125b224 (commits 5225376f kernel, 1b029fee objective pin, 506182d1 row fixes, f580e539 fixture re-emit).
Pushed to burst4 /srv/git/minidregg.git and GitHub. ROOT accepted. ISSUE1-REPLY.md stays UNPOSTED (Ember posts).
TASK NOW (ROOT): rebase lane/floors onto next v3.1 03d338ee (v2 a5483db3 changed every world-root value: compressed world root; INTEGRATOR
re-emitted NativeAcceptedFixtureData at ca427c06). Expect f580e539 to conflict with ca427c06: resolve by DROPPING f580e539's hunk and
re-emitting the fixture at the rebased tip (generator refuses unless Assurance/NativeAcceptedFixtureAuthority.lean is unchanged — that is the check).
Then on burst4: umbrella + objective ratchet once, rows, push to burst4 remote + GitHub FROM burst4, report sha + row lines to ROOT.
HOW (all measured this session):
- burst4: ssh -F ~/.ssh/burst4-20261015.conf burst4-a; lane /srv/lanes/floors (src, rust-target, artifacts, candidate). Lean builds ONLY via
  /srv/pipeline/slots/with-lean-slot. git identity set in repo (ember arlynx / bobb@ember.software, gpgsign false). GitHub push works from burst4.
- Rebase: cd /srv/lanes/floors/src; git fetch /srv/git/minidregg.git next (or GitHub); git rebase 03d338ee. Likely conflicts besides the fixture:
  Kernel/NativeHost.lean (one doc line), scripts/gates/objective-contract-changes.txt + objective-manifest/*.tsv (the 1b029fee pin: DROP my
  pin hunks, re-run `scripts/check-objective-proofs.sh proofs --draft 03d338ee..HEAD`, write reasons — my reasons script ledger_fix.py is at
  hbox:/tank/dregg-build/claude-lanes/floors/ledger_fix.py and scratchpad; then `--pin`, separate gates commit).
  New code on next may construct `Book` literals (add `floors := 0` / 4th field), use old Admission fields, or write genesis JSON without
  "issuanceCap" (grep: sourceSolvent|leaseWellFormed|isIssuerMint|leaseRecords := |"tailBound").
- Umbrella: Deployed minidregg-host + Host/*.lean + AxiomCensus (scripts/lane/ub.sh target list). Known reds already on next v1:
  Host.PrivateCircuitPlanFixture, Kernel.NativeCurrentMemberKey (re-check on v3.1).
- Candidate: /srv/lanes/floors/cand.sh then cand2.sh (consent retries while "Lean compiler seats are occupied"; move a failed consent-out aside;
  MINIDREGG_NATIVE_JOBS must be 1 or 2). Pack refuses unless compiled inputs equal the host-build commit, so build host at the final Lean tip.
- Fixture: bash scripts/kern/regenerate-native-fixture.sh /srv/lanes/floors/rust-target /srv/lanes/floors/artifacts (after candidate);
  then lake build Assurance.NativeAcceptedFixture Assurance.NativeAcceptedFixtureAuthority (slot), lake build AxiomCensusResearch (slot) +
  scripts/check-native-transcripts.sh, scripts/pipeline/check-fixture-authority.sh <base>..HEAD.
- Rows: /srv/lanes/floors/run-rows.sh SRC SET OUT journey call send objectrecord bounty jpay  (PAY_WATCHER_BIN=$SET/bin/pay-watcher for JPAY1/4);
  jwell via /srv/lanes/floors/jwell-run.sh (JOURNEY_STEPS="J0 J1 J2 J3 J4 J5 KW").
LAST ROW LINES (f580e539-era candidate): journey PASS; call 63/63; send 192/192; objectrecord 39/39; bounty 190/190; JPAY1 15/15, JPAY2 18/18,
JPAY3 24/24, JPAY4 25/25, JPAY6 UNCONFIGURED (no GRAIN); jwell KW 19/19.
FOLLOW-UPS: cv task 01a13e34 (sweep clock/grant binding; pay-well runtime cap raise; Ember veto on issuer cap).

## FLOORS-2 (successor, 2026-10-15)
- 06:25 burst4 /srv/lanes/floors/src: branch floors-v1-f580e539 keeps the old tip. floors reset to next v3.1 03d338ee; cherry-picked 5225376f -> 03205cf6 (clean; NativeHost/PersistedCodecTags/jpay6 auto-merged),
  506182d1 -> 2ca28b09, 195506cb -> 743fc5ce (seats). DROPPED 1b029fee (all 244 files = objective pin) and f580e539 (fixture) whole; both redone at the tip.
  grep sourceSolvent|leaseWellFormed|isIssuerMint|"tailBound": only doc mentions; new-on-next Book literal Assurance/QuotaGcSettlementWitness already has floors (it predates? auto); jpay6 has issuanceCap.
  u1 umbrella (ub.sh via with-lean-slot swarm-build, u1.pid, src/build-logs/u1.log) running.
- 06:5x u1 umbrella on 743fc5ce FINISHED (EXIT=1) before ROOT's pause: only reds = Host.PrivateCircuitPlanFixture (toJson unknown, lines 23-26) and
  Kernel.NativeCurrentMemberKey (42:47 application type mismatch; 43:4 `.error`); neither file differs from 03d338ee (still on next, NOT mine).
  AxiomCensus: "none on sorryAx or a declared axiom". Everything else in Deployed + Host/* + minidregg-host built at 743fc5ce.
- PAUSED (ROOT/Ember: usage wall, burst4 deleted). Pushed lane/floors-rebase-wip = 743fc5ce to burst4 shared + GitHub (ls-remote verified).
  lane/floors on GitHub is STILL the old f580e539 (on next v1). Not mine, left alone: a systemd scope running objective-native-acceptance.py
  out of /srv/lanes/floors/src/.lake/kp-fixture.* (not started this session; dies with burst4).

## CONTINUATION (FLOORS-2 -> successor, 2026-10-15 ~07:00)
STATE: GitHub lane/floors-rebase-wip = 743fc5ce on next v3.1 03d338ee:
  03205cf6 kernel(floors)! (=5225376f replayed clean) · 2ca28b09 rows(floors) (=506182d1) · 743fc5ce cherry-pick of 195506cb (seats; keep as its own commit).
  1b029fee (objective pin) and f580e539 (fixture re-emit) were DROPPED, not replayed: both must be redone at the tip.
  Umbrella at 743fc5ce MEASURED green except the two next-side reds above.
DO FIRST (on whatever box replaces burst4; Lean only through that box's with-lean-slot):
 1. clone/fetch lane/floors-rebase-wip; confirm next has not moved (else rebase again; the 3 commits replayed with zero conflicts onto v3.1).
 2. objective draft: `OBJECTIVE_KEEP_TMP=1 OBJECTIVE_SELF_TESTS=0 scripts/check-objective-proofs.sh proofs --draft 03d338ee..HEAD` (slot), read
    build-logs/objective/draft-review.txt, apply reasons with ledger_fix.py (hbox:/tank/dregg-build/claude-lanes/floors/ledger_fix.py; sha in the
    restated suffix must be 03205cf6, not 5225376f; it asserts every removed row is known, so new rows from next-side causes fail loudly — add a reason
    per cause), append final-ledger.txt lines to scripts/gates/objective-contract-changes.txt, `--pin`, commit as its own gates(objective) commit.
 3. candidate (cand.sh/cand2.sh recipe in the continuation above; host build at the FINAL Lean tip; seats change already in tree),
    fixture re-emit (scripts/kern/regenerate-native-fixture.sh; generator refusal on a changed NativeAcceptedFixtureAuthority.lean is the check),
    fixture builds + check-native-transcripts + check-fixture-authority 03d338ee..HEAD, commit fixture(native-accepted)!.
 4. rows: journey call send objectrecord bounty jpay1-4 jwell (JPAY6 UNCONFIGURED); push to lane/floors (force-with-lease; old tip f580e539) + GitHub; report sha + row lines to ROOT.
