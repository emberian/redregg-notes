# LEDGER-LOG — BUILD-LEDGER continuation (nanodregg), written 2026-10-17

Brief: /Users/ember/dev/redregg/work/nanodregg-scout/ASSEMBLY-ledger.md §6 (FIRST BUILDER BRIEF). Charter:
~/dev/nanodregg/CHARTER.md. Since 10-17 **main lives on hbox**: recipe in
~/dev/redregg/work/MIGRATE-HBOX-LOG.md "RECIPE FOR THE LANES". Worktree `hbox:/tank/dregg-build/nanodregg/wt/ledger`.
The Mac worktree is DELETED; the Mac builds nothing. Subject prefix `kernel:` (gates/OWNERS: Kernel/ → KERNEL;
`ledger` is a registered layer). Decisions: decisions/kernel.md LEDGER-1..4.

## Tools of mine on hbox (/tank/dregg-build/nanodregg/logs/)
- `ledger-rebase.sh`: carry tracked edits onto current main (patch, reset, checkout main, apply --3way); prints clean/CONFLICTS.
- `ledger-land.sh MSGFILE CROSS PATH...`: rebase + scripts/commit, retrying while main moves (CROSS "" = none).
  Run it with nohup + `ledger-land.pid`; wait with a deadline loop on `kill -0`.
- Never put backticks in a remote unquoted heredoc (7e94bf9 lost its code spans that way; fixed 477a682):
  write python/text files on the Mac scratchpad, scp them, run them.
- Plants: back up the file, mutate, build module + kernel-sim, restore the backup (never `git checkout --` a file
  that holds uncommitted work).

## On main (mine)
- 9e6fd1c LEDGER-1: `sealTurn X c creates (effects : List (D × Act)) (nullifiers : List D)`, `duplicateEffect`
  (met by `probeSeal`, a direct seal probe; ROOT accepted that for receiver-unreachable refusals).
- b2d60e7 `Codec.Stream.i64` + `i64_lawful` (cross-layer; CODEC-2 reviews).
- c023469 LEDGER-2/3: `Discipline.value` (Kernel/Value.lean: keys 8/9/10 denom/balance(i64)/floor(u64);
  Flow, flowsOf, sumBy, accumulate with Bounds.denomsMax 8, denomBytesMax 64). World.admit: postWrite's `.value`
  branch → checkValueCell (valueMalformed, belowFloor); Post.flows from touchCheck's one lookup; checkValue after
  touches (notConserved, floorNotConserved unless the turn bears the denom, overBound denoms). Spec measures
  cellsSum/entrySum/World.sumOf/valueSum/floorSum/outstanding in World.lean.
  Proofs/Value.lean: admit_value, fold_value, admit_floors, fold_floors, admit_floorOk, fold_floorOk,
  outstanding_le_floors, outstanding_le_cap, admit_birth, admit_floorsBorn, admit_not_born, fold_floors_held,
  cellsSum_noValue, floorOk_noValue. Receivers (Kernel/Receive/Ledger.lean; kindAccount 6): issue cap (ONE cell,
  the well: its own id is the denomination, floor = cap, overflow past 2^63), account asset (no well pin),
  transfer src dst amount via once (ownerAuthority .mutate on src; sameAccount zeroAmount assetMismatch overflow;
  once → nullifier H(domOnce, src ‖ key)). walk/principalOf/ownerAuthority/slotsOf MOVED to
  Kernel/Receive/Authority.lean (KERNEL-5 now owns further changes there). Proofs/Ledger.lean: transfer_authorized,
  transfer_once, dispatch_value_born, transfer_exact, admit_written, accountCell_value.
- 7e94bf9 LEDGER-4: `credit well acct amount via` (floor transfer out of a WELL under its owner's authority;
  notWell new). credit_authorized, credit_exact, sealed_two_writes (shared with transfer_exact).
- Sim (Kernel/Sim/Gen.lean): independent model (wells, accounts, balances, floors, onces), scanValue after every
  step, ledgerAct arms 0 issue / 1 account / 2 transfer / 3 credit, probeValue (forged turns: notConserved,
  floorNotConserved, valueMalformed, overBound). kernel-sim --seeds 64 ALL PASS toy and deployed.
- Plants recorded in each commit message and in LEDGER-2/3/4.

