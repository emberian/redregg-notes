VERDICT: RELEASE PROT-6-BUILT

Seventeen conditions, each kept in the candidate. Base of the diff: `1fc905f`. Judged: `promo/PROT6/built.diff` whole (21 files, the deletions, `StdOffer`, the four proof files, the journey, the one Ledger statement), the ready line in `codex/CX-PROMO.report.md` (the last `READY-IMPACT PROT-6-BUILT`), `promo/PROT6/decls-lines.txt`, `promo/PROT6/int-journey.txt` against `promo/PROT2/journey.txt`, and the two decision drafts the ready line names. `IMPACT-PROT-6.md` still ends at the design (Q6); there is no BUILT section in it. No build. No tree edit.

The one thing the numbered conditions do not contain, and the second read's paragraph did: the run-grain *converse* of `take_iff_compliant`. It is not proved. It is said in the theorem file and in the LANG-75.11 draft. It is not a `sorry`, and it is not a landed statement made weaker. Section (3).

---

## (1) The seventeen

**1. The peer read is declared, never ambient. An unpinned peer cell is `unpinned`. An unpinned peer row is `peerRowUnpinned`.** Kept.

[READ `built.diff` `Lang/Program.lean`] `runSetupWith` is still the only call that builds the rows argument, and it calls `methodReads` with `p.peerReads ℓ`. `Package.peerReads` reads `methodPeer` off the method type. `methodReads` with `ps = []` returns the own `readsData` and does not call `peerOf` (`methodReads_no_peer`). A peer record appears iff the type asked. [READ `PeerRead.lean` `peerReads_unpinned`] `look q = .error e` is returned as that same `e`, and `readKind` is the first read of the peer cell, so the kernel's name is the one that comes out. [READ `int-journey.txt:803`] LF3 is `refused unpinned`. [READ `StdOffer.lean` `offerTakeBody`] the peer point's `none` arm is `fail "peerRowUnpinned"`, after the own offer was `some`. [READ `StdOffer.lean` proofs `take_peerRowUnpinned`] the method term refuses that string. [READ `int-journey.txt:804`] LF3r is `refused program "take: refused peerRowUnpinned"`. The two names are not swapped.

**2. `Std.offer`, and the matcher's `fuse` forwarding one `deal` to `x.take` and `y.take`, one call tree, one Turn.** Kept.

[READ `StdOffer.lean` `offerFuseBody`] both `offerTakeCall`s take `(a "deal")`. `offerPackage` checks the package; the methods are `fuse`, `post`, `take`, `withdraw`; `session` is `activityLog` with `activityWaiting`; there is no resume and no retire. [READ `StdOffer.lean` proofs `fuse_calls`] a returned `Lang.program` run of `fuse` has `calls = [.invoke x' take deal budget vx', .invoke y' take deal budget vy']` and `rows = []`. Same bytes, same method, both `take`. The tree and the one seal are the kernel's, untouched: no `Kernel/` file is in the diff. `fuse_atomic` is the theorem that both retracts are in that one `receive`.

**3. `take_iff_compliant` per side is the honesty. `fuse_iff_compliant` is not restated.** Kept.

[READ `StdOffer.lean` proofs, `take_iff_compliant`] the statement is `BigStep` of the generated `take` body, both offer points present, iff `JointOk`. The matcher's code is not a premise. The docstring's mutation is P2, F2's pair, the mutant returns where `JointOk` is false. [READ the same file's header] there is no theorem named `fuse_iff_compliant` anywhere in the diff. `fuse_calls` is the calls half, and it does not mention `JointOk`. The run-grain direction that a returned take did judge is `take_run_sound` (success implies `JointOk`, calls empty, own retract plus own session insert). The converse at `Program.run` is the gap in (3), not a restated false iff.

**4. `fuse_atomic` is the fuse call only. Membership is the touch's slot and its act. The mutation is P3.** Kept.

