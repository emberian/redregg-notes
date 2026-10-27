// scenes-market.js — the market (DESIGN-CTX §2.5b): the escrow offer as a book, a stranger's take
// by name. The steps are the journey rows' own calls (Lang/Journey/OfferEscrow.lean §LE, §LF's
// lfTakeArg) as nd argv, and each refusal is its row's: LE9 a take a member signs (notFuser,
// LANG-100: only the book whose fuse judged the deal), LE7 a fuse with a thin leg (unfairLegs,
// LANG-82), LE1 the fuse that moves both legs in one Turn. The package text is the journey's own
// (`Lang.Std.offerEscrowPackage`), printed by the kernel (`tg_text`), never copied here.

/** LE0's post argument: `give` is the leg the offer holds, `want` the least leg it asks, `grant` the
 * poster's grant of transfer on its own account (KERNEL-60), `payTo` where the peer's leg is paid.
 * The one term is a box, `price` in `[lo, hi]`. */
const post = (v, n, role, lo, hi, amount, asset, grant, payTo, want, wasset) =>
  `(record (give (record (amount ${amount}) (asset #${asset}))) (grant #${grant}) (n ${n}) (payTo #${payTo}) (role ${role})` +
  ` (terms (record (price (record (hi ${hi}) (lo ${lo}))))) (want (record (amount ${want}) (asset #${wasset}))))`;

/** The deal, as LF's `lfFuseArg` and `lfTakeArg` spell it: each side's offer by number (`keys`), the
 * two books (`pair`), the terms both accepted (`theta`); a fuse also names the grant its call to the
 * peer's take goes through (`via`). A take signed by a member names no `via`. */
const deal = (v, ka, kb, via = null) =>
  `(record (keys (record (a ${ka}) (b ${kb}))) (pair (record (a #${v.X}) (b #${v.Y}))) (theta (record (price 9)))` +
  (via == null ? '' : ` (via (some #${via}))`) + ')';
const offerRow = (n) => `(record (n ${n}))`;

