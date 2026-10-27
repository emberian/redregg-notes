# DESIGN-QA — what nanodregg's quality assurance is for, and the program that replaces scripted rows with generated, differential and emitted evidence (real 2026-10-26)

Ember, real 10-26, asked to approve one gate (compiled hash/signature code checked against the
interpreter): "instead of just saying yes (it would be fine), I push back and ask: maybe we should be
being more ambitious about our QA or other testing processes."

Labels: **MEASURED** = run on hbox on 10-26 in `/tank/dregg-build/nanodregg/wt/qa` at origin/main
f193a3e (+ this lane's two files); **READ** = read in the tree or the reader memos; **INFERRED** = my
reasoning, not run. Inputs: `readers/VERDICT-20261024.md` §3 and §8, the nine `readers/HOLISTIC-*.md`,
`readers/COLLATION-20261024.md` (cited as A1…A23, B1…B6, Q1…Q6), nano's `gates/`, `decisions/gates.md`,
`CHARTER.md`, `promo/DESIGN-TESTGROUND.md`.

---

## ⚑ What is worth a lane (real 2026-10-27, Ember: "I keep seeing certificate pin and vector rechecking and checking and rechecking. We're not doing real work.")

**Two pieces of this design are worth a lane: Q5 and Q6.** They are the only pieces that DELETE
instruments and that get their tests from the spec instead of from someone's memory of it. Every
other piece re-checks something already checked and is marked **not worth a lane** below. Their
work, where any exists, is parked, not landed.

### Q5: Lean-emitted traces replace the Rust stand-ins

- **Today.** `client/tests` hold `ScriptedFollow`, a Rust re-implementation of follow, plus:
  - receipt lines typed by hand;
  - Python follow stand-ins;
  - a Rust copy of the Bell's patience.

  Each test checks that Rust agrees with its author's memory of the Lean. That is how A6 (the
  attempt store re-submits after `uncertain`) went unseen: the stand-in did the next step by hand.
- **The change.** The protocol rows already record every operation on both sockets.
  1. `rows --emit-trace NAME` writes one row's exchange as frames: the bytes `nd` must send, and the
     bytes follow and custody answer.
  2. A generated Rust test (the `emit-rust` pattern) replays `nd` against a peer that speaks exactly
     those frames, and fails on the first byte `nd` sends that the trace does not hold.
  3. A lying peer's script comes from the Lean row that defines the lie, never from the test's author.
- **What it deletes.** `ScriptedFollow`, every hand-typed receipt and follow stand-in in
  `client/tests` and `launcher/tests`, and the Rust copies of Lean constants they carry.
- **What it lets the system do.** The client is tested against what the protocol actually says. A6
  reds on its first byte the day the trace exists. Any later change to the protocol moves the Rust
  tests with it, with no hand edit.
- **Order.** It rides RUST's move of the attempt machine into follow. Emit the traces of the rows
  that move first.

### Q6: a generated adversarial Host, judged by the member-level spec

- **Today.** 51 hand-written protocol rows (`Protocol/Rows.lean`) and 28 `Sys` harness booleans
  (`Protocol/Rows/Loopback.lean:53–115`). Each boolean is one adversary move that someone thought of,
  with a row that turns it on. A3 (the frame bound at the deployed page budget), A7 (a lying cancel),
  D3 (swapped continuations), A8 (an honest shutdown read as a lie) and PROTOCOL-73 (endless re-send)
  were each a move no row made.
- **The change.** One seeded generator in Lean, in kernel-sim's shape, over the real
  `Protocol.Command.start/step` and the real writer, at deployed parameters.
  1. **Its moves are drawn from the wire grammar:**
     - deliver, drop, duplicate or reorder frames;
     - swap continuations;
     - answer any status to a lookup or a cancel;
     - serve a head that is stale, forked or ahead;
     - serve pages at every size up to the deployed budget;
     - stop the writer mid-command;
     - restart follow.
  2. **Its oracle is the member-level spec** (HOLISTIC-PROTOCOL §2.4), as a decidable check of each
     trace:
     - every message offered for signature is a planned call;
     - `done ok` means the member's own World journals that call;
     - `refused` and `expired` are final;
     - the member's World is a fold of the writer's log;
     - each command ends within a named number of exchanges.
  3. **The property runs before anyone proves it.** A statement the generator refutes is not worth
     proving, and today clause (ii) is false (D2, D3).
