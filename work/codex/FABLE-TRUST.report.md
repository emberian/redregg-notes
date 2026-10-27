# FABLE-TRUST — report (real 2026-10-26)

Lane: the trust-model design (`redregg/work/promo/DESIGN-TRUST.md`) and its first move, built and landed.
Worktree: `hbox:/tank/dregg-build/nanodregg/wt/fable-trust` (from ad90a47; main moved to 62a36ee under it,
FABLE-CTX's two Lang landings; no path overlap).

## Done

- **DESIGN-TRUST.md** (~440 lines): agreement as an OBJECT of the kernel's theory — a `Head`
  `(origin, steps, height, roots, chain)` with an `Authority` (genesis rule: none / writer 1-of-1 /
  2f+1-of-3f+1) and member `Attestation`s under every authority; one-writer, committee and "a fork is a
  new World" as instances; fork consistency as the first instance (nano already had the no-rejoin half
  by the chain; only the compare act and the witness were missing); mini's nine ambitions as
  member-facing guarantees with what meets each (M9, offline merge, met by nothing here and said so);
  the price (0 kernel premises; T2 `lang!`; T3 `host!`+`protocol!`); the Store signing seed question in
  system terms (needed first at T3, not before); the sequence T1–T5; the one way it is wrong.
- **T1 built: PROTOCOL-74.** `nd sync --to STEPS:CHAIN | --attest | --check ATTEST`; `Protocol/Head.lean`
  (Head, Attestation, domHead, verified, signer, anchorCheck); `Protocol/Proofs/Head.lean`
  (`anchor_binds`, `forked_not_on_fold`, `shared_on_fold`, `attestTip_sign`, …); Domains +6 pairs;
  `absorbSync` wraps `absorbPage` (no consumer restated); refusals `forkedWorld`, `ahead`,
  `badAttestation`, `otherWorld`, `badHeadSignature`, `notMember`, `staleKey`; row `fork` (PASS toy +
  deployed, plant `ignoreAnchor` caught at line 10); `client/tests/join.rs` drives
  attest/check/forkedWorld/ahead/badAttestation over real sockets (cargo test ok, fmt ok, check ok);
  `decisions/protocol.md` PROTOCOL-74 with critique + meta-critique.
- Landing: `scripts/commit` launched detached from the worktree (`land1.log`, `land1.pid`), fast mode,
  `--cross-layer` for `client/tests/join.rs` (CLIENT) and `Hosting/Proofs/Socket.lean` (HOSTING, two
  try-lines in `step_cont`). Status: see the bottom of this file.

## Coordination with FABLE-CTX

Nothing in `Lang/**` touched. T2 (self-heads through the writer) will: `Std.head`'s `headAtTy` gains
`("chain", .digest)` and the `at → at` law compares it at equal steps (`Lang/StdHead.lean`, ~20 lines,
`lang!`: `world/head/Head` re-emits, `headPackageId` moves, the X rows re-pin). I will not start that
edit while FABLE-CTX holds `Lang/**`; say when, or do it yourselves from the memo's §4.2 and I will
land the Protocol half (follow walks every absorbed self-head post as an anchor).

## For Ember (one decision, not blocking)

The Store signing seed (KERNEL-44 refused it; DESIGN-TRUST §4.4): needed at T3 (writer-certified heads:
strangers and thin joiners believe a head by one signature; E5's `hr` discharged; a fork attributed to the
writer by its own signature). T1 and T2 need nothing. Default I would defend: take it at T3 as a `certify`
key distinct from the MAC keys, one Store's seed on one host (a tcb.tsv row).

## Status

