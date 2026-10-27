# What the sprint overlooked (real 2026-10-27, OVERLOOKED lane)

Read-only. Tree read at nanodregg origin/main after `git fetch` (97 commits since 2026-10-26 ~04:00Z). Sources: `git log --since="36 hours ago" --name-only`, FRONTIER-BOARD.md, STALL-WATCH-20261007.md (tail), readers/COLLATION-20261024.md and HOLISTIC-*.md, critiques/CRIT-*.md, `cv task list`, decisions/root.md (ROOT-DOCS obligations), and the files named below. Every claim cites a path. "Not found" means a grep of origin/main returned nothing; it is not proof of absence.

## 1. The map

The sprint touched 567 of the paths in the log; 325 of the 823 files now in the tree were not touched. Per layer, untouched files over files in the tree: Bench 10/14, Census 3/3, Codec 41/59, Host 42/66, Hosting 34/62, Protocol 23/61, Kernel 28/85, Lang 57/160, client 20/42, deploy 16/31, gates 11/32, Emit 7/12, Ops 4/8, launcher 4/22, proposals 7/7, attach 3/3, devtools 3/4, sandbox 2/11, world 2/13, Ledger 1/11. Spec, testground, docs, decisions, scripts: 0 untouched.

The axes worked: CTX, TRUST (including the seed), TYPES, PCC, META, OBS (the meter), AGENT, SPEC, TESTGROUND, QA, SANDBOX, DOCS, RETIRE, RESTORE, and the judge's replacement. Live now: UI-OVERHAUL, PERF-TESTGROUND, SYNTAX-*, CAUSAL, GLM waves, FAERIE-SURFACE, AGENT-5, TESTGROUND-6, CTX-6, TRUST-5. Nothing below is claimed to be in those lanes unless it says so.

Untouched is not the same as overlooked. Most of the 325 files are proofs and sims nothing needed to change. The items below are the places where the sprint changed what a file depends on, or promised something a file has to keep, and the file was not looked at.

## 2. Ranked list

Rank rule: (A) the sprint built on it without looking; (B) a member or operator hits it first; (C) the readers asked and nobody answered. Within a tier, by how soon it bites.

### Tier A: built on without looking

**A1. The re-genesis path (carry / `host export` / `host import`).**
- Exists: `Host/Carry.lean` (last 2026-10-20), `Kernel/World.lean` `Carried` and `Kernel/Receive/Follow.lean` `carryWorld` (10-18/10-20), `deploy/RUNBOOK.md` section 6, `docs/OPERATING.md` Carry row.
- Why now: this is the only upgrade path (CHARTER law 1), and the sprint changed what a World is. The authority is now a genesis input committed in the origin (`domOrigin` v3, KERNEL-69) and lives as one ROM cell in the trie. The window trie gained the tick meter (KERNEL-68). Retirement tombstones exist (KERNEL-70). Every package re-ids (package wire 5 to 10). None of these landings touched `Host/Carry.lean`.
- Facts: `Carried` holds trie, allowance, height, journal, rows. `carryWorld` sets `refusals := .empty`, so window counts and the meter reset on import. `carryOriginOf` hashes roots, allowance, height, journal, the exported origin, name and nonce; it does not take an authority. `host import` has no `--certifier` or `--threshold` (usage in `Host/Cli.lean`). RUNBOOK section 6 does not mention authority, certifiers, the certify key or the meter. `authorityOf_honest_fold` (`Kernel/Proofs/AuthorityOf.lean`) is stated for Worlds an honest fold reaches from a genesis. I did not find a statement about a carried World. So an imported World appears to inherit the old authority cell and cannot change it, and the new origin does not commit to it. This is a reading of the code, not a measured failure.
- First card: state and test what authority an imported World bears, with a row that exports an authority-bearing World, imports it, and runs `host certified` against it.
- Risk: the first real upgrade of a certifying World either silently keeps the old authority or cannot certify.

