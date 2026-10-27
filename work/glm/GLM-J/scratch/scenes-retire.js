// scenes-retire.js — the retirement scene (KERNEL-70, journey §RT in Lang/Journey/Retire.lean): an
// owner ends an object with `retire CELL`. The board is the rows' own one-slot package
// (`Protocol.slot`, the text `kernel:slot`): `post` (method 1) inserts a row, `clear` (method 0)
// retracts it. The steps follow the journey's RT rows as a member reaches them: RT1 a member that
// does not own the object is refused `notOwner` before its key signs; RT5 a parent holding a row is
// not retired (`rowsRemain`); RT7 the empty object retires, its id stays a tombstone and the
// storage it held returns to the World (the allowance line beside each command); after it every
// read under the id names the missing cell (RT9 and RT10 are turns no receiver derives, so the
// member's own refusals are `missingCell`). `retireChecks` is what the gate measures: the inspector
// reads the tombstone, and a retirement gives an entry's weight back to the allowance.

/** The demo `retire`, registered by demos.js's one line. */
export const scenes = {
  retire: {
    title: 'Retire: an owner ends an object',
    texts: { board: 'kernel:slot' },
    steps: [
      { who: 'alice', say: 'alice installs a one-slot board: an object whose package holds one relation, posts, with one row in it.',
        argv: (v) => ['install', v.text.board], bind: 'pkg' },
      { who: 'alice', say: 'alice creates the board. She owns it.',
        argv: (v) => ['create', '--pkg', v.pkg, '(record)'], bind: 'obj', open: 'obj' },
      { who: 'alice', say: 'alice grants everyone the right to post into it.',
        argv: (v) => ['grant', v.obj, 'anyone', 'invoke:1'], bind: 'pub' },
      { who: 'bob', say: 'bob does not own the board. His retirement is refused (notOwner). Nothing is signed.',
        argv: (v) => ['retire', v.obj], expect: 'refused', refusal: 'notOwner' },
      { who: 'alice', say: 'alice posts one row. The relation holds it.',
        argv: (v) => ['invoke', v.obj, '1', '(record (k 1) (text "first"))'] },
      { who: 'alice', say: 'alice retires the board while the row stands. The writer declines the call (rowsRemain): a parent holding a row is not retired.',
        argv: (v) => ['retire', v.obj], expect: 'declined', says: 'rowsRemain' },
      { who: 'alice', say: 'alice clears the row. The relation is empty.',
        argv: (v) => ['invoke', v.obj, '0', '(record (k 1))'] },
      { who: 'alice', say: 'alice retires the empty board. The id stays as a tombstone (a retired cell). The storage it held returns to the World: the allowance line beside each command rises.',
        argv: (v) => ['retire', v.obj] },
      { who: 'bob', say: 'bob reads the relation under the retired board. Refused (missingCell): the id names a tombstone, and no row is read under it.',
        argv: (v) => ['read', v.obj, 'posts', '8'], expect: 'refused', refusal: 'missingCell' },
      { who: 'bob', say: 'bob posts through the grant. The grant died with the object (every grant over a retired object is dead); the plan reads the object first and refuses (missingCell).',
        argv: (v) => ['invoke', v.obj, '1', '(record (k 2) (text "second"))', '--via', v.pub], expect: 'refused', refusal: 'missingCell' },
      { who: 'alice', say: 'The inspector reads the tombstone. Click the board\'s id in any line above: the object window shows kind retired.',
        argv: (v) => ['read', v.obj, '?'], expect: 'refused', refusal: 'missingCell' },
    ],
  },
};

/**
 * What the gate measures after the demo (axes-run.mjs): the inspector's own read of the retired
 * board (`tg_cell`: `kind retired`), and the storage credit a retirement returns. A fresh cell is
 * written full, the allowance is read, the cell is retired, the allowance is read again: the
 * difference is the weight the retirement gave back (RT2's `weight back`, less the call's charge).
 * `members` are the demo's (each carries its kernel and client); `v` holds the demo's bindings.
 */
export async function retireChecks(members, v) {
  const dec = new TextDecoder();
  const alice = members[0];
  const K = alice.K;
  const allowanceOf = (m) => +Object.fromEntries(dec.decode(K.meter(m.index).slice(1)).trim().split('\n').map((l) => l.split(' '))).allowance;
  const tomb = dec.decode(K.cell(alice.index, v.obj).slice(1));
  const made = await alice.nd.run(alice, ['create']);
  const cell = (made.stdout.match(/^id ([0-9a-f]{64})/m) || [])[1];
  const fill = [];
  for (let s = 0; s < 12; s++) fill.push(await alice.nd.run(alice, ['write', cell, `${s}`, `storage held by slot ${s} of a cell soon retired`]));
  const before = allowanceOf(alice);
  const gone = await alice.nd.run(alice, ['retire', cell]);
  const after = allowanceOf(alice);
  const reads = (await alice.nd.run(alice, ['read', cell])).exit;
  return {
    tombstone: tomb.trim() === 'kind retired',
    retired: gone.exit === 'ok' && fill.every((r) => r.exit === 'ok'),
    unreadable: reads === 'refused',
    before, after,
    back: after - before,
  };
}
