# DRAFT reply to akapug, emberian/minidregg#1 (do not post until ROOT/Ember approves)

Thanks, pug. We built this, and the commit credits you as co-author. It is on
`lane/floors`: the kernel commit 5225376f, plus the manifest pin 1b029fee, row fixes 506182d1 and the fixture re-emit f580e539. It lands on main through our integration queue. Here is what landed, where it
differs from your proposal, and one design choice that is still open to a veto.

## What landed

**Floors (`Theory/CanonicalResourceKernel.lean`).** Admission now has one solvency rule:
`Int.ofNat amount ≤ balance src asset + Int.ofNat (floor src asset)`. It applies to every
source, the issuer well included. `isIssuerMint` and the Boolean `sourceSolvent` are gone; we
kept no compatibility shim. Floors are Book state, `Book.floors : Π₀ (AccountId × AssetId), Nat`,
and absent means 0. One new operation sets them:

- `setFloor asset account floor` is a zero-value posting from the issuer well `asset` to
  `account`. Because its posting source is the well, the authority to extend credit in an asset
  is the authority that issues it. On the wire it needs the well's `mintAsset` verb
  (`ResourceMoneyWire.operationVerb`, and the realm-well `floor` command). A floor is never set
  below what the account already owes (`floorBelowBalance`).
- The theorems you listed are stated over the Book's own floors:
  `admitted_preserves_floors`, its batch form `Batch.apply_withinFloors`, and
  `outstanding_le_sum_floors` (given `totalAsset = 0` and the floor law, the positive balances
  sum to at most the sum of the floors).
- The equivalence with the old rule is two named theorems, `sourceWithinFloor_iff_preFloorRule`
  and `admission_iff_preFloorRule`. When every non-mint source has floor 0, and the well's floor
  covers the mint (the finite form of the old "unbounded well"), the floor rule admits exactly
  what `isIssuerMint ∨ amount ≤ balance` admitted.
- Refusals name the account: `belowFloor account asset`, `floorBelowBalance`, `sweepInexact`.
  Deregistration also refuses an account that still holds a floor (`floorRemains`), and
  registration refuses a hidden floor coordinate, just as it refuses a hidden balance.

**Sweep.** `sweep holder commons asset permille epochs amount` is the posting
`holder → commons`. It is admitted only when `amount = recycle (balance holder asset) permille epochs`.
`recycle` is pure integer demurrage: each epoch removes `⌊kept·permille/1000⌋`, so every
rounding remainder stays with the holder, and a balance at or below zero recycles nothing. If
the destination is the issuer well, the same posting is destruction, so the kernel does not
choose between recycling and destruction. The display is the view
`displayBalance balance permille epochs`, and it is never stored. The lemma that keeps it
honest is `sweep_materializes_display`: an admitted sweep writes exactly the displayed balance.

**Your example book** is `creditBook`/`creditBatch` in the same file. It has a well with cap
100, two members with limit 20, a commons account, and one sweep at 100‰ that moves 6 of 65
(the 0.5 stays with the holder). Named refusals, each by `decide`:
`credit_limit_refused` (a member paying past its limit), `issuance_cap_refused` (a mint past
the cap), `issuance_cap_nets_burns`, `floor_under_debt_refused`, `sweep_inexact_refused` and
`sweep_to_well_destroys`. We also planted a defect (wells unbounded again) and watched
`issuance_cap_refused` go red before we reverted it.

**External effects (`Kernel/IrreversibleEffectSettlement.lean`).**

- `Settlement.reconcile` takes a `quarantinedForward` settlement and new evidence for the same
  forward command. The `Observed` type is indexed by the command, so evidence about any other
  command does not typecheck. Performed against a fresh pre-root commits, not performed refuses,
  and indeterminate stays quarantined. It never produces a compensation (`reconcile_status`).
- `KeyedTarget` is the first `ImplementationRefinement` instance: a toy class-1 target whose
  physical state is the list of keys it has applied. A performed receipt must carry the
  intent's own key.
  - `refinement`: the instance itself.
  - `duplicate_forward_no_second_effect`: once a key is applied, every step on a forward
    command for it leaves the target unchanged.
  - `applied_at_most_once`: in every represented state, each key is applied at most once.
  - `lost_reply_reconciled`: a reply is lost, the settlement is quarantined, the retry is
    answered from the key table, and the reconcile commits the exact post.
- Your class 1/2/3 taxonomy is now a note in PROJECT.md (§ Privacy and external effects). It
  says plainly that only class 1 has an instance, and that one is a toy.

## Where it differs from your proposal, and why

1. **Floors are committed Book state, not a policy parameter of admission.** A parameter
   would let whoever calls admission choose the floors. In a deployment, the cap and the limits
   have to be committed and changed under authority. Your `Admission' floors book op` becomes
   `Admission book op` reading `book.floor`.
2. **The invariant is over every account, not just registered ones.** `WithinFloors` quantifies
   over all accounts. The registration and deregistration checks plus the extended
   `AccountSupported` law keep floor coordinates on registered accounts only.
3. **Sweep authority and the epoch clock are not bound yet.** The kernel checks the arithmetic
   (`amount = recycle …` on the pre-book). The Book has no clock, and nothing yet attenuates a
   standing grant to sweep-only. So today `epochs` and `permille` are operation fields that the
   holder's ordinary transfer authority must cover. Binding them to the clock cell and to a
   sweep-only grant is filed as follow-up work (cv 01a13e34).
4. **The rule changes for every existing mint path.** See the next section.

## The design choice open to veto: the issuer is capped

Floors **replace** `isIssuerMint`, so every issuer well now has a finite cap (its own floor),
not an unbounded one.

- **Genesis.** Genesis takes a mandatory `issuanceCap`. The genesis source frame is v6, and v5
  sources refuse. The cap is installed as the tariff asset's well floor, and genesis validity
  requires the sum of the initial balances to be at most the cap. `initialBook_withinFloors`
  proves the floor law holds from the start.
- **Paid credit.** It now nets against the cap. Burns restore headroom. The pay well has no
  runtime path to raise its cap yet, so in a deployment it is fixed at genesis.
- **Realm wells.** They start at cap 0 until the founder sets one with `mini well --action floor`
  (account = the well).

This is an economics choice, and Ember may veto it. The alternative is to keep wells unbounded
and use floors only for credit limits. The equivalence theorem above shows exactly what that
alternative would admit.

Nothing is needed from you. If ClockDAG wants to use `outstanding_le_sum_floors` as its
checkpoint cross-check, it is the well-inclusive Σδ = 0 you described, with the well's floor
as the cap.
