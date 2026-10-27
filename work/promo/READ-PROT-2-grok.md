VERDICT: RULE PROT-2

Do not land this as "roles replace Polarity". Land the type and the rename, with no roles claim. Base: nanodregg `origin/main` = `50e8805` (fetched this read; local `HEAD` is `7e02852`, behind). `Authority.lean`, `Kernel/Receive/{Authority,Call,Derive}.lean` blobs match `HEAD`. `Bell.ob`, `Lang/Journey.lean`, `launcher/tests/resident_bell.rs` do not; those were read from `origin/main`. The candidate is `promo/PROT2/candidate.diff` (its `Protocol.lean` base blob `beec095` is `origin/main`'s). No build.

Conditions:

1. **Docstring-plus-rename, not a projection.** Delete `Polarity`. Keep `Role` as an index, `Iface.chooser`, `Open.me`, `Subst.mine`, `fill me`, `HasProt sp me`. Strike, from `Iface`'s docstring and from `hasProt_holes_mine`'s, the sentences that this is "not a two-valued side" and that another role's choice "enters as a `call` that role answers". Neither is a theorem. `LANG-75.10` says the same: an open index in place of `ours | theirs`, not HYC / Scalas–Yoshida projection. Do not add a theorem whose only job is to mention a third role; it would have no reader, which is why `responder` was correctly left out.
2. **The 34 lines stay `RESTATES-MEANING`, and the message says why that verb is not a meaning change.** GATES-20t accepts exactly one spelling. It does not accept either. The commit message states that no hypothesis was gained and that no theorem distinguishes two non-`me` roles.
3. **Bell rows may land with that rename, after the state conjuncts look at the run the call returned.** They close cv `01a165f1-a212` as mis-measured. They are controls of `invoke_authorized`, not a new tooth, and not the plan's tooth (`activity_resume_requires_resumer` is untouched).
4. **Do not cite R1 as a tooth.** R2 and R3 are the plants, and they red different theorems.

The card is shaped so PROT-6 can name two chooser roles on this `Iface` / `HasProt` without another index on `HasProt`. It is not shaped for an acceptor, and not for a call's responder. Those stay with their first reader (PROT-6, PROT-3).

---

## (1) The Bell: the filed defect does not exist

The predecessor was not wrong about the method bodies. The predecessor was incomplete: the kernel refuses the invoke before a body runs.

[READ `origin/main:world/resident/Bell.ob`] Methods in order, which the journey checks: `answer`, `close`, `open`, `retire`, `ring` (`journey.txt` LB1: `methods [answer, close, open, retire, ring]`, admitted). `answer` has `check ((deq req.agent state.resident) "notResident")`. `ring` has `check (state.open "closed")`. `close`, `open`, and `retire` have no `check`. [MEASURED `journey.txt` LB9] The owner, who may invoke every method, reaches `answer`'s body and is refused `program "answer: refused notResident"`. [MEASURED LB10, LB12] The same owner retires and closes, and those are admitted. So a body with no signer check really does let the owner through. That half of the reading is true.

[READ `Kernel/Receive/Derive.lean:182-231`, blob identical on `origin/main`] `invoke` calls `invokeRun` and only then `X.program.run`. `invokeRun` calls `ownerAuthority` on `Right.invoke method` before returning. The method body is not reached if that fails. [READ `Kernel/Receive/Authority.lean:33-61`] `walk` requires the grant's slot for that right, else `grantRight g` (`:41`). `ownerAuthority` then requires the principal to be the owner, else `noGrant obj` (`:60`). `via = none` never consults a grant: `principalOf` returns the actor. [READ `Kernel/Proofs/Authority.lean:113-152`] `invoke_authorized` (`:117`, KERNEL-25) is that gate as a theorem: a derived invoke is the owner, or a grant chain for `.invoke method` rooted at the owner. `invoke_stranger_noGrant` (`:145`) says the stranger with `via = none` is `noGrant` "before any method runs or any law judges". `ownerAuthority_program_free` (`:158`) says the gate does not read the program.

Per method, not per object. [READ `origin/main:Lang/Journey.lean:1296-1300`] LB3 grants B `[.invoke 0, .invoke 4]` and every later call by B goes `via` that grant. Methods 1, 2, 3 are not on it, so `walk` refuses `grantRight` and `program.run` does not start. [MEASURED `promo/PROT2/journey.txt:136-140`]

```
ok   LB12n B (the resident, granted answer and ring) closes A's bell: refused grantRight …
ok   LB12o B opens A's bell: refused grantRight …
ok   LB12q B retires A's answered ring at 53: refused grantRight …
ok   LB12 A closes the bell: admitted
```

[READ `origin/main:launcher/tests/resident_bell.rs`] The deployed split is the same fact with the rights on two grants, not one: resident `m` gets `observe,invoke:0` on bell `b`, founder C gets `observe,invoke:4` (`grant(&b, &c, "observe,invoke:4")`). The header calls C the member "granted `ring`". Nobody is granted `invoke:1`, `invoke:2`, or `invoke:3`. The operator retires as owner (`invoke` method `"3"`, Q5), which needs no grant. The impact's `:253-257` matches this block in the checkout's copy of the file; the origin blob differs later (activity row parsing, `(agent #…)`), and the grant text is the same. [INFERRED] line numbers on origin are those of the checkout if the prefix edits are line-count-neutral, which the two row-parser comments are.

A `check (deq req.agent state.resident)` on `close` would refuse LB12. The owner is not the resident. [READ the impact's Q2, agreed] A member the operator grants `invoke:3` can retire any answered ring. That is a delegation choice, not a hole in the gate.

**The state conjuncts do not observe the refusal.** [READ `candidate.diff` Journey hunk] LB12 threads the returned run (`r12`) into `bellField … "open" == some false`. LB12n/o/q bind `let (_, v, _) := go …` and then read `bellField` / `present` on the pre-call `r`. The open-bit and the ring's presence are the state before B's call. They stay true whether or not the call closed or retired. The rows go red only when the reply text does not start with `refused grantRight`. LB12o has no state conjunct at all. The impact's "each row also asserts the state is unchanged" is not what the predicates check. Thread the returned run, as LB12 does, or drop the sentence.

The rows are controls of KERNEL-25, through the real receiver. The plan's tooth for this card was `activity_resume_requires_resumer` (`StdActivityTeeth.lean:160`). The diff does not touch it. Nothing here is a new tooth, and the builder says so. That part is right.

## (2) The calculus: a polarity, on a wider type

Literature asked for a projection. [READ `LITERATURE-PROTOCOLS-20261022.md` C.1 PROT-2] Replace `ours | theirs` by a role set; a hole names its chooser; a `theirs` hole becomes a `call` whose responder is a role; restate the two polarity theorems as "a filling is typed in its chooser role's projection only". [READ HYC as that memo states it, not re-read this session] `G ↾ p` is a local type in which the other participants stay distinct. [INFERRED, from that memo's B.1 / Scalas–Yoshida citation, not from the papers this session] Same for a Scalas–Yoshida local type: an action still says who the other party is. PROT-3 is where `proj : Glob → Role → Prot` was supposed to land.

What was built is the binary test, indexed by a type. [READ `candidate.diff`]

- `Subst.mine` / `fill me`: `if I.chooser = me then σ i h else none`.
- `HasProt.hole`: `I.chooser = me`.
- `SubstOK`: `I.chooser = me`.
- `fill_skips_others`: hypothesis `I.chooser ≠ me`.
- `others_hole_untypable`: hypothesis `I.chooser ≠ me`.
- `hasProt_holes_mine`: conclusion `I.chooser = me`.

Every one of those is `= me` or `≠ me`. [READ the whole diff] No theorem binds two roles and uses them as different non-`me` choosers. `Coin.peer_hole_never_planned` is `fill .player (ctxOf .peer)`: peer is "not the player", and the game has no third party. Adding a third `Party` constructor would change no theorem's truth. `Negotiation.Party.provider` is an inhabitant and the prose subject of `commit`. No theorem mentions `.provider`. The R3 plant is the first use of that inhabitant as a chooser, and it is a mislabel, not a statement.

`hasProt_holes_mine` does not say the excluded component is a call, and it does not name who answers. [READ its statement in the diff]

```
HasProt sp me Ω Γ Q Φ Δ P → Occurs P j h → ∃ I, Ω j h = some I ∧ I.chooser = me
```

The "becomes a call whose responder is a role" sentence is the docstring. `Spec` has `consumes`, `requires`, `establishes`. No responder. A hole chosen by role A and a hole chosen by role B are the same fact to every theorem, once both differ from `me`: both skipped by `fill me`, both untypable as `me`. That is `ours | theirs` with `theirs` opened into an uninterpreted parameter.

So the 34 are not buying a distinction. They are the cost of writing the index into every statement that mentions `HasProt`, `fill`, `SubstOK`, or `Open.WF`. Under the translation `ours ↦ (chooser = me)`, `theirs ↦ (chooser ≠ me)`, each old theorem is the new one. [INFERRED] the definitions can tell A from B inside one `Ω` (`fill A` fills A's holes and skips B's); no theorem asks them to.

**PROT-6 can use the chooser index without a second restatement of `HasProt`.** [READ plan §3 PROT-6; literature C.1 PROT-6] An offer row is an `Iface` value with a chooser role. This `Iface.chooser : Role` and this `HasProt sp me` already are that. A fuse theorem may say `I1.chooser` and `I2.chooser`, or judge `HasProt sp r1` and `HasProt sp r2`, without changing the judgment's arity. The acceptor the plan names is not a field. The responder literature PROT-2 asked for is not a field. [INFERRED] adding an unread field later changes definition values and proofs that construct `Iface`; it does not by itself insert a binder into `HasProt`, so it is not another copy of these 34. Not measured; the exporter was not run. Do not add either field on this card.

This is not "rule in a third-role theorem now". A theorem with no consumer is the no-op the charter forbids, same as `responder`. The roles claim waits until PROT-6 (two offer choosers) or PROT-3 (`proj`) actually distinguishes them.

## (3) The 34, and the guard

[READ `gates/decls.py:27-42, 384-404, 477-528` and `decisions/gates.md` GATES-20t at `50e8805`] A two-name line rewrites constant names in the candidate (NEW → OLD, longest component-wise prefix) and then compares elaborated-statement digests. Binder names are erased; binder info is kept (`decls.py:17`). An extra binder is a different term either way.

- `RESTATES` requires the digests equal. If not: `restate not equal`, and the tool tells you to write `RESTATES-MEANING`.
- `RESTATES-MEANING` requires the digests differ. If they are equal under the map: `unused map line`.

One spelling is legal, never both. The 34 cannot be `RESTATES`. `HasProt sp Ω …` and `HasProt sp me Ω …` are not equal under a rename of declaration names.

They are also not a change of meaning in the plan's own price ("a binder is not a hypothesis"). [READ the impact §3, agreed] `me` is a section variable. No premise was added. The four renames (`fill_skips_theirs`, `theirs_hole_untypable`, `SubstOK.ours`, `Coin.theirs_never_planned`) are the old binary rules with a new literal; their digests differ for the same reason, so `RESTATES-MEANING` is what the guard demands there too, and `RENAMES` would be `rename not equal`.

[READ the impact's list against the diff] Protocol 10 and Negotiation 21 are the theorems whose statements the diff actually edits (`me`, `.buyer`, `fill .buyer`, `Subst.mine`). The ProtocolTyping 3 are the `Open.WF` projections; the structure's fields gained `me`, and this read did not re-export, so that 3 is the impact's count. [INFERRED] 10+21+3 = 34 matches the diff plus those projections. The plan's "~12" was the theorems that mentioned `.ours`. The gap is the index, as the impact says. Hypotheses gained: 0. That claim is right. Do not let the guard's verb stand in for it in the decision.

## (4) `responder` deferred

Acceptable. [READ `Spec` in `origin/main:Lang/Contextual/Protocol.lean:51-55`, unchanged by the diff] Nothing in this cone projects a responder. PROT-3's `proj` is the first reader the literature named. An unread field is the no-op they refused, and refusing it was the right call. The mistake is the docstring that talks as if the field existed, not the omission.

## (5) Plants

[READ `promo/PROT2/plant-R2.diff`, `plant-R3.diff`, `plant-R1.diff`, and the three logs]

**R2 is a plant.** `Subst.mine` becomes `if I.chooser = me ∨ True`. [MEASURED `plant-R2.log`] `Lang.Proofs.Contextual.Protocol` fails with unsolved goals, not an arity error: `fill_skips_others` at `:121` (the `match σ i h` does not reduce to `.hole h` under `I.chooser ≠ me`) and `Coin.peer_hole_never_planned` at `:861` (`wins` does not reduce to `false`). The statements are false. Negotiation is not built, because Protocol failed first.

**R3 is a plant, and it is not R2.** `Negotiation.iface.chooser := .provider` while every judgment is `.buyer`. [MEASURED `plant-R3.log`] `Protocol` builds (`[99/100]`). `Negotiation` fails. `template_hasProt` at `:47-48` and `:71` (`iface.chooser = Party.buyer` is not `rfl`). From `:269` the `change` tactics fail because `fill .buyer` is no longer definitionally the filled plan (`cancel_path_refunds_obligation`, `commit_path_pays`, `reach_reserved`, the lost-reply / replan family). Last error `:416`. The impact's ":269 to :416" is the back half; the module is already red at `:47`. Different file, different mutation, different theorems from R2.

**R1 is not a plant.** The hole rule drops `I.chooser = me` and keeps the other premises (`plant-R1.diff`). [MEASURED `plant-R1.log`] The failures are elaboration against the old constructor shape: "Too many variable names provided at alternative `hole`: 8 provided, but 7 expected" at `:72` and `:686`, and shifted premises at `others_hole_untypable` `:136` and `hasProt_holes_mine` `:147` (`hp'` / `hc` now have type `∀ f ∈ I.ctx` and the proof still applies them as `I.chooser = me`). `weaken`, `subst_preserves_hasProt`, and `hasProt_mapTok` break the same way. Those three stay true if the rule loses a premise; their proofs merely do not elaborate. A red that hits still-true theorems by arity does not identify a false statement. The impact calls it definitional and is right to. It is not a tooth. `hasProt_holes_mine` has no plant of its own: it is `others_hole_untypable` at `Occurs.here`, and the builder says that too.

---

What this card may land: `Polarity` deleted, the index and the rename, the four old rules under their new names, the 34 guard lines with the sentence that they are an index, and LB12n/o/q as the mis-measure, once their state conjuncts read the returned run. What it may not land: a roles claim, a projection claim, or R1 as a tooth.
