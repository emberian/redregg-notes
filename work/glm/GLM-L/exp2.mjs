import factory from "/tmp/glm-l-exp/kernel.mjs";
import { loadKernel, client, genesis, rand32 } from "/home/hbox/nd-land/glm-l/testground/nd.js";
const K = await loadKernel(factory);
const nd = client(K);
const g = genesis(K, "exp", ["alice", "bob"]);
const alice = g.members[0];
const run = async (m, argv) => { const r = await nd.run(m, argv); console.log(`\n$ nd ${argv.join(" ")}\n exit=${r.exit}\n${(r.stdout + r.stderr).trim()}`); return r; };
const cell = (id) => { const r = K.cell(alice.index, id); console.log("tg_cell:", new TextDecoder().decode(r.slice(1)).trim()); };
const r0 = await nd.run(alice, ["create"]); const id = (r0.stdout.match(/^id (\S+)/m) || [])[1];
await run(alice, ["write", id, "0", "before"]);
console.log("member cell BEFORE:"); cell(alice.id);
await run(alice, ["rotate"]);
console.log("member cell AFTER rotate:"); cell(alice.id);
// the thief: the old key attempts a rotate (the JROT row's thief line)
const th = await nd.forge(alice, ["rotate"]); console.log("thief rotate:", th.exit, (th.stdout + th.stderr).trim());
// roll: current := next, next := pending, pending := fresh
const s = alice.custody.seeds; s.splice(0, 3, s[1], s[2], rand32());
await run(alice, ["write", id, "0", "new key after rotate"]);
console.log("member cell AFTER roll+write:"); cell(alice.id);
await run(alice, ["rotate"]);
s.splice(0, 3, s[1], s[2], rand32());
await run(alice, ["write", id, "0", "second rotation works"]);
