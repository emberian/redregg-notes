# IMPACT-PROT-2 · roles replace `Polarity`; the Bell's open/close/retire, measured

CX-PROMO-4, 2026-10-23, nano main `50e8805` (hbox `wt/promo`). Plan §3 P3 PROT-2 + E4(i); R-0044 (the Bell signer
defect rides here; cv 01a165f1-a212); R-0046 ("then PROT-2 as the next card"). Grant: R-0044's Lang/**.
Artifacts: `promo/PROT2/` (candidate diff, plant diffs and logs, the journey output).

**Candidate BUILT**: the protocol cone (`lake build Lang.Proofs.Contextual.Negotiation`) GREEN; `lang-journey` GREEN with
three new rows; whole tree running (result appended as §7). Nothing landed.

## 1. The Bell half, MEASURED first: the defect as filed does not exist

cv 01a165f1-a212 (from IMPACT-P3-MEASURE): "the Bell's open/close/retire check no signer: any member can close or retire
another member's bell". The Bell's METHODS check no signer. That is true (`world/resident/Bell.ob`: `close`, `open` and
`retire` have no `check`). But a member cannot invoke them. The kernel gives invoke authority PER METHOD:
`invoke_authorized` (`Kernel/Proofs/Authority.lean:117`, KERNEL-25) says a derived invoke comes from the object's
owner, or from an agent whose grant chain names `invoke method` and is rooted at the owner. Otherwise it is refused
`noGrant` / `grantRight`. The deployed Bell (`launcher/tests/resident_bell.rs:253-257`) grants the resident
`observe,invoke:0` (answer) and a ringer `observe,invoke:4` (ring). Nobody but the operator holds `invoke:1|2|3`.

Journey rows, new, through the real receivers (`Lang/Journey.lean`, before LB12; `promo/PROT2/journey.txt`):

    ok   LB12n B (the resident, granted answer and ring) closes A's bell: refused grantRight …
    ok   LB12o B opens A's bell: refused grantRight …
    ok   LB12q B retires A's answered ring at 53: refused grantRight …

Each row also asserts the state is unchanged: the bell still open, and the ring still present. The role that opens,
closes and retires is **the object's owner or a holder of a grant naming the method**. The refusal is named
(`grantRight`), and the kernel makes it before the Bell runs. A package-level `check (deq req.agent state.resident)` on
`close` would be WRONG: it would refuse the operator (LB12 "A closes the bell", the owner who is not the resident).
**So the Bell needs no Lang check, the package does not re-emit, and no byte moves.** The rows are the "named refusal +
journey row" the card asks for. The refusal is the kernel's.

What stays a real question (Q2, a design fork, not a defect): a member the operator grants `invoke:3` can retire ANY
answered ring, not only its own. A ringer-scoped retire would be a package-level role (`retire` by the ring's
`ringer` or the resident). That is taste: it limits what an operator can delegate.

## 2. The calculus half: roles replace `Polarity` (as built)

`Lang/Contextual/Protocol.lean`:
- `Polarity` (`ours | theirs`) DELETED.
- `Iface S Hole A Role Tok Fact Ob i`, field `chooser : Role` (was `pol : Polarity`). `Ctx` and `Open` gain `Role`.
  `Open` gains `me : Role`, the role whose object it is.
- `Subst.ours Ω σ` → `Subst.mine me Ω σ` (fills the holes `me` chooses). `fill Ω σ P` → `fill me Ω σ P`.
- The examples name their roles. Coin: `Party.player | peer`. Negotiation: `Party.buyer | provider` (the provider
  answers `commit`), and its hole is chosen by `.buyer`.

`Lang/Proofs/Contextual/ProtocolTyping.lean`: `HasProt sp me Ω …`, whose hole rule requires `I.chooser = me` (was
`I.pol = .ours`). `Fills sp me`, `SubstOK sp me` (`I.chooser = me`). `Open.WF` and `Open.Replan` read `O.me`.

Theorems (`Lang/Proofs/Contextual/Protocol.lean`), as statements:

```lean
theorem fill_skips_others (σ) (hI : Ω i h = some I) (hp : I.chooser ≠ me) : fill me Ω σ (.hole h) = .hole h
theorem others_hole_untypable (hI : Ω i h = some I) (hp : I.chooser ≠ me) : ¬ HasProt sp me Ω Γ Q Φ Δ (.hole h)
theorem hasProt_holes_mine : HasProt sp me Ω Γ Q Φ Δ P → Occurs P j h → ∃ I, Ω j h = some I ∧ I.chooser = me   -- NEW
theorem Coin.peer_hole_never_planned (σ b) : wins b (fill .player (ctxOf .peer) σ planHole) () = false
```

`hasProt_holes_mine` is the plan's "a theirs hole becomes a call whose responder is a role", stated. Every hole of a
protocol judged as `me`, at any depth, is one `me` chooses. A component another role decides can only enter `me`'s
protocol as a `call`, whose continuation is a family over that role's answer. `others_hole_untypable` is its top-level
case (Q3).

**Not built: a `responder : Op → Role` in `Spec`.** No theorem here reads it. A field nothing reads is the no-op the
charter forbids. Its consumer is PROT-3's global type and projection (`proj` needs who answers each call). Default:
it lands there (Q1).

