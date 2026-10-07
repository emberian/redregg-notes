# FALLOW-DIGEST (FALLOW-KEEPER, 2026-10-04 evening EDT; ended early on ROOT's resume message)

LANDED
- 259a2fb0 (fk1): protocol/host-operations.json registers ops 210-214 ACTIVITY_PLAN/ASSEMBLE/SUBMIT/LOOKUP/VIEW
  (receiver fnDispatch, routes public+operator, from Host/Main.lean arms + transport.rs); native/host-operations.rs
  regenerated. Declarations only, no Lean. Gate burst-gate /srv/lanes/fk-1: umbrella 9685 0 built, ALL rows PASS
  incl. host-operations + test-host-operations.py + objective-proofs 2099/1643.
  main = next = green = 259a2fb0 (green moved from 5a079a9c, forced tag). Both f4 bases FROZEN 259a2fb0
  (burst-gate swap; burst-lane1 ff in place via bundle, --verify 0 modules compiled). TIPS appended.

BOUNCED / NOT LANDED
- Batch fk2 = 259a2fb0 + W27-hybrid-pq-3 (8a2a5764) + W21-BYZ-TARGETED (da3c8909) + W30-CORE4-DIGEST 1db5fd4a (3c8e86df)
  + W40-verify-mldsa (16d22e17) + W38-JOURNEY-ROWS-WIRING (f3714442) + pins fab4a617. Candidate: burst-gate
  /srv/lanes/fk-2/src branch fkcand fab4a617; Mac mini-unified-push-20261003 refs/fk/*.
  Gate: umbrella 9688 rc=0, closure 665, boundary, hygiene, surfaces 1415, host-operations, axiom-census, objective-proofs
  2099/1643, Rust rows (311 s) all PASS. ONE RED: exports -- `implemented_by at Theory/Sp800185Cshake256Fast.lean:27`
  (W30's Compiler->Theory move; the exports gate does not accept it at the new path). Fix the script/allowlist or the
  attribute in W30, OR re-gate the other four without W30 (they are independent of it). Nothing of fk2 pushed.
- W30 note: lane branch also has 3c541dd5 (digest primitive) + a72b9766 (WIP); only 1db5fd4a was requested/picked.
- ob2-finish needs W17 36a58c81 which is NOT on main although MERGE-QUEUE has it as LANDED c13 (content absent: no
  Primitive modulo/lessEqual in Compiler). Verify that LANDED line; ob2 also conflicts in docs/OBJECTIVE-BEND.md.

HELD-FOR-KEEPER (strict: any cherry-pick conflict onto 259a2fb0; marked on each queue line with the file)
- lean-build-surfaces.json only (mechanical, regenerate): W02-PAY-WEEK-EXACT, W31-RETIRE-DECIDED-VIEWS, laws-receiver,
  fn-direct, schema-v2-2 (the first conflict seen; later ones may exist).
- ob2-finish (docs/OBJECTIVE-BEND.md), W15-TRAFFIC-V13 (cohort-native-tcp.py), W04-SPK-V4-LAND (Kernel/NativeHostReplay.lean),
  W35-RC-DEDUP (cohort_tcp.rs), W43-ORPHAN-GATES + native-exercise-2 (scripts/local-gates.sh GATES line),
  deploy3b-3 (mini-sdk durable.rs; main already has d982e1d5 sync_ancestors).
- journey-reds: not attempted (held by ROOT: J5/JROT edits weaken a check; fairy-green 671f7191/d7e2b27f; W05 stays held).
  Its path on burst-lane1 is /srv/lanes/journey-reds (not /src), so fetch failed anyway.

JOURNEYS (newest tip run: df0cd116, 20:28Z, none on 259a2fb0 yet; runner log shows no newer tip)
  PASS=9 FAIL=4 ABSENT=2: J5 (2/6 strangers not refused), J8 (1/5), JROT (3/30; NE2 D4 8f987600 on main since should fix),
  rooms red; activity + seats ABSENT. Unchanged all day.

BURN (byzburn left running on all three f4s; loads under 10 only on burst-e2e, so no byzburn2 started)
  results.txt lines: burst-gate 335831, burst-lane1 336156, burst-e2e 109051; FAIL count 0 on all three. No BURN-FAILS copied.
LOADS (23:55): burst-gate 12.0, burst-lane1 17.2, burst-e2e 7.9 (avail 91G/90G/28G).
