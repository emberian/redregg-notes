VERDICT: RULE PROT-6

The shape is accepted: fork L, a declared peer read, `Std.offer` reusing `activityLog`, no `Std.pending`, `invitation_once` per standing row, no `HasProt` bridge, the Negotiation `World` deleted, `lang:`. Do not build against IMPACT-PROT-6 as written, and do not record KERNEL-45 item 3 as a joint law. Eight conditions, then it is the spec:

1. **L is two evaluations of one term, not one judge.** The KERNEL-45 amendment says that. `jointLaw_sound` keeps the conjunct that both runs evaluated `offerJoint`. P2 (fuse drops the judge, take keeps it) reds `jointLaw_sound` on a compliant pair (F1), not only `fuse_iff_compliant`. The symmetric plant is in the table: take drops the judge, fuse keeps it; `take_iff_compliant` reds; F2 stays refused by fuse.
2. **The peer-box witness is not F2.** Dropping the peer `inBox` is still a refusal at θ = 11, because the caller's box `[5,10]` already fails. The witness is a θ inside the caller's box and outside the peer's. F2 stays the both-boxes row.
3. **An unpinned peer row is not `unpinned`.** Peer cell unpinned is `Refusal.unpinned` (F3). Peer cell pinned, offer row not pinned, is an empty point slot the generated method refuses `peerRowUnpinned`. That refusal has a row or a theorem. Do not rename it.
4. **`Conds.space` goes with `Conds`.** It is `Lang/Proofs/Contextual/ProtocolTyping.lean:123` and it will not elaborate once the structure is gone. `Assigns` (`:128`) has no consumer left; delete it in the same landing.
5. **`Sig` gains no field.** `sg.peer` in the prose is `peerSig`'s parse of the method type. `⟨unit, [], [], 0⟩` stays (`Hosting/Proofs/Allowance.lean:93`, `Hosting/Proofs/Package.lean:154`).
6. **`invitation_once` says what it is.** The grant is not spent. Once per standing row. `post` again at the same `n` is a new offer. Not `spent_never_minted`.
7. **Q5: the index is not earned, and this card does not revert it.** No bridge from the offer row to `Iface` / `HasProt`. The revert, if PROT-3's `proj` will not read the index, is its own landing.
8. **L2 is not `safeAt`, and it is not this landing.** `termsOk` on an open row is well-formedness. `row_turn_cases` is a new theorem; `dispatched_ok` concatenates cell effects, not rows.

Q6 is L. Q1–Q4 stand as the IMPACT's defaults. Base: `origin/main` = `1fc905f` (fetched this read; local `HEAD` is `7e02852`). No build. No tree edit.

---

## (1) The cross-object row read

Kernel price 0. Confirmed.

[READ `Kernel/Receive/Call.lean:282`] `RowView.points : D → Nat → List (ByteArray × Option RowLeaf)`, parent then relation. [READ `:427–431`] `rowView` keeps a pin when `k.parent = parent ∧ k.rel = rel`, for any parent. [READ `:550–557`] every pin becomes a `RowTouch` with `seen := some digest`, parent unrestricted; an effect on an unpinned slot is `rowUnpinned`, an insert or a declare needs no pin. [READ `Kernel/Proofs/Receive.lean:38–41`] `receive_congr` takes `rowView X.env w₁ c.unsigned = rowView X.env w₂ c.unsigned` and concludes the receives are equal. The cell hypothesis beside it (`agree`) is `World.live` of cell pins only. A peer row pin is inside the rows hypothesis, not a new one. [READ `Kernel/Proofs/Rows.lean:680`] `rows_stale_refused` is any `RowTouch` whose `seen` does not match, whatever the parent. Nothing in the kernel asks whether the parent is the running object.

[READ `Lang/Program.lean:404`] the only executable call of `readsData` is `readsData digestOf look p.rels rv r.self sg.reads`, inside `runSetupWith`. [READ `Lang/Rel.lean:177–179`] `relReads` takes the parent as an argument and reads `rv.points self i`. The parameter is named `self`; it is whichever parent the caller passes. A peer read is `readsData` at `parent := peer`. `readsData` and `relReads` themselves change by nothing. [MEASURED `git grep readsData origin/main`] the other hits are proof hypotheses (`Load`, `Invoke`, `LiveInvoke`, `Extract`, `Provenance`, `Ledger/Proofs/EscrowWitness`). The method term sees rows as `var 3` (`apply4`). It does not see `rv`. So the peer read is declared: it is in the rows argument iff the setup put it there iff the method type asked. Not ambient. Law 5 holds if `peerSig` is the only way a non-empty peer list appears, and `Std.offer` is not given a back door.

