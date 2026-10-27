# DESIGN-TESTGROUND — a nanodregg World you can live in, in a browser tab (real 2026-10-26)

Ember's ask, verbatim: "i'd like to ship (on github pages?) the 'nanodregg testground' that is like a
early 00s style net OS that exposes and allows introspecting, editing, all actions etc in a visual way
so that people can 'learn the system from immersion' and we can have the demos and whatever in there."

**Verdict, measured: (A) — the kernel in the browser — is feasible NOW, not a later phase.** The
writer's deployed loop and each member's `host follow` decision, at the deployed parameters, compile
to one 3.5 MB WebAssembly module (0.66 MB gzipped) that a static page loads in ~70 ms; a write is
admitted in 10–14 ms in Chromium, the whole document demo (14 `nd` commands, three packages
installed, a revoke, a refusal by name) runs in 3.7–4.5 s; the wasm build answers 368 recorded kernel
calls **byte for byte** as a native build of the same C does, at native speed (the shipped `-Os` module: 0.95–1.07× native over three paired runs; `-O2`: 1.17–1.23×). (B) — a hosted
World — becomes the same page with ONE function swapped: the writer's frames go over a WebSocket to a
real `host serve`, while the visitor's own follow stays in the tab and re-derives every step. Both,
in that order. A prototype runs today (§2).

Labels: MEASURED = run here on 10-26 (Chromium 1234 via Playwright and node 26 on an M2 Max; hbox for
the Lean half); READ = read in the code at origin/main f193a3e; INFERRED = my reasoning, not run.

---

## 1. The measurement

### 1.1 What compiled (MEASURED)

