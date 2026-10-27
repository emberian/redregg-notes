VERDICT: DOCSTRING C9

`commit_checks_justification_atomically` is a rename of `invoke`. Do not land it. Do not land `cellLive_pinned` on this card. Land a docstring that says the pin check and the derived calls share one Turn, and land the plan's two-Turn split as a journey row that records admission. The builder's plant (commit with no `select`, P8.2 goes red) is a weaker mutation C1 already catches.

Base read: nano `origin/main` = **4916f3a** (fetched). Nothing built.

---

## 1. The conjunction is not a theorem

**Nano object.** [READ] `receive` builds one view and never another: `receiveWith X (pinned X.env w c.unsigned.pins) (rowView …) c` (`Kernel/Receive/Derive.lean`, `def receive`). [READ] `pinned` is `if pins.any (·.1 = c) then .ok (w.live E c) else .error (.unpinned c)` (`Kernel/Receive/Call.lean`). [READ] `invoke` runs `X.program.run look …` and then `deriveCalls sub obj ⟨[], writeOf obj (diffOps old new), [], rows⟩ … calls` on that same `look` argument (`def invoke`). [READ] `tree` / `dispatch` close `sub` over that same `look` (`dispatch` passes `tree X look rv c n` into `invoke`). [READ] A returned `.transfer` is `transfer X look …`, which calls `spendVia look transferBase via amount .transferSpent` (`Kernel/Receive/Ledger.lean`, `def transfer`; `spendVia` itself is `Kernel/Receive/Authority.lean`, not `Ledger.lean:113`).

The deployed instance is not "the certificate". [READ] `p8CommitPackage` builds `commit` as `activityApply select` and, in the `finish` the select's result is applied to, one `transfer` whose `via` is `arg "grant"` (`Lang/Journey.lean`, `def p8CommitPackage`). [READ] The journey fills that argument with `cap` (`p8Arg asset owner cap`; REOR C1's cite of `via = cap` still matches). The cell the judge reads is the provider grant, through the live facts column. The cell the ledger spends is `cap`. Two cells, one method, one `look`.

**What the proposed statement actually says.** [READ, IMPACT-C9 §1.2] `invoke … = .ok (d, wk') → ∃ …, X.program.run look … = .ok (…) ∧ deriveCalls sub … = .ok (d, wk')`, plus a prose rider that at `sub = tree X look …` a transfer's spend is `spendVia look`. The `∃` does not mention `cellLive`, a support, `spendVia`, or `receive`. `sub` is a parameter of `invoke`; the shared `look` of the nested call is true only because the caller (`tree`) built `sub` from the `look` it also passed in. `wk''` in the written `∃` is not bound. [INFERRED] A type-correct repair is still `simp [invoke]`: the do-block, one binder, no new fact.

**Which landed theorem or consumer is weaker without it.** None.

- [READ] `cited_authenticated` (`Lang/Proofs/Rel.lean`): on a live `relReads`, slot `j`'s `live` bit is `cellLive look g` for the cell the key names. It already quantifies over the `look` the run was given.
- [READ] `selectHole_cell_support`: a successful `selectHole` has every `.cell` support at `look g = .ok (some cell)`. Its own tooth is `supportLive (.cell _) := true`, which leaves `selectHole_origin` true. That tooth is not a split of `invoke`.
- [READ] `revoked_support_refused` / `revoked_support_refused_hole`: a tombstone (`look g = .ok none`) yields no selection, and at the generated judge probes 3 and refuses `support0 dead`. The through-`submit` tooth is already the row `P8.2 re-pinned tombstone` (LANG-75.1). The comment on `revoked_support_refused_hole` already says "the commit's own read, in the same Turn as its spend." That sentence is the conjunction. It is not a proof obligation the comment fails to discharge; there is nothing further to discharge.
- [READ] `spendVia_ok` (`Kernel/Proofs/Ledger.lean`): `(via = none ∧ ef = none) ∨ ∃ g gc, via = some g ∧ readKind look g kindGrant = .ok gc ∧ spendAt … = .ok ef`. The left disjunct is the owner's own authority, nothing spent. Conjoining it does not force a counted spend, and the `g` it binds is the grant in `via` (`cap`), not the provider cell.
- [READ] P8.4 (`Lang/Journey.lean`: "RE-EXECUTE atomic checked commitment", counted left 0, then replay rejected and a second commit refused `accepted`) executes the one method. It does not become a stronger statement by naming `invoke`'s parameter.

**Disjunct check.** The proposed `∃` has no disjunct. It is not a hash collision and not an `∃ a b, a ≠ b ∧ h a = h b`. The vacuity is the other one in §8.2 / REOR D.3: two facts that are already theorems (or already the definition), written under one binder. `spendVia_ok`'s own `∨` is real (`via = none` spends nothing); it is not a new hole, and it means the plan's sketch "cell-support ∧ `spendVia_ok`" does not even say a unit moved.

**The mutation.** There is no deployed mutation that makes the conjunction false and that neither conjunct's tooth already catches.

- The plan's mutation (PROGRAM §1 B3, REOR B.9): split `commit` into two Turns so a revoke lands between them, and the later spend admits. [INFERRED] That row goes red against a safety claim, and it does not falsify the proposed theorem. Each Turn's `receive` still threads one `pinned`. Turn 1's `cellLive` was true (the provider was live). Turn 2's `spendVia_ok` is true of `cap` (still a live grant). The theorem stays. What failed is the method's shape, which is `p8CommitPackage`, not a lemma.
- The builder's plant (IMPACT-C9 §2): `commit` without its `select`, and P8.2's re-pinned tombstone admits. That is a different mutation, and a weaker one. It deletes the check. [READ] LANG-75.1 plant (c) already does that observable: `holeProbePoint` ignores `live` → P8.2 and LH14b RED, LH14a stays green; plant (a) `cellLive := true` admits P8.2 the same way. `revoked_support_refused_hole`'s tooth is that edit. A conjunction-theorem is not what goes false.
- The mutation the IMPACT names for the lemma ("`deriveCalls` under `pinned` of another World") is an edit of `tree`/`invoke` that no row performs. It falsifies a sentence that restates the function. It is not a plant.

