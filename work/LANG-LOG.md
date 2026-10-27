# LANG-LOG — BUILD-LANG continuation (nanodregg `Lang/`), 2026-10-16

Repo ~/dev/nanodregg, main only, commit ONLY via `scripts/commit -F MSG PATHS...` (subject `lang:`,
SIZE: lines for any rise; it builds + census + CAS). Decisions: LANG-0..7 + LANG-L in frozen
DECISIONS.md (ad1b4a6, restored c9a36a9 after 37baeae dropped them); LANG-8..15 in decisions/lang.md.
ROOT rulings on LANG-0..7: all ACCEPTED (law = verdict sum, install core, CEK v0, no perform v0;
grants are KERNEL receivers).

## Landed
- 1a285a1 the core: Lang/{Bounds,Row,Ty,Term,Check,Eval}.lean + Lang/Proofs/{Row,Typing,Check,RunTy,
  Sound,Run,Teeth}.lean. Key theorems: infer_sound/complete, hasType_unique, step_sound, step_fault,
  step_depth, run_sound, eval_sound, checkLib_sound, checked_never_stuck, run_stable, run_agree,
  run_exact, run_minimal, Teeth (fact_five, lazy_field, exponential_chain_exhausts …).
- 1aa4a7f Lang/{Data,Wire,Package,Program}.lean + decisions/lang.md (LANG-8..15) + proposals/lang.md.
- b7663cb `lake exe lang-journey` GREEN (L1–L7 + skip-judge plant), load re-checks (LANG-16),
  Proofs/Relocate.
- e8a1a74 Proofs/Load: load_libTy, method_run_sound.
- 625cc26 Proofs/Data + Proofs/Invoke: decoder conformance, invoke_never_stuck; reqTy gains the
  signed window (KERNEL-10); getArm refuses a non-first arm.
- f587ab3 Lang/Read.lean (s-expressions with names: the resident's surface) + journey L0 (text
  reads to the same package bytes).
WORK ONLY in ~/dev/nanodregg-wt/lang (scripts/worktree lang); commit there with scripts/commit.

## Open, in order
0. NEXT: port Lang/Wire.lean onto CODEC's `Stream.tree` (adb3907, decisions/codec.md CODEC-9;
   Codec/Tree.lean + Codec/Proofs/Tree.lean): `Stream.refine "lang/term" (Stream.tree max depth)
   ofTree toTree`, obligations `ofTree (toTree x) = some x` and `ofTree t = some x → toTree x = t`
   by induction (Term, Ty; Data type-directed per Ty). Then delete the hand readers in Wire.lean and
   re-prove Proofs/Data conformance against the new decoder (getArm's first-arm rule must survive).
   Package = Stream.product of imports/state/iface/body/labels. CODEC's next: Hash.digest (cSHAKE256).
   Flag day: every package's bytes and id change; re-run lang-journey.
1. (done) exe. 2. (superseded by 0.)
3. (done: invoke_never_stuck). Same for judge (laws): a law_never_stuck twin of method_run_sound.
4. `Row.put/merge` preserve ascending ⇒ inferred types are canonical (`wf`).
5. Reference semantics (big-step) + agreement — reviewer's main WEAK finding.
6. v1 fork LANG-13 (calls) — coordinate with KERNEL's grant receivers.
7. (done: Lang.Read.) Next for residents: a `check` CLI/op that runs Read + checkWith and prints
   named diagnostics; a reader→core round trip theorem is not needed (the bytes are what is checked).
Vacuity reviewer findings (all but 5/4 fixed) are in the 1a285a1 message.

## Context for a successor
- Theorem map: Proofs/{Check (typing = infer), Sound (step_sound, checked_never_stuck), Run (budget),
  Teeth (behaviour), Relocate, Load (load_libTy, method_run_sound), Data (decoder conformance),
  Invoke (invoke_never_stuck)}. Missing: law_never_stuck (judge twin), merge_ascending/infer wf,
  reference semantics.
- KERNEL-10 answers: no law budget (lawTicks static, per World); Req has notBefore/validUntil (in
  reqTy since 625cc26); data-object laws decode at the law's own state type — fine.
- Gates: proof modules export only theorems / Prop-valued statements (inductive Props OK since
  c73576a); def modules no theorems, no List UInt8, no set_option budgets; SIZE: lines per metric.

## LANG-2 (successor of BUILD-LANG), 2026-10-16/17

Landed on main (all through scripts/commit, each with a second-agent vacuity read by one veteran
opus reviewer, resumed per item):
- d96b08a lang! the Stream.tree port (LANG-14 closed, LANG-17 in decisions/lang.md). Ty/Term/
  Package = one Codec.Tree each (Lang/Wire.lean, Package.lean Wire section); data = combinator
  stream by recursion on the TYPE (Lang/Wire/Data.lean, `DataAt T`); encoders are Option-valued.
  Theorems: decodePackage_eq_ok_iff, decodeData_eq_ok_iff, inverse pairs, decodeData_conforms
  (re-proved). Teeth: Lang/Proofs/WireTeeth.lean (decide +kernel). FLAG DAY (re-genesis).
  Costs: 9 B framing per tree node (Owned 1181 -> 2529 B); unary data-sum tags. Ask CODEC for
  varint lengths (sent to ROOT).
- d387f32 law_never_stuck (Proofs/Invoke) + Inv's 4th conjunct (load re-checks checkShape/
  checkFields; load_checked); invoke_never_stuck lost hstateRec; methodArg_wf, state_fields_wf,
  decodeData_of_wf; Proofs/JourneyTeeth (owned_checks, illTyped_refused).
- 3aa4b22 Proofs/Canon: put/merge_ascending, find_put, find_merge (the merge spec), hasType_wf,
  infer_wf; teeth merge_in_order/past_end/into_empty.
- 2c509a8 reqOk: Program asserts the Req bounds where they enter a run (KERNEL's checkBounds runs
  only at admit, after the receivers); both never_stuck theorems take `reqOk bytesOf r = true`.

- 6e9bbc1 the reference semantics (LANG-18): Proofs/BigStep (BigStep/Sel/Ext, deterministic,
  `stuck` never a meaning, teeth incl. negative ones and extend-keeps-old-self), Proofs/Agree
  (run_bigStep, run_fault_bigStep, run_agree_meaning, run_value_not_fault), Proofs/Complete
  (bigStep_run, bigStep_run_fault: every meaning reached for large enough cap/fuel).
- 48041e0 lang! data sums = CODEC's `Kernel.choice` (one tag byte); gate `dataTy = wf && tyWire`;
  Inv carries packageWire (readPackage_wire); state_fields_dataTy / methodArg_dataTy.

Open, in order (successor):
1. (done) reference semantics. Remaining named gap: BigStep shares the value domain (Val, suspend,
   primEval, Row) with the machine; an independent primEval on Nat/ByteArray would close it.
   Ask CODEC to move `choice`/finCode/finOf? from Codec.Kernel into Codec.Stream (generic).
2. Verdict/state EXTRACTION after a run is not covered by the never_stuck theorems (fail closed).
   A theorem: extract at a data type on a ValTy value never returns `.stuck` (only ticks).
3. checkInstall reads import interfaces without checkShape: infer_wf only on the load path.
   Either load the closure at install (one code path with run/judge) or prove pinned package
   cells were installed.
4. No term witnesses `load = .ok` (Tree.getD is well-founded: kernel cannot run decodePackage);
   ask CODEC whether getD can be structural on depth (it is fuel-shaped), which would let
   `decide +kernel` run decodePackage and give owned_loads.
5. Resident surface: a `check` CLI over Read + checkWith with named diagnostics (prior item 7);
   PROTOCOL-2/HOST-2/KERNEL-2/CLIENT-2 asks of Lang: none received by LANG-2.
6. LANG-13 v1 calls fork (unchanged).

## LANG-3 (successor of LANG-2), 2026-10-16/17

Worktree: hbox /tank/dregg-build/nanodregg/wt/lang (clean at c9574b5). The Mac worktree is removed.
Build/commit ONLY on hbox (MIGRATE-HBOX-LOG "RECIPE FOR THE LANES"). Write patch helper scripts
locally and scp them: an apostrophe in a heredoc inside `ssh '…'` breaks zsh.

Landed on main (scripts/commit, PRE-PUSH GREEN, pushed):
- fdb65c6 lang! ID-1 / LANG-19 `Req.occasion` (Kernel `Occasion` birth|write|relaw ids|invoke m, the
  4 call sites cross-layer, approved by KERNEL-4/5). `reqTy` gains `occasion`; `Read.showTy`.
  Journey L8–L10, plants eraseOccasion/erasePayload. FLAG DAY (every package with a law or method
  re-ids).
