// scenes-rotate.js — a member's key rotation, one scene and one demo (GLM-L, CLIENT-54). The rows it
// reads: the `rotate` row (Protocol/Rows.lean, JROT/JROTL: a stolen key cannot rotate — `notPrecommitted`;
// a lost reply is found by lookup; a rotation that never reached the writer ends `open`) and the kernel
// sim's rotate lines (Kernel/Sim/Gen.lean: `thief-rotate` refused `notPrecommitted`, `rotate` ok,
// `rotate-stales` stale; KERNEL-60 `rotate_stales_outstanding`). Lang/Journey has no rotate rows: the
// journeys fix founders' next-key digests at genesis and never rotate.
//
// The page's demo (`demos.rotate`, merged by one line in demos.js) is the subset a plain runner drives:
// alice rotates, and the tab's wallet — which still holds the old key — has its next call refused by
// name. The full scene (below) adds what a runner must do for the member: a thief's forged calls with
// the saved old key, and custody's advance on the settlement (in nd, `client/src/run.rs`, the advance is
// part of the rotate command; the tab's wallet in nd.js does not advance — the cv card in the report).

import { codec, names, rand32 } from './nd.js';

const enc = new TextEncoder(), dec = new TextDecoder();
const hex = (b) => Array.from(b, (x) => x.toString(16).padStart(2, '0')).join('');

/** The member cell's slots as `tg_cell` prints them: `{ kind, key, next, sponsor }`. */
export function memberCell(K, m) {
  const t = dec.decode(K.cell(m.index, m.id).slice(1)).trim();
  return Object.fromEntries(t.split('\n').map((l) => { const i = l.indexOf(' '); return [l.slice(0, i), l.slice(i + 1)]; }));
}

/** Custody's advance on a committed rotate (run.rs `Custody::settle` → `Keys::advance`):
 *  current := next, next := pending, pending := fresh. The member cell already holds the first two. */
export function advance(m) {
  m.custody.seeds.splice(0, 3, m.custody.seeds[1], m.custody.seeds[2], rand32());
}

/** The demo a plain runner (the page's Demos window, demo-run.mjs) drives. Its last `read` works: a
 *  read envelope does not name the member's key, only a call does, so the old wallet still reads. */
export const rotateDemo = {
  title: 'Rotate your key',
  steps: [
    { who: 'alice', say: 'alice creates a cell and writes slot 0. Her current key signs the call. The object window names the owner: her member id.', argv: () => ['create'], bind: 'O', open: 'O' },
    { who: 'alice', argv: (v) => ['write', v.O, '0', 'first key'] },
    { who: 'alice', say: 'alice rotates. The NEXT key signs the rotate, and precommits the key after it. The member cell takes the new key.', argv: () => ['rotate'] },
    { who: 'alice', say: 'The wallet in this tab still holds the old key. Its call names a key the member no longer holds: refused (unknownKey). In nd the wallet advances inside the rotate command.', argv: (v) => ['write', v.O, '1', 'old key'], expect: 'refused', refusal: 'unknownKey' },
    { who: 'alice', say: 'The cell still reads. The member cell holds the new key and the digest of the next one; click the owner id to read it.', argv: (v) => ['read', v.O, '?'] },
  ],
};

/** The full scene: every beat the rows spell, plus the member cell's key slots read before and after.
 *  Step kinds a plain runner knows: `{ who, argv, bind, expect, refusal }`. This scene's own kinds:
 *  `{ cell: 'before' | 'after' }` (assert the member cell's key), `{ thief: 'write' | 'rotate' }`
 *  (a forged call signed with the saved old key), `{ advance: true }` (custody takes the new key). */
export const rotateScene = {
  title: 'Rotate your key',
  steps: [
    { who: 'alice', say: 'alice creates a cell and writes slot 0. Her current key signs the call.', argv: () => ['create'], bind: 'O' },
    { cell: 'before', say: 'Her member cell holds the signing key and the digest of the next one. The next key is precommitted: only its holder can rotate.' },
    { who: 'alice', say: 'alice rotates. The NEXT key signs the rotate, and precommits the key after it.', argv: () => ['rotate'] },
    { cell: 'after', say: 'The member cell holds the new key. The old key is no longer the member\'s.' },
    { thief: 'write', say: 'A copy of the old key writes. The call names a key the member no longer holds: refused (unknownKey).', expect: 'refused', refusal: 'unknownKey' },
    { thief: 'rotate', say: 'The copy tries to rotate to itself. A rotate must be signed by the precommitted next key: refused (notPrecommitted). This is the rotate row\'s thief line.', expect: 'refused', refusal: 'notPrecommitted' },
    { advance: true, say: 'Custody advances on the rotation\'s settlement: the wallet takes the new key and mints the key after next. In nd this is part of the rotate command.' },
    { who: 'alice', say: 'The new key signs. Admitted.', argv: (v) => ['write', v.O, '1', 'new key'] },
  ],
};