[READ `StdOfferFuse.lean` `fuse_atomic`] premises include `c.unsigned.body = .invoke z offerFuseIx` and `z`, `x'`, `y'` live cells of the generated package. Conclusion: `∃ kx ky, (∃ τ ∈ t.rows, τ.slot = .row ⟨x', 0, kx⟩ ∧ τ.act = .retract) ∧` the same for `y'`. Not `t.rows.map (·.act)`. The docstring names P3 (the second invoke dropped: `receive` can still be `.ok`, `y'`'s retract absent) and says a refusing take is "no Turn", not a conjunct. [READ `plants/P3.new`] the second call is `noCallT`. The same-bytes sentence is not in this conclusion.

**5. `offerJoint_meaning`, and the peer-box witness is a θ inside one box and outside the other, not F2.** Kept.

[READ `offerJoint_meaning`] three arms: equal roles and `refused "sameRole"`, or `JointOk` and `ok`, or unequal roles and not `JointOk` and `refused "notCompliant"`. `JointOk` is both `InBox`s. [READ its docstring] the mutation that drops the peer `offerInBox` is false at own box `[5,10]`, peer box `[8,12]`, θ = 6: inside the own box, outside the peer's. Not F2. [READ `int-journey.txt:801`] LF2 is θ = 9 against seller `[11,12]`, where the buyer's `[5,10]` already fails, and the refusal is `notCompliant` with both rows standing. F2 stays the both-boxes row. `fuse_refused_disjoint` is that pair at every conforming θ, plus a witness inside each box alone (7 and 11).

**6. `jointLaw_sound` keeps both runs evaluating `offerJoint`, and the plants that separate it are the asymmetric ones.** Kept.

[READ `jointLaw_sound`] under `fuse_atomic`'s premises plus each party's id round-trip: one `decodeData` of the one `deal` to one `pair` and one `th`; each side's `methodReads` of that record; `JointOk ox qx th` and `JointOk oy qy th`; each `peerOf` is the other party; `ox = qy`, `qx = oy`, keys too; both session inserts carry the same value bytes. The docstring's title is "Two evaluations of one generated term, coupled by one forwarded byte string". The formal conjunct is `JointOk` twice, not a `BigStep` of the name `offerJoint`. The evaluation is what the proof unfolds: `party` calls `take_run_sound`, and that proof cases on the generated body, which applies `offerJoint`, and contradicts the two refusal arms. P1 (`offerJoint` forced to `ok`) makes `JointOk` false on LF2's pair while a returned run would still be a premise. P4 (a second deal) breaks the one-decode and the equal-bytes conjuncts. P3 does not: dropping the second call makes `fuse_atomic`'s premise-to-both-retracts fail, and this theorem's one-θ conjunct is a different tooth. The one θ is attributed, in the docstring, to the matcher. Section (2) for what was observed.

**7. `invitation_once` is once per standing row. The grant is not spent.** Kept.

[READ `invitation_once`] a fuse `receive` admitted from canonical rows leaves both offer slots the takes read absent (`rowAt = none`). The docstring: `.invoke` is not a counted right; a later `post` at the same key is a new offer; not `spent_never_minted`. [READ `int-journey.txt:806`] LF5 is `noOffer` on the post-LF1 world, and both grants are still live. The "later take refuses" is `take_noOffer` at the term grain plus that row, not a conjunct of this theorem. P5 does not red the theorem; (2).

**8. F6's name follows `via`.** Kept.

[READ `Journey/Offer.lean` LF6a–c, and `int-journey.txt:807–809`] `viaY = none` is `refused noGrant`. `viaY` a live grant of `[invoke post]` only is `refused grantRight` naming that grant. The take grant not pinned is `refused unpinned` naming it. Three names, three rows. They are kernel controls, and the draft says so.

**9. The same-bytes guarantee is the matcher's, and it is not copied onto `fuse_atomic` or `jointLaw_sound` as "whatever the caller".** Kept.

[READ `fuse_calls` docstring] "The one θ is this theorem's." [READ `StdOffer.lean` header] a package other than this one, granted `take`, could hand the two takes different bytes; an owner may root-invoke `take` with no matcher; each take's honesty does not depend on who called it. [READ `fuse_atomic`] no byte-equality conjunct. [READ `jointLaw_sound` docstring] "The one θ is the MATCHER's guarantee (`fuse_calls`, `z` of the generated package): a caller of another package granted `take` could hand the two takes different bytes, and each take's own judgement (`take_iff_compliant`) does not depend on who called it." The one-decode conjunct sits under `hp : readPackage … = offerPackageOf`, which is "the matcher is `P`", not "any matcher".

**10. The owner can root-invoke `take`. One session row is not a fuse.** Kept.

[READ `fuse_atomic` docstring] "the owner can root-invoke `take` alone, and one session row is not a fuse." The theorem's body premise is `invoke z fuse`. A root `take` is outside it. [READ `StdOffer.lean` header] the same sentence, and `jointLaw_sound` is named as the two session rows. [READ `KERNEL-45-amend.draft.md`] "An owner may root-invoke its own `take` with no matcher at all, so one session row is not a fuse." `offer_safe_forever` is not stated, so the conjunct that would be false is not landed (14).

**11. `Conds`, `Conds.space`, `Assigns`, `firstFit`, `coverAll`, `priceConds`, the Negotiation `World`, and its 12 theorems are deleted.** Kept.

[READ `decls-lines.txt`] `Conds`, `Conds.space`, `Assigns`, `firstFit`, `coverAll`, `priceConds`, and the twelve: `unrelated_update_keeps_plan`, `unrelated_update_repair_reuses`, `provider_revoked_unavailable`, `revocation_repair`, `current_at`, `representation_change_transports`, `stale_opening_refused`, `competing_commitments`, `replay_refused`, `deadline_expires`, `AdmittedIn`, `separate_witnesses_over_substitutions`. Also the World's helpers (`World`, `view`, `viewAt`, `store`, `commit`, `revoke`, `w0`, `candidates`, `available`, `frags`, `Tok'`, `Tok.at`, `Tok'.current`, `BuyerGuard`) and the four scalar theorems `separate_witnesses_insufficient`, `witnesses_do_not_compose`, `greedy_vs_logical`, `search_state_ne_logical_status`. [READ the Negotiation diff] `internal_of_histories`, `exactly_once_needs_reply_and_dedupe`, the cancellation path, the lost-reply family, and `replan_before_dispatch` stay. [READ `Protocol.lean` proofs] `separate_witnesses_bounded` stays. It was not on the ruled list; it does not mention `Conds` or `firstFit`. The draft says so.

**12. `Sig` gains no field.** Kept.

[READ `Package.lean` in the diff, `methodSig`] the success arm is still `some ⟨A, ks, rs, es⟩`. Peer reads are `rowsOf`'s second component and are not stored. No hunk adds a field to `Sig`. `peerNotNamed` is a `CheckError`, not a signature field.

**13. The `HasProt` role index is neither earned nor reverted.** Kept. Section (5).

**14. `offer_safe_forever` is not landed. `row_turn_cases` is later.** Kept.

No such theorem is in the diff. [READ `LANG-75.11.draft.md`] " `offer_safe_forever` is NOT this landing. It needs a new `row_turn_cases` … and READ-PROT-6b condition 2 makes its second conjunct as written false."

**15. The KERNEL-45 line says two runs of one term, one forwarded byte string, one seal. It does not say a joint law. And LANG-23 (iii)'s trigger is rewritten.** Kept. Second read, conditions 7 and 8. The text is not a hunk of `built.diff`; it is the draft the ready line says this landing pastes.

[READ `KERNEL-45-amend.draft.md`] "two runs of one term". Each `take` decodes the one byte string and evaluates `offerJoint`. "Both retracts sit in one Draft, and that Draft is sealed once." "It is not a joint law, and it is not one judge. Nothing in the Turn observes both offer rows, or both session rows, together." Kernel lines changed: 0. K stays deferred, and its trigger now includes the owner-root `take`. The word "coupled" is not in the draft; the two sentences are the coupling. [READ `LANG-75.11.draft.md` title] "one judge term" is the generated term, and the body says "not a joint law and not one judge." [READ the same draft] "LANG-23 (iii) stays open. Its trigger is rewritten: the first method whose nested invoke argument is not a byte string it already holds. This fuse is not that method: it forwards bytes." The words "until ID-4" are not there.

**16. The escrow instance is deferred to PROT-8.** Kept.

[READ `StdOffer.lean` header] "this package has no method that answers it (settlement moves value: PROT-8)." The session plan's `precondition` is `false`. No escrow offer, no `Val`. [READ `EscrowWitness.lean`] the only edit is the private `setup_eq` hypothesis (`readsData` to `methodReads`) and the deletion of `hw0`, which is the grant R-0049 named. Not an escrow fuse.

**17. The same-bytes sentence, the owner's root take, and the fuse-call restriction are said where the theorems can be misread, not only in the draft.** Kept as the conjunction of 4, 9, and 10, which is what the second read's conditions 1 and 2 required to be *in the theorems*. Counted here so the seventeen are the two reads' conditions (first read 2–8, second read 1–9) with the declared-peer shape and the escrow deferral the release also named, and without counting the superseded fork L. Each of 1–9 of the second read is in 3, 4, 5, 8, 9, 10, 11, 15 above. Each of 2–8 of the first read is in 5, 2's refusal names, 11, 12, 7, 13, 14.

---

## (2) The plants

The lake logs the ready line cites are not in `promo/PROT6/plants/` on this machine. That directory holds the seven mutation snippets `P1.new`–`P7.new`. The account of what went red is the builder's, in the LANG-75.11 draft, and I did not re-run it. No landed theorem is named there. I cannot confirm the absence from a log I do not have.

What the snippets are, and what the draft says each red:

- **P1** [READ `P1.new`] not a literal `offerJoint := okT`. The `sameRole` test is `andT (.bool false) …`, and the box test is `anyOf [.bool true, andT (offerInBox …) (offerInBox …)]`, so the ok arm is forced. Draft: reds the judge's evaluation lemmas (`offerJoint_meaning`'s route) and LF2 / LF2r admit. Not observed on `jointLaw_sound`: under P1–P5, Lake leaves `StdOfferFuse` unbuilt below the red `Proofs.StdOffer`.
- **P2** [READ `P2.new`] `Term.ite (.bool true) okT (activityApply offerJoint …)`. Draft: reds `take_iff_compliant`'s route, and LF2 / LF2r admit. That is B7's tooth at the term grain. `offerJoint_meaning` is a different site, and the draft does not say P2 reds it.
- **P3** [READ `P3.new`] the second call is `noCallT`. Draft: reds `fuse_calls` and LF1 (Y's row left). `fuse_atomic` is reasoned, not observed red by name.
- **P4** [READ `P4.new`] `y` is called with `(a "dealY")`. Draft: reds `fuse_calls`, and every LF row, because the argument type changed and the journey deal no longer decodes. That is a coarse red of the harness, not seven distinct teeth. `jointLaw_sound`'s one-θ conjunct is reasoned, not observed.
- **P5** [READ `P5.new`] the offer edit is `upsert`, with a value. Draft: `offer_guard` refuses `final`, so LF1 refuses, and `invitation_once` does not go red (its premise, a successful fuse `receive`, never happens). The tooth is the journey row, not the theorem. Not a landed theorem. The mutation that would red only `invitation_once` (retract, then a second run that finds a different slot) was not the plant.
- **P6** [READ `P6.new`] the peer `readsData` is under `self`. Draft: reds `peerReads_parent`, and LF1 / LF2 by `sameRole`.
- **P7** [READ `P7.new`] the package check is `… || true`. Draft: reds `peerReads_package` and LF4.

The draft also says several of those reds sit in private helper lemmas of the target proof, with the journey row as the outcome evidence. A private lemma going red is the theorem's proof failing; it is not the theorem's name in the error. P3's and P4's teeth on `fuse_atomic` and `jointLaw_sound` were not read off a log. None of this is a landed theorem going red, on the account I was given. No correction to name.

---

## (3) The proofs

No `sorry`. No `admit`. No `native_decide`. I read every new proof and every proof hunk. `decide` is used on finite checks (`roles_wf`, slot labels, `callSlotsOf`). `decide +kernel` appears only where `EscrowWitness` already used it; the diff replaces `hw0` with `by rfl` at three call sites. No `open … in`. The new files `open` the kernel namespaces at the top. `PeerRead.lean` adds a `private instance : LawfulBEq ByteArray`, file-local, so `==` on the arrays is equality inside that file.

The weakening, declared, not hidden:

[READ `Proofs/StdOffer.lean` header, and `take_run_sound`'s docstring, and `LANG-75.11.draft.md` "Not proved"] `take_iff_compliant` is an iff at the method-term grain. At `Lang.program`'s `run`, only soundness is proved: a returned take decoded the argument, read the two pinned offers, found `JointOk`, made no calls, and its row acts are the own retract and the own session insert. The converse (compliant implies the run returns) is not proved. The file names the two missing lemmas: machine completeness at `Bounds.stackMax`, and `extract` completeness. No containment was built in their place. LF1 is the instance, not the theorem. This is the second read's paragraph ("`Program.run` of `take` … iff `jointOk`") met in one direction. The numbered condition ("the iff is `take_iff_compliant`, on each side", and not a restated `fuse_iff_compliant`) is the theorem that landed.

`jointLaw_sound`'s statement says `JointOk` of each side's reads, not `BigStep … offerJoint …`. A term that returned `ok` exactly on `JointOk` by a different computation would keep the statement and break the proof. P1, which returns `ok` off `JointOk`, falsifies the statement. That is the tooth the statement has.

No landed theorem's statement was edited except the ten `RESTATES-MEANING` in (4). Their proofs follow `hrows` onto `methodReads`. I did not see a hypothesis added to make one go through.

---

## (4) The price

[READ `decls-lines.txt`] Under `RESTATES-MEANING` / `DELETES`, nothing else.

Restated, the rows step or the rows type, one binder where there was one:

- `methodSig_spec`, `methodArg_spec`, `method_run_sound`, `method_live_run_sound`
- `runSetupWith_spec`, `runSetup_spec`
- `invoke_never_stuck`, `invoke_live_never_stuck` (each gains an implicit `{pkg : D}` on the rows step; not a `Prop` hypothesis)
- `runMeasured_means`
- the private `setup_eq` (`EscrowWitness`, the R-0049 grant)

Zero lines that are a new hypothesis. `readsData_conforms` and `readsData_digests` are not in the list; `readsData` is unchanged. The provenance proofs call `methodReads_digests`. That is a proof edit. The first read's six are inside this ten; the four extra are the statements whose type mentions `readsTy` or `methodArg` and now mention `rowsTy`.

Vanished, all declared: the thirty-eight Lang names in (11), plus `hw0`. I did not see a name leave the diff that is absent from that list. `separate_witnesses_bounded` did not leave.

[READ `int-journey.txt` against `PROT2/journey.txt`] The same offsets match at lines 1, 200, 400, 500, 700, and 780–798 (the P8 tail, then `lang-journey: GREEN` in the baseline). The built output continues 799–810 with LF0, LF1, LF2, LF2r, LF3, LF3r, LF4, LF5, LF6a, LF6b, LF6c, LF7, then GREEN. Twelve new rows, no shifted line before them. That is the journey diff: the new rows only. LF0–LF7 as specified, plus the three the conditions added (LF3r, and F6 split into the three `via` names).

No byte moves, as a statement about the diff, not a vector run I repeated. [READ `rowsTy`] `ps = []` returns `readsTy` unchanged. No codec tag, no `packageWireVersion`, no `Sig` field, no `Std.activity` layout change (`session` is `activityLog`). A new package is new bytes, not a moved vector. The ready line says the codec vectors were checked identical and the gate is `lang:`. I did not re-run that check. Nothing in the diff is a `lang!` cause. Not a Bell re-emit.

---

## (5) The roles

Still not earned. The index still has no reader, and this landing does not revert it.

[READ `offerJoint` / `offerJoint_meaning`] the two chooser roles are fields of two offer *values*. The test is `o.field "role" ≠ q.field "role"`. No new theorem mentions `HasProt`, `Iface`, or `Open.me`. No theorem has `HasProt sp r1` and `HasProt sp r2` for `r1 ≠ r2`, both different from `me`. A's offer and B's offer are distinguished by which object holds the row and by a label in the row. A third `Role` still changes no `HasProt` theorem. [READ `LANG-75.11.draft.md` "The roles claim"] "Not earned here, and not reverted here. … PROT-3's `proj` is still the index's named reader." That is the sentence the decision has to keep, and the draft has it.

---

What landed, against the two reads: fork M, the declared peer read, `Std.offer`, `take_iff_compliant` as the honesty at the term grain with `take_run_sound` as the run's one direction, `fuse_calls`, `fuse_atomic` on the fuse call, `jointLaw_sound` as two `JointOk`s of one forwarded deal, `invitation_once` as the row, the deletions, `lang:` plus the one Ledger statement. What did not land: T, K, L, a theorem named `fuse_iff_compliant`, a joint law, a `Sig` field, a `HasProt` bridge, a use-once grant, `offer_safe_forever`, the escrow.
