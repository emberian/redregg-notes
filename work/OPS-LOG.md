# OPS-LOG — BUILD-OPS continuation (2026-10-17)

Read first: CHARTER.md, ~/dev/redregg/work/nanodregg-scout/ASSEMBLY-ops.md §5, then
decisions/ops.md (OPS-0..5) in the ops worktree.

## Landed
- 28de15e `host:` (cross-layer, ROOT-ruled): Host/Exit.lean (D5 exit table: ExitClass, Status one
  per code, codesOf; every fault → status; locked fatal; io 13 fatal / ioServing 6 restart),
  Host/Check.lean (D6 `host check STORE [--anchor H:CHAIN]`, incl. the pre-base history recover),
  Host/Proofs/{Exit,Check}.lean (13 theorems, second-read by HOST-4). Pushed.

## Landed on hbox (main lives there; worktree /tank/dregg-build/nanodregg/wt/ops; Mac worktree REMOVED)
- b2b901d `ops:` Ops/{Founder,Plants,PlantsMain,Units,Main}.lean, Ops/Proofs/Units.lean, lakefile
  (lean_lib Ops; exes store-plants, emit-units), decisions/ops.md OPS-0..5. store-plants ALL PASS
  (17 lines) on hbox at 99b5cbc. emit-units renders ok (sample in hbox logs/ops-units/).

## Pending files (hbox logs, not in tree)
- /tank/dregg-build/nanodregg/logs/ops-RUNBOOK.md → lands as deploy/RUNBOOK.md (NOT ops/: `ops/` and
  `Ops/` are one dir on the case-insensitive Mac; asked GATES-2 to replace the OWNERS row `ops/` by
  `deploy/`, add generated.tsv `emit-units	deploy/units`, classify Ops as tooling in size.py,
  and later a store-plants standing stage). Update the RUNBOOK's paths ops/ → deploy/ and its
  §1 note: KERNEL-24 (9d2e5df) decided "a call names its World; genesis commits to name, nonce,…"
  — check what landed before writing the HOST-side consequence.
- Then: `emit-units deploy/units` + commit the two .service files right after GATES' row.

## Open / next
1. Live systemd harness (deploy/live/), NOT STARTED: ROOT moved it to burst5 (Linux systemd, user units,
   /srv/scratch only, `ssh -F ~/.ssh/burst5-20261016.conf burst5-a`) once MIGRATE-HBOX's recipe
   lands. Must report: whether CLIENT-9's floor suffices for the Lean resident, exit 3 restarted,
   a fatal exit stopped (systemd) / throttled by name (launchd). Units started by name, stopped by
   name, bounded waits, PID files. Labels software.ember.nd-ops-* on launchd.
2. nd-supervise's own exits: CLIENT-2 (a1612c507f0ff2b93) agreed to land `SupervisorExit`
   (refusedAtLaunch 64 fatal, childUnroutable 65 fatal, childSignaled 66 restart; reuses
   Host.ExitClass; code_disjoint_host) when builds resume. I flagged the import cycle
   (Host.Loop imports Protocol.Table) → CLIENT-2 took it: module Protocol/Exit.lean, ns Nanodregg.Protocol.SupervisorExit (imports Host.Exit; Emit.Rust imports it); sha comes when builds return. Then
   Ops.Units' `prevent` = Status.codesOf .fatal ++ supervisor fatal codes; update ofNode_prevent.
3. Plants not yet run: live copy during a running serve (D7 race); a SEALED Store (≥1 MiB:
   segmentShort, history check after a real seal). Founder calls need notBefore=i,
   validUntil=i+windowMax/2 to go past height 1024.
4. HOST-4 (a127d18f879bdd316) rebases D4 onto 28de15e: deletes Status.fuel (code 4 unused),
   adds reopenFailed/reopenDiverged/noThreads fatal, lifetime/stream restart (stream eof → .eof);
   mirrors "corrupt history" in the follower audit. I second-read their D4 statement (sent).
5. OPS-2 replay: KERNEL-4 owns D3; PROTOCOL-4 (a987d514b07b38010) has the wrongWorld row blockedOn
   KERNEL. RUNBOOK §1 says never reuse a LABEL until then.
6. OPS-1 export/import verbs: nobody builds them yet (law text only).
7. BAR: PERF owns it (scripts/bar.sh); OPS builds none (OPS-5, confirmed).

## Laws attacked
- Law 1 → amended (OPS-1, charter b3787d3).
- None other argued wrong. Candidate: law 7 vs launchd (a fatal verdict cannot stop a launchd job;
  the Mac is half-supervised by construction).

## Scratch
Scratch clone + early drivers: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/ops-lane/ (plants dirs sp*, replay/, plants.sh — mine, deletable).
No launchd/systemd job was ever bootstrapped by OPS. No processes left running.