It is not refused `unpinned` by name when the peer's **row** is not pinned. [READ `Lang/Rel.lean:179–192`] an empty point list is empty slots, not an error. `rangeUnpinned` (`:192`) fires when a declared **range** has no signed range, and the parent it names is the parent `relReads` was given, so a peer range does take the kernel's name. A point read does not. `Refusal.rowUnpinned` (`Call.lean:201`) is an effect on a slot the caller did not pin (`guardOld` at `Rel.lean:274–276`, `rowTouchesOf`), not a read that missed. The generated `peerRowUnpinned` is the right name for the empty slot, and it is the E1 R1 asymmetry (a cell takes the kernel's name, a row slot takes the program's). F3 is the cell (`readKind` → `pinned` → `.unpinned peer`). Condition 3 is the row.

It does not give a pin a second meaning. The method is handed `(key, leaf)` from `rowAt`. The pin digest stays in the touch's `seen`, and `rows_stale_refused` is the claim, checked at `World.admit`, outside the method. Same split as E1: the pin is the claim, the leaf is the observation, and the observation is not written back onto the pin. Do not make "I pinned some digest" count as "this offer is here".

The peer cell's slot 0 is the package **id** (`Derive.objectCell` writes `env.bytes` of the package id at `slotPackage = 0`), not the package cell's content bytes. `bytesOf pkg` matches that only as the id encoding. The check is "same package id".

## (2) The fuse, and the Turn

[READ `Derive.lean:225`] `rowParent`: a run's row edit whose parent is not the running object is refused. X cannot retract Y's offer. Two runs is forced, not chosen. [READ `:210–231`] `invoke` runs the program, and only on `.ok (new, calls, rows, used)` builds a draft and `deriveCalls` the returned calls. A program error never enters the draft. [READ `:380–383`] `deriveTurn` seals the draft once, after `derive` returns `.ok`. [READ `:393`] `receive` is that Turn or an error. [READ `Kernel/World.lean:1565–1568`] `World.admit` is check-then-commit; an error returns no world. [READ `decisions/kernel.md:1893`] KERNEL-45: the tree seals one Turn, or fails whole.

So "Y.take refuses after X.fuse retracted" does not roll a world back. Fuse's retract exists only as a `RowAct` in a `Draft`. If take's run returns `.error`, `deriveCalls` fails, `sealTurn` is not called, `admit` is not called. Both rows stand because neither act was committed. F2 is the stricter path: a non-compliant pair is refused inside fuse's run, take never starts, and the draft is never built. The honesty plant (fuse skips the judge, take refuses) is the path where the retract is in the draft and then discarded. Say it that way. Do not say admit undoes a write.

The invitation is not a use-once token. [READ `Authority.lean:17–23`] `granteeHolds`: grantee equals the actor, or, for the first link only, a public grant whose actor is a live **member**. An object cannot hold `pub`. [READ `Derive.lean:305–312`] `checkGrantee` does accept an object, and [READ `Lang/Journey.lean:1782`] `(.grant y x [.invoke 0] none)` is the deployed shape. [READ `Authority.rightKey` / `spendAt`] `invoke` is not a counted right. Nothing spends the grant. B's grant to X authorises every later `take`; the row's retract is what stops the second spend. `invitation_once` per standing row is the right statement (Q3). Zoe's `spent_never_minted` (`minidregg/Kernel/Invitation.lean:160`) is a different object, and it would turn F1's "both rows gone" into "both rows taken", against plan §1 B7. Condition 6.

Q4 stays out. A public grant held by an object is `granteeHolds` accepting `kindObject` on `pub`, which weakens the check. Not this card.

## (3) Q6: L, and it is not a joint law

[READ `decisions/kernel.md:1908`] item 3, deferred until "the first row whose invariant spans two objects changed in one turn". Price named there: "a separate judge (as LANG-44's row guards are)", so the law theorems keep their statements. Row guards run inside `run` (`guardEdits`, `Program.lean:428`), not in `deriveTurn`. L is that price. K adds a field to `Program` and a call in `deriveTurn`; the 85 / 86 / 59 / 51 / 21 stay put only because L does not touch `Program.judge`. Rule L. K's trigger, as the IMPACT writes it (two packages, or a method no generator wrote), is the right trigger and it has no reader today.