/** The tour entry for this scene, for the Tour's array (testground.js): `{ ...tourStep }` appended as
 *  one line runs the demo and advances on its result, like the meter and time-lock steps. */
export const tourStep = { say: 'Your key: a rotate is signed by the NEXT key, precommitted when you joined. The old key\'s next call is refused (unknownKey); a copy of it cannot rotate (notPrecommitted).', demo: 'rotate' };

/** Run the full scene. `deps`: `members` (the genesis members; alice's custody is read, never
 *  replaced), `run(m, argv)` (a command), `forge(m, argv, seed, nextSeed)` (a call planned without
 *  the follow's admission and signed with `seed`), `cell(m)` (the member cell's slots), and `say(text)`
 *  (optional, the lesson lines). `control: true` inverts the thief-write expectation, so a harness
 *  that cannot fail is caught. */
export async function runRotateScene(scene, { members, run, forge, cell, say = () => {}, control = false }) {
  const alice = members.find((m) => m.name === 'alice');
  if (!alice) return { ok: false, why: 'no alice' };
  const v = {};
  const wallet = alice.custody.seeds.slice();          // before anything: current, next, pending
  const keys = { before: hex(alice.custody.pub(0)), after: hex(alice.custody.pub(1)) };
  let nextBefore = null, sponsor = null;
  const outcome = (step, r) => {
    const want = control && step.thief === 'write' ? 'ok' : (step.expect ?? 'ok');
    if (r.exit !== want) return `ended ${r.exit}, wanted ${want}`;
    if (step.refusal && !(r.stderr || '').split('\n').some((l) => l.startsWith(`refused ${step.refusal}`)))
      return `did not refuse ${step.refusal}: ${(r.stderr || '').trim()}`;
    return null;
  };
  for (const s of scene.steps) {
    say(s.say);
    if (s.cell) {
      const c = cell(alice);
      if (c.kind !== 'member') return { ok: false, why: `the member cell reads ${c.kind}`, at: s };
      if (c.key !== keys[s.cell]) return { ok: false, why: `the member cell's key is ${c.key}, wanted ${keys[s.cell]}`, at: s };
      if (s.cell === 'before') { nextBefore = c.next; sponsor = c.sponsor; continue; }
      if (c.next === nextBefore) return { ok: false, why: 'the member cell\'s next did not move', at: s };
      if (c.sponsor !== sponsor) return { ok: false, why: 'the member cell\'s sponsor moved', at: s };
      continue;
    }
    if (s.thief) {
      const r = forge(alice, s.thief === 'write' ? ['write', v.O, '2', 'the old key'] : ['rotate'], wallet[0], wallet[1]);
      const bad = outcome(s, r); if (bad) return { ok: false, why: bad, at: s };
      continue;
    }
    if (s.advance) { advance(alice); continue; }
    const r = await run(alice, s.argv(v));
    if (s.bind) { const id = (r.stdout.match(/^id ([0-9a-f]{64})/m) || [])[1]; if (!id) return { ok: false, why: 'no id printed', at: s }; v[s.bind] = id; }
    const bad = outcome(s, r); if (bad) return { ok: false, why: bad, at: s };
  }
  return { ok: true };
}

/** A `forge` for `runRotateScene` over the tab's kernel: the command frame, planned without the
 *  follow's admission, signed with the given seed, sent once (nd.js `client.forge` with the seed
 *  named instead of the wallet's current one). */
export function forgeOn(K) {
  const C = codec(K.table), N = names(K.table);
  return (m, argv, seed, next) => {
    const frame = C.write(K.table.command, { argv: argv.map((a) => enc.encode(a)) }, K.table.bounds.argvBytesMax);
    const r = K.forge(m.index, frame, seed, next);
    if (r[0] !== N.status.ok) return { exit: 'refused', stderr: `refused ${dec.decode(r.slice(1))}\n` };
    const h = K.host(N.op.submit, r.slice(1));
    const said = N.statusName[h[0]];
    return { exit: said === 'ok' ? 'ok' : said, stderr: said === 'ok' ? '' : `${said} ${dec.decode(h.slice(1))}\n` };
  };
}