## Open (in ROOT's order, 10-17)
1. PROTOCOL-5 (a4cd717157c6d458e) has the well/pay re-cut message (verbs issue/account/transfer/credit are
   PROTOCOL's; the checkValue plant lives in kernel-sim, the row needs its own). Answer its questions.
2. The waste row `seal bytes-per-appended-byte` rose 1.708→1.720 (seed 1) at c023469; measured and handed to
   KERNEL-5/HOST-5 (appended bytes unchanged; the base grew). Not re-pinned by me.
3. D5 (methods post value): LEDGER-5 PROPOSED on main (fe3d5a3). LANG-3 ACCEPTED with two amendments, recorded
   in LEDGER-5 at 1b4135c: `calls` is a fixed-arity row of 8 `opt callTy` slots (no lists in the core), `callTy`
   generated from KERNEL's Body codec with a decode theorem; install check `forwardsCalls` is partial, the guard
   is principal = calling object. LANG-3 retired; LANG-4 (a2fbb4419dc4a69aa) writes LANG-22 and builds LANG's
   half. KERNEL-5's answer on (b) object-as-principal, (c) Draft + one seal, (d) `account … (owner)` is STILL
   PENDING. Build order: KERNEL-5 (Body codec, Program.run signature, Draft) → LANG-4 (callTy, methodTy,
   runMeasured calls, visit_distinct) → LEDGER escrow (a package + kernel-sim arms + a PROTOCOL row request). Waste row: closed (HOST-5
   re-pins: D2's base shape stamp). LANG-21 (decisions/lang.md) already decides "effects as data, visited depth
   first, callee principal = calling object". LEDGER-5's direction: effects ARE `Body` values (one call
   language, law 1; LANG-21's Effect{target,method,args,budget,via} = Body.invoke), each derived by its own
   receiver with principal = the calling object; receivers return a Draft {creates, effects, nullifiers} and
   `receive` seals once (born-id offsets per draft); `account asset (owner : Option D)` so a depositor can open an
   account OWNED by the escrow object (harmless: floor 0, only its owner can debit). Escrow = a package whose
   release/refund methods return [transfer escrowAcct → party]; double payout is impossible by the kernel's floor 0.
3b. LANG-4 (a2fbb4419dc4a69aa) ANSWERED LEDGER-5 "yes with changes", to be decisions/lang.md LANG-23:
   exact Lang signatures (optTy, rightTy, rightsTy fixed-arity 4, callTy (account{asset, owner opt},
   credit{acct, amount, via, well}, grant{grantee, parent, rights, target}, invoke{args, budget, method, obj, via},
   transfer{amount, dst, once, src, via}), callsTy c0..c7, methodTy codomain record {calls, state}; Lang/Call.lean
   callData/bodyOf/callsOf + callsOf_callable/callsOf_length/round trip; runMeasured returns calls). KERNEL-5 side
   it expects: `Program.run … : Except (Refusal D) (Slots × List (Body D))`, `Bounds.callsMax 8`, callDepthMax,
   treeTicksMax, `Refusal.notCallable` kept as the kernel's own assertion (plant: a stub program returning a
   `create`), Draft, and visit_distinct is KERNEL-5's. WITHDRAWN: LANG-3's `forwardsCalls` install check (it
   refuses a legitimate object-owned treasury; LANG-4 flags it to ROOT) — so LEDGER-5's text "the LANG check is
   a second line" must be updated to "there is no LANG check; the guard is principal = calling object +
   KERNEL-25's owner-gated invoke". callTy is hand-stated in Lang, guarded by round-trip theorems (not generated).
   ESCROW GAPS for LEDGER to close before the package:
   (i) FUNDING: deposit's calls run as the escrow object, so the depositor must first grant the ESCROW OBJECT
       `mutate` on its account and deposit emits `transfer depAcct acct amount (via := some g)`; otherwise an
       unfunded deposit sets phase=held and both release and refund are belowFloor (wedged). Critique: mutate is
       the whole balance; an amount-bounded right would be KERNEL's.
   (ii) BINDING acct: a method reads no other cell, so the escrow cannot learn/check its own account id; an
       argument-supplied acct lets a depositor name its own account. Options: a canonical account id per
       (owner, asset) (a new bornId rule, KERNEL's) so the package derives it, or acct fixed in the seed by a
       creator who opened it with owner = escrow (checked off-chain). Decide in LEDGER-6 with both critiques.
   (iii) nested invoke `args : bytes` can only forward held bytes until LANG's bytes prims (ID-4).
4. Taste forks left to Ember: sweep/decay/commons (brief: do not build); reclaiming unused credit (whose authority).
5. D6 (data-object laws removable by their owner) is KERNEL/LANG's; LANG-19 (occasion relaw) partly answers it.

## LEDGER-2 (spawned 2026-10-17 ~11:20Z; successor of BUILD-LEDGER)
Prefix: commits are `kernel:` (gates/owners.py has no `ledger` prefix; `kernel:` owns LEDGER paths). Message files
in hbox logs/ledger2-*.txt; Mac scratch .../scratchpad/ledger2/.
### Landed
- 5c8353f `decisions/ledger.md` (new): LEDGER-5 CLOSED (accepted/amended/owed per layer), LEDGER-6 escrow:
  account = accountId e asset (opened top-level before deposit; pinned view forbids same-tree birth);
  funding = depositor's v0 mutate grant to e, deposit emits transfer(once := self) in the same tree;
  CORRECTION: the floor does not prevent double payout (top-up) — release/refund share once key "payout"
  so transfer_once gives at-most-once; lifecycle theorems escrow_absorbing / escrow_one_payout.
### Asked (awaiting answers)
- KERNEL-5 (aaf0617c549722c7a): checkGrantee admits a live programmed object; Req.self; D5 theorem names
  (effect_as_signed, visit_distinct, draft_cells_distinct, account_keyed, Draft restatements); re-entry name.
- LANG-4 (a2fbb4419dc4a69aa): reqTy `(self bytes)`; builtin accountOf with meaning theorem.
- PROTOCOL-5 (a4cd717157c6d458e): 4 verbs issue/account/transfer/credit; well/pay row lines + plants (LEDGER-6 (f)).
### Open, in order
1. pay/well rows PASS — blocked on PROTOCOL-5's verbs (its layer); answer its questions.
2. D5: start only after KERNEL-24 lands on main (main at 5c8353f had KERNEL-24 NOT landed). Move LEDGER-1..5
   from kernel.md into ledger.md in the D5 commit (it is cross-layer anyway).
3. Escrow package + sim arms + plants (top-up; unfunded deposit) + PROTOCOL row request, after lang!.
### Answered
- KERNEL-5 (10-17): checkGrantee = member | World | LIVE kindObject cell, else refused by name; Req.self accepted
  (set in Derive); re-entry refusal `revisited obj`; theorem list accepted, effect_principal dropped;
  account_keyed MUST state injectivity up to collision: accountId a s = accountId b t → (a,s) = (b,t) ∨ HashColl.
  KERNEL-5 messages when KERNEL-24 is on main (changes Unsigned.world, World.origin, genesis, receive's first line).
- LANG-4 (10-17): Req.self YES (reqTy `(self bytes)` in lang!); accountOf builtin NO (digest-parametric Eval,
  kernel-decide teeth die under a real hash). Counter accepted, narrowed: LEDGER-7 landed 7229d95 —
  `AcctRef = well asset | of owner asset` in transfer src/dst + credit acct; resolve_well/resolve_of in D5;
  told KERNEL-5 and LANG-4. PROTOCOL verbs then spell refs `of:OWNER:ASSET` / `well:ASSET` (tell PROTOCOL-5 with D5).
- PROTOCOL-5 (10-17): builds the 4 verbs ONCE after D5: `issue CAP`, `account ASSET [--owner O]`,
  `transfer SRC DST AMOUNT [--via G] [--once HEX]`, `credit WELL ACCT AMOUNT [--via G]`, refs well:ASSET / of:OWNER:ASSET
  (hex id or row binding); re-cuts well/pay on my lines (plants skipJudge at over-cap / second --once).
  OWED BY ME: message PROTOCOL-6 (abd8f012f13228e0b; PROTOCOL-5 retired, briefed by ROOT) the D5 sha when it is on main.
### Successions (ROOT, 10-17): KERNEL-6 = aa36c7021124d8bdb (reviews D5 statements; trie port AFTER my D5a);
LANG-6 = a0e14827e8b076d95 (send it the D5c sha; LANG-5 retired, agreed (e)); PROTOCOL-6 = abd8f012f13228e0b (send D5 sha).
D5 split: D5a explicit create ids (+notContentId, KERNEL-6's conditions: refuse before writing, tooth in
kernel-sim plantedArms, freshness stays `w.cells.contains c`); D5b keyed accountId + AcctRef; D5c Draft/actor/tree.
- LANDED 5b87949 D5a (Turn.creates : List (D × Cell), bornAt, Turn.born, createdIds t, notContentId + RomContent
  admit/fold/genesis/empty, probeRom arm rom-id:notContentId). Tools: hbox logs/ledger2-*.txt msgs; Mac scratch
  .../scratchpad/ledger2/src is a local git mirror of the files I edit (push.sh tars changed files to wt/ledger);
  RESYNC it from hbox before each sub-landing. Landing: nohup ledger-land.sh MSG CROSS PATHS, pid ledger2-land.pid.
  scripts/commit needs `SIZE: <row>: <why>` lines for every risen SIZE row.
- LANDED 56ff26f decisions/ledger.md LEDGER-8 (D5 split; D5c shape: Draft, At{actor,base}, Req.self, visitor refusals
  notCallable/callTooDeep/revisited/tooManyCalls, one tick pool with Program.run returning ticks used (ASKED LANG-5), overTicks).
- D5b WRITTEN + GREEN on 5b87949, KERNEL-6 vacuity OK, HELD for KERNEL-6's World port (it messages when landed).
  Saved: hbox logs/ledger2-d5b.patch (tracked diff) + logs/ledger2-LedgerDeployed.lean (new file); Mac scratch src git
  commit "D5b deployed keyed"; paths in scratch d5b-paths.txt. Plants: account at bornId ⇒ 59/64 red; .well check
  off ⇒ 18/64 red. After port: rebase (proofs use w.cells → w.trie/w.live E), rebuild, sim, land with SIZE lines.
- ROOT 10-17: KERNEL-6 retired; KERNEL-7 = ac9b1fb8228590424 lands the port (green in wt/kernel) then reviews D5b/D5c.
  D5b statements were already vacuity-OK'd by KERNEL-6 (incl. deployed_account_keyed ask, done). Send D5c statements to KERNEL-7.
- D5c IN PROGRESS in hbox wt/ledger ON TOP of D5b (uncommitted). Done: Call/Bounds/Authority/Ledger receivers/Derive
  (Draft, At, Walk, Sub, callStep, deriveCalls, invoke w/ visitor, stepped, dispatch, tree, poolOf, derive), Lang glue,
  Proofs: Receive, Tree (new: invoke_ok, tree_succ, effect_as_signed, foldCalls_all, dispatch_all, tree_all, derive_all,
  Grows, visit_distinct, stepped_draft), Authority, Rooted (derive_born, receiveWith_born). TODO: Ledger proofs, Sim
  (stub program calls + arms + plants), Lang/Hosting proofs, Protocol Machine, measure treeTicksMax.
- ROOT: LANG-6 = a0e14827e8b076d95 gets the D5c sha (LANG-5 retired).
- D5c WRITTEN + GREEN (full build 340 jobs; kernel-sim ALL PASS toy+deployed; host/hosting/lang-journey pass; rows
  INCOMPLETE 3 pending, pre-existing). 8 plants all red (logs/ledger2-plants-c.out). Statements sent to KERNEL-7.
  Patches on hbox: logs/ledger2-d5b-only.patch (applies to main ca798ba, checked) and logs/ledger2-d5bc.patch
  (D5b+D5c vs 56ff26f, `git diff HEAD`). Mac scratch git: 66afa66 = D5b, a7349a8 = D5c.
  ⚠ scratch base is 5b87949; files main moved since (Loopback!) must be refreshed from hbox before pushing edits.
  LANDING PLAN after port: reset wt/ledger to main, apply d5b-only (3way), build, land D5b (SIZE lines, cross-layer
  Codec); then apply d5bc patch 3way onto new main, fix port conflicts (w.cells → trie API), build, sims, land D5c;
  then send sha to LANG-6 (a0e14827e8b076d95) and PROTOCOL-6 (abd8f012f13228e0b); ROOT on each landing.
- KERNEL-7: port green, awaiting CODEC-3 review; will send sha, then review D5c statements IN the rebased tree. Port: w.live E c, w.taken E c, w.isSpent E n, no cells/spent (World.cellIds), Canon/Slotted premises — discharge with existing genesis_/admit_/fold_ theorems, NO new undischarged premises.
- LANDED e8077f8 D5b (rebased on port 7c43273). D5c rebased on e8077f8 in wt/ledger (uncommitted; logs/ledger2-d5c-rebased.patch),
  green (362 jobs, all sims), 8 plants red again. Sent to KERNEL-7 for in-tree review; land on its OK.
- D5c commit msg ready: hbox logs/ledger2-msg-d5c.txt (add SIZE lines when pre-push asks; cross-layer: Lang glue, Hosting proof, Protocol Machine/Command/Loopback).
- KERNEL-7 OK'd D5c, then retired; KERNEL-8 = a3757d866eb64f133 confirms the rebase. D5c rebased onto 5105d8b (incl KERNEL-31
  2618fe3), clean apply, green (378 jobs, sims). Changes since review: Body.isInvoke moved to Call.lean (closure C3);
  waste row admit hashes-per-nullifier re-pinned 2.695→3.634 with WASTE line (workload: payout nullifier; 2.666 without it).
  Msg ready: logs/ledger2-msg-d5c.txt (SIZE+WASTE). Land with: nohup bash logs/ledger-land.sh MSG "CROSS" $(git diff --name-only HEAD) Kernel/Proofs/Tree.lean
  (ssh with < /dev/null; wait via pid loop ≤ 9.5 min per call). cv task 01a14a03 = ticks-spent theorem (KERNEL-7 follow-up).
- LANDED c3c7aa3 D5c (D5 complete: 5b87949, e8077f8, c3c7aa3). Waste row re-pinned w/ source text rewritten (KERNEL-7/8 accepted).
  Sent sha to LANG-6 (lang! day) and PROTOCOL-6 (verbs + well/pay rows). cv task 01a14a03 open (tick exactness).
- PENDING: doc move LEDGER-1..5 kernel.md → ledger.md, diff uncommitted in wt/ledger, awaiting KERNEL-8 OK.
### Open, in order (after D5)
1. Escrow package (LEDGER-6): after LANG-6's lang! lands (callTy/acctRefTy/reqTy self). Package text = LANG; theorems
   escrow_absorbing/escrow_one_payout; sim arms (top-up plant, unfunded deposit); row request to PROTOCOL-6.
2. pay/well rows PASS: PROTOCOL-6 builds verbs on D5.
3. cv task 01a14a03.
- LANDED 0b8e417: LEDGER-1..5 moved into decisions/ledger.md (KERNEL-8 agreed).
- LANG-6 retired; LANG-7 = ac6dbe9957c6ff484 does lang! day first. Sent it the escrow signatures (state, 3 methods,
  calls, refusal names notOpen/notHeld/settled/notParty, needs acctRefTy, reqTy self, bytes eq). Awaiting confirm + sha.
  Ownership of escrow package path: asking ROOT (proposed Ledger/Escrow.lean).
- HOSTING-3 convention for world/escrow/: text printed by Lang.Print.package from the Lean package (writer mode in my sim, like hosting-sim --write-text), byte-compare gate in the sim (cf Hosting/Sim/Journey.lean ~226), round-trip theorem like lifecycle_text_reads via readPackage_checked; re-emit when LANG re-ids.
- GATES-2 lands owners.py ledger: prefix + OWNERS rows itself (sha pending). LEDGER-9 text uncommitted in wt/ledger decisions/ledger.md; land it as ledger: AFTER GATES-2's sha. lean_lib Ledger goes with the first Ledger/*.lean.
- LANDED 65ea019 (first ledger: commit): LEDGER-9 ownership ruling. GATES-2's cb99f02 registered ledger: prefix + OWNERS rows. ALL LEDGER commits now use ledger:.
- LANG-7 confirmed escrow signatures (callTy/acctRef/reqTy exact text in its msg; beq prim; lawDenied pkg "LAW: <name>" is how names reach wire; law sees old/new/req not calls). My theorems: escrow_absorbing, escrow_law_payout_once, escrow_calls_payout ⇒ escrow_one_payout; kernel once = second line. Awaiting lang! sha.
- PROTOCOL-6 landed verbs + well/pay rows PASS (4669195, PROTOCOL-32; my skipJudge plant corrected). Task 2 DONE. Recorded in LEDGER-6 (f).
- PROTOCOL-6 landed verbs + well/pay rows PASS (4669195, PROTOCOL-32; my skipJudge plant corrected). Task 2 DONE. Recorded in LEDGER-6 (f). Rows 17 PASS 1 PENDING (bounty = escrow).

### LEDGER-2 HAND-OFF (2026-10-17, at context ceiling ~620K) — successor LEDGER-3 starts HERE
State of main (relevant): 9d217cb = LANG-7's lang! day (LANG-33). D5 done (5b87949 / e8077f8 / c3c7aa3). Rows: 17 PASS,
1 PENDING (bounty = escrow). Prefix: ALL LEDGER commits are `ledger:` (cb99f02 / LEDGER-9). Worktree wt/ledger is clean at
an older main: `git checkout --detach main` first.
NEXT WORK = the escrow package (LEDGER-6, decisions/ledger.md; agreed signatures with LANG-7):
- Paths (ROOT ruling LEDGER-9): Ledger/Escrow.lean (package as Lean data/generator, via Lang.Std: Std.pkgOf methods are
  (label, A, ks, term); Std.methodWith S A slots fields), Ledger/Proofs/Escrow.lean (theorems), lean_lib Ledger entry in
  lakefile in the SAME commit as the first Ledger/*.lean; shipped text world/escrow/Escrow printed by Lang.Print.package
  (HOSTING-3's convention: a writer mode in my sim + byte-compare gate, cf Hosting/Sim/Journey.lean ~226 and Hosting/Package.lean,
  round-trip theorem like lifecycle_text_reads via LANG's readPackage_checked; re-emit when LANG re-ids).
- Read 9d217cb for exact types (NOT LANG-23 prose). LANG-7's message: methodTy S A ks; callsTy ks = rec {c0 : optTy ks[0],..};
  T := Lang.callOf ["transfer"]; each escrow method ks = [T]; c0 = someCallT T (.inj T "transfer" (.record [("amount",…),
  ("dst", acctRef), ("once", opt), ("src", acctRef), ("via", opt)])); acctRef = .inj acctRefTy "of" (.record [("asset",…),("owner",…)]).
  reqTy fields agent, notBefore, occasion, principal, self, validUntil. Prim `beq` on bytes; #hex literals. Cite run_calls,
  runMeasured_calls_slots, callData_conforms (Lang/Proofs/Call.lean).
- Package: state rec {amount nat, arbiter bytes, asset bytes, beneficiary bytes, depositor bytes, phase sum{held,open,refunded,released}}.
  0 deposit A=rec{grant bytes}: law requires agent=depositor ∧ open→held; c0 transfer src of{depositor,asset} dst of{self,asset}
    amount, via some grant, once some self.
  1 release A=rec{}: agent ∈ {depositor, arbiter}, held→released; transfer of{self} → of{beneficiary}, via none, once some #7061796f7574.
  2 refund A=rec{}: agent ∈ {beneficiary, arbiter}, held→refunded; same with dst of{depositor}, SAME once "payout".
  Rules in the package LAW over (old,new,req) casing req.occasion (invoke m); refusals reach wire as lawDenied pkg "LAW: notOpen"
  | notHeld | settled | notParty (first token after "LAW: ").
- Theorems (agreed with LANG-7): escrow_absorbing (from released/refunded the law refuses every invoke `settled`);
  escrow_law_payout_once (along law-admitted states ≤1 held→released|refunded step); escrow_calls_payout (methods 1/2 emit
  exactly one transfer from of{self,asset}; method 0 none from it) ⇒ escrow_one_payout. Kernel's shared once key = second line.
- Sim/journey arms (Lang journey-style, with LANG's real program): fund via depositor→escrow mutate grant (v0; amount-bounded
  right = cv 01a14938); release ok; second release `settled`; refund after release `settled`; TOP-UP plant: phase guard off AND
  two once keys ⇒ second payout admitted ⇒ red; unfunded deposit (no grant) ⇒ whole call refused, phase stays open.
  Account opened first by anyone: `account asset (owner := escrow)` (pinned view forbids same-tree birth).
- Then: send sha to PROTOCOL-6 (abd8f012f13228e0b) for the bounty row (row currently expects world/bounty/BountyEscrow; agree
  re-cut to world/escrow/Escrow) and to ROOT. Theorem statements → KERNEL-8 (a3757d866eb64f133)? No: escrow theorems are
  LANG-semantics; second-agent vacuity read by LANG-7 (ac6dbe9957c6ff484) or a fresh reviewer.
Other open: cv 01a14a03 (ticks spent = pool deducted theorem, Kernel/Proofs/Tree.lean, needs a run trace).
Tools: hbox logs/ledger-land.sh MSG CROSS PATHS (rebase+commit retry; run with < /dev/null; foreground pid wait ≤ 9.5 min);
 never put apostrophes/backticks in ssh '…' strings — write msg/scripts on Mac scratch, scp. fixomit.py pattern for the
 unused-section-variable linter (errors-as-warnings). SIZE: lines required for every risen SIZE row; WASTE: for ceiling raises.

## LEDGER-3 (spawned 2026-10-18 ~02:50Z; successor of LEDGER-2)
Ids now: LANG-8 = a4b6bc659ce41e2d9 (LANG-31 may re-id; told to hold until my escrow sha), KERNEL-9 = a3c391ed385095648
(reviews Kernel/ statements; shares cv 01a14a03). Mac scratch: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/ledger3
(source of Ledger/*.lean; scp to wt/ledger). hbox: logs/ledger3-*.
- ESCROW BUILT + GREEN in wt/ledger (uncommitted, on main 9b23ca6): Ledger/Escrow.lean, Ledger/Proofs/Escrow.lean,
  Ledger/Sim/{Journey,Main}.lean, lean_lib Ledger + lean_exe ledger-sim (lakefile), runs.tsv `ledger-sim 1 ALL PASS`,
  world/escrow/Escrow (11413 B, from `ledger-sim --write-text`), decisions/ledger.md LEDGER-10. Methods 0 deposit 1 refund
  2 release (sorted). ledger-sim ALL PASS (honest + skip-judge + two-keys + drop-calls). Mutations M1-M3 red (logs/ledger3-mut.sh).
  Vacuity review: fresh reviewer subagent spawned 10-18; land after its OK.
- LANDED 7c6c7e1 (ledger:, LEDGER-10): escrow package + Ledger/EscrowSpec.lean (data measures: closure C3 forbids data
  defs in proof-modules) + proofs + ledger-sim + world/escrow/Escrow. Reviewer (fresh subagent) found nothing vacuous; its
  two WEAK items fixed pre-landing (one_payout now over acts' own calls via escrow.methods[m]; verdicts via runLaw +
  escrow_admits witnesses). Remaining named gaps: no slot-level (invoke_slots-style) restatement; calls are eval Vals at
  1000 ticks, not composed through extract/callsOf/accountId (no fuel-monotonicity lemma in LANG).
  scripts/commit needed SIZE lines for 6 rows (msg: hbox logs/ledger3-msg-escrow.txt). Mutations: logs/ledger3-mut.sh (M1-M4).
- Sent: PROTOCOL-6 sha + draft bounty row lines (re-cut to <world/escrow/Escrow); LANG-8 (re-id => ledger-sim --write-text;
  list of LANG lemmas my proofs use); HOSTING-4 (FYI); ROOT.
- cv 01a14a03 CLOSED with KERNEL-9's agreement (per-step exactness = invoke_ok; reopen trigger on the task).
### Open for LEDGER-3/successor
1. Answer PROTOCOL-6 on the bounty row (verbs/plant shape); the row is PROTOCOL's to land.
2. Possible strengthening (not owed): slot-level escrow theorem (native_decide + axioms-allow row, GATES), and a LANG fuel
   monotonicity lemma to carry escrow_calls_payout to the receiver's budget (ask LANG-8 if wanted).
3. LEDGER-2's taste forks stay Ember's (sweep/decay/commons; reclaiming unused credit). Amount-bounded grant = cv 01a14938 (KERNEL).
- LANDED 8e009cd: CORRECTION. 7c6c7e1's "no fuel-monotonicity lemma exists" was false: Lang/Proofs/Run.lean run_stable/run_agree,
  and c4e435a Lang/Proofs/CallLive.lean (extract_conforms, runMeasured_calls_le, callsOf_live). The remaining gap is only composing
  the projected eval fields with whole-result extraction. Open item 2 above is now: compose them (doable, not owed).
- Bounty row PASS: PROTOCOL-6 2f5a201 (PROTOCOL-34); no rows pending. LANG is now LANG-9 = ae7c1ef24d42d1286 (told it which surfaces I depend on).
- LANDED fa390f7 (KERNEL-9's ask, KERNEL-37): admit_birth/admit_not_born/fold_floors_held/account_keyed take hE : E.Lawful n;
  deployed_account_keyed = account_keyed deployed_lawful (LedgerDeployed.lean cross-layer KERNEL). Sent KERNEL-9 for review.
- Correction to my ROOT report: rows are 19 PASS but the carry row is open (waits on HOST-8), so "no rows pending" was wrong.
- KERNEL-9 reviewed fa390f7: OK (premise-only change; LedgerDeployed cross-layer accepted). Kernel/ has one Env premise shape.
- KERNEL is now KERNEL-10 = a7049ec6dbdff31cc; told it fa390f7 was already reviewed OK by KERNEL-9.
- LANG is now LANG-10 = a712e8c509a3bb0e0; escrow re-checked green on main 3ed84fc (after LANG-34/35): Ledger builds, ledger-sim ALL PASS (E0 byte-identical). Told LANG-10 the surfaces I depend on.
- COMING: lang! re-id (ROOT ruling cv 01a14aab-adae (ii): a digest Ty, callTy id fields digest). LANG-11 agrees the hour with me. My side: escrow id fields + deposit grant -> digest; agentIs equality prim; proofs' Val.bytes RHS; beq_fields twin; seed/args encoders; then ledger-sim --write-text. Prepare against LANG-11's branch, land in the same window.
- LANG is now LANG-11 = ac74cc733b391d27a (digest lang! day first; agrees hour with me, HOSTING-6, PROTOCOL-7). Sent it my readiness + the surface I need.
- DIGEST DAY drafted (unbuilt) in Mac scratch .../scratchpad/ledger3/digest (git: base ebb4dc4 = main 64c89e0 files; working diff = patch). Escrow gains nonce : bytes (deposit once key; self is digest now), LEDGER-11 drafted. Told LANG-11 (bounty seed needs (nonce ...) via PROTOCOL-7 in the same commit). Next: LANG-11 sends tree path -> apply on a copy of its tree in wt/ledger, build Ledger + ledger-sim, --write-text, hand patch.
- LANG-11 accepted nonce design; it adds (nonce "bounty-1") to the bounty row itself (PROTOCOL-7 agreed). New: Bounds.digestBytesMax 32 (my fixtures are <=8 bytes; symbolic eval proofs unaffected). Waiting for its tree path.
- KERNEL is now KERNEL-11 = a97af574d573a9dbb (canonical-journal flag day coming; my Kernel/Value + Kernel/Proofs/Ledger rebuild under it, no statement change). No open Kernel ask.
- DIGEST patch HANDED to LANG-11: hbox logs/ledger3-digest.patch (vs 2b4f3bb; built green on lang11-digest-lang.patch, ledger-sim ALL PASS, M1-M4 red via logs/ledger3-mutd.sh). wt/ledger holds LANG+my diff uncommitted: after LANG-11 lands, checkout --detach main and verify my files == patch, rerun ledger-sim 1.
- LANDED (by LANG-11, cross-layer) 1b831da: escrow on digest ids + nonce (LEDGER-11); rows 21/21 incl bounty. wt/ledger reset to main 1b831da (reset --hard after verifying my paths == main); Ledger builds, ledger-sim ALL PASS on main. Nothing in flight.
- KERNEL is now KERNEL-12 = ac263f30c5dbd8c95 (KERNEL-41 (a') journal port day; tells me the hour). Re-checked escrow after 1ed7867 (KERNEL-42 domain day).
- LANG is now LANG-12 = aa6fec46b5067cd28 (announces any re-emit of world/escrow/Escrow; I run ledger-sim --write-text).
- K41 journal-trie flag day landed 5eb9b30 (KERNEL-12); my Kernel/Ledger proofs rebuilt green there; wt/ledger moved to main and re-checked.

## LEDGER-4 (spawned 2026-10-19; successor of LEDGER-3; ROLES.txt id ab4228d03643a267b)
Mac scratch: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/l4.
hbox tools: logs/ledger4-stmts.py OLD NEW FILE... (old/new statement of every changed decl, by name; it can
swallow a decl after a one-line `:= term` proof: logs/ledger4-cov.py lists the names it missed, check those by diff).
Pitfall: in `ssh hbox 'cd X && nohup … & echo $! > rel/path'` the `&` backgrounds the whole `cd && nohup` list,
so the pid echo runs in $HOME: use absolute paths, or wrap `(cd … && nohup … & echo $! > /abs)`.

## LEDGER-4 AUDIT (2026-10-19, main 1e90c0b)
Range: every commit touching Kernel/Value.lean, Kernel/Proofs/{Value,Ledger,LedgerDeployed}.lean,
Kernel/Receive/Ledger.lean, Ledger/, world/escrow/, decisions/ledger.md after 1b831da (LEDGER-3's last check;
38d94e1 landed after LEDGER-3 ended and was never owner-read, so it is in). Statement diffs:
hbox logs/ledger4-stmts.py over each consecutive pair; built on main in wt/ledger: lake build Ledger
Kernel.Proofs.{Ledger,Value,LedgerDeployed} green, 0 warnings; ledger-sim 1 ALL PASS; --harness-control RED (1).
- 38d94e1 (KERNEL-44/47, the log is a list of steps) ACCEPTED. fold_value / fold_floors / fold_floors_held now
  over `List (Step D)` with a `.refusal` case; fold_floorOk / fold_floorsBorn restated through fold_keeps with
  named args (same premises). fold_floors' premise is `∀ t ∈ Step.turns l, …`: the old premise over the turns
  of the new log, not an added one. New refuse_sumOf, refuse_taken (a recorded refusal leaves the cells' trie).
- 42c261b (rows, the fourth trie) ACCEPTED. derive_value_born, effect_transfer_authorized, tree_zeroBorn gain
  `{rv : RowView D}`, universally quantified, no hypothesis. issue/account/transfer/credit Drafts gain a rows
  field, always [] (ledger receivers write no rows). Escrow methods take the rels record first
  (`.lam (.record [])`); EscrowSpec evaluates with it; escrow_slots over `methodSig state rels` / `Sig.calls`.
- 7c09186 (rows key LEB128) ACCEPTED, no effect: touches no LEDGER path; no Ledger statement names rows bytes.
- 87dff6e (LANG-50) ACCEPTED: world/escrow/Escrow.ob is the surface source; --write-text lowers it; row E0s.
- 0e1b027 (GATES-15) ACCEPTED: --harness-control on ledger-sim, measured RED (1).
- b48c10f (KERNEL-54, version binder) ACCEPTED; "no premise added" CONFIRMED statement by statement:
  touchCheck_flows (conclusion `∃ cell v`, same content), born_sum (born at version 0 = bornEntries' 0),
  cellsSum_noValue / floorOk_noValue / entry_outstanding (hypothesis `∀ c v, e = .live c v → P c`: in negative
  position, equivalent to the old `∀ c, e = .live c → P c` for the new Entry). admit_written: proof only.
- 482aecc (KERNEL-56) ACCEPTED with the disjunct check. account_keyed / deployed_account_keyed: premises
  unchanged (hE, h). Conclusion `(a,s) = (b,t) ∨ CollidesAmong hash [accountPre a s, accountPre b t]`. Under h
  (the two hashes equal) the right disjunct is exactly `accountPre a s ≠ accountPre b t`, not provable from
  the premises (a=b, s=t satisfies them and makes it false) nor from the deployed instance (a s b t free).
  So the theorem is: equal preimages give one pair, which is the Lawful size split, real content; the tooth
  account_keyed_sep (Separates over the explicit pair) states it with no escape. S is the theorem's own two
  objects; no unbounded ∃ collision predicate is left in any LEDGER file (grep: only these two).
- 1e90c0b (LANG-60) CORRECTED: it left the escrow's doc empty `(doc)`. LEDGER-12 (prepared, not landed: hold
  until ROOT's GATES-20a hash) writes the line in Escrow.ob and Ledger/Escrow.lean and re-emits through
  --write-text. E0/E0s both FAIL with the core stale (RED (2)), ALL PASS after; rows bounty PASS.
  Message: hbox logs/ledger4-msg-doc.txt. Files: Ledger/Escrow.lean world/escrow/Escrow world/escrow/Escrow.ob
  decisions/ledger.md (uncommitted in wt/ledger on 1e90c0b). No theorem, so no vacuity read is owed.
- QUESTION: none. RED: none.
- LANDED c7f455e (ledger:, LEDGER-12, the Escrow doc) after GATES-20a 6527d9f lifted the hold; judged green 3 times
  (displaced twice by main moving), pushed. wt/ledger moved by scripts/commit.
- Removed (my own strays, created this session by a mistaken cp): logs/{Escrow.lean,Escrow,Escrow.ob,ledger.md},
  each byte-identical to logs/ledger4-bak/ before removal.
- Next per ROOT: LEDGER-3 open item 2 (compose escrow_calls_payout's projected eval fields with whole-result
  extraction via Lang/Proofs/CallLive.lean + Run.lean run_stable) if context allows, else LEDGER-5 handoff.

### LEDGER-4 HAND-OFF (for LEDGER-5; main c7f455e; nothing in flight, wt/ledger clean at main)
State: audit done (above), LEDGER-12 landed c7f455e. No open rows, no open asks to me. Taste forks stay Ember's
(sweep/decay/commons; reclaiming unused credit); amount-bounded grant is cv 01a14938 (KERNEL).
The ONE optional item, scoped (not started; I stopped on context, ~180K, since it is a 200-400 line proof):
compose `escrow_calls_payout` (Ledger/Proofs/Escrow.lean:252, which reads each call FIELD by running
`slotField ℓ pick` = `.case (.get (.get (methodAt ℓ) "calls") "c0") …` with `Lang.eval [] 1000`, i.e. the
machine `run` from `State.init`) with what the receiver does: `runMeasured` runs the WHOLE method application
at the method's budget, `extract (resultTy …)` forces the result into Data, `callsOf` reads `Body D`.
Pieces on main: Lang/Proofs/Call.lean `runMeasured_calls` (the calls are `callsOf c` of the extracted
`calls` field), `callData_bodyOf` (needs `digestOf (bytesOf x) = some x`); Lang/Proofs/Agree.lean `run_bigStep`
(a run ending in a value computed the term's `BigStep` meaning) and `run_agree_meaning`; BigStep.lean
`bigStep_deterministic`; Run.lean `run_stable`/`run_agree` (budget independence); CallLive.lean
`extract_conforms`, `bodyOf_live`. MISSING (the actual work): a lemma that extracting a record result at a
record type forces each field to the BigStep meaning of `.get result ℓ` (so the receiver's extracted `c0`
equals the Data of the value `escrow_calls_payout` computes), and the step from the Val/Data AcctRef
`of self asset` to `accountId X e asset`. Ask LANG (decisions/lang.md owner) whether the extract/BigStep field
lemma belongs in Lang/Proofs (it would: it is about `extract`, not the escrow). Target statement shape:
`runMeasured … escrowId state m args r budget = .ok (s, calls, …) → m ∈ [1,2] → calls = [Body.transfer
(.of self asset) (.of party asset) amount none (some "payout")]` with the parties read from `state`.

## LEDGER-5 (spawned 2026-10-21; successor of LEDGER-4; ROLES.txt id ad08711ec506b6f66)
Mac scratch: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/l5.
hbox: logs/ledger5-{patch,msg.txt,commit.log,commit.pid,sim2.log,vac-1.lean,x1.lean,x2.lean}.
### LEDGER-13 (the escrow strengthening on LANG-61)
- Statement: `Ledger.Proofs.EscrowRun.escrow_run_calls`: (∀ x, digestOf (bytesOf x) = some x) →
  readPackage look pkg = .ok escrow → runMeasured … = .ok (s, calls, rows, t, n) →
  `RunCalls digestOf state method args r.self calls` (state reads as stateOf 7 terms; method 0/1/2 with
  exactly the one transfer each; other indices do not run). Forms: `escrow_program_calls` (X.program.run,
  X.Lawful, program = Lang.program over its codec), `escrow_run_deployed` (Host.Deployed.X, only hpkg left).
- Spec now = the receiver's term: `EscrowSpec.methodResult` (apply4 0 ℓ under [escrow.body], extracted whole
  at resultOf); `escrow_method_results` replaces escrow_calls_payout + escrow_method_state; the 14
  projections/methodAt/spendsB/reqOf deleted. escrow_one_payout statement unchanged.
- Teeth: run_calls_pins_payee, run_result_needs_body, escrow_run_spends. Vacuity read (2nd agent, disjunct
  check): nothing vacuous, nothing weaker; fixed the escrow_run_spends label, added run_calls_pins_payee.
- Built: lake build Ledger ledger-sim green; ledger-sim 1 ALL PASS; --harness-control RED (1); closure ok.
- OPEN (named in decisions/ledger.md LEDGER-13 critique): (a) no kernel witness of a whole successful run
  (decide +kernel stuck in runSetup though each piece reduces alone; logs/ledger5-x2.lean has the probes);
  (b) the slots the run WRITES: needs runMeasured_means to expose `stateSlots (recordRow p.state) ds 0 = some s`
  with st = .record ds (Lang's; ask ROOT for LANG-22), then readState_go_stateSlots gives
  readState s = stateOf … target; (c) chain over receiver runs (after (b)); (d) move private means_relib
  into Lang/Proofs/Extract.lean beside bigStep_relib (Lang's).
- LANDED 9ced635 (ledger:, LEDGER-13), pushed. First attempt refused only for SIZE lines (theorems +20, max
  dependents +1); second judged green, CAS at queue head. wt/ledger moved to 9ced635 by scripts/commit.
- Pitfall (mine): `ssh 'cd X && … && nohup … & echo $! > pid'` backgrounds the whole && list, so the pid
  file held the wrapper (1538295), not scripts/commit (1538305); it exited by itself. Launch the nohup alone.
### LEDGER-5 HAND-OFF: nothing in flight; open items (a)-(d) above; (b) waits on a Lang need sent to ROOT.

## LEDGER-6 (spawned 2026-10-21 10:49Z; successor of LEDGER-5; ROLES.txt id ae39612ab24612424)
Mac scratch: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/l6
(b.sh scp+build, r.sh probe runner). hbox: logs/ledger6-{msg.txt,commit.log,commit.pid,sim.log,simc.log,x1..x3,W,vac-1,vac-2}.
### LEDGER-14 (the chain over receiver runs + the kernel witness)
- `Runs prog pkg p state runs` (EscrowRun): per step readPackage look pkg = .ok p, prog.run ok, prog.judge
  look (some pkg) laws state s r ok, next step on any slots equal to s key by key (readState_get).
  `escrow_runs_one_payout` (payoutCalls ≤ 1, payout = grantless transfer, EscrowSpec.isPayoutCall),
  `escrow_program_one_payout`, `escrow_runs_deployed` (premise: the runs only). `escrow_runs_after_payout`,
  `escrow_judge_settled`. RunCalls gained the written slots (LANG-63 read-back).
- Deleted the spec chain: escrow_one_payout, spends, Act, stepsOf, callAt, spendCount, escrow_run_spends …
- (a) DONE without native_decide: Ledger/Proofs/EscrowWitness.lean, `escrow_runs_witness` (deposit then
  release on Codec.Digest, Runs of the deployed program, payoutCalls = 1) + tooth `escrow_second_release_refused`.
  ROOT CAUSE of LEDGER-5's stuck probe: load/loadAll are mutual WF recursion (kernel won't unfold) and
  decodePackage in the kernel blows past 6G. LEDGER-5's "each piece reduces alone" was FALSE: those probes
  were OOM-killed silently (exit 143, no output). Route: rw [load] equation, readPackage_installed (encode
  side), setup_eq from pieces, decide +kernel for the rest. ~10 s / 2.7 GB.
- Vacuity read (2nd agent, disjunct check): nothing vacuous/weaker; fixed the key-wise hand-off.
- Open (decisions/ledger.md LEDGER-14 critique): self-deposit is not counted (kernel refuses sameAccount
  outside Runs); invoke's write → next stateOf key-wise equality is KERNEL's, not composed; readState_get
  belongs in Lang/Proofs.
- LANDED ebe9d81 (ledger:, LEDGER-14), pushed. First attempt refused for a needless `--reverts 9ced635`
  (the candidate reverts nothing of 9ced635: deleting a theorem LEDGER-13 only re-labelled is not a revert);
  second displaced once by main moving, then CAS at head. wt/ledger moved to ebe9d81.
### LEDGER-6 HAND-OFF: nothing in flight; open items in decisions/ledger.md LEDGER-14 critique (1)-(4).
### LEDGER-15 (ROOT's follow-up: the chain over admitted invokes)
- LANDED e86f237 (ledger:), pushed. Ledger/Proofs/EscrowInvokes.lean: `Invokes` (steps `invoke` = top-level
  signed invoke of obj received+admitted; `other` = admitted turn not touching/creating obj), `invokes_runs`
  (admit_frame, invokeRun_live, invoke_next_judged, invoke_next_slots), `escrow_invokes_one_payout`,
  `escrow_invokes_deployed`; tooth `escrow_link_bites` in EscrowWitness.
- Vacuity read 2: fixed interleaving (the `other` step) and a phantom tooth name; satisfiability of an
  invoke of a programmed object closed by KERNEL-23's InvokeWitness (628a8b9).
- cv filed: 01a15456-b411 (move readState_get to Lang), 01a1553b-2765 (escrow-specific admitted invoke
  witness, after KERNEL-28). Agreed KERNEL-24's KERNEL-28 amount right on my paths with 4 conditions
  (no statement weaker; package bytes unchanged; ledger-sim ALL PASS + plant flips + control RED; LEDGER-16 pointer).
### LEDGER-6 HAND-OFF (2): nothing in flight; next: cv 01a1553b-2765 once KERNEL-28 lands; nested invokes = KERNEL cv 01a15430-0f62.
### ROOT-DOCS (2026-10-21, ROOT for LEDGER): the credit taste fork CLOSED
- Ember: "FINAL. Just let it sit there. It isn't a strong opinion, it's just for simplicity's sake." Unspent credit sits: no sweep, no decay, no reclaim to a commons or the issuer; final for v1. Written as decisions/ledger.md LEDGER-17 (LEDGER-16 left for KERNEL-28's pointer). The carry "taste forks left to Ember: sweep/decay/commons; reclaiming unused credit" (lines 82, 235, 307 above) is closed.

## LEDGER-7 (spawned 2026-10-22; successor of LEDGER-6)
Mac scratch: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/7c10f132-0e99-4487-aaaa-62ea34c9f1c0/scratchpad/l7
(b.sh: scp + build in wt/ledger; r.sh: probe runner). hbox logs/ledger7-{b.log,sim.log,simc.log,msg*.txt,commit*.log,p1,pA,pX}.
Reader probes: logs/ledger7r-*.
### Owner's read of KERNEL-60's five shape changes (sent to ROOT first): none weaker
- transfer/effect_transfer/credit_authorized: the chain is over `.transfer 0` / `.credit 0`. rightKey
  ignores the cap, so 0 is a kind marker. Each gains the leaf grant's spend conjuncts.
- transfer/credit_exact: the frame excludes only `via = some k`, and g is described whole.
- FINDING: no spend was read back (no ledger contiguity invariant). ROOT ruled KERNEL-30 (landed 1fe9f93:
  LedgerContiguous, grant_turn_ledger, spend_reads_back(_dispatched)), and grant_moves_le_cap is mine.
### LEDGER-18 LANDED c3efc97 (cv 01a1553b-2765)
- ledger-sim E7 reads the cap off the live escrow (`Escrow.amountOf`), and E7 checks the read
  against the born terms.
- The short-cap plant and E9 pin `transferSpent` of THAT grant id (`spentOf`).
- Ledger/Proofs/EscrowAdmitted.lean: escrow_history_witnessed (an ObjectHistory with
  payoutCalls = 1, deposit + release through the real receive/admit, decide +kernel),
  escrow_deposit_spends_cap, and the tooth escrow_short_cap_refused.
- Pitfall: `decide +kernel` of `readKind … = .ok pkgCell` compares the package literal and hung for
  25 min. `rfl` closes it.
- The escrow package bytes are unchanged, and there is no flag day.
### LEDGER-19 LANDED 704af55 (FAST GREEN after waiting behind PROTOCOL's head FULL lander ~45 min)
- Std.Chain is generalised over its request and state types (ROOT for LANG, --cross-layer).
- Ledger/Proofs/GrantCap.lean: audit_grant_chain, grant_moves_le_cap and grant_credits_le_cap
  (chain_sum over Worlds).
- GrantCapTooth: grant_cap_needs_contiguous (an audited gapped grant moves 20 against 10).
- Reader (LEDGER-7-READER): LAND after its fixes.
- Open (decisions/ledger.md LEDGER-19 critique):
  - carves are not counted as moves;
  - no contiguous non-empty audited witness;
  - no credit tooth.
- Open, standing: the self-deposit note (LEDGER-14 (3)).
- Not via ObjectHistory: a grant spend is no ObjectStep, so the history is the audit's own Std.Chain (told ROOT).
### LEDGER-7 HAND-OFF: nothing in flight; wt/ledger at 704af55; open items = LEDGER-19 critique (1)-(4) + LEDGER-14 (3).