export const scenes = {
  market: {
    title: 'Market: two offers, one fuse',
    texts: { escrow: 'kernel:offerEscrow' },
    steps: [
      { who: 'alice', say: 'alice installs the escrow offer package. An offer holds its leg: what it gives moves into the book when the offer is posted, and leaves only with the row.', argv: (v) => ['install', v.text.escrow], bind: 'E' },
      { who: 'alice', say: 'alice creates a market object. It is a book: its offers stand as rows, each holding its leg.', argv: (v) => ['create', '--pkg', v.E, '(record)'], bind: 'X', open: 'X' },
      { who: 'bob', say: 'bob creates his own book. A deal needs two: each book takes what its peer\'s fuse judged.', argv: (v) => ['create', '--pkg', v.E, '(record)'], bind: 'Y', open: 'Y' },
      { who: 'alice', say: 'alice issues her coin, cap 100. Its well is her account in it.', argv: (v) => ['issue', '100'], bind: 'alpha' },
      { who: 'bob', say: 'bob issues his.', argv: (v) => ['issue', '100'], bind: 'beta' },
      { who: 'alice', say: 'the accounts the legs move between: each member\'s own, each book\'s, and the two a fuse pays into.', argv: (v) => ['account', v.alpha], bind: 'aA' },
      { who: 'alice', argv: (v) => ['account', v.alpha, '--owner', v.X], bind: 'xA' },
      { who: 'alice', argv: (v) => ['account', v.alpha, '--owner', v.bob], bind: 'bA' },
      { who: 'bob', argv: (v) => ['account', v.beta], bind: 'bB' },
      { who: 'bob', argv: (v) => ['account', v.beta, '--owner', v.Y], bind: 'yB' },
      { who: 'bob', argv: (v) => ['account', v.beta, '--owner', v.alice], bind: 'aB' },
      { who: 'alice', say: 'alice moves 20 out of her well into her account.', argv: (v) => ['transfer', `well:${v.alpha}`, `of:${v.alice}:${v.alpha}`, '20'] },
      { who: 'bob', argv: (v) => ['transfer', `well:${v.beta}`, `of:${v.bob}:${v.beta}`, '20'] },
      { who: 'alice', say: 'alice grants her book transfer 5 on her account: the deposit her offer spends. A grant over a balance lends at most its cap.', argv: (v) => ['grant', `of:${v.alice}:${v.alpha}`, v.X, 'transfer:5'], bind: 'gA' },
      { who: 'bob', say: 'bob grants his book transfer 9 on his.', argv: (v) => ['grant', `of:${v.bob}:${v.beta}`, v.Y, 'transfer:9'], bind: 'gB' },
      { who: 'alice', argv: (v) => ['read', v.X, '?'], method: { post: 'post', take: 'take', fuse: 'fuse' } },
      { who: 'alice', say: 'alice posts her offer: give 5 of her coin, ask 7 of bob\'s, price 5 to 10. The 5 leaves her account and stands in the book.', argv: (v) => ['invoke', v.X, v.post, post(v, 0, 'buyer', 5, 10, 5, v.alpha, v.gA, v.alice, 7, v.beta)] },
      { who: 'bob', say: 'bob posts the matching offer: give 7 of his coin, ask 5 of alice\'s, price 8 to 12. Price 9 is inside both boxes, and each gives what the other asks.', argv: (v) => ['invoke', v.Y, v.post, post(v, 0, 'seller', 8, 12, 7, v.beta, v.gB, v.bob, 5, v.alpha)] },
      { who: 'bob', say: 'bob posts a thin offer too: give 1, ask 5, the same box. Its box matches at 9. Its leg does not.', argv: (v) => ['invoke', v.Y, v.post, post(v, 1, 'seller', 8, 12, 1, v.beta, v.gB, v.bob, 5, v.alpha)] },
      { who: 'alice', say: 'the balances the legs stand on: alice holds 15 of her 20, her book 5; bob holds 12 of his 20, his book 8.', argv: (v) => ['read', v.aA], says: '15' },
      { who: 'alice', argv: (v) => ['read', v.xA], says: '5' },
      { who: 'bob', argv: (v) => ['read', v.bB], says: '12' },
      { who: 'bob', argv: (v) => ['read', v.yB], says: '8' },
      { who: 'alice', say: 'alice grants bob\'s book take on hers. A fuse sends its peer\'s take through this grant.', argv: (v) => ['grant', v.X, v.Y, `invoke:${v.take}`], bind: 'gX' },
      { who: 'alice', say: 'carol asks for the same invitation, and gets it. An invitation is not a take.', argv: (v) => ['grant', v.X, v.carol, `invoke:${v.take}`], bind: 'gC' },
      { who: 'carol', say: 'carol signs a take on the pair herself, pinning both offers. Refused (notFuser): a member\'s call has no caller, and a take answers only the book whose fuse judged the deal.', argv: (v) => ['invoke', v.X, v.take, deal(v, 0, 0), '--pin', 'offer', offerRow(0), '--pin', `${v.Y}/offer`, offerRow(0), '--via', v.gC], expect: 'refused', says: 'notFuser' },
      { who: 'bob', say: 'bob fuses naming the thin offer. The boxes agree at 9. The legs do not: alice asks 7, it gives 1. Refused (unfairLegs). Nothing moved.', argv: (v) => ['invoke', v.Y, v.fuse, deal(v, 0, 1, v.gX), '--pin', 'offer', offerRow(1), '--pin', `${v.X}/offer`, offerRow(0)], expect: 'refused', says: 'unfairLegs' },
      { who: 'bob', say: 'bob fuses the matching pair. One turn: his book judges, retracts its offer, pays its 7 to alice, and calls her book\'s take; hers judges, retracts, pays its 5 to bob. Both legs moved, or neither.', argv: (v) => ['invoke', v.Y, v.fuse, deal(v, 0, 0, v.gX), '--pin', 'offer', offerRow(0), '--pin', `${v.X}/offer`, offerRow(0)] },
      { who: 'alice', say: 'the balances after: alice\'s book 0, bob 5 of her coin; bob\'s book 1 (the thin offer\'s leg), alice 7 of his.', argv: (v) => ['read', v.xA], says: '0' },
      { who: 'bob', argv: (v) => ['read', v.bA], says: '5' },
      { who: 'bob', argv: (v) => ['read', v.yB], says: '1' },
      { who: 'alice', argv: (v) => ['read', v.aB], says: '7' },
    ],
  },
};