L is not what the words "a joint law" claim. Each side runs `offerJoint` on the two pinned rows. The Turn admits only when both runs return `.ok`, because the tree fails whole. That coupling is the call tree, not a judgment whose subject is the pair of rows.

The mutation that separates them: change one side's judge and leave the other.

- P2, fuse's judge dropped, take's kept. On F2 the Turn does not admit: take refuses, both rows stand. From outside the Turn this looks joint. It is not. `fuse`'s `Program.run` returns `.ok` on a pair `jointOk` rejects, and `take`'s run returns `.error` on the same rows. Two local checks disagree. A joint judge has one answer. `fuse_iff_compliant` is false; `take_iff_compliant` is true. On F1 (the pair is compliant) fuse still does not evaluate `offerJoint`, take does, `receive` is `.ok`, and `jointLaw_sound`'s both-evaluated conjunct is false. The plant table does not say that. Condition 1.
- The converse plant is missing. Take's judge dropped, fuse's kept: F2 stays refused, now by fuse, and the Turn never shows that take would have accepted. `take_iff_compliant` is the only tooth, and nothing in §5 reds it alone. Condition 1.

`jointLaw_sound` as stated (both runs evaluated `offerJoint` to `ok` on those two pinned values, and `jointOk` holds) is the honest theorem for two checks. It is not a theorem of one judge over the sealed draft. The amendment line says "two evaluations of one generated term, coupled by the call tree". It does not say item 3 landed as K, and it does not say one law judged both rows.

## (4) Q5: the roles claim is not earned

[READ `Lang/Contextual/Protocol.lean:76–78`, `:110`] `Iface.chooser : Role`. `fill` is `if I.chooser = me then σ i h else none`. [READ `ProtocolTyping.lean:34`, `:49`] `HasProt sp me`, and the hole rule is `I.chooser = me`. PROT-2's verdict was that no theorem binds two roles and uses them as different non-`me` choosers, and that PROT-6 or PROT-3 would be the reader.

This card's judge is `o.role ≠ q.role` on two offer **values**, plus two boxes over θ. [READ the IMPACT §1(c), §2] the offer is a decidable box, not an `Iface`, and `HasProt` is not in the theorem list. A's offer and B's offer are distinguished by which object holds the row, and by a label in the row. They are not distinguished by `HasProt sp r1` and `HasProt sp r2`. A third `Role` still changes no `HasProt` theorem. The index bought nothing here.

Do not add the bridge so that the index has a reader. That is a Lean model beside the deployed judge, which is the twin the IMPACT refuses, correctly.

Do not revert the index in this landing. PROT-3's `proj` is still the named reader. P3-MEASURE, as the IMPACT cites it, dropped the session-type framing of **negotiation** (LITP D.3: one θ, no second round). It did not, on what I was given, collapse the Bell's projection. If ROOT rules that PROT-3 will not judge `HasProt sp r` for an `r` that is not `me`, the index reverts as its own card: 34 `RESTATES-MEANING` back, 0 hypotheses, the sentence PROT-2 already required. Condition 7.

## (5) The theorems

None of these is `∃ a b, a ≠ b ∧ h a = h b` over an unbounded hash. The `∃`s are a selected row, a peer in the same turn, or a θ inside a named box.