- **What it deletes.**
  - The 28 `Sys` booleans: they become moves.
  - The per-row plants: replaced by one control, the generator with a move removed, which must red
    the oracle.
  - The 51 rows as scenarios: they become named seeds and regressions the generator must reach.
    A row it cannot reach is a move its grammar lacks.
- **What it lets the system do.** It finds protocol defects of the kind six of the collation's were,
  with no one writing the scenario, and the member-level theorem is written against a statement that
  survived generation.

### Not worth a lane

| piece | why not |
|---|---|
| Q1 | landed (GATES-27, 5527b018); it stays as it is and grows no further |
| Q2 | the ledger-sim and hosting-sim TRACE lines land once, as they are (green and trivial); lang-journey, host-sim and rows by name are not worth a lane |
| Q3 | re-checking. Built and measured, then parked: see the measurements below. Not landed |
| Q4 | re-checking (vectors three ways). Parked: see below. Not landed |
| Q7, Q8 | ride HOST's Store cut and RUST's attempt move. When those land, the crash model and the small-scope check belong to those owners' own tests, not to a QA lane |
| automated mutants, more plants, more vector tables | instruments about instruments |

**Q3 measured before the stop** (hbox, 10-27, load 18–35):
- A compiled `host follow` catch-up of THE BAR's 1000-record Store was captured byte for byte (447,859 B
  in, 12,345 B out) and replayed into `lean --run Host/Main.lean follow` over the same genesis Store.
- The replies and all 5 Store files (771,098 B) were identical.
- Times: compiled 2.2 s, interpreted 185.8 s (84×). The whole BAR run with it took 418 s.
- Found on the way: the interpreter cannot run inside `nd-supervise`, because Lean's runtime needs
  `/proc` to locate itself and the sandbox never mounts it.

**Q4 measured before the stop:**
- RFC 8032 TEST 3 and TEST 1024 (the 1023-byte message), SHA-512's 2-block and million-`a` vectors
  pass compiled (0.34 s) and in Rust with ed25519-dalek and sha2 (0.30 s). OpenSSL 4.0.3 and `shasum`
  confirmed the vectors.
- Kernel cost: a 2-block hash takes 17 s and 1.7 GB, and a 9-block one ~14 GB unstaged. The staged
  form was not finished.
- The patch is in `qa-scratch/q3q4-parked.patch` on hbox.

---

## 0. The answer in one page

**The gap.** Every theorem is about a Lean TERM. The kernel checks a handful of closed instances of
it (`decide +kernel` on KATs and a sample of codec rows). The binary that runs is that term after
the compiler: LCNF → IR → EmitC → cc → the compiled runtime. It is trusted on the compiler's word.
CODEC-4 already measured that word false once: a C string literal that fuses two escapes
(GATES-20y). Nothing measured the compiler across the code the deployment runs.