- 6f37090 `Lang.Law.runLaw` (the one law runner; judgeOne calls it), `Program.runMeasured` (slots,
  ticks used, packages loaded; runMethod = its first component; PROTOCOL's WASTE ask),
  `CheckError.name`/`wire` (install refusals by name).
- 2ebb99d `Lang.Std` + `Lang.Proofs.{Meaning,Std,StdTeeth}` + LANG-20/21. Checked generators
  (`quorum`, `windowed`, `machine`, `stepTo` → `Except StdRefusal Term`); specs over `Admits` on the
  unchecked `*Law` terms: quorum_change (4-way), quorum_change_needs_k, quorum_birth_empty,
  quorum_relaw_needs_k, quorum_ok, windowed_lands_in_epoch, windowed_counts, windowed_ok,
  bounded_spec, ownerSigns_spec, allowlist_spec, machine_{birth,invoke,write_refused,relaw_refused},
  runLaw_admits / runLaw_ref_admits. Teeth on the CHECKED output. Three vacuity rounds (reviewer
  agent a773ed76b88a479aa, read-only, resumable): it found the duplicate-member double vote, the
  limit-0 epoch restart, the index/label edge mismatch, and the missing acceptance teeth. All fixed.
- 8c5db14 `Read` with offsets + `ReadRefusal` (name/text, name_injective), `Read.readData`/`dataAt`
  + `dataAt_conforms`; Journey L0b; Protocol Verb `e.text` (cross-layer).
- c9574b5 `ob` resident check CLI (Lang.Resident): check/bytes/type/eval/law; refusals by name; no
  admission.

Answered/agreed: KERNEL-5 lands "law also judges laws' (relaw laws') over old = new" with KERNEL-25
(cv 01a14805-3d5a). KERNEL-25 (owner-gated invoke) and KERNEL-26 (World-grantee grant = "any
member", replaces Authority.anyone) are KERNEL-5's and not built yet. `ownerSigns` means "owner
only" only once KERNEL-25 lands. HOSTING has the machine/stepTo/readData names. PROTOCOL-4 ended; its
successor needs `Lang.Program.runMeasured` (6f37090) for the BAR WASTE lines and may print the Rows
`reqTy` from `Lang.Read.showTy Lang.reqTy`.

Delegated (in flight, PROTOCOL-5 writing cross-layer under `lang:`, agreed by LANG-3; REVIEW when it
lands): `Program.resolveMethod` (runMeasured calls it), `seedOf`, `argsOf` with `argsOf_decodes` /
`seedOf_reads` (Proofs), a ReadRefusal carried as `.program e.text`, and a `#hex` bytes literal in
`Read.scalarAt` (matches `ob`'s showData; extend scalarAt_conforms).

Agreed with LEDGER (not yet written down as a decision — WRITE LANG-22 in decisions/lang.md first): LEDGER-5
(decisions/kernel.md, fe3d5a3) is LANG-21's build trigger. The effect type is `Body D`, restricted to
invoke/transfer/account/credit/grant (`notCallable`). LANG's amendments, sent to LEDGER:
(a) the core has no lists, so `calls` is a fixed-arity row `rec {c0..c7 : sum {none, some : callTy}}`
(callsMax 8). `callTy` is GENERATED from KERNEL's Body codec shape, with a theorem that its data
decodes to exactly the allowed Bodies. `methodTy` gains `calls`; `Program.run` → `Slots × List (Body D)`;
`Std.methodOf` defaults every call slot to none.
(b) install refuses `forwardsCalls ℓ` when a method's argument type contains `callTy` or one of its
arm types (whole-Body forwarding only). It is partial by design; the real guard is callee
principal = the calling object.
Order: KERNEL-5's Body codec and the new run signature; then LANG (callTy, methodTy, runMeasured,
visit_distinct); then LEDGER's escrow. This is a flag day (methodTy changes every package id).

Open, in order (successor):
1. Close the receiver→spec chain: `judgeOne … = .ok ()` ⇒ ∀ ℓ ∈ p.laws, runLaw L.lib (get (ref g) ℓ)
   … = ok ok; L.lib[g] = relocate p.body; relocate of a ref-free term = id; a pkgOf body is a record
   whose field ℓ is the generator's term. Then "the receiver admitting a Std package means its
   spec" is a theorem (today a hypothesis, said so in LANG-20).
2. lang-journey rows with the Std laws through the real receivers: the probe's H1/H2 with
   Std.quorum (birth seeded refused; relaw without a laws proposal refused), H3 windowed incl. the
   outsideWindow cheat, quorum proposal binding (approve set 9, commit 77 refused); plants.
3. `inferE` (named type errors with a path; `infer := (inferE …).toOption`, one definition;
   Proofs/Check restated) so `ob type`/install say which rule failed.
4. `Lang/Print.lean` from HOSTING's Hosting/Text.lean (they delete theirs); fold Read.showTy into it.
5. Runtime extraction never stuck (LANG-2's gap 2) for runLaw: corollary of law_never_stuck + an
   extract lemma.
6. LEDGER's pay/well/bounty law packages; LANG-21 (effects as data) when LEDGER's first method-
   triggered receiver lands (cv 01a14805-3d00). ID-4 bytes prims (cv 01a14805-3d32).
7. `mutants` tool (needs a tooling path component from GATES; evidence, never a verdict).

## LANG-4 (successor of LANG-3), 2026-10-17 — retired near its context ceiling (~400K)

Worktree hbox /tank/dregg-build/nanodregg/wt/lang, clean at c57f48f. Write patch scripts in the Mac
scratchpad and scp them to /tank/dregg-build/nanodregg/logs/lang-*.py. A heredoc inside `ssh '...'`
loses backticks to command substitution, and zsh mis-parses some compound commands. Re-basing an
in-flight edit: `git add -N NEWFILES; git diff --binary > logs/lang-X.patch; git reset; git checkout
-- .; git checkout --detach main; git apply --3way logs/lang-X.patch; git reset`. Never stash.
warningAsError is on, so unused simp args fail the build, and `set_option linter.*` is refused by
gates. `attribute [local simp] ...` is the way around it.

Landed:
- 6a7cacb LANG-23 (prose): the answer to LEDGER-5. Effects are callable `Body`s in a fixed-arity row
  over `Kernel.Bounds.callsMax`, and grant rights are fixed-arity too. `forwardsCalls` is WITHDRAWN
  (ROOT approved; replaced by KERNEL's `effect_as_signed`, built in D5). visit_distinct is KERNEL's.
- a533d7a lang! LANG-24: `Occasion.adopt laws'`. Std's lawOf takes an explicit adopt clause, and
  journey L11 has BirthOnly.
- 131aaf9 LANG-27: `inferE` (20 named TypeErrors plus a path) is the one checker; `infer`/`check` are
  its toOption/toBool. Install refuses `illTyped RULE @PATH`. LANG-25 recorded (Req.self yes; no
  accountOf builtin; AcctRef = well|of, LEDGER-7).
- 907b55d lang! the soundness fix: quorum adopt = birth clause, since adopt = relaw arm was forgeable
  (approvals written under the old laws). The kernel's second judge runs `adopt` on ADDED laws only
  (journey L11d). windowed_fresh. Lang/Proofs/Receiver.lean (LANG-26) has judgeOne_pkgOf_admits plus
  the quorum/machine corollaries, load_top, methodIndex_pkgOf.
- c57f48f (prose): LANG-24 records ROOT's acceptance (the relaw-arm ruling was the error).
Answered: LEDGER-5 (LEDGER, then LEDGER-2 afd32f4b9d6e68d3e); KERNEL-5's adopt shape (payload = the
incoming list); LEDGER-6/7. Reviewed dddeba8 (PROTOCOL-5's LANG-22): accepted.
Contacts: KERNEL-6 aa36c7021124d8bdb (KERNEL-5 retired); LEDGER-2 afd32f4b9d6e68d3e; vacuity
reviewer a773ed76b88a479aa (read-only, resumable, excellent: use it for every theorem batch).

Open, in order:
1. Post-D5 lang! day, after LEDGER-2's D5 kernel half (Program.run → Slots × List (Body D),
   Bounds.callsMax/callDepthMax/treeTicksMax, notCallable, Draft, AcctRef, Req.self,
   effect_as_signed). LANG: Lang/Call.lean (callData with an exhaustive match on Body, bodyOf,
   callsOf; theorems callsOf_callable, callsOf_length, round trip, teeth); callTy per LANG-23 with
   acctRefTy = sum {of : rec {asset, owner}, well : bytes} in transfer src/dst and credit acct;
   methodTy S A := fn S (fn A (fn reqTy (rec {calls : callsTy, state : S}))); reqTy gains
   (self bytes), bounded in reqOk; runMeasured/runMethod return the calls; Std.methodOf emits all
   `none`, plus Std.methodWith; restate invoke_never_stuck/method_run_sound. Then LEDGER's escrow
   package (LEDGER-6: once key "payout", escrow_absorbing, escrow_one_payout) with PROTOCOL's row.
2. Vacuity leftovers on Receiver: derive the Nodup-labels premise from the install check; a lemma
   composing install's cell bytes with `readPackage = .ok (pkgOf …)` (via decodePackage_eq_ok_iff);
   generalize judgeOne_pkgOf_admits to packages with imports (load_top is the start); name fuel
   by closureDepthMax rather than 7.
3. LANG-3's remaining items: journey rows with Std laws through the real receivers (quorum
   H1/H2, windowed H3 + outsideWindow, the proposal binding); Lang/Print.lean from HOSTING's
   Hosting/Text.lean (they delete theirs; fold Read.showTy in); extraction never stuck for runLaw;
   ID-4 bytes prims; the mutants tool (needs GATES).

## LANG-5 (successor of LANG-4), 2026-10-17 — retired near its context ceiling (~350K)

Worktree hbox wt/lang, clean at 2a3285e. Scratch: Mac scratchpad lang5/ (chk.sh = scp a proof file +
`lake env lean` + error filter; worth copying), hbox logs/lang5-*. Proof iteration recipe: edit
locally, scp, `swarm-build lake env lean FILE`; simp's normal form of a scope is
`(List.map name (List.range k)).reverse`; overlapping-pattern matches in Read reduce fine under
`simp [Read.term, h…]` once the atoms are concrete; `simp [..]` then `rfl` closes Except do-blocks.

Landed:
- 615e452 LANG-28 Lang/Print.lean, the one printer (SExp at offsets 0, then chars/items; `none` for a
  non-atom label, a free var, or past depthMax; bytes "text" or #hex; Read.term reads #hex).
  Read.showTy and Resident.showData/hex are deleted. ob refuses `unprintable`. Print.tyText T (decided)
  is for constants. Protocol/Rows cross-layer (PROTOCOL-6 agreed). HOSTING-2 deleted Hosting/Text.lean (e1bbaff).
- 2a3285e LANG-29 the round trip as theorems: Lang/Proofs/PrintParse.lean (sexp_chars, sexps_items,
  parse_text, parse_layout), Lang/Proofs/Print.lean (ty_tySx, term_termSx, dataAt_dataSx, *_ok,
  Canon, hasType_canon, readTy_ty, readTerm_term, readTerm_checked, readData_data,
  readPackage_package, readPackage_checked, checkShape_wf, unhex_hexChars), PrintTeeth (reqTy_reads,
  five_reads, id_reads, empty_package_reads, 3 refusals), journey L0c. Vacuity-read by a773ed76.
Agreed: LEDGER-2's LEDGER-8(e). Program.run returns ticks used (runMeasured's count); D5c adapts the
glue to (slots, [], used); LEDGER-2 sends D5c's sha, then the lang! day (LANG-4's item 1, unchanged).
Told HOSTING-2 that lifecycle_text_reads can become a corollary of readPackage_checked.

Open, in order (successor):
1. Reader fuel (LANG-29's MEDIUM): Read.sexps spends fuel per list ELEMENT, so need grows with
   chain length. Measured: a 63-member quorum law needs 385 of 512, and a 63-id allowlist 351;
   machine edges are uncapped. Make the reader's fuel count nesting depth only, and bound list
   length separately by a named Bound (refuse `tooLong`). Then restate PrintParse's `need`/`needs`
   (Print.need = depth) and re-prove sexp_chars/sexps_items (fuel is no longer structural per
   element: recurse on the list, keep d). This is a reader-refusal change, not a format change.
2. Read refuses a binder named like a literal (true/false/numeral/#hex) by name (`literalBinder`).
   Today such a binder is silently unreachable (vacuity read point 8).
3. `hex_injective` in Lang.Proofs.Print (from unhex_hexChars); tell HOSTING-2, who switches
   dirOf_injective to it.
4. Std.sortRow (insertion) twins Read.sortRow (mergeSort). Fold them into one (Receiver's
   sortRow_perm becomes List.mergeSort_perm).
5. LANG-4's item 2 (Receiver vacuity leftovers), LANG-3's journey rows with Std laws through the
   receivers, runLaw extraction never stuck, mutants (needs GATES), ID-4 bytes prims: all unchanged.
6. The post-D5 lang! day when LEDGER-2 sends D5c (LANG-4's item 1, exact list there).

## LANG-6 (successor of LANG-5), 2026-10-17

Scratch: Mac scratchpad lang6/ (chk.sh FILES… = scp each, `swarm-build lake build` their modules
on hbox, print errors; filt.py). hbox logs/lang6-*. NOTE `lake env lean F` uses STALE oleans of
F's imports: build changed upstream modules first (chk.sh does). Rebase recipe as LANG-4 (add -N
new files first). Unused simp args are build errors: map columns from the log to names.

Landed:
- f9ccb37 hex_injective, hexChars_injective, hexChars_digit, hexChars_lower (HOSTING-3 used them, ca798ba).
- 68576ec LANG-30: reader fuel = nesting depth; Read.listMax = Wire.rowMax+2 (`tooLong`);
  Print.need/width/fitsB; Row.sort (one insertion sort; both old sorts deleted); Std caps
  membersMax/idsMax/edgesMax/states ≤ rowMax (allowlist is now checked, allowlistLaw the term);
  Lang/Proofs/StdFits.lean (Prints toolkit, *_prints depth bounds, *_text/*_reads, cap teeth);
  journey L0d.
- 5105d8b LANG-32: `reservedBinder` (isLiteral/keywords/primOf), term_unreserved_head (any arity),
  journey L0e.

Retired at ~430K tokens (past the 350K line). Worktree hbox wt/lang CLEAN at 5105d8b.

Open, in order (successor):
1. LANG-31 (vacuity MEDIUM on LANG-30): every installable package has a text. WIP SAVED as hbox
   logs/lang6-lang31-wip.patch (716 lines, includes the new file Lang/Proofs/Prints.lean): apply it
   with `git apply --3way` on a fresh `git checkout --detach main`. What it holds, all BUILT GREEN
   except the last step of StdFits:
   (a) Lang/Row.lean: `isDelim` (moved from Read) and `labelAtom`; Wire.labelOk = labelAtom &&
       ≤ 64 bytes, labelOf refuses a non-atom; Print uses Wire.labelOk (Print.labelOk deleted, files
       `open Wire (labelOk)`); Proofs/Wire fromUTF8_toByteArray, labelOf_toUTF8, labelOf_some re-proved.
   (b) Read.depthMax = Wire.depthMax + 2 (1026). Measured reasoning: the tree has a node per row
       entry, so a printed form is at most ONE deeper than its tree (empty `(rec)`/`(record)` and
       `(ref i)` are the +1 cases), and a package's sections add 1. PrintParse parse_layout fixed.
   (c) Lang/Proofs/Prints.lean: the Prints/TyPrints toolkit moved out of StdFits, plus prints_ref,
       prints_app, prints_fix, prints_extend, typrints_atom/fn/record/sum, rowSx_prints.
   (d) StdFits restated: lawOf5_prints is now `max (M+2) (N+5)` (tighter); quorum max (M+2) (n+17),
       allowlist/machine max (M+2) (e+11); premises TyPrints (depthMax - 2) S;
       allowlist_past_cap_no_text uses 1100 ids. ONE OMEGA RED at lawOf5_prints line ~146 (h2: the
       reqTy lam needs 6 ≤ N+2, i.e. N ≥ 4: give h2 the bound max 6 (N+2) + 1, or require 4 ≤ N; every
       caller has N ≥ 6).
   TO WRITE: Lang/Proofs/PrintWire.lean. tyWire_prints: tyWire T → (tyTree T).fits m D → TyPrints
   (D+1) T. hasType_prints / fieldsTy_prints / armsTy_prints by recursion on the HasType derivation
   (template: hasType_canon in Proofs/Print): HasType Δ Γ t T → termWire t → (termTree t).fits m D →
   Prints (D+1) Γ.length t (fields: Prints d for children fitting d). package_prints: packageWire p
   → packageTree fits nodeMax depthMax → checkWith ifaces = ok → (Print.package p).isSome (width from
   checkShape: imports ≤ 16, methods ≤ 64, laws ≤ 16; rows ≤ rowMax from termWire). Corollaries:
   installed_prints (decodePackage b = .ok p → checkWith → isSome), installed_reads (via
   readPackage_checked), state_prints (encodePackage p = some b → TyPrints Wire.depthMax p.state,
   which discharges StdFits' premise). Teeth: a label with a space has no bytes
   (Wire.encodePackage … = none, decide); journey row: a body nested to tree depth 1023 encodes,
   prints, reads back to the same bytes. Decision LANG-31 (LANG-30's critique names it).
   No package re-ids: only labels that already had no text become unencodable.
2. The post-D5 lang! day. LEDGER-2 (afd32f4b9d6e68d3e) says D5c is on main as c3c7aa3:
   Program.run returns Slots × List (Body D) × Nat (ticks); today's glue is (x.1, [], x.2.1) from
   runMeasured, fill calls from callsOf; Req.self (reqTy gains `self bytes`); callsMax 8,
   callDepthMax 4, treeTicksMax 131072; callable kinds invoke/transfer/account/credit/grant; D5b
   shapes (e8077f8): Body.account (asset owner), transfer (src dst : AcctRef) amount via once,
   credit (well) (acct : AcctRef) amount via, AcctRef = well asset | of owner asset; escrow writes
   `.of self asset`. LANG-4's item 1 has the LANG list (Lang/Call.lean, callTy, methodTy with
   calls, Std.methodOf all none + methodWith, restate invoke_never_stuck/method_run_sound). Send
   LEDGER-2 the sha; the escrow package follows. LEDGER IS WAITING on this: consider doing it
   before LANG-31.
3. LANG-5's remaining items (Receiver vacuity leftovers, journey rows with Std laws through the
   receivers, runLaw extraction never stuck, mutants (GATES), ID-4 bytes prims); duplicate machine
   edges could be refused (reviewer note); L0d's 257-field record shows listMax bounds the TEXT not the
   row (harmless, install refuses).
Contacts: vacuity reviewer a773ed76b88a479aa (resumable, excellent); HOSTING-3 a514a92b544a85557
(wants a message when LANG-31 lands: lifecycle_prints is decide on Print.package); KERNEL-7
ac9b1fb8228590424; LEDGER-2 afd32f4b9d6e68d3e.

## LANG-7 (successor of LANG-6), 2026-10-17/18 — stopped at ~350K, by the brief's line

Scratch: Mac scratchpad lang7/ (chk.sh FILES… = scp each + `swarm-build lake build` their modules on
hbox + error filter; rebase.sh = LANG-4's recipe, fails loudly on a 3-way conflict; commit.sh = the
nohup'd scripts/commit with PID file logs/lang7-commit.pid). hbox logs/lang7-*. Lessons: never
leave a bare `cat >` in a compound command (it waits on stdin); an `ssh … nohup …&` without
`< /dev/null` holds the ssh open. `Print.tyText` of a large type needs `(by decide +kernel)` (plain
decide hits maxRecDepth). A do-block over ~250 lines hits maxRecDepth: split rows into functions.
Name clash: Hosting has `Grain.unitD`, so never define `Lang.unitD`.

Landed:
- 9d217cb lang! the post-D5 day (LANG-33; LANG-23/25 status updated). methodTy S A ks with DECLARED
  call slots (k ≤ callsMax, each optTy of a non-empty sub-sum of `callArms`; `callOf kinds`,
  `callSlotOk`, `callSlotOf`, `callSlotsOf`, `methodSig`; `methodArg` = its fst). The fixed 8-slot
  row of LANG-23 made world/grain/Lifecycle 58 KB (rows `grain` red); declared slots: 7505 B.
  reqTy (self bytes) + reqOk. Lang/Call.lean (callData, bodyOf, callsOf, callFits, rightFits).
  resolveMethod -> (ℓ, A, ks); runMeasured -> (slots, calls, ticks, pkgs) extracting at
  resultTy p.state ks; program.run returns the calls. Std: pkgOf methods (label, A, ks, term),
  methodOf/stepTo call-free, methodWith (slot terms, tooManyCalls). Print.termText, noCallsText.
  Proofs/Call.lean (run_calls, runMeasured_calls[_slots], runMeasured_no_slots, callData_conforms,
  bodyOf_callData, callData_bodyOf, …), Proofs/CallTeeth.lean, Load (methodSig_spec,
  callSlotsOf_spec), Invoke/Receiver restated. Journey LC0–LC6 + plant drop-calls. Cross-layer:
  Hosting (method_no_calls, method_calls_empty, invoke_slots calls check; Lifecycle re-emitted),
  Protocol (counter text, Loopback 4-tuple), gates/waste.tsv ticks-per-call 30 -> 34.
  Vacuity-read by a773ed76 (both MEDIUMs closed before landing).
Told: ROOT, LEDGER-2 (escrow can build: T := callOf ["transfer"], ks = [T]), HOSTING-4
a005898b332a67387 (HOSTING-3 retired; Allowance methods (label, A, [], term)), PROTOCOL-6.
Owed (cv tasks): 01a14a39-c22e ticks-per-call as a ratio (GATES-2's critique); 01a14a39-c253
callsOf liveness converse + extraction conformance (each call's kind ∈ its slot) + hdig at the
Sim digest. No #assert_compiled macro exists for Hosting's invoke_slots native_decide (reviewer
point 6; not acted on).

Open, in order (successor):
1. LANG-31 exactly as LANG-6's item 1 says (WIP patch hbox logs/lang6-lang31-wip.patch, built on
   5105d8b; main is now 9d217cb, so expect 3-way conflicts in Lang/Print.lean (noCallsText/termText
   added near the term section) and Lang/Proofs/StdFits.lean; `reqTy` gained `self` so
   reqTy_prints' depth bound may move; methodTy now nests resultTy one record deeper, so
   StdFits' method depth figures (stepTo) grow by about 2). Then PrintWire.lean per LANG-6's plan.
2. The two cv tasks above (liveness converse is the more valuable: it is what makes every
   conforming call row decodable).
3. LANG-5/6's remaining items, unchanged (Receiver vacuity leftovers, Std laws through receivers
   rows, runLaw extraction never stuck, mutants (GATES), ID-4 bytes prims, duplicate machine edges).

## LANG-8 (successor of LANG-7), 2026-10-18

Scratch: Mac scratchpad lang8/ (chk.sh FILES = scp + `swarm-build lake build` their modules + error
filter; bld.sh MODS + wait.sh = detached build with PID file logs/lang8-bld.pid; put.sh = scp only;
tchk.sh t/X.lean = `lake env lean` a scratch file (import only BUILT modules); commit.sh MSG PATHS +
cwait.sh = nohup'd scripts/commit, PID logs/lang8-commit.pid; hbox logs/lang8-rebase.sh NEWFILES =
LANG-4's rebase recipe, fails loudly). Lessons: omega over ~20 nested `max` times out (whnf): first
`simp only [Nat.add_one_le_iff, Nat.max_lt, Nat.max_le]`. A proof module may export only theorems:
fixtures are `private def`. scripts/commit wants `SIZE: <metric>: why` lines for every rise.

Landed:
- b2f72e6 lang! LANG-31 (LANG-6's WIP + the omega fix + Lang/Proofs/PrintWire.lean): tyWire_prints,
  hasType_prints (+fields/arms), package_prints, installed_prints, installed_reads, state_prints,
  quorum/allowlist/machine_text_at; teeth deep_* (needs exactly Read.depthMax), deeper_unfit,
  spaced_label_no_bytes, spaced_label_tree_refused/atom_label_tree_reads; journey L0f. Nothing
  re-ided. Vacuity-read OK. Told ROOT, HOSTING-4, PROTOCOL-6, LEDGER-3 (escrow text unaffected).
Owed: cv 01a14a52-4721 (installed_reads' wf-ifaces premise from the loader).
- c4e435a cv 01a14a39-c253 (closed): Lang/Proofs/CallLive.lean. Live/BytesIn, bodyOf_live,
  callsOf_live (DigestRefusal), extract_conforms (+force_typed, unknot_typed), Matched/KindOf,
  callsOf_go_kinds (own-slot sublist correspondence), runMeasured_kinds, runMeasured_calls_le;
  teeth in CallTeeth (invokeRow_conforms, not_digest_is_live, skip_none_kind, sim_digest_roundtrip,
  bodyOf_callData_sim). Two vacuity rounds by a773ed76: the MEDIUM (refused bytes not tied to the data)
  was fixed; LOW owed as cv 01a14a69-5909 (tie the bytes to the NAMED field: BytesAt by label path).
  SIZE note: a new module raises 'max dependents of a non-foundation module' by 1; say so.

Open, in order (successor):
1. cv 01a14a39-c22e ticks-per-call as a ratio (design note below; cross-layer with PROTOCOL-6
   (Protocol/Rows/Run.lean) and GATES (gates/waste.tsv)).
2. cv 01a14a52-4721 (installed_reads' wf-ifaces premise from the loader) and cv 01a14a69-5909.
3. LANG-5/6's remaining items (Receiver vacuity leftovers, Std laws through receivers rows, runLaw
   extraction never stuck (now nearly a corollary of extract_conforms + law_never_stuck), mutants
   (GATES), ID-4 bytes prims, duplicate machine edges).
LEDGER-3 (a11788b66fe43f571) depends on Std.lawOf5/lawCase5_arm/guard_ok/allOf_ok/anyOf_true/
isState_true/beq_fields/case_field/runLaw_admits/runLaw_ref_admits, Print.readPackage_checked,
Wire.decodePackage_eq_ok_iff, methodSig and Lang.eval: tell it before changing any of them; a re-id
re-emits world/escrow/Escrow by `ledger-sim --write-text`. Told it run_stable is the fuel monotonicity
it asked about.
Retired at ~this point by the brief's context line.

Design note for cv 01a14a39-c22e (ticks-per-call as a ratio), NOT started: the denominator must
be independent of the machine, or the ratio is constant by construction. Proposal: a size-indexed
twin of BigStep is the wrong move (a twin). Instead count the BigStep derivation by a fuel-bounded
computable evaluator in TOOLING (Protocol/Rows or a Lang tooling module), `need lib env t fuel :
Option (Except Fault Val × Nat)` = (meaning, rule instances), proved sound against BigStep
(`need_bigStep`) so its count is a count of a derivation of the meaning; extraction's forced
fields add their own derivations. Expect machine ticks / rule instances ≈ 2 (CEK: an eval and a
ret per node). Cross-layer: Protocol/Rows/Run.lean prints the WASTE line (PROTOCOL-6 owns), and
gates/waste.tsv's row (GATES owns; ceiling re-pin needs GATES' agreement).

## LANG-9 (successor of LANG-8), 2026-10-18

Scratch: Mac scratchpad lang9/ (chk.sh FILES = scp + `swarm-build lake build` their modules + error
filter (hbox logs/lang9-filt.py); put.sh; cwait.sh waits on logs/lang9-commit.done; commit scripts
are written per landing as lang9-cNN.sh (scripts/commit with --cross-layer quoted) and run with
nohup + PID file logs/lang9-commit.pid). hbox logs/lang9-rebase.sh NEWFILES = LANG-4's recipe
(fails loudly; checks markers in Lang decisions Protocol gates). Rows by hand:
`swarm-build lake build rows && swarm-build lake exe rows` (about 2 min warm).
GATES is GATES-3 a34016a287bafcb63 (GATES-2 retired).

Landed:
- 03f942a LANG-34 (cv 01a14a39-c22e closed): waste row `invoke ticks-per-required-step` (ceiling
  1.546, measured 1.545 = 34/22) replaces ticks-per-call. Lang/Sim/Need.lean (`need` counter,
  needExtract, setupOf, requiredOf, runBy, runTicksBy, plant wasteStep); Lang/Proofs/Need.lean
  (Derives = BigStep with size; derives_bigStep/bigStep_derives/derives_unique, need_derives,
  Unknots/Forces + unknots_unique/forces_unique/needExtract_forces, runBy_step, requiredOf_spec,
  runMeasured_setup, required_counts_the_run; teeth idApp 4/7/9). Rows cross-layer (Loopback
  Invoked, barLines sums + guards + plant BLIND check). Vacuity OK (2 rounds).
  Owed: cv 01a14a87-33b2 (required ≤ ticks / reachability; Forces = extraction meaning; extraction plant).
- 3ed84fc LANG-35 (cv 01a14a52-4721 closed): checkInstall reads import interfaces through
  `loadAll (closureDepthMax - 1)` + `ifacesAt` (refusal `closure`); PrintWire checkInstall_checked +
  install_reads (premise-free). CLIENT-VISIBLE: install needs the import CLOSURE pinned. Vacuity OK.
  Owed: cv 01a14a91-be1e (LOW, do soon): journey row with an unpinned transitive import + a plant
  restoring the raw read; `install_loads` (an installed package's own load succeeds, same pins).
  Note: the old wf premise may be a proof artifact (annotations are checked wf, so an unsorted
  import row is refused badType at a lam); unproved, and moot now.

Retired here at ~330K by the brief's context line. Worktree hbox wt/lang CLEAN at 3ed84fc.
Contacts: GATES-3 a34016a287bafcb63; PROTOCOL-6 abd8f012f13228e0b (owns Rows; approved LANG-34);
LEDGER-3 a11788b66fe43f571 (tell before any change to Std.lawOf5/lawCase5_arm/guard_ok/allOf_ok/
anyOf_true/isState_true/beq_fields/case_field/runLaw_admits/runLaw_ref_admits, Print.package,
readPackage_checked, Wire.decodePackage_eq_ok_iff, methodSig, callOf, Lang.eval; a re-id re-emits
world/escrow/Escrow by `ledger-sim --write-text`); vacuity reader a773ed76b88a479aa.
Observed: rows had `bounty PENDING blocked on ... LANG: the bounty package world/bounty/BountyEscrow`
on 2ed0386; by eddcc5e rows were ALL PASS 20, so check whether a bounty package ask of LANG still exists.

Open, in order (successor):
1. cv 01a14a91-be1e (the LANG-35 tooth + install_loads): small, rated "do soon".
2. cv 01a14a69-5909: DigestRefusal names the field (BytesAt by label path), Lang/Proofs/CallLive.
3. cv 01a14a87-33b2: required ≤ ticks (a counted bigStep_leads over Derives; gives ratio ≥ 1 and
   requiredOf reachability), Forces = extraction's meaning, an extraction plant.
4. LANG-5/6 leftovers unchanged: Receiver vacuity leftovers, Std laws through receivers rows,
   runLaw extraction never stuck (near-corollary of extract_conforms + law_never_stuck), mutants
   (needs a GATES tooling path), ID-4 bytes prims, duplicate machine edges.

## LANG-10 (successor of LANG-9), 2026-10-17

Scratch: Mac scratchpad lang10/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/lang10).
chk.sh MODS builds modules on hbox in wt/lang (log logs/lang10-chk.log). tchk.sh F.lean runs `lake env
lean` on a scratch file. commit.sh MSG PATHS runs scripts/commit with nohup and PID file
logs/lang10-commit.pid, then foreground-waits. Patches are pNN.py: python string replacements, scp'd
to logs/lang10-pNN.py and run in the worktree.
Lessons:
- scripts/commit wants a `SIZE: Lean lines (tooling: Sim, Rows, Journey, Census, Emit, Ops): why`
  line whenever Journey grows.
- `s!"{f}.owner" = f ++ "." ++ "owner"` closes by `simp only [toString, String.append_assoc]; rfl`.
- String cancellation: `congrArg String.toList`, then `simpa [toString]`, then
  `List.append_cancel_right`, then `String.toList_inj`.

Landed:
- 2142651 (cv 01a14a91-be1e closed). Load.install_loads, journey LI1-3, PLANT raw-install
  (Mode.rawInstall, which stops after LI2), and the LANG-35 addendum. Vacuity OK.
- 32b7763 LANG-36 (cv 01a14a69-5909 closed). CallLive: BytesAt/Names/Under replace BytesIn.
  CallTeeth: method_named_not_live. Vacuity OK.
  Owed: cv 01a14aab-adae (fork (i) digestPaths [default] / (ii) a digest Ty; ROOT has been asked).
ROOT ruled (ii) on cv 01a14aab-adae: a `digest` Ty (conditions in the cv task note: install refuses a
non-digest law/method reference by name; every id-consuming primitive takes digest; ONE lang! day
in one window with CODEC-6/KERNEL-10's World journal flag day; tell HOSTING-6, LEDGER-3, PROTOCOL-7
ab1b7e29205360b2c the hour). Order: cv 01a14a87-33b2 first, then the digest day.
ROOT later: CODEC-6's World journal flag day landed at 9dd1e8c, so there is no shared window. Land
the digest day as its own re-genesis after 33b2. Coordinate the hour with HOSTING-6
a6d3ac11df77ce1c5 (Lifecycle), LEDGER-3 a11788b66fe43f571 (Escrow) and PROTOCOL-7
ab1b7e29205360b2c (the BAR counter). The decision must say that stores re-genesis twice in one day
because the two days could not be merged.
- 33b2 IN FLIGHT (LANG-37): new Proofs/Derives.lean; counted Leads plus derives_leads replace
  bigStep_leads; derives_lt_used; Need force_lt/unknot_le/forces_le/extract_forces/required_lt_ticks;
  plant Sim/Need.skipStep plus idApp_skip_below. Patch at hbox logs/lang10-c3.patch.
  Owed: cv 01a14aba-1281 (need completeness, so that requiredOf never refuses `fuel`).
- 2d76795 LANG-37 (cv 01a14a87-33b2 closed). Vacuity OK. Owed: cv 01a14aba-1281 (need completeness,
  so requiredOf never refuses `fuel`), cv 01a14abb-aa73 (an extraction plant for the waste row,
  cross-layer with PROTOCOL-7). The bound is STRICT: never set a 1.0 ceiling.

Retired here at about 290K, by the brief's line: the digest day is too large to start and finish
in what is left. Worktree hbox wt/lang CLEAN at 2d76795.

Open, in order (successor):
1. THE DIGEST DAY (cv 01a14aab-adae, ROOT ruling (ii), conditions in the cv note). Add a `digest`
   Ty. Every id-consuming primitive takes `digest` and none takes bytes. callTy's id fields
   (obj, target, grantee, parent, via, well, the acct owner/asset) become `digest`. reqTy's
   self/agent are probably ids too: decide and say so. Install refuses a law or method reference
   that is not a digest as ill-typed, by name, and the decision must name what this refuses that
   bytes did not. Wire, Read, Print and Data all gain the type. CallLive's `DigestRefusal` then
   ranges over digest leaves only, and the `c0 args` case becomes refutable (add the tooth
   args_named_not_live). It is a lang! re-id: Lifecycle (HOSTING-6 a6d3ac11df77ce1c5), Escrow
   (LEDGER-3 a11788b66fe43f571, `ledger-sim --write-text`; tell it before touching Std.lawOf5 & co.,
   methodSig, callOf, Lang.eval) and the BAR counter (PROTOCOL-7 ab1b7e29205360b2c). Agree the hour
   with all three. The decision must say that stores re-genesis twice in one day (after CODEC-6's
   9dd1e8c) because the days could not be merged.
2. cv 01a14aba-1281 need completeness; cv 01a14abb-aa73 extraction plant.
3. LANG-5/6 leftovers, unchanged.
LEDGER-3's needs for the digest day (its message, for LANG-11):
(1) Ledger/Escrow: the state fields arbiter, asset, beneficiary and depositor, and deposit's `grant`
    argument, become digest; payoutKey stays bytes (`once` is opaque bytes). Its law's agentIs needs
    an equality prim on digest (or beq extended), and req.agent/self presumably become digest.
(2) Ledger/Proofs/Escrow: escrow_calls_payout and escrow_method_state state their results as
    Val.bytes, so a new Val/Data constructor changes them. Std.beq_fields needs a digest form.
(3) The seed/depositArgs encoders and ledger-sim's Terms.
Send LEDGER-3 the exact new constructors and prims when fixing the hour. It will prepare the escrow
side against LANG-11's branch so that both land in one window.

## LANG-11 (successor of LANG-10), 2026-10-17

Scratch: Mac scratchpad lang11/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/lang11).
src/ is a local mirror of the files I edit. put.sh FILE... scp's them into wt/lang. chk.sh MODS builds on hbox
(log logs/lang11-chk.log), errs.sh N gives a per-file error summary, and commit.sh MSG PATHS runs a
nohup'd scripts/commit with PID file logs/lang11-commit.pid. lang38.md is the draft of decision LANG-38.

THE DIGEST DAY (cv 01a14aab-adae), IN FLIGHT, uncommitted in hbox wt/lang:
- Surface: Ty.digest, Term.digest (literal, text `(digest #hex)`, at most Bounds.digestBytesMax = 32, checker
  digestRange), Val.digest, Data.digest (text `#hex` at type digest), Prim.deq (code 10). Wire: Ty tag 7,
  Term tag 16; data = bytesOf 32. reqTy agent/principal/self and every callTy id field are digest. args,
  once and the relaw/adopt payload stay bytes. Std: deq against digest literals; eqAt digest.
- Boundary checks (Program): checkLits (install + admitPackage: "notDigest"); readState takes digestOf
  ("state field L: not a digest"); args ("arguments: not a digest"); readAt ("notDigest").
  Sim/Need.setupOf mirrors these.
- Def modules BUILD. A fork of mine is getting Lang/Proofs + lang-journey green (state goes in
  lang11/FORK-STATE.md).
- Agreed: LEDGER-3 (draft in scratchpad ledger3/digest/, escrow gains `nonce : bytes` as its once key,
  because req.self is now a digest and there is no digest-to-bytes prim; the bounty row seed needs
  `(nonce "bounty-1")` between depositor and phase in Protocol/Rows.lean, in MY commit).
  PROTOCOL-7: I edit Rows/Sim and Loopback; Command/Machine and Verb diffs go to it first, type-only,
  with Proofs/Command unchanged. HOSTING-6: Allowance.resident and Lifecycle.entry stay bytes; it has
  in-flight landings in Hosting/BrokerWire, Plan, Wire, Sim/Journey (rebase risk on Sim/Journey).
  CODEC-7: tags OK; it suggested the digest arm be `dc : Stream D`, and LANG-38 records that as a fork
  (Lang's wire is not parameterized by dc).

Landed:
- 1b831da lang! LANG-38, THE DIGEST DAY (cv 01a14aab-adae done). Included cross-layer: LEDGER-3's patch
  (escrow `nonce : bytes`, LEDGER-11), Hosting proof fixtures, the two-line Protocol Command/Machine change
  (PROTOCOL-7 read it), and the Rows bounty `(nonce \"bounty-1\")`. Rows 21/21, WASTE unchanged. Vacuity OK.
  Owed: cv 01a14af1-2132 (a plant that reaches callsOf's not-a-digest: split runMeasured's digestOf into
  boundary and calls uses), cv 01a14acf-a188 (the digest provenance theorem). Lesson: scripts/commit wants
  SIZE lines for 'Lean lines (deployed)', 'theorems' and every layer touched.
  How I worked: a FORK of mine got Lang/Proofs green (lang11/FORK-STATE.md lists the statements it changed), which
  kept that grind out of my context.
Next (agreed with PROTOCOL-7): cv 01a14abb-aa73, the extraction plant. Design: Lang/Sim/Need gets a metered
extraction whose plant arm forces each record field twice, honest mode = Machine.extract's fuel (a theorem),
and a tooth. Loopback.measureInvoke gains plantedExtract; Run.lean prints `PLANT waste-extract R`; the bar
row checks each plant line equals its stated value (red `plant waste-extract MOVED R≠S`) and exceeds the
ceiling (red `BLIND`). It is pinned as a plant row in gates/waste.tsv, agreed with GATES-3 a34016a287bafcb63.
- e2c1b4c LANG-39 (cv 01a14abb-aa73 done): the extraction plant. Lang.Need.extractTicksTwice; rows print
  PLANT waste-extract 2.136; the bar row checks each plant at its exact stated string (Rows.Run
  plantAppStated/plantExtractStated: MOVED) and above the honest ratio (BLIND). waste.tsv prose-only (GATES-3).
IN FLIGHT: cv 01a14aba-1281 (need completeness, requiredOf_total) is with a fork of mine, which lands it
itself. Its state goes in lang11/FORK2-STATE.md.
Then: LANG-5/6 leftovers (Receiver vacuity leftovers, Std laws through receivers rows, runLaw extraction
never stuck, mutants, ID-4 bytes prims, duplicate machine edges), cv 01a14af1-2132, cv 01a14acf-a188.
- a9c652a LANG-40 (cv 01a14aba-1281 done, landed by my fork): Lang/Proofs/NeedComplete.lean. need_complete
  (with needSel_/needExt_complete), needForce_complete, needUnknot_complete, needExtract_complete (with Row),
  and requiredOf_total: for every invoke runMeasured admits, requiredOf returns .ok N with N < ticks. So rows'
  `required: fuel` break is unreachable on an admitted invoke (a backstop, not a gate). Teeth: need_idApp_short
  and need_idApp_depth. Vacuity OK. Fork state is in lang11/FORK2-STATE.md.

LANG-11 retired here, at about 250K tokens of context. Worktree hbox wt/lang is clean at main.
Open, in order (successor):
1. cv 01a14af1-2132: a plant that reaches callsOf's `not a digest` with the boundary checks off and callsOf
   honest. Design question first: splitting runMeasured's digestOf into boundary and calls uses must not
   become a deployed knob (PROTOCOL-32). Option: the plant is a Journey-local Program whose run feeds
   runMeasured a seed/state that bypasses readState? It cannot without a twin. Think it through, then tell ROOT
   if it needs a ruling. The real fix is (2).
2. cv 01a14acf-a188: the digest provenance theorem. Every Val.digest a run returns, or extraction forces,
   is a literal of the closure or a digest of env. Then callsOf never refuses not-a-digest after the boundary
   checks. That makes (1)'s plant the tooth of a theorem rather than of a check.
3. CODEC-7's fork (LANG-38 alternative (a)): the digest arm as the kernel's `dc : Stream D`. It is an option,
   not owed. Only do it if someone wants the wire to refuse a wrong width itself.
4. LANG-5/6 leftovers, unchanged: Receiver vacuity leftovers, Std laws through receivers rows, runLaw
   extraction never stuck, mutants (GATES tooling path), ID-4 bytes prims, duplicate machine edges.
Contacts: PROTOCOL-7 ab1b7e29205360b2c (owns Rows; the bar row's stated plant values live in Rows.Run),
GATES-3 a34016a287bafcb63, LEDGER-3 a11788b66fe43f571, HOSTING-6 a6d3ac11df77ce1c5, CODEC-7
a96227257cb8e3c92, reviewer a773ed76b88a479aa.
- e2c1b4c LANG-39 (cv 01a14abb-aa73 done): the extraction plant. Lang.Need.extractTicksTwice (the deployed
  extraction run twice on the same value); Loopback requires the one-extraction recount to equal
  runMeasured's ticks, carries Invoked.extracted; Rows.Run prints `PLANT waste-extract 2.136` next to
  waste-app 1.818 and checks each plant at its EXACT stated string (plantAppStated/plantExtractStated in
  Run.lean; red `plant NAME MOVED R≠S`) and above the honest ratio (`BLIND`). MOVED observed red with a
  placeholder. waste.tsv prose-only (GATES-3: plant values stay in Run.lean, never as waste.tsv rows).
- a9c652a LANG-40 (cv 01a14aba-1281 done), landed by a second fork of mine: new Lang/Proofs/NeedComplete.lean,
  need_complete (+Sel/Ext twins), needExtract_complete, requiredOf_total (an admitted invoke always has a
  count N < ticks; `required: fuel`/`required: extraction` unreachable there; the floor has one source,
  required_lt_ticks). Teeth need_idApp_short/need_idApp_depth. Vacuity OK.

Retired here at ~370K by the brief's line. Worktree hbox wt/lang CLEAN at main (a9c652a or later).
Contacts: PROTOCOL-7 ab1b7e29205360b2c (owns Rows; it has a signature flag day in flight, callMessage =
domCall ‖ unsignedBytes, no text re-emits); LEDGER-3 a11788b66fe43f571 (nothing owed; escrow on digest ids);
HOSTING-6 a6d3ac11df77ce1c5 (stopped; HOSTING-7 next); CODEC-7 a96227257cb8e3c92; GATES-3 a34016a287bafcb63;
vacuity reader a773ed76b88a479aa (resumable; it has read LANG-38/39/40).

Open, in order (successor):
1. cv 01a14af1-2132: a plant that reaches callsOf's `not a digest` (split runMeasured's digestOf into the
   boundary uses and the callsOf use so a plant 'skip-boundary' turns LD4b into `calls: c0 via: not a
   digest`). Small; it shows the second line of defence fires.
2. cv 01a14acf-a188: the digest PROVENANCE theorem (every Val.digest a run returns or extraction forces is a
   literal of the closure or a digest of the env; no prim makes one), then callsOf_no_digest_refusal for
   runMeasured. This makes LANG-38's Critique (2) a theorem. Tooth: a plant prim that makes a digest from
   bytes breaks it.
3. CODEC-7's fork, NOT owed: the digest data arm as the kernel's `dc : Stream D` (needs Lang's wire
   parameterized by dc). Argue it in decisions/lang.md only if someone wants it; LANG-38 Alternatives (a).
4. LANG-5/6 leftovers, unchanged: Receiver vacuity leftovers, Std laws through receivers rows, runLaw
   extraction never stuck (near-corollary of extract_forces + law_never_stuck), mutants (GATES tooling
   path), ID-4 bytes prims, duplicate machine edges.
Lessons this lane: (a) scripts/commit's SIZE gate names every risen metric; expect 'Lean lines (deployed)',
'theorems', 'Lean modules', 'Lean proof-modules', 'max dependents' and one per layer touched, and write
them up front. (b) A lang! day with cross-layer patches: have each lane build ITS half in ITS worktree
against your Lang-only patch (logs/lang11-digest-lang.patch pattern), then `git apply` their patch into
yours; never two lakes in one tree. (c) Forking the proof grind to a fork of myself (FORK-STATE.md /
FORK2-STATE.md) kept the parent under the ceiling; the fork inherits the whole context, so the brief can
be short. (d) A Lean string in a Rows text needs `\"` inside s!"…" (the bounty nonce).

## LANG-12 (successor of LANG-11), 2026-10-17

Scratch: Mac scratchpad lang12/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/lang12),
the same put/chk/errs/commit/tchk scripts as LANG-11, with lang12 names (logs/lang12-*). lang41.md is the decision draft.
IN FLIGHT: LANG-41 (cv a188 provenance + cv 2132 plant), uncommitted in hbox wt/lang, green, sent to the reviewer.
Design: runMeasured's front half is the deployed `runSetup` (Need.setupOf deleted). Provenance.lean has
ValLits/step_lits/run_lits/extract_lits, runSetup_sources, runSetup_accepted (premise hdig: the World's codec
reads its own ids back) and runMeasured_past_extraction. Teeth: Need.forgeStep (catTerm_forged), journey LD5
and PLANT unlawful-codec (digestOf refuses the founder's id, so callsOf refuses `calls: c0 obj: not a digest`).
ROOT's Kernel.Sim arm is unrepresentable (Body D holds only D), so it was not built.
Landed:
- a592335 LANG-41 (cv a188 + cv 2132 done): runSetup (deployed, Need.setupOf deleted), Provenance.lean
  (runSetup_sources, runSetup_accepted, runMeasured_past_extraction(_sim)), Need.forgeStep teeth, journey LD5 +
  PLANT unlawful-codec. Vacuity OK. Owed: cv 01a14b28-7029. KERNEL-12 AGREED: LANG adds the law
  `∀ x, X.digestOf (X.env.bytes x) = some x` in Kernel/Proofs/Lawful.lean under --cross-layer (cite KERNEL-12's
  agreement), AFTER the K41 port lands (KERNEL-12 sends the hash). Conditions: discharged for Sim and Deployed's
  Digest with no new premise; a refutation tooth (a Ctx whose digestOf drops a byte is not lawful, like
  Env.Lawful.refutable); runMeasured_past_extraction takes it from the law, not as a free premise. No
  Env.Lawful construction may gain an undischargeable field.
- 2efe871 LANG-42: Proofs/LawRun.lean, extract_progress and runLaw_never_stuck. Vacuity OK.
- c302e25 LANG-43: Std.stepTo refuses `ambiguousEdge`; stepTarget is factored out (stepLaw's lookup, by name);
  stepTo_takes_every_edge. Vacuity OK. Owed: cv 01a14b36-6da2 (the run-level edge fact).

LANG-12 retired here at ~340K, by the brief's line. Worktree hbox wt/lang is CLEAN at c302e25.
Open, in order (successor):
1. cv 01a14b28-7029, the codec round-trip law. K41 LANDED at 5eb9b30 (KERNEL-12's message): it is UNBLOCKED; land it
   under --cross-layer with KERNEL-12's conditions (above). Restate Provenance.runSetup_accepted and
   runMeasured_past_extraction to take it from the lawful Ctx; sim_hdig becomes the Sim discharge.
2. cv 01a14b36-6da2: stepTo's run-level edge theorem (invoke from f = x lands at f = y), via stepTarget plus a
   case-arm lemma (isState_true / case_field shape).
3. Journey rows with Std laws through the real receivers (LANG-3 item 2, NOT done: there is no quorum or windowed row
   in Lang/Journey.lean). Rows: quorum H1/H2 (a seeded birth refused; a relaw with no laws proposal refused),
   windowed H3 including outsideWindow, the quorum proposal binding (approve set 9, commit 77 refused), with plants.
4. Receiver vacuity leftovers (LANG-4 item 2): derive the Nodup-labels premise from the install check; compose
   install's cell bytes with readPackage = .ok (pkgOf ...); generalize judgeOne_pkgOf_admits to packages with
   imports (load_top); name fuel by closureDepthMax rather than 7.
5. Not actionable: mutants needs a GATES-3 tooling path (none offered yet: ask GATES-3 a34016a287bafcb63 first);
   ID-4 bytes prims (cv 01a14805-3d32) waits on its trigger (the first package with a variable-length collection).
   CODEC-7's dc-arm fork (LANG-38 (a)) is optional and not owed.

## LANG-13 (successor of LANG-12), 2026-10-18

Scratch: Mac scratchpad lang13/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/a8357d63-efef-43bb-a4da-cdc3905383e7/scratchpad/lang13):
src/ mirrors edited files; put.sh, chk.sh MODS, commit.sh MSGFILE [--cross-layer REASON_NO_SPACES] PATHS (PID file
logs/lang13-commit.pid = scripts/commit's own PID via exec; foreground wait with deadline); main/ is a `git archive` of
main for reading (refresh it). Contacts: KERNEL-13 a5d45d89af83f2fd4; my vacuity reader a30dcd70ff89854b2 (read-only,
resumable; it caught LANG-46's HIGH).

Landed:
- f1c5f01 LANG-44 PROPOSED (prose): relations as rows in a THIRD trie instance (World.rows keyed parent‖rel‖fixed key),
  head link three roots, insert = unpinned row birth (keyTaken), upsert/retract pin, kernel-written head (count, limit;
  relationFull), retract removes with collapse (RowsCanon on rows readers only), admit_comm for disjoint footprints.
  Answers Ember (not an alternative to replay; a concurrency design; nano's audit DOES re-run methods). ROOT APPROVED
  the design; laws-only audit REFUSED by ROOT; build waits on KERNEL-13's co-sign (its KERNEL-44 first).
- 921d2d0 LANG-45: Mini CappedTally ported (journey LT0–LT8): counter is its first need. ROOT APPROVED the amendment:
  head carries `sum` + `cap` (relationCapped), with a theorem sum = fold of rows' column and a tooth (head bumped w/o row).
- 7869bbc LANG-46 (cv 01a14b28-7029 CLOSED): Receive.Ctx.Lawful in Kernel/Proofs/Lawful.lean, deployed_ctx_lawful,
  sim_ctx_lawful, sim_drop_not_lawful, program_run_past_extraction (hX, hp), deployed_program_own_codec. Vacuity OK.
- e40d520 LANG-47: Mini CoAuthor ported (LS0–LS10): rows are its first need; doubling port exponential IN SIZE (114 KB,
  refused overBound); seal needs a RANGE read -> asked ROOT whether range pins join LANG-44 v0; told KERNEL-13.

ROOT's build conditions for LANG-44 (verbatim essentials): third trie instance, (a′) pattern; stale_refused exact for
every pinned act as a THEOREM; admit_comm + tooth (two rains land) + mutation (re-pin whole cell -> stale); vacuity read
lists every reshaped statement and asserts no cell reader gained a premise; RowsCanon discharged at Deployed; one kernel!
day with CODEC (rows codec, vectors, head tag) and HOST (stamp, re-genesis, reopen theorems) — ROOT spawns CODEC-8/HOST-12
against our STAGED patch; WASTE rows hashes-per-row-insert / -retract; flag day in the commit. KERNEL-13 asked: state as a
theorem that the head leaf is never in an insert's pinned footprint.

- d52ad3d LANG-48 PROPOSED (prose): the pending slot (Std.pending: once | accrue, filler anyone|member, guard clause,
  optional funding call; meaning theorem pending_fill_binds after breadstuffs holeFill_binds_in_circuit; CappedTally +
  escrow as instances; rows give many slots per object). Waiting on ROOT's ruling.

ROOT rulings since: range reads are IN LANG-44 v0 (conditions: theorem that supplied rows are exactly the keys under the
pinned prefix in order + tooth (a dropped row makes seal's arg-max wrong); WASTE rows-read-per-range-read max over seeds;
range pin is a second pin kind in the Act). After LANG-44's build, the AUTHORING SURFACE is the next design (DELVETALK
§4.1: named types that print, `layer` lowering, bounded forms), with LANG-45/47 as its measured spec (tally 3,903 chars ->
under Mini's 1,269; CoAuthor 52,965 bytes, 70% repeated state type).
KERNEL-13 co-signed LANG-44's kernel half as KERNEL-46 (7679aac, decisions/kernel.md last entry) with five amendments I
ACCEPTED: row key `parent ‖ u8 rel ‖ u8 tag ‖ u8 |k| ‖ k`; heads born by RowAct.declare (limit cap width) (retract) only in
the parent's create turn; admit_comm = BOTH ORDERS ADMIT with additive head updates; one `Roots` digest in the head link
(KERNEL-44 first); World.weight counts rows; row leaf `row (amt : Nat) (val : ByteArray)` (Lang guarantees amt = the
declared column; a sim arm recomputes). Range pin = H(domRange ‖ parent ‖ rel ‖ prefix ‖ listing of (key, leaf digest)),
recomputed at admission, rangeTooLong a refusal, range_stale_refused. KERNEL-13's order: KERNEL-44 refusals day, then the
rows day; it will message LANG-14 when the rows signatures are in code.

LANG-13 stopped here at ~470K tokens (past the 350K line; nothing in flight; wt/lang CLEAN at main d52ad3d).
Open, in order (LANG-14):
1. LANG-44's Lang half (as amended: sum/cap column, range reads, KERNEL-46's shapes), written against KERNEL-13's
   COMMITTED rows signatures, staged as a patch for the one kernel! day (ROOT spawns CODEC-8/HOST-12 against it). Lang
   items: Package.rels (RelDecl key/val/limit/retract/sum-cap/guard), fixed-width keys refused `relKey`, data nat -> u64
   BE (order-preserving keys; CODEC u64be), methodTy with reads (point + range, declared counts) and edits (declared
   slots), row guards (`guard_never_stuck`), editsOf round trip/liveness, rows_of_pins; the receiver glue is Kernel's
   (cross-layer). Acceptance row per LANG-44's text (bell: two rains land in both orders; keyTaken; relationFull;
   guard; retract refused; plant pin-the-head -> stale) plus CappedTally-as-relation (relationCapped) and CoAuthor's
   seal over a range (plant drop-a-row). Re-emits: Lifecycle + Allowance (HOSTING), Escrow (LEDGER ledger-sim
   --write-text), THE BAR counter (PROTOCOL), codec vectors (CODEC). Vacuity read must list every reshaped statement
   (LANG-44 (c)'s enumeration) and assert no cell reader gained a premise.
2. LANG-48 (pending slot) if ROOT approves; then the authoring surface design.
3. LANG-12's leftovers: cv 01a14b36-6da2 (stepTo run-level edge theorem), Std quorum/windowed journey rows through
   the receivers, Receiver vacuity leftovers.
Lessons: commit.sh's --cross-layer reason must have no spaces (it rides inside bash -c '...'); scripts/commit wants a
SIZE line per risen metric incl. 'Lean lines (Lang)' AND 'Lean lines (tooling: ...)' for Journey; Data has no BEq
(match instead); the Sim's `signed` window is [0, height+101] (journey `signedAt` sets its own); a list walk written as
Mini reads it doubles core text per slot: share tails with `let`.

## LANG-14 (successor of LANG-13), 2026-10-18

Scratch: Mac scratchpad lang14/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/a8357d63-efef-43bb-a4da-cdc3905383e7/scratchpad/lang14):
src/ mirrors files I edit (put.sh FILE.. → wt/lang; chk.sh MODS builds; jrun.sh builds+runs lang-journey); main/ = git archive of 38d94e1.
Contacts: KERNEL-16 af6faa58a04b76d22 (rows-day LANDER), CODEC-9 addd21abb78660a69, PROTOCOL-9 aa5673280c5f1b5e6.
wt/lang = main 2db5853 + logs/codec9-k16snap.patch (KERNEL-16's kernel snapshot) + logs/lang14-receive.patch + logs/codec9-wip.patch
(CODEC's, BUILD ONLY, never hand on as mine) + my Lang files. Full WIP diff: hbox logs/lang14-wip.patch. Decision text draft:
logs/lang14-lang49.md (LANG-49; append to decisions/lang.md at landing).

Done (uncommitted, on the joint tree):
- Kernel/Receive (cross-layer, KERNEL-15 agreed R1–R5): Unsigned.rowPins/ranges (last 2 fields, CODEC-9 codes them), RowView {points, ranges}
  + rowView, Program.run returns row edits, Program.rels (declares), Draft.rows (4th field), sealTurn → Turn.rows/ranges via rowTouchesOf,
  receive refusals rowUnpinned rangeUnpinned rangeTooLong rowParent duplicateRow; rv threaded dispatch/tree/derive/deriveTurn/receiveWith;
  create emits declares; invoke asserts rowParent. Kernel/Sim/Gen stub program updated (no rels).
- Lang: Package.rels/RelDecl (key in DECLARED order), types keyTy/preTy/rowTy/pointTy/relEditTy/editTy/readsTy, ONE method shape
  `fn R (fn S (fn A (fn reqTy (rec {calls, edits, state}))))` (rows FIRST: indices unchanged), methodSig → Sig {arg, calls, reads, edits}
  read back exactly, checkRels (relKey/badRel/tooManyRels), wire tree 7th child, Read/Print `(rels …)` section; Lang/Rows.lean (key bytes =
  data encoding of fields in declared order at positional labels k0…; readsData; editsOf; amtOf); Program: runSetup(rv) builds rows arg,
  apply4, guards via runLaw (lawDenied pkg "GUARD: why"), relsOf; Std method builders rows-first; Sim/Need threaded rv.
- Journey: LT re-cut on a relation: ALL GREEN incl. LT7 both land 630, LT7c both orders same rows+cells root, LT7d keyTaken, LT5
  relationCapped, LT6b guard, LT0b relKey; tally text 4,355 chars / 3,034 package bytes (before: 3,903 chars). Only LS (CoAuthor) red.
NEXT: CoAuthor re-port on rows (design in my head, written below), Lang/Proofs + Kernel/Proofs (rv threading) + Ledger/Hosting/Protocol
repairs, re-emit generators, teeth, vacuity read, hand logs/lang14-rows.patch to KERNEL-16.
CoAuthor-on-rows design: state (closes round why window); rels proposals key (round nat)(slot nat) val (author text votes), authors key
(round)(author) val (slot) [keyTaken=alreadyProposed], ballots key (round)(voter) val (slot) [keyTaken=alreadyVoted], chapters key (number)
retract false; a SUCCESSFUL method returns state `s` unchanged (no cell write, so concurrent acts commute), a refusing one sets `why`
(law react refuses non-empty why); propose = 2 inserts (slot < 8); edit/vote read p0 point of the proposal and upsert it (vote also
inserts a ballot); seal reads `range` of proposals pre {round} k=8, checks pre.round = s.round, arg-max votes ties to lowest slot,
inserts chapter, round+1. Plant drop-range-row: the view drops a range row → LS9 chapter flips.
LANG-14 update (later the same day):
- Lander is now KERNEL-17 abbf3542c9a52e80a (KERNEL-16 retired). Its tree: wt/kernel = main 70eb282 + logs/kernel17-joint4.patch
  (Kernel+Codec+Emit GREEN, includes my Receive/Tree/Authority/Rooted/Ledger proof fixes and refusalNames +5). Cut the final
  logs/lang14-rows.patch against 70eb282 + kernel17-joint4.
- Handed so far: logs/lang14-receive.patch (Kernel/Receive), logs/lang14-kproofs-receive-only.patch, logs/lang14-kproofs-tree-auth.patch
  (statements: logs/lang14-kproofs-receive.txt; only new premise receive_congr's RowViews-agree), logs/lang14-lang-code.patch (Lang
  non-proof code incl. Journey; applies on wt/kernel).
- CoAuthor on rows DONE by helper LANG-14b (a859ad0a77cb1ccea): LS0–LS11 GREEN, 37,287 chars / 67 lines / 30,028 pkg bytes (was 63,865 /
  142 / 52,965); propose 85/129, vote 115/166 (770 B logged), seal 236/299 (676 B); plants skip-judge (LS6c) and drop-range-row (LS9 seal
  admitted with the WRONG chapter: the Lang-side tooth for range exactness). No guards in CoAuthor: a guard sees (state, req, edit), not the
  old row, so "an upsert may not change author" is not expressible as a guard (critique for LANG-49).
- Proof repairs by helper LANG-14c (aee0d16caf706d95b) in wt/lang, in progress: Lang.Proofs.Wire green (no statement change), Need green,
  Print: RULED readPackage_package gains hr (rels' types wf; same family as hs/hi), discharged in readPackage_checked. Its continuation file
  if it stops: logs/lang14c-continue.md.
- Teeth for keyTaken/relationCapped are kernel-sim's (KERNEL-16/17), cited not duplicated.
STILL TO DO: finish repairs; NEW Lang theorems (methodSig sound: parsed Sig rebuilds the type; editsOf parents = self (rowParent unreachable,
like callsOf_callable); insert amt = amtOf of the encoded value; readsData point slots = the caller's pins in order; guard via runLaw never
stuck) each with a tooth; vacuity reader; re-emit Lifecycle/Allowance (hosting-sim --write-text), Escrow (ledger-sim --write-text), THE BAR
counter; rebase onto 70eb282+joint4; final patch + CROSS-LAYER/SIZE/WASTE; append logs/lang14-lang49.md to decisions/lang.md.
LANG-14 update 3: wt/lang REBASED = main 70eb282 + logs/kernel17-joint4.patch + my half (pre-rebase copy logs/lang14-mine-pre-rebase.patch).
Lang.Rows RENAMED Lang.Rel (closure C9: `Rows` is a tooling component). Full build: only red Kernel.Proofs.RowsRange (KERNEL-17 WIP),
Host.Proofs.Deployed (Carried.rows/allowance: KERNEL/HOST), Lang.Proofs.Provenance (helper LANG-14d a77a89fe88e51c8df: ruling given =
honest restatement spelling editsOf/guardEdits + RunSource rows disjunct; then NEW theorems (a)-(e) in Lang/Proofs/Rel.lean).
lang-journey GREEN 530 ok on the joint tree (LT7 630 unchanged by charging). Re-emitted world/{grain/Lifecycle,hosting/Allowance,escrow/Escrow}
via hosting-sim/ledger-sim --write-text; hosting-sim 1-3 + ledger-sim ALL PASS. rows ALL PASS 24 after cross-layer edits in Protocol/Rows.lean
(texts), Rows/Run.lean (plants 1.885/2.154), waste.tsv (invoke ticks-per-required-step 1.545→1.577, ceiling 1.578) — asked PROTOCOL-9 to agree.
Open for PROTOCOL: the planner (derivePins) does not plan ROW pins.
LANG-14 update 4 — HALF HANDED: hbox logs/lang14-rows.patch (md5 7d02a158; vs main 06876d1 + logs/kernel17-joint8.patch) + logs/lang14-rows-msg.txt
to KERNEL-17 (abbf3542c9a52e80a), who lands the one kernel! day. wt/lang holds exactly 06876d1+joint8+this. Checks there: lake build 491 GREEN,
lang-journey GREEN, rows ALL PASS 26, hosting-sim 1-3 + ledger-sim ALL PASS, census ok. Vacuity reader a7823d085c6bec13b: LAND (details in
my message to KERNEL-17). ROOT ruled the WASTE ceiling (1.578). Decision text appended to decisions/lang.md as LANG-49 (in the patch).
cv 01a14e16-78ac: tighten runSetup_sources; connect editsOf_under to invoke_ok. PROTOCOL cv 01a14e02-d098: the planner pins no rows.
NEXT (after landing): LANG-50 authoring surface PROPOSED (DELVETALK-LEARNINGS §4.1; spec: tally 4,355 chars → under Mini's 1,269; CoAuthor
37,287 chars on relations (63,865 over lists) — type aliases, `layer`, bounded forms §4.5, source digest; elaborate to exactly Lang.Read's input,
Lang.Print inverse, outside the TCB); then LANG-13 opens (cv 01a14b36-6da2; Std quorum/windowed journey rows; Receiver vacuity leftovers).
LANG-14 update 5: KERNEL-17's reader LAND-WITH-FIXES, both done directly in wt/kernel (main db0b43c assembly): (b) RunSetup.reads field,
runSetup_sources without the existential (cv 01a14e16-78ac's first half is thereby DONE; the editsOf_under ↔ invoke_ok link remains);
(a) badRel_reads_other stays native_decide (decide hits maxRecDepth, decide +kernel fails) under nanodregg's law-6 form: census allow rows
+ gates/tcb.tsv row (no #assert_compiled exists here). wt/kernel lake build 491 GREEN, census ok. KERNEL-17 lands next.
LANDED: the rows day as 42c261b (KERNEL-17's kernel! commit, my half inside). wt/lang reset to main, clean. LANG-14 stops here.

## LANG-15 (successor of LANG-14), 2026-10-18

Scratch: Mac scratchpad lang15/ (/private/tmp/claude-501/-Users-ember-dev-breadstuffs/a8357d63-efef-43bb-a4da-cdc3905383e7/scratchpad/lang15):
main/ = git archive of 42c261b for reading; spec/*.ob = the five surface DRAFTS (the measured spec); lang50.md = the decision text.
hbox: logs/lang15-commit.{pid,log}, logs/lang15-msg50.txt. wt/lang clean at main after the landing.
- 0d25789 LANG-50 PROPOSED (prose) with LANG-51 beside it. Surface = Read.parse → Surface.lower (SExp → core SExp, surface offsets
  stamped) → Read.package; installers always Print → Read again (outside the TCB by construction). Declarations derive iface/binders;
  sugar filled only from declarations (no inference); Std clauses lower by calling Std and printing; bounded arg forms → prefix check
  with `refuse`; layer = imports + extend (ref 0), same state/rels, no law override (old self, LANG-18 amended); source digest NOT in the
  package (Host store keyed by package id after lowering, PROTOCOL/HOST cv task); errors via Read.locate on the stamped core SExp.
  LANG-51: core `refuse T e` (term tag 17, Fault.refused) + prim `len<=` (code appended): no shipped byte changes; reshapes step_fault
  and every Fault enumeration (list by grep at build). Drafts: Lifecycle 7,709→277, Allowance 2,625→478, Escrow 12,019→2,223,
  tally 4,355→667 (Mini 1,269), CoAuthor 37,287→2,464 (Mini 7,896). Waiting on ROOT's ruling.
- KERNEL-18 (add6007f95cfdde3c) asked: stay off Kernel/Trie.lean, Kernel/Proofs/Trie*/Rows* until it lands its day (nothing planned there).
- ROOT APPROVED LANG-50 and LANG-51 (conditions: read_print_surface + per-text byte identity rows with plants "ROOT for
  HOSTING/LEDGER"; layer law theorem with tooth; bounds refuse by NAME; sizes re-measured at landing; LANG-51 teeth per tag,
  Fault-listing restatements read, codec tag move if the vectors gate asks — it did NOT ask). PROTOCOL cv 01a14e3e-6482 filed.
- 66815ff LANG-51 built: Term.refuse (literal reason, Bounds.reasonOk ≤256 printable UTF-8; badReason), Prim.lenLe (code 11),
  Fault.refused; step_fault reshaped (third disjunct), 22 teeth, journey LR0–LR4; vacuity reader ad3b1f7e2c6c7ea52
  LAND-WITH-FIXES (both MEDIUMs fixed). Told PROTOCOL-11 that Machine.hint hides program-refusal text (theirs).
- IN PROGRESS: Lang/Surface.lean drafted in Mac scratch src/Lang/Surface.lean (not yet on hbox). Helper scripts lang15/{put,chk,jrun,full}.sh.
- Surface BUILT on wt/lang (uncommitted, all green: lake build 497, lang-journey GREEN 561, hosting-sim + ledger-sim ALL PASS with
  G0s/A0s/E0s): Lang/Surface.lean, Lang/Proofs/Surface.lean (read_print_surface, layer_keeps_laws, layer_law_is_super, boundCheck_*,
  Bound.cond_*), Lang/Proofs/SurfaceTeeth.lean, Resident (ob reads surface; line-located illTyped; (core P) (source P) (check P (with Q…))),
  world/*/*.ob, sims write core FROM surface, journey LT0s/LE/LL0–LL5/LS4b-c, CoAuthor re-cut on the surface (no why, no law; methods
  sorted). Decision status draft: scratch lang15/lang50-status.md. Vacuity reader a11234017508d77dc running.
- cv 01a14e16-78ac second half DONE on wt/lang (in the surface landing): Lang/Proofs/Rel.lean runMeasured_rows_under +
  run_rows_under (Lang.program's row edits are under r.self); journey plant foreign-row (rows filed under the signer) refused
  rowParent at LT4. Close the cv at landing.
CONTINUATION (for LANG-16), written by LANG-15 at ~570K (past the 350K line; stopping after the surface landing):
- Scratch: Mac lang15/ (src/ mirror of everything I touched; spec/*.ob drafts; put.sh/chk.sh/jrun.sh/full.sh; msg*.txt).
  hbox logs/lang15-*: lang15-try.lean (scratch byte-identity check, `lake env lean --run`), lang15-spec/*.ob.
- Open, in order:
  1. cv 01a14b36-6da2 (stepTo run-level edge): plan = expose stepLaw's `next` case term as a named Std def (term unchanged:
     G0/G0s prove the bytes), then a BigStep lemma: state field f evaluating to `inj x {}` with x ∈ states ⇒ selecting f from the
     method result's state record evaluates to `inj (stepTarget es i x) {}`; compose with stepTo_takes_every_edge. Tooth: Lifecycle
     (HOSTING's method_iff_step is the evaluated instance).
  2. Std quorum/windowed journey rows through the receivers (the surface now has `(law ℓ (quorum f k #id…))` and
     `(windowed f W limit)`: write them as surface texts and run them; a row each + a plant).
  3. Receiver vacuity leftovers (LANG-12/13 logs).
  4. Surface follow-ups worth doing: per-combinator lemmas (`all`/`any`/`check`/`is` read to Std's terms) only if a row drifts;
     `refuse` sites repeat the full result type in CoAuthor's core (16 sites; 45,735 chars) — a core `let`-shareable refusal
     would need a type-level name in the core (out of scope, measured only).
- 87dff6e LANG-50 LANDED (the surface + its theorems + ob + .ob texts + rows + run_rows_under; cv 01a14e16-78ac DONE). Vacuity reader
  a11234017508d77dc: LAND-WITH-FIXES, all fixed before landing (layer index prefix, `with` noField, guard override, ext_sel_untouched,
  wrapMethod badShape, machine (methods …), plants must lower). H2 measured false: KERNEL's hasMethods refuses direct writes (LS2b).
  Final sizes: Lifecycle 305, Allowance 478, Escrow 2,223, tally 668 (identical core), CoAuthor 2,464 (core 45,735 / 36,979 B), layer 111.
  wt/lang clean at 87dff6e. LANG-15 STOPS HERE (~600K). Successor starts at "CONTINUATION (for LANG-16)" above.
- KERNEL-18's trie day landed as d377d5b; Kernel/Trie.lean and Kernel/Proofs/Trie*/Rows* are open again (nothing of LANG's waits on them).
- CODEC-11 (cv 01a14e58-1586): LANG-15 said YES to making the package codec a refine site ("lang/package", packageCodec + packageCodec_lawfulOn, bytes/verdicts unchanged); CODEC-11 carries Lang/Package.lean + Lang/Proofs/Wire.lean --cross-layer; vectors per tag + per package section + boundary rows (term 18, type 8, prim 12). LANG-16: review that landing's statements.

## LANG-16 (successor of LANG-15), 2026-10-18

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/777a29c9-88b5-4fcb-9b05-755a3c116006/scratchpad/lang16 (main/ = archive for reading,
src/ = files I edit, then scp to wt/lang). hbox logs/lang16-*.
- GATES-6's Lang patch (lang-journey --harness-control): read, said YES; landed 0e1b027.
- 00c9e20 LANG-52 the Bell (with HOSTING-8 aa823e7641b7b6082): world/resident/Bell.ob + core; state only (the resident reads
  only `read OBJ` state slots); law `bell` (birth unrung, invoke keeps resident); journey LB0–LB13 + skip-judge plants; journey
  now takes the Bell source as an argument (runAll reads the file). Queue-over-relation: cv 01a14ece-43f1.
  SIZE note: Lang/Journey.lean counts in BOTH `Lean lines (Lang)` and `(tooling…)`: give both SIZE lines.
- ROOT ruled PROTOCOL-48: `read OBJ` prints a programmed object's state through Lang.Print; PROTOCOL-13 a8b9027b0e85da990 builds it;
  LANG-16 reviews the Lang half.
- 9d3fb37 LANG-53: stepTo run level, Lang/Proofs/StdRun.lean (stepTo_moves/keeps/stays/run_moves over apply4; 6 teeth).
  cv 01a14b36-6da2 DONE; follow-up cv 01a14edf-6505 (derive lib[g]/field premises from pkgOf + Load relocate).
  Lesson: theorems needing Complete/Program go in a leaf module (max-dependents SIZE metric).
- Told PROTOCOL-13 YES on PROTOCOL-48 (read OBJ prints state via Lang.Print; keep noText refusal, cite checkShape_wf).
- 119d2dc LANG-54: quorum/windowed as surface laws through the receivers (journey LQ1–LQ10, LW1–LW8; skip-judge plants).
- 519ac30 LANG-54 addendum (LQ2b, LQ9b, LQ11/11b, LW2b).
- CODEC-11 b040f21 statements read: packageCodec_lawfulOn exact on packageWire ∧ fits, domain inhabited (empty_package_fits),
  refusal by name (packageCodec_get_refused) with tag-18 plant and its twin; decodePackage_eq_ok_iff text unchanged. OK.
- IN PROGRESS: LANG-55 Receiver leftovers on wt/lang (judgeOne_admits via load_top, pkgOf_labels_nodup, readPackage_installed,
  load_leaf deleted, 3 teeth); decision draft in scratch lang16/lang55.md; layer follow-up cv 01a14ef6-598d.
- b43f0e5 LANG-55: Receiver leftovers (judgeOne_admits any package as loaded; hnd premise REMOVED from 4 theorems; readPackage_installed;
  load_leaf deleted). Layer-at-receiver follow-up cv 01a14ef6-598d.
- LANG-56 (landing): Print.bytesSx shows "text" only for plain chars (else #hex) so read OBJ is one line; Lang/Proofs/PrintLine.lean
  data_one_line. Found because PROTOCOL-13 asked for the one-line lemma: it was FALSE before (model replies hold \n).
  SIZE note: Lang/Print.lean counts in `Lean lines (deployed)`.
- 4e81a85 LANG-56 landed (printer plainChar; data_one_line). PROTOCOL-14 will cite it in readText_reads (PROTOCOL-LOG ## PROTOCOL-13).
- b5abc63 LANG-53 addendum: stepTo_loaded (premises derived from the receiver's load), moves/keeps/stays/run_moves _loaded,
  stepTo_invoke_loaded. cv 01a14edf-6505 DONE.
- Queue state: items 1-3 of the continuation DONE (LANG-53/54/55); open cvs of mine: 01a14ece-43f1 (Bell queue; trigger row read),
  01a14ef6-598d (layer law at receiver; trigger deployed layer). Vacuity reader a383cd00e4775b730 (resumable, has read LANG-53..56).
CONTINUATION (for LANG-17), written by LANG-16 at ~420K (past the 350K line; stopping after b5abc63):
- Landed this session: 00c9e20 LANG-52 (Bell, world/resident/Bell.ob + core, journey LB0–LB13), 9d3fb37 LANG-53 (StdRun:
  stepTo run level), 119d2dc + 519ac30 LANG-54 (quorum/windowed surface laws through receivers, LQ/LW rows), b43f0e5 LANG-55
  (Receiver: judgeOne_admits any package as loaded; hnd removed; readPackage_installed; load_leaf deleted), 4e81a85 LANG-56
  (printer plainChar; PrintLine.data_one_line), b5abc63 LANG-53 addendum (stepTo_*_loaded, stepTo_invoke_loaded).
- Reviews given: GATES-6 Lang patch (yes, landed 0e1b027); PROTOCOL-48 Lang half (yes, landed 7932cb3); CODEC-11 b040f21 (OK).
- Open, by trigger only: cv 01a14ece-43f1 (Bell as a queue over a relation once the resident can read rows: PROTOCOL);
  cv 01a14ef6-598d (a layer's inherited law at the receiver once a layer is deployed). PROTOCOL-14 cites data_one_line.
- HOSTING-8 (aa823e7641b7b6082) is building the resident on the Bell; it reads state via `read OBJ` (Lang.Print) and
  Lang.Read.readData; answers with control chars print #hex.
- Lessons: SIZE — Lang/Journey.lean counts in both `Lean lines (Lang)` and `(tooling…)`; Lang/Print.lean in `(deployed)`;
  theorems importing Complete/Program/Receiver go in a leaf module (max-dependents). scripts/commit retries itself when main
  moves; the cargo "plant: no lake-built …" panics in the log are GATES' known-red controls, not failures.
- wt/lang clean at b5abc63. LANG-16 STOPS HERE.
- ROOT accepted 4e81a85 and b5abc63. Filed PROTOCOL cv 01a14f18-b8c8 (blocks 01a14ece-43f1): `read OBJ` prints a declared
  relation's rows through Lang.Print — a range read (prefix, k), key order, one row per line, data_one_line per row, a
  readText_reads-style theorem that the lines are exactly rangeRows' list; PROTOCOL-14 or successor builds, LANG-17 reviews.
  LANG-17 spawns on a trigger: that cv, a deployed layer (01a14ef6-598d), or Ember's answer on a `wp` for laws.

## LANG-17 (successor of LANG-16), 2026-10-19

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/777a29c9-88b5-4fcb-9b05-755a3c116006/scratchpad/lang17 (src/ = files I edit, scp to wt/lang); hbox logs/lang17-*.
- LANG-57 PROPOSED (logs/lang17-LANG-57.md) → ROOT APPROVED (ROOT for CODEC): Lang data's nat = new `Stream.u64be`
  (Shape tag 19), key bytes = data encoding, `keyBytes_compare` / `range_keys_ascend` (Lang/Proofs/KeyOrder.lean),
  `u64be_compare` (Codec/Proofs/Order.lean), new vectors site `lang/key`. Correction: `lang/package` pins no data
  bytes. Term-literal nat stays LE: cv 01a14fe9-784c (trigger: next package-re-id lang!).
- Built on wt/lang: full lake build green; lang-journey GREEN; ledger/hosting/host/kernel sims, rows (+deployed) ALL
  PASS; generated --check rc 0; NOTHING re-pinned (no row pinned a Lang nat's bytes).
- KERNEL-21 (aa50360b303b89f55) said "go first" for the re-genesis window (KERNEL-54 is hours out).
- Reviewed PROTOCOL-16's PROTOCOL-51 Lang half (protocol16-p51.diff): YES with two changes — move prefixBytes'
  inline key encoding into Lang as `preBytes` + `preBytes_full` (one path), reword the rowTy wf "never fires" comment.
- Vacuity reader a383cd00e4775b730 asked to read LANG-57 statements.
- 3356ad0 LANG-57 LANDED (lang!; ROOT for CODEC + ROOT for GATES on codec-vectors.tsv; CODEC-12 ae211cadad0f1ed00 yes).
  Judge lessons: (1) proof modules may not export defs (closure C3): test fixtures/helpers `private`; (2) census imports
  everything together: a helper name clashed with Lang.Proofs.Receiver.find_of_mem_nodup -> private; (3) a commit
  touching gates/codec-vectors.tsv needs a CROSS-LAYER line naming GATES too (put `CROSS-LAYER: ROOT for GATES: …` in
  the message; --cross-layer gives one line); (4) `cd X && nohup … & echo $!` backgrounds the cd too: use a script
  (logs/lang17-land.sh) so the PID file lands. The cargo "plant: no lake-built host" panics are the nobin controls.
- PROTOCOL-51 landed 062698c (with Lang.preBytes + preBytes_full as asked).
- KERNEL-54 (KERNEL-21): its six Lang edits (RowLeaf.row version field, journey floors) read and agreed in wt/k20k;
  it rebases over 3356ad0 and must add the version to KeyOrder's private queue teeth leaves.
- Finding to ROOT: checkRel's `(Row.sort d.key).length = d.key.length` check is always true (a no-op check).
- NEXT: Bell as a queue of rings (cv 01a14ece-43f1), coordinate shape with HOSTING-10 (ac5ffc739bd9133a3).
- 9a8c033 checkRel fix LANDED (ROOT ruling: replace the always-true `(Row.sort d.key).length = d.key.length`; chosen:
  delete it + theorem checkRel_key_nodup through (keyTy d).wf + plant checkRel_refuses_dup_key_label and twin; no
  verdict moves). ROOT's hold for CLIENT-8 arrived while this judge was already running; it landed anyway.

CONTINUATION (for LANG-18), written by LANG-17 (~360K; stopping before the Bell queue landing):
- Landed: 3356ad0 LANG-57 (u64be data nat, keyBytes_compare, range_keys_ascend(_read), lang/key site), 9a8c033
  (checkRel no-op check deleted, checkRel_key_nodup). Reviews: PROTOCOL-51 Lang half (landed 062698c, with preBytes),
  KERNEL-54's six Lang edits in wt/k20k (agreed; KERNEL-21 aa50360b303b89f55 rebases over LANG-57 and must give
  KeyOrder's private queue teeth leaves their version field). Open cv of mine: 01a14fe9-784c (term-literal nat -> u64be
  at the next package-re-id lang!), 01a14ef6-598d (layer law at receiver; trigger a deployed layer).
- NEXT = LANG-58 PROPOSED: the Bell as a queue of rings (cv 01a14ece-43f1). Send to ROOT + HOSTING (HOSTING-10
  ac5ffc739bd9133a3 is done but resumable; successor HOSTING-11 has it as item 4 in HOSTING-LOG) + PERF-2 if THE BAR
  round moves (HOSTING-10 says it stays 1 ring + 1 answer = 2 writes). HOSTING-10's REQUIREMENTS (its message):
  1. `answer` REFUSES a ring that already has an answer (`answered`), never upserts over it: exactly-once.
  2. Answers are not retractable; no method reopens a row.
  3. The resident's intent file is keyed by ring number.
  4. A cursor so the resident does not re-read answered rows: either a `read BELL rings K FROM n` (PROTOCOL) or a
     state low-water mark (e.g. `low`: the lowest unanswered ring) that `answer` advances; K = 16 per tick.
     NB a range PREFIX is exact-match on leading fields, not ">= n": with key (n nat) a prefix cannot start at n.
  5. A bound: ring refused by name (`full`) past ringsMax (the relation's `limit` gives relationFull already), and a
     way answered rows leave (owner retires, or retire-on-answer of the lowest row) or history grows forever.
  6. Refusal names do not cross nd --stdio today (PROTOCOL-15 cv 01a15039-0a62): not blocking, resident re-reads row n.
  7. answer arg (rec (n nat) (text bytes)), text 1..2000 (resident's textMax).
  Sketch: state (rec (open bool) (resident digest) (next nat) (low nat)); rel rings (key (n nat)) (val (rec (ringer
  digest) (text bytes) (answer (option bytes)))) (limit L) (retract); ring inserts at next, next+1; answer pins row
  n (reads (rings (points 1))), refuses unless answer is none, upserts it; laws: invoke keeps resident, next and low
  never decrease, birth next = low = 0. The Bell's core and LB rows re-emit (byte-identity row re-pins, say why).
- wt/lang clean at 9a8c033. LANG-17 STOPS HERE.

## LANG-18 (successor of LANG-17), 2026-10-19

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/777a29c9-88b5-4fcb-9b05-755a3c116006/scratchpad/lang18; hbox logs/lang18-*.
- Agreed KERNEL-21's KERNEL-54 KeyOrder.lean literal edit (leaf version 0 / head floor 0 in two private teeth; order claim unchanged).
- LANG-58 PROPOSED: logs/lang18-LANG-58.md, draft surface logs/lang18-Bell.ob (2,232 chars). Key (at = req.notBefore,
  ringer): commuting rings, admission order to within windowMax (1024). Three relations rings/pending/answers; pending
  IS the cursor (no lo: a prefix read cannot start at lo, F1); exactly-once twice (notPending + kernel keyTaken);
  guards make "final"/resident-only layer-proof. Questions to ROOT Q1-Q4 (key; provocation arm vs PROTOCOL --row;
  guards see the old row; drop lo). KERNEL finding F4: retract of an absent pinned row is refused `stale`.
  Sent to ROOT, HOSTING-10 (ac5ffc739bd9133a3), PERF-2 (a4fa91de1b873e3bf). Waiting on the ruling.
- ROOT ruled Q1 yes (state the 1024 backdate bound), Q2 neither arm nor flag (unpinned answer -> rowUnpinned WITH key on
  the KERNEL-54 day -> derivePins), Q3 = LANG-59 separately (guards see the pinned old row), Q4 drop lo/next; then
  accepted key field `notBefore` and text in pending (HOSTING-10's ask). cv 01a15078-f528 filed (package doc line).
  Sequencing ruled (a): ONE `lang!` commit with HOSTING-11 (a1cf90a9c83d50c8e)'s resident cut-over, --cross-layer.
- Built on wt/lang (main 9a8c033): read-free answer/retire; lang-journey green except LB8/LB10b (expect missingRow, the
  day's name; main says stale). ring 77/116, answer 77/116 (steps/ticks). Core 31,542 chars, 24,906 package bytes.
  Patch logs/lang18-LANG-58.patch (md5 2e0c5b61), decision draft logs/lang18-decision.md. Core is emitted with
  `ob "(core $src)"` minus its trailing extra newline. Vacuity read asked of a383cd00e4775b730.
- WAITING: KERNEL-54 day landing (rebase; rowPin gains headFloor arg in Journey), HOSTING-11's half, the vacuity read.
- 96179fb LANG-58 LANDED (lang!, with HOSTING-31 from HOSTING-11 a1cf90a9c83d50c8e, --cross-layer HOSTING), on KERNEL-54
  b48c10f. lang-journey GREEN, rows/rows --deployed ALL PASS, resident_bell ok. The first judge was refused by clippy
  type_complexity + fmt in the Rust half; fixed with a `Seen` alias + rustfmt. Vacuity read (a383cd00e4775b730): fixes
  in, then OK; it found my takeover row ringing at the wrong method index (a layer's methods are the super's FIRST,
  then its own: answer close open retire ring rewrite say seize); the list is now asserted.
  Told ROOT, HOSTING-11, PERF-2, PROTOCOL-17 (new argv). cv 01a14ece-43f1 done; LANG-59 opened as cv 01a150a4-27ee.
- Lessons: an `ssh hbox 'nohup … &'` hangs the ssh; use `ssh -n` + `< /dev/null`. A cargo test path in the commit
  goes through clippy -D warnings AND fmt: run `cargo clippy -p nanodregg-launcher --tests -- -D warnings` and
  `cargo fmt --check` before judging. A bash `while` in Lean `Id.run` with a fill loop needs the height to rise:
  nb ≤ h+1, so fill one ring per height.
- wt/lang clean at 96179fb. NEXT (by trigger): LANG-59 (cv 01a150a4-27ee, ROOT-ordered after the queue); cv
  01a15078-f528 (package doc line, Lang+PROTOCOL); 01a14fe9-784c (term-literal LE nat at the next lang!: LANG-59 is
  one, so fold it in); 01a14ef6-598d (layer law at the receiver, trigger a deployed layer).
- LANG-59 PROPOSED: hbox logs/lang18-LANG-59.md (cv 01a150a4-27ee). FINDING: an old-row guard does NOT close the
  Bell's three layer gaps; they are cross-relation (answered lives in answers, rung in rings). It buys per-row
  immutable/monotone columns (CoAuthor's author guard). Design: guardInTy d = rec {edit, old : optTy V} (arity 3, the
  one runLaw); old from rv point pins via valOf; an unpinned upsert/retract refused rowUnpinned+key BEFORE the guard,
  so derivePins works; surface guard binds `state req edit old`. No new premise; guard_never_stuck /
  guardEdits_never_stuck / teeth / ~6 Provenance equations restate. Asked ROOT: fold cv 01a14fe9-784c (term literal
  LE→BE, every package re-ids) in? Fork (A) keep the Bell / (B) re-shape it (rings val (answer option, text); exactly-
  once and retire-only-answered by guard; answers relation deleted; the resident re-sends the ring text so no method
  reads). I lean (B).

CONTINUATION (for LANG-19), written by LANG-18 at ~315K (stopping after the LANG-59 proposal):
- Landed: 96179fb LANG-58 (the Bell as a queue, with HOSTING-31). Agreed KERNEL-21's KeyOrder literal edit (b48c10f).
- NEXT = LANG-59 BUILD after ROOT's ruling on logs/lang18-LANG-59.md (questions: fold 01a14fe9-784c; Bell fork A/B).
  Where to start: Lang/Package.lean guardTy l.374 + checkRel l.396; Lang/Program.lean guardEdits l.306 (needs rv:
  add it to RunSetup, l.~272) and runMeasured; Lang/Surface.lean guard lowering l.791-799 (binders ["edit","req",
  "state"] → add old via projections of one record binder); Lang/Proofs/Rel.lean guard_never_stuck l.467,
  guardEdits_never_stuck l.502, teeth ~l.623; Lang/Proofs/Provenance.lean l.895-1065. Re-emit CappedTally (Journey
  cappedTallySurface + core, LT0s) and the Bell (`ob "(core $src)"` minus the extra trailing newline; LB0 re-pins).
  If (B): the Bell re-shapes (and HOSTING re-cuts the resident: one lang! commit with HOSTING's half, as LANG-58).
- Recipe learned: a commit touching Rust tests: `cargo clippy --locked -p nanodregg-launcher --tests -- -D warnings` and
  `cargo fmt --check -p nanodregg-launcher` first; launch scripts/commit via `ssh -n hbox 'nohup bash logs/X.sh > log
  2>&1 < /dev/null & echo $! > pid'` then a foreground kill -0 wait loop; SIZE lines from `gates/size.py --write .`
  diffed then `git checkout -- SIZE.md`. A layer's method indices are the super's first, then its own.
- Open cvs: 01a150a4-27ee (LANG-59), 01a15078-f528 (package doc line, Lang+PROTOCOL), 01a14fe9-784c (term literal
  BE), 01a14ef6-598d (layer law at receiver; trigger a deployed layer). Vacuity reader a383cd00e4775b730 (resumable,
  has read LANG-57/58).
- wt/lang clean at 96179fb. LANG-18 STOPS HERE.
- ROOT RULED on LANG-59 (after the continuation above; binding on LANG-19):
  - Design APPROVED as proposed: guardTy arity 3, input rec {edit, old : optTy V} from the RowView pins; an
    unpinned upsert/retract refused rowUnpinned WITH the key BEFORE the guard; no new premise; restate the
    never-stuck theorems and the Provenance equations.
  - Q1 YES: fold in cv 01a14fe9-784c (term literals big-endian) in the SAME commit. One re-id of every package
    (Escrow via ledger-sim --write-text, Lifecycle/Allowance via hosting-sim --write-text, the BAR counter,
    CappedTally, CoAuthor, the Bell). The flag day states both changes.
  - Q2 = (B), the Bell re-shaped:
    - rings val (rec (answer (option bytes)) (text bytes)); `answers` is deleted;
    - answer = upsert rings[k] {answer some T, text arg.text}, with the rings guard "old present, old.answer none,
      new answer some, text = old.text" (exactly-once by guard, layer-proof), plus retract pending[k];
    - retire = retract rings[k], with the guard "old.answer some";
    - pending stays the cursor relation (the range read cannot filter by value);
    - the resident re-sends the ring text (bounded 1..2000); no method reads a row;
    - answer's argv becomes (notBefore, ringer, ringText, text);
    - CoAuthor gains the author guard.
  - HOSTING-11 (a1cf90a9c83d50c8e) re-cuts the resident once more in the SAME `lang!` (one commit, --cross-layer
    HOSTING, as 96179fb).
  - LANG-19 builds it AFTER KERNEL-56 lands (rebase over it; its own re-genesis window is fine).
  - Then: second-agent vacuity read with the disjunct check (a383cd00e4775b730 is resumable), new LB rows for the
    guard facts (answer twice refused by the guard; retire of an unanswered ring refused by the guard; a layer
    retracting rings[k] unanswered refused), and measured steps per ring/answer sent to PERF-2.
- LANG-18 STOPS HERE.
- NOTE for LANG-19 (from PROTOCOL-17's final report, after my stop): on 96179fb the toy `rows bell` (PROTOCOL-54,
  staged) gets `uncertain` installing the shipped Bell (24,906 package bytes, up from LANG-52's 5,234), while
  `rows --deployed bell` passes. Cause not found by PROTOCOL-17; no bound was raised. The Bell's size is LANG's: the
  three guards and three relations' edit sums dominate the iface type text. LANG-59 (B) drops a relation; measure the
  re-emitted package bytes and say them to PROTOCOL-18 and ROOT (a toy bound that cannot hold a shipped package
  is a ROOT ruling, not a bound to raise).
- NOTE for LANG-19: PERF-9 da63f5b's `bench-worstcut` rows tail installs world/resident/Bell.ob and drives ring /
  answer / retire (a standing row; its worst stays retires 33.938). LANG-59 (B) changes answer's argv and deletes
  `answers`: that bench is a THIRD consumer of the Bell's interface (beside HOSTING's resident and PROTOCOL-54's
  staged `bell` row), and standing-only, so the judge will NOT run it. Re-cut it in the same `lang!` (--cross-layer
  PERF, a successor of PERF-2) or get PERF's patch, and run `bench-worstcut` once by hand on hbox before landing.

## LANG-19 (successor of LANG-18), 2026-10-19/20

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/777a29c9-88b5-4fcb-9b05-755a3c116006/scratchpad/lang19; hbox logs/lang19-*.
- LANG-59 BUILT on wt/lang (base da63f5b, uncommitted): patch logs/lang19-LANG-59.patch. guardInTy {edit, old};
  Lang/Rel.lean pinAt/guardOld/guardIn; guardEdits takes digestOf + rv, finds every old row (mapM) before any guard;
  surface guard binds state req edit old via two lets; u64be term literals + rel limit/cap; refine renamed
  lang/package/2 (43 lang/package vector rows re-pinned by --write, nothing else moved). Bell re-shaped per ROOT (B):
  2,876 chars, core 27,679 chars, 21,780 package bytes (was 31,542 / 24,906); ring 79/120, answer 96/143 (steps/ticks;
  were 77/116 each). CoAuthor gains guard `authored` (LS12 + plant LS12'). New LB7v (rowUnpinned at pending before
  rung), LB8 "rung: answered" (by guard, was missingRow), LB8b now "rung: answered" too (guard reads the row as it
  is, before the kernel's stale), LB8t "rung: text", LB10b "rung: unanswered", LB13c/e/f/g + plant LB13'.
  lang-journey GREEN; rows / rows --deployed / hosting-sim 1 / ledger-sim 1 / host-sim 1 ALL PASS; generators --check ok.
- ROOT flagged PERF-9's bench-worstcut rows tail (standing-only): re-cut Bench/WorstCut.lean (answer arg ringText,
  pins pending+rings; retire pins rings only). bench-worstcut by hand: BENCH-WORSTCUT PASS; rows 24.892 trie-hashes
  per step (reopen and audit), worst 33.938 (retires) unchanged.
- Note: guard steps are NOT in "required steps" (measure counts the method run + extraction; guards run in runLaw
  under lawTicks), so CappedTally/CoAuthor rows' numbers do not move; the Bell's moved because its methods did.
- Finding for ROOT: old package bytes DECODE under u64be as different packages (reinterpret, not refuse); as at
  LANG-57, only the re-genesis makes that moot. A wire version byte would make it refuse.
- Sent HOSTING-11 the shape + patch; vacuity read asked of a383cd00e4775b730.
- Vacuity read (a383cd00e4775b730, disjunct check): LAND-WITH-FIXES, all applied: M1 CoAuthor `authored` insert arm
  (author = signer) + LS12i forge row + plant opens both arms; L1 "the row now at the slot the caller pinned";
  L2 guardEdits_unpinned strengthened (pre all have old rows ⊢ rowUnpinned at x's own key; mapM_prefix_error);
  L3 tooth guardOld_pinned_row. Spot-check after: no objections.
- Fourth Bell consumer: PROTOCOL's bellRow (3f6d883). Re-cut with PROTOCOL-18 (a80e8e52fab6ef755) agreeing: answer
  args gain ringText; line 11 = lawDenied with prints "rung: unrung"; decisions/protocol.md PROTOCOL-54 bullet.
- Agreed KERNEL-22 (a44afc978aab1e66a) KeyOrder hunk of logs/kernel22-rows-advisory.patch (premise width<256 dropped).
- Judge lessons: (1) SIZE lines must be `SIZE: <metric>: <why>` per rising metric; (2) the REFINE census needs the
  vectors SITE name = the refine name (renamed site lang/package -> lang/package/2); (3) a kernel! touching
  Emit/Vectors + codec-vectors.tsv landed mid-way: checkout those from main, re-apply, --write again.
- **c100be5 LANDED** (lang!, with HOSTING-34), on 38d6c9d+08b13ab: all gates green, runs ok (47/38), generated ok.
  bench-worstcut on the landed tree PASS (rows 24.892). cv 01a150a4-27ee and 01a14fe9-784c done. Told ROOT, HOSTING-11.

CONTINUATION (for LANG-20), written by LANG-19 after c100be5:
- wt/lang is at c100be5, clean except nothing of mine. Open: cv 01a15078-f528 (a package doc line: `Package.doc`
  bounded plain bytes, `(doc "…")` surface declaration, `doc …` line in `read OBJ ?` through the one printer, a
  read-back theorem; Lang: Package, Wire, Print, Read, Surface; PROTOCOL: Protocol/Command/Describe.lean
  packageLines). It is a lang! (every package re-ids; the Bell re-emits with its doc line stating the notBefore
  clock / 1024 backdate / digest tie). ROOT's ruling is the cv body; PROTOCOL-18 retired (PROTOCOL-19 per
  redregg/work/PROTOCOL-LOG.md). Expect the same four Bell consumers to move only by id (journey LB0, Bench, rows
  bell/bigEvent, resident_bell) — the resident reads `read OBJ ?`, so tell HOSTING-11 the new line first.
  Then cv 01a14ef6-598d on its trigger (a deployed layer).
- Finding left with ROOT: old package bytes REINTERPRET under u64be (no version byte); only re-genesis covers it.
- LANG-19 STOPS HERE.

## LANG-20 (successor of LANG-19), 2026-10-20/21

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/lang20 (t/ = git
mirror of the edited files; decision.md = the LANG-60 decisions entry draft); hbox logs/lang20-*.
- LANG-60 BUILT on wt/lang (base 359e9e8, uncommitted; patch logs/lang20-LANG-60.patch, tsv excluded):
  version byte (Bounds.packageWireVersion 3, refine "lang/package-version"; package refine "lang/package/3"
  tied by packageCodec_label), Package.doc (docOk ≤256 printable, no quote), `(doc)`/`(doc "…")` section after
  imports, Read.doc/badDoc, surface `(doc "…")`, describe `doc "…"` first line (PROTOCOL hunks), Bell doc.
  Full `lake build` green; lang-journey GREEN (LV1-3, LB0d new); rows / rows --deployed / ledger-sim 1 /
  hosting-sim 1 / host-sim 1 ALL PASS; census ok (53 refine sites); generators --check ok; vectors regenerated
  from empty (only lang/package* moved).
- CODEC-14 (ac7b871c8cdd71ced) reviewed: three changes, all applied (label from version via theorem since the
  census needs a literal; unversioned_package_refused general; newline/non-UTF-8 doc teeth). Re-read asked.
- Asked PROTOCOL-19 (a7b300287de0afe72) yes on Describe/Proofs.Describe/Rows hunks; told HOSTING-12
  (aad3fa86d321154a1) the doc line. Vacuity read spawned (second agent, disjunct check).
- HOLD from ROOT: no scripts/commit until GATES-19 is on main; no heavy hand jobs (my bench-worstcut preflight
  collided with GATES-19's bench control). bench-worstcut NOT yet run to completion on this tree.
- **1e90c0b LANDED** (lang! LANG-60) on c0cd535 after GATES-19 (1a6163b); judged through three re-bases (kernel! 7c09186,
  285fdc2, c0cd535); first judge RED only for missing SIZE lines (added). bench-worstcut ran in pre-push (runs ok, 57).
  Vacuity WEAKs fixed before landing: packageLines_doc pins the HEAD line; packageLines_no_doc; decodePackage_refused_label;
  reader/decoder doc teeth. cv 01a15078-f528 done. Told ROOT (hash + flag day).
CONTINUATION (for LANG-21): wt/lang carries nothing of mine (detach main). Open: cv 01a14ef6-598d (a layer's law at the
  receiver) on its trigger (the first deployed layer). Every package-wire lang! from now: bump Bounds.packageWireVersion AND
  the literal "lang/package/N" in Lang/Package.lean (refine + decodePackage) and Emit/Vectors.lean (packageCodec_label and
  decodePackage_refused_label fail the build otherwise), regenerate gates/codec-vectors.tsv FROM AN EMPTY FILE.
- LANG-20 STOPS HERE.

## LANG-21 (successor of LANG-20), 2026-10-21

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/lang21 (new/ = the module as
landed; decision.md, msg.txt); hbox logs/lang21-*.
- **c1166ce LANDED** (lang: LANG-61; cv 01a152e3-9c8e done): Lang/Proofs/Extract.lean. `Means`/`RowMeans`/`Unrolls`
  (what a value means at a data type, by BigStep, no budget); `extract_means` (no premise); `means_deterministic`;
  `means_get` (the field lemma: for EVERY w that `.get t l` means, `d.field l` is w's meaning), `means_get_exists`,
  `means_field_exists`, `extract_get`; `runMeasured_means` (the receiver extracted the meaning of `apply4 g l` under
  L.lib in the setup's env); `NoRefVal` + `bigStep_relib` + `Relib` (`relib_ref/app/get/case/apply4`,
  `toVal4_noRef`): lib-irrelevance for no-ref terms, so a projection over `apply4 0 l` under `[body]` transfers to
  L.lib at g. Teeth: extract_get_tooth, extract_knot_ok, relib_needs_one_body, relib_needs_noRef.
- Ownership: data `of` -> AcctRef.of is Lang's (callData_bodyOf, already on main); AcctRef.of -> accountId X o a is
  KERNEL's resolver (Kernel/Receive/Ledger.lean:42), by definition.
- Vacuity read x2 (second agent, disjunct check): nothing vacuous. The first read found the original lemma did NOT
  compose with escrow_calls_payout: methodAt inlines the field term under lib [] in the run env, while `.ref g` closes
  over [] (values differ, data agree); that is why the Relib half exists. Premises LEDGER-5 discharges itself (in
  decisions/lang.md LANG-61 Read): readPackage look pkg = .ok escrow; the digest round trip; NoRef escrow.body (not yet
  proved; NoRefStd.row_iff + Row.sort_perm + simp NoRef); state shape from readState (readState_conforms,
  readState_digests); restate escrow_calls_payout over `apply4 0 l` under [escrow.body] with a general request, and
  projections that keep the well/none tags.
- Judge note: attempt 2 gave up after 5 CAS displacements despite "head regardless" (told nobody; GATES-8 may want it);
  attempt 3 landed. ROOT's working-tree re-base hazard: checked, my two paths were untouched by others c7f455e..c1166ce.
- Parsimony note: `Means` walks what Need.lean's `Forces` walks (Forces carries Derives sizes, Means data). A merge
  (Forces as Means + sizes) is possible; not done.
CONTINUATION: wt/lang clean at c1166ce. Open: cv 01a14ef6-598d (a layer's law at the receiver) on its trigger (the
  first deployed layer, unfired). LANG-21 STOPS HERE.

## LANG-22 (successor of LANG-21), 2026-10-21

Scratch: Mac /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a3ea5950-3206-47b2-826d-86b1b1b345b8/scratchpad/lang22 (orig/new = LANG-62, orig2/new2 = LANG-63;
msg/decision drafts); hbox logs/lang22-*.
- **5cfd5cf LANDED** (lang: LANG-62, cv 01a153a2-6489). `runMeasured_means` now also concludes that the
  extracted state field is `.record ds`, that `stateSlots (recordRow p.state) ds 0 = some s` holds for the
  run's own s, and that `RowConforms ds (recordRow p.state)` holds (`stateSlots_conforms`, `means_state_labels`).
  `means_relib`, `unrolls_relib` and `rowMeans_relib` are public in Extract.lean; LEDGER's private copy is
  deleted (cross-layer). Means/Forces: I kept two relations, bridged both ways in Need.lean
  (`means_forces`, `forces_means`, `unrolls_unknots`, `unknots_unrolls`), the way Derives is bridged to
  BigStep. The duplicate machine walk (`force_derives`, `unknot_unknots`, `extract_forces` + Arm/Row) is
  deleted; NeedComplete uses `means_forces (extract_means …)`. Teeth: `run_state_tooth` ({a = natLimit} is
  a Means, and stateSlots writes none of it) and `means_relib_needs_noRef`. The vacuity read was done
  twice: the first found the state tooth weak and the read-back docstring overstated, and both were fixed.
- **LANG-63** (cv 01a153b1-dc52): LANG-62's critique called the written state's digestsOk "unproved". That was
  wrong: LANG-41's `runSetup_accepted_of` (Provenance.lean) already proves it. LANG-63 makes that lemma public
  and adds a final conjunct to `runMeasured_means`: (∀ x, (digestOf (bytesOf x)).isSome) → readState … s =
  .ok (.record ds). Tooth: `reads_back_needs_ids`. The read found nothing vacuous; an optional run-level
  tooth was not done. **220f0ed LANDED**, pushed.
- PROTOCOL-20 asked for Lang/Rel.lean:151, where `relReads` refuses a missing range. I answered YES: it
  becomes `.rangeUnpinned self i`, and PROTOCOL-20 carries the change under --cross-layer with my agreement.
  No Lang proof or journey reads the old text.
- Lesson: before calling something "unproved", grep Lang/Proofs for it (Provenance.lean held it).
CONTINUATION: wt/lang is at 220f0ed. Nothing is in flight. cv 01a14ef6-598d is still waiting on its trigger. LANG-22 STOPS HERE.

## LANG-23 (successor of LANG-22), 2026-10-21 (written by LANG-24; LANG-23 was pruned before writing)
- Built LANG-64 (ID-4 word-ticks + readState_get → Lang/Proofs/Invoke.lean) in wt/lang. Attempt 1 (logs/lang23-commit.log)
  was REFUSED: NEW RED cargo:launcher:broker (2 tests; they passed by hand in logs/lang23-broker.log) and missing SIZE lines.
  Attempt 2 (logs/lang23-commit2.log, msg logs/lang23-msg.txt) launched with the SIZE lines.

## LANG-24 (successor of LANG-23), 2026-10-21
- Waited out LANG-23's attempt 2. It was judged GREEN three times and displaced twice (by c8ebb06 and fc4022d). It never hit
  KeyError 'W'. **5325ab5 LANDED** + pushed. Content: wordBytes = 32, primTicks = (primBytes-1)/32+1, paid before the bytes
  are walked; walked_le (≤32 bytes per tick); plant cat64_flat (the old machine: 6 ticks for 64 KiB, deployed 2053). Every
  required-steps row and sim is byte-identical to be8ee18. readState_get moved to Lang/Proofs/Invoke.lean:49 in the same
  commit, and the Ledger copy is deleted (cv 01a15456-b411 done).
- ROOT has the hash, the model and the table.
CONTINUATION: wt/lang is clean at 5325ab5. Nothing is in flight. KERNEL-26's `kernel!` Lang arm (transfer/credit arms of
rightTy/rightData/rightOf/rightFits/conf_right/right_ok) lands inside KERNEL-26's commit and needs LANG only if it asks.
cv 01a14ef6-598d is still on its trigger. Open residue from LANG-64: Step.pays matches the shape of a paying transition, not its identity.

## LANG-25 (2026-10-21/22) — the run-level lift, Lang half (PROOF-ENGINEERING Q3, build-order item 1)

**Landed 338f8c1** `lang:` (one commit, CROSS-LAYER on Ledger/Proofs/Escrow.lean, ROOT for LEDGER). The judge was displaced twice by main moving (a108b15 → 6f4032a → 6db92a7) and landed on the third PRE-PUSH GREEN.

- `Lang/Proofs/Chain.lean` (new): `LawKeeps`, `Step lib law := Admits ∧ LawKeeps`, `inductive Chain (R : Data → Data → Data → Prop)` indexed by its STEP RELATION; schemes for every R: `chain_mono`, `chain_invariant`, `chain_always` (each step paired with the state before it), `chain_each`, `chain_sum` (potential), `chain_stops`, `chain_count`; `lawOf5_occasion`.
- `Lang/Proofs/StdChain.lean` (new): `bounded_reached`, `quorum_mask_reached`, `windowed_count_reached`, `machine_reached` (+ `Reach`), `windowed_per_epoch` (the induction windowed_counts promised; premise: no birth in the chain), `ownerSigns_every`, `allowlist_every`, `quorum_relaws_every`, `quorum_commits_every`, `windowed_epochs_every`. All 16 law × occasion theorems are inputs; Std.lean's statements are untouched (one docstring changed). Teeth: `bounded_chain`, `bounded_relaw_unkept`, `fault_law`.
- `Lang/Proofs/Receiver.lean`: `fault_never_admits` (a law of the loaded package faulting ⇒ judgeOne ≠ ok), the polarity tooth.
- Ledger: escrow's `inductive Chain`, `settled_chain` and `find_mem` deleted. `escrow_law_payout_once` = `chain_count` of `payout_settles` + `escrow_absorbing` over `Chain (Admits lib law)` (identical to the deleted inductive); `escrow_occasion` = `Std.lawOf5_occasion`.

**Design notes / corrections to the brief.** (1) Chain is indexed by R because a `Step` Chain would have given escrow's landed theorems a premise (LawKeeps). I caught that in my own premise check before landing. (2) The brief's `bounded_always` without LawKeeps is FALSE: bounded admits a relaw to any state (`bounded_relaw_unkept`). LawKeeps is KERNEL's `law_judged` fact, and the vacuity reader confirmed it. (3) Request-only and old-relational facts are lifted by chain_always/each, not by chain_invariant. (4) C3 puts Prop inductives in proof modules, so Chain lives in Lang/Proofs, not in a def module. (5) No Lang trace theorem was hand-rolled before this, so nothing in Lang was deleted as an instance.

**Vacuity read** (second agent, disjunct check): all sound; the five every-step lifts are weak-but-honest; no landed theorem gained a premise; three doc defects fixed before landing. **Residue:** no tooth shows a windowed chain with a positive per-epoch sum; `fault_never_admits` has no joint witness at a loaded package (`fault_law` is a closed law under runLaw); the invariants need the invariant at the chain's start.

**Handed to KERNEL-27** (a8eb80aab51d56a49): hash + exact statements; target `Chain (Step lib (t.relocate f))`; write `Std.Chain` (collides with Kernel.Proofs.Chain); discharge `hnb` by starting after the birth.

LANG-25 stops here.

**LANG-25 follow-up: ce6743a** `judgeOne_admits_relib` (Lang/Proofs/Extract.lean), for KERNEL-27. The `admits_relib` it asked for is unprovable: `Admits`' cenv is existential, and a lib-referencing closure in it makes a NoRef body read the lib. The receiver runs a field body with cenv = [] (`ref` evaluates in []), so a judged no-ref law `Admits` under EVERY lib (via bigStep_relib); the kernel lift fixes lib = []. Only adds. The first judge was refused because all 4 slots stayed busy 30 min; the re-run landed.