- **`offerJoint_meaning`.** Object: the generated term, `BigStep`. Without it, `fuse_iff_compliant` can say the run agrees with `jointOk` while the term returns `ok` for a different reason, or names the wrong conjunct. Not a disjunct. The mutation that falsifies it and not the run iff: the term swaps `sameRole` and `notCompliant`, and `fuse_iff`'s refusal is the disjunction of the two strings (the IMPACT writes it that way). Dropping the peer `inBox` reds this and `fuse_iff` together, and F2 at θ = 11 does not red it (condition 2). Keep.
- **`fuse_iff_compliant`.** Object: `Program.run` of `fuse`, the grain of a method run, not of `receive`. Without it, P2 is invisible at the Turn: take refuses, F2 stays red, and fuse is not a judge. Not a disjunct. Mutation: fuse emitted without the judge. False when the run returns `.ok` and `jointOk` is false. `jointLaw_sound` does not catch that on F2, because its premise is `receive = .ok`, which take prevents. This is the theorem P2 actually kills. Keep.
- **`take_iff_compliant`.** Object: `Program.run` of `take`. This is the honesty claim: Y retracts only after judging the pair itself. Without it, only the both-skipped plant (P3, F2 admits) exists, and a take that trusts fuse is green. Not a disjunct. Mutation: take without the judge, fuse keeping it. F2 stays refused by fuse. The theorem is the tooth, and it is not in §5. Condition 1. Keep, once that plant is named.
- **`fuse_atomic`.** Object: `receive = .ok t` and both offer slots carry `.retract` in `t.rows`. Without it, `fuse_iff` says the run returned a call; it does not say Y's retract is in the sealed Turn. Not a census disjunct: the `∃ y o q` is the two offer rows of that call. Mutation that hits it and not the run iffs: the call is returned, both runs return their retracts in the statement of the iffs, and one retract is absent from `t.rows`. P4 (fuse returns no call) also reds `fuse_iff`'s `calls` conjunct; the plant note that the ok-branch **rows** stay is right, and the table should say the calls conjunct goes red. "Neither" is not a conjunct of this theorem. It is "no Turn", which is `deriveTurn` failing, and it is already true of every refusal. Keep. The proof route can unfold `Dispatched` from a Lang file; it does not need a kernel edit.
- **`jointLaw_sound`.** Object: the two runs inside one `receive = .ok`, not `Program.judge`. Without the both-evaluated conjunct it is `take_iff` plus `fuse_atomic` (the pair was compliant because take ran). With the conjunct it is the statement that each side judged those pinned values. Not a disjunct. Mutation: fuse computes `jointOk` by something other than `offerJoint`, and returns `.ok` exactly when it holds. `fuse_iff` stays, `offerJoint_meaning` stays (the term is fine, unused), this theorem fails. P1 (`offerJoint := okT`) reds it and also the meaning and the disjoint theorem; that is a coarser plant, not a substitute. Condition 1. Keep under that reading. The name is not a licence to call it one judge.
- **`fuse_refused_disjoint`.** Object: the two concrete rows, buyer `[5,10]` and seller `[11,12]`. It replaces the arithmetic half of `separate_witnesses_over_substitutions` (each side satisfiable, no common θ), not the substitution-composition half (a typed guard-witness and a typed admission-witness, no θ that is both). Not a disjunct: the two `∃ θ` are witnesses inside the boxes, and the rest is `∀ θ, run = error`. Mutation `offerJoint := okT` reds it, and also reds `offerJoint_meaning` and admits F2. What F2 does not catch, and this does, is a judge that refuses only the journey's θ and accepts another. `fuse_iff` at that other θ catches it too; this is the packaged instance the plan named, over real rows. Keep. It is not a second copy of the old theorem.
- **`invitation_once`.** Object: `receive` then `World.admit`, then a second run on the resulting world. Without it, `fuse_atomic` says the retracts are in the Turn and does not say the rows are gone or that the second call refuses. Not a disjunct. Mutation: the generator upserts where it should retract. That also reds `fuse_atomic` (the act is not `.retract`). The mutation that hits only this one: the turn retracts, and the second run looks up a different slot and succeeds. P5 as written is the coarser plant; F5 is the row. Keep, with condition 6 in the docstring. Re-post at the same `n` is outside the theorem, on purpose.
- **`peerReads_parent`.** Object: `peerReads`. Without it, a peer record built under `self` still typechecks against `readsTy`, and F1 happens to die `sameRole` only because the two rows then carry one object's role. A peer whose role differs from ours would fuse against our own row. Mutation: read under `self` (P6). Keep.
- **`peerReads_package`.** Object: the slot-0 check. Without it, F4 is the only tooth, and a foreign object of this package's layout is read. Mutation: drop the check (P7). Keep. The check is the package id, §1.
- **`peerReads_unpinned`.** Object: `readKind` / `pinned` on the peer cell. Without it, F3 is a journey row with no theorem. Mutation: an unpinned peer cell treated as absent or as live. Keep. It says nothing about an unpinned **row**. Condition 3.
- **`methodReads_conforms`**, **`methodReads_digests`.** Object: the rows argument `runSetupWith` actually builds. `readsData_conforms` and `readsData_digests` stay about `readsData`, which does not change; they do not cover the `peer` field. Without the lift, `runSetup_accepted_of` (`Provenance.lean:946`) is false or unprovable for a method that declares a peer: its proof applies `readsData_digests` to `hrows` (`:964`). The statements of the provenance theorems do not name `readsData`, so they are not in the restate list; the proofs must call the lift. Mutation: the peer record admits a digest `digestOf` rejects. Keep.

`offer_safe_forever` is §6, and it is not in this landing.

## (6) `row_turn_cases` and `offer_safe_forever`

