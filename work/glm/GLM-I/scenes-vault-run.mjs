// scenes-vault-run.mjs — the Vault demo (scenes-vault.js) under node, on a fresh World, against the
// kernel the page loads. Every step answers as scripted (runDemo), and each `check` step must ALSO
// meet the kernel's menu (K.holds, tg_holds): the outcome, the refusal's own words, and — read at
// the end, as the page's account windows show them live — the balances and rows the journey's §HV
// rows assert. The scene never moves value after the deposit (two refusals and a read), so the end
// state is each check's state. Balances are read through tg_cell (Kernel.Value.ofCell) off the
// member's own follow, never asked of the writer. --harness-control adds an expectation nothing
// meets (GATES-15).
//   node scenes-vault-run.mjs [--harness-control]
import factory from './kernel.mjs';
import { loadKernel, client, genesis } from './nd.js';
import { demos, runDemo, outcomeOf } from './demos.js';
import './scenes-vault.js';

const control = process.argv.includes('--harness-control');
const dec = new TextDecoder();
const K = await loadKernel(factory);
const menu = K.holds();
// the control rewrites one expectation into one nothing can meet, so the reader's own comparison
// must refuse it (GATES-15): a reader that compares nothing passes it, and the gate calls that FAIL
if (control) menu.steps[0].expect = 'harness-control: an outcome no command ends with';

const g = genesis(K, 'testground', ['alice', 'bob']);
const nd = client(K, {});
const members = g.members.map((m) => ({ ...m, K, nd }));
const alice = members[0];
const entry = (name) => menu.steps.find((s) => s.step === name);
let bad = 0;
const fail = (why) => { bad++; console.log(`FAIL  ${why}`); };

if (!menu.rel || menu.steps.length < 3) fail('the kernel menu has no Vault (tg_holds: the journey moved)');
console.log(`menu   rel ${menu.rel} · grade ${menu.moves} · why "${entry('withdrawPastGrade')?.why}" / "${entry('depositUnpaid')?.why}"`);

const t = performance.now();
const r = await runDemo('vault', {
  fetchText: async (p) => dec.decode(K.text(p.slice(7)).slice(1)),
  members,
  run: async (m, a, s) => {
    const o = await nd.run(m, a);
    if (process.env.V) console.log(`  ${m.name}$ nd ${a.join(' ').slice(0, 90)} -> ${o.exit} ${(o.stderr ?? '').trim()}`);
    if (s.check) {
      const e = entry(s.check) ?? {};
      if (outcomeOf(o) !== (e.expect ?? `no menu entry for ${s.check}`)) fail(`${s.check}: got "${outcomeOf(o)}"  menu expects "${e.expect}"`);
      if (e.why && !(o.stdout + o.stderr).includes(e.why)) fail(`${s.check}: the refusal does not say "${e.why}"`);
    }
    return o;
  },
});
if (!r.ok) { bad++; console.log(`FAIL  the demo stopped at ${JSON.stringify(r.at?.argv ?? r.at?.say ?? r.at)}: ${r.r?.exit} ${r.r?.stderr ?? ''}`); }
const last = r.results.at(-1);

// the balances and rows, read as the page reads them (tg_cell; a read command), against the menu
const cell = (id) => Object.fromEntries(dec.decode(K.cell(alice.index, id).slice(1)).trim().split('\n').map((l) => { const i = l.indexOf(' '); return [l.slice(0, i), l.slice(i + 1)]; }));
const e = entry('deposit');
for (const [id, who] of [[r.v.acctV, 'vault'], [r.v.acctA, 'alice']]) {
  const c = cell(id);
  if (c.balance !== String(e[who])) fail(`${who}'s balance ${c.balance ?? '-'}, the journey's row says ${e[who]}`);
  else console.log(`      ${who.padEnd(5)} holds ${c.balance} (asset ${c.asset?.slice(0, 8)}…)`);
}
const rows = await nd.run(alice, ['read', r.v.V, menu.rel, '2']);
const ls = rows.stdout.trim().split('\n').filter(Boolean);
if (rows.exit === 'ok' && e.row0 === 'yes' && ls.length === 1 && e.row1 === 'no') console.log(`      row   ${ls[0]}`);
else fail(`the rows: ${rows.exit} "${rows.stdout.trim()}" (the journey's row says row 0 present, row 1 never written)`);

const ok = !bad && r.ok && last?.exit === 'ok';
console.log(bad || !r.ok ? `TESTGROUND VAULT RED: ${bad} check(s)` : `TESTGROUND VAULT GREEN: 3 checks, ${((performance.now() - t) / 1000).toFixed(1)} s`);
process.exit(ok ? 0 : 1);