**A2. THE BAR has not been judged since 2026-10-18, and the charter's headline promise has no passing full run on record.**
- Exists: `gates/bar.tsv`, `scripts/bar.sh`, `Bench/`, `decisions/perf.md`, `deploy/RUNBOOK.md` (v2 section), `attach/`.
- Last touched: the last `run` row is 2026-10-18T12:59Z at de718bf. The only PASS is standing N=60 at b9cd50f. All three N=1000 full runs read UNJUDGED (load). Recorded values from those unjudged runs: write p99 70 to 137 ms; writer cold reopen 63128, 105249 and 110074 ms; follow reopen 106689 to 113911 ms; the limit is 60000 ms for reopen. No v2 (two friends plus hosted Hermes over ssh) row exists in the file.
- Why now: since 10-18 the sprint added the meter leaf, retirement, graded effects, `holds` legs, the authority cell, certified heads and the seed. Each changes bytes per Turn, per base, or per page. `Bench/Count.lean` mentions the meter once; `Bench/WorstCut.lean` was touched only for the authority (8f1e332) and retires (79b1ffe). Nothing checks that `worldBytesMax` (derived from the budget, HOST-57) still covers a World carrying per-member meter leaves.
- First card: one judged full run on a quiet box at current main, recorded, plus a v2 run once Ember drops the caches.
- Risk: the 60 s cold-follow limit in the charter may already be false and nothing is positioned to say so.

**A3. The whole-tree convergence is stale and was red when last run.**
- Exists: `scripts/standing.sh`, `scripts/converge`, `gates/*`.
- Facts (STALL-WATCH 10-27 15:21Z and 15:43Z): CONVERGENCE 176110a RED 3 after 192 minutes at load 15 to 70. Census red: 24 declarations use `native_decide` auxiliary axioms with no allow row, from 87a1eb1 (Spec receipts) and dependents (cv 01a17df3-6a65). Broker and isolation rows fail under load (cv 01a17df3-6a9a). Deadline raised 600 to 1200 s (f95ed6c) because rows took 603 to 645 s on a quiet box. About 20 landings have gone in since.
- Why now: GATES-28 (6faa984) replaced the judge with rule 1, so a landing builds only what it touched. The census, certificate, plants and rows now run only in the periodic report, and that report is the single whole-tree gate. Readers' A2 (gates blind to a definition's body) is the reason this matters.
- First card: a convergence at current tip, with the 24 allow rows decided (allow or remove the `native_decide`) before it runs.
- Risk: reds accumulate unattributed; the report names a landing from 20 commits ago.

**A4. Backup and restore of the state the seed added.**
- Exists: `deploy/units/STORE.md` (generated; last 2026-10-21), `deploy/RUNBOOK.md` sections 4 and 5, `Hosting/BrokerCli.lean`, `Hosting/BrokerWire.lean`.
- Facts: STORE.md lists key, base.world, index, seg files, and nothing else. decisions/root.md (ROOT-DOCS) says "Store documentation must account for the optional certificate sidecar"; STORE.md still has no `base.cert`. The writer's certify key lives in keybroker custody: `KEYS` with `certify` and `certify.next` lines, and `KEYS.certified`, the last head it signed (HOSTING-56, -60). The broker refuses to sign a head below or beside the last it signed. `grep certify deploy/RUNBOOK.md` finds nothing. So restoring a Store to an earlier position while `KEYS.certified` records a later head leaves a writer the broker will not certify; restoring an old `KEYS.certified` beside a newer Store weakens the sign-once guard. Nothing says which to do. Card 01a17c30-be07 and 01a17c30-bde2 (8h): the live-backup theorem models one append-only file and `--retain` rewrites and unlinks; the open theorems are over `openWith` in `Id`, with the deployed `openAt` read off.
- First card: RUNBOOK sections 4 and 5 gain the broker state and `base.cert`, and a plant restores a Store to an earlier step under a later `KEYS.certified`.
- Risk: the first restore on a certifying box ends with a writer that cannot certify, or one that can equivocate.