[READ `Kernel/Proofs/InvokeTree.lean:886–894`] `object_turn_cases` is about the object **cell**: keep, or the top call is `write` or `law`, or some `Dispatched` invoke. It does not mention rows. [READ `Kernel/Proofs/Logic/History.lean:63–103`] `ObjectStep`'s payload is pins, package, laws, request, old state, new state, calls. The `invoke` constructor binds `rows` and drops them. Widening that payload is R-0046's fork B, refused. A separate theorem is the right shape.

It is a real statement over `World.admit`, and it is not yet a corollary of anything I read. [READ `InvokeTree.lean:148–155`] `dispatched_ok` concludes `R.1.effects = l₁ ++ r.1.effects ++ l₂`. Cell effects. The draft's `rows` are concatenated by `Draft.append` the same way, and no theorem says so. `Dispatched.call` does record the parent run's `rows` (`:68–80`). So `row_turn_cases` — a non-head row slot under `obj` changed by an admitted Turn iff a dispatched invoke of `obj` returned that act — is provable beside `object_turn_cases`, in a Lang file, without an `ObjectStep` edit and without a kernel edit. The IMPACT's "over `dispatched_ok`" overclaims the lemma it would use. The statement itself is the one to prove. Heads born by `create` are the other case; an offer row is not a head.

It is not mini's shape. [READ `minidregg/Kernel/Seat.lean:1649–1654`]

```
theorem seat_offer_safe_forever (empty : genesis.seats = [])
    (reachable : Reachable genesis world) :
    ∀ seat ∈ world.seats, safeAt world.book seat.account seat.proposal = true
```

`safeAt` is "every want met, or every give refunded", a state invariant of every open seat in every world reachable from no seats. The proposed nano statement's first conjunct is `termsOk` (lo ≤ hi) on every standing offer in every world of an `audit_ok` log. That is well-formedness of a box the insert guard already checks, and an open row satisfies it whether or not the offerer is safe. The safety is the second conjunct: a row that disappears was the owner's `withdraw`, or a compliant peer row disappears in the same step. Mini's forever-theorem does not say that; mini's `step_inv` does, off to the side. The quantifier (every open row, every world of an honest fold) matches. The predicate does not.

[READ `Kernel/Proofs/Audit.lean:275–277`] `audit_ok` is `audit = .ok ↔ World.fold = .ok ∧ Honest`. That is the right premise. `worlds` and `steps` in the IMPACT's statement are not defined (`git grep` finds unrelated `steps`). Define them as the prefixes of that fold, or state the theorem over `World.fold` and `Honest` directly.

L2 is its own landing. Its plant (the retract arm accepts `withdraw` from a non-owner occasion; the second conjunct reds) is a real tooth, and `fuse_iff` does not replace it. The value half waits for PROT-8. Condition 8: do not cite `Seat.lean:1651` as "the same theorem".

## (7) `Std.pending` is not the mechanism

Agreed. [READ `decisions/lang.md:1609–1648`] LANG-48 is a slot whose shape is fixed now and whose **value arrives later** (`open {closes, filler}` → `filled {by, value}`), absorbing in the `once` mode, with `pending_fill_binds` as the meaning. The fuse binds in the Turn that retracts both rows. Nothing is filled afterwards. Settlement, if it ever moves value, is the session activity's resume, which is `Std.activity`, already built. A `Std.pending` generator here would have no reader in this card.

LANG-48 stays PROPOSED. Its trigger is unchanged: CappedTally and the escrow are two hand-written copies of "filled later", and the co-receipt is an `anyone` filler. Q4 keeps `anyone` out of this card for a different reason (public grants). Do not close the cv. Do not let this landing's decision say the slot was absorbed.

## (8) The deletions

None of the twelve is the only statement of a deployed fact. Each is a theorem about `Lang.Contextual.Protocol`'s private `World` (`:655`), which no importer outside the calculus mentions. [MEASURED] `git grep Contextual.Negotiation origin/main` hits comments only.