**The seed (ROOT's), built today.** The system's own accountability model, turned on its compiler.
The writer runs compiled. A FOLLOWER UNDER THE INTERPRETER re-derives the same work. A
disagreement is a named refusal. The first piece is landed as GATES-27 (`gates/interp.py`, one
`script:` row). kernel-sim's seeds run compiled and under `lake env lean --run`, and must print
byte-identical stdout, stderr and exit. Each seed prints one `TRACE` line, which commits to the Host
World's chain, its four roots, every verdict name in order, and the stream of hash marks.
- MEASURED: seeds 1, 2 and 3 agree, 3,054–3,064 bytes each.
- MEASURED: the interpreter is **85–160× slower**, 230–316 s a seed against 1.5–2.7 s, under a load
  average of ~11.
- MEASURED: a mutant binary (one hash domain changed) reds on the `TRACE` line.
- MEASURED: the known-red control (the interpreter given the next seed) reds.
- MEASURED, ad hoc (not yet rows): four more exes agree byte for byte compiled vs interpreted:
  - `ledger-sim 1` (9.3 s interpreted);
  - `hosting-sim 1` (4.6 s);
  - `lang-journey` (349 s against 17 s, 98,887 bytes identical);
  - `host-sim 1` (515 s against 11.6 s).
- MEASURED: the deployed `host` binary runs under the interpreter. That needs a 30-line dynlib shim
  for its two C-extern modules (§2.3); `host check` agrees byte for byte on a fresh Store.

**The ambition beyond the seed.** In the field's terms, nano's QA is mostly **one technique**:
mutation analysis, as plants and known-red controls. It is applied to **scripted examples**: 51
protocol rows with 28 harness booleans, Rust tests against hand-written stand-ins. Plants are good
vacuity hygiene (VERDICT §3), and they cannot find the next defect. The collation's worst defects
were each in a place no script looked:
- A3, the frame bound: INFERRED from arithmetic; the rows page at a toy size.
- A6, the attempt store: its promise was tested by doing the next step by hand.
- A7, the lying cancel: no row lies about a cancel.
- PROTOCOL-73's endless re-send: no row exercises it.

nano is unusual in that **the spec runs**. `World.admit` is the receive path, and compiled Lean is
the deployed code. So it can have, cheaply, what most verified systems pay dearly for: generated
environments judged by the spec, traces emitted by the spec to drive the untrusted code, and every
piece of compiled code held to an independent evaluator of the same term.

**The program, in order** (§2). Each step is a new thing the system refuses or measures, never a
ritual (memory: method items that soothe ROOT are not progress).

| # | piece | what it makes true | cost per batch | cost to build |
|---|---|---|---|---|
| Q1 | interpreter differential over kernel-sim (**BUILT**, GATES-27) | the compiled kernel, codecs, cSHAKE256 and Ed25519 agree with the interpreter on 2 generated seeds per batch | ~13 min of one core (control + 2 seeds) | done |
| Q2 | every verdict exe interpreted, each with a `TRACE` line (ledger-sim, hosting-sim, lang-journey, host-sim; rows by name) | the same for LANG's evaluator, the escrow, the controller, HOST's loop under crashes | +~15 min of cores, in parallel | days; one TRACE line per owner |
| Q3 | the interpreter follower on THE BAR's Store | the deployed follow's code, interpreted, re-derives what the compiled writer wrote at the charter's 1000 records | INFERRED ~3–6 min | ~1 week (§2.3) |
| Q4 | codec-vectors three ways + compiled KATs (CODEC's proposal; Q5 of the collation) | compiled = kernel = emitted Rust on every pinned vector, multi-block SHA-512, RFC 8032's 1023-byte TEST | seconds | 1–2 weeks |
| Q5 | Lean-emitted traces drive the Rust tests | no Rust test holds its author's copy of Lean behaviour; A6 is red the day it lands | seconds | 2–3 weeks |
| Q6 | a generated adversarial Host over `Protocol.Command`, judged by the member spec | the 51 rows become seeds of one generator; the 28 booleans become its moves; A3/A7/D3/PROTOCOL-73 are reachable by construction | minutes (seeded, like kernel-sim) | 3–4 weeks |
| Q7 | crash injection as a model: one crash-semantic Store shared by proofs and sims | every crash point of `serve`, generated, not the ones a plant named | minutes | weeks (HOST's structural change) |
| Q8 | the attempt store checked over all interleavings at small scope, in Lean | "at most one call per intent across crashes, timeouts, re-runs", checked exhaustively at small scope | seconds | after RUST's move of the attempt machine into follow |

**What it deletes** (§3). The 28 `Sys` booleans (Q6). `ScriptedFollow` and every hand-typed receipt
and follow stand-in in `client/tests` (Q5). The per-row plants of the protocol rows: the generator's
own known-red control replaces them (Q6). `gates/cbytes.py vectors` once Q4's compiled column covers
its literal classes. Nothing is deleted before its replacement is a row that reds.

**The one way it is wrong** (§4). The interpreter shares LCNF and IR with the compiler, so Q1–Q3 see
EmitC, cc and the runtime, and nothing above them. A generated adversary generates only the moves
its grammar names. Both are priced below, with what would show each.

---

## 1. What QA is FOR here, in the field's terms

nano's trust story is **theorems about the term, plus re-execution by followers**. QA has three
jobs that neither does:

1. **The term is the binary.** Theorems are about the Lean term; the binary is the compiler's output.
2. **The statement is the right one.** A true, non-vacuous theorem can still state the wrong
   property: A1, A4, A5, A9, A15.
3. **The untrusted parts behave.** Rust, the OS, the disk and the network are outside every theorem.

The table places each established technique against those jobs.

| technique (field) | what it measures | nano HAS | nano MIMICS (scripted) | nano LACKS |
|---|---|---|---|---|
| **Differential testing** (McKeeman 1998; Csmith, Yang et al. PLDI 2011; EMI, Le et al. PLDI 2014) | two implementations of one spec agree on many inputs | `cbytes.py vectors`: 14 literals, compiled vs interpreted (GATES-20y); the testground's wasm-vs-native over 368 recorded calls (DESIGN-TESTGROUND §1) | `codec-vectors.tsv` (293 rows) is evaluated by ONE evaluator, the generator's own definition | compiled vs interpreted vs kernel over the deployed surface: **Q1 (built), Q2–Q4** |
| **Translation validation** (Pnueli, Siegel, Singerman 1998; Necula PLDI 2000) | each compiler run checked, not the compiler | nothing | nothing | Q3 is runtime translation validation of the follower, per batch |
| **Model-based testing / generated environments** (QuickCheck state machines, Hughes 2016; FoundationDB's deterministic simulation; TigerBeetle's VOPR; Jepsen) | a generator draws operations and faults; an oracle judges every trace | **kernel-sim**: a seeded generator over the REAL `Receive.submit`, judged against expectations by refusal name, restarted by fold, with the follower re-deriving. This is real MBT, and the best QA asset nano has | **protocol rows**: 51 hand-written scenarios + 28 `Sys` booleans, each a hand-enumerated adversary move (READ `Protocol/Rows/Loopback.lean:53–115`) | a generated adversary above the kernel: **Q6** |
| **Property-based testing against an executable spec** | random inputs, a decidable property of the spec | `World.admit` IS the spec and runs; kernel-sim checks follower = writer, conservation and refusal names | per-row expectations | the member-level spec (HOLISTIC-PROTOCOL §2.4's four clauses) as a decidable check on generated traces, run before it is proved: **test the theorem statement first** (Q6) |
| **Trace-driven conformance** (trace validation against TLA+, Cirstea, Kuppe, Loillier, Merz, Pressler 2024; eXtreme modelling at MongoDB, Davis, Schvimer, Zhou, VLDB 2020) | the implementation's traces replayed against the model | the rows' judge compares OBSERVED ops with declared ones, with a proved oracle (`judge_members_pass_iff`) | Rust tests against `ScriptedFollow`, hand-typed receipt lines, Python follow stand-ins (HOLISTIC-RUST §4.2) | Lean-emitted traces as the only source of expected behaviour in Rust tests: **Q5** |
| **Crash and fault injection** (ALICE, Pillai et al. OSDI 2014; CrashMonkey, Mohan et al. OSDI 2018; FSCQ, Chen et al. SOSP 2015) | every crash point of a persistence protocol | `Host.Sim.MemStore` (`synced`, `pending`, `crashImage`); host-sim's crash plants; store-plants against the live binary | crash points chosen by the plant's author | one crash-semantic Store model used by proofs AND sims, with generated crash points (HOLISTIC-HOST §2.2): **Q7**; ALICE-style checks of `client/src/fsx.rs` (A18) |
| **Mutation analysis** (DeMillo, Lipton, Sayward 1978; mCoq, Celik et al. ASE 2019; vacuity, Kupferman–Vardi) | would anything go red? | plants, known-red controls with the mutation asserted first (GATES-15; HOLISTIC-GATES: A−) | (it IS the method) | automated mutants (cargo-mutants on the Rust; a Lean mutator over deployed defs) as the adequacy measure for the generators, not per theorem |
| **Model checking at small scope** (Alloy's small-scope hypothesis, Jackson 2006; TLC) | every interleaving up to a bound | nothing | `Protocol.Attempt` theorems per step | the attempt store over all interleavings of crash/timeout/re-run at small scope, by exhaustive enumeration in Lean (law 1: one language, no TLA+ toolchain): **Q8** |
| **Compiler validation by an independent evaluator** (CompCert's validated passes; CertiCoq; extraction testing) | the deployed artefact agrees with the term's semantics | the kernel on KATs (single-block only, Q5 of the collation) | `cbytes.py` (one literal class) | **Q1–Q4** |

**What QA is FOR in nano, in one line.** It closes the distance between the statements and the
running system from three sides. Q1–Q4 tie the compiler's output to the term. Q6 and Q8 check
whether the statements are the ones needed, by running candidate top-level properties over
generated traces before anyone proves them. Q5 and Q7 hold the untrusted parts to the spec's own
expected behaviour. Mutation analysis stays as the hygiene that proves each instrument can fail.

---

## 2. The program

### 2.1 Q1: kernel-sim under the interpreter (BUILT: GATES-27)

**How.** `gates/interp.py EXE ARG…` runs `$ND_LEAN_BIN/EXE ARG…` and
`lake env lean --run <EXE's root>.lean ARG…`. The root is read from `lakefile.lean`, the one place it
is named. The two must print byte-identical stdout and stderr and exit the same.
- The compiled stdout must hold a `TRACE ` line. An exe compared here prints a function of what it
  computed, not only counts.
- kernel-sim's `Gen.traceLine` commits, per seed, to:
  - the Host World's `chain` (every admitted Turn and recorded refusal, linked under cSHAKE256);
  - its trie, journal, refusals and rows roots, and its origin;
  - height, steps and allowance;
  - every verdict name the run met, in order (1,210 at seed 1);
  - its failures;
  - the stream of hash marks the counting env wrote (18,072 at seed 1).
- The row is `script:gates/interp.py  kernel-sim 1 ; kernel-sim 2  INTERP AGREE  kernel-sim 3 --harness-control`.
- The control gives the interpreter seed 4, so the comparator must read two runs as different.

**What the interpreter is, and so what this measures** (READ: Lean's `ir_interpreter.cpp` behaviour,
INFERRED for the details). `lean --run` elaborates the root file. Every imported module's IR comes
from its `.olean` and is interpreted. Lean's own runtime and core (`Init`, `Std`, the `@[extern]`
primitives on `ByteArray`, `UInt64`, `Nat`) are native in both runs.
- **It sees:** EmitC (the CODEC-4 class), the C compiler and its flags, the compiled calling
  conventions (boxed vs unboxed, borrowed parameters, destructive update when the refcount is 1),
  the initialisation of closed terms, and every user `@[extern]` it reaches.
- **It does not see:** an LCNF or IR pass that is wrong in both runs, nor a bug in a core primitive.
  The kernel is the evaluator for those, at the sizes the kernel reaches (Q4).

**MEASURED.**

| run | compiled | interpreted | ratio | verdict |
|---|---|---|---|---|
| kernel-sim 1 | 1.2–2.7 s | 183 s (quiet) to 299 s (load ~11) | 85–150× | agree, 3,064 B |
| kernel-sim 2 | 1.5 s | 244 s | 160× | agree, 3,054 B |
| kernel-sim 3 vs interpreted 4 (control) | 2.4 s | 253 s | — | **RED**, first difference the TRACE line |
| mutant kernel-sim 1 (seed domain `…/seeX`) vs interpreted 1 | 2.7 s | 232 s | — | **RED** at the TRACE line (and 8 count lines: a content-addressed run moves its trie shape with its bytes) |

The interpreter's peak RSS is 790 MB a seed. runs.py's 600 s deadline (GATES-16) allows one seed a
run with 2× margin at a load average of 11.

**What it would have caught.**
- **CODEC-4 / A16:** yes, on any literal the sim reaches, in any spelling. The cbytes vectors prove
  the class exists, and this row proves the deployed kernel path is not hit by it.
- **Q5 of the collation** (compiled hash/Ed25519 never run on vectors): partly. Every sim signature
  is made by compiled `Ed25519.sign` and checked by compiled `verify`, and the interpreter re-derives
  both. A sign/verify pair that is consistently wrong in both runs is Q4's job (KATs).

**The first control was blind, and the row found it.** The obvious control was the exe's own
`--harness-control`. MEASURED: under one seed it changes nothing, because kernel-sim judges its
planted arms only over 16 or more seeds, so the control read AGREE. The control is now the moved
seed, and a control that reds for any other reason (no TRACE line, a crash) is printed without the
control's name, so runs.py reads the harness as broken. This is the minted lesson again: a
falsifier that stopped falsifying, caught by the control discipline (GATES-15).

### 2.2 Q2: every verdict exe, each with a TRACE line

MEASURED, ad hoc (compiled vs `lake env lean --run`, `cmp` of stdout):

| exe | compiled | interpreted | identical? | needs |
|---|---|---|---|---|
| ledger-sim 1 | 0.57 s | 9.3 s | yes | a TRACE line (LEDGER) |
| hosting-sim 1 | 0.11 s | 4.6 s | yes | a TRACE line (HOSTING) |
| lang-journey | 17.3 s | 349 s (~220 s of it module initialisation: an interpreted run with a bad argument took 222 s to print usage) | yes, 98,887 B | it already prints ids; one TRACE line (LANG) |
| host-sim 1 | 11.6 s | 515 s | yes | a TRACE line (HOST); 515 s is too near the 600 s deadline, so the row runs a seed's phases separately or host-sim gains a smaller `--steps` |
| rows | 339 s | not run (INFERRED hours) | — | per row by name (`rows NAME`): the deployed-parameter rows with Ed25519 are the ones worth it |

**Cost per batch.** About 6 runs of up to 6 min each. They are parallel across judge slots, so the
convergence's wall clock grows by about one run, not six.

**What it makes true.** The compiler is measured on LANG's metered evaluator (the consensus
semantics), the escrow, the controller's decisions and HOST's loop under crashes. That is most of
the code that decides anything.

### 2.3 Q3: the interpreter follower on THE BAR

This is ROOT's seed taken literally: the deployed follow's own code, interpreted, re-deriving every
event the compiled writer wrote at the charter's 1000 records.

**Can `host` run interpreted?** MEASURED: yes, with a shim. `Host.File` and `Host.Sock` declare
`@[extern]` C (`Host/c/*.c`). The interpreter looks up the module's own BOXED wrapper
(`lp_nanodregg_…___boxed`), which lives in the module's emitted C, not in `libndhost.a`.
1. A shared library of `.lake/build/ir/Host/{File,Sock}.c` plus `file.o` and `sock.o`, plus a
   one-line stub for the one foreign initialiser (`initialize_nanodregg_Host_Loop`), loads under
   `lean --load-dynlib`.
2. `host check STORE` then prints the same STATUS line interpreted as compiled.
3. Those two modules run native inside the interpreted run. They are the IO shim, already in the
   TCB table, so the coverage lost is small and named.
4. The right form is a lake target for that dynlib, built from source like `ndhost` (law 9). That
   is not the hand `cc` used here.

**Which code.** By A9 the deployed follower is `Protocol.Command.absorbStep`, not
`Kernel.Receive.audit`. The interpreted follower must run `host follow`'s path, or this measures a
twin.
- Two shapes, in order of fidelity:
  - **(a)** `bar.sh` runs ONE of its three follows under the interpreter. That is the deployed
    command, driven by real `nd` over the real socket. The price: the interpreted follow must see
    the toolchain and `.olean`s inside its confinement, and THE BAR's clock limits do not apply to
    that actor (it is marked, and its follow-reopen is not a BAR measurement).
  - **(b)** A one-shot catch-up: an interpreted `host follow` over a copy of the writer's Store,
    absorbing every page from genesis. This needs a non-interactive entry to follow's catch-up, the
    same function `nd`'s first command drives. That is not a new verb (law 1).
- I would build (b) first: it is cheaper, it has no clock interaction, and it is the same
  `absorbStep`.

**Speed** (INFERRED from Q1's rates: ~0.2 s an interpreted verdict at the deployed parameters,
Ed25519 dominating): 1000 records ≈ 200 s, plus ~5 s to load. One run per batch fits the 600 s
deadline. The first build step is to MEASURE it on a real BAR Store. If it is too slow, the row
follows the last N records from a base.

**What it would have caught.** Any miscompile on the follower's path: page decode, frame decode,
`absorbStep`, the base reopen. This is the path every member's safety rests on, and today it is
evaluated only compiled.

### 2.4 Q4: codec-vectors three ways, and compiled KATs

This is CODEC's own structural change (HOLISTIC-CODEC §4.1), the gate Ember was asked to approve,
made general. Every row of `gates/codec-vectors.tsv` (293 rows; 57 of them `lang/package/7`) is
evaluated by three evaluators:
- **the kernel** (`decide +kernel` on a sample, or the generator's definition);
- **the compiled exe**;
- **the emitted Rust** (a generated `cargo test`).

Add the published KATs as rows of their own sites: NIST SHA-512 multi-block and RFC 8032 TEST 1024
(1023 bytes). Collation Q5 notes that every hash KAT today is single-block, while deployed calls are
multi-block. With Q1 in place the interpreter adds nothing to the codec rows: a fourth evaluator of
the same IR. **The kernel is the column that matters here**, because it is the only evaluator
independent of LCNF.

### 2.5 Q5: Lean-emitted traces drive the Rust tests (law 1: one source of expected behaviour)

**Today** (READ, HOLISTIC-RUST §2.4 and §4.2): `client/tests/run.rs` holds `ScriptedFollow`, a Rust
reconstruction of follow. Receipt lines are hand-typed; Python follow stand-ins exist; the Bell's
patience is copied into Rust. Each confirms only that Rust agrees with its author's memory of Lean.

**The change.** The protocol rows already record every op on either socket, observed against
declared (`judge_members_pass_iff`). A `rows --emit-trace NAME` writes that row's exchange as frames:
the bytes `nd` must send, and the bytes follow and custody answer. A generated Rust test (the
`emit-rust` pattern, checked by `gates/generated.tsv`) replays `nd` against a peer that speaks
exactly those frames, and fails on the first byte `nd` sends that the trace does not hold.
- Where a stand-in is unavoidable (a lying Host), its script comes from the Lean row that defines
  the lie (HOLISTIC-RUST's own wording), never from the test's author.

**What it would have caught.**
- **A6** (the attempt store). The emitted trace of "re-run after `uncertain`" holds a `lookup` of the
  frozen call. Today's `nd` sends a fresh `submit`, so the test reds on its first byte, the day it
  lands.
- **A8** (`refused stopped` at an honest shutdown) is visible as soon as a trace of a stopping writer
  exists.

**Deletes.** `ScriptedFollow` and every hand-written follow or receipt stand-in in `client/tests` and
`launcher/tests`.

### 2.6 Q6: a generated adversarial Host over `Protocol.Command`, judged by the member spec

**Today.** There are 51 rows (READ `Protocol/Rows.lean`) and 28 `Sys` booleans (READ
`Protocol/Rows/Loopback.lean:53–115`: `resendFresh`, `trustCancel`, `staleRange`, `dropRange`, …).
Each boolean is a hand-enumerated adversary move with a row that turns it on. HOLISTIC-PROTOCOL
§4.2: "Stop answering each finding with a new scripted row and a new harness flag."

**The change.** A generator in Lean, in kernel-sim's shape: seeded, deployed parameters, the real
`Protocol.Command.start/step`, the real writer.
1. **The environment's moves are drawn from the wire grammar.** Every reply constructor, every
   frame field, every relay act:
   - deliver, drop or duplicate a frame; reorder two;
   - swap continuations between commands (D3);
   - answer a lookup or a cancel with any status (A7);
   - serve a head that is stale, forked or ahead;
   - serve a page at every size up to the DEPLOYED page budget (A3: the rows page at 65,541, not
     261,120);
   - draw argv sizes up to their bound (A3);
   - stop the writer mid-command (A8);
   - restart follow.
2. **The oracle is the member-level spec**, as a decidable property of the trace: the four clauses
   of HOLISTIC-PROTOCOL §2.4.
   - (i) every message offered for signature is `callMessage u` for a planned `u`;
   - (ii) every `done ok` implies the member's own World journals the planned call;
   - (iii) `refused`/`expired` is final;
   - (iv) the member's World is a fold of the writer's log;
   - plus one liveness bound: each command ends within a named number of exchanges (PROTOCOL-73's
     endless re-send).
3. **Run the property before proving it.** Today (ii) is FALSE by D2 and D3, and the generator finds
   that in seconds. The theorem is then written against a statement that survived generation, which
   is the cheapest vacuity check there is: a statement the generator refutes is not a statement
   worth proving.
4. **The 51 rows become named seeds and regressions.** The generator must reach each row's scenario
   as an instance. That is a check that its grammar covers the known attacks. The 28 booleans
   become moves and are deleted from `Sys`.

**What it would have caught.** A3 (frame bound at the deployed budget), A7 (lying cancel), D3
(continuation swap), A8 (honest shutdown read as a lie), A13 (endless retry class in the resident,
if the generator drives Hosting's resident too), PROTOCOL-73. Six of the collation's protocol-layer
defects. None was caught by a row.

**Cost per batch.** Minutes: kernel-sim is 1–3 s a seed compiled, and the protocol machine is
lighter than the kernel. Its seeds also run under Q1's interpreter row.

### 2.7 Q7: crash injection as a model

HOLISTIC-HOST §2.2's missing cut is the Store as an effect signature (`append`, `sync`, `rename`,
`read`) with a crash semantics: a crash keeps `synced ++ prefix(pending)`. That is
`MemStore.crashImage` promoted from test harness to THE model, used by:
- **the proofs** (`Host ⊑ Kernel` across the crash edge);
- **the simulator**, which draws a crash at every effect index, not at the points a plant named.

The Rust side gets the ALICE-style twin: `fsx::create_once` writes in place, so a crash leaves an
empty `rotation` (A18). A crash-point enumerator over the client's file protocol would have read
that red.

### 2.8 Q8: the attempt store at small scope

After RUST's structural change (the attempt machine moves into follow), the property is "for each
intent, across any interleaving of crashes, timeouts and re-runs, at most one call commits". Check it
by exhaustive enumeration in Lean over 2 intents, 3 crashes and 3 re-runs: Alloy's small-scope
hypothesis, no TLA+ (law 1, one language). Prove it after the enumeration has failed to refute it.
A6 is the defect it exists for.

---

## 3. What to DELETE, and when

| deleted | replaced by | when |
|---|---|---|
| the 28 `Sys` booleans in `Protocol/Rows/Loopback.lean` | Q6's generator moves | when Q6 reaches each row's scenario as an instance |
| per-row plants of the protocol rows | Q6's known-red control (a generator with a move removed must red the oracle) | same |
| `ScriptedFollow`, hand-typed receipt lines, Python follow stand-ins, Rust copies of the Bell's patience | Q5's emitted traces | per test, as each gains a trace |
| `gates/cbytes.py vectors` | Q4's compiled column over the same literal classes | when Q4's table holds them; `cbytes.py scan` (the pre-build source gate) stays |
| kernel-sim's standing `--seeds 64` arm count | nothing: it stays | Q1 adds; it does not replace the sim's own judgment |

**Not deleted:** plants as vacuity hygiene (VERDICT §3: keep them, stop treating them as
correctness); the known-red control discipline (GATES-15, which caught this lane's own blind
control).

## 4. The one way it is wrong, and what would show it

1. **The interpreter shares the frontend compiler.** Q1–Q3 compare two back ends of one IR. A
   miscompile in LCNF (specialisation, `@[csimp]`, `implemented_by`) is identical in both and
   invisible. What shows it: the kernel column (Q4) disagreeing with both. That column reaches only
   small closed instances (memory: one Poseidon2 permutation under whnf is 47 GB), so the frontend
   stays measured at KAT size only. That is a real limit, stated, not a phase.
2. **The interpreter cannot keep up.** At 85–160× it is no FOLLOWER in the deployed sense: it
   re-derives a sample per batch, not every event live. MEASURED: one seed at 230–316 s, lang-journey
   at 349 s, host-sim at 515 s against a 600 s deadline. If Q3's 1000-record follow measures above
   the deadline, the row follows a suffix. What shows it: the `interp:` timing line each run prints.
3. **A generated adversary never generates the real attack.** Q6's moves are the wire grammar's
   constructors. An attack that is not a wire event (a timing channel, a resource exhaustion across
   Worlds) is outside it, and A1 (a check ORDER inside the kernel) is a statement defect no
   environment generator reaches. What shows it: a defect found by a reader that the generator, once
   given the move, reaches in under N seeds. Then the grammar was missing a move, and the move is
   added. The reverse also counts: a row the generator cannot reach as an instance is a known attack
   it does not cover, and that is red.
4. **Agreement is not correctness.** Compiled = interpreted = kernel = Rust can all be wrong against
   the intent. That is the statement's job (Q6's run-the-property-first, and the spec layer GATES
   proposes), not the evaluators'.

## 5. Order and why

Q1 is first: it is the cheapest piece that measures the compiler on real work, and it is built.
- **Q2** is days, and multiplies Q1's coverage by the number of deciding layers.
- **Q3** is the deployed follower, so it is the most faithful, but it needs a lake dynlib target
  and a catch-up entry.
- **Q4** closes the frontend gap at KAT size and is CODEC's.
- **Q6** has the largest yield: six of the collation's defects, plus the deletion of 28 booleans
  and their plants. It follows Q2 because its seeds should be interpreted from day one.
- **Q5, Q7 and Q8** ride their owners' structural changes (RUST's attempt move, HOST's Store cut);
  building them before those changes would test code about to move.