**A5. The deployed units do not run the seed, and the box is behind.**
- Exists: `Ops/Units.lean` (10-27 10:58), `deploy/units/linux/*.service`, `deploy/testground/`, `testground/PUBLISH.md`.
- Facts: card 01a17b00-67a4 (14h): render `host serve --certify`, `--connect` and the KEYS hide in the deployed units; not done. The box serves 5c0c2055, about 20 landings behind (STALL-WATCH 15:43Z). The page and the writer must speak one wire (PUBLISH.md); `publish.sh` checks that `world.json` answers, not that the wire matches. The tenant files live in another repository (`dregg-infra-demo-vm/edge/demo/tenants/nd-testground`), not in this tree. AGENT-5 and TESTGROUND-6 are launched to redeploy; I could not tell whether anything checks the result.
- First card: a check that compares the page's `kernel.json` commit and wire with the box's `/world.json`, run by `publish-check.mjs`.
- Risk: a republished page joins a box on an older wire and every visitor sees a refusal that reads as the writer lying.

**A6. The systemd live harness has not been re-run on the units the sprint changed.**
- Exists: `deploy/live/README.md`, `harness.sh`, `broker.sh`, `confined-unit.sh`, `Ops/LiveCalls.lean` (10-18).
- Facts: the README records runs on 2026-10-17 and 10-18 only, under the retired bwrap. Its own header says so. Rows L and P ("NOT YET RUN under systemd") are still not run. Since then the sandbox became Landlock plus seccomp (7ec9456, 5c0c205), the unit renderer changed (9cf567d, 5c0c205), and the seed units are unrendered (A5). decisions/root.md lists "Re-run the changed systemd harness" as a surviving obligation. Stale bwrap-era cards remain open: 01a15812-884b and 01a15816-7439 (GATES-20m, bwrap rows), 01a15622-81a0 (confinement story from nd-bwrap/AppArmor), 01a155e0-8f91 (`--hide /home`).
- First card: run harness.sh and broker.sh on a box at current main, append the run to the README, and close or rewrite the four bwrap cards.
- Risk: the first production start under systemd is the first test of the new sandbox under a real unit.