## GATES-2 aa4c0ab (after handoff)
- OWNERS: `deploy/	OPS` replaces `ops/`; check.py gate `paths` refuses case-colliding paths.
- Ops is in TOOLING_LIBS (size: tooling row; C9 refuses a deployed module importing Ops).
- OPS-2 MUST land `gates/generated.tsv` row `emit-units	deploy/units` IN THE SAME COMMIT as
  deploy/units/linux/*.service, with `--cross-layer "gates/generated.tsv: the emit-units row, landed
  with the files it checks"` (pre-agreed by GATES-2).
- store-plants standing stage: command sent to GATES-2
  (`$T/.lake/build/bin/store-plants $T/.lake/build/bin/host $T/<fresh dir>`; writes only under DIR).

## CLIENT-2 5122e62 (after handoff): Protocol/Exit.lean LANDED
- ns Nanodregg.Protocol.SupervisorExit: all = [refusedAtLaunch, childUnroutable, childSignaled],
  code 64/65/66, cls fatal/fatal/restart (Host.ExitClass), `codesOf (k : Host.ExitClass) : List Nat`.
  Theorems (Protocol/Proofs/Exit.lean): code_injective, code_disjoint_host, code_pos_lt, restart_fatal_disjoint.
- OPS-2: Service.ofNode's `prevent := Status.codesOf .fatal ++ SupervisorExit.codesOf .fatal`
  (Ops/Units.lean imports Protocol.Exit); restate ofNode_prevent over both tables (a Host status
  prevented iff fatal; a supervisor exit prevented iff fatal); re-render units before landing
  (old nd-supervise numbers 2/70/1 are gone: 64/65/66).

## OPS-2 (successor, spawned 2026-10-17 ~12:20Z)
- LANDED c835c6d `ops!:` preventCodes over both tables (+ theorems, tooth), start limit 5/120 s,
  deploy/units/{linux/*.service,EXITS.md} rendered (hostAction/supervisorAction exhaustive),
  deploy/RUNBOOK.md (§7 → EXITS.md; §1 KERNEL-24 NOT built at 7797070), generated.tsv row,
  decisions OPS-6. ROOT + HOST-5 told (HOST adding a Status needs a hostAction arm).
- Lane scratch: Mac .../scratchpad/ops2/ ; hbox logs/ops2-*.
- NEXT: plants (live copy D7 deterministic interleave; sealed Store via ~48 KiB-slot creates,
  weightMax 256 KiB, sealMinBytes 1 MiB), then burst5 live harness, then OPS-1 verbs.
- LANDED 4ae6608 `ops:` live/sealed/replay plants (9 rows, ALL PASS ~4 s at 9e91ede); RUNBOOK §1/§4/§5;
  OPS-2 CLOSED, OPS-3 ACCEPTED. Lesson: long-lived pipe readers must be `.dedicated` tasks.
- AGREED with HOST-6 (a59922b2afa99acbc): HOST-25 adds foreignOrigin (30) + its hostAction arm
  cross-layer; then OPS adds plants (origin flip through `serve` → corrupt; foreign-origin splice
  over a sealed Store → foreignOrigin). HOST-6 messages when on main.
- burst5: INTEGRATOR-5 OK'd a light harness now (≤2 cores, /srv/scratch); must tell it unit names;
  NOT during its batch-2 publish+journey (~3–5 h after 12:40Z; ask for the window).
- LANDED fd1d4b2 `ops!:` units pass `--exec HOST` (rendered units exited 64 ProgramOutside at every start).
- LANDED e31b4ee `ops:` deploy/live (harness.sh SRC ROOT, feed.py, README run 1), live-calls exe, emit-units --live.
  burst5 run 1: A floor OK, B kill→137 restarted, C locked stopped, D start limit, E LimitFSIZE→153 SIGXFSZ (HOST-6 fix pending),
  F follower needed mkdir. CLIENT-2 fixed 128+N→66 at c6e4abf.
- burst5 CLOSED to OPS until INTEGRATOR-5 says "window open". Run 2: copy fresh binaries (host after HOST-6's SIGXFSZ fix,
  nd-supervise ≥ c6e4abf) to /srv/scratch/ops2-live/src/bin (+feed.py), then `harness.sh /srv/scratch/ops2-live/src /srv/scratch/ops2-live/run2`.
  Run-1 data at /srv/scratch/ops2-live/{store,...} (old layout; mine). Teardown: BURST5-UP-LOG item 7.
- Waiting on HOST-6: foreignOrigin arm (they add it) + my two plants after HOST-25 lands.
- Small todo: supervisorAction childSignaled text could say "on Linux, any mechanism exit ≥128".
- NEXT: OPS-1 export/import, agree with HOST-6 (a59922b2afa99acbc) + PROTOCOL-5 before touching their files.
- LANDED 46a1189 proposals/ops.md OPS-P1. KERNEL-6 (aa36c7021124d8bdb) ACCEPTED w/ amendments → KERNEL-29 after World port:
  Carried={trie,allowance}, origin over root(trie), carry_carried/carry_origin_ne_genesis/carry_canon. PROTOCOL-6 (abd8f012f13228e0b)
  PROTOCOL-29: carry the in-window journal (A) or clients get wrong REFUSED; I agreed + told KERNEL-6 ⇒ carry keeps height.
  HOST-6 + CODEC-2 (a5db8dcb963c5d57d) answers pending. Update proposals/ops.md when KERNEL-29 is written; plants then.
- LANDED df033f2: originPlants (6 rows), burst5 runs 2/3 (66 on kill; follower = reproduced genesis; RUNBOOK §2). Only open row:
  append-failure-is-uncertain-restarted (waits HOST-6 SIG_IGN). Run dirs /srv/scratch/ops2-live/run{2,3}; src/ holds binaries.
  Re-run: copy new host to src/bin, `src/harness.sh /srv/scratch/ops2-live/src /srv/scratch/ops2-live/runN` ONLY in INTEGRATOR-5's window.
- LANDED 1d326dd: burst5 run 4 ALL PASS on HOST-27 (exit 3 restarted for real). OPS-P1: HOST-28 accepted (stamped file,
  --digest, no stability promise; "rarer" withdrawn). CODEC-2 pending. Next buildable: carry plants after KERNEL-29 + CODEC
  carried codec + HOST-28 verbs (carry-roundtrip incl. lookup-committed-after-import, carry-mismatch, carry-not-history).
  burst5 teardown (BURST5-UP-LOG item 7) when ROOT says.
- burst5 TEARDOWN DONE 10:38Z (units, links, nd-bwrap). Data kept at /srv/scratch/ops2-live. A later run: ask ROOT first, reinstall nd-bwrap.
- STOPPED, waiting for KERNEL-29 or CODEC-2's OPS-P1 answer.
- LANDED (see hbox log ops2-commit9): OPS-P1 AGREED by all four; CODEC-22 content-addressed stamp. Build order KERNEL-29 → CODEC-22 → HOST-28 → OPS plants.
- KERNEL-7 (ac9b1fb8228590424) replaced KERNEL-6: World port carries a one-line Ops/Founder.lean edit (w.live X.env me), agreed by OPS-2; KERNEL-29 after the port, KERNEL-7 messages before landing.
- 7c43273 World port landed (KERNEL-7): store-plants 33 rows ALL PASS + emit-units --check ok on it. CODEC-2 retired → CODEC-3. KERNEL-29 after KERNEL-31; KERNEL-7 messages OPS + CODEC-3 before landing. Still STOPPED.
- KERNEL-31 Ops hunks (Founder.world : Except, Founder.create w/o name, expected : Except String) READ and OK'd to KERNEL-7. KERNEL-29 after it. Still STOPPED.
- KERNEL-7 retired → KERNEL-8 (a3757d866eb64f133); KERNEL-29 is 3rd in its queue (after D5c review, Turn-weights move); it sends the sha. CODEC owner: CODEC-3. Still STOPPED.
- Owners now: HOST-7 (ae95b4547c42ba031), CODEC-4 (aaba467e9c60e21bc), KERNEL-8 (a3757d866eb64f133). Order: KERNEL-29 → CODEC-4 carried codec → HOST-7 export/import --digest → OPS plants + RUNBOOK §6. Still STOPPED until KERNEL-29 sha.
- HOST-30 (HOST-7, ROOT-ruled BUILD): index.log in STORE; indexShort 45/indexCorrupt 46 arms (HOST adds cross-layer); Host.Store.layout/backupOrder; HOST sets Plants.files := backupOrder. OPS after landing: emit-units renders deploy/units/STORE.md from layout; RUNBOOK cites it; plants (a) orphan page past indexOffset ignored/truncated, (b) index before base → writer height or indexShort, (c) right order across a seal. Waiting for HOST-7 sha (and KERNEL-29).
- LANDED add00d8: HOST-30 OPS duties (orphan-index-page-* 3 rows, copy-index-before-base-wrong-order → indexShort; deploy/units/STORE.md from Host.Store.layout; RUNBOOK cites it). HOST is HOST-8 (a7b51f5a41be70521), told of standing coupling (Status arms + layout re-render). STOPPED until KERNEL-29.
- CODEC is now CODEC-5 (afad87333c5b8a98a). Order: KERNEL-8 KERNEL-29 → CODEC-5 carried codec → HOST-8 export/import --digest → OPS plants + RUNBOOK §6. STOPPED until KERNEL-29 sha.
- LANDED 973dc44: indexMovedPlant (index-moved-under-writer 48, index-moved-restart-truncates) for HOST-8's 9dad4d2 (entryUnfit 47 / indexMoved 48 arms added by HOST-8). STOPPED until KERNEL-29.
- KERNEL-29 LANDED b8e0f82 (Carried {trie, allowance, height, journal whole}). Carry plants + §6 DRAFTED at scratchpad ops2/carry/DRAFT.md; land after CODEC-5 carried codec + HOST-8 HOST-28 verbs (confirm CLI output names).
- HOST-8 CONFIRMED carry contract: export prints carried/from/anchor, writes only OUT; import STORE NAME IN --digest HEX [--nonce HEX32]; usage/carryMismatch digest/shapeMismatch/decode before any Store path (exception: 'carryMismatch reopen' may leave a Store); check prints carried height. HOST-8 lands after CODEC-5. Draft rows unchanged (row 7/8: assert no Store created; reopen case is the only one that may leave files).
- CODEC-22 LANDED 28b4a38 (CODEC-5): carried = trie listing ‖ u64 allowance ‖ u64 height ‖ journal ascending by txId; decode refusals kernel/leaf-fit, kernel/trie-order, kernel/ascending; teeth in Codec/Proofs/WorldTooth.lean. Draft adds row: carry-journal-swapped (two journal entries swapped in the file, digest recomputed) → refused at decode (carryMismatch decode / kernel/ascending on stderr), no Store. Waiting for HOST-8's verbs sha.
- INCOMING (ROOT): HOSTING-15 via HOSTING-5 — deploy/ emits the broker's production trust-anchor file from pinned webpki-root-certs, with a generated.tsv-style byte-for-byte check against the crate's pinned bytes (shape like emit-units/STORE.md). No action until HOSTING-5 asks. Carry plants still wait on HOST-8.
- HOSTING-15 anchors: agreed with HOSTING-4/5: deploy/tls/anchors.pem, emitted by Rust bin emit-anchors [--check] in new workspace member deploy/anchors, webpki-root-certs =1.0.9, PEM per root in crate order. BLOCKED on GATES-2 (aedb775dc4517c504): generated.tsv rows only run lake exes; asked for a cargo:BIN row form. Then: one commit with crate+pem+generated.tsv row (cross-layer gates/generated.tsv).
- HOSTING is now HOSTING-5 (a16c2e5b494aa5e26); anchors plan re-sent there. Built in hbox wt/ops (UNCOMMITTED): deploy/anchors/ crate (emit-anchors, 2 tests, clippy+fmt clean), root Cargo.toml member + Cargo.lock, deploy/tls/anchors.pem (121 roots, openssl-parsed). Waiting on GATES-2 for a cargo generated.tsv row.
- LANDED f77c564: deploy/tls/anchors.pem + deploy/anchors (emit-anchors) + generated.tsv cargo row (GATES-2 2ed0386); OPS-7. Next for HOSTING-5: render the keybroker unit with emit-units when they send its argv. Carry plants: wait HOST-8.
- LANDED 60a12e5: RUNBOOK §2a custody paths (CLIENT-19 StrictModes, Dir(PATH)/keyFileDir, Owner, Mode; /etc/nd/keybroker layout). Keybroker unit render: /etc/nd/keybroker/{anchors.pem,provider.key}, user nd — waiting HOSTING-5 argv.
- LANDED 6bfd534: OPS-P1 BUILT — carryPlants 13 rows ALL PASS (export reads only/over-existing; import no-digest/wrong/flipped/stamp, no Store file; keeps height + KERNEL origin; lookup committed + control; old-origin not admitted; new-origin via createAs admitted; two imports two worlds); RUNBOOK §6 the carry procedure; OPS-1/OPS-P1 BUILT. Open: keybroker unit render (wait HOSTING-5 argv).
- HOST is now HOST-9 (aa03e59965e1f9ec4), building HOST-33 (fixed 80-byte MAC-per-position index entries; base names indexCount; flag day). Expect: layout change → re-render STORE.md (HOST may do it under pre-agreement), maybe a new Status arm, and my corrupt-history plant moving to check + a page read. Wait for HOST-9.
- keybroker argv (0eb0803): KEYS ANCHORS SOCKDIR PIDS UPSTREAM STORE OPERATOR RESIDENTS DECIDER. Planned unit: User=nd, ExecStartPre emit-anchors --check installed anchors, RuntimeDirectory=nd-keybroker, EnvironmentFile /etc/nd/keybroker/keybroker.env, RestrictAddressFamilies. BLOCKED: keybroker exits 1 for fatal+transient alike → asked HOSTING-5 for a Lean BrokerExit table (classes, disjoint codes, emitted) before rendering.
- LANDED 11a9c97: nd-keybroker.service rendered (Broker in Ops.Units; prevent from HOSTING-16 tables; ExecStartPre emit-anchors --check; RuntimeDirectory nd-keybroker{,/sock}); EXITS.md broker tables; theorems mem_brokerPrevent_*, brokerPrevent_split; OPS-8; RUNBOOK §2a install. Rendered not run. Open: HOSTING stage 3 socket access; HOST-9 HOST-33.

## OPS-3 — HANDOFF from OPS-2 (2026-10-17). Start here; the ## OPS-2 lines above are the record.

### State on main (all pushed; OPS commits by OPS-2)
c835c6d units+EXITS.md+RUNBOOK · 4ae6608 live/sealed/replay plants · fd1d4b2 --exec HOST · e31b4ee deploy/live
harness · df033f2 origin plants · 1d326dd run 4 · add00d8 index.log plants + STORE.md · 973dc44 indexMoved ·
f77c564 TLS anchors (deploy/anchors crate, emit-anchors, cargo: generated row) · 60a12e5 RUNBOOK §2a custody ·
6bfd534 carry plants (OPS-P1 BUILT) · 11a9c97 keybroker unit. decisions/ops.md OPS-0..8; proposals/ops.md OPS-P1 BUILT.
store-plants ~50 rows ALL PASS (hbox). emit-units renders deploy/units/{linux/*.service, EXITS.md, STORE.md}.

### How to work (hbox only)
worktree /tank/dregg-build/nanodregg/wt/ops; `git checkout --detach main`; edit by writing files on the Mac and scp
(apostrophes break ssh heredocs); build `swarm-build lake build <targets>`; plants:
`swarm-build .lake/build/bin/store-plants .lake/build/bin/host <fresh dir under logs/>`; re-render:
`.lake/build/bin/emit-units deploy/units`; commit `scripts/commit -F msgfile PATHS` (needs SIZE: lines when a size row
rises; --cross-layer for others' paths). Rust: CARGO_TARGET_DIR=/tank/dregg-build/nanodregg/logs/ops2-cargo-target.

### Standing couplings (pre-agreed, others do it in their commits)
- HOST/HOSTING adding a Status / BrokerExit end: add its arm (hostAction / keybrokerAction / deciderAction /
  supervisorAction) in Ops/Units.lean cross-layer + `emit-units deploy/units`.
- HOST changing Host.Store.layout/backupOrder: re-render (STORE.md is checked).
- deploy/tls/anchors.pem: `cargo:emit-anchors` row; a webpki-root-certs bump = re-emit in the same commit.

### OPEN — pick up in this order
1. HOST-33 (HOST-9, aa03e59965e1f9ec4: fixed 80-byte MAC-per-position index entries, base names indexCount, flag day).
   AGREED by OPS-2 (HOST-9 re-emits STORE.md/EXITS.md in its commit; no Status change; sentences OK). After it
   lands: NEW row owed — flip a byte in a MIDDLE 80-byte entry of the sealed Store's index.log: `serve` opens
   (asserted), `host check` → indexCorrupt 46 `entry K`, a `log` page over entry K → badIndex 34 (HOST-9 sends
   the `log` payload shape at landing). Watch index-moved-restart-truncates (1-byte partial entry must truncate).
   When it lands: re-render STORE.md if HOST-9 didn't; the corrupt-history plant moves to `check` plus a page
   read (HOST-9 will say exactly); re-run store-plants (orphan-index-page-*, copy-index-before-base, index-moved
   rows depend on the index format: expect to adapt their byte assertions).
2. keybroker under systemd on burst5-a: ONE short window AFTER INTEGRATOR-6 (a55ad25cb5ddaeebc) reports minidregg
   batch 3 landed. Ask INTEGRATOR-6 for the window AND ask ROOT before reinstalling. Reinstall:
   `sudo install -D -o root -g root -m 0755 /usr/bin/bwrap /usr/local/libexec/nd-bwrap` (+ links, teardown list
   BURST5-UP-LOG item 7; record again). nd-keybroker is a SYSTEM unit (User=nd) in the deployed render; for the
   harness render a user-unit variant under /srv/scratch (extend emit-units --live with a Broker under ROOT, as
   liveNodes does for host) — never install into /etc on burst5 unless ROOT says. Questions: does it start,
   ExecStartPre refuse a hand-edited anchors copy, a custody refusal (e.g. key file mode 0644 → 84) stop it,
   SIGKILL of the decider → 102 restarted. Needs a hosting-broker exe and a Store; upstream can be unreachable
   (the row is the unit, not the call). Report by name; teardown after.
3. HOSTING stage 3 (HOSTING-6, spawned from HOSTING-5's handoff): who may connect to the 0600 resident sockets
   (/run/nd-keybroker/sock) and where SOCKDIR sits; re-render nd-keybroker.service when it says.
4. Known untested: NoNewPrivileges + nd-bwrap measured OK on hbox (restriction on) by setpriv, not under systemd.

### Scratch (OPS-2's, deletable by its successor)
Mac: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/ops2/
(live/ harness sources, carry/DRAFT.md done). hbox: logs/ops2-* (plant dirs, build logs, msg files, cargo target).
burst5: /srv/scratch/ops2-live (run1-4 data; goes with the box). No process of OPS-2's is running anywhere.

## OPS-3 (a successor's record; spawned 2026-10-18 after HOST-33 ff60a08)
- Scratch: Mac .../scratchpad/ops3/ (main/ = a read-only `git archive main` copy, wt/ = edit staging, scp'd to hbox wt/ops);
  hbox logs/ops3-* (build logs, plant dirs ops3-plants1, ops3-tooth-plants, msg files, patches).
- LANDED df425e4 `ops:` HOST-33 follow-up: 4 rows (index-middle-entry-is-counted-not-last, -log-page-intact-control,
  -flip-opens-page-badIndex, -flip-check-indexCorrupt-names-entry), Founder.logFrame (founder 0's signed read envelope),
  orphan-index-page-* renamed orphan-index-entries-*, STORE.md wording, badIndex sentence (exit only of check --anchor),
  RUNBOOK §3, OPS-9. Tooth measured (Entry.read tag compare removed → both flip rows FAIL, page served). 54 rows ALL PASS.
  EXITS.md/STORE.md otherwise byte-identical to main's render (verified). cv 01a14ac9-a38a: a scheduled `host check` timer.
- HOSTING-6 landed 45b1394 (keybroker PEER, SOCKDIR /run/nd-broker, sockDir 105 arm, RuntimeDirectory nd-keybroker only).
  broker test builds keybroker argv from the rendered ExecStart word by word: renaming a rendered literal needs
  launcher/tests/broker.rs's argv() map (HOSTING's) — tell HOSTING-6 or carry with agreement.
- HOST is now HOST-10 (a466e00c707f4b7be): follower socket path shape + any new Status (missing index.log) go there.
- ROOT RULED (B) for the nd-hosted follower: trusted side initiates; host.sock stays nd-only; follower socket in a
  setgid 02710 nd-hosted:nd dir, 0660 under nd-supervise --group GID (CLIENT-3 LANDED 77fde4e: numeric GID, before `--`,
  once; refusals sharedDirRefused:<..> / groupMismatch; never creates dirs); driver = client `nd` as nd (unit nd-follow-drive).
  GID = ND_GID in the env file (getent group nd). HOST-10's path: /run/nd-follow/<label>/follow.sock (I proposed flat).
- LANDED f1a1327 `ops!:` sysusers nd.conf + tmpfiles nd-broker.conf (hostedIsKeyHolder refused), writer RuntimeDirectory=nd,
  Node.runtime/Node.sock by construction, runtimeOnUserUnit, ofNode_ok refactor, RUNBOOK §2/§2a, OPS-10 (records the ruling).
- HOST-10 HOST-35 (`missing` 20 replaces noBase/badKey 0): AGREED, HOST-10 carries arm+plants; I owe RUNBOOK §5 line
  "a Store file reported `missing` is never re-created by hand" after it lands.
- Asked HOSTING-6 for a Lean grain-launch exit table (exits 1 for all but usage) before the grain-launch unit.
- LANDED 0739bfa `ops:` nd-hosted-follow@.service (template, User=nd-hosted, --group ${ND_GID}, socket FLAT
  /run/nd-follow/%i.sock agreed HOST-10+CLIENT-3, store /srv/nd-hosted/worlds/%i/store, env /etc/nd/hosted/%i.env),
  tmpfiles nd-follow.conf, Node.template/group + ofNode_group, deploy/live/follow-argv.py (hbox /tank: 64 sharedDirRefused
  Dir — grammar ok), RUNBOOK §2b, OPS-11.
- WAITING: HOSTING-19 (LaunchExit/ControllerExit tables; grain-launch argv ROOT BROKER LABEL PIDS CONTROLLER [ARG]) →
  render nd-grain-launch@.service + EXITS arms. PROTOCOL-7 `sync` verb (Protocol.CommandExit ok0 done/refused1 fatal/
  uncertain2 restart/absent3 done/behind4 restart) + CLIENT-3 observer record (`nd --init-observer`, ws/observer;
  ND_FOLLOW_SOCK/ND_HOST_SOCK landed 32d9352) → render nd-follow-drive@ timer+oneshot as nd (ND_WORKSPACE=observer ws,
  key under /etc/nd/follow/<label>/). INTEGRATOR-6 window for burst5 (asked).
- LANDED 2b4f3bb `ops:` nd-grain-launch@.service (User=nd-hosted, RuntimeDirectory nd-grain-launch/%i, prevent =
  ControllerExit+LaunchExit fatal from 8be4026, Wants/After follower), controllerAction/launchAction, Launcher.check_follower,
  deploy/live/unit-argv.py (general; follow-argv.py deleted): grain-launch → controller store 109 passed through. OPS-12.
- HOSTING is HOSTING-7 (a8d9d17a1910bbe3b). Remaining: nd-follow-drive timer (PROTOCOL-7 sync + CLIENT-3 observer);
  burst5 run (INTEGRATOR-6 window; ROOT before nd-bwrap); RUNBOOK §5 `missing` line after HOST-35; liveBroker render for burst5.
- burst5 plan recorded in BURST5-UP-LOG §8 (PLANNED). Bundle hbox logs/ops3-src (b598ffc). Run: scp bundle to /srv/scratch/ops3-live/src; bash src/broker.sh /srv/scratch/ops3-live/src /srv/scratch/ops3-live/run1
- LANDED b598ffc (liveBroker + deploy/live/broker.sh; bundle hbox logs/ops3-src) and 17b2015 (nd-follow-drive@:
  nd sync as nd, Restart=always RestartSec=40, prevent CommandExit fatal (1), Driver.check_trusted, sync_loop_under_start_limit;
  unit-argv passes Environment=; nd exits 52 on missing follow.sock; RUNBOOK §2b driver + §5 `missing` line (HOST-35 e285406); OPS-13).
- ROOT YES for burst5 (nd-bwrap + nd-ops-live-keybroker link; follower+grain-launch covered too, same undo shape), ONLY in
  INTEGRATOR-6's window. Still waiting INTEGRATOR-6. Rebuild the bundle's emit-units/host from current main before the run
  (HOST-35 changed host).
- LANDED bf1839b: liveHostedFollower/liveLauncher + broker.sh rows L/M/N. Bundle REBUILT at bf1839b: hbox logs/ops3-src (32 MB,
  COMMIT file). Preflight on hbox outside systemd (~/.cache/nd-t/ops3-kb2, ops3-h1, ops3-drive1: mine, deletable): keybroker
  socket 0660 + decider.pid; follower socket 660 gid; grain-launch runs; instance x → 109 `store missing key`.

### BURST5 RUN — exact steps when INTEGRATOR-6 opens the window (ROOT YES given; BURST5-UP-LOG §8 holds cmds + undo)
  B5='ssh -F ~/.ssh/burst5-20261016.conf burst5-a'
  1. $B5 'mkdir -p /srv/scratch/ops3-live && chmod 0755 /srv/scratch/ops3-live'; copy hbox logs/ops3-src → burst5
     /srv/scratch/ops3-live/src (hbox→Mac→burst5 scp of the 32 MB bundle; Mac /tmp nothing: use scratchpad ops3/).
  2. $B5 'sudo install -D -o root -g root -m 0755 /usr/bin/bwrap /usr/local/libexec/nd-bwrap'  (record time in §8)
  3. $B5 'bash /srv/scratch/ops3-live/src/broker.sh /srv/scratch/ops3-live/src /srv/scratch/ops3-live/run1' (≤ ~5 min)
  4. UNDO (§8) yourself, record time; report the 5 answers + L/M/N by name to ROOT, plus any unpredicted exit.
  5. Append the run to deploy/live/README.md (RAN) and commit.
- BURST5 RUN DONE (window 18:04–18:07:40Z, undone, INTEGRATOR-6 + ROOT told). run1 FAIL 2 (keybroker RestrictAddressFamilies lacked
  AF_NETLINK → bwrap loopback fail → `deciderEnded 1` unnamed, restart-loop); run2 ALL PASS 8 rows. LANDED 774b090: AF_NETLINK,
  Launcher.driver (grain-launch Wants/After nd-follow-drive@), RUNBOOK §2/2a/2b (RAN, observer enrolment 3e09d67, members dir),
  broker.sh journal --since, OPS-14. Asked HOSTING-7 (a8d9d17a1910bbe3b): name the decider mechanism failure (not deciderEnded 1);
  a by-name refusal at start for a missing worlds/<l>/members (LaunchExit arm; I carry no sentence until told).
- OPEN for successor: system-unit run (User=, RuntimeDirectory, two uids) needs a box with root + two users (none yet);
  driver against a live writer; HOSTING-7 answers; cv 01a14ac9 (scheduled host check). Scratch: hbox logs/ops3-*, ~/.cache/nd-t/ops3-*,
  Mac scratchpad ops3/, burst5 /srv/scratch/ops3-live (goes with the box). No process of OPS-3's running anywhere.
- HOSTING-7 shapes AGREED (sentences sent): deciderMechanism (KeybrokerExit fatal), controllerMechanism + layoutMissing (LaunchExit fatal); HOSTING-7 carries arms + re-render cross-layer, sends diff first. Order: grain row → (1) → (2). OPS reads the diff.
- YES given to HOSTING-7's hosting7-mech.patch (deciderMechanism 79, controllerMechanism 67, layoutMissing 68; my sentences verbatim).
  OWED after it lands (HOSTING-7 sends sha): broker.sh row N — make hosted/worlds/x/members so N still measures controller store 109;
  new row O layout-missing-stops (remove w/members → 68). Not run on any box until a new window.
- HOST is now HOST-11 (a2f74b4272ca9175d): journal-port Status/layout changes come from there. burst5 awaits Ember's teardown word.
- FYI (CLIENT-3, unlanded, waits a size ceiling): nd-supervise gains --peer UID (with --group) and --connect; nd --stdio WORKSPACE FOLLOW_SOCK HOST_SOCK serves a resident. When it lands, consider --peer on nd-hosted-follow@ (peer = nd's uid via ND_PEER-style env) — ask CLIENT then.
- HOSTING-7 LANDED a487504 (deciderMechanism 79, controllerMechanism 67, layoutMissing 68; ≥128 → *Signaled restart).
- LANDED a7cdda8: broker.sh row N gets x/members; row O layout-missing-stops (68). Preflight hbox at a487504: 68 / 109.
- DEFECT OF MINE fixed forward 013f35d: 774b090 had replaced deploy/live/README.md with only its new section (a staging copy
  named by basename collided: README.md.cur vs README.live.md.cur). Restored from bf1839b + appended. LESSON: stage fetched
  files under their full repo path, and check `git diff --stat` before every commit for unexpected deletions.

## OPS-4 (successor of OPS-3; spawned 2026-10-18 07:50Z for the TOFU residue CLIENT-5 enumerated)
- ROOT RULED (on my ask): no join unit, no kept custody file for the hosted follower. `host join` takes the key as HEX, and a
  rendered oneshot would run `host` bare, which Units' law forbids. The operator is the sponsor; the hosted chain rule is the
  operator's shell. `nd --join-store` (CLIENT) is NOT taken.
- LANDED d1c3fbb `ops:` OPS-15.
  - RUNBOOK §2 (member `nd --join` steps 1-5, refusals by name, the founder-nonce residual + mitigation);
    §2b (`sudo -u nd-hosted host join STORE INVITATION KEY_HEX`, re-follow = fresh `nd invite`); §6.7 (carry rejoin is
    trust on first use by design).
  - Ops.Founder.input/invitation (test invitation from the RFC 8032 vectors).
  - store-plants joinPlants: 6 rows; 66 ALL PASS.
  - Teeth measured: accept's checks cut → forged/notSponsor/follow-over red; nonce flip → honest red; exists cut → again red.
  - live-calls writes calls/invitation and calls/sponsor.key. broker.sh row L joins; row P (forged join → follower missing 20,
    NRestarts=0) is preflighted outside systemd (~/.cache/nd-t/ops4-pre1 on hbox, mine), NOT run under systemd.
- Lesson (again): the worktree's .lake/build/bin/{host,emit-units} are stale until rebuilt. My first plants run and first
  `emit-units --check` read old binaries. The first tooth build failed (linter) and its plants ran the OLD binary: check
  "Build completed" before reading any verdict.
- OPEN: HOST-43 seal act (HOST-12 proposes after the rows day → STORE.md/RUNBOOK re-render + an operator sentence); the rows day
  (KERNEL-17: a Status? units unchanged otherwise); cv 01a14df6-0647 (CLIENT's: the follower policy from a Lean plan, noted, not
  OPS's to build); row P under systemd in a box window; cv 01a14ac9 (scheduled host check).
- Scratch: Mac .../a8357d63-.../scratchpad/ops4/; hbox logs/ops4-* (plant dirs, tooth logs, msgs). No process of OPS-4's is running.
- PROTOCOL-10 (afa6834d506757f31) asked a yes for Ops/Plants.lean usePlants (`use=U` in `host check` STATUS, cv 01a14de7-225e).
  YES, conditional: (1) use-one-member is vacuous on `intact` (4 creates, no use): it needs a self-use call on a copy, with
  the measured mutation (drop the distinct-member condition), or a rename to a control; (2) rebase over d1c3fbb, then
  re-run store-plants; (3) docstring: callsAt is in process, not through the exe. OWED by OPS after they land: RUNBOOK §3's
  STATUS line gets `use=U` + their sentence. THE BAR is PERF's (told them to ask PERF).
- HOST-12 (a28e294ce7b0dcec6) advance notice HOST-43: `host seal STORE` (stopped writer, flock → locked if live, prints
  `sealed steps=S chain=C digest=D`; NO new Status; layout unchanged). AGREED. RUNBOOK is mine: HOST-12 sends the
  paragraph + sha, I land it (§2 after the invite steps; §4 if needed). ASKED them: how the sealed pin reaches `nd invite`
  (invite pins the sponsor's follow World at its current height, so a turn between the seal and the invite → baseMoved);
  plants: seal on a live writer → locked, base_steps=S + digest match, a second seal at the same height. Who carries the
  plants: theirs to say.
- HOST-12 answered: the invite must pin the writer's NEWEST BASE (it stays newest until the next cadence seal, ≥1 MiB), not
  the sponsor's tip. That is PROTOCOL's fix in `nd invite`/Machine.start (pin from the `read` reply header, or from
  `host seal`'s printed steps:digest); HOST-12 told PROTOCOL-10. The RUNBOOK paragraph comes only after that settles
  (§4 = a pointer only, openWith_backup). OPS CARRIES three store-plants rows after `host seal` is on main:
  seal-live-writer-locked (16, bytes unchanged), seal-base-is-the-pin (base_steps=S, digest = Keys.worldDigest),
  seal-again-idempotent (0, same line, base.world bytes+mtime unchanged), each with a measured tooth.
- PROTOCOL-10 landed db0b43c (use=U; use-zero-on-creates-only control, use-self-use-zero with measured tooth; store-plants 69 ALL PASS).
  LANDED 6558c56 `ops:` RUNBOOK §3: the STATUS line as Host.Check prints it (it had drifted: no steps=, base_height for
  base_steps) + `use=U` sentence. Remaining queue: HOST-43 (after PROTOCOL's invite-pin fix) → 3 seal plants + paragraph; rows day.
- PROTOCOL-10 retired; the invite base-pin fix is PROTOCOL-11's queue item 3 (PROTOCOL-LOG `### PROTOCOL-10 HANDOFF → PROTOCOL-11`):
  follow records its World digest at each writer-stated base step count; `invite` pins the newest base it verified, refused
  `baseMismatch` / `noBase`. Lands with the thin-row re-cut AFTER HOST-12's sealNow. OWED when it lands: RUNBOOK §2 refusal list
  gains baseMismatch/noBase with what the sponsor does (seal, catch up, invite again), plus HOST-12's seal paragraph and the
  3 seal plants. PROTOCOL-11 signals.
- QUEUE EMPTY for now (everything open waits on HOST-12 sealNow → PROTOCOL-11 invite pin, and the rows day). OPS-4 stopping
  at ~200K; a successor (or OPS-4 resumed) starts from this section.
- PROTOCOL-11 (a0b1899e3383e7392) PROTOCOL-46 on 42c261b: CommandExit drops absent 50 (never reused), adds open 54 / hostContradicted 55
  (both restart). YES to its commandAction arms (their wording), condition: EXITS.md re-emitted in the same commit (it was
  not in the diff). No RUNBOOK change (§2b lists 1/2/51/52). Reminded them: baseMismatch/noBase sentences owed to §2 at
  the base-pin invite.
- KERNEL-18 (add6007f95cfdde3c, successor of KERNEL-17) notice: the trie day re-geneses every Store (every root changes); OPS acts
  only if a Status or Host.Store.layout moves. store-plants computes its anchors/origins in process, so a root change needs no
  OPS edit (the standing stage will say if a row's assumption breaks).
- LANDED c80db80 `ops:` HOST-43 seal plants (seal-live-writer-locked, seal-base-is-the-pin, seal-again-idempotent; 72 ALL PASS at
  6df6a3f; teeth: tryLock ignored / chain-as-digest / sealNow short-circuit removed → each row red by name).
  LESSON (Lean): a pipe Handle no longer used is freed and CLOSES the child's stdin. A live-writer plant must use `input`
  after the act under test, and assert the writer is alive (IO.hasFinished) before and after it. My first draft read
  a host "defect" that was my plant; a hand reproduction refuted it before anything was reported.
- Remaining: RUNBOOK seal step + baseMismatch/noBase sentences when PROTOCOL-11's base-pin invite lands (HOST-12 sends the
  paragraph); row P under systemd in a box window; rows/trie day (KERNEL-18) only if a Status/layout moves.
- LANDED 2d4c38d `ops:` OPS-16 (GATES-5 fail-open, ROOT): deploy/live/journal.sh sourced by harness.sh + broker.sh; every judged
  journal read is `jr` (--after-cursor of the run-start cursor, report/journal-cursor); journal_mark plants it (stale marker
  hidden, fresh seen, else `journal-reads-only-this-run FAIL` exit 2), tooth measured on hbox (unbounded jr → refused);
  harness row B judges its feed (status=0 ×1, height=5). The bundle needs journal.sh. Not run under systemd since.
- GATES-5 (a7d2da80c806974b6) GATES-15 landing B: `store-plants … --harness-control` appends an always-FAIL plant on the judge
  path; runs.py reads it first. YES (cross-layer, ROOT-ruled), notes: usage string; the control covers judge/aggregation
  only, not the ~2/3 of rows printed by their own say/println (those rest on each row's measured tooth).
- LANDED 5a71be7 `ops:` RUNBOOK §2 step 1: the invitation pins the newest base the sponsor's follow verified (PROTOCOL-47
  5f9edc2, PROTOCOL-12 ab85c36fd01b6c4eb); stop/`host seal`/start before a thin invite; noBase (seal again) / baseMismatch (do not
  invite through this writer); upgrade writer+followers together (log-reply flag day, badResult); §4 pointer.
- HOST-12's paragraph arrived after; corrected it at source: a newer base not crossed is noBase (Machine 451-461), not
  baseMismatch. OWED when HOST-12 lands positionUnfit (56, fatal; arm + re-render theirs, sentence agreed): RUNBOOK §2 line
  "host seal's refusals = open's + seal's, fatal, keep the Store, report to HOST" + "the joiner's `nd adopt` prints the same
  steps=/digest=".

## OPS-5 (successor of OPS-4; 2026-10-18)
- LANDED bada768 `ops:` OPS-17: RUNBOOK §2 `host seal` paragraph completed (refusals = serve's names + `locked` + `positionUnfit` 56; the joiner's `nd adopt` prints `adopted STEPS DIGEST`, must equal the `sealed` line's steps=/digest=). noBase/baseMismatch + seal step were already in 5a71be7 (checked against PROTOCOL-47). EXITS.md (deploy/units/EXITS.md) already had row 56 from HOST-46's re-render; emit-units --check green. Nothing re-renders.
- Standing, nothing asked yet: HOSTING-8 (nd-keybroker ${ND_RESIDENTS} removal, per-resident socket), HOST-13 (page IO Status sentence), PERF-1 (RUNBOOK §7 THE BAR), GATES-6 (--harness-control: yes, two notes). Row L/O/P systemd runs + journal-cursor: wait on a box window.
- Scratch: hbox ~/ops5/ (commit msg + log). No process of OPS-5's running.
- LANDED b422d7f `ops:` EXITS row 64 refusedAtLaunch gains the open-file refusal (CLIENT-28 cf79591); only that row re-renders.
- LESSON: `emit-units --check` WITHOUT a DIR treats `--check` as the DIR and writes ./--check/ (usage text only mentions it). The real form is `emit-units --check deploy/units`. My OPS-17 "check green" was that vacuous call; commit's own generated:deploy/units gate was the real check (ok). Removed my ./--check/ dir.
- OWED: HOSTING-25 (aa823e7641b7b6082) after it commits: RUNBOOK §2b argv + nd-member.conf install line, deploy/live/broker.sh member dir, later the member unit.
- LANDED 2d24d67 `ops:` HOSTING-25 operator side: Ops.Units.Resident -> deploy/units/linux/nd-member@.service (User=nd; ExecStartPre install -d -m 2710 /run/nd-member/%i; nd-supervise --group ${ND_GID} --peer ${ND_PEER} --hide /etc/nd --hide /home --write ${ND_MEMBER_WS} --exec nd --connect host --connect follow -- nd --stdio); EnvironmentFile /etc/nd/hosted/member-%i.env (ND_GID ND_PEER ND_MEMBER_WS ND_FOLLOW_SOCK ND_HOST_SOCK). RUNBOOK §2b: nd-member.conf install, grain-launch argv with MEMBER, member-socket paragraph (host.sock/follow sock alone in their dirs, 69 foreignPath). broker.sh makes $R/member 2710. NOT run under systemd; live harness renders no member unit; the birth->start ordering is HOSTING-26-open (RUNBOOK says: operator starts nd-member@ID first). Commit needed `SIZE:` lines for Ops lines (+68).
- LANDED f466780 `ops:` RUNBOOK §3: pageIo (HOST-48 01396b7) page refusal, writer serves on, STATUS page line, operator sentence. No re-render.
- LANDED c32a36a `ops:` RUNBOOK §2a keybroker.env = ND_OPERATOR+ND_PEER; resident socket at birth/removal, residentsPastBound, notResident, pathMissing race (HOSTING-26 43ab42a); broker.sh stops writing ND_RESIDENTS. KNOWN RED OWED: broker.sh rows G/I/K use broker/01/broker.sock; the live Store (live-calls genesis) holds no resident grain, so keybroker binds nothing -> G fails. Fix = live-calls creates a resident grain (name = dirOf hex, not 01) and broker.sh derives $sock from it; needs a box window to run. nd-member@ decision is HOSTING-9 (HOSTING-LOG FOR HOSTING-9 item 3).
- LANDED 5771c74 `ops:` live keybroker harness gets a resident grain (ROOT: a red row is not left red). live-calls writes grain-000.bin (install Grain.lifecycle?) + grain-001.bin (create resident, phase installed) + grain.dir (Controller.dirOf hex); Founder.callAs generalises createAs; feed.py takes a PREFIX; broker.sh links nd-ops-live-serve, feeds the grain calls (height=2 checked), derives $sock from grain.dir, row G also asserts SOCKDIR lists only that name. Row G's 660 was ALREADY stale since HOSTING-21 113537f (PEER==own uid binds 0600): now 600.
  Preflight by hand on hbox (~/ops5/pre1, pre1.sh/pre2.sh): nd-supervise writer admitted both calls (status=0 x2), host check height=2; keybroker by the rendered argv: broker/<dirOf>/ 2710, socket 600, SOCKDIR lists only that name, decider.pid present, stopped by PID file. NOT run under systemd: rows G..P await a box window.
  LESSONS: (1) a hand-copied emit-units/host from a stale .lake renders the OLD unit (still had ${ND_RESIDENTS}) and writes a Store the new hosting-broker cannot read (`store record`); rebuild before preflight. (2) keybroker custody (keyFileDir) refuses a group-writable parent: chmod 0755 the preflight dir. (3) Install the allowed validUntil: i must stay < windowMax/2 (1000 refused overBound window).
- LANDED ff530a7 `ops:` RUNBOOK §8 measuring THE BAR (PERF-1 text, hbox logs/perf1-runbook-bar.md at 5f7c58d); bench-worstcut paragraph PENDING (PERF) until its hash; fds bullet tied to EXITS 64 / CLIENT-28. OWED: HOSTING-9 pins/anchors landing -> broker.sh $R/etc/pins + RUNBOOK §2a (pins install, rotation recipe, pinMismatch 23, narrowed anchors, reply shape).
- LANDED b0d33d2 `ops:` RUNBOOK §8 worst-cut RAN (bench-worstcut c392f51) + bar.sh PID files in $HOME/.nd-bar/run.XXXXXX.
- LANDED ddca7c6 `ops:` RUNBOOK §2a pins/anchors 7of121/reply shape (HOSTING-28/29 9df02da); broker.sh installs empty pins. Preflight by hand: keybroker binds with pins arg; missing pins -> 146. No harness row for pinMismatch (needs a TLS upstream; HOSTING-9 planted it). OWED: CLIENT-8 nd-members@WORLD.service render + delete nd-member@; row set under systemd awaits a box window.
- LANDED eaa591a `ops:` RUNBOOK §8: worst cut = 3 tail shapes (PERF-6 2d2189e), bar.sh stale/foreign binaries + dirty-tree (PERF-7 ce23f2e), THE BAR v2 (PERF-2) PENDING/unrun (open: resident round = HOSTING-27; drop_caches root on each machine).
- LANDED 46ae495 `ops:` RUNBOOK §8 v2: drop_caches = Ember act, then says go (ROOT via PERF-2). Resident round still open (HOSTING-10).
- LANDED d5a8996 `ops:` RUNBOOK §8 v2 resident round (HOSTING-10 via PERF-2); PENDING HOSTING-27 hash.
- LANDED 07f31d6 `ops:` RUNBOOK §8 v2: resident landed 0e4d57f; PENDING = box + friends + Ember drop_caches. Agreed (yes) KERNEL-21 pinOf live->entry in Founder.lean:60/Plants.lean:670.
- LANDED f68f968 `ops:` nd-members@.service (HOSTING-30/CLIENT-29 ecb02bf) replaces nd-member@ (deleted) + env file; EXITS nd-members table 150-159; tmpfiles nd-member-follow.conf (0700 nd); RUNBOOK §2b provisioning. EnvironmentFile = keybroker.env (ND_OPERATOR, ND_PEER). TasksMax 270338 from residentsMax/connectionsMax. OPEN filed: decider T0 literal 0/SLOTS 1 until hosting-residents; MEMBERS under nd-hosted 0700 tree vs nd-owned chain (layout conflict); RestrictAddressFamilies/TasksMax unmeasured. Hand check: rendered argv parses -> 151 at missing MEMBER. Live harness has no members row. Not run under systemd.
- ROOT RULING (layout, via coordinator): MEMBERS + FOLLOW roots leave the hosted tree -> /srv/nd-members/<LABEL>/{members,follow} 0700 nd; MEMBER socket dir stays group-traversable; plan entries are HOSTING-11 (HOSTING-32); I re-render nd-members@, tmpfiles, RUNBOOK §2b + broker.sh from it AFTER the LANG-58 commit; note T0 literal removed by CLIENT-9 hosting-residents STORE; unit comment: RestrictAddressFamilies/TasksMax unmeasured until a box window. Asked HOSTING-11 for paths/plan entries/hash; nothing landed meanwhile.
- HOSTING-11 preview of HOSTING-32 (hash to follow): MEMBERS=/srv/nd-members/<L>/members, STATE=/srv/nd-members/<L>/follow/<dirOf>/{store,follow} (nd 0700, chain /srv/nd-members + /<L> nd 0700); FOLLOW sockets stay /run/nd-member-follow/<dirOf>/follow.sock; nd-members argv gains STATE: MEMBER MEMBERS STATE FOLLOW ...; plans hide only worlds/<l>/store, layoutHidden=[store], membersDir deleted, broker.sh hosted/worlds/w/members can go. Units must render from new Lean root defs (HOSTING-11 names them), not literals. Order: LANG-58+HOSTING-31, HOSTING-32, then my re-render.
- AGREED (a) to HOSTING-11: HOSTING-32 carries the minimal Ops/Units.lean change (membersAction .stateRoot 160, Members.state, roots rendered from Lean defs, tmpfiles for /srv/nd-members, re-emit) cross-layer; mine after its hash: RUNBOOK §2b, broker.sh members dir, hand preflight, unit comments (unmeasured AF/TasksMax; T0 literal until hosting-residents).
- LANDED aa50bf6 `ops:` RUNBOOK §8 v2 round under the bell queue (96179fb, HOSTING-11/LANG-18 via PERF-2).
- LANDED 0debb31 `ops:` RUNBOOK §2b + broker.sh + live README for HOSTING-32 (9e41ba0): /srv/nd-members/L/{members,follow}, STATE/<id>/{store,follow}, 160/161; broker.sh drops worlds/*/members, row O now = instance y without store (layoutMissing 68). Hand preflight: grain-launch y -> 68 .../worlds/y/store; rendered nd-members argv -> 151. Not under systemd. NEXT: HOSTING-33 (hosting-residents) Units line carried by HOSTING-11 (no objection).
- AGREED to HOST-14 (HOST-56 KERNEL-55 budget check): Units.lean status arms allowancePastBound 58 / potentialPastBound 59 cross-layer; conditions: emit-units --check DIR, EXITS rows, collision check, flag-day statement; I owe RUNBOOK §6 sentence if exported Worlds now refuse to import.