- 2026-10-26: **T1 LANDED** as nano main `5fa281d` (pushed to origin). First attempt RED on two things,
  both fixed: decls (the map needed `custodyEnd`, `custodyPhase`, `signedReads`, `submits` — their
  matchers changed with `Cmd.sync`'s arity — and `Nanodregg.Protocol.rows`, not `Rows.rows`) and the
  statement census (`anchor_binds`'s collision list ranged over a prefix the conclusion chose; restated
  over a premise-fixed prefix, GATES-20s). Second attempt: judge GREEN twice (displaced once by a moved
  main), landed by CAS. Parked at ~600K tokens; continuation: `redregg/work/FABLE-TRUST.continuation.md`.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.

## FABLE-TRUST-2 (real 2026-10-26, successor; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`, rebased on 1e8a2a0)

**The Std.head hunk (Lang half, TRUST's by FABLE-OWNERSHIP; for FABLE-CTX to object to):** `Lang/StdHead.lean`
`headAtTy := .record [("chain", .digest), ("height", .nat), ("roots", .digest), ("steps", .nat)]`; `atRec c h r s`;
`HeadView.at (world chain : ByteArray) (height) (roots) (steps)`; `headView` reads the field. The law's `at → at`
arm is unchanged in text (`eqData headAtTy` now compares the chain at an equal step count). `Lang/Proofs/StdHead.lean`:
`AtOk c h r s`, `atRec_conforms`, `head_at_at` gains `c = c'`. `Lang/Journey/Head.lean`: the chain in every seed and
post, HD3b (held roots, another chain: `forkedHead`). `world/head/Head` re-emitted from `Lang.Print.packageText`
(3 lines). Nothing else under `Lang/**` touched. Decision LANG-95 (claimed in FABLE-OWNERSHIP.md).

**T2 as built (PROTOCOL-75):** `nd sync --post OBJ` (`Cmd.post`: `invoke OBJ post` with `Head.headText` of follow's
OWN World at the tip; consent `body_post`); after `absorbSync`, `Head.forkedSelfPost` walks the page against every
self-head post it carries (`selfPosts`: a `Std.head` of THIS World a step touched) and refuses `forkedPost STEPS`
(poster named) with the PAGE KEPT — refusing the page would let any member with post rights freeze every other
member's follow; theorems `forkedSelfPost_forked`, `forkedSelfPost_none`; row `selfHead` (plant MEASURED: no
harness mutation reaches follow's walk). `receipt CALL` prints `head STEPS HEIGHT ROOTS CHAIN`.

**The hole I found and did not paper over:** the pure walk compares a post only against positions INSIDE the page
that carries it. A live member is past every post it absorbs, so it compares nothing purely; its chain at that step
is in its own Store's index (`host check --anchor` reads it, `Page.kept` at budget 0). DESIGN-TRUST §4.2's "or
records `ahead`" is the COMMON case, not an edge. Fix = the follow loop (`Host.Follow.loop`) takes a `PageFiles` from
`Host/Cli.lean` and resolves behind-positions through `pageKept`; HOST-prefixed; **cv task 01a176ab-14f5 (T2b')**,
next after this landing. Until then "M3 continuously" holds for members behind the post (cold joiners, members
catching up), which the row states (`fault := .cold`).

**Store signing seed:** untouched; cv 01a1769d-2f64 still `open`, posed to Ember (default: take it at T3). T3's
unsigned pieces (Authority in genesis, Certificate codec, Thin.accept's check, the head law's `uncertified`) are
NOT started in this session (context spent on T2 + the hole); the continuation says where to start.

**Status (FABLE-TRUST-2, parked at the context ceiling, real 2026-10-26):** T2 BUILT and measured green on
`wt/fable-trust` (rows PASS toy+deployed, plant measured, cargo ok) but **NOT LANDED**: `scripts/pre-push` refuses the
`set_option maxHeartbeats` that `step_world` needed under my `if let` in `step`; the measured fix (`postOr`, a top-level
function in place of the match: `step_world` then builds) leaves two proof files red by reply shape
(`Protocol/Proofs/Incoming.lean`, `Protocol/Proofs/Command.lean`), which the successor fixes first — exact recipe in
`redregg/work/FABLE-TRUST.continuation.md`. Nothing on main moved from this lane. Open tasks: T2b' `01a176ab-14f5`
(the follow loop's index resolution, the honest hole); the seed `01a1769d-2f64` (Ember's). The `.lake` is warm.

## FABLE-TRUST-3 (real 2026-10-26, successor of FABLE-TRUST-2; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`, rebased onto origin/main c82f171)

**T2 (PROTOCOL-75 + LANG-95) fixed without a budget raise and sent to the judge.** The measured fix is the
one the continuation named: `postOr` (`Protocol/Command/Machine.lean`, now `@[irreducible]`) applies the
self-head verdict to every reply the page arm's `moved` hands out, so `step` gains no match. The reply-shape
proofs read it by an algebra in a NEW proof module `Protocol/Proofs/PostOr.lean` (C3 refused theorems in
the def module): `postOr_cases`, `postOr_eq_elim`, `postOr_cont_elim`, `postOr_cont_some`, and one elim per
reply constructor (`sign`, `signIncoming`, `signNext`, `host`, `submit`, `precommit`, `done ok`). Strip lines
in `Proofs/Incoming.lean` (`step_incoming_kept`, `step_signIncoming_asked`, `step_asked_signIncoming`),
`Proofs/Command.lean` (`step_submit_planned`, `step_host_cancel`, the `cancel` settlement theorem),
`Hosting/Proofs/Socket.lean` (`step_cont`, `step_invoke_ok`) and `SocketStrong.lean` (`step_describe_ok`).
MEASURED: with the wrapped `behind` arms left to the `_ne_submit`/`_ne_host` cascades, `step_submit_planned`
and `step_host_cancel` pass 200 000 heartbeats (bisected in a scratch module: variants through the strip
pass, the cascade times out); closing those arms right after the strip (`simp only [reduceCtorEq,
and_false] at h; done`) brings both under budget. Every proof in the tree is at the default budget.
Rebase onto c82f171 was clean by `git checkout -m`; two upstream consumers of the old four-field head
fixed: `client/tests/foreign.rs` X6 (`receipt` is a 5-tuple, `head_text` takes the chain) and
`Lang/Journey/Gen.lean` GN2 (seeds and posts with a chain; `headPackageBytes` is symbolic, so GN1 tracks).
Green on the rebased tree: `lake build Protocol Hosting rows host`; rows `selfHead fork receipt
lang-journey` PASS toy, `selfHead fork` PASS deployed; `cargo test --test foreign` ok (1 passed).
Judge: `scripts/commit -F commit-msg2.txt --cross-layer … ` (22 files, PROTOCOL-75 + LANG-95; `protocol!`),
three refusals fixed in turn (a `set_option`-free tree; C3 moved the lemmas; SIZE lines named exactly:
`Lean lines (Hosting)`, `Lean modules`, `Lean proof-modules`), **fourth attempt running as PID 2907901
behind four other lanes' judges on the main commit queue (`land5.log` in the worktree; empty until its
slot)**. Attempt 5 verdict (land5.log, after a 3327 s run of 35 exes): build ok, census ok, runs ok, cargo-check
ok, clippy ok; RED on `decls` (the RESTATES-MEANING map: drop `Command.parse`; add the twelve it printed — the
`Lang.Std` head theorems, the five `Command` definitions whose match bodies gained the `.post` arm, the four
`Proofs.Foreign` statements) and `fmt` (one rustfmt wrap in foreign.rs X6). Both fixed; attempt 6 = `land6.log`
(launched with T2 alone in the tree; T3 re-spliced after its record line). The gate log also shows `launcher
--test fence` and `attach --test attach` failing on hosted-uid/group-socket tests (not named in the verdict line;
environmental by their names; say so to ROOT if attempt 6 names them).

**T3's unsigned half BUILT (PROTOCOL-76; not yet judged — it sits on T2's files).** `Protocol/Head.lean`:
`Authority`, `Authority.none`, `domCertify`, `certifiedLayout`/`certificateLayout`, `certifiedBytes`,
`certifyMessage`, `certificateBytes`, `Certificate`, `CertRefusal` (+`name`/`tag`), `certifiedSaid`,
`certificateOfBytes`, `certifySigners`, `certified`. `Protocol/Proofs/Head.lean`: `CertRefusal.name_injective`,
`certificateOfBytes_head`, `certifySigners_ok`, `certified_ok`, `certified_none_unlisted`, `nodup_lt_length`,
`certified_intersect` (the committee row as a theorem: `n < 2t` ⇒ a shared listed certifier, by pigeonhole
through `Kernel.nodup_window_length`), `certified_equivocation`. `Protocol/Proofs/Domains.lean`: seven
`certify_*_disjoint` + seven `certify_not_*`. MEASURED: `lake build Protocol.Proofs.Head Protocol.Proofs.Domains`
green (build20.log); then MEASURED under T3 on the whole tree (build21.log): `lake build Protocol Hosting rows host`
green, rows `selfHead fork receipt lang-journey` PASS toy and `selfHead fork` PASS deployed, `cargo test --test
foreign` ok. Not run: the judge (it needs T2 on main first). The entry PROTOCOL-76 is appended to `decisions/protocol.md` in the worktree;
`commit-msg3.txt` is in the worktree root (`protocol:` prefix: no wire or disk byte moves). The splice is
reproducible: `t3/t3apply.py t3` over `t3/t2bak/*` (the three files as T2 left them).

**Seed:** cv `01a1769d-2f64` still `open` (checked at session start); nothing signed, no custody object.
**Tasks:** T3b (the genesis wiring and the consumers) opened as cv `01a176f6-ac3f`; T2b' `01a176ab-14f5`
untouched (context went to T2's landing and T3's object).

**Status (FABLE-TRUST-3, parking at the context ceiling, real 2026-10-26):** T2 green on the rebased tree; attempt 6
of the judge running in gate slot 1 (T2 alone recorded; `land6.log` empty, verdict in the gate-1 log / origin/main);
T3's object + theorems built green on the whole tree (rows and cargo unchanged), unjudged, re-spliced in the working
tree with `commit-msg3.txt` ready; T3b tasked (cv 01a176f6-ac3f); the seed Ember's (cv 01a1769d, open); T2b' untouched.

## FABLE-TRUST-4 (real 2026-10-26, successor of FABLE-TRUST-3; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`)

**T2 LANDED: origin/main `9ccb6b6e` (PROTOCOL-75 + LANG-95; `protocol!`).** Attempt 6 was judged whole in gate slot
1 (tree 714bfe058e20: census, decls 26/26, cbytes, 77 runs of 35 exes, cargo-check, clippy, fmt — PRE-PUSH GREEN),
then displaced once (c4800fb7, HOSTING-53 the inbox, landed under its verdict); the judge re-based itself (3-way
merges of `Hosting/Proofs/Socket.lean`, `SocketStrong.lean`, `Protocol/Rows.lean` onto the recorded bases), judged
again as tree 7b838e51f022 (79 runs of 36 exes, 11 re-run, the rest reused byte-identical) and landed by
compare-and-swap. No file was touched by hand between the verdicts. T3's three files + PROTOCOL-76 were kept by the
judge as uncommitted edits on the landed copy (384 insertions, no conflict markers; verified by `git diff --stat`).

**T3's unsigned half re-measured on the landed tree (9ccb6b6e) and sent to the judge.** `build22.sh`: `lake build
Protocol.Proofs.Head Protocol.Proofs.Domains` green (107 jobs); `lake build Protocol Hosting rows host` green (427
jobs); rows `receipt lang-journey fork selfHead` PASS toy, `fork selfHead` PASS deployed (unchanged: nothing deployed
consumes a certificate); `cargo test --test foreign` ok (1 passed). Judge: `scripts/commit -F commit-msg3.txt
Protocol/Head.lean Protocol/Proofs/Head.lean Protocol/Proofs/Domains.lean decisions/protocol.md` (`protocol:`, no
`!`: no byte moves), `land-t3.log` in the worktree. SIZE lines name the metrics as `SIZE.md` spells them (`Lean lines
(Protocol)`, `Lean lines (deployed)`, `theorems`; `refusal constructors` counts only `Kernel.World.Reject` and
`Kernel.Receive.Refusal`, so `CertRefusal` does not move it).

**T3's unsigned half LANDED: origin/main `f70a5f9e` (PROTOCOL-76; `protocol:`).** Judged FAST (no `!`): tree
aec3a49d83e9, decls 0 map lines / 0 declared changes, census ok over the 47-module reach, built `Protocol Host
Hosting Bench rows host-sim host …`; PRE-PUSH FAST GREEN; landed by compare-and-swap on 9ccb6b6e. The worktree
is detached at f70a5f9e, clean.

**T3b, first landing (KERNEL-68 + PROTOCOL-77), BUILDING on `wt/fable-trust` over f70a5f9e.** The map (an Explore
scout, read against origin/main): `atGenesis` admits only member/grant cells at step 0 (`Machine.lean:1201-1215`);
`founderEntries_length` and `genesisWorld_codecFits` enumerate the genesis trie exactly (`Host/Proofs/Deployed.lean`);
`Thin.accept` has ONE caller (`Machine.lean:1530`); no Rust reads the `log`/`read` reply layouts (passed verbatim, not
emitted). `RomContent` has no consumer outside `Kernel/Proofs/Rooted.lean`; `romIdOf` is content-only; every receiver
reads cells through `readKind` (kind-checked) and no receiver names a new kind. Decision (DESIGN-TRUST BUILT-4): the
authority is a genesis input committed in the origin (`domOrigin` v3) AND one ROM cell at its content id (`fold_rom`
= immutability as a theorem; `RomContent` by construction), found by kind; `Carried` gains nothing. Written by me
(K1): `Kernel/Receive/Follow.lean`, `Kernel/Receive/Call.lean`, `Kernel/Proofs/Origin.lean` (`Authority.Fits`,
`checkCertifiers_ok`, the six-clause `GenesisFits`, `genesis_inj` ⇒ `auth = auth'`), `Kernel/Proofs/Rooted.lean`
(`mem_genesisEntries`, `genesis_rooted`, `genesis_romContent`), `Kernel/Proofs/CellsFit.lean`; `Kernel.Receive.Follow`
builds; the proof modules sit under `Kernel/Proofs/Rows.lean`, the first of the ~40-file binder sweep, delegated to a
worker in the worktree with the exact signatures (design items 1–7 in its brief: Deployed's `genesisEntries_length`,
`genesisLeaf` + `genesisWorld_atGenesis`, `Protocol.Head.Authority` deleted, `Start.genesis … auth`, `host genesis
--certifier/--threshold` + the `authority` line before `input`, Ops/Founder, Trusted/Carry/Foreign binders). Texts
ready in my scratch: KERNEL-68, PROTOCOL-77, `commit-msg4.txt` (`kernel!`, cross-layer PROTOCOL + HOST + the call
sites in LANG/HOSTING/PERF). The decls map lines (every statement restated by binder) will be taken from the judge's
first refusal, not guessed.
**Deferred into cv, not prose:** `authorityOf_genesis` (the honest-carrier theorem of KERNEL-68) is cv
`01a177f3-2293`, TRUST-owned, to land with or before T3b's consumer landing (cv `01a176f6-ac3f`). The texts for
the first landing sit in the worktree under `t3b/` (`commit-msg4.txt`, `kernel68.md`, `protocol77.md`).

**T3b first landing (KERNEL-68 + PROTOCOL-77) BUILT green on the whole tree and IN THE JUDGE.** The sweep (a worker
in the worktree, 53 files) + my 5: 58 files, +623/−418; bare `lake build` 777 jobs green; `Protocol Hosting rows
host` green; rows `receipt lang-journey fork selfHead` PASS toy, `fork selfHead` PASS deployed; `cargo test --test
foreign` 1 passed, `--test join` 1 passed (the `authority` line sits before `input`; the Rust reads lines by prefix);
0 sorry / set_option in the diff (checked on the diff, not the report). Statements changed beyond a binder:
`Invite.Start`, `accept_genesis`, `accept_origin`, `Cli.join_genesis_iff`, `Deployed.CheckpointTrusted.reached`,
`genesisEntries_length` (new), `genesisLeaf`, `hintReps` (the four refusal names, `hintNames_complete`); deleted
`Protocol.Head.Authority` + `.none`. Repairs the worker made to my five: `swap` → `case inr =>` (no Mathlib), two
`decide`s named as facts, two unused simp args. Judge: `scripts/commit -F t3b/commit-msg4.txt --cross-layer … ` over
60 files (58 + `decisions/kernel.md` KERNEL-68 + `decisions/protocol.md` PROTOCOL-77), `kernel!` ⇒ FULL; log
`land-t3b.log`, PID in `land-t3b.judge.pid` (the judge deletes its own `.pid`; mine is a copy; never kill). Queued
behind four landers at launch (ctx-k1, meta, pcc, types). The decls gate will print the binder-restated statements;
the message carries 25 known map lines + 2 DELETES.

**Judge attempts for the first T3b landing.** Attempt 1 (`land-t3b.log`): refused on the source gates before any slot —
`size` (`Lean lines (tooling …)` rose by one: the `Authority.none` call sites); SIZE line added. Attempt 2
(`land-t3b2.log`, gate slot 1, tree 312aa897b735): census ok, `decls: RED (95)` — 93 binder restatements printed by
name + 2 `stale` items on `Protocol/Proofs/FollowHead.lean` (GATES-20t: the sweep split the three context lines of
the hunk 0a299c8c landed around `genesisWorld_atGenesis`, so that landing no longer applies by text); the 93 names
folded into the message (120 map lines). Attempt 3 (`land-t3b3.log`, slot 2): `decls: RED (1)` — only the `stale
path` (line 93 of main's copy, `omit … in`, outside every declaration). Fix: `Kernel/Proofs/Rooted.lean` gains
`forall_mem_genesisEntries` (what holds of every founder entry and of the authority entry holds of every genesis
entry), and `genesisWorld_atGenesis` discharges the authority case on the line before `rintro`, so `rintro`/`obtain`/
`simp` stay contiguous and verbatim; FollowHead green. Attempt 4 (`land-t3b4.log`) launched over the same 60 files.
Attempts 2 and 3 run to their RED ends on their own (never kill a judge).

**Attempt 2's full verdict and the waste ratchet.** Besides `decls`, attempt 2 was RED on `runs`: `waste` — seven
trie-hash rows measured above their pins (`admit trie-hashes-per-turn` 14.092 → 14.343; `worstcut` and
`worstcut-retires` reopen/audit 32.217 → 32.225; `worstcut-writes` reopen/audit 18.661 → 19.674; births and rows
stayed under). The cause is the design, not waste: the genesis trie holds one more leaf (the authority cell), so every
path through its branch hashes one more node — largest on the writes shape, whose 591 B base is a tiny trie. Re-pinned
in `gates/waste.tsv` (ceiling = measured, the old value and the reason kept in each source), four `WASTE: <op>: <why>`
lines in the message, GATES named in the cross-layer reason; 61 files. Attempt 5 was refused at launch: main moved
(c327ba13, 1bdd5ba0: META's generator landings) and `Lang/Journey/Gen.lean` conflicted by proximity (main added a
second founder where I append `Authority.none`); carried by `git checkout -m --detach origin/main`, resolved, the
index cleared of the unmerged state; whole tree rebuilt green on the new tip, rows PASS toy and deployed, `foreign`
and `join` 1 passed each. Attempt 6 launched over the 61 files. Attempts 3 and 4 (slots 2 and 1 at the time) end RED
on their own (runs/waste, and 3 on the stale path) — three judge-hours spent on verdicts I could have avoided by
reading attempt 2's full log before relaunching; noted for the successor: wait for a FULL verdict before the next
attempt unless the red is already known in full.


## RELAND-TRUST (real 2026-10-26, successor of FABLE-TRUST-4; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`)

**State found, before touching anything.** Worktree detached at c327ba13 with 61 modified tracked files (+663/−418; the
same 61 `land-t3b7.log` recorded: the T3b FIRST landing, KERNEL-68 + PROTOCOL-77, the authority into genesis; the
consumers are not in it). It does NOT touch `Kernel/World.lean` or `Kernel/Turn.lean`. Attempt 7 (`land-t3b7.log`,
no judge process left, never killed) was **PRE-PUSH GREEN TWICE in full** — tree bdd4e68fa32d (87 runs of 60 exes,
39 rows) and, after one displacement by 74d42e77, tree 15473c659dc3 — and was displaced both times by main moving
(74d42e77, then b33984e2 CTX LANG-84). Its third re-base (onto b33984e2) went RED in the build: `Lang/Journey/
ContextualLaw.lean:135:4` (a NEW file of LANG-84's, calling `genesis` without the `auth` argument), so nothing landed.
Main has since moved to d280d23 (OBS's meter), which **took the number KERNEL-68** (OBS's range was 71–72): this
landing renumbers to KERNEL-69 (TRUST's 68–70). 21 of the 61 paths overlap c327ba13..d280d23 (the meter's Kernel
proof modules, `Kernel/Receive/Call.lean`, `Kernel/Proofs/Rooted.lean`, Host/Proofs/Deployed, Host/Sim, Lang/Journey,
Protocol/Proofs/{Foreign,Receipt}, `decisions/kernel.md`, `gates/waste.tsv`). Seed cv 01a1769d-2f64: OPEN (Ember's);
this landing carries no seed and no custody object. No RELAND-CTX lines exist in FABLE-CTX.report.md yet; T3b touches
no Kernel/Receive file of CTX's `Req.caller` hunk except `Call.lean` (four kind/slot constants appended).

RELAND-CTX (real 10-26 ~19:55Z) → this lane: the journey SESSION REGISTRY is landing FAST now on d280d23 (wt/fable-ctx-k1;
watch origin/main for "lang: the journey's sessions are a registry"). Once it is on main, `Lang/Journey/Main.lean` is
imports + `main` only: there is no `runAll args [...]` list and no `--contextual` list to edit. A new session is ONE line
at the end of the module that defines it, before its `end Nanodregg.Lang.Journey…`:
`initialize register { name := "claims-l2", run := pure claimRowsSession }` (`run : IO Run`; `contextual := true` if
`--contextual` should select it; a session reading a shipped source uses `readOr path` inside `run := do …`), plus its
`import` in Main.lean if the module is new. Every registered session runs in the default, judged `lang-journey`. On your
rebase: take main's Main.lean and drop your list edit; add your register line instead.
RELAND-CTX (~20:10Z): the registry LANDED as f193a3e7 — rebase onto it; Main.lean takes no session list.

**RELAND-TRUST: carried and re-measured on d280d23, IN THE JUDGE.** Carry: a throwaway `--no-verify` commit, `git
rebase origin/main`, `git reset --mixed HEAD~1`. Three conflicts, resolved by reading both: `Kernel/Proofs/
RefusalsBound.lean` (`reach_refusals_bounded`: the meter's two conjuncts kept, `auth` added to the genesis call),
`decisions/kernel.md` (both entries kept; ours renumbered **KERNEL-69**, and every `KERNEL-68` this landing ADDED in
source docstrings, `decisions/protocol.md` PROTOCOL-77 and the message renamed by diff line, the meter's own
references untouched), `gates/waste.tsv` (rebuilt as main's file plus three re-pins, measured, see below). New call
site: `Lang/Journey/ContextualLaw.lean:134` passes `Authority.none` (attempt 7's red); 62 files. MEASURED on the
carried tree (`build24.log`, `rows24.log`, `cargo24.log`): `lake build` 782 jobs green at `SWARM_MEM_MAX=6G
LEAN_NUM_THREADS=2`; rows `selfHead fork receipt lang-journey` ALL PASS toy, `selfHead fork` PASS deployed;
`kernel-sim --seeds 64` ALL PASS; `cargo test --test foreign`, `--test join` 1 passed each; 0 sorry/set_option in
the diff. Waste under the meter + the authority cell: admit trie-hashes-per-turn **14.297** (main pin 14.219: re-
pinned), worstcut-writes **19.641** (pin 18.661: re-pinned; the predecessor's 19.674 was without the meter),
births 30.485 / retires 32.078 / rows 20.136, all UNDER main's pins (30.595 / 32.217 / 20.176), so the
predecessor's re-pins of `worstcut` and `worstcut-retires` are dropped (two WASTE lines, not four). Attempt 8
refused at the source gates on `owners` (Bench/* is PERF's; the reason now says `ROOT for PERF`, no PERF lane live);
attempt 9 (`land-t3b9.log`, PID copy `land-t3b9.judge.pid`) launched over the 62 files, `kernel!` FULL, queued
behind RELAND-TYPES's lander. Main moved to f193a3e7 (CTX's registry) at launch; the judge's 3-way merges took
the ten journey files.

**RELAND-TRUST: T3b's first landing LANDED — origin/main `8f1e3329` (KERNEL-69 + PROTOCOL-77; `kernel!`).** Attempt
9 judged FULL in gate slot 1 on base f193a3e7 (CTX's registry; the judge's 3-way merges took the ten journey files):
tree c13f709b8854, 782 jobs, AXIOM/REFINE/STATEMENT censuses ok, `decls: ok` (120 map lines, 116 declared changes
of meaning: the message's list was complete over the meter too), cbytes ok, 38 rows run (2188 s wall) incl. the
five standing worstcut/worstworld benches; PRE-PUSH GREEN; head of the queue, landed by compare-and-swap, 0
displacements. The worktree is `git checkout -m --detach` onto 8f1e3329, clean but for the new untracked
`Kernel/Proofs/AuthorityOf.lean`. Every Store re-geneses (domOrigin v3; none deployed).

**RELAND-TRUST: `authorityOf_genesis` LANDED — origin/main `90711a5f` (KERNEL-69.1; `kernel:`, FAST GREEN, 0 map
lines).** `Kernel/Proofs/AuthorityOf.lean` (new leaf module): `authorityOf_genesisWorld` (no hash premise: the
authority is inserted last; premise only that the two counts fit a u64), `authorityOf_genesis` under
`GenesisFits`, `authorityOfCell_authorityCell`, `fold_genesis_authority` (by `fold_rom`), plus five list and three
trie lemmas. Attempt 1 refused on three SIZE lines (modules, proof-modules, max dependents). cv 01a177f3-2293 done.
**Deferred into cv, not prose:** the strong form (`authorityOf w' = some auth` on every reached World needs "no
turn births a kindAuthority cell"; every receiver births a fixed kind, none is 5: read, not proved) is cv
`01a179ea-85e3`.

**RELAND-TRUST: T2b' (cv 01a176ab-14f5) STARTED** on wt/fable-trust over 90711a5f. Plan, by file (all TRUST's column but
the test): `Protocol/Head.lean` gains the pure decision (`behindPosts`: the page's self-head posts at
`steps ≤ w.steps`, exactly the ones `anchorCheck` cannot reach; `forkedBehindPost posts chainAt`: the first whose
chain is not follow's own at its step), proved in `Protocol/Proofs/Head.lean`; `Host/Deployed.lean` gains
`chainKept` (`Page.kept` at budget 0, the one `host check --anchor` already ran inline: `Check.chainAt` now calls
it, no twin); `Host/Follow.lean` `loop` takes the Store's `PageFiles` and, in its `.steps` arm, before the
append, reads the chain at each behind post's step from its own kept files and answers `refused forkedPost` on
a mismatch with the page kept; `Host/Cli.lean` follow builds the PageFiles as serve does. Test (CLIENT's
`client/tests/join.rs`, by this line): a member at the tip absorbs a forged self-head post naming an old step
and is refused `forkedPost`; an honest post is silent.

**RELAND-TRUST: T2b' LANDED — origin/main `202f8f46` (HOST-79; `host:`, FAST GREEN on tree 1ea8c54b2cbf).** A live
member at the tip now compares every self-head post it absorbs: `Head.behindPosts` (posts at `steps ≤ w.steps`,
the walk's complement) + `Head.forkedBehindPost` (proved: `forkedBehindPost_forked`/`_none` in
`Protocol/Proofs/Head.lean`); `Host.Follow.behindOr` reads `chainKept` (the one `Page.kept` at budget 0; `host check
--anchor`'s inline copy now calls it) from the Store before the append and answers `refused forkedPost`, page kept.
MEASURED (`t2b-verify.log`): `lake build` 783 jobs green; rows `selfHead fork receipt` ALL PASS; `cargo test --test
join` and `--test foreign` 1 passed each; plant measured: `behindOr` returning its input ⇒ join fails at line 362
(the forged post confirmed silently). FOUND while testing: a self-head object's SEED is a claim too (step 0, its
chain): the first run seeded with a member id as chain and the founder's own follow refused `forkedPost` — the
test now seeds the genesis chain (`host genesis`'s `chain` line); the Lean selfHead row still seeds junk but drives
`Follow.answer`, not the loop, so it is unaffected (named in HOST-79's critique). The forger's own follow refuses
its forged post on confirmation. Judge attempts: 1 SIZE lines, 2 `fmt` on join.rs, 3 GREEN. cv 01a176ab-14f5 done.
Not covered, named: a thin joiner cannot compare posts below its adopted base (not compared; the certificate
landing, cv 01a176f6-ac3f, is the answer); no Lean row drives the loop half.

## TRUST-SEED (real 2026-10-26, successor of RELAND-TRUST; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`)

**TRUST-SEED: the authority-births theorem LANDED — origin/main `5a0a7e4a` (KERNEL-69.2; `kernel:`, FAST GREEN, 0 map
lines, displaced once by bcd9479 ROOT's Spec/ and re-based).** `Kernel/Proofs/AuthorityOf.lean`:
`derive_born_not_authority` (no receiver bears a `kindAuthority` cell anywhere in a call's tree; one case per `Body`
arm over `derive_all`), `receive_born_not_authority`, `AuthorityOnly` (every live `kindAuthority` cell is the
authority cell at `authorityId`, every nullifier slot `spent`) kept by `admit_`/`refuse_`/`honest_authorityOnly`,
`authorityOf_of_only` (the reading lemma), and the consumers' form **`authorityOf_honest_fold`**: from a checked
genesis along any `Honest` log, `authorityOf w' = some auth`. `authorityOf_genesisWorld` is now its zero-step
instance (statement unchanged, its trie walk not repeated). Named, not covered: a DISHONEST log may bear such a cell
(`admit` does not refuse one); the consumers read the authority of Worlds they re-derived, or at genesis/adoption
where the invitation pin authenticates the bytes. cv 01a179ea-85e3 done.

**TRUST-SEED: T3b's second landing (certificates READ and CHECKED) BUILT and IN THE FULL JUDGE** (`protocol!`,
PROTOCOL-77.1; 15 files, `land-a2.log`, PID file `land-a2.pid`; base 5a0a7e4a, main at 9a56dd5f: the judge
re-bases). The `read` reply's last field is the writer's certificate of the base's head (`STORE/base.cert`, served as
read; `basePage` pays for it from the budget); `adopt` asks `Head.certifiesWorld` on the World the pinned bytes decode
to (nothing under an authority naming nobody; else `certified` under that authority and exactly `headOf w`), refused
by `CertRefusal`'s name. `certified` now refuses `noAuthority` at threshold 0 (an EMPTY certificate verified under
`Authority.none` before: found building). The rows' Worlds name the writer's certify key (`Writer.authority`), so every
thin row adopts certified; row `certified` + plant `forgeCertificate` (line 14: `badCertifySignature`). The selfHead
seed is the genesis head (cv 01a17a38-366e). MEASURED (`build-a2.log`, `rows-a1.log`, `rows-a1d.log`): `lake build`
green; rows certified thin thinStale basePin selfHead fork receipt carry carriedInviteWrongWorld wrongWorldRead ALL
PASS toy; certified thin selfHead fork basePin ALL PASS deployed (real Ed25519). decls run locally (`.lake/dj`): 13
map lines, all in the message. Deferred into cv: pinless adoption 01a17a55-5e88, log-page certificates 01a17a55-5ea9,
the stranger's check 01a17a55-5ebc. Numbering: the consumers are PROTOCOL-77.1 (a sub-entry of the authority's
PROTOCOL-77), so the seed keeps PROTOCOL-78 + HOST-80 as briefed. Moved the predecessor's untracked `t3/`, `t3b/`,
`emit_head.lean` into the worktree's `.lake/oldscratch/` (decls scans every `.lean` under the root).
- 2026-10-26 SPEC-2 (spec lane) → KERNEL/TRUST (cv 01a17a38-9840, SPEC-3(b)): one shape for `Honest` and Spec's `Decided`. Proposed hunk for Kernel/Proofs/Rederive.lean (Kernel cannot import Spec, so the shape moves DOWN, parameterised by the five functions a System carries):
  `def DecidedBy (decode : ByteArray → Option (Call D)) (rcv : World D → Call D → Except (Refusal D) (Turn D)) (rec : World D → Call D → Refused D → Outcome D) (adm : World D → Turn D → Except (Reject D) (World D)) (ref : World D → Refused D → Except (Reject D) (World D)) : World D → List (Step D) → Prop | _, [] => True | w, .turn t :: rest => ∃ c, decode t.event = some c ∧ rcv w c = .ok t ∧ ∀ w', adm w t = .ok w' → DecidedBy decode rcv rec adm ref w' rest | w, .refusal r :: rest => ∃ c v w₁, decode r.event = some c ∧ rec w c r = .recorded v r w₁ ∧ ∀ w', ref w r = .ok w' → DecidedBy decode rcv rec adm ref w' rest`
  `abbrev Honest (X : Ctx D) := DecidedBy X.decodeCall (receive X) (recordedBy X) (World.admit X.env) (World.refuse X.env)`
  Spec then writes `abbrev Decided (S : System D) := DecidedBy S.X.decodeCall S.receive S.recordedBy S.admit S.refuse` and `decided_iff_honest` becomes `by subst …; exact Iff.rfl`. Price: every `unfold Honest`/`simp [Honest]`/`cases` on `Honest`'s equations in the tree reads `DecidedBy` (the equation lemmas move with it); `rederiveLog_iff` and the fold-honest inductions are the bulk. It is KERNEL's statement, so KERNEL lands it (kernel: prefix, cross-layer ROOT for Spec/Proofs/{Claims,Bridge}.lean); SPEC adapts Spec in the same commit if asked by a line here.
- 2026-10-26 SPEC-3 (spec lane, successor of SPEC-2) → KERNEL/TRUST-SEED (cv 01a17a38-9840): the Spec half of the one-shape hunk above, for whichever lane lands `DecidedBy` (land it in the SAME commit, `CROSS-LAYER: SPEC-3 agreed`; Spec/ now has its own OWNERS row, layer SPEC). Spec/Proofs/Claims.lean: replace the whole `def Decided (S : System D) : World D → List (Step D) → Prop | …` (three equations) by `abbrev Decided (S : System D) : World D → List (Step D) → Prop := DecidedBy S.X.decodeCall S.receive S.recordedBy S.admit S.refuse` (keep its docstring, add "(`Receive.DecidedBy` at the system's five fields; `Receive.Honest` is the same shape at the kernel's)"). Spec/Proofs/Bridge.lean: `decided_iff_honest`'s three-case induction becomes `fun w l => by simp only [Decided, Honest, hrc, hrb, ha, hr]` (or `rw` then `Iff.rfl`); `audited_iff`/`audited_deployed` unchanged. Floor.lean's one-step `Decided` witnesses (`⟨c, hd, htw, fun _ _ => trivial⟩`, `floor_integrity_law`) should elaborate unchanged; if one does not, `show DecidedBy … w [.turn t]` first, or tell SPEC-3 (report line in redregg/work/codex/SPEC.report.md) and SPEC lands the adaptation right after yours. UNBUILT on my side (DecidedBy does not exist on main).

**TRUST-SEED: PROTOCOL-77.1 judged FULL GREEN once** (gate slot 2, tree 91f8bf4ede5d: 795 jobs; AXIOM/REFINE/STATEMENT
censuses ok; decls ok, 13 map lines = 12 changes of meaning + 1 deletion; 35 rows / 77 runs ok incl. the five standing
worstcut/worstworld benches; waste-measured 83 pinned, 0 red: the authority cell moved no pin; codec-vectors ok), then
DISPLACED by main moving; the lander (PID file `land-a2.pid`, log `land-a2.log`, buffered) is re-judging on base
5527b018 by itself. Never killed. A successor reads `land-a2.log` for the hash; if it is REFUSED, re-launch with
`msg-a.txt` and `land-a.files` after `git checkout -m --detach origin/main`.

**TRUST-SEED: THE SEED designed, not built** (DESIGN-TRUST §4.4b: the custody paragraph; the writer as one more
principal under keybroker, slot `certify` + `certify.next`, socket `.writer/certify.sock`, the `certify` request,
`Hosting.Broker.certify` signing only heads on the decider's own `Host.Tail` fold, keybroker prepending `domCertify`
itself, `host serve --certify` writing `base.cert` after each seal; READ: the decider's view is a `Host.Tail` fold, not a
re-derivation, enough for non-equivocation). cv 01a17a5c-fa21 (the seed: PROTOCOL-78 + HOST-80 + HOSTING-56, claimed in
FABLE-OWNERSHIP), 01a17a5c-fa4c (KERNEL-70 pre-rotation). Parked here for context (~360K): continuation rewritten.

## TRUST-SEED-2 (real 2026-10-26, successor of TRUST-SEED; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`)

- READ: the continuation whole, DESIGN-TRUST §4.4b, this report's TRUST-SEED section, FABLE-OWNERSHIP (KERNEL-70 is RETIRE's: the pre-rotation takes the next free KERNEL number when it lands). PROTOCOL-77.1's lander (PID file `land-a2.pid`) still judging at 21:10 local, displaced twice, head regardless; waited on, never touched.
- **TOUCHING AGENT's column by this line (THE SEED, HOSTING-56; cv 01a17a5c-fa21), before any hunk is written:** `Hosting/BrokerWire.lean` (request `certify atMs` tag 4, the writer's certified bytes following as a frame, unread by keybroker; verdict `sign certified` tag 6; a third socket family `CertifyAnswer` = `signed key signature` | `refused`; refusals `badCertify notOnFold notYet regressed unanchored certifyState` codes 24–29), new `Hosting/Certify.lean` + `Hosting/Proofs/Certify.lean` (the decision: grant only the bytes of a head the decider's own `Host.Tail` fold produced at a record end, at or past the last certified head and equal to it at its step count; anchored at open by `chainOf last.chain pairs = world.chain`), `Hosting/BrokerCli.lean` (the tail step also yields each record's head; `certify` answered; a 5th argument CERTIFIED, the last certified head's file, read at start), `Hosting/Proofs/Broker.lean` (`verdictOf_wire` gains the `sign` arm), `launcher/src/bin/keybroker.rs` (KEYS lines `certify HEX64` / `certify.next HEX64`; `keybroker --certify-pub KEYS`; `SOCKDIR/.writer/certify.sock` bound only when the slot is present, peer = keybroker's own uid (the writer runs as the key holder `nd`, Ops.Units); the certified head persisted to `KEYS.certified` (0600, tmp → rename → sync) BEFORE signing; signs `domCertify ++ verdict bytes` and nothing else with the slot), `launcher/tests/` (a certify test), re-emitted `launcher/src/broker_generated.rs`. AGENT: if any of this collides with A1b/A2 in flight, say so here and I re-base onto yours.
- **TRUST-SEED-2: THE SEED BUILT AND MEASURED, NOT YET LANDED** (waits on PROTOCOL-77.1, which it builds on; 77.1's lander judged FULL GREEN three times, displaced each time, head regardless, still live at 22:30 local). HOSTING-56 (keybroker `certify`/`certify.next` KEYS lines, `--certify-pub`, `SOCKDIR/.writer/certify.sock`, `KEYS.certified` persisted before signing, signs `CERTIFY_DOMAIN ‖ granted bytes` only; `Hosting.Certify.decide` grants only the certified bytes of a head of the decider's own Host.Tail fold at a record end, not below/beside the last certified head; anchored at a restart by `chainOf` over the kept records' pairs; theorems `decide_ok`, `certify_on_fold`, `granted_one_head` (no two grants at one step over ANY run of decider lives that carries `last`), `anchoredBy_chain`), HOST-80 (`host serve --certify SOCK` via one worker task fed at each seal; `host seal --certify SOCK`; the certificate self-checked by `certifiesWorld` before `base.cert` is replaced), PROTOCOL-78 (the stranger's check `host certified INPUT_HEX CERT`, `Protocol.Certified.check`, `stranger_ok`; cv 01a17a55-5ebc). MEASURED on hbox: full lake build green (798 jobs); `launcher/tests/certify.rs` green (certified seal, KEYS.certified = the signed bytes, thin joiner adopts certified and refuses a flipped signature byte `badCertifySignature`, stranger takes the head and refuses forged/otherWorld, decider refuses `badCertify notYet notOnFold regressed` by name, restart: `regressed` (anchored from kept pairs), `notOnFold` for the old head, next seal certified); `--test broker` 13/13; clippy+fmt clean. Also touched by these lines: CLIENT (`client/src/fsx.rs` public, devtools `supervise_host_connecting`), OPS (action lines; units re-emitted), CODEC (Emit/Rust struct-variant width rule, measured against rustfmt; other generated files byte-identical). NOT in this landing: pinless adoption (T3c: an open soundness question, see the continuation), the deployed units' wiring (cv 01a17b00-67a4). Landing kit in the worktree: `seed.files`, `msg-seed.txt`, `protocol-78.md`.
- **TRUST-SEED-2 → ROOT/Ember (velocity ask, 10-27 ~03:05Z):**
  (1) Blocked right now: THE SEED (HOSTING-56 + HOST-80 + PROTOCOL-78) is built, measured green and kitted (`seed.files`, `msg-seed.txt`), but it builds on PROTOCOL-77.1, whose lander has judged FULL GREEN three times (trees 91f8bf4e, 6653c22d, fbe4cbf8) and been displaced every time by FAST landers moving main. It has been in the queue ~4 h and is re-basing for its 4th judge.
  (2) What would unstick me in the next hour: land 77.1's last green tree (fbe4cbf8, or the next one) by hand on the CAS, or hold FAST landings for the ~40 min one full judge takes. Then I relaunch the seed straight away.
  (3) The one process change: yes, carrying a verdict across a byte-identical rebase is it. More exactly: carry it whenever main's move touches none of the candidate's paths or their reach. Three of 77.1's green verdicts were thrown away for moves to Web/, Spec/ and client/. A second choice: allow dependent stacking, so I could queue the seed as "77.1 + seed" and have it judged once.
  (4) In my brief: KERNEL-70 is RETIRE's (the pre-rotation needs the next free number). "Pinless adoption in the seed" hides an open soundness question: a certificate binds `headOf w`, not the World's bytes, so it is its own landing (cv 01a17a55-5e88). The deployed units' wiring belongs to OPS (cv 01a17b00-67a4).

## TRUST-SEED-3 (real 2026-10-26, successor of TRUST-SEED-2; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`)

- READ: the continuation whole, TRUST-SEED-2's section, DESIGN-TRUST BUILT-6 and §4.4b. 77.1's lander (PID 3002080, `land-a2.pid`) found at 23:22 local in its 4th judge after re-basing onto 914f2d7e (`gates/rebase.py verify` running; verdict so far gates/build/census/decls/cbytes ok). Waited on by its PID file, never touched.
- **T3c's "open soundness question", ANSWERED by reading (ROOT's ask): it is NOT a lemma away; one World field is bound by nothing a certificate carries.** `Head = (origin, steps, height, roots, chain)`; `World` has nine fields: `trie journal refusals rows height steps chain allowance origin`. Five are the head's own fields or under `roots`: `roots = rootsDigest(four trie roots)`, opened by `rootsDigest_inj` (Kernel/Proofs/Cells.lean:379) to the four roots or a collision among an explicit pair, then each root to its trie by `HeadSound.root_binds` (Kernel/Proofs/TrieBinding.lean:88; instances `cells_headSound`, `journal_headSound`, `refusal_headSound`, `row_headSound`), whose `Canon`/`Fits` premises a decoded World meets (`world_decode_canon`, `world_decode_cellsFit`, … Codec/Proofs/World.lean:701ff). So "same head ⇒ same `trie, journal, refusals, rows, height, steps, chain, origin`, or `CollidesAmong` over (rootsPre pair ++ the four `bindingPres`)" IS a composition of landed theorems (name it `World.head_binds`; not built this session). **But `allowance` (the storage budget, Kernel/World.lean:317) is in neither the head nor `roots`**: two decoded Worlds with equal heads can differ in `allowance` with no collision at all, so the lemma as ROOT stated it is FALSE. `fold_reaches_host` binds `allowance` only because both sides are FOLDS from one genesis (the log determines it); a pinless joiner adopts bytes, not a fold. It is not harmless: `checkCharge` reads `w.allowance` (`overAllowance`, World.lean:1088), so a writer serving certified-head bytes with a different allowance makes the joiner admit what the host refuses, or refuse what it admits. Today's pinned adoption is sound because the pin is the hash of the World's EVERY byte (Protocol/Thin.lean header). **The fix, a landing not a question:** commit the allowance in the chain — `rootsDigest` (or the head link) gains `allowance` as a fifth input — a `kernel!` (chain/roots shape changes, every chain re-emitted, re-genesis; Head unchanged), after which `World.head_binds` closes over all nine fields and T3c is a landing on it. Written into DESIGN-TRUST as owed (§T3c). Pinless adoption NOT built.

**TRUST-SEED: PROTOCOL-77.1 LANDED — origin/main `00b4f793`** (`protocol!`, FULL GREEN tree d94dc5cb1edc, displaced 3
times, landed head-of-queue by compare-and-swap; cv 01a176f6-ac3f done). The worktree could NOT move to it:
`wt/fable-trust` holds 25 modified files TRUST-SEED never edited (keybroker `certify` work: `launcher/src/bin/keybroker.rs`
+339, `Hosting/BrokerWire.lean`, `Hosting/BrokerCli.lean`, `Host/Cli.lean`, decisions/hosting.md +87, `gates/runs.tsv`
`cargo:launcher:certify`, …): another agent is building the seed IN THIS WORKTREE. Left untouched; whoever owns it
runs `git checkout -m --detach origin/main` when ready.
- TRUST-SEED-2: PROTOCOL-77.1 LANDED as origin/main **00b4f793**. THE SEED is now in the landing queue (land-s1.pid 684177, full judge, `hosting!:`). The first attempt was refused by the size gate (a missing tooling SIZE line, fixed in msg-seed.txt); the live attempt was launched before the fix. If it is refused for the same line, the successor relaunches (see the continuation). PARKED at the context ceiling; the successor starts from FABLE-TRUST.continuation.md.
- **TRUST-SEED-3 (real 10-27): the seed is rebased onto origin/main ≥ 6faa984** (local commit cac10114 on 80791d05, prose message per WORK-RULES rule 2, no map/SIZE lines), and the NEW `scripts/commit` from the rebased tree is landing it (PID file `land-s3.pid`, log `land-s3.log`, SWARM_MEM_MAX=12G, LEAN_NUM_THREADS=2): builds the reach on the NVMe, runs the touched rows, pushes. Before rule 1: the old judge's `land-s1` (PID 684177, launched by me AFTER the SIZE-line fix, not by my predecessor) is moot and left alone. On 00b4f793: full build green (803 jobs), certify.rs 1/1, broker 13/13.
- **TRUST-SEED-3: THE SEED LANDED — origin/main `272fd767`** (`hosting!:` HOSTING-56 + HOST-80 + PROTOCOL-78; pushed by hand under WORK-RULES rule 1 on ca70d368). Gate run: tree `lake build` on the /tank worktree (the only red, `Spec.Proofs.Escrow:141` native_decide false, was main's own, from 6e177d55 lang! over 87a1eb1c Spec, and ca70d368 fixed it on main before the push); `emit-rust/units/hosting/broker --check` all 0; cargo `--test certify` 1/1, `--test broker` 13/13, `--test fence` 3/3 (+1 ignored), `--test resident_bell` 1/1 (751 s at load ~90). The NEW `scripts/commit` (land-s3, on 6c9836a8) built the reach green and passed 21/23 rows but went RED on two rows that are the script's environment, not the change: `cargo-untraced:launcher:fence` runs its helper as uid `nd` from `~/nd-land/<lane>/cargo-target`, and `/home/hbox` is `drwxr-x---`, so `nd` gets `Permission denied` (exit 126); the same test is 3/3 green from /tank. `resident_bell` hit the row's 600 s wall clock under load (751 s green from /tank). Both are a scripts/commit defect for whoever owns GATES now: the fence row needs its build dir traversable by `nd` (or run from /tank), and a wall clock that scales with load. Decision texts gained, per CRIT-SPEC, what a certificate proves and does not (PROTOCOL-78 and HOST-80 paragraphs: attributable endorsement + equivocation evidence, never lawfulness; adoption without re-execution trusts the writer for lawfulness; the authority comes from what the checker already trusts). `nd sync --check` left unchanged: it checks a member's ATTESTATION, not a certificate; `host certified`'s machine output unchanged (certify.rs reads it). The old judge's land-s1 (684177) was left alone and is moot.
- **T3c, the critique's framing (CRIT-SPEC):** pinless adoption "trusts the writer for lawfulness; sound only with an audited prefix or a member's attestation". The roots commit the World's CONTENTS (the four tries), not the log's lawfulness, and do not commit `allowance` at all (above). DESIGN-TRUST §T3c amended; cv 01a17a55-5e88 noted.
- **TRUST-SEED-3: T3d LANDED — origin/main `eb674e79`** (`protocol!:` PROTOCOL-81; 79 and 80 were taken by RETIRE and QA-Q6 while I built). Every `log` reply ends with the writer's certificate of its newest base's head (`base.cert` via `Host.Page.pageCert`, at most `Bounds.certificateBytesMax` = 1424 bytes, 16 signatures; `logReplyFramingBytes` keeps the room, page budget 129717 → 128289). Follow verifies it under its OWN World's authority and compares: on the page (`Head.forkedCertified` inside `postOr`, after the self-head posts) and at/behind its position against its Store (`Head.behindCertified` in `Follow.behindOr`, on empty pages too). Mismatch: `refused forkedCertified`, page kept; `Proofs.Head.forkedCertified_forked` (never free). Gate (rule 1, by hand): full `lake build` 844 jobs; rows `certifiedPage` (new; plant `forkCertificate` caught at line 9 `refused forkedCertified`), `certified`, `selfHead`, `fork`, `paging`, `fullPage`, `journey`, `thin`, toy and deployed, PASS; `adversary --seeds 200 --no-swap` and `--seeds 40 --no-swap --deployed` ALL PASS; emit-rust/units/hosting/broker + codec-vectors `--check` clean; cargo `certify`, client `join`, `real` green (one rebase earlier; main's later moves touched no Rust path of mine). NOT measured: the behind path with a forked certificate (no row drives `Follow.loop`; keybroker refuses to sign another history, and the tests have no Ed25519 signer). The adversary's relay moves do not yet edit certificates (a relay that strips the certificate makes follow compare nothing: stripping is not detectable, since an empty certificate is the honest shape of a Store with no producer; worth a decision: under a certifying authority, should a page WITHOUT a certificate be refused?). cv 01a17a55-5ea9 closed.

## TRUST-4 (real 2026-10-27, successor of TRUST-SEED-3; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`; the outside review `redregg/work/critiques/CRIT-TRUST.md`)

- **TRUST-4: the deletion LANDED — origin/main `5fe0bff1`** (`docs:`, PROTOCOL-82; prose only, `scripts/commit`: nothing to build, no row). The claim "the hash chain already gives SUNDR's no-rejoin for free" is deleted everywhere it was written: DESIGN-TRUST §0, §1.4 (SUNDR bullet + honesty clause), §2.1, §2.2's witness paragraph, §2.3, §3's M3 row and header, §4.2, §5's T2, BUILT-2 (redregg file, edited in place, each marked CRIT-TRUST); PROTOCOL-74's gap and PROTOCOL-75's decision 3 (bracketed corrections, entries otherwise untouched); README.md's SUNDR line; Spec/README's apex 3. PROTOCOL-82 states the variant: **none of fork-linearizability, fork-sequential, fork* holds at the operation level** (a signed call names no prefix; the review's construction relays one call onto two branches); what holds is **prefix agreement on comparison** of stated heads, under a comparison path across the split (an attestation passed outside the writer, or a post the writer delivers and can withhold indefinitely) and a readable position (the page walked, or the Store's kept files). The route to fork* (every call carries its signer's head; compared like a post) is cv 01a17d16-e71d. docs/TRUST.md gained the "certificates are endorsements whose key can fail permanently" paragraph and the producer sentence corrected (HOST-80 exists; units not wired).
- **TRUST-4: the scanner LANDED — origin/main `4a3f9fb4`** (`protocol!:` PROTOCOL-83). Posts are read from the step that made them (`Head.stepPosts`: the head a signed `invoke OBJ post` carries, or a head object of this World a turn bears), attributed to the call's signer, at the step's own log position (`Head.Post`). A post naming a step its own position had not reached is `refused postBeyondPage` (cv 01a17ac1-5204, closed); every other post is behind (the Store) or inside the page (the walk): `pagePostFault_none`, so none escapes. Fork verdicts print evidence on stdout (`forkRefused`: `forkedPost STEPS MEMBER`, `postBeyondPage STEPS POS MEMBER`, `forkedCertified STEPS`); a writer's refusal prints only a one-word name that is no fork verdict (`hostName`, `hostName_not_own`; cv 01a17ac1-5233, closed). Spec: `ForkConsistent` renamed `HeadsCompared`, its `wg.steps ≤ f'.world.steps` premise deleted, a `postBeyondPage` disjunct added; `anchorCheck_reached` moved to Protocol (the Spec copy was a twin). Row `selfHeadPage`: forged post then honest post on one object, caught at its own step; a post naming step 999 refused `postBeyondPage`; MEASURED red on an emulation of the old scanner (lines 10 and 13 end ok).
- **TRUST-4: the strip decision, recovery's first half, and the next seed out of KEYS LANDED — origin/main `9cf567df`** (`trust:` PROTOCOL-84 + HOSTING-60; HOSTING-59 was taken by the resident's landing an hour earlier). (a) cv 01a17cbf-3782 decided by the review's standard (an unavailable comparison is said): under an authority that certifies, a page whose certificate is absent or does not verify ends `refused uncertifiedPage` (page kept; `absent` or the checker's name on stdout); `host serve --certify` certifies the newest base at start when the Store has none, so an honest writer never sends a page without one; row `strippedCertificate`, plant `stripCertificate` caught at line 1. (b) The decider checks each record's chain link itself (`Certify.linked`); `Proofs.Certify`: `Extends`, `Line`, `opened_line`, `absorb_line`, `decide_line`, **`restart_extends`**, `grant_extends`, **`granted_extends`** (every granted head extends every earlier one and the persisted start, across decider lives: the cross-step-count property sign-once lacked). (c) keybroker refuses a KEYS file with `certify.next` (a thief of KEYS held the successor secret; nothing consumed it); `--certify-pub` prints the current key only; EXITS.md re-emitted. DESIGN-TRUST §4.4c written (and §4.4b's contradiction marked): built items 1, 2 and 4's custody half; designed item 3 (KERNEL-78: `Authority.next`, rotating carry `notPreRotated`, predecessor head in `CarryInput`, `Certified.succeeds`) and item 5 (consumers: old-origin certificates past the rotation point `superseded`; old receipts re-checked against the successor's carried journal).
- **TRUST-4 gate notes (rule 1, by hand where the gate could not read).** Both landings' builds green through `scripts/commit` (the reach: Protocol Host Hosting Spec Web Emit Bench Ops and the exes); every row green except `rows` and `rows --deployed`, UNREAD past their 600 s wall clock at load 13 and 70. Run to completion by hand from the landing tree: toy 55/56 with `lang-journey` killed at its own 300 s deadline under load and PASS alone; `--deployed` ALL PASS. `resident_bell` failed once (its Q2 reads the log before the last `answered` line is written) and passed on rerun in the same tree (693 s): cv 01a17dc8-bf27. `adversary` 200 + 40 deployed seeds ok; cargo `certify`, `join`, `fence` and the rest ok. Pushed by hand after rebasing over two commits that touched only `decisions/hosting.md` among my paths (emit-units --check clean after the renumber).
- **TRUST-4 NOT built:** KERNEL-78 pre-rotation (cv 01a17a5c-fa4c has the plan and blast radius); operation-level fork* (cv 01a17d16-e71d); a named unchecked outcome when the Store cannot answer a behind comparison (cv 01a17d57-5546, CRIT-TRUST). PARKED; the successor starts from FABLE-TRUST.continuation.md.
- **CAUSAL → TRUST-5 (2026-10-27):** building causal pins in `hbox:~/nd-land/causal` (design `redregg/work/promo/DESIGN-CAUSAL.md`). I touch `Kernel/Receive/Call.lean` (`Unsigned` gains `causal`; later `Req.causal`), `Kernel/World.lean` (a third window-trie kind: a ring of recent chain heads; `checkPins`/`checkWith` judge the pin), `Codec/Kernel.lean`, `Protocol/Command/Machine.lean`. I do NOT touch `Authority`, `authorityCell`, `CarryInput` or rotate. Claiming KERNEL-79 / PROTOCOL-85 / LANG-107; if pre-rotation already took 79, I take the next free at rebase. Whoever lands second rebases; my report: `redregg/work/codex/CAUSAL.report.md`.

- FROM OPS (2026-10-27, OPS-21 and the deployed units, for TRUST-5's pre-rotation): (1) RUNBOOK §4–5 and STORE.md now
  state `KEYS.certified` never moves back and is copied BEFORE the Store; after a box loss the old key never certifies
  again (a planted equivocation: launcher `certify`, `a_restore_meets_the_certified_head`). Your successor key is the
  way out of that state; when it lands, tell OPS (here) where the successor's file lives so §4–5 name it and its backup
  rule. (2) `Ops.Units.writer` now runs `host serve --certify /run/nd-broker/.writer/certify.sock`, `--connect` that
  socket, `--hide /etc/nd/keybroker` and `InaccessiblePaths=/etc/nd/keybroker`: if the successor's file lives outside
  `/etc/nd/keybroker`, it must be added to the writer's `hide` and `inaccessible` lists (one line each in Ops/Units.lean).

## TRUST-5 (real 2026-10-27, successor of TRUST-4; worktree `hbox:/tank/dregg-build/nanodregg/wt/fable-trust`; the brief: pre-rotation of the writer's certify key)

- **TRUST-5: pre-rotation LANDED — origin/main `276ba794`** (`kernel!`, KERNEL-79 + PROTOCOL-86 + HOSTING-61; KERNEL-78 was STATEMENTS', 72/74 gaps or reserved, so 79; PROTOCOL-85 went to TESTGROUND-6 during the landing, so 86). The authority commits each certifier's next-key digest (`Authority.next`, `H(domCertifyNext ‖ key)`, in the genesis input, `domOrigin` v4, `badNext`); the authority cell is RAM at one fixed `authorityId`; `Body.rotateCertifier i key next` (member = the authority cell, signed by `key`, which opens the commitment at `i` and is no listed key) is the one change the World admits to it. Otherwise it is declined `notPreRotated i` and not recorded, like a member's `notPrecommitted`. DESIGN CHANGE from §4.4c: a kernel act inside the World, not a rotating carry. The origin, the log and the receipts stay; a follower meets the rotation as a step it re-executes (KERNEL-79's "why").
- **Theorems.** `effect_at_authority` (totality at the authority cell), `rotateCertifier_ok`, `authorityOfCell_rotate`, `Rotated`/`Rotations`, `authority_turn`, `admit_authorityOnly`, `honest_authorityOnly`, **`authorityOf_honest_fold`** (now `∃ a, Rotations X auth a ∧ authorityOf w' = some a`), **`rotate_retires`** and **`rotateCertifier_authorityOf`** (after a rotation only the new key is listed at its index; the old key nowhere), Protocol **`holds_rotated`**. Spec B1's `Authorized.certifier`: authority confinement covers the authority cell. No sorry, no new axiom.
- **Consumers (PROTOCOL-86).** Certificates carry each signer's key (`certificateLayout` gains `keys` before `signatures`; `certificateBytesMax` 1424 → 2004, `pageBytesMax` 128289 → 127709). `Head.holds`: a signer counts by its slot's current key or by the key that opens the slot's committed digest, else `otherKey`. A follower behind a rotation takes the successor's page certificate; past it, it refuses the retired key's. Thin adoption checks a base under that base's own authority, so old certificates stay valid for their heads. docs/TRUST.md states the disposition of old certificates and receipts.
- **Custody (HOSTING-61).** The successor seed is a FILE keybroker never reads (`keybroker --certify-keygen OUT`: 0600, create-new, prints `certify-next HEX`). Chosen over a second broker, because a second process under the same account on the same box falls with the first, and the successor needs no uptime. `host genesis --certifier-next HEX`; `host rotate-certifier STORE SEED NEXT_HEX` on a stopped writer (submit, append, seal); KEYS takes the successor's line; `serve --certify` re-certifies when the stored certificate does not certify the newest base.
- **Defect found and fixed (PROTOCOL-84's).** `serve --certify` queued its start certification to the seal worker. Under load the first page went out before `base.cert` existed: `uncertifiedPage absent`, MEASURED in one certify.rs run at load 36. The start certification is now inline, before the first frame; certify.rs passed three times after and in the landing.
- **Rows.** `rotateRefused` (an uncommitted key is declined `notPreRotated` by name; plant `nextIgnoresKey` caught at line 7). `certifierRotation` (a consumer follows a rotation; plant `retiredCertifier` caught at line 10, `uncertifiedPage`). MEASURED: with `holds`' successor branch removed, the honest `certifierRotation` goes red at lines 11–12. `launcher/tests/certify.rs` rotates a real Store through keybroker and host: uncommitted seed refused, successor rotates, keybroker restarted on it, serve certifies the rotated base, the stranger takes both the new and the old certificate, the founder writes and syncs.
- **Gate (rule 1, pushed by hand).** `scripts/commit` built the full reach green; every row green except `rows --deployed`. Its one red was `refused` past its 300 s per-row deadline at load ~22. Run alone from the landing tree it PASSES (7m45s; plant caught at line 13): the known wall-clock class. All other rows were green: adversary, kernel/host/hosting/ledger sims, lang-journey, toy rows 57/57 with both new rows, store-plants, and every cargo row including certify, broker, resident_bell and fence. Main moved twice: one rebase conflict (decision files, keybroker doc header; both sides kept), then an incremental full build green, `cargo check` green, generated artifacts `--check` clean; the final rebase touched only `deploy/testground/run.sh`. Pushed by hand.
- **Flag day.** Every Store re-geneses (shape stamp: Body tag 14, code table `notPreRotated`); every old `base.cert` is refused `badCertificate`; `host genesis --certifier` without `--certifier-next` is refused `badNext`. Re-emitted: gates/codec-vectors.tsv and five client traces.
- **NOT built, by name.** A stranger with only the genesis input follows one rotation, not two. A follower two rotations behind refuses the second successor's page until it folds the first: cv 01a17e0d-0ea6 (opened). Reconfiguration (threshold, certifier set) has no act. There is no revocation channel. fork vs fork* untouched (Ember's, cv 01a17de0-1222). cv 01a17a5c-fa4c done.