**A7. The meter has holes the sprint filed but did not close.**
- Exists: `Kernel/` meter (d280d23), `Protocol/Health.lean`, cards 01a17d72-9404, 01a176d9-0005/-0014/-0021, 01a176d8-ffe9.
- Facts: law and guard ticks are unmetered, fixed at 100,000 each, with no decision entry (2h old). The ticks budget has no owner when a row bites its cap. There is no bytes meter. The meter's fold theorem (the meter at (m, win) is the sum of that window's Turns' ticks by m) is unstated. The family is still named "refusals". Storage: one shared allowance; retirement returns storage but nothing caps one member's share (readers' Q1). The meter is not carried (A1).
- First card: decide law and guard ticks (meter them or write the entry), then the fold theorem.
- Risk: a member runs a law that costs 100,000 ticks per call and the meter reports zero for it.

**A8. Platform: macOS.**
- Exists: `sandbox/src/lib.rs` (macOS `sandbox-exec` branch), `sandbox/src/custody.rs`, `sandbox/src/bin/sandbox-probe.rs`, README line 347.
- Facts: decisions/client.md records the macOS half "unrun since the hbox move" (lines 83, 506, 918, 970). `sandbox-probe` prints "refused unsupported" off Linux. `custody.rs` declares peer-credential checks `Unsupported` on macOS. `standing.sh` and the trace gates need Linux strace; nothing runs the tree's Rust or rows on macOS. The README says macOS is supported through `sandbox-exec`. The sprint rewrote the Linux mechanism and kept the macOS one unchanged.
- First card: run `sandbox/tests/confine.rs` and `client/tests/supervise.rs` on the Mac and record the result, or change the README line.
- Risk: the README claims a platform nobody has run since 10-17.

**A9. The wire moved five times in a day with no version in any handshake I could find.**
- Exists: `Protocol/`, `client/src/generated.rs`, `deploy/units/EXITS.md`, `Host/Carry.lean` (`domStamp`).
- Facts: package wire 5 to 10; call body tags changed (`revoke` to `retire`, `createOf` tag 13); `domOrigin` v3. Old shapes refuse, by `badTag`, `unknownOp`, `shapeMismatch` (decisions/protocol.md lines 1918, 1949). A stamp exists on the carried file only. A member on an older `nd` sees a bare tag name. Greenfield makes the break free; the doctrine asks the break to be loud, and nothing enumerates that each old shape reaches a named, readable refusal.
- First card: a row that sends each superseded wire (old package, old call tag, old origin domain) and asserts the refusal name and that `nd` prints a line saying "upgrade".
- Risk: a stale client reads as a lying or broken writer.

### Tier B: a member or operator hits it first

**B1. Nobody sees the writer die.**
- Exists: `Ops/Units.lean` (Restart=on-failure, StartLimitBurst 5 in 120 s), `deploy/units/EXITS.md`, `Protocol/Health.lean`, card 01a14ac9-a38a (9d: a scheduled `host check` timer).
- Facts: past the start limit the unit stays failed. `grep` of Ops/Units.lean, deploy and docs for OnFailure, WatchdogSec, alert, metrics, uptime: no hits. The OBS axis built a per-member health receipt (`nd receipt --health`), which reads counters from the member's own fold; it says nothing about writer liveness. `deploy/live/journal.sh` reads journals for tests, not for operators.
- First card: a unit-level `OnFailure=` target and a `host check` timer, rendered from Ops.Units.
- Risk: the public box is down and the first signal is a visitor.

**B2. Member keys: loss, backup and rotation.**
- Exists: `client/src/custody.rs` (576 lines, 10-24), `docs/MEMBER.md`, `docs/TRUST.md`.
- Facts: `grep` of docs, decisions, README and client for lost key, key loss, custody backup: no hits. Precommitted `rotate` helps only if the next key is kept. Members are not retirable (KERNEL-70), so a dead member stays. Open cards: observer key rotation for envelope-only custody (01a155a1-f47b, 7d), sign through Lean's Ed25519 instead of dalek (01a155a1-f49e, 7d; QA added `client/tests/kats.rs` and trace replay, which narrows but does not remove it), founder genesis from inputs the founder signed (01a155a1-f4ae, 7d), a member's departure (01a17ad8-5df4, 14h), per-object epoch keys (01a154f6-9cc7, 7d). CLAUDE doctrine lists key custody as a pause item; it has had no pause.
- First card: a MEMBER.md section "if the key file is lost" that states what is and is not recoverable, tested by a row.
- Risk: a member loses a key and the system has no answer in any document.

**B3. What a member keeps on disk.**
- Exists: `Host/Follow`, `client/` workspace (`ND_WORKSPACE`, `ND_HOLDING`), `docs/MEMBER.md`, card 01a14fb9-adb0 (9d, one shared follower Store per World).
- Facts: each follower holds a full re-executed Store; each unsettled attempt keeps argv, continuation and signed call. No document gives the growth rate, the retention a follower may use, or a member's backup order. `--retain` makes older anchors unavailable (OPERATING.md). The 7295 leaked scratch directories and 328 leaked supervisors (cards 01a15812-87ea, 01a16b44-0a52) show disk and process hygiene was an operator problem on hbox already; `devtools/src/lib.rs` now removes its scratch on Drop, but the supervisors card is still open.
- First card: measure a follower's bytes per Turn at deployed parameters and write it in MEMBER.md with the backup order.
- Risk: disk pressure from a member store arrives before anyone has a number.

**B4. Error messages a human reads in `nd`.**
- Exists: `client/src/bin/nd.rs`, `Protocol/Command/Text.lean`, `docs/MEMBER.md`.
- Facts: `nd` prints bare refusal names (`refused missingCell`, `lawDenied`). The plain-word glosses written in the sprint live in testground strings (`testground/demos.js`, `teach.js`), not in a table `nd` or the docs can read. Card 01a17d68-114f (3h): refusal lines should name the cell. Card 01a17c6a-868c: a cancel's final refusal ends with the Host's own text as the refusal name.
- First card: one Lean table from refusal name to a plain sentence, read by `nd` and by the testground.
- Risk: the testground teaches words the real client never says.

**B5. The resident's provider.**
- Exists: `Hosting/Broker.lean` (`providers`, one row: prefix `claude-`), `deploy/tls/pins` (10-20), `decisions/ops.md` OPS-19.
- Facts: one provider, one wire (Messages API), one SPKI pin. The pinned leaf certificate expires 2026-12-20 (OPS-19); if the key changes every call is refused `pinMismatch` until the operator re-pins by hand (RUNBOOK 2a). AGENT-5 is adding a hosted resident on the demo box, so the pin becomes a live dependency in 54 days.
- First card: a dated check that fetches the live leaf key and compares it with `deploy/tls/pins`, run weekly.
- Risk: the agent demo stops on 2026-12-20 with `pinMismatch` and a red herring.

**B6. Testground accessibility and mobile.**
- Exists: `testground/index.html`, `testground.css`, `testground.js`, `teach.js`.
- Facts: one `@media (max-width: 640px)` rule; windows move by `pointerdown`/`pointermove`; `tabindex` count 0; no touch handling; no accessibility or mobile check in `testground/build/gate.sh`. CRIT-TESTGROUND read desktop and hosted flows, not these. UI-OVERHAUL is rebuilding the window manager now, so this may be covered; the brief I saw does not say so. Also card 01a17b8f-3c5e: 10 C signature mismatches in the wasm link (`Host/c/file.c`); `kernel.wasm` is 4.65 MB after 0f86881.
- First card: add keyboard and narrow-viewport steps to `gate.sh`, and settle the 10 wasm mismatches by name.
- Risk: the public demo does not work on a phone or from the keyboard, and a signature mismatch in wasm can trap at call time.

**B7. Operator docs for what landed.**
- Exists: `docs/OPERATING.md` (43 lines), `docs/MEMBER.md`, `docs/reference/` (kernel.md, protocol.md only).
- Facts: grep counts in docs and README: bell/agent/resident 1 to 2 hits per page outside the README; retire/meter/claims in OPERATING 2, MEMBER 1. No reference page for Host (CLI and Store), Hosting (resident, Bell inbox, agent grant set, budgets), Codec or Ops. decisions/root.md lists "executable docs" (parser-backed examples, checked names and links, negative plants) as an unrecovered promise; no such gate exists.
- First card: an OPERATING section for the resident and the agent's human-owned grant set, with the withdraw-by-name step.
- Risk: the agent feature is operable only by its authors.

**B8. Multi-World.**
- Exists: `Protocol/Foreign.lean`, `Spec/Proofs/Foreign.lean`, `client/tests/foreign.rs`, `world/` time-lock fixture, charter scope item 3.
- Facts: the charter puts many Worlds in scope on receipts checked against held heads. No `nd` verb produces or checks a foreign receipt (Verb.lean has none); the only user path is a package that reads `Std.head`. The sprint touched it through the spec and the time-lock demo only. Card 01a14de7-224a (6d): an invitation to a carried World is still TOFU. Card 01a17d72-9488: three comparison paths carry no claim.
- First card: a member-level walk-through of one receipt crossing two Worlds in `nd`, or an entry saying `nd` will not do it.
- Risk: the third scope item of the charter has a theorem and no user.

**B9. The thin joiner.**
- Exists: `Protocol/Proofs/Thin.lean` (10-18), cards T3c 01a17a55-5e88 (12h), testground thin join 01a17a6b-f81d (13h).
- Facts: thin adoption by the writer's certificate alone is not built; adoption still needs a sponsor pin. Certificates landed (PROTOCOL-77.1, -84) but the one consumer that is the point of them has not.
- First card: T3c as filed.
- Risk: certified heads are produced and checked and still not used to join.

### Tier C: the readers asked and nobody answered

**C1. Q4 HOSTING (cv 01a16d3e-5396, open on ember, 3 days).** If a member's follower is re-genesised while the resident runs, nothing re-describes and the cached shape persists. It meets A1 (re-genesis) directly. No lane has it.

**C2. Q2 KERNEL (01a16d3e-5382).** Ember pushed back 10-26; PROTOCOL-79 landed (join signed over the origin), then was reverted by d422453 and reapplied in 79b1ffed. The card still reads pending Ember's read of the ROOT answer; "fix ops.md's sentence" is not recorded as done.

**C3. Q5 CODEC (01a16d3e-53a8).** Partly answered by QA (compiled exe held to the interpreter, GATES-27; Rust replays 45 of 47 traces, `client/tests/kats.rs`). The card stays open on Ember. `Codec/Hash.lean` and `Codec/Ed25519.lean` were not touched; whether a multi-block compiled-versus-interpreted vector exists I did not find.

**C4. The follower as one object.** HOST, PROTOCOL and RUST each named it (VERDICT section 5). PROTOCOL-83/84 and the SPEC claims moved toward it; card 01a17a7a-1f6f (16h) "command state inside follow" and the three Q6 findings (01a17c6a-*: a swapped continuation ends `done ok` or signs another argv) are the unresolved core. Not stale; unworked.

**C5. Rust-side hand layouts.** Readers' A17 (hand-written byte layouts) has fixes for deadlines and `create_once` (decisions/client.md 1224, 1238). I did not find a closure for the hand-written frame and custody layouts, and no open card names them.

**C6. Contextual consolidation.** 01a15f18-2609 (6d, REVIEW HIGH): the contextual program built toy calculi beside nano. CTX-2 moved the resident inside the open calculus and deleted NanoBridge, which answers part. Remaining: `Lang/Contextual/*` research instances against `LiveHoles`. Unworked since the card was filed.

**C7. The decisions record.** `decisions/lang.md` is 7610 lines and `decisions/hosting.md` 2762, with status lines the readers called false (B3). The new `docs/spec/` is the first spec beside them, but no one reconciled the status lines.

**C8. `proposals/`.** Seven files from 2026-10-16 (CHARTER told KERNEL to read them). Untouched; superseded by the layers. The doctrine prefers deletion.

## 3. Open cards with no lane (nanodregg repo; 119 open, 66 aged one day or more)

Counts by layer from `cv task list --tsv --since 30d`: PROTOCOL 16, KERNEL 14, GATES 11, HOST/HOSTING 10, LANG 9, SPEC 9, TESTGROUND/TRUST 7, CLIENT/LAUNCHER 5, other 38. Cards aged four days and more number about 55 and were not touched by the sprint. The 46 minidregg and 9 redregg cards in the same list, and about 30 "census defect: Compiler.* carries no L1 guarantee" cards (12 days), belong to breadstuffs-era trees, not nano.

Aged 9 to 10 days (from the 10-17 to 10-20 era):
- KERNEL: 01a1498e-855a KERNEL-30 carry (OPS-P1); 01a1498e-854c Turn/Cell/Op weights to the codec's byte numbers; 01a14dfa-200a refusals-trie soundness and the World's last head link.
- LANG: 01a14805-3d00 LANG-21 cross-object calls; 01a14e3e-6482 source store; 01a14ef6-598d inherited law at the receiver.
- HOSTING: 01a14aad-fc83 per-grain uids; 01a14a8a-ffa6 closed witness that `open_world_canon`'s premise is satisfiable; 01a14fb9-adb0 shared follower Store.
- PROTOCOL: 01a14ef0-ffe7 Receipt round-trip theorem; 01a14de7-225e use count on a real Store; 01a14df6-0647 follower policy from a Lean plan.
- OPS/GATES: 01a14ac9-a38a scheduled host check; 01a14d95-36cf kernel-sim refusal-early plant; 01a14b42-8eef HOST WASTE ratio prints 0 on zero measured.

Aged 7 days (the STAND-INS and READ batch of 10-20): 01a155a1-f4df (host-sim at the deployed Ctx), f4ef (THE BAR v2 records inviter downtime), f4ae (founder genesis), f49e (sign through Lean), f48c (delete `roundtrip.rs`), f50f (KERNEL-45 addendum: same-turn grants, finality-tier theory, co-receipt matching), f550 (rows' `replaces` audit), f585 (bench rows near the 600 s deadline), f53e (traced read-set store grows without bound), f4c0, f4cf; 01a15746-21fa (carry Honest across a crash); 01a155c8-2d35 (LANG-48 Std.pending, "ruled 10-18, never built"); the Lean-contextual cards 01a1587d-9a98, 01a158da-017c, 01a158c0-dd90, 01a158c0-ddae.

Four to six days: 01a15f18-2609/-2649/-265c (REVIEW HIGH, MEDIUM, METHOD), 01a15b7a-6dd9 (complete observations in the `Std.hole` receive path), 01a14de7-224a (carried-World invitation TOFU), 01a16201-ef03 (`gates/size.py` meaning), 01a165f2-bb33, 01a165b2-5689, 01a1654c-543c (GATES-20s tooth: the census miss COLLATION A22 named).

Stale by the sprint itself: the four bwrap cards in A6.

Cards under four days are mostly this sprint's own follow-ups. Several have an owner lane (TRUST-5 has KERNEL-70 pre-rotation; the GLM waves have 01a17d72-9427, -9462, -9475). Without a lane as of the 15:49Z log: the Q6 findings (01a17c6a-*), 01a17d72-949b and -94af (command-step bounds and interleaving), 01a17d72-944d (no claim for holes over a history), 01a17ab4-17b1 (BELL: a ring key answered twice), 01a17a4a-59df (a grant over a nonexistent cell is admitted), 01a17c7f-abf4 (the fence row cannot run from `~/nd-land`), 01a17bdd-fc1b (`host.sock` after a lost reply).

## 4. Examined and found covered (so the next reader does not repeat them)

- Ledger value conservation under `holds` legs: `Lang/Proofs/Holds.lean` and `Lang/Journey/Holds.lean` landed with LANG-90; `Ledger/` was touched 10 of 11 files; retirement of an account requires balance and floor zero (`valueRemains`), and an object with rows cannot retire (`rowsRemain`), so a retire moves no value.
- The Census after the judge: the census is a standing stage in `standing.sh` and was red for a real reason (A3), not because it is unreached.
- Readers' A13, A14 (resident retries, undecodable output): fixed 10-24 (37772b9, 0c9b14e). A4 (escrow ignores legs): `Spec/Proofs/Exchange.lean`. A6, A7: CLIENT-37, PROTOCOL-73.
- Key custody of the writer's certify key: designed and built (HOSTING-56/60); what is missing is its backup (A4) and deployment (A5).

## 5. What I could not determine

- Whether UI-OVERHAUL covers keyboard and touch (B6).
- Whether the 6d-old REVIEW cards were answered by CTX-2/CTX-6 (C6).
- What an imported World's authority cell actually does at runtime (A1); a row would settle it in minutes.
- Whether `worldBytesMax` accounts for meter leaves (A2).
- The hbox state; I did not log in.
