# CX-PROMO-8/promo8-escrow — the fuse deal names its offer; the escrow's run-grain theorems (LANG-75.20, LANG-75.21)

Read /Users/ember/dev/redregg/work/promo/P8/HELPER-COMMON.md first, whole. Worktree NAME = promo8-escrow.

Context to read: Lang/StdOffer.lean (Std.offer, PROT-6: fuse/post/take/withdraw, `offerJoint`,
`offer_guard`), Lang/StdOfferEscrow.lean (PROT-8, c57603d: the same with a value leg `give {amount, asset}`
and `payTo` on the offer row; post/take/withdraw each make ONE transfer call), Lang/Proofs/StdOffer.lean
(`take_iff_compliant` at the term grain, `take_run_sound` (~line 847) and `fuse_calls` at the deployed
`Lang.program` run, and their private helpers), Lang/Proofs/StdOfferFuse.lean (`fuse_atomic`,
`jointLaw_sound`, `invitation_once`), Lang/Journey/Offer.lean (§LF) and Lang/Journey/OfferEscrow.lean
(§LE), and decisions LANG-75.11 and LANG-75.18 (grep `### LANG-75.11`, `### LANG-75.18` in decisions/lang.md).

CARD A (first; its own landing, `lang:`, decision `### LANG-75.20`): cv 01a166fa-5091 (`cv task show`).
Today a take consumes whichever of its own offers the CALL pinned (the deal names no key), so a matcher
picks which of a party's standing offers a fuse consumes. Make the deal name its offer, one key per side
(e.g. `{pair, theta, keys {a, b}}`), in BOTH generators (they share `offerTakeArg`); the take refuses
(a new named refusal) when its pinned own row's key is not the one the deal names for it. Theorem: the
consumed rows are exactly the named ones (restate `take_run_sound`'s row-acts conclusion with the named
key; restatements are RESTATES-MEANING map lines). Journey: a row where the matcher pins another standing
offer than the one named -> refused by name (LF has Y's offers 0/1/2: use them). Also the task's second
half: today plants P1-P5 red Lang/Proofs/StdOffer.lean so Lang/Proofs/StdOfferFuse.lean never elaborates;
restructure so each plant reds exactly its own theorem's module (plant at a site the upstream proof does
not unfold) and record each red by name. Close cv 01a166fa-5091 with the hash.

CARD B (second; `lang:`, decision `### LANG-75.21`): the escrow's run-grain theorems, new file
Lang/Proofs/StdOfferEscrow.lean, mirroring `take_run_sound` / `fuse_calls` over
`offerEscrowPackageOf theta roles ol sl b` and `Lang.program`'s run:
- `escrow_take_run_sound`: a returned take decoded its deal, read both pinned offers, found their
  `{role, terms}` JointOk, its ONE call is `transfer (of self give.asset) (of peerPayTo give.asset)
  give.amount (via none) (once none)` with `give` its own pinned offer's leg and `peerPayTo` the peer's
  pinned offer's `payTo`, and its row acts are exactly its own offer's retract and its own session insert.
- `escrow_withdraw_run_sound`: a returned withdraw read its own pinned offer (present), its one call
  pays that offer's leg from self to the offer's own `payTo`, its one row act is that offer's retract.
- `escrow_post_run_sound`: a returned post's one call moves `give` from `of agent asset` to
  `of self asset` via `some grant`, its one row act inserts exactly that offer value.
- `escrow_retract_moves_leg` (the linear corollary, the point of PROT-8): for every returned run of any
  method of the escrow package, every retract of an `offer` row among its row acts comes with a call in
  the same result transferring THAT row's `give` out of the object (to the peer's or the row's own
  `payTo`); `fuse` makes no row act. State it over the package's run, not per method.
Plants: the landed plants P8d (take pays nothing: in the take body's `done`, the call slot `none`) and
P8e (withdraw pays nothing) must now ALSO red `escrow_take_run_sound` / `escrow_withdraw_run_sound` and
`escrow_retract_moves_leg` by name, observed (the plant sits in Lang/StdOfferEscrow.lean, upstream of
your proof module; the journey rows LE1/LE3 red too). CX-PROMO-8's plant script with those two plants:
/tank/dregg-build/nanodregg/logs/promo/p8/p8_plant.py (copy it; it edits paths relative to the cwd).
If the run-grain statement needs a lemma the tree lacks (TAKE measured ~400 lines for the run-grain
CONVERSE of take; you need only the soundness direction, as take_run_sound), say what is missing and
land the term-grain versions (as take_iff_compliant is) rather than a containment.