No mutation specific to the conjunction. The card's own refuter then applies: it is a docstring on `cellLive` / KERNEL-60.

## 2. `cellLive_pinned`

[READ] `cellLive_iff`: `cellLive look g = true ↔ ∃ c, look g = .ok (some c)`. [READ] `World.live` is `some cell` only on `.live cell _`, and `none` on a tombstone or an absence. [READ] `cited_authenticated` never mentions `World` or the pin list; it says the bit equals `cellLive` of whatever `look` the read was given.

So the proposed iff

`cellLive (pinned E w pins) g = true ↔ (∃ p ∈ pins, p.1 = g) ∧ (w.live E g).isSome`

is `cellLive_iff` plus `unfold pinned` plus `Option.isSome`. [INFERRED] The proof is `simp [cellLive_iff, pinned]`.

What it adds, and only this: the right-hand side is the World's live column at the call's pins, not an abstract `look`. `cited_authenticated` does not say that. LANG-75.1 already says it in prose ("`pinned` returns `World.live`").

The distinct mutation is real and is not `cellLive_iff`'s. [INFERRED] `pinned` answering a pinned tombstone with `.ok (some _)` makes the iff false, and leaves both `cellLive_iff` and `cited_authenticated` true (they talk about whatever `look` returned). The parenthetical in IMPACT-C9 §1.1, "`cellLive` reading `(look g).isOk`", is `cellLive_iff`'s own tooth (E1 §4.1; plant (a) is the stronger `cellLive := true`). Do not list it as this lemma's mutation.

It still does not belong to C9. No landed consumer is weaker without it. The named consumer is C2's `kernelWorld` (`live (.cell g) := cellLive look g`), which is not landed. Consumer first: it rides with C2, or it does not land. Landing it here is a lemma ahead of its caller.

## 3. Premise price

0, confirmed, for the proposal as written and for the docstring landing. [READ] Both proposed statements are new; neither edits a landed theorem's hypotheses or a definition other than a comment. A binder is not a hypothesis, and this card does not even add a binder to an old statement. A journey row is not a premise. [INFERRED] The census digest diff of a docstring-plus-row landing is empty of theorem statements. The unbound `wk''` would not type-check; fixing it still adds no premise.

## 4. The LPCFS docstring claims more than the theorems give

[READ, IMPACT-C9 §3] The proposed sentence on `cellLive`: a provider's grant is "a use-once, revocable certificate (Morgenstern 2011)"; revocation retires the cell; "every reader of a fact that names it reads it through the call's pins"; "the spend that uses the certificate is derived from the same pinned view in the same Turn."

That says **certificate**. The theorems say **a pin check and one Turn**, and not even that as a combined statement.

- [READ] Use-once is KERNEL-60's ledger: `spendAt` / `spendVia` append `left - units` on the grant named by `via`. `cellLive` is `w.live` being `some`. Revocation is `revoke`'s `(g, .retire)`, after which `live` is `none`. A provider grant in P8 is retired, not spent. The thing spent is `cap`.
- [READ] "The spend that uses the certificate" identifies those two cells. `p8CommitPackage` does not. LPCFS's "each certificate in a submitted request, atomically with the use-once check" (REOR B.9, the plan's citation) is, here, a Lang term that reads one cell and spends another, under the one `look` `receive` already threaded. The kernel does not know the provider cell is authority for the transfer (REOR C1: `g` is an extra pin, `via` is `cap`).
- [READ] "Every reader" is false. LANG-75.1's residual: `(live)` is per read; a hand-written method that reads `facts` without it still treats a pin match as current. The generator rows (`LH0f`, P8's) cover Std.hole, not every package.
- [READ] `World.admit`'s pin check is not this atomicity. A re-pinned tombstone passes it (the pin names the tombstone) and fails the live read. That is P8.2, already a row.

The sentence that matches:

> A method's live read (`cellLive` at `pinned`) and the calls that run returns (`spendVia` included) are the same Turn: `receive` takes one `pinned` view and `invoke` runs and derives under it. That is the pin check plus one Turn. It is not a certificate the kernel consumes. In P8 the checked cell is the provider grant and the spent cell is `cap`.

Put that on `cellLive` (LANG-75.2 citing KERNEL-60). Do not put it in `decisions/kernel.md`. KERNEL-60's text is the counted ledger; this card does not change it. [AGREE with the IMPACT's default on Q2.]

## 5. What lands

- Docstring, the sentence in §4, not the certificate sentence.
- One journey row, the plan's plant, not the builder's. Shape: a Turn that `select`s while the provider is live, a revoke, a later Turn that spends `cap` and does not re-select. It **admits** and the unit moves. Record that admission. The row's point is that the kernel does not close the gap; the one method does. If this row refuses, the docstring is wrong and C9 comes back as a theorem — that is the card's refuter, and it has not been run. [INFERRED] It will admit, because the spend's `look` never reads the provider cell; do not treat this note as that run.
- Not `commit_checks_justification_atomically`.
- Not `cellLive_pinned` (C2's, when C2 has a caller).
- Not "commit without its `select` reds P8.2". That is plant (c) / P8.2, landed with C1.

Price 0. No wire. No re-genesis. `lang:` only if the new row is in the journey exe; the docstring alone is a comment.
