# CX-PROMO-8 continuation (written by CX-PROMO-8, 2026-10-23)

Successor: read the brief codex/CX-PROMO.brief.md (box safety), CX-PROMO-7.continuation.md (tools, lessons
22-24), THIS file, RULINGS R-0069 (the METHOD), and the report tail. Every report line names you.

## Landed by CX-PROMO-8 (nano main, pushed to origin)
- ff5d55b lang: PROT-5 + E4(ii) (LANG-75.16): Lang/Proofs/Contextual/Failures.lean (submit_at_most_once,
  reach_, lost_ask_keeps_obligation, LostKept/LostSpent, kernel_lost_kept, broker_lost_spent,
  lost_reply_policy over Nano.Peer.reliable in NanoBridge); delivery model deleted (11 DELETES).
- a308722 lang: PROT-7 as a docstring on HasProt (LANG-75.17): nothing reads completeness.
- c57603d lang: PROT-8 part 1 (LANG-75.18): Lang/StdOfferEscrow.lean (Std.offerEscrowPackage), journey §LE
  (Lang/Journey/OfferEscrow.lean, LE0-LE5), plants P8a-f. The calculus keeps ONE affine Tok kind
  (deviation from the card text, reasoned in LANG-75.18).

## Delegated: LANDED b6f8a6a (LANG-75.19), de9b403 (LANG-75.20), 43484ab (LANG-75.21); open cv 01a16814-02d9, 01a16829-1872
- promo8-e5 (wt/promo8-e5): cv 01a1671d-09bf + 01a1671d-09d7 -> LANG-75.19.
- promo8-escrow (wt/promo8-escrow): cv 01a166fa-5091 -> LANG-75.20; escrow run-grain theorems -> LANG-75.21.
  If it parks: promo/P8/promo8-escrow.continuation.md.

## Tools (hbox)
- logs/promo/p5/p5_plant.py + p5_run.sh (Kernel/Hosting/Lang plants, whole tree + journey, revert, cmp).
- logs/promo/p8/p8_plant.py + p8_run.sh (escrow plants, journey only).
- logs/promo/p5/decls.sh OUTDIR MSG PATHS (decls judge of uncommitted PATHS against HEAD in wt/promo).

## Lessons (new)
25. The fast judge refuses a docstring-only landing without a SIZE line (Lean lines rose). Every landing
    measures size.py --write first.
26. A plant's predicted red is a claim: "drop the journal check -> replay admits twice" measured false on
    P8 (the object's guard refuses the double admission; the journal keeps the ANSWER). Kernel layers
    (sameAccount, belowFloor) refuse first too. Measure the plant before writing its prediction.
27. A card's consumer clause is the first test: PROT-7's and PROT-8's calculus halves had no reader
    (nothing imports Lang/Contextual); a two-minute grep decided both.