## 3. Price (MEASURED: the decls export of the cone against main's cached digest)

`gates/decls.py export` over the 6 cone modules, `digest_row` against the parent cache `a1817724…`.

- **Statement changed (RESTATES-MEANING), 34.** `HasProt` gains its index `me`, so every theorem that mentions `HasProt`,
  `SubstOK`, `Fills`, `fill` or `Open.WF` restates. So does every Negotiation theorem whose `Ω` or `obj` type gained
  `Role`. Protocol (10): `HasProt.weaken`, `subst_preserves_hasProt`, `fill_preserves_hasProt`, `fill_eq_subst`,
  `hasProt_reach`, `at_most_once`, `hasProt_runs`, `started_obligations`, `Open.resubst_wf`, `hasProt_mapTok`. ProtocolTyping (3): the projections `Open.WF.typed/substOK/started`. Negotiation (21): `template_hasProt`,
  `choose_ok`, `plan_fills`, `cancel_fills`, `planFlip_fills`, `instantiations_hasProt`, `holes_instance`,
  `cancel_path_refunds_obligation`, `commit_path_pays`, `reach_reserved`, `started_lost`, `lost_reply_not_started`,
  `lost_reply_keeps_obligation`, `lost_reply_blocks_replan`, `answered_blocks_replan`, `guard_stricter_than_wf`,
  `guarded_replan_after_dispatch_is_noop`, `replan_before_dispatch`, `provider_revoked_unavailable`,
  `representation_change_transports`, `separate_witnesses_over_substitutions`.
- **Renamed and restated, 4:** `fill_skips_theirs → fill_skips_others`, `theirs_hole_untypable →
  others_hole_untypable`, `SubstOK.ours → SubstOK.mine`, `Coin.theirs_never_planned → Coin.peer_hole_never_planned`.
- **Deleted, 5 lines:** `Polarity` (with what it owns), `instDecidableEqPolarity`, `instReprPolarity`, `Iface.pol`,
  `Subst.ours`.
- **New:** `hasProt_holes_mine`, `Iface.chooser`, `Open.me`, `Subst.mine`, the two `Party` types.
- The plan's "~12 restatements" counted theorems that mention `.ours`. The measured count is 38 statements (34 + 4).
  The difference is the index on `HasProt`, which every judged statement carries. No hypothesis is gained: `me` is
  an index (a binder), not a premise. **No deployed consumer**: nothing outside these modules imports them (NanoBridge
  embeds the resident's `Prog` and mentions no `Iface`; its `nano_*` theorems are unchanged).
- Wire, fixtures, package ids: none. The Bell is unchanged. Journey: three rows added (LB12n/o/q). Every other row's
  text is unchanged. Gate: **`lang:` fast**.

## 4. Plants (the cone built under each, restored; `promo/PROT2/plant-*.log`)

| plant | mutation | red |
|---|---|---|
| **R2** | `Subst.mine` fills every hole (`if I.chooser = me ∨ True`) | `fill_skips_others` (:121), `Coin.peer_hole_never_planned` (:861): statements false |
| **R3** | the negotiation's hole chosen by `.provider` (a role mislabel) | Negotiation proofs from :269 to :416 (`fill .buyer` no longer fills the hole: the plan / cancel / lost-reply family); the module fails |
| **R1** | the hole rule without `I.chooser = me` | `others_hole_untypable` (:136) and `hasProt_holes_mine` (:147) by statement, and four proof scripts by the constructor's arity (`weaken`, `subst_preserves`, `hasProt_mapTok`): a definitional plant, reported as such |

`hasProt_holes_mine` has no plant that `others_hole_untypable` misses. One reds exactly when the other does, since the
second is the first at `Occurs.here`. So it is the general form of a restated rule, not a separate tooth (Q3).
Bell rows: the plant that would red LB12n/o/q is the kernel's grant check, already `invoke_authorized`'s tooth
(KERNEL-25). The rows are controls of the deployed role, not new teeth.

## 5. The landing

`lang:` fast. Files: `Lang/Contextual/Protocol.lean`, `Lang/Proofs/Contextual/{ProtocolTyping,Protocol,Negotiation}.lean`,
`Lang/Journey.lean`, `decisions/lang.md` (LANG-75.10). The message carries the 34 + 4 RESTATES-MEANING and 5 DELETES
lines (from the judge's own refusal if my export missed one). The cv task 01a165f1-a212 closes as MIS-MEASURED: the
kernel refuses by grant, and rows LB12n/o/q are the evidence.

## 6. Questions (defaults in bold)

1. `responder` in `Spec`: **lands with PROT-3's projection, its first reader (default)**, or now as an unread field.
2. The Bell's retire: **stay with the kernel's per-method grant (default)**. The operator decides who may retire. The
   alternative is a ringer-scoped `retire` check (a `lang!`: the Bell re-emits).
3. `hasProt_holes_mine` and `others_hole_untypable`: **keep both (default)**. The plan names the "becomes a call"
   statement and the restated rule. Or delete `others_hole_untypable` as `hasProt_holes_mine` at `Occurs.here`.

## 7. Whole tree

`lake build` on the candidate: GREEN, 726 jobs, 0 errors (hbox logs/promo/p2-whole.log).
