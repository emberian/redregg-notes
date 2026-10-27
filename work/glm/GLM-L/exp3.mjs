import factory from "/tmp/glm-l-exp/kernel.mjs";
import { loadKernel, client, genesis } from "/home/hbox/nd-land/glm-l/testground/nd.js";
const K = await loadKernel(factory);
const nd = client(K);
const g = genesis(K, "exp", ["alice", "bob"]);
const alice = g.members[0];
const run = async (m, argv) => { const r = await nd.run(m, argv); console.log(`$ nd ${argv.join(" ")} -> ${r.exit} :: ${(r.stdout + r.stderr).trim().split("\n").join(" | ")}`); return r; };
const r0 = await nd.run(alice, ["create"]); const O = (r0.stdout.match(/^id (\S+)/m) || [])[1];
await run(alice, ["write", O, "0", "first"]);
await run(alice, ["rotate"]);
await run(alice, ["write", O, "1", "old"]);       // expect refused unknownKey
await run(alice, ["read", O]);                     // does a read with the old wallet key work?
await run(alice, ["read", O, "?"]);
// thief forged WRITE with the old seed, post-rotate:
const enc = new TextEncoder();
const old = alice.custody.seeds.slice();           // snapshot the whole wallet
const C = (await import("/home/hbox/nd-land/glm-l/testground/nd.js")).codec(K.table);
const N = (await import("/home/hbox/nd-land/glm-l/testground/nd.js")).names(K.table);
const cmd = (argv) => C.write(K.table.command, { argv: argv.map((a) => enc.encode(a)) }, K.table.bounds.argvBytesMax);
const forged = K.forge(alice.index, cmd(["write", O, "2", "thief"]), old[0], old[1]);
console.log("forge write:", forged[0] === 0 ? "planned" : "refused " + new TextDecoder().decode(forged.slice(1)));
if (forged[0] === 0) {
  const reply = K.host(N.op.submit, forged.slice(1));
  console.log("writer:", N.statusName[reply[0]], new TextDecoder().decode(reply.slice(1)));
}
