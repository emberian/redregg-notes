ROOT (real 10-26 04:39Z): read /Users/ember/dev/redregg/work/codex/FABLE-OWNERSHIP.md before editing any file another Fable owns; a conflicting need for one definition is a design fork: write it here and ROOT rules within the hour.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.
ROOT (real 10-26 05:30Z) FORK RULED: the package wire version is assigned by LANDING ORDER: take (origin/main's version when your judge starts) + 1; re-draw the vectors at that number; add your child at the next free node; re-number on any rebase over another bump. Expected CTX 6, TYPES 7, PCC 8 unless the judges order otherwise. Never two of one number. See FRONTIER-BOARD.md.

FABLE-TYPES-2 (real 10-26 ~09:0xZ): LANG-89 (package wire 5 → 6, the `effects` section) re-ids every package, so
`world/doc/Section`'s `(imports …)` line moves (the three helpers' ids); re-emitted by `lang-journey --write world/doc`,
nothing else in the four texts changes, DC0 reads it back GREEN. It lands with LANG-89 (CROSS-LAYER: HOSTING, by this line).

FABLE-CTX-2 (real 10-26, started ~03:20Z). READ the continuation, DESIGN-CTX whole, the board, the ownership table.
- S2 (contract pins, LANG-84) re-drawn on origin/main c82f171 in wt/fable-ctx: the 18 files merged by `git merge-file`
  (one conflict, decisions/lang.md's end-of-file append: LANG-84 now sits mid-file between LANG-83 and LANG-92), the
  worktree detached at c82f171, Lean rebuilt (419 jobs green), `codec-vectors --write` + `--check` ok (288 of 59
  sites), `lang-journey --write world/doc` (only Section's imports line moves), the four journey modes GREEN,
  `cargo test -p nanodregg-client --test doc` ok. MEASURED. NOT LAUNCHED: the queue holds five full landers
  (263 TYPES, 264 AGENT, 267 PCC, 269 TRUST, 270 META; three of them package-wire bumps), nothing has landed since
  c82f171, and under the landing-order ruling my number is (origin/main's when my judge starts)+1: launching now at 6
  would be displaced by every bump and its generated files (codec-vectors.tsv, world/doc/Section) re-drawn each
  time. I launch when the bumps ahead have landed, at their number + 1; the two waste rows (worstcut-rows
  reopen/audit trie-hashes-per-step) are measured locally at that number before the message pins them (WASTE line,
  GATES by cross-layer, LANG-76's precedent). The reland message carries the seven RESTATES-MEANING lines the judge
  named (the five package-version theorems, runHoleGuard, selectHole).
- FOUND: `gates/runs.tsv`'s lang-journey row runs `(none)` and `--hole-omitted-blocker-pin-admits` only: nothing
  judges `--contextual` or `--contextual-checks` (the contextual sessions, P8's cycle, S2's LG rows, the LP boundary
  rows). Fixed by the registry card below: every registered session runs in the default journey.
- BUILDING (wt/fable-ctx-k1, the board's session-line friction; its own one-line `lang:`): the journey's SESSION
  REGISTRY. `Lang/Journey.lean`: `Session {name, run : IO Run, contextual}`, `initialize sessionsRef : IO.Ref`,
  `register`, `readOr`, `checksRun`, `selectSessions`; `runAll args` reads the registry (the `extra` parameter is
  gone; `--contextual` and `--contextual-checks` are filters printing the same `lang-journey: GREEN` last line).
  `Lang/Journey/Main.lean` is imports + `main` (the `--write` arm), no line per session. One `initialize register
  { name := …, run := … }` line at the end of Offer, OfferEscrow, Head (reads its two .ob sources itself), Doc
  (reads the shipped texts itself), Claims (PCC's file, one line, by this report line), Gen (META's file, one line,
  by this report line), ContextualCycle, ContextualReceive, ContextualWire (the LP checks as a session; it now
  imports Lang.Journey), and Journey.lean's own p8 and hole-observation. AGENT's Inbox session (in the judge now)
  gets its line when it lands; S2's ContextualLaw registers `Law.lawSession`. Lands FAST when the queue is quiet (a
  fast landing displaces every full lander in the judge; not while five are).
- BUILDING (wt/fable-ctx-caller): K1 `Req.caller` (DESIGN-CTX §2.5b; TYPES §7 priced it the same shape; AGENT
  wants it for "which member World's object called"). THE HUNK, by this report line in TRUST's column
  (Kernel/Receive/*): `Req` gains `caller : Option D` (none when a member signed the call, `some obj` when object
  `obj`'s run returned it); `At` gains `caller : Option D`; `reqOf u self principal occasion caller`; the five
  receiver arms pass `a.caller`; `invokeRun`/`invoke`/`dispatch` take `(caller : Option D)` after `actor`; `tree`
  dispatches with `some obj`, `derive` with `none`. LANG (mine/TYPES's Package.lean by this line): `reqTy` gains
  `("caller", optTy .digest)` (second field), `reqData` the `optData` of it, `reqOk` bounds it. The package wire
  FORMAT does not move (no new tag; a package at the old `reqTy` is refused at install by the method-type check, by
  name, never read as the new one) but every package's bytes do, so every shipped text re-emits and the waste rows
  re-pin; it is `kernel!` + `lang!`. Then `Std.offer`'s `take` refuses `notFuser` unless `req.caller = some peer`:
  one session row IS a fuse (LANG-77 L2's critique closed), `offer_safe_forever` statable; then the market.
- K1 `Req.caller` BUILT (wt/fable-ctx-caller on origin/main c82f171): the whole tree green (`lake build` of every
  default target, 774 jobs) after fifteen mechanical passes over the proofs — the kernel hunk as written above;
  `Dispatched` carries the caller as an index (`root` at `none`, `call` at `some obj`); `effect_as_signed`,
  `Lang.RunSource`, `reqData_digests`, `Ledger.MovesThrough/CreditsThrough`, `Ledger.reqAt` restate; no landed
  theorem gains a hypothesis. MEASURED on the K1 tree: lang-journey (every session, with the registry) GREEN,
  --contextual GREEN, --hole-omitted-blocker-pin-admits GREEN, --harness-control RED (the control); codec-vectors
  re-drawn + --check ok; every shipped text re-emitted by its writer (Bell/Escrow/Accept/Timelock lowered from
  their .ob; Head from Std.headPackage; Allowance/Lifecycle by hosting-sim --write-text; world/doc by
  lang-journey --write; pin/Live — NO generator in the tree — brought to the printer's form by hand, `ob` reads
  it); cargo rows doc, foreign, pin ok; `rows` 49/50 → the bar row's `reopen-bytes-per-byte-past-base` plant
  moved 5.260 → 5.292 (every package's text grew: the base World the stale reopen re-reads is bigger), re-pinned
  in Protocol/Rows/Run.lean (TRUST's column, by this line) with the reason, re-run pending; bench-worstcut-rows
  measures 20.191 (ceiling 20.184; S2 alone 20.187): the two waste rows re-pin with K1 as with LANG-76. Entries
  KERNEL-76 (after KERNEL-75) and LANG-85 (after LANG-83) placed mid-file. Lands `kernel!` + `lang!` after S2
  (its own full judge; the queue first). Not in K1: a deployed reader of `caller` — S3's `take` (`notFuser`)
  is the next `lang:` on the settled type, its patch (`offerGate … fuserOnly`) drafted.

FABLE-CTX-3 (real 10-26, started ~08:40Z). READ the continuation whole, DESIGN-CTX, the board, the ownership table.
- The queue at 08:40Z: main unmoved at c82f171; PCC's lander 267 died/was refused after 2h08 (relaunched as 275);
  META 270, AGENT 272, TRUST 273, TYPES 274 in the judge. READ scripts/commit + gates/land.py: a FAST lander holds no
  ticket and lands by compare-and-swap unless a twice-displaced full lander is alive (then it waits ≤ 1 h); every full
  lander mid-judge is displaced at ITS OWN CAS, so a fast landing costs them one displacement (charged only while not
  head) — the free window is right after a full landing, before the displaced ones have re-based.
- STAGED on hbox (/tmp/fable-ctx): `registry2.py` (the registry on ANY main: Main.lean's session lists are PARSED, a
  session another lane added gets its own register line by the module that defines it; reproduces the built tree on
  c82f171 byte for byte), `merge-onto-main.sh` (MINE/BASE/THEIRS per file by git merge-file; conflicts named),
  `registry-reland.sh`, `s2-reland.sh` + `s2-reland-2.sh` (normalise MINE's wire strings to main's N before the merge
  so the bump lines never conflict, then renumber N → N+1 in Bounds/Package/Proofs/Wire/Emit/Vectors (the SITE
  LABELS `lang/package/N` in Emit/Vectors.lean, which the earlier S2 had left at 5 — TYPES/META move them too), the
  Bounds docstring names what N+1 means, the LANG-84 block is inserted after LANG-83 from the saved copy), `s2-finish.py`.
- FOUND and fixed in the S2 reland: FABLE-CTX-1's text edit had spliced LANG-84's MEASURED/Plant paragraphs INTO
  LANG-80's "The blocker, fixed first (MEASURED)." line (the anchor matched twice); the reland takes main's
  decisions/lang.md and inserts only the LANG-84 block.
- DRY RUN of the S2 reland on the unmoved main (V=6): merge clean, Lean 419 jobs green, vectors write+check ok (288 of
  59 sites), doc write, four journey modes GREEN, cargo doc ok; bench-worstcut-rows 20.184 = the ceiling (on c82f171 the
  Bell's cell at version 6 does NOT move the waste rows; the earlier 20.187 was on 62a36ee). The waste rows re-measure at
  the real number.
- STARTED S3 (`notFuser`) in a FOURTH worktree wt/fable-ctx-s3 (an rsync of wt/fable-ctx-caller, the K1 tree): the
  term patch (`offerCallerIsPeerT`, `offerGate … fuserOnly`, take `true` / fuse `false`, offer + escrow) and proof pass 1
  (`CalledByPeer`, `pair_shape_bounded`, `offerCallerIsPeer_eval` via `eqDataBody_meaning`, `callerIsPeer_in_take`,
  `gate_pass`, `body_notFuser`, `take_notFuser`, `take_iff_compliant` gains the `CalledByPeer` conjunct, the method-grain
  refusals gain the premise, `offerTakeTree_inv` gains `hcaller` and the conjunct, `reqData_caller[_conforms]`,
  `take_run_sound` gains the conjunct; fuse sites pass `nomatch`) applied; building.
- S3 BUILT (wt/fable-ctx-s3 = the K1 tree + LANG-96; recipe `/tmp/fable-ctx/notfuser.py`, `s3-proofs1.py`,
  `s3-proofs1b.py`, `s3-proofs3.py`, `s3-journey.py` + three hand fixes (a docstring placement, a `nomatch e, fun …`
  parse, two destructure arities)): `offerCallerIsPeerT`, `offerGate … fuserOnly` (take `true`, fuse `false`, offer +
  escrow); proofs as DESIGN-CTX BUILT-6 says; LF9/LE9 refused `take: refused notFuser`. MEASURED: `lake build` of every
  default target green (5 proof passes, ~2–5 min each at 4 threads on the warm K1 tree), lang-journey GREEN,
  --contextual GREEN, --harness-control RED (1), ledger-sim 1 ALL PASS, emit-cores: Bell/Escrow/Accept/Timelock/Head
  byte-identical, codec-vectors write+check ok (no row moves), `rows` running. It is `lang:` (no shipped byte moves)
  and lands AFTER K1 (it reads `Req.caller`): message `/tmp/fable-ctx/msg-s3.txt` (16 RESTATES-MEANING lines; the
  judge names the rest). LANG-96 claimed in FABLE-OWNERSHIP.md, placed in decisions/lang.md after LANG-85.
- Registry LAUNCHED FAST at 09:24Z (the window right after AGENT's c4800fb7 landed; registry2.py took the Inbox
  session in stride once told its argument form): attempt 1 refused by the source gates for a missing
  `SIZE: Lean lines (Lang)` line (the Journey modules count as Lang lines); attempt 2 launched 09:25Z and has WAITED
  ≥ 1 h 33 min for a gate slot (four full judges hold the four slots) — on the board as friction. TRUST's T2 landed
  9ccb6b6e at ~10:05Z meanwhile; the wire is still 5 (TYPES 274 left the queue unlanded; PCC 275, META 278 still in).
- S2 RELANDED at VERSION 7 and LAUNCHED (full judge, lander pid 915331, log /tmp/fable-ctx/land-s2.log, 12:55Z): META's
  LANG-87 landed 1bdd5ba0 at 12:35Z with the wire at 6, so under the landing-order ruling S2 is 7. `s2-reland.sh` merged
  13 files onto 1bdd5ba0 with two conflicts resolved by hand (Journey.lean's LV rows: mine, they read the version from
  Bounds; Bounds' docstring: main's, the script appends "7: a ROM pin may demand the cell's LAW or PACKAGE"), renumbered
  6 → 7 (Bounds, Package, Proofs/Wire, Emit/Vectors' site labels), re-drew the vectors (291 of 59 sites: META's three
  rows), re-emitted world/doc/Section, Lean 424 jobs green, four journey modes GREEN, cargo doc ok. FOUND: the bench
  binary must be REBUILT at the new version before measuring (a stale `bench-worstcut-rows` refuses the Bell's bytes as
  `refused program` at step 0; the dry run had hidden this); rebuilt: 331851/16448 = 20.176 (main pins 20.187 since
  LANG-87): the two waste rows re-pinned with the LANG-84 sentence (GATES by cross-layer). Also: emit-cores rewrote
  `client/tests/fixtures/foreign/Timelock` by one trailing newline (main's copy is not the writer's byte for byte) —
  reverted, not mine; CLIENT should know.
- S2 attempt 1 (base 1bdd5ba0, V=7): PRE-PUSH GREEN in FULL at ~14:20Z — decls ok (263 modules exported, 10848 parent
  declarations in the reach, 23 map lines, 23 declared changes of meaning: the message's RESTATES list is complete), runs
  ok (87 runs of 60 exes, 39 rows run, 3383 s wall), every generated file ok — then DISPLACED by META's fast
  c327ba13 (1 of 5 charged); attempt 2 re-bases onto it with the record reused. The registry's fast lander (attempt 2)
  has waited for a slot since ~11:50Z.

RELAND-CTX (real 10-26, started ~19:50Z; successor of FABLE-CTX-3).
- Found: the registry's attempt 2 (land-reg2) REFUSED at its 4th re-base by a Main.lean conflict with S2 (b33984e
  added `Law.lawSession` to the `--contextual` list); S2 landed b33984e (version 7); OBS's meter d280d23 on top.
- REGISTRY LANDED f193a3e7 (FAST, CAS on d280d23, ~20:10Z; log /tmp/fable-ctx/land-reg3.log): `registry-reland.sh`
  re-drew it on d280d23 (registry2.py parsed S2's `Law.lawSession` and gave ContextualLaw.lean its register line, 13
  files), lang-journey built at 6G/2 threads, GREEN in every mode (1240 lines, 0 FAIL; 173 LP + 17 LG rows now in
  the default run), --harness-control RED (the control), `--write world/doc` unchanged; fast judge: decls 0 changes
  of meaning, census ok. Told RELAND-TYPES, RELAND-PCC and RELAND-TRUST in their reports: a new session is one
  `initialize register` line in its own module; drop the Main.lean list edit on rebase.
- K1 `Req.caller` (KERNEL-76 + LANG-85, `kernel!`) RELANDED on f193a3e and LAUNCHED (full judge; lander pid file
  /tmp/fable-ctx/land-k1.pid, log /tmp/fable-ctx/land-k1.log, message /tmp/fable-ctx/msg-k1.txt, ~21:00Z; RELAND-TRUST's
  T3b is in the judge ahead of it). `k1-reland.sh`: 38 hand-written files merged onto f193a3e, six conflicts, all one
  shape (OBS's meter added `sealTurn … ticks` / `deriveWithTicks` where K1 added `none` after `c.unsigned.member`):
  main's side taken with the `none` inserted; `deriveWithTicks` (new on main) dispatches with `none`. Whole tree green
  (782 jobs; at 6G two tries were cgroup OOM-kills of one lean while heavy modules overlapped, retried, cached work
  kept). Emitters: Bell, Escrow, Head, foreign/Accept, foreign/Timelock, Lifecycle, Allowance, world/doc re-emitted;
  codec-vectors re-drawn UNCHANGED (292 of 59 sites). lang-journey GREEN in every mode (1240 lines), harness-control RED
  (the control); cargo client doc/foreign/pin ok. `rows`: the bar plant moved 6.069 → 6.105 (main's pin since KERNEL-68;
  re-pinned in Protocol/Rows/Run.lean, TRUST's column, by this line) → ALL PASS. Bench worstcut-rows: K1 319701/15872 =
  20.142; MAIN f193a3e measured 319393/15872 = 20.123 (the meter's 40-byte Turn left 15872 steps where there were 16448
  and nobody re-pinned; the pin still says 20.176): the two ceilings LOWERED to 20.142 with both numbers in the row
  (GATES by cross-layer). decls: `gates/decls.py judge` run locally against main's cached export (a COPY of the cache, the
  shared one untouched): first RED with 38 private names + `deriveWithTicks` to add and `derive` to drop (it now reads
  deriveWithTicks); then ok, 118 map lines = 118 declared changes. Source gates (`gates/check.py`) green but for SIZE.md
  (commit writes it) after five SIZE lines and seven per-owner CROSS-LAYER lines (KERNEL/TRUST, LANG, LEDGER, PROTOCOL,
  HOSTING, CLIENT, GATES; ROOT for the ones with no live lane).
- S3 (`notFuser`, LANG-96) re-drawn on top of the relanded K1 in wt/fable-ctx-s3 (`/tmp/fable-ctx/s3-prep.sh`: the 8 Lang
  files 3-way merged clean against the old K1 copies, LANG-96 placed after LANG-85); building (`s3-build.sh`); it lands
  `lang:` FAST after K1 is on main.
- S3 BUILT on the relanded K1 (wt/fable-ctx-s3, 9 files over the K1 tree): whole tree green, lang-journey GREEN in every
  mode, LF9/LE9 `take: refused notFuser`, harness-control RED (control), every shipped text unchanged, vectors ok;
  source gates green on the K1 tree as base. Message /tmp/fable-ctx/msg-s3b.txt. Lands FAST once K1 is on main
  (decls judged then against K1's cached export).
- Main moved under K1's judge (TRUST T3b 8f1e332 + 90711a5, then 202f8f4): K1 re-checked on 90711a5 in wt/fable-ctx-k1
  (`git apply --3way` of the caller diff, no conflict): whole tree green, every shipped text unchanged by the re-base,
  lang-journey GREEN, rows ALL PASS (plant 6.105 holds), worstcut-rows 319287/15872 = 20.117 (under the 20.142 ceiling).
  The lander's automatic re-base should judge green.
- K1 attempt 1 REFUSED (~23:15Z, log /tmp/fable-ctx/land-k1-attempt1.log): build, decls, generated files green; runs RED on
  ONE new red — gates/certificate_plants.py P3's plant site names `Dispatched X o c n wk actor (.transfer …)`, which
  K1's `Dispatched … actor caller …` no longer contains (and gates/certificate.py's pin of grant_moves_le_cap: its
  vocabulary word `MovesThrough` restated). Fixed on the built tree: P3's site and region take the caller binder;
  certificate-grant.json re-emitted by `--emit-pin` (statement, axioms, supports unchanged); certificate-pin GREEN and
  its control RED; CERTIFICATE PLANTS GREEN and its control RED. Attempt 2 LAUNCHED ~23:23Z (pid file
  /tmp/fable-ctx/land-k1.pid, log land-k1.log), the GATES cross-layer line names both files. Lesson for a lane that
  restates a definition: grep gates/*_plants.py for the old text before launching (a plant site is a source-text anchor).
- K1 attempt 2 REFUSED (~01:00Z+, log /tmp/fable-ctx/land-k1-attempt2.log): its automatic re-base took TRUST's
  Kernel/Proofs/AuthorityOf.lean (5a0a7e4, new on main), whose `derive_all` base case did not bind the caller → build
  red. Caller worktree carried onto 7e362108 by throwaway `--no-verify` commit + rebase + `reset --mixed` (clean), the one
  intro fixed, whole tree green, every shipped text unchanged, journeys GREEN, certificate-pin GREEN, decls judge ok (118
  = 118) against 7e362108's cached export, source gates green. Attempt 3 LAUNCHED (pid file /tmp/fable-ctx/land-k1.pid).
- K1 attempt 3 NOT JUDGED (~01:25Z, log land-k1-attempt3.log): build, census, decls (118 = 118), cbytes, clippy ok; the
  runs step UNREAD — `standing:bench-worstcut-rows --harness-control` passed 600 s of wall clock twice under load (not a
  verdict). Attempt 4 LAUNCHED ~01:31Z on main 5527b018 (nothing on main since 7e362108 names Dispatched/derive_all/reqOf).
RELAND-CTX answer to Ember's velocity question (real 10-27 ~03:10Z):
(1) BLOCKED NOW: nothing I can fix — K1 attempt 4 (pid file /tmp/fable-ctx/land-k1.pid) is ~1h25 into the full judge. In ~6 h
    K1 spent ~5 h waiting: attempt 1 red on a gates plant anchor (my miss: a source-text site naming the old `Dispatched`);
    attempt 2 red from an automatic re-base onto a TRUST file that landed mid-judge (one `intro` binder); attempt 3 NOT JUDGED
    (bench-worstcut-rows' control passed its 600 s wall-clock limit under load). Each refusal costs a fresh 2-2.5 h judge. S3
    (notFuser) is BUILT and waits on K1. The registry landed fast in 15 min.
(2) ROOT/Ember in the next hour: give the standing bench rows (bench-worstcut-*) a wall clock that scales with load, or run them
    only at convergence (they are standing-only anyway), so a load spike is never a NOT JUDGED; and let a lander re-run only the
    failed step (a red/unread run row) on the same tree instead of the whole judge.
(3) The ONE change: a refused/unjudged lander KEEPS the verdicts of its green steps on a byte-identical tree and re-runs only the
    red ones (FIX-QUEUE's "byte-identical reach keeps its verdict" generalised from displacement to refusal). Flag days on the fast
    judge with the full set at convergence would also have landed K1 in ~20 min: yes to that too.
(4) Brief: the 6G cap OOM-kills one lean per whole-tree build when heavy kernel modules overlap (two to three retries each, cached
    work kept, so it costs time, not correctness); 8-10G would build in one pass. Otherwise the brief was right.
- RELAND-CTX (real 10-27 ~06:00Z): LANDED registry f193a3e7. LANDING K1 Req.caller by rule 1 now (wt/fable-ctx-caller rebased onto origin/main past 6faa984, one prose commit; the deleted gates' certificate files dropped; the NEW scripts/commit running, pid /tmp/fable-ctx/land-k1-r1.pid, log land-k1-r1.log, one build at its 24G default). BUILT and waiting on K1: S3 notFuser (wt/fable-ctx-s3). NEXT: S3 by rule 1 the moment K1 is on main.
- RELAND-CTX (10-27 ~08:00Z): K1's first rule-1 landing RED in the new Spec layer (Spec/Proofs/AuthKernel, Auth, Cap, Law; Spec/Sim/Auth, Bell, Cap had not seen the caller): ported (Prov/walk/Authorized carry the caller; sims pass none), Spec builds; re-based again over TYPES' LANG-89 (6e177d5; conflicts: the bar plant pin, two generated texts); whole-tree build + emitters + journeys + rows running (k1-r3.sh), then scripts/commit.
- RELAND-CTX (10-27): K1 Req.caller LANDED 176110a7 (pushed by hand under rule 1 on ee2f790f: whole tree built, lang-journey every mode GREEN, ledger-sim, rows ALL PASS with the bar plant at 6.119, cargo client doc/foreign/pin ok). On the way it threaded the caller through what landed meanwhile: the Spec layer (AuthKernel, Auth, Cap, Law, Escrow, sims), Web/Sim/Teach callLines (none at depth 0, the calling object below), KERNEL-70's retire (receiver + retire_derived/retire_next + History), META's createOf (+ createOf_draft); and pin/Live gained the (holds) field b03731b landed without (main's pin row refused badPackage). Next: S3 notFuser.

FABLE-CTX-4 (real 10-27, started ~11:10Z; ROOT's redirect at ~11:25Z: the resident into the open calculus first, NanoBridge deleted only after).
- CTX-4 PLAN: DESIGN-CTX §11 written (the resident's four holes `serve`, `text r`, `pins r`, `use r t`; the Prot term sketched; the order).
- CTX-4 FIRST FINDING — what the calculus (`Lang/Contextual/Protocol.lean`) lacks to hold the resident (READ, not yet built):
  (1) resolution at run time: `σ` is chosen before anything is observed and `interpret` ends `stuck` at a hole; the resident decides
  after its read, so the calculus needs "at the hole's reach, with the view then current, fill the selected candidate whose supports
  hold, or withdraw by name" and a `withdrawn` outcome; (2) candidates with supports: `Iface` has no candidate set, no per-candidate
  supports, no selection (this IS the SLOT); (3) the view moves during the run and refusals are RESPONSES: `View` is a static record
  and `admits` a precondition, but on nano the kernel checks supports at the effect and the resident learns of a dead support from the
  refusal's coordinate; (4) one repair rule: `Open.replan` (guarded by `Dispatched`) and `Frag.repair` are unconnected; (5) permanent vs
  reversible supports (a tombstone vs a law membership); (6) response-indexed hole names are called foresight because `σ` is pre-chosen,
  sound under run-time resolution; (7) a monadic interpreter. What already fits: the affine discipline — one ask per ring is a token
  spent once (`at_most_once`), a kept answer is a filling the history entered (`Dispatched`), and `Open.Replan` forbids re-planning it.
  A deployed defect the theory names: an aimed ring whose `via` grant was retired before the answer stops the WHOLE queue
  (`answerRefused`); under the `use` hole it is withdrawn by name and the next ring served.
- CTX-4 K2/S3 `notFuser` (LANG-100): built green on origin/main 176110a7 in wt/fable-ctx-s3 (whole tree, lang-journey every
  mode, ledger-sim, rows ALL PASS). LANDING by rule 1 with a prose message: attempt 1 build/journeys/rows ok but `rows --deployed`
  UNREAD (600 s wall clock under load); attempt 2 running at parking (pid /tmp/fable-ctx/land-s3-r1.pid, log land-s3-r1.log). No hash yet.
- CTX-4 THE RESIDENT IN THE CALCULUS — BUILT IN PART (uncommitted, hbox wt/fable-ctx4 on 5fe0bff1): `Lang/Contextual/Slot.lean`
  (the SLOT, `slot_repair` — the one repair theorem — and `interp`, the calculus's monadic interpreter with holes resolved when
  reached) GREEN; the resident's `Prog` IS `Prot sig Hole` with two holes (`serve`: which ring, a slot over the kept answer, an
  ask per pending ring, idling, each ring citing "pending" and "its answer stands"; `use`: after a refused answer, closed /
  withdrawn by the name of the aim's via or target cell / stop), run by `Slot.interp`; `ResidentRun` ported and GREEN (tick_order,
  tick_counts over the live rings, kept_follows, retries, `tickP_fits`, `interp_runs`); NanoBridge + ContextualNano deleted,
  ContextualFailures → `Hosting/Proofs/LostReply.lean`. RED next: Spec/Sim/Bell (one field), BellConform (a withdrawal must
  DISCHARGE the round's debt by name: `Frees` gains the refused-naming-a-cited-cell arm; the owed ring must stand), Lifetime
  (mechanical). Not yet: the resident repair theorem as a `slot_repair` instance, the H4 launcher row (retired via → withdrawn by
  name, next ring answered; also measures the real refusal line), the testground line, the document's evidence-bearing read.
- CTX-4 PARKED at ~390K context. Continuation: /Users/ember/dev/redregg/work/codex/FABLE-CTX-4.continuation.md.

FABLE-CTX-5 (real 10-27, from FABLE-CTX-4's continuation).
- CTX-5 K2/S3 `notFuser` (LANG-100) LANDED 48232e7b. The lander's second attempt was again RED only on `rows --deployed`
  (UNREAD: the 600 s wall clock under load 12-50, the known limit defect); lander dead. Pushed by hand under rule 1: the
  commit 07d5ec9b rebased onto origin/main 276ded81 (LANG-93; one conflict, decisions/lang.md, both entries kept), built
  `Lang Spec Web lang-journey` (24G) green, lang-journey default / --contextual / --contextual-checks /
  --hole-omitted-blocker-pin-admits all GREEN (LF10/LE9 `take: refused notFuser`). Logs hbox /tmp/fable-ctx/k2-r3*.log.
- CTX-5 THE RESIDENT IN THE OPEN CALCULUS — LANDED 2630ea32 (hosting!; pushed by hand under rule 1: scripts/commit --reverts
  built the reach and ran 13 rows, all ok but `rows --deployed` and `cargo:launcher:resident_bell`, both UNREAD at the 600 s
  wall clock; resident_bell then run alone in the landing tree: ok in 690 s; rebased over LANG-103 with no overlapping path).
  `--reverts` because deleting NanoBridge/ContextualNano reads as reverting be589b7e7's move of them.
  What it is: `Prog` IS `Prot sig Hole`, two holes run by `Slot.interp`; `serve` (pending + stands) and `use` (closed /
  withdraw by a gone cited cell / stop). Reds fixed: Spec/Sim/Bell (Mem field; `tickWith`'s act is now the serve hole's
  filling, `tickWith_actOn` a Runs implication; `Bell.oneAsk` (a) names `serveChoice`), Lifetime (mechanical), BellConform:
  the round is now a SET of owed rings (`Owes m D`: each owed ring is the kept one or does not stand), proved over the term's
  paths; `bell_resident_conforms` and `Frees` UNCHANGED — the plan's "withdrawal frees the ring" arm was not taken: it would
  have let the theorem permit a second ask about a withdrawn ring.
  MEASURED (agent_hole H4, first run): the member's line for an answer through a retired `via` is exactly `refused
  missingCell` — it names no cell — so the text-matching `use` slot stopped the queue (answerRefused, crash loop) while every
  theorem stayed green. Fixed in the same landing: after a refusal whose ring waits, the resident PROBES each cited cell
  (`Cmd.probe c` = `read CELL ?`; `probeGone`: refused missingCell → gone) and the `use` slot reads those facts
  (`UseFact.gone c`). H4 then: `resident: answer withdrawn 23 ff42…: its support aa5e… is gone (refused missingCell)`, the
  plain ring answered, three asks in all. A member line naming the coordinate: cv task 01a17d68.
  The repair theorem (Hosting/Proofs/ResidentSlots.lean): `resident_repair` (slot_repair at serve), `use_withdraw_names`,
  `use_withdraws`, `withdrawn_blocked`, `withdrawn_not_served`, `serve_keeps_withdrawn`, `serve_repairs`.
  `order_refuses_forget_while_pending` lost its premise (probes come first). Tree 850 jobs green; lang-journey --contextual,
  --contextual-checks, --hole-omitted-blocker-pin-admits GREEN; resident, resident_bell, agent_hole ok.
  Decisions: LANG-101 (the SLOT), HOSTING-59 (the resident in the calculus), each with critique + meta-critique.
  DESIGN-CTX §1.4 (the ACL-row-store baseline, four guarantees beyond it, and what it still has that the slot lacks).
- CTX-5 (5) THE WITHDRAWN LIST PERSISTED — LANDED 2efa6a57 (hosting!; pushed by hand under rule 1). `Eff.note` writes
  `vol/withdrawn-<bell>` (one printed value per line: the ring and the gone cell's name) before the forget; `run` seeds
  `Mem.withdrawn` from it (`notedSeed`; unreadable ends `volume`) and resumes it (`resumeAt w.notedAt`); a note IS a keep at
  `Where.notedAt`, so the ResidentVolume theorems hold of it unchanged; `ResidentRun.UseCore` is the `use` filling's grammar.
  A restart no longer asks a withdrawn ring again. Verified on 2630ea32: tree 858 jobs green; agent_hole ok (H4 also reads
  the volume file: it names the withdrawn ring's cell); resident ok; resident_bell ok (449 s). Rebased over PROTOCOL-83,
  PROTOCOL-84/HOSTING-60 and a testground commit: no path in common. Not done: a restart row (the file's content is checked;
  the restart path is `run`'s code).
- CTX-5 NOT DONE: (7) the document's read with evidence (the SLOT's second instance). Parked with a continuation at ~360K:
  /Users/ember/dev/redregg/work/codex/FABLE-CTX-5.continuation.md.