| piece | what | result |
|---|---|---|
| the closure | `Web.Sim.Testground` (the prototype's one Lean module) imports `Protocol.Rows.Writer`, `Protocol.Rows.Deployed`, `Host.Follow`, `Host.Cli` | 105 tree modules + 590 `Init` + 59 `Std` modules; **zero** `Lean` (elaborator) modules |
| tree C | `lake build Web.Sim.Testground:c` in `wt/testground` | the tree's own IR C, as `lake` emits it for `host` |
| toolchain C | `lean -Dbackward.do.legacy=false -R src/lean -c` over the toolchain's own sources, per module | 649/649; without the flag the core build uses, `Init.Data.Iterators.Lemmas.Combinators.FlatMap` does not elaborate ("definition not exposed") |
| one divergence | `Init.Data.String.PosRaw`: the official IR names `String.instDecidableLtRaw._aux_1`, which importers inline (from the official .olean) and a standalone re-emit does not produce | the only undefined symbol at link; stage0's `PosRaw.c` at v4.30.0 is ours plus exactly that definition (export sets and import lists diffed equal otherwise) and is used. Every other symbol we define is in the toolchain's `libInit.a`/`libStd.a` (`nm`, 27,472 symbols, 0 extra) |
| the runtime | lean4 `src/runtime` at v4.30.0, em++ (emscripten 6.0.9) `-std=c++20 -DLEAN_EMSCRIPTEN`, **single-threaded**, no GMP, no mimalloc | builds after 4 patches to bit-rotted no-thread/no-libuv stubs (`unique_lock` lacks `adopt_lock`/`release`; three `uv` stubs disagree with their headers). Upstream builds this branch only with `-pthread`. |
| the C FFI | `Host/c/file.c` (the only C the closure names) | compiles with emcc unchanged |
| link | `-fwasm-exceptions`, `-sERROR_ON_UNDEFINED_SYMBOLS=1`, 8 MB stack, memory growth, ES module for web and node | links; two signature-mismatch warnings (`nd_ignore_sigxfsz`, `lean_io_create_tempfile`: Lean calls with no argument, C takes the world token) — not on any path the page drives; they would trap if called |

Why single-threaded: a `-pthread` module needs `SharedArrayBuffer`, which needs COOP/COEP response
headers, which GitHub Pages cannot send. The path the page drives never spawns a Task: the writer's
checkpoint is the in-memory one (`Host.Sim.memCheckpoint`, `async := false`, READ), and follow is a
pure function per frame.

### 1.2 Size (MEASURED)

| build | raw | gzip -9 | brotli -11 |
|---|---|---|---|
| `-O2` | 3,613,192 B | 663,543 B | 448,708 B |
| `-Os` (shipped) | 3,455,643 B | 661,552 B | — |

The size is the Lean code: 649 toolchain modules' C are in because `initialize_Init` names every
`Init` module (an import of `Init` is all of it). The JS glue is 60 KB.

### 1.3 Speed (MEASURED, Chromium, M2 Max; node agrees within ~20%)

| act | in the tab | frames |
|---|---|---|
| fetch + compile + `initialize` the kernel | 65–84 ms (desktop drawn at 270 ms) | — |
| genesis (two founders, a Store as `memGenesis` leaves it) | 10–19 ms | — |
| `create` (the first command: sign envelope → log page → absorb → plan → sign → submit → confirm) | 32–46 ms | 11 |
| `write OBJ 0 …` (an ordinary write, admitted) | 10–14 ms; 7.0–9.8 ms mean over 20 | 11 |
| `read OBJ ?` (describe) | 3–4 ms | 4 |
| `grant` | 11–14 ms | 11 |
| the race: bob's write declined `stale` after alice's moved his pin | 23–27 ms | 18 |
| `install` the Bell package (74 KB text) | 143–154 ms; again: `refused idTaken` in 43 ms | 11 |
| `install` the document's four packages | 78–335 ms each | 11 |
| `invoke` a document method (post, propose, select, rejudge) | 430–690 ms each | 15–18 |
| the whole document demo (14 commands) | 3.7–4.5 s | 208 |

**Differential (MEASURED).** `record.mjs` ran the document demo and 21 writes through the wasm
kernel and recorded every kernel call with its reply (368 calls, 6.1 MB); `replay.c`, built natively
(leanc, the toolchain's own `libInit`/`libStd`/`libleanrt`) and to wasm from the same generated C,
replayed them: **0 mismatches** both ways. Kernel time, first pair: native 3,033 ms, wasm 3,556–3,738 ms
(**1.17–1.23×**) for the `-O2` module; the shipped `-Os` module, three paired runs on the same trace: wasm 2,324–2,616 ms against native 2,202–2,421 ms (**0.95–1.07×**: indistinguishable on a laptop). Of the native time, follow is 2,700 ms and the writer 333 ms: a member's own
re-derivation and planning is the cost, and an `invoke` costs ~0.5 s natively too (INFERRED: the
package closure is loaded and re-checked per invoke, `Invoked.pkgs`; THE BAR's WASTE lines are where
that belongs, not here).

### 1.4 What did not compile, and why

Nothing in the closure failed. What a builder must know is in `testground/build/build.sh`'s header:
the core-build flag, the PosRaw override, the runtime patches, no threads. The deployed resident
(`host serve` over files, `Host.Sock`, the stdio pump's Task) is NOT in the module and need not be.

---

## 2. The prototype (LANDED: nanodregg `36c4ea5f`, FAST judge green; files in codex/TESTGROUND.report.md)

`Web/Sim/Testground.lean` (one module, tooling by its `Sim` component: it is the rows' system in a
tab, and no deployed module imports it) exports six functions over bytes:

* `tg_genesis` — `Receive.genesis` at the deployed `Ctx`, a Store as `Host.Sim.memGenesis` leaves it,
  one follow per founder; answers `host genesis`'s lines (`Host.Cli.genesisLines`).
* `tg_host OP PAYLOAD` — one frame through **`Host.serve`, the deployed loop** (group commit, seal
  cadence, whole-World bases, the pager) over the in-memory disk, with a port that holds the one frame
  and ends at `eof`: the writer the rows use (`Protocol.Rows.Writer.machine/checkpoint/pager`), no plant.
* `tg_follow I OP PAYLOAD` — `Host.Follow.answer`, the deployed per-frame decision of `host follow`.
* `tg_pub`, `tg_sign` — CODEC's Ed25519 for the page's custody (follow never sees a seed).
* `tg_attempt` — `Protocol.Attempt.next`, the attempt store's decision.
* `tg_table` — the protocol table as JSON, read off `Protocol.Table`'s `all` lists (ops, statuses,
  step tags with layouts, the follow socket's layouts, custody refusals, command exits, the attempt
  store's words, bounds).

`testground/nd.js` (~230 lines) is `client/src/run.rs`'s part and nothing more: a reader and writer
for any `Codec.Layout` the table carries, custody (current/next/pending seeds held by the page), the
step loop (`sign`/`precommit`/`signNext`/`signIncoming`/`host`/`submit`/`done`), and the attempt
loop with every decision asked of `tg_attempt`. It contains no op code, status byte, step tag,
layout, bound or refusal name: the wire moving 7→8→9 and `Req` gaining `caller` change nothing in
it (INFERRED from the code; it has no constant to change).

What a visitor sees (MEASURED, screenshots in `promo/testground-*.png`): a blue desktop with icons
(World, alice, bob, Wire, Start here, Demos) and a taskbar. "World — testground" shows the genesis
lines (origin, nonce, each founder's member and grant, chain) and a **Re-genesis** button. Each member
has a terminal (`alice$ nd …`) whose output is follow's own text, every id a link. The tour's five
steps: alice creates an object, writes it, describes it, grants bob mutate; bob writes through the
grant while alice's write lands first — and a dialog titled **Declined** says, in the kernel's words,
**`declined stale`**, that the writer's last word was `submit → declined stale`, and why. Clicking
an id opens the object as a window laid out from `read OBJ ?` (object, owner, package, the core's
size, each method with an `invoke…` link that pre-fills the terminal, its laws and relations) and
`read OBJ`. The Wire window lists every frame (who → writer/follow, op, status, bytes) with a scrub
bar. **Demos ▸ The document** types the 14 commands of `client/tests/doc.rs` into the two terminals
with a narrator line each: the section opens as a window with methods 0–10, the candidate reads
`verified`, then after the revoke `suspended "support0 dead"`, and selecting it again raises a
**Refused** dialog: `refused program` / `hint program: select: refused support0 dead` / "the writer
said nothing — your own follow re-derived the call on its own World, refused it, and never asked
custody to sign."

---

## 3. The architecture: both, (A) first

### 3.1 (A) the World in the tab

```
 page (JS: pixels + nd's part)            kernel.wasm (Lean, one module)
 ───────────────────────────────          ─────────────────────────────────────────────
 terminal argv ──command frame──────────▶ tg_follow i  = Host.Follow.answer (member i)
 step loop: sign ◀── step bytes ─────────  (plans, re-derives, renders, refuses by name)
   custody: seeds in the tab ─tg_sign──▶  CODEC Ed25519
   host step ──frame─────────────────────▶ tg_host = Host.serve over the in-memory Store
   submit ─▶ attempt loop ─tg_attempt──▶  Protocol.Attempt.next
 windows ◀── follow's stdout lines
```

The Store is bytes (`Host.Sim.Disk`/`Bases`). Persisting them and the seeds in IndexedDB makes
**reloading the tab a crash recovery through the real `Host.openWith`** (sequence item 5).

### 3.2 (B) a hosted World: the same page, `tg_host` replaced by a socket

```
 page: nd.js + kernel.wasm (follow stays HERE) ──ws: (conn, op, payload)──▶ relay ──▶ host serve (hbox)
```

* **The relay moves bytes only**: it is the supervisor's mux (`client/src/mux.rs`: `(conn, op,
  payload)` frames, parses no payload) with a WebSocket on one side. It may refuse ops by code from
  the table (only `Op.relayable` + `submit`, never `command`/`resume`, which belong to a member's own
  follow) and rate-limit connections; it decides nothing about a call.
* **The visitor is a thin member, not a viewer.** Its follow runs in the tab and re-derives every
  logged step before it signs anything (`absorbStep`, PROTOCOL-4); a lying writer is refused by name
  in the visitor's own tab (`chainMismatch`, `eventMismatch`, `forkedPost`).
* **Where its first World comes from** (the trust model): it joins over an invitation
  (`Invite.accept`, PROTOCOL-42) signed by a sponsor key the page carries, or adopts a pinned base
  (thin consent, PROTOCOL-14). The page is then the out-of-band channel, and that is the weak spot:
  whoever publishes the page chooses both the kernel and the sponsor key (§7). Once the Store signing
  seed lands (TRUST T3; Ember said yes 10-26), a visitor checks the writer's certified head instead of
  one member's attestation.
* **Enrollment and abuse**: a guest-book resident holds a World grant `enroll:N` and enrolls each
  visitor's join token; abuse control is the kernel's own: per-member refusal budgets and the meter
  (KERNEL-68, `ticksBudget`) — the demo of the meter IS the rate limit.
* **The model** (the inbox demo) runs only in (B): the provider key stays in `keybroker` on hbox; a
  tab never holds it.

(B) costs one function and a relay because the follow is already in the tab. A pure thin client with
no wasm would need the decisions over the wire — the follow on a server — which makes the visitor a
viewer of someone else's re-execution; I recommend against it.

### 3.3 The law-1 / law-2 boundary

| the page IS | the page is NOT |
|---|---|
| framing: a reader/writer for the layouts the table names (the Cursor primitives `generated.rs` hand-writes too) | a parser of argv (follow's `Verb.parse`), a planner, an encoder of a request |
| custody: seeds, and asking CODEC's Ed25519 to sign the bytes it is handed | a chooser of what to sign (follow asks; `planMoved` re-derives) |
| the attempt loop, asking `Attempt.next` at every turn | a classifier of verdicts (a status byte names `Seen`, by the table) |
| windows laid out by a line's first word | a renderer of meaning: every word shown is follow's stdout or a table name |

**The table is read at run time from the kernel the page talks to** (`tg_table`), not emitted into a
TS file: the page cannot hold a table older than its kernel, which is a stronger form of law 1 than
`generated.rs`, whose staleness a gate has to catch. So "extend Emit/ to emit TS" becomes: move the
one JSON renderer into `Emit/` beside `Emit.Rust` (CODEC's, a one-hour move) so both projections of
`Protocol.Table` live together; no TS file exists.

One hand-written table remains and is named: the refusal **glossary** in `testground.js` (a sentence
per refusal name for visitors). It cannot mislabel a refusal (the name shown is always follow's) but
it can go silent on a rename. Its right home is the constructors' own docstrings, emitted with the
table (sequence item 7).

---

## 4. The UI as a net OS

| nanodregg | on the desktop | state |
|---|---|---|
| a World | a desktop; its genesis lines are "World properties"; **Re-genesis** = a new desktop | built |
| a member | a user: a terminal titled `alice@testground — nd`, its keys in the tab | built |
| an object | a window opened by clicking its id: `read OBJ ?` as a property sheet, methods with `invoke…` | built |
| a grant | a permission: the grant id in the terminal opens the grant cell as a window (target, grantee, issuer, rights) | design (needs a `read` of a grant cell) |
| a refusal | a modal dialog titled Refused / Declined whose heading is the refusal's NAME, the writer's last word, and one sentence | built |
| the log | the Wire window: every frame, scrubbable; (next) the writer's steps with the World's roots at each, scrubbing re-folds `World.fold` to that step | frames built; steps design |
| a hole | a field in the object window showing each candidate's status; on revoke it turns from `verified` to `suspended "support0 dead"` live, because every window re-reads after every command | status shown in the terminal's `read OBJ candidates`; the field design |
| a receipt | a thing you hold: `nd receipt CALL` prints the receipt, the head it was checked against and the verdict; a "Receipts" folder keeps them and re-checks any against the current head | design |
| a lying writer | the Writer menu: honest ▾ / hides the tail / forges a refusal / forgets spent / lies about its base — the rows' own plants (`Rows.Writer.Params`), so the visitor watches their own follow refuse by name | design (item 2) |

## 5. The demos it ships with (one per axis)

Each demo is the argv a member types — the rows and client tests already are these sequences.

| axis | demo | source of the sequence | (A) now? |
|---|---|---|---|
| CTX | the document repairs across a revoked contributor | `client/tests/doc.rs`, DC rows | **built** |
| LEDGER | escrow: offer, accept, settle; an over-draw refused by a floor | LE/LF rows, `world/escrow` | yes (argv only) |
| AGENT | the inbox: ring the Bell, a model answers into the document | HOSTING-53 | (B) only (the key stays on hbox); (A) with a scripted answerer, labelled |
| META | a generator installs a package; a write past the generated law refused | GN rows | yes |
| OBS | a time-lock on a foreign clock | TL rows | after "two Worlds in a tab" (item 4) |
| TRUST | a fork detected: two members' heads compared, `forkedWorld` by name | PROTOCOL-74/75 rows | after item 4 (two writers from one genesis), and in (B) across two tabs |
| PCC | a claim refused at install (`claimUnproved`) | L2 rows | after PCC L2 lands (wire 9); a rebuild |
| TYPES | graded effects refuse an over-move | LANG-89 rows | after it lands (wire 8); a rebuild |
| OBS | the meter: invoke until `ticksBudget` | KERNEL-68 | yes (d280d23 is in the module) |
| base | two members race one slot: `declined stale` | the tour's step 5 | **built** |

## 6. The first five minutes

1. (0:00) The desktop draws in under half a second; "Start here" says: two members, one World, all in this tab.
2. (0:30) Run the tour: create, write, describe — the object opens as a window with its owner a member link.
3. (1:30) Grant bob; bob writes through it; alice's write lands first; a **Declined: `declined stale`** dialog. The visitor has met pins and optimistic concurrency without the words.
4. (2:30) Free play: write as bob without `--via` (`refused noGrant`), install a package twice (`refused idTaken`), press Re-genesis.
5. (3:30) Demos ▸ The document: watch a section select bob's text, then suspend it by name when his grant is revoked, and refuse to select it again **before anything leaves the tab**.
6. (later) Switch the writer to "forges a refusal" and watch your own follow refuse the log by name: the moment the system's point lands.

## 7. Re-emits, price, and the one way it is wrong

**What re-emits.** `testground/kernel.{mjs,wasm}` on every change to the 105-module closure (every
flag day today: wire 7→8→9, `Req.caller`): run `build.sh c` on hbox and `build.sh wasm` with emcc
(~5 min + ~1.5 min). Nothing in `nd.js`/`testground.js` re-emits. The kernel is not committed: a
committed 3.5 MB binary would be stale after every flag day; Pages publishes `build.sh`'s output.

**Price.** Prototype: done (one day). Then (INFERRED): landing ~hours of judge; plants menu 0.5 day;
escrow / generators / meter demos 0.5 day each; two Worlds in a tab 1 day; IndexedDB Store +
reopen-on-reload 0.5 day; the relay and guest-book resident for (B) 2–3 days; the table JSON into
`Emit/` 1 hour; docstring-derived glossary 0.5 day; a reproducible-kernel check (hash printed in the
World window, rebuilt by CI or by Ember) 0.5 day.

**The one way it is wrong.** In (A) every party is the same honest program in one tab, so immersion
teaches the thing nano is NOT for: a system where the writer can be trusted. What nano is for — members
who consent by re-execution against a writer they do not trust — is invisible until the writer lies.
So the plants are not a later nicety; the Writer menu (§4, sequence item 2) is the second thing to
build, and until it exists the testground demonstrates mechanism, not the guarantee. The (B) caveat
is its twin: a visitor re-executes with code and a sponsor key the page's publisher chose; it is a
demonstration of the check, not a trust anchor, until the kernel's hash is reproducible from source.

## 8. The sequence after

1. ~~Land the prototype~~ landed 36c4ea5f under CLIENT (`Web/`, `testground/`, CLIENT-41; the byte ABI `Web/c/glue.c` is an `extern_lib` like `Host/c`).
2. The Writer menu (cv 01a17a48-b31e): the rows' plants as a switch on the in-tab writer (`Rows.Writer.Params`), each with the refusal the visitor's follow raises.
3. Demos as argv: escrow, generators, the meter.
4. Many Worlds in a tab (`Ground` → an array of writers): the time-lock and the fork demos.
5. The Store and custody in IndexedDB; reload = `Host.openWith`.
6. Move the table JSON into `Emit/` (CODEC); emit refusal docstrings for the glossary.
7. (B) (cv 01a17a48-b346): a WebSocket face on the supervisor's mux; a guest-book resident with `enroll:N`; join over an invitation in the tab; the inbox demo against the real model.
8. Reproducible kernel hash shown in the World window; Ember publishes `testground/` to Pages.