## OPS-6 AUDIT (successor of OPS-5; 2026-10-20) of the OPS-path edits made while no OPS lane was live
Read hunk by hunk on hbox main 1e90c0b, each sentence against the code it describes.
- e1e8084 HOSTING-33 (nd-members decider `hosting-residents /srv/nd/store`; Proofs/Units `membersUnit_decider_store`): ACCEPTED. Rendered ExecStart matches Hosting/ResidentsCli. Owed prose CORRECTED: RUNBOOK §2b still said the unit reads ND_OPERATOR (it reads ND_PEER only) and did not list the binaries to install.
- cfdb08d HOST-56 (allowancePastBound 58 / potentialPastBound 59, three RestartPreventExitStatus lists, EXITS rows): ACCEPTED (names/classes match Host/Exit.lean; check order allowance then potential matches Host/Cli budgetFault). CORRECTED the owed prose: RUNBOOK §6 step 4 (import) and §2b (join) now list 58/59 with what to do.
- 359e9e8 HOST-57 (decisions only): no OPS edit was made, one was owed. CORRECTED: `worldTooLarge` (11) still said "HOST-14 design limit"; since HOST-57 it is unreachable by admitted turns, so its own arm says defect (EXITS row 11 re-rendered; no literal copy of the bound in the sentence).
- 3f6d883 PROTOCOL-54/55 (decisions only): ACCEPTED, no operator sentence moves.
- c0cd535 CLIENT-30: 73 fds ACCEPTED (client/src/mux.rs fds_max = 8 + CONNECTIONS_MAX + 1 = 73, the doc names the SIGTERM pair). memberStopping/memberStopForced are named in the membersAction docstring only; ACCEPTED as docstring (neither is an exit), CORRECTED by giving them their operator sentence in RUNBOOK §2b (stopping = rebirth waits, automatic; forced = SIGKILL past GRACE, report if repeated).
- bfdff2d PERF-10 RUNBOOK §8 resident round (79/120, 96/143, rings[k]): ACCEPTED (matches PERF-10's text). CORRECTED the §8 worst-cut paragraph it left stale (20.374/33.031/33.959, three shapes -> 19.382/32.036/32.938/rows 24.892, four shapes; 7:59, 751 MB) and added the worst-World bench paragraph (HOST-57 bound 91,914,346 B, 5,252,227 hashes, 56.3 s loaded).
- HOST-61 (judge/host wt 5fff199+dirty: beforeLog 60, Units sentence + 3 lists + EXITS row): ACCEPTED (Host/Exit.lean code 60 fatal; the sentence names where it is read, `host check --anchor`, and the writer's page refusal). Note: the `log` page request before the log start is the same refusal.
- CLIENT-31 (client wt, staged: memberRoot/followRoot sun_path length case): ACCEPTED (SOCK_PATH_MAX 107, GRAIN_NAME_MAX 64 in broker_generated.rs; the stderr line prints `socket path N bytes > 107`). Note to CLIENT, not a block: followRoot's "fix the tmpfiles line" is also the length cure (the root is a unit literal).
- RUNBOOK §2a PINS recipe vs HOSTING-28 as landed: ACCEPTED (keybroker.rs parse_pins: `HOST HEX` + LF, 64 lowercase hex, no repeat, empty = no pin; exits 140-148 as BrokerExit; no ExecStartPre compare, matches Broker.exec's comment; the openssl SPKI hash is the pinned value). Nothing to change.
- RUNBOOK §2b layout vs HOSTING-32/33/35: MEMBERS /srv/nd-members/L/members, STATE /srv/nd-members/L/follow/<id>, sockets /run/nd-member-follow/<id>/follow.sock all agree with the rendered argv. CORRECTED: it counted "five roots" for a check that compares four (MEMBER, MEMBERS, STATE, FOLLOW); the hosted tree is kept apart by the plans.
- QUESTIONS to ROOT: none.
- PREPARED in /tank/dregg-build/nanodregg/wt/ops (uncommitted, 1e90c0b + diff): Ops/Units.lean (worldTooLarge arm), deploy/units/EXITS.md (row 11 re-rendered; `emit-units --check deploy/units` green; Ops.Proofs.Units builds), deploy/RUNBOOK.md, decisions/ops.md OPS-18. To land as one `ops:` commit when ROOT sends GATES-20a's hash. Scratch: hbox ~/ops6-*.
- Remaining OPS owes: systemd runs rows G-P (a box window: Ember's); §8 v2 PENDING items = the box, the friends' machines, Ember's drop_caches (stated as Ember's acts, unchanged); live harness still renders no nd-members unit.
- LANDED 224e9fe `ops:` OPS-18 (the audit corrections above; GATES-20a hold lifted at 6527d9f; first judge RED on a missing SIZE: line for Ops lines, fixed in the message; 3 re-bases). HOST-61 landed bd39f78 meanwhile: its beforeLog arm/EXITS row 60 were audited ACCEPTED above.
- 2026-10-21 OPS-6: HOST-19 (aee51d5b605789aa3) announced KERNEL-44 Part 2 checkpoint names (RETAIN --retain N, retainBelowFloor, layout index.<k0>.log/seg.<o>.log, checkpointed/checkpointCorrupt/storeMissing, retained_from=H). OWED after its hash: Units retain field, Status arms + EXITS re-render, RUNBOOK §3/§4/§5, plants anchors. Landed this stretch: 8547e9b (crashLoop sentence, HOSTING-13); agreed Plants.lean edit (HOST-17) and RUNBOOK §8 bench-worstcut split (PERF-5), conditions in their messages.
- 2026-10-21 OPS-6 B8: Latitude tag tag_xG6mROjVd9TX4YB2olzAHVgBJAo (burst5-20261016, created by curl payload latitude-burst5-20261016/create-payload.js; description "burst5: minidregg build box ... review 2026-10-19") was attached to NOTHING (GET /servers = 0 servers; sv_zrPm0dBJ65KOw 404 since 10-18). Deleted with `curl -X DELETE https://api.latitude.sh/tags/ID` (the teardown tool): HTTP 204; the 4 older burst tags remain untouched.
- 2026-10-21 OPS-6 hbox install (ROOT direct, Ember approved the second uid), main ececba1, each printed with rc: `sudo -n install -m 0644 deploy/units/linux/tmpfiles/{nd-broker,nd-follow,nd-member,nd-member-follow,nd-members}.conf /etc/tmpfiles.d/<same>` (rc 0 x5); `sudo -n install -m 0644 .../sysusers/nd.conf /etc/sysusers.d/nd.conf` FAILED rc 1 (/etc/sysusers.d does not exist on hbox: the RUNBOOK §2a recipe lacks -D); redone `sudo -n install -D -m 0644 ...` rc 0; `sudo -n systemd-tmpfiles --create` rc 0 (one unrelated warning, /usr/lib/tmpfiles.d/legacy.conf:13 duplicate /run/lock); `sudo -n systemd-sysusers` rc 0; uids unchanged nd 981, nd-hosted 980; stat: /run/nd-broker and /run/nd-member 2710. Only /etc/tmpfiles.d/nd-*.conf and /etc/sysusers.d/nd.conf (+ its new dir) were written. OWED in my next `ops:`: RUNBOOK §2a `install -D` for the sysusers line + "on hbox the confs are installed; a reboot recreates the dirs".
- Also owed/queued (order): [landing in flight: custody write-down, judge re-basing]; pin (api.anthropic.com SPKI 9fe3851dbd7a61523c284bb1e372e4e238c5b0aefac4ba256af95c0024045eae, leaf valid 2026-09-21..2026-12-20 issuer GTS WE1, 4 fetches agree: 2 hbox + 2 Mac) into Hosting/Pins.lean + RUNBOOK §2a + decisions/ops.md; checkpoint Ops side after HOST-20 lands (they port Plants/Units arms; I do RUNBOOK §3/4/5 + retain Node). UMask 0027 hunk handed to HOSTING-16 (OPS-6 agreed).
