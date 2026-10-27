// scenes-rotate-run.mjs — the key-rotation scene under node, against the page's kernel (gate.sh).
// alice rotates; a copy of the old key writes and rotates (refused by name); custody advances on the
// settlement and the new key writes; the member cell's key slots are read before and after (`tg_cell`).
// --harness-control inverts the thief-write expectation: this harness must then FAIL (gate.sh checks).
import factory from './kernel.mjs';
import { loadKernel, client, genesis } from './nd.js';
import { runRotateScene, rotateScene, memberCell, forgeOn } from './scenes-rotate.js';

const K = await loadKernel(factory);
const nd = client(K);
const g = genesis(K, 'testground', ['alice', 'bob']);
const control = process.argv.includes('--harness-control');
const r = await runRotateScene(rotateScene, {
  members: g.members,
  control,
  say: (t) => t && console.log(t.replace(/^/m, '  ')),
  run: (m, argv) => nd.run(m, argv),
  forge: forgeOn(K),
  cell: (m) => memberCell(K, m),
});
if (!r.ok) console.log(`ROTATE SCENE ${control ? 'read red (the control\'s inverted expectation, as it must)' : 'STOPPED'}: ${r.why} at ${JSON.stringify(r.at)}`);
else console.log('ROTATE SCENE OK');
process.exit(r.ok ? 0 : 1);