| theorem | what it is | the deployed fact, if any |
|---|---|---|
| `unrelated_update_keeps_plan`, `unrelated_update_repair_reuses` | `admits` / `repair` on the private store | `locality` stays in `Protocol.lean`'s proofs; the kernel frame is not this |
| `provider_revoked_unavailable`, `revocation_repair` | `World.revoke` on a `Provider` constructor | kernel revoke is KERNEL-25; E1's live column is the grant. Not this `World` |
| `current_at`, `representation_change_transports` | `Tok.at` / `Tok'.current`, plus `hasProt_mapTok` | `hasProt_mapTok` stays. The epoch encoding does not exist on a kernel pin |
| `stale_opening_refused` | private epoch mismatch | `rows_stale_refused`, `stale_refused`. A different stale |
| `competing_commitments`, `replay_refused` | a nullifier inside `World.commit` | journal replay is `Submit` / `Kernel/Proofs/Journal.lean` (`replayed`). The offer-row form is `fuse_atomic` + `invitation_once`, which this card adds |
| `deadline_expires` | the private clock | no deployed offer has this clock. The fact dies with the model. That is a deletion, not a hole |
| `AdmittedIn`, `separate_witnesses_over_substitutions` | one θ cannot be both the buyer-guard witness and the admission witness | the disjoint-box half becomes `fuse_refused_disjoint`. The "two substitutions, no common completion" half is not restated, and it is not a fact about `receive` |

`separate_witnesses_insufficient`, `witnesses_do_not_compose`, `greedy_vs_logical`, `search_state_ne_logical_status` are the scalar illustrations (`priceConds`, `firstFit`, `coverAll`). Nothing deployed calls them.

Do not delete, here, `Consistent`, `External`, `Internal`, `internal_once_not_external_once`, or the template / lost-reply family. They do not use `World` (the `World` hits in `Negotiation.lean` stop at the theorems in the table). They are PROT-5's named deletion, and removing them now would land that deletion with no replacement.

## (9) The price

`lang:` is right. Not `lang!`. Not a Bell re-emit.

[READ `Lang/StdActivity.lean:50–51`, `:185`] `activityLog` is the relation the generator already emits. The session row is one of those, with `activityWaiting` as its guard. `Std.activity`'s layout does not change, so the resident world does not re-genesis.

[READ `Lang/Package.lean:315–319`] `Sig` is `arg`, `calls`, `reads`, `edits`. The peer list is a field of the method **type's** rows record, parsed back, not a fifth field and not a codec tag. [READ `:674–675`] the version moves when a new tag turns a refused boundary into a read. A label inside an existing record `Ty` is not that. [MEASURED] `git grep '"peer"' origin/main` on `*.lean` / `*.ob` is empty, so nothing that installs today is refused `badRel peer`. `packageWireVersion` is already 5 (E1's bump). Codec vectors of existing sites stay byte-identical if `rowsTy rels rs []` is defined to be `readsTy rels rs`, not a wrapper. That equation is the thing to check at build; it is the whole of "no byte moves".

Restatements, statements that **name** the setup's rows step, one hypothesis replaced by one, none gained:

- `runSetup_spec`, `runSetupWith_spec` (`Load.lean:407`, `:429`)
- `runMeasured_means` (`Extract.lean:363`, the conjunct at `:374`)
- `invoke_never_stuck` (`Invoke.lean:461`, hypothesis at `:470`)
- the live twin (`LiveInvoke.lean:47`)
- `methodSig_spec` (`Load.lean:334`): `readsTy` becomes `rowsTy … ps`. For `ps = []` the meaning is the old one; the elaborated statement changes, so `RESTATES-MEANING`, not `RESTATES`.

That is the six. `readsData_conforms` and `readsData_digests` are not restatements: `readsData` is unchanged. The provenance theorems (`runSetup_accepted_of`, `runSetup_sources`, the `program_run_past_extraction` pair) do not name `readsData` in the statement; their proofs must follow `hrows` onto `methodReads_digests`. Count them as proof edits, not as hypotheses.

[READ `Ledger/Proofs/EscrowWitness.lean:56`] the private `setup_eq` has the same hypothesis. One cross-layer statement, proof shape unchanged. The ASK is the right size. Law theorems: 0 under L, because `Program.judge` and `deriveTurn` are not edited. I did not re-count K's 17 files; they are the price of the fork this ruling does not take.

Q1, same package: yes. A peer from `imports`, read at the imported `RelDecl`, trusts a declaration the reader's package did not check. Nothing in F0–F6 needs it. Q2, escrow to PROT-8: yes. An offer that moves no value does not exercise the fuse, and `Val` is not landed.

---

What may land after the eight conditions: the declared peer read, `Std.offer`, fork L as two checks, the theorems in §5 with the plants named there, `invitation_once` as a row fact, the Negotiation `World` and the scalar matchers gone, `lang:` plus the one Ledger statement if it is granted. What may not land: a joint law, a `Sig` field, `Std.pending`, a `HasProt` bridge, a use-once grant, or `offer_safe_forever` described as mini's `safeAt`.
